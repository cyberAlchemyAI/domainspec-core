# Context Pack — SWU-GSP-002

## Contract

- Task: `TASK-GSP-002`
- SWU: `SWU-GSP-002`
- Dependency: joined passing `SWU-GSP-001` receipts.
- Objective: every store query and mutation begins from current valid persisted
  bytes.
- Allowed writes:
  - `backend/src/modules/ui-prototyping-studio/infrastructure/file-studio-session-store.ts`
  - focused infrastructure tests
- Acceptance-critical validation: full unit/slice suite plus an actual child
  process freshness witness.
- Successor after joined closeout: `SWU-GSP-003` only.

## Current Defect

The adapter loads `documentState` once at construction. Every subsequent query
and mutation reads that snapshot, so a long-running preview does not observe
CLI writes, and its later save can overwrite an external transition.

## Implementation Decision

Each query reloads the current document. Each mutation acquires a short-lived
atomic sibling lock, reloads current bytes inside the lock, applies one store
operation, atomically renames the result, and releases the lock.

Options considered:

- reload only: smallest change, but two overlapping writers can still silently
  overwrite each other;
- reload plus optimistic fingerprint: detects many races but retains a
  check/rename gap;
- reload under an exclusive lock: prevents overlapping adapter writes and
  fails closed instead of silently overwriting.

Selected: exclusive per-operation lock. Classification: consequential to
infrastructure behavior but bounded, reversible, and directly required by the
task’s fail-closed concurrency rule.

## Witness

A focused test constructs the reader first, then uses real child CLI processes
to create a session, stage a candidate, Accept, and Revert. The original reader
must observe each transition without restart. It also proves sequential ID
allocation across two store instances and post-construction corruption
failure.

Strict coverage: pass.
