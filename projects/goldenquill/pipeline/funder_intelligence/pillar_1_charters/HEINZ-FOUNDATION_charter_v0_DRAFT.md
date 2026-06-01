# Depth Charter — `HEINZ-FOUNDATION` (funder behavior profile)

> **Pillar 1 of 4** per `pipeline/planning/funder_intelligence_database_research_project_2026-05-16.md` §3.1.
> **Quality bar** per `docs/FID_ARTIFACT_OPTIMIZATION_PRINCIPLES_2026-05-18.md` §1 + §2 + Codex framing.
> **Status: DEPTH CHARTER v0 (pre-corpus hypothesis; do not load as signed logic) — [FIDELITY-FIX-HEINZ] applied 2026-05-18** — re-authored to Codex yaml shape per operator directive 2026-05-18, then patched against Heinz GPR 2024 + Heinz public grants page after operator caught P0 geo-scope fidelity break.
>
> **[CONJECTURE — Pillar-2 corpus pending]** Most Heinz-Endowments-specific funder-fact claims remain operator-asserted; Pillar-2 corpus assembly (Heinz strategic + strategy-area position papers + 990-PF FY22-FY24 + program-officer interviews) promotes each. `F-FID-FACT-ORPHAN` enforces.
>
> **[FACT — corpus-backed at this revision]** Geographic scope (SWPA 10 counties + PA-Commonwealth eligibility envelope), seven-strategy taxonomy, application logistics (Blackbaud portal / rolling LOI / 45-day response / 60-90 day decision), 501(c)(3) + 509(a) + federally-tax-exempt government entity eligibility, individuals-and-for-profits-not-eligible, median grant size ($100K 2024), average grant length (1.7 years), annual grantmaking volume (~$90M), and DEI portfolio pattern (>2/3 grantees serve at least one historically disadvantaged group) are now backed by the Heinz GPR 2024 Key Findings Memo + Heinz public grants page (see `source_backing.corpus_refs`).

---

## Header

| Field | Value |
|------:|:------|
| `artifact_id` | `HEINZ-FOUNDATION` |
| `artifact_family` | `funder` |
| `version` | `depth_charter_v0` |
| `lifecycle` | `draft` |
| `phase` | `1 — exemplar pair` |

---

## §A — Adversarial pre-checks

```yaml
runtime_consumer:
  scout:
    reads_fields: [behavior_mechanisms, geographic_eligibility, strategic_areas]
    stage: DISCOVER
    decision_changed: "Scout DISCOVER applies weighted-fit shaped by the three GPR-derived behavior_mechanisms. M1 (regional_legitimacy_capital): prioritize projects where Heinz participation could unlock other funders, public partners, or civic legitimacy. M2 (transition_sensitive_relationship_clarity): flag applicants with documented Heinz contact, prior funding, peer-grantee introduction, or clear current-strategy fit. M3 (capacity_partnership_beyond_grant): prioritize projects that can credibly absorb thought partnership, convening, collaboration, or funder-alignment support. Geographic fit is a WEIGHTED dimension: SWPA-10-county = HIGH; PA-Commonwealth-serving-SWPA = MEDIUM; outside-PA = LOW-but-not-universal-fail at the funder layer (GPR respondent geography includes outside-PA respondents; program-specific Heinz initiatives may layer additional geo gates that DO fail closed)."
  scribe:
    reads_fields: [behavior_mechanisms, funder_dialect, language_register, drafting_implications]
    stage: scaffold
    decision_changed: "Scribe wires to all three behavior_mechanisms. M1: frame the request as a regional alignment opportunity, not merely an organizational need. M2: make strategic-fit logic explicit; never assume Heinz already understands why this work matters (Heinz is in active strategy refresh; program staff carry 53 active grants + 50 apps per staffer per GPR 2024 p.5 — they do not have spare attention to reconstruct context). M3: include a partnership-use paragraph naming how Heinz can help beyond dollars (thought partnership, convening, introductions to other funders, multi-year support) without making unrealistic demands. Foundation-program-officer register applies; theory-of-change framing is the dominant section-I shape; SWPA sub-geography (Pittsburgh neighborhoods AND non-Pittsburgh SWPA counties — Mon Valley, Beaver County, Westmoreland, etc.) named precisely."
  judge:
    reads_fields: [behavior_mechanisms, judge_implications]
    stage: cross_check
    decision_changed: "Judge rewards (M1) evidence the project sits inside a larger Pittsburgh civic / SWPA-ecosystem movement, (M2) proposals that help the program officer understand applicant context, community context, and strategy fit without over-explaining, and (M3) proposals with multi-year logic, collaboration pathways, and clear capacity outcomes. Foundation-program-officer register rewards remain (theory-of-change coherence, outcomes articulation, relational-trust signals). Does NOT downgrade non-Pittsburgh-proper SWPA-county applicants (Beaver / Greene / Indiana / Fayette / Armstrong / Lawrence / Butler / Washington / Westmoreland are equally in-scope per Heinz public grants page). The 'outcomes-vs-outputs is the #1 downgrade vector' framing is a general foundation-program-officer heuristic, NOT a Heinz-specific finding — GPR 2024 surfaces declining communication / understanding ratings, not an outputs-conflation downgrade signal — Judge weights it as a general-heuristic priority, not as Heinz-specific load-bearing."
  red_team:
    reads_fields: [behavior_mechanisms, red_team_probe_seeds]
    stage: probe_target_selection
    decision_changed: "Red Team probes per mechanism: M1 — is the applicant asking Heinz for money only or positioning Heinz as a catalytic regional partner? M2 — does the proposal depend on old Heinz priorities, unclear strategic fit, or stale relationship assumptions? M3 — is the applicant asking for a short-term check to solve a long-term capacity problem? Plus general-foundation heuristics: outcomes-vs-outputs distinction (general foundation register, not Heinz-specific), theory-of-change linearity, geographic-fit weighting (PA-Commonwealth-serving-SWPA is favored but not required at the funder layer), unsupported-innovation language (innovation framing IS rewarded when backed by track record per GPR p.2 — empty innovation language is the failure mode, NOT innovation itself)."
  logician:
    reads_fields: [eligibility_gates, logician_gate_candidates]
    stage: PRE
    decision_changed: "Logician fires Heinz funder-wide PRE-gates: F-HEINZ-ELIGIBLE-ENTITY-MISSING (P0; applicant is not 501(c)(3)+509(a) public charity AND not federally tax-exempt government entity AND no fiscal sponsor), F-HEINZ-INDIVIDUAL-OR-FORPROFIT (P0; individuals and for-profit organizations are not eligible per Heinz grants page), F-HEINZ-OUTSIDE-PA-WARNING (MED; primary service area entirely outside the Commonwealth of Pennsylvania — warn-not-fail at the funder layer per GPR respondent-geography evidence; program-specific Heinz initiatives may upgrade this to P0), F-HEINZ-COLD-OUTREACH-WARNING (MED; advisory with structured recommended-operator-actions, NOT a universal hard-fail), F-HEINZ-LEGACY-TAXONOMY-LEAK (LOW; draft uses legacy 4-area taxonomy)."
```

```yaml
artifact_must_not_contain:
  - facts belonging to another artifact
  - applicant-specific claims                              # no named applicant
  - uncited generalizations
  - compliance framework internals
  - reviewer-type heuristics                               # → reviewer_heuristics/foundation-program-officer.yaml
  - other SWPA-region foundations                          # Hillman, Pittsburgh Foundation, McCune, RK Mellon = separate
  - case law interpretation
```

```yaml
strength_test:
  - "Name one concrete drafting decision this artifact changes."
  - "Name one proposal this artifact would reject or downgrade."
  - "Name one Red Team probe this artifact enables."
```

**Answers (PASSED):**

1. **Drafting decision.** Scribe wires §I to behavior_mechanism M1 (regional_legitimacy_capital): frames the request as a regional alignment opportunity, not merely an organizational need — *"This project advances [named SWPA civic / ecosystem movement] and positions Heinz as a catalytic regional partner in [specific alignment opportunity]."* + behavior_mechanism M2 (transition_sensitive_relationship_clarity): makes strategic-fit logic explicit — *"Under Heinz's [current 7-strategy] framing, this work sits inside [named strategy] because [mechanism]."* + behavior_mechanism M3 (capacity_partnership_beyond_grant): includes a partnership-use paragraph in §V — *"Beyond grant dollars, the most useful Heinz partnership would be [convening / introductions / thought partnership / multi-year continuity]."* Theory-of-change framing remains the §I shape inside this register.
2. **Proposal rejected.** Logician `F-HEINZ-ELIGIBLE-ENTITY-MISSING` (P0) fails closed any applicant that is not a 501(c)(3)+509(a) public charity, not a federally-tax-exempt government entity, and has no fiscal sponsor. `F-HEINZ-INDIVIDUAL-OR-FORPROFIT` (P0) fails closed any individual or for-profit applicant. **Geographic fit at the Heinz funder layer is WEIGHTED, not universal-fail.** GPR 2024 respondent geography includes outside-Allegheny and outside-Pennsylvania respondents, so a universal P0 gate on geography would over-restrict against the corpus evidence. `F-HEINZ-OUTSIDE-PA-WARNING` (MED) advises rather than rejects at the funder layer. Program-specific Heinz initiatives (e.g., a specific Workforce or Food-Systems RFP that explicitly limits geography to the SWPA 10-county region) may layer additional P0 geo gates — those live in the per-program charter, not the funder charter.
3. **Red Team probe.** Per-mechanism probes: M1 — *"Is the applicant asking Heinz for money only, or positioning Heinz as a catalytic regional partner?"* M2 — *"Does the proposal depend on old Heinz priorities (legacy 4-area taxonomy) or stale relationship assumptions, or does it engage Heinz's current 7-strategy framing and current program-staff capacity?"* M3 — *"Is the applicant asking for a short-term check (1-year ask in a context that needs 3+ years of capacity work) to solve a long-term capacity problem?"* General-foundation heuristics also probed but flagged as general (not Heinz-specific): outcomes-vs-outputs distinction, unsupported-innovation claims, theory-of-change linearity.

---

## §B — Codex-shape depth-charter YAML

```yaml
artifact_id: HEINZ-FOUNDATION
artifact_family: funder
version: depth_charter_v0
lifecycle: draft
validation_status: pre_corpus_hypothesis
runtime_load_status: do_not_load_as_signed_logic
operator_label: depth_charter_v0

one_sentence_job: |
  Equip every Heinz Endowments-targeted draft with foundation-program-officer
  register, theory-of-change framing, southwestern-Pennsylvania (10-county SWPA
  + PA-Commonwealth-serving-SWPA) geographic discipline, outcomes-vs-outputs
  distinction, and prior-relationship integrity.

runtime_consumers:
  # All four AI seats wire to the three GPR-derived behavior_mechanisms
  # (regional_legitimacy_capital + transition_sensitive_relationship_clarity
  # + capacity_partnership_beyond_grant). Geographic / eligibility shaping
  # is weighted-fit, not universal hard-fail — see logician section + §F
  # below.
  scout:
    pre_filter_question: |
      Is this opportunity Heinz-Endowments-shaped (eligible-entity-type +
      SWPA-geographic-weighted-fit + GPR-mechanism alignment) BEFORE Scribe
      is invoked?
    eligibility_dimensions:
      - entity_type_eligibility       # 501(c)(3)+509(a) public charity OR federally-tax-exempt government OR fiscal-sponsored
      - geographic_weighted_fit       # SWPA-10-county HIGH; PA-Commonwealth-serving-SWPA MEDIUM; out-of-PA NOT universal-fail
      - relationship_mechanism_signal # GPR-derived mechanism-1/2/3 (regional_legitimacy / transition_relationship / capacity_partnership)
    hard_gate_refs:
      - F-HEINZ-ELIGIBLE-ENTITY-MISSING
      - F-HEINZ-INDIVIDUAL-OR-FORPROFIT
    cross_funder_signal: |
      Foundation-class funder; routes opportunity TOWARD other Pittsburgh
      foundation cohort (Hillman, McCune, Pittsburgh Foundation, RK Mellon)
      for peer-funder comparison. Flags applicants with only-federal-track-
      record as potentially-wrong-funder-match.
    operator_assist_required: |
      Escalate to operator when: (a) primary service area entirely outside
      Commonwealth of PA (F-HEINZ-OUTSIDE-PA-WARNING MED), (b) no documented
      Heinz contact / prior funding / peer-grantee introduction (F-HEINZ-
      COLD-OUTREACH-WARNING MED), (c) entity-eligibility chain involves
      fiscal-sponsor branch (sponsor identity + agreement need verification).
    source_authority: |
      Heinz GPR 2024 (canonical reference §Heinz GPR mechanisms) + Heinz
      public Grants page (anchored in [FIDELITY-FIX-HEINZ] commit). Geographic
      weighted-fit dimension source-backed; mechanism signals source-backed.
    prose_summary: |
      DISCOVER applies weighted fit on (a) GPR-mechanism-1: regional
      legitimacy potential (HIGH for projects that could unlock other SWPA
      funders / public partners / civic legitimacy), (b) GPR-mechanism-2:
      documented Heinz contact / prior funding / peer-grantee introduction /
      clear current-strategy fit, and (c) GPR-mechanism-3: project's capacity
      to absorb thought partnership / convening / multi-year support. Geography
      is a WEIGHTED dimension (SWPA-10-county = HIGH; PA-Commonwealth-serving-
      SWPA = MEDIUM; outside-PA respondents appear in GPR data, so
      out-of-PA does NOT universal-fail at the funder layer — program-specific
      Heinz initiatives may layer additional geo gates).
  scribe:
    voice_change: |
      Foundation-program-officer register; theory-of-change framing dominates
      §I; all three GPR-derived behavior_mechanisms (M1 regional_legitimacy_
      capital + M2 transition_sensitive_relationship_clarity + M3 capacity_
      partnership_beyond_grant) wired explicitly into section content.
    section_ordering:
      - "§I theory of change + 3-year operational picture + [M1] regional alignment language + [M2] named Heinz strategy"
      - "§II outcomes + measurement plan (distinct from outputs)"
      - "§III sustained-change / transition plan + [M1] regional alignment thread"
      - "§IV budget"
      - "§V qualifications + prior-relationship references + [M3] partnership-use paragraph"
      - "§VI work plan"
    must_do:
      - "[M1] Frame the request as a regional alignment opportunity, not merely an organizational need. Name the larger Pittsburgh civic / SWPA-ecosystem movement the project sits inside. Name other funders / public partners Heinz could align with."
      - "[M2] Make strategic-fit logic explicit. Map the project to one (or more) of the seven canonical strategic areas: Arts & Culture; Civic Participation; Climate, Environment & Health; Community & Economic Development; Food Systems; Veterans; Workforce. Surface any context that Heinz program officers might NOT already have."
      - "[M3] Include a partnership-use paragraph in §V (or as a sidebar): name how Heinz can help beyond dollars — thought partnership, convening, introductions to other funders, multi-year continuity — without making unrealistic demands."
      - "[M3] If the work is multi-year capacity-building, explicitly articulate the request horizon vs the work horizon. If asking for a single-year cycle on multi-year work, name the transition plan."
      - "Lead §I with theory-of-change framing (intervention → mechanism → outcome over time + 3-year operational picture). Foundation-program-officer register."
      - "Reference named Heinz program officer + prior site visit if applicable."
      - "Frame SWPA scope with sub-geography specificity — name the actual county (Allegheny / Armstrong / Beaver / Butler / Fayette / Greene / Indiana / Lawrence / Washington / Westmoreland) and, where applicable, the named Pittsburgh neighborhood (downtown / North Side / East End / Hazelwood / Mon Valley)."
      - "If applicant is PA-Commonwealth-but-outside-SWPA or fully outside-PA, explicitly articulate how the proposed work serves SWPA-region or PA-state residents (funder-layer enforcement is advisory not P0)."
      - "Include sustained-change / transition-plan in §III."
      - "Calibrate request size against Heinz's median grant of ~$100K (2024 GPR). Ambitious larger asks are not blocked but need stronger sustained-change framing."
    must_not_do:
      - "Lead with problem statement (federal style); start with theory of change."
      - "Frame the ask as money-only — Heinz's value is also legitimacy + partnership + multi-year continuity ([M1] + [M3] both penalize)."
      - "Assume Heinz already understands why this work matters or who the applicant is — Heinz is in active strategy refresh + program-staff capacity stretch ([M2] explicit signal)."
      - "Pitch a single-year check for a multi-year capacity problem without naming the mismatch ([M3] explicit signal)."
      - "Use 'innovative' / 'cutting-edge' / 'novel' framing without a backing track record, named mechanism, or evidence — empty innovation language is suspicious; backed innovation is rewarded (GPR p.2)."
      - "Treat outcomes-vs-outputs distinction as Heinz's #1 scoring vector — it's a general foundation heuristic, not a Heinz-specific load-bearing finding per GPR 2024."
      - "Generic 'greater Pittsburgh area' framing without naming the actual SWPA county or neighborhood."
      - "Default to Allegheny-County-only scoping when the project actually serves multiple SWPA counties."
      - "Use the legacy 4-area taxonomy (Sustainability / Creativity / Learning / Community & Economic Development) — Heinz refreshed to a 7-strategy taxonomy."
      - "Cold-outreach without first attempting program-officer conversation or peer-grantee introduction (advisory not impermissible; program staff carry 53 active grants + 50 apps per the 2024 GPR — cold proposals compete for thin attention)."
    cross_funder_signal: |
      Heinz Scribe register is FOUNDATION-class — distinct from federal
      (USDA-RD / USDA-NIFA / USDA-AMS) and state-program (PA-DEPT-AG /
      PA-DCED) registers. Within the SWPA Pittsburgh-foundation cohort
      (Heinz ↔ RK Mellon ↔ Hillman ↔ McCune ↔ Pittsburgh Foundation),
      Heinz uniquely wires to the three GPR-derived behavior_mechanisms;
      RK Mellon's register prioritizes scale-and-permanence over Heinz's
      M1/M2/M3 stack.
    source_authority: |
      Heinz GPR 2024 Key Findings Memo (canonical reference §Heinz GPR
      mechanisms) + Heinz public grants page + Heinz strategies page
      (anchored in [FIDELITY-FIX-HEINZ] commit). The three-mechanism
      wiring (M1/M2/M3) is source-backed. Foundation-program-officer
      register is operator-derived heuristic; cross-foundation Pillar-2
      ingest pending.
    prose_summary: |
      Wires to all three mechanisms. Mechanism-1: frames the ask as a regional
      alignment opportunity (not merely an organizational need). Mechanism-2:
      makes strategic-fit logic explicit; never assumes Heinz remembers why
      this work matters. Mechanism-3: includes a partnership-use paragraph
      naming how Heinz can help beyond dollars without making unrealistic
      demands. Foundation-program-officer register with named SWPA sub-
      geography.
  judge: |
    Rewards (1) evidence the project sits inside a larger Pittsburgh civic /
    SWPA-ecosystem movement, (2) proposals that help the program officer
    understand applicant + community context + strategy fit without over-
    explaining, (3) multi-year logic + collaboration pathways + clear
    capacity outcomes. Does NOT downgrade non-Pittsburgh-proper SWPA-county
    applicants.
  red_team: |
    Probes per mechanism: M1 — is the applicant asking Heinz for money only
    or positioning Heinz as a catalytic regional partner? M2 — does the
    proposal depend on old Heinz priorities / unclear strategic fit / stale
    relationship assumptions? M3 — is the applicant asking for a short-term
    check to solve a long-term capacity problem? Also probes general-
    foundation heuristics (outcomes-vs-outputs distinction; unsupported
    innovation claims — see §judge_implications + language_register).
  logician: |
    PRE-gates: F-HEINZ-ELIGIBLE-ENTITY-MISSING (P0; entity is not 501(c)(3)
    +509(a) public charity AND not federally-tax-exempt government entity
    AND no fiscal sponsor), F-HEINZ-INDIVIDUAL-OR-FORPROFIT (P0; entity is
    individual or for-profit without fiscal sponsor), F-HEINZ-OUTSIDE-PA-
    WARNING (MED; primary service area entirely outside the Commonwealth of
    Pennsylvania — warn-not-fail at the funder layer per GPR respondent-
    geography evidence; program-specific Heinz gates may upgrade to P0),
    F-HEINZ-COLD-OUTREACH-WARNING (MED; advisory with recommended operator
    actions, NOT universal hard-fail), F-HEINZ-LEGACY-TAXONOMY-LEAK (LOW;
    draft uses legacy 4-area taxonomy).

behavior_mechanisms:
  # Three distinct funder-behavior mechanisms parsed from the 2024 GPR
  # (operator + collaborator analysis 2026-05-18). These are the load-bearing
  # cause-of-decision shapes. Seat decision_changed strings + drafting /
  # judging / red-team behavior wire to these — generic "Heinz likes
  # relationships" framing is REPLACED by these three specific mechanisms.

  - id: regional_legitimacy_capital
    summary: |
      Heinz is positioned by its grantees as an indispensable regional anchor
      whose participation unlocks other funders, public partners, and civic
      legitimacy. A Heinz grant is partly a money flow and partly a regional
      signal — a yes from Heinz often catalyzes other yeses across the SWPA
      ecosystem.
    source: |
      GPR 2024 §"The Endowments as a Community Leader" (p.2) — grantees rate
      Heinz top-quarter on local-community impact, sustained over time and
      across programs; comments call Heinz "indispensable" and reference
      "critical resourcing... and amplification" of regional work. Quoted
      grantee (GPR p.2): "Heinz has a huge impact on everything that happens
      in Pittsburgh. Pittsburgh is a very foundation-oriented city... A yes
      or no from Heinz can make or break a project. Heinz is our biggest
      foundation funder, and these funds are critical to our organization
      from both budgetary and legitimacy perspectives."
    runtime_effect:
      scout: "Prioritize projects where Heinz participation could unlock other funders, public partners, or civic legitimacy."
      scribe: "Frame the request as a regional alignment opportunity, not merely an organizational need."
      judge: "Reward evidence that the project sits inside a larger Pittsburgh civic / SWPA-ecosystem movement."
      red_team: "Probe whether the applicant is asking Heinz for money only, or positioning Heinz as a catalytic regional partner."

  - id: transition_sensitive_relationship_clarity
    summary: |
      Heinz was in active staff / communications / strategy transition through
      2024-2025. Program staff load has grown (53 active grants + 50 apps per
      staffer vs 36/36 in 2019). Grantees report significantly lower clarity-
      of-communication, openness-to-grantee-ideas, candor, and staff-
      responsiveness ratings since 2019. Grantees want clearer communication,
      deeper re-engagement, and transparent change management — the funder
      cannot be assumed to remember why this work matters.
    source: |
      GPR 2024 §"Context and Overview" (p.1) — staff turnover including
      communications + program staff + leadership; strategy refresh underway.
      §"Decreases in Clarity of Communication and Depth in Grantee
      Relationships" (p.4) — "Ratings are significantly lower than in 2019
      for the clarity, transparency, and consistency of communication... and
      at the bottom of Heinz's peer funder cohort for how well grantees
      understand how their work fits into the Endowments' broader efforts."
      Program-staff-load context: GPR p.5 — "Program staff now manage 53
      active grants and 50 applications, on average, compared to 36 active
      grants and 36 applications in 2019."
    runtime_effect:
      scout: "Flag applicants with documented Heinz contact, prior funding, peer-grantee introduction, or clear fit with current strategy."
      scribe: "Make strategic-fit logic explicit; avoid assuming Heinz already understands why this work matters."
      judge: "Reward proposals that help the program officer understand applicant context, community context, and strategy fit without over-explaining."
      red_team: "Probe whether the proposal depends on old Heinz priorities, unclear strategic fit, or stale relationship assumptions."

  - id: capacity_partnership_beyond_grant
    summary: |
      Heinz's average grant length has dropped to 1.7 years — the shortest
      since the GPR was first fielded in 2005, down from 2.5 years in 2019.
      Grantees ask for longer, larger, more flexible support and explicitly
      ask Heinz to play more of a connecting / convening / thought-partnership
      role. Grantees who receive any beyond-the-grant assistance rate Heinz
      higher across understanding, interaction quality, clarity, openness,
      and transparency. Heinz wants to be a multi-year capacity partner, not
      a single-cycle check-writer — but the recent trend is the opposite, and
      grantees are aware of it.
    source: |
      GPR 2024 §"Monetary Support" (p.3) — "At an average length of 1.7
      years, Heinz's grants are the shortest they've been since this survey
      was first fielded in 2005." §"Future Opportunity – Increase Grant
      Length" (p.4) — third-most-common improvement theme. §"Assistance
      Beyond Grant Dollars" (p.3) — "About half of grantees, a lower than
      typical proportion, report receiving assistance beyond the grant...
      Grantees that receive any type of assistance beyond the grant rate
      more positively on nearly all measures." Sustainability-program 70%+
      beyond-grant rate noted on p.3.
    runtime_effect:
      scout: "Prioritize projects that can credibly absorb thought partnership, convening, collaboration, or funder-alignment support."
      scribe: "Include a partnership-use paragraph: how Heinz can help beyond dollars without making unrealistic demands."
      judge: "Reward proposals with multi-year logic, collaboration pathways, and clear capacity outcomes."
      red_team: "Probe whether the applicant is asking for a short-term check to solve a long-term capacity problem."

mission_framing:
  one_paragraph_summary: |
    The Heinz Endowments funds projects across seven strategic areas — Arts &
    Culture; Civic Participation; Climate, Environment & Health; Community &
    Economic Development; Food Systems; Veterans; Workforce — concentrating
    its efforts and resources in the southwestern Pennsylvania (SWPA) 10-
    county region (Allegheny, Armstrong, Beaver, Butler, Fayette, Greene,
    Indiana, Lawrence, Washington, Westmoreland) with a PA-Commonwealth
    eligibility envelope when a proposal is expressly for the benefit of
    SWPA-region or PA-state residents. Annual grantmaking averages ~$90M;
    median grant size in 2024 was ~$100K; average grant length 1.7 years
    (GPR 2024). Funder behavior is driven by three load-bearing mechanisms
    parsed from the GPR (see `behavior_mechanisms` above): regional
    legitimacy capital, transition-sensitive relationship clarity, and
    capacity-partnership-beyond-grant. Foundation-program-officer register
    dominates; site-visit + program-officer-check-in cadence is the post-
    award relationship infrastructure.
  corpus_ref: |
    Heinz GPR 2024 Key Findings Memo (CEP, dated 2025-03-21) — canonical PDF
    at https://www.heinz.org/UserFiles/File/THE%20Grantee%20Perception%20Report.pdf;
    Heinz public grants page at https://www.heinz.org/grants;
    Heinz strategies page at https://www.heinz.org/strategic-areas.
    Pillar 2 still owed: 990-PF FY22-FY24, per-strategy position papers, 0-2
    program-officer interviews.

stage_behavior:
  screen:
    primary_question: "Eligible-entity status (P0; 501(c)(3)+509(a) public charity OR federally-tax-exempt government entity OR fiscally sponsored) + individual-or-for-profit-without-fiscal-sponsor exclusion (P0) + behavior-mechanism fit (regional legitimacy potential + strategic-fit clarity + capacity-partnership absorption) + strategic-area alignment (one of seven) + geographic weighting (SWPA-10-county HIGH, PA-Commonwealth-serving-SWPA MEDIUM, outside-PA LOW-but-not-fail at funder layer)."
    time_budget: "Heinz public grants page: rolling LOI ~10 min to complete; 45-day acknowledgement target; 60-90 day decision after general application. Per-strategy cycle norms still <NEEDED Pillar 2>."
    pass_fail_triggers:
      - "Applicant is an individual or for-profit organization AND has no fiscal sponsor → FAIL (P0; Heinz public grants page: 'Individuals and for-profit organizations are not eligible for funding')"
      - "Applicant is non-501(c)(3)+509(a) public charity AND not a federally-tax-exempt government entity AND no fiscal sponsor → FAIL (P0)"
      - "Strategic-area misalignment (none of: Arts & Culture; Civic Participation; Climate, Environment & Health; Community & Economic Development; Food Systems; Veterans; Workforce) → FAIL"
      - "Primary service area entirely outside Commonwealth of Pennsylvania → WARN at funder layer (NOT P0 fail), DOWNGRADE Scout priority to LOW. Heinz public grants page favors PA-Commonwealth-serving-SWPA proposals, but GPR 2024 respondent geography includes outside-Allegheny and outside-Pennsylvania respondents — so a universal funder-layer P0 geo gate would over-restrict against the corpus evidence. Per-program Heinz initiatives may upgrade this to P0."
      - "Primary service area is PA-Commonwealth-but-outside-SWPA-10-county AND proposal does not expressly benefit SWPA-region or PA-state residents → DOWNGRADE (not fail; flag for operator)"
      - "Cold-outreach proposal without program-officer prior contact → WARN with structured recommended-operator-actions (seek PO conversation; find peer-grantee/civic-partner intro; tighten strategy-fit language before submitting LOI); NOT a fail."
      - "Project depends visibly on legacy 4-area taxonomy (Sustainability / Creativity / Learning) → DOWNGRADE; flag for taxonomy refresh; F-HEINZ-LEGACY-TAXONOMY-LEAK fires."
    common_rejections:
      - "Individual artist or for-profit applicant without fiscal sponsor — direct ineligibility (fiscal sponsorship by an eligible 501(c)(3) may rescue)."
      - "Strategic-area claim without operational evidence (e.g., 'Food Systems' claim without food-systems practice)."
      - "Multi-year capacity-building need framed as a single-year project ask — fails mechanism-M3 fit; Red Team flags this pattern explicitly."
      - "Cold-outreach without LOI / introduction from existing Heinz grantee — does NOT fail closed but is downgraded; operator should be advised to use the recommended-operator-actions before submitting."
      - "Geographic fit framed only as 'greater Pittsburgh' without naming the actual SWPA county or neighborhood — downgrade for vagueness, not for geography per se."

  score:
    primary_question: "Theory-of-change coherence + outcomes-vs-outputs articulation + relational-trust signals + thematic alignment."
    evidence_rewarded:
      - "Theory-of-change diagram or explicit articulation (intervention → mechanism → outcome over time)"
      - "3-year operational success picture with specific indicators"
      - "Prior Heinz site visit referenced + program-officer named (Tier-2/3)"
      - "Outcomes distinct from outputs with measurement plan"
      - "Sustained-change framing (not one-shot)"
    scoring_blind_spots:
      - "Theory-of-change can become overly linear (problem → activity → outcome) — reality is non-linear; balance."
      - "Relational-trust signals (program-officer name, prior visits) are powerful but can read as transactional if overplayed."
    common_penalties:
      - "Outcomes conflated with outputs → -3 to -5 points."
      - "Cold-outreach without prior Heinz relationship → -2 to -4 points (informal scoring)."
      - "Theory of change reads as naive linear chain → -3 points."

  consensus:
    primary_question: "Theory-of-change rigor + outcomes articulation + relational-trust vs panel peers."
    tie_breakers:
      - "Adjacent theory-of-change scores: higher band requires named mechanism + named risks + adaptation plan."
      - "Adjacent outcomes scores: higher band requires measurement plan + baseline + targets."
    portfolio_considerations: |
      Heinz balances portfolio across the seven strategic areas (Arts &
      Culture; Civic Participation; Climate, Environment & Health; Community
      & Economic Development; Food Systems; Veterans; Workforce),
      organizational maturity stages (emergent → established), and SWPA
      sub-geographic distribution — both Pittsburgh neighborhoods (downtown,
      North Side, East End, Hazelwood, etc.) AND non-Pittsburgh SWPA
      counties (Mon Valley straddling Allegheny/Washington/Fayette, Beaver
      County, Westmoreland, Armstrong, Butler, Greene, Indiana, Lawrence).
      Heinz's own 2026 Workforce announcement confirmed grants "span 10
      counties." DEI portfolio pattern (GPR 2024): over two-thirds of
      grantees report their funded work was meant primarily to benefit at
      least one historically disadvantaged group — particularly African
      American or Black individuals and communities.

evidence_ladder:
  strongest:
    - "Prior Heinz grant track record with documented outcomes"
    - "Theory-of-change diagram with mechanism + risks + adaptation"
    - "Named Heinz program officer + documented prior site visit"
    - "Outcomes measurement plan with baseline + targets + indicators"
    - "Multi-year sustained-change framing"
  acceptable:
    - "Prior similar foundation funding (Hillman, Pittsburgh Foundation, etc.)"
    - "Theory-of-change narrative without diagram"
    - "Introduction letter from existing Heinz grantee"
    - "Outcomes named with proxy indicators"
  weak:
    - "Outputs framed as outcomes (workshops delivered, attendance counts)"
    - "Linear problem-activity-outcome chain"
    - "Generic SWPA-region framing without sub-geography (which county, which neighborhood, which valley)"
  unacceptable:
    - "Cold-outreach without any prior foundation relationship"
    - "Out-of-PA-Commonwealth service area with no SWPA-or-PA-state-resident benefit articulated"
    - "Activity count as success metric"
    - "Individual artist or for-profit applicant without fiscal sponsor"

language_register:
  preferred_terms:
    - theory_of_change
    - outcomes                                              # NOT outputs
    - mechanism
    - sustained_change
    - operational_picture
    - program_officer                                       # foundation-canonical
    - strategic_area                                        # Heinz canonical (per 2026 site refresh; supersedes "thematic_area")
    - southwestern_pennsylvania                             # Heinz canonical
    - SWPA                                                  # Heinz canonical short form
    - emerging_practice
    - place_based                                           # SWPA-region resonance
    - historically_disadvantaged                            # GPR 2024 portfolio-pattern alignment
  suspicious_terms:
    # "Innovative" is NOT inherently suspicious at Heinz — GPR 2024 p.2
    # explicitly praises grantees' "long-term 'innovative' approaches" and
    # "statewide systems change" commitments. The failure mode is EMPTY /
    # UNSUPPORTED innovation language, not innovation itself. Editor flags
    # the term only when it appears without a backing track record, named
    # mechanism, or evidence.
    - unsupported_innovation                                # innovative claim without track record / mechanism / evidence
    - unsupported_cutting_edge                              # same shape — claim without backing
    - we_will_deliver                                       # activity framing not outcomes
    - significant_outputs                                   # outputs ≠ outcomes
    # NOTE: "rural" was previously flagged here and has been REMOVED in the
    # [FIDELITY-FIX-HEINZ] amendment 2026-05-18. SWPA includes Greene,
    # Fayette, Indiana, Lawrence, Armstrong, Butler — all of which have
    # rural and small-town communities Heinz actively funds. Flagging
    # "rural" as suspicious was a P1 unsupported assertion that would
    # have suppressed valid applications from the non-Pittsburgh half of
    # the SWPA 10-county region.
    # NOTE: "innovative" was previously listed as a flat suspicious term;
    # changed to "unsupported_innovation" in the [FIDELITY-FIX-HEINZ]
    # three-mechanism amendment 2026-05-18 because GPR 2024 explicitly
    # praises Heinz's long-term innovative approaches as a portfolio
    # signature. Innovation framing is rewarded when backed; the failure
    # mode is empty language, not the concept.
  sentence_shapes_that_work:
    - "If we [intervention] in [named SWPA county or Pittsburgh neighborhood], we expect [outcome] over [3 years], because [mechanism]. By year 3, success looks like [specific operational picture]."
    - "Sustained change at year 5 requires [retention mechanism] beyond grant period; we will [transition plan]."
    - "Our work expressly benefits residents of [named SWPA county] within the southwestern Pennsylvania region."   # PA-statewide-serving-SWPA framing per Heinz public grants page
  sentence_shapes_that_fail:
    - '"We will deliver workshops to X participants..." (outputs as outcomes)'
    - '"Our innovative approach will create..." (suspicious)'
    - '"Our program serves the greater Pittsburgh area..." (generic; name the actual county or neighborhood)'
drafting_implications:
  scribe_must_do:
    - "[M1] Frame the request as a regional alignment opportunity, not merely an organizational need. Name the larger Pittsburgh civic / SWPA-ecosystem movement the project sits inside. Name other funders / public partners Heinz could align with."
    - "[M2] Make strategic-fit logic explicit. Map the project to one (or more) of the seven canonical strategic areas: Arts & Culture; Civic Participation; Climate, Environment & Health; Community & Economic Development; Food Systems; Veterans; Workforce. Surface any context that Heinz program officers might NOT already have."
    - "[M3] Include a partnership-use paragraph in §V (or as a sidebar): name how Heinz can help beyond dollars — thought partnership, convening, introductions to other funders, multi-year continuity — without making unrealistic demands."
    - "[M3] If the work is multi-year capacity-building, explicitly articulate the request horizon vs the work horizon. If asking for a single-year cycle on multi-year work, name the transition plan."
    - "Lead §I with theory-of-change framing (intervention → mechanism → outcome over time + 3-year operational picture). Foundation-program-officer register."
    - "Reference named Heinz program officer + prior site visit if applicable."
    - "Frame SWPA scope with sub-geography specificity — name the actual county (Allegheny / Armstrong / Beaver / Butler / Fayette / Greene / Indiana / Lawrence / Washington / Westmoreland) and, where applicable, the named Pittsburgh neighborhood (downtown / North Side / East End / Hazelwood / Mon Valley)."
    - "If applicant is PA-Commonwealth-but-outside-SWPA or fully outside-PA, explicitly articulate how the proposed work serves SWPA-region or PA-state residents (per Heinz public grants page; funder-layer enforcement is advisory not P0)."
    - "Include sustained-change / transition-plan in §III."
    - "Calibrate request size against Heinz's median grant of ~$100K (2024 GPR). Ambitious larger asks are not blocked but need stronger sustained-change framing."
  scribe_must_not_do:
    - "Lead with problem statement (federal style); start with theory of change."
    - "Frame the ask as money-only — Heinz's value is also legitimacy + partnership + multi-year continuity."
    - "Assume Heinz already understands why this work matters or who the applicant is — Heinz is in active strategy refresh + program-staff capacity stretch."
    - "Pitch a single-year check for a multi-year capacity problem without naming the mismatch."
    - "Use 'innovative' / 'cutting-edge' / 'novel' framing without a backing track record, named mechanism, or evidence — empty innovation language is suspicious; backed innovation is rewarded (GPR p.2)."
    - "Treat outcomes-vs-outputs distinction as Heinz's #1 scoring vector — it's a general foundation heuristic, not a Heinz-specific load-bearing finding per GPR 2024."
    - "Generic 'greater Pittsburgh area' framing without naming the actual SWPA county or neighborhood."
    - "Default to Allegheny-County-only scoping when the project actually serves multiple SWPA counties."
    - "Use the legacy 4-area taxonomy (Sustainability / Creativity / Learning / Community & Economic Development) — Heinz refreshed to a 7-strategy taxonomy."
    - "Cold-outreach without first attempting program-officer conversation or peer-grantee introduction (advisory not impermissible; program staff carry 53 active grants + 50 apps per the 2024 GPR — cold proposals compete for thin attention)."
  section_ordering_notes: |
    §I theory of change + 3-year picture → §II outcomes + measurement plan
    → §III sustained-change / transition → §IV budget → §V qualifications +
    prior-relationship references + [M3] partnership-use paragraph → §VI work
    plan. [M1] regional alignment language threads through §I + §III. [M2]
    strategic-fit clarity threads through §I (named strategy) + §II (named
    outcome under that strategy) + §V (named relationship history).

judge_implications:
  # Weighting reshapes around the three GPR behavior_mechanisms.
  # Outcomes-vs-outputs is downweighted from "Heinz-specific load-bearing" to
  # "general foundation-officer heuristic" because GPR 2024 does not support
  # the prior claim that outcomes-conflation is Heinz's #1 downgrade vector.
  scoring_dimensions_to_weight_harder:
    - "[M1] Regional Legitimacy Capital — evidence the project sits inside a larger Pittsburgh civic / SWPA-ecosystem movement and that Heinz participation could unlock other funders / public partners / civic legitimacy. Weight ≥20%."
    - "[M2] Transition-Sensitive Strategic-Fit Clarity — proposal makes strategic-fit logic explicit under Heinz's current 7-strategy framing, without assuming Heinz remembers prior context. Weight ≥20%."
    - "[M3] Capacity-Partnership Logic — multi-year logic, collaboration pathways, clear capacity outcomes, articulated beyond-the-grant partnership use. Weight ≥20%."
    - "Theory-of-Change Coherence — general foundation-program-officer register. Weight ≥15%."
    - "Sustained Change / Transition Plan — alignment with mechanism M3. Weight ≥10%."
    - "Outcomes Articulation (distinct from outputs) — general foundation-officer heuristic, NOT Heinz-specific per GPR 2024. Weight ~5-10% (downweighted from prior ≥20%)."
  evidence_required_before_high_score:
    - "[M1] Regional Legitimacy ≥4: named SWPA civic / ecosystem partners, named other funders co-investing or alignable, named public partner (city / county / state agency) where applicable, explicit framing of regional alignment opportunity."
    - "[M2] Strategic-Fit Clarity ≥4: explicit mapping to one of the seven current Heinz strategic areas with reasoning; explicit acknowledgement of any context that Heinz program officers might NOT already have; current-strategy framing language (not legacy 4-area taxonomy)."
    - "[M3] Capacity-Partnership ≥4: multi-year horizon with named milestones, named beyond-the-grant partnership uses (convening / thought partnership / introductions / multi-year continuity), explicit articulation of how a short grant cycle would or would not match the work."
    - "Theory of Change ≥4: explicit mechanism + named risks + adaptation."
    - "Sustained Change ≥4: transition plan + retention mechanism + post-grant funder pipeline."

red_team_probe_seeds:
  # Heinz-specific probes derived from the three GPR behavior_mechanisms first.
  # General-foundation heuristics follow at lower priority and are marked GENERAL.
  - probe: "[M1] Is the applicant asking Heinz for money only, or positioning Heinz as a catalytic regional partner whose participation could unlock other funders, public partners, or civic legitimacy?"
    why_it_matters: "Behavior-mechanism M1 (regional_legitimacy_capital). GPR 2024 p.2: grantees describe Heinz participation as legitimacy-bearing. Money-only framing under-uses Heinz's actual function."
    source: "GPR 2024 §'The Endowments as a Community Leader', p.2"
  - probe: "[M2] Does the proposal depend on old Heinz priorities (legacy 4-area taxonomy or stale relationship assumptions) or does it engage Heinz's current 7-strategy framing and the realities of current program-staff capacity (53 active grants + 50 apps per staffer)?"
    why_it_matters: "Behavior-mechanism M2 (transition_sensitive_relationship_clarity). GPR 2024 p.1, p.4, p.5: Heinz is in active strategy/staff/communications transition; grantees rate communication clarity significantly lower than 2019."
    source: "GPR 2024 §'Context and Overview' p.1 + §'Decreases in Clarity of Communication and Depth in Grantee Relationships' p.4-5"
  - probe: "[M3] Is the applicant asking for a single-year check to solve a multi-year capacity problem? Or does the request horizon match the work horizon?"
    why_it_matters: "Behavior-mechanism M3 (capacity_partnership_beyond_grant). GPR 2024 p.3: average Heinz grant length is 1.7 years (shortest since 2005); grantees explicitly ask for longer / larger / more flexible. Horizon mismatch undermines fit."
    source: "GPR 2024 §'Monetary Support' p.3 + §'Future Opportunity – Increase Grant Length' p.4"
  - probe: "[M3] Does the proposal name how Heinz can help beyond dollars — thought partnership, convening, introductions to other funders, multi-year continuity — without making unrealistic demands?"
    why_it_matters: "Behavior-mechanism M3. GPR 2024 p.3: grantees receiving any beyond-grant assistance rate Heinz higher across understanding / interaction / clarity / openness / transparency."
    source: "GPR 2024 §'Assistance Beyond Grant Dollars' p.3"
  - probe: "Is the applicant a 501(c)(3)+509(a) public charity, a federally-tax-exempt government entity, or fiscally sponsored by one? Or is it an individual or for-profit (which Heinz does not fund)?"
    why_it_matters: "Eligibility envelope is explicit on Heinz public grants page; individual artists and for-profits need fiscal sponsorship."
    source: "Heinz public grants page, Step 2 (Determine your eligibility)"
  - probe: "Is the proposed work mapped to one of Heinz's seven canonical strategic areas (Arts & Culture; Civic Participation; Climate, Environment & Health; Community & Economic Development; Food Systems; Veterans; Workforce)? Or does it reach back to the legacy 4-area taxonomy (Sustainability / Creativity / Learning / CED)?"
    why_it_matters: "Heinz refreshed its strategy framework; legacy-taxonomy language signals stale source material. F-HEINZ-LEGACY-TAXONOMY-LEAK fires."
    source: "https://www.heinz.org/strategic-areas"
  - probe: "Is geographic fit inside the Commonwealth of Pennsylvania, and ideally within the SWPA 10-county region? If applicant is outside-PA, is there an explicit articulation of how the work serves SWPA-region or PA-state residents, or a partner SWPA-resident organization?"
    why_it_matters: "Heinz public grants page favors PA-Commonwealth-serving-SWPA proposals. Funder-layer enforcement is a weighted preference + advisory warning (F-HEINZ-OUTSIDE-PA-WARNING MED), not a universal hard-fail. Per-program initiatives may upgrade."
    source: "Heinz public grants page (Step 2) + GPR 2024 respondent-geography evidence"
  - probe: "[GENERAL] Does the proposal distinguish outcomes (sustained change in target population) from outputs (activities delivered)?"
    why_it_matters: "General foundation-program-officer heuristic — applies across the foundation funder family, NOT a Heinz-specific load-bearing finding per GPR 2024. Editor flags conflation; severity is LOW."
    source: "General foundation-officer heuristic; not Heinz-specific per GPR"
  - probe: "[GENERAL] Is theory of change overly linear (problem → activity → outcome) or does it include mechanism + risks + adaptation?"
    why_it_matters: "General foundation-officer heuristic. Naive linearity signals proposal lacks rigor across funders."
    source: "General foundation-officer heuristic"
  - probe: "Is innovation language backed by track record, named mechanism, or evidence — or is it empty / unsupported claim language?"
    why_it_matters: "GPR 2024 p.2 praises Heinz's long-term 'innovative' approaches — innovation framing is rewarded when backed. Unsupported innovation language is the failure mode (F-HEINZ-UNSUPPORTED-INNOVATION LOW), not innovation itself."
    source: "GPR 2024 §'The Endowments as a Community Leader' p.2"

logician_gate_candidates:
  - gate: F-HEINZ-ELIGIBLE-ENTITY-MISSING
    gate_type: hard_eligibility_gate
    failure_condition: "kfr.applicant.tax_status not in {'501c3_public_charity', 'government_entity_federally_tax_exempt'} AND not kfr.applicant.has_fiscal_sponsor()"
    severity: P0
    fail_action: REJECT_NO_DRAFT
    source_required: true
    corpus_ref: "Heinz Endowments public Grants page (Process & How to Apply); canonical-reference-doc anchored §Heinz Endowments Eligibility"
    confidence:
      level: medium
      reason: "Eligibility is canonical-reference-doc anchored + Heinz grants page direct citation; pinpoint URL ingested in [FIDELITY-FIX-HEINZ] commit"
      promotion_requirement: "Heinz public grants page snapshot verbatim ingested at Pillar-2"
    note: "Renamed from F-HEINZ-501C3-MISSING in [FIDELITY-FIX-HEINZ] 2026-05-18. The previous gate was incomplete (P1): Heinz public grants page explicitly funds 501(c)(3)+509(a) public charities AND federally-tax-exempt government entities."
  - gate: F-HEINZ-INDIVIDUAL-OR-FORPROFIT
    gate_type: hard_eligibility_gate
    failure_condition: "kfr.applicant.entity_type in {'individual', 'for_profit'} AND not kfr.applicant.has_fiscal_sponsor()"
    severity: P0
    fail_action: REJECT_NO_DRAFT
    source_required: true
    corpus_ref: "Heinz Endowments public Grants page — 'Individuals and for-profit organizations are not eligible for funding.'"
    confidence:
      level: high
      reason: "Direct verbatim citation from Heinz public Grants page included in [FIDELITY-FIX-HEINZ] commit; canonical-reference-doc-grounded"
      promotion_requirement: "Already at level: high — no further promotion needed pre-Pillar-2"
    note: "Added in [FIDELITY-FIX-HEINZ] 2026-05-18. Heinz public grants page: 'Individuals and for-profit organizations are not eligible for funding.' Previously absent — material omission that could have led Scribe to draft for ineligible applicants."
  - gate: F-HEINZ-OUTSIDE-PA-WARNING
    gate_type: relationship_signal
    failure_condition: "kfr.applicant.primary_service_state != 'PA' AND not kfr.applicant.expressly_benefits_swpa_or_pa_residents()"
    severity: MED
    fail_action: WARN_OPERATOR
    source_required: false
    corpus_ref: "Heinz GPR 2024 Key Findings Memo §respondent-geography; Heinz public grants page §SWPA-and-PA-Commonwealth-serving framing"
    confidence:
      level: medium
      reason: "Geography-as-relationship-signal demotion is GPR-2024-backed per [FIDELITY-FIX-HEINZ] three-mechanism amendment; canonical-reference-doc anchored"
      promotion_requirement: "Heinz grants page snapshot + GPR 2024 respondent-geography exhibit ingested at Pillar-2"
    note: "Demoted from P0 to MED in [FIDELITY-FIX-HEINZ] three-mechanism amendment 2026-05-18 (replaces the deleted F-HEINZ-NOT-SWPA-OR-PA P0 / F-HEINZ-NOT-PITTSBURGH-METRO P0 chain). Rationale: GPR 2024 respondent geography includes outside-Allegheny and outside-Pennsylvania respondents — a universal funder-layer P0 geo gate would over-restrict against the corpus evidence. Heinz public grants page favors PA-Commonwealth-serving-SWPA proposals, but the funder-layer enforcement is a weighted preference + advisory warning, not a universal hard-fail. Per-program Heinz initiatives (e.g., a specific RFP that geo-limits to the SWPA 10-county region) may upgrade this to P0 in the per-program charter; those gates layer ON TOP of this funder-layer warning, not replacing it."
    recommended_operator_action:
      - "If applicant is PA-Commonwealth-but-outside-SWPA-10-county, articulate explicitly how the proposed work serves SWPA-region or PA-state residents (the Heinz grants page language)."
      - "If applicant is fully outside PA, confirm with program officer that the proposal is in scope before drafting; consider whether a partner SWPA-resident organization should hold the application instead."
  - gate: F-HEINZ-COLD-OUTREACH-WARNING
    gate_type: relationship_signal
    failure_condition: "not kfr.applicant.has_documented_prior_heinz_relationship()"
    severity: MED
    fail_action: WARN_OPERATOR
    source_required: false
    corpus_ref: "Heinz GPR 2024 p.5 — program-staff load 53 active grants + 50 applications per staffer"
    confidence:
      level: medium
      reason: "Relationship-warmth gate is GPR-2024-backed per [FIDELITY-FIX-HEINZ] three-mechanism amendment"
      promotion_requirement: "Heinz program-staff load exhibit from GPR 2024 p.5 ingested at Pillar-2"
    note: "Revised in [FIDELITY-FIX-HEINZ] three-mechanism amendment 2026-05-18: structured recommended-operator-actions added; gate explicitly NOT a hard-fail. Program-staff load is 53 active grants + 50 applications per staffer per GPR 2024 p.5, so cold-outreach proposals compete for thin attention — but cold-outreach is not impermissible."
    recommended_operator_action:
      - "Seek program-officer conversation before submission."
      - "Find peer grantee / civic partner introduction."
      - "Submit LOI only after strategy-fit language is tightened."
  - gate: F-HEINZ-CAPACITY-SHORT-TERM-MISMATCH
    gate_type: competitive_scoring_signal
    failure_condition: "draft.request_horizon == 'single_year' AND draft.work_type in {'multi_year_capacity_build', 'systems_change', 'sustained_program_continuity'}"
    severity: MED
    fail_action: WARN_OPERATOR
    source_required: false
    corpus_ref: "Heinz GPR 2024 p.3-4 — grant length 1.7 years average; grantee ask-for-longer-flexible-support signal"
    confidence:
      level: medium
      reason: "Mechanism-mismatch heuristic is GPR-2024-backed per [FIDELITY-FIX-HEINZ] three-mechanism amendment"
      promotion_requirement: "GPR 2024 §p.3-4 exhibit ingested at Pillar-2"
  - gate: F-HEINZ-OUTCOMES-CONFLATED-WITH-OUTPUTS
    gate_type: competitive_scoring_signal
    failure_condition: "draft.outcomes_section.contains_only_activity_counts_or_attendance_numbers()"
    severity: LOW
    fail_action: WARN_OPERATOR
    source_required: false
    corpus_ref: pending_pillar_2  # general foundation-program-officer heuristic; not Heinz-specific per GPR
    confidence:
      level: low
      reason: "general foundation-officer heuristic; GPR 2024 does not surface this as a Heinz-specific load-bearing finding per [FIDELITY-FIX-HEINZ] amendment"
      promotion_requirement: "(Not promoted — gate explicitly demoted to LOW per [FIDELITY-FIX-HEINZ]. Pillar-2 may surface evidence that promotes or retires.)"
    pass_1_reconciliation_note: "Purpose-wise this is drafting heuristic; classified as competitive_scoring_signal per (LOW, WARN_OPERATOR) tuple. Migration to drafting_warning with WARN_SCRIBE is a Pass 3 reconciliation candidate."
    note: "Severity LOWERED from MED to LOW in [FIDELITY-FIX-HEINZ] three-mechanism amendment 2026-05-18. Outcomes-vs-outputs conflation is a general foundation-program-officer heuristic, NOT a Heinz-specific load-bearing finding. GPR 2024 does not surface outcomes-conflation as the #1 Heinz downgrade vector — it surfaces declining communication / understanding ratings and shortened grant length. Editor still warns on conflation as part of the general foundation register, but the gate weighting drops."
  - gate: F-HEINZ-LEGACY-TAXONOMY-LEAK
    gate_type: competitive_scoring_signal
    failure_condition: "draft.strategic_area_mapping uses any of {'Sustainability','Creativity','Learning'} as a Heinz strategic-area label"
    severity: LOW
    fail_action: WARN_OPERATOR
    source_required: true
    corpus_ref: "Heinz 7-area taxonomy snapshot per [FIDELITY-FIX-HEINZ] amendment 2026-05-18 (Arts & Culture; Civic Participation; Climate, Environment & Health; Community & Economic Development; Food Systems; Veterans; Workforce)"
    confidence:
      level: medium
      reason: "Taxonomy refresh is documented in [FIDELITY-FIX-HEINZ] commit; pinpoint Heinz strategic-area page citation pending Pillar-2"
      promotion_requirement: "Heinz strategic-area page snapshot ingested at Pillar-2"
    pass_1_reconciliation_note: "Purpose-wise this is drafting heuristic (stale-vocabulary detector); classified as competitive_scoring_signal per (LOW, WARN_OPERATOR) tuple. Pass 3 may migrate to drafting_warning."
    note: "Added in [FIDELITY-FIX-HEINZ] 2026-05-18. Heinz refreshed to 7-area taxonomy (Arts & Culture; Civic Participation; Climate, Environment & Health; Community & Economic Development; Food Systems; Veterans; Workforce). Legacy-taxonomy language reveals stale charter or stale corpus."
  - gate: F-HEINZ-UNSUPPORTED-INNOVATION
    gate_type: competitive_scoring_signal
    failure_condition: "draft uses 'innovative' / 'cutting-edge' / 'novel' framing without a backing track record, named mechanism, or evidence"
    severity: LOW
    fail_action: WARN_OPERATOR
    source_required: false
    corpus_ref: "Heinz GPR 2024 §'The Endowments as a Community Leader' p.2 — innovation praised when backed by long-term track record"
    confidence:
      level: low
      reason: "Detector heuristic explicitly tagged [CONJECTURE — Pillar-2 corpus pending] in [FIDELITY-FIX-HEINZ] amendment"
      promotion_requirement: "Detector pattern specification + Heinz innovation-language portfolio sample ingested at Pillar-2"
    pass_1_reconciliation_note: "Purpose-wise this is drafting heuristic (Scribe register guidance); classified as competitive_scoring_signal per (LOW, WARN_OPERATOR) tuple. Pass 3 may migrate to drafting_warning."
    note: "Added in [FIDELITY-FIX-HEINZ] three-mechanism amendment 2026-05-18. Replaces the earlier flat 'innovative is suspicious' framing. GPR 2024 p.2 explicitly praises Heinz's long-term innovative approaches as a portfolio signature — innovation language is rewarded when backed, suspicious only when empty. [CONJECTURE — Pillar-2 corpus pending] for the exact detector heuristic."

# DELETED GATES (preserved here as audit trail for [FIDELITY-FIX-HEINZ] amendment):
#   - F-HEINZ-NOT-PITTSBURGH-METRO (P0; pre-fix) — replaced by F-HEINZ-NOT-SWPA-OR-PA in geo-only fix, then DELETED entirely in three-mechanism amendment. Reason: GPR respondent geography includes outside-PA respondents; a universal funder-layer geo P0 over-restricts against the corpus. Geo enforcement now lives in F-HEINZ-OUTSIDE-PA-WARNING (MED).
#   - F-HEINZ-NOT-SWPA-OR-PA (P0; intermediate state from geo-only fix) — DELETED in three-mechanism amendment. Same reason as above.
#   - F-HEINZ-501C3-MISSING (P0; pre-fix) — replaced by F-HEINZ-ELIGIBLE-ENTITY-MISSING (P0) with broadened entity scope.

source_backing:
  corpus_refs:
    - artifact: "Heinz GPR 2024 Key Findings Memo (prepared by CEP)"
      url: "https://www.heinz.org/UserFiles/File/THE%20Grantee%20Perception%20Report.pdf"
      local_copy: "uploads/c9f4d852-THE_2024_GPR__Key_Findings_Memo__03212025.pdf (operator-uploaded 2026-05-18; SHA elsewhere)"
      date_published: "2025-03-21"
      retrieved: "2026-05-18"
      relied_on_for: "Median grant size 2024 (~$100K); average grant length 1.7 years; 64% grantee response rate (356 respondents); program staff load 53 active grants + 50 apps per staffer; DEI portfolio pattern (>2/3 grantees serve historically disadvantaged groups, particularly Black communities); declining ratings on communication/relationships post-2019; 61% receive consistent Heinz funding; median grantee annual budget ~$1.5M."
    - artifact: "Heinz Endowments public Grants page (Process & How to Apply)"
      url: "https://www.heinz.org/grants"
      retrieved: "2026-05-18"
      relied_on_for: "Geographic eligibility text ('We concentrate our efforts and resources in southwestern Pennsylvania (SWPA)... the foundation is generally unable to consider applications for funding outside the Commonwealth of Pennsylvania, unless the proposal is expressly for the benefit of residents of the SWPA region or state'); eligible-entity definition (501(c)(3) + 509(a) + federally-tax-exempt government entities; individuals and for-profits not eligible); application process (rolling LOI ~10 min, 45-day acknowledgement, 60-90 day decision, Blackbaud portal)."
    - artifact: "Heinz Endowments public Strategies page"
      url: "https://www.heinz.org/strategic-areas"
      retrieved: "2026-05-18"
      relied_on_for: "Canonical seven-strategy taxonomy (Arts & Culture; Civic Participation; Climate, Environment & Health; Community & Economic Development; Food Systems; Veterans; Workforce)."
    - artifact: "Heinz Endowments home page + 2026 Workforce grants announcement"
      url: "https://www.heinz.org/"
      retrieved: "2026-05-18"
      relied_on_for: "10-county SWPA span confirmation ('These Workforce grants span 10 counties'); ~$90M annual grantmaking volume; mission framing ('southwestern Pennsylvania has the drive and wisdom to shape our nation's future')."
    - "<NEEDED — Pillar 2: Heinz 990-PF FY22-FY24>"
    - "<NEEDED — Pillar 2: Per-strategy position papers / annual report>"
    - "<NEEDED — Pillar 2: 0-2 Heinz program officer conversations (Tier-2/3)>"
  confidence: MEDIUM (was LOW pre-corpus). Geographic, eligibility, taxonomy, and application-process facts now corpus-backed; portfolio composition and per-strategy priorities still owed.
  unresolved_questions:
    - "Per-strategy priority weighting (equal vs weighted by strategic-plan emphasis)"
    - "Foundation-officer relationship-management cadence post-award"
    - "Heinz fiscal-sponsorship acceptance practice + named fiscal-sponsorship intermediaries"
    - "Whether the 'Community Partners Fund' is in-scope for general-application logic or a separate track"
    - "Per-strategy median grant size + length (GPR memo gives overall medians; per-strategy detail likely in 990-PF FY22-FY24)"
```

---

## §1 — What "depth" means for THIS artifact

Heinz-Endowments funder-level depth is **the three GPR-derived behavior_mechanisms** — regional legitimacy capital, transition-sensitive relationship clarity, and capacity-partnership-beyond-grant — operating within a **foundation-program-officer register substrate**. The mechanisms (not generic "Heinz likes relationships" framing) are what makes this charter Heinz-specific. The substrate (theory-of-change framing, foundation-officer vocabulary, named relationship history) is general foundation-funder behavior that applies across the family but is necessary scaffolding for the mechanisms to land.

**Codex same-prompt-with/without test:**
- **Without** — Scribe writes problem-statement-first proposal with money-only framing. Generic foundation pitch. Likely defaults to Pittsburgh-metro framing and misses the broader SWPA-10-county scope; likely maps to the legacy 4-area taxonomy; doesn't explain why the work matters to Heinz's current strategy; doesn't surface beyond-the-grant partnership use; doesn't name regional alignment opportunities; doesn't acknowledge the request-horizon vs work-horizon question.
- **With** — Scribe wires §I to behavior_mechanism M1 (regional alignment opportunity language), §I + §II to M2 (explicit current-strategy mapping; no assumed shared context), §V to M3 (partnership-use paragraph; request horizon vs work horizon). Uses precise SWPA sub-geography (which of 10 counties, which Pittsburgh neighborhood, which corridor). Maps to one of the seven canonical strategic areas. Calibrates request size against ~$100K median. Judge weights M1 ≥20% + M2 ≥20% + M3 ≥20% + Theory of Change ≥15% + Sustained Change ≥10% + Outcomes ~5-10%. Red Team probes per mechanism (M1: money-only vs catalytic partner; M2: stale priorities / unclear strategic fit; M3: short-term check for long-term capacity problem) PLUS general-foundation heuristics flagged as general (outcomes-vs-outputs; theory-of-change linearity; unsupported innovation). Logician fails closed on ineligible-entity + individual-or-for-profit (both P0); warns on outside-PA (NOT a P0 universal fail — funder-layer is weighted), cold-outreach (advisory with structured operator-actions), capacity-short-term-mismatch, legacy-taxonomy leak, unsupported innovation.

---

## §2 — Primary sources in scope

| Corpus category | Specific sources | Access path | Estimated count | Pillar-1 status |
|-----------------|------------------|-------------|-----------------|-----------------|
| `strategic/` | Heinz strategic framework + per-strategy position papers; annual report | Public Heinz site (`/strategic-areas`, `/about-us`) | 2-4 | Strategies page LANDED for taxonomy; per-strategy + annual report owed |
| `grantee_perception/` | **Heinz GPR 2024 Key Findings Memo (CEP, 2025-03-21)** | https://www.heinz.org/UserFiles/File/THE%20Grantee%20Perception%20Report.pdf | 1 | **LANDED 2026-05-18 — primary source for the [FIDELITY-FIX-HEINZ] amendment** |
| `application_process/` | Heinz public Grants page (eligibility + process + portal) | https://www.heinz.org/grants | 1 | LANDED 2026-05-18 |
| `awards/` | Heinz 990-PF FY22-FY24; food-systems / Community-Partners-Fund patterns | Public 990-PF (Candid / ProPublica) | 3-4 | owed |
| `interviews/` | 0-2 Heinz program officer (Tier-2/3) | Operator network outreach | 0-2 | owed |
| `guidance/` | Published essays / thought-leadership pieces signaling priority shifts; h Magazine | Public Heinz publications | 1-3 | owed |
| `geographic/` | SWPA 10-county scope framing + 2026 Workforce 10-county span announcement | Heinz public + 990-PF geographic distribution | 1-2 | LANDED 2026-05-18 (Workforce announcement on Heinz home page) |

Case law OUT OF SCOPE.

---

## §3 — Tier classification

| Field | Tier |
|-------|:----:|
| Default | `1` |
| `funder_officer_relationship_notes` | `3` |
| `dialect_notes_operator_derived` | `2` |
| `program_officer_check_in_cadence_norms` | `2` |

---

## §4 — Refresh cadence

`annual` + `event_triggered` (leadership change; major strategic plan release).

---

## §5 — Calibration applicant pair

`food_systems` (CIC-01) × `operating_capacity` (CLC-03), with Catalytic Change (CLC-02) overlay.

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

- Per-initiative RFP text (Heinz relationship-driven solicitation dominates)
- Other SWPA-region foundations — separate funder artifacts (Hillman, Pittsburgh Foundation, McCune, RK Mellon)
- Compliance framework internals
- Reviewer-type heuristics
- Per-applicant 501(c)(3) / 509(a) / government-entity status (lives in `orgs/<slug>/`)
- Per-applicant fiscal-sponsorship arrangement (lives in `orgs/<slug>/`)
- Case law interpretation
- Per-grantee award-history dossier (lives in `funders/HEINZ-FOUNDATION/awards/`)
