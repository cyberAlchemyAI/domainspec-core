# Context Pack: SWU-MSB-003

## Selection

- Work-pack: `projects/ide-extension/development/manual-session-bridge-plan/WORK-PACK.md`
- Task/SWU: `TASK-BRIDGE-KERNEL / SWU-MSB-003`
- Dependency receipt: `task-sessions/20260712T060816Z-swu-msb-002/TASK-SESSION-RESULT.md`
- Runtime: local Codex / Task Session
- Strict runtime handoff: not requested

## Controlling Sources

1. Bridge-kernel task contract: authorization receipt, singleton ready/unready,
   private pre-claim inventory, revocation, actor separation, restart, atomic events.
2. Approved architecture/decisions: manual poll, one selected target, no skill
   disclosure, read-only profile, separate receipts, unattested local actors.
3. SWU-001 schemas and SWU-002 v2 reducer/event contracts.
4. Current server mutation queue, storage append/reconcile, artifact interface,
   legacy dry-run helpers, and API/persistence tests.

## Brownfield Baseline

- Legacy prepare/approve/reject behavior and all 65 Node tests pass.
- The current server emits event v1 and approval terminalizes dry-run envelopes.
- Existing artifact IDs and routes can carry authorization artifacts without
  changing the receipt schema or exposing raw paths.
- The mutation queue serializes all state-changing HTTP routes.

## Execution Decision

- Select v2 preparation only for the exact bridge grants
  `preview.read + skill.invoke`; preserve all other legacy dry-run requests.
- Construct actor descriptors in the kernel; operator endpoints accept an empty
  body and reject caller-supplied identity fields.
- Keep authorization receipt and its before/after/receipt artifacts atomic with
  one v2 `approval.granted` event.
- Add ready/unready v2 events and a pre-claim GET projection containing only an
  opaque handle, state, effect profile, assurance, and timestamps.
- Reuse pending rejection; treat reject on approved/ready v2 requests as explicit
  revocation that preserves authorization evidence and clears the singleton.

## Gates

- Dependencies/W0: pass.
- Decisions: no unresolved blocker.
- Write scope: bridge envelope helper, server/projector integration, schemas,
  focused API tests, package script, and task evidence.
- Runtime/tool boundary: server still does not resolve or execute skills.
- Gate verdict: PASS.

## Done Evidence Required

- Exactly one authorization receipt survives replay/restart and has no status.
- Exactly one target can be ready; ready/unready/revoke persist across restart.
- Agent pre-claim inventory contains no task, skill, context, hashes, or token.
- Duplicate/stale/wrong-actor actions append no events.
- Injected append failure leaves no authorization event or projected receipt.
- Legacy Node suite remains green.
