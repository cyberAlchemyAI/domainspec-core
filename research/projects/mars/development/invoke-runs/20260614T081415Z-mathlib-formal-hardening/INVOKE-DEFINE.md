# Invoke Define - Mathlib Formal Hardening

Mode: `define`
Status: `pass`
Target: `research/projects/mars/papers/triton-top2-backward-kernel/formal/`

## Intent

Harden the Triton Top2 paper package by adding Mathlib-backed Lean evidence for
real-valued finite-dimensional router backward identities.

## Scope

In scope:

- pin Mathlib for Lean 4.30.0;
- add real-valued finite-sum identities for logits, dW, and dX-router adjoints;
- update the formal report and paper-facing review artifacts;
- validate with `lake build`.

Out of scope:

- full CAP2 calculus proof;
- softmax derivative proof;
- Triton/CUDA memory proof;
- FP16 numerical proof;
- novelty claims.

## Glossary

| Term | Definition |
| --- | --- |
| Mathlib hardening | Replacing or supplementing toy Lean definitions with Mathlib-backed real-valued finite-sum theorems. |
| Adjoint identity | Equality showing that a proposed backward contraction has the same inner-product action as the forward linear map. |
| Router linear map | The map `(X, W) -> X W^T` viewed before softmax or hard/relaxed routing. |
| Formal standing | Paper credibility gained from mechanized proof of a precise claim, not from merely importing a library. |

## Decisions

| Decision | Selection | Rationale |
| --- | --- | --- |
| Mathlib version | `v4.30.0` | Matches local Lean `4.30.0`; tag verified by `git ls-remote`. |
| First theorem slice | Real finite-sum adjoint identities for logits. | Stronger than reducer wiring and directly relevant to backward kernels. |
| Claim posture | bounded formal hardening | Avoids overclaiming full CAP2/Triton correctness. |

## Next Route

`invoke design` then `invoke plan`, followed by `task-session` execution in the
same bounded package.

