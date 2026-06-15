# TASK-PROOF-FIXED-MASK: Fixed-Mask Backward Proof

Status: `complete`

## Purpose

Formalize the exact backward pass for the fixed-mask relaxed graph, where mask/selection values are treated as constant data.

## Write Scope

- Add `research/projects/mars/papers/triton-top2-backward-kernel/formal/TritonTop2/FixedMaskBackward.lean`.
- Update `formal/TritonTop2.lean`.
- Update `formal/FORMAL-VALIDATION-REPORT.md`.

## Smallest Useful Work Unit

Prove one narrow theorem that composes the existing real-valued adjoint identities with a fixed mask or fixed routing weight. The theorem should avoid claiming differentiability through the mask itself.

## Validation

```bash
cd research/projects/mars/papers/triton-top2-backward-kernel/formal
lake build
```

## Fallback

If the theorem statement is too broad, reduce to a scalar or finite-index lemma and record the deferred generalization in the formal validation report.

## Completion Criteria

- `lake build` passes.
- The theorem name and limitation are listed in the formal report.
- Paper prose says fixed-mask proof, not hard-selection proof.

## Completion Evidence

- Lean file: `research/projects/mars/papers/triton-top2-backward-kernel/formal/TritonTop2/FixedMaskBackward.lean`
- Formal entrypoint: `research/projects/mars/papers/triton-top2-backward-kernel/formal/TritonTop2.lean`
- Formal report: `research/projects/mars/papers/triton-top2-backward-kernel/formal/FORMAL-VALIDATION-REPORT.md`
- Session result: `research/projects/mars/development/task-sessions/20260614T091000Z-task-proof-fixed-mask/RESULT.md`
