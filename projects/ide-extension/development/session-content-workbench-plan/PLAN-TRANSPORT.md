---
id: ide-extension-session-content-workbench-plan-transport
project: ide-extension
title: "Session Content Workbench Plan Transport"
status: pass
node_type: plan-transport
updatedAt: 2026-07-12
observed_capability: invoke
invoke_mode: plan
---

# Plan Transport: Session Content Workbench

## Provenance

| Field | Value |
| --- | --- |
| Observed capability | `invoke` |
| Mode | `plan` |
| Target owner | `projects/ide-extension` |
| Source design | `session-content-canvas-design/` refreshed and accepted |
| Refresh evidence | `session-content-workbench-refresh/REFRESH-REPORT.md` |
| Runtime mutation | none |
| Next owner | `task-session` |

## Context Selection

Selected context was limited to the refreshed design/decisions, current
`SPEC.md` and `ARCHITECTURE.md`, the implemented server/projector/storage/CLI/
workbench/test anchors, and the completed manual-session bridge plan patterns.

External research and subagents were skipped because the plan depends on local
brownfield contracts and already accepted product decisions.

## Template Selection

| Artifact | Selection | Reason |
| --- | --- | --- |
| Layering | standalone implementation layering | Required for V0-A/B/C promotion boundaries. |
| Work-pack | split work-pack | Nine SWUs cross contracts, kernel, CLI, UI, browser, and witnesses. |
| Execution pack | medium-complexity execution pack | Five sequential value waves need explicit gates. |
| Tasks/waves | split contracts | Each Task Session needs exact scope and evidence. |

## Dispatch Technique Trace

- Full dispatch: [session-content-workbench-plan.dispatch.json](session-content-workbench-plan.dispatch.json).
- Selected: `sequence`, `scu_swu_reduction`, `recomposition_proof`,
  `validation_loop`, `owner_boundary_check`, `handle_handoff`, `residue_ledger`,
  `execution_receipt_handoff`, `artifact_contract_bridge`,
  `state_namespace_boundary`, `concrete_path_evidence`, and
  `observability_grouping`.
- Full dispatch is required because Invoke, Distill, Task Session, kernel,
  browser, active Codex, and human witnesses cross lifecycle/evidence boundaries.
- Planning subagents: none. Runtime delegation requires a separate explicit gate.

## Distill

- Verdict: `pass`.
- First unit: `SWU-SCW-001`.
- Recomposition: contracts/replay -> manual display -> automatic update ->
  interaction return -> automated/live value proof.
- Main guardrail: do not build a generic secure platform before proving the
  trusted-local loop is useful.

## Validation

- Refreshed design dispatch: `VALIDATION=pass`.
- Plan dispatch: `VALIDATION=pass`.
- Artifact census: 23 files, five tasks, five waves, nine manifest SWUs, and
  nine uniquely expanded task SWUs.
- Local links: all 22 Markdown files pass.
- JSON, ASCII, and scoped whitespace checks: pass.
- Brownfield baseline: 12 runtime schemas, six module manifests, and 41 schema
  fixtures validate; 66/66 bridge tests pass; 4/4 desktop/mobile Playwright
  journeys pass.

## Handoff

```text
task-session to projects/ide-extension/development/session-content-workbench-plan/WORK-PACK.md --swu SWU-SCW-001
```
