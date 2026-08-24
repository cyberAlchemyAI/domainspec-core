# Execution Pack

```text
W0 baseline
  -> W1 OAVA-001 -> OAVA-002
  -> B-001 dependency gate
  -> W2 OAVA-003 -> OAVA-004 -> OAVA-005
  -> W3 OAVA-006 -> OAVA-007
  -> W4 OAVA-008
  -> separate S7 Invoke/Task Session route
```

| Wave | Question | SWUs | Entry | Exit |
|---|---|---|---|---|
| W0 | Is the plan/source/runtime context current? | none | this accepted refinement | digest and environment receipt |
| W1 | Does candidate consultation fail closed? | 001 → 002 | W0 | deterministic contract/consultation evidence |
| W2 | Can the S6 beat run locally? | 003 → 004 → 005 | W1 + B-001 | local standard/reduced prototype |
| W3 | Does it preserve semantics and merit reuse? | 006 → 007 | W2 + B-002/B-003 | browser receipt and owner disposition |
| W4 | What durable residue should survive? | 008 | accepted/revised W3 outcome | episode receipt and non-executed S7 handoff |

## Choreography rules

- Recheck source, plan, runtime, and browser identities at each wave boundary.
- Stop on any source/vault mutation, network request, runtime drift, semantic mismatch, owner-gate implication, or acceptance-critical failure.
- Use the unique-successor handle for continuation when unchanged; do not repeat Define/Design/Plan or readiness discovery mechanically.
- Dependency acquisition, external network, deployment, publishing, voice work, and production rendering remain separate authority gates.

