# TASK-PAPER-SYNC

Status: `complete`

Layer: L3

## Purpose

Synchronize paper evidence after proof attempts.

## Write Scope

- `research/projects/mars/papers/triton-top2-backward-kernel/formal/FORMAL-VALIDATION-REPORT.md`
- `research/projects/mars/papers/triton-top2-backward-kernel/EVIDENCE-MANIFEST.md`
- `research/projects/mars/papers/triton-top2-backward-kernel/CLAIM-GUARDS.md`
- `research/projects/mars/papers/triton-top2-backward-kernel/PAPER-REVIEW.md`
- this invoke run's `evidence-index.json`

## Smallest Working Unit

### SWU-LSP-008

Goal: update paper-facing evidence and claim guards from the actual proof results.

Validation:

```bash
rg -n "softmaxCoord|CAP2Definition|dynamic load|novel|Top2|Lean" research/projects/mars/papers/triton-top2-backward-kernel
```

## Done Criteria

- Completed proof files or blocker reports are represented in the evidence manifest.
- Claim guards prevent overclaiming.
- Paper review names residual risks.

## Completion Evidence

- Formal report: `research/projects/mars/papers/triton-top2-backward-kernel/formal/FORMAL-VALIDATION-REPORT.md`
- Evidence manifest: `research/projects/mars/papers/triton-top2-backward-kernel/EVIDENCE-MANIFEST.md`
- Claim guards: `research/projects/mars/papers/triton-top2-backward-kernel/CLAIM-GUARDS.md`
- Session result: `research/projects/mars/development/task-sessions/20260614T111000Z-task-paper-sync/RESULT.md`
