# Spec-to-Proof Factory

## 1. Executive Summary

This submission was produced by a reusable five-seat autonomous software factory running in BAND Desktop with Codex.

The factory is built around a simple principle:

> Passing visible tests is evidence, not proof of specification correctness.

Instead of treating implementation as complete when shipped checks become green, the factory builds a traceable chain:

SPECIFICATION
→ ATOMIC REQUIREMENTS
→ RISK MODEL
→ IMPLEMENTATION
→ EXACT COMMIT SHA
→ INDEPENDENT VERIFICATION
→ ACCEPT / REJECT
→ ROOT-CAUSE REPAIR
→ RE-VERIFICATION
→ COMPATIBILITY / UPGRADE PROOF
→ RELEASE

The judged submission run was executed in a fresh BAND room and a fresh result repository.

After the single initial human dispatch:

- no additional human clarification was provided;
- no human approval was provided;
- no debugging hint was provided;
- no "continue" message was sent;
- no stage was manually rerun by the human;
- no implementation decision was supplied by the human.

The factory autonomously completed all four cumulative Tablekeeper stages.

Final fresh cumulative official result:

- Stage 1: 120 / 120
- Stage 2: 145 / 145
- Stage 3: 152 / 152
- Stage 4: 158 / 158
- Total: 575 / 575 applicable checks
- Highest contiguous stage: 4
- Folder claims: exactly 1 / 2 / 3 / 4

All required populated upgrade paths passed.

No unresolved CRITICAL or HIGH product defect remained.

---

## 2. Why Five Seats?

The factory deliberately separates interpretation, implementation, experience engineering, verification, and release control.

Using multiple coding agents without separation of duties would provide parallelism but weak independence. The five-seat design creates different responsibilities and incentives.

| Seat | Primary responsibility | Explicitly does NOT own |
|---|---|---|
| Conductor | Orchestration, handoffs, progression, repair routing, release control | Production implementation, self-acceptance |
| Contract Auditor | Specification decomposition, risk, traceability, compatibility obligations | Production implementation |
| Systems Engineer | Core production semantics and state transitions | Independent acceptance |
| Experience Engineer | Human-facing/browser experience and interaction correctness | Core domain authority, independent acceptance |
| Adversarial Verifier | Independent exact-revision verification and verdicts | Production repair |

This separation is important because the final run demonstrated that owner checks alone were not sufficient: independent review found a real HIGH-severity Stage 1 defect and forced a production repair before acceptance.

---

## 3. Factory Roster

### Conductor

Owns orchestration and release control.

Responsibilities:

- decomposes work into meaningful work units;
- sends complete self-contained handoffs;
- confirms seat availability;
- controls production/evidence commit windows;
- records exact production revisions;
- routes defects to the responsible production owner;
- distinguishes product, verifier, and infrastructure failures;
- freezes accepted stages;
- controls copy-forward progression;
- prevents redundant evidence work after acceptance.

The Conductor never implements production code and never self-accepts work.

### Contract Auditor

Owns specification analysis, risk modeling, and traceability.

Responsibilities:

- turns specification prose into atomic normative obligations;
- preserves qualifiers, precedence, negative requirements, and invariants;
- classifies CRITICAL / HIGH / MEDIUM / LOW risk;
- tracks concurrency, retry, rollback, temporal, authorization, historical, migration, and no-op requirements;
- identifies likely hidden-test exposure;
- builds cumulative compatibility obligations;
- maintains the canonical Spec-to-Evidence ledger.

### Systems Engineer

Owns core production implementation.

Responsibilities include:

- domain/state transitions;
- transactions and atomicity;
- concurrency control;
- validation and error semantics;
- authentication/authorization;
- retry and replay semantics;
- history/revisions;
- migrations and state transfer;
- deterministic algorithms;
- runtime/build implementation;
- owner-level regression testing.

Every meaningful production result is committed and reported using a full Git SHA.

### Experience Engineer

Owns the human-facing and browser experience.

Responsibilities include:

- route and component architecture;
- responsive interaction;
- browser-state correctness;
- loading / empty / error / uncertain / success states;
- stale-response protection;
- retry continuity;
- accessibility;
- keyboard and focus behavior;
- local/offline runtime assets;
- required browser hooks/selectors;
- presentation quality.

The browser product remains the primary experience; verification/proof surfaces never replace the actual product.

### Adversarial Verifier

Despite the historical seat name, this seat acts as the independent verifier.

Responsibilities include:

- exact-SHA independent verification;
- official harness execution;
- additional black-box specification validation;
- boundary and robustness checks;
- concurrency validation;
- retry/replay verification;
- temporal/historical checks;
- upgrade verification;
- independent reference models;
- metamorphic checks;
- verifier calibration;
- clean-environment reproducibility;
- formal ACCEPT / REJECT verdicts.

The verifier never repairs production code.

---

## 4. Runtime Configuration

All five seats in the judged run used:

- Harness: Codex
- Model: gpt-6.1-sol
- Reasoning effort: high
- Approval policy: never ask
- Tool access: full
- Host OS: Windows 11
- Linux environment: Ubuntu on WSL2
- Containers: Docker Desktop

The submitted services run as containers and require no outbound runtime network access.

---

## 5. How to Stand Up This Factory

The permanent mandates are generic. Another team can reuse the same factory on a different staged software specification.

### Prerequisites

Prepare:

- BAND Desktop;
- Codex runtime;
- Git;
- Docker;
- a clean result repository;
- authoritative task/specification files;
- any task-specific external checker or harness.

### Repository

Create a clean result repository, for example:

```text
<WORKSPACE>/result/
```

Initialize Git and create the first required output directory.

Keep:

- challenge/specification inputs read-only;
- generated result repository separate;
- temporary verification output outside the submission repository when possible.

### Seats

Create five BAND seats corresponding to the roles in `mandates/`:

1. Conductor
2. Contract Auditor
3. Systems Engineer
4. Experience Engineer
5. Adversarial Verifier

Configure each seat with the harness/model declared at the top of its mandate.

All seats should point to the same result repository while maintaining explicit ownership boundaries.

### Room

Create a fresh BAND room.

Add all five seats before the first handoff.

For a judged/autonomous run, use a fresh room and fresh result repository.

### Dispatch

Give the Conductor:

- authoritative specification locations;
- result repository path;
- stage/output structure;
- checker/harness location if applicable;
- autonomy requirement;
- completion target.

After the autonomous run begins, do not supply steering, debugging advice, approvals, or continuation prompts.

### Reuse

No Tablekeeper-specific endpoint, field, error-code, or domain behavior is embedded in the permanent mandates.

To reuse the factory, replace only:

- the authoritative task/specifications;
- result repository;
- task-specific harness/checker inputs;
- initial dispatch.

The factory workflow itself remains unchanged.

---

## 6. Operating Protocol

The normal lifecycle for one work unit is:

```text
             COMPLETE SPECIFICATION
                     |
                     v
             CONTRACT AUDITOR
              requirements/risk
                     |
                     v
                 CONDUCTOR
              ownership routing
              /              \
             v                v
      SYSTEMS ENGINEER   EXPERIENCE ENGINEER
             \                /
              \              /
               committed result
                     |
               FULL COMMIT SHA
                     |
                     v
             INDEPENDENT VERIFIER
                     |
               +-----+-----+
               |           |
             ACCEPT      REJECT
               |           |
               |           v
               |       CONDUCTOR
               |           |
               |      correct owner
               |           |
               |      root-cause fix
               |           |
               |        NEW SHA
               |           |
               +------ re-verify
```

No seat may accept its own production work.

---

## 7. Acceptance State Machine

Each stage moves through the following states:

```text
PLANNED
  ↓
CONTRACTED
  ↓
IMPLEMENTING
  ↓
COMMITTED
  ↓
PRODUCTION_FROZEN
  ↓
INDEPENDENT_VERIFICATION
  ↓
 ┌─────────────────────────┐
 │                         │
REJECTED                 ACCEPTED
 │                         │
 v                         v
REPAIRING               EVIDENCE_FROZEN
 │                         │
NEW_SHA                    v
 │                    COPY_FORWARD
 └────→ RE-VERIFY           │
                            v
                         NEXT_STAGE
```

A new evidence commit never silently becomes the production revision being tested.

Acceptance always names the exact production SHA.

---

## 8. Spec-to-Evidence Graph

The Contract Auditor maintained cumulative requirement ledgers connecting normative requirements to risk and verification evidence.

Final cumulative obligation counts:

| Stage | Cumulative obligations |
|---|---:|
| Stage 1 | 187 |
| Stage 2 | 338 |
| Stage 3 | 557 |
| Stage 4 | 730 |

Final risk scope included:

- 382 CRITICAL obligations
- 325 HIGH obligations
- remaining MEDIUM obligations

The purpose of the graph is not bureaucracy.

It prevents these common failure modes:

- a visible test passes while an untested normative clause is ignored;
- a requirement interaction is lost between stages;
- compatibility is assumed instead of demonstrated;
- an accepted result lacks independent evidence;
- later configuration is incorrectly projected onto historical state.

---

## 9. Exact-Revision Verification

The factory uses exact committed revisions as verification boundaries.

The process is:

1. production owner completes coherent work;
2. owner commits;
3. owner reports FULL SHA;
4. production is frozen;
5. verifier receives that exact SHA;
6. verifier operates against immutable materialized content;
7. verifier issues a verdict naming that SHA;
8. evidence-only commits remain separate.

This gives a traceable chain:

```text
Room handoff
→ owner
→ production SHA
→ independent execution
→ evidence
→ verdict
```

The verifier avoids intentionally accepting mutable shared `HEAD`.

Cross-platform linked worktree behavior was also treated carefully after earlier rehearsal evidence showed that Windows/WSL Git pointers could create misleading verification state.

---

## 10. Meaningful Review: Real REJECT → Repair

The final judged run contains a genuine independent rejection.

Initial Stage 1 production:

```text
b03ce55647b70a46f478ea50ba077e02945bcefe
```

was independently REJECTED for HIGH-severity product defects.

The independent campaign reproduced:

- valid ignored numeric JSON becoming malformed instead of being ignored;
- availability overflow at the final supported calendar boundary.

The defects were reproduced before repair.

Systems Engineer then created a distinct repaired production revision:

```text
d41a7627711951a07ce7a1718fac47c6ea5b6dd4
```

The verifier did not transfer acceptance from the old SHA.

The new revision was independently re-executed and accepted only after the failing scenarios and interacting regressions were closed.

This was not manufactured conflict. Independent verification materially changed production.

Earlier owner checks also exposed an unsupported assumption of globally unique table IDs, which was repaired without rewriting the collaboration history.

---

## 11. Failure Classification and Recovery

The factory distinguishes four failure classes:

| Failure class | Meaning | Production changed? |
|---|---|---|
| PRODUCT DEFECT | Specification violation in production | Yes, by production owner |
| VERIFIER DEFECT | Incorrect verifier logic/fixture/oracle | No |
| INFRASTRUCTURE DEFECT | Docker/Git/network/runtime/tooling failure | No |
| INCONCLUSIVE | Insufficient evidence to classify | Not until classified |

### Recovery policy

For infrastructure/verifier failures:

- preserve the exact production SHA;
- preserve valid completed evidence;
- repair the verifier/runtime environment;
- resume from the last proven checkpoint;
- do not modify production merely to make verification infrastructure happy.

The development process autonomously recovered from issues including:

- runtime process exits;
- Docker registry/network failures;
- credential-helper problems;
- host-port behavior;
- verifier fixture/model mistakes;
- cleanup/observer races;
- transient handoff-rendering problems.

No human debugging was required during the judged run.

---

## 12. Concurrency and Atomicity

Concurrency was treated as a semantic property.

Independent campaigns used coordinated overlapping operations and inspected:

- invocation order;
- responses;
- resulting state;
- preserved invariants;
- compatibility with permitted serial outcomes.

Campaigns reached the required 50 simultaneous operations.

A successful concurrency check required more than "no server error": the resulting state and responses had to satisfy the specification's permitted execution model.

---

## 13. Independent Models and Metamorphic Checks

Where deterministic behavior was high-risk and bounded, verification used independently derived models instead of reusing production decision logic.

Examples included independent models for:

- exact numeric/member semantics;
- typed JSON behavior;
- effective policy behavior;
- recurring behavior;
- bounded deterministic optimization.

Metamorphic checks were used when the specification established semantic equivalence.

Verifier calibration used controlled incorrect variants to demonstrate that important classes of implementation mistakes could actually be detected.

---

## 14. Upgrade Continuity Matrix

Cross-stage state continuity was treated as a first-class verification surface.

All six populated required upgrade paths passed:

| Source | Destination | Result |
|---|---|---|
| Stage 1 | Stage 2 | PASS |
| Stage 1 | Stage 3 | PASS |
| Stage 2 | Stage 3 | PASS |
| Stage 1 | Stage 4 | PASS |
| Stage 2 | Stage 4 | PASS |
| Stage 3 | Stage 4 | PASS |

The campaigns verified required continuity of relevant:

- sessions/login;
- identities/references;
- reservation state;
- original retry receipts;
- policies;
- histories;
- revisions;
- recurring agreements;
- moved/cancelled/excluded members;
- accepted historical terms;
- schedules;
- later operations on imported state.

Upgrade success was therefore based on populated state, not merely empty-state import.

---

## 15. Product Experience

The browser product uses a warm hospitality visual direction with locally bundled runtime assets.

Experience validation covered:

- mobile layout at 375 CSS pixels;
- conventional desktop layout;
- keyboard use;
- visible focus;
- contrast;
- absence of unintended horizontal overflow;
- human-readable table/seating labels;
- loading states;
- empty states;
- confirmed failure states;
- uncertain outcome states;
- successful confirmation states;
- stale-response protection;
- form retention after conflicts;
- exact retry behavior after uncertain/lost responses;
- required browser routes and hooks.

The final Stage 4 experience campaign included 28 browser groups and 21 contrast pairs with no reported runtime errors.

Optional work was deliberately bounded.

The factory completed useful differentiators around:

- readable reservation provenance;
- accepted terms;
- reassigned seating history;
- separation between current seating and immutable original receipts.

A large manager dashboard was intentionally omitted because the expected judging value did not justify additional privacy/scope/failure surface.

---

## 16. Architecture Decisions

The final implementation uses a deliberately conservative architecture:

- Python standard-library threaded HTTP;
- one transaction lock protecting coherent state transitions;
- explicit modules for domain behavior, policies, history, import/state transfer, and scheduling;
- scrypt password hashing;
- bundled IANA time-zone support;
- local runtime assets;
- no outbound runtime dependency.

### Why a coarse transaction lock?

The specified concurrency bound is modest.

A coarse lock made atomic multi-record transitions easier to reason about, audit, and independently model.

The alternative — fine-grained locking — could improve theoretical throughput but would significantly increase deadlock, ordering, and partial-state risk for little judging value under the specified workload.

### Why an embedded/in-process state model?

Durable cross-restart persistence was not required.

Keeping the deployment self-contained reduced:

- operational dependencies;
- network failure surface;
- setup complexity;
- external-service assumptions.

### Why exact deterministic search for bounded planning?

The planning input is explicitly bounded.

The implementation therefore uses exact deterministic optimization with admissible pruning rather than a heuristic approximation.

This preserves the specification's full lexicographic optimum:

1. moved count;
2. unused capacity;
3. deterministic rank vector.

Independent bounded models were used to validate the result.

### Why not a more complex distributed architecture?

The objective was specification correctness and autonomous verification, not infrastructure novelty.

Unnecessary services would have increased:

- deployment risk;
- synchronization complexity;
- runtime networking assumptions;
- verification surface.

---

## 17. Stage Results

Accepted production revisions:

### Stage 1

```text
d41a7627711951a07ce7a1718fac47c6ea5b6dd4
```

Official cumulative result:

```text
120 / 120
```

### Stage 2

```text
2c431f7e6c0c5ed3bdae232bde255ec24c1bbab3
```

Official cumulative result:

```text
145 / 145
```

### Stage 3

```text
0ca5880272740494e541a903a49ea423c6e8ce2b
```

Official cumulative result:

```text
152 / 152
```

### Stage 4

```text
e0caa7221dc63638418768801eed24fc5ed9b7b0
```

Official cumulative result:

```text
158 / 158
```

### Final fresh cumulative verification

```text
575 / 575 applicable checks PASS
highest contiguous stage: 4
folder claims: 1 / 2 / 3 / 4
```

The final official all-folder isolated process completed in approximately:

```text
227.265 seconds
```

Additional standalone execution checks covered default port, offline runtime, and independently assigned host ports.

---

## 18. Evidence Layout

The result repository contains stage-specific and final evidence.

Important evidence categories include:

```text
evidence/
  stage-1/
  stage-2/
  stage-3/
  stage-4/
  releases/
  final/
```

Representative evidence includes:

- canonical requirement ledgers;
- risk analysis;
- production SHA references;
- independent verification reports;
- formal verdicts;
- upgrade results;
- independent models;
- concurrency campaigns;
- release attestations;
- final cumulative harness evidence.

Large raw diagnostics not appropriate for a public submission were kept outside the result repository.

---

## 19. Evidence Safety

Evidence safety is an explicit release gate.

The repository was checked for credential-shaped content and unwanted environment material.

The final audit found no real:

- API keys;
- access tokens;
- passwords;
- secrets;
- credential-bearing URLs;
- raw private state exports containing live session values;
- raw environment dumps.

Synthetic fixtures required by tests remain where appropriate.

Submission evidence contains sanitized summaries rather than arbitrary runtime-environment captures.

---

## 20. Efficiency Evolution

Earlier rehearsals showed that high-quality multi-agent verification can become inefficient if every assertion creates:

- a new conversational task;
- another snapshot;
- another graph comparison;
- another evidence binding;
- another post-acceptance reconciliation.

The final factory introduced an Evidence Freeze discipline:

- one canonical requirements ledger per stage;
- coarse meaningful implementation tasks;
- batched verification campaigns;
- one formal verdict per production revision;
- one release attestation;
- immediate progression after required obligations close.

Supplemental evidence is justified only when it:

- closes a concrete CRITICAL/HIGH gap;
- investigates a reproducible defect;
- verifies a new production revision;
- satisfies a required compatibility gate;
- resolves a real blocker.

This preserved verification depth while reducing unnecessary communication and model consumption.

---

## 21. Measured Time and Model Spend

Measured final task-to-report interval:

```text
5h 39m 06s
```

Recorded first-to-final task timestamps:

```text
14:44:58 UTC → 20:24:04 UTC
```

Observed BAND attribution:

```text
5 Codex sessions
model: gpt-6.1-sol
catalog-estimated equivalent spend: ~USD 38.67
```

The spend value is the tooling's catalog-equivalent estimate.

It is NOT claimed to be confirmed provider billing.

The factory intentionally spent substantial compute on independent verification because hidden-test resistance and meaningful review were explicit design goals.

---

## 22. Judged-Run Autonomy

The final room began from one human dispatch.

After that dispatch:

- no implementation hint was supplied;
- no repair instruction was supplied;
- no permission prompt was answered;
- no debugging help was supplied;
- no "continue" message was sent;
- no human stage rerun was requested.

The seats resolved implementation choices, specification questions, verification failures, runtime failures, and repairs autonomously.

Additional human input required:

```text
NONE
```

---

## 23. Reusing the Factory on Another Problem

A new team can reuse this factory as follows:

1. Copy the five generic mandates.
2. Create five corresponding BAND seats.
3. Configure each seat with the declared harness/model.
4. Point all seats at a clean result repository.
5. Prepare the authoritative specifications and task-specific checker.
6. Create a fresh room.
7. Add every seat.
8. Dispatch the task to the Conductor.
9. Do not steer the autonomous run.
10. Inspect the resulting Git/evidence/room provenance.

No domain-specific Tablekeeper behavior is required in the mandates.

The expected generic workflow is:

```text
specification
→ requirements/risk model
→ implementation
→ exact-SHA independent verification
→ ACCEPT / REJECT
→ repair if required
→ compatibility proof
→ release
```

---

## 24. Known Limitations

The factory does not claim mathematical proof of arbitrary software correctness.

Known limits:

- shipped checks are preview coverage and hidden judging tests are unavailable;
- finite verification campaigns cannot prove unlimited workloads;
- some runtime state is intentionally ephemeral where permitted;
- arbitrarily large exact outputs eventually encounter finite compute/resource budgets;
- behavior not defined by the authoritative specification is not claimed;
- optional product surfaces were deliberately bounded to protect correctness and scope.

These limitations are stated rather than hidden.

---

## 25. Final Outcome

All four cumulative stages were independently ACCEPTED.

Final accepted production revision:

```text
e0caa7221dc63638418768801eed24fc5ed9b7b0
```

Fresh final cumulative official result:

```text
575 / 575 applicable checks PASS
```

All required populated upgrade paths passed.

No unresolved CRITICAL/HIGH product defect remained.

No unresolved blocker remained.

Additional human input after initial dispatch:

```text
NONE
```

The result demonstrates not only a completed application, but a reusable autonomous process capable of detecting bad work, repairing it, independently re-verifying it, preserving provenance, and advancing through cumulative software evolution without human steering.
