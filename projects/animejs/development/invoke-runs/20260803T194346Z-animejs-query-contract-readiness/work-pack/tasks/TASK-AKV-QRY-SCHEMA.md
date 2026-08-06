# TASK-AKV-QRY-SCHEMA — Define the QueryReceipt structure

- Layer/slice/wave: L0 / S-SCHEMA / W0
- SWU: `SWU-AKV-QRY-002`
- State: planned, dependency-gated, not selected, runtime-admission blocked
- Task class: material-mutation
- Execution mode: routed-mutation
- Owner recommendation: Task Session local Codex after QRY-001 and package admission

## Objective and primary behavior

Create one Draft 2020-12 JSON Schema that makes success and abstention mutually exclusive, restricts `abstention_code` to the policy vocabulary or null, and preserves subordinate gaps without admitting a second primary code.

## Sources and selectors

- `SPEC.md#normative-invariants`
- candidate policy from QRY-001
- Refine matrix `receipt_invariants`
- Related context: `ARCHITECTURE.md#view-3--low-level-components`

## Dependencies

`SWU-AKV-QRY-001` pass receipt bound to the same work-pack snapshot.

## Exact writes

- materialWrites:
  - `projects/animejs/development/candidates/agent-knowledge-vault/query-contract/schema/query-receipt.schema.json`
- executionOutputs: none
- allowedWrites: exactly the material write above

## Implementation detail

The schema must:

1. close unknown fields;
2. require algorithm version, selected IDs, abstention code, subordinate gaps, evidence IDs, and next-question IDs;
3. use `oneOf` for success versus abstention;
4. require non-empty unique selected IDs and null code on success;
5. require empty selected IDs and one declared non-null code on abstention;
6. make subordinate gaps an independent unique array rather than additional terminal codes.

Edge cases: empty success selection, non-null success code, non-empty abstention selection, undeclared code, two primary codes, and unknown properties must fail.

## Acceptance boundary

This unit passes independently when `Draft202012Validator.check_schema` accepts the file and the terminal receipt cites the exact schema digest.

Split analysis: the schema owns one structural XOR behavior. Policy, migration, semantic validation, and replay remain separate.

## Closeout

- Terminal projection: `execution-evidence/SWU-AKV-QRY-002/TERMINAL-RECEIPT.json`
- Refresh receipt: `closeout/SWU-AKV-QRY-002/refresh-report.json`
- Synchronize: `WORK-PACK.md`, this task, `PLAN-TRANSPORT.json`, `HANDOFF-STATE.json`
- Baseline: latest matching readiness snapshot plus live rehash
- Allowed deltas: evidence_added, blocker_opened, blocker_resolved, status_changed, route_changed
- Unique successor: `SWU-AKV-QRY-003`, expose only

## Expected result shape

Same normalized terminal projection shape as QRY-001, with exact schema artifact and validation command evidence.
