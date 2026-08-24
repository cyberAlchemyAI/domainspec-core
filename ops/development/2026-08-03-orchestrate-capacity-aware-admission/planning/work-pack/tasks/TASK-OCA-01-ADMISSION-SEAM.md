---
taskId: TASK-OCA-01
swuId: SWU-OCA-001
status: selected-not-authorized
layer: L0
wave: W1
---

# Whole-wave admission seam

## Objective and boundary

Make one deterministic snapshot-only decision before action compilation:
either admit the complete requested wave or persist a block with zero action
documents and zero spawn attempts. This SWU does not discover live capacity,
verify/reserve slots, project route options, alter topology, or invoke a host
operation. Reservation-required inputs block as `unsupported`.

Primary behavior: frozen versioned capacity evidence controls whether the
exact approved wave reaches compilation.

Independent acceptance boundary: the fixture matrix proves sufficient evidence
emits exactly the full plan, while missing, malformed, stale, cross-scope,
advisory, unknown, insufficient, and unreserved evidence emits no action.

## Source anchors

- `arcanum/runtime/orchestrate/SKILL.md`
- `arcanum/runtime/orchestrate/scripts/native_dispatch_coordinator.py`
- `arcanum/runtime/orchestrate/tests/preflight/test_preflight_contract.py`
- `../../../define/interfaces.md`
- `../../../design/ARCHITECTURE.md`

## Exact future write scope

- add `arcanum/runtime/orchestrate/schemas/host-capacity-evidence.schema.json`
- add `arcanum/runtime/orchestrate/schemas/capacity-admission-receipt.schema.json`
- add `arcanum/runtime/orchestrate/scripts/evaluate_capacity_admission.py`
- add `arcanum/runtime/orchestrate/tests/capacity-admission/capacity-admission-fixtures.json`
- add `arcanum/runtime/orchestrate/tests/capacity-admission/test_capacity_admission.py`
- add `arcanum/runtime/orchestrate/tests/preflight/preflight-receipt-v0.2.schema.json`
- add `arcanum/runtime/orchestrate/tests/preflight/capacity-blocked.receipt.v0.2.json`
- add `arcanum/runtime/orchestrate/tests/preflight/capacity-ready.receipt.v0.2.json`
- edit `arcanum/runtime/orchestrate/tests/preflight/test_preflight_contract.py`
- edit `arcanum/runtime/orchestrate/scripts/native_dispatch_coordinator.py`
- edit `arcanum/runtime/orchestrate/SKILL.md`

No generated surface is edited in this SWU.

## Implementation detail

1. Add pure `derive_initial_wave_demand(dispatch, run_id, host_id)` logic that
   binds run/host identity and sums the selected dependency-free wave's
   validated role `agent_count` values before constructing action objects.
2. Add pure `evaluate_capacity_admission(policy_version, demand, evidence,
   evaluated_at)` logic. `evaluated_at` is an injected ISO-8601 value; the
   evaluator never reads a wall clock.
3. Parse and schema-check one immutable evidence record, then bind its digest,
   host, scope, run, wave, requested width, and freshness to the demand.
4. Evaluate `strict_whole_wave`; advisory/unknown records cannot admit and any
   reservation-required policy returns `blocked-unsupported` in this SWU.
5. Canonical evidence and decision digests use SHA-256 over UTF-8 JSON with
   recursively sorted object keys, compact separators `,` and `:`, preserved
   array order, and no ASCII coercion; the digest field itself is excluded from
   its digest.
6. The coordinator entrypoint is `compile_to_directory(..., host_id,
   capacity_contract_version, capacity_evidence_path, evaluated_at)`. The
   governed execute path always passes `strict_whole_wave_v0_2`; omission,
   partial inputs, or an unknown version blocks and never downgrades.
7. Legacy behavior is confined to a separately named
   `compile_to_directory_legacy_v0_1(...)` compatibility entrypoint referenced
   only by declared v0.1 fixtures. It is not a default or fallback for governed
   execution.
8. In strict mode, persist `capacity-admission.json` immediately after dispatch
   validation and demand derivation, before `run-plan.json` or any action.
9. Call the existing action compiler only when admitted; assert emitted action
   count equals requested width. On block, emit a typed decision and empty
   action set—no route-option handles, slicing, or serialization.

Edge cases: zero/negative widths reject; integer overflow or wrong types reject;
expired or future-invalid timestamps relative to injected evaluation time
reject; changed evidence digest creates a new decision rather than mutating the
old one; action replay rules remain unchanged.

## Done and evidence

- both schemas validate positive and negative fixtures;
- capacity-admission matrix passes deterministically;
- current v0.1 preflight fixtures remain green only through the named legacy
  compatibility entrypoint;
- v0.2 missing/partial evidence blocks before compilation;
- no block fixture creates an action path or calls spawn/wait/interrupt;
- diff contains only the exact write scope and generic public vocabulary.

Owner: Arcanum Orchestrate lifecycle owner. Handoff: Invoke Refresh using the
`SWU-OCA-001` row in `../../CLOSEOUT-SYNC-INVENTORY.json`; only then may
`SWU-OCA-002` be selected. Expected Task Session result is a terminal receipt,
fixture report, target digests, and residue list—not an automatic successor.
