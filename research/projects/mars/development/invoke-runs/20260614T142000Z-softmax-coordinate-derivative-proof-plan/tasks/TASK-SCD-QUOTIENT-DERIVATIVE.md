# Task: Raw Quotient Derivative

Task id: `TASK-SCD-QUOTIENT-DERIVATIVE`

Status: `complete`

Layer: `L2`

## Objective

Prove a raw quotient-rule derivative for `softmaxCoord (coordLine z k h) i`.

## Dependencies

- `TASK-SCD-DENOMINATOR-DERIVATIVE`

## Smallest Working Units

### `SWU-SCD-004`

Goal: prove a raw theorem equivalent to:

```text
((Real.exp (z i) * basis k i) * softmaxDen z
  - Real.exp (z i) * Real.exp (z k)) / (softmaxDen z)^2
```

as the derivative of:

```lean
fun h : ℝ => softmaxCoord (coordLine z k h) i
```

at `0`.

Implementation detail:

- use numerator theorem;
- use denominator theorem;
- use `softmaxDen_ne_zero`;
- apply quotient rule;
- keep algebraic normalization out of this task.

## Write Scope

- `formal/TritonTop2/SoftmaxCoordinate.lean`
- optional blocker report if quotient theorem shape blocks progress
- task-session result link in this task file

## Done Criteria

- A raw quotient theorem builds, or a precise blocker report preserves all prior theorem evidence.

## Validation

```bash
cd research/projects/mars/papers/triton-top2-backward-kernel/formal
lake build
```

Result: `pass`, `Build completed successfully (2106 jobs).`

## Completion Evidence

- Theorem: `softmaxCoord_coordLine_hasDerivAt_raw`
- Task session: `research/projects/mars/development/task-sessions/20260614T151000Z-task-scd-quotient-derivative/RESULT.md`
