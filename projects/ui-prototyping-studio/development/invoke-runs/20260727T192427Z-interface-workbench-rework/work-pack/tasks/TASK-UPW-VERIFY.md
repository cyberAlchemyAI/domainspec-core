# TASK-UPW-VERIFY — Closure Verification

Status: `not-started`

## Objective

Verify recomposition, current regression, receipt completeness, residue, and
claim ceilings after SWU-UPW-001–019 complete.

- Layer/wave: L2 / W5
- Dependencies: passing synchronized execution and refresh receipts for all 19
  mutation SWUs
- Exact closure contract:
  `CLOSEOUT-SYNC-INVENTORY.json#closure_report_contract`

## Smallest Working Unit Exemption

The task ID includes `VERIFY` and owns closure evidence only. It must not mutate
product source. Any source repair opens a new SWU through Invoke Plan; it is not
performed inside this task.

## Exact Report

- Path:
  `closure-reports/interface-workbench-closure.json`
- Schema:
  `ui-prototyping-studio.interface-workbench-closure.v1`
- Writable fields:
  `schema_version`, `generated_at`, `source_commit`, `commands`,
  `swu_receipts`, `refresh_receipts`, `acceptance_assertions`,
  `recomposition`, `regressions`, `residue`, `verdict`, `next_owner`.
- Required synchronization inventory: every literal path and receipt range in
  `CLOSEOUT-SYNC-INVENTORY.json#closure_report_contract.synchronization_inventory`.
- Forbidden effect: the report may not mutate Plan definitions, select an SWU,
  authorize human study, or grant release/deployment authority.

## Checks

Run from `projects/ui-prototyping-studio/backend`:

```bash
./node_modules/.bin/tsc -p tsconfig.json --noEmit
./node_modules/.bin/tsx --test "src/**/*.test.ts"
./node_modules/.bin/playwright test --reporter=list
```

Then verify:

1. `SWU-MANIFEST.json`, `SWU-SCOPE-INVENTORY.json`,
   `SWU-ACCEPTANCE-MATRIX.json`, and `CLOSEOUT-SYNC-INVENTORY.json` contain the
   same 19 unique SWU IDs.
2. Every assertion has exactly one primary owner and its exact receipt field is
   present/passing; shared witness rows are explicitly non-primary.
3. UPW-FIX-001–024 each maps to executed primary/shared evidence without
   counting planned contracts as runtime evidence.
4. All six selected Design views and seven selected architecture extensions
   recompose.
5. `location.reload()` is absent from polling and successful action paths.
6. current/staged/acknowledgment/Revert/Export gates remain exact.
7. source changes match each preflight scope binding; generated/browser residue
   is absent or enumerated.
8. human, cross-browser, certification, release, and deployment gaps remain
   explicit.

## Verdict And Successor

A passing report may recommend a separately owned human-study/readiness route.
It cannot select, authorize, or execute that route. Any failure records the
exact assertion, receipt, or source mismatch and routes to Invoke Plan or the
owning SWU rather than repairing source inside W5.
