# TASK-GSP-006 — Handoff Evidence And Readiness Semantics

## Primary Behavior

Export confirmation, evidence completeness, integration readiness,
implementation readiness, and release authorization remain separate facts.

## Dependencies

`SWU-GSP-001`.

## Write Scope

- handoff domain models
- `application/export-design-handoff.ts`
- slice tests
- active product docs only when needed for the model contract

## Rules

1. `exportConfirmed` means only that the export action was explicitly
   confirmed.
2. `evidenceComplete = missingRefs.length === 0`.
3. Integration and implementation readiness require their own monotone
   predicates; export confirmation alone never sets them.
4. Release authorization is not represented as implied readiness.
5. Preserve `missingRefs` as explicit evidence.

## Acceptance

A confirmed export with any missing reference records
`exportConfirmed=true`, `evidenceComplete=false`, and false integration and
implementation readiness. A complete fixture proves the positive predicates
without asserting release.

## Validation

```sh
cd projects/ui-prototyping-studio/backend
./node_modules/.bin/tsx --test "src/**/*.test.ts"
```
