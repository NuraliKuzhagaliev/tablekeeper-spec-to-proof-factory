import copy
import json
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta

from domain import APIError, UTC, booking, overlaps, read_timestamp
from service import Service


def fixture(zone='Europe/Berlin', date='2032-06-03'):
    weekday = ('mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun')[datetime.fromisoformat(date).weekday()]
    return {'users': [{'id': 'alice', 'email': 'alice@example.com', 'password': 'password123', 'display_name': 'Alice'},
                      {'id': 'bob', 'email': 'bob@example.com', 'password': 'password456', 'display_name': 'Bob'}],
            'restaurants': [{'id': 'r', 'name': 'Restaurant', 'timezone': zone, 'slot_minutes': 30,
                             'reservation_duration_minutes': 90, 'cancellation_cutoff_minutes': 120,
                             'opening_hours': [{'weekday': weekday, 'opens': '00:00', 'closes': '23:30'}],
                             'tables': [{'id': 't1', 'label': '1', 'capacity': 4}, {'id': 't2', 'label': '2', 'capacity': 6}]}],
            'reservations': []}


class ServiceTests(unittest.TestCase):
    def setUp(self):
        self.service = Service()
        self.call('POST', '/_test/reset', fixture())
        self.token = self.call('POST', '/auth/login', {'email': 'alice@example.com', 'password': 'password123'})[1]['token']
        self.other = self.call('POST', '/auth/login', {'email': 'bob@example.com', 'password': 'password456'})[1]['token']

    def call(self, method, path, body=None, key=None, token=None, query=None):
        headers = {}
        if token is not False:
            headers['Authorization'] = 'Bearer ' + (token or getattr(self, 'token', ''))
        if key is not None:
            headers['Idempotency-Key'] = key
        return self.service.request(method, path, query or {}, body or {}, headers)

    def request_body(self, table='t1', start='2032-06-03T18:00', count=4):
        return {'restaurant_id': 'r', 'table_id': table, 'starts_at_local': start, 'party_size': count}

    def assert_error(self, code, operation, status=None):
        with self.assertRaises(APIError) as result:
            operation()
        self.assertEqual(result.exception.code, code)
        if status:
            self.assertEqual(result.exception.status, status)

    def test_public_browsing_and_owner_privacy(self):
        self.assertEqual(self.call('GET', '/restaurants', token=False)[0], 200)
        self.assertEqual(self.call('GET', '/restaurants/r', token=False)[0], 200)
        result = self.call('POST', '/reservations', self.request_body(), 'one')[1]
        self.assert_error('not_found', lambda: self.call('GET', '/reservations/' + result['reference'], token=self.other), 404)
        self.assert_error('unauthenticated', lambda: self.call('GET', '/reservations', token=False), 401)

    def test_table_identity_is_scoped_to_restaurant_and_seeded_password_is_preserved(self):
        data = fixture()
        second = copy.deepcopy(data['restaurants'][0])
        second['id'] = 'other-restaurant'
        second['timezone'] = 'America/New_York'
        data['restaurants'].append(second)
        data['users'][0]['password'] = 'seed'
        self.call('POST', '/_test/reset', data)
        self.token = self.call('POST', '/auth/login', {'email': 'alice@example.com', 'password': 'seed'})[1]['token']
        first_body = self.request_body()
        other_body = {**first_body, 'restaurant_id': 'other-restaurant'}
        first = self.call('POST', '/reservations', first_body, 'first')[1]
        other = self.call('POST', '/reservations', other_body, 'other')[1]
        self.assertEqual(first['table_id'], other['table_id'])
        snapshot = self.call('GET', '/_test/export')[1]
        self.call('POST', '/_test/import', snapshot)
        self.assertEqual(self.call('POST', '/reservations', other_body, 'other'), (200, other))
        self.assert_error('validation_failed', lambda: self.call('POST', '/reservation-moves', {'moves': [{'reference': first['reference']}, {'reference': other['reference']}]}, 'cross-restaurant'))

    def test_parallel_identical_requests_and_half_open_intervals(self):
        body = self.request_body()
        barrier = threading.Barrier(50)
        def write(_):
            barrier.wait()
            return self.call('POST', '/reservations', body, 'same')
        with ThreadPoolExecutor(max_workers=50) as workers:
            results = list(workers.map(write, range(50)))
        self.assertEqual(sum(status == 201 for status, _ in results), 1)
        self.assertTrue(all(body == results[0][1] for _, body in results))
        self.assertEqual(len(self.call('GET', '/reservations')[1]['reservations']), 1)
        self.assert_error('table_unavailable', lambda: self.call('POST', '/reservations', self.request_body(start='2032-06-03T19:00'), 'overlap'))
        self.assertEqual(self.call('POST', '/reservations', self.request_body(start='2032-06-03T19:30'), 'adjacent')[0], 201)

    def test_concurrent_different_keys_cannot_double_book(self):
        with ThreadPoolExecutor(max_workers=50) as workers:
            def write(index):
                try:
                    return self.call('POST', '/reservations', self.request_body(), str(index))[0]
                except APIError as exc:
                    return exc.code
            outcomes = list(workers.map(write, range(50)))
        self.assertEqual(outcomes.count(201), 1)
        self.assertEqual(outcomes.count('table_unavailable'), 49)
        self.assertEqual(len(self.service.state['receipts']), 1)

    def test_receipts_preserve_original_response_and_failed_keys(self):
        body = self.request_body()
        result = self.call('POST', '/reservations', body, 'same')[1]
        self.call('PATCH', '/reservations/' + result['reference'], {'party_size': 2})
        self.call('POST', '/reservations/' + result['reference'] + '/cancel')
        self.assertEqual(self.call('POST', '/reservations', dict(reversed(list(body.items()))), 'same'), (200, result))
        self.assert_error('idempotency_key_reuse', lambda: self.call('POST', '/reservations', {'party_size': False}, 'same'))
        self.assert_error('validation_failed', lambda: self.call('POST', '/reservations', {'party_size': False}, 'unused'))
        self.assertEqual(self.call('POST', '/reservations', body, 'unused')[0], 201)
        self.assert_error('table_unavailable', lambda: self.call('POST', '/reservations', body, 'unused', token=self.other))

    def test_swap_atomicity_and_path_scoped_receipts(self):
        one = self.call('POST', '/reservations', self.request_body(), 'shared')[1]
        two = self.call('POST', '/reservations', self.request_body(table='t2'), 'two')[1]
        batch = {'moves': [{'reference': one['reference'], 'table_id': 't2'}, {'reference': two['reference'], 'table_id': 't1'}]}
        status, original = self.call('POST', '/reservation-moves', batch, 'shared')
        self.assertEqual(status, 201)
        self.assertEqual([r['table_id'] for r in original['reservations']], ['t2', 't1'])
        before = self.call('GET', '/_test/export')[1]
        bad = {'moves': [{'reference': one['reference'], 'party_size': 1}, {'reference': two['reference'], 'party_size': 99}]}
        self.assert_error('party_exceeds_capacity', lambda: self.call('POST', '/reservation-moves', bad, 'bad'))
        self.assertEqual(self.call('GET', '/_test/export')[1], before)
        self.call('PATCH', '/reservations/' + one['reference'], {'party_size': 1})
        self.assertEqual(self.call('POST', '/reservation-moves', batch, 'shared'), (200, original))
        no_op = {'moves': [{'reference': one['reference']}]}
        current = self.call('GET', '/reservations/' + one['reference'])[1]
        self.assertEqual(self.call('POST', '/reservation-moves', no_op, 'no-op')[1]['reservations'], [current])

    def test_batch_nonoccupancy_errors_precede_conflicts(self):
        one = self.call('POST', '/reservations', self.request_body(), 'one')[1]
        two = self.call('POST', '/reservations', self.request_body(table='t2'), 'two')[1]
        bad = {'moves': [{'reference': one['reference'], 'table_id': 't2'}, {'reference': two['reference'], 'party_size': True}]}
        self.assert_error('validation_failed', lambda: self.call('POST', '/reservation-moves', bad, 'bad'), 422)
        before = self.call('GET', '/_test/export')[1]
        collide = {'moves': [{'reference': one['reference'], 'table_id': 't2'}, {'reference': two['reference']}]}
        self.assert_error('table_unavailable', lambda: self.call('POST', '/reservation-moves', collide, 'collision'))
        self.assertEqual(self.call('GET', '/_test/export')[1], before)

    def test_cutoff_precedes_changes_and_cancel_is_idempotent(self):
        data = fixture(date='2000-06-01')
        self.call('POST', '/_test/reset', data)
        self.token = self.call('POST', '/auth/login', {'email': 'alice@example.com', 'password': 'password123'})[1]['token']
        result = self.call('POST', '/reservations', self.request_body(start='2000-06-01T18:00'), 'past')[1]
        self.assert_error('cutoff_passed', lambda: self.call('PATCH', '/reservations/' + result['reference'], {'party_size': 99}))
        self.assert_error('cutoff_passed', lambda: self.call('POST', '/reservation-moves', {'moves': [{'reference': result['reference'], 'party_size': False}]}, 'past-move'))
        self.assert_error('cutoff_passed', lambda: self.call('POST', '/reservations/' + result['reference'] + '/cancel'))

    def test_snapshot_preserves_tokens_passwords_ids_and_receipts(self):
        body = self.request_body()
        create = self.call('POST', '/reservations', body, 'create')[1]
        batch = {'moves': [{'reference': create['reference'], 'party_size': 2}]}
        moved = self.call('POST', '/reservation-moves', batch, 'batch')[1]
        snapshot = self.call('GET', '/_test/export')[1]
        self.call('POST', '/reservations/' + create['reference'] + '/cancel')
        destination = Service()
        self.assertEqual(destination.request('POST', '/_test/import', {}, json.loads(json.dumps(snapshot)), {}), (204, None))
        self.assertEqual(destination.request('GET', '/_test/export', {}, {}, {})[1], snapshot)
        headers = {'Authorization': 'Bearer ' + self.token, 'Idempotency-Key': 'create'}
        self.assertEqual(destination.request('POST', '/reservations', {}, body, headers), (200, create))
        headers['Idempotency-Key'] = 'batch'
        self.assertEqual(destination.request('POST', '/reservation-moves', {}, batch, headers), (200, moved))
        self.assertEqual(destination.request('POST', '/auth/login', {}, {'email': 'alice@example.com', 'password': 'password123'}, {})[0], 200)
        destination.request('POST', '/_test/import', {}, snapshot, {})
        self.assertEqual(destination.request('GET', '/_test/export', {}, {}, {})[1], snapshot)
        invalid = copy.deepcopy(snapshot)
        invalid['state']['reservations'][create['reference']]['party_size'] = 99
        self.assert_error('validation_failed', lambda: destination.request('POST', '/_test/import', {}, invalid, {}))
        self.assertEqual(destination.request('GET', '/_test/export', {}, {}, {})[1], snapshot)

    def test_spring_and_fall_absolute_durations(self):
        cases = [('Europe/Berlin', '2026-03-29', '2026-10-25', '02:30', '02:30', '03:00', '+02:00', '+01:00'),
                 ('America/New_York', '2026-03-08', '2026-11-01', '02:30', '01:30', '02:00', '-04:00', '-05:00')]
        for zone, spring, fall, gap, repeated, end_clock, initial_offset, end_offset in cases:
            with self.subTest(zone=zone):
                self.call('POST', '/_test/reset', fixture(zone, spring))
                self.token = self.call('POST', '/auth/login', {'email': 'alice@example.com', 'password': 'password123'})[1]['token']
                body = self.request_body(start=spring + 'T' + gap)
                self.assert_error('invalid_local_time', lambda: self.call('POST', '/reservations', body, 'gap'))
                slots = self.call('GET', '/availability', token=False, query={'restaurant_id': 'r', 'date': spring, 'party_size': '4'})[1]['slots']
                self.assertTrue(all(not s['starts_at_local'].startswith(spring + 'T02:') for s in slots))
                self.call('POST', '/_test/reset', fixture(zone, fall))
                self.token = self.call('POST', '/auth/login', {'email': 'alice@example.com', 'password': 'password123'})[1]['token']
                result = self.call('POST', '/reservations', self.request_body(start=fall + 'T' + repeated), 'fall')[1]
                self.assertTrue(result['starts_at'].endswith(initial_offset))
                self.assertEqual(result['ends_at'], fall + 'T' + end_clock + ':00' + end_offset)
                self.assertEqual((read_timestamp(result['ends_at']) - read_timestamp(result['starts_at'])).total_seconds(), 5400)

    def test_explicit_validation_and_json_value_equality(self):
        for value in [True, False, '4', 0, -1, 1.5, None]:
            self.assert_error('validation_failed', lambda: self.call('POST', '/reservations', self.request_body(count=value), 'bad-' + repr(value)), 422)
        self.assert_error('malformed_request', lambda: self.call('POST', '/reservations', self.request_body(table=1), 'wrong-type'), 400)
        self.assert_error('validation_failed', lambda: self.call('POST', '/reservations', self.request_body(start='2032-06-03T18:00Z'), 'offset'), 422)
        for value in ['4.0', '+4', '1e9', '0', '-1', '']:
            self.assert_error('validation_failed', lambda: self.call('GET', '/availability', query={'restaurant_id': 'r', 'date': '2032-06-03', 'party_size': value}))
        body = self.request_body()
        body['ignored'] = {'value': 1}
        result = self.call('POST', '/reservations', body, 'json')[1]
        equal = copy.deepcopy(body)
        equal['ignored']['value'] = 1.0
        self.assertEqual(self.call('POST', '/reservations', equal, 'json'), (200, result))
        unequal = copy.deepcopy(body)
        unequal['ignored']['value'] = True
        self.assert_error('idempotency_key_reuse', lambda: self.call('POST', '/reservations', unequal, 'json'))


if __name__ == '__main__':
    unittest.main()
