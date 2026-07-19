---
taskId: TASK-HALP-WITNESS
docType: work-pack-task
status: blocked-by-fixtures
layer: L0
slice: S-001
---

# TASK-HALP-WITNESS — Offline End-To-End Witness

## Objective

Prove the complete semantic artifact chain before spending model/GPU budget.

Related context: [shared execution context](../shared/context.md),
[cross-task gaps](../shared/cross-task-gaps.md), and
[traceability](../shared/traceability.md).

## Smallest Working Units

### SWU-HALP-010

- Primary behavior: rebuild one example from each primary fixture family through
  required arms/rotations and stored valid/invalid outputs into score receipts.
- Acceptance boundary: one content-addressed offline witness report.
- Split analysis: component checks already belong to SWU 007/008; this SWU owns
  only recomposition and cannot be split without duplicating them.
- Dependencies: SWU 007, 008.
- Source anchors: architecture workflow; mappings; L0 layering row.
- Write scope: `fixtures/offline-witness/`, `reports/l0/`.

Procedure:

1. Start from empty generated output directory.
2. Build selected semantic fixtures twice from identical inputs.
3. Render every required arm/rotation.
4. Score stored correct, incorrect, unsupported, abstaining, and malformed
   outputs.
5. Verify every receipt links through content hashes to protocol/fixture/render.
6. Compare clean rebuild outputs and emit one report.

Failure modes: nondeterminism, missing arm/rotation, truth drift, untraceable
score, parser ambiguity, hidden timestamp/random source.

- Done: all chains validate and rebuild byte-identically under explicit time
  input policy.
- Evidence: `reports/l0/offline-witness.md` plus machine receipt index.
- Validation: `node src/validate/run-offline-witness.mjs --clean --repeat 2`.
- Execution owner: local fallback.
- Handoff note: no runtime/model invocation is permitted.

## Synchronization

On pass, record L0 promotion evidence in layering/work-pack. On failure, route
to the owning component SWU; do not patch evidence in the witness task.
