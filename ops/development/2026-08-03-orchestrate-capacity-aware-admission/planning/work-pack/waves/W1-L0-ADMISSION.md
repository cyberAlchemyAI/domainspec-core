# W1 — Whole-wave admission

- Unit: `SWU-OCA-001`
- Task: [TASK-OCA-01](../tasks/TASK-OCA-01-ADMISSION-SEAM.md)
- Dependency: W0 pass
- Concurrency: none

Execute schema, evaluator, preflight wiring, and the capacity fixture matrix as
one atomic behavior. Gate on the sufficient case and every zero-action block
case. Stop rather than entering W2 if a host operation occurs during preflight,
the compiler sees a blocked decision, or current preflight fixtures regress.

Terminal evidence: Task Session receipt, exact diff, test transcript, residue,
and Invoke Refresh receipt for OCA-001.
