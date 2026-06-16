# Task: Algebraic Normalization And Corollaries

Task id: `TASK-SCD-ALGEBRA-COROLLARIES`

Status: `complete`

Layer: `L3`

## Objective

Normalize the raw quotient theorem into the paper-facing finite-softmax coordinate derivative.

## Dependencies

- `TASK-SCD-QUOTIENT-DERIVATIVE`

## Smallest Working Units

### `SWU-SCD-005`

Goal: prove:

```lean
theorem softmaxCoord_coordLine_hasDerivAt
    {E : Nat} [Nonempty (Fin E)] (z : Fin E -> ℝ) (k i : Fin E) :
    HasDerivAt
      (fun h : ℝ => softmaxCoord (coordLine z k h) i)
      (softmaxCoord z i * (basis k i - softmaxCoord z k))
      0 := by
  ...
```

Optional corollaries:

- `softmaxCoord_coordLine_hasDerivAt_self`
- `softmaxCoord_coordLine_hasDerivAt_of_ne`

## Write Scope

- `formal/TritonTop2/SoftmaxCoordinate.lean`
- optional blocker report if algebraic normalization blocks progress
- task-session result link in this task file

## Done Criteria

- The normalized theorem builds.
- Optional corollaries build or are explicitly deferred.

## Validation

```bash
cd research/projects/mars/papers/triton-top2-backward-kernel/formal
lake build
```

Result: `pass`, `Build completed successfully (3044 jobs).`

## Completion Evidence

- Theorem: `softmaxCoord_coordLine_hasDerivAt`
- Optional corollaries: deferred; the normalized theorem specializes through `basis`.
- Task session: `research/projects/mars/development/task-sessions/20260614T152000Z-task-scd-algebra-corollaries/RESULT.md`
