# Context Pack: SWU-WUI-003

- Task: `SWU-WUI-003` - Mobile Navigation
- Mode: standard
- Runtime: local Node and Playwright Chromium
- Dependency receipt: [SWU-WUI-002 PASS](../20260720T154814Z-swu-wui-002/TASK-SESSION-RESULT.md)
- Gate verdict: pass; the unit is ready in the synchronized Work Pack

## Obligation Matrix

| ID | Obligation | Status | Controlling evidence |
| --- | --- | --- | --- |
| A1 | Execute exactly `SWU-WUI-003` after `SWU-WUI-002`. | covered | Work Pack, task contract, dependency receipt |
| A2 | Provide reachable mobile Work, Canvas, and Evidence views. | covered | task contract, UX plan, architecture bundle |
| A3 | Keep one navigation state machine without duplicating current run or Canvas state. | covered | task handoff, current DOM/script state |
| A4 | Preserve the current run status and existing top-bar task controls while adding mobile navigation. | covered | UX plan, current header DOM |
| A5 | Keep the write scope to mobile controls/state, responsive CSS, and focused mobile Playwright assertions. | covered | task contract |
| A6 | Prove text and controls fit without horizontal overflow or viewport clipping in each mobile view. | covered | mobile witness contract |
| A7 | Prove navigation away from and back to Work preserves an in-page prepared proposal. | covered | task acceptance, existing prepare flow |
| A8 | Run the focused mobile witness and the existing workbench suite. | covered | task contract, package scripts |
| A9 | Do not alter request mode, lifecycle projection, evidence content, Canvas APIs, Craft mutation, provider, browser, worker, or IDE-host scope. | covered | task handoff, Work Pack gates, product spec |

## Selected Context

| Source | Why selected | Selectors / obligations |
| --- | --- | --- |
| `development/workbench-ui-v1/WORK-PACK.md` | authoritative ready-unit and next-route state | WUI-003 manifest, gates; A1-A9 |
| `development/workbench-ui-v1/work-pack/tasks/TASK-WUI-001-SHELL.md` | exact mobile navigation write scope and handoff | SWU-WUI-003 contract; A1-A9 |
| `development/workbench-ui-v1/UX-PLAN.md` | intended mobile views, status visibility, and accessibility rules | mobile layout, primary interactions, stability; A2-A4, A6 |
| `development/workbench-ui-v1/ARCHITECTURE-BUNDLE.md` | ownership boundary for shell, Canvas, Inspector, and existing APIs | responsive shell and dependency interface; A2-A5, A9 |
| `public/demo/l0.html` | current mobile CSS, region DOM, and script ownership | `@media (max-width: 720px)`, `data-region`, current controls; A2-A5, A9 |
| `tests/e2e/l0-approval-desk.spec.mjs` | existing prepare/state-preservation browser oracle | prepare action and layout checks; A3, A6-A8 |
| `tests/l0-workbench-ui.test.mjs` | existing local workbench contract oracle | static DOM and behavior invariants; A5, A8-A9 |
| `playwright.config.mjs` | mobile viewport and local server contract | mobile Chromium project; A6-A8 |

## Implementation Assumption

Add a mobile-only `tablist` with Work, Canvas, and Evidence buttons above the
existing shell. Store the selected view on the existing `.workbench-shell`
element and use CSS to hide inactive regions at widths up to `720px`. The
Inspector column is the Evidence destination because it already owns detail,
receipt, and evidence content; no evidence data or lifecycle mapper changes are
needed. This is reversible within the shell unit and avoids duplicating the
existing proposal, Canvas, or evidence state.

## Execution Constraints

- Keep all existing IDs, `data-panel` selectors, `data-region` selectors,
  action selectors, API calls, and event handlers intact.
- Keep the server status, task composer, and skill controls in the existing
  header; mobile navigation must not replace or reinterpret them.
- Use text-labeled controls with keyboard-accessible tab semantics and stable
  dimensions.
- Preserve the existing stacked mobile layout as the fallback when the view
  state is not selected or when scripting is unavailable.
- Do not implement the request-mode selector, lifecycle projection, primary
  action resolver, Canvas API change, Craft mutation, or host integration.

## Context Builder Result

- Files selected: 8
- Snippets selected: 8 selector-level excerpts
- Obligation coverage: 9/9
- Strict coverage: pass
- Fallback search: none
- Blockers: 0

## Next Actions

1. Add the mobile view tablist and one presentation-only view controller.
2. Add responsive visibility rules and focused mobile reachability/state tests.
3. Run the focused mobile and retained workbench suites, retain a mobile
   screenshot, and synchronize the next route only after pass.
