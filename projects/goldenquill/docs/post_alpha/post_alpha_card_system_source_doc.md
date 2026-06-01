---
title: Post-Alpha Card System — Source Ideation Doc (Paul)
filed: 2026-05-15
operator: Josh Inklovich
status: SOURCE — preserved ideation material; not authoritative. Authoritative homes are the pending architecture amendment v7.0.11 (DRAFT) and blueprint §18 (DRAFT) — see below.
authoritative_homes:
  - pipeline/architecture/v0.1/architecture_v7_0_11_card_amendment.md  # DRAFT — pending L-005 two-cycle round
  - pipeline/blueprint/v0.1/section_18_card_system.md                  # DRAFT — pending L-005 two-cycle round
  - pipeline/blueprint/v0.1/section_00_5_section_18_card_amendment.md  # DRAFT — paired-commit row stubs
  - pipeline/cards/                                                              # directory scaffold + fixture stubs
note: This file is the verbatim ideation source preserved for reference and traceability. The proposed file path inside the doc body ("docs/post_alpha/card_system_report_and_process.md") was the author's suggestion; landed here under the same parent directory under a name that signals "source doc" rather than "authoritative spec." For the operational specs, read the DRAFT amendment + blueprint section linked above — they reconcile the ideation against the locked architecture (v7.0.10), the locked CIC/CLC orthogonality discipline (v7.0.8), the locked Logician F-CLASS family format, and the §0.5 interface index conventions.
operator_review_status: PENDING — DRAFT integration landed 2026-05-15; L-005 two-cycle audit not yet dispatched.
---

# Source ideation doc — verbatim text below

# Post-Alpha Report and Process: CIC × CLC Card System

Proposed file path: docs/post_alpha/card_system_report_and_process.mdStatus: Post-Alpha planning draftAudience: Platform engineering, product architecture, grant-writing workflow design, memory/runtime implementationScope: Customer Identity Cards (CICs), Capital Logic Cards (CLCs), card schema, research workflow, runtime integration, validation, and post-Alpha implementation sequence

## 1. Executive Summary

The post-Alpha objective is to convert Tilth’s Customer Identity Cards and Capital Logic Cards from visual/conceptual planning assets into runtime grant-writing intelligence.

The Alpha system establishes the broad product thesis: Tilth supports grant discovery, application decomposition, evidence organization, drafting, review, reporting, and institutional memory. The post-Alpha phase must make the system behave differently depending on the applicant’s funding world and the capital logic of the opportunity.

This requires a new structured layer:

The Card System

A Card is a signed, versioned, machine-readable knowledge artifact that translates a Card into executable behavior for Scout, Scribe, Judge, Logician, Archivist, Report Generator, and the model-routing layer.

The post-Alpha task is not to make the Cards more visually refined. The task is to make the Cards operational.

A correct implementation will allow Tilth to:

Search with the vocabulary of the applicant’s sector and operating reality.

Identify opportunity fit using applicant-side evidence patterns.

Classify the funding mechanism behind an opportunity.

Assemble the right evidence for each proposal section.

Draft in the appropriate register.

Flag unsupported claims, administrative-risk terms, and compliance issues.

Score proposal sections against likely reviewer logic.

Extract commitments for post-award reporting.

Preserve institutional memory without violating organizational isolation.

Improve over time through reviewed, privacy-preserving, non-identifying pattern learning.

## 2. Definitions

### 2.1 Golden Quill

The customer-owned local funding workstation or deployment environment where Tilth runs.

### 2.2 Tilth

The grant, proposal, evidence, reporting, and institutional-memory operating system running inside the Golden Quill environment.

### 2.3 Card

A visual or conceptual profile representing either a customer funding-world identity or a capital logic.

### 2.4 Card

The machine-readable runtime version of a Card. A card is structured YAML or JSON that contains vocabulary, evidence expectations, language register defaults, risk patterns, reviewer heuristics, reporting rhythms, validation metadata, and memory-routing instructions.

### 2.5 Customer Identity Card — CIC

Applicant-side knowledge. A CIC describes what kind of organization or operating world the applicant belongs to.

The post-Alpha CIC set is:

Card ID

Slug

Display Name

Coverage Axis

TILTH-CIC-01

food_systems

Food Systems

Production

TILTH-CIC-02

educator

Educator

Learning

TILTH-CIC-03

public_agency

Public Agency

Public Sector

TILTH-CIC-04

arts_culture

Arts & Culture

Culture

TILTH-CIC-05

cooperative

Cooperative

Member Ownership

TILTH-CIC-06

ecosystem_intermediary

Ecosystem Intermediary / Regenerative Systems Supplier

Intermediary Infrastructure

### 2.6 Capital Logic Card — CLC

Funder-side underwriting knowledge. A CLC describes why and how a funder moves money.

The post-Alpha CLC set is:

Card ID

Slug

Display Name

Funding Mechanism

TILTH-CLC-01

public_purpose_works

Public Purpose & Works

Mandate, eligibility, allowable use, civic benefit, public infrastructure

TILTH-CLC-02

catalytic_change

Catalytic Change

Demonstration, transition, innovation, systems change, leverage

TILTH-CLC-03

operating_capacity

Operating Capacity

Staff, systems, readiness, administration, delivery capacity

TILTH-CLC-04

research_evidence

Research & Evidence

Study design, learning agenda, evaluation, proof, validation

TILTH-CLC-05

market_access

Market Access

Buyers, customers, distribution, sales channels, commercialization, demand

TILTH-CLC-06

credit_underwriting

Credit & Underwriting

Repayment capacity, collateral, cash flow, financial controls, creditworthiness

TILTH-CLC-07

sponsorship_corporate

Sponsorship & Corporate Support

Brand alignment, audience, CSR, visibility, relationship value

TILTH-CLC-08

shared_assets

Shared Assets

Commons, cooperative infrastructure, pooled resources, community facilities

### 2.7 CIC × CLC Matrix

An advisory intersection layer describing how an applicant-side identity may approach a funder-side capital logic.

The matrix is observational only. It may store strategy, framing pivots, evidence substitutions, and historical pattern signals. It must not constrain eligibility.

## 3. Post-Alpha Problem Statement

The Alpha-stage card layer is useful as a strategy model, but it is not sufficient for production behavior until it becomes structured runtime knowledge.

The current gap can be summarized as follows:

Layer

Meaning

Alpha Status

Post-Alpha Requirement

Applicant-side knowledge

What a Food Systems applicant looks like versus an Educator or Public Agency

Conceptual / partially enumerated

CIC cards with vocabulary, evidence schema, KFR classes, register defaults, risks, reporting rhythms

Funder-side knowledge

How Public Purpose & Works money differs from Catalytic Change or Market Access money

Conceptual / partially enumerated

CLC cards with underwriting criteria, reviewer patterns, evidence weights, portal/form conventions, post-award commitments

Intersection knowledge

How a given applicant identity approaches a given capital logic

Mostly absent

Advisory CIC × CLC matrix with framing pivots and evidence substitution rules

Process knowledge

Section-by-section drafting, compliance gates, review, audit, reporting

Partially built / designed

Card-aware integration across Scout, Scribe, Judge, Logician, Archivist, Report Generator, and routing

Post-Alpha success means the system no longer treats every grant applicant and every funding opportunity as generic.

## 4. Product Principle

A good grant-writing system does not merely generate prose. It must know what an experienced grant writer knows implicitly:

Which search terms uncover the right opportunities.

Which search terms produce false positives.

What evidence reviewers trust.

What evidence is weak or stale.

What claims require documentation.

What language register fits the funder.

What terms may create administrative or political risk.

What sections carry the most scoring weight.

What budget lines require explanation.

What commitments must be tracked after award.

What must remain under human authority.

The Card System is the post-Alpha mechanism for encoding that grant-writing acumen.

## 5. Non-Goals

The post-Alpha Card System must not:

Replace human review.

Submit applications autonomously.

Guarantee awards.

Treat Card guidance as legal, financial, or compliance advice.

Hardcode which CICs may pursue which CLCs.

Store customer-specific private data inside workspace-shared cards.

Allow cross-organization memory retrieval.

Use unreviewed web research as production-trusted knowledge.

Promote unsigned cards into production runtime.

Flatten applicant voice into generic grant language.

## 6. Runtime Architecture

### 6.1 High-Level Flow

Customer / Project Intake        ↓CIC Selection or Inference        ↓Opportunity Intake / Discovery        ↓CLC Classification        ↓CIC Card + CLC Card + Matrix Context Loaded        ↓Grant Module Mapper        ↓Section-by-Section Drafting        ↓Judge Review + Logician Gates        ↓Human Approval        ↓Export / Submission Packet        ↓Award / Decline / Withdrawn Outcome        ↓Archivist + Commitments + Lessons + Optional Pattern Learning

### 6.2 Runtime Components

Component

Card Usage

Scout

Uses CIC search vocabulary, synonym maps, program keywords, disqualifiers, and CLC classification patterns.

Scribe

Uses evidence schema, register defaults, admin-risk terms, narrative patterns, and CIC × CLC framing pivots.

Judge

Uses CLC underwriting criteria, evidence weights, reviewer profiles, red flags, and scoring patterns.

Logician

Uses hard constraints, provenance requirements, compliance burdens, required forms, and export gates.

Archivist

Tags cycles by CIC/CLC, stores commitments, lessons, outcomes, and opt-in pattern signals.

Report Generator

Uses reporting cadence, metrics templates, and CLC commitment-tracking patterns.

Model Router

Uses section sensitivity, customer posture, task complexity, Card defaults, and authorization state.

## 7. Repository Structure

Recommended post-Alpha repository layout:

pipeline/  cards/    CIC/      food_systems.yaml      educator.yaml      public_agency.yaml      arts_culture.yaml      cooperative.yaml      ecosystem_intermediary.yaml    CLC/      public_purpose_works.yaml      catalytic_change.yaml      operating_capacity.yaml      research_evidence.yaml      market_access.yaml      credit_underwriting.yaml      sponsorship_corporate.yaml      shared_assets.yaml    matrix/      food_systems__market_access.yaml      food_systems__operating_capacity.yaml      ...  schemas/    card_cic.schema.json    card_clc.schema.json    card_matrix.schema.json  types/    identity_capital.py    card_models.py  validation/    card_thesis/    card_schema_checks/  memory/    profiles/      cards_cic_profile.yaml      cards_clc_profile.yaml      cards_matrix_profile.yaml  rubrics/    ...  funders/    ...  programs/    ...docs/  post_alpha/    card_system_report_and_process.md    card_research_dispatch_process.md    card_runtime_integration_plan.md

## 8. CIC Card Schema

Each CIC card should contain the following fields.

schema_version: "1.0-cic"card_axis: "CIC"card_id: "TILTH-CIC-NN"slug: "food_systems"display_name: "Food Systems"coverage_axis: "Production"nickname: "optional card tagline"tilth_cic_id: "TILTH-CIC-NN"search_vocabulary:  core_terms:    - term: "canonical term"      source_citation: "required before production signing"  synonym_map:    canonical_term:      - "synonym"  funder_program_keywords:    - keyword: "program keyword or code"      funder: "agency or funder"      source_citation: "required before production signing"  disqualifier_terms:    - term: "out-of-scope term"      reason: "why this flags mismatch"evidence_signals:  - kind: "evidence type"    source_pattern: "document, metric, report, ledger, quote, record, certification"    weight: "HIGH | MEDIUM | LOW"    freshness_tolerance_days: 365    source_citation: "required before production signing"kfr_fact_classes:  - fact_class: "fact key"    description: "what this fact means"    typical_provenance: "document type"provenance_requirements:  fact_class:    required_citation_type: "source type"    verbatim_quote_required: trueregister_defaults:  language_register: "formal | conversational | movement | hybrid"  narrative_voice: "first_person_plural | third_person | applicant_as_character"  tone: "technical_precise | movement_aligned | neutral_institutional | custom"  operator_override: "PROJECT_CONTEXT match_overrides take precedence"dialect_routing_table:  - funder_political_axis: "conservative | centrist | progressive | soul_fire"    dialect: "Scribe sub-mode"    example_funder: "optional"admin_risk_term_register:  - flagged_term: "term"    severity: "LOW | MEDIUM | HIGH"    substitution_candidates:      - "substitute phrase"    reviewer_context: "when this term is risky"    approval_required: truereporting_cadence_typical:  default_frequency: "quarterly | semi_annual | annual | project_based"  per_funder_overrides: {}metrics_table_template:  - metric: "name"    unit: "unit"    typical_target_range: "range or null"    source_for_target: "benchmark or null"narrative_sections_typical:  - "section name"capacity_signals_required:  - signal: "name"    evidence_type: "doc type"    required_for_competitive: truecompliance_burdens:  - framework: "framework name"    applicability: "when it applies"    required_filings:      - "filing or document"common_risk_register_entries:  - risk: "risk name"    likelihood: "LOW | MEDIUM | HIGH"    impact: "LOW | MEDIUM | HIGH"    mitigation_pattern: "standard mitigation"common_clc_patterns_observed:  - clc_slug: "operating_capacity"    frequency: "FREQUENT | OCCASIONAL | RARE | UNKNOWN"    win_rate_observed: "HIGH | MEDIUM | LOW | UNKNOWN"    note: "OBSERVATIONAL ONLY — does not bind eligibility"common_funders_observed:  - funder_name: "name"    funder_type: "federal | state | foundation | corporate | local"    typical_award_range: "$X - $Y or UNKNOWN"    note: "OBSERVATIONAL ONLY"_research_metadata:  authored_at: "ISO 8601"  authored_by_role: "research_session | internal_editor | platform_team"  research_budget_hours_actual: 0.0  priors_consulted:    - path: "file or URL"      extract_note: "one-line summary"  primary_sources:    - url: "URL"      access_date: "ISO 8601"      relevance: "what was extracted"  operator_review_status: "PENDING | PASSED | CHANGES_REQUESTED"  cross_family_thesis_status: "PENDING | PASSED | FAILED"  signature_status: "UNSIGNED | SIGNED | REVOKED"  ed25519_signature: null

## 9. CLC Card Schema

Each CLC card should contain the following fields.

schema_version: "1.0-clc"card_axis: "CLC"card_id: "TILTH-CLC-NN"slug: "public_purpose_works"display_name: "Public Purpose & Works"funding_mechanism_summary: "one-sentence summary"tilth_clc_id: "TILTH-CLC-NN"underwriting_criteria:  - criterion: "criterion name"    description: "what reviewers evaluate"    weight_in_typical_rubric: "percent, range, or qualitative"    source_citation: "required before production signing"scoring_weight_patterns:  - rubric_example: "NOFO or RFA name"    weights:      criterion: 25    source_citation: "required before production signing"evidence_weights:  evidence_kind:    weight: "HIGH | MEDIUM | LOW"    rationale: "why this evidence matters"common_application_forms:  - form_id: "form name or ID"    form_version: "version or UNKNOWN"    required_for: "program type"    source: "URL or internal source path"narrative_section_patterns:  - section_name: "section"    typical_word_count: "range or UNKNOWN"    source_citation: "required before production signing"budget_structure_conventions:  direct_cost_categories:    - "personnel"    - "fringe"    - "travel"    - "equipment"    - "supplies"    - "contractual"    - "other"  indirect_cost_treatment: "default guidance"  match_requirements_typical: "default guidance"  source_citation: "required before production signing"reviewer_profile_typical:  reviewer_types:    - "program officer"    - "peer reviewer"  reviewer_priorities:    - "what they read for first"  common_red_flags_from_reviewer_pov:    - "flag"common_portals:  - portal: "portal name"    typical_use: "which programs"common_red_flags:  - flag: "red flag"    severity: "LOW | MEDIUM | HIGH"    red_team_probe: "question Red Team should ask"reporting_requirements_typical:  performance_reporting:    frequency: "quarterly | semi_annual | annual | project_based"    content_required:      - "element"  financial_reporting:    frequency: "frequency"    content_required:      - "element"  final_report_required: truecompliance_obligations:  - framework: "framework name"    applicability: "when it applies"    typical_filings:      - "filing"commitment_tracking_pattern:  typical_commitments_extracted:    - commitment_type: "number_of_customers_acquired"      measurement_method: "how measured"  proposal_commitments_yaml_extension:    field_name: "type"_research_metadata:  authored_at: "ISO 8601"  authored_by_role: "research_session | internal_editor | platform_team"  research_budget_hours_actual: 0.0  priors_consulted:    - path: "file or URL"      extract_note: "one-line summary"  primary_sources:    - url: "URL"      access_date: "ISO 8601"      relevance: "what was extracted"  operator_review_status: "PENDING | PASSED | CHANGES_REQUESTED"  cross_family_thesis_status: "PENDING | PASSED | FAILED"  signature_status: "UNSIGNED | SIGNED | REVOKED"  ed25519_signature: null

## 10. CIC × CLC Matrix Schema

Matrix files are optional at first, but the schema should be established early so that outcome learning does not become ad hoc.

schema_version: "1.0-cic-clc-matrix"cic_slug: "food_systems"clc_slug: "market_access"intersection_id: "food_systems__market_access"historical_match_pattern:  frequency: "FREQUENT | OCCASIONAL | RARE | UNKNOWN"  win_rate_observed: "HIGH | MEDIUM | LOW | UNKNOWN"  confidence: "HIGH | MEDIUM | LOW"  sample_size: null  note: "OBSERVATIONAL ONLY — not eligibility binding"boundary_strategies:  - strategy: "how to make this intersection funder-legible"    when_to_use: "conditions"    evidence_needed:      - "evidence type"    risk: "what could go wrong"framing_pivots:  - from_applicant_language: "how applicant says it"    to_funder_language: "how funder needs to hear it"    rationale: "why this pivot works"evidence_substitution_rules:  - default_evidence_expected_by_clc: "buyer LOI"    cic_specific_substitute: "member purchase commitments"    allowed_when: "specific scenario"    review_required: truered_team_prompts:  - "What would make this framing look forced or opportunistic?"  - "Is the applicant using the capital logic authentically?"  - "What evidence would a skeptical reviewer demand?"review_status: "PENDING | PASSED | CHANGES_REQUESTED"

## 11. Starter CIC Content Requirements

The following field groups must be populated for all six CICs.

### 11.1 Food Systems — food_systems

Required starter content:

Search terms for farms, producers, value-added agriculture, food hubs, conservation, local/regional food, direct markets, and institutional procurement.

Program keywords for USDA, state agriculture, conservation, food access, energy, and local food programs.

Evidence signals such as sales ledgers, buyer letters, production records, crop plans, soil tests, conservation plans, food safety certifications, equipment quotes, business plans, and match documentation.

KFR classes for land tenure, acreage, crop/product categories, annual revenue, certifications, buyer relationships, equipment, production volume, and conservation practices.

Register defaults that are grounded, practical, evidence-forward, and capable of shifting between business, ecological, and community-benefit language.

Admin-risk terms such as food sovereignty, land back, climate justice, decolonize, and anti-capitalist, with context-sensitive substitutions.

Risk entries for weather variance, yield volatility, food safety, market concentration, undercapitalization, seasonality, equipment delays, and overclaiming regenerative impact.

### 11.2 Educator — educator

Required starter content:

Search terms for schools, afterschool, youth development, tutoring, mentoring, workforce readiness, CTE, college readiness, STEM/STEAM, social-emotional learning, family engagement, and evidence-based intervention.

Program keywords for education, youth, workforce, national service, and state/local education funding.

Evidence signals such as enrollment reports, attendance records, assessment data, curriculum, staff credentials, school agreements, evaluation plans, privacy protocols, and partner letters.

KFR classes for enrollment, grade bands, demographics, Title I status, FERPA relevance, curriculum, instructional hours, staff credentials, partner schools, evaluation design, and consent requirements.

Register defaults that are formal, student-centered, outcomes-oriented, and privacy-aware.

Admin-risk terms such as DEI, equity, trauma-informed, restorative justice, gender identity, culturally responsive, and related terms, with funder-sensitive substitutions.

Risk entries for FERPA exposure, unsupported achievement claims, weak evaluation design, low dosage, missing authorization, safeguarding gaps, and privacy risk in photos/testimonials.

### 11.3 Public Agency — public_agency

Required starter content:

Search terms for municipalities, boroughs, public works, infrastructure, water, wastewater, stormwater, parks, public safety, broadband, brownfields, community development, capital improvement, and hazard mitigation.

Program keywords for public works, CDBG, USDA community facilities, EPA, FEMA, DOT, EDA, state infrastructure, and local development programs.

Evidence signals such as board resolutions, capital plans, engineering estimates, feasibility studies, site control, procurement policy, match commitments, census data, maps, public meeting minutes, and environmental review status.

KFR classes for public entity type, UEI/SAM, authorized representative, board authorization, population, service area, capital plan reference, procurement threshold, engineering estimate, match source, and audit status.

Register defaults that are formal, public-benefit-centered, compliance-aware, and precise.

Admin-risk terms such as activist, abolition, anti-police, gentrification, environmental justice, racial justice, sanctuary, and anti-development, with civic substitutions.

Risk entries for missing authorization, procurement noncompliance, match weakness, unresolved site control, preliminary estimates, environmental review delay, public controversy, maintenance ambiguity, and audit exposure.

### 11.4 Arts & Culture — arts_culture

Required starter content:

Search terms for arts, culture, humanities, performance, exhibition, festival, public art, creative placemaking, placekeeping, cultural heritage, community arts, audience engagement, preservation, and accessibility.

Program keywords for federal arts/humanities, state arts councils, humanities councils, local arts grants, creative placemaking, and cultural foundation support.

Evidence signals such as work samples, artist statements, curatorial plans, venue agreements, audience data, prior programming, documentation plans, press coverage, partner letters, accessibility plans, and production budgets.

KFR classes for discipline, project history, artist credentials, audience, venue/site, confirmed dates, work samples, partner organizations, artist fees, production budget, accessibility, documentation, and rights/permissions.

Register defaults that preserve voice while translating artistic and cultural significance into funder-legible value.

Admin-risk terms such as radical, abolition, decolonial, liberation, resistance, queer, trans, racial justice, censorship, and occupation, with context-sensitive substitutions.

Risk entries for flattened voice, unsupported audience projections, underbudgeted artist fees, weak documentation, unconfirmed venue, rights ambiguity, diluted cultural specificity, accessibility gaps, and political-register mismatch.

### 11.5 Cooperative — cooperative

Required starter content:

Search terms for cooperative, worker-owned, producer-owned, consumer-owned, platform cooperative, multi-stakeholder, democratic governance, patronage, shared services, collective purchasing, employee ownership, and community wealth.

Program keywords for rural cooperative development, cooperative development, employee ownership, shared services, CDFIs, USDA rural business programs, and community wealth-building support.

Evidence signals such as bylaws, articles, member roster, signed commitments, governance minutes, board/steering committee roster, patronage model, financial projections, capitalization plan, shared asset plan, and technical assistance agreements.

KFR classes for cooperative type, legal status, member count, member classes, voting rights, bylaws, governance history, patronage model, capitalization, shared assets, member commitments, and financial controls.

Register defaults that translate democratic enterprise into funder-legible operational capacity and shared benefit.

Admin-risk terms such as anti-capitalist, solidarity economy, mutual aid, commons, worker control, collectivize, abolition, and wealth redistribution, with substitutions such as shared ownership, democratic enterprise, pooled infrastructure, and community wealth-building.

Risk entries for governance immaturity, informal member commitments, slow decision-making, legal-form mismatch, capitalization gaps, unclear patronage model, weak controls, member-class conflict, and underutilized shared assets.

### 11.6 Ecosystem Intermediary / Regenerative Systems Supplier — ecosystem_intermediary

Required starter content:

Search terms for intermediary, ecosystem builder, backbone organization, technical assistance, capacity builder, implementation partner, training provider, systems integrator, navigator, extension provider, adoption support, deployment partner, and regenerative systems supplier.

Program keywords for rural business, cooperative development, regional food business centers, EDA, SBIR/STTR, extension, technical assistance, workforce, innovation clusters, and capacity-building grants.

Evidence signals such as customer letters, partner commitments, prior deployments, case studies, technical specifications, implementation plans, training curriculum, support model, pricing model, staff credentials, and evaluation plan.

KFR classes for service type, customer segment, end-user benefit, technical capability, technology readiness, prior deployments, partner network, customer commitments, support model, pricing, adoption barriers, and downstream outcomes.

Register defaults that are credible, implementation-oriented, and careful not to sound like vendor hype.

Admin-risk terms such as disruption, platform dominance, surveillance, automation replacing workers, monopoly, proprietary lock-in, extractive scaling, and AI replacing staff, with substitutions around adoption support, workforce augmentation, interoperable tools, and customer-owned infrastructure.

Risk entries for private-vendor subsidy perception, unclear end-user benefit, overstated readiness, weak demand evidence, adoption friction, support burden, proprietary lock-in, data governance, weak maintenance, and insufficient training.

## 12. Starter CLC Content Requirements

The following field groups must be populated for all eight CLCs.

### 12.1 Public Purpose & Works — public_purpose_works

Required starter content:

Underwriting criteria for eligibility, public benefit, statutory/program purpose, allowable use, readiness, procurement, match, site control, maintenance, service-area need, and audit readiness.

Program terms for public works, infrastructure, CDBG, community facilities, water/wastewater, stormwater, transportation safety, brownfields, hazard mitigation, public safety, broadband, main street, distressed community, and environmental review.

Evidence weights for eligibility citation, board resolution, engineering estimate, capital plan, service-area data, census data, match commitment, site control, procurement policy, and maintenance plan.

Narrative sections for eligibility, need, public benefit, readiness, budget, match, procurement, environmental review, operations, maintenance, and timeline.

Reviewer profile centered on program officers, compliance reviewers, engineers, financial reviewers, and economic-development reviewers.

Red flags for vague eligibility, weak public benefit, uncommitted match, procurement silence, unresolved site control, missing planning citations, and unrealistic construction timelines.

Post-award commitments for construction milestones, procurement, match expenditures, beneficiary counts, facility improvements, jobs, compliance filings, and closeout.

### 12.2 Catalytic Change — catalytic_change

Required starter content:

Underwriting criteria for theory of change, systems leverage, novelty, transition plausibility, replication, field learning, partnership strength, measurement, follow-on capital, and timing.

Program terms for innovation, demonstration, pilot, proof of concept, systems change, transformation, climate-smart, accelerator, challenge grant, catalytic capital, field building, model replication, leverage, and social innovation.

Evidence weights for explicit theory of change, systems map, pilot results, partner commitments, learning agenda, replication pathway, leverage plan, baseline metrics, and evaluation partner.

Narrative sections for theory of change, systems context, intervention model, innovation, learning, partnerships, evaluation, dissemination, and scale.

Reviewer profile centered on foundation program officers, innovation reviewers, policy/systems-change reviewers, and subject matter experts.

Red flags for wishlist theory of change, no leverage point, unsupported innovation, no learning agenda, no replication path, role-less partnerships, and diffuse benefits.

Post-award commitments for pilot milestones, learning products, convenings, model refinements, dissemination, policy/market engagement, replication inquiries, and follow-on funding.

### 12.3 Operating Capacity — operating_capacity

Required starter content:

Underwriting criteria for capacity bottleneck, mission relationship, staffing/systems need, implementation plan, management readiness, governance, measurable capacity gain, sustainability, budget-to-task integrity, and dependency risk.

Program terms for capacity building, operating support, organizational effectiveness, technical assistance, planning, readiness, staffing, administrative capacity, systems improvement, governance, board development, strategic planning, and data systems.

Evidence weights for workload evidence, staffing plan, job descriptions, org chart, board approval, systems audit, strategic plan, backlog/demand, financial statements, and implementation timeline.

Narrative sections for organizational background, capacity need, proposed investment, staffing/systems plan, outcomes, sustainability, and budget justification.

Reviewer profile centered on foundation program officers, capacity reviewers, public agency program officers, and national service reviewers.

Red flags for vague operating support, no measurable capacity gain, new hire not tied to outcomes, systems purchase without adoption plan, no sustainability, hidden management weakness, and weak budget mapping.

Post-award commitments for staff hired, systems implemented, trainings completed, policies adopted, service capacity increased, turnaround time reduced, and data quality improved.

### 12.4 Research & Evidence — research_evidence

Required starter content:

Underwriting criteria for research question, significance, method fit, data collection, evaluation rigor, team qualifications, human subjects/IRB, data management, dissemination, broader impacts, and feasibility.

Program terms for research, evidence, evaluation, study, pilot study, applied research, participatory research, field trial, randomized controlled trial, quasi-experimental, mixed methods, data management, broader impacts, intellectual merit, IRB, human subjects, dissemination, SBIR, and STTR.

Evidence weights for aims, literature review, preliminary data, study protocol, evaluation design, data management, IRB plan, research partner letter, biosketches, dissemination plan, and methodology-linked budget.

Narrative sections for abstract, aims, significance, background, innovation, approach, evaluation, data management, human subjects, broader impacts, dissemination, and investigator qualifications.

Reviewer profile centered on peer reviewers, scientific reviewers, evaluators, program officers, and technical subject matter experts.

Red flags for vague questions, method mismatch, underbudgeted evaluation, ignored human subjects, missing data management, unrealistic sample size, overclaimed causality, vague dissemination, and team expertise gaps.

Post-award commitments for protocol completion, IRB milestones, participant recruitment, data collection, analysis, interim findings, reports, publications, presentations, and datasets.

### 12.5 Market Access — market_access

Required starter content:

Underwriting criteria for target market, verified demand, buyer commitment, channel strategy, revenue model, competitive position, delivery capacity, pricing logic, customer acquisition, unit economics, and risk mitigation.

Program terms for market access, commercialization, business development, export development, procurement readiness, buyer development, distribution, sales channel, marketing plan, trade promotion, product-market fit, go-to-market, e-commerce, retail readiness, wholesale readiness, and institutional procurement.

Evidence weights for buyer letters, purchase orders, sales history, customer pipeline, distributor agreements, market study, price sheet, production capacity proof, revenue projections, customer interviews, and channel partner letters.

Narrative sections for market opportunity, customer profile, sales strategy, distribution, competitive landscape, pricing, production capacity, projections, and risk.

Reviewer profile centered on business reviewers, lenders, economic-development reviewers, agriculture market specialists, and commercialization reviewers.

Red flags for no buyer commitment, market-size substitution, unsupported projections, unsolved distribution, ignored customer acquisition cost, insufficient production capacity, pricing below cost, and no competitive analysis.

Post-award commitments for buyers contacted, buyers converted, sales meetings, contracts, units sold, revenue, new markets, distributors, repeat purchases, acquisition cost, and margin.

### 12.6 Credit & Underwriting — credit_underwriting

Required starter content:

Underwriting criteria for repayment capacity, cash flow, debt service coverage, collateral, credit history, owner equity, management capacity, financial controls, use of funds, risk mitigation, guarantor strength, and covenant compliance.

Program terms for loan, credit, underwriting, working capital, term loan, microloan, loan guarantee, SBA 7(a), SBA 504, CDFI, revolving loan fund, debt service, collateral, guarantee, pro forma, balance sheet, income statement, debt schedule, covenant, and loan loss reserve.

Evidence weights for financial statements, tax returns, pro forma, cash flow projections, debt schedule, collateral documentation, credit explanation, purchase orders/contracts, owner equity injection, management resume, insurance, and use-of-funds budget.

Narrative sections for borrower profile, use of funds, repayment source, business history, management capacity, financial projections, collateral, risk mitigation, and community impact for mission lenders.

Reviewer profile centered on lenders, credit analysts, loan committees, CDFI underwriters, SBA lenders, and community development finance reviewers.

Red flags for weak cash flow, unsupported pro forma, no repayment source, poor controls, unclear collateral, missing owner equity, commingled finances, inconsistent tax returns, weak management, and hidden debt.

Post-award commitments for financial statements, covenant tracking, debt service, revenue targets, expense controls, collateral status, insurance, jobs, use-of-funds documentation, and annual financials.

### 12.7 Sponsorship & Corporate Support — sponsorship_corporate

Required starter content:

Underwriting criteria for audience fit, brand alignment, visibility value, community goodwill, activation plan, sponsor benefits, measurable reach, reputational safety, relationship pathway, and renewal potential.

Program terms for sponsorship, corporate giving, corporate foundation, CSR, ESG, community relations, employee engagement, brand partnership, cause marketing, in-kind sponsorship, event sponsorship, activation, audience reach, impressions, benefits package, sponsorship deck, and community investment.

Evidence weights for audience demographics, attendance history, sponsorship deck, media kit, prior sponsor outcomes, social/email reach, activation calendar, press coverage, brand alignment memo, benefits package, and sponsor testimonials.

Narrative sections for partnership opportunity, audience and reach, brand alignment, community value, sponsor benefits, activation, measurement, and renewal.

Reviewer profile centered on corporate giving officers, marketing managers, CSR managers, community relations officers, and corporate foundation staff.

Red flags for treating sponsorship like a grant, no sponsor benefit, audience mismatch, ignored brand risk, vague activation, no measurement, inflated impressions, and one-way ask without relationship strategy.

Post-award commitments for logo placements, social posts, impressions, attendance, sponsor mentions, employee engagement, VIP benefits, content assets, post-event reporting, and renewal meetings.

### 12.8 Shared Assets — shared_assets

Required starter content:

Underwriting criteria for shared need, user base, governance, access policy, utilization, maintenance, asset control, cost recovery, equitable access, replacement reserve, and community/member benefit.

Program terms for shared asset, shared infrastructure, commons, community facility, equipment library, tool library, shared-use kitchen, maker space, food hub, cooperative infrastructure, community land trust, pooled resource, collective ownership, public access, utilization, maintenance reserve, and asset management.

Evidence weights for user/member commitments, governance agreement, access policy, site control, equipment quote, utilization forecast, maintenance budget, scheduling policy, insurance, replacement reserve, shared-use agreement, and demand study.

Narrative sections for shared need, asset description, user base, governance, access/equity, operations, maintenance, budget, sustainability, and community/member benefit.

Reviewer profile centered on community development reviewers, cooperative development reviewers, facilities reviewers, foundation program officers, and public agency reviewers.

Red flags for one-party capture of shared asset, unclear governance, vague access rules, unfunded maintenance, assumed utilization, no scheduling/conflict process, unresolved site control, ignored replacement cost, and no insurance plan.

Post-award commitments for users served, utilization hours, bookings, maintenance logs, downtime, cost recovery, access equity, repairs, replacement reserve contributions, and community benefit outcomes.

## 13. Research Process for Card Population

### 13.1 Phase 1 — Prior-Art Absorption

Before external research, each card research session must inspect available internal prior art:

Type definitions for CIC and CLC slugs.

Existing card visuals and card language.

Existing grant-writing skills and prompts.

Existing rubric library.

Existing knowledge packs.

Existing funder or program databases.

Existing project-context templates.

Existing lessons or process notes.

Output:

_research_metadata:  priors_consulted:    - path: "path"      extract_note: "what was extracted"

### 13.2 Phase 2 — Primary Research

For CIC cards:

Review awarded grant abstracts or public award descriptions.

Review agency program pages.

Review foundation award descriptions or 990-PF grants where applicable.

Review state/local program pages where relevant.

Extract vocabulary, evidence patterns, capacity signals, compliance burdens, and reporting rhythms.

For CLC cards:

Review representative NOFOs, RFAs, FOAs, program guidelines, or lender/sponsor materials.

Extract underwriting criteria, scoring patterns, required sections, forms, reviewer logic, red flags, and post-award obligations.

### 13.3 Phase 3 — Draft Card

Populate the card using the relevant schema. Empty fields must not be hidden. Use explicit flags:

_note: "NEEDED — research or review"

### 13.4 Phase 4 — Self-Validation

Before review, each draft card must pass:

Schema completeness check.

Source/provenance completeness check.

No hardcoded CIC × CLC eligibility coupling.

No private customer data.

No unsourced numeric win-rate claims.

No unsupported program claims.

No excessive copied source text.

No production load if unsigned.

### 13.5 Phase 5 — Review Handback

Each card handback should include:

Card Research HandbackCard: <axis>:<slug>Card file: pipeline/cards/<axis>/<slug>.yamlResearch hours actual: <X.X>Schema completeness:  Required fields populated: <N>/<TOTAL>  Fields needing review: <N>  Total citations: <N>  Unique primary sources: <N>Decision queue:  - <decision>Conflicts with prior art:  - <conflict or NONE>Review readiness:  READY | DEFER_PENDING_CHANGES

## 14. Review, Signing, and Runtime Promotion

### 14.1 Lifecycle States

lifecycle:  draft_status: draft | reviewed | thesis_passed | signed | loaded | deprecated  operator_review_status: pending | passed | changes_requested  cross_family_thesis_status: pending | passed | failed  signature_status: unsigned | signed | revoked  runtime_load_status: not_loaded | loaded | disabled

### 14.2 Promotion Requirements

A card may be loaded into production only when:

It validates against schema.

It contains no private organization-specific data.

It has passed internal review.

It has passed adversarial review.

It has source citations for factual claims.

It has no unresolved coupling violations.

It has a valid signature.

### 14.3 Development vs. Production Loading

Development mode may load unsigned cards for testing.

Production mode must reject:

unsigned cards;

malformed cards;

cards with missing required fields;

cards marked changes_requested;

cards with revoked signatures;

cards containing private organization data;

cards that encode CIC × CLC eligibility subsets.

## 15. Memory Architecture

### 15.1 Namespace Layout

orgs:<org_slug>:kfrorgs:<org_slug>:cycle:<cycle_id>orgs:<org_slug>:lessonsorgs:<org_slug>:funder_intelorgs:<org_slug>:commitmentscards:cic:food_systemscards:cic:educatorcards:cic:public_agencycards:cic:arts_culturecards:cic:cooperativecards:cic:ecosystem_intermediarycards:clc:public_purpose_workscards:clc:catalytic_changecards:clc:operating_capacitycards:clc:research_evidencecards:clc:market_accesscards:clc:credit_underwritingcards:clc:sponsorship_corporatecards:clc:shared_assetscards:matrix:cic_x_clctilth:rubricstilth:funderstilth:programstilth:lessonstilth:formstilth:policytilth:vault

### 15.2 Cross-Organization Isolation Rule

A request made from orgs:<org_slug> may retrieve from:

orgs:<same_org_slug>:*

cards:cic:*

cards:clc:*

cards:matrix:cic_x_clc

tilth:rubrics

tilth:funders

tilth:programs

tilth:lessons

tilth:forms

tilth:policy

It may not retrieve from:

orgs:<different_org_slug>:*

Required fail-closed rule:

rule_id: "R-BRAIN-CROSS-ORG-DISCOVER-FORBIDDEN"condition:  retrieval_mode: "discover"  namespaces_contains_multiple_orgs: trueaction: "FAIL_CLOSED"message: "Cross-org memory discovery is forbidden. Use explicit namespace allow-list."

## 16. Loader Process

### 16.1 Loader Responsibilities

The card loader must:

Read YAML/JSON card.

Validate schema.

Verify lifecycle state.

Verify signature in production.

Reject malformed or unsigned production cards.

Load card into correct memory namespace.

Seed concept graph nodes and edges.

Register runtime defaults for Scout, Scribe, Judge, Logician, Archivist, Report Generator, and Model Router.

Record load event in audit log.

### 16.2 Loader Pseudocode

def load_card(path: str, environment: str):    card = read_yaml(path)    validate_schema(card)    if environment == "production":        require_operator_review_pass(card)        require_cross_family_review_pass(card)        require_signature(card)        verify_signature(card)        reject_private_org_data(card)        reject_cic_clc_coupling_violation(card)    namespace = resolve_card_namespace(card)    profile = build_memory_profile(card)    concept_graph = extract_concept_graph(card)    memory.set_profile(namespace, profile)    memory.seed(namespace, card)    memory.seed_concepts(namespace, concept_graph)    register_runtime_defaults(card)    audit_log.record("card_loaded", card_metadata(card))

## 17. Testing Requirements

Post-Alpha implementation should include automated tests for:

Schema validation:  - Missing required CIC field fails.  - Missing required CLC field fails.  - Unknown card slug fails.  - Invalid card_axis fails.Signing and lifecycle:  - Unsigned card fails production load.  - Revoked signature fails production load.  - Draft card can load only in development.Memory isolation:  - Cross-org retrieval fails closed.  - Card namespace cannot contain org-specific data.  - Matrix observations cannot retrieve private cycle records.Coupling discipline:  - CIC card cannot hardcode eligible CLC list.  - CLC card cannot hardcode eligible CIC list.  - Matrix files must label observations as non-binding.Runtime behavior:  - Scout expands vocabulary by active CIC.  - Scribe applies register defaults by active CIC.  - Judge uses CLC underwriting criteria.  - Logician blocks hard compliance failures.  - Report Generator extracts CLC-specific commitments.Safety and quality:  - Unsupported claims are surfaced.  - Admin-risk terms are flagged.  - Required evidence gaps are listed.  - Export is blocked when hard gates fail.

## 18. Post-Alpha Implementation Sequence

### 18.1 Phase A — Schema and Directory Foundation

Create repository directories.

Add CIC, CLC, and matrix schemas.

Add Pydantic models or equivalent typed models.

Add schema validation CLI.

Add fixture cards for one CIC and one CLC.

Recommended first fixtures:

food_systems.yaml

operating_capacity.yaml

### 18.2 Phase B — Runtime Context Injection

Add CardRuntimeContext object.

Load active CIC/CLC into workflow state.

Inject CIC context into Scout.

Inject CIC/CLC context into Scribe.

Inject CLC underwriting into Judge.

Inject compliance/provenance requirements into Logician.

Inject reporting rhythm into Report Generator.

### 18.3 Phase C — Memory Integration

Establish card namespaces.

Add retrieval wrapper with explicit namespace allow-list.

Disable unsafe default discovery across organization namespaces.

Seed concept graph nodes from card fields.

Store outcome signals only through approved, non-identifying pattern records.

### 18.4 Phase D — Research and Review Pipeline

Run formal research dispatch for first CIC.

Run formal research dispatch for first CLC.

Validate output shape.

Revise schema if required.

Run remaining CIC/CLC dispatches in waves.

Review, adversarially test, sign, and load cards.

### 18.5 Phase E — User Interface Exposure

Expose Card behavior in customer-visible terms:

Funding Profile.

Funding Logic.

Evidence Needed.

Language / Register Notes.

Risk Flags.

Missing Information.

Reporting Commitments.

Do not expose internal implementation terms unless the user is in an admin or engineering view.

## 19. Post-Alpha Milestones

### Milestone 1 — First Runtime Card Pair

Definition of done:

One CIC card validates.

One CLC card validates.

Both load in development.

Scout and Scribe behavior changes based on active card pair.

Recommended pair:

CIC: Food Systems.

CLC: Operating Capacity.

### Milestone 2 — First Signed Production Pair

Definition of done:

First CIC/CLC pair passes review.

First pair is signed.

Production loader accepts signed pair.

Production loader rejects unsigned pair.

Basic memory namespace tests pass.

### Milestone 3 — Full CIC Set

Definition of done:

All six CIC starter cards exist.

All six validate.

Scout can load search vocabulary for each.

Scribe can load register/evidence defaults for each.

### Milestone 4 — Full CLC Set

Definition of done:

All eight CLC starter cards exist.

All eight validate.

Judge can load underwriting criteria for each.

Report Generator can load commitment patterns for each.

### Milestone 5 — Matrix Layer

Definition of done:

Matrix schema exists.

At least five high-value CIC × CLC intersections are populated.

Observational/non-binding label is enforced.

Match DB can use matrix data as ranking signal but not eligibility gate.

### Milestone 6 — Outcome Learning Loop

Definition of done:

Cycle receipt includes CIC/CLC tags.

Award/decline outcomes can be stored.

Lessons can be extracted.

Opt-in, non-identifying pattern signal can be created.

Pattern signal review is required before shared library ingestion.

## 20. Engineering Handoff Summary

The Card System is the post-Alpha bridge between Tilth’s grant-writing strategy and its runtime behavior.

The critical implementation principle is this:

Cards should change system behavior, not merely appear in the interface.

A successful post-Alpha implementation will make the active CIC and CLC influence:

search vocabulary;

opportunity fit;

evidence assembly;

drafting register;

claim support checks;

reviewer simulation;

compliance warnings;

red-team questions;

reporting commitments;

memory tagging;

outcome learning.

The system must remain human-led, locally governed, source-aware, and organizationally isolated.

The immediate next action is to create the schema and directory foundation, then populate one CIC card and one CLC card as the first executable pair.