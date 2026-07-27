# TASK-GSP-002 — Persisted Session Freshness

## Primary Behavior

Every store read reflects the latest valid persisted document, including writes
made by another process after the reader was created.

## Dependencies

`SWU-GSP-001`.

## Write Scope

- `backend/src/modules/ui-prototyping-studio/infrastructure/file-studio-session-store.ts`
- store or slice tests
- independent-process probe under checked-in tests when practical

## Rules

1. Read or version-check the current file before every query.
2. Preserve fail-closed behavior for corrupt JSON.
3. Preserve append-only revision and deterministic ID semantics.
4. Do not silently overwrite concurrent external state with a stale in-memory
   snapshot.

## Edge Cases

- file absent at first read;
- file created by another process;
- valid external Accept/Revert/stage write;
- corrupt external bytes;
- two sequential writers.

## Acceptance

An already-running preview/store observes an external state transition without
restart. Corrupt state still throws instead of resetting.

## Validation

```sh
cd projects/ui-prototyping-studio/backend
./node_modules/.bin/tsx --test "src/**/*.test.ts"
```

Also run the work-pack independent-process freshness witness.

## Closeout

This task binds `SWU-GSP-002` to the Common Task Session Closeout Contract in
the parent work-pack. Its only admissible successor is `SWU-GSP-003`.
