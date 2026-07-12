---
id: ide-extension-v0-canvas-repair-plan-transport
project: ide-extension
title: "V0 Canvas Repair Plan Transport"
status: pass
node_type: plan-transport
updatedAt: 2026-07-12
observed_capability: invoke
invoke_mode: plan
---

# Plan Transport: V0 Canvas Repair

## Provenance

| Field | Value |
| --- | --- |
| Observed capability | `invoke` |
| Mode | `plan` |
| Target | Current V0 canvas issue repair |
| Lifecycle owner | `projects/ide-extension` |
| Approved design refs | Existing session-content canvas design plus accepted architecture review |
| Runtime mutation | none |
| Next owner | `task-session` |

## Template Selection

- Standalone implementation layering: required for every plan.
- Split work-pack: required because the plan has more than two artifacts and
  spans policy, kernel/server, tests, and closure evidence.
- Execution pack: required for medium-complexity wave and SWU handoff.

## Dispatch Technique Trace

| Technique | Effect on plan |
| --- | --- |
| `sequence` | Policy, admission, adversarial proof, and closure execute in order. |
| `scu_swu_reduction` | Four independently verifiable SWUs replace a broad "fix canvas" task. |
| `recomposition_proof` | Distill maps every retained review obligation to SWU evidence. |
| `validation_loop` | Every slice has focused and inherited validation. |
| `owner_boundary_check` | Invoke plans; Task Session executes one SWU. |
| `handle_handoff` | Runtime workers consume source and task handles, not copied files. |
| `residue_ledger` | Portable race limits, Operations V1, and dirty-worktree handling remain explicit. |
| `execution_receipt_handoff` | Every SWU must return files, validation, blockers, residue, and reroute. |
| `concrete_path_evidence` | Review, source, tests, and task contracts use exact paths. |
| `authority_split_gate` | Preview/display exception cannot authorize protected effects. |
| `observability_grouping` | Plan output and later SWUs remain distinguishable. |

Full dispatch: [v0-canvas-repair-plan.dispatch.json](v0-canvas-repair-plan.dispatch.json).

## Gate Result

- Approved design references: `pass`.
- Layering and split work-pack: `pass`.
- Implementation detail: `pass`.
- SWU coverage: `4/4 complete`.
- Distill: `pass`, zero blocking gaps.
- Mutation authority: not exercised.

## Next Route

`task-session` on `SWU-VCR-001` only.
