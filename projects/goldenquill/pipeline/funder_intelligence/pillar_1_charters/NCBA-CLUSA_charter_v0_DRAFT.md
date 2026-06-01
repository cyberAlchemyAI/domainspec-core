# Depth Charter — `NCBA-CLUSA` (funder behavior profile)

> **Pillar 1 of 4** per `pipeline/planning/funder_intelligence_database_research_project_2026-05-16.md` §3.1.
> **Quality bar** per `docs/FID_ARTIFACT_OPTIMIZATION_PRINCIPLES_2026-05-18.md` §1 + §2 + Codex framing.
> **Status: DEPTH CHARTER v0 (pre-corpus hypothesis; do not load as signed logic)** — re-authored to Codex yaml shape per operator directive 2026-05-18.
>
> **[CONJECTURE — Pillar-2 corpus pending]** All NCBA-CLUSA-specific funder-fact claims operator-asserted; Pillar-2 corpus assembly (NCBA strategic + Cooperative Identity Statement + Co-op Capital framework + 990 + Rochdale principles operationalization) promotes each. `F-FID-FACT-ORPHAN` enforces.

---

## Header

| Field | Value |
|------:|:------|
| `artifact_id` | `NCBA-CLUSA` |
| `artifact_family` | `funder` |
| `version` | `depth_charter_v0` |
| `lifecycle` | `draft` |
| `phase` | `1 — exemplar pair` |

---

## §A — Adversarial pre-checks

```yaml
runtime_consumer:
  scout:
    reads_fields: [program_roster, cooperative_form_authenticity_signals]
    stage: DISCOVER
    decision_changed: "Scout DISCOVER tags radar hits requiring authentic cooperative form. Downgrades nonprofit-with-cooperative-language applicants who fail Rochdale-principles operational test."
  scribe:
    reads_fields: [funder_dialect, language_register, drafting_implications]
    stage: scaffold
    decision_changed: "Scribe applies cooperative-board-peer-review register: one-member-one-vote framing in §I, member-ownership recordkeeping documented in §II, patronage-distribution mechanics in §III, democratic-governance-as-substance-not-decoration throughout. Distinct from federal-program-officer / foundation-program-officer / peer-reviewer-academic registers."
  judge:
    reads_fields: [judge_implications]
    stage: cross_check
    decision_changed: "Judge cross-checks cooperative-form-authenticity + member-ownership integrity + democratic-governance discipline + patronage-distribution practice; downgrades formal-cooperative-status-without-operational-substance."
  red_team:
    reads_fields: [red_team_probe_seeds]
    stage: probe_target_selection
    decision_changed: "Red Team probes NCBA-CLUSA-specific failure modes: cooperative-form-authenticity (NOT generic nonprofit with cooperative language), Rochdale-principles operationalization (one-member-one-vote? surplus-to-members? democratic governance? member education?), state-cooperative-law compliance (PA cooperative corporation act vs generic nonprofit), patronage-dividend tax pass-through (Subchapter T)."
  logician:
    reads_fields: [eligibility_gates, logician_gate_candidates]
    stage: PRE
    decision_changed: "Logician fires NCBA-CLUSA funder-wide PRE-gates: F-NCBA-NOT-COOPERATIVE-FORM (P0; applicant entity is not formally cooperative under state law), F-NCBA-MEMBER-OWNERSHIP-UNDOCUMENTED (HIGH; cooperative claim without member-ownership records), F-NCBA-DEMOCRATIC-GOVERNANCE-WEAK (HIGH; one-member-one-vote not operationalized OR proxy/concentration concerns)."
```

```yaml
artifact_must_not_contain:
  - facts belonging to another artifact
  - applicant-specific claims
  - uncited generalizations
  - compliance framework internals                         # Subchapter T tax mechanics → compliance_cascades/
  - reviewer-type heuristics                               # → reviewer_heuristics/cooperative-board-peer-reviewer.yaml
  - other cooperative intermediaries                       # DAWI, USFWC, NEFOC-LT = separate
  - case law interpretation
```

```yaml
strength_test:
  - "Name one concrete drafting decision this artifact changes."
  - "Name one proposal this artifact would reject or downgrade."
  - "Name one Red Team probe this artifact enables."
```

**Answers (PASSED):**

1. **Drafting decision.** Scribe writes the **democratic-governance operational substrate** explicitly in §II: *"Cooperative operates under [state cooperative corporation act]; [N] members each with one vote at annual meeting; bylaws Article [X] specifies surplus-to-members allocation per patronage Y; member-education obligation operationalized via [program]."* Without artifact: generic "we are a cooperative" framing. With artifact: Rochdale-principles operational substrate that NCBA-CLUSA reviewers score against.
2. **Proposal rejected.** Logician `F-NCBA-NOT-COOPERATIVE-FORM` (P0) fails closed any application where applicant is not formally cooperative under state law (regardless of cooperative-language self-description). Saves Scribe from drafting cooperative-framed proposals for nonprofits that haven't completed cooperative formation.
3. **Red Team probe.** `NCBA-PROBE-ROCHDALE-OPERATIONALIZATION` asks: *"Are all 7 Rochdale principles operationalized in cooperative practice (voluntary + open membership; democratic member control; member economic participation; autonomy + independence; education + training + information; cooperation among cooperatives; concern for community), or is the cooperative-form claim formal-only?"*

---

## §B — Codex-shape depth-charter YAML

```yaml
artifact_id: NCBA-CLUSA
artifact_family: funder
version: depth_charter_v0
lifecycle: draft
validation_status: pre_corpus_hypothesis
runtime_load_status: do_not_load_as_signed_logic
operator_label: depth_charter_v0

one_sentence_job: |
  Equip every NCBA-CLUSA-targeted draft + every USDA-RD-RCDG cooperative-
  development draft with cooperative-form-authenticity discipline, Rochdale-
  principles operationalization probes, member-ownership recordkeeping
  requirements, and patronage-distribution + state-cooperative-law gates.

runtime_consumers:
  scout:
    pre_filter_question: |
      Is the applicant an authentic cooperative form (Rochdale-operationalized,
      member-owned, state-cooperative-law-compliant) — NOT a nonprofit using
      cooperative language?
    eligibility_dimensions:
      - cooperative_form_authenticity     # state cooperative law incorporation + bylaws + member-equity-and-patronage
      - rochdale_principle_operationalization  # 7 Rochdale principles enacted, not aspirational
      - member_governance_substance       # democratic governance documented in bylaws + minutes
    hard_gate_refs:
      - F-NCBA-NOT-COOPERATIVE-FORM
    cross_funder_signal: |
      Cooperative-intermediary funder; routes opportunity TOWARD other coop
      funders (Cooperative Development Foundation, Capital Impact Partners,
      Shared Capital Cooperative). Flags applicants with nonprofit-only
      structure as wrong-funder-match unless they have an explicit
      cooperative-conversion or cooperative-incubation pathway.
    operator_assist_required: |
      Escalate to operator when: (a) applicant is a nonprofit with cooperative
      language but not formally incorporated as a cooperative (decision needed
      whether to pursue NCBA fit or redirect), (b) member-equity / patronage-
      dividend mechanism is undocumented (F-NCBA-MEMBER-OWNERSHIP-UNDOCUMENTED
      HIGH fires).
    source_authority: |
      [CONJECTURE — Pillar-2 corpus pending] NCBA CLUSA program materials
      + Rochdale Pioneers cooperative principles. Cooperative-form-
      authenticity dimension is the central Pillar-2 ingest target.
    prose_summary: |
      DISCOVER tags hits requiring authentic cooperative form; downgrades
      nonprofit-with-cooperative-language applicants.
  scribe:
    voice_change: |
      Cooperative-board-peer-review register: state-cooperative-corporation-
      act registration documented in §I; all 7 Rochdale principles
      operationalized explicitly in §II; bylaws Articles cited for
      patronage-distribution + surplus-to-members + democratic-governance;
      member-education program (curriculum + facilitator + cadence)
      documented; sister-coop partnerships + NCBA-network engagement
      named.
    section_ordering:
      - "§I cooperative-form registration + member-ownership headline"
      - "§II Rochdale-7-principles operationalization (each principle gets ≥1 substantive paragraph or evidence anchor)"
      - "§III patronage-distribution + surplus-to-members mechanics (bylaws-cited)"
      - "§IV member-education + cooperation-among-cooperatives"
      - "§V cooperative qualifications + sister-coop network"
      - "§VI work plan with member-engagement milestones"
    must_do:
      - "Document state cooperative corporation act registration + filing in §I."
      - "Operationalize all 7 Rochdale principles explicitly in §II."
      - "Cite bylaws Articles for patronage-distribution + surplus-to-members + democratic-governance."
      - "Document member-education program (curriculum + facilitator + cadence)."
      - "Reference sister-coop partnerships + NCBA-network engagement."
    must_not_do:
      - "Frame project as 'cooperative-like' without state-cooperative-filing."
      - "Use 'member-driven' or 'community-oriented' without one-member-one-vote operationalization."
      - "Submit nonprofit + cooperative-language proposal without completing cooperative formation."
      - "Omit member-list / ownership-records when claiming cooperative form."
    cross_funder_signal: |
      NCBA-CLUSA register is COOPERATIVE-AUTHENTICITY-OVERLAY — not a
      standalone-funder register but a cross-funder composable layer.
      Any USDA program favoring cooperatives (RCDG / VAPG / RBDG) or
      foundation funder favoring cooperative governance composes the
      Rochdale-principles operationalization layer over its own register.
      The two principles routinely tested by scoring are
      one-member-one-vote (Rochdale 2) and patronage (Rochdale 3) per
      canonical reference §NCBA CLUSA Use in Grants.
    source_authority: |
      Canonical reference §NCBA CLUSA — Cooperative Authenticity Layer
      + the Rochdale Pioneers principles + IRS Subchapter T cooperative
      tax pass-through. Full Pillar-2 corpus (NCBA program materials +
      ICA Cooperative Identity Statement + state cooperative corporation
      acts) pending ingest per Pass-2 P2-7. Marked
      [CONJECTURE — Pillar-2 corpus pending] until Pillar-2 corroboration
      lands.
    prose_summary: |
      Applies cooperative-board-peer-review register + Rochdale operationalization
      in §II + democratic-governance substance throughout.
  judge: |
    Cross-checks cooperative-form-authenticity + member-ownership + governance
    + patronage-distribution; downgrades formal-cooperative-status-without-substance.
  red_team: |
    Probes cooperative-form-authenticity, Rochdale-7-principles operationalization,
    state-cooperative-law compliance, patronage-dividend pass-through.
  logician: |
    PRE-gates F-NCBA-NOT-COOPERATIVE-FORM (P0),
    F-NCBA-MEMBER-OWNERSHIP-UNDOCUMENTED (HIGH),
    F-NCBA-DEMOCRATIC-GOVERNANCE-WEAK (HIGH).

mission_framing:
  one_paragraph_summary: |
    The National Cooperative Business Association / CLUSA International is the
    national-intermediary anchor for cooperative-board-peer-review register —
    member-driven, democracy-flavored, Rochdale-principles-grounded. Co-op
    Capital + Co-op Federal Credit Union network + member services + technical
    assistance. NCBA-CLUSA reviewer mapping is canonical for USDA-RD-RCDG
    cooperative-development center applicants.
  corpus_ref: "<NEEDED — Pillar 2: NCBA-CLUSA strategic framework + Cooperative Identity Statement>"
stage_behavior:
  screen:
    primary_question: "Cooperative form (state law) + member-ownership documentation + Rochdale-principles operational practice + state-cooperative-law compliance."
    time_budget: <NEEDED Pillar 2>
    pass_fail_triggers:
      - "Applicant not formally cooperative under state law → FAIL"
      - "Member-ownership not documented → FAIL"
      - "One-member-one-vote not operationalized (e.g., proxy concentration; non-member control) → FAIL"
      - "Patronage-dividend / surplus-to-members not specified in bylaws → FAIL"
    common_rejections:
      - "501(c)(3) nonprofit with cooperative language but no cooperative state-filing."
      - "Cooperative form filed but governance dominated by non-member board."
      - "Surplus-to-members allocation absent from bylaws."

  score:
    primary_question: "Cooperative-form-authenticity + Rochdale-7-principles operationalization + member-economic-participation + community-concern integration."
    evidence_rewarded:
      - "State cooperative corporation act registration + filing documentation"
      - "Member-list with member-ownership records + annual-meeting attendance + voting records"
      - "Bylaws Article specifying surplus-to-members allocation + patronage-dividend formula"
      - "Member-education program operationalized (curriculum + facilitator + cadence)"
      - "Cooperation-among-cooperatives evidence (sister-coop partnerships, NCBA-network engagement)"
    scoring_blind_spots:
      - "Cooperative-form-authenticity test is rigorous; informal practice that's spiritually cooperative but legally non-cooperative scores 0."
      - "Patronage-distribution can be deferred (retained-earnings vs immediate-distribution); document discipline either way."
    common_penalties:
      - "Formal cooperative status without operational substance → -10+ points (functionally administrative rejection)."
      - "Member-education absent or generic → -3 to -5 points."
      - "Concentration concerns (e.g., 3 members control 80% of votes) → -5+ points."

  consensus:
    primary_question: "Cooperative-form-authenticity + Rochdale-7-principles operationalization + community-concern vs panel peers."
    tie_breakers:
      - "Adjacent cooperative-form scores: higher band requires all 7 Rochdale principles operationalized."
      - "Adjacent member-participation scores: higher band requires annual-meeting attendance + voting-records documented."
    portfolio_considerations: |
      NCBA-CLUSA balances funded portfolio across cooperative types (worker /
      producer / consumer / housing / multi-stakeholder) + maturity stages
      (emergent / established / scaling).

evidence_ladder:
  strongest:
    - "State cooperative corporation act registration + filing"
    - "Member-list + ownership records + annual-meeting attendance + voting records"
    - "Bylaws Article specifying patronage-distribution formula + surplus-to-members allocation"
    - "Member-education program operationalized with curriculum + facilitator + cadence"
    - "Sister-coop partnerships + NCBA-network engagement documented"
  acceptable:
    - "State cooperative filing + bylaws + member-list (without annual-meeting records)"
    - "Cooperative form + informal sister-coop engagement"
    - "Member-education narrative without full curriculum"
  weak:
    - "501(c)(3) nonprofit with cooperative language (no state cooperative filing)"
    - "Cooperative filing without operationalized democratic governance"
    - "Generic 'member-driven' claim without member-list"
  unacceptable:
    - "Aggregator/intermediary claiming cooperative form without state filing"
    - "Cooperative form with concentration (3 members controlling >80% of votes)"
    - "Surplus-to-members absent from bylaws"

language_register:
  preferred_terms:
    - cooperative
    - member_ownership
    - one_member_one_vote
    - patronage_dividend
    - surplus_allocation
    - Rochdale_principles
    - democratic_governance
    - member_education
    - cooperation_among_cooperatives
    - Subchapter_T                                          # IRS cooperative tax pass-through
  suspicious_terms:
    - innovative
    - cutting_edge
    - we_are_cooperative                                   # without operational substance
    - member_driven                                        # without one-member-one-vote operationalization
    - community_oriented_nonprofit                         # signals NOT cooperative form
  sentence_shapes_that_work:
    - "Cooperative registered under [state cooperative corporation act §X], with [N] members each holding one vote at annual meeting (Bylaws Art. [Y]). Surplus allocated to members per patronage formula in Bylaws Art. [Z]."
    - "All 7 Rochdale principles operationalized: [voluntary membership: open enrollment]; [democratic governance: annual meeting + member vote]; [member economic participation: patronage distribution]; [autonomy: independence from non-member control]; [education: curriculum + facilitator]; [cooperation: sister-coop partnerships]; [community concern: outreach program]."
  sentence_shapes_that_fail:
    - '"We are a member-driven organization..." (without operational substance)'
    - '"Our cooperative approach to community work..." (cooperative as adjective; not cooperative as form)'
drafting_implications:
  scribe_must_do:
    - "Document state cooperative corporation act registration + filing in §I."
    - "Operationalize all 7 Rochdale principles explicitly in §II."
    - "Cite bylaws Articles for patronage-distribution + surplus-to-members + democratic-governance."
    - "Document member-education program (curriculum + facilitator + cadence)."
    - "Reference sister-coop partnerships + NCBA-network engagement."
  scribe_must_not_do:
    - "Frame project as 'cooperative-like' without state-cooperative-filing."
    - "Use 'member-driven' or 'community-oriented' without one-member-one-vote operationalization."
    - "Submit nonprofit + cooperative-language proposal without completing cooperative formation."
    - "Omit member-list / ownership-records when claiming cooperative form."
  section_ordering_notes: |
    §I cooperative-form-registration + member-ownership headline →
    §II Rochdale-7-principles operationalization →
    §III patronage-distribution + surplus-to-members mechanics →
    §IV member-education + cooperation-among-cooperatives →
    §V cooperative qualifications + sister-coop network →
    §VI work plan with member-engagement milestones.

judge_implications:
  scoring_dimensions_to_weight_harder:
    - "Cooperative Form Authenticity + Rochdale Operationalization — weight ≥30%"
    - "Member Ownership + Democratic Governance — weight ≥20%"
    - "Patronage Distribution + Member Education — weight ≥15%"
  evidence_required_before_high_score:
    - "Cooperative-Form ≥4: state cooperative corporation act registration + all 7 Rochdale operationalized"
    - "Governance ≥4: annual-meeting attendance + voting records + no concentration concerns"
    - "Distribution ≥4: bylaws Article specifying formula + actual annual-distribution practice"

red_team_probe_seeds:
  - probe: "Is applicant entity formally cooperative under state cooperative corporation act, or is it a 501(c)(3) nonprofit with cooperative language?"
    why_it_matters: "P0 administrative rejection if formal cooperative form absent."
  - probe: "Are all 7 Rochdale principles operationalized (voluntary membership; democratic governance; member economic participation; autonomy; education; cooperation; community concern), or is the cooperative claim formal-only?"
    why_it_matters: "Formal cooperative status without operational substance = -10+ points."
  - probe: "Is one-member-one-vote operationalized (member-list + annual-meeting + voting records), or is governance concentrated (3 members controlling >80%)?"
    why_it_matters: "Concentration concerns are -5+ points."
  - probe: "Does bylaws specify patronage-distribution formula + surplus-to-members allocation explicitly?"
    why_it_matters: "Patronage discipline is canonical cooperative-form distinguishing test."

logician_gate_candidates:
  - gate: F-NCBA-NOT-COOPERATIVE-FORM
    gate_type: hard_eligibility_gate
    failure_condition: "kfr.applicant.entity_type != 'cooperative' OR not kfr.applicant.has_state_cooperative_filing()"
    severity: P0
    fail_action: REJECT_NO_DRAFT
    source_required: true
    corpus_ref: pending_pillar_2  # PA cooperative corporation act + state cooperative filing requirement
    confidence:
      level: medium
      reason: "Cooperative-form requirement is canonical-reference-doc anchored (FID_CANONICAL_REFERENCE §NCBA CLUSA). PA cooperative corporation act citation pending Pillar-2"
      promotion_requirement: "PA cooperative corporation act + IRS Subchapter T patronage-dividend guidance ingested at Pillar-2"
    pass_1_reconciliation_note: "NCBA CLUSA is an overlay register, not a standalone funder per canonical reference. P0 fire-condition applies only when downstream funder requires cooperative form (VAPG / RCDG / some foundation funders). Per-funder composition is operator-decision; flag for Pass 6 inheritance review."
  - gate: F-NCBA-MEMBER-OWNERSHIP-UNDOCUMENTED
    gate_type: competitive_scoring_signal
    failure_condition: "not kfr.applicant.has_member_list_with_ownership_records()"
    severity: HIGH
    fail_action: WARN_OPERATOR
    source_required: true
    corpus_ref: pending_pillar_2  # Cooperative Identity Statement (Rochdale principle 3: member economic participation)
    confidence:
      level: medium
      reason: "Member-ownership documentation is Rochdale-principle-3 anchored; pinpoint cooperative-identity-statement citation pending"
      promotion_requirement: "ICA Cooperative Identity Statement ingested at Pillar-2"
  - gate: F-NCBA-DEMOCRATIC-GOVERNANCE-WEAK
    gate_type: competitive_scoring_signal
    failure_condition: "not kfr.applicant.has_one_member_one_vote_operationalized() OR kfr.applicant.has_voting_concentration_above_threshold(0.5, members=3)"
    severity: HIGH
    fail_action: WARN_OPERATOR
    source_required: true
    corpus_ref: pending_pillar_2  # Rochdale principle 2: democratic member control
    confidence:
      level: medium
      reason: "One-member-one-vote is Rochdale-principle-2 + canonical-reference-doc anchored; concentration-threshold heuristic is operator-derived"
      promotion_requirement: "Rochdale principle 2 + operator-attested concentration threshold ingested at Pillar-2"
  - gate: F-NCBA-PATRONAGE-DISTRIBUTION-BYLAWS-MISSING
    gate_type: competitive_scoring_signal
    failure_condition: "not kfr.applicant.bylaws.specifies_patronage_distribution_formula()"
    severity: HIGH
    fail_action: WARN_OPERATOR
    source_required: true
    corpus_ref: pending_pillar_2  # Rochdale principle 3 (patronage) + IRS Subchapter T
    confidence:
      level: medium
      reason: "Patronage discipline is Rochdale-principle-3 + IRS Subchapter T anchored (canonical-reference-doc references it as canonical cooperative-form-distinguishing test)"
      promotion_requirement: "IRS Subchapter T patronage-dividend regulations + ICA cooperative-identity statement ingested at Pillar-2"

source_backing:
  corpus_refs:
    - "<NEEDED — Pillar 2: NCBA-CLUSA strategic framework>"
    - "<NEEDED — Pillar 2: Cooperative Identity Statement (Rochdale principles)>"
    - "<NEEDED — Pillar 2: Co-op Capital underwriting framework>"
    - "<NEEDED — Pillar 2: 990 + Co-op Capital deployment history>"
    - "<NEEDED — Pillar 2: PA cooperative corporation act references>"
    - "<NEEDED — Pillar 2: IRS Subchapter T patronage-dividend guidance>"
  confidence: LOW pre-corpus.
  unresolved_questions:
    - "Whether NCBA-CLUSA accepts limited-cooperative-association forms (some states have new variants)"
    - "Member-education program acceptance criteria"
    - "Cross-coop-type variance in evaluation discipline (worker / producer / consumer / housing / multi-stakeholder)"
```

---

## §1 — What "depth" means for THIS artifact

NCBA-CLUSA funder-level depth is the **cooperative-board-peer-review register substrate** — formal cooperative form under state law, Rochdale-7-principles operationalization, member-ownership recordkeeping, patronage-distribution mechanics, democratic-governance substance. Distinct from foundation-program-officer / federal-program-officer / peer-reviewer-academic registers on every load-bearing axis.

**Codex same-prompt-with/without test:**
- **Without** — Scribe writes "we are a cooperative organization" framing. Generic nonprofit-with-cooperative-language proposal.
- **With** — Scribe documents state cooperative corporation act registration in §I; operationalizes all 7 Rochdale principles in §II; cites bylaws Articles for patronage-distribution; documents member-education program. Judge weights Cooperative-Form-Authenticity ≥30% + Member-Ownership ≥20% + Patronage Distribution ≥15%. Red Team probes Rochdale operationalization + concentration concerns + patronage discipline. Logician fails closed on non-cooperative form + missing member-ownership + governance weakness + patronage missing.

Force-multiplier: USDA-RD-RCDG cooperative-development applicants also inherit this register + cascade per RCDG's cooperative-form authenticity test (cross-funder pattern).

---

## §2 — Primary sources in scope

| Corpus category | Specific sources | Access path | Estimated count |
|-----------------|------------------|-------------|-----------------|
| `strategic/` | NCBA-CLUSA strategic framework + Cooperative Identity Statement; Rochdale principles operationalization guides | Public NCBA-CLUSA site | 3-4 |
| `regulatory/` | PA cooperative corporation act references; IRS Subchapter T patronage-dividend guidance | PA General Assembly + IRS | 2-3 |
| `awards/` | NCBA-CLUSA 990 + Co-op Capital deployment history | Public 990 + NCBA reports | 2-3 |
| `interviews/` | 0-2 NCBA program contact conversations (Tier-2/3) | Operator network outreach | 0-2 |
| `guidance/` | Rochdale operationalization guidance + cooperative governance best practices | NCBA publications | 1-3 |
| `cooperative_form/` | State-law variance (PA cooperative corporation act); patronage-dividend tax pass-through | NCBA + IRS Subchapter T | 1-2 |

Case law OUT OF SCOPE.

---

## §3 — Tier classification

| Field | Tier |
|-------|:----:|
| Default | `1` |
| `funder_officer_relationship_notes` | `3` |
| `dialect_notes_operator_derived` | `2` |
| `cooperative_identity_principles` | `1` (Rochdale public) |
| `member_education_norms` | `2` (operator-derived) |

---

## §4 — Refresh cadence

`annual` + `event_triggered` (NCBA-CLUSA strategic update; intermediary mergers).

---

## §5 — Calibration applicant pair

`cooperative` (CIC-05) primary; `food_systems` (CIC-01) overlay. Reference applicants of either CIC are named only in their own `orgs/<slug>/PROJECT_CONTEXT.md`.

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

- Other cooperative intermediaries (DAWI, USFWC, NEFOC-LT) — separate funder artifacts
- International cooperative development pass-through programs (out of scope for the current FID consumer roster)
- Compliance framework internals
- Reviewer-type heuristics (lives in `reviewer_heuristics/cooperative-board-peer-reviewer.yaml`)
- Per-applicant cooperative state-of-formation detail (lives in `orgs/<slug>/`; Law 3 org-isolation enforces separation between any two distinct legal entities even when they share branding or operator)
- IRS Subchapter T tax mechanics interpretation (compliance-officer territory)
- Case law interpretation
