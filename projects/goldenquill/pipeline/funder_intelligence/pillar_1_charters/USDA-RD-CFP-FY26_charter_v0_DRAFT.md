# Depth Charter — `USDA-RD-CFP-FY26` (Community Facilities Program)

> **Pillar 1 of 4** per `pipeline/planning/funder_intelligence_database_research_project_2026-05-16.md` §3.1.
> **Quality bar** per `docs/FID_ARTIFACT_OPTIMIZATION_PRINCIPLES_2026-05-18.md` §1 + §2 + Codex framing.
> **Status: DEPTH CHARTER v0 (pre-corpus hypothesis; do not load as signed logic)** — re-authored to Codex yaml shape per operator directive 2026-05-18. Inherits USDA-RD funder depth charter.
>
> **Naming-collision note:** "CFP" inside USDA can refer to two distinct programs — (1) USDA-RD **Community Facilities Program** (essential community facilities in rural areas; 7 CFR Part 3570) and (2) USDA-NIFA **Community Food Projects** (food-security framing; entirely separate). **This charter scopes (1) only.**
>
> **[CONJECTURE — Pillar-2 corpus pending]** CFP FY26 framework not yet pulled. `F-FID-FACT-ORPHAN` enforces.

---

## Header

| Field | Value |
|------:|:------|
| `artifact_id` | `USDA-RD-CFP-FY26` |
| `artifact_family` | `program` |
| `funder_pointer` | `USDA-RD` |
| `version` | `depth_charter_v0` |
| `lifecycle` | `draft` |
| `phase` | `1 — exemplar pair` |
| `pillar_2_dispatch_position` | **3 of 6** |

---

## §A — Adversarial pre-checks

```yaml
runtime_consumer:
  scout:
    reads_fields: [scout_verify.live_check_url, eligibility_gates]
    stage: both
    decision_changed: "Scout DISCOVER restricts to applicants serving rural areas ≤20,000 population (CFP-specific threshold) + applicant in public body / nonprofit / federally-recognized tribe. VERIFY continuously-open program (not annual-cycle)."
  scribe:
    reads_fields: [scribe_section_requirements, scoring_rubric, drafting_implications]
    stage: both
    decision_changed: "Scribe leads §I with 'essential community facility' framing cited verbatim from USDA-RD definition; quantifies service-area median household income (MHI) for priority-points tier calculation; structures grant + loan blend strategy in §IV; documents Davis-Bacon prevailing-wage discipline when construction component; documents NEPA categorical-exclusion claim or EA/EIS scoping when ground-disturbing."
  judge:
    reads_fields: [scoring_rubric, judge_scoring_map]
    stage: rubric_scoring
    decision_changed: "Judge applies CFP priority-points framework (tiered to service-area MHI vs state non-metropolitan MHI). Higher MHI gap = higher priority points. Tie-breakers favor grant-loan-blend optimization + Davis-Bacon discipline + NEPA decision documented."
  red_team:
    reads_fields: [red_team_probes]
    stage: probe_target_selection
    decision_changed: "Red Team probes CFP-specific failure modes: essential-community-facility definition rigor (USDA-RD canonical test); rural ≤20K population threshold honesty; service-area MHI documentation discipline; Davis-Bacon trigger compliance when construction in scope; NEPA CE-vs-EA-vs-EIS decision tree."
  logician:
    reads_fields: [eligibility_gates, disqualifiers, logician_gates]
    stage: PRE
    decision_changed: "Logician fires F-CFP-RURAL-POP-INELIGIBLE (P0; service-area pop ≥20,000), F-CFP-NOT-ESSENTIAL-COMMUNITY-FACILITY (HIGH; project doesn't satisfy ECF definition), F-CFP-DAVIS-BACON-TRIGGER-MISS (HIGH; construction component + no prevailing-wage discipline), F-CFP-NEPA-CE-CLAIM-MISSING (HIGH; ground-disturbing activity + no NEPA decision documented)."
```

```yaml
artifact_must_not_contain:
  - facts belonging to another artifact          # USDA-RD funder + compliance cascades
  - applicant-specific claims
  - uncited generalizations
  - compliance framework internals               # Davis-Bacon + NEPA internals → compliance_cascades/
  - reviewer-type heuristics
  - case law interpretation
  - other USDA-RD programs
  - USDA-NIFA Community Food Projects (different program; naming-collision)
  - CFP loan-only awards detail (compliance + financial-officer territory)
  - cycles prior to FY26 except as historical-pattern
```

```yaml
strength_test:
  - "Name one concrete drafting decision this artifact changes."
  - "Name one proposal this artifact would reject or downgrade."
  - "Name one Red Team probe this artifact enables."
```

**Answers (PASSED):**

1. **Drafting decision.** Scribe writes the **service-area MHI vs state-non-metropolitan-MHI gap** explicitly in §II for priority-points tier calculation: *"Service area MHI = $[X]; PA non-metropolitan MHI = $[Y]; gap = [Z]%; this places applicant in priority-points Tier [N] per CFP framework."* Without artifact: priority-points tier omitted or qualitative; with artifact: quantified tier calculation that maps directly to grant/loan blend.
2. **Proposal rejected.** Logician `F-CFP-RURAL-POP-INELIGIBLE` (P0) fails closed any application where service-area population >20,000 (CFP-specific threshold; lower than RBDG's 50,000). Operator gets redirect-suggestion to RBDG (different population threshold) or other USDA-RD programs.
3. **Red Team probe.** `CFP-PROBE-DAVIS-BACON-TRIGGER-DISCIPLINE` asks: *"If project has construction component, is Davis-Bacon prevailing-wage discipline reflected in budget (weekly certified payrolls + wage determination + classification + apprenticeship-utilization)? Construction without Davis-Bacon documentation is HIGH-severity compliance audit risk + administrative-review return."*

---

## §B — Codex-shape depth-charter YAML

```yaml
artifact_id: USDA-RD-CFP-FY26
artifact_family: program
version: depth_charter_v0
lifecycle: draft
validation_status: pre_corpus_hypothesis
runtime_load_status: do_not_load_as_signed_logic
operator_label: depth_charter_v0

one_sentence_job: |
  Equip Scribe/Judge/Red Team/Logician with CFP FY26-specific eligibility
  (essential-community-facility + rural ≤20K population + public-body /
  nonprofit / tribe), priority-points MHI framework, grant-loan blend
  strategy, and Davis-Bacon + NEPA cascade integration.

runtime_consumers:
  scout:
    pre_filter_question: |
      Is the project located in a rural area ≤20,000 population (CFP rural-
      pop threshold), AND is the applicant in CFP's eligible applicant class
      (public body / nonprofit / federally-recognized Tribe), AND does the
      proposed facility satisfy the "essential community facility" definition?
    eligibility_dimensions:
      - rural_pop_threshold               # rural-area population ≤20,000 (CFP definition; per Pass-0 D-CFP boundary-inclusive)
      - eligible_applicant_class          # public body / nonprofit / federally-recognized Tribe
      - essential_community_facility      # facility satisfies ECF definition per 7 CFR 3570-B
      - mhi_priority_signal               # median household income gap drives priority-points tier (competitive scoring)
      - davis_bacon_nepa_triggers         # construction triggers Davis-Bacon + NEPA cascade
      - sam_uei_baseline                  # SAM-active + UEI present (inherits USDA-RD funder-wide)
    hard_gate_refs:
      - F-CFP-RURAL-POP-INELIGIBLE
      - F-CFP-INELIGIBLE-APPLICANT-CLASS
    cross_funder_signal: |
      Federal-program program-instance funder under USDA-RD funder-level.
      Routes opportunity LATERALLY to USDA-RD funder-level program portfolio
      (RBDG, RCDG, B&I Loan Guarantee) and TOWARD federal sister-programs
      (EDA Public Works, HUD CDBG) when CFP fit is borderline. Urban-area
      applicants routed AWAY from USDA-RD entirely.
    operator_assist_required: |
      Escalate to operator when: (a) essential-community-facility definition
      is borderline (F-CFP-NOT-ESSENTIAL-COMMUNITY-FACILITY HIGH fires)
      — operator must confirm facility classification, (b) Davis-Bacon
      trigger applies but applicant lacks prevailing-wage compliance posture
      (F-CFP-DAVIS-BACON-TRIGGER-MISS HIGH), (c) NEPA categorical exclusion
      claim missing (F-CFP-NEPA-CE-CLAIM-MISSING HIGH) — operator must
      confirm CE pathway with state RD office.
    source_authority: |
      USDA-RD Community Facilities Program 7 CFR 3570-B + FY26 NOFO
      (canonical reference §USDA-RD CFP rural-pop threshold + ECF definition).
      Rural-pop ≤20,000 source-pinned per Pass-0 D-CFP boundary-fix.
    prose_summary: |
      DISCOVER restricts to rural <20K + eligible-applicant + essential-community-
      facility framing.
  scribe:
    voice_change: |
      Inherits USDA-RD register; CFP-specific overlays: essential-
      community-facility (ECF) framing leads §I; MHI-gap quantification
      (service-area median household income vs state non-metropolitan MHI)
      drives priority-points tier in §II; grant-loan blend structured in
      §IV; Davis-Bacon prevailing-wage discipline + NEPA categorical-
      exclusion / EA / EIS scoping documented when construction +
      ground-disturbing activity present.
    section_ordering:
      - "§I essential-community-facility framing + rural ≤20,000 population eligibility (boundary-inclusive: 20,000 IS eligible)"
      - "§II MHI-gap quantification + community-support documentation + significant-community-support framing"
      - "§III project methodology + facility design + community-benefit narrative"
      - "§IV grant-loan blend budget + Davis-Bacon prevailing-wage discipline (when construction) + NEPA decision posture (CE / EA / EIS)"
      - "§V applicant qualifications + governing-body resolution"
      - "§VI work plan"
    must_do:
      - "Inherit USDA-RD scribe.must_do (rural-area citation, leveraging, public-purpose)."
      - "Lead §I with essential-community-facility (ECF) framing; cite USDA-RD ECF canonical definition."
      - "Quantify service-area MHI vs state non-metropolitan MHI in §II to surface priority-points tier (75% / 55% / 35% / 15% grant-share bands)."
      - "Document inability to obtain credit at commercially reasonable rates."
      - "Document significant community support (resolutions / petitions / public meetings)."
      - "When construction is in scope: document Davis-Bacon prevailing-wage discipline in §IV budget + narrative."
      - "When ground-disturbing activity in scope: document NEPA CE claim OR EA/EIS scoping in §IV."
    must_not_do:
      - "Inherit USDA-RD scribe.must_not_do (don't lead with 'innovative')."
      - "Confuse state non-metropolitan MHI with statewide MHI — comparator is state non-metro."
      - "Frame ≤20,000 as 'under 20,000' boundary-exclusive — 20,000 IS eligible per Pass-0 D-CFP fix."
      - "Skip Davis-Bacon discussion when construction is in scope."
      - "Skip NEPA discussion when ground-disturbing activity is in scope."
    cross_funder_signal: |
      Program-instance under USDA-RD; distinct from sister program-
      instances RBDG (small-and-emerging beneficiary) and RCDG (CDC
      identity). Davis-Bacon + NEPA compliance cascades fire on CFP
      more frequently than on RBDG / RCDG because CFP construction
      projects are common.
    source_authority: |
      USDA-RD CFP 7 CFR 3570-B + canonical reference §USDA-RD CFP
      (eligibility + MHI bands + significant community support +
      inability-to-obtain-credit + Davis-Bacon + NEPA). Boundary-
      inclusive ≤20,000 source-pinned per Pass-0 D-CFP boundary fix.
    prose_summary: |
      Leads §II with MHI-gap quantification for priority-points tier; structures
      grant-loan blend; documents Davis-Bacon + NEPA when triggered.

language_register_inheritance:
  parent_charter: USDA-RD
  inherits:
    - language_register.preferred_terms
    - language_register.suspicious_terms
    - language_register.sentence_shapes_that_work
    - language_register.sentence_shapes_that_fail
    - drafting_implications.scribe_must_do
    - drafting_implications.scribe_must_not_do
  cfp_specific_overlays:
    preferred_terms:
      - essential_community_facility
      - state_non_metropolitan_mhi
      - significant_community_support
      - inability_to_obtain_credit
      - davis_bacon
      - nepa_categorical_exclusion
    suspicious_terms:
      - statewide_mhi                        # CFP-specific reviewer-skepticism trigger; should be state_non_metropolitan_mhi
  note: |
    No standalone language_register / drafting_implications blocks. CFP
    inherits from USDA-RD funder-level + adds CFP-specific MHI / ECF /
    Davis-Bacon / NEPA overlays.
  judge: |
    Applies CFP priority-points framework tiered to MHI gap; tie-breakers
    favor grant-loan-blend optimization + Davis-Bacon discipline.
  red_team: |
    Probes essential-community-facility definition, rural-pop threshold,
    MHI documentation, Davis-Bacon trigger discipline, NEPA decision tree.
  logician: |
    PRE-gates F-CFP-RURAL-POP-INELIGIBLE (P0),
    F-CFP-NOT-ESSENTIAL-COMMUNITY-FACILITY (HIGH),
    F-CFP-DAVIS-BACON-TRIGGER-MISS (HIGH),
    F-CFP-NEPA-CE-CLAIM-MISSING (HIGH).

funder_pointer: USDA-RD
program_summary_one_paragraph: |
  USDA Rural Development's Community Facilities Program funds essential
  community facilities in rural areas ≤20,000 population — food hubs,
  community kitchens, processing-shared-asset construction, health clinics,
  libraries, public-safety facilities, etc. Triggers Davis-Bacon prevailing-
  wage cascade when construction involved + NEPA cascade when ground-
  disturbing. Mixed grant + direct-loan + guaranteed-loan structure tiered
  to service-area median household income.

nofo:
  source_url: <NEEDED Pillar 2 — CFP continuously-open program page>
  cycle_status: rolling   # CFP is continuously-open; not annual-cycle

eligibility_gates:
  - gate_id: F-CFP-RURAL-POP-INELIGIBLE
    gate_type: hard_eligibility_gate
    predicate: "Service-area population ≤20,000 per OMB-adjusted decennial census (CFP-specific threshold; 20,000 IS eligible)"
    machine_check:
      field_in_applicant_context: kfr.applicant.service_area_population
      operator: lte                                                # deprecated alias for less_or_equal per Discipline 3a.3
      threshold: 20000
    on_fail: REJECT_NO_DRAFT
    severity: P0
    source_required: true
    corpus_ref: 7_cfr_3570.pdf:§eligibility
    confidence:
      level: medium
      reason: "20,000-population ceiling + boundary-inclusive (20,000 IS eligible) is canonical-reference-doc anchored (§USDA-RD CFP Eligibility) + Pass-0 D-CFP boundary fix; 7 CFR 3570 citation present pre-Pass-2"
      promotion_requirement: "7 CFR 3570 §eligibility verbatim text ingested at Pillar-2"
  - gate_id: F-CFP-INELIGIBLE-APPLICANT-CLASS
    gate_type: hard_eligibility_gate
    predicate: "Applicant in {public_body, nonprofit, federally_recognized_tribe}"
    machine_check:
      operator: in
      threshold: [public_body, nonprofit, federally_recognized_tribe]
    on_fail: REJECT_NO_DRAFT
    severity: P0
    source_required: true
    corpus_ref: "<NEEDED — Pillar 2: 7 CFR 3570 applicant-type section>"
    confidence:
      level: medium
      reason: "Applicant-type roster canonical-reference-doc anchored (§USDA-RD CFP Eligibility Applicant types); pinpoint 7 CFR 3570 citation pending"
      promotion_requirement: "7 CFR 3570 applicant-type section verbatim ingested at Pillar-2"
  - gate_id: F-CFP-NOT-ESSENTIAL-COMMUNITY-FACILITY
    gate_type: competitive_scoring_signal
    predicate: "Project satisfies USDA-RD essential-community-facility definition"
    machine_check:
      operator: matches                                            # composite-shape check; decompose at future pass
      threshold: { satisfies_ecf_canonical_test: true }
    on_fail: WARN_OPERATOR
    severity: HIGH
    source_required: true
    corpus_ref: "<NEEDED — Pillar 2: USDA-RD essential-community-facility canonical definition>"
    confidence:
      level: medium
      reason: "ECF canonical test anchored in §USDA-RD CFP Purpose enumeration; verbatim definition pending"
      promotion_requirement: "USDA-RD essential-community-facility canonical definition ingested at Pillar-2"
    pass_1_reconciliation_note: "Purpose-wise this is eligibility verification (verify_required_gate semantics); fail_action WARN_OPERATOR + severity HIGH classifies as competitive_scoring_signal per Discipline 3a.4. Migrating to HOLD_FOR_OPERATOR_REVIEW is a fail_action-semantic change Pass 1 is not authorized to make; flag for operator review."

scoring_rubric:
  framework: priority_points_tiered_to_mhi_gap
  description: |
    CFP uses priority-points framework tiered to service-area MHI vs state
    non-metropolitan MHI. Lower MHI gap = lower priority. Tiered grant /
    loan / guaranteed-loan blend; lower-MHI applicants get higher grant
    percentage.

scribe_section_requirements:
  - nofo_section_id: §II  # Service Area + MHI
    drafting_decisions:
      - decision: "Quantify service-area MHI vs state non-metropolitan MHI gap explicitly; map to priority-points tier."
        rationale: "Priority-points tier directly determines grant-vs-loan blend; quantification required."
  - nofo_section_id: §IV  # Budget + Funding Structure
    drafting_decisions:
      - decision: "Structure grant + direct-loan + guaranteed-loan blend per priority-points tier."
        rationale: "Optimization of grant percentage vs loan-debt service is strategic lever; not optional."
  - nofo_section_id: §V  # Construction (if applicable)
    drafting_decisions:
      - decision: "If construction in scope, document Davis-Bacon prevailing-wage discipline in budget: weekly certified payrolls + wage determination per locality + classifications + apprenticeship utilization."
        rationale: "Davis-Bacon trigger is automatic on CFP construction; absence = HIGH-severity compliance flag."
      - decision: "Document NEPA decision: categorical exclusion claim with rationale OR EA/EIS scoping with timeline."
        rationale: "NEPA decision required on ground-disturbing; missing = HIGH-severity Red Team flag."

evidence_ladder:
  strongest:
    - "Service-area MHI cited from PA-Census + state non-metropolitan MHI baseline"
    - "Architect/engineer cost estimate with construction-discipline breakdown"
    - "Davis-Bacon wage determination obtained for project locality"
    - "NEPA categorical-exclusion checklist or EA scoping document"
    - "Prior USDA-RD CFP track record"
  acceptable:
    - "Service-area MHI from PA-Census without state-non-metropolitan baseline cross-reference"
    - "Cost estimate without Davis-Bacon breakdown (but trigger acknowledged)"
    - "NEPA decision narrative without checklist"
  weak:
    - "Service-area MHI handwave"
    - "Construction component without Davis-Bacon mention"
    - "Ground-disturbing without NEPA decision"
  unacceptable:
    - "Service area >20,000 population (administrative rejection)"
    - "Construction with no compliance discipline"
    - "Project not satisfying essential-community-facility definition"

red_team_probes:
  - probe_id: CFP-PROBE-DAVIS-BACON-TRIGGER-DISCIPLINE
    probe_question: "If construction component, is Davis-Bacon prevailing-wage discipline in budget (weekly payrolls + wage determination + classifications + apprenticeship)?"
    score_impact_if_fails: "HIGH compliance flag + admin return"
  - probe_id: CFP-PROBE-NEPA-DECISION-DOCUMENTED
    probe_question: "If ground-disturbing, is NEPA decision documented (CE claim with rationale OR EA/EIS scoping)?"
    score_impact_if_fails: "HIGH compliance flag + admin return"
  - probe_id: CFP-PROBE-MHI-DOCUMENTATION
    probe_question: "Is service-area MHI quantified vs state non-metropolitan MHI baseline for priority-points calculation?"
    score_impact_if_fails: "-3 to -5 + reviewer can't calculate priority-points tier"
  - probe_id: CFP-PROBE-RURAL-20K-THRESHOLD
    probe_question: "Service-area population ≤20,000? (CFP threshold; 20,000 IS eligible. NOT RBDG's 50,000.)"
    score_impact_if_fails: ADMINISTRATIVE_REJECTION

logician_gates:
  - gate_id: F-CFP-DAVIS-BACON-TRIGGER-MISS
    gate_type: competitive_scoring_signal
    when: PRE
    severity: HIGH
    predicate_python: "draft.has_construction_component() == True AND not draft.budget_includes_davis_bacon_discipline()"
    fail_action: WARN_OPERATOR
    source_required: true
    corpus_ref: pending_pillar_2  # Davis-Bacon Act 40 USC 3141-48 + USDA-RD CFP construction guidance (inherits USDA-RD funder gate)
    confidence:
      level: medium
      reason: "Inherits USDA-RD funder gate F-USDA-RD-DAVIS-BACON-TRIGGER-MISS; canonical-reference-doc anchored (§USDA-RD CFP Requirements)"
      promotion_requirement: "Davis-Bacon Act + USDA-RD CFP construction-guidance pinpoint ingested at Pillar-2"
    pass_1_reconciliation_note: "Inherits USDA-RD funder F-USDA-RD-DAVIS-BACON-TRIGGER-MISS. Pass 6 (inheritance) considers whether this program-level gate is redundant."
  - gate_id: F-CFP-NEPA-CE-CLAIM-MISSING
    gate_type: competitive_scoring_signal
    when: PRE
    severity: HIGH
    predicate_python: "draft.has_ground_disturbing_activity() == True AND draft.nepa_decision is None"
    fail_action: WARN_OPERATOR
    source_required: true
    corpus_ref: pending_pillar_2  # NEPA + 7 CFR 1970 (inherits USDA-RD funder gate)
    confidence:
      level: medium
      reason: "Inherits USDA-RD funder gate F-USDA-RD-NEPA-CE-CLAIM-MISSING; canonical-reference-doc anchored (§USDA-RD CFP Requirements)"
      promotion_requirement: "7 CFR 1970 USDA-RD environmental policy text ingested at Pillar-2"
    pass_1_reconciliation_note: "Inherits USDA-RD funder F-USDA-RD-NEPA-CE-CLAIM-MISSING. Pass 6 (inheritance) considers whether this program-level gate is redundant."

source_backing:
  corpus_refs:
    - "<NEEDED — Pillar 2: CFP FY26 program-overview docs>"
    - "<NEEDED — Pillar 2: 7 CFR Part 3570 regulatory text>"
    - "<NEEDED — Pillar 2: USDA-RD essential-community-facility canonical definition>"
    - "<NEEDED — Pillar 2: FY24 + FY25 CFP grant+loan award rosters>"
    - "<NEEDED — Pillar 2: Davis-Bacon trigger guidance + NEPA CE-vs-EA decision-tree>"
  confidence: LOW pre-corpus.
  unresolved_questions:
    - "Current priority-points tier MHI gap thresholds"
    - "FY26 grant cap variance by tier"
    - "Recent FY24-FY25 CFP grant-vs-loan blend distributions"
```

---

## §1 — What "depth" means for THIS artifact

CFP FY26 program-level depth is the **essential-community-facility decision substrate** — eligibility (rural <20K + applicant class + ECF definition), priority-points MHI framework, grant-loan blend strategy, Davis-Bacon + NEPA cascade integration. Distinct from RBDG/RCDG on rural-pop threshold (20K vs 50K) and on compliance-cascade complexity (Davis-Bacon + NEPA both triggered).

**Codex same-prompt-with/without test:**
- **Without** — Scribe writes generic rural-facility proposal. No MHI calculation. No Davis-Bacon discipline. No NEPA decision.
- **With** — Scribe quantifies MHI gap → priority-points tier → grant/loan blend in §II + §IV; documents Davis-Bacon in §V when construction; documents NEPA decision when ground-disturbing. Judge applies CFP priority-points framework. Red Team probes Davis-Bacon + NEPA discipline. Logician fails closed on ≥20K pop + ECF-mismatch + Davis-Bacon-trigger-miss + NEPA-decision-missing.

---

## §2 — Primary sources in scope

| Corpus | Sources | Path | Count |
|--------|---------|------|-------|
| `nofos/` | CFP FY26 program-overview + Federal Register notices | USDA-RD + Federal Register | 2-4 |
| `regulatory/` | 7 CFR Part 3570 | Federal Register | 1-2 |
| `awards/` | FY24 + FY25 CFP rosters (grant + loan); PA-specific; food-systems-adjacent | USAspending.gov + USDA-RD | 2-3 |
| `guidance/` | Essential-community-facility definition; Davis-Bacon trigger; NEPA CE/EA decision tree | USDA-RD public guidance | 2-4 |

Case law OUT OF SCOPE.

---

## §3 — Tier classification

| Field | Tier |
|-------|:----:|
| Default | `1` |
| `eligibility_rules[]` | `1` |
| `priority_points_framework[]` | `1` |
| `loan_grant_blend_strategy_notes[]` | `2` |
| `reviewer_relationship_notes[]` | `3` |
| `davis_bacon_trigger_notes[]` | `1` |

---

## §4 — Refresh cadence

`quarterly` — CFP is continuously-open (not annual NOFO). Recheck against Federal Register on ECF definition + priority-points tier MHI thresholds.

---

## §5 — Calibration applicant pair

`food_systems` (CIC-01) × `operating_capacity` (CLC-03), with Shared Assets (CLC-08) overlay for food-hub / community-kitchen / processing-shared-asset framing.

---

## §6 — Done definition

`audited` per SARE-NE / USDA-RD discipline; Davis-Bacon + NEPA compliance-cascade pointers resolve at L-005.

---

## §7 — Operator signature

```yaml
charter_signed_at: <pending_operator_attestation>
charter_signed_by_pubkey: <pending_operator_attestation>
charter_signed_canonical_bytes_sha3_512: <pending_operator_attestation>
charter_ed25519_signature: <pending_operator_attestation>
```

---

## §8 — Out of scope

- USDA-NIFA Community Food Projects — DIFFERENT program (naming-collision)
- Other USDA-RD programs (RBDG, RCDG, B&I) — separate artifacts
- CFP loan-only awards detail (compliance + financial-officer territory)
- Davis-Bacon compliance internals (→ `compliance_cascades/DAVIS-BACON-PREVAILING-WAGE.yaml` or PRP cross-cutting)
- NEPA compliance internals (→ `compliance_cascades/NEPA-CATEGORICAL-EXCLUSIONS.yaml` or PRP)
- Reviewer-type heuristics (→ `reviewer_heuristics/federal-program-officer.yaml`)
- Per-applicant service-area MHI calculation (→ `orgs/<slug>/`)
- Case law interpretation
