---
title: Funder-as-specimen integration — compound amendment pre-stage
date: 2026-05-16
status: PENDING — single compound amendment when triggered ("when we get there"); not currently in L-005 pipeline
authority: source conversation 2026-05-16 (Josh + Claude) over regenerative-funder exploration; canonical drawings TILTH-CLC-00 + TILTH-CIC-REVIEW-01
locks_affected: §8 architecture thesis (Cards-vs-Cards reconciliation closure) + §0.5 closed-set extension (3 new primitive_kinds — applicant_playbook + evidence_grammar + vertical_configuration) + §4 Logician (F-RELEVANCE-* family + candidate F-PLAYBOOK-* gates) + Wave 2 CLC card content deepening
locks_NOT_affected: TILTH-CIC-01 Food Systems (Wave 1 LOCKED 2026-05-15 PM) + TILTH-CLC-03 Operating Capacity (Wave 1 LOCKED 2026-05-15 PM) + architecture v7.0.8 F-CIC-CLC-COUPLING-VIOLATION (structural floor — this amendment extends it to applicant_playbook)
operator_lean: single compound amendment when triggered; sixteen FULL cross-family rounds suggest the single-vehicle discipline is carryable
---

# Funder-as-specimen integration — compound amendment pre-stage

## 1. Thesis

Funders are training specimens, not card primitives. SARE, PASA, VAPG, PA Agricultural Innovation, and PA DEP SBAG taught us what the eight CLCs and six CICs needed to be. Their reusable persuasive logic folds into the canonical CLC card content; the specimens themselves stay in the Funder Intelligence Database (FID) where Scout queries them and Editor / Scribe consult during dialect code-switching. **No funder-card primitive.**

Per-funder distilled lesson:

- **SARE** — farmer-led research, technical-advisor logic, outreach, reimbursement, useful-learning discipline. Trains Research & Evidence (primarily) + Operating Capacity (TA dimension).
- **PASA** — food-system field grammar: environmentally sound, economically viable, community-focused farms. Trains Operating Capacity + Public Purpose & Works.
- **VAPG** — value-added business viability, market expansion, match readiness, federal work-plan discipline. Trains Market Access + Credit & Underwriting.
- **PA Agricultural Innovation** — state-level implementation, technology adoption, five innovation principles, regional impact. Trains Catalytic Change + Public Purpose & Works + Shared Assets (regional-impact track).
- **PA DEP SBAG** (regenerative subset only) — measured retrofit logic, pre/post savings evidence, calculator integrity, reimbursement discipline, one-year follow-up proof. Trains Credit & Underwriting + Public Purpose & Works. **Only enters the regenerative card stack through the Regenerative Relevance Filter.**

## 2. Asking / giving — canonical CIC × CLC orthogonality frame

One taxonomy asks, the other gives. Any (CIC × CLC) pair is reachable in principle. Matching is opportunity-driven at runtime, never archetype-driven at design-time. F-CIC-CLC-COUPLING-VIOLATION (architecture v7.0.8, 2026-05-08) remains the structural floor; this round extends it to any new applicant-side primitive (`applicant_playbook`).

Canonical disambiguators — print on CIC cards themselves so orthogonality is shown, not asserted:

- A **farmer** (Food Systems CIC) can ask for **education money** (could activate Operating Capacity, Catalytic Change, Research & Evidence — depending on the opportunity).
- A **school** (Educator CIC) can ask for **solar / ag money** (could activate Public Purpose & Works, Catalytic Change, Shared Assets — depending on the opportunity).

Both directions are routine. No CIC ever preselects its reachable CLC set.

## 3. Canonical names — proposal label → canonical mapping

CLC canonical names per TILTH-CLC-00 (Sovereign Node LLC drawing, 2026). No "-Capital" suffix.

| Proposal label | Canonical CLC | Card # |
|---|---|---|
| Public Purpose & Works | Public Purpose & Works | 1 |
| Catalytic Change Capital | **Catalytic Change** | 2 |
| Capacity Building Capital | **Operating Capacity** | 3 |
| Research & Evidence Capital | **Research & Evidence** | 4 |
| Market Access Capital | **Market Access** | 5 |
| Credit & Underwriting Capital | **Credit & Underwriting** | 6 |
| Sponsorship & Corporate Support | Sponsorship & Corporate Support | 7 |
| Commons / Shared Asset Capital | **Shared Assets** | 8 |
| equity_and_access_capital | (orphan — does not exist; no 9th CLC) | — |

The orphan `equity_and_access_capital` reference in the proposal traces to an earlier draft when Urban Agriculture was a separate CIC. Urban Ag was folded into Food Systems CIC; equity / access concerns now distribute across the Food Systems CIC search vocabulary + evidence schemas + the Public Purpose & Works civic-benefit framing. Not a 9th CLC.

CIC canonical names per TILTH-CIC-REVIEW-01 (six core customer worlds). No change at this layer from this round — the Food Systems CIC is the only CIC affected, and only by adding `applicant_playbook` sub-primitives beneath it.

## 4. Compound amendment — seven components

### Component 1 — §8 architecture thesis update

Funder-as-specimen + asking / giving canonical, with farmer-asks-for-education-money and school-asks-for-solar-money as disambiguators. Closes the §8 Cards-vs-Cards reconciliation flagged in `memory/project_capital_logic_cards_v9_state.md`. Replace the §8 reconciliation-pending language with the resolved thesis.

### Component 2 — New §0.5 primitive_kind `applicant_playbook`

Seven Food Systems composition profiles. Each is a sub-primitive **beneath** TILTH-CIC-01 Food Systems (not a parallel CIC). Captures **what the applicant brings** — evidence shapes, language register, project archetypes, red flags. **Never captures which CLCs the applicant can reach.** Same AST-lint + Cedar floor as F-CIC-CLC-COUPLING-VIOLATION; extended to bar playbook→CLC coupling.

Seven stubs (full YAML in Annex A): Working Farm / Producer · Value-Added Producer / Processor · Agricultural Innovation Implementer · Regional Food Infrastructure / Cooperative · Agricultural Technical Assistance Provider · Urban Agriculture / Community Food · Regenerative Small Business Retrofit.

The Regenerative Small Business Retrofit playbook is the SBAG-derived card, **scope-gated by the Regenerative Relevance Filter** — excludes generic small-business retrofits (medical X-ray, generic office HVAC, unrelated retail / manufacturing, etc.).

### Component 3 — New §0.5 primitive_kind `evidence_grammar`

Seven evidence grammars. Attach orthogonally to multiple CICs and multiple CLCs. Pulled out of the per-CIC Evidence Schema so the same grammar (e.g., on-farm research evidence) is reusable across the Food Systems CIC, the Educator CIC (school-led research), and any CLC where the grammar matches the opportunity.

Seven stubs (full YAML in Annex B): On-farm research · Value-added business case · Ag innovation implementation · Regenerative pre/post savings · Agricultural natural resource protection · Market expansion / value chain · Reimbursement & match readiness.

### Component 4 — New Logician failure family `F-RELEVANCE-*` + `vertical_configuration` primitive

The Regenerative Relevance Filter as Law 2 (No Boundary Drift) structural floor at the vertical layer. Stops the medical-X-ray-scanner pollution example by deterministic predicate, not by LLM judgment.

The filter itself is a `vertical_configuration` primitive (new §0.5 closed-set extension — third primitive_kind added in this compound). Golden Quill v0.1 ships with the regenerative-agriculture configuration loaded; future verticals swap the configuration payload without re-implementing the gate mechanism.

Regenerative-agriculture configuration:

```yaml
vertical_id: regenerative_agriculture
brand_line: "Golden Quill — regenerative grant intelligence."

pass_if_project_advances:
  - soil_health
  - water_quality
  - watershed_protection
  - agricultural_runoff_reduction
  - farm_viability
  - producer_income
  - food_processing_efficiency
  - food_storage_or_cold_chain_efficiency
  - local_or_regional_food_distribution
  - agricultural_energy_efficiency
  - renewable_or_reduced_energy_use_for_farm_or_food_operations
  - labor_augmentation_for_agricultural_operations
  - biosecurity_or_plant_animal_health
  - producer_owned_value_added_processing
  - cooperative_or_multi_farm_infrastructure
  - farmer_training_or_technical_assistance
  - climate_resilience_for_land_based_enterprises
  - urban_agriculture_land_water_food_access_benefit
  - food_loss_reduction
  - composting_or_waste_reduction_when_program_eligible
  - agricultural_bmp_implementation

reject_examples:
  - medical_office_upgrade
  - generic_professional_services_energy_upgrade
  - unrelated_retail_lighting
  - non_ag_manufacturing_retrofit
  - generic_commercial_hvac_without_food_land_or_ag_context
  - digital_xray_or_scanner_upgrade
  - general_small_business_green_upgrade_without_regenerative_connection
  - unrelated_industrial_pollution_control
```

Candidate F-RELEVANCE-* gates to land at compound (predicate signatures; bodies LIVE at LOCK per §17 v1 precedent):

- `F-RELEVANCE-OUT-OF-VERTICAL` — project_advances tag set disjoint from vertical pass_if set; fail-closed.
- `F-RELEVANCE-FUNDER-SCOPE-GUARD` — funder module invoked outside its regenerative-relevance subset (e.g., SBAG medical / office branch); fail-closed.
- `F-RELEVANCE-CARD-INJECTION-OUT-OF-SCOPE` — non-regenerative funder logic attempting to enter a card (Wave 2 deepening protection); fail-closed.
- `F-RELEVANCE-COVERAGE-INCOMPLETE` — META gate; required F-RELEVANCE-* enforcement modules + drift tests missing from runtime tree. Mirrors F-CLASS-COVERAGE-INCOMPLETE / F-PACKET-COVERAGE-INCOMPLETE / F-WPFA-COVERAGE-INCOMPLETE pattern.

Additional candidate F-PLAYBOOK-* gates surfaced in conversation (probably defer to follow-on §4 v2.x.y after compound lands):

- `F-PLAYBOOK-REIMBURSEMENT-CASH-FLOW` — applicant_playbook signals reimbursement program but cash-flow readiness evidence absent.
- `F-PLAYBOOK-MATCH-SOURCE-INTEGRITY` — match source claimed but not allowed under program rule, or amount does not meet program rule.
- `F-PLAYBOOK-BUDGET-CROSSWALK` — budget lines do not crosswalk to work-plan activities.
- `F-PLAYBOOK-CALCULATOR-INTEGRITY` — calculator inputs do not match vendor quote / invoice line items.
- `F-PLAYBOOK-PROMISE-LEDGER-DRIFT` — post-award commitments tracked in `proposal_commitments.yaml` (per §11 AWARD_INGEST) drift from drafted promises; surfaces at award-acceptance gate.

### Component 5 — Wave 2 CLC card deepening

The 12-card Wave 2 currently in flight (per `project_card_wave_1_locked.md` follow-on; vocabulary now "cards" not "cards") absorbs the deepened CLC injection logic from the SARE / PASA / VAPG / PA AIG / SBAG specimens, mapped to canonical CLC names. Per-CLC deepening notes:

- **Public Purpose & Works** — PA Agricultural Innovation language seeds: "Pennsylvania agricultural competitiveness · environmental stewardship · farm viability · resource efficiency · water quality protection · soil and water resources · regional food-system resilience · public-benefit agricultural infrastructure." Public-purpose-vs-private-benefit framing discipline. Avoid private-benefit-only framing.
- **Catalytic Change** — SARE farmer-led innovation grammar + PA AIG five-innovation-principles (relevant · practical · accessible · scalable · triple-bottom-line aligned). Distinguishes practical innovation from "innovation as buzzword." Tests: old constraint → innovation in plain operational terms → who can replicate.
- **Operating Capacity** — PASA technical-assistance / farmer-training field grammar; PA AIG planning grant logic; SARE technical-advisor requirement. Implementation-support / planning-to-implementation pathway language. Producer readiness, peer learning, resource navigation, field-tested guidance.
- **Research & Evidence** — SARE on-farm research / demonstration / prototype / survey grammar; useful-failure discipline; technical-advisor role; outreach-so-other-farmers-can-learn requirement. Field-tested, farmer-led inquiry, practical knowledge, replicable learning, measured under real production conditions.
- **Market Access** — VAPG value-added chain (commodity → producer ownership or control → transformation step → product → buyer channel → distribution / storage → margin → producer income). Maple RO / cold storage / wash-pack / cooperative distribution patterns. Producer-owned value-added processing emphasis. Reject product-without-buyer and processing-equipment-without-market-channel.
- **Credit & Underwriting** — VAPG 1:1 match requirement; PA AIG 30% / 50% non-state cash match; SBAG reimbursement-readiness. Source-and-use of funds discipline. Quote → calculator → invoice → reimbursement integrity. Cash-flow risk disclosure. Eligible / ineligible cost separation.
- **Sponsorship & Corporate Support** — reframe for regenerative context: field validation, buyer / partner / mentor credibility, success-story consent. SBAG follow-up success-story / mentor logic; SARE outreach requirement. Reject performative partnership and partner-named-without-role.
- **Shared Assets** — PA AIG regional-impact grant logic (two or more persons / businesses or a cooperative association involved in growing, harvesting, processing, packing, or managing agricultural commodities); VAPG mid-tier value chain; food-hub / shared-cold-storage / cooperative-processing patterns. Required logic: who uses, how access governed, what problem is shared, how small / medium farms benefit.

### Component 6 — Funder dialect → FID records, no card primitive

Funder dialect samples (the "this is how SARE talks about farmer-led inquiry" content) live as Funder Intelligence Database records. Editor and Scribe query the FID at runtime during dialect code-switching. **No `funder_dialect_card` primitive.** Cards are heavy primitives (signed publisher pubkey, loader, validators, seat dependencies, Cedar policy, F-CARDS-COVERAGE-INCOMPLETE participation); funder dialect is reference material consumed during drafting, not runtime-orchestrated. Promoting funder material into the card layer would also undermine the funder-as-specimen thesis by stealth.

### Component 7 — Mode router lands at code time as Scribe / Scout heuristic

The five modes from the 2026-05-16 conversation:

- `farmer_research_mode` (exemplar SARE) — research / demonstration / prototype / survey / farmer education project types; primary question "What can farmers test, learn, and share?"; primary CLC activations Research & Evidence + Operating Capacity (TA dimension).
- `food_system_field_mode` (exemplar PASA) — technical assistance / farmer training / community science / equity access / peer learning; primary question "How does this strengthen food-system capacity, resilience, equity, and farmer support?"; primary CLC activations Operating Capacity + Public Purpose & Works + Research & Evidence.
- `value_added_business_mode` (exemplar USDA VAPG) — value-added processing / working capital / planning / market access; primary question "Can the producer create a viable value-added product, market, and income case?"; primary CLC activations Market Access + Credit & Underwriting.
- `innovation_implementation_mode` (exemplar PA Agricultural Innovation) — equipment implementation / ag technology / automation / biosecurity / energy / processing efficiency; primary question "Can the applicant implement practical innovation that improves agriculture?"; primary CLC activations Catalytic Change + Public Purpose & Works + Credit & Underwriting.
- `measured_retrofit_mode` (exemplar PA DEP SBAG regenerative subset) — energy efficiency / pollution prevention / water reduction / food storage efficiency / agricultural NRP; **regenerative_relevance_filter must pass**; primary question "Can the applicant prove measurable pre/post resource savings?"; primary CLC activations Credit & Underwriting + Public Purpose & Works.

These are runtime composition shortcuts but **not** new primitives. Implement as a Scribe / Scout heuristic dispatcher: given project_type, recommend a starting compose across CIC × applicant_playbook × evidence_grammar × CLC. If the modes become architectural, they'll start coupling CIC and CLC by stealth. The "primary CLC activations" notes above are **drafting hints for the dispatcher**, not bindings — Logician still gates against playbook→CLC coupling and asks Scribe to verify opportunity-fit at runtime.

## 5. Open questions before compound dispatch

**OQ-1** — Confirm `applicant_playbook` as the primitive name, or operator-preferred alternative?

**OQ-2** — `vertical_configuration` primitive scope: limit to v0.1 (regenerative only) or design for multi-vertical from the start? Multi-vertical design is mostly schema work; regenerative-only is lighter but forces a v0.2 amendment when a second vertical lands.

**OQ-3** — Deeper playbook-side Logician gates (F-PLAYBOOK-REIMBURSEMENT-CASH-FLOW · F-PLAYBOOK-MATCH-SOURCE-INTEGRITY · F-PLAYBOOK-BUDGET-CROSSWALK · F-PLAYBOOK-CALCULATOR-INTEGRITY · F-PLAYBOOK-PROMISE-LEDGER-DRIFT) — bundle into compound, or follow-on amendment?

**OQ-4** — Memory consolidation precondition. MEMORY.md is over its 24.4KB size limit (28.2KB observed). Several index entries reference "card" / "Card System" vocabulary that this amendment retires. A consolidation pass should land before the compound to keep §8 thesis writing against clean vocabulary. Run `tilth memory consolidate-index` before dispatch?

**OQ-5** — Wave 2 timing. The 12-card Wave 2 deepening is already in flight. Does the compound amendment land BEFORE Wave 2 (so Wave 2 carries the funder-as-specimen logic from inception) or AFTER (so Wave 2 absorbs the deepening as a Wave 2.1 follow-on)?

## 6. Annex A — applicant_playbook stubs

All seven stubs faithful to the 2026-05-16 conversation content. Fields stripped vs the original "client information card" proposal:

- `default_capital_logic` / `default_capital_logic_stack` — REMOVED (F-CIC-CLC-COUPLING-VIOLATION; CICs and playbooks never preselect CLCs).
- `default_funder_modules` — RENAMED to `relevant_fid_funder_modules` with explicit comment that these are FID query hints for Scout, NOT card bindings and NOT eligibility gates.
- Parent attribution added (`parent_cic: TILTH-CIC-01` — all seven sit beneath Food Systems).
- `governing_filter: regenerative_relevance_filter` added where applicable.

### A.1 Working Farm / Producer

```yaml
applicant_playbook:
  name: "Working Farm / Producer"
  parent_cic: TILTH-CIC-01  # Food Systems
  governing_filter: regenerative_relevance_filter

  eligibility_signals:
    - produces_agricultural_commodity
    - farm_sales_or_normal_sales
    - land_or_production_site
    - operator_experience
    - production_records
    - farm_financials

  common_project_types:
    - on_farm_research
    - sustainable_agriculture_demonstration
    - equipment_implementation
    - energy_efficiency
    - soil_health_or_water_quality_bmp
    - labor_augmentation
    - biosecurity
    - value_added_processing
    - market_access

  evidence_to_collect:
    - production_records
    - crop_or_livestock_plan
    - soil_tests
    - water_or_energy_use
    - sales_history
    - photos
    - quotes
    - invoices
    - technical_advisor_letter
    - buyer_or_partner_letters
    - farm_map_or_site_plan

  relevant_fid_funder_modules:
    # FID query hints for Scout — NOT card bindings, NOT eligibility gates
    - sare_farmer
    - pa_agricultural_innovation
    - usda_vapg
    - pa_sbag_regenerative_subset

  red_flags:
    - vague_regenerative_claims
    - equipment_without_operational_problem
    - no_measurement_plan
    - reimbursement_cash_flow_gap
    - market_claim_without_buyer_or_channel
```

### A.2 Value-Added Producer / Processor

```yaml
applicant_playbook:
  name: "Value-Added Producer / Processor"
  parent_cic: TILTH-CIC-01  # Food Systems
  governing_filter: regenerative_relevance_filter

  eligibility_signals:
    - agricultural_commodity_control
    - processing_or_transformation_step
    - value_added_product
    - producer_income_logic
    - market_channel
    - food_safety_or_processing_readiness
    - business_plan_or_feasibility_support

  common_project_types:
    - feasibility_study
    - business_plan
    - marketing_plan
    - working_capital
    - processing_equipment
    - cold_storage_or_refrigeration
    - packaging_or_labeling_workflow
    - food_safety_market_access
    - direct_or_wholesale_market_expansion

  evidence_to_collect:
    - commodity_supply
    - product_description
    - production_capacity
    - processing_capacity
    - buyer_letters
    - revenue_history
    - cost_of_goods
    - pro_forma
    - break_even_analysis
    - vendor_quotes
    - food_safety_requirements
    - match_sources

  relevant_fid_funder_modules:
    - usda_vapg
    - pa_agricultural_innovation
    - pa_sbag_regenerative_subset

  grantwriter_translation:
    raw: "We want to make and sell a new product."
    translated: >
      The project converts an agricultural commodity under producer control into a
      value-added product with defined market channels, documented operational readiness,
      and a credible path to increased producer income.

  red_flags:
    - product_without_buyer
    - value_added_claim_without_producer_income_logic
    - processing_equipment_without_market_channel
    - working_capital_request_before_readiness
    - market_expansion_without_evidence
```

### A.3 Agricultural Innovation Implementer

```yaml
applicant_playbook:
  name: "Agricultural Innovation Implementer"
  parent_cic: TILTH-CIC-01  # Food Systems
  governing_filter: regenerative_relevance_filter

  eligibility_signals:
    - grows_or_processes_agricultural_commodity
    - provides_agricultural_technical_services
    - uses_agricultural_commodities_to_create_products_or_energy
    - project_located_in_or_supporting_pennsylvania_agriculture

  common_project_types:
    - precision_agriculture
    - robotics_or_ai_for_ag_operations
    - automation
    - diagnostics_and_data_collection
    - renewable_or_low_carbon_ag_energy
    - sorting_grading_processing_efficiency
    - biosecurity_or_plant_animal_health
    - farm_management_technology
    - labor_augmentation

  evidence_to_collect:
    - operational_problem_baseline
    - equipment_or_technology_specs
    - vendor_quote
    - installation_plan
    - timeline
    - cash_match
    - outputs_and_outcomes
    - five_innovation_principles_response
    - worker_protection_form_if_required

  relevant_fid_funder_modules:
    - pa_agricultural_innovation

  required_claim_chain:
    - challenge
    - innovation
    - implementation
    - measurable_improvement
    - pennsylvania_agriculture_benefit

  red_flags:
    - innovation_as_buzzword
    - technology_without_operational_problem
    - novelty_without_adoption_path
    - equipment_purchase_without_measurable_change
    - scalability_claims_without_small_or_medium_farm_relevance
```

### A.4 Regional Food Infrastructure / Cooperative

```yaml
applicant_playbook:
  name: "Regional Food Infrastructure / Cooperative"
  parent_cic: TILTH-CIC-01  # Food Systems
  governing_filter: regenerative_relevance_filter

  eligibility_signals:
    - cooperative_association
    - multiple_farms_or_businesses_impacted
    - regional_processing_or_distribution_problem
    - shared_asset_or_network_need
    - partner_roles

  common_project_types:
    - shared_processing
    - shared_cold_storage
    - food_hub_infrastructure
    - cooperative_sorting_grading_or_packing
    - regional_energy_or_biosecurity_system
    - mid_tier_value_chain
    - multi_farm_market_access
    - regional_technical_assistance

  evidence_to_collect:
    - partner_letters
    - farms_or_businesses_served
    - service_area
    - throughput_or_capacity_projection
    - governance_model
    - access_rules
    - regional_problem_statement
    - buyer_or_market_channel_evidence
    - implementation_timeline
    - match_or_financing_sources

  relevant_fid_funder_modules:
    - pa_agricultural_innovation
    - usda_vapg

  red_flags:
    - cooperative_claim_without_governance_model
    - regional_benefit_unmapped
    - throughput_projection_unsupported
    - partner_listed_without_role
```

### A.5 Agricultural Technical Assistance Provider

```yaml
applicant_playbook:
  name: "Agricultural Technical Assistance Provider"
  parent_cic: TILTH-CIC-01  # Food Systems
  governing_filter: regenerative_relevance_filter

  eligibility_signals:
    - provides_services_to_farmers
    - conservation_or_engineering_or_veterinary_or_farm_management_expertise
    - farmer_network
    - field_support_model
    - implementation_or_reporting_support

  common_project_types:
    - farmer_training
    - conservation_technical_assistance
    - innovation_planning
    - application_navigation
    - implementation_support
    - payment_or_reporting_support
    - community_science_coordination
    - peer_learning_network

  evidence_to_collect:
    - farmer_relationships
    - service_model
    - staff_or_advisor_expertise
    - outreach_plan
    - technical_curriculum
    - farmer_feedback
    - implementation_tracking
    - reporting_capacity

  relevant_fid_funder_modules:
    - sare_farmer
    - pa_agricultural_innovation

  language_seeds:
    - "farmer-facing technical assistance"
    - "implementation support"
    - "resource navigation"
    - "producer readiness"
    - "peer learning"
    - "field correction"

  red_flags:
    - ta_claim_without_farmer_relationships
    - curriculum_without_implementation_track
    - reporting_claim_without_capacity_evidence
```

### A.6 Urban Agriculture / Community Food

```yaml
applicant_playbook:
  name: "Urban Agriculture / Community Food"
  parent_cic: TILTH-CIC-01  # Food Systems
  governing_filter: regenerative_relevance_filter

  eligibility_signals:
    - urban_growing_site
    - community_food_access
    - land_tenure_or_site_control
    - soil_or_water_safety
    - neighborhood_relationships
    - stormwater_or_biodiversity_benefit
    - food_access_or_training_component

  common_project_types:
    - land_access_or_site_stabilization
    - soil_safety_or_testing
    - stormwater_management
    - hoop_house_or_season_extension
    - irrigation_or_water_efficiency
    - community_food_distribution
    - training_or_workforce_pathway
    - urban_agricultural_bmp

  evidence_to_collect:
    - site_plan
    - landowner_permission
    - soil_test_or_safety_data
    - community_partner_letters
    - stormwater_or_waterbody_info
    - photos
    - production_records
    - participant_or_beneficiary_data
    - maintenance_plan

  relevant_fid_funder_modules:
    - pa_agricultural_innovation
    - pa_sbag_regenerative_subset

  red_flags:
    - community_claim_without_relationship_evidence
    - food_access_claim_without_distribution_logic
    - land_tenure_unclear
    - soil_safety_unaddressed
```

### A.7 Regenerative Small Business Retrofit (SBAG-derived; scope-gated)

```yaml
applicant_playbook:
  name: "Regenerative Small Business Retrofit"
  parent_cic: TILTH-CIC-01  # Food Systems
  governing_filter: regenerative_relevance_filter  # MANDATORY — distinguishes from generic SBAG

  scope: >
    For farms, food businesses, processors, forestry/maple operations, cold-storage
    operators, local food distributors, compost/resource businesses, and land-based
    enterprises using measured equipment or process upgrades to reduce energy,
    water, waste, runoff, or pollution.

  eligibility_signals:
    - for_profit_small_business
    - pennsylvania_based_if_pa_sbag
    - regenerative_or_food_or_land_based_context
    - existing_equipment_or_process_baseline
    - proposed_replacement_or_upgrade
    - measurable_savings
    - reimbursement_readiness

  include_project_types:
    - agricultural_natural_resource_protection
    - farm_energy_efficiency
    - food_storage_refrigeration_efficiency
    - maple_reverse_osmosis_or_processing_efficiency
    - wash_pack_or_post_harvest_efficiency
    - water_or_wastewater_reduction_for_food_or_farm_processing
    - runoff_control
    - resource_efficiency_for_regenerative_operations

  exclude_project_types:
    # F-RELEVANCE-OUT-OF-VERTICAL fail-closed on any of these
    - medical_xray_scanner
    - generic_office_lighting
    - unrelated_retail_retrofit
    - generic_commercial_hvac
    - non_ag_manufacturing_without_regenerative_connection

  evidence_to_collect:
    - existing_process_description
    - utility_bill_or_resource_baseline
    - proposed_equipment_specs
    - vendor_quote
    - calculator_inputs
    - E_line_item_mapping
    - pre_project_photos
    - projected_annual_savings
    - one_year_followup_metric_plan

  relevant_fid_funder_modules:
    - pa_sbag_regenerative_subset

  red_flags:
    - retrofit_without_regenerative_context
    - baseline_unverified
    - calculator_not_tied_to_vendor_quote
    - savings_projection_without_measurement_plan
    - no_followup_metric_capacity
```

## 7. Annex B — evidence_grammar stubs

Seven evidence grammars. Each attaches orthogonally to multiple CICs and multiple CLCs. Per-grammar fields: name, attaches_to (CICs allowed to compose this grammar; default: all six), attaches_to_clcs (CLCs typically activating this grammar; non-restrictive hint, not a binding), evidence_classes, judge_checks where applicable, language_seeds where applicable.

### B.1 On-farm research

```yaml
evidence_grammar:
  name: "On-farm research"
  attaches_to_cics: all_six  # CIC-agnostic; farmers, schools, cooperatives, intermediaries all do field research
  typically_activates_clcs:  # non-restrictive hint
    - research_and_evidence
    - operating_capacity

  project_forms:
    - on_farm_experiment
    - demonstration
    - prototype
    - survey
    - field_observation
    - soil_health_benchmark
    - market_or_producer_research
    - community_science
    - farmer_led_data_collection

  evidence_classes:
    - research_question
    - hypothesis
    - treatment_or_comparison
    - field_notes
    - farm_records
    - soil_tests
    - production_records
    - yield_or_quality_data
    - labor_hours
    - energy_or_water_use
    - farmer_observation
    - technical_advisor_input
    - outreach_feedback
    - unexpected_results

  judge_checks:
    - question_is_measurable
    - method_answers_question
    - data_collection_is_realistic
    - timeline_matches_seasonality
    - claims_not_overstated
    - outreach_to_farmers_defined
    - useful_failure_can_be_reported
    - technical_advisor_role_is_credible

  language_seeds:
    - "farmer-led inquiry"
    - "field-tested"
    - "practical knowledge"
    - "community science"
    - "useful results"
    - "replicable learning"
    - "measured under real production conditions"
```

### B.2 Value-added business case

```yaml
evidence_grammar:
  name: "Value-added business case"
  attaches_to_cics: all_six  # cooperatives, food systems, intermediaries, public agencies (food-procurement); not just food systems
  typically_activates_clcs:
    - market_access
    - credit_and_underwriting

  value_added_chain:
    - commodity
    - producer_ownership_or_control
    - transformation_or_processing_step
    - value_added_product
    - buyer_or_market_channel
    - distribution_or_storage_strategy
    - margin_or_revenue_logic
    - producer_income_mechanism

  evidence_classes:
    - feasibility_study
    - business_plan
    - marketing_plan
    - buyer_letters
    - revenue_history
    - pro_forma
    - production_capacity
    - processing_capacity
    - storage_or_cold_chain_need
    - cost_of_goods
    - break_even_analysis
    - market_demand_signal

  red_flags:
    - product_without_buyer
    - value_added_claim_without_producer_income_logic
    - processing_equipment_without_market_channel
    - working_capital_request_before_readiness
    - market_expansion_without_evidence
```

### B.3 Ag innovation implementation

```yaml
evidence_grammar:
  name: "Ag innovation implementation"
  attaches_to_cics: all_six
  typically_activates_clcs:
    - catalytic_change
    - public_purpose_and_works
    - credit_and_underwriting

  innovation_types:
    - new_practice
    - improved_practice
    - new_market
    - new_supply_or_resource_pathway
    - improved_processing_or_sorting_method
    - farm_management_diagnostic_tool
    - low_or_no_carbon_energy_system
    - biosecurity_or_health_innovation
    - labor_augmentation_or_automation
    - cooperative_or_regional_operating_model

  required_claim_chain:
    - define_the_old_constraint
    - define_the_innovation_in_plain_operational_terms
    - prove_it_is_practical_not_futuristic_theater
    - show_who_can_use_or_replicate_it
    - identify_outputs_and_outcomes
    - tie_innovation_to_people_planet_profit

  five_innovation_principles:
    - relevant
    - practical
    - accessible
    - scalable
    - triple_bottom_line_aligned

  red_flags:
    - innovation_as_buzzword
    - technology_without_operational_problem
    - novelty_without_adoption_path
    - equipment_purchase_without_measurable_change
    - scalability_claims_without_small_or_medium_farm_relevance
```

### B.4 Regenerative pre/post savings

```yaml
evidence_grammar:
  name: "Regenerative pre/post savings"
  attaches_to_cics: all_six
  typically_activates_clcs:
    - credit_and_underwriting
    - public_purpose_and_works
  governing_filter: regenerative_relevance_filter  # mandatory — distinguishes from generic energy / efficiency programs

  evidence_classes:
    - existing_process_description
    - utility_bill_or_resource_baseline
    - proposed_equipment_specs
    - vendor_quote
    - calculator_inputs
    - E_line_item_mapping
    - pre_project_photos
    - projected_annual_savings
    - one_year_followup_metric_plan

  judge_checks:
    - baseline_is_documented
    - savings_projection_uses_calculator
    - calculator_ties_to_vendor_quote
    - eligible_costs_separated_from_ineligible
    - costs_occur_in_contract_period
    - followup_capacity_is_real

  red_flags:
    - baseline_unverified
    - calculator_not_tied_to_vendor_quote
    - savings_projection_without_measurement_plan
    - no_followup_metric_capacity
```

### B.5 Agricultural natural resource protection

```yaml
evidence_grammar:
  name: "Agricultural natural resource protection"
  attaches_to_cics: all_six
  typically_activates_clcs:
    - public_purpose_and_works
    - shared_assets

  evidence_classes:
    - watershed_or_waterbody_identified
    - soil_water_energy_or_waste_metric
    - bmp_plan
    - runoff_or_pollution_metric
    - conservation_partner_letter
    - public_agriculture_priority_area
    - environmental_justice_or_access_signal
    - regional_partner_or_multi_farm_benefit
    - state_or_federal_program_alignment

  language_seeds:
    - "watershed protection"
    - "soil and water resources"
    - "agricultural BMP"
    - "runoff control"
    - "regional conservation benefit"
```

### B.6 Market expansion / value chain

```yaml
evidence_grammar:
  name: "Market expansion / value chain"
  attaches_to_cics: all_six
  typically_activates_clcs:
    - market_access
    - shared_assets

  applies_to:
    - value_added_processing
    - maple_reverse_osmosis_or_processing_efficiency
    - cold_storage_or_refrigeration_efficiency
    - wash_pack_or_post_harvest_systems
    - cooperative_distribution
    - regional_processing
    - food_safety_market_access
    - direct_market_expansion
    - wholesale_or_institutional_market_entry
    - mid_tier_value_chain

  evidence_classes:
    - feasibility_study
    - business_plan
    - marketing_plan
    - buyer_letters
    - revenue_history
    - pro_forma
    - production_capacity
    - processing_capacity
    - storage_or_cold_chain_need
    - cost_of_goods
    - break_even_analysis
    - market_demand_signal
    - mid_tier_value_chain_partners
```

### B.7 Reimbursement & match readiness

```yaml
evidence_grammar:
  name: "Reimbursement & match readiness"
  attaches_to_cics: all_six
  typically_activates_clcs:
    - credit_and_underwriting

  underwriting_objects:
    - match_source
    - cash_match
    - in_kind_match_if_allowed
    - reimbursement_float_capacity
    - vendor_quote
    - itemized_invoice
    - project_budget
    - grant_calculator
    - business_plan
    - feasibility_study
    - pro_forma
    - payback_period
    - savings_projection
    - post_award_reporting_capacity

  judge_checks:
    - match_source_is_allowed
    - match_amount_meets_program_rule
    - applicant_can_pay_before_reimbursement
    - quote_items_match_budget_lines
    - eligible_and_ineligible_costs_separated
    - costs_occur_in_contract_period
    - payment_documentation_available
    - no_unallowable_costs_in_request
    - cash_flow_risk_disclosed
    - feasibility_evidence_matches_project_scale

  language_seeds:
    - "reimbursement readiness"
    - "cash match secured"
    - "eligible project costs"
    - "documented source and use of funds"
    - "cost basis"
    - "payback period"
    - "financial feasibility"
    - "budget-to-work-plan integrity"
```

## 8. Reference drawings

- **TILTH-CLC-00** — eight CLCs canonical drawing (Sovereign Node LLC, 2026). On disk at `assets/cards/capital_logic/Capital Logic Cards.png`.
- **TILTH-CIC-REVIEW-01** — six core customer worlds (CICs) canonical drawing (Sovereign Node LLC, 2026). On disk at `assets/cards/customer_identification/`.

Both drawings were re-shared by Josh in the 2026-05-16 conversation to confirm canonical names against the proposal's drift. Both match the canonical names used throughout this document.

## 9. Source

2026-05-16 Cowork dialogue between Josh and Claude over the regenerative-funder integration proposal Josh had prepared (SARE / PASA / VAPG / PA Agricultural Innovation / PA DEP SBAG synthesis).

Settled dispositions: funder-as-specimen thesis · asking/giving frame · card vocabulary retirement · CLC "-Capital" suffix drop · Urban Ag fold into Food Systems CIC · applicant_playbook and evidence_grammar and vertical_configuration as new primitives · F-RELEVANCE-* family · Wave 2 CLC deepening · funder dialect in FID (no card primitive) · mode router as code-time heuristic · single compound amendment as landing vehicle.

Operator-pinned lean: single compound amendment when triggered ("when we get there"). Not currently in L-005 pipeline.
