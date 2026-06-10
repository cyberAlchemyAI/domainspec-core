# Stage 6 — Design: Ontology Reuse

**Role:** ontology-reuse · **capability:** `invoke` mode `design` · **artifact intent:** bind autoads to ontologize's two-axis ontology and DAG, resolving T1.

---

## 1. Two-axis ontology for ad creatives

**Axes [adapt SB ontologize/PRODUCT.md §3]:**
- **Subject/Segment axis** — audience × creative family (e.g., "B2B SaaS buyers" × "product-demo family")
- **Value-mechanism axis** — the ad objective (awareness / click / conversion)

**Ontology Card Structure** (one card per axis value pair):

| Field | Configures | Example (B2B SaaS awareness family) | Source |
|-------|-----------|-----------------------------------|--------|
| `audience_segment` | targeting rules, demographic schema | "B2B SaaS <50 employees" | [adapt] |
| `creative_family` | generation vocabulary, asset templates | "product-demo: 15s video + CTA" | [adapt] |
| `objective` | outcome schema + KPI denominator | awareness: impressions, reach decay window | [adapt] |
| `outcome_schema` | metric shape (numerator/denom/period) | impressions ÷ spend, 7-day window | [SB DAG-AND-METRICS §5 anti-collapse] |
| `veracidade_threshold` | minimum evidence grade for promotion | "high only" or "medium allowed" | [adapt] |
| `language_register` | tone, claims density, formality | "executive-facing, no jargon" | [adapt] |
| `reporting_rhythm` | review cadence (weekly, per-week threshold) | "weekly reflection + 50-impression floor" | [adapt] |
| `interpretation_limits` | what the metric does NOT prove (external validity) | "network-only; does not predict conversion" | [adapt] |

Cards match at runtime (Outcome-Measurement + Grader stages in Creative Learning Cycle) and parameterize the Generator; never hardcoded. **[SB PRODUCT.md §3: match at runtime, never hardcoded]**

---

## 2. Execution DAG and Promotion DAG mapping

**Execution DAG (immutable audit spine, append-only) [SB DAG-AND-METRICS §1]:**

| Creative Run Node | Corresponds to N(ontologize) | Semantics |
|-------------------|-----|-----------|
| `CreativeVariant` proposed | (prologue; not yet N1) | generation hypothesis + source ontology card |
| `CreativeDispatch` event | **N1 OutcomeEvent** | ad network receives variant, timestamp, source |
| `NetworkOutcome` | **N1 OutcomeEvent** | ad network returns impression/click/conversion event with source |
| `LifecycleStage` (proposed → active → paused) | **N2 LifecycleState** | stage ≠ outcome; a paused creative is not a failed creative [SB GQ-PR-L0-003] |
| `MetricObservation` (CTR, ROAS, reach, etc.) | **N3 MetricObservation** | carries denominator (CTR ÷ impressions), `veracidade`, `evidence_refs` [SB §2b] |

**Promotion DAG (ontology meanings, review-gated, owned):**

| Promotion Node | Corresponds to N(ontologize) | Semantics | Ad-specific example |
|---|---|---|---|
| Creative pattern signal | **N4 PromotionCandidate** | "this audience segment + creative family yields 3.2x click lift" + mandatory `contradiction_path` [SB GQ-PR-L0-004] | "Demo videos (family) for mid-market (segment) outperform static on 2 runs; contradicted by: Q2 run showed no lift" |
| Review + owner gate | **N5 OwnerDecision** | marketing ops lead approves/rejects promotion; records `approved_allowed_uses` (reuse target: "next demo variant", "similar segment") [SB GQ-PR-L0-005, -010] | "Approve: feed to next Q3 demo variant; restrict: no cross-segment reuse until 3rd run" |
| Promoted lesson | **N6 KnowledgeProjection** | stored in ontology vault; feeds the ontology card (updates generation vocabulary or `language_register` or raises `veracidade_threshold`) [SB DAG-AND-METRICS §6 feedback target] | Card update: `creative_family.demo += "pattern: 15-30s beats static; confidence: high; 2 tests; owner: mkt_ops_lead"` |

**Event flow [SB DAG-AND-METRICS §4 event model]:**
1. Ingest CreativeDispatch + NetworkOutcome → N1 (gate: source-truth rule GQ-PR-L0-001)
2. Project LifecycleStage → N2 (gate: stage≠outcome rule GQ-PR-L0-003)
3. Compute MetricObservation → N3 (gate: denominator semantics, `veracidade` required; metric ⊘ N4 rule GQ-PR-L0-008)
4. (Optional, human or threshold) Propose PromotionCandidate → N4 (gate: `contradiction_path`, `proposed_allowed_uses`)
5. Privacy gate (redact network-specific or PII fields)
6. Owner reviews and decides → N5 (gate: explicit approval)
7. Project KnowledgeProjection → N6 (gate: non-empty `evidence_refs`)

---

## 3. Coupling-violation / metric≠authority guard for ads

**Problem [SB PRODUCT.md metric≠authority]:** ad-network metrics (CTR, ROAS) can masquerade as truth without governance. A single number hides two failure modes:

1. **Concept erasure** — schema drops a dimension (e.g., "CTR" ignores audience segment, creative family, funnel stage). [SB DAG-AND-METRICS §5]
2. **Number hallucination** — value distorted at compute time (e.g., CTR denominator shifts: impressions in _that network_ vs impressions _that reached unique user_). [SB §5]

**Guard Rules for autoads:**

| Rule | Governs | Blocks | Guard axis |
|------|---------|--------|-----------|
| **metric ⊘ candidate** [GQ-PR-L0-008 adapted] | N3 → N4 edge (forbidden) | A MetricObservation (e.g., "CTR = 3.2%") may NOT directly spawn a PromotionCandidate; a human must propose the candidate with context (audience, family, window, confounds) | number hallucination |
| **denominator explicit** [GQ-PR-L0-002 adapted] | every N3 creation | every CTR/ROAS must state: numerator (which event?), denominator (which ad set scope? per-network or aggregated?), period (7-day window? lifetime?) | concept erasure |
| **ontology card match required** [adapt] | before N1 acceptance | a CreativeDispatch must declare which ontology card (audience+family+objective) it targets; unmapped dispatches are logged but not measured | concept erasure |
| **`veracidade` ≠ network metric** [adapt] | N3 + N4 + N6 creation | `veracidade` is assigned by the Grader using evidence-external-to-the-metric (confound flags, cross-network tests, historical replay). A high-CTR metric is NOT automatically `high` veracidade. | number hallucination |
| **open contradicts blocks promotion** [DAG-AND-METRICS §3, adapted] | N4 → N6 edge (forbidden if edge exists) | a candidate with an unsettled `contradicts` edge cannot become a KnowledgeProjection until an OwnerDecision resolves it | number hallacination |

**Concrete example:** "Demo videos yield 3.2x CTR" (N4 Candidate) requires evidence for veracidade=high: (a) CTR denominator = impressions reaching the intended segment only (no impressions outside), (b) tested on ≥2 independent runs, (c) confounds (time-of-day, network saturation, audience overlap) flagged and ruled-out or controlled, (d) an open `contradicts` edge to "static images actually beat video in Q1" must be resolved before promotion. No single number can pass.

---

## 4. Resolving T1: Ontology granularity

**T1 from distill:** per (audience × family × objective) cards vs per-network cards?

**Recommendation: per (audience × family × objective) cards, not per-network.**

**Rationale:**

1. **Reuse across networks [SB PRODUCT.md §2, §3 generalization claim]:** ontologize's core claim is that ontology cards reuse across verticals (the CyberAlchemy generalization hypothesis). Autoads inherits this: a "B2B SaaS" × "demo video" × "awareness" card should guide creative generation for Google Ads _and_ LinkedIn _and_ Twitter without re-learning the segment. Tying cards to networks forecloses that reuse and defeats the learning-loop promise. **[adapt]**

2. **Per-network metrics are observations, not ontology [SB DAG-AND-METRICS §3 execution vs ontology DAGs]:** network-specific differences (Google's attribution window vs Facebook's event-schema vs LinkedIn's audience overlap) are *execution-DAG* properties (N3 MetricObservations), not ontology-DAG properties (ontology cards). Store network variance in the metric denominator and response window; do not embed it in the card. **[SB]**

3. **Confound control and card match [adapt]:** per-network cards would require separate `veracidade` thresholds, language registers, and interpretation limits for each network, multiplying governance gates without adding clarity. A single card with a generic `interpretation_limits = "network-specific network attribution windows may introduce confound"` is simpler and forces the Grader to name the confound explicitly (rule: audit via contradiction_path). **[adapt]**

4. **Pilot feasibility:** the autoads MVP will likely start with one vertical (one audience × family × objective bundle) and one network (e.g., Google Ads). A per-network design would bake in that one-vertical-one-network structure as the ontology ceiling; a per-axis design allows the second network to reuse the same card and test cross-network generalization. **[adapt]**

**Caveat:** if a future pilot discovers that a demographic segment's response to a creative family is *fundamentally different* across networks (not just attribution-window variance, but actual audience behavior divergence), that finding gets captured as a `contradicts` edge and escalated to owner decision, potentially splitting the card. But we start unified. **[adapt]**

---

## Residue

- **Network-to-card adapter contract:** how does a CreativeDispatch declare its card match? (message schema, validation hook). Deferred to implementation.
- **Confound flagging in Grader:** which external signals (time-of-day, competitor activity, platform feature change) trigger a lower `veracidade`? Tuned in pilot.

---

## Evidence chain

**Source-backed [SB]:**
- ontologize/PRODUCT.md §3 (ontology structure, match at runtime)
- ontologize/DAG-AND-METRICS.md §1 (two DAGs, audit spine)
- ontologize/DAG-AND-METRICS.md §2 (node types N1–N6, adaptation points)
- ontologize/DAG-AND-METRICS.md §3 (edge catalog, metric ⊘ candidate rule GQ-PR-L0-008, contradicts blocking)
- ontologize/DAG-AND-METRICS.md §4 (event model, 7-step flow)
- ontologize/DAG-AND-METRICS.md §5 (anti-collapse, concept erasure vs number hallucination)
- ontologize/DAG-AND-METRICS.md §6 (feedback target: ontology cards, feedback loop closes)

**Adapted [adapt]:**
- Creative card fields (language_register, reporting_rhythm, veracidade_threshold)
- Network Adapter system-agnostic contract (data-governance register application)
- per-axis card design (T1 resolution)
- Ad-specific event types (CreativeDispatch, NetworkOutcome)
- Grader's external-evidence-based veracidade (not network-metric-based)

