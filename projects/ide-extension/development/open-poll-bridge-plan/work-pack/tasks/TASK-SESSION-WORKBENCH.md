---
taskId: TASK-SESSION-WORKBENCH
module: ide-extension-open-poll-bridge
status: completed
layer: L0
wave: W2
---

# TASK-SESSION-WORKBENCH

Goal: make the human and session surfaces express open availability without
adding automation.

## SWUs

### SWU-OPB-005

- Goal: update session bridge CLI/protocol for open ready and claim identity.
- Dependencies: `SWU-OPB-004`.
- Write scope: `scripts/session-bridge.mjs`, `SESSION-BRIDGE-PROTOCOL.md`,
  CLI tests.
- Done: ready command does not need a selector; claim accepts explicit
  `--agent-ref`; Codex is only a default label; CLI cannot perform operator
  recovery or inspect full debug state.
- Validation: `npm --prefix projects/ide-extension run test:bridge-cli`.
- Status: completed.
- Evidence: [TASK-SESSION-RESULT.md](../../task-sessions/20260717T010136Z-swu-opb-005/TASK-SESSION-RESULT.md).

### SWU-OPB-006

- Goal: update workbench labels and states from target/selected to
  available/claimed.
- Dependencies: `SWU-OPB-004`.
- Write scope: `public/demo/l0.html`, UI tests.
- Done: operator sees available/open/claimed/result language; no polling type
  selector implies exclusive routing.
- Validation: `npm --prefix projects/ide-extension run test:workbench`;
  browser inspection if UI changed.
- Status: completed.
- Evidence: [TASK-SESSION-RESULT.md](../../task-sessions/20260717T010408Z-swu-opb-006/TASK-SESSION-RESULT.md).

## Edge Cases

- Existing operators can still run the Codex path.
- Workbench must not expose requested skill before claim.
- No automatic polling loop is added.
