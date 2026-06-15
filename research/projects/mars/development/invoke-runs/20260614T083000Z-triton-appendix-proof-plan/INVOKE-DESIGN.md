# Invoke Design: Appendix And Formal Proof Package

## Context View

The paper package already has executable evidence for the reference implementation, CUDA/Triton readiness on a RunPod GPU, and a Lean/Mathlib theorem slice for real-valued router adjoint identities. The next work should make the paper easier to defend by adding a math appendix and selectively expanding formal proof coverage.

## High-Level Structure

The next phase should be executed in waves:

- `W0`: add the math appendix first, because it clarifies the semantic contract for later proof claims.
- `W1`: implement the fixed-mask backward proof, because it is closest to the existing Lean identities and least likely to overclaim.
- `W2`: run softmax and CAP2 proof feasibility lanes, with permission to produce scoped proof reports if implementation becomes too expensive.
- `W3`: run the paper reviewer pass and closure updates.

## Low-Level Components

`APPX-MATH` should explain:

- `Z = X W^T` as router logits.
- `P = sigma(Z)` as relaxed routing probabilities.
- `A` or `M` as the continuous or fixed mask used by the surrogate graph.
- `dZ` as upstream router-logit gradient.
- `dW = dZ^T X`.
- `dX_router = dZ W`.
- Why "exact backward" means exact for the chosen smooth/fixed-mask surrogate, not exact for hard `Top2`.

`PROOF-FIXED-MASK` should target:

- A fixed-mask surrogate graph.
- Algebraic backward identities over real scalars.
- An imported Lean file that builds under the existing lake project.

`PROOF-SOFTMAX` should target:

- A finite-dimensional softmax definition with positive denominator.
- The standard Jacobian identity, scoped to the simplest Mathlib representation that builds.
- A feasibility report if derivative APIs or finite-index ergonomics make the proof too large for this phase.

`PROOF-CAP2` should target:

- Fixed-load/load-penalty derivative pieces only.
- No global routing optimality claim.
- No novelty claim.

## Workflow View

Each task-session should:

1. Read the paper claim guards and current formal report.
2. Perform only the task's scoped edits.
3. Run the lane validation.
4. Update local evidence notes or explain why no update was needed.
5. Stop if a theorem would require broad math infrastructure beyond the task boundary.

## Decision Flow

Use this ordering:

1. If appendix is absent, write it first.
2. If fixed-mask theorem is absent, implement that before softmax/CAP2.
3. If softmax proof is tractable in small scope, add it; otherwise write a blocker report.
4. If CAP2 proof is tractable in small scope, add it; otherwise write a blocker report.
5. Run skeptical review only after the appendix and at least the fixed-mask lane have been attempted.

## Dependency Interface

Lean dependencies:

- Reuse `Mathlib`.
- Reuse `TritonTop2.RealBackwardIdentities`.
- Add new files only under `formal/TritonTop2/`.
- Import new proof files from `formal/TritonTop2.lean`.

Paper dependencies:

- Link appendix from `paper.md`.
- Update `EVIDENCE-MANIFEST.md` only for durable evidence.
- Update `CLAIM-GUARDS.md` if any new guard is discovered.

