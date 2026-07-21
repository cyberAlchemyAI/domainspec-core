# Context Pack: SWU-WUI-001

- Task: `SWU-WUI-001` - Semantic Workbench Regions
- Mode: standard
- Runtime: local Node test runner
- Dependency receipt: none; the SWU has no dependencies
- Gate verdict: pass from `development/workbench-ui-v1/DECISION-GATE.md`

## Obligation Matrix

| ID | Obligation | Status | Controlling evidence |
| --- | --- | --- | --- |
| A1 | Execute exactly `SWU-WUI-001`, not a later UI unit. | covered | `WORK-PACK.md`, task contract |
| A2 | Expose named Work, Canvas, and Inspector landmarks. | covered | task contract, architecture, UX plan |
| A3 | Keep the change semantic-only. | covered | task handoff, Work Pack gates |
| A4 | Preserve request, run, Canvas, Craft, bridge, and receipt behavior. | covered | architecture, product spec, focused tests |
| A5 | Keep the declared write scope bounded to the demo shell and focused test. | covered | task contract |
| A6 | Validate with `npm --prefix projects/ide-extension run test:workbench`. | covered | task contract, package script |
| A7 | Synchronize the task result, Work Pack, and Craft route after evidence passes. | covered | task synchronization contract, Craft ledger |
| A8 | Do not add desktop grid, mobile navigation, state projection, provider, browser, worker, or IDE-host scope. | covered | task handoff, Work Pack gates, product spec |

## Selected Context

| Source | Why selected | Selectors / obligations |
| --- | --- | --- |
| `development/workbench-ui-v1/WORK-PACK.md` | authoritative unit, acceptance, gates, and next-route contract | SWU manifest, atomicity, gates; A1-A8 |
| `development/workbench-ui-v1/work-pack/tasks/TASK-WUI-001-SHELL.md` | exact objective, write scope, done criteria, and handoff | Product Shell, SWU-WUI-001; A1-A8 |
| `development/workbench-ui-v1/ARCHITECTURE-BUNDLE.md` | region ownership and local-kernel boundary | structure and component views; A2-A4, A8 |
| `development/workbench-ui-v1/UX-PLAN.md` | semantic region intent and keyboard order | desktop/mobile layout and accessibility; A2-A4, A8 |
| `development/workbench-ui-v1/SPEC.md` | product inclusions and exclusions | definition, success criteria, exclusions; A4, A8 |
| `public/demo/l0.html` | current DOM and behavior surface to preserve | existing shell, controls, scripts; A2-A5 |
| `tests/l0-workbench-ui.test.mjs` | focused regression oracle | document selectors and server behavior; A4-A6 |
| `development/workbench-ui-v1/DECISION-GATE.md` | resolved frontier and no remaining blocker | PASS and deferred decisions; A1, A8 |

## Execution Constraints

- Add semantic landmarks without changing CSS layout, endpoint calls, state
  projection, dynamic rendering, or control behavior.
- Keep all current `data-*` selectors and existing accessible names stable.
- Do not infer or introduce request modes in this unit.
- Do not move the Canvas or change the evidence/detail ownership model in this
  unit; later SWUs own layout and projection composition.

## Context Builder Result

- Files selected: 8
- Snippets selected: 8 selector-level excerpts
- Obligation coverage: 8/8
- Strict coverage: pass
- Fallback search: none
- Blockers: 0

## Next Actions

1. Add stable semantic Work, Canvas, and Inspector landmarks inside the declared
   write scope.
2. Run the focused workbench test and inspect the scoped diff.
3. Record the result and synchronize the Work Pack/Craft route only after pass.
