---
module: ide-extension-open-poll-bridge
version: current
status: planned
updatedAt: 2026-07-16
docType: execution-pack
---

# EXECUTION-PACK: Open Poll Bridge

## Execution Policy

- One Task Session per SWU.
- Use the SWU contract as the execution boundary.
- Keep writes inside `projects/ide-extension` unless the SWU explicitly names a
  plan/status artifact.
- Preserve unrelated dirty worktree changes.
- Return `block` if a SWU needs L1/L3 scope to pass.

## Wave Order

1. W0 contract identity: `SWU-OPB-001`, then `SWU-OPB-002`.
2. W1 API kernel: `SWU-OPB-003`, then `SWU-OPB-004`.
3. W2 session/workbench: `SWU-OPB-005` and `SWU-OPB-006` after W1.
4. W3 witness/readiness: `SWU-OPB-007`, `SWU-OPB-008`, `SWU-OPB-009`.

## Common Validation Surface

Use focused tests first, then broaden at closure:

```bash
npm --prefix projects/ide-extension run validate:schemas
npm --prefix projects/ide-extension run test:schemas
npm --prefix projects/ide-extension run test:bridge
npm --prefix projects/ide-extension run test:workbench
npm --prefix projects/ide-extension run test:e2e
git diff --check -- projects/ide-extension/development/open-poll-bridge-plan projects/ide-extension
```

## Stop Rules

- Stop if ready polling still depends on a caller `agent_ref`.
- Stop if a pre-claim response leaks `requested_skill`.
- Stop if result identity can be supplied independently of the stored claim.
- Stop if a race loser sees task payload.
- Stop if passing requires queue semantics, background polling, or authenticated
  workers.
