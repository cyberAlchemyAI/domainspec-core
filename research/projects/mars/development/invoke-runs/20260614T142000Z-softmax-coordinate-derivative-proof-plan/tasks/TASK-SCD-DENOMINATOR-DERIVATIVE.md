# Task: Denominator Finite-Sum Derivative

Task id: `TASK-SCD-DENOMINATOR-DERIVATIVE`

Status: `complete`

Layer: `L1`

## Objective

Prove the derivative of the finite softmax denominator along `coordLine`.

## Dependencies

- `TASK-SCD-NUMERATOR-DERIVATIVE`

## Smallest Working Units

### `SWU-SCD-003`

Goal: prove:

```lean
theorem softmaxDen_coordLine_hasDerivAt
    {E : Nat} [Nonempty (Fin E)] (z : Fin E -> ℝ) (k : Fin E) :
    HasDerivAt
      (fun h : ℝ => softmaxDen (coordLine z k h))
      (Real.exp (z k))
      0 := by
  ...
```

Implementation detail:

- unfold `softmaxDen`;
- use finite-sum derivative over `Finset.univ`;
- use `exp_coordLine_hasDerivAt` for each term;
- simplify `∑ j, Real.exp (z j) * basis k j` to `Real.exp (z k)`.

## Write Scope

- `formal/TritonTop2/SoftmaxCoordinate.lean`
- optional blocker report if Mathlib sum theorem shape blocks progress
- task-session result link in this task file

## Done Criteria

- The theorem builds, or a precise blocker report names the missing Mathlib theorem-shape.

## Validation

```bash
cd research/projects/mars/papers/triton-top2-backward-kernel/formal
lake build
```

Result: `pass`, `Build completed successfully (2105 jobs).`

## Completion Evidence

- Theorem: `softmaxDen_coordLine_hasDerivAt`
- Task session: `research/projects/mars/development/task-sessions/20260614T150000Z-task-scd-denominator-derivative/RESULT.md`
