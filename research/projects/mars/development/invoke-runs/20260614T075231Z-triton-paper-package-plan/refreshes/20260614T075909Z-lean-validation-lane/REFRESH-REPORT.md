# Refresh Report - Lean Validation Lane

Mode: `refresh`
Mutation mode: `apply-approved`
Status: `pass`

## Source Signals

| Signal ID | Type | Source | Claim | Confidence |
| --- | --- | --- | --- | --- |
| SIG-LEAN-001 | route_changed | user request | Add a Lean validation design and plan before paper drafting. | high |
| SIG-LEAN-002 | evidence_added | local tooling probe | `lean`, `lake`, and `elan` are already installed under local elan. | high |
| SIG-LEAN-003 | evidence_added | `research/triton-top2-backward-kernel/FORMAL-MATH-SPEC.md` | Existing formal proof targets already identify PO-004, PO-005, PO-006 and non-theorems. | high |
| SIG-LEAN-004 | artifact_drift | paper package plan | Previous plan had paper contract/draft path but no formal-boundary lane. | high |

## Applied Changes

- Added `LEAN-VALIDATION-DESIGN.md`.
- Added `LEAN-VALIDATION-PLAN.md`.
- Added `TASK-TTP-005L` for Lean setup and formal scope.
- Added `TASK-TTP-005M` for Lean boundary proof slice.
- Added `waves/W1L-LEAN.md`.
- Updated `WORK-PACK.md` so `TASK-TTP-006` depends on Lean validation.
- Updated `INVOKE-DESIGN.md`, `INVOKE-PLAN.md`, and
  `IMPLEMENTATION-LAYERING.md` with formal-boundary gates.
- Updated affected task contracts so Lean statuses are tested and reviewed.
- Updated `RUN-MANIFEST.md` and `evidence-index.json`.

## Local Tooling Evidence

```text
Lean 4.30.0
Lake 5.0.0-src+d024af0
elan 4.2.2
```

## Claim Boundary

Lean validation may support:

- formal boundary clarity;
- fixed-mask/fixed-load assumptions;
- finite-sum router algebra proof targets;
- paper claims about what is inside and outside the differentiable graph.

Lean validation must not be used as evidence for:

- Triton implementation correctness;
- FP16 numerical correctness;
- GPU memory allocation behavior;
- production performance;
- hard Top2 differentiability.

## Next Route

The first executable task remains:

```text
task-session to research/projects/mars/development/invoke-runs/20260614T075231Z-triton-paper-package-plan/WORK-PACK.md --task TASK-TTP-001
```

Lean tasks run after `TASK-TTP-005`:

```text
task-session to research/projects/mars/development/invoke-runs/20260614T075231Z-triton-paper-package-plan/WORK-PACK.md --task TASK-TTP-005L
```

