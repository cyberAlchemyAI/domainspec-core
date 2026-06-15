# Refine Seed Proposal - Triton Appendix And Proof Strategy

Status: `strategy-ready`
Preset: `standard`
Research mode: `research-if-gap-appears`

## Target

`research/projects/mars/papers/triton-top2-backward-kernel/`

## Desired Outcome

Create a non-executed, evidence-governed strategy for:

1. a plain-language math appendix explaining the Mathlib-backed router adjoint
   identities;
2. next formal proof lanes;
3. a skeptical paper reviewer pass.

## Source Context

- Existing paper package:
  `research/projects/mars/papers/triton-top2-backward-kernel/`
- Mathlib hardening:
  `research/projects/mars/papers/triton-top2-backward-kernel/formal/TritonTop2/RealBackwardIdentities.lean`
- Formal report:
  `research/projects/mars/papers/triton-top2-backward-kernel/formal/FORMAL-VALIDATION-REPORT.md`
- Claim guards:
  `research/projects/mars/papers/triton-top2-backward-kernel/CLAIM-GUARDS.md`

## Refined Scope

The next phase should plan four lanes:

| Lane | Purpose | Risk |
| --- | --- | --- |
| APPX-MATH | Explain `logits = X W^T`, upstream `dZ`, `dW = dZ^T X`, and `dX = dZ W` in prose. | Medium: must stay readable without weakening rigor. |
| PROOF-FIXED-MASK | Prove fixed-mask exact backward for the masked smooth graph. | Medium: achievable and most directly useful. |
| PROOF-SOFTMAX | Prove or scope the softmax derivative theorem needed for a fuller router graph. | High: calculus/API complexity. |
| PROOF-CAP2 | Prove or scope CAP2 fixed-load derivative pieces. | High: candidate relaxation plus nontrivial formula surface. |

## Done Criteria

- Dispatch route validates.
- Invoke define/design/plan artifacts exist.
- Each proof lane has a theorem target, write scope, validation command, and
  claim boundary.
- Execution is not started without operator confirmation.

## Claim Boundary

No next-phase artifact may claim:

- hard Top2 differentiability;
- CAP2 novelty;
- exact 2-sparsity for CAP2;
- Triton/CUDA correctness from Lean;
- FP16 numerical proof.

