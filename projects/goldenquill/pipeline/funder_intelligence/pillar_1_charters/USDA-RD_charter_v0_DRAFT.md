# Depth Charter — `USDA-RD` (funder behavior profile)

> **Pillar 1 of 4** per `pipeline/planning/funder_intelligence_database_research_project_2026-05-16.md` §3.1.
> **Quality bar** per `docs/FID_ARTIFACT_OPTIMIZATION_PRINCIPLES_2026-05-18.md` §1 + §2 + Codex framing (2026-05-18).
> **Status: DEPTH CHARTER v0 (pre-corpus hypothesis; do not load as signed logic)** — funder-pattern-detector quality bar for the 8 funder charters in this roster (paired with USDA-NIFA-SARE-NE-FY26 program-depth-charter). **Once operator approves, the other 7 funder + 5 program charters are re-authored as `[PRE-DEPTH-CHARTER]` placeholders.**
>
> **[CONJECTURE — Pillar-2 corpus pending]** All USDA-RD-specific funder-fact claims in this charter are operator-asserted + general-knowledge-grounded at charter authoring. Pillar-2 corpus assembly (USDA-RD strategic plan FY22-26 + Rural Prosperity Task Force docs + 7 CFR cross-program citations + 2 years of USAspending.gov aggregate awards + sample of FY24-FY25 NOFOs) must promote each claim with `corpus_ref` + ≤2-sentence verbatim quote or remove it. Logician `F-FID-FACT-ORPHAN` enforces at Pillar-3 L-005.

---

## Header

| Field | Value |
|------:|:------|
| `artifact_id` | `USDA-RD` |
| `artifact_family` | `funder` |
| `version` | `depth_charter_v0` |
| `lifecycle` | `draft` |
| `phase` | `1 — exemplar pair` |

---

## §A — Adversarial pre-checks (canonical 2026-05-18)

```yaml
runtime_consumer:
  scout:
    reads_fields: [geographic_eligibility, program_roster, compliance_cascade_defaults]
    stage: DISCOVER
    decision_changed: "Scout DISCOVER filters radar to applicants whose service area satisfies USDA-RD rural eligibility (population threshold varies per program — RBDG/RCDG typically <50K; CFP <20K). Non-rural applicants downgrade to OUT_OF_SCOPE before program-level matching fires."
  scribe:
    reads_fields: [language_register, drafting_implications, funder_dialect, mission_framing]
    stage: scaffold
    decision_changed: "Scribe applies USDA-RD-canonical register across ALL USDA-RD program drafts: 'rural prosperity' framing, 'leveraging' (noun-form only for match), 'economic impact' (FTE + dollar metrics), 'small and emerging private businesses' (RBDG-specific but USDA-RD-dialect-typical), public-purpose justification leading every narrative. Cross-program dialect consistency reduces register switching cost and signals 'USDA-RD-fluent applicant' to state office reviewers."
  judge:
    reads_fields: [judge_implications, known_failure_modes_at_funder_level]
    stage: cross_check
    decision_changed: "Judge applies cross-program USDA-RD weighting pattern: leveraging + economic-impact criteria carry higher weight than scientific-merit / innovation criteria across the USDA-RD portfolio (verify per program at Pillar 2). Judge cross-checks: does the draft surface FTE-quantified economic impact + leveraged match? If absent, downgrade independent of program-specific rubric."
  red_team:
    reads_fields: [red_team_probe_seeds, known_failure_modes_at_funder_level, compliance_cascade_defaults]
    stage: probe_target_selection
    decision_changed: "Red Team probes USDA-RD cross-program failure modes: match-fund authenticity (unconditional vs contingent — same as program-level but funder-wide pattern); rural-population threshold honesty; Davis-Bacon trigger discipline when construction; NEPA categorical-exclusion declaration when ground-disturbing; SAM-active-at-submission (vs SAM-active-at-application — state office desk-check moment)."
  logician:
    reads_fields: [eligibility_gates, compliance_cascade_defaults, logician_gate_candidates]
    stage: PRE
    decision_changed: "Logician applies USDA-RD funder-wide PRE-gates that fire BEFORE any USDA-RD program-level gates: SAM-active, UEI-present, federal-debt-resolved, suspension-debarment-not-active. Failure of any of these on any USDA-RD program application = REJECT_NO_DRAFT immediately regardless of program-specific eligibility. Saves Scribe + downstream seats from work on applicants that fail funder-level baseline."
```

```yaml
artifact_must_not_contain:
  - facts belonging to another artifact          # → program-level facts live in programs/USDA-RD-<program>-FY26.yaml
  - applicant-specific claims                    # no named applicants; CLAUDE.md Law 3 + Codex-audit P0
  - uncited generalizations                      # every fact carries corpus_ref + ≤2-sentence verbatim at Pillar 3
  - compliance framework internals               # 2 CFR 200, Davis-Bacon, NEPA → compliance_cascades/
  - reviewer-type heuristics                     # reviewer_heuristics/federal-program-officer.yaml
  - other USDA agencies                          # USDA-AMS, USDA-NIFA, USDA-FNS, USDA-FSA, USDA-NRCS — separate funder artifacts
  - case law interpretation                      # compliance-officer territory
```

```yaml
strength_test:
  - "Name one concrete drafting decision this artifact changes."
  - "Name one proposal this artifact would reject or downgrade."
  - "Name one Red Team probe this artifact enables."
```

**Answers (PASSED — concretely realized in §1 + §B below):**

1. **Drafting decision.** Scribe applies USDA-RD funder-wide register across ALL USDA-RD program drafts: "rural prosperity" framing in §I opening, "leveraging" as noun-only when describing match, FTE-quantified economic-impact framing in §II, "small and emerging private businesses" terminology when describing beneficiaries (RBDG-specific but cross-program-typical). Same Scribe prompt WITHOUT this artifact produces register-inconsistent drafts that don't read as "USDA-RD-fluent" to state office reviewers.
2. **Proposal rejected.** Logician `F-USDA-RD-SAM-INACTIVE` (P0; cross-program) fails closed any USDA-RD application where applicant SAM.gov status is not Active. Scribe is never invoked across ANY USDA-RD program; operator gets a redirect-suggestion to fix SAM registration before any USDA-RD work fires. Same applies to `F-USDA-RD-UEI-MISSING`, `F-USDA-RD-FEDERAL-DEBT-UNRESOLVED`, `F-USDA-RD-SUSPENSION-ACTIVE`.
3. **Red Team probe.** Red Team's `USDA-RD-PROBE-RURAL-MIXED-AREA-HONESTY` probe asks: *"If the service area mixes rural + non-rural population, does the application explicitly calculate rural-only beneficiary count or attribute all benefits to the rural portion? Inflated rural-area attribution is a known USDA-RD State Office desk-check finding."* Generic Red Team probes service-area description quality; USDA-RD-aware Red Team probes the specific rural-attribution methodology, a known administrative-rejection vector across the USDA-RD portfolio.

---

## §B — Codex-shape depth-charter YAML

```yaml
artifact_id: USDA-RD
artifact_family: funder
version: depth_charter_v0
lifecycle: draft
validation_status: pre_corpus_hypothesis
runtime_load_status: do_not_load_as_signed_logic
operator_label: depth_charter_v0

one_sentence_job: |
  Equip every USDA-RD program draft with funder-wide register, default
  compliance cascades, cross-program eligibility predicates, and reviewer-
  type pointers — so Scribe / Judge / Red Team / Logician behave as
  USDA-RD-fluent across the whole USDA-RD portfolio, not just per-program.

runtime_consumers:
  scout:
    pre_filter_question: |
      Does the applicant satisfy the USDA-RD federal-baseline (SAM-active,
      UEI present, federal-debt-resolved, suspension-debarment-not-active)
      AND does the project serve a rural area (per the program-instance
      definition — CFP ≤20K, RBDG/RCDG ≤50K, etc.)?
    eligibility_dimensions:
      - sam_active                        # SAM-active at submission (not just application time)
      - uei_present                       # Unique Entity Identifier present in SAM record
      - federal_debt_resolved             # no delinquent federal debt
      - suspension_debarment_clear        # no active suspension / debarment
      - rural_area_signal                 # project serves rural area (downstream program-instance threshold)
    hard_gate_refs:
      - F-USDA-RD-SAM-INACTIVE
      - F-USDA-RD-UEI-MISSING
      - F-USDA-RD-FEDERAL-DEBT-UNRESOLVED
      - F-USDA-RD-SUSPENSION-ACTIVE
    cross_funder_signal: |
      Federal-program funder-level (the umbrella that hosts CFP / RBDG /
      RCDG / B&I / REAP / etc.). Routes opportunity DOWN to USDA-RD
      program-instance charters. Non-rural applicants routed AWAY to
      USDA-AMS (urban-allowed value-added program portfolio), USDA-NIFA
      (research), or non-USDA federal portfolios (EDA, HUD CDBG). Federal-
      baseline failures (SAM inactive, etc.) route to operator-attention
      BEFORE any program-instance is even considered.
    operator_assist_required: |
      Escalate to operator when: (a) SAM record is inactive or expiring
      within submission window (F-USDA-RD-SAM-INACTIVE P0 — operator must
      renew before any USDA-RD draft proceeds), (b) UEI missing or
      malformed (F-USDA-RD-UEI-MISSING P0), (c) federal-debt status unknown
      (F-USDA-RD-FEDERAL-DEBT-UNRESOLVED P0), (d) suspension / debarment
      active or pending appeal (F-USDA-RD-SUSPENSION-ACTIVE P0).
    source_authority: |
      USDA-RD federal-baseline per 2 CFR 200 Uniform Guidance §200.205
      (SAM-active requirement) + 2 CFR 180 (suspension/debarment) +
      31 USC 3720B (federal-debt collection). Canonical reference
      §USDA-RD Federal Baseline.
    prose_summary: |
      DISCOVER pre-filters non-rural applicants; reads program_roster to
      enumerate USDA-RD programs across active radar.
  scribe:
    voice_change: |
      USDA-RD-fluent federal-program-officer register: rural-prosperity
      framing in §I; "leveraging" (noun-form only); FTE-quantified
      economic-impact; public-purpose justification for nonprofit/tribal
      applicants.
    section_ordering:
      - "§I rural-prosperity mission + economic-impact theory-of-change + named rural area"
      - "§II FTE-quantified jobs (created + retained, separate methodologies + counting periods)"
      - "§III public-purpose justification (nonprofit/tribal applicants)"
      - "§IV match narrative (program-specific ordering — RBDG cash-first; RCDG cooperative-form-first; CFP ECF-first)"
      - "§V applicant qualifications + prior USDA-RD / federal track record"
      - "§VI work plan"
    must_do:
      - "Open §I with rural-prosperity mission alignment + named rural-area + economic-impact theory of change."
      - "Use 'leveraging' (noun) when describing match; never 'leverage' (verb)."
      - "Quantify jobs in FTE + counting period + verification path; distinguish created vs retained."
      - "Cite rural-area service-area with OMB-adjusted decennial census reference."
      - "For nonprofit / tribal applicants, include public-purpose framing paragraph in §I."
      - "Reference applicant's prior USDA-RD or USDA federal-grant track record in qualifications section if available."
    must_not_do:
      - "Lead narrative with 'innovative' framing — USDA-RD reviewers underweight novelty relative to leveraging + impact."
      - "Conflate jobs-created with jobs-retained — they're separate criteria typically."
      - "Frame rural-area service eligibility on assertion alone — always cite census + methodology."
      - "Mix applicant-identity with beneficiary-identity (for RBDG/RCDG — applicant is the rural public body/nonprofit/tribe; beneficiary is the small/emerging private business)."
    cross_funder_signal: |
      USDA-RD register is distinct from USDA-NIFA (hypothesis/methodology-first
      peer-review-academic register) and USDA-AMS (market-access + producer-
      revenue-causal-chain register). Same applicant pitching all three USDA
      sub-agencies code-switches per agency.
    source_authority: |
      USDA-RD federal-baseline register per canonical reference §USDA-RD
      Funder Profile + cross-program 7 CFR Part 4280 / 4284 / 3570 framing
      patterns. Specific "leveraging > innovation" weighting pattern is
      operator-derived heuristic; pinpoint Pillar-2 corroboration pending.
    prose_summary: |
      Reads funder_dialect + language_register at scaffold stage to apply
      USDA-RD register across any USDA-RD program draft.
  judge: |
    Cross-checks program-level rubric scores against USDA-RD funder-wide
    weighting pattern (leveraging + economic impact heavier than
    scientific-merit-style criteria).
  red_team: |
    Probes funder-wide failure modes: matching-fund authenticity, rural-area
    honesty, Davis-Bacon trigger discipline, NEPA CE/EA decision discipline,
    SAM-active-at-submission (not just at-application).
  logician: |
    PRE-gates fire before any USDA-RD program-level gate: SAM-active,
    UEI-present, federal-debt-resolved, suspension-debarment-not-active.
    Fail-closed REJECT_NO_DRAFT prevents Scribe invocation across the
    whole USDA-RD portfolio for non-baseline-eligible applicants.

mission_framing:
  one_paragraph_summary: |
    USDA Rural Development advances rural prosperity through three sub-mission
    areas: Rural Business-Cooperative Service (RBDG, RCDG, B&I, REAP);
    Rural Housing Service (Community Facilities + housing); Rural Utilities
    Service (RUS programs). Cross-cutting framing: economic + community
    development in rural areas, with population thresholds varying per
    program. Federal-program-officer review register dominates.
  corpus_ref: "<NEEDED — Pillar 2: USDA-RD strategic plan FY22-26 + Rural Prosperity Task Force docs>"
stage_behavior:                                                # how funder-level fields influence each program-level review stage
  screen:
    primary_question: |
      Does the applicant satisfy USDA-RD funder-wide baseline (SAM-active,
      UEI, no federal debt, no suspension/debarment) AND program-specific
      rural-population threshold?
    time_budget: <NEEDED — verify USDA-RD state-office screen-stage budget; historical ~0.5 hr/proposal>
    pass_fail_triggers:
      - "SAM.gov inactive at submission → FAIL"
      - "UEI missing → FAIL"
      - "Federal debt unresolved → FAIL"
      - "Suspension or debarment active → FAIL"
      - "Service area population exceeds program rural threshold → FAIL (program-specific gate)"
    common_rejections:
      - "Mixed rural + non-rural service area without explicit rural-only beneficiary attribution methodology — state office desk-check finding."
      - "SAM.gov shows Active at application date but lapsed before submission — state office checks at submission moment, not application."
      - "Letter of support / authorization from rural public body that has not formally adopted the resolution by submission date."

  score:
    primary_question: |
      How well does the proposal demonstrate cross-USDA-RD-pattern strengths
      (leveraging of resources, FTE-quantified economic impact, rural-prosperity
      mission alignment, public-purpose justification)?
    evidence_rewarded:
      - "Match commitments with unconditional language + dollar amounts + commitment letters attached"
      - "FTE-quantified jobs created + retained with counting period + verification path"
      - "Rural-prosperity narrative tied to specific rural community + economic indicators"
      - "Public-purpose framing for nonprofit and tribal applicants (public-bodies don't need this; nonprofits + tribes do)"
    scoring_blind_spots:
      - "Innovation framing tends to be UNDER-rewarded relative to leveraging + economic-impact framing in the USDA-RD portfolio. Drafts that lead with 'innovative' often score lower than drafts that lead with 'leveraged match + jobs.'"
      - "Reviewer attention can fade on multi-program-arm narratives; lead with the strongest economic-impact metric in §I to capture early scoring."
    common_penalties:
      - "Vague match commitments (no dollar amounts; no commitment letters; no unconditional language) → -3 to -5 points across USDA-RD programs."
      - "Headcount jobs without FTE conversion + counting period → -3 to -5 points on economic-impact criteria across USDA-RD programs."
      - "Public-purpose framing absent for nonprofit/tribal applicants → -2 to -4 points on scoring criteria where 'public-purpose' shows up."

  consensus:
    primary_question: |
      Across panel-scored USDA-RD proposals, how does this proposal's
      leveraging + economic impact + rural-mission alignment compare to
      top-quartile peers?
    tie_breakers:
      - "Between two adjacent scores on Leveraging criterion (any USDA-RD program), the higher band requires ≥50% cash match + all unconditional commitments."
      - "Between two adjacent scores on Economic Impact, the higher band requires FTE methodology explicit (not just implied)."
    portfolio_considerations: |
      USDA-RD state offices generally balance funded portfolio across PA
      rural-county distribution; Westmoreland / Allegheny / Washington /
      Greene / Fayette underrepresented vs eastern PA in recent FY24-FY25
      cycles per general impression. Verify per program at Pillar 2.

evidence_ladder:                                              # cross-program; specific evidence types USDA-RD reviewers reward
  strongest:
    - "Match commitment letter on funder/source letterhead with explicit dollar amount + unconditional language + signature"
    - "FTE methodology with explicit counting period + verification path (e.g., 'beneficiary business will provide quarterly payroll affidavit')"
    - "Prior USDA-RD grant track record (number + amount + outcomes) for the applicant"
    - "Rural-area service-area documentation with OMB-adjusted decennial census cite"
    - "Public-body resolution or nonprofit-board minutes formally adopting the project (for applicants where governance approval is required)"
  acceptable:
    - "Match commitment described in narrative with dollar amount but commitment letter pending"
    - "Headcount jobs with FTE conversion methodology described but not finalized"
    - "Other federal-grant track record (USDA but not USDA-RD; SBA; HUD; NIFA)"
  weak:
    - "Match described as 'significant in-kind support' without dollar valuation methodology"
    - "Jobs framed as 'created and retained' without separating the two"
    - "Generic federal-grant track record without rural focus"
  unacceptable:
    - "Speculative match without commitment"
    - "Speculative job projections without methodology"
    - "Rural-area assertion without census or methodology backing"

language_register:
  preferred_terms:
    - rural_prosperity
    - leveraging                                              # noun form for match contributions
    - economic_impact
    - jobs_created
    - jobs_retained
    - small_and_emerging_businesses                           # RBDG-canonical but USDA-RD-cross-program-typical
    - rural_community
    - public_purpose
    - essential_community_facility                            # CFP-canonical
    - cooperative                                             # RCDG-canonical
  suspicious_terms:
    - innovative                                              # rewarded less than leveraging + impact framing
    - cutting_edge
    - revolutionary
    - significant_impact                                      # without effect size; trigger for Red Team probe
    - sustainable                                             # not punished but not particularly rewarded at USDA-RD; SARE-specific term
  sentence_shapes_that_work:
    - "We will leverage $[X] in cash match (unconditional, commitment letters attached) to deliver [N] FTE jobs created + [M] FTE jobs retained over [T] years in [named rural county/region]."
    - "This project advances USDA-RD's rural prosperity mission by [specific economic-impact mechanism]."
  sentence_shapes_that_fail:
    - '"Our innovative approach will create rural opportunity..." (suspicious terms + vague)'
    - '"Significant economic impact will result..." (no effect size; no methodology)'
    - '"We will partner with local farmers to..." (applicant-vs-beneficiary clarity absent for RBDG/RCDG)'
drafting_implications:
  scribe_must_do:
    - "Open §I with rural-prosperity mission alignment + named rural-area + economic-impact theory of change."
    - "Use 'leveraging' (noun) when describing match; never 'leverage' (verb)."
    - "Quantify jobs in FTE + counting period + verification path; distinguish created vs retained."
    - "Cite rural-area service-area with OMB-adjusted decennial census reference."
    - "For nonprofit / tribal applicants, include public-purpose framing paragraph in §I."
    - "Reference applicant's prior USDA-RD or USDA federal-grant track record in qualifications section if available."
  scribe_must_not_do:
    - "Lead narrative with 'innovative' framing — USDA-RD reviewers underweight novelty relative to leveraging + impact."
    - "Conflate jobs-created with jobs-retained — they're separate criteria typically."
    - "Frame rural-area service eligibility on assertion alone — always cite census + methodology."
    - "Mix the applicant-identity with the beneficiary-identity (for RBDG/RCDG specifically — applicant is the rural public body / nonprofit / tribe, beneficiary is the small/emerging private business)."
  section_ordering_notes: |
    Cross-program: lead §I with rural-prosperity framing + economic-impact
    theory-of-change. Move match-narrative ordering decision to the specific
    program artifact (RBDG leads with cash; RCDG leads with cooperative-form
    integrity; CFP leads with essential-community-facility framing).

judge_implications:
  scoring_dimensions_to_weight_harder:
    - "Leveraging / Match Quality — cross-program USDA-RD pattern weights this heavier than scientific-merit-style criteria"
    - "Economic Impact (jobs created + retained) — second-heaviest cross-program"
    - "Rural-area service + public-purpose alignment — third"
  evidence_required_before_high_score:
    - "Leveraging ≥4: cash match documented + unconditional commitments + commitment letters attached"
    - "Economic Impact ≥4: FTE methodology + counting period + verification path"
    - "Rural-area ≥4: census-cited service-area + OMB-adjusted methodology"

red_team_probe_seeds:
  - probe: "Are match commitments UNCONDITIONAL or CONTINGENT on USDA-RD award being granted?"
    why_it_matters: "Contingent match zero-weights in leveraging scoring across USDA-RD programs (RBDG/RCDG/CFP). Funder-wide pattern."
  - probe: "Does the rural-area attribution explicitly handle mixed rural + non-rural service areas, or attribute all benefits to the rural portion uniformly?"
    why_it_matters: "USDA-RD State Office desk-check finding across programs. Inflated rural attribution triggers administrative review rejection."
  - probe: "Is SAM.gov registration verified Active at the SUBMISSION moment, not just the application start? USDA-RD State Office checks at submission."
    why_it_matters: "Lapse between application start + submission is a known FY24-FY25 administrative-rejection vector."
  - probe: "If the project has any construction component, is Davis-Bacon prevailing-wage discipline reflected in the budget + narrative? Construction without Davis-Bacon acknowledgment = compliance audit risk."
    why_it_matters: "Cross-program USDA-RD compliance cascade (CFP especially); failure = HIGH-severity Red Team flag."
  - probe: "If the project has ground-disturbing activity, is the NEPA categorical-exclusion claim explicit or is EA/EIS scoping addressed?"
    why_it_matters: "USDA-RD NEPA-cascade; cross-program."
  - probe: "Are jobs-created and jobs-retained separated cleanly, with FTE methodology + counting period + verification path for each?"
    why_it_matters: "Aggregating the two is the single most-common downgrade vector on USDA-RD economic-impact criteria."

logician_gate_candidates:                                     # cross-USDA-RD-program gates (fire before any program-specific gate)
  - gate: F-USDA-RD-SAM-INACTIVE
    gate_type: hard_eligibility_gate
    failure_condition: "kfr.applicant.sam_gov_status != 'Active' at submission time"
    severity: P0
    fail_action: REJECT_NO_DRAFT
    source_required: true
    corpus_ref: pending_pillar_2  # 2 CFR 200 + SAM.gov registration requirement
    confidence:
      level: low
      reason: "pre_corpus_hypothesis — federal SAM.gov requirement is universally known but pinpoint citation pending Pillar-2"
      promotion_requirement: "2 CFR 200 regulatory citation + SAM.gov user agreement ingestion"
  - gate: F-USDA-RD-UEI-MISSING
    gate_type: hard_eligibility_gate
    failure_condition: "kfr.applicant.uei is None or kfr.applicant.uei == ''"
    severity: P0
    fail_action: REJECT_NO_DRAFT
    source_required: true
    corpus_ref: pending_pillar_2  # 2 CFR 25 UEI mandate
    confidence:
      level: low
      reason: "pre_corpus_hypothesis — UEI mandate per 2 CFR 25 widely cited but pinpoint pending"
      promotion_requirement: "2 CFR 25 regulatory citation ingested at Pillar-2"
  - gate: F-USDA-RD-FEDERAL-DEBT-UNRESOLVED
    gate_type: hard_eligibility_gate
    failure_condition: "kfr.applicant.has_unresolved_delinquent_federal_debt == True"
    severity: P0
    fail_action: REJECT_NO_DRAFT
    source_required: true
    corpus_ref: pending_pillar_2  # OMB-wide delinquent-debt bar
    confidence:
      level: low
      reason: "pre_corpus_hypothesis — OMB delinquent-debt eligibility bar is governmentwide but pinpoint pending"
      promotion_requirement: "OMB Circular A-129 / 31 USC 3711 citation ingested at Pillar-2"
  - gate: F-USDA-RD-SUSPENSION-ACTIVE
    gate_type: hard_eligibility_gate
    failure_condition: "kfr.applicant.sam_gov_exclusion_status in {'Suspended', 'Debarred', 'Ineligible'}"
    severity: P0
    fail_action: REJECT_NO_DRAFT
    source_required: true
    corpus_ref: pending_pillar_2  # 2 CFR 180 suspension & debarment
    confidence:
      level: low
      reason: "pre_corpus_hypothesis — 2 CFR 180 suspension-and-debarment regime cited governmentwide; pinpoint pending"
      promotion_requirement: "2 CFR 180 + SAM.gov exclusion list documentation ingested at Pillar-2"
  - gate: F-USDA-RD-RURAL-MIXED-AREA-UNRESOLVED
    gate_type: competitive_scoring_signal
    failure_condition: "kfr.applicant.service_area_includes_non_rural == True AND kfr.applicant.rural_only_attribution_methodology is None"
    severity: HIGH
    fail_action: WARN_OPERATOR
    source_required: false
    corpus_ref: pending_pillar_2  # USDA-RD rural-mixed-area attribution guidance
    confidence:
      level: low
      reason: "pre_corpus_hypothesis — USDA-RD rural-mixed-area attribution methodology pattern; documented guidance pending"
      promotion_requirement: "USDA-RD rural-mixed-area attribution guidance ingested at Pillar-2"
  - gate: F-USDA-RD-DAVIS-BACON-TRIGGER-MISS
    gate_type: competitive_scoring_signal
    failure_condition: "draft.has_construction_component() == True AND not draft.budget_includes_davis_bacon_prevailing_wage_discipline()"
    severity: HIGH
    fail_action: WARN_OPERATOR
    source_required: true
    corpus_ref: pending_pillar_2  # Davis-Bacon Act 40 USC 3141-48 + USDA-RD construction guidance
    confidence:
      level: medium
      reason: "Davis-Bacon trigger on USDA-RD construction is canonical-reference-doc anchored (USDA-RD funder profile §Compliance baseline); pinpoint citation pending Pillar-2"
      promotion_requirement: "Davis-Bacon Act + USDA-RD construction-guidance pinpoint ingested at Pillar-2"
  - gate: F-USDA-RD-NEPA-CE-CLAIM-MISSING
    gate_type: competitive_scoring_signal
    failure_condition: "draft.has_ground_disturbing_activity() == True AND draft.nepa_categorical_exclusion_claim is None AND draft.nepa_ea_eis_scoping is None"
    severity: HIGH
    fail_action: WARN_OPERATOR
    source_required: true
    corpus_ref: pending_pillar_2  # NEPA + 7 CFR 1970 USDA-RD environmental policy
    confidence:
      level: medium
      reason: "NEPA cascade on USDA-RD ground-disturbing projects is canonical-reference-doc anchored; pinpoint citation pending Pillar-2"
      promotion_requirement: "7 CFR 1970 USDA-RD environmental policy text ingested at Pillar-2"

source_backing:
  corpus_refs:
    - "<NEEDED — Pillar 2: USDA-RD Strategic Plan FY22-26>"
    - "<NEEDED — Pillar 2: Rural Prosperity Task Force final report cross-program references>"
    - "<NEEDED — Pillar 2: 7 CFR Part 4280 + 4284 + 3570 cross-program citations>"
    - "<NEEDED — Pillar 2: FY24 + FY25 USDA-RD aggregate award rolls from USAspending.gov>"
    - "<NEEDED — Pillar 2: 2-3 sample USDA-RD program NOFOs (FY26 RBDG / RCDG / CFP cited) to verify cross-program register>"
    - "<NEEDED — Pillar 2: USDA-RD State Office PA contact + administrative-review-pattern interview synthesis (Tier-2)>"
  confidence: |
    LOW pre-corpus. All cross-program register patterns, weighting tendencies,
    and state-office desk-check norms are operator-asserted + general-knowledge-
    grounded; Pillar-2 must promote each via NOFO/regulatory/USAspending cite.
  unresolved_questions:
    - "Does the cross-program 'leveraging > innovation' weighting pattern hold uniformly, or vary materially per program (RBDG vs RCDG vs CFP vs B&I)?"
    - "What is the actual PA State Office desk-check failure pattern across recent FY24-FY25 USDA-RD applications? (FOIA candidate.)"
    - "How does USDA-RD's Rural Prosperity framework wording change under any new Farm Bill reauthorization mid-FY26? (Event-triggered refresh.)"
    - "Davis-Bacon trigger threshold for RBDG (typically applies only when construction is in scope, but verify if any RBDG Enterprise activities trigger it)."
```

---

## §1 — What "depth" means for THIS artifact

USDA-RD funder-level depth is the **funder pattern detector** — what's TRUE across all USDA-RD programs, that Scribe / Judge / Red Team / Logician can apply once and benefit on every USDA-RD program draft. Distinct from program-level artifacts (which carry per-NOFO rubrics, eligibility, dollar caps) and from compliance-cascade artifacts (which carry 2 CFR 200 + Davis-Bacon + NEPA internals).

Codex quality test: *"Same Scribe prompt with/without the artifact should produce visibly different drafts."* For USDA-RD:

- **Without artifact** — Scribe writes a generic federal grant: any register, any match framing, any rural framing, headcount jobs without FTE. Judge applies generic federal rubric. Red Team probes generic adversarial. Logician applies generic federal eligibility (SAM, UEI).
- **With artifact** — Scribe applies USDA-RD register (rural prosperity, leveraging, economic impact, public-purpose for nonprofits/tribes), FTE-quantified jobs with verification path, OMB-adjusted rural-area cite, USDA-RD-specific sentence shapes. Judge cross-checks leveraging + economic-impact dimensions weighted heavier than novelty/innovation. Red Team probes USDA-RD-specific failure modes: match contingency, rural-mixed-area attribution, SAM-active-at-submission, Davis-Bacon-trigger-discipline, NEPA-CE-claim. Logician fails closed on funder-wide baseline gates (SAM, UEI, federal debt, suspension) BEFORE any program-level gate fires — saving Scribe + downstream work on baseline-ineligible applicants across the entire USDA-RD portfolio.

The deltas are funder-wide. The artifact is a force multiplier: once funder-level depth is in the lattice, every USDA-RD program draft (RBDG / RCDG / CFP / B&I / REAP / others) inherits the register + cascades + baseline gates automatically.

---

## §2 — Primary sources in scope

| Corpus category | Specific sources | Access path | Estimated count |
|-----------------|------------------|-------------|-----------------|
| `strategic/` | USDA-RD Strategic Plan FY22-26; Rural Prosperity Task Force final report | Public USDA-RD site | 1-2 |
| `regulatory/` | 7 CFR Part 4280 (RBDG/RCDG framework); 7 CFR Part 4284 (RCDG-specific); 7 CFR Part 3570 (CFP); cross-program OMB Uniform Guidance citations | Federal Register | 2-4 |
| `awards/` | FY24 + FY25 USDA-RD aggregate award rolls; PA-specific cross-program award totals | USAspending.gov + USDA-RD annual report | 2-3 |
| `interviews/` | 0-2 USDA-RD PA State Office contact conversations (Tier-2/3); 1-2 successful-USDA-RD-applicant cross-program debrief | Operator network outreach | 0-3 |
| `sample_nofos/` | 2-3 sample USDA-RD program NOFOs (FY26 RBDG/RCDG/CFP) to verify cross-program register | Grants.gov + USDA-RD | 2-3 |
| `guidance/` | OMB urban-area-definition adoption notice; USDA-RD's rural-area threshold guidance; NIFA-vs-USDA-RD indirect-cost cap distinction | Federal Register + USDA-RD public guidance | 2-3 |

Case law OUT OF SCOPE.

---

## §3 — Tier classification

| Field | Tier |
|-------|:----:|
| Default | `1` |
| `funder_dialect` (operator-derived) | `2` |
| `funder_officer_relationship_notes` (PA State Office) | `3` |
| `state_office_desk_check_pattern_notes` | `2` (operator-derived) |
| `historical_award_patterns_aggregate` | `1` (USAspending.gov public) |

---

## §4 — Refresh cadence

`annual` baseline + `event_triggered` overlay (Farm Bill reauthorization, USDA-RD Under-Secretary change, major Federal Register cross-program guidance update).

---

## §5 — Calibration applicant pair

`food_systems` (CIC-01) × `operating_capacity` (CLC-03). Pillar 4 DORMANT roster-wide.

---

## §6 — Done definition

`audited` when Pillar-3 single-cycle L-005 audit passes: every yaml field in §B carries `corpus_ref` + ≤2-sentence verbatim quote; `runtime_consumers.decision_changed` traces to specific fields; `strength_test` answers cross-reference §1 + §B; "same Scribe prompt with/without" diff captured in PR body inline test note + methodology v1.0 doc at week 5.

**Quality-bar role:** once operator approves this funder depth-charter (alongside SARE-NE Partnership program depth-charter), the other 7 funder + 5 program charters re-author as `[PRE-DEPTH-CHARTER]` placeholders pending re-author against this bar.

---

## §7 — Operator signature

```yaml
charter_signed_at: <pending_operator_attestation>
charter_signed_by_pubkey: <pending_operator_attestation>
charter_signed_canonical_bytes_sha3_512: <pending_operator_attestation>
charter_ed25519_signature: <pending_operator_attestation>
```

Manual ceremony per `pillar_1_charters/README.md`. Helper script `sign_charter.py` is a follow-up engineering task (Codex-audit P1).

---

## §8 — Out of scope (anti-drift)

- Per-program FY26 NOFO text, rubric, eligibility (lives in `programs/USDA-RD-<program>-FY26.yaml`)
- Compliance framework internals (lives in `compliance_cascades/` — this artifact carries pointers + cross-program trigger conditions only)
- Reviewer-type heuristics (lives in `reviewer_heuristics/federal-program-officer.yaml`)
- Other USDA agencies (USDA-AMS, USDA-NIFA, USDA-FNS, USDA-FSA, USDA-NRCS) — separate funder artifacts
- Per-applicant compliance posture / cross-program portfolio strategy (lives in `orgs/<slug>/`)
- Case law interpretation
