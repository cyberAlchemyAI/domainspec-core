# Execution Pack: Interface Workbench Rework

## Planning Control

| Field | Value |
| --- | --- |
| planningGateStatus | block-pending-plan-repair-redistill-and-swu-selection |
| complexity | medium |
| baselineWave | W0 |
| activePlanRef | `WORK-PACK.md` |
| workPackManifest | `WORK-PACK.md` |
| layeringArtifact | `IMPLEMENTATION-LAYERING.md` |
| specRef | `SPEC.md` |
| activeLayerWindow | L0 |
| readinessProfile | pilot |
| selectedSWU | none |

## Wave Choreography

| Wave | Layer | Question | SWUs/tasks | Entry | Exit |
| --- | --- | --- | --- | --- | --- |
| [W0](work-pack/waves/W0.md) | L0 | Is projection identity coherent and reproducible? | SWU-UPW-001–003 / TASK-UPW-PROJECTION | Design pass | version/snapshot/state receipts |
| [W1](work-pack/waves/W1.md) | L0 | Can stable refresh preserve governed work? | SWU-UPW-004–007 / TASK-UPW-COORDINATOR | W0 pass | inert/trailing/rollback/context receipts |
| [W2](work-pack/waves/W2.md) | L1 | Do six regions recompose without coarse rerender? | SWU-UPW-008–013 / TASK-UPW-REGIONS | W1 pass | six region receipts |
| [W3](work-pack/waves/W3.md) | L1 | Does mobile order and copy preserve the active task? | SWU-UPW-014–015 / TASK-UPW-RESPONSIVE-COPY | W2 pass | responsive and copy receipts |
| [W4](work-pack/waves/W4.md) | L2 | Do bounded semantics and security fail correctly? | SWU-UPW-016–017 / TASK-UPW-HARDENING | W3 pass | accessibility/security receipts |
| [W5](work-pack/waves/W5.md) | L2 | Does the whole workbench close without regression? | TASK-UPW-VERIFY exemption | W4 pass | full-suite and audit receipts |

## Parallelization Boundary

Mutation is serial. Multiple SWUs touch `studio.ts`,
`interface/workbench-shell.ts`, or the same E2E fixtures; shared files do not
justify a parallel merge. A future Task Session executes exactly one selected
SWU and synchronizes its receipt before any successor becomes a candidate.

## Closure

W5 may close the implementation evidence cycle but cannot admit L3, select a
human study, certify accessibility, or authorize release.

## Current Owner

This pack is not eligible for Task Session. `invoke plan` must first repair
PD-01–10, including the SWU-UPW-016/017 splits and regenerated wave
choreography. A fresh governed Plan Distill pass and explicit SWU selection are
later, separate gates.
