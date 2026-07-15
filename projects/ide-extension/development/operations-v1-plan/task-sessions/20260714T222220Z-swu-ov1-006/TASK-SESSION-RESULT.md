# Task Session Result: SWU-OV1-006

```yaml
swu_id: SWU-OV1-006
result: pass
capability_ref: task-session
receipt_kind: local-fallback
receipt_artifact: development/operations-v1-plan/task-sessions/20260714T222220Z-swu-ov1-006/TASK-SESSION-RESULT.md
files_touched:
  - package.json
  - src/kernel/operations.mjs
  - src/server.mjs
  - scripts/session-bridge.mjs
  - tests/operations-v1-replace.test.mjs
validation:
  - npm run test:operations-replace: pass
  - npm run test:operations-transform: pass
  - npm run test:operations-derive: pass
  - npm run test:operations-replay: pass
  - npm run test:canvas-publish: pass
  - npm run test:canvas-replay: pass
  - npm run test:canvas-paths: pass
  - npm run test:persistence: pass
  - npm run test:bridge-cli: pass
  - Node syntax and scoped whitespace checks: pass
blockers: []
residue:
  - Append and rebuild remain explicitly unavailable until SWU-OV1-007 and SWU-OV1-008.
  - Browser delivery and durable navigation remain deferred; replacement only emits a notice when its Operations surface is already selected.
  - Pruned content behavior is projected and served as 410, but retention deletion remains deferred.
  - Trusted-local HTML is parsed and stored inertly server-side; browser execution safety is not claimed.
  - Unrelated concurrent worktree changes remain preserved outside this SWU.
reroute: SWU-OV1-007
handoff_note: Reuse the same operation digest, CAS, blob, event, content, and CLI path for deterministic body-context append.
```

## Result

PASS. The derived Operations surface now supports retry-safe whole-document
replacement and immutable revision content through:

- `POST /api/canvas/operation-surfaces/:surfaceId/operations`;
- `GET /api/canvas/operation-surfaces/:surfaceId/revisions/:revisionId/content`;
- `session-bridge.mjs operate`.

The service hashes exact inline UTF-8 bytes, replaces the raw body with that
digest in fixed-order normalized JSON, and looks up `operation_id` before CAS.
Same-id/same-digest returns the original operation, revision, content URL, and
operation-time surface snapshot even after later commits. Same-id/different-
input fails `operation_id_conflict`. A new operation must match the current
revision or fails `revision_changed` without transformation, blob, or event.

Accepted replacement uses the pinned parse5 8.0.1 complete-document serializer,
enforces 4 MiB input and 8 MiB serialized-result limits, stores exact result
bytes before the V4 content event, and appends one ordered immutable revision.
Distinct operations may share a result digest and blob while retaining separate
operation and revision identities.

Content reads resolve event-derived Operations lineage and verified blobs only;
they never reread mutable workspace files. Unknown lineage returns 404, a
durable tombstone returns stable 410 metadata, and both old and current
unpruned revisions survive restart byte-for-byte. Replacement does not change
V0 current selection or durably redirect the workbench.

## Recovery

Scoped review caught one exact-retry defect before receipt: after a later
commit, retry returned the original operation/revision with the newer live
surface snapshot. The result projector now reconstructs the operation-time
surface from ordered lineage and `committed_at`; the test requires exact surface
equality with the original response.

The focused suite also proves two-writer stale CAS, shared-result deduplication,
append/rebuild deferral, route binding, unknown surface, input and expansion-
driven result limits, append-failure orphan reporting, event-success/projection-
failure repair, CLI operation, restart, and tombstone 410.

## Validation Evidence

| Command | Result |
| --- | --- |
| `npm run test:operations-replace` | PASS: 7 tests. |
| `npm run test:operations-transform` | PASS: 6 tests. |
| `npm run test:operations-derive` | PASS: 6 tests. |
| `npm run test:operations-replay` | PASS: 8 tests. |
| `npm run test:canvas-publish` | PASS: 4 tests. |
| `npm run test:canvas-replay` | PASS: 4 tests. |
| `npm run test:canvas-paths` | PASS: 5 tests. |
| `npm run test:persistence` | PASS: 6 tests. |
| `npm run test:bridge-cli` | PASS: 3 tests. |
| Service/server/CLI syntax checks | PASS. |
| Scoped `git diff --check` | PASS. |

## Session Metadata

- Context pack: [CONTEXT-PACK.md](CONTEXT-PACK.md)
- Gate: [GATE.md](GATE.md)
- Strict context coverage: pass, 12/12 obligations
- Gate verdict: pass
- Runtime: local
- Handoff: none
- Subagents: not applicable; started 0, completed 0, failed 0, blocked 0
- Experiment harness: not applicable
- Next bounded unit: `SWU-OV1-007`
