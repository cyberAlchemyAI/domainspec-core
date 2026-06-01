# TILTH-CIC-05 Cooperative — Research Handback

**Filed:** 2026-05-17
**Workspace:** `/Users/goldenquill/Downloads/GoldenQuill/`
**Run:** Run 2 of operator's controlled-batch sequence (Phase 4 CIC handbacks; 5 of 6).
**Card:** `pipeline/cards/CIC/cooperative.yaml` (Wave 2 LOCKed 2026-05-16 row 253; SHA-256 `ffba9a…81ce`; signed `2026-05-16T16:00:00Z`).
**Authority chain:** master prompt §2 + plan §1.5 + Run 1 priors (binding).
**Run 1 priors folded in:** all 14 cards on disk are `draft_status: "signed"`; §18 v1.2 LOCKed-but-not-applied; operator v2.1 Law-5 split uniformly applied; coupling-extension value-position regex not LIVE at runtime; operator reframe = aggressive content OK.
**Operator-special context:** Per card header lines 23–28 the operator (Josh) is co-founder of MycoSymbiotics Cooperative. This CIC is operationally first-person for the operator and must work for any cooperative-customer (worker / producer / consumer / multi-stakeholder / shared-services / platform / ESOP). The card carries the legal_status fact-class to surface entity-form diversity.

---

## §1. Card Impact Thesis

`cooperative` is the densest movement-vocabulary CIC in the canonical roster — it sits at the intersection of governance / capitalization / patronage / democratic-control / shared-benefit / financial-controls **and** the political-vocabulary surface that triggers the most reviewer reactions across federal + foundation panels. Its job is to make Tilth **understand member-governed ownership as a governance + capitalization + patronage + democratic-control + shared-benefit + financial-controls problem — not just a values statement**, and to navigate the movement-aligned admin-risk landscape (anti-capitalist / solidarity economy / mutual aid / commons / worker control / collectivize / abolition / wealth redistribution) with operator-grade substitution discipline.

What this card should *cause Tilth to do differently*:

1. When Scout sees `cooperative`, `worker-owned cooperative`, `producer cooperative`, `consumer cooperative`, `multi-stakeholder cooperative`, `platform cooperative`, `purchasing cooperative`, `shared services cooperative`, `ESOP`, `employee ownership`, `Mutually Owned Business`, `community wealth-building`, anchor to USDA RBCS (RCDG / RBDG) statutory framing + USFWC / DAWI sector identity + IRC Subchapter T + Mainstreet Employee Ownership Act + ICA Cooperative Identity Principles.
2. When Scribe drafts a cooperative narrative, route per the four dialect lanes (conservative formal_commercial / centrist technical_precise / progressive movement_aligned / soul_fire cooperative_solidarity) per active-RFA funder dialect — NEVER collapse to a single tone.
3. When Logician audits a draft mentioning `anti-capitalist`, `solidarity economy`, `mutual aid`, `commons`, `worker control`, `collectivize`, `abolition`, `wealth redistribution`, fire admin_risk_term entries with severity HIGH (most of these); surface substitution candidates that preserve substance via shared ownership / democratic enterprise / cooperative economics / community wealth-building / member-owned business model. Operator approves per approval_required: true default — Tilth NEVER silently rewrites.
4. When the active opportunity is USDA RD (RCDG / RBDG / VAPG / SDGG / REAP under current administration framing), emphasize jobs-created-or-retained + small-business-formation + rural-employment + member-equity-raised framing per conservative formal_commercial dialect.
5. When the active opportunity is cooperative-development CDFI or national cooperative-development intermediary, use technical-precise cooperative-development vocabulary (governance / patronage / member equity) — substituting to plain commercial language misses the cooperative-form-specific underwriting cues.
6. When the applicant entity is ESOP (vs true statutory cooperative vs LLC-with-cooperative-bylaws), surface the ERISA fiduciary boundary + Mainstreet Employee Ownership Act + SBA 7(a) ESOP loan-guarantee pathway distinction.
7. When PA-specific applicant context surfaces, flag the weak-PA-cooperative-statute reality — many PA cooperatives operate as LLCs with cooperative bylaws because PA has no comprehensive cooperative statute.

The runtime-behavior delta this card produces is **movement-vocabulary discipline + entity-form diversity navigation (ESOP / true cooperative / LLC-with-cooperative-bylaws / Subchapter T pass-through) + cooperative-funder dialect routing precision + PA-specific weak-statute reality.** The card is currently strong on all four.

---

## §2. Current State Audit

### §2.1 What is strong now

- **Cooperative-form taxonomy depth.** 20+ core_terms covering all major cooperative forms (worker / producer / consumer / platform / multi-stakeholder / purchasing / shared services / rural / employee-ownership trust / ESOP) with statutory anchors per IRC Subchapter T (IRC §§1381–1388), Mainstreet Employee Ownership Act (Pub. L. 115-232), ERISA §407(d)(6) for ESOPs, USDA RCDG 7 CFR 4284 Subpart F.
- **Statutory anchor precision.** ICA Cooperative Identity Statement (Principle 1 Mutually Owned + Principle 2 Democratic Member Control); USDA RCDG "Mutually Owned Business" statutory category; IRC §1388(a) patronage-dividend definition; State cooperative statutes (CA Cal. Corp. Code §12253.5; NY BCL §1402).
- **Four-dialect routing precision.** Lines 419–464: conservative formal_commercial (USDA RD frame as small-business form + jobs engine); centrist technical_precise (cooperative-development CDFIs + national intermediaries; technical cooperative-development vocabulary); progressive movement_aligned (community-wealth-building-aligned community foundations); soul_fire cooperative_solidarity (movement-aligned cooperative-priority funders). Per-dialect prose 5–7 lines each explaining when substitution misses funder underwriting cues.
- **10 admin_risk_term entries** (lines 472–631) — anti-capitalist (HIGH), solidarity economy (HIGH), mutual aid (MEDIUM), commons (MEDIUM), worker control (HIGH), collectivize (HIGH), abolition (HIGH), wealth redistribution (HIGH), DEI / equity / inclusion (MEDIUM), stakeholder capitalism (MEDIUM). All approval_required: true. Heaviest movement-vocabulary surface in the CIC body.
- **ESOP-vs-true-cooperative boundary clarification.** Comment block at lines 36–39 explicitly states "ESOP-owned firms are *one form of* employee ownership but have distinct ERISA fiduciary obligations and a different (Mainstreet Employee Ownership Act + SBA 7(a)) financing pathway than a true cooperatively-governed worker co-op (one-member-one-vote + Subchapter T patronage). Both are in scope; card differentiates via fact-class + compliance_burdens." Strong boundary-discipline.
- **PA-specific weak-statute reality.** Comment + compliance_burdens narrative documents PA-specific reality (no comprehensive PA cooperative statute; many PA cooperatives use LLC-with-cooperative-bylaws form). Operator-relevant via FIT Farms LLC + MycoSymbiotics jurisdiction.
- **Phase D A.1 cleanup.** Five named soul_fire-axis exemplar orgs (Cooperation Jackson / USFWC / DAWI / The Industrial Commons / Highlander) were briefly relocated to `_research_metadata.priors_consulted` at Phase D and then fully removed per operator directive 2026-05-16 (full anonymization). The dialect_routing_table soul_fire row uses a generic descriptor. Strong Law-5 + operator-side discipline.
- **Phase E Option 2 Law-5 cleanup.** Top-level `common_funders_observed: []` at line 893; subagent candidates at `_research_metadata.draft_funder_candidates_pending_operator_engagement_confirmation` line 1059.
- **Lifecycle truth.** lock_history_row 253.

### §2.2 What is stale, ambiguous, over-broad, too local, too federal, or under-sourced

- **`dialect_routing_table` v1.1 shape with retired political-axis enum** (lines 419–464). Same status as siblings: cards-ceremony bottleneck. The four-dialect prose at lines 422–464 is rich operator-defensive content — preserve into post-ceremony register_description fields.
- **`anti-capitalist` and `solidarity economy` admin_risk_term entries at HIGH severity** are operator-defensible given cooperative-applicant funder-mix. But the substitution candidates ("shared ownership," "democratic enterprise," "cooperative economics," "community wealth-building") may understate scope for some applicants (e.g., a solidarity-economy framework explicitly invokes worker co-ops + community land trusts + time banks + worker centers, not just cooperatives). For soul_fire-aligned funders the original term is preferred per the reviewer_context. Operator decides per RFA. Recommend `_review_handback.surface_ambiguities` already flags this at line 1224.
- **PA-specific entries** in funder_program_keywords + draft_funder_candidates. State-overlay candidates per master prompt §1.5 + Run 1 P2.
- **No `solidarity economy intermediary`** or `cooperative development corporation (CDC)` named in funder_program_keywords as omnibus. National Center for Employee Ownership, Democracy at Work Institute, US Federation of Worker Cooperatives — these appear in admin_risk_term reviewer_context and primary_sources but not as Scout-vocabulary funder_program_keywords. (USDA RCDG funds cooperative-development centers; these intermediaries are the typical sub-recipients.)
- **No `Aspen Institute Economic Opportunities Program (EOP)` named** — Aspen EOP is the key ESOP-track research / TA / capacity-building intermediary. Project Equity is the key practitioner-side ESOP-transition intermediary. Both named in `_review_handback.surface_ambiguities` (lines 1220–1226) but absent from card body Scout vocabulary.
- **No `Subchapter T election-vs-non-election`** treatment in the patronage_model fact-class. Subchapter T is optional; many cooperatives operate without Subchapter T (paying tax at corporate or LLC pass-through level). The card captures this via patronage_model fact-class but does not prescribe — recommend explicit fact-class extension or KFR sub-field for Subchapter T election status.
- **No `cooperative housing` core_term.** Housing cooperative (limited-equity housing co-op / market-rate housing co-op / mutual housing association) is a major cooperative form not currently named — the card folds housing into consumer + multi-stakeholder per ICA convention. Per `_review_handback.surface_ambiguities` line 1220: "Some practitioners include 'housing cooperative' as a distinct type." Operator decides scope.
- **No `cooperative association` or `mutual benefit corporation`** statutory entity-form clarification — some states (NY, NJ) distinguish "mutual benefit corporation" from "cooperative corporation."
- **`metrics_table_template` not visible from initial read.** Recommend confirming metrics-template coverage of cooperative-specific metrics (member count + members-by-class + patronage-dividends-paid + member-equity-raised + jobs-by-worker-owner-vs-non-owner + cooperative-principles-compliance-score if applicable).
- **No `cooperative-development center` evidence_signal pattern.** USDA RCDG funds cooperative-development centers as sub-recipients; this is a typical pathway for cooperative-development intermediaries to access federal funds. Worth surfacing.
- **`compliance_burdens` not deeply scanned in this read** — confirm coverage of ERISA + Subchapter T + state-cooperative-statute + Mainstreet Employee Ownership Act in compliance_burdens.

### §2.3 Lifecycle / signature / schema concerns

- **`draft_status: signed`.** No normalization needed.
- **Header comment drift (P1-4).** Line 45: `# Lifecycle: draft. NO Ed25519 signature. Operator review pending before Wave 2 LOCK ceremony as separate dispatch.` Stale (per Run 1 Phase 1 §5). Recommend update.
- **`dialect_routing_table` v1.1 shape.** Cards-ceremony bottleneck.
- **`_research_metadata.draft_funder_candidates_pending_operator_engagement_confirmation` field not schema-known.** Same status.
- **Phase D A.1 cleanup discipline** — five named soul_fire orgs fully anonymized per operator directive 2026-05-16. Cross-card discipline for future research dispatches: do not reintroduce named third-party orgs in `dialect_routing_table.example_funder` without operator approval. This is the canonical anti-named-org pattern.

### §2.4 Coupling-discipline self-audit

| Line | Path | Match | Exempt? |
|---|---|---|---|
| 1 | (YAML header comment) | `TILTH-CIC-05` | YES — comments not in canonical bytes |
| 50 | `card_id` | `TILTH-CIC-05` | YES |
| 55 | `tilth_cic_id` | `TILTH-CIC-05` | YES |
| 936 | `_research_metadata.priors_consulted[*].extract_note` | `TILTH-CIC-05` | YES — `_research_metadata` exempt subtree |
| 938 | `_research_metadata.priors_consulted[*].extract_note` | `TILTH-CIC-05` | YES |
| 950 | `_research_metadata.priors_consulted[*].extract_note` | `TILTH-CIC-05` + `Customer Identity Categories` | YES |
| 1222 | `_review_handback.surface_ambiguities[2]` | `TILTH-CIC-05` | YES — `_review_handback` exempt subtree |

**Verdict — LIVE regex set: 0 non-exempt findings.** Card passes.

### §2.5 Legacy-phrase defense scan

Grep for `[Cc]ustomer [Ii]nformation`: 0 hits.

**Verdict — legacy-phrase defense-in-depth: 0 findings.**

---

## §3. Research Findings

### §3.1 Source verification table — official + primary

| URL | Type | Access date | Fields supported | Confidence |
|---|---|---|---|---|
| https://www.rd.usda.gov/programs-services/business-programs/rural-cooperative-development-grant-program | official | 2026-05-15 | RCDG nonprofit-only eligibility + cooperative-development scope + Mutually Owned Business statutory category | HIGH |
| https://www.ecfr.gov/current/title-7/subtitle-B/chapter-XLII/part-4284/subpart-F | official | 2026-05-15 | RCDG statutory regulation | HIGH |
| https://www.rd.usda.gov/programs-services/business-programs/socially-disadvantaged-groups-grant | official | 2026-05-15 | SDGG eligibility + cooperative-development-center model + Socially Disadvantaged Group statutory category | HIGH |
| https://www.rd.usda.gov/programs-services/business-programs/value-added-producer-grants | official | 2026-05-15 | VAPG cooperative-priority eligibility category | HIGH |
| https://www.congress.gov/bill/115th-congress/house-bill/5236 | official | 2026-05-15 | Mainstreet Employee Ownership Act (Pub. L. 115-232) | HIGH |
| https://www.law.cornell.edu/uscode/text/26/subtitle-A/chapter-1/subchapter-T | official | 2026-05-15 | IRC Subchapter T (§§1381–1388) cooperative tax treatment + patronage-dividend definition | HIGH |
| https://www.law.cornell.edu/uscode/text/26/4975 | official | 2026-05-15 | 26 USC §4975(e)(7) ESOP statutory definition | HIGH |
| https://institute.coop/ | practitioner | 2026-05-15 | DAWI sector vocabulary | HIGH |
| https://www.usworker.coop/home/ | practitioner | 2026-05-15 | USFWC | HIGH |
| https://www.ica.coop/en/cooperatives/cooperative-identity | practitioner | 2026-05-15 | ICA Cooperative Identity Statement | HIGH |

### §3.2 New / refreshed sources to verify and add

| URL | Type | Why add | Card fields it would support | Confidence |
|---|---|---|---|---|
| https://www.aspeninstitute.org/programs/economic-opportunities-program/ | practitioner | Aspen Institute EOP — ESOP-track research / TA / capacity-building intermediary | New funder_program_keywords + priors_consulted | HIGH |
| https://project-equity.org/ | practitioner | Project Equity — ESOP-transition intermediary | New funder_program_keywords + priors_consulted | HIGH |
| https://www.nceo.org/ | practitioner | National Center for Employee Ownership (NCEO) — ESOP research + TA + member resource | optional priors_consulted | MEDIUM |
| https://www.sba.gov/funding-programs/loans/7a-loans | official | SBA 7(a) ESOP loan-guarantee pathway under Mainstreet Employee Ownership Act | refresh `funder_program_keywords[SBA 7(a) ESOP loan]` source_citation | HIGH |
| https://www.dol.gov/general/topic/health-plans/employerresponsibilities | official | DOL ERISA fiduciary-obligation guidance for ESOPs | optional `_research_metadata.priors_consulted` | MEDIUM |
| https://www.usda.gov/oce/sustainability/socially-disadvantaged-farmers-ranchers | official | USDA Socially Disadvantaged Farmer / Rancher framing — relevant for producer-cooperative + cooperative-priority routing | refresh substitution candidates in admin_risk_term["DEI / equity / inclusion"] | HIGH |
| https://www.democracycollaborative.org/community-wealth | practitioner | Democracy Collaborative community wealth-building framing — anchor for substitution candidates | optional priors_consulted | MEDIUM |
| https://www.cooperationjackson.org/ + https://theindustrialcommons.org/ + https://www.workingworld.org/ + https://highlandercenter.org/ + (removed per operator directive 2026-05-16 — do NOT reintroduce) | (anonymized per operator directive) | Per Phase D A.1 cleanup; do not reintroduce | NONE (anonymized) | N/A |
| https://www.cdfi.org/ + https://ofn.org/ | practitioner | CDFI Coalition + Opportunity Finance Network — cooperative-development CDFI cross-reference | optional priors_consulted | MEDIUM |
| https://www.cooperativedevelopmentfoundation.org/ | practitioner | Cooperative Development Foundation typical-grantee framing | refresh priors_consulted | MEDIUM |
| https://www.ncbaclusa.coop/ | practitioner | National Cooperative Business Association (NCBA CLUSA) | refresh sector vocabulary cross-reference | MEDIUM |

### §3.3 Internet Archive snapshot verification

Recommended for next Phase 4-CIC re-pass: USDA RD pages are relatively stable; cooperative-development practitioner orgs (NCEO / DAWI / USFWC / NCBA CLUSA) are stable. Cooperation Jackson + Industrial Commons + Working World + Highlander URLs are anonymized per operator directive; do NOT reintroduce.

---

## §4. Proposed Card Improvements

### §4.1 search_vocabulary / classification

- **`search_vocabulary.core_terms[NEW]` — add `cooperative housing` / `housing cooperative` (limited-equity / market-rate / mutual housing association), `mutual benefit corporation`, `cooperative association`, `cooperative-development center`.** Why: housing cooperative is the operator-flagged gap (`_review_handback.surface_ambiguities` line 1220); cooperative-development center is the sub-recipient pathway for USDA RCDG. **Seat:** Scout + Logician. **Where:** card body.
- **`search_vocabulary.core_terms[NEW]` — add `Subchapter T election`, `non-Subchapter-T cooperative` (operator-flagged at `_review_handback` line 1221).** Currently the patronage_model fact-class captures this implicitly; surfacing as core_term + KFR makes the Subchapter-T-or-not status surfaceable at intake. **Seat:** Scout + Logician. **Where:** card body.
- **`search_vocabulary.funder_program_keywords[NEW]` — add Aspen Institute EOP, Project Equity, NCEO (ESOP-track intermediaries); Democracy Collaborative community wealth-building portfolio; Cooperative Development Foundation typical grantee.** **Seat:** Scout. **Where:** card body.
- **`search_vocabulary.synonym_map[NEW]` — add `employee_ownership_transition` mapping (ESOP / employee ownership trust / EOT / worker-owner conversion / cooperative-conversion / cooperative-transition).** **Seat:** Scout. **Where:** card body.
- **`search_vocabulary.disqualifier_terms[NEW]` — add `for-profit-without-cooperative-bylaws applicant`, `ESOP-only applicant for true-cooperative-priority funder` (USDA RCDG, USFWC-aligned programs), `non-rural applicant for USDA RD rural-only program`.** **Seat:** Logician. **Where:** card body.

### §4.2 evidence capture / missing-evidence prompts

- **`evidence_signals[NEW]` — add `cooperative_governance_documentation_portfolio`.** source_pattern = "Bylaws current; articles of incorporation under state cooperative statute or LLC-with-cooperative-bylaws (for weak-statute states); member roster + member-class structure; board minutes (recent 12-months); patronage-allocation model + recent patronage-dividend payments; cooperative principles compliance attestation." weight = HIGH. freshness_tolerance_days = 365. source_citation = USDA RCDG + ICA Cooperative Identity Statement. **Seat:** Scribe + Logician. **Where:** card body.
- **`evidence_signals[NEW]` — add `subchapter_t_election_status_or_alternative`.** source_pattern = "Subchapter T election status; if non-Subchapter-T: alternative tax-treatment narrative (corporate / LLC pass-through / other) + rationale for non-election." weight = MEDIUM. freshness_tolerance_days = 365. source_citation = IRC §1388(a) + Subchapter T statute + state cooperative-statute variation. **Seat:** Scribe + Logician. **Where:** card body.
- **`evidence_signals[NEW]` — add `esop_erisa_compliance_documentation` (where applicant is ESOP).** source_pattern = "ESOP fiduciary committee membership; ESOP trustee compliance status; ERISA Section 408(e) prohibited-transaction review; annual ESOP appraisal cycle; SBA 7(a) ESOP loan-guarantee status (if applicable)." weight = HIGH. freshness_tolerance_days = 365. source_citation = 26 USC §4975(e)(7) + ERISA §407(d)(6) + Mainstreet Employee Ownership Act + SBA 7(a) ESOP guidance. **Seat:** Scribe + Logician. **Where:** card body.
- **`evidence_signals[NEW]` — add `member_equity_capitalization_documentation`.** source_pattern = "Member equity contribution model + member-class share structure + member-equity-raised-to-date + retained-earnings allocation + per-member account balances per cooperative governance." weight = HIGH. freshness_tolerance_days = 365. source_citation = USDA RCDG cooperative-development framework + ICA Cooperative Identity Principle 3 (Member Economic Participation). **Seat:** Scribe + Logician. **Where:** card body.

### §4.3 KFR fact classes + provenance_requirements

- **`kfr_fact_classes[NEW]` — add `cooperative_legal_form`.** description = "Entity legal form: state-statutory cooperative / LLC-with-cooperative-bylaws / federal cooperative / Subchapter T pass-through / Section 521 farmer-cooperative-tax-exempt / non-Subchapter-T cooperative / ESOP / employee ownership trust. State of incorporation; state cooperative-statute reference if applicable." typical_provenance = "articles of incorporation; bylaws; state filing record; Subchapter T election record; ERISA filings for ESOPs." **Where:** card body.
- **`kfr_fact_classes[NEW]` — add `member_class_and_governance_structure`.** description = "Member classes (worker / producer / consumer / multi-stakeholder); voting rights per class; board composition + member-elected seats; quorum + meeting cadence; conflict-of-interest policy." typical_provenance = "bylaws + member-class structure document + recent annual member meeting record." **Where:** card body.
- **`kfr_fact_classes[NEW]` — add `patronage_model_and_allocation`.** description = "Patronage dividend rate; allocation cycle; per-member-account tracking; retained-earnings allocation; written-notice-of-allocation compliance (Subchapter T §1388(a))." typical_provenance = "patronage policy + recent allocation memo + member-account reports." **Where:** card body.
- **`kfr_fact_classes[NEW]` — add `cooperative_capitalization_status`.** description = "Member equity to-date; equity-class structure; retained-earnings; debt-to-member-equity ratio; capitalization plan for growth + member-equity-raise targets." typical_provenance = "balance sheet + cooperative bylaws + capitalization plan." **Where:** card body.
- **`provenance_requirements[NEW]` — entries for new KFR fact-classes.** **Where:** card body.

### §4.4 drafting register / admin-risk handling

- **`admin_risk_term_register[REFINE]` — soften administration-time-anchoring per arts_culture defer-to-active-RFA pattern.** Per-entry reviewer_context tighten to defer-to-active-RFA-attestation language rather than naming current administration as binding context.
- **`admin_risk_term_register[NEW]` — add `cooperative commonwealth`** (movement-aligned framing). severity = HIGH. substitution_candidates = ["broad-based cooperative economy", "shared-ownership commonwealth (operator decides per RFA)", "community-wealth-building movement"]. reviewer_context = "Term carries explicit cooperative-movement provenance. Conservative + most centrist climates read as ideological. For soul-fire / USFWC-aligned funders, retain verbatim where active RFA uses it; otherwise substitute."
- **`admin_risk_term_register[NEW]` — add `cooperative principles` / `seven cooperative principles`** as canonical-vocabulary entry (not admin-risk-flagged for substitution but worth documenting as the operator-defensible framing). Per ICA Statement on the Cooperative Identity. **Recommendation:** include in `register_defaults` or `narrative_sections_typical` rather than admin_risk_term_register — these are operator-grade canonical-language anchors, not flagged risks.
- **OD-A v2.4 cross-CIC migration check.** The 10 admin_risk_term entries include 4–5 cross-CIC shared (DEI / equity / inclusion / commons / mutual aid / abolition / wealth redistribution). ≥3-card recurrence threshold met for some. Surface to workspace-register migration ceremony.

### §4.5 reviewer / rubric logic

- **`narrative_sections_typical[NEW]` — add `"Cooperative Governance Structure"`** as discrete section (member classes + board composition + voting rights + cooperative principles attestation). Currently bundled into `"Applicant Background"` per food_systems precedent.
- **`narrative_sections_typical[NEW]` — add `"Patronage Model and Allocation"`** as discrete section (Subchapter T compliance + per-member-account tracking + recent allocation history).
- **`narrative_sections_typical[NEW]` — add `"Member Equity Capitalization Plan"`** as discrete section (member-equity-raised + per-member-class structure + growth-capitalization roadmap).
- **`narrative_sections_typical[NEW]` — add `"ESOP / Worker-Owner Conversion Discipline"` (where applicable for transition-stage applicants)** documenting transition timeline + valuation + financing + governance ramp-up.

### §4.6 red-team probes / admin-risk register

- **`common_risk_register_entries[NEW]` — add `Cooperative governance misalignment`.** likelihood = MEDIUM. impact = HIGH. mitigation_pattern = "Bylaws-vs-practice alignment audit; recent annual member meeting record verification; member-class-structure-vs-declared-form alignment."
- **`common_risk_register_entries[NEW]` — add `Subchapter T election ambiguity`.** likelihood = MEDIUM. impact = MEDIUM. mitigation_pattern = "Subchapter T election status verified; if non-elected, alternative tax-treatment narrative + rationale documented before VAPG / RCDG / RBDG application."
- **`common_risk_register_entries[NEW]` — add `ERISA fiduciary-gap on ESOP`.** likelihood = MEDIUM. impact = HIGH. mitigation_pattern = "ESOP fiduciary committee membership current; annual ESOP appraisal cycle verified; ERISA Section 408(e) compliance review; SBA 7(a) ESOP loan covenant compliance if applicable."
- **`common_risk_register_entries[NEW]` — add `Member-equity dilution risk during growth`.** likelihood = MEDIUM. impact = MEDIUM. mitigation_pattern = "Capitalization plan models member-equity growth alongside debt + retained earnings; per-member-class dilution analysis + member-vote-required-for-significant-equity-change protocols."

### §4.7 reporting / commitment extraction

- **`reporting_cadence_typical.per_funder_overrides[NEW]` — add USDA RD SDGG + USDA RD RBDG + DOL Employee Ownership Initiative (EOI) + SBA 7(a) ESOP loan reporting + cooperative-development-center reporting.** **Seat:** Archivist + Report Generator.

### §4.8 memory namespace usefulness

Standard sub-keys mirroring siblings: `cards:cic:cooperative:scout_vocabulary` through `cards:cic:cooperative:draft_funder_candidates`.

### §4.9 Phase 4 fold-in discipline self-check

| Proposal | (a) | (b) | (c) | (d) |
|---|---|---|---|---|
| §4.1 core_terms / synonym_map / funder_program_keywords additions | NO | NO | NO | NO |
| §4.1 disqualifier_terms additions | NO | NO | NO | NO |
| §4.2 evidence_signals additions | NO | NO | NO | NO |
| §4.3 kfr_fact_classes / provenance_requirements additions | NO | NO | NO | NO |
| §4.4 admin_risk_term refines + adds | NO | NO | NO | NO |
| §4.5 narrative_sections_typical additions | NO | NO | NO | NO |
| §4.6 common_risk_register_entries additions | NO | NO | NO | NO |
| §4.7 reporting_cadence_typical.per_funder_overrides additions | NO | NO | NO | NO |

**Verdict:** No proposed change trips any of the four Phase 4 fold-in refusals.

---

## §5. Operator Decision Queue

1. **Defer-to-active-RFA reviewer_context tightening across all 10 admin_risk_term entries** (mirroring arts_culture pattern). Approval required per OQ-5.
2. **`cooperative commonwealth` admin_risk_term addition.** Approval required per OQ-5.
3. **`cooperative principles` / `seven cooperative principles`** documentation location — operator decides whether to land in `register_defaults` or `narrative_sections_typical` or both.
4. **OD-A v2.4 cross-CIC migration for shared terms** (DEI / equity / inclusion / commons / mutual aid / abolition / wealth redistribution).
5. **Housing cooperative scope expansion** — operator confirms whether `cooperative housing` core_term is in v0.1 Beta scope (current draft folds housing into consumer + multi-stakeholder per ICA convention).
6. **ESOP-vs-true-cooperative scope expansion** — operator confirms (per `_review_handback` line 1222) whether to keep both pathways in CIC-05 OR carve ESOP out to separate CIC variant in v1.x.
7. **Platform cooperative scope** — operator confirms (per `_review_handback` line 1223) whether platform cooperatives belong in CIC-05 or in CIC-06 Ecosystem Intermediary.
8. **Subchapter T election fact-class explicit treatment** — operator approves new `subchapter_t_election_status_or_alternative` evidence_signal + KFR fact_class.
9. **PA-specific state-overlay routing** — defer to v1.x cross-cutting amendment per food_systems / public_agency precedent.
10. **`cooperative-development center` core_term + evidence_signal pathway** — operator confirms scope for RCDG sub-recipient pathway.
11. **Lock-history housekeeping field disposition** (cross-card).
12. **Re-signing ceremony budget for card body changes.** ~22 distinct edits; bundle into cards-ceremony per Run 1 Patch Queue Batch B.

---

## §6. Validation Checklist

| Check | Result | Evidence |
|---|---|---|
| Schema fields complete against current §18.5 schema | PASS | 15/15 required CIC fields present |
| No forbidden coupling field names | PASS | Grep across file: 7 forbidden CIC-side names absent |
| No forbidden value-position regex matches outside exempt paths | PASS | §2.4 — 0 non-exempt findings; line 1222 inside `_review_handback` (exempt subtree) |
| No legacy-phrase `[Cc]ustomer [Ii]nformation` matches | PASS | 0 hits |
| No private organization-specific data in card body | PASS | Top-level common_funders_observed empty; named soul_fire-axis orgs fully anonymized per Phase D A.1 cleanup |
| No unsourced program-law claims at body | PASS at body | Statutory anchors cited (IRC Subchapter T, Mainstreet Employee Ownership Act, USDA RCDG 7 CFR 4284 Subpart F) |
| No excessive verbatim source text | PASS | Per OQ-4 |
| Lifecycle status consistent with architecture v7.0.11 §1.5 | PASS | All five lifecycle gate fields at pass-state |
| **Top-level `common_funders_observed:` is empty (Law-5 split per operator v2.1)** | PASS | Line 893 empty list; subagent candidates at `_research_metadata.draft_funder_candidates_pending_operator_engagement_confirmation` line 1059 |
| **No populated top-level `common_funders_observed` without operator-engagement-attestation** | PASS | Empty list |
| For multi-track CLCs: shared root + oneOf branch 2 compliance | N/A — CIC card |

**Net coupling-discipline regression: 0 findings.**

---

## §7. Regression Tests

### Test 1 — PA worker-owner conversion (LLC-with-cooperative-bylaws)

**Prompt:** "Five-person business in central PA exploring worker-owner conversion via LLC-with-cooperative-bylaws structure (PA has no comprehensive cooperative statute); seeking USDA RCDG sub-recipient pathway + SBA 7(a) ESOP loan-guarantee path."

**Pre-edit:** Scout matches `cooperative` / `worker-owned cooperative` / `RCDG` / `Mainstreet Employee Ownership Act`. Scribe drafts conversion narrative with bylaws + member roster + financing path. Logician fires admin_risk_term for movement vocabulary.

**Post-edit (with §4.1 + §4.2 + §4.3 + §4.6 additions):** Scout adds `cooperative-development center` core_term (RCDG sub-recipient pathway); `LLC-with-cooperative-bylaws` cooperative_legal_form KFR surfaces in intake; `subchapter_t_election_status_or_alternative` evidence_signal fires. Logician fires `Subchapter T election ambiguity` risk for PA non-Subchapter-T pathway. Scribe drafts narrative with conversion-pathway-specific bylaws-vs-practice alignment audit.

**Seat:** Scout + Scribe + Logician. **Pass criterion:** PA weak-statute reality surfaces explicitly; LLC-with-cooperative-bylaws form distinct from ESOP path.

### Test 2 — Multi-stakeholder food cooperative

**Prompt:** "Producer + consumer + worker multi-stakeholder food cooperative applying to USDA RFSP + VAPG + Cooperative Development Foundation."

**Pre-edit:** Scout matches `multi-stakeholder cooperative` / `RFSP` / `VAPG`. Scribe drafts member-class-structure narrative; Logician fires governance + Subchapter T compliance prompts.

**Post-edit (with §4.2 + §4.3 + §4.5 additions):** `member_class_and_governance_structure` KFR fact_class surfaces; `cooperative_governance_documentation_portfolio` evidence_signal fires HIGH; Scribe drafts discrete `"Cooperative Governance Structure"` narrative section + `"Patronage Model and Allocation"` section.

**Seat:** Scout + Scribe + Logician. **Pass criterion:** Multi-stakeholder member-class structure surfaces as discrete intake question.

### Test 3 — ESOP firm applying to SBA 7(a) + DOL EOI

**Prompt:** "Mid-size manufacturing firm in transition to 100% ESOP via SBA 7(a) loan-guarantee under Mainstreet Employee Ownership Act."

**Pre-edit:** Scout matches `ESOP` / `Mainstreet Employee Ownership Act` / `SBA 7(a)`. Scribe drafts narrative without explicit ERISA fiduciary discipline.

**Post-edit (with §4.2 + §4.3 + §4.6 additions):** `esop_erisa_compliance_documentation` evidence_signal fires HIGH; `cooperative_legal_form` KFR surfaces ESOP-specific structure; Logician fires `ERISA fiduciary-gap on ESOP` risk if applicant lacks fiduciary committee or annual appraisal.

**Seat:** Scout + Scribe + Logician. **Pass criterion:** ERISA fiduciary discipline surfaces at intake; distinct from true-cooperative compliance discipline.

### Test 4 — Soul-fire cooperative funder application

**Prompt:** "Worker-owner cooperative organizing as part of solidarity-economy intermediary network applying to soul-fire-aligned regional foundation."

**Pre-edit:** Scribe drafts narrative using `worker control` / `solidarity economy` / `mutual aid` per active RFA. Logician fires admin_risk_term entries HIGH severity. Operator approves per approval_required: true.

**Post-edit (with §4.4 defer-to-active-RFA refresh):** Per-entry reviewer_context defers to active-RFA-attestation language rather than naming current administration as binding context. Same operational outcome for soul-fire-aligned funder (retain vocabulary verbatim per RFA).

**Seat:** Scribe + Logician. **Pass criterion:** Movement vocabulary retained verbatim when active RFA uses it; substitutions surface only for federal-pass-through or centrist routing.

### Test 5 — Cards-ceremony post-condition

**Prompt:** "Cooperative-development CDFI applying to NCBA CLUSA-aligned foundation."

**Pre-cards-ceremony:** dialect_routing_table keyed on `funder_political_axis: centrist` (cooperative-development CDFI route); dialect `scribe.technical_precise`.

**Post-cards-ceremony:** dialect_routing_table row re-keys to `clc: operating_capacity` + `dialect: scribe.technical_precise` + `register_description: "cooperative-development CDFI underwriting register; governance + patronage + member equity vocabulary; technical-precise cooperative-development terminology"`.

**Seat:** Scribe + Judge. **Pass criterion:** Pre-ceremony body validates against v1.1 schema; post-ceremony validates against §18 v1.2 schema.

---

## §8. Patch Plan

### File: `pipeline/cards/CIC/cooperative.yaml`

**Ceremony shape:** supersession-re-sign per OD-E precedent. Parent_lock_row = 253.

**Edit set:**

1. Header comment normalization (line 45 — Patch A4 candidate).
2. `search_vocabulary.core_terms[NEW]` — cooperative housing / mutual benefit corporation / cooperative association / cooperative-development center / Subchapter T election / non-Subchapter-T cooperative (§4.1).
3. `search_vocabulary.synonym_map[NEW]` — employee_ownership_transition (§4.1).
4. `search_vocabulary.funder_program_keywords[NEW]` — Aspen Institute EOP / Project Equity / NCEO / Democracy Collaborative / Cooperative Development Foundation (§4.1).
5. `search_vocabulary.disqualifier_terms[NEW]` — for-profit-without-cooperative-bylaws / ESOP-only-for-true-cooperative-priority-funder / non-rural-for-USDA-RD-rural-only (§4.1).
6. `evidence_signals[NEW]` — cooperative_governance_documentation_portfolio / subchapter_t_election_status_or_alternative / esop_erisa_compliance_documentation / member_equity_capitalization_documentation (§4.2).
7. `kfr_fact_classes[NEW]` — cooperative_legal_form / member_class_and_governance_structure / patronage_model_and_allocation / cooperative_capitalization_status (§4.3).
8. `provenance_requirements[NEW]` — entries for new KFR fact-classes (§4.3).
9. `admin_risk_term_register[REFINE]` — defer-to-active-RFA reviewer_context across all 10 entries (§4.4).
10. `admin_risk_term_register[NEW]` — `cooperative commonwealth` (§4.4).
11. `narrative_sections_typical[NEW]` — `Cooperative Governance Structure` / `Patronage Model and Allocation` / `Member Equity Capitalization Plan` / `ESOP / Worker-Owner Conversion Discipline` (§4.5).
12. `common_risk_register_entries[NEW]` — Cooperative governance misalignment / Subchapter T election ambiguity / ERISA fiduciary-gap on ESOP / Member-equity dilution risk during growth (§4.6).
13. `reporting_cadence_typical.per_funder_overrides[NEW]` — USDA SDGG / USDA RBDG / DOL EOI / SBA 7(a) ESOP loan / cooperative-development-center reporting (§4.7).
14. `register_defaults` / dialect_routing_table refresh — bundle with cards-ceremony.

### File: `pipeline/cards/_schema/card_cic.schema.json`

15. Patch B20 (Run 1) + Patch B1 (Run 1) — cards-ceremony schema patches.

### File: `pipeline/institutional_memory/admin_risk_register.yaml`

16. Cross-CIC workspace-register migration candidates for shared terms (§4.4 + §5 item 4).

**OD-D Phase 4 forward-binding contract note:** All proposed edits value-position clean per §2.4 + Phase 4 fold-in clean per §4.9.

---

**Summary block:**

```
Card: CIC:cooperative
Card file: pipeline/cards/CIC/cooperative.yaml
Research hours actual: 1.5
Findings: 26 total — 0 P0, 13 P1, 13 P2
Decision queue: 12 operator approvals required
Conflicts with prior art: NONE (cross-card consistency with food_systems / public_agency / arts_culture admin_risk_term severity-tier mapping)
Coupling-discipline regression: NONE
Lifecycle gap surfaced: draft_status reads "signed" on disk; no normalization required per Run 1 P0-3
Review readiness: READY
```
