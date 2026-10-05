# Tablekeeper Stage 3 cumulative requirements and risk ledger

This is the single authoritative cumulative Stage 3 analysis ledger for the FINAL SUBMISSION RUN. The Conductor's corrected complete handoff `d6a86c65-c85f-437e-9d8f-b9d48a51fb40` supplies the complete Stage 1+2+3 specification and confirms no differences from the read-only official local specifications. It supersedes the missing blocks in assignment `740f8d7d-aa54-4449-a516-bdd80741414b`. All source contracts were independently read; neither visible checks nor existing product code/docs/schema define this ledger.

Read-only source provenance: official repository FULL `803560d2a678ace1414465c098eb0ab5380ffade`; clean files under D:\dark\dark-factory-wearedevs\tablekeeper\spec. SHA256: stage-1.md `3b53451d4ad2b1e12765c97fd8bdff3fce20d56b6969a049c84e0bc302daf2cbd`; stage-2.md `192909e9f784e2e2849c996db1b5e86107bbbf7001f5cb31427dba69421d9abf`; stage-3.md `73629edfd9b38d6671eef00974e6bcb95e39171e9ed10767a57840a6ea778528`.

Stage 1 is independently ACCEPTED only at production `d41a7627711951a07ce7a1718fac47c6ea5b6dd4`, evidence `e4a923e5fda0857e9e28221e92ff0bcfb49641a4`; accepted source/evidence are frozen. Stage 2 analysis `4e11f5e91e2186a5461345977f08a1c51f4d057f` supplies 338 stable inherited IDs. Neither historical acceptance nor this ledger accepts Stage 3 production. Stage 3 implementation requires Stage 2 formal ACCEPT plus a committed copied baseline first.

## Record conventions owners and evidence

Every row records stable ID, source, atomic obligation, risk/categories, dependencies, production owner, independent verification strategy and compatibility duty. C=CRITICAL, H=HIGH, M=MEDIUM, L=LOW. Tags: TX atomicity/rollback; CC serialization/races; RP retries/original receipts; AU authorization/privacy; TM calendar/DST/cutoff; VA type/value/range; OR precedence/order; ST portable state; HT historical truth; UI browser behavior; QA rendered quality; DEP offline deployment; HTTP protocol; SC release scope.

All inherited TK1/TK2 IDs retain their identity and V01..V20/W01..W20 obligations. Inherited dependencies abbreviate TK1 IDs where originally used; new dependencies are fully qualified. Inherited TK1 rows default owner S except CON annotations. Owner S=Systems Engineer (backend/container/docs), E=Experience Engineer (browser), C=Conductor (release); S/E indicates the interface boundary. New Stage 3 rows default to S unless their Owner column differs. Verifier owns independent cases and exact-SHA formal verdict. Auditor owns only evidence/stage-3/requirements.md, never production acceptance or implementation.

Defaults for each inherited/new requirement: **OPEN / Stage 3 production unverified**, **visible-check coverage UNKNOWN (not inspected)**, **evidence reference NONE**. V/W/Z procedures are concrete independent-evidence obligations. Historical Stage 1 closure is provenance and a required regression baseline, not closure at a Stage 3 SHA. Record future exact SHA, case ID and sanitized evidence for any closure. Stage-specific release bookkeeping IDs describe their historical gates; they do not recreate past work.

Compatibility S=current configuration/identity/owner/status/timestamps/state through required transfer; R=exact successful request bodies/original response receipts, including old field shapes; B=retained browser session/reference/form/pending replay identity; H=immutable policies/accepted terms/history/revisions; A=agreement membership/indices/exceptions/counters. Combined letters accumulate obligations. Format1 opaque snapshots remain portable; no later-stage downgrade, Stage 4 general counter API, crash persistence, new history/explanation screens or unspecified management UI is invented.

## Inherited specialization map

All338 inherited IDs are reproduced below, with explicit Stage 3 specialization where semantics evolve. Other inherited wording retains its cumulative meaning.

| Inherited IDs | Stage 3 specialization |
|---|---|
| TK1-SC-04 | Assigned folder contains cumulative Stages1+2+3, no future-stage production. |
| TK1-AUTH-10; TK1-AUTH-11; TK1-ERR-10 | Public policy list added; history/decision/series owner reads use anonymous/nonowner404 exceptions; other protected writes remain401 for missing auth. |
| TK1-FIX-09..12; TK1-AV-04; TK1-AV-07; TK2-PAIR-06; TK2-OPTIONS-04 | Current decisions select date-effective policy; existing occupancy and cutoff use retained accepted terms. Original detail remains fixture configuration. |
| TK1-IDEM-01 | Policy-publication and series-adoption paths join create/moves, retaining user/method/path/full-body identity. |
| TK1-CREATE-01; TK1-GET-03; TK2-SELECT-06 | New/current reservation responses add revision/accepted_terms; historical original replay JSON stays unchanged. |
| TK1-PATCH-01; TK1-PATCH-03; TK1-PATCH-04; TK1-MOVE-06; TK1-MOVE-11; TK1-MOVE-13 | Optional expected_revision controls, accepted cutoff, no-op retention, real change validates complete result against result date policy; per-item stale priority precedes cutoff/changes. |
| TK1-CANCEL-04; TK1-PATCH-07; TK1-MOVE-17; TK1-MOVE-20 | Accepted cutoff and atomic histories/terms/revisions/agreement flags; no-op preserves existing accepted state. |
| TK2-UP-01; TK2-UP-11 | Old requests/receipts remain supported by current service; Stage 3 additionally accepts both populated Stage1 and2 exports. |

The adopted historical-receipt rule is normative run guidance: new/current representations gain later fields, but old successful receipts retain their exact original JSON, with no revision/terms/table_ids enrichment. Full parsed-body identity precedes unordered selection normalization, so reversed arrays differ under a used key. Stage 3 additionally makes a reversed pair alone a semantic no-op amendment.

## Active inherited Stage 1 atomic requirements

### Scope delivery and runtime

| ID | Source | Atomic requirement | Risk/tags | Dependencies | Verify | Compat |
|---|---|---|---|---|---|---|
| TK1-SC-01 |§1 + Stage 2 | Expose the required HTTP API; Stage 2 additionally requires the specified browser screens. | M SC | - | V01 | - |
| TK1-SC-02 | Intro | Do not use source code from existing products in this domain. Owner CON. | H SC | - | V01 | - |
| TK1-SC-03 | Intro | Do not use existing domain-product API documentation or schemas. Owner CON. | H SC | - | V01 | - |
| TK1-SC-04 | Assignment + Stage 2 + Stage 3 | Assigned Stage 3 folder implements cumulative Stages 1, 2 and 3 only. Owner CON. | H SC | - | V01 | - |
| TK1-RUN-01 | §2 | Deliver a Dockerfile that builds the submitted HTTP service. | H DEP | SC-01 | V01 | - |
| TK1-RUN-02 | §2 | Deliver RUN.md with a build/start command requiring no manual setup. Owner Systems Engineer. | M DEP | RUN-01 | V01 | - |
| TK1-RUN-03 | §2 | Image operates alone using PORT and port mapping, without Compose startup. | H DEP | RUN-01 | V01 | - |
| TK1-RUN-04 | §2 | Runtime dependencies, initialization and seed data work inside the single container with no outbound network. | H DEP ST | RUN-03 | V01 | - |
| TK1-RUN-05 | §2 | Runtime assets/dependencies are included in the image. | H DEP | RUN-04 | V01 | - |
| TK1-RUN-06 | §2 | Service operates within 2 vCPU. | H DEP CC | RUN-03 | V01,V16 | - |
| TK1-RUN-07 | §2 | Ordinary requests complete within 5 seconds, at up to 50 requests in flight. | H CC HTTP | RUN-06 | V16 | - |
| TK1-RUN-08 | §§2,10 | Test control calls complete within 10 seconds. | H ST HTTP | RUN-06 | V02,V18 | - |
| TK1-RUN-09 | §3.1 | Listen on 0.0.0.0 at PORT when supplied. | H DEP | RUN-03 | V01 | - |
| TK1-RUN-10 | §3.1 | Default listening port is 8080. | M DEP | RUN-03 | V01 | - |
| TK1-RUN-11 | §3.2 | GET /health returns 200 and {"status":"ok"} once both service and store can serve requests. | H HTTP ST | RUN-04 | V01 | - |
| TK1-RUN-12 | §§2,3.2 | First healthy response occurs within 60 seconds of container start. | H DEP | RUN-11 | V01 | - |
| TK1-RUN-13 | §2 | Service operates within 2 GiB memory. | H DEP CC | RUN-03 | V01,V16 | - |
| TK1-HTTP-01 |§3.4 + Stage 2 | API requests/responses use application/json; charset=utf-8 (204 has no content); required screen routes return HTML. | M HTTP | - | V03 | - |
| TK1-HTTP-02 | §3.4 | Response timestamps are RFC3339 with an explicit offset. | H TM HTTP | - | V03,V09 | S |
| TK1-HTTP-03 | §3.4 | Ignore unknown request-body fields without error. | H VA | - | V03,V06 | - |
| TK1-HTTP-04 | §3.4 | Ignore unknown query parameters. | M VA | - | V03 | - |
| TK1-HTTP-05 | §3.4 | IDs are opaque strings at most 64 characters, including fixture-supplied IDs. | H VA ST | - | V03,V02 | S |

### Fixture and error semantics

| ID | Source | Atomic requirement | Risk/tags | Dependencies | Verify | Compat |
|---|---|---|---|---|---|---|
| TK1-FIX-01 | §3.3 | POST /_test/reset is enabled in the image and unauthenticated. | H ST HTTP | RUN-04 | V02 | - |
| TK1-FIX-02 | §3.3 | Successful reset replaces all service state with the supplied fixture. | C ST TX | FIX-01 | V02,V20 | - |
| TK1-FIX-03 | §3.3 | Reset returns 204 with no body. | M HTTP | FIX-02 | V02 | - |
| TK1-FIX-04 | §3.3 | After reset returns, subsequent calls see only that fixture. | C ST CC | FIX-02 | V02,V20 | - |
| TK1-FIX-05 | §3.3 | Repeated resets are supported. | H ST | FIX-02 | V02 | - |
| TK1-FIX-06 | §4 + Stage 3 | Original restaurant/table fixture configuration is supplied through reset; creation endpoints remain out of scope. Only dated policy publication extends decision rules. | M SC | FIX-02 | V02 | S |
| TK1-FIX-07 | §4 | Preserve restaurant IANA timezone and local-time configuration. | H TM ST | FIX-02 | V02,V09 | S |
| TK1-FIX-08 | §4 | Missing weekday entry denotes a closed day. | H TM | FIX-07 | V08 | S |
| TK1-FIX-09 | §4 + Stage 3 | Use the selected or retained accepted policy's opening-anchored slot grid as applicable. | H TM VA | FIX-07 | V08,V10 | S |
| TK1-FIX-10 | §4 + Stage 3 | Use the date-selected duration for new/real amended bookings; existing/no-op bookings retain their accepted duration. | H TM ST | FIX-07 | V08,V10 | S |
| TK1-FIX-11 | §4 + Stage 3 | Use the reservation's accepted cancellation cutoff against its current start. | H TM ST | FIX-07 | V12,V13 | S |
| TK1-FIX-12 | §4 + Stage 3 | Use selected policy table capacities for current decisions; retain original fixture capacities in original detail. | H VA ST | FIX-02 | V08,V10 | S |
| TK1-FIX-13 | §4 | Seeded users can immediately log in with fixture passwords. | H AU ST | FIX-02,AUTH-12 | V02,V04 | S |
| TK1-FIX-14 |§4 + Stage 2 | Seeded reservations retain supplied selection/body fields, id, reference and user_id; default confirmed unless explicitly cancelled. | H ST AU | FIX-02 | V02,V11 | S |
| TK1-FIX-15 | §4 | Seeded confirmed reservations participate in occupancy. | C TX ST | FIX-14,OCC-01 | V02,V08 | S |
| TK1-FIX-16 | §4 | Do not reject a booking solely for a past start date. | H TM VA | FIX-07 | V10 | - |
| TK1-FIX-17 | §4 | Past bookings remain subject to cancellation/amendment cutoffs. | H TM | FIX-16,FIX-11 | V12,V13 | S |
| TK1-ERR-01 | §5 | Every 4xx/5xx response uses error.code and a human-readable error.message. | H HTTP | - | V03 | - |
| TK1-ERR-02 | §5 | Unparseable body returns 400 malformed_request. | H VA HTTP | ERR-01 | V03 | - |
| TK1-ERR-03 | §5 | Wrong JSON field types return 400 malformed_request except explicit endpoint overrides. | H VA OR | ERR-01 | V03,V14 | - |
| TK1-ERR-04 | §5 | Missing required field/query returns 422 validation_failed unless a specific code applies. | H VA OR | ERR-01 | V03 | - |
| TK1-ERR-05 | §5 | Correct-type invalid format/range/length returns 422 validation_failed unless a specific code applies. | H VA OR | ERR-01 | V03 | - |
| TK1-ERR-06 | §5 | Invalid party_size, including string, boolean, fractional or below 1, is 422 validation_failed. | H VA OR | ERR-05 | V03,V10,V13,V14 | - |
| TK1-ERR-07 | §5 | A starts_at_local string not bare YYYY-MM-DDTHH:MM is 422 validation_failed. | H TM VA OR | ERR-05 | V03,V09 | - |
| TK1-ERR-08 | §5 | Integer query values use plain decimal digits; 1e9, 4.0 and +4 are 422 validation_failed. | H VA | ERR-05 | V03,V08 | - |
| TK1-ERR-09 | §5 + Stage 3 | A nonempty Idempotency-Key exceeding 255 characters is 422 validation_failed on all four required-key write families. | H VA RP | ERR-05 | V06 | - |
| TK1-ERR-10 | §5 + Stage 3 | Missing/malformed/unknown bearer identity gives 401 on ordinary protected endpoints, with Stage 3 owner-only read exceptions. | H AU | ERR-01 | V05 | - |
| TK1-ERR-11 | §5 | Authenticated forbidden access uses 403 forbidden when applicable; reservation-owner rules specifically require 404. | H AU OR | ERR-01,GET-04 | V05 | - |
| TK1-ERR-12 | §5 | Missing/nonvisible resources use 404 not_found where specified. | H AU HTTP | ERR-01 | V05,V10,V14 | - |
| TK1-ERR-13 | §5 | Requests never produce 5xx, including under concurrent load. | C CC HTTP | ERR-01 | V03,V16,V20 | - |

### Authentication and privacy

| ID | Source | Atomic requirement | Risk/tags | Dependencies | Verify | Compat |
|---|---|---|---|---|---|---|
| TK1-AUTH-01 | §6 | Signup returns 201 with user_id, display_name and token. | H AU HTTP | ERR-01 | V04 | S |
| TK1-AUTH-02 | §6 | Signup rejects registered email with 409 email_taken. | H AU CC | AUTH-01 | V04,V16 | S |
| TK1-AUTH-03 | §6 | Signup password shorter than 8 characters gives 422 validation_failed. | H VA AU | ERR-05 | V04 | - |
| TK1-AUTH-04 | §6 | Invalid local@domain email format gives 422 validation_failed. | M VA | ERR-05 | V04 | - |
| TK1-AUTH-05 | §6 | Valid login returns 200 with user_id, display_name and token. | H AU HTTP | AUTH-01,FIX-02 | V04 | S |
| TK1-AUTH-06 | §6 | Wrong password gives 401 unauthenticated. | H AU | AUTH-05 | V04 | - |
| TK1-AUTH-07 | §6 | Unknown login email gives 401 unauthenticated. | H AU | AUTH-05 | V04 | - |
| TK1-AUTH-08 | §6 | Tokens never expire. | H AU TM | AUTH-01,AUTH-05 | V04,V18 | S |
| TK1-AUTH-09 | §6 | Multiple valid tokens/sessions for an account coexist. | H AU CC | AUTH-08 | V04,V16 | S |
| TK1-AUTH-10 | §§6,8,10 + Stage 3 | Health/reset/signup/login/public browsing/export/import and GET policy lists require no bearer token; browser routes retain their public behavior. | H AU HTTP | - | V05 | - |
| TK1-AUTH-11 | §§6,8,11 + Stage 3 | Protected operations require bearer identity; history/decision/series reads use their explicit owner-only 404 exceptions. | C AU | AUTH-08 | V05 | S |
| TK1-AUTH-12 | §6 | Store passwords only using a password-hashing function or equivalent; plaintext storage prohibited. | C AU ST | - | V04,V18 | S |

### Occupancy and idempotency

| ID | Source | Atomic requirement | Risk/tags | Dependencies | Verify | Compat |
|---|---|---|---|---|---|---|
| TK1-OCC-01 |§1 + Stage 2 | Two confirmed bookings never overlap on any member table in the same restaurant. | C TX CC | FIX-10 | V10,V16,V20 | S |
| TK1-OCC-02 |§1 + Stage 2 | Each member table occupies the half-open absolute interval [start,start+duration). | C TM TX | FIX-10,TIME-05 | V10,V09 | S |
| TK1-OCC-03 | §1 | Concurrent competing writes preserve OCC-01. | C CC TX | OCC-01 | V16 | S |
| TK1-OCC-04 | §1 | Retries never create duplicate bookings. | C RP CC | IDEM-08 | V06,V16 | R |
| TK1-OCC-05 | §1 | Rejected requests create no partial bookings. | C TX | OCC-01 | V10,V13,V14,V20 | S |
| TK1-IDEM-01 | §7 + Stage 3 | Create, moves, policy publication and series adoption require Idempotency-Key under the same user/method/path/full-body rules. | H RP HTTP | AUTH-11 | V06 | - |
| TK1-IDEM-02 | §7 | Absent/empty key returns 400 missing_idempotency_key. | H VA RP | IDEM-01 | V06 | - |
| TK1-IDEM-03 | §7 | Key scope isolates different authenticated users. | C AU RP | AUTH-11 | V06,V16 | R |
| TK1-IDEM-04 | §7 | Receipt lookup distinguishes method/path; same key/body on another required path is independent. | C RP OR | IDEM-03 | V06,V15 | R |
| TK1-IDEM-05 | §7 | After parsing an object and authenticating, resolve idempotency before endpoint field validation. | C RP OR | ERR-02,AUTH-11 | V06 | R |
| TK1-IDEM-06 | §7 | Resolve idempotency before current-resource checks. | C RP OR | IDEM-05 | V06,V15 | R |
| TK1-IDEM-07 | §7 | Successful first use returns normal 201. | H HTTP RP | IDEM-01 | V06 | R |
| TK1-IDEM-08 | §7 | Same request replay returns 200 and original response as the same JSON value. | C RP ST | IDEM-07 | V06,V15,V18 | R |
| TK1-IDEM-09 | §7 | Concurrent identical unused-key requests yield exactly one 201, others 200, with one effect and identical bodies. | C CC RP TX | IDEM-08,OCC-01 | V16 | R |
| TK1-IDEM-10 | §7 | Used key with different parsed JSON body returns 409 idempotency_key_reuse. | C RP VA OR | IDEM-05 | V06 | R |
| TK1-IDEM-11 | §7 | Compare JSON values, ignoring object key order and textual whitespace. | H RP VA | IDEM-10 | V06 | R |
| TK1-IDEM-12 | §7 | Keys from failed 4xx requests remain reusable as first use. | C RP TX | OCC-05 | V06,V14,V18 | R |
| TK1-IDEM-13 | §7 | Replay after amendment/cancellation returns original receipt. | C RP ST | IDEM-08 | V15,V18 | R |
| TK1-IDEM-14 | §7 | Replay makes no further state changes. | C RP TX | IDEM-13 | V15,V20 | R |

### Browsing and availability

| ID | Source | Atomic requirement | Risk/tags | Dependencies | Verify | Compat |
|---|---|---|---|---|---|---|
| TK1-BROWSE-01 | §8 | Restaurant list returns restaurants with id, name and timezone. | M HTTP ST | FIX-02 | V07 | S |
| TK1-BROWSE-02 | §8 | Restaurant detail returns fixture-shaped policy, hours and tables. | H HTTP ST | FIX-07 | V07 | S |
| TK1-BROWSE-03 | §8 | Unknown restaurant detail returns 404 not_found. | M HTTP | ERR-12 | V07 | - |
| TK1-AV-01 | §8 | Availability requires restaurant_id, date and party_size; missing parameter is 422 validation_failed. | H VA | ERR-04 | V08 | - |
| TK1-AV-02 | §8 | Availability date is the restaurant-local calendar date. | H TM | FIX-07 | V08,V09 | S |
| TK1-AV-03 | §8 | Availability returns restaurant_id, date, timezone and slots. | M HTTP | AV-01 | V08 | S |
| TK1-AV-04 | §8 + Stage 3 | Enumerate the date-selected policy's opening grid slots whose absolute duration fits by closing. | H TM OR | FIX-09,FIX-10,TIME-05 | V08,V09 | S |
| TK1-AV-05 | §8 | Each slot exposes full local YYYY-MM-DDTHH:MM and offset-bearing starts_at for the same instant. | H TM HTTP | TIME-01 | V08,V09 | S |
| TK1-AV-06 | §8 | Available tables belong to the queried restaurant. | H ST | FIX-02 | V08 | S |
| TK1-AV-07 | §8 + Stage 3 | Available singles have selected-policy capacity at least queried party_size. | H VA | FIX-12 | V08 | S |
| TK1-AV-08 |§8 + Stage 2 | Available single tables have no overlapping confirmed reservation containing that member. | C TX TM | OCC-01,OCC-02 | V08,V16 | S |
| TK1-AV-09 | §8 | Available table IDs appear in fixture order. | H OR ST | FIX-02 | V08,V18 | S |
| TK1-AV-10 | §8 | Keep slots with no available tables, with an empty array. | H HTTP | AV-04 | V08 | S |
| TK1-AV-11 | §8 | Closed day returns slots: []. | H TM HTTP | FIX-08 | V08 | S |
| TK1-AV-12 | §8 | Returned starts_at_local can be used unchanged to create a reservation. | H TM VA | AV-05,CREATE-01 | V08,V09 | S |

### Creation reads and reservation lifecycle

| ID | Source | Atomic requirement | Risk/tags | Dependencies | Verify | Compat |
|---|---|---|---|---|---|---|
| TK1-CREATE-01 | §8 + Stage 2 + Stage 3 | Create accepts legacy/new selection, local start and party; returns 201 current reservation shape with revision and accepted_terms, except immutable historical replay JSON. | H HTTP ST | IDEM-01 | V10 | S |
| TK1-CREATE-02 | §8 | Resolve bare local start in the restaurant's zone. | H TM | FIX-07,TIME-01 | V09,V10 | S |
| TK1-CREATE-03 | §8 | New reservation status is confirmed. | H ST | CREATE-01 | V10 | S |
| TK1-CREATE-04 | §8 | Reference is 6..12 characters in A-Z0-9. | H VA ST | CREATE-01 | V10 | S |
| TK1-CREATE-05 | §8 | Reference is unique across all reservations, including seeded/cancelled ones. | C ST CC | FIX-14,CREATE-04 | V10,V16 | S |
| TK1-CREATE-06 | §8 | Reference never changes. | C ST | CREATE-04 | V13,V14,V18 | S |
| TK1-CREATE-07 | §8 | Overlapping occupancy returns 409 table_unavailable. | C TX HTTP | OCC-01 | V10,V16 | - |
| TK1-CREATE-08 | §8 | Off-grid start returns 422 not_on_slot_grid. | H TM VA | FIX-09 | V10 | - |
| TK1-CREATE-09 | §8 | Outside hours or end after closing returns 422 outside_opening_hours. | H TM VA | FIX-08,FIX-10,TIME-05 | V09,V10 | - |
| TK1-CREATE-10 | §8 | Positive integer party exceeding capacity returns 422 party_exceeds_capacity. | H VA OR | ERR-06,FIX-12 | V10 | - |
| TK1-CREATE-11 | §8 | Unknown restaurant returns 404 not_found. | H HTTP | ERR-12 | V10 | - |
| TK1-CREATE-12 | §8 | Unknown table returns 404 not_found. | H HTTP | ERR-12 | V10 | - |
| TK1-CREATE-13 | §8 | Table from another restaurant returns 404 not_found. | H ST AU | CREATE-11 | V10 | - |
| TK1-GET-01 | §8 | List returns only caller's reservations. | C AU | AUTH-11 | V05,V11 | S |
| TK1-GET-02 | §8 | List orders reservations by starts_at descending. | H OR ST | GET-01 | V11,V13 | S |
| TK1-GET-03 | §8 + Stage 3 | Current list entries have current create-response shape including revision/accepted_terms; no records returns reservations: []. | M HTTP | GET-01 | V11 | S |
| TK1-GET-04 | §8 | Reference lookup returns caller's record; unknown/another owner's reference returns 404 without leaking existence. | C AU | AUTH-11 | V05,V11 | S |
| TK1-GET-05 | §8 | List includes both confirmed and cancelled reservations. | H ST | GET-01 | V11,V12 | S |
| TK1-CANCEL-01 | §8 | Successful cancel returns 200 with current reservation state and status cancelled. | H HTTP ST | GET-04 | V12 | S |
| TK1-CANCEL-02 |§8 + Stage 2 | Cancellation releases every member's occupancy immediately for the next availability read. | C TX CC | CANCEL-01,AV-08 | V12,V16 | S |
| TK1-CANCEL-03 | §8 | Cancelling an already-cancelled record returns 200 with current state. | H ST OR | CANCEL-01 | V12 | S |
| TK1-CANCEL-04 | §8 + Stage 3 | Confirmed cancellation at/after accepted cutoff boundary returns 409 cutoff_passed. | H TM OR | FIX-11 | V12 | - |
| TK1-CANCEL-05 | §8 | Cancellation of another owner's/unknown reference returns 404 not_found. | C AU | GET-04 | V05,V12 | - |
| TK1-PATCH-01 | §8 + Stage 2 + Stage 3 | PATCH accepts optional expected_revision and any subset of selection/time/party; omitted state retains current values. | H ST VA | GET-04 | V13 | S |
| TK1-PATCH-02 | §8 | PATCH requires no idempotency key. | H HTTP | PATCH-01 | V13 | - |
| TK1-PATCH-03 | §8 + Stage 3 | Real PATCH validates all resulting fields against result-date policy under create codes; no-op retains accepted state instead of adopting new policy. | H VA TM | CREATE-07..13,ERR-06..07 | V13 | - |
| TK1-PATCH-04 | §8 + Stage 3 | PATCH checks retained accepted cutoff against current start, after applicable expected_revision stale check. | H TM OR | FIX-11 | V13 | - |
| TK1-PATCH-05 | §8 | PATCH of cancelled record returns 409 reservation_cancelled. | H ST OR | CANCEL-01 | V13 | - |
| TK1-PATCH-06 | §8 | Successful PATCH releases old occupancy and acquires new occupancy together. | C TX CC | OCC-01 | V13,V16 | S |
| TK1-PATCH-07 | §8 + Stage 3 | Failed PATCH preserves record, all occupancy, accepted terms/end time, revisions/history and series exception state. | C TX ST | PATCH-06 | V13,V20 | S |
| TK1-PATCH-08 | §8 | PATCH preserves reservation_id and reference. | C ST | CREATE-06 | V13,V18 | S |

### Time and DST

| ID | Source | Atomic requirement | Risk/tags | Dependencies | Verify | Compat |
|---|---|---|---|---|---|---|
| TK1-TIME-01 | §9 | Dates/times follow IANA zone rules for the actual fixture date. | H TM | FIX-07 | V09 | S |
| TK1-TIME-02 | §9 | Skipped spring-forward times never appear in availability. | H TM | TIME-01,AV-04 | V09 | S |
| TK1-TIME-03 | §§8,9 | Booking a nonexistent local time returns 422 invalid_local_time. | H TM VA | TIME-01 | V09 | - |
| TK1-TIME-04 | §9 | Repeated local times always resolve to the first occurrence before clocks change. | C TM TX | TIME-01 | V09 | S |
| TK1-TIME-05 | §9 | Duration is absolute elapsed time rather than wall-clock addition. | C TM TX | TIME-01,FIX-10 | V09 | S |
| TK1-TIME-06 | §9 | Response offsets reflect the correct zone/date, independently at start and end. | H TM HTTP | TIME-05,HTTP-02 | V09 | S |
| TK1-TIME-07 | §9 | Handle Berlin 2026-03-29 skipped 02:00..02:59 and 2026-10-25 repeated 02:00..02:59. | H TM | TIME-02..06 | V09 | S |
| TK1-TIME-08 | §9 | Handle New York 2026-03-08 skipped 02:00..02:59 and 2026-11-01 repeated 01:00..01:59. | H TM | TIME-02..06 | V09 | S |
| TK1-TIME-09 | §9 | A repeated local slot appears once in availability. | H TM OR | TIME-04,AV-04 | V09 | S |
| TK1-TIME-10 | §9 | The second occurrence of a repeated local start is not bookable. | H TM VA | TIME-04 | V09 | - |

### Export import and continuity

| ID | Source | Atomic requirement | Risk/tags | Dependencies | Verify | Compat |
|---|---|---|---|---|---|---|
| TK1-XFER-01 | §10 | Unauthenticated GET /_test/export returns 200 and a JSON object with track tablekeeper, format_version 1 and opaque object state. | H HTTP ST | AUTH-10 | V17 | S |
| TK1-XFER-02 | §10 | Export is an atomic read-only state snapshot. | C ST TX CC | OCC-01,IDEM-09 | V17,V20 | S |
| TK1-XFER-03 | §10 | Later source writes do not change the already-exported snapshot. | C ST TX | XFER-02 | V17,V18 | S |
| TK1-XFER-04 | §10 | Import accepts an unchanged export from this service in a different process. | C ST DEP | XFER-01 | V18 | S |
| TK1-XFER-05 | §10 | Import has no dependency on source process/files/volume/port/network address. | C ST DEP | XFER-04 | V18 | S |
| TK1-XFER-06 | §10 | Successful import atomically replaces all destination state and returns 204. | C ST TX CC | XFER-04 | V18,V20 | S |
| TK1-XFER-07 | §10 | Import removes previous destination data and credentials rather than merging. | C ST AU | XFER-06 | V18 | S |
| TK1-XFER-08 | §10 | Repeated import restores the exported state without duplicates. | C RP ST | XFER-06 | V18,V19 | S |
| TK1-XFER-09 | §10 | Invalid JSON on import follows §5 malformed_request behavior. | H VA | ERR-02 | V19 | - |
| TK1-XFER-10 | §10 | Missing fields/wrong track/wrong version/invalid state return 422 validation_failed. | H VA OR | ERR-05 | V19 | - |
| TK1-XFER-11 | §10 | Invalid import leaves all destination state unchanged. | C TX ST AU | XFER-10 | V19,V20 | S |
| TK1-XFER-12 | §10 | Preserve accounts and usable hashed-password login after import. | C AU ST | AUTH-12,XFER-06 | V18 | S |
| TK1-XFER-13 | §10 | Preserve every existing bearer token after import. | C AU ST | AUTH-09,XFER-06 | V18 | S |
| TK1-XFER-14 | §10 | Preserve fixture configuration, including table order and local policies. | H ST OR TM | FIX-07..12,XFER-06 | V18 | S |
| TK1-XFER-15 | §10 | Preserve reservations and references, including cancelled records. | C ST | CANCEL-01,CREATE-06,XFER-06 | V18 | S |
| TK1-XFER-16 | §10 | Preserve identities without regeneration. | C ST | XFER-15 | V18 | S |
| TK1-XFER-17 | §10 | Preserve completed idempotent request bodies and original responses. | C RP ST | IDEM-08,XFER-06 | V18 | R |
| TK1-XFER-18 | §10 | Failed request keys remain reusable after import. | C RP ST | IDEM-12,XFER-06 | V18 | R |
| TK1-XFER-19 | §10 | Existing references, tokens, successful receipts and retries remain valid after import. | C ST RP AU | XFER-12..18 | V18 | R |
| TK1-XFER-20 | §10 | Reset clears imported state and its credentials/receipts. | C ST AU RP | FIX-02,XFER-06 | V02,V18 | - |
| TK1-XFER-21 | §10 | Exports containing credentials/tokens remain private test artifacts; do not commit them. | C AU | XFER-01 | V01,V18 | - |
| TK1-XFER-22 | §10 | Preserve statuses without regeneration. | C ST | XFER-15 | V18 | S |
| TK1-XFER-23 | §10 | Preserve timestamps without regeneration. | C ST TM | XFER-15 | V18 | S |

### Atomic reservation moves

| ID | Source | Atomic requirement | Risk/tags | Dependencies | Verify | Compat |
|---|---|---|---|---|---|---|
| TK1-MOVE-01 | §11 | Moves requires authentication; missing token returns 401 unauthenticated. | C AU | AUTH-11 | V05,V14 | - |
| TK1-MOVE-02 | §11 | Moves requires the §7 idempotency key semantics. | C RP | IDEM-01..14 | V06,V15 | R |
| TK1-MOVE-03 | §11 | moves is an array of objects with string references; invalid shape gives 422 validation_failed. | H VA OR | ERR-01 | V14 | - |
| TK1-MOVE-04 | §11 | Every referenced reservation belongs to caller; unknown/other-owner reference returns 404 not_found. | C AU | GET-04 | V05,V14 | - |
| TK1-MOVE-05 | §11 | All bookings are from the same restaurant; mixed restaurants return 422 validation_failed. | H ST VA | MOVE-04 | V14 | - |
| TK1-MOVE-06 | §11 + Stage 2 + Stage 3 | Items accept ordinary PATCH fields including table_ids and optional expected_revision; omitted values retain current state. | H ST VA | PATCH-01 | V14 | S |
| TK1-MOVE-07 | §11 | Ignore unknown item fields. | H VA | HTTP-03 | V14,V15 | - |
| TK1-MOVE-08 | §11 | Each booking keeps identity, owner and creation time. | C ST AU | PATCH-08 | V14,V18 | S |
| TK1-MOVE-09 | §11 | Cancelled listed booking returns 409 reservation_cancelled. | H ST OR | PATCH-05 | V14 | - |
| TK1-MOVE-10 | §11 | Apply each listed booking's existing-start cutoff. | H TM OR | PATCH-04 | V14 | - |
| TK1-MOVE-11 | §11 + Stage 3 | Non-occupancy move errors use ordinary amendment codes, including expected_revision type/range and stale rules. | H VA OR | PATCH-03 | V14 | - |
| TK1-MOVE-12 | §11 | Non-occupancy errors take precedence in input order. | C OR TX | MOVE-11 | V14 | - |
| TK1-MOVE-13 | §11 + Stage 3 | Per item, optional revision stale checks precede accepted cutoff; accepted cutoff precedes proposed changes. | C OR TM | MOVE-10 | V14 | - |
| TK1-MOVE-14 |§11 + Stage 2 | Any member overlap among resulting listed bookings gives 409 table_unavailable. | C TX | OCC-01,MOVE-12 | V14 | - |
| TK1-MOVE-15 |§11 + Stage 2 | Any member overlap with an unlisted confirmed booking gives 409 table_unavailable. | C TX | OCC-01,MOVE-12 | V14,V16 | - |
| TK1-MOVE-16 |§11 + Stage 2 | Unchanged listed bookings retain every member's occupancy. | C TX ST | MOVE-06 | V14 | S |
| TK1-MOVE-17 | §11 + Stage 3 | Moves commit records/member occupancy, accepted terms/histories/revisions/series flags and receipt together, or none. | C TX RP CC | MOVE-14..16,IDEM-12 | V14,V16,V20 | R |
| TK1-MOVE-18 | §11 | Success returns 201 with a reservations array. | H HTTP | MOVE-17 | V14,V15 | R |
| TK1-MOVE-19 | §11 | Replays return original response with 200 after later amendments/cancellations. | C RP ST | IDEM-13,MOVE-18 | V15,V18 | R |
| TK1-MOVE-20 | §11 + Stage 3 | No-op moves retain all existing accepted terms, end times, reservation revisions and history. | C ST TX | MOVE-06 | V14,V15,V18 | S |
| TK1-MOVE-21 | §11 | Export/import preserves successful batch receipts as well as resulting bookings. | C RP ST | XFER-17,MOVE-18 | V18 | R |
| TK1-MOVE-22 | §11 | Successful reservations array preserves input order. | H OR | MOVE-18 | V14,V15 | R |
| TK1-MOVE-23 | §11 | Successful reservations array includes unchanged items. | H HTTP ST | MOVE-18 | V14,V15 | R |
| TK1-MOVE-24 | §11 | moves length must be 1..8; other lengths give 422 validation_failed. | H VA | MOVE-03 | V14 | - |
| TK1-MOVE-25 | §11 | References must be distinct; duplicates give 422 validation_failed. | H VA | MOVE-03 | V14 | - |

## Active inherited Stage 2 atomic requirements

Sources below name Stage 2 headings; § references still refer to Stage 1. Dependencies on an inherited group mean its named baseline obligation plus these additions, not permission to weaken that baseline.

### Browser routes authentication and search

| ID | Source | Atomic requirement | Risk/tags | Dependencies | Owner | Verify | Compat |
|---|---|---|---|---|---|---|---|
| TK2-WEB-01 | Routes | URL / reaches search/availability screen and returns HTML. | H HTTP UI | TK1-RUN-03 | S/E | W01 | - |
| TK2-WEB-02 | Routes | URL /signup reaches signup screen and returns HTML. | H HTTP UI | TK2-WEB-01 | S/E | W01 | - |
| TK2-WEB-03 | Routes | URL /login reaches login screen and returns HTML. | H HTTP UI | TK2-WEB-01 | S/E | W01 | - |
| TK2-WEB-04 | Routes | URL /lookup reaches reference lookup screen and returns HTML. | H HTTP UI | TK2-WEB-01 | S/E | W01 | - |
| TK2-WEB-05 | Routes | Other required screens/states are reachable through the UI. | H UI | TK2-WEB-01 | E | W01,W02 | - |
| TK2-WEB-06 | §2; Product | Browser runtime assets are bundled and required flows work without external services. | H DEP UI | TK1-RUN-04,TK1-RUN-05 | S/E | W01,W17 | - |
| TK2-AUI-01 | Signup/login | Signup email input exposes signup-email. | M UI | TK2-WEB-02 | E | W02 | - |
| TK2-AUI-02 | Signup/login | Signup password input exposes signup-password. | M UI | TK2-WEB-02 | E | W02 | - |
| TK2-AUI-03 | Signup/login | Signup display-name input exposes signup-display-name. | M UI | TK2-WEB-02 | E | W02 | - |
| TK2-AUI-04 | Signup/login | Signup submit button exposes signup-submit and performs signup. | H UI AU | TK1-AUTH-01 | E | W02 | - |
| TK2-AUI-05 | Signup/login | Login email input exposes login-email. | M UI | TK2-WEB-03 | E | W02 | - |
| TK2-AUI-06 | Signup/login | Login password input exposes login-password. | M UI | TK2-WEB-03 | E | W02 | - |
| TK2-AUI-07 | Signup/login | Login submit button exposes login-submit and performs login. | H UI AU | TK1-AUTH-05 | E | W02 | B |
| TK2-AUI-08 | Signup/login | auth-error is present only when an authentication error exists. | H UI AU | TK2-AUI-04,TK2-AUI-07 | E | W02 | - |
| TK2-AUI-09 | Signup/login | Signed-in user has visible current-user on every screen. | H UI AU | TK2-AUI-07 | E | W02,W18 | B |
| TK2-AUI-10 | Signup/login | current-user text contains the signed-in user's display name. | H UI AU | TK2-AUI-09 | E | W02,W18 | B |
| TK2-AUI-11 | Signup/login | Expose a working logout button with logout-button. | H UI AU | TK2-AUI-09 | E | W02 | - |
| TK2-SEARCH-01 | Search | restaurant-select selects a restaurant using restaurant IDs as option values. | H UI ST | TK1-BROWSE-01 | E | W03 | - |
| TK2-SEARCH-02 | Search | date-input represents a date with YYYY-MM-DD value. | H UI TM | TK1-AV-02 | E | W03 | - |
| TK2-SEARCH-03 | Search | party-size-input is a number input. | M UI VA | TK1-ERR-06 | E | W03 | - |
| TK2-SEARCH-04 | Search | search-button runs the availability search for the selected inputs. | H UI | TK1-AV-01 | E | W03,W04 | - |
| TK2-SEARCH-05 | Search | Results grid exposes availability-grid. | M UI | TK2-SEARCH-04 | E | W03 | - |
| TK2-SEARCH-06 | Search | Show one single-table cell for every restaurant table and returned slot. | H UI OR | TK1-BROWSE-02,TK1-AV-04 | E | W03,W14 | - |
| TK2-SEARCH-07 | Search | Single cell testid is slot-{table_id}-{HH:MM} using that slot's local time. | H UI TM | TK1-AV-05 | E | W03,W14 | - |
| TK2-SEARCH-08 | Search | Single cell data-available is exactly true iff table_id is in that slot's available_table_ids for the searched party; false otherwise. | C UI VA | TK1-AV-08,TK2-SEARCH-04 | E | W03,W04,W14 | - |
| TK2-SEARCH-09 | Search | Clicking an available single cell opens booking form for that table/slot. | H UI | TK2-SEARCH-08 | E | W03,W05 | - |
| TK2-SEARCH-10 | Search | Clicking an unavailable single cell does nothing. | H UI | TK2-SEARCH-08 | E | W03 | - |
| TK2-SEARCH-11 | Search | Signed-out available-cell click shows auth-error or navigates to /login; it does not book. | C UI AU | TK1-AUTH-11,TK2-SEARCH-09 | E | W02,W03 | - |
| TK2-SEARCH-12 | Search | When the day has no slots, show no-slots instead of the grid. | H UI TM | TK1-AV-11 | E | W03 | - |

### Out-of-order browser responses

| ID | Source | Atomic requirement | Risk/tags | Dependencies | Owner | Verify | Compat |
|---|---|---|---|---|---|---|---|
| TK2-RACE-01 | Competing clients | If A starts before B but completes after B, the grid describes B. | C UI OR | TK2-SEARCH-04 | E | W04 | - |
| TK2-RACE-02 | Competing clients | Under the same race, table labels describe B. | C UI OR | TK2-RACE-01,TK1-BROWSE-02 | E | W04 | - |
| TK2-RACE-03 | Competing clients | Under the same race, the booking form describes B. | C UI OR | TK2-RACE-01,TK2-SEARCH-09 | E | W04 | - |
| TK2-RACE-04 | Competing clients | A late search response must not restore A's results. | C UI OR | TK2-RACE-01 | E | W04 | - |
| TK2-RACE-05 | Competing clients; Product | Detail/label responses used to render B must remain associated with B's restaurant rather than a stale restaurant request. | C UI ST OR | TK2-RACE-02 | E | W04 | - |
| TK2-RACE-06 | Competing clients; Booking form | Selection/form updates retain the active table/slot context when dependent detail/availability responses finish out of order. | H UI OR | TK2-RACE-03 | E | W04,W06 | - |

RACE-05/06 are decompositions of the required coherent B labels/form and selected-form behavior, not demands for a particular fetch/cancellation architecture. They cover search/detail/selection response races even when requests are separate. A synchronous implementation can satisfy them without adding requests.

### Booking confirmation conflict and uncertain success

| ID | Source | Atomic requirement | Risk/tags | Dependencies | Owner | Verify | Compat |
|---|---|---|---|---|---|---|---|
| TK2-BOOK-01 | Booking form | Booking form container exposes booking-form. | M UI | TK2-SEARCH-09 | E | W05 | B |
| TK2-BOOK-02 | Booking form; combined UI | booking-summary names every selected table using its label. | H UI ST | TK1-BROWSE-02 | E | W05,W14 | B |
| TK2-BOOK-03 | Booking form | booking-summary includes the local start time. | H UI TM | TK1-AV-05 | E | W05,W14 | B |
| TK2-BOOK-04 | Booking form | booking-party-size is a number input prefilled from the completed search's party size. | H UI VA | TK2-SEARCH-04 | E | W05,W04 | B |
| TK2-BOOK-05 | Booking form | booking-submit submits the selected form through the authenticated reservation API. | C UI AU RP | TK1-CREATE-01,TK1-IDEM-01 | E | W05,W07 | B |
| TK2-BOOK-06 | Booking form | Keep the booking form on screen after success. | H UI | TK2-BOOK-05 | E | W05 | B |
| TK2-BOOK-07 | Booking form | Resubmitting an unchanged successful form yields the same confirmation-reference. | C UI RP | TK1-IDEM-08,TK2-BOOK-06 | E | W05,W07 | R/B |
| TK2-BOOK-08 | Booking form | Unchanged successful resubmission creates no additional booking. | C UI RP TX | TK2-BOOK-07 | S/E | W05,W07 | R/B |
| TK2-BOOK-09 | Booking form | Unchanged successful resubmission has no booking-error. | H UI RP | TK2-BOOK-07 | E | W05 | - |
| TK2-BOOK-10 | Booking form | Changing a form field makes the next submission a new booking request. | C UI RP | TK1-IDEM-10,TK2-BOOK-05 | E | W05,W07 | - |
| TK2-CONF-01 | Confirmation | Successful booking shows confirmation. | H UI | TK2-BOOK-05 | E | W05,W07 | - |
| TK2-CONF-02 | Confirmation | confirmation-reference text is exactly the reference without surrounding words. | H UI ST | TK2-CONF-01 | E | W05,W18 | R/B |
| TK2-CONF-03 | Confirmation | confirmation-details contains restaurant name. | H UI ST | TK2-CONF-01 | E | W05,W14 | - |
| TK2-CONF-04 | Confirmation | confirmation-details contains table label and local start time. | H UI TM | TK2-CONF-01 | E | W05,W14 | - |
| TK2-CONF-05 | Combined UI | confirmation-tables contains every reserved table label. | H UI ST | TK2-CONF-01 | E | W14 | - |
| TK2-CONFLICT-01 | Competing clients | A confirmed 409 table_unavailable shows booking-error. | H UI HTTP | TK1-CREATE-07 | E | W06 | - |
| TK2-CONFLICT-02 | Competing clients | That conflict refreshes availability from the server. | H UI ST | TK2-CONFLICT-01 | E | W06,W04 | - |
| TK2-CONFLICT-03 | Competing clients | Preserve the selected form on screen after conflict. | C UI ST | TK2-CONFLICT-01 | E | W06 | - |
| TK2-CONFLICT-04 | Competing clients | Preserve that form's inputs after conflict. | C UI ST | TK2-CONFLICT-03 | E | W06 | - |
| TK2-CONFLICT-05 | Competing clients | Allow the diner to change selection after conflict. | H UI | TK2-CONFLICT-04 | E | W06 | - |
| TK2-CONFLICT-06 | Competing clients | Do not show a confirmation for the rejected attempt. | C UI ST | TK2-CONFLICT-01 | E | W06 | - |
| TK2-UNCERTAIN-01 | Competing clients | Lost booking response, including after commit, shows nonempty booking-uncertain text. | C UI RP | TK2-BOOK-05 | E | W07,W18 | B |
| TK2-UNCERTAIN-02 | Competing clients | Lost response does not show booking-error. | H UI OR | TK2-UNCERTAIN-01 | E | W07 | - |
| TK2-UNCERTAIN-03 | Competing clients | Lost response does not show a new confirmation. | C UI ST | TK2-UNCERTAIN-01 | E | W07 | - |
| TK2-UNCERTAIN-04 | Competing clients | Unchanged uncertain form retries with exactly the same idempotency key. | C UI RP | TK1-IDEM-08,TK2-UNCERTAIN-01 | E | W07,W18 | R/B |
| TK2-UNCERTAIN-05 | Competing clients | Unchanged uncertain form retries with exactly the same body. | C UI RP | TK1-IDEM-11,TK2-UNCERTAIN-01 | E | W07,W18 | R/B |
| TK2-UNCERTAIN-06 | Competing clients | Successful retry removes booking-uncertain elements. | H UI RP | TK2-UNCERTAIN-04 | E | W07,W18 | - |
| TK2-UNCERTAIN-07 | Competing clients | Successful retry removes booking-error elements. | H UI RP | TK2-UNCERTAIN-04 | E | W07,W18 | - |
| TK2-UNCERTAIN-08 | Competing clients | Successful retry displays the original reference. | C UI RP ST | TK1-IDEM-13 | E | W07,W18 | R/B |
| TK2-UNCERTAIN-09 | Competing clients | A confirmed rejection uses booking-error. | H UI HTTP | TK1-ERR-01 | E | W06,W07 | - |
| TK2-UNCERTAIN-10 | Competing clients | Browser must not manufacture success from cached data; server response remains authoritative. | C UI RP ST | TK2-CONF-01 | E | W07,W18 | - |
| TK2-UNCERTAIN-11 | Competing clients; combined UI | Conflict and uncertain-response recovery rules also apply to pair bookings. | C UI RP TX | TK2-CONFLICT-01,TK2-UNCERTAIN-01 | S/E | W06,W07,W14,W18 | R/B |

### Lookup and product quality

| ID | Source | Atomic requirement | Risk/tags | Dependencies | Owner | Verify | Compat |
|---|---|---|---|---|---|---|---|
| TK2-LOOKUP-01 | Lookup | Expose lookup-reference-input and lookup-submit to look up a reference. | H UI AU | TK2-WEB-04,TK1-GET-04 | E | W08,W18 | B |
| TK2-LOOKUP-02 | Lookup | Found record shows reservation-detail. | H UI | TK2-LOOKUP-01 | E | W08 | - |
| TK2-LOOKUP-03 | Lookup | reservation-status text is exactly confirmed or cancelled. | H UI ST | TK2-LOOKUP-02 | E | W08,W18 | S/B |
| TK2-LOOKUP-04 | Lookup | reservation-cancel-button cancels an eligible confirmed booking. | H UI TX | TK1-CANCEL-01 | E | W08,W14 | - |
| TK2-LOOKUP-05 | Lookup | Cancel button is absent once cancelled. | H UI ST | TK2-LOOKUP-04 | E | W08 | - |
| TK2-LOOKUP-06 | Lookup | Unknown/nonvisible lookup shows reservation-error. | C UI AU | TK1-GET-04 | E | W08 | - |
| TK2-LOOKUP-07 | Lookup | Refused cancellation shows reservation-error. | H UI TM | TK1-CANCEL-04 | E | W08 | - |
| TK2-LOOKUP-08 | Combined UI | reservation-tables contains every member table label. | H UI ST | TK2-LOOKUP-02 | E | W08,W14,W18 | - |
| TK2-LOOKUP-09 | Combined UI | Single-table cell/confirmation/lookup behavior remains compatible with the original single selection flow. | H UI ST | TK2-SEARCH-07,TK2-CONF-04,TK2-LOOKUP-02 | E | W05,W08,W14 | B |
| TK2-QA-01 | Product | Required browser flows form a coherent presentation-ready restaurant product. | H QA UI | TK2-WEB-05 | E | W17 | - |
| TK2-QA-02 | Product | Visual direction expresses a warm confident hospitality character. | M QA | TK2-QA-01 | E | W17 | - |
| TK2-QA-03 | Product | Search/availability/booking hierarchy makes dates/times/party/seating easy to scan. | H QA UI | TK2-SEARCH-05,TK2-BOOK-01 | E | W17 | - |
| TK2-QA-04 | Product | Typography/spacing/colour/controls/feedback use a consistent visual system. | M QA | TK2-QA-01 | E | W17 | - |
| TK2-QA-05 | Product | Primary actions are easy to identify. | H QA UI | TK2-QA-03 | E | W17 | - |
| TK2-QA-06 | Product | Available/unavailable/selected states are visually distinct. | H QA UI | TK2-SEARCH-08 | E | W17 | - |
| TK2-QA-07 | Product | Loading/success/refused/uncertain states are visually distinct. | H QA UI | TK2-UNCERTAIN-01,TK2-CONFLICT-01 | E | W17 | - |
| TK2-QA-08 | Product | Human-readable restaurant/table labels are prominent. | H QA UI | TK1-BROWSE-02 | E | W17 | - |
| TK2-QA-09 | Product | Combined seating reads as an intentional seating option rather than raw concatenated technical identifiers. | H QA UI | TK2-BOOK-02 | E | W14,W17 | - |
| TK2-QA-10 | Product | Technical identifiers are exposed only where they help the diner. | M QA UI | TK2-QA-08 | E | W17 | - |
| TK2-QA-11 | Product | Required flows are clear/usable at 375 CSS-pixel viewport width. | H QA UI | TK2-WEB-05 | E | W17 | - |
| TK2-QA-12 | Product | Required flows are clear/usable at conventional desktop widths. | H QA UI | TK2-WEB-05 | E | W17 | - |
| TK2-QA-13 | Product | Neither viewport has horizontal page scrolling. | H QA UI | TK2-QA-11,TK2-QA-12 | E | W17 | - |
| TK2-QA-14 | Product | Inputs have visible labels. | H QA UI | TK2-WEB-05 | E | W17 | - |
| TK2-QA-15 | Product | Keyboard focus is apparent. | H QA UI | TK2-WEB-05 | E | W17 | - |
| TK2-QA-16 | Product | Text and controls have sufficient contrast. | H QA UI | TK2-QA-04 | E | W17 | - |
| TK2-QA-17 | Product | Empty states are considered and readable. | H QA UI | TK2-SEARCH-12 | E | W03,W17 | - |
| TK2-QA-18 | Product | Loading states are considered and readable. | H QA UI | TK2-SEARCH-04 | E | W04,W17 | - |
| TK2-QA-19 | Product | Error states are considered and readable. | H QA UI | TK2-CONFLICT-01,TK2-LOOKUP-06 | E | W06,W08,W17 | - |
| TK2-QA-20 | Product | Navigation remains consistent across required routes. | H QA UI | TK2-WEB-01,TK2-WEB-02,TK2-WEB-03,TK2-WEB-04 | E | W01,W17 | - |

### Combined model selection capacity and occupancy

| ID | Source | Atomic requirement | Risk/tags | Dependencies | Owner | Verify | Compat |
|---|---|---|---|---|---|---|---|
| TK2-PAIR-01 | Model | Restaurant fixture supports combinable declared table-ID pairs. | H ST VA | TK1-FIX-02 | S | W09 | S |
| TK2-PAIR-02 | Model | Each combinable entry is an unordered pair of member IDs in that restaurant. | H ST VA | TK2-PAIR-01 | S | W09,W10 | S |
| TK2-PAIR-03 | Model | A pair not declared cannot be combined even if capacities fit. | C VA ST | TK2-PAIR-01 | S | W10 | S |
| TK2-PAIR-04 | Model | Combinability is not transitive. | C VA ST | TK2-PAIR-03 | S | W09,W10 | S |
| TK2-PAIR-05 | Model | Only two-table combinations are supported; more than two returns 422 combination_not_allowed. | H VA OR | TK2-PAIR-01 | S | W10,W12,W13 | - |
| TK2-PAIR-06 | Model + Stage 3 | Combination capacity is the sum of the selected policy's member capacities. | H VA ST | TK1-FIX-12 | S | W09,W10 | S |
| TK2-PAIR-07 | Combined tables | Booking a pair occupies both members for its full absolute duration. | C TX TM CC | TK1-OCC-02,TK1-TIME-05 | S | W10,W15,W16 | S |
| TK2-PAIR-08 | API | Any member's overlapping confirmed occupancy gives 409 table_unavailable. | C TX CC | TK2-PAIR-07 | S | W10,W12,W13,W16 | - |
| TK2-PAIR-09 | API | Party above summed pair capacity gives 422 party_exceeds_capacity. | H VA | TK2-PAIR-06,TK1-ERR-06 | S | W10,W12,W13 | - |
| TK2-PAIR-10 | Model | Seeded bookings default to confirmed. | H ST | TK1-FIX-14 | S | W09 | S |
| TK2-PAIR-11 | Model | Seeded explicit cancelled bookings remain cancelled and do not occupy members. | C ST TX | TK1-FIX-14,TK1-AV-08 | S | W09 | S |
| TK2-PAIR-12 | Model | Seeded reservations accept legacy table_id or table_ids. | H ST VA | TK1-FIX-14 | S | W09 | S |
| TK2-SELECT-01 | API | Creation accepts table_ids to select a single or approved pair. | H HTTP VA | TK1-CREATE-01,TK2-PAIR-01 | S | W10 | S |
| TK2-SELECT-02 | API | Legacy table_id remains accepted and means one member. | C HTTP ST | TK1-CREATE-01 | S | W10,W18 | S |
| TK2-SELECT-03 | API | Sending both table_id and table_ids gives 422 validation_failed. | H VA OR | TK2-SELECT-01,TK2-SELECT-02 | S | W10,W12,W13 | - |
| TK2-SELECT-04 | API | Duplicate member ID gives 422 validation_failed. | H VA | TK2-SELECT-01 | S | W10,W12,W13 | - |
| TK2-SELECT-05 | API | Pair membership matching is unordered. | H VA OR | TK2-PAIR-02 | S | W10,W12,W13 | S |
| TK2-SELECT-06 | API + Stage 3 | New/current reservation responses expose table_ids plus revision/accepted_terms; historical original receipt shapes remain exact. | H HTTP ST | TK2-SELECT-01 | S | W10,W12,W13,W18 | S |
| TK2-SELECT-07 | API | A one-member response also carries table_id. | C HTTP ST | TK2-SELECT-06 | S | W10,W18 | S |
| TK2-SELECT-08 | API | A multi-member response omits table_id. | H HTTP ST | TK2-SELECT-06 | S | W10,W12,W13 | S |
| TK2-SELECT-09 | API | PATCH accepts table_ids under the same create selection rules. | C TX VA | TK1-PATCH-03,TK2-SELECT-01 | S | W12 | S |
| TK2-SELECT-10 | API | Cancellation frees every table in the selection. | C TX CC | TK1-CANCEL-02,TK2-PAIR-07 | S | W12,W16 | S |
| TK2-SELECT-11 | Combined UI/moves | Each atomic move accepts table_ids under the ordinary selection rules. | C TX VA RP | TK1-MOVE-06,TK2-SELECT-01 | S | W13 | S |
| TK2-SELECT-12 | Combined UI/moves | No member table belongs to overlapping resulting bookings. | C TX CC | TK1-MOVE-14,TK2-PAIR-07 | S | W13,W16 | S |
| TK2-SELECT-13 | API; §8 | Unknown table/member or a member absent from the selected restaurant gives 404 not_found. | H HTTP ST | TK1-CREATE-12,TK1-CREATE-13 | S | W10,W12,W13 | - |
| TK2-SELECT-14 | API; §5 | Wrong table_ids array/member JSON types use 400 malformed_request under ordinary type rules. | H VA OR | TK1-ERR-03 | S | W10,W12,W13 | - |

### Availability options and combination cells

| ID | Source | Atomic requirement | Risk/tags | Dependencies | Owner | Verify | Compat |
|---|---|---|---|---|---|---|---|
| TK2-OPTIONS-01 | Availability API | Slots gain available_options. | H HTTP ST | TK1-AV-03 | S | W11 | - |
| TK2-OPTIONS-02 | Availability API | available_table_ids retains its Stage 1 single-table-only meaning. | C HTTP ST | TK1-AV-06,TK1-AV-07,TK1-AV-08 | S | W11,W18 | - |
| TK2-OPTIONS-03 | Availability API | available_options lists every eligible single and declared pair. | H HTTP VA | TK2-PAIR-01,TK2-SELECT-01 | S | W11 | - |
| TK2-OPTIONS-04 | Availability API + Stage 3 | Each option contains table_ids and capacity summed from date-selected policy. | H HTTP VA | TK2-PAIR-06,TK2-OPTIONS-03 | S | W11 | - |
| TK2-OPTIONS-05 | Availability API | Options require capacity >= queried party_size. | H VA | TK2-OPTIONS-04 | S | W11 | - |
| TK2-OPTIONS-06 | Availability API | Options require no overlapping confirmed occupancy on any member. | C TX HTTP | TK2-PAIR-07,TK1-AV-08 | S | W11,W16 | - |
| TK2-OPTIONS-07 | Availability API | Singles precede pairs, with singles in fixture order. | H OR ST | TK2-OPTIONS-03 | S | W11,W18 | S |
| TK2-OPTIONS-08 | Availability API | Pairs appear in combinable declaration order. | H OR ST | TK2-OPTIONS-03 | S | W11,W18 | S |
| TK2-OPTIONS-09 | Availability API | Member order inside pair options is the combinable declaration order. | H OR ST | TK2-PAIR-02,TK2-OPTIONS-08 | S | W11,W14,W18 | S |
| TK2-PUI-01 | Combined UI | Available declared pairs for searched party size have combination grid cells. | H UI VA | TK2-OPTIONS-03,TK2-OPTIONS-05,TK2-OPTIONS-06 | E | W14 | - |
| TK2-PUI-02 | Combined UI | Combination testid is slot-{t_a}+{t_b}-{HH:MM}, with IDs in combinable order. | H UI OR | TK2-OPTIONS-09 | E | W14 | - |
| TK2-PUI-03 | Combined UI | Combination cell data-available reflects server option availability as for singles. | C UI VA | TK2-OPTIONS-06,TK2-SEARCH-08 | E | W14,W04 | - |
| TK2-PUI-04 | Combined UI | Available combination selection opens a form for both members at the chosen slot. | H UI ST | TK2-PUI-01,TK2-BOOK-02 | E | W14,W05 | - |
| TK2-PUI-05 | Combined UI | Combo confirmation and lookup display every member label without changing single-table behavior. | H UI ST | TK2-CONF-05,TK2-LOOKUP-08,TK2-LOOKUP-09 | E | W14,W18 | - |

### Upgrade and serialization

| ID | Source | Atomic requirement | Risk/tags | Dependencies | Owner | Verify | Compat |
|---|---|---|---|---|---|---|---|
| TK2-UP-01 | Existing clients + Stage 3 | Current service accepts unchanged exports from the same team's Stage 1 service, retaining cumulative legacy compatibility. | C ST TX | TK1-XFER-04,TK1-XFER-06 | S | W18 | S/R |
| TK2-UP-02 | Existing clients | Browser signed in before export/import remains signed in after upgrade. | C AU UI ST | TK1-XFER-13,TK2-AUI-09 | S/E | W18 | B |
| TK2-UP-03 | Existing clients | Retained booking reference works through /lookup after upgrade. | C UI ST AU | TK1-XFER-15,TK2-LOOKUP-01 | S/E | W18 | B |
| TK2-UP-04 | Existing clients | Booking whose response was lost before export remains retryable after import with the same body/key. | C RP UI ST | TK1-XFER-17,TK2-UNCERTAIN-04,TK2-UNCERTAIN-05 | S/E | W18 | R/B |
| TK2-UP-05 | Existing clients | UI recovers the original confirmation from that retry. | C RP UI ST | TK2-UP-04,TK2-UNCERTAIN-08 | S/E | W18 | R/B |
| TK2-UP-06 | Existing clients | Upgrade recovery requires no page reload. | C UI ST | TK2-UP-02,TK2-UP-05 | S/E | W18 | B |
| TK2-UP-07 | Existing clients | Upgrade recovery requires no new screen. | H UI ST | TK2-UP-05 | E | W18 | B |
| TK2-UP-08 | Existing clients | Selected form survives the between-request upgrade. | C UI ST | TK2-BOOK-01,TK2-UP-01 | E | W18 | B |
| TK2-UP-09 | Existing clients | Pending retry identity survives the between-request upgrade. | C UI RP ST | TK2-UP-04 | E | W18 | R/B |
| TK2-UP-10 | §10; Combined UI | Stage 2 own exports preserve pair configuration, pair records/member sets and successful create/batch receipts. | C ST RP TX | TK1-XFER-14,TK1-XFER-17,TK2-PAIR-07 | S | W19 | S/R |
| TK2-UP-11 | §10; Existing clients + Stage 3 | Stage 1 legacy request/receipt formats continue to work after current-service import. | C HTTP RP ST | TK2-UP-01,TK2-SELECT-02,TK1-IDEM-08 | S/E | W18 | S/R/B |
| TK2-CC-01 | Concurrent bookings/amendments | Concurrent requests yield results equivalent to some one-at-a-time order. | C CC TX | TK1-OCC-03,TK1-MOVE-17,TK2-PAIR-07 | S | W16,W19 | S/R |
| TK2-CC-02 | Concurrent bookings/amendments | All stated requirements hold at every read during concurrent writes. | C CC TX ST | TK2-CC-01 | S | W16,W19 | S/R |
| TK2-GATE-01 | Assignment | Stage 2 production starts only after Stage 1 ACCEPT plus committed copied baseline. | C SC ST | - | C | W20 | - |
| TK2-GATE-02 | Assignment | Stage 2 evidence commit waits for verifier's announced window completion. | H SC | - | C | W20 | - |

## New Stage 3 atomic requirements

### TK3-EXPL: Availability explanations

| ID | Source | Atomic requirement | Risk/tags | Dependencies | Owner | Verify | Compat |
|---|---|---|---|---|---|---|---|
| TK3-EXPL-01 | Stage 3 Availability explanations | Optional explain accepts only literal query value true; every other supplied value, including empty, false and 1, returns 422 validation_failed. | H VA HTTP | TK1-ERR-05 | S | Z01,Z02 | S/H |
| TK3-EXPL-02 | Stage 3 Availability explanations | Omitted explain adds no explanation fields; cumulative Stage 2 available_options remains present. | H HTTP ST | TK2-OPTIONS-01 | S | Z01,Z02 | S/H |
| TK3-EXPL-03 | Stage 3 Availability explanations | Capacity rule independently evaluates party_size against the selected policy capacity for that single table. | H VA HT | TK3-POL-11 | S | Z01,Z02 | S/H |
| TK3-EXPL-04 | Stage 3 Availability explanations | No_overlap independently evaluates every confirmed reservation using the candidate selected-policy interval against retained existing occupancy. | C TX TM HT | TK1-OCC-01,TK3-TERMS-09 | S | Z01,Z02 | S/H |
| TK3-EXPL-05 | Stage 3 Availability explanations | A table is available if and only if both capacity and no_overlap hold. | C TX VA | TK3-EXPL-03,TK3-EXPL-04 | S | Z01,Z02 | S/H |
| TK3-EXPL-06 | Stage 3 Availability explanations | With explain=true each slot has explain entries for every restaurant table exactly once. | H HTTP OR | TK3-EXPL-01 | S | Z01,Z02 | S/H |
| TK3-EXPL-07 | Stage 3 Availability explanations | Explanation entries use fixture table order, including unavailable tables. | H OR | TK3-EXPL-06 | S | Z01,Z02 | S/H |
| TK3-EXPL-08 | Stage 3 Availability explanations | Each explanation identifies table_id and selected policy_version. | H HT HTTP | TK3-POL-11 | S | Z01,Z02 | S/H |
| TK3-EXPL-09 | Stage 3 Availability explanations | Every table explanation reports both capacity and no_overlap rules without short-circuit omission. | H VA HTTP | TK3-EXPL-03,TK3-EXPL-04 | S | Z01,Z02 | S/H |
| TK3-EXPL-10 | Stage 3 Availability explanations | Rules appear in capacity then no_overlap order. | H OR | TK3-EXPL-09 | S | Z01,Z02 | S/H |
| TK3-EXPL-11 | Stage 3 Availability explanations | Each holds boolean reports the actual truth of its independent rule, including both false together. | H VA HTTP | TK3-EXPL-09 | S | Z01,Z02 | S/H |
| TK3-EXPL-12 | Stage 3 Availability explanations | Each available boolean equals the conjunction of its rule truths. | H HTTP | TK3-EXPL-11 | S | Z01,Z02 | S/H |
| TK3-EXPL-13 | Stage 3 Availability explanations | True explanation table IDs exactly equal available_table_ids in the same order. | C OR HTTP | TK3-EXPL-12,TK1-AV-09 | S | Z01,Z02 | S/H |
| TK3-EXPL-14 | Stage 3 Availability explanations | A closed day still returns slots:[] when explanations are requested. | H TM | TK1-AV-11 | S | Z01,Z02 | S/H |
| TK3-EXPL-15 | Stage 3 Availability explanations | A fitting slot with no available tables remains present with complete explanations. | H HTTP | TK3-EXPL-06,TK1-AV-10 | S | Z01,Z02 | S/H |

### TK3-MGR: Policies and accepted terms: permissions

| ID | Source | Atomic requirement | Risk/tags | Dependencies | Owner | Verify | Compat |
|---|---|---|---|---|---|---|---|
| TK3-MGR-01 | Stage 3 Policies and accepted terms: permissions | Reset fixtures accept optional manager_user_ids on each restaurant. | H VA ST | TK1-FIX-01 | S | Z03 | S |
| TK3-MGR-02 | Stage 3 Policies and accepted terms: permissions | Missing manager_user_ids defaults to an empty list. | H AU ST | TK3-MGR-01 | S | Z03 | S |
| TK3-MGR-03 | Stage 3 Policies and accepted terms: permissions | Only a restaurant's named managers may publish its policies. | C AU | TK3-MGR-01 | S | Z03 | S |
| TK3-MGR-04 | Stage 3 Policies and accepted terms: permissions | Authenticated non-manager policy publication returns 403 forbidden. | H AU HTTP | TK3-MGR-03 | S | Z03 | S |
| TK3-MGR-05 | Stage 3 Policies and accepted terms: permissions | Policy publication for an unknown restaurant returns 404 not_found. | H HTTP | TK1-ERR-12 | S | Z03 | S |
| TK3-MGR-06 | Stage 3 Policies and accepted terms: permissions | Policy publication with no token returns 401 unauthenticated. | H AU HTTP | TK1-AUTH-11 | S | Z03 | S |
| TK3-MGR-07 | Stage 3 Policies and accepted terms: permissions | Manager permission does not confer access to another diner's private reservation lookup. | C AU | TK1-GET-04 | S | Z03 | S |
| TK3-MGR-08 | Stage 3 Policies and accepted terms: permissions | Manager permission does not confer access to another diner's history. | C AU | TK3-HIST-02 | S | Z03 | S |

### TK3-POL: Policies and accepted terms: publication selection and validation

| ID | Source | Atomic requirement | Risk/tags | Dependencies | Owner | Verify | Compat |
|---|---|---|---|---|---|---|---|
| TK3-POL-01 | Stage 3 Policies and accepted terms: publication selection and validation | POST /restaurants/{id}/policies requires an idempotency key and all Stage 1 replay rules. | C RP | TK1-IDEM-01,TK3-MGR-03 | S | Z03,Z04,Z05 | S/R/H |
| TK3-POL-02 | Stage 3 Policies and accepted terms: publication selection and validation | Policy publication accepts a complete policy rather than merging a partial patch. | H VA ST | TK3-POL-01 | S | Z03,Z04,Z05 | S/R/H |
| TK3-POL-03 | Stage 3 Policies and accepted terms: publication selection and validation | Success returns 201 with supplied recognized policy fields plus integer policy_version. | H HTTP | TK3-POL-02 | S | Z03,Z04,Z05 | S/R/H |
| TK3-POL-04 | Stage 3 Policies and accepted terms: publication selection and validation | Publication versions begin at 1 separately for each restaurant. | H OR HT | TK3-POL-03 | S | Z03,Z04,Z05 | S/R/H |
| TK3-POL-05 | Stage 3 Policies and accepted terms: publication selection and validation | Each successful new publication increases that restaurant's policy_version sequence by exactly one. | C CC HT | TK3-POL-04 | S | Z03,Z04,Z05 | S/R/H |
| TK3-POL-06 | Stage 3 Policies and accepted terms: publication selection and validation | Failed policy writes allocate no version and change no state. | C TX RP HT | TK3-POL-02 | S | Z03,Z04,Z05 | S/R/H |
| TK3-POL-07 | Stage 3 Policies and accepted terms: publication selection and validation | Policy replays allocate no version and make no further changes. | C RP HT | TK1-IDEM-14,TK3-POL-05 | S | Z03,Z04,Z05 | S/R/H |
| TK3-POL-08 | Stage 3 Policies and accepted terms: publication selection and validation | Published policy records are immutable. | C HT ST | TK3-POL-03 | S | Z03,Z04,Z05 | S/R/H |
| TK3-POL-09 | Stage 3 Policies and accepted terms: publication selection and validation | Policy 0 is the restaurant's original fixture rules. | H HT | TK1-FIX-01 | S | Z03,Z04,Z05 | S/R/H |
| TK3-POL-10 | Stage 3 Policies and accepted terms: publication selection and validation | Policy 0 supplies decisions when no published policy is effective for the local start date. | H HT TM | TK3-POL-09 | S | Z03,Z04,Z05 | S/R/H |
| TK3-POL-11 | Stage 3 Policies and accepted terms: publication selection and validation | For a booking local start date select the greatest effective_from not later than that date, independent of publication order. | C TM OR HT | TK3-POL-08 | S | Z03,Z04,Z05 | S/R/H |
| TK3-POL-12 | Stage 3 Policies and accepted terms: publication selection and validation | Among equal effective dates choose the greatest policy_version. | C OR HT | TK3-POL-11 | S | Z03,Z04,Z05 | S/R/H |
| TK3-POL-13 | Stage 3 Policies and accepted terms: publication selection and validation | A new same-date policy supersedes older ones only for future decisions. | C HT | TK3-POL-12,TK3-TERMS-09 | S | Z03,Z04,Z05 | S/R/H |
| TK3-POL-14 | Stage 3 Policies and accepted terms: publication selection and validation | Effective dates may be in the past. | H TM VA | TK1-FIX-16 | S | Z03,Z04,Z05 | S/R/H |
| TK3-POL-15 | Stage 3 Policies and accepted terms: publication selection and validation | Publication never retroactively edits accepted reservations. | C HT TX | TK3-POL-08 | S | Z03,Z04,Z05 | S/R/H |
| TK3-POL-16 | Stage 3 Policies and accepted terms: publication selection and validation | All six fields effective_from, slot_minutes, reservation_duration_minutes, cancellation_cutoff_minutes, opening_hours and capacities are required. | H VA | TK3-POL-02 | S | Z03,Z04,Z05 | S/R/H |
| TK3-POL-17 | Stage 3 Policies and accepted terms: publication selection and validation | effective_from must be an actual calendar date written YYYY-MM-DD. | H VA TM | TK3-POL-16 | S | Z03,Z04,Z05 | S/R/H |
| TK3-POL-18 | Stage 3 Policies and accepted terms: publication selection and validation | Published slot_minutes is an integer in 1..1440. | H VA TM | TK3-POL-16 | S | Z03,Z04,Z05 | S/R/H |
| TK3-POL-19 | Stage 3 Policies and accepted terms: publication selection and validation | Published reservation_duration_minutes is an integer in 1..1440. | H VA TM | TK3-POL-16 | S | Z03,Z04,Z05 | S/R/H |
| TK3-POL-20 | Stage 3 Policies and accepted terms: publication selection and validation | Published cancellation_cutoff_minutes is an integer in 0..10080. | H VA TM | TK3-POL-16 | S | Z03,Z04,Z05 | S/R/H |
| TK3-POL-21 | Stage 3 Policies and accepted terms: publication selection and validation | Booleans are invalid for numeric policy fields. | H VA | TK3-POL-18,TK3-POL-19,TK3-POL-20 | S | Z03,Z04,Z05 | S/R/H |
| TK3-POL-22 | Stage 3 Policies and accepted terms: publication selection and validation | Published opening_hours follows Stage 1 weekdays and same-day HH:MM opening/closing rules. | H VA TM | TK1-FIX-07,TK1-FIX-08 | S | Z03,Z04,Z05 | S/R/H |
| TK3-POL-23 | Stage 3 Policies and accepted terms: publication selection and validation | Published opening_hours contains no duplicate weekdays. | H VA | TK3-POL-22 | S | Z03,Z04,Z05 | S/R/H |
| TK3-POL-24 | Stage 3 Policies and accepted terms: publication selection and validation | capacities names exactly the restaurant's table IDs, without missing or additional IDs. | H VA ST | TK3-POL-16 | S | Z03,Z04,Z05 | S/R/H |
| TK3-POL-25 | Stage 3 Policies and accepted terms: publication selection and validation | Each published capacity is an integer in 1..100, excluding booleans. | H VA | TK3-POL-24 | S | Z03,Z04,Z05 | S/R/H |
| TK3-POL-26 | Stage 3 Policies and accepted terms: publication selection and validation | Invalid policy returns 422 validation_failed without version or state change; unparseable JSON retains 400 malformed_request. | C VA TX HTTP | TK3-POL-06,TK1-ERR-02 | S | Z03,Z04,Z05 | S/R/H |
| TK3-POL-27 | Stage 3 Policies and accepted terms: publication selection and validation | A policy cannot change table identities. | C HT ST | TK3-POL-24 | S | Z03,Z04,Z05 | S/R/H |
| TK3-POL-28 | Stage 3 Policies and accepted terms: publication selection and validation | A policy cannot change table labels. | H HT | TK3-POL-02 | S | Z03,Z04,Z05 | S/R/H |
| TK3-POL-29 | Stage 3 Policies and accepted terms: publication selection and validation | A policy cannot change restaurant timezone. | C TM HT | TK3-POL-02 | S | Z03,Z04,Z05 | S/R/H |
| TK3-POL-30 | Stage 3 Policies and accepted terms: publication selection and validation | A policy cannot change declared table combinations. | C HT ST | TK3-POL-02 | S | Z03,Z04,Z05 | S/R/H |
| TK3-POL-31 | Stage 3 Policies and accepted terms: publication selection and validation | Unknown policy request fields are ignored for effects, while included in full parsed-body receipt identity. | H VA RP | TK1-HTTP-03,TK1-IDEM-10,TK1-IDEM-11 | S | Z03,Z04,Z05 | S/R/H |
| TK3-POL-32 | Stage 3 Policies and accepted terms: publication selection and validation | GET /restaurants/{id}/policies is public and returns {policies:[...]}. | H AU HTTP | TK3-POL-08 | S | Z03,Z04,Z05 | S/R/H |
| TK3-POL-33 | Stage 3 Policies and accepted terms: publication selection and validation | Public policy list is in publication order. | H OR | TK3-POL-05,TK3-POL-32 | S | Z03,Z04,Z05 | S/R/H |
| TK3-POL-34 | Stage 3 Policies and accepted terms: publication selection and validation | Public policy list omits policy 0. | H HTTP | TK3-POL-09,TK3-POL-32 | S | Z03,Z04,Z05 | S/R/H |
| TK3-POL-35 | Stage 3 Policies and accepted terms: publication selection and validation | Ordinary restaurant detail retains original fixture configuration after publications. | H HT HTTP | TK1-BROWSE-02 | S | Z03,Z04,Z05 | S/R/H |
| TK3-POL-36 | Stage 3 Policies and accepted terms: publication selection and validation | Availability uses the policy selected for the searched local date. | C TM HT | TK3-POL-11,TK1-AV-04 | S | Z03,Z04,Z05 | S/R/H |
| TK3-POL-37 | Stage 3 Policies and accepted terms: publication selection and validation | New booking decisions use the policy selected for the requested local start date. | C TM HT | TK3-POL-11,TK1-CREATE-01 | S | Z03,Z04,Z05 | S/R/H |

### TK3-TERMS: Policies and accepted terms: snapshots

| ID | Source | Atomic requirement | Risk/tags | Dependencies | Owner | Verify | Compat |
|---|---|---|---|---|---|---|---|
| TK3-TERMS-01 | Stage 3 Policies and accepted terms: snapshots | Every new/current reservation response carries revision and accepted_terms; old successful original receipts are preserved verbatim. | C RP HT HTTP | TK1-CREATE-01,TK1-IDEM-12 | S | Z06,Z07,Z08 | S/R/H |
| TK3-TERMS-02 | Stage 3 Policies and accepted terms: snapshots | A newly created reservation begins at revision 1. | H HT | TK3-TERMS-01 | S | Z06,Z07,Z08 | S/R/H |
| TK3-TERMS-03 | Stage 3 Policies and accepted terms: snapshots | accepted_terms contains the entire selected policy snapshot, not only the chosen tables or weekday. | C HT ST | TK3-POL-11 | S | Z06,Z07,Z08 | S/R/H |
| TK3-TERMS-04 | Stage 3 Policies and accepted terms: snapshots | accepted_terms includes policy_version, slot_minutes, reservation_duration_minutes and cancellation_cutoff_minutes. | H HT HTTP | TK3-TERMS-03 | S | Z06,Z07,Z08 | S/R/H |
| TK3-TERMS-05 | Stage 3 Policies and accepted terms: snapshots | accepted_terms includes complete opening_hours and all table capacities. | H HT HTTP | TK3-TERMS-03 | S | Z06,Z07,Z08 | S/R/H |
| TK3-TERMS-06 | Stage 3 Policies and accepted terms: snapshots | accepted_terms excludes effective_from. | H HTTP | TK3-TERMS-03 | S | Z06,Z07,Z08 | S/R/H |
| TK3-TERMS-07 | Stage 3 Policies and accepted terms: snapshots | Seeded bookings begin at revision 1 under policy 0. | H HT ST | TK3-POL-09,TK1-FIX-15 | S | Z06,Z07,Z08 | S/R/H |
| TK3-TERMS-08 | Stage 3 Policies and accepted terms: snapshots | Successful old-key retries return original response revision/terms, or their original absence in an older-stage receipt. | C RP HT | TK1-IDEM-13 | S | Z06,Z07,Z08 | S/R/H |
| TK3-TERMS-09 | Stage 3 Policies and accepted terms: snapshots | Policy publication changes neither existing booking state nor accepted terms. | C HT TX | TK3-POL-15 | S | Z06,Z07,Z08 | S/R/H |
| TK3-TERMS-10 | Stage 3 Policies and accepted terms: snapshots | Policy publication does not change existing reservation end times. | C HT TM | TK3-TERMS-09 | S | Z06,Z07,Z08 | S/R/H |
| TK3-TERMS-11 | Stage 3 Policies and accepted terms: snapshots | Policy publication does not change existing histories. | C HT | TK3-TERMS-09 | S | Z06,Z07,Z08 | S/R/H |
| TK3-TERMS-12 | Stage 3 Policies and accepted terms: snapshots | Cancel uses the accepted cutoff measured against the booking's current start. | C TM HT | TK1-CANCEL-04 | S | Z06,Z07,Z08 | S/R/H |
| TK3-TERMS-13 | Stage 3 Policies and accepted terms: snapshots | A real amendment first checks the old accepted cutoff. | C OR TM | TK1-PATCH-04 | S | Z06,Z07,Z08 | S/R/H |
| TK3-TERMS-14 | Stage 3 Policies and accepted terms: snapshots | A real amendment validates all resulting fields against the policy applicable to the resulting local start date. | C TM VA HT | TK3-TERMS-13,TK3-POL-11 | S | Z06,Z07,Z08 | S/R/H |
| TK3-TERMS-15 | Stage 3 Policies and accepted terms: snapshots | A real amendment atomically replaces accepted_terms with the entire resulting selected policy. | C TX HT | TK3-TERMS-14 | S | Z06,Z07,Z08 | S/R/H |
| TK3-TERMS-16 | Stage 3 Policies and accepted terms: snapshots | A real amendment atomically recomputes end time using the newly accepted absolute duration. | C TX TM | TK3-TERMS-15,TK1-TIME-05 | S | Z06,Z07,Z08 | S/R/H |
| TK3-TERMS-17 | Stage 3 Policies and accepted terms: snapshots | A real amendment increments reservation revision exactly once. | C HT TX | TK3-TERMS-15 | S | Z06,Z07,Z08 | S/R/H |
| TK3-TERMS-18 | Stage 3 Policies and accepted terms: snapshots | A no-op retains accepted_terms, end time and revision, even if a newer policy would reject the old fields. | C HT TM | TK3-TERMS-09 | S | Z06,Z07,Z08 | S/R/H |
| TK3-TERMS-19 | Stage 3 Policies and accepted terms: snapshots | A no-op still requires a confirmed editable booking and accepted cutoff compliance. | H TM OR | TK3-TERMS-12 | S | Z06,Z07,Z08 | S/R/H |
| TK3-TERMS-20 | Stage 3 Policies and accepted terms: snapshots | A failed amendment changes no booking, occupancy, terms, end time, revision or history. | C TX HT | TK1-PATCH-07 | S | Z06,Z07,Z08 | S/R/H |

### TK3-REV: Policies and accepted terms: revision controls

| ID | Source | Atomic requirement | Risk/tags | Dependencies | Owner | Verify | Compat |
|---|---|---|---|---|---|---|---|
| TK3-REV-01 | Stage 3 Policies and accepted terms: revision controls | Cancellation increments reservation revision once on its first real success. | C HT TX | TK3-TERMS-12 | S | Z08,Z09 | S/H/R |
| TK3-REV-02 | Stage 3 Policies and accepted terms: revision controls | Repeated cancellation leaves revision unchanged. | C HT | TK1-CANCEL-03,TK3-REV-01 | S | Z08,Z09 | S/H/R |
| TK3-REV-03 | Stage 3 Policies and accepted terms: revision controls | PATCH accepts optional expected_revision. | H HTTP | TK1-PATCH-01 | S | Z08,Z09 | S/H/R |
| TK3-REV-04 | Stage 3 Policies and accepted terms: revision controls | expected_revision must be a positive integer; invalid type or range returns 422 validation_failed. | H VA HTTP | TK3-REV-03 | S | Z08,Z09 | S/H/R |
| TK3-REV-05 | Stage 3 Policies and accepted terms: revision controls | A valid expected_revision differing from the current revision returns 409 stale_revision. | C CC HT | TK3-REV-04 | S | Z08,Z09 | S/H/R |
| TK3-REV-06 | Stage 3 Policies and accepted terms: revision controls | Stale-revision detection precedes cutoff and proposed-change validation. | C OR CC | TK3-REV-05 | S | Z08,Z09 | S/H/R |
| TK3-REV-07 | Stage 3 Policies and accepted terms: revision controls | Omitting expected_revision retains ordinary Stage 1 amendment semantics as cumulatively extended. | H HTTP | TK1-PATCH-03 | S | Z08,Z09 | S/H/R |
| TK3-REV-08 | Stage 3 Policies and accepted terms: revision controls | At most one real change can succeed among concurrent amendments using the same expected revision. | C CC TX | TK3-REV-05,TK3-TERMS-17 | S | Z08,Z09 | S/H/R |
| TK3-REV-09 | Stage 3 Policies and accepted terms: revision controls | Unknown unrelated PATCH fields remain ignored. | H VA | TK1-HTTP-03 | S | Z08,Z09 | S/H/R |
| TK3-REV-10 | Stage 3 Policies and accepted terms: revision controls | No-op PATCH records no history entry. | C HT | TK3-TERMS-18 | S | Z08,Z09 | S/H/R |

### TK3-HIST: Reservation history and resulting snapshots

| ID | Source | Atomic requirement | Risk/tags | Dependencies | Owner | Verify | Compat |
|---|---|---|---|---|---|---|---|
| TK3-HIST-01 | Stage 3 Reservation history and resulting snapshots | GET /reservations/{reference}/history returns {reference,entries} for the reservation's own record. | H HTTP HT | TK1-GET-04 | S | Z07,Z10,Z11 | S/H |
| TK3-HIST-02 | Stage 3 Reservation history and resulting snapshots | Only the reservation owner may read its history. | C AU | TK1-GET-04 | S | Z07,Z10,Z11 | S/H |
| TK3-HIST-03 | Stage 3 Reservation history and resulting snapshots | Unknown, other-owner and anonymous history requests return the same 404 not_found. | C AU HTTP | TK3-HIST-02 | S | Z07,Z10,Z11 | S/H |
| TK3-HIST-04 | Stage 3 Reservation history and resulting snapshots | A cancelled reservation retains readable owner history. | H HT | TK1-CANCEL-01 | S | Z07,Z10,Z11 | S/H |
| TK3-HIST-05 | Stage 3 Reservation history and resulting snapshots | History seq begins at 1. | H OR HT | TK3-HIST-01 | S | Z07,Z10,Z11 | S/H |
| TK3-HIST-06 | Stage 3 Reservation history and resulting snapshots | Each new entry increments seq by exactly one without gaps. | C OR HT TX | TK3-HIST-05 | S | Z07,Z10,Z11 | S/H |
| TK3-HIST-07 | Stage 3 Reservation history and resulting snapshots | seq gives a total order even for writes in the same second. | H OR HT CC | TK3-HIST-06 | S | Z07,Z10,Z11 | S/H |
| TK3-HIST-08 | Stage 3 Reservation history and resulting snapshots | Entries are returned in seq order, also at order. | H OR TM | TK3-HIST-07 | S | Z07,Z10,Z11 | S/H |
| TK3-HIST-09 | Stage 3 Reservation history and resulting snapshots | Each native entry carries seq, RFC3339 at, event and changes. | H HTTP HT TM | TK1-HTTP-02 | S | Z07,Z10,Z11 | S/H |
| TK3-HIST-10 | Stage 3 Reservation history and resulting snapshots | Native single-table created event names table_id, starts_at_local and party_size in that order. | H OR HT | TK3-HIST-09 | S | Z07,Z10,Z11 | S/H |
| TK3-HIST-11 | Stage 3 Reservation history and resulting snapshots | Each created field has from:null and its created to value. | H HT | TK3-HIST-10 | S | Z07,Z10,Z11 | S/H |
| TK3-HIST-12 | Stage 3 Reservation history and resulting snapshots | Changed events name only fields whose values actually changed. | C HT | TK3-REV-10 | S | Z07,Z10,Z11 | S/H |
| TK3-HIST-13 | Stage 3 Reservation history and resulting snapshots | Changed field order is selection, starts_at_local, party_size. | H OR | TK3-HIST-12 | S | Z07,Z10,Z11 | S/H |
| TK3-HIST-14 | Stage 3 Reservation history and resulting snapshots | A changed selection uses table_id for single-to-single and table_ids if a pair is involved. | H HT | TK3-PAIRHIST-02,TK3-PAIRHIST-04 | S | Z07,Z10,Z11 | S/H |
| TK3-HIST-15 | Stage 3 Reservation history and resulting snapshots | Cancelled event carries empty changes. | H HT | TK3-REV-01 | S | Z07,Z10,Z11 | S/H |
| TK3-HIST-16 | Stage 3 Reservation history and resulting snapshots | Nothing follows a cancelled event in that reservation's history. | C HT | TK1-PATCH-05,TK1-CANCEL-03 | S | Z07,Z10,Z11 | S/H |
| TK3-HIST-17 | Stage 3 Reservation history and resulting snapshots | Successful create replay records no history. | C RP HT | TK1-IDEM-14 | S | Z07,Z10,Z11 | S/H |
| TK3-HIST-18 | Stage 3 Reservation history and resulting snapshots | Each history entry carries the reservation's resulting revision. | C HT | TK3-TERMS-17,TK3-REV-01 | S | Z07,Z10,Z11 | S/H |
| TK3-HIST-19 | Stage 3 Reservation history and resulting snapshots | Each history entry carries the complete resulting accepted_terms snapshot. | C HT ST | TK3-TERMS-03 | S | Z07,Z10,Z11 | S/H |
| TK3-HIST-20 | Stage 3 Reservation history and resulting snapshots | Old history entries never acquire newer policy terms. | C HT | TK3-HIST-19,TK3-TERMS-11 | S | Z07,Z10,Z11 | S/H |

### TK3-DEC: Policies and accepted terms: decision lookup

| ID | Source | Atomic requirement | Risk/tags | Dependencies | Owner | Verify | Compat |
|---|---|---|---|---|---|---|---|
| TK3-DEC-01 | Stage 3 Policies and accepted terms: decision lookup | GET /reservations/{reference}/decision returns reference, current revision and current accepted_terms. | H HTTP HT | TK3-TERMS-01 | S | Z10 | S/H |
| TK3-DEC-02 | Stage 3 Policies and accepted terms: decision lookup | Decision lookup works after cancellation. | H HT | TK3-DEC-01 | S | Z10 | S/H |
| TK3-DEC-03 | Stage 3 Policies and accepted terms: decision lookup | Only the reservation owner may read its decision. | C AU | TK1-GET-04 | S | Z10 | S/H |
| TK3-DEC-04 | Stage 3 Policies and accepted terms: decision lookup | Unknown or another owner's decision returns 404 not_found. | C AU HTTP | TK3-DEC-03 | S | Z10 | S/H |
| TK3-DEC-05 | Stage 3 Policies and accepted terms: decision lookup | Anonymous decision returns 404 not_found rather than general unauthenticated 401. | C AU HTTP | TK3-DEC-03 | S | Z10 | S/H |

### TK3-ADOPT: Recurring reservations: adoption

| ID | Source | Atomic requirement | Risk/tags | Dependencies | Owner | Verify | Compat |
|---|---|---|---|---|---|---|---|
| TK3-ADOPT-01 | Stage 3 Recurring reservations: adoption | POST /series adopts an existing reservation as occurrence zero. | C HT ST | TK1-GET-04 | S | Z12,Z13,Z14,Z15 | S/R/H/A |
| TK3-ADOPT-02 | Stage 3 Recurring reservations: adoption | Series adoption requires a bearer token; absent authentication returns 401 unauthenticated. | H AU HTTP | TK1-AUTH-11 | S | Z12,Z13,Z14,Z15 | S/R/H/A |
| TK3-ADOPT-03 | Stage 3 Recurring reservations: adoption | Series adoption requires an idempotency key with the full Stage 1 replay contract. | C RP TX | TK1-IDEM-01 | S | Z12,Z13,Z14,Z15 | S/R/H/A |
| TK3-ADOPT-04 | Stage 3 Recurring reservations: adoption | Series request requires anchor_reference, count and interval_weeks. | H VA | TK3-ADOPT-01 | S | Z12,Z13,Z14,Z15 | S/R/H/A |
| TK3-ADOPT-05 | Stage 3 Recurring reservations: adoption | count is an integer 2..12 including the anchor; invalid values or booleans give 422 validation_failed. | H VA | TK3-ADOPT-04 | S | Z12,Z13,Z14,Z15 | S/R/H/A |
| TK3-ADOPT-06 | Stage 3 Recurring reservations: adoption | interval_weeks is an integer 1..4; invalid values or booleans give 422 validation_failed. | H VA | TK3-ADOPT-04 | S | Z12,Z13,Z14,Z15 | S/R/H/A |
| TK3-ADOPT-07 | Stage 3 Recurring reservations: adoption | Unknown or another owner's anchor returns 404 not_found. | C AU HTTP | TK1-GET-04 | S | Z12,Z13,Z14,Z15 | S/R/H/A |
| TK3-ADOPT-08 | Stage 3 Recurring reservations: adoption | A cancelled anchor returns 409 reservation_cancelled. | H HT HTTP | TK1-PATCH-05 | S | Z12,Z13,Z14,Z15 | S/R/H/A |
| TK3-ADOPT-09 | Stage 3 Recurring reservations: adoption | The anchor must satisfy its existing accepted cancellation cutoff. | C TM HT | TK3-TERMS-12 | S | Z12,Z13,Z14,Z15 | S/R/H/A |
| TK3-ADOPT-10 | Stage 3 Recurring reservations: adoption | An already adopted anchor returns 409 already_in_series. | H HT HTTP | TK3-ADOPT-01 | S | Z12,Z13,Z14,Z15 | S/R/H/A |
| TK3-ADOPT-11 | Stage 3 Recurring reservations: adoption | Occurrence zero is the existing anchor and retains its reference and identity. | C HT ST | TK3-ADOPT-01 | S | Z12,Z13,Z14,Z15 | S/R/H/A |
| TK3-ADOPT-12 | Stage 3 Recurring reservations: adoption | Adoption leaves the anchor's revision unchanged. | C HT | TK3-ADOPT-11 | S | Z12,Z13,Z14,Z15 | S/R/H/A |
| TK3-ADOPT-13 | Stage 3 Recurring reservations: adoption | Adoption leaves the anchor's accepted_terms and end time unchanged. | C HT TM | TK3-ADOPT-11 | S | Z12,Z13,Z14,Z15 | S/R/H/A |
| TK3-ADOPT-14 | Stage 3 Recurring reservations: adoption | Adoption leaves the anchor's history unchanged. | C HT | TK3-ADOPT-11 | S | Z12,Z13,Z14,Z15 | S/R/H/A |
| TK3-ADOPT-15 | Stage 3 Recurring reservations: adoption | Adoption leaves the anchor's timestamps unchanged. | C HT TM | TK3-ADOPT-11 | S | Z12,Z13,Z14,Z15 | S/R/H/A |
| TK3-ADOPT-16 | Stage 3 Recurring reservations: adoption | Adoption leaves the original anchor idempotent response unchanged. | C RP HT | TK3-ADOPT-11,TK3-TERMS-08 | S | Z12,Z13,Z14,Z15 | S/R/H/A |
| TK3-ADOPT-17 | Stage 3 Recurring reservations: adoption | Occurrence i uses the anchor's current local date plus i*interval_weeks*7 calendar days. | C TM | TK3-ADOPT-06 | S | Z12,Z13,Z14,Z15 | S/R/H/A |
| TK3-ADOPT-18 | Stage 3 Recurring reservations: adoption | Each generated occurrence retains the anchor's local clock time, rather than advancing fixed UTC weeks. | C TM | TK3-ADOPT-17,TK1-TIME-01 | S | Z12,Z13,Z14,Z15 | S/R/H/A |
| TK3-ADOPT-19 | Stage 3 Recurring reservations: adoption | Each generated occurrence independently selects its own local date's policy. | C TM HT | TK3-POL-11,TK3-ADOPT-17 | S | Z12,Z13,Z14,Z15 | S/R/H/A |
| TK3-ADOPT-20 | Stage 3 Recurring reservations: adoption | Each generated occurrence uses the anchor's party size. | H ST VA | TK3-ADOPT-11 | S | Z12,Z13,Z14,Z15 | S/R/H/A |
| TK3-ADOPT-21 | Stage 3 Recurring reservations: adoption | Each generated occurrence uses the anchor's table selection, including a pair. | C ST TX | TK3-ADOPT-11,TK2-PAIR-07 | S | Z12,Z13,Z14,Z15 | S/R/H/A |
| TK3-ADOPT-22 | Stage 3 Recurring reservations: adoption | Every generated occurrence obeys its selected policy's grid and opening hours. | C TM VA | TK3-ADOPT-19,TK1-CREATE-08,TK1-CREATE-09 | S | Z12,Z13,Z14,Z15 | S/R/H/A |
| TK3-ADOPT-23 | Stage 3 Recurring reservations: adoption | Every generated occurrence uses its selected policy's absolute duration and capacity. | C TM VA HT | TK3-ADOPT-19,TK3-TERMS-03 | S | Z12,Z13,Z14,Z15 | S/R/H/A |
| TK3-ADOPT-24 | Stage 3 Recurring reservations: adoption | Every generated occurrence obeys ordinary member occupancy rules. | C TX | TK3-ADOPT-21,TK1-OCC-01 | S | Z12,Z13,Z14,Z15 | S/R/H/A |
| TK3-ADOPT-25 | Stage 3 Recurring reservations: adoption | A nonexistent generated local time rejects the entire adoption with 422 invalid_local_time. | C TM TX | TK1-TIME-03,TK3-ADOPT-18 | S | Z12,Z13,Z14,Z15 | S/R/H/A |
| TK3-ADOPT-26 | Stage 3 Recurring reservations: adoption | A repeated generated local time resolves to the first occurrence. | C TM | TK1-TIME-04,TK3-ADOPT-18 | S | Z12,Z13,Z14,Z15 | S/R/H/A |
| TK3-ADOPT-27 | Stage 3 Recurring reservations: adoption | Any adoption failure leaves no partial series or generated reservation. | C TX ST | TK3-ADOPT-22,TK3-ADOPT-24 | S | Z12,Z13,Z14,Z15 | S/R/H/A |
| TK3-ADOPT-28 | Stage 3 Recurring reservations: adoption | Any adoption failure leaves no partial histories. | C TX HT | TK3-ADOPT-27 | S | Z12,Z13,Z14,Z15 | S/R/H/A |
| TK3-ADOPT-29 | Stage 3 Recurring reservations: adoption | Any adoption failure leaves no changed counters. | C TX HT | TK3-ADOPT-27 | S | Z12,Z13,Z14,Z15 | S/R/H/A |
| TK3-ADOPT-30 | Stage 3 Recurring reservations: adoption | Any adoption failure leaves no consumed idempotency claim. | C TX RP | TK1-IDEM-12,TK3-ADOPT-27 | S | Z12,Z13,Z14,Z15 | S/R/H/A |
| TK3-ADOPT-31 | Stage 3 Recurring reservations: adoption | The first failing generated occurrence in index order determines the ordinary booking error. | C OR VA TM | TK3-ADOPT-17 | S | Z12,Z13,Z14,Z15 | S/R/H/A |
| TK3-ADOPT-32 | Stage 3 Recurring reservations: adoption | Adoption succeeds with 201 and an opaque series_id, revision 1 and interval_weeks. | H HTTP HT | TK3-ADOPT-01,TK1-HTTP-05 | S | Z12,Z13,Z14,Z15 | S/R/H/A |
| TK3-ADOPT-33 | Stage 3 Recurring reservations: adoption | Success returns all count occurrences in index order. | H OR HTTP | TK3-ADOPT-05 | S | Z12,Z13,Z14,Z15 | S/R/H/A |
| TK3-ADOPT-34 | Stage 3 Recurring reservations: adoption | Each occurrence carries index, reference, exception:false and an ordinary reservation response. | H HTTP HT | TK3-ADOPT-33 | S | Z12,Z13,Z14,Z15 | S/R/H/A |
| TK3-ADOPT-35 | Stage 3 Recurring reservations: adoption | Every occurrence has a distinct ordinary reservation reference. | C ST HT | TK1-CREATE-05,TK3-ADOPT-33 | S | Z12,Z13,Z14,Z15 | S/R/H/A |
| TK3-ADOPT-36 | Stage 3 Recurring reservations: adoption | Occurrence references never change when dates or tables change. | C HT ST | TK3-ADOPT-35 | S | Z12,Z13,Z14,Z15 | S/R/H/A |
| TK3-ADOPT-37 | Stage 3 Recurring reservations: adoption | Occurrence indices never change when dates or tables change. | C HT ST | TK3-ADOPT-33 | S | Z12,Z13,Z14,Z15 | S/R/H/A |
| TK3-ADOPT-38 | Stage 3 Recurring reservations: adoption | Generated occurrences appear in ordinary reservation lists. | H HTTP | TK1-GET-01,TK3-ADOPT-33 | S | Z12,Z13,Z14,Z15 | S/R/H/A |
| TK3-ADOPT-39 | Stage 3 Recurring reservations: adoption | Generated occurrences occupy their member tables. | C TX | TK3-ADOPT-24 | S | Z12,Z13,Z14,Z15 | S/R/H/A |
| TK3-ADOPT-40 | Stage 3 Recurring reservations: adoption | Generated occurrences have ordinary native histories. | C HT | TK3-HIST-10,TK3-ADOPT-34 | S | Z12,Z13,Z14,Z15 | S/R/H/A |
| TK3-ADOPT-41 | Stage 3 Recurring reservations: adoption | Successful adoption increments the restaurant revision exactly once for the whole operation. | C HT TX | TK3-ADOPT-27 | S | Z12,Z13,Z14,Z15 | S/R/H/A |
| TK3-ADOPT-42 | Stage 3 Recurring reservations: adoption | Series replay returns the original series response even after later amendments or cancellations. | C RP HT | TK1-IDEM-13,TK3-ADOPT-32 | S | Z12,Z13,Z14,Z15 | S/R/H/A |
| TK3-ADOPT-43 | Stage 3 Recurring reservations: adoption | Series replay changes no counters or state. | C RP HT | TK3-ADOPT-42 | S | Z12,Z13,Z14,Z15 | S/R/H/A |
| TK3-ADOPT-44 | Stage 3 Recurring reservations: adoption | Unknown series request fields are ignored for effects, while full parsed bodies remain receipt identities. | H VA RP | TK1-HTTP-03,TK1-IDEM-10,TK1-IDEM-11 | S | Z12,Z13,Z14,Z15 | S/R/H/A |

### TK3-SERIES: Recurring reservations: current state and individual edits

| ID | Source | Atomic requirement | Risk/tags | Dependencies | Owner | Verify | Compat |
|---|---|---|---|---|---|---|---|
| TK3-SERIES-01 | Stage 3 Recurring reservations: current state and individual edits | GET /series/{series_id} returns the adoption response shape with current reservation states. | H HTTP HT | TK3-ADOPT-32 | S | Z16,Z17 | S/H/A/R |
| TK3-SERIES-02 | Stage 3 Recurring reservations: current state and individual edits | Only the series owner may read it; another user gets 404 not_found. | C AU | TK3-SERIES-01 | S | Z16,Z17 | S/H/A/R |
| TK3-SERIES-03 | Stage 3 Recurring reservations: current state and individual edits | An anonymous series read returns 404 not_found. | C AU HTTP | TK3-SERIES-02 | S | Z16,Z17 | S/H/A/R |
| TK3-SERIES-04 | Stage 3 Recurring reservations: current state and individual edits | An unknown series returns 404 not_found. | H HTTP | TK3-SERIES-01 | S | Z16,Z17 | S/H/A/R |
| TK3-SERIES-05 | Stage 3 Recurring reservations: current state and individual edits | A real individual PATCH permanently marks its occurrence exception:true. | C HT | TK3-TERMS-17,TK3-ADOPT-37 | S | Z16,Z17 | S/H/A/R |
| TK3-SERIES-06 | Stage 3 Recurring reservations: current state and individual edits | A real individual PATCH increments the containing series revision once. | C HT TX | TK3-SERIES-05 | S | Z16,Z17 | S/H/A/R |
| TK3-SERIES-07 | Stage 3 Recurring reservations: current state and individual edits | A no-op PATCH changes neither series revision nor exception flag. | C HT | TK3-TERMS-18 | S | Z16,Z17 | S/H/A/R |
| TK3-SERIES-08 | Stage 3 Recurring reservations: current state and individual edits | A failed PATCH changes neither series revision nor exception flag. | C TX HT | TK3-TERMS-20 | S | Z16,Z17 | S/H/A/R |
| TK3-SERIES-09 | Stage 3 Recurring reservations: current state and individual edits | First cancellation increments the containing series revision once. | C HT TX | TK3-REV-01 | S | Z16,Z17 | S/H/A/R |
| TK3-SERIES-10 | Stage 3 Recurring reservations: current state and individual edits | Cancellation retains the occurrence in the series. | H HT | TK3-SERIES-09 | S | Z16,Z17 | S/H/A/R |
| TK3-SERIES-11 | Stage 3 Recurring reservations: current state and individual edits | Cancellation does not mark an unexcepted occurrence as exception and does not clear an already permanent exception. | C HT | TK3-SERIES-05,TK3-SERIES-09 | S | Z16,Z17 | S/H/A/R |
| TK3-SERIES-12 | Stage 3 Recurring reservations: current state and individual edits | Repeated cancellation changes no series counter. | C HT | TK3-REV-02 | S | Z16,Z17 | S/H/A/R |
| TK3-SERIES-13 | Stage 3 Recurring reservations: current state and individual edits | Cancelling the anchor does not cancel siblings. | C HT TX | TK3-SERIES-09 | S | Z16,Z17 | S/H/A/R |
| TK3-SERIES-14 | Stage 3 Recurring reservations: current state and individual edits | Ordinary accepted cutoff and optional booking revision checks still apply to occurrence edits. | C OR TM CC | TK3-TERMS-12,TK3-REV-05 | S | Z16,Z17 | S/H/A/R |

### TK3-PAIRHIST: Combined-table history

| ID | Source | Atomic requirement | Risk/tags | Dependencies | Owner | Verify | Compat |
|---|---|---|---|---|---|---|---|
| TK3-PAIRHIST-01 | Stage 3 Combined-table history | Combination decisions use summed capacities from the selected policy. | C VA HT | TK3-POL-11,TK2-PAIR-06 | S | Z11,Z17 | S/H/R |
| TK3-PAIRHIST-02 | Stage 3 Combined-table history | Single creation and single-to-single history operations retain table_id changes. | H HT HTTP | TK3-HIST-10 | S | Z11,Z17 | S/H/R |
| TK3-PAIRHIST-03 | Stage 3 Combined-table history | Pair creation uses table_ids from null to the complete pair instead of table_id. | H HT HTTP | TK3-HIST-11 | S | Z11,Z17 | S/H/R |
| TK3-PAIRHIST-04 | Stage 3 Combined-table history | Any actual selection change involving a pair uses table_ids with complete before/after lists. | H HT HTTP | TK3-HIST-12 | S | Z11,Z17 | S/H/R |
| TK3-PAIRHIST-05 | Stage 3 Combined-table history | Pair history lists use declared combination order, including normalized reversed input. | H OR HT | TK2-OPTIONS-09 | S | Z11,Z17 | S/H/R |
| TK3-PAIRHIST-06 | Stage 3 Combined-table history | Reversing the same pair alone is not a real amendment and retains revision, accepted terms, end time and history. | C HT OR | TK3-TERMS-18 | S | Z11,Z17 | S/H/R |
| TK3-PAIRHIST-07 | Stage 3 Combined-table history | Pair policy, revision and replay semantics are identical to single-table semantics, including exact array-order request identity. | C RP HT CC | TK3-REV-05,TK1-IDEM-10,TK1-IDEM-11 | S | Z11,Z17 | S/H/R |

### TK3-BATCH: Collective moves under policies and agreements

| ID | Source | Atomic requirement | Risk/tags | Dependencies | Owner | Verify | Compat |
|---|---|---|---|---|---|---|---|
| TK3-BATCH-01 | Stage 3 Collective moves under policies and agreements | Each real batch move applies individual PATCH old accepted cutoff checks. | C TM OR | TK3-TERMS-13,TK1-MOVE-13 | S | Z18,Z19,Z20 | S/R/H/A |
| TK3-BATCH-02 | Stage 3 Collective moves under policies and agreements | Each real batch move validates all resulting fields and adopts its resulting date's policy. | C TM VA HT | TK3-TERMS-14 | S | Z18,Z19,Z20 | S/R/H/A |
| TK3-BATCH-03 | Stage 3 Collective moves under policies and agreements | Per-move expected_revision is optional. | H HTTP | TK3-REV-03,TK1-MOVE-06 | S | Z18,Z19,Z20 | S/R/H/A |
| TK3-BATCH-04 | Stage 3 Collective moves under policies and agreements | Per-move expected_revision follows PATCH positive-integer validation and stale-revision rules. | C VA OR CC | TK3-REV-04,TK3-REV-06 | S | Z18,Z19,Z20 | S/R/H/A |
| TK3-BATCH-05 | Stage 3 Collective moves under policies and agreements | Within each item stale checks precede accepted cutoff and result validation; non-occupancy errors retain input-order priority. | C OR | TK1-MOVE-12,TK3-BATCH-04 | S | Z18,Z19,Z20 | S/R/H/A |
| TK3-BATCH-06 | Stage 3 Collective moves under policies and agreements | A no-op move retains accepted terms, end time, revision and history. | C HT | TK3-TERMS-18 | S | Z18,Z19,Z20 | S/R/H/A |
| TK3-BATCH-07 | Stage 3 Collective moves under policies and agreements | Every resulting booking satisfies real-change amendment and member occupancy rules, including unchanged listed occupancy. | C TX VA | TK1-MOVE-16,TK3-BATCH-02 | S | Z18,Z19,Z20 | S/R/H/A |
| TK3-BATCH-08 | Stage 3 Collective moves under policies and agreements | Any batch failure leaves every booking unchanged. | C TX HT | TK1-MOVE-17,TK3-BATCH-07 | S | Z18,Z19,Z20 | S/R/H/A |
| TK3-BATCH-09 | Stage 3 Collective moves under policies and agreements | Each changed booking increments its own revision exactly once. | C HT TX | TK3-TERMS-17 | S | Z18,Z19,Z20 | S/R/H/A |
| TK3-BATCH-10 | Stage 3 Collective moves under policies and agreements | Each changed booking receives exactly one changed history entry with actual fields/resulting terms. | C HT TX | TK3-HIST-12,TK3-HIST-19 | S | Z18,Z19,Z20 | S/R/H/A |
| TK3-BATCH-11 | Stage 3 Collective moves under policies and agreements | A successful batch containing real changes increments restaurant revision once for the whole batch. | C HT TX | TK3-BATCH-09 | S | Z18,Z19,Z20 | S/R/H/A |
| TK3-BATCH-12 | Stage 3 Collective moves under policies and agreements | Each affected series increments its revision once for the whole batch, even with multiple changed members. | C HT TX | TK3-SERIES-06,TK3-BATCH-09 | S | Z18,Z19,Z20 | S/R/H/A |
| TK3-BATCH-13 | Stage 3 Collective moves under policies and agreements | Each actually changed series occurrence permanently becomes an exception. | C HT | TK3-SERIES-05,TK3-BATCH-09 | S | Z18,Z19,Z20 | S/R/H/A |
| TK3-BATCH-14 | Stage 3 Collective moves under policies and agreements | A failed batch changes no reservation, restaurant or series revision. | C TX HT | TK3-BATCH-08 | S | Z18,Z19,Z20 | S/R/H/A |
| TK3-BATCH-15 | Stage 3 Collective moves under policies and agreements | A failed batch changes no histories or exception flags. | C TX HT | TK3-BATCH-08 | S | Z18,Z19,Z20 | S/R/H/A |
| TK3-BATCH-16 | Stage 3 Collective moves under policies and agreements | A successful batch replay changes no revisions, histories or exception flags. | C RP HT | TK1-MOVE-19,TK3-BATCH-10 | S | Z18,Z19,Z20 | S/R/H/A |
| TK3-BATCH-17 | Stage 3 Collective moves under policies and agreements | An all-no-op successful batch leaves counters unchanged under the adopted interpretation. | C HT | TK3-BATCH-06 | S | Z18,Z19,Z20 | S/R/H/A |
| TK3-BATCH-18 | Stage 3 Collective moves under policies and agreements | A series represented only by unchanged listed items does not increment its revision under the adopted interpretation. | C HT | TK3-BATCH-06,TK3-BATCH-12 | S | Z18,Z19,Z20 | S/R/H/A |

### TK3-UP: Recurring reservations and cumulative export import

| ID | Source | Atomic requirement | Risk/tags | Dependencies | Owner | Verify | Compat |
|---|---|---|---|---|---|---|---|
| TK3-UP-01 | Stage 3 Recurring reservations and cumulative export import | Stage 3 accepts an unchanged export from the same team's Stage 1 service. | C ST | TK1-XFER-04 | S | Z21,Z22,Z23,W14,W15 | S/R/B/H/A |
| TK3-UP-02 | Stage 3 Recurring reservations and cumulative export import | Stage 3 accepts an unchanged export from the same team's Stage 2 service. | C ST | TK2-UP-01 | S | Z21,Z22,Z23,W14,W15 | S/R/B/H/A |
| TK3-UP-03 | Stage 3 Recurring reservations and cumulative export import | Adoption works on eligible reservations imported from Stage 1 or Stage 2. | C ST HT | TK3-UP-01,TK3-UP-02,TK3-ADOPT-01 | S | Z21,Z22,Z23,W14,W15 | S/R/B/H/A |
| TK3-UP-04 | Stage 3 Recurring reservations and cumulative export import | Existing confirmation references and links remain usable through upgrade. | C ST UI | TK2-UP-03 | S/E | Z21,Z22,Z23,W14,W15 | S/R/B/H/A |
| TK3-UP-05 | Stage 3 Recurring reservations and cumulative export import | Existing browser sessions remain signed in through upgrade between requests. | C ST AU UI | TK2-UP-02 | S/E | Z21,Z22,Z23,W14,W15 | S/R/B/H/A |
| TK3-UP-06 | Stage 3 Recurring reservations and cumulative export import | Existing original booking retries remain valid with exact old response JSON. | C RP ST | TK2-UP-04,TK3-TERMS-08 | S/E | Z21,Z22,Z23,W14,W15 | S/R/B/H/A |
| TK3-UP-07 | Stage 3 Recurring reservations and cumulative export import | Retained browser form and pending key/body recover original legacy confirmation without enrichment or reconstructed request. | C RP UI ST | TK2-UP-05,TK2-UP-11 | S/E | Z21,Z22,Z23,W14,W15 | S/R/B/H/A |
| TK3-UP-08 | Stage 3 Recurring reservations and cumulative export import | Transfer preserves native immutable policy records, publication versions and effective-date/tie selection. | C ST HT | TK1-XFER-14,TK3-POL-08 | S | Z21,Z22,Z23,W14,W15 | S/R/B/H/A |
| TK3-UP-09 | Stage 3 Recurring reservations and cumulative export import | Transfer preserves native accepted terms, end times, reservation revisions and immutable history entries. | C ST HT | TK1-XFER-15,TK1-XFER-22,TK1-XFER-23,TK3-HIST-20 | S | Z21,Z22,Z23,W14,W15 | S/R/B/H/A |
| TK3-UP-10 | Stage 3 Recurring reservations and cumulative export import | Transfer preserves native series identities, owner, index/reference membership, revisions and permanent exception flags. | C ST HT | TK1-XFER-16,TK3-SERIES-05 | S | Z21,Z22,Z23,W14,W15 | S/R/B/H/A |
| TK3-UP-11 | Stage 3 Recurring reservations and cumulative export import | Transfer preserves all completed policy/series/create/batch request bodies and original receipts. | C ST RP | TK1-XFER-17,TK3-POL-01,TK3-ADOPT-03 | S | Z21,Z22,Z23,W14,W15 | S/R/B/H/A |
| TK3-UP-12 | Stage 3 Recurring reservations and cumulative export import | Transfer preserves Stage 3's explicitly required restaurant-revision deltas/state without importing later-stage rules. | C ST HT | TK3-ADOPT-41,TK3-BATCH-11 | S | Z21,Z22,Z23,W14,W15 | S/R/B/H/A |
| TK3-UP-13 | Stage 3 Recurring reservations and cumulative export import | Legacy import preserves identities, existing timestamps, statuses, original receipts and any existing history exactly. | C ST HT RP | TK3-UP-01,TK3-UP-02 | S | Z21,Z22,Z23,W14,W15 | S/R/B/H/A |
| TK3-UP-14 | Stage 3 Recurring reservations and cumulative export import | Missing legacy reservation revision/accepted-terms initializes revision 1 and policy-0 baseline under adopted interpretation. | C ST HT | TK3-TERMS-07,TK3-UP-13 | S | Z21,Z22,Z23,W14,W15 | S/R/B/H/A |
| TK3-UP-15 | Stage 3 Recurring reservations and cumulative export import | Legacy history baseline does not invent unobserved edits or event timestamps; verify chosen baseline plus truthful future native entries. | H ST HT | TK3-UP-13,TK3-HIST-18 | S | Z21,Z22,Z23,W14,W15 | S/R/B/H/A |
| TK3-UP-16 | Stage 3 Recurring reservations and cumulative export import | Reset clears published policies, histories, series, counters and new receipts as well as inherited state. | C TX ST RP | TK1-FIX-02,TK1-XFER-20 | S | Z21,Z22,Z23,W14,W15 | S/R/B/H/A |
| TK3-UP-17 | Stage 3 Recurring reservations and cumulative export import | Import still replaces all destination data and credentials, repeats restore the snapshot, and invalid import changes nothing. | C TX ST AU | TK1-XFER-06,TK1-XFER-07,TK1-XFER-08,TK1-XFER-11 | S | Z21,Z22,Z23,W14,W15 | S/R/B/H/A |
| TK3-UP-18 | Stage 3 Recurring reservations and cumulative export import | No new explanation/history screen or unspecified series-management browser flow is required; cumulative Stage 2 screens remain compliant. | H UI | TK2-WEB-01,TK3-EXPL-02 | S | Z21,Z22,Z23,W14,W15 | S/R/B/H/A |

### TK3-GATE: Final submission assignment

| ID | Source | Atomic requirement | Risk/tags | Dependencies | Owner | Verify | Compat |
|---|---|---|---|---|---|---|---|
| TK3-GATE-01 | Stage 3 Final submission assignment | Stage 3 production starts only after independent Stage 2 ACCEPT and a committed copied baseline. | C SC ST | TK2-GATE-01 | C | Z24 | - |
| TK3-GATE-02 | Stage 3 Final submission assignment | Stage 3 acceptance requires independent formal verdict on the exact integrated production FULL SHA. | C SC | TK3-GATE-01 | C | Z24 | - |
| TK3-GATE-03 | Stage 3 Final submission assignment | Only the canonical owned sanitized Stage 3 ledger path is committed during the serialized evidence window. | H SC | - | C | Z24 | - |

## Precedence and state-transition map

These are a partial order of specified decisions, not an invented total error ranking. When multiple unrelated rules have no specified order, isolate them in independent cases and record the observed stable interpretation.

| Boundary | Required order and observable outcome |
|---|---|
| Protected idempotent writes | Parse JSON object and authenticate; resolve user/method/path/key/full parsed-body identity before endpoint fields, permissions/resources and current-state checks. Missing/empty key400; oversize key422. Used differing body409 even if now invalid; successful replay200 returns immutable original JSON without a new effect. Do not normalize pair arrays or strip ignored fields before comparison. |
| Policy publication | After receipt resolution, enforce manager visibility/permission and complete policy validity before committing policy, version and receipt together. Unknown restaurant404, non-manager403, anonymous401 are isolated cases; their mutual priority with invalid fields is not otherwise specified. Failure/replay allocates no version. |
| Date-effective selection | Resolve actual local calendar start date; choose greatest eligible effective_from, then greatest version for ties, else fixture policy0. Publication chronology never substitutes for effective-date ordering. Existing accepted intervals/cutoffs do not use freshly selected terms. |
| Individual amendment | Owner/resource visibility; optional expected_revision type/range and valid mismatch before accepted current-start cutoff and proposed-field validation. Confirmed/editable requirement still applies. Detect semantic no-op without adopting a new policy; real change validates the complete merged result under resulting-date policy before final occupancy and atomic record/terms/end/history/revision/agreement update. Cancelled-vs-stale priority is not explicitly specified. |
| Cancellation | Owner visibility; already cancelled returns200 with current state and no additional counters/history. First cancellation checks accepted current-start cutoff, frees all members and atomically appends terminal empty-changes event with resulting revision; native series revision increments once without newly marking exception. |
| Collective moves | Resolve receipt first; validate structure/distinct references/same restaurant and item errors under inherited input-order rule. Within an item revision control precedes accepted cutoff, then proposed changes. Non-occupancy errors in input order precede final overlaps. Build final candidates while unchanged listed occupancy remains present; publish all records, histories, terms, booking revisions, at-most-one restaurant increment, per-affected-series increments, exception flags and original receipt together. |
| Series adoption | Resolve receipt first, validate owner/confirmed/unadopted/editable anchor and count/interval; these unrelated anchor/body-error tie rankings are unspecified. Preserve occurrence0. Generate in index order using calendar weeks and each date policy; first failing generated occurrence determines ordinary error. Publish agreement, new bookings/histories, one restaurant increment and receipt together, or none. |
| Owner-only new reads | History, decision and series reads use indistinguishable404 for unknown/foreign/anonymous; general protected write401 remains intact. Managers retain foreign private-read404. |
| Import/reset/export | Validate candidate replacement before one atomic publication. Export reads a coherent snapshot of complete records, receipts, histories, policies and agreements. Import is replacement; retries see original receipts, existing sessions remain valid, old destination credentials disappear. Reset clears every generation's state. |

Capacity and no_overlap are independent explanation truths, not alternative errors to short-circuit. Ordinary creation errors not given a relative ranking stay individually specified. Preserve the Stage 1 body type/value overrides, plain-digit query restrictions, exact cutoff equality, half-open UTC/absolute intervals, fixture ordering and Stage 2 browser response-generation rules.

## Risk model dependencies and implementation handoff

| Blocking risk cluster | Atomic obligations and dependency order | Independent coverage obligation |
|---|---|---|
| Published policy chosen by version rather than local effective date; ties or per-restaurant counters wrong | TK3-POL-04..15,36..37; configuration/auth -> validated complete immutable policy -> successful version allocation -> date/tie resolver | Z03..05: reverse publication dates, same-date ties, earlier-than-all dates, exact effective boundary, two restaurants, failed/replayed versions. |
| Publication retroactively edits accepted occupancy/cutoff; policy changes only partially applied to real amendments | TK3-TERMS-03..20, TK3-REV-01..10; selected policy -> full terms snapshot -> old accepted cutoff -> real/no-op decision -> complete resulting validation -> member occupancy | Z06..09: strict new policy, retained end/cutoff, party-only real change revalidates old time/table, new duration causes overlap, no-op retains now-invalid terms, stale priority/CAS. |
| Historical truth corrupted by replay, pair normalization or same-second ordering | TK3-HIST-05..20, TK3-PAIRHIST-02..07, inherited TK1-IDEM-05..14 | Z07,10,11: contiguous seq/at order, actual-only fields, pair orientation and single/pair transitions, terminal cancel, old response JSON after change and transfer. |
| New read privacy or policy permission regresses inherited auth | TK3-MGR-01..08, TK3-HIST-02..04, TK3-DEC-03..05, TK3-SERIES-02..04 | Z03,10,16 plus V05: owner/foreign/unknown/anonymous/malformed-token matrix; manager cannot view foreign private records. |
| Series advances UTC weeks, mutates anchor or leaves partial state/receipt | TK3-ADOPT-11..43; preserved anchor -> calendar dates -> per-date policy/DST/member candidates -> full validation -> one atomic agreement/records/receipt commit | Z12..15,19..22: spring gap, fold first occurrence, policy capacity/grid/duration changes, first error index, member contention, anchor exact equality, failed-key reuse and no orphan identities. |
| Agreement counters/exceptions drift under no-op/cancel or multi-member batch | TK3-SERIES-05..14, TK3-BATCH-01..18; existing expected revision/cutoff -> result candidates -> once-per-booking/series/restaurant effects | Z16..20: permanent exceptions, cancelled exceptions, anchor-only cancel, unchanged series listed, several changed members in one series, multiple affected series, all-no-op batch. |
| Upgrade destroys legacy session/receipt or fabricates historical edits | TK3-UP-01..17; classify legacy format -> preserve known fields/history/receipts -> missing baseline under policy0 -> portable atomic replacement | Z21,22 plus W18,19: populated exact Stage1/2 sources, original old JSON shape, lost-response browser retry, imported anchor adoption, Stage3 same-stage historical truth. |
| Browser confuses original detail with selected-policy eligibility or manufactures success | TK2-RACE/CONFLICT/UNCERTAIN/QA obligations; current server response -> matching labels/form -> retained request identity | Z23 plus W03..08,14,17,18: current capacities/duration, delayed searches/detail, conflict preservation, before/after-commit loss, mobile/desktop keyboard/labels/contrast and bundled offline assets. |
| Release evidence substitutes for product acceptance | TK3-GATE-01..03; exact Stage2 ACCEPT -> committed separate copy -> integrated Stage3 FULL SHA -> independent complete verdict | Z24; analysis-only commit does not open production gate or accept candidate. |

Systems owns policy/term/history/series/selection/transaction state, export/import and transport/container/docs. Experience owns retained browser session/request identity, authoritative current selections, labels and feedback and all rendered product checks. Their interface requires current API fields and exact historical receipt fallback; original detail labels/timezone remain useful while its original capacities/hours are not current booking rules. Conductor owns gates and serialized Git windows; Verifier owns independent oracles, executed evidence and final verdict. This is behavioral dependency ordering, not a prescribed storage or locking architecture.

## Cumulative independent verification catalogue

All fixture values and labels in these procedures are synthetic. Expected intervals, pair eligibility, JSON values and DOM state transitions must be derived independently of production helpers. Record case IDs, exact production FULL SHA, status/code/JSON or rendered-state observations and sanitized evidence references. Never commit actual passwords, bearer tokens, opaque exports or browser session dumps. Keep snapshots private and ephemeral; public evidence can report equality outcomes and redacted structural counts.

### Inherited procedures applied cumulatively

V01..V20 retain their obligation sets and use current Stage 3 shapes, date-selected policies and retained accepted occupancy/cutoffs where appropriate; historical replay values remain unchanged. All four required-key write families are covered, extending the original V06 wording. The following summaries keep the cumulative ledger self-contained; the initial Stage 1 ledger supplies original calibration detail but is not required to interpret the rows above.

| Procedure | Independent obligation and coverage expectation |
|---|---|
| V01 | Reproduce Dockerfile/RUN.md build and single-container launch with custom/default PORT, 2 CPU/2GiB, no runtime outbound access; healthy/API-ready <=60s. Confirm scoped delivery/provenance and bundled browser assets. Host package imports are not acceptance. |
| V02 | Reset A->B repeatedly removes old accounts/tokens/records/config/receipts, with coherent visibility after204. Seed config order, all ID boundaries, given short passwords, single/pair confirmed/cancelled records; login and occupancy reflect fixture. Reject wrong-type/value inputs using §5 without partial state. |
| V03 | Endpoint matrix of missing/null/wrong-type/correct-type invalid fields, dates, party values, query plain digits, bare local times, IDs/keys and ignored fields. Include unknown valid JSON numeric exponent1e309 and calendar years0001/9999 without assuming binary-float parser limits. Verify all error envelopes/statuses/codes and no5xx. Pair selectors obey specific codes; distinguish historical response from new shape. |
| V04 | Signup/login errors and successful responses; signup8-character boundary versus unrestricted seeded password login; concurrent duplicate signup; all old session tokens coexist and survive import. Independent storage/source inspection proves password hashing for every account; HTTP behavior alone does not prove it. |
| V05 | Enumerate public/protected APIs and new HTML routes. Cross-owner list/reference GET/cancel/PATCH/moves cannot leak or mutate another record; foreign/unknown refs404. Export/import/reset deliberately remain unauthenticated. Browser signed-out cell selection cannot book. |
| V06 | All four required-key families:0/1/255/256-length keys, replay with reordered object keys/whitespace, different body including ignored fields, different user/path, failed4xx retry. Changed invalid body conflicts before field/resource rules. Arrays retain order and booleans differ from numbers; reversing a valid pair is a changed JSON body under the same key. |
| V07 | Public restaurant list/detail retain complete config/fixture shapes and ordering where specified; Stage 2 detail includes combinable. Duplicate table-ID strings in different restaurants remain independent. Unknown detail404; do not invent restaurant-list sorting. |
| V08 | Arbitrary calendar dates, closed day, unusual grid anchor, last end exactly closes, fully unavailable slot retained. Single-table capacity/overlap/filtering/order unchanged; available_options independently includes eligible pairs in specified order. Round-trip available slots into both request formats. |
| V09 | Berlin/New York's four specified2026 transition dates: gaps absent/rejected, repeated start first occurrence once, duration real elapsed minutes, offsets independently correct. Pair members share the same interval. Test valid boundary dates0001-01-01/9999-12-31 and long grid step; don't infer mandatory policy for unspecified gap-valued business boundaries. |
| V10 | Create legacy/new single/pair shape, IDs/reference uniqueness and immutable creation fields; capacities, hours/grid/DST/resources. Half-open adjacent intervals succeed; every overlapping member conflict fails atomically. Past valid creation allowed; seeds/cancellations remain in uniqueness scope. |
| V11 | Owner list contains confirmed/cancelled records, actual start instant descending, current create-shaped entries and empty-list shape. Current detail respects new selection fields; list after amendments reorders appropriately. Equal-start tie-break unspecified. |
| V12 | Before/at/after current cutoff, already-cancelled200, foreign404; successful cancel frees all members immediately but remains visible as cancelled. A single overlapping pair released does not free occupancy belonging to another nonoverlapping interval. |
| V13 | PATCH one/all/none fields without a key, single<->pair changes, merged omitted fields, no self-conflict; explicit legacy selector replaces old set. Future target cannot bypass existing cutoff. Every failure preserves full original state/member occupancy; success transfers together and preserves ID/reference. |
| V14 | Batch1/8/0/9, malformed structure/duplicate refs/foreign/mixed restaurants; every amendment code. Non-occupancy input order/cutoff priority before final member conflicts; pair/single swaps and no-ops; every failure preserves all records, members and reusable key. Results remain input order including unchanged records. |
| V15 | Original create/batch receipt replay after amend/cancel/no-op returns original JSON200, including historical selection/status/timestamps; no effect. Cross-path same key independent. Pair normalization must not rewrite receipt bodies or historical responses. |
| V16 | Barrier-start up to50 competing/identical requests: single201 and replay200 for identical key; member contention, changed bodies/users, create/PATCH/moves/cancel races. Audit complete response set, latency/no5xx and every confirmed member interval. Separate restaurants with equal table strings stay independent. |
| V17 | Export atomic/read-only/coherent snapshot; concurrent transaction leaves before-or-after booking+receipt state. Later source mutations cannot alter snapshot. Transfer wrapper stays track/version1 with opaque object state. |
| V18 | Independent source/destination processes with source unavailable, no shared files/volume/port: accounts/hashes/all tokens/config/order/records/IDs/statuses/timestamps and original successful receipts survive. Destination credentials/data removed, failed keys reusable, repeated restore idempotent, A->B->C portable; reset clears imported state. Includes required Stage 1->2 path and new browser continuity via W18. |
| V19 | Malformed JSON import400; missing/wrong track/version/invalid state422 under specific envelope interpretation; no partial destination replacement. Test pair config/membership/receipts and reuse after rejection. Private exports never become repo evidence. |
| V20 | Export/reset/import versus create/PATCH/batch/cancel/receipt replay races remain serializable and whole-state coherent. Reads cannot expose half a pair, partial batch, torn record/receipt or mixed generations. Replacement success sets subsequent visibility boundary. |

### Inherited Stage 2 procedures

| Procedure | Concrete cases and required observations |
|---|---|
| W01 | Direct GET of all four routes at fresh startup yields HTML; API remainsJSON. Navigate required screens/states through UI, including signed-out browsing. Deny external network and inspect assets/fonts/scripts/styles load from bundled image. Verify custom PORT and an independently started browser/server origin. |
| W02 | Exercise signup/login through exact hooks, invalid/valid inputs and visible/absent auth-error. Signed-in display name appears on every route and inline booking/confirmation/detail state; logout updates client state across in-page navigation and prevents anonymous booking. Existing other account tokens remain governed by inherited multiple-session rules. |
| W03 | Controlled fixtures: tables deliberately out of ID/capacity order, closed day, slots with no seats, some singles below party capacity. Assert one single cell per table/slot, exact testids and true/false from the completed search party, unavailable click no-op, available selection correct form, signed-out auth behavior and no-slots only when slots absent. Labels come from matching detail. Changing controls without a search must not relabel old results as a new query. |
| W04 | Deterministic browser/network interception: search A earlier/slower than B, same restaurant different date/party and different restaurant with colliding table strings/distinct labels. Release availability and detail responses in both crossed orders. Click B selection while stale A/detail callbacks are pending; grid/labels/form remain B. A late closed-day/error response must not replace successful B with no-slots/error. Start conflict refresh C then search D; late C cannot reset D. Assert DOM fields, data-available, labels and outgoing booking restaurant/slot/party together. |
| W05 | Signed-in single/pair booking flow uses exact form/summary/input/submit hooks. Pre-fill actual searched party, not subsequently edited search inputs. Success leaves form and exact reference/details/member labels. Submit unchanged twice: same request key/body/reference and one server effect, noerror. Change party or selection/time: new request identity and independent server outcome. Capture requests privately and report equality only. |
| W06 | Two clients: open form in A, B takes selected single or one pair member, A submit ->409booking-error, availability refresh, form/selection/inputs preserved and noconfirmation for rejected attempt. Edit choice and recover. Delay refresh/detail responses to ensure form preservation and newest-search coherence coexist. Test other confirmed4xx/cutoff errors have understandable error states. |
| W07 | Drop response after server commit using proxy/interception, and fail before server receives request: both produce nonempty booking-uncertain, no booking-error/newconfirmation. Unchanged retry has identical key/body; after-commit retry returns200/originalreference and one effect, before-commit retry returns201/one effect. Successful retry removes uncertainty/error elements. Change field after uncertainty ->newidentity; historical pending attempt remains a server fact, not a cached success. Exercise repeated/double submit and pair body. A delivered409/422 is confirmed rejection, not uncertainty. |
| W08 | Lookup own/foreign/unknown references via exact hooks; found detail exact status, all member labels. Cancel success removes button, updates status and all-member availability; repeated API cancel remains200. Past/cutoff refusal shows reservation-error and unchanged record. After successful lookup, a failed lookup must not present stale data as the requested record. Test signed-in display name on lookup and retained imported reference. |
| W09 | Fixture pairs [b,a],[a,c] with unequal capacities/nonlexical table order; no [b,c] inferred. Empty/omitted legacy combinable configuration retains ordinary singles. Seed each legacy/new selector, default confirmed and explicit cancelled; cancelled members free. Same table strings in another restaurant independent. Check policy/fixture fidelity after reset/export/import. Invalid fixture-pair details beyond stated model have unspecified precedence; distinguish recommendation from contract. |
| W10 | Both create request formats; table_ids [a] single, [b,a] and reversed [a,b] valid declared pair, undeclared [b,c], three members, duplicates, both selectors, empty/missing/wrong-type selector/member and unknown/cross-restaurant members. Party=combined capacity succeeds, capacity+1 fails specific code, invalid party types422. New single responses contain both table_ids/table_id, pair responses onlytable_ids; prior receipt JSON preserved. No partial occupancy on failure; same key reversed arrayconflicts before membership validation. |
| W11 | Independently enumerate all singles and all declared pairs for each slot. Verify filtering, capacity sum, any-member overlap including pair-vs-single and overlapping pairs; singles first fixture order, pairs declaration order, pair member orientation declaration order. Legacy available_table_ids excludes pair encodings and preserves exact single semantics. Empty available_options still retains slot; closed day returnsno slots. Export/import retains order. |
| W12 | PATCH single->pair, pair->single via both accepted explicit selectors, pair->another pair, time/party only, empty/no-op. A stored single record carrying both response fields must still accept a one-selector request. Cutoff based on original start; target capacity/approval/member overlap failures preserve all old members/record. Identity/reference/creation truth remains intact. Cancel pair frees both immediately. |
| W13 | Atomic batch final-state tests: swaps/cycles single<->pair with shared members, unchanged pair blocking a listed/unlisted target, resulting pairs sharing one member, pair vs unlisted single, simultaneous adjacency allowed. Error input/cutoff ordering; unknown fields ignored; selection codes apply per item. All-or-none records/member occupancy/key, input-order response, no-op preserves every value, retry after4xx first-use, original batch replay after pair/single amendments/cancel. |
| W14 | Pair cells for all available eligible declarations; exact declared-order ID concatenation and local time, data-available from server options. Use labels unlike IDs and long names; summary names every member, confirmation-tables/reservation-tables all labels, human-readable combination. Verify legacy single hook/flow unchanged. Pair conflicts/lost-response recovery exercised through UI, not API alone. Unavailable pair cells are optional; if shown their data-available/click behavior must be truthful. |
| W15 | Both Berlin/New York gap/fold fixtures with declared pairs; availability/creation/PATCH/moves consistently first occurrence and elapsed duration. Pair member conflicts straddling transition, each member cancellation and half-open adjacency. Confirm displayed local time/labels correspond to server offsets rather than browser timezone. |
| W16 | Up to50 synchronized HTTP writes: pair vs each member single, two pairs sharing one member, distinct disjoint selections, competing pair amendments, batch vs create, no-op vs create. Include identical keys and different users. Reads while writes run see no half-pair or transient released member; statuses/receipts/results admit one valid serialization. Audit intervals by (restaurant,member-ID), not array equality. |
| W17 | At375CSSpx and desktop (e.g.1280CSSpx), render all routes, single/pair forms, large grids/long labels, empty/loading/error/refused/uncertain/success. Check document scrollWidth<=viewport width while all necessary data/controls remain accessible; readable hierarchy and consistent navigation/style. Inspect visible input labels, keyboard tab/focus and activation through required flows, focus after feedback, computed/rendered contrast and distinct states. Capture sanitized screenshots with synthetic names/references. No numeric contrast threshold or exact reference artwork is specified; substantiate sufficient contrast rather than invent mandatory visual tokens. Check no external asset requests. |
| W18 | Build accepted exact Stage 1 source and candidate exact Stage 2 destination independently. Use stable browser origin with Stage 2 assets and test routing to Stage 1 APIs before upgrade, or an equivalent retained client setup that does not require Stage 1 to serve a nonexistent UI. Sign in against source, retain token/form/reference, commit a Stage 1 legacy booking while dropping only response, take private export with token and successful receipt included. Stop source, import unchanged into destination, switch API routing between browser requests without reload/newscreen. Same tab remains signedin; unchanged pending form retries exact oldbody/key, serverreturns200/originalJSON/reference, UIclearsuncertainty and showsconfirmation. Retained ownreference lookup works. Also test imported amended/cancelled originals and batch receipt atAPI level. A separate Stage 2 pair lost-response snapshot/import case proves combo continuity. |
| W19 | Stage 2 A->fresh/populated B, repeatrestore, B->C with pair config/confirmed+cancelled records/all sessions/create+batch historical receipts. Audit every member/order/ID/status/timestamp, failed reusable keys, destination removal. Concurrent atomic snapshots after pair/batch commit are all-before/all-after including receipt. Corrupt imports reject without touching credentials/member occupancy/receipts. |
| W20 | Verify Stage 1 exact-SHA ACCEPT precedes committed copied Stage 2 production baseline; no premature backend/browser production acceptance. Verify ledger commit occurs only after verifier releases its window and changes only this owned file. The completed historical Stage 2 gate supplies provenance; Stage 3's active gate is Z24. Verify cumulative behavior on the exact Stage 3 candidate, not just test hooks or official pass count. |


### Stage 3 independent procedures

| Procedure | Concrete independent cases and required observations |
|---|---|
| Z01 | Explanation query/shape boundaries: omit explain, true, false, 1, empty, TRUE and arbitrary values; omitted means no explain fields while available_options remains. Closed day has slots:[]; fully occupied fitting slot survives. Public calls need no token. Assert status/code, response keys and local/offset fields. |
| Z02 | Independent truth matrix: synthetic fixture order [c,a,b], capacity-limited free table, sufficient occupied table, insufficient occupied table and sufficient free table. Both rules must appear in fixed order; verify each truth and AND, true IDs exactly match ordered available_table_ids. Pair reservation blocks both member explanations; old-duration occupancy persists after publishing a shorter policy. New candidate interval follows selected duration. |
| Z03 | Manager/API/complete-policy matrix: managers of one restaurant versus another, non-manager, anonymous and unknown restaurant. Validate missing six fields, actual invalid dates, integer/bool/fraction/string types, limits0/1/1440/1441 and cutoff0/10080/10081, opening weekdays/HH:MM/same-day/duplicates, exact capacity-key set and values1/100/101. Treat endpoint invalid-policy422 override explicitly. Failed writes leave versions/list/config/receipts unchanged. Unknown fields ignored without altering fixture identities/labels/zone/combinations; same key changed ignored field conflicts. |
| Z04 | Publication version/concurrency: two restaurants each start1; publish successes around failed attempts and replays and require contiguous successful versions. GET public list excludes0 in publication order; detail stays original. Concurrent identical-key publications exactly one201/others200 one version; different keys serialize distinct versions; original response replay after later publications unchanged. Same key across users and distinct policy paths independent; used key with invalid new body409. |
| Z05 | Selection oracle: publish synthetic effective dates2030-06-15 then2030-06-01 then another2030-06-15; distinguish all policy grids/durations/caps/cutoffs. Query/create before first, on each boundary, between and after. Expect policy0/second/third by eligible date and tie, never highest published version alone. Include past effective dates and booking local date different from UTC date; all weekdays/policy0 fallback. Rejected/replayed publications never change selection. |
| Z06 | Terms immutability: create single/pair under0/P1, save response/decision/history/end. Publish backdated stricter P2 and same-date P3; every saved accepted snapshot/current booking/end/history stays P1. A new booking uses newly selected policy. Whole accepted_terms includes unselected-table capacities and all weekdays, excludes effective_from; selected pair capacity sums policy capacities. Cancel must use old accepted cutoff, not fixture/current policy. |
| Z07 | Native history truth: create and immediately change table/time/party individually and together, then cancel; verify seq1,+1, event/at/revision/terms/order and from/to values. Multiple writes within a second still have total sequence and nondecreasing at. Creation has null sources/all three fields; changed only actual fields; cancellation empty/terminal. Failed writes/replay/repeated cancel do not append. Old snapshots unchanged after new terms and export/import. |
| Z08 | No-op versus real full-result validation: after publishing policy that forbids existing grid/party or lengthens duration, empty PATCH, same-value explicit fields, unknown-only PATCH and reversed pair must retain old terms/end/revision/history. Still confirmed/editable and cutoff constrained. Party-only or table-only real amendment must validate ALL resulting fields and adopt result-date terms/end; new length hitting another booking fails with original state intact. No-op should not be rejected just because latest policy would reject an old accepted slot. |
| Z09 | Expected revision matrix: missing, zero, negative, bool, string, fraction and current/stale positive values. Stale plus cutoff violation or invalid proposed party must give stale_revision before those rules; invalid control422. At barrier, two distinct real PATCHes with same revision admit at most one change, other stale; two true no-ops may both200 with unchanged revision. Test resulting-date policy change, occupancy failure/retry, cancellation/repeated cancel and unknown fields. Do not invent cancelled-vs-stale tie ranking. |
| Z10 | History/decision owner-read matrix: own confirmed/cancelled, another diner, manager but not owner, unknown reference, anonymous and malformed/unknown token. All nonowners use same404 envelope; own decision matches current revision/terms even after cancellation. Contrast ordinary reservation lookup anonymous401 and policy publication anonymous401. Verify wrapper/reference and that foreign content is never returned. |
| Z11 | Pair history normalization: declared pair [b,a], reversed request [a,b]. Pair creation has table_ids null->[b,a]; single->pair, pair->single and pair->different pair carry complete normalized before/after arrays; single->single table_id. Unchanged selection with party/time change contributes no selection change. Reversal alone no history/terms/revision update, but reused create/move key with reversed array is409 as parsed body differs. Arrays and full-body numeric identity survive transfer. |
| Z12 | Series request/anchor rules: count2/12 versus1/13 and interval1/4 versus0/5, bool/wrong types/missing fields, ignored fields. Own editable anchor, unknown/foreign404, cancelled409, already adopted409 and accepted-cutoff refusal. Keys0/1/255/256, failed4xx reusable, per-user/path identity. Eligibility and unrelated field-error ties not specified; isolate cases. Managers do not gain anchor ownership. |
| Z13 | Anchor preservation and generated state: adopt current amended single/pair anchor (created under older policy) with count12/interval4; exact pre/post anchor identity/reference/revision/terms/end/history/timestamps/original receipt equal. Generated starts equal anchor current local calendar date plus index*weeks*7 and same clock; distinct references/index order and each revision1/created history. Generated members/party copied from anchor, each date selects policy independently. Ordinary list/detail/availability includes generated bookings. Replays after modifications return original series JSON. |
| Z14 | Recurring DST/calendar/policy: use future editable anchors so an old cutoff does not mask DST. At preparation date2026-10-05, Berlin weekly anchor2027-03-21 at02:30 reaches verified IANA gap03-28; New York2027-03-07 at02:30 reaches gap03-14; adoption entirely rejects invalid_local_time. Berlin2026-10-18 at02:30 reachesfold10-25; NewYork2026-10-25 at01:30 reaches11-01; first occurrence/elapsed durations independently verified. If execution occurs later, choose upcoming independently verified transition dates; V09 retains all four explicitly specified2026 creation/availability cases, which allow past starts. A later policy reducing capacity, shifting grid or closing weekday rejects at its first affected index. Actual last/calendar-limit dates must reject impossible generation cleanly422 rather than5xx or partial allocation; representable occurrence dates retain ordinary validity. |
| Z15 | All-or-none/error-index oracle: later generated occurrence occupied on one pair member; another later occurrence off-grid/closed/overcapacity. First failing index wins ordinary error even if later code differs. Snapshot structural equality, owner lists/histories/agreement lookup and restaurant counter prove no partial allocation/claim. Release conflict and retry same key succeeds201; subsequent replay200. Policy0 with an unusually long fixture duration can cause generated occurrences to overlap each other or the anchor; whole adoption rejects. Include unlisted occupancy and half-open adjacent intervals. |
| Z16 | Current agreement/individual changes: GET own series returns current reservation states in stable index order; foreign/anonymous/unknown404. Real PATCH increments booking+series once, marks permanent exception; no-op/failure0. Cancel increments booking+series once but newly unexcepted staysfalse; alreadytrue staystrue. Repeatcancel0. Cancelling anchor leaves siblings. Reference/index/creation identity retained when occurrence dates cross/reorder; ordinary owner list still descending actual start. |
| Z17 | Terms/cutoff/exception interactions: imported/native anchor under old accepted cutoff, newer stricter/looser policy; occurrence edits use old cutoff then selected result-date policy. Reverse pair no-op preserves series revision and existing flag; single/pair real transition appends proper history and permanently marks exception. Moving an exception back to initial fields remains exception:true. Failure/stale leaves old flag/counters. Adopted anchor's pre-adoption receipt remains unchanged after series edits/cancel. |
| Z18 | Collective policy/CAS precedence: input item1 stale or cutoff with invalid party and item2 other validation; per-item stale before cutoff and input-order nonoccupancy before any final conflict. Mixed result dates select differing terms/durations; swaps/cycles succeed only when all final member intervals valid. Unchanged listed old-policy bookings remain occupant with old terms, not revalidated against new policy. Any failed item/conflict rolls back every record, terms/end/history/counter/flag and receipt; same failed key later first-use. |
| Z19 | Collective agreement counters: two changed occurrences from series A, one changed from B, unchanged from C, ordinary changed booking and no-op ordinary item. Each changed booking+1/one history; restaurant+1 whole; A/B each+1; C0; only actually changed occurrences permanent exceptions. All-no-op batch including reversed pair leaves all counters/history/terms/flags unchanged; successful receipt still recorded and replay returns original input-order result. Replay after later cancel changes nothing. Observe Stage3 restaurant deltas via accessible state/source inspection if no public counter exists; do not require a Stage4 endpoint. |
| Z20 | Serialization campaign up to50 in-flight: policy publications versus create/PATCH/series, concurrent anchor adoption, adoption versus member booking, series sibling PATCH/cancel, collective swaps versus create, expected-revision contenders and identical used/unused keys. Requests/results admit one valid order; reads/decisions/history/series/availability and snapshots never expose mismatched terms/end/revisions or partial generated/batch state. Audit member interval uniqueness, contiguous histories, per-operation counter deltas, original receipts and timeout/no5xx. Use independent transaction oracle, not production lock helpers. |
| Z21 | Required populated legacy upgrades: independently launch accepted exact Stage1 and independently accepted exact Stage2 source images into Stage3 candidate, source stopped/no shared volume/network address. Multiple tokens/accounts, amended/cancelled singles, pairs/declarations, existing create/batch originals and failed reusable keys preserved. Missing terms/revision gets policy0/revision1 baseline; retain any existing histories exactly, no invented old events. Imported eligible single/pair anchor can adopt; occurrence0 known state unchanged, generated occurrences have native histories. Preserve historical old JSON shape and exact numeric/full-body receipts. Browser retained source-session/reference and lost-response form retry recovers original confirmation without reload between completed import and next request. Report chosen legacy history baseline, not fabricated reconstructive equality. |
| Z22 | Native Stage3 transfer A->populated B->C: multiple policy dates/ties, accepted old/new terms, terminal histories, several series/exceptions/cancelled anchors and all four receipt families. Stop source and import unchanged opaque object with hashes/tokens privately. Full known structural equality, ordering/identities/timestamps, old immutable receipts and pending retry; old destination credentials/receipts removed. Repeated import restores snapshot after changes; invalid imports rollback; reset clears every new artifact. Coordinated export versus series/batch/publication yields complete before/after records+histories+counters+receipts, never torn generations. |
| Z23 | Cumulative browser product under policies: authoritative availability changes from original detail capacities/hours, labels still correct; all single/pair grid/form/confirmation/lookup hooks and Stage2 races/conflict preservation/exact lost-response retry work. Public browsing, sessiondisplay/logout, signed-out selection, successful unchanged resubmit and field-change new key. At375CSSpx and desktop, keyboard/focus/visible labels/contrast/no horizontal page scroll and distinct available/unavailable/selected/loading/success/refused/uncertain states with bundled offline assets. Native history/explain/series controls are optional, not new screens required by contract. |
| Z24 | Release/evidence audit: exact Stage2 formalACCEPT plus committed copied baseline precedes any Stage3 production. Exact integrated Stage3 Docker build/HTTP/browser/portable transfer evidence includes all inherited/new CRITICAL/HIGH obligations and concrete failure attribution. Formal independent verifier verdict on that FULL SHA; official pass counts alone insufficient. Confirm canonical ledger commit only owned sanitized path, index serialized and release complete. Freeze accepted prior-stage source/evidence. |


## Upgrade and historical-continuity matrix

All sources/destinations are independently built from recorded exact FULL SHAs. Populate state before export, import the unchanged private wrapper into a separately started destination, and make the source unavailable. A clean-fixture substitute is not a migration test.

| Path | Required retained truth and exercised interactions | Procedures |
|---|---|---|
| Accepted Stage1 -> Stage3 | Hashed login, multiple valid tokens, fixture timezone/hours/grid/duration/cutoff/capacities/order, current single identities/statuses/timestamps, original create/batch parsed bodies/responses, failed keys reusable. Initialize only missing policy0 accepted baseline/revision; own old reference lookup and eligible imported anchor adoption. Historic receipt stays table_id-only and lacks fields not originally returned. | V18,V19,Z21 |
| Independently accepted Stage2 -> Stage3 | All preceding truth plus combinable order, pair member selections/occupancy, confirmed/cancelled singles/pairs and exact original Stage2 receipt shape. Adopt an eligible imported pair, preserve anchor known state, and generate policy0 native occurrence history. | W19,Z21 |
| Stage1 -> Stage2 -> Stage3 | Cumulative forward upgrade must not lose earlier exact receipts/tokens/references during either transfer. Replay both original Stage1 create/batch receipts through final destination, including values ignored by endpoints and numeric JSON identity. | W18,W19,Z21 |
| Retained browser client during completed upgrade | Existing sign-in, reference lookup, form values and unchanged pending key/body remain usable; original legacy single or Stage2 pair lost-response retry returns server-authoritative original reference/JSON without reload/new screen. Current destination API metadata never enriches the historical receipt or reconstructs its body. | W04,W07,W18,Z21,Z23 |
| Stage3 -> Stage3 -> Stage3 | Native immutable policies/version/publication order/effective-date selection, accepted snapshots/end times, contiguous histories/resulting revisions, membership/index/reference/exception truth, explicit restaurant and series counters, hashes/tokens and all four receipt families. Replays after later changes remain original, no effects. | V17..20,Z20,Z22 |
| Populated destination replacement/repetition/reset | Import removes destination-only users/tokens/config/reservations/receipts/policies/histories/series; repeated import restores exactly the snapshot after intervening changes without duplication. Invalid import rollback includes all new state; reset clears imported old/new generations. | V02,V19,V20,Z22 |

Publication-only bounds (grid/duration1..1440, cutoff0..10080, capacities1..100) do not retroactively restrict Stage1 fixtures, legacy exports or already accepted policy0 terms. Fixture/legacy configuration continues to follow its original contract. A policy0 duration/capacity larger than newly published bounds remains faithfully retained and can affect adoption/occupancy; native publication still enforces its bounds.

Missing legacy manager lists default[]; no role-management endpoint or manager privilege is invented to enable a test. Fresh Stage3 manager fixtures support publication tests; populated legacy adoption can use retained policy0. Native Stage3 snapshots preserve known manager lists. Transport compatibility is acceptance of the unchanged opaque format1 export, not a required exposed internal schema.

## Ambiguities and adopted reasoned interpretations

| Topic | Interpretation and verification limit |
|---|---|
| Authority/missing handoff blocks | Corrected complete handoff d6a86c65 and Conductor confirmation d603d79b-c3e1-433f-a23a-73a6cb22995a explicitly authorize independently read local Stage1+2+3 files. Earlier literal undefined blocks add no contract. |
| Restaurant revision before Stage4 | Stage3 explicitly requires adoption+1 per whole operation and collective real batch+1 per whole batch, failure/replay0. Initial value, public counter endpoint and general increments for create/cancel/policy/PATCH are not specified here. Record/verifiably observe only these deltas/retained state; source inspection is acceptable when no public view exists. Do not import Stage4 definitions backwards or create a missing-endpoint blocker. |
| All-no-op batch and unaffected series | Wording “restaurant revision increases once for the whole batch” does not explicitly exclude a wholly no-op batch. Conductor adopts unchanged counters for all-no-op batch and a series listed only with unchanged items. A batch with actual changes increments the restaurant once and each series with actual changed members once. Successful no-op receipt still exists. TK3-BATCH-17..18 represent adopted interpretation; ambiguity remains documented, not hidden. |
| Missing legacy revision/accepted terms | Conductor adopts revision1 and policy0 baseline only when missing; preserve any existing history, timestamps, identities, status and original receipt exactly. A native Stage3 record's actual existing revision/terms/history must never reset. Policy0 baseline may have no authority to reconstruct historical edits that older stages did not retain. |
| Legacy/seed history initialization | Exact recipe for initial history of an imported older amended/cancelled record, or a seed carrying cancelled status at revision1, is unspecified. Chosen analysis baseline: retain existing history if present; otherwise establish a documented current known-state baseline under revision1/policy0 without claiming unseen events or inventing event timestamps. Source owner documents the precise stored baseline and verifier checks preservation/adoption plus future native entries. Exact seq/event reconstruction of unknown past is not a blocker. Native Stage3 creation/change/cancel sequence/terms/terminal rules remain binding for new events; any future event numbering follows the stored documented baseline. |
| Old receipt versus new response enrichment | Run-adopted rule preserves exact original successful response JSON, including absent table_ids/revision/terms. New/current representations use current fields; accepted-history snapshots native to their recorded event never receive newer terms. Browser accepts legacy single selection receipt and resolves human labels from matching restaurant config. |
| Table sets versus receipt bodies | Unordered pair semantics normalize to declared combination order for current seating/history/no-op detection. Full parsed JSON body is compared first for receipt identity; reversed arrays are different bodies. Unknown fields and precise numeric values also participate in equality though ignored for effects. Pair presence does not insert an unchanged selection field into a party-only history event; actual-field-only rule still applies. |
| Integer JSON values | A boolean is never an integer. JSON body numeric values with exact integral value use integer semantics; Stage1's plain-decimal-digit restriction applies only to query parameters. Equivalent numeric encodings compare as parsed JSON values; avoid floating-point overflow/rounding in ignored fields or original receipts. Token-level digit-only restrictions for body fields would add an unstated constraint. |
| Unbounded exact combined-capacity output versus finite budgets | Stage1/2 fixture capacities and retained policy0 lack an upper bound. For capacities 10^N and1, the exact summed JSON number has N+1 significant decimal digits: its final1 prevents trailing-zero/exponent compression. Thus 1e1000000000+1 needs at least1,000,000,001 digit bytes, and arbitrary N yields unbounded output work under fixed5s/2CPU/2GiB limits. Streaming can reduce buffering, but cannot remove the output-length lower bound; the particular billion-digit example alone does not prove a mandatory memory failure. Equal large exponents may remain compact. No numeric upper bound, rounding permission or resource-error code is stated. Conductor adopted the resource-feasibility interpretation in489b5773-8c50-4449-8659-228e1fda76e1: retain exact arithmetic/output with no unsupported numeric range or silent rounding, exercise large feasible disparate-exponent sums/capacity thresholds using an independent exact oracle under the actual request budget, and report observed bounds honestly. The mathematically unbounded output domain remains a known specification/resource boundary, not a claim of unlimited performance or permission to reject valid compact JSON. Feasible-case correctness stays fully binding; frozen prior evidence is not reopened. Stage3 published capacity1..100 bounds new policies only, not imported/fixture policy0. Independently verify feasible mixed sums such as1e309+1 (310 significant digits), equal large-exponent compact sums, full-body equality/receipt transfer and ordinary latency; do not confuse ignored compact numeric fields with intrinsically expanded exact sums. |
| Invalid complete policies | Endpoint-specific “Invalid policy is422” governs recognized policy field type/value/range/shape errors, including booleans; truly unparseable/nonobject JSON retains Stage1 malformed_request400 parsing rule. Wrong types on unrelated ordinary fields retain ordinary400 unless specifically overridden. Verifier isolates gross parsing from recognized invalid policy and records this reasoned interpretation. |
| Competing error priorities | Explicit replay-before-current-resource, stale-before-cutoff/changes, accepted-cutoff-before-real-change-validation, batch input-order/nonoccupancy-before-overlap and first failing generated index are binding. Cancelled-versus-stale, unknown restaurant-versus-invalid-policy and unrelated adoption anchor-versus-count errors have no total ranking specified. Don't create blocking priorities unsupported by text. |
| Without explain “Stage1 shape” | Cumulative Stage2 available_options continues to apply; phrase forbids explanation fields unless true, rather than removing inherited pair options. Explain remains single-table rule reporting; no pair-explanation API is specified. |
| Time/DST business boundaries | Absolute duration and first repeated occurrence remain binding for selected/accepted policies and calendar recurring dates. Resolve repeated opening/closing boundaries consistently using first occurrence as the adopted prior-stage interpretation. Gap-valued opening/closing business boundaries remain unspecified; do not impose an invented mandatory schedule policy. Generated out-of-representable-range dates must fail cleanly without partial state or5xx; verify representable dates/ordinary date formats. |
| Series exceptions and cancellation | Permanent true exception survives later cancellation; cancellation alone does not newly mark an exception. No operation resets a diner exception just because fields return to initial values. Adoption changes only linkage/new agreement and new occurrences, never anchor booking/history/revision/receipt. No collective series-edit API or UI is invented. |
| Counter observability and no retroactive records | Explicit counter obligations can require independent source/state inspection when Stage3 has no public counter endpoint. Opaque export content is private, not repository evidence. Report sanitized comparison outcomes only. No speculative schema, historical event fabrication or Stage4 API requirement substitutes for concrete Stage3 behavior. |

## Acceptance criteria coverage and evidence safety

Audited inventory: **557 atomic obligations = 338 inherited + 219 new**; **249 CRITICAL, 285 HIGH, 23 MEDIUM**; **64 independent procedures = V01..V20 + W01..W20 + Z01..Z24**. All inherited IDs are retained once; new IDs, referenced dependencies and procedure mappings resolve without duplicates or missing references. This checks ledger integrity, not production behavior. The 534 CRITICAL/HIGH obligations are the blocking acceptance set, qualified by explicit adopted interpretations and unspecified boundaries above.

The ledger contains one canonical cumulative record per stable requirement ID. All statuses remain OPEN / Stage3 unverified; no implementation has been reviewed or accepted by this analysis seat. Every CRITICAL/HIGH obligation requires independently observed evidence on one exact integrated Stage3 FULL production SHA, or explicit defensible source inspection for hashing/internal counter invariants. Execute all 64 V/W/Z procedures with sufficient distinct cases to close their mapped obligations; procedure counts and visible pass counts alone never prove closure. Every case records expected/observed status/code/JSON or rendered behavior, SHA, independent oracle and sanitized trace reference. Where a procedure covers multiple boundaries, trace each atomic row to the cases exercising it. Official checks remain evidence, not the sole contract or a replacement for unrepresented C/H cases.

Formal release requires Stage2 independent ACCEPT, committed copied Stage3 baseline, scoped production delivery under Stage3 only, all inherited and new blocking obligations addressed and an independent verifier formal exact-SHA verdict. Analysis evidence, owner tests, previous-stage acceptance and a “ready” message never substitute. No Stage3 production begins from this ledger handoff alone.

Sanitize the single owned evidence file before commit: no credentials, actual passwords/tokens, session dumps, opaque export payloads, raw environments, caches or logs. Synthetic table/date/reference labels illustrate independent procedures only. Stage1 accepted source/evidence and the official kickoff/spec/harness/shipped checks remain read-only. Stage2 implementation/browser/verifier paths belong to their seats and are never staged by the auditor. Stage3 evidence commit stages only evidence/stage-3/requirements.md after serialized index-window authorization; report FULL evidence SHA/path/counts, then release index and close board#9.
