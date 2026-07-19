---
id: ide-extension-workbench-ui-v1-work-pack
project: ide-extension
title: "Workbench UI V1 Work Pack"
status: planned
node_type: work-pack
updatedAt: 2026-07-17
planning_gate_status: pass
complexity: medium
output_mode: split
active_layer: L0
execution_pack_ref: EXECUTION-PACK.md
layering_artifact_ref: IMPLEMENTATION-LAYERING.md
distill_validation_status: pass
swu_atomicity_status: pass
first_unit_narrowness_status: pass
---

# Work Pack: Workbench UI V1

## Objective

Replace the proof-oriented page composition with one usable agent-task journey
while preserving all existing kernel, bridge, Canvas, Craft, and receipt
contracts.

## Source Contracts

- [Spec](SPEC.md)
- [Architecture bundle](ARCHITECTURE-BUNDLE.md)
- [UX plan](UX-PLAN.md)
- [Layering](IMPLEMENTATION-LAYERING.md)
- `projects/ide-extension/public/demo/l0.html`
- `projects/ide-extension/SPEC.md`
- `projects/ide-extension/development/operations-v1-plan/WORK-PACK.md`

## Task Board

| Task | Goal | Layer | Wave | Gate | Status |
| --- | --- | --- | --- | --- | --- |
| [TASK-WUI-001](work-pack/tasks/TASK-WUI-001-SHELL.md) | Establish the responsive product shell without changing run behavior. | L0 | [W0](work-pack/waves/W0.md) | pass | ready |
| [TASK-WUI-002](work-pack/tasks/TASK-WUI-002-COMPOSER.md) | Make Agent task/Dry run explicit and mode-safe. | L1 | [W1](work-pack/waves/W1.md) | dependency | planned |
| [TASK-WUI-003](work-pack/tasks/TASK-WUI-003-LIFECYCLE.md) | Project and present the run lifecycle with legal actions. | L1 | [W1](work-pack/waves/W1.md) | dependency | planned |
| [TASK-WUI-004](work-pack/tasks/TASK-WUI-004-WORKSPACE.md) | Compose Canvas, Craft sources, and evidence around the run. | L2 | [W2](work-pack/waves/W2.md) | dependency | planned |
| [TASK-WUI-005](work-pack/tasks/TASK-WUI-005-VALIDATE.md) | Run integrated UX evidence and human usefulness gate. | L3 | [W3](work-pack/waves/W3.md) | dependency + human | planned |

## SWU Manifest

| SWU | Parent | Primary Behavior | Dependencies | Independent Acceptance | Validation | Owner | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-WUI-001 | TASK-WUI-001 | Introduce semantic Work, Canvas, and Inspector regions. | none | landmarks exist while current behavior tests remain green | `npm run test:workbench` | local-fallback | ready |
| SWU-WUI-002 | TASK-WUI-001 | Arrange the three regions in a stable desktop grid. | 001 | desktop screenshot has no overlap, clipping, or unreachable controls | focused desktop Playwright | local-fallback | planned |
| SWU-WUI-003 | TASK-WUI-001 | Add mobile Work, Canvas, and Evidence navigation. | 002 | each view is reachable without duplicated state | focused mobile Playwright | local-fallback | planned |
| SWU-WUI-004 | TASK-WUI-002 | Make Agent task and Dry run explicit request modes. | 003 | both modes emit their intended payload and preserve invalid input | workbench tests plus two mode journeys | local-fallback | planned |
| SWU-WUI-005 | TASK-WUI-003 | Project raw bridge state into a pure `RunView`. | 004 | mapper fixtures cover every bridge typestate without DOM effects | mapper unit tests | local-fallback | planned |
| SWU-WUI-006 | TASK-WUI-003 | Render the ordered run timeline from `RunView`. | 005 | all lifecycle stages render with truthful labels | lifecycle Playwright states | local-fallback | planned |
| SWU-WUI-007 | TASK-WUI-003 | Resolve one legal primary action for each run state. | 005 | action matrix exposes no illegal or premature completion action | action resolver tests and journey | local-fallback | planned |
| SWU-WUI-008 | TASK-WUI-004 | Place retained Canvas output in the primary workspace. | 003 | revision identity and old-frame failure behavior remain intact | Canvas tests plus browser witness | local-fallback | planned |
| SWU-WUI-009 | TASK-WUI-004 | Seed composer fields from a Craft frontier selection. | 004 | selection fills task/context without mutating Craft | Craft API/UI tests | local-fallback | planned |
| SWU-WUI-010 | TASK-WUI-004 | Present receipt-linked run evidence in the Inspector. | 006,007 | receipt, validation, grants, context, and IDs remain attributable | receipt/evidence journey | local-fallback | planned |
| SWU-WUI-011 | TASK-WUI-005 | Validate the composed V1 and record the human verdict. | 008,009,010 | scoped matrix, retained screenshots, and explicit human verdict agree | Node/Playwright matrix plus Decision Gate | local-fallback-plus-human-review | planned |

## SWU Atomicity Review

| SWU | Candidate Child Units | Retained-Boundary Rationale | Verdict |
| --- | --- | --- | --- |
| 001 | one unit per landmark | landmarks form one semantic shell and share one accessibility oracle | pass |
| 002 | track sizing; panel placement | neither is independently useful without the resulting desktop grid | pass |
| 003 | one unit per mobile view | navigation is one state machine and one reachability oracle | pass |
| 004 | selector; validation; payload mapping | these are one request-mode decision and cannot be accepted separately | pass |
| 005 | envelope mapper; approval mapper; result mapper | all branches produce one pure `RunView` contract | pass |
| 006 | one unit per timeline stage | stages are fixtures of one ordered renderer | pass |
| 007 | action selection; overflow menu | both enforce one legal-action decision | pass |
| 008 | Canvas placement; revision label | revision identity is acceptance evidence for the placed Canvas | pass |
| 009 | task seed; context seed | both are fields of one read-only Craft selection event | pass |
| 010 | receipt; validation; grants; IDs | all are projections of one admitted evidence record | pass |
| 011 | machine matrix; human verdict | final promotion requires both and performs no product mutation | pass |

`SWU-WUI-001` is the narrowest reversible trust-building step: it changes only
semantic page regions and can be reverted without coupling desktop layout,
mobile navigation, projection logic, or request behavior.

## Gates

1. Do not change kernel authority to simplify UI code.
2. Do not infer request mode from an empty Skill value.
3. Do not label claimed work completed.
4. Do not expose task or requested skill through the ready-only poll projection.
5. Do not let Craft selection mutate its ledger.
6. Preserve the previously loaded Canvas revision on navigation failure.
7. Do not add provider, browser-control, IDE-host, or worker scope.
8. Do not make V1 the default claim until the human usefulness gate passes.

## Next Route

Task Session on `SWU-WUI-001`.
