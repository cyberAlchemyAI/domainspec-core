# Invoke Design: Lean Proof Architecture

## Context View

The current formal package already proves router-linear adjoint identities and fixed-mask backward adjoint identities. The next proof work should extend the formal surface in a controlled ladder:

1. finite softmax coordinate derivative;
2. CAP2-v0 definitions;
3. fixed-load CAP2 scalar/boundary theorem;
4. optional generalizations.

## High-Level Structure View

Add theorem files under `formal/TritonTop2/`:

```text
SoftmaxCoordinate.lean
CAP2Definition.lean
CAP2FixedLoadScalar.lean
```

Optional later files:

```text
SoftmaxJacobian.lean
CAP2NormalizedGateDerivative.lean
```

Each file should be imported by `formal/TritonTop2.lean` only after it builds.

## Low-Level Components View

### `SoftmaxCoordinate.lean`

Definitions:

- `softmaxDen`
- `softmaxCoord`
- `basis`
- `coordLine`

Core theorem sequence:

- denominator positivity;
- coordinate line simplification;
- derivative of denominator along coordinate line;
- derivative of `softmaxCoord` along coordinate line.

### `CAP2Definition.lean`

Definitions:

- `cap2Capacity`
- `cap2Overload`
- `cap2AdjustedLogit`
- `cap2PairwiseSoftRank`
- `cap2Membership`
- `cap2Gated`
- `cap2WeightDen`
- `cap2Weight`

Boundary lemmas:

- load is an explicit argument;
- load is not differentiated by definition;
- weights are defined from adjusted logits and fixed load.

### `CAP2FixedLoadScalar.lean`

First theorem:

- a scalar fixed-load boundary theorem, likely proving the capacity/load pressure term is constant with respect to a coordinate perturbation when load is fixed;
- after softmax coordinate theorem exists, optionally prove one normalized-gate quotient derivative.

## Workflow Process View

Run one SWU at a time:

1. build softmax definitions and positivity;
2. prove softmax coordinate derivative;
3. freeze CAP2 definitions;
4. prove CAP2 fixed-load scalar boundary;
5. update paper evidence/review.

Every SWU ends with `lake build`.

## Decision Flow View

Decision order:

1. If `SoftmaxCoordinate.lean` definitions do not build, stop and repair representation.
2. If positivity builds but derivative blocks, keep the coordinate theorem as the active blocker; do not move to Jacobian.
3. If CAP2 definition conflicts with reference/prose, stop and update CAP2 definition notes before proving derivative lemmas.
4. If CAP2 scalar proof starts implying dynamic load gradients, stop and restate the theorem.

## Dependency Interface View

Dependencies:

- `Mathlib.Analysis.Calculus.Deriv.Basic`
- `Mathlib.Analysis.SpecialFunctions.Exp`
- `Mathlib.Algebra.BigOperators.Group.Finset.Basic`
- existing `TritonTop2.RealBackwardIdentities`
- existing claim guards in paper package

Interfaces to update after successful theorem slices:

- `formal/TritonTop2.lean`
- `formal/FORMAL-VALIDATION-REPORT.md`
- `EVIDENCE-MANIFEST.md`
- `CLAIM-GUARDS.md`
- `PAPER-REVIEW.md`

## Risk Design

Softmax risk: Mathlib derivative API complexity. Mitigation: coordinate-line theorem before Jacobian.

CAP2 risk: proving the wrong formula. Mitigation: CAP2 definition freeze before derivative proof.

Paper risk: overclaiming. Mitigation: every theorem name gets a matching non-claim boundary.

