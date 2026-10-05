# Stage 1 independent verification

VERDICT: REJECT

REVISION: `b03ce55647b70a46f478ea50ba077e02945bcefe`

Two HIGH product defects independently reproduced in the container built from the exact clean pinned revision. This is a targeted rejection gate, released by Conductor in room message `406df998-413e-42c1-ac42-6b763ef72cdd`. As directed, the full expensive campaign and official isolated acceptance harness are deferred to a replacement FULL production SHA. No ACCEPT is asserted, and no production file was changed by the verifier.

## Defect TK1-VERIFY-001

DEFECT ID: TK1-VERIFY-001

REQUIREMENT: §3.4 unknown request fields are ignored without error; §5 reserves malformed_request for unparseable JSON/wrong field types. Canonical TK1-HTTP-03, TK1-ERR-02; V03/V06/V18.

SEVERITY: HIGH

CLASSIFICATION: PRODUCT DEFECT

REPRODUCTION: `ignored_numeric_receipt_boundaries` in `campaign.py`. First reset the ordinary generated fixture successfully and log in. Send `POST /_test/reset`, Content-Type application/json; charset=utf-8, with the same valid fixture and an extra unknown top-level field whose literal JSON value is `1e309`. Exact construction: `encode_json(fixture())[:-1] + ',"ignored":1e309}'`. Fixture credentials are generated in memory and never recorded. The supplied numeric token is valid finite JSON numeric syntax; it is not the invalid constant Infinity.

EXPECTED: 204 No Content; install the fixture while ignoring the unknown field.

OBSERVED: 400 with `error.code = malformed_request`.

EVIDENCE: Campaign run `av-stage1-b03ce55647b7-88f033a9`, independent-summary.json and independent-console.log under the external diagnostic directory below. The same failure was independently reproduced in the preceding run `av-stage1-b03ce55647b7-df3ec2fd`.

AFFECTED SCOPE: Transport parses all POST/PATCH bodies with a binary-float converter that rejects overflow before unknown-field handling. The executed counterexample is reset; the shared parser exposes other write routes to the same rejection path. No broader route was silently marked tested.

REGRESSION RISK: A repair must preserve exact parsed-body equality and receipt transfer for large finite numbers without accepting non-JSON NaN/Infinity or turning numbers into strings. The executable case already includes replay, changed-number conflict and export/import assertions after this first failing step; those later assertions were NOT REACHED on the rejected revision.

REQUIRED OUTCOME: Accept valid JSON unknown numeric fields without a parse error. Preserve original JSON values through receipt comparison, export and import; retain malformed_request for invalid JSON constants/syntax. Release a new exact FULL production SHA for independent re-verification.

## Defect TK1-VERIFY-002

DEFECT ID: TK1-VERIFY-002

REQUIREMENT: §§4,8 permit arbitrary valid calendar dates and require every fitting grid slot in availability; §5 invalid-format rules do not make a valid date invalid. Canonical TK1-AV-04, TK1-TIME-01; V08/V09.

SEVERITY: HIGH

CLASSIFICATION: PRODUCT DEFECT

REPRODUCTION: `calendar_extremes` in `campaign.py`. Reset a UTC restaurant `r`, open every weekday 18:00..23:00, `slot_minutes = 1440`, duration 90 minutes, cutoff 120 minutes, with fixture-order tables `z` capacity 4, `a` capacity 2, `m` capacity 6. Request `GET /availability?restaurant_id=r&date=9999-12-31&party_size=2` without authentication. The same fixture first successfully serves date 0001-01-01 and creates its reservation; it has no booking on 9999-12-31.

EXPECTED: 200 with one fitting slot: local `9999-12-31T18:00`, instant `9999-12-31T18:00:00+00:00`, and available tables `["z","a","m"]` in fixture order.

OBSERVED: 422 with `error.code = validation_failed`.

EVIDENCE: Same run and independent-summary.json as TK1-VERIFY-001; separately executed case, so the numeric failure did not prevent the calendar reproduction. Both runs reproduced this outcome.

AFFECTED SCOPE: Availability advances its local grid candidate beyond the final representable calendar date after already generating a fitting slot; transport turns the resulting OverflowError into validation_failed. The executed boundary is UTC/date 9999-12-31/1440-minute step.

REGRESSION RISK: Grid termination must preserve unusual opening anchors, exact closing fits, large positive slot steps, closed days and DST first-occurrence/absolute-duration behavior. Do not add an undocumented calendar-date restriction to avoid the overflow.

REQUIRED OUTCOME: Return all fitting slots for valid dates without overflowing the final unused grid increment. Release a new exact FULL production SHA and pass both targeted reproductions plus the complete interacting campaign.

## Executed evidence and limits

| Check | Outcome |
|---|---|
| Exact materialization | Clean detached Linux-native clone; before/after SHA b03ce55647b70a46f478ea50ba077e02945bcefe; tracked production state remains clean |
| Docker build | PASS from pinned stage-1/Dockerfile |
| Offline runtime | PASS: unique Docker network inspected Internal=true; separate containers, no shared state volume |
| Resource configuration | 2 vCPU / 2 GiB per service; custom PORT 8765 and 8766; no host port assumptions |
| Readiness | Source 1.092 s; destination 1.276 s; allowed budget 60 s |
| Targeted independent cases | 2 executed; 2 PRODUCT DEFECT failures |
| HTTP budgets in targeted run | 8 requests; max ordinary 0.0299 s; max control 0.0846 s; budgets 5 s / 10 s |
| Calibration | PASS: closed-interval, second-fold and wall-duration variants distinguished; exact large-number serializer checked |
| Official checks | NOT RUN by independent verifier on this SHA, per Conductor's targeted-rejection instruction |
| Full concurrency/privacy/DST/transfer campaign | NOT RUN on this rejected SHA; prepared cases below are future gates, not passing evidence |
| Cleanup | All owned campaign containers/network/image removed; unrelated resources preserved; native pinned clone and external diagnostics retained |

External diagnostics: `/mnt/d/dark/band-work/checks/av-stage1-b03ce55647b7-88f033a9` (Windows `D:\dark\band-work\checks\av-stage1-b03ce55647b7-88f033a9`). Raw diagnostics remain outside the result repository. Only sanitized observations and executable verifier code are committed.

Executed campaign SHA256: `51efd1941daadac48dd3499c59fb47c80c6040557f6c7632d0bd90ec50546eb6`.

Executed orchestrator SHA256: `0f5bae349c877a32a03bca50e50b1f33fb73b508763821f2a5bff1dbae415318`.

Reproduce this targeted exact-revision gate from WSL Ubuntu:

```sh
source ~/.venvs/dark-factory/bin/activate
python /mnt/d/dark/band-work/result/evidence/stage-1/run_campaign.py --released --revision b03ce55647b70a46f478ea50ba077e02945bcefe --boundary-only --materialized /home/nurali/av-stage1-b03ce556-review-8810cfb1
```

Evidence remains tied to this production SHA even while shared HEAD and production repairs advance. No acceptance transfers to a replacement revision.

Authoritative specification: complete Tablekeeper Stage 1 contract supplied by Conductor in room message `00df3272-622a-4c08-b0b3-60ab0b13e0cf`. Baseline recorded as `a0ba09453b7630fcb5eed6982fe19a9a1aa0eb73`; this baseline is not a tested production revision.

Canonical ledger handoff: commit `d2f8b20705cc12cb0f0995f04bdc80f9dcb29a57`, containing only Contract Auditor's `requirements.md`; reported final ledger has 187 records (66 CRITICAL, 109 HIGH). This evidence-only revision is not a production verification release. Subsequent working ledger findings identify targeted regressions at production `b03ce55647b70a46f478ea50ba077e02945bcefe`; those peer findings are inputs to case preparation, not this verifier's executed evidence or verdict.

Systems handoff `STAGE1-PRODUCTION-001` supplied candidate SHA `b03ce55647b70a46f478ea50ba077e02945bcefe`. A clean detached Linux-native clone was materialized at `/home/nurali/av-stage1-b03ce556-review-8810cfb1`, with tracked stage source made read-only. Both `git rev-parse HEAD` and empty porcelain status confirmed the pinned state. Conductor subsequently released this exact SHA for targeted reproductions and a formal rejection, deferring the full campaign to its replacement.

Preliminary source observations for that exact candidate only: seeded/signup accounts store salted scrypt hashes (`n=16384`, `r=8`, `p=1`), not raw passwords; hash verification uses constant-time digest comparison. A single RLock encloses dispatch and deep-copying responses; export/import/reset and successful receipt publication share this boundary. Docker bundles timezone data and standard-library runtime code; transport binds 0.0.0.0 using PORT with fallback 8080. These observations do not substitute for the unexecuted full campaign. The numeric/date failure paths were independently confirmed over HTTP as reported above.

## Revision and execution gate

The verifier will materialize the released 40-character SHA into a clean Linux-native detached clone, preserve that clone for review/recovery, and freeze tracked source files. It will never execute against mutable shared HEAD or use Windows/WSL linked worktrees. Evidence commits will be distinct from the tested production revision.

`run_campaign.py` requires both a full SHA and an explicit release flag. It independently builds that exact stage directory, runs the unmodified supplied harness in isolated mode, then tests three disposable containers on a unique internal Docker network under 2 vCPU / 2 GiB limits per service. Two containers use distinct non-default PORT values, 8765 and 8766; the third omits PORT and must use 8080. No host port assumptions are required for internal-network tests. Container/network names are unique to each campaign. Only resources owned by that run are removed. The source is paused by the orchestrator before final transfer checks; imports and the A -> B -> C continuity check run with A unavailable.

Raw official logs and runtime diagnostics go outside result, under `/mnt/d/dark/band-work/checks/av-stage1-<sha-prefix>-<nonce>`. Tokens, fixture passwords, passwords from service state, and opaque exports stay in process memory; they are never written into evidence or diagnostics by the independent HTTP campaign. The executable generates fixture passwords in memory; no literal usable credential is committed.

## Preparation evidence

- Linux distribution: WSL Ubuntu. Docker server 29.8.0; Python 3.14.4 in `~/.venvs/dark-factory`.
- Observed host memory: 7,748 MiB total, 6,543 MiB available at preflight. Native `/tmp`: approximately 3.8 GiB available. Preflight will be refreshed at execution.
- Official checkout: `/mnt/d/dark/dark-factory-wearedevs`, revision `803560d2a678ace1414465c098eb0ab5380ffade`. Tracked status reports line-ending changes; `git diff --ignore-space-at-eol --stat` is empty. No official file was edited by this verifier. Exact official provenance and suite digest will be recorded with execution.
- No stale containers carrying the verifier ownership label were present at preparation. Existing unrelated containers were left alone.
- Python syntax validation passed for `campaign.py` and `run_campaign.py`.
- Independent oracle calibration passed. Controlled disposable predicate variants for closed-interval overlap, second occurrence of repeated local times, and wall-clock rather than absolute duration are distinguished by the boundary cases. This is oracle calibration, not end-to-end mutation validation of the production service.
- Shared assignment #3 is in progress. Contract Auditor's canonical `requirements.md` has been read, and uncovered CRITICAL/HIGH cases have been added without editing that seat's evidence. Exact-SHA result traceability will reference its stable TK1 requirement IDs and V01..V20 procedures. Preparation does not close any requirement as production-verified.

## Consolidated coverage map

| Contract | Independent campaign case | Evidence intended |
|---|---|---|
| §§3.4, 5, 7, 10 | `ignored_numeric_receipt_boundaries` | Finite valid JSON numeric syntax 1e309 in unknown fields, exact replay/conflict and receipt transfer without binary-float overflow; reject non-JSON NaN/Infinity |
| §§8, 9 | `calendar_extremes` | Dates 0001-01-01 and 9999-12-31 with a 1440-minute slot step; independent checks remain separate so one failure cannot hide the other |
| §§3, 6, 8 | `public_auth_reset` | Public browse with unknown token, restaurant fixture detail, unauthenticated/private access, signup/login validation, multiple sessions, repeated reset invalidates tokens |
| §§1, 4, 8 | `availability_oracle` | Enumerated opening grids (30/90, 17/43, 45/120), capacity thresholds, fixture order, occupied/empty slots, cancellation release, closed days |
| §§3, 5, 7, 8 | `validation` | Body parse/types, missing fields, party-size exceptions, bare-local format, impossible dates, decimal-only query counts, keys absent/empty/1/255/256 |
| §§1, 8 | `booking_boundaries_privacy` | Opening/end/grid boundaries, half-open adjacency, overlap rejection, hidden foreign lookup/cancel/amend, descending order, repeated cancel |
| §7 | `receipt_semantics` | JSON ordering/whitespace equivalence, unknown-field differences, reuse precedes field/current-resource checks, failed keys reusable, caller scoping, same body/key across distinct paths, original receipts after amendment/cancel |
| §§4, 8 | `amendments_atomic_cutoff` | Failed amendments preserve records/occupancy, successful move releases old slot, identities persist, historical creation, current-start cutoff and precedence |
| §9 | `dst_oracle` | All four specified Berlin/New York transitions; exhaustive independent availability; skipped hour rejection, first fold, absolute duration and offsets, occupied slots across transitions |
| §11 | `moves_atomic_precedence` | Three-way cyclic swap, response input order, no-op values, occupancy vs non-occupancy precedence, input-order failures, shape/duplicates, ownership privacy, failed keys reusable, historical receipts |
| §11 | `moves_eight_and_restaurant_scope` | Eight-item cyclic move, cross-restaurant table rejection, mixed-restaurant atomic rejection |
| §§3, 4, 8, 11 | `seed_ids_and_batch_cutoff` | Fixture identities of length 64, seeded lookup and occupancy, half-open seed boundary, overlap among resulting bookings, batch cutoff before changes, rollback and retry |
| §§5, 7, 8, 9, 11 | `patch_and_batch_field_validation` | PATCH and batch type/value/grid/hours/capacity errors and full rollback; both amendment routes reject skipped local times; batch key length boundaries |
| §§1, 7 | `concurrency_identical_50` | Coordinated 50-way identical creation: one 201, 49 identical 200 receipts, one record |
| §§1, 7 | `concurrency_distinct_50` | Coordinated 50-way contention: one booking, 49 table-unavailable errors, failed key reusable |
| §§1, 7 | `concurrency_changed_key_50` | Coordinated same-key/different-body competition: one initial response, matching receipts, changed-body conflicts, one record |
| §§1, 7, 11 | `concurrency_batch_snapshot` | 25 identical swaps and 25 readers start together; one 201 and 24 replays; readers observe complete before/after state |
| §§1, 6, 7 | `concurrency_signup_and_users` | Coordinated duplicate signup and different owners contending the same table; one identity/one booking |
| §§10, 11 | `export_atomic_batch` | Export races a multi-record swap; each imported snapshot has complete before/after records with the corresponding receipt; export is read-only |
| §§3, 10 | `control_replacement_races` | Reset and import overlap authenticated writes; resulting configuration, credentials, tokens, records, receipts and occupancy form one replacement generation |
| §§7, 8, 11 | `patch_batch_cancel_replay_races` | PATCH races a batch on the same record; occupancy agrees with final state; cancellation racing replays cannot resurrect a booking |
| §10 | `snapshot_import_receipts` | Source unavailable during transfer, A -> B -> C chaining, cross-process replacement, source writes after snapshot, repeated import, original identities/timestamps/statuses, multiple bearer sessions, hashed-password login continuity, create/batch receipts, failed key reuse, destination credential removal, malformed/invalid import rollback including login and receipt checks, reset after import |
| §§2, 3 | orchestration + supplied isolated harness | Docker build, single-container seed/dependencies, offline runtime, default/non-default PORT, readiness ≤60 s, requests ≤5 s, controls ≤10 s, CPU/memory limits |
| §6 | pinned source review (pending release) | Actual password-hashing function and absence of plaintext credential storage; HTTP behavior alone cannot establish storage representation |

The oracle uses only fixture data, Python IANA zone data, UTC interval arithmetic, and independently enumerated wall-clock grid points. It does not import, copy, or reuse production decision code. Cases reset isolated service state individually and retain only sanitized case results, status/code mismatches, request counts, and timing summaries.

Canonical procedure correlation: V01 orchestration and pinned delivery/source review; V02 public_auth_reset/seed_ids_and_batch_cutoff/control_replacement_races; V03 validation/patch_and_batch_field_validation; V04 public_auth_reset/concurrency_signup_and_users plus pinned hash review; V05 public_auth_reset/booking_boundaries_privacy/moves_atomic_precedence; V06 receipt_semantics/patch_and_batch_field_validation; V07 public_auth_reset/moves_eight_and_restaurant_scope; V08 availability_oracle; V09 dst_oracle/patch_and_batch_field_validation; V10 booking_boundaries_privacy/seed_ids_and_batch_cutoff; V11 booking_boundaries_privacy plus supplied checks/source review; V12 amendments_atomic_cutoff plus pinned exact-cutoff comparison review; V13 amendments_atomic_cutoff/patch_and_batch_field_validation; V14 moves_atomic_precedence/moves_eight_and_restaurant_scope/seed_ids_and_batch_cutoff; V15 receipt_semantics/snapshot_import_receipts; V16 coordinated concurrency cases; V17 export_atomic_batch; V18 snapshot_import_receipts; V19 snapshot_import_receipts; V20 control_replacement_races/export_atomic_batch/patch_batch_cancel_replay_races. Catalogue recommendations beyond these concrete cases are not silently marked passed; any remaining critical/high coverage gap at release will be addressed or reported before verdict.

`ignored_numeric_receipt_boundaries` and `calendar_extremes` additionally cover V03/V06/V08/V09/V18 and run first in the independent HTTP campaign. Its serializer and parser preserve exact finite JSON numbers independently using Decimal; opaque state containing such receipts is transferred without changing numeric values into Infinity or strings.

## Full campaign after replacement release

From WSL Ubuntu, with the authorized exact SHA substituted:

```sh
source ~/.venvs/dark-factory/bin/activate
python /mnt/d/dark/band-work/result/evidence/stage-1/run_campaign.py --released --revision FULL_PRODUCTION_SHA
```

The orchestration invokes the official final acceptance check as:

```sh
python -m harness run --track tablekeeper --mode isolated --repo PINNED_LINUX_CLONE --stage 1 --out EXTERNAL_DIAGNOSTIC_DIRECTORY/official
```

Campaign completion is not an automatic verdict. Any failure must first be classified as PRODUCT DEFECT, VERIFIER DEFECT, INFRASTRUCTURE DEFECT, or INCONCLUSIVE using the exact revision, a reproducible request, and diagnostics. A failed preflight is not a product defect. Source review and canonical required CRITICAL/HIGH obligations remain gates. If defects are repaired, re-verification requires a newly released full SHA and a new verdict.

## Remaining acceptance gates

This exact revision is REJECTED. The full official isolated harness, all prepared independent cases, compatibility checks, 50-request concurrency, clean-environment reproducibility, performance evidence and new pinned source review remain mandatory for a newly released replacement SHA. Canonical obligations remain OPEN except for the specific observations explicitly reported here. The evidence commit is separate from the production revision tested.
