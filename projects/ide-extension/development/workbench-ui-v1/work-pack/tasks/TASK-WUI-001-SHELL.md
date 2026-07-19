# TASK-WUI-001: Product Shell

## Objective

Recompose the existing page into Work rail, Canvas workspace, and Inspector
without changing request or run behavior.

## Source Contracts

- [Architecture](../../ARCHITECTURE-BUNDLE.md)
- [UX plan](../../UX-PLAN.md)
- `projects/ide-extension/public/demo/l0.html`
- `projects/ide-extension/tests/l0-workbench-ui.test.mjs`

## SWU-WUI-001: Semantic Regions

- Primary behavior: expose stable Work, Canvas, and Inspector landmarks.
- Dependencies: none.
- Write scope: `public/demo/l0.html`, focused workbench structure tests.
- Done criteria: existing controls live under one named landmark without behavior changes.
- Independent acceptance: landmark assertions and current workbench tests pass.
- Validation: `npm run test:workbench`.
- Owner: `local-fallback`.
- Split analysis: one landmark per SWU would not produce an independently useful shell; the three landmarks share one accessibility and ownership oracle.
- Handoff: change semantic structure only; do not add desktop grid, mobile navigation, or state projection.

## SWU-WUI-002: Desktop Grid

- Primary behavior: arrange the three semantic regions in a stable desktop grid.
- Dependencies: `SWU-WUI-001`.
- Write scope: shell CSS/layout and focused desktop Playwright assertions.
- Done criteria: Work, Canvas, and Inspector remain visible and usable at supported desktop widths.
- Independent acceptance: retained screenshot and checks show no overlap, clipping, or unreachable controls.
- Validation: focused desktop Playwright shell journey plus `npm run test:workbench`.
- Owner: `local-fallback`.
- Split analysis: track sizing and region placement share one rendered grid oracle and are not useful independently.
- Handoff: preserve DOM contracts from SWU-WUI-001; do not add mobile state.

## SWU-WUI-003: Mobile Navigation

- Primary behavior: switch among Work, Canvas, and Evidence views on mobile.
- Dependencies: `SWU-WUI-002`.
- Write scope: shell mobile controls/state, responsive CSS, focused mobile Playwright assertions.
- Done criteria: each view is reachable, state is not duplicated, and text/controls fit.
- Independent acceptance: mobile journey reaches all views and returns without losing current run or Canvas state.
- Validation: focused mobile Playwright journey plus `npm run test:workbench`.
- Owner: `local-fallback`.
- Split analysis: one SWU per destination would fragment one navigation state machine and cannot establish reachability alone.
- Handoff: do not alter request mode, lifecycle projection, or evidence content.

## Synchronization

After each SWU, update the parent task status and preserve the next uncompleted
SWU as the only mutation-capable handle.
