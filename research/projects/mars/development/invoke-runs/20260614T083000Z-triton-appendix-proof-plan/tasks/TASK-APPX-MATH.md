# TASK-APPX-MATH: Math Appendix

Status: `complete`

## Purpose

Create a math appendix that lets a reader understand the backward-pass contract without needing to already know routing, softmax, TopK, or Lean.

## Write Scope

- Add a math appendix under `research/projects/mars/papers/triton-top2-backward-kernel/`.
- Link it from `paper.md`.
- Update `EVIDENCE-MANIFEST.md` if the appendix becomes a durable evidence artifact.

## Required Content

- Define `Z = X W^T` as router logits.
- Define `P = sigma(Z)` as continuous routing probabilities.
- Explain the fixed/relaxed mask used in the surrogate graph.
- Explain that hard `Top2` selection is non-differentiable.
- Explain why the exact backward pass is exact for the surrogate graph only.
- Bridge upstream `dZ` to `dW = dZ^T X` and `dX_router = dZ W`.
- Reference current Lean theorem names from `RealBackwardIdentities.lean`.

## Validation

```bash
rg -n "dW|dX_router|dZ|Top2|surrogate|dWReal_adjoint|dXRouterReal_adjoint" research/projects/mars/papers/triton-top2-backward-kernel
```

## Completion Criteria

- Appendix exists and is linked.
- Claims do not exceed `CLAIM-GUARDS.md`.
- Reader can distinguish hard selection from the differentiable surrogate.

## Completion Evidence

- Appendix: `research/projects/mars/papers/triton-top2-backward-kernel/MATH-APPENDIX.md`
- Paper link/section: `research/projects/mars/papers/triton-top2-backward-kernel/paper.md`
- Evidence sync: `research/projects/mars/papers/triton-top2-backward-kernel/EVIDENCE-MANIFEST.md`
- Session result: `research/projects/mars/development/task-sessions/20260614T090000Z-task-appx-math/RESULT.md`
