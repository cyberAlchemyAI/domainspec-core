# Work-Pack: Lean Softmax And CAP2 Proofs

Status: `complete_with_softmax_derivative_blocker`

Next ready task: `none`

## Objective

Execute the next formal proof ladder for the Triton Top2 paper package:

1. prove finite softmax foundations;
2. prove finite softmax coordinate derivative;
3. freeze CAP2-v0 definitions in Lean;
4. prove one fixed-load CAP2 theorem slice;
5. synchronize paper evidence and claim guards.

## Task Board

| Task | Status | Layer | Contract |
| --- | --- | --- | --- |
| `TASK-SOFTMAX-FOUNDATION` | complete | L0 | `tasks/TASK-SOFTMAX-FOUNDATION.md` |
| `TASK-SOFTMAX-COORD-DERIVATIVE` | blocked_after_foundation | L1 | `tasks/TASK-SOFTMAX-COORD-DERIVATIVE.md` |
| `TASK-CAP2-DEFINITION` | complete | L2 | `tasks/TASK-CAP2-DEFINITION.md` |
| `TASK-CAP2-FIXED-LOAD-SCALAR` | complete | L3 | `tasks/TASK-CAP2-FIXED-LOAD-SCALAR.md` |
| `TASK-PAPER-SYNC` | complete | L3 | `tasks/TASK-PAPER-SYNC.md` |

## SWU Manifest

| SWU | Parent Task | Goal | Owner | Verification |
| --- | --- | --- | --- | --- |
| `SWU-LSP-001` | `TASK-SOFTMAX-FOUNDATION` | Add softmax finite-vector definitions. | local-fallback | `lake build` |
| `SWU-LSP-002` | `TASK-SOFTMAX-FOUNDATION` | Prove denominator positivity. | local-fallback | `lake build` |
| `SWU-LSP-003` | `TASK-SOFTMAX-COORD-DERIVATIVE` | Prove coordinate-line support lemmas. | local-fallback | `lake build` |
| `SWU-LSP-004` | `TASK-SOFTMAX-COORD-DERIVATIVE` | Prove coordinate derivative or produce blocker report. | local-fallback | `lake build` or blocker report |
| `SWU-LSP-005` | `TASK-CAP2-DEFINITION` | Add CAP2-v0 definitions matching source evidence. | local-fallback | `lake build` |
| `SWU-LSP-006` | `TASK-CAP2-DEFINITION` | Add fixed-load boundary lemmas. | local-fallback | `lake build` |
| `SWU-LSP-007` | `TASK-CAP2-FIXED-LOAD-SCALAR` | Prove first fixed-load scalar theorem or blocker report. | local-fallback | `lake build` or blocker report |
| `SWU-LSP-008` | `TASK-PAPER-SYNC` | Sync formal report, evidence manifest, claim guards, and review. | local-fallback | `rg` review checks |

## Shared Claim Guards

- No hard `Top2` differentiability claim.
- No Triton/CUDA correctness proof claim.
- No FP16 formal proof claim.
- No CAP2 novelty claim.
- No dynamic-load gradient claim unless a theorem explicitly proves it.

## Shared Source Anchors

- `research/projects/mars/development/refinement-runs/20260614T101000Z-lean-feasibility-proofs/RESULT.md`
- `research/projects/mars/papers/triton-top2-backward-kernel/formal/SOFTMAX-PROOF-FEASIBILITY.md`
- `research/projects/mars/papers/triton-top2-backward-kernel/formal/CAP2-PROOF-FEASIBILITY.md`
- `research/triton-top2-backward-kernel/CAP2-CANDIDATE-SPEC.md`
- `research/triton-top2-backward-kernel/CAP2-REFERENCE.md`
- `research/triton-top2-backward-kernel/reference/router_torch.py`

## Stop Conditions

- Stop if a theorem requires a representation change; record the exact blocker.
- Stop if CAP2 definitions diverge from source evidence.
- Stop if proof text implies dynamic load gradients or CAP2 novelty.
- Stop if `lake build` fails after bounded repair.
