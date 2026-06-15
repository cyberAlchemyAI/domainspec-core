# Result - Mathlib Formal Hardening

Status: `pass`

## Completed Tasks

| Task | Result |
| --- | --- |
| TASK-MFH-001 | Pinned Mathlib `v4.30.0`, added `RealBackwardIdentities.lean`, and imported it from `TritonTop2.lean`. |
| TASK-MFH-002 | Updated formal report, paper, claim guards, paper spec, test spec, review, evidence manifest, and presentation package. |
| TASK-MFH-003 | Synchronized validation evidence and work-pack status. |

## Proved Theorem Slice

- `dWReal_adjoint`: real-valued finite-sum dW contraction is adjoint to the logits map in the W argument.
- `dXRouterReal_adjoint`: real-valued finite-sum router-side dX contraction is adjoint to the logits map in the X argument.

## Validation

```bash
cd research/projects/mars/papers/triton-top2-backward-kernel/formal && lake update
```

Result: pass.

```bash
cd research/projects/mars/papers/triton-top2-backward-kernel/formal && lake build
```

Result: pass, `991 jobs`.

```bash
jq empty research/projects/mars/development/invoke-runs/20260614T081415Z-mathlib-formal-hardening/evidence-index.json
```

Result: pass.

## Residuals

- Full softmax derivative proof remains deferred.
- Full CAP2 calculus proof remains deferred.
- Triton/CUDA memory correctness remains empirical/test-backed, not Lean-proved.
- FP16 numerical error proof remains deferred.
