# TASK-AKVE-03: Atomic Episode Journal

- Layer/wave: L1 / W1.
- Dependency: SWU-AKVE-003.
- Lifecycle owner: `animejs-vault-candidate-owner`.

## SWU-AKVE-004: Compare-and-append, idempotency, and receipt recovery

- Primary behavior: make accepted event plus idempotency binding one observable
  atomic commit boundary.
- Inputs: canonical request digest, proposed event, expected tail/revision,
  idempotency scope, and injected storage/clock/ID ports.
- Outputs: accepted/replayed/conflict/temporary-failure receipt and recovery
  handle; canonical journal bytes.
- Algorithm:
  1. lock or invoke an atomic store transaction scoped to the episode;
  2. check the scoped idempotency map before reading the target tail;
  3. replay identical request digest or reject a mismatch;
  4. compare revision/tail digest, finalize event/prior/event digests;
  5. commit event, idempotency mapping, and recoverable receipt atomically;
  6. classify injected failure as before-commit or committed-receipt-unavailable;
  7. recover only through an owner/capability-scoped opaque handle.
- Edge cases: simultaneous stale writers, same key/different body, truncated
  tail, cross-principal recovery, crash immediately before/after commit.
- Split analysis: journal append, idempotency, and recovery could be modules,
  but none can separately prove the non-ambiguous commit contract.
- Exact write scope:
  - `projects/animejs/ontology/agent-knowledge-vault/operational/src/canonical-json.mjs`
  - `projects/animejs/ontology/agent-knowledge-vault/operational/src/journal.mjs`
  - `projects/animejs/ontology/agent-knowledge-vault/operational/fixtures/journal-cases.json`
  - `projects/animejs/ontology/agent-knowledge-vault/operational/tests/journal.test.mjs`
- Done: concurrency and crash fixtures prove one event maximum and unambiguous
  recovery; tests use temporary directories and leave no repository runtime data.
- Validation: `node --test projects/animejs/ontology/agent-knowledge-vault/operational/tests/journal.test.mjs`.
- Execution owner recommendation: `subagent`, with `local-fallback` allowed.
- Handoff: implement a local port/fixture store, not a production database.

### Closeout synchronization

- Target inventory: exactly the four write-scope paths.
- Baseline binding: all four absent at Plan time; bind transition/schema digests
  from SWU-003/002 receipts and fail on drift.
- Admitted deltas: create four files only; temporary journal data must be outside
  the repository and removed by tests.
- Owner validation: targeted command run twice plus repository inventory diff.
- Terminal receipt: `../../task-sessions/SWU-AKVE-004/terminal-receipt.json`.
- Owner receipt: `../../task-sessions/SWU-AKVE-004/owner-closeout.json`.
- Continuation receipt: `../../task-sessions/SWU-AKVE-004/continuation-router.json`.
- Successor policy: route only 005 after pass; otherwise stop.

