# Work Pack - Mathlib Formal Hardening

Status: `complete`
Owner: `research/projects/mars`

## Objective

Add Mathlib-backed formal hardening to the Triton Top2 paper package and update
the paper evidence so it can honestly cite stronger real-valued Lean theorems.

## Output Root

`research/projects/mars/papers/triton-top2-backward-kernel/`

## Task Matrix

| Task ID | Wave | Objective | Dependencies | Status | Validation |
| --- | --- | --- | --- | --- | --- |
| [TASK-MFH-001](tasks/TASK-MFH-001.md) | W0 | Pin Mathlib and add real-valued theorem module. | none | pass | `lake build` |
| [TASK-MFH-002](tasks/TASK-MFH-002.md) | W1 | Update formal report and paper-facing claim artifacts. | TASK-MFH-001 | pass | report/review consistency check |
| [TASK-MFH-003](tasks/TASK-MFH-003.md) | W2 | Close validation receipt and synchronize work-pack status. | TASK-MFH-002 | pass | JSON and work-pack review |

## SWU Manifest

| SWU ID | Parent Task | Goal | Write Scope | Verification |
| --- | --- | --- | --- | --- |
| SWU-MFH-001A | TASK-MFH-001 | Convert Lake project to Mathlib-enabled configuration. | `formal/` | `lake update` and `lake build` |
| SWU-MFH-001B | TASK-MFH-001 | Prove real-valued dW and dX-router adjoint identities. | `formal/TritonTop2/*.lean` | `lake build` |
| SWU-MFH-002A | TASK-MFH-002 | Update formal validation report. | `formal/FORMAL-VALIDATION-REPORT.md` | report includes proved/deferred table |
| SWU-MFH-002B | TASK-MFH-002 | Update paper, claim guards, test spec, and review. | paper package markdown | no unsupported claim escalation |
| SWU-MFH-003A | TASK-MFH-003 | Record task-session evidence and final status. | invoke/task-session artifacts | JSON validates |

## Source Anchors

- `research/projects/mars/papers/triton-top2-backward-kernel/formal/`
- `research/projects/mars/papers/triton-top2-backward-kernel/formal/FORMAL-VALIDATION-REPORT.md`
- `research/projects/mars/papers/triton-top2-backward-kernel/paper.md`
- `research/projects/mars/papers/triton-top2-backward-kernel/CLAIM-GUARDS.md`
- `research/projects/mars/papers/triton-top2-backward-kernel/PAPER-REVIEW.md`

## Gates

- G1: Mathlib dependency must match Lean 4.30.0.
- G2: `lake build` must pass.
- G3: paper claims must say real-valued router adjoint identities, not full CAP2/Triton proof.
- G4: deferred obligations must remain visible.

## Current State

Next ready task: none.

Execution receipt:
`research/projects/mars/development/task-sessions/20260614T081415Z-mathlib-formal-hardening/RESULT.md`.
