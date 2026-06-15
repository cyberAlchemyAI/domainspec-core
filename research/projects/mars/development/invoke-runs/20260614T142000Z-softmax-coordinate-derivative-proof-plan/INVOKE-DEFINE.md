# Invoke Define: Softmax Coordinate Derivative Proof

Mode: `define`

Phase status: `pass`

## Target

Prove the finite softmax coordinate derivative in Lean for the existing representation in `TritonTop2/SoftmaxCoordinate.lean`.

## Scope

In scope:

- `coordLine` derivative primitives.
- Exponential numerator derivative along `coordLine`.
- Finite-sum denominator derivative along `coordLine`.
- Quotient derivative for `softmaxCoord`.
- Algebraic normalization to the standard finite-softmax expression.
- Paper/evidence sync after the theorem builds.

Out of scope:

- hard `Top2` differentiability;
- Triton/CUDA correctness proof;
- FP16 formal proof;
- CAP2 dynamic-load gradient proof;
- CAP2 novelty proof.

## Definitions To Preserve

```lean
softmaxDen : (Fin E -> ℝ) -> ℝ
softmaxCoord : (Fin E -> ℝ) -> Fin E -> ℝ
basis : Fin E -> Fin E -> ℝ
coordLine : (Fin E -> ℝ) -> Fin E -> ℝ -> Fin E -> ℝ
```

The existing representation should not be changed unless a theorem-shape blocker proves the representation cannot support the derivative proof. If a representation change is required, task-session must stop and write a blocker report before mutation.

## Primary Theorem

Preferred statement:

```lean
theorem softmaxCoord_coordLine_hasDerivAt
    {E : Nat} [Nonempty (Fin E)] (z : Fin E -> ℝ) (k i : Fin E) :
    HasDerivAt
      (fun h => softmaxCoord (coordLine z k h) i)
      (softmaxCoord z i * (basis k i - softmaxCoord z k))
      0 := by
  ...
```

## Required Intermediate Theorems

1. `coordLine_hasDerivAt`
2. `exp_coordLine_hasDerivAt`
3. `softmaxDen_coordLine_hasDerivAt`
4. `softmaxCoord_coordLine_hasDerivAt_raw`
5. `softmaxCoord_coordLine_hasDerivAt`

## Decisions

- Use `basis k i` as the formal indicator term.
- Prove denominator derivative before quotient derivative.
- Keep selected/non-selected coordinate corollaries optional until the main theorem builds.

## Gaps

- Exact Mathlib theorem names for finite-sum derivative and quotient derivative must be discovered during task execution.
- If `HasDerivAt` theorem shape proves too brittle, the fallback is a local theorem with `deriv` only after a blocker report explains the trade-off.
