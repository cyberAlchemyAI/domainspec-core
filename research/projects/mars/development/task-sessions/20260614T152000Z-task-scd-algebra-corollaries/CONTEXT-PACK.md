# Context Pack: TASK-SCD-ALGEBRA-COROLLARIES

Task: `TASK-SCD-ALGEBRA-COROLLARIES`

Mode: `lean`

Strict coverage: `pass`

## Obligations

| Obligation | Status | Evidence |
| --- | --- | --- |
| Dependency complete | covered | `softmaxCoord_coordLine_hasDerivAt_raw` builds. |
| Normalize derivative | covered | Target theorem `softmaxCoord_coordLine_hasDerivAt`. |
| Decide optional corollaries | resolved | Deferred; normalized theorem specializes through `basis`. |
| Keep claim boundary | covered | No hard Top2 or full Jacobian claim introduced. |

## Validation Surface

```bash
cd research/projects/mars/papers/triton-top2-backward-kernel/formal
lake build
```
