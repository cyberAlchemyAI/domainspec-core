---
taskId: TASK-WITNESS
module: ide-extension-open-poll-bridge
status: completed
layer: L0
wave: W3
---

# TASK-WITNESS

Goal: prove the open-poll bridge works as a human-usable local loop.

## SWUs

### SWU-OPB-007

- Goal: add Node witness for open ready, non-Codex claim, race, result, replay,
  and restart.
- Dependencies: `SWU-OPB-005`, `SWU-OPB-006`.
- Write scope: integration/adversarial/recovery tests.
- Done: one non-Codex claimant wins; ten competing claims leave one winner;
  loser secrecy is preserved; replay/restart retain identity.
- Validation: `npm --prefix projects/ide-extension run test:bridge`.
- Status: completed.
- Evidence: [TASK-SESSION-RESULT.md](../../task-sessions/20260717T010554Z-swu-opb-007/TASK-SESSION-RESULT.md).

### SWU-OPB-008

- Goal: add Playwright/manual witness evidence for the workbench path.
- Dependencies: `SWU-OPB-007`.
- Write scope: `tests/e2e/`, checked-in evidence report/assets.
- Done: browser shows open availability; session claims with
  `openrouter.local-session`; result receipt is visible and claim-bound.
- Validation: `npm --prefix projects/ide-extension run test:e2e`; retained
  witness report.
- Status: completed.
- Evidence: [TASK-SESSION-RESULT.md](../../task-sessions/20260717T010713Z-swu-opb-008/TASK-SESSION-RESULT.md).

## Edge Cases

- If a live manual witness is unavailable, return `block` with automated proof
  retained, not a simulated manual pass.
- The debug `/api/state` surface is not evidence for the open poll contract.
