# Task Session Result: SWU-OV1-012

```yaml
swu_id: SWU-OV1-012
result: pass
capability_ref: task-session
receipt_kind: local-fallback
receipt_artifact: development/operations-v1-plan/task-sessions/20260715T002431Z-swu-ov1-012-resume/TASK-SESSION-RESULT.md
files_touched:
  - package.json
  - src/kernel/canvas-blobs.mjs
  - src/kernel/canvas-retention.mjs
  - src/kernel/operations-contracts.mjs
  - src/kernel/projector.mjs
  - src/server.mjs
  - tests/operations-v1-contracts.test.mjs
  - tests/operations-v1-replay.test.mjs
  - tests/operations-v1-retention-auto.test.mjs
  - development/operations-v1-plan/task-sessions/20260714T234403Z-swu-ov1-012/DECISION-GATE.md
  - development/operations-v1-plan/task-sessions/20260715T002431Z-swu-ov1-012-resume/*
validation:
  - npm run test:operations-retention-auto: pass, 8/8
  - node --test --test-concurrency=1 tests/operations-v1-*.test.mjs: pass, 75/75
  - npm run test:operations-retention: pass, 6/6
  - npm run test:persistence: pass, 6/6
  - npm run test:workbench: pass, 6/6
  - npm run validate:schemas: pass, 21 schemas, 6 manifests, 78 fixtures
  - node --test --test-concurrency=1 tests/*.test.mjs: 185/186; one inherited non-SWU assertion mismatch
  - module imports and scoped whitespace checks: pass
blockers: []
residue:
  - session-content-workbench-matrix.test.mjs still forbids /api/craft/* even though the pre-existing Craft frontier intentionally exposes /api/craft/frontier; reconcile before SWU-OV1-014 integrated closeout.
  - The separate Session Content Workbench human usefulness gate remains open and does not block SWU-OV1-013 execution.
  - Unrelated concurrent worktree changes remain preserved outside this SWU.
reroute: SWU-OV1-013
handoff_note: W5 is complete. Add CLI value commands and retained interactive evidence without changing the proven retention/event contracts; stop for the SWU-013 human usefulness review.
```

## Result

PASS. The user-selected `OV1-EVENT-V4-M2` migration adds the exact
`canvas.pruning_completed` event. Replay accepts it only for the active request
and a final physical total below that request's soft limit, then durably records
completion, returns retention to Normal, and clears the request. Existing V4
histories and revision-tombstone semantics remain unchanged.

Automatic evaluation now runs after successful startup reconciliation and
after non-idempotent blob-producing or pruning commits. It opens one durable
grace request at soft, reclaims immediately at hard, reclaims after deadline
expiry, and schedules one injected/cancellable deadline timer otherwise. Timer
callbacks re-enter the server's existing mutation queue; manual/timer races
cannot double-prune.

Every destructive run reconciles again first. It removes regular stale
temporary files and replay-proven orphan blobs before selecting historical
revisions through the same oldest/shared-reference-aware candidate algorithm
as manual pruning. Automatic revision tombstones commit before body deletion
and remain `reclaiming`; only a verified completion event closes the cycle.
Current, displayed, shared-still-referenced, and un-tombstoned bodies remain
protected.

Failures do not turn a committed user operation into an HTTP failure. They
produce explicit cleanup diagnostics and leave replayable state for the next
startup/evaluation. Restart recovers both expired grace and a process stop
between tombstone append and physical deletion. Invalid history or corrupt
committed blobs fail readiness before any delete call.

## Automatic Matrix

Focused tests prove hard crossing before grace, shared digest references,
expired-grace restart, orphan-plus-temporary-only completion, one timer,
timer/manual serialization, append failure, deletion failure, restart recovery,
all-current non-convergence, malformed history, corrupt blobs, and process
close timer cancellation. Production 1 GiB/2 GiB/seven-day defaults remain
fixed; only tests inject thresholds, clocks, and timers.

## Validation Evidence

| Command | Result |
| --- | --- |
| `npm run test:operations-retention-auto` | PASS: 8 tests. |
| Full Operations V1 Node matrix | PASS: 75 tests. |
| `npm run test:operations-retention` | PASS: 6 manual-retention tests. |
| `npm run test:persistence` | PASS: 6 recovery tests. |
| `npm run test:workbench` | PASS: 6 workbench/Craft tests. |
| `npm run validate:schemas` | PASS: 21 schemas, 6 manifests, 78 fixtures. |
| Complete top-level Node matrix | 185 PASS, 1 inherited generic-matrix assertion mismatch for the existing `/api/craft/frontier` route. |
| Runtime imports and `git diff --check` | PASS. |

The inherited matrix mismatch is not caused by SWU-012 and does not contradict
its done criteria. It is retained as explicit integrated-audit residue rather
than silently changing another feature's contract here.

## Session Metadata

- Context pack: [CONTEXT-PACK.md](CONTEXT-PACK.md)
- Gate: [GATE.md](GATE.md)
- Decision: [../20260714T234403Z-swu-ov1-012/DECISION-GATE.md](../20260714T234403Z-swu-ov1-012/DECISION-GATE.md)
- Migration: [EVENT-V4-MIGRATION.md](EVENT-V4-MIGRATION.md)
- Strict context coverage: pass, 14/14 obligations
- Gate verdict: pass
- Runtime: local
- Handoff: none
- Subagents: not applicable; started 0, joined 0, closed 0, blocked 0, timed out 0, handed off 0, open 0
- Experiment harness: not applicable
- L2 promotion: W5 complete; W6 ready
- Next bounded unit: `SWU-OV1-013`
