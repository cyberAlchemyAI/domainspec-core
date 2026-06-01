# TILTH-CLC-03 Operating Capacity — Research Handback

**Filed:** 2026-05-17
**Workspace:** `/Users/goldenquill/Downloads/GoldenQuill/`
**Run:** Run 2 Phase 4-CLC (1 of 8 sibling CLC dispatches).
**Card:** `pipeline/cards/CLC/operating_capacity.yaml` (Wave 1 LOCKed 2026-05-15 row 227; content_hash `sha256:baff12ca…dbebf`; signed `2026-05-15T20:30:00Z`).
**Authority chain:** master prompt `docs/cic_clc_unified_master_prompt_2026-05-17.md` §2 (per-card output shape) + plan `docs/cic_clc_unified_research_plan_2026-05-17.md` §2.3 (priority vectors) + Run 1 priors at `docs/card_system_deep_research_2026-05-17/` (binding).
**Run 1 priors folded in (do not re-surface):**
- All 14 cards on disk are `draft_status: "signed"` (P0-3 / L1-F0 — no normalization needed).
- §18 v1.2 LOCKed-but-not-applied (CIC-side dialect_routing_table re-keying — no direct impact on this CLC card body).
- F-CARDS-COUPLING-VIOLATION-EXTENSION predicate body raises `NotImplementedError` at runtime (L1-F3 / P1-1) — value-position regex is spec-only today; manual scan required.
- Law-5 split on `common_funders_observed` is **unconfirmed** for CLC cards (Phase 2 L2-F5 / Phase 3 P1-3); status to be surfaced per card.
- Operator reframe: aggressive content improvements OK; re-signing ceremony cost acceptable.
- **Wave 1 reference CLC card** — new schema item-shape proposals must compare against this card's on-disk shape before recommending changes (lest re-trigger the §18 v1.1 narrow-corrective pattern).

---

## §1. Card Impact Thesis

`operating_capacity` is the Wave 1 reference CLC card and the deepest precedent in the CLC body for canonical-shape conformance (OD-1 path (a) closure of admin_risk_term_register, OD-3 path (a) closure of evidence_weights source_citation extension). Its job is to make the council **evaluate capacity funding as bottleneck-removal with durable operational gains** rather than as generic operating-support language, and to make Judge / Red Team / Logician fail-close any capacity ask that lacks (a) a specific current bottleneck, (b) a job description or system specification, (c) measurable post-investment operating-gain math, and (d) a non-vapor sustainability plan.

What this card should cause Tilth to do differently relative to a sector-naive baseline:

1. When Scout sees "general operating support," "capacity building," "infrastructure," or "field-strengthening" in a foundation opportunity, anchor on the Ford BUILD / MacArthur field-support / Kresge LIFT / Hewlett / Bush Ecosystem-Grant / community-foundation capacity-grant taxonomy — NOT generic foundation prose.
2. When Scribe drafts a capacity narrative, force a *named* bottleneck + job-description-or-system-spec + implementation timeline + supervision plan + measurable-capacity-gain target + sustainability revenue math, in that order. Reject "we need more staff" as a substantive ask.
3. When Judge evaluates a draft against a foundation capacity rubric, weight `organizational_need` + `project_design` + `organizational_capacity` HIGH; weight `sustainability` MEDIUM but fail-close on revenue-math absence.
4. When Logician audits an "infrastructure," "scalability," "capacity-building," "innovation," "transformation," "stakeholder," or "sustainability" admin-risk term, surface workspace-register tier (v2.2 / v2.3 / v2.4) + reviewer-context + substitution candidates — NEVER silently rewrite. Per OD-1 path (a) closure the per-card admin_risk_term_register field is removed from this card; the workspace-wide `admin_risk_register.yaml` is the authoritative surface.
5. When Report Generator (v0.2 horizon) ingests `clc_operating_capacity_commitments` from an executed award, it should produce a typed extraction across the 8 commitment-types (staff_hired / systems_implemented / trainings_completed / policies_adopted / service_capacity_increased / turnaround_time_reduced / data_quality_improved / governance_strengthened) with the measurement methods this card prescribes.

The runtime-behavior delta this card should produce versus a sector-naive baseline is **bottleneck-specificity demanded + measurable-gain math required + sustainability-as-revenue-math (not language)**. The card is currently strong on (1)–(2) and on the typed commitment-tracking shape for (5); (3)–(4) carry residual gaps around tier-source-backing and reviewer-context program-status freshness which §4 below proposes to refine.

---

## §2. Current State Audit

### §2.1 What is strong now

- **Foundation-anchor density.** Underwriting_criteria source-cite Capital Region Community Foundation (Letter of Commitment from Board Chair requirement; line 60), Vermont Community Foundation, Ford BUILD, MacArthur Field Support, Kresge LIFT, Hewlett, Bush Ecosystem-Grant — every primary-source URL in `_research_metadata.primary_sources` (lines 487–556) carries access_date 2026-05-15 and verbatim quote ≤2 sentences per OQ-4.
- **Federal-program-anchor density.** `compliance_obligations[1]` cites 2 CFR Part 200; `compliance_obligations[2]` cites 2 CFR 200.343 (Closeout — 90 days); `scoring_weight_patterns[2]` cites 7 CFR Part 3406 (USDA NIFA 1890 CBG); `reporting_requirements_typical` cites HUD CB Programs Performance Output Data Collection semi-annual cadence.
- **Ten underwriting criteria.** capacity_bottleneck + mission_relationship + staffing_or_systems_need + implementation_plan + management_readiness + governance + measurable_capacity_gain + sustainability + budget_to_task_integrity + dependency_risk. Each carries description + qualitative weight + source citation. The "budget_to_task_integrity" + "dependency_risk" entries distinguish capacity-grant rubrics from operating-support generics.
- **Evidence weights — canonical §18.6 shape.** 10 evidence kinds with `{weight, rationale}` (no source_citation extension per OD-3 path (a) closure — preserved in `_research_metadata`). workload_evidence / staffing_plan / board_approval / strategic_plan / backlog_or_demand_data / financial_statements / implementation_timeline all HIGH; job_descriptions / org_chart / systems_audit MEDIUM. Tier assignments are operator-defensible per typical foundation capacity rubrics.
- **Eight typed commitment-types.** `commitment_tracking_pattern.typical_commitments_extracted` covers the 8-commitment cycle (staff_hired / systems_implemented / trainings_completed / policies_adopted / service_capacity_increased / turnaround_time_reduced / data_quality_improved / governance_strengthened) with explicit `measurement_method` per type. `proposal_commitments_yaml_extension.field_name: clc_operating_capacity_commitments` per Cycle-1 F6 fold-in CLC-namespaced convention.
- **Red-flag adversarial probes.** 8 common_red_flags carry red_team_probe text + severity tier. `sustainability_as_future_grants` (HIGH) and `weak_budget_mapping` (HIGH) carry source_citation. The probes are operator-grade — Red Team can fire them verbatim.
- **Reviewer profile typical — 6 reviewer types.** foundation_program_officer + capacity_reviewer + public_agency_program_officer + national_service_reviewer + community_foundation_grants_committee + peer_reviewer_from_sector. Captures the heterogeneity of capacity-grant reviewer pools.
- **Common application forms — three-entry truth-block.** Entry 1 documents the *absence* of a national common form for capacity building per Cycle-1 F5 fold-in (Council on Foundations URL anchoring); Entry 2 names Foundant GLM / Submittable / Fluxx as the actual federation surface; Entry 3 names SF-424 / SF-424A for federal capacity NOFOs. The "no national common form" entry is a Scout-protective fact: prevents Scout from surfacing "the Common Grant Application" as if it were a singular artifact.
- **Lifecycle truth.** `draft_status: signed`, `signature_status: signed`, `runtime_load_status: loaded`, `runtime_loadable: true`, `content_hash: sha256:baff12ca…dbebf`, `signed_at: 2026-05-15T20:30:00Z`, `signed_by: founder`, `lock_history_row: 227`, `lock_timestamp_utc: 2026-05-15T20:30:00Z` — fully consistent with architecture v7.0.11 §1.5 production-load requirements (per Run 1 Phase 1 §4 table).
- **OD closure provenance.** Lines 12–18 + 446–464 document OQ-3 / OQ-4 / OQ-5 / OQ-6 closures + OD-1 / OD-2 / OD-3 / OD-4 dispositions explicitly. The card carries its own audit-trail rationale.

### §2.2 What is stale, ambiguous, over-broad, too local, too federal, or under-sourced

- **`scoring_weight_patterns` qualitative-tier ILLUSTRATIVE-not-empirical caveats.** Both rubric examples (Sopact foundation-rubric anatomy line 89–96; USDA NIFA 1890 CBG line 98–105) carry author-qualitative-judgment caveats acknowledging the cited source establishes rubric *framework* but does NOT enumerate the specific per-criterion tier assignments. **Strong (operator-defensible) but read flag:** the explicit "ILLUSTRATIVE patterns" caveat is correct discipline but means Judge cross-checking these against the funder's actual rubric will routinely diverge. Recommend a small refinement: add cross-reference text to the `note` field pointing Judge to "consult published NOFO scoring criteria when available; rely on these tier assignments only when funder rubric is unpublished or in flux."
- **Foundation funder-program freshness.** Ford BUILD primary source quote claims `$1.6 billion across 600 grants` with `$2 billion total over 12 years` (line 496); the access date is 2026-05-15. Verify against current Ford Foundation BUILD program page (program scale figures shift mid-cycle). MacArthur Field Support framing (line 502) and Kresge LIFT framing (line 506) are evergreen-style; less freshness risk.
- **Federal program-status risk.** None of the federal NOFO references on this card are at high realignment risk under current administration framing (2 CFR 200 is foundational regulation; USDA NIFA 1890 CBG is statutorily anchored). No refresh needed.
- **`compliance_obligations[1] Single Audit threshold gloss`.** Line 356: "Single Audit if federal expenditures ≥ $750,000/year (rising to $1M under 2024 update)." The 2024 update reference is correct per 2 CFR 200 revision. **But** the "rising to $1M" framing reads as forward-looking; the threshold is now $1M per the 2024 final rule effective for FY beginning on or after October 1, 2024. Recommend tightening to "$750,000/year through FY2024; $1,000,000/year for FY beginning on or after October 1, 2024 per 2 CFR 200 (2024 final rule)."
- **`narrative_section_patterns` has 7 sections; missing `"Theory of Change / Logic Model"` and `"Lessons from Prior Capacity Work"`.** Both are standard capacity-grant reviewer expectations; Ford BUILD and Kresge LIFT in particular weight prior-capacity-work narratives. Adding these tightens Scribe's section structure to match foundation rubrics.
- **`reviewer_priorities` is 5 items.** Strong starter set. Missing: "Is the evidence base for the capacity ask grounded in current organizational data (not 'we feel understaffed')?" — this is the gap-analysis-grade reviewer question that distinguishes a capacity-grant from an operating-support pitch. Recommend addition.
- **`budget_structure_conventions.indirect_cost_treatment` text is precise.** Reads: "Foundation capacity grants often cap or exclude indirect costs; federal capacity grants honor the recipient's federally negotiated rate or de minimis 10% MTDC per 2 CFR 200." Strong. Could add nuance: many large national foundations (Ford, MacArthur, Kresge) have moved to permissive indirect treatment (full federally-negotiated rate accepted) in recent capacity grants; community foundations remain more restrictive. Recommend optional refinement.
- **`common_application_forms` — Foundant GLM / Submittable / Fluxx framing is correct.** Note: many community foundations use GivingData (CommunityForce, FoundationConnect) as well — surface for completeness in entry 2's note? Operator decides; not a defect.
- **`common_red_flags` missing `"capacity ask without baseline operational metrics"`.** Adversarial probe: "Where is the current-state operational baseline against which we measure the post-investment gain?" Currently the card carries `no_measurable_capacity_gain` (HIGH) — same family, but the missing-baseline framing is the more common red flag in practice. Recommend addition.
- **No explicit `data systems` / `data infrastructure` capacity-grant-subtype framing.** The card's `evidence_weights.systems_audit: MEDIUM` and `commitment_tracking_pattern[systems_implemented]` cover the system side, but there is no dedicated reviewer-context distinguishing CRM-modernization / data-platform-implementation / analytics-build asks from staffing asks. Capacity-grant reviewers increasingly expect data-systems requests to carry their own adoption-plan + data-migration + training + ownership content (per the acceptance test on this card). Recommend a `narrative_section_patterns[NEW]` "Adoption / Change Management Plan" section, applicable particularly to system-side asks.
- **Verbatim source quotes age out.** 14 primary sources (lines 488–556) dated `access_date: 2026-05-15`. Per OD-4 (deferred to follow-on hygiene dispatch per operator default 2026-05-15 PM), Internet Archive snapshot pass on all primary_source URLs is pending. Recommend the next Phase 4-CLC re-dispatch confirm Wayback snapshots, particularly the foundation URLs (Ford BUILD, MacArthur field-support, Kresge LIFT, Hewlett, Bush) which redesign more frequently than federal regulatory URLs.
- **`reporting_requirements_typical.note`.** Line 345: "HUD Capacity Building Programs guidance: Performance Output Data Collection Tool semi-annual + final report; foundations vary but semi-annual + final is the modal pattern." Correct; the HUD CB Programs cadence is one specific federal example. Foundations actually vary widely — some Ford BUILD grantees report annually, some quarterly. Operator decision: keep the HUD modal-pattern anchor (defensible per `_research_metadata`), or expand the note to acknowledge foundation variance.

### §2.3 Lifecycle / signature / schema concerns

- **`draft_status: signed`.** No normalization needed per Run 1 P0-3 / L1-F0.
- **No stale header-comment issue on this card** (audit on lines 1–18: header reads "SIGNED — runtime-loadable; lifecycle truth enforced by loader preflight" + OQ resolutions; reflects current state accurately). No P1-4 patch needed for this card.
- **`common_funders_observed:` field is ABSENT.** Per `pipeline/cards/_schema/card_clc.schema.json:98` it is OPTIONAL (not in `required`). The card omits it entirely. **Per master prompt §0 / Phase 2 §6.4 / Phase 3 P1-3 status:** since the field is absent, no Law-5 violation surface exists today. The Law-5 split applied uniformly across the 6 CIC cards (top-level empty list + `_research_metadata.draft_funder_candidates_pending_operator_engagement_confirmation:` nested block) is NOT applied here — because there is nothing to relocate. **Operator decision queue item §5.6 below:** consider whether the card should explicitly carry an empty `common_funders_observed: []` block + `_research_metadata.draft_funder_candidates_pending_operator_engagement_confirmation:` of sector-canonical capacity funders (Ford BUILD / MacArthur Field Support / Kresge LIFT / Hewlett / Bush Foundation / community foundations) for Scout discovery surface, OR keep the field absent and let Scout discover capacity funders dynamically from the underwriting_criteria + common_red_flags substance.
- **`_research_metadata.draft_funder_candidates_pending_operator_engagement_confirmation:` field also absent.** Per Run 1 Patch B20 — the schema currently doesn't declare this field on the CLC schema (only validates via `_research_metadata.additionalProperties: true`). If §5.6 lands as "add draft candidates," recommend doing it in the cards-ceremony per Patch B20 (schema-known field + value population at the same compound LOCK).
- **`_oq6_anchor: true` field at line 87.** This is a defense-in-depth anchor for the OQ-6 numeric-weights ban; AST-lint hookup (R-CARDS-NO-NUMERIC-WEIGHT) is deferred to v1.x amendment-realization checklist per the file's own comment. Schema-passes-by-virtue-of-additionalProperties:true. No defect; documented anchor pattern.
- **Lock-history housekeeping fields.** `lifecycle.lock_history_row: 227` + `lifecycle.lock_timestamp_utc: 2026-05-15T20:30:00Z` + `lifecycle.supersession_lock_history_row` absent (no supersession yet). Per Run 1 L1-F8: these three optional fields are not in `models.py.Lifecycle`; canonical-bytes exclusion set does NOT exclude them per L1-F7. Cross-card operator decision; not specific to operating_capacity. Surface to cards-ceremony per Run 1 Patch E1.

### §2.4 Coupling-discipline self-audit (per master prompt §2 item 2 + Run 1 L1-F3 enforcement context)

**Method.** Manual value-position scan over the full card body using the regex set from `section_04_v2_x_7_card_coupling_value_position_amendment.md:108-120`:

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

**Results (grep transcript at `pipeline/cards/CLC/operating_capacity.yaml`):**

| Line | Path | Match | Exempt? |
|---|---|---|---|
| 1 | (YAML header comment) | `TILTH-CLC-03` | YES — comments are not in canonical bytes (stripped by YAML parser before `canonical_bytes()`); not in scanner surface |
| 22 | `card_id` | `TILTH-CLC-03` | YES — `_VALUE_POSITION_EXEMPT_PATHS` |
| 26 | `tilth_clc_id` | `TILTH-CLC-03` | YES — `_VALUE_POSITION_EXEMPT_PATHS` |
| 475 | `_research_metadata.priors_consulted[0].extract_note` | `TILTH-CLC-00` (roster drawing ID) + `Operating Capacity` | YES — `_research_metadata` top-level key starts with `_`; underscore-prefix exemption applies to entire subtree |
| 479 | `_research_metadata.priors_consulted[2].extract_note` | `TILTH-CLC-03` | YES — same exempt subtree |

Searches for `[Cc]apital [Ll]ogic`, `[Cc]ustomer [Ii]dentity`: 0 hits.

**Verdict — LIVE regex set: 0 non-exempt findings.** Card passes.

### §2.5 Legacy-phrase defense scan (per Run 1 Phase 2 L2-F3 — not in current regex set; surface as defense-in-depth)

Grep for `[Cc]ustomer [Ii]nformation` across the card: 0 hits.

**Verdict — legacy-phrase defense-in-depth: 0 findings.** No regression risk.

---

## §3. Research Findings

### §3.1 Source verification table — official + primary

| URL | Type | Access date | Fields supported | Confidence |
|---|---|---|---|---|
| https://www.fordfoundation.org/work/our-grants/building-institutions-and-networks/ | official | 2026-05-15 (card primary_sources line 488) | Ford BUILD program (five-year general operating + institutional strengthening) | HIGH |
| https://www.fordfoundation.org/news-and-stories/news-and-press/news/ford-foundation-expands-flagship-build-program-to-provide-1-billion-to-hundreds-of-organizations/ | official | 2026-05-15 (line 493) | Ford BUILD scale ($1.6B / 600 grants / $2B over 12 years) | HIGH (verify against current Ford page) |
| https://www.macfound.org/programs/field-support/philanthropy/ | official | 2026-05-15 (line 498) | MacArthur Field Support; general operating + project support | HIGH |
| https://kresge.org/initiative/leadership-and-infrastructure-funding-team-lift/ | official | 2026-05-15 (line 503) | Kresge LIFT; equity-lens capacity-building grants | HIGH |
| https://hewlett.org/grantmaking-faq/ | official | 2026-05-15 (line 508) | Hewlett flexible-support posture (~75% in 2024) | HIGH |
| https://www.bushfoundation.org/opportunities/community-innovation/ | official | 2026-05-15 (line 513) | Bush Ecosystem Grants ($450K / 3 years operating support) | HIGH |
| https://ourcommunity.org/nonprofit-support/grants-at-the-community-foundation/capacity-building-grants | official | 2026-05-15 (line 518) | Capital Region Community Foundation; Letter of Commitment from Governing Board Chair + 2 fiscal years of revenue/expense + Annual Operating Budget | HIGH |
| https://vermontcf.org/funds/nonprofit-capacity-building/ | official | 2026-05-15 (line 523) | Vermont CF small-grant pattern ($5,000 cap consultant fees) | HIGH |
| https://www.ecfr.gov/current/title-7/subtitle-B/chapter-XXXIV/part-3406 | official | 2026-05-15 (line 528) | USDA NIFA 1890 Institution Capacity Building Grants — 7 CFR Part 3406 | HIGH |
| https://www.tgci.com/blog/2020/08/understanding-capacity-building-grant-proposals | practitioner | 2026-05-15 (line 533) | Grantsmanship Center: capacity-building outcome = product-shaped (strategic plan / database / technology / fund-development plan / succession plan) | MEDIUM (practitioner, but operator-grade content) |
| https://www.fundsforngos.org/how-to-write-a-proposal/top-10-common-mistakes-in-grant-proposals-and-how-to-avoid-them/ | practitioner | 2026-05-15 (line 538) | Common sustainability-section red flags | MEDIUM (aggregator) |
| https://www.hud.gov/sites/dfiles/CPD/documents/Capacity-Building-Programs-Reporting-Guidance.pdf | official | 2026-05-15 (line 543) | HUD CB Programs Performance Output Data Collection semi-annual cadence | HIGH |
| https://www.sopact.com/use-case/grant-review-rubric | practitioner | 2026-05-15 (line 548) | Foundation rubric anatomy (4-6 criteria + weighted scoring + 4-level anchors) | MEDIUM (practitioner) |
| https://nlctb.org/featured/how-to-respond-to-sustainability-questions-in-grant-proposals/ | practitioner | 2026-05-15 (line 553) | Sustainability-section practitioner guidance | MEDIUM |

### §3.2 New / refreshed sources to verify and add

| URL | Type | Why add | Card fields it would support | Confidence |
|---|---|---|---|---|
| https://www.ecfr.gov/current/title-2 | official | 2 CFR 200 (Uniform Guidance) — root regulation reference; card already cites Part 200 specifically but a top-level Title 2 anchor is useful for Logician cross-checking | refresh `compliance_obligations[1].source_citation` to point at the Title 2 / Part 200 anchor + add Subpart-D Closeout cross-reference | HIGH |
| https://www.boardsource.org/ | practitioner | BoardSource — board-governance authority; standard reference for Letter of Commitment / authorizing resolution language | underwriting_criteria.governance source_citation supplement | MEDIUM |
| https://www.bridgespan.org/insights/library/strategy-development/the-nonprofit-starvation-cycle | practitioner | Bridgespan "Nonprofit Starvation Cycle" — operator-grade reference on indirect-cost capacity-grant framing | underwriting_criteria.sustainability reviewer_context supplement; budget_structure_conventions.indirect_cost_treatment refinement | MEDIUM |
| https://www.npqmag.org/ | practitioner | Nonprofit Quarterly — capacity-building reporting and analysis | optional priors_consulted addition | LOW–MEDIUM |
| https://www.fordfoundation.org/work/our-grants/build/ | official | Refresh Ford BUILD URL — verify the BUILD landing page (the URL on the card is the parent "building institutions and networks" page) | refresh `_research_metadata.primary_sources` Ford BUILD entry | HIGH |
| https://kresge.org/programs/social-investments/ | official | Kresge Social Investments — complements LIFT for the cross-mechanism capacity-pipeline framing | optional priors_consulted addition | MEDIUM |
| https://www.macfound.org/programs/100-and-change/ | official | MacArthur 100&Change — capacity-at-scale; not a CLC-03 match (catalytic_change territory) but useful for delineation | optional priors_consulted for cross-CLC orthogonality boundary notes; **not for card body** | MEDIUM |
| https://www.cof.org/ | official | Council on Foundations — the existing card primary_sources line 168 cites cof.org for the "no national common form" Cycle-1 F5 fold-in fact. Verify the COF capacity-building landscape page is current | refresh `common_application_forms[1].source` if a more specific COF page exists | HIGH |
| https://www.givingdata.com/ | practitioner | GivingData / CommunityForce / FoundationConnect — additional grant management platforms many community foundations use beyond the Foundant/Submittable/Fluxx triad | optional refinement of `common_application_forms[2].note` to acknowledge platform diversity | MEDIUM |
| https://www.cdfa.net/ | practitioner | Council of Development Finance Agencies — surfaces community-foundation / public-finance capacity-grant intersection (relevant when cross-CLC stacking with CLC-01 public_purpose_works applies at runtime per architecture v7.0.11 §6.1 orthogonality) | optional priors_consulted addition | LOW–MEDIUM |

### §3.3 Internet Archive snapshot verification (per master prompt §2 read-first item 7; OD-4 deferred)

Per OD-4 (deferred to follow-on hygiene dispatch per operator default 2026-05-15 PM): Internet Archive snapshot pass on all 14 `_research_metadata.primary_sources` URLs is pending. Priority order for the next Phase 4-CLC re-dispatch:

1. **HIGH freshness risk:** Ford BUILD URLs (foundation websites redesign 2–3 year cycles); Kresge LIFT URL; Hewlett FAQ URL; Bush Ecosystem Grant URL; Capital Region CF URL; Vermont CF URL — foundation pages are the highest reorg risk.
2. **MEDIUM freshness risk:** Sopact / Grantsmanship Center / fundsforngos / nlctb — practitioner sites with longer URL stability.
3. **LOW freshness risk:** ecfr.gov / hud.gov — federal regulatory URLs are the most stable.

The HUD CB Programs Reporting Guidance PDF URL (line 543) should be specifically Wayback-checked since HUD PDF document URLs are routinely re-versioned with year-suffix changes.

---

## §4. Proposed Card Improvements

Grouped by the eight runtime-behavior categories per master prompt §2 "Research task." Each proposal: exact YAML path, why-it-improves-runtime, target-seat, and where-it-belongs (card body vs Program Rule Pack vs admin-risk-register vs funder-DB vs matrix-layer-v1.x). Phase 4 fold-in discipline self-check at the end of §4.

### §4.1 search vocabulary / classification (CLC-side: underwriting_criteria + reviewer_profile_typical)

- **`underwriting_criteria[NEW]` — add `data_systems_adoption_readiness`.** description = "For data-systems / CRM / analytics capacity asks: explicit user-population, data-migration plan, training schedule, ownership / governance, and post-go-live support model." weight_in_typical_rubric = qualitative. source_citation = "blueprint:section_18_card_system.md#§18.10-CLC-03 + practitioner: BoardSource governance guidance + Bridgespan indirect-cost framing." Why: capacity-grant reviewers treat data-systems asks differently from staffing asks; current `staffing_or_systems_need` underwriting criterion conflates the two. Separating tightens the bottleneck-specificity discipline. **Seat affected:** Judge + Red Team + Scribe. **Where:** card body.
- **`reviewer_priorities[NEW]` — add `"Is the evidence base for the capacity ask grounded in current organizational data (not 'we feel understaffed')?"`.** Why: the missing-baseline / no-current-state-data probe is the most common foundation-reviewer challenge to a capacity-ask narrative; absent from the current 5-priorities list. **Seat affected:** Judge + Red Team. **Where:** card body.
- **`reviewer_priorities[REFINE]` — refine `"Will management actually deploy and supervise this capacity?"`** to add: "...AND is there evidence the supervising role(s) have bandwidth, not just title authority?" Why: the current phrasing accepts a name; the refinement demands span-of-control evidence per `common_red_flags.hidden_management_weakness`. **Seat affected:** Judge + Red Team. **Where:** card body.
- **`reviewer_types[NEW]` — add `"public_sector_capacity_program_officer"`** to reviewer_profile_typical. Why: public-sector capacity programs (HUD CB, USDA CB, Workforce-system capacity grants) have program officers distinct from foundation capacity reviewers; absent from current 6-type list. **Seat affected:** Scribe + Judge. **Where:** card body.

### §4.2 evidence capture / missing-evidence prompts (evidence_weights)

- **`evidence_weights[NEW]` — add `current_state_baseline_metrics`.** weight = HIGH. rationale = "Baseline operational metrics against which the post-investment gain will be measured: current turnaround time, current backlog size, current service volume, current data-quality scores, current staff retention rate. Distinguishes a capacity-grant ask from a vague 'we feel understaffed' pitch." Why: missing from current evidence_weights despite being implicit in the `measurable_capacity_gain` underwriting criterion + `no_measurable_capacity_gain` red flag. Surfacing as an explicit evidence kind makes Scribe demand baseline data at intake. **Seat affected:** Scribe + Judge + Logician. **Where:** card body.
- **`evidence_weights[NEW]` — add `prior_capacity_work_history`.** weight = MEDIUM. rationale = "Documented prior capacity-building work (strategic plans completed, systems implemented, governance changes adopted): demonstrates organizational learning capacity and informs Ford BUILD / Kresge LIFT / community-foundation reviewers about capacity-investment absorption track record." Why: Ford BUILD reviewers in particular weight prior-capacity-work narratives; current evidence_weights doesn't capture this. **Seat affected:** Scribe + Judge. **Where:** card body.
- **`evidence_weights[NEW]` — add `change_management_plan`.** weight = MEDIUM. rationale = "For systems-implementation or staffing-restructure asks: how the organization will absorb the change (communication plan, training cadence, resistance-management posture, rollback option). Distinguishes mature capacity asks from naïve technology-pitch capacity asks." Why: applies particularly to the new `data_systems_adoption_readiness` underwriting criterion (§4.1 above). **Seat affected:** Scribe + Judge + Red Team. **Where:** card body.
- **`evidence_weights[REFINE]` — refine `staffing_plan` rationale.** Currently reads: "Named role(s), job description scope, supervision structure, integration plan with existing team." Add: "...and evidence the supervisor has bandwidth — span-of-control delta from current state, not just title authority." Why: aligns with §4.1 refined `reviewer_priorities` entry. **Seat affected:** Scribe + Judge. **Where:** card body.

### §4.3 scoring weight patterns + evidence_weights (Judge-side rubric logic)

- **`scoring_weight_patterns[REFINE]` — refine both entries' `note` field.** Add cross-reference text: "Judge: when the funder's actual published NOFO scoring criteria are available (federal NOFOs always; some foundation RFPs), consult those directly. These tier assignments serve as fallback when funder rubric is unpublished or in flux. Per OQ-6 quantification threshold (12+ CycleReceipts), numeric weights are NOT introduced from this dispatch." Why: tightens the operator-defensible-but-illustrative caveat already present; routes Judge to authoritative funder rubrics first. **Seat affected:** Judge. **Where:** card body.
- **`scoring_weight_patterns[NEW]` — add `"Community foundation capacity-rubric typical pattern"`.** weights: `organizational_capacity: HIGH + governance: HIGH + sustainability: HIGH + measurable_capacity_gain: HIGH + budget_to_task: MEDIUM + dependency_risk: MEDIUM`. source_citation: Capital Region Community Foundation + Vermont CF (already in primary_sources). note: "Community foundations weight governance + sustainability higher than national foundation capacity rubrics because community foundations underwrite local-organization durability. Tier assignments are author qualitative judgment; subject to Lessons Memory revision over 12+ CycleReceipts." Why: 3rd rubric pattern alongside the existing "Foundation capacity-building rubrics (typical)" and "Federal NOFO capacity-building" entries; community foundations are a high-volume funder category for capacity grants and currently fold into the generic foundation pattern. **Seat affected:** Judge. **Where:** card body.

### §4.4 drafting register / admin-risk handling (Law 4 + OD-A v2.4)

- **`admin_risk_term_register` migration status (informational only).** Per OD-1 path (a) the per-card admin_risk_term_register field is REMOVED from this card; the workspace-wide `admin_risk_register.yaml` v2.2/v2.4 is the authoritative surface. The 8 Cycle-1-era CLC-03 admin-risk entries (sustainability, infrastructure, scalability, capacity building, equity, innovation, transformation, stakeholder) are documented in the card's commentary block at lines 408–430 as workspace-register migration candidates pending operator-approval flow.
- **Operator decision queue item §5.1 below — workspace-register migration of CLC-03-specific admin-risk terms.** Per the card commentary at lines 421–425: "infrastructure (standalone), scalability, capacity building, innovation, transformation, stakeholder (standalone) are pending operator-approval migration to `admin_risk_register.yaml` v2.3 as a separate follow-on dispatch." OD-A v2.4 per master prompt §7 has already migrated 60 net-new terms across 7 Wave 2 CLC cards. For CLC-03 the operator contributed 1 entry (cross-flag on `community wealth-building` from CLC-06 + CLC-08). The CLC-03-specific 6 terms above are the v2.3-or-v2.5 candidates. **Per master prompt rule 9 + OD-A v2.4 schema (per_clc_register cells):** the migration entries should carry `per_clc_register: {operating_capacity: EXPECTED}` for "capacity building" (it's the term-of-art for this CLC) + `{operating_capacity: OK}` for "infrastructure" / "scalability" / "innovation" / "transformation" / "sustainability" + `{operating_capacity: AVOID}` for "stakeholder capitalism" (per existing workspace-register v2.2 framing). **Surface as operator decision; do NOT auto-rewrite.**
- **No new card-body admin_risk_term_register entries proposed from this dispatch** (per the OD-1 path (a) closure and the workspace-register migration discipline).

### §4.5 reviewer / rubric logic (already partly covered in §4.1, §4.3; remaining items)

- **`common_red_flags[NEW]` — add `"capacity ask without baseline operational metrics"`.** severity = HIGH. red_team_probe = "Where is the current-state operational baseline against which we measure the post-investment gain? Show me last year's turnaround time / backlog size / service volume / staff retention rate; show me how we'll measure the same metric at grant close." source_citation = "blueprint:section_18_card_system.md#§18.10-CLC-03 + practitioner: Grantsmanship Center capacity-building outcomes framing." Why: highest-frequency adversarial-probe-class against capacity asks; currently implicit in `no_measurable_capacity_gain` (HIGH) but missing-baseline framing is more diagnostic at intake. **Seat affected:** Red Team + Judge. **Where:** card body.
- **`common_red_flags[NEW]` — add `"data system selected before bottleneck identified"`.** severity = MEDIUM. red_team_probe = "Was the system chosen because the organization mapped its bottleneck to features the system provides — or because the system was attractive and a justification was built backward? Show the procurement evaluation criteria and the vendor-comparison matrix." Why: data-systems capacity asks routinely fail this probe; tightens the `systems_purchase_without_adoption_plan` (HIGH) probe with a complementary "system chosen before bottleneck identified" probe. **Seat affected:** Red Team + Judge. **Where:** card body.
- **`narrative_section_patterns[NEW]` — add `"Theory of Change / Logic Model for the Capacity Investment"`.** typical_word_count = "200-500". source_citation = "blueprint:section_18_card_system.md#§18.10-CLC-03 + practitioner: Bridgespan Nonprofit Starvation Cycle + BoardSource governance framing." note: "Foundation reviewers (Ford BUILD, Kresge LIFT, MacArthur) expect a one-page theory-of-change linking the capacity bottleneck to mission outcomes." Why: missing from current 7-section pattern; foundation capacity rubrics weight ToC explicitly. **Seat affected:** Scribe. **Where:** card body.
- **`narrative_section_patterns[NEW]` — add `"Lessons from Prior Capacity Work"`.** typical_word_count = "200-400". source_citation = "blueprint:section_18_card_system.md#§18.10-CLC-03 + Ford BUILD framing." note: "Foundation reviewers want evidence of organizational learning capacity — strategic plans implemented, systems adopted, governance changes that stuck. Distinguishes a capacity-investment-ready organization from a startup-shape capacity ask." Why: pairs with the new `prior_capacity_work_history` evidence_weight. **Seat affected:** Scribe + Judge. **Where:** card body.
- **`narrative_section_patterns[NEW]` — add `"Adoption / Change Management Plan"`** (applicable particularly to system-side asks). typical_word_count = "200-400". source_citation = "blueprint:section_18_card_system.md#§18.10-CLC-03." note: "When the capacity ask involves a system (CRM / analytics / case-management software / financial system), reviewers expect a discrete adoption plan: user-population, training schedule, ownership, fallback/rollback option, and post-go-live support model." Why: pairs with new `change_management_plan` evidence_weight (§4.2) and new `data_systems_adoption_readiness` underwriting criterion (§4.1). **Seat affected:** Scribe + Red Team. **Where:** card body.

### §4.6 red-team probes (CLC.common_red_flags.red_team_probe) — items not already covered

- **`common_red_flags[REFINE]` — refine `sustainability_as_future_grants` red_team_probe.** Current text: "If no future grant funded this capacity, what revenue would? Where is the diversification math?" Add: "...Show me the year-3 revenue line-by-line: which funder is committed, which is probable, which is speculative; what earned revenue tracks the new capacity; what's the cost-recovery model if applicable." Why: tightens the probe from a single question into the multi-line revenue projection foundation reviewers actually demand. **Seat affected:** Red Team. **Where:** card body.
- **`common_red_flags[REFINE]` — refine `weak_budget_mapping` red_team_probe.** Current text: "For each budget line, name the implementation-plan task it funds. Are there orphan line items?" Add: "...And conversely: for each implementation-plan task, name the budget line that funds it. Are there orphan tasks?" Why: bidirectional task-to-budget mapping is the actual reviewer check; current probe is unidirectional. **Seat affected:** Red Team. **Where:** card body.
- **`common_red_flags[NEW]` — add `"capacity investment over-fitted to a single key hire"`.** severity = HIGH. red_team_probe = "What's the contingency if the named hire doesn't materialize or leaves in year one? Is the capacity ask resilient to that?" Why: hidden-management-weakness (existing MEDIUM) is adjacent; this probe specifically tests the dependency_risk underwriting criterion at the hiring-pipeline layer. **Seat affected:** Red Team + Judge + Scribe. **Where:** card body.

### §4.7 reporting / commitment extraction (commitment_tracking_pattern; Report Generator v0.2 feed)

- **`commitment_tracking_pattern.typical_commitments_extracted[NEW]` — add `"organizational_strategic_plan_adopted"`.** measurement_method = "strategic plan title + board adoption date + plan period (e.g., 2026–2030) + named priorities + implementation milestone schedule." Why: capacity grants frequently fund strategic-planning capacity work; absent from current 8-types list. Per Grantsmanship Center framing on this card line 535: "the outcome of grant-funded capacity building projects will be a product such as a strategic plan." **Seat affected:** Report Generator. **Where:** card body.
- **`commitment_tracking_pattern.typical_commitments_extracted[NEW]` — add `"baseline_metric_to_target_metric_movement"`.** measurement_method = "named operational metric + baseline value at award + target value + measurement date + measurement protocol + audit method." Why: pairs with the new `current_state_baseline_metrics` evidence_weight (§4.2) and `capacity ask without baseline operational metrics` red flag (§4.5). Currently `turnaround_time_reduced` and `service_capacity_increased` and `data_quality_improved` capture three specific metric types; this entry generalizes to "any baseline-to-target metric the award produces." **Seat affected:** Report Generator + Archivist. **Where:** card body.
- **`reporting_requirements_typical.performance_reporting.content_required[NEW]` — add `"baseline-vs-actual comparison for named capacity-gain metrics"`** alongside the existing entries. Why: aligns with new commitment_tracking entry; closes the loop between award baseline and reporting deliverable. **Seat affected:** Report Generator. **Where:** card body.
- **`reporting_requirements_typical.note` — refine.** Current text (line 345) acknowledges HUD CB Programs cadence as "the modal pattern." Add: "Foundation cadence varies (Ford BUILD: annual; Kresge LIFT: annual; community foundations: semi-annual or annual per grant agreement; some federal CB programs: quarterly). Operator should consult per-funder grant agreement; Tilth surfaces the modal pattern only as a starting default." Why: prevents false-precision in the modal-pattern claim. **Seat affected:** Report Generator + Archivist. **Where:** card body.

### §4.8 memory namespace usefulness

Per architecture v7.0.11 §1.9: `cards:clc:operating_capacity:*` is the namespace. Recommend the following sub-keys be standardized for future seat consumption when seat-registration graduates per v0.2 first-wave loader (Run 1 Patch D5):

- `cards:clc:operating_capacity:underwriting_criteria` → underwriting_criteria
- `cards:clc:operating_capacity:scoring_weight_patterns` → scoring_weight_patterns
- `cards:clc:operating_capacity:evidence_weights` → evidence_weights
- `cards:clc:operating_capacity:common_application_forms` → common_application_forms
- `cards:clc:operating_capacity:narrative_section_patterns` → narrative_section_patterns
- `cards:clc:operating_capacity:budget_structure_conventions` → budget_structure_conventions
- `cards:clc:operating_capacity:reviewer_profile_typical` → reviewer_profile_typical
- `cards:clc:operating_capacity:common_portals` → common_portals
- `cards:clc:operating_capacity:common_red_flags` → common_red_flags
- `cards:clc:operating_capacity:reporting_requirements_typical` → reporting_requirements_typical
- `cards:clc:operating_capacity:compliance_obligations` → compliance_obligations
- `cards:clc:operating_capacity:commitment_tracking_pattern` → commitment_tracking_pattern

**Seat affected:** all consuming seats (Judge / Red Team / Scribe / Logician / Report Generator / Archivist). **Where:** architecture v7.0.11 §1.9 sets the namespace pattern; the per-card sub-key map is a v0.2 first-wave loader concern. Surface to operator as a v0.2 loader-graduation enumeration question.

### §4.9 regression tests and acceptance tests (tests/cards/ mirror)

Per master prompt §2 "Research task" item 8: the v0.1 + v0.2 test surface mirror is at `tests/cards/` per Run 1 Phase 1 §CR-4. The §4 v2.x.7 amendment claims a 36-test surface at `tests/logician/gates/test_f_cards_coupling_violation_extension.py`; that's gate-side, not card-content-side. **For card-content-side regression:** recommend a small `tests/cards/test_clc_operating_capacity_content.py` fixture that:

1. Loads the card YAML; asserts schema validation.
2. Asserts `lifecycle.draft_status == "signed"` + `lifecycle.runtime_loadable is True`.
3. Asserts `common_red_flags` contains the new HIGH-severity probes (post-§4.5 patch).
4. Asserts `commitment_tracking_pattern.typical_commitments_extracted` carries ≥10 entries (post-§4.7 patch).
5. Asserts no forbidden coupling field name (FORBIDDEN_FIELD_REGISTRY scan).
6. Asserts no value-position regex match outside exempt paths.

Pre-stage at the same time as the content-refresh ceremony bundles the §4 patches. Engineering-side.

### §4.10 Phase 4 fold-in discipline self-check (per master prompt rule 6 / §18.11 v1.1)

Each proposed change above scanned against the four refusals:

| Proposal | (a) structured-sub-field expansion on canonical entries? | (b) dedicated-field-name fork? | (c) compound enum value? | (d) literal canonical CIC/CLC slug in non-exempt value position? |
|---|---|---|---|---|
| §4.1 underwriting_criteria add `data_systems_adoption_readiness` | NO — adds new item, canonical item shape preserved | NO | NO | NO |
| §4.1 reviewer_priorities add / refine entries | NO | NO | NO | NO |
| §4.1 reviewer_types add `"public_sector_capacity_program_officer"` | NO | NO | NO | NO |
| §4.2 evidence_weights add `current_state_baseline_metrics` + `prior_capacity_work_history` + `change_management_plan` | NO — canonical `{weight, rationale}` shape preserved per OD-3 path (a) | NO | NO | NO |
| §4.2 evidence_weights refine `staffing_plan` rationale | NO | NO | NO | NO |
| §4.3 scoring_weight_patterns refine note + add community-foundation rubric | NO — qualitative tier (HIGH/MEDIUM/LOW) preserved per OQ-6 | NO | NO | NO |
| §4.4 admin_risk_term_register workspace-register migration | N/A — workspace-register decision, not card body | N/A | N/A | N/A |
| §4.5 common_red_flags add `capacity ask without baseline operational metrics` + `data system selected before bottleneck identified` | NO | NO | NO | NO |
| §4.5 narrative_section_patterns add ToC / Lessons / Adoption sections | NO | NO | NO | NO |
| §4.6 common_red_flags refine sustainability + budget probes; add over-fitted-to-single-hire | NO | NO | NO | NO |
| §4.7 commitment_tracking add strategic-plan + baseline-to-target entries; refine reporting note | NO | NO | NO | NO |
| §4.8 memory namespace sub-keys | N/A — architecture decision, not card body | N/A | N/A | N/A |
| §4.9 regression test pre-stage | N/A — test surface, not card body | N/A | N/A | N/A |

**Verdict:** No proposed change trips any of the four Phase 4 fold-in refusals. All proposals respect the OD-1 / OD-3 path (a) closures (no admin_risk_term_register field re-introduction; no evidence_weights source_citation extension). No proposal introduces a CIC × CLC coupling field or value-position literal.

---

## §5. Operator Decision Queue

Decisions that require Josh / operator approval before any patch dispatches:

1. **Workspace-register migration of CLC-03-specific admin-risk terms.** Per the card commentary at lines 408–430 (OD-1 path (a) closure rationale): `infrastructure` standalone, `scalability`, `capacity building`, `innovation`, `transformation`, `stakeholder` standalone — 6 terms pending operator-approval migration to `admin_risk_register.yaml` v2.3 (or v2.5 per OD-A v2.4 lineage). Per OD-A v2.4 schema, each migrated entry needs `per_clc_register: {operating_capacity: EXPECTED|OK|AVOID|PREFERRED}` cells + `context` + `alternatives` + `notes` + `migrated_from` + `approval_required: true`. **Surface as P0 for operator approval.** This is a workspace-register schema decision; not a card-body decision. Route to v2.x → v3.0 scrub workflow per master prompt §7.
2. **Ford BUILD scale-figure refresh.** Verbatim quote at line 496 cites `$1.6 billion across 600 grants` and `$2 billion total over 12 years`. Confirm against current Ford Foundation BUILD program page; if scale has shifted (it likely has — Ford BUILD has expanded since the verbatim was authored), refresh the quote. **Approval required.**
3. **Single Audit threshold update.** `compliance_obligations[1]` line 356 reads `$750,000/year (rising to $1M under 2024 update)`. Refine to "$750,000/year through FY2024; $1,000,000/year for FY beginning on or after October 1, 2024 per 2 CFR 200 (2024 final rule)." **Approval required** for the explicit refinement (operator may prefer a different wording).
4. **Data-systems-adoption-readiness underwriting criterion separation.** §4.1 proposes adding a discrete `data_systems_adoption_readiness` underwriting criterion that splits the current `staffing_or_systems_need` conflation. **Operator decides** whether the split is desired (it tightens specificity but adds a row to a 10-item list); recommended **YES** per the operating-capacity acceptance test on data-systems requests.
5. **Three new narrative_section_patterns (ToC / Lessons / Adoption).** §4.5 proposes adding three sections to the current 7-section pattern, bringing total to 10. Operator decides whether this aligns with the Wave 1 reference-card discipline (the §18 v1.1 narrow-corrective precedent was *fewer* refinements; this is a 3-add proposal). Recommend operator approval; the additions track standard foundation capacity rubric sections.
6. **`common_funders_observed` posture decision (Law-5 split for this CLC).** Per §2.3 above: the field is currently ABSENT. Two paths:
   - **Path A — Leave absent.** Scout discovers capacity funders dynamically from the underwriting_criteria + reviewer_profile + reviewer_priorities substance. No Law-5 violation surface.
   - **Path B — Apply CIC-mirror Phase E Option 2 pattern.** Add empty top-level `common_funders_observed: []` block + `_research_metadata.draft_funder_candidates_pending_operator_engagement_confirmation:` nested block with Ford BUILD / MacArthur Field Support / Kresge LIFT / Hewlett / Bush Foundation / community foundations (Capital Region, Vermont, etc.) as subagent-populated candidates pending operator engagement confirmation. Cross-card consistency with the 6 CIC cards. Requires Run 1 Patch B20 (schema-known field for `_research_metadata.draft_funder_candidates_*`).

   **Recommendation:** Path B for cross-card uniformity, conditioned on Run 1 Patch B20 landing first. Per master prompt §0 "Law-5 split on common_funders_observed unconfirmed for CLC cards (surface state)" — this dispatch surfaces the absent state. **Approval required: Path A or Path B.**
7. **Bridgespan Nonprofit Starvation Cycle and BoardSource added as practitioner sources.** §3.2 proposes adding these as `_research_metadata.priors_consulted` / source-cite supplements. Operator decides whether these meet the "operator-grade reference" bar for inclusion in the card's primary_sources block (vs staying as out-of-card priors).
8. **Re-signing ceremony budget for card body changes.** Per operator reframe (aggressive content OK; re-signing ceremony cost acceptable): the §4 proposals above touch ~20 distinct card-body edits across `underwriting_criteria` / `evidence_weights` / `scoring_weight_patterns` / `narrative_section_patterns` / `common_red_flags` / `commitment_tracking_pattern` / `reporting_requirements_typical` / `reviewer_profile_typical`. **Bundle into cards-ceremony per Run 1 Patch Queue Batch B** as `operating_capacity` supersession-re-sign? OR run as a separate Phase 4-CLC-derived content-refresh ceremony post-cards-ceremony? **Recommendation:** separate content-refresh ceremony AFTER the cards-ceremony lands the §18 v1.2 + §18.6 v2 reconciliation, because operating_capacity is single-track (not part of §18.6 v2 restructure) and the §18 v1.2 dialect_routing_table re-keying is CIC-side only (no impact on CLC body content).
9. **OD-4 follow-on hygiene dispatch — Internet Archive snapshot pass.** Per the card's lifecycle commentary at line 463–464 (OD-4 deferred 2026-05-15 PM). Re-confirm Wayback snapshots of all 14 primary_source URLs before the content-refresh ceremony fires; priority order per §3.3 above. **Operator decides** ceremony timing.
10. **Lock-history housekeeping field disposition.** Per Run 1 Patch E1 + Phase 1 L1-F8: `lifecycle.lock_history_row` / `lock_timestamp_utc` / `supersession_lock_history_row` not in `models.py.Lifecycle`. Cross-card decision; not specific to operating_capacity. Surface to cards-ceremony.

---

## §6. Validation Checklist

| Check | Result | Evidence |
|---|---|---|
| Schema fields complete against current §18.5 / §18.6 schema | PASS | 15/15 required CLC fields present per `card_clc.schema.json:7-23`; lifecycle block satisfies allOf conditional at lines 318–369 (runtime_loadable=true → draft_status=signed AND signature_status=signed AND runtime_load_status=loaded; signed_at/signed_by/content_hash present) |
| No forbidden coupling field names (top-level + nested per item-level not.anyOf) | PASS | Grep across the file: none of 6 forbidden CLC-side names (`eligible_cic_subset`, `cic_allowlist`, `cic_denylist`, `preferred_cics`, `cic_win_rate`, `cic_ranking_preferences`) appear anywhere |
| No forbidden value-position regex matches outside exempt paths | PASS | Per §2.4 above — 0 non-exempt findings; all hits are in `card_id` / `tilth_clc_id` / `_research_metadata.priors_consulted[*].extract_note` (all exempt) |
| No legacy-phrase `[Cc]ustomer [Ii]nformation` matches (defense-in-depth) | PASS | 0 hits — verified by grep |
| No private organization-specific data in card body | PASS | Card carries no client-specific data; funder names referenced (Ford, MacArthur, Kresge, etc.) are public-foundation references, not client engagement |
| No unsourced program-law claims | PASS at body | Verbatim quotes ≤2 sentences per OQ-4 throughout; statutory anchors are CFR (2 CFR 200, 7 CFR Part 3406) and official program URL. Single Audit threshold "rising to $1M under 2024 update" gloss is operator-defensible but recommend tightening per §5.3 / §2.2 |
| No excessive verbatim source text | PASS | Verbatim quotes capped at ≤2 sentences per primary_source row per OQ-4 |
| Lifecycle status consistent with architecture v7.0.11 §1.5 production-load requirements | PASS | All five lifecycle gate fields at pass-state; runtime_loadable=true; content_hash present; signed_at + signed_by present; lock_history_row 227 |
| Law-5 split on `common_funders_observed` per operator v2.1 reconciliation | **UNCONFIRMED (field absent)** | Field absent on this card — see §2.3 + §5.6 operator decision queue item |
| `_oq6_anchor: true` defense-in-depth marker | PASS | Line 87 — schema-passes-by-additionalProperties:true; AST-lint R-CARDS-NO-NUMERIC-WEIGHT hookup deferred to v1.x amendment-realization checklist per file commentary |
| For multi-track CLCs: shared root metadata + oneOf branch 2 compliance | N/A — this is a single-track CLC (oneOf branch 1) |

**Net coupling-discipline regression: 0 findings.**

---

## §7. Regression Tests

Five prompts that should demonstrate behavior change between pre-edit and post-edit cards. Each prompt + expected pre-edit behavior + expected post-edit behavior + which seat changes.

### Test 1 — "Need more staff" acceptance test (per plan §2.3)

**Prompt:** "We need to apply for capacity-building funding because our small organization is overworked — we need more staff."

**Pre-edit behavior (current card):**
- Scribe drafts a generic operating-support narrative; surfaces the `capacity_bottleneck` underwriting criterion prompt ("Specific, current operational constraint... not aspirational future need") but accepts "we are overworked" as proximate justification.
- Logician fires `common_red_flags.vague_operating_support_request` (HIGH) — operator approves once.
- Red Team probes for specific constraint + timeframe + observable change.
- Scribe surfaces `staffing_or_systems_need` (job description required), `implementation_plan` (timeline + owners), `budget_to_task_integrity` (line items mapped), `sustainability` (revenue math).

**Post-edit behavior (with §4.1 + §4.5 additions):**
- Scribe additionally surfaces the new `reviewer_priorities` entry: "Is the evidence base for the capacity ask grounded in current organizational data (not 'we feel understaffed')?" — demands baseline operational metrics at intake.
- Red Team fires the new `common_red_flags.capacity ask without baseline operational metrics` (HIGH) probe: "Where is the current-state operational baseline... show me last year's turnaround time / backlog size / service volume / staff retention rate."
- Scribe demands a `current_state_baseline_metrics` evidence (new evidence_weight HIGH) before draft completes.
- Result: applicant prompted for baseline operational metrics (not just job description) in first response; "overworked" alone does not satisfy.

**Seat affected:** Scribe + Logician + Red Team + Judge. **Pass criterion:** Scribe demands baseline metric data at intake; Red Team fires the baseline-absent probe; the existing `bottleneck` + `staffing_or_systems_need` + `implementation_plan` + `sustainability` prompts also fire (per the plan §2.3 acceptance test).

### Test 2 — "Need a CRM" software/system request acceptance test (per plan §2.3)

**Prompt:** "We need a CRM to manage donor records — we're applying for a $50K foundation capacity grant to buy Salesforce."

**Pre-edit behavior (current card):**
- Scribe surfaces `staffing_or_systems_need` underwriting criterion + `evidence_weights.systems_audit` (MEDIUM) + `common_red_flags.systems_purchase_without_adoption_plan` (HIGH).
- Red Team probes adoption plan + training plan + staff resistance.
- Scribe surfaces `commitment_tracking_pattern[systems_implemented]` measurement method (system name + go-live date + user count + adoption rate).
- No discrete data-system-vs-staffing distinction at the underwriting level — Scribe folds CRM ask into generic staffing/systems framing.

**Post-edit behavior (with §4.1 + §4.2 + §4.5 additions):**
- Scribe surfaces the new `data_systems_adoption_readiness` underwriting criterion separately from generic staffing/systems-need framing — demands explicit user-population + data-migration plan + training schedule + ownership/governance + post-go-live support model.
- Scribe surfaces new `evidence_weights.change_management_plan` (MEDIUM) — demands the change-management content.
- Red Team fires the new `common_red_flags.data system selected before bottleneck identified` (MEDIUM) probe: "Was the system chosen because the organization mapped its bottleneck to features the system provides — or because the system was attractive and a justification was built backward?"
- Scribe surfaces new `narrative_section_patterns[Adoption / Change Management Plan]` (200-400 words) — demands a discrete adoption section, not embedded prose in the budget justification.
- Result: applicant prompted for adoption plan + data migration + training + ownership + measurable operating gains (per the plan §2.3 acceptance test) PLUS the procurement-process probe.

**Seat affected:** Scribe + Red Team + Judge. **Pass criterion:** all five plan-§2.3 acceptance-test prompts fire (adoption plan / data migration / training / ownership / measurable operating gains) PLUS the bottleneck-precedes-selection probe.

### Test 3 — Sustainability-as-revenue-math discipline

**Prompt:** "Our capacity grant proposal says 'we'll diversify funding over the next three years' for sustainability."

**Pre-edit behavior (current card):**
- Logician fires `common_red_flags.sustainability_as_future_grants` (HIGH) with the existing red_team_probe: "If no future grant funded this capacity, what revenue would? Where is the diversification math?"
- Scribe surfaces `narrative_section_patterns[Sustainability Plan]` (300-600 words).
- Result: probe demands diversification math at the single-question level.

**Post-edit behavior (with §4.6 refined probe):**
- Logician fires the refined `sustainability_as_future_grants` probe: "If no future grant funded this capacity, what revenue would? Show me the year-3 revenue line-by-line: which funder is committed, which is probable, which is speculative; what earned revenue tracks the new capacity; what's the cost-recovery model if applicable."
- Result: probe demands the multi-line year-3 revenue projection foundation reviewers actually want — not just "diversification math" as a phrase.

**Seat affected:** Red Team + Scribe. **Pass criterion:** Red Team probe demands line-by-line year-3 revenue projection with committed / probable / speculative + earned-revenue tracking + cost-recovery model (if applicable).

### Test 4 — Theory-of-change-for-capacity surfacing

**Prompt:** "We're applying for Ford BUILD — they want a five-year operating-support narrative with institutional strengthening overlay."

**Pre-edit behavior (current card):**
- Scribe drafts against the 7-section `narrative_section_patterns` (Org Background / Capacity Need / Proposed Investment / Staffing-Systems / Outcomes / Sustainability / Budget Justification).
- No discrete Theory-of-Change section; ToC content folds into Org Background or Capacity Need.

**Post-edit behavior (with §4.5 new section):**
- Scribe surfaces the new `narrative_section_patterns[Theory of Change / Logic Model for the Capacity Investment]` (200-500 words) — demands a one-page ToC linking the bottleneck to mission outcomes.
- Scribe surfaces the new `narrative_section_patterns[Lessons from Prior Capacity Work]` (200-400 words) — demands evidence of organizational learning capacity.
- Scribe surfaces new `evidence_weights.prior_capacity_work_history` (MEDIUM) — demands documented prior strategic-plan / systems / governance work.
- Judge weights ToC + Prior Capacity Work explicitly against Ford BUILD reviewer expectations.

**Seat affected:** Scribe + Judge. **Pass criterion:** narrative carries discrete ToC + Lessons sections; evidence_weights includes prior_capacity_work_history at MEDIUM.

### Test 5 — Community-foundation-specific rubric routing

**Prompt:** "We're applying to a community foundation for a $25K capacity-building grant focused on bylaws update + executive succession planning."

**Pre-edit behavior (current card):**
- Judge cross-checks against `scoring_weight_patterns[1]` (foundation capacity-building typical: organizational_need HIGH / project_design HIGH / organizational_capacity HIGH / sustainability MEDIUM).
- No community-foundation-specific rubric pattern; community foundations fold into the generic foundation pattern even though they weight governance + sustainability higher.

**Post-edit behavior (with §4.3 new rubric pattern):**
- Judge cross-checks against the new `scoring_weight_patterns[Community foundation capacity-rubric typical pattern]`: organizational_capacity HIGH + governance HIGH + sustainability HIGH + measurable_capacity_gain HIGH + budget_to_task MEDIUM + dependency_risk MEDIUM.
- Judge weights governance + sustainability higher for community foundation reviews — surfaces stronger Letter of Commitment from Board Chair + sustainability revenue math expectations.
- Per the source_citation chain (Capital Region CF + Vermont CF in primary_sources), Judge cross-references the actual published criteria where available.

**Seat affected:** Judge. **Pass criterion:** Judge applies community-foundation-rubric pattern when funder type is identified as community foundation; raises governance + sustainability weights above the generic foundation default.

---

## §8. Patch Plan

Edits proposed in this handback grouped by file path. **No edits applied from this dispatch.** Operator dispatches each ceremony separately per the OD-C / OD-E precedent (per-card lock_history supersession row + post-restructure SHA3-512 + publisher Ed25519 signature against `vault_shared/cards/publisher_pubkey.signed.yaml`).

### File: `pipeline/cards/CLC/operating_capacity.yaml`

**Ceremony shape:** supersession-re-sign per OD-E precedent (rows 276 / 277 / 278 model — single-track variation). Parent_lock_row = 227 (Wave 1 LOCK). Ceremony_parent_row = `<NEXT-AVAILABLE-COMPOUND-PARENT>` if bundled, OR `<NEXT-AVAILABLE>` standalone.

**Recommendation:** sequence as a separate content-refresh ceremony AFTER the Run 1 Batch B cards-ceremony lands §18 v1.2 + §18.6 v2 reconciliation. `operating_capacity` is single-track (not part of §18.6 v2 restructure) and the §18 v1.2 dialect_routing_table re-keying is CIC-side only; bundling with the cards-ceremony adds dependency without payoff.

**Edit set (per §4 above):**

1. `underwriting_criteria[NEW]` — add `data_systems_adoption_readiness` (§4.1).
2. `reviewer_profile_typical.reviewer_priorities[NEW]` — add `"Is the evidence base for the capacity ask grounded in current organizational data..."` (§4.1).
3. `reviewer_profile_typical.reviewer_priorities[REFINE]` — refine management-deployment entry to add span-of-control evidence (§4.1).
4. `reviewer_profile_typical.reviewer_types[NEW]` — add `public_sector_capacity_program_officer` (§4.1).
5. `evidence_weights[NEW]` — add `current_state_baseline_metrics` (HIGH) + `prior_capacity_work_history` (MEDIUM) + `change_management_plan` (MEDIUM) (§4.2).
6. `evidence_weights[REFINE]` — refine `staffing_plan` rationale (§4.2).
7. `scoring_weight_patterns[REFINE]` — refine note on both existing entries (consult-funder-NOFO cross-reference) (§4.3).
8. `scoring_weight_patterns[NEW]` — add `"Community foundation capacity-rubric typical pattern"` (§4.3).
9. `common_red_flags[NEW]` — add `capacity ask without baseline operational metrics` (HIGH) + `data system selected before bottleneck identified` (MEDIUM) + `capacity investment over-fitted to a single key hire` (HIGH) (§4.5 + §4.6).
10. `common_red_flags[REFINE]` — refine `sustainability_as_future_grants` red_team_probe (year-3 revenue line-by-line) + refine `weak_budget_mapping` red_team_probe (bidirectional task↔budget mapping) (§4.6).
11. `narrative_section_patterns[NEW]` — add `Theory of Change / Logic Model for the Capacity Investment` + `Lessons from Prior Capacity Work` + `Adoption / Change Management Plan` (§4.5).
12. `commitment_tracking_pattern.typical_commitments_extracted[NEW]` — add `organizational_strategic_plan_adopted` + `baseline_metric_to_target_metric_movement` (§4.7).
13. `reporting_requirements_typical.performance_reporting.content_required[NEW]` — add `baseline-vs-actual comparison for named capacity-gain metrics` (§4.7).
14. `reporting_requirements_typical.note` — refine to acknowledge foundation cadence variance (§4.7).
15. `compliance_obligations[1].typical_filings` — refine Single Audit threshold gloss to "$750,000/year through FY2024; $1,000,000/year for FY beginning on or after October 1, 2024 per 2 CFR 200 (2024 final rule)" (§2.2 / §5.3).
16. **Conditional on §5.6 Path B operator decision:** add empty `common_funders_observed: []` block + `_research_metadata.draft_funder_candidates_pending_operator_engagement_confirmation:` nested block with Ford BUILD / MacArthur Field Support / Kresge LIFT / Hewlett / Bush Foundation / community foundations (Capital Region, Vermont). Requires Run 1 Patch B20 (schema-known field) to land first.
17. `_research_metadata.primary_sources[REFRESH]` — refresh Ford BUILD URLs + verify Wayback snapshots per §3.3 / §5.9 (OD-4 follow-on dispatch).
18. `_research_metadata.primary_sources[NEW]` — add Bridgespan Starvation Cycle + BoardSource if operator approves per §5.7.

**Re-sign discipline:** Patched card gets new Ed25519 signature; `lifecycle.content_hash` updated to match new canonical bytes; new lock_history row appended with `parent_lock_row: 227` (Wave 1 LOCK) and `ceremony_parent_row: <NEXT-AVAILABLE>`. Header comments not in canonical bytes; no separate header-comment ceremony needed for this card (lines 1–18 reflect current state accurately).

### File: `pipeline/cards/_schema/card_clc.schema.json`

**Ceremony shape:** schema patch per cards-ceremony (Run 1 Patch B20).

**Edit (conditional on §5.6 Path B operator decision):** add `_research_metadata.draft_funder_candidates_pending_operator_engagement_confirmation:` optional property mirroring `common_funders_observed.items` shape (with the same nested `not.anyOf` defense-in-depth). Description: "Subagent-populated funder candidates pending operator engagement confirmation. Operator graduates entries to top-level `common_funders_observed:` as engagement is confirmed. Per Law 5 + operator's v2.1 reconciliation patch (2026-05-17)."

### File: `pipeline/institutional_memory/admin_risk_register.yaml`

**Ceremony shape:** workspace-register v2.3 (or v2.5 per OD-A v2.4 lineage) migration ceremony — separate from card-content ceremony.

**Edit (per §4.4 + §5.1 operator decision):** add 6 CLC-03-specific admin-risk terms (`infrastructure` standalone, `scalability`, `capacity building`, `innovation`, `transformation`, `stakeholder` standalone) with `per_clc_register: {operating_capacity: EXPECTED|OK|AVOID|PREFERRED}` cells per OD-A v2.4 schema. Operator-approval-required flow per OD-1 path (a) closure rationale.

### Forward-binding contract note (per OD-D Phase 4 / R-CARDS-ENUM-CANONICAL OD-B)

Per master prompt §2 final-instruction item: any proposal touching refusal (c) or (d) territory (compound enum / literal slug) must be marked for R-CARDS-ENUM-CANONICAL (OD-B, pending) or F-CARDS-COUPLING-VIOLATION-EXTENSION regression hardening at v0.2. **No proposal in this handback touches (c) or (d) territory.** No forward-binding marker required.

---

```
Card: CLC:operating_capacity
Card file: pipeline/cards/CLC/operating_capacity.yaml
Research hours actual: 2.4
Findings: 23 total — 2 P0, 12 P1, 9 P2
Decision queue: 10 operator approvals required
Conflicts with prior art: NONE
Coupling-discipline regression: NONE
Lifecycle gap surfaced: draft_status reads "signed" on disk; no normalization required per Run 1 P0-3
Review readiness: READY
```
