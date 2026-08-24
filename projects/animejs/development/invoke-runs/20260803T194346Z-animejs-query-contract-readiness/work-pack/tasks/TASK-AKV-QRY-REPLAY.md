# TASK-AKV-QRY-REPLAY — Replay the eight terminal paths

- Layer/slice/wave: L1 / S-REPLAY / W1
- SWU: `SWU-AKV-QRY-005`
- State: planned, dependency-gated, not selected, runtime-admission blocked
- Task class: material-mutation
- Execution mode: routed-mutation
- Owner recommendation: Task Session local Codex after QRY-004 and package admission

## Objective and primary behavior

Create the exact eight-case fixture corpus and one runner that executes every case once, rejects missing/extra/duplicate cases, and writes one deterministic validation report.

## Sources and selectors

- Refine matrix `planned_fixtures`
- `VALIDATION-CONTRACTS.md#design-witness-contracts`
- candidate policy/schema/validator from QRY-001 through QRY-004
- Related context: `ARCHITECTURE.md#quality`

## Dependencies

`SWU-AKV-QRY-004` pass receipt plus all transitive QRY-001–003 receipts, bound to the same work-pack snapshot.

## Exact writes

- materialWrites:
  - `projects/animejs/development/candidates/agent-knowledge-vault/query-contract/qry003-terminal-cases.json`
  - `projects/animejs/development/candidates/agent-knowledge-vault/query-contract/run-terminal-fixtures.mjs`
- executionOutputs:
  - `projects/animejs/development/invoke-runs/20260803T194346Z-animejs-query-contract-readiness/execution-evidence/SWU-AKV-QRY-005/query-contract-validation.json`
- allowedWrites: exact union of the two material writes and one execution output

## Algorithm

1. Load the exact policy, schema, validator, and fixture corpus.
2. Require exactly the eight Refine fixture IDs once each.
3. Run each input through the validator.
4. Compare selected IDs, primary code, subordinate gaps, conflicts, evidence IDs, and next questions to expected fields.
5. Fail the process if any case is missing, extra, duplicate, or mismatched.
6. Write one sorted JSON report containing source digests, runtime identity, per-case result, total count, and overall verdict.

Edge cases: stale policy/schema digest, undeclared fixture ID, duplicate ID, missing next question, wrong tie code, reordered precedence, or output path collision all block.

## Acceptance boundary

This unit passes independently when the exact bounded-write command exits 0, the report contains eight passing cases and zero failures, and Task Session reconciles the one output path.

Split analysis: fixtures and runner are coupled parts of one replay behavior—neither produces the acceptance result alone. The semantic validator is separately accepted in QRY-004.

## Closeout

- Terminal projection: `execution-evidence/SWU-AKV-QRY-005/TERMINAL-RECEIPT.json`
- Refresh receipt: `closeout/SWU-AKV-QRY-005/refresh-report.json`
- Synchronize: `WORK-PACK.md`, this task, `PLAN-TRANSPORT.json`, `HANDOFF-STATE.json`
- Baseline: latest matching readiness snapshot plus live rehash
- Allowed deltas: evidence_added, blocker_opened, blocker_resolved, status_changed, route_changed
- Unique successor: none; expose `invoke:plan` for relation repair and stop

## Expected result shape

Same normalized terminal projection shape, plus the exact eight-case report and no automatic successor execution.
