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
graph points at it. Acyclicity is enforced **per edge type**, not as a blanket "the whole graph is
acyclic" claim — see the acyclic set in the [edge catalog](#3-edge-catalog-how-nodes-connect--governed)
(§3); a few evidence/contradiction edges are legitimately non-acyclic.

> **Branch view:** the two DAGs sit across the 4 ontology branches (see
> [ONTOLOGY-BRANCHES.md](ONTOLOGY-BRANCHES.md)) — the execution DAG ≈ system + run-context branches;
> the ontology DAG ≈ meaning + bridge branches. Metric denominators live in the run-context branch.

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

### 2b. Node confidence fields (formalizing proven/hypothesis)

The three **evidence-bearing** node types — **N3 MetricObservation, N4 PromotionCandidate, N6
KnowledgeProjection** — carry two formal fields, replacing the project's hand-written proven/hypothesis
prose with checkable data:

- **`veracidade`** ∈ {high, medium, low} **[adapt]** — how much external evidence confirms this node's claim.
  `high` = tested against reality (production data, ≥1 confirmed run); `medium` = derived from
  established principle, not yet tested in this client's system; `low` = untested projection/guess.
- **`evidence_refs`** — list of source/event/test locators justifying the `veracidade` value. May be
  empty for `low`/`medium`; **must be non-empty for `high`** (you cannot claim proven without receipts).

This is a **single confidence axis**, deliberately *not* the vault's `veracidade` × `convicção` 2×2.
Internal commitment (convicção) is already materialized in the DAG topology — an approved `OwnerDecision`
with `approved_allowed_uses` *is* the commitment signal — so a second scalar would correlate with
"has this been promoted?" and fail the orthogonality test. Only veracidade has no structural proxy.
**N1 OutcomeEvent** and **N2 LifecycleState** are deliberately excluded: an OutcomeEvent's honesty is
its mandatory `source` (sourced or rejected), and LifecycleState is a deterministic projection governed
by stage≠outcome. So this is **2 fields on 3 of 6 node types**, not a label on everything. **[adapt** —
borrows the `veracidade` axis from `domainspec/vault`; convicção dropped by the orthogonality heuristic.
Residue: re-introducing convicção is the documented escape hatch if a "proven-but-unexploited" portfolio
signal is later needed.**]**

> **Orthogonality is a design heuristic here, not a computed gate.** We use the "does this field add
> information the node doesn't already carry?" test to keep the field set lean (it justified dropping
> 4 of the vault's labels and the convicção axis). We do **not** import the formal `I(Lᵢ;Lⱼ)=0`
> measurement — a client engagement has neither the corpus nor the tooling to compute it, and claiming
> so would overstate rigor.

---

## 3. Edge catalog (how nodes connect — governed)

The edges are not a loose list: each one is governed by an explicit **source-type → target-type**
rule, a cardinality, a named inverse, a category, and whether it must be acyclic. This is the
concrete expression of the "two acyclic graphs kept orthogonal" idea — it is what makes the
deterministic gate testable (§8) and the client's graph auditable. Node shorthand: **OE**
OutcomeEvent · **LS** LifecycleState · **MO** MetricObservation · **PC** PromotionCandidate ·
**OD** OwnerDecision · **KP** KnowledgeProjection. Categories: **execution** (the immutable audit
spine), **promotion** (the ontology-DAG governance chain), **structural** (B4 bridge edges across
branches), **control** (DAG gate/approval edges).

| Edge (forward)    | Source → Target      | Card. | Inverse              | Category   | Acyclic? | Tag      |
| ----------------- | -------------------- | ----- | -------------------- | ---------- | -------- | -------- |
| `precedes`        | OE → OE              | 1:N   | `preceded_by`        | execution  | **yes**  | [SB]     |
| `consumes`        | OE → OE,MO,OD,KP     | N:M   | `consumed_by`        | execution  | **yes**  | [SB]     |
| `emits`           | OE → OE,MO           | N:M   | `emitted_by`         | execution  | **yes**  | [SB]     |
| `revised_by`      | OE,KP → OD           | N:M   | `revises`            | execution  | **yes**  | [SB]     |
| `observed_by`     | LS,OE → MO           | N:M   | `observes`           | structural | **yes**  | [SB]     |
| `realized_by`     | KP → OE,LS           | 1:N   | `realizes`           | structural | no       | [SB]     |
| `depends_on`      | KP → KP              | N:M   | `depended_on_by`     | structural | **yes**  | [SB]     |
| `tested_by`       | KP,PC → OE,MO        | N:M   | `tests`              | structural | no       | [SB]     |
| `traced_to`       | PC,OD,KP → OE,MO     | N:M   | `traced_from`        | structural | **yes**  | [SB]     |
| `drifts_from`     | MO,OE → KP           | N:M   | `drift_observed_by`  | structural | no       | [SB]     |
| `contradicts`     | PC → PC,KP           | N:M   | `contradicts` (sym)  | promotion  | no¹      | [adapt]  |
| `promotes_to`     | PC → KP              | 1:1   | `promoted_from`      | promotion  | **yes**  | [SB]     |
| `supersedes`      | KP → KP              | 1:1   | `superseded_by`      | promotion  | **yes**  | [SB]     |
| `retires`         | OD → KP,PC           | 1:N   | `retired_by`         | promotion  | **yes**  | [SB]     |
| `constrains`      | KP → KP,PC           | N:M   | `constrained_by`     | promotion  | **yes**  | [SB]     |
| `validates`       | OE,MO → PC,KP        | N:M   | `validated_by`       | promotion  | **yes**  | [SB]     |
| `blocked_by_gate` | OE,PC → OD           | N:1   | `gates`              | control    | **yes**  | [SB]     |
| `approved_by`     | PC → OD              | N:1   | `approves`           | control    | **yes**  | [SB]     |

¹ `contradicts` is symmetric (same name both ends) and is the one edge that is *not* acyclic, but
**self-loops are forbidden** — a candidate cannot contradict itself.

**`contradicts` vs `drifts_from` (the load-bearing distinction).** `drifts_from` is the *raw,
neutral signal*: an observation (MO/OE) diverges from intended meaning (KP), preserving **both**
sides with no smoothing. `contradicts` is the *adjudicated conflict*: two governance artifacts
(PC↔PC or PC↔KP) logically exclude each other. The rule: a `drifts_from` finding feeds a
`PromotionCandidate`; if that candidate logically excludes already-promoted knowledge it declares
`contradicts → KP`, and **a candidate with any open `contradicts` edge cannot be promoted** (cannot
gain a `promotes_to` edge) until an `OwnerDecision` resolves it. This is the candidate-only guardrail
expressed as a graph rule — `contradicts` only ever *blocks* promotion, it never promotes anything.
`contradicts` is declared on the artifact (PC/KP), never raised by a raw OutcomeEvent. **[adapt** —
generalizes GoldenQuill's mandatory `contradiction_path` (rule GQ-PR-L0-004) into a first-class edge;
patterned on the `domainspec/vault` `contradicts` edge, which is symmetric and promotion-blocking**]**

**Acyclic set** (enforced by the cycles check the Lane-B `inventory lint` bridge runs): `precedes,
consumes, emits, revised_by, observed_by, depends_on, traced_to, promotes_to, supersedes, retires,
constrains, validates, blocked_by_gate, approved_by`. **Non-acyclic:** `realized_by, tested_by,
drifts_from, contradicts`. Note "the graph is acyclic" is too strong as a blanket claim — acyclicity
is **per-edge-type**, not per-graph; the evidence edges (`tested_by`, `drifts_from`) and `contradicts`
are legitimately non-acyclic.

> **Authoring note (do not over-govern).** Inverses are catalogued for documentation and query, but
> ontologize's DAG is append-only rows (Lane A) or `inventory`/`ontology-vault` entries (Lane B)
> where the inverse is *computed*, not hand-authored. Do **not** import the vault's "declare the edge
> on both endpoints" rule — that constraint exists because the vault is hand-written Markdown; it does
> not apply to a row-based DAG.

---

## 4. The event model (what updates the DAG)

This is the part the old design omitted. An update is **event-driven**: a real-world signal becomes
an `OutcomeEvent`, which may move a `LifecycleState`, refresh a `MetricObservation`, and _optionally_
spawn a `PromotionCandidate`. Nothing auto-promotes.

**Update sequence (per run):**

1. **Ingest event** → create `OutcomeEvent` with source (else reject — rule GQ-PR-L0-001). **[SB]**
2. **Project lifecycle** → update `LifecycleState`; stage depth is _not_ an outcome (rule GQ-PR-L0-003). **[SB]**
3. **Refresh metrics** → recompute `MetricObservation`s; each needs a denominator definition
   (numerator/denominator/period), is stamped with `veracidade` + `evidence_refs` (§2b), and may _not_
   trigger promotion directly (rules GQ-PR-L0-002, -008). **[SB** + [adapt] for the confidence fields**]**
4. **Maybe propose** → a human or rule may raise a `PromotionCandidate` with a mandatory
   `contradiction_path`, `proposed_allowed_uses`, and `veracidade` + `evidence_refs` (rules GQ-PR-L0-004,
   -011). **[SB** + [adapt]**]**
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

**Anti-collapse principle (the differentiator).** A metric can fail in two structurally independent
ways, and one number cannot see both:

- **Concept erasure** — the metric's _schema_ drops a dimension the business actually carries (a flat
  win-rate with no slot for lifecycle depth, realization gap, or evidence quality). The concept is
  gone before any number is computed.
- **Number hallucination** — the metric's _value_ is fabricated or distorted at populate-time: a
  denominator silently swapped (÷ booked vs ÷ delivered), a default substituted for a missing input,
  a join inventing rows the source events never authorized.

These are **two separate audits**: a reviewer who only checks "the metric is defined over the right
dimensions" still passes a hallucinated value, and a reviewer who only checks "the number reconciles"
still passes a metric whose schema dropped a dimension. So every `N3 MetricObservation` must report a
**pair, not a number** — its denominator/dimension definition (guards concept erasure) _and_ its
source-event chain with interpretation limit (guards number hallucination). No single headline number
stands alone (e.g., "on-time-delivery ÷ _delivered_, not ÷ _booked_ — does not count cancellations").

> **Grounding (honest framing).** This two-axis split is an _interpretive principle_, not a proof. It
> adapts the schema-residue vs instance-residue distinction from the DomainSpec two-layer framework
> (`../domainspec-theorem/docs/domainspec-two-layer-framework.md` §2.4). That framework has a
> Lean-checked no-go result (`M6Counter.lean`) showing schema-level correctness does not force
> instance-level fidelity — but that theorem is about functorial data migration and is _silent on
> metrics and scoring_; the framework's own README classes BI/KPI-style applications as a
> plausible-but-unproven fit. We use the vocabulary because it names a real, separable pair of failure
> modes our gates already enforce (denominator semantics vs source-truth); we do **not** claim a
> mathematical proof that our KPIs cannot collapse. **[adapt** — interpretive grounding, not [SB], not
> proven**]**

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

### Optimization chain method (the BI-expression layer)

[OPTIMIZATION-CHAIN-METHOD.md](OPTIMIZATION-CHAIN-METHOD.md) adds the BI-expression layer **on top of**
this loop. Where the engine (§9) *runs* the loop and grades each metric (`veracidade` + `evidence_refs`),
the optimization chain is how a *graded* metric becomes a client-facing business-intelligence claim
without letting the metric self-promote. A chain binds:

```text
RunNode + MetricObservation (carrying veracidade) + response window + analysis method -> named BI optimization
```

The chain carries seven expression forms, a claim label, interpretation limits, privacy scope, and an
owner-decision route. It does not compete with the engine or the ledger — it *consumes* their graded
output and expresses it. **[adapt]**

---

## 7. Deterministic gates (as typed transition guards)

The 11 GoldenQuill L0 rules become the vertical-agnostic gate ruleset (this is [PLAN.md](PLAN.md)
IDS-2 made concrete). Instead of a flat list, each rule is organized as a **guard on a node-type
transition** — a rule fires on a specific `Nx → Ny` edge. This makes coverage gaps visible and gives
the validator (§8) a transition-indexed structure to test. The last column ties each gate back to the
two anti-collapse axes in §5.

| Rule (GoldenQuill ID)                | Governs transition  | Node edge          | What it guards                                | Residue axis        |
| ------------------------------------ | ------------------- | ------------------ | --------------------------------------------- | ------------------- |
| GQ-PR-L0-001 Source-truth            | ingest → exists     | (source) → **N1**  | no event without provenance                   | number hallucination|
| GQ-PR-L0-003 Stage ≠ outcome         | N1 → N2             | **N1 → N2**        | stage depth is never outcome truth            | concept erasure     |
| GQ-PR-L0-002 Denominator semantics   | N1 → N3             | **N1 → N3**        | every metric defines numerator/denom/period   | concept erasure     |
| GQ-PR-L0-008 Metric ≠ authority      | N3 → N4 (blocked)   | **N3 ⊘ N4**        | a metric may not self-promote                 | number hallucination|
| GQ-PR-L0-004 Contradiction path      | → N4                | **→ N4**           | every candidate states how it could be wrong  | number hallucination|
| GQ-PR-L0-011 Proposed-uses complete  | → N4                | **→ N4**           | candidate carries `proposed_allowed_uses`     | concept erasure     |
| (catalog) Contradiction gate         | N4 → N6 (blocked)   | **N4 ⊘ N6**        | open `contradicts` edge blocks promotion      | number hallucination|
| GQ-PR-L0-006 Privacy boundary        | N4 → N5             | **N4 → N5**        | scoped feedback redacted before shared reuse  | governance (both)   |
| GQ-PR-L0-005 No premature promotion  | N4 → N5             | **N4 → N5**        | reuse needs an explicit owner decision        | number hallucination|
| GQ-PR-L0-010 Approved-decision complete | N4 → N5          | **N4 → N5**        | decision carries `approved_allowed_uses` + `decision_source` | concept erasure |
| GQ-PR-L0-007 Projection evidence     | N5 → N6             | **N5 → N6**        | projection has non-empty `evidence_refs`      | number hallucination|
| GQ-PR-L0-009 Projection kind         | N5 → N6             | **N5 → N6**        | `record_kind = promotion_record`              | concept erasure     |
| G-honesty-node (a) veracidade declared | → N3,N4,N6        | **→ N3,N4,N6**     | every evidence-bearing node declares `veracidade` | number hallucination|
| G-honesty-node (b) high needs evidence | → N3,N4,N6        | **→ N3,N4,N6**     | `veracidade=high` requires non-empty `evidence_refs` | number hallucination|
| G-honesty-node (c) low blocks promotion | N4 → N6 (blocked) | **N4 ⊘ N6**       | `veracidade=low` blocks promotion unless `approved_allowed_uses` has a strategic-bet override | concept erasure |

> **Framing.** This table organizes the rules as typed guards on node-type transitions, adapting the
> "typed edge-law" idea (`EdgeLaw : MetaType → MetaType → Prop`) from the DomainSpec formalization. It
> is an _organizational schema_, not a formalization: in the theorem repo `EdgeLaw` is an opaque axiom
> with no populated law table, and our node types (N1–N6) are not its meta-types. The value is that
> every gate now has an explicit `from-type → to-type` home, which makes coverage gaps visible — e.g.
> **no rule currently guards `N2 → N3`** (a lifecycle state feeding a metric), a genuine finding worth
> surfacing in assessment. **[adapt** — organizational, not formalized**]**

**G-honesty-node (a generalization of GQ-PR-L0-007/-009, not a net-new rule).** Three deterministic
rules generalize projection-integrity (GQ-PR-L0-007/-009) from N6 alone to all three evidence-bearing
nodes (N3/N4/N6): (a) every N3/N4/N6 node must declare `veracidade ∈ {high, medium, low}` — block if
absent; (b) `veracidade: high` requires non-empty `evidence_refs`; (c) a candidate may not advance to
`promoted` (the N4→N6 transition only — an N3 MetricObservation is observed, not promoted) while
`veracidade: low` without an explicit `approved_allowed_uses` override stating the strategic-bet
rationale. This replaces "block on untagged capability claims" (a prose grep) with a node-level
assertion. **[adapt]**

---

## 8. Validation hook

The ruleset is testable the same way GoldenQuill tests it: a fixture pack of positive/negative cases
run through a deterministic validator (cf. `grant_dag/validate.py` + `test_promotion_record_l0.py`).
The pilot (work-pack T3/T5) dry-runs the ruleset on the client's sample historical runs before any
live use. **[SB** test pattern**]**

The optimization-chain schema (the BI-expression layer, §6) is validated separately through
[schemas/optimization-chain-method.schema.json](schemas/optimization-chain-method.schema.json), with
the first example at
[examples/optimization-chain.logistics-exception-resolution.json](examples/optimization-chain.logistics-exception-resolution.json).

## 9. Engine & audit ledger (who operates the loop)

The nodes/edges/gates above are the *vocabulary*; the runtime *operator* is the engine — 5 agents over
the 6 node types plus a human OwnerDecision gate, and an append-only `promotion_events` ledger that
makes every mutation auditable. Full spec, agent↔node mapping, ledger schema, per-lane placement, and
the buildable-vs-aspirational callouts: **[ENGINE.md](ENGINE.md)**.

- **Intake** emits N1 (gate 1) · **Run Tracker** maintains N2 (gate 3) · **Gate Runner** runs the §7
  rules fail-closed · **Promotion Scorer** proposes N4 + maintains N3 trend · **OwnerDecision** (human)
  is the trust gate · **Receipts/Query** serves N6 + ledger.
- The `promotion_events` ledger is append-only (INSERT only) — this upgrades the P3 audit-integrity
  guardrail from convention to enforced invariant; a `GATE_BLOCK` row is written even on rejection. **[adapt]**

---

## Residue

- Run-boundary for cap factory (lot vs order) — assessment decision (S5). **[H]**
- Exact event catalog + the one proof metric per vertical — assessment (D-defer-1). **[H]**
- Reflection cadence + thresholds — pilot tuning. **[H]**
- GoldenQuill's own open items (owner-decision persistence, PromotionRecord home) are upstream and
  not ours to resolve.
