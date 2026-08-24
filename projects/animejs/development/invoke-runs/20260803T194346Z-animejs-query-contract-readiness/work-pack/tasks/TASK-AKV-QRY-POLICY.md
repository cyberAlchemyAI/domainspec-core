# TASK-AKV-QRY-POLICY — Close the terminal policy

- Layer/slice/wave: L0 / S-POLICY / W0
- SWU: `SWU-AKV-QRY-001`
- State: planned, dependency-ready, not selected, runtime-admission blocked
- Task class: material-mutation
- Execution mode: routed-mutation
- Owner recommendation: Task Session local Codex after package admission

## Objective and primary behavior

Create one immutable policy JSON that declares the six-code vocabulary, byte-ordered precedence, candidate algorithm version, eight terminal path IDs, and success/abstention invariants.

## Sources and selectors

- `SPEC.md#normative-invariants`
- Refine `08-query-contract-matrix.json`: `closed_abstention_vocabulary`, `primary_precedence`, `receipt_invariants`, `terminal_paths`
- Related context: `ARCHITECTURE.md#view-5--decision-flow`

## Dependencies

None.

## Exact writes

- materialWrites:
  - `projects/animejs/development/candidates/agent-knowledge-vault/query-contract/policy/qry003-terminal-contract.json`
- executionOutputs: none
- allowedWrites: exactly the material write above

## Implementation detail

Input is the exact Refine matrix. Output is a JSON object with:

1. schema and algorithm version IDs;
2. `abstention_codes` in exact precedence order;
3. `primary_precedence` byte-identical to that array;
4. eight stable terminal-path records and their expected result class;
5. explicit success, abstention, subordinate-gap, and tie-normalization invariants.

Reject any additional code, missing path, duplicate path, reordered precedence, or `ABSTAIN_AMBIGUOUS_CHOICE`.

## Acceptance boundary

This unit passes independently when the policy file parses and the exact jq assertion in `COMMAND-MATRIX.json` exits 0.

Split analysis: schema, migration, validator, and replay are independent child behaviors and are separate SWUs. Splitting the policy record itself would remove the single total-order contract that QRY-003 consumes.

## Closeout

- Terminal projection: `execution-evidence/SWU-AKV-QRY-001/TERMINAL-RECEIPT.json`
- Refresh receipt: `closeout/SWU-AKV-QRY-001/refresh-report.json`
- Synchronize: `WORK-PACK.md`, this task, `PLAN-TRANSPORT.json`, `HANDOFF-STATE.json`
- Baseline: latest matching readiness snapshot plus live rehash
- Allowed deltas: evidence_added, blocker_opened, blocker_resolved, status_changed, route_changed
- Unique successor: `SWU-AKV-QRY-002`, expose only

## Expected result shape

`result: pass|flag|block|interrupted`; `receipt_kind: task-session-terminal-projection`; exact files touched; validation argv/exit; blockers; residue; reroute; handoff note.
