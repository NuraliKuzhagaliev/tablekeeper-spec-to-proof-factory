import json
import threading
import tempfile
import unittest
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import patch

import server
from service import Service
from test_service import fixture
from test_combinations import paired_fixture
from json_value import loads, dumps


class HTTPTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.http = server.Server(('127.0.0.1', 0), server.Handler)
        cls.thread = threading.Thread(target=cls.http.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = 'http://127.0.0.1:' + str(cls.http.server_port)

    @classmethod
    def tearDownClass(cls):
        cls.http.shutdown()
        cls.http.server_close()
        cls.thread.join()

    def setUp(self):
        server.service = Service()

    def call(self, path, body=None, raw=None, headers=None, method=None):
        data = raw if raw is not None else None if body is None else dumps(body).encode()
        request = urllib.request.Request(self.base + path, data=data, method=method, headers={'Content-Type': 'application/json', **(headers or {})})
        try:
            response = urllib.request.urlopen(request, timeout=5)
        except urllib.error.HTTPError as exc:
            response = exc
        with response:
            payload = response.read()
            return response.status, loads(payload) if payload else None, response.headers

    def test_errors_are_json_and_wrong_body_types_are_distinct(self):
        self.assertEqual(self.call('/health')[0], 200)
        for raw in [b'{', b'[]', b'null', b'{"email":NaN}', b'{"email":Infinity}', b'{"email":-Infinity}']:
            status, body, headers = self.call('/auth/signup', raw=raw)
            self.assertEqual((status, body['error']['code']), (400, 'malformed_request'))
            self.assertEqual(headers['Content-Type'], 'application/json; charset=utf-8')
        status, body, _ = self.call('/auth/signup', body={'email': 3, 'password': 'password123', 'display_name': 'Ada'})
        self.assertEqual((status, body['error']['code']), (400, 'malformed_request'))
        status, body, _ = self.call('/auth/signup', body={'email': 'bad', 'password': 'password123', 'display_name': 'Ada'})
        self.assertEqual((status, body['error']['code']), (422, 'validation_failed'))

    def test_fixed_browser_routes_serve_local_assets_and_no_arbitrary_files(self):
        with tempfile.TemporaryDirectory() as directory:
            assets = {'index.html': b'<!doctype html><title>Tablekeeper</title>',
                      'app.js': b'const local = true;', 'styles.css': b'body { color: black; }'}
            for filename, content in assets.items():
                (Path(directory) / filename).write_bytes(content)
            with patch.object(server, 'PUBLIC', Path(directory)):
                for route, (filename, content_type) in server.ASSETS.items():
                    with urllib.request.urlopen(self.base + route + '?ignored=1', timeout=5) as response:
                        self.assertEqual(response.status, 200)
                        self.assertEqual(response.headers['Content-Type'], content_type)
                        self.assertEqual(response.read(), assets[filename])
                for path in ('/assets/../service.py', '/assets/%2e%2e/service.py', '/public/index.html'):
                    status, error, _ = self.call(path)
                    self.assertEqual((status, error['error']['code']), (401, 'unauthenticated'))

    def test_fifty_http_retries_commit_once(self):
        self.assertEqual(self.call('/_test/reset', body=fixture())[0], 204)
        token = self.call('/auth/login', body={'email': 'alice@example.com', 'password': 'password123'})[1]['token']
        body = {'restaurant_id': 'r', 'table_id': 't1', 'starts_at_local': '2032-06-03T18:00', 'party_size': 4}
        barrier = threading.Barrier(50)
        def write(_):
            barrier.wait()
            return self.call('/reservations', body=body, headers={'Authorization': 'Bearer ' + token, 'Idempotency-Key': 'http-retries'})
        with ThreadPoolExecutor(max_workers=50) as workers:
            results = list(workers.map(write, range(50)))
        self.assertEqual(sum(status == 201 for status, _, _ in results), 1)
        self.assertEqual(sum(status == 200 for status, _, _ in results), 49)
        self.assertTrue(all(response == results[0][1] for _, response, _ in results))

    def test_pair_http_retries_conflicts_and_portable_snapshot(self):
        self.assertEqual(self.call('/_test/reset', body=paired_fixture())[0], 204)
        token = self.login()
        headers = {'Authorization': 'Bearer ' + token, 'Idempotency-Key': 'pair-retry'}
        body = {'restaurant_id': 'r', 'table_ids': ['a', 'b'], 'starts_at_local': '2032-06-03T18:00', 'party_size': 6}
        barrier = threading.Barrier(50)
        def write(_):
            barrier.wait()
            return self.call('/reservations', body=body, headers=headers)
        with ThreadPoolExecutor(max_workers=50) as workers:
            results = list(workers.map(write, range(50)))
        self.assertEqual([status for status, _, _ in results].count(201), 1)
        self.assertEqual([status for status, _, _ in results].count(200), 49)
        original = results[0][1]
        self.assertEqual(original['table_ids'], ['b', 'a'])
        self.assertNotIn('table_id', original)
        self.assertTrue(all(response == original for _, response, _ in results))
        status, error, _ = self.call('/reservations', body={**body, 'table_ids': ['b', 'a']}, headers=headers)
        self.assertEqual((status, error['error']['code']), (409, 'idempotency_key_reuse'))
        status, error, _ = self.call('/reservations', body={**body, 'table_ids': ['b'], 'party_size': 4},
                                     headers={**headers, 'Idempotency-Key': 'member'})
        self.assertEqual((status, error['error']['code']), (409, 'table_unavailable'))
        snapshot = self.call('/_test/export')[1]
        server.service = Service()
        self.assertEqual(self.call('/_test/import', body=snapshot)[0], 204)
        route = '/reservations/' + original['reference']
        auth = {'Authorization': 'Bearer ' + token}
        self.assertEqual(self.call(route, headers=auth)[1], original)
        self.assertEqual(self.call(route + '/cancel', body={}, headers=auth)[1]['status'], 'cancelled')
        self.assertEqual(self.call('/reservations', body=body, headers=headers)[:2], (200, original))
        self.assertEqual(self.call('/reservations', body={**body, 'table_ids': ['b'], 'party_size': 4},
                                   headers={**headers, 'Idempotency-Key': 'member'})[0], 201)

    def login(self):
        return self.call('/auth/login', body={'email': 'alice@example.com', 'password': 'password123'})[1]['token']

    def test_ignored_numbers_have_no_machine_magnitude_limit(self):
        ordinary = dumps(fixture()).encode()
        for token in ('1e309', '1e-999', '1e9999999999999999999999999', '9' * 5000):
            with self.subTest(number=token[:30]):
                raw = ordinary[:-1] + b',"ignored":' + token.encode() + b'}'
                self.assertEqual(self.call('/_test/reset', raw=raw)[0], 204)
        token = self.login()
        headers = {'Authorization': 'Bearer ' + token, 'Idempotency-Key': 'large-party'}
        raw = b'{"restaurant_id":"r","table_id":"t1","starts_at_local":"2032-06-03T18:00","party_size":1e309}'
        status, body, _ = self.call('/reservations', raw=raw, headers=headers)
        self.assertEqual((status, body['error']['code']), (422, 'party_exceeds_capacity'))

    def test_exact_numeric_receipts_survive_snapshot_and_cancellation(self):
        self.assertEqual(self.call('/_test/reset', body=fixture())[0], 204)
        token = self.login()
        headers = {'Authorization': 'Bearer ' + token, 'Idempotency-Key': 'numbers'}
        base = b'{"restaurant_id":"r","table_id":"t1","starts_at_local":"2032-06-03T18:00","party_size":4'
        raw = base + b',"ignored":[1e309,1e-400,9007199254740993.0,1e9999999999999999999999999]}'
        status, original, _ = self.call('/reservations', raw=raw, headers=headers)
        self.assertEqual(status, 201)
        equivalent = base + b',"ignored":[10e308,10e-401,9007199254740993,10e9999999999999999999999998]}'
        self.assertEqual(self.call('/reservations', raw=equivalent, headers=headers)[:2], (200, original))
        for replacement in (b'[2e309,1e-400,9007199254740993.0,1e9999999999999999999999999]',
                            b'[1e309,0,9007199254740993.0,1e9999999999999999999999999]',
                            b'[1e309,1e-400,9007199254740992.0,1e9999999999999999999999999]'):
            status, body, _ = self.call('/reservations', raw=base + b',"ignored":' + replacement + b'}', headers=headers)
            self.assertEqual((status, body['error']['code']), (409, 'idempotency_key_reuse'))
        batch_raw = ('{"moves":[{"reference":"' + original['reference']
                     + '","party_size":4.0,"ignored":1e309}],"ignored":1e-400}').encode()
        batch_headers = {'Authorization': 'Bearer ' + token, 'Idempotency-Key': 'batch-numbers'}
        batch_status, batch_original, _ = self.call('/reservation-moves', raw=batch_raw, headers=batch_headers)
        self.assertEqual(batch_status, 201)
        self.call('/reservations/' + original['reference'] + '/cancel', body={}, headers={'Authorization': 'Bearer ' + token})
        status, snapshot, _ = self.call('/_test/export')
        self.assertEqual(status, 200)
        receipt = next(iter(loads(snapshot['state']['payload'])['receipts'].values()))
        self.assertEqual([dumps(n) for n in receipt['body']['ignored']],
                         ['1e309', '1e-400', '9007199254740993.0', '1e9999999999999999999999999'])
        server.service = Service()
        # The public snapshot wrapper round-trips through an ordinary JSON
        # parser/writer without exposing unsupported machine numeric values.
        portable = json.loads(json.dumps(snapshot, allow_nan=False))
        self.assertEqual(self.call('/_test/import', body=portable)[0], 204)
        self.assertEqual(self.call('/reservations', raw=equivalent, headers=headers)[:2], (200, original))
        self.assertEqual(self.call('/reservation-moves', raw=batch_raw, headers=batch_headers)[:2], (200, batch_original))
        self.assertEqual(self.call('/reservations/' + original['reference'], headers={'Authorization': 'Bearer ' + token})[1]['status'], 'cancelled')
        self.assertEqual(self.call('/_test/export')[1], snapshot)

    def test_large_capacity_and_integer_numeric_forms_remain_exact(self):
        data = fixture()
        data['restaurants'][0]['tables'][0]['capacity'] = loads('1e309')
        self.assertEqual(self.call('/_test/reset', body=data)[0], 204)
        token = self.login()
        headers = {'Authorization': 'Bearer ' + token, 'Idempotency-Key': 'large-valid'}
        raw = b'{"restaurant_id":"r","table_id":"t1","starts_at_local":"2032-06-03T18:00","party_size":1e309}'
        status, original, _ = self.call('/reservations', raw=raw, headers=headers)
        self.assertEqual(status, 201)
        self.assertEqual(dumps(original['party_size']), '1e309')
        snapshot = self.call('/_test/export')[1]
        server.service = Service()
        self.assertEqual(self.call('/_test/import', body=snapshot)[0], 204)
        self.assertEqual(self.call('/reservations', raw=raw, headers=headers)[:2], (200, original))

    def test_terminal_calendar_day_grid_stops_within_its_bounds(self):
        data = fixture(zone='UTC')
        restaurant = data['restaurants'][0]
        restaurant['opening_hours'] = [{'weekday': day, 'opens': '18:00', 'closes': '23:00'}
                                       for day in ('mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun')]
        for step in (1440, 10 ** 100, 299, 30):
            with self.subTest(step=str(step)[:10]):
                restaurant['slot_minutes'] = step
                self.assertEqual(self.call('/_test/reset', body=data)[0], 204)
                for day in ('0001-01-01', '2026-10-09', '9999-12-31'):
                    status, response, _ = self.call('/availability?restaurant_id=r&date=' + day + '&party_size=2')
                    self.assertEqual(status, 200)
                    expected = 1 if step > 210 else 8
                    self.assertEqual(len(response['slots']), expected)
                    self.assertEqual(response['slots'][0]['starts_at_local'], day + 'T18:00')
        token = self.login()
        status, result, _ = self.call('/reservations', body={'restaurant_id': 'r', 'table_id': 't1',
                                      'starts_at_local': '9999-12-31T18:00', 'party_size': 2},
                                     headers={'Authorization': 'Bearer ' + token, 'Idempotency-Key': 'last-date'})
        self.assertEqual(status, 201)
        self.assertEqual(result['ends_at'], '9999-12-31T19:30:00+00:00')

    def test_terminal_local_date_can_cross_utc_year_boundary(self):
        for zone in ('UTC', 'America/New_York', 'Europe/Berlin', 'Asia/Tokyo'):
            with self.subTest(zone=zone):
                data = fixture(zone=zone, date='9999-12-31')
                data['restaurants'][0]['opening_hours'][0].update(opens='18:00', closes='23:00')
                data['restaurants'][0]['slot_minutes'] = 30
                self.assertEqual(self.call('/_test/reset', body=data)[0], 204)
                status, availability, _ = self.call('/availability?restaurant_id=r&date=9999-12-31&party_size=2')
                self.assertEqual(status, 200)
                self.assertEqual(len(availability['slots']), 8)
                token = self.login()
                headers = {'Authorization': 'Bearer ' + token, 'Idempotency-Key': 'edge'}
                request = {'restaurant_id': 'r', 'table_id': 't1', 'starts_at_local': '9999-12-31T18:00', 'party_size': 2}
                status, result, _ = self.call('/reservations', body=request, headers=headers)
                self.assertEqual(status, 201)
                self.assertTrue(result['ends_at'].startswith('9999-12-31T19:30:00'))
                snapshot = self.call('/_test/export')[1]
                server.service = Service()
                self.assertEqual(self.call('/_test/import', body=snapshot)[0], 204)
                self.assertEqual(self.call('/reservations', body=request, headers=headers)[:2], (200, result))
                request['starts_at_local'] = '9999-12-31T19:30'
                headers['Idempotency-Key'] = 'adjacent'
                self.assertEqual(self.call('/reservations', body=request, headers=headers)[0], 201)
                self.assertEqual(len(self.call('/reservations', headers={'Authorization': 'Bearer ' + token})[1]['reservations']), 2)
