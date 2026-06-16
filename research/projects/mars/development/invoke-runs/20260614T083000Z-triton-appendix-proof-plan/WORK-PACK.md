# Work-Pack: Triton Top2 Appendix And Proof Plan

Status: `complete`

Next ready task: `none`

## Goal

Turn the existing Triton Top2 paper package into a more defensible research artifact by adding a math appendix, expanding formal proof coverage where tractable, and running a final skeptical review.

## Execution Order

1. `TASK-APPX-MATH`: write the math appendix and link it from the paper. `complete`
2. `TASK-PROOF-FIXED-MASK`: add the fixed-mask relaxed backward theorem slice. `complete`
3. `TASK-PROOF-SOFTMAX`: attempt or scope the softmax derivative theorem. `complete_feasibility_fallback`
4. `TASK-PROOF-CAP2`: attempt or scope CAP2 fixed-load derivative pieces. `complete_feasibility_fallback`
5. `TASK-PAPER-REVIEW`: run the reviewer pass against updated paper/evidence. `complete`
6. `TASK-CLOSURE`: synchronize manifests, reports, and presentation package. `complete`

## Shared Claim Guards

- "Exact backward" means exact for the selected surrogate graph.
- Hard `Top2` selection remains non-differentiable.
- Fixed-mask proof does not imply differentiability through mask selection.
- Softmax proof does not imply CAP2 or end-to-end routing correctness.
- CAP2 fixed-load derivative pieces do not imply novelty.
- Lean proofs do not prove Triton/CUDA implementation correctness.
- FP16 behavior remains empirical unless separately proved.

## Shared Validation

Lean validation:

```bash
cd research/projects/mars/papers/triton-top2-backward-kernel/formal
lake build
```

Paper validation:

```bash
rg -n "hard Top2|exact backward|Lean|CAP2|FP16" research/projects/mars/papers/triton-top2-backward-kernel
```

Dispatch validation:

```bash
.agents/skills/dispatch-spec/scripts/validate-dispatch.py research/projects/mars/development/dispatches/20260614T083000Z-triton-appendix-proof-strategy.dispatch.json
```

## Stop Conditions

- Stop if a task would require broad formal infrastructure not named in the task.
- Stop if a draft claim implies hard `Top2` differentiability.
- Stop if a proof task cannot be validated with `lake build` and no feasibility report is produced.
- Stop before spawning subagents unless explicitly authorized.
