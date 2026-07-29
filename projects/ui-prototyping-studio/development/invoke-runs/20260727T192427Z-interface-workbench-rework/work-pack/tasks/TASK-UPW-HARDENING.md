# TASK-UPW-HARDENING — Interaction, Visual, Route, And Frame Boundaries

Status: `not-started`

## Objective

Close four independently receiptable L2 boundaries without claiming
accessibility certification, remote-origin safety, release, or deployment.

- Layer/wave: L2 / W4
- Scope authority: `SWU-SCOPE-INVENTORY.json` rows 016–019
- Acceptance authority: `SWU-ACCEPTANCE-MATRIX.json` assertions 016–019
- Closeout authority: `CLOSEOUT-SYNC-INVENTORY.json` rows 016–019

The previous SWU-016 was split into interaction/status and visual/target
contracts. Scoped status remains with interaction because it shares the same
action event, feedback destination, focus transition, and live-region
acceptance boundary; a third child would duplicate that event contract. The
previous SWU-017 was split into server route admission and browser rendering.
All omitted paths are unauthorized.

## SWU-UPW-016 — Keyboard, Focus, Live Region, And Scoped Status

- Primary behavior: keyboard/pointer parity, bounded focus movement, and exact
  status urgency/scope.
- Semantic dependencies: SWU-UPW-010 and 012.
- Serialization-only predecessor: 015.
- Exact scope: `SWU-SCOPE-INVENTORY.json#SWU-UPW-016`.
- Algorithm: bind keyboard/pointer to the same handlers; retain focus after
  nonterminal feedback; move focus to the new task heading only when a
  transition removes the control; make only `#cf-msg`, `#act-msg`, and
  `#act-msg2` polite atomic status scopes; use assertive status only for the
  separately tested blocking error.
- Edge cases: disabled control, stale invalidation, region removal, recoverable
  network error, blocking malformed state, and unchanged poll.
- Split analysis: event activation, focus result, feedback destination, and
  live urgency form one interaction outcome. Visual contrast and target
  geometry have a separate calibrated acceptance and are 017.
- Validation:
  `./node_modules/.bin/playwright test e2e/workbench-accessibility.spec.ts --grep "UPW-016 keyboard focus and scoped status" --reporter=list`.
- Receipt: `validation.assertions.UPW_A_016_INTERACTION`.
- Owner/handoff: `subagent`; exact assertion includes the UPW-FIX-022 urgency
  sub-assertion, while its non-color sub-assertion belongs to 017.

## SWU-UPW-017 — Visual Perceivability And Target Geometry

- Primary behavior: calibrated contrast, visible focus, non-color-only cues,
  and outer-control target floor.
- Semantic dependencies: SWU-UPW-008, 010–014.
- Serialization-only predecessor: 016.
- Exact scope: `SWU-SCOPE-INVENTORY.json#SWU-UPW-017`.
- Algorithm: sample declared light-surface normal text using computed
  foreground/background compositing; require 4.5:1; measure outer action boxes
  at desktop/mobile and require 24×24 CSS px or record the designed exception;
  verify focus indicator perceivability; remove color cues and assert text/state
  remains.
- Edge cases: disabled controls, wrapped mobile actions, translucent
  backgrounds, nested iframe content excluded from the outer-shell claim, and
  high-contrast/zoom beyond the current bounded fixture left as residue.
- Split analysis: calibrated visual properties share one style/geometry
  acceptance; keyboard and live behavior pass independently in 016.
- Validation:
  `./node_modules/.bin/playwright test e2e/workbench-accessibility.spec.ts --grep "UPW-017 visual perceivability and targets" --reporter=list`.
- Receipt: `validation.assertions.UPW_A_017_VISUAL`.
- Owner/handoff: `subagent`; return raw ratios and bounding boxes, not only a
  boolean.

## SWU-UPW-018 — Server Route-Family Admission

- Primary behavior: every route field is admitted against exact local families
  before projection versioning.
- Semantic dependency: SWU-UPW-003.
- Serialization-only predecessor: 017; this is work-pack ordering, not a need
  for visual evidence.
- Exact scope: `SWU-SCOPE-INVENTORY.json#SWU-UPW-018`; browser shell and CLI
  renderer are explicitly forbidden.
- Algorithm:
  1. Parse the route as a path-only value; reject scheme, authority,
     protocol-relative, query, fragment, backslash, and decoded traversal.
  2. Admit exact `/raw/current`, `/annotate/current`, and `/raw/staged`.
  3. Admit `/raw/variant/{label}` only when `{label}` is exactly a valid
     `VariantLabel` segment.
  4. Validate every projection route before digesting/versioning.
  5. On rejection throw `ProjectionRouteRejectedError` with field/family but
     no reflected unsafe route; emit no projection.
- Relationship to 003: 003 uses only current internal constructors and claims
  no arbitrary route failure. 018 introduces the reusable admission boundary
  for current and later route-producing code.
- Split analysis: parsing and family checking jointly decide one server
  admission; iframe sandbox behavior is browser-owned and remains 019.
- Validation:
  `./node_modules/.bin/tsx --test src/modules/ui-prototyping-studio/application/workbench-route-admission.test.ts`.
- Receipt: `validation.assertions.UPW_A_018_ROUTES`.
- Owner/handoff: `subagent`; loopback-only and no remote origin expansion.

## SWU-UPW-019 — Sandbox And Safe Outer Rendering

- Primary behavior: admitted routes are rendered only into correctly sandboxed
  iframes and outer server data uses safe sinks.
- Semantic dependencies: SWU-UPW-009, 011, and 018.
- Exact scope: `SWU-SCOPE-INVENTORY.json#SWU-UPW-019`; route-admission source
  and tests are explicitly forbidden.
- Algorithm: create iframe nodes explicitly; raw current/staged/history frames
  receive an empty sandbox token set; annotation alone receives exact
  `allow-scripts`; set admitted route via allowlisted `src`; use `textContent`,
  explicit nodes, and allowlisted attributes for all outer data; reject
  unexpected attributes before mount.
- Edge cases: missing/expanded sandbox, raw outer HTML, quote/markup labels,
  encoded route already rejected by 018, and annotation token widening.
- Split analysis: sandbox and safe-sink enforcement are one browser rendering
  admission; server route validation passes independently in 018.
- Validation:
  `./node_modules/.bin/playwright test e2e/workbench-security.spec.ts --grep "UPW-019 sandbox and safe sinks" --reporter=list`.
- Receipt: `validation.assertions.UPW_A_019_RENDERING`.
- Owner/handoff: `subagent`; preserve the exact annotation exception and
  existing loopback/no-remote boundary.
