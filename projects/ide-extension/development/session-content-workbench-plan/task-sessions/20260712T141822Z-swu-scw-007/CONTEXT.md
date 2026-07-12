# Context Pack: SWU-SCW-007

## Selection

- Task/SWU: `TASK-VALUE-WITNESSES / SWU-SCW-007`
- Mode: standard, local Task Session
- Dependency: SWU-SCW-006 PASS

## Obligations

| ID | Obligation | Evidence | Status |
| --- | --- | --- | --- |
| O1 | Prove a keyboard/button presentation and automatic changed revision. | Witness 1. | covered |
| O2 | Prove Decision selection emits exact generic payload and CLI poll. | Witness 2. | covered |
| O3 | Prove Craft action uses the same event route without effect claims. | Witness 3. | covered |
| O4 | Cover desktop/mobile, reload-before-poll, and duplicate poll. | Edge cases and done criteria. | covered |
| O5 | Prove no specialized Decision or Craft server route exists. | Source-scan exit gate. | covered |
| O6 | Keep runtime behavior unchanged unless an acceptance defect is found. | Exact write scope. | covered |

## Execution Decisions

- Keep canonical HTML fixtures under `tests/fixtures/canvas/`; copy them into a
  temporary workspace so republish tests never mutate tracked fixtures.
- Use one own-process test server per browser journey, preserving real HTTP,
  EventSource, iframe, restart-safe projection, and CLI behavior.
- Record Decision and Craft as request events only. The fixture text and tests
  do not imply their requested effects completed.
- Retain one screenshot per surface and viewport under SWU-SCW-007 evidence.

## Gates

- Dependency/context/write scope/validation: pass.
- Blocker decisions: none.
- Strict coverage: pass, six of six obligations.

## Required Evidence

- Dedicated Node source/fixture contract test.
- Dedicated Playwright three-surface journey on desktop and mobile.
- Exact CLI poll payloads and stable event ids across reload/duplicate poll.
- Full bridge/e2e regression and visual inspection of retained screenshots.
