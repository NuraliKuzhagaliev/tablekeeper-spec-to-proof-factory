# Stage 1 release attestation

Conductor advances Stage 1 on the independent verifier's formal ACCEPT, not on owner tests or a self-review.

- Accepted production: `d41a7627711951a07ce7a1718fac47c6ea5b6dd4`.
- Frozen service tree: `7d35fe7568addec4437c2eb8705ed788ed46f0f2` (`stage-1`).
- Independent acceptance evidence: `e4a923e5fda0857e9e28221e92ff0bcfb49641a4`, `evidence/stage-1/verification.md` and the three committed campaign executables.
- Canonical requirements: initial `d2f8b20705cc12cb0f0995f04bdc80f9dcb29a57`; concrete review findings `0cf8748edeaa61438afa7a35e136e48513adb8f7` in the same ledger.
- Production owner: Systems Engineer, handoffs `STAGE1-PRODUCTION-001` and `STAGE1-REPAIR-001`.
- Specification analysis and exact-revision source/HTTP findings: Contract Auditor. Formal acceptance: Adversarial Verifier. Release progression: Conductor.
- Room: `8024d193-cafb-4214-b8d5-913975ac634f`. Initial specification handoff: `7d6930a1-10ef-4190-9d81-38bdbc0e5b5e`; production handoff: `a73f8290-a207-4d0c-96c0-0593d5e9a3d6`; replacement verification release: `f970bfcc-47d2-4470-9be2-b3fd3dc8290c`; formal ACCEPT: `481bbbad-1843-4b57-b64f-20fa258941de`.

Independent isolated official checks passed 120/120. The consolidated independent campaign passed 30 distinct cases over 1,044 observed HTTP requests, traced all 187 requirements (66 CRITICAL, 109 HIGH), detected six controlled oracle variants, and checked coordinated overlaps up to 50 requests. Maximum observed ordinary/control requests were 0.0766821/0.0875098 seconds; readiness was at most 1.982 seconds. These are bounded observations, not guarantees for unbounded data.

The clean read-only Linux-native materialization remained at the exact production revision before and after testing. Offline internal-network execution enforced 2 vCPU and 2 GiB and covered default/custom ports and an actual Docker-assigned published mapping. Separately started source-paused A→B→C transfers verified accounts and hashed login, multiple sessions, identities and timestamps, historical create/batch receipts, failed-key reuse, replacement, rollback, reset, and legacy direct-object snapshots. No reproducible blocking product defect remains.

The initial committed production `b03ce55647b70a46f478ea50ba077e02945bcefe` was independently REJECTED under evidence `f476314d258a8e1955a58c9182d9ab9c009a62df`. Review caught a valid large JSON number being rejected in an ignored field and availability overflowing after its last valid slot on `9999-12-31`. The owner reproduced both, repaired exact JSON representation/portable snapshots and calendar boundaries in a NEW commit, and the verifier independently closed both on the accepted revision. Earlier uncommitted owner checks also caught an unsupported global table-ID uniqueness restriction; that repair and the 114/120→120/120 history are retained in owner provenance.

Architecture uses standard-library threaded HTTP with one transaction lock covering occupancy, reservation records, retry receipts and snapshots. Candidate changes and replacement states validate before publication. Passwords use scrypt; IANA data and all runtime dependencies are bundled. Exact compact numeric representation preserves JSON values without expanding extreme exponents. Ephemeral state is permitted; unbounded dataset performance and unspecified gap-valued business opening boundaries are not established.

Only Stage 1 behavior is released. Its service and acceptance evidence are frozen. Stage 2 must begin with a separate committed copy of the complete accepted tracked service, contain no nested Git repository, and extend only `stage-2`. No additional human input was required. Verifier/runtime recoveries preserved completed evidence and did not trigger product changes; repository evidence contains no raw exports, session values or environment dumps.
