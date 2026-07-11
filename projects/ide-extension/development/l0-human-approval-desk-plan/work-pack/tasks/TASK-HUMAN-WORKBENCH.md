# TASK-HUMAN-WORKBENCH

## Objective

Expose the repaired kernel as a restrained, accessible local Approval Desk and prove the workflow in a real browser.

- Layer/slice: L0 / S-004
- Wave: W3
- Dependencies: TASK-PERSISTENCE-EVIDENCE
- Source contracts: existing `public/demo/l0.html`, SPEC acceptance, IDE Ergonomics restraint inherited by architecture, evidence APIs from SWU-007
- Blockers: Playwright browser availability is fail-closed at SWU-009.

## Interaction Contract

- The first screen is the actual workbench, not a landing page.
- The proposal queue is scannable and selectable.
- Details expose task, agent ref, normalized grants, state, timestamps, and evidence links.
- Approve and reject are explicit commands with confirmation appropriate to a no-op local action.
- The UI says `local operator action` or equivalent, never `verified human`.
- Terminal proposals remain in history and cannot be acted on again.
- Errors remain visible without destroying the selected proposal.

## Smallest Working Units

### SWU-IDEAD-008: Queue, Detail, Disposition, History, And Evidence UI

- Goal: make all repaired L0 behavior operable through the local HTML page.
- Dependencies: SWU-IDEAD-007.
- Write scope: `src/server.mjs` read/detail endpoints, `public/demo/l0.html`, smoke/DOM-level tests.
- Source anchors: current `render()`, prepare and approve handlers, `/api/state`; final lifecycle and evidence shapes.
- Related context: DEC-IDEAD-001/002/007 and Nimbalyst precedent recommendation to keep one restrained next governed step and honest evidence.

#### Required Behavior

1. Prepare at least two proposals without hiding either.
2. Select a proposal from the queue/history and inspect its complete L0 contract.
3. Approve or reject only a pending selected proposal.
4. Disable terminal actions while preserving details and evidence.
5. Show receipt and before/after evidence through bounded read-only API projections; never expose arbitrary filesystem paths.
6. Preserve selection when state refreshes where the selected ID still exists.
7. Use semantic buttons, lists/tables, focus states, status announcements, stable `data-*` selectors, and responsive dimensions.
8. Render untrusted values as text, not interpolated HTML.

- Edge cases: no proposals; stale selected ID; concurrent disposition conflict; server validation error; missing evidence; long task/grant text; narrow viewport.
- Done criteria: a person can complete prepare/inspect/approve, prepare/inspect/reject, reload, and history/evidence review without using raw JSON endpoints.
- Acceptance evidence: updated smoke assertions and screenshots/snapshots prepared for SWU-009.
- Validation: `npm run smoke` plus focused UI/API tests.
- Execution owner: local-fallback.
- Handoff note: return stable browser selectors and the exact end-to-end flow.

### SWU-IDEAD-009: Playwright Human Workflow Proof

- Goal: prove the complete L0 job in a real browser against an isolated local server/state directory.
- Dependencies: SWU-IDEAD-008.
- Write scope: Playwright dependency/config, `tests/e2e/l0-approval-desk.spec.*`, package test script, test-only server harness.
- Source anchors: UI selectors from SWU-008; SPEC acceptance; GAP-IDEAD-004.
- Related context: existing loopback host strategy.

#### Required Scenarios

1. Page renders nonblank at desktop and mobile viewports with no incoherent overlap.
2. Prepare A and B; both remain navigable.
3. Approve A once; replay action is unavailable and direct replay returns conflict.
4. Reject B; no passed receipt is created for B.
5. Reload; terminal states, selection fallback, receipt, and evidence remain reachable.
6. Open before/after evidence and verify bound IDs.
7. Keyboard traversal reaches queue and disposition controls with visible focus.
8. Browser console has no unexpected errors.

- Failure mode: if the required browser is unavailable, return BLOCK with the exact project-scoped install command; do not replace browser proof with HTTP assertions.
- Done criteria: scenarios pass at one desktop and one mobile viewport using temporary state.
- Acceptance evidence: Playwright report and two screenshots stored as test/session evidence, not canonical app assets.
- Validation: `npm run test:e2e` and the full validation command in TASK-VERIFY-READINESS.
- Execution owner: local-fallback.
- Handoff note: return report paths, screenshot paths, viewport list, console result, and any visual residue.

## Synchronization

Do not add explanatory marketing copy or imply external-agent capability. Keep the UI destination-native and work-focused.
