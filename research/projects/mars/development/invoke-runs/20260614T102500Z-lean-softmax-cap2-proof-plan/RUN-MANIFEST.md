# Invoke Run Manifest: Lean Softmax And CAP2 Proof Plan

Run id: `20260614T102500Z-lean-softmax-cap2-proof-plan`

Purpose: turn the refine result for Lean feasibility proofs into define, design, and plan artifacts with task-session-ready proof tasks.

Status: `ready_for_task_session`

Source anchors:

- Refine result: `research/projects/mars/development/refinement-runs/20260614T101000Z-lean-feasibility-proofs/RESULT.md`
- Softmax feasibility: `research/projects/mars/papers/triton-top2-backward-kernel/formal/SOFTMAX-PROOF-FEASIBILITY.md`
- CAP2 feasibility: `research/projects/mars/papers/triton-top2-backward-kernel/formal/CAP2-PROOF-FEASIBILITY.md`
- Current fixed-mask proof: `research/projects/mars/papers/triton-top2-backward-kernel/formal/TritonTop2/FixedMaskBackward.lean`
- Router real identities: `research/projects/mars/papers/triton-top2-backward-kernel/formal/TritonTop2/RealBackwardIdentities.lean`
- CAP2 candidate spec: `research/triton-top2-backward-kernel/CAP2-CANDIDATE-SPEC.md`
- CAP2 reference: `research/triton-top2-backward-kernel/CAP2-REFERENCE.md`
- CAP2 PyTorch reference: `research/triton-top2-backward-kernel/reference/router_torch.py`

Validation baseline:

```bash
cd research/projects/mars/papers/triton-top2-backward-kernel/formal
lake build
```

