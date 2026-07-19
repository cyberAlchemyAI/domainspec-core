# W1 — Deterministic Offline Witness

- Layer: L0.
- Layer question: Does one semantic plan deterministically recompose into the
  required arms/rotations and correct score receipts without model inference?
- Entry gate: W0 contract pass.
- Tasks: [FIXTURES](../tasks/TASK-HALP-FIXTURES.md),
  [WITNESS](../tasks/TASK-HALP-WITNESS.md).
- SWUs: 007, 008, 010.

## Order

1. Generate semantic plans, splits, and provenance (007).
2. Render/score stored valid and invalid outputs (008).
3. Rebuild and verify one end-to-end content-addressed witness (010).

## Exit Evidence

- Byte-identical repeat generation.
- Early/middle/late and required arms from identical semantic plans.
- Tested output grammar and exact answer/evidence/support scoring.
- Fixture -> render -> stored output -> score receipt trace.

## Stop Conditions

Stop on nondeterminism, cross-split leakage, provenance ambiguity, prompt-arm
semantic drift, evidence-span mismatch, or scorer disagreement with fixtures.
