# Execution Pack: WaveDB Craft Projection Experiment

## Control

- Work Pack: `WORK-PACK.md`
- Layering: `IMPLEMENTATION-LAYERING.md`
- Architecture: `../design/ARCHITECTURE.md`
- Mode: bounded serial Task Sessions until first blocker or frontier complete
- Captured frontier: `SWU-WCP-001` through `SWU-WCP-008`
- Session budget: 8
- Current selected unit: `SWU-WCP-001`
- Mutation ceiling: experiment package only; native install prohibited until
  `SWU-WCP-001=pass`

## Waves

| Wave | Units | Gate | Stop condition |
| --- | --- | --- | --- |
| W0 Input closure | SWU-WCP-001, SWU-WCP-002 | provenance pass before fixture/package resolution | any identity or fixture contradiction |
| W1 Construction | SWU-WCP-003, SWU-WCP-004 | frozen exact inputs and supported native build | build, YAML guard, or exact normal-path failure |
| W2 Failure evidence | SWU-WCP-005, SWU-WCP-006, SWU-WCP-007 | verified normal generation | hybrid iterator, non-zero negative output, or rebuild mismatch |
| W3 Closeout | SWU-WCP-008 | all prior receipts pass | missing evidence or claim-ceiling violation |

## Serial orchestration rule

Each unit receives a fresh Task Session context pack and produces its own
terminal receipt and Invoke Refresh closeout receipt or exact no-op proof. The
next unit is legal only when it is the single declared dependency-ready
successor. Any block, flag outside the allowlist, missing owner receipt,
acceptance-critical validation failure, or scope drift stops the chain.

## Runtime isolation

- registry download cache and unpacked audit sources use an explicit temporary
  directory;
- any later dependency installation is local to `experiment/runtime/` and
  requires a passed provenance receipt;
- stores live only under `experiment/execution/stores/<run-id>/` or an exact
  temporary sibling named in the Task Session receipt;
- corruption and crash controls target child processes and isolated copies;
- canonical Craft paths and every real `.craft/` path are read-only.

## Final reducer

`COMPLETE` requires eight passing Task Session receipts, their closeout joins,
all exact acceptance evidence, and no unresolved L0 blocker. Otherwise return
`BLOCK` with the first failed unit, remaining captured frontier, preserved
HOLD/KILL residue, and one owner route. Never average or conceal failed
controls.
