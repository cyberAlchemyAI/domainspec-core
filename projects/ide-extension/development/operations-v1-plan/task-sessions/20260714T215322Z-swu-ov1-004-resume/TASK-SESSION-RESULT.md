# Task Session Result: SWU-OV1-004

```yaml
swu_id: SWU-OV1-004
result: pass
capability_ref: task-session
receipt_kind: local-fallback
receipt_artifact: development/operations-v1-plan/task-sessions/20260714T215322Z-swu-ov1-004-resume/TASK-SESSION-RESULT.md
decision_gate: DEC-IDEEXT-OV1-V4-INTERACTION option 1
contract_migration: OV1-EVENT-V4-M1
files_touched:
  - package.json
  - src/kernel/operations-contracts.mjs
  - src/kernel/projector.mjs
  - src/kernel/storage.mjs
  - tests/fixtures/events/operations-v1-lifecycle.jsonl
  - tests/operations-v1-contracts.test.mjs
  - tests/operations-v1-replay.test.mjs
  - tests/session-content-workbench-replay.test.mjs
  - tests/manual-session-bridge-replay.test.mjs
validation:
  - npm run test:operations-replay: pass
  - npm run test:operations-contracts: pass
  - npm run test:canvas-replay: pass
  - npm run test:bridge-replay: pass
  - npm run test:persistence: pass
  - npm run test:workbench: pass
  - Node syntax and scoped whitespace checks: pass
blockers: []
residue:
  - V4 event-producing HTTP, CLI, browser, and operation-service routes remain intentionally deferred to later SWUs.
  - Blob diagnostics expose valid orphan residue but do not delete it; retention authority remains deferred.
  - Any storage caller replaying unpruned V4 revisions must inject the Canvas blob store.
  - Pruning reducers freeze normal, grace, and reclaiming transitions but do not implement threshold evaluation or deletion.
  - Unrelated concurrent worktree changes remain preserved outside this SWU.
reroute: SWU-OV1-005
handoff_note: Derive one Operations V1 surface from an exact admitted V0 revision using the frozen V4 event and blob-before-event substrate.
```

## Result

PASS. Event version 4 now adds an Operations V1 namespace beneath Canvas
without changing exact V1, V2, or V3 projections. The human-selected migration
reuses `canvas.interaction_recorded`; `event_version` distinguishes its V3 V0
binding from its V4 Operations binding.

The pure projector now validates and reduces six exact V4 event shapes:

- surface derivation with one idempotency-key/input-digest outcome;
- content commit with unique operation identity, current-source CAS lineage,
  whole-document target, and result digest/ref bindings;
- durable redirect command and admitted display target;
- threshold/grace pruning request;
- revision tombstone with current/display protection and explicit retention
  state transition;
- interaction bound to the exact displayed, unpruned Operations revision.

`canvas.operations_v1` projects derivation keys, independent surface and
revision lineage, operation records, redirect history/display target, pruning
state, tombstones, and interaction history. Existing V0 Canvas fields remain
unchanged and current V0 selection is not redirected by derivation or content
events.

Storage reconciliation remains event-authoritative and now verifies every
unpruned Operations revision through the content-addressed blob store before a
projection is usable. Missing, corrupt, or metadata-mismatched bodies fail
closed. Commit validates the blob before append; if append succeeds and
projection replacement fails, the event remains authoritative and the next
reconciliation repairs the projection without misclassifying its body as an
orphan.

## Recovery Matrix

The focused suite proves mixed V3/V4 replay, exact legacy projection, unknown
V4/future-version rejection, duplicate derivation and operation identities,
stale and outside-lineage operation results, current-revision prune rejection,
interaction target mismatch, restart reconstruction, valid orphan reporting,
missing/corrupt reference failure, no-store failure before append, and
append-success/projection-failure recovery.

## Validation Evidence

| Command | Result |
| --- | --- |
| `npm run test:operations-replay` | PASS: 8 tests. |
| `npm run test:operations-contracts` | PASS: 8 tests. |
| `npm run test:canvas-replay` | PASS: 4 tests. |
| `npm run test:bridge-replay` | PASS: 7 tests. |
| `npm run test:persistence` | PASS: 6 tests. |
| `npm run test:workbench` | PASS: 6 tests, including stale-index refusal. |
| Projector/storage syntax checks | PASS. |
| Scoped `git diff --check` | PASS. |

## Session Metadata

- Context pack: [CONTEXT-PACK.md](CONTEXT-PACK.md)
- Migration: [EVENT-V4-MIGRATION.md](EVENT-V4-MIGRATION.md)
- Prior BLOCK receipt: [../20260714T214740Z-swu-ov1-004/TASK-SESSION-RESULT.md](../20260714T214740Z-swu-ov1-004/TASK-SESSION-RESULT.md)
- Decision Gate: [../20260714T214740Z-swu-ov1-004/DECISION-GATE.md](../20260714T214740Z-swu-ov1-004/DECISION-GATE.md)
- Strict context coverage: pass, 12/12 obligations
- Gate: pass
- Runtime: local
- Handoff: none
- Subagents: not applicable; started 0, completed 0, failed 0, blocked 0
- Experiment harness: not applicable
- Next bounded unit: `SWU-OV1-005`
