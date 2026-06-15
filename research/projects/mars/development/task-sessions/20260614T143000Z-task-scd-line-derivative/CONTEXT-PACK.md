# Context Pack: TASK-SCD-LINE-DERIVATIVE

Task: `TASK-SCD-LINE-DERIVATIVE`

Mode: `lean`

Strict coverage: `pass`

## Obligations

| Obligation | Status | Evidence |
| --- | --- | --- |
| Select exactly one ready task | covered | `WORK-PACK.md` lists `TASK-SCD-LINE-DERIVATIVE` as next ready task. |
| Keep write scope narrow | covered | Task allows `formal/TritonTop2/SoftmaxCoordinate.lean` and task-session evidence sync. |
| Prove coordinate-line derivative | covered | Target theorem `coordLine_hasDerivAt`. |
| Preserve existing softmax foundation | covered | Validation command: `lake build`. |
| Avoid denominator or quotient work | covered | Task handoff note says not to attempt denominator or quotient calculus. |

## Selected Evidence

- `research/projects/mars/development/invoke-runs/20260614T142000Z-softmax-coordinate-derivative-proof-plan/WORK-PACK.md`
  - selected for task board, next ready task, SWU manifest, shared write scope, claim guards, and stop conditions.
- `research/projects/mars/development/invoke-runs/20260614T142000Z-softmax-coordinate-derivative-proof-plan/tasks/TASK-SCD-LINE-DERIVATIVE.md`
  - selected for objective, theorem statement, write scope, done criteria, and validation command.
- `research/projects/mars/papers/triton-top2-backward-kernel/formal/TritonTop2/SoftmaxCoordinate.lean`
  - selected for current definitions and existing softmax foundation.

## Constraints

- Do not change existing definitions unless a blocker proves it is necessary.
- Do not claim hard `Top2` differentiability.
- Do not work on denominator, quotient, or paper sync in this task.

## Validation Surface

```bash
cd research/projects/mars/papers/triton-top2-backward-kernel/formal
lake build
```
