"""Threaded HTTP transport; the service owns all application transactions."""
import json
import math
import os
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, unquote, urlsplit

from domain import APIError, fail
from service import Service

service = Service()


def reject_constant(value):
    raise ValueError('non-JSON numeric constant')


def finite_float(value):
    result = float(value)
    if not math.isfinite(result):
        raise ValueError('non-finite number')
    return result


class Handler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def log_message(self, format, *args):
        # Do not log URLs, request bodies, credentials, session tokens or exports.
        pass

    def handle_request(self):
        try:
            split = urlsplit(self.path)
            path = unquote(split.path)
            body = {}
            if self.command in ('POST', 'PATCH', 'PUT'):
                try:
                    length = int(self.headers.get('Content-Length', '0'))
                    if length < 0:
                        raise ValueError()
                    if self.headers.get('Transfer-Encoding'):
                        raise ValueError()
                    raw = self.rfile.read(length)
                    if not raw and path.startswith('/reservations/') and path.endswith('/cancel'):
                        body = {}
                    else:
                        body = json.loads(raw.decode('utf-8'), parse_constant=reject_constant, parse_float=finite_float)
                except (ValueError, UnicodeError, RecursionError):
                    fail('malformed_request', 400)
                if type(body) is not dict:
                    fail('malformed_request', 400)
            query = {k: v[0] for k, v in parse_qs(split.query, keep_blank_values=True).items()}
            status, response = service.request(self.command, path, query, body, self.headers)
        except APIError as exc:
            status, response = exc.status, {'error': {'code': exc.code, 'message': str(exc)}}
        except (ValueError, OverflowError, TypeError, RecursionError):
            status, response = 422, {'error': {'code': 'validation_failed', 'message': 'Invalid request value'}}
        except Exception as exc:
            # Unexpected faults are reported without leaking private state.
            print('Unexpected application fault: ' + type(exc).__name__, file=sys.stderr, flush=True)
            status, response = 500, {'error': {'code': 'internal_error', 'message': 'Unexpected service error'}}
        encoded = b'' if response is None else json.dumps(response, ensure_ascii=True, separators=(',', ':'), allow_nan=False).encode('utf-8')
        try:
            self.send_response(status)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(encoded)))
            self.end_headers()
            if encoded:
                self.wfile.write(encoded)
        except (BrokenPipeError, ConnectionResetError):
            pass

    do_GET = do_POST = do_PATCH = do_PUT = do_DELETE = do_OPTIONS = handle_request


class Server(ThreadingHTTPServer):
    request_queue_size = 128
    daemon_threads = True
    block_on_close = False


if __name__ == '__main__':
    Server(('0.0.0.0', int(os.environ.get('PORT', '8080'))), Handler).serve_forever()
