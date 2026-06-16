# Invoke Run Manifest: Triton Appendix And Proof Plan

Run id: `20260614T083000Z-triton-appendix-proof-plan`

Purpose: define, design, and plan the next paper phase for the Triton Top2 backward kernel package: math appendix, fixed-mask proof, softmax derivative proof lane, CAP2 proof lane, and a skeptical paper-review pass.

Status: `strategy_ready`

Source anchors:

- Paper package: `research/projects/mars/papers/triton-top2-backward-kernel/`
- Current paper: `research/projects/mars/papers/triton-top2-backward-kernel/paper.md`
- Claim guards: `research/projects/mars/papers/triton-top2-backward-kernel/CLAIM-GUARDS.md`
- Evidence manifest: `research/projects/mars/papers/triton-top2-backward-kernel/EVIDENCE-MANIFEST.md`
- Formal report: `research/projects/mars/papers/triton-top2-backward-kernel/formal/FORMAL-VALIDATION-REPORT.md`
- Current Lean entrypoint: `research/projects/mars/papers/triton-top2-backward-kernel/formal/TritonTop2.lean`
- Current real identities: `research/projects/mars/papers/triton-top2-backward-kernel/formal/TritonTop2/RealBackwardIdentities.lean`
- Dispatch strategy: `research/projects/mars/development/dispatches/20260614T083000Z-triton-appendix-proof-strategy.dispatch.json`
- Refine proposal: `research/projects/mars/development/refinement-runs/20260614T083000Z-triton-appendix-proof-refine/RESULT.md`

Validation policy:

- Every Lean task must end with `cd research/projects/mars/papers/triton-top2-backward-kernel/formal && lake build`.
- Every paper task must update evidence links or explicitly state that no evidence index mutation was needed.
- No task may claim hard Top2 differentiability, Triton kernel correctness proof, FP16 numerical proof, or CAP2 novelty unless a new validated artifact proves it.

