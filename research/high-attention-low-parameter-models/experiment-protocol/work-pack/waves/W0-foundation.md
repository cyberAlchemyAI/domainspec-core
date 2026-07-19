# W0 — Decisions And Contract Foundation

- Layer: L0.
- Layer question: Is the intended claim and machine contract explicit enough to
  build without inventing methodology during implementation?
- Entry gate: user authorizes one-question decision work.
- Tasks: [DECISIONS](../tasks/TASK-HALP-DECISIONS.md),
  [CONTRACTS](../tasks/TASK-HALP-CONTRACTS.md).
- SWUs: 001–006.

## Order

1. SWU 001 claim/estimands.
2. SWU 002–005 decision families; each consumes 001 and may proceed only with
   its own owner approval.
3. SWU 006 schemas/validators after all decision-dependent fields freeze.

No parallel mutation is authorized before SWU 001. After 001, decision
interviews may be scheduled independently but their records must not overlap.

## Exit Evidence

- Five valid, approval-bearing decision records.
- Frozen draft protocol projection.
- Positive and negative contract fixtures.
- Deterministic validator receipt.

## Promotion

Promote to W1 only when all fields required by fixture/render/score contracts
are frozen. Platform/resource decisions may remain materially unfulfilled but
their admission rules must be explicit.
