"""Threaded HTTP transport; the service owns all application transactions."""
import os
import sys
from pathlib import Path
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, unquote, urlsplit

from domain import APIError, fail
from service import Service
from json_value import loads, dumps

service = Service()
PUBLIC = Path(__file__).resolve().parent / 'public'
ASSETS = {
    '/': ('index.html', 'text/html; charset=utf-8'),
    '/signup': ('index.html', 'text/html; charset=utf-8'),
    '/login': ('index.html', 'text/html; charset=utf-8'),
    '/lookup': ('index.html', 'text/html; charset=utf-8'),
    '/assets/app.js': ('app.js', 'application/javascript; charset=utf-8'),
    '/assets/styles.css': ('styles.css', 'text/css; charset=utf-8'),
}


class Handler(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def log_message(self, format, *args):
        # Do not log URLs, request bodies, credentials, session tokens or exports.
        pass

    def handle_request(self):
        try:
            split = urlsplit(self.path)
            path = unquote(split.path)
            if self.command == 'GET' and path in ASSETS:
                filename, content_type = ASSETS[path]
                try:
                    asset = (PUBLIC / filename).read_bytes()
                except FileNotFoundError:
                    fail('not_found', 404)
                self.send_response(200)
                self.send_header('Content-Type', content_type)
                self.send_header('Content-Length', str(len(asset)))
                self.send_header('Cache-Control', 'no-store')
                self.end_headers()
                self.wfile.write(asset)
                return
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
                        body = loads(raw.decode('utf-8'))
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
        encoded = b'' if response is None else dumps(response).encode('utf-8')
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
