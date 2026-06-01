# Depth Charter — `USDA-AMS-VAPG-FY26` (Value-Added Producer Grant)

> **Pillar 1 of 4** per `pipeline/planning/funder_intelligence_database_research_project_2026-05-16.md` §3.1.
> **Quality bar** per `docs/FID_ARTIFACT_OPTIMIZATION_PRINCIPLES_2026-05-18.md` §1 + §2 + Codex framing.
> **Status: DEPTH CHARTER v0 (pre-corpus hypothesis; do not load as signed logic)** — re-authored to Codex yaml shape per operator directive 2026-05-18. Inherits USDA-AMS funder depth-charter. **VAPG-FY26 cycle CLOSED** per operator 2026-05-18 — artifact stays in roster for completeness because recent-cycle intelligence informs FY27 pre-planning; sibling `USDA-AMS-VAPG-FY27` charter authored when FY27 NOFO drops.
>
> **[CONJECTURE — Pillar-2 corpus pending]** Cross-references existing extracted rubric at `pipeline/rubrics/vapg_fy26.json` (MEDIUM confidence anchor — verbatim NOFO citations still required at Pillar 2). `F-FID-FACT-ORPHAN` enforces remaining facts at L-005.

---

## Header

| Field | Value |
|------:|:------|
| `artifact_id` | `USDA-AMS-VAPG-FY26` |
| `artifact_family` | `program` |
| `funder_pointer` | `USDA-AMS` |
| `version` | `depth_charter_v0` |
| `lifecycle` | `draft` |
| `cycle_status` | **CLOSED** (deferred to FY27 pursuit per operator 2026-05-18) |
| `pillar_2_dispatch_position` | **5 of 6** (deprioritized — cycle closed) |

---

## §A — Adversarial pre-checks

```yaml
runtime_consumer:
  scout:
    reads_fields: [scout_verify.live_check_url, eligibility_gates, nofo.cycle_status]
    stage: both
    decision_changed: "Scout DISCOVER pre-filters applicants in USDA-AMS producer-eligibility chain. VERIFY checks cycle_status=CLOSED for FY26 and surfaces FY27 NOFO when it drops. Operator-radar tags FY27 NOFO as priority pursuit-window."
  scribe:
    reads_fields: [scribe_section_requirements, scoring_rubric, drafting_implications]
    stage: both
    decision_changed: "Scribe leads §I with USDA-AMS canonical value-added definition cited verbatim; structures producer-revenue causal chain in §II (commodity baseline → transformation → premium → revenue delta); attaches buyer commitment letters in §III (signed PO ideal, LOI minimum); leads §IV match-narrative with CASH-first (cross-USDA discipline)."
  judge:
    reads_fields: [scoring_rubric, judge_scoring_map]
    stage: rubric_scoring
    decision_changed: "Judge applies VAPG FY26 7-criterion 100-pt rubric per cross-reference to `pipeline/rubrics/vapg_fy26.json`. Tie-breakers favor cash-match-≥50% + signed-PO buyer commitments + producer-revenue causal chain explicit."
  red_team:
    reads_fields: [red_team_probes]
    stage: probe_target_selection
    decision_changed: "Red Team probes VAPG-specific failure modes: independent-producer-vs-aggregator misclassification; value-added definition rigor (state-change OR differentiation OR producer-ownership-through-marketing); Planning vs Working Capital track-mismatch; buyer-commitment authenticity (LOI vs signed PO); matching-funds with state-source rules."
  logician:
    reads_fields: [eligibility_gates, disqualifiers, logician_gates]
    stage: PRE
    decision_changed: "Logician fires F-VAPG-NOT-INDEPENDENT-PRODUCER (P0; inherits USDA-AMS funder-level gate), F-VAPG-VALUE-ADDED-DEFINITION-MISMATCH (HIGH; inherits), F-VAPG-PLANNING-VS-WORKING-CAPITAL-TRACK-MISMATCH (HIGH; applicant target track doesn't match project shape), F-VAPG-CYCLE-CLOSED (META; warn operator that pursuit is FY27)."
```

```yaml
artifact_must_not_contain:
  - facts belonging to another artifact          # USDA-AMS funder facts → funders/USDA-AMS.yaml
  - applicant-specific claims
  - uncited generalizations
  - compliance framework internals
  - reviewer-type heuristics
  - case law interpretation
  - other USDA-AMS programs                       # FSMIP / Specialty Crop / FMLFPP = separate
  - VAPG cycles prior to FY26 except as historical reference
```

```yaml
strength_test:
  - "Name one concrete drafting decision this artifact changes."
  - "Name one proposal this artifact would reject or downgrade."
  - "Name one Red Team probe this artifact enables."
```

**Answers (PASSED):**

1. **Drafting decision.** Scribe writes the **producer-revenue causal chain** explicitly in §II per inherited USDA-AMS register, AND selects **Planning vs Working Capital track** based on project shape: Planning ($75K typical cap) for feasibility / business-plan / marketing-plan work; Working Capital ($250K typical cap) for inventory / market-development / processing-operations work. Without artifact: generic value-added pitch + wrong track selection. With artifact: causal chain + correct track.
2. **Proposal rejected.** Logician `F-VAPG-PLANNING-VS-WORKING-CAPITAL-TRACK-MISMATCH` (HIGH) fires when applicant target track (Planning vs Working Capital) doesn't match project shape (feasibility/plan work targets Planning; inventory/market-development targets Working Capital). Mismatched-track applications routinely return at administrative review.
3. **Red Team probe.** `VAPG-PROBE-TRACK-FIT` asks: *"Does the project description align with Planning track (feasibility / business plan / marketing plan / market study) OR Working Capital track (inventory / market development / processing operations)? Track-mismatch is a known administrative-rejection vector + reviewer-skepticism trigger on other claims."*

---

## §B — Codex-shape depth-charter YAML

```yaml
artifact_id: USDA-AMS-VAPG-FY26
artifact_family: program
version: depth_charter_v0
lifecycle: draft
validation_status: pre_corpus_hypothesis
runtime_load_status: do_not_load_as_signed_logic
operator_label: depth_charter_v0
cycle_status: closed_fy26_defer_to_fy27

one_sentence_job: |
  Equip Scribe/Judge/Red Team/Logician with VAPG FY26-specific eligibility +
  7-criterion 100-pt rubric (cross-ref pipeline/rubrics/vapg_fy26.json) +
  Planning-vs-Working-Capital track discipline + buyer-commitment authenticity
  + cycle-CLOSED-defer-to-FY27 awareness.

runtime_consumers:
  scout:
    pre_filter_question: |
      Is the applicant (a) an independent producer (or majority-producer-
      controlled entity) per VAPG independent-producer test, (b) proposing
      a value-added product satisfying USDA-AMS canonical value-added
      definition, and (c) selecting a coherent Planning-vs-Working-Capital
      track? Cycle-aware: FY26 closed → defer to FY27 NOFO drop.
    eligibility_dimensions:
      - independent_producer_authenticity # majority-producer-controlled entity per VAPG independent-producer test
      - value_added_definition_compliance # change-in-state / differentiation / producer-ownership-through-marketing
      - track_selection_coherence         # Planning vs Working Capital track fits applicant maturity
      - cycle_status                      # FY26 closed → flag; FY27 NOFO drop monitored
      - sam_uei_baseline                  # SAM-active + UEI present (inherits USDA-RD funder-wide)
    hard_gate_refs:
      - F-VAPG-NOT-INDEPENDENT-PRODUCER
    cross_funder_signal: |
      Federal-program program-instance funder under USDA-AMS funder-level.
      Routes opportunity LATERALLY to USDA-AMS funder-level program portfolio
      (FSMIP, Specialty Crop Block Grant pass-through, FMLFPP) when producer-
      eligibility passes but VAPG track doesn't fit. Aggregator/distributor
      applicants flagged as wrong-funder-match unless majority-producer-
      controlled per VAPG independent-producer test.
    operator_assist_required: |
      Escalate to operator when: (a) Planning-vs-Working-Capital track
      selection unclear (F-VAPG-PLANNING-VS-WORKING-CAPITAL-TRACK-MISMATCH
      HIGH fires), (b) FY26 cycle is closed (F-VAPG-CYCLE-CLOSED META
      warning fires) — operator confirms pivot to FY27 monitoring, (c)
      value-added test borderline (e.g., minimal differentiation, weak
      change-in-state).
    source_authority: |
      USDA-AMS VAPG FY26 Notice of Funding Opportunity + 7 CFR 4284-J
      (canonical reference §USDA-AMS VAPG canonical value-added definition).
      Rubric source: `pipeline/rubrics/vapg_fy26.json` (extracted).
    prose_summary: |
      DISCOVER pre-filters producer-eligibility chain; VERIFY surfaces FY27 NOFO
      drop as priority pursuit window.
  scribe:
    voice_change: |
      Inherits USDA-AMS register (market-access + producer-revenue
      causal chain). VAPG-specific overlays: USDA-AMS canonical value-
      added definition cited verbatim in §I; Planning Grant vs Working
      Capital Grant track selected explicitly based on project shape;
      buyer commitments (signed PO ideal, LOI minimum) attached as
      Exhibits and referenced by ID in §III.
    section_ordering:
      - "§I USDA-AMS canonical value-added definition verbatim + Planning vs Working Capital track selection"
      - "§II producer-revenue causal chain (commodity baseline → transformation → premium → revenue delta dollars)"
      - "§III buyer commitments — signed PO ideal, LOI minimum, Exhibit-referenced"
      - "§IV budget + matching (cash before in-kind, contingent flagged)"
      - "§V producer qualifications + producer-control documentation (majority-controlled by producers)"
      - "§VI work plan"
    must_do:
      - "Inherit USDA-AMS scribe.must_do (producer-revenue chain in §II; value-added definition verbatim in §I; buyer commitments Exhibit-referenced; cash-before-in-kind match)."
      - "Select Planning OR Working Capital track explicitly based on project shape; do not aggregate."
      - "If FY26 cycle is closed (per F-VAPG-CYCLE-CLOSED META warning), Scribe declines to draft and surfaces operator-defer-to-FY27."
    must_not_do:
      - "Inherit USDA-AMS scribe.must_not_do (no innovation-only framing; no vendor-marketing data; no aggregator/distributor as applicant; no missing producer-revenue baseline)."
      - "Conflate Planning + Working Capital tracks within one proposal."
      - "Claim 'value-added' without mapping to the AMS canonical test (state-change OR differentiation OR producer-ownership-through-marketing)."
    cross_funder_signal: |
      Program-instance under USDA-AMS. Inherits AMS funder-level register
      with VAPG-specific track-selection + value-added-definition overlay.
      When applicant is a cooperative, composes NCBA-CLUSA cooperative-
      authenticity overlay (one-member-one-vote + patronage). When
      applicant has rural-area focus, sister-routes to USDA-RD RBDG /
      RCDG.
    source_authority: |
      USDA-AMS VAPG FY26 NOFO + 7 CFR 4288 + canonical reference §USDA-AMS
      VAPG. Rubric source-backed at pipeline/rubrics/vapg_fy26.json
      (100 pts, 7 criteria — extracted). Inherits USDA-AMS funder-level
      scribe register source-authority.
    prose_summary: |
      Reads scribe_section_requirements; leads §I with USDA-AMS canonical
      value-added definition verbatim; §II producer-revenue causal chain;
      §III buyer commitments; selects Planning vs Working Capital track.

language_register_inheritance:
  parent_charter: USDA-AMS
  inherits:
    - language_register.preferred_terms
    - language_register.suspicious_terms
    - language_register.sentence_shapes_that_work
    - language_register.sentence_shapes_that_fail
    - drafting_implications.scribe_must_do
    - drafting_implications.scribe_must_not_do
  vapg_specific_overlays:
    preferred_terms:
      - value_added_definition_verbatim
      - planning_grant
      - working_capital_grant
      - producer_revenue_increase
      - buyer_commitment
    suspicious_terms:
      - aggregate_planning_and_working_capital   # VAPG-specific track-conflation flag
  note: |
    No standalone language_register / drafting_implications blocks. VAPG
    inherits from USDA-AMS funder-level. When applicant is a cooperative,
    NCBA-CLUSA overlay composes on top.
  judge: |
    Applies VAPG FY26 7-criterion 100-pt rubric per
    pipeline/rubrics/vapg_fy26.json cross-reference.
  red_team: |
    Probes track fit, value-added definition rigor, buyer-commitment
    authenticity, independent-producer integrity.
  logician: |
    PRE-gates inherited from USDA-AMS funder; program-specific
    F-VAPG-PLANNING-VS-WORKING-CAPITAL-TRACK-MISMATCH (HIGH),
    F-VAPG-CYCLE-CLOSED (META warning operator that FY26 is closed).

funder_pointer: USDA-AMS
program_summary_one_paragraph: |
  USDA-AMS Value-Added Producer Grant funds independent producers / ag
  producer groups / farmer-rancher cooperatives / majority-controlled
  producer-based businesses to develop or market value-added agricultural
  products. Two tracks: Planning Grant (~$75K cap) for feasibility +
  business-plan + marketing-plan work; Working Capital Grant (~$250K cap)
  for inventory + market-development + processing-operations work.
  Rubric extracted at pipeline/rubrics/vapg_fy26.json (100 pts, 7 criteria).
  FY26 cycle CLOSED per operator 2026-05-18; deferred to FY27.

nofo:
  source_url: <NEEDED Pillar 2 — most-recent FY26 NOFO snapshot for historical reference>
  cycle_status: closed
  next_cycle_expected: FY27 (per AMS annual-cycle pattern; verify dates)

eligibility_gates:
  - gate_id: F-VAPG-NOT-INDEPENDENT-PRODUCER
    gate_type: hard_eligibility_gate
    predicate: "Applicant entity in canonical producer set (inherits USDA-AMS funder gate)"
    machine_check:
      field_in_applicant_context: kfr.applicant.entity_type
      operator: in
      threshold: [independent_producer, ag_producer_group, farmer_rancher_coop, majority_controlled_producer_based_business]
    on_fail: REJECT_NO_DRAFT
    severity: P0
    source_required: true
    corpus_ref: pending_pillar_2  # 7 CFR 4288 VAPG + AMS canonical producer definitions (inherits USDA-AMS funder gate)
    confidence:
      level: medium
      reason: "Inherits USDA-AMS funder gate F-USDA-AMS-NOT-INDEPENDENT-PRODUCER; canonical-reference-doc anchored (§USDA-AMS Default Applicant Types + §VAPG)"
      promotion_requirement: "7 CFR 4288 (VAPG) + AMS canonical producer definitions ingested at Pillar-2"
    pass_1_reconciliation_note: "Inherits USDA-AMS funder F-USDA-AMS-NOT-INDEPENDENT-PRODUCER. Pass 6 (inheritance) considers whether this program-level gate is redundant or expresses VAPG-specific narrowing."
  - gate_id: F-VAPG-VALUE-ADDED-DEFINITION-MISMATCH
    gate_type: competitive_scoring_signal
    predicate: "Product satisfies USDA-AMS canonical value-added test (state-change OR differentiation OR producer-ownership-through-marketing)"
    machine_check:
      operator: matches                                            # composite-shape check; decompose at future pass
      threshold: { satisfies_ams_canonical_test: true }
    on_fail: WARN_OPERATOR
    severity: HIGH
    source_required: true
    corpus_ref: pending_pillar_2  # AMS canonical value-added definition verbatim
    confidence:
      level: medium
      reason: "Value-added test is canonical-reference-doc anchored; inherits USDA-AMS funder gate; verbatim definition pending"
      promotion_requirement: "AMS canonical value-added definition verbatim ingested at Pillar-2"
    pass_1_reconciliation_note: "Purpose-wise eligibility verification (verify_required_gate semantics); (HIGH, WARN_OPERATOR) tuple classifies as competitive_scoring_signal per Discipline 3a.4. Flag for operator review whether fail_action should change."
  - gate_id: F-VAPG-PLANNING-VS-WORKING-CAPITAL-TRACK-MISMATCH
    gate_type: competitive_scoring_signal
    predicate: "Project shape aligns with claimed track (Planning OR Working Capital)"
    machine_check:
      operator: matches
      threshold: { project_shape_matches_track: true }
    on_fail: WARN_OPERATOR
    severity: HIGH
    source_required: true
    corpus_ref: pending_pillar_2  # AMS Planning vs Working Capital track guidance
    confidence:
      level: low
      reason: "pre_corpus_hypothesis — Planning vs Working Capital distinction is canonical-reference-doc referenced (§USDA-AMS VAPG) but program-shape-fit-test heuristic pending source"
      promotion_requirement: "AMS Planning vs Working Capital track guidance + project-shape-fit rubric ingested at Pillar-2"

scoring_rubric:
  total_points: 100
  cross_reference: pipeline/rubrics/vapg_fy26.json
  criteria_count: 7
  note: "Detailed weights + criteria already extracted at pipeline/rubrics/vapg_fy26.json; Pillar-2 corpus assembly verifies extraction against FY26 NOFO source."

scribe_section_requirements:
  - nofo_section_id: §I
    drafting_decisions:
      - decision: "Cite USDA-AMS canonical value-added definition verbatim in opening paragraph."
        rubric_ref: vapg_rubric_criterion_1_value_added
      - decision: "Select Planning OR Working Capital track explicitly based on project shape."
        rubric_ref: vapg_track_eligibility
  - nofo_section_id: §II
    drafting_decisions:
      - decision: "Write producer-revenue causal chain explicitly: commodity baseline → transformation → premium → revenue delta with dollar figures."
        rubric_ref: vapg_rubric_criterion_producer_revenue_increase
  - nofo_section_id: §III
    drafting_decisions:
      - decision: "Attach buyer commitment letters (signed PO ideal, LOI minimum) as Exhibits; reference by Exhibit ID in narrative with volume + price + delivery schedule."
        rubric_ref: vapg_rubric_criterion_market_feasibility

evidence_ladder:
  strongest:
    - "Signed PO from named buyer with volume + price + delivery schedule"
    - "USDA-AMS Census + USDA-NASS data establishing commodity baseline + value-added premium"
    - "Cash match commitment letter with unconditional language"
    - "Prior VAPG track record (FY24 / FY25 awards)"
  acceptable:
    - "LOI from named buyer with volume + price"
    - "Peer-reviewed agricultural-economics market data"
    - "In-kind match with third-party-confirmed valuation"
  weak:
    - "Generic 'identified buyers' without named entity"
    - "Trade-press market data"
    - "Qualitative match"
  unacceptable:
    - "Aggregator/distributor applicant misclassified as producer"
    - "Speculative market without commitments"
    - "Track-mismatch (Planning shape claiming Working Capital cap)"

red_team_probes:
  - probe_id: VAPG-PROBE-TRACK-FIT
    probe_question: "Does project shape align with claimed track (Planning OR Working Capital)?"
    score_impact_if_fails: "HIGH admin-rejection + reviewer skepticism"
  - probe_id: VAPG-PROBE-VALUE-ADDED-RIGOR
    probe_question: "Does product satisfy USDA-AMS canonical value-added test?"
    score_impact_if_fails: "-3 to -5 + administrative review"
  - probe_id: VAPG-PROBE-BUYER-COMMITMENT-QUALITY
    probe_question: "Buyer commitments signed PO (ideal), LOI (min), or generic (downgrade)?"
    score_impact_if_fails: "-5 to -10 on market-feasibility"
  - probe_id: VAPG-PROBE-PRODUCER-INTEGRITY
    probe_question: "Is applicant majority-controlled BY producers (not aggregator)?"
    score_impact_if_fails: ADMINISTRATIVE_REJECTION

source_backing:
  corpus_refs:
    - "Internal: pipeline/rubrics/vapg_fy26.json (extracted FY26 rubric — MEDIUM-confidence anchor)"
    - "<NEEDED — Pillar 2: FY26 NOFO + Grants.gov synopsis (verify extracted rubric)>"
    - "<NEEDED — Pillar 2: AMS canonical value-added definition verbatim>"
    - "<NEEDED — Pillar 2: FY24 + FY25 VAPG award rosters + PA-specific>"
    - "<NEEDED — Pillar 2: AMS Planning vs Working Capital track guidance>"
  confidence: MEDIUM (rubric already extracted anchors part of this).
  unresolved_questions:
    - "Whether FY27 NOFO will use same 7-criterion 100-pt rubric or revise"
    - "Recent FY24-FY25 administrative-rejection pattern at AMS"
    - "Track-selection guidance documentation from AMS"
```

---

## §1 — What "depth" means for THIS artifact

VAPG FY26 program-level depth is the **value-added decision substrate** — producer-eligibility chain (inherits USDA-AMS), value-added canonical test, Planning vs Working Capital track distinction, buyer-commitment authenticity, producer-revenue causal chain. Inherits USDA-AMS funder depth-charter register. Cycle CLOSED for FY26; pursuit deferred to FY27.

**Codex same-prompt-with/without test:**
- **Without** — Scribe writes generic value-added pitch with wrong track + speculative market. Aggregator misclassification risk.
- **With** — Scribe cites USDA-AMS canonical value-added definition verbatim; writes producer-revenue causal chain; selects Planning vs Working Capital track per project shape; attaches buyer commitments. Judge applies 7-criterion 100-pt rubric per `pipeline/rubrics/vapg_fy26.json`. Red Team probes track fit + value-added rigor + buyer-commitment quality + producer integrity. Logician fails closed on non-producer + value-added mismatch + track mismatch.

---

## §2 — Primary sources in scope

| Corpus | Sources | Path | Count |
|--------|---------|------|-------|
| `nofos/` | VAPG FY26 NOFO snapshot (historical) | Grants.gov + AMS | 1-2 |
| `rubrics/` | Cross-ref `pipeline/rubrics/vapg_fy26.json` (extracted) | Internal | 1 |
| `awards/` | FY24 + FY25 VAPG rosters; PA-specific | USAspending.gov + AMS | 2-3 |
| `guidance/` | AMS value-added definition verbatim; Planning vs Working Capital | AMS public guidance | 2-3 |

Case law OUT OF SCOPE.

---

## §3 — Tier classification

| Field | Tier |
|-------|:----:|
| Default | `1` |
| `rubric.weighted_dimensions[]` | `1` |
| `eligibility_rules[]` | `1` |
| `reviewer_relationship_notes[]` | `3` |
| `applicant_debrief_distillations[]` | `2` |

---

## §4 — Refresh cadence

`per_cycle`. FY27 NOFO drop triggers sibling `USDA-AMS-VAPG-FY27` charter authoring; FY26 artifact preserved for historical reference + recent-cycle intelligence informing FY27 pre-planning.

---

## §5 — Calibration applicant pair

`food_systems` (CIC-01) × `operating_capacity` (CLC-03), with Market Access (CLC-05) as primary CLC.

---

## §6 — Done definition

`audited` per SARE-NE / USDA-RD discipline. **Cycle CLOSED** marker prevents `field_tested` graduation until FY27 cycle re-opens.

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

- Other USDA-AMS programs (FSMIP, Specialty Crop, FMLFPP)
- VAPG cycles prior to FY26 except as historical-pattern reference
- Compliance framework internals
- Reviewer-type heuristics
- Per-applicant value-added product specifics (→ `orgs/<slug>/`)
- Case law interpretation
- FY27 cycle specifics (sibling artifact when FY27 NOFO drops)
