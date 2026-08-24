---
taskId: TASK-OCA-02
swuId: SWU-OCA-002
status: planned
layer: L0
wave: W2
---

# Pre-agent failure evidence

## Objective and boundary

Represent a host spawn that fails before returning an agent ID without
fabricating identity or leaving the gate structurally incomplete. The terminal
path is always blocking.

Primary behavior: `action_attempted -> host_spawn_failed ->
pre_agent_failure_receipt_admitted -> gate_block` is a valid causal sequence.

Independent acceptance boundary: the canonical schema/reducer accepts exactly
that sequence with `agent_id: null`; it rejects gate pass, duplicate closure,
fabricated IDs, and missing predecessor evidence.

## Source anchors and future write scope

Read and edit only:

- `arcanum/runtime/orchestrate/schemas/run-event.schema.json`
- `arcanum/runtime/orchestrate/schemas/receipt.schema.json`
- `arcanum/runtime/orchestrate/scripts/native_dispatch_coordinator.py`
- `arcanum/runtime/orchestrate/scripts/validate_run_evidence.py`
- `arcanum/runtime/orchestrate/SKILL.md`
- `arcanum/runtime/orchestrate/tests/native-spawn/native-spawn-event.schema.json`
- `arcanum/runtime/orchestrate/tests/native-spawn/native-spawn-receipt.schema.json`
- `arcanum/runtime/orchestrate/tests/native-spawn/test_native_spawn_contract.py`
- `arcanum/runtime/orchestrate/tests/partial-wave/partial-wave-result.schema.json`
- `arcanum/runtime/orchestrate/tests/partial-wave/fixtures/expected-unresolved-trace.json`
- `arcanum/runtime/orchestrate/tests/partial-wave/test_partial_wave_recovery.py`
- `arcanum/runtime/orchestrate/tests/evidence-order/fixture-matrix.json`
- `arcanum/runtime/orchestrate/tests/evidence-order/test_evidence_order.py`
- `arcanum/runtime/orchestrate/tests/receipt-admission/receipt-admission-matrix.json`
- `arcanum/runtime/orchestrate/tests/receipt-admission/test_receipt_admission_matrix.py`

## Implementation detail

Add a canonical failed-before-agent receipt variant and event. Bind it to the
persisted action and failed host result, require a safe failure class plus an
opaque private diagnostic reference, and forbid a non-null agent identity.
Update causal validation so the variant accounts for the attempted action but
can only reduce the wave to block. Keep successful sibling cleanup separate;
cleanup must not imply physical capacity release.

Negative cases include a receipt without `action_attempted`, a mismatched
action/result digest, a failure receipt followed by `gate_pass`, dependent work
after block, duplicate terminal receipts, and test-local undeclared event kinds.

## Done and evidence

- new and existing event/receipt fixtures schema-check;
- causal matrix covers success, timeout, interrupt, and no-agent failure;
- partial-wave recovery passes without synthetic agent IDs;
- failure diagnostics remain private/opaque in public evidence;
- exact target diff and regression commands pass.

Dependency: terminal pass receipt for `SWU-OCA-001`. Owner: Orchestrate evidence
owner. Closeout: `SWU-OCA-002` inventory row; successor selection remains a
separate lifecycle decision.
