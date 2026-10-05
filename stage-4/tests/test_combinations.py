"""Stage 2 member occupancy, selector and exact Stage 1 upgrade regressions."""
import copy
import subprocess
import sys
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from domain import APIError, overlaps
from json_value import dumps, loads
from service import Service
from test_service import fixture


def paired_fixture():
    data = fixture(zone='UTC')
    restaurant = data['restaurants'][0]
    restaurant['tables'] = [{'id': 'a', 'label': 'Window', 'capacity': 2},
                            {'id': 'b', 'label': 'Garden', 'capacity': 4},
                            {'id': 'c', 'label': 'Corner', 'capacity': 3}]
    restaurant['combinable'] = [['b', 'a'], ['b', 'c']]
    return data


class CombinationTests(unittest.TestCase):
    def setUp(self):
        self.service = Service()
        self.call('POST', '/_test/reset', paired_fixture())
        self.token = self.call('POST', '/auth/login', {'email': 'alice@example.com', 'password': 'password123'})[1]['token']

    def call(self, method, path, body=None, key=None, query=None):
        headers = {'Authorization': 'Bearer ' + getattr(self, 'token', '')}
        if key is not None:
            headers['Idempotency-Key'] = key
        return self.service.request(method, path, query or {}, body or {}, headers)

    def body(self, selection=None, party=2, start='2032-06-03T18:00'):
        return {'restaurant_id': 'r', 'starts_at_local': start, 'party_size': party,
                **(selection if selection is not None else {'table_ids': ['a', 'b']})}

    def error(self, operation, status, code):
        with self.assertRaises(APIError) as error:
            operation()
        self.assertEqual((error.exception.status, error.exception.code), (status, code))

    def availability(self, party=2):
        slots = self.call('GET', '/availability', query={'restaurant_id': 'r', 'date': '2032-06-03', 'party_size': str(party)})[1]['slots']
        return next(slot for slot in slots if slot['starts_at_local'].endswith('T18:00'))

    def test_declared_order_capacity_and_member_occupancy(self):
        self.assertEqual(self.availability()['available_options'], [
            {'table_ids': ['a'], 'capacity': 2}, {'table_ids': ['b'], 'capacity': 4},
            {'table_ids': ['c'], 'capacity': 3}, {'table_ids': ['b', 'a'], 'capacity': 6},
            {'table_ids': ['b', 'c'], 'capacity': 7}])
        self.assertEqual(self.availability(6)['available_table_ids'], [])
        result = self.call('POST', '/reservations', self.body(party=6), 'pair')[1]
        self.assertEqual(result['table_ids'], ['b', 'a'])
        self.assertNotIn('table_id', result)
        self.assertEqual(self.availability()['available_options'], [{'table_ids': ['c'], 'capacity': 3}])
        for selector in ({'table_id': 'a'}, {'table_ids': ['c', 'b']}):
            self.error(lambda: self.call('POST', '/reservations', self.body(selector), 'blocked-' + dumps(selector)), 409, 'table_unavailable')
        self.call('POST', '/reservations/' + result['reference'] + '/cancel')
        self.assertEqual(len(self.availability()['available_options']), 5)
        self.assertEqual(self.call('POST', '/reservations', self.body(party=6), 'pair'), (200, result))

    def test_selector_rules_and_full_body_retry_identity(self):
        cases = [({'table_id': 'a', 'table_ids': ['a']}, 422, 'validation_failed'),
                 ({'table_ids': []}, 422, 'validation_failed'),
                 ({'table_ids': ['a', 'a']}, 422, 'validation_failed'),
                 ({'table_ids': ['a', 'b', 'c']}, 422, 'combination_not_allowed'),
                 ({'table_ids': ['a', 'c']}, 422, 'combination_not_allowed'),
                 ({'table_ids': ['a', 'unknown']}, 404, 'not_found'),
                 ({'table_ids': 'a'}, 400, 'malformed_request'),
                 ({'table_ids': ['a', 1]}, 400, 'malformed_request')]
        for selector, status, code in cases:
            with self.subTest(selector=selector):
                self.error(lambda: self.call('POST', '/reservations', self.body(selector), 'reusable'), status, code)
        self.error(lambda: self.call('POST', '/reservations', self.body(party=7), 'reusable'), 422, 'party_exceeds_capacity')
        original = self.call('POST', '/reservations', self.body(), 'reusable')[1]
        self.error(lambda: self.call('POST', '/reservations', self.body({'table_ids': ['b', 'a']}), 'reusable'), 409, 'idempotency_key_reuse')
        self.error(lambda: self.call('POST', '/reservations', {'table_ids': None}, 'reusable'), 409, 'idempotency_key_reuse')
        self.assertEqual(self.call('POST', '/reservations', self.body(), 'reusable'), (200, original))

    def test_patch_explicit_selector_replaces_stored_selection(self):
        original = self.call('POST', '/reservations', self.body({'table_id': 'a'}), 'single')[1]
        route = '/reservations/' + original['reference']
        pair = self.call('PATCH', route, {'table_ids': ['a', 'b'], 'party_size': 6})[1]
        self.assertEqual(pair['table_ids'], ['b', 'a'])
        self.assertNotIn('table_id', pair)
        self.assertEqual(pair['reservation_id'], original['reservation_id'])
        before = self.call('GET', '/_test/export')[1]
        self.error(lambda: self.call('PATCH', route, {'table_id': 'c'}), 422, 'party_exceeds_capacity')
        self.assertEqual(self.call('GET', '/_test/export')[1], before)
        single = self.call('PATCH', route, {'table_id': 'c', 'party_size': 3})[1]
        self.assertEqual(single['table_ids'], ['c'])
        self.assertEqual(single['table_id'], 'c')
        self.assertEqual(self.call('PATCH', route, {'party_size': 3})[1], single)
        self.assertEqual(self.call('PATCH', route, {'table_ids': ['c']})[1], single)
        self.assertEqual(self.call('POST', '/reservations', self.body({'table_ids': ['a']}), 'released')[0], 201)

    def test_atomic_pair_single_swap_noop_and_failure_receipt(self):
        pair = self.call('POST', '/reservations', self.body(), 'pair')[1]
        single = self.call('POST', '/reservations', self.body({'table_id': 'c'}), 'single')[1]
        swap = {'moves': [{'reference': pair['reference'], 'table_id': 'c'},
                          {'reference': single['reference'], 'table_ids': ['a', 'b']}]}
        response = self.call('POST', '/reservation-moves', swap, 'swap')[1]
        self.assertEqual([record['table_ids'] for record in response['reservations']], [['c'], ['b', 'a']])
        before = self.call('GET', '/_test/export')[1]
        collision = {'moves': [{'reference': pair['reference'], 'table_ids': ['b', 'c']},
                               {'reference': single['reference']}]}
        self.error(lambda: self.call('POST', '/reservation-moves', collision, 'failed'), 409, 'table_unavailable')
        self.assertEqual(self.call('GET', '/_test/export')[1], before)
        invalid = copy.deepcopy(collision)
        invalid['moves'][1]['party_size'] = False
        self.error(lambda: self.call('POST', '/reservation-moves', invalid, 'failed'), 422, 'validation_failed')
        noop = {'moves': [{'reference': pair['reference']}, {'reference': single['reference'], 'table_ids': ['a', 'b']}]}
        self.assertEqual(self.call('POST', '/reservation-moves', noop, 'failed')[1], response)
        self.call('POST', '/reservations/' + pair['reference'] + '/cancel')
        self.assertEqual(self.call('POST', '/reservation-moves', swap, 'swap'), (200, response))
        snapshot = self.call('GET', '/_test/export')[1]
        self.call('POST', '/_test/import', snapshot)
        self.assertEqual(self.call('POST', '/reservation-moves', swap, 'swap'), (200, response))

    def test_parallel_pairs_and_member_amendments_are_serializable(self):
        c = self.call('POST', '/reservations', self.body({'table_id': 'c'}), 'c')[1]
        barrier = threading.Barrier(50)
        def execute(index):
            barrier.wait()
            try:
                if index % 2:
                    return self.call('PATCH', '/reservations/' + c['reference'], {'table_id': 'b'})[0]
                return self.call('POST', '/reservations', self.body(), str(index))[0]
            except APIError as error:
                return error.code
        with ThreadPoolExecutor(max_workers=50) as workers:
            outcomes = list(workers.map(execute, range(50)))
        records = self.call('GET', '/reservations')[1]['reservations']
        self.assertTrue(all(not overlaps(a, b) for index, a in enumerate(records) for b in records[index + 1:]))
        if 201 in outcomes:
            self.assertEqual(outcomes.count(201), 1)
            self.assertEqual(outcomes.count('table_unavailable'), 49)
        else:
            self.assertEqual(outcomes.count(200), 25)
            self.assertEqual(outcomes.count('table_unavailable'), 25)

    def test_seed_cancelled_pair_does_not_occupy_members(self):
        data = paired_fixture()
        seeded = {**self.body(party=6), 'id': 'seeded', 'reference': 'SEED01', 'user_id': 'alice', 'status': 'cancelled'}
        data['reservations'] = [seeded, {**seeded, 'id': 'active', 'reference': 'SEED02', 'status': 'confirmed'}]
        self.call('POST', '/_test/reset', data)
        self.token = self.call('POST', '/auth/login', {'email': 'alice@example.com', 'password': 'password123'})[1]['token']
        self.assertEqual(self.call('GET', '/reservations/SEED01')[1]['status'], 'cancelled')
        self.assertEqual(self.call('POST', '/reservations/SEED01/cancel')[1]['status'], 'cancelled')
        self.assertEqual(self.availability()['available_table_ids'], ['c'])
        self.call('POST', '/reservations/SEED02/cancel')
        self.assertEqual(self.availability()['available_table_ids'], ['a', 'b', 'c'])

    def test_invalid_pair_state_controls_leave_destination_unchanged(self):
        self.call('POST', '/reservations', self.body(), 'pair')
        before = self.call('GET', '/_test/export')[1]
        for pairs in ([['a', 'unknown']], [['a', 'a']], [['a', 'b', 'c']], [['a', 'b'], ['b', 'a']]):
            data = paired_fixture()
            data['restaurants'][0]['combinable'] = pairs
            self.error(lambda: self.call('POST', '/_test/reset', data), 422, 'validation_failed')
            self.assertEqual(self.call('GET', '/_test/export')[1], before)
        invalid = copy.deepcopy(before)
        state = loads(invalid['state']['payload'])
        record = next(iter(state['reservations'].values()))
        record['table_ids'] = ['a', 'c']
        invalid['state']['payload'] = dumps(state)
        self.error(lambda: self.call('POST', '/_test/import', invalid), 422, 'validation_failed')
        self.assertEqual(self.call('GET', '/_test/export')[1], before)

    def test_exact_combination_capacity_above_float_range(self):
        data = paired_fixture()
        data['restaurants'][0]['tables'][0]['capacity'] = loads('1e309')
        data['restaurants'][0]['tables'][1]['capacity'] = loads('2e309')
        self.call('POST', '/_test/reset', data)
        self.token = self.call('POST', '/auth/login', {'email': 'alice@example.com', 'password': 'password123'})[1]['token']
        count = loads('3e309')
        options = self.availability('3' + '0' * 309)['available_options']
        self.assertEqual(options, [{'table_ids': ['b', 'a'], 'capacity': count}])
        self.assertEqual(self.call('POST', '/reservations', self.body(party=count), 'huge')[0], 201)
        self.call('POST', '/_test/import', self.call('GET', '/_test/export')[1])

    def test_real_stage1_snapshot_preserves_sessions_and_original_receipts(self):
        # Execute the frozen Stage 1 modules in a separate interpreter so this
        # test cannot accidentally construct a Stage 2-shaped source snapshot.
        source = Path(__file__).resolve().parents[2] / 'stage-1'
        script = '''
from service import Service
from json_value import loads, dumps
import sys
s = Service()
data = loads(sys.stdin.read())
s.request('POST', '/_test/reset', {}, data, {})
token = s.request('POST', '/auth/login', {}, {'email':'alice@example.com','password':'password123'}, {})[1]['token']
headers = {'Authorization':'Bearer '+token,'Idempotency-Key':'lost'}
body = {'restaurant_id':'r','table_id':'t1','starts_at_local':'2032-06-03T18:00','party_size':4,'ignored':loads('1e309')}
created = s.request('POST', '/reservations', {}, body, headers)[1]
move = {'moves':[{'reference':created['reference'],'party_size':2}]}
headers['Idempotency-Key'] = 'move'
moved = s.request('POST', '/reservation-moves', {}, move, headers)[1]
snapshot = s.request('GET', '/_test/export', {}, {}, {})[1]
print(dumps({'snapshot':snapshot,'token':token,'body':body,'created':created,'move':move,'moved':moved}))
'''
        result = subprocess.run([sys.executable, '-B', '-c', script], cwd=source,
                                input=dumps(fixture()), text=True, capture_output=True, check=True)
        migration = loads(result.stdout)
        self.call('POST', '/_test/import', migration['snapshot'])
        self.token = migration['token']
        reference = migration['created']['reference']
        current = self.call('GET', '/reservations/' + reference)[1]
        self.assertEqual(current['table_ids'], ['t1'])
        self.assertEqual(current['party_size'], 2)
        self.assertNotIn('table_ids', migration['created'])
        self.assertEqual(self.call('POST', '/reservations', migration['body'], 'lost'), (200, migration['created']))
        self.assertEqual(self.call('POST', '/reservation-moves', migration['move'], 'move'), (200, migration['moved']))
        self.assertEqual(self.call('POST', '/auth/login', {'email': 'alice@example.com', 'password': 'password123'})[0], 200)
        self.call('POST', '/reservations/' + reference + '/cancel')
        stage2_snapshot = self.call('GET', '/_test/export')[1]
        self.call('POST', '/_test/import', stage2_snapshot)
        self.assertEqual(self.call('POST', '/reservations', migration['body'], 'lost'), (200, migration['created']))
        self.assertEqual(self.call('POST', '/reservation-moves', migration['move'], 'move'), (200, migration['moved']))
        self.assertEqual(self.call('GET', '/reservations/' + reference)[1]['status'], 'cancelled')


if __name__ == '__main__':
    unittest.main()
