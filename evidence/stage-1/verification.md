# Stage 1 independent verification

VERDICT: ACCEPT

REVISION: `d41a7627711951a07ce7a1718fac47c6ea5b6dd4`

This verdict applies only to the exact Stage 1 production tree in this committed revision, released by Conductor in room message `f970bfcc-47d2-4470-9be2-b3fd3dc8290c`. The official isolated harness passes 120/120 checks. All 30 distinct independent cases have passing evidence, including the two previously rejected counterexamples. No reproducible blocking product defect remains.

SPECIFICATION COVERAGE: All 187 canonical obligations are closed in the traceability table below: 66 CRITICAL, 109 HIGH and 12 other. Closure combines independent HTTP observations, supplied checks and the explicitly identified source inspections where black-box evidence cannot establish an internal property. Generic 403 behavior has no applicable Stage 1 permission route; specified foreign-reservation responses are independently verified as 404. Source provenance is assessed through repository/source/dependency inspection, rather than claimed as a mathematical proof of authorship.

OFFICIAL CHECKS: 120 collected, 120 passed; zero failed, errors, skipped, deselected or xfailed. Mode isolated, state completed, Stage 1 pass. The report's generic working-tree provenance refers to the clean read-only native clone of the assigned commit, with exact revision verified before and after execution; it does not refer to shared mutable HEAD.

INDEPENDENT ROBUSTNESS CHECKS: 30 distinct cases PASS, six controlled oracle variants detected, coordinated barriers up to 50 workers, response and final-state audits. Across closure, main, repaired verifier checkpoints, supplementary boundary checks and the mapped-port probe, 1,044 observed HTTP requests were issued. This count excludes official harness traffic and readiness polling; it includes legacy-source calls and setup requests in the recovered verifier case.

COMPATIBILITY CHECKS: Current exports transfer unchanged across separately started source, destination and third processes with distinct ports and no shared state volume. Source is Docker-paused and its unavailable state inspected before destination import. Two existing sessions, hashed-password login, configuration, exact reservation values, cancelled states, historical create/batch responses and retry semantics survive. Import removes destination credentials/records/receipts; repeated import restores a snapshot; invalid import preserves state/login/receipts; reset clears imported state and receipts. A separately built, paused old revision also supplies a legacy direct-object export accepted by the new revision. These additional legacy tests do not transfer acceptance from the rejected revision.

CLEAN-ENVIRONMENT CHECKS: Native detached clone `/home/nurali/av-stage1-d41a7627-review-847ab33d`, no linked worktree, no hardlinks, tracked source read-only, clean exact SHA before/after. Docker 29.8.0; host verifier Python 3.14.4; submitted image Python 3.13 with bundled Debian tzdata. The authoritative readonly harness checkout is `/mnt/d/dark/dark-factory-wearedevs` at `803560d2a678ace1414465c098eb0ab5380ffade`; its tracked differences were EOL-only and no check was edited. Unique owned Docker resources were cleaned. Final owned container/network listings are empty.

KNOWN LIMITATIONS: Verification uses bounded datasets and the specified maximum concurrent in-flight request count; unbounded dataset performance is not established. Hidden checks are unavailable. Gap-valued opening/closing boundaries are unspecified by the contract and are not invented blockers. Exact cutoff equality is inspected in source with wide and live before/after HTTP boundaries; there is no controllable server clock. Ephemeral state and absence of restart persistence comply with the contract. Provenance inspection cannot establish the historical origin of every character of an implementation.

EVIDENCE ARTIFACTS: `campaign.py` is the executable independent HTTP campaign/oracle; `run_campaign.py` orchestrates immutable-SHA builds, isolated official checks, runtime constraints and checkpoint recovery; `runtime_probe.py` verifies actual Docker-assigned published mapping; this report is the consolidated verdict and coverage surface. Only these four owned verifier files belong to the evidence commit. Raw exports, credentials, bearer values and environments were not written or committed. The evidence commit is reported separately from the tested production SHA.

## Requirement authority and prior defects

The single canonical ledger is `evidence/stage-1/requirements.md` at evidence-only commit `d2f8b20705cc12cb0f0995f04bdc80f9dcb29a57`: 187 records, V01..V20, precedence and compatibility matrix. Later auditor finding annotations do not change those stable requirement IDs. The verifier does not modify the auditor's ledger.

The prior exact revision `b03ce55647b70a46f478ea50ba077e02945bcefe` was formally REJECTED in sanitized evidence commit `f476314d258a8e1955a58c9182d9ab9c009a62df`. Its two HIGH product defects remain audit history; this replacement is independently tested.

| Defect | Prior expected / observed | Replacement evidence and outcome |
|---|---|---|
| TK1-VERIFY-001 | Valid fixture plus ignored literal numeric `1e309`: expected reset 204; prior observed 400 malformed_request. TK1-HTTP-03 / TK1-ERR-02. | `ignored_numeric_receipt_boundaries` PASS in closure and main runs. Large ignored values parse, semantically equivalent encodings replay, changed numbers conflict, original receipts survive cancellation and import without new effects. |
| TK1-VERIFY-002 | UTC all-week 18:00..23:00, slot 1440, duration 90, date 9999-12-31: expected availability 200 / one 18:00 slot; prior observed 422 validation_failed. TK1-AV-04 / TK1-TIME-01. | `calendar_extremes` PASS for years 0001, ordinary and 9999. `terminal_zone_instants` additionally passes local dates whose UTC instants cross year 0 or 10000, with exact independent integer-instant overlap/receipt/import audit. |

## Official and independent evidence checkpoints

All diagnostics below are outside the result repository under `D:/dark/band-work/checks` (WSL `/mnt/d/dark/band-work/checks`). Diagnostic summaries contain sanitized outcomes/counts; opaque state/session values remain only in test memory. The campaign reports any assertion failure explicitly rather than writing response bodies containing private values.

| Checkpoint | Run directory | Observed outcome |
|---|---|---|
| Prior counterexample closure | `av-stage1-d41a76277119-21a9300c` | 2 cases PASS; 19 requests. |
| Official isolated | `av-stage1-d41a76277119-d3d96380/official` | 120/120 PASS; complete exact-SHA report. |
| Main independent | `av-stage1-d41a76277119-27d82820` | 27 PASS; one verifier OverflowError in expected terminal-date grid construction; 963 requests. Valid completed cases retained. |
| Corrected terminal case | `av-stage1-d41a76277119-08282f26` | 1 PASS; 20 requests; only affected case repeated. |
| Reset/import receipt erasure | `av-stage1-d41a76277119-25c76c65` | 1 PASS; 19 requests; same fixture user IDs expose leftover receipts. |
| DST resolved closing boundaries | `av-stage1-d41a76277119-bd0a160c` | 1 PASS; 20 requests; four transitions and resolved closing instants. |
| Standalone published port | `av-published-d41a76277119-505de904` | Health 200, empty reset 204, public restaurants 200; 3 requests. |

Official report: `av-stage1-d41a76277119-d3d96380/official/report.json`; suite digest `c4272f6e544cb878ece8469c1eab3b477216701f92f0a5d1111e5e591e67bd09`. UTC start 2026-10-05T15:40:55.424666+00:00, finish 15:41:38.187850+00:00 (42.763 seconds including harness work). File counts: health/reset/auth 12, reservations 37, restaurant/availability 18, retries/time/input 20, sample 20, seeded state 13. The expected unsuccessful Stage 2 overshoot probe is outside the released Stage 1 contract and is not a Stage 1 defect.

The main summary deliberately retains its original `all_passed: false` and verifier error. The consolidated verdict is based on its 27 valid passing cases plus the independently successful replacement terminal checkpoint and two additional coverage closures; it does not rewrite or conceal original diagnostics.

## Runtime and budget observations

Every independent service runs with enforced 2 vCPU and 2 GiB Docker limits. Main campaign uses a unique internal Docker network (`Internal=true`) without outbound runtime access. Service ports are 8765/8766, third 8080 with PORT omitted, and legacy source 8899. No shared database/files/volume or source address is required for state transfer. Build-time access only supplies image/tzdata dependencies; all service runtime dependencies are packaged.

Maximum observed ordinary request duration across independent checks is 0.0766821 seconds; maximum control call is 0.0875098 seconds. These are below the actual 5/10-second contract budgets. Main current-revision readiness is 1.586/1.799/1.982 seconds; old legacy source 2.220 seconds. Other current services are ready within 1.328 seconds; the separate published-port service is ready in 0.736 seconds. All are within the actual 60-second readiness allowance. The live cutoff case's 68.377-second overall case duration includes intentional clock-boundary waiting; each HTTP request still uses its own contract timeout.

The independent publication probe runs the submitted image alone with custom PORT 8987 and Docker-assigned host mapping 127.0.0.1:52466, queried from Docker rather than assumed. HostConfig confirms NanoCpus 2000000000 and memory 2147483648. Its native Windows HTTP client reaches the container over the actual mapping. This publication phase uses a bridge network; outbound isolation is established separately by the main internal-network campaign. RUN.md's single-image build/start command and default/custom binding are also inspected.

## Independent models, stress and ordering

The independent oracle imports no production module and uses no production decision logic. It enumerates local minute grids from the supplied opening anchor, resolves IANA starts by first occurrence with a round-trip gap check, converts to independent absolute instants, fits absolute duration against resolved close, and compares half-open intervals. It retains fixture table order and scopes identity by restaurant plus table. An integer ordinal/offset model checks terminal local dates without requiring a Python datetime for UTC year 0 or 10000. Decimal-based independent JSON encoding/comparison avoids binary64 numeric loss.

Six controlled decisions are detected by calibration: closed rather than half-open intervals, second rather than first fold, wall rather than absolute duration, contamination across equal table IDs in different restaurants, binary64 number equality collapse, and wall-clock rather than resolved-instant closing fit. Calibration affects disposable verifier decisions only, never production.

Availability is compared against independently computed slots for several grid/duration pairs, capacities, parties 1..7, nonsorted table IDs, confirmed occupancy, cancellation and closed days. Four specified Berlin/New York transitions test gap rejection/omission, single first-fold slot, start/end offsets, absolute duration, PATCH/batch behavior and closing fit. Party/type/local-format/key/ID/shape boundaries and error precedence are checked separately to avoid ambiguous error ties.

Numeric metamorphic vectors include `1e309` versus `10e308` versus changed `1e310`; tiny `1e-1000` versus equivalent `10e-1001` versus zero; precision beyond binary64; adjacent integers beyond 2^53; booleans versus numbers; ordered arrays; reordered object keys and whitespace. Valid enormous capacity/party/grid values and excessive duration exercise bounded operation without exponent expansion. NaN/Infinity remain malformed JSON. Successful receipt bodies stay original after later amendments/cancellation/import; failed keys remain reusable.

Barrier-coordinated 50-way identical requests yield exactly one 201 and 49 identical 200 receipts with one effect. Fifty distinct competing writes and changed-body same-key requests yield one legal effect and specified conflicts. Fifty overlapping batch/read operations expose only whole states; additional overlapping signup, reset/import, amendments/cancellation/replay and export-versus-swap scenarios audit responses plus final records/occupancy. Every reservation-list observation checks unique IDs/references, half-open confirmed occupancy per restaurant/table and absolute-time descending order.

Moves independently cover final-state swaps, unchanged-item occupancy, unlisted conflicts, complete rollback, 1/8/9-length bounds, duplicate references, mixed restaurants, ownership, input-order non-occupancy precedence, current cutoff before proposed changes, no-op field preservation and input-order responses. Historical create and batch receipts are tested after mutation and transfer, rather than only against their immediate successful state.

## Source inspection evidence

| Reference | Independently inspected property |
|---|---|
| SR-1 | Exact production Dockerfile, RUN.md and new Stage 1 Git tree: HTTP-only service, standalone image, four standard-library production modules, bundled tzdata, no runtime external asset/service dependency. |
| SR-2 | Repository and dependency/source inspection found no reused domain-product implementation, API schema or documentation; submission is Stage 1 only. This is provenance inspection within the available repository, with the limitation stated above. |
| SR-3 | Account creation stores random 16-byte salt and scrypt hash (n=16384, r=8, p=1), constant-time digest comparison; no plaintext password field retained. Token map allows multiple sessions without expiry logic. Hash/token snapshot continuity is exercised over HTTP. |
| SR-4 | Cutoff compares exact elapsed minutes to the restaurant cutoff with <=, including equality and past starts; current reservation start is checked before proposed changes. Cancelled state returns before cutoff evaluation for repeated cancellation. HTTP wide and live clock boundaries confirm the observable behavior. |
| SR-5 | A single state RLock encloses authentication, validation, occupancy, mutation, receipts and snapshot/control operations. Candidate/replacement state validates before publication; export copies/serializes under that boundary. HTTP coordinated races independently check serial outcomes and snapshot records/receipts. |

## Recovery and classification

No product change was requested for verifier or infrastructure failures. After the complete official pass, a Docker Desktop credential-helper error during a public-base-image rebuild was classified INFRASTRUCTURE DEFECT. The pinned revision and official checkpoint were preserved; clean bounded build recovery resumed the independent campaign. The checkpoint validator requires the exact revision, isolated completed pass and unchanged official suite digest.

A terminal-date expected-grid increment raised OverflowError inside the verifier, classified VERIFIER DEFECT. Its expected slots were corrected to bounded minute-integer enumeration; only that affected case reran and passed. An early boundary-only wrapper exit incorrectly required a skipped official result despite all targeted assertions passing; classified VERIFIER DEFECT and corrected. During preparation the oracle's restaurant discriminator coverage gap was fixed and calibrated before relevant product execution. None of these is represented as a production failure or as silently passing evidence.

## Executable identity and reproduction

Run from Linux with the supplied verifier venv active and official checkout present. Existing native clones must be clean and detached at the stated full revisions. The runner can also make its own independent native clone using `--repo`. A complete run without checkpoint arguments executes the official harness and all applicable independent cases; provide the legacy clone to include that extra compatibility case.

```sh
source ~/.venvs/dark-factory/bin/activate
python /mnt/d/dark/band-work/result/evidence/stage-1/run_campaign.py \
  --released --revision d41a7627711951a07ce7a1718fac47c6ea5b6dd4 \
  --materialized /home/nurali/av-stage1-d41a7627-review-847ab33d \
  --legacy-materialized /home/nurali/av-stage1-b03ce556-review-8810cfb1
```

| Executable checkpoint | campaign.py SHA-256 | run_campaign.py SHA-256 |
|---|---|---|
| Main 27 valid cases | 15ce961f435bf36efc742ac13d40e31d4f6bf7ecec31c49f953f6eef3f924b50 | e1acd97853ca55a3aa3f87fb5c6238e38d45c3a4884c9fab841e9a8d3edd1904 |
| Terminal recovery | 16b339ab790e21feaa11fc3c42f9dab9aa03979deabcd502e393f6400f6340ca | b358210b4db8d13213d62bbed0e4d7193d92cf66df39487f53d2a2fa5ce0c95c |
| Control erasure closure | 5eec56a6f674a0f620821c7c8dc4248e0d25eba1167719fec26e15deab22d913 | b358210b4db8d13213d62bbed0e4d7193d92cf66df39487f53d2a2fa5ce0c95c |
| Final DST closing closure / shipped verifier | 4fe9e7c5670f89132d36164332c24bf8abe12983c997923efec88a0345707176 | b358210b4db8d13213d62bbed0e4d7193d92cf66df39487f53d2a2fa5ce0c95c |

Mapped-port executable `runtime_probe.py` SHA-256: `5baf2be13a9ac441e150723383a4ba772656d6dc9a6334de00018f9281cdf7dc`. Main and affected earlier executed verifier copies are retained in their external checkpoint directories. Final campaign changes correct the terminal oracle and add receipt-erasure/DST-closing closures, leaving previously passing case bodies unchanged; the orchestrator adds explicit case selection for checkpoint recovery. Official results were preserved rather than needlessly repeated. Production remained the same exact clean commit throughout.

## Independent case outcomes

Checkpoint abbreviations: MAIN=`av-stage1-d41a76277119-27d82820`, TERM=`av-stage1-d41a76277119-08282f26`, ERASE=`av-stage1-d41a76277119-25c76c65`, DST=`av-stage1-d41a76277119-bd0a160c`.

| Case | Result | Checkpoint | Case duration seconds |
|---|---|---|---|
| `amendments_atomic_cutoff` | PASS | MAIN | 0.192 |
| `availability_oracle` | PASS | MAIN | 0.407 |
| `booking_boundaries_privacy` | PASS | MAIN | 0.131 |
| `calendar_extremes` | PASS | MAIN | 0.094 |
| `cancelled_after_cutoff_temporal` | PASS | MAIN | 68.377 |
| `concurrency_batch_snapshot` | PASS | MAIN | 0.135 |
| `concurrency_changed_key_50` | PASS | MAIN | 0.135 |
| `concurrency_distinct_50` | PASS | MAIN | 0.140 |
| `concurrency_identical_50` | PASS | MAIN | 0.129 |
| `concurrency_signup_and_users` | PASS | MAIN | 0.210 |
| `control_receipt_erasure` | PASS | ERASE | 0.345 |
| `control_replacement_races` | PASS | MAIN | 0.285 |
| `dst_closing_instant_boundaries` | PASS | DST | 0.417 |
| `dst_oracle` | PASS | MAIN | 0.191 |
| `duplicate_table_ids_and_short_seed_password` | PASS | MAIN | 0.168 |
| `export_atomic_batch` | PASS | MAIN | 0.187 |
| `ignored_numeric_receipt_boundaries` | PASS | MAIN | 0.237 |
| `legacy_direct_snapshot_continuity` | PASS | MAIN | 0.504 |
| `moves_atomic_precedence` | PASS | MAIN | 0.153 |
| `moves_eight_and_restaurant_scope` | PASS | MAIN | 0.099 |
| `numeric_equivalence_and_precision` | PASS | MAIN | 0.761 |
| `offset_ordering_and_amendment` | PASS | MAIN | 0.100 |
| `patch_and_batch_field_validation` | PASS | MAIN | 0.220 |
| `patch_batch_cancel_replay_races` | PASS | MAIN | 0.116 |
| `public_auth_reset` | PASS | MAIN | 0.296 |
| `receipt_semantics` | PASS | MAIN | 0.137 |
| `seed_ids_and_batch_cutoff` | PASS | MAIN | 0.101 |
| `snapshot_import_receipts` | PASS | MAIN | 0.911 |
| `terminal_zone_instants` | PASS | TERM | 0.249 |
| `validation` | PASS | MAIN | 0.120 |

## Canonical procedure bindings

These bindings resolve the per-row procedure references to the exact-SHA case table, runtime evidence and source inspections above. They supplement the official checks; they do not imply that the official harness covers every ledger row.

| Procedure | Independent evidence |
|---|---|
| <a id="v01"></a>V01 | Pinned Docker build, offline/default/custom-port runtime; published-port probe; SR-1/SR-2; evidence secret scan |
| <a id="v02"></a>V02 | public_auth_reset; seed_ids_and_batch_cutoff; control_receipt_erasure; control_replacement_races |
| <a id="v03"></a>V03 | validation; patch_and_batch_field_validation; ignored_numeric_receipt_boundaries; numeric_equivalence_and_precision; response audit |
| <a id="v04"></a>V04 | public_auth_reset; concurrency_signup_and_users; duplicate_table_ids_and_short_seed_password; snapshot_import_receipts; SR-3 |
| <a id="v05"></a>V05 | public_auth_reset; booking_boundaries_privacy; moves_atomic_precedence; protected-route token matrix |
| <a id="v06"></a>V06 | receipt_semantics; numeric_equivalence_and_precision; concurrency_identical_50; concurrency_changed_key_50; control_receipt_erasure |
| <a id="v07"></a>V07 | public_auth_reset; duplicate_table_ids_and_short_seed_password; moves_eight_and_restaurant_scope |
| <a id="v08"></a>V08 | availability_oracle; calendar_extremes; numeric_equivalence_and_precision; duplicate_table_ids_and_short_seed_password |
| <a id="v09"></a>V09 | dst_oracle; dst_closing_instant_boundaries; terminal_zone_instants; patch_and_batch_field_validation |
| <a id="v10"></a>V10 | booking_boundaries_privacy; seed_ids_and_batch_cutoff; availability_oracle; calendar_extremes; numeric_equivalence_and_precision |
| <a id="v11"></a>V11 | offset_ordering_and_amendment; seed_ids_and_batch_cutoff; every reservation-list audit |
| <a id="v12"></a>V12 | amendments_atomic_cutoff; cancelled_after_cutoff_temporal; seed_ids_and_batch_cutoff; SR-4 |
| <a id="v13"></a>V13 | amendments_atomic_cutoff; patch_and_batch_field_validation; patch_batch_cancel_replay_races; SR-4 |
| <a id="v14"></a>V14 | moves_atomic_precedence; moves_eight_and_restaurant_scope; seed_ids_and_batch_cutoff; patch_and_batch_field_validation; concurrency_batch_snapshot |
| <a id="v15"></a>V15 | receipt_semantics; moves_atomic_precedence; numeric_equivalence_and_precision; snapshot_import_receipts; legacy_direct_snapshot_continuity |
| <a id="v16"></a>V16 | concurrency_identical_50; concurrency_distinct_50; concurrency_changed_key_50; concurrency_batch_snapshot; concurrency_signup_and_users; final-state audit |
| <a id="v17"></a>V17 | export_atomic_batch; snapshot_import_receipts; control_replacement_races; SR-5 |
| <a id="v18"></a>V18 | snapshot_import_receipts; legacy_direct_snapshot_continuity; ignored_numeric_receipt_boundaries; duplicate_table_ids_and_short_seed_password; control_receipt_erasure |
| <a id="v19"></a>V19 | snapshot_import_receipts; invalid-import state/login/receipt rollback assertions; repeated import |
| <a id="v20"></a>V20 | control_replacement_races; export_atomic_batch; patch_batch_cancel_replay_races; control_receipt_erasure; SR-5 |

## Atomic obligation closure

All rows below refer to the supplied canonical requirement text at the ledger commit identified above; the ledger remains the sole requirement authority. Each row is closed for this revision by its linked independent procedure evidence and applicable official/source evidence. CLOSED means verified to the stated evidence limits, not exhaustive proof over unbounded inputs.

| Requirement ID | Risk | Result | Evidence bindings |
|---|---|---|---|
| TK1-SC-01 | M | CLOSED | [V01](#v01) |
| TK1-SC-02 | H | CLOSED: source/provenance inspection SR-2 | [V01](#v01) |
| TK1-SC-03 | H | CLOSED: source/provenance inspection SR-2 | [V01](#v01) |
| TK1-SC-04 | H | CLOSED | [V01](#v01) |
| TK1-RUN-01 | H | CLOSED | [V01](#v01) |
| TK1-RUN-02 | M | CLOSED | [V01](#v01) |
| TK1-RUN-03 | H | CLOSED | [V01](#v01) |
| TK1-RUN-04 | H | CLOSED | [V01](#v01) |
| TK1-RUN-05 | H | CLOSED | [V01](#v01) |
| TK1-RUN-06 | H | CLOSED | [V01](#v01), [V16](#v16) |
| TK1-RUN-07 | H | CLOSED | [V16](#v16) |
| TK1-RUN-08 | H | CLOSED | [V02](#v02), [V18](#v18) |
| TK1-RUN-09 | H | CLOSED | [V01](#v01) |
| TK1-RUN-10 | M | CLOSED | [V01](#v01) |
| TK1-RUN-11 | H | CLOSED | [V01](#v01) |
| TK1-RUN-12 | H | CLOSED | [V01](#v01) |
| TK1-RUN-13 | H | CLOSED | [V01](#v01), [V16](#v16) |
| TK1-HTTP-01 | M | CLOSED | [V03](#v03) |
| TK1-HTTP-02 | H | CLOSED | [V03](#v03), [V09](#v09) |
| TK1-HTTP-03 | H | CLOSED | [V03](#v03), [V06](#v06) |
| TK1-HTTP-04 | M | CLOSED | [V03](#v03) |
| TK1-HTTP-05 | H | CLOSED | [V03](#v03), [V02](#v02) |
| TK1-FIX-01 | H | CLOSED | [V02](#v02) |
| TK1-FIX-02 | C | CLOSED | [V02](#v02), [V20](#v20) |
| TK1-FIX-03 | M | CLOSED | [V02](#v02) |
| TK1-FIX-04 | C | CLOSED | [V02](#v02), [V20](#v20) |
| TK1-FIX-05 | H | CLOSED | [V02](#v02) |
| TK1-FIX-06 | M | CLOSED | [V02](#v02) |
| TK1-FIX-07 | H | CLOSED | [V02](#v02), [V09](#v09) |
| TK1-FIX-08 | H | CLOSED | [V08](#v08) |
| TK1-FIX-09 | H | CLOSED | [V08](#v08), [V10](#v10) |
| TK1-FIX-10 | H | CLOSED | [V08](#v08), [V10](#v10) |
| TK1-FIX-11 | H | CLOSED | [V12](#v12), [V13](#v13) |
| TK1-FIX-12 | H | CLOSED | [V08](#v08), [V10](#v10) |
| TK1-FIX-13 | H | CLOSED | [V02](#v02), [V04](#v04) |
| TK1-FIX-14 | H | CLOSED | [V02](#v02), [V11](#v11) |
| TK1-FIX-15 | C | CLOSED | [V02](#v02), [V08](#v08) |
| TK1-FIX-16 | H | CLOSED | [V10](#v10) |
| TK1-FIX-17 | H | CLOSED | [V12](#v12), [V13](#v13) |
| TK1-ERR-01 | H | CLOSED | [V03](#v03) |
| TK1-ERR-02 | H | CLOSED | [V03](#v03) |
| TK1-ERR-03 | H | CLOSED | [V03](#v03), [V14](#v14) |
| TK1-ERR-04 | H | CLOSED | [V03](#v03) |
| TK1-ERR-05 | H | CLOSED | [V03](#v03) |
| TK1-ERR-06 | H | CLOSED | [V03](#v03), [V10](#v10), [V13](#v13), [V14](#v14) |
| TK1-ERR-07 | H | CLOSED | [V03](#v03), [V09](#v09) |
| TK1-ERR-08 | H | CLOSED | [V03](#v03), [V08](#v08) |
| TK1-ERR-09 | H | CLOSED | [V06](#v06) |
| TK1-ERR-10 | H | CLOSED | [V05](#v05) |
| TK1-ERR-11 | H | CLOSED: no applicable 403 route; required 404 verified | [V05](#v05) |
| TK1-ERR-12 | H | CLOSED | [V05](#v05), [V10](#v10), [V14](#v14) |
| TK1-ERR-13 | C | CLOSED | [V03](#v03), [V16](#v16), [V20](#v20) |
| TK1-AUTH-01 | H | CLOSED | [V04](#v04) |
| TK1-AUTH-02 | H | CLOSED | [V04](#v04), [V16](#v16) |
| TK1-AUTH-03 | H | CLOSED | [V04](#v04) |
| TK1-AUTH-04 | M | CLOSED | [V04](#v04) |
| TK1-AUTH-05 | H | CLOSED | [V04](#v04) |
| TK1-AUTH-06 | H | CLOSED | [V04](#v04) |
| TK1-AUTH-07 | H | CLOSED | [V04](#v04) |
| TK1-AUTH-08 | H | CLOSED | [V04](#v04), [V18](#v18) |
| TK1-AUTH-09 | H | CLOSED | [V04](#v04), [V16](#v16) |
| TK1-AUTH-10 | H | CLOSED | [V05](#v05) |
| TK1-AUTH-11 | C | CLOSED | [V05](#v05) |
| TK1-AUTH-12 | C | CLOSED | [V04](#v04), [V18](#v18) |
| TK1-OCC-01 | C | CLOSED | [V10](#v10), [V16](#v16), [V20](#v20) |
| TK1-OCC-02 | C | CLOSED | [V10](#v10), [V09](#v09) |
| TK1-OCC-03 | C | CLOSED | [V16](#v16) |
| TK1-OCC-04 | C | CLOSED | [V06](#v06), [V16](#v16) |
| TK1-OCC-05 | C | CLOSED | [V10](#v10), [V13](#v13), [V14](#v14), [V20](#v20) |
| TK1-IDEM-01 | H | CLOSED | [V06](#v06) |
| TK1-IDEM-02 | H | CLOSED | [V06](#v06) |
| TK1-IDEM-03 | C | CLOSED | [V06](#v06), [V16](#v16) |
| TK1-IDEM-04 | C | CLOSED | [V06](#v06), [V15](#v15) |
| TK1-IDEM-05 | C | CLOSED | [V06](#v06) |
| TK1-IDEM-06 | C | CLOSED | [V06](#v06), [V15](#v15) |
| TK1-IDEM-07 | H | CLOSED | [V06](#v06) |
| TK1-IDEM-08 | C | CLOSED | [V06](#v06), [V15](#v15), [V18](#v18) |
| TK1-IDEM-09 | C | CLOSED | [V16](#v16) |
| TK1-IDEM-10 | C | CLOSED | [V06](#v06) |
| TK1-IDEM-11 | H | CLOSED | [V06](#v06) |
| TK1-IDEM-12 | C | CLOSED | [V06](#v06), [V14](#v14), [V18](#v18) |
| TK1-IDEM-13 | C | CLOSED | [V15](#v15), [V18](#v18) |
| TK1-IDEM-14 | C | CLOSED | [V15](#v15), [V20](#v20) |
| TK1-BROWSE-01 | M | CLOSED | [V07](#v07) |
| TK1-BROWSE-02 | H | CLOSED | [V07](#v07) |
| TK1-BROWSE-03 | M | CLOSED | [V07](#v07) |
| TK1-AV-01 | H | CLOSED | [V08](#v08) |
| TK1-AV-02 | H | CLOSED | [V08](#v08), [V09](#v09) |
| TK1-AV-03 | M | CLOSED | [V08](#v08) |
| TK1-AV-04 | H | CLOSED | [V08](#v08), [V09](#v09) |
| TK1-AV-05 | H | CLOSED | [V08](#v08), [V09](#v09) |
| TK1-AV-06 | H | CLOSED | [V08](#v08) |
| TK1-AV-07 | H | CLOSED | [V08](#v08) |
| TK1-AV-08 | C | CLOSED | [V08](#v08), [V16](#v16) |
| TK1-AV-09 | H | CLOSED | [V08](#v08), [V18](#v18) |
| TK1-AV-10 | H | CLOSED | [V08](#v08) |
| TK1-AV-11 | H | CLOSED | [V08](#v08) |
| TK1-AV-12 | H | CLOSED | [V08](#v08), [V09](#v09) |
| TK1-CREATE-01 | H | CLOSED | [V10](#v10) |
| TK1-CREATE-02 | H | CLOSED | [V09](#v09), [V10](#v10) |
| TK1-CREATE-03 | H | CLOSED | [V10](#v10) |
| TK1-CREATE-04 | H | CLOSED | [V10](#v10) |
| TK1-CREATE-05 | C | CLOSED | [V10](#v10), [V16](#v16) |
| TK1-CREATE-06 | C | CLOSED | [V13](#v13), [V14](#v14), [V18](#v18) |
| TK1-CREATE-07 | C | CLOSED | [V10](#v10), [V16](#v16) |
| TK1-CREATE-08 | H | CLOSED | [V10](#v10) |
| TK1-CREATE-09 | H | CLOSED | [V09](#v09), [V10](#v10) |
| TK1-CREATE-10 | H | CLOSED | [V10](#v10) |
| TK1-CREATE-11 | H | CLOSED | [V10](#v10) |
| TK1-CREATE-12 | H | CLOSED | [V10](#v10) |
| TK1-CREATE-13 | H | CLOSED | [V10](#v10) |
| TK1-GET-01 | C | CLOSED | [V05](#v05), [V11](#v11) |
| TK1-GET-02 | H | CLOSED | [V11](#v11), [V13](#v13) |
| TK1-GET-03 | M | CLOSED | [V11](#v11) |
| TK1-GET-04 | C | CLOSED | [V05](#v05), [V11](#v11) |
| TK1-GET-05 | H | CLOSED | [V11](#v11), [V12](#v12) |
| TK1-CANCEL-01 | H | CLOSED | [V12](#v12) |
| TK1-CANCEL-02 | C | CLOSED | [V12](#v12), [V16](#v16) |
| TK1-CANCEL-03 | H | CLOSED | [V12](#v12) |
| TK1-CANCEL-04 | H | CLOSED | [V12](#v12) |
| TK1-CANCEL-05 | C | CLOSED | [V05](#v05), [V12](#v12) |
| TK1-PATCH-01 | H | CLOSED | [V13](#v13) |
| TK1-PATCH-02 | H | CLOSED | [V13](#v13) |
| TK1-PATCH-03 | H | CLOSED | [V13](#v13) |
| TK1-PATCH-04 | H | CLOSED | [V13](#v13) |
| TK1-PATCH-05 | H | CLOSED | [V13](#v13) |
| TK1-PATCH-06 | C | CLOSED | [V13](#v13), [V16](#v16) |
| TK1-PATCH-07 | C | CLOSED | [V13](#v13), [V20](#v20) |
| TK1-PATCH-08 | C | CLOSED | [V13](#v13), [V18](#v18) |
| TK1-TIME-01 | H | CLOSED | [V09](#v09) |
| TK1-TIME-02 | H | CLOSED | [V09](#v09) |
| TK1-TIME-03 | H | CLOSED | [V09](#v09) |
| TK1-TIME-04 | C | CLOSED | [V09](#v09) |
| TK1-TIME-05 | C | CLOSED | [V09](#v09) |
| TK1-TIME-06 | H | CLOSED | [V09](#v09) |
| TK1-TIME-07 | H | CLOSED | [V09](#v09) |
| TK1-TIME-08 | H | CLOSED | [V09](#v09) |
| TK1-TIME-09 | H | CLOSED | [V09](#v09) |
| TK1-TIME-10 | H | CLOSED | [V09](#v09) |
| TK1-XFER-01 | H | CLOSED | [V17](#v17) |
| TK1-XFER-02 | C | CLOSED | [V17](#v17), [V20](#v20) |
| TK1-XFER-03 | C | CLOSED | [V17](#v17), [V18](#v18) |
| TK1-XFER-04 | C | CLOSED | [V18](#v18) |
| TK1-XFER-05 | C | CLOSED | [V18](#v18) |
| TK1-XFER-06 | C | CLOSED | [V18](#v18), [V20](#v20) |
| TK1-XFER-07 | C | CLOSED | [V18](#v18) |
| TK1-XFER-08 | C | CLOSED | [V18](#v18), [V19](#v19) |
| TK1-XFER-09 | H | CLOSED | [V19](#v19) |
| TK1-XFER-10 | H | CLOSED | [V19](#v19) |
| TK1-XFER-11 | C | CLOSED | [V19](#v19), [V20](#v20) |
| TK1-XFER-12 | C | CLOSED | [V18](#v18) |
| TK1-XFER-13 | C | CLOSED | [V18](#v18) |
| TK1-XFER-14 | H | CLOSED | [V18](#v18) |
| TK1-XFER-15 | C | CLOSED | [V18](#v18) |
| TK1-XFER-16 | C | CLOSED | [V18](#v18) |
| TK1-XFER-17 | C | CLOSED | [V18](#v18) |
| TK1-XFER-18 | C | CLOSED | [V18](#v18) |
| TK1-XFER-19 | C | CLOSED | [V18](#v18) |
| TK1-XFER-20 | C | CLOSED | [V02](#v02), [V18](#v18) |
| TK1-XFER-21 | C | CLOSED | [V01](#v01), [V18](#v18) |
| TK1-XFER-22 | C | CLOSED | [V18](#v18) |
| TK1-XFER-23 | C | CLOSED | [V18](#v18) |
| TK1-MOVE-01 | C | CLOSED | [V05](#v05), [V14](#v14) |
| TK1-MOVE-02 | C | CLOSED | [V06](#v06), [V15](#v15) |
| TK1-MOVE-03 | H | CLOSED | [V14](#v14) |
| TK1-MOVE-04 | C | CLOSED | [V05](#v05), [V14](#v14) |
| TK1-MOVE-05 | H | CLOSED | [V14](#v14) |
| TK1-MOVE-06 | H | CLOSED | [V14](#v14) |
| TK1-MOVE-07 | H | CLOSED | [V14](#v14), [V15](#v15) |
| TK1-MOVE-08 | C | CLOSED | [V14](#v14), [V18](#v18) |
| TK1-MOVE-09 | H | CLOSED | [V14](#v14) |
| TK1-MOVE-10 | H | CLOSED | [V14](#v14) |
| TK1-MOVE-11 | H | CLOSED | [V14](#v14) |
| TK1-MOVE-12 | C | CLOSED | [V14](#v14) |
| TK1-MOVE-13 | C | CLOSED | [V14](#v14) |
| TK1-MOVE-14 | C | CLOSED | [V14](#v14) |
| TK1-MOVE-15 | C | CLOSED | [V14](#v14), [V16](#v16) |
| TK1-MOVE-16 | C | CLOSED | [V14](#v14) |
| TK1-MOVE-17 | C | CLOSED | [V14](#v14), [V16](#v16), [V20](#v20) |
| TK1-MOVE-18 | H | CLOSED | [V14](#v14), [V15](#v15) |
| TK1-MOVE-19 | C | CLOSED | [V15](#v15), [V18](#v18) |
| TK1-MOVE-20 | C | CLOSED | [V14](#v14), [V15](#v15), [V18](#v18) |
| TK1-MOVE-21 | C | CLOSED | [V18](#v18) |
| TK1-MOVE-22 | H | CLOSED | [V14](#v14), [V15](#v15) |
| TK1-MOVE-23 | H | CLOSED | [V14](#v14), [V15](#v15) |
| TK1-MOVE-24 | H | CLOSED | [V14](#v14) |
| TK1-MOVE-25 | H | CLOSED | [V14](#v14) |

Acceptance evidence is frozen after this exact-revision verdict and its separate sanitized evidence commit. No additional cosmetic reconciliation or retesting is required.
