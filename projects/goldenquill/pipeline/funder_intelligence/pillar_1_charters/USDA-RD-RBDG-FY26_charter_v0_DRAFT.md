# Depth Charter — `USDA-RD-RBDG-FY26` (Rural Business Development Grant)

> **Pillar 1 of 4** per `pipeline/planning/funder_intelligence_database_research_project_2026-05-16.md` §3.1.
> **Quality bar** per `docs/FID_ARTIFACT_OPTIMIZATION_PRINCIPLES_2026-05-18.md` §1 + §2 + Codex framing.
> **Status: DEPTH CHARTER v0 (pre-corpus hypothesis; do not load as signed logic)** — re-authored to Codex yaml shape per operator directive 2026-05-18. Inherits USDA-RD funder-level depth-charter (commit 071408b) for cross-program register + cascade defaults.
>
> **[CONJECTURE — Pillar-2 corpus pending]** RBDG FY26 NOFO not yet pulled; rubric weights + cap + cycle dates [CONJECTURE] until corpus. `F-FID-FACT-ORPHAN` enforces.

---

## Header

| Field | Value |
|------:|:------|
| `artifact_id` | `USDA-RD-RBDG-FY26` |
| `artifact_family` | `program` |
| `funder_pointer` | `USDA-RD` |
| `version` | `depth_charter_v0` |
| `lifecycle` | `draft` |
| `phase` | `1 — exemplar pair` |
| `pillar_2_dispatch_position` | **1 of 6** (methodology anchor) |

---

## §A — Adversarial pre-checks

```yaml
runtime_consumer:
  scout:
    reads_fields: [scout_verify.live_check_url, eligibility_gates, nofo.cycle_status]
    stage: both
    decision_changed: "Scout DISCOVER pre-filters applicants with service-area population ≤50,000 (rural-area threshold) AND applicant entity in {rural_public_body, rural_serving_nonprofit, federally_recognized_tribe}. Scout VERIFY checks FY26 NOFO URL returns 200 + 'FY26' literal + non-past closing_date."
  scribe:
    reads_fields: [scribe_section_requirements, scoring_rubric, drafting_implications]
    stage: both
    decision_changed: "Scribe leads §I with rural-prosperity framing + named PA rural county + economic-impact-theory-of-change; leads match-narrative section (§IV) with CASH match ordered before in-kind; quantifies jobs in FTE + counting-period + verification-path; distinguishes applicant (rural body / nonprofit / tribe) from beneficiary (small + emerging private business) explicitly."
  judge:
    reads_fields: [scoring_rubric, judge_scoring_map]
    stage: rubric_scoring
    decision_changed: "Judge applies RBDG-specific 5-criterion weighted rubric (Leveraging / Economic Impact / Sustainability / Applicant Capacity / Project Rationale) instead of generic 12-dimension Tilth scoring. Tie-breakers favor cash-match-≥50%-with-unconditional-commitments and FTE-methodology-explicit."
  red_team:
    reads_fields: [red_team_probes, known_failure_modes_from_prior_cycles]
    stage: probe_target_selection
    decision_changed: "Red Team probes RBDG-specific failure modes: match-fund authenticity (unconditional vs contingent), rural-population threshold honesty, beneficiary-class authenticity (Enterprise vs Opportunity track distinction), sub-recipient monitoring (2 CFR 200.332), budget-tie-mismatch (line items must sum to declared total)."
  logician:
    reads_fields: [eligibility_gates, disqualifiers, logician_gates]
    stage: PRE
    decision_changed: "Logician fires F-RBDG-RURAL-POP-INELIGIBLE (P0; service-area pop >50,000), F-RBDG-INELIGIBLE-APPLICANT-CLASS (P0; applicant not in rural public body / rural-serving nonprofit / federally-recognized tribe), F-RBDG-MATCH-CONTINGENT-LEAK (HIGH), F-RBDG-BENEFICIARY-NOT-SMALL-AND-EMERGING (HIGH; <50 new employees AND <$1M projected annual gross revenue both required), F-RBDG-BUDGET-TIE-MISMATCH (HIGH; POST-gate)."
```

```yaml
artifact_must_not_contain:
  - facts belonging to another artifact          # USDA-RD funder-level → funders/USDA-RD.yaml
  - applicant-specific claims
  - uncited generalizations
  - compliance framework internals               # 2 CFR 200, Davis-Bacon → compliance_cascades/
  - reviewer-type heuristics
  - case law interpretation
  - other USDA-RD programs                       # RCDG / CFP / B&I = separate
  - cycles prior to FY26 except as historical-pattern reference
```

```yaml
strength_test:
  - "Name one concrete drafting decision this artifact changes."
  - "Name one proposal this artifact would reject or downgrade."
  - "Name one Red Team probe this artifact enables."
```

**Answers (PASSED — §1 + §B realize concretely):**

1. **Drafting decision.** Scribe leads RBDG match-narrative section (NOFO §IV-B) with **CASH match commitments before in-kind**, ordered: cash → documented-third-party-in-kind → applicant-confirmed-in-kind. Rubric criterion #3 "Leveraging" awards full points to documented cash + third-party-verified in-kind, zero/partial to unverified in-kind. Without artifact: Scribe orders match by largest dollar regardless of composition.
2. **Proposal rejected.** Logician `F-RBDG-RURAL-POP-INELIGIBLE` (P0) fails closed any applicant where service-area population (decennial-census + OMB-adjusted) >50,000. Scribe never invoked; operator gets redirect-suggestion to USDA-RD-RBIG (different population threshold) or non-USDA-RD program.
3. **Red Team probe.** `RBDG-PROBE-MATCH-AUTHENTICITY` asks: *"For each match commitment, is it UNCONDITIONAL or CONTINGENT on RBDG award? Per 7 CFR 4280-E + NOFO §V.C.3, contingent matches zero-weight in leverage scoring regardless of dollar."*

---

## §B — Codex-shape depth-charter YAML

```yaml
artifact_id: USDA-RD-RBDG-FY26
artifact_family: program
version: depth_charter_v0
lifecycle: draft
validation_status: pre_corpus_hypothesis
runtime_load_status: do_not_load_as_signed_logic
operator_label: depth_charter_v0

one_sentence_job: |
  Equip Scribe / Judge / Red Team / Logician with RBDG FY26-specific eligibility
  predicates, 5-criterion weighted rubric, match-narrative discipline, and
  Enterprise-vs-Opportunity activity-track distinction — methodology-anchor
  program for the FID program-artifact family.

runtime_consumers:
  scout:
    pre_filter_question: |
      Is the project located in a rural area ≤50,000 population (RBDG rural-
      pop threshold, boundary-inclusive `lte`), AND is the applicant in
      RBDG's eligible class (public body / nonprofit / federally-recognized
      Tribe), AND does the project serve small-and-emerging private business
      beneficiaries?
    eligibility_dimensions:
      - rural_pop_threshold               # rural-area population ≤50,000 (RBDG; boundary-inclusive per Pass-0)
      - eligible_applicant_class          # public body / nonprofit / federally-recognized Tribe
      - small_and_emerging_beneficiary    # private businesses ≤50 new employees AND projected annual gross revenue <$1M
      - cash_match_signal                 # competitive scoring per match_logic.required_match: false (Pass-0 D-RBDG fix)
      - sam_uei_baseline                  # SAM-active + UEI present
    hard_gate_refs:
      - F-RBDG-RURAL-POP-INELIGIBLE
      - F-RBDG-INELIGIBLE-APPLICANT-CLASS
    cross_funder_signal: |
      Federal-program program-instance funder under USDA-RD funder-level.
      Routes opportunity LATERALLY to other USDA-RD program-instances (CFP,
      RCDG, B&I Loan Guarantee, REAP) when applicant + project profile
      better fits another program. Routes TOWARD SBA programs when business-
      development focus dominates over rural-development focus.
    operator_assist_required: |
      Escalate to operator when: (a) match commitments are contingent
      (F-RBDG-MATCH-CONTINGENT-LEAK HIGH fires) — operator confirms
      unconditional posture, (b) beneficiary class is borderline
      (F-RBDG-BENEFICIARY-NOT-SMALL-AND-EMERGING fires — composite predicate
      flagged Pass-1 P1-5 for decomposition), (c) budget tie mismatch
      between narrative and budget (POST-gate F-RBDG-BUDGET-TIE-MISMATCH
      fires).
    source_authority: |
      USDA-RD RBDG 7 CFR 4280-E + FY26 NOFO (canonical reference §USDA-RD
      RBDG rural-pop threshold + small-and-emerging-beneficiary test).
      Rural-pop ≤50,000 source-pinned. Cash-match-≥50% reconciled at Pass-1
      as competitive-factor not hard requirement per Pass-0 D-RBDG.
    prose_summary: |
      DISCOVER pre-filters rural-pop ≤50k + applicant entity-type; VERIFY checks
      FY26 NOFO URL + 'FY26' literal + non-past closing_date.
  scribe:
    voice_change: |
      Inherits USDA-RD register (rural-prosperity + leveraging + FTE-
      quantified economic impact + public-purpose for nonprofit/tribal).
      RBDG-specific overlays: small-and-emerging-beneficiary class
      (≤50 new employees, <$1M projected annual gross revenue);
      "Enterprise Grants" vs "Opportunity Grants" track distinction;
      cash-first match ordering in §IV (per Pass-0 D-RBDG —
      match is competitive-factor not hard requirement).
    section_ordering:
      - "§I rural-prosperity + economic-impact theory-of-change + small-and-emerging-beneficiary framing"
      - "§II FTE-quantified jobs (created + retained separate methodologies)"
      - "§III public-purpose justification (nonprofit/tribal applicants)"
      - "§IV match narrative — CASH-FIRST ordering; flag any contingent commitments explicitly"
      - "§V applicant qualifications + Enterprise-vs-Opportunity track justification"
      - "§VI work plan + sub-recipient monitoring posture"
    must_do:
      - "Inherit USDA-RD scribe.must_do (rural-prosperity §I, FTE jobs, public-purpose for nonprofits/tribes)."
      - "Lead §IV match narrative with CASH commitments before in-kind; flag contingent commitments explicitly."
      - "Verify beneficiary small-and-emerging definition (<50 new employees AND <$1M projected annual gross revenue) when describing project beneficiaries."
      - "Choose Enterprise Grant (capital equipment + working capital TA) vs Opportunity Grant (broader rural community econ-dev TA) explicitly in §V."
    must_not_do:
      - "Inherit USDA-RD scribe.must_not_do (don't conflate jobs-created/retained; don't lead with 'innovative'; don't mix applicant-vs-beneficiary identity)."
      - "Frame match as a hard ≥50% requirement — Pass-0 D-RBDG demoted match to competitive-factor; required_match: false."
      - "Aggregate Enterprise + Opportunity narratives — pick a track."
    cross_funder_signal: |
      Program-instance under USDA-RD. Inherits funder-level register
      with RBDG-specific small-and-emerging overlay. Distinct from
      sister USDA-RD program-instances RCDG (cooperative-form first)
      and CFP (essential-community-facility first).
    source_authority: |
      USDA-RD RBDG 7 CFR 4280-E + canonical reference §USDA-RD RBDG.
      Inherits USDA-RD funder-level scribe register source-authority.
      Cash-match competitive-factor posture source-backed per Pass-0
      D-RBDG harm-prevention fix.
    prose_summary: |
      Reads scribe_section_requirements + scoring_rubric + drafting_implications;
      leads §I with rural-prosperity + economic-impact-theory-of-change; leads
      §IV match with CASH-first ordering; FTE-quantified jobs.

language_register_inheritance:
  parent_charter: USDA-RD
  inherits:
    - language_register.preferred_terms
    - language_register.suspicious_terms
    - language_register.sentence_shapes_that_work
    - language_register.sentence_shapes_that_fail
    - drafting_implications.scribe_must_do
    - drafting_implications.scribe_must_not_do
  rbdg_specific_overlays:
    preferred_terms:
      - small_and_emerging_businesses
      - enterprise_grant
      - opportunity_grant
    suspicious_terms:
      - aggregate_jobs_count                  # RBDG-specific reinforcement
  note: |
    No standalone language_register / drafting_implications blocks in this
    charter — RBDG inherits from USDA-RD funder-level. Program-specific
    overlays scoped above are operator-derived heuristics pending Pillar-2.
  judge: |
    Applies 5-criterion weighted rubric (Leveraging / Economic Impact /
    Sustainability / Applicant Capacity / Project Rationale).
  red_team: |
    Probes match-fund authenticity, rural-pop honesty, beneficiary-class
    authenticity, sub-recipient monitoring, budget-tie-mismatch.
  logician: |
    PRE-gates F-RBDG-RURAL-POP-INELIGIBLE / INELIGIBLE-APPLICANT-CLASS /
    MATCH-CONTINGENT-LEAK / BENEFICIARY-NOT-SMALL-AND-EMERGING /
    BUDGET-TIE-MISMATCH (POST).

funder_pointer: USDA-RD
program_summary_one_paragraph: |
  USDA Rural Development's Rural Business Development Grant funds rural public
  bodies, rural-serving nonprofits, and federally-recognized tribes to provide
  TA, training, or other activities developing/financing small + emerging
  private businesses in rural areas. Two tracks: Enterprise Grants (capital
  equipment + working capital for individual small businesses through grantee
  TA program) and Opportunity Grants (broader rural-community econ-dev TA —
  incubators, business plan training, market studies).

nofo:
  source_url: "<NEEDED — Pillar 2: Grants.gov FY26 synopsis URL>"
  source_pdf_sha256: <NEEDED Pillar 2>
  posted_date: <NEEDED Pillar 2>
  closing_date: <NEEDED Pillar 2>
  cycle_status: <NEEDED — expected open at posting>

eligibility_gates:
  - gate_id: F-RBDG-RURAL-POP-INELIGIBLE
    gate_type: hard_eligibility_gate
    predicate: "Service-area population ≤50,000 per OMB-adjusted decennial census"
    machine_check:
      field_in_applicant_context: kfr.applicant.service_area_population
      operator: lte                                                # deprecated alias for less_or_equal per Discipline 3a.3
      threshold: 50000
    on_fail: REJECT_NO_DRAFT
    severity: P0
    source_required: true
    corpus_ref: 7_cfr_4280_e.pdf:§4280.503
    confidence:
      level: medium
      reason: "7 CFR 4280-E §4280.503 citation present pre-Pass-2; canonical-reference-doc anchored (§USDA-RD RBDG Eligibility)"
      promotion_requirement: "7 CFR 4280-E §4280.503 verbatim text ingested at Pillar-2"
  - gate_id: F-RBDG-INELIGIBLE-APPLICANT-CLASS
    gate_type: hard_eligibility_gate
    predicate: "Applicant in {rural_public_body, rural_serving_nonprofit_501c, federally_recognized_tribe}"
    machine_check:
      field_in_applicant_context: kfr.applicant.entity_type
      operator: in
      threshold: [rural_public_body, rural_serving_nonprofit_501c, federally_recognized_tribe]
    on_fail: REJECT_NO_DRAFT
    severity: P0
    source_required: true
    corpus_ref: 7_cfr_4280_e.pdf:§4280.504
    confidence:
      level: medium
      reason: "7 CFR 4280-E §4280.504 citation present pre-Pass-2; canonical-reference-doc anchored"
      promotion_requirement: "7 CFR 4280-E §4280.504 verbatim text ingested at Pillar-2"
  - gate_id: F-RBDG-SMALL-AND-EMERGING-BENEFICIARY
    gate_type: competitive_scoring_signal
    predicate: "Beneficiary <50 new employees AND <$1M projected annual gross revenue at start"
    machine_check:
      operator: matches                                            # composite-shape check; flagged for decomposition per Discipline 3a.3
      threshold: { max_new_employees: 50, max_projected_annual_gross_revenue_dollars: 1000000 }
    on_fail: WARN_OPERATOR
    severity: HIGH
    source_required: true
    corpus_ref: usda_rd_guidance_small_emerging.pdf:p3
    confidence:
      level: medium
      reason: "Beneficiary class definition (≤50 employees, <$1M revenue) canonical-reference-doc anchored (§USDA-RD RBDG Beneficiary)"
      promotion_requirement: "USDA-RD interpretive guidance on 'small and emerging' definition ingested at Pillar-2"
    pass_1_reconciliation_note: "operator `matches` with object-shape threshold is a composite predicate not in canonical DSL grammar (Discipline 3a.3). Decompose into two atomic predicates (max_new_employees less_or_equal 50 AND max_projected_annual_gross_revenue_dollars less_than 1000000) at a future predicate-decomposition pass; predicate semantics preserved at Pass 1."

match_logic:
  # PASS-0 harm-prevention fix (operator canonical reference 2026-05-18):
  # earlier prose treated ≥50% cash match as a hard requirement; per
  # 7 CFR 4280-E + RBDG NOFO history, match is a competitive scoring
  # factor only. Logician must not REJECT for missing match.
  required_match: false
  competitive_factor: true
  source_required: true            # corpus_ref pending Pillar 2
  preferred_evidence:
    - non_federal_funding_committed
    - commitment_letters
    - cash_or_verifiable_in_kind
  logician_behavior:
    missing_match: "DO_NOT_REJECT"
    vague_committed_resources: "WARN_OPERATOR"

scoring_rubric:
  total_points: 100  # NEEDED verify FY26
  criteria:
    - criterion_id: RBDG-RUBRIC-LEVERAGING
      name: "Leveraging of Resources"
      weight_pct: <NEEDED — historical ~20-25%>
      reviewer_expectation: "≥50% cash match, all commitments unconditional, in-kind third-party-documented."
      reviewer_punishment: "Vague match, contingent language, applicant-asserted in-kind without third-party letters."
    - criterion_id: RBDG-RUBRIC-ECONOMIC-IMPACT
      name: "Economic Impact (Jobs Created + Retained)"
      weight_pct: <NEEDED — historical ~25-30%>
      reviewer_expectation: "FTE methodology + counting period + verification path; created vs retained distinguished."
    - criterion_id: RBDG-RUBRIC-SUSTAINABILITY
      name: "Sustainability of Project Beyond Grant"
      weight_pct: <NEEDED — historical ~10-15%>
      reviewer_expectation: "Post-grant revenue source identified + dollar committed; transition plan."
    - criterion_id: RBDG-RUBRIC-APPLICANT-CAPACITY
      name: "Applicant Capacity / Experience"
      weight_pct: <NEEDED — historical ~15-20%>
      reviewer_expectation: "Prior federal-grant track record + named TA-delivery staff + documented partnerships."
    - criterion_id: RBDG-RUBRIC-PROJECT-RATIONALE
      name: "Project Rationale / Need"
      weight_pct: <NEEDED — historical ~15-20%>
      reviewer_expectation: "Data-cited rural-business-need analysis + named gap + theory of change."

evidence_ladder:
  strongest:
    - "Cash match commitment letter on funder letterhead with unconditional language + signature"
    - "FTE methodology with counting period + verification path (quarterly payroll affidavit, etc.)"
    - "Prior USDA-RD grant track record"
    - "Rural-area service-area documentation with OMB-adjusted decennial census cite"
  acceptable:
    - "Match described with dollar amount but commitment letter pending"
    - "FTE methodology described but counting period not finalized"
    - "Other federal-grant track record"
  weak:
    - "Match as 'significant in-kind support' without dollar valuation"
    - "Jobs framed as 'created and retained' without separation"
  unacceptable:
    - "Speculative match without commitment"
    - "Speculative job projections without methodology"
    - "Rural-area assertion without census backing"

scribe_section_requirements:
  - nofo_section_id: §IV.B.3                    # Project Approach (NEEDED verify FY26)
    drafting_decisions:
      - decision: "Lead match-narrative with CASH match before in-kind; order cash → documented-third-party-in-kind → applicant-confirmed-in-kind."
        rubric_ref: RBDG-RUBRIC-LEVERAGING
      - decision: "Quantify jobs FTE + counting-period + verification-path; distinguish created vs retained."
        rubric_ref: RBDG-RUBRIC-ECONOMIC-IMPACT
    forbidden_register_in_this_section:
      - phrase: "innovative"
        prefer_instead: "describe the operational difference"
      - phrase: "leverage (as verb)"
        prefer_instead: "leverage (as noun) OR match"
  - nofo_section_id: §IV.B.6                    # Budget Narrative
    drafting_decisions:
      - decision: "Line items map 1-to-1 to project-narrative activities; budget total ties to match-narrative total."
        rationale: "RBDG admin review rejects budgets where line items don't tie to narrative — FY24+FY25 pattern."

judge_scoring_map:
  - criterion_id: RBDG-RUBRIC-LEVERAGING
    judge_question: "How well does the draft demonstrate cash-match dominance + unconditional commitment + third-party-documented in-kind?"
    score_bands:
      - { band: 5, descriptor: "≥50% cash, all unconditional commitments with letters, all in-kind third-party-documented" }
      - { band: 4, descriptor: "≥30% cash, all unconditional, in-kind mostly third-party-documented" }
      - { band: 3, descriptor: "<30% cash, some contingent, in-kind partly applicant-asserted" }
      - { band: 0, descriptor: "No match documented OR all match contingent on RBDG award" }
    # Pass-1 reconciliation 2026-05-18 per D-RBDG follow-up: tie_breaker re-aligned with
    # match_logic block (required_match: false; competitive_factor: true). The prior
    # tie-breaker "favor cash-match-≥50%" assumed match was a hard requirement, which
    # was demoted at Pass 0. Tie-breaker now anchors on documented non-federal funding
    # commitment authenticity (unconditional vs contingent), per 7 CFR 4280-E + RBDG
    # NOFO history. Tier descriptors above are NOT changed at Pass 1 (predicate
    # semantics out-of-scope; Pass 4 Judge revisits descriptor language).
    tie_breaker: "Between 4 and 3, higher band requires documented non-federal funding committed with all commitments unconditional (cash AND/OR third-party-documented in-kind); cash-share dominance scores higher but is NOT a hard threshold per match_logic block."
    pass_1_reconciliation_note: "Tier descriptors (band 5 ≥50% cash, band 4 ≥30% cash) still encode cash-share-as-threshold framing. Pass 4 (Judge) reconciles descriptor language with match_logic.required_match: false; Pass 1 reconciles the tie-breaker but not the descriptor text (scoring-weight changes are Pass 4 scope)."

red_team_probes:
  - probe_id: RBDG-PROBE-MATCH-AUTHENTICITY
    probe_question: "For each match commitment: UNCONDITIONAL or CONTINGENT on RBDG award?"
    targets_rubric_criterion: RBDG-RUBRIC-LEVERAGING
    score_impact_if_fails: "-5 (full criterion-3 reduction worst case)"
  - probe_id: RBDG-PROBE-RURAL-POP-HONESTY
    probe_question: "Does claimed service-area population match OMB-adjusted most-recent decennial census?"
    score_impact_if_fails: ADMINISTRATIVE_REJECTION
  - probe_id: RBDG-PROBE-BENEFICIARY-CLASS-AUTHENTICITY
    probe_question: "Beneficiary satisfies BOTH 'small' (<50 employees) AND 'emerging' (<$1M revenue) — both required?"
    score_impact_if_fails: "-10 or ADMINISTRATIVE_REJECTION"
  - probe_id: RBDG-PROBE-SUBRECIPIENT-MONITORING
    probe_question: "Does draft describe sub-recipient monitoring per 2 CFR 200.332?"
    targets_rubric_criterion: RBDG-RUBRIC-APPLICANT-CAPACITY
    score_impact_if_fails: "-3"

logician_gates:
  - gate_id: F-RBDG-MATCH-CONTINGENT-LEAK
    gate_type: competitive_scoring_signal
    when: PRE
    severity: HIGH
    predicate_python: "any(m.get('contingent_on_award') is True for m in kfr.applicant.match_commitments or [])"
    fail_action: WARN_OPERATOR
    source_required: true
    corpus_ref: pending_pillar_2  # 7 CFR 4280-E §V.C.3 + RBDG NOFO §V.C.3
    confidence:
      level: medium
      reason: "Contingent-match zero-weight rule is canonical-reference-doc anchored (RBDG NOFO §V.C.3 referenced in §A red_team)"
      promotion_requirement: "7 CFR 4280-E §V.C.3 verbatim text ingested at Pillar-2"
  - gate_id: F-RBDG-BUDGET-TIE-MISMATCH
    gate_type: competitive_scoring_signal
    when: POST
    severity: HIGH
    predicate_python: "sum(item.amount for item in draft.budget_line_items) != draft.budget_total_declared"
    fail_action: WARN_OPERATOR
    source_required: false
    corpus_ref: pending_pillar_2  # RBDG FY24-FY25 admin-review pattern (operator-attested)
    confidence:
      level: low
      reason: "pre_corpus_hypothesis — admin-review pattern referenced in scribe_section_requirements §IV.B.6 rationale; FOIA evidence pending"
      promotion_requirement: "RBDG FY24-FY25 admin-rejection pattern documented via FOIA/USDA-OIG ingested at Pillar-2"

source_backing:
  corpus_refs:
    - "<NEEDED — Pillar 2: RBDG FY26 NOFO + Grants.gov synopsis + Federal Register notice>"
    - "<NEEDED — Pillar 2: RBDG FY26 scoring rubric (NOFO appendix or FOIA)>"
    - "<NEEDED — Pillar 2: FY24 + FY25 RBDG award rosters + PA-specific history>"
    - "<NEEDED — Pillar 2: 7 CFR Part 4280-E regulatory text>"
    - "<NEEDED — Pillar 2: USDA-RD interpretive guidance on 'small and emerging' definition>"
  confidence: LOW pre-corpus.
  unresolved_questions:
    - "FY26 exact rubric weights per criterion"
    - "FY26 dollar range + cap"
    - "Recent FY24-FY25 administrative-rejection pattern"
```

---

## §1 — What "depth" means for THIS artifact

RBDG FY26 program-level depth is the **methodology-anchor decision substrate** — eligibility predicates + 5-criterion rubric + match-narrative discipline + Enterprise-vs-Opportunity activity-track distinction + sub-recipient monitoring (2 CFR 200.332) integration.

**Codex same-prompt-with/without test:**
- **Without** — Scribe writes generic federal grant with applicant-beneficiary confusion. Headcount jobs. Vague match. Judge applies generic 12-dim scoring.
- **With** — Scribe leads match with CASH-first, FTE-quantifies jobs, names rural county with census cite, distinguishes applicant (rural body) from beneficiary (small + emerging private business). Judge applies RBDG 5-criterion weighted rubric. Red Team probes match-contingency + rural-pop honesty + beneficiary-class authenticity + sub-recipient monitoring. Logician fails closed on rural-pop >50k + ineligible applicant class + budget-tie mismatch.

Inherits USDA-RD funder depth charter register + funder-wide PRE-gates (SAM-active, UEI, federal-debt, suspension).

---

## §2 — Primary sources in scope

| Corpus | Sources | Path | Count |
|--------|---------|------|-------|
| `nofos/` | RBDG FY26 NOFO PDF + Grants.gov synopsis + Federal Register | Grants.gov + Federal Register | 2-3 |
| `rubrics/` | RBDG FY26 scoring rubric (NOFO appendix or FOIA) | USDA-RD | 1-2 |
| `statutory/` | 7 CFR Part 4280-E | Federal Register | 1-2 |
| `awards/` | FY24 + FY25 RBDG rosters + PA-specific | USAspending.gov + USDA-RD | 2-3 |
| `guidance/` | "Small and emerging" definition; rural-pop methodology | USDA-RD public guidance | 1-3 |
| `prior_cycle_debrief/` | FY24 + FY25 administrative-rejection patterns | FOIA + USDA-OIG | 1-3 |

Case law OUT OF SCOPE.

---

## §3 — Tier classification

| Field | Tier |
|-------|:----:|
| Default | `1` |
| `rubric.weighted_dimensions[]` | `1` |
| `eligibility_gates[]` | `1` |
| `reviewer_relationship_notes[]` | `3` |
| `red_team_probes[]` | `2` |

---

## §4 — Refresh cadence

`per_cycle` (annually-cycled). `F-FID-STALE-RUBRIC` fires if rubric >18 months old AND annually-cycled.

---

## §5 — Calibration applicant pair

`food_systems` (CIC-01) × `operating_capacity` (CLC-03). Pillar 4 DORMANT.

---

## §6 — Done definition

`audited` when L-005 passes per same discipline as SARE-NE / USDA-RD depth-charters. Methodology-anchor role: this artifact's Pillar-3 cycle is the source of methodology v1.0 doc at week 5.

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

- USDA-RD funder-level facts (→ `funders/USDA-RD.yaml`)
- Other USDA-RD programs (RCDG / CFP / B&I / REAP) — separate artifacts
- Compliance internals (→ `compliance_cascades/` — 2 CFR 200; Davis-Bacon if construction)
- Reviewer-type heuristics (→ `reviewer_heuristics/federal-program-officer.yaml`)
- Per-applicant rural-population-served framing (→ `orgs/<slug>/`)
- Per-beneficiary small-business profile detail
- RBDG cycles prior to FY26 except as historical reference
- Case law interpretation
- USDA-RD-RBIG (Rural Business Investment Grant) — separate program; redirect target if RBDG fails rural-pop threshold but RBIG threshold satisfied
