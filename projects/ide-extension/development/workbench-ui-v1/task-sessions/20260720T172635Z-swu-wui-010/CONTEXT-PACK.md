# Context Pack: SWU-WUI-010

- Task: `SWU-WUI-010` - Evidence Inspector
- Parent: `TASK-WUI-004` - Canvas, Craft, And Evidence
- Mode: standard
- Runtime: local Node and Playwright Chromium
- Dependency receipts:
  - [SWU-WUI-006 PASS](../20260720T162753Z-swu-wui-006/TASK-SESSION-RESULT.md)
  - [SWU-WUI-007 PASS](../20260720T164437Z-swu-wui-007/TASK-SESSION-RESULT.md)
  - [SWU-WUI-009 PASS](../20260720T170841Z-swu-wui-009/TASK-SESSION-RESULT.md)
- Gate verdict: pass; the current detail and evidence projections already carry
  the required receipt-linked metadata, so implementation must begin with a
  focused retained-receipt journey rather than a new server route

## Obligation Matrix

| ID | Obligation | Status | Controlling evidence |
| --- | --- | --- | --- |
| A1 | Execute exactly `SWU-WUI-010` after the completed Craft seed boundary. | covered | Work Pack, WUI-009 receipt |
| A2 | Consume existing proposal detail, receipt, and evidence read projections without mutating kernel authority. | covered | server detail/evidence routes, architecture boundary |
| A3 | Keep authorization and execution receipts visibly distinct. | covered | receipt projection, run timeline, bridge journey |
| A4 | Keep receipt, evidence artifact, envelope, run, and approval identifiers attributable to one admitted run. | covered | proposal detail and evidence routes |
| A5 | Present validation, requested grants, context refs, result summary, and source evidence in the Inspector. | covered | current detail/evidence renderer, result schema |
| A6 | Keep ready-for-poll metadata opaque before claim and never treat chat output as terminal completion. | covered | bridge safe fields, Work Pack gates, bridge tests |
| A7 | Resolve each receipt evidence control through its existing receipt-bound endpoint and preserve not-found/unavailable behavior. | covered | evidence route, L0 UI tests |
| A8 | Keep terminal result inspection reachable through the legal action projection without adding illegal actions. | covered | RunView/action resolver, WUI-007 receipt |
| A9 | Prove the retained receipt journey on desktop and mobile without layout overflow or inaccessible evidence controls. | covered | existing responsive shell/mobile tests, focused witness |
| A10 | Preserve all existing bridge, schema, Craft freshness, persistence, and Canvas contracts. | covered | `npm run test:bridge`, prior receipts |

## Selected Context

| Source | Why selected | Selectors / obligations |
| --- | --- | --- |
| `development/workbench-ui-v1/WORK-PACK.md` | authoritative WUI-010 scope and sequencing | WUI-010 row, evidence boundary; A1-A10 |
| `development/workbench-ui-v1/work-pack/tasks/TASK-WUI-004-WORKSPACE.md` | exact Evidence Inspector acceptance contract | receipt attribution, evidence groups, no new authority; A1-A10 |
| `development/workbench-ui-v1/ARCHITECTURE-BUNDLE.md` | Inspector ownership and existing dependency interfaces | evidence drawer, detail route, ready opacity; A2-A6 |
| `development/workbench-ui-v1/task-sessions/20260720T170841Z-swu-wui-009/TASK-SESSION-RESULT.md` | completed predecessor and current route | WUI-010 handoff; A1 |
| `src/server.mjs` | authoritative detail and receipt evidence projections | `proposalDetail`, `projectReceiptForUi`, evidence route; A2-A4, A7 |
| `public/demo/l0.html` | current Inspector, receipt, evidence, and action renderer | detail fields, receipt controls, evidence viewer; A3-A9 |
| `src/ui/run-view.mjs` | pure typestate, stage, and evidence projection | terminal receipt and evidence identity; A3, A6, A8 |
| `src/ui/run-actions.mjs` | legal primary action projection | terminal Inspect result action; A8 |
| `tests/e2e/manual-session-bridge.spec.mjs` | existing admitted execution receipt journey | authorization/execution distinction and same-run evidence; A3-A7 |
| `tests/e2e/workbench-ui-v1-actions.spec.mjs` | existing terminal action journey | inspect reachability across lifecycle; A8-A9 |
| `tests/l0-workbench-ui.test.mjs` | route, markup, detail, evidence, and not-found contracts | A2-A7, A10 |
| `schemas/receipt.schema.json` and `schemas/bridge-result-request.schema.json` | field-level receipt/result authority | validation, grants, context, evidence refs; A4-A7 |

## Implementation Decision

Start with one focused desktop/mobile receipt journey against the existing
detail and evidence routes. Use a bridge request with explicit task, skill,
context, and grants; approve it, make it available, claim it through the test
client, admit a terminal result, select the terminal proposal, and resolve
authorization and execution evidence controls. Assert every displayed group
points to the same envelope, run, approval, and receipt identifiers, while the
ready projection remains free of task and skill before claim.

Only add production UI or server code when this journey proves a missing
Inspector obligation. Do not add a second evidence endpoint, duplicate receipt
model, automatic polling, provider execution, or browser control.

## Execution Constraints

- Keep authorization evidence distinct from `skill.execution` evidence.
- Do not expose task, requested skill, context refs, or validation through the
  ready-only bridge projection before claim.
- Do not let a receipt detail become an action that can mutate a terminal run.
- Preserve existing evidence route error classes and the redacted receipt
  projection.
- Keep the one-page implementation and existing CSS vocabulary unless the
  focused journey proves a layout defect.
- Maintain desktop and mobile Inspector access through the existing tabs.
- Keep the Work Pack boundary bounded to evidence presentation and tests.

## Validation Plan

1. Add a focused desktop/mobile Playwright witness for one admitted bridge run.
2. Assert contract, grants, context, validation, result, receipt, and evidence
   identity all resolve to the same run.
3. Assert authorization and execution receipt rows remain distinct and the
   ready-only projection remains opaque before claim.
4. Assert every evidence kind resolves in the Inspector and terminal Inspect
   result remains the only primary action after completion.
5. Run the existing action, manual bridge, workbench, and full bridge suites.
6. Synchronize the WUI-010 receipt and route to WUI-011 only after all checks
   pass.

## Context Builder Result

- Files selected: 12 source groups
- Obligation coverage: 10/10
- Strict coverage: pass
- Fallback search: none
- Blockers: 0

## Next Actions

1. Run the focused retained receipt journey before changing production code.
2. Repair only the Inspector projection gaps that the journey exposes.
3. Synchronize the pass receipt and route to WUI-011.
