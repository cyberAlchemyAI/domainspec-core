# TASK-WCP-04: Non-vacuous negative controls

## SWU-WCP-006

- Layer/slice/wave: L0, S-WCP-03, W2.
- Dependency: SWU-WCP-005 pass.
- Primary behavior: execute the frozen negative-control matrix with stable
  zero-output oracles.
- Controls: invalid relation; wrong workspace with pre-proven beta sentinel;
  stale digest; batch preflight rejection; derived-view edit; iterator timing;
  process termination barriers; logical corruption; named physical corruption;
  synchronized concurrent A/B observation; YAML mutation guard.
- Inputs: verified normal store and disposable copies.
- Outputs: one receipt per control plus matrix reducer.
- Edge/failure cases: a control that never demonstrates its trigger is vacuous;
  power loss, true mid-apply rollback, multiwriter support, and in-place repair
  must not be inferred.
- Write scope: exact negative run/copy/session directories only.
- Forbidden: live store damage, real ledger mutation, broad process kill, power
  manipulation, prefix/workspace deletion claims.
- Done: every trigger is proven, expected stable code appears, row count is
  zero where required, and YAML bytes remain exact.
- Validation: control-matrix schema, trigger preconditions, event ordering,
  output count, expected codes, pre/post YAML hashes, target realpaths.
- Execution owner: Task Session local.

## Split analysis

Controls share one immutable harness and one claim ceiling. Individual controls
have no adoption value and recomposition requires the whole declared matrix, so
they remain one SWU. A future destructive/power harness is a different route.
