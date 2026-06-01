# Six Forms of Value — Card Optimization Rubric

**Status:** v0.1 Beta scoring lens. Lands as durable infrastructure per Embedding Plan §A.3 P2-2.
**Source canon:** `Cards_Prompts_and_Research_Plans_v2_fused.md` §2 + GPT package §3.
**Companion:** `skills/tilth-card-research/SKILL.md` (the Master Activation Prompt that produces card content scored against this rubric).

## Why this rubric exists

Cards that only improve **drafting value** are under-leveraged. A finished CIC or CLC must demonstrably move the needle across all six axes — search, evidence, drafting, review, compliance, memory — or the work that produced it stopped early.

The rubric is the lens used when:

- Authoring a new card or refining an existing one (research-time)
- Scoring whether a card is ready for LOCK ceremony (review-time)
- Designing the per-arm scoring dimensions in the Three-Arm Study (eval-time)
- Pitching the card system to external evaluators (narrative-time)

## The Six Forms

| # | Form | What it asks | Where it lives at runtime | Primary seat consumer |
|---|------|-------------|---------------------------|------------------------|
| 1 | **Search value** | Does this card improve the system's ability to *discover* the right opportunity for the applicant? | CIC: `search_vocabulary.core_terms`, `funder_program_keywords`, `disqualifier_terms`. CLC: `funding_mechanism_summary`, `common_application_forms`. | Scout |
| 2 | **Evidence value** | Does this card surface the missing-evidence interview the applicant actually needs? | CIC: `kfr_fact_classes`, `evidence_signals`, `provenance_requirements`. CLC: `evidence_weights`, `common_red_flags`. | Scout + Scribe + Archivist |
| 3 | **Drafting value** | Does this card improve register, structure, claim discipline, and applicant-voice preservation? | CIC: `register_defaults`, `dialect_routing_table`, `admin_risk_term_register`, `narrative_sections_typical`. CLC: `narrative_section_patterns`, `budget_structure_conventions`, `reviewer_profile_typical`. | Scribe |
| 4 | **Review value** | Does this card sharpen Judge scoring, surface red flags, and produce actionable revision plans? | CIC: `capacity_signals_required`, `compliance_burdens`, `common_risk_register_entries`. CLC: `underwriting_criteria`, `scoring_weight_patterns`, `evidence_weights`, `common_red_flags`. | Judge + Red Team |
| 5 | **Compliance value** | Does this card hand off cleanly to Logician + Program Rule Packs without embedding live program law? | CIC: `provenance_requirements`, `compliance_burdens`, `admin_risk_term_register`. CLC: `common_application_forms`, `compliance_obligations`, `provenance_requirements`. | Logician |
| 6 | **Memory value** | Does this card encode post-award commitment-tracking + renewal-evidence patterns so each cycle compounds? | CIC: `kfr_fact_classes`, `common_risk_register_entries`, `reporting_cadence_typical`, `metrics_table_template`. CLC: `commitment_tracking_pattern`, `reporting_requirements_typical`. | Archivist + Report Generator |

## Scoring schema

Each card is scored 0–4 on each axis. Aggregate is reported as a 6-tuple, not a sum — cards have different shapes and the tuple keeps the shape visible.

| Score | Label | Meaning |
|-------|-------|---------|
| 0 | **Absent** | Field empty or stub; no content; no provenance. |
| 1 | **Skeletal** | Structurally present but content is generic or uncited; would not influence runtime seat behavior. |
| 2 | **Partial** | Some content with citations; covers the most common patterns; gaps marked NEEDS_REVIEW. |
| 3 | **Substantive** | Comprehensive content with primary-source citations; covers modal + edge cases; structural alignment with seat consumption verified. |
| 4 | **Differentiating** | Content that demonstrably outperforms uncarded baseline in the Three-Arm Study (or, pre-study, in informal carded-vs-uncarded comparison). Source citations include award-abstracts + reviewer rubrics, not just program pages. |

Scores must be evidence-able: a 3 or 4 score requires a pointer to the content + the citation pattern that justifies the score. Scoring without that pointer is hallucination.

## Per-form scoring guidance

### 1. Search value — Scout-facing

A card scores well on Search value when:

- `core_terms` includes the modal funder vocabulary AND the modal applicant vocabulary AND the modal disqualifier vocabulary
- `funder_program_keywords` cover the federal + state + foundation + corporate breakdown relevant to the axis
- `disqualifier_terms` actually disqualify (test: can Scout reject a wrong-fit opportunity that contains a disqualifier?)
- `synonym_map` covers the legacy / current / movement-language variants

A card with weak Search value forces Scout to do brute-force keyword matching and misses opportunities Scout *should* find. The opportunity-discovery layer is the Six-Forms axis most visible to operators because it controls the daily-pipeline-volume gauge.

### 2. Evidence value — Intake + Archivist-facing

A card scores well on Evidence value when:

- `kfr_fact_classes` covers the must-have / nice-to-have / risk-reduction / renewal proof inventories
- `provenance_requirements` specifies citation-type + verbatim-quote requirement per fact-class
- `evidence_signals` (CIC) names the structural artifacts the system should ask the applicant to produce
- `evidence_weights` (CLC) ranks which evidence buckets the reviewer weighs heaviest

A card with weak Evidence value produces grant drafts that read confident but cite nothing the reviewer cares about. The missing-evidence-interview quality is the Evidence value axis's direct test.

### 3. Drafting value — Scribe-facing

A card scores well on Drafting value when:

- `register_defaults` correctly identifies the dominant voice for the axis (formal / conversational / movement / hybrid)
- `dialect_routing_table` covers all four political-axis dialects (conservative / centrist / progressive / soul_fire) with example funders
- `admin_risk_term_register` flags the dialect-sensitive terms with severity tiers + substitution candidates
- `narrative_sections_typical` (CIC) + `narrative_section_patterns` (CLC) name the section ordering the reviewer expects

Drafting value is the axis most visible at first glance — most "the card works!" claims are Drafting value claims. Important but insufficient.

### 4. Review value — Judge + Red Team-facing

A card scores well on Review value when:

- `underwriting_criteria` (CLC) maps to the dimensions the funder's published rubric actually scores
- `scoring_weight_patterns` (CLC) captures the modal weight distribution (qualitative HIGH/MEDIUM/LOW until 12+ CycleReceipts per OQ-6)
- `common_red_flags` (CLC) includes the disqualifiers + the soft-flags + the post-submission discovery patterns
- `common_risk_register_entries` (CIC) covers the applicant-side risks Judge should surface for self-evaluation

Review value is the axis the Three-Arm Study most directly measures: do reviewer scores improve between Arm A (uncarded) and Arm B (carded)?

### 5. Compliance value — Logician-facing

A card scores well on Compliance value when:

- `compliance_burdens` (CIC) names the regulatory regimes the applicant operates under
- `compliance_obligations` (CLC) names the post-award compliance flow-downs the funder enforces
- `common_application_forms` (CLC) maps to the actual federal forms (SF-424 family, etc.)
- `provenance_requirements` keys to the fact-classes that trigger Logician's hard gates
- **Critical:** the card hands off live program law to a Program Rule Pack and does NOT embed it inline. CFR citations belong in PRPs; the *shape* of compliance lives in the card.

A card with weak Compliance value either silently embeds stale law (compounds across cycles) or shifts compliance burden to operator memory (drift across cycles).

### 6. Memory value — Archivist + Report Generator-facing

A card scores well on Memory value when:

- `commitment_tracking_pattern` (CLC) covers the post-award commitments Archivist must persist
- `reporting_requirements_typical` (CLC) names the cadence + the formal forms
- `reporting_cadence_typical` (CIC) names the cadence the applicant-side will face
- `metrics_table_template` (CIC) defines the metrics Report Generator pulls
- `kfr_fact_classes` (CIC) covers the renewal-evidence facts that compound across cycles

Memory value is the most-underweighted axis. Most cards in v0.1 Beta score 1–2 here. This is the axis that, once strong, makes Tilth compounding across grant cycles instead of starting from zero each cycle.

## Aggregate scoring

A "ready for LOCK" card scores ≥3 on Search + Evidence + Drafting + Review + Compliance, and ≥2 on Memory. The Memory tolerance reflects v0.1 Beta scope: Archivist v0.2-late and Report Generator v0.2-horizon mean Memory value is correctly under-built at v0.1.

A "Differentiating" card (any axis at 4) requires Three-Arm Study evidence or, pre-study, informal carded-vs-uncarded comparison documented at `pipeline/cards/eval/results/<scenario_slug>/`.

## How this rubric feeds the Three-Arm Study

The Three-Arm Study's primary outcome list (per `Cards_Prompts_and_Research_Plans_v2_fused.md` §8.3) maps onto the Six Forms:

| Three-Arm Study primary outcome | Six Forms axis |
|----------------------------------|-----------------|
| Rubric alignment (per CLC underwriting_criteria) | Review |
| Evidence sufficiency (per CLC evidence_weights) | Evidence |
| Reviewer confidence (Likert) | Drafting + Review |
| Red-flag reduction (count of card-flagged failure modes in draft) | Review + Compliance |
| Likelihood-of-funding score (Likert) | composite |
| Overall rank preference | composite |
| Missing-evidence interview quality | Evidence |
| Reduction in generic AI language | Drafting |

A scenario where Arm B (carded) outperforms Arm A (uncarded) on, say, Evidence sufficiency, validates the Evidence-value content of the CIC + CLC under test. Per-axis differential scoring across the four §10 scenarios is what makes the cards a publishable claim, not just an internal heuristic.

## Pre-LOCK score-check

Before any card-content re-sign ceremony fires, the operator (or dispatching agent) runs this rubric over the new body and records the 6-tuple in the ceremony handoff doc. A drop on any axis vs. the prior LOCK requires explicit justification (e.g. "Memory value dropped from 2 to 1 because we removed `commitment_tracking_pattern.deprecated_entries`; replacement lands in PRP `usda_rcdg_fy26.md` instead").

The 6-tuple lives alongside the new content_hash in the lock_history row so future audits can trace not only *what* changed but *why on each value axis*.
