# Task Session Context — SWU-WCND-002

- Mode: lean, strict.
- Resolution: explicit current-user request plus live npm registry identity.
- Runtime: local Node `v26.6.0` / npm `11.18.0` through existing NVM.
- Handoff: none; local execution, no subagents.
- Strict coverage: 12/12 obligations.

## Obligation matrix

| ID | Obligation | Evidence | Status |
| --- | --- | --- | --- |
| WCND2-01 | newest package is exactly `@vijayee/wavedb@0.15.9` | live npm metadata | covered |
| WCND2-02 | exact SHA-1/SRI/tarball identity before scripts | live npm metadata; TASK.md | covered |
| WCND2-03 | tarball is identity; registry `gitHead` is annotation only | prior Decision; current TASK.md | covered |
| WCND2-04 | new immutable attempt/evidence namespaces | live absence check | covered |
| WCND2-05 | Node/npm fixed; NVM default unchanged | live preflight | covered |
| WCND2-06 | isolated install/build with 180-second controller timeout | TASK.md | covered |
| WCND2-07 | one addon and bounded load | prior harness contract; TASK.md | covered |
| WCND2-08 | basic, empty, batch/reopen canaries | prior harness; TASK.md | covered |
| WCND2-09 | 100 concurrent puts plus reads | prior harness; TASK.md | covered |
| WCND2-10 | controller timeout is not package-crash proof | prior Work Pack | covered |
| WCND2-11 | no Craft/prior attempt/Git/default/publication/deployment effect | baselines; TASK.md | covered |
| WCND2-12 | terminal receipt, no inferred Craft/API handoff | TASK.md | covered |

## Selected evidence

- `TASK.md`: exact current unit, identity, scope, done criteria, ceiling.
- `plan/WORK-PACK.md#Ordered algorithm`: previously validated canary procedure;
  reused as method precedent, not authorization for the new version.
- `execution/npm-node26/npm-diagnostic-receipt.json`: immutable `0.15.8` baseline.
- `.work/wcnd-20260805-node26-01/harness.js`: prior canary implementation to
  reproduce byte-for-byte in the new attempt.
- `craft-ledger-import/execution/wcli-20260805-node26-04/receipt.json`: proves
  Craft ingestion remains pinned to `0.15.8`; it is not relabeled.

## Gate

PASS to execution-output-only mutation. The current user request supplies the
new-version decision; identity, runtime, exact outputs, stop rules, and
validation are fully bound. Stop on the first acceptance-critical failure and
preserve the attempt. Do not retry or substitute a source checkout/version.
