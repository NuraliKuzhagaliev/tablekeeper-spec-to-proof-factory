# Tablekeeper — Spec-to-Proof Autonomous Factory

> A four-stage Tablekeeper submission produced by a five-seat autonomous software factory in BAND Desktop, with independent exact-revision verification and zero human steering after the initial dispatch.

## Submission snapshot

- **Track:** Tablekeeper
- **Completed stages:** **4 / 4**
- **Fresh cumulative official result:** **575 / 575 applicable checks**
- **Exact folder claims:** **1 / 2 / 3 / 4**
- **Highest contiguous stage:** **4**
- **Required populated upgrade paths:** **6 / 6 passed**
- **Unresolved CRITICAL/HIGH product defects:** **0**
- **Additional human input after dispatch:** **NONE**
- **Measured judged-run interval:** **5h 39m 06s**
- **Final accepted Stage 4 production SHA:** `e0caa7221dc63638418768801eed24fc5ed9b7b0`

## Why this submission is different

The factory does not use “visible tests are green” as its acceptance rule.

```text
specification
→ atomic requirements + risk model
→ implementation
→ exact production SHA
→ independent verification
→ ACCEPT / REJECT
→ root-cause repair
→ re-verification
→ compatibility / upgrade proof
→ release
```

A real independent rejection occurred in the judged run: the first Stage 1 production revision was rejected for HIGH-severity specification defects, repaired in a new commit, and accepted only after independent re-verification. The failed revision and repair provenance remain in Git and the BAND room transcript.

## Factory

| Seat | Role |
|---|---|
| **Conductor** | Orchestration, complete handoffs, progression, repair routing, release control |
| **Contract Auditor** | Atomic specification ledger, risk model, traceability, compatibility obligations |
| **Systems Engineer** | Core production semantics, state transitions, concurrency, migrations, implementation tests |
| **Experience Engineer** | Responsive browser UX, accessibility, async-state correctness, product polish |
| **Adversarial Verifier** | Independent exact-SHA verification, oracles, concurrency/upgrades, formal verdicts |

The verifier never repairs production. Production owners never self-accept.

See **[FACTORY.md](FACTORY.md)** for the complete reusable factory design, setup instructions, recovery model, architectural trade-offs, measured time/spend, and evidence strategy.

Generic seat mandates are in **[mandates/](mandates/)**.

## Stage results

| Stage | Accepted production SHA | Official cumulative checks |
|---|---|---:|
| **Stage 1** | `d41a7627711951a07ce7a1718fac47c6ea5b6dd4` | **120 / 120** |
| **Stage 2** | `2c431f7e6c0c5ed3bdae232bde255ec24c1bbab3` | **145 / 145** |
| **Stage 3** | `0ca5880272740494e541a903a49ea423c6e8ce2b` | **152 / 152** |
| **Stage 4** | `e0caa7221dc63638418768801eed24fc5ed9b7b0` | **158 / 158** |

Final fresh all-folder isolated verification: **575 / 575 applicable checks PASS**.

## Product experience

The browser experience is intentionally a real hospitality product rather than a verification dashboard.

Validated areas include:

- 375px mobile and desktop layouts
- keyboard/focus behavior
- readable contrast and no unintended horizontal overflow
- loading / empty / error / uncertain / success states
- stale-response protection
- retained form state after conflicts
- exact lost-response replay behavior
- reservation lookup
- readable reservation history and accepted terms
- locally bundled runtime assets with no CDN dependency

## Meaningful independent review

Initial Stage 1 production:

`b03ce55647b70a46f478ea50ba077e02945bcefe`

was independently **REJECTED** for HIGH-severity product defects.

The failures were reproduced, root causes were repaired, and a new production revision was created:

`d41a7627711951a07ce7a1718fac47c6ea5b6dd4`

Acceptance was not transferred from the rejected revision. The new SHA was independently re-run before Stage 1 received ACCEPT.

This is visible in **[room.json](room.json)** and Git history.

## Upgrade continuity

All required populated paths passed:

- Stage 1 → Stage 2
- Stage 1 → Stage 3
- Stage 2 → Stage 3
- Stage 1 → Stage 4
- Stage 2 → Stage 4
- Stage 3 → Stage 4

## Repository map

```text
.
├── README.md
├── FACTORY.md
├── FINAL_REPORT.md
├── mandates/
├── room.json
├── evidence/
├── stage-1/
├── stage-2/
├── stage-3/
└── stage-4/
```

## Run Stage 4 locally

From `stage-4/`:

```bash
docker build -t tablekeeper-stage-4 .
docker run --rm -e PORT=8080 -p 8080:8080 tablekeeper-stage-4
```

Then open `http://localhost:8080/`.

## Evidence entry points

1. **[FACTORY.md](FACTORY.md)** — factory architecture and judging story
2. **[FINAL_REPORT.md](FINAL_REPORT.md)** — final run metrics, limitations, contributions and accepted SHAs
3. **[evidence/final/official-all-stages.md](evidence/final/official-all-stages.md)** — final fresh cumulative official gate
4. **[evidence/releases/](evidence/releases/)** — stage release provenance
5. **[room.json](room.json)** — autonomous collaboration trace

## Runtime and cost

All five seats used **Codex / gpt-6.1-sol** with high reasoning.

Measured judged-run interval: **5h 39m 06s**.

BAND reported a catalog-equivalent estimate of approximately **USD 38.67** for the judged run. This is a tooling estimate, not claimed provider billing.

## Autonomy

After the initial dispatch, the judged run required:

- no human clarification
- no human approval
- no human debugging
- no implementation hints
- no “continue” messages
- no human-triggered stage reruns

## Final outcome

**4 / 4 stages independently accepted.**  
**575 / 575 applicable fresh cumulative checks passed.**  
**6 / 6 required populated upgrade paths passed.**  
**0 unresolved CRITICAL/HIGH product defects.**  
**0 additional human steering after the initial dispatch.**
