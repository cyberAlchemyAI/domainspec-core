# Context Pack: Node 26 WaveDB source-build retry

- Mode: `standard`, strict
- Activation: direct user request, `update to node 26`
- Target: one newly planned immutable diagnostic attempt
- Runtime handoff: none; this pack is Invoke Refresh session evidence
- Authority: live Work Pack and receipts outrank Inventory discovery

## Obligations

| ID | Obligation | Evidence | Status |
| --- | --- | --- | --- |
| O1 | Preserve the Node 22 attempt and its blocker | SWU-WCSB-002 terminal receipt, task contract | covered |
| O2 | Pin one exact Node 26 toolchain | official release index observed 2026-08-05: Node `v26.6.0`, npm `11.18.0`, non-LTS | covered |
| O3 | Use the reviewed WaveDB source identity | runner contract and source-build receipt bind commit `01c77e8b70f71de9b72480e73a3a179f6e93a009` | covered |
| O4 | Allocate a fresh attempt and evidence namespace | `wcsb-20260805-node26-01`, `execution/source-build-node26/**` | covered |
| O5 | Keep all build/test/canary/scope gates acceptance-critical | runner and validator | covered |
| O6 | Correct only relevant plan drift | Work Pack selects none; Execution Pack still names SWU-WCSB-001 | covered |
| O7 | Keep Craft, publication, deployment, and addon handoff out of scope | Inventory decision boundary and Work Pack | covered |
| O8 | Use a separate validated serial route | new Node 26 retry dispatch; no subagents | covered |

## Selected evidence

| Source | Selector | Obligation fit |
| --- | --- | --- |
| `plan/WORK-PACK.md` | control fields, SWU manifest, blockers, closeout | O1, O4-O7 |
| `plan/EXECUTION-PACK.md` | selected SWU and choreography | O6, O8 |
| `plan/work-pack/waves/W0-SOURCE-BUILD.md` | current state and retry rule | O1, O4, O5 |
| `plan/work-pack/shared/traceability.md` | source-build evidence map | O3-O5 |
| `plan/work-pack/shared/cross-task-gaps.md` | compatibility and authority residue | O2, O7 |
| `plan/work-pack/tasks/TASK-WCSB-02-EXECUTE.md` | prior attempt and blocked stage | O1, O5 |
| `execution/task-sessions/SWU-WCSB-002/terminal-receipt.json` | blocker, partial evidence, smallest unblock | O1, O4, O5 |
| `runtime/run_source_build.py` | toolchain pins and ordered gates | O2-O5 |
| `runtime/validate_source_build.py` | terminal pass validation | O3-O5 |
| `.arcanum/inventory/entries/wavedb-craft-runtime-research-result-synthesis.md` | candidate-only/Craft boundary | O7 |

## Constraints

- Do not reuse or edit `.work/wcsb-20260804-01` or its receipts.
- Do not change the WaveDB commit, lockfile, build files, OpenSSL mode, or test set.
- Install Node `v26.6.0` through existing user-local NVM without changing the default alias.
- The new task stops on the first acceptance-critical failure and performs no implicit retry.
- A successful Node 26 result remains one local Linux x86_64 observation and still requires a separate parent handoff.

## Target inventory

- `plan/WORK-PACK.md`
- `plan/EXECUTION-PACK.md`
- `plan/work-pack/waves/W0-SOURCE-BUILD.md`
- `plan/work-pack/shared/traceability.md`
- `plan/work-pack/shared/cross-task-gaps.md`
- `plan/work-pack/tasks/TASK-WCSB-03-NODE26.md`
- `plan/node26-retry.dispatch.json`

## Excluded candidates

- Canonical and historical Craft trees: explicitly forbidden.
- Original `source-build.dispatch.json`: historical record of the Node 22 chain; a new retry dispatch avoids rewriting it.
- Runner/validator source: current CLI already accepts exact Node/npm identities and fresh attempt/evidence paths.
- Parent experiment plan: no passing source-build receipt exists.

## Result

Strict obligation coverage is complete. The next owner is Invoke Refresh
`apply-approved` over exactly the seven target paths above, followed by one
Task Session for `SWU-WCSB-003`.
