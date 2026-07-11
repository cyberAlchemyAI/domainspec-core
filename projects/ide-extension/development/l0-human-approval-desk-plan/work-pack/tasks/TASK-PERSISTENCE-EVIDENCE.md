# TASK-PERSISTENCE-EVIDENCE

## Objective

Make the event history authoritative, the workbench projection rebuildable, and every committed receipt reference resolvable.

- Layer/slice: L0 / S-003
- Wave: W2
- Dependencies: TASK-TRUSTED-KERNEL
- Source contracts: review AR-CAND-006/007, DEC-IDEAD-005/006, SPEC required state files and receipt contract
- Blockers: none

## Commit Model

```text
validate command
-> enter serialized mutation boundary
-> reload/reconcile committed event state
-> compare-and-transition
-> create evidence artifacts exclusively
-> append one complete authoritative event
-> atomically replace workbench projection
-> respond
```

If projection replacement fails after event append, the event remains authoritative and restart/read reconciliation rebuilds the projection. Artifacts without a committed referencing event are non-authoritative orphans and must be reported.

## Smallest Working Units

### SWU-IDEAD-006: Serialized Event Projection And Recovery

- Goal: prevent concurrent divergence and define deterministic startup/read recovery.
- Dependencies: SWU-IDEAD-005.
- Write scope: `src/kernel/audit.mjs`, `src/server.mjs`, new reducer/projector/storage modules, race/restart tests.
- Source anchors: `readWorkbench()`, `writeWorkbench()`, prepare/disposition write ordering, `appendEvent()`, AR-CAND-006.
- Related context: DEC-IDEAD-005/006; final state shape from SWU-002.

#### Algorithm

1. Maintain a per-server promise queue or mutex for all state-changing commands.
2. Represent each accepted command as one complete versioned event sufficient for deterministic reduction.
3. On startup or before the first command, parse all events and reduce them into the canonical projection; reject malformed/truncated authoritative history with a clear startup error rather than guessing.
4. Write projection to a same-directory temporary file, flush/close as supported, then rename atomically.
5. After an event commits, projection failure returns a recoverable server error and marks reconciliation required; the next read/start rebuilds it.
6. Compare reduced event state to `workbench.json`; repair only the projection, never rewrite committed history silently.
7. Report artifacts not referenced by committed events as residue; do not silently delete them in L0.

- Edge cases: simultaneous prepare; simultaneous same approval; event append failure; projection rename failure; stale projection; truncated final event line; orphan artifact.
- Done criteria: repeated race and restart runs yield equal event-derived and file projections with one receipt per consumed approval.
- Acceptance evidence: deterministic test fixtures for interruption points and projection checksums/counts.
- Validation: race/recovery tests repeated three times.
- Execution owner: local-fallback.
- Handoff note: return event versions, reducer API, projection invariants, and recovery behavior.

### SWU-IDEAD-007: Materialized And Resolvable Receipt Evidence

- Goal: create real before/after/receipt artifacts and reject any receipt whose references do not resolve.
- Dependencies: SWU-IDEAD-006.
- Write scope: `src/kernel/artifacts.mjs`, receipt construction, receipt schema, server disposition command, artifact/reference tests.
- Source anchors: `writeArtifactRef()`, `approveDryRunEnvelope()`, receipt schema, AR-CAND-007.
- Related context: commit model above.

#### Ordered Rules

1. Generate artifact IDs from bound run/approval/disposition identifiers, not UI labels.
2. Use exclusive creation (`wx` or equivalent) so duplicate IDs fail before overwrite.
3. Materialize a before artifact from the pending records and an after artifact from the proposed terminal records.
4. Resolve and validate both artifacts and all evidence refs before constructing the committed receipt event.
5. Materialize the receipt artifact from the same validated receipt payload.
6. Bind receipt to run, envelope, approval, normalized grants, disposition, before ref, after ref, and evidence refs supported at L0.
7. Rejection may have a disposition artifact/event but must not mint a passed receipt.

- Edge cases: duplicate artifact ID; missing file; path escape; malformed artifact JSON; mismatched run/approval; receipt schema failure; orphan artifact after append failure.
- Done criteria: every committed receipt ref resolves within the project state artifact root and matches its bound identifiers.
- Acceptance evidence: tests enumerate every receipt ref and load/validate the target artifact.
- Validation: artifact/reference tests, adversarial suite, restart suite.
- Execution owner: local-fallback.
- Handoff note: provide the stable evidence API fields and UI-safe artifact projection.

## Synchronization

Preserve the review's boundary correction: this task does not add cryptographic chaining, signatures, or generic tamper-evidence claims.
