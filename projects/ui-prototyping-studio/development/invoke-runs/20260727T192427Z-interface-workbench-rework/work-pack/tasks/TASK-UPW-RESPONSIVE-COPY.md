# TASK-UPW-RESPONSIVE-COPY — Mobile Order And State Copy

## Objective

Prove responsive semantic order and domain-faithful action language after all
six regions exist.

- Layer/wave: L1 / W3
- Dependencies: SWU-UPW-013
- Source: UX Plan Responsive/Content Contracts, FR-14

## SWU-UPW-014 — Responsive Semantic Order

- Primary behavior: at 390×844, spine/action and current task precede collapsed
  history without horizontal overflow or covering content.
- Write scope: workbench shell styles/layout plus
  `backend/e2e/action-annotation-mobile.spec.ts` or a focused responsive spec.
- Algorithm: preserve desktop canvas/inspector enhancement; use the same DOM
  order for mobile; stack staged frames; keep stable frame sources and usable
  control widths.
- Edge cases: long hashes/copy, unavailable regions, nested iframe scrolling,
  all lifecycle states.
- Acceptance: UPW-FIX-013 passes at 390×844 and desktop structure remains.
- Validation:
  `./node_modules/.bin/playwright test e2e/action-annotation-mobile.spec.ts --grep "mobile" --reporter=list`
- Split analysis: width, order, and overflow jointly establish one responsive
  behavior; region semantics were already split into 008–013.

## SWU-UPW-015 — State/Action Copy Matrix

- Primary behavior: browser wording names the current task and action while raw
  CLI detail remains secondary.
- Write scope: server projection labels/copy, shell rendering, focused copy
  matrix tests.
- Algorithm: define a literal per-state matrix; render “current head,” “staged
  candidate,” “recorded revision,” and “historical” consistently; prohibit
  unqualified approved/ready/safe/complete; keep Export terminal-only.
- Edge cases: unavailable content, recovery errors, RevisionApplied versus
  RevisionRecorded, SessionCompleted.
- Acceptance: UPW-FIX-020 and governance negatives pass.
- Validation:
  `./node_modules/.bin/playwright test e2e/workbench-copy.spec.ts --reporter=list`
- Split analysis: copy matrix is independently reviewable from responsive
  geometry.

## Execution Owner And Handoff

Both SWUs: `subagent`, serial. Synchronize the exact work-pack/task/wave rows
and receipts; do not update the human-test script until automated behavior
closes.
