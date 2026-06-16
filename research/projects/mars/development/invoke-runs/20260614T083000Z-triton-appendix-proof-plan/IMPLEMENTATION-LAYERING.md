# Implementation Layering

## L0: Reader Contract

Goal: make the problem explainable before adding more proof surface.

Deliverable: math appendix explaining the relaxed/fixed-mask backward contract and mapping prose to current Lean theorem names.

Exit check: appendix exists, is linked from the paper, and does not expand claims.

## L1: Low-Risk Formal Expansion

Goal: prove the fixed-mask relaxed backward graph, where the selection/mask is data and the remaining graph is differentiable.

Deliverable: `formal/TritonTop2/FixedMaskBackward.lean` or an equivalent narrow file.

Exit check: `lake build` passes and the formal report names the new theorem.

## L2: Feasibility-First Formal Expansion

Goal: test whether softmax and CAP2 derivative pieces can be added without turning this paper package into a large formalization project.

Deliverables:

- `formal/TritonTop2/SoftmaxDerivative.lean` or `SOFTMAX-PROOF-FEASIBILITY.md`.
- `formal/TritonTop2/CAP2FixedLoadDerivative.lean` or `CAP2-PROOF-FEASIBILITY.md`.

Exit check: either `lake build` passes with the new theorem slice, or the feasibility report states the exact blocker and next smallest theorem.

## L3: Paper Hardening

Goal: make the presentation defensible.

Deliverables: updated paper review, claim guards, evidence manifest, and presentation package.

Exit check: review pass has no unresolved high-severity overclaim.

