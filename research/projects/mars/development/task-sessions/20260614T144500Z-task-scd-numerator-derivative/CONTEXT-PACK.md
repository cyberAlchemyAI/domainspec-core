# Context Pack: TASK-SCD-NUMERATOR-DERIVATIVE

Task: `TASK-SCD-NUMERATOR-DERIVATIVE`

Mode: `lean`

Strict coverage: `pass`

## Obligations

| Obligation | Status | Evidence |
| --- | --- | --- |
| Select exactly one ready task | covered | `WORK-PACK.md` lists `TASK-SCD-NUMERATOR-DERIVATIVE` as next ready task. |
| Dependency complete | covered | `TASK-SCD-LINE-DERIVATIVE` is complete and `coordLine_hasDerivAt` builds. |
| Keep write scope narrow | covered | Task allows `formal/TritonTop2/SoftmaxCoordinate.lean` and task-session evidence sync. |
| Prove numerator derivative | covered | Target theorem `exp_coordLine_hasDerivAt`. |
| Preserve line derivative for downstream tasks | covered | Validation command: `lake build`. |

## Selected Evidence

- `research/projects/mars/development/invoke-runs/20260614T142000Z-softmax-coordinate-derivative-proof-plan/WORK-PACK.md`
  - selected for task board, dependencies, shared write scope, and stop conditions.
- `research/projects/mars/development/invoke-runs/20260614T142000Z-softmax-coordinate-derivative-proof-plan/tasks/TASK-SCD-NUMERATOR-DERIVATIVE.md`
  - selected for objective, theorem statement, write scope, done criteria, and validation command.
- `research/projects/mars/papers/triton-top2-backward-kernel/formal/TritonTop2/SoftmaxCoordinate.lean`
  - selected for current definitions and `coordLine_hasDerivAt`.

## Constraints

- Do not change existing definitions.
- Do not work on denominator or quotient calculus in this task.
- No hard `Top2` differentiability claim.

## Validation Surface

```bash
cd research/projects/mars/papers/triton-top2-backward-kernel/formal
lake build
```
