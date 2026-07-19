---
module: ide-extension-open-poll-bridge
taskId: TASK-WITNESS
swuId: SWU-OPB-007
status: pass
capability_ref: task-session
receipt_kind: local-fallback
createdAt: 2026-07-17T01:05:54Z
---

# TASK SESSION RESULT: SWU-OPB-007

## Scope

Add Node witness for open ready, non-Codex claim, race, result, replay, and
restart.

## Context Pack

- Mode: lean.
- Strict coverage: pass.
- Sources: W3 witness task, bridge server, claim/result APIs, and existing
  bridge integration tests.
- Controlling obligations: no-query ready, ignored selector, no pre-claim skill
  leak, one non-Codex race winner, loser secrecy, result receipt identity, and
  restart replay.

## Decisions

- No blocker decisions.

## Files Updated

- `projects/ide-extension/tests/manual-session-bridge-open-poll-witness.test.mjs`

## Validation

- PASS: `node --test --test-concurrency=1 projects/ide-extension/tests/manual-session-bridge-open-poll-witness.test.mjs`
  - 1 witness test passed.
- PASS: `npm --prefix projects/ide-extension run test:bridge`
  - 68 tests passed.
- PASS: scoped `git diff --check`.

## Result

PASS. The Node witness proves the core open-poll route with
`openrouter.local-session`, including race secrecy and restart replay.

## Reroute

Proceed to `SWU-OPB-008`.
