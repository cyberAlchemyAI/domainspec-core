# Refresh Context Pack

Mode: `invoke:refresh`; activation: `direct-user`; resolved mutation mode:
`apply-approved`.

## Selected Source Evidence

- `readiness-runs/pre-refresh-r2/work-pack-readiness-report.json`
- `readiness-runs/pre-refresh-r2/REFRESH-SIGNAL-PACK.json`
- `IMPLEMENTATION-READINESS-DRY-RUN.md`
- current `WORK-PACK.md`
- current split task contracts and closeout contract
- live
  `arcanum/arcana/task-session/schemas/mutation-admission-request.schema.json`

The canonical audit returned `block`, with 26 numeric SWUs plus three closure
tasks, 24 units missing exact argv contracts, five incomplete attempt
lifecycles, three row-only closure tasks, fail-open terminal receipt semantics,
ambiguous source selectors, an absent closeout directory without a creation
contract, and zero currently runtime-admissible units.

## Exact Apply Scope

1. `WORK-PACK.md`
2. `TASK-SESSION-RECEIPT.schema.json`
3. `work-pack/shared/CONTEXT.md`
4. `work-pack/shared/CLOSEOUT-CONTRACT.md`
5. `work-pack/shared/COMMAND-MATRIX.json`
6. `work-pack/shared/validate-task-session-receipt.py`
7. `work-pack/shared/test-task-session-receipt.py`
8. `work-pack/tasks/TASK-CLOSURE.md`
9. `work-pack/tasks/TASK-FOUNDATION.md`
10. `work-pack/tasks/TASK-PACKAGE.md`

## Claim Ceiling

This refresh may make the plan contract complete. It cannot make any SWU
runtime-admissible without a current material package or a truthful Task
Session execution mode for output-only and audit-only work. It selects and
executes no SWU.
