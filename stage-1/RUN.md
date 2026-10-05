# Tablekeeper Stage 1

From this directory, build and start the standalone HTTP service:

```sh
docker build -t tablekeeper-stage-1 . && docker run --rm -e PORT=8080 -p 8080:8080 tablekeeper-stage-1
```

The service listens on `0.0.0.0`, defaults to port 8080, and responds to
`GET /health` immediately after initialization. It starts with empty state;
`POST /_test/reset` installs the supplied fixture. The image includes Python and
IANA timezone data. It needs no outbound runtime networking, volume, separate
database or other service. State is intentionally ephemeral across restarts.

The Python standard-library threaded HTTP transport delegates to a service with
one lock around every observable state transition. Occupancy validation, record
updates and immutable retry receipts commit together. Batch moves validate all
candidate reservations against the final occupancy before publishing any change.
Reset and import validate a complete replacement before swapping state. Export
copies a coherent snapshot under the same lock.

`domain.py` centralizes JSON field validation, slot rules, half-open overlap,
scrypt password hashes and timezone conversion. Wall-clock starts resolve to the
first DST occurrence; nonexistent starts are rejected. Durations and overlap
comparisons use UTC instants, and responses convert back to restaurant local time.
`service.py` owns state and endpoint behavior; `server.py` owns HTTP parsing and
error envelopes. Test controls are enabled without authentication as required.

Exports include password hashes and bearer tokens. Treat them as private data.
Import preserves those tokens, booking identities and original retry responses.
Reset clears accounts, sessions, reservations and receipts.

Run owner regressions without external dependencies from this directory:

```sh
python -m unittest discover -s tests -v
```
