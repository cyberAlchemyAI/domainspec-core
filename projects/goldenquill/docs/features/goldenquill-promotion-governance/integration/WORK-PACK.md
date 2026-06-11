---
module: gq-victor-promotion-integration-L0
version: current
status: draft
updatedAt: 2026-06-10
docType: work-pack
---

# WORK-PACK: Victor ↔ Promotion-Governance Integration — L0 (fixture-only event spine)

## Purpose

Executable plan for **L0 only**: the fixture-only, audit-only event spine +
projection proof. This is the minimum working unit that proves the seam shape
before any production wiring. L1–L3 (live capture, owner-gated reuse, scale)
escalate to medium/high complexity and will get their own work-packs.

## Control Fields

| Field | Value | Notes |
| --- | --- | --- |
| workPackGateStatus | pass | full SWU contracts inline below |
| complexity | low | fixture-only, deterministic, single write-scope tree |
| outputMode | single-file | L0 slice is reviewable in one file |
| executionPackRef | n/a | low complexity; L1+ will need split + execution-pack |
| layeringArtifactRef | [layering.md](layering.md) | L0 layer |
| activeLayerWindow | L0 | |
| lastUpdatedAt | 2026-06-10 | |
| readinessProfile | pilot | fixture proof, not production |

## Objective Summary

- Objective: stand up `pipeline/grant_dag/` with a typed event envelope,
  idempotent `AcceptGrantWorkEvent`, a DAG projector, an audit-only
  `OntologyVaultProjection`, and a deterministic validator that passes the
  existing [TEST-SPEC.md](../TEST-SPEC.md) T1–T35 corpus.
- Primary inputs: [ARCHITECTURE.md](ARCHITECTURE.md) (six views, C2/C3/C4/C8),
  [runtime-design.md](runtime-design.md) §2/§5, [../domain.md](../domain.md),
  [../events.md](../events.md), [../mappings.md](../mappings.md),
  [../TEST-SPEC.md](../TEST-SPEC.md).
- Success condition: validator runs deterministically over all 35 fixtures;
  idempotent re-acceptance is a no-op; `mutation_allowed=false` everywhere; no
  fixture promotes Inventory/Ontology/card/sigil knowledge.

## Delivery Slices

| Slice ID | Outcome | Layer | Wave | Dependencies | Validation |
| --- | --- | --- | --- | --- | --- |
| S-001 | Event envelope schema + acceptance/idempotency | L0 | W0 | none | T1–T10 fixtures pass |
| S-002 | DAG projection + read model + receipts | L0 | W1 | S-001 | T11–T22 fixtures pass |
| S-003 | Audit-only OntologyVaultProjection | L0 | W1 | S-001 | T23–T30 fixtures pass |
| S-004 | Deterministic validator + full fixture corpus | L0 | W2 | S-001..S-003 | T1–T35 all pass; deterministic |

## Task Status Board

| Task ID | Goal | Layer | Complexity | Waves | Source | Gate Status | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TASK-EVT | Event envelope + AcceptGrantWorkEvent + receipts (C3, C2 fixture) | L0 | low | W0 | [ARCHITECTURE.md](ARCHITECTURE.md) C2/C3; [../domain.md](../domain.md); [../events.md](../events.md) | ready | not-started |
| TASK-DAG | GrantRunNode/Edge + ProjectEventToDag + read model (C4) | L0 | low | W1 | [../domain.md](../domain.md); [../states.md](../states.md) | ready | not-started |
| TASK-VAULT | OntologyVaultProjection audit-only (C8) | L0 | low | W1 | [../mappings.md](../mappings.md) §OntologyVaultProjection | ready | not-started |
| TASK-FIX | Deterministic validator + T1–T35 fixtures | L0 | low | W2 | [../TEST-SPEC.md](../TEST-SPEC.md) | ready | not-started |
| TASK-VERIFY | Completion verification: validator over all fixtures | L0 | low | W2 | this work-pack | ready-after-implementation | not-started |

## SWU Execution Handoff

| SWU ID | Parent Task | Source Anchors | Related Context | Dependencies | Write Scope | Done Criteria | Acceptance Evidence | Validation Surface | Execution Owner | Handoff Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SWU-GQDAG-001 | TASK-EVT | [../domain.md](../domain.md) §GrantWorkEventEnvelope | [ARCHITECTURE.md](ARCHITECTURE.md) View 6, R-001 | none | `pipeline/grant_dag/event_spine/envelope.py` | Pydantic frozen envelope (event_id, event_kind, producer_kind, run_id, org_scope, source_ref, occurred_at, captured_at, idempotency_key, interpretation_limits, gate_refs); adapter cannot set approved_allowed_uses | model rejects envelope with approved_allowed_uses; required-field omission raises | `python -m pytest pipeline/grant_dag/event_spine/` | subagent | ready |
| SWU-GQDAG-002 | TASK-EVT | [../events.md](../events.md) GrantWorkEventAccepted/Rejected; [../operations.md](../operations.md) AcceptGrantWorkEvent R5–R6 | seam-map.md §Seam 1 §2.2 | SWU-GQDAG-001 | `pipeline/grant_dag/event_spine/accept.py`, `.../journal.py` | JSONL append journal + in-memory idempotency index; same key+hash → skipped_reason=idempotent_replay; key+diff hash → blocked_reason=duplicate_conflict; missing source_ref on source-backed event → reject | T1–T10 fixtures: accept, reject-no-source, idempotent replay no-op, duplicate-conflict block | pytest event_spine | subagent | ready |
| SWU-GQDAG-003 | TASK-EVT | [../domain.md](../domain.md) §EventProjectionReceipt | — | SWU-GQDAG-002 | `pipeline/grant_dag/event_spine/receipt.py` | EventProjectionReceipt (created_refs, updated_refs, skipped_reason, blocked_reason, validation_state) emitted on every accept | every accept/reject path returns a receipt; receipt is deterministic | pytest event_spine | subagent | ready |
| SWU-GQDAG-004 | TASK-DAG | [../domain.md](../domain.md) §GrantRunNode/§GrantRunEdge (14 node + 7 edge kinds) | [ARCHITECTURE.md](ARCHITECTURE.md) View 3 | SWU-GQDAG-001 | `pipeline/grant_dag/execution/nodes.py`, `.../edges.py` | frozen Pydantic GrantRunNode/Edge with closed kind enums; traversal semantics per [../states.md](../states.md) GRT-I1..I3 | node/edge with unknown kind raises; delivery node requires operator_signoff predecessor | pytest execution | subagent | ready |
| SWU-GQDAG-005 | TASK-DAG | [../mappings.md](../mappings.md) GrantWorkEventToDagNode/Edge | seam-map.md §Seam 1 table | SWU-GQDAG-002, SWU-GQDAG-004 | `pipeline/grant_dag/execution/project.py` | ProjectEventToDag maps accepted events → nodes/edges + read-model projection; replayable | T11–T22: projection from event stream; blocked-gate stops downstream node without reopen | pytest execution | subagent | ready |
| SWU-GQDAG-006 | TASK-VAULT | [../mappings.md](../mappings.md) §OntologyVaultProjection (defaults, validation) | [ARCHITECTURE.md](ARCHITECTURE.md) R-005 | SWU-GQDAG-002 | `pipeline/grant_dag/ontology_vault/projection.py` | audit-only projection; mutation_allowed=false always; approved_allowed_uses only with approved owner decision; evidence_refs/review_gate/contradiction_path required | T23–T30: projection refuses mutation; candidate with approved_allowed_uses blocks | pytest ontology_vault | subagent | ready |
| SWU-GQDAG-007 | TASK-FIX | [../TEST-SPEC.md](../TEST-SPEC.md) T1–T35 | all above | SWU-GQDAG-002,005,006 | `pipeline/grant_dag/fixtures/`, `pipeline/grant_dag/validate/validator.py` | positive/negative fixtures for all 35 cases; deterministic fail-closed validator | `validator.py fixtures/` → all 35 pass; rerun byte-identical | `python pipeline/grant_dag/validate/validator.py pipeline/grant_dag/fixtures/` | subagent | ready |
| SWU-GQDAG-008 | TASK-VERIFY | this work-pack §Objective | — | SWU-GQDAG-007 | (read-only; report) | full corpus passes; idempotency + audit-only + no-promotion invariants hold | validator exit 0; promotion-guardrail check: grep fixtures for card/ontology mutation = none | validator run + manual review | manual | ready |

## Blockers

| Blocker ID | Scope | Description | Owner | Next Action | Target Date |
| --- | --- | --- | --- | --- | --- |
| B-001 | cross-task | TEST-SPEC T1–T35 must be confirmed authored/stable before TASK-FIX | grant-runtime | read [../TEST-SPEC.md](../TEST-SPEC.md); reconcile any drift | before W2 |
| B-002 | downstream (not L0) | OQ-4 / D-D vocabulary LOCK blocks L1 candidate shape, not L0 | joint vocabulary owner | LOCK before L1 work-pack | before L1 |

## Gate Checks

1. workPackGateStatus = pass — all 8 SWUs carry dependencies, source anchors, write scope, done criteria, acceptance evidence, validation surface, execution owner. ✓
2. Low complexity → executionPackRef = n/a permitted. ✓
3. Layer mappings consistent with [layering.md](layering.md) L0. ✓
4. No L0 blocker affects acceptance (B-002 is downstream). ✓
5. All SWUs complete. ✓
7. Each task's SWUs are independent files within `pipeline/grant_dag/`; pick one per worker. ✓
8. Parallel SWUs have disjoint write scopes (event_spine / execution / ontology_vault / fixtures+validate). ✓

## Change Log

| Date | Change | Author |
| --- | --- | --- |
| 2026-06-10 | Initial L0 work-pack created (invoke plan) | invoke |
