# TASK-WPRA-RUNTIME

## SWU-OAP-002 — Generate and audit the projection

- Primary behavior: produce one deterministic v2 projection or a stable
  pre-route blocker code.
- Dependencies: OAP-001.
- Write scope: WPRA runner, test, task matrix, and validation documents only.
- Inputs: v2 config, exact refs, material/receipt owners, validators, graph,
  closeout bindings, approval policy.
- Outputs: schema-valid projection, v2 report, stable blocker list.
- Algorithm:
  1. Capture all exact refs.
  2. Validate owners and binding classes.
  3. Build canonical semantic payload and digest.
  4. Build the authority-none projection and digest.
  5. Reject missing material, schema, inventory, baseline, delta, closeout,
     successor, or digest before chain selection.
  6. Recheck snapshot; emit only observability flags.
- Done criteria: legacy 10 tests pass; v2 positives and deterministic negatives
  pass; no configured command executes.
- Validation: WPRA fixture script and scoped whitespace check.
- Execution owner: local fallback under candidate fast lane.
