# TASK-AKV-QRY-VALIDATOR — Implement semantic validation

- Layer/slice/wave: L1 / S-VALIDATOR / W1
- SWU: `SWU-AKV-QRY-004`
- State: planned, dependency-gated, not selected, runtime-admission blocked
- Task class: material-mutation
- Execution mode: routed-mutation
- Owner recommendation: Task Session local Codex after QRY-003 and package admission

## Objective and primary behavior

Implement one side-effect-free Node module/CLI that validates QueryReceipt semantic invariants against the exact policy/schema versions and exits nonzero on invalid input.

## Sources and selectors

- candidate policy, schema, and migration note from QRY-001 through QRY-003
- `VALIDATION-CONTRACTS.md#validator-contract`
- Related context: `ARCHITECTURE.md#view-3--low-level-components`

## Dependencies

`SWU-AKV-QRY-003` pass receipt plus its transitive dependencies, bound to the same work-pack snapshot.

## Exact writes

- materialWrites:
  - `projects/animejs/development/candidates/agent-knowledge-vault/query-contract/validate-query-receipt.mjs`
- executionOutputs: none
- allowedWrites: exactly the material write above

## Algorithm

1. Load policy and schema versions from fixed sibling paths.
2. Reject version mismatch, missing required fields, undeclared codes, or unknown terminal path IDs.
3. Compute applicable failure predicates supplied by an input receipt/fixture.
4. Select the first applicable code from `primary_precedence`.
5. Enforce success/abstention XOR and preserve remaining failures as subordinate gaps.
6. Enforce tie normalization to `ABSTAIN_AMBIGUOUS_INTENT`.
7. Return typed findings without writing files; CLI exits 0 only for valid input.
8. `--self-test` runs small embedded positive/negative structural cases without replacing QRY-005 fixtures.

Failure modes include invalid JSON, policy/schema mismatch, duplicate selected IDs, invalid nullability, undeclared code, precedence mismatch, and historical-rewrite instruction.

## Acceptance boundary

This unit passes independently when `node validate-query-receipt.mjs --self-test` exits 0 and the terminal receipt cites the module digest.

Split analysis: fixture corpus and replay/report emission are independently acceptable and remain QRY-005.

## Closeout

- Terminal projection: `execution-evidence/SWU-AKV-QRY-004/TERMINAL-RECEIPT.json`
- Refresh receipt: `closeout/SWU-AKV-QRY-004/refresh-report.json`
- Synchronize: `WORK-PACK.md`, this task, `PLAN-TRANSPORT.json`, `HANDOFF-STATE.json`
- Baseline: latest matching readiness snapshot plus live rehash
- Allowed deltas: evidence_added, blocker_opened, blocker_resolved, status_changed, route_changed
- Unique successor: `SWU-AKV-QRY-005`, expose only

## Expected result shape

Same normalized terminal projection shape, with module artifact and self-test evidence.
