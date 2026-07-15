# Context Pack: SWU-OV1-010

- Task: `SWU-OV1-010` - Browser Display Projection And Acknowledgement
- Mode: standard
- Handoff: none; local Task Session execution
- Strict coverage: pass
- Gate verdict: pass
- Runtime: local plus real Chromium
- Dependency receipt: `../20260714T224925Z-swu-ov1-009/TASK-SESSION-RESULT.md`

## Obligation Matrix

| ID | Obligation | Status |
| --- | --- | --- |
| O1 | Startup and SSE reconnect fetch `/api/canvas/display`, not V0 `/current`. | covered |
| O2 | Preflight complete content, load a hidden iframe, then atomically swap. | covered |
| O3 | Failed preflight/load removes only the pending frame and retains the last good frame and identity. | covered |
| O4 | Redirect notices refetch display and acknowledge loaded or failed. | covered |
| O5 | Refresh notices force reload of the same revision and acknowledge loaded or failed. | covered |
| O6 | Revision notices reload only when their surface matches the server display target. | covered |
| O7 | Duplicate/open/reconnect notices do not create overlapping visible frames. | covered |
| O8 | Open-in-new-tab always binds to the successfully loaded display content URL. | covered |
| O9 | V0 interactions preserve the existing V3 route and request behavior. | covered |
| O10 | Operations interactions use a strict V4 request and bind to the displayed Operations revision. | covered |
| O11 | Non-selected Operations commits do not reload the browser; selected commits converge to the new revision. | covered |
| O12 | Manual refresh works with and without EventSource while using the navigation runtime. | covered |
| O13 | Desktop and mobile Chromium prove V0, redirect, append/reload, refresh, failure retention, interaction, reconnect, and restart behavior. | covered |
| O14 | Existing approval desk, Canvas Node, and Canvas/bridge Playwright journeys remain green. | covered |

## Implementation Shape

- Keep the existing Canvas panel and hidden pending iframe design; replace its
  state binding with the display response shape and typed navigation notices.
- Acknowledge command IDs only after successful swap/current-target confirmation
  or after preserving the old frame on failure.
- Add one strict Operations interaction request schema and one surface-scoped
  POST route while leaving V0 `/api/canvas/events` unchanged.
- Add focused Node selector/contract assertions and a dedicated desktop/mobile
  Playwright suite with retained screenshots.

## Write Scope

- `public/demo/l0.html` display controller and interaction routing.
- Operations interaction schema, registry, fixtures, route, and focused tests.
- `tests/l0-workbench-ui.test.mjs` browser contract assertions.
- `tests/e2e/operations-v1-navigation.spec.mjs` and package command.
- Task Session and synchronized plan/Craft evidence.

## Excluded

- New visual redesign, browser identity, tabs, durable refresh replay, queues,
  pruning implementation, named regions, remote control, provider calls, and
  hostile HTML containment claims.

## Context Builder Result

- Obligation coverage: 14/14, 100 percent
- Strict coverage: pass
- Blockers: 0
- Fallback search: none
- Noise: bounded to workbench display delivery and Operations interaction binding
