---
module: ide-extension-open-poll-bridge
taskId: TASK-SESSION-WORKBENCH
swuId: SWU-OPB-005
status: pass
capability_ref: task-session
receipt_kind: local-fallback
createdAt: 2026-07-17T01:01:36Z
---

# TASK SESSION RESULT: SWU-OPB-005

## Scope

Update session bridge CLI/protocol for open ready and claim identity.

## Context Pack

- Mode: lean.
- Strict coverage: pass.
- Sources: `scripts/session-bridge.mjs`, CLI tests, protocol doc, and W2 task
  contract.
- Controlling obligations: ready command sends no selector; claim accepts
  explicit `--agent-ref`; Codex remains only a compatibility default; CLI does
  not gain operator-only commands.

## Decisions

- No blocker decisions.
- Assumption: retaining `codex.current-session` as the default is useful for
  current manual sessions while explicit `--agent-ref` proves the open protocol.

## Files Updated

- `projects/ide-extension/scripts/session-bridge.mjs`
- `projects/ide-extension/tests/manual-session-bridge-cli.test.mjs`
- `projects/ide-extension/SESSION-BRIDGE-PROTOCOL.md`

## Validation

- PASS: `npm --prefix projects/ide-extension run test:bridge-cli`
  - 3 tests passed.
- PASS: `npm --prefix projects/ide-extension run test:bridge`
  - 67 tests passed.
- PASS: scoped `git diff --check`.

## Result

PASS. The session CLI now polls open availability without a selector and binds
claim identity through `--agent-ref`, with Codex kept only as the default label.

## Reroute

Proceed to `SWU-OPB-006`.
