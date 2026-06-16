# Task: Numerator Exponential Derivative

Task id: `TASK-SCD-NUMERATOR-DERIVATIVE`

Status: `complete`

Layer: `L0`

## Objective

Prove the derivative of the exponential numerator along `coordLine`.

## Dependencies

- `TASK-SCD-LINE-DERIVATIVE`

## Smallest Working Units

### `SWU-SCD-002`

Goal: prove:

```lean
theorem exp_coordLine_hasDerivAt
    {E : Nat} (z : Fin E -> ℝ) (k i : Fin E) :
    HasDerivAt
      (fun h : ℝ => Real.exp (coordLine z k h i))
      (Real.exp (z i) * basis k i)
      0 := by
  ...
```

Optional helper corollaries:

- selected numerator derivative is `Real.exp (z k)`;
- non-selected numerator derivative is `0`.

## Write Scope

- `formal/TritonTop2/SoftmaxCoordinate.lean`
- task-session result link in this task file

## Done Criteria

- The theorem builds.
- `coordLine_hasDerivAt` remains available to downstream tasks.

## Validation

```bash
cd research/projects/mars/papers/triton-top2-backward-kernel/formal
lake build
```

Result: `pass`, `Build completed successfully (2105 jobs).`

## Completion Evidence

- Theorem: `exp_coordLine_hasDerivAt`
- Task session: `research/projects/mars/development/task-sessions/20260614T144500Z-task-scd-numerator-derivative/RESULT.md`
