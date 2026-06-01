# FID Artifact Optimization Principles

**Status:** Canonical spec — operator-set 2026-05-18.
**Authority:** Operator directive 2026-05-18 (mid-PR-#33 pivot from compressed-roster Week-1 Pillar-1 authoring).
**Supersedes:** Looser quality-bar implied by the pre-2026-05-18 charter template and §3.1 of the FID research planning doc when those documents conflict with this spec.
**Companion:** `pipeline/funder_intelligence/_templates/depth_charter_template.md` (template; this spec dictates required fields), `pipeline/planning/funder_intelligence_database_research_project_2026-05-16.md` (planning authority for FID overall), `docs/FID_EXPANDED_ROSTER_8_6_3_2026-05-18.md` (roster scope).

---

## §1 — The core thesis

> **What should Scribe, Judge, Red Team, Scout, or Logician do *differently* because this artifact exists?**
>
> **If it doesn't change a runtime decision, it's reference prose, not a strong component.**

Every FID artifact (funder / program / compliance cascade / reviewer type / review stage / charter) must justify itself by naming the runtime decision it changes. Artifacts that read as a well-written encyclopedia entry but never alter a Scribe section choice, a Judge dimension score, a Red Team probe target, a Scout VERIFY check, or a Logician gate predicate are **reference prose** — they may be useful to humans, but they are not FID-grade components and must not be merged into the lattice in that form.

This is the **strong-component bar**. Anything below it is held as DRAFT pending re-authoring against the bar.

### Why this bar exists

Tilth's value to applicants is concentrated in the runtime decisions its seats make — what sections to draft a certain way, what to score how, what to probe, what to fail-closed on. Reference prose duplicates effort that already exists in NOFOs, agency websites, and grantwriter heads. The marginal value of FID is in the **machine-readable, decision-shaped substrate** that lets seats act with funder-specific intelligence at runtime, deterministically and audit-traceably.

### Three anti-patterns this bar rules out

1. **Encyclopedia entries.** "USDA-RD funds rural development under the Consolidated Farm and Rural Development Act of 1972 across three sub-mission areas..." — every grantwriter blog has this. If Scout doesn't change a discovery filter or Scribe doesn't change a section, this content does not earn its place in FID.
2. **Operator-derived essays.** "In my experience, foundation program officers value theory-of-change framing..." — this is reviewer-type heuristic content that belongs in `reviewer_heuristics/foundation-program-officer.yaml`, not in funder artifacts, and only if it surfaces as a Scribe drafting cue or a Red Team probe.
3. **Stub fields with no consumer.** "We will capture `funder_dialect_notes` here." — the field is named but no seat reads it, no gate enforces it, no probe consumes it. That is a future-work TODO, not a strong-component artifact field.

### The runtime-consumer test (mandatory)

Every artifact carries a `runtime_consumer:` block (see §3.6) that names — per seat — which artifact fields the seat reads, at what stage of which pipeline, and what decision the field changes. If the block has `null` for all five seats, the artifact has failed the strong-component bar and is held as DRAFT.

---

## §2 — The three adversarial fields (mandatory on every artifact + every depth charter)

These three blocks are the operationalization of §1. Every artifact YAML AND every Pillar-1 Depth Charter carries them. Charter values are intent-stage (what we expect the artifact to do); artifact values are realized-stage (what the artifact actually does). Pillar-3 extraction must produce artifact values that satisfy the charter's intent or the L-005 audit fails.

### 2.1 `runtime_consumer:` — who reads, when, and what decision changes

```yaml
runtime_consumer:
  scout:
    reads_fields: [<artifact_field_path>, ...]      # e.g., [endpoints.live_check_url, endpoints.synopsis_url]
    stage: DISCOVER | VERIFY | both | not_applicable
    decision_changed: <one-sentence summary of what Scout does differently>
  scribe:
    reads_fields: [<artifact_field_path>, ...]
    stage: scaffold | substance | both | not_applicable
    decision_changed: <one-sentence summary>
  judge:
    reads_fields: [<artifact_field_path>, ...]
    stage: rubric_scoring | cross_check | not_applicable
    decision_changed: <one-sentence summary>
  red_team:
    reads_fields: [<artifact_field_path>, ...]
    stage: probe_generation | probe_target_selection | not_applicable
    decision_changed: <one-sentence summary>
  logician:
    reads_fields: [<artifact_field_path>, ...]
    stage: PRE | POST | COMMIT | not_applicable
    decision_changed: <one-sentence summary of which gate predicates use this artifact>
```

**Rules:**
- At least **one** seat must be active (i.e., not `not_applicable` in `stage`). An artifact that is `not_applicable` to all five seats fails the strong-component bar.
- `reads_fields` must name actual fields in this artifact's YAML (or, for charters, fields the artifact YAML will carry post-extraction). No phantom fields.
- `decision_changed` must be a **concrete behavior change**, not a description. "Scribe knows the funder dialect" fails. "Scribe substitutes `community partner` → `cooperative member` in §III narrative when funder_id == NCBA-CLUSA" passes.

### 2.2 `artifact_must_not_contain:` — anti-drift discipline

```yaml
artifact_must_not_contain:
  - facts belonging to another artifact          # canonical default — keep verbatim
  - applicant-specific claims                    # canonical default — keep verbatim
  - uncited generalizations                      # canonical default — keep verbatim
  - <additional artifact-specific exclusions>    # add as needed
```

The three canonical defaults are non-negotiable. Add artifact-specific exclusions as discovered (e.g., a program artifact might add "compliance framework internals — point to `compliance_cascades/<id>.yaml` instead"). Logician `F-FID-CROSS-ARTIFACT-COUPLING` (HIGH) + `F-FID-FACT-ORPHAN` (P0) gates enforce the first two at runtime; the third is operator-audited at L-005.

### 2.3 `strength_test:` — three concrete questions the artifact must answer

```yaml
strength_test:
  - "Name one concrete drafting decision this artifact changes."
  - "Name one proposal this artifact would reject or downgrade."
  - "Name one Red Team probe this artifact enables."
```

The three canonical questions are mandatory on every artifact + charter. The artifact body (charter §1 prose; artifact YAML's substantive fields) must contain explicit answers to all three. A charter that does not pass all three strength tests is **pre-spec DRAFT** and held pending re-authoring. An artifact that does not pass all three at L-005 audit fails with `READY_TO_LOCK = NO`.

**Example pass for `USDA-RD-RBDG-FY26`** (sketch — fully realized in the gold-standard charter):

- Drafting decision changed: Scribe's match-narrative section must lead with cash match (vs. in-kind) because RBDG NOFO §V.C weights cash-match-leverage 3× in-kind-match-leverage at scoring criterion #3 "leveraging."
- Proposal rejected: Logician `F-RBDG-RURAL-POP-INELIGIBLE` fails closed any applicant whose service-area population exceeds 50,000 per the OMB urban-area-definition lookup (Scribe is never invoked).
- Red Team probe enabled: Red Team probes match-fund authenticity by asking whether each cash-match commitment letter is **unconditional** or **contingent on award**, because contingent matches score 0 under rubric criterion #3 even when nominally on the same dollar value.

### 2.4 Where the three blocks live

- **Pillar-1 Depth Charter** — three blocks in YAML form at a new §A "Adversarial pre-checks" right after the Header, before §1. Charter author writes intent-stage values; operator signs them as part of the charter sign-off.
- **Artifact YAML (`pipeline/funder_intelligence/<family>/<id>.yaml`)** — three blocks at top level, alongside other artifact metadata. Pillar-3 extraction writes realized-stage values.

---

## §3 — YAML field specs per artifact family

All artifact YAMLs share the canonical canonicalization rule (sort_keys=True, separators=(',', ':'), UTF-8, ensure_ascii=False, signature field excluded). All artifacts carry `ed25519_signature` over canonical-JSON-bytes verified against the FID publisher pubkey at `vault_shared/funder_intelligence/publisher_pubkey.signed.yaml`.

### 3.1 Common header (every artifact)

```yaml
artifact_id: <canonical id, e.g., USDA-RD-RBDG-FY26>
artifact_family: funder | program | compliance_cascade | reviewer_type | review_stage
artifact_path: pipeline/funder_intelligence/<family>/<artifact_id>.yaml
schema_version: 1.0                                 # bump on schema-breaking change
lifecycle_status: draft | audited | field_tested | validated
classification_default_tier: 1 | 2 | 3              # per architecture v7.0.10
charter_pointer: pipeline/funder_intelligence/pillar_1_charters/<artifact_id>_charter_v<N>_SIGNED.md
corpus_dir: pipeline/funder_intelligence/_research_corpus/<artifact_id>/
publisher_pubkey_fingerprint: <hex>                 # pinned at white-glove
publisher_pubkey_path: vault_shared/funder_intelligence/publisher_pubkey.signed.yaml
runtime_consumer: { ... }                           # per §2.1 — required
artifact_must_not_contain: [ ... ]                  # per §2.2 — required
strength_test: [ ... ]                              # per §2.3 — required
ed25519_signature: <base64>                         # signature over canonical bytes
canonical_bytes_sha3_512: <hex>                     # hash for audit replay
```

### 3.2 `funder` artifact (`pipeline/funder_intelligence/funders/<funder_id>.yaml`)

```yaml
# Common header per §3.1
# ...
mission_framing:
  one_paragraph_summary: <plain-English; ≤500 chars; cited to corpus>
  corpus_ref: <artifact_id>:<filename>:<page_or_line>
program_roster:                                     # pointers only; no embedded program detail
  - program_id: USDA-RD-RBDG-FY26
    artifact_path: pipeline/funder_intelligence/programs/USDA-RD-RBDG-FY26.yaml
  - ...
compliance_cascade_defaults:                        # pointers to cascade artifacts
  - cascade_id: 2-CFR-200-UG
    activation: always
  - cascade_id: DAVIS-BACON-PREVAILING-WAGE
    activation: when_construction_in_scope
  - ...
funder_dialect:                                     # operator-derived; Tier-2; Scribe reads
  register: federal_program_officer | foundation_program_officer | peer_reviewer_academic | state_program_officer | cooperative_board_peer | <other>
  load_bearing_terms:
    - term: <funder-canonical word>
      preferred_register: <when to use>
      avoid_register: <when not to use>
      corpus_ref: <ref>
  dialect_notes: <bullet list of substantive observations; each carrying corpus_ref>
funder_officer_relationship_notes:                  # Tier-3; never composable; my-eyes-only
  - relationship_id: <opaque token; not the officer's name in shareable contexts>
    notes: <Tier-3 content>
historical_award_patterns_aggregate:                # public; Tier-1; Scout reads
  total_award_volume_fy24: <int dollars>
  total_award_volume_fy25: <int dollars>
  award_count_fy24: <int>
  award_count_fy25: <int>
  geographic_distribution_fy24_25_pa_percent: <float>
  corpus_ref: <ref>
geographic_eligibility:                             # public; Scout DISCOVER filter
  in_scope_geographies: [<list of state codes, regions, or "national">]
  out_of_scope_geographies: [<list>]
  rural_pop_threshold_default: <int or null>
known_failure_modes_at_funder_level:                # Red Team probe seeds
  - failure_mode: <one-line description>
    severity: P0 | HIGH | MED | LOW
    corpus_ref: <ref>
refresh_cadence: annual | quarterly | per_cycle | per_rfa | event_triggered
last_refreshed_at: <UTC ISO-8601>
next_refresh_due_at: <UTC ISO-8601>
```

### 3.3 `program` artifact (`pipeline/funder_intelligence/programs/<program_id>.yaml`)

This is the densest artifact type — it carries machine-parseable structures that Logician, Judge, and Scribe all read at runtime.

```yaml
# Common header per §3.1
# ...
funder_pointer: <funder_id>                         # pointer up to funder artifact
program_summary_one_paragraph: <≤500 chars; cited>
nofo:
  source_url: <Grants.gov synopsis URL or agency posting URL>
  source_pdf_sha256: <hex>                          # corpus-manifest cross-reference
  posted_date: <UTC ISO-8601>
  closing_date: <UTC ISO-8601 or "rolling">
  cycle_status: open | closed | upcoming | rolling
  corpus_ref: <ref>

eligibility_gates:                                  # machine-parseable; Logician reads as PRE-gates
  - gate_id: <ARTIFACT_PREFIX>-<SHORT-NAME>          # e.g., F-RBDG-RURAL-POP-INELIGIBLE
    predicate: <plain-language description>
    machine_check:                                  # Logician deterministic check
      field_in_applicant_context: <kfr field path>
      operator: in | not_in | gte | lte | eq | ne | matches | not_matches
      threshold: <value or array>
    on_fail: REJECT_NO_DRAFT | DOWNGRADE | WARN_OPERATOR
    severity: P0 | HIGH | MED
    corpus_ref: <ref>

disqualifiers:                                      # special class of eligibility_gates with severity=P0 + on_fail=REJECT_NO_DRAFT
  - dealbreaker_id: <ID>
    description: <when this applies>
    machine_check: { ... }
    corpus_ref: <ref>

match_requirements:
  required: true | false
  match_ratio: <e.g., "1:1" or "10_percent_of_grant" or null>
  match_cash_required_min_pct: <float 0-100 or null>
  match_in_kind_allowable: true | false
  match_fund_authenticity_rules:
    - rule: <e.g., "cash match must be unconditional, not contingent on award">
      corpus_ref: <ref>
  match_documentation_required:
    - doc_type: <e.g., "match commitment letter on funder letterhead">
      timing: <when due; with application or post-award>

scoring_rubric:                                     # Judge reads; weighted dimensions
  total_points: <int>
  criteria:
    - criterion_id: <id>
      name: <name from NOFO>
      max_points: <int>
      weight_pct: <float>
      sub_criteria:
        - sub_id: <id>
          name: <sub-name>
          max_points: <int>
          rubric_guidance: <how reviewers score; cited>
          corpus_ref: <ref>
      reviewer_expectation_one_sentence: <what a strong response looks like>
      reviewer_punishment_one_sentence: <what a weak response looks like>
      corpus_ref: <ref>

review_stages:                                      # per D3 enum vocabulary once locked
  - stage_id: screen | score | consensus | <operator-preferred>
    description: <what happens in this stage>
    reviewer_types_active: [<reviewer_type_id>, ...]   # pointers
    time_budget_hours_per_proposal: <float>
    deliverable: <e.g., "pass-to-score-stage" or "1-to-5 numeric rating per criterion">
    corpus_ref: <ref>

required_application_elements:
  - element_id: <id>
    name: <e.g., "Project Narrative", "SF-424", "Match Commitment Letter">
    required: true | conditional
    conditional_on: <if conditional>
    max_pages: <int or null>
    formatting_rules: [<list>]
    section_anchor_in_nofo: <NOFO section reference>
    corpus_ref: <ref>

scout_verify:
  live_check_url: <URL>
  expected_response_indicator: <e.g., "Page returns 200 + contains 'FY26' + closing_date string">
  failure_action: MARK_VERIFICATION_FAILED
  check_cadence: <e.g., "weekly during open cycle">

scribe_section_requirements:                        # Scribe reads at scaffold + substance
  - nofo_section_id: <id>                            # ties to required_application_elements
    drafting_decisions:                              # CONCRETE decisions Scribe makes
      - decision: <e.g., "Lead match-narrative with cash before in-kind">
        rationale_one_sentence: <e.g., "Rubric criterion #3 weights cash 3× in-kind">
        rubric_ref: <criterion_id>
        corpus_ref: <ref>
    forbidden_register_in_this_section:              # dialect anti-patterns specific to this section
      - phrase: <e.g., "innovative" — funder dialect averse>
        prefer_instead: <substitution>
    evidence_requirements:                           # what KFR fields must be cited
      - kfr_field: <kfr path>
        in_paragraph: <which narrative paragraph>

judge_scoring_map:                                  # Judge reads; maps rubric to numeric scores
  - criterion_id: <id>
    judge_question: <one-sentence question Judge asks about the draft>
    score_bands:
      - band: 5
        descriptor: <what a 5-point response shows>
      - band: 4
        descriptor: <...>
      - band: 3
        descriptor: <...>
      - band: 2
        descriptor: <...>
      - band: 1
        descriptor: <...>
      - band: 0
        descriptor: <what makes a 0 — e.g., absent, off-topic, disqualifying>
    tie_breaker_rule: <how Judge resolves between two close bands>

logician_gates:                                     # PRE/POST predicates owned by this artifact
  - gate_id: <F-PROGRAMID-NAME>
    family: F-FID-* | F-PROGRAM-SPECIFIC
    when: PRE | POST | COMMIT
    severity: P0 | HIGH | MED
    predicate_python: <python expression body — read for review at L-005>
    fail_action: REJECT_NO_DRAFT | DOWNGRADE | WARN_OPERATOR
    corpus_ref: <ref>

red_team_probes:                                    # Red Team reads
  - probe_id: <ID>
    probe_question: <one-sentence adversarial question Red Team asks about draft>
    targets_rubric_criterion: <criterion_id or null>
    targets_failure_mode: <failure_mode reference>
    score_impact_if_fails: <int point reduction or "P0 fail">
    corpus_ref: <ref>

post_award_obligations:
  reporting_cadence: <e.g., "annual">
  reporting_deliverables:
    - deliverable_id: <id>
      due_at_each_cycle: <relative due date>
      content_summary: <what's reported>
  beneficiary_metric_tracking_required: true | false
  data_collector_v0_2_inputs:                       # forward-pointing: which fields Data Collector will gather
    - metric: <e.g., "small businesses assisted">
      operationalization: <how counted>
  audit_obligations: <e.g., "Single Audit when aggregate federal awards ≥ $750K">

known_failure_modes_from_prior_cycles:              # historical lessons; Red Team + Judge consume
  - cycle: FY24 | FY25
    failure: <one-line>
    severity: P0 | HIGH | MED
    corpus_ref: <ref>

historical_award_patterns:                          # Scout reads
  award_count_prior_cycle: <int>
  award_count_two_cycles_ago: <int>
  median_award_dollars: <int>
  award_size_range: [<min>, <max>]
  pa_specific_award_count_recent: <int>
  corpus_ref: <ref>

refresh_cadence: per_cycle                           # programs default per_cycle
last_refreshed_at: <UTC ISO-8601>
next_refresh_due_at: <UTC ISO-8601>
```

### 3.4 `compliance_cascade` artifact (`pipeline/funder_intelligence/compliance_cascades/<framework_id>.yaml`)

```yaml
# Common header per §3.1
# ...
framework_short_name: <e.g., "2 CFR 200" or "Davis-Bacon">
statutory_authority:
  - cite: <e.g., "2 CFR Part 200">
    authority_type: regulation | statute | OMB_guidance | federal_register_notice
    corpus_ref: <ref>
trigger_conditions:                                 # when does this cascade fire?
  - trigger_id: <id>
    description: <e.g., "any federal grant ≥ $0 — always active">
    machine_check:
      field_in_program_context: <field path>
      operator: <op>
      threshold: <value>
mandatory_gates:                                    # Logician reads
  - gate_id: <F-COMPLIANCE-id>
    when: PRE | POST | COMMIT
    severity: P0 | HIGH
    predicate_python: <expression body>
    fail_action: REJECT_NO_DRAFT | DOWNGRADE | WARN_OPERATOR
    corpus_ref: <ref>
failure_modes:                                      # Red Team consumes
  - failure_id: <id>
    description: <e.g., "Sub-recipient monitoring not documented = Single Audit finding">
    detection_signal_in_application: <what Red Team probes for>
    corpus_ref: <ref>
audit_obligations:
  audit_type: <Single Audit | program audit | compliance review>
  triggered_when: <condition>
  documentation_required: [<list>]
reporting_obligations:
  cadence: <annual | quarterly | per_event>
  deliverables: [<list>]
refresh_cadence: annual                              # cascades default annual
```

### 3.5 `reviewer_type` artifact (`pipeline/funder_intelligence/reviewer_heuristics/<reviewer_type_id>.yaml`)

**Authored in the parallel reviewer-types-first workstream. Spec included here for completeness; concrete content authoring is out of scope for this PR / this session.**

```yaml
# Common header per §3.1
# ...
reviewer_type_label: <e.g., "federal_program_officer">
typical_role_at_funder: <e.g., "USDA-RD state office staff or program leadership">
time_budget_hours_per_proposal: <float>
participates_in_review_stages: [<stage_id>, ...]    # ties to review_stages enum once D3 locks
top_heuristics:                                     # Scribe reads as drafting cues
  - heuristic_id: <id>
    one_line_pattern: <e.g., "Punishes vague match-fund commitments">
    drafting_implication_for_scribe: <one-sentence cue>
    provenance: operator_interview | public_debrief | NOFO_cited_review_guidance | other
    provenance_corpus_ref: <ref>
common_punishments:                                 # Red Team probe seeds
  - punishment_id: <id>
    description: <what reviewer downgrades>
    score_impact: <points lost>
    corpus_ref: <ref>
common_rewards:                                     # Scribe positive-pattern cues
  - reward_id: <id>
    description: <what reviewer upgrades>
    score_impact: <points gained>
    corpus_ref: <ref>
dialect_cues:                                       # language register signals
  - cue: <word/phrase>
    register_effect: positive | negative | neutral
    corpus_ref: <ref>
denial_feedback_patterns:                           # synthesized from declined-application debriefs
  - pattern_id: <id>
    one_line: <description>
    operationalization_for_scribe_or_judge: <how Tilth uses this>
    corpus_ref: <ref>
refresh_cadence: annual                              # reviewer types default annual
```

### 3.6 `review_stage` artifact (DEFERRED to Phase 2 spike per roster doc; spec included here)

```yaml
# Common header per §3.1
# ...
stage_label: screen | score | consensus | <operator-preferred>
stage_purpose_one_sentence: <e.g., "Eliminate admin-incomplete + ineligible applications before scoring">
typical_reviewer_types_active: [<reviewer_type_id>, ...]
typical_time_budget_hours_per_proposal: <float>
deliverable_from_stage: <e.g., "pass/fail with note OR 1-to-5 rating per rubric criterion">
cross_funder_substance:                              # the test from the Phase-2 spike — what's GENUINELY shared
  - substance_id: <id>
    one_line: <e.g., "SAM.gov registration status check is universal at screen stage">
    applies_to_funder_kinds: [federal | foundation | state | cdfi | all]
    operationalization: <how Tilth uses this>
    corpus_ref: <ref>
funder_specific_footnotes:                           # if mostly funder-specific, primitive is weak
  - funder_id: <id>
    note: <funder-specific exception>
```

**The Phase-2 spike test:** if the body of `cross_funder_substance:` is ≤1 page of substance across federal + foundation + state + CDFI, drop the primitive; if 3+ pages, formalize. See `docs/FID_EXPANDED_ROSTER_8_6_3_2026-05-18.md` §"Deferred to Phase 2 research".

### 3.7 `depth_charter` (Pillar-1 charter; markdown not YAML)

The charter is markdown for human readability + operator sign-off ergonomics. The three adversarial blocks (§2) are embedded as YAML code-fences inside §A "Adversarial pre-checks". See `pipeline/funder_intelligence/_templates/depth_charter_template.md` for the canonical template; this spec dictates the content of §A.

---

## §4 — Scribe / Judge / Red Team / Scout / Logician interaction contract

How seats USE the artifacts at runtime.

### 4.1 Scout

- **DISCOVER:** reads `funder.geographic_eligibility` + `funder.program_roster` + `program.cycle_status` to filter raw radar feeds.
- **VERIFY:** reads `program.scout_verify.live_check_url` + `program.scout_verify.expected_response_indicator` to check that the program is still open before elevating opportunities to CRITICAL fit.
- Decision changed by FID: opportunities that would have been elevated naively get downgraded if VERIFY fails.

### 4.2 Scribe

- **Scaffold stage:** reads `program.required_application_elements` (section structure) + `program.scribe_section_requirements[].drafting_decisions[]` (section-specific decisions) + `funder.funder_dialect.register` (register).
- **Substance stage:** reads `program.scribe_section_requirements[].evidence_requirements[]` (which KFR fields to cite where) + `reviewer_type.top_heuristics[].drafting_implication_for_scribe` (drafting cues).
- Decision changed by FID: section ordering, match-narrative ordering, evidence placement, register substitution choices are all funder-+program-+reviewer-specific rather than generic.

### 4.3 Judge

- Reads `program.judge_scoring_map[]` to map draft sections → numeric scores per rubric criterion.
- Reads `program.scoring_rubric.criteria[].weight_pct` to weight scores.
- Reads `program.known_failure_modes_from_prior_cycles[]` to cross-check whether the draft repeats a known-fail pattern.
- Decision changed by FID: scoring is mechanically tied to the funder's actual rubric weights instead of Judge's generic 12-dimension evaluation.

### 4.4 Red Team

- Reads `program.red_team_probes[]` to enumerate probes specific to this program.
- Reads `compliance_cascade.failure_modes[]` for cross-cutting cascade probes.
- Reads `reviewer_type.common_punishments[]` for reviewer-type-specific probes.
- Decision changed by FID: probes are funder-specific (not generic adversarial), so Red Team finds the actual failure modes this funder punishes.

### 4.5 Logician

- Reads `program.eligibility_gates[].machine_check` as PRE-cycle predicates.
- Reads `program.disqualifiers[].machine_check` as PRE-cycle predicates with `severity=P0`.
- Reads `compliance_cascade.mandatory_gates[].predicate_python` as PRE/POST/COMMIT predicates.
- Reads `program.logician_gates[].predicate_python` for program-specific gates.
- Decision changed by FID: deterministic fail-closed gates are funder-specific, applicant-context-aware, and Cedar/Python-enforced — not advisory prose.

---

## §5 — How to read this spec when authoring a charter or artifact

1. Read §1 (the bar).
2. Read §2 (the three adversarial blocks).
3. Read the family-specific subsection of §3 for your artifact's family.
4. Author the charter (markdown) per `pipeline/funder_intelligence/_templates/depth_charter_template.md`, with §A populated against §2.
5. Pass the strength_test by writing concrete content for all three §2.3 questions in §1 of the charter.
6. At Pillar-3 extraction time, populate the artifact YAML per §3.<family>; populate `runtime_consumer:` + `artifact_must_not_contain:` + `strength_test:` at the top level; verify Pillar-3 output satisfies the charter's §A intent.

The gold-standard example is `pipeline/funder_intelligence/pillar_1_charters/USDA-RD-RBDG-FY26_charter_v0_DRAFT.md` (re-authored 2026-05-18 as the spec-anchor; Status: pre-spec DRAFT only for the OTHER 13 charters in the Week-1 roster).

---

## §6 — What gets retired by this spec

- The looser Pillar-1 template wording at `_templates/depth_charter_template.md` (pre-2026-05-18) that did not require the three adversarial blocks — superseded by template update committed alongside this spec.
- Any prior charter that does not pass the three strength_test questions concretely — marked as pre-spec DRAFT and held for re-authoring.
- Reference-prose-only artifact content patterns that do not name a runtime decision — disallowed at L-005 audit; Pillar-3 extraction must produce decision-shaped output or fail closed.

---

## §7 — Cross-references

- Roster scope: `docs/FID_EXPANDED_ROSTER_8_6_3_2026-05-18.md`
- FID research planning: `pipeline/planning/funder_intelligence_database_research_project_2026-05-16.md`
- FID lattice README: `pipeline/funder_intelligence/README.md`
- Depth charter template (updated to match this spec): `pipeline/funder_intelligence/_templates/depth_charter_template.md`
- Gold-standard charter (RBDG): `pipeline/funder_intelligence/pillar_1_charters/USDA-RD-RBDG-FY26_charter_v0_DRAFT.md`
- F-FID-* failure-code family (forward-declared in planning doc §2.2): lands at `§4 v2.x.z` follow-on amendment when first artifact LOCKs
- Architecture v7.0.10 three-posture routing (classification register that gates seat cloud-vs-local routing): `pipeline/architecture/v0.1/architecture_v7_0_10_amendment.md`
- Reviewer-types-first parallel workstream (concrete reviewer_type artifact authoring): `docs/FID_PHASE_1_PRE_KICKOFF_BRIEF_2026-05-18.md` + handoff at `pipeline/handoffs/` (verify path)
