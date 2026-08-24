# Context Pack — include nested Craft ledger

Session evidence only; this is not a canonical planning artifact.

## Obligations

| ID | Obligation | Status | Evidence selector |
| --- | --- | --- | --- |
| O1 | Bind the user's option 2 to one exact added ledger. | covered | `decision-result.json` selected option and authority boundary |
| O2 | Preserve the failed `-01` attempt and its stop reason. | covered | `terminal-receipt.json` terminal verdict; `inventory-drift.json` added path |
| O3 | Refresh only the Work Pack and TASK-RUNTIME counts, paths, and route. | covered | current `WORK-PACK.md`; current `TASK-RUNTIME.md` |
| O4 | Admit only a fresh `-02` SWU-CAPI-000 attempt. | covered | decision authority boundary and Work Pack execution policy |
| O5 | Keep successors and product implementation unauthorized. | covered | decision remaining blockers and Work Pack stop decisions |

## Selected evidence

- `decision-gates/20260806T024137Z-include-nested-ledger/decision-result.json` — selected option, exact scope ceiling, and no-successor boundary.
- `readiness/20260806T011647Z-capi-000-one-unit/task-session/inventory-drift.json` — only newly discovered ledger and projected 28/57 scope.
- `readiness/20260806T011647Z-capi-000-one-unit/task-session/terminal-receipt.json` — immutable blocked `-01` result and zero-execution boundary.
- `WORK-PACK.md` — current route projection and SWU board.
- `work-pack/tasks/TASK-RUNTIME.md` — current ingestion and reader contracts.

## Exclusions

- API design/task files: no API implementation delta is authorized.
- Nested ledger contents beyond its path/hash/size: source bytes are inputs, not mutation targets.
- Public Arcanum and canonical Craft sources: outside the private internal refresh scope.

Strict coverage: pass. Five obligations covered, zero unresolved.
