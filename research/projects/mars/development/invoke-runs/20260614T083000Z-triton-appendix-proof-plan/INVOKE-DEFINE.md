# Invoke Define: Appendix And Proof Lanes

## Objective

Prepare an execution-ready work-pack for the next rigorous paper phase without expanding claims beyond the current evidence.

The phase has five lanes:

1. `APPX-MATH`: write a reader-facing math appendix that connects the challenge expression to the current Lean-backed router-adjoint identities.
2. `PROOF-FIXED-MASK`: formalize the exact backward pass for the fixed-mask relaxed graph, where selection is treated as constant data.
3. `PROOF-SOFTMAX`: determine and, if tractable, formalize the finite softmax derivative theorem needed by the relaxed router story.
4. `PROOF-CAP2`: determine and, if tractable, formalize CAP2 fixed-load derivative pieces without claiming novelty or end-to-end routing proof.
5. `PAPER-REVIEW`: run a skeptical review pass over the paper package after appendix and proof updates.

## Non-Goals

- Do not prove differentiability of hard `Top2`.
- Do not claim the Lean model proves Triton/CUDA implementation correctness.
- Do not claim FP16 numerical stability is formally proved.
- Do not claim CAP2 is novel unless separate prior-art review establishes it.
- Do not force softmax or CAP2 proofs if Mathlib scope makes them disproportionate; in that case produce a precise feasibility report.

## Required Outputs

- `WORK-PACK.md`: execution order and task-session handoff.
- `IMPLEMENTATION-LAYERING.md`: dependency and risk layering.
- `tasks/TASK-APPX-MATH.md`
- `tasks/TASK-PROOF-FIXED-MASK.md`
- `tasks/TASK-PROOF-SOFTMAX.md`
- `tasks/TASK-PROOF-CAP2.md`
- `tasks/TASK-PAPER-REVIEW.md`
- `tasks/TASK-CLOSURE.md`

## Acceptance Standard

The plan is acceptable when each lane has:

- A write scope.
- A smallest useful work unit.
- A validation command.
- A claim boundary.
- A fallback if proof implementation is blocked.

