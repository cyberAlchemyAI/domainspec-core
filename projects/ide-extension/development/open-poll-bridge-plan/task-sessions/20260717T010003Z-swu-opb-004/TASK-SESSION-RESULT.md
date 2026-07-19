---
module: ide-extension-open-poll-bridge
taskId: TASK-READY-CLAIM-API
swuId: SWU-OPB-004
status: pass
capability_ref: task-session
receipt_kind: local-fallback
createdAt: 2026-07-17T01:00:03Z
---

# TASK SESSION RESULT: SWU-OPB-004

## Scope

Bind non-Codex claim/result identity and preserve race secrecy.

## Context Pack

- Mode: lean.
- Strict coverage: pass.
- Sources: claim API tests, result API tests, result admission handler, bridge
  suite, and W1 task contract.
- Controlling obligations: non-Codex claim wins once; race losers receive safe
  state; result receipt uses the stored claimant identity.

## Decisions

- No blocker decisions.
- Assumption: `openrouter.local-session` is the current proof identity for the
  local non-Codex claimant.

## Files Updated

- `projects/ide-extension/tests/manual-session-bridge-claim-recovery.test.mjs`
- `projects/ide-extension/tests/manual-session-bridge-result.test.mjs`

## Validation

- PASS: `npm --prefix projects/ide-extension run test:bridge-claim`
  - 5 tests passed.
- PASS: `npm --prefix projects/ide-extension run test:bridge-result`
  - 6 tests passed.
- PASS: `npm --prefix projects/ide-extension run test:bridge`
  - 67 tests passed.

## Result

PASS. The API evidence now explicitly proves a non-Codex claimant can win a
claim, race losers do not receive the execution payload, and result receipts
preserve the stored claimant identity.

## Reroute

Proceed to `SWU-OPB-005`.
