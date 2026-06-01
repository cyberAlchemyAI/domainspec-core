---
title: Post-Alpha Card System — Revised LOCK Candidate Source Doc (2026-05-15 PM)
filed: 2026-05-15
operator: Josh Inklovich
status: SOURCE — preserved revised ideation material. Supersedes the morning version at post_alpha_card_system_source_doc.md by incorporating Cowork-session feedback (kill `common_clc_patterns_observed`; matrix forward-compat only; F-CARDS-* + F-CIC-CLC-PATTERN-READ-DURING-ELIGIBILITY hardening; phase mapping to v0.1 Beta / v0.2 / v1.x; L-005 two-cycle audit plan; Move-now-on-Phase-A directive).
supersedes: docs/post_alpha/post_alpha_card_system_source_doc.md
authoritative_homes:
  - pipeline/architecture/v0.1/architecture_v7_0_11_card_amendment.md  # DRAFT — pending L-005 two-cycle round
  - pipeline/blueprint/v0.1/section_18_card_system.md                  # DRAFT — pending L-005 two-cycle round
  - pipeline/blueprint/v0.1/section_04_logician_v2_x_card_hardening.md           # DRAFT — F-CARDS-* + F-CIC-CLC-PATTERN-READ-DURING-ELIGIBILITY family
  - pipeline/blueprint/v0.1/section_00_5_section_18_card_amendment.md  # DRAFT — paired §0.5 row stubs
  - pipeline/cards/                                                              # directory scaffold + fixture stubs + README + memory/profiles
operator_review_status: PENDING — DRAFT integration landed 2026-05-15; L-005 two-cycle audit not yet dispatched.
---

# Source ideation doc (REVISED) — verbatim text below

Card System
Architecture Amendment + Blueprint Section LOCK Candidate
Proposed architecture amendment: pipeline/architecture/v0.1/
architecture_v7_0_11_card_amendment.md
Proposed blueprint section: pipeline/blueprint/v0.1/section_18_card_system.md
Proposed repository home: pipeline/cards/
Status:  Draft for L-005 two-cycle audit
Audience:  Platform engineering, product architecture, memory/runtime implementation, grant-writing
workflow design
Scope:  Customer Identity Cards (CICs), Capital Logic Cards (CLCs), card schemas, runtime loading,
memory integration, validation gates, and phased implementation
1. Executive Summary
The Card System is the runtime-machine-readable layer for Tilth’s Customer Identity Cards and
Capital Logic Cards.
The visual Card layer resolves how the product explains funding-world identities and funding mechanisms.
The unresolved architecture layer is how those Cards become executable system behavior . This document
proposes that bridge.
A Card  is a signed, versioned, schema-validated knowledge artifact that turns one Card into
runtime behavior for Scout, Scribe, Judge, Logician, Archivist, Report Generator , and the model-routing
layer .
The core product principle is:
Cards must change behavior , not merely appear in the interface.
A correct implementation allows Tilth to:
Search with applicant-specific vocabulary.
Interpret opportunities through funder-side capital logic.
Assemble the right evidence for each proposal section.
Draft in the appropriate register .
Flag unsupported claims and administrative-risk terms.
Score sections against likely reviewer logic.
Enforce hard constraints through Logician gates.
Extract post-award commitments.
Preserve organizational isolation.
Support future non-identifying, reviewed pattern learning.•

This is not a cosmetic product feature. It is a grant-writing intelligence substrate.
2. Architectural Framing
2.1 Problem
Tilth has a strong workflow thesis: discover , decompose, draft, review, capture, report, remember . However ,
for the system to become a more effective grant-writing workbench, it must distinguish between applicant
operating worlds and funder underwriting logics.
A Food Systems applicant does not search, evidence, draft, or report like a Public Agency. A Market Access
opportunity does not underwrite like a Public Purpose & Works opportunity. A Research & Evidence
proposal does not require the same proof as a Sponsorship & Corporate Support ask.
The Card System provides the structured runtime layer that lets the system know those
differences.
2.2 What this amendment closes
This amendment closes the Cards-vs-Cards reconciliation:
Cards  remain the visual and product-language layer .
Cards  become the runtime, schema-validated, machine-readable layer .
CIC cards  carry applicant-side knowledge.
CLC cards  carry funder-side underwriting knowledge.
Matrix files  are forward-compatible only in this lock candidate and must not ship populated runtime
content before the v1.x matrix phase.
3. Definitions
3.1 Card
A visual or conceptual profile representing either an applicant funding-world identity or a capital logic.
3.2 Card
A machine-readable runtime version of a Card. A card is structured YAML or JSON with schema
validation, lifecycle state, source metadata, review state, and signature state.
3.3 Customer Identity Card — CIC
Applicant-side knowledge. A CIC describes what kind of organization or operating world the applicant
belongs to.•

The CIC set is:
Card ID Slug Display Name Coverage Axis
TILTH-
CIC-01food_systems Food Systems Production
TILTH-
CIC-02educator Educator Learning
TILTH-
CIC-03public_agency Public Agency Public Sector
TILTH-
CIC-04arts_culture Arts & Culture Culture
TILTH-
CIC-05cooperative Cooperative Member Ownership
TILTH-
CIC-06ecosystem_intermediaryEcosystem Intermediary /
Regenerative Systems SupplierIntermediary
Infrastructure
3.4 Capital Logic Card — CLC
Funder-side underwriting knowledge. A CLC describes why and how money moves.
The CLC set is:
Card ID Slug Display Name Funding Mechanism
TILTH-
CLC-01public_purpose_worksPublic Purpose &
WorksMandate, eligibility, allowable use,
civic benefit, public infrastructure
TILTH-
CLC-02catalytic_change Catalytic ChangeDemonstration, transition,
innovation, systems change,
leverage
TILTH-
CLC-03operating_capacity Operating CapacityStaff, systems, readiness,
administration, delivery capacity
TILTH-
CLC-04research_evidenceResearch &
EvidenceStudy design, learning agenda,
evaluation, proof, validation
TILTH-
CLC-05market_access Market AccessBuyers, customers, distribution,
sales channels, commercialization,
demand
TILTH-
CLC-06credit_underwritingCredit &
UnderwritingRepayment capacity, collateral, cash
flow, financial controls,
creditworthiness

Card ID Slug Display Name Funding Mechanism
TILTH-
CLC-07sponsorship_corporateSponsorship &
Corporate SupportBrand alignment, audience, CSR,
visibility, relationship value
TILTH-
CLC-08shared_assets Shared AssetsCommons, cooperative
infrastructure, pooled resources,
community facilities
3.5 CIC × CLC Matrix
A forward-compatible advisory layer for future intersection strategy.
The matrix may eventually store observed strategies, framing pivots, and evidence-substitution patterns. It
must not be used for eligibility filtering, opportunity exclusion, ranking suppression, or runtime
discouragement of unusual CIC × CLC pairings.
For this lock candidate, matrix schema may be defined, but matrix content must not ship as active runtime
guidance before the v1.x matrix phase.
4. Non-Goals and Hard Boundaries
The Card System must not:
Replace human review.
Submit applications autonomously.
Guarantee awards.
Treat Card guidance as legal, financial, or compliance advice.
Encode which CICs may or may not pursue which CLCs.
Store customer-specific private data inside workspace-shared cards.
Allow cross-organization memory retrieval.
Use unreviewed research as production-trusted knowledge.
Promote unsigned cards into production runtime.
Flatten applicant voice into generic grant language.
Allow matrix observations to influence eligibility evaluation.
The highest-risk failure mode is hidden CIC × CLC coupling. The schema must avoid it, the loader must
reject it, and Logician must fail closed if runtime components attempt to use observational pattern data as
eligibility or opportunity-ranking logic.
5. Repository Structure
The Card System should live with runtime pipeline assets, not as a general documentation-only
post-Alpha file.•

Recommended repository layout:
pipeline/
  cards/
    CIC/
      food_systems.yaml
      educator.yaml
      public_agency.yaml
      arts_culture.yaml
      cooperative.yaml
      ecosystem_intermediary.yaml
    CLC/
      public_purpose_works.yaml
      catalytic_change.yaml
      operating_capacity.yaml
      research_evidence.yaml
      market_access.yaml
      credit_underwriting.yaml
      sponsorship_corporate.yaml
      shared_assets.yaml
    matrix/
      _FORWARD_COMPAT_ONLY.md
      _schema/
        card_matrix.schema.json
      # No populated matrix content before the v1.x matrix phase.
      # Future per-intersection files will use:
      # <cic_slug>__<clc_slug>.yaml
    _schema/
      card_cic.schema.json
      card_clc.schema.json
    models.py
    loader.py
    validators.py
    README.md
  programs/
    ...
  funders/
    ...
  rubrics/
    ...

  memory/
    profiles/
      cards_cic_profile.yaml
      cards_clc_profile.yaml
      cards_matrix_forward_compat_profile.yaml
  validation/
    card_thesis/
    card_schema_checks/
6. Runtime Architecture
6.1 High-Level Flow
Customer / Project Intake
        ↓
CIC Selection or Inference
        ↓
Opportunity Intake / Discovery
        ↓
CLC Classification
        ↓
CIC Card + CLC Card Loaded
        ↓
Grant Module Mapper
        ↓
Section-by-Section Drafting
        ↓
Judge Review + Logician Gates
        ↓
Human Approval
        ↓
Export / Submission Packet
        ↓
Award / Decline / Withdrawn Outcome
        ↓
Archivist + Commitments + Lessons
        ↓
Future reviewed, non-identifying pattern signal path

6.2 Runtime Component Mapping
Component Card Usage
ScoutUses CIC search vocabulary, synonym maps, program keywords, disqualifiers, and
CLC classification patterns.
ScribeUses CIC evidence schema, register defaults, admin-risk terms, CLC narrative
patterns, and CLC evidence weights.
JudgeUses CLC underwriting criteria, evidence weights, reviewer profiles, red flags, and
scoring patterns.
LogicianEnforces hard constraints, provenance requirements, compliance burdens, signature
state, schema validity, and anti-coupling gates.
ArchivistTags cycles by CIC/CLC, stores commitments, lessons, outcomes, and possible future
pattern signals.
Report
GeneratorUses CIC reporting rhythms, CIC metrics templates, and CLC commitment-tracking
patterns.
Model RouterUses section sensitivity, customer posture, task complexity, signed-card status,
and data-boundary rules.
6.3 Routing Compatibility
Signed cards are workspace-shared, public/shareable assets by construction. The loader must reject
private organization data in cards. Because signed cards contain no customer-private content,
they may be included in cloud-frontier scaffold calls under Split-Context Hybrid routing.
Per-organization context remains subject to customer data posture, data classification, authorization state,
and split-context rules. A card may travel with a scaffold call; restricted organization evidence may not.
This prevents conservative failure modes where future drafting agents refuse to use signed card
guidance during hybrid routing despite the card being non-private and approved for shared runtime
use.
7. CIC Card Schema
CIC cards carry applicant-side knowledge. They must not include common_clc_patterns_observed
or any equivalent field that embeds CLC preference, frequency, win-rate, or recommended pairings inside
the CIC itself.
Observed CIC × CLC pattern knowledge belongs only in future Archivist lessons or forward-compatible
matrix files, not in CIC cards.

schema_version :"1.0-cic"
card_axis :"CIC"
card_id:"TILTH-CIC-NN"
slug:"food_systems"
display_name :"FoodSystems"
coverage_axis :"Production"
nickname :"optional cardtagline"
tilth_cic_id :"TILTH-CIC-NN"
search_vocabulary :
core_terms :
-term:"canonical term"
source_citation :"required beforeproduction signing"
synonym_map :
canonical_term :
-"synonym"
funder_program_keywords :
-keyword:"program keyword orcode"
funder:"agency orfunder"
source_citation :"required beforeproduction signing"
disqualifier_terms :
-term:"out-of-scope term"
reason:"whythisflagsmismatch"
evidence_signals :
-kind:"evidence type"
source_pattern :"document, metric, report, ledger, quote,record,
certification"
weight:"HIGH|MEDIUM|LOW"
freshness_tolerance_days :365
source_citation :"required beforeproduction signing"
kfr_fact_classes :
-fact_class :"factkey"
description :"whatthisfactmeans"
typical_provenance :"document type"
provenance_requirements :
fact_class :
required_citation_type :"source type"
verbatim_quote_required :true
register_defaults :
language_register :"formal |conversational |movement |hybrid"
narrative_voice :"first_person_plural |third_person |applicant_as_character"
tone:"technical_precise |movement_aligned |neutral_institutional |custom"
operator_override :"PROJECT_CONTEXT match_overrides takeprecedence"

dialect_routing_table :
-funder_political_axis :"conservative |centrist |progressive |soul_fire"
dialect:"Scribe sub-mode"
example_funder :"optional"
admin_risk_term_register :
-flagged_term :"term"
severity :"LOW|MEDIUM|HIGH"
substitution_candidates :
-"substitute phrase"
reviewer_context :"whenthistermisrisky"
approval_required :true
reporting_cadence_typical :
default_frequency :"quarterly |semi_annual |annual|project_based"
per_funder_overrides :{}
metrics_table_template :
-metric:"name"
unit:"unit"
typical_target_range :"rangeornull"
source_for_target :"benchmark ornull"
narrative_sections_typical :
-"section name"
capacity_signals_required :
-signal:"name"
evidence_type :"doctype"
required_for_competitive :true
compliance_burdens :
-framework :"framework name"
applicability :"whenitapplies"
required_filings :
-"filing ordocument"
common_risk_register_entries :
-risk:"riskname"
likelihood :"LOW|MEDIUM|HIGH"
impact:"LOW|MEDIUM|HIGH"
mitigation_pattern :"standard mitigation"
common_funders_observed :
-funder_name :"name"
funder_type :"federal |state|foundation |corporate |local"
typical_award_range :"$X-$YorUNKNOWN"

note:"OBSERVATIONAL ONLY—noteligibility binding"
_research_metadata :
authored_at :"ISO8601"
authored_by_role :"research_session |internal_editor |platform_team"
research_budget_hours_actual :0.0
priors_consulted :
-path:"fileorURL"
extract_note :"one-line summary"
primary_sources :
-url:"URL"
access_date :"ISO8601"
relevance :"whatwasextracted"
review_status :"PENDING |PASSED|CHANGES_REQUESTED"
cross_family_thesis_status :"PENDING |PASSED|FAILED"
signature_status :"UNSIGNED |SIGNED|REVOKED"
ed25519_signature :null
8. CLC Card Schema
CLC cards carry funder-side underwriting knowledge. They must not include CIC eligibility subsets or
preferred CIC pairings.
schema_version :"1.0-clc"
card_axis :"CLC"
card_id:"TILTH-CLC-NN"
slug:"public_purpose_works"
display_name :"Public Purpose &Works"
funding_mechanism_summary :"one-sentence summary"
tilth_clc_id :"TILTH-CLC-NN"
underwriting_criteria :
-criterion :"criterion name"
description :"whatreviewers evaluate"
weight_in_typical_rubric :"percent, range,orqualitative"
source_citation :"required beforeproduction signing"
scoring_weight_patterns :
-rubric_example :"NOFOorRFAname"
weights:
criterion :25
source_citation :"required beforeproduction signing"
evidence_weights :

evidence_kind :
weight:"HIGH|MEDIUM|LOW"
rationale :"whythisevidence matters"
common_application_forms :
-form_id:"formnameorID"
form_version :"version orUNKNOWN"
required_for :"program type"
source:"URLorinternal sourcepath"
narrative_section_patterns :
-section_name :"section"
typical_word_count :"rangeorUNKNOWN"
source_citation :"required beforeproduction signing"
budget_structure_conventions :
direct_cost_categories :
-"personnel"
-"fringe"
-"travel"
-"equipment"
-"supplies"
-"contractual"
-"other"
indirect_cost_treatment :"default guidance"
match_requirements_typical :"default guidance"
source_citation :"required beforeproduction signing"
reviewer_profile_typical :
reviewer_types :
-"program officer"
-"peerreviewer"
reviewer_priorities :
-"whattheyreadforfirst"
common_red_flags_from_reviewer_pov :
-"flag"
common_portals :
-portal:"portal name"
typical_use :"whichprograms"
common_red_flags :
-flag:"redflag"
severity :"LOW|MEDIUM|HIGH"
red_team_probe :"question RedTeamshouldask"
reporting_requirements_typical :
performance_reporting :

frequency :"quarterly |semi_annual |annual|project_based"
content_required :
-"element"
financial_reporting :
frequency :"frequency"
content_required :
-"element"
final_report_required :true
compliance_obligations :
-framework :"framework name"
applicability :"whenitapplies"
typical_filings :
-"filing"
commitment_tracking_pattern :
typical_commitments_extracted :
-commitment_type :"number_of_customers_acquired"
measurement_method :"howmeasured"
proposal_commitments_yaml_extension :
field_name :"type"
_research_metadata :
authored_at :"ISO8601"
authored_by_role :"research_session |internal_editor |platform_team"
research_budget_hours_actual :0.0
priors_consulted :
-path:"fileorURL"
extract_note :"one-line summary"
primary_sources :
-url:"URL"
access_date :"ISO8601"
relevance :"whatwasextracted"
review_status :"PENDING |PASSED|CHANGES_REQUESTED"
cross_family_thesis_status :"PENDING |PASSED|FAILED"
signature_status :"UNSIGNED |SIGNED|REVOKED"
ed25519_signature :null
9. Matrix Schema — Forward-Compatible Only
Matrix schema may be defined now, but populated matrix content must not ship before the v1.x matrix
phase.
Matrix files are the most coupling-prone surface. They must be treated as advisory, retrospective, and non-
binding. They must never participate in eligibility evaluation.

Future matrix file path:
pipeline/cards/matrix/<cic_slug>__<clc_slug>.yaml
Future memory namespace:
cards:matrix:<intersection_id>
Forward-compatible schema:
schema_version :"1.0-cic-clc-matrix"
status:"FORWARD_COMPAT_ONLY"
cic_slug :"food_systems"
clc_slug :"market_access"
intersection_id :"food_systems__market_access"
allowed_runtime_readers :
-Archivist
forbidden_runtime_readers_during_eligibility :
-Scout
-Scribe
-Judge
-Logician_as_evaluator
historical_match_pattern :
frequency :"FREQUENT |OCCASIONAL |RARE|UNKNOWN"
win_rate_observed :"HIGH|MEDIUM|LOW|UNKNOWN"
confidence :"HIGH|MEDIUM|LOW"
sample_size :null
note:"OBSERVATIONAL ONLY—noteligibility binding; notopportunity-ranking
suppression"
boundary_strategies :
-strategy :"howtomakethisintersection funder-legible"
when_to_use :"conditions"
evidence_needed :
-"evidence type"
risk:"whatcouldgowrong"
framing_pivots :
-from_applicant_language :"howapplicant saysit"
to_funder_language :"howfunderneedstohearit"
rationale :"whythispivotworks"

evidence_substitution_rules :
-default_evidence_expected_by_clc :"buyerLOI"
cic_specific_substitute :"member purchase commitments"
allowed_when :"specific scenario"
review_required :true
red_team_prompts :
-"Whatwouldmakethisframing lookforcedoropportunistic?"
-"Istheapplicant usingthecapital logicauthentically?"
-"Whatevidence wouldaskeptical reviewer demand?"
review_status :"PENDING |PASSED|CHANGES_REQUESTED"
The matrix phase is deferred until v1.x. Before that phase, matrix directory content should be limited to
schema and forward-compat notes.
10. Memory Architecture
10.1 Namespace Layout
orgs:<org_slug>:kfr
orgs:<org_slug>:cycle:<cycle_id>
orgs:<org_slug>:lessons
orgs:<org_slug>:funder_intel
orgs:<org_slug>:commitments
cards:cic:food_systems
cards:cic:educator
cards:cic:public_agency
cards:cic:arts_culture
cards:cic:cooperative
cards:cic:ecosystem_intermediary
cards:clc:public_purpose_works
cards:clc:catalytic_change
cards:clc:operating_capacity
cards:clc:research_evidence
cards:clc:market_access
cards:clc:credit_underwriting
cards:clc:sponsorship_corporate
cards:clc:shared_assets
cards:matrix:<intersection_id>     # v1.x forward-compatible only

tilth:rubrics
tilth:funders
tilth:programs
tilth:lessons
tilth:forms
tilth:policy
tilth:vault
10.2 Cross-Organization Isolation Rule
A request made from orgs:<org_slug>  may retrieve from:
orgs:<same_org_slug>:*
cards:cic:*
cards:clc:*
tilth:rubrics
tilth:funders
tilth:programs
tilth:lessons
tilth:forms
tilth:policy
It may not retrieve from:
orgs:<different_org_slug>:*
Matrix namespaces remain inactive for Scout/Scribe/Judge eligibility use until the v1.x matrix phase and
must remain unavailable to opportunity-ranking suppression logic.
Required fail-closed rule:
rule_id:"R-BRAIN-CROSS-ORG-DISCOVER-FORBIDDEN"
condition :
retrieval_mode :"discover"
namespaces_contains_multiple_orgs :true
action:"FAIL_CLOSED"
message:"Cross-org memorydiscovery isforbidden. Useexplicit namespace allow-
list."
11. Logician Hardening: F-CARDS-* Gate Family
The Card System requires a dedicated Logician hardening family.•

11.1 F-CARDS-SCHEMA-INVALID
Fails closed when a card does not validate against the CIC, CLC, or matrix schema.
11.2 F-CARDS-UNSIGNED-PRODUCTION-LOAD
Fails closed when production runtime attempts to load an unsigned card.
11.3 F-CARDS-PRIVATE-DATA-IN-CARD
Fails closed when a card contains organization-specific private data, restricted customer data, named
private clients, private cycle IDs, or source text that belongs inside an organization namespace.
11.4 F-CARDS-CROSS-ORG-NAMESPACE-LEAK
Fails closed when card retrieval returns or requests memory from another organization namespace.
11.5 F-CARDS-COUPLING-VIOLATION-EXTENSION
Fails closed when a CIC card includes CLC allowlists, deny-lists, ranking preferences, win-rate fields, or
fields that imply one CIC should or should not pursue one or more CLCs.
Fails closed when a CLC card includes CIC allowlists, deny-lists, ranking preferences, or fields that imply
one CLC is restricted to one or more CICs.
11.6 F-CIC-CLC-PATTERN-READ-DURING-ELIGIBILITY
Fails closed when Scout, Scribe, Judge, or eligibility-evaluation code attempts to read matrix or historical
pattern fields during opportunity eligibility, fit gating, opportunity exclusion, or ranking suppression.
Allowed reader during v1.x matrix phase:
Archivist, retrospectively.
Possible future reader after explicit amendment:
Match DB advisory layer , if and only if the result is labeled as a non-binding suggestion and cannot
suppress or exclude opportunities.
11.7 F-CARDS-COVERAGE-INCOMPLETE
Warns or fails depending on mode when a card is active but required card coverage is incomplete.
Development mode:
WARN.•

Production mode:
FAIL if a required runtime component depends on the missing field.
WARN if the missing field is nonessential or explicitly marked forward-compatible.
12. Loader Process
12.1 Loader Responsibilities
The card loader must:
Read YAML/JSON card.
Validate schema.
Verify lifecycle state.
Verify signature in production.
Reject malformed or unsigned production cards.
Reject cards containing private organization data.
Reject CIC/CLC coupling fields.
Load card into correct memory namespace.
Seed concept graph nodes and edges where allowed.
Register runtime defaults for Scout, Scribe, Judge, Logician, Archivist, Report Generator , and Model
Router .
Record load event in audit log.
12.2 Loader Pseudocode
defload_card (path:str,environment :str):
card =read_yaml (path)
validate_schema (card )
reject_coupling_fields (card )
reject_private_org_data (card )
ifenvironment =="production" :
require_review_pass (card )
require_cross_family_review_pass (card )
require_signature (card )
verify_signature (card )
namespace =resolve_card_namespace (card )
profile =build_memory_profile (card )
concept_graph =extract_allowed_concept_graph (card )
memory.set_profile (namespace ,profile)
memory.seed(namespace ,card )
memory.seed_concepts (namespace ,concept_graph )•

register_runtime_defaults (card )
audit_log .record("card_loaded" ,card_metadata (card ))
13. Starter CIC Content Requirements
The following field groups must be populated for all six CIC cards.
13.1 Food Systems — food_systems
Required starter content:
Search terms for farms, producers, value-added agriculture, food hubs, conservation, local/regional
food, direct markets, and institutional procurement.
Program keywords for USDA, state agriculture, conservation, food access, energy, and local food
programs.
Evidence signals such as sales ledgers, buyer letters, production records, crop plans, soil tests,
conservation plans, food safety certifications, equipment quotes, business plans, and match
documentation.
KFR classes for land tenure, acreage, crop/product categories, annual revenue, certifications, buyer
relationships, equipment, production volume, and conservation practices.
Register defaults that are grounded, practical, evidence-forward, and capable of shifting between
business, ecological, and community-benefit language.
Admin-risk terms such as food sovereignty, land back, climate justice, decolonize, and anti-capitalist,
with context-sensitive substitutions.
Risk entries for weather variance, yield volatility, food safety, market concentration,
undercapitalization, seasonality, equipment delays, and overclaiming regenerative impact.
13.2 Educator — educator
Required starter content:
Search terms for schools, afterschool, youth development, tutoring, mentoring, workforce readiness,
CTE, college readiness, STEM/STEAM, social-emotional learning, family engagement, and evidence-
based intervention.
Program keywords for education, youth, workforce, national service, and state/local education
funding.
Evidence signals such as enrollment reports, attendance records, assessment data, curriculum, staff
credentials, school agreements, evaluation plans, privacy protocols, and partner letters.
KFR classes for enrollment, grade bands, demographics, Title I status, FERPA relevance, curriculum,
instructional hours, staff credentials, partner schools, evaluation design, and consent requirements.
Register defaults that are formal, student-centered, outcomes-oriented, and privacy-aware.
Admin-risk terms such as DEI, equity, trauma-informed, restorative justice, gender identity, culturally
responsive, and related terms, with funder-sensitive substitutions.•

Risk entries for FERPA exposure, unsupported achievement claims, weak evaluation design, low
dosage, missing authorization, safeguarding gaps, and privacy risk in photos/testimonials.
13.3 Public Agency — public_agency
Required starter content:
Search terms for municipalities, boroughs, public works, infrastructure, water , wastewater ,
stormwater , parks, public safety, broadband, brownfields, community development, capital
improvement, and hazard mitigation.
Program keywords for public works, CDBG, USDA community facilities, EPA, FEMA, DOT, EDA, state
infrastructure, and local development programs.
Evidence signals such as board resolutions, capital plans, engineering estimates, feasibility studies,
site control, procurement policy, match commitments, census data, maps, public meeting minutes,
and environmental review status.
KFR classes for public entity type, UEI/SAM, authorized representative, board authorization,
population, service area, capital plan reference, procurement threshold, engineering estimate,
match source, and audit status.
Register defaults that are formal, public-benefit-centered, compliance-aware, and precise.
Admin-risk terms such as activist, abolition, anti-police, gentrification, environmental justice, racial
justice, sanctuary, and anti-development, with civic substitutions.
Risk entries for missing authorization, procurement noncompliance, match weakness, unresolved
site control, preliminary estimates, environmental review delay, public controversy, maintenance
ambiguity, and audit exposure.
13.4 Arts & Culture — arts_culture
Required starter content:
Search terms for arts, culture, humanities, performance, exhibition, festival, public art, creative
placemaking, placekeeping, cultural heritage, community arts, audience engagement, preservation,
and accessibility.
Program keywords for federal arts/humanities, state arts councils, humanities councils, local arts
grants, creative placemaking, and cultural foundation support.
Evidence signals such as work samples, artist statements, curatorial plans, venue agreements,
audience data, prior programming, documentation plans, press coverage, partner letters,
accessibility plans, and production budgets.
KFR classes for discipline, project history, artist credentials, audience, venue/site, confirmed dates,
work samples, partner organizations, artist fees, production budget, accessibility, documentation,
and rights/permissions.
Register defaults that preserve voice while translating artistic and cultural significance into funder-
legible value.
Admin-risk terms such as radical, abolition, decolonial, liberation, resistance, queer , trans, racial
justice, censorship, and occupation, with context-sensitive substitutions.
Risk entries for flattened voice, unsupported audience projections, underbudgeted artist fees, weak
documentation, unconfirmed venue, rights ambiguity, diluted cultural specificity, accessibility gaps,
and political-register mismatch.•

13.5 Cooperative — cooperative
Required starter content:
Search terms for cooperative, worker-owned, producer-owned, consumer-owned, platform
cooperative, multi-stakeholder , democratic governance, patronage, shared services, collective
purchasing, employee ownership, and community wealth.
Program keywords for rural cooperative development, cooperative development, employee
ownership, shared services, CDFIs, USDA rural business programs, and community wealth-building
support.
Evidence signals such as bylaws, articles, member roster , signed commitments, governance minutes,
board/steering committee roster , patronage model, financial projections, capitalization plan, shared
asset plan, and technical assistance agreements.
KFR classes for cooperative type, legal status, member count, member classes, voting rights, bylaws,
governance history, patronage model, capitalization, shared assets, member commitments, and
financial controls.
Register defaults that translate democratic enterprise into funder-legible operational capacity and
shared benefit.
Admin-risk terms such as anti-capitalist, solidarity economy, mutual aid, commons, worker control,
collectivize, abolition, and wealth redistribution, with substitutions such as shared ownership,
democratic enterprise, pooled infrastructure, and community wealth-building.
Risk entries for governance immaturity, informal member commitments, slow decision-making,
legal-form mismatch, capitalization gaps, unclear patronage model, weak controls, member-class
conflict, and underutilized shared assets.
13.6 Ecosystem Intermediary / Regenerative Systems Supplier —
ecosystem_intermediary
Required starter content:
Search terms for intermediary, ecosystem builder , backbone organization, technical assistance,
capacity builder , implementation partner , training provider , systems integrator , navigator , extension
provider , adoption support, deployment partner , and regenerative systems supplier .
Program keywords for rural business, cooperative development, regional food business centers,
EDA, SBIR/STTR, extension, technical assistance, workforce, innovation clusters, and capacity-
building grants.
Evidence signals such as customer letters, partner commitments, prior deployments, case studies,
technical specifications, implementation plans, training curriculum, support model, pricing model,
staff credentials, and evaluation plan.
KFR classes for service type, customer segment, end-user benefit, technical capability, technology
readiness, prior deployments, partner network, customer commitments, support model, pricing,
adoption barriers, and downstream outcomes.
Register defaults that are credible, implementation-oriented, and careful not to sound like vendor
hype.
Admin-risk terms such as disruption, platform dominance, surveillance, automation replacing
workers, monopoly, proprietary lock-in, extractive scaling, and AI replacing staff, with substitutions•

around adoption support, workforce augmentation, interoperable tools, and customer-owned
infrastructure.
Risk entries for private-vendor subsidy perception, unclear end-user benefit, overstated readiness,
weak demand evidence, adoption friction, support burden, proprietary lock-in, data governance,
weak maintenance, and insufficient training.
14. Starter CLC Content Requirements
The following field groups must be populated for all eight CLC cards.
14.1 Public Purpose & Works — public_purpose_works
Required starter content:
Underwriting criteria for eligibility, public benefit, statutory/program purpose, allowable use,
readiness, procurement, match, site control, maintenance, service-area need, and audit readiness.
Program terms for public works, infrastructure, CDBG, community facilities, water/wastewater ,
stormwater , transportation safety, brownfields, hazard mitigation, public safety, broadband, main
street, distressed community, and environmental review.
Evidence weights for eligibility citation, board resolution, engineering estimate, capital plan, service-
area data, census data, match commitment, site control, procurement policy, and maintenance plan.
Narrative sections for eligibility, need, public benefit, readiness, budget, match, procurement,
environmental review, operations, maintenance, and timeline.
Reviewer profile centered on program officers, compliance reviewers, engineers, financial reviewers,
and economic-development reviewers.
Red flags for vague eligibility, weak public benefit, uncommitted match, procurement silence,
unresolved site control, missing planning citations, and unrealistic construction timelines.
Post-award commitments for construction milestones, procurement, match expenditures,
beneficiary counts, facility improvements, jobs, compliance filings, and closeout.
14.2 Catalytic Change — catalytic_change
Required starter content:
Underwriting criteria for theory of change, systems leverage, novelty, transition plausibility,
replication, field learning, partnership strength, measurement, follow-on capital, and timing.
Program terms for innovation, demonstration, pilot, proof of concept, systems change,
transformation, climate-smart, accelerator , challenge grant, catalytic capital, field building, model
replication, leverage, and social innovation.
Evidence weights for explicit theory of change, systems map, pilot results, partner commitments,
learning agenda, replication pathway, leverage plan, baseline metrics, and evaluation partner .
Narrative sections for theory of change, systems context, intervention model, innovation, learning,
partnerships, evaluation, dissemination, and scale.
Reviewer profile centered on foundation program officers, innovation reviewers, policy/systems-
change reviewers, and subject matter experts.•

Red flags for wishlist theory of change, no leverage point, unsupported innovation, no learning
agenda, no replication path, role-less partnerships, and diffuse benefits.
Post-award commitments for pilot milestones, learning products, convenings, model refinements,
dissemination, policy/market engagement, replication inquiries, and follow-on funding.
14.3 Operating Capacity — operating_capacity
Required starter content:
Underwriting criteria for capacity bottleneck, mission relationship, staffing/systems need,
implementation plan, management readiness, governance, measurable capacity gain, sustainability,
budget-to-task integrity, and dependency risk.
Program terms for capacity building, operating support, organizational effectiveness, technical
assistance, planning, readiness, staffing, administrative capacity, systems improvement, governance,
board development, strategic planning, and data systems.
Evidence weights for workload evidence, staffing plan, job descriptions, org chart, board approval,
systems audit, strategic plan, backlog/demand, financial statements, and implementation timeline.
Narrative sections for organizational background, capacity need, proposed investment, staffing/
systems plan, outcomes, sustainability, and budget justification.
Reviewer profile centered on foundation program officers, capacity reviewers, public agency
program officers, and national service reviewers.
Red flags for vague operating support, no measurable capacity gain, new hire not tied to outcomes,
systems purchase without adoption plan, no sustainability, hidden management weakness, and
weak budget mapping.
Post-award commitments for staff hired, systems implemented, trainings completed, policies
adopted, service capacity increased, turnaround time reduced, and data quality improved.
14.4 Research & Evidence — research_evidence
Required starter content:
Underwriting criteria for research question, significance, method fit, data collection, evaluation rigor ,
team qualifications, human subjects/IRB, data management, dissemination, broader impacts, and
feasibility.
Program terms for research, evidence, evaluation, study, pilot study, applied research, participatory
research, field trial, randomized controlled trial, quasi-experimental, mixed methods, data
management, broader impacts, intellectual merit, IRB, human subjects, dissemination, SBIR, and
STTR.
Evidence weights for aims, literature review, preliminary data, study protocol, evaluation design,
data management, IRB plan, research partner letter , biosketches, dissemination plan, and
methodology-linked budget.
Narrative sections for abstract, aims, significance, background, innovation, approach, evaluation,
data management, human subjects, broader impacts, dissemination, and investigator qualifications.
Reviewer profile centered on peer reviewers, scientific reviewers, evaluators, program officers, and
technical subject matter experts.
Red flags for vague questions, method mismatch, underbudgeted evaluation, ignored human
subjects, missing data management, unrealistic sample size, overclaimed causality, vague
dissemination, and team expertise gaps.•

Post-award commitments for protocol completion, IRB milestones, participant recruitment, data
collection, analysis, interim findings, reports, publications, presentations, and datasets.
14.5 Market Access — market_access
Required starter content:
Underwriting criteria for target market, verified demand, buyer commitment, channel strategy,
revenue model, competitive position, delivery capacity, pricing logic, customer acquisition, unit
economics, and risk mitigation.
Program terms for market access, commercialization, business development, export development,
procurement readiness, buyer development, distribution, sales channel, marketing plan, trade
promotion, product-market fit, go-to-market, e-commerce, retail readiness, wholesale readiness, and
institutional procurement.
Evidence weights for buyer letters, purchase orders, sales history, customer pipeline, distributor
agreements, market study, price sheet, production capacity proof, revenue projections, customer
interviews, and channel partner letters.
Narrative sections for market opportunity, customer profile, sales strategy, distribution, competitive
landscape, pricing, production capacity, projections, and risk.
Reviewer profile centered on business reviewers, lenders, economic-development reviewers,
agriculture market specialists, and commercialization reviewers.
Red flags for no buyer commitment, market-size substitution, unsupported projections, unsolved
distribution, ignored customer acquisition cost, insufficient production capacity, pricing below cost,
and no competitive analysis.
Post-award commitments for buyers contacted, buyers converted, sales meetings, contracts, units
sold, revenue, new markets, distributors, repeat purchases, acquisition cost, and margin.
14.6 Credit & Underwriting — credit_underwriting
Required starter content:
Underwriting criteria for repayment capacity, cash flow, debt service coverage, collateral, credit
history, owner equity, management capacity, financial controls, use of funds, risk mitigation,
guarantor strength, and covenant compliance.
Program terms for loan, credit, underwriting, working capital, term loan, microloan, loan guarantee,
SBA 7(a), SBA 504, CDFI, revolving loan fund, debt service, collateral, guarantee, pro forma, balance
sheet, income statement, debt schedule, covenant, and loan loss reserve.
Evidence weights for financial statements, tax returns, pro forma, cash flow projections, debt
schedule, collateral documentation, credit explanation, purchase orders/contracts, owner equity
injection, management resume, insurance, and use-of-funds budget.
Narrative sections for borrower profile, use of funds, repayment source, business history,
management capacity, financial projections, collateral, risk mitigation, and community impact for
mission lenders.
Reviewer profile centered on lenders, credit analysts, loan committees, CDFI underwriters, SBA
lenders, and community development finance reviewers.
Red flags for weak cash flow, unsupported pro forma, no repayment source, poor controls, unclear
collateral, missing owner equity, commingled finances, inconsistent tax returns, weak management,
and hidden debt.•

Post-award commitments for financial statements, covenant tracking, debt service, revenue targets,
expense controls, collateral status, insurance, jobs, use-of-funds documentation, and annual
financials.
14.7 Sponsorship & Corporate Support — sponsorship_corporate
Required starter content:
Underwriting criteria for audience fit, brand alignment, visibility value, community goodwill,
activation plan, sponsor benefits, measurable reach, reputational safety, relationship pathway, and
renewal potential.
Program terms for sponsorship, corporate giving, corporate foundation, CSR, ESG, community
relations, employee engagement, brand partnership, cause marketing, in-kind sponsorship, event
sponsorship, activation, audience reach, impressions, benefits package, sponsorship deck, and
community investment.
Evidence weights for audience demographics, attendance history, sponsorship deck, media kit, prior
sponsor outcomes, social/email reach, activation calendar , press coverage, brand alignment memo,
benefits package, and sponsor testimonials.
Narrative sections for partnership opportunity, audience and reach, brand alignment, community
value, sponsor benefits, activation, measurement, and renewal.
Reviewer profile centered on corporate giving officers, marketing managers, CSR managers,
community relations officers, and corporate foundation staff.
Red flags for treating sponsorship like a grant, no sponsor benefit, audience mismatch, ignored
brand risk, vague activation, no measurement, inflated impressions, and one-way ask without
relationship strategy.
Post-award commitments for logo placements, social posts, impressions, attendance, sponsor
mentions, employee engagement, VIP benefits, content assets, post-event reporting, and renewal
meetings.
14.8 Shared Assets — shared_assets
Required starter content:
Underwriting criteria for shared need, user base, governance, access policy, utilization, maintenance,
asset control, cost recovery, equitable access, replacement reserve, and community/member benefit.
Program terms for shared asset, shared infrastructure, commons, community facility, equipment
library, tool library, shared-use kitchen, maker space, food hub, cooperative infrastructure,
community land trust, pooled resource, collective ownership, public access, utilization, maintenance
reserve, and asset management.
Evidence weights for user/member commitments, governance agreement, access policy, site control,
equipment quote, utilization forecast, maintenance budget, scheduling policy, insurance,
replacement reserve, shared-use agreement, and demand study.
Narrative sections for shared need, asset description, user base, governance, access/equity,
operations, maintenance, budget, sustainability, and community/member benefit.
Reviewer profile centered on community development reviewers, cooperative development
reviewers, facilities reviewers, foundation program officers, and public agency reviewers.•

Red flags for one-party capture of shared asset, unclear governance, vague access rules, unfunded
maintenance, assumed utilization, no scheduling/conflict process, unresolved site control, ignored
replacement cost, and no insurance plan.
Post-award commitments for users served, utilization hours, bookings, maintenance logs, downtime,
cost recovery, access equity, repairs, replacement reserve contributions, and community benefit
outcomes.
15. Research Process for Card Population
15.1 Phase 1 — Prior-Art Absorption
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
_research_metadata :
priors_consulted :
-path:"path"
extract_note :"whatwasextracted"
15.2 Phase 2 — Primary Research
For CIC cards:
Review awarded grant abstracts or public award descriptions.
Review agency program pages.
Review foundation award descriptions or 990-PF grants where applicable.
Review state/local program pages where relevant.
Extract vocabulary, evidence patterns, capacity signals, compliance burdens, and reporting rhythms.
For CLC cards:
Review representative NOFOs, RFAs, FOAs, program guidelines, or lender/sponsor materials.
Extract underwriting criteria, scoring patterns, required sections, forms, reviewer logic, red flags,
and post-award obligations.•

15.3 Phase 3 — Draft Card
Populate the card using the relevant schema. Empty fields must not be hidden. Use explicit flags:
_note:"NEEDED —research orreview"
15.4 Phase 4 — Self-Validation
Before review, each draft card must pass:
Schema completeness check.
Source/provenance completeness check.
No hardcoded CIC × CLC eligibility coupling.
No private customer data.
No unsourced numeric win-rate claims.
No unsupported program claims.
No excessive copied source text.
No production load if unsigned.
15.5 Phase 5 — Review Handback
Each card handback should include:
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
  READY | DEFER_PENDING_CHANGES•

16. Review, Signing, and Runtime Promotion
16.1 Lifecycle States
lifecycle :
draft_status :draft | reviewed | thesis_passed | signed | loaded | deprecated
review_status :pending | passed | changes_requested
cross_family_thesis_status :pending | passed | failed
signature_status :unsigned | signed | revoked
runtime_load_status :not_loaded | loaded | disabled
16.2 Promotion Requirements
A card may be loaded into production only when:
It validates against schema.
It contains no private organization-specific data.
It has passed internal review.
It has passed adversarial review.
It has source citations for factual claims.
It has no unresolved coupling violations.
It has a valid signature.
16.3 Development vs. Production Loading
Development mode may load unsigned cards for testing.
Production mode must reject:
unsigned cards;
malformed cards;
cards with missing required fields;
cards marked changes_requested ;
cards with revoked signatures;
cards containing private organization data;
cards that encode CIC × CLC eligibility subsets.
17. Testing Requirements
Post-Alpha implementation should include automated tests for:
Schema validation:
  - Missing required CIC field fails.
  - Missing required CLC field fails.•

  - Unknown card slug fails.
  - Invalid card_axis fails.
Signing and lifecycle:
  - Unsigned card fails production load.
  - Revoked signature fails production load.
  - Draft card can load only in development.
Memory isolation:
  - Cross-org retrieval fails closed.
  - Card namespace cannot contain org-specific data.
  - Matrix observations cannot retrieve private cycle records.
Coupling discipline:
  - CIC card cannot contain common_clc_patterns_observed.
  - CIC card cannot contain CLC allowlists, deny-lists, ranking
preferences, or win-rate fields.
  - CLC card cannot contain CIC allowlists, deny-lists, ranking
preferences, or win-rate fields.
  - Matrix schema must label observations as non-binding and forward-compatible
only.
  - Scout/Scribe/Judge cannot read matrix fields during eligibility or ranking.
Runtime behavior:
  - Scout expands vocabulary by active CIC.
  - Scribe applies register defaults by active CIC.
  - Judge uses CLC underwriting criteria.
  - Logician blocks hard compliance failures.
  - Report Generator extracts CLC-specific commitments.
Safety and quality:
  - Unsupported claims are surfaced.
  - Admin-risk terms are flagged.
  - Required evidence gaps are listed.
  - Export is blocked when hard gates fail.
18. Phased Implementation Map
The label “post-Alpha” is too broad for implementation control. This work should be staged by architecture/
blueprint lock state and runtime maturity.
18.1 Phase A — v0.1 Beta Scope: Architecture, Schema, Logician, Loader Stubs
Phase A can move immediately.

Definition of done:
Architecture amendment candidate exists.
Blueprint §18 candidate exists.
F-CARDS-* Logician hardening family is specified.
Directory layout exists under pipeline/cards/ .
CIC and CLC schemas exist.
Pydantic models or equivalent typed models exist.
Loader stub exists.
Unsigned development fixtures exist for:
food_systems  CIC
operating_capacity  CLC
Production loader rejects unsigned cards.
CIC schema excludes common_clc_patterns_observed .
Matrix content is explicitly forward-compatible only.
Phase A does not require the full research population of all fourteen cards.
18.2 Phase B — v0.2 First Wave: Runtime Context Injection
Definition of done:
Active CIC and CLC load into workflow state.
Scout can use CIC search vocabulary.
Scribe can use CIC register and evidence defaults.
Judge can use CLC underwriting criteria.
Logician can evaluate card lifecycle and schema validity.
Report Generator can read reporting and commitment patterns.
18.3 Phase C — v0.2 First Wave: Memory Wiring
Definition of done:
Card namespaces exist.
Explicit namespace allow-list retrieval is enforced.
Cross-org discovery fails closed.
Signed cards can be retrieved as public/shareable scaffold context.
Per-organization content remains isolated.
18.4 Phase D — v0.2 Through v1: Full Card Content Population
Definition of done:
All six CIC cards are researched, reviewed, and signed.
All eight CLC cards are researched, reviewed, and signed.
Each card contains citations or source metadata for factual claims.
Each card passes schema and coupling tests.
Each card has a handback summary and review record.•

Phase D is research-heavy and can run in parallel with Phase B/C once Phase A locks.
18.5 Phase E — v1.x: UI Surfacing
Definition of done:
Customer-visible interface exposes active Funding Profile and Funding Logic.
UI shows evidence needed, missing information, risk flags, register notes, and reporting
commitments.
Internal implementation terms remain behind admin/engineering views.
18.6 Phase F — v1.x: Matrix and Outcome Learning
Definition of done:
Matrix content begins only after explicit v1.x amendment.
Matrix files use per-intersection namespace: cards:matrix:<intersection_id> .
Matrix is read only by allowed components.
Matrix never participates in eligibility filtering or opportunity exclusion.
Cycle receipts can store CIC/CLC tags.
Non-identifying pattern signals require review before shared ingestion.
19. L-005 Two-Cycle Audit Plan
This amendment should pass through the standard two-cycle review before lock.
Cycle 1 — Scoping and Defect Identification
Review targets:
Schema completeness.
Coupling violations.
Namespace consistency.
Routing compatibility.
Signature lifecycle.
Repository layout.
Phase mapping.
Logician gate sufficiency.
Expected Cycle 1 outputs:
Defect list.
Required revisions.
Open decisions.
Lock blockers.•

Cycle 2 — Verification and Lock Recommendation
Review targets:
Confirm defects were resolved.
Confirm no hidden CIC × CLC coupling remains.
Confirm matrix is forward-compatible only.
Confirm repository layout aligns with pipeline structure.
Confirm Phase A can land without full content population.
Confirm loader and Logician fail-closed behavior .
Expected Cycle 2 outputs:
PASS / FAIL.
Lock recommendation.
Remaining non-locking notes.
20. Immediate Action Plan
Move now
Proceed with Phase A:
Create architecture amendment candidate.
Create blueprint §18 candidate.
Add F-CARDS-* Logician hardening specification.
Establish pipeline/cards/  directory structure.
Add CIC and CLC schemas.
Add typed models.
Add loader stub.
Add fixture stubs for food_systems  and operating_capacity .
Run L-005 two-cycle audit.
Do not wait for full research population
Phase A does not depend on full card research. The purpose of Phase A is to provide the schema,
gates, loader , and architecture target that future card research will populate.
Defer
Defer until later phases:
Full population of all fourteen cards.
Matrix content.
Outcome-learning loop.
Customer-facing UI surfacing.•
1.
2.
3.
4.
5.
6.
7.
8.
9.

21. Lock Candidate Summary
This document should be treated as a paired architecture amendment and blueprint section candidate.
Recommended paired lock package:
Architecture:
  pipeline/architecture/v0.1/architecture_v7_0_11_card_amendment.md
Blueprint:
  pipeline/blueprint/v0.1/section_18_card_system.md
Logician hardening:
  pipeline/blueprint/v0.1/section_04_logician_v2_x_card_hardening.md
Repository assets:
  pipeline/cards/CIC/
  pipeline/cards/CLC/
  pipeline/cards/matrix/
  pipeline/cards/_schema/
  pipeline/cards/models.py
  pipeline/cards/loader.py
The lock candidate is acceptable only if:
CIC cards do not include common_clc_patterns_observed .
CLC cards do not include CIC eligibility or preference fields.
Matrix files are forward-compatible only until v1.x.
Matrix namespace is per-intersection.
Logician gates prevent pattern reads during eligibility.
Signed cards are treated as public/shareable scaffold context.
Private organization data is rejected from card content.
Production loading requires review and signature.
The Card System is the runtime substrate that makes Tilth’s Cards operational. It should land as
architecture, schema, and hardening first; content population can follow against the locked target.•
32