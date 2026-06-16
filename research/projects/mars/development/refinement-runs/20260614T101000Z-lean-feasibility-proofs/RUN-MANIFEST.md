# Run Manifest: Lean Feasibility Proof Refinement

Run id: `20260614T101000Z-lean-feasibility-proofs`

Target: `research/projects/mars/papers/triton-top2-backward-kernel/formal/`

Operator question: if we want to turn the softmax and CAP2 feasibility reports into Lean proofs, what would it take?

Preset: `standard`

Research mode: `research-if-gap-appears`

Status: `strategy_proposal_ready`

Primary evidence:

- `formal/SOFTMAX-PROOF-FEASIBILITY.md`
- `formal/CAP2-PROOF-FEASIBILITY.md`
- `formal/TritonTop2/FixedMaskBackward.lean`
- `formal/TritonTop2/RealBackwardIdentities.lean`
- `formal/FORMAL-VALIDATION-REPORT.md`
- `research/projects/mars/development/invoke-runs/20260614T083000Z-triton-appendix-proof-plan/WORK-PACK.md`

Run boundary:

- This refinement does not implement new Lean theorem files.
- It defines what a rigorous proof program would require.
- It preserves current claim guards: no hard `Top2` differentiability, no Triton/CUDA formal proof, no CAP2 novelty claim.

