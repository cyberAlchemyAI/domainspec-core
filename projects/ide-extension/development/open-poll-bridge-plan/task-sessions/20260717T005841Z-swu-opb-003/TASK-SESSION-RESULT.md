---
module: ide-extension-open-poll-bridge
taskId: TASK-READY-CLAIM-API
swuId: SWU-OPB-003
status: pass
capability_ref: task-session
receipt_kind: local-fallback
createdAt: 2026-07-17T00:58:41Z
---

# TASK SESSION RESULT: SWU-OPB-003

## Scope

Make ready polling caller-neutral and selector-free.

## Context Pack

- Mode: lean.
- Strict coverage: pass.
- Sources: ready endpoint route, authorization tests, claim recovery tests,
  bridge suite, and W1 plan contract.
- Controlling obligations: `GET /api/bridge/requests/ready` works without
  `agent_ref`, ignores query identity, and does not disclose task/skill before
  claim.

## Decisions

- No blocker decisions.
- Assumption: existing query parameters are tolerated for compatibility but have
  no selector authority.

## Files Updated

- `projects/ide-extension/src/server.mjs`
- `projects/ide-extension/tests/manual-session-bridge-authorization.test.mjs`
- `projects/ide-extension/tests/manual-session-bridge-claim-recovery.test.mjs`

## Validation

- PASS: `npm --prefix projects/ide-extension run test:bridge-authorization`
  - 7 tests passed.
- PASS: `npm --prefix projects/ide-extension run test:bridge-claim`
  - 5 tests passed.
- PASS: `npm --prefix projects/ide-extension run test:bridge`
  - 67 tests passed.

## Result

PASS. Ready polling is now an open availability endpoint: no selector is
required, query `agent_ref` is ignored, and pre-claim payload remains private.

## Reroute

Proceed to `SWU-OPB-004`.
