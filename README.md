# Tablekeeper — Spec-to-Proof Autonomous Factory

> A four-stage Tablekeeper submission produced by a five-seat autonomous software factory in BAND Desktop, with independent exact-revision verification and zero human steering after the initial dispatch.

## Live demo

**Public Stage 4 demo:**  
https://tablekeeper-spec-to-proof-factory.onrender.com

**Demo account**

```text
Email: demo@example.com
Password: password123
```

The demo runs the same Stage 4 service as the submission. It uses the specification's intentionally ephemeral in-memory state.

> **Render Free may restart/sleep the service.** If the restaurant list is empty after a restart, use the PowerShell seed block in [Seed the demo](#seed-the-demo). The judged repository itself does not depend on Render or any external state service.

Quick health check:

```text
https://tablekeeper-spec-to-proof-factory.onrender.com/health
```

---

## Choose how you want to evaluate it

### Option A — Open the live demo

1. Open https://tablekeeper-spec-to-proof-factory.onrender.com
2. If restaurants are visible, use the demo normally.
3. Sign in with:
   - `demo@example.com`
   - `password123`
4. Search availability, choose a table, book it, and open **Your reservation**.
5. If the restaurant list is empty because the free Render instance restarted, run the seed block below once and refresh.

### Option B — Run the accepted Stage 4 service locally with Docker

```bash
git clone https://github.com/NuraliKuzhagaliev/tablekeeper-spec-to-proof-factory.git
cd tablekeeper-spec-to-proof-factory/stage-4

docker build -t tablekeeper-stage-4 .
docker run --rm -e PORT=8080 -p 8080:8080 tablekeeper-stage-4
```

Then open:

```text
http://localhost:8080/
```

Health:

```text
http://localhost:8080/health
```

To populate the local instance with the same demo catalogue, use the PowerShell seed block below and set:

```powershell
$BaseUrl = "http://localhost:8080"
```

### Option C — Inspect the full judged submission and factory evidence

Start with:

1. [FACTORY.md](FACTORY.md) — reusable factory architecture, setup, design choices, cost/time, failure handling
2. [FINAL_REPORT.md](FINAL_REPORT.md) — judged-run completion report and accepted SHAs
3. [evidence/final/official-all-stages.md](evidence/final/official-all-stages.md) — fresh final cumulative official gate
4. [evidence/releases/](evidence/releases/) — release provenance
5. [room.json](room.json) — full BAND room transcript for the submitted run
6. Git history — implementation, rejection, repair, verification and release provenance

---

## Seed the demo

The following PowerShell block replaces the current runtime state with a presentation-ready catalogue of six restaurants.

It is safe to rerun. `/_test/reset` is part of the required Tablekeeper test/runtime contract and atomically replaces the in-memory state.

For the hosted Render demo:

```powershell
$BaseUrl = "https://tablekeeper-spec-to-proof-factory.onrender.com"
```

For a local Docker instance:

```powershell
$BaseUrl = "http://localhost:8080"
```

Then run:

```powershell
$body = @{
  users = @(
    @{
      id = "u_demo"
      email = "demo@example.com"
      password = "password123"
      display_name = "Demo Guest"
    }
  )

  restaurants = @(

    @{
      id = "r_aurelia"
      name = "Maison Aurelia"
      timezone = "Europe/Berlin"
      slot_minutes = 30
      reservation_duration_minutes = 90
      cancellation_cutoff_minutes = 120
      opening_hours = @(
        @{ weekday="mon"; opens="17:00"; closes="23:00" },
        @{ weekday="tue"; opens="17:00"; closes="23:00" },
        @{ weekday="wed"; opens="17:00"; closes="23:00" },
        @{ weekday="thu"; opens="17:00"; closes="23:00" },
        @{ weekday="fri"; opens="17:00"; closes="23:30" },
        @{ weekday="sat"; opens="17:00"; closes="23:30" },
        @{ weekday="sun"; opens="17:00"; closes="22:00" }
      )
      tables = @(
        @{ id="a1"; label="Window for two"; capacity=2 },
        @{ id="a2"; label="Garden table"; capacity=4 },
        @{ id="a3"; label="Family table"; capacity=6 }
      )
    },

    @{
      id = "r_osteria"
      name = "Osteria Verde"
      timezone = "Europe/Rome"
      slot_minutes = 30
      reservation_duration_minutes = 120
      cancellation_cutoff_minutes = 180
      opening_hours = @(
        @{ weekday="mon"; opens="18:00"; closes="23:00" },
        @{ weekday="tue"; opens="18:00"; closes="23:00" },
        @{ weekday="wed"; opens="18:00"; closes="23:00" },
        @{ weekday="thu"; opens="18:00"; closes="23:30" },
        @{ weekday="fri"; opens="18:00"; closes="23:30" },
        @{ weekday="sat"; opens="17:30"; closes="23:30" },
        @{ weekday="sun"; opens="17:30"; closes="22:30" }
      )
      tables = @(
        @{ id="o1"; label="Candlelit table"; capacity=2 },
        @{ id="o2"; label="Courtyard table"; capacity=4 },
        @{ id="o3"; label="Long family table"; capacity=8 }
      )
    },

    @{
      id = "r_lumiere"
      name = "Atelier Lumiere"
      timezone = "Europe/Paris"
      slot_minutes = 30
      reservation_duration_minutes = 90
      cancellation_cutoff_minutes = 240
      opening_hours = @(
        @{ weekday="mon"; opens="18:30"; closes="22:30" },
        @{ weekday="tue"; opens="18:30"; closes="22:30" },
        @{ weekday="wed"; opens="18:30"; closes="22:30" },
        @{ weekday="thu"; opens="18:30"; closes="23:00" },
        @{ weekday="fri"; opens="18:30"; closes="23:00" },
        @{ weekday="sat"; opens="18:00"; closes="23:00" },
        @{ weekday="sun"; opens="18:00"; closes="22:00" }
      )
      tables = @(
        @{ id="l1"; label="Salon table"; capacity=2 },
        @{ id="l2"; label="Terrace table"; capacity=4 },
        @{ id="l3"; label="Chef's room"; capacity=6 }
      )
    },

    @{
      id = "r_sakura"
      name = "Sakura House"
      timezone = "Asia/Tokyo"
      slot_minutes = 30
      reservation_duration_minutes = 90
      cancellation_cutoff_minutes = 120
      opening_hours = @(
        @{ weekday="mon"; opens="17:30"; closes="22:30" },
        @{ weekday="tue"; opens="17:30"; closes="22:30" },
        @{ weekday="wed"; opens="17:30"; closes="22:30" },
        @{ weekday="thu"; opens="17:30"; closes="22:30" },
        @{ weekday="fri"; opens="17:30"; closes="23:00" },
        @{ weekday="sat"; opens="17:00"; closes="23:00" },
        @{ weekday="sun"; opens="17:00"; closes="22:00" }
      )
      tables = @(
        @{ id="s1"; label="Tatami for two"; capacity=2 },
        @{ id="s2"; label="Garden booth"; capacity=4 },
        @{ id="s3"; label="Private room"; capacity=6 }
      )
    },

    @{
      id = "r_ember"
      name = "Ember & Oak"
      timezone = "Europe/London"
      slot_minutes = 30
      reservation_duration_minutes = 120
      cancellation_cutoff_minutes = 120
      opening_hours = @(
        @{ weekday="mon"; opens="17:00"; closes="23:00" },
        @{ weekday="tue"; opens="17:00"; closes="23:00" },
        @{ weekday="wed"; opens="17:00"; closes="23:00" },
        @{ weekday="thu"; opens="17:00"; closes="23:00" },
        @{ weekday="fri"; opens="17:00"; closes="23:30" },
        @{ weekday="sat"; opens="16:30"; closes="23:30" },
        @{ weekday="sun"; opens="16:30"; closes="22:00" }
      )
      tables = @(
        @{ id="e1"; label="Fireplace table"; capacity=2 },
        @{ id="e2"; label="Oak booth"; capacity=4 },
        @{ id="e3"; label="Feasting table"; capacity=8 }
      )
    },

    @{
      id = "r_nocturne"
      name = "Nocturne Dining"
      timezone = "America/New_York"
      slot_minutes = 30
      reservation_duration_minutes = 90
      cancellation_cutoff_minutes = 180
      opening_hours = @(
        @{ weekday="mon"; opens="17:30"; closes="23:00" },
        @{ weekday="tue"; opens="17:30"; closes="23:00" },
        @{ weekday="wed"; opens="17:30"; closes="23:00" },
        @{ weekday="thu"; opens="17:30"; closes="23:30" },
        @{ weekday="fri"; opens="17:30"; closes="23:30" },
        @{ weekday="sat"; opens="17:00"; closes="23:30" },
        @{ weekday="sun"; opens="17:00"; closes="22:30" }
      )
      tables = @(
        @{ id="n1"; label="Velvet table"; capacity=2 },
        @{ id="n2"; label="Library booth"; capacity=4 },
        @{ id="n3"; label="Private dining room"; capacity=10 }
      )
    }
  )

  reservations = @()
} | ConvertTo-Json -Depth 12

Invoke-RestMethod `
  -Uri "$BaseUrl/_test/reset" `
  -Method Post `
  -ContentType "application/json" `
  -Body $body

Write-Host "Demo seeded. Open: $BaseUrl"
Write-Host "Login: demo@example.com / password123"
```

Expected restaurant catalogue:

- Maison Aurelia
- Osteria Verde
- Atelier Lumiere
- Sakura House
- Ember & Oak
- Nocturne Dining

---

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
