# Tablekeeper Stage 4 cumulative atomic requirements and risk ledger

This is the ONE canonical Stage 4 analysis ledger for the FINAL SUBMISSION RUN, owned only at D:\dark\band-work\result\evidence\stage-4\requirements.md. Authoritative complete cumulative handoff f3d1689c-dcbf-4c59-8a52-451c06ddfb5a supplies all Stage 1..4 contracts. All contracts were independently read and reconciled with read-only local official files; existing product source/API documentation/schema and visible checks never define the contract.

Official read-only repository FULL803560d2a678ace1414465c098eb0ab5380ffade, clean specs under D:\dark\dark-factory-wearedevs\tablekeeper\spec. SHA256 stage-1.md3b53451d4ad2b1e12765c97fd8bdff3fce20d56b6969a049c84e0bc302daf2cbd; stage-2.md192909e9f784e2e2849c996db1b5e86107bbbf7001f5cb31427dba69421d9abf; stage-3.md73629edfd9b38d6671eef00974e6bcb95e39171e9ed10767a57840a6ea778528; stage-4.md8bc6c784ecb8b1dda6e68aaab5d642415c280fe219b83fd53fabb8987c2e2510.

Accepted Stage 1 production d41a7627711951a07ce7a1718fac47c6ea5b6dd4 and formal evidence e4a923e5fda0857e9e28221e92ff0bcfb49641a4 remain frozen. Canonical inherited Stage 3 analysis429c365ae5e36a02883d10d36efed26dcc32a6fa contains557 obligations/64 procedures. Stage 2/3 production acceptance is pending at assignment time. No Stage 4 production begins before Stage 3 independent ACCEPT and a separately committed copy of its complete service. This ledger neither implements nor accepts any production.

## Record schema ownership status and evidence

Each row supplies stable requirement ID, authoritative section, atomic behavioral obligation, risk/tags, dependencies, owner where explicit, independent procedure and compatibility duty. All557 inherited IDs are retained exactly once; semantic specialization is limited to the current Stage 4 cumulative ledger. Earlier frozen/complete ledgers are untouched. All rows default **OPEN / Stage 4 unverified**, visible-check coverage **UNKNOWN (not inspected)**, evidence reference **NONE**. A future closure requires exact integrated Stage 4 FULL SHA, independent case/observed result and sanitized evidence reference. Historical release rows retain their stage-local meaning and provenance, rather than instructing this seat to repeat past work.

C=CRITICAL core invariant/state/privacy/history/release risk; H=HIGH externally visible correctness/compatibility risk; M=MEDIUM narrower protocol/usability risk. Tags TX atomicity/rollback, CC serialization/races, RP replay/body identity, AU permission/privacy, TM instant/calendar/DST/cutoff, VA shape/type/value, OR precedence/deterministic ordering, ST portable state, HT historical truth/revisions, UI browser behavior, QA rendered quality, DEP offline deployment, HTTP protocol, SC scope/gates, OPT exact optimization. Dependencies in original TK1 rows abbreviate TK1 IDs/ranges; later rows use full IDs.

Production owner S=Systems Engineer backend/container/docs; E=Experience Engineer browser assets; C=Conductor release coordination; S/E=interface boundary. TK1 owner defaults S except CON annotations. Independent verifier owns executable oracles, coverage evidence and formal exact-SHA verdict. Auditor owns only this ledger and performs no production implementation/acceptance. Compatibility S=identity/config/status/timestamps/state, R=full parsed request bodies/exact original receipt JSON, B=retained browser session/form/reference/retry, H=immutable policies/accepted snapshots/history/revisions, A=series membership/original schedules/exceptions/counters, P=plans/applied flags/closures/captured restaurant revisions. Combined letters accumulate.

V01..20/W01..20/Z01..24 retain their independent obligations; P01..24 add Stage 4 procedures. Tests use synthetic dates/IDs/labels only; private credentials and opaque snapshots never become evidence. Exact feasible numeric arithmetic/output remains binding. Conductor-adopted unbounded output-size/resource boundary489b5773-8c50-4449-8659-228e1fda76e1 is a documented limitation, not an invented numeric limit, rounding permission or unlimited-performance claim.

## Current specialization and feature boundaries

| Inherited obligations | Stage 4 specialization or retained boundary |
|---|---|
| TK1-SC-04 | Assigned cumulative Stage 4 folder only; separate copied baseline and exact-SHA verdict gates. |
| TK1-IDEM-01; TK1-ERR-09 | Seven write families, including distinct preview/apply/full-plan paths and series amend; full parsed body identity before table-set normalization remains binding. |
| TK1-AV-08; TK2-OPTIONS-06; TK3-EXPL-04 | Applied closure on any member is an occupancy exclusion, including no_overlap=false explanations; half-open instant semantics. |
| TK3-TERMS-13..19 | Real diner writes use old accepted cutoff/new resulting policy. Operator repairs bypass cutoff and retain accepted terms/times. Ordinary individual/batch no-ops retain their old eligibility rules; series-amend no-ops use its explicit real-change-only cutoff wording. |
| TK3-HIST-14; TK3-SERIES-05..14 | Ordinary diner changed history/exception rules remain. Operator reassigned history always uses table_ids plus plan_id; repairs and collective agreement amendments preserve exception flags and original schedule dates. |
| TK3-UP-12; TK3-UP-16; TK3-UP-18 | Current general restaurant counters, closure/plan/receipt state and current browser reflection added; no retroactive Stage 4 semantics in earlier accepted services. |
| TK1-IDEM-08..14; TK3-TERMS-08; TK3-UP-13..15 | Historical original JSON stays exact, including missing later fields; legacy known history/identity/timestamps preserved and unknown events never fabricated. |
| TK3-GATE-01..03 | Inherited Stage 3 release obligations remain historical/preceding gates; active Stage 4 gates are new TK4-GATE rows. |

Original restaurant detail remains fixture configuration. Planning uses each reservation's own accepted capacities and retained interval, while new diner changes/availability use date-effective policies. Manager plan responses legitimately cover all considered restaurant bookings; ordinary foreign private lookup/history/decision remains404. No new plan/closure GET API, manager browser screen, polling/live updates, crash persistence, downgrade compatibility or role-management endpoint is invented.

## Active inherited Stage 1 atomic requirements

### Scope delivery and runtime

| ID | Source | Atomic requirement | Risk/tags | Dependencies | Verify | Compat |
|---|---|---|---|---|---|---|
| TK1-SC-01 |§1 + Stage 2 | Expose the required HTTP API; Stage 2 additionally requires the specified browser screens. | M SC | - | V01 | - |
| TK1-SC-02 | Intro | Do not use source code from existing products in this domain. Owner CON. | H SC | - | V01 | - |
| TK1-SC-03 | Intro | Do not use existing domain-product API documentation or schemas. Owner CON. | H SC | - | V01 | - |
| TK1-SC-04 |Assignment + Stage 2 + Stage 3 + Stage 4 | Assigned Stage 4 folder implements cumulative Stages 1, 2, 3 and 4 only. Owner CON. | H SC | - | V01 | - |
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
| TK1-ERR-09 |§5 + Stage 3 + Stage 4 | A nonempty Idempotency-Key exceeding 255 characters is 422 validation_failed on all seven required-key write families. | H VA RP | ERR-05 | V06 | - |
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
| TK1-IDEM-01 |§7 + Stage 3 + Stage 4 | Create, moves, policy publication, series adoption, replan preview, replan application and series amendment require Idempotency-Key under the same user/method/full-path/full-body rules. | H RP HTTP | AUTH-11 | V06 | - |
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
| TK1-AV-08 |§8 + Stage 2 + Stage 4 | Available single tables have no overlapping confirmed reservation containing that member and no overlapping applied closure. | C TX TM | OCC-01,OCC-02 | V08,V16 | S |
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
| TK2-OPTIONS-06 |Availability API + Stage 4 | Options require no overlapping confirmed occupancy or applied closure on any member. | C TX HTTP | TK2-PAIR-07,TK1-AV-08 | S | W11,W16 | - |
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

## Active inherited Stage 3 atomic requirements

### TK3-EXPL: Availability explanations

| ID | Source | Atomic requirement | Risk/tags | Dependencies | Owner | Verify | Compat |
|---|---|---|---|---|---|---|---|
| TK3-EXPL-01 | Stage 3 Availability explanations | Optional explain accepts only literal query value true; every other supplied value, including empty, false and 1, returns 422 validation_failed. | H VA HTTP | TK1-ERR-05 | S | Z01,Z02 | S/H |
| TK3-EXPL-02 | Stage 3 Availability explanations | Omitted explain adds no explanation fields; cumulative Stage 2 available_options remains present. | H HTTP ST | TK2-OPTIONS-01 | S | Z01,Z02 | S/H |
| TK3-EXPL-03 | Stage 3 Availability explanations | Capacity rule independently evaluates party_size against the selected policy capacity for that single table. | H VA HT | TK3-POL-11 | S | Z01,Z02 | S/H |
| TK3-EXPL-04 |Stage 3 Availability explanations + Stage 4 | No_overlap independently evaluates the candidate selected-policy interval against retained confirmed occupancy and applied closures on that table. | C TX TM HT | TK1-OCC-01,TK3-TERMS-09 | S | Z01,Z02 | S/H |
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
| TK3-TERMS-13 |Stage 3 Policies and accepted terms: snapshots + Stage 4 | A real diner amendment checks the old accepted cutoff first; operator seating repairs are explicitly exempt. | C OR TM | TK1-PATCH-04 | S | Z06,Z07,Z08 | S/R/H |
| TK3-TERMS-14 |Stage 3 Policies and accepted terms: snapshots + Stage 4 | A real diner amendment validates all resulting fields against the policy for the resulting local start date; operator repairs retain accepted terms. | C TM VA HT | TK3-TERMS-13,TK3-POL-11 | S | Z06,Z07,Z08 | S/R/H |
| TK3-TERMS-15 | Stage 3 Policies and accepted terms: snapshots | A real amendment atomically replaces accepted_terms with the entire resulting selected policy. | C TX HT | TK3-TERMS-14 | S | Z06,Z07,Z08 | S/R/H |
| TK3-TERMS-16 | Stage 3 Policies and accepted terms: snapshots | A real amendment atomically recomputes end time using the newly accepted absolute duration. | C TX TM | TK3-TERMS-15,TK1-TIME-05 | S | Z06,Z07,Z08 | S/R/H |
| TK3-TERMS-17 | Stage 3 Policies and accepted terms: snapshots | A real amendment increments reservation revision exactly once. | C HT TX | TK3-TERMS-15 | S | Z06,Z07,Z08 | S/R/H |
| TK3-TERMS-18 | Stage 3 Policies and accepted terms: snapshots | A no-op retains accepted_terms, end time and revision, even if a newer policy would reject the old fields. | C HT TM | TK3-TERMS-09 | S | Z06,Z07,Z08 | S/R/H |
| TK3-TERMS-19 |Stage 3 Policies and accepted terms: snapshots + Stage 4 | Ordinary individual PATCH/move no-ops still require confirmed editable bookings and accepted cutoff compliance; Stage 4 series-amend no-ops follow its real-change-only cutoff rule. | H TM OR | TK3-TERMS-12 | S | Z06,Z07,Z08 | S/R/H |
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
| TK3-HIST-14 |Stage 3 Reservation history and resulting snapshots + Stage 4 | Ordinary changed selection uses table_id for single-to-single and table_ids if a pair is involved; Stage 4 reassigned selection always uses table_ids. | H HT | TK3-PAIRHIST-02,TK3-PAIRHIST-04 | S | Z07,Z10,Z11 | S/H |
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
| TK3-UP-12 |Stage 3 Recurring reservations and cumulative export import + Stage 4 | Transfer preserves known inherited restaurant revisions; Stage 4 general revision deltas apply after upgrade without retrocomputing unknown earlier operations. | C ST HT | TK3-ADOPT-41,TK3-BATCH-11 | S | Z21,Z22,Z23,W14,W15 | S/R/B/H/A |
| TK3-UP-13 | Stage 3 Recurring reservations and cumulative export import | Legacy import preserves identities, existing timestamps, statuses, original receipts and any existing history exactly. | C ST HT RP | TK3-UP-01,TK3-UP-02 | S | Z21,Z22,Z23,W14,W15 | S/R/B/H/A |
| TK3-UP-14 | Stage 3 Recurring reservations and cumulative export import | Missing legacy reservation revision/accepted-terms initializes revision 1 and policy-0 baseline under adopted interpretation. | C ST HT | TK3-TERMS-07,TK3-UP-13 | S | Z21,Z22,Z23,W14,W15 | S/R/B/H/A |
| TK3-UP-15 | Stage 3 Recurring reservations and cumulative export import | Legacy history baseline does not invent unobserved edits or event timestamps; verify chosen baseline plus truthful future native entries. | H ST HT | TK3-UP-13,TK3-HIST-18 | S | Z21,Z22,Z23,W14,W15 | S/R/B/H/A |
| TK3-UP-16 |Stage 3 Recurring reservations and cumulative export import + Stage 4 | Reset clears policies, histories, series, counters, closures, stored plans/applied flags and all old/new receipts as well as inherited state. | C TX ST RP | TK1-FIX-02,TK1-XFER-20 | S | Z21,Z22,Z23,W14,W15 | S/R/B/H/A |
| TK3-UP-17 | Stage 3 Recurring reservations and cumulative export import | Import still replaces all destination data and credentials, repeats restore the snapshot, and invalid import changes nothing. | C TX ST AU | TK1-XFER-06,TK1-XFER-07,TK1-XFER-08,TK1-XFER-11 | S | Z21,Z22,Z23,W14,W15 | S/R/B/H/A |
| TK3-UP-18 |Stage 3 Recurring reservations and cumulative export import + Stage 4 | No new history/explanation/operator/series-management screen is required; cumulative existing browser screens reflect applied plans on subsequent authoritative reads. | H UI | TK2-WEB-01,TK3-EXPL-02 | S | Z21,Z22,Z23,W14,W15 | S/R/B/H/A |

### TK3-GATE: Final submission assignment

| ID | Source | Atomic requirement | Risk/tags | Dependencies | Owner | Verify | Compat |
|---|---|---|---|---|---|---|---|
| TK3-GATE-01 | Stage 3 Final submission assignment | Stage 3 production starts only after independent Stage 2 ACCEPT and a committed copied baseline. | C SC ST | TK2-GATE-01 | C | Z24 | - |
| TK3-GATE-02 | Stage 3 Final submission assignment | Stage 3 acceptance requires independent formal verdict on the exact integrated production FULL SHA. | C SC | TK3-GATE-01 | C | Z24 | - |
| TK3-GATE-03 | Stage 3 Final submission assignment | Only the canonical owned sanitized Stage 3 ledger path is committed during the serialized evidence window. | H SC | - | C | Z24 | - |

## New Stage 4 atomic requirements

### TK4-RREV

| ID | Source | Atomic requirement | Risk/tags | Dependencies | Owner | Verify | Compat |
|---|---|---|---|---|---|---|---|
| TK4-RREV-01 | Stage 4 Seating changes after a table closure | After reset each restaurant revision is0, including restaurants with seeded reservations. | C HT ST | TK1-FIX-02 | S | P01,P09,P17,P21 | S/H/P/A |
| TK4-RREV-02 | Stage 4 Seating changes after a table closure | Each successful new ordinary booking increments its restaurant revision once. | C HT TX | TK1-CREATE-01 | S | P01,P09,P17,P21 | S/H/P/A |
| TK4-RREV-03 | Stage 4 Seating changes after a table closure | Each real individual diner amendment increments its restaurant revision once. | C HT TX | TK3-TERMS-17 | S | P01,P09,P17,P21 | S/H/P/A |
| TK4-RREV-04 | Stage 4 Seating changes after a table closure | First successful cancellation increments its restaurant revision once; repeated cancellation does not. | C HT TX | TK3-REV-01,TK3-REV-02 | S | P01,P09,P17,P21 | S/H/P/A |
| TK4-RREV-05 | Stage 4 Seating changes after a table closure | Each successful new policy publication increments its restaurant revision once. | C HT TX | TK3-POL-05 | S | P01,P09,P17,P21 | S/H/P/A |
| TK4-RREV-06 | Stage 4 Seating changes after a table closure | First successful plan application increments restaurant revision once for the whole plan. | C HT TX | TK4-APPLY-16 | S | P01,P09,P17,P21 | S/H/P/A |
| TK4-RREV-07 | Stage 4 Seating changes after a table closure | A collective batch containing real changes increments restaurant revision once, not per moved booking. | C HT TX | TK3-BATCH-11 | S | P01,P09,P17,P21 | S/H/P/A |
| TK4-RREV-08 | Stage 4 Seating changes after a table closure | Series adoption retains its once-per-whole-operation restaurant increment. | C HT TX | TK3-ADOPT-41 | S | P01,P09,P17,P21 | S/H/P/A |
| TK4-RREV-09 | Stage 4 Seating changes after a table closure | Series amendment increments restaurant revision once if anything changed. | C HT TX | TK4-SERFX-04 | S | P01,P09,P17,P21 | S/H/P/A |
| TK4-RREV-10 | Stage 4 Seating changes after a table closure | No-op writes do not increment restaurant revision. | C HT | TK3-BATCH-17,TK3-TERMS-18 | S | P01,P09,P17,P21 | S/H/P/A |
| TK4-RREV-11 | Stage 4 Seating changes after a table closure | Failures do not increment restaurant revision. | C TX HT | TK3-BATCH-14 | S | P01,P09,P17,P21 | S/H/P/A |
| TK4-RREV-12 | Stage 4 Seating changes after a table closure | Replan previews do not increment restaurant revision. | C HT | TK4-PLAN-09 | S | P01,P09,P17,P21 | S/H/P/A |
| TK4-RREV-13 | Stage 4 Seating changes after a table closure | Successful replays do not increment restaurant revision. | C RP HT | TK1-IDEM-14 | S | P01,P09,P17,P21 | S/H/P/A |
| TK4-RREV-14 | Stage 4 Seating changes after a table closure | Restaurant revision is local: changes to another restaurant do not invalidate this restaurant's plan. | C CC HT | TK4-PLAN-01 | S | P01,P09,P17,P21 | S/H/P/A |

### TK4-PRE

| ID | Source | Atomic requirement | Risk/tags | Dependencies | Owner | Verify | Compat |
|---|---|---|---|---|---|---|---|
| TK4-PRE-01 | Stage 4 Seating changes after a table closure | POST /restaurants/{id}/replans requires restaurant-manager permission. | C AU | TK3-MGR-03 | S | P02,P03,P04 | S/R/H/P |
| TK4-PRE-02 | Stage 4 Seating changes after a table closure | An unauthenticated replan preview returns401 unauthenticated. | H AU HTTP | TK1-AUTH-11 | S | P02,P03,P04 | S/R/H/P |
| TK4-PRE-03 | Stage 4 Seating changes after a table closure | An authenticated non-manager replan preview returns403 forbidden. | H AU HTTP | TK3-MGR-04 | S | P02,P03,P04 | S/R/H/P |
| TK4-PRE-04 | Stage 4 Seating changes after a table closure | An unknown restaurant for preview returns404 not_found. | H HTTP | TK1-ERR-12 | S | P02,P03,P04 | S/R/H/P |
| TK4-PRE-05 | Stage 4 Seating changes after a table closure | Replan preview requires an idempotency key under the full Stage1 contract. | C RP | TK1-IDEM-01 | S | P02,P03,P04 | S/R/H/P |
| TK4-PRE-06 | Stage 4 Seating changes after a table closure | Preview body requires table_id, from and to. | H VA HTTP | TK1-ERR-04 | S | P02,P03,P04 | S/R/H/P |
| TK4-PRE-07 | Stage 4 Seating changes after a table closure | Unknown closure table at the restaurant returns404 not_found. | H HTTP | TK1-ERR-12 | S | P02,P03,P04 | S/R/H/P |
| TK4-PRE-08 | Stage 4 Seating changes after a table closure | Closure instants require explicit offsets; invalid interval gives422 validation_failed. | H VA TM | TK1-ERR-05 | S | P02,P03,P04 | S/R/H/P |
| TK4-PRE-09 | Stage 4 Seating changes after a table closure | Closure from must be strictly earlier than to as instants. | H VA TM | TK4-PRE-08 | S | P02,P03,P04 | S/R/H/P |
| TK4-PRE-10 | Stage 4 Seating changes after a table closure | The proposed closure interval is half-open [from,to). | C TM TX | TK1-OCC-02 | S | P02,P03,P04 | S/R/H/P |
| TK4-PRE-11 | Stage 4 Seating changes after a table closure | Consider every confirmed booking at this restaurant overlapping the proposed interval, not just occupants of the closed table. | C OPT TX | TK4-PRE-10 | S | P02,P03,P04 | S/R/H/P |
| TK4-PRE-12 | Stage 4 Seating changes after a table closure | Other bookings remain fixed on their existing assignments. | C OPT TX | TK4-PRE-11 | S | P02,P03,P04 | S/R/H/P |
| TK4-PRE-13 | Stage 4 Seating changes after a table closure | Cancelled bookings are excluded from considered occupancy and planning. | C OPT TX | TK1-OCC-01 | S | P02,P03,P04 | S/R/H/P |
| TK4-PRE-14 | Stage 4 Seating changes after a table closure | Planning supports up to6 restaurant tables inclusive. | H OPT DEP | TK4-PRE-11 | S | P02,P03,P04 | S/R/H/P |
| TK4-PRE-15 | Stage 4 Seating changes after a table closure | Planning supports up to4 declared pairs inclusive. | H OPT DEP | TK4-PRE-11 | S | P02,P03,P04 | S/R/H/P |
| TK4-PRE-16 | Stage 4 Seating changes after a table closure | Planning supports up to6 considered bookings inclusive. | H OPT DEP | TK4-PRE-11 | S | P02,P03,P04 | S/R/H/P |
| TK4-PRE-17 | Stage 4 Seating changes after a table closure | Inputs above these limits may return422 planning_limit; in-range inputs cannot use this escape. | H OPT HTTP | TK4-PRE-14,TK4-PRE-15,TK4-PRE-16 | S | P02,P03,P04 | S/R/H/P |
| TK4-PRE-18 | Stage 4 Seating changes after a table closure | Each considered booking retains reference and owner through repair. | C HT AU | TK4-PRE-11 | S | P02,P03,P04 | S/R/H/P |
| TK4-PRE-19 | Stage 4 Seating changes after a table closure | Each considered booking retains party size through repair. | C HT VA | TK4-PRE-11 | S | P02,P03,P04 | S/R/H/P |
| TK4-PRE-20 | Stage 4 Seating changes after a table closure | Each considered booking retains start and end through repair. | C HT TM | TK4-PRE-11 | S | P02,P03,P04 | S/R/H/P |
| TK4-PRE-21 | Stage 4 Seating changes after a table closure | Each considered booking retains complete accepted_terms through repair. | C HT | TK4-PRE-11,TK3-TERMS-03 | S | P02,P03,P04 | S/R/H/P |
| TK4-PRE-22 | Stage 4 Seating changes after a table closure | Diner cancellation cutoffs do not prevent operator planning/application repair. | C TM AU | TK3-TERMS-13 | S | P02,P03,P04 | S/R/H/P |
| TK4-PRE-23 | Stage 4 Seating changes after a table closure | No booking disappears or becomes cancelled through a seating repair. | C TX HT | TK4-PRE-18 | S | P02,P03,P04 | S/R/H/P |

### TK4-OPT

| ID | Source | Atomic requirement | Risk/tags | Dependencies | Owner | Verify | Compat |
|---|---|---|---|---|---|---|---|
| TK4-OPT-01 | Stage 4 Seating changes after a table closure | Each considered booking may be assigned any single table or declared pair at its restaurant. | C OPT TX | TK4-PRE-11,TK2-PAIR-01 | S | P04,P05,P06,P07,P08 | S/H/P |
| TK4-OPT-02 | Stage 4 Seating changes after a table closure | Eligibility/capacity is evaluated under that booking's own accepted capacities, not a new/current policy. | C OPT HT VA | TK4-PRE-21 | S | P04,P05,P06,P07,P08 | S/H/P |
| TK4-OPT-03 | Stage 4 Seating changes after a table closure | Assigned capacity must be at least that booking's party size. | C OPT VA | TK4-OPT-02 | S | P04,P05,P06,P07,P08 | S/H/P |
| TK4-OPT-04 | Stage 4 Seating changes after a table closure | Pair capacity is the exact sum of its members' capacities in that booking's accepted_terms. | C OPT VA HT | TK4-OPT-02,TK2-PAIR-06 | S | P04,P05,P06,P07,P08 | S/H/P |
| TK4-OPT-05 | Stage 4 Seating changes after a table closure | Assignments must not conflict with fixed bookings on any member for their full retained intervals. | C OPT TX | TK4-PRE-12,TK4-PRE-20 | S | P04,P05,P06,P07,P08 | S/H/P |
| TK4-OPT-06 | Stage 4 Seating changes after a table closure | Assignments must not overlap each other on any member. | C OPT TX | TK1-OCC-01,TK4-PRE-20 | S | P04,P05,P06,P07,P08 | S/H/P |
| TK4-OPT-07 | Stage 4 Seating changes after a table closure | Assignments must not conflict with previously applied closures on any member. | C OPT TX | TK4-CLOSE-02,TK4-PRE-20 | S | P04,P05,P06,P07,P08 | S/H/P |
| TK4-OPT-08 | Stage 4 Seating changes after a table closure | Assignments must not conflict with the proposed closure on any member. | C OPT TX | TK4-PRE-10,TK4-PRE-20 | S | P04,P05,P06,P07,P08 | S/H/P |
| TK4-OPT-09 | Stage 4 Seating changes after a table closure | The primary objective minimizes number of considered bookings whose unordered table set changes. | C OPT OR | TK4-OPT-01 | S | P04,P05,P06,P07,P08 | S/H/P |
| TK4-OPT-10 | Stage 4 Seating changes after a table closure | Subject to minimal changes, minimize total unused seats across every considered booking using its own accepted capacities. | C OPT OR VA | TK4-OPT-02,TK4-OPT-09 | S | P04,P05,P06,P07,P08 | S/H/P |
| TK4-OPT-11 | Stage 4 Seating changes after a table closure | Subject to both preceding optima, minimize option-rank vector in ascending reservation-reference order lexicographically. | C OPT OR | TK4-OPT-09,TK4-OPT-10 | S | P04,P05,P06,P07,P08 | S/H/P |
| TK4-OPT-12 | Stage 4 Seating changes after a table closure | Option ranks start at0 with singles in fixture order. | H OPT OR | TK1-AV-09 | S | P04,P05,P06,P07,P08 | S/H/P |
| TK4-OPT-13 | Stage 4 Seating changes after a table closure | Pair option ranks follow all singles in declared-pair order, without re-ranking after capacity/closure filtering. | H OPT OR | TK2-OPTIONS-08,TK4-OPT-12 | S | P04,P05,P06,P07,P08 | S/H/P |
| TK4-OPT-14 | Stage 4 Seating changes after a table closure | Rank vector includes every considered booking, including unchanged assignments. | C OPT OR | TK4-OPT-11,TK4-PRE-11 | S | P04,P05,P06,P07,P08 | S/H/P |
| TK4-OPT-15 | Stage 4 Seating changes after a table closure | Pair member output order is declared combination order; set reversal alone does not count as a changed assignment. | H OPT OR HT | TK2-OPTIONS-09,TK3-PAIRHIST-06 | S | P04,P05,P06,P07,P08 | S/H/P |
| TK4-OPT-16 | Stage 4 Seating changes after a table closure | No feasible plan returns409 no_feasible_plan with no plan, closure, booking/history/revision or successful receipt mutation. | C OPT TX RP | TK4-OPT-05,TK4-OPT-06,TK4-OPT-07,TK4-OPT-08 | S | P04,P05,P06,P07,P08 | S/H/P |

### TK4-PLAN

| ID | Source | Atomic requirement | Risk/tags | Dependencies | Owner | Verify | Compat |
|---|---|---|---|---|---|---|---|
| TK4-PLAN-01 | Stage 4 Seating changes after a table closure | Successful preview returns201 with opaque plan_id and captured restaurant_revision. | H HTTP HT | TK4-PRE-05,TK1-HTTP-05 | S | P03,P08,P09,P19 | S/R/H/P |
| TK4-PLAN-02 | Stage 4 Seating changes after a table closure | Preview response carries the proposed closure table/from/to. | H HTTP TM | TK4-PRE-06 | S | P03,P08,P09,P19 | S/R/H/P |
| TK4-PLAN-03 | Stage 4 Seating changes after a table closure | Preview assignments include every considered booking exactly once. | H HTTP OR | TK4-PRE-11 | S | P03,P08,P09,P19 | S/R/H/P |
| TK4-PLAN-04 | Stage 4 Seating changes after a table closure | Assignments are in ascending reference order. | H OR | TK4-PLAN-03 | S | P03,P08,P09,P19 | S/R/H/P |
| TK4-PLAN-05 | Stage 4 Seating changes after a table closure | Each assignment carries reference, normalized table_ids and truthful changed flag. | H HTTP OPT | TK4-OPT-09,TK4-OPT-15 | S | P03,P08,P09,P19 | S/R/H/P |
| TK4-PLAN-06 | Stage 4 Seating changes after a table closure | moved_count equals the number of changed assignments. | H HTTP OPT | TK4-PLAN-05 | S | P03,P08,P09,P19 | S/R/H/P |
| TK4-PLAN-07 | Stage 4 Seating changes after a table closure | unused_seats is the exact total accepted-capacity-minus-party objective value. | H HTTP OPT VA | TK4-OPT-10 | S | P03,P08,P09,P19 | S/R/H/P |
| TK4-PLAN-08 | Stage 4 Seating changes after a table closure | Preview stores a plan and its successful original receipt without recording a closure or changing occupancy. | C TX RP ST | TK4-PRE-05,TK4-OPT-16 | S | P03,P08,P09,P19 | S/R/H/P |
| TK4-PLAN-09 | Stage 4 Seating changes after a table closure | Preview changes no reservation revision or history. | C HT TX | TK4-PLAN-08 | S | P03,P08,P09,P19 | S/R/H/P |
| TK4-PLAN-10 | Stage 4 Seating changes after a table closure | Preview response/captured assignments remain immutable original receipt values after later restaurant changes or application. | C HT RP | TK1-IDEM-13,TK4-PLAN-01 | S | P03,P08,P09,P19 | S/R/H/P |

### TK4-APPLY

| ID | Source | Atomic requirement | Risk/tags | Dependencies | Owner | Verify | Compat |
|---|---|---|---|---|---|---|---|
| TK4-APPLY-01 | Stage 4 Seating changes after a table closure | POST /restaurants/{id}/replans/{plan_id}/apply requires a manager. | C AU | TK4-PRE-01 | S | P10,P11,P12,P13,P19 | S/R/H/P/A |
| TK4-APPLY-02 | Stage 4 Seating changes after a table closure | Apply requires an idempotency key and normal Stage1 full-path/body replay rules. | C RP | TK1-IDEM-01 | S | P10,P11,P12,P13,P19 | S/R/H/P/A |
| TK4-APPLY-03 | Stage 4 Seating changes after a table closure | Apply accepts a JSON object body{}; unknown fields remain ignored for effects and part of receipt identity. | H VA RP | TK1-HTTP-03,TK1-IDEM-11 | S | P10,P11,P12,P13,P19 | S/R/H/P/A |
| TK4-APPLY-04 | Stage 4 Seating changes after a table closure | First successful application returns201 with plan_id, resulting restaurant_revision and reservations. | H HTTP | TK4-APPLY-02 | S | P10,P11,P12,P13,P19 | S/R/H/P/A |
| TK4-APPLY-05 | Stage 4 Seating changes after a table closure | Application reservations include every considered booking in reference order, including unmoved ones. | H HTTP OR | TK4-PLAN-03,TK4-PLAN-04 | S | P10,P11,P12,P13,P19 | S/R/H/P/A |
| TK4-APPLY-06 | Stage 4 Seating changes after a table closure | An unknown plan returns404 not_found. | H HTTP | TK1-ERR-12 | S | P10,P11,P12,P13,P19 | S/R/H/P/A |
| TK4-APPLY-07 | Stage 4 Seating changes after a table closure | A plan belonging to another restaurant returns404 not_found. | C AU HTTP | TK4-APPLY-06 | S | P10,P11,P12,P13,P19 | S/R/H/P/A |
| TK4-APPLY-08 | Stage 4 Seating changes after a table closure | Any intervening revision at the plan's restaurant gives409 stale_plan and changes nothing. | C CC HT TX | TK4-PLAN-01,TK4-RREV-02 | S | P10,P11,P12,P13,P19 | S/R/H/P/A |
| TK4-APPLY-09 | Stage 4 Seating changes after a table closure | A closure or other revision-changing operation at another restaurant does not invalidate the plan. | C CC HT | TK4-RREV-14 | S | P10,P11,P12,P13,P19 | S/R/H/P/A |
| TK4-APPLY-10 | Stage 4 Seating changes after a table closure | An already applied plan under a different key returns409 plan_already_applied. | C RP HT | TK4-APPLY-02 | S | P10,P11,P12,P13,P19 | S/R/H/P/A |
| TK4-APPLY-11 | Stage 4 Seating changes after a table closure | Already-applied detection precedes staleness for a different key under the reasoned interpretation. | C OR RP | TK4-APPLY-10,TK4-APPLY-08 | S | P10,P11,P12,P13,P19 | S/R/H/P/A |
| TK4-APPLY-12 | Stage 4 Seating changes after a table closure | Successful-key replay returns200 with the original application response even after later changes. | C RP HT | TK1-IDEM-13 | S | P10,P11,P12,P13,P19 | S/R/H/P/A |
| TK4-APPLY-13 | Stage 4 Seating changes after a table closure | Receipt resolution precedes already-applied/stale/current-state checks; differing used-key body remains409 idempotency_key_reuse. | C OR RP | TK1-IDEM-05,TK1-IDEM-06,TK1-IDEM-10 | S | P10,P11,P12,P13,P19 | S/R/H/P/A |
| TK4-APPLY-14 | Stage 4 Seating changes after a table closure | Application records the closure and every assignment atomically. | C TX CC | TK4-PLAN-08 | S | P10,P11,P12,P13,P19 | S/R/H/P/A |
| TK4-APPLY-15 | Stage 4 Seating changes after a table closure | Each moved booking increments its revision exactly once. | C HT TX | TK4-PLAN-05 | S | P10,P11,P12,P13,P19 | S/R/H/P/A |
| TK4-APPLY-16 | Stage 4 Seating changes after a table closure | The restaurant increments its revision once for the whole first application, even when no booking moves. | C HT TX | TK4-APPLY-14 | S | P10,P11,P12,P13,P19 | S/R/H/P/A |
| TK4-APPLY-17 | Stage 4 Seating changes after a table closure | Each moved booking gains exactly one reassigned history entry. | C HT TX | TK4-APPLY-15 | S | P10,P11,P12,P13,P19 | S/R/H/P/A |
| TK4-APPLY-18 | Stage 4 Seating changes after a table closure | Reassigned entry contains a table_ids change with complete before/after lists, even for single-to-single moves. | C HT HTTP | TK4-APPLY-17,TK3-HIST-12 | S | P10,P11,P12,P13,P19 | S/R/H/P/A |
| TK4-APPLY-19 | Stage 4 Seating changes after a table closure | Reassigned entry identifies plan_id and carries resulting revision and retained complete accepted_terms. | C HT HTTP | TK4-APPLY-17,TK3-HIST-18,TK3-HIST-19 | S | P10,P11,P12,P13,P19 | S/R/H/P/A |
| TK4-APPLY-20 | Stage 4 Seating changes after a table closure | Unmoved bookings gain no revision or history entry. | C HT | TK4-PLAN-05 | S | P10,P11,P12,P13,P19 | S/R/H/P/A |
| TK4-APPLY-21 | Stage 4 Seating changes after a table closure | Application leaves accepted_terms and booking times identical. | C HT TM | TK4-PRE-20,TK4-PRE-21 | S | P10,P11,P12,P13,P19 | S/R/H/P/A |
| TK4-APPLY-22 | Stage 4 Seating changes after a table closure | Application preserves series exception flags. | C HT ST | TK3-SERIES-05 | S | P10,P11,P12,P13,P19 | S/R/H/P/A |
| TK4-APPLY-23 | Stage 4 Seating changes after a table closure | Application preserves occurrence original scheduled local dates and identities. | C HT TM ST | TK3-ADOPT-36,TK3-ADOPT-37 | S | P10,P11,P12,P13,P19 | S/R/H/P/A |
| TK4-APPLY-24 | Stage 4 Seating changes after a table closure | Each series with at least one moved member increments revision once for the whole application. | C HT TX ST | TK4-APPLY-15,TK3-SERIES-06 | S | P10,P11,P12,P13,P19 | S/R/H/P/A |
| TK4-APPLY-25 | Stage 4 Seating changes after a table closure | A series with no moved member gains no revision. | C HT ST | TK4-APPLY-20 | S | P10,P11,P12,P13,P19 | S/R/H/P/A |
| TK4-APPLY-26 | Stage 4 Seating changes after a table closure | Failed/stale/already-applied application changes no closure, booking/history/revisions, series flags or receipt claim. | C TX RP HT | TK4-APPLY-08,TK4-APPLY-10 | S | P10,P11,P12,P13,P19 | S/R/H/P/A |
| TK4-APPLY-27 | Stage 4 Seating changes after a table closure | Application replay changes no state, histories or counters. | C RP HT | TK4-APPLY-12,TK1-IDEM-14 | S | P10,P11,P12,P13,P19 | S/R/H/P/A |

### TK4-CLOSE

| ID | Source | Atomic requirement | Risk/tags | Dependencies | Owner | Verify | Compat |
|---|---|---|---|---|---|---|---|
| TK4-CLOSE-01 | Stage 4 Seating changes after a table closure | Closure becomes active only upon successful atomic plan application. | C TX HT | TK4-APPLY-14 | S | P04,P13,P14,P19 | S/H/P |
| TK4-CLOSE-02 | Stage 4 Seating changes after a table closure | Applied closure blocks an overlapping single-table option on its table under half-open instant semantics. | C TX TM | TK4-PRE-10 | S | P04,P13,P14,P19 | S/H/P |
| TK4-CLOSE-03 | Stage 4 Seating changes after a table closure | Applied closure blocks any overlapping pair containing its table. | C TX TM | TK2-OPTIONS-06,TK4-CLOSE-02 | S | P04,P13,P14,P19 | S/H/P |
| TK4-CLOSE-04 | Stage 4 Seating changes after a table closure | Applied closures exclude affected singles from available_table_ids. | C HTTP TX | TK1-AV-08,TK4-CLOSE-02 | S | P04,P13,P14,P19 | S/H/P |
| TK4-CLOSE-05 | Stage 4 Seating changes after a table closure | Applied closures exclude affected singles/pairs from available_options. | C HTTP TX | TK2-OPTIONS-06,TK4-CLOSE-03 | S | P04,P13,P14,P19 | S/H/P |
| TK4-CLOSE-06 | Stage 4 Seating changes after a table closure | Create against an overlapping closed member returns409 table_unavailable. | C TX HTTP | TK4-CLOSE-02,TK4-CLOSE-03 | S | P04,P13,P14,P19 | S/H/P |
| TK4-CLOSE-07 | Stage 4 Seating changes after a table closure | Real amendments/moves/series candidates against an overlapping closed member return409 table_unavailable without partial changes. | C TX HTTP | TK4-CLOSE-02,TK3-BATCH-08,TK4-AMEND-26 | S | P04,P13,P14,P19 | S/H/P |
| TK4-CLOSE-08 | Stage 4 Seating changes after a table closure | With explain=true no_overlap is false for an overlapping closure as for a reservation conflict; both rule truths remain independent. | H HTTP VA | TK3-EXPL-04,TK3-EXPL-09 | S | P04,P13,P14,P19 | S/H/P |

### TK4-AMEND

| ID | Source | Atomic requirement | Risk/tags | Dependencies | Owner | Verify | Compat |
|---|---|---|---|---|---|---|---|
| TK4-AMEND-01 | Stage 4 Amend recurring reservations | POST /series/{series_id}/amend is an owner-only write. | C AU | TK3-SERIES-02 | S | P15,P16,P17,P18,P19 | S/R/H/A/P |
| TK4-AMEND-02 | Stage 4 Amend recurring reservations | Unknown or another owner's series amendment returns404 not_found. | C AU HTTP | TK4-AMEND-01 | S | P15,P16,P17,P18,P19 | S/R/H/A/P |
| TK4-AMEND-03 | Stage 4 Amend recurring reservations | An unauthenticated series amendment returns401 unauthenticated, unlike anonymous series reads404. | H AU HTTP | TK3-ADOPT-02,TK3-SERIES-03 | S | P15,P16,P17,P18,P19 | S/R/H/A/P |
| TK4-AMEND-04 | Stage 4 Amend recurring reservations | Series amendment requires an idempotency key with full Stage1 replay semantics. | C RP | TK1-IDEM-01 | S | P15,P16,P17,P18,P19 | S/R/H/A/P |
| TK4-AMEND-05 | Stage 4 Amend recurring reservations | expected_revision is required and must be a positive integer. | H VA | TK1-ERR-04 | S | P15,P16,P17,P18,P19 | S/R/H/A/P |
| TK4-AMEND-06 | Stage 4 Amend recurring reservations | from_index is required and must be an integer in0..count-1. | H VA | TK3-ADOPT-05 | S | P15,P16,P17,P18,P19 | S/R/H/A/P |
| TK4-AMEND-07 | Stage 4 Amend recurring reservations | local_time is required and must be exactly HH:MM in00:00..23:59. | H VA TM | TK1-ERR-04 | S | P15,P16,P17,P18,P19 | S/R/H/A/P |
| TK4-AMEND-08 | Stage 4 Amend recurring reservations | Booleans are invalid integer revision/index inputs. | H VA | TK4-AMEND-05,TK4-AMEND-06 | S | P15,P16,P17,P18,P19 | S/R/H/A/P |
| TK4-AMEND-09 | Stage 4 Amend recurring reservations | Invalid recognized input gives422 validation_failed; unparseable/nonobject JSON retains malformed_request400. | H VA HTTP | TK1-ERR-02,TK4-AMEND-05 | S | P15,P16,P17,P18,P19 | S/R/H/A/P |
| TK4-AMEND-10 | Stage 4 Amend recurring reservations | Valid mismatched series expected_revision gives409 stale_revision. | C CC HT | TK4-AMEND-05,TK3-SERIES-01 | S | P15,P16,P17,P18,P19 | S/R/H/A/P |
| TK4-AMEND-11 | Stage 4 Amend recurring reservations | Series staleness is checked before any occurrence cutoff or booking validation, including empty/no-op eligible sets. | C OR CC | TK4-AMEND-10 | S | P15,P16,P17,P18,P19 | S/R/H/A/P |
| TK4-AMEND-12 | Stage 4 Amend recurring reservations | Unknown amendment fields are ignored for effects but remain in parsed-body receipt identity. | H VA RP | TK1-HTTP-03,TK1-IDEM-11 | S | P15,P16,P17,P18,P19 | S/R/H/A/P |
| TK4-AMEND-13 | Stage 4 Amend recurring reservations | Consider occurrence indices at or after from_index. | H OR HT | TK4-AMEND-06 | S | P15,P16,P17,P18,P19 | S/R/H/A/P |
| TK4-AMEND-14 | Stage 4 Amend recurring reservations | Exclude cancelled occurrences from collective series amendment. | C HT TX | TK4-AMEND-13 | S | P15,P16,P17,P18,P19 | S/R/H/A/P |
| TK4-AMEND-15 | Stage 4 Amend recurring reservations | Exclude all permanent diner-exception occurrences from collective series amendment. | C HT TX | TK3-SERIES-05,TK4-AMEND-13 | S | P15,P16,P17,P18,P19 | S/R/H/A/P |
| TK4-AMEND-16 | Stage 4 Amend recurring reservations | Change eligible occurrences' clock time on their original scheduled local calendar dates. | C TM HT | TK4-AMEND-07,TK3-ADOPT-17 | S | P15,P16,P17,P18,P19 | S/R/H/A/P |
| TK4-AMEND-17 | Stage 4 Amend recurring reservations | Each eligible occurrence retains its reference and owner. | C HT AU | TK4-AMEND-16 | S | P15,P16,P17,P18,P19 | S/R/H/A/P |
| TK4-AMEND-18 | Stage 4 Amend recurring reservations | Each eligible occurrence retains its party size. | C HT VA | TK4-AMEND-16 | S | P15,P16,P17,P18,P19 | S/R/H/A/P |
| TK4-AMEND-19 | Stage 4 Amend recurring reservations | Each eligible occurrence retains its current table selection, including a prior operator assignment. | C HT TX | TK4-AMEND-16,TK4-APPLY-14 | S | P15,P16,P17,P18,P19 | S/R/H/A/P |
| TK4-AMEND-20 | Stage 4 Amend recurring reservations | Identical resulting fields are a no-op retaining that occurrence's accepted terms, end time and revision. | C HT TM | TK4-AMEND-16,TK3-TERMS-18 | S | P15,P16,P17,P18,P19 | S/R/H/A/P |
| TK4-AMEND-21 | Stage 4 Amend recurring reservations | Each real change checks its old accepted cutoff against current start before resulting-policy validation. | C OR TM | TK3-TERMS-13 | S | P15,P16,P17,P18,P19 | S/R/H/A/P |
| TK4-AMEND-22 | Stage 4 Amend recurring reservations | Each real change adopts the policy for its resulting scheduled local start date and validates all resulting fields. | C HT TM VA | TK3-TERMS-14,TK4-AMEND-21 | S | P15,P16,P17,P18,P19 | S/R/H/A/P |
| TK4-AMEND-23 | Stage 4 Amend recurring reservations | Every real result obeys ordinary DST first-occurrence/gap/grid/hours/capacity/absolute-duration rules. | C TM VA | TK4-AMEND-22,TK1-TIME-03,TK1-TIME-04,TK1-TIME-05 | S | P15,P16,P17,P18,P19 | S/R/H/A/P |
| TK4-AMEND-24 | Stage 4 Amend recurring reservations | Results must not conflict with unchanged occurrences. | C TX TM | TK4-AMEND-14,TK4-AMEND-15,TK4-AMEND-20 | S | P15,P16,P17,P18,P19 | S/R/H/A/P |
| TK4-AMEND-25 | Stage 4 Amend recurring reservations | Results must not conflict with other confirmed bookings on any member. | C TX TM | TK1-OCC-01,TK4-AMEND-19 | S | P15,P16,P17,P18,P19 | S/R/H/A/P |
| TK4-AMEND-26 | Stage 4 Amend recurring reservations | Results must not conflict with applied closures on any member. | C TX TM | TK4-CLOSE-02,TK4-CLOSE-03 | S | P15,P16,P17,P18,P19 | S/R/H/A/P |
| TK4-AMEND-27 | Stage 4 Amend recurring reservations | Resulting changed occurrences must not overlap each other on any member under ordinary occupancy. | C TX TM | TK1-OCC-01 | S | P15,P16,P17,P18,P19 | S/R/H/A/P |
| TK4-AMEND-28 | Stage 4 Amend recurring reservations | Non-occupancy errors take precedence in occurrence-index order before final occupancy checks. | C OR TX | TK4-AMEND-21,TK4-AMEND-23 | S | P15,P16,P17,P18,P19 | S/R/H/A/P |
| TK4-AMEND-29 | Stage 4 Amend recurring reservations | Otherwise an occupancy conflict returns409 table_unavailable. | C TX HTTP | TK4-AMEND-24,TK4-AMEND-25,TK4-AMEND-26,TK4-AMEND-27 | S | P15,P16,P17,P18,P19 | S/R/H/A/P |
| TK4-AMEND-30 | Stage 4 Amend recurring reservations | Any failure leaves all occurrence records, terms/end times, histories and revisions unchanged. | C TX HT | TK4-AMEND-28,TK4-AMEND-29 | S | P15,P16,P17,P18,P19 | S/R/H/A/P |
| TK4-AMEND-31 | Stage 4 Amend recurring reservations | Any failure leaves idempotency records/claim unchanged and failed key reusable. | C TX RP | TK1-IDEM-12,TK4-AMEND-30 | S | P15,P16,P17,P18,P19 | S/R/H/A/P |
| TK4-AMEND-32 | Stage 4 Amend recurring reservations | All-no-op and empty eligible sets succeed without changing any revisions. | C HT | TK4-AMEND-13,TK4-AMEND-20 | S | P15,P16,P17,P18,P19 | S/R/H/A/P |
| TK4-AMEND-33 | Stage 4 Amend recurring reservations | Only real changed occurrences need cutoff checks; no-op/excluded occurrences cannot block success on an expired cutoff under the reasoned interpretation. | C OR TM | TK4-AMEND-21,TK4-AMEND-32 | S | P15,P16,P17,P18,P19 | S/R/H/A/P |

### TK4-SERFX

| ID | Source | Atomic requirement | Risk/tags | Dependencies | Owner | Verify | Compat |
|---|---|---|---|---|---|---|---|
| TK4-SERFX-01 | Stage 4 Amend recurring reservations | Successful series amendment returns201 with the current complete series response. | H HTTP HT | TK3-SERIES-01,TK4-AMEND-04 | S | P17,P18,P19 | S/R/H/A |
| TK4-SERFX-02 | Stage 4 Amend recurring reservations | Each actually changed occurrence gains exactly one ordinary changed history entry. | C HT TX | TK3-HIST-12,TK3-HIST-19 | S | P17,P18,P19 | S/R/H/A |
| TK4-SERFX-03 | Stage 4 Amend recurring reservations | Each actually changed occurrence increments its booking revision exactly once. | C HT TX | TK3-TERMS-17 | S | P17,P18,P19 | S/R/H/A |
| TK4-SERFX-04 | Stage 4 Amend recurring reservations | The restaurant increments revision once for the entire successful amendment if anything changed. | C HT TX | TK4-AMEND-30,TK4-SERFX-03 | S | P17,P18,P19 | S/R/H/A |
| TK4-SERFX-05 | Stage 4 Amend recurring reservations | The series increments revision once for the entire successful amendment if anything changed. | C HT TX | TK4-SERFX-03 | S | P17,P18,P19 | S/R/H/A |
| TK4-SERFX-06 | Stage 4 Amend recurring reservations | Unchanged/excluded occurrences gain no history, terms/end-time or booking-revision changes. | C HT TX | TK4-AMEND-14,TK4-AMEND-15,TK4-AMEND-20 | S | P17,P18,P19 | S/R/H/A |
| TK4-SERFX-07 | Stage 4 Amend recurring reservations | Collective series amendment does not mark or clear occurrence exception flags. | C HT | TK3-SERIES-05 | S | P17,P18,P19 | S/R/H/A |
| TK4-SERFX-08 | Stage 4 Amend recurring reservations | Collective series amendment preserves original scheduled dates and stable index/reference identities. | C HT TM | TK3-ADOPT-36,TK3-ADOPT-37,TK4-AMEND-16 | S | P17,P18,P19 | S/R/H/A |
| TK4-SERFX-09 | Stage 4 Amend recurring reservations | All-no-op/empty success still records a normal successful immutable receipt and returns201; its replay returns200. | C RP HT | TK1-IDEM-07,TK1-IDEM-08,TK4-AMEND-32 | S | P17,P18,P19 | S/R/H/A |
| TK4-SERFX-10 | Stage 4 Amend recurring reservations | Replay returns the original series-amend response after subsequent edits or cancellations. | C RP HT | TK1-IDEM-13 | S | P17,P18,P19 | S/R/H/A |
| TK4-SERFX-11 | Stage 4 Amend recurring reservations | Replay changes no histories, terms, flags or counters. | C RP HT | TK1-IDEM-14 | S | P17,P18,P19 | S/R/H/A |
| TK4-SERFX-12 | Stage 4 Amend recurring reservations | Concurrent amendments from the same series expected_revision may not both make a real change. | C CC TX | TK4-AMEND-10,TK4-SERFX-05 | S | P17,P18,P19 | S/R/H/A |

### TK4-CC

| ID | Source | Atomic requirement | Risk/tags | Dependencies | Owner | Verify | Compat |
|---|---|---|---|---|---|---|---|
| TK4-CC-01 | Stage 4 Seating changes after a table closure | Concurrent plan applications cannot expose partially moved bookings or closure-only/assignment-only state. | C CC TX | TK4-APPLY-14,TK2-CC-02 | S | P19,P20,P21 | S/R/H/A/P |
| TK4-CC-02 | Stage 4 Seating changes after a table closure | Application records, histories, booking/series/restaurant revisions, applied flag and receipt commit atomically. | C CC TX RP | TK4-APPLY-15,TK4-APPLY-17,TK4-APPLY-24 | S | P19,P20,P21 | S/R/H/A/P |
| TK4-CC-03 | Stage 4 Seating changes after a table closure | Concurrent previews/applications/diner writes admit some valid one-at-a-time execution order. | C CC TX | TK2-CC-01,TK4-APPLY-08 | S | P19,P20,P21 | S/R/H/A/P |
| TK4-CC-04 | Stage 4 Seating changes after a table closure | Concurrent series amendments/CAS, ordinary occurrence edits/cancel and operator repairs admit valid serialized revision/flag/history results. | C CC TX HT | TK2-CC-01,TK4-SERFX-12 | S | P19,P20,P21 | S/R/H/A/P |
| TK4-CC-05 | Stage 4 Seating changes after a table closure | Identical unused-key preview/apply/series-amend contenders yield exactly one201 and others200 with one effect. | C CC RP | TK1-IDEM-09 | S | P19,P20,P21 | S/R/H/A/P |
| TK4-CC-06 | Stage 4 Seating changes after a table closure | Snapshots taken during preview/apply/series amendments contain a coherent whole state and corresponding receipts. | C CC ST TX | TK1-XFER-02,TK1-XFER-03 | S | P19,P20,P21 | S/R/H/A/P |
| TK4-CC-07 | Stage 4 Seating changes after a table closure | All concurrent requests remain within actual inherited5s/10s/readiness/resource budgets with no5xx on feasible bounded workloads. | H CC DEP HTTP | TK1-RUN-06,TK1-RUN-07,TK1-RUN-08,TK1-ERR-13 | S | P19,P20,P21 | S/R/H/A/P |

### TK4-UP

| ID | Source | Atomic requirement | Risk/tags | Dependencies | Owner | Verify | Compat |
|---|---|---|---|---|---|---|---|
| TK4-UP-01 | Stage 4 Cumulative export/import | Stage4 accepts an unchanged export from the same team's Stage1 service. | C ST | TK3-UP-01 | S | P21,P22,P23 | S/R/B/H/A/P |
| TK4-UP-02 | Stage 4 Cumulative export/import | Stage4 accepts an unchanged export from the same team's Stage2 service. | C ST | TK3-UP-02 | S | P21,P22,P23 | S/R/B/H/A/P |
| TK4-UP-03 | Stage 4 Cumulative export/import | Stage4 accepts an unchanged export from the same team's Stage3 service. | C ST | TK1-XFER-04,TK3-UP-08 | S | P21,P22,P23 | S/R/B/H/A/P |
| TK4-UP-04 | Stage 4 Cumulative export/import | Imported native series remain usable for owner amendments and authorized seating repair. | C ST HT | TK3-UP-10,TK4-AMEND-01 | S | P21,P22,P23 | S/R/B/H/A/P |
| TK4-UP-05 | Stage 4 Cumulative export/import | Imported moved and cancelled occurrences preserve current assignment/status and exclusion semantics. | C ST HT | TK4-UP-04,TK4-AMEND-14,TK4-AMEND-19 | S | P21,P22,P23 | S/R/B/H/A/P |
| TK4-UP-06 | Stage 4 Cumulative export/import | Original scheduled dates survive transfer or are truthfully recovered from preserved adoption response/known metadata, never the changed current anchor date. | C ST HT TM | TK3-ADOPT-42,TK4-AMEND-16 | S | P21,P22,P23 | S/R/B/H/A/P |
| TK4-UP-07 | Stage 4 Cumulative export/import | Earlier booking/create/move receipts, histories and retries remain valid exact original JSON. | C ST RP HT | TK3-UP-06,TK3-UP-09,TK3-UP-11 | S | P21,P22,P23 | S/R/B/H/A/P |
| TK4-UP-08 | Stage 4 Cumulative export/import | Earlier series-adoption receipts and original response/revision remain valid after upgrade and later changes. | C ST RP HT | TK3-ADOPT-42,TK3-UP-11 | S | P21,P22,P23 | S/R/B/H/A/P |
| TK4-UP-09 | Stage 4 Cumulative export/import | Existing sessions and references remain valid without new browser sign-in/reload when import completes between requests. | C ST AU UI | TK3-UP-04,TK3-UP-05,TK3-UP-07 | S/E | P21,P22,P23 | S/R/B/H/A/P |
| TK4-UP-10 | Stage 4 Cumulative export/import | Native Stage4 transfer preserves closures, immutable plans, captured restaurant revisions and applied flags. | C ST HT | TK1-XFER-15,TK4-PLAN-10,TK4-APPLY-10 | S | P21,P22,P23 | S/R/B/H/A/P |
| TK4-UP-11 | Stage 4 Cumulative export/import | Native Stage4 transfer preserves all seven successful receipt families and failed-key reuse. | C ST RP | TK1-XFER-17,TK1-XFER-18 | S | P21,P22,P23 | S/R/B/H/A/P |
| TK4-UP-12 | Stage 4 Cumulative export/import | Native Stage4 transfer preserves booking/series/restaurant revisions, histories, accepted terms, scheduled dates and permanent flags. | C ST HT | TK3-UP-09,TK3-UP-10,TK4-SERFX-08 | S | P21,P22,P23 | S/R/B/H/A/P |
| TK4-UP-13 | Stage 4 Cumulative export/import | Replacement import removes all destination-only closure/plan/revision/receipt state; repeated import restores source snapshot without duplication. | C ST TX | TK1-XFER-06,TK1-XFER-07,TK1-XFER-08 | S | P21,P22,P23 | S/R/B/H/A/P |
| TK4-UP-14 | Stage 4 Cumulative export/import | Invalid import preserves all destination data including new operator/agreement state and credentials. | C ST TX AU | TK1-XFER-11 | S | P21,P22,P23 | S/R/B/H/A/P |
| TK4-UP-15 | Stage 4 Cumulative export/import | Reset clears all imported/native closures, previews/applied flags and new receipt families, and starts restaurant revisions at0. | C ST TX RP | TK1-XFER-20,TK4-RREV-01 | S | P21,P22,P23 | S/R/B/H/A/P |
| TK4-UP-16 | Stage 4 Cumulative export/import | Existing truthful legacy identities/statuses/timestamps/history/receipts remain exact; missing baseline metadata never fabricates unobserved past events. | C ST HT RP | TK3-UP-13,TK3-UP-14,TK3-UP-15 | S | P21,P22,P23 | S/R/B/H/A/P |

### TK4-UI

| ID | Source | Atomic requirement | Risk/tags | Dependencies | Owner | Verify | Compat |
|---|---|---|---|---|---|---|---|
| TK4-UI-01 | Stage 4 Existing screens and applied plans | Existing availability screen reflects applied closures/assignments on subsequent authoritative searches. | H UI HTTP | TK2-RACE-01,TK4-CLOSE-04,TK4-CLOSE-05 | S/E | P14,P23 | S/R/B/P |
| TK4-UI-02 | Stage 4 Existing screens and applied plans | Existing lookup screen reflects current applied table assignments and every member label. | H UI HT | TK2-LOOKUP-01,TK4-APPLY-21 | S/E | P14,P23 | S/R/B/P |
| TK4-UI-03 | Stage 4 Existing screens and applied plans | Existing confirmation presentation reflects current applied assignments without rewriting original server receipt JSON or pending key/body. | C UI RP HT | TK3-UP-07,TK4-PLAN-10,TK4-APPLY-12 | S/E | P14,P23 | S/R/B/P |
| TK4-UI-04 | Stage 4 Existing screens and applied plans | No new operator/recurring-amendment/history screen, background polling or idle live update is required; prior375px/desktop/accessibility/state/offline obligations remain. | H UI QA | TK3-UP-18,TK2-QA-01 | S/E | P14,P23 | S/R/B/P |

### TK4-GATE

| ID | Source | Atomic requirement | Risk/tags | Dependencies | Owner | Verify | Compat |
|---|---|---|---|---|---|---|---|
| TK4-GATE-01 | Stage 4 Final submission assignment | Stage4 production starts only after independent Stage3 ACCEPT and a separately committed copy of its complete service. | C SC ST | TK3-GATE-02 | C | P24 | - |
| TK4-GATE-02 | Stage 4 Final submission assignment | Stage4 production acceptance requires independent formal verdict on the exact integrated FULL SHA, covering all inherited/new blocking obligations. | C SC | TK4-GATE-01 | C | P24 | - |
| TK4-GATE-03 | Stage 4 Final submission assignment | Commit only the owned sanitized Stage4 canonical requirements.md during a coordinated index window, then report FULL SHA/path/counts and release index. | H SC | - | C | P24 | - |

## Independent exact planning oracle and bounded witnesses

The verifier builds its model from synthetic controlled fixture configuration, each current booking's recorded accepted_terms and retained starts_at/ends_at, explicit prior closures, and the proposal. Do not import production selection, overlap, optimizer, normalization, revision or migration helpers. Do not treat GET /availability as the oracle for planning: it uses the newly selected policy rather than every booking's accepted capacities.

Use exact comparable instants: independently parse offset timestamps into ordinal-day/time/fraction scalars minus offsets; avoid local-wall overlap, binary-float fractions and UTC-year0/10000 conversion overflow. Two intervals conflict iff a.start < b.end and b.start < a.end. Capacities/party/objective values use exact integer arithmetic on feasible outputs. Unknown field numeric tokens and immutable receipt equality use an independent parsed-JSON value oracle. Rank options before any filtering, then canonicalize unordered selection to declaration orientation solely for seating identity/output.

Bounded reference algorithm (model work need not satisfy the product's HTTP timeout, but product requests must):
```text
options = singles in fixture order followed by declared pairs in declaration order
rank(option) = its index in this full list
C = all confirmed bookings in restaurant overlapping proposal interval
sort C by reference; F = all other confirmed bookings at that restaurant
for each booking b in C:
    choices[b] = options fitting party under b.accepted_terms.capacities
    remove choices overlapping F, prior closures or proposal on any member
for each complete combination of choices, without dropping any booking:
    reject any member-overlap between assigned bookings
    score = (count(unordered assigned set != current set),
             sum(own accepted option capacity - party_size),
             tuple(option ranks in C reference order))
choose minimum score using tuple/lexicographic comparison
if no combination exists: expect no_feasible_plan with exact rollback
else expect all assignments, truthful changed flags, moved_count and unused_seats
```
At mandatory maxima there are at most10 options and6 considered bookings, so naive complete enumeration is bounded by10^6 candidate vectors. Constraint pruning is allowed in the independent oracle, but must preserve completeness. Small exhaustive cases calibrate every objective; include an in-range maximum case and controlled concurrent request budgets separately. Streaming does not solve mathematically unbounded exact numeric output; report feasible dataset/output limits as adopted, never substitute approximate objective comparisons or an unsupported capacity cap.

Concrete synthetic witnesses independently derived from the contract:

| Witness | Configuration and exact expected decision |
|---|---|
| Changes dominate waste | Fixture singles [a:4,b:4,c:2,d:8], no pairs. Simultaneous booking A party2 on a, B party4 on b; propose closure of b overlapping both. Optimal A remainsa/B movesd: moved_count1,unused_seats6. Moving A->c and B->a has waste0 but two changes and must lose. This also exposes incorrectly considering only b's occupants. |
| Waste dominates rank | Fixture [a:4,b:4,d:6,c:4], A party2 on a and B party4 on closedb, same interval. Both B->d and B->c move one booking, but c gives total waste2 versusd4; choose c despite its higher rank. |
| Rank vector uses reference order | Fixture [a:4,c:4,b:4,d:2], no pairs. Same-time AA0001 party2 ona, BB0001 party4 on closedb, CC0001 party2 onc. Two best two-change/waste2 plans exist. Required assignment AA->a unchanged, BB->c changed, CC->d changed has vector(0,1,3); competing AA->d/BB->a/CC->c vector(3,0,1) loses. Renaming the incumbent references reverses which displacement wins; do not greedily seat BB first. |
| Own accepted capacities | Record earlier booking terms with a large enough alternative and later booking terms with different capacities, then publish a conflicting current policy. Oracle uses each saved capacity map independently; original detail/current availability may both disagree with valid repair. Pair sums are computed separately for each booking. |
| Retained full intervals/fixed bookings | Considered booking begins before proposal or ends after it. A booking not overlapping proposal remains fixed but overlaps the considered interval's outside portion on a candidate member; reject that option. Prior closure outside proposal but within retained booking interval likewise blocks it. Exact adjacency to any closure/booking is allowed. |
| Pair/member interaction | Declared pairs [b,a] and [b,c], no [a,c]. A considered reservation may use any declared pair under its terms; shared memberb conflicts even when arrays differ. Pair orientation alone changes neither moved_count nor history. Ranks retain all preceding singles/declared pairs even if filtered. |
| Operator cutoff bypass | Use an editable-policy fixture with a confirmed historical or imminent booking whose accepted cutoff has passed. Owner real PATCH must refuse; manager repair retains times/party/terms and succeeds if a feasible seating assignment exists. Time passing alone is not a restaurant-revision change. |
| Zero considered/no moved | A valid closure with no considered bookings yields empty assignments,moved_count0,unused_seats0 and unchanged preview counter. First apply still records closure and increments restaurant counter once. Considered but already feasible assignments likewise remain unchanged with no booking/series events while the closure takes effect. |
| Feasible exact numeric distinction | Synthetic accepted policy0 capacity1e309 and a small second capacity yields a310-digit exact pair sum; independently prove capacity threshold/objective differences of1. Never use binary float or rounded Decimal default context to determine unused_seats/eligibility/objective ties. |

Metamorphic checks supplement exact witnesses, rather than replace the objective oracle:
- Rename table IDs/labels while preserving order, members and all recorded references: transform assignments accordingly with identical objective/ranks.
- Rename booking references: first two optimum objective components stay equal, but recompute the final vector under the new ascending-reference order; assignments may change.
- Reorder fixtures/pair declarations: moved/waste minima are unchanged when admissible sets are preserved, while rank tie-break may choose a different assignment and pair orientation follows new declarations.
- Add an unrelated other restaurant operation or cancelled overlapping record: the target restaurant's model and captured revision/staleness stay unchanged.
- Shift all controlled UTC intervals and closure instants by the same whole-week offset: all overlap/objective outcomes stay equivalent; verify absolute/calendar boundaries independently outside this transformation.
- Increase every considered party by the same delta while keeping all prior admissible choices admissible: waste decreases by count*delta uniformly; optimal assignments/ranks stay unchanged. Do not apply this claim if capacity eligibility changes.
- In singles-only models, adding the same capacity increment to every option within each booking's terms adds a constant waste offset when eligibility is unchanged. This invariance does not generally hold for mixed singles/pairs.
- A new non-current pair that is an occupancy superset of a single, with greater waste and with that single eligible for every relevant booking, is dominated; it cannot improve the optimum. Without all these qualifiers, adding an option can improve the primary movement objective.

Calibrate the independent oracle against intentionally wrong decision variants: current-policy capacities, only-closed-table considered set, greedy reference/party order, weighted movement+waste, rank-compaction after filtering, sum of ranks instead of lexicographic vector, wall-clock overlap/closed intervals and assignment array-equality instead of unordered identity. Each has a designated witness that must fail, preventing a shared mistaken oracle from approving production.

## Specified precedence and atomic state boundaries

| Operation | Required order/atomic boundary |
|---|---|
| All seven idempotent families | Parse object/authenticate -> user/method/full path/key/full parsed-body receipt resolution -> endpoint control/resource/permission/state rules. Same key differing body409 before proposed fields/current resources; same-key successful replay200 exact original JSON even after later change. Normalize seating only after comparison. |
| Preview | Required interval/table/manager checks and planning limits where applicable -> complete accepted-term/fixed/closure feasibility -> exact lexicographic optimum -> immutable plan plus original receipt publication. No occupancy/closure/booking-history/counter mutation. Unrelated permission/field-error ties are not assigned unsupported total priorities. |
| Apply | Receipt resolution first. Unknown/foreign-restaurant plan404; applied under different key409plan_already_applied before stale, then captured local revision match. Commit closure, assignments, moved events/revisions, affected series increments, applied flag, one restaurant increment and receipt together. All errors/replays change nothing. |
| Ordinary diner writes with closures | Retain inherited resource/expected_revision/accepted-cutoff/field-error precedence; final member occupancy now includes applied closures. Current-policy validation must not retroactively alter accepted repair terms. Manager repairs bypass diner cutoff. |
| Series amend | After object parsing/authentication and receipt resolution, owner/resource/control validation; valid mismatched series revision before every occurrence cutoff/booking validation, even empty/no-op sets. Iterate eligible indices ascending; cancelled/exceptions excluded. No-op retains old state; real change old cutoff then complete result-date policy. All non-occupancy errors by index precede final closure/member overlaps. Publish records/events/book/series/restaurant revisions and receipt together, no exception marking. |
| Read/export/import | Every read and snapshot sees a serializable whole transaction; invalid import rolls back all metadata/credentials/receipts. Import restores known history/terms/schedules/counters/plans/flags, rather than retroactively computing unknown events. Reset clears all generations and sets local restaurant counter0. |

A stale series revision is explicitly before occurrence cutoff/booking checks, not explicitly before an invalid from_index/local_time control. Already-applied precedes stale under a different key because application itself changes the restaurant counter and the contract separately prescribes plan_already_applied. Ordinary no-op eligibility and the collective-series real-change-only cutoff distinction are kept explicit. General current-stage counters apply only in Stage4, not retroactively to accepted earlier services.



## Inherited independent verification catalogue

All fixture values and labels in these procedures are synthetic. Expected intervals, pair eligibility, JSON values and DOM state transitions must be derived independently of production helpers. Record case IDs, exact production FULL SHA, status/code/JSON or rendered-state observations and sanitized evidence references. Never commit actual passwords, bearer tokens, opaque exports or browser session dumps. Keep snapshots private and ephemeral; public evidence can report equality outcomes and redacted structural counts.

### Inherited procedures applied cumulatively

V01..V20 retain their obligation sets and use current cumulative shapes, date-selected policies and retained accepted occupancy/cutoffs where appropriate; historical replay values remain unchanged. All seven required-key write families are covered, extending the original V06 wording. The following summaries keep the cumulative ledger self-contained; the initial Stage 1 ledger supplies original calibration detail but is not required to interpret the rows above.

| Procedure | Independent obligation and coverage expectation |
|---|---|
| V01 | Reproduce Dockerfile/RUN.md build and single-container launch with custom/default PORT, 2 CPU/2GiB, no runtime outbound access; healthy/API-ready <=60s. Confirm scoped delivery/provenance and bundled browser assets. Host package imports are not acceptance. |
| V02 | Reset A->B repeatedly removes old accounts/tokens/records/config/receipts, with coherent visibility after204. Seed config order, all ID boundaries, given short passwords, single/pair confirmed/cancelled records; login and occupancy reflect fixture. Reject wrong-type/value inputs using §5 without partial state. |
| V03 | Endpoint matrix of missing/null/wrong-type/correct-type invalid fields, dates, party values, query plain digits, bare local times, IDs/keys and ignored fields. Include unknown valid JSON numeric exponent1e309 and calendar years0001/9999 without assuming binary-float parser limits. Verify all error envelopes/statuses/codes and no5xx. Pair selectors obey specific codes; distinguish historical response from new shape. |
| V04 | Signup/login errors and successful responses; signup8-character boundary versus unrestricted seeded password login; concurrent duplicate signup; all old session tokens coexist and survive import. Independent storage/source inspection proves password hashing for every account; HTTP behavior alone does not prove it. |
| V05 | Enumerate public/protected APIs and new HTML routes. Cross-owner list/reference GET/cancel/PATCH/moves cannot leak or mutate another record; foreign/unknown refs404. Export/import/reset deliberately remain unauthenticated. Browser signed-out cell selection cannot book. |
| V06 | All seven required-key families:0/1/255/256-length keys, replay with reordered object keys/whitespace, different body including ignored fields, different user/path, failed4xx retry. Changed invalid body conflicts before field/resource rules. Arrays retain order and booleans differ from numbers; reversing a valid pair is a changed JSON body under the same key. |
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
| W20 | Verify Stage 1 exact-SHA ACCEPT precedes committed copied Stage 2 production baseline; no premature backend/browser production acceptance. Verify ledger commit occurs only after verifier releases its window and changes only this owned file. The completed historical Stage 2 gate supplies provenance; Stage 3's preceding gate is Z24; Stage 4's active release gate is P24. Verify cumulative behavior on the exact Stage 3 candidate, not just test hooks or official pass count. |


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



V/W/Z procedures retain their original feature obligations under current Stage4 closures, operator history and general counters where applicable. Original-stage upgrade paths remain preceding compatibility provenance; P21..23 add direct populated Stage1/2/3->4 paths. Native Stage3 ordinary noop cutoff/exception rules are not generalized over Stage4's explicit series-amend or operator exceptions. Prior-stage acceptance never substitutes for current exact-SHA regression evidence.



## Stage 4 independent verification procedures

Every P procedure is an execution obligation for the independent verifier, not a claimed product pass in this analysis. Cases report exact candidate FULL SHA, expected/observed status/code/JSON/DOM state, oracle provenance, latency and sanitized evidence. Private snapshots/tokens remain outside committed artifacts.
| Procedure | Independently derived cases and coverage expectation |
|---|---|
| P01 | Restaurant revision transition oracle: reset with seeded records starts0, then independently count each new ordinary create, real individual PATCH, first cancel, policy publish, whole batch/adoption/series amend and first plan apply. No-op/repeat-cancel/failed writes/read/auth/export/previews/replays do not increment. Observe via fresh zero-considered preview on a valid table/interval or defensible state/source inspection; no new GET counter endpoint is required. Real compound operations increment once, not per generated/changed member. Other restaurants remain independent. |
| P02 | Preview request/auth matrix: manager, authenticated non-manager403, anonymous401, unknown restaurant/table404; required fields, unknown fields, invalid JSON/object/types, missing offsets, invalid dates, equal/reversed intervals. Use differently offset strings with reversed lexical versus instant order and equivalent instants. Check half-open/fractional boundaries without unsupported precision truncation; Z as explicit UTC and accepted interval normalization are documented interpretations. All key0/1/255/256/user/path/full-body cases; used key differing invalid body409 before resource/fields. |
| P03 | Planning limits and preview effects: test6 tables/4 pairs/6 considered bookings inclusive and separate above-limit fixtures. In-range cannot planning_limit; above-limit may use422planning_limit or correctly implement the normal optimum/error. Preview preserves all records/occupancy/terms/history/book/series/restaurant counters while storing immutable plan+receipt. Include zero considered/zero moved, fully infeasible409 with exact rollback/reusable key. Count every confirmed overlapping booking across owners, not only closed-table occupants; cancelled excluded. |
| P04 | Feasibility oracle from accepted snapshots: every single/declared pair, own capacities, current-policy/detail mismatch, no transitive undeclared pair. Retained full intervals include portions before/after closure; fixed booking outside proposed interval can still block an assignment there. Prior closures, proposed closure, overlapping assigned pairs/singles, cross-restaurant identical table IDs and half-open adjacency. Manager repair works despite old cutoff. Verify no considered booking removed/cancelled/time/party/owner/identity/terms change. |
| P05 | Exact movement/waste witness cases in the model above: one move/waste6 beats two moves/waste0; equal one-move choices select lower waste despite worse rank. Include a feasible unchanged assignment of an unclosed-table booking and unused_seats over all considered bookings, not only moved ones. New policy publication cannot replace per-booking accepted capacity maps. Empty result scores0/0. |
| P06 | Exact vector witness [a:4,c:4,b:4,d:2] and refsAA0001/BB0001/CC0001 yields AA->a,BB->c,CC->d, score(2,2,(0,1,3)); competing score(2,2,(3,0,1)) loses. Reverse incumbent reference ordering and independently recompute the winner. Reorder fixture/declarations and rename IDs/labels; ensure ranks follow order rather than lexical table IDs, party size or solver traversal. Filtered options retain original rank gaps. |
| P07 | Pair optimization/history identity: declaration[b,a] output follows that order; reversed current/request pair is same set and changed:false when otherwise unchanged. Pairs use each booking's own exact capacity sum and member intersection against fixed/proposed/prior closure constraints. Test single->pair,pair->single,pair->pair assignments, pair on one closed member, overlapping pairs, all4 declared pairs. No greedy capacity-only or pair-first ranking. Unavailable lower-ranked options do not renumber remaining choices. |
| P08 | Independent bounded enumeration/metamorphic calibration: synthetic models use at most10 options/6 considered records, exact feasible integers and independently parsed instants. Run all stated witness and qualified transformations, plus feasible disparate-exponent1e309+1 and objective differences of1 using exact arithmetic. Detect controlled wrong variants for current capacities, considered-set restriction, weighted/greedy objective, rank compaction/summed ranks, array identity and closed/wall-time intervals. Do not reuse production helpers or availability decisions. Report dataset/output bounds and actual product request latency; no arbitrary input cap/rounding. |
| P09 | Immutable preview receipts: repeat same key/body returns200 same plan_id/captured counter/closure/assignments/scores; first201 only. Later diner changes,publish,application/cancel do not rewrite old preview JSON or its flags. New-key previews may capture a newer revision with different optimum; previews alone do not stale each other. Unknown-body fields ignored in effects but count for key conflict. Failed no_feasible_plan/invalid/limit keys remain reusable when conditions become valid. |
| P10 | Apply permission/resource/idempotency matrix: manager versus nonmanager/anonymous, unknown plan and wrong restaurant404. Same key across preview/apply paths independent. First apply201; same successful key200 exact original response after later state changes; different key already-applied409 even though its own application raised restaurant revision. Used differing body409 before applied/stale. Test replay after booking cancel or further reassignment and after import. Normal{} plus ignored fields remain body identities; no unsupported strict-empty-body rule. |
| P11 | Restaurant-local stale map: take preview then each real same-restaurant new booking (even outside closure), PATCH,cancel,publish,batch,adoption/series change/another planapply must stale it with no mutations. No-op writes,repeatcancel,preview/replay/failed operations must not stale it. Other restaurant booking/policy/closure changes, including equal table strings, do not stale. Competing plans at same revision: first successful apply invalidates remaining unapplied plans; applied one under another key has already-applied precedence. |
| P12 | Atomic application/history: compare all considered records before/after, including owners across accounts. Moved book revision+1 and exactly one reassigned entry with table_ids complete before/after and plan_id,resulting revision/retained terms; this applies even single->single. Unmoved records/history unchanged. Accepted terms/start/end/party/reference/reservation_id/owner/creation truth preserved. Responses include all considered in reference order, current single aliases and pair shape consistent. Preview replay remains its original changed flags. |
| P13 | Series repairs and counters: several moved members of one agreement increment that series once; two affected agreements eachonce, unchanged-only agreement0. A prior true exception remains true; false remains false. Original schedules/index/reference/owner/terms stay identical even anchor cancelled or individually date-shifted elsewhere. Operator repair never marks diner exceptions, and may repair cutoff-passed confirmed members. Closure/apply history/counters/flags publish together; later ordinary diner edit still marks exception and later series amendment retains repaired current tables. |
| P14 | Applied closure HTTP/browser occupancy: member singles/pairs disappear from options, available_table_ids stays singles-only, fitting empty slots retained. Explain every table/independent capacity+no_overlap truths including bothfalse and closure-no_overlapfalse. Creates,PATCH,moves,adoption/series real candidates crossing closed member409table_unavailable with full rollback, subject to inherited nonoccupancy precedence. Exact endpoints adjacent to closure work; bookings overlapping its outside proposal portions stay blocked by fixed records. Refresh browser search/lookup and current confirmation reads reflect assignments/labels. |
| P15 | Series-amend control matrix: expected_revision required positive integer,from_index0..count-1,local_time exact00:00..23:59; missing/bool/string/fraction/out-of-range/bad-format recognized input422, unparseable/nonobject400. Owner/foreign/unknown404 versus anonymous write401. Valid stale revision409 before any eligible occurrence cutoff/grid/party/closure conflict, including empty/all-noop. Invalid control-versus-stale ties are documented without invented ranking. Unknown fields/full key identity/per-user/full-path replay and failed key reuse. |
| P16 | Original schedules/current selection/eligibility: adopt, individually shift anchor date/clock or another occurrence to permanent exception, cancel siblings, and operator-reassign remaining singles/pairs. Amend from_index boundary inclusive; skip cancelled and exceptions, keep index/ref/owner/party/current repaired tables, use recorded original dates rather than deriving from changed anchor or current table defaults. Use original adoption receipt/known metadata for legacy migration. Eligible native series never mark exceptions on collective clock changes. |
| P17 | Terms/no-op/cutoff effects: real changes check each old accepted cutoff then all fields under result-date policy, updating terms/end/book history/revision. A newer restrictive policy does not revalidate unchanged terms. All-noop/empty successes201 store receipt with no counters/events/flags; stale control still refused. To test expired eligible no-op without clock mocks, adopt an editable later-today anchor, collectively move clock earlier on the same original day into the past (old current cutoff passes and past target alone is allowed), then repeat desired clock with a new key/current revision; no-op must succeed despite now-expired first occurrence. Choose a zone with enough remaining open-day margin; no host-time manipulation required. |
| P18 | Per-index errors and calendar: future Berlin/NewYork weekly series originally at safe01:30; collectively change to02:30 on a future spring gap date to reject the whole operation at first failing eligible index. Repeated fall clock uses first occurrence/absolute duration. Different resulting date policies alter grid/hours/caps/duration; earliest eligible nonoccupancy failure wins before a later cutoff or any overlap, never sort by reference/date. New durations may conflict with fixed/unchanged/cancelled-status-aware records or prior closures. Every failure preserves full series/history/terms/flags/revisions/receipt claim. |
| P19 | Atomic state and CAS race campaign: barrier-start up to50 previews/applications/series-amends, member booking/PATCH/cancel/batch/policy/adoption and expected-series-revision contenders. Identical unused keys one201/others200; differing bodies/users/paths independent or specific conflicts. Concurrent distinct real series amendments at one revision cannot both change; true noops may coexist. Every read/snapshot admits some valid transaction order; no closure-only/partially moved/event-counter mismatch. Audit record+history+book/series/restaurant counter deltas, applied flags, exact receipts, all member intervals and source configuration. |
| P20 | Maximum supported/latency/offline concurrency: separately test6 tables/4 pairs/6 considered, difficult feasible/infeasible assignments, plus50 in-flight bounded HTTP operations, including coordinated in-range planning work rather than only cheap reads, with2CPU/2GiB,5s normal/10s controls/60sready. Independent oracle may enumerate offline; product timeout never extended because its solver is exact. Native Docker no runtime outbound,custom/default PORT,bundled existing browser assets and full V/W/Z regression. No unbounded output/performance claim beyond observed feasible envelope. |
| P21 | Native Stage4 A->populated B->C transfer: unapplied/stale/applied plans,closures, multiple policies/accepted snapshots, histories/reassignments, series schedules/flags/counters and all7 receipt families. Source unavailable/no shared files/volume/address; unchanged opaque import. Original preview/apply/amend replay exact after later writes, applied flag still blocks different key, captured local revision remains accurate. Destination credentials/plans/closures removed, repeated restore no duplicates, invalid import rollback/reset all new state. Export against apply/amend yields whole before/after records+closure/history/counters/receipts. |
| P22 | Every populated earlier upgrade: accepted exact Stage1,independently accepted Stage2 and Stage3 source containers separately export into Stage4 candidate. Preserve hashes/all tokens/refs/creation/status/current assignments/terms/history and exact booking/batch/adoption receipts with failed keys reusable. Missing old metadata gets documented truthful baseline, no retroactive events/counter recomputation. Stage1/2 lack manager roles/series: defaults[]remain; owner can adopt eligible imported single/pair and amend. Stage3 with actual manager IDs exercises imported exception/moved/cancelled series repair/amend; original schedules from preserved adoption response/metadata, not changed anchor. Native known counters/history remain exact. |
| P23 | Retained browser and current plan reflection: keep logged-in tab,pending body/key/reference through completed populated import without reload. Lost preupgrade booking response retries exact old JSON/reference; no manufactured result. After applied repair, authoritative refreshed availability/lookup/confirmation displays current single/pair labels/time/party; original server receipts and unchanged form retry identity remain untouched. Repeat delayed search/detail/conflict/lost-response races, keyboard/focus/visible labels/contrast/distinct feedback/no horizontal scrolling at375CSSpx and desktop, bundled offline assets. No required new operator UI or idle polling. |
| P24 | Release/evidence trace audit: Stage3 formal exact-SHA ACCEPT and separately committed complete copied baseline before anyStage4 production. Independent verdict on exact integrated Stage4 FULL SHA closes every inherited/new C/H obligation with case-specific evidence,not just owner/official counts. Ledger unique stable IDs/dependencies/procedure mapping, sanitization/owned-file-only commit and serialized index-window release verified. Accepted prior source/evidence and official specs/harness/shipped checks remain untouched. |


## Blocking risk model and dependency ordering

There are730 atomic records:557 inherited and173 new. Risk totals are382 CRITICAL,325 HIGH and23 MEDIUM. The707 CRITICAL/HIGH obligations require independent closure on the exact current production revision; grouping rows into a procedure never waives any atomic obligation. There are88 named independent procedures:20 V,20 W,24 Z and24 P. Procedure definitions are planned verification obligations; this preparation ledger claims no Stage4 product execution, pass or acceptance.

| Blocking cluster | Requirement mapping | Concrete release risk / dependency |
|---|---|---|
| Occupancy and exact planning | TK1-OCC, TK2-PAIR/OPTIONS/CC, TK4-PRE/OPT/CLOSE | Considering only the closed table's customers, using current policy capacities, dropping a fixed interval portion, or greedy/weighted optimization can return a feasible-looking but contractually wrong plan. Independent exhaustive feasibility and lexicographic objective precede response checks. |
| Preview and apply historical truth | TK1-IDEM, TK4-PLAN/APPLY/CC | A preview that mutates occupancy, a receipt rewritten with current state, applied-versus-stale inversion, or closure/assignment/event partial commit corrupts review and retries. Stable plan snapshot and local captured revision precede atomic publication. |
| Revisions and no-ops | TK3-TERMS/REV/SERIES/BATCH, TK4-RREV/AMEND/SERFX | Per-record restaurant increments, stale no-op shortcuts, old cutoff replaced by new policy, or collective exception marking break counters and future eligibility. Record/series/restaurant deltas must be independently counted together. |
| Calendar and scheduled-date continuity | TK1-TIME, TK3-ADOPT, TK4-AMEND/UP | Duration is absolute; recurring amendments use original schedules and current tables, never modified anchor dates. Per-index non-occupancy errors precede final overlap. UTC/year boundaries, both zones' gaps/folds and policy-date boundaries need independent cases. |
| Authorization and visibility | TK1-AUTH/READ, TK3-MGR/HIST/DEC, TK4-PRE/APPLY/AMEND | Manager authority is restaurant-local and does not grant private lookup/history. Anonymous history/decision/series-read404 versus anonymous new-write401 remain endpoint-specific. Missing legacy manager roles cannot be invented during migration. |
| Snapshot and upgrade continuity | TK1-XFER, TK2-UP, TK3-UP, TK4-UP | Credentials/tokens, identities, accepted terms, history, series schedules/flags, closures/plans/applied flags/captured counters and original receipts must transfer as a coherent replacement. Feasible exact numeric values must survive ordinary opaque wrapping without rounding. |
| Browser authority and rendered quality | TK2-RACE/BOOK/LOOKUP/QA, TK4-UI | Current lookup/availability/confirmation must reflect applied assignments, while old receipts and pending exact request identity stay historical. Search/detail/selection races, conflict-form retention, lost-success retry and375px/desktop quality remain full regressions. |
| Provenance and acceptance | TK1-RUN/SC, TK3-GATE, TK4-GATE | No Stage4 implementation before preceding formal ACCEPT/copy gate; exact integrated container/HTTP/browser evidence required. Owner green counts and this analysis are not acceptance. |

Dependency order is behavioral, not a prescribed architecture:
1. Preserve identity/authentication, exact JSON values/receipts, date/instant and unordered-set semantics; establish portable accepted snapshots and truthful existing history.
2. Define current Stage4 restaurant/series/booking counter transitions and original scheduled dates independently of present anchor dates.
3. Compute closure membership, full retained intervals, fixed occupancy and all complete ranked options under each booking's own terms; calibrate the independent feasible-plan/objective model.
4. Produce immutable previews and validate manager/current local revision/apply state. Atomically publish closure, assignments, history, counters and receipts.
5. Select recurring eligible indices, validate stale control and real-change old-cutoff/new-policy candidates in index order, then final occupancy, then atomic histories/counters/receipt without exception marking.
6. Exercise actual simultaneous operations and snapshots; verify each read admits a whole valid serialized state.
7. Verify every populated earlier upgrade plus native replacement; then retained browser recovery/current rendered reflection and actual offline resource budgets.
8. Obtain formal independent verdict on the exact integrated production SHA and close every blocking row with inspectable sanitized evidence.

## Compatibility matrix and preserved truth

| Source -> Stage4 | Required populated source / future operation | Required preservation and verification |
|---|---|---|
| Stage1 ->4 | Multiple sessions, confirmed/cancelled single bookings, completed create/batch receipts after later edits and failed reusable keys. Adopt an eligible imported owner booking, then collectively amend it. | Keep hashes/tokens, references/IDs/owners/creation/status/times and exact old response JSON; document missing metadata baseline. No manager-role elevation. P22/P23 plus V/W/Z inherited cases. |
| Stage2 ->4 | Single/pair bookings with declaration orientation, amended/cancelled records, exact complete bodies and original receipts, retained pending browser request. Owner adoption/amendment on imported pair. | Current representations can gain later fields while old receipts remain unchanged; reversed arrays still conflict under a used key. Preserve full pair occupancy/labels and retained browser identity. P22/P23. |
| Stage3 ->4 | Effective-dated policies/managers, native accepted histories/revisions, adopted anchor individually date-shifted, repaired or diner-changed selection, permanent exception and cancelled sibling, successful adoption receipt. | Preserve known histories/terms/counters/flags; derive schedules only from known metadata/original adoption response. Authorized repair and owner series amendment retain/exclude members correctly; original creation/adoption receipts remain exact after new changes. P13/P16/P22/P23. |
| Stage4 ->4 | Applied/unapplied/stale plans, closures, old policy snapshots, reassigned histories, multiple series flags/schedules, all seven successful receipt families plus failed keys. | Atomic read-only snapshot and replacement import, no source-process/files/volume/network dependency. Restore applied detection/local staleness/closures/counters, repeat without duplication, invalid rollback, reset clears everything. P19/P21. |

No downgrade requirement is invented. Earlier source services are built from independently accepted immutable revisions when available; source-stage lack of acceptance is a release dependency, not permission to substitute synthetic fixtures for required populated upgrade evidence. Opaque exports/private sessions stay out of the repository and room messages. Known native histories are immutable; old records with no recorded history do not license reconstruction of unobserved changes.

## Ambiguities and reasoned interpretations

| Topic | Interpretation / verification limit |
|---|---|
| Replay, already applied and stale | Full receipt resolution is normative before current-state checks. An already-applied plan under a different key yields plan_already_applied before stale_plan, because applying it necessarily increments its restaurant revision and the contract explicitly prescribes the former error. This total order does not invent priorities between unrelated malformed controls/permission failures. |
| Zero-moved application | First application records an active closure and increments restaurant revision once even with no moved/considered bookings. Reservation and series revisions/history stay unchanged. Previews never increment. An all-no-op batch retains counters, following the earlier adopted ambiguity resolution. |
| Series amendment no-op eligibility | Only a real series change checks its old accepted cutoff, per explicit Stage4 wording. Excluded/no-op members cannot block an otherwise successful collective operation on cutoff alone. Valid stale series revision still fails before occurrences, including empty/all-no-op sets. Ordinary individual/batch editable no-ops retain their inherited cutoff rules. |
| Control-versus-stale ties | The contract orders a valid mismatch before occurrence cutoff/booking validation. It does not impose a total order between stale_revision and invalid from_index/local_time controls; validate controls before occurrence work, and do not use an unspecified tie as a fabricated blocker. |
| Missing legacy metadata | Preserve every known counter/history/status/identity/timestamp/receipt exactly. Missing revision/accepted terms use the adopted truthful revision1/policy0 baseline; missing restaurant counter initializes0 without counting invented earlier edits. Missing history initialization recipe is documented by the owner and future native histories verified; do not fabricate past edits or timestamps. |
| Original schedules | Preserve native original scheduled dates when present; otherwise recover them from the preserved original adoption response or known immutable adoption metadata. Current shifted anchor/date is insufficient. Stage1/2 have no native series until adopted; Stage3 imports must support later collective amendments. |
| Explicit instant offsets | Z is treated as explicit UTC, consistent with RFC3339 inherited conventions; numeric offsets also qualify. Closure equality/ordering/overlap compares instants, including feasible fractions, independently of text/local zone. Equivalent offset spelling need not be preserved outside immutable original receipts; endpoints cannot silently change represented instants. |
| Applied plan browser reflection | Fresh authoritative search/lookup/current confirmation presentation must reflect current assigned labels/sets. No idle polling or cross-tab/reload recovery is newly required. Historical server receipt JSON and pending exact key/body remain unchanged; a successful server replay is still required to resolve uncertainty. |
| Manager roles in old imports | Missing manager_user_ids remains[]; neither import nor adoption invents operator privilege. Stage1/2 imported-owner flows exercise adoption/amendment; populated Stage3 imports with actual managers exercise operator repairs. Native manager authorization remains binding. |
| Numeric/resource feasibility | No unsupported numeric limit, rounding or binary-float objective is allowed. Exact capacity sums/objectives/receipt values with feasible output size must satisfy actual budgets. Arbitrarily separated exponents can require arbitrarily many output digits, conflicting mathematically with finite2GiB/5s; this adopted specification boundary is reported honestly and never used to waive feasible exact cases. Published policy capacity1..100 limits only that declared policy endpoint, not all legacy policy0 fixtures. |
| Unspecified earlier edge cases | Gap-valued opening/closing boundary behavior and legacy history initialization remain earlier documented ambiguities. Preserve adopted first-occurrence/absolute closing interpretation for specified cases; do not import later-stage rules backwards or invent missing APIs/screens. |

Conductor message26741e7e-7f78-408b-ac99-234564fd106e adopted the replay/already-applied/stale order, zero-moved closure counter, stale/no-op/real-change-only cutoff behavior, truthful imported counter/schedule/role baseline and current-read versus historical-receipt browser interpretation after checking the complete contract. Feasible bounded exact output remains binding. These interpretations are deliberately separate from normative rows where wording is ambiguous. No unobserved Stage4 source or visible-check behavior was used as a substitute for the specification.

## Acceptance and evidence obligations

A release is blocked by any reproducible violation of a stated CRITICAL/HIGH obligation on its exact integrated candidate. Formal acceptance requires independent verifier attribution (PRODUCT DEFECT versus verifier/infrastructure defect), exact revision/provenance, independent calibration, complete earlier regression, objective witnesses and bounded exhaustive model, real coordinated concurrency, each populated upgrade path, rendered browser cases and measured offline resource budgets. For every blocking row attach independent case IDs and an observed result; aggregate official/owner pass counts alone do not close it. MEDIUM obligations remain contractually required and should be checked alongside their procedures.

The auditor's completion criterion is a coherent730-row/88-procedure canonical ledger, unique inherited stable IDs and valid dependency/procedure mappings, sanitized owned-file-only commit, FULL evidence SHA/absolute path handoff and released serialized index. All production rows remain OPEN/unverified until independent evidence on a Stage4 candidate exists. No Stage4 acceptance is claimed by this document.

Preparation checks completed:730 unique rows, all557 inherited IDs retained, all88 procedure definitions uniquely mapped, owner/risk/compatibility schemas valid, full-ID dependencies resolved and new dependency paths acyclic. Sanitization matched no actual credential literal, private key, raw environment assignment or opaque export payload. Independent synthetic complete-option enumeration confirmed the three movement/waste/reference-vector witnesses, five additional accepted-capacity/pair/fixed-interval/prior-closure/reversal witnesses, exact fractional half-open adjacency and an infeasible case. Waste-before-movement and summed-rank variants were rejected, and reference renaming changed the tie-breaking assignment as predicted. These observations validate this analysis model only; no Stage4 service, Docker build, browser or formal production campaign was executed by this seat.

Repository evidence may contain synthetic IDs/calendar/capacity examples and immutable code/contract hashes, but no actual passwords, bearer/session tokens, private exported state, raw environments, caches or peer-owned files. Diagnostics and private transfer payloads belong outside result. This ledger is the only Stage4 analysis artifact; prior frozen/complete stage evidence and official checkout/specs/harness/shipped checks remain untouched.
