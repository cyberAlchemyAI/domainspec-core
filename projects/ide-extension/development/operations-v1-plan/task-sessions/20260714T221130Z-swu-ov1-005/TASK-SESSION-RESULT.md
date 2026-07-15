# Task Session Result: SWU-OV1-005

```yaml
swu_id: SWU-OV1-005
result: pass
capability_ref: task-session
receipt_kind: local-fallback
receipt_artifact: development/operations-v1-plan/task-sessions/20260714T221130Z-swu-ov1-005/TASK-SESSION-RESULT.md
files_touched:
  - package.json
  - src/kernel/operations.mjs
  - src/server.mjs
  - scripts/session-bridge.mjs
  - tests/operations-v1-derive.test.mjs
validation:
  - npm run test:operations-derive: pass
  - npm run test:canvas-publish: pass
  - npm run test:canvas-paths: pass
  - npm run test:canvas-replay: pass
  - npm run test:operations-replay: pass
  - npm run test:persistence: pass
  - npm run test:bridge-cli: pass
  - Node syntax and scoped whitespace checks: pass
blockers: []
residue:
  - Operations revision content serving begins in SWU-OV1-006; SWU-OV1-005 exposes metadata only.
  - Exact V0 admission still depends on mutable workspace bytes matching the selected revision; drift and deletion fail closed.
  - Blob write plus event-append failure leaves reported orphan residue for later retention authority.
  - Derivation is local trusted-workbench behavior and does not add remote, approval, navigation, or browser control.
  - Unrelated concurrent worktree changes remain preserved outside this SWU.
reroute: SWU-OV1-006
handoff_note: Add CAS/idempotent whole-document replacement and immutable Operations content serving on the derived surface.
```

## Result

PASS. The local server can now derive one independent Operations V1 surface
from an exact admitted V0 revision through:

- `POST /api/canvas/operation-surfaces`;
- `GET /api/canvas/operation-surfaces/:surfaceId`;
- `session-bridge.mjs derive`.

The derivation service canonicalizes the four semantic request fields in fixed
order, hashes that JSON, and binds the idempotency key to one digest and one
projected outcome. Same-key/same-input retries return the original surface and
revision without rereading workspace bytes. Same-key/different-input fails with
`derivation_key_conflict`.

For a new key, the service resolves the named V0 surface/revision, including a
historical non-current revision, then reads through canonical workspace path
admission. Missing, deleted, drifted, oversized, or projection-unknown sources
return `source_revision_unavailable` before blob or event creation. Exact bytes
are stored content-addressed before the V4 derivation event is appended.

Derivation preserves V0 identity and selection: it does not republish, mutate,
redirect, or synchronize the source. A later V0 publication leaves the derived
surface metadata and blob unchanged, and restart reconstructs both from the V4
event plus verified blob.

## Recovery Matrix

The focused suite proves exact stored bytes, idempotent retry after workspace
drift, later V0 publication independence, restart, historical source admission,
deleted/drifted/unknown/oversized rejection, 5 MiB HTTP rejection, six-way
same-key concurrency, key conflict, append-failure orphan reporting,
event-success/projection-failure repair, metadata GET, unknown GET, and the real
one-shot CLI command.

## Validation Evidence

| Command | Result |
| --- | --- |
| `npm run test:operations-derive` | PASS: 6 tests. |
| `npm run test:canvas-publish` | PASS: 4 tests. |
| `npm run test:canvas-paths` | PASS: 5 tests. |
| `npm run test:canvas-replay` | PASS: 4 tests. |
| `npm run test:operations-replay` | PASS: 8 tests. |
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
- Next bounded unit: `SWU-OV1-006`
