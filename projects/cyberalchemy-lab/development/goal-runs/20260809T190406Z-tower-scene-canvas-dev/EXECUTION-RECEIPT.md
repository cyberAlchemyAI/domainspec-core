# WP-CAL-TOWER-SCENE-V1 — dev-mode execution receipt

- Goal profile: `development/refinement-runs/20260809T182018Z-tower-scene-canvas/goal-profile/GOAL-PROFILE.md`
- Selected stream: `SWU-CAL-SCENE-001 -> 002 -> 003 -> 004`
- Status: pass
- Authority boundary: synthetic, local, read-only candidate; `authority_effect: none`.

## Implemented

1. `loadResearchTowerL0` now exposes a validated `cal.tower-scene-manifest.v1` with one `tower:toy`, three evidence scenes, and a separately namespaced unavailable Tower System atlas.
2. The page now uses native tower and scene controls, source/state/ceiling status, explicit unavailable text, and focus/reset orientation controls while retaining source orbit and relation inspection.
3. Decoration remains separate from semantic navigation and is hidden from assistive technology; motion controls only decoration.
4. The page has desktop/mobile/reduced-motion browser coverage and negative manifest checks.

## Changed product paths

- `projects/ide-extension/src/research-tower/l0-witness.mjs`
- `projects/ide-extension/public/demo/research-tower.html`
- `projects/ide-extension/tests/research-tower-explorer.test.mjs`
- `projects/ide-extension/tests/e2e/research-tower-explorer.spec.mjs`
- `projects/ide-extension/README.md`

The existing `src/server.mjs` and local visual assets were reused; they were not changed by this Goal run.

## Validation

- `node tests/research-tower-explorer.test.mjs`: 4/4 pass.
- `node tests/l0-workbench-ui.test.mjs`: 6/6 pass.
- `./node_modules/.bin/playwright test tests/e2e/research-tower-explorer.spec.mjs --reporter=line`: 4/4 pass (desktop/mobile, including reduced motion).
- `git diff --check` on the changed tracked implementation paths: pass.

## Read-only helper receipt

`/root/scene_canvas_contract_check` inspected the current loader/server/page/test seams without edits. Its recommendations—preserve the L0 trust boundary, use native semantic controls, add an explicit refusal panel, keep decoration hidden, and add focused test coverage—were incorporated.

## Residue

- The canvas still has only the locked synthetic `tower:toy`; real-tower selection remains out of scope.
- System atlas buttons are explanatory unavailable states, not a queryable graph, personas, MOGT policy, scoring, or adjudication runtime.
- No animation/game dependency was introduced. Future engine selection requires a separate named gap and confirmation.
- No authority/promotion/publication/deployment, commit, push, or external research occurred.
