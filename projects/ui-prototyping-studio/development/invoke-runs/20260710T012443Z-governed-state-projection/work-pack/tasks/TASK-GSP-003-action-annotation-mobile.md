# TASK-GSP-003 - Durable Action Framing, Annotation, Mobile

## Objective

Make durable reversible actions and first-pass annotation/mobile comparison
usable enough that the operator understands what will stick.

## Source Contracts

- `projects/ui-prototyping-studio/backend/src/cli/studio.ts`
- `projects/ui-prototyping-studio/TEST-PROTOCOL.md`
- `projects/ui-prototyping-studio/development/research/20260709-ux-ui-upgrade-research/findings.md`

## Smallest Working Units

### SWU-GSP-003

- Goal: add confirmation framing for Accept/Revert and fix the first
  annotation/mobile inspectability slice.
- Dependencies: `SWU-GSP-001`.
- Write scope:
  - `backend/src/cli/studio.ts`
  - focused e2e spec
- Implementation detail:
  1. Replace one-click Accept/Revert with a lightweight confirmation panel or
     disabled-post flow that shows candidate/revision id, diff recap, target
     state, and "I inspected this change" confirmation.
  2. Keep Export absent from browser buttons.
  3. Hide/disable annotation form until target selection; replace free-text
     severity with constrained values.
  4. Add selected target label and captured comment count.
  5. Stack or segment before/after panes at mobile width.
- Edge cases:
  - staged candidate missing;
  - revert unavailable at baseline;
  - annotation click without `data-od-id`;
  - 390px viewport.
- Done criteria:
  - Accept/Revert cannot advance history without explicit confirmation state;
  - mobile before/after is inspectable;
  - annotation form no longer presents a blank target as ready.
- Acceptance evidence:
  - Playwright desktop + mobile assertions;
  - screenshot receipt for 390px staged comparison.
- Validation command:
  - `cd projects/ui-prototyping-studio/backend && ./node_modules/.bin/playwright test e2e/action-annotation-mobile.spec.ts --reporter=list`
- Execution owner: task-session.
