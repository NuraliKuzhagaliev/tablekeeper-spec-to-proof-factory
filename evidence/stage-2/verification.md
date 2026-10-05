# Stage 2 cumulative independent verification

VERDICT: ACCEPT

REVISION: 2c431f7e6c0c5ed3bdae232bde255ec24c1bbab3

SPECIFICATION COVERAGE: All 338 canonical obligations closed at this revision: 115 CRITICAL, 200 HIGH and 23 MEDIUM. Exact cumulative Stage 1+2 authority is Conductor release 3d43e075-3029-4ad4-9efb-9383e34284d5, the readonly official specifications, and canonical ledger FULL 4e11f5e91e2186a5461345977f08a1c51f4d057f. The requirement ledger remains untouched. Historical Stage 1 acceptance does not substitute for current execution.

OFFICIAL CHECKS: Isolated cumulative harness PASS: Stage 1 120/120 and Stage 2 25/25; zero failed/errors/skipped/deselected/xfailed in the applicable suites. Upgrade checks included. Official revision 803560d2a678ace1414465c098eb0ab5380ffade; suite digest f98962753222bf04eae211beb9e8bf8b9f3edd062beeb55ae857391365a6fb83. Official report revision equals the tested production SHA. The optional later-stage probe is outside this acceptance scope.

INDEPENDENT ROBUSTNESS CHECKS: 59 distinct passing macro cases: 29 inherited regressions, 13 combined-table API cases, 9 initial browser cases, 3 explicit API protocols and 5 additional browser protocols. 1754 instrumented API-only HTTP requests observed across preserved checkpoints, including repeated controls and investigations; browser fetches and browser-directed API setup calls are additional and excluded from this count. Every instrumented normal/control response is checked against the specified timeout, JSON/error envelope and absence of 5xx. All blocking protocol gaps have passing evidence; no unresolved PRODUCT DEFECT or INCONCLUSIVE case remains.

COMPATIBILITY CHECKS: Separately built accepted Stage 1 d41a7627711951a07ce7a1718fac47c6ea5b6dd4 -> this Stage 2 revision; retained genuine old tokens and hashed login, identities/timestamps/statuses, original create/batch response JSON, failed-key reuse and destination replacement. Source-pause handshakes prove no dependency on a live source. A->B->C transfer, repeated/invalid import, reset erasure, concurrent snapshots, same-tab pending single upgrade and pair import recovery pass. Current records gain table_ids; historical legacy table_id receipts remain exactly original, with label fallback in the browser.

CLEAN-ENVIRONMENT CHECKS: Clean detached clone made with --no-hardlinks at /tmp/av-stage2-2c431f7e6c0c-a76f6c90-vwdnv_ei/candidate; tracked files read-only, exact HEAD verified before/after. Stage 2 Git tree 5e0f3ee38f68f7cb846b28c5dbd1850e7b768f91; frozen Stage 1 tree 7d35fe7568addec4437c2eb8705ed788ed46f0f2. The official harness calls its clean submitted checkout working-tree provenance; independent byte/blob and clean-HEAD binding establishes exact committed content. Docker 29.8.0; observed host 20 CPUs/8125067264 bytes. Services ran on unique internal networks with 2 vCPU/2147483648-byte limits; packaged local HTML/JS/CSS and bundled tzdata worked offline. Distinct custom ports and omitted-PORT default 8080 both passed.

KNOWN LIMITATIONS: State is ephemeral by contract. This campaign establishes the specified finite scenarios and budgets, not unlimited datasets/performance. Exact sums of compact numbers with arbitrarily disparate exponents can require mathematically unbounded output size; finite memory/time cannot honestly prove unlimited output. No arbitrary numeric range or silent rounding is adopted, and feasible correctness is not waived. Response pair member order beyond explicit availability/UI declaration ordering, gap-valued business-hour boundaries, equal-start ties, duplicate JSON keys and edit-then-revert behavior remain specified interpretation boundaries rather than invented blockers. No reload recovery, cross-tab synchronization, future-stage behavior or downgrade is claimed.

EVIDENCE ARTIFACTS: This one report, executable independent campaign/oracles/runtime probe, and two reviewed sanitized confirmation screenshots. Evidence commit is distinct from production; its FULL SHA is reported in the final room handoff. Raw diagnostics remain outside result. No credentials, tokens, passwords, raw environments or opaque exports are committed.

## Observed budgets and exact-number bounds

Observed maximum instrumented ordinary API request: 0.045800 seconds (budget 5). Maximum test control: 0.102228 seconds (budget 10). Macro duration can include multiple requests or intentionally held callbacks and is not a per-request latency. Main independent service health observations from actual Docker StartedAt: 0.709s, 0.754s, 0.703s, 0.773s, within 60 seconds. Published standalone actual mapping 127.0.0.1:53715, readiness 0.857 seconds, reset 0.094208s/read 0.082676s; inspected limits 2000000000 2147483648.

The exact-number reference uses Fraction(Decimal) and integer thresholds, never production parser/equality/addition functions. Five feasible vectors check full option capacities/order, sum-1/sum/sum+1 thresholds, exact party responses, equivalent-number replay and failed-key reuse. The largest representation has 2049 decimal digits; it also survived source-state destruction, A->B->C transfer, multiple tokens, cancellation and historical create/move receipts without rounding.

| Capacity inputs | Exact sum digits | Ordinary max seconds | Control max seconds | Outcome |
|---|---:|---:|---:|---|
| 1E+18 + 1 | 19 | 0.029981 | 0.068875 | PASS |
| 1E+56 + 1E+29 | 57 | 0.028817 | 0.058225 | PASS |
| 1E+309 + 2 | 310 | 0.030823 | 0.056497 | PASS |
| 1E+1000 + 1E+7 | 1001 | 0.028950 | 0.056189 | PASS |
| 1E+2048 + 1E+17 | 2049 | 0.028668 | 0.058547 | PASS |

## Independent decision and concurrency evidence

The verifier imports only its own frozen Stage 1 campaign and independent pair models. Minute-grid/IANA first-occurrence/absolute interval enumeration, approved pair sets and exact sums are independently derived. Singles/pairs are compared in fixture/declaration orientation; approval is not transitive. Every member participates in half-open occupancy. Validation/current cutoff/input ordering precedes final occupancy as specified; used-key parsed-body conflict/replay precedes all field/resource checks. Arrays retain order for receipt identity, while pair membership is unordered. Semantic pair PATCH no-ops and unchanged batch values retain identities/timestamps/history.

Coordinated 50-worker identical requests return exactly one 201 and 49 identical 200 bodies with one effect. Fifty distinct single/pair/member contenders are checked against final disjoint winners and corresponding rejections. Create/PATCH three-operation outcomes are compared against all six independently enumerated serial orders. Twenty exports coordinated with a batch swap preserve either complete before-state/unspent receipt or complete after-state/original receipt. Twenty-five swaps plus twenty-five reads audit whole member sets and stable identities. Inherited reset/import/cancel/PATCH/replay races, privacy, short seeded passwords, restaurant-scoped duplicate table IDs, exact JSON precision/booleans/ignored fields, calendar extremes and all four required DST transitions were reexecuted. Pair create/PATCH/moves independently cover skipped starts and first-fold absolute duration.

Controlled oracle calibration detected six inherited mistakes and six pair/receipt mistakes, plus rounded-sum variants for all five exact capacity vectors; 49 bounded member comparisons pass. Calibration is evidence about verifier discrimination, not production success. Exact-source review separately confirms scrypt hashing in reset/signup, validated imported hashes, random salts, constant-time comparison, one observable state lock, completed receipt copies and packaged offline assets. Source checks corroborate behavioral evidence and are not used as an oracle. Repository/owner provenance and standard-library-only production imports support original implementation scope; no external domain-product code/schema/API material was used by this verification.

## Independent browser and rendered review

Actual packaged pages at 375 and 1280 CSS pixels pass direct HTML route/MIME checks, public browsing, signup/login/logout/current-user, exact grid hooks and single/pair availability truth, closed versus no-seats states, labels, keyboard cell activation/form submission and focus. Long restaurant/member labels wrap without page scrolling. Every audited visible input has an associated visible label. Primary actions, local times and human seating labels are prominent; approved combinations read as intentional seats. Consistent warm cream/terracotta/green styling, type hierarchy, spacing/navigation and mobile stacking form a coherent restaurant product rather than a test dashboard. Independent screenshots were actually inspected, not accepted from locator success or owner screenshots.

Available pale-green/dashed cells, muted unavailable cells and filled-green selections are distinct. Loading text/spinner, considered empty states, green confirmation, red refusal and amber uncertainty are visibly distinct and communicate the authoritative outcome. Password fields are masked in auth diagnostics. Computed composited foreground/background metrics corroborate readable text/control contrast; numerical ratios are supporting evidence, not new specification thresholds. Keyboard focus is an apparent outline/offset and was visually inspected. The two committed viewport screenshots contain synthetic labels/references only.

Deterministic held callbacks cover old availability, restaurant detail, closed/error results, selection labels, conflict refresh versus a newer query, submitted caller/input, lookup record/detail and cancellation. New intent/user/reference remains authoritative. Conflict keeps the selected editable form/inputs, refreshes actual availability and shows no false confirmation. Single/pair response loss before forwarding, after real commit, and unreadable committed JSON show uncertainty; identical unchanged key/body/user retries contact the real server and recover its original reference with one effect. Successful retry also contacts the server; changed fields use a new identity. Same-tab legacy/pair imports occur between requests without reload, keeping genuine source tokens, pending form/body/key and original receipt labels. Off-origin runtime requests are blocked by the verifier; tested resources remain same-origin. Final explicit browser protocols record zero unhandled runtime errors.

![Independent pair confirmation at 375 CSS pixels](independent-pair-confirmation-375.png)

![Independent pair confirmation at 1280 CSS pixels](independent-pair-confirmation-1280.png)

## Recovery and classification

Initial checkpoint a76f6c90: INFRASTRUCTURE DEFECT, Docker Desktop registry DNS failed before product execution. Clean immutable clone and logs retained. Disposable credential-free Docker configuration plus successful base pull recovered the build; no product change. Main checkpoint 91b7e86e completed all official and 51 initial independent cases.

Additional protocol checkpoint ba935977 preserved passing API/lookup/visual checks, with verifier-control faults: expected availability omitted a real competing booking, an error setup raced catalogue loading, and held Playwright APIResponse handles were disposed during failed-case cleanup. These are VERIFIER DEFECTS; corrected independent expected occupancy/setup, copied response bytes and bounded cleanup recovered the controls. Checkpoint17828213 passes crossed search/detail/closed/error and conflict refresh/frozen-search intent. A newly overridden held-write handler had omitted request logging, making a changed-key assertion compare a request with itself; recording held requests fixes this VERIFIER DEFECT, and checkpoint73b7e4b4 passes unreadable/changed-intent recovery. It also supplies reviewed long-label screenshots. In numeric chain checkpoint5372e8af the verifier expected first-use201 twice after exporting an already-completed retry key; corrected third-process expectation is original200 replay. Checkpointc1ef0446 closes the exact numeric snapshot/receipt protocol. No correction altered production or official checks; all valid completed evidence is retained. No acceptance is inferred from an interrupted or failed checkpoint.

## Reproduction and executable identities

Use the supplied verifier venv and official readonly checkout. From Linux run `python evidence/stage-2/run_campaign.py --released --revision 2c431f7e6c0c5ed3bdae232bde255ec24c1bbab3 --repo /mnt/d/dark/band-work/result`. It materializes a clean native exact clone, runs official isolated cumulative checks, then inherited/pair/browser/explicit protocols. The standalone `runtime_probe.py --released --revision FULL --materialized NATIVE_PIN` queries an actual Docker-assigned host mapping. Resuming uses --materialized and --resume-official with exact revision, digest and complete count checks. Unique owned resources are removed; other seats/resources are untouched.

| Owned executable | SHA-256 of final reproducible file |
|---|---|
| browser_campaign.py | e6100b41315a456a53d05fb4f0f77fdff10622558c64c048a038007bc45ac397 |
| campaign.py | 90e834d3fc9737693a95a616a189e383a52396faecc37109589fc164c81f3c6a |
| extensions.py | bb0d09e39971e80e332839a06dd0777ef09aba1a3ce3cdf453f397141b0ef975 |
| oracle.py | d66aea543bab43211f44e9be6cf4bd4a25db23353343c79ed767e077acc57198 |
| run_campaign.py | 5cd5ed5b6705519b161ba30638f5f69e7639553681deaff6dc3d1cae6230054e |
| runtime_probe.py | c6eb80924e74c6817761b058b438678aade5c34b99c4db9bc5b63c9bcbff1475 |
| stage1_campaign.py | 4fe9e7c5670f89132d36164332c24bf8abe12983c997923efec88a0345707176 |

The main checkpoint records earlier run_campaign.py identity e6fb0c241487c7f5d7097067e1632ff4f106da72671120d66f2dd55d07c478bb; later changes add the explicit-protocol phase/runtime probe. Initial core oracle/API/browser files remain byte-identical to their observed main identities. Each preserved checkpoint records its own executable hashes; the final extension fixes are the ones used for all resolved protocols. This separates tested-production identity from evolving verifier-control identity. Frozen Stage 1 production/evidence remain unchanged.

## Preserved exact-revision checkpoints

| Checkpoint | Evidence |
|---|---|
| /mnt/d/dark/band-work/checks/av-stage2-2c431f7e6c0c-91b7e86e | Complete official report/logs; inherited/pairs/browser summaries; clean pin, image builds, limits, internal network, readiness and source-pause markers |
| /mnt/d/dark/band-work/checks/av-stage2-2c431f7e6c0c-ba935977 | Explicit protocol summary, controls, executable identities and sanitized screen diagnostics; valid passes retained as described above |
| /mnt/d/dark/band-work/checks/av-stage2-2c431f7e6c0c-17828213 | Explicit protocol summary, controls, executable identities and sanitized screen diagnostics; valid passes retained as described above |
| /mnt/d/dark/band-work/checks/av-stage2-2c431f7e6c0c-73b7e4b4 | Explicit protocol summary, controls, executable identities and sanitized screen diagnostics; valid passes retained as described above |
| /mnt/d/dark/band-work/checks/av-stage2-2c431f7e6c0c-5372e8af | Explicit protocol summary, controls, executable identities and sanitized screen diagnostics; valid passes retained as described above |
| /mnt/d/dark/band-work/checks/av-stage2-2c431f7e6c0c-c1ef0446 | Explicit protocol summary, controls, executable identities and sanitized screen diagnostics; valid passes retained as described above |
| /mnt/d/dark/band-work/checks/av-published-2c431f7e6c0c-5fafe41c | Actual host mapping/readiness/reset/read/resource check |
| /mnt/d/dark/band-work/checks/av-stage2-preparation-c618d1eb | Oracle/control calibration, release guards, source-audit manifest and final aggregate |

## Distinct passing case evidence

| Case | Passing checkpoint | Macro seconds |
|---|---|
| amendments_atomic_cutoff | inherited | 0.202 |
| availability_oracle | inherited | 0.425 |
| booking_boundaries_privacy | inherited | 0.144 |
| calendar_extremes | inherited | 0.095 |
| cancelled_after_cutoff_temporal | inherited | 18.523 |
| concurrency_batch_snapshot | inherited | 0.143 |
| concurrency_changed_key_50 | inherited | 0.142 |
| concurrency_distinct_50 | inherited | 0.159 |
| concurrency_identical_50 | inherited | 0.145 |
| concurrency_signup_and_users | inherited | 0.206 |
| conflict_preserves_form | browser | 6.962 |
| conflict_refresh_and_frozen_search_intent | av-stage2-2c431f7e6c0c-17828213 | 8.107 |
| control_receipt_erasure | inherited | 0.281 |
| control_replacement_races | inherited | 0.295 |
| crossed_detail_closed_and_error | av-stage2-2c431f7e6c0c-17828213 | 4.481 |
| desktop_long_labels_and_no_seats | av-stage2-2c431f7e6c0c-73b7e4b4 | 6.977 |
| dst_closing_instant_boundaries | inherited | 0.392 |
| dst_oracle | inherited | 0.201 |
| duplicate_table_ids_and_short_seed_password | inherited | 0.178 |
| export_atomic_batch | inherited | 0.198 |
| ignored_numeric_receipt_boundaries | inherited | 0.232 |
| lookup_detail_and_cancel_races | av-stage2-2c431f7e6c0c-ba935977 | 6.364 |
| lost_response_recovery | browser | 9.864 |
| moves_atomic_precedence | inherited | 0.159 |
| moves_eight_and_restaurant_scope | inherited | 0.108 |
| numeric_equivalence_and_precision | inherited | 0.750 |
| offset_ordering_and_amendment | inherited | 0.094 |
| out_of_order_search | browser | 2.172 |
| pair_amendment_dst_and_cutoff | av-stage2-2c431f7e6c0c-ba935977 | 0.856 |
| pair_batch_final_state | pairs | 0.101 |
| pair_concurrency_50 | pairs | 0.289 |
| pair_create_validation | pairs | 1.273 |
| pair_dst | pairs | 0.370 |
| pair_exact_sum_snapshot_transfer | av-stage2-2c431f7e6c0c-c1ef0446 | 0.373 |
| pair_model_and_seeds | pairs | 0.367 |
| pair_numeric_capacity | pairs | 0.526 |
| pair_options_oracle | pairs | 0.367 |
| pair_patch_create_serial_oracle | pairs | 0.384 |
| pair_patch_replacement_rollback | pairs | 0.107 |
| pair_reads_and_atomic_snapshots | pairs | 0.326 |
| pair_receipt_array_identity | pairs | 0.095 |
| pair_same_tab_import | browser | 2.670 |
| pair_selector_precedence_and_receipts | av-stage2-2c431f7e6c0c-ba935977 | 0.248 |
| pair_snapshot_receipts | pairs | 0.543 |
| patch_and_batch_field_validation | inherited | 0.245 |
| patch_batch_cancel_replay_races | inherited | 0.122 |
| public_auth_reset | inherited | 0.290 |
| receipt_semantics | inherited | 0.145 |
| routes_auth_grid | browser | 3.465 |
| same_tab_upgrade | browser | 2.120 |
| seed_ids_and_batch_cutoff | inherited | 0.108 |
| signup_keyboard_empty_refused | browser | 2.081 |
| snapshot_import_receipts | inherited | 0.691 |
| stage1_upgrade_receipts | pairs | 0.624 |
| submitted_user_race | browser | 4.467 |
| success_retry_lookup | browser | 10.874 |
| terminal_zone_instants | inherited | 0.195 |
| unreadable_and_changed_pending_intent | av-stage2-2c431f7e6c0c-73b7e4b4 | 13.740 |
| validation | inherited | 0.131 |

## Canonical procedure closure

All 40 procedure profiles have actual exact-revision evidence. The case table and explicit narratives above provide the executed binding; these are not preparation-only promises.

| Profile | Executed evidence binding |
|---|---|
| <a id="v01"></a>V01 | Pinned build/source inspections, custom/default PORT, standalone published mapping, offline bundled browser runtime; runner; applicable explicit protocols PASS |
| <a id="v02"></a>V02 | 29 inherited cases plus pair_model_and_seeds; reset/import replacement and seeded cancelled pairs; applicable explicit protocols PASS |
| <a id="v03"></a>V03 | Inherited validation/numeric/calendar matrix plus pair_create_validation and pair selectors in PATCH/moves; applicable explicit protocols PASS |
| <a id="v04"></a>V04 | Inherited auth/short seeded password/multiple sessions; browser signup/login; hashing inspection on released source; applicable explicit protocols PASS |
| <a id="v05"></a>V05 | Inherited privacy/token matrix; routes_auth_grid and own/foreign/unknown lookup/refusal vectors; applicable explicit protocols PASS |
| <a id="v06"></a>V06 | Inherited receipt matrix; pair_receipt_array_identity; reversed move arrays, user/path scopes and failed keys; applicable explicit protocols PASS |
| <a id="v07"></a>V07 | Inherited restaurants/duplicate table namespaces; pair_model_and_seeds and declared-order details; applicable explicit protocols PASS |
| <a id="v08"></a>V08 | Inherited unusual grid/capacity/closed/full slots; pair_options_oracle and numeric summed capacities; applicable explicit protocols PASS |
| <a id="v09"></a>V09 | Inherited four DST transitions/closing/calendar bounds; pair_dst and pair_amendment_dst_and_cutoff; applicable explicit protocols PASS |
| <a id="v10"></a>V10 | Inherited create fields/cutoff/past/reference uniqueness; pair_create_validation and member adjacency; applicable explicit protocols PASS |
| <a id="v11"></a>V11 | Every current-record read audited by member/absolute instant; inherited offset ordering and post-amendment ordering; applicable explicit protocols PASS |
| <a id="v12"></a>V12 | Inherited cutoff/live repeated cancellation; pair cancellation and browser cutoff refusal; applicable explicit protocols PASS |
| <a id="v13"></a>V13 | Inherited amend validation/rollback; pair_patch_replacement_rollback and exhaustive patch/create serial oracle; applicable explicit protocols PASS |
| <a id="v14"></a>V14 | Inherited batch shape/precedence/cutoff/1..8; pair_batch_final_state and member-conflict vectors; applicable explicit protocols PASS |
| <a id="v15"></a>V15 | Inherited immutable receipt histories; pair receipts after cancellation, pair batch swap receipt, unchanged no-ops; applicable explicit protocols PASS |
| <a id="v16"></a>V16 | Inherited coordinated 50-way retries/contention; pair_concurrency_50 and pair_reads_and_atomic_snapshots; applicable explicit protocols PASS |
| <a id="v17"></a>V17 | Inherited atomic/read-only exports; pair_reads_and_atomic_snapshots (records plus receipt) and late source writes; applicable explicit protocols PASS |
| <a id="v18"></a>V18 | Stage1_upgrade_receipts; pair_snapshot_receipts; same_tab_upgrade; pair_same_tab_import; A->B->C private transfer; applicable explicit protocols PASS |
| <a id="v19"></a>V19 | Inherited invalid import rollback/login/receipt; pair invalid-state/track and unchanged member occupancy; applicable explicit protocols PASS |
| <a id="v20"></a>V20 | Inherited reset/import/PATCH/cancel/replay races; pair snapshot/swap/read serial states and receipt generation boundaries; applicable explicit protocols PASS |
| <a id="w01"></a>W01 | routes_auth_grid at 375/1280; exact HTML/API MIME; assets blocked off-origin; navigation and packaged source review; applicable explicit protocols PASS |
| <a id="w02"></a>W02 | routes_auth_grid, signup_keyboard_empty_refused, successful signup/login, errors, current-user every route and logout; applicable explicit protocols PASS |
| <a id="w03"></a>W03 | grid oracle versus all single/pair hooks; no-slots, no seats, unauth selection, no-op unavailable cells; searched-party intent; applicable explicit protocols PASS |
| <a id="w04"></a>W04 | out_of_order_search plus deterministic gate variants A/B crossed availability/details, late closed/error A, late conflict refresh C versus D; applicable explicit protocols PASS |
| <a id="w05"></a>W05 | success_retry_lookup single/pair; summary labels/time, searched party, unchanged key/body/user and one effect; changed selection/time; applicable explicit protocols PASS |
| <a id="w06"></a>W06 | conflict_preserves_form single/pair; another user takes one member; error+refresh preserves full form; deferred refresh versus new search; applicable explicit protocols PASS |
| <a id="w07"></a>W07 | lost_response_recovery before/after commit for singles/pairs; changed-field/double-submit variants; exact equality and server count; applicable explicit protocols PASS |
| <a id="w08"></a>W08 | success_retry_lookup; signup_keyboard_empty_refused cutoff; foreign/unknown lookup and stale detail removal; exact statuses and labels; applicable explicit protocols PASS |
| <a id="w09"></a>W09 | pair_model_and_seeds, omitted/empty combinable, confirmed/cancelled selectors, namespace and declaration fidelity; applicable explicit protocols PASS |
| <a id="w10"></a>W10 | pair_create_validation, pair_receipt_array_identity, pair_numeric_capacity; isolation of each selector fault and state rollback; applicable explicit protocols PASS |
| <a id="w11"></a>W11 | pair_options_oracle and pair reads; all singles/pairs in fixture/declaration orientation/order, summed capacity and member occupancy; applicable explicit protocols PASS |
| <a id="w12"></a>W12 | pair_patch_replacement_rollback; single<->pair, stored dual single shape, legacy replacement, no-op/cancel/cutoff/rollback; applicable explicit protocols PASS |
| <a id="w13"></a>W13 | pair_batch_final_state plus inherited batch limits/precedence; swaps, unchanged occupancy, unlisted conflicts and receipt history; applicable explicit protocols PASS |
| <a id="w14"></a>W14 | grid oracle, all pair/single booking/lookup labels; conflict/loss/recovery UI and declared-order pair hooks; applicable explicit protocols PASS |
| <a id="w15"></a>W15 | pair_dst plus inherited DST; pair_amendment_dst_and_cutoff; absolute member intervals and browser Tokyo timezone; applicable explicit protocols PASS |
| <a id="w16"></a>W16 | pair_concurrency_50, pair_reads_and_atomic_snapshots, pair_patch_create_serial_oracle; all six bounded serial orders and member audit; applicable explicit protocols PASS |
| <a id="w17"></a>W17 | 375/1280 screenshots/DOM widths, labels, keyboard activation/focus, computed contrast/states plus independent rendered product review; applicable explicit protocols PASS |
| <a id="w18"></a>W18 | stage1_upgrade_receipts and same_tab_upgrade: accepted Stage1 source unavailable, original legacy receipt unchanged, actual old token and same-tab pending retry; applicable explicit protocols PASS |
| <a id="w19"></a>W19 | pair_snapshot_receipts, pair_same_tab_import, pair_reads_and_atomic_snapshots: current-format portability and coherent member/receipt snapshots; applicable explicit protocols PASS |
| <a id="w20"></a>W20 | Git/release inspection: accepted frozen Stage1 tree, committed copy baseline, exact integrated release and separate evidence window; no acceptance inheritance; applicable explicit protocols PASS |

## Atomic requirement closure

Canonical ledger remains the requirement authority; this report alone records independent closure on the named production revision. All 338 rows, including every CRITICAL/HIGH row, are bound to executed evidence profiles above.

| Requirement | Risk | Exact-revision status | Evidence profiles |
|---|---|---|---|
| TK1-SC-01 | M | CLOSED / PASS | [V01](#v01) |
| TK1-SC-02 | H | CLOSED / PASS | [V01](#v01) |
| TK1-SC-03 | H | CLOSED / PASS | [V01](#v01) |
| TK1-SC-04 | H | CLOSED / PASS | [V01](#v01) |
| TK1-RUN-01 | H | CLOSED / PASS | [V01](#v01) |
| TK1-RUN-02 | M | CLOSED / PASS | [V01](#v01) |
| TK1-RUN-03 | H | CLOSED / PASS | [V01](#v01) |
| TK1-RUN-04 | H | CLOSED / PASS | [V01](#v01) |
| TK1-RUN-05 | H | CLOSED / PASS | [V01](#v01) |
| TK1-RUN-06 | H | CLOSED / PASS | [V01](#v01), [V16](#v16) |
| TK1-RUN-07 | H | CLOSED / PASS | [V16](#v16) |
| TK1-RUN-08 | H | CLOSED / PASS | [V02](#v02), [V18](#v18) |
| TK1-RUN-09 | H | CLOSED / PASS | [V01](#v01) |
| TK1-RUN-10 | M | CLOSED / PASS | [V01](#v01) |
| TK1-RUN-11 | H | CLOSED / PASS | [V01](#v01) |
| TK1-RUN-12 | H | CLOSED / PASS | [V01](#v01) |
| TK1-RUN-13 | H | CLOSED / PASS | [V01](#v01), [V16](#v16) |
| TK1-HTTP-01 | M | CLOSED / PASS | [V03](#v03) |
| TK1-HTTP-02 | H | CLOSED / PASS | [V03](#v03), [V09](#v09) |
| TK1-HTTP-03 | H | CLOSED / PASS | [V03](#v03), [V06](#v06) |
| TK1-HTTP-04 | M | CLOSED / PASS | [V03](#v03) |
| TK1-HTTP-05 | H | CLOSED / PASS | [V03](#v03), [V02](#v02) |
| TK1-FIX-01 | H | CLOSED / PASS | [V02](#v02) |
| TK1-FIX-02 | C | CLOSED / PASS | [V02](#v02), [V20](#v20) |
| TK1-FIX-03 | M | CLOSED / PASS | [V02](#v02) |
| TK1-FIX-04 | C | CLOSED / PASS | [V02](#v02), [V20](#v20) |
| TK1-FIX-05 | H | CLOSED / PASS | [V02](#v02) |
| TK1-FIX-06 | M | CLOSED / PASS | [V02](#v02) |
| TK1-FIX-07 | H | CLOSED / PASS | [V02](#v02), [V09](#v09) |
| TK1-FIX-08 | H | CLOSED / PASS | [V08](#v08) |
| TK1-FIX-09 | H | CLOSED / PASS | [V08](#v08), [V10](#v10) |
| TK1-FIX-10 | H | CLOSED / PASS | [V08](#v08), [V10](#v10) |
| TK1-FIX-11 | H | CLOSED / PASS | [V12](#v12), [V13](#v13) |
| TK1-FIX-12 | H | CLOSED / PASS | [V08](#v08), [V10](#v10) |
| TK1-FIX-13 | H | CLOSED / PASS | [V02](#v02), [V04](#v04) |
| TK1-FIX-14 | H | CLOSED / PASS | [V02](#v02), [V11](#v11) |
| TK1-FIX-15 | C | CLOSED / PASS | [V02](#v02), [V08](#v08) |
| TK1-FIX-16 | H | CLOSED / PASS | [V10](#v10) |
| TK1-FIX-17 | H | CLOSED / PASS | [V12](#v12), [V13](#v13) |
| TK1-ERR-01 | H | CLOSED / PASS | [V03](#v03) |
| TK1-ERR-02 | H | CLOSED / PASS | [V03](#v03) |
| TK1-ERR-03 | H | CLOSED / PASS | [V03](#v03), [V14](#v14) |
| TK1-ERR-04 | H | CLOSED / PASS | [V03](#v03) |
| TK1-ERR-05 | H | CLOSED / PASS | [V03](#v03) |
| TK1-ERR-06 | H | CLOSED / PASS | [V03](#v03), [V10](#v10), [V13](#v13), [V14](#v14) |
| TK1-ERR-07 | H | CLOSED / PASS | [V03](#v03), [V09](#v09) |
| TK1-ERR-08 | H | CLOSED / PASS | [V03](#v03), [V08](#v08) |
| TK1-ERR-09 | H | CLOSED / PASS | [V06](#v06) |
| TK1-ERR-10 | H | CLOSED / PASS | [V05](#v05) |
| TK1-ERR-11 | H | CLOSED / PASS | [V05](#v05) |
| TK1-ERR-12 | H | CLOSED / PASS | [V05](#v05), [V10](#v10), [V14](#v14) |
| TK1-ERR-13 | C | CLOSED / PASS | [V03](#v03), [V16](#v16), [V20](#v20) |
| TK1-AUTH-01 | H | CLOSED / PASS | [V04](#v04) |
| TK1-AUTH-02 | H | CLOSED / PASS | [V04](#v04), [V16](#v16) |
| TK1-AUTH-03 | H | CLOSED / PASS | [V04](#v04) |
| TK1-AUTH-04 | M | CLOSED / PASS | [V04](#v04) |
| TK1-AUTH-05 | H | CLOSED / PASS | [V04](#v04) |
| TK1-AUTH-06 | H | CLOSED / PASS | [V04](#v04) |
| TK1-AUTH-07 | H | CLOSED / PASS | [V04](#v04) |
| TK1-AUTH-08 | H | CLOSED / PASS | [V04](#v04), [V18](#v18) |
| TK1-AUTH-09 | H | CLOSED / PASS | [V04](#v04), [V16](#v16) |
| TK1-AUTH-10 | H | CLOSED / PASS | [V05](#v05) |
| TK1-AUTH-11 | C | CLOSED / PASS | [V05](#v05) |
| TK1-AUTH-12 | C | CLOSED / PASS | [V04](#v04), [V18](#v18) |
| TK1-OCC-01 | C | CLOSED / PASS | [V10](#v10), [V16](#v16), [V20](#v20) |
| TK1-OCC-02 | C | CLOSED / PASS | [V10](#v10), [V09](#v09) |
| TK1-OCC-03 | C | CLOSED / PASS | [V16](#v16) |
| TK1-OCC-04 | C | CLOSED / PASS | [V06](#v06), [V16](#v16) |
| TK1-OCC-05 | C | CLOSED / PASS | [V10](#v10), [V13](#v13), [V14](#v14), [V20](#v20) |
| TK1-IDEM-01 | H | CLOSED / PASS | [V06](#v06) |
| TK1-IDEM-02 | H | CLOSED / PASS | [V06](#v06) |
| TK1-IDEM-03 | C | CLOSED / PASS | [V06](#v06), [V16](#v16) |
| TK1-IDEM-04 | C | CLOSED / PASS | [V06](#v06), [V15](#v15) |
| TK1-IDEM-05 | C | CLOSED / PASS | [V06](#v06) |
| TK1-IDEM-06 | C | CLOSED / PASS | [V06](#v06), [V15](#v15) |
| TK1-IDEM-07 | H | CLOSED / PASS | [V06](#v06) |
| TK1-IDEM-08 | C | CLOSED / PASS | [V06](#v06), [V15](#v15), [V18](#v18) |
| TK1-IDEM-09 | C | CLOSED / PASS | [V16](#v16) |
| TK1-IDEM-10 | C | CLOSED / PASS | [V06](#v06) |
| TK1-IDEM-11 | H | CLOSED / PASS | [V06](#v06) |
| TK1-IDEM-12 | C | CLOSED / PASS | [V06](#v06), [V14](#v14), [V18](#v18) |
| TK1-IDEM-13 | C | CLOSED / PASS | [V15](#v15), [V18](#v18) |
| TK1-IDEM-14 | C | CLOSED / PASS | [V15](#v15), [V20](#v20) |
| TK1-BROWSE-01 | M | CLOSED / PASS | [V07](#v07) |
| TK1-BROWSE-02 | H | CLOSED / PASS | [V07](#v07) |
| TK1-BROWSE-03 | M | CLOSED / PASS | [V07](#v07) |
| TK1-AV-01 | H | CLOSED / PASS | [V08](#v08) |
| TK1-AV-02 | H | CLOSED / PASS | [V08](#v08), [V09](#v09) |
| TK1-AV-03 | M | CLOSED / PASS | [V08](#v08) |
| TK1-AV-04 | H | CLOSED / PASS | [V08](#v08), [V09](#v09) |
| TK1-AV-05 | H | CLOSED / PASS | [V08](#v08), [V09](#v09) |
| TK1-AV-06 | H | CLOSED / PASS | [V08](#v08) |
| TK1-AV-07 | H | CLOSED / PASS | [V08](#v08) |
| TK1-AV-08 | C | CLOSED / PASS | [V08](#v08), [V16](#v16) |
| TK1-AV-09 | H | CLOSED / PASS | [V08](#v08), [V18](#v18) |
| TK1-AV-10 | H | CLOSED / PASS | [V08](#v08) |
| TK1-AV-11 | H | CLOSED / PASS | [V08](#v08) |
| TK1-AV-12 | H | CLOSED / PASS | [V08](#v08), [V09](#v09) |
| TK1-CREATE-01 | H | CLOSED / PASS | [V10](#v10) |
| TK1-CREATE-02 | H | CLOSED / PASS | [V09](#v09), [V10](#v10) |
| TK1-CREATE-03 | H | CLOSED / PASS | [V10](#v10) |
| TK1-CREATE-04 | H | CLOSED / PASS | [V10](#v10) |
| TK1-CREATE-05 | C | CLOSED / PASS | [V10](#v10), [V16](#v16) |
| TK1-CREATE-06 | C | CLOSED / PASS | [V13](#v13), [V14](#v14), [V18](#v18) |
| TK1-CREATE-07 | C | CLOSED / PASS | [V10](#v10), [V16](#v16) |
| TK1-CREATE-08 | H | CLOSED / PASS | [V10](#v10) |
| TK1-CREATE-09 | H | CLOSED / PASS | [V09](#v09), [V10](#v10) |
| TK1-CREATE-10 | H | CLOSED / PASS | [V10](#v10) |
| TK1-CREATE-11 | H | CLOSED / PASS | [V10](#v10) |
| TK1-CREATE-12 | H | CLOSED / PASS | [V10](#v10) |
| TK1-CREATE-13 | H | CLOSED / PASS | [V10](#v10) |
| TK1-GET-01 | C | CLOSED / PASS | [V05](#v05), [V11](#v11) |
| TK1-GET-02 | H | CLOSED / PASS | [V11](#v11), [V13](#v13) |
| TK1-GET-03 | M | CLOSED / PASS | [V11](#v11) |
| TK1-GET-04 | C | CLOSED / PASS | [V05](#v05), [V11](#v11) |
| TK1-GET-05 | H | CLOSED / PASS | [V11](#v11), [V12](#v12) |
| TK1-CANCEL-01 | H | CLOSED / PASS | [V12](#v12) |
| TK1-CANCEL-02 | C | CLOSED / PASS | [V12](#v12), [V16](#v16) |
| TK1-CANCEL-03 | H | CLOSED / PASS | [V12](#v12) |
| TK1-CANCEL-04 | H | CLOSED / PASS | [V12](#v12) |
| TK1-CANCEL-05 | C | CLOSED / PASS | [V05](#v05), [V12](#v12) |
| TK1-PATCH-01 | H | CLOSED / PASS | [V13](#v13) |
| TK1-PATCH-02 | H | CLOSED / PASS | [V13](#v13) |
| TK1-PATCH-03 | H | CLOSED / PASS | [V13](#v13) |
| TK1-PATCH-04 | H | CLOSED / PASS | [V13](#v13) |
| TK1-PATCH-05 | H | CLOSED / PASS | [V13](#v13) |
| TK1-PATCH-06 | C | CLOSED / PASS | [V13](#v13), [V16](#v16) |
| TK1-PATCH-07 | C | CLOSED / PASS | [V13](#v13), [V20](#v20) |
| TK1-PATCH-08 | C | CLOSED / PASS | [V13](#v13), [V18](#v18) |
| TK1-TIME-01 | H | CLOSED / PASS | [V09](#v09) |
| TK1-TIME-02 | H | CLOSED / PASS | [V09](#v09) |
| TK1-TIME-03 | H | CLOSED / PASS | [V09](#v09) |
| TK1-TIME-04 | C | CLOSED / PASS | [V09](#v09) |
| TK1-TIME-05 | C | CLOSED / PASS | [V09](#v09) |
| TK1-TIME-06 | H | CLOSED / PASS | [V09](#v09) |
| TK1-TIME-07 | H | CLOSED / PASS | [V09](#v09) |
| TK1-TIME-08 | H | CLOSED / PASS | [V09](#v09) |
| TK1-TIME-09 | H | CLOSED / PASS | [V09](#v09) |
| TK1-TIME-10 | H | CLOSED / PASS | [V09](#v09) |
| TK1-XFER-01 | H | CLOSED / PASS | [V17](#v17) |
| TK1-XFER-02 | C | CLOSED / PASS | [V17](#v17), [V20](#v20) |
| TK1-XFER-03 | C | CLOSED / PASS | [V17](#v17), [V18](#v18) |
| TK1-XFER-04 | C | CLOSED / PASS | [V18](#v18) |
| TK1-XFER-05 | C | CLOSED / PASS | [V18](#v18) |
| TK1-XFER-06 | C | CLOSED / PASS | [V18](#v18), [V20](#v20) |
| TK1-XFER-07 | C | CLOSED / PASS | [V18](#v18) |
| TK1-XFER-08 | C | CLOSED / PASS | [V18](#v18), [V19](#v19) |
| TK1-XFER-09 | H | CLOSED / PASS | [V19](#v19) |
| TK1-XFER-10 | H | CLOSED / PASS | [V19](#v19) |
| TK1-XFER-11 | C | CLOSED / PASS | [V19](#v19), [V20](#v20) |
| TK1-XFER-12 | C | CLOSED / PASS | [V18](#v18) |
| TK1-XFER-13 | C | CLOSED / PASS | [V18](#v18) |
| TK1-XFER-14 | H | CLOSED / PASS | [V18](#v18) |
| TK1-XFER-15 | C | CLOSED / PASS | [V18](#v18) |
| TK1-XFER-16 | C | CLOSED / PASS | [V18](#v18) |
| TK1-XFER-17 | C | CLOSED / PASS | [V18](#v18) |
| TK1-XFER-18 | C | CLOSED / PASS | [V18](#v18) |
| TK1-XFER-19 | C | CLOSED / PASS | [V18](#v18) |
| TK1-XFER-20 | C | CLOSED / PASS | [V02](#v02), [V18](#v18) |
| TK1-XFER-21 | C | CLOSED / PASS | [V01](#v01), [V18](#v18) |
| TK1-XFER-22 | C | CLOSED / PASS | [V18](#v18) |
| TK1-XFER-23 | C | CLOSED / PASS | [V18](#v18) |
| TK1-MOVE-01 | C | CLOSED / PASS | [V05](#v05), [V14](#v14) |
| TK1-MOVE-02 | C | CLOSED / PASS | [V06](#v06), [V15](#v15) |
| TK1-MOVE-03 | H | CLOSED / PASS | [V14](#v14) |
| TK1-MOVE-04 | C | CLOSED / PASS | [V05](#v05), [V14](#v14) |
| TK1-MOVE-05 | H | CLOSED / PASS | [V14](#v14) |
| TK1-MOVE-06 | H | CLOSED / PASS | [V14](#v14) |
| TK1-MOVE-07 | H | CLOSED / PASS | [V14](#v14), [V15](#v15) |
| TK1-MOVE-08 | C | CLOSED / PASS | [V14](#v14), [V18](#v18) |
| TK1-MOVE-09 | H | CLOSED / PASS | [V14](#v14) |
| TK1-MOVE-10 | H | CLOSED / PASS | [V14](#v14) |
| TK1-MOVE-11 | H | CLOSED / PASS | [V14](#v14) |
| TK1-MOVE-12 | C | CLOSED / PASS | [V14](#v14) |
| TK1-MOVE-13 | C | CLOSED / PASS | [V14](#v14) |
| TK1-MOVE-14 | C | CLOSED / PASS | [V14](#v14) |
| TK1-MOVE-15 | C | CLOSED / PASS | [V14](#v14), [V16](#v16) |
| TK1-MOVE-16 | C | CLOSED / PASS | [V14](#v14) |
| TK1-MOVE-17 | C | CLOSED / PASS | [V14](#v14), [V16](#v16), [V20](#v20) |
| TK1-MOVE-18 | H | CLOSED / PASS | [V14](#v14), [V15](#v15) |
| TK1-MOVE-19 | C | CLOSED / PASS | [V15](#v15), [V18](#v18) |
| TK1-MOVE-20 | C | CLOSED / PASS | [V14](#v14), [V15](#v15), [V18](#v18) |
| TK1-MOVE-21 | C | CLOSED / PASS | [V18](#v18) |
| TK1-MOVE-22 | H | CLOSED / PASS | [V14](#v14), [V15](#v15) |
| TK1-MOVE-23 | H | CLOSED / PASS | [V14](#v14), [V15](#v15) |
| TK1-MOVE-24 | H | CLOSED / PASS | [V14](#v14) |
| TK1-MOVE-25 | H | CLOSED / PASS | [V14](#v14) |
| TK2-WEB-01 | H | CLOSED / PASS | [W01](#w01) |
| TK2-WEB-02 | H | CLOSED / PASS | [W01](#w01) |
| TK2-WEB-03 | H | CLOSED / PASS | [W01](#w01) |
| TK2-WEB-04 | H | CLOSED / PASS | [W01](#w01) |
| TK2-WEB-05 | H | CLOSED / PASS | [W01](#w01), [W02](#w02) |
| TK2-WEB-06 | H | CLOSED / PASS | [W01](#w01), [W17](#w17) |
| TK2-AUI-01 | M | CLOSED / PASS | [W02](#w02) |
| TK2-AUI-02 | M | CLOSED / PASS | [W02](#w02) |
| TK2-AUI-03 | M | CLOSED / PASS | [W02](#w02) |
| TK2-AUI-04 | H | CLOSED / PASS | [W02](#w02) |
| TK2-AUI-05 | M | CLOSED / PASS | [W02](#w02) |
| TK2-AUI-06 | M | CLOSED / PASS | [W02](#w02) |
| TK2-AUI-07 | H | CLOSED / PASS | [W02](#w02) |
| TK2-AUI-08 | H | CLOSED / PASS | [W02](#w02) |
| TK2-AUI-09 | H | CLOSED / PASS | [W02](#w02), [W18](#w18) |
| TK2-AUI-10 | H | CLOSED / PASS | [W02](#w02), [W18](#w18) |
| TK2-AUI-11 | H | CLOSED / PASS | [W02](#w02) |
| TK2-SEARCH-01 | H | CLOSED / PASS | [W03](#w03) |
| TK2-SEARCH-02 | H | CLOSED / PASS | [W03](#w03) |
| TK2-SEARCH-03 | M | CLOSED / PASS | [W03](#w03) |
| TK2-SEARCH-04 | H | CLOSED / PASS | [W03](#w03), [W04](#w04) |
| TK2-SEARCH-05 | M | CLOSED / PASS | [W03](#w03) |
| TK2-SEARCH-06 | H | CLOSED / PASS | [W03](#w03), [W14](#w14) |
| TK2-SEARCH-07 | H | CLOSED / PASS | [W03](#w03), [W14](#w14) |
| TK2-SEARCH-08 | C | CLOSED / PASS | [W03](#w03), [W04](#w04), [W14](#w14) |
| TK2-SEARCH-09 | H | CLOSED / PASS | [W03](#w03), [W05](#w05) |
| TK2-SEARCH-10 | H | CLOSED / PASS | [W03](#w03) |
| TK2-SEARCH-11 | C | CLOSED / PASS | [W02](#w02), [W03](#w03) |
| TK2-SEARCH-12 | H | CLOSED / PASS | [W03](#w03) |
| TK2-RACE-01 | C | CLOSED / PASS | [W04](#w04) |
| TK2-RACE-02 | C | CLOSED / PASS | [W04](#w04) |
| TK2-RACE-03 | C | CLOSED / PASS | [W04](#w04) |
| TK2-RACE-04 | C | CLOSED / PASS | [W04](#w04) |
| TK2-RACE-05 | C | CLOSED / PASS | [W04](#w04) |
| TK2-RACE-06 | H | CLOSED / PASS | [W04](#w04), [W06](#w06) |
| TK2-BOOK-01 | M | CLOSED / PASS | [W05](#w05) |
| TK2-BOOK-02 | H | CLOSED / PASS | [W05](#w05), [W14](#w14) |
| TK2-BOOK-03 | H | CLOSED / PASS | [W05](#w05), [W14](#w14) |
| TK2-BOOK-04 | H | CLOSED / PASS | [W05](#w05), [W04](#w04) |
| TK2-BOOK-05 | C | CLOSED / PASS | [W05](#w05), [W07](#w07) |
| TK2-BOOK-06 | H | CLOSED / PASS | [W05](#w05) |
| TK2-BOOK-07 | C | CLOSED / PASS | [W05](#w05), [W07](#w07) |
| TK2-BOOK-08 | C | CLOSED / PASS | [W05](#w05), [W07](#w07) |
| TK2-BOOK-09 | H | CLOSED / PASS | [W05](#w05) |
| TK2-BOOK-10 | C | CLOSED / PASS | [W05](#w05), [W07](#w07) |
| TK2-CONF-01 | H | CLOSED / PASS | [W05](#w05), [W07](#w07) |
| TK2-CONF-02 | H | CLOSED / PASS | [W05](#w05), [W18](#w18) |
| TK2-CONF-03 | H | CLOSED / PASS | [W05](#w05), [W14](#w14) |
| TK2-CONF-04 | H | CLOSED / PASS | [W05](#w05), [W14](#w14) |
| TK2-CONF-05 | H | CLOSED / PASS | [W14](#w14) |
| TK2-CONFLICT-01 | H | CLOSED / PASS | [W06](#w06) |
| TK2-CONFLICT-02 | H | CLOSED / PASS | [W06](#w06), [W04](#w04) |
| TK2-CONFLICT-03 | C | CLOSED / PASS | [W06](#w06) |
| TK2-CONFLICT-04 | C | CLOSED / PASS | [W06](#w06) |
| TK2-CONFLICT-05 | H | CLOSED / PASS | [W06](#w06) |
| TK2-CONFLICT-06 | C | CLOSED / PASS | [W06](#w06) |
| TK2-UNCERTAIN-01 | C | CLOSED / PASS | [W07](#w07), [W18](#w18) |
| TK2-UNCERTAIN-02 | H | CLOSED / PASS | [W07](#w07) |
| TK2-UNCERTAIN-03 | C | CLOSED / PASS | [W07](#w07) |
| TK2-UNCERTAIN-04 | C | CLOSED / PASS | [W07](#w07), [W18](#w18) |
| TK2-UNCERTAIN-05 | C | CLOSED / PASS | [W07](#w07), [W18](#w18) |
| TK2-UNCERTAIN-06 | H | CLOSED / PASS | [W07](#w07), [W18](#w18) |
| TK2-UNCERTAIN-07 | H | CLOSED / PASS | [W07](#w07), [W18](#w18) |
| TK2-UNCERTAIN-08 | C | CLOSED / PASS | [W07](#w07), [W18](#w18) |
| TK2-UNCERTAIN-09 | H | CLOSED / PASS | [W06](#w06), [W07](#w07) |
| TK2-UNCERTAIN-10 | C | CLOSED / PASS | [W07](#w07), [W18](#w18) |
| TK2-UNCERTAIN-11 | C | CLOSED / PASS | [W06](#w06), [W07](#w07), [W14](#w14), [W18](#w18) |
| TK2-LOOKUP-01 | H | CLOSED / PASS | [W08](#w08), [W18](#w18) |
| TK2-LOOKUP-02 | H | CLOSED / PASS | [W08](#w08) |
| TK2-LOOKUP-03 | H | CLOSED / PASS | [W08](#w08), [W18](#w18) |
| TK2-LOOKUP-04 | H | CLOSED / PASS | [W08](#w08), [W14](#w14) |
| TK2-LOOKUP-05 | H | CLOSED / PASS | [W08](#w08) |
| TK2-LOOKUP-06 | C | CLOSED / PASS | [W08](#w08) |
| TK2-LOOKUP-07 | H | CLOSED / PASS | [W08](#w08) |
| TK2-LOOKUP-08 | H | CLOSED / PASS | [W08](#w08), [W14](#w14), [W18](#w18) |
| TK2-LOOKUP-09 | H | CLOSED / PASS | [W05](#w05), [W08](#w08), [W14](#w14) |
| TK2-QA-01 | H | CLOSED / PASS | [W17](#w17) |
| TK2-QA-02 | M | CLOSED / PASS | [W17](#w17) |
| TK2-QA-03 | H | CLOSED / PASS | [W17](#w17) |
| TK2-QA-04 | M | CLOSED / PASS | [W17](#w17) |
| TK2-QA-05 | H | CLOSED / PASS | [W17](#w17) |
| TK2-QA-06 | H | CLOSED / PASS | [W17](#w17) |
| TK2-QA-07 | H | CLOSED / PASS | [W17](#w17) |
| TK2-QA-08 | H | CLOSED / PASS | [W17](#w17) |
| TK2-QA-09 | H | CLOSED / PASS | [W14](#w14), [W17](#w17) |
| TK2-QA-10 | M | CLOSED / PASS | [W17](#w17) |
| TK2-QA-11 | H | CLOSED / PASS | [W17](#w17) |
| TK2-QA-12 | H | CLOSED / PASS | [W17](#w17) |
| TK2-QA-13 | H | CLOSED / PASS | [W17](#w17) |
| TK2-QA-14 | H | CLOSED / PASS | [W17](#w17) |
| TK2-QA-15 | H | CLOSED / PASS | [W17](#w17) |
| TK2-QA-16 | H | CLOSED / PASS | [W17](#w17) |
| TK2-QA-17 | H | CLOSED / PASS | [W03](#w03), [W17](#w17) |
| TK2-QA-18 | H | CLOSED / PASS | [W04](#w04), [W17](#w17) |
| TK2-QA-19 | H | CLOSED / PASS | [W06](#w06), [W08](#w08), [W17](#w17) |
| TK2-QA-20 | H | CLOSED / PASS | [W01](#w01), [W17](#w17) |
| TK2-PAIR-01 | H | CLOSED / PASS | [W09](#w09) |
| TK2-PAIR-02 | H | CLOSED / PASS | [W09](#w09), [W10](#w10) |
| TK2-PAIR-03 | C | CLOSED / PASS | [W10](#w10) |
| TK2-PAIR-04 | C | CLOSED / PASS | [W09](#w09), [W10](#w10) |
| TK2-PAIR-05 | H | CLOSED / PASS | [W10](#w10), [W12](#w12), [W13](#w13) |
| TK2-PAIR-06 | H | CLOSED / PASS | [W09](#w09), [W10](#w10) |
| TK2-PAIR-07 | C | CLOSED / PASS | [W10](#w10), [W15](#w15), [W16](#w16) |
| TK2-PAIR-08 | C | CLOSED / PASS | [W10](#w10), [W12](#w12), [W13](#w13), [W16](#w16) |
| TK2-PAIR-09 | H | CLOSED / PASS | [W10](#w10), [W12](#w12), [W13](#w13) |
| TK2-PAIR-10 | H | CLOSED / PASS | [W09](#w09) |
| TK2-PAIR-11 | C | CLOSED / PASS | [W09](#w09) |
| TK2-PAIR-12 | H | CLOSED / PASS | [W09](#w09) |
| TK2-SELECT-01 | H | CLOSED / PASS | [W10](#w10) |
| TK2-SELECT-02 | C | CLOSED / PASS | [W10](#w10), [W18](#w18) |
| TK2-SELECT-03 | H | CLOSED / PASS | [W10](#w10), [W12](#w12), [W13](#w13) |
| TK2-SELECT-04 | H | CLOSED / PASS | [W10](#w10), [W12](#w12), [W13](#w13) |
| TK2-SELECT-05 | H | CLOSED / PASS | [W10](#w10), [W12](#w12), [W13](#w13) |
| TK2-SELECT-06 | H | CLOSED / PASS | [W10](#w10), [W12](#w12), [W13](#w13), [W18](#w18) |
| TK2-SELECT-07 | C | CLOSED / PASS | [W10](#w10), [W18](#w18) |
| TK2-SELECT-08 | H | CLOSED / PASS | [W10](#w10), [W12](#w12), [W13](#w13) |
| TK2-SELECT-09 | C | CLOSED / PASS | [W12](#w12) |
| TK2-SELECT-10 | C | CLOSED / PASS | [W12](#w12), [W16](#w16) |
| TK2-SELECT-11 | C | CLOSED / PASS | [W13](#w13) |
| TK2-SELECT-12 | C | CLOSED / PASS | [W13](#w13), [W16](#w16) |
| TK2-SELECT-13 | H | CLOSED / PASS | [W10](#w10), [W12](#w12), [W13](#w13) |
| TK2-SELECT-14 | H | CLOSED / PASS | [W10](#w10), [W12](#w12), [W13](#w13) |
| TK2-OPTIONS-01 | H | CLOSED / PASS | [W11](#w11) |
| TK2-OPTIONS-02 | C | CLOSED / PASS | [W11](#w11), [W18](#w18) |
| TK2-OPTIONS-03 | H | CLOSED / PASS | [W11](#w11) |
| TK2-OPTIONS-04 | H | CLOSED / PASS | [W11](#w11) |
| TK2-OPTIONS-05 | H | CLOSED / PASS | [W11](#w11) |
| TK2-OPTIONS-06 | C | CLOSED / PASS | [W11](#w11), [W16](#w16) |
| TK2-OPTIONS-07 | H | CLOSED / PASS | [W11](#w11), [W18](#w18) |
| TK2-OPTIONS-08 | H | CLOSED / PASS | [W11](#w11), [W18](#w18) |
| TK2-OPTIONS-09 | H | CLOSED / PASS | [W11](#w11), [W14](#w14), [W18](#w18) |
| TK2-PUI-01 | H | CLOSED / PASS | [W14](#w14) |
| TK2-PUI-02 | H | CLOSED / PASS | [W14](#w14) |
| TK2-PUI-03 | C | CLOSED / PASS | [W14](#w14), [W04](#w04) |
| TK2-PUI-04 | H | CLOSED / PASS | [W14](#w14), [W05](#w05) |
| TK2-PUI-05 | H | CLOSED / PASS | [W14](#w14), [W18](#w18) |
| TK2-UP-01 | C | CLOSED / PASS | [W18](#w18) |
| TK2-UP-02 | C | CLOSED / PASS | [W18](#w18) |
| TK2-UP-03 | C | CLOSED / PASS | [W18](#w18) |
| TK2-UP-04 | C | CLOSED / PASS | [W18](#w18) |
| TK2-UP-05 | C | CLOSED / PASS | [W18](#w18) |
| TK2-UP-06 | C | CLOSED / PASS | [W18](#w18) |
| TK2-UP-07 | H | CLOSED / PASS | [W18](#w18) |
| TK2-UP-08 | C | CLOSED / PASS | [W18](#w18) |
| TK2-UP-09 | C | CLOSED / PASS | [W18](#w18) |
| TK2-UP-10 | C | CLOSED / PASS | [W19](#w19) |
| TK2-UP-11 | C | CLOSED / PASS | [W18](#w18) |
| TK2-CC-01 | C | CLOSED / PASS | [W16](#w16), [W19](#w19) |
| TK2-CC-02 | C | CLOSED / PASS | [W16](#w16), [W19](#w19) |
| TK2-GATE-01 | C | CLOSED / PASS | [W20](#w20) |
| TK2-GATE-02 | H | CLOSED / PASS | [W20](#w20) |
