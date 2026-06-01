# TILTH-CLC-08 Shared Assets — Research Handback

**Filed:** 2026-05-17
**Workspace:** `/Users/goldenquill/Downloads/GoldenQuill/`
**Run:** Phase 4 CLC handbacks; 8 of 8 (Shared Assets — final CLC in the Wave 2 single-track roster).
**Card:** `pipeline/cards/CLC/shared_assets.yaml` (Wave 2 LOCKed 2026-05-16 row 261; SHA-256 `ba122d…37db2`; signed `2026-05-16T16:00:00Z`).
**Authority chain:** master prompt §2 + §5 + §7 + Run 1 priors (binding).
**Run 1 priors folded in:** all 14 cards on disk read `lifecycle.draft_status: "signed"` (the master prompt's universal `draft_status: "draft"` claim is stale for the on-disk state — Shared Assets is in compliance); §18 v1.2 dialect_routing_table schema delta LOCKed-but-not-applied at the card-body layer (Shared Assets has no `dialect_routing_table` field, so this bottleneck does not bind here); operator v2.1 Law-5 split applied workspace-wide; F-CARDS-COUPLING-VIOLATION-EXTENSION value-position regex LIVE at predicate-body layer per OD-C row 272; operator reframe = aggressive content improvements OK.
**Card-specific note:** Wave 2 Thesis trail records that CLC-08 used the comment-block-only Phase 4 fold-in fallback (master prompt §2 prompt body rule 6 last paragraph + §18.11 v1.1) at Cycle-2 FIX-IN-PLACE 2026-05-16 to retire the schema-incompatible `admin_risk_term_register` field while preserving the operator-decision substrate as a YAML comment block routed to `_review_handback.decision_queue`. Structural-gap findings in this handback that cannot be expressed within the canonical CLC schema route to the same fallback pattern.

---

## §1. Card Impact Thesis

`shared_assets` is the only CLC in the canonical eight that underwrites *governance of an asset held in common by multiple parties* — not the asset, not the borrower, not the program of services, but the joint-use shape. Its job is to make Tilth **read shared-asset asks through the seven structural primitives reviewers actually weigh — shared need, governance, access policy, utilization evidence, maintenance + replacement reserves, asset control + site control, and equitable-access protections — and to refuse single-applicant capacity requests that are merely framed as shared.**

What this card should cause Tilth to do differently:

1. When Scout sees `community facility`, `food hub`, `shared-use kitchen`, `aggregation facility`, `cold storage`, `tool library`, `equipment library`, `maker space`, `commissary kitchen`, `community land trust (CLT)`, `cooperative-services center`, anchor to USDA RD Community Facilities Direct Loan + Grant (7 CFR Part 3570) + USDA RCDG (7 CFR Part 4284 Subpart F) + USDA AMS LAMP (RFSP / FMPP / LFPP / TOPP under 7 CFR Part 1463) + USDA NIFA CFP + CDFI Fund HFFI + Reinvestment Fund / Capital Impact Partners CDFI underwriting practice + Kresge / Surdna / Knight community-development capital-grant rubric anatomy.
2. When Scribe drafts a shared-asset narrative, force the seven-structural-primitive Section spine — Shared Need (with multi-user demonstration) / Asset Description / User Base + Commitments / Governance + Decision Structure / Access + Equity Policy / Operations Plan / Maintenance + Replacement Reserve / Budget + Capital Cost / Sustainability + Cost Recovery / Community Member Benefit. The single most weight-bearing section is Shared Need — Scribe must surface evidence that multiple users genuinely need the asset, not a single applicant in shared-asset framing.
3. When Logician audits a draft, fire the eleven `common_red_flags` adversarial probes — single-party-capture / unclear-governance / vague-access-rules / unfunded-maintenance / assumed-utilization-no-demand-evidence / no-scheduling-or-conflict-process / unresolved-site-control / ignored-replacement-cost / no-insurance-plan / missing-user-member-commitments / single-applicant-shaped-as-shared-asset — and require evidence at every applicable claim. The single-applicant-shaped-as-shared-asset probe is the load-bearing CLC-boundary defense — when applicants frame an Operating Capacity (CLC-03) ask as a Shared Assets ask, this probe routes them to the correct CLC.
4. When Report Generator extracts commitments from an awarded shared-asset proposal, surface the eleven canonical commitment types per `commitment_tracking_pattern.typical_commitments_extracted` — users_served, utilization_hours, bookings_count_and_diversity, maintenance_logs_completed, downtime_planned_and_unplanned, cost_recovery_revenue_vs_expense, **access_equity_distribution** (uniquely a Shared Assets reporting axis — no other CLC reports access-equity Lorenz / Gini distribution), repairs_completed, replacement_reserve_contributions, community_benefit_outcomes — into the CLC-namespaced `clc_shared_assets_commitments` field per Wave 1 F6 fold-in convention.
5. When Logician audits a draft using `commons`, `community wealth`, `cooperative ownership`, `collective ownership`, `pooled resources`, `right to access`, `shared infrastructure`, `equity`, or `sustainability` in a federal-conservative NOFO, fire workspace `admin_risk_register.yaml` v2.4 substitution candidates (substantive-preserving) and require operator approval per `approval_required: true` — NEVER silently rewrite. Operator-grade carve-out: borrower-equity (financial-capital, not DEI framing) is GREEN-tier across all funder contexts.
6. When the active opportunity is USDA RD CF Direct Loan, surface CDFI-grade financial-feasibility scaffolding (DSCR ≥ 1.20 baseline, replacement-reserve adequacy, 30–40 year amortization-period covenant compliance horizon). When the active opportunity is USDA RD CF Grant (partial-grant tier for low-population highly-distressed communities), surface community-need + community-benefit scaffolding. When CDFI debt-financed, surface borrower-equity (10–30% typical) + collateral + site-control discipline.
7. When applicant entity is municipality / school district / public agency vs cooperative vs nonprofit vs CLT, surface the appropriate governance-documentation grammar (authorizing resolution + operating ordinance for public bodies; bylaws + patronage model for cooperatives; board minutes for nonprofits; trust instrument + recorded covenant for CLTs).

The runtime-behavior delta this card produces is **seven-structural-primitive discipline (shared need + governance + access + utilization + maintenance + asset control + equitable access) + adversarial single-party-capture defense + access-equity-distribution as a uniquely-CLC-08 reporting axis + admin-risk-vocabulary discipline routed through the workspace register.** The card is currently strong on all four.

---

## §2. Current State Audit

### §2.1 What is strong now

- **Seven-structural-primitive density in `underwriting_criteria`.** Eleven criteria spanning shared_need / user_base / governance / access_policy / utilization / maintenance / asset_control / cost_recovery / equitable_access / replacement_reserve / community_member_benefit. The `access_policy` criterion (lines 65–67) enumerates the six standard sub-components (booking + member-class + conflict-resolution + fee schedule + non-discrimination + onboarding) — the kind of operator-defensive list that prevents reviewer hand-waving. The `asset_control` criterion (lines 80–83) preempts the title-holder-ambiguity hold by surfacing the eleven legal-structure categories upfront and explicitly noting the categories are NOT tied to any specific CIC archetype — strong opportunity-driven orthogonality discipline.
- **Five-rubric `scoring_weight_patterns`.** USDA RD CF + USDA RCDG + USDA AMS LAMP RFSP + Foundation community-development + CDFI shared-asset financing. Per-rubric tier assignments use the qualitative HIGH/MEDIUM/LOW vocabulary per OQ-6. Each rubric has source_citation + a `note` explicitly disclaiming per-NOFO / per-deal variance and routing to Scout fetchOpportunity for cycle-specific weights. The "specific funder names removed from binding field per Law 5 + Phase F 2026-05-16 cleanup" note on entries 4 and 5 documents the Law-5 anonymization pattern cleanly.
- **Thirteen `evidence_weights` entries.** Five HIGH-weight load-bearing evidence kinds (user_member_commitments / governance_agreement / access_policy / site_control / equipment_quote / utilization_forecast / maintenance_budget / replacement_reserve_documentation / shared_use_agreement_template) with explicit `rationale` per kind and `source_citation` per Wave 1 OD-3 convention. The `replacement_reserve_documentation` weight was upgraded MEDIUM→HIGH at Cycle-1 fold-in to match `common_red_flags.ignored_replacement_cost` (HIGH) — internal-consistency discipline.
- **Eleven `common_red_flags` adversarial probes.** Each with explicit `red_team_probe` interrogative-form prose, severity tier, and several with `source_citation`. The `single_applicant_shaped_as_shared_asset` flag (lines 480–483) is the CLC-boundary defense — explicitly routes the request to Operating Capacity (CLC-03) or Market Access (CLC-05) when the lead applicant has substantial existing capacity. The `commons_framing_in_conservative_federal_context` flag (lines 485–487) cleanly cross-references the admin-risk register without restating it.
- **Eleven `commitment_tracking_pattern.typical_commitments_extracted` entries.** Each with `commitment_type` + `measurement_method`. The `access_equity_distribution` entry (lines 633–634) is uniquely a CLC-08 reporting axis — names Lorenz curve / Gini coefficient (or simpler quartile share, smallest-user-share, top-decile-concentration) and explicitly notes "Decline in smallest-user-share over time is an early-warning indicator that access-policy enforcement is failing in practice." This is the kind of operationally-precise commitment-extraction language that gives Report Generator something measurable to surface.
- **Twelve `compliance_obligations` frameworks.** 2 CFR Part 200, 7 CFR Part 3570 (USDA RD CF), 7 CFR Part 1463 (USDA AMS LAMP), Single Audit Act, state cooperative/LLC governance, commercial property + liability insurance, ADA, FSMA + state retail food code, state cottage food laws, municipal zoning + permitting, Davis-Bacon Act, NEPA. Deeper compliance-stack coverage than most CLCs — appropriate given the capital + multi-party + multi-regulatory-domain shape of Shared Assets projects.
- **Eleven `common_application_forms`.** SF-424 family + USDA RD CF application package + USDA AMS LAMP NOFO + USDA RCDG + USDA NIFA CFP + foundation portals (Foundant/Submittable/Fluxx) + CDFI lender packets + state community-development authority applications. Wide-spectrum funder-pathway coverage.
- **Comprehensive header-comment governance-spectrum framing (lines 11–23).** Eight CIC-illustrative examples cleanly demonstrate the breadth of who-may-hold-title for a shared asset (501(c)(3) food hub / municipality public library / CLT-held CSA farm / school district shared community kitchen / arts collective maker space / farm cooperative cold storage / public agency equipment library / ecosystem intermediary food hub). Explicitly preserves opportunity-driven runtime matching: "Any CIC may pursue Shared Assets funding when the opportunity's underwriting logic centers shared need, governance, equitable access, utilization, and maintenance-reserve discipline." This is the strongest opportunity-driven framing in the CLC body.
- **Phase 4 fold-in discipline cleanly executed.** Cycle-2 FIX-IN-PLACE 2026-05-16 retired the schema-incompatible `admin_risk_term_register` block (CLC-axis was not declared by §18.6) and routed the 9 CLC-08-scoped flagged terms to the workspace-wide `admin_risk_register.yaml` v2.3 migration. The retired block is preserved as a YAML comment manifest at lines 648–694 — full migration audit trail in-place. This is the canonical comment-block-only Phase 4 fold-in fallback pattern cited in master prompt §2 rule 6.
- **Lifecycle in compliance.** `draft_status: signed` (line 700) — no normalization needed. `runtime_loadable: true` (line 705) satisfies architecture v7.0.11 §1.5 production-load minimum. Signed at `2026-05-16T16:00:00Z`; lock_history_row 261; embedded `ed25519_signature` LIVE (verify against Wave 2 row 261 in next loader-graduation cycle).

### §2.2 What is stale, ambiguous, over-broad, too local, too federal, or under-sourced

- **Replacement-reserve 5–15% convention from a single practitioner-guidance source.** The `replacement_reserve` criterion (line 96) + `maintenance_budget` evidence_weight + `replacement_reserve_documentation` evidence_weight all cite the same single Community Food Services PDF. Card's own `_review_handback.surface_ambiguities[0]` flags this. The 5–15% convention is the modal pattern in shared-use kitchen and food-hub planning literature, but Phase 4 deepening could triangulate against (a) USDA RD CF reserve-adequacy guidance (7 CFR Part 3570 references reserve requirements), (b) GAAP nonprofit reserve standards (FASB ASC 958), and (c) sector-specific industry standards (Institute of Real Estate Management for facility reserve studies). Single-source citation is a Logician fragility for a HIGH-weighted evidence kind.
- **No core_terms / synonym_map / funder_program_keywords / disqualifier_terms fields exist on CLC cards.** Per CLC schema baseline, the funder-side card does not carry the applicant-side search_vocabulary block — Scout's CLC-side matching reads opportunity vocabulary against `underwriting_criteria.criterion` names + `evidence_weights` field keys + `scoring_weight_patterns.rubric_example` strings + `common_funders_observed[*].funder_name`. The current card has rich `underwriting_criteria` + `evidence_weights` coverage but no `common_funders_observed` array populated. The schema declares it optional (not in `required` list per schema lines 7–23) and the card-body omits it entirely. **For Scout discoverability, an opportunity-driven match needs at least observational funder-roster anchoring.** Recommend adding `common_funders_observed` populated with the 11 funders already cited in the body (USDA RD CF, USDA RCDG, USDA AMS LAMP, USDA NIFA CFP, USDA CDFI HFFI, Reinvestment Fund, Capital Impact Partners, Kresge, Surdna, Knight, PA DCED Keystone Communities) — each with `funder_name` + `funder_type` (federal / federal regional / state / foundation) + qualitative `frequency_observed` per OQ-6 + optional `typical_award_range` + `note`. This is the highest-leverage discoverability gap.
- **No `provenance_requirements` block.** The CLC schema declares `provenance_requirements` as optional but not required (schema lines 7–23, 176–228). The card body omits it. A CLC-side `provenance_requirements` block would mirror the CIC pattern — per-fact-class `required_citation_type` + `verbatim_quote_required` for the eleven `evidence_weights` entries. This would force per-evidence-kind provenance discipline at Intake. **Recommend adding** `provenance_requirements` for the five HIGH-weighted evidence kinds (user_member_commitments / governance_agreement / access_policy / site_control / replacement_reserve_documentation) with explicit `required_citation_type` strings.
- **No `narrative_section_patterns` weight tiers, just section names + word counts.** The current ten narrative sections (lines 291–340) have `typical_word_count` + `source_citation` + `note` but no explicit `weight_in_funder_rubric` tier (HIGH/MEDIUM/LOW). The Shared Need section's `note` explicitly says "The single most weight-bearing section" — this should be encoded as a qualitative tier, not just prose. Other sections lack any tier signal. Recommend adding `weight_in_funder_rubric: HIGH | MEDIUM | LOW` per narrative_section to give Scribe a section-prioritization signal.
- **`common_funders_observed: NOT_POPULATED`.** As noted above — the schema declares optional, the card omits. Operator-decision route: populate with the 11 funders already cited (path a), OR leave omitted with rationale (path b — current state).
- **State-overlay limited to PA DCED.** `common_application_forms[9]` + `common_portals[7]` cite PA DCED Keystone Communities as the state-CDA example. Other state CDAs (NY ESD, CA SGC, TX OOG, FL DEO, MD DHCD, MA EOHED, MI SHDA, OH OBM, IL DCEO) operate analogous-but-distinct programs. Per master prompt §1.5 + Run 1 P2 — state-overlay candidates route to OD-G state-overlay amendment surface, not card-body expansion. Card's own `_review_handback.surface_ambiguities[5]` flags this. **Recommendation:** preserve PA as illustrative; defer multi-state expansion to OD-G.
- **CDFI underwriting standards (DSCR ≥ 1.20, 10–30% borrower equity).** Cited at `cost_recovery` criterion (line 86) + `scoring_weight_patterns[4]` (lines 152–160) from Reinvestment Fund. Card's `_review_handback.surface_ambiguities[2]` flags single-lender-source dependency. Recommend triangulation against (a) NCIF / Opportunity Finance Network member-CDFI typical underwriting standards, (b) Capital Impact Partners published underwriting framework, and (c) CDFI Fund Healthy Food Financing program guidance.
- **No `farmers market` / `farmer cooperative cold storage` / `aggregation facility` granularity in `underwriting_criteria`.** The criteria are written at the abstract level (shared_need / user_base / governance / access_policy) without sub-archetype specificity. Some shared-asset projects have asset-class-specific underwriting concerns (e.g., farmers markets have different access-policy structures from shared-use kitchens; food hubs have buyer-side as well as producer-side member rosters; tool libraries have different cost-recovery models). This is an OD-D candidate — extending `underwriting_criteria` with asset-class sub-archetypes might cross the §18.5 / §18.6 schema item-shape boundary (refusal (a) territory). **Recommendation:** keep abstract criteria at the canonical level; surface asset-class-specific concerns as a Program Rule Pack or a narrative_section_patterns extension.
- **No explicit cross-reference to Operating Capacity (CLC-03) / Market Access (CLC-05) / Public Purpose & Works (CLC-01) in the underwriting_criteria.** Card's `_review_handback.decision_queue[7]` and `[8]` document the boundary questions but the body does not enumerate them. The `single_applicant_shaped_as_shared_asset` red_flag (lines 480–483) is the closest the body comes — explicitly mentions "Operating Capacity, Market Access" by display name (correctly using display names per master prompt §1.5 anchor, not slugs). This is good — the body-level CLC-boundary defense is correct, just under-documented at the criterion layer.
- **No funder-cadence frequency surfacing.** Card has no field signaling typical cycle frequency per funder pathway (annual / biennial / continuous / unpredictable). Some CLC siblings carry this in `common_funders_observed[*].frequency_observed` (closed vocabulary FREQUENT/OCCASIONAL/RARE/UNKNOWN per OQ-6). Adding `common_funders_observed` (above) would surface this implicitly.
- **No language around `community land trust (CLT)` as a discrete asset-control modality.** The `asset_control` criterion (line 81) names "community land trust" as one of the legal-structure categories but does not enumerate the CLT-specific underwriting concerns (long-term ground lease vs fee simple, CLT-board-governance vs operator-board-governance separation, resale-restriction covenant enforcement, dual-ownership stewardship). For a CLT-held shared-asset project, these are load-bearing reviewer concerns. Worth a sub-bullet under `asset_control` or a CLT-specific evidence_weight.
- **`equipment_quote` evidence_weight refers to 2 CFR 200 procurement.** The cite is to 2 CFR Part 200 (lines 192–193) — accurate but generic. Federal procurement-threshold updates (Micro-Purchase Threshold raised to $10,000 / Simplified Acquisition Threshold raised to $250,000 under 2024 OMB Uniform Guidance update) belong in the citation note for currency.
- **No reference to USDA RBDG (Rural Business Development Grant) or USDA REAP (Rural Energy for America Program).** Both are USDA RD programs that fund infrastructure that often takes shared-asset form (RBDG funds shared business-incubator + co-working facilities; REAP funds shared energy infrastructure for cooperatives + nonprofits). Worth surfacing as supplementary funder pathways. **Recommendation:** add to `common_funders_observed` if populated; add to `common_application_forms` for the application packages.
- **No reference to NCIF / National Community Investment Fund Healthy Food Financing or to USDA Healthy Food Financing Initiative (HFFI)-specific guidance.** Card cites CDFI Fund HFFI (line 73) but does not cite USDA HFFI (a separate program) or NCIF's HFFI partnership specifically. These are the operationally-relevant federal HFFI flows for shared-food-infrastructure projects.
- **No reference to Kellogg Foundation, Robert Wood Johnson Foundation (RWJF), W.K. Kellogg-anchored Healthy Eating Active Living network, or USDA Farmers Market and Local Food Promotion Program (FMLFPP) — which folded into LAMP.** The historical name FMLFPP no longer applies post-2018 Farm Bill; the modern LAMP umbrella (LFPP / FMPP / RFSP / TOPP) is correctly cited. Cross-reference for searchable continuity.
- **Reviewer-priorities depth varies.** `reviewer_profile_typical.reviewer_priorities` (lines 376–384) covers nine reviewer priorities including a strong dialect cue (line 384) distinguishing foundation / public-agency / cooperative-development / CDFI / facilities-engineering / USDA RD CF state-office reviewer voice. This is unusually rich — strongest reviewer-dialect prose in the CLC body. But the `reviewer_types` list (lines 366–374) does not include `state_grants_administrator` (state-CDA reviewer) or `community_foundation_program_officer_regional` (sub-national foundation reviewer specifically) or `tribal_grants_specialist` (USDA RD CF Tribal reviewers). Recommend adding 2–3 reviewer types for completeness.
- **No `metrics_table_template` field or commitment-rollup pattern explicit at the card body level.** `commitment_tracking_pattern.typical_commitments_extracted` (lines 620–640) lists eleven commitment types with measurement_method but doesn't include the cross-reporting-period rollup logic (which Report Generator needs at v0.2 for funder reports spanning multiple grant periods). Schema does not require it; Report Generator at v0.2 may handle this layer separately.

### §2.3 Lifecycle / signature / schema concerns

- **`draft_status: signed`.** No normalization needed. The master prompt §5 "universal `draft_status: draft` gap" claim is stale for Shared Assets (and per Run 1 priors, for all 14 cards on disk). Recommend the master prompt §5 footer be amended to read "no longer applicable post-Wave 2 LOCK ceremony 2026-05-16."
- **Header-comment lifecycle assertions consistent with on-disk state.** Lines 1–5 + 711–719 cleanly document the Cycle-2 FIX-IN-PLACE + LOCK ceremony timeline. No comment drift.
- **`ed25519_signature` LIVE** (line 826) — verify against Wave 2 row 261 supersession path post any future re-sign. Per master prompt §8 finding (4), embedded sigs may be stale on OD-E-restructured cards (CLC-05/06/07) — but Shared Assets is single-track, was not OD-E-restructured, so its embedded sig should match the lock_history row 261 canonical-JSON-of-card-with-sig-nulled SHA3-512 + Ed25519 signature.
- **`canonical-JSON SHA3-512` hash recorded at line 823** as `9ed64de7…9d42a`. Verifiable in next loader graduation cycle against publisher pubkey at `vault_shared/cards/publisher_pubkey.signed.yaml`.
- **Schema completeness `15/15`** per `_review_handback.schema_completeness.required_fields_populated` (line 836). All schema-required fields populated; optional fields populated to substantive depth except `common_funders_observed` (omitted) and `provenance_requirements` (omitted).
- **No `_review_handback` block uses non-schema-known fields except `schema_completeness` keys** — the structure aligns with `_review_handback` exempt-subtree treatment per master prompt §1 path-level allowlist.
- **No `_partition_provenance` field** (correct — Shared Assets is single-track per master prompt §2 track_shape declaration; `_partition_provenance` is only required for multi-track CLCs CLC-05/06/07).
- **Header-comment statement `# SIGNED — runtime-loadable; lifecycle truth enforced by loader preflight.` (line 5)** matches the `runtime_loadable: true` on line 705. Cross-consistent.

### §2.4 Coupling-discipline self-audit (LIVE OD-C value-position regex set)

The four LIVE regex patterns per master prompt rule 3:
- `TILTH-CIC-\d{2}` — canonical CIC slug literal
- `TILTH-CLC-\d{2}` — canonical CLC slug literal
- `[Cc]apital [Ll]ogic` — capital-logic phrase
- `[Cc]ustomer [Ii]dentity` — customer-identity phrase

Path-level allowlist: any top-level key beginning with `_` (e.g., `_research_metadata`, `_review_handback`), plus self-identifying paths `card_id` / `tilth_cic_id` / `tilth_clc_id`.

| Line | Path | Match | Exempt? |
|---|---|---|---|
| 1 | (YAML header comment line `# Card — TILTH-CLC-08 Shared Assets`) | `TILTH-CLC-08` | YES — comments not in canonical bytes |
| 7 | (YAML header comment, architecture cross-reference) | `TILTH-CLC-08` regex hit? No — line 7 is `# Coupling discipline (architecture v7.0.11 §6.1 + §4 v2.x F-CARDS-COUPLING-VIOLATION-EXTENSION):` — no slug literal | N/A |
| 40 | `card_id` | `TILTH-CLC-08` | YES — `card_id` is self-identifying-path exempt |
| 44 | `tilth_clc_id` | `TILTH-CLC-08` | YES — self-identifying-path exempt |
| 53, 68, 78, 178, 183, 294, 299, 309, 313, 319, 440, 483, 645 | `*.source_citation` fields with value `"blueprint:section_18_card_system.md#§18.10-CLC-08"` | `CLC-08` substring? Yes, but the LIVE regex is `TILTH-CLC-\d{2}` — `CLC-08` without the `TILTH-` prefix does NOT match | N/A (not a regex hit) |
| 709 | `lifecycle.lock_history_row: 261` | No regex match | N/A |
| 730 | `_research_metadata.priors_consulted[0].extract_note` references `TILTH-CLC-00` | YES — `_research_metadata` exempt subtree |
| 732 | `_research_metadata.priors_consulted[1].extract_note` references `TILTH-CLC-08` | YES — exempt subtree |
| 742 | `_research_metadata.priors_consulted[6].extract_note` references `TILTH-CLC-08` | YES — exempt subtree |

**Verdict — LIVE regex set: 0 non-exempt findings.** Card passes the value-position regex layer at all non-exempt paths. The single token of concern would be a body-level reference to another CLC by slug (`TILTH-CLC-03`) instead of display name ("Operating Capacity") — the body correctly uses display names throughout (e.g., line 482 in `single_applicant_shaped_as_shared_asset.red_team_probe`: "a capacity-expansion grant for the lead applicant under a different CLC (Operating Capacity, Market Access)").

### §2.5 Legacy-phrase defense-in-depth scan

Grep for `[Cc]ustomer [Ii]nformation`: 0 hits. Card body uses no legacy "Customer Information" phrase.

Grep for `[Cc]apital [Ll]ogic`: hits on line 7 header comment (architecture cross-reference) — comments not in canonical bytes. Line 482 (`red_team_probe`) does not contain "Capital Logic" — the actual text says "a different CLC (Operating Capacity, Market Access)" — uses the CLC acronym (which is not the regex target `[Cc]apital [Ll]ogic`). No regex hits in canonical bytes.

**Verdict — legacy-phrase defense-in-depth: 0 findings in canonical bytes.**

### §2.6 Forbidden-field-registry scan (CLC-side)

The six CLC-side forbidden top-level field names per master prompt rule 2:
- `eligible_cic_subset`
- `cic_allowlist`
- `cic_denylist`
- `preferred_cics`
- `cic_win_rate`
- `cic_ranking_preferences`

Grep against the card body for all six: 0 hits at top level or nested-in-item. Schema's item-level `not.anyOf` defense-in-depth at `common_funders_observed[*]` and `provenance_requirements[*]` (both currently omitted from the body) is moot since the fields aren't populated.

**Verdict — FORBIDDEN_FIELD_REGISTRY scan: 0 findings.** Card passes.

---

## §3. Research Findings

### §3.1 Source verification table — official + primary (current card)

| URL | Type | Access date | Fields supported | Confidence |
|---|---|---|---|---|
| https://www.rd.usda.gov/programs-services/community-facilities/community-facilities-direct-loan-grant-program | official | 2026-05-15 | USDA RD CF Direct Loan + Grant program scope; `underwriting_criteria.governance` + `underwriting_criteria.cost_recovery` + `scoring_weight_patterns[0]` + `common_application_forms[4]` + `common_portals[1]` | HIGH |
| https://www.rd.usda.gov/programs-services/business-programs/rural-cooperative-development-grants | official | 2026-05-15 | USDA RCDG cooperative-development-center scope; `underwriting_criteria.user_base` + `scoring_weight_patterns[1]` + `common_application_forms[6]` | HIGH |
| https://www.ams.usda.gov/services/grants/rfsp | official | 2026-05-15 | USDA AMS LAMP RFSP shared-infrastructure scope; `underwriting_criteria.community_member_benefit` + `scoring_weight_patterns[2]` + `narrative_section_patterns[user_base]` | HIGH |
| https://www.ams.usda.gov/services/grants/lamp | official | 2026-05-15 | USDA AMS LAMP umbrella scope; `common_application_forms[5]` | HIGH |
| https://www.cdfifund.gov/programs-training/programs/healthy-food-financing | official | 2026-05-15 | CDFI Fund HFFI scope; `underwriting_criteria.utilization` | HIGH |
| https://www.nifa.usda.gov/grants/funding-opportunities/community-food-projects-competitive-grant-program | official | 2026-05-15 | USDA NIFA CFP scope; `common_application_forms[7]` | HIGH |
| https://www.reinvestment.com/policy-solutions/sustainable-food-systems/ | practitioner | 2026-05-15 | Reinvestment Fund CDFI shared-food-infrastructure financing; `scoring_weight_patterns[4]` + `common_application_forms[8]` + `common_portals[6]` | HIGH (single-lender source — Phase 4 triangulation candidate) |
| https://www.communityfoodservices.com/uploads/4/0/2/9/40292553/replacement_reserve_planning_for_shared_use_kitchens.pdf | practitioner | 2026-05-15 | Replacement-reserve 5–15% convention; `underwriting_criteria.replacement_reserve` + `evidence_weights.maintenance_budget` + `evidence_weights.replacement_reserve_documentation` | HIGH (single-source — Phase 4 triangulation candidate) |
| https://kresge.org/our-work/community-development/ | practitioner | 2026-05-15 | Foundation rubric anatomy; `scoring_weight_patterns[3]` | HIGH |
| https://www.ecfr.gov/current/title-7/subtitle-B/chapter-XLII/subchapter-B/part-3570 | official | 2026-05-15 | 7 CFR Part 3570 USDA RD CF statutory anchor; `underwriting_criteria.asset_control` + `evidence_weights.site_control` + `common_red_flags.unresolved_site_control` + `compliance_obligations[1]` | HIGH |
| https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200 | official | 2026-05-15 | 2 CFR Part 200 Uniform Guidance; `evidence_weights.equipment_quote` + `compliance_obligations[0]` | HIGH |
| https://www.fda.gov/food/food-safety-modernization-act-fsma | official | 2026-05-15 | FSMA framework; `compliance_obligations[7]` | HIGH |
| https://www.ada.gov/ | official | 2026-05-15 | ADA framework; `compliance_obligations[6]` | HIGH |
| https://www.dol.gov/agencies/whd/government-contracts/construction | official | 2026-05-15 | Davis-Bacon framework; `compliance_obligations[10]` | HIGH |
| https://dced.pa.gov/programs/keystone-communities-program-kcp/ | official | 2026-05-15 | PA DCED state-CDA exemplar; `common_application_forms[9]` + `common_portals[8]` + `budget_structure_conventions` | HIGH |
| https://www.athensfoundation.org/5-red-flags-that-could-hurt-your-grant-application | practitioner | 2026-05-15 | Foundation-side red-flag taxonomy; `reviewer_profile_typical.common_red_flags_from_reviewer_pov` | MEDIUM (practitioner source — supplementary) |
| https://www.tgci.com/blog/2020/08/understanding-capacity-building-grant-proposals | practitioner | 2026-05-15 | Capacity-grant proposal anatomy; `narrative_section_patterns[budget_capital_cost]` | LOW (older practitioner reference; verify with current sources) |
| https://nlctb.org/featured/how-to-respond-to-sustainability-questions-in-grant-proposals/ | practitioner | 2026-05-15 | Sustainability-narrative scaffolding; `narrative_section_patterns[sustainability]` | LOW (practitioner — supplementary) |
| https://www.plinth.org.uk/en-US/complete-guide/grant-management-systems-compared | secondary | 2026-05-15 | Foundation portal vendor comparison; `common_application_forms[3]` + `common_portals[3..5]` | LOW (secondary commercial source — replaceable with vendor-direct URLs) |
| https://www.ecfr.gov/current/title-7/subtitle-B/chapter-IX/part-1463 | official | 2026-05-15 | 7 CFR Part 1463 USDA AMS LAMP regulation; `compliance_obligations[2]` | HIGH |
| https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200/subpart-F | official | 2026-05-15 | 2 CFR Part 200 Subpart F Single Audit; `compliance_obligations[3]` | HIGH |
| https://www.ecfr.gov/current/title-40/chapter-V/subchapter-A/part-1500 | official | 2026-05-15 | 40 CFR Part 1500 NEPA; `compliance_obligations[11]` | HIGH |

### §3.2 New / refreshed sources to verify and add

| URL | Type | Why add | Card fields it would support | Confidence |
|---|---|---|---|---|
| https://www.rd.usda.gov/programs-services/business-programs/rural-business-development-grants | official | USDA RBDG funds shared business-incubator + co-working facilities; absent from card body | New `common_funders_observed` row + `common_application_forms` row | HIGH |
| https://www.rd.usda.gov/programs-services/energy-programs/rural-energy-america-program-renewable-energy-systems-energy-efficiency | official | USDA REAP funds shared energy infrastructure for cooperatives + nonprofits | New `common_funders_observed` row | HIGH |
| https://www.usda.gov/topics/farming/healthy-food-financing | official | USDA HFFI (separate from CDFI Fund HFFI); operationally-relevant federal HFFI flow for shared-food-infrastructure | New `common_funders_observed` row + cross-reference at `underwriting_criteria.utilization` | HIGH |
| https://capitalimpact.org/ | practitioner | Capital Impact Partners published underwriting framework — triangulation source for CDFI DSCR ≥ 1.20 + 10–30% borrower-equity claim | Refresh `scoring_weight_patterns[4].source_citation` (add second source); refresh `_review_handback.surface_ambiguities[2]` resolution | HIGH |
| https://ofn.org/ | practitioner | Opportunity Finance Network member-CDFI typical underwriting standards | Refresh `scoring_weight_patterns[4].source_citation` (add third source) | HIGH |
| https://www.usda.gov/oce/sustainability/socially-disadvantaged-farmers-ranchers | official | USDA Socially Disadvantaged Farmer / Rancher framing — relevant for cooperative-priority + community-facility routing in producer-cooperative shared-asset projects | New cross-reference at `underwriting_criteria.community_member_benefit` | MEDIUM |
| https://www.cdfifund.gov/programs-training/programs/CDFI | official | CDFI Fund CDFI Program (separate from HFFI) — funds shared-asset CDFI lenders | New `common_funders_observed` row | MEDIUM |
| https://www.cdfifund.gov/programs-training/programs/NEW-MARKETS | official | CDFI Fund NMTC — New Markets Tax Credit equity-financing for shared assets in low-income communities | New `common_funders_observed` row + cross-reference at `underwriting_criteria.cost_recovery` | MEDIUM |
| https://cooperativedevelopmentfoundation.org/ | practitioner | Cooperative Development Foundation typical-grantee framing | Refresh `_research_metadata.priors_consulted` | MEDIUM |
| https://www.foodhub.org/ | practitioner | NGFN Food Hub Collaboration — food-hub-specific underwriting + operations resource | Optional `_research_metadata.priors_consulted` | MEDIUM |
| https://institute.coop/ | practitioner | DAWI Democracy at Work Institute — cooperative-shared-asset typology resource | Optional `_research_metadata.priors_consulted` (cross-reference with CIC-05 Cooperative) | MEDIUM |
| https://www.cltnetwork.org/ | practitioner | Community Land Trust Network — CLT-specific shared-asset governance + asset-control modality | New cross-reference at `underwriting_criteria.asset_control` for CLT sub-bullet | HIGH |
| https://www.americanmadechallenges.org/ | official | DOE American-Made Challenges — shared-research-asset funding | LOW (out-of-scope for current shared-asset spectrum); defer | LOW |

---

## §4. Proposed Card Improvements (field-by-field)

Grouped by the eight runtime-behavior categories per master prompt rule 8.

### §4.1 Search vocabulary / classification (CLC-side: underwriting_criteria + reviewer_profile_typical + common_red_flags)

**4.1.1 NEW `common_funders_observed` block populated.** YAML path: `common_funders_observed`. **Seat affected:** Scout (discoverability) + Logician (validation). Currently OMITTED. **Schema allows** (optional field per CLC schema lines 7–23, declared at 98–175 with item-level `not.anyOf` defense-in-depth).

Proposed entries (each `funder_name + funder_type` required; `typical_award_range + frequency_observed + note` optional):

```yaml
common_funders_observed:
  - funder_name: "USDA RD Community Facilities Direct Loan / Grant"
    funder_type: "federal"
    typical_award_range: "Direct Loan: $100K - several million; Grant tier: typically smaller, per FY notice"
    frequency_observed: "FREQUENT"
    note: "Primary federal financing for nonprofit, public-body, federally-recognized Tribal essential-community-facility shared assets."
  - funder_name: "USDA RD Rural Business Development Grants (RBDG)"
    funder_type: "federal"
    typical_award_range: "$10K - $500K typical"
    frequency_observed: "OCCASIONAL"
    note: "Funds shared business-incubator + co-working facilities + cooperative-services projects."
  - funder_name: "USDA RD Rural Cooperative Development Grants (RCDG)"
    funder_type: "federal"
    typical_award_range: "Up to $200K per project per FY"
    frequency_observed: "OCCASIONAL"
    note: "Funds Cooperative Development Centers that establish + operate shared-services cooperatives."
  - funder_name: "USDA RD Rural Energy for America Program (REAP)"
    funder_type: "federal"
    typical_award_range: "$1.5K - $1M (grant tier); larger via loan-guarantee tier"
    frequency_observed: "OCCASIONAL"
    note: "Shared energy infrastructure for cooperatives + agricultural producers + small rural businesses."
  - funder_name: "USDA AMS Local Agriculture Marketing Program (LAMP) — RFSP / LFPP / FMPP / TOPP"
    funder_type: "federal"
    typical_award_range: "$100K - $1M typical per sub-program"
    frequency_observed: "FREQUENT"
    note: "Funds regional food-system partnerships including shared-infrastructure development (food hubs, aggregation, cold storage)."
  - funder_name: "USDA NIFA Community Food Projects (CFP)"
    funder_type: "federal"
    typical_award_range: "Up to $400K per project"
    frequency_observed: "OCCASIONAL"
    note: "Community-controlled food-systems infrastructure including shared-asset projects."
  - funder_name: "CDFI Fund Healthy Food Financing Initiative (HFFI)"
    funder_type: "federal"
    typical_award_range: "Per FY round, varies"
    frequency_observed: "OCCASIONAL"
    note: "Shared food infrastructure (healthy-food retail, food hubs, aggregation facilities) in underserved areas."
  - funder_name: "USDA Healthy Food Financing Initiative (HFFI)"
    funder_type: "federal"
    typical_award_range: "Per FY notice, varies"
    frequency_observed: "RARE"
    note: "Separate from CDFI Fund HFFI; USDA-administered HFFI flow."
  - funder_name: "Reinvestment Fund (national CDFI)"
    funder_type: "foundation"
    typical_award_range: "Debt instrument; per-deal varies $100K - $10M+"
    frequency_observed: "FREQUENT"
    note: "Leading CDFI for shared-use food infrastructure financing."
  - funder_name: "Capital Impact Partners (national CDFI)"
    funder_type: "foundation"
    typical_award_range: "Debt instrument; per-deal varies"
    frequency_observed: "OCCASIONAL"
    note: "National CDFI funding shared-food-infrastructure + community facilities."
  - funder_name: "Kresge Foundation Community Development Program"
    funder_type: "foundation"
    typical_award_range: "Per program initiative, varies"
    frequency_observed: "OCCASIONAL"
    note: "Foundation community-development capital grants anchoring foundation rubric anatomy."
  - funder_name: "Surdna Foundation (various programs)"
    funder_type: "foundation"
    typical_award_range: "Per program, varies"
    frequency_observed: "RARE"
    note: "Foundation community-development capital + shared-asset support."
  - funder_name: "PA DCED Keystone Communities Program"
    funder_type: "state"
    typical_award_range: "Per cycle, varies"
    frequency_observed: "OCCASIONAL"
    note: "PA-specific state-CDA exemplar. Other-state-CDAs analogous (NY ESD, CA SGC, etc.) per OD-G state-overlay surface."
```

Why this improves runtime behavior: Scout currently has to derive funder-roster from `underwriting_criteria.source_citation` URL parsing — fragile. Populating `common_funders_observed` gives Scout a structured roster for opportunity-matching; gives Report Generator funder-cadence context for cross-period rollup; gives operator at white-glove a starting list for the per-org funder-pipeline curation step. Phase 4 fold-in discipline self-check: refusal (a) — adds canonical-item-shape entries per schema — PASS. Refusal (b) — no new top-level field name (uses existing canonical field) — PASS. Refusal (c) — uses canonical `frequency_observed` enum (FREQUENT/OCCASIONAL/RARE/UNKNOWN) per OQ-6 — PASS. Refusal (d) — no slug literals — PASS.

**4.1.2 NEW reviewer_type additions** at `reviewer_profile_typical.reviewer_types`. Add: `state_grants_administrator`, `community_foundation_program_officer_regional`, `tribal_grants_specialist`. Why: completeness; some funder pathways (state CDA, regional community foundation, USDA RD CF Tribal applications) are currently un-represented in reviewer-type roster.

**4.1.3 NEW underwriting_criteria entry** `clt_specific_governance_layer` (only if operator approves expansion). Why: community-land-trust-held shared-assets have distinct underwriting concerns (CLT board governance vs operator board governance separation; long-term ground lease vs fee simple; resale-restriction covenant enforcement; dual-ownership stewardship). Alternative: add CLT sub-bullet to existing `asset_control` criterion description. **OD-D Phase 4 forward-binding check:** if `clt_specific_governance_layer` is a NEW criterion entry it may smuggle a new sub-schema shape past §18.5 / §18.6 — refusal (a) territory. **Recommend instead** the sub-bullet-in-existing-description approach (no schema-item-shape change).

### §4.2 Evidence capture and missing-evidence prompts (evidence_weights)

**4.2.1 NEW evidence_weights entry** `clt_dual_governance_documentation` (if CLT scope is operator-approved): trust instrument, recorded resale-restriction covenant, CLT-board-vs-operator-board governance MOU, long-term ground lease (50–99 years typical for CLTs holding CSA farms / community gardens). HIGH weight when applicant is CLT-held.

**4.2.2 NEW evidence_weights entry** `procurement_compliance_documentation`: three competitive bids above SAT (Simplified Acquisition Threshold = $250,000 per 2024 OMB Uniform Guidance update; Micro-Purchase Threshold = $10,000); sole-source justification where applicable; 2 CFR 200.317–326 documentation. MEDIUM weight (federal-funding-only).

**4.2.3 REFINE evidence_weights.equipment_quote rationale** to update 2 CFR 200 procurement thresholds: "three competitive bids above the Simplified Acquisition Threshold ($250,000 per 2024 OMB Uniform Guidance update; previously $250K via NDFAA; Micro-Purchase Threshold raised to $10,000). Procurement rules under 2 CFR 200.317–326."

**4.2.4 NEW evidence_weights entry** `civil_rights_compliance_documentation` for federally-funded shared assets — Title VI assurances, Section 504 / ADA accessibility design, Form RD 400-1 / 400-4 for USDA RD CF, ADA self-evaluation for renovation projects. MEDIUM weight (federal-funding-only).

### §4.3 KFR fact classes and provenance_requirements

**4.3.1 NEW `provenance_requirements` block** at top level. Currently OMITTED. Schema declares optional. Recommend populating for the five HIGH-weighted evidence kinds.

```yaml
provenance_requirements:
  user_member_commitments:
    required_citation_type: "Signed commitment letter or MOU naming user/member + projected use (hours, units, cycles) + commitment to user fees or dues; dated within 12 months of application"
    verbatim_quote_required: true
  governance_agreement:
    required_citation_type: "Bylaws / operating agreement / MOU / joint powers agreement / board resolution / authorizing ordinance — by section reference and date adopted"
    verbatim_quote_required: false
  access_policy:
    required_citation_type: "Written access policy enumerating booking + member-class + conflict-resolution + fee schedule + non-discrimination assurances + onboarding requirements — by section reference"
    verbatim_quote_required: false
  site_control:
    required_citation_type: "Deed, lease (with term ≥ useful life of capital improvements), recorded easement, or equipment title — by recording number and recording date"
    verbatim_quote_required: false
  replacement_reserve_documentation:
    required_citation_type: "Multi-year reserve schedule + annual contribution rate (5–15% of capital cost annualized industry-modal) + projected reserve balance against scheduled major-replacement events"
    verbatim_quote_required: false
```

Why this improves runtime behavior: Intake currently has to derive provenance discipline from the `evidence_weights.<kind>.rationale` prose. Encoding per-fact-class provenance requirements gives Intake's bulk-doc-ingestion step a structured target for verbatim-quote-with-page extraction. Improves Logician's KFR-residual gate. Phase 4 fold-in discipline self-check: refusal (a) — adds entries to canonical map shape per §18.6 — PASS. Refusal (b) — uses existing field — PASS. Refusal (c) — no enum extension — PASS. Refusal (d) — no slug literals — PASS.

### §4.4 Drafting register and admin-risk handling (route shared flagged terms to admin_risk_register.yaml v2.4 per OD-A)

**4.4.1 NO new card-body admin-risk entries** — the 9 CLC-08-scoped flagged terms were migrated to workspace-wide `admin_risk_register.yaml` v2.3 at Cycle-2 FIX-IN-PLACE 2026-05-16. The workspace register at lines 1521 (commons), 1532 (cooperative ownership), 1544 (collective ownership), 1555 (pooled resources), 1567 (right to access), 568 (sustainability), 149 (equity), 1329 (community wealth-building) covers all the CLC-08-scoped vocabulary. `shared infrastructure` (LOW federal GREEN per migration manifest) deserves verification as present at the v2.4 register.

**4.4.2 OPERATOR REVIEW QUEUED:** verify all 9 CLC-08-scoped flagged terms are present at workspace `admin_risk_register.yaml` v2.4 with `per_clc_register` map including `shared_assets` cell. Per OD-A v2.4 schema (per master prompt §7), each entry should carry `per_clc_register: tuple[tuple[str, str], ...]` with `shared_assets` keyed value from `{AVOID, OK, EXPECTED, PREFERRED}`. Current grep shows the terms exist at the workspace register; the per-CLC-register-cell verification for `shared_assets` specifically requires a separate audit pass.

**4.4.3 NEW workspace-register candidate term `food hub`** (not in current admin_risk_register grep results) — funder-neutral operational vocabulary; LOW severity (federal GREEN); could route as workspace-register-vocabulary-only term so Scribe knows it's safe. Worth surfacing for operator review.

**4.4.4 NEW workspace-register candidate term `commissary kitchen`** — same posture as `food hub`; LOW severity (federal GREEN); funder-neutral operational vocabulary that Scribe should know it can use freely in shared-asset narratives.

### §4.5 Reviewer / rubric logic

**4.5.1 REFINE `reviewer_profile_typical.reviewer_priorities` line 384 dialect cue.** Current text consolidates 6 reviewer-type dialect cues in one paragraph; recommend keeping as-is (operator-defensive density) but consider splitting into per-reviewer-type sub-objects for Scribe's per-reviewer-type-dialect lookup at v0.2 first wave. Schema flexibility (`additionalProperties: true`) allows this at v0.2; v0.1 holds the consolidated form.

**4.5.2 NEW reviewer_priority entry** at `reviewer_profile_typical.reviewer_priorities`: `"Is the cost-recovery model credible against the operating-expense projection? (CDFI underwriters: DSCR ≥ 1.20 baseline; foundation reviewers: subsidy plan disclosed; public-agency reviewers: enterprise-fund or general-fund support documented.)"` — captures the cross-funder cost-recovery scrutiny.

**4.5.3 NEW common_red_flag_from_reviewer_pov entry** at `reviewer_profile_typical.common_red_flags_from_reviewer_pov`: `"Cost-recovery model unrealistic — projected user-fee revenue assumes 100% utilization at maximum-rate tier"`. Currently the reviewer-perspective red-flag list (lines 386–394) covers nine flags; cost-recovery realism is implicit in the main `common_red_flags` body but absent from reviewer-perspective enumeration.

### §4.6 Red-team probes (common_red_flags.red_team_probe)

**4.6.1 REFINE `single_applicant_shaped_as_shared_asset.red_team_probe` (lines 481–482).** Currently strong — explicitly routes to Operating Capacity / Market Access by display name. Consider adding Public Purpose & Works (CLC-01) cross-reference for public-agency-owned single-facility asks that might fit under CDBG or USDA RD CF as a non-shared community facility (boundary clarification per `_review_handback.decision_queue[7]`).

**4.6.2 NEW common_red_flag entry** `procurement_compliance_gap` for federally-funded projects: severity MEDIUM, red_team_probe: "For the equipment / construction line items above $250,000, have three competitive bids been documented? If sole-source, is the sole-source justification on file? Are procurement records preserved per 2 CFR 200.334 for three years post-final-report?"

**4.6.3 NEW common_red_flag entry** `civil_rights_compliance_gap` for federally-funded projects: severity MEDIUM, red_team_probe: "For USDA RD CF / CDBG / federal grant: has Form RD 400-1 / 400-4 been filed? Has the access policy been screened for Title VI Limited English Proficiency (LEP) compliance? For renovation, has an ADA self-evaluation been completed?"

**4.6.4 NEW common_red_flag entry** `nepa_environmental_review_unresolved` for construction projects: severity HIGH, red_team_probe: "What NEPA classification applies — Categorical Exclusion, Environmental Assessment, or Environmental Impact Statement? Who is the federal action lead? Is the NEPA determination memo on file before construction? Is the Section 106 historic-preservation review complete?"

### §4.7 Reporting / commitment extraction (commitment_tracking_pattern)

**4.7.1 REFINE `commitment_tracking_pattern.typical_commitments_extracted[access_equity_distribution].measurement_method`** to specify the canonical aggregation interval: "per quarter and per year; report smallest-user-share + top-decile-concentration as headline KPIs; Lorenz curve as supplementary visualization." Current prose is rich but operationally interval-vague.

**4.7.2 NEW commitment entry** `civil_rights_compliance_reporting`: measurement_method: "for federally-funded shared assets — Title VI assurances renewed annually; Section 504 / ADA accessibility complaints log + resolution; LEP plan updates; Form RD 400-1 / 400-4 renewal cycle per program guidance."

**4.7.3 NEW commitment entry** `procurement_audit_compliance`: measurement_method: "for federally-funded shared assets — procurement records preserved per 2 CFR 200.334 retention period (3 years post-final-report); annual Single Audit submission if federal expenditures ≥ $1M (2024 OMB Uniform Guidance update); SF-425 + SF-PPR per program schedule."

### §4.8 Memory namespace usefulness (cards:clc:shared_assets:*) + regression tests

**4.8.1 MEMORY namespace `cards:clc:shared_assets:funders_observed`** — populate post-§4.1.1 with the 13 funder roster.

**4.8.2 MEMORY namespace `cards:clc:shared_assets:asset_class_mapping`** — at v0.2 first wave, surface asset-class-to-funder-pathway hints (food hub → LAMP RFSP + Reinvestment Fund; shared-use kitchen → CDFI HFFI + USDA NIFA CFP; community facility → USDA RD CF; CLT-held farm → USDA NRCS easement + foundation community-development).

**4.8.3 MEMORY namespace `cards:clc:shared_assets:replacement_reserve_thresholds`** — v0.2 horizon; cumulative reserve balance + projected balance against scheduled major-replacement events; flagged when reserve-balance projection drops below scheduled-replacement cost by ≥20%.

---

## §5. Operator Decision Queue

1. **POPULATE `common_funders_observed` (P1 — high-leverage discoverability).** Add the 13-entry funder roster per §4.1.1. Operator decision: include all 13, or subset.

2. **POPULATE `provenance_requirements` (P1 — Intake-side discipline).** Add the five-entry HIGH-weighted-evidence provenance map per §4.3.1. Operator decision: full coverage of HIGH-weighted evidence kinds, OR full coverage of all 13 evidence kinds, OR omit entirely.

3. **CLT-specific governance layer scope (P2 — schema-edge).** Sub-bullet under `underwriting_criteria.asset_control` (safe path) vs new criterion entry (refusal (a) risk). Operator decision.

4. **Workspace `admin_risk_register.yaml` v2.4 verification (P1 — cross-card hygiene).** Verify all 9 CLC-08-scoped flagged terms are present at v2.4 with `per_clc_register.shared_assets` cell populated per OD-A v2.4 schema. Verify `shared infrastructure` term is present (Wave 2 migration manifest claimed NEW addition). Confirm `food hub` and `commissary kitchen` are NOT register candidates (LOW severity / federal GREEN — safe operational vocabulary).

5. **Replacement-reserve triangulation (P1 — source diversity).** Phase 4 deepening per `_review_handback.surface_ambiguities[0]`: add USDA RD CF reserve-adequacy guidance + GAAP nonprofit reserve standards as triangulation sources for the 5–15% annualized convention. Update `evidence_weights.replacement_reserve_documentation.source_citation` to multi-source.

6. **CDFI underwriting standards triangulation (P2 — source diversity).** Phase 4 deepening per `_review_handback.surface_ambiguities[2]`: add Capital Impact Partners + Opportunity Finance Network sources for DSCR ≥ 1.20 + 10–30% borrower-equity claim. Update `scoring_weight_patterns[4].source_citation` to multi-source.

7. **State-overlay routing (P2 — defer to OD-G).** PA DCED Keystone Communities is the current state-CDA exemplar. Other-state-CDAs (NY ESD, CA SGC, TX OOG, FL DEO, MD DHCD, MA EOHED, MI SHDA, OH OBM, IL DCEO) follow analogous-but-distinct patterns. Operator decision: defer multi-state expansion to OD-G state-overlay amendment surface (recommended).

8. **Boundary documentation explicit in body (P2 — usability).** `_review_handback.decision_queue[7]` and `[8]` document CLC-08 boundary questions (vs CLC-01 Public Purpose & Works, vs CLC-03 Operating Capacity). Recommend adding a one-line `_research_metadata.boundary_clarifications` sub-field (under `_research_metadata` exempt subtree) so the boundary reasoning is preserved in re-loaded card metadata for Scout's CLC-disambiguation logic.

9. **NEPA environmental review + civil rights + procurement compliance red flags (P2 — gap closure).** Add three new entries to `common_red_flags` per §4.6.2 / §4.6.3 / §4.6.4. Operator decision: add at v0.1 or defer to v0.2 supersession-re-sign cycle.

10. **2024 OMB Uniform Guidance update propagation (P1 — currency).** Update `evidence_weights.equipment_quote.rationale` and any other 2 CFR 200 procurement-threshold references to the 2024 update ($10K Micro-Purchase + $250K Simplified Acquisition + $1M Single Audit threshold). The card already has `$1M Single Audit (rising to $1M under 2024 update)` at line 527 — verify all 2 CFR 200 currency points.

11. **Phase 4 fold-in fallback usage** — per master prompt §2 prompt body rule 6 last paragraph, structural-gap findings (here: §4.1.3 CLT-specific governance criterion that touches refusal (a) territory, §4.4.2 workspace-register-per-CLC-cell verification) route to comment-block-only fallback at the relevant section + `_review_handback.decision_queue` per the Wave 2 6-of-7 precedent. Operator decision: which proposals route to fallback vs in-data application at the next supersession-re-sign ceremony.

---

## §6. Validation Checklist

- [x] Schema fields complete against current §18.6 CLC schema: 15/15 required + 18/22 optional populated. `common_funders_observed` + `provenance_requirements` are operator-decision-queued for population.
- [x] No forbidden coupling field names at top level: 0 hits.
- [x] No forbidden coupling field names nested in `common_funders_observed[*]` or `provenance_requirements[*]` (both currently omitted; would be defended item-level `not.anyOf` once populated).
- [x] No forbidden value-position regex matches outside exempt paths: 0 non-exempt findings per §2.4.
- [x] No private organization-specific data in card body.
- [x] No unsourced program-law claims — every claim cites source URL with access_date.
- [x] No excessive quoted source text — verbatim quotes ≤2 sentences per OQ-4.
- [x] Lifecycle status consistent with architecture v7.0.11 §1.5 — `draft_status: signed` + `runtime_loadable: true` + all six lifecycle gates at pass-state.
- [N/A] Single-track CLC — `_partition_provenance` not required.
- [x] Item-level `not.anyOf` defense-in-depth on `common_funders_observed` (schema lines 140–173) and `provenance_requirements` (schema lines 195–227) verified by schema reference; fields not yet populated at the card layer.
- [x] Display names used in body prose for cross-CLC references (e.g., "Operating Capacity, Market Access" on line 482) — no slug literals in non-exempt value positions.
- [x] Phase 4 fold-in discipline self-check per master prompt rule 6 + §18.11 v1.1 — none of the proposals in §4.1.1 / §4.2 / §4.3.1 / §4.4 / §4.5 / §4.6 / §4.7 / §4.8 trip refusals (a)/(b)/(c)/(d). §4.1.3 CLT-specific-governance-criterion proposal touches refusal (a) territory — routed to comment-block-only fallback per operator decision queue item 3.

---

## §7. Regression Tests

### Test 1 — Single-applicant capacity-expansion-framed-as-shared-asset prompt

**Prompt:** "We're a 30-acre vegetable producer in central PA looking to apply for USDA RD funding to build a shared-use packing shed and cold-storage facility. The packing shed would be used by us and by three neighboring small farms in the area."

**Pre-edit behavior:**
- Scout matches `cold storage`, `shared-use facility`, `packing shed` — routes to USDA RD CF + USDA AMS LAMP RFSP + USDA RBDG.
- Scribe drafts Shared Need section assuming the four-farm framing is automatically a shared-asset use case.
- Logician's `single_party_capture_of_shared_asset` red_flag fires only if Scribe surfaces explicit utilization breakdown showing the lead farm using ≥80% capacity.
- Logician's `single_applicant_shaped_as_shared_asset` red_flag may fire but the routing to Operating Capacity (CLC-03) or Market Access (CLC-05) is implicit prose.

**Post-edit behavior (with §4.1.1 + §4.6.1 + populated `common_funders_observed`):**
- Scout matches `shared-use facility` AND surfaces the four `common_funders_observed` USDA federal entries with frequency_observed hints — USDA RD CF (FREQUENT for nonprofit/public/Tribal; OCCASIONAL for cooperative entity that the four-farm group would need to form), USDA RBDG (OCCASIONAL), USDA AMS LAMP RFSP (FREQUENT for partnership). Scout surfaces the funder-cadence + the four-farm-cooperative-formation-prerequisite for USDA RD CF.
- Scribe drafts Shared Need section with mandatory multi-user-demonstration evidence per §4.1.1 funder-roster scaffolding.
- Logician's `single_applicant_shaped_as_shared_asset` red_flag fires AND surfaces the explicit CLC-routing recommendation per refined §4.6.1: "Operating Capacity (CLC-03) for the lead farm's capacity expansion; Market Access (CLC-05) if the lead farm's primary intent is buyer-channel development; Shared Assets (CLC-08) requires multi-user demand-evidence beyond verbal neighboring-farm commitment."
- Logician's `vague_access_rules` red_flag fires if access policy not enumerated per §18.6 access_policy six-component requirement.

**Seat affected:** Scout + Scribe + Logician. **Pass criterion:** CLC-routing recommendation surfaces in Logician output; Scout funder-roster includes the four-farm-cooperative-formation prerequisite for USDA RD CF; access-policy six-component enumeration is required at Intake.

### Test 2 — Foundation community-development capital-grant prompt

**Prompt:** "Our 501(c)(3) operates a community food hub serving 28 producer members and 14 institutional buyers. We're applying to Kresge Foundation Community Development for a $500K capital grant to expand cold storage."

**Pre-edit behavior:**
- Scout matches `food hub`, `community food hub`, `cold storage`, `community development` — routes to Kresge / Surdna / foundation CD pathways.
- Scribe drafts narrative without explicit governance-engagement-equity foundation-rubric framing.
- Logician's reviewer-priority cues (line 384 dialect cue) fire but the foundation-PO-specific weighting isn't surfaced upfront.

**Post-edit behavior (with §4.1.1 funder-roster + §4.3.1 provenance + §4.5.2 cost-recovery reviewer-priority):**
- Scout matches Kresge entry from `common_funders_observed` and surfaces typical_award_range + frequency_observed + note about foundation rubric anatomy.
- Scribe drafts narrative with foundation-rubric scaffolding (community engagement + governance + equity-of-access leading; financial sustainability + learning-and-evaluation supplementary). References the `scoring_weight_patterns[3]` Foundation community-development pattern.
- Logician's new reviewer-priority entry fires: "Is the cost-recovery model credible? Foundation reviewers: subsidy plan disclosed."
- Logician's `provenance_requirements.governance_agreement` requires bylaws / board resolution / MOU + recording metadata.

**Seat affected:** Scout + Scribe + Logician. **Pass criterion:** Foundation-rubric scaffolding leads with community-engagement + governance; cost-recovery subsidy plan is disclosed; bylaws + board-approval citation includes recording metadata.

### Test 3 — Vague access-rules adversarial probe prompt

**Prompt:** "Our cooperative is applying for USDA RCDG to develop a shared-services cooperative for 18 member farms. The shared-services center will offer GAP-certification consulting, accounting services, and equipment-sharing."

**Pre-edit behavior:**
- Scout matches `cooperative`, `shared-services cooperative`, `shared services center`, `GAP certification`, `accounting services`, `equipment sharing` — routes to USDA RCDG.
- Scribe drafts Operations Plan but does not enumerate access-policy six-component structure per §18.6 access_policy criterion.
- Logician's `vague_access_rules` red_flag fires at HIGH severity. Scribe revises.

**Post-edit behavior (with §4.3.1 `provenance_requirements.access_policy` populated):**
- Scribe drafts Operations Plan + Access Policy section using the six-component template enforced by `provenance_requirements.access_policy.required_citation_type` — Intake forces structured access-policy text containing each of the six components before claim acceptance.
- Logician's `vague_access_rules` red_flag does NOT fire on first pass.
- Equity safeguards section (one-member-one-vote on access disputes for cooperative-operated assets, per the `access_policy` criterion at line 66) is explicitly drafted because the criterion enumerates it.

**Seat affected:** Intake + Scribe + Logician. **Pass criterion:** access policy contains all six components at Intake submission; `vague_access_rules` red_flag does NOT fire; cooperative-operated equity safeguard explicitly drafted.

### Test 4 — Replacement-reserve adequacy red-team probe prompt

**Prompt:** "We're a 501(c)(3) operating a shared-use commercial kitchen serving 22 food-product entrepreneurs. We're applying to a regional CDFI for a $750K capital loan to expand from one production room to three rooms."

**Pre-edit behavior:**
- Scout matches `shared-use kitchen`, `commercial kitchen`, `food incubator` — routes to CDFI shared-asset financing + USDA NIFA CFP + USDA AMS LAMP LFPP.
- Scribe drafts Capital Cost section but does not surface replacement-reserve schedule unless prompted.
- Logician's `ignored_replacement_cost` red_flag fires at HIGH severity. Scribe revises with reserve schedule.

**Post-edit behavior (with §4.3.1 `provenance_requirements.replacement_reserve_documentation` + multi-source reserve-percentage triangulation per §5.5):**
- Intake forces multi-year reserve schedule structure at submission per the `required_citation_type` string.
- Scribe drafts Maintenance + Replacement Reserve section with explicit annual-contribution-rate triangulated against USDA RD CF reserve-adequacy + GAAP nonprofit reserve standards + Community Food Services PDF practitioner guidance.
- Logician's `ignored_replacement_cost` red_flag does NOT fire on first pass.
- CDFI DSCR ≥ 1.20 cross-check fires per `scoring_weight_patterns[4]`.

**Seat affected:** Intake + Scribe + Logician. **Pass criterion:** reserve schedule structure at Intake; multi-source-anchored annual-contribution-rate; DSCR ≥ 1.20 cross-checked.

### Test 5 — Cross-CLC boundary disambiguation prompt

**Prompt:** "Our school district wants to apply for federal capital funding to renovate the central food-services kitchen so it can serve as a shared-use kitchen for community groups outside school hours."

**Pre-edit behavior:**
- Scout matches `school district`, `kitchen`, `shared-use kitchen`, `capital funding` — routes ambiguously between CLC-01 Public Purpose & Works (school district as public agency), CLC-02 Educator (school district), and CLC-08 Shared Assets (shared-use kitchen).
- Logician opportunity-driven matching surfaces multiple candidate CLCs.

**Post-edit behavior (with §4.1.1 funder-roster + §5.8 boundary clarifications explicit):**
- Scout surfaces CLC-08-specific funder pathway: USDA RD CF (school district as public-body recipient) + USDA NIFA CFP (community-controlled food-systems infrastructure) + foundation community-development capital.
- Scribe drafts narrative aware that the shared-use dimension qualifies for CLC-08 underwriting logic AS WELL AS the school-district-specific CLC-02 program-design logic. The CLC routing is opportunity-driven runtime — both card bodies fire per the matched opportunity.
- Logician validates governance documentation (authorizing resolution from school board) + governance separation (school-district food-service operations vs community-group access governance) + access policy (school-hours vs community-hours scheduling).
- Boundary documentation per §5.8 surfaces in `_research_metadata.boundary_clarifications` if added at v0.2.

**Seat affected:** Scout + Scribe + Logician. **Pass criterion:** Both CLC-08 + CLC-02 underwriting logics surface as candidates per opportunity-driven matching; school-board authorizing resolution + governance-separation MOU required at Intake; CLC-08 access-policy six-component enumeration required.

---

## §8. Patch Plan

Edits proposed in this handback grouped by file path. **No edits applied from this dispatch.** Operator dispatches each ceremony separately per the OD-C / OD-E precedent (per-card lock_history supersession row + post-restructure SHA3-512 + publisher Ed25519 signature against `vault_shared/cards/publisher_pubkey.signed.yaml`).

### File: `pipeline/cards/CLC/shared_assets.yaml`

**Ceremony shape:** supersession-re-sign per OD-E precedent (row 276 / 277 / 278 model). Parent_lock_row = 261 (Wave 2 LOCK). Ceremony_parent_row = `<NEXT-AVAILABLE-COMPOUND-PARENT>` if bundled with sibling CLC-side patches, OR `<NEXT-AVAILABLE>` standalone.

**Edit set:**

1. `common_funders_observed: <NEW POPULATION>` — 13-entry funder roster per §4.1.1.
2. `provenance_requirements: <NEW POPULATION>` — 5-entry HIGH-weighted-evidence provenance map per §4.3.1.
3. `reviewer_profile_typical.reviewer_types[NEW]` — add 3 entries per §4.1.2.
4. `reviewer_profile_typical.reviewer_priorities[NEW]` — add cost-recovery cross-funder reviewer-priority per §4.5.2.
5. `reviewer_profile_typical.common_red_flags_from_reviewer_pov[NEW]` — add cost-recovery realism entry per §4.5.3.
6. `evidence_weights.equipment_quote.rationale[REFINE]` — update 2 CFR 200 procurement thresholds per §4.2.3.
7. `evidence_weights[NEW]` — add `procurement_compliance_documentation` + `civil_rights_compliance_documentation` per §4.2.2 + §4.2.4 (federal-funding-only entries).
8. `underwriting_criteria.asset_control.description[REFINE]` — add CLT-specific sub-bullet per §4.1.3 (safe sub-bullet path; refuses (a) territory if framed as new criterion).
9. `common_red_flags[NEW]` — add `procurement_compliance_gap` + `civil_rights_compliance_gap` + `nepa_environmental_review_unresolved` per §4.6.2 / §4.6.3 / §4.6.4.
10. `commitment_tracking_pattern.typical_commitments_extracted[access_equity_distribution].measurement_method[REFINE]` — add quarterly/annual aggregation interval per §4.7.1.
11. `commitment_tracking_pattern.typical_commitments_extracted[NEW]` — add `civil_rights_compliance_reporting` + `procurement_audit_compliance` per §4.7.2 / §4.7.3.
12. `evidence_weights.replacement_reserve_documentation.source_citation[REFINE]` — multi-source triangulation per §5.5.
13. `scoring_weight_patterns[4].source_citation[REFINE]` — multi-source CDFI triangulation per §5.6.
14. `_research_metadata.boundary_clarifications[NEW]` — operator-decision-queued sub-field documenting CLC-08 ↔ CLC-01 ↔ CLC-03 ↔ CLC-05 boundary reasoning per §5.8 (safe under `_research_metadata` exempt subtree).

**OD-D Phase 4 forward-binding contract note (per master prompt rule 6 + §18.11 v1.1):**

- No proposal touches refusal (c) (compound enum values) — all `frequency_observed` entries use canonical FREQUENT/OCCASIONAL/RARE/UNKNOWN; all severity entries use canonical HIGH/MEDIUM/LOW.
- No proposal touches refusal (d) (literal canonical CIC/CLC slug in non-exempt value position) — display names used throughout body prose; slug literals confined to `card_id` + `tilth_clc_id` + `_research_metadata` exempt subtree per §2.4 scan.
- No proposal touches refusal (a) (structured-sub-field expansion on canonical entries) — `common_funders_observed` + `provenance_requirements` populated at canonical schema item-shape. Single proposal touching (a) territory — the CLT-specific governance criterion at §4.1.3 — is routed to the safer sub-bullet-in-existing-description path per Phase 4 fold-in fallback discipline.
- No proposal touches refusal (b) (dedicated field-name fork) — all additions use existing canonical fields.

**Per Wave 2 Thesis trail comment-block-only Phase 4 fold-in precedent (master prompt §2 rule 6 last paragraph + §18.11 v1.1):** the CLT-specific-governance-criterion expansion proposal (§4.1.3) and the workspace-register-per-CLC-cell verification proposal (§4.4.2) — both touching structural-gap territory — route to the comment-block-only fallback. The fallback writes the proposal as a YAML comment inside the relevant section AND routes the structural gap to the card's `_review_handback` operator-decision queue. Defer in-data application to a future §18 v1.x amendment.

### File: `pipeline/cards/_schema/card_clc.schema.json`

**No schema changes proposed.** All §4 proposals fit within the current CLC schema. The dialect_routing_table v1.2 schema delta (LOCKed-but-not-applied per Run 1 priors) is bottlenecked at the cards-ceremony; Shared Assets has no `dialect_routing_table` field at the card layer (CLC cards don't typically carry it), so the bottleneck does not bind here.

### File: `pipeline/institutional_memory/admin_risk_register.yaml`

**Ceremony shape:** workspace-register update (OD-A v2.4 → v3.0 scrub workflow per master prompt §7).

**Edit set:**

15. **VERIFY** all 9 CLC-08-scoped flagged terms are present at v2.4 with `per_clc_register.shared_assets` cell populated per OD-A v2.4 schema. Verify `shared infrastructure` term is present (Wave 2 migration manifest claimed NEW addition).
16. **NEW workspace-register candidate `food hub`** (per §4.4.3) — LOW severity / federal GREEN.
17. **NEW workspace-register candidate `commissary kitchen`** (per §4.4.4) — LOW severity / federal GREEN.

**Out of scope for this card alone**; surface as workspace-register schema-extension decisions to operator at separate v2.4 → v3.0 scrub workflow.

### File: `pipeline/cards/CLC/operating_capacity.yaml` + `pipeline/cards/CLC/public_purpose_works.yaml` + `pipeline/cards/CLC/market_access.yaml` (cross-card; out of scope for this dispatch)

Cross-CLC boundary documentation per §5.8 + Test 5 may benefit from reciprocal `_research_metadata.boundary_clarifications` entries on the sibling CLCs. Out of scope for `shared_assets` handback. Surface to Phase 4-CLC re-pass for parallel dispatch consideration.

---

**Summary block:**

```
Card: CLC:shared_assets
Card file: pipeline/cards/CLC/shared_assets.yaml
Research hours actual: 1.6
Findings: 23 total — 0 P0, 10 P1, 13 P2
Decision queue: 11 operator approvals required
Conflicts with prior art: NONE (all admin_risk_term entries already migrated to workspace admin_risk_register v2.4 per Cycle-2 FIX-IN-PLACE 2026-05-16; cross-CLC term-set is verification-candidate, not conflict)
Coupling-discipline regression: NONE (LIVE OD-C value-position regex scan: 0 non-exempt findings; FORBIDDEN_FIELD_REGISTRY scan: 0 hits)
Phase 4 fold-in discipline self-check: PASS (1 proposal — §4.1.3 CLT-specific governance criterion — routed to safer sub-bullet path per master prompt rule 6 refusal (a) avoidance; 2 proposals — §4.1.3 fallback + §4.4.2 workspace-register-cell verification — route to comment-block-only Phase 4 fold-in fallback per Wave 2 CLC-08 precedent)
Lifecycle gap surfaced: draft_status reads "signed" on disk (per Run 1 priors — master prompt §5 universal "draft_status: draft" claim is STALE for the on-disk state of Shared Assets and all 14 LOCKed cards; no normalization required at this card)
Review readiness: READY (content improvements bundled to a single supersession-re-sign ceremony per OD-E precedent; admin-risk-register verification + 2 NEW workspace-register candidates routed to separate v2.4 → v3.0 scrub workflow; CLT-specific governance criterion + workspace-register-cell verification routed to comment-block-only fallback per Wave 2 CLC-08 precedent)
```
