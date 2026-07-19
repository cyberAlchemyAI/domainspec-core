---
taskId: TASK-READY-CLAIM-API
module: ide-extension-open-poll-bridge
status: completed
layer: L0
wave: W1
---

# TASK-READY-CLAIM-API

Goal: implement open singleton ready polling, atomic non-Codex claim, and
claim-bound result receipts.

## SWUs

### SWU-OPB-003

- Goal: make ready polling caller-neutral and selector-free.
- Dependencies: `SWU-OPB-002`.
- Write scope: server bridge route/kernel helpers and API tests.
- Done: ready endpoint works without `agent_ref`; any supplied query identity is
  ignored as selector; pre-claim payload remains safe.
- Validation: focused ready/API tests plus `npm --prefix projects/ide-extension run test:bridge`.
- Status: completed.
- Evidence: [TASK-SESSION-RESULT.md](../../task-sessions/20260717T005841Z-swu-opb-003/TASK-SESSION-RESULT.md).

### SWU-OPB-004

- Goal: bind non-Codex claim/result identity and preserve race secrecy.
- Dependencies: `SWU-OPB-003`.
- Write scope: claim/result handlers, receipts, concurrency tests.
- Done: exactly one claimant wins; loser response omits payload; result receipt
  uses stored claimant identity.
- Validation: focused claim/result/race tests and `npm --prefix projects/ide-extension run test:bridge`.
- Status: completed.
- Evidence: [TASK-SESSION-RESULT.md](../../task-sessions/20260717T010003Z-swu-opb-004/TASK-SESSION-RESULT.md).

## Edge Cases

- Claim request without identity fails clearly.
- Duplicate claim returns safe closed/unavailable state.
- Restart after claim still remembers claimant.
