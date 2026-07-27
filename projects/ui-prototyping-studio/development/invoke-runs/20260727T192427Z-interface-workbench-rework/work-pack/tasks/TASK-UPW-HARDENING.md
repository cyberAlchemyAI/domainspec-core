# TASK-UPW-HARDENING — Bounded Semantics And Security

## Objective

Close the named accessibility-semantics and frame/route security contracts
without claiming certification or release.

- Layer/wave: L2 / W4
- Dependencies: SWU-UPW-015

## SWU-UPW-016 — Keyboard, Focus, Live Region, And Color Semantics

- Primary behavior: keyboard/pointer parity, visible/bounded focus movement,
  exact live scopes, and non-color-only communication.
- Write scope: shell interaction/status styles and
  `backend/e2e/workbench-accessibility.spec.ts`.
- Algorithm: route keyboard/pointer to the same handlers; retain focus after
  nonterminal feedback; move it to the new task heading only when transition
  removes the control; use polite atomic `cf-msg`, `act-msg`, `act-msg2`; use
  assertive status only for the separately tested blocking condition; pair
  color with text/state.
- Edge cases: disabled control, stale invalidation, region removal, recoverable
  network error, blocking malformed state.
- Acceptance: UPW-FIX-008–012, 021–022 exact checks pass; no accessibility
  completeness claim.
- Validation:
  `./node_modules/.bin/playwright test e2e/workbench-accessibility.spec.ts --reporter=list`
- Split analysis: these properties form one interaction-semantic contract; size
  and contrast calibration remain exact assertions within it, not a second UI
  feature.

## SWU-UPW-017 — Sandbox And Route-Family Validation

- Primary behavior: frames keep required sandbox attributes and projection
  routes fail closed outside allowlisted local families.
- Write scope: projection route validation, shell frame renderer, unit tests,
  `backend/e2e/workbench-security.spec.ts`.
- Algorithm: validate route strings server-side before versioning; allow only
  exact current local families; render allowlisted attributes; reject
  external/unknown routes without patching; keep annotation’s narrow
  `allow-scripts` exception and all other raw frames fully sandboxed.
- Edge cases: protocol-relative URLs, encoded traversal, unknown variant route,
  missing/expanded sandbox tokens, raw outer-shell HTML.
- Acceptance: UPW-FIX-023–024 and existing injection negative pass.
- Validation:
  `./node_modules/.bin/playwright test e2e/workbench-security.spec.ts --reporter=list`
- Split analysis: route validation and sandbox rendering jointly enforce one
  browser boundary; accessibility behavior passes independently in 016.

## Execution Owner And Handoff

Both SWUs: `subagent`, serial. Return exact negative-fixture evidence and
preserve the loopback/no-remote-origin boundary.
