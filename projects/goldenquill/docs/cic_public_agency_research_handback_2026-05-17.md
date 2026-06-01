# TILTH-CIC-03 Public Agency — Research Handback

**Filed:** 2026-05-17
**Workspace:** `/Users/goldenquill/Downloads/GoldenQuill/`
**Run:** Run 2 of operator's controlled-batch sequence (Phase 4 CIC handbacks; 3 of 6).
**Card:** `pipeline/cards/CIC/public_agency.yaml` (Wave 2 LOCKed 2026-05-16 row 251; SHA-256 `ed1ce4…14b`; signed `2026-05-16T16:00:00Z`).
**Authority chain:** master prompt §2 + plan §1.3 + Run 1 priors (binding).
**Run 1 priors folded in:** all 14 cards on disk are `draft_status: "signed"` (P0-3 / L1-F0); §18 v1.2 LOCKed-but-not-applied (L2-F0); operator v2.1 Law-5 split uniformly applied (L2-F5); F-CARDS-COUPLING-VIOLATION-EXTENSION value-position regex NOT LIVE at runtime (L1-F3); operator reframe = aggressive content improvements OK.

---

## §1. Card Impact Thesis

`public_agency` is the compliance-stack-deepest CIC for the public-sector applicant type — municipalities, boroughs, townships, counties, authorities, special districts, public works departments, and (with operator-disambiguation) school districts acting as public entities. Its job is to make Tilth **read public-sector applicants through authority, public benefit, procurement, site control, match, engineering readiness, environmental review, public accountability, audit exposure** — and to do so without sliding into out-of-date Justice40-era movement vocabulary or under-serving the statutory-anchor density that public-agency reviewers expect.

What this card should cause Tilth to do differently:

1. When Scout sees `municipality`, `borough`, `township`, `county`, `authority`, `special district`, `unit of general local government`, anchor to 24 CFR 570.3 + the relevant state-code citation (PA Title 8 / Title 53 / 53 Pa.C.S. Ch. 56). When the applicant is a school district, surface the CIC-02 vs CIC-03 boundary question (capital improvement / public safety / broadband = CIC-03; education delivery = CIC-02).
2. When Scribe drafts a public-agency narrative, force statutory-compliance + public-benefit + engineering / technical + fiscal-stewardship registers per the four-layer prose at lines 444–465; reviewer profile determines which layer dominates.
3. When Logician audits draft, fire 2 CFR 200 procurement standards / Davis-Bacon / Build America Buy America (BABA) / NEPA + Section 106 / Title VI / Section 504 / URA / FFATA compliance prompts; force `governing_body_resolution` + `capital_improvement_plan` + `engineering_estimate` + `site_control_documentation` + `procurement_policy` + `match_commitment` + `environmental_review_status` + `audit_findings_clean_or_remediated` evidence at every public-agency claim.
4. When the active opportunity is federal under current administration framing, surface admin-risk-flagged vocabulary (environmental justice, racial justice, Justice40, equity, gentrification, anti-displacement, sanctuary, activist, abolition, anti-police, anti-development, climate justice, DEI) with substitution candidates that preserve substance via statutory anchors (LMI / CEJST tier / Section 104(d) / URA / ADA / Title VI LEP plan / FRPL / Section 504 / Tribal-specific statutory categories).
5. When match commitment is mentioned, force the federal-funds-as-match prohibition default disclosure (2 CFR 200.306) + per-program statutory carve-out citation if federal-source match is invoked (e.g., specific CDBG-DR appropriations provisions).
6. When audit posture surfaces, force the 2024-OMB-Final-Rule Single Audit threshold ($1M for FY beginning on or after 2024-10-01; prior $750K for earlier FY) per the card's explicit line 853 + 382 documentation — this is a 2026-relevant threshold change that sector-naive Scribes will get wrong.

The runtime-behavior delta this card produces is **statutory-anchor density + procurement / Davis-Bacon / BABA / NEPA / Title VI / Section 504 / URA compliance prompting + administration-aware admin-risk discipline on Justice40-era vocabulary + audit-threshold accuracy.** The card is currently strong on all four.

---

## §2. Current State Audit

### §2.1 What is strong now

- **Statutory-anchor density.** 28 core_terms with 1:1 CFR / USC / state-code / agency program citations. PA-specific statutory anchors (Title 8 boroughs, Title 53 cities/townships, PA Municipality Authorities Act of 1945 / 53 Pa.C.S. Ch. 56, PA Urban Redevelopment Law 35 P.S. §1701) cited at lines 58, 60, 64, 100.
- **Procurement + audit accuracy.** Lines 853 + 382 explicitly cite the 2024-OMB-Final-Rule Single Audit threshold change ($1M for FY beginning on or after 2024-10-01; prior $750K threshold for earlier FY). This is the kind of program-law update that sector-naive Scribes get wrong; the card has it right.
- **Match-prohibition discipline.** Federal-funds-as-match prohibition default (2 CFR 200.306) cited at lines 302 + 376 + 422. Per-program statutory carve-out citation required where federal-source match is invoked. This is exactly the kind of statutory-anchor density public-agency reviewers expect.
- **15 compliance frameworks.** Lines 844–908: SAM/UEI, 2 CFR 200, Davis-Bacon (40 USC §3141), BABA (IIJA §70901-70927), NEPA + Section 106 + Section 7, Title VI Civil Rights Act, Section 504 / ADA, URA, HUD CDBG Citizen Participation, FEMA Hazard Mitigation Planning, FFATA. Deeper than any other CIC.
- **14 admin_risk_term entries** (lines 494–694) all approval_required:true. Justice40-era framing acknowledged honestly (lines 540–550 on `Justice40` admin_risk_term entry). The card flags vocabulary without endorsing or repudiating; the dialect-aware substitution candidates preserve substance via statutory anchors (LMI / CEJST / SVI / EJScreen / URA / Section 104(d)).
- **Four-layer register prose.** Lines 444–465 enumerates four register layers: statutory / compliance, public-benefit, engineering / technical, fiscal-stewardship. Reviewer-profile-aware. Stronger than most CIC sub_register treatments.
- **`environmental_review_status` KFR fact-class + provenance_requirements with verbatim_quote_required: false** but with detailed required_citation_type — `"NEPA determination memo OR HUD ERR finding OR SHPO concurrence letter — by date and reviewing-agency citation"` (line 426). HUD CDBG Responsible Entity Environmental Review (24 CFR Part 58) named at line 320; USDA 7 CFR 1970 named at line 320; DOT 23 CFR 771 named at line 320.
- **Phase E Option 2 Law-5 cleanup.** Top-level `common_funders_observed: []` at line 992; subagent-populated candidates at `_research_metadata.draft_funder_candidates_pending_operator_engagement_confirmation:` line 1188.
- **Boundary discrimination prose** (lines 22–34). Important framing decision documented: Public Agency = applies; Tribal Nations are distinct statutory category; school districts overlap with CIC-02 Educator with operator-disambiguation per scope.
- **Multi-source match + commit-letter discipline.** `match_commitment` evidence_signal source_pattern (lines 302–305) is exceptionally detailed: cash-vs-in-kind breakdown; non-federal-vs-federal source disclosed; federal-funds-as-match prohibition status declared (default-prohibited under 2 CFR 200.306). This level of evidence-prompt density rare across CICs.

### §2.2 What is stale, ambiguous, over-broad, too local, too federal, or under-sourced

- **Justice40 status under current administration.** `Justice40` admin_risk_term reviewer_context (lines 540–550) says "Rescinded by current administration; references to Justice40 as a live framework will read as out-of-date in 2026 federal NOFOs." This is operator-defensible at authoring time but verifies-administration-dependently. Per master prompt §1.5 — program-status changes faster than card LOCK ceremonies; route program-status detail to Program Rule Packs. **Recommendation:** keep the admin-risk-vocabulary discipline; soften the operational program-status claim to "Justice40-as-a-named-policy-framework is undergoing transition; some related Federal investments may continue under different program names. Verify per active RFA before assuming Justice40 framework is operational."
- **`environmental justice` reviewer_context** (lines 502–516) carries 14-line operator-defensive prose. Operator-grade but verbose; runtime overhead is the verbose reviewer_context string. Acceptable cost at v0.1.
- **`dialect_routing_table` v1.1 shape with retired political-axis enum** (lines 470–482). Same status as siblings: LOCKed-but-not-applied per §18 v1.2; bottlenecked on cards-ceremony.
- **`sanctuary` admin_risk_term** (lines 596–608) carries explicit "no default substitution" + "operator must review per active funder + jurisdiction posture" — strong but the DOJ Byrne JAG framing is administration-dependent. Verify with operator at each administration transition.
- **PA-specific PennVEST + DCED CFA + DCED Keystone Communities + DCNR C2P2 + Multimodal entries** in funder_program_keywords (lines 236–253). State-overlay candidates per master prompt §1.3 + Run 1 P2-state-overlay-separation guidance. Operator decides.
- **No `Tribal Nation` core_term** — Tribal Nations are explicitly flagged as out-of-scope in disqualifier_terms (lines 258–260) and in the comment block (lines 25–30), but they're an under-represented adjacent statutory category. For Tilth's PA-anchored v0.1 scope, this is correct; v0.2 Wave 3 may extend Tribal-Nation-specific vocabulary.
- **No `regional council of governments` (COG)` or `metropolitan planning organization (MPO)`** core_terms. COGs and MPOs are public-agency applicants for many DOT BUILD/RAISE / SS4A / RCP / ATIIP awards; current core_terms cover `municipality / borough / township / county / authority / special district / public works department` but not regional-coordination entities.
- **No `community development corporation (CDC)` or `redevelopment authority subsidiary` boundary clarification.** CDCs are nonprofit entities that operate AS public-agency-implementing partners; they're not units of government themselves. The card's disqualifier_terms at lines 256–258 names "non-governmental applicant only" mismatches but doesn't surface the implementing-partner pathway (sub-recipient via CDBG entitlement).
- **`maintenance_and_operations_plan` evidence_signal at lines 332–335** has `weight: MEDIUM` but covers USDA RD CF managerial/financial/technical (MFT) capacity, EPA asset-management program, LWCF perpetuity stewardship. MFT capacity for USDA RD CF is HIGH-stakes for the long-term-asset-management score — recommend weight tightening for USDA RD CF context (or split into sub-weight per program).
- **No `EJScreen` or `CEJST` or `CDC SVI` named term in core_terms** — these tools appear in admin_risk_term reviewer_context (lines 501, 538, 668) and `census_and_disadvantaged_community_data` evidence_signal (line 307) but not as Scout vocabulary. Scout matching on these tool-name terms in an opportunity would surface the public_agency CIC + the appropriate disadvantaged-community-data discipline.
- **No `American Rescue Plan Act (ARPA) State and Local Fiscal Recovery Funds (SLFRF)`** named program. ARPA SLFRF was the largest federal-to-local-public-agency funding stream 2021–2024 (~$130B); some municipalities still report on remaining SLFRF balances. Reporting-cadence + audit-posture relevance.
- **Verbatim source-quote depth varies.** Some primary_sources carry verbatim quotes; some are framing references. Per OQ-4: ≤2 sentences each. Card respects this; deeper verification recommended per Phase 4-CIC re-pass.

### §2.3 Lifecycle / signature / schema concerns

- **`draft_status: signed`.** No normalization needed.
- **Header comment drift (P1-4).** Line 36: `# Lifecycle: draft. NO Ed25519 signature. Operator review pending before Wave 2 LOCK ceremony as separate dispatch.` Stale (per Run 1 Phase 1 §5). Recommend update.
- **`dialect_routing_table` v1.1 shape.** Same status: cards-ceremony bottleneck.
- **`_research_metadata.draft_funder_candidates_pending_operator_engagement_confirmation` field not schema-known.** Same status; cards-ceremony Patch B20.
- **Embedded `ed25519_signature` LIVE** (verify against Wave 2 row 251 supersession path post any future re-sign).
- **No `_review_handback` block visible at file end via grep.** The card uses `_research_metadata.priors_consulted` and `_research_metadata.primary_sources` per the canonical pattern; the Wave 2 review handback content is presumably consolidated in `pipeline/validation/cards_wave_2_thesis_2026-05-15/CIC/public_agency/` — confirm during cards-ceremony.

### §2.4 Coupling-discipline self-audit

**Results:**

| Line | Path | Match | Exempt? |
|---|---|---|---|
| 1 | (YAML header comment) | `TILTH-CIC-03` | YES — comments not in canonical bytes |
| 24 | (YAML header comment) | `TILTH-CIC-03` | YES |
| 41 | `card_id` | `TILTH-CIC-03` | YES |
| 46 | `tilth_cic_id` | `TILTH-CIC-03` | YES |
| 1039 | `_research_metadata.priors_consulted[2].extract_note` | `TILTH-CIC-03` | YES — `_research_metadata` exempt subtree |
| 1043 | `_research_metadata.priors_consulted[4].extract_note` | `TILTH-CIC-03` + `Customer Identity Categories` | YES |

**Verdict — LIVE regex set: 0 non-exempt findings.** Card passes.

### §2.5 Legacy-phrase defense scan

Grep for `[Cc]ustomer [Ii]nformation`: 0 hits.

**Verdict — legacy-phrase defense-in-depth: 0 findings.**

---

## §3. Research Findings

### §3.1 Source verification table — official + primary (current card)

| URL | Type | Access date | Fields supported | Confidence |
|---|---|---|---|---|
| https://www.hud.gov/program_offices/comm_planning/cdbg | official | 2026-05-15 | CDBG scope | HIGH |
| 24 CFR 570 (referenced throughout) | official | 2026-05-15 | CDBG eligibility / national objectives / LMI documentation | HIGH |
| 2 CFR 200 (referenced throughout) | official | 2026-05-15 | Uniform Guidance procurement / property / cost principles / reporting | HIGH |
| 24 CFR Part 58 (HUD ERR) | official | 2026-05-15 | HUD CDBG Responsible Entity Environmental Review | HIGH |
| 40 USC §3141 (Davis-Bacon) | official | 2026-05-15 | Davis-Bacon Act statutory anchor | HIGH |
| BABA IIJA §70901-70927 + 2 CFR Part 184 + OMB M-22-11 | official | 2026-05-15 | BABA compliance | HIGH |
| 44 CFR Part 201 (FEMA HMP) | official | 2026-05-15 | FEMA Hazard Mitigation Planning | HIGH |
| 24 CFR 91.105 (HUD Citizen Participation) | official | 2026-05-15 | HUD CDBG citizen-participation requirement | HIGH |

(The card has more primary_sources beyond line 1043; full source-verification pass deferred to next Phase 4-CIC re-dispatch.)

### §3.2 New / refreshed sources to verify and add

| URL | Type | Why add | Card fields it would support | Confidence |
|---|---|---|---|---|
| https://www.epa.gov/ejscreen | official | EJScreen is named in admin_risk_term reviewer_context but absent from core_terms; useful Scout vocabulary for disadvantaged-community-data thinking | New `search_vocabulary.core_terms` entry | HIGH |
| https://screeningtool.geoplatform.gov/en/ | official | CEJST (Climate and Economic Justice Screening Tool) — same | New core_term + cross-reference | HIGH |
| https://www.atsdr.cdc.gov/placeandhealth/svi/index.html | official | CDC SVI — same | New core_term + cross-reference | HIGH |
| https://home.treasury.gov/policy-issues/coronavirus/assistance-for-state-local-and-tribal-governments/state-and-local-fiscal-recovery-funds | official | ARPA SLFRF reporting + remaining-balance compliance still relevant for municipalities | New `funder_program_keywords` row + compliance_burdens entry for SLFRF tracking | MEDIUM (program closing out) |
| https://www.eda.gov/funding/programs/recompete | official | EDA Distressed Area Recompete Pilot Program — newer EDA program (CHIPS Act §10621A); absent from current `funder_program_keywords` | New funder_program_keywords row | HIGH |
| https://www.eda.gov/funding/programs/tech-hubs | official | EDA Tech Hubs — newer EDA program; some municipal-applicant tracks; absent from current `funder_program_keywords` | New funder_program_keywords row | HIGH |
| https://www.nrcs.usda.gov/programs-initiatives/cig-conservation-innovation-grants | official | USDA NRCS Conservation Innovation Grants (CIG) — some municipal-applicant tracks via state agencies | Optional new funder_program_keywords | MEDIUM |
| https://www.fema.gov/grants/mitigation/swift-current | official | FEMA Swift Current (BRIC subprogram for already-flooded properties) — newer FEMA program absent from current core_terms / funder_program_keywords | New funder_program_keywords row | MEDIUM |
| https://www.bls.gov/cpi/ | official | Davis-Bacon wage determination cycle — useful for source verification of wage determination process | Optional `_research_metadata.priors_consulted` | LOW |
| https://www.naco.org/ | practitioner | National Association of Counties — useful for cross-reference on county-applicant practice | Optional priors_consulted | LOW |
| https://www.nlc.org/ | practitioner | National League of Cities — useful for cross-reference on city/borough/township-applicant practice | Optional priors_consulted | LOW |
| https://www.nado.org/ | practitioner | National Association of Development Organizations — represents regional councils of governments + MPO networks; useful for new COG/MPO core_term scaffolding | Optional priors_consulted | MEDIUM |

### §3.3 Internet Archive snapshot verification

Recommended for next Phase 4-CIC re-pass: verify Wayback Machine snapshots of every primary_sources URL. EPA EJScreen + CEJST pages may have program-status restructuring under current administration. HUD CDBG + USDA RD pages are relatively stable. Treasury SLFRF reporting page is in close-out phase — high snapshot-volatility risk.

---

## §4. Proposed Card Improvements

### §4.1 search_vocabulary / classification

- **`search_vocabulary.core_terms[NEW]` — add `EJScreen`, `CEJST`, `CDC SVI`, `American Rescue Plan Act (ARPA) State and Local Fiscal Recovery Funds (SLFRF)`, `regional council of governments (COG)`, `metropolitan planning organization (MPO)`, `community development corporation (CDC) as sub-recipient`.** Why: Scout vocabulary gap for disadvantaged-community-data tooling + regional-coordination entities + nonprofit-implementing-partner pathway. **Seat:** Scout + Logician. **Where:** card body.
- **`search_vocabulary.funder_program_keywords[NEW]` — add `EDA Recompete`, `EDA Tech Hubs`, `FEMA Swift Current` (BRIC subprogram), `USDA NRCS CIG` (state-administered).** **Seat:** Scout. **Where:** card body.
- **`search_vocabulary.synonym_map[NEW]` — add `regional_coordination` mapping** (regional council of governments / COG / metropolitan planning organization / MPO / area agency on aging / regional planning commission / planning region). **Seat:** Scout. **Where:** card body.
- **`search_vocabulary.disqualifier_terms[NEW]` — add `private commercial product launch (no public-benefit framing)`, `Tribal-only set-aside (where municipal applicant)`, `pre-existing federal-funds-as-match-without-statutory-carve-out`.** Refines the existing disqualifier_terms list. **Seat:** Logician. **Where:** card body.

### §4.2 evidence capture / missing-evidence prompts

- **`evidence_signals[NEW]` — add `slfrf_compliance_status`.** source_pattern = "ARPA SLFRF expenditure-reporting submission record; remaining-balance attestation; SEFA inclusion if Single Audit threshold crossed; project-categorization compliance (revenue replacement / public health / negative economic impacts / premium pay / water/sewer/broadband / capital expenditure)." weight = MEDIUM. freshness_tolerance_days = 365. source_citation = Treasury Final Rule 31 CFR Part 35 + SLFRF Compliance and Reporting Guidance v4.1 (post-2024 cycle). **Seat:** Scribe + Logician. **Where:** card body.
- **`evidence_signals[NEW]` — add `regional_coordination_partnership`.** source_pattern = "Regional planning organization (COG / MPO / regional planning commission) MOU + role designation + sub-recipient relationship documentation if regional entity is implementing partner." weight = MEDIUM. freshness_tolerance_days = 365. source_citation = DOT BUILD / RAISE / SS4A / RCP regional-applicant eligibility; EDA Public Works regional-eligibility; HUD CDBG entitlement consortia. **Seat:** Scribe + Logician. **Where:** card body.
- **`evidence_signals[REFINE]` — `maintenance_and_operations_plan` weight split.** Currently MEDIUM. Recommend splitting: HIGH for USDA RD CF (MFT capacity scored), MEDIUM for EPA SRF asset-management programs, HIGH for LWCF perpetuity stewardship. Per master prompt rule 6 / §18.11 v1.1 — this is potentially refusal (a) compound-enum-value territory; safer to RAISE the existing single weight to HIGH (reflecting most stringent context) rather than introduce sub-weights per program.

### §4.3 KFR fact classes + provenance_requirements

- **`kfr_fact_classes[NEW]` — add `regional_coordination_status`.** description = "Membership in regional council of governments / MPO / regional planning commission; specific implementation partnerships; project-area coordination scope across multi-jurisdictional applicant cluster." typical_provenance = "regional org MOU; council resolution authorizing regional participation; project-area map." **Where:** card body.
- **`kfr_fact_classes[NEW]` — add `slfrf_compliance_status_and_remaining_balance`.** description = "ARPA SLFRF allocation + obligation status; project-categorization status; remaining-balance status; SEFA inclusion if applicable." typical_provenance = "Treasury reporting submission record; council resolution per SLFRF project; SEFA." **Where:** card body.
- **`provenance_requirements[NEW]` — entries for `regional_coordination_status` and `slfrf_compliance_status_and_remaining_balance`.** **Where:** card body.

### §4.4 drafting register / admin-risk handling

- **`admin_risk_term_register[REFINE]` — `Justice40` reviewer_context** (lines 540–550). Recommend rewrite: "Justice40 as a named policy framework is undergoing transition; some related federal investments may continue under different program names. Verify per active RFA before assuming Justice40 framework is operational. Some state and foundation programs still adopt Justice40-style targeting under different names; cite the underlying targeting tool by name (CEJST / EJScreen / SVI). For soul_fire-oriented funders, retain verbatim if the RFA itself uses it; otherwise substitute to the underlying targeting tool by name." Per Law 4: approval_required: true preserved.
- **`admin_risk_term_register[REFINE]` — `environmental justice` reviewer_context** (lines 502–516). Same administration-neutralizing edit. Keep the dialect-aware substitution candidates; soften the administration-status claim.
- **`admin_risk_term_register[NEW]` — add `community benefit agreement (CBA)`.** severity = MEDIUM. substitution_candidates = ["public-private partnership benefit terms", "community investment plan", "project labor agreement (PLA) compliance documentation where applicable", "anchor-institution commitment letter"]. reviewer_context = "Term reads as movement-aligned framing in conservative review climates and as standard public-private-partnership practice in centrist + progressive climates. Federal programs vary widely on acceptance. For HUD CDBG, statutory authority is the framework — cite 24 CFR 570 directly. For DOT BUILD/RAISE, CBAs are routinely cited but no statutory anchor. Operator decides per RFA + applicant funder mix." approval_required: true.
- **`admin_risk_term_register[NEW]` — add `displacement` (in addition to `gentrification` + `anti-displacement` already present).** severity = MEDIUM. substitution_candidates = ["population-stability indicator", "Uniform Relocation Act-anchored displacement-risk analysis", "Section 104(d) one-for-one replacement housing analysis"]. reviewer_context = "Less politically loaded than 'gentrification' but in the same vocabulary family. Statutory anchor (URA + Section 104(d)) preferred in conservative review climates."
- **OD-A v2.4 cross-CIC migration check.** Card has 14 admin_risk_term entries; many cross-CIC shared (DEI / equity / inclusion / climate justice / racial justice / activist / anti-displacement). ≥3-card recurrence threshold met. Surface to OD-A workspace-register migration ceremony.

### §4.5 reviewer / rubric logic

- **`narrative_sections_typical[REFINE]` — `Partnerships and Sub-recipients` section** (already present at line 800–801). Refine: name `regional council of governments (COG) / metropolitan planning organization (MPO) participation` + `nonprofit / CDC / housing authority sub-recipient relationship` explicitly to ensure Scribe surfaces these explicitly in narrative scaffold.
- **`narrative_sections_typical[NEW]` — add `"Build America Buy America (BABA) Compliance and Domestic-Content Certification"` between `"Procurement and Build America Buy America Compliance"` and `"Environmental Review"`.** Currently BABA is folded into the procurement-section name; some federal NOFOs require BABA as discrete narrative. Recommend split.

### §4.6 red-team probes / admin-risk register

- **`common_risk_register_entries[NEW]` — add `Sub-recipient monitoring discipline gap` (2 CFR 200.331-200.333).** likelihood = MEDIUM. impact = HIGH. mitigation_pattern = "Documented sub-recipient monitoring protocol; risk-assessment + Single-Audit-status verification at sub-award + during-period-of-performance; pass-through-entity responsibilities per 2 CFR 200.332 mapped to applicant's compliance team."
- **`common_risk_register_entries[NEW]` — add `Regional-coordination authority ambiguity`.** likelihood = MEDIUM. impact = HIGH. mitigation_pattern = "When applicant is regional council of governments (COG) or MPO, source-of-authority must be documented (state-enabling statute; member-jurisdiction resolutions); when applicant is a member jurisdiction acting under regional plan, regional org's role + scope of authority documented."
- **`common_risk_register_entries[NEW]` — add `SLFRF remaining-balance + categorization-shift risk`.** likelihood = MEDIUM. impact = MEDIUM. mitigation_pattern = "Project-categorization compliance per Treasury Final Rule; remaining-balance attestation current; remaining-allocation deployment per obligation deadlines; SEFA inclusion verified."

### §4.7 reporting / commitment extraction

- **`reporting_cadence_typical.per_funder_overrides[NEW]` — add EDA Recompete + EDA Tech Hubs + FEMA Swift Current + USDA NRCS CIG.** **Seat:** Archivist + Report Generator. **Where:** card body.

### §4.8 memory namespace usefulness

Standard sub-keys mirroring food_systems / educator pattern:
- `cards:cic:public_agency:scout_vocabulary`
- `cards:cic:public_agency:evidence_signals`
- `cards:cic:public_agency:kfr_fact_classes`
- `cards:cic:public_agency:provenance_requirements`
- `cards:cic:public_agency:register_defaults`
- `cards:cic:public_agency:dialect_routing_table`
- `cards:cic:public_agency:admin_risk_terms`
- `cards:cic:public_agency:reporting_cadence`
- `cards:cic:public_agency:metrics_template`
- `cards:cic:public_agency:narrative_sections`
- `cards:cic:public_agency:capacity_signals`
- `cards:cic:public_agency:compliance_burdens`
- `cards:cic:public_agency:common_risks`
- `cards:cic:public_agency:common_funders_observed`
- `cards:cic:public_agency:draft_funder_candidates`

### §4.9 Phase 4 fold-in discipline self-check

| Proposal | (a) | (b) | (c) | (d) |
|---|---|---|---|---|
| §4.1 core_terms / synonym_map / funder_program_keywords additions | NO | NO | NO | NO |
| §4.1 disqualifier_terms additions | NO | NO | NO | NO |
| §4.2 evidence_signals additions (SLFRF / regional coordination) | NO | NO | NO | NO |
| §4.2 maintenance_and_operations_plan weight RAISE to HIGH | NO — refines weight within canonical HIGH/MEDIUM/LOW set | NO | NO | NO |
| §4.3 kfr_fact_classes additions + provenance_requirements pairings | NO | NO | NO | NO |
| §4.4 admin_risk_term refines + adds | NO — refines within canonical entry shape | NO | NO | NO |
| §4.5 narrative_sections_typical additions | NO | NO | NO | NO |
| §4.6 common_risk_register_entries additions | NO | NO | NO | NO |
| §4.7 reporting_cadence_typical.per_funder_overrides additions | NO | NO | NO | NO |
| §4.8 memory namespace sub-keys | N/A — architecture decision | N/A | N/A | N/A |

**Verdict:** No proposed change trips any of the four Phase 4 fold-in refusals.

---

## §5. Operator Decision Queue

1. **`Justice40` + `environmental justice` reviewer_context administration-neutralizing rewrites.** Approval required per OQ-5.
2. **`community benefit agreement (CBA)` + `displacement` admin_risk_term additions.** Approval required per OQ-5.
3. **OD-A v2.4 cross-CIC migration for shared terms.** DEI / equity / inclusion / climate justice / racial justice / activist / anti-displacement appear ≥3 cards; dispatch workspace-register migration ceremony.
4. **PA-specific state-overlay routing.** PennVEST / DCED CFA / DCED Keystone Communities / DCNR C2P2 / PA DCED Multimodal Transportation Fund in funder_program_keywords are PA-anchored. Per master prompt §1.3 + Run 1 P2 — base card OR PA-state overlay? Defer to v1.x cross-cutting amendment per food_systems precedent.
5. **`Tribal Nation` core_term scope expansion** (vs disqualifier_terms-only treatment). Operator confirms whether Tribal-Nation-specific applicant pathway is in v0.1 Beta scope.
6. **`regional council of governments (COG)` / `metropolitan planning organization (MPO)` core_terms + `regional_coordination_status` KFR fact-class additions.** Operator confirms scope in v0.1.
7. **ARPA SLFRF tracking entries.** Program is closing out; relevance still high for municipalities reporting remaining balances. Operator confirms timing — bundle now or defer.
8. **`sanctuary` admin_risk_term DOJ Byrne JAG framing refresh.** Verify with operator on next administration transition.
9. **Lock-history housekeeping field disposition** (cross-card).
10. **Re-signing ceremony budget for card body changes.** ~20 distinct edits; bundle into cards-ceremony per Run 1 Patch Queue Batch B as `public_agency` supersession-re-sign.

---

## §6. Validation Checklist

| Check | Result | Evidence |
|---|---|---|
| Schema fields complete against current §18.5 schema | PASS | 15/15 required CIC fields present |
| No forbidden coupling field names | PASS | Grep across file: none of 7 forbidden CIC-side names appear |
| No forbidden value-position regex matches outside exempt paths | PASS | §2.4 — 0 non-exempt findings |
| No legacy-phrase `[Cc]ustomer [Ii]nformation` matches | PASS | 0 hits |
| No private organization-specific data in card body | PASS | Top-level common_funders_observed empty |
| No unsourced program-law claims at body | PASS | Card carries program-law sparingly (2024 OMB Single Audit threshold; FEMA BRIC 25% non-federal cost share standard; specific 2 CFR section citations); these are statutory-anchor citations, not active-cycle program-law. |
| No excessive verbatim source text | PASS | Per OQ-4 |
| Lifecycle status consistent with architecture v7.0.11 §1.5 | PASS | All five lifecycle gate fields at pass-state |
| **Top-level `common_funders_observed:` is empty (Law-5 split per operator v2.1)** | PASS | Line 992 `common_funders_observed: []`; subagent candidates at `_research_metadata.draft_funder_candidates_pending_operator_engagement_confirmation` line 1188 |
| **No populated top-level `common_funders_observed` without operator-engagement-attestation** | PASS | Empty list |
| For multi-track CLCs: shared root + oneOf branch 2 compliance | N/A — CIC card |

**Net coupling-discipline regression: 0 findings.**

---

## §7. Regression Tests

### Test 1 — Municipal water-infrastructure project (CDBG / SRF stacking)

**Prompt:** "Borough of 8,000 population in Western PA applying for combined CDBG + PennVEST funding for a wastewater treatment plant upgrade with stormwater management component."

**Pre-edit:** Scout matches `borough` / `municipality` / `wastewater treatment` / `stormwater` — routes toward CDBG state allocation + PennVEST + USDA RD Water/Environmental Programs. Scribe drafts statutory-compliance + engineering registers. Logician fires NEPA + Davis-Bacon + BABA + 2 CFR 200 procurement prompts.

**Post-edit (with §4.1 additions):** Scout adds disadvantaged-community-data tools (EJScreen / CEJST / SVI core_terms) — surfaces explicit per-tool routing for federal-EJ-aligned scoring components. Scribe surfaces `regional_coordination_partnership` evidence_signal if regional COG / MPO involvement is in scope. Logician fires SLFRF tracking if borough has ARPA SLFRF remaining balance.

**Seat:** Scout + Scribe + Logician. **Pass criterion:** EJScreen / CEJST / SVI surface in Scout output when service-area-demographic component is requested by active RFA.

### Test 2 — County hazard mitigation BRIC application

**Prompt:** "Rural county applying to FEMA BRIC for flood-mitigation infrastructure protecting 300 structures in distressed-community service area."

**Pre-edit:** Scout matches `county` / `BRIC` / `hazard mitigation`. Scribe drafts FEMA BRIC narrative with benefit-cost analysis (BCA) cost input + Federally-approved Hazard Mitigation Plan reference. Logician fires NEPA + Section 106 + Title VI + URA prompts.

**Post-edit (with §4.4 admin_risk_term refines):** `climate justice` reviewer_context refresh (lines 666–680) routes substitution to BRIC's own "distressed and impoverished communities" priority language when active RFA framing aligns; retains verbatim if soul_fire-aligned funder. Logician audits per refresh; operator approves via approval_required: true.

**Seat:** Scribe + Logician. **Pass criterion:** climate-justice vocabulary routes per BRIC distressed-community-priority language; retained verbatim only when applicable.

### Test 3 — ARPA SLFRF remaining-balance compliance

**Prompt:** "City applying for HUD CDBG entitlement allocation; has $500K remaining ARPA SLFRF balance allocated to public-health category."

**Pre-edit:** Scout matches `city` / `CDBG`. Scribe drafts CDBG narrative without SLFRF disclosure framing. Logician does NOT fire SLFRF tracking — field absent.

**Post-edit (with §4.2 + §4.3 + §4.6 additions):** `slfrf_compliance_status` evidence_signal fires (MEDIUM weight). `slfrf_compliance_status_and_remaining_balance` KFR fact-class surfaces in intake. Logician fires `SLFRF remaining-balance + categorization-shift risk` common_risk_register_entries if balance is at risk of deobligation.

**Seat:** Scout + Scribe + Logician. **Pass criterion:** SLFRF tracking surfaces; project-categorization compliance documented.

### Test 4 — Regional COG applicant

**Prompt:** "Regional council of governments (COG) representing 12 member jurisdictions applying for EDA Public Works planning grant."

**Pre-edit:** Scout matches `EDA Public Works`. No `regional council of governments (COG)` core_term — Scout doesn't fire COG-specific scaffolding. Scribe drafts as if applicant is single-jurisdiction.

**Post-edit (with §4.1 + §4.2 + §4.3 + §4.6 additions):** Scout matches `regional council of governments (COG)` core_term + `regional_coordination` synonym_map. Scribe surfaces `regional_coordination_partnership` evidence_signal + `regional_coordination_status` KFR. Logician fires `Regional-coordination authority ambiguity` risk if member-jurisdiction-resolution documentation is thin.

**Seat:** Scout + Scribe + Logician. **Pass criterion:** COG vocabulary surfaces; regional-coordination evidence prompts fire.

### Test 5 — Cards-ceremony post-condition (dialect_routing_table re-keyed)

**Prompt:** "Municipality applying to EPA CWSRF for combined sewer overflow remediation."

**Pre-cards-ceremony:** dialect_routing_table keyed on `funder_political_axis: centrist`, dialect `scribe.technical_precise`. Scribe selects technical_precise register.

**Post-cards-ceremony:** dialect_routing_table row re-keys to `clc: public_purpose_works` + `dialect: scribe.technical_precise` + `register_description: "EPA SRF state-administered technical-reviewer panel; engineering / regulatory-driver register; Intended Use Plan integration"` + optional `example_program: "EPA CWSRF"`. Same operational outcome.

**Seat:** Scribe + Judge. **Pass criterion:** Pre-ceremony body validates against v1.1 schema; post-ceremony validates against §18 v1.2 schema.

---

## §8. Patch Plan

### File: `pipeline/cards/CIC/public_agency.yaml`

**Ceremony shape:** supersession-re-sign per OD-E precedent. Parent_lock_row = 251.

**Edit set:**

1. Header comment normalization (line 36 — Patch A4 candidate).
2. `search_vocabulary.core_terms[NEW]` — `EJScreen`, `CEJST`, `CDC SVI`, `ARPA SLFRF`, `COG`, `MPO`, `CDC sub-recipient` (§4.1).
3. `search_vocabulary.synonym_map[NEW]` — `regional_coordination` mapping (§4.1).
4. `search_vocabulary.funder_program_keywords[NEW]` — EDA Recompete / EDA Tech Hubs / FEMA Swift Current / USDA NRCS CIG (§4.1).
5. `search_vocabulary.disqualifier_terms[NEW]` — private commercial product launch / Tribal-only set-aside boundary clarification / pre-existing federal-funds-as-match-without-statutory-carve-out (§4.1).
6. `evidence_signals[NEW]` — `slfrf_compliance_status`, `regional_coordination_partnership` (§4.2).
7. `evidence_signals[REFINE]` — `maintenance_and_operations_plan` weight raise to HIGH (§4.2).
8. `kfr_fact_classes[NEW]` — `regional_coordination_status`, `slfrf_compliance_status_and_remaining_balance` (§4.3).
9. `provenance_requirements[NEW]` — entries for new KFR fact-classes (§4.3).
10. `admin_risk_term_register[REFINE]` — `Justice40` + `environmental justice` reviewer_context administration-neutralizing rewrites (§4.4).
11. `admin_risk_term_register[NEW]` — `community benefit agreement (CBA)`, `displacement` (§4.4).
12. `narrative_sections_typical[REFINE]` — `Partnerships and Sub-recipients` section refinement (§4.5).
13. `narrative_sections_typical[NEW]` — `"Build America Buy America (BABA) Compliance and Domestic-Content Certification"` discrete section (§4.5).
14. `common_risk_register_entries[NEW]` — `Sub-recipient monitoring discipline gap`, `Regional-coordination authority ambiguity`, `SLFRF remaining-balance + categorization-shift risk` (§4.6).
15. `reporting_cadence_typical.per_funder_overrides[NEW]` — EDA Recompete / EDA Tech Hubs / FEMA Swift Current / USDA NRCS CIG (§4.7).
16. `register_defaults` / dialect_routing_table refresh — bundle with cards-ceremony post-§18 v1.2 (§4.5).

### File: `pipeline/cards/_schema/card_cic.schema.json`

17. Patch B20 (Run 1) — `_research_metadata.draft_funder_candidates_pending_operator_engagement_confirmation` schema-known.
18. Patch B1 (Run 1) — §18 v1.2 dialect_routing_table re-key.

### File: `pipeline/institutional_memory/admin_risk_register.yaml`

19. Cross-CIC workspace-register migration candidates for shared terms (§4.4 + §5 item 3).

**OD-D Phase 4 forward-binding contract note:** Edit set 1–16 is value-position clean per §2.4 + Phase 4 fold-in clean per §4.9. Edits 17–18 are cards-ceremony schema patches.

---

**Summary block:**

```
Card: CIC:public_agency
Card file: pipeline/cards/CIC/public_agency.yaml
Research hours actual: 1.6
Findings: 25 total — 0 P0, 12 P1, 13 P2
Decision queue: 10 operator approvals required
Conflicts with prior art: NONE
Coupling-discipline regression: NONE
Lifecycle gap surfaced: draft_status reads "signed" on disk; no normalization required per Run 1 P0-3
Review readiness: READY
```
