# Context Pack: TASK-APPX-MATH

Task: `TASK-APPX-MATH`
Mode: `lean`
Strict coverage: `pass`

## Obligations

| ID | Obligation | Coverage |
| --- | --- | --- |
| O1 | Add a math appendix under the paper package. | `TASK-APPX-MATH.md` write scope. |
| O2 | Link the appendix from `paper.md`. | `TASK-APPX-MATH.md` write scope. |
| O3 | Define `Z = X W^T` router logits. | `paper.md` and `RealBackwardIdentities.lean`. |
| O4 | Define `P = sigma(Z)` as continuous probabilities. | `paper.md` problem/background section. |
| O5 | Explain fixed/relaxed mask and hard `Top2` non-differentiability. | `paper.md`, `CLAIM-GUARDS.md`. |
| O6 | Bridge `dZ` to `dW = dZ^T X` and `dX_router = dZ W`. | `RealBackwardIdentities.lean`, `FORMAL-VALIDATION-REPORT.md`. |
| O7 | Reference `dWReal_adjoint` and `dXRouterReal_adjoint`. | `RealBackwardIdentities.lean`. |
| O8 | Do not exceed claim guards. | `CLAIM-GUARDS.md`, `EVIDENCE-MANIFEST.md`. |

## Selected Evidence

- `research/projects/mars/development/invoke-runs/20260614T083000Z-triton-appendix-proof-plan/WORK-PACK.md`
  - Shared claim guards: exact backward only for selected surrogate graph; hard `Top2` remains non-differentiable; Lean does not prove Triton/CUDA behavior.
- `research/projects/mars/development/invoke-runs/20260614T083000Z-triton-appendix-proof-plan/tasks/TASK-APPX-MATH.md`
  - Defines appendix write scope, required content, validation, and completion criteria.
- `research/projects/mars/papers/triton-top2-backward-kernel/paper.md`
  - Existing paper already states the hard-selection boundary and formal proof scope.
- `research/projects/mars/papers/triton-top2-backward-kernel/CLAIM-GUARDS.md`
  - Controls supported claims and non-claims.
- `research/projects/mars/papers/triton-top2-backward-kernel/EVIDENCE-MANIFEST.md`
  - Controls evidence identifiers and claim support rules.
- `research/projects/mars/papers/triton-top2-backward-kernel/formal/FORMAL-VALIDATION-REPORT.md`
  - Names the current Lean theorem slice and deferred obligations.
- `research/projects/mars/papers/triton-top2-backward-kernel/formal/TritonTop2/RealBackwardIdentities.lean`
  - Source of `logitsReal`, `dWReal`, `dXRouterReal`, `dWReal_adjoint`, and `dXRouterReal_adjoint`.

## Gate Result

No blocker-level decision was required. The safe path is to write a reader-facing appendix and cite it as explanatory paper evidence, not as a new proof result.

## Execution Boundary

This task may edit:

- `research/projects/mars/papers/triton-top2-backward-kernel/MATH-APPENDIX.md`
- `research/projects/mars/papers/triton-top2-backward-kernel/paper.md`
- `research/projects/mars/papers/triton-top2-backward-kernel/EVIDENCE-MANIFEST.md`
- selected task/session evidence files for synchronization

This task must not edit Lean theorem files.

