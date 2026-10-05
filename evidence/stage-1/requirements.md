# Tablekeeper Stage 1 requirements and acceptance ledger

This is the single canonical contract ledger for the FINAL SUBMISSION RUN, derived independently from the complete Stage 1 specification supplied by the Conductor in room message `7d6930a1-10ef-4190-9d81-38bdbc0e5b5e`. Source baseline: `a0ba09453b7630fcb5eed6982fe19a9a1aa0eb73`. Only Stage 1 HTTP behavior is in scope. No production acceptance is asserted here. No shipped checks, existing product source, API documentation or schemas were used to derive the contract.

## Reading and updating the ledger

Each row is an atomic normative obligation. IDs are stable: retain them when recording evidence or revising interpretation. Source sections refer to the supplied specification. `C` = CRITICAL, `H` = HIGH, `M` = MEDIUM, `L` = LOW. Risk tags: `TX` transaction/rollback, `CC` concurrency/serialization, `RP` replay, `AU` authorization/privacy, `TM` temporal/calendar, `VA` type/value/boundary validation, `OR` order/precedence, `ST` state/replacement/portability, `HTTP` observable protocol, `DEP` deployment, `SC` scope. Dependencies are requirement IDs or groups; `-` means no prerequisite beyond the shared protocol. `Vxx` identifies the independent verification procedure below.

Production owner recommendation for every row is Systems Engineer unless explicitly marked `EE` (Experience Engineer owns delivery documentation/API contract documentation) or `CON` (Conductor owns submission scope/release coordination). Adversarial Verifier owns independent evidence for every row; the Contract Auditor owns this ledger, not production. Recommendations are not architecture requirements.

Every row currently has **status OPEN / production not verified**, **visible-check coverage UNKNOWN (not inspected)** and **evidence reference NONE**. These are explicit record defaults, not a claim that checks are absent. The assigned V procedure is the independent-evidence obligation for that row. Later verification should record exact production FULL SHA, procedure/case identifiers, observed result and sanitized evidence reference against these IDs in this file or an exact-SHA verifier report linked here. Passing visible tests alone does not close an untested obligation.

Compatibility column: `S` means the observable state/identity/configuration must survive unchanged export -> import in a different process (§10); `R` additionally covers original successful idempotency receipts; `-` means no durable compatibility obligation attaches to that row. Stage 1 has format version 1 only; no later-version migration or restart persistence is invented. The cross-process compatibility matrix below specifies all required paths.

## Canonical atomic requirements

### Scope delivery and runtime

| ID | Source | Atomic requirement | Risk/tags | Dependencies | Verify | Compat |
|---|---|---|---|---|---|---|
| TK1-SC-01 | §1 | Expose the required service through HTTP; no UI is required. | M SC | - | V01 | - |
| TK1-SC-02 | Intro | Do not use source code from existing products in this domain. Owner CON. | H SC | - | V01 | - |
| TK1-SC-03 | Intro | Do not use existing domain-product API documentation or schemas. Owner CON. | H SC | - | V01 | - |
| TK1-SC-04 | Assignment | Stage 1 submission folder implements Stage 1 only. Owner CON. | H SC | - | V01 | - |
| TK1-RUN-01 | §2 | Deliver a Dockerfile that builds the submitted HTTP service. | H DEP | SC-01 | V01 | - |
| TK1-RUN-02 | §2 | Deliver RUN.md with a build/start command requiring no manual setup. Owner EE. | M DEP | RUN-01 | V01 | - |
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
| TK1-HTTP-01 | §3.4 | JSON requests/responses use application/json; charset=utf-8 (204 has no content). | M HTTP | - | V03 | - |
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
| TK1-FIX-06 | §4 | Restaurant/table configuration is supplied through reset only; creation endpoints are out of scope. | M SC | FIX-02 | V02 | S |
| TK1-FIX-07 | §4 | Preserve restaurant IANA timezone and local-time configuration. | H TM ST | FIX-02 | V02,V09 | S |
| TK1-FIX-08 | §4 | Missing weekday entry denotes a closed day. | H TM | FIX-07 | V08 | S |
| TK1-FIX-09 | §4 | Use slot_minutes grid anchored at opening time. | H TM VA | FIX-07 | V08,V10 | S |
| TK1-FIX-10 | §4 | Use each restaurant's reservation duration. | H TM ST | FIX-07 | V08,V10 | S |
| TK1-FIX-11 | §4 | Use each restaurant's cancellation cutoff. | H TM ST | FIX-07 | V12,V13 | S |
| TK1-FIX-12 | §4 | Use each table's capacity. | H VA ST | FIX-02 | V08,V10 | S |
| TK1-FIX-13 | §4 | Seeded users can immediately log in with fixture passwords. | H AU ST | FIX-02,AUTH-12 | V02,V04 | S |
| TK1-FIX-14 | §4 | Seeded confirmed reservations retain supplied body fields, id, reference and user_id. | H ST AU | FIX-02 | V02,V11 | S |
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
| TK1-ERR-09 | §5 | A nonempty Idempotency-Key exceeding 255 characters is 422 validation_failed on both required-key endpoints. | H VA RP | ERR-05 | V06 | - |
| TK1-ERR-10 | §5 | Missing/malformed/unknown bearer token is 401 unauthenticated on protected endpoints. | H AU | ERR-01 | V05 | - |
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
| TK1-AUTH-10 | §§6,8,10 | Health/reset/signup/login/restaurants list/detail/availability/export/import require no token. | H AU HTTP | - | V05 | - |
| TK1-AUTH-11 | §§6,8,11 | Every other specified endpoint requires bearer authentication. | C AU | AUTH-08 | V05 | S |
| TK1-AUTH-12 | §6 | Store passwords only using a password-hashing function or equivalent; plaintext storage prohibited. | C AU ST | - | V04,V18 | S |

### Occupancy and idempotency

| ID | Source | Atomic requirement | Risk/tags | Dependencies | Verify | Compat |
|---|---|---|---|---|---|---|
| TK1-OCC-01 | §1 | Two confirmed bookings never overlap on the same table. | C TX CC | FIX-10 | V10,V16,V20 | S |
| TK1-OCC-02 | §1 | Occupancy is the half-open absolute interval [start,start+duration). | C TM TX | FIX-10,TIME-05 | V10,V09 | S |
| TK1-OCC-03 | §1 | Concurrent competing writes preserve OCC-01. | C CC TX | OCC-01 | V16 | S |
| TK1-OCC-04 | §1 | Retries never create duplicate bookings. | C RP CC | IDEM-08 | V06,V16 | R |
| TK1-OCC-05 | §1 | Rejected requests create no partial bookings. | C TX | OCC-01 | V10,V13,V14,V20 | S |
| TK1-IDEM-01 | §7 | Create and moves require Idempotency-Key. | H RP HTTP | AUTH-11 | V06 | - |
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
| TK1-AV-04 | §8 | Enumerate every opening-anchored grid slot whose reservation fits by closing. | H TM OR | FIX-09,FIX-10,TIME-05 | V08,V09 | S |
| TK1-AV-05 | §8 | Each slot exposes full local YYYY-MM-DDTHH:MM and offset-bearing starts_at for the same instant. | H TM HTTP | TIME-01 | V08,V09 | S |
| TK1-AV-06 | §8 | Available tables belong to the queried restaurant. | H ST | FIX-02 | V08 | S |
| TK1-AV-07 | §8 | Available tables have capacity at least party_size. | H VA | FIX-12 | V08 | S |
| TK1-AV-08 | §8 | Available tables have no overlapping confirmed occupancy. | C TX TM | OCC-01,OCC-02 | V08,V16 | S |
| TK1-AV-09 | §8 | Available table IDs appear in fixture order. | H OR ST | FIX-02 | V08,V18 | S |
| TK1-AV-10 | §8 | Keep slots with no available tables, with an empty array. | H HTTP | AV-04 | V08 | S |
| TK1-AV-11 | §8 | Closed day returns slots: []. | H TM HTTP | FIX-08 | V08 | S |
| TK1-AV-12 | §8 | Returned starts_at_local can be used unchanged to create a reservation. | H TM VA | AV-05,CREATE-01 | V08,V09 | S |

### Creation reads and reservation lifecycle

| ID | Source | Atomic requirement | Risk/tags | Dependencies | Verify | Compat |
|---|---|---|---|---|---|---|
| TK1-CREATE-01 | §8 | Create accepts restaurant_id, table_id, starts_at_local and party_size and returns 201 with the specified reservation fields. | H HTTP ST | IDEM-01 | V10 | S |
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
| TK1-GET-03 | §8 | List entries have create-response shape; no records returns reservations: []. | M HTTP | GET-01 | V11 | S |
| TK1-GET-04 | §8 | Reference lookup returns caller's record; unknown/another owner's reference returns 404 without leaking existence. | C AU | AUTH-11 | V05,V11 | S |
| TK1-GET-05 | §8 | List includes both confirmed and cancelled reservations. | H ST | GET-01 | V11,V12 | S |
| TK1-CANCEL-01 | §8 | Successful cancel returns 200 with current reservation state and status cancelled. | H HTTP ST | GET-04 | V12 | S |
| TK1-CANCEL-02 | §8 | Cancellation releases occupancy immediately for the next availability read. | C TX CC | CANCEL-01,AV-08 | V12,V16 | S |
| TK1-CANCEL-03 | §8 | Cancelling an already-cancelled record returns 200 with current state. | H ST OR | CANCEL-01 | V12 | S |
| TK1-CANCEL-04 | §8 | Confirmed cancellation at/after cutoff boundary gives 409 cutoff_passed. | H TM OR | FIX-11 | V12 | - |
| TK1-CANCEL-05 | §8 | Cancellation of another owner's/unknown reference returns 404 not_found. | C AU | GET-04 | V05,V12 | - |
| TK1-PATCH-01 | §8 | PATCH accepts any subset of table_id, starts_at_local, party_size; omitted fields retain current values. | H ST VA | GET-04 | V13 | S |
| TK1-PATCH-02 | §8 | PATCH requires no idempotency key. | H HTTP | PATCH-01 | V13 | - |
| TK1-PATCH-03 | §8 | PATCH applies the same destination validation and codes as create. | H VA TM | CREATE-07..13,ERR-06..07 | V13 | - |
| TK1-PATCH-04 | §8 | PATCH cutoff uses current start, not the proposed start. | H TM OR | FIX-11 | V13 | - |
| TK1-PATCH-05 | §8 | PATCH of cancelled record returns 409 reservation_cancelled. | H ST OR | CANCEL-01 | V13 | - |
| TK1-PATCH-06 | §8 | Successful PATCH releases old occupancy and acquires new occupancy together. | C TX CC | OCC-01 | V13,V16 | S |
| TK1-PATCH-07 | §8 | Failed PATCH preserves entire original booking and occupancy. | C TX ST | PATCH-06 | V13,V20 | S |
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
| TK1-MOVE-06 | §11 | Each item accepts PATCH fields and retains omitted values. | H ST VA | PATCH-01 | V14 | S |
| TK1-MOVE-07 | §11 | Ignore unknown item fields. | H VA | HTTP-03 | V14,V15 | - |
| TK1-MOVE-08 | §11 | Each booking keeps identity, owner and creation time. | C ST AU | PATCH-08 | V14,V18 | S |
| TK1-MOVE-09 | §11 | Cancelled listed booking returns 409 reservation_cancelled. | H ST OR | PATCH-05 | V14 | - |
| TK1-MOVE-10 | §11 | Apply each listed booking's existing-start cutoff. | H TM OR | PATCH-04 | V14 | - |
| TK1-MOVE-11 | §11 | Non-occupancy errors use ordinary amendment codes. | H VA OR | PATCH-03 | V14 | - |
| TK1-MOVE-12 | §11 | Non-occupancy errors take precedence in input order. | C OR TX | MOVE-11 | V14 | - |
| TK1-MOVE-13 | §11 | Cutoff errors precede other proposed changes for that booking. | C OR TM | MOVE-10 | V14 | - |
| TK1-MOVE-14 | §11 | Overlap among resulting listed bookings gives 409 table_unavailable. | C TX | OCC-01,MOVE-12 | V14 | - |
| TK1-MOVE-15 | §11 | Resulting overlap with an unlisted confirmed booking gives 409 table_unavailable. | C TX | OCC-01,MOVE-12 | V14,V16 | - |
| TK1-MOVE-16 | §11 | Unchanged listed bookings retain occupancy. | C TX ST | MOVE-06 | V14 | S |
| TK1-MOVE-17 | §11 | All moves commit together or none commit, including records, occupancy and retry keys. | C TX RP CC | MOVE-14..16,IDEM-12 | V14,V16,V20 | R |
| TK1-MOVE-18 | §11 | Success returns 201 with a reservations array. | H HTTP | MOVE-17 | V14,V15 | R |
| TK1-MOVE-19 | §11 | Replays return original response with 200 after later amendments/cancellations. | C RP ST | IDEM-13,MOVE-18 | V15,V18 | R |
| TK1-MOVE-20 | §11 | No-op moves retain all existing values. | C ST TX | MOVE-06 | V14,V15,V18 | S |
| TK1-MOVE-21 | §11 | Export/import preserves successful batch receipts as well as resulting bookings. | C RP ST | XFER-17,MOVE-18 | V18 | R |
| TK1-MOVE-22 | §11 | Successful reservations array preserves input order. | H OR | MOVE-18 | V14,V15 | R |
| TK1-MOVE-23 | §11 | Successful reservations array includes unchanged items. | H HTTP ST | MOVE-18 | V14,V15 | R |
| TK1-MOVE-24 | §11 | moves length must be 1..8; other lengths give 422 validation_failed. | H VA | MOVE-03 | V14 | - |
| TK1-MOVE-25 | §11 | References must be distinct; duplicates give 422 validation_failed. | H VA | MOVE-03 | V14 | - |

## Explicit precedence map

1. A required-key write must have a parseable JSON object and authenticated caller before receipt lookup. Unparseable JSON is 400; invalid authentication is 401. The relative order of parsing versus authentication when both fail is not specified.
2. An absent/empty required key is 400 missing_idempotency_key; a key longer than 255 is 422 validation_failed. Receipt resolution precedes destination field validation/resource checks. A used key with a different body gives 409 even if that body would otherwise be invalid; a true replay returns its original 200 receipt despite current cutoff, cancellation, resource changes or conflicts.
3. Wrong type is normally 400, correct-type invalid value is normally 422. Explicit exceptions win: party_size invalid types/values -> 422; incorrectly formatted starts_at_local **strings** -> 422; moves shape/duplicates -> 422; invalid import state/envelope rules -> 422. A nonstring ordinary starts_at_local remains 400. Required missing fields are 422.
4. Reservation ownership hides existence: foreign reference is 404, overriding generic forbidden. Authenticate before protected resource visibility checks. Public test endpoints remain unauthenticated even though exports may contain private state.
5. Already-cancelled cancellation returns current state 200; apply cutoff to a still-confirmed cancellation. PATCH of cancelled booking gives 409 reservation_cancelled. Exact equality at the cutoff boundary counts as cutoff passed. Proposed future start never bypasses current-start cutoff.
6. Batch: validate envelope/references, then determine non-occupancy errors in input order. For a given eligible record, current cutoff precedes proposed-field changes. Check final occupancy only after non-occupancy checks; even an earlier overlap loses to a later non-occupancy error. Evaluate all final listed states together, retaining unchanged occupancy and excluding only listed old states that are actually replaced. This permits table/time swaps while rejecting final collisions.
7. No universal priority is specified among ordinary create destination errors, between cutoff and cancelled PATCH state, between missing key and invalid authentication, or between batch same-restaurant violations and other item errors. Do not mark an implementation wrong solely for an invented ordering; use isolated-error tests plus explicitly specified compound-error cases.

## Risk model and dependency ordering

CRITICAL release blockers are the OCC group; AUTH-11/12 and owner visibility; IDEM scoping, receipts, precedence and single-commit behavior; PATCH atomic transfer/rollback and identity; TIME first occurrence/absolute duration; XFER snapshot/replacement/rollback/continuity/private artifacts; and MOVE final-state occupancy/all-or-nothing/no-op/precedence. A single counterexample blocks acceptance. ERR-13 also blocks acceptance if malformed or concurrent traffic yields a 5xx. HIGH obligations are externally observable validations/codes, cutoff boundaries, availability filtering/order, fixture fidelity, DST offsets, deployment independence and bounded concurrency. Every normative requirement remains binding regardless of risk label.

Recommended implementation dependency order (not prescribed architecture): runtime/error envelope -> fixture model and safe state replacement -> auth/hash/token identity -> zone resolution/grid/absolute intervals -> reservation records and occupancy invariant -> receipt identity and atomic receipt+write publication -> availability/create/reads -> cancel/PATCH -> simultaneous moves -> portable full-state snapshot/import -> whole-state concurrent interactions and exact-SHA release verification. Receipt/state transfer design must be considered before implementation; retrofitting only reservation records cannot satisfy §10. Owner Systems Engineer covers state/protocol; Experience Engineer covers RUN.md/documented HTTP interface; Conductor coordinates exact revisions; independent verifier must test observable outcomes against this ledger.

## Independent verification catalogue and edge cases

All dates, labels and booking names below are synthetic specification examples. Never store actual credentials, bearer tokens or raw exports in repository evidence. Use ephemeral test inputs and report counts, statuses, reference comparisons or redacted summaries. Derive expected answers independently; do not reuse production slot generation or validation helpers.

| Procedure | Concrete verification obligation and coverage expectation |
|---|---|
| V01 | Build only stage-1/Dockerfile and run the image alone with no outbound network, 2 CPU/2 GiB. Test custom PORT and default 8080 through mapped ports. Measure healthy response <=60s; confirm store readiness by a real API request. Reproduce RUN.md. Inspect included assets, build scope, provenance and sanitized commit. Harness is container HTTP only; language/package imports on host are not an acceptance requirement. |
| V02 | Reset fixture A, mutate accounts/tokens/reservations/receipts, reset fixture B, and show A records/credentials/tokens/keys disappear. Repeat B reset. Seed nontrivial restaurant/table IDs, order, capacities, hours, users and reservations; verify immediate login and seeded occupancy. Include exactly 64-character IDs and over-limit invalid input. Unspecified malformed fixture behavior beyond §5 must not define the contract. |
| V03 | Endpoint-by-endpoint type/value matrix: omitted field, null, array/object/string/boolean/numeric substitutions, correct-type invalid values, invalid dates, malformed JSON, nonobject body, ignored unknown fields/queries. Check actual status/code/error message and content type. party_size 0,-1,1,capacity,capacity+1,1.5,true,"4"; reject query 1e9/4.0/+4 and invalid calendar dates. Check local format seconds/offset/Z/date-only, numeric local start, key lengths 0,1,255,256. Require no 5xx. |
| V04 | Signup/login success, 7/8-character password boundary, duplicate email including concurrent signup, wrong/unknown login. Multiple logins retain all old tokens. Confirm seeded credentials work and tokens remain valid across import. Independently inspect password storage/hash verification; HTTP success cannot prove plaintext prohibition. No raw hash/token/export evidence is committed. |
| V05 | Enumerate every public/protected route with absent, malformed and unknown tokens. For two owners, test reference GET/cancel/PATCH/moves with foreign and nonexistent references: same 404 class, no leaked booking fields; list contains only owner records. Public browsing works before signup. Test controls work without auth, as expressly required. |
| V06 | Create and moves independently: missing/empty/oversize keys; same key/body replay reordered object keys/whitespace; changed body including ignored unknown fields -> conflict; conflict precedes invalid party/nonexistent table; different users independent; same key on create vs moves independent. Failed validation/occupancy request then corrected request with same key -> first-use 201. Preserve array ordering in JSON equality; reordered arrays are different values. |
| V07 | Multi-restaurant reset; public list shape and complete fixture-shaped detail; unknown detail 404. Verify opaque IDs are not inferred by syntax. Restaurant-list ordering is not specified; do not demand a particular sort. |
| V08 | Use unusual opening anchor (e.g. 18:10), multiple slot/duration combinations, end exactly close, just beyond close, closed day, tables below/equal/above party capacity. Maintain deliberately nonsorted fixture table order. Seed overlaps and cancellations; full slots still appear with []. Cross-restaurant tables never appear. Round-trip each available local slot into booking. Compare ascending grid enumeration, not global server timezone. |
| V09 | Independently compute Berlin and New York's four specified DST dates using an independent IANA oracle/known transition instants. Spring candidates in gap excluded; direct create/PATCH/moves at a gap -> invalid_local_time. Fall repeated starts appear once with pre-transition offset; second occurrence offset/Z input rejected as nonbare local. For New York 2026-11-01 01:30 first occurrence +90 real minutes -> 02:00 -05:00, not 03:00. Berlin 2026-10-25 01:30 +90 -> 02:00 +01:00. Check start/end offsets separately, elapsed UTC duration, overlap across fold/gap, opening-end boundary and normal winter/summer dates. Dates from fixtures need not be near today. |
| V10 | Create shape/ID/reference/created_at, grid, hours/end, capacity, unknown/mismatched resource codes. Half-open adjacency both directions succeeds; equal starts and partial/containing/contained overlaps fail. Different tables/restaurant records independent. Past valid creation succeeds. Include table/reference ID collision potential after seeded/cancelled reservations and concurrent generation. Failed requests leave no extra record/occupancy. |
| V11 | Empty list, own confirmed+cancelled list with timestamps deliberately out of insertion order and differing offsets. Sort by actual starts_at instant descending. Detail equals current create-shaped record. After moving start, recheck list ordering. Equal-start tie-break is unspecified; only maintain a consistent implementation convention. |
| V12 | Cancel active booking safely before cutoff, at exact now=start-cutoff and after start; use wide margins for live-clock checks plus independent boundary validation where clock control exists. Cancelled record remains listed; repeated cancel succeeds even after cutoff and after table rebooking. Next availability releases only its interval. Unauthorized cancel cannot change occupancy. |
| V13 | PATCH each field singly and all together; omitted fields retained, no key required. Own-booking unchanged target does not conflict with itself. Future target cannot evade old-start cutoff. Failure for each destination rule preserves complete old JSON and occupancy; success frees old and acquires new together, preserving ID/reference. Cancelled PATCH rejected. Empty/unknown-only body interpretation is documented below. |
| V14 | Moves sizes 0/1/8/9, missing/null/nonarray moves, nonobject items, missing/nonstring/duplicate refs, foreign/unknown refs, mixed restaurants. Test each ordinary amendment error, current cutoff, cancellation and unknown fields. Include successful two-table swap, time swap/cycle, partial-field updates and no-op batch. Check all item values/identity/creation time unchanged for no-ops, input order and unchanged occupancy. Earlier occupancy conflict + later validation error -> later non-occupancy code; earlier invalid item + later cutoff -> earlier item's code; one item's cutoff + invalid proposed field -> cutoff. Failure preserves every record/slot/key. |
| V15 | Create receipt then PATCH/cancel; replay still has original status/timestamps/start/table, not current record. Successful moves receipt then amend/cancel some records; replay returns original ordered array and has no new effects. Replay no-op batch and changed-body conflict. Same key cross-path requests both first-use succeed with independently appropriate bodies. |
| V16 | Barrier-start up to 50 HTTP requests: same unused key/body -> one 201/rest 200/same JSON/one effect; same key/different bodies -> one committed body and remaining appropriate conflicts; distinct keys/users contest one interval -> one success, rest table_unavailable. Overlapping create/PATCH/moves/cancel races preserve final invariant and records/receipt consistency. Race no-op moves with conflicting create. Concurrent sessions/signup do not corrupt accounts. Measure limits/timeouts and check every response for 5xx. Repeat nontrivial schedules; final reads and independent interval audit supplement status counts. |
| V17 | Export empty/seeded/rich modified state and inspect wrapper only. Snapshot read-only: compare API observations before/after without writes. Race export with multi-record transaction; destination snapshot contains all-before or all-after, never torn booking/receipt pairs. Subsequent source writes cannot alter an already-taken snapshot. |
| V18 | Source A: seed config/accounts/bookings, signup/log in twice, create keyed receipt, amend/cancel original record, successful moves/no-op moves and a failed key. Export privately; import unchanged into independently started B on another port with no shared files/volume and A unavailable. Old A tokens/passwords work, exact identities/statuses/timestamps/references/config order retained, original receipts replay with 200 and no effect; failed keys return normal first use. B's old credentials/tokens/records/receipts disappear. Mutate B then reimport A twice: no duplicates, original state restored. Export B and import into C; repeat continuity assertions. Reset B then prove all imported identities/tokens/receipts removed. Delete private snapshots after tests. |
| V19 | Invalid import: malformed JSON ->400; missing wrapper fields, wrong track/version, corrupt/invalid state ->422. Check complete destination API state, logins/tokens and receipt behavior before/after every rejection. Test correct-type invalid values and type conflict interpretation below separately. Repeated valid import after rejection still succeeds. |
| V20 | Interactions: export vs batch/create receipt commits, invalid import vs requests, reset/import vs authenticated writes, cancellation vs replay, PATCH vs batch on same record, independent users contending table. Externally observed states must correspond to a complete valid serialization; no mixed fixture generations, dangling owners/tables, torn receipts or partial moves. Reset/import success forms replacement boundary: all subsequent reads use replacement state. Test rejected operation snapshots through public API/redacted structural comparison, never raw committed exports. |

## State transaction and no-op acceptance model

At each visible committed state, independently enumerate confirmed intervals for every table and prove no pair satisfies `a.start < b.end && b.start < a.end`. Adjacent ends/starts are legal. Cancelled bookings never occupy a table. Atomic publication comprises record(s), occupancy and successful request receipt together. A retry after any ordinary 4xx must not find a spent key; a successful receipt must not exist without its complete booking effect. Concurrent calls can have any valid serialization consistent with already-completed responses; exact scheduler order is not specified.

PATCH must check against other bookings while excluding its own replaced interval. Batch must compute final state against unlisted confirmed bookings and all listed final bookings; validating each move against every listed old booking incorrectly rejects legal swaps. An unchanged listed item still blocks occupancy. A no-op batch must not rewrite timestamps, regenerate IDs/references, change status/owner, reorder results or free its occupied interval. The batch receipt is a new successful request receipt even when every booking stays unchanged. Replay is a read of historical response, not a rerun of current mutation logic.

Export captures all state needed for both current records and historical successful responses, including cancelled/amended originals. Account/password-hash/token relationships, record owners/tables/config, original JSON bodies, request namespace and receipt responses must agree. Invalid import validation happens before state replacement; an attempted partial import cannot invalidate destination credentials or erase receipts. No dependency on restart persistence, external queue/storage or outbound runtime networking is permitted or needed.

## Compatibility matrix

| Required source -> destination | Required continuity | Independent evidence |
|---|---|---|
| Stage 1 format 1 A -> fresh independent Stage 1 B | Full account/hash/token/config/reservation/identity/timestamp/receipt fidelity; A unavailable. | V18 |
| A format 1 -> populated B | Replacement removes all B credentials/data/receipts; A survives exactly. | V18 |
| Same A snapshot -> B repeatedly, including after B mutations | Restore A state each time without duplicate identities/occupancy or spent failed keys. | V18,V19 |
| A -> B -> export B -> fresh C | Portable state and replay/credential continuity across successive processes. | V18 |
| Invalid snapshot -> populated B | No replacement/merge/partial credential or record change. | V19 |
| Imported B -> reset with fresh fixture | Imported identities/tokens/receipts/config removed; only fixture remains. | V02,V18 |

No source -> later-stage upgrade path is supplied. No cross-implementation format compatibility, expired-token policy, abrupt-restart recovery or backward compatibility with unpublished formats is required.

## Ambiguities and reasoned interpretations

These are analysis findings, not added normative requirements. Route disagreements to the Conductor; do not ask the human operator during this run.

1. **DST fitting and opening boundaries.** §8's slot+duration<=closes shorthand is ordinary wall-time text; §9 expressly makes duration absolute. Interpret fitting as resolved start instant + real duration <= resolved closing instant, while candidate grid uses local minute steps. Repeated starts and repeated boundaries use first occurrence consistently. A gap-valued opens/closes is not defined: fixture text permits HH:MM but does not state how nonexistent business boundaries resolve. Conservative recommendation: preserve the local grid anchor and compare against the transition instant reached at the first valid local time after the gap; flag any actual test case separately rather than assert this interpretation as normative. Test normal valid boundaries on transition days to verify all explicit DST obligations without depending on this gap-boundary choice.
2. **Type rules in moves/import.** Explicit invalid moves shape ->422 overrides generic wrong-type ->400 for the envelope/array/items/reference structure. Ordinary PATCH item field types still use §5 with party_size exception. Import invalid state and missing/wrong track/version explicitly ->422; an envelope field's gross wrong JSON type also meets §5's wrong-type rule. Recommend using 422 for invalid export-envelope/state semantics under §10, keeping malformed JSON/nonobject body at 400. The contract does not fully settle gross envelope-type precedence; report such cases distinctly.
3. **Empty PATCH.** Any subset plus ignored unknown fields includes the empty subset. Recommend treating empty/unknown-only PATCH as a no-op on an eligible confirmed record, subject to current ownership/cancelled/cutoff checks. PATCH success status is not explicitly specified; recommend 200 with current create-shaped state. Do not invent an empty-PATCH rejection or bypass cutoff.
4. **Cutoff clock.** Use actual current absolute time; cutoff passed when now >= current_start - cutoff_minutes. The spec supplies no controllable clock endpoint. Tests must avoid flaky live-time boundaries; inability to freeze time does not remove the exact equality requirement.
5. **JSON equality and ignored fields.** Compare parsed entire JSON body, including unknown fields, because §7 defines same JSON value while §3.4 only ignores fields for endpoint behavior. Object order/whitespace do not matter; array order does. Numeric JSON encodings denoting the same number should compare by value (e.g. 4 vs 4.0); party_size is integer-valued, excluding booleans. No maximum party_size is supplied beyond table capacity. Query digits are a separate stricter syntax rule. Duplicate JSON object-member handling and Unicode character-count details are unspecified; do not invent mandatory normalization.
6. **Ordering.** Available tables are in fixture order, moves results in input order, reservation list in descending actual start instant. Grid slots naturally follow increasing local grid steps. Tie-breaks for equal list starts, restaurant-list order and generated ID/reference format beyond stated limits are implementation choices; fixtures/config order must remain truthful through transfer.
7. **Fixtures and uniqueness.** Weekday set, same-day closes>opens and ID-length constraints are stated. The contract supplies no behavior for internally contradictory seeded occupancy/duplicate references or all malformed fixture substructures beyond shared §5. Do not invent fixture repair policies. Successful generated references must be unique across all retained records, including seeds/cancellations; import must preserve valid exported state rather than regenerate it.
8. **Cancellation and batch error ties.** Already-cancelled cancel is 200 even when current clock is past cutoff. Cancelled PATCH/batch items report reservation_cancelled; cutoff precedes proposed changes for otherwise eligible items. Mixed batch restaurant checks versus item-order errors and cancelled-vs-cutoff ties are not fully ordered; isolate explicit requirements when asserting exact codes.
9. **Concurrent control operations.** Reset/import successful replacement and export atomic snapshot imply coherent whole-state visibility. The response of a write already in flight during replacement is not specified. Require a valid serialization and no torn state; do not demand a particular winner or new undocumented conflict code.

## Formal acceptance criteria and evidence boundaries

The ledger is ready for implementation handoff when all sections are traced, blockers are explicit, and the evidence file is sanitized and committed. That is separate from production acceptance. Production acceptance requires the Adversarial Verifier's formal verdict on the **exact production FULL SHA**, with a clean reproducible Stage 1 image, official HTTP checks and independent V01..V20 evidence that addresses every CRITICAL/HIGH row and all remaining normative requirements. Any omitted case must be reported as an evidence gap rather than silently passed. Changing production after verification invalidates the exact-SHA verdict until appropriate revalidation.

Evidence must distinguish contract-derived cases from visible-check coverage, prove rollback using before/after records and occupancy rather than status alone, prove concurrency using complete response sets plus final-state invariants, prove privacy across owners, and prove portability using separate processes with existing tokens/receipts. Hash-storage prohibition additionally needs independent storage/source inspection. The verifier owns acceptance; this document supplies obligations only and does not accept production.

Never modify official specification, harness or shipped checks. Never commit passwords, tokens, credentials, raw session exports, raw environment dumps or unneeded environment assignments. Preserve one authoritative ledger: deliberate corrections/evidence references belong here; no cosmetic addenda or overlapping requirement graphs are needed after formal acceptance.
