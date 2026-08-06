# Plan Transport

- Mode: `plan`
- Design prerequisite: `design-validator-pass`
- Complexity/output: high, split
- Layering: `IMPLEMENTATION-LAYERING.md`
- Work Pack: `WORK-PACK.md`
- Execution Pack: `EXECUTION-PACK.md`
- Dispatch trace: `DISPATCH-TECHNIQUE-TRACE.md`
- Distill validation: `pass` for authored Plan coherence
- Work Pack gate: pass for the selected read-only provenance SWU only
- First selected unit: `SWU-WCP-001`
- Native mutation admission: blocked until `SWU-WCP-001=pass`
- Execution route: a fresh Task Session for `SWU-WCP-001`; stop on its first
  provenance contradiction and preserve the remaining frontier.
- Claim ceiling: a Plan is not execution evidence and a provenance receipt is
  not a passing WaveDB/Craft projection experiment.
