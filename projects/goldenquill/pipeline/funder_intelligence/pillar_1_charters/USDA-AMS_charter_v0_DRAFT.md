# Depth Charter — `USDA-AMS` (funder behavior profile)

> **Pillar 1 of 4** per `pipeline/planning/funder_intelligence_database_research_project_2026-05-16.md` §3.1.
> **Quality bar** per `docs/FID_ARTIFACT_OPTIMIZATION_PRINCIPLES_2026-05-18.md` §1 + §2 + Codex framing.
> **Status: DEPTH CHARTER v0 (pre-corpus hypothesis; do not load as signed logic)** — re-authored to Codex yaml shape per operator directive 2026-05-18.
>
> **[CONJECTURE — Pillar-2 corpus pending]** All USDA-AMS-specific funder-fact claims are operator-asserted; Pillar-2 corpus assembly (AMS strategic framework + VAPG canonical guidance + Specialty Crop Block Grant pass-through + agency-aggregate awards) promotes each claim. `F-FID-FACT-ORPHAN` enforces.

---

## Header

| Field | Value |
|------:|:------|
| `artifact_id` | `USDA-AMS` |
| `artifact_family` | `funder` |
| `version` | `depth_charter_v0` |
| `lifecycle` | `draft` |
| `phase` | `1 — exemplar pair` |

---

## §A — Adversarial pre-checks

```yaml
runtime_consumer:
  scout:
    reads_fields: [program_roster, producer_eligibility_chains]
    stage: DISCOVER
    decision_changed: "Scout DISCOVER filters AMS-radar to applicants matching the producer-eligibility chain (independent producer / ag producer group / farmer-rancher coop / majority-controlled producer-based business). Non-producer applicants downgrade to OUT_OF_SCOPE for VAPG-class programs."
  scribe:
    reads_fields: [funder_dialect, language_register, drafting_implications]
    stage: scaffold
    decision_changed: "Scribe applies market-access register: value-added product framing in §I, revenue-from-agricultural-commodities causal chain in §II, market-development metrics (units, market reach, price-premium captured) in §III. Distinct from USDA-RD's rural-prosperity register and USDA-NIFA's methodology-first register."
  judge:
    reads_fields: [judge_implications]
    stage: cross_check
    decision_changed: "Judge cross-checks market-feasibility + producer-revenue-increase + matching-funds dimensions weighted heavier than scientific-merit. AMS reviewers reward producer-revenue causal chains; downgrade speculative market projections without buyer commitments."
  red_team:
    reads_fields: [red_team_probe_seeds]
    stage: probe_target_selection
    decision_changed: "Red Team probes AMS-specific failure modes: producer-eligibility-chain integrity (not aggregator misclassified); 'value-added' definition rigor (USDA-AMS canonical test cited verbatim); buyer commitment authenticity (LOI vs MOU vs signed PO); matching-funds documentation."
  logician:
    reads_fields: [eligibility_gates, logician_gate_candidates]
    stage: PRE
    decision_changed: "Logician fires USDA-AMS funder-wide PRE-gates: F-USDA-AMS-NOT-INDEPENDENT-PRODUCER (P0; applicant entity-type not in producer set), F-USDA-AMS-VALUE-ADDED-DEFINITION-MISMATCH (HIGH; proposed product fails canonical value-added test)."
```

```yaml
artifact_must_not_contain:
  - facts belonging to another artifact          # VAPG-FY26 rubric → programs/USDA-AMS-VAPG-FY26.yaml
  - applicant-specific claims
  - uncited generalizations
  - compliance framework internals
  - reviewer-type heuristics
  - other USDA agencies
  - case law interpretation
```

```yaml
strength_test:
  - "Name one concrete drafting decision this artifact changes."
  - "Name one proposal this artifact would reject or downgrade."
  - "Name one Red Team probe this artifact enables."
```

**Answers (PASSED):**

1. **Drafting decision.** Scribe writes the **producer-revenue causal chain** explicitly in §II of any USDA-AMS program draft: *"applicant produces commodity X → transformation Y captures premium $Z/unit → producer revenue increases by $W."* Without artifact: generic "this project benefits producers" framing. With artifact: explicit dollar-mechanism that AMS reviewers score against.
2. **Proposal rejected.** Logician `F-USDA-AMS-NOT-INDEPENDENT-PRODUCER` (P0) fails closed any USDA-AMS application where applicant entity-type is not in canonical producer set. Scribe never invoked for aggregator/distributor applicants who misclassify as producers.
3. **Red Team probe.** `USDA-AMS-PROBE-VALUE-ADDED-DEFINITION-RIGOR` asks: *"Does the proposed product satisfy the USDA-AMS canonical value-added test (change in physical state OR differentiation creating marketing identity OR aggregation that captures producer ownership through marketing chain)?"*

---

## §B — Codex-shape depth-charter YAML

```yaml
artifact_id: USDA-AMS
artifact_family: funder
version: depth_charter_v0
lifecycle: draft
validation_status: pre_corpus_hypothesis
runtime_load_status: do_not_load_as_signed_logic
operator_label: depth_charter_v0

one_sentence_job: |
  Equip every USDA-AMS program draft (VAPG / FSMIP / Specialty Crop Block /
  FMLFPP) with producer-eligibility predicates, value-added-definition
  enforcement, market-access drafting register, and buyer-commitment
  authenticity probes.

runtime_consumers:
  scout:
    pre_filter_question: |
      Is the applicant a producer (independent producer or majority-producer-
      controlled entity) AND proposing value-added agricultural product
      development / market access / producer-marketing infrastructure under
      USDA-AMS portfolio (VAPG / FSMIP / SCBG pass-through / FMLFPP)?
    eligibility_dimensions:
      - producer_entity_authenticity      # independent-producer OR majority-producer-controlled (not aggregator misclassified)
      - value_added_definition_compliance # change-in-state / differentiation / producer-ownership-through-marketing
      - market_access_focus               # project advances market access / buyer commitments / producer-marketing infrastructure
      - sam_uei_baseline                  # SAM-active + UEI present (inherits federal-baseline)
    hard_gate_refs:
      - F-USDA-AMS-NOT-INDEPENDENT-PRODUCER
    cross_funder_signal: |
      Federal-program funder-level under USDA. Routes opportunity DOWN to
      USDA-AMS program-instances (VAPG, FSMIP, SCBG, FMLFPP) and LATERALLY
      to USDA-RD when project has rural-development overlap, USDA-NIFA when
      research overlap. Non-producer applicants (e.g., aggregator-only,
      research-only) routed AWAY from USDA-AMS toward USDA-NIFA or USDA-RD.
    operator_assist_required: |
      Escalate to operator when: (a) value-added definition borderline
      (F-USDA-AMS-VALUE-ADDED-DEFINITION-MISMATCH HIGH fires), (b) matching-
      funds documentation incomplete (F-USDA-AMS-MATCH-DOCUMENTATION-MISSING
      HIGH fires), (c) aggregator/distributor entity claims producer status
      — operator must verify majority-producer-control.
    source_authority: |
      USDA-AMS canonical value-added definition (canonical reference
      §USDA-AMS Producer-Eligibility + Value-Added Definition); 7 CFR 4284-J
      (VAPG); per-program-instance NOFAs ingested via §J child charters.
    prose_summary: |
      DISCOVER filters non-producer applicants out of AMS-radar.
  scribe:
    voice_change: |
      Market-access register: producer-revenue causal chain explicit;
      USDA-AMS canonical value-added definition cited verbatim in §I;
      buyer commitments (signed PO ideal, LOI minimum) attached as
      Exhibits and referenced by ID in narrative; 'producer' (not
      'farmer alone'); matching funds with cash before in-kind.
    section_ordering:
      - "§I summary + USDA-AMS canonical value-added framing (definition verbatim)"
      - "§II producer-revenue causal chain (commodity baseline → transformation → premium → revenue delta with dollar figures)"
      - "§III market-access + buyer commitments (signed PO or LOI; Exhibit-referenced)"
      - "§IV budget + matching (cash first, in-kind second, contingent commitments flagged)"
      - "§V qualifications + producer track record"
      - "§VI work plan"
    must_do:
      - "Write producer-revenue causal chain explicitly in §II."
      - "Cite USDA-AMS canonical value-added definition verbatim in §I."
      - "Attach buyer commitment letters; reference by Exhibit ID in narrative."
      - "Lead matching-funds with cash before in-kind; flag contingent commitments explicitly."
      - "Use 'producer' not 'farmer' in narrative."
    must_not_do:
      - "Frame project around 'innovation' without specific operational difference."
      - "Cite vendor-marketing market-size claims; use USDA-AMS Census / USDA-NASS instead."
      - "Submit proposal where applicant is aggregator/distributor (not majority-controlled by producers)."
      - "Omit producer-revenue baseline."
    cross_funder_signal: |
      USDA-AMS register is MARKET-ACCESS / PRODUCER-REVENUE — distinct
      from USDA-NIFA's peer-review-academic register and USDA-RD's
      rural-prosperity / leveraging register. Same producer applying to
      VAPG (AMS) + RBDG (RD) + AFRI (NIFA) code-switches per agency.
      LFPP/FMPP/SCBGP program-instances inherit this register but layer
      program-specific evidence requirements (e.g., LFPP intermediated-
      market hub focus vs FMPP direct-to-consumer focus).
    source_authority: |
      Canonical reference §USDA-AMS Funder Profile + §USDA-AMS Evaluation
      Themes (market viability / producer benefit / project sustainability
      / customer & supply diversity / partnership-leverage). VAPG rubric
      source-backed at pipeline/rubrics/vapg_fy26.json (100 pts, 7 criteria).
      Cross-program weighting heuristics operator-derived; pinpoint Pillar-2
      LAMP / FMPP / LFPP / SCBGP corroboration pending.
    prose_summary: |
      Applies market-access register + producer-revenue causal chain in §II.
  judge: |
    Cross-checks market-feasibility + producer-revenue dimensions weighted
    heavier than scientific-merit; rewards buyer-commitment authenticity.
  red_team: |
    Probes producer-eligibility integrity, value-added-definition rigor,
    buyer-commitment authenticity, matching-funds.
  logician: |
    PRE-gates F-USDA-AMS-NOT-INDEPENDENT-PRODUCER (P0),
    F-USDA-AMS-VALUE-ADDED-DEFINITION-MISMATCH (HIGH),
    F-USDA-AMS-MATCH-DOCUMENTATION-MISSING (HIGH).

mission_framing:
  one_paragraph_summary: |
    USDA Agricultural Marketing Service funds value-added agricultural product
    development + market access + producer-marketing infrastructure. Houses
    VAPG (flagship; rubric extracted at pipeline/rubrics/vapg_fy26.json), FSMIP,
    Specialty Crop Block Grant (state pass-through), FMLFPP. Market-access
    register dominates; producer-revenue causal chains are load-bearing.
  corpus_ref: "<NEEDED — Pillar 2: AMS strategic framework FY22-26>"
stage_behavior:
  screen:
    primary_question: "Producer-eligibility + value-added-definition + matching-funds documentation."
    time_budget: <NEEDED Pillar 2>
    pass_fail_triggers:
      - "Applicant entity-type not in producer set → FAIL"
      - "Proposed product fails value-added test → FAIL"
      - "Match commitments below required ratio → FAIL"
      - "SAM.gov inactive at submission → FAIL"
    common_rejections:
      - "Aggregator/distributor misclassified as producer (must be majority-controlled BY producers)."
      - "Value-added claim failing change-in-state OR differentiation OR producer-ownership-through-marketing test."

  score:
    primary_question: "Producer-revenue causal chain + market feasibility + matching-funds leverage."
    evidence_rewarded:
      - "Buyer commitment letters (LOI min; signed PO ideal) with dollar volumes + price"
      - "Producer-revenue baseline (current commodity price) + projected value-added price (sourced market data)"
      - "Market-access channel diversification (≥2 channels)"
      - "Matching-funds with unconditional commitment letters"
    scoring_blind_spots:
      - "Reviewers may over-weight market-research polish over substance; verify market data cites USDA-AMS Census / USDA-NASS."
    common_penalties:
      - "Speculative market projections without buyer commitments → -5 to -10 points."
      - "Value-added definition not explicitly mapped to AMS canonical test → -3 to -5 points."
      - "Contingent match commitments → -5 points on leveraging."

  consensus:
    primary_question: "Producer-revenue chain + buyer-commitment authenticity + market diversification vs panel peers."
    tie_breakers:
      - "Adjacent market-feasibility scores: higher band requires signed-PO (not LOI-only)."
      - "Adjacent leveraging scores: higher band requires ≥50% cash match all-unconditional."
    portfolio_considerations: "Panels balance funded portfolio across commodity types + producer-type + geography."

evidence_ladder:
  strongest:
    - "Signed purchase order from named buyer with dollar volume + price + delivery schedule"
    - "Multi-year buyer relationship documented"
    - "USDA-AMS Census / USDA-NASS data establishing producer-revenue baseline"
    - "Cash match commitment letter on funder letterhead with unconditional language"
  acceptable:
    - "Letter of Intent from named buyer with dollar volume + price"
    - "Market data from peer-reviewed agricultural-economics publications"
    - "In-kind match with third-party-confirmed valuation"
  weak:
    - "Generic 'identified buyers in region' without named entity"
    - "Trade-press market data without sourcing"
    - "Match described qualitatively without dollar amounts"
  unacceptable:
    - "Speculative buyer projections without named entity / commitment letter"
    - "Vendor-marketing-derived market-size claims"
    - "Contingent match with no fallback"

language_register:
  preferred_terms:
    - value_added
    - producer                                              # not 'farmer' alone
    - market_access
    - revenue_increase
    - producer_marketing_chain
    - aggregation_for_producer_ownership
    - planning_grant                                        # VAPG track
    - working_capital                                       # VAPG track
    - matching_funds
  suspicious_terms:
    - innovative
    - cutting_edge
    - we_will_explore_market
    - significant_market_opportunity                        # without sized dollar
    - farmer                                                # use 'producer'
  sentence_shapes_that_work:
    - "Producer [name] produces [commodity X] at [N units/year]; this project transforms X into [value-added product Y]; Y captures premium of $[Z]/unit; revenue increases from $[A]/year to $[B]/year."
    - "Buyer commitment from [named buyer] documents [N units] at $[price] over [T years] (signed PO Exhibit [X])."
  sentence_shapes_that_fail:
    - '"We will market our product to farmers..." (passive; no causal chain)'
    - '"Significant market opportunity exists..." (suspicious terms; no sizing)'
drafting_implications:
  scribe_must_do:
    - "Write producer-revenue causal chain explicitly in §II."
    - "Cite USDA-AMS canonical value-added definition verbatim in §I."
    - "Attach buyer commitment letters; reference by Exhibit ID in narrative."
    - "Lead matching-funds with cash before in-kind; flag contingent commitments explicitly."
    - "Use 'producer' not 'farmer' in narrative."
  scribe_must_not_do:
    - "Frame project around 'innovation' without specific operational difference."
    - "Cite vendor-marketing market-size claims; use USDA-AMS Census / USDA-NASS instead."
    - "Submit proposal where applicant is aggregator/distributor (not majority-controlled by producers)."
    - "Omit producer-revenue baseline."
  section_ordering_notes: |
    AMS-typical: §I summary + value-added framing → §II producer-revenue chain
    → §III market-access + buyer commitments → §IV budget + matching → §V
    qualifications → §VI work plan.

judge_implications:
  scoring_dimensions_to_weight_harder:
    - "Market Feasibility / Buyer Commitments — weight ≥25%"
    - "Producer Revenue Increase / Causal Chain — weight ≥20%"
    - "Matching Funds / Leveraging — weight ≥15%"
  evidence_required_before_high_score:
    - "Market Feasibility ≥4: signed PO from named buyer with volume + price + schedule"
    - "Revenue Increase ≥4: baseline cited + transformation cost + value-added price + delta calculated"
    - "Leveraging ≥4: ≥50% cash match all-unconditional"

red_team_probe_seeds:
  - probe: "Is applicant entity-type in canonical AMS producer set?"
    why_it_matters: "Aggregator misclassification = P0 administrative rejection."
  - probe: "Does proposed product satisfy USDA-AMS canonical value-added test (state-change OR differentiation OR producer-ownership-through-marketing)?"
    why_it_matters: "Value-added definition rigor is the load-bearing eligibility test."
  - probe: "Are buyer commitments LOI (min) or signed PO (ideal)? LOIs without volume + price downgrade."
    why_it_matters: "Speculative projections without commitments score 0-2 on market-feasibility."
  - probe: "Is producer-revenue causal chain explicit (baseline → transformation → premium → delta), or asserted without chain?"
    why_it_matters: "Reviewers cannot score revenue-increase without explicit chain."
  - probe: "Are matching-funds unconditional or contingent?"
    why_it_matters: "Contingent matches zero-weight in leverage."

logician_gate_candidates:
  - gate: F-USDA-AMS-NOT-INDEPENDENT-PRODUCER
    gate_type: hard_eligibility_gate
    failure_condition: "kfr.applicant.entity_type not in {independent_producer, ag_producer_group, farmer_rancher_coop, majority_controlled_producer_based_business}"
    severity: P0
    fail_action: REJECT_NO_DRAFT
    source_required: true
    corpus_ref: pending_pillar_2  # AMS producer / coop / majority-controlled definitions (VAPG-canonical)
    confidence:
      level: medium
      reason: "AMS producer-eligibility definitions are canonical-reference-doc anchored (FID_CANONICAL_REFERENCE §USDA-AMS); pinpoint regulatory citation pending"
      promotion_requirement: "7 CFR 4288 (VAPG) + AMS canonical producer definitions ingested at Pillar-2"
  - gate: F-USDA-AMS-VALUE-ADDED-DEFINITION-MISMATCH
    gate_type: competitive_scoring_signal
    failure_condition: "not kfr.project.value_added_definition_satisfies_ams_canonical_test()"
    severity: HIGH
    fail_action: WARN_OPERATOR
    source_required: true
    corpus_ref: pending_pillar_2  # AMS canonical value-added definition (verbatim)
    confidence:
      level: low
      reason: "pre_corpus_hypothesis — AMS canonical value-added test invoked but verbatim definition pending Pillar-2"
      promotion_requirement: "AMS canonical value-added definition verbatim ingested at Pillar-2"
  - gate: F-USDA-AMS-MATCH-DOCUMENTATION-MISSING
    gate_type: competitive_scoring_signal
    failure_condition: "len(kfr.applicant.match_commitments) == 0 AND program.match_required == True"
    severity: HIGH
    fail_action: WARN_OPERATOR
    source_required: true
    corpus_ref: pending_pillar_2  # FMPP/LFPP 25% match per FID_CANONICAL_REFERENCE §USDA-AMS Cost Share
    confidence:
      level: medium
      reason: "FMPP/LFPP 25% match is canonical-reference-doc anchored; VAPG match varies by track; per-program pinpoint pending"
      promotion_requirement: "Per-program NOFO match-requirement text ingested at Pillar-2"
  - gate: F-USDA-AMS-CONTINGENT-MATCH-LEAK
    gate_type: competitive_scoring_signal
    failure_condition: "any(m.contingent_on_award is True for m in kfr.applicant.match_commitments)"
    severity: MED
    fail_action: WARN_OPERATOR
    source_required: false
    corpus_ref: pending_pillar_2  # AMS reviewer-behavior pattern; not statutory
    confidence:
      level: low
      reason: "pre_corpus_hypothesis — contingent-match penalty is well-known reviewer behavior but not statutory; pattern documentation pending"
      promotion_requirement: "AMS reviewer-training materials or NOFO scoring rubric pinpoint ingested at Pillar-2"

source_backing:
  corpus_refs:
    - "<NEEDED — Pillar 2: AMS Strategic Framework FY22-26>"
    - "<NEEDED — Pillar 2: VAPG canonical value-added definition (verbatim)>"
    - "<NEEDED — Pillar 2: AMS producer / coop / majority-controlled definitions>"
    - "<NEEDED — Pillar 2: FY24 + FY25 AMS aggregate awards>"
    - "Internal: pipeline/rubrics/vapg_fy26.json (VAPG FY26 extracted rubric)"
  confidence: MEDIUM pre-corpus (VAPG rubric already extracted anchors this).
  unresolved_questions:
    - "FSMIP / Specialty Crop / FMLFPP cross-program producer-eligibility coherence with VAPG"
    - "Recent AMS reviewer-panel composition norms"
```

---

## §1 — What "depth" means for THIS artifact

USDA-AMS funder-level depth is the **market-access register substrate** — producer-eligibility predicates, value-added-definition enforcement, producer-revenue causal-chain drafting, buyer-commitment-authenticity probes. Distinct from USDA-RD's rural-prosperity register and USDA-NIFA's methodology-first register.

**Codex same-prompt-with/without test:**
- **Without** — Scribe writes "this project benefits producers through innovative value-added approaches." No producer-revenue causal chain. No buyer commitments.
- **With** — Scribe writes explicit chain (commodity baseline → transformation → premium → revenue delta), cites AMS canonical value-added definition verbatim, attaches buyer commitments as Exhibit. Judge weights Market Feasibility ≥25% + Producer Revenue ≥20% + Leveraging ≥15%. Red Team probes producer-eligibility + value-added rigor + buyer-commitment authenticity. Logician fails closed on non-producer applicants + value-added mismatch.

Force-multiplier: every USDA-AMS program (VAPG / FSMIP / Specialty Crop / FMLFPP) inherits register + cascades + baseline gates.

---

## §2 — Primary sources in scope

| Corpus category | Specific sources | Access path | Estimated count |
|-----------------|------------------|-------------|-----------------|
| `strategic/` | AMS Strategic Framework FY22-26; VAPG canonical guidance | Public AMS site | 2-3 |
| `regulatory/` | AMS producer definitions + value-added canonical test | Public AMS + Federal Register | 2-3 |
| `awards/` | FY24 + FY25 AMS aggregate award rolls; PA-specific VAPG history | USAspending.gov + AMS | 2-3 |
| `interviews/` | 0-2 AMS program-officer conversations (Tier-2/3) | Operator network outreach | 0-2 |
| `guidance/` | Matching-funds documentation; producer-eligibility verification | AMS public guidance | 2-3 |
| `cross_ref/` | `pipeline/rubrics/vapg_fy26.json` (extracted VAPG FY26 rubric) | Internal | 1 |

Case law OUT OF SCOPE.

---

## §3 — Tier classification

| Field | Tier |
|-------|:----:|
| Default | `1` |
| `funder_officer_relationship_notes` | `3` |
| `dialect_notes_operator_derived` | `2` |
| `producer_eligibility_chains` | `1` |

---

## §4 — Refresh cadence

`annual` baseline + `event_triggered` overlay.

---

## §5 — Calibration applicant pair

`food_systems` (CIC-01) × `operating_capacity` (CLC-03), with Market Access (CLC-05) as primary CLC.

---

## §6 — Done definition

`audited` when Pillar-3 L-005 audit passes per same discipline as USDA-RD funder gold-standard.

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

- Per-program FY26 NOFO + rubric (lives in `programs/USDA-AMS-<program>-FY26.yaml`)
- Specialty Crop Block Grant state-level detail
- Compliance framework internals
- Reviewer-type heuristics
- Other USDA agencies — separate funder artifacts
- Per-applicant value-added product specifics (lives in `orgs/<slug>/`)
- Case law interpretation
