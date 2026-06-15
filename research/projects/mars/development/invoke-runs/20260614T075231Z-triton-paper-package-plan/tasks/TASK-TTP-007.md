# TASK-TTP-007 - Paper Draft

Status: `pending`
Layer: L2

## Objective

Draft `paper.md` from the paper spec, stories, test spec, and data appendix.

## Write Scope

- `research/projects/mars/papers/triton-top2-backward-kernel/paper.md`

## Implementation Detail

Write prose in the section order from `PAPER-SPEC.md`, including a dedicated
formal-boundary validation section if Lean validation was completed or a clearly
labeled deferral if it was not.

Each section must include source/evidence links. Use the supported public framing:

```text
Implemented a Triton-backed exact backward path for a fixed-load continuous
Top2 routing relaxation, with PyTorch/manual VJP parity, finite-difference
checks, and RunPod CUDA validation.
```

Avoid novelty and hard Top2 differentiability claims.

## Smallest Working Units

| SWU ID | Goal | Done Criteria | Verification |
| --- | --- | --- | --- |
| SWU-TTP-007A | Draft paper. | `paper.md` has all planned sections and evidence links. | `test -f .../paper.md` |
