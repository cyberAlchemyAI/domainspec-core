# TASK-AKV-QRY-MIGRATION — Bind new-receipt-only adoption

- Layer/slice/wave: L0 / S-MIGRATION / W0
- SWU: `SWU-AKV-QRY-003`
- State: planned, dependency-gated, not selected, runtime-admission blocked
- Task class: material-mutation
- Execution mode: routed-mutation
- Owner recommendation: Task Session local Codex after QRY-002 and package admission

## Objective and primary decision

Create one migration note that increments the candidate algorithm version for new receipts and forbids rewriting, backfilling, or silently reinterpreting historical receipts.

## Sources and selectors

- `SPEC.md#normative-invariants` rule 6
- Refine matrix `receipt_invariants.migration`
- candidate policy/schema from QRY-001/QRY-002
- Related context: `ARCHITECTURE.md#migration-and-rollout`

## Dependencies

`SWU-AKV-QRY-002` pass receipt and its transitive QRY-001 dependency, all bound to the same work-pack snapshot.

## Exact writes

- materialWrites:
  - `projects/animejs/development/candidates/agent-knowledge-vault/query-contract/MIGRATION.md`
- executionOutputs: none
- allowedWrites: exactly the material write above

## Implementation detail

State the old/new version boundary, new-receipt-only rule, historical byte immutability, consumer opt-in requirement, no bulk migration, rollback boundary, and invalidation trigger when policy/schema changes.

Required sentence: `Historical receipts are immutable.`

## Acceptance boundary

This unit passes independently when the exact review command finds the required sentence and the terminal receipt cites the migration note digest.

Split analysis: this is one reviewable compatibility decision. It does not implement schema, validator, replay, or consumer rollout.

## Closeout

- Terminal projection: `execution-evidence/SWU-AKV-QRY-003/TERMINAL-RECEIPT.json`
- Refresh receipt: `closeout/SWU-AKV-QRY-003/refresh-report.json`
- Synchronize: `WORK-PACK.md`, this task, `PLAN-TRANSPORT.json`, `HANDOFF-STATE.json`
- Baseline: latest matching readiness snapshot plus live rehash
- Allowed deltas: evidence_added, blocker_opened, blocker_resolved, status_changed, route_changed
- Unique successor: `SWU-AKV-QRY-004`, expose only

## Expected result shape

Same normalized terminal projection shape, with the migration artifact and exact review check.
