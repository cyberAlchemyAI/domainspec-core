# Branch-evidence-mapper receipt (ledger: branch-evidence-mapper-receipt)

One approved subagent (branch-evidence-mapper), join parent_synthesis. Completed and closed.

## Canonical branch set [SB]

Reconciles ontology-vault (business / system / bridge) with the GoldenQuill ontology DAG on master
(meaning / system / operational / bridge). Result = **4 branches**:

- **B1 meaning** (a.k.a. business/domain/intent) — domain semantics, policy, rules, value claims,
  outcomes, premises. [SB ontology_dag synthesis "meaning" row; ontology-vault branch-aware schema]
- **B2 system** — implementation artifacts, runtime behavior, technical constraints, tests,
  observability, data shapes. [SB synthesis "system" row; ontology-vault README]
- **B3 operational** — one bounded run context (org, run_id, deadline, posture); lifecycle states +
  depth. First-class, not optional. [SB ontology_dag findings "operational as first-class branch"]
- **B4 bridge** — cross-branch evidence/alignment/realization/validation/constraint/contradiction/drift.
  [SB ontology-vault README bridge edges]

## Bridge edge types (7) [SB]

`realized_by` · `depends_on` · `constrained_by` · `observed_by` · `tested_by` · `drifts_from` ·
`traced_to` (+ GoldenQuill DAG edges `blocked_by_gate`/`approved_by`).

## Branch → product layer [SB]

- B1 meaning → L-ont (primary, cards) + L-reg (authority class) + L-dag (claim/rule/criterion nodes) + L-bi (business outcomes/KPIs).
- B2 system → L-dag (execution-path nodes) + L-reg (field→authority) + L-bi (system metrics, routing, gates).
- B3 operational → **L-dag (lifecycle_state, outcome_event)** + L-reg (org scope) + L-bi (**run-boundary = denominator semantics**, rule GQ-PR-L0-002/003). Not a card.
- B4 bridge → L-dag (edges + drift_finding/test_link/evidence_gap) + L-bi (feedback loops, promotion) + L-reg (cross-field constraints).

## Branch → client work [SB/H]

- **Cap factory:** meaning = yield/scheduling/cost policy; system = MES/defect/rework events;
  operational = lot-or-order run boundary; bridge = "Q4 line-2 rework spike drifts_from baseline rule".
- **Logistics:** meaning = routing/SLA/carrier policy; system = TMS/delivery/exception/cost events;
  operational = shipment-id run boundary; bridge = "lane A→B late observed_by metric when carrier C in winter".

## Drift detection [SB]

Every promoted business behavior with impact needs ≥1 bridge edge or an explicit evidence gap; drift
edges preserve BOTH the business expectation and the observed behavior (no silent smoothing); bridge
claims asserting alignment must cite evidence from both branches before promotion.

## Residue [H]

Run-boundary (cap factory); event catalog + proof metric per vertical; card runtime graphing dormant
in GoldenQuill; operational branch was missing from old ontology templates (now first-class).
