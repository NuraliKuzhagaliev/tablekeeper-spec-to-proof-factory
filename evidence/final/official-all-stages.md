# Final all-folder official release gate

FINAL GATE: PASS

TESTED PRODUCTION REVISION: `e0caa7221dc63638418768801eed24fc5ed9b7b0`

This separately required release gate tests the complete four-folder submitted snapshot. It preserves the earlier independent ACCEPT verdicts and their evidence; it does not repeat their robustness campaigns or transfer acceptance to another production revision.

The complete official `--all` command exited 0. All **575/575 applicable checks** passed across four standalone builds. Every folder claims exactly its intended stage, and the complete submission's highest contiguous stage is **4**. There are no applicable failures, errors, skips, deselections or expected failures. Later-stage overshoot probes correctly prevent earlier folders from claiming a later answer; their expected negative results are excluded from the 575 applicable checks.

```sh
cd /mnt/d/dark/dark-factory-wearedevs
~/.venvs/dark-factory/bin/python -m harness run --track tablekeeper --repo /tmp/av-stage4-e0caa7221dc6-9482c6f9-83_bepl8/candidate --all --mode isolated --out /mnt/d/dark/band-work/checks/av-final-e0caa7221dc6-f40036ea/official
```

Official checkout: `803560d2a678ace1414465c098eb0ab5380ffade`. It was read-only throughout. Its Windows checkout reports EOL-only differences under Linux; `git diff --ignore-space-at-eol` is empty, and before/after status and SHA are identical. No specification, test, harness or production edit was made. The harness labels submission provenance `working-tree`; that working tree is the clean detached, Linux-native immutable production pin named above.

| Standalone folder | Applicable cumulative checks | Claimed stage | Highest contiguous | Official elapsed seconds |
|---|---|---|---|---|
| stage-1 | 120 = 120 | 1 | 1 | 43.379 |
| stage-2 | 120 + 25 = 145 | 2 | 2 | 55.618 |
| stage-3 | 120 + 25 + 7 = 152 | 3 | 3 | 60.266 |
| stage-4 | 120 + 25 + 7 + 6 = 158 | 4 | 4 | 61.116 |

Whole official process elapsed: **227.265s**, including all builds, readiness, upgrade sources and overshoot probes. Resource preflight: Docker 29.8.0, 20 host CPUs, 8125067264 bytes. These are configured limits and finite observations, not peak-resource or unlimited-throughput measurements.

## Exact binding and official outputs

External diagnostics root: `/mnt/d/dark/band-work/checks/av-final-e0caa7221dc6-f40036ea`. Raw logs remain outside Result. The complete official summary is `official/summary.json`; each folder has `official/stage-N/report.json`, per-suite count files and logs. Report revisions all equal the FULL tested production SHA. The summary's contiguous stage chain is four claimed folders. Official adjacent upgrade sources are the preserved folders inside the same clean pin, rather than a mutable shared checkout.

| Folder | Suite SHA256 | Report SHA256 |
|---|---|---|
| stage-1 | `c4272f6e544cb878ece8469c1eab3b477216701f92f0a5d1111e5e591e67bd09` | `03b37c2afcccaa1827d37aabceff710acddf7afa669a17b469d7d26c7a8d6f8e` |
| stage-2 | `f98962753222bf04eae211beb9e8bf8b9f3edd062beeb55ae857391365a6fb83` | `f58b4282d154316aee4ee06494395390a3888810b87beb2bcee03339241353fc` |
| stage-3 | `2f27c2abe7e225758da8e656d354896e527953af8cd7ea3cbb9e3d336ac211c2` | `023ea25f8911831c638aa3179f3c469baed21a61c2573e79ed1fd86677a04680` |
| stage-4 | `5dc29292a2c9b4b9f8c70601a485a154d3cafa9c0d5b02fb04e8b2adf77f8047` | `4d15060b703d0eb99afd915977024779e1317a7e1d22d98c6c68525233c57eff` |

Complete summary SHA256: `52db9c9389398bf981718a0076f115424bfb831edaef7b281ef807b1bf801235`. Observer metadata SHA256: `7d265bfac41678351037711fe50c04a25b8efe2c90b2df952d6ff2205e9c5e04`. Standalone runtime summary SHA256: `d7232c44813a20213ca1773ce9019c22288363494f274bf18811fe61c0419f07`.

| Preserved production folder | Accepted FULL production SHA | Matching Git tree |
|---|---|---|
| Stage1 | `d41a7627711951a07ce7a1718fac47c6ea5b6dd4` | `7d35fe7568addec4437c2eb8705ed788ed46f0f2` |
| Stage2 | `2c431f7e6c0c5ed3bdae232bde255ec24c1bbab3` | `5e0f3ee38f68f7cb846b28c5dbd1850e7b768f91` |
| Stage3 | `0ca5880272740494e541a903a49ea423c6e8ce2b` | `6db40e3e5b32431d5cb976f67b8be33c633da6ae` |
| Stage4 | `e0caa7221dc63638418768801eed24fc5ed9b7b0` | `181bcef3172bf41c2feba3195e628c5d145c81de` |

All four trees match before and after execution and the current submitted production folders. The pin remains clean. There are no nested stage Git repositories or cross-platform linked worktrees. All 56 tracked files under the four stage acceptance-evidence directories remain equal to acceptance checkpoint `aeb7291fc48aa03c052b6615ae8626c961ce5c4c`, allowing only checkout EOL conversion. Evidence-only release attestations do not change tested production identity.

## Standalone runtime and assets

The official service and upgrade-source containers were observed with 2 vCPU / 2147483648-byte limits on unique internal networks, with explicit PORT=8080. Every official build started independently and passed health readiness under the actual 60s allowance. Official clients use 5s ordinary and 10s control request budgets. Source initialization and all required dependencies worked with no runtime outbound network.

An additional minimal runtime audit built every pinned folder separately. Each passed with PORT omitted (default 8080) on a unique internal network. Stages 2–4 returned the required HTML routes and bundled JavaScript/CSS from the image. Each also passed a custom-port publication probe using a native Windows client and Docker's actual assigned mapping. Published probes establish host reachability; offline operation is established by the separate internal-network probes and official runs.

| Folder | Offline default readiness/assets seconds | Custom internal port | Actual host mapping | Published readiness seconds |
|---|---|---|---|---|
| stage-1 | 1.154 | 8991 | `127.0.0.1:53409` | 0.966 |
| stage-2 | 1.059 | 8992 | `127.0.0.1:53415` | 0.746 |
| stage-3 | 1.093 | 8993 | `127.0.0.1:53421` | 0.733 |
| stage-4 | 1.098 | 8994 | `127.0.0.1:55859` | 0.735 |

All eight minimal probes used 2 vCPU / 2 GiB and passed. The readiness/assets times include client-process startup and, where applicable, packaged-route checks. The official isolated browser suites additionally exercise the required interfaces. Owned probe containers/images/network and official service/source containers were cleaned. No unrelated resource was removed.

## Required upgrade path matrix

Existing exact-revision independent reports and passing checkpoints were inspected rather than duplicating completed compatibility campaigns. Each path includes genuinely populated source state, retained credentials/sessions/references/status/timestamps and exact original create/batch receipts. Direct Stage3→4 additionally retains policies, terms, histories, adopted/edited/cancelled agreement members and original schedules. Same-tab between-request pending lost-response identity is documented at each destination, using genuine old sessions and no reload. Destination replacement, source pause, failed import rollback and retry continuity are documented in the linked accepted campaigns.

| Required path | Accepted destination evidence | Passing independent case |
|---|---|---|
| Stage1→2 | [Stage2 report](../stage-2/verification.md) | `stage1_upgrade_receipts`, `same_tab_upgrade` |
| Stage1→3 | [Stage3 report](../stage-3/verification.md), [coverage](../stage-3/coverage.json) | `legacy_direct_upgrades`, source_stage1 same-tab variant |
| Stage2→3 | [Stage3 report](../stage-3/verification.md), [coverage](../stage-3/coverage.json) | `legacy_direct_upgrades`, source_stage2 same-tab variant |
| Stage1→4 | [Stage4 report](../stage-4/verification.md), [coverage](../stage-4/coverage.json) | `direct_legacy_populated_transfers`, browser1 `same_tab_upgrade` |
| Stage2→4 | [Stage4 report](../stage-4/verification.md), [coverage](../stage-4/coverage.json) | `direct_legacy_populated_transfers`, browser2 `same_tab_upgrade` |
| Stage3→4 | [Stage4 report](../stage-4/verification.md), [coverage](../stage-4/coverage.json) | `direct_legacy_populated_transfers`, browser3 `same_tab_upgrade` |

The new official all-folder run repeats applicable lower upgrades in cumulative suites. Direct nonadjacent populated paths rely on the frozen independent checkpoints above, whose source/destination trees match this snapshot. This is an explicit reuse of completed evidence, not a claim that the official adjacent upgrades exercise every direct path.

Inspected API summary identities:

- `/mnt/d/dark/band-work/checks/av-stage2-2c431f7e6c0c-91b7e86e/pairs-summary.json` — SHA256`c3f90b11dc8f0ed7279e736c0d6eea08c53fff5f66f6862c15b0cbe8a68766d2`.
- `/mnt/d/dark/band-work/checks/av-stage3-0ca588027274-f854babf/core-summary.json` — SHA256`3fa951f7bf071febc2fbc575b09d7f57ee1c498404fec5d476d093a9701ec14a`.
- `/mnt/d/dark/band-work/checks/av-stage4-e0caa7221dc6-5c6af200/extra4-summary.json` — SHA256`422701369bef1f6afc1a11bd16377d7ad6a0c67ff829bb1c976f6bbdaa0e1795`.

## Recovery, cleanup and limits

No reproducible product defect or unresolved infrastructure failure remains. Before execution, a VERIFIER DEFECT in an observer assertion treated official Windows EOL status as content drift; its check was corrected to verify EOL-neutral content and unchanged before/after state. During execution a Docker observer raced a normally removed container; this auxiliary observer limitation did not affect official results. The complete fresh official run finished without a gate restart or lost result.

As explicitly authorized, the two untracked historical stage3/stage4 preparation.json files and the old untracked stage1 verifier cache were preserved under the external diagnostic root's `precursors/` directory and removed from Result. No tracked acceptance evidence was changed. A shell cleanup command was automatically rejected; preservation completed safely through an external helper, without changing production or requiring human input.

The official summary sets `preview: true` and explicitly warns that the shipped checks are only a portion of the tests applied before judging. All shipped checks ran here; the frozen independent campaigns provide additional normative, concurrency, history, optimizer and upgrade coverage. This gate does not claim exhaustive proof over every schedule or input. The documented mathematically unbounded exact-output/resource boundary remains; feasible exact correctness is binding. Ephemeral state, no crash persistence, no polling/reload recovery and no manager UI remain the contract's scope. No stricter unofficial readiness/request budget was used.

Only this sanitized final gate artifact is added to Result. Raw diagnostics, precursors, credentials and exports remain outside it. The separate evidence commit and clear-index release are supplied in the final room handoff. Earlier ACCEPT evidence remains frozen.
