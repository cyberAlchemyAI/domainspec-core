---
taskId: TASK-CONTRACT-IDENTITY
module: ide-extension-open-poll-bridge
status: completed
layer: L0
wave: W0
---

# TASK-CONTRACT-IDENTITY

Goal: make the event contract and replay model express open availability and
claim-bound identity before behavior changes.

## SWUs

### SWU-OPB-001

- Goal: add schema fixtures for open ready and claim-bound `agent_ref`.
- Write scope: `projects/ide-extension/schemas/`, fixture/test files.
- Done: fixtures accept `openrouter.local-session` claim identity and reject
  malformed identity; ready fixtures do not require a selector.
- Validation: `npm --prefix projects/ide-extension run validate:schemas`;
  `npm --prefix projects/ide-extension run test:schemas`.
- Status: completed.
- Evidence: [TASK-SESSION-RESULT.md](../../task-sessions/20260717T005539Z-swu-opb-001/TASK-SESSION-RESULT.md).

### SWU-OPB-002

- Goal: update reducer/projector replay to preserve stored claim identity.
- Dependencies: `SWU-OPB-001`.
- Write scope: bridge event/projector modules and replay tests.
- Done: replay of existing v1 history still passes; v2/open bridge history
  preserves non-Codex claim identity through result.
- Validation: `npm --prefix projects/ide-extension run test:bridge-replay`;
  focused contract tests.
- Status: completed.
- Evidence: [TASK-SESSION-RESULT.md](../../task-sessions/20260717T005707Z-swu-opb-002/TASK-SESSION-RESULT.md).

## Edge Cases

- Existing Codex-shaped histories remain valid.
- Missing claim identity blocks result admission.
- Terminal result cannot override stored claim identity.
