# Tablekeeper Stage 3

From this directory, build and start the standalone HTTP service:

```sh
docker build -t tablekeeper-stage-3 . && docker run --rm -e PORT=8080 -p 8080:8080 tablekeeper-stage-3
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

Stage 3 adds complete dated policies at `/restaurants/{id}/policies`. Public reads
list publication order; manager-only writes require the ordinary idempotency key.
Manager IDs come from `manager_user_ids` in the reset fixture (default empty).
Policy selection uses the latest eligible effective date, then the greatest version
for ties. Restaurant detail continues to show the original fixture. `policies.py`
keeps that identity/configuration distinct from decision rules and immutable
`accepted_terms`. Publication never changes an accepted reservation's interval.
`explain=true` adds both independent single-table predicates to each availability
slot, in fixture/rule order; omission adds no explanations.

Current bookings carry `revision` and `accepted_terms`. PATCH optionally takes a
positive `expected_revision`; a stale revision precedes cutoff/change validation.
Editable semantic no-ops retain their terms, end time, history and revision, even
when a newer policy could not accept them. Real changes check the accepted cutoff
before validating the entire result under its date's policy. History events retain
their resulting terms/revision and actual field changes. GET owner-only `/history`
and `/decision` suffixes return 404 for anonymous or foreign callers.

`POST /series` adopts an existing editable anchor with a key and a count of 2..12,
at intervals of 1..4 calendar weeks. Its anchor stays unchanged. Generated starts
retain the local clock time and choose each date's policy/DST interpretation.
Each index is validated completely before the next, and nothing publishes until
every occurrence succeeds. Real individual changes mark permanent exceptions;
cancellation retains membership without newly marking an exception. Collective
moves commit histories/terms/revisions and at most one increment per affected series.
The private restaurant counter increments only for Stage 3 adoption and batches
with real changes; no later-stage general-counter behavior is implemented.

`state.py` validates the entire fixture or portable snapshot before replacement,
including retained policy snapshots, native history evolution, series membership,
counters and all four receipt families. Both accepted Stage 1 and Stage 2 exports
remain importable unchanged. Missing current metadata initializes revision 1 and
fixture policy 0; original receipt JSON is never enriched. Legacy history returns
`provenance: {"kind":"legacy_baseline","known_state":...}` and empty `entries`.
The known state contains the retained public record at migration, with only missing
current metadata initialized. It claims no earlier events or fabricated event times.
Future actual changes/cancellation start at seq 1. Native histories use
`{"kind":"native"}` and begin with the real creation event. Confirmed fixture seeds
get a creation event at actual reset initialization; cancelled fixture seeds use
`fixture_baseline` with their known state and no fabricated prior creation/cancellation.
Known native history and all timestamps are preserved through subsequent imports.

Exact feasible pair-capacity sums remain required, including disparate exponents.
The fixture/legacy numeric domain is unbounded: the exact sum of 10^N and 1 needs
N+1 significant decimal digits, so arbitrarily large N inherently conflicts with a
universal finite request/output budget. No unsupported numeric limit or approximation
is introduced. Compact parsing/comparison/receipts remain distinct from that expanded
output-size boundary. Owner/independent checks report observed finite coverage.

Run owner regressions without external dependencies from this directory:

```sh
python -m unittest discover -s tests -v
```
