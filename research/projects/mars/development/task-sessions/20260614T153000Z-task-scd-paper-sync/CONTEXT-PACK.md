# Context Pack: TASK-SCD-PAPER-SYNC

Task: `TASK-SCD-PAPER-SYNC`

Mode: `lean`

Strict coverage: `pass`

## Obligations

| Obligation | Status | Evidence |
| --- | --- | --- |
| Dependency complete | covered | `softmaxCoord_coordLine_hasDerivAt` builds. |
| Sync formal report | covered | `FORMAL-VALIDATION-REPORT.md`. |
| Sync evidence and guards | covered | `EVIDENCE-MANIFEST.md`, `CLAIM-GUARDS.md`. |
| Sync paper package | covered | `paper.md`, `PAPER-REVIEW.md`, `PAPER-TEST-SPEC.md`, `PRESENTATION-PACKAGE.md`. |
| Preserve non-claims | covered | No hard Top2, CUDA, FP16, or full CAP2 calculus claim introduced. |

## Validation Surface

```bash
rg -n "softmaxCoord_coordLine_hasDerivAt|EV-FORMAL-010|NC-010|finite softmax coordinate" research/projects/mars/papers/triton-top2-backward-kernel
```
