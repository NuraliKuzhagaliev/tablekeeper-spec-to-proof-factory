import json
import threading
import unittest
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

import server
from service import Service
from test_service import fixture


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
        data = raw if raw is not None else None if body is None else json.dumps(body).encode()
        request = urllib.request.Request(self.base + path, data=data, method=method, headers={'Content-Type': 'application/json', **(headers or {})})
        try:
            response = urllib.request.urlopen(request, timeout=5)
        except urllib.error.HTTPError as exc:
            response = exc
        with response:
            payload = response.read()
            return response.status, json.loads(payload) if payload else None, response.headers

    def test_errors_are_json_and_wrong_body_types_are_distinct(self):
        self.assertEqual(self.call('/health')[0], 200)
        for raw in [b'{', b'[]', b'null', b'{"email":NaN}', b'{"email":1e999}']:
            status, body, headers = self.call('/auth/signup', raw=raw)
            self.assertEqual((status, body['error']['code']), (400, 'malformed_request'))
            self.assertEqual(headers['Content-Type'], 'application/json; charset=utf-8')
        status, body, _ = self.call('/auth/signup', body={'email': 3, 'password': 'password123', 'display_name': 'Ada'})
        self.assertEqual((status, body['error']['code']), (400, 'malformed_request'))
        status, body, _ = self.call('/auth/signup', body={'email': 'bad', 'password': 'password123', 'display_name': 'Ada'})
        self.assertEqual((status, body['error']['code']), (422, 'validation_failed'))

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
