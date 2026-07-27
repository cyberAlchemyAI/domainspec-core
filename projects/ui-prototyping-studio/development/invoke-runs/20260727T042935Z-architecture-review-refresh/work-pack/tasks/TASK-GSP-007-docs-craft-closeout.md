# TASK-GSP-007 — Receipt-Driven Documentation And Craft Closeout

## Primary Behavior

Active documentation and scoped Craft state describe current reproducibility,
completed SWUs, remaining gaps, and next authority without stale counts or
proposal-as-build language.

## Dependencies

`SWU-GSP-006`.

## Write Scope

- `README.md`
- `ARCHITECTURE.md`
- `SPEC.md`
- root `WORK-PACK.md`
- `development/PLAN-NEXT.md`
- test protocol/readme files whose current commands or counts are stale

The work-pack, `.craft/ledger.yml`, `CRAFT.md`, and owner receipts remain
Invoke Refresh closeout targets; Task Session does not mutate them directly.

## Rules

1. Separate dated historical receipts from current reproducibility.
2. Mark the June deep spec and July package as historical proposals.
3. Record exact current test commands and counts from final receipts.
4. Close only findings proven by current code and browser evidence.
5. Preserve human-study and release-authorization residue.
6. Keep the ledger source authoritative and the Markdown view derived.

## Acceptance

The full suite passes; grep-backed review finds no stale test count,
read-only-preview claim, historical plan presented as current execution
authority, or export-equals-readiness claim. Craft indexes resolve every new
row and name no further implementation SWU.

## Validation

```sh
cd projects/ui-prototyping-studio/backend
./node_modules/.bin/tsc -p tsconfig.json --noEmit
./node_modules/.bin/tsx --test "src/**/*.test.ts"
./node_modules/.bin/playwright test --reporter=list
```

## Closeout

This task binds `SWU-GSP-007` to the Common Task Session Closeout Contract in
the parent work-pack. It has no successor. The joined closeout owner receipt
must mark the captured implementation frontier complete while preserving
human-study and release-authorization residue.
