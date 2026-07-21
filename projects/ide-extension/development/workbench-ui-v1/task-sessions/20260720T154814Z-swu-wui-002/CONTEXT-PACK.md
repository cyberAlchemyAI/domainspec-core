# Context Pack: SWU-WUI-002

- Task: `SWU-WUI-002` - Desktop Grid
- Mode: standard
- Runtime: local Node and Playwright Chromium
- Dependency receipt: [SWU-WUI-001 PASS](../20260720T153545Z-swu-wui-001/TASK-SESSION-RESULT.md)
- Gate verdict: pass; the unit is ready in the synchronized Work Pack

## Obligation Matrix

| ID | Obligation | Status | Controlling evidence |
| --- | --- | --- | --- |
| A1 | Execute exactly `SWU-WUI-002` after `SWU-WUI-001`. | covered | Work Pack, task contract, dependency receipt |
| A2 | Arrange Work, Canvas, and Inspector in a stable desktop grid. | covered | UX plan, architecture bundle |
| A3 | Use the UX track guidance of approximately `300px minmax(0, 1fr) 360px`. | covered | UX plan; recorded as reversible implementation assumption |
| A4 | Preserve WUI-001 semantic region selectors and existing controls/scripts. | covered | prior result, current HTML, focused Node tests |
| A5 | Keep the write scope to shell CSS/DOM grouping and focused desktop Playwright evidence. | covered | task contract |
| A6 | Prove no overlap, clipping, horizontal overflow, or unreachable controls at desktop width. | covered | desktop witness contract |
| A7 | Retain a screenshot and run the existing workbench suite. | covered | task contract, package scripts |
| A8 | Do not add mobile navigation, lifecycle projection, request modes, provider, browser, worker, or IDE-host scope. | covered | task handoff, Work Pack gates, product spec |

## Selected Context

| Source | Why selected | Selectors / obligations |
| --- | --- | --- |
| `development/workbench-ui-v1/WORK-PACK.md` | authoritative ready-unit and next-route state | WUI-002 manifest, gates; A1-A8 |
| `development/workbench-ui-v1/work-pack/tasks/TASK-WUI-001-SHELL.md` | exact layout write scope and handoff | SWU-WUI-002 contract; A1-A8 |
| `development/workbench-ui-v1/work-pack/waves/W0.md` | shell promotion order | W0 sequence; A1, A8 |
| `development/workbench-ui-v1/UX-PLAN.md` | desktop tracks and accessibility order | desktop layout, stability; A2-A3, A6 |
| `development/workbench-ui-v1/ARCHITECTURE-BUNDLE.md` | intended Work/Canvas/Inspector ownership | structure and components; A2, A4, A8 |
| `public/demo/l0.html` | current DOM/CSS and selector surface | shell styles and existing controls; A2, A4-A5 |
| `tests/e2e/l0-approval-desk.spec.mjs` | existing desktop layout and interaction oracle | no-overlap, overflow, focus, screenshot; A4, A6-A7 |
| `playwright.config.mjs` | project viewport and local server contract | desktop Chromium at 1440x900; A6-A7 |

## Implementation Assumption

Use the UX plan's recommended desktop tracks as the exact CSS grid:
`minmax(260px, 300px) minmax(0, 1fr) minmax(300px, 360px)`. This is reversible
within the shell unit and does not resolve any later mobile or product decisions.

## Execution Constraints

- Preserve `data-panel`, `data-region`, IDs, action selectors, and module script
  query targets.
- Keep request, approval, bridge, Canvas, Craft, evidence, and receipt behavior
  unchanged.
- The desktop grid may regroup existing DOM surfaces but must not introduce
  mobile navigation or state projection.
- Any responsive CSS adaptation must preserve the existing stacked behavior;
  mobile interaction design remains `SWU-WUI-003`.

## Context Builder Result

- Files selected: 8
- Snippets selected: 8 selector-level excerpts
- Obligation coverage: 8/8
- Strict coverage: pass
- Fallback search: none
- Blockers: 0

## Next Actions

1. Group the existing Work and Inspector children around the Canvas grid item
   without changing their behavior selectors.
2. Add the desktop grid CSS and focused desktop Playwright witness.
3. Run the focused browser and workbench suites, retain the screenshot, and
   synchronize the next route only after pass.
