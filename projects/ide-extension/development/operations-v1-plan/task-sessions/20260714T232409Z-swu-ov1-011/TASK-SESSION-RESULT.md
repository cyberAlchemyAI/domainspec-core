# Task Session Result: SWU-OV1-011

```yaml
swu_id: SWU-OV1-011
result: pass
capability_ref: task-session
receipt_kind: local-fallback
receipt_artifact: development/operations-v1-plan/task-sessions/20260714T232409Z-swu-ov1-011/TASK-SESSION-RESULT.md
files_touched:
  - package.json
  - public/demo/l0.html
  - src/kernel/canvas-blobs.mjs
  - src/kernel/canvas-retention.mjs
  - src/kernel/operations.mjs
  - src/server.mjs
  - tests/e2e/operations-v1-retention.spec.mjs
  - tests/l0-workbench-ui.test.mjs
  - tests/operations-v1-retention.test.mjs
validation:
  - npm run test:operations-retention: pass
  - npm run test:workbench: pass
  - npm run test:operations-contracts: pass
  - npm run test:operations-blobs: pass
  - npm run test:operations-replay: pass
  - npm run test:operations-replace: pass
  - npm run test:operations-append: pass
  - npm run test:operations-rebuild: pass
  - npm run test:operations-navigation: pass
  - npm run test:persistence: pass
  - npm run test:schemas: pass
  - npm run test:runtime-schemas: pass
  - npm run test:e2e: pass
  - npm run test:e2e:operations-retention: pass after final UI fix
  - runtime syntax, schema-contract, and scoped whitespace checks: pass
blockers: []
residue:
  - Automatic orphan-first reclamation, temporary cleanup, startup and post-commit evaluation, hard-threshold trigger, grace timer, and retry scheduling remain deferred to SWU-OV1-012.
  - A committed tombstone whose physical deletion fails remains explicit orphan residue for SWU-OV1-012 recovery.
  - Production policy constants are fixed; only tests inject byte-scale thresholds and clocks.
  - The unrelated Session Content Workbench human usefulness gate remains open and does not block Operations V1.
  - Unrelated concurrent worktree changes remain preserved outside this SWU.
reroute: SWU-OV1-012
handoff_note: Reuse the proven retention coordinator for startup/post-commit evaluation, hard or expired-grace automatic reclaim, orphan-first cleanup, timers, and recovery without changing manual contracts or defaults.
```

## Result

PASS. The server now reports replay-verified storage diagnostics through
`GET /api/canvas/storage`: total, referenced, orphan, and largest-blob bytes;
fixed policy thresholds; durable retention state and deadline; eligible and
selected candidate counts; event cursor; and explicit blocked reason.

Crossing the 1 GiB production soft threshold opens exactly one durable
seven-day grace request. Preview is explicit and deterministic: it protects
current and displayed revisions, sorts historical revisions by commit time and
id, accounts for shared content-addressed bodies, and hashes the event cursor,
policy, active request, and selected revision ids into one candidate digest.
Tests inject smaller thresholds; production defaults remain fixed.

Manual commit recomputes the candidate under the server mutation queue and
rejects stale digests. Each `canvas.revision_pruned` tombstone is durably
appended before deletion is attempted. Shared bodies survive until no unpruned
revision references them. Append failure stops the batch while preserving prior
tombstones and all un-tombstoned bodies. Delete failure keeps the tombstone and
returns explicit recoverable residue instead of pretending the body remains
available.

Pruned content returns `410 revision_pruned`. Exact retries return their
original operation, revision, and surface metadata plus
`operation_result_pruned`; they never rerun. The workbench receives typed
storage notices, shows grace and byte diagnostics, previews server-selected
history, and requires explicit confirmation before manual prune.

## Browser Evidence

Real Chromium began below threshold, then observed the SSE transition from
Normal to Grace after replay-verified inspection. Desktop and mobile previewed
one candidate, displayed the explicit prune control, confirmed the action,
returned to Normal, and observed `410` for the historical body. Layout checks
proved no horizontal overflow or control overlap.

- `assets/desktop-retention-preview.png`
- `assets/mobile-retention-preview.png`

Both screenshots were inspected at original detail and are nonblank, readable,
correctly framed, and free of overlapping controls.

## Failure And Recovery Matrix

Focused tests cover below-soft no-op, one grace event, restart restoration,
deterministic preview, command retry/conflict, stale digest, current and
displayed protection, shared references, event-before-delete observation,
partial tombstone append failure, deletion failure after durable tombstone,
410 content, exact retry after prune, and successful convergence below soft.

## Validation Evidence

| Command | Result |
| --- | --- |
| `npm run test:operations-retention` | PASS: 6 tests. |
| `npm run test:workbench` | PASS: 6 tests. |
| Inherited Operations/replay/persistence/schema/workbench run | PASS: 72 tests. |
| `npm run test:e2e` | PASS: all 16 desktop/mobile journeys. |
| `npm run test:e2e:operations-retention` | PASS: desktop and mobile after final UI fix. |
| `npm run validate:schemas` | PASS: 21 runtime schemas, 6 manifests, 78 fixtures. |
| Runtime/test syntax and scoped whitespace checks | PASS. |

## Session Metadata

- Context pack: [CONTEXT-PACK.md](CONTEXT-PACK.md)
- Gate: [GATE.md](GATE.md)
- Strict context coverage: pass, 18/18 obligations
- Gate verdict: pass
- Runtime: local plus real Chromium
- Handoff: none
- Subagents: not applicable; started 0, completed 0, failed 0, blocked 0
- Experiment harness: not applicable
- L2 promotion recommendation: partial; W5 automatic recovery remains
- Next bounded unit: `SWU-OV1-012`
