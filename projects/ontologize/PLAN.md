# PLAN — CyberAlchemy ontology+DAG engagement

Implementation plan. Maps [DESIGN.md](DESIGN.md) + [IMPLEMENTATION-LAYERING.md](IMPLEMENTATION-LAYERING.md)
into ordered tasks with implementation-detail specs. Complexity: **high**. Execution owner: `task-session`.
Work-pack with SWUs: [WORK-PACK.md](WORK-PACK.md).

## Delivery slices & validation strategy

| Slice                         | Layer | Output                                                                           | Validation                                                                         |
| ----------------------------- | ----- | -------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| S1 Assessment instrument      | L0    | assessment template + filled logistics assessment                                | Client confirms the ontology-map + inventories are accurate                        |
| S1b Lane selection            | L0    | chosen delivery lane (A / B / hybrid) per [DELIVERY-LANES.md](DELIVERY-LANES.md) | Selection rule applied to observable client facts; Lane-B bridges scoped if chosen |
| S2 Method install (logistics) | L1    | 4 installed layers (on the chosen lane), signed register                         | Each layer's evidence gate passes; register signed before agents                   |
| S3 Deliverable template v1    | L1    | client-sendable package (logistics)                                              | Honesty gate: every claim tagged; BI-led ordering present                          |
| S4 Proof harness (logistics)  | L1    | one metric, evidence chain, baseline, movement                                   | Metric traces to evidence chain; movement measured vs baseline                     |
| S5 Cap factory parallel run   | L2    | assessment + method + package (cap factory)                                      | Run-boundary decided; per-vertical metric moved                                    |
| S6 Cross-vertical + hardening | L3    | generalization report + 5 gap sections                                           | Both verticals independent; gaps closed; template reusable                         |

## Implementation-detail specs (algorithmic / domain-logic tasks)

### IDS-1 Assessment ontology-mapping procedure

- **Inputs:** client interviews, sample data, system list.
- **Outputs:** `ontology-map` = {subject_axis: [cards], mechanism_axis: [cards], match_rule: runtime},
  `data-inventory`, `agent-inventory`, `maturity-score`.
- **Rules (ordered):** (1) elicit who/what the client serves → subject axis candidates; (2) elicit
  how value flows (orders/shipments/contracts) → mechanism axis candidates; (3) assert orthogonality —
  reject any baked subject→mechanism binding; (4) for each axis card capture the operational primitives
  (search vocabulary, evidence schema, language register, reporting rhythm); (5) inventory data sources
  with an owner + sensitivity guess; (6) inventory existing agents; (7) score each Four-Autonomy-Rule
  0–3.
- **Edge cases:** continuous-production client with no discrete "run" → flag run-boundary decision;
  client with no agents → maturity-score = 0, agent layer becomes greenfield.
- **Failure modes:** client cannot grant data access → block S2 for that vertical; axes collapse into
  one → re-interview, do not force.
- **Validation evidence:** client sign-off that the map reflects reality.

### IDS-2 Promotion DAG gate ruleset (per vertical)

- **Concrete spec:** [DAG-AND-METRICS.md](DAG-AND-METRICS.md) §2–§7 — the 6 node types, edge set,
  event model, and the 11 GoldenQuill rules generalized. This IDS is the per-vertical instantiation of it.
- **Inputs:** the vertical's run definition + evidence types.
- **Outputs:** a gate ruleset adapting GoldenQuill's 11 L0 rules to the vertical.
- **Rules:** enforce source-truth (every event has a source); metric≠authority (KPIs cannot
  auto-promote); mandatory contradiction path; privacy redaction before any cross-scope reuse;
  propose-vs-approve allowed-uses; stage≠outcome≠validation.
- **Edge cases:** cap factory lot-as-run vs order-as-run (decided in S5 assessment).
- **Failure modes:** no clear outcome signal → metric cannot be evidence-linked → pick a different metric.
- **Validation:** dry-run the ruleset on sample historical runs.

### IDS-3 Proof-harness measurement

- **Concrete spec:** metric families + anti-collapse denominator rule in
  [DAG-AND-METRICS.md](DAG-AND-METRICS.md) §5. The proof metric is one `MetricObservation` from those families.
- **Inputs:** chosen metric, its evidence chain, a baseline window.
- **Outputs:** baseline value, post-install value, movement + interpretation limits.
- **Rules:** metric must trace to source events (no dashboard-only numbers); state denominator
  definition; record interpretation limits (anti-collapse).
- **Failure modes:** baseline window too short / noisy → widen window, mark low-confidence.
- **Validation:** an independent reviewer can reproduce the number from the evidence chain.

## Native handoff readiness

- Capability handles: `task-session` (execution), optional `whisper` (deliverable prose),
  `decision-gate` (run-boundary if contested), `feature-glossary` (taxonomy).
- Expected receipts: per-slice artifacts + validation result.
- Fallback boundary: assessment + design are author-time; client-data steps require operator presence
  and signed register (no autonomous agent runs on client data).

## Unresolved gaps

Per-vertical proof metric (D-defer-1), buyer per client (D-defer-2), sequencing (D-defer-3), candidate
axes (A1) — all resolve inside S1/S5 assessments, none block planning.
