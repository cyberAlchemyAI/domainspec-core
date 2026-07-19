---
taskId: TASK-HALP-ANALYZE
docType: work-pack-task
status: blocked-by-measurement
layer: L2-L3
slice: S-003
---

# TASK-HALP-ANALYZE — Paired Analysis And Phase Gate

## Objective

Execute only the frozen inference plan, preserve feasibility/resource axes, and
return a bounded phase decision.

Related context: [shared execution context](../shared/context.md),
[cross-task gaps](../shared/cross-task-gaps.md), and
[traceability](../shared/traceability.md).

## Smallest Working Units

### SWU-HALP-013 — Paired Behavioral Analysis

- Primary behavior: calculate the approved paired estimands, uncertainty, and
  multiplicity results on one sealed eligibility population.
- Acceptance boundary: reproducible analysis result with claim-bounded verdict.
- Split analysis: individual estimands can be functions, but their inclusion,
  pairing, and multiplicity population must be reviewed together.
- Dependencies: SWU 012.
- Source anchors: `operations.md#analyzephase`, `mappings.md#scorestocontrasts`,
  inference decision record.
- Write scope: `src/analysis/`, `analysis/decision-pilot/`.

Algorithm:

1. Verify protocol/analysis/eligibility hashes.
2. Construct paired units and position rotations.
3. Compute scale-specific retention and direct checkpoint contrast.
4. Compute difference-in-retention only for the corresponding claim.
5. Compute middle loss, evidence-present/absent behavior, and false support.
6. Apply frozen uncertainty, multiplicity, and exclusion rules.
7. Emit confirmatory verdicts separately from diagnostics.
8. Recompute from receipts in a clean process and compare result hash.

Edge cases: zero denominators, incomplete pairs, ceiling effects, infeasible
cells, all-zero outcomes, changed analysis code after freeze.

- Done: all primary outcomes and uncertainty present; diagnostics labeled;
  clean recomputation matches.
- Evidence: analysis JSON, code/version hash, human projection.
- Validation: `node src/analysis/run.mjs --protocol configs/protocol.json --eligibility analysis/decision-pilot/eligibility.json --recompute`.
- Owner: subagent or local fallback with independent review.
- Handoff note: no threshold changes after inspecting results.

### SWU-HALP-014 — Resource Frontier And Phase Decision

- Primary behavior: compute named-axis non-dominance and record one authorized
  continue/narrow/pivot/stop/repair decision.
- Acceptance boundary: frontier plus signed decision record.
- Split analysis: frontier and gate were considered separately; neither is a
  lifecycle result alone because the decision must cite the measured frontier.
- Dependencies: SWU 013 and complete resource receipts.
- Source anchors: `domain.md#resourcefrontier`, `queries.md#getresourcefrontier`,
  `operations.md#evaluatephasegate`, L2/L3 layering boundary.
- Write scope: `src/frontier/`, `analysis/frontier/`, `reports/phase-gate/`.

Algorithm:

1. Validate every requested axis and its measurement boundary.
2. Join capability and resource receipts by trial/run identifiers.
3. Preserve infeasible/missing cells and uncertainty.
4. Compute weak dominance without scalarization.
5. Evaluate whether any queued extension can change a declared decision.
6. Present frontier, deployment constraint, options, and stop rules.
7. Capture authorized phase decision and residue.

Edge cases: incomparable measurement boundaries, missing energy samples,
cost-price date drift, dominance ties, normalization rank reversal.

- Done: reproducible frontier and approved phase decision.
- Validation: `node src/frontier/test-frontier.mjs fixtures/frontier && node src/frontier/build.mjs analysis/decision-pilot` plus human gate review.
- Owner: analysis builder plus manual phase owner.
- Handoff note: do not select an extension merely because it is interesting.

## Synchronization

Update layering promotion evidence and work-pack status from the signed phase
decision. Inventory backfill is a separate explicit owner route.
