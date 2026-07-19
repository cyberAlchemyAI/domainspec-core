---
module: ide-extension-open-poll-bridge
taskId: TASK-SESSION-WORKBENCH
swuId: SWU-OPB-006
status: pass
capability_ref: task-session
receipt_kind: local-fallback
createdAt: 2026-07-17T01:04:08Z
---

# TASK SESSION RESULT: SWU-OPB-006

## Scope

Update workbench labels and states from target/selected to available/claimed.

## Context Pack

- Mode: lean.
- Strict coverage: pass.
- Sources: `public/demo/l0.html`, workbench UI tests, focused Playwright
  bridge spec, and W2 task contract.
- Controlling obligations: operator sees available/open/claimed/result
  language; no polling type or selected-target language implies exclusive
  routing.

## Decisions

- No blocker decisions.

## Files Updated

- `projects/ide-extension/public/demo/l0.html`
- `projects/ide-extension/tests/l0-workbench-ui.test.mjs`
- `projects/ide-extension/tests/e2e/manual-session-bridge.spec.mjs`

## Validation

- PASS: `npm --prefix projects/ide-extension run test:workbench`
  - 6 tests passed.
- PASS: `npm --prefix projects/ide-extension run test:bridge`
  - 67 tests passed.
- PASS: scoped `git diff --check`.
- PASS: `npm exec -- playwright test tests/e2e/manual-session-bridge.spec.mjs`
  from `projects/ide-extension`
  - 2 Chromium projects passed.

## Result

PASS. The workbench now presents the bridge as open singleton availability and
claim-bound execution instead of selected-target polling.

## Reroute

Proceed to `SWU-OPB-007`.
