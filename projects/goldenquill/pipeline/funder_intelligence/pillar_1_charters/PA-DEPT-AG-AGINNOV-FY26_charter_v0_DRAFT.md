# Depth Charter — `PA-DEPT-AG-AGINNOV-FY26` (PA Ag Innovation Grant)

> **Pillar 1 of 4** per `pipeline/planning/funder_intelligence_database_research_project_2026-05-16.md` §3.1.
> **Quality bar** per `docs/FID_ARTIFACT_OPTIMIZATION_PRINCIPLES_2026-05-18.md` §1 + §2 + Codex framing.
> **Status: DEPTH CHARTER v0 (pre-corpus hypothesis; do not load as signed logic)** — re-authored to Codex yaml shape per operator directive 2026-05-18. Inherits PA-DEPT-AG funder depth-charter for state-program-officer register + PA-Preferred discipline.
>
> **[CONJECTURE — Pillar-2 corpus pending]** Active FY26 tracks not yet pulled; rubric publication discipline varies. `F-FID-FACT-ORPHAN` enforces at L-005.

---

## Header

| Field | Value |
|------:|:------|
| `artifact_id` | `PA-DEPT-AG-AGINNOV-FY26` |
| `artifact_family` | `program` |
| `funder_pointer` | `PA-DEPT-AG` |
| `version` | `depth_charter_v0` |
| `lifecycle` | `draft` |
| `pillar_2_dispatch_position` | **6 of 6** (last in sequence; least pursuit-urgency for current consumer roster) |

---

## §A — Adversarial pre-checks

```yaml
runtime_consumer:
  scout:
    reads_fields: [scout_verify.live_check_url, eligibility_gates, active_tracks]
    stage: both
    decision_changed: "Scout DISCOVER pre-filters PA-located applicants matching active-track eligibility (infrastructure / processing / dairy / hemp / ag-tech — tracks vary year-over-year). VERIFY checks for FY26 active track list."
  scribe:
    reads_fields: [scribe_section_requirements, scoring_rubric, drafting_implications]
    stage: both
    decision_changed: "Scribe applies state-program-officer register (inherits PA-DEPT-AG funder depth-charter): named PA county + Senate/House districts in §II; PA-Preferred branding verified in §I; grant-type-specific eligibility cascade in §III per claimed_grant_type enum (innovation_planning $7.5K–$50K @ 30% non-state match; onsite_project $5K–$200K @ 50% non-state match; regional_impact $100K–$2M @ 50% non-state match); state-budget-cycle-aware timeline in §V."
  judge:
    reads_fields: [scoring_rubric, judge_scoring_map]
    stage: rubric_scoring
    decision_changed: "Judge applies PA Ag Innovation track-specific rubric (when publicly published) OR criteria-without-weights synthesis (when state declines to publish full rubric). Tie-breakers favor named-district economic-impact + PA-Preferred + state-source match."
  red_team:
    reads_fields: [red_team_probes]
    stage: probe_target_selection
    decision_changed: "Red Team probes PA Ag Innovation-specific failure modes: grant-type-eligibility-cascade mismatch (e.g., claimed innovation_planning with budget exceeding $50K enum max; claimed onsite_project with 30% match below required 50%; claimed regional_impact outside $100K–$2M range); PA-Preferred branding eligibility integrity; legislator-district economic-impact sensitivity; state-budget-cycle timeline risk."
  logician:
    reads_fields: [eligibility_gates, logician_gates]
    stage: PRE
    # Pass-1 reconciliation 2026-05-18 per D-AGINNOV follow-up: §A logician.decision_changed
    # reconciled with Pass-0 polarity-flip + severity-promotion on
    # F-AGINNOV-MATCH-USES-STATE-SOURCE. Prior text described pre-Pass-0 posture
    # (HIGH severity, "cash match not from named PA source"). Updated text matches
    # §B definition: P0 severity, REJECT_NO_DRAFT on match-contains-State-sourced-funds.
    decision_changed: "Logician fires F-AGINNOV-NOT-PA-LOCATED (P0; applicant not PA-located), F-AGINNOV-TRACK-ELIGIBILITY-CASCADE-MISMATCH (P0; grant-type-specific eligibility cascade failure — predicate references retired commodity-track model, see pass_1_reconciliation_note in §B), F-AGINNOV-MATCH-USES-STATE-SOURCE (P0; required cash match contains prohibited State-sourced funds per canonical reference §PA Ag Innovation), F-AGINNOV-PA-PREFERRED-INELIGIBLE-CLAIM (HIGH; inherits PA-DEPT-AG funder gate)."
```

```yaml
artifact_must_not_contain:
  - facts belonging to another artifact          # PA-DEPT-AG funder facts → funders/PA-DEPT-AG.yaml
  - applicant-specific claims
  - uncited generalizations
  - compliance framework internals
  - reviewer-type heuristics
  - case law interpretation
  - other PA Dept of Ag programs                  # Specialty Crop / Conservation Excellence / Dairy / Hardwoods = separate
  - cycles prior to FY26 except as historical-pattern
```

```yaml
strength_test:
  - "Name one concrete drafting decision this artifact changes."
  - "Name one proposal this artifact would reject or downgrade."
  - "Name one Red Team probe this artifact enables."
```

**Answers (PASSED):**

1. **Drafting decision.** Scribe writes the **grant-type-specific eligibility cascade** verification explicitly in §III: *"This proposal claims the [innovation_planning / onsite_project / regional_impact] grant type. Applicant satisfies grant-type-eligibility cascade: [specific cascade tests passed — dollar range within enum bounds; non-state match at required percentage (30% for innovation_planning; 50% for onsite_project + regional_impact); project shape matches grant-type purpose (Exhibit X)]."* Without artifact: generic Ag Innovation pitch without grant-type-cascade verification. With artifact: grant-type-specific cascade verification that state-program officers desk-check.
2. **Proposal rejected.** Logician `F-AGINNOV-TRACK-ELIGIBILITY-CASCADE-MISMATCH` (P0) fails closed when applicant claims a specific grant_type but grant-type-cascade verification fails (e.g., claimed innovation_planning with $150K budget exceeds enum max; claimed onsite_project with 30% match falls short of required 50%; claimed regional_impact with $40K budget below enum min). Saves Scribe from drafting cross-grant-type-mismatched proposals. (Note: gate predicate name retains "TRACK" for backward stability per Pass-1 no-invention rule; semantic intent is grant-type-cascade.)
3. **Red Team probe.** `AGINNOV-PROBE-TRACK-CASCADE-INTEGRITY` asks: *"For the claimed grant_type (innovation_planning / onsite_project / regional_impact), does the applicant satisfy ALL grant-type-specific eligibility-cascade tests (dollar range within enum bounds + non-state match at required percentage + project shape matches grant-type purpose + supporting documentation)? Grant-type-mismatch is state-desk-check rejection vector."*

---

## §B — Codex-shape depth-charter YAML

```yaml
artifact_id: PA-DEPT-AG-AGINNOV-FY26
artifact_family: program
version: depth_charter_v0
lifecycle: draft
validation_status: pre_corpus_hypothesis
runtime_load_status: do_not_load_as_signed_logic
operator_label: depth_charter_v0

one_sentence_job: |
  Equip Scribe/Judge/Red Team/Logician with PA Ag Innovation FY26-specific
  track-eligibility-cascade discipline, state-source match rules, PA-Preferred
  branding integrity, and named-district economic-impact framing.

runtime_consumers:
  scout:
    pre_filter_question: |
      Is the applicant (a) PA-located, (b) eligible under one of the three
      FY26 AGINNOV grant-types (innovation_planning $7.5K–$50K @ 30% match,
      onsite_project $5K–$200K @ 50% match, regional_impact $100K–$2M @ 50%
      match), and (c) using non-State-sourced match funds?
    eligibility_dimensions:
      - pa_locality                       # principal operations in PA per F-AGINNOV-NOT-PA-LOCATED
      - grant_type_cascade                # claimed_grant_type matches eligibility cascade (innovation_planning / onsite_project / regional_impact)
      - match_source_provenance           # match funds NOT sourced from PA State funding (per Pass-0 D-AGINNOV polarity flip)
      - pa_preferred_signal               # competitive scoring: PA-Preferred eligibility of applicant + downstream products
      - named_district_economic_impact    # competitive scoring: legislator-district named impact
    hard_gate_refs:
      - F-AGINNOV-NOT-PA-LOCATED
      - F-AGINNOV-TRACK-ELIGIBILITY-CASCADE-MISMATCH
      - F-AGINNOV-MATCH-USES-STATE-SOURCE
    cross_funder_signal: |
      State-agriculture program funder; routes opportunity TOWARD other PA
      Dept-Ag funder-level programs (Specialty Crop Block Grant pass-through,
      PA Farm Bill programs) and TOWARD USDA-AMS / USDA-RD when applicant
      has federal-track-record. Flags when applicant has 100% State-sourced
      match (F-AGINNOV-MATCH-USES-STATE-SOURCE fires) — must pivot match
      source before draft can proceed.
    operator_assist_required: |
      Escalate to operator when: (a) claimed_grant_type doesn't cleanly map
      to project scope (cascade integrity check fails), (b) PA-Preferred
      eligibility unclear (probe AGINNOV-PROBE-PA-PREFERRED-INTEGRITY),
      (c) state-budget-cycle timeline collision risk (state appropriation
      not yet enacted at planned submission window).
    source_authority: |
      PA-DEPT-AG canonical reference + AGINNOV FY26 program guidelines
      (canonical reference §AGINNOV FY26 Three-Grant-Type Model). Match-
      source dimension source-backed per Pass-0 D-AGINNOV polarity flip
      with canonical-reference citation. Commodity-track legacy prose
      marked [CONJECTURE — Pillar-2 corpus pending] per Pass-1 P1-8.
    prose_summary: |
      DISCOVER pre-filters PA-located applicants matching active-track
      eligibility. VERIFY surfaces FY26 active track list.
  scribe:
    voice_change: |
      Inherits PA-DEPT-AG register (state-program-officer + PA-Preferred +
      named-district + Commonwealth-localized + state-budget-cycle aware).
      AGINNOV-specific overlay: claimed_grant_type (innovation_planning /
      onsite_project / regional_impact) selected explicitly with grant-
      type-specific eligibility cascade verified in §III; non-State-
      sourced match documented in §IV (per Pass-0 D-AGINNOV polarity
      flip); state-budget-cycle-aware timeline in §V.
    section_ordering:
      - "§I PA Farm Bill statutory authority + PA-Preferred branding eligibility verification (inherits PA-DEPT-AG)"
      - "§II Named PA county + Senate + House districts economic-impact framing (inherits PA-DEPT-AG)"
      - "§III claimed_grant_type selection (innovation_planning / onsite_project / regional_impact) + grant-type-specific eligibility cascade verification with supporting Exhibits"
      - "§IV budget + non-State-sourced match documentation"
      - "§V applicant qualifications + state-budget-cycle-aware disbursement timeline"
      - "§VI work plan"
    must_do:
      - "Inherit PA-DEPT-AG scribe.must_do (named county + district; verify PA-Preferred before claiming; PA-source data; Commonwealth-localized formal register)."
      - "Select claimed_grant_type explicitly in §III: innovation_planning ($7.5K–$50K @ 30% non-state match) OR onsite_project ($5K–$200K @ 50% non-state) OR regional_impact ($100K–$2M @ 50% non-state)."
      - "Verify grant-type-specific eligibility cascade with supporting documentation Exhibits per claimed_grant_type."
      - "Document non-State-sourced cash match in §IV — match must NOT include PA-State-sourced funds (Pass-0 D-AGINNOV polarity)."
      - "Document state-budget-cycle awareness in §V — avoid PA-state-budget-reconciliation window (typical June) for disbursement-dependent milestones."
    must_not_do:
      - "Inherit PA-DEPT-AG scribe.must_not_do (no 'innovative' lead; no unverified PA-Preferred; no generic 'rural region'; no national-only data)."
      - "Frame match as State-sourced — F-AGINNOV-MATCH-USES-STATE-SOURCE fails closed (P0)."
      - "Reference the retired commodity-track model (dairy / specialty-crop / hemp / ag-tech) as if it were the active eligibility primitive — Pass-0 D-AGINNOV retired it; use claimed_grant_type enum instead."
      - "Aggregate two grant_types in one proposal — pick innovation_planning, onsite_project, or regional_impact."
    cross_funder_signal: |
      Program-instance under PA-DEPT-AG. Inherits funder-level register
      with AGINNOV-specific grant-type-selection + non-State-match
      overlay. When applicant has scale >$200K and federal-track-record,
      Scout may sister-route to federal USDA-RD-RBDG / USDA-AMS for
      portfolio comparison. State-budget-cycle uncertainty operator-
      escalation trigger inherits from PA-DEPT-AG.
    source_authority: |
      PA-DEPT-AG canonical reference + AGINNOV FY26 program guidelines
      (canonical reference §PA Ag Innovation Grant Types — three-grant-
      type enum + non-state match column). Inherits PA-DEPT-AG funder-
      level scribe register source-authority. Grant-type model source-
      backed per Pass-0 D-AGINNOV + canonical reference. Commodity-track
      legacy prose flagged [CONJECTURE — Pillar-2 corpus pending] per
      Pass-1 P1-8 — Pass 3 (Scribe) strip in progress.
    prose_summary: |
      Reads scribe_section_requirements; applies state-program-officer register
      (inherited); writes grant-type-eligibility-cascade verification in §III;
      state-budget-cycle-aware timeline in §V.

language_register_inheritance:
  parent_charter: PA-DEPT-AG
  inherits:
    - language_register.preferred_terms
    - language_register.suspicious_terms
    - language_register.sentence_shapes_that_work
    - language_register.sentence_shapes_that_fail
    - drafting_implications.scribe_must_do
    - drafting_implications.scribe_must_not_do
  aginnov_specific_overlays:
    preferred_terms:
      - innovation_planning_grant
      - onsite_project_grant
      - regional_impact_grant
      - claimed_grant_type
      - non_state_match
    suspicious_terms:
      - commodity_track                      # retired model per Pass-0 D-AGINNOV; flag legacy references
      - dairy_track                          # retired
      - specialty_crop_track                 # retired
      - hemp_track                           # retired
      - state_sourced_match                  # per Pass-0 D-AGINNOV polarity flip — match must be NON-state-sourced
  note: |
    No standalone language_register / drafting_implications blocks. AGINNOV
    inherits from PA-DEPT-AG funder-level + adds AGINNOV-specific grant-
    type-selection + non-state-match overlays. Commodity-track legacy
    references flagged for Pass-3 prose strip.
  judge: |
    Applies track-specific rubric or criteria-without-weights synthesis;
    favors named-district + PA-Preferred + state-source match.
  red_team: |
    Probes track-cascade integrity, PA-Preferred eligibility, legislator-
    district sensitivity, state-budget-cycle timeline risk.
  logician: |
    PRE-gates F-AGINNOV-TRACK-ELIGIBILITY-CASCADE-MISMATCH (P0),
    F-AGINNOV-MATCH-USES-STATE-SOURCE (HIGH),
    F-AGINNOV-PA-PREFERRED-INELIGIBLE-CLAIM (HIGH; inherits PA-DEPT-AG).

funder_pointer: PA-DEPT-AG
program_summary_one_paragraph: |
  PA Ag Innovation Grant is a recurring PA-state multi-track program funding
  agriculture businesses, processors, and infrastructure projects. Tracks
  vary year-over-year (infrastructure, processing, dairy, hemp, ag-tech).
  Track-specific eligibility cascades load-bearing; track-mismatch is
  state-desk-check rejection vector. Typical dollar ranges $25K-$500K
  varying by track.

claimed_grant_type:
  # PASS-0 fix 2026-05-18: prior charter used a commodity-track model
  # (dairy / specialty-crop / hemp). Per operator canonical reference,
  # PA Ag Innovation runs three grant TYPES (not commodity tracks).
  # Commodity-track logic and historical_tracks list retired below;
  # eligibility cascades attach to grant TYPE, not commodity.
  enum:
    - innovation_planning
    - onsite_project
    - regional_impact
  innovation_planning:
    dollar_range_usd: { min: 7500, max: 50000 }
    non_state_match_pct: 30
    source_required: true
  onsite_project:
    dollar_range_usd: { min: 5000, max: 200000 }
    non_state_match_pct: 50
    source_required: true
  regional_impact:
    dollar_range_usd: { min: 100000, max: 2000000 }
    non_state_match_pct: 50
    source_required: true
  retired_commodity_track_model:
    historical_tracks_pre_pass_0: [infrastructure, processing, dairy, hemp, ag_tech, specialty_crop_value_added]
    note: "Retained for traceability only; do not load as runtime logic."
  cycle_status: "<NEEDED — Pillar 2 verify FY26 cycle dates per grant type>"

eligibility_gates:
  - gate_id: F-AGINNOV-NOT-PA-LOCATED
    gate_type: hard_eligibility_gate
    predicate: "Applicant operations in PA (inherits PA-DEPT-AG funder gate)"
    machine_check:
      field_in_applicant_context: kfr.applicant.primary_operations_state
      operator: eq                                                 # deprecated alias for equals per Discipline 3a.3
      threshold: PA
    on_fail: REJECT_NO_DRAFT
    severity: P0
    source_required: true
    corpus_ref: pending_pillar_2  # canonical reference §PA Ag Innovation Eligibility — project work must occur in Pennsylvania (inherits PA-DEPT-AG funder gate)
    confidence:
      level: medium
      reason: "PA-location requirement is canonical-reference-doc anchored (§PA Ag Innovation Eligibility) + inherits PA-DEPT-AG funder gate"
      promotion_requirement: "PA Ag Innovation Grant program guidance verbatim PA-location text ingested at Pillar-2"
    pass_1_reconciliation_note: "Inherits PA-DEPT-AG funder F-PA-DEPT-AG-NOT-PA-LOCATED. Pass 6 (inheritance) considers whether this program-level gate is redundant."
  - gate_id: F-AGINNOV-TRACK-ELIGIBILITY-CASCADE-MISMATCH
    gate_type: hard_eligibility_gate
    predicate: "Applicant satisfies ALL track-specific eligibility cascade tests for claimed track"
    machine_check:
      operator: matches                                            # composite-shape check; decompose at future pass
      threshold: { track_cascade_verified: true }
    on_fail: REJECT_NO_DRAFT
    severity: P0
    source_required: true
    corpus_ref: pending_pillar_2  # PA Ag Innovation track-eligibility-cascade per grant-type model (Pass-0 D-AGINNOV: claimed_grant_type enum)
    confidence:
      level: low
      reason: "pre_corpus_hypothesis — predicate language references retired commodity-track model; the grant-type model (innovation_planning / onsite_project / regional_impact per Pass-0 D-AGINNOV + canonical reference §PA Ag Innovation Grant Types) supersedes commodity tracks. Predicate text NOT rewritten at Pass 1 (no-invention rule); flagged for Pass 3 (Scribe) systemic strip."
      promotion_requirement: "PA Ag Innovation grant-type cascade documentation per claimed_grant_type enum ingested at Pillar-2"
    pass_1_reconciliation_note: "[CONJECTURE — Pillar-2 corpus pending] Predicate references 'track-specific eligibility cascade' which Pass-0 D-AGINNOV retired in favor of the three-grant-type enum (innovation_planning / onsite_project / regional_impact). The semantic intent of the gate (cascade verification per grant type) is preserved; the surrounding prose still refers to commodity tracks (dairy / specialty-crop / hemp). Pass 3 (Scribe) replaces commodity-track references with grant-type references throughout §A scribe/red_team prose, strength_test answer 1, evidence_ladder strongest, and scribe_section_requirements §III. Pass 1 does NOT rewrite prose."
  - gate_id: F-AGINNOV-MATCH-USES-STATE-SOURCE
    gate_type: hard_eligibility_gate
    # PASS-0 polarity fix 2026-05-18: previous predicate was BACKWARDS
    # (required PA-source match); per operator canonical reference, PA
    # Ag Innovation prohibits State-sourced funds as the required match.
    # PASS-1 reconciliation 2026-05-18: P0/REJECT_NO_DRAFT severity CONFIRMED.
    # Source-authority traceability per Discipline 2: the non-state match
    # requirement is source-backed (canonical reference §PA Ag Innovation
    # Grant Types — Planning 30% non-state; On-site 50% non-state;
    # Regional 50% non-state) AND machine-checkable (match_sources field
    # screen for State-sourced funds). Both Pillar-2 source pin AND
    # machine-checkability satisfied → P0 hard_eligibility_gate confirmed.
    predicate: "Required cash match includes prohibited State-sourced funds"
    machine_check:
      operator: matches                                            # composite-shape check; decompose at future pass
      threshold: { match_contains_state_sourced_funds: true }
    on_fail: REJECT_NO_DRAFT
    severity: P0
    source_required: true
    corpus_ref: "canonical_reference_2026-05-18.md:§PA Ag Innovation Grant Types — non-state match column"
    confidence:
      level: medium
      reason: "Non-state match requirement is canonical-reference-doc anchored (§PA Ag Innovation Grant Types table); pinpoint PA Ag Innovation grant guidance citation pending Pillar-2"
      promotion_requirement: "PA Ag Innovation grant guidance non-state match section ingested at Pillar-2 + operator attestation"
    pass_1_reconciliation_note: "Pass-0 promoted HIGH/WARN_OPERATOR → P0/REJECT_NO_DRAFT (operator flagged for review). Pass 1 CONFIRMS P0/REJECT_NO_DRAFT per Discipline 2 source-authority rule: non-state match requirement is source-backed (canonical reference §PA Ag Innovation Grant Types) AND machine-checkable (match_sources screen). Operator may revert if PA Ag Innovation guidance documents a softer enforcement posture."

scoring_rubric:
  framework: track_specific
  description: |
    PA Ag Innovation publishes rubric per track when available. When state
    declines to publish full rubric, FOIA-derived criteria-without-weights
    synthesis substitutes at Pillar 2.
  publication_pattern: <NEEDED Pillar 2 — varies per track>

scribe_section_requirements:
  - nofo_section_id: §I
    drafting_decisions:
      - decision: "Cite PA Farm Bill statutory authority + PA-Preferred branding eligibility verification."
        rationale: "State-program-officer register expects statutory grounding."
  - nofo_section_id: §II
    drafting_decisions:
      - decision: "Name PA county + Senate + House districts for economic-impact framing (inherits PA-DEPT-AG)."
  - nofo_section_id: §III
    drafting_decisions:
      - decision: "Select claimed_grant_type explicitly (innovation_planning / onsite_project / regional_impact) AND verify grant-type-specific eligibility cascade with supporting documentation Exhibits (dollar range within enum bounds + non-state match at required percentage + project shape matches grant-type purpose)."
        rationale: "Grant-type-mismatch = state-desk-check rejection. (Pass-0 D-AGINNOV retired the commodity-track model in favor of the three-grant-type enum per canonical reference §PA Ag Innovation Grant Types; Pass-3 prose strip aligns this section with the enum.)"
  - nofo_section_id: §V
    drafting_decisions:
      - decision: "Document timeline awareness of PA state-budget-cycle (Jul 1 fiscal year + Jun reconciliation typical) — disbursement schedule avoids reconciliation window."
        rationale: "State-budget-cycle risk is operator-side mitigation."

evidence_ladder:
  strongest:
    - "Grant-type-eligibility-cascade verification with supporting Exhibits (innovation_planning: project shape matches planning purpose + dollar range $7.5K–$50K + 30% non-state match documented; onsite_project: $5K–$200K range + 50% non-state match; regional_impact: $100K–$2M + 50% non-state match + regional scope)"
    - "Named PA county + Senate + House districts"
    - "PA-Preferred eligibility verified (product origin documented per category)"
    - "Cash match from named PA county economic-dev fund / regional foundation (non-State source)"
    - "Prior PA Ag Innovation grant track record"
  acceptable:
    - "Grant-type-eligibility-cascade narrative without explicit Exhibit"
    - "Named PA county without district-level specifics"
    - "PA-Preferred conceptual alignment (eligibility verified but no branding plan)"
  weak:
    - "Grant-type claim without cascade verification"
    - "Generic PA framing without named county"
    - "PA-Preferred claim without product-origin verification"
  unacceptable:
    - "Out-of-state applicant"
    - "Grant-type claim with clear cascade failure (e.g., claimed innovation_planning with budget exceeding $50K enum max; claimed onsite_project with 30% match below required 50%)"
    - "PA-Preferred claim where origin clearly fails standards"
    - "State-sourced match funds (violates F-AGINNOV-MATCH-USES-STATE-SOURCE)"

red_team_probes:
  - probe_id: AGINNOV-PROBE-TRACK-CASCADE-INTEGRITY
    probe_question: "For claimed grant_type (innovation_planning / onsite_project / regional_impact), does applicant satisfy ALL grant-type-specific eligibility-cascade tests with documentation (dollar range within enum bounds + non-state match at required percentage + project shape matches grant-type purpose)?"
    score_impact_if_fails: ADMINISTRATIVE_REJECTION
    pass_3_relabel_note: "Probe_id retains 'TRACK' for backward stability per Pass-1 no-invention rule + Pass-3 no-probe-rewrite rule; semantic intent at Pass-3 LOCK is grant-type-cascade per canonical reference §PA Ag Innovation Grant Types."
  - probe_id: AGINNOV-PROBE-PA-PREFERRED-INTEGRITY
    probe_question: "If PA-Preferred branding claimed, is product origin verified per PA-Preferred standards (PA-grown / produced / processed per category)?"
    score_impact_if_fails: "-3 to -5 + reviewer skepticism"
  - probe_id: AGINNOV-PROBE-STATE-BUDGET-CYCLE-TIMELINE
    probe_question: "Does timeline avoid PA-state-budget-reconciliation window (typical Jun)?"
    score_impact_if_fails: "operational risk + potential disbursement delay"

logician_gates:
  - gate_id: F-AGINNOV-PA-PREFERRED-INELIGIBLE-CLAIM
    gate_type: competitive_scoring_signal
    when: PRE
    severity: HIGH
    predicate_python: "kfr.applicant.claims_pa_preferred_branding and not kfr.product.satisfies_pa_preferred_standards()"
    fail_action: WARN_OPERATOR
    source_required: true
    corpus_ref: pending_pillar_2  # inherits PA-DEPT-AG funder gate F-PA-DEPT-AG-PA-PREFERRED-INELIGIBLE-CLAIM
    confidence:
      level: low
      reason: "Inherits PA-DEPT-AG funder gate; PA-Preferred standards documentation pending"
      promotion_requirement: "PA-Preferred standards document per category ingested at Pillar-2"
    pass_1_reconciliation_note: "Inherits PA-DEPT-AG funder F-PA-DEPT-AG-PA-PREFERRED-INELIGIBLE-CLAIM. Pass 6 (inheritance) considers whether this program-level gate is redundant."

source_backing:
  corpus_refs:
    - "<NEEDED — Pillar 2: PA Ag Innovation FY26 RFP per active track>"
    - "<NEEDED — Pillar 2: rubric per track (PA Right-to-Know FOIA if needed)>"
    - "<NEEDED — Pillar 2: FY24 + FY25 PA Ag Innovation award rosters per track>"
    - "<NEEDED — Pillar 2: grant-type-specific eligibility cascade documentation (innovation_planning / onsite_project / regional_impact per canonical reference §PA Ag Innovation Grant Types)>"
  confidence: LOW pre-corpus.
  unresolved_questions:
    - "FY26 active track list + dollar caps per track"
    - "Rubric publication discipline per track (full rubric vs criteria-only)"
    - "Recent state-desk-check rejection patterns"
```

---

## §1 — What "depth" means for THIS artifact

PA Ag Innovation FY26 program-level depth is the **grant-type-eligibility-cascade decision substrate** — grant-type-specific eligibility cascades per the three-grant-type enum (innovation_planning $7.5K–$50K @ 30% non-state match / onsite_project $5K–$200K @ 50% non-state / regional_impact $100K–$2M @ 50% non-state) per canonical reference §PA Ag Innovation Grant Types, state-source match rules (non-State-sourced match required — Pass-0 D-AGINNOV polarity), PA-Preferred integrity. Inherits PA-DEPT-AG funder depth-charter register (state-program-officer + PA-Preferred + named-district economic-impact + state-budget-cycle awareness). (Pass-0 D-AGINNOV retired the prior commodity-track model — dairy / specialty-crop / hemp / ag-tech — in favor of this grant-type enum; Pass-3 Scribe strip aligns this §1 + §A + §B prose with the enum. Historical commodity-track references retained at `claimed_grant_type.retired_commodity_track_model.historical_tracks_pre_pass_0` for audit-trail traceability only.)

**Codex same-prompt-with/without test:**
- **Without** — Scribe writes generic PA Ag Innovation pitch without grant-type-cascade verification. Reviewers desk-check grant-type-mismatch → admin rejection.
- **With** — Scribe writes grant-type-eligibility-cascade verification with Exhibits in §III (claimed_grant_type selected explicitly + dollar range + non-state match percentage + project shape); cites PA Farm Bill statutory authority in §I; names PA county + Senate/House districts in §II; documents state-budget-cycle-aware timeline in §V. Judge applies grant-type-specific rubric. Red Team probes grant-type-cascade integrity + PA-Preferred + state-budget-cycle timeline. Logician fails closed on non-PA + grant-type-cascade-mismatch + State-sourced match.

---

## §2 — Primary sources in scope

| Corpus | Sources | Path | Count |
|--------|---------|------|-------|
| `nofos/` | FY26 RFP per active track; PA Dept of Ag program-overview | Public PA Dept of Ag | 2-5 |
| `rubrics/` | FY26 rubric per track (Right-to-Know FOIA if needed) | PA Dept of Ag / FOIA | 1-3 best-effort |
| `awards/` | FY24 + FY25 award rosters per track | Public PA Dept of Ag + state budget | 2-3 |
| `guidance/` | Track-eligibility-cascade documentation; PA-Preferred standards | PA public records | 1-3 |

Case law OUT OF SCOPE.

---

## §3 — Tier classification

| Field | Tier |
|-------|:----:|
| Default | `1` |
| `rubric.weighted_dimensions[]` | `1` (when published) or `2` (FOIA-synthesis) |
| `eligibility_rules[]` | `1` |
| `legislator_district_sensitivity_notes[]` | `3` |
| `pa_preferred_branding_norms[]` | `2` |
| `reviewer_relationship_notes[]` | `3` |

---

## §4 — Refresh cadence

`per_cycle` (annually-cycled, multi-track stagger). `F-FID-STALE-RUBRIC` applies.

---

## §5 — Calibration applicant pair

`food_systems` (CIC-01) × `operating_capacity` (CLC-03).

---

## §6 — Done definition

`audited` per SARE-NE / USDA-RD discipline.

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

- Other PA Dept of Ag programs (Conservation Excellence; Specialty Crop Block; Hardwoods; Dairy Investment)
- PA Ag Innovation cycles prior to FY26 except as historical reference
- Compliance framework internals
- Reviewer-type heuristics
- Per-applicant PA-Preferred branding alignment (→ `orgs/<slug>/`)
- Case law interpretation
- Drafting actual PA Ag Innovation applications (this artifact carries depth-knowledge; drafting belongs to Scribe + applicant)
- FIT Farms dogfooding this program at v0.1 (per CLAUDE.md "What NOT to Do" — narrow v0.1 demo-target rule; does not affect this artifact's existence in shared FID layer)
