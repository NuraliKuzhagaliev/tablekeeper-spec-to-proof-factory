# Tablekeeper Stage 2 cumulative requirements and acceptance ledger

This is the single canonical cumulative contract ledger for Stage 2 of the FINAL SUBMISSION RUN. Authority is the complete Stage 1 plus Stage 2 specification supplied by the Conductor in room message `f6190e93-d4be-42ad-b9b3-606e3ab06a7c`. Stage 1 normative records are mapped from the existing 187-record ledger without renumbering. Stage 2 adds required browser flows, approved two-table bookings and upgrade continuity. This analysis does not implement or accept production. No existing domain-product code, API documentation, schemas or shipped checks were used to derive the requirements.

## Record conventions ownership and evidence

Every normative row has a stable ID, source, atomic obligation, risk/tags, dependencies, independent verification procedure and compatibility obligation. `C` = CRITICAL, `H` = HIGH, `M` = MEDIUM, `L` = LOW. Tags: TX atomicity/rollback; CC concurrency/serialization; RP retry/historical replay; AU auth/privacy; TM time/DST; VA type/value/range; OR deterministic ordering/precedence; ST state/import; UI browser behavior/races; QA visual/usability; HTTP protocol; DEP offline deployment; SC scope. Inherited dependencies abbreviate TK1 IDs; new dependencies use full IDs. A row is a contract obligation; verification cases and interpretations are evidence guidance, not new requirements.

Owner `S` = Systems Engineer (backend, container, RUN.md and delivery docs); `E` = Experience Engineer (stage-2/public/index.html, app.js, styles.css and browser behavior); `C` = Conductor (release/scope). All inherited rows default to S, with original CON annotations meaning C; the Stage 1 recommendation for documentation ownership is superseded by this explicit assignment. New rows have an Owner column. Adversarial Verifier owns independent execution and the formal verdict on the exact production FULL SHA; Contract Auditor owns only this evidence file.

Record defaults for every inherited and new row: **status OPEN / Stage 2 production unverified**, **visible-check coverage UNKNOWN (not inspected)**, **evidence reference NONE**. The referenced V/W procedure is an independent-evidence obligation. Stage 1 evidence is historical provenance, not proof of Stage 2 behavior. Stage 1 boundary findings were recorded at `b03ce55647b70a46f478ea50ba077e02945bcefe` in ledger revision `0cf8748edeaa61438afa7a35e136e48513adb8f7`. The verifier formally REJECTED that production SHA with independently reproduced TK1-VERIFY-001/002 in room message `b3ee2ac8-b9fc-4028-a26d-d26989be4083`, evidence commit `f476314d258a8e1955a58c9182d9ab9c009a62df`. That verdict applies only to the inspected Stage 1 revision; replacement verification remains open and must not be silently inherited as a Stage 2 pass or assumed failure at a future revision.

Compatibility: `S` = preserve current state, identities/config/owner/status/timestamps through required export/import; `R` = additionally preserve completed body/response receipts exactly; `B` = preserve browser session/form/pending retry across Stage 1->2 import between browser requests; `-` = no separate stored-state duty. Inherited S/R obligations apply to Stage 2 same-version transfer and Stage 1->2 upgrade. Export wrapper remains track tablekeeper / format_version 1; state remains opaque and portable. No Stage 2->1 downgrade, later-stage compatibility, abrupt-restart durability, cross-tab synchronization or reload recovery is invented.

## Inherited Stage 1 mapping

All 187 TK1 IDs remain active, with their original V01..V20 evidence obligations. The cumulative contract explicitly specializes the following records; every other inherited row retains its normative meaning. Compound API concepts now operate on each member of a table selection, while available_table_ids stays single-only. Stage 1 row wording below reflects these specializations; it is not a second independent ledger.

| Existing ID | Stage 2 specialization and source |
|---|---|
| TK1-SC-01 | HTTP API remains required; Stage 2 additionally requires HTML browser screens. |
| TK1-SC-04 | Assigned Stage 2 folder contains cumulative Stage 1+2 behavior, with no future-stage production. |
| TK1-HTTP-01 | JSON convention applies to API; named screen routes return HTML. |
| TK1-FIX-14 | Preserve seeded body/identity/owner; table_id or table_ids; default confirmed, explicit cancelled honored. |
| TK1-OCC-01; TK1-OCC-02 | Nonoverlap/half-open full duration applies to every member table. |
| TK1-AV-08 | Singles are unavailable when any overlapping confirmed single/pair contains that member. |
| TK1-CREATE-01 | Legacy request retained; table_ids accepted; current response has new selection shape. |
| TK1-CANCEL-02 | Cancellation frees every member immediately. |
| TK1-PATCH-01 | table_ids added; omitted selection/time/party fields retain current values. |
| TK1-MOVE-06 | table_ids added per item under ordinary amendment rules. |
| TK1-MOVE-14; TK1-MOVE-15; TK1-MOVE-16 | Final listed/unlisted overlap and unchanged occupancy consider all members. |

All inherited authentication, passwords, IDs, errors, time/DST, idempotency, cutoff, owner visibility, export/import replacement, no-op, batch ordering and resource limits still apply. Existing single-table clients continue to work. Historical Stage 1 receipt responses are preserved exactly; the general new response shape does not justify editing an original successful receipt (see interpretation P1).

## Active inherited atomic requirements

### Scope delivery and runtime

| ID | Source | Atomic requirement | Risk/tags | Dependencies | Verify | Compat |
|---|---|---|---|---|---|---|
| TK1-SC-01 |§1 + Stage 2 | Expose the required HTTP API; Stage 2 additionally requires the specified browser screens. | M SC | - | V01 | - |
| TK1-SC-02 | Intro | Do not use source code from existing products in this domain. Owner CON. | H SC | - | V01 | - |
| TK1-SC-03 | Intro | Do not use existing domain-product API documentation or schemas. Owner CON. | H SC | - | V01 | - |
| TK1-SC-04 |Assignment + Stage 2 | Assigned Stage 2 submission folder implements cumulative Stage 1 plus Stage 2 only. Owner CON. | H SC | - | V01 | - |
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
| TK1-FIX-06 | §4 | Restaurant/table configuration is supplied through reset only; creation endpoints are out of scope. | M SC | FIX-02 | V02 | S |
| TK1-FIX-07 | §4 | Preserve restaurant IANA timezone and local-time configuration. | H TM ST | FIX-02 | V02,V09 | S |
| TK1-FIX-08 | §4 | Missing weekday entry denotes a closed day. | H TM | FIX-07 | V08 | S |
| TK1-FIX-09 | §4 | Use slot_minutes grid anchored at opening time. | H TM VA | FIX-07 | V08,V10 | S |
| TK1-FIX-10 | §4 | Use each restaurant's reservation duration. | H TM ST | FIX-07 | V08,V10 | S |
| TK1-FIX-11 | §4 | Use each restaurant's cancellation cutoff. | H TM ST | FIX-07 | V12,V13 | S |
| TK1-FIX-12 | §4 | Use each table's capacity. | H VA ST | FIX-02 | V08,V10 | S |
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
| TK1-OCC-01 |§1 + Stage 2 | Two confirmed bookings never overlap on any member table in the same restaurant. | C TX CC | FIX-10 | V10,V16,V20 | S |
| TK1-OCC-02 |§1 + Stage 2 | Each member table occupies the half-open absolute interval [start,start+duration). | C TM TX | FIX-10,TIME-05 | V10,V09 | S |
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
| TK1-AV-08 |§8 + Stage 2 | Available single tables have no overlapping confirmed reservation containing that member. | C TX TM | OCC-01,OCC-02 | V08,V16 | S |
| TK1-AV-09 | §8 | Available table IDs appear in fixture order. | H OR ST | FIX-02 | V08,V18 | S |
| TK1-AV-10 | §8 | Keep slots with no available tables, with an empty array. | H HTTP | AV-04 | V08 | S |
| TK1-AV-11 | §8 | Closed day returns slots: []. | H TM HTTP | FIX-08 | V08 | S |
| TK1-AV-12 | §8 | Returned starts_at_local can be used unchanged to create a reservation. | H TM VA | AV-05,CREATE-01 | V08,V09 | S |

### Creation reads and reservation lifecycle

| ID | Source | Atomic requirement | Risk/tags | Dependencies | Verify | Compat |
|---|---|---|---|---|---|---|
| TK1-CREATE-01 |§8 + Stage 2 | Create accepts restaurant_id, legacy table_id or table_ids, starts_at_local and party_size; returns 201 with current specified reservation shape. | H HTTP ST | IDEM-01 | V10 | S |
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
| TK1-CANCEL-02 |§8 + Stage 2 | Cancellation releases every member's occupancy immediately for the next availability read. | C TX CC | CANCEL-01,AV-08 | V12,V16 | S |
| TK1-CANCEL-03 | §8 | Cancelling an already-cancelled record returns 200 with current state. | H ST OR | CANCEL-01 | V12 | S |
| TK1-CANCEL-04 | §8 | Confirmed cancellation at/after cutoff boundary gives 409 cutoff_passed. | H TM OR | FIX-11 | V12 | - |
| TK1-CANCEL-05 | §8 | Cancellation of another owner's/unknown reference returns 404 not_found. | C AU | GET-04 | V05,V12 | - |
| TK1-PATCH-01 |§8 + Stage 2 | PATCH accepts any subset of table_id or table_ids, starts_at_local, party_size; omitted fields retain current values. | H ST VA | GET-04 | V13 | S |
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
| TK1-MOVE-06 |§11 + Stage 2 | Each item accepts PATCH fields including table_ids and retains omitted values. | H ST VA | PATCH-01 | V14 | S |
| TK1-MOVE-07 | §11 | Ignore unknown item fields. | H VA | HTTP-03 | V14,V15 | - |
| TK1-MOVE-08 | §11 | Each booking keeps identity, owner and creation time. | C ST AU | PATCH-08 | V14,V18 | S |
| TK1-MOVE-09 | §11 | Cancelled listed booking returns 409 reservation_cancelled. | H ST OR | PATCH-05 | V14 | - |
| TK1-MOVE-10 | §11 | Apply each listed booking's existing-start cutoff. | H TM OR | PATCH-04 | V14 | - |
| TK1-MOVE-11 | §11 | Non-occupancy errors use ordinary amendment codes. | H VA OR | PATCH-03 | V14 | - |
| TK1-MOVE-12 | §11 | Non-occupancy errors take precedence in input order. | C OR TX | MOVE-11 | V14 | - |
| TK1-MOVE-13 | §11 | Cutoff errors precede other proposed changes for that booking. | C OR TM | MOVE-10 | V14 | - |
| TK1-MOVE-14 |§11 + Stage 2 | Any member overlap among resulting listed bookings gives 409 table_unavailable. | C TX | OCC-01,MOVE-12 | V14 | - |
| TK1-MOVE-15 |§11 + Stage 2 | Any member overlap with an unlisted confirmed booking gives 409 table_unavailable. | C TX | OCC-01,MOVE-12 | V14,V16 | - |
| TK1-MOVE-16 |§11 + Stage 2 | Unchanged listed bookings retain every member's occupancy. | C TX ST | MOVE-06 | V14 | S |
| TK1-MOVE-17 | §11 | All moves commit together or none commit, including records, occupancy and retry keys. | C TX RP CC | MOVE-14..16,IDEM-12 | V14,V16,V20 | R |
| TK1-MOVE-18 | §11 | Success returns 201 with a reservations array. | H HTTP | MOVE-17 | V14,V15 | R |
| TK1-MOVE-19 | §11 | Replays return original response with 200 after later amendments/cancellations. | C RP ST | IDEM-13,MOVE-18 | V15,V18 | R |
| TK1-MOVE-20 | §11 | No-op moves retain all existing values. | C ST TX | MOVE-06 | V14,V15,V18 | S |
| TK1-MOVE-21 | §11 | Export/import preserves successful batch receipts as well as resulting bookings. | C RP ST | XFER-17,MOVE-18 | V18 | R |
| TK1-MOVE-22 | §11 | Successful reservations array preserves input order. | H OR | MOVE-18 | V14,V15 | R |
| TK1-MOVE-23 | §11 | Successful reservations array includes unchanged items. | H HTTP ST | MOVE-18 | V14,V15 | R |
| TK1-MOVE-24 | §11 | moves length must be 1..8; other lengths give 422 validation_failed. | H VA | MOVE-03 | V14 | - |
| TK1-MOVE-25 | §11 | References must be distinct; duplicates give 422 validation_failed. | H VA | MOVE-03 | V14 | - |

## New Stage 2 atomic requirements

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
| TK2-PAIR-06 | Model | Combination capacity is the sum of member capacities. | H VA ST | TK1-FIX-12 | S | W09,W10 | S |
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
| TK2-SELECT-06 | API | New/current reservation responses always expose table_ids. | H HTTP ST | TK2-SELECT-01 | S | W10,W12,W13,W18 | S |
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
| TK2-OPTIONS-04 | Availability API | Each option contains table_ids and summed capacity. | H HTTP VA | TK2-PAIR-06,TK2-OPTIONS-03 | S | W11 | - |
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
| TK2-UP-01 | Existing clients | Stage 2 import accepts an unchanged export from the same team's Stage 1 service. | C ST TX | TK1-XFER-04,TK1-XFER-06 | S | W18 | S/R |
| TK2-UP-02 | Existing clients | Browser signed in before export/import remains signed in after upgrade. | C AU UI ST | TK1-XFER-13,TK2-AUI-09 | S/E | W18 | B |
| TK2-UP-03 | Existing clients | Retained booking reference works through /lookup after upgrade. | C UI ST AU | TK1-XFER-15,TK2-LOOKUP-01 | S/E | W18 | B |
| TK2-UP-04 | Existing clients | Booking whose response was lost before export remains retryable after import with the same body/key. | C RP UI ST | TK1-XFER-17,TK2-UNCERTAIN-04,TK2-UNCERTAIN-05 | S/E | W18 | R/B |
| TK2-UP-05 | Existing clients | UI recovers the original confirmation from that retry. | C RP UI ST | TK2-UP-04,TK2-UNCERTAIN-08 | S/E | W18 | R/B |
| TK2-UP-06 | Existing clients | Upgrade recovery requires no page reload. | C UI ST | TK2-UP-02,TK2-UP-05 | S/E | W18 | B |
| TK2-UP-07 | Existing clients | Upgrade recovery requires no new screen. | H UI ST | TK2-UP-05 | E | W18 | B |
| TK2-UP-08 | Existing clients | Selected form survives the between-request upgrade. | C UI ST | TK2-BOOK-01,TK2-UP-01 | E | W18 | B |
| TK2-UP-09 | Existing clients | Pending retry identity survives the between-request upgrade. | C UI RP ST | TK2-UP-04 | E | W18 | R/B |
| TK2-UP-10 | §10; Combined UI | Stage 2 own exports preserve pair configuration, pair records/member sets and successful create/batch receipts. | C ST RP TX | TK1-XFER-14,TK1-XFER-17,TK2-PAIR-07 | S | W19 | S/R |
| TK2-UP-11 | §10; Existing clients | Stage 1 legacy request and receipt formats continue to work after import. | C HTTP RP ST | TK2-UP-01,TK2-SELECT-02,TK1-IDEM-08 | S/E | W18 | S/R/B |
| TK2-CC-01 | Concurrent bookings/amendments | Concurrent requests yield results equivalent to some one-at-a-time order. | C CC TX | TK1-OCC-03,TK1-MOVE-17,TK2-PAIR-07 | S | W16,W19 | S/R |
| TK2-CC-02 | Concurrent bookings/amendments | All stated requirements hold at every read during concurrent writes. | C CC TX ST | TK2-CC-01 | S | W16,W19 | S/R |
| TK2-GATE-01 | Assignment | Stage 2 production starts only after Stage 1 ACCEPT plus committed copied baseline. | C SC ST | - | C | W20 | - |
| TK2-GATE-02 | Assignment | Stage 2 evidence commit waits for verifier's announced window completion. | H SC | - | C | W20 | - |

## Explicit and derived precedence map

1. Stage 1 §5/§7 precedence is unchanged: parse object/authenticate before receipt resolution; receipt conflict/replay precedes all new selection, combination, capacity, cutoff and resource validation. Header/body/user/path scope does not change because the form selects two tables.
2. Seating membership is unordered, but original JSON arrays remain ordered values. Reverse [a,b] to [b,a] with the same used key ->409 idempotency_key_reuse, even if both would be valid new requests. Object key order/whitespace still do not matter. Never canonicalize the body before receipt comparison. Unknown fields remain part of the receipt value while being ignored for mutation.
3. Both selectors present ->422 validation_failed; duplicates ->422 validation_failed; undeclared pair or >2 members ->422 combination_not_allowed; any member occupied ->409 table_unavailable; party above summed capacity ->422 party_exceeds_capacity. Wrong ordinary JSON field types remain400; invalid party types remain422. Missing/empty valid-type selection violates a required selection rule ->422; exact ties among multiple simultaneous selection faults are unspecified.
4. PATCH/moves validate explicit incoming selector fields before merging defaults. An existing single record legitimately carries both response fields; that stored shape must not make a request with one selector count as sending both. Omitted selection retains current members; an explicit legacy table_id replaces the whole selection with one member, not a merge with old table_ids.
5. Batch preserves Stage 1 ordering: non-occupancy errors in input order; current cutoff before proposed changes for that booking; final member conflicts only after all non-occupancy checks. Evaluate final member sets together against unlisted confirmed bookings. Unchanged listed members remain occupied. Duplicate references and duplicate member IDs are distinct validation obligations.
6. A confirmed rejection is an error, not uncertainty. A lost response is uncertainty, not a confirmed rejection or success, even if server committed. Unchanged retry retains exact user/method/path/key/body context; successful server replay clears uncertainty/error and supplies the original reference. Server remains authoritative.
7. Latest search intent B owns grid/labels/form; an older A response or a stale restaurant detail/selection callback cannot restore A. Conflict-triggered refresh must not erase the current selected form/inputs. A stale refresh cannot overwrite a newer search B; preserve form context only when it is still the selected intent.
8. Preserve historical original receipt JSON over the general new response-shape rule during Stage 1->2 migration (reasoned interpretation P1). Current record reads/new responses use table_ids; legacy replay need not be rewritten to look like a newly generated response.

## Critical and high risk handoff

CRITICAL inherited blockers remain nonoverlap, auth/privacy/password hashing, atomic state+receipt publication/rollback, correct idempotent scoping/precedence/historical replay, absolute duration/first DST occurrence, portable complete replacement and atomic batches. Stage 2 additionally blocks on any member double-booking; pair/single and overlapping-pair interactions; nontransitive approval; UI stale-result truthfulness; wrong searched-party availability; conflict form destruction; uncertain-success new-key duplicates or manufactured confirmations; and broken old browser/token/reference/receipt continuity.

HIGH obligations include all explicit field codes, selection shape compatibility, capacities, ordering and fixture normalization; all required screen routes/hooks and reliable signup/login/lookup; responsive 375px/desktop flows, labels/focus/contrast/distinct states; and offline assets. Product-quality evidence is required alongside test hooks. Qualitative design is evaluated through concrete rendered flows; a passing locator test alone cannot prove usability.

Recommended dependency order: accepted copied baseline -> selection/member model and backward-compatible snapshot importer -> member occupancy/selection validation/current response shapes -> option enumeration/order -> pair create/PATCH/batch/cancel/no-op and state transfer -> basic HTML/auth/search/lookup -> coherent asynchronous grid/detail/selection contexts -> frozen attempt body/key and conflict/uncertainty behavior -> combination UI -> retained old-client upgrade -> concurrency and product review -> exact-SHA independent verdict. State import/legacy receipt decisions must precede browser recovery assumptions. This is ordering of obligations, not prescribed architecture.

## Independent verification catalogue

All fixture values and labels in these procedures are synthetic. Expected intervals, pair eligibility, JSON values and DOM state transitions must be derived independently of production helpers. Record case IDs, exact production FULL SHA, status/code/JSON or rendered-state observations and sanitized evidence references. Never commit actual passwords, bearer tokens, opaque exports or browser session dumps. Keep snapshots private and ephemeral; public evidence can report equality outcomes and redacted structural counts.

### Inherited procedures applied cumulatively

V01..V20 retain the Stage 1 obligation set and now use Stage 2 shapes/member occupancy where appropriate. The following summaries keep the cumulative ledger self-contained; the initial Stage 1 ledger supplies original calibration detail but is not required to interpret the rows above.

| Procedure | Independent obligation and coverage expectation |
|---|---|
| V01 | Reproduce Dockerfile/RUN.md build and single-container launch with custom/default PORT, 2 CPU/2GiB, no runtime outbound access; healthy/API-ready <=60s. Confirm scoped delivery/provenance and bundled browser assets. Host package imports are not acceptance. |
| V02 | Reset A->B repeatedly removes old accounts/tokens/records/config/receipts, with coherent visibility after204. Seed config order, all ID boundaries, given short passwords, single/pair confirmed/cancelled records; login and occupancy reflect fixture. Reject wrong-type/value inputs using §5 without partial state. |
| V03 | Endpoint matrix of missing/null/wrong-type/correct-type invalid fields, dates, party values, query plain digits, bare local times, IDs/keys and ignored fields. Include unknown valid JSON numeric exponent1e309 and calendar years0001/9999 without assuming binary-float parser limits. Verify all error envelopes/statuses/codes and no5xx. Pair selectors obey specific codes; distinguish historical response from new shape. |
| V04 | Signup/login errors and successful responses; signup8-character boundary versus unrestricted seeded password login; concurrent duplicate signup; all old session tokens coexist and survive import. Independent storage/source inspection proves password hashing for every account; HTTP behavior alone does not prove it. |
| V05 | Enumerate public/protected APIs and new HTML routes. Cross-owner list/reference GET/cancel/PATCH/moves cannot leak or mutate another record; foreign/unknown refs404. Export/import/reset deliberately remain unauthenticated. Browser signed-out cell selection cannot book. |
| V06 | Both required-key paths:0/1/255/256-length keys, replay with reordered object keys/whitespace, different body including ignored fields, different user/path, failed4xx retry. Changed invalid body conflicts before field/resource rules. Arrays retain order and booleans differ from numbers; reversing a valid pair is a changed JSON body under the same key. |
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

### Stage 2 independent procedures

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
| W20 | Verify Stage 1 exact-SHA ACCEPT precedes committed copied Stage 2 production baseline; no premature backend/browser production acceptance. Verify ledger commit occurs only after verifier releases its window and changes only this owned file. Stage 2 release needs independent exact candidate SHA verdict addressing all inherited/new obligations, not just test hooks or official pass count. |

## Upgrade compatibility matrix

| Source -> destination | Obligations that must remain true | Independent evidence |
|---|---|---|
| Accepted team's Stage 1 format1 -> fresh Stage 2 | Accounts/hashes/alltokens/config/single records/IDs/refs/statuses/timestamps; original create/batch body+response receipts and failed reusable keys; existing single requests accepted. | V18,W18 |
| Stage 1 format1 -> populated Stage 2 | Same continuity; remove destination users/tokens/pairs/bookings/receipts rather than merge. Legacy config has no pairs unless present in valid source. | V18,W18 |
| Retained signed-in browser -> Stage 2 import between browser requests | Same session/displayname/form/pending key+body and reference; no reload/newscreen; original lost-response confirmation recovered from server. | W18 |
| Stage 2 format1 A -> fresh/populated Stage 2 B | All baseline state plus pair definitions/member ordering/occupancy/statuses and successful pair/batch receipts. | W19 |
| Same Stage 1/2 snapshot -> destination repeatedly after mutations | Restore exact source state without duplicate records/occupancy or spent failed keys; identities/timestamps stable. | V18,W19 |
| Stage 1 -> Stage 2 B -> export B -> Stage 2 C | Continued legacy credential/reference/historical-receipt truth alongside new pair data/receipts. | W18,W19 |
| Invalid Stage 1/2 import -> populated Stage 2 | No state, credential, receipt or occupancy change. | V19,W19 |
| Imported Stage 2 -> reset fresh Stage 1-shaped or Stage 2-shaped fixture | Old/imported tokens/records/receipts removed; only new fixture single/pair/status policy remains. | V02,W09,W19 |

No Stage 2->Stage 1 downgrade path is specified. Migration during an in-flight browser request is explicitly not required; nevertheless ordinary backend concurrency and atomic control-call behavior continue to apply. No recovery across browser page reload or cross-tab synchronization is required. Formats remain opaque; consumers must not recreate identities or reinterpret raw state externally.

## State and browser acceptance invariants

For every visible confirmed record, expand its one/two members and independently audit half-open intervals by (restaurant_id,table-ID). Two records overlap iff they share a member and their absolute intervals intersect. Capacity is summed for the selected approved pair. Approval is exact unordered declared-pair membership, not transitive reachability and not total capacity alone. Pair commit, amendment, cancellation, batch, snapshot and import must publish complete member/record/receipt state together. No rejected operation leaves a partial member or spent retry key.

Keep three concepts distinct: semantic unordered seating set; ordered declaration/option/UI representation; exact original parsed JSON receipt value. Normalize semantic membership and current output deliberately without normalizing away JSON-array identity or rewriting successful original response snapshots. No-op batches preserve all existing values, even when representations might otherwise be reordered.

Browser state must associate results and labels with completed search intent, selection with its restaurant/slot/member context, and each submitted attempt with authenticated caller/method/path/key/body. An unchanged attempt has one retry identity across success, loss and upgrade. A changed field creates a new request. UI errors, uncertainty and confirmation describe the corresponding server outcome, not whichever callback finished last. A conflict refresh updates available choices without deleting the selected editable form. Controls typed after search do not retroactively change the party/date under which displayed availability was calculated.

## Ambiguities and reasoned interpretations

These findings identify interpretation boundaries. They are not unsupported new contract requirements and should be resolved with the Conductor, never the human operator during the autonomous run.

The Conductor adopted P1 and P2's historical-receipt/request-identity rules in room message `39757f09-cf2b-4898-b5ab-27c8f22541b0`: historical receipts retain their exact original JSON; new/current representations use table_ids; browser recovery accepts legacy table_id and resolves human labels; full parsed body comparison precedes table-set normalization, so reversed arrays are different bodies. These points are settled for this run. Response member-order recommendations beyond explicit option/UI declaration order remain interpretations.

**P1 Historical receipt shape versus table_ids.** Stage 2 says responses always carry table_ids; unchanged Stage 1 receipts do not have it, while §§7/10 and upgrade continuity require original JSON response preservation. Interpret the more specific original-receipt obligation as an exception for historical replays. Preserve imported original body/response exactly; normalize current records/new responses into Stage 2 shape and let browser recognize legacy table_id on recovered server replay. Adding a field to stored historical response changes the promised JSON value. No shape exception is needed for new Stage 2 receipts.

**P2 Pair normalization/order.** Membership is unordered and reversed declared pair is allowed. Availability options/member order and combo cell IDs explicitly use declaration order. Create/PATCH/move response member order is not separately specified. Recommend stable declaration order for new pair records and preserve stored order on semantic no-op; do not assert lexicographic sorting or original request order as normative. JSON request arrays remain ordered for idempotency, regardless of seating equivalence.

**P3 Missing legacy combinable and selector replacement.** Cumulative old fixture/export support implies no pair declarations when old config omits combinable. Legacy table_id means one member. Validate both-selector conflict on incoming fields, then replace selection if supplied; defaulting from an existing single response with both fields must not manufacture a conflict. Empty table_ids has no members and cannot be a valid selection, so422validation_failed is the natural §5 rule. Exact precedence for multiple selector faults/unknown members/>2/duplicate IDs is not fully specified; use isolated-error assertions plus explicit replay/batch priority cases.

**P4 Fixture pair validity.** Pair entries must reference two restaurant members. Handling duplicate declarations/reversed duplicate declarations, repeated same member within a declared pair, invalid fixture-pair substructure and their exact error precedence is not specified beyond §5/model. Recommend validating distinct membership and preserving declared order. Do not create transitive pairs, repair invalid declarations silently or demand unprovided deduplication policy as a release gate.

**P5 Combination cell absence.** Every available eligible pair must have a cell. The specification does not require an unavailable pair cell. Extra unavailable cells are permitted if their availability/click behavior is truthful. Singles always have cells for every table/slot, even when unavailable; no-slots means no times, not merely no eligible seating options.

**P6 Lost response classification and edits.** Network failure cannot establish commit/rejection; show booking-uncertain and retain exact pending identity. A delivered rejection uses booking-error. Changed fields after loss create a new request under the stated form rule; the first attempt may still have committed and must not be erased or manufactured as a confirmation. No lookup heuristic/local optimistic record can replace server replay. Exact UI treatment of an older known confirmation while a new attempt fails is not specified, but it must not be presented as success for the failed/lost attempt.

The distinction between an edit later reverted to its original value and an entirely untouched form is not fully specified. Recommend treating an actual field edit as a new-attempt boundary on next submission, while preserving the prior receipt; do not demand an undisclosed history-tracking mechanism as an extra acceptance condition.

**P7 Latest intent and form preservation.** A new search B can invalidate a form originating from A; clear/rebind stale context so no visible form misdescribes B. This does not require automatic table selection. Conflict refresh preserves the actively selected form/inputs and does not replace a newer search context. Any request cancellation or generation-token mechanism is an implementation choice, not a contract demand. Lookup/detail races are tested to prevent stale data being represented as the requested reference; no background polling is required.

**P8 Pre-upgrade browser setup.** Stage 1 defines no browser, yet Stage 2 requires a retained signed-in browser across Stage 1 export/import. Verify the same team's old API data/session with a retained Stage 2-capable client and stable origin/test routing, without inventing a Stage 1 HTML obligation. The token included in source export must be the actual token retained by that browser; minting a destination-only token after the snapshot and expecting it to survive replacement is an invalid test setup. Import must occur between browser requests as expressly scoped.

**P9 Product thresholds and optional work.** Sufficient contrast, warm coherent presentation and usable hierarchy are normative; no exact artwork, fonts, pixel match, brand asset or numerical contrast threshold is specified. Computed contrast and keyboard/screenshot inspection provide evidence, not invented visual requirements. Signup/login persistence across required screens and upgrade is required, while reload recovery, cross-tab storage synchronization/liveupdates/polling and batch UI are not required. Optional features cannot undermine required state/retry rules.

**P10 Inherited boundaries.** Stage 1 error ties, gap-valued business-hour boundaries, equal-start tie-breaks, duplicate JSON keys and Unicode character-count details remain unspecified. Keep explicit first-occurrence/absolute-time/offset obligations; do not confuse hypothetical DST boundary advice with reproduced numeric/calendar counterexamples. Signup password minimum does not reject given short seeded passwords. Table IDs are restaurant-scoped; equal strings across restaurants must not share occupancy.

## Formal acceptance and evidence safety

This ledger is complete for handoff when all 187 inherited IDs and new normative records are traced, dependencies/procedures/owners/compatibility and interpretation boundaries are auditable, and the sanitized file is committed after the required verifier window. That is not production acceptance. Stage 2 production remains gated on Stage 1 formal ACCEPT plus committed copied baseline.

Acceptance requires the independent verifier's formal verdict on the exact Stage 2 production FULL SHA, with official HTTP/browser checks and contract-derived evidence covering every CRITICAL/HIGH and remaining normative obligation. Required stories include desktop/375px render and keyboard/focus/labels/contrast review, deterministic out-of-order responses, conflict input preservation, lost-after-commit exact replay, every-member concurrency/rollback, and actual Stage 1->2 session/reference/receipt continuity in separate processes. Source/owner checks are supporting evidence; any missing independent case is an explicit coverage gap. Production changes after verification require appropriate revalidation of a new exact SHA.

Only evidence/stage-2/requirements.md is owned by this assignment. Do not alter kickoff, official specs, harness/shipped checks, production or other evidence. Never commit credentials, passwords, tokens, session dumps, opaque state exports or raw environments. Do not copy Stage 1 opaque exports into repository evidence; use ephemeral private transfers and sanitized result comparisons. Keep this one cumulative ledger authoritative and update it deliberately; after formal acceptance, stop cosmetic reconciliation.
