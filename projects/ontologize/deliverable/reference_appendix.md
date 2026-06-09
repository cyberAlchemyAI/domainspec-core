# CyberAlchemy — Reference Appendix (KPI / Ontology Taxonomy)

> **Candidate reference. Not a contract.** Claims tagged `[proven]` / `[hypothesis]`. The metric
> values shown are illustrative *families and shapes*, not your numbers — your numbers come from the
> pilot and carry `[PLACEHOLDER — fill from <source>]` slots. No fabricated client data.

This appendix is BI-led: it specifies the **graded evidence-linked metric model** first, then the
underlying **ontology / DAG vocabulary** that makes the metrics auditable.

## 1. Evidence discipline (the BI layer)

Every metric separates these states so a number can never silently stand in for a different kind of claim:

| State | Meaning |
| --- | --- |
| Lifecycle stage | Where a run appears to be in its lifecycle. Stage depth is **not** an outcome. |
| Outcome event | A source-backed real-world event (delivered, defected, accepted, returned, …). |
| Validation state | Whether a denominator, source interpretation, or claim has been checked. |
| Graph authority | Whether the run history is traceable and reviewable before it becomes reusable knowledge. |
| Source truth | The source that proves a fact (system export, signed record, operator-confirmed entry). |

**Boundary rules** (a metric never substitutes for a different claim):

```text
lifecycle stage   != outcome truth
a metric value    != promotion authority
a candidate lesson!= approved reuse
raw feedback      != shareable knowledge
```

**[proven]** this evidence-state separation and the boundary rules are lifted from the GoldenQuill
evidence/KPI appendix.

## 2. The graded-BI model — `veracidade` + `evidence_refs`

Each evidence-bearing node carries two formal fields, replacing hand-written "proven/hypothesis" prose
with checkable data:

- **`veracidade` ∈ {high, medium, low}** — how much external evidence confirms the node's claim.
  `high` = tested against reality (production data, ≥1 confirmed run); `medium` = derived from an
  established principle, not yet tested in your system; `low` = untested projection.
- **`evidence_refs`** — the source/event/test locators justifying the grade. **Must be non-empty for
  `high`** — you cannot claim proven without receipts.

This is a **single confidence axis** by design. **[proven]** the `veracidade` axis is borrowed from the
DomainSpec vault. **[hypothesis]** applying it per-node in a client BI layer is the adaptation validated
in the pilot.

> **Meta-metric hook.** Because every promoted lesson carries this grade, the governance layer itself
> becomes measurable — e.g. *what fraction of promoted lessons were `veracidade: high` at decision
> time?* See `gaps/meta-metrics.md`.

## 3. KPI families (vertical-agnostic, with per-vertical instantiation slots)

Adapted from the six GoldenQuill KPI families. **[proven]** the family structure is from the reference
build's KPI appendix. **[hypothesis]** the per-vertical metric is a candidate confirmed in
assessment. Every metric is an evidence-linked observation (denominator + source chain + grade).

| Family (generic) | What it measures | Cap-factory candidate `[hypothesis]` | Logistics candidate `[hypothesis]` |
| --- | --- | --- | --- |
| **Lifecycle depth** | How far each run actually progressed | % orders reaching "accepted" | % shipments reaching "closed" |
| **Outcome evidence** | The source-backed result | defect / rework rate (defects ÷ lots) | on-time-delivery (on-time ÷ *delivered*) |
| **Quality / review movement** | Improvement across iterations | first-pass yield trend | exception-resolution time |
| **Fit / selectivity** | Match of work to capacity/strategy | order-mix vs capacity fit | lane / carrier fit score |
| **Effort & ROI** | Cost and return | cost per good unit | cost per lane / per shipment |
| **Capacity & relationship** | Durable relationship health | supplier / line capacity health | carrier reliability |

Each populated metric must record, in your instantiation:
`[PLACEHOLDER — numerator]`, `[PLACEHOLDER — denominator]`, `[PLACEHOLDER — period]`,
`[PLACEHOLDER — source events]`, `[PLACEHOLDER — interpretation limit]`, `veracidade`, `evidence_refs`.

**Worked example of the discipline (not your number):** "on-time-delivery = on-time ÷ *delivered*, not
÷ *booked* — does not count cancellations." The denominator choice is the audit.

## 4. Ontology / DAG vocabulary (what makes the BI auditable)

### 4a. Node types

**[proven]** adapted from the five GoldenQuill node types. Generic on the left; per-vertical examples right.

| # | Node | Cap factory `[hypothesis]` | Logistics `[hypothesis]` |
| - | ---- | -------------------------- | ------------------------ |
| N1 | **OutcomeEvent** (must carry a source) | lot completed / defect logged | shipment delivered / delayed |
| N2 | **LifecycleState** (stage ≠ outcome) | planned→in-production→shipped→accepted | booked→in-transit→delivered→closed |
| N3 | **MetricObservation** (denominator + grade) | defect-rate, on-time-fulfillment | on-time-delivery, cost-per-lane |
| N4 | **PromotionCandidate** (states how it could be wrong) | "SKU X reworks spike on line 2 in Q4" | "lane A→B late when carrier C used in winter" |
| N5 | **OwnerDecision** (human approve/reject/retire/contradict) | ops lead decision | ops lead decision |
| N6 | **KnowledgeProjection** (promoted lesson, non-empty evidence) | process/scheduling rule | routing/carrier rule |

Nodes N3 / N4 / N6 carry `veracidade` + `evidence_refs` (§2). N1's honesty is its mandatory source; N2
is a deterministic projection.

### 4b. The governed deterministic gates (summary)

**[proven]** eleven L0 rules from the reference build, plus a contradiction gate and the honesty-node
checks, organized as guards on node transitions:

- source-truth (no event without provenance) · stage ≠ outcome · denominator semantics ·
  metric ≠ authority (a metric may not self-promote) · contradiction-path required on every candidate ·
  proposed-uses complete · open contradiction blocks promotion · privacy boundary (scoped feedback
  redacted before shared reuse) · no premature promotion (explicit owner decision required) ·
  approved-decision complete · projection has non-empty evidence · `veracidade` declared on every
  evidence node · `high` requires non-empty evidence · `low` blocks promotion absent an explicit override.

> **A genuine coverage finding (surface in assessment).** No current rule guards the `N2 → N3`
> transition (a lifecycle state feeding a metric). This is an honest gap in the ruleset, not a hidden
> defect — flagged here so it is on the table. **[hypothesis]**.

### 4c. The two linked DAGs

**[proven]** an **execution DAG** (immutable audit spine — what happened, in order) and an **ontology
DAG** (what becomes reusable — points at the execution DAG, never rewrites it). Acyclicity is enforced
**per edge type**, not as a blanket "the whole graph is acyclic" claim.

## 5. The audit ledger

**[hypothesis]** every node mutation appends one row to an **append-only `promotion_events` ledger**
(actor, action, node, reason, source, `veracidade`, `evidence_refs`, per-rule gate results, a hash-chain
pointer for tamper-evidence). A `GATE_BLOCK` row is written even on rejection — the ledger is an
integrity record, not just a success log. **[hypothesis]** the time-series storage choice (sheet / sqlite
/ db) is a pilot decision.
