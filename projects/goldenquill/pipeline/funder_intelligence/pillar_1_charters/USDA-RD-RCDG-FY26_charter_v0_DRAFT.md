# Depth Charter — `USDA-RD-RCDG-FY26` (Rural Cooperative Development Grant)

> **Pillar 1 of 4** per `pipeline/planning/funder_intelligence_database_research_project_2026-05-16.md` §3.1.
> **Quality bar** per `docs/FID_ARTIFACT_OPTIMIZATION_PRINCIPLES_2026-05-18.md` §1 + §2 + Codex framing.
> **Status: DEPTH CHARTER v0 (pre-corpus hypothesis; do not load as signed logic)** — re-authored to Codex yaml shape per operator directive 2026-05-18. Inherits USDA-RD funder depth charter (commit 071408b) + NCBA-CLUSA cooperative-form-authenticity register.
>
> **[CONJECTURE — Pillar-2 corpus pending]** RCDG FY26 NOFO not yet pulled. `F-FID-FACT-ORPHAN` enforces at L-005.

---

## Header

| Field | Value |
|------:|:------|
| `artifact_id` | `USDA-RD-RCDG-FY26` |
| `artifact_family` | `program` |
| `funder_pointer` | `USDA-RD` |
| `version` | `depth_charter_v0` |
| `lifecycle` | `draft` |
| `phase` | `1 — exemplar pair` |
| `pillar_2_dispatch_position` | **4 of 6** |

---

## §A — Adversarial pre-checks

```yaml
runtime_consumer:
  scout:
    reads_fields: [scout_verify.live_check_url, eligibility_gates]
    stage: both
    decision_changed: "Scout DISCOVER restricts to nonprofit cooperative development center applicants serving rural areas. VERIFY checks FY26 NOFO URL."
  scribe:
    reads_fields: [scribe_section_requirements, scoring_rubric, drafting_implications]
    stage: both
    decision_changed: "Scribe leads §I with cooperative-development-center qualifications + named TA staff + rural service area; leads §II with cooperative-form-authenticity test for SUB-COOPERATIVES the applicant develops (Rochdale operationalization + member-ownership records); leads §III with TA-delivery methodology + measurable cooperative-development outcomes."
  judge:
    reads_fields: [scoring_rubric, judge_scoring_map]
    stage: rubric_scoring
    decision_changed: "Judge applies RCDG-specific 4-cluster rubric (Qualifications of Applicant / Delivery + Impact of Services / Demonstrated Capacity / Expected Outcomes). Tie-breakers favor cooperative-form-authentic applicants and sub-cooperative-impact-tracking discipline."
  red_team:
    reads_fields: [red_team_probes]
    stage: probe_target_selection
    # Pass-1 reconciliation 2026-05-18 per D-RCDG follow-up: §A red_team prose
    # aligned with widened applicant-type gate. Prior framing implied applicant
    # had to be an already-operating CDC; updated framing tests applicant's
    # capacity to establish OR operate a center per canonical reference.
    decision_changed: "Red Team probes RCDG-specific failure modes: applicant's cooperative-development-center capacity (TA staff + prior outcomes + sister-coop network) — whether establishing OR operating an existing center; sub-cooperative authenticity (RCDG funds TA to develop OTHER cooperatives — those sub-cooperatives must satisfy cooperative form authenticity); rural-area service threshold honesty; matching-funds (when required) discipline."
  logician:
    reads_fields: [eligibility_gates, disqualifiers, logician_gates]
    stage: PRE
    # Pass-1 reconciliation 2026-05-18 per D-RCDG follow-up: §A parenthetical
    # reconciled with widened §B predicate. Prior text "applicant not a 501(c)
    # nonprofit cooperative development center" described the pre-Pass-0 narrow
    # predicate; §B now widens to eligible nonprofit institution / nonprofit
    # corporation / eligible higher-ed institution (predicate does NOT require
    # applicant be an already-operating CDC; the grant funds establishment OR
    # operation per canonical reference §USDA-RD RCDG Eligibility).
    decision_changed: "Logician fires F-RCDG-INELIGIBLE-APPLICANT-TYPE (P0; applicant not in {nonprofit_institution, nonprofit_corporation, eligible_higher_ed_institution}), F-RCDG-RURAL-AREA-INELIGIBLE (P0; rural-area population threshold per 7 CFR 4284-F), F-RCDG-CENTER-CAPACITY-UNDOCUMENTED (HIGH; capacity to establish or operate the cooperative development center not documented), F-RCDG-TA-CAPACITY-UNDOCUMENTED (HIGH; TA-delivery capacity not documented)."
```

```yaml
artifact_must_not_contain:
  - facts belonging to another artifact          # USDA-RD funder + NCBA-CLUSA funder
  - applicant-specific claims
  - uncited generalizations
  - compliance framework internals
  - reviewer-type heuristics
  - case law interpretation
  - other USDA-RD programs
  - cycles prior to FY26 except as historical-pattern
```

```yaml
strength_test:
  - "Name one concrete drafting decision this artifact changes."
  - "Name one proposal this artifact would reject or downgrade."
  - "Name one Red Team probe this artifact enables."
```

**Answers (PASSED):**

1. **Drafting decision.** Scribe documents **sub-cooperative cooperative-form authenticity test** in §III: *"Sub-cooperatives the applicant develops via this RCDG TA must satisfy Rochdale-7-principles operationalization, member-ownership recordkeeping, and patronage-distribution discipline. The applicant's TA methodology includes [specific curriculum + measurable cooperative-form maturity indicators]."* Without artifact: generic "we will support cooperative development" framing. With artifact: Rochdale-grounded sub-cooperative-development methodology.
2. **Proposal rejected.** Logician `F-RCDG-INELIGIBLE-APPLICANT-TYPE` (P0) fails closed any applicant that is not an eligible nonprofit institution / nonprofit corporation / eligible higher-ed institution per the current NOFA (Pass-0 widening 2026-05-18 per canonical reference §USDA-RD RCDG Eligibility — applicant does NOT need to already be a cooperative development center; the grant funds establishment OR operation of a center). Saves Scribe from drafting RCDG proposals for ineligible-entity-type applicants.
3. **Red Team probe.** `RCDG-PROBE-SUB-COOPERATIVE-AUTHENTICITY` asks: *"Will sub-cooperatives developed via this RCDG TA satisfy all 7 Rochdale principles, member-ownership recordkeeping, and patronage-distribution? Or is the TA framed as 'cooperative-like business development' without authentic cooperative-form discipline?"*

---

## §B — Codex-shape depth-charter YAML

```yaml
artifact_id: USDA-RD-RCDG-FY26
artifact_family: program
version: depth_charter_v0
lifecycle: draft
validation_status: pre_corpus_hypothesis
runtime_load_status: do_not_load_as_signed_logic
operator_label: depth_charter_v0

one_sentence_job: |
  Equip Scribe/Judge/Red Team/Logician with RCDG FY26-specific eligibility
  (nonprofit cooperative development center + rural area), 4-cluster rubric,
  sub-cooperative authenticity discipline, and TA-delivery measurement.

runtime_consumers:
  scout:
    pre_filter_question: |
      Is the applicant a nonprofit institution / nonprofit corporation /
      eligible higher-education institution (widened predicate per Pass-0
      D-RCDG fix) operating as or building Cooperative Development Center
      capacity, AND does the project serve rural areas per 7 CFR 4284-F?
    eligibility_dimensions:
      - eligible_applicant_type           # nonprofit_institution / nonprofit_corporation / eligible_higher_ed (post-Pass-0 widening)
      - rural_area_service                # service area meets RD rural-area definition (P1-10 placeholder threshold flagged)
      - cdc_capacity                      # Cooperative Development Center qualifications + named TA staff
      - sub_cooperative_focus             # project advances sub-cooperative development (cooperative form authenticity)
      - sam_uei_baseline                  # SAM-active + UEI present
    hard_gate_refs:
      - F-RCDG-INELIGIBLE-APPLICANT-TYPE
      - F-RCDG-RURAL-AREA-INELIGIBLE
    cross_funder_signal: |
      Federal-program program-instance funder under USDA-RD funder-level.
      Routes opportunity LATERALLY to NCBA-CLUSA when applicant has direct
      cooperative-form authenticity needs, to USDA-RD-RBDG when project
      focus shifts toward business-development beneficiaries, and TOWARD
      USDA-AMS / state-level coop programs when sub-cooperative TA scope
      narrows.
    operator_assist_required: |
      Escalate to operator when: (a) CDC capacity is partial / nascent
      (F-RCDG-TA-CAPACITY-UNDOCUMENTED HIGH; HIGH companion
      F-RCDG-CENTER-CAPACITY-UNDOCUMENTED WARN_OPERATOR fires per Pass-0
      widening), (b) rural-area threshold uses placeholder predicate (P1-10
      `gt 0` near-degenerate proxy; operator must confirm actual 7 CFR
      4284-F rural-area population threshold pending Pillar-2 source-pin),
      (c) sub-cooperative authenticity unclear for proposed beneficiaries.
    source_authority: |
      USDA-RD RCDG 7 CFR 4284-F + FY26 NOFO (canonical reference §USDA-RD
      RCDG eligible-applicant-type + CDC qualifications). Applicant-type
      widening source-pinned per Pass-0 D-RCDG. Rural-area threshold
      placeholder flagged Pass-1 P1-10 for Pillar-2 source-acquisition.
    prose_summary: |
      DISCOVER restricts to 501(c) nonprofit cooperative development center
      applicants serving rural areas.
  scribe:
    voice_change: |
      Inherits USDA-RD register; composes NCBA-CLUSA cooperative-
      authenticity overlay for sub-cooperatives. RCDG-specific framing:
      "we are establishing or operating a cooperative development center"
      (NOT "we are a cooperative seeking direct grant funding"); CDC
      qualifications + named TA staff lead §I; sub-cooperative
      authenticity in §II.
    section_ordering:
      - "§I CDC applicant identity + named TA staff + cooperative-development-mission"
      - "§II Sub-cooperative authenticity (composes NCBA-CLUSA Rochdale-principles overlay for proposed beneficiary cooperatives)"
      - "§III TA-delivery methodology (curriculum + facilitator + cadence + outcome-tracking)"
      - "§IV match narrative (program match guidance per current NOFO)"
      - "§V CDC qualifications + prior outcomes"
      - "§VI work plan"
    must_do:
      - "Inherit USDA-RD scribe.must_do (rural-area service-area citation, public-purpose framing)."
      - "Compose NCBA-CLUSA Rochdale-principles overlay when describing sub-cooperative beneficiaries (one-member-one-vote + patronage explicit)."
      - "Lead §I with CDC identity + named TA staff."
      - "Describe TA delivery methodology (curriculum + facilitator + cadence) explicitly in §III."
      - "Document center capacity (staff + curriculum + prior outcomes) — F-RCDG-CENTER-CAPACITY-UNDOCUMENTED warns when absent."
    must_not_do:
      - "Inherit USDA-RD scribe.must_not_do (don't lead with 'innovative')."
      - "Frame applicant as direct-to-cooperative grantee — RCDG funds CDCs, not cooperatives themselves."
      - "Use vague 'we will provide TA' without methodology + cadence."
      - "Submit sub-cooperative authenticity claim without bylaws / governance citation."
    cross_funder_signal: |
      Program-instance under USDA-RD; natural pair with NCBA-CLUSA
      cooperative-authenticity overlay. Distinct from sister USDA-RD
      program-instances RBDG (small-and-emerging beneficiary) and CFP
      (essential-community-facility). When applicant is itself a
      cooperative (not a CDC), Scout routes to USDA-AMS VAPG or
      USDA-RD RBDG, not RCDG.
    source_authority: |
      USDA-RD RCDG 7 CFR 4284-F + canonical reference §USDA-RD RCDG
      (eligibility widening per Pass-0 D-RCDG). Inherits USDA-RD funder-
      level scribe register. Cooperative-form authenticity overlay
      source-backed by NCBA-CLUSA canonical reference §NCBA CLUSA Use
      in Grants.
    prose_summary: |
      Leads §I with CDC qualifications + named TA staff; §II with cooperative-
      form authenticity for sub-cooperatives; §III with TA-delivery methodology.

language_register_inheritance:
  parent_charter: USDA-RD
  composed_overlay: NCBA-CLUSA
  inherits:
    - language_register.preferred_terms
    - language_register.suspicious_terms
    - language_register.sentence_shapes_that_work
    - language_register.sentence_shapes_that_fail
    - drafting_implications.scribe_must_do
    - drafting_implications.scribe_must_not_do
  rcdg_specific_overlays:
    preferred_terms:
      - cooperative_development_center
      - technical_assistance
      - sub_cooperative
      - cooperative_form_authenticity        # composed from NCBA-CLUSA
    suspicious_terms:
      - cooperative_like                     # composed from NCBA-CLUSA
      - direct_to_cooperative                # RCDG-specific misreading flag
  note: |
    No standalone language_register / drafting_implications blocks. RCDG
    inherits from USDA-RD funder-level AND composes NCBA-CLUSA cooperative-
    authenticity overlay when describing sub-cooperative beneficiaries.
  judge: |
    Applies 4-cluster rubric (Qualifications / Delivery + Impact / Capacity /
    Outcomes); favors cooperative-form-authentic applicants.
  red_team: |
    Probes applicant CDC capacity, sub-cooperative authenticity, rural-area
    service threshold, matching-funds discipline.
  logician: |
    PRE-gates F-RCDG-INELIGIBLE-APPLICANT-TYPE (P0),
    F-RCDG-RURAL-AREA-INELIGIBLE (P0),
    F-RCDG-TA-CAPACITY-UNDOCUMENTED (HIGH).

funder_pointer: USDA-RD
program_summary_one_paragraph: |
  USDA Rural Development's Rural Cooperative Development Grant funds nonprofit
  cooperative development centers (CDCs) to provide TA to rural cooperatives
  and emerging cooperative businesses. RCDG is the natural pair with
  NCBA-CLUSA funder artifact — the cooperative-form authenticity test that
  NCBA-CLUSA applies at funder level applies to RCDG sub-cooperatives at
  program level. Typical award cap ~$250K.

nofo:
  source_url: <NEEDED Pillar 2>
  closing_date: <NEEDED Pillar 2>
  cycle_status: <NEEDED — annual-cycle expected>

eligibility_gates:
  - gate_id: F-RCDG-INELIGIBLE-APPLICANT-TYPE
    gate_type: hard_eligibility_gate
    predicate: "Applicant is an eligible nonprofit institution / nonprofit corporation / eligible higher-ed institution per current NOFO"
    machine_check:
      operator: matches                                            # composite-shape check; decompose at future pass
      threshold: { entity_type_in: [nonprofit_institution, nonprofit_corporation, eligible_higher_ed_institution] }
    on_fail: REJECT_NO_DRAFT
    severity: P0
    source_required: true
    corpus_ref: "<NEEDED — Pillar 2: 7 CFR 4284-F + current RCDG NOFO eligible-applicant section>"
    confidence:
      level: medium
      reason: "Predicate widened at Pass 0 (D-RCDG) per canonical reference §USDA-RD RCDG Eligibility; pinpoint 7 CFR 4284-F citation pending"
      promotion_requirement: "7 CFR 4284-F + current RCDG NOFA eligible-applicant verbatim text ingested at Pillar-2"
  - gate_id: F-RCDG-CENTER-CAPACITY-UNDOCUMENTED
    gate_type: competitive_scoring_signal
    predicate: "Applicant lacks credible plan/capacity to establish or operate rural cooperative development center"
    machine_check:
      operator: matches
      threshold: { center_capacity_plan_documented: true }
    on_fail: WARN_OPERATOR
    severity: HIGH
    source_required: false
    corpus_ref: "<NEEDED — Pillar 2: USDA-RD RCDG center-capacity guidance>"
    confidence:
      level: low
      reason: "pre_corpus_hypothesis — companion gate added at Pass 0 (D-RCDG) to widen applicant-type while preserving capacity-rigor as warning"
      promotion_requirement: "USDA-RD RCDG center-capacity scoring band documentation ingested at Pillar-2"
  - gate_id: F-RCDG-RURAL-AREA-INELIGIBLE
    gate_type: hard_eligibility_gate
    predicate: "Service area includes rural area per 7 CFR Part 4284-F threshold"
    machine_check:
      field_in_applicant_context: kfr.applicant.service_area_rural_population
      operator: gt                                                 # deprecated alias for greater_than per Discipline 3a.3
      threshold: 0
    on_fail: REJECT_NO_DRAFT
    severity: P0
    source_required: true
    corpus_ref: "<NEEDED — Pillar 2: 7 CFR Part 4284-F rural-area threshold>"
    confidence:
      level: low
      reason: "pre_corpus_hypothesis — predicate uses placeholder 'population gt 0' as proxy; actual 7 CFR 4284-F rural-area threshold pending"
      promotion_requirement: "7 CFR Part 4284-F rural-area threshold verbatim ingested at Pillar-2"
    pass_1_reconciliation_note: "Threshold value `0` is a placeholder proxy ('any rural population suffices' = no actual rural-area floor encoded). Actual RD rural-area definition has program-specific population thresholds. Pillar-2 source-acquisition must surface and encode the correct threshold; current predicate would fire only on service-area-with-zero-rural-population which is a near-degenerate check."
  - gate_id: F-RCDG-TA-CAPACITY-UNDOCUMENTED
    gate_type: competitive_scoring_signal
    predicate: "TA delivery capacity documented (staff + curriculum + prior outcomes)"
    machine_check:
      operator: matches
      threshold: { has_named_ta_staff: true, has_curriculum: true, has_prior_outcomes: true }
    on_fail: WARN_OPERATOR
    severity: HIGH
    source_required: false
    corpus_ref: "<NEEDED — Pillar 2: USDA-RD RCDG scoring rubric — TA capacity criterion>"
    confidence:
      level: low
      reason: "pre_corpus_hypothesis — TA-capacity-as-scoring-criterion canonical-reference anchored; specific evidence threshold pending"
      promotion_requirement: "RCDG FY26 scoring rubric criterion text ingested at Pillar-2"

scoring_rubric:
  total_points: 100  # NEEDED verify FY26
  criteria:
    - criterion_id: RCDG-RUBRIC-QUALIFICATIONS
      name: "Qualifications of the Applicant"
      weight_pct: <NEEDED — historical ~25%>
      reviewer_expectation: "Named TA staff with CDC experience + prior RCDG track record + sister-CDC partnerships."
    - criterion_id: RCDG-RUBRIC-DELIVERY-IMPACT
      name: "Delivery + Impact of Services"
      weight_pct: <NEEDED — historical ~25%>
      reviewer_expectation: "TA methodology specific + sub-cooperative impact measurement plan + Rochdale-operationalization curriculum."
    - criterion_id: RCDG-RUBRIC-DEMONSTRATED-CAPACITY
      name: "Demonstrated Capacity"
      weight_pct: <NEEDED — historical ~25%>
      reviewer_expectation: "Prior CDC track record + financial-stewardship evidence + sub-cooperative outcomes data."
    - criterion_id: RCDG-RUBRIC-EXPECTED-OUTCOMES
      name: "Expected Outcomes"
      weight_pct: <NEEDED — historical ~25%>
      reviewer_expectation: "Sub-cooperatives developed = N; sub-coop members = M; sub-coop revenue = $X; cooperative-form maturity indicators per sub-coop."

scribe_section_requirements:
  - nofo_section_id: §I  # Project Summary
    drafting_decisions:
      - decision: "Lead with applicant CDC qualifications + named TA staff + sister-CDC partnerships."
        rubric_ref: RCDG-RUBRIC-QUALIFICATIONS
  - nofo_section_id: §III  # TA Methodology + Sub-Cooperative Development
    drafting_decisions:
      - decision: "Document sub-cooperative cooperative-form authenticity test (Rochdale operationalization + member-ownership + patronage-distribution) as the applicant's TA-delivery framework."
        rubric_ref: RCDG-RUBRIC-DELIVERY-IMPACT
      - decision: "Specify TA curriculum with cooperative-form-maturity indicators per sub-coop."
        rubric_ref: RCDG-RUBRIC-DELIVERY-IMPACT
  - nofo_section_id: §IV  # Outcomes
    drafting_decisions:
      - decision: "Quantify sub-cooperatives developed + sub-coop members + sub-coop revenue + cooperative-form-maturity indicators."
        rubric_ref: RCDG-RUBRIC-EXPECTED-OUTCOMES

evidence_ladder:
  strongest:
    - "Prior RCDG track record with documented sub-cooperative outcomes"
    - "Named TA staff with CDC-specific experience + prior cooperative-form-maturity outcomes"
    - "Sister-CDC partnerships + NCBA-CLUSA network engagement"
    - "Curriculum with Rochdale-operationalization framework"
  acceptable:
    - "Prior cooperative-development work without RCDG funding history"
    - "Named TA staff with cooperative-form expertise"
  weak:
    - "Generic 'cooperative-friendly business development' framing"
    - "TA delivery without cooperative-form-maturity measurement"
  unacceptable:
    - "Non-CDC applicant (501(c)(3) nonprofit without CDC status)"
    - "TA framed as 'cooperative-like' without Rochdale discipline"

red_team_probes:
  - probe_id: RCDG-PROBE-SUB-COOPERATIVE-AUTHENTICITY
    probe_question: "Will sub-cooperatives developed via RCDG TA satisfy all 7 Rochdale principles + member-ownership + patronage-distribution?"
    targets_rubric_criterion: RCDG-RUBRIC-DELIVERY-IMPACT
    score_impact_if_fails: "-5 to -10"
  - probe_id: RCDG-PROBE-CDC-CAPACITY
    probe_question: "Is applicant CDC capacity documented (named TA staff + prior outcomes + sister-CDC engagement)?"
    targets_rubric_criterion: RCDG-RUBRIC-QUALIFICATIONS
    score_impact_if_fails: "-5"
  - probe_id: RCDG-PROBE-RURAL-AREA-SERVICE
    probe_question: "Does service area include rural area per 7 CFR 4284-F threshold (not just rural-adjacent)?"
    score_impact_if_fails: ADMINISTRATIVE_REJECTION

source_backing:
  corpus_refs:
    - "<NEEDED — Pillar 2: RCDG FY26 NOFO>"
    - "<NEEDED — Pillar 2: RCDG FY26 scoring rubric>"
    - "<NEEDED — Pillar 2: FY24 + FY25 RCDG award rosters + cooperative-development-center grantee patterns>"
    - "<NEEDED — Pillar 2: 7 CFR Part 4284-F regulatory text>"
    - "<NEEDED — Pillar 2: USDA-RD interpretive guidance on 'cooperative' definition>"
  confidence: LOW pre-corpus.
  unresolved_questions:
    - "FY26 rubric weights"
    - "Whether RCDG accepts limited-cooperative-association sub-coop forms"
    - "Cross-CDC peer-review panel composition"
```

---

## §1 — What "depth" means for THIS artifact

RCDG FY26 program-level depth is the **cooperative-development-center decision substrate** — CDC eligibility, sub-cooperative authenticity (Rochdale), TA-delivery methodology, measurable cooperative-form-maturity outcomes. Inherits USDA-RD funder-level register + NCBA-CLUSA cooperative-form discipline.

**Codex same-prompt-with/without test:**
- **Without** — Scribe writes generic "we will support cooperative development" framing. Sub-cooperative authenticity not tested. Reviewers can't score cooperative-form-maturity outcomes.
- **With** — Scribe documents CDC qualifications + sub-cooperative Rochdale-operationalization curriculum + cooperative-form-maturity indicators per sub-coop. Judge applies 4-cluster rubric. Red Team probes sub-cooperative authenticity + CDC capacity + rural-area service. Logician fails closed on non-CDC applicants + rural-area threshold + TA-capacity gaps.

---

## §2 — Primary sources in scope

| Corpus | Sources | Path | Count |
|--------|---------|------|-------|
| `nofos/` | RCDG FY26 NOFO + Grants.gov + Federal Register | Grants.gov | 1-3 |
| `rubrics/` | RCDG FY26 scoring rubric | NOFO appendix / FOIA | 1 |
| `awards/` | FY24 + FY25 RCDG rosters; CDC grantee patterns | USAspending.gov + USDA-RD | 2-3 |
| `statutory/` | 7 CFR Part 4284-F | Federal Register | 1-2 |
| `guidance/` | USDA-RD "cooperative" definition; rural-area methodology | USDA-RD | 1-3 |

Case law OUT OF SCOPE.

---

## §3 — Tier classification

| Field | Tier |
|-------|:----:|
| Default | `1` |
| `rubric.weighted_dimensions[]` | `1` |
| `eligibility_rules[]` | `1` |
| `cooperative_form_authenticity_heuristics[]` | `2` |
| `reviewer_relationship_notes[]` | `3` |

---

## §4 — Refresh cadence

`per_cycle`. `F-FID-STALE-RUBRIC` applies.

---

## §5 — Calibration applicant pair

`cooperative` (CIC-05) primary; `food_systems` (CIC-01) overlay for cooperative-development-center-serving-food-coops.

---

## §6 — Done definition

`audited` per SARE-NE / USDA-RD discipline; NCBA-CLUSA cross-reference required at L-005.

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

- Other USDA-RD programs — separate artifacts
- RCDG cycles prior to FY26 except as historical reference
- Compliance internals (→ `compliance_cascades/`)
- Reviewer-type heuristics (→ `reviewer_heuristics/`)
- Per-applicant cooperative-form documentation (→ `orgs/<slug>/`; Law 3 org-isolation enforces separation between any two distinct legal entities even when they share branding or operator)
- Sub-cooperative beneficiary detail (lives in applicant's post-award reporting)
- Case law interpretation
