# Implementation Layering: Lean Softmax And CAP2 Proofs

## L0: Softmax Foundation

Question: can the package state and build finite softmax definitions and denominator positivity?

Promotion evidence:

- `SoftmaxCoordinate.lean` exists.
- `softmaxDen_pos` or equivalent theorem builds.
- `lake build` passes.

## L1: Softmax Coordinate Derivative

Question: can the package prove the useful coordinate-direction derivative before attempting a full Jacobian?

Promotion evidence:

- coordinate derivative theorem builds.
- formal report records the theorem and its scope.

## L2: CAP2 Definition Freeze

Question: can the CAP2-v0 implementation contract be represented canonically in Lean without ambiguity?

Promotion evidence:

- `CAP2Definition.lean` builds.
- definitions match `CAP2-CANDIDATE-SPEC.md` and `CAP2-REFERENCE.md`.
- load is explicitly fixed data.

## L3: CAP2 First Proof Slice And Paper Sync

Question: can one fixed-load CAP2 proof slice build without implying dynamic-load gradients or novelty?

Promotion evidence:

- `CAP2FixedLoadScalar.lean` builds or produces a scoped blocker report.
- paper evidence and claim guards are synchronized.

