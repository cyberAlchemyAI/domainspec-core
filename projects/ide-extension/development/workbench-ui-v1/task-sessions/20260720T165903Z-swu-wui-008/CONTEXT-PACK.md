# Context Pack: SWU-WUI-008

- Task: `SWU-WUI-008` - Primary Canvas
- Parent: `TASK-WUI-004` - Canvas, Craft, And Evidence
- Mode: standard
- Runtime: local Node and Playwright Chromium
- Dependency receipts:
  - [SWU-WUI-003 PASS](../20260720T155936Z-swu-wui-003/TASK-SESSION-RESULT.md)
  - [SWU-WUI-007 PASS](../20260720T164437Z-swu-wui-007/TASK-SESSION-RESULT.md)
- Gate verdict: pass; the existing Canvas frame and retention behavior are available

## Obligation Matrix

| ID | Obligation | Status | Controlling evidence |
| --- | --- | --- | --- |
| A1 | Execute exactly `SWU-WUI-008` after the completed WUI-007 boundary. | covered | Work Pack, WUI-007 receipt |
| A2 | Keep the retained Canvas artifact in the primary desktop workspace. | covered | Work Pack, shell layout witness |
| A3 | Keep current surface and revision identity visible beside the frame. | covered | Canvas identity renderer, DOM data attributes |
| A4 | Prove a successful later revision can replace the retained frame. | covered | Canvas publish notification and refresh path |
| A5 | Prove a failed later navigation keeps the previous frame and revision usable. | covered | pending iframe swap and old-frame contract |
| A6 | Keep Canvas reachable and fitted on the mobile Canvas view. | covered | mobile navigation and viewport-fit witness |
| A7 | Preserve artifact interaction after successful placement and after failed navigation. | covered | iframe interaction route and retained-frame assertions |
| A8 | Do not add server behavior, Craft mutation, evidence projection, or provider/IDE scope. | covered | task write scope and Work Pack gates |

## Selected Context

| Source | Why selected | Selectors / obligations |
| --- | --- | --- |
| `development/workbench-ui-v1/WORK-PACK.md` | authoritative WUI-008 scope and gates | WUI-008 row, Canvas placement, no new server behavior; A1-A8 |
| `development/workbench-ui-v1/work-pack/tasks/TASK-WUI-004-WORKSPACE.md` | exact objective and acceptance contract | retained artifact, revision identity, old-frame failure; A1-A8 |
| `development/workbench-ui-v1/task-sessions/20260720T164437Z-swu-wui-007/TASK-SESSION-RESULT.md` | completed lifecycle/action dependency | downstream Canvas handle; A1, A8 |
| `public/demo/l0.html` | current Canvas placement and browser retention implementation | primary grid, mobile tab, identity, pending iframe swap, refresh; A2-A7 |
| `src/server.mjs` | existing display/content routes only | v0 revision content contract; A4-A5, A8 |
| `tests/e2e/workbench-ui-v1-shell.spec.mjs` | existing desktop region/fit witness | Work, Canvas, Inspector grid; A2 |
| `tests/e2e/workbench-ui-v1-mobile.spec.mjs` | existing mobile reachability witness | Canvas tab and viewport fit; A6 |
| `tests/e2e/operations-v1-navigation.spec.mjs` | existing old-frame and revision behavior witness | successful swap, failed target, retained frame; A3-A7 |

## Implementation Decision

Keep the current Canvas implementation and add one focused WUI-008 browser
witness. The page already renders Canvas as the middle desktop column, exposes a
mobile Canvas view, labels the loaded surface/revision, swaps through a pending
iframe, and removes the pending frame on failure before replacing the current
frame. The new test will prove that contract using a real v0 publish flow and a
blocked later revision. No server or product behavior change is required.

## Execution Constraints

- Preserve existing Canvas endpoints and notification payloads.
- Do not replace the current frame before the next frame has loaded.
- Do not clear the current frame or identity on a failed later navigation.
- Keep successful artifact interaction available through the current iframe.
- Do not add Craft selection, evidence inspector, provider, worker, browser
  automation, VSCodium, or server scope.
- Keep the witness valid in both configured desktop and mobile projects.

## Validation Plan

1. Add a focused WUI-008 Playwright witness with a temporary workspace and
   server.
2. Publish revision A and prove the Canvas identity, iframe content, desktop
   primary-column fit, and mobile Canvas tab.
3. Publish revision B while blocking its content URL; prove revision A remains
   visible and interactive while the Canvas reports the failed load.
4. Remove the block, use the existing Refresh canvas action, and prove revision B
   becomes the current frame.
5. Run the focused WUI-008 Playwright test, existing Canvas navigation test,
   existing workbench shell/mobile tests, and scoped diff checks.

## Context Builder Result

- Files selected: 8
- Obligation coverage: 8/8
- Strict coverage: pass
- Fallback search: none
- Blockers: 0

## Next Actions

1. Add the focused retained-Canvas browser witness.
2. Run desktop/mobile Playwright validation and inspect screenshots.
3. Synchronize the WUI-008 receipt, Work Pack, task contract, Craft ledger, and
   generated index if the witness passes.
