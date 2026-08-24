# TASK-UPW-RESPONSIVE-COPY — Mobile Order And State Copy

Status: `not-started`

## Objective

Prove mobile semantic order and domain-faithful browser language after the
region contracts close.

- Layer/wave: L1 / W3
- Scope authority: `SWU-SCOPE-INVENTORY.json` rows 014–015
- Acceptance authority: `SWU-ACCEPTANCE-MATRIX.json` assertions 014–015
- Closeout authority: `CLOSEOUT-SYNC-INVENTORY.json` rows 014–015

All omitted paths are unauthorized and declared targets use the preflight
digest/`ABSENT` contract.

## SWU-UPW-014 — Responsive Semantic Order

- Primary behavior: at 390×844, spine, active canvas, inspector/review, action,
  then collapsed history appear in one DOM order without document horizontal
  overflow or covering content.
- Semantic dependencies: SWU-UPW-008–013.
- Exact scope: `SWU-SCOPE-INVENTORY.json#SWU-UPW-014`.
- Algorithm: preserve one semantic DOM order; add desktop canvas/inspector
  enhancement; stack staged frames; constrain long hashes/copy; keep stable
  iframe identities and usable control widths.
- Edge cases: every lifecycle state, missing regions, nested frame scroll, long
  identities, and both desktop/mobile viewports.
- Split analysis: width, order, and overflow are one responsive behavior;
  region meaning is already separated into 008–013.
- Validation:
  `./node_modules/.bin/playwright test e2e/workbench-responsive.spec.ts --grep "UPW-014 mobile semantic order" --reporter=list`.
- Receipt: `validation.assertions.UPW_A_014_RESPONSIVE`.
- Owner/handoff: `subagent`; receive exact scope/assertion rows and all six
  synchronized region receipts.

## SWU-UPW-015 — State And Action Copy Matrix

- Primary behavior: browser wording names the current task/action while raw CLI
  detail remains secondary.
- Semantic dependencies: 008, 010, 011, 012, and 013.
- Serialization-only predecessor: 014 because both change shared shell output.
- Exact scope: `SWU-SCOPE-INVENTORY.json#SWU-UPW-015`.
- Algorithm: implement the literal state matrix from UX Plan; use “current
  head”, “staged candidate”, “recorded revision”, and “historical”
  consistently; prohibit unqualified approved/ready/safe/complete; retain
  Export as terminal-only secondary disclosure.
- Edge cases: unavailable content, recovery errors, RevisionApplied versus
  RevisionRecorded, SessionCompleted, and raw CLI-primary mutant.
- Split analysis: copy is independently reviewable from responsive geometry.
- Validation:
  `./node_modules/.bin/playwright test e2e/workbench-copy.spec.ts --grep "UPW-015 state and action copy matrix" --reporter=list`.
- Receipt: `validation.assertions.UPW_A_015_COPY`.
- Owner/handoff: `subagent`; do not update the human-test script or claim human
  comprehension.
