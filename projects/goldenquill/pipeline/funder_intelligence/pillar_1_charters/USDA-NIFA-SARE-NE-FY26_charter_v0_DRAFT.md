# Depth Charter — `USDA-NIFA-SARE-NE-FY26` (Partnership Grant track focus)

> **Pillar 1 of 4** per `pipeline/planning/funder_intelligence_database_research_project_2026-05-16.md` §3.1.
> **Quality bar** per `docs/FID_ARTIFACT_OPTIMIZATION_PRINCIPLES_2026-05-18.md` §1 + §2 + Codex framing (2026-05-18).
> **Status: DEPTH CHARTER v0 (pre-corpus hypothesis; do not load as signed logic)** — methodology anchor + quality bar for the other 12 charters in the Week-1 roster. Operator override 2026-05-18 swapped this charter from RBDG; rationale (Partnership track open cycle + best fit for FIT Farms applicant shape) lives in PR #33 body, not here. Operator review + Ed25519 sign-off pending. **Once operator approves this depth-charter, the other 12 charters are re-authored as `[PRE-DEPTH-CHARTER]` placeholders pending re-author at the same quality bar.**
>
> **[CONJECTURE — Pillar-2 corpus pending]** All SARE-NE-specific facts in this charter are operator-asserted + general-knowledge-grounded at charter authoring. Pillar-2 corpus assembly (FY26 Partnership RFA + national SARE framework + 2 years of NE-region award rosters + reviewer-debrief synthesis) must promote each claim with `corpus_ref` + ≤2-sentence verbatim quote or remove it. Logician `F-FID-FACT-ORPHAN` enforces at Pillar-3 L-005.

---

## Header

| Field | Value |
|------:|:------|
| `artifact_id` | `USDA-NIFA-SARE-NE-FY26` |
| `artifact_family` | `program` |
| `track_focus` | **Partnership Grant** (the depth-charter depth target; other SARE-NE tracks — Farmer/Rancher, Research & Education, Sustainable Communities, Professional Development — get parallel artifacts at scale-out, not depth in this artifact) |
| `funder_pointer` | `USDA-NIFA` |
| `cycle_status` | **OPEN** (FY26 Partnership cycle confirmed by operator 2026-05-18) |
| `version` | `depth_charter_v0` |
| `lifecycle` | `draft` (pre-sign) |

---

## §A — Adversarial pre-checks (canonical 2026-05-18)

Per `docs/FID_ARTIFACT_OPTIMIZATION_PRINCIPLES_2026-05-18.md` §2 + Codex framing.

```yaml
runtime_consumer:
  scout:
    reads_fields: [scout_verify.live_check_url, scout_verify.expected_response_indicator, nofo.cycle_status, eligibility_gates]
    stage: both
    decision_changed: "Scout DISCOVER filters radar to applicant-context with at least one producer + one researcher named (Partnership requires the pair). Scout VERIFY checks the SARE-NE Partnership RFA page returns 200 with FY26 + non-past deadline; non-conforming responses downgrade to VERIFICATION_FAILED."
  scribe:
    reads_fields: [scribe_section_requirements, scoring_rubric, evidence_ladder, language_register, drafting_implications]
    stage: both
    decision_changed: "Scribe leads §I narrative with the SARE three-pillar sustainability framing (economically viable + environmentally sound + socially responsible) cited verbatim from SARE's published definition, NOT a paraphrase. Scribe structures producer-researcher partnership as named co-investigators with defined roles, not as 'PI + farm-collaborator.' Scribe leads outreach plan with audience + format + dissemination channel + measurable reach target, not generic 'we will share results.'"
  judge:
    reads_fields: [scoring_rubric, judge_implications, evidence_ladder]
    stage: rubric_scoring
    decision_changed: "Judge applies the SARE-NE Partnership-specific 5-criterion rubric with sustainability weighted ≥25% and outreach weighted ≥15% (verify FY26 weights at Pillar 2); tie-breakers favor drafts with producer-as-named-co-investigator over producer-as-collaborator. Judge scores outreach criterion 0 when only single farm-day named (single-channel dissemination)."
  red_team:
    reads_fields: [red_team_probe_seeds, language_register.suspicious_terms]
    stage: probe_target_selection
    decision_changed: "Red Team probes outreach-plan adequacy (single-channel = downgrade), producer-engagement authenticity (named co-investigator OR data-source-only), three-pillar coverage gap (one pillar treated as afterthought = scoring penalty), IRB status presence/absence when human-subject research signals are in narrative."
  logician:
    reads_fields: [eligibility_gates, logician_gate_candidates]
    stage: PRE
    decision_changed: "Logician fails closed on F-SARE-NE-PARTNERSHIP-NO-PRODUCER (P0; applicant team lacks a named producer participant), F-SARE-NE-PARTNERSHIP-NO-RESEARCHER (P0; team lacks a named research/extension/NGO partner), F-SARE-NE-IRB-MISSING (HIGH; KFR.project.human_subjects_research==true AND KFR.applicant.irb_protocol_id is null), F-SARE-NE-OUTREACH-PLAN-MISSING (HIGH; KFR.project.outreach_plan is null or empty)."
```

```yaml
artifact_must_not_contain:
  - facts belonging to another artifact          # USDA-NIFA funder-level facts → funders/USDA-NIFA.yaml
  - applicant-specific claims                    # no FIT Farms / MycoSymbiotics / any named applicant
  - uncited generalizations                      # every fact carries corpus_ref + ≤2-sentence verbatim at Pillar 3
  - other SARE-NE tracks' depth                  # this artifact narrows to Partnership; sibling tracks get parallel artifacts at scale-out
  - other SARE regions                           # Southern, North Central, Western SARE = sibling artifacts
  - compliance framework internals               # 2 CFR 200, IRB Common Rule → compliance_cascades/
  - reviewer-type heuristics                     # reviewer_heuristics/peer-reviewer-academic.yaml + farmer-reviewer overlay
  - case law interpretation                      # compliance-officer territory
```

```yaml
strength_test:
  - "Name one concrete drafting decision this artifact changes."
  - "Name one proposal this artifact would reject or downgrade."
  - "Name one Red Team probe this artifact enables."
```

**Answers (PASSED — concretely realized in §1 below + §9 yaml preview):**

1. **Drafting decision.** Scribe's §I narrative opening leads with SARE's verbatim three-pillar sustainability definition ("economically viable, environmentally sound, and socially responsible") — not a paraphrase — because the SARE-NE Partnership rubric criterion #1 (Sustainability of Agriculture) rewards three-pillar coverage explicitly and downgrades single-pillar treatment. Same Scribe prompt WITHOUT this artifact produces a generic "we will use sustainable practices" opening that scores partial on criterion #1; WITH the artifact produces a three-pillar-bounded opening that scores full.
2. **Proposal rejected.** Logician `F-SARE-NE-PARTNERSHIP-NO-PRODUCER` (P0) fails closed any applicant team that does not name at least one producer participant with verified production context. Scribe is never invoked; operator gets a redirect to SARE-NE Research & Education track (where university PI + farmer collaborator suffices) or to AFRI Foundational (where no producer is required at all). Without this artifact, an ineligible single-PI draft is generated and rejected at SARE-NE administrative review.
3. **Red Team probe.** Red Team's `SARE-NE-PROBE-OUTREACH-CHANNEL-COUNT` probe asks: *"How many DISTINCT dissemination channels (farm day + publication + workshop + on-line resource + extension bulletin + farmer-to-farmer mentoring etc.) does the outreach plan name, with measurable reach targets per channel?"* SARE-NE Partnership rubric criterion on Outreach historically downgrades single-channel plans by ≥40% of the criterion's points (verify FY26 weight). Generic Red Team probes outreach 'adequacy' qualitatively; SARE-aware Red Team probes channel COUNT with measurable reach targets per channel — a specific, mechanical adversarial vector.

---

## §B — Codex-shape depth-charter YAML (the load-bearing decision substrate)

This is the artifact Pillar-3 extraction will populate fully against the FY26 RFA corpus. Pre-corpus values carry `<NEEDED — verify FY26 RFA>` markers; Pillar-2 promotes each.

```yaml
artifact_id: USDA-NIFA-SARE-NE-FY26
artifact_family: program
version: depth_charter_v0
lifecycle: draft
validation_status: pre_corpus_hypothesis
runtime_load_status: do_not_load_as_signed_logic
operator_label: depth_charter_v0

one_sentence_job: |
  Equip Scribe to write a Partnership-grant-shaped proposal with named
  producer + researcher co-investigators, three-pillar sustainability
  framing cited verbatim from SARE, and a multi-channel outreach plan with
  measurable reach — and equip Logician + Judge + Red Team to fail-close or
  downgrade drafts that miss any of those three load-bearing elements.

runtime_consumers:
  scout:
    pre_filter_question: |
      Does the applicant context include (a) at least one named producer,
      (b) at least one named researcher / extension / NGO, (c) a defensible
      outreach plan covering ≥2 channels, and (d) a SARE-NE Partnership
      project scope within FY26 budget cap?
    eligibility_dimensions:
      - producer_named                    # at least one producer named (not generic "producers will be engaged")
      - researcher_or_extension_named     # at least one researcher / extension / NGO named
      - outreach_channel_count            # ≥2 outreach channels documented (SARE-NE explicit requirement)
      - budget_cap_compliance             # project total within SARE-NE Partnership budget cap
      - irb_status                        # IRB approval / pending / not-needed (when human-subject signals present)
    hard_gate_refs:
      - F-SARE-NE-PARTNERSHIP-NO-PRODUCER
      - F-SARE-NE-PARTNERSHIP-NO-RESEARCHER
      - F-SARE-NE-BUDGET-OVER-CAP
    cross_funder_signal: |
      Federal-research program-instance funder under USDA-NIFA funder-level.
      Routes opportunity LATERALLY to USDA-NIFA AFRI when scientific-merit
      framing is dominant + producer-engagement is weak; routes TOWARD
      USDA-AMS when value-added market focus is stronger than research focus.
      Northeast-SARE region applicability (NY, PA, MA, ME, VT, NH, RI, CT,
      NJ, DE, MD, WV, DC + tribal lands) — out-of-region applicants routed
      to their regional SARE program (Southern, North-Central, Western).
    operator_assist_required: |
      Escalate to operator when: (a) only generic "producers will be engaged"
      language present (operator confirms named producer is plausible),
      (b) IRB status unclear when project has human-subject signals
      (researcher confirms IRB pathway), (c) project scope exceeds budget
      cap (F-SARE-NE-BUDGET-OVER-CAP P0 fires — operator must trim scope
      or pivot to larger SARE program track).
    source_authority: |
      USDA-NIFA-SARE-NE FY26 Partnership Grant RFA (canonical reference
      §SARE-NE Partnership FY26). VERIFY: RFA URL returns 200, "FY26"
      literal in body, non-past closing_date.
    prose_summary: |
      DISCOVER filters radar to applicant-context with at least one producer
      + one researcher/extension/NGO named. VERIFY checks SARE-NE Partnership
      RFA URL returns 200 + FY26 literal + non-past closing_date.
  scribe:
    voice_change: |
      Sustainable-agriculture-research register (SARE-specific overlay
      on USDA-NIFA academic register): SARE's three-pillar sustainability
      definition (economically viable + environmentally sound + socially
      responsible) cited verbatim in §I; producer named as co-investigator
      (NOT collaborator / subject / data source); outreach plan as a
      distinct section with ≥3 dissemination channels + reach target per
      channel + timeline; producer-engagement letter on PRODUCER
      letterhead (not researcher-institution letterhead).
    section_ordering:
      - "§I Project Summary + three-pillar sustainability framing (SARE definition verbatim)"
      - "§II Producer-Researcher Partnership (named co-investigators + roles + producer letterhead letter referenced)"
      - "§III Outreach Plan (channels + audiences + reach targets + timeline)"
      - "§IV Research Design (methodology + prior evidence + measurement)"
      - "§V Budget + justification (NIFA indirect-cost cap respected)"
      - "§VI Qualifications"
    must_do:
      - "Open §I with SARE's three-pillar sustainability definition cited VERBATIM from the SARE national framework (corpus_ref required at Pillar 3); do NOT paraphrase."
      - "Name the producer co-investigator on the first page of the project narrative, with research role defined (not 'collaborator' / 'farmer participant')."
      - "Structure the outreach plan with ≥3 named dissemination channels, each with (a) audience, (b) format, (c) reach target, (d) timeline. Front-load this plan in §II or §III for reviewer visibility."
      - "Cite prior-evidence (peer-reviewed publication, prior SARE outcome, NRCS practice trial) before describing the proposed intervention; SARE reviewers reward grounded extension, not novel speculation."
      - "Include producer-engagement letter on PRODUCER letterhead, signed by the producer, confirming partnership commitment + time + research-role responsibility. Letter on researcher-institution letterhead = downgrade signal."
      - "Treat the 'socially responsible' pillar as substantive — write ≥1 paragraph covering community, equity, farmworker conditions, cultural fit, or producer livelihoods; do NOT relegate to one-line gesture."
    must_not_do:
      - "Use 'innovative' / 'cutting-edge' / 'revolutionary' without naming the concrete operational difference."
      - "Frame producer as 'subject' / 'data source' / 'site' / 'participant' — these signal extractive research, not partnership."
      - "Leave outreach plan as 'we will share findings' or 'results will be published' — that's a Red Team probe target."
      - "Cite blog posts / vendor materials / trade press as evidence for proposed practice effectiveness."
      - "Submit budget with university indirect costs at non-NIFA-capped rate without prior negotiation documented."
    cross_funder_signal: |
      SARE-NE register OVERLAYS USDA-NIFA's peer-review-academic base
      register with sustainable-agriculture-specific moves: producer-as-
      co-investigator (not subject), three-pillar framing, multi-channel
      outreach. Same researcher applying to AFRI vs SARE code-switches
      partner framing (AFRI: collaborator-acceptable; SARE: co-investigator-
      required). Northeast-region applicability; out-of-region applicants
      route to sister-SARE programs (Southern / North-Central / Western).
      Farmer Grant track (under-$30K) further code-switches to plain-
      language operator narrative.
    source_authority: |
      USDA-NIFA-SARE-NE FY26 Partnership Grant RFA (canonical reference
      §SARE-NE Partnership FY26 + §SARE-canonical three-pillar definition).
      SARE national framework definition source-backed. Producer-as-co-
      investigator weighting heuristic operator-derived from SARE
      Partnership track guidance; pinpoint Pillar-2 FY26 RFA ingest
      pending.
    prose_summary: |
      Scaffold reads required_application_elements + section_ordering_notes;
      Substance reads drafting_implications.scribe_must_do +
      language_register + evidence_ladder + reviewer-type pointer.
  judge: |
    Reads scoring_rubric + judge_implications + evidence_ladder; applies
    SARE-NE-Partnership-specific rubric instead of generic 12-dimension
    Tilth scoring.
  red_team: |
    Reads red_team_probe_seeds + language_register.suspicious_terms +
    known_failure_modes_from_prior_cycles; probes SARE-specific failure
    vectors (outreach-channel count, producer-engagement authenticity,
    three-pillar coverage gap, IRB presence when human-subject signals).
  logician: |
    Reads eligibility_gates + logician_gate_candidates + cascade pointers
    → 2-CFR-200-UG.yaml. PRE-gates fail closed on missing producer, missing
    researcher, missing outreach plan, missing IRB when needed.

stage_behavior:
  screen:
    primary_question: |
      Is the applicant team eligible (producer + researcher/extension/NGO
      pair named), is the budget within the Partnership cap (NEEDED —
      verify FY26 typical $30K-$50K), is SAM.gov active + UEI present,
      is the outreach plan present (even if thin)?
    time_budget: <NEEDED — verify FY26 SARE-NE Partnership screen-stage budget; historical ~0.5 hr/proposal>
    pass_fail_triggers:
      - "Missing named producer → FAIL"
      - "Missing named researcher/extension/NGO partner → FAIL"
      - "Outreach plan section absent → FAIL"
      - "Budget exceeds Partnership cap → FAIL"
      - "SAM.gov inactive at submission → FAIL"
    common_rejections:
      - "Single-PI applications with farmer named only in collaborator section (producer-as-collaborator, not co-investigator) — SARE-NE screen-stage reviewers flag this as Partnership-form-violation."
      - "Outreach plan reads 'we will share results' without channels, formats, or reach targets — interpreted as no outreach plan."
      - "Budget includes university overhead at NIFA-cap-exceeding rate without negotiated waiver."

  score:
    primary_question: |
      How rigorously does the proposal demonstrate three-pillar sustainability,
      producer-researcher partnership integrity, scientific merit, potential
      impact, and multi-channel outreach with measurable reach?
    evidence_rewarded:
      - "Three-pillar sustainability framing with SARE-canonical definition cited verbatim"
      - "Producer-as-named-co-investigator with defined research role (not 'collaborator' / 'subject' / 'data source')"
      - "Outreach plan with ≥3 dissemination channels + reach target per channel + dissemination timeline"
      - "Prior-evidence cite (peer-reviewed publication, prior SARE outcome, NRCS practice trial) for the proposed practice"
      - "Producer-engagement letter on producer letterhead (not researcher institution letterhead) confirming partnership commitment"
    scoring_blind_spots:
      - "Reviewers may over-weight scientific merit if narrative reads as conventional research and under-weight producer-engagement authenticity. Counterbalance by leading §I with partnership framing before scientific design."
      - "Outreach criterion is often graded last in panel discussion and can be deprioritized if proposal looks otherwise strong — but it's a 15%+ weighted criterion. Front-load outreach plan in §II or §III for visibility."
    common_penalties:
      - "Three-pillar narrative covers economic + environmental but treats 'socially responsible' pillar as afterthought (no community / equity / farmworker / cultural framing) → -3 to -5 points on Sustainability criterion."
      - "Single-channel outreach (farm day OR publication, not both) → -5 to -7 points on Outreach criterion."
      - "Producer named as 'farmer collaborator' rather than co-investigator with defined research role → -3 points on Partnership criterion."

  consensus:
    primary_question: |
      Across the panel's scored proposals, how does this proposal's
      partnership integrity + outreach reach + three-pillar coverage
      compare to the panel's other top-quartile candidates?
    tie_breakers:
      - "Between two adjacent scores on Sustainability criterion, the higher band requires explicit three-pillar coverage with each pillar getting ≥1 substantive paragraph."
      - "Between two adjacent scores on Outreach criterion, the higher band requires ≥3 named channels with reach targets per channel."
      - "Between two adjacent scores on Partnership criterion, the higher band requires producer-named-as-co-investigator with research role (not collaborator)."
    portfolio_considerations: |
      SARE-NE panels balance funded proposals across NE-region states +
      production-type diversity (livestock, vegetable, grain, dairy,
      specialty crop, agroforestry). A strong proposal from an
      over-represented state-type-pair may rank below a slightly weaker
      proposal from an under-represented one. Operator should NOT
      contort the proposal to fit a perceived gap, but Scribe should be
      aware that geographic/production-type framing is a soft consensus
      lever.

evidence_ladder:
  strongest:
    - "Peer-reviewed publication of the proposed practice with effect sizes for the proposed agroecosystem"
    - "Prior SARE outcome-database entry naming the producer or researcher with documented results"
    - "Producer-engagement letter on producer letterhead with explicit research-role commitment + time commitment"
    - "NRCS practice trial data for the proposed practice in the proposed region"
  acceptable:
    - "Regional extension bulletin documenting the proposed practice"
    - "USDA-AMS Census of Agriculture data for the proposed region establishing baseline conditions"
    - "Producer's own production records (verified by NRCS or extension) demonstrating baseline"
    - "Practitioner-to-practitioner network reference (e.g., named farmer-mentor with proven track record)"
  weak:
    - "Trade-press article on the practice"
    - "General-purpose sustainability framework citations not specific to the practice or region"
    - "Researcher's prior publications on adjacent topics (without effect-size carryover argument)"
  unacceptable:
    - "Blog posts, social-media claims, vendor marketing materials"
    - "Unverified producer assertions presented as research findings"
    - "Speculative effect sizes not tied to a baseline + counterfactual"

language_register:
  preferred_terms:
    - sustainable_agriculture  # SARE-canonical; verbatim from SARE definition
    - economically_viable
    - environmentally_sound
    - socially_responsible
    - producer  # not 'farmer' alone; SARE includes ranchers, producers, growers
    - co_investigator  # for the producer partner; signals partnership integrity
    - outreach
    - dissemination
    - measurable_outcome
    - on_farm_research  # SARE-canonical
    - producer_to_producer  # SARE-canonical for farmer-network outreach
  suspicious_terms:
    - innovative                # SARE reviewers averse without specific operational difference
    - cutting_edge              # generic-sounding; SARE prefers concrete + measurable
    - subject                   # for the producer — implies extraction, not partnership
    - collaborator              # for the producer — should be co-investigator; collaborator is weaker
    - will_share_results        # placeholder for outreach plan; trigger for Red Team probe
    - significant_impact        # without effect size + counterfactual
  sentence_shapes_that_work:
    - "We will [specific action] with [named producer] as co-investigator, measuring [specific outcome] over [timeframe], with reach to [N] producers via [named channels]."
    - "SARE defines sustainable agriculture as [verbatim three-pillar definition]. This proposal advances all three pillars through [pillar 1 mechanism], [pillar 2 mechanism], [pillar 3 mechanism]."
  sentence_shapes_that_fail:
    - '"We will conduct research and share findings." (generic; no outreach channels; no co-investigator language)'
    - '"Our innovative approach will revolutionize..." (suspicious terms; no concrete operational difference)'
    - '"Farmers will benefit from..." (passive; producer-as-recipient, not co-investigator)'
drafting_implications:
  scribe_must_do:
    - "Open §I with SARE's three-pillar sustainability definition cited VERBATIM from the SARE national framework (corpus_ref required at Pillar 3); do NOT paraphrase."
    - "Name the producer co-investigator on the first page of the project narrative, with research role defined (not 'collaborator' / 'farmer participant')."
    - "Structure the outreach plan with ≥3 named dissemination channels, each with (a) audience, (b) format, (c) reach target, (d) timeline. Front-load this plan in §II or §III for reviewer visibility."
    - "Cite prior-evidence (peer-reviewed publication, prior SARE outcome, NRCS practice trial) before describing the proposed intervention; SARE reviewers reward grounded extension, not novel speculation."
    - "Include producer-engagement letter on PRODUCER letterhead, signed by the producer, confirming partnership commitment + time + research-role responsibility. Letter on researcher-institution letterhead = downgrade signal."
    - "Treat the 'socially responsible' pillar as substantive — write ≥1 paragraph covering community, equity, farmworker conditions, cultural fit, or producer livelihoods; do NOT relegate to one-line gesture."
  scribe_must_not_do:
    - "Use 'innovative' / 'cutting-edge' / 'revolutionary' without naming the concrete operational difference."
    - "Frame producer as 'subject' / 'data source' / 'site' / 'participant' — these signal extractive research, not partnership."
    - "Leave outreach plan as 'we will share findings' or 'results will be published' — that's a Red Team probe target."
    - "Cite blog posts / vendor materials / trade press as evidence for proposed practice effectiveness."
    - "Submit budget with university indirect costs at non-NIFA-capped rate without prior negotiation documented."
  section_ordering_notes: |
    Recommended ordering (verify against FY26 RFA explicit section order):
    §I Project Summary + three-pillar sustainability framing (lead with SARE
    definition verbatim) → §II Producer-Researcher Partnership (named
    co-investigators + roles + producer letterhead letter referenced) →
    §III Outreach Plan (channels + audiences + reach targets) → §IV Research
    Design (methodology + prior evidence + measurement) → §V Budget +
    justification → §VI Qualifications. This ordering signals partnership
    integrity early; standard research-grant ordering (research design first)
    underweights the Partnership signal.

judge_implications:
  scoring_dimensions_to_weight_harder:
    - "Sustainability of Agriculture (criterion #1) — weight ≥25% (verify FY26); three-pillar coverage is the differentiator"
    - "Producer-Researcher Partnership (criterion-specific to Partnership track) — weight ≥20% (verify FY26); producer-as-co-investigator is the differentiator"
    - "Outreach + Education (criterion ~#4) — weight ≥15% (verify FY26); multi-channel + measurable reach is the differentiator"
  evidence_required_before_high_score:
    - "Sustainability criterion ≥4 (out of 5): three-pillar coverage with ≥1 substantive paragraph per pillar AND SARE-canonical definition cited verbatim"
    - "Partnership criterion ≥4: producer named as co-investigator on title page AND producer-letterhead letter confirming research-role commitment"
    - "Outreach criterion ≥4: ≥3 dissemination channels named AND reach target per channel AND timeline"
    - "Scientific Merit criterion ≥4: prior-evidence cite for proposed practice with effect size for proposed agroecosystem"

red_team_probe_seeds:
  - probe: "How many DISTINCT dissemination channels does the outreach plan name, with measurable reach targets per channel?"
    why_it_matters: "SARE-NE Outreach criterion downgrades single-channel plans by ≥40% of criterion points. Multi-channel is a load-bearing scoring differentiator."
  - probe: "Is the producer named as co-investigator with a defined research role, OR as 'collaborator' / 'subject' / 'data source' / 'farm site'?"
    why_it_matters: "Producer-as-collaborator signals extractive research framing. SARE Partnership rubric punishes this specifically; the rubric's 'Partnership' criterion is about partnership integrity, not just presence of a producer."
  - probe: "Does the three-pillar sustainability narrative substantively cover all three pillars (economically viable + environmentally sound + socially responsible), or treat one as an afterthought?"
    why_it_matters: "Socially-responsible pillar is the most commonly neglected. -3 to -5 points on Sustainability criterion when treated as afterthought."
  - probe: "Does the proposal include human-subject research signals (producer interviews, surveys, focus groups, social-science data collection)? If yes, is the IRB protocol number cited?"
    why_it_matters: "F-SARE-NE-IRB-MISSING is a HIGH-severity Logician gate. Missing IRB when human-subject signals are present = administrative-rejection vector at NIFA."
  - probe: "Is prior evidence (peer-reviewed publication / prior SARE outcome / NRCS practice trial) cited for the proposed practice in the proposed agroecosystem? Or is the proposal claiming a novel intervention without grounded extension?"
    why_it_matters: "SARE rewards grounded extension over novel speculation. Scientific Merit criterion is rarely scored high when novelty is unbacked by adjacent prior evidence."
  - probe: "Is the budget within the Partnership cap (NEEDED — verify FY26 cap; historical $30K-$50K)? Do university indirect costs respect the NIFA cap (NEEDED — verify FY26 rate; historical 30%)?"
    why_it_matters: "Budget rejection at administrative review is a known FY24-FY25 failure mode."

logician_gate_candidates:
  - gate: F-SARE-NE-PARTNERSHIP-NO-PRODUCER
    gate_type: hard_eligibility_gate
    failure_condition: "KFR.applicant.team_members does not contain any entry with role=='producer' AND verified_producer_status==true"
    severity: P0
    fail_action: REJECT_NO_DRAFT
    source_required: true
    corpus_ref: pending_pillar_2  # SARE-NE Partnership RFA — producer co-investigator requirement
    confidence:
      level: medium
      reason: "Partnership-form-violation is canonical-reference-doc anchored (FID_CANONICAL_REFERENCE §SARE NE — Partnership eligibility); pinpoint RFA citation pending"
      promotion_requirement: "SARE-NE Partnership FY26 RFA verbatim eligibility text ingested at Pillar-2"
  - gate: F-SARE-NE-PARTNERSHIP-NO-RESEARCHER
    gate_type: hard_eligibility_gate
    failure_condition: "KFR.applicant.team_members does not contain any entry with role in {researcher, extension, NGO} AND institutional_affiliation_documented==true"
    severity: P0
    fail_action: REJECT_NO_DRAFT
    source_required: true
    corpus_ref: pending_pillar_2  # SARE-NE Partnership RFA — researcher/extension/NGO partner requirement
    confidence:
      level: medium
      reason: "Researcher-pair requirement is canonical-reference-doc anchored; pinpoint RFA citation pending"
      promotion_requirement: "SARE-NE Partnership FY26 RFA verbatim eligibility text ingested at Pillar-2"
  - gate: F-SARE-NE-OUTREACH-PLAN-MISSING
    gate_type: competitive_scoring_signal
    failure_condition: "draft.outreach_plan is None OR len(draft.outreach_plan.channels) == 0"
    severity: HIGH
    fail_action: WARN_OPERATOR
    source_required: true
    corpus_ref: pending_pillar_2  # SARE-NE Outreach criterion in scoring rubric
    confidence:
      level: medium
      reason: "Outreach-plan-missing as load-bearing scoring vector is canonical-reference-doc anchored (§SARE NE Evaluation Criteria 'outreach plan'); pinpoint weight pending"
      promotion_requirement: "SARE-NE FY26 scoring rubric ingested at Pillar-2"
  - gate: F-SARE-NE-OUTREACH-SINGLE-CHANNEL
    gate_type: competitive_scoring_signal
    failure_condition: "draft.outreach_plan is not None AND len(draft.outreach_plan.channels) < 3"
    severity: MED
    fail_action: WARN_OPERATOR
    source_required: false
    corpus_ref: pending_pillar_2  # SARE-NE reviewer pattern — multi-channel preference
    confidence:
      level: low
      reason: "pre_corpus_hypothesis — multi-channel preference is operator-derived reviewer-behavior heuristic; exact channel-count threshold pending"
      promotion_requirement: "SARE-NE Outreach-criterion scoring band documentation ingested at Pillar-2"
  - gate: F-SARE-NE-IRB-MISSING
    gate_type: competitive_scoring_signal
    failure_condition: "draft.has_human_subjects_signals() == True AND KFR.applicant.irb_protocol_id is None"
    severity: HIGH
    fail_action: WARN_OPERATOR
    source_required: true
    corpus_ref: pending_pillar_2  # 45 CFR 46 Common Rule + NIFA-RCR guidance (inherits USDA-NIFA funder gate)
    confidence:
      level: low
      reason: "pre_corpus_hypothesis — inherits USDA-NIFA funder F-USDA-NIFA-IRB-MISSING shape"
      promotion_requirement: "USDA-NIFA funder gate Pillar-2 promotion propagates to this program-level gate"
    pass_1_reconciliation_note: "Inherits USDA-NIFA funder gate F-USDA-NIFA-IRB-MISSING. Pass 6 (inheritance) should consider whether this program-level gate is redundant with funder-level inheritance or genuinely program-specific."
  - gate: F-SARE-NE-PRODUCER-AS-COLLABORATOR
    gate_type: competitive_scoring_signal
    failure_condition: "draft.producer_role_in_narrative in {'collaborator', 'subject', 'data source', 'site', 'participant'} (NOT 'co-investigator' or 'research partner')"
    severity: MED
    fail_action: WARN_OPERATOR
    source_required: false
    corpus_ref: pending_pillar_2  # SARE-NE Partnership-criterion reviewer-behavior pattern
    confidence:
      level: low
      reason: "pre_corpus_hypothesis — producer-as-collaborator detection is operator-derived reviewer-behavior heuristic"
      promotion_requirement: "SARE-NE Partnership-criterion scoring rubric ingested at Pillar-2"
    pass_1_reconciliation_note: "Purpose-wise this is drafting heuristic (Scribe register guidance — vocabulary detection); classified as competitive_scoring_signal per (MED, WARN_OPERATOR) tuple. Pass 3 may migrate to drafting_warning."
  - gate: F-SARE-NE-BUDGET-OVER-CAP
    gate_type: hard_eligibility_gate
    failure_condition: "draft.budget_total > program.match_requirements.cap_partnership_track_fy26 (NEEDED Pillar 2)"
    severity: P0
    fail_action: REJECT_NO_DRAFT
    source_required: true
    corpus_ref: pending_pillar_2  # SARE-NE Partnership track cap (canonical reference: $30K-$50K historical)
    confidence:
      level: low
      reason: "pre_corpus_hypothesis — historical cap $30K-$50K per canonical reference §SARE NE Grant Types; exact FY26 cap pending"
      promotion_requirement: "SARE-NE Partnership FY26 RFA dollar-cap text ingested at Pillar-2"
  - gate: F-SARE-NE-INDIRECT-COST-EXCEEDS-NIFA-CAP
    gate_type: competitive_scoring_signal
    failure_condition: "draft.budget_indirect_cost_rate > 0.30 (NEEDED — verify FY26 NIFA cap)"
    severity: HIGH
    fail_action: WARN_OPERATOR
    source_required: true
    corpus_ref: pending_pillar_2  # NIFA indirect-cost-cap guidance current FY26
    confidence:
      level: low
      reason: "pre_corpus_hypothesis — 30% historical NIFA cap; FY26 exact rate pending verification"
      promotion_requirement: "NIFA indirect-cost-cap guidance current FY26 ingested at Pillar-2"

source_backing:
  corpus_refs:
    - "<NEEDED — Pillar 2: USDA-NIFA-SARE-NE-FY26:partnership_rfa_fy26.pdf — primary NOFO>"
    - "<NEEDED — Pillar 2: SARE national framework — three-pillar sustainability definition verbatim>"
    - "<NEEDED — Pillar 2: SARE-NE FY24 + FY25 Partnership-track award rosters from SARE outcome database>"
    - "<NEEDED — Pillar 2: SARE peer-review-panel composition guidance + COI rules>"
    - "<NEEDED — Pillar 2: NIFA indirect-cost-cap guidance (current FY26)>"
  confidence: |
    LOW pre-corpus. All track-specific dollar caps, rubric weights, screening
    norms, indirect-cost caps, and known-failure-modes are operator-asserted
    + general-knowledge-grounded; Pillar-2 must promote each via verbatim
    NOFO cite + ≤2-sentence quote. Logician F-FID-FACT-ORPHAN fails any
    fact lacking corpus_ref at Pillar-3 L-005.
  unresolved_questions:
    - "Exact FY26 Partnership-track dollar cap (range expected $30K-$50K but verify)"
    - "Exact FY26 rubric criterion weights (verify Sustainability + Partnership + Outreach percentages)"
    - "FY26 indirect-cost cap (NIFA-wide vs SARE-specific)"
    - "Whether FY26 cycle has a screen → score → consensus three-stage structure OR single-pass merit review (per D3 review-stage enum question deferred to reviewer-types Universe LOCK)"
    - "Whether SARE-NE FY26 Partnership reviewer panel composition has changed vs FY24-FY25"
```

---

## §1 — What "depth" means for THIS artifact

Depth here is the **decision substrate**, not a description: the eligibility predicates Logician evaluates pre-Scribe; the rubric weights Judge applies instead of generic 12-dimension scoring; the section-ordering + drafting decisions Scribe makes that differ from a generic research-grant prompt; the probes Red Team runs that differ from generic adversarial framing; the live-check URL Scout VERIFY hits. The §B yaml above IS the depth — every field in `runtime_consumers`, `eligibility_gates`, `scoring_rubric`, `drafting_implications`, `judge_implications`, `red_team_probe_seeds`, and `logician_gate_candidates` changes a specific runtime decision.

The Codex quality test: *"Same Scribe prompt with/without the artifact should produce visibly different drafts."* For SARE-NE Partnership specifically:

- **Without artifact** — Scribe writes a generic on-farm research proposal: PI + farm site, "innovative" sustainable practices, "we will share findings", standard research-grant section ordering. Judge scores generic 12-dimension. Red Team probes generic adversarial. Logician applies generic federal-grant eligibility (SAM.gov active, UEI present).
- **With artifact** — Scribe leads with SARE's verbatim three-pillar definition, names producer as co-investigator on title page with defined research role, structures outreach plan with ≥3 dissemination channels + reach targets, cites prior SARE-outcome / NRCS-practice-trial evidence before proposed intervention, treats socially-responsible pillar substantively (community + equity + farmworker + cultural). Judge applies 5-criterion SARE rubric with Sustainability ≥25% + Partnership ≥20% + Outreach ≥15%, with tie-breakers favoring three-pillar + co-investigator + multi-channel drafts. Red Team probes outreach-channel count, producer-engagement authenticity, three-pillar coverage gap, IRB-when-human-subjects, prior-evidence-cited-before-novelty. Logician fails closed on `F-SARE-NE-PARTNERSHIP-NO-PRODUCER` / `F-SARE-NE-PARTNERSHIP-NO-RESEARCHER` / `F-SARE-NE-OUTREACH-PLAN-MISSING` / `F-SARE-NE-IRB-MISSING` / `F-SARE-NE-BUDGET-OVER-CAP` etc.

The deltas are visible, mechanical, and traceable to specific artifact fields.

---

## §2 — Primary sources in scope

| Corpus category | Specific sources | Access path | Estimated count |
|-----------------|------------------|-------------|-----------------|
| `nofos/` | SARE-NE Partnership Grant FY26 RFA PDF; SARE-NE national framework cross-reference | Public SARE-NE site (UVM host) + national SARE | 2-3 |
| `rubrics/` | SARE-NE Partnership FY26 scoring rubric (RFA appendix or SARE-NE publication) | RFA appendix / SARE-NE | 1-2 |
| `awards/` | FY24 + FY25 SARE-NE Partnership-track award rosters; NE-region project database extracts | Public SARE outcome database + USAspending.gov | 2-3 |
| `interviews/` | 0-2 SARE-NE regional-coordinator conversations (Tier-2/3); 1-2 prior-Partnership-grantee debrief | Operator network outreach | 0-3 |
| `guidance/` | SARE national three-pillar sustainability definition (verbatim source for Scribe drafting cue); SARE peer-review panel composition + COI rules; NIFA indirect-cost-cap guidance | SARE + NIFA public guidance | 3-4 |
| `endpoints/` | SARE-NE Partnership program page; Grants.gov synopsis URL (if separately listed); national SARE outcome database; `live_check_url` for Scout VERIFY | SARE-NE + Grants.gov | 3-5 URLs |

Case law OUT OF SCOPE.

---

## §3 — Tier classification

| Field | Tier |
|-------|:----:|
| Default for facts in this artifact | `1` |
| `scoring_rubric.criteria[].weight_pct` | `1` |
| `eligibility_gates[]` | `1` |
| `reviewer_relationship_notes[]` (if any) | `3` |
| `red_team_probe_seeds[]` | `2` (operator-derived synthesis) |
| `language_register.suspicious_terms[]` | `2` (operator-derived) |
| `endpoints[]` | `1` |

---

## §4 — Refresh cadence

`per_cycle`. SARE-NE Partnership is annually-cycled. `F-FID-STALE-RUBRIC` fires if rubric > 18 months old.

---

## §5 — Calibration applicant pair

`food_systems` (CIC-01) × `operating_capacity` (CLC-03), with Research & Evidence (CLC-04) as primary CLC for this program. Pillar 4 calibration DORMANT roster-wide.

---

## §6 — Done definition

`audited` when Pillar-3 single-cycle L-005 audit passes: every yaml field in §B carries `corpus_ref` + ≤2-sentence verbatim quote at Pillar 3; `runtime_consumers` block traces each `decision_changed` to a specific field that L-005 reviewers can verify; `strength_test` answers in §A.3 cross-reference §1 prose + §B yaml; "same Scribe prompt with/without the artifact" diff captured as an inline test note (PR body for v0; methodology v1.0 doc at week 5 close).

**Methodology-anchor role:** this artifact's Pillar-3 extraction is the source of methodology v1.0 doc at week 5. Lessons learned feed `pipeline/funder_intelligence/_methodology/methodology_v1.0.md`.

**Quality-bar role:** once operator approves this depth-charter, the other 12 charters are re-authored as `[PRE-DEPTH-CHARTER]` placeholders pending full re-author at this quality bar.

---

## §7 — Operator signature

```yaml
charter_signed_at: <pending_operator_attestation>
charter_signed_by_pubkey: <pending_operator_attestation>
charter_signed_canonical_bytes_sha3_512: <pending_operator_attestation>
charter_ed25519_signature: <pending_operator_attestation>
```

Manual ceremony per `pillar_1_charters/README.md` §"Validity discipline" + §"Format discipline". Helper script `sign_charter.py` is a follow-up engineering task (Codex-audit P1).

---

## §8 — Out of scope (anti-drift)

- Other SARE-NE tracks (Farmer/Rancher, Research & Education, Sustainable Communities, Professional Development) — parallel artifacts at scale-out
- Other SARE regions (Southern, North Central, Western) — separate artifacts
- USDA-NIFA funder-level facts (lives in `funders/USDA-NIFA.yaml`)
- AFRI or other NIFA programs
- SARE-NE Partnership cycles prior to FY26 (FY24 + FY25 only as historical-pattern reference)
- Compliance framework internals (lives in `compliance_cascades/`)
- Per-reviewer-type heuristics (lives in `reviewer_heuristics/peer-reviewer-academic.yaml` + farmer-reviewer overlay)
- Per-applicant research design / IRB protocol / partnership-org-specific detail (lives in `orgs/<slug>/`)
- Case law interpretation
- Drafting actual SARE-NE Partnership applications
