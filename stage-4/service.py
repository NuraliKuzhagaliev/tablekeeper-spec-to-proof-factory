"""Linearizable transitions: occupancy, history, agreements and receipts."""
import copy
import json
import re
import secrets
import threading
import uuid
from datetime import datetime, timedelta

from domain import (APIError, UTC, bounds, check_password, email, fail, field, fixed_instant,
                    hash_password, identifier, local_date, local_datetime, members, overlaps,
                    party, positive_integer, read_timestamp, resolve, same_json, selected_members, timestamp)
from history import changes, entry, native_history, public
from json_value import add_numbers, dumps
from policies import applicable_terms, complete_policy, decided_booking, rules_config
from state import empty_state, fixture_state, imported_state, restaurant_from_fixture


def new_id(prefix):
    return prefix + uuid.uuid4().hex


class Service:
    def __init__(self):
        self.lock = threading.RLock()
        self.state = empty_state()

    def request(self, method, path, query, body, headers):
        with self.lock:
            return copy.deepcopy(self.dispatch(method, path, query, body, headers))

    def user(self, headers):
        match = re.fullmatch(r'Bearer ([^\s]+)', headers.get('Authorization', ''), flags=re.IGNORECASE)
        if match is None or match[1] not in self.state['tokens']:
            fail('unauthenticated', 401)
        return self.state['tokens'][match[1]]

    def private_reader(self, headers):
        try:
            return self.user(headers)
        except APIError:
            fail('not_found', 404)

    def restaurant(self, rid):
        identifier(rid)
        if rid not in self.state['restaurants']:
            fail('not_found', 404)
        return self.state['restaurants'][rid]

    def owned(self, reference, uid):
        reservation = self.state['reservations'].get(reference)
        if reservation is None or reservation['user_id'] != uid:
            fail('not_found', 404)
        return reservation

    def receipt(self, uid, path, body, headers):
        key = headers.get('Idempotency-Key', '')
        if not key or not key.strip():
            fail('missing_idempotency_key', 400)
        if len(key) > 255:
            fail()
        scope = json.dumps([uid, 'POST', path, key], separators=(',', ':'))
        previous = self.state['receipts'].get(scope)
        if previous is not None and not same_json(previous['body'], body):
            fail('idempotency_key_reuse', 409)
        return scope, previous

    def cutoff(self, reservation):
        remaining = (read_timestamp(reservation['starts_at']) - datetime.now(UTC)).total_seconds() / 60
        if remaining <= reservation['accepted_terms']['cancellation_cutoff_minutes']:
            fail('cutoff_passed', 409)

    def amended(self, original, body):
        if 'expected_revision' in body:
            expected = positive_integer(body['expected_revision'])
            if expected != original['revision']:
                fail('stale_revision', 409)
        if original['status'] == 'cancelled':
            fail('reservation_cancelled', 409)
        self.cutoff(original)
        restaurant = self.state['restaurants'][original['restaurant_id']]
        if 'table_id' in body and 'table_ids' in body:
            fail()
        selector = {key: body[key] for key in ('table_id', 'table_ids') if key in body}
        chosen = selected_members(restaurant, selector) if selector else list(members(original))
        count = party(body['party_size']) if 'party_size' in body else original['party_size']
        local = (local_datetime(body['starts_at_local']).isoformat(timespec='minutes')
                 if 'starts_at_local' in body else original['starts_at_local'])
        proposed = {**original, 'table_ids': chosen, 'party_size': count, 'starts_at_local': local}
        proposed.pop('table_id', None)
        if len(chosen) == 1:
            proposed['table_id'] = chosen[0]
        if not changes(original, proposed):
            # No-op bookings keep their accepted policy, including when a newer
            # policy could not accept the old fields or duration.
            return copy.deepcopy(original)
        proposed.update(decided_booking(self.state, restaurant,
                         {'table_ids': chosen, 'party_size': count, 'starts_at_local': local}))
        proposed['revision'] = original['revision'] + 1
        return proposed

    def ensure_available(self, candidates, excluded=()):
        others = [record for reference, record in self.state['reservations'].items() if reference not in excluded]
        for index, candidate in enumerate(candidates):
            if any(overlaps(candidate, other) for other in others + candidates[:index]):
                fail('table_unavailable', 409)

    def build_reservation(self, uid, restaurant, body, pending=()):
        candidate = decided_booking(self.state, restaurant, body)
        references = set(self.state['reservations']) | {record['reference'] for record in pending}
        reference = ''.join(secrets.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(10))
        while reference in references:
            reference = ''.join(secrets.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(10))
        candidate.update(reservation_id=new_id('res_'), reference=reference, user_id=uid,
                         status='confirmed', created_at=timestamp(datetime.now(UTC)), revision=1)
        return candidate

    def publish_created(self, candidates):
        histories = {record['reference']: native_history(self.state['restaurants'][record['restaurant_id']], record) for record in candidates}
        self.state['reservations'].update({record['reference']: record for record in candidates})
        self.state['histories'].update(histories)

    def publish_changes(self, candidates, event='changed'):
        changed = {record['reference']: record for record in candidates
                   if record['revision'] != self.state['reservations'][record['reference']]['revision']}
        histories = {}
        for reference, candidate in changed.items():
            history = copy.deepcopy(self.state['histories'][reference])
            history['entries'].append(entry(history, self.state['restaurants'][candidate['restaurant_id']],
                                            self.state['reservations'][reference], candidate, event))
            histories[reference] = history
        agreements = {}
        for sid, agreement in self.state['series'].items():
            if any(occurrence['reference'] in changed for occurrence in agreement['occurrences']):
                replacement = copy.deepcopy(agreement)
                replacement['revision'] += 1
                if event == 'changed':
                    for occurrence in replacement['occurrences']:
                        if occurrence['reference'] in changed:
                            occurrence['exception'] = True
                agreements[sid] = replacement
        self.state['reservations'].update(changed)
        self.state['histories'].update(histories)
        self.state['series'].update(agreements)
        return bool(changed)

    def series_response(self, agreement, pending=()):
        records = {**self.state['reservations'], **{record['reference']: record for record in pending}}
        return {key: agreement[key] for key in ('series_id', 'revision', 'interval_weeks')} | {
            'occurrences': [{**occurrence, 'reservation': public(records[occurrence['reference']])}
                            for occurrence in agreement['occurrences']]}

    def adopt(self, uid, body):
        reference = identifier(field(body, 'anchor_reference', str))
        count, interval = positive_integer(body.get('count')), positive_integer(body.get('interval_weeks'))
        if not 2 <= count <= 12 or interval > 4:
            fail()
        anchor = self.owned(reference, uid)
        if anchor['status'] == 'cancelled':
            fail('reservation_cancelled', 409)
        if any(any(item['reference'] == reference for item in agreement['occurrences']) for agreement in self.state['series'].values()):
            fail('already_in_series', 409)
        self.cutoff(anchor)
        restaurant = self.state['restaurants'][anchor['restaurant_id']]
        local = local_datetime(anchor['starts_at_local'])
        generated = []
        for index in range(1, int(count)):
            try:
                start = local + timedelta(days=index * int(interval) * 7)
            except OverflowError:
                fail()
            candidate = self.build_reservation(uid, restaurant, {'table_ids': list(members(anchor)),
                            'party_size': anchor['party_size'], 'starts_at_local': start.isoformat(timespec='minutes')}, generated)
            # Complete each index, including occupancy, before trying the next.
            self.ensure_available([*generated, candidate])
            generated.append(candidate)
        agreement = {'series_id': new_id('series_'), 'user_id': uid, 'restaurant_id': restaurant['id'],
                     'revision': 1, 'interval_weeks': interval,
                     'occurrences': [{'index': index, 'reference': record['reference'], 'exception': False}
                                     for index, record in enumerate([anchor, *generated])]}
        response = self.series_response(agreement, generated)
        self.publish_created(generated)
        self.state['series'][agreement['series_id']] = agreement
        self.state['restaurant_revisions'][restaurant['id']] += 1
        return response

    def availability(self, query):
        if any(key not in query for key in ('restaurant_id', 'date', 'party_size')):
            fail()
        if 'explain' in query and query['explain'] != 'true':
            fail()
        if not re.fullmatch('[0-9]+', query['party_size']):
            fail()
        count = party(int(query['party_size']))
        day = local_date(query['date'])
        original = self.restaurant(query['restaurant_id'])
        accepted = applicable_terms(self.state, original, query['date'])
        restaurant = rules_config(original, accepted)
        slots = []
        hours = bounds(restaurant, day)
        if hours:
            local, close = hours
            zone = restaurant['timezone']
            closing = fixed_instant(close, zone)
            while local < close:
                try:
                    start = resolve(local, zone)
                    if restaurant['reservation_duration_minutes'] <= (closing - start).total_seconds() / 60:
                        end = start + timedelta(minutes=int(restaurant['reservation_duration_minutes']))
                        available, options, explanations = [], [], []
                        tables = {table['id']: table for table in restaurant['tables']}
                        def free(selection):
                            candidate = {'restaurant_id': restaurant['id'], 'table_ids': selection, 'status': 'confirmed',
                                         'starts_at': timestamp(start, zone), 'ends_at': timestamp(end, zone)}
                            return not any(overlaps(candidate, record) for record in self.state['reservations'].values())
                        for table in restaurant['tables']:
                            capacity, no_overlap = table['capacity'] >= count, free([table['id']])
                            if capacity and no_overlap:
                                available.append(table['id'])
                                options.append({'table_ids': [table['id']], 'capacity': table['capacity']})
                            explanations.append({'table_id': table['id'], 'policy_version': accepted['policy_version'],
                                                  'available': capacity and no_overlap,
                                                  'rules': [{'rule': 'capacity', 'holds': capacity}, {'rule': 'no_overlap', 'holds': no_overlap}]})
                        for pair in restaurant['combinable']:
                            capacity = add_numbers(tables[pair[0]]['capacity'], tables[pair[1]]['capacity'])
                            if capacity >= count and free(pair):
                                options.append({'table_ids': list(pair), 'capacity': capacity})
                        slot = {'starts_at_local': local.isoformat(timespec='minutes'), 'starts_at': timestamp(start, zone),
                                'available_table_ids': available, 'available_options': options}
                        if 'explain' in query:
                            slot['explain'] = explanations
                        slots.append(slot)
                except APIError as error:
                    if error.code != 'invalid_local_time':
                        raise
                remaining = int((close - local).total_seconds() // 60)
                if restaurant['slot_minutes'] >= remaining:
                    break
                local += timedelta(minutes=int(restaurant['slot_minutes']))
        return {'restaurant_id': original['id'], 'date': query['date'], 'timezone': original['timezone'], 'slots': slots}

    def dispatch(self, method, path, query, body, headers):
        if method == 'GET' and path == '/health':
            return 200, {'status': 'ok'}
        if method == 'POST' and path == '/_test/reset':
            replacement = fixture_state(body)
            self.state = replacement
            return 204, None
        if method == 'GET' and path == '/_test/export':
            return 200, {'track': 'tablekeeper', 'format_version': 1,
                         'state': {'encoding': 'tablekeeper-json-v1', 'payload': dumps(self.state)}}
        if method == 'POST' and path == '/_test/import':
            replacement = imported_state(body)
            self.state = replacement
            return 204, None
        if method == 'POST' and path in ('/auth/signup', '/auth/login'):
            address, password = email(field(body, 'email', str)), field(body, 'password', str)
            found = next((user for user in self.state['users'].values() if user['email'] == address), None)
            if path == '/auth/signup':
                name = field(body, 'display_name', str)
                if len(password) < 8:
                    fail()
                if found is not None:
                    fail('email_taken', 409)
                uid = new_id('u_')
                found = {'id': uid, 'email': address, 'display_name': name, 'password_hash': hash_password(password)}
                self.state['users'][uid] = found
            elif found is None or not check_password(password, found['password_hash']):
                fail('unauthenticated', 401)
            token = secrets.token_urlsafe(32)
            self.state['tokens'][token] = found['id']
            return (201 if path == '/auth/signup' else 200), {'user_id': found['id'], 'display_name': found['display_name'], 'token': token}
        if method == 'GET' and path == '/restaurants':
            return 200, {'restaurants': [{key: restaurant[key] for key in ('id', 'name', 'timezone')} for restaurant in self.state['restaurants'].values()]}
        policy_path = re.fullmatch('/restaurants/([^/]+)/policies', path)
        if method == 'GET' and policy_path:
            restaurant = self.restaurant(policy_path[1])
            return 200, {'policies': self.state['policies'][restaurant['id']]}
        restaurant_path = re.fullmatch('/restaurants/([^/]+)', path)
        if method == 'GET' and restaurant_path:
            return 200, self.restaurant(restaurant_path[1])
        if method == 'GET' and path == '/availability':
            return 200, self.availability(query)
        history_path = re.fullmatch('/reservations/([^/]+)/(history|decision)', path)
        if method == 'GET' and history_path:
            reservation = self.owned(history_path[1], self.private_reader(headers))
            if history_path[2] == 'decision':
                return 200, {key: reservation[key] for key in ('reference', 'revision', 'accepted_terms')}
            return 200, {'reference': reservation['reference'], **self.state['histories'][reservation['reference']]}
        series_path = re.fullmatch('/series/([^/]+)', path)
        if method == 'GET' and series_path:
            uid = self.private_reader(headers)
            agreement = self.state['series'].get(series_path[1])
            if agreement is None or agreement['user_id'] != uid:
                fail('not_found', 404)
            return 200, self.series_response(agreement)
        uid = self.user(headers)
        if method == 'POST' and (path in ('/reservations', '/reservation-moves', '/series') or policy_path):
            scope, previous = self.receipt(uid, path, body, headers)
            if previous:
                return 200, previous['response']
            if policy_path:
                restaurant = self.restaurant(policy_path[1])
                if uid not in restaurant['manager_user_ids']:
                    fail('forbidden', 403)
                policy = complete_policy(restaurant, body)
                policy['policy_version'] = len(self.state['policies'][restaurant['id']]) + 1
                response = policy
                self.state['policies'][restaurant['id']].append(policy)
            elif path == '/series':
                response = self.adopt(uid, body)
            elif path == '/reservations':
                restaurant = self.restaurant(identifier(field(body, 'restaurant_id', str)))
                candidate = self.build_reservation(uid, restaurant, body)
                self.ensure_available([candidate])
                response = public(candidate)
                self.publish_created([candidate])
            else:
                moves = body.get('moves')
                if type(moves) is not list or not 1 <= len(moves) <= 8:
                    fail()
                references = []
                for move in moves:
                    if type(move) is not dict or type(move.get('reference')) is not str or not 1 <= len(move['reference']) <= 64 or move['reference'] in references:
                        fail()
                    references.append(move['reference'])
                candidates, rid = [], None
                for move in moves:
                    original = self.owned(move['reference'], uid)
                    if rid is not None and rid != original['restaurant_id']:
                        fail()
                    rid = original['restaurant_id']
                    candidates.append(self.amended(original, move))
                self.ensure_available(candidates, references)
                response = {'reservations': [public(record) for record in candidates]}
                if self.publish_changes(candidates):
                    self.state['restaurant_revisions'][rid] += 1
            self.state['receipts'][scope] = {'body': copy.deepcopy(body), 'response': copy.deepcopy(response)}
            return 201, response
        if method == 'GET' and path == '/reservations':
            records = [record for record in self.state['reservations'].values() if record['user_id'] == uid]
            records.sort(key=lambda record: read_timestamp(record['starts_at']), reverse=True)
            return 200, {'reservations': [public(record) for record in records]}
        reservation_path = re.fullmatch('/reservations/([^/]+)(/cancel)?', path)
        if reservation_path:
            original = self.owned(reservation_path[1], uid)
            if method == 'GET' and not reservation_path[2]:
                return 200, public(original)
            if method == 'POST' and reservation_path[2]:
                if original['status'] == 'cancelled':
                    return 200, public(original)
                self.cutoff(original)
                candidate = {**original, 'status': 'cancelled', 'revision': original['revision'] + 1}
                self.publish_changes([candidate], 'cancelled')
                return 200, public(candidate)
            if method == 'PATCH' and not reservation_path[2]:
                candidate = self.amended(original, body)
                self.ensure_available([candidate], [original['reference']])
                self.publish_changes([candidate])
                return 200, public(candidate)
        fail('not_found', 404)
