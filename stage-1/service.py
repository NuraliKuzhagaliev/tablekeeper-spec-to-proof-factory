"""In-memory transactional service. All observable state uses one lock boundary."""
import copy
import json
import re
import secrets
import threading
import uuid
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from domain import (APIError, UTC, WEEKDAYS, booking, bounds, check_password, email,
                    fail, field, hash_password, identifier, local_date, overlaps,
                    party, positive_integer, read_timestamp, resolve, same_json,
                    timestamp, valid_hash)


def empty_state():
    return {'users': {}, 'restaurants': {}, 'reservations': {}, 'tokens': {}, 'receipts': {}}


def new_id(prefix):
    return prefix + uuid.uuid4().hex


def public(reservation):
    return {k: v for k, v in reservation.items() if k != 'user_id'}


def restaurant_from_fixture(value):
    if type(value) is not dict:
        fail('malformed_request', 400)
    result = {k: field(value, k, str) for k in ('id', 'name', 'timezone')}
    identifier(result['id'])
    try:
        ZoneInfo(result['timezone'])
    except (ZoneInfoNotFoundError, ValueError):
        fail()
    for key in ('slot_minutes', 'reservation_duration_minutes', 'cancellation_cutoff_minutes'):
        result[key] = positive_integer(field(value, key, int), zero=key == 'cancellation_cutoff_minutes')
    result['opening_hours'], result['tables'] = [], []
    seen = set()
    for entry in field(value, 'opening_hours', list):
        if type(entry) is not dict:
            fail('malformed_request', 400)
        hours = {k: field(entry, k, str) for k in ('weekday', 'opens', 'closes')}
        if hours['weekday'] not in WEEKDAYS or hours['weekday'] in seen:
            fail()
        seen.add(hours['weekday'])
        if any(not re.fullmatch(r'(?:[01][0-9]|2[0-3]):[0-5][0-9]', hours[k]) for k in ('opens', 'closes')):
            fail()
        if hours['opens'] >= hours['closes']:
            fail()
        result['opening_hours'].append(hours)
    seen = set()
    for entry in field(value, 'tables', list):
        if type(entry) is not dict:
            fail('malformed_request', 400)
        table = {'id': identifier(field(entry, 'id', str)), 'label': field(entry, 'label', str),
                 'capacity': positive_integer(field(entry, 'capacity', int))}
        if table['id'] in seen:
            fail()
        seen.add(table['id'])
        result['tables'].append(table)
    return result


def fixture_state(body):
    state = empty_state()
    emails, reservation_ids = set(), set()
    for entry in field(body, 'users', list):
        if type(entry) is not dict:
            fail('malformed_request', 400)
        user_id = identifier(field(entry, 'id', str))
        address = email(field(entry, 'email', str))
        password = field(entry, 'password', str)
        if user_id in state['users'] or address in emails:
            fail()
        state['users'][user_id] = {'id': user_id, 'email': address,
                                  'display_name': field(entry, 'display_name', str),
                                  'password_hash': hash_password(password)}
        emails.add(address)
    for entry in field(body, 'restaurants', list):
        restaurant = restaurant_from_fixture(entry)
        if restaurant['id'] in state['restaurants']:
            fail()
        state['restaurants'][restaurant['id']] = restaurant
    for entry in field(body, 'reservations', list):
        if type(entry) is not dict:
            fail('malformed_request', 400)
        restaurant_id = identifier(field(entry, 'restaurant_id', str))
        if restaurant_id not in state['restaurants']:
            fail()
        result = booking(state['restaurants'][restaurant_id], entry)
        res_id = identifier(field(entry, 'id', str))
        reference = field(entry, 'reference', str)
        user_id = identifier(field(entry, 'user_id', str))
        if (not re.fullmatch('[A-Z0-9]{6,12}', reference) or reference in state['reservations']
                or res_id in reservation_ids or user_id not in state['users']):
            fail()
        result.update(reservation_id=res_id, reference=reference, user_id=user_id, status='confirmed',
                      created_at=timestamp(datetime.now(UTC)))
        if any(overlaps(result, r) for r in state['reservations'].values()):
            fail()
        state['reservations'][reference] = result
        reservation_ids.add(res_id)
    return state


def imported_state(body):
    """Validate a replacement completely before publishing it to readers."""
    try:
        if body.get('track') != 'tablekeeper' or type(body.get('format_version')) is not int or body['format_version'] != 1:
            fail()
        state = body.get('state')
        if type(state) is not dict or set(state) != set(empty_state()) or any(type(v) is not dict for v in state.values()):
            fail()
        emails, reservation_ids = set(), set()
        for uid, user in state['users'].items():
            identifier(uid)
            if type(user) is not dict or user.get('id') != uid or not valid_hash(user.get('password_hash')):
                fail()
            address = email(field(user, 'email', str))
            field(user, 'display_name', str)
            if address in emails:
                fail()
            emails.add(address)
        for rid, restaurant in state['restaurants'].items():
            normalized = restaurant_from_fixture(restaurant)
            if normalized != restaurant or normalized['id'] != rid:
                fail()
        for reference, reservation in state['reservations'].items():
            if type(reservation) is not dict or not re.fullmatch('[A-Z0-9]{6,12}', reference):
                fail()
            if (reservation.get('reference') != reference or reservation.get('user_id') not in state['users']
                    or reservation.get('restaurant_id') not in state['restaurants']
                    or reservation.get('status') not in ('confirmed', 'cancelled')):
                fail()
            rid = identifier(field(reservation, 'reservation_id', str))
            if rid in reservation_ids:
                fail()
            reservation_ids.add(rid)
            expected = booking(state['restaurants'][reservation['restaurant_id']], reservation)
            if any(reservation.get(k) != v for k, v in expected.items()):
                fail()
            read_timestamp(field(reservation, 'created_at', str))
            if set(reservation) != set(expected) | {'reservation_id', 'reference', 'user_id', 'status', 'created_at'}:
                fail()
        records = list(state['reservations'].values())
        for index, reservation in enumerate(records):
            if any(overlaps(reservation, other) for other in records[index + 1:]):
                fail()
        for token, uid in state['tokens'].items():
            if not token or uid not in state['users']:
                fail()
        for key, receipt in state['receipts'].items():
            scope = json.loads(key)
            if (type(scope) is not list or len(scope) != 4 or scope[0] not in state['users']
                    or scope[1] != 'POST' or scope[2] not in ('/reservations', '/reservation-moves')
                    or type(scope[3]) is not str or not 1 <= len(scope[3]) <= 255
                    or type(receipt) is not dict or set(receipt) != {'body', 'response'}
                    or type(receipt['body']) is not dict or type(receipt['response']) is not dict):
                fail()
            response = receipt['response']
            responses = [response] if scope[2] == '/reservations' else response.get('reservations')
            if type(responses) is not list or not responses or len(responses) > 8:
                fail()
            for original in responses:
                if type(original) is not dict or original.get('reference') not in state['reservations']:
                    fail()
                current = state['reservations'][original['reference']]
                if (original.get('reservation_id') != current['reservation_id'] or current['user_id'] != scope[0]
                        or original.get('status') != 'confirmed' or set(original) != set(public(current))):
                    fail()
                expected = booking(state['restaurants'][original['restaurant_id']], original)
                if any(original[k] != v for k, v in expected.items()):
                    fail()
                read_timestamp(original['created_at'])
        return copy.deepcopy(state)
    except (APIError, ValueError, TypeError, KeyError, OverflowError):
        fail()


class Service:
    def __init__(self):
        self.lock = threading.RLock()
        self.state = empty_state()

    def request(self, method, path, query, body, headers):
        # Validation, collision detection, reservation mutation and receipt commit
        # are one linearizable operation. Failed operations never publish candidates.
        with self.lock:
            return copy.deepcopy(self.dispatch(method, path, query, body, headers))

    def user(self, headers):
        authorization = headers.get('Authorization', '')
        match = re.fullmatch(r'Bearer ([^\s]+)', authorization, flags=re.IGNORECASE)
        if match is None or match[1] not in self.state['tokens']:
            fail('unauthenticated', 401)
        return self.state['tokens'][match[1]]

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
        restaurant = self.state['restaurants'][reservation['restaurant_id']]
        delta = (read_timestamp(reservation['starts_at']) - datetime.now(UTC)).total_seconds()
        if delta <= restaurant['cancellation_cutoff_minutes'] * 60:
            fail('cutoff_passed', 409)

    def amended(self, reservation, changes):
        if reservation['status'] == 'cancelled':
            fail('reservation_cancelled', 409)
        self.cutoff(reservation)
        candidate = dict(reservation)
        for key in ('table_id', 'starts_at_local', 'party_size'):
            if key in changes:
                candidate[key] = changes[key]
        candidate.update(booking(self.state['restaurants'][reservation['restaurant_id']], candidate))
        return candidate

    def ensure_available(self, candidates, excluded=()):
        others = [r for ref, r in self.state['reservations'].items() if ref not in excluded]
        for index, candidate in enumerate(candidates):
            if any(overlaps(candidate, r) for r in others + candidates[:index]):
                fail('table_unavailable', 409)

    def dispatch(self, method, path, query, body, headers):
        if method == 'GET' and path == '/health':
            return 200, {'status': 'ok'}
        if method == 'POST' and path == '/_test/reset':
            replacement = fixture_state(body)
            self.state = replacement
            return 204, None
        if method == 'GET' and path == '/_test/export':
            return 200, {'track': 'tablekeeper', 'format_version': 1, 'state': self.state}
        if method == 'POST' and path == '/_test/import':
            replacement = imported_state(body)
            self.state = replacement
            return 204, None
        if method == 'POST' and path in ('/auth/signup', '/auth/login'):
            address = email(field(body, 'email', str))
            password = field(body, 'password', str)
            found = next((u for u in self.state['users'].values() if u['email'] == address), None)
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
            return 200, {'restaurants': [{k: r[k] for k in ('id', 'name', 'timezone')} for r in self.state['restaurants'].values()]}
        match = re.fullmatch('/restaurants/([^/]+)', path)
        if method == 'GET' and match:
            return 200, self.restaurant(match[1])
        if method == 'GET' and path == '/availability':
            if any(k not in query for k in ('restaurant_id', 'date', 'party_size')):
                fail()
            if not re.fullmatch('[0-9]+', query['party_size']):
                fail()
            try:
                count = party(int(query['party_size']))
            except ValueError:
                fail()
            day = local_date(query['date'])
            restaurant = self.restaurant(query['restaurant_id'])
            slots = []
            hours = bounds(restaurant, day)
            if hours:
                local, close = hours
                zone = restaurant['timezone']
                closing = close.replace(tzinfo=ZoneInfo(zone), fold=0).astimezone(UTC)
                while local < close:
                    try:
                        start = resolve(local, zone)
                        if restaurant['reservation_duration_minutes'] * 60 <= (closing - start).total_seconds():
                            end = start + timedelta(minutes=restaurant['reservation_duration_minutes'])
                            available = []
                            for table in restaurant['tables']:
                                candidate = {'restaurant_id': restaurant['id'], 'table_id': table['id'], 'status': 'confirmed',
                                             'starts_at': timestamp(start, zone), 'ends_at': timestamp(end, zone)}
                                if table['capacity'] >= count and not any(overlaps(candidate, r) for r in self.state['reservations'].values()):
                                    available.append(table['id'])
                            slots.append({'starts_at_local': local.isoformat(timespec='minutes'), 'starts_at': timestamp(start, zone), 'available_table_ids': available})
                    except APIError as exc:
                        if exc.code != 'invalid_local_time':
                            raise
                    local += timedelta(minutes=min(restaurant['slot_minutes'], 1440))
            return 200, {'restaurant_id': restaurant['id'], 'date': query['date'], 'timezone': restaurant['timezone'], 'slots': slots}
        uid = self.user(headers)
        if method == 'POST' and path in ('/reservations', '/reservation-moves'):
            scope, previous = self.receipt(uid, path, body, headers)
            if previous:
                return 200, previous['response']
            if path == '/reservations':
                restaurant = self.restaurant(identifier(field(body, 'restaurant_id', str)))
                candidate = booking(restaurant, body)
                reference = ''.join(secrets.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(10))
                while reference in self.state['reservations']:
                    reference = ''.join(secrets.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(10))
                candidate.update(reservation_id=new_id('res_'), reference=reference, user_id=uid,
                                 status='confirmed', created_at=timestamp(datetime.now(UTC)))
                self.ensure_available([candidate])
                candidates = [candidate]
                response = public(candidate)
            else:
                moves = body.get('moves')
                if type(moves) is not list or not 1 <= len(moves) <= 8:
                    fail()
                references = []
                for move in moves:
                    if type(move) is not dict or type(move.get('reference')) is not str:
                        fail()
                    if move['reference'] in references or not 1 <= len(move['reference']) <= 64:
                        fail()
                    references.append(move['reference'])
                candidates, restaurant_id = [], None
                for move in moves:
                    original = self.owned(move['reference'], uid)
                    if restaurant_id is not None and original['restaurant_id'] != restaurant_id:
                        fail()
                    restaurant_id = original['restaurant_id']
                    candidates.append(self.amended(original, move))
                self.ensure_available(candidates, references)
                response = {'reservations': [public(r) for r in candidates]}
            receipt = {'body': copy.deepcopy(body), 'response': copy.deepcopy(response)}
            for candidate in candidates:
                self.state['reservations'][candidate['reference']] = candidate
            self.state['receipts'][scope] = receipt
            return 201, response
        if method == 'GET' and path == '/reservations':
            own = [r for r in self.state['reservations'].values() if r['user_id'] == uid]
            own.sort(key=lambda r: read_timestamp(r['starts_at']), reverse=True)
            return 200, {'reservations': [public(r) for r in own]}
        match = re.fullmatch('/reservations/([^/]+)(/cancel)?', path)
        if match:
            original = self.owned(match[1], uid)
            if method == 'GET' and not match[2]:
                return 200, public(original)
            if method == 'POST' and match[2]:
                if original['status'] != 'cancelled':
                    self.cutoff(original)
                    original['status'] = 'cancelled'
                return 200, public(original)
            if method == 'PATCH' and not match[2]:
                candidate = self.amended(original, body)
                self.ensure_available([candidate], [original['reference']])
                self.state['reservations'][candidate['reference']] = candidate
                return 200, public(candidate)
        fail('not_found', 404)
