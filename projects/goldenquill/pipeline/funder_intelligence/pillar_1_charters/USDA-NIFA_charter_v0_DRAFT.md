# Depth Charter — `USDA-NIFA` (funder behavior profile)

> **Pillar 1 of 4** per `pipeline/planning/funder_intelligence_database_research_project_2026-05-16.md` §3.1.
> **Quality bar** per `docs/FID_ARTIFACT_OPTIMIZATION_PRINCIPLES_2026-05-18.md` §1 + §2 + Codex framing.
> **Status: DEPTH CHARTER v0 (pre-corpus hypothesis; do not load as signed logic)** — re-authored to Codex yaml shape per operator directive 2026-05-18.
> **Status: GOLD-STANDARD DRAFT v0** — re-authored to Codex yaml shape per operator directive 2026-05-18.
>
> **[CONJECTURE — Pillar-2 corpus pending]** All USDA-NIFA-specific funder-fact claims are operator-asserted at charter authoring; Pillar-2 corpus assembly (NIFA strategic plan + AFRI/SARE national framework + peer-review panel composition guidance + agency-aggregate awards) promotes each claim via `corpus_ref` + verbatim quote. `F-FID-FACT-ORPHAN` enforces at Pillar-3 L-005.

---

## Header

| Field | Value |
|------:|:------|
| `artifact_id` | `USDA-NIFA` |
| `artifact_family` | `funder` |
| `version` | `depth_charter_v0` |
| `version` | `gold_standard_v0` |
| `lifecycle` | `draft` |
| `phase` | `1 — exemplar pair` |

---

## §A — Adversarial pre-checks

```yaml
runtime_consumer:
  scout:
    reads_fields: [program_roster, peer_review_panel_composition_norms]
    stage: DISCOVER
    decision_changed: "Scout DISCOVER tags radar hits with peer-review-academic register pre-filter; downgrades hits where applicant context lacks researcher/extension/PI signal for tiered NIFA programs that require academic credential."
  scribe:
    reads_fields: [funder_dialect, language_register, drafting_implications]
    stage: scaffold
    decision_changed: "Scribe applies peer-reviewer-academic register across all USDA-NIFA program drafts: methodology-first ordering (not narrative-first), explicit literature citation in §I, prior-publication track record in qualifications, IRB/animal-care/data-management certifications surfaced early. Distinct from USDA-RD's rural-prosperity-first register."
  judge:
    reads_fields: [judge_implications, scoring_dimensions_to_weight_harder]
    stage: cross_check
    decision_changed: "Judge cross-checks scientific-merit + methodology rigor + investigator qualifications dimensions weighted heavier than economic-impact-style criteria. NIFA reviewers reward novelty + falsifiable hypothesis + appropriate statistical power; downgrade observational-only-no-controls designs."
  red_team:
    reads_fields: [red_team_probe_seeds, known_failure_modes_at_funder_level]
    stage: probe_target_selection
    decision_changed: "Red Team probes NIFA-specific failure modes: COI declaration completeness, IRB/IACUC status when subjects involved, data-management plan presence, statistical-power adequacy, prior-NIFA-track-record honesty."
  logician:
    reads_fields: [eligibility_gates, logician_gate_candidates]
    stage: PRE
    decision_changed: "Logician fires USDA-NIFA funder-wide PRE-gates: F-USDA-NIFA-IRB-MISSING (HIGH), F-USDA-NIFA-IACUC-MISSING (HIGH), F-USDA-NIFA-DMP-MISSING (HIGH), F-USDA-NIFA-COI-INCOMPLETE (MED)."
```

```yaml
artifact_must_not_contain:
  - facts belonging to another artifact          # program-level → programs/USDA-NIFA-<program>-FY26.yaml
  - applicant-specific claims
  - uncited generalizations
  - compliance framework internals               # 2 CFR 200, IRB Common Rule, IACUC, FERPA-in-research → compliance_cascades/
  - reviewer-type heuristics                     # reviewer_heuristics/peer-reviewer-academic.yaml
  - other USDA agencies
  - case law interpretation
```

```yaml
strength_test:
  - "Name one concrete drafting decision this artifact changes."
  - "Name one proposal this artifact would reject or downgrade."
  - "Name one Red Team probe this artifact enables."
```

**Answers (PASSED — §1 + §B realize these concretely):**

1. **Drafting decision.** Scribe applies **methodology-first §I ordering** across all USDA-NIFA program drafts (hypothesis + research design + statistical power *before* impact narrative). Same Scribe prompt WITHOUT artifact produces narrative-first ordering; WITH artifact produces methodology-anchored opening that signals peer-review-academic-fluent applicant.
2. **Proposal rejected.** Logician `F-USDA-NIFA-IRB-MISSING` (HIGH) fails closed any USDA-NIFA application with human-subjects-research signals AND no IRB protocol ID in KFR. Saves Scribe from drafting + downstream from reviewing applications that NIFA will administratively reject at submission.
3. **Red Team probe.** `USDA-NIFA-PROBE-STATISTICAL-POWER-ADEQUACY` asks: *"Does the proposed design specify sample size + effect size + alpha + power explicitly, or is the design observational-only with no controls?"* NIFA peer-review panels routinely downgrade designs lacking explicit power analysis.

---

## §B — Codex-shape depth-charter YAML
## §B — Codex-shape gold-standard YAML

```yaml
artifact_id: USDA-NIFA
artifact_family: funder
version: depth_charter_v0
lifecycle: draft
validation_status: pre_corpus_hypothesis
runtime_load_status: do_not_load_as_signed_logic
operator_label: depth_charter_v0
version: gold_standard_v0
lifecycle: draft

one_sentence_job: |
  Equip every USDA-NIFA program draft (AFRI / SARE / BFRDP / CFP-NIFA / etc.)
  with peer-reviewer-academic register, COI + IRB + IACUC + DMP cascade
  defaults, and cross-program eligibility predicates.

runtime_consumers:
  scout: |
    DISCOVER tags hits with peer-review-academic register requirement; downgrades
    hits where applicant context lacks researcher/extension/PI signal.
  scribe: |
    Reads funder_dialect + language_register at scaffold; applies methodology-
    first §I ordering + peer-review-academic register.
  judge: |
    Cross-checks scientific-merit + methodology rigor + qualifications dimensions
    weighted heavier than economic-impact.
  red_team: |
    Probes COI completeness, IRB/IACUC status, DMP specificity, statistical-
    power adequacy, prior-track-record honesty.
  logician: |
    PRE-gates F-USDA-NIFA-IRB-MISSING / IACUC-MISSING / DMP-MISSING /
    COI-INCOMPLETE fire before any NIFA program-level gate.

mission_framing:
  one_paragraph_summary: |
    USDA National Institute of Food and Agriculture funds research, extension,
    and education across the land-grant cooperative-extension partnership +
    competitive grants programs (AFRI, BFRDP, SARE, CFP-NIFA, others).
    Peer-review-academic register dominates; methodology rigor + scientific
    merit weighted heavier than economic-impact criteria.
  corpus_ref: "<NEEDED — Pillar 2: NIFA strategic framework FY22-26>"
  corpus_ref: <NEEDED — Pillar 2: NIFA strategic framework FY22-26>

stage_behavior:
  screen:
    primary_question: "Baseline (SAM, UEI, federal-debt) + research-compliance (IRB/IACUC/DMP) + program-specific eligibility."
    time_budget: <NEEDED Pillar 2>
    pass_fail_triggers:
      - "Missing IRB protocol when human-subjects signal → FAIL"
      - "Missing IACUC protocol when animal-subjects signal → FAIL"
      - "Missing data-management plan → FAIL"
      - "Missing COI declaration → FAIL"
      - "Budget over per-program cap → FAIL"
    common_rejections:
      - "Letter of support from collaborating institution missing for multi-institution proposals."
      - "Biosketch in non-NIH format (verify per program)."
      - "Indirect-cost rate exceeds NIFA-mandated cap (varies by program; typically 30% for AFRI)."

  score:
    primary_question: "Scientific merit (novel hypothesis, methodology, power) + investigator qualifications (track record) + broader impacts."
    evidence_rewarded:
      - "Falsifiable hypothesis with explicit alternative outcomes"
      - "Statistical power analysis (sample size + effect size + alpha + power)"
      - "Prior peer-reviewed publication in proposed sub-discipline"
      - "Control + treatment design (not observational-only)"
      - "Letter of collaboration from named co-investigator at collaborating institution"
    scoring_blind_spots:
      - "Broader-impacts criterion often graded last; front-load extension/outreach for visibility."
      - "Reviewers may over-weight prior-publication track record vs. novelty; balance qualifications section."
    common_penalties:
      - "Observational-only design with no controls → -5 to -10 points on methodology."
      - "No statistical power analysis → -3 to -5 points."
      - "Single-PI proposal without collaboration when multi-disciplinary implied → -2 to -3 points."

  consensus:
    primary_question: "Methodology rigor + qualifications + broader impacts vs panel top-quartile peers."
    tie_breakers:
      - "Between adjacent scientific-merit scores, higher band requires explicit power analysis + control design."
      - "Between adjacent qualifications scores, higher band requires prior peer-reviewed publication in sub-discipline."
    portfolio_considerations: |
      NIFA panels balance funded portfolio across land-grant + non-land-grant
      institutions, geographic distribution, and program-area priority alignment.

evidence_ladder:
  strongest:
    - "Peer-reviewed publication in proposed sub-discipline by investigator (or co-investigator)"
    - "Prior NIFA-funded project with documented outcomes (CRIS database entry)"
    - "Pilot data showing effect size + variability for sample-size calculation"
    - "Letter of collaboration on collaborating-institution letterhead with role + time commitment"
  acceptable:
    - "Prior non-NIFA federal-grant funding (NIH, NSF, USDA-AMS, USDA-RD)"
    - "Extension publication or technical bulletin"
    - "Pilot data from researcher's own institution"
  weak:
    - "Conference abstract or non-peer-reviewed proceedings"
    - "Adjacent-topic publication without effect-size carryover argument"
  unacceptable:
    - "Trade-press article; vendor white paper; blog post"
    - "Speculative effect size with no pilot + no published precedent"

language_register:
  preferred_terms:
    - hypothesis
    - methodology
    - statistical_power
    - control
    - treatment
    - falsifiable
    - peer_reviewed
    - broader_impacts
    - extension                                              # NIFA-canonical
    - intellectual_merit
  suspicious_terms:
    - innovative                                             # without methodology specifics
    - groundbreaking
    - paradigm_shift
    - significant_results                                    # without effect size
    - we_will_explore                                        # implies no hypothesis
  sentence_shapes_that_work:
    - "We hypothesize that [X mechanism] produces [Y measurable outcome] in [Z agroecosystem], testable via [methodology] with statistical power of [N] to detect effect size [E]."
    - "Prior work (Smith et al. 2023; Jones et al. 2024) demonstrates [phenomenon] in adjacent systems; this proposal extends to [novel context] via [specific methodology]."
  sentence_shapes_that_fail:
    - '"We will explore the relationship between..." (no hypothesis)'
    - '"This innovative approach will yield significant insights..." (suspicious terms)'
    - '"We expect to see effects..." (no methodology, no effect size)'
    - "We will explore the relationship between..." (no hypothesis)
    - "This innovative approach will yield significant insights..." (suspicious terms)
    - "We expect to see effects..." (no methodology, no effect size)

drafting_implications:
  scribe_must_do:
    - "Open §I with falsifiable hypothesis + measurable outcome + methodology, before impact narrative."
    - "Include statistical power analysis (sample size + effect size + alpha + power) in methodology section."
    - "Cite ≥2 peer-reviewed publications establishing prior-art baseline."
    - "Name co-investigators with explicit role + time commitment + letter of collaboration."
    - "Include broader-impacts / extension-outreach plan with audience + format + measurable reach."
    - "Include IRB/IACUC/DMP cross-references when subjects-research or data-generation signals present."
  scribe_must_not_do:
    - "Frame research as 'exploration' without hypothesis."
    - "Use 'innovative' / 'groundbreaking' / 'paradigm-shifting' without specific operational difference."
    - "Skip statistical power analysis for hypothesis-testing designs."
    - "Frame extension/outreach as 'we will publish results' (single-channel = downgrade)."
  section_ordering_notes: |
    Methodology-first §I ordering: hypothesis → design → power analysis →
    prior evidence → broader impacts. Narrative-first ordering is NIFA-suboptimal.

judge_implications:
  scoring_dimensions_to_weight_harder:
    - "Scientific Merit / Methodology Rigor — weight ≥30% (cross-NIFA pattern)"
    - "Investigator Qualifications — weight ≥20%"
    - "Broader Impacts / Extension — weight ≥15%"
  evidence_required_before_high_score:
    - "Scientific Merit ≥4: explicit hypothesis + power analysis + control design"
    - "Qualifications ≥4: prior peer-reviewed publication in sub-discipline"
    - "Broader Impacts ≥4: ≥3 outreach channels + measurable reach"

red_team_probe_seeds:
  - probe: "Does proposed design include statistical power analysis (sample size + effect size + alpha + power)?"
    why_it_matters: "Missing power analysis = single most-common methodology downgrade vector across NIFA."
  - probe: "Is COI declaration complete for all named investigators including off-cycle co-investigators?"
    why_it_matters: "NIFA peer-review panels enforce strict COI; incomplete declaration triggers administrative return."
  - probe: "If human/animal subjects implied, is IRB/IACUC protocol cited (or pending-IRB status with submission timeline)?"
    why_it_matters: "F-USDA-NIFA-IRB-MISSING / IACUC-MISSING are HIGH-severity gates."
  - probe: "Is data-management plan specific (formats, repositories, retention, access) or generic?"
    why_it_matters: "NIFA-DMP increasingly enforced; generic 'follow institutional policies' downgrades."
  - probe: "Are prior peer-reviewed publications cited for both sub-discipline AND methodology?"
    why_it_matters: "Single-criterion citation signals incomplete prior-art grounding."

logician_gate_candidates:
  - gate: F-USDA-NIFA-IRB-MISSING
    failure_condition: "draft.has_human_subjects_signals() == True AND kfr.applicant.irb_protocol_id is None"
    severity: HIGH
    fail_action: WARN_OPERATOR
  - gate: F-USDA-NIFA-IACUC-MISSING
    failure_condition: "draft.has_animal_subjects_signals() == True AND kfr.applicant.iacuc_protocol_id is None"
    severity: HIGH
    fail_action: WARN_OPERATOR
  - gate: F-USDA-NIFA-DMP-MISSING
    failure_condition: "draft.has_data_generation_signals() == True AND kfr.applicant.data_management_plan is None"
    severity: HIGH
    fail_action: WARN_OPERATOR
  - gate: F-USDA-NIFA-COI-INCOMPLETE
    failure_condition: "any(inv.coi_form is None for inv in kfr.applicant.named_investigators)"
    severity: MED
    fail_action: WARN_OPERATOR

source_backing:
  corpus_refs:
    - "<NEEDED — Pillar 2: NIFA strategic framework FY22-26>"
    - "<NEEDED — Pillar 2: AFRI Foundational + Applied Science RFA shapes>"
    - "<NEEDED — Pillar 2: SARE national framework + regional-host model docs>"
    - "<NEEDED — Pillar 2: NIFA peer-review panel composition + COI rules>"
    - "<NEEDED — Pillar 2: NIFA indirect-cost cap guidance per program>"
    - "<NEEDED — Pillar 2: NIFA Data Management Plan policy>"
  confidence: LOW pre-corpus.
  unresolved_questions:
    - "Cross-program indirect-cost cap variance"
    - "Recent NIFA DMP-enforcement rigor"
    - "Peer-review panel composition norms across competitive programs"
```

---

## §1 — What "depth" means for THIS artifact

USDA-NIFA funder-level depth is the **peer-reviewer-academic register substrate** for the NIFA program portfolio — methodology-first drafting, COI/IRB/IACUC/DMP cascade defaults, scientific-merit-weighted scoring. Distinct from USDA-RD's federal-program-officer register on every load-bearing axis.

**Codex same-prompt-with/without test:**
- **Without** — Scribe writes generic federal grant: narrative-first opening, "innovative sustainable agriculture approach," no power analysis. Judge applies generic 12-dimension scoring.
- **With** — Scribe leads §I with falsifiable hypothesis + statistical power analysis + prior peer-reviewed publication. Judge weights Scientific Merit ≥30%, Qualifications ≥20%, Broader Impacts ≥15%. Red Team probes power-analysis adequacy + COI completeness + DMP specificity + IRB/IACUC status. Logician fails closed on IRB/IACUC/DMP missing-when-needed.

Force-multiplier: every USDA-NIFA program (AFRI / SARE / BFRDP / CFP-NIFA) inherits register + cascades + baseline gates automatically.

---

## §2 — Primary sources in scope

| Corpus category | Specific sources | Access path | Estimated count |
|-----------------|------------------|-------------|-----------------|
| `strategic/` | NIFA Strategic Plan FY22-26; AFRI framework | Public NIFA site | 2-3 |
| `regulatory/` | NIFA indirect-cost-cap; DMP policy; biosketch format | Public NIFA + Federal Register | 2-3 |
| `awards/` | FY24 + FY25 NIFA aggregate award rolls; PA-specific totals | USAspending.gov + NIFA CRIS | 2-3 |
| `interviews/` | 0-2 NIFA program-leader conversations (Tier-2/3) | Operator network outreach | 0-2 |
| `guidance/` | Peer-review panel + COI rules; IRB/IACUC compliance | NIFA public guidance | 2-3 |

Case law OUT OF SCOPE.

---

## §3 — Tier classification

| Field | Tier |
|-------|:----:|
| Default | `1` |
| `funder_dialect` | `2` |
| `funder_officer_relationship_notes` | `3` |
| `peer_review_panel_composition_norms` | `1` |

---

## §4 — Refresh cadence

`annual` + `event_triggered` overlay.

---

## §5 — Calibration applicant pair

`food_systems` (CIC-01) × `operating_capacity` (CLC-03), with Research & Evidence (CLC-04) as primary CLC.

---

## §6 — Done definition

`audited` when Pillar-3 single-cycle L-005 audit passes per same discipline as USDA-RD funder depth charter.
`audited` when Pillar-3 single-cycle L-005 audit passes per same discipline as USDA-RD funder gold-standard.

---

## §7 — Operator signature

```yaml
charter_signed_at: <pending_operator_attestation>
charter_signed_by_pubkey: <pending_operator_attestation>
charter_signed_canonical_bytes_sha3_512: <pending_operator_attestation>
charter_ed25519_signature: <pending_operator_attestation>
```

Manual ceremony per `pillar_1_charters/README.md`; signing helper at `pipeline/funder_intelligence/_methodology/sign_charter.py`.

---

## §8 — Out of scope (anti-drift)

- Per-program FY26 RFA + rubric (lives in `programs/USDA-NIFA-<program>-FY26.yaml`)
- Compliance framework internals (lives in `compliance_cascades/`)
- Reviewer-type heuristics (lives in `reviewer_heuristics/peer-reviewer-academic.yaml`)
- Other USDA agencies — separate funder artifacts
- Per-applicant research design / IRB protocol (lives in `orgs/<slug>/`)
- Case law interpretation
