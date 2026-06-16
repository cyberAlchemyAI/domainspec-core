# Run Manifest: Softmax Coordinate Derivative Proof Plan

Run id: `20260614T142000Z-softmax-coordinate-derivative-proof-plan`

Status: `complete`

Target artifact: `research/projects/mars/papers/triton-top2-backward-kernel/formal/TritonTop2/SoftmaxCoordinate.lean`

Parent refine route: `research/projects/mars/development/refinement-runs/20260614T135903Z-softmax-coordinate-derivative-plan/REFINE-DISPATCH.json`

## Objective

Author the `invoke define`, `invoke design`, and `invoke plan` route for proving the full finite softmax coordinate derivative in Lean.

## Outputs

- `INVOKE-DEFINE.md`
- `INVOKE-DESIGN.md`
- `INVOKE-PLAN.md`
- `IMPLEMENTATION-LAYERING.md`
- `WORK-PACK.md`
- `tasks/`
- `waves/`
- `evidence-index.json`

## Source Evidence

- `research/projects/mars/development/refinement-runs/20260614T135903Z-softmax-coordinate-derivative-plan/REFINE-SEED-PROPOSAL.md`
- `research/projects/mars/development/refinement-runs/20260614T135903Z-softmax-coordinate-derivative-plan/REFINE-DISPATCH.json`
- `research/projects/mars/papers/triton-top2-backward-kernel/formal/TritonTop2/SoftmaxCoordinate.lean`
- `research/projects/mars/papers/triton-top2-backward-kernel/formal/SOFTMAX-COORDINATE-BLOCKER.md`
- `research/projects/mars/development/invoke-runs/20260614T102500Z-lean-softmax-cap2-proof-plan/WORK-PACK.md`

## Claim Boundary

- This plan targets finite softmax only.
- It does not claim hard `Top2` differentiability.
- It does not claim Triton/CUDA formal correctness.
- It does not claim FP16 formal proof.
- It does not modify CAP2 claims.

## Validation

- `jq empty evidence-index.json`
- `rg` marker checks for task IDs, SWU IDs, theorem names, and claim guards.
- Future execution validation: `cd research/projects/mars/papers/triton-top2-backward-kernel/formal && lake build`

Final validation:

- `lake build`: pass, `Build completed successfully (3044 jobs)`.
- `evidence-index.json`: pass.
- paper/evidence marker scan: pass.
