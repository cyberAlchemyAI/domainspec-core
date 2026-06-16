# Run Manifest: Full Softmax Coordinate Derivative Refinement

Run id: `20260614T135903Z-softmax-coordinate-derivative-plan`

Status: `strategy_proposal_ready`

Target: `research/projects/mars/papers/triton-top2-backward-kernel/formal/TritonTop2/SoftmaxCoordinate.lean`

Operator request: refine the full step-by-step path to the softmax coordinate derivative, then invoke define/design/plan.

## Evidence Baseline

- `research/projects/mars/papers/triton-top2-backward-kernel/formal/TritonTop2/SoftmaxCoordinate.lean`
- `research/projects/mars/papers/triton-top2-backward-kernel/formal/SOFTMAX-COORDINATE-BLOCKER.md`
- `research/projects/mars/development/invoke-runs/20260614T102500Z-lean-softmax-cap2-proof-plan/WORK-PACK.md`
- `research/projects/mars/papers/triton-top2-backward-kernel/formal/FORMAL-VALIDATION-REPORT.md`
- `research/projects/mars/papers/triton-top2-backward-kernel/CLAIM-GUARDS.md`

## Run Boundary

- This run materializes the refine strategy proposal and dispatch route.
- It does not execute the ten-stage refine loop.
- It does not execute `invoke define`, `invoke design`, or `invoke plan`.
- It does not edit Lean theorem files.

## Planned Stage Evidence

| Stage | Owner | Status | Planned Artifact |
| --- | --- | --- | --- |
| Context Builder evidence baseline | `context-builder` | `pending_confirmation` | `stages/01-context-builder.md` |
| Invoke Define | `invoke` | `pending_confirmation` | `stages/02-invoke-define.md` |
| Interrogation refine-review | `interrogation` | `pending_confirmation` | `stages/03-refine-review.md` |
| Research decision | `refine` | `pending_confirmation` | `stages/04-research-decision.md` |
| Distill proof lanes | `distill` | `pending_confirmation` | `stages/05-distill.md` |
| Invoke Design | `invoke` | `pending_confirmation` | `stages/06-invoke-design.md` |
| Interrogation design review | `interrogation` | `pending_confirmation` | `stages/07-design-review.md` |
| Distill repair | `distill` | `pending_confirmation` | `stages/08-distill-repair.md` |
| Invoke Plan | `invoke` | `pending_confirmation` | `stages/09-invoke-plan.md`, `WORK-PACK.md`, `IMPLEMENTATION-LAYERING.md` |
| Final synthesis | `interrogation` + `refine` | `pending_confirmation` | `RESULT.md` |

## Proof Ladder To Preserve

1. Coordinate-line derivative primitive.
2. Numerator exponential derivative.
3. Denominator finite-sum derivative.
4. Quotient derivative for `softmaxCoord`.
5. Algebraic rewrite to `softmaxCoord z i * (basis k i - softmaxCoord z k)`.
6. Optional selected/non-selected coordinate corollaries.
7. Evidence and claim-guard sync.

## Current Gate

`G-001-confirm-before-runtime`: waiting for operator confirmation before executing the route.
