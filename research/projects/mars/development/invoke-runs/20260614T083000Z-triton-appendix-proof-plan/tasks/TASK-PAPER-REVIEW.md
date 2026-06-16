# TASK-PAPER-REVIEW: Skeptical Paper Review

Status: `complete`

## Purpose

Review the paper package as if a skeptical reader is looking for overclaims, missing evidence, or unclear proof boundaries.

## Write Scope

- Update `research/projects/mars/papers/triton-top2-backward-kernel/PAPER-REVIEW.md`.
- Update `CLAIM-GUARDS.md` only if new claim boundaries are discovered.
- Update `PAPER-TEST-SPEC.md` if new validation expectations are added.

## Review Questions

- Does the paper clearly say hard `Top2` is not differentiated?
- Does every formal claim point to a Lean file or formal report entry?
- Does every empirical claim point to a test or run artifact?
- Does the paper avoid novelty claims for CAP2 unless proven separately?
- Does the paper separate CUDA/Triton correctness evidence from Lean algebra proof?

## Validation

```bash
rg -n "novel|exact|Top2|Lean|Triton|CUDA|CAP2|FP16" research/projects/mars/papers/triton-top2-backward-kernel
```

## Completion Criteria

- No unresolved high-severity overclaim remains.
- Review file names every residual risk.

## Completion Evidence

- Review: `research/projects/mars/papers/triton-top2-backward-kernel/PAPER-REVIEW.md`
- Test spec: `research/projects/mars/papers/triton-top2-backward-kernel/PAPER-TEST-SPEC.md`
- Session result: `research/projects/mars/development/task-sessions/20260614T094000Z-task-paper-review/RESULT.md`
