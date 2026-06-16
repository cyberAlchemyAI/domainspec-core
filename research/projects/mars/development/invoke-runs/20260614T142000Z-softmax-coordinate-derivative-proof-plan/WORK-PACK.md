# Work-Pack: Softmax Coordinate Derivative Proof

Status: `complete`

Next ready task: `none`

## Objective

Prove the full finite softmax coordinate derivative in Lean, starting from the existing softmax foundation.

## Task Board

| Task | Status | Layer | Contract |
| --- | --- | --- | --- |
| `TASK-SCD-LINE-DERIVATIVE` | complete | L0 | `tasks/TASK-SCD-LINE-DERIVATIVE.md` |
| `TASK-SCD-NUMERATOR-DERIVATIVE` | complete | L0 | `tasks/TASK-SCD-NUMERATOR-DERIVATIVE.md` |
| `TASK-SCD-DENOMINATOR-DERIVATIVE` | complete | L1 | `tasks/TASK-SCD-DENOMINATOR-DERIVATIVE.md` |
| `TASK-SCD-QUOTIENT-DERIVATIVE` | complete | L2 | `tasks/TASK-SCD-QUOTIENT-DERIVATIVE.md` |
| `TASK-SCD-ALGEBRA-COROLLARIES` | complete | L3 | `tasks/TASK-SCD-ALGEBRA-COROLLARIES.md` |
| `TASK-SCD-PAPER-SYNC` | complete | L3 | `tasks/TASK-SCD-PAPER-SYNC.md` |

## SWU Manifest

| SWU | Parent Task | Goal | Owner | Verification |
| --- | --- | --- | --- | --- |
| `SWU-SCD-001` | `TASK-SCD-LINE-DERIVATIVE` | Add calculus imports and prove coordinate-line derivative. | local-fallback | `lake build` |
| `SWU-SCD-002` | `TASK-SCD-NUMERATOR-DERIVATIVE` | Prove exponential numerator derivative along `coordLine`. | local-fallback | `lake build` |
| `SWU-SCD-003` | `TASK-SCD-DENOMINATOR-DERIVATIVE` | Prove denominator finite-sum derivative along `coordLine`. | local-fallback | `lake build` |
| `SWU-SCD-004` | `TASK-SCD-QUOTIENT-DERIVATIVE` | Prove raw quotient derivative for `softmaxCoord`. | local-fallback | `lake build` or blocker report |
| `SWU-SCD-005` | `TASK-SCD-ALGEBRA-COROLLARIES` | Normalize raw quotient derivative to paper-facing expression. | local-fallback | `lake build` or blocker report |
| `SWU-SCD-006` | `TASK-SCD-PAPER-SYNC` | Sync formal report, evidence manifest, claim guards, and paper text. | local-fallback | `rg` review checks |

## Shared Write Scope

- `research/projects/mars/papers/triton-top2-backward-kernel/formal/TritonTop2/SoftmaxCoordinate.lean`
- optional blocker file under `research/projects/mars/papers/triton-top2-backward-kernel/formal/`
- paper evidence files only in `TASK-SCD-PAPER-SYNC`
- this invoke run's `WORK-PACK.md`, task files, evidence index, and task-session result links

## Shared Claim Guards

- No hard `Top2` differentiability claim.
- No Triton/CUDA formal proof claim.
- No FP16 formal proof claim.
- No CAP2 novelty claim.
- No paper sync claim until `lake build` proves the theorem.

## Shared Source Anchors

- `research/projects/mars/development/refinement-runs/20260614T135903Z-softmax-coordinate-derivative-plan/REFINE-SEED-PROPOSAL.md`
- `research/projects/mars/papers/triton-top2-backward-kernel/formal/TritonTop2/SoftmaxCoordinate.lean`
- `research/projects/mars/papers/triton-top2-backward-kernel/formal/SOFTMAX-COORDINATE-BLOCKER.md`
- `research/projects/mars/papers/triton-top2-backward-kernel/formal/FORMAL-VALIDATION-REPORT.md`

## Stop Conditions

- Stop if a theorem requires changing existing definitions; record the exact blocker.
- Stop if `lake build` fails after bounded repair.
- Stop if a proof statement would overclaim hard `Top2` differentiability.
- Stop if a task cannot preserve completed earlier proof lemmas.
