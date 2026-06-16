# Implementation Layering: Softmax Coordinate Derivative Proof

## L0: Calculus Primitives

Question: can Lean prove the derivative of `coordLine` and the numerator exponential?

Promotion evidence:

- `coordLine_hasDerivAt` builds.
- `exp_coordLine_hasDerivAt` builds.
- `lake build` passes.

## L1: Denominator Derivative

Question: can Lean move the derivative through the finite softmax denominator sum?

Promotion evidence:

- `softmaxDen_coordLine_hasDerivAt` builds.
- The theorem states derivative `Real.exp (z k)` at `0`.
- `lake build` passes.

## L2: Quotient Derivative

Question: can Lean prove a raw derivative for `softmaxCoord` using the quotient rule?

Promotion evidence:

- `softmaxCoord_coordLine_hasDerivAt_raw` builds or a precise blocker report is written.
- Nonzero denominator proof uses `softmaxDen_ne_zero`.
- `lake build` passes.

## L3: Normalized Theorem And Evidence Sync

Question: can the raw derivative be rewritten into the paper-facing finite-softmax expression and synchronized into evidence?

Promotion evidence:

- `softmaxCoord_coordLine_hasDerivAt` builds.
- Optional selected/non-selected corollaries build or are deferred with rationale.
- Formal validation report, evidence manifest, claim guards, and paper text are synchronized.
