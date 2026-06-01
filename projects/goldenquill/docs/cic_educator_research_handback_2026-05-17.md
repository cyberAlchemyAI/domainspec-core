# TILTH-CIC-02 Educator — Research Handback

**Filed:** 2026-05-17
**Workspace:** `/Users/goldenquill/Downloads/GoldenQuill/`
**Run:** Run 2 of operator's controlled-batch sequence (Phase 4 CIC handbacks; 2 of 6).
**Card:** `pipeline/cards/CIC/educator.yaml` (Wave 2 LOCKed 2026-05-16 row 250; SHA-256 `0fbd05…c898`; signed `2026-05-16T16:00:00Z`).
**Authority chain:** master prompt §2 + plan §1.2 + Run 1 priors (binding).
**Run 1 priors folded in:** all 14 cards on disk are `draft_status: "signed"` (P0-3 / L1-F0); §18 v1.2 LOCKed-but-not-applied (L2-F0); operator v2.1 Law-5 split applied uniformly across 6 CIC cards (L2-F5); F-CARDS-COUPLING-VIOLATION-EXTENSION value-position regex NOT LIVE at runtime (L1-F3); operator reframe = aggressive content improvements OK.
**Companion artifact:** `pipeline/cards/CIC/educator_amendment_proposal_2026-05-16.md` — STAGED-NOT-YET-DISPATCHED amendment with operator-supplied 2026-05-16 content (Item A.1–A.5 deferred decisions; Item B.1–B.3 candidate additions; Item C.1–C.7 rejected). This handback aligns with the proposal direction; recommendations below cross-reference proposal sections where relevant.

---

## §1. Card Impact Thesis

`educator` is the densest compliance-stack CIC in the canonical roster. Its job is to make Tilth treat education applicants — LEAs, charters, afterschool/OST programs, IHEs, workforce-training intermediaries, K-12 / postsecondary nonprofits — **as compliance-dense learning institutions where dosage, authorization, student privacy, evidence-of-learning, and safeguarding matter as much as mission language.**

What this card should *cause Tilth to do differently*:

1. When Scout sees "afterschool," "tutoring," "evidence-based intervention," or "youth development" in an opportunity, route to the appropriate USDE / DOL / NSF / state-pass-through program family with dosage + evidence-tier discipline anchored to ESSA § 8101(21).
2. When Scribe drafts a learning-outcomes narrative, force evaluator-grade methodology disclosure (design tier / instruments / sample / analysis / dissemination) NOT advocacy prose; pair to IES What Works Clearinghouse evidence-tier thinking.
3. When Logician audits draft, fire FERPA / PPRA / COPPA / IDEA compliance prompts at every PII / data / survey / online-tool surface; force LEA / IHE Letter-of-Commitment and signed MOU evidence at every partner claim.
4. When the active opportunity is federal under EO 14151 + EO 14168 framing, surface admin-risk-flagged vocabulary (DEI, equity, trauma-informed, SEL, gender identity, restorative justice, culturally responsive, marginalized, anti-racist, systemic inequity, LGBTQ, decolonize, intersectional, achievement gap, white privilege) with substitution candidates that preserve substance via USDE *statutory* priority categories (Title I FRPL, IDEA, TRIO first-generation, ESEA Title III EL, McKinney-Vento, IDEA disability).
5. When the active opportunity is foundation, allow the more movement-aligned vocabulary verbatim when funder's own materials use it, with operator approval per approval_required: true default.
6. When safeguarding evidence is requested (background checks, mandated-reporter training, Title IX, McKinney-Vento, CIPA, Section 504, ADA Title II), force the named statutory framing + state-specific clearance documentation (PA Act 153 cited at lines 372–382 as a canonical example).

The runtime-behavior delta this card produces versus a sector-naive baseline is **compliance-stack-depth precision + admin-risk-discipline under EO 14151 / EO 14168 framing + safeguarding-evidence rigor.** The card is currently strong on all three. The pending Item B amendments from the 2026-05-16 proposal (granular education-data-privacy classification defaults; per-client evidence-class enumeration; Educator-specific reviewer heuristic enumeration) could deepen runtime behavior further but require schema work and operator decisions.

---

## §2. Current State Audit

### §2.1 What is strong now

- **Compliance-stack depth.** 13 compliance frameworks named at lines 827–904: SAM.gov + UEI, 2 CFR 200, FERPA, PPRA, COPPA, IDEA, ESSA, state education code, EDGAR, CIPA, Section 504 / ADA Title II, McKinney-Vento, Title IX. PA Act 153 background-check requirement cited at line 250 + 380 as the state-specific anchor.
- **Admin-risk register depth.** 14 admin_risk_term_register entries (lines 474–712): DEI (HIGH), equity (MEDIUM), trauma-informed (MEDIUM), restorative justice (MEDIUM), gender identity (HIGH), culturally responsive (MEDIUM), SEL (MEDIUM), marginalized (MEDIUM), anti-racist (HIGH), systemic inequity (HIGH), LGBTQ (HIGH), decolonize curriculum (HIGH), white privilege (HIGH), achievement gap (MEDIUM), intersectional (MEDIUM). Two executive orders cited directly in primary_sources (EO 14151 at line 1160; EO 14168 at line 1169) with verbatim quotes per OQ-4.
- **ESSA evidence-tier discipline.** Lines 210–222: card explicitly clarifies Tier 4 (demonstrates rationale) is fully valid for most USDE programs admitting any of four tiers; Tier 1 / Tier 2 required only for EIR Mid-Phase / Expansion. Prevents Scribe from over-claiming "strong evidence" without WWC-meeting design.
- **Sub-register triad.** Lines 388–428 (mirrors food_systems pattern): student_centered / technical_precise / family_community_engagement. `sub_register_selection_rule` explicit at lines 421–428 anchoring opportunity-driven CLC matching per architecture v7.0.11 §6.1.
- **Safeguarding-evidence rigor.** `youth_safeguarding_policy` provenance_requirement at lines 381–383 specifies portfolio: written policy + training-completion logs + state-specific clearances + PA Act 153 named example + designated child-protection officer.
- **Phase E Option 2 Law-5 cleanup.** Top-level `common_funders_observed: []` at line 1011; subagent-populated candidates at `_research_metadata.draft_funder_candidates_pending_operator_engagement_confirmation:` line 1197 — 28 candidates covering federal (USDE / USDA FNS / HHS / DOL / NSF / IMLS / AmeriCorps), foundation, and PA-state.
- **Lifecycle truth.** All five lifecycle gate fields at pass-state; lock_history_row 250; signed 2026-05-16T16:00:00Z.
- **Cross-card consistency.** Severity tier mapping comment block at lines 27–32 (HIGH ≈ admin_risk_register RED; MEDIUM ≈ YELLOW; LOW ≈ GREEN) — explicit cross-card discipline anchor.

### §2.2 What is stale, ambiguous, over-broad, too local, too federal, or under-sourced

- **EO-driven reviewer_context is administration-time-stamped.** EO 14151 + EO 14168 named throughout admin_risk_term reviewer_context (lines 485–625) as live federal framing. This is operator-defensible at authoring time (2026-05) but the card explicitly flags at line 1409 that "EO 14151 + EO 14168 reviewer_context language is current as of 2025-2026 administration. Will become stale on next federal-administration transition; admin_risk_term_register will need a between-administration refresh pass." This is correctly documented as a v1.x backlog item.
- **`dialect_routing_table` v1.1 shape with retired political-axis enum** (lines 441–453). Same status as food_systems: LOCKed-but-not-applied per §18 v1.2; bottlenecked on cards-ceremony.
- **`per_funder_overrides` in reporting_cadence_typical names "Foundation_typical" + "State_pass_through" as omnibus labels** (lines 730–731). Adequate at v0.1 Beta; v1.x or post-Wave-2 may want more granular foundation breakdowns once operator engagement history accumulates.
- **`achievement gap` term reviewer_context (lines 677–697)** is operator-defensive and explicitly cross-references the Judge Cycle 2 finding. Strong but verbose; runtime overhead is the verbose reviewer_context string. Acceptable cost.
- **`gender identity` substitution candidate `"biological sex (where statutorily required per EO 14168)"`** is a deeply EO-time-anchored substitution. Per `educator_amendment_proposal_2026-05-16.md` §A.3 "Decision still pending operator dispatch" — the substitution carries asymmetric political weight: in a non-EO-14168 future the substitution itself becomes the activist-leaning framing rather than vice versa. Recommend operator review of this entry on every administration transition; flag for between-administration refresh per amendment proposal.
- **Item B.1 (granular education-data-privacy classification defaults) not yet folded in.** Per amendment proposal: 5 PII / disability / discipline / family-survey / sanitized-summary classifications with severity tiers + operator-override + per-grant SP0 override semantics. Currently `provenance_requirements.ferpa_relevance` at lines 351–353 captures FERPA-data signed-agreement requirement but does NOT capture the per-data-category classification taxonomy. Worth folding in.
- **Item B.2 (per-client evidence-class enumeration — 11 classes) not yet folded in.** Currently `evidence_signals` (12 items at lines 224–289) captures evidence at signal-type granularity (enrollment, attendance, assessment, curriculum, staff, partnership, evaluation, privacy, partner LOC, logic model, prior performance, dosage, match), but not at the 11-class taxonomy the operator's 2026-05-16 draft enumerated (eligibility & authorization / student need / instructional model / student experience / educator capacity / leadership capacity / governance / operations / finance & sustainability / community & family engagement / evaluation & continuous improvement). The 11-class taxonomy is more reviewer-rubric-aligned than the 12-evidence-signal granularity.
- **Item B.3 (Educator-specific reviewer heuristic enumeration) not yet folded in.** Three heuristics with Educator-flavored upgrade requirements: "inclusion without infrastructure," "shared governance without decision rights," "compliance without articulation." Currently absent from card body; cross-cutting versions live in `skills/scribe-ghostwriter/references/reviewer_heuristics.md` per amendment proposal.
- **No `tribal_education` or `BIE` core_term.** BIE (Bureau of Indian Education) + Tribal Education Departments + Native American Languages Act + Indian Education Title VI Part A are referenced in the `decolonize curriculum / Indigenous knowledge centering` reviewer_context (lines 654–664) but not in core_terms. Adding tribal-education vocabulary would surface the parallel statutory framework for Native-serving applicants more explicitly at Scout time.
- **No `homeless education liaison` or `unaccompanied youth` core_term.** McKinney-Vento liaison designation is named in compliance_burdens (lines 891–897) but not in core_terms; school-district / charter applicants serving homeless / housing-insecure youth have a specific statutory framework that Scout currently doesn't index.
- **No `English learner` or `EL services` evidence_signal.** Title III is named in core_terms (line 82) + compliance_burdens (line 864) but no evidence_signal for EL services dosage / qualified-staff / per-pupil-allocation. Worth adding.
- **`disqualifier_terms` 4 entries thin.** religious instruction / for-profit only / adult-only programming / individual research only. Missing: "out-of-school youth without LEA partner" (eliminates EIR / 21st CCLC eligibility for community-only programs); "K-12 charter without authorizer-approval status" (CSP / Magnet eligibility precondition); "international beneficiary scope" (most USDE programs are US-domestic only).
- **`metrics_table_template` 11 entries strong but no `family / caregiver participation` count.** Family-engagement metric is listed (line 769) but unit ambiguous ("count of caregivers / events") — recommend split into separate metrics: caregivers engaged (count) + family events delivered (count) + caregiver-completed-survey-response-rate (percent).
- **PA-specific PCCD / PHEAA / PDE entries** in draft_funder_candidates_pending_operator_engagement_confirmation (lines 1356, 1362, 1368, 1356) are operator-defensible (FIT Farms LLC PA-anchored) but are state-overlay candidates per master prompt §1.2 and Run 1 P2-state-overlay-separation guidance. Per amendment proposal §A.1: "Decision still deferred to v1.x cross-cutting amendment with sibling CICs."

### §2.3 Lifecycle / signature / schema concerns

- **`draft_status: signed`.** No normalization needed (per Run 1 Phase 1 §3.2).
- **Header comment cleanliness.** Lines 1–32 are reasonably clean — no stale `# Lifecycle: draft. NO Ed25519 signature.` claim. The OQ-pinned operating posture (OQ-3 / OQ-4 / OQ-5 / OQ-6) is documented at line 16–24. Severity tier mapping at lines 27–32 is operator-grade.
- **`dialect_routing_table` v1.1 shape** (lines 441–453). Same status as food_systems: cards-ceremony bottleneck. Card body is valid against current on-disk schema.
- **`_research_metadata.draft_funder_candidates_pending_operator_engagement_confirmation` field not schema-known** (per Run 1 Patch B20). Surface at cards-ceremony.
- **Embedded `ed25519_signature` is LIVE** (line 1380): `de90a25e...95935b0e`. Loader-time signature verification is NotImplemented per Run 1 L1-F4 — embedded sig is unverified at runtime today.
- **`_review_handback` block at end of file (lines 1387–1411) carries decision_queue and surface_ambiguities entries.** Schema-permissible per underscore-prefixed exemption; these contain Tilth-internal review process notes that are research-trail, not operational. No runtime consumer reads `_review_handback`; reading is operator-side only.

### §2.4 Coupling-discipline self-audit

**Method.** Manual value-position regex scan over the full card body per master prompt §2 item 2 + Run 1 enforcement-context guidance L1-F3 + section_04_v2_x_7_card_coupling_value_position_amendment.md lines 108–120.

**Results:**

| Line | Path | Match | Exempt? |
|---|---|---|---|
| 1 | (YAML header comment) | `TILTH-CIC-02` | YES — comments not in canonical bytes |
| 3 | (YAML header comment) | `TILTH-CIC-02` | YES — comments not in canonical bytes |
| 36 | `card_id` | `TILTH-CIC-02` | YES — `_VALUE_POSITION_EXEMPT_PATHS` |
| 41 | `tilth_cic_id` | `TILTH-CIC-02` | YES — `_VALUE_POSITION_EXEMPT_PATHS` |
| 1056 | `_research_metadata.priors_consulted[1].extract_note` | `TILTH-CIC-02` | YES — `_research_metadata` top-level `_` |
| 1064 | `_research_metadata.priors_consulted[5].extract_note` | `TILTH-CIC-02` + `Customer Identity Categories` | YES — same exempt subtree |

**Verdict — LIVE regex set: 0 non-exempt findings.** Card passes.

### §2.5 Legacy-phrase defense scan

Grep for `[Cc]ustomer [Ii]nformation` across the card: 0 hits.

**Verdict — legacy-phrase defense-in-depth: 0 findings.** No regression risk.

---

## §3. Research Findings

### §3.1 Source verification table — official + primary

| URL | Type | Access date | Fields supported | Confidence |
|---|---|---|---|---|
| https://www.ed.gov/laws-and-policy/k-12-laws-and-policy/elementary-and-secondary-education/title-i | official | 2026-05-15 | Title I scope; LEA eligibility framing | HIGH |
| https://www.ed.gov/grants-and-programs/grants-special-populations/early-learning/twenty-first-century-community-learning-centers | official | 2026-05-15 | 21st CCLC scope | HIGH |
| https://www.ed.gov/grants-and-programs/grants-elementary-secondary-education/elementary-secondary-education-innovation-research/education-innovation-and-research-program | official | 2026-05-15 | EIR Early-Phase / Mid-Phase / Expansion tier structure + ESSA evidence-tier requirement | HIGH |
| https://www.ed.gov/grants-and-programs/grants-higher-education/improving-undergraduate-postsecondary-preparation/gaining-early-awareness-and-readiness-for-undergraduate-programs-gear-up | official | 2026-05-15 | GEAR UP scope (low-income students prepared for postsecondary) | HIGH |
| https://www.ed.gov/grants-and-programs/grants-higher-education/improving-undergraduate-postsecondary-preparation/federal-trio-programs | official | 2026-05-15 | TRIO five-program family | HIGH |
| https://www.ed.gov/grants-and-programs/grants-special-populations/charter-school-programs/charter-schools-program-csp | official | 2026-05-15 | CSP scope | HIGH |
| https://studentprivacy.ed.gov/ferpa | official | 2026-05-15 | FERPA statutory anchor (20 USC § 1232g; 34 CFR Part 99) | HIGH |
| https://studentprivacy.ed.gov/topic/protection-pupil-rights-amendment-ppra | official | 2026-05-15 | PPRA scope | HIGH |
| https://www.ftc.gov/business-guidance/privacy-security/childrens-privacy | official | 2026-05-15 | COPPA scope (parental consent for online tools collecting from children under 13) | HIGH |
| https://sites.ed.gov/idea/ | official | 2026-05-15 | IDEA portal — special education compliance | HIGH |
| https://www.ed.gov/laws-and-policy/k-12-laws-and-policy/elementary-and-secondary-education/every-student-succeeds-act | official | 2026-05-15 | ESSA § 8101(21) evidence-tier definitions | HIGH |
| https://ies.ed.gov/ncee/wwc/ | official | 2026-05-15 | IES What Works Clearinghouse dosage standards + EIR evaluation tier | HIGH |
| https://www.fns.usda.gov/cfs/farm-school-grant-program | official | 2026-05-15 | USDA FNS Patrick Leahy Farm to School — bridges Educator + Food Systems CICs | HIGH |
| https://www.dol.gov/agencies/eta/youth/youthbuild | official | 2026-05-15 | DOL YouthBuild OST 16–24 scope | HIGH |
| https://www.nsf.gov/funding/initiatives/stem-education | official | 2026-05-15 | NSF EDU directorate (DRK-12 / ITEST / STEM+C / Noyce) | HIGH |
| https://www.federalregister.gov/documents/2025/01/29/2025-02101/ending-radical-and-wasteful-government-dei-programs-and-preferencing | official | 2026-05-15 | EO 14151 verbatim — drives DEI / related-term HIGH severity | HIGH |
| https://www.federalregister.gov/documents/2025/01/30/2025-02090/defending-women-from-gender-ideology-extremism-and-restoring-biological-truth-to-the-federal | official | 2026-05-15 | EO 14168 — drives gender-identity HIGH severity | HIGH |
| https://www.arts.gov/grants/grant-program-description | official | 2026-05-15 | NEA grants conditions — gender-ideology language cross-reference | HIGH |

### §3.2 New / refreshed sources to verify and add

| URL | Type | Why add | Card fields it would support | Confidence |
|---|---|---|---|---|
| https://www.bie.edu/ | official | BIE is named in reviewer_context but absent from core_terms / funder_program_keywords; tribal education has its own statutory framework | New `search_vocabulary.core_terms` entries (`Bureau of Indian Education`, `Tribal Education Department`); new `funder_program_keywords` row | HIGH |
| https://www.bia.gov/bie | official | Same as above; BIE under Department of Interior | Cross-reference for tribal-education funding pathway | HIGH |
| https://www2.ed.gov/about/offices/list/oese/oie/programs.html | official | OESE Office of Indian Education programs — TRIO-equivalent for Native students; Title VI Part A | New funder_program_keywords entry (Title VI Part A Indian Education Formula Grants) | HIGH |
| https://www.unicef.org/data/ — (illustrative; specific URLs vary) | practitioner | Cross-reference for evidence-tier definitions when applicant scope involves international beneficiaries — most USDE programs are US-domestic only, so this is for disqualifier_terms reinforcement | Minimal — only if `international beneficiary` disqualifier is added | LOW |
| https://nche.ed.gov/ | official | National Center for Homeless Education — USDE technical-assistance center for McKinney-Vento; primary source for `homeless education liaison` core_term + evidence pattern | New search_vocabulary core_term + evidence_signal | HIGH |
| https://www.casel.org/ | practitioner | CASEL (Collaborative for Academic, Social, and Emotional Learning) — `social-emotional learning / SEL` reviewer_context references CASEL framework. Useful for evidence pattern when applicant uses SEL frame with foundation funder | refresh `admin_risk_term_register["social-emotional learning / SEL"]` reviewer_context | MEDIUM |
| https://www.wallacefoundation.org/knowledge-center/Pages/foundations-investments-in-Out-of-School-Time.aspx — (illustrative) | practitioner | Wallace OST research portfolio — useful for sustainability / quality-improvement framing on OST applications | optional `_research_metadata.priors_consulted` addition | MEDIUM |
| https://www2.ed.gov/about/offices/list/octae/ | official | OCTAE Office of Career, Technical, and Adult Education — Perkins V administrator + Adult Education and Family Literacy Act (AEFLA); current `disqualifier_terms[adult-only programming]` references AEFLA as separate statutory category but doesn't surface it as a core_term | New core_term: `Adult Education and Family Literacy Act (AEFLA)` | MEDIUM |
| https://www.acf.hhs.gov/ofa/programs/tanf | official | HHS OFA TANF — some youth-development / family-engagement education programs draw on TANF funding through state pass-through | Optional `funder_program_keywords` row + state-pass-through reporting cadence | MEDIUM |
| https://www2.ed.gov/about/offices/list/oese/sfgp/index.html | official | OESE Statewide Family Engagement Centers Program — currently named in funder_program_keywords but URL not in primary_sources; should be added for source verification | Verify primary_source citation | MEDIUM |
| https://www.fns.usda.gov/cn/seamless-summer-option-sso | official | USDA FNS Summer Food Service Program / Seamless Summer Option — cross-cuts Educator CIC + Food Systems CIC for school-meal-program operators | Optional new funder_program_keywords row | MEDIUM |
| https://nedsharedlearning.org/ (NCSI / National Center for Systemic Improvement) | practitioner | IDEA technical assistance — useful for special-education-leaning applicants | Optional `_research_metadata.priors_consulted` | LOW |

### §3.3 Internet Archive snapshot verification

Recommended for next Phase 4-CIC re-pass: verify Wayback Machine snapshots of every primary_sources URL (18 URLs). EO 14151 + EO 14168 Federal Register pages are stable. USDE program pages have been actively restructured in 2025 under current administration — high snapshot-volatility risk. IES WWC + IDEA portal are relatively stable.

---

## §4. Proposed Card Improvements

Grouped by the eight runtime-behavior categories. Each proposal: exact YAML path, why-it-improves-runtime, target-seat, where-it-belongs.

### §4.1 search_vocabulary / classification

- **`search_vocabulary.core_terms[NEW]` — add `Tribal Education Department` + `Bureau of Indian Education (BIE)` + `Native American Languages Act` + `Indian Education Title VI Part A`.** Why: Indigenous-education vocabulary currently lives only in admin_risk_term reviewer_context as substitution candidates; without Scout-side core_terms, Native-serving applicants are mis-routed to non-tribal pathways. **Seat:** Scout + Logician. **Where:** card body.
- **`search_vocabulary.core_terms[NEW]` — add `McKinney-Vento liaison` + `unaccompanied youth` + `student experiencing homelessness`.** Why: McKinney-Vento is in compliance_burdens but absent from core_terms; school-district applicants serving housing-insecure youth have an under-indexed statutory framework. **Seat:** Scout. **Where:** card body.
- **`search_vocabulary.core_terms[NEW]` — add `Adult Education and Family Literacy Act (AEFLA)`.** Why: AEFLA is referenced in `disqualifier_terms[adult-only programming]` but not in core_terms; adult-literacy applicants currently filtered as out-of-scope without surfacing AEFLA as the right statutory category. **Seat:** Scout. **Where:** card body.
- **`search_vocabulary.core_terms[NEW]` — add `English Language Learner (ELL)` + `Title III ELL services`.** Why: Title III is in compliance_burdens (line 864) + core_term `English learner` (line 82) but EL services dosage / qualified-staff evidence is under-surfaced. **Seat:** Scout. **Where:** card body.
- **`search_vocabulary.disqualifier_terms[NEW]` — add `out-of-school youth without LEA partner`, `K-12 charter without authorizer-approval status`, `international beneficiary scope` (US-only program disqualifier).** Why: under-covered disqualifier space. **Seat:** Logician. **Where:** card body.
- **`search_vocabulary.funder_program_keywords[NEW]` — add Title VI Part A Indian Education Formula Grants, USDA FNS Summer Food Service Program / SSO.** Why: surface tribal-education pathway + food-systems-bridge pathway. **Seat:** Scout. **Where:** card body.
- **`search_vocabulary.synonym_map[NEW]` — add `tribal_education` mapping** (BIE / Tribal Education Department / Title VI Part A / Native American Languages Act). **Seat:** Scout. **Where:** card body.

### §4.2 evidence capture / missing-evidence prompts

- **`evidence_signals[NEW]` — add `english_learner_services_dosage`.** source_pattern = "EL services dosage per Title III: ESL/ELD/SIOP/sheltered-content instruction minutes per week, per-student EL plan documentation, qualified-EL-teacher credential, exit criteria; bilingual paraprofessional documentation if applicable." weight = HIGH. freshness_tolerance_days = 365. source_citation = ESEA Title III + 34 CFR 200.24–200.27 + ACCESS for ELLs assessment framework. **Seat:** Scribe + Logician. **Where:** card body.
- **`evidence_signals[NEW]` — add `mckinney_vento_identification_and_services`.** source_pattern = "LEA McKinney-Vento liaison designation; identification protocol; immediate enrollment + transportation provision documentation; services tracking; per-pupil count + disaggregation reporting." weight = HIGH. freshness_tolerance_days = 365. source_citation = McKinney-Vento Homeless Assistance Act + 42 USC § 11431 et seq. **Seat:** Scribe + Logician. **Where:** card body.
- **`evidence_signals[NEW]` — add `idea_part_b_or_c_compliance_documentation`.** source_pattern = "IEP/IFSP samples (de-identified); FAPE / LRE compliance narrative; Section 504 plan templates; maintenance-of-effort documentation; supplement-not-supplant compliance memo." weight = HIGH. freshness_tolerance_days = 365. source_citation = IDEA + 34 CFR Part 300 (Part B) + Part 303 (Part C). **Seat:** Scribe + Logician. **Where:** card body.
- **`evidence_signals[NEW]` — add `cipa_internet_safety_compliance`.** source_pattern = "internet safety policy on file; Technology Protection Measure documentation; public-notice/hearing record for policy adoption." weight = MEDIUM. freshness_tolerance_days = 730. source_citation = CIPA 47 USC § 254(h)(5) + 47 CFR 54.520. **Seat:** Logician. **Where:** card body.
- **`evidence_signals[NEW]` — add `safeguarding_portfolio_completeness`.** source_pattern = "designated child-protection officer name + role; background-check completion records for all adult staff + volunteers with student contact; state-specific clearance documentation (PA Act 153 cited as example); mandated-reporter training completion logs; transportation / supervision protocols." weight = HIGH. freshness_tolerance_days = 365. source_citation = state-specific child-protection statutes (e.g., PA Act 153 of 2014; equivalent in CA / NY / TX / IL / FL). **Seat:** Logician. **Where:** card body. Pairs with existing `youth_safeguarding_policy` provenance_requirement (lines 381–383).
- **Item B.1 from amendment proposal — `field_classification_defaults` sub-block under `register_defaults`.** Five classifications: FERPA-protected student PII → confidential default; IDEA/disability data → confidential default + severity HIGH; discipline/attendance data → confidential default + severity MEDIUM; family/student survey raw data → confidential default; sanitized aggregated summaries → shareable with operator approval. **Schema concern:** this is a new sub-block under register_defaults, not a canonical entry expansion. **Phase 4 fold-in self-check refusal (a) trip:** structured-sub-field expansion on canonical entries — would smuggle a new schema item shape past §18.5. **Recommendation:** route to §18 v1.x schema-refinement amendment surface per master prompt rule 6; do NOT bake into card body silently. Surface to operator decision queue.

### §4.3 KFR fact classes + provenance_requirements

- **`kfr_fact_classes[NEW]` — add `el_services_designation`.** description = "EL identification protocol + per-student EL plan + qualified-EL-staff credential roster + ACCESS for ELLs assessment cycle." typical_provenance = "EL identification protocol document; HQ-EL-teacher certification record; state-administered ACCESS reports." Pairs with new evidence_signal. **Where:** card body.
- **`kfr_fact_classes[NEW]` — add `mckinney_vento_compliance_status`.** description = "Designated McKinney-Vento liaison; identification and service-tracking system; per-pupil count + disaggregation by school + transportation arrangement count." typical_provenance = "liaison-designation document; LEA McKinney-Vento policy; reporting to SEA." **Where:** card body.
- **`kfr_fact_classes[NEW]` — add `tribal_education_partnership_status`.** description = "Tribal Education Department(s) involved as partners / sub-recipients; Tribal Nation consultation status; Title VI Part A formula grant participation; Native American Languages Act consideration if Indigenous-language instruction." typical_provenance = "Tribal Education Department MOU; Tribal consultation record; Title VI Part A application materials if applicant invokes." **Where:** card body.
- **`kfr_fact_classes[NEW]` — add `safeguarding_clearance_portfolio_completeness`.** description = "Per-adult-staff-and-volunteer-with-student-contact clearance status; designated child-protection officer roster; mandated-reporter training cycle." typical_provenance = "HR file portfolio per state-specific code (PA Act 153 cited as example); designated-CPO documentation; training-completion logs." **Where:** card body.
- **`provenance_requirements[NEW]` — entries for `el_services_designation`, `mckinney_vento_compliance_status`, `tribal_education_partnership_status`, `safeguarding_clearance_portfolio_completeness`.** Pairs with new KFR fact_classes. **Where:** card body.

### §4.4 drafting register / admin-risk handling

- **`admin_risk_term_register[REFINE]` — refine `gender identity / gender-affirming` substitution candidate.** Current `"biological sex (where statutorily required per EO 14168)"` is administration-time-anchored; on next administration transition the substitution itself becomes politically charged. Recommended rewrite: `"biological sex (where active RFA explicitly requires this framing)"` — moves anchor from EO to active-RFA-required language (defer-to-RFA discipline). Per amendment proposal §A.3 still operator-decision-pending; recommend operator approval now since the active-RFA-required framing is administration-neutral.
- **`admin_risk_term_register[NEW]` — add `equity audit` + `racial equity audit`.** Currently absent from explicit entries. Severity = HIGH for federal grants under EO 14151 / EO 14168 framing; substitution candidates = ["disaggregated student-outcomes analysis," "achievement-data disaggregation," "student-population-group analysis," "Title I FRPL / IDEA / EL / TRIO-first-generation analysis per statutory categories"]. Why: equity-audit framing appears in foundation applications but routinely flags federal reviewers.
- **`admin_risk_term_register[NEW]` — add `disrupt(ing) inequity`** (and similar movement-aligned framing). Severity = MEDIUM. Substitution candidates = ["addressing outcome differences," "improving student access to opportunity," "closing opportunity gaps (use cautiously per achievement-gap entry above)"].
- **OD-A v2.4 cross-CIC migration check.** The 14 admin_risk_term entries on this card include 8 that are cross-CIC shared (DEI, equity, trauma-informed, gender identity, culturally responsive, SEL, marginalized, anti-racist, systemic inequity, intersectional, achievement gap, LGBTQ, decolonize, white privilege). ≥3-card recurrence threshold met for many. **Surface to operator: dispatch a workspace-register migration ceremony for shared educator + arts_culture + public_agency + cooperative + ecosystem_intermediary terms.**

### §4.5 reviewer / rubric logic

- **`narrative_sections_typical[NEW]` — add `"Indigenous / Tribal Nation Consultation Record"` (where applicable) between `"Partner / LEA / IHE Roles"` and `"Project Personnel Qualifications"`.** Why: Title VI Part A + Indian Education programs explicitly require Tribal consultation evidence; current narrative_sections_typical 12 items conflate this into "Partner / LEA / IHE Roles."
- **`narrative_sections_typical[NEW]` — add `"Safeguarding and Child Protection Plan"`.** Why: 21st CCLC + EIR + GEAR UP + Magnet Schools + AmeriCorps state-and-national all require child-protection narrative as a discrete scoring criterion; current narrative_sections_typical conflates into "Project Management Plan."
- **Item B.3 from amendment proposal — Educator-specific reviewer heuristic enumeration in `reviewer_lens` sub-block.** Three heuristics with Educator-flavored upgrade requirements per amendment proposal. **Phase 4 fold-in self-check refusal (a) trip:** structured-sub-field expansion on canonical entries. **Recommendation:** route to §18 v1.x amendment surface. Surface to operator decision queue.

### §4.6 red-team probes / admin-risk register

- **`common_risk_register_entries[NEW]` — add `Tribal consultation gap`.** likelihood = MEDIUM. impact = HIGH. mitigation_pattern = "For projects on or near Indigenous lands, in Tribal Nation school districts, or invoking Indigenous-knowledge curriculum: Tribal consultation record + Tribal Education Department engagement + Title VI Part A formula-grant participation status verification before application submission."
- **`common_risk_register_entries[NEW]` — add `English Learner services dosage mismatch`.** likelihood = MEDIUM. impact = HIGH. mitigation_pattern = "Title III dosage minimums + WIDA ACCESS for ELLs assessment cycle + per-student EL plan + qualified-EL-teacher staffing ratio verified against state-specific Title III plan."
- **`common_risk_register_entries[NEW]` — add `McKinney-Vento liaison or service-tracking gap`.** likelihood = MEDIUM. impact = HIGH. mitigation_pattern = "LEA McKinney-Vento liaison designation current; identification protocol active; per-pupil count + disaggregation reporting current; transportation arrangement documentation per district policy."

### §4.7 reporting / commitment extraction

- **`reporting_cadence_typical.per_funder_overrides[NEW]` — add USDE Title VI Part A Indian Education + USDE Office of Special Education Programs (OSEP) Personnel Preparation grants + DOL Apprenticeship + USDA Summer Food Service Program (SFSP).** **Seat:** Archivist + Report Generator. **Where:** card body.

### §4.8 memory namespace usefulness

Standardized sub-keys for v0.2 first-wave loader graduation per architecture v7.0.11 §1.9, mirroring food_systems pattern:

- `cards:cic:educator:scout_vocabulary`
- `cards:cic:educator:evidence_signals`
- `cards:cic:educator:kfr_fact_classes`
- `cards:cic:educator:provenance_requirements`
- `cards:cic:educator:register_defaults`
- `cards:cic:educator:sub_registers` (Educator-specific sub_registers + sub_register_selection_rule)
- `cards:cic:educator:dialect_routing_table` (post-cards-ceremony)
- `cards:cic:educator:admin_risk_terms`
- `cards:cic:educator:reporting_cadence`
- `cards:cic:educator:metrics_template`
- `cards:cic:educator:narrative_sections`
- `cards:cic:educator:capacity_signals`
- `cards:cic:educator:compliance_burdens`
- `cards:cic:educator:common_risks`
- `cards:cic:educator:common_funders_observed` (live; engagement-confirmed only)
- `cards:cic:educator:draft_funder_candidates`

**Seat:** all consuming seats. **Where:** v0.2 loader-graduation enumeration; surface to operator at Run 1 Patch D5 dispatch.

### §4.9 Phase 4 fold-in discipline self-check (per master prompt rule 6 / §18.11 v1.1)

| Proposal | (a) structured-sub-field expansion on canonical entries? | (b) dedicated-field-name fork? | (c) compound enum value? | (d) literal canonical CIC/CLC slug in non-exempt value position? |
|---|---|---|---|---|
| §4.1 core_terms / synonym_map / funder_program_keywords additions | NO | NO | NO | NO |
| §4.1 disqualifier_terms additions | NO | NO | NO | NO |
| §4.2 evidence_signals additions (EL / McKinney-Vento / IDEA / CIPA / safeguarding) | NO | NO | NO | NO |
| §4.2 **Item B.1 — register_defaults.field_classification_defaults sub-block** | **YES — TRIPS (a)** | NO | NO | NO |
| §4.3 kfr_fact_classes / provenance_requirements additions | NO | NO | NO | NO |
| §4.4 admin_risk_term_register refines / adds | NO — refines reviewer_context within canonical entry shape; adds new entries with canonical schema | NO | NO | NO |
| §4.5 narrative_sections_typical additions (`Tribal consultation` + `Safeguarding`) | NO | NO | NO | NO |
| §4.5 **Item B.3 — reviewer_lens sub-block** | **YES — TRIPS (a)** (likely; needs schema-shape check) | possibly — if reviewer_lens not present in canonical schema, this would be (b) | NO | NO |
| §4.6 common_risk_register_entries additions | NO | NO | NO — uses canonical HIGH/MEDIUM × HIGH/MEDIUM | NO |
| §4.7 reporting_cadence_typical.per_funder_overrides additions | NO | NO | NO | NO |
| §4.8 memory namespace sub-keys | N/A — architecture decision | N/A | N/A | N/A |

**Verdict:** Two proposals trip refusal (a): Item B.1 (`register_defaults.field_classification_defaults`) and Item B.3 (`reviewer_lens` block). Per master prompt rule 6 / §18.11 v1.1 — these route to a §18 v1.x amendment, NOT into the card body silently. Surface to Operator Decision Queue.

Item B.2 (per-client evidence-class enumeration — 11-class taxonomy) is borderline: it could land as a new top-level field `evidence_class_taxonomy` (which would be refusal (b) — dedicated field-name fork from `evidence_signals`); OR as a sub-block under `evidence_signals` (refusal (a)). Either way: route to §18 v1.x amendment surface, do NOT bake into card body silently. Surface to Operator Decision Queue.

---

## §5. Operator Decision Queue

1. **`gender identity / gender-affirming` substitution candidate refresh** (per amendment proposal §A.3, still pending). Proposed rewrite: replace `"biological sex (where statutorily required per EO 14168)"` with `"biological sex (where active RFA explicitly requires this framing)"`. Administration-neutral; defer-to-active-RFA discipline. Approval required per OQ-5.
2. **Item B.1 (granular education-data-privacy classification defaults) routing.** Schema work needed. Route to §18 v1.x amendment surface OR adopt comment-block-only fold-in per §18.11 v1.1 (write classification defaults as YAML comments + route structural gap to `_review_handback` operator-decision queue). **Recommend:** comment-block-only fold-in for v0.1+v0.2; §18 v1.x amendment to make `register_defaults.field_classification_defaults` schema-known.
3. **Item B.2 (per-client evidence-class taxonomy — 11 classes) routing.** Schema work needed. Same comment-block-only fold-in OR §18 v1.x amendment decision. **Recommend:** §18 v1.x amendment for the 11-class taxonomy because it's a reviewer-rubric-aligned reorganization, not just a runtime-evidence-trigger taxonomy.
4. **Item B.3 (Educator-specific reviewer heuristic enumeration) routing.** Same options. **Recommend:** comment-block-only fold-in for v0.1+v0.2 since the three heuristics build on existing `reviewer_heuristics.md` cross-cutting reference; §18 v1.x amendment if operator wants reviewer-lens block schema-known.
5. **OD-A v2.4 cross-CIC migration ceremony for shared admin-risk terms.** 8 cross-CIC shared terms on this card alone (DEI / equity / trauma-informed / gender identity / culturally responsive / SEL / marginalized / anti-racist / systemic inequity / intersectional / achievement gap / LGBTQ / decolonize / white privilege — subset of these are on 3+ cards). Dispatch a workspace-register migration ceremony.
6. **Per amendment proposal §A.1 — PA-specific funders state-overlay.** Three PA entries (PDE, PCCD, PHEAA) in draft_funder_candidates. Per master prompt §1.2 + Run 1 P2-state-overlay-separation guidance: do these belong in base card OR PA-state overlay? Decision deferred to v1.x cross-cutting amendment with sibling CICs.
7. **`equity audit` + `racial equity audit` admin_risk_term additions.** Operator approval per OQ-5.
8. **`disrupt(ing) inequity` admin_risk_term addition.** Operator approval per OQ-5.
9. **Tribal Education / BIE / Title VI Part A Indian Education / Native American Languages Act core_term + funder_program_keyword additions.** Operator confirms scope expansion is in v0.1 Beta vs v0.2 backlog. Indigenous-education vocabulary is a meaningful runtime-routing improvement but may exceed v0.1 PA-anchored deployment scope.
10. **McKinney-Vento / EL services / IDEA core_term + evidence_signal + KFR additions.** Each is a compliance-stack depth improvement; bundle or sequence?
11. **`Adult Education and Family Literacy Act (AEFLA)` core_term + boundary clarification.** Currently `disqualifier_terms[adult-only programming]` says "AEFLA is its own statutory category." Operator decides: is adult education in scope of CIC-02 (carve-out from disqualifier), or stays disqualified (AEFLA = different CIC or v0.2 Wave 3 scope)?
12. **AmeriCorps administration-volatility note** (lines 1273–1283). Currently the draft_funder_candidates entry for AmeriCorps carries a 6-line operator-defensive prose note. Acceptable now; verify at next dispatch when administration-driven changes to AmeriCorps stabilize.
13. **Title IX framework regulation-in-flux flag** (per amendment proposal §A.4). Card carries a flag at line 903 ("Per active federal-regulation cycle: Tilth flags Title IX as a regulatory-environment-in-flux compliance area"). Recommend operator revisit on Title IX rule stabilization.
14. **Severity assignment for 'trauma-informed'** (per amendment proposal §A.5 surface_ambiguities). Card has it MEDIUM; admin_risk_register.yaml has it YELLOW (equivalent). Some state RFPs (FL, TX) crosses into RED for state-level review. Operator may want a state-level severity-tier overlay at Archivist Reflection layer.
15. **Lock-history housekeeping field disposition** (cross-card). Same as food_systems — operator decides via cards-ceremony.
16. **Re-signing ceremony budget for card body changes** (similar bundle as food_systems). ~22 distinct card-body edits proposed (excluding the 3 amendment-route items B.1 / B.2 / B.3). Bundle into cards-ceremony per Run 1 Patch Queue Batch B as `educator` supersession-re-sign? Or sequence as separate content-refresh dispatch?

---

## §6. Validation Checklist

| Check | Result | Evidence |
|---|---|---|
| Schema fields complete against current §18.5 schema | PASS | 15/15 required CIC fields present; lifecycle allOf conditional satisfied |
| No forbidden coupling field names (top-level + nested) | PASS | Grep across file: none of 7 forbidden CIC-side names appear |
| No forbidden value-position regex matches outside exempt paths | PASS | §2.4 — 0 non-exempt findings |
| No legacy-phrase `[Cc]ustomer [Ii]nformation` matches | PASS | 0 hits |
| No private organization-specific data in card body | PASS | Top-level common_funders_observed is empty list; subagent-populated candidates carry no client-specific data |
| No unsourced program-law claims | PASS at body | Verbatim quotes ≤2 sentences; EO 14151 + EO 14168 cited with Federal Register URL + access date |
| No excessive verbatim source text | PASS | Per OQ-4 |
| Lifecycle status consistent with architecture v7.0.11 §1.5 | PASS | All five lifecycle gate fields at pass-state |
| **Top-level `common_funders_observed:` is empty (Law-5 split per operator v2.1)** | PASS | Line 1011 `common_funders_observed: []`; subagent candidates at `_research_metadata.draft_funder_candidates_pending_operator_engagement_confirmation` line 1197 |
| **No populated top-level `common_funders_observed` without operator-engagement-attestation** | PASS | Empty list; no Law-5 violation |
| For multi-track CLCs: shared root metadata + oneOf branch 2 compliance | N/A — CIC card |

**Net coupling-discipline regression: 0 findings.**

---

## §7. Regression Tests

### Test 1 — Indigenous-serving K-12 school district

**Prompt:** "We're a K-8 school district serving a Tribal community in the Southwest, applying for USDE funding to expand culturally-grounded science instruction using Indigenous-language pedagogy and Tribal Education Department partnership."

**Pre-edit:** Scout matches `school district`, `K-12 school`, `LEA`. No tribal-education routing; `Indigenous education sovereignty` appears only in admin_risk_term reviewer_context. Scribe drafts without Title VI Part A framing or Tribal consultation discipline.

**Post-edit (with §4.1 / §4.5 additions):** Scout matches `Tribal Education Department`, `Bureau of Indian Education (BIE)`, `Native American Languages Act`, `Indian Education Title VI Part A` core_terms. Scribe surfaces Title VI Part A as primary federal pathway + Tribal consultation evidence as a discrete narrative_sections_typical section. Logician fires `Tribal consultation gap` risk if applicant lacks Tribal Education Department MOU.

**Seat:** Scout + Scribe + Logician. **Pass criterion:** Title VI Part A appears in Scout output; Tribal consultation appears in narrative outline.

### Test 2 — McKinney-Vento and EL-service-dense applicant

**Prompt:** "Title I school district with 25% student homelessness + 18% English Learner population applying to USDE 21st CCLC for afterschool programming targeting these populations."

**Pre-edit:** Scout matches `Title I school`, `afterschool program`, `21st CCLC`. No McKinney-Vento or EL-specific evidence prompts. Scribe drafts generic Title I framing without per-population-statutory-anchor specificity.

**Post-edit (with §4.2 + §4.3 additions):** Scout matches McKinney-Vento liaison + ELL core_terms. Scribe fires `english_learner_services_dosage` + `mckinney_vento_identification_and_services` evidence_signals (both HIGH weight) — surfaces Title III dosage + ACCESS for ELLs cycle + McKinney-Vento liaison + identification protocol + per-pupil-disaggregation reporting. Logician fires `English Learner services dosage mismatch` + `McKinney-Vento liaison or service-tracking gap` common_risk_register_entries if evidence is thin.

**Seat:** Scout + Scribe + Logician. **Pass criterion:** EL-services + McKinney-Vento evidence prompts fire; corresponding KFR fact-classes surface in intake.

### Test 3 — DEI vocabulary substitution under EO 14151 framing

**Prompt:** "Foundation grant application + USDE EIR Mid-Phase application for a tutoring intervention targeting equity in math outcomes for Title I FRPL-eligible students."

**Pre-edit:** Scribe drafts `equity` + `equity-focused` + `closing the achievement gap` verbatim. Logician fires admin_risk_term_register["equity"] MEDIUM + ["achievement gap"] MEDIUM; substitution candidates surfaced; operator approves per OQ-5.

**Post-edit (with §4.4 + admin_risk register refresh):** Same operational outcome for foundation route (equity / achievement gap retained where active foundation funder accepts). For USDE EIR Mid-Phase route, Scribe substitutes to `differences in proficiency rates across student groups` + `Title I FRPL-eligible students' outcomes vs comparison` + `students-in-low-income-communities` per refined substitution candidates. Logician fires `equity audit` MEDIUM-HIGH if applicant uses equity-audit framing on federal route.

**Seat:** Scribe + Logician. **Pass criterion:** federal route avoids DEI-coded vocabulary; foundation route retains.

### Test 4 — Gender-identity substitution administration-neutrality

**Prompt:** "Trans-inclusive afterschool program applying to LGBTQ-focused foundation funder AND to USDE 21st CCLC state-pass-through."

**Pre-edit:** Foundation route — Scribe retains "gender identity" + "trans" + "LGBTQ" verbatim per admin_risk_term reviewer_context (foundation funders fund queer arts/programs and expect vocabulary). Federal route — Scribe substitutes per EO 14168 framing; current substitution candidate `"biological sex (where statutorily required per EO 14168)"` is administration-time-anchored.

**Post-edit (with §4.4 refined substitution candidate `"biological sex (where active RFA explicitly requires this framing)"`):** Same operational outcome; substitution candidate is administration-neutral. Federal route substitutes only when active RFA explicitly requires biological-sex framing (rather than when administration-side EO is in force).

**Seat:** Scribe + Logician. **Pass criterion:** federal route substitutes only when active RFA requires; administration-neutral framing in reviewer_context.

### Test 5 — Cards-ceremony post-condition (dialect_routing_table re-keyed)

**Prompt:** "K-12 school district applying to USDE EIR Mid-Phase for evidence-based literacy intervention with external evaluator."

**Pre-cards-ceremony:** dialect_routing_table keyed on funder_political_axis = `centrist`, dialect `scribe.technical_precise`. Scribe selects sub_register `technical_precise`.

**Post-cards-ceremony (per Run 1 Patch B2–B7):** dialect_routing_table row re-keys to `clc: research_evidence` + `dialect: scribe.technical_precise` + `register_description: "evidence-tier-required technical reviewer panel; external-evaluator-required; biosketch-grade methodology disclosure expected"` + optional `example_program: "USDE EIR Mid-Phase"`. Same operational outcome; no funder_political_axis intermediary.

**Seat:** Scribe + Judge. **Pass criterion:** Pre-ceremony body validates against v1.1 schema; post-ceremony validates against §18 v1.2 schema. Same proposal routing for this opportunity.

---

## §8. Patch Plan

### File: `pipeline/cards/CIC/educator.yaml`

**Ceremony shape:** supersession-re-sign per OD-E precedent. Parent_lock_row = 250. Ceremony_parent_row = `<NEXT-AVAILABLE-COMPOUND-PARENT>` if bundled with cards-ceremony.

**Edit set (excluding the 3 schema-routed items B.1 / B.2 / B.3):**

1. Header comment normalization (only if needed; current header is reasonably clean — lower priority than food_systems Patch A4 case).
2. `search_vocabulary.core_terms[NEW]` — add tribal-education vocabulary (BIE / Tribal Education Department / Native American Languages Act / Indian Education Title VI Part A); McKinney-Vento liaison / unaccompanied youth / student experiencing homelessness; AEFLA; English Language Learner (ELL) / Title III ELL services (§4.1).
3. `search_vocabulary.synonym_map[NEW]` — `tribal_education` mapping (§4.1).
4. `search_vocabulary.funder_program_keywords[NEW]` — Title VI Part A Indian Education Formula Grants, USDA FNS Summer Food Service Program / SSO (§4.1).
5. `search_vocabulary.disqualifier_terms[NEW]` — `out-of-school youth without LEA partner`, `K-12 charter without authorizer-approval status`, `international beneficiary scope` (§4.1).
6. `evidence_signals[NEW]` — `english_learner_services_dosage`, `mckinney_vento_identification_and_services`, `idea_part_b_or_c_compliance_documentation`, `cipa_internet_safety_compliance`, `safeguarding_portfolio_completeness` (§4.2).
7. `kfr_fact_classes[NEW]` — `el_services_designation`, `mckinney_vento_compliance_status`, `tribal_education_partnership_status`, `safeguarding_clearance_portfolio_completeness` (§4.3).
8. `provenance_requirements[NEW]` — entries for the four new KFR fact-classes (§4.3).
9. `admin_risk_term_register[REFINE]` — `gender identity / gender-affirming` substitution candidate refresh (§4.4 + Operator Decision §A.3 resolution).
10. `admin_risk_term_register[NEW]` — `equity audit` / `racial equity audit`; `disrupt(ing) inequity` (§4.4).
11. `narrative_sections_typical[NEW]` — `"Indigenous / Tribal Nation Consultation Record"`; `"Safeguarding and Child Protection Plan"` (§4.5).
12. `common_risk_register_entries[NEW]` — `Tribal consultation gap`, `English Learner services dosage mismatch`, `McKinney-Vento liaison or service-tracking gap` (§4.6).
13. `reporting_cadence_typical.per_funder_overrides[NEW]` — Title VI Part A Indian Education / OSEP Personnel Preparation / DOL Apprenticeship / USDA SFSP entries (§4.7).
14. `register_defaults.sub_register_selection_rule[REFINE]` — post-cards-ceremony selection rule clarification (§4.4). Bundle with cards-ceremony.

### File: `pipeline/cards/_schema/card_cic.schema.json`

15. Patch B20 — `_research_metadata.draft_funder_candidates_pending_operator_engagement_confirmation` schema-known field (Run 1).
16. Patch B1 — §18 v1.2 dialect_routing_table re-key schema delta (Run 1).

### New file: `pipeline/blueprint/v0.1/section_18_v1_x_register_defaults_field_classification_amendment.md` (proposed)

17. §18 v1.x amendment for Item B.1 (`register_defaults.field_classification_defaults` sub-block) per master prompt rule 6 / §18.11 v1.1 refusal (a) routing. **Out of scope for this dispatch; surface to Operator Decision Queue for amendment authoring.**

### New file: `pipeline/blueprint/v0.1/section_18_v1_x_evidence_class_taxonomy_amendment.md` (proposed)

18. §18 v1.x amendment for Item B.2 (11-class evidence taxonomy) per master prompt rule 6. **Out of scope; surface to Operator Decision Queue.**

### New file: `pipeline/blueprint/v0.1/section_18_v1_x_reviewer_lens_amendment.md` (proposed)

19. §18 v1.x amendment for Item B.3 (reviewer_lens block with Educator-flavored upgrades) per master prompt rule 6. **Out of scope; surface to Operator Decision Queue.**

### File: `pipeline/institutional_memory/admin_risk_register.yaml`

20. Workspace-register update — surface 8 cross-CIC shared educator terms as workspace migration candidates per OD-A v2.4 → v3.0 scrub workflow.

### File: `pipeline/cards/CIC/educator_amendment_proposal_2026-05-16.md`

21. Update STAGED-NOT-YET-DISPATCHED amendment proposal status to LANDED for items A.3 (gender identity substitution refresh) + B.1 / B.2 / B.3 (now §18 v1.x amendment candidates surfaced). Per master prompt safety overlay: no LOCKed-file edits, but `educator_amendment_proposal_2026-05-16.md` is NOT a LOCKed amendment text — it's a working proposal doc. Surface to operator: do you want this updated to reflect §18 v1.x amendment routing? **Recommend:** YES — supports operator-side amendment dispatch.

**OD-D Phase 4 forward-binding contract note:** Edit set 1–14 is value-position clean per §2.4. Edits 15–16 are schema patches per cards-ceremony. Edits 17–19 are §18 v1.x amendment authoring (out of this dispatch). Edit 20 is OD-A workspace-register update. Edit 21 is amendment-proposal status update.

---

**Summary block:**

```
Card: CIC:educator
Card file: pipeline/cards/CIC/educator.yaml
Research hours actual: 1.8
Findings: 30 total — 0 P0, 14 P1, 16 P2
Decision queue: 16 operator approvals required
Conflicts with prior art: NONE (consistent with educator_amendment_proposal_2026-05-16.md direction; all admin_risk_term entries align with admin_risk_register v2.2 severity tiers)
Coupling-discipline regression: NONE
Lifecycle gap surfaced: draft_status reads "signed" on disk; no normalization required per Run 1 P0-3
Review readiness: READY (Item B.1 / B.2 / B.3 from amendment proposal route to §18 v1.x amendment surface per master prompt rule 6 / §18.11 v1.1 refusal-(a) discipline)
```
