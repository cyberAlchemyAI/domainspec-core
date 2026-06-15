# Refine Seed Proposal: Full Softmax Coordinate Derivative

Run id: `20260614T135903Z-softmax-coordinate-derivative-plan`

## Target

`research/projects/mars/papers/triton-top2-backward-kernel/formal/TritonTop2/SoftmaxCoordinate.lean`

## Operator Intent

Refine the whole step-by-step route from the current softmax foundation to a full Lean proof of the finite softmax coordinate derivative, then hand the route to `invoke` for define, design, and plan authoring.

## Desired Outcome

A confirmed, non-executed proof-program strategy that can become an `invoke` define/design/plan bundle and then a `task-session` work-pack for proving:

```text
d/dh softmaxCoord (coordLine z k h) i at h = 0
  = softmaxCoord z i * (indicator(i = k) - softmaxCoord z k)
```

## Current Evidence Baseline

- `formal/TritonTop2/SoftmaxCoordinate.lean` defines `softmaxDen`, `softmaxCoord`, `basis`, and `coordLine`.
- `formal/TritonTop2/SoftmaxCoordinate.lean` proves denominator positivity and support simplification lemmas.
- `formal/SOFTMAX-COORDINATE-BLOCKER.md` narrows the remaining proof to Mathlib calculus steps.
- `development/invoke-runs/20260614T102500Z-lean-softmax-cap2-proof-plan/WORK-PACK.md` records the previous task as `blocked_after_foundation`.

## Preset

`standard`

## Research Mode

`research-if-gap-appears`

Local-first is enough for the first pass. External research should only be requested if the invoke/interrogation/distill loop identifies a named Mathlib theorem-shape gap that cannot be resolved from the repository and installed Lean environment.

## Proposed Proof Ladder

1. Preserve the existing representation:
   - keep `softmaxDen : (Fin E -> ℝ) -> ℝ`;
   - keep `softmaxCoord : (Fin E -> ℝ) -> Fin E -> ℝ`;
   - keep `coordLine z k h j = z j + h * basis k j`.

2. Prove coordinate-line derivative primitives:
   - `HasDerivAt (fun h => coordLine z k h j) (basis k j) 0`;
   - special forms for `j = k` and `j ≠ k`.

3. Prove numerator derivative:
   - `HasDerivAt (fun h => Real.exp (coordLine z k h i)) (Real.exp (z i) * basis k i) 0`;
   - simplify to `Real.exp (z i)` when `i = k`;
   - simplify to `0` when `i ≠ k`.

4. Prove denominator derivative:
   - move `HasDerivAt` through the finite sum;
   - use the numerator derivative for every `j`;
   - simplify the finite sum of all zero terms except `k`;
   - target theorem:

```text
HasDerivAt
  (fun h => softmaxDen (coordLine z k h))
  (Real.exp (z k))
  0
```

5. Prove quotient derivative:
   - numerator derivative for coordinate `i`;
   - denominator derivative for selected coordinate `k`;
   - nonzero denominator from `softmaxDen_ne_zero`;
   - quotient rule for `fun h => softmaxCoord (coordLine z k h) i`.

6. Normalize algebra:
   - rewrite `Real.exp (z i) / softmaxDen z` as `softmaxCoord z i`;
   - rewrite `Real.exp (z k) / softmaxDen z` as `softmaxCoord z k`;
   - express the indicator as `basis k i`;
   - prove final derivative:

```text
HasDerivAt
  (fun h => softmaxCoord (coordLine z k h) i)
  (softmaxCoord z i * (basis k i - softmaxCoord z k))
  0
```

7. Add optional readable corollaries:
   - selected coordinate case `i = k`;
   - non-selected coordinate case `i ≠ k`;
   - finite softmax Jacobian row/column statement if the coordinate theorem is stable.

8. Sync evidence:
   - update formal validation report;
   - update claim guards;
   - update evidence manifest;
   - keep the paper language scoped to finite softmax coordinate derivative only.

## Done Criteria

- A validated dispatch route exists before stage execution.
- The route includes the ten canonical refine stages.
- Invoke define/design/plan stages are explicit and owner-bound.
- The next execution route is a `task-session` work-pack with smallest proof units.
- No artifact claims hard `Top2` differentiability, Triton/CUDA formal correctness, FP16 formal proof, or CAP2 novelty.

## Validation Surface

- `lake build` inside `research/projects/mars/papers/triton-top2-backward-kernel/formal`.
- JSON shape checks for dispatch/index artifacts.
- `rg` checks for proof theorem names, claim guards, and evidence IDs.

## Permission Boundary

This proposal does not run the ten-stage refine loop or execute `invoke` stages. The next step requires operator confirmation because `refine` requires a strategy preview before runtime-backed stage execution.
