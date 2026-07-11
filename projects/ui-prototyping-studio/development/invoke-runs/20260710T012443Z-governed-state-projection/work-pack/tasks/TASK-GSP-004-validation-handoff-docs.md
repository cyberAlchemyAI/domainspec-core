# TASK-GSP-004 - Validation Harness, Handoff Semantics, Docs Sync

## Objective

Repair evidence production and claim semantics so current proof can be refreshed
without overclaiming implementation readiness.

## Source Contracts

- `projects/ui-prototyping-studio/backend/e2e/helpers.ts`
- `projects/ui-prototyping-studio/backend/src/modules/ui-prototyping-studio/application/export-design-handoff.ts`
- `projects/ui-prototyping-studio/ARCHITECTURE.md`
- `projects/ui-prototyping-studio/SPEC.md`
- `projects/ui-prototyping-studio/CRAFT.md`
- `projects/ui-prototyping-studio/development/PLAN-NEXT.md`

## Smallest Working Units

### SWU-GSP-004

- Goal: make checked-in e2e helpers use a deterministic local `tsx` path or
  pinned package-manager route that does not fail on ambient Corepack.
- Dependencies: none.
- Write scope:
  - `backend/e2e/helpers.ts`
  - package scripts only if needed
- Done criteria:
  - standard checked-in e2e can start without `/tmp` pnpm shim.
- Validation command:
  - `cd projects/ui-prototyping-studio/backend && ./node_modules/.bin/playwright test --reporter=list`
- Execution owner: task-session.

### SWU-GSP-005

- Goal: separate handoff `exportConfirmed`, `evidenceComplete`,
  `integrationReady`, and `implementationReady` semantics.
- Dependencies: SWU-GSP-004 may run independently; semantic tests should use
  current source state.
- Write scope:
  - handoff export use case/schema/tests
  - docs only as needed
- Done criteria:
  - confirmed export with nonempty `missingRefs` cannot imply implementation-ready.
- Validation command:
  - `cd projects/ui-prototyping-studio/backend && ./node_modules/.bin/tsx --test "src/**/*.test.ts"`
- Execution owner: task-session.

### SWU-GSP-005-DOC

- Goal: reconcile docs/test-count/state drift after code receipts exist.
- Dependencies: SWU-GSP-001 and SWU-GSP-004.
- Write scope:
  - `ARCHITECTURE.md`
  - `SPEC.md`
  - `CRAFT.md`
  - `development/PLAN-NEXT.md`
  - test protocol docs if needed
- Done criteria:
  - docs do not claim read-only preview, stale counts, or stale persistence invariant.
- Validation surface:
  - grep-backed review plus command transcript.
- Execution owner: local-fallback.
