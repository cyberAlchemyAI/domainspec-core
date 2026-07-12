# SWU-IDEAD-006 Evidence

```yaml
swu_id: SWU-IDEAD-006
result: pass
capability_ref: task-session
receipt_kind: local-fallback
receipt_artifact: projects/ide-extension/development/l0-human-approval-desk-plan/work-pack/evidence/SWU-IDEAD-006.md
files_touched:
  - src/kernel/audit.mjs
  - src/kernel/projector.mjs
  - src/kernel/storage.mjs
  - src/server.mjs
  - tests/l0-persistence-recovery.test.mjs
  - tests/l0-lifecycle.test.mjs
  - tests/l0-runtime-schema-enforcement.test.mjs
  - tests/l0-adversarial.test.mjs
  - package.json
validation:
  - npm run test:persistence
  - node --test --test-concurrency=1 tests/l0-lifecycle.test.mjs tests/l0-grants-disposition.test.mjs tests/l0-persistence-recovery.test.mjs tests/l0-runtime-schema-enforcement.test.mjs tests/l0-schema-validation.test.mjs tests/l0-smoke.test.mjs
  - npm run test:adversarial
  - npm run validate:schemas
  - npm audit --audit-level=high
  - git diff --check
blockers: []
residue:
  - AR-CAND-007 remains red and is owned by SWU-IDEAD-007.
reroute: SWU-IDEAD-007
handoff_note: Event version 1 is authoritative; reduceEvents rebuilds workbench.json; reconciliation reports projection repair and orphan artifacts.
```

## Event And Projection Contract

- `event_version: 1` events contain complete validated envelope, approval, and optional receipt records.
- Supported event types are `envelope.prepared`, `receipt.appended`, and `approval.rejected`.
- `reduceEvents(events, { validateEvent })` is the deterministic projection API.
- `projectionChecksum(projection)` provides a stable SHA-256 equality surface for tests and reconciliation reports.
- Duplicate event IDs, unknown versions/types, broken bindings, malformed JSON, blank lines, and truncated final lines fail with `invalid_event_history`.
- `workbench.json` is never promoted into authority; stale or malformed projection data is replaced from committed events.

## Commit And Recovery Behavior

1. Every mutation enters the per-server serialized queue and reconciles from events.
2. The candidate complete event is schema-validated and reduced before append.
3. Event append writes one JSONL line, flushes the file handle, and closes it.
4. Projection replacement writes and flushes a same-directory exclusive temporary file, then renames it atomically.
5. If projection replacement fails after append, the API returns `503 reconciliation_required`; the next read or startup rebuilds the projection.
6. If event append fails after artifacts exist, no receipt becomes authoritative; subsequent reads report those files as orphan residue without deleting them.

## Validation Results

| Command | Result |
| --- | --- |
| `npm run test:persistence` | pass in three invocations; each race/restart test performs three repetitions; 6/6 per invocation |
| focused non-adversarial suite | pass: 34/34 |
| `npm run test:adversarial` | flag: 7/8 pass; AR-CAND-006 passes; expected AR-CAND-007 remains red |
| `npm run validate:schemas` | pass: 7 schemas, 6 manifests, 21 fixtures |
| `npm audit --audit-level=high` | pass: 0 vulnerabilities after one transient registry retry |
| syntax checks and `git diff --check` | pass |

No subagents or external runtime adapters were used. No experiment harness applies to this product SWU. This evidence does not claim cryptographic chaining, signatures, or generic tamper evidence.
