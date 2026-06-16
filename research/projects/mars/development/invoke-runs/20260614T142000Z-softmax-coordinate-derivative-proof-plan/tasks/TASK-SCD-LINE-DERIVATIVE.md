# Task: Coordinate-Line Derivative

Task id: `TASK-SCD-LINE-DERIVATIVE`

Status: `complete`

Layer: `L0`

## Objective

Prove the derivative primitive for `coordLine`.

## Smallest Working Units

### `SWU-SCD-001`

Goal: add the narrow Mathlib calculus imports and prove:

```lean
theorem coordLine_hasDerivAt
    {E : Nat} (z : Fin E -> ℝ) (k j : Fin E) :
    HasDerivAt (fun h : ℝ => coordLine z k h j) (basis k j) 0 := by
  ...
```

Optional helper corollaries:

- selected coordinate derivative is `1`;
- non-selected coordinate derivative is `0`.

## Write Scope

- `formal/TritonTop2/SoftmaxCoordinate.lean`
- task-session result link in this task file

## Done Criteria

- The theorem builds.
- Existing softmax foundation theorems still build.

## Validation

```bash
cd research/projects/mars/papers/triton-top2-backward-kernel/formal
lake build
```

Result: `pass`, `Build completed successfully (2068 jobs).`

## Completion Evidence

- Theorem: `coordLine_hasDerivAt`
- Task session: `research/projects/mars/development/task-sessions/20260614T143000Z-task-scd-line-derivative/RESULT.md`

## Handoff Note

Start here. Do not attempt denominator or quotient calculus in this task.
