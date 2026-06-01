# Test scenario authoring schema

Each test scenario is a self-contained YAML file at `pipeline/cards/eval/scenarios/<scenario_slug>.yaml` describing one fictional-applicant + real-opportunity pair. Identical scenarios are run through all three arms (A, B, C) per §18.19.1.

## Required fields

```yaml
scenario_slug: "mushroom_coop_pa_operating_capacity"
scenario_kind: "synthetic"                    # synthetic | permission_based_real
authored_at: "2026-MM-DDTHH:MM:SSZ"
authored_by_role: "platform_team"

cic_assignment:
  primary_cic_slug: "cooperative"             # one of the six canonical slugs
  secondary_cic_slug: "food_systems"          # optional — for multi-axis applicants

clc_assignment:
  primary_clc_slug: "operating_capacity"      # one of the eight canonical slugs

opportunity:
  funder_name: "USDA Rural Cooperative Development Grant"
  opportunity_type: "federal_nofo"            # federal_nofo | foundation_rfa | state_rfa | corporate_rfp | cdfi_loan_app
  nofo_or_rfa_url: "https://..."              # public-domain source
  award_range_usd:
    min: 50000
    max: 250000
  due_date: "2026-MM-DD"
  application_length_pages: 25
  funder_rubric_path: "pipeline/rubrics/<funder>_<year>.json"  # if rubric is in library; otherwise null

fictional_applicant:
  organization_name: "Mycelium Commons Cooperative LLC"   # NOT a real organization
  legal_structure: "Worker cooperative LLC, Pennsylvania"
  ein: "FICTIONAL-EIN-PLACEHOLDER"            # NOT a real EIN
  uei: "FICTIONAL-UEI-PLACEHOLDER"
  founded: 2024
  member_count: 12
  annual_revenue_usd: 380000
  service_area: "Lehigh Valley, Pennsylvania"
  brief_description: "A 12-member worker cooperative growing specialty mushrooms..."

kfr_seed_facts:
  # Fictional applicant fact-sheet content the applicant would supply at Intake.
  # Same structure as a real org's PROJECT_CONTEXT.md — fictional values throughout.
  - fact_class: "land_tenure"
    value: "Lease + option to purchase, 8.5 acres"
    provenance: "Synthetic — scenario authoring time"
  - fact_class: "annual_revenue"
    value: "$380,000 (2025), $425,000 projected (2026)"
    provenance: "Synthetic"
  # ... full KFR seeded as the scenario requires

ground_truth_expected_behaviors:
  # What a competent human grant writer would do for this scenario.
  # Used to author the reviewer-panel rubric, NOT used by Judge directly.
  expected_search_vocabulary:
    - "cooperative development"
    - "value-added agriculture"
    - "rural business"
  expected_evidence_emphasis:
    - "Member commitments + governance documentation"
    - "Capitalization plan + match documentation"
    - "Production capacity proof"
  expected_red_flags_to_address:
    - "Governance immaturity (founded 2024)"
    - "Member-class conflict risk"
  expected_funder_language_register: "movement_aligned + technical_precise hybrid"

review_dimensions:
  # The rubric dimensions reviewers score. Drawn from active CLC's
  # underwriting_criteria + reviewer_profile_typical.reviewer_priorities +
  # common_red_flags, PLUS the funder rubric's actual scoring weights.
  - dimension: "Capacity bottleneck clarity"
    source: "TILTH-CLC-03 operating_capacity.underwriting_criteria.capacity_bottleneck"
    scoring_scale: "0-5"
  - dimension: "Mission relationship articulated"
    source: "TILTH-CLC-03 operating_capacity.underwriting_criteria.mission_relationship"
    scoring_scale: "0-5"
  # ... full dimension list

pre_registered_primary_outcome_measure:
  measure: "Mean per-dimension score across all dimensions (Arm B − Arm A)"
  pre_registered_threshold_for_significance: 0.5    # half-point per dimension
  statistical_test: "Paired t-test or Wilcoxon signed-rank per reviewer"
  pre_registered_at: "2026-MM-DDTHH:MM:SSZ"
  pre_registration_url: "https://osf.io/<registration_id>"   # OSF preregistration or equivalent
```

## Scenario authorship rules

1. **Synthetic only at v0.1/v0.2.** Permission-based real-applicant scenarios require explicit consent + IRB-equivalent review.
2. **No leakage from operator's customer fleet.** Fictional applicant names, EINs, UEIs, addresses, and service areas must NOT match any real operator-customer. Cross-check at scenario-authoring time.
3. **Real opportunities only.** Use public-domain NOFOs/RFAs that were open during the study window or recently closed. Fictional funders would not produce realistic reviewer behavior.
4. **Funder rubric grounding.** Where a funder's rubric is in `pipeline/rubrics/` library, link it. Where not, scenario must document what the realistic rubric would look like based on funder type + opportunity kind.
5. **Pre-register before reviewers see drafts.** No HARKing.
6. **Coverage discipline.** Aim for one scenario per CIC at minimum; one scenario per CLC at minimum; multiple scenarios per high-volume intersection (food_systems × operating_capacity, food_systems × market_access, food_systems × catalytic_change as the operator's actual customer-pipeline priority).

## Forbidden content

- Real operator-customer organization names, EINs, UEIs, addresses, or any PII-equivalent identifier.
- Any KFR seed fact copied verbatim from an existing `orgs/<slug>/PROJECT_CONTEXT.md`.
- Funder-rubric content not yet locked in `pipeline/rubrics/` (avoid drift between scenario rubric expectations and rubric library ground truth).
- Pre-registration date later than first-reviewer-drafts-distribution date (HARKing protection).
