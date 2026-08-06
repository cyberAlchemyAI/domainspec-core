# Task Session context: SWU-WCND-001

- Mode: lean, strict.
- Resolution: explicit `WORK-PACK.md#SWU-WCND-001`.
- Runtime: local Node `v26.6.0` / npm `11.18.0` through existing NVM.
- Strict coverage: 12/12 obligations.
- Handoff pack: none; no runtime delegation.

## Execution contract

| ID | Obligation | Controlling evidence | Status |
| --- | --- | --- | --- |
| WCND-TS-01 | exact package `@vijayee/wavedb@0.15.8` only | Work Pack; Decision | covered |
| WCND-TS-02 | exact SHA-1/SRI/tarball URL before scripts | Work Pack; provenance result | covered |
| WCND-TS-03 | tarball is artifact identity; no Git-source claim | Decision; history reconstruction | covered |
| WCND-TS-04 | fresh immutable attempt/evidence namespaces | Work Pack write scope and live absence check | covered |
| WCND-TS-05 | exact Node/npm and unchanged NVM default | Work Pack; live preflight | covered |
| WCND-TS-06 | isolated native install with 180-second external timeout | Work Pack algorithm | covered |
| WCND-TS-07 | exactly one addon and load within 20 seconds | Work Pack validation table | covered |
| WCND-TS-08 | basic, empty, batch/reopen canaries | Work Pack validation table | covered |
| WCND-TS-09 | upstream-shaped 100-write concurrency within 30 seconds | source integration selector; Work Pack | covered |
| WCND-TS-10 | controller termination is not crash proof | Work Pack step 9 | covered |
| WCND-TS-11 | no Craft/prior attempt/Git/default/publication/deployment effect | Decision; Work Pack forbidden scope | covered |
| WCND-TS-12 | terminal receipt and exact one-target closeout | Work Pack closeout row | covered |

## Exact outputs

- `ops/development/2026-08-04-wavedb-craft-runtime-research/experiment/source-build/.work/wcnd-20260805-node26-01/**`;
- `ops/development/2026-08-04-wavedb-craft-runtime-research/experiment/source-build/npm-diagnostic/execution/npm-node26/**`;
- `ops/development/2026-08-04-wavedb-craft-runtime-research/experiment/source-build/npm-diagnostic/execution/task-sessions/SWU-WCND-001/**`.

Material writes: none. The attempt-local consumer, tarball extraction, harness,
node_modules, stores, npm logs, and result files are validation-owned execution
outputs. Plan files are controlling inputs and may change only through the
declared Invoke closeout owner after the terminal receipt exists.

## Stop rules

Stop without retry at any identity drift, install/build failure or timeout,
addon mismatch/load failure, functional failure/timeout, unexpected scope
effect, or missing receipt. Preserve all attempt residue. Do not substitute a
source checkout, version, tarball, dependency policy, Node version, or Craft
integration.
