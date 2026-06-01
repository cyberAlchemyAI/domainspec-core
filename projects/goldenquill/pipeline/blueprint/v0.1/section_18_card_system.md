---
title: §18 v1 — Card System — Runtime schemas, lifecycle, research, integration
filed: 2026-05-15
operator: Josh Inklovich
status: DRAFT — LOCK-READY. Paired with architecture v7.0.11 (DRAFT). Pending L-005 strict two-cycle Thesis dispatch via openclaw bridge per AGENTS.md. Compound paired-commit at LOCK with architecture v7.0.11 + §4 v2.x.y F-CARDS-* + §0.5 v?? per §6.17 Option-B.
parent_locks:
  - pipeline/architecture/v0.1/tilth_architecture_locked.md                                          # v7 LOCKED 2026-04-19 A1-A12
  - pipeline/architecture/v0.1/architecture_v7_0_7_amendment.md                                     # v7.0.7 LOCKED 2026-05-10 row 180 — signed-asset publisher trust mechanism precedent
  - pipeline/architecture/v0.1/architecture_v7_0_8_amendment.md                                     # v7.0.8 LOCKED 2026-05-08 — F-CIC-CLC-COUPLING-VIOLATION; CIC + CLC slug rosters
  - pipeline/architecture/v0.1/architecture_v7_0_10_amendment.md                                    # v7.0.10 LOCKED 2026-05-11 row 215 — three-posture routing vocabulary
  - pipeline/blueprint/v0.1/section_02_v7_2_amendment.md                                            # §2 v7.2 LOCKED 2026-05-10 row 186 — SUB_KIND_REGISTRY pattern (card sub-kinds extend)
  - pipeline/blueprint/v0.1/section_04_v2_x_amendment.md                                            # §4 v2.x LOCKED 2026-05-10 rows 193/194 — F-CLASS-* family format pattern this section mirrors for F-CARDS-*
parent_amendment_paired_DRAFT: pipeline/architecture/v0.1/architecture_v7_0_11_card_amendment.md
companion_amendments_DRAFT:
  - pipeline/blueprint/v0.1/section_04_v2_x_y_cards_amendment.md
  - pipeline/blueprint/v0.1/section_00_5_section_18_card_amendment.md
authority: Operator directive 2026-05-15 ("with Beta locked, I want to integrate as much of this ideation as possible now"). Source ideation: docs/post_alpha/post_alpha_card_system_source_doc.md. This blueprint section is the operational specification for the card system; the architecture amendment v7.0.11 is the architectural primitive declaration.
section_18_rationale: Topical cluster — §15 Archivist (Tilth-internal between-cycle preservation), §16 Reflection Packet (Tilth-internal artifact), §17 WPFA (operator-and-buyer-facing accounting). §18 introduces a new boundary: workspace-shared knowledge that consumes from research artifacts but is operator-and-customer-shared (not per-org). Placing Cards/Cards at §18 after the cycle-close accounting cluster signals the audience boundary (shared knowledge across the operator's customer fleet).
---

# §18.0 — Purpose

The Card System is the post-v0.1-Beta bridge between Tilth's grant-writing strategy and its runtime behavior. It converts the visual Customer Identity Cards (CIC) and Capital Logic Cards (CLC) — currently planning assets at `assets/cards/customer_identification/` and `assets/cards/capital_logic/` — into signed, versioned, machine-readable artifacts consumed by Scout, Scribe, Judge, Logician, Archivist, Report Generator, and the model router at runtime.

**Critical implementation principle:** Cards change system behavior, not merely appear in the interface. A successful §18 implementation makes the active CIC + CLC influence search vocabulary, opportunity fit, evidence assembly, drafting register, claim support checks, reviewer simulation, compliance warnings, red-team questions, reporting commitments, memory tagging, and outcome learning.

The system remains human-led, locally governed, source-aware, and organizationally isolated per the Five Operating Laws.

# §18.1 — Definitions (binding)

| Term | Definition |
|------|------------|
| Card | Visual or conceptual profile (PNG, drawing, written description) of a customer funding-world identity (CIC) or a capital logic (CLC). Human-readable communication surface. |
| Card | Machine-readable runtime version of a Card. Signed, versioned YAML/JSON encoding vocabulary, evidence expectations, language register defaults, risk patterns, reviewer heuristics, reporting rhythms, validation metadata, and memory-routing instructions. |
| CIC | Customer Identity Card. Applicant-side. Six canonical entries per §18.2 below. |
| CLC | Capital Logic Card. Funder-side. Eight canonical entries per §18.3 below. |
| CIC × CLC Matrix | Advisory intersection layer. Observational only. Must not constrain eligibility per F-CARDS-COUPLING-VIOLATION (architecture v7.0.11 §1.6 + v7.0.8 F-CIC-CLC-COUPLING-VIOLATION). |
| Card Loader | The runtime component at `pipeline/cards/loader.py` that reads YAML cards from disk, validates schema, verifies lifecycle + signature, and registers runtime defaults with consuming seats. |
| Publisher Key | Operator-controlled Ed25519 signing key for cards. White-glove-pinned at appliance setup per architecture v7.0.11 §1.10 (mirrors v7.0.7 §6.1 router-template signing + §17 v1 §17.6 Coefficient Registry signing). |

# §18.2 — Customer Identity Card (CIC) roster (canonical)

Per architecture v7.0.8 LOCK + drawing TILTH-CIC-REVIEW-01 (2026-05-08). Six entries:

| Card ID | Slug | Display Name | Coverage Axis |
|---------|------|--------------|---------------|
| TILTH-CIC-01 | `food_systems` | Food Systems | Production |
| TILTH-CIC-02 | `educator` | Educator | Learning |
| TILTH-CIC-03 | `public_agency` | Public Agency | Public Sector |
| TILTH-CIC-04 | `arts_culture` | Arts & Culture | Culture |
| TILTH-CIC-05 | `cooperative` | Cooperative | Member Ownership |
| TILTH-CIC-06 | `ecosystem_intermediary` | Ecosystem Intermediary / Regenerative Systems Supplier | Intermediary Infrastructure |

**Display-name format at CIC-06 (architecture v7.0.11 §7.2 resolved 2026-05-15 PM).** The display name retains the slash form "Ecosystem Intermediary / Regenerative Systems Supplier". CIC card schema gains a new optional `display_name_short` field — set to "Ecosystem Intermediary" at CIC-06; absent or equal-to-display_name at the other five CICs. Downstream consumers that cannot safely render slashes (audit-log canonical-bytes formatting, future Match-DB grid display, terminal-pipeline-CLI table rendering) use `display_name_short`; consumers that can render the full form use `display_name`. Loader resolves `display_name_short` to `display_name` when the field is absent. Slug (`ecosystem_intermediary`) is unaffected and filesystem-safe.

# §18.3 — Capital Logic Card (CLC) roster (canonical)

Per drawing TILTH-CLC-00 (2026-05-08). Eight entries:

| Card ID | Slug | Display Name | Funding Mechanism Summary |
|---------|------|--------------|---------------------------|
| TILTH-CLC-01 | `public_purpose_works` | Public Purpose & Works | Mandate, eligibility, allowable use, civic benefit, public infrastructure |
| TILTH-CLC-02 | `catalytic_change` | Catalytic Change | Demonstration, transition, innovation, systems change, leverage |
| TILTH-CLC-03 | `operating_capacity` | Operating Capacity | Staff, systems, readiness, administration, delivery capacity |
| TILTH-CLC-04 | `research_evidence` | Research & Evidence | Study design, learning agenda, evaluation, proof, validation |
| TILTH-CLC-05 | `market_access` | Market Access | Buyers, customers, distribution, sales channels, commercialization, demand |
| TILTH-CLC-06 | `credit_underwriting` | Credit & Underwriting | Repayment capacity, collateral, cash flow, financial controls, creditworthiness |
| TILTH-CLC-07 | `sponsorship_corporate` | Sponsorship & Corporate Support | Brand alignment, audience, CSR, visibility, relationship value |
| TILTH-CLC-08 | `shared_assets` | Shared Assets | Commons, cooperative infrastructure, pooled resources, community facilities |

# §18.4 — Repository structure

```
pipeline/cards/
  README.md                                  # directory orientation + canonical homes pointer
  _schema/
    card_cic.schema.json           # JSON schema for CIC cards
    card_clc.schema.json           # JSON schema for CLC cards
  models.py                                  # Pydantic models mirroring each schema
  loader.py                                  # card loader (validation + signature + namespace + seat-default registration)
  validators.py                              # auxiliary self-validation checks (Phase 4 card-research-time gates)
  CIC/
    food_systems.yaml                        # fixture stub at v7.0.11 LOCK (content-incomplete)
    educator.yaml                            # NEEDED — Phase D research
    public_agency.yaml                       # NEEDED — Phase D research
    arts_culture.yaml                        # NEEDED — Phase D research
    cooperative.yaml                         # NEEDED — Phase D research
    ecosystem_intermediary.yaml              # NEEDED — Phase D research
  CLC/
    public_purpose_works.yaml                # NEEDED — Phase D research
    catalytic_change.yaml                    # NEEDED — Phase D research
    operating_capacity.yaml                  # fixture stub at v7.0.11 LOCK (content-incomplete)
    research_evidence.yaml                   # NEEDED — Phase D research
    market_access.yaml                       # NEEDED — Phase D research
    credit_underwriting.yaml                 # NEEDED — Phase D research
    sponsorship_corporate.yaml               # NEEDED — Phase D research
    shared_assets.yaml                       # NEEDED — Phase D research
  matrix/
    _FORWARD_COMPAT_ONLY.md                  # marker file — matrix content forbidden before v1.x
    _schema/
      card_matrix.schema.json                # forward-compat schema only
    # No populated matrix content before the v1.x matrix phase.
    # Future per-intersection files will use: <cic_slug>__<clc_slug>.yaml
  memory/
    profiles/
      cards_cic_profile.yaml                 # memory-layer CIC profile registration
      cards_clc_profile.yaml                 # memory-layer CLC profile registration
      cards_matrix_forward_compat_profile.yaml  # memory-layer matrix profile (inactive at v7.0.11)
```

Tests at `tests/cards/` mirror the directory layout. Validation artifacts at `pipeline/validation/cards/` (one subfolder per card for the L-005 Thesis Team audit trails when individual cards are signed).

# §18.5 — CIC Card Schema (full)

**Coupling-violation discipline (CIC).** CIC cards MUST NOT include `common_clc_patterns_observed` or any equivalent field that embeds CLC preference, frequency, win-rate, or recommended pairings inside the CIC itself. Observed CIC × CLC pattern knowledge belongs only in future Archivist lessons memory or forward-compatible matrix files (v1.x), never in CIC cards. F-CARDS-COUPLING-VIOLATION-EXTENSION fails closed at load time on any CIC card that violates this constraint.

```yaml
schema_version: "1.0-cic"
card_axis: "CIC"
card_id: "TILTH-CIC-NN"
slug: "food_systems"
display_name: "Food Systems"
coverage_axis: "Production"
nickname: "optional tagline or alternate framing"
tilth_cic_id: "TILTH-CIC-NN"

search_vocabulary:
  core_terms:
    - term: "canonical term"
      source_citation: "required before production signing"
  synonym_map:
    canonical_term:
      - "synonym"
  funder_program_keywords:
    - keyword: "program keyword or code"
      funder: "agency or funder"
      source_citation: "required before production signing"
  disqualifier_terms:
    - term: "out-of-scope term"
      reason: "why this flags mismatch"

evidence_signals:
  - kind: "evidence type"
    source_pattern: "document, metric, report, ledger, quote, record, certification"
    weight: "HIGH | MEDIUM | LOW"
    freshness_tolerance_days: 365
    source_citation: "required before production signing"

kfr_fact_classes:
  - fact_class: "fact key"
    description: "what this fact means"
    typical_provenance: "document type"

provenance_requirements:
  fact_class:
    required_citation_type: "source type"
    verbatim_quote_required: true

register_defaults:
  language_register: "formal | conversational | movement | hybrid"
  narrative_voice: "first_person_plural | third_person | applicant_as_character"
  tone: "technical_precise | movement_aligned | neutral_institutional | custom"
  operator_override: "PROJECT_CONTEXT match_overrides take precedence"

dialect_routing_table:
  - funder_political_axis: "conservative | centrist | progressive | soul_fire"
    dialect: "Scribe sub-mode"
    example_funder: "optional"

admin_risk_term_register:
  - flagged_term: "term"
    severity: "LOW | MEDIUM | HIGH"
    substitution_candidates:
      - "substitute phrase"
    reviewer_context: "when this term is risky"
    approval_required: true

reporting_cadence_typical:
  default_frequency: "quarterly | semi_annual | annual | project_based"
  per_funder_overrides: {}

metrics_table_template:
  - metric: "name"
    unit: "unit"
    typical_target_range: "range or null"
    source_for_target: "benchmark or null"

narrative_sections_typical:
  - "section name"

capacity_signals_required:
  - signal: "name"
    evidence_type: "doc type"
    required_for_competitive: true

compliance_burdens:
  - framework: "framework name"
    applicability: "when it applies"
    required_filings:
      - "filing or document"

common_risk_register_entries:
  - risk: "risk name"
    likelihood: "LOW | MEDIUM | HIGH"
    impact: "LOW | MEDIUM | HIGH"
    mitigation_pattern: "standard mitigation"

# `common_clc_patterns_observed` REMOVED at v7.0.11 LOCK per architecture
# v7.0.11 §6.1 resolved Option A (kill). CIC cards MUST NOT include this
# field or any equivalent. F-CARDS-COUPLING-VIOLATION-EXTENSION fails closed.

common_funders_observed:
  - funder_name: "name"
    funder_type: "federal | state | foundation | corporate | local"
    typical_award_range: "$X - $Y or UNKNOWN"
    note: "OBSERVATIONAL ONLY"

lifecycle:
  draft_status: "draft"
  review_status: "pending"
  cross_family_thesis_status: "pending"
  signature_status: "unsigned"
  runtime_load_status: "not_loaded"

_research_metadata:
  authored_at: "ISO 8601"
  authored_by_role: "research_session | internal_editor | platform_team"
  research_budget_hours_actual: 0.0
  priors_consulted:
    - path: "file or URL"
      extract_note: "one-line summary"
  primary_sources:
    - url: "URL"
      access_date: "ISO 8601"
      relevance: "what was extracted"
  ed25519_signature: null
```

# §18.6 — CLC Card Schema (full)

```yaml
schema_version: "1.0-clc"
card_axis: "CLC"
card_id: "TILTH-CLC-NN"
slug: "public_purpose_works"
display_name: "Public Purpose & Works"
funding_mechanism_summary: "one-sentence summary"
tilth_clc_id: "TILTH-CLC-NN"

underwriting_criteria:
  - criterion: "criterion name"
    description: "what reviewers evaluate"
    weight_in_typical_rubric: "percent, range, or qualitative"
    source_citation: "required before production signing"

scoring_weight_patterns:
  - rubric_example: "NOFO or RFA name"
    weights:
      criterion: 25
    source_citation: "required before production signing"

evidence_weights:
  evidence_kind:
    weight: "HIGH | MEDIUM | LOW"
    rationale: "why this evidence matters"

common_application_forms:
  - form_id: "form name or ID"
    form_version: "version or UNKNOWN"
    required_for: "program type"
    source: "URL or internal source path"

narrative_section_patterns:
  - section_name: "section"
    typical_word_count: "range or UNKNOWN"
    source_citation: "required before production signing"

budget_structure_conventions:
  direct_cost_categories:
    - "personnel"
    - "fringe"
    - "travel"
    - "equipment"
    - "supplies"
    - "contractual"
    - "other"
  indirect_cost_treatment: "default guidance"
  match_requirements_typical: "default guidance"
  source_citation: "required before production signing"

reviewer_profile_typical:
  reviewer_types:
    - "program officer"
    - "peer reviewer"
  reviewer_priorities:
    - "what they read for first"
  common_red_flags_from_reviewer_pov:
    - "flag"

common_portals:
  - portal: "portal name"
    typical_use: "which programs"

common_red_flags:
  - flag: "red flag"
    severity: "LOW | MEDIUM | HIGH"
    red_team_probe: "question Red Team should ask"

reporting_requirements_typical:
  performance_reporting:
    frequency: "quarterly | semi_annual | annual | project_based"
    content_required:
      - "element"
  financial_reporting:
    frequency: "frequency"
    content_required:
      - "element"
  final_report_required: true

compliance_obligations:
  - framework: "framework name"
    applicability: "when it applies"
    typical_filings:
      - "filing"

commitment_tracking_pattern:
  typical_commitments_extracted:
    - commitment_type: "number_of_customers_acquired"
      measurement_method: "how measured"
  proposal_commitments_yaml_extension:
    field_name: "type"

lifecycle:
  draft_status: "draft"
  review_status: "pending"
  cross_family_thesis_status: "pending"
  signature_status: "unsigned"
  runtime_load_status: "not_loaded"

_research_metadata:
  authored_at: "ISO 8601"
  authored_by_role: "research_session | internal_editor | platform_team"
  research_budget_hours_actual: 0.0
  priors_consulted:
    - path: "file or URL"
      extract_note: "one-line summary"
  primary_sources:
    - url: "URL"
      access_date: "ISO 8601"
      relevance: "what was extracted"
  ed25519_signature: null
```

# §18.7 — CIC × CLC Matrix Card Schema (FORWARD-COMPAT ONLY at v7.0.11 LOCK)

**Status at v7.0.11 LOCK.** Schema defined; **populated matrix content MUST NOT ship before the v1.x matrix phase**. `pipeline/cards/matrix/` directory contains exactly one explanatory file at LOCK (`_FORWARD_COMPAT_ONLY.md`) and the schema (`_schema/card_matrix.schema.json`). Loader fails closed via F-CARDS-COUPLING-VIOLATION-EXTENSION on any populated matrix card encountered before v1.x explicit amendment.

Matrix files are the most coupling-prone surface. They must be treated as advisory, retrospective, and non-binding. They must never participate in eligibility evaluation, opportunity exclusion, or ranking suppression. The `allowed_runtime_readers` / `forbidden_runtime_readers_during_eligibility` lists below are normative at v1.x activation.

```yaml
schema_version: "1.0-cic-clc-matrix"
status: "FORWARD_COMPAT_ONLY"                # MUST be present at v7.0.11 LOCK
card_axis: "MATRIX"
cic_slug: "food_systems"
clc_slug: "market_access"
intersection_id: "food_systems__market_access"

allowed_runtime_readers:
  - Archivist                                # retrospective lessons-memory consumer; v1.x activation

forbidden_runtime_readers_during_eligibility:
  - Scout
  - Scribe
  - Judge
  - Logician_as_evaluator

binding_eligibility: false                   # MUST be false; F-CARDS-COUPLING-VIOLATION-EXTENSION enforces

historical_match_pattern:
  frequency: "FREQUENT | OCCASIONAL | RARE | UNKNOWN"
  win_rate_observed: "HIGH | MEDIUM | LOW | UNKNOWN"
  confidence: "HIGH | MEDIUM | LOW"
  sample_size: null
  note: "OBSERVATIONAL ONLY — not eligibility binding"

boundary_strategies:
  - strategy: "how to make this intersection funder-legible"
    when_to_use: "conditions"
    evidence_needed:
      - "evidence type"
    risk: "what could go wrong"

framing_pivots:
  - from_applicant_language: "how applicant says it"
    to_funder_language: "how funder needs to hear it"
    rationale: "why this pivot works"

evidence_substitution_rules:
  - default_evidence_expected_by_clc: "buyer LOI"
    cic_specific_substitute: "member purchase commitments"
    allowed_when: "specific scenario"
    review_required: true

red_team_prompts:
  - "What would make this framing look forced or opportunistic?"
  - "Is the applicant using the capital logic authentically?"
  - "What evidence would a skeptical reviewer demand?"

lifecycle:
  draft_status: "draft"
  review_status: "pending"
  cross_family_thesis_status: "pending"
  signature_status: "unsigned"
  runtime_load_status: "not_loaded"
```

# §18.8 — Runtime component consumption (per-seat)

| Component | Card Usage |
|-----------|------------|
| Scout | Uses CIC.search_vocabulary, synonym_map, funder_program_keywords, disqualifier_terms; uses CLC classification patterns to tag opportunities by capital logic. |
| Scribe | Uses CIC.evidence_signals, register_defaults, dialect_routing_table, admin_risk_term_register; uses CLC.narrative_section_patterns; consults matrix.framing_pivots when active matrix loaded (v1.x). |
| Judge | Uses CLC.underwriting_criteria, scoring_weight_patterns, evidence_weights, reviewer_profile_typical, common_red_flags. |
| Logician | Uses CIC.compliance_burdens, provenance_requirements; uses CLC.common_application_forms, compliance_obligations; enforces F-CARDS-* family. |
| Archivist | Tags cycles by active CIC/CLC; stores commitments, lessons, outcomes; allowed runtime reader of matrix cards retrospectively when v1.x matrix phase activates. |
| Report Generator | Uses CIC.reporting_cadence_typical, metrics_table_template; uses CLC.reporting_requirements_typical, commitment_tracking_pattern. |
| Model Router | Uses card content as public/shareable input (architecture v7.0.11 §1.7); no per-card routing decision. |

# §18.9 — Starter content requirements (per-CIC)

Each CIC card MUST be populated with the following field-group content before production signing:

**TILTH-CIC-01 `food_systems`** — search terms (farms, producers, value-added agriculture, food hubs, conservation, local/regional food, direct markets, institutional procurement); program keywords (USDA, state agriculture, conservation, food access, energy, local food programs); evidence signals (sales ledgers, buyer letters, production records, crop plans, soil tests, conservation plans, food safety certifications, equipment quotes, business plans, match documentation); KFR classes (land tenure, acreage, crop/product categories, annual revenue, certifications, buyer relationships, equipment, production volume, conservation practices); register defaults (grounded, practical, evidence-forward, capable of shifting between business / ecological / community-benefit language); admin-risk terms (food sovereignty, land back, climate justice, decolonize, anti-capitalist with context-sensitive substitutions); risk entries (weather variance, yield volatility, food safety, market concentration, undercapitalization, seasonality, equipment delays, overclaiming regenerative impact).

**TILTH-CIC-02 `educator`** — search terms (schools, afterschool, youth development, tutoring, mentoring, workforce readiness, CTE, college readiness, STEM/STEAM, social-emotional learning, family engagement, evidence-based intervention); program keywords (education, youth, workforce, national service, state/local education funding); evidence signals (enrollment reports, attendance records, assessment data, curriculum, staff credentials, school agreements, evaluation plans, privacy protocols, partner letters); KFR classes (enrollment, grade bands, demographics, Title I status, FERPA relevance, curriculum, instructional hours, staff credentials, partner schools, evaluation design, consent requirements); register defaults (formal, student-centered, outcomes-oriented, privacy-aware); admin-risk terms (DEI, equity, trauma-informed, restorative justice, gender identity, culturally responsive, with funder-sensitive substitutions); risk entries (FERPA exposure, unsupported achievement claims, weak evaluation design, low dosage, missing authorization, safeguarding gaps, privacy risk in photos/testimonials).

**TILTH-CIC-03 `public_agency`** — search terms (municipalities, boroughs, public works, infrastructure, water, wastewater, stormwater, parks, public safety, broadband, brownfields, community development, capital improvement, hazard mitigation); program keywords (public works, CDBG, USDA community facilities, EPA, FEMA, DOT, EDA, state infrastructure, local development); evidence signals (board resolutions, capital plans, engineering estimates, feasibility studies, site control, procurement policy, match commitments, census data, maps, public meeting minutes, environmental review status); KFR classes (public entity type, UEI/SAM, authorized representative, board authorization, population, service area, capital plan reference, procurement threshold, engineering estimate, match source, audit status); register defaults (formal, public-benefit-centered, compliance-aware, precise); admin-risk terms (activist, abolition, anti-police, gentrification, environmental justice, racial justice, sanctuary, anti-development with civic substitutions); risk entries (missing authorization, procurement noncompliance, match weakness, unresolved site control, preliminary estimates, environmental review delay, public controversy, maintenance ambiguity, audit exposure).

**TILTH-CIC-04 `arts_culture`** — search terms (arts, culture, humanities, performance, exhibition, festival, public art, creative placemaking, placekeeping, cultural heritage, community arts, audience engagement, preservation, accessibility); program keywords (federal arts/humanities, state arts councils, humanities councils, local arts grants, creative placemaking, cultural foundation support); evidence signals (work samples, artist statements, curatorial plans, venue agreements, audience data, prior programming, documentation plans, press coverage, partner letters, accessibility plans, production budgets); KFR classes (discipline, project history, artist credentials, audience, venue/site, confirmed dates, work samples, partner organizations, artist fees, production budget, accessibility, documentation, rights/permissions); register defaults (preserve voice while translating artistic and cultural significance into funder-legible value); admin-risk terms (radical, abolition, decolonial, liberation, resistance, queer, trans, racial justice, censorship, occupation with context-sensitive substitutions); risk entries (flattened voice, unsupported audience projections, underbudgeted artist fees, weak documentation, unconfirmed venue, rights ambiguity, diluted cultural specificity, accessibility gaps, political-register mismatch).

**TILTH-CIC-05 `cooperative`** — search terms (cooperative, worker-owned, producer-owned, consumer-owned, platform cooperative, multi-stakeholder, democratic governance, patronage, shared services, collective purchasing, employee ownership, community wealth); program keywords (rural cooperative development, cooperative development, employee ownership, shared services, CDFIs, USDA rural business programs, community wealth-building); evidence signals (bylaws, articles, member roster, signed commitments, governance minutes, board/steering committee roster, patronage model, financial projections, capitalization plan, shared asset plan, technical assistance agreements); KFR classes (cooperative type, legal status, member count, member classes, voting rights, bylaws, governance history, patronage model, capitalization, shared assets, member commitments, financial controls); register defaults (translate democratic enterprise into funder-legible operational capacity and shared benefit); admin-risk terms (anti-capitalist, solidarity economy, mutual aid, commons, worker control, collectivize, abolition, wealth redistribution with substitutions: shared ownership, democratic enterprise, pooled infrastructure, community wealth-building); risk entries (governance immaturity, informal member commitments, slow decision-making, legal-form mismatch, capitalization gaps, unclear patronage model, weak controls, member-class conflict, underutilized shared assets).

**TILTH-CIC-06 `ecosystem_intermediary`** — search terms (intermediary, ecosystem builder, backbone organization, technical assistance, capacity builder, implementation partner, training provider, systems integrator, navigator, extension provider, adoption support, deployment partner, regenerative systems supplier); program keywords (rural business, cooperative development, regional food business centers, EDA, SBIR/STTR, extension, technical assistance, workforce, innovation clusters, capacity-building); evidence signals (customer letters, partner commitments, prior deployments, case studies, technical specifications, implementation plans, training curriculum, support model, pricing model, staff credentials, evaluation plan); KFR classes (service type, customer segment, end-user benefit, technical capability, technology readiness, prior deployments, partner network, customer commitments, support model, pricing, adoption barriers, downstream outcomes); register defaults (credible, implementation-oriented, careful not to sound like vendor hype); admin-risk terms (disruption, platform dominance, surveillance, automation replacing workers, monopoly, proprietary lock-in, extractive scaling, AI replacing staff with substitutions: adoption support, workforce augmentation, interoperable tools, customer-owned infrastructure); risk entries (private-vendor subsidy perception, unclear end-user benefit, overstated readiness, weak demand evidence, adoption friction, support burden, proprietary lock-in, data governance, weak maintenance, insufficient training).

# §18.10 — Starter content requirements (per-CLC)

Each CLC card MUST be populated with the following field-group content before production signing:

**TILTH-CLC-01 `public_purpose_works`** — underwriting criteria (eligibility, public benefit, statutory/program purpose, allowable use, readiness, procurement, match, site control, maintenance, service-area need, audit readiness); program terms (public works, infrastructure, CDBG, community facilities, water/wastewater, stormwater, transportation safety, brownfields, hazard mitigation, public safety, broadband, main street, distressed community, environmental review); evidence weights (eligibility citation, board resolution, engineering estimate, capital plan, service-area data, census data, match commitment, site control, procurement policy, maintenance plan); narrative sections (eligibility, need, public benefit, readiness, budget, match, procurement, environmental review, operations, maintenance, timeline); reviewer profile (program officers, compliance reviewers, engineers, financial reviewers, economic-development reviewers); red flags (vague eligibility, weak public benefit, uncommitted match, procurement silence, unresolved site control, missing planning citations, unrealistic construction timelines); post-award commitments (construction milestones, procurement, match expenditures, beneficiary counts, facility improvements, jobs, compliance filings, closeout).

**TILTH-CLC-02 `catalytic_change`** — underwriting criteria (theory of change, systems leverage, novelty, transition plausibility, replication, field learning, partnership strength, measurement, follow-on capital, timing); program terms (innovation, demonstration, pilot, proof of concept, systems change, transformation, climate-smart, accelerator, challenge grant, catalytic capital, field building, model replication, leverage, social innovation); evidence weights (explicit theory of change, systems map, pilot results, partner commitments, learning agenda, replication pathway, leverage plan, baseline metrics, evaluation partner); narrative sections (theory of change, systems context, intervention model, innovation, learning, partnerships, evaluation, dissemination, scale); reviewer profile (foundation program officers, innovation reviewers, policy/systems-change reviewers, subject matter experts); red flags (wishlist theory of change, no leverage point, unsupported innovation, no learning agenda, no replication path, role-less partnerships, diffuse benefits); post-award commitments (pilot milestones, learning products, convenings, model refinements, dissemination, policy/market engagement, replication inquiries, follow-on funding).

**TILTH-CLC-03 `operating_capacity`** — underwriting criteria (capacity bottleneck, mission relationship, staffing/systems need, implementation plan, management readiness, governance, measurable capacity gain, sustainability, budget-to-task integrity, dependency risk); program terms (capacity building, operating support, organizational effectiveness, technical assistance, planning, readiness, staffing, administrative capacity, systems improvement, governance, board development, strategic planning, data systems); evidence weights (workload evidence, staffing plan, job descriptions, org chart, board approval, systems audit, strategic plan, backlog/demand, financial statements, implementation timeline); narrative sections (organizational background, capacity need, proposed investment, staffing/systems plan, outcomes, sustainability, budget justification); reviewer profile (foundation program officers, capacity reviewers, public agency program officers, national service reviewers); red flags (vague operating support, no measurable capacity gain, new hire not tied to outcomes, systems purchase without adoption plan, no sustainability, hidden management weakness, weak budget mapping); post-award commitments (staff hired, systems implemented, trainings completed, policies adopted, service capacity increased, turnaround time reduced, data quality improved).

**TILTH-CLC-04 `research_evidence`** — underwriting criteria (research question, significance, method fit, data collection, evaluation rigor, team qualifications, human subjects/IRB, data management, dissemination, broader impacts, feasibility); program terms (research, evidence, evaluation, study, pilot study, applied research, participatory research, field trial, randomized controlled trial, quasi-experimental, mixed methods, data management, broader impacts, intellectual merit, IRB, human subjects, dissemination, SBIR, STTR); evidence weights (aims, literature review, preliminary data, study protocol, evaluation design, data management, IRB plan, research partner letter, biosketches, dissemination plan, methodology-linked budget); narrative sections (abstract, aims, significance, background, innovation, approach, evaluation, data management, human subjects, broader impacts, dissemination, investigator qualifications); reviewer profile (peer reviewers, scientific reviewers, evaluators, program officers, technical subject matter experts); red flags (vague questions, method mismatch, underbudgeted evaluation, ignored human subjects, missing data management, unrealistic sample size, overclaimed causality, vague dissemination, team expertise gaps); post-award commitments (protocol completion, IRB milestones, participant recruitment, data collection, analysis, interim findings, reports, publications, presentations, datasets).

**TILTH-CLC-05 `market_access`** — underwriting criteria (target market, verified demand, buyer commitment, channel strategy, revenue model, competitive position, delivery capacity, pricing logic, customer acquisition, unit economics, risk mitigation); program terms (market access, commercialization, business development, export development, procurement readiness, buyer development, distribution, sales channel, marketing plan, trade promotion, product-market fit, go-to-market, e-commerce, retail readiness, wholesale readiness, institutional procurement); evidence weights (buyer letters, purchase orders, sales history, customer pipeline, distributor agreements, market study, price sheet, production capacity proof, revenue projections, customer interviews, channel partner letters); narrative sections (market opportunity, customer profile, sales strategy, distribution, competitive landscape, pricing, production capacity, projections, risk); reviewer profile (business reviewers, lenders, economic-development reviewers, agriculture market specialists, commercialization reviewers); red flags (no buyer commitment, market-size substitution, unsupported projections, unsolved distribution, ignored customer acquisition cost, insufficient production capacity, pricing below cost, no competitive analysis); post-award commitments (buyers contacted, buyers converted, sales meetings, contracts, units sold, revenue, new markets, distributors, repeat purchases, acquisition cost, margin).

**TILTH-CLC-06 `credit_underwriting`** — underwriting criteria (repayment capacity, cash flow, debt service coverage, collateral, credit history, owner equity, management capacity, financial controls, use of funds, risk mitigation, guarantor strength, covenant compliance); program terms (loan, credit, underwriting, working capital, term loan, microloan, loan guarantee, SBA 7(a), SBA 504, CDFI, revolving loan fund, debt service, collateral, guarantee, pro forma, balance sheet, income statement, debt schedule, covenant, loan loss reserve); evidence weights (financial statements, tax returns, pro forma, cash flow projections, debt schedule, collateral documentation, credit explanation, purchase orders/contracts, owner equity injection, management resume, insurance, use-of-funds budget); narrative sections (borrower profile, use of funds, repayment source, business history, management capacity, financial projections, collateral, risk mitigation, community impact for mission lenders); reviewer profile (lenders, credit analysts, loan committees, CDFI underwriters, SBA lenders, community development finance reviewers); red flags (weak cash flow, unsupported pro forma, no repayment source, poor controls, unclear collateral, missing owner equity, commingled finances, inconsistent tax returns, weak management, hidden debt); post-award commitments (financial statements, covenant tracking, debt service, revenue targets, expense controls, collateral status, insurance, jobs, use-of-funds documentation, annual financials).

**TILTH-CLC-07 `sponsorship_corporate`** — underwriting criteria (audience fit, brand alignment, visibility value, community goodwill, activation plan, sponsor benefits, measurable reach, reputational safety, relationship pathway, renewal potential); program terms (sponsorship, corporate giving, corporate foundation, CSR, ESG, community relations, employee engagement, brand partnership, cause marketing, in-kind sponsorship, event sponsorship, activation, audience reach, impressions, benefits package, sponsorship deck, community investment); evidence weights (audience demographics, attendance history, sponsorship deck, media kit, prior sponsor outcomes, social/email reach, activation calendar, press coverage, brand alignment memo, benefits package, sponsor testimonials); narrative sections (partnership opportunity, audience and reach, brand alignment, community value, sponsor benefits, activation, measurement, renewal); reviewer profile (corporate giving officers, marketing managers, CSR managers, community relations officers, corporate foundation staff); red flags (treating sponsorship like a grant, no sponsor benefit, audience mismatch, ignored brand risk, vague activation, no measurement, inflated impressions, one-way ask without relationship strategy); post-award commitments (logo placements, social posts, impressions, attendance, sponsor mentions, employee engagement, VIP benefits, content assets, post-event reporting, renewal meetings).

**TILTH-CLC-08 `shared_assets`** — underwriting criteria (shared need, user base, governance, access policy, utilization, maintenance, asset control, cost recovery, equitable access, replacement reserve, community/member benefit); program terms (shared asset, shared infrastructure, commons, community facility, equipment library, tool library, shared-use kitchen, maker space, food hub, cooperative infrastructure, community land trust, pooled resource, collective ownership, public access, utilization, maintenance reserve, asset management); evidence weights (user/member commitments, governance agreement, access policy, site control, equipment quote, utilization forecast, maintenance budget, scheduling policy, insurance, replacement reserve, shared-use agreement, demand study); narrative sections (shared need, asset description, user base, governance, access/equity, operations, maintenance, budget, sustainability, community/member benefit); reviewer profile (community development reviewers, cooperative development reviewers, facilities reviewers, foundation program officers, public agency reviewers); red flags (one-party capture of shared asset, unclear governance, vague access rules, unfunded maintenance, assumed utilization, no scheduling/conflict process, unresolved site control, ignored replacement cost, no insurance plan); post-award commitments (users served, utilization hours, bookings, maintenance logs, downtime, cost recovery, access equity, repairs, replacement reserve contributions, community benefit outcomes).

# §18.11 — Research process for card population (Paul's skill home)

This is where Paul's research skill (or equivalent grant-finder/grant-writer extension) plugs in. The process is a five-phase pipeline:

**Phase 1 — Prior-Art Absorption.** Before external research, each card research session inspects available internal prior art: type definitions for CIC + CLC slugs, existing card visuals + language, existing grant-writing skills + prompts, existing rubric library, existing knowledge packs, existing funder + program databases, existing project-context templates, existing lessons + process notes. Output captured in card `_research_metadata.priors_consulted`.

**Phase 2 — Primary Research.** For CIC cards: review awarded grant abstracts or public award descriptions, agency program pages, foundation award descriptions or 990-PF grants where applicable, state/local program pages where relevant; extract vocabulary, evidence patterns, capacity signals, compliance burdens, reporting rhythms. For CLC cards: review representative NOFOs / RFAs / FOAs, program guidelines, lender/sponsor materials; extract underwriting criteria, scoring patterns, required sections, forms, reviewer logic, red flags, post-award obligations.

**Phase 3 — Draft Card.** Populate using the relevant schema. Empty fields are not hidden — use explicit `_note: "NEEDED — research or review"` markers.

**Phase 4 — Self-Validation.** Before review, each draft card must pass: schema completeness check, source/provenance completeness check, no hardcoded CIC × CLC eligibility coupling, no private customer data, no unsourced numeric win-rate claims, no unsupported program claims, no excessive copied source text, no production load if unsigned.

**Phase 5 — Review Handback.** Format:

```
Card Research Handback
Card: <axis>:<slug>
Card file: pipeline/cards/<axis>/<slug>.yaml
Research hours actual: <X.X>
Schema completeness:
  Required fields populated: <N>/<TOTAL>
  Fields needing review: <N>
  Total citations: <N>
  Unique primary sources: <N>
Decision queue:
  - <decision>
Conflicts with prior art:
  - <conflict or NONE>
Review readiness:
  READY | DEFER_PENDING_CHANGES
```

# §18.12 — Lifecycle and runtime promotion

A card promotes through these lifecycle states (architecture v7.0.11 §1.4):

```
draft → reviewed → thesis_passed → signed → loaded
                                         → deprecated (terminal)
```

Promotion requirements (production load):

- Validates against schema (`F-CARDS-SCHEMA-INVALID` if not).
- Contains no private organization-specific data (`F-CARDS-PRIVATE-DATA-IN-CARD` if not).
- Passed internal review (`review_status: passed`).
- Passed adversarial review (`cross_family_thesis_status: passed`).
- Source citations for factual claims (Phase 4 self-validation gate).
- No unresolved coupling violations (`F-CARDS-COUPLING-VIOLATION` if not).
- Valid Ed25519 signature against operator-pinned publisher pubkey (`F-CARDS-UNSIGNED-PRODUCTION-LOAD` + `F-CARDS-SIGNATURE-INVALID` if not).

Development mode (per architecture §1.5): MAY load unsigned cards for testing; production mode rejects.

# §18.13 — Memory namespace + Law 3 cross-org isolation

Per architecture v7.0.11 §1.9. Cards live in workspace-shared namespaces `cards:cic:*` and `cards:clc:*` (matrix `cards:matrix:*` forward-compat). A request from `orgs:<org_slug>:*` retrieval context MAY read cards namespaces; it MUST NOT read `orgs:<different_org_slug>:*`. Mixed-scope retrieval calls fail closed per `F-CARDS-CROSS-ORG-NAMESPACE-LEAK`.

Required fail-closed rule (mirrors architecture §1.9):

```yaml
rule_id: "R-BRAIN-CROSS-ORG-DISCOVER-FORBIDDEN"
condition:
  retrieval_mode: "discover"
  namespaces_contains_multiple_orgs: true
action: "FAIL_CLOSED"
message: "Cross-org memory discovery is forbidden. Use explicit namespace allow-list."
```

# §18.14 — Loader (responsibilities + pseudocode)

The card loader at `pipeline/cards/loader.py`:

```python
def load_card(path: str, environment: str) -> LoadedCard:
    card = read_yaml(path)
    validate_schema(card)                           # F-CARDS-SCHEMA-INVALID
    require_lifecycle_block(card)                   # F-CARDS-MALFORMED-LIFECYCLE
    reject_private_org_data(card)                   # F-CARDS-PRIVATE-DATA-IN-CARD
    reject_cic_clc_coupling_violation(card)         # F-CARDS-COUPLING-VIOLATION
    if environment == "production":
        require_operator_review_pass(card)
        require_cross_family_thesis_pass(card)
        require_signature(card)                     # F-CARDS-UNSIGNED-PRODUCTION-LOAD
        verify_signature(card)                      # F-CARDS-SIGNATURE-INVALID
    namespace = resolve_card_namespace(card)        # F-CARDS-LOAD-IN-WRONG-NAMESPACE
    profile = build_memory_profile(card)
    concept_graph = extract_concept_graph(card)
    memory.set_profile(namespace, profile)
    memory.seed(namespace, card)
    memory.seed_concepts(namespace, concept_graph)
    register_runtime_defaults(card)                 # routes to Scout, Scribe, Judge, etc.
    audit_log.record("card_loaded", card_metadata(card))
    return LoadedCard(namespace=namespace, profile=profile, ...)
```

# §18.15 — Testing requirements

```yaml
schema_validation:
  - Missing required CIC field fails.
  - Missing required CLC field fails.
  - Unknown card slug fails.
  - Invalid card_axis fails.

signing_and_lifecycle:
  - Unsigned card fails production load.
  - Revoked signature fails production load.
  - Draft card can load only in development.

memory_isolation:
  - Cross-org retrieval fails closed.
  - Card namespace cannot contain org-specific data.
  - Matrix observations cannot retrieve private cycle records.

coupling_discipline:
  - CIC card cannot contain common_clc_patterns_observed.
  - CIC card cannot contain CLC allowlists, deny-lists, ranking preferences, or win-rate fields.
  - CLC card cannot contain CIC allowlists, deny-lists, ranking preferences, or win-rate fields.
  - Matrix schema must label observations as non-binding and forward-compatible only.
  - Scout/Scribe/Judge cannot read matrix fields during eligibility or ranking.

runtime_behavior:
  - Scout expands vocabulary by active CIC.
  - Scribe applies register defaults by active CIC.
  - Judge uses CLC underwriting criteria.
  - Logician blocks hard compliance failures.
  - Report Generator extracts CLC-specific commitments.

safety_and_quality:
  - Unsupported claims are surfaced.
  - Admin-risk terms are flagged.
  - Required evidence gaps are listed.
  - Export is blocked when hard gates fail.
```

# §18.16 — Implementation phase sequence (binding version-arc mapping)

Per architecture v7.0.11 §5 binding split:

### §18.16.A — v0.1 Beta scope (lands at LOCK + immediately consumable)

- Create repository directories under `pipeline/cards/`.
- Add CIC, CLC, matrix JSON schemas at `pipeline/cards/_schema/`.
- Add Pydantic models or equivalent typed models at `pipeline/cards/models.py`.
- Add schema validation CLI (callable from `scripts/run_cards_validate.sh` or equivalent).
- Add fixture card stubs for `food_systems` (CIC) + `operating_capacity` (CLC) at v7.0.11 LOCK. Stubs are schema-valid but content-incomplete; every required content field carries `_note: "NEEDED — research or review"` markers awaiting Phase D research.
- F-CARDS-* family roster + module skeletons + NotImplementedError predicate bodies (graduates LIVE at v0.2 first wave).

### §18.16.B — v0.2 first wave scope (post-Beta)

- Add `CardRuntimeContext` object.
- Load active CIC/CLC into workflow state.
- Inject CIC context into Scout.
- Inject CIC/CLC context into Scribe.
- Inject CLC underwriting into Judge.
- Inject compliance/provenance requirements into Logician.
- Inject reporting rhythm into Report Generator.
- F-CARDS-* predicate bodies graduate NotImplementedError → LIVE.

### §18.16.C — v0.2 first wave scope (post-Beta, parallel with §18.16.B)

- Establish card namespaces in memory layer.
- Add retrieval wrapper with explicit namespace allow-list.
- Disable unsafe default discovery across organization namespaces.
- Seed concept graph nodes from card fields.
- Store outcome signals only through approved, non-identifying pattern records.

### §18.16.D — v0.2 ongoing (Paul-blocked)

- Run formal research dispatch for first CIC (recommended `food_systems`).
- Run formal research dispatch for first CLC (recommended `operating_capacity`).
- Validate output shape.
- Revise schema if required.
- Run remaining CIC/CLC dispatches in waves.
- Review, adversarially test, sign, and load cards into production.

### §18.16.E — v1.x scope (UI surface)

Expose Card behavior in customer-visible terms:

- Funding Profile.
- Funding Logic.
- Evidence Needed.
- Language / Register Notes.
- Risk Flags.
- Missing Information.
- Reporting Commitments.

Do not expose internal implementation terms unless the user is in an admin or engineering view.

# §18.17 — Milestones

**Milestone 1 — First Runtime Card Pair.** One CIC card validates; one CLC card validates; both load in development; Scout and Scribe behavior changes based on active card pair. Recommended pair: `food_systems` + `operating_capacity`. Lands in v0.2 first wave.

**Milestone 2 — First Signed Production Pair.** First CIC/CLC pair passes review; first pair is signed; production loader accepts signed pair; production loader rejects unsigned pair; basic memory namespace tests pass. Lands in v0.2 mid-wave.

**Milestone 3 — Full CIC Set.** All six CIC starter cards exist; all six validate; Scout can load search vocabulary for each; Scribe can load register/evidence defaults for each. Paul-blocked timeline.

**Milestone 4 — Full CLC Set.** All eight CLC starter cards exist; all eight validate; Judge can load underwriting criteria for each; Report Generator can load commitment patterns for each. Paul-blocked timeline.

**Milestone 5 — Matrix Layer.** Matrix schema exists (v7.0.11 LOCK closes); at least five high-value CIC × CLC intersections populated; observational/non-binding label enforced; Match DB can use matrix data as ranking signal but not eligibility gate. v1.x scope.

**Milestone 6 — Outcome Learning Loop.** Cycle receipt includes CIC/CLC tags; award/decline outcomes can be stored; lessons can be extracted; opt-in, non-identifying pattern signal can be created; pattern-signal review required before shared-library ingestion. v1.x scope; depends on §15 Archivist v1.x runtime implementation + Sovereign Node consent tiers (Stage 5 onward).

# §18.18 — Non-goals (binding)

The Card System MUST NOT:

- Replace human review.
- Submit applications autonomously.
- Guarantee awards.
- Treat Card guidance as legal, financial, or compliance advice.
- Hardcode which CICs may pursue which CLCs (F-CARDS-COUPLING-VIOLATION + F-CIC-CLC-COUPLING-VIOLATION).
- Store customer-specific private data inside workspace-shared cards (F-CARDS-PRIVATE-DATA-IN-CARD).
- Allow cross-organization memory retrieval (F-CARDS-CROSS-ORG-NAMESPACE-LEAK).
- Use unreviewed web research as production-trusted knowledge.
- Promote unsigned cards into production runtime (F-CARDS-UNSIGNED-PRODUCTION-LOAD).
- Flatten applicant voice into generic grant language.

# §18.19 — Card Effectiveness Test Harness — three-arm blind expert-reviewer study (operator directive 2026-05-15 PM)

**Operator framing (verbatim, 2026-05-15 PM):** "the idea of the crads and whether they work has to be tested. ... part of needing funding is to pay experts to survey different answers. One with Tilth, one with Tilth and the cards active, one with a different LLM that is highest rated at the time with rudimentary promting."

This section operationalizes that directive. **The core empirical test of whether cards deliver value is a three-arm blind expert-reviewer comparison, not an in-house automated eval.** In-house automated eval exists for build-time sanity (schema validation, AST-lint, gate-coverage smoke), but it is structurally insufficient to answer the cards-work question.

## §18.19.1 — Three-arm comparison design (the cards-work test)

For each test grant scenario, three drafts are produced and submitted to a paid expert-reviewer panel under blind evaluation:

| Arm | System | Purpose |
|-----|--------|---------|
| **A** | Tilth WITHOUT cards active | Baseline — controls for everything Tilth-specific except the card layer. The "did the cards add value, or did Tilth already do this without them?" question. |
| **B** | Tilth WITH cards active | Treatment — the card-driven Scout vocabulary + Scribe register defaults + Judge underwriting criteria + Logician compliance gates + Report Generator commitment patterns all live. |
| **C** | Highest-rated frontier LLM at study time, with rudimentary prompting | Industry-reference baseline — what someone using ChatGPT/Claude/Gemini with a basic "write me a grant for X" prompt would produce. |

**Blind evaluation.** Reviewers do not know which arm produced which draft. Drafts are anonymized for applicant identity, system identity, and any tell-tale formatting differences. Order of presentation is randomized per reviewer.

**Expert reviewer panel (paid).** Mix of grant reviewers (federal program officers, foundation program staff), grant writers (independent practitioners, agency contractors), and funder reps (foundation officers, agency review-committee experience). Multiple reviewers per draft for inter-rater reliability.

**Evaluation criteria.** Drawn from two sources: (a) the active CLC card's `underwriting_criteria` + `scoring_weight_patterns` + `common_red_flags` + `reviewer_profile_typical.reviewer_priorities` for the relevant funding mechanism, and (b) the locked funder rubric library at `pipeline/rubrics/` for any funder-specific scoring weights. Reviewers score on the same dimensions a real reviewer would; cards are tested against their own claimed targets, but **the scoring is done by humans, not by Judge** (avoids the circularity of using one Judge to evaluate drafts produced by another Judge).

**Outcome measures.** Per-dimension scores (mean, std, inter-rater κ); rank-order preference (which arm did each reviewer prefer for this scenario); free-text reviewer comments (qualitative signal); estimated likelihood-of-funding judgment.

**Sample size + statistical power.** TBD; depends on funding. The study itself is fundable work (§18.19.4).

## §18.19.2 — Test scenarios (synthetic + permission-based, NOT historical-replay)

Test scenarios are synthetic applicant + opportunity pairs, NOT replays of the operator's historical grants. Per operator directive 2026-05-15 PM, historical-replay against operator wins is **not the plan** — wrong target (single-applicant sample, survivor bias, private data leaking through a workspace-shared card surface, and the test would measure card mimicry of existing skill rather than card contribution to grant outcomes).

Scenario sources:

- **Synthetic scenarios authored at scenario-design time.** Each scenario specifies: (i) a fictional applicant with a CIC profile (e.g., "a 12-member worker cooperative growing specialty mushrooms in Pennsylvania"), (ii) a real opportunity (a public NOFO/RFA that was open during the study window or recently closed — public domain), (iii) a fictional applicant fact sheet (KFR-equivalent content the applicant would supply at intake). Synthetic applicants prevent confidential data leakage; real opportunities ensure the funder rubric is realistic.
- **Permission-based real applicants (optional, post-study-IRB-equivalent review).** Future-cycle real applicants (with explicit consent to use their grant work as eval material) could supplement the synthetic pool. Out of scope for v0.1 / v0.2 of the study; possible v1.x extension.

Test scenarios cover the six CIC × eight CLC matrix as broadly as practical given budget — at minimum one scenario per CIC and one per CLC, ideally multiple scenarios per high-volume intersection (food_systems × operating_capacity, food_systems × market_access, food_systems × catalytic_change being the most relevant to Josh's existing customer pipeline).

## §18.19.3 — In-house pre-checks (build-time sanity, NOT the cards-work test)

Before the expensive expert-reviewer study runs on a candidate card set, the in-house pre-checks must pass. These are deterministic, fast, free, and necessary-but-not-sufficient:

- **Schema validation** — every card validates against its `*_card.schema.json` (loader F-CARDS-SCHEMA-INVALID gate live).
- **AST-lint clean** — R-CARDS-NO-COUPLING-FIELD scan of all `pipeline/cards/CIC/**.yaml` + `pipeline/cards/CLC/**.yaml` returns zero findings.
- **Gate coverage complete** — F-CARDS-COVERAGE-INCOMPLETE META gate returns PASS at production-environment evaluation.
- **Fixture-stub round-trip** — fixture stubs at `pipeline/cards/CIC/food_systems.yaml` + `pipeline/cards/CLC/operating_capacity.yaml` load via `pipeline.cards.loader.load_card(environment='development')` without exception.
- **Signature verification** — every production-loaded card passes F-CARDS-SIGNATURE-INVALID against the operator-pinned Ed25519 publisher pubkey.
- **Per-seat dependency coverage** — every card field declared in `pipeline.cards.seat_dependencies.SEAT_CARD_FIELD_DEPENDENCIES` is present in every signed card that loads into production.

If any in-house pre-check fails, the card set is unfit for the expert-reviewer study. The pre-check failures must be fixed before the human-evaluation budget is spent.

## §18.19.4 — Funding pathway (the study itself is fundable work)

Per operator directive: paying expert reviewers requires funding. The expert-reviewer study is itself a grantable research project — Tilth applies for funding to evaluate Tilth.

**Probable CLC matches for the study's funding pitch:**

- `research_evidence` (TILTH-CLC-04) — formal evaluation study with defined methods, IRB-equivalent considerations, sample-size analysis, blinded peer review.
- `catalytic_change` (TILTH-CLC-02) — demonstration / proof-of-concept of a new approach (card-driven grant-writing intelligence) with theory of change + replication pathway.
- `market_access` (TILTH-CLC-05) — could fit if framed as commercialization-readiness evidence for the Golden Quill product line.

**Probable funder types:**

- Federal research grants (NSF, USDA SARE, USDA AFRI evaluation strands).
- Foundation-side innovation funds (e.g., MacArthur Foundation, Ford Foundation, Schmidt Futures, climate-tech foundations).
- Field-building intermediaries (community-development sector evaluation funders, philanthropy-research intermediaries).
- SBIR/STTR (Phase I research demonstration if framed as small-business-research evaluation).

Tilth's grant-finder skill should produce a funder shortlist for this study as one of its own dogfooded use cases. Tilth's grant-writer skill drafts the application. Meta — closes the loop.

## §18.19.5 — Harness directory scaffold

`pipeline/cards/eval/` directory landing at v7.0.11 LOCK alongside the cards/ runtime modules. Empty content at v0.1 Beta scope; populates incrementally as scenario design + funding land.

```
pipeline/cards/eval/
  README.md                                    # study orientation + arm definitions
  scenarios/
    _SCHEMA.md                                 # scenario authoring schema (applicant + opportunity + KFR seed)
    # one .yaml per synthetic scenario; populates as study scopes
  arms/
    arm_a_tilth_no_cards/
      README.md                                # baseline-arm execution recipe
    arm_b_tilth_with_cards/
      README.md                                # treatment-arm execution recipe
    arm_c_external_llm_rudimentary_prompt/
      README.md                                # industry-reference-arm execution recipe + frontier-LLM selection criteria
  reviewer_panel/
    README.md                                  # paid-reviewer recruitment + blind-eval protocol
    rubric_template.md                         # the eval rubric reviewers complete per draft
  results/
    # per-study results land here post-eval
  funding_pitch/
    README.md                                  # the funding application(s) for the study itself
```

## §18.19.6 — Definition of done (Milestone 7, v1.x scope)

The cards-work test is **Milestone 7** in the §18.17 milestone sequence, post-Milestone-6 outcome learning loop:

- §18.19.1 three-arm comparison study runs at least once with funded paid reviewer panel.
- Per-CIC × CLC intersection scenarios covered at minimum-one-each level.
- Inter-rater reliability acceptable (κ ≥ pre-registered threshold).
- Results published — public outcome write-up regardless of finding direction.
- If Arm B significantly outperforms Arm A on the pre-registered primary outcome measure with adequate statistical power, the cards-work hypothesis confirms; Tilth's customer-facing materials gain empirical backing.
- If Arm B ≈ Arm A, the cards add no measurable value over Tilth's baseline; card investment redirects (or pauses).
- If Arm B < Arm A, cards actively harm; card layer rolls back.

Pre-registration of hypothesis + primary outcome measure + statistical power calculation is a precondition of the study. No HARKing.

# §18.20 — Open questions surfaced for L-005 round

The morning-DRAFT decisions-pending (architecture v7.0.11 §6.1 / §6.2 / §6.3) and the afternoon operator-review decisions (architecture v7.0.11 §7.1 / §7.2 / §7.3) are all **resolved** and baked in. Single remaining open question for L-005 audit explicit review:

- v0.1 Beta scope honest-claim caveat — card files exist on disk + validate at LOCK + the empty test harness scaffold lands per §18.20, but no seat consumes cards at v0.1 Beta. Does this require an "honest schema-ready, runtime wiring v0.2" caveat in customer-facing docs, or is the existing v0.1 Beta posture (architecture v7.0.10 §1) sufficient framing?
