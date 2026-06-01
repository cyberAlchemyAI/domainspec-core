# Depth Charter — `RICHARD-KING-MELLON-FOUNDATION` (funder behavior profile)

> **Pillar 1 of 4** per `pipeline/planning/funder_intelligence_database_research_project_2026-05-16.md` §3.1.
> **Quality bar** per `docs/FID_ARTIFACT_OPTIMIZATION_PRINCIPLES_2026-05-18.md` §1 + §2 + Codex framing.
> **Status: DEPTH CHARTER v0 (pre-corpus hypothesis; do not load as signed logic)** — re-authored to Codex yaml shape per operator directive 2026-05-18. D1 operator override 2026-05-18 from McCune; rationale in MANIFEST.md D1 block.
>
> **[CONJECTURE — Pillar-2 corpus pending]** All RK-Mellon-specific funder-fact claims operator-asserted; Pillar-2 corpus assembly (RK Mellon strategic + 990-PF FY22-FY24 + conservation-strategy publications + program-area position papers) promotes each. `F-FID-FACT-ORPHAN` enforces.

---

## Header

| Field | Value |
|------:|:------|
| `artifact_id` | `RICHARD-KING-MELLON-FOUNDATION` |
| `artifact_family` | `funder` |
| `version` | `depth_charter_v0` |
| `lifecycle` | `draft` |
| `phase` | `1 — exemplar pair` |

---

## §A — Adversarial pre-checks

```yaml
runtime_consumer:
  scout:
    reads_fields: [program_roster, geographic_eligibility, strategic_capital_deployment_norms]
    stage: DISCOVER
    decision_changed: "Scout DISCOVER restricts radar to RK Mellon program areas (Conservation, Economic Development, Education, Family Wellness, Community Vitality) with southwestern-PA geographic emphasis; tags strategic-capital-scale opportunities (multi-year, multi-million-dollar commitments) distinctly from smaller targeted grants."
  scribe:
    reads_fields: [funder_dialect, language_register, drafting_implications]
    stage: scaffold
    decision_changed: "Scribe applies strategic-capital register: scale-and-permanence framing in §I (10-20 year horizon), conservation-outcomes-in-protected-acres / habitat metrics for conservation tracks, economic-development outcomes in jobs + private-investment leverage, senior-leadership-engaged solicitation discipline. Distinct from Heinz's thematic-portfolio register."
  judge:
    reads_fields: [judge_implications]
    stage: cross_check
    decision_changed: "Judge cross-checks scale-and-permanence + multi-year commitment readiness + senior-leadership relationship infrastructure. RK Mellon reviewers reward proposals where applicant can absorb + deploy strategic-capital scale; downgrade scope mismatches."
  red_team:
    reads_fields: [red_team_probe_seeds]
    stage: probe_target_selection
    decision_changed: "Red Team probes RK-Mellon-specific failure modes: scale mismatch (small applicant + large request; or vice versa), permanence-mechanism weakness (10-20 year sustainability without retention plan), senior-leadership engagement absence (RK Mellon strategic-capital deployment requires senior-leadership relationship), conservation-outcomes-measurement specificity (protected acres / habitat metrics vs vague 'protect natural resources')."
  logician:
    reads_fields: [eligibility_gates, logician_gate_candidates]
    stage: PRE
    decision_changed: "Logician fires RK Mellon funder-wide PRE-gates: F-RK-MELLON-501C3-MISSING (P0), F-RK-MELLON-OUT-OF-PROGRAM-AREA (HIGH; project doesn't fit Conservation / Economic Dev / Education / Family Wellness / Community Vitality), F-RK-MELLON-SCALE-MISMATCH (MED; applicant organizational capacity not aligned with strategic-capital scale)."
```

```yaml
artifact_must_not_contain:
  - facts belonging to another artifact
  - applicant-specific claims
  - uncited generalizations
  - compliance framework internals
  - reviewer-type heuristics
  - other Pittsburgh-region foundations                    # Heinz, Hillman, Pittsburgh Foundation, McCune = separate
  - case law interpretation
  - RK Mellon land-trust / real-estate transaction mechanics  # compliance + transaction territory
```

```yaml
strength_test:
  - "Name one concrete drafting decision this artifact changes."
  - "Name one proposal this artifact would reject or downgrade."
  - "Name one Red Team probe this artifact enables."
```

**Answers (PASSED):**

1. **Drafting decision.** Scribe leads §I with **scale-and-permanence framing**: *"What changes in southwestern Pennsylvania over 10-20 years if this works? [specific operational picture]. Strategic capital deployed at $[X] over [N] years."* Without artifact: 1-3 year project framing typical of smaller foundations. With artifact: long-horizon scale framing that signals RK Mellon fit.
2. **Proposal rejected.** Logician `F-RK-MELLON-OUT-OF-PROGRAM-AREA` (HIGH) fails closed any application where project doesn't fit one of the five RK Mellon program areas. Saves Scribe from drafting an out-of-scope proposal that RK Mellon won't review.
3. **Red Team probe.** `RK-MELLON-PROBE-SCALE-MATCH` asks: *"Is applicant organizational capacity (staffing, budget, governance, prior strategic-capital deployment) aligned with request scale? Mismatch in either direction (small org + large request; or large org + small request) is downgrade vector."*

---

## §B — Codex-shape depth-charter YAML

```yaml
artifact_id: RICHARD-KING-MELLON-FOUNDATION
artifact_family: funder
version: depth_charter_v0
lifecycle: draft
validation_status: pre_corpus_hypothesis
runtime_load_status: do_not_load_as_signed_logic
operator_label: depth_charter_v0

one_sentence_job: |
  Equip every RK-Mellon-targeted draft with strategic-capital scale-and-
  permanence register, program-area discipline (Conservation / Economic Dev /
  Education / Family Wellness / Community Vitality), senior-leadership-
  engagement readiness, and conservation-outcomes specificity.

runtime_consumers:
  scout:
    pre_filter_question: |
      Is the applicant (a) 501(c)(3) eligible-entity (or, per canonical
      reference §RK Mellon Six Program Areas, public-agency / mission-driven-
      for-profit for social-impact-investment branch), (b) project located /
      principally benefiting southwestern Pennsylvania, (c) within one of
      RK Mellon's program areas, and (d) at scale appropriate to RK Mellon's
      grant-size posture?
    eligibility_dimensions:
      - entity_type_eligibility           # 501(c)(3) baseline; canonical-ref widens to public-agency + SI-investment-for-profit
      - swpa_geographic_concentration     # primary service / impact in southwestern PA
      - program_area_alignment            # canonical-ref enumerates 6 program areas (Conservation / Economic Development / Economic Mobility / Health & Well-Being / Organizational Effectiveness / Social-Impact Investments)
      - scale_and_permanence              # multi-year + permanence-mechanism + senior-leadership engagement
    hard_gate_refs:
      - F-RK-MELLON-501C3-MISSING
    cross_funder_signal: |
      Large-strategic-capital foundation funder; routes opportunity LATERALLY
      to other Pittsburgh foundation cohort (Heinz, Hillman, Pittsburgh
      Foundation) for peer-funder comparison + capital-stack assembly. Flags
      small / short-term projects as scale-mismatch (F-RK-MELLON-SCALE-
      MISMATCH MED). Conservation-focused projects route to additionally
      consider Western Pennsylvania Conservancy + Allegheny Land Trust.
    operator_assist_required: |
      Escalate to operator when: (a) project sits outside RK Mellon's named
      program areas (F-RK-MELLON-OUT-OF-PROGRAM-AREA HIGH fires) — operator
      must confirm program-area roster against canonical-reference 6-area
      roster (Pass-1 P1-9 reconciliation pending), (b) permanence mechanism
      undocumented or absent, (c) senior-leadership relationship status
      unclear.
    source_authority: |
      RK Mellon Foundation public materials (canonical reference §RK Mellon
      Six Program Areas). Predicate widening reconciliation flagged at
      Pass-1 P1-9 — current charter encodes 5-program-area subset; canonical
      reference enumerates 6. Pillar-2 corpus must reconcile.
    prose_summary: |
      DISCOVER restricts to RK Mellon program areas + southwestern-PA + scale-
      appropriate opportunities.
  scribe:
    voice_change: |
      Strategic-capital register: 10-20 year scale-and-permanence framing
      leads §I; conservation outcomes quantified in protected acres +
      habitat metrics; economic-development outcomes quantified in FTE
      jobs + private-investment leverage; permanence mechanism named
      (endowment / earned revenue / cross-funder pipeline); senior-
      leadership / board engagement readiness documented.
    section_ordering:
      - "§I 10-20 year scale-and-permanence headline"
      - "§II program-area fit + specific outcomes (Conservation: acres + habitat; Economic Dev: FTE + private-investment leverage)"
      - "§III permanence mechanism + multi-year roadmap"
      - "§IV strategic-capital budget + matching"
      - "§V senior-leadership + governance readiness"
      - "§VI work plan"
    must_do:
      - "Lead §I with 10-20 year scale-and-permanence framing."
      - "For Conservation track, quantify in protected acres + habitat metrics."
      - "For Economic Dev, quantify in FTE jobs + private-investment leverage."
      - "Document permanence mechanism (endowment / earned revenue / cross-funder pipeline)."
      - "Reference senior-leadership / board engagement readiness in qualifications."
    must_not_do:
      - "Frame project as 1-year / short-horizon — RK Mellon is multi-year-strategic-capital."
      - "Use aspirational permanence language ('we hope to attract additional funders')."
      - "Conservation framing without acres + habitat metrics."
      - "Submit out-of-program-area project with handwave fit."
    cross_funder_signal: |
      RK Mellon Scribe register is STRATEGIC-CAPITAL — distinct from
      Heinz (theory-of-change + M1/M2/M3 mechanism stack). Within the
      Pittsburgh-foundation cohort: RK Mellon weights scale-and-permanence
      heavier than Heinz; Heinz weights M1/M2/M3 relationship signals
      heavier than RK Mellon. Same SWPA applicant pitching both code-
      switches per foundation. P1-9 reconciliation pending: charter
      encodes 5-program-area subset; canonical reference §RK Mellon
      enumerates 6 (Conservation / Economic Development / Economic
      Mobility / Health & Well-Being / Organizational Effectiveness /
      Social-Impact Investments).
    source_authority: |
      Canonical reference §Richard King Mellon Foundation (six program
      areas + emphasis: scale, permanence, leadership, measurable
      outcomes). Strategic-capital weighting heuristics operator-derived;
      pinpoint Pillar-2 RK Mellon position-paper / program-officer
      interview ingest pending. Charter program-area subset vs canonical
      6-area roster flagged Pass-1 P1-9.
    prose_summary: |
      Applies strategic-capital register + scale-and-permanence framing +
      conservation-outcomes specificity.
  judge: |
    Cross-checks scale-and-permanence + multi-year commitment readiness +
    senior-leadership relationship.
  red_team: |
    Probes scale mismatch, permanence-mechanism weakness, senior-leadership
    engagement absence, conservation-outcomes specificity.
  logician: |
    PRE-gates F-RK-MELLON-501C3-MISSING (P0),
    F-RK-MELLON-OUT-OF-PROGRAM-AREA (HIGH),
    F-RK-MELLON-SCALE-MISMATCH (MED).

mission_framing:
  one_paragraph_summary: |
    The Richard King Mellon Foundation is a large-scale strategic-capital +
    conservation + regional-economic-development foundation with southwestern
    PA presence. Five program areas: Conservation, Economic Development,
    Education, Family Wellness, Community Vitality. Multi-year, multi-million-
    dollar commitments routine; conservation reach extends beyond region.
  corpus_ref: "<NEEDED — Pillar 2: RK Mellon strategic framework + program-area position papers>"
stage_behavior:
  screen:
    primary_question: "Program-area fit + 501(c)(3) status + organizational scale + senior-leadership engagement readiness."
    time_budget: <NEEDED Pillar 2>
    pass_fail_triggers:
      - "Project outside the 5 program areas → FAIL"
      - "Non-501(c)(3) applicant for direct grant → FAIL (fiscal sponsorship may rescue)"
      - "Scale mismatch (Tier 1 capacity org applying for Tier 4 capital deployment, or vice versa) → DOWNGRADE"
    common_rejections:
      - "Out-of-program-area project with handwave fit to one of the 5 areas."
      - "Cold-outreach without prior RK Mellon relationship or peer-introduction."
      - "Scope mismatch: small applicant requesting strategic-capital-scale deployment without organizational readiness."

  score:
    primary_question: "Scale-and-permanence + program-area fit + senior-leadership relationship + outcomes specificity."
    evidence_rewarded:
      - "Multi-year strategic-capital deployment plan with year-by-year milestones"
      - "Permanence mechanism (endowment build / earned revenue / cross-funder pipeline) for sustained change beyond grant"
      - "Conservation outcomes in protected acres + habitat metrics (for Conservation track)"
      - "Economic-development outcomes in jobs + private-investment leverage (for Economic Dev track)"
      - "Senior-leadership / board relationship documented"
    scoring_blind_spots:
      - "Scale ambition can be over- or under-played; calibrate to applicant capacity."
      - "Permanence mechanism can be aspirational; specificity wins over vision."
    common_penalties:
      - "Generic 'protect natural resources' instead of acres + habitat → -3 to -5 points."
      - "Aspirational permanence ('we hope to sustain') without mechanism → -3 points."
      - "Scope mismatch with applicant capacity → reviewer skepticism on other claims."

  consensus:
    primary_question: "Scale-and-permanence + program-area fit + relationship infrastructure vs panel peers."
    tie_breakers:
      - "Adjacent scale-and-permanence scores: higher band requires named permanence mechanism."
      - "Adjacent conservation-outcomes scores: higher band requires acres + habitat metrics."
    portfolio_considerations: |
      RK Mellon balances funded portfolio across program areas + strategic-
      capital vs smaller-grant blend + southwestern PA + conservation geographies
      beyond region.

evidence_ladder:
  strongest:
    - "Multi-year strategic-capital deployment plan with year-by-year milestones + governance + reporting"
    - "Permanence mechanism (endowment / earned revenue / multi-funder pipeline) with named donors / sources"
    - "Conservation: protected acres + habitat metrics + ecological-outcome measurement"
    - "Economic Dev: FTE jobs + private-investment commitments + signed letters"
    - "Senior-leadership / board prior engagement documented"
  acceptable:
    - "Single-year-then-multi-year roadmap (not full strategic-capital but credible build-up)"
    - "Permanence narrative without named donors"
    - "Conservation: acres alone without habitat metrics"
    - "Letter of introduction from existing RK Mellon grantee"
  weak:
    - "1-year project framing without multi-year vision"
    - "Aspirational permanence ('we hope to attract additional funders')"
    - "Conservation: 'protect natural resources' without acres or habitat"
  unacceptable:
    - "Scope clearly mismatched to applicant capacity"
    - "Project outside the 5 program areas with handwave fit"
    - "Cold-outreach without any introduction pathway"

language_register:
  preferred_terms:
    - strategic_capital
    - scale_and_permanence
    - multi_year_commitment
    - conservation                                           # canonical for RK Mellon Conservation track
    - protected_acres
    - habitat_metrics
    - large_landscape_stewardship
    - regional_economic_development
    - senior_leadership
    - endowment
  suspicious_terms:
    - innovative                                             # rewarded less than scale-and-permanence
    - cutting_edge
    - we_hope_to                                            # aspirational permanence flag
    - significant_impact                                     # without scale + permanence + measurement
  sentence_shapes_that_work:
    - "Over 10-20 years, this project [outcome] in [southwestern PA / specific landscape], deployed at $[X] strategic capital with permanence mechanism [Y]."
    - "Conservation outcomes: [N] protected acres of [habitat type], measured by [methodology], over [T] year horizon."
  sentence_shapes_that_fail:
    - '"We will protect natural resources..." (no acres / habitat)'
    - '"We hope to sustain this beyond the grant..." (aspirational; no mechanism)'
drafting_implications:
  scribe_must_do:
    - "Lead §I with 10-20 year scale-and-permanence framing."
    - "For Conservation track, quantify in protected acres + habitat metrics."
    - "For Economic Dev, quantify in FTE jobs + private-investment leverage."
    - "Document permanence mechanism (endowment / earned revenue / cross-funder pipeline)."
    - "Reference senior-leadership / board engagement readiness in qualifications."
  scribe_must_not_do:
    - "Frame project as 1-year / short-horizon — RK Mellon is multi-year-strategic-capital."
    - "Use aspirational permanence language ('we hope to attract additional funders')."
    - "Conservation framing without acres + habitat metrics."
    - "Submit out-of-program-area project with handwave fit."
  section_ordering_notes: |
    §I 10-20 year scale-and-permanence headline → §II program-area fit +
    specific outcomes → §III permanence mechanism + multi-year roadmap →
    §IV strategic-capital budget + matching → §V senior-leadership + governance
    readiness → §VI work plan.

judge_implications:
  scoring_dimensions_to_weight_harder:
    - "Scale and Permanence — weight ≥25%"
    - "Program-Area Outcomes Specificity — weight ≥20%"
    - "Senior-Leadership / Governance Readiness — weight ≥15%"
  evidence_required_before_high_score:
    - "Scale and Permanence ≥4: multi-year plan + named permanence mechanism"
    - "Outcomes ≥4: acres + habitat (Conservation) OR FTE + private-investment (Economic Dev)"
    - "Governance ≥4: senior-leadership engagement + board readiness documented"

red_team_probe_seeds:
  - probe: "Is applicant organizational capacity aligned with strategic-capital scale, or is there scope mismatch (small org + large request; or large org + small request)?"
    why_it_matters: "Scope mismatch triggers reviewer skepticism."
  - probe: "Is permanence mechanism specific (named endowment / earned revenue / cross-funder pipeline) or aspirational?"
    why_it_matters: "Aspirational permanence = -3 points + trust damage."
  - probe: "For Conservation track, are outcomes in protected acres + habitat metrics, or generic 'protect natural resources'?"
    why_it_matters: "Generic conservation framing = -3 to -5 points."
  - probe: "Is there documented senior-leadership / board prior engagement with RK Mellon, or cold-outreach?"
    why_it_matters: "Strategic-capital deployment requires senior-leadership relationship infrastructure."

logician_gate_candidates:
  - gate: F-RK-MELLON-501C3-MISSING
    gate_type: hard_eligibility_gate
    failure_condition: "kfr.applicant.tax_status != '501c3' AND not kfr.applicant.has_fiscal_sponsor()"
    severity: P0
    fail_action: REJECT_NO_DRAFT
    source_required: true
    corpus_ref: pending_pillar_2  # RK Mellon eligibility per FID_CANONICAL_REFERENCE §RK Mellon Eligibility
    confidence:
      level: medium
      reason: "501(c)(3) requirement is canonical-reference-doc anchored; pinpoint program-page citation pending. Note: canonical reference also names public-agency + mission-driven-for-profit eligibility (for social-impact-investments only); current gate predicate is narrower than canonical reference."
      promotion_requirement: "RK Mellon Foundation Eligibility page text ingested at Pillar-2; predicate may need widening to match canonical-reference scope"
    pass_1_reconciliation_note: "Predicate narrower than canonical reference (which names public agencies + social-impact-investment-eligible for-profits). Pass 6 (inheritance) or operator review should widen predicate; Pass 1 normalizes structure only."
  - gate: F-RK-MELLON-OUT-OF-PROGRAM-AREA
    gate_type: competitive_scoring_signal
    failure_condition: "kfr.project.program_area not in {conservation, economic_development, education, family_wellness, community_vitality}"
    severity: HIGH
    fail_action: WARN_OPERATOR
    source_required: true
    corpus_ref: pending_pillar_2  # RK Mellon Six Program Areas per FID_CANONICAL_REFERENCE
    confidence:
      level: low
      reason: "pre_corpus_hypothesis — predicate lists 5 program areas; canonical reference enumerates 6 (Conservation / Economic Development / Economic Mobility / Health & Well-Being / Organizational Effectiveness / Social-Impact Investments). Predicate roster mismatches canonical reference."
      promotion_requirement: "RK Mellon program-area position papers ingested at Pillar-2; predicate roster reconciled with canonical reference"
    pass_1_reconciliation_note: "Predicate roster (5 areas) mismatches canonical reference roster (6 areas: Conservation, Economic Development, Economic Mobility, Health & Well-Being, Organizational Effectiveness, Social-Impact Investments). Names also differ (family_wellness vs Health & Well-Being; community_vitality not in canonical). Pass 6 (inheritance) or operator review required."
  - gate: F-RK-MELLON-SCALE-MISMATCH
    gate_type: competitive_scoring_signal
    failure_condition: "abs(kfr.applicant.organizational_capacity_tier - kfr.project.requested_capital_tier) > 1"
    severity: MED
    fail_action: WARN_OPERATOR
    source_required: false
    corpus_ref: pending_pillar_2  # operator-pattern heuristic
    confidence:
      level: low
      reason: "pre_corpus_hypothesis — scale-mismatch detection is operator-derived heuristic; capacity-tier and capital-tier scaling functions not specified"
      promotion_requirement: "Operator-attested tier-scaling function specification ingested at Pillar-2"
  - gate: F-RK-MELLON-PERMANENCE-ASPIRATIONAL
    gate_type: competitive_scoring_signal
    failure_condition: "draft.permanence_section.uses_aspirational_language() AND not draft.permanence_section.names_specific_mechanism()"
    severity: MED
    fail_action: WARN_OPERATOR
    source_required: false
    corpus_ref: pending_pillar_2  # operator-pattern heuristic (RK Mellon emphasis on permanence per canonical reference)
    confidence:
      level: low
      reason: "pre_corpus_hypothesis — permanence-vs-aspirational detection is heuristic; RK Mellon emphasis on permanence is canonical-reference-anchored but detection rule is operator-derived"
      promotion_requirement: "Operator-attested aspirational-language detector pattern ingested at Pillar-2"
    pass_1_reconciliation_note: "Purpose-wise drafting heuristic; classified as competitive_scoring_signal per (MED, WARN_OPERATOR) tuple. Migration to drafting_warning with WARN_SCRIBE is a Pass 3 reconciliation candidate."

source_backing:
  corpus_refs:
    - "<NEEDED — Pillar 2: RK Mellon strategic framework + program-area position papers>"
    - "<NEEDED — Pillar 2: RK Mellon 990-PF FY22-FY24>"
    - "<NEEDED — Pillar 2: conservation-strategy publications + regional-economic-development white papers>"
    - "<NEEDED — Pillar 2: 0-2 program officer / senior-leadership conversations (Tier-2/3)>"
  confidence: LOW pre-corpus.
  unresolved_questions:
    - "Cross-program-area scale-vs-smaller-grant blend proportions"
    - "Senior-leadership engagement cadence + escalation paths"
    - "Conservation outcomes catalog (acres + habitat type matrix)"
```

---

## §1 — What "depth" means for THIS artifact

RK Mellon funder-level depth is the **strategic-capital + scale-and-permanence register substrate** — multi-year multi-million-dollar deployment readiness, 10-20 year horizon framing, conservation/economic-dev outcomes specificity, senior-leadership relationship infrastructure. Distinct from Heinz's thematic-portfolio register on scale + permanence axes.

**Codex same-prompt-with/without test:**
- **Without** — Scribe writes 1-3 year project framing typical of mid-sized foundations. Aspirational permanence. Generic conservation framing.
- **With** — Scribe leads §I with 10-20 year scale-and-permanence; quantifies conservation in protected acres + habitat metrics; documents permanence mechanism (named endowment / earned revenue / cross-funder pipeline); references senior-leadership engagement readiness. Judge weights Scale-and-Permanence ≥25% + Outcomes Specificity ≥20% + Governance Readiness ≥15%. Red Team probes scale mismatch + permanence aspirationalism + outcomes specificity + cold-outreach. Logician fails closed on out-of-program-area + non-501(c)(3) + scope mismatch.

---

## §2 — Primary sources in scope

| Corpus category | Specific sources | Access path | Estimated count |
|-----------------|------------------|-------------|-----------------|
| `strategic/` | RK Mellon strategic framework + program-area position papers; annual report | Public RK Mellon site | 2-4 |
| `awards/` | RK Mellon 990-PF FY22-FY24; grants-list extracts; conservation + economic-dev patterns | Public 990-PF (Candid / ProPublica) | 3-5 |
| `interviews/` | 0-2 program officer / senior-leadership conversations (Tier-2/3) | Operator network outreach | 0-2 |
| `guidance/` | Conservation-strategy publications; regional-economic-development white papers | Public RK Mellon publications | 1-3 |
| `geographic/` | Southwestern PA emphasis + conservation reach beyond region | RK Mellon public + 990-PF geographic data | 1-2 |

Case law OUT OF SCOPE.

---

## §3 — Tier classification

| Field | Tier |
|-------|:----:|
| Default | `1` |
| `funder_officer_relationship_notes` | `3` |
| `senior_leadership_relationship_notes` | `3` |
| `dialect_notes_operator_derived` | `2` |
| `strategic_capital_deployment_norms` | `2` |

---

## §4 — Refresh cadence

`annual` + `event_triggered` (leadership change; major strategic-capital initiative announce/close).

---

## §5 — Calibration applicant pair

`food_systems` (CIC-01) × `operating_capacity` (CLC-03), with Catalytic Change (CLC-02) overlay for strategic-capital framing.

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

- Per-initiative grant text (relationship-driven solicitation dominates)
- Other Pittsburgh-region foundations — separate funder artifacts
- RK Mellon large-landscape-conservation transaction internals (real-estate, land-trust mechanics) — compliance / transaction territory
- Compliance framework internals
- Reviewer-type heuristics
- Per-applicant 501(c)(3) status (lives in `orgs/<slug>/`)
- Case law interpretation
