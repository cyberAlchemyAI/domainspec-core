# W2 — Failed-spawn causal evidence

- Unit: `SWU-OCA-002`
- Task: [TASK-OCA-02](../tasks/TASK-OCA-02-FAILURE-EVIDENCE.md)
- Dependency: OCA-001 terminal pass and refresh
- Concurrency: none

Add the no-agent failure receipt/event/validator branch together. The gate must
have complete causal evidence yet remain blocked. Re-run native spawn,
partial-wave, evidence-order, and receipt-admission matrices.

L0 closes only when both W1 and W2 have terminal pass receipts. A cleanup result
or logical close is not physical capacity evidence.
