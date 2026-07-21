# Context Pack: SWU-WUI-006

- Task: `SWU-WUI-006` - Run Timeline
- Parent: `TASK-WUI-003` - Run Lifecycle
- Mode: standard
- Runtime: local Node and Playwright
- Dependency receipt: [SWU-WUI-005 PASS](../20260720T161925Z-swu-wui-005/TASK-SESSION-RESULT.md)
- Gate verdict: pass; the pure `RunView` projection is available and stable

## Obligation Matrix

| ID | Obligation | Status | Controlling evidence |
| --- | --- | --- | --- |
| A1 | Execute exactly `SWU-WUI-006` after `SWU-WUI-005`. | covered | Work Pack, dependency receipt |
| A2 | Render `Prepared`, `Approved`, `Available`, `Running`, `Result`, and `Receipt` in order. | covered | lifecycle task, current bridge markup |
| A3 | Consume `RunView` rather than rederive kernel state in timeline DOM code. | covered | `src/ui/run-view.mjs`, task handoff |
| A4 | Show current, completed, and pending treatment truthfully for every supported typestate. | covered | RunView state matrix, lifecycle task |
| A5 | Keep claimed work visibly running and never completed. | covered | RunView contract, Work Pack gate |
| A6 | Keep interrupted, blocked, failed, and residue states attributable in the timeline. | covered | RunView labels/stages, UX plan |
| A7 | Keep timeline output free of action controls. | covered | lifecycle independent acceptance |
| A8 | Make the canonical UI modules available to the local browser without duplicating projection logic. | covered | `src/server.mjs` explicit route boundary |
| A9 | Prove lifecycle rendering on desktop and mobile with focused Playwright fixtures. | covered | task validation, Playwright config |
| A10 | Do not alter action controls, kernel authority, provider, browser, worker, IDE-host, or Craft scope. | covered | Work Pack gates, task write scope |

## Selected Context

| Source | Why selected | Selectors / obligations |
| --- | --- | --- |
| `development/workbench-ui-v1/WORK-PACK.md` | authoritative ready unit and sequencing | WUI-006 manifest, lifecycle order, gates; A1-A10 |
| `development/workbench-ui-v1/work-pack/tasks/TASK-WUI-003-LIFECYCLE.md` | exact renderer contract and handoff | WUI-006 done/acceptance/validation; A1-A7, A9-A10 |
| `development/workbench-ui-v1/SPEC.md` | truthful lifecycle and excluded authority boundaries | claimed is not complete; A4-A6, A10 |
| `development/workbench-ui-v1/ARCHITECTURE-BUNDLE.md` | UI/kernel ownership boundary | UI projection consumes kernel projection; A3, A10 |
| `src/ui/run-view.mjs` | canonical pure projection and labels | supported typestates, stage, evidence; A2-A6 |
| `src/server.mjs` | browser transport boundary | only `/demo/l0`, logo, and API routes are served; A8 |
| `public/demo/l0.html` | current timeline markup and render call site | `#bridge-flow`, `renderBridgeDemo`; A2-A7 |
| `tests/e2e/server-harness.mjs` | focused browser server root and lifecycle | local server serves project public plus explicit routes; A8-A9 |
| `playwright.config.mjs` | desktop/mobile validation surface | Chromium desktop and 390px mobile projects; A9 |

## Implementation Decision

The workbench serves the canonical `src/ui/run-view.mjs` and the new pure DOM
renderer through explicit local `/ui/*.mjs` routes. The page remains an ES module
and imports both modules. This is a local transport adapter, not a general static
file server: it exposes only the two required UI modules and does not widen the
server's filesystem boundary.

`renderRunTimeline(container, runView)` owns the ordered six-stage DOM projection.
For ordinary states, the current RunView stage is active, earlier stages are done,
and later stages are pending. `interrupted` remains attached to the Running stage
with its truthful interrupted label. Terminal `blocked`, `failed`, and residue
labels remain attached to Result unless admitted receipt evidence advances the
view to Receipt. No buttons or action handlers are created by the renderer.

## Execution Constraints

- Preserve the existing envelope, approval, bridge, canvas, and Craft contracts.
- Replace only the old six-step timeline projection; leave safe fields, actions,
  receipts, and detail authority unchanged for WUI-007/WUI-010.
- Do not label claimed work completed.
- Do not infer completion from chat text or receipt presence outside `RunView`.
- Keep the renderer deterministic and testable from a serializable `RunView`.
- Do not add provider execution, browser control, worker, VSCodium host, or IDE
  integration scope.
- Do not create a browser-side copy of `projectRunView`.

## Validation Plan

1. Unit-test the ordered renderer contract, labels, current/done/pending matrix,
   interrupted and terminal residue behavior, and absence of controls.
2. Run focused desktop and mobile Playwright fixtures that exercise prepared,
   approved, available, running, and admitted receipt states.
3. Run the existing workbench and bridge suites to detect regressions.
4. Run scoped `git diff --check`.

## Context Builder Result

- Files selected: 9
- Obligation coverage: 10/10
- Strict coverage: pass
- Fallback search: none
- Blockers: 0

## Next Actions

1. Add the canonical `src/ui/run-timeline.mjs` renderer and explicit local UI
   module routes.
2. Import the renderer into `public/demo/l0.html` and project the existing detail
   through `projectRunView` for the timeline only.
3. Add focused renderer and desktop/mobile lifecycle fixtures.
4. Validate and synchronize the Work Pack, Craft ledger/index, README, and task
   session receipt after all checks pass.
