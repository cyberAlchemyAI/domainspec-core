# Task Contract: Guided Surface And Focused IDE Route

## Control

| Field | Value |
| --- | --- |
| Task ID | `TASK-RDL-GUIDED-SURFACE` |
| Objective | Deliver the FPR-01 learning/restatement/source/proposal loop through a dedicated IDE mode. |
| Layer / slice / wave | L0 / S-002 / W1 |
| Dependencies | SWU-RDL-004 pass |
| Blockers | `l0.html` and `server.mjs` are currently dirty; selection requires overlap/owner resolution. |
| Execution | Blocked: generated surface completed; focused parent route requires dirty-scope owner decision. |

## Sources

- [UX primary journey and states](../../UX-PLAN.md#primary-journey)
- [RDL-O02 proposal flow](../../ARCHITECTURE-BUNDLE.md#rdl-o02-submit-restatement-or-proposal)
- Existing `l0.html` exact postMessage admission and Canvas API routes.

## SWU-RDL-005 — FPR-01 learning and proposal surface

- **Objective:** Make the generated roadmap HTML teach and collect one honest
  proposal using only the existing Canvas message envelope.
- **Dependencies:** SWU-RDL-004.
- **Write scope:** visibility copy/template/build tests, new focused browser
  fixture/spec if kept with the visibility package, and regenerated outputs.
- **Rules:** implement orientation, FPR-01 learning packet, three-part
  restatement, copyable source paths/request, class/field proposal form, owner
  preview, immutable bindings, client contract validation, payload-size guard,
  stored-only acknowledgment, retry-preserved draft, keyboard/focus/status
  semantics; emit no passive clicks.
- **Edge cases:** missing binding, republish during draft, blank participant,
  unsupported proposal class, field not in manifest, multiline/HTML text,
  postMessage rejection, API failure response from parent.
- **Done:** exact semantic events match W0 schemas and the UI never calls a
  mutation endpoint or claims review/application.
- **Acceptance evidence:** browser snapshots, keyboard trace, exact messages,
  failure-state capture, and regenerated output digest.
- **Validation:** visibility suite plus focused Playwright/DOM tests of generated
  roadmap HTML.
- **Owner:** `local-fallback`.
- **Handoff:** return exact event payload fixtures and published HTML path for
  SWU-RDL-006.
- **Result:** [PASS](../../task-sessions/20260714T223345Z-swu-rdl-005/TASK-SESSION-RESULT.md) —
  generated FPR-01 lab panel emits exact orientation, restatement, source, and
  proposal messages; waits for parent storage acknowledgment; preserves drafts
  on local validation failure; and has focused Playwright desktop/mobile
  evidence.

## SWU-RDL-006 — Dedicated Roadmap Lab mode and Canvas witness

- **Objective:** Give a newcomer a focused route while reusing the existing
  Canvas kernel and message/event path.
- **Dependencies:** SWU-RDL-005.
- **Write scope:** only the approved overlapping IDE files among
  `projects/ide-extension/src/server.mjs`, `public/demo/l0.html`, focused tests,
  and package scripts when necessary. Prefer a route/mode over duplicating the
  Canvas implementation.
- **Rules:** `/demo/roadmap-lab` (or equivalently explicit stable route) loads a
  focused mode; hide unrelated ide-extension Craft/operations context; retain
  current/revision indicator, refresh/reconnect, event adapter, and error
  boundary; do not add DomainSpec effect APIs; publish the existing generated
  workspace HTML through the existing CLI/API.
- **Edge cases:** no current canvas, wrong surface kind/title, stale revision,
  refresh, reconnect, deep link/reload, mobile viewport sanity, unrelated Canvas
  surface published.
- **Done:** a clean local journey opens the dedicated route, displays FPR-01,
  submits a restatement/source request/proposal, and retrieves them through the
  existing cursor poll with exact bindings.
- **Acceptance evidence:** publish response, route/browser screenshots, stored
  event/poll JSON, and complete Canvas regression output.
- **Validation:** focused Node route/UI tests; `npm run test:canvas-contracts`,
  `test:canvas-replay`, `test:canvas-publish`, `test:canvas-interactions`, and a
  focused Playwright Roadmap Lab journey.
- **Owner:** `local-fallback`.
- **Handoff:** W1 closes only with a real generated roadmap publication, not a
  substitute HTML fixture.
- **Result:** [BLOCK](../../task-sessions/20260714T224609Z-swu-rdl-006/TASK-SESSION-RESULT.md) —
  current `l0.html`, `server.mjs`, package scripts, and IDE tests are dirty with
  Craft Frontier and Operations v1 work overlapping the required route/kernel
  surface. Decision Gate recommends finishing or isolating that IDE work before
  rerunning SWU-RDL-006.

## Synchronization And Completion

If current dirty changes cannot be cleanly composed, stop with exact overlapping
hunks and owner question. Do not create a duplicate Canvas kernel to avoid that
coordination.
