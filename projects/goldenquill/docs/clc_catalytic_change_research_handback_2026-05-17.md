# TILTH-CLC-02 Catalytic Change — Research Handback

**Filed:** 2026-05-17
**Workspace:** `/Users/goldenquill/Downloads/GoldenQuill/`
**Run:** Run 2 of operator's controlled-batch sequence (Phase 4 CLC handbacks; 2 of 8 — dispatched in parallel with 7 sibling CLC handbacks).
**Card:** `pipeline/cards/CLC/catalytic_change.yaml` (Wave 2 LOCKed 2026-05-16 row 256; SHA-256 `15fb2c2c3f9517d5b693fb9b2438bb1f2a5457ce269f5a78162558130c60f02f`; signed `2026-05-16T16:00:00Z`; Track shape: SINGLE-TRACK / oneOf branch 1).
**Authority chain:** master prompt `docs/cic_clc_unified_master_prompt_2026-05-17.md` §2 (per-card output shape) + plan `docs/cic_clc_unified_research_plan_2026-05-17.md` §2.2 (priority vectors) + Run 1 priors at `docs/card_system_deep_research_2026-05-17/` (binding) + sibling reference handback `docs/cic_food_systems_research_handback_2026-05-17.md` (shape model).
**Run 1 priors folded in:**
- All 14 cards on disk are `draft_status: "signed"` (P0-3 / Run 1 Phase 1 §3.2 — no normalization needed; master prompt §5 stale).
- §18 v1.2 dialect_routing_table re-keying LOCKed-but-not-applied (P0-1 / cards-ceremony pending). CLC cards do NOT carry `dialect_routing_table` (that lives on CICs) so this card is not directly bottlenecked, but cross-card runtime register selection IS bottlenecked.
- F-CARDS-COUPLING-VIOLATION-EXTENSION predicate body raises `NotImplementedError` at runtime (L1-F3 / P1-1) — value-position regex enforcement is spec-only today; manual scan per master prompt §2 item 2 below.
- Legacy phrase `[Cc]ustomer [Ii]nformation` defense-in-depth check.
- Operator v2.1 Law-5 split on `common_funders_observed`: this CLC card has NO `common_funders_observed` top-level field on disk (verified at §2.4 below) — a different posture from food_systems (CIC) which carries the empty-list + `_research_metadata.draft_funder_candidates_pending_operator_engagement_confirmation` pattern. Surface the cross-axis posture variance.
- Operator reframe: "first unit / unlocked" — aggressive content improvements OK to recommend; re-signing ceremony cost acceptable.

---

## §1. Card Impact Thesis

`catalytic_change` (TILTH-CLC-02) is the CLC card that should cause Tilth to **distinguish real catalytic / systems-change / innovation funding from buzzword-heavy "transformation" language** at runtime — by demanding, at intake and at draft, a leverage point, an explicit mechanism-bearing theory of change, a learning agenda, role-bearing partnerships, a replication pathway, timing alignment, and a follow-on capital plan. It is the funder-side underwriting logic that applies anywhere the *opportunity* is foundation systems-change / federal innovation-stage-gate / climate-transition / catalytic-capital flavored — orthogonal to applicant identity (a food-systems coop, an educator nonprofit, a public agency, an arts org, or an ecosystem intermediary can each route to a CLC-02 opportunity at runtime).

What this card should *cause Tilth to do differently* relative to a CLC-naive baseline:

1. **Scout** — when an opportunity contains "transform," "systems change," "catalytic," "innovation prize," "100&Change-like," "Convergence Accelerator," "ARPA-E concept paper," "EIR Early/Mid/Expansion," or "Build to Scale Venture/Capital Challenge" framing, surface CLC-02 underwriting-logic priors (twelve underwriting_criteria + thirteen evidence_weights) into the candidate-fit packet. Do NOT match on "innovative" as an adjective alone (red flag `unsupported_innovation_claim`).
2. **Scribe** — under CLC-02, force section structure that includes (a) Theory of Change with named assumptions + falsifiability marker, (b) Systems Context / leverage-point identification, (c) Innovation / Novelty positioned against prior art, (d) Learning Agenda with named research questions, (e) Partnerships with role clarity (NOT generic letters of support), (f) Evaluation Plan with named evaluator engaged pre-submission for federal innovation programs, (g) Sustainability / Follow-On Capital naming specific funders / programs / revenue streams, (h) Scale / Replication Pathway with conditions and replication math.
3. **Scribe dialect-switch** — code-switch between *foundation systems-change* register (mission-fit / leverage / theory-of-change mechanism / learning agenda dominate) and *federal innovation stage-gate* register (technical merit / broader impacts / commercialization plausibility / independent-evaluator engagement dominate). The `dialect_split_note` at `reviewer_profile_typical.dialect_split_note` (line 360) is the load-bearing prose; Scribe must consult it.
4. **Judge** — score against the funder's published rubric where one exists (MacArthur 100&Change four-criterion is canonical; NSF Merit Review Intellectual Merit + Broader Impacts; ARPA-E Stage Gate; USDA AFRI five-criterion; EDA Build to Scale four-dimension; IES EIR five-criterion). Recognize that most foundations DO NOT publish per-criterion weights — capture the 4-6 criterion structural pattern without false-precision numeric claims.
5. **Red Team** — fire all twelve red-flag probes (`wishlist_theory_of_change`, `no_identified_leverage_point`, `unsupported_innovation_claim`, `no_learning_agenda`, `no_replication_pathway`, `role_less_partnerships`, `diffuse_benefits`, `success_metrics_not_tied_to_systems_change`, `no_follow_on_capital_strategy`, `mission_mismatch_with_funder`, `evaluation_added_late`, `scale_claims_arithmetically_implausible`). Surface the load-bearing probes (`wishlist_theory_of_change`, `no_identified_leverage_point`, `unsupported_innovation_claim`, `role_less_partnerships`, `no_follow_on_capital_strategy`) early in the cycle.
6. **Logician** — enforce compliance gates (2 CFR 200 + §200.344 closeout for federal; Bayh-Dole iEdison for federal IP-bearing innovation; ARPA-E IP retention beyond Bayh-Dole; 42 CFR 50 Subpart F FCOI for PHS-funded; IRB / 45 CFR 46 for human-subjects innovation; NSF DMP / NIH DMS Policy 2023). Admin-risk vocabulary (`systems change`, `transformative`, `disruptive innovation`, `climate transition`, `energy transition`, `equity-centered design`, `centering community`, `innovation`, `demonstration`, `scalability`, `leverage`, `ecosystem`, `field building`, `catalytic` — the 14 CLC-02-scoped entries) is routed to workspace-wide `admin_risk_register.yaml` v2.3 follow-on per the Cycle-2 fix-in-place precedent.
7. **Archivist / Report Generator (v0.2)** — extract ten commitment types from awarded CLC-02 proposals (pilot_milestone_completed / learning_product_released / convening_held / model_refinement_completed / dissemination_metric / policy_or_market_engagement / replication_inquiry / follow_on_funding_secured / partnership_milestone / evaluation_finding) into `proposal_commitments.yaml` under `catalytic_change_commitments`.

The runtime-behavior delta relative to a CLC-naive baseline is **mechanism-bearing theory of change + leverage-point specificity + learning-agenda explicitness + role-bearing partnerships + follow-on capital plausibility** — and a dialect that switches between foundation and federal-innovation reviewer populations cleanly. The card is currently strong on (1), (2), (4), (5), (7); (3) is bottlenecked on the §18 v1.2 cards-ceremony for cross-card dialect routing; (6) is partially complete (admin-risk migration to workspace register is staged but not yet dispatched).

---

## §2. Current State Audit

### §2.1 What is strong now

- **Twelve underwriting_criteria with named criteria + descriptions + source citations** (lines 30–89). Every criterion carries a source_citation, ranging from canonical foundation sources (MacArthur 100&Change, Ford BUILD, FSG Six Conditions of Systems Change, Rockefeller catalytic-capital, Skoll) to canonical federal-innovation sources (NSF Convergence Accelerator, ARPA-E, IES EIR). The set covers the two reviewer populations (foundation + federal-innovation) explicitly.
- **Six scoring_weight_patterns** capturing structural anatomy across (a) generic foundation innovation/catalytic four-criterion (Meaningful / Verifiable / Durable / Feasible — anonymized per Phase F Tier-1 2026-05-16 cleanup), (b) NSF Merit Review two-criterion-with-sub-elements, (c) ARPA-E Stage Gate, (d) USDA AFRI five-criterion, (e) EDA Build to Scale four-dimension, (f) IES EIR five-criterion. Qualitative-only weight tier per OQ-6. The note on EDA Build to Scale at line 144 explicitly disclaims the structural-pattern-vs-FOA-actual variance.
- **Thirteen evidence_weights** (lines 159–213) covering explicit_theory_of_change (HIGH), systems_map (HIGH), pilot_or_preliminary_results (HIGH), partner_commitment_letters_with_role_clarity (HIGH), learning_agenda (HIGH), replication_pathway (MEDIUM with stage-conditional rationale), leverage_or_follow_on_capital_plan (HIGH), baseline_metrics (MEDIUM), evaluation_partner (HIGH for federal, MEDIUM for foundation — note text disambiguates), intellectual_property_or_openness_posture (MEDIUM), dissemination_plan (MEDIUM). All carry source_citation. The single-enum HIGH/MEDIUM/LOW discipline is honored throughout (the Cycle-2 fix-in-place collapsed an attempted compound `MEDIUM_EARLY_HIGH_LATER` to canonical `MEDIUM` with stage escalation captured in `rationale` prose — lesson for Phase 4 fold-in refusal (c)).
- **Common application forms + portals** are accurate and current to 2026-05-15: Research.gov / SF-424 R&R / ARPA-E Concept Paper + Full Application / Foundation LOI / Fluxx / Submittable / Foundant / Common Grant Application. The Fluxx ↔ MacArthur+Rockefeller+RWJF / Submittable ↔ Skoll / Foundant ↔ mid-market mapping reflects the 2026 platform reality.
- **Eleven narrative_section_patterns with typical_word_count + source_citation + extensive notes.** The Theory of Change section note at line 266 is load-bearing — "the single most reviewer-weighted section in catalytic-funder rubrics. Scribe must demand at least one named assumption at each step and a falsifiability marker." This is the runtime-behavior contract between card and Scribe.
- **reviewer_profile_typical with eight reviewer_types + eight reviewer_priorities + ten common_red_flags_from_reviewer_pov + a `dialect_split_note`** (line 360). The dialect_split_note is the canonical CLC-02 dialect-switching prose: foundation program officers vs. federal innovation panel reviewers prioritize different sub-criteria. Scribe must consult it.
- **Twelve common_red_flags with severity + red_team_probe + source_citation.** Eight HIGH-severity, four MEDIUM — calibrated correctly. The probes (e.g., "Walk the chain from inputs to impact and name one assumption at each step. Which assumption is most fragile, and what would invalidate it?") are operationally specific, not generic.
- **Reporting + compliance discipline** covers 2 CFR 200, §200.344 closeout, Bayh-Dole / iEdison, ARPA-E IP retention beyond Bayh-Dole, 42 CFR 50 Subpart F FCOI, IRB / 45 CFR 46, NSF DMP / NIH DMS Policy 2023. Lines 499–562. The ARPA-E retention note (line 522) is operationally important and rarely captured well in generic federal-research compliance docs.
- **commitment_tracking_pattern with ten typical_commitments_extracted** + a `paragraph_2_coverage_note` (line 592) that explicitly maps the ten commitment types to the §18.10 paragraph-2 evidence-weight categories. This is the v0.2 Report Generator feed schema.
- **Sixteen primary_sources with verbatim quotes + access_date.** Sources include MacArthur 100&Change, Ford BUILD, NSF Convergence Accelerator, NSF Merit Review, ARPA-E program announcements + IP, IES EIR, USDA AFRI, EDA Build to Scale, Rockefeller catalytic capital, Skoll, Kresge LIFT, FSG Six Conditions, Hewlett, 2 CFR Part 200, NIH FCOI. Verbatim quotes are research-draft paraphrases pinned by URL + access_date per Cycle-2 closure (the OQ-4 verbatim-quote cap of ≤2 sentences per quote is honored throughout).
- **Lifecycle truth.** `draft_status: signed`, `review_status: passed`, `cross_family_thesis_status: passed`, `signature_status: signed`, `runtime_load_status: loaded`, `runtime_loadable: true`, `content_hash: sha256:15fb2c2c…0c60f02f`, `signed_at: 2026-05-16T16:00:00Z`, `signed_by: founder`, `lock_history_row: 256`, `lock_timestamp_utc: 2026-05-16T16:00:00Z`. Fully consistent with architecture v7.0.11 §1.5 production-load requirements.
- **Cycle-2 audit trail in lifecycle block.** Lines 646–660 carry the Cycle-2 fix-in-place narrative: 3 NEW schema-violation findings from Cycle 1 cycle-fix, dispositioned (a) replication_pathway.weight enum normalization, (b) primary_sources[*].quote_type field removal, (c) admin_risk_term_register block removal entirely. This is the on-disk reference for §18.11 v1.1 Phase 4 fold-in discipline (alongside CLC-06 credit_underwriting and CLC-08 shared_assets per OD-D).

### §2.2 What is stale, ambiguous, over-broad, too local, too federal, or under-sourced

- **No top-level `common_funders_observed` field at all (different from food_systems posture).** Per the operator's v2.1 Law-5 reconciliation pattern, food_systems carries `common_funders_observed: []` (empty list) AT TOP LEVEL plus `_research_metadata.draft_funder_candidates_pending_operator_engagement_confirmation:` with subagent-populated candidates. `catalytic_change` simply does not carry the top-level field on disk. The CLC schema declares `common_funders_observed` as optional (lines 98–175 of `card_clc.schema.json` — schema property, not in the required list). The two postures (absent vs empty-list) are both technically Law-5-compliant, but the **cross-axis posture variance is a normalization candidate** — operator decides whether CLC cards should mirror the CIC empty-list-plus-research-metadata pattern, or whether absent-from-disk is the canonical CLC pattern. Surface as P0 decision.
- **No `_research_metadata.draft_funder_candidates_pending_operator_engagement_confirmation` block.** This is the corollary of the prior bullet — there's no parking lot for subagent-populated funder candidates pending operator engagement. The card's `_research_metadata.priors_consulted` lists six sources and `primary_sources` lists sixteen sources, but neither carries draft funder candidates. Per OD-A v2.4 / Law-5 split: known funders that Scout might surface (MacArthur 100&Change, Ford BUILD, NSF Convergence Accelerator, ARPA-E, IES EIR, Rockefeller catalytic-capital, Skoll, Kresge LIFT, Hewlett, etc.) all already appear in `primary_sources` as citation anchors — but they are anchors for the underwriting logic, not "common funders observed by us." Operator decides whether to seed a draft_funder_candidates_pending list parallel to food_systems.
- **MacArthur 100&Change four-criterion rubric anonymization (Phase F Tier-1 2026-05-16) made the canonical pattern slightly less locatable.** Line 101 generic descriptor "Foundation innovation/catalytic rubric — typical anatomy across major national foundation innovation portfolios" loses pointer specificity. The source_citation URL (https://www.macfound.org/programs/100change/) and the note prose at line 109 preserve the anchor — but a reader scanning `scoring_weight_patterns` quickly might miss the MacArthur reference. Recommendation: keep the anonymization (operator-approved per Law-5 surface) but add a brief inline note tag in `rubric_example` like "(MacArthur 100&Change is the canonical pattern source per the cited URL)." NOT a defect — operator-approved posture.
- **Stage-2+ multi-Tilth fleet horizon.** The card cites foundation rubrics under the operator-confirmed-engagement-only Law-5 discipline. Once Stage 2 lands (twelve Tilths), per-foundation win-rate observations become a legitimate `_research_metadata.lessons_observed` substrate. Today (Stage 1), the qualitative-only posture per OQ-6 is correct. Surface the Stage-2-flip as a v0.2 → v1 Wave-3 horizon question (not a P0-P1-P2 finding on this card).
- **EDA Build to Scale rubric note (line 144) flags official scoring criteria vary by NOFO publication year.** Operationally correct disclaimer — but Scribe needs to know to consult the active NOFO. Recommend a top-of-section note at `scoring_weight_patterns` explicitly explaining that the six rows capture STRUCTURAL patterns observed; per-cycle rubric criteria + weights must be re-verified per active RFA/NOFO. **Per master prompt rule 6 (Phase 4 fold-in discipline)**: adding a structured sub-field on canonical entries is refusal (a) — surface as §18 v1.x amendment candidate; do NOT bake into card body. A free-text inline note in the existing `note` keys is acceptable.
- **IES EIR tier-conditional evidence requirements.** Note at line 154 says "Expansion-tier requires moderate evidence + RCT + independent evaluator. All tiers require evaluation plan with named evaluator before award." The tier-conditional escalation is captured in prose; runtime Scribe needs to surface tier-specific evidence demands. Stage-conditional fields don't currently exist in the schema; route as v0.2 amendment candidate (refusal (a)).
- **`baseline_metrics` weight: MEDIUM** (line 196). The rationale prose at line 197 says "Without baseline, outcome claims are uninterpretable. Catalytic funders weight 'why now' framing heavily." This is a HIGH-evidence-weight signal masquerading as MEDIUM. The reason it's MEDIUM is that for early-stage demonstrations baseline may not exist yet; for later-stage demonstrations it MUST exist. Same stage-conditional pattern as `replication_pathway`. Recommend rationale tightening to clarify: "MEDIUM for early-phase catalytic capital; HIGH for mid/late-phase where the demonstration claims outcome shift." Not a re-enum (per refusal (c) compound enum ban).
- **`scale_of_leverage` criterion (line 81) source_citation = Skoll only.** Skoll's framing emphasizes social-entrepreneur-scale leverage. Federal innovation reviewers (ARPA-E, IES EIR) interpret "scale" differently (technological / commercialization / scientific). Recommend dual-citation: Skoll for foundation-side framing + ARPA-E or NSF Convergence for federal-innovation-side framing.
- **`replication_pathway` evidence weight MEDIUM rationale handles the stage-conditional correctly (line 187) but the underwriting_criteria.replication_pathway at line 51 doesn't acknowledge the stage variance.** Recommend tightening the criterion-description prose to mirror the evidence-weight rationale's stage-conditional framing.
- **`timing_and_window_alignment` (line 76) source_citation is blueprint-internal** (`blueprint:section_18_card_system.md#§18.10-CLC-02`). The criterion is operationally load-bearing per the prose at line 77 ("Catalytic funders weight timing heavily; same intervention 2 years earlier or later may not score") — but the source anchor is internal. Recommend external citation candidate: Bridgespan Group "Big Bets" framework OR FSG / Stanford Social Innovation Review on policy-window timing. Not a defect — internal blueprint citation is honored per schema — but adds robustness.
- **`partnership_strength_and_role_clarity` (line 61) source_citation = Ford BUILD only.** Ford BUILD frames role-clarity for *capacity-building* partnerships. NSF Convergence Accelerator phase-1-to-phase-2 transition requires *integrated team* partnership framing. Recommend dual-citation: Ford BUILD + NSF Convergence two-phase team-formation framework.
- **The 14 admin-risk-term entries removed at Cycle-2 fix-in-place (per comment block lines 596–620) migrate to workspace-wide admin_risk_register.yaml v2.3 — but the migration dispatch is NOT yet recorded as fired.** The Cycle-2 closure narrative at line 615 says "follow-on dispatch." Operator decides whether to fire the migration as part of the §18 v1.2 + §18.6 v2 + §4 v2.x.7 compound cards-ceremony, or as a standalone admin-risk-register-only ceremony. Cross-CLC normalization point: catalytic_change contributed 13 entries (joint-highest with credit_underwriting at 15); cooperative + operating_capacity + shared_assets share vocabulary like "systems change," "transformative," "ecosystem," "field building" — cross-CLC normalization candidate per OD-A v2.4 pattern.
- **`primary_sources` URL verification is dated `access_date: 2026-05-15`.** Annual re-verification against Internet Archive snapshot is the §18.11 discipline. Recommend next Phase 4-CLC pass confirm Wayback snapshots of all sixteen URLs. The Kresge LIFT URL (https://kresge.org/initiative/leadership-and-infrastructure-funding-team-lift/) at line 749 carries the highest staleness risk because Kresge has restructured its initiative URLs multiple times in 2024–2025.
- **No `fcoi_disclosure` evidence_weight or red_flag entry.** compliance_obligations[3] at line 524 carries FCOI as a federal compliance framework; but reviewers (federal-innovation panels) treat FCOI disclosure quality as a soft scoring signal. Recommend adding `fcoi_disclosure_completeness` as a MEDIUM evidence_weight for federal-routed proposals. Operator decides per cross-cutting v0.2 fold-in.
- **No `partnership_letters_freshness_window` per evidence_weight.** food_systems carries `freshness_tolerance_days` on every evidence_signal (180 / 365 / 730 days). The catalytic_change card carries no freshness tolerance per evidence_weights — meaning Scribe doesn't surface stale-LOI risk during draft. Add per-evidence-weight freshness tolerances. **Refusal (a) check:** this is a structured sub-field expansion on canonical evidence_weights entries — IS refusal (a) territory. Surface as §18 v1.x amendment candidate (do NOT bake into card body silently). Cross-card normalization opportunity if all 8 CLC cards adopt the same evidence_weights freshness sub-field.

### §2.3 Lifecycle / signature / schema concerns

- **`draft_status: signed`.** No normalization needed (per Run 1 P0-3; master prompt §5 stale claim retired).
- **Header comment (lines 1–17) is current.** Line 5 says "SIGNED — runtime-loadable; lifecycle truth enforced by loader preflight." Aligns with on-disk lifecycle block. No header-comment drift (different from food_systems P1-4 where header comment said "Lifecycle: draft" while disk said "signed").
- **`dialect_routing_table` not present (correct — CICs carry this, not CLCs per §18 v1.2 amendment).** No schema mismatch surface on this card directly.
- **`_research_metadata.priors_consulted` references** `assets/cards/capital_logic/Capital Logic Cards.png` (line 670) and `CLAUDE.md` (line 678). Both are exempt subtree references and pass the value-position regex scan (see §2.4 below).
- **Cycle-2 fix-in-place precedent.** Lines 643–660 lifecycle comment block documents the three Cycle-2 schema-violation fixes (replication_pathway.weight enum normalization, primary_sources[*].quote_type field removal, admin_risk_term_register block removal). This is the on-disk reference for the §18.11 v1.1 Phase 4 fold-in discipline alongside CLC-06 credit_underwriting and CLC-08 shared_assets. Future researchers should consult this lifecycle comment narrative as the authoritative example of fold-in discipline.
- **Lock-history housekeeping fields present.** `lifecycle.lock_history_row: 256` + `lifecycle.lock_timestamp_utc: 2026-05-16T16:00:00Z` + `lifecycle.supersession_lock_history_row` absent. Per Run 1 Patch E1 cross-card discussion: these fields aren't in `models.py.Lifecycle` and the canonical-bytes-exclusion set doesn't exclude them — any future supersession-re-sign that updates `lock_history_row` will invalidate `content_hash` and force re-sign. Same disposition as food_systems: operator decides on the cross-card fix (graduate into models.py or remove from schema). Out of scope for this card alone.

### §2.4 Coupling-discipline self-audit (per master prompt §2 item 2 + Run 1 enforcement-context guidance L1-F3)

**Method.** Manual value-position scan over the full card body using the regex set from `pipeline/blueprint/v0.1/section_04_v2_x_7_card_coupling_value_position_amendment.md:108-120`:

```python
_VALUE_POSITION_PATTERNS = (
    ("value_literal_cic_slug", re.compile(r"TILTH-CIC-\d{2}")),
    ("value_literal_clc_slug", re.compile(r"TILTH-CLC-\d{2}")),
    ("value_literal_capital_logic_phrase", re.compile(r"[Cc]apital [Ll]ogic")),
    ("value_literal_customer_identity_phrase", re.compile(r"[Cc]ustomer [Ii]dentity")),
)
_VALUE_POSITION_EXEMPT_TOP_LEVEL_PREFIXES = ("_",)
_VALUE_POSITION_EXEMPT_PATHS = frozenset({("card_id",), ("tilth_cic_id",), ("tilth_clc_id",)})
```

**Results (grep transcript at `pipeline/cards/CLC/catalytic_change.yaml`):**

| Line | Path | Match | Exempt? |
|---|---|---|---|
| 1 | (YAML header comment) | `TILTH-CLC-02` | YES — comments are not in canonical bytes (stripped by YAML parser before `canonical_bytes()` hash); not in scanner surface |
| 21 | `card_id` | `TILTH-CLC-02` | YES — `_VALUE_POSITION_EXEMPT_PATHS` |
| 25 | `tilth_clc_id` | `TILTH-CLC-02` | YES — `_VALUE_POSITION_EXEMPT_PATHS` |
| 670 | `_research_metadata.priors_consulted[0].path` (`assets/cards/capital_logic/Capital Logic Cards.png`) | `Capital Logic` phrase | YES — `_research_metadata` top-level key starts with `_` |
| 671 | `_research_metadata.priors_consulted[0].extract_note` | `TILTH-CLC-00` (matches regex `TILTH-CLC-\d{2}`; reference to drawing TILTH-CLC-00) | YES — same exempt subtree |
| 673 | `_research_metadata.priors_consulted[1].extract_note` | `TILTH-CLC-02` | YES — same exempt subtree |
| 679 | `_research_metadata.priors_consulted[4].extract_note` | `TILTH-CLC-02` | YES — same exempt subtree |

**Verdict — LIVE regex set: 0 non-exempt findings.** Card passes the value-position regex defense.

### §2.5 Legacy-phrase defense scan (per Run 1 Phase 2 L2-F3 — not in current regex set; surface as defense-in-depth)

Grep for `[Cc]ustomer [Ii]nformation` across the card: 0 hits.

**Verdict — legacy-phrase defense-in-depth: 0 findings.** No regression risk.

### §2.6 Forbidden-coupling-field-name scan (CLC-side six)

Grep across the card body for the six CLC-side forbidden top-level field names (`eligible_cic_subset`, `cic_allowlist`, `cic_denylist`, `preferred_cics`, `cic_win_rate`, `cic_ranking_preferences`): 0 hits.

`common_funders_observed` absent on disk (no items to scan); `provenance_requirements` absent (no items to scan). Other arrays scanned for nested forbidden-field-names: 0 hits.

**Verdict — coupling-discipline regression: 0 findings.**

---

## §3. Research Findings

### §3.1 Source verification table — official + primary (verified against current card `_research_metadata.primary_sources`)

| URL | Type | Access date | Fields supported | Confidence |
|---|---|---|---|---|
| https://www.macfound.org/programs/100change/ | official (foundation) | 2026-05-15 (card line 694) | scoring_weight_patterns canonical four-criterion (Meaningful/Verifiable/Durable/Feasible); evidence_weights.learning_agenda; evidence_weights.dissemination_plan; narrative_section_patterns Theory of Change / Learning Agenda / Dissemination; reviewer_profile_typical foundation-side | HIGH |
| https://www.fordfoundation.org/work/our-grants/building-institutions-and-networks/ | official (foundation) | 2026-05-15 (card line 699) | underwriting_criteria.partnership_strength_and_role_clarity; evidence_weights.partner_commitment_letters_with_role_clarity; narrative_section_patterns Partnerships / Team | HIGH |
| https://new.nsf.gov/funding/opportunities/convergence-accelerator-phases-1-2 | official (federal) | 2026-05-15 (card line 704) | underwriting_criteria.novelty_or_innovation; evidence_weights.pilot_or_preliminary_results; common_red_flags.unsupported_innovation_claim; common_application_forms Research.gov | HIGH |
| https://www.nsf.gov/bfa/dias/policy/merit_review/ | official (federal) | 2026-05-15 (card line 709) | scoring_weight_patterns.NSF_Merit_Review (Intellectual Merit + Broader Impacts); applies across NSF innovation portfolios | HIGH |
| https://arpa-e.energy.gov/news-and-media/program-announcements | official (federal) | 2026-05-15 (card line 714) | underwriting_criteria.replication_pathway; evidence_weights.replication_pathway; scoring_weight_patterns.ARPA-E_Stage_Gate; narrative_section_patterns Scale / Replication Pathway | HIGH |
| https://arpa-e.energy.gov/about/intellectual-property | official (federal) | 2026-05-15 (card line 719) | evidence_weights.intellectual_property_or_openness_posture; compliance_obligations[Bayh-Dole]; ARPA-E retention beyond Bayh-Dole | HIGH |
| https://ies.ed.gov/funding/ncer_progs.asp | official (federal) | 2026-05-15 (card line 724) | underwriting_criteria.measurement_and_evaluation_rigor; evidence_weights.evaluation_partner; scoring_weight_patterns.IES_EIR (Significance / Project Design / Management / Evaluation Plan / Personnel); narrative_section_patterns Evaluation Plan; common_red_flags.evaluation_added_late | HIGH |
| https://www.nifa.usda.gov/grants/programs/agriculture-food-research-initiative-afri | official (federal) | 2026-05-15 (card line 729) | scoring_weight_patterns.USDA_AFRI (Scientific Merit / Relevance / Qualifications / Management / Budget) | HIGH |
| https://www.eda.gov/funding/programs/build-to-scale | official (federal) | 2026-05-15 (card line 734) | scoring_weight_patterns.EDA_Build_to_Scale (Strategy / Capacity / Impact / Sustainability_Match); budget_structure_conventions.match_requirements_typical (50%) | HIGH |
| https://www.rockefellerfoundation.org/case-study/catalytic-capital/ | official (foundation) | 2026-05-15 (card line 739) | underwriting_criteria.follow_on_capital_plan; evidence_weights.leverage_or_follow_on_capital_plan; narrative_section_patterns Sustainability / Follow-On Capital; common_red_flags.no_follow_on_capital_strategy | HIGH |
| https://www.skoll.org/about/approach/ | official (foundation) | 2026-05-15 (card line 744) | underwriting_criteria.scale_of_leverage; reviewer_profile_typical foundation-side; common_red_flags.scale_claims_arithmetically_implausible | HIGH |
| https://kresge.org/initiative/leadership-and-infrastructure-funding-team-lift/ | official (foundation) | 2026-05-15 (card line 749) | cross-CLC reference for capacity-building + field-building intersection with operating_capacity (CLC-03); equity-lens framing | MEDIUM (URL restructuring risk per Kresge 2024-2025 portfolio reorganization) |
| https://www.fsg.org/blog/six-conditions-systems-change/ | practitioner (canonical) | 2026-05-15 (card line 754) | underwriting_criteria.systems_leverage_point; evidence_weights.systems_map; evidence_weights.baseline_metrics; narrative_section_patterns Systems Context / Problem Framing | HIGH (canonical systems-change framework) |
| https://hewlett.org/grantmaking-faq/ | official (foundation) | 2026-05-15 (card line 759) | Hewlett flexible-funding posture; budget_structure_conventions.indirect_cost_treatment (Hewlett 0% indirect example) | HIGH |
| https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200 | official (federal) | 2026-05-15 (card line 764) | compliance_obligations[2 CFR Part 200]; budget_structure_conventions.indirect_cost_treatment (federal de minimis 10%); reporting_requirements_typical | HIGH |
| https://grants.nih.gov/grants/policy/coi/ | official (federal) | 2026-05-15 (card line 769) | compliance_obligations[Conflict of Interest disclosure]; NIH FCOI 42 CFR 50 Subpart F | HIGH |

### §3.2 New / refreshed sources to verify and add

| URL | Type | Why add | Card fields it would support | Confidence |
|---|---|---|---|---|
| https://www.macfound.org/programs/100change/about-the-competition | official | 100&Change selection-criteria + judging-process page; closer pin to four-criterion-rubric anchor than the program landing page | refresh scoring_weight_patterns[0].source_citation specificity | HIGH |
| https://hewlett.org/about-us/grantmaking-faq/ (vs root) | official | Hewlett flexible-funding statistic ("approximately three-quarters of grant dollars as flexible support") needs URL refresh — anchor page restructured | refresh primary_sources[Hewlett] | HIGH |
| https://www.bridgespan.org/insights/big-bets-philanthropy | practitioner | Bridgespan "Big Bets" framework for catalytic-capital large-gift framing — operationally cited in foundation-side strategy work; complements Rockefeller catalytic-capital anchor | new `_research_metadata.priors_consulted` entry; supports underwriting_criteria.timing_and_window_alignment + scale_of_leverage | HIGH |
| https://ssir.org/articles/entry/the_dawn_of_system_leadership | practitioner | Senge / SSIR "System Leadership" — companion to FSG Six Conditions; one of the most cited systems-change practitioner sources | optional `_research_metadata.priors_consulted` addition; supports systems_leverage_point criterion + systems_map evidence | MEDIUM |
| https://arpa-e.energy.gov/technologies (vs `/news-and-media/program-announcements`) | official | Active-program technology-area page is operationally more relevant for Scribe/Scout than press-release stream | refresh primary_sources[ARPA-E] URL | HIGH |
| https://www.nsf.gov/pubs/policydocs/pappg/index.jsp | official | NSF PAPPG — load-bearing for NSF innovation programs (Project Description / Project Summary structure / Biosketches / DMP); currently only Research.gov template page cited | new primary_sources entry; supports common_application_forms.NSF; narrative_section_patterns | HIGH |
| https://catalyticcapital.org/ | official (consortium) | Catalytic Capital Consortium (MacArthur / Omidyar / Rockefeller multi-funder collaboration) — canonical authority on catalytic-capital framing beyond any single foundation | new primary_sources entry; refines evidence_weights.leverage_or_follow_on_capital_plan + underwriting_criteria.follow_on_capital_plan | HIGH |
| https://www.surdna.org/grants/ | official (foundation) | Surdna sustainable-environments + thriving-cultures portfolios — canonical mid-sized foundation systems-change funder; useful for foundation-rubric pattern triangulation | optional `_research_metadata.priors_consulted` addition | MEDIUM |
| https://walton.org/our-work/education/ | official (foundation) | Walton Family Foundation education-innovation portfolio — canonical mid-sized foundation education-innovation funder; cross-reference to IES EIR for foundation-vs-federal education-innovation dialect | optional `_research_metadata.priors_consulted` addition | MEDIUM |
| https://www.climatebreakthrough.org/ | official (climate-transition fund) | Climate Breakthrough Project — catalytic-capital + climate-transition intersection; current admin admin-risk overlay relevant | optional `_research_metadata.priors_consulted` addition; supports underwriting_criteria.transition_plausibility | MEDIUM |
| https://www.bezosearthfund.org/our-grants | official (foundation) | Bezos Earth Fund climate-transition portfolio — large 2020s catalytic-capital climate funder | optional `_research_metadata.priors_consulted` addition | MEDIUM |
| https://www.ssir.org/articles/entry/collective_impact | practitioner | Kania / Kramer "Collective Impact" — canonical reference for backbone-organization + cross-sector partnership framing | optional `_research_metadata.priors_consulted` addition; supports partnership_strength_and_role_clarity criterion | MEDIUM |
| https://2cfr200.com/ | aggregator | 2 CFR 200 practitioner reference (NOT authoritative — eCFR primary) | NOT recommended — defer to eCFR primary | LOW |

### §3.3 Internet Archive snapshot verification (per master prompt §2 read-first item 7)

Recommended next Phase 4-CLC pass: verify Wayback Machine snapshots of all sixteen primary_sources URLs. Highest-risk URLs (highest restructuring probability):

1. **Kresge LIFT** (`https://kresge.org/initiative/leadership-and-infrastructure-funding-team-lift/`) — Kresge has restructured initiative URLs multiple times in 2024–2025; verify snapshot.
2. **ARPA-E** (`https://arpa-e.energy.gov/news-and-media/program-announcements`) — program-announcement stream is rolling; consider switching to the technology-area page or program-roster page.
3. **NSF Convergence Accelerator** (`https://new.nsf.gov/funding/opportunities/convergence-accelerator-phases-1-2`) — NSF migrated from FastLane → Research.gov and updated funding-opportunity URL schemas in 2024; verify snapshot reaches the current page.
4. **EPA-adjacent / climate-transition pages NOT in current primary_sources** — if added per §3.2, Wayback verification critical given the current administration's EPA/EE program realignment posture.

---

## §4. Proposed Card Improvements

Grouped by the eight runtime-behavior categories per master prompt §2 "Research task." Each proposal: exact YAML path, why-it-improves-runtime, target-seat, and where-it-belongs (card body vs Program Rule Pack vs admin-risk-register vs funder-DB vs matrix-layer-v1.x). Phase 4 fold-in discipline self-check at the end of §4.

### §4.1 search vocabulary / classification (CLC-side: underwriting_criteria + reviewer_profile_typical)

- **`underwriting_criteria.replication_pathway.description[REFINE]`.** Current text (line 52) doesn't acknowledge the stage-conditional weighting that `evidence_weights.replication_pathway.rationale` (line 187) handles correctly. Recommend adding to description: "Stage-conditional: at early/pilot phase reviewers expect a defined pathway articulated; at later phases reviewers expect documented replication evidence (sites copied, conditions met, lessons traveled). What changes with stage is the evidentiary burden, not the requirement." **Seat affected:** Scout (candidate-fit packet) + Scribe (replication-section drafting). **Where:** card body.
- **`underwriting_criteria.scale_of_leverage.source_citation[REFINE]` — dual-cite Skoll (foundation-side) + ARPA-E or NSF Convergence (federal-innovation-side).** Why: Skoll's "social-entrepreneur-scale" framing doesn't capture federal-innovation reviewers' "technological/commercialization/scientific scale" framing. **Seat affected:** Scribe (dialect switching) + Judge (rubric scoring). **Where:** card body.
- **`underwriting_criteria.partnership_strength_and_role_clarity.source_citation[REFINE]` — dual-cite Ford BUILD + NSF Convergence Accelerator phase-1-to-phase-2 team-formation framework.** Why: Ford BUILD captures capacity-building partnerships; NSF Convergence captures integrated-team partnerships across academic + industry + community. **Seat affected:** Scribe + Judge. **Where:** card body.
- **`underwriting_criteria.timing_and_window_alignment.source_citation[REFINE]`** — currently internal blueprint citation. Add external citation: Bridgespan "Big Bets" framework OR Stanford SSIR "System Leadership" article. **Seat affected:** Scribe (timing-anchor framing) + Judge. **Where:** card body.
- **`reviewer_profile_typical.dialect_split_note[REFINE]` — strengthen sub-sector splits.** Current note (line 360) distinguishes foundation vs federal-innovation. Recommend adding sub-sector-specific framing: "climate-transition: federal (ARPA-E / DOE) vs foundation (Bezos Earth Fund / Hewlett Climate / ClimateWorks) reviewer populations have different vocabulary preferences (federal favors techno-economic feasibility; foundation favors systems-leverage + policy-window)"; "education innovation: federal (IES EIR with RCT/independent-evaluator requirements) vs foundation (Walton / Hewlett / Carnegie with mission-fit + theory-of-change weighting) produce materially different drafting registers." **Seat affected:** Scribe (dialect routing) + Editor. **Where:** card body. **Per refusal (a) check:** this is a refinement to existing prose, not a structured sub-field expansion — PASSES.

### §4.2 evidence capture / missing-evidence prompts (CLC-side: evidence_weights)

- **`evidence_weights.baseline_metrics.rationale[REFINE]`.** Current rationale (line 197) says "Catalytic funders weight 'why now' framing heavily — baseline metrics paired with policy-window / market-signal context distinguish timely catalytic capital from speculative bets." Recommend tightening: "Weight: MEDIUM at early-phase/concept-paper stage where baseline may not yet be measured; HIGH at mid/late-phase where outcome claims depend on credible baseline. Without baseline, outcome claims are uninterpretable. Same stage-conditional logic as `replication_pathway` (above) — the single-enum value reflects the early-stage default per §18.6 schema enum (HIGH | MEDIUM | LOW); stage escalation captured in this rationale per card composer guidance." **Seat affected:** Scribe + Logician (evidence-completeness gate). **Where:** card body. **Per refusal (c) check:** does NOT introduce compound enum; PASSES.
- **`evidence_weights[NEW] — fcoi_disclosure_completeness`.** weight = MEDIUM. rationale = "Financial-conflict-of-interest disclosure completeness for federal-routed innovation proposals (NSF, NIH, USDA AFRI, IES per 42 CFR 50 Subpart F for PHS-funded research). Reviewers (federal-innovation panels) treat FCOI disclosure quality as a soft scoring signal — a complete, organization-policy-anchored disclosure reads as institutional-readiness; an incomplete one signals administrative gap. For foundation grants, FCOI is not formally required but corporate-foundation grants increasingly request similar disclosures." source_citation = https://grants.nih.gov/grants/policy/coi/. **Seat affected:** Logician + Scribe + Judge. **Where:** card body. **Per refusal (a) check:** new entry uses canonical evidence_weight item shape (weight + rationale + source_citation); PASSES.
- **`evidence_weights[NEW] — independent_evaluator_engagement_documentation`.** weight = HIGH (with rationale capturing federal-vs-foundation conditional). rationale = "Federal innovation programs (IES EIR all tiers, NSF AISL, USDA AFRI demonstration projects) require independent evaluator named with budget allocated at the time of application; reviewer panels look for documentation of pre-submission engagement (consultancy letter, scope-of-work draft, budget line). Late-engaged evaluators (added at submission for compliance) score weakly. Foundations vary — internal evaluation acceptable for some; external preferred at scale. The single-enum value HIGH reflects federal-innovation primacy; foundation weight escalates per scale (over-$500K foundation grants typically expect external evaluator pre-engagement)." source_citation = https://ies.ed.gov/funding/ncer_progs.asp. **Seat affected:** Scribe + Logician + Red Team (evaluation_added_late probe). **Where:** card body.
- **`evidence_weights.evaluation_partner.rationale[REFINE]` — lead with dialect-conditional.** Current value: HIGH (line 200). Rationale prose at line 202 says "Weight: HIGH for federal innovation, MEDIUM for foundation." But the single enum value is HIGH. The Cycle-2 fix-in-place precedent (replication_pathway.weight from compound `MEDIUM_EARLY_HIGH_LATER` → canonical `MEDIUM`) suggests keeping a single enum value with rationale-prose capturing the conditional. NO change to the weight value (HIGH); refine rationale to lead with the dialect-conditional. **Per refusal (c) check:** preserves canonical enum; PASSES.

### §4.3 Scoring weight patterns + rubric library (CLC-side)

- **`scoring_weight_patterns[0].rubric_example[REFINE]` — add inline source anchor.** Current (line 101): "Foundation innovation/catalytic rubric — typical anatomy across major national foundation innovation portfolios." source_citation correctly points to MacArthur 100&Change. Recommend appending to rubric_example string: " — MacArthur 100&Change is the canonical pattern source per the cited URL; other major foundation innovation portfolios (Ford BUILD field-building rubric, Skoll Award rubric, Hewlett innovation portfolios) adopt similar 4-6 criterion structures." This preserves Phase F Tier-1 Law-5 anonymization while making the pattern source more locatable. **Seat affected:** Judge (rubric-pattern lookup) + Scribe. **Where:** card body.
- **`scoring_weight_patterns[NEW] — Catalytic Capital Consortium (CCC) framing`.** rubric_example = "Catalytic Capital Consortium (MacArthur / Omidyar / Rockefeller multi-funder collaboration) catalytic-capital criteria: patient capital, risk-tolerant, concessionary, flexible — the four-attribute pattern beyond per-funder rubrics." weights: `patient: weighted`, `risk_tolerant: weighted`, `concessionary: weighted`, `flexible: weighted`. source_citation = https://catalyticcapital.org/. note = "CCC framing is consortium-side and tier-agnostic — applies to any opportunity framed as catalytic capital; the four attributes are useful as a check beyond a single foundation's published rubric." **Seat affected:** Judge + Scribe. **Where:** card body.
- **`scoring_weight_patterns[NEW]` — top-of-section note (free-text key inside an item, NOT a new structured field) reminding consumers that the six rows capture structural patterns and per-cycle rubrics must be re-verified per active RFA/NOFO.** Currently this disclaimer is only on the EDA Build to Scale row (line 144). Recommend either (a) extending the disclaimer to each rubric row's `note` key, OR (b) adding a meta-row at the top of scoring_weight_patterns whose `rubric_example` says "NOTE: structural-patterns surface; actual rubric criteria + weights vary per published RFA/NOFO." **Per refusal (a) check:** option (a) is a prose-refinement on existing notes (PASSES); option (b) is a new item using canonical item shape (PASSES); avoid a new top-level field or sub-field. **Seat affected:** Judge. **Where:** card body.

### §4.4 drafting register / admin-risk handling (Law 4 + OD-A v2.4)

- **The 14 admin-risk-term entries removed at Cycle-2 fix-in-place migrate to workspace-wide `admin_risk_register.yaml` v2.3 follow-on dispatch.** Per Cycle-2 closure narrative at line 615, this is a separate ceremony. Recommend bundling with the §18 v1.2 + §18.6 v2 + §4 v2.x.7 compound cards-ceremony per Run 1 P0-1 to amortize ceremony cost. **Per OD-A v2.4 cross-CLC normalization:** the 14 catalytic_change-scoped terms overlap with credit_underwriting (15 entries; "innovation," "leverage," "scalability," "ecosystem"), operating_capacity (1 entry; "community wealth-building" cross-flag), and cooperative + shared_assets (each ~7-9 entries via OD-A v2.4 audit). Specifically:
  - `systems change`, `transformative`, `disruptive innovation` — likely shared across catalytic_change + research_evidence + cooperative.
  - `climate transition`, `energy transition` — likely shared with public_purpose_works (CLC-01) and credit_underwriting (CLC-06 climate finance).
  - `equity-centered design`, `centering community` — likely shared across catalytic_change + cooperative + arts_culture (CIC-04).
  - `innovation`, `demonstration`, `scalability`, `leverage`, `ecosystem`, `field building`, `catalytic` — high recurrence across most CLCs; canonical OD-A v2.4 cross-CLC consolidation candidates.
- **Cross-axis admin-risk-term normalization** — `centering community` likely also appears on CIC-side (cooperative, food_systems). Per OD-A v2.4 ≥3-card recurrence threshold + master prompt §9 ("admin-risk terms that are repeated across CLCs migrate to the workspace-wide admin_risk_register, NOT individual card bodies"): surface as P0 operator decision queue item.

### §4.5 reviewer / rubric logic

- **`reviewer_profile_typical.reviewer_priorities[REFINE]` — augment with a stage-conditional probe.** Current eight reviewer_priorities (lines 351–359) are excellent. Recommend adding: "What stage of the innovation lifecycle is this — feasibility, pilot, demonstration, expansion — and does the evidence burden match the stage?" Why: helps Judge calibrate against IES EIR tiers (Early-phase / Mid-phase / Expansion), NSF Convergence (Phase 1 / Phase 2), ARPA-E (Concept Paper / Full Application), Foundation (LOI / Full Proposal) stage gates. **Seat affected:** Judge + Red Team. **Where:** card body.
- **`reviewer_profile_typical.common_red_flags_from_reviewer_pov[REFINE]` — add `"Theory of change uses 'innovative' as adjective rather than as substantive claim"`.** Currently line 364 says "Innovation claim unsupported by reference to prior art or comparable approaches" which is correct but covers only the explicit-claim case. The adjective-without-substance variant is more common in early-draft proposals. **Seat affected:** Red Team + Editor. **Where:** card body.

### §4.6 red-team probes (CLC: common_red_flags)

- **`common_red_flags.no_replication_pathway.severity[REFINE]`.** Currently MEDIUM. Recommend upgrading to HIGH and refining the red_team_probe prose: "For early-phase opportunities (concept paper / Phase 1 / Early EIR), articulate a defined replication pathway with named conditions even without supporting evidence yet; for late-phase opportunities (Phase 2 / Mid or Expansion EIR / ARPA-E later-stage), provide documented replication evidence (sites copied, conditions met)." **Per refusal (c) check:** single-enum severity per canonical set (HIGH | MEDIUM | LOW) — preserve canonical enum; do NOT introduce compound `HIGH_LATE_MEDIUM_EARLY`. **Seat affected:** Red Team + Judge. **Where:** card body.
- **`common_red_flags[NEW] — theory_of_change_lacks_falsifiability_marker`.** severity = MEDIUM. red_team_probe = "What evidence would invalidate your theory of change at each step of the chain? If no evidence could invalidate any step, the theory is unfalsifiable and reads as a wishlist to reviewers." source_citation = https://www.macfound.org/programs/100change/. Why: this is the "falsifiability marker" demand from `narrative_section_patterns.Theory_of_Change.note` (line 266) elevated to an explicit red-flag probe; currently the `wishlist_theory_of_change` flag (line 414) probes for mechanism, not falsifiability. Distinct probes. **Seat affected:** Red Team. **Where:** card body.
- **`common_red_flags[NEW] — learning_agenda_collapses_to_evaluation_plan`.** severity = MEDIUM. red_team_probe = "Are your 'learning questions' identical to your evaluation outcome metrics? If yes, you have an evaluation plan, not a learning agenda. A learning agenda asks questions the field doesn't yet know the answer to; an evaluation plan measures whether your intervention worked. Foundations distinguish these — federal innovation reviewers (IES EIR especially) increasingly do too." Why: a common conflation in early drafts. **Seat affected:** Red Team + Editor. **Where:** card body.
- **`common_red_flags[NEW] — follow_on_capital_named_as_additional_foundation_grants`.** severity = HIGH. red_team_probe = "Does your sustainability section name 'additional foundation grants' as the follow-on capital strategy? If yes, the funder reads this as 'you have no plan beyond rotating philanthropic dollars.' Catalytic capital expects post-pilot funding sources to include earned revenue, public budgets, federal program funds, or impact investment — not just more grants." Why: currently `common_red_flags_from_reviewer_pov[6]` (line 369) captures this from the reviewer POV but no probe surfaces in Red Team's structured probe list. **Seat affected:** Red Team. **Where:** card body.

### §4.7 reporting / commitment extraction (CLC: commitment_tracking_pattern)

- **`commitment_tracking_pattern.typical_commitments_extracted.evaluation_finding.measurement_method[REFINE]`.** Current: "named research question + finding + evidence source + dissemination plan." Recommend tightening: "named research question (from the proposal's learning agenda) + finding (qualitative or quantitative; preserve uncertainty bounds) + evidence source (data type + collection method) + dissemination plan (channel + audience + timing)." Why: aligns the v0.2 Report Generator extraction discipline to the §18 v1.1 KFR provenance-cap discipline. **Seat affected:** Archivist (v1.x) + Report Generator (v0.2). **Where:** card body.
- **`commitment_tracking_pattern.typical_commitments_extracted[NEW] — evaluator_pre_engagement_evidence`.** measurement_method = "evaluator name + organization + scope-of-work signed at proposal stage + budget line + pre-submission engagement documentation (consultancy letter, kickoff email, scope draft)." Why: pairs with the new evidence_weights.independent_evaluator_engagement_documentation entry; enables v0.2 Report Generator to extract evaluator-engagement-status across awarded grants. **Seat affected:** Report Generator. **Where:** card body.
- **`commitment_tracking_pattern.paragraph_2_coverage_note[REFINE]` — explicit v0.2 → v1 horizon mapping.** Current note (line 592) maps 10 typical_commitments to §18.10 paragraph-2 categories. Recommend appending: "v0.2 first-wave Report Generator initial scope: 5 of 10 (learning_product_released / dissemination_metric / pilot_milestone_completed / follow_on_funding_secured / partnership_milestone — highest-frequency commitments). v0.2 second-wave + v1.x extend to all 10. v1.x Archivist Reflection sub-mode integrates evaluation_finding + policy_or_market_engagement + replication_inquiry into long-running curation." Why: clarifies the implementation-phase scope mapping per master prompt rule 11 / Run 1 §0. **Seat affected:** Archivist + Report Generator + operator (v0.2 spec). **Where:** card body OR v0.2 spec doc; either acceptable.

### §4.8 memory namespace usefulness (architecture v7.0.11 §1.9)

Recommend the following `cards:clc:catalytic_change:*` namespace sub-keys be standardized for future Scout / Scribe / Judge / Logician / Archivist / Report Generator / Model Router consumption when seat-registration graduates per v0.2 first-wave loader:

- `cards:clc:catalytic_change:underwriting_criteria` → underwriting_criteria
- `cards:clc:catalytic_change:scoring_weight_patterns` → scoring_weight_patterns
- `cards:clc:catalytic_change:evidence_weights` → evidence_weights
- `cards:clc:catalytic_change:common_application_forms` → common_application_forms
- `cards:clc:catalytic_change:narrative_section_patterns` → narrative_section_patterns
- `cards:clc:catalytic_change:budget_structure_conventions` → budget_structure_conventions
- `cards:clc:catalytic_change:reviewer_profile_typical` → reviewer_profile_typical
- `cards:clc:catalytic_change:dialect_split_note` → reviewer_profile_typical.dialect_split_note (sub-key elevated for direct dialect-router consumption)
- `cards:clc:catalytic_change:common_portals` → common_portals
- `cards:clc:catalytic_change:common_red_flags` → common_red_flags
- `cards:clc:catalytic_change:reporting_requirements_typical` → reporting_requirements_typical
- `cards:clc:catalytic_change:compliance_obligations` → compliance_obligations
- `cards:clc:catalytic_change:commitment_tracking_pattern` → commitment_tracking_pattern
- `cards:clc:catalytic_change:primary_sources` → `_research_metadata.primary_sources` (audit-trail; not for runtime authority)
- `cards:clc:catalytic_change:draft_funder_candidates` → (NOT POPULATED — Law-5 posture question; see §5 OD queue item 1)

**Seat affected:** all consuming seats. **Where:** architecture v7.0.11 §1.9 sets the namespace pattern; the per-card sub-key map is a v0.2 first-wave loader concern; the seat-registry depends-on-field mapping per Run 1 Patch D5 is the right home. Surface to operator as a v0.2 loader-graduation enumeration question (parallel to food_systems §4.8).

### §4.9 Phase 4 fold-in discipline self-check (per master prompt rule 6 / §18.11 v1.1)

Each proposed change above scanned against the four refusals:

| Proposal | (a) structured-sub-field expansion on canonical entries? | (b) dedicated-field-name fork? | (c) compound enum value? | (d) literal canonical CIC/CLC slug in non-exempt value position? |
|---|---|---|---|---|
| §4.1 underwriting_criteria.replication_pathway.description refine | NO — refines description prose within canonical item shape | NO | NO | NO |
| §4.1 scale_of_leverage source_citation dual-cite | NO | NO | NO | NO |
| §4.1 partnership_strength source_citation dual-cite | NO | NO | NO | NO |
| §4.1 timing_and_window_alignment source_citation external add | NO | NO | NO | NO |
| §4.1 reviewer_profile_typical.dialect_split_note refine | NO — refines prose | NO | NO | NO |
| §4.2 evidence_weights.baseline_metrics rationale refine | NO | NO | NO — preserves MEDIUM | NO |
| §4.2 evidence_weights add fcoi_disclosure_completeness | NO — uses canonical evidence_weights item shape | NO | NO — uses MEDIUM | NO |
| §4.2 evidence_weights add independent_evaluator_engagement_documentation | NO — same | NO | NO — uses HIGH | NO |
| §4.2 evidence_weights.evaluation_partner rationale refine | NO | NO | NO — preserves HIGH | NO |
| §4.3 scoring_weight_patterns[0] rubric_example refine | NO — refines prose | NO | NO | NO |
| §4.3 scoring_weight_patterns add CCC | NO — uses canonical scoring_weight_patterns item shape | NO | NO | NO |
| §4.3 scoring_weight_patterns top-of-section note (free-text in note key OR new item) | NO if free-text in note; new item uses canonical shape | NO | NO | NO |
| §4.4 admin-risk-term migration to workspace-register | N/A — workspace-register change | N/A | N/A | N/A |
| §4.5 reviewer_priorities augment | NO — adds item to canonical array | NO | NO | NO |
| §4.5 common_red_flags_from_reviewer_pov refine | NO | NO | NO | NO |
| §4.6 common_red_flags.no_replication_pathway severity upgrade | NO — preserves single-enum HIGH | NO | NO | NO |
| §4.6 common_red_flags add theory_of_change_lacks_falsifiability_marker | NO — uses canonical item shape | NO | NO | NO |
| §4.6 common_red_flags add learning_agenda_collapses_to_evaluation_plan | NO — same | NO | NO | NO |
| §4.6 common_red_flags add follow_on_capital_named_as_additional_foundation_grants | NO — same | NO | NO | NO |
| §4.7 commitment_tracking_pattern.evaluation_finding refine | NO | NO | NO | NO |
| §4.7 commitment_tracking_pattern add evaluator_pre_engagement_evidence | NO — uses canonical commitment_type item shape | NO | NO | NO |
| §4.7 paragraph_2_coverage_note refine | NO — refines prose | NO | NO | NO |
| §4.8 memory namespace sub-keys | N/A — architecture decision, not card body | N/A | N/A | N/A |

**Verdict:** No proposed change trips any of the four Phase 4 fold-in refusals.

---

## §5. Operator Decision Queue

Decisions that require Josh / operator approval before any patch dispatches:

1. **Law-5 posture for CLC cards — `common_funders_observed` absent vs empty-list-plus-research-metadata.** food_systems (CIC) carries `common_funders_observed: []` (empty list) AT TOP LEVEL plus `_research_metadata.draft_funder_candidates_pending_operator_engagement_confirmation:` with subagent-populated candidates. catalytic_change (CLC) carries NEITHER field on disk. Both are technically Law-5-compliant (the empty-list approach makes the absence-by-Law-5-discipline explicit; the absent-from-disk approach makes it implicit). **Operator decision: should CLC cards mirror the CIC empty-list-plus-research-metadata pattern, or is absent-from-disk the canonical CLC posture?** Suggest the cross-axis sweep across all 8 CLC cards plus all 6 CIC cards to confirm canonical posture before re-sign ceremonies fire. **P0** (affects all 14 cards if reconciled).
2. **Admin-risk-register cross-CLC normalization for the 14 catalytic_change-scoped entries.** Per Cycle-2 fix-in-place at line 615, the 14 terms migrate to `admin_risk_register.yaml` v2.3 follow-on dispatch. Per OD-A v2.4 ≥3-card recurrence threshold, the high-recurrence terms (`innovation`, `demonstration`, `scalability`, `leverage`, `ecosystem`, `field building`, `catalytic`, `systems change`, `transformative`) qualify for workspace-wide consolidation. **Operator decides: fire the migration as part of the compound §18 v1.2 + §18.6 v2 + §4 v2.x.7 cards-ceremony, or as a standalone admin-risk-register ceremony?** Recommendation: bundle to amortize ceremony cost. **P0**.
3. **MacArthur 100&Change anonymization Tier-1 cleanup (Phase F 2026-05-16) — keep current posture vs add inline anchor.** Current posture (line 101): generic descriptor + URL citation + note prose at line 109. Anchor specificity is preserved via URL but anonymized in the rubric_example string. §4.3 recommends adding an inline note appending "MacArthur 100&Change is the canonical pattern source per the cited URL." **Operator decides:** preserve Phase F Tier-1 anonymization strictness OR add the inline anchor for locator clarity (still Law-5-compliant because URL is already cited). **P1**.
4. **Stage-conditional evidence-weight discipline (baseline_metrics + replication_pathway).** Both fields handle stage-conditional weighting via rationale-prose only (single-enum value per §18.6 schema). §4.2 + §4.6 propose tightening rationale prose; refusal (a) forbids structured sub-field expansion. **Operator decides:** route to v0.2 §18.6 amendment proposing a `stage_conditional_weight: {early: MEDIUM, late: HIGH}` schema extension? OR remain with rationale-prose-only forever? Cross-CLC implication (research_evidence + market_access track_a likely have same stage-conditional weighting need). **P1 / route to v0.2 Wave 3**.
5. **Independent-evaluator pre-engagement evidence elevation.** §4.2 proposes a new evidence_weights entry. This is operationally load-bearing for federal-innovation programs (IES EIR all tiers REQUIRE evaluator named at proposal time; NSF AISL strongly recommended; USDA AFRI demonstration-grade encouraged). **Operator decides:** add as new evidence_weights entry (current proposal) OR fold into existing `evaluation_partner` entry as a sub-clause? Recommendation: separate entry to surface the pre-engagement distinction explicitly. **P1**.
6. **Falsifiability marker as explicit red-flag probe.** §4.6 proposes a new `theory_of_change_lacks_falsifiability_marker` red_flag. This elevates the falsifiability demand from `narrative_section_patterns.Theory_of_Change.note` to a structured Red Team probe. **Operator decides:** the proposal targets Scribe/Red Team behavior directly; recommend approval. **P1**.
7. **NSF PAPPG addition to primary_sources.** §3.2 recommends adding `https://www.nsf.gov/pubs/policydocs/pappg/index.jsp` — load-bearing for NSF innovation programs (Project Description / Project Summary / Biosketches / DMP). **Operator decides:** add to `_research_metadata.primary_sources` with brief verbatim quote (≤2 sentences per OQ-4). **P1**.
8. **Catalytic Capital Consortium addition to scoring_weight_patterns.** §4.3 proposes adding CCC's four-attribute framing (patient / risk-tolerant / concessionary / flexible) as a consortium-side rubric_example. **Operator decides:** approve addition; consortium-side framing genuinely fills a gap beyond per-funder rubrics. **P1**.
9. **Foundation rubric structural-pattern-vs-FOA-actual disclosure (EDA Build to Scale precedent at line 144).** Currently the EDA Build to Scale row carries the structural-pattern disclaimer in `note`. Recommend extending the disclaimer to each rubric row's `note` key (free-text refinement; not a structured field). **Operator decides:** card-body addition vs Program Rule Pack convention. **P1**.
10. **Climate-transition + energy-transition admin-risk handling under current EO 14154 administrative framing.** The 14 Cycle-2-removed admin-risk terms include `climate transition` and `energy transition` — both flagged RED under current administration. The workspace-register migration (decision item 2) needs to address whether Tilth defaults to substitute-and-flag or retain-and-flag at federal-routed cycles. **Operator decides** per cross-CLC + per-funder posture; may need a v0.2 Lessons Memory per-funder override mechanism. **P0** (affects every federal-innovation cycle Tilth touches).
11. **IP / openness posture per mission-aligned funder.** Card cites `intellectual_property_or_openness_posture` weight = MEDIUM (line 205). Mission-aligned funders (Skoll, climate funds, OSS-aligned foundations) often prefer open-source / open-data — recommend bumping the signal to HIGH in their dialect overlays. **Operator decides:** schema permits single-enum MEDIUM per §18.6 (HIGH | MEDIUM | LOW); dialect-overlay-driven weight escalation is a v0.2 dialect-routing concern. Route to v0.2. **P2**.
12. **State-overlay / international funder considerations.** Card is federal + national-foundation heavy. Some state arts/innovation councils + international funders (e.g., Wellcome Trust UK for global-health innovation; Bezos Earth Fund global-scope) operate similar catalytic-capital logic. **Operator decides:** route state-specific and international funders to OD-G state-overlay or v0.2 multi-region overlay. **P2**.
13. **Lock-history housekeeping field disposition (cross-card).** Per Run 1 Patch E1: `lifecycle.lock_history_row` / `lock_timestamp_utc` / `supersession_lock_history_row` are schema-only with no `models.py` mirror. Same disposition as food_systems. Operator decides on the cross-card fix. **P1**.
14. **Re-signing ceremony budget for content edits.** Per operator reframe ("first units / unlocked"): aggressive content improvements OK to recommend; re-signing ceremony cost acceptable. The §4 proposals above touch ~17 distinct card-body edits. Bundle with the §18 v1.2 + §18.6 v2 + §4 v2.x.7 compound cards-ceremony OR run as a separate Phase 4-CLC-derived content refresh ceremony. Recommendation: bundle to amortize. **P1**.

---

## §6. Validation Checklist

| Check | Result | Evidence |
|---|---|---|
| Schema fields complete against current §18.5 / §18.6 schema | PASS | 15/15 required CLC fields present per `card_clc.schema.json:7-23` (schema_version / card_axis / card_id / slug / display_name / funding_mechanism_summary / tilth_clc_id / underwriting_criteria / evidence_weights / reviewer_profile_typical / common_red_flags / reporting_requirements_typical / commitment_tracking_pattern / lifecycle / _research_metadata); lifecycle block satisfies allOf conditional at lines 318–369 (runtime_loadable=true → draft_status=signed AND signature_status=signed AND runtime_load_status=loaded; signed_at/signed_by/content_hash present) |
| No forbidden coupling field names (top-level CLC-side six) | PASS | Grep across the file: none of 6 forbidden CLC-side names (`eligible_cic_subset`, `cic_allowlist`, `cic_denylist`, `preferred_cics`, `cic_win_rate`, `cic_ranking_preferences`) appear anywhere |
| No forbidden coupling field names (item-level not.anyOf defense-in-depth) | N/A — `common_funders_observed` absent; `provenance_requirements` absent; no item-level surface to scan | Verified by structural read |
| No forbidden value-position regex matches outside exempt paths | PASS | Per §2.4 above — 0 non-exempt findings; all hits are in `card_id` / `tilth_clc_id` / `_research_metadata.priors_consulted[*]` |
| No legacy-phrase `[Cc]ustomer [Ii]nformation` matches (defense-in-depth) | PASS | 0 hits — verified by grep |
| No private organization-specific data in card body | PASS | No org-specific data on disk; primary_sources are all funder/regulatory anchors; priors_consulted are workspace docs and Skill files |
| No unsourced program-law claims | PASS at body | Verbatim quotes ≤2 sentences per OQ-4 throughout; program statutory anchors are CFR / agency page cited per OQ-3. Note: budget_structure_conventions.match_requirements_typical text (line 335) names EDA Build to Scale 50% match — this is program structure (not live program-law variation); appropriate for card body. PASS. |
| No excessive verbatim source text | PASS | Verbatim quotes capped at ≤2 sentences per primary_source row per OQ-4. Per Cycle-2 closure narrative the strict-verbatim verification deepening is acknowledged as a Phase 4 step before the next re-sign (lines 686 + 804) — current paraphrase posture is operator-documented. |
| Lifecycle status consistent with architecture v7.0.11 §1.5 production-load requirements | PASS | All five lifecycle gate fields at pass-state; runtime_loadable=true; content_hash present; signed_at + signed_by present |
| **Top-level `common_funders_observed:` absent on disk (Law-5 split posture variance)** | PASS-with-caveat | No `common_funders_observed` top-level field on disk; no Law-5 violation surface (absent ≠ populated-without-attestation). Cross-axis posture variance vs food_systems (which carries the empty-list pattern) is a P0 normalization candidate — see §5 decision item 1. |
| **No populated top-level `common_funders_observed` without operator-engagement-attestation** | PASS | Field absent; no Law-5 violation possible. |
| **No `_research_metadata.draft_funder_candidates_pending_operator_engagement_confirmation:` block** | PASS-with-caveat | Field absent on disk. Cross-axis posture variance vs food_systems is a P0 normalization candidate — see §5 decision item 1. |
| Phase 4 fold-in discipline (refusals a/b/c/d) | PASS | Per §4.9 table — none of the proposed changes trip any of the four refusals. |
| Cycle-2 fix-in-place precedent acknowledged in lifecycle block | PASS | Lines 643–660 carry the Cycle-2 closure narrative explicitly; the three fixes (replication_pathway.weight enum normalization, primary_sources[*].quote_type removal, admin_risk_term_register block removal) are on-disk record. |
| For multi-track CLCs: shared root metadata + oneOf branch 2 compliance | N/A — this is a single-track CLC (oneOf branch 1 per §18.6 v2) |

**Net coupling-discipline regression: 0 findings.**

---

## §7. Regression Tests

3–5 prompts that should demonstrate behavior change between pre-edit and post-edit cards. Each prompt + expected pre-edit behavior + expected post-edit behavior + which seat changes.

### Test 1 — "Transform food systems" prompt (food_systems × catalytic_change high-volume intersection per §18.19.2)

**Prompt:** "We are a regional food-systems coalition planning to apply for a foundation grant to transform how mid-Atlantic small farms reach institutional buyers across hospital systems, school districts, and universities. The grant ask is $3M over four years to scale up an existing pilot."

**Pre-edit behavior (current CLC-02 card):**
- Scout matches `transform`, `systems`, `pilot`, `scale` — routes to CLC-02 catalytic_change underwriting logic.
- Scribe drafts narrative with Theory of Change section (current 600–1500 word count) and Learning Agenda section.
- Red Team fires `wishlist_theory_of_change` probe.
- Logician requires partner LOIs + evaluation plan.
- BUT: no explicit falsifiability marker probe; no learning_agenda-vs-evaluation-plan conflation probe; replication_pathway flag at MEDIUM may understate severity for a 4-year demonstration scope.

**Post-edit behavior (with §4.6 new red_flags):**
- Scribe drafts with explicit assumption-naming at each ToC step + a falsifiability marker per `narrative_section_patterns.Theory_of_Change.note`.
- Red Team fires `theory_of_change_lacks_falsifiability_marker` probe — surfaces if the ToC lacks "what evidence would invalidate this chain."
- Red Team fires `learning_agenda_collapses_to_evaluation_plan` probe — surfaces if learning questions are identical to evaluation metrics.
- Red Team fires `follow_on_capital_named_as_additional_foundation_grants` probe — surfaces if sustainability section names only "additional grants" as follow-on.
- Replication pathway severity upgraded to HIGH for late-phase opportunity; Red Team prompts for documented sites + conditions met.
- Result: a "transform food systems" prompt produces a draft that survives the four high-severity Catalytic-Change red flags rather than reading as a wishlist + grant-rotation plan.

**Seat affected:** Scribe + Red Team + Editor + Judge. **Pass criterion:** all four new/upgraded red-flag probes fire in Red Team output for a draft lacking the demanded substantive elements; the resulting draft scaffolds (a) system map, (b) leverage point, (c) pilot design, (d) partner roles, (e) learning outputs.

### Test 2 — "Innovative" adjective without substantive claim (master-prompt acceptance test "Innovation ask is rejected or downgraded if novelty is unsupported")

**Prompt:** "We are developing an innovative new approach to youth mentorship using AI-powered matching technology. We're seeking $500K from the NSF Convergence Accelerator to pilot this innovation."

**Pre-edit behavior:**
- Scout matches `innovation`, `AI`, `pilot` — routes to CLC-02 catalytic_change underwriting logic.
- Scribe drafts narrative using "innovative" framing throughout.
- Red Team fires `unsupported_innovation_claim` probe (HIGH severity) — demands three comparable approaches.
- Logician applies admin-risk register for "innovation" (post-migration to workspace-register).

**Post-edit behavior (with §4.5 new common_red_flags_from_reviewer_pov item):**
- Scribe drafts with "innovative" only where load-bearing claim substantiated; otherwise uses substantive verb phrases (e.g., "matching algorithm leverages multilingual NLP not present in prior mentorship platforms").
- Red Team fires `unsupported_innovation_claim` AND new "innovative as adjective rather than substantive claim" probe.
- Editor surfaces adjective-without-substance instances for substitution.
- Judge downgrades the innovation claim where evidence path is missing.
- Result: a draft that earns the "innovation" claim by reference to prior art rather than asserting it as a vibe; or the application is downgraded for unsupported novelty.

**Seat affected:** Scribe + Red Team + Editor + Judge. **Pass criterion:** Red Team output identifies all `[Ii]nnovat\w*` instances without comparator + flags for substantiation; Judge downgrades a draft lacking prior-art comparison.

### Test 3 — Federal innovation (IES EIR Mid-phase) evaluation-discipline test

**Prompt:** "We are applying for an IES EIR Mid-phase grant to expand our literacy-tutoring program from one school district to twenty. The ask is $4M over three years."

**Pre-edit behavior:**
- Scout matches `expand`, `tutoring`, `school district`, `EIR Mid-phase` — routes to CLC-02 catalytic_change + IES EIR sub-rubric (scoring_weight_patterns[5]).
- Scribe drafts with Evaluation Plan section using current `evidence_weights.evaluation_partner` weight HIGH.
- Red Team fires `evaluation_added_late` probe (MEDIUM severity).
- Logician notes IES EIR Mid-phase requires moderate evidence + RCT + independent evaluator.
- BUT: no explicit pre-engagement-documentation demand; `independent_evaluator_engagement_documentation` evidence_weight does not exist; Logician's evaluator-pre-engagement probe is heuristic, not anchored.

**Post-edit behavior (with §4.2 new evidence_weights entry):**
- Scribe drafts with `independent_evaluator_engagement_documentation` evidence_weight (HIGH) — prompts for evaluator scope-of-work signed at proposal stage + budget line + pre-submission engagement documentation (consultancy letter or kickoff email or scope draft).
- Logician enforces evaluator-pre-engagement gate as a pre-submission check.
- Red Team fires `evaluation_added_late` probe with new probe prose expanded — "Was the evaluator engaged before submission, with documented pre-submission scope of work?"
- Result: applicant prompted for evaluator-pre-engagement documentation at intake; not at submission.

**Seat affected:** Scribe + Logician + Red Team. **Pass criterion:** `independent_evaluator_engagement_documentation` evidence_weight fires in Scribe-section-drafting; Logician's pre-engagement gate fires before draft is finalized.

### Test 4 — Foundation vs federal-innovation dialect switching

**Prompt 1:** "We are applying to Hewlett Foundation's Climate Initiative for $750K to demonstrate a community-scale energy-transition model in three frontline neighborhoods."

**Prompt 2:** "We are applying to ARPA-E for $2M to demonstrate a new grid-scale energy-storage technology achieving X efficiency at Y cost."

**Pre-edit behavior:**
- Scribe drafts both narratives using underwriting_criteria.replication_pathway + scale_of_leverage criterion (sourced Skoll only).
- Scribe's dialect-routing selects sub-register heuristically; current `dialect_split_note` (line 360) distinguishes foundation vs federal-innovation at top-level but does not surface sub-sector splits (climate-transition: ARPA-E vs Hewlett).
- Judge scores both against MacArthur 100&Change-pattern rubric + ARPA-E Stage Gate rubric; runtime tries both, selects best fit.
- BUT: Prompt 1 may bleed federal-innovation techno-economic vocabulary into a foundation-side draft; Prompt 2 may bleed foundation-side leverage/policy-window vocabulary into a federal-side draft.

**Post-edit behavior (with §4.1 dialect_split_note refinement):**
- Scribe consults refined `dialect_split_note` with explicit climate-transition sub-sector framing — "federal (ARPA-E / DOE) vs foundation (Bezos Earth Fund / Hewlett Climate / ClimateWorks) reviewer populations have different vocabulary preferences."
- Prompt 1 draft uses leverage + policy-window + systems-leverage framing (foundation register); evidence_weights weight foundation-side criteria.
- Prompt 2 draft uses techno-economic + commercialization + technical-merit framing (federal register); evidence_weights weight federal-side criteria.
- Result: drafts read as native to their respective reviewer populations.

**Seat affected:** Scribe + Judge + Editor. **Pass criterion:** narrative drafts surface sub-sector-appropriate vocabulary; Editor flags cross-dialect bleed.

### Test 5 — Catalytic Capital Consortium framing (cross-CLC + cross-stage)

**Prompt:** "We are applying to the Catalytic Capital Consortium (CCC) for a $1.5M PRI to deploy capital that catalyzes additional investment in regenerative-agriculture supply chains."

**Pre-edit behavior:**
- Scout matches `catalytic capital`, `PRI`, `regenerative agriculture` — routes to CLC-02 catalytic_change + CIC-01 food_systems (orthogonal pair).
- Scribe drafts using underwriting_criteria.follow_on_capital_plan + Rockefeller catalytic-capital framing.
- Judge scores against MacArthur 100&Change-pattern rubric.
- BUT: no scoring_weight_patterns entry capturing CCC's four-attribute framing (patient / risk-tolerant / concessionary / flexible); Judge cannot triangulate against CCC's consortium-side framework.

**Post-edit behavior (with §4.3 new scoring_weight_patterns entry):**
- Judge scores against MacArthur 100&Change-pattern rubric AND CCC four-attribute framing (patient / risk-tolerant / concessionary / flexible).
- Scribe surfaces CCC-specific framing where applicable (PRI as concessionary, blended capital, etc.).
- Logician applies admin-risk register for "catalytic" (post-migration to workspace-register).
- Result: CCC-aligned application receives consortium-side rubric triangulation in addition to per-funder rubric scoring.

**Seat affected:** Scribe + Judge. **Pass criterion:** Judge's rubric-pattern lookup surfaces CCC entry in addition to MacArthur 100&Change; Scribe surfaces patient/risk-tolerant/concessionary/flexible framing.

---

## §8. Patch Plan

Edits proposed in this handback grouped by file path. **No edits applied from this dispatch.** Operator dispatches each ceremony separately per the OD-C / OD-E precedent.

### File: `pipeline/cards/CLC/catalytic_change.yaml`

**Ceremony shape:** supersession-re-sign per OD-E precedent (row 276 / 277 / 278 model). Parent_lock_row = 256 (Wave 2 LOCK). Ceremony_parent_row = `<NEXT-AVAILABLE-COMPOUND-PARENT>` if bundled with §18 v1.2 + §18.6 v2 + §4 v2.x.7 cards-ceremony, OR `<NEXT-AVAILABLE>` standalone.

**Edit set:**

1. `underwriting_criteria.replication_pathway.description[REFINE]` — add stage-conditional acknowledgment (§4.1).
2. `underwriting_criteria.scale_of_leverage.source_citation[REFINE]` — dual-cite Skoll + ARPA-E or NSF Convergence (§4.1).
3. `underwriting_criteria.partnership_strength_and_role_clarity.source_citation[REFINE]` — dual-cite Ford BUILD + NSF Convergence (§4.1).
4. `underwriting_criteria.timing_and_window_alignment.source_citation[REFINE]` — add external citation (Bridgespan or SSIR) (§4.1).
5. `reviewer_profile_typical.dialect_split_note[REFINE]` — add climate-transition + education-innovation sub-sector splits (§4.1).
6. `evidence_weights.baseline_metrics.rationale[REFINE]` — tighten stage-conditional framing (§4.2).
7. `evidence_weights[NEW] — fcoi_disclosure_completeness` (§4.2).
8. `evidence_weights[NEW] — independent_evaluator_engagement_documentation` (§4.2).
9. `evidence_weights.evaluation_partner.rationale[REFINE]` — lead with dialect-conditional (§4.2).
10. `scoring_weight_patterns[0].rubric_example[REFINE]` — add inline source anchor (§4.3).
11. `scoring_weight_patterns[NEW] — Catalytic Capital Consortium (CCC) framing` (§4.3).
12. `scoring_weight_patterns[*].note[REFINE]` — extend EDA Build to Scale structural-pattern disclaimer to each rubric row's note key (§4.3 + §5 item 9).
13. `reviewer_profile_typical.reviewer_priorities[REFINE]` — add stage-conditional probe (§4.5).
14. `reviewer_profile_typical.common_red_flags_from_reviewer_pov[REFINE]` — add "innovative as adjective" item (§4.5).
15. `common_red_flags.no_replication_pathway.severity[REFINE]` — upgrade to HIGH with stage-conditional probe prose (§4.6).
16. `common_red_flags[NEW] — theory_of_change_lacks_falsifiability_marker` (§4.6).
17. `common_red_flags[NEW] — learning_agenda_collapses_to_evaluation_plan` (§4.6).
18. `common_red_flags[NEW] — follow_on_capital_named_as_additional_foundation_grants` (§4.6).
19. `commitment_tracking_pattern.typical_commitments_extracted.evaluation_finding.measurement_method[REFINE]` (§4.7).
20. `commitment_tracking_pattern.typical_commitments_extracted[NEW] — evaluator_pre_engagement_evidence` (§4.7).
21. `commitment_tracking_pattern.paragraph_2_coverage_note[REFINE]` — add v0.2 → v1 horizon mapping (§4.7).
22. `_research_metadata.primary_sources[NEW]` — add NSF PAPPG entry (§3.2).
23. `_research_metadata.primary_sources[NEW]` — add Catalytic Capital Consortium entry (§3.2 + §4.3).
24. `_research_metadata.primary_sources[REFINE]` — refresh ARPA-E URL to technology-area page (§3.2).
25. `_research_metadata.priors_consulted[NEW]` — add Bridgespan "Big Bets" + SSIR "System Leadership" + SSIR "Collective Impact" (§3.2).
26. (Operator decision pending) `common_funders_observed: []` (empty list) AT TOP LEVEL + `_research_metadata.draft_funder_candidates_pending_operator_engagement_confirmation:` block — if operator decides per OD queue item 1 to normalize CLC cards to the CIC empty-list-plus-research-metadata posture (§5 item 1).

**OD-D Phase 4 forward-binding contract note (per master prompt rule 6 + §18.11 v1.1):**

- No proposal touches refusal (c) (compound enum values) — all evidence_weights / common_red_flags / severity additions use canonical HIGH/MEDIUM/LOW or FREQUENT/OCCASIONAL/RARE/UNKNOWN.
- No proposal touches refusal (d) (literal canonical CIC/CLC slug in non-exempt value position) — value-position scan verified clean per §2.4.
- No proposal touches refusal (a) (structured-sub-field expansion on canonical entries) — all additions are at canonical item-shape boundaries; stage-conditional + dialect-conditional refinements stay in prose.
- No proposal touches refusal (b) (dedicated field-name fork) — no new top-level field names proposed.

Per Run 1 P1-1 / L1-F3 — the F-CARDS-COUPLING-VIOLATION-EXTENSION gate body is currently `NotImplementedError`. Value-position-scan that should catch refusal (d) regressions is not LIVE at runtime today. The compensating control is loader.py's enforce_no_forbidden_coupling (field-name layer only). This patch plan is value-position clean per manual scan; gate-body graduation per Run 1 Patch C1 should happen in parallel with or before the cards-ceremony to harden runtime defense.

R-CARDS-ENUM-CANONICAL (OD-B, pending) tagging: applies to edits 6, 9, 15 (single-enum weight + severity refinements that exercise enum-canonical discipline). Future regression hardening at v0.2.

### File: `pipeline/cards/_schema/card_clc.schema.json`

**Ceremony shape:** part of cards-ceremony compound LOCK per Run 1 Patch Queue Batch B.

**Edit set:**

27. (Operator decision pending OD queue item 4) — if operator approves a `stage_conditional_weight` schema extension: add sub-field shape to evidence_weights item definition. **Per refusal (a):** structured sub-field expansion — route as §18 v1.x amendment candidate; DO NOT bake silently.
28. (Cross-card with food_systems Patch B20) — schema acknowledgment of `_research_metadata.draft_funder_candidates_pending_operator_engagement_confirmation` if operator approves OD queue item 1.

### File: `pipeline/institutional_memory/admin_risk_register.yaml`

**Ceremony shape:** workspace-register update (OD-A v2.4 → v3.0 scrub workflow per master prompt §7).

**Edit set:**

29. Add 14 CLC-02-scoped admin-risk terms migrated from card body per Cycle-2 fix-in-place narrative at line 615 (§4.4). Verify cross-CLC normalization candidates (`innovation`, `demonstration`, `scalability`, `leverage`, `ecosystem`, `field building`, `catalytic`, `systems change`, `transformative`, `climate transition`, `energy transition`, `equity-centered design`, `centering community`, `disruptive innovation`) for per_clc_register cell coverage.
30. Climate-transition + energy-transition severity disposition per OD queue item 10 (substitute-and-flag vs retain-and-flag default).

### File(s): `pipeline/cards/CLC/operating_capacity.yaml` + `pipeline/cards/CLC/research_evidence.yaml` + other CLC siblings (cross-card; out of scope for this dispatch)

Per OD-A v2.4 cross-CLC normalization: any vocabulary migration affects the per-CLC register cells on sibling CLC-side cards too. **Out of scope for `catalytic_change` handback. Surface to cards-ceremony / Phase 4-CLC parallel dispatch and to the batch supervisor's cross-card synthesis.**

---

**Summary block:**

```
Card: CLC:catalytic_change
Card file: pipeline/cards/CLC/catalytic_change.yaml
Research hours actual: 1.6
Findings: 22 total — 3 P0, 11 P1, 8 P2
Decision queue: 14 operator approvals required
Conflicts with prior art: NONE (all admin_risk_term entries align with the Cycle-2 closure narrative for workspace-register migration; cross-CLC term-set is normalization-candidate, not conflict; the no-`common_funders_observed`-on-disk posture is a cross-axis variance, not a Law-5 violation)
Coupling-discipline regression: NONE
Lifecycle gap surfaced: draft_status reads "signed" on disk; no normalization required per Run 1 P0-3
Review readiness: READY
```
