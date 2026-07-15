# Task Session Result: SWU-OV1-008

```yaml
swu_id: SWU-OV1-008
result: pass
capability_ref: task-session
receipt_kind: local-fallback
receipt_artifact: development/operations-v1-plan/task-sessions/20260714T224033Z-swu-ov1-008/TASK-SESSION-RESULT.md
files_touched:
  - package.json
  - src/kernel/operations.mjs
  - src/server.mjs
  - tests/operations-v1-rebuild.test.mjs
  - tests/operations-v1-replace.test.mjs
validation:
  - npm run test:operations-rebuild: pass
  - npm run test:operations-append: pass
  - npm run test:operations-replace: pass
  - npm run test:operations-derive: pass
  - npm run test:operations-replay: pass
  - npm run test:operations-transform: pass
  - npm run test:canvas-paths: pass
  - npm run test:canvas-publish: pass
  - npm run test:canvas-replay: pass
  - npm run test:persistence: pass
  - Node syntax and scoped whitespace checks: pass
blockers: []
residue:
  - Durable redirect, transient refresh acknowledgement, and display selection remain deferred to SWU-OV1-009.
  - Browser frame delivery and acknowledgement remain deferred to SWU-OV1-010.
  - Rebuild is explicit and exact-hash bound; no workspace watch or implicit V0 synchronization is claimed.
  - Trusted-local HTML remains the V0 threat model; hostile HTML safety is not claimed.
  - Unrelated concurrent worktree changes remain preserved outside this SWU.
reroute: SWU-OV1-009
handoff_note: Add durable display selection and transient refresh status without changing V0 current publication semantics or redirecting on Operations commits.
```

## Result

PASS. The existing generic content-operation route and CLI now admit explicit
`rebuild` from a caller-selected workspace HTML path and expected SHA-256. The
service performs operation-id lookup and surface-revision CAS before rereading
the source, then uses the canonical workspace admission helper, verifies the
exact bytes, requires lossless UTF-8, applies the pinned complete-document
parse5 transform, and enforces the 4 MiB source and 8 MiB result limits.

The committed V4 operation preserves the Operations surface identity, advances
one ordered revision, and records workspace path/hash lineage. Result bytes are
stored before the event, remain immutable across restart, and do not alter V0
current publication. A later explicit V0 publish of the same workspace source
does not rebuild, replace, or redirect the Operations surface.

## Failure And Recovery Matrix

Focused tests reject source drift, missing files, directories, external links,
plus-one-byte sources, invalid UTF-8, stale revisions, and conflicting operation
IDs without appending events. An exact retry remains idempotent after the source
changes. Same-result rebuild creates a new revision while sharing the content
blob. Event-append failure exposes the orphan result blob, and projection-write
failure is repaired from the authoritative event.

Enabling rebuild correctly invalidated one old replacement-suite assertion that
the mode was unavailable. That assertion now verifies the supported mode's
missing-source response; all replacement CAS, limits, recovery, content, CLI,
and tombstone checks remain green.

## Validation Evidence

| Command | Result |
| --- | --- |
| `npm run test:operations-rebuild` | PASS: 7 tests. |
| `npm run test:operations-append` | PASS: 5 tests. |
| `npm run test:operations-replace` | PASS: 7 tests. |
| `npm run test:operations-derive` | PASS: 6 tests. |
| `npm run test:operations-replay` | PASS: 8 tests. |
| `npm run test:operations-transform` | PASS: 6 tests. |
| `npm run test:canvas-paths` | PASS: 5 tests. |
| `npm run test:canvas-publish` | PASS: 4 tests. |
| `npm run test:canvas-replay` | PASS: 4 tests. |
| `npm run test:persistence` | PASS: 6 tests. |
| Service/server/test syntax checks | PASS. |
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
- L2 promotion recommendation: partial; W4 continues through SWU-OV1-010
- Next bounded unit: `SWU-OV1-009`
