# Stage 6 — Design: Creative Generation → Dispatch → Measurement → Improvement Loop

- **Role:** creative-pipeline · **receipt:** native-stage · **verdict:** pass

## 1. Creative Variant Data Shape

A **creative variant** is the atomic unit of generation and measurement. It carries:

- **header** `variant_id`, `parent_variant_id` (lineage), `family_id` (control vs challenger grouping), `generation_timestamp`
- **source** `ontology_card_ref` (from §2 Define), `hypothesis_ref` (what we test), `generation_method` (LLM|template|hybrid) **[H]**
- **creative_fields** hook (headline), format (image/video/carousel), body copy, CTA, audience segment, placement (feed|stories|native)
- **objective** (awareness|click|conversion), **lineage_depth** (N generations from base template), **governance_class** (audit needed?)
- **outcome_contract** `response_window_days`, `minimum_sample_size`, `confound_control_strategy` (see §3)

**Rationale [SB]:** per OPTIMIZATION-CHAIN-METHOD.md, every creative is a run node in the Execution DAG. The variant shape operationalizes the chain: hook/format/objective are the *action fact* inputs; the outcome_contract pre-declares how we'll measure "better" (no post-hoc windowing).

## 2. Variant Management & Experiment Structure

**Family** = (control + challenger set) grouped by ontology_card + hypothesis. One family runs concurrently; outcomes are measured over a shared **response_window** (e.g., 72 hours post-dispatch). 

**Validity operationalization [SB, adapt]:**

- **Response window:** fixed at family creation (ontology card declares typical window for the objective). Window is immutable once live — prevents p-hacking. 
- **Minimum sample:** family declares minimum impressions/clicks threshold *before* statistical test — fail-closed if undershot.
- **Confound control:** vector of confounds (day-of-week, network capacity, seasonality, audience churn) pre-declared in hypothesis. Grader (§3) flags uncontrolled confounds as `veracidade: medium|low` with evidence_refs pointing to the declared but unmeasured confound.

**Control variant:** the reigning "best" from prior cycles, or a baseline template. Always included; confounds are *measured as deltas to control*, not absolute lift.

## 3. Feedback Path (Optimization Chain → Next Generation)

**Promotion → Reuse [SB, adapt]:**

When an OwnerDecision approves a variant family (KnowledgeProjection), the promoted outcome becomes a **claim-labeled optimization** per OPTIMIZATION-CHAIN-METHOD.md:

```
When [creative_variant deployed],
measure [outcome_KPI: CTR|conversion_rate|cost_per_acquisition] 
over [response_window_days]
using [analysis_method: cohort_comparison | uplift_model]
to produce [named BI optimization: "hook_pattern_X increases CTR 15%"],
with [claim_label: correlation_candidate | quasi_causal_candidate],
reuse target: [ontology_card.hook_vocabulary | objective_scoring_rule].
```

**Feedback reparam [adapt, ontologize-driven]:**

1. Promoted **winning patterns** (e.g., "emotional hook + urgency CTA" → +18% CTR) update the ontology card's **generation vocabulary** — next LLM calls see the pattern in the system prompt or template weights.
2. **Residue** (unexpected variance, confound signals, edge cases) feed the auto-research pool as **research candidates** — human reviewers propose new hypotheses or variant axes (e.g., "seasonal decay" → test dayparting).
3. **Retired anti-patterns** (statistically significant regressions) are logged in `contradicts` edges in the Promotion DAG, blocking future variants from re-exploring the same space without explicit override.

## 4. Tension T2 Resolution: Generation Strategy

**T2: LLM-gen vs template/asset-library vs hybrid**

**Recommendation: Hybrid with governance gates. [H]**

- **Template/asset-library is the default**: existing approved creative elements (hooks, CTAs, visuals keyed to ontology card) are combined deterministically. Fast, auditable, low-variance. **[SB]** per ontologize's "reuse boundary," promoted patterns become templates.
- **LLM-gen enters when templates exhaust**: after N cycles on one card, a research candidate signals "need novel creative." LLM is prompted with the card's winning patterns (weights, contradictions, retired anti-patterns) as constraints. Output is sandboxed to one-per-family, lower priority than template variants.
- **Governance gate**: LLM-generated variants carry `generation_method: llm` and `veracidade: medium` by default (untested patterns). They advance to OwnerDecision only if template siblings fail to improve. Prevents LLM drift from dominating.

**Rationale:** template-first honors the optimization chain's claim discipline (proven patterns + reuse boundary). LLM as an exploration tool (not default) keeps the loop auditable and captures why new shapes matter (the research candidate tracks the reasoning).

## 5. Tension T3 Resolution: Promotion Cadence

**T3: Online bandit (continuous) vs batch windowed promotion**

**Recommendation: Batch windowed with signaling gates. [H]**

- **Batch cycle**: collect all families that completed their response window over a calendar period (e.g., 2-week sprint). Run deterministic gates (§2.3 DAG-AND-METRICS.md) on the batch: source-truth check, denominator semantics, confound-control declaration, metric≠authority (must cite response window, not raw metric).
- **Signaling gate (early alert)**: if a variant achieves statistical significance early (before full window), emit a `promotion_candidate` flag and alert the OwnerDecision queue, but do **not** promote until the full window closes. Prevents premature optimization.
- **Why not online bandit**: ad networks' traffic is heterogeneous (audience churn, budget fluctuations, creative fatigue). A 72h window is required to observe week-day effects and steady-state performance. Continuous promotion creates false winners and robs the optimization chain of the response-window guard (rule OCM-003).

**Rationale [SB, adapt]:** OPTIMIZATION-CHAIN-METHOD.md §General Contract makes response_window_refs a required contract field. Batch cycles align with the Promotion DAG's deterministic gates (GQ-PR-L0-003, -002 from DAG-AND-METRICS.md §7) and preserve the "evidence first, promotion second" discipline.

## 6. Residue & Next Routes

- **Auto-research scope**: the candidate pool (competitor signals, trend mining, hypothesis generation) is explicitly routed out of this design — owned by the Auto-Research component (05-distill.md §X-ray). Design should cite its input/output contract with generation.
- **Network adapter**: system-agnostic outcome interface (04-research-decision.md) defers real ad-network metric schema. Before MVP pilot, recommend a bounded-research pass validating one network's outcome shape (meta/google/tiktok) against the `outcome_contract` shape in §1.
- **Confound measurement**: current design assumes confounds are pre-declared (honesty about uncertainty). Advanced: hierarchical models or causal inference to *estimate* confound effects — descope from seed; mark as [H] for pilot validation.

---

**T2_recommendation:** Template-library-first generation with LLM as constrained exploration tool; promoted patterns become templates via ontology cards.

**T3_recommendation:** Batch windowed promotion with signaling gates; response windows immutable at family creation per optimization-chain method.

