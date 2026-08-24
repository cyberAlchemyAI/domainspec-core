# TASK-INTEGRATION

## SWU-OAP-006 — Execute the 19 frozen-input fixtures

- Primary behavior: turn every proposed research fixture into an executed
  private receipt.
- Dependencies: OAP-002 and OAP-005.
- Write scope:
  - `ops/development/2026-07-30-one-shot-admission-prototype/fixtures/**`
  - `ops/development/2026-07-30-one-shot-admission-prototype/scripts/**`
  - `ops/development/2026-07-30-one-shot-admission-prototype/runs/**`
- Body War inputs: read-only exact refs from accepted research.
- Algorithm:
  1. Verify all frozen path/selector/digest bindings.
  2. Materialize each single-fault config in a temporary run directory.
  3. Invoke public WPRA/chain functions without writing Body War product files.
  4. Assert terminal code, receipt count, allowed writes, and forbidden
     transitions.
  5. Persist one private result per fixture and an aggregate receipt.
- Done criteria: 19/19 pass; PBW-01 completes; NBW-01..10 select no session;
  runtime negatives stop without overwrite/adoption.
- Validation: private fixture runner plus JSON parse.
- Execution owner: local fallback under candidate fast lane.
