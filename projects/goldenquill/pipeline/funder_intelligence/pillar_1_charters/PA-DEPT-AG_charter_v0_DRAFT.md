# Depth Charter — `PA-DEPT-AG` (funder behavior profile)

> **Pillar 1 of 4** per `pipeline/planning/funder_intelligence_database_research_project_2026-05-16.md` §3.1.
> **Quality bar** per `docs/FID_ARTIFACT_OPTIMIZATION_PRINCIPLES_2026-05-18.md` §1 + §2 + Codex framing.
> **Status: DEPTH CHARTER v0 (pre-corpus hypothesis; do not load as signed logic)** — re-authored to Codex yaml shape per operator directive 2026-05-18.
>
> **[CONJECTURE — Pillar-2 corpus pending]** All PA-Dept-Ag-specific funder-fact claims operator-asserted; Pillar-2 corpus assembly (PA Dept of Ag strategic + PA Farm Bill legislative refs + agency-aggregate awards + Right-to-Know synthesis) promotes each. `F-FID-FACT-ORPHAN` enforces.

---

## Header

| Field | Value |
|------:|:------|
| `artifact_id` | `PA-DEPT-AG` |
| `artifact_family` | `funder` |
| `version` | `depth_charter_v0` |
| `lifecycle` | `draft` |
| `phase` | `1 — exemplar pair` |

---

## §A — Adversarial pre-checks

```yaml
runtime_consumer:
  scout:
    reads_fields: [program_roster, geographic_eligibility]
    stage: DISCOVER
    decision_changed: "Scout DISCOVER restricts PA-Dept-Ag radar to PA-located operations (state-program geographic-eligibility is hard gate; non-PA applicants downgrade to OUT_OF_SCOPE). PA-Preferred-eligible applicants tagged for register-alignment scoring."
  scribe:
    reads_fields: [funder_dialect, language_register, drafting_implications]
    stage: scaffold
    decision_changed: "Scribe applies state-program-officer register: PA-Preferred branding alignment in §I (soft scoring lever), legislator-district economic-impact framing in §II (politically-aware), PA-Farm-Bill statutory authority citation when applicable, state-budget-line-item alignment in §IV. Distinct from federal-program-officer register on the political-awareness axis."
  judge:
    reads_fields: [judge_implications]
    stage: cross_check
    decision_changed: "Judge cross-checks PA-economic-impact dimension + PA-Preferred branding alignment + state-budget-fit dimensions; rewards drafts with named PA county/region impact framing and PA-Preferred-eligible products. Distinct from federal scoring on political-awareness."
  red_team:
    reads_fields: [red_team_probe_seeds]
    stage: probe_target_selection
    decision_changed: "Red Team probes PA-state-specific failure modes: PA-Preferred branding eligibility (product origin verification), legislator-district sensitivity (avoid framing that politically dis-aligns with PA budget cycle), state-budget-reconciliation-timing risks, PA Right-to-Know responsiveness if rubric / scoring documentation is FOIA-derived."
  logician:
    reads_fields: [eligibility_gates, logician_gate_candidates]
    stage: PRE
    decision_changed: "Logician fires PA-Dept-Ag funder-wide PRE-gates: F-PA-DEPT-AG-NOT-PA-LOCATED (P0; applicant operations not in PA), F-PA-DEPT-AG-PA-PREFERRED-INELIGIBLE-CLAIM (HIGH; PA-Preferred branding claimed but product origin doesn't satisfy PA-Preferred standards)."
```

```yaml
artifact_must_not_contain:
  - facts belonging to another artifact          # Ag Innovation FY26 rubric → programs/PA-DEPT-AG-AGINNOV-FY26.yaml
  - applicant-specific claims
  - uncited generalizations
  - compliance framework internals
  - reviewer-type heuristics
  - other PA-state agencies                      # PA-DCED, PA-DEP, PCCD, PHMC separate
  - case law interpretation
```

```yaml
strength_test:
  - "Name one concrete drafting decision this artifact changes."
  - "Name one proposal this artifact would reject or downgrade."
  - "Name one Red Team probe this artifact enables."
```

**Answers (PASSED):**

1. **Drafting decision.** Scribe leads §II with **named PA county / region + economic-impact framing** (e.g., "this project creates [N] FTE jobs in Westmoreland County's PA Senate District [X] and PA House District [Y]"). Without artifact: generic "rural Pennsylvania" framing. With artifact: explicit district-level impact framing that state-program officers track against constituent-economic-impact patterns.
2. **Proposal rejected.** Logician `F-PA-DEPT-AG-NOT-PA-LOCATED` (P0) fails closed any application where applicant primary operations are not in PA. Saves Scribe from drafting state-program proposals for out-of-state applicants.
3. **Red Team probe.** `PA-DEPT-AG-PROBE-PA-PREFERRED-INTEGRITY` asks: *"If applicant claims PA-Preferred branding alignment, does product origin satisfy PA-Preferred standards (PA-grown OR PA-produced OR PA-processed depending on category)? PA-Preferred claim without underlying eligibility is a known reviewer downgrade vector."*

---

## §B — Codex-shape depth-charter YAML

```yaml
artifact_id: PA-DEPT-AG
artifact_family: funder
version: depth_charter_v0
lifecycle: draft
validation_status: pre_corpus_hypothesis
runtime_load_status: do_not_load_as_signed_logic
operator_label: depth_charter_v0

one_sentence_job: |
  Equip every PA Dept of Ag program draft (Ag Innovation / Specialty Crop /
  Conservation Excellence / Dairy Investment / Hardwoods / etc.) with PA-
  state-program-officer register, PA-Preferred branding-alignment discipline,
  legislator-district-aware economic-impact framing, and state-budget-cycle-
  sensitive timing.

runtime_consumers:
  scout:
    pre_filter_question: |
      Is the applicant PA-located (principal operations in PA) AND eligible
      under PA Dept of Agriculture program portfolio (Specialty Crop Block
      Grant pass-through / AGINNOV / Farm Bill pass-through / PA-Preferred
      branding programs)?
    eligibility_dimensions:
      - pa_locality                       # principal operations in PA per F-PA-DEPT-AG-NOT-PA-LOCATED
      - pa_preferred_signal               # PA-Preferred eligibility tagging (competitive scoring, not hard gate)
      - named_district_impact_signal      # legislator-district named impact (competitive scoring)
    hard_gate_refs:
      - F-PA-DEPT-AG-NOT-PA-LOCATED
    cross_funder_signal: |
      State-agriculture funder; routes opportunity DOWN to specific PA-DEPT-
      AG program-level charters (AGINNOV, SCBG, Farm Bill pass-through) and
      LATERALLY to USDA-AMS / USDA-RD when applicant has both PA-state-track-
      record and federal-track-record. Flags out-of-PA applicants as wrong-
      funder-match.
    operator_assist_required: |
      Escalate to operator when: (a) PA-Preferred eligibility claimed but
      not verifiable (F-PA-DEPT-AG-PA-PREFERRED-INELIGIBLE-CLAIM HIGH fires),
      (b) state-budget-reconciliation timing collides with planned submission
      window (operator must confirm appropriation status), (c) legislator-
      district sensitivity around applicant identity (operator judgment on
      named-district framing).
    source_authority: |
      [CONJECTURE — Pillar-2 corpus pending] PA Dept of Agriculture program
      portfolio page + PA Right-to-Know Law operational implications.
      PA-locality dimension source-backed. PA-Preferred branding program
      details need Pillar-2 corpus ingest.
    prose_summary: |
      DISCOVER restricts radar to PA-located operations; tags PA-Preferred-
      eligible applicants for register-alignment scoring.
  scribe:
    voice_change: |
      State-program-officer register: PA-Commonwealth-localized; named
      county + Senate-district + House-district economic-impact framing;
      PA-Preferred branding conditional (verify eligibility BEFORE
      claiming); PA-source data backing (PA-Census, PA Center for
      Workforce Information) over national-only data; state-budget-cycle
      awareness.
    section_ordering:
      - "§I PA-Preferred + statutory authority (when applicable)"
      - "§II PA economic impact — named county + Senate district + House district + FTE + wage"
      - "§III project methodology"
      - "§IV budget + state match (named PA-source funds when state-match required)"
      - "§V applicant qualifications + PA-network"
      - "§VI work plan"
    must_do:
      - "Name PA county + PA Senate district + PA House district in §II economic-impact framing."
      - "Verify PA-Preferred eligibility BEFORE claiming PA-Preferred branding in §I."
      - "Cite PA-Census + PA Center for Workforce Information data for baseline economic indicators."
      - "Document cash match with named PA source when state-match required."
      - "Use 'Commonwealth of Pennsylvania' or 'Pennsylvania' (not generic 'PA' alone in formal narrative)."
    must_not_do:
      - "Lead with 'innovative' or 'cutting-edge' framing — state officers reward economic-impact over novelty."
      - "Claim PA-Preferred branding without product-origin verification."
      - "Use 'rural region' or 'rural area' without named PA county."
      - "Cite national-only data without PA-Census / state-source data backing."
    cross_funder_signal: |
      PA-DEPT-AG register is STATE-PROGRAM-OFFICER with PA-Preferred /
      named-district overlay. Distinct from federal (USDA-AMS / USDA-RD /
      USDA-NIFA), distinct from PA sister state-agency PA-DCED
      (economic-development-metrics register with private-investment-
      leverage overlay). Same PA applicant pitching PA-DEPT-AG +
      PA-DCED code-switches per agency. Program-instance charter
      PA-DEPT-AG-AGINNOV-FY26 inherits this register.
    source_authority: |
      Canonical reference §PA Department of Agriculture Funder Profile
      + Heinz/RK-Mellon PA-Preferred messaging norms (cross-foundation
      anchor for PA state-aligned language). PA-Preferred standards
      operator-attested per current PA Dept of Ag publications; pinpoint
      ingest pending Pillar-2.
    prose_summary: |
      Applies state-program-officer register + PA-Preferred framing + legislator-
      district impact framing across PA-Dept-Ag drafts.
  judge: |
    Cross-checks PA-economic-impact + PA-Preferred + state-budget-fit;
    rewards named-county / district-level impact framing.
  red_team: |
    Probes PA-Preferred integrity, legislator-district sensitivity, state-
    budget-reconciliation-timing risks, Right-to-Know responsiveness.
  logician: |
    PRE-gates F-PA-DEPT-AG-NOT-PA-LOCATED (P0),
    F-PA-DEPT-AG-PA-PREFERRED-INELIGIBLE-CLAIM (HIGH).

mission_framing:
  one_paragraph_summary: |
    Pennsylvania Department of Agriculture funds PA-located agriculture
    businesses, processors, and infrastructure projects across multiple
    state-level programs (Ag Innovation, Specialty Crop Block Grant pass-
    through, Conservation Excellence, Dairy Investment, Hardwoods Development,
    Plant Health). State-program-officer register dominates with political-
    awareness layer absent from federal programs.
  corpus_ref: "<NEEDED — Pillar 2: PA Dept of Ag strategic framework FY24-26>"
stage_behavior:
  screen:
    primary_question: "PA-located applicant + PA-Preferred eligibility (when claimed) + program-specific eligibility cascade."
    time_budget: <NEEDED Pillar 2>
    pass_fail_triggers:
      - "Applicant operations not in PA → FAIL"
      - "PA-Preferred branding claimed but product origin fails standards → FAIL or DOWNGRADE"
      - "Specialty-crop track applicant not producing list-eligible crop → FAIL"
      - "Dairy track applicant not dairy-producer-or-processor → FAIL"
    common_rejections:
      - "PA-Preferred claim on product with non-PA primary inputs."
      - "Specialty-crop product not on PA-DEPT-AG specialty-crop list."
      - "Match commitments not specifying PA-source funds when state-matching-required."

  score:
    primary_question: "PA economic impact + PA-Preferred alignment + state-program-officer dialect + match leverage."
    evidence_rewarded:
      - "Named PA county / Senate-district / House-district impact framing"
      - "PA-Preferred branding strategy explicit (when product-class eligible)"
      - "PA-Census + PA-state-economic-development data baseline citations"
      - "Cash match including PA-source funds where state-match required"
    scoring_blind_spots:
      - "Legislator-district economic-impact framing can be over- or under-played; balance per district economic posture."
      - "PA-Preferred branding alignment is soft (not formally weighted) but tracked."
    common_penalties:
      - "Generic 'rural Pennsylvania' framing without named county/district → -2 to -3 points."
      - "PA-Preferred claim without underlying product-origin eligibility → -3 to -5 points + reviewer skepticism on other claims."

  consensus:
    primary_question: "PA economic impact + PA-Preferred + match + state-budget-fit vs panel peers."
    tie_breakers:
      - "Adjacent economic-impact scores: higher band requires named district + FTE methodology."
      - "Adjacent PA-Preferred scores: higher band requires PA-Preferred branding strategy with marketing materials."
    portfolio_considerations: |
      PA-Dept-Ag balances funded portfolio across PA-rural-county distribution +
      commodity-type + producer-vs-processor + Republican-vs-Democrat legislator
      districts (politically-aware but not formalized). Out-of-region applicants
      not present; PA-eligible default.

evidence_ladder:
  strongest:
    - "Named PA county + Senate-district + House-district economic-impact framing"
    - "PA-Census + PA Center for Workforce Information data baseline citations"
    - "PA-Preferred branding plan with marketing materials"
    - "Cash match from named PA-source (county economic-dev fund, PA-state-coordinated foundation, etc.)"
    - "PA-Dept-Ag prior-funded-applicant track record"
  acceptable:
    - "Named PA county without district-level specifics"
    - "PA-source data without district-level breakdown"
    - "PA-Preferred conceptual alignment (eligibility verified but no branding plan yet)"
    - "Generic PA cash match"
  weak:
    - "'Rural Pennsylvania' framing without county"
    - "National data + PA extrapolation"
    - "PA-Preferred claim without product-origin verification"
  unacceptable:
    - "Out-of-state applicant with PA-impact handwave"
    - "PA-Preferred claim where product origin clearly fails standards"

language_register:
  preferred_terms:
    - PA_Preferred
    - Pennsylvania
    - PA_Farm_Bill
    - rural_PA
    - PA_specialty_crop
    - state_match
    - Pennsylvania_agriculture
    - Commonwealth_of_Pennsylvania
  suspicious_terms:
    - innovative                                             # state-officers neutral on innovation framing
    - cutting_edge
    - we_will_serve_the_region                              # too vague for state-program-officer
    - significant_PA_impact                                 # without FTE / dollar sizing
  sentence_shapes_that_work:
    - "This project creates [N] FTE jobs in [named PA county] (PA Senate District [X], PA House District [Y]) at $[Z] average wage, with PA-source match of $[W] from [named PA funder/program]."
    - "Product is PA-Preferred eligible (PA-grown / PA-produced / PA-processed per category [C]) per PA-Preferred standards."
  sentence_shapes_that_fail:
    - '"We will serve rural Pennsylvania..." (no district / county specifics)'
    - '"This innovative PA-Preferred opportunity..." (suspicious terms; PA-Preferred without eligibility)'
drafting_implications:
  scribe_must_do:
    - "Name PA county + PA Senate district + PA House district in §II economic-impact framing."
    - "Verify PA-Preferred eligibility BEFORE claiming PA-Preferred branding in §I."
    - "Cite PA-Census + PA Center for Workforce Information data for baseline economic indicators."
    - "Document cash match with named PA source when state-match required."
    - "Use 'Commonwealth of Pennsylvania' or 'Pennsylvania' (not generic 'PA' alone in formal narrative)."
  scribe_must_not_do:
    - "Lead with 'innovative' or 'cutting-edge' framing — state officers reward economic-impact over novelty."
    - "Claim PA-Preferred branding without product-origin verification."
    - "Use 'rural region' or 'rural area' without named PA county."
    - "Cite national-only data without PA-Census / state-source data backing."
  section_ordering_notes: |
    §I PA-Preferred + statutory authority → §II PA economic impact (named
    county + district) → §III project methodology → §IV budget + state match
    → §V applicant qualifications + PA-network → §VI work plan.

judge_implications:
  scoring_dimensions_to_weight_harder:
    - "PA Economic Impact / Named-District Specificity — weight ≥25%"
    - "PA-Preferred Branding Alignment (when eligible) — weight ≥10%"
    - "State Match / Leveraging — weight ≥15%"
  evidence_required_before_high_score:
    - "Economic Impact ≥4: named county + Senate + House districts + FTE + wage"
    - "PA-Preferred ≥4: eligibility verified + branding plan with marketing materials"
    - "Match ≥4: ≥50% cash including named PA-source funds"

red_team_probe_seeds:
  - probe: "Are PA county + Senate-district + House-district names specific in §II, or is it generic 'rural Pennsylvania'?"
    why_it_matters: "Generic framing → -2 to -3 points; named-district framing signals state-program-officer fluency."
  - probe: "If PA-Preferred branding is claimed, is product origin verified per PA-Preferred standards (PA-grown / PA-produced / PA-processed per category)?"
    why_it_matters: "Unverified PA-Preferred claim is a known reviewer downgrade + trust signal damage."
  - probe: "Is cash match from named PA source (county fund, foundation, etc.) when state-match required?"
    why_it_matters: "Non-PA-source match doesn't satisfy state-match requirements on some PA-Dept-Ag programs."
  - probe: "Does the project timeline align with PA state-budget-cycle (Jul 1 fiscal year + budget-reconciliation typical Jun)?"
    why_it_matters: "Timeline that requires fund-disbursement during PA-budget-reconciliation period faces operational risk."

logician_gate_candidates:
  - gate: F-PA-DEPT-AG-NOT-PA-LOCATED
    gate_type: hard_eligibility_gate
    failure_condition: "kfr.applicant.primary_operations_state != 'PA'"
    severity: P0
    fail_action: REJECT_NO_DRAFT
    source_required: true
    corpus_ref: pending_pillar_2  # PA Dept of Ag PA-only eligibility per FID_CANONICAL_REFERENCE
    confidence:
      level: medium
      reason: "PA-only eligibility is canonical-reference-doc anchored (FID_CANONICAL_REFERENCE §PA Dept of Ag default eligibility)"
      promotion_requirement: "PA Dept of Ag programmatic guidance pinpoint ingested at Pillar-2"
  - gate: F-PA-DEPT-AG-PA-PREFERRED-INELIGIBLE-CLAIM
    gate_type: competitive_scoring_signal
    failure_condition: "kfr.applicant.claims_pa_preferred_branding == True AND not kfr.product.satisfies_pa_preferred_standards()"
    severity: HIGH
    fail_action: WARN_OPERATOR
    source_required: true
    corpus_ref: pending_pillar_2  # PA-Preferred branding standards
    confidence:
      level: low
      reason: "pre_corpus_hypothesis — PA-Preferred standards exist as PA Dept of Ag publication; verbatim text pending"
      promotion_requirement: "PA-Preferred standards document per category ingested at Pillar-2"
  - gate: F-PA-DEPT-AG-NAMED-DISTRICT-MISSING
    gate_type: competitive_scoring_signal
    failure_condition: "draft.has_section('PA economic impact') AND not draft.names_pa_county_and_districts()"
    severity: MED
    fail_action: WARN_OPERATOR
    source_required: false
    corpus_ref: pending_pillar_2  # operator-pattern, state-program-officer-fluency heuristic
    confidence:
      level: low
      reason: "pre_corpus_hypothesis — named-district framing is operator-derived state-program-officer heuristic"
      promotion_requirement: "PA Dept of Ag reviewer-training materials or scoring rubric pattern ingested at Pillar-2"
    pass_1_reconciliation_note: "Purpose-wise this gate is drafting heuristic (Scribe register guidance), closer to drafting_warning than competitive_scoring_signal. Fail_action stays WARN_OPERATOR per Pass 0; migrating to WARN_SCRIBE is a Pass 3 reconciliation candidate."

source_backing:
  corpus_refs:
    - "<NEEDED — Pillar 2: PA Dept of Ag strategic framework FY24-26>"
    - "<NEEDED — Pillar 2: PA Farm Bill enabling legislation refs>"
    - "<NEEDED — Pillar 2: PA-Preferred standards documentation>"
    - "<NEEDED — Pillar 2: FY24 + FY25 PA Dept of Ag aggregate awards + Right-to-Know synthesis>"
  confidence: LOW pre-corpus.
  unresolved_questions:
    - "PA-Preferred standards per category (production vs processing vs labeling)"
    - "Cross-program rubric publication discipline at PA Dept of Ag"
    - "State-budget-cycle interaction with grant timelines"
```

---

## §1 — What "depth" means for THIS artifact

PA-Dept-Ag funder-level depth is the **state-program-officer register substrate** — PA-located eligibility, PA-Preferred branding discipline, named-district economic-impact framing, state-budget-cycle awareness. Distinct from federal-program-officer register on political-awareness + named-district specificity.

**Codex same-prompt-with/without test:**
- **Without** — Scribe writes generic "rural Pennsylvania" with PA-Preferred handwave. Judge applies federal-style scoring.
- **With** — Scribe names PA county + Senate + House districts; verifies PA-Preferred eligibility before claiming; cites PA-Census data. Judge weights PA Economic Impact ≥25% + PA-Preferred ≥10% + State Match ≥15%. Red Team probes PA-Preferred integrity + district specificity. Logician fails closed on non-PA applicants + unverified PA-Preferred.

Force-multiplier: every PA-Dept-Ag program (Ag Innovation / Specialty Crop / Conservation Excellence / Dairy / Hardwoods) inherits register + cascades.

---

## §2 — Primary sources in scope

| Corpus category | Specific sources | Access path | Estimated count |
|-----------------|------------------|-------------|-----------------|
| `strategic/` | PA Dept of Ag strategic framework; PA Farm Bill refs | Public PA site | 2-3 |
| `regulatory/` | PA-Preferred standards; PA-state-match rules | Public PA Dept of Ag | 2-3 |
| `awards/` | FY24 + FY25 PA aggregate awards; Right-to-Know FOIA | Public PA + Right-to-Know | 2-3 |
| `interviews/` | 0-1 PA Dept of Ag program-officer (Tier-2/3) | Operator network | 0-1 |
| `legislative_context/` | PA Farm Bill text; PA Specialty Crop state plan | PA General Assembly | 1-2 |

Case law OUT OF SCOPE.

---

## §3 — Tier classification

| Field | Tier |
|-------|:----:|
| Default | `1` |
| `funder_officer_relationship_notes` | `3` |
| `legislator_district_sensitivity_notes` | `3` |
| `dialect_notes_operator_derived` | `2` |

---

## §4 — Refresh cadence

`annual` + `event_triggered` overlay (PA Secretary change; PA Farm Bill reauthorization).

---

## §5 — Calibration applicant pair

`food_systems` (CIC-01) × `operating_capacity` (CLC-03), with Public Purpose & Works (CLC-01) overlay.

---

## §6 — Done definition

`audited` per same discipline as USDA-RD funder depth charter.

---

## §7 — Operator signature

```yaml
charter_signed_at: <pending_operator_attestation>
charter_signed_by_pubkey: <pending_operator_attestation>
charter_signed_canonical_bytes_sha3_512: <pending_operator_attestation>
charter_ed25519_signature: <pending_operator_attestation>
```

Manual ceremony per `pillar_1_charters/README.md`.

---

## §8 — Out of scope (anti-drift)

- Per-program FY26 RFP + rubric (lives in `programs/PA-DEPT-AG-<program>-FY26.yaml`)
- Other PA-state agencies (PA-DCED, PA-DEP, PCCD, PHMC)
- Compliance framework internals
- Reviewer-type heuristics
- Per-applicant PA-Preferred branding alignment specifics (lives in `orgs/<slug>/`)
- Case law interpretation
