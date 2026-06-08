# DAG & Metrics — concrete design

Concrete answer to: _how is the DAG structured, which events update it, which metrics do we track,
and how does it improve over time?_ Produced by the refine run
[`ontologize-dag-metrics-20260608`](development/refinement-runs/ontologize-dag-metrics-20260608/).

**Source basis.** Lifted from GoldenQuill's promotion-record DAG on `master`
(`projects/goldenquill/pipeline/grant_dag/validate.py` — 5 node types + 11 rules) and its KPI
families. Each element below is **[SB]** source-backed (with path), **[adapt]** a generalized
adaptation, or **[H]** hypothesis to validate in the pilot. GoldenQuill is read-only; nothing here
is promoted to canonical vocabulary, and no pricing/clients are committed.

---

## 1. Two linked DAGs (the structure)

GoldenQuill keeps **two** acyclic graphs, and we keep the same split — it is the load-bearing idea.
**[SB** `goldenquill_promotion_governance_architecture_design_2026-06-01.md`**]**

- **Execution DAG** — _what happened, in order._ The operational trace of a run. Append-only; never
  mutated by learning. This is the audit spine.
- **Ontology DAG** — _what it means / what becomes reusable._ Sits after-and-around the execution
  DAG and never rewrites it (audit integrity / promotion primitive P3).

The two graphs share nothing except references — the execution record is immutable; the ontology
graph points at it.

> **Branch view:** the two DAGs sit across the 4 ontology branches (see
> [ONTOLOGY-BRANCHES.md](ONTOLOGY-BRANCHES.md)) — the execution DAG ≈ system + operational branches;
> the ontology DAG ≈ meaning + bridge branches. Metric denominators live in the operational branch.

---

## 2. Node types (the vocabulary of the DAG)

Adapted directly from the five GoldenQuill fixture/node types in `validate.py` **[SB]**. Generic
form on the left, per-vertical instantiation on the right.

| #   | Generic node                                                                         | GoldenQuill origin [SB]       | Cap factory [adapt]                                             | Logistics [adapt]                                    |
| --- | ------------------------------------------------------------------------------------ | ----------------------------- | --------------------------------------------------------------- | ---------------------------------------------------- |
| N1  | **OutcomeEvent** — a source-backed real-world event                                  | `GrantOutcomeEvent`           | lot completed / order shipped / defect logged / return received | shipment delivered / delayed / damaged / cost posted |
| N2  | **LifecycleState** — projection of the deepest verified stage (≠ outcome)            | `application_lifecycle_state` | order stage (planned→in-production→shipped→accepted)            | shipment stage (booked→in-transit→delivered→closed)  |
| N3  | **MetricObservation** — a read-model metric with denominator semantics               | `GrantKpiObservation`         | defect-rate, on-time-fulfillment                                | on-time-delivery, cost-per-lane                      |
| N4  | **PromotionCandidate** — a proposed reusable lesson/relation (not yet authoritative) | `PromotionCandidate`          | "SKU X reworks spike on line 2 in Q4"                           | "lane A→B late when carrier C used in winter"        |
| N5  | **OwnerDecision** — explicit approve/reject/retire/contradict                        | `OwnerDecision`               | ops lead decision                                               | ops lead decision                                    |
| N6  | **KnowledgeProjection** — promoted lesson written into the governed store            | `OntologyVaultProjection`     | process/scheduling rule                                         | routing/carrier rule                                 |

Each **OutcomeEvent** must carry a **source** (`type`, `locator`/`uri`, `captured_at`) — no event
without provenance. **[SB** `_has_source()`, rule GQ-PR-L0-001**]**

---

## 3. Edge types (how nodes connect)

From the execution-DAG edge set **[SB** architecture design §1**]**, kept generic:

- `precedes` — ordering between events.
- `consumes` — a step used a source/artifact/decision.
- `emits` — a step produced an event/artifact.
- `blocked_by_gate` — a deterministic gate stopped traversal (the critical control edge).
- `revised_by` — an artifact was changed by later review.
- `approved_by` — a human/owner approval permitted the next transition.
- Ontology-DAG edges (`proposed_relation`): `promotes_to`, `supersedes`, `retires`, `constrains`,
  `validates` **[SB** PromotionCandidate `proposed_relation`**]**.

---

## 4. The event model (what updates the DAG)

This is the part the old design omitted. An update is **event-driven**: a real-world signal becomes
an `OutcomeEvent`, which may move a `LifecycleState`, refresh a `MetricObservation`, and _optionally_
spawn a `PromotionCandidate`. Nothing auto-promotes.

**Update sequence (per run):**

1. **Ingest event** → create `OutcomeEvent` with source (else reject — rule GQ-PR-L0-001). **[SB]**
2. **Project lifecycle** → update `LifecycleState`; stage depth is _not_ an outcome (rule GQ-PR-L0-003). **[SB]**
3. **Refresh metrics** → recompute `MetricObservation`s; each needs a denominator definition
   (numerator/denominator/period) and may _not_ trigger promotion directly (rules GQ-PR-L0-002, -008). **[SB]**
4. **Maybe propose** → a human or rule may raise a `PromotionCandidate` with a mandatory
   `contradiction_path` and `proposed_allowed_uses` (rules GQ-PR-L0-004, -011). **[SB]**
5. **Govern** → privacy gate: org/client-scoped feedback can't become shared reuse without
   redaction/generalization (rule GQ-PR-L0-006). **[SB]**
6. **Decide** → `OwnerDecision`; only an approved decision (with `approved_allowed_uses` +
   `decision_source`) confers reuse (rules GQ-PR-L0-005, -010). **[SB]**
7. **Project knowledge** → `KnowledgeProjection` with non-empty `evidence_refs`, `record_kind =
promotion_record` (rules GQ-PR-L0-007, -009). **[SB]**

**Concrete event catalog (candidate, validate in assessment):**

- Cap factory **[H]**: `lot_completed`, `defect_logged`, `order_shipped`, `order_accepted`,
  `return_received`, `rework_logged`. Run boundary = lot OR order (decided in assessment, S5).
- Logistics **[H]**: `shipment_booked`, `picked_up`, `delivered`, `delivery_exception` (late/damaged),
  `cost_posted`, `claim_filed`. Run boundary = shipment (clean).

---

## 5. Metrics (what we track)

Adapted from GoldenQuill's KPI families **[SB** `evidence_and_kpi_appendix.md`**]**. Every metric is an
`N3 MetricObservation`: it carries a denominator definition, interpretation limits, source events,
and a promotion owner — so it is **evidence-linked** and cannot silently drift.

| Family (generic)              | GoldenQuill family [SB]   | Cap factory metric [adapt/H]        | Logistics metric [adapt/H]             |
| ----------------------------- | ------------------------- | ----------------------------------- | -------------------------------------- |
| **Lifecycle depth**           | Lifecycle Depth           | % orders reaching "accepted"        | % shipments reaching "closed"          |
| **Outcome evidence**          | Outcome Evidence          | defect/rework rate (defects ÷ lots) | on-time-delivery (on-time ÷ delivered) |
| **Quality / review movement** | Quality & Review Movement | first-pass yield trend              | exception-resolution time              |
| **Fit / selectivity**         | Strategy Fit              | order-mix vs capacity fit           | lane/carrier fit score                 |
| **Effort & ROI**              | Effort & ROI              | cost per good unit                  | cost per lane / per shipment           |
| **Capacity & relationship**   | Capacity & Relationship   | supplier/line capacity health       | carrier reliability / relationship     |

**Anti-collapse rule (the differentiator):** no single headline number stands alone. Each metric
states its denominator and interpretation limit (e.g., "on-time-delivery ÷ _delivered_, not ÷
_booked_ — does not count cancellations"). **[SB** rule GQ-PR-L0-002 + appendix boundary rules**]**

**Proof metric (one per vertical, picked in assessment — D-defer-1):** cap factory = defect/rework
rate _or_ on-time-fulfillment; logistics = on-time-delivery _or_ cost-per-lane.

---

## 6. Improve-over-time loop (how it gets better)

The improvement loop is the **observe → propose → approve → project → feed-back** cycle, governed so
learning is safe. **[SB** promotion state model**]**

```text
OutcomeEvents  ──▶ MetricObservations ──▶ (signal a) PromotionCandidate
                                                  │  (contradiction_path required)
                                          privacy/redaction gate
                                                  ▼
                                            OwnerDecision
                            ┌──────────────┬───────┴───────┬──────────────┐
                         approved        rejected        retired      contradicted
                            │               │               │              │
                    KnowledgeProjection   residue        history       residue+path
                            │
                 feeds the ontology cards / routing rules / agent gates
                            │
                  next runs are routed/scored using the promoted lesson
```

- **State machine [SB]:** `captured → candidate → reviewed → decision_pending →
{promoted | rejected | retired | contradicted}`. Reuse only within the target's rules after approval.
- **Feedback target:** a promoted `KnowledgeProjection` updates the ontology cards, the classification
  register, the routing rules, or the deterministic gates — so the _next_ run is discovered, routed,
  or scored better. That closing edge is what makes the system improve rather than just log. **[adapt]**
- **Contradiction handling:** every candidate states how it could be wrong; counterevidence moves it
  to `contradicted` and preserves the path (no silent stale "truth"). **[SB** rule GQ-PR-L0-004**]**
- **Cadence [H]:** a periodic reflection pass (per N runs or per quarter) batches candidates for owner
  review — GoldenQuill's Reflection-Packet shape, adapted. Frequency/severity thresholds decide what
  reaches the owner.

---

## 7. Deterministic gates (reused verbatim, generalized)

The 11 GoldenQuill L0 rules become the vertical-agnostic gate ruleset (this is [PLAN.md](PLAN.md)
IDS-2 made concrete). The six that always apply:

1. Source-truth — every OutcomeEvent has a source. (GQ-PR-L0-001)
2. Denominator semantics — every metric defines numerator/denominator/period. (GQ-PR-L0-002)
3. Stage ≠ outcome — lifecycle depth is never outcome truth. (GQ-PR-L0-003)
4. Contradiction path — every candidate states how it could be wrong. (GQ-PR-L0-004)
5. No premature/auto promotion — approved uses need an owner decision; metrics can't self-promote.
   (GQ-PR-L0-005, -008)
6. Privacy boundary — scoped feedback needs redaction before shared reuse. (GQ-PR-L0-006)

Plus projection integrity (GQ-PR-L0-007, -009) and approved-decision completeness (GQ-PR-L0-010, -011).

---

## 8. Validation hook

The ruleset is testable the same way GoldenQuill tests it: a fixture pack of positive/negative cases
run through a deterministic validator (cf. `grant_dag/validate.py` + `test_promotion_record_l0.py`).
The pilot (work-pack T3/T5) dry-runs the ruleset on the client's sample historical runs before any
live use. **[SB** test pattern**]**

## Residue

- Run-boundary for cap factory (lot vs order) — assessment decision (S5). **[H]**
- Exact event catalog + the one proof metric per vertical — assessment (D-defer-1). **[H]**
- Reflection cadence + thresholds — pilot tuning. **[H]**
- GoldenQuill's own open items (owner-decision persistence, PromotionRecord home) are upstream and
  not ours to resolve.
