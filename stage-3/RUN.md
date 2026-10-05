# Tablekeeper Stage 2

From this directory, build and start the standalone HTTP service:

```sh
docker build -t tablekeeper-stage-2 . && docker run --rm -e PORT=8080 -p 8080:8080 tablekeeper-stage-2
```

The service listens on `0.0.0.0`, defaults to port 8080, and responds to
`GET /health` immediately after initialization. It starts with empty state;
`POST /_test/reset` installs the supplied fixture. The image includes Python and
IANA timezone data. It needs no outbound runtime networking, volume, separate
database or other service. State is intentionally ephemeral across restarts.

Open `http://localhost:8080/` for restaurant search and booking. `/signup`, `/login`
and `/lookup` return the same local browser shell. JavaScript and CSS are served at
`/assets/app.js` and `/assets/styles.css` from the image; no CDN or external font is
needed. The JSON API keeps its Stage 1 URLs and authentication rules.

The Python standard-library threaded HTTP transport delegates to a service with
one lock around every observable state transition. Occupancy validation, record
updates and immutable retry receipts commit together. Batch moves validate all
candidate reservations against the final occupancy before publishing any change.
Reset and import validate a complete replacement before swapping state. Export
copies a coherent snapshot under the same lock.

`domain.py` centralizes JSON field validation, slot rules, half-open overlap,
scrypt password hashes and timezone conversion. Wall-clock starts resolve to the
first DST occurrence; nonexistent starts are rejected. Durations and overlap
comparisons use fixed-offset absolute instants, and responses convert back to
restaurant local time. Slot enumeration stops at the closing bound before adding
another step, including on the last supported calendar day. Boundary local dates
can remain valid even when their intermediate UTC year would be outside 1..9999.
`service.py` owns state and endpoint behavior; `server.py` owns HTTP parsing and
error envelopes. `json_value.py` preserves decimal JSON numbers exactly, including
large exponents, through request comparison, responses and state transfer without
expanding powers of ten. Test controls are enabled without authentication as required.

Exports include password hashes and bearer tokens. Treat them as private data.
Their opaque state contains JSON text so ordinary caller JSON libraries do not
round large receipt numbers; import accepts both this representation and the
earlier direct-object snapshot representation.
Import preserves those tokens, booking identities and original retry responses.
Reset clears accounts, sessions, reservations and receipts.

Restaurants may declare `combinable` pairs in their fixture. New bookings accept
either legacy `table_id` or `table_ids` with one or two members; sending both is
invalid. Two-member selections must exactly match an approved unordered pair.
Current records expose `table_ids`, with `table_id` additionally present for a
single member. Availability lists eligible singles first, then approved pairs in
declaration order as `available_options`, while `available_table_ids` stays single-only.

Each confirmed record occupies every selected member. Amendments explicitly replace
the selection before merging time/party defaults. Batch moves validate all resulting
member sets together and can perform single/pair swaps atomically. Pair cancellation
releases both members. JSON-body idempotency comparison happens before semantic
selection normalization, so reversed arrays are distinct requests under a used key.

An unchanged export from the accepted Stage 1 service can be imported directly.
Import preserves all passwords, sessions, references, timestamps and original
create/batch receipts; only current records gain `table_ids` and legacy configuration
gains an empty pair list. Historical Stage 1 replay responses remain verbatim,
including their original `table_id` shape. The browser accepts that legacy response
when recovering a pending booking without reload after an upgrade.

Run owner regressions without external dependencies from this directory:

```sh
python -m unittest discover -s tests -v
```
