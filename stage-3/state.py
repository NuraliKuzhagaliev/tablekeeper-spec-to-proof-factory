"""Complete fixture/snapshot validation before atomic replacement publication."""
import copy
import json
import re
from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from domain import (APIError, UTC, booking, email, fail, field, hash_password, identifier,
                    overlaps, positive_integer, read_timestamp, same_json, stored_booking_fields,
                    timestamp, valid_hash)
from history import baseline_history, changes, native_history, public
from json_value import dumps, is_number, loads
from policies import complete_policy, fixture_terms, opening_hours, rules_config, terms

BASE_KEYS = {'users', 'restaurants', 'reservations', 'tokens', 'receipts'}


def empty_state():
    return {key: {} for key in (*sorted(BASE_KEYS), 'policies', 'histories', 'series', 'restaurant_revisions')}


def restaurant_from_fixture(value):
    if type(value) is not dict:
        fail('malformed_request', 400)
    result = {key: field(value, key, str) for key in ('id', 'name', 'timezone')}
    identifier(result['id'])
    try:
        ZoneInfo(result['timezone'])
    except (ZoneInfoNotFoundError, ValueError):
        fail()
    for key in ('slot_minutes', 'reservation_duration_minutes', 'cancellation_cutoff_minutes'):
        result[key] = positive_integer(field(value, key, int), zero=key == 'cancellation_cutoff_minutes')
    result['opening_hours'] = opening_hours(field(value, 'opening_hours', list))
    result['tables'] = []
    seen = set()
    for item in field(value, 'tables', list):
        if type(item) is not dict:
            fail('malformed_request', 400)
        table = {'id': identifier(field(item, 'id', str)), 'label': field(item, 'label', str),
                 'capacity': positive_integer(field(item, 'capacity', int))}
        if table['id'] in seen:
            fail()
        seen.add(table['id'])
        result['tables'].append(table)
    result['combinable'] = []
    seen_pairs = set()
    for pair in field(value, 'combinable', list) if 'combinable' in value else []:
        if type(pair) is not list:
            fail('malformed_request', 400)
        if len(pair) != 2:
            fail()
        for table_id in pair:
            if type(table_id) is not str:
                fail('malformed_request', 400)
            identifier(table_id)
        key = frozenset(pair)
        if len(key) != 2 or not key.issubset(seen) or key in seen_pairs:
            fail()
        seen_pairs.add(key)
        result['combinable'].append(list(pair))
    result['manager_user_ids'] = []
    for manager in field(value, 'manager_user_ids', list) if 'manager_user_ids' in value else []:
        if type(manager) is not str:
            fail('malformed_request', 400)
        result['manager_user_ids'].append(identifier(manager))
    return result


def fixture_state(body):
    state = empty_state()
    emails, reservation_ids = set(), set()
    for user in field(body, 'users', list):
        if type(user) is not dict:
            fail('malformed_request', 400)
        uid = identifier(field(user, 'id', str))
        address = email(field(user, 'email', str))
        if uid in state['users'] or address in emails:
            fail()
        state['users'][uid] = {'id': uid, 'email': address, 'display_name': field(user, 'display_name', str),
                               'password_hash': hash_password(field(user, 'password', str))}
        emails.add(address)
    for item in field(body, 'restaurants', list):
        restaurant = restaurant_from_fixture(item)
        rid = restaurant['id']
        if rid in state['restaurants']:
            fail()
        state['restaurants'][rid] = restaurant
        state['policies'][rid], state['restaurant_revisions'][rid] = [], 0
    for item in field(body, 'reservations', list):
        if type(item) is not dict:
            fail('malformed_request', 400)
        rid = identifier(field(item, 'restaurant_id', str))
        if rid not in state['restaurants']:
            fail()
        restaurant = state['restaurants'][rid]
        candidate = booking(restaurant, item)
        res_id = identifier(field(item, 'id', str))
        reference = field(item, 'reference', str)
        uid = identifier(field(item, 'user_id', str))
        if (not re.fullmatch('[A-Z0-9]{6,12}', reference) or reference in state['reservations']
                or res_id in reservation_ids or uid not in state['users']):
            fail()
        status = field(item, 'status', str) if 'status' in item else 'confirmed'
        if status not in ('confirmed', 'cancelled'):
            fail()
        candidate.update(reservation_id=res_id, reference=reference, user_id=uid, status=status,
                         created_at=timestamp(datetime.now(UTC)), revision=1, accepted_terms=fixture_terms(restaurant))
        if any(overlaps(candidate, other) for other in state['reservations'].values()):
            fail()
        state['reservations'][reference] = candidate
        state['histories'][reference] = (native_history(restaurant, candidate) if status == 'confirmed'
                                         else baseline_history(candidate, 'fixture_baseline'))
        reservation_ids.add(res_id)
    return state


def accepted_snapshot(state, restaurant, value):
    if type(value) is not dict:
        fail()
    version = positive_integer(value.get('policy_version'), zero=True)
    if version > len(state['policies'][restaurant['id']]):
        fail()
    expected = fixture_terms(restaurant) if version == 0 else terms(state['policies'][restaurant['id']][int(version) - 1])
    if not same_json(expected, value):
        fail()
    return copy.deepcopy(value)


def reservation_record(state, record, owner=None, migrate=False, historical=False):
    if type(record) is not dict or not re.fullmatch('[A-Z0-9]{6,12}', record.get('reference', '')):
        fail()
    restaurant = state['restaurants'][record['restaurant_id']]
    accepted = (accepted_snapshot(state, restaurant, record['accepted_terms']) if 'accepted_terms' in record
                else fixture_terms(restaurant))
    revision = positive_integer(record.get('revision', 1))
    expected = booking(rules_config(restaurant, accepted), stored_booking_fields(record))
    source_shape = expected if 'table_ids' in record else {key: value for key, value in expected.items() if key != 'table_ids'}
    allowed = set(source_shape) | {'reservation_id', 'reference', 'status', 'created_at'}
    allowed |= {key for key in ('revision', 'accepted_terms') if key in record}
    if owner is not None:
        allowed.add('user_id')
        if record['user_id'] != owner or owner not in state['users']:
            fail()
    if set(record) != allowed or any(not same_json(record[key], value) for key, value in source_shape.items()):
        fail()
    identifier(record['reservation_id'])
    read_timestamp(record['created_at'])
    if record['status'] not in ('confirmed', 'cancelled') or historical and record['status'] != 'confirmed':
        fail()
    if not migrate and ('accepted_terms' not in record or 'revision' not in record) and not historical:
        fail()
    normalized = copy.deepcopy(record)
    normalized.update(table_ids=list(expected['table_ids']), accepted_terms=accepted, revision=revision)
    return normalized


def validate_history(state, reference, history):
    current = state['reservations'][reference]
    if type(history) is not dict or set(history) != {'entries', 'provenance'} or type(history['entries']) is not list:
        fail()
    origin = history['provenance']
    if type(origin) is not dict:
        fail()
    native = origin.get('kind') == 'native'
    if native:
        if set(origin) != {'kind'} or not history['entries']:
            fail()
        previous = None
    else:
        if origin.get('kind') not in ('legacy_baseline', 'fixture_baseline') or set(origin) != {'kind', 'known_state'}:
            fail()
        previous = reservation_record(state, origin['known_state'])
        if any(previous[key] != current[key] for key in ('reference', 'reservation_id', 'restaurant_id', 'created_at')):
            fail()
    last_at = None
    for index, item in enumerate(history['entries'], 1):
        if type(item) is not dict or set(item) != {'seq', 'at', 'event', 'changes', 'revision', 'accepted_terms'}:
            fail()
        if positive_integer(item['seq']) != index:
            fail()
        at = read_timestamp(item['at'])
        if last_at is not None and at < last_at:
            fail()
        last_at = at
        event = item['event']
        if (event not in ('created', 'changed', 'cancelled') or type(item['changes']) is not list
                or previous is None and event != 'created' or previous is not None and (event == 'created' or previous['status'] == 'cancelled')):
            fail()
        revision = positive_integer(item['revision'])
        if revision != (1 if previous is None else previous['revision'] + 1):
            fail()
        accepted = accepted_snapshot(state, state['restaurants'][current['restaurant_id']], item['accepted_terms'])
        candidate = copy.deepcopy(previous or public(current))
        candidate.update(revision=revision, accepted_terms=accepted, status='cancelled' if event == 'cancelled' else 'confirmed')
        if event == 'cancelled':
            if item['changes'] or not same_json(accepted, previous['accepted_terms']):
                fail()
        else:
            for change in item['changes']:
                if type(change) is not dict or set(change) != {'field', 'from', 'to'}:
                    fail()
                key = change['field']
                if key not in ('table_id', 'table_ids', 'starts_at_local', 'party_size'):
                    fail()
                if key in ('table_id', 'table_ids'):
                    candidate.pop('table_id', None)
                    candidate.pop('table_ids', None)
                candidate[key] = change['to']
            selector = {key: candidate[key] for key in ('table_id', 'table_ids') if key in candidate}
            # Current responses contain both selectors for singles; select just
            # table_ids except when the history event explicitly wrote table_id.
            if len(selector) == 2:
                selector.pop('table_id')
            expected = booking(rules_config(state['restaurants'][current['restaurant_id']], accepted),
                               {**selector, 'starts_at_local': candidate['starts_at_local'], 'party_size': candidate['party_size']})
            candidate.pop('table_id', None)
            candidate.update(expected)
            if not same_json(item['changes'], changes(previous, candidate)) or event == 'changed' and not item['changes']:
                fail()
        previous = candidate
    if previous is None or not same_json(previous, public(current)):
        fail()


def validate_receipts(state):
    for key, receipt in state['receipts'].items():
        scope = json.loads(key)
        if (type(scope) is not list or len(scope) != 4 or type(scope[0]) is not str or scope[0] not in state['users']
                or scope[1] != 'POST' or type(scope[2]) is not str or type(scope[3]) is not str
                or not 1 <= len(scope[3]) <= 255 or type(receipt) is not dict or set(receipt) != {'body', 'response'}
                or type(receipt['body']) is not dict or type(receipt['response']) is not dict):
            fail()
        path, response = scope[2], receipt['response']
        policy_path = re.fullmatch('/restaurants/([^/]+)/policies', path)
        if policy_path:
            restaurant = state['restaurants'][policy_path[1]]
            version = positive_integer(response['policy_version'])
            if version > len(state['policies'][restaurant['id']]):
                fail()
            expected = state['policies'][restaurant['id']][int(version) - 1]
            if not same_json(response, expected) or not same_json(complete_policy(restaurant, receipt['body']), {k: v for k, v in expected.items() if k != 'policy_version'}):
                fail()
            continue
        if path == '/series':
            agreement = state['series'][response['series_id']]
            if (agreement['user_id'] != scope[0] or set(response) != {'series_id', 'revision', 'interval_weeks', 'occurrences'}
                    or response['revision'] != 1 or response['interval_weeks'] != agreement['interval_weeks']
                    or type(response['occurrences']) is not list or len(response['occurrences']) != len(agreement['occurrences'])):
                fail()
            originals = []
            for index, occurrence in enumerate(response['occurrences']):
                if (set(occurrence) != {'index', 'reference', 'exception', 'reservation'} or occurrence['index'] != index
                        or occurrence['exception'] is not False or occurrence['reference'] != agreement['occurrences'][index]['reference']
                        or occurrence['reservation']['reference'] != occurrence['reference']):
                    fail()
                originals.append(occurrence['reservation'])
            if (receipt['body'].get('anchor_reference') != originals[0]['reference']
                    or receipt['body'].get('count') != len(originals) or receipt['body'].get('interval_weeks') != agreement['interval_weeks']):
                fail()
        elif path == '/reservations':
            originals = [response]
        elif path == '/reservation-moves':
            if set(response) != {'reservations'} or type(response['reservations']) is not list or not 1 <= len(response['reservations']) <= 8:
                fail()
            originals = response['reservations']
        else:
            fail()
        for original in originals:
            normalized = reservation_record(state, original, historical=True)
            current = state['reservations'][normalized['reference']]
            if (current['user_id'] != scope[0] or any(normalized[name] != current[name] for name in ('reservation_id', 'restaurant_id', 'created_at'))
                    or normalized['revision'] > current['revision']):
                fail()


def imported_state(body):
    try:
        if body.get('track') != 'tablekeeper' or not is_number(body.get('format_version')) or body['format_version'] != 1:
            fail()
        source = body.get('state')
        if type(source) is dict and set(source) == {'encoding', 'payload'}:
            if source['encoding'] != 'tablekeeper-json-v1' or type(source['payload']) is not str:
                fail()
            source = loads(source['payload'])
        if type(source) is not dict or set(source) not in (BASE_KEYS, set(empty_state())) or any(type(value) is not dict for value in source.values()):
            fail()
        legacy = set(source) == BASE_KEYS
        state = copy.deepcopy(source)
        if legacy:
            state.update(policies={}, histories={}, series={}, restaurant_revisions={})
        emails, reservation_ids = set(), set()
        for uid, user in state['users'].items():
            identifier(uid)
            if (type(user) is not dict or set(user) != {'id', 'email', 'display_name', 'password_hash'}
                    or user.get('id') != uid or not valid_hash(user.get('password_hash'))
                    or set(user['password_hash']) != {'algorithm', 'salt', 'digest'}):
                fail()
            address = email(field(user, 'email', str))
            field(user, 'display_name', str)
            if address in emails:
                fail()
            emails.add(address)
        for rid, restaurant in state['restaurants'].items():
            normalized = restaurant_from_fixture(restaurant)
            shape = {key: value for key, value in normalized.items() if key not in ('combinable', 'manager_user_ids') or key in restaurant}
            if not same_json(shape, restaurant) or normalized['id'] != rid:
                fail()
            state['restaurants'][rid] = normalized
            if legacy:
                state['policies'][rid], state['restaurant_revisions'][rid] = [], 0
        if set(state['policies']) != set(state['restaurants']) or set(state['restaurant_revisions']) != set(state['restaurants']):
            fail()
        for rid, policies in state['policies'].items():
            if type(policies) is not list:
                fail()
            positive_integer(state['restaurant_revisions'][rid], zero=True)
            for index, policy in enumerate(policies, 1):
                if not same_json(policy, {**complete_policy(state['restaurants'][rid], policy), 'policy_version': index}):
                    fail()
        for reference, record in list(state['reservations'].items()):
            normalized = reservation_record(state, record, owner=record['user_id'], migrate=legacy)
            if normalized['reference'] != reference or normalized['reservation_id'] in reservation_ids:
                fail()
            reservation_ids.add(normalized['reservation_id'])
            state['reservations'][reference] = normalized
            if legacy:
                state['histories'][reference] = baseline_history(normalized)
        records = list(state['reservations'].values())
        if any(overlaps(a, b) for index, a in enumerate(records) for b in records[index + 1:]):
            fail()
        if set(state['histories']) != set(state['reservations']):
            fail()
        for reference, history in state['histories'].items():
            validate_history(state, reference, history)
        adopted = set()
        for sid, agreement in state['series'].items():
            identifier(sid)
            if (type(agreement) is not dict or set(agreement) != {'series_id', 'user_id', 'restaurant_id', 'revision', 'interval_weeks', 'occurrences'}
                    or agreement['series_id'] != sid or agreement['user_id'] not in state['users'] or agreement['restaurant_id'] not in state['restaurants']):
                fail()
            positive_integer(agreement['revision'])
            interval = positive_integer(agreement['interval_weeks'])
            if interval > 4 or type(agreement['occurrences']) is not list or not 2 <= len(agreement['occurrences']) <= 12:
                fail()
            for index, occurrence in enumerate(agreement['occurrences']):
                if (type(occurrence) is not dict or set(occurrence) != {'index', 'reference', 'exception'}
                        or type(occurrence['exception']) is not bool or positive_integer(occurrence['index'], zero=True) != index
                        or occurrence['reference'] in adopted):
                    fail()
                record = state['reservations'][occurrence['reference']]
                if record['user_id'] != agreement['user_id'] or record['restaurant_id'] != agreement['restaurant_id']:
                    fail()
                adopted.add(occurrence['reference'])
        for token, uid in state['tokens'].items():
            if type(token) is not str or not token or uid not in state['users']:
                fail()
        validate_receipts(state)
        return state
    except (APIError, ValueError, TypeError, KeyError, IndexError, AttributeError, OverflowError):
        fail()
