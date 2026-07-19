---
taskId: TASK-HALP-MEASURE
docType: work-pack-task
status: blocked-by-admission
layer: L1-L2
slices: [S-002, S-003]
---

# TASK-HALP-MEASURE — Runtime Smoke And Decision Pilot

## Objective

Translate admitted cells into repeatable Experiment Harness runs, first as a
non-confirmatory measurement smoke and only then as the paired decision pilot.

Related context: [shared execution context](../shared/context.md),
[cross-task gaps](../shared/cross-task-gaps.md), and
[traceability](../shared/traceability.md).

## Smallest Working Units

### SWU-HALP-011 — One-Stack Measurement Smoke

- Primary behavior: execute a tiny repeated cell set and prove run/resource
  receipt completeness and systems repeatability.
- Acceptance boundary: one L1 smoke report; no behavioral claim.
- Split analysis: prefill/decode/energy repeats are fields of one measurement
  boundary and cannot independently establish run comparability.
- Dependencies: SWU 009, 010 and resource authorization.
- Source anchors: `operations.md#executetrialcell`, L1 layering row,
  W2 stop conditions.
- Write scope: `src/run-adapter/`, `trials/smoke/`, `runs/smoke/`,
  `reports/l1/` under the approved evidence policy.

Algorithm:

1. Build the smallest approved smoke matrix for one admitted stack.
2. Warm/cache exactly as frozen.
3. Execute repetitions serially on controlled hardware.
4. Emit a run receipt for every attempt, including failure.
5. Validate prefill/decode/memory/energy fields and repeat tolerance.
6. Mark the smoke non-confirmatory and decide pass/repair/stop.

Edge cases: hardware contention, thermal/power-policy drift, stale cache,
runtime retry, missing GPU-energy sample, output parse failure.

- Done: complete receipts, measurement repeatability, at least one feasible long
  cell, and no prohibited fallback.
- Validation: `node src/validate/validate-smoke.mjs runs/smoke --policy configs/protocol.json`.
- Owner: local fallback/Experiment Harness.
- Handoff note: do not infer retention or compare checkpoints from smoke data.

### SWU-HALP-012 — Paired Decision-Pilot Execution

- Primary behavior: execute the frozen required 1B/3B cell pairs and close an
  eligibility/exclusion ledger.
- Acceptance boundary: complete confirmatory receipt set for the approved matrix.
- Split analysis: matrix shards may run independently operationally, but none
  passes the decision-pilot acceptance boundary alone; shards are child run
  batches with parent join validation, not SWUs.
- Dependencies: SWU 002–005, 011 and explicit phase authorization.
- Source anchors: frozen protocol/matrix, W3, `queries.md#gettrialmatrix`.
- Write scope: `trials/decision-pilot/`, `runs/decision-pilot/`,
  `scores/decision-pilot/` under approved evidence policy.

Algorithm:

1. Project exact matrix and expected pair keys.
2. Freeze shard assignment with disjoint output paths.
3. Execute one cell/attempt per Experiment Harness unit.
4. Score each raw output with frozen scorer.
5. Join attempts; preserve typed failures and retries.
6. Validate required pairs and route every missing/ineligible cell through the
   frozen exclusion/repeat policy.
7. Seal receipt/eligibility index.

Edge cases: partial shard, duplicated cell, mixed runtime manifest, invalid
retry replacement, missing pair, resource-boundary drift.

- Done: all expected cells are completed, failed, or explicitly dispositioned;
  eligible pair set is sealed.
- Validation: `node src/validate/validate-pilot-receipts.mjs trials/decision-pilot runs/decision-pilot scores/decision-pilot`.
- Owner: subagent shards under parent Experiment Harness join, or local fallback.
- Handoff note: parent must join and close every shard receipt; no hidden open
  subagent or partial success claim.

## Synchronization

Run artifacts update the work-pack only through receipts and status projection;
they do not rewrite protocol or analysis decisions.
