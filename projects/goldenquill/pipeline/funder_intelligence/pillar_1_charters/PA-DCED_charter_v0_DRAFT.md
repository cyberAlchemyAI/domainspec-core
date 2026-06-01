# Depth Charter — `PA-DCED` (funder behavior profile)

> **Pillar 1 of 4** per `pipeline/planning/funder_intelligence_database_research_project_2026-05-16.md` §3.1.
> **Quality bar** per `docs/FID_ARTIFACT_OPTIMIZATION_PRINCIPLES_2026-05-18.md` §1 + §2 + Codex framing.
> **Status: DEPTH CHARTER v0 (pre-corpus hypothesis; do not load as signed logic)** — re-authored to Codex yaml shape per operator directive 2026-05-18.
>
> **[CONJECTURE — Pillar-2 corpus pending]** All PA-DCED-specific funder-fact claims operator-asserted; Pillar-2 corpus assembly (DCED strategic + PIDA enabling legislation + Keystone Communities + economic-impact methodology + aggregate awards) promotes each. `F-FID-FACT-ORPHAN` enforces.

---

## Header

| Field | Value |
|------:|:------|
| `artifact_id` | `PA-DCED` |
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
    decision_changed: "Scout DISCOVER tags radar hits with PA economic-development + private-investment-leverage requirement; downgrades hits where applicant context lacks jobs-created or private-investment-leverage signal for PA-DCED-eligible projects."
  scribe:
    reads_fields: [funder_dialect, language_register, drafting_implications]
    stage: scaffold
    decision_changed: "Scribe applies economic-impact-metrics-first register: jobs-created/retained FTE in §I (canonical PA-DCED scoring vector), private-investment-leverage ratio in §II, named PA county / Senate / House districts in §III. Distinct from PA-Dept-Ag's PA-Preferred + agriculture register and federal RD's rural-prosperity register."
  judge:
    reads_fields: [judge_implications]
    stage: cross_check
    decision_changed: "Judge cross-checks economic-impact + private-investment-leverage + downtown-revitalization-fit dimensions; rewards FTE-quantified job metrics + named private-investor commitments. PA-DCED reviewers downgrade speculative-jobs framing without methodology."
  red_team:
    reads_fields: [red_team_probe_seeds]
    stage: probe_target_selection
    decision_changed: "Red Team probes PA-DCED-specific failure modes: jobs-created-vs-retained conflation, private-investment-leverage authenticity (committed vs aspirational), downtown-revitalization-fit when Keystone Communities track, environmental review for ground-disturbing site work, state-match-source PA-locality requirements."
  logician:
    reads_fields: [eligibility_gates, logician_gate_candidates]
    stage: PRE
    decision_changed: "Logician fires PA-DCED funder-wide PRE-gates: F-PA-DCED-NOT-PA-LOCATED (P0), F-PA-DCED-JOBS-METHODOLOGY-MISSING (HIGH; jobs claim without FTE + counting-period + verification path), F-PA-DCED-PRIVATE-INVESTMENT-LEVERAGE-MISSING (HIGH; many DCED programs require named-private-investor leverage)."
```

```yaml
artifact_must_not_contain:
  - facts belonging to another artifact          # PIDA / Keystone Communities program-level → programs/
  - applicant-specific claims
  - uncited generalizations
  - compliance framework internals
  - reviewer-type heuristics
  - other PA-state agencies
  - case law interpretation
```

```yaml
strength_test:
  - "Name one concrete drafting decision this artifact changes."
  - "Name one proposal this artifact would reject or downgrade."
  - "Name one Red Team probe this artifact enables."
```

**Answers (PASSED):**

1. **Drafting decision.** Scribe leads §I with **FTE-quantified jobs-created + jobs-retained metric** (e.g., "[N] FTE jobs created over 3 years + [M] FTE jobs retained, with private-investment leverage of $[X] from [named PA private investor]"). Without artifact: generic "this project will create jobs" framing. With artifact: FTE methodology + private-investment-leverage commitment explicit on page 1.
2. **Proposal rejected.** Logician `F-PA-DCED-JOBS-METHODOLOGY-MISSING` (HIGH) fires when jobs claim lacks FTE conversion + counting period + verification path. Operator warned before Scribe drafts further.
3. **Red Team probe.** `PA-DCED-PROBE-PRIVATE-INVESTMENT-LEVERAGE-AUTHENTICITY` asks: *"Are private-investment-leverage commitments documented with named investor + dollar amount + commitment letter, or aspirational ('we expect to attract private investment')?"* PA-DCED reviewers specifically downgrade aspirational leverage claims.

---

## §B — Codex-shape depth-charter YAML

```yaml
artifact_id: PA-DCED
artifact_family: funder
version: depth_charter_v0
lifecycle: draft
validation_status: pre_corpus_hypothesis
runtime_load_status: do_not_load_as_signed_logic
operator_label: depth_charter_v0

one_sentence_job: |
  Equip every PA-DCED program draft (Keystone Communities / PIDA / Industrial
  Sites Reuse / Manufacturing PA / Business in Our Sites) with FTE-quantified
  economic-impact register, named private-investment-leverage discipline,
  and PA-locality state-match rules.

runtime_consumers:
  scout:
    pre_filter_question: |
      Is the project (a) located/principally-operating in Pennsylvania and
      (b) economic-development-eligible (FTE jobs, capital investment,
      blight remediation, or downtown revitalization) under DCED program
      portfolio?
    eligibility_dimensions:
      - pa_locality                      # project located in PA / principal operations in PA
      - economic_development_category    # FTE-jobs / capital-investment / blight / downtown-revitalization
      - private_investment_leverage      # private-match-funds posture where program requires
    hard_gate_refs:
      - F-PA-DCED-NOT-PA-LOCATED
    cross_funder_signal: |
      State-economic-development funder; routes opportunity TOWARD other PA
      state economic-development programs (PA-DEPT-AG when ag-adjacent; PA-
      Industrial Development Authority; Ben Franklin Technology Partners)
      and AWAY from federal-research-only paths. Flags applicants with no
      jobs-or-investment narrative.
    operator_assist_required: |
      Escalate to operator when: (a) jobs methodology is missing (F-PA-DCED-
      JOBS-METHODOLOGY-MISSING HIGH fires) — operator must confirm
      jobs-created-vs-retained methodology, (b) private-investment leverage
      is required by the program-instance but absent from KFR (F-PA-DCED-
      PRIVATE-INVESTMENT-LEVERAGE-MISSING HIGH where required).
    source_authority: |
      [CONJECTURE — Pillar-2 corpus pending] PA DCED programs page; PA Act
      90 funding categories. PA-locality + jobs-methodology dimensions need
      Pillar-2 ingest of specific program NOFAs (the funder-level charter is
      multi-program; program-instance charters will source-pin).
    prose_summary: |
      DISCOVER restricts to PA-located + economic-development-eligible projects.
  scribe:
    voice_change: |
      Economic-development-metrics register: FTE-quantified jobs-created +
      jobs-retained (separate methodologies + counting periods) lead §I;
      private-investment-leverage commitments (named investor + dollar
      amount + signed commitment letter) lead §II for programs requiring
      leverage (PIDA / Industrial Sites Reuse); downtown-revitalization
      fit for Keystone Communities track.
    section_ordering:
      - "§I FTE jobs-created + jobs-retained headline (separate counts + methodology)"
      - "§II detailed economic-impact + private-investment-leverage (named investor + dollar amount + commitment letter) + PA-locality framing"
      - "§III project methodology"
      - "§IV budget + match"
      - "§V qualifications"
      - "§VI work plan"
    must_do:
      - "Lead §I with FTE-quantified jobs-created + jobs-retained metric on page 1."
      - "Name private investor + dollar amount + commitment letter in §II for programs requiring leverage."
      - "Distinguish jobs-created vs jobs-retained explicitly with separate methodologies."
      - "Cite PA-Census + PA Center for Workforce Information for baseline."
      - "Name PA county + Senate + House districts for economic-impact framing."
    must_not_do:
      - "Aggregate jobs-created + jobs-retained into single count."
      - "Frame private-investment as aspirational ('we will attract') without committed investor."
      - "Use 'innovative' / 'cutting-edge' without operational specifics."
      - "Cite national-only data without PA-source backing."
    cross_funder_signal: |
      PA-DCED register is ECONOMIC-DEVELOPMENT-METRICS — distinct from
      PA sister state-agency PA-DEPT-AG (state-program-officer + PA-
      Preferred overlay) and from federal economic-development funders
      (EDA, SBA, HUD CDBG). Food-systems applicants reach PA-DCED when
      project frames as economic development (food hubs, value-added
      processing infrastructure, regional supply-chain coordination);
      otherwise route to PA-DEPT-AG / USDA-AMS.
    source_authority: |
      Canonical reference §PA Department of Community & Economic
      Development. Specific weighting heuristics ("Economic Impact ≥30%")
      operator-derived; pinpoint Pillar-2 PIDA / Keystone Communities /
      Industrial Sites Reuse NOFA ingest pending.
    prose_summary: |
      Applies FTE-jobs-first §I register + private-investment-leverage in §II.
  judge: |
    Weights Economic Impact + Private Investment Leverage + Downtown
    Revitalization Fit heavier; downgrades speculative jobs framing.
  red_team: |
    Probes jobs-created-vs-retained conflation, private-investment
    authenticity, downtown-revitalization fit, environmental review.
  logician: |
    PRE-gates F-PA-DCED-NOT-PA-LOCATED (P0), F-PA-DCED-JOBS-METHODOLOGY-MISSING
    (HIGH), F-PA-DCED-PRIVATE-INVESTMENT-LEVERAGE-MISSING (HIGH where required).

mission_framing:
  one_paragraph_summary: |
    Pennsylvania Department of Community & Economic Development funds business
    attraction / retention / expansion, downtown revitalization, manufacturing
    infrastructure, and industrial-site reuse across multiple PA programs.
    Economic-impact-metrics register dominates with private-investment-leverage
    as canonical scoring vector. Food-systems applicants reach DCED when
    project frames as economic development (food hubs, value-added processing
    infrastructure, regional supply-chain coordination).
  corpus_ref: "<NEEDED — Pillar 2: DCED strategic framework FY24-26>"
stage_behavior:
  screen:
    primary_question: "PA-located + economic-development-eligible + jobs methodology + private investment (when required) + program-specific eligibility."
    time_budget: <NEEDED Pillar 2>
    pass_fail_triggers:
      - "Applicant operations not in PA → FAIL"
      - "Jobs claim without FTE methodology → FAIL (or DOWNGRADE depending on program)"
      - "Required private-investment-leverage missing → FAIL (for PIDA, Industrial Sites Reuse)"
      - "Site-work proposal without environmental review → FAIL"
    common_rejections:
      - "Headcount jobs without FTE conversion → administrative return."
      - "Speculative private-investment-leverage without commitment letters."
      - "Industrial-site reuse without environmental due diligence."

  score:
    primary_question: "Economic impact + private-investment leverage + downtown-revitalization fit + PA-locality state-match."
    evidence_rewarded:
      - "FTE jobs created + retained with explicit counting period + verification path"
      - "Named private investor + dollar amount + commitment letter"
      - "Downtown revitalization fit (Keystone Communities track): named main-street + revitalization metrics"
      - "PA-locality state-match (county economic-dev fund, regional foundation)"
    scoring_blind_spots:
      - "Reviewers may over-weight quantity (FTE count) vs quality (wage level + benefits); balance both."
      - "Downtown revitalization metrics can be qualitative (foot traffic, business density) or quantitative; cite both."
    common_penalties:
      - "Headcount jobs without FTE → -3 to -5 points."
      - "Speculative private-investment-leverage → -5 to -7 points + reviewer trust damage."
      - "Generic 'regional impact' without named PA county / district → -2 points."

  consensus:
    primary_question: "Economic impact + private-investment + downtown fit vs panel peers."
    tie_breakers:
      - "Adjacent economic-impact scores: higher band requires FTE + wage + benefits."
      - "Adjacent private-investment-leverage scores: higher band requires named-investor commitment letter."
    portfolio_considerations: |
      DCED balances funded portfolio across PA economic-development regions +
      urban-vs-rural distribution + manufacturing-vs-service mix.

evidence_ladder:
  strongest:
    - "Named private investor + dollar amount + signed commitment letter (or LOI minimum)"
    - "PA-Census + PA Center for Workforce Information jobs/wages baseline"
    - "Cash match from named PA county economic-dev fund / regional foundation"
    - "Prior PA-DCED grant track record"
    - "Downtown revitalization data (foot traffic studies + business-density indicators) for Keystone Communities"
  acceptable:
    - "Private-investment letter of intent without signed commitment"
    - "PA-state-economic-development data without district-level breakdown"
    - "Generic PA cash match"
  weak:
    - "Speculative jobs without FTE methodology"
    - "Aspirational private-investment-leverage without commitments"
    - "Generic 'we will attract investment' framing"
  unacceptable:
    - "Out-of-state private investment without PA-job-creation pathway"
    - "Jobs claims without methodology or counting period"

language_register:
  preferred_terms:
    - economic_impact
    - jobs_created
    - jobs_retained
    - FTE
    - private_investment_leverage
    - downtown_revitalization
    - Keystone_Communities
    - industrial_sites_reuse
    - PIDA                                                   # Pennsylvania Industrial Development Authority
    - main_street
  suspicious_terms:
    - innovative
    - cutting_edge
    - we_will_attract                                       # without committed investor
    - significant_economic_growth                            # without sized FTE / dollar
  sentence_shapes_that_work:
    - "This project creates [N] FTE jobs over [T] years at $[W] average wage with [B] benefits, retaining [M] FTE positions threatened by [documented threat]."
    - "Private-investment leverage of $[X] from [named investor] is committed (Exhibit [E]: signed commitment letter)."
  sentence_shapes_that_fail:
    - '"We will create significant economic growth..." (suspicious; no sizing)'
    - '"Innovative business attraction approach..." (suspicious terms)'
drafting_implications:
  scribe_must_do:
    - "Lead §I with FTE-quantified jobs-created + jobs-retained metric on page 1."
    - "Name private investor + dollar amount + commitment letter in §II for programs requiring leverage."
    - "Distinguish jobs-created vs jobs-retained explicitly with separate methodologies."
    - "Cite PA-Census + PA Center for Workforce Information for baseline."
    - "Name PA county + Senate + House districts for economic-impact framing."
  scribe_must_not_do:
    - "Aggregate jobs-created + jobs-retained into single count."
    - "Frame private-investment as aspirational ('we will attract') without committed investor."
    - "Use 'innovative' / 'cutting-edge' without operational specifics."
    - "Cite national-only data without PA-source backing."
  section_ordering_notes: |
    §I FTE jobs + private-investment headline → §II detailed economic-impact
    + PA-locality framing → §III project methodology → §IV budget + match
    → §V qualifications → §VI work plan.

judge_implications:
  scoring_dimensions_to_weight_harder:
    - "Economic Impact / FTE Jobs Methodology — weight ≥30%"
    - "Private Investment Leverage — weight ≥20% (for PIDA / Industrial Sites)"
    - "Downtown Revitalization Fit (Keystone Communities) — weight ≥15%"
  evidence_required_before_high_score:
    - "Economic Impact ≥4: FTE + counting period + wage + benefits + verification path"
    - "Private Leverage ≥4: named investor + dollar + signed commitment"
    - "Downtown Fit ≥4: named main-street + foot-traffic + business-density data"

red_team_probe_seeds:
  - probe: "Are jobs distinguished into created vs retained with separate FTE methodology + counting period + verification path for each?"
    why_it_matters: "Conflated jobs framing is the most-common DCED scoring downgrade vector."
  - probe: "Is private-investment-leverage committed (named investor + dollar + letter) or aspirational?"
    why_it_matters: "Aspirational leverage → -5 to -7 points + reviewer trust damage on other claims."
  - probe: "For Keystone Communities, is downtown-revitalization fit documented (named main-street + foot-traffic + business-density)?"
    why_it_matters: "Generic 'downtown' framing without metrics doesn't pass Keystone Communities scoring."
  - probe: "For site work, is environmental due diligence documented (Phase I ESA minimum)?"
    why_it_matters: "Industrial Sites Reuse + Business in Our Sites trigger environmental discipline."

logician_gate_candidates:
  - gate: F-PA-DCED-NOT-PA-LOCATED
    gate_type: hard_eligibility_gate
    failure_condition: "kfr.applicant.primary_operations_state != 'PA'"
    severity: P0
    fail_action: REJECT_NO_DRAFT
    source_required: true
    corpus_ref: pending_pillar_2  # DCED enabling legislation / PIDA / Keystone Communities Act
    confidence:
      level: medium
      reason: "PA-only eligibility is statutory across DCED programs; pinpoint enabling-legislation citation pending"
      promotion_requirement: "PIDA + Keystone Communities Act statutory citations ingested at Pillar-2"
  - gate: F-PA-DCED-JOBS-METHODOLOGY-MISSING
    gate_type: competitive_scoring_signal
    failure_condition: "draft.claims_jobs() AND not draft.has_fte_methodology_with_counting_period_and_verification()"
    severity: HIGH
    fail_action: WARN_OPERATOR
    source_required: true
    corpus_ref: pending_pillar_2  # DCED jobs-methodology + private-investment-leverage standards
    confidence:
      level: low
      reason: "pre_corpus_hypothesis — DCED jobs-FTE methodology expectation is well-known reviewer behavior; standards document pending"
      promotion_requirement: "DCED jobs-methodology standards document ingested at Pillar-2"
  - gate: F-PA-DCED-PRIVATE-INVESTMENT-LEVERAGE-MISSING
    gate_type: competitive_scoring_signal
    failure_condition: "program.requires_private_investment_leverage AND not kfr.applicant.has_committed_private_investor()"
    severity: HIGH
    fail_action: WARN_OPERATOR
    source_required: true
    corpus_ref: pending_pillar_2  # per-program leverage requirement (PIDA / Keystone Communities)
    confidence:
      level: low
      reason: "pre_corpus_hypothesis — per-program leverage requirement varies; pinpoint per-program text pending"
      promotion_requirement: "Per-program NOFA leverage-requirement text ingested at Pillar-2"
  - gate: F-PA-DCED-JOBS-CONFLATION
    gate_type: competitive_scoring_signal
    failure_condition: "draft.jobs_created + draft.jobs_retained both claimed AND not draft.distinguishes_with_separate_methodology()"
    severity: MED
    fail_action: WARN_OPERATOR
    source_required: false
    corpus_ref: pending_pillar_2  # DCED reviewer-behavior pattern
    confidence:
      level: low
      reason: "pre_corpus_hypothesis — jobs-conflation downgrade pattern is operator-derived reviewer-behavior heuristic"
      promotion_requirement: "DCED reviewer-training materials or scoring-rubric pattern ingested at Pillar-2"

source_backing:
  corpus_refs:
    - "<NEEDED — Pillar 2: DCED Strategic Framework FY24-26>"
    - "<NEEDED — Pillar 2: PIDA enabling legislation>"
    - "<NEEDED — Pillar 2: Keystone Communities Act + program guidance>"
    - "<NEEDED — Pillar 2: DCED jobs-methodology + private-investment-leverage standards>"
    - "<NEEDED — Pillar 2: FY24 + FY25 DCED aggregate awards>"
  confidence: LOW pre-corpus.
  unresolved_questions:
    - "Exact FTE methodology DCED requires (3-year counting period standard?)"
    - "Private-investment-leverage ratio per program"
    - "Keystone Communities downtown-revitalization metrics catalog"
```

---

## §1 — What "depth" means for THIS artifact

PA-DCED funder-level depth is the **economic-impact-metrics-first register substrate** — FTE-quantified jobs as canonical scoring vector, named private-investment-leverage discipline, downtown-revitalization fit for Keystone Communities. Distinct from PA-Dept-Ag's PA-Preferred + agriculture register.

**Codex same-prompt-with/without test:**
- **Without** — Scribe writes "this project will create jobs and attract investment." Generic economic-development framing.
- **With** — Scribe writes "[N] FTE jobs created + [M] FTE retained at $[W]/year average wage + private leverage of $[X] from [named investor with signed commitment]." Judge weights Economic Impact ≥30% + Private Leverage ≥20% + Downtown Fit ≥15%. Red Team probes jobs-conflation + leverage authenticity + environmental due diligence. Logician fails closed on missing FTE methodology + missing private-investment commitments.

Force-multiplier: every PA-DCED program inherits FTE-first register + leverage discipline.

---

## §2 — Primary sources in scope

| Corpus category | Specific sources | Access path | Estimated count |
|-----------------|------------------|-------------|-----------------|
| `strategic/` | DCED strategic framework; PIDA framing; Keystone Communities | Public DCED site | 2-3 |
| `regulatory/` | DCED economic-impact metric guidance; private-investment-leverage standards | DCED public guidance | 2-3 |
| `awards/` | FY24 + FY25 DCED aggregate awards; food-systems-adjacent awards | Public DCED + state budget | 2-3 |
| `legislative_context/` | PIDA enabling legislation; Keystone Communities Act | PA General Assembly | 1-2 |

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

`annual` + `event_triggered` (DCED Secretary change; PIDA reauthorization).

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

- Per-program FY26 RFP + rubric (lives in `programs/PA-DCED-<program>-FY26.yaml`)
- Other PA-state agencies (PA-DEPT-AG, PA-DEP, PCCD, PHMC)
- Compliance framework internals
- Reviewer-type heuristics
- Per-applicant economic-impact-metric calculations (lives in `orgs/<slug>/`)
- Case law interpretation
