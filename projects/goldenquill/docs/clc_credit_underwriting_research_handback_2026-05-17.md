# Research Handback — CLC:credit_underwriting

Prepared: 2026-05-17
Card file: `pipeline/cards/CLC/credit_underwriting.yaml`
Schema: `pipeline/cards/_schema/card_clc.schema.json`
Axis: CLC | card_id: TILTH-CLC-06 | slug: `credit_underwriting` | display name: Credit & Underwriting
Track shape declared in dispatch: multi-track per §18.6 v2 OD-E LOCK row 274 — **OPERATOR DIRECTIVE: Track B is a MINIMAL-STUB per L-024 (master prompt §6 lines 422–430).**
Track shape on disk: **single-track legacy shape** (no `track_a:` / `track_b:` / `_partition_provenance:` keys present). §18.6 v2 LOCKed-but-not-applied per Run 1 §3.2 + L2-F1. The card body still mixes debt + grant framing inside a single-track structure with the load-bearing CRITICAL FRAMING header at lines 14–22 carrying the L-024 distinction in prose form.
Research hours actual: 2.9
Conflicts with prior art: NONE
Coupling-discipline regression scan: NONE (recursive value-position scan against the four LIVE regex patterns under the non-exempt path tree yielded zero matches; the canonical-token references that exist are all under `_research_metadata` and the self-identifying `card_id` / `tilth_clc_id` paths — exempt per §2.2 of `section_04_v2_x_7_card_coupling_value_position_amendment.md`).
Forbidden-field-registry scan (CLC-side six names): NONE present at root or nested in items.
Law-5 status: NOT-SPLIT — flagged terms register was removed from card body at Wave 2 Cycle 2 fix-in-place (lines 749–765 comment block); the 13 CLC-06-scoped terms still pending workspace migration to `pipeline/institutional_memory/admin_risk_register.yaml` v2.4 per OD-A pattern. Migration confirmation needed for operator decision queue (OD-A handback at `pipeline/handoffs/od_a_completion_2026-05-16.md` reports 60 net-new terms migrated workspace-wide; per-CLC-06 cell completion unverified).

---

## §1 — Card Impact Thesis

### §1.A — Track A (debt) — IN SCOPE FOR RESEARCH

Track A — debt — is the load-bearing scope for CLC-06. The card should cause Tilth to read every CDFI / SBA / USDA RD / conventional-bank / SSBCI opportunity as a **commercial credit underwriting transaction** — not a grant proposal — and to surface debt-side primitives at every seat: Intake classifies the funding instrument as debt | guarantee | revolving-fund | TA-bundled; Scout VERIFY confirms repayment-source structure at the funder portal before promoting candidates; Scribe enters credit-memo register (precise, financial, conservative) and refuses grant-narrative drafting under this CLC; Judge applies a 5C / SBA SOP 50 10 / USDA RD 7 CFR 5001 / CDFI mission-plus-credit dual-lens scoring frame; Red Team probes against weak DSCR, unsupported pro forma, hidden debt, commingled finances, owner-equity-injection sourcing, and post-COVID balance-sheet residuals; Logician fail-closes on debt-as-grant misframing, ineligible use-of-funds categories, and missing personal-guarantor / spousal-signature ECOA compliance; Archivist accumulates lender-specific underwriting overlays into Lessons Memory as cycles complete. The card holds the load-bearing applicant-side commitment: **the funding mechanism is repayment-anchored — every dollar pays back, no exceptions; mission alignment supplements credit but does not replace it.**

### §1.B — Track B (grant) — MINIMAL-STUB PER L-024 OPERATOR DIRECTIVE

Track B is **not the right home for grant-side capital-readiness logic** per operator directive 2026-05-17 (OD-E row 277 + L-024 lesson). The verbatim operator rationale: grant logic and credit underwriting logic are objectively different mechanisms even though both are financial-access tools; the stacked-funding use case (VAPG + low-interest farm loan + tourism grant + small business loan + small business advantage grant) requires separate logic per funding type. A separate CLC for grant-side credit-readiness or grant-side capital matching belongs in v0.2 Wave 3, not as Track B of `credit_underwriting`. Track B must therefore document this position as a minimal-stub with a `_partition_provenance.domain_clarification` block carrying the verbatim L-024 rationale, and route substantive Track B research to a v0.2 Wave 3 backlog item (provisional slug: `grant_side_credit_readiness` or `capital_readiness_grant`; final naming pending Wave 3 dispatch). **This handback proposes zero substantive Track B content per binding operator directive.** Track B's runtime effect: when a Tilth seat surfaces an opportunity that looks like grant-side capital-readiness, the operator-decision-at-draft surface should recommend "route to v0.2 Wave 3 grant-side-credit-readiness CLC when it exists; fall back to minimal-stub for v0.1."

---

## §2 — Current State Audit

### §2.A — Track A audit (debt)

#### What is strong now

- **CRITICAL FRAMING header (lines 14–22)** explicitly names the debt-vs-grant boundary and pre-stages Cycle 1 F-02 fold-in runtime expectation (Intake classify funding instrument; Scout VERIFY surface; Scribe refuse grant-narrative under CLC-06). This is the load-bearing L-024 lesson rendered in prose; carries the operative effect even before the multi-track shape graduates.
- **`underwriting_criteria` (13 entries)** covers the canonical commercial-credit surface: repayment capacity, cash flow, DSCR, collateral, credit history, owner equity, management capacity, financial controls, use of funds, risk mitigation, guarantor strength, covenant compliance, community impact for mission lenders. The DSCR criterion (lines 63–66) carries qualified numeric bands (≥1.20–1.25x typical; ~1.15x SBA 7(a) global; 1.10–1.15x CDFI mission) with explicit author-judgment-not-regulatory-floor caveat.
- **`scoring_weight_patterns` (4 rubric examples)** captures 5C / SBA 7(a) SOP / USDA RD B&I / CDFI mission underwriting weight patterns at qualitative tier per OQ-6.
- **`evidence_weights` (13 entries)** covers financial statements, tax returns, pro forma, debt schedule, collateral docs, credit explanation letters, contracts as repayment source, owner-equity-injection docs, management resumes, insurance, use-of-funds budget, business plan, community-impact docs. Strongest evidence block among CLC cards.
- **`common_application_forms` (11 forms)** enumerates SBA Forms 1919 / 413 / 912 / 1920, USDA RD Forms 4279-1 / 442-7 / IRP, CDFI lender portals, state RLF apps, SSBCI applications, FDIC bank application reference.
- **`common_portals` (11 entries)** covers SBA Lender Match / E-Tran, USDA RD Apply, OFN CDFI Locator, CDFI Fund Awards Database, individual CDFI portals, CDFA Online Resource Database, Treasury SSBCI page, SBDC, SCORE, SAM.gov — the complete debt-discovery surface.
- **`common_red_flags` (17 entries)** includes the OD-flagged probes: weak DSCR, unsupported pro forma, no clear repayment source, poor financial controls, unclear collateral, missing equity injection, commingled finances, tax-vs-statement mismatch, weak management bench, hidden UCC liens, max-leverage refinance, COVID-era residual liabilities (upgraded HIGH per Wave 2 Cycle 1 F-08), single-buyer concentration, ineligible use of funds, collateral-over-reliance (MEDIUM), and `treating_debt_as_grant_in_application_framing` (HIGH — the L-024 runtime backstop). The COVID-era liability flag is the strongest in-market signal among CLC cards.
- **`reviewer_profile_typical`** covers 10 reviewer types + 8 reviewer-priority questions in the operative order ("where does the cash come from to service this debt?" load-bearing first).
- **`compliance_obligations` (10 frameworks)** covers loan agreement covenants, SBA SOP 50 10, USDA RD 7 CFR 5001 / 4274 Subpart D, FFIEC, CDFI Fund, ECOA / Reg B, FHA + fair lending, USA PATRIOT / BSA, environmental Phase I/II, state usury, UCC filing maintenance.
- **`commitment_tracking_pattern` (18 commitment types)** is the deepest Report Generator feed across CLC cards; covers DSCR / leverage / current-ratio testing, debt service payments, covenant compliance, collateral status across multiple dimensions (insurance / valuation / condition), jobs created/retained, use-of-funds documentation.
- **`_research_metadata.primary_sources` (17 unique URLs)** — predominantly official / primary (SBA.gov, Treasury CDFI Fund, USDA RD, OFN, CDFA, Treasury SSBCI, FDIC, CFPB, ConsumerFinance.gov Reg B), one practitioner (Investopedia for the 5C heuristic), and one inter-departmental reference (uniformlaws.org).

#### What is stale, ambiguous, over-broad, too local, too federal, or under-sourced

- **Investopedia 5C source citation** (`scoring_weight_patterns[0].source_citation` line 136 + primary_sources entry line 880) is the non-primary in the source set. Per master prompt §6 L-024 dispatch instruction "Avoid Investopedia-style materials where official lender guidance exists." The 5C heuristic is universal but the canonical source authority is FDIC / OCC / SBA SOP / Federal Reserve Bank publications, not Investopedia. Recommend replacing with FDIC Risk Management Manual of Examination Policies §3 (Loans) or OCC Comptroller's Handbook (Commercial Real Estate Lending / Commercial Lending booklets) as the primary source for the 5C framework. Investopedia may stay only as a tertiary reference. (**P0 per L-024 dispatch directive**)
- **SBA SOP 50 10 edition drift** — the SOP-edition qualifier (lines 34–39) is a good defense but the on-disk source URL `https://www.sba.gov/document/sop-50-10-lender-development-company-loan-programs` has historically been re-anchored at each SOP revision. Per OD-E precedent + L-024 dispatch instruction "Strengthen evidence prompts; clarify where Program Rule Packs own lender-specific eligibility": the card should explicitly defer SOP-edition specifics (equity injection percentages, credit-score thresholds, eligibility-screen tests) to the Program Rule Pack layer, with the card itself carrying only the durable framework. (P1)
- **USDA RD 7 CFR consolidation reference** — card cites 7 CFR Part 5001 (consolidated 2024) but legacy materials still reference 7 CFR 4279 / 4280. Crosswalk note exists in `_review_handback.surface_ambiguities[2]` but the runtime crosswalk discipline is not encoded in the card body — Scout / Scribe could miss-route an opportunity citing legacy 4279 / 4280 against the new card. (P2)
- **DSCR target ranges** — bands of 1.20–1.25x typical commercial; 1.15x SBA 7(a) global; 1.10–1.15x CDFI mission are widely-cited industry norms but specific lender policies vary. Per master prompt §6 + §18.16 implementation-phase mapping, these specific bands belong at Program Rule Pack layer or per-CDFI overlay (forward-compat at v0.2). Card body should retain the qualitative framework + caveat; numeric bands should be footnoted as "modal practice, not regulatory floor" (which the card already does at line 64) — consider strengthening the disclaimer further. (P2)
- **CDFI underwriting variation** — card treats CDFI mission-plus-credit as a single composite. In reality Capital Impact Partners / RSF Social Finance / Shared Capital Cooperative / Self-Help / Reinvestment Fund / NCB Capital Impact each publish their own board-approved credit policies. The `_review_handback.decision_queue[8]` flags INDIVIDUAL CDFI VARIATION as a v0.2 overlay candidate — appropriate routing. (P2 — defer to v0.2 per master prompt §18.16)
- **HELOC-as-equity-injection treatment** (criterion `owner_equity` line 79) carries a nuanced statement: HELOC generally excluded as borrowed equity, exception permitted when lender documents full secured + non-dependent repayment. Accurate per SBA SOP language but the conditional is intricate and could trip Logician's PRE-flight check against equity-injection sourcing. Recommend explicit Logician gate spec at v0.2 (`R-CREDIT-EQUITY-HELOC-DISCLOSURE`) requiring the borrower to disclose HELOC sourcing and the lender's secured-and-non-dependent finding before equity injection counts. (P2)
- **No explicit USDA FSA Farm Loan Programs reference** — card focuses on USDA RD B&I / CF / IRP but USDA FSA debt programs route to a different USDA agency (FSA, not RD) with separate regulations (7 CFR Subchapter A) and Borrower's Toolkit. Per L-024 stacked-funding use case (VAPG + low-interest farm loan), the farm-loan reference is operator-relevant. (**P1** — add to `common_application_forms` and `common_portals` as USDA FSA cross-reference)
- **No FDIC underbanked or CFPB credit-invisible explicit reference in card body** — the primary_sources block at lines 890–898 cites both FDIC National Survey of Unbanked + CFPB credit-invisible research, but these statutory-population references are not surfaced in the card body's evidence or red-flag layer where they would inform Scout / Scribe recognition of underbanked applicants. The references currently exist only as residue of the removed admin_risk_term_register (per Cycle 2 fix-in-place). Recommend adding a `common_red_flags` entry or `reviewer_profile_typical.reviewer_priorities` entry that references CFPB credit-invisible status as a Scout-VERIFY signal for CDFI matching. (P1)
- **No explicit MDI (Minority Depository Institution) FDIC reference in body** — primary_sources cites FDIC MDI page (lines 900–903) but the card body does not surface MDI as a lender category in `reviewer_profile_typical.reviewer_types` or `common_portals`. MDIs are a distinct lender category alongside CDFIs and conventional banks. (P1)
- **No `common_funders_observed` field at all.** CLC schema offers this as an observational-only optional field with item-level not.anyOf defense-in-depth. Adding it would let Tilth Archivist accumulate funder-cadence observations against the CLC. (P2 — defer to v0.2)
- **Missing COVID-era commitment-tracking cell.** `common_red_flags` includes COVID-era residuals at HIGH severity (line 553) but `commitment_tracking_pattern` does not have a matching post-loan EIDL re-amortization / PPP forgiveness / ERTC tracking commitment-type. Report Generator gap. (P1)
- **No SBA Community Advantage / Veterans Advantage / EWCP / International Trade Loan / CAPLines references** — card focuses on canonical 7(a) / 504 / Microloan / Express but the SBA suite includes specialized debt products that route through the same SOP 50 10 framework. (P2 — defer to v0.2 SBA-program-specific overlay)
- **`indirect_cost_treatment` framing (line 401)** correctly distinguishes credit from grant budgeting. Strong. (No finding)
- **`match_requirements_typical` REPLACED BY OWNER EQUITY INJECTION (line 402)** is the strongest debt-vs-grant clarification in any card. Strong. (No finding)
- **Personal-guarantor + spousal-signature framing (criterion `guarantor_strength` lines 103–106)** captures ECOA + ownership-not-marital-status distinction correctly. (No finding)

#### Lifecycle / signature / schema concerns

- **Lifecycle gap inverted from sibling CIC pattern.** Card carries `lifecycle.draft_status: "signed"` on disk (line 771) — *not* `"draft"` as flagged in master prompt §5 for the 14-card lifecycle-normalization sweep. The dispatch instruction footer "Lifecycle gap surfaced: draft_status reads 'signed' on disk; no normalization required per Run 1 P0-3" confirms this. **No P0 lifecycle finding here.**
- **`runtime_load_status: "loaded"`** (line 775) is consistent with `runtime_loadable: true` (line 776) and `draft_status: "signed"` — the schema's `allOf[0]` conditional is satisfied.
- **`content_hash: sha256:83293bd551f800f161ea79e8bb269d8c59beb77667219bb41a710b2fede02467`** (line 779) and `ed25519_signature: 4cefd73f...bd2e05` (line 911) are present. Per master prompt §8 item 4, the embedded `ed25519_signature` is intentionally stale on the 3 OD-E-restructured CLC cards (market_access / credit_underwriting / sponsorship_corporate) per OD-C row 272 precedent — loader-time re-validation is v0.2 first-wave scope. A research-session validation script checking the embedded sig against the pinned pubkey will report a mismatch — that is the expected state.
- **Single-track on-disk shape** despite §18.6 v2 LOCK row 274 declaring this card a multi-track CLC. Per Run 1 §3.2 + L2-F1, the §18.6 v2 amendment is LOCKed-but-not-applied — cards-ceremony restructure (parent_lock_row = 259; supersession ceremony = future) pending operator dispatch. The CRITICAL FRAMING header at lines 14–22 carries the L-024 distinction in prose form, holding the operative effect until the structural restructure fires. **Flag for operator decision queue: when to fire the multi-track restructure ceremony.**
- **`admin_risk_term_register` block REMOVED** at Wave 2 Cycle 2 fix-in-place (lines 749–765 comment block documenting the removal). The 13 CLC-06-scoped flagged terms (predatory lending, financial inclusion, underbanked, community wealth-building, wealth-building loans, alternative credit, responsible lending, mission-aligned capital, patient capital, credit-invisible, minority depository institution, creditworthy, stakeholder) carry runtime value but **migration to workspace-wide `admin_risk_register.yaml` v2.4 still pending confirmation** per `_review_handback.decision_queue[1]`. The OD-A handback at `pipeline/handoffs/od_a_completion_2026-05-16.md` reports 60 net-new flagged terms migrated workspace-wide and notes CLC-06 contributed 15 terms — confirmation needed that those 13 substantive terms are among them with per-CLC-register cells populated.

#### Coupling-discipline self-audit (LIVE value-position regex set)

Recursive scan of card body against the four LIVE regex patterns (`TILTH-CIC-\d{2}`, `TILTH-CLC-\d{2}`, `[Cc]apital [Ll]ogic`, `[Cc]ustomer [Ii]dentity`) under the non-exempt path tree:

- `TILTH-CIC-\d{2}`: zero matches.
- `TILTH-CLC-\d{2}`: matches at `card_id` (line 43) and `tilth_clc_id` (line 47) — both exempt per `_VALUE_POSITION_EXEMPT_PATHS` frozenset. Zero non-exempt matches.
- `[Cc]apital [Ll]ogic`: match at `_research_metadata.priors_consulted[0].path` (line 800: `assets/cards/capital_logic/Capital Logic Cards.png`) — exempt per `_VALUE_POSITION_EXEMPT_TOP_LEVEL_PREFIXES = ("_",)`. Zero non-exempt matches.
- `[Cc]ustomer [Ii]dentity`: zero matches.

**Coupling-discipline regression: NONE.** Card is clean under the OD-C row 272 LIVE three-layer predicate.

#### Forbidden-field-registry self-audit

CLC-side six forbidden top-level field names from `FORBIDDEN_FIELD_REGISTRY` (`eligible_cic_subset`, `cic_allowlist`, `cic_denylist`, `preferred_cics`, `cic_win_rate`, `cic_ranking_preferences`): scan returns zero matches at root, zero matches nested anywhere. `common_funders_observed` is absent (no nested-item scan needed); `provenance_requirements` is absent.

**Forbidden-field scan: clean.**

### §2.B — Track B audit (grant) — POSTURE-ONLY PER L-024

Per binding L-024 operator directive: Track B audit is limited to **documenting that the minimal-stub posture is the correct posture** and that the `_partition_provenance.domain_clarification` block (when the card restructures to multi-track shape) must carry verbatim the operator rationale from OD-E row 277:

> Grant logic and credit underwriting logic are objectively different mechanisms even though both are financial-access tools. The stacked-funding use case (e.g., VAPG + low-interest farm loan + tourism grant + small business loan + small business advantage grant) requires separate logic per funding type. Track B is therefore not the right home for grant-side capital — a separate CLC for grant-side credit-readiness or grant-side capital matching belongs in v0.2 Wave 3, not as Track B of credit_underwriting.

On-disk state: card is still single-track shape; the verbatim rationale exists in §G of `section_00_5_section_18_6_v2_amendment.md` (per master prompt §6) but is not yet embedded in the card body's `_partition_provenance.domain_clarification` because the cards-ceremony restructure has not fired. When the restructure fires, the verbatim rationale block must be present.

Routing for grant-side capital-readiness ideas: **v0.2 Wave 3 backlog item, provisional slug `grant_side_credit_readiness` or `capital_readiness_grant` (final naming pending Wave 3 dispatch).**

This handback **proposes zero substantive Track B content** — any substantive Track B proposal would be a binding L-024 violation.

---

## §3 — Research Findings (source verification + new sources)

### §3.A — Track A (debt) source-verification pass

| URL | Source type | Access date | Card field(s) supported | Confidence | Status |
|---|---|---|---|---|---|
| https://www.sba.gov/document/sop-50-10-lender-development-company-loan-programs | official | 2026-05-15 | underwriting_criteria, scoring_weight_patterns, evidence_weights, common_application_forms, narrative_section_patterns, common_red_flags, reporting_requirements_typical, compliance_obligations | HIGH | Current (verify SOP edition at Scout-VERIFY runtime) |
| https://www.rd.usda.gov/programs-services/business-programs/business-industry-loan-guarantees | official | 2026-05-15 | scoring_weight_patterns[USDA RD B&I], common_application_forms, common_portals, compliance_obligations | HIGH | Current |
| https://www.rd.usda.gov/programs-services/community-facilities/community-facilities-direct-loan-grant-program | official | 2026-05-15 | common_application_forms[USDA RD 442-7], common_portals | HIGH | Current |
| https://www.rd.usda.gov/programs-services/business-programs/intermediary-relending-program | official | 2026-05-15 | common_application_forms[IRP], common_portals | HIGH | Current |
| https://www.cdfifund.gov/programs-training/certification/cdfi | official | 2026-05-15 | underwriting_criteria[community_impact], evidence_weights[community_impact_doc], compliance_obligations | HIGH | Current |
| https://www.cdfifund.gov/awards | official | 2026-05-15 | common_portals | HIGH | Current |
| https://ofn.org/cdfi-locator/ | primary (trade-association) | 2026-05-15 | common_application_forms[CDFI portal], common_portals, evidence_weights[credit_explanation_letter] | HIGH | Current |
| https://www.sba.gov/funding-programs/loans/lender-match | official | 2026-05-15 | common_portals | HIGH | Current |
| https://home.treasury.gov/policy-issues/small-business-programs/state-small-business-credit-initiative-ssbci | official | 2026-05-15 | common_application_forms[SSBCI], common_portals | HIGH | Current |
| https://www.cdfa.net/cdfa/cdfaweb.nsf/pages/financing-tools.html | primary (trade-association) | 2026-05-15 | common_application_forms[state RLF], common_portals | HIGH | Current |
| https://americassbdc.org/ | primary | 2026-05-15 | common_portals | HIGH | Current |
| https://www.score.org/ | primary | 2026-05-15 | common_portals | HIGH | Current |
| https://www.investopedia.com/terms/f/five-c-credit.asp | practitioner / secondary | 2026-05-15 | scoring_weight_patterns[5C] | LOW (replace) | **REPLACE per L-024 dispatch instruction** |
| https://www.consumerfinance.gov/rules-policy/regulations/1002/ | official | 2026-05-15 | compliance_obligations[ECOA], underwriting_criteria[guarantor_strength] | HIGH | Current |
| https://www.fdic.gov/analysis/household-survey/ | official | 2026-05-15 | _research_metadata only (residue of removed admin-risk register) | HIGH | Add to body |
| https://www.consumerfinance.gov/data-research/research-reports/data-point-credit-invisibles/ | official | 2026-05-15 | _research_metadata only (residue) | HIGH | Add to body |
| https://www.fdic.gov/regulations/resources/minority/mdi.html | official | 2026-05-15 | _research_metadata only (residue) | HIGH | Add to body |

### §3.B — New official sources proposed for body integration

| URL | Source type | Card field(s) to support | Confidence |
|---|---|---|---|
| https://www.fdic.gov/regulations/safety/manual/section3-1 (FDIC Risk Management Manual of Examination Policies §3 Loans) | official | scoring_weight_patterns[5C] — REPLACE Investopedia | HIGH |
| https://www.occ.treas.gov/publications-and-resources/publications/comptrollers-handbook/files/commercial-lending/index-commercial-lending.html (OCC Comptroller's Handbook — Commercial Lending booklet) | official | scoring_weight_patterns[5C], underwriting_criteria — co-citation with FDIC | HIGH |
| https://www.fsa.usda.gov/programs-and-services/farm-loan-programs/ (USDA FSA Farm Loan Programs — Direct + Guaranteed Farm Operating / Farm Ownership) | official | common_application_forms[USDA FSA farm loans] + common_portals — operator-relevant per L-024 stacked-funding example | HIGH |
| https://www.fsa.usda.gov/programs-and-services/farm-loan-programs/microloans/ (USDA FSA Microloans) | official | common_application_forms — operator-relevant | HIGH |
| https://www.sba.gov/funding-programs/loans/community-advantage-loans (SBA Community Advantage / 7(a) Community Advantage) | official | common_application_forms — fills SBA 7(a)-specialty gap | MEDIUM |

### §3.C — Track B (grant) — no source research per L-024 directive

---

## §4 — Proposed Card Improvements (Track A only — eight runtime-behavior categories)

### §4.A.1 — Search vocabulary / classification

**TA-1 — Add explicit MDI / credit-invisible / underbanked references to reviewer_profile_typical.reviewer_types.** Path: `reviewer_profile_typical.reviewer_types[NEW]`. Why: Scout matching should recognize MDI lenders as a distinct lender category; CFPB credit-invisible and FDIC underbanked are statutory populations that signal CDFI-matching opportunities. Source: FDIC MDI page, CFPB credit-invisibles research, FDIC underbanked survey. Belongs in: card YAML. Seat: Scout / Judge. (P1)

**TA-2 — Add `usda_fsa_farm_loan_officer` and `farm_credit_system_lender` to reviewer_profile_typical.reviewer_types.** Path: `reviewer_profile_typical.reviewer_types[NEW]`. Why: L-024 stacked-funding example includes "low-interest farm loan" which routes through USDA FSA + Farm Credit System (not USDA RD). Scout / Judge needs to recognize farm-credit lender as a Credit & Underwriting CLC reviewer category. Source: fsa.usda.gov. Belongs in: card YAML. Seat: Scout / Judge. (P1)

### §4.A.2 — Evidence capture / missing-evidence prompts

**TA-3 — Strengthen `evidence_weights.tax_returns` and `evidence_weights.financial_statements` to add post-disbursement audit anchoring per L-024 dispatch.** Path: `evidence_weights.tax_returns.rationale` + `evidence_weights.financial_statements.rationale`. Why: per L-024 dispatch "Strengthen evidence prompts: tax returns, P&L, balance sheet, cash flow forecast, debt schedule, collateral, owner equity, insurance, management resume, use-of-funds." Card already covers these; the strengthening request is to make rationale explicitly call out that **each evidence item is paired against a Scout-VERIFY missing-evidence prompt** that fires when the applicant has not provided it. Belongs in: card YAML. Seat: Scout / Scribe / Logician. (P1)

**TA-4 — Split `evidence_weights.debt_schedule` into `business_debt_schedule` + `personal_debt_schedule`.** Path: `evidence_weights[REVISED]`. Why: SBA SOP separates business + personal debt schedules; SBA Form 413 owns personal side. Card currently bundles both in one entry. Source: SBA SOP 50 10, SBA Form 413 instructions. Belongs in: card YAML. Seat: Scribe / Logician. (P2)

**TA-5 — Add explicit `personal_financial_statement_sba_form_413` evidence item.** Path: `evidence_weights[NEW]`. Why: SBA Form 413 is universally required and runs alongside the financial statements + tax returns triad; currently bundled into general "tax_returns" + "debt_schedule" coverage. Source: SBA Form 413 instructions. Belongs in: card YAML. Seat: Scout / Scribe / Logician. (P1)

**TA-6 — Add `ucc_search_result` evidence item.** Path: `evidence_weights[NEW]`. Why: Card flags hidden-debt UCC discovery as HIGH red flag (line 543) but does not list UCC search as an evidence weight. Pre-application UCC search is standard CDFI / SBA discipline. Source: SBA SOP 50 10, uniformlaws.org. Belongs in: card YAML. Seat: Scout / Logician. (P1)

### §4.A.3 — KFR fact classes / scoring weight patterns / evidence weights

**TA-7 — Add KFR fact class `loan_purpose_specificity` + `repayment_source_traceability` to underwriting_criteria scope (as supplementary criteria).** Why: these are derived facts that emerge from Intake / Scout VERIFY. Currently captured implicitly in `use_of_funds` + `repayment_capacity` criteria; making them explicit KFR classes lets Logician PRE-flight check them. Source: SBA SOP 50 10. Belongs in: card YAML + Logician spec at v0.2. Seat: Logician / Scribe. (P2)

**TA-8 — Replace Investopedia 5C source citation with FDIC RMS Manual + OCC Comptroller's Handbook co-citation.** Path: `scoring_weight_patterns[0].source_citation` (currently `https://www.investopedia.com/terms/f/five-c-credit.asp`). Replace with FDIC §3 Loans + OCC Commercial Lending booklet URLs. Why: per L-024 dispatch instruction "Avoid Investopedia-style materials where official lender guidance exists." Source: fdic.gov, occ.treas.gov. Belongs in: card YAML. Seat: Scout / Scribe / Judge. **(P0 per L-024 dispatch directive)**

### §4.A.4 — Drafting register and admin-risk handling

**TA-9 — Confirm migration status of 13 CLC-06-scoped flagged terms to workspace `admin_risk_register.yaml` v2.4.** Per OD-A handback `pipeline/handoffs/od_a_completion_2026-05-16.md` reports 60 net-new flagged terms migrated workspace-wide; CLC-06 contributed 15 terms. The card-body `admin_risk_term_register` was REMOVED at Wave 2 Cycle 2 fix-in-place (lines 749–765). **Operator decision: confirm v2.4 contains the 13 substantive CLC-06 terms (predatory lending, financial inclusion, underbanked, community wealth-building, wealth-building loans, alternative credit, responsible lending, mission-aligned capital, patient capital, credit-invisible, minority depository institution, creditworthy, stakeholder).** Belongs in: workspace admin_risk_register.yaml; NOT in card body. Seat: Archivist / Editor. (P1)

**TA-10 — For each migrated term, recommend `per_clc_register` map cell.** Per OD-A v3.0 schema: `per_clc_register: tuple[tuple[str, str], ...]`. For credit_underwriting CLC-06 specifically:
- `predatory lending`: AVOID (RED — never use about lenders we want to draft to)
- `financial inclusion`: PREFERRED (GREEN — CDFI + foundation-PRI dialect)
- `underbanked`: EXPECTED (GREEN — CDFI dialect; CFPB statutory term)
- `community wealth-building`: PREFERRED in CDFI / foundation contexts; AVOID in conventional bank (split per dialect — operator review)
- `wealth-building loans`: PREFERRED in CDFI / foundation; AVOID in conventional bank (split)
- `alternative credit`: OK (qualitative; common practitioner usage)
- `responsible lending`: PREFERRED (GREEN — universal positive)
- `mission-aligned capital`: PREFERRED in CDFI / foundation; AVOID in conventional bank (split)
- `patient capital`: PREFERRED in CDFI / foundation-PRI; AVOID in conventional bank (split)
- `credit-invisible`: EXPECTED (GREEN — CFPB statutory term)
- `minority depository institution`: EXPECTED (GREEN — FDIC statutory category)
- `creditworthy`: OK (universal)
- `stakeholder`: AVOID (RED — per CLC-03 + CIC-05 cross-CLC coordination)

The split-dialect terms (community wealth-building / wealth-building loans / mission-aligned capital / patient capital) are the load-bearing operator decisions. Belongs in: workspace `admin_risk_register.yaml` v2.4 with per_clc_register cells. Seat: Editor / Archivist. (P1)

### §4.A.5 — Reviewer / rubric logic

**TA-11 — Add `mdi_lender_underwriting_overlay` to scoring_weight_patterns at v0.2.** Why: MDIs operate under separate FDIC oversight + Treasury MDI program; their underwriting prioritizes minority-community lending alongside credit. Currently absent from card. Source: FDIC MDI page. Belongs in: v0.2 lender-specific overlay (not card body proper). Seat: Judge. (P2)

**TA-12 — Strengthen `reviewer_priorities` to explicitly enumerate the "five questions a credit memo must answer" pattern.** Card already does this at lines 421–429 — strengthen note to anchor the framing as the canonical credit-memo answer pattern (where does the cash come from? will it arrive? what if it doesn't? has the team done this before? are the financial controls strong enough?). Seat: Judge / Scribe. (P2)

### §4.A.6 — Red-team probes (common_red_flags)

**TA-13 — Add `equity_injection_heloc_undisclosed` red flag.** Path: `common_red_flags[NEW]`. Why: HELOC-sourced equity injection is a SBA SOP edge case — generally excluded, exception permitted when lender documents secured + non-dependent finding. Currently captured in `missing_owner_equity_injection` (line 522) as "Is any portion borrowed (HELOC, 401(k) loan)?" but not as a dedicated probe. Source: SBA SOP 50 10. Belongs in: card YAML. Seat: Red Team / Logician. (P1)

**TA-14 — Add `farm_loan_misroute_to_business_loan` red flag.** Path: `common_red_flags[NEW]`. Why: L-024 stacked-funding example surfaces farm loans (USDA FSA) routed through farm-credit channels not USDA RD business channels. Misroute would fail USDA RD eligibility screen. Source: USDA FSA Farm Loan Programs page. Belongs in: card YAML. Seat: Scout / Red Team. (P1)

**TA-15 — Add `mission_lender_misrouted_as_commercial_bank` red flag.** Path: `common_red_flags[NEW]`. Why: CDFI portfolio matching depends on lender type; routing a CDFI opportunity through conventional bank dialect (or vice versa) is a structural misframing. Source: OFN CDFI Locator + CDFI Fund certification page. Belongs in: card YAML. Seat: Scout / Scribe / Red Team. (P1)

### §4.A.7 — Reporting / commitment extraction

**TA-16 — Add `covid_era_residual_liability_status` commitment type to commitment_tracking_pattern.** Path: `commitment_tracking_pattern.typical_commitments_extracted[NEW]`. Why: Card's `common_red_flags` includes COVID-era residuals (line 553) at HIGH severity but does not have a matching commitment-extraction cell. Report Generator needs to track post-loan EIDL re-amortization status + PPP forgiveness final status + ERTC IRS scrutiny status as ongoing covenant-adjacent obligations. Source: SBA COVID-19 relief options page. Belongs in: card YAML. Seat: Report Generator / Logician. (P1)

**TA-17 — Add `mdi_lender_classification` commitment type for portfolio-tracking purposes.** Why: borrower-level reporting where the lender is an MDI surfaces a distinct CDFI-Fund + Treasury MDI program reporting requirement. Source: FDIC MDI page. Belongs in: card YAML. Seat: Report Generator. (P2)

### §4.A.8 — Memory namespace usefulness

**TA-18 — Memory namespace `cards:clc:credit_underwriting:lender_overlay:<lender_slug>`** at v0.2 — accumulates per-CDFI / per-SBA-lender / per-USDA-RD-office underwriting overlays as cycles complete. Source: architecture v7.0.11 §1.9. Seat: Archivist. (P2 — defer to v0.2 lender-specific overlay)

**TA-19 — Memory namespace `cards:clc:credit_underwriting:debt_grant_misframe:<grant_id>`** at v0.2 — accumulates Tilth-detected debt-as-grant misframing events for Lessons Memory belief-weight accumulation. Source: master prompt §6 L-024 lesson. Seat: Archivist / Logician. (P2 — defer to v0.2)

### §4.A — Phase 4 fold-in discipline self-check

Per §18.11 v1.1 four refusals:
- (a) Structured-sub-field expansions on canonical entries that smuggle a new schema item shape: none proposed. All proposed additions follow existing schema item shapes (new items inside existing canonical fields).
- (b) Dedicated-field-name forks: none proposed. No new top-level field names parallel to canonical ones.
- (c) Compound enum values: none proposed. All severity / weight / frequency values use canonical enum sets (HIGH | MEDIUM | LOW; FREQUENT | OCCASIONAL | RARE | UNKNOWN).
- (d) Literal canonical CIC/CLC slug strings in non-exempt value positions: none proposed. All cross-CLC references use display names (e.g., "CLC-03 Operating Capacity" only inside this handback's prose, not in proposed YAML values).

**Phase 4 fold-in discipline: clean.** No proposal trips any refusal.

---

## §5 — Operator Decision Queue

### §5.A — Track A (debt) operator decisions

1. **OD-CLC-06-1 — Investopedia source replacement (P0 per L-024 dispatch).** Replace Investopedia 5C citation with FDIC RMS Manual + OCC Comptroller's Handbook co-citation. Operator decision: approve replacement source URLs and Patch Plan §8.1 dispatch.

2. **OD-CLC-06-2 — `admin_risk_register.yaml` v2.4 migration confirmation (P1).** Confirm the 13 CLC-06-scoped flagged terms migrated to workspace register per OD-A pattern. If not yet migrated, dispatch v2.4 follow-on migration. **Load-bearing operator decision: when to fire the v2.4 compound migration dispatch (if not already complete).**

3. **OD-CLC-06-3 — Split-dialect per_clc_register cells for 4 terms (P1).** For `community wealth-building` / `wealth-building loans` / `mission-aligned capital` / `patient capital`: the per_clc_register cell varies by funder dialect (CDFI / foundation-PRI vs conventional bank). Operator decides whether to split the per_clc_register cell by dialect or pick a unified posture. Per Law 4 + admin-risk discipline, applicant approves each substitution at runtime — operator decision is whether to encode the dialect split at admin_risk_register level or leave to runtime applicant approval.

4. **OD-CLC-06-4 — Multi-track restructure cards-ceremony dispatch (P1).** §18.6 v2 LOCKed but the card is still single-track shape on disk. When to fire the restructure ceremony (parent_lock_row=259; new ceremony_parent_row=future §18.6 v2.x card-restructure amendment). Restructure inserts `_partition_provenance.domain_clarification` carrying the verbatim L-024 operator rationale.

5. **OD-CLC-06-5 — USDA FSA farm-loan reference addition (P1).** Operator confirms adding USDA FSA Farm Loan Programs (Direct + Guaranteed Farm Operating / Farm Ownership / Microloans) references to `common_application_forms` and `common_portals`. Operator-relevant per L-024 stacked-funding example.

6. **OD-CLC-06-6 — Personal Financial Statement SBA Form 413 as separate evidence item (P1).** Operator approves splitting current bundled coverage into dedicated `personal_financial_statement_sba_form_413` evidence item.

7. **OD-CLC-06-7 — UCC search as evidence weight (P1).** Operator approves adding `ucc_search_result` to evidence_weights.

8. **OD-CLC-06-8 — Red-flag additions (P1).** Operator approves `equity_injection_heloc_undisclosed`, `farm_loan_misroute_to_business_loan`, `mission_lender_misrouted_as_commercial_bank` red-flag additions.

9. **OD-CLC-06-9 — COVID-era residual commitment-tracking cell (P1).** Operator approves `covid_era_residual_liability_status` commitment type addition.

10. **OD-CLC-06-10 — MDI / credit-invisible / underbanked body-surface references (P1).** Operator approves surfacing FDIC MDI + CFPB credit-invisible + FDIC underbanked references in card body (currently only in `_research_metadata.primary_sources`).

11. **OD-CLC-06-11 — Forward-compat v0.2 lender-specific overlay design (P2).** Whether to spec per-CDFI / per-MDI / per-SBA-lender / per-USDA-RD-office overlay card pattern at v0.2 first-wave. Forward-compat at v7.0.11.

12. **OD-CLC-06-12 — SBA SOP 50-10 edition pinning + Program Rule Pack boundary (P2).** Confirm card defers SOP-edition specifics (equity injection percentages, credit score thresholds, eligibility screens) to Program Rule Pack layer.

13. **OD-CLC-06-13 — DSCR target band caveat strengthening (P2).** Strengthen "modal practice, not regulatory floor" disclaimer in DSCR criterion (line 64).

### §5.B — Track B (grant) operator decisions

14. **OD-CLC-06-14 — v0.2 Wave 3 grant-side-credit-readiness CLC dispatch (P1).** Operator confirms v0.2 Wave 3 backlog item for a separate grant-side credit-readiness or grant-side capital-matching CLC (provisional slug: `grant_side_credit_readiness` or `capital_readiness_grant`). Per L-024 operator directive, this is the canonical home for substantive grant-side capital-readiness logic — NOT Track B of CLC-06.

15. **OD-CLC-06-15 — `_partition_provenance.domain_clarification` block placement (P1).** When the cards-ceremony multi-track restructure fires for CLC-06 per OD-CLC-06-4, confirm the verbatim L-024 rationale is embedded in `_partition_provenance.domain_clarification`. Operator approves verbatim text per OD-E row 277.

---

## §6 — Validation Checklist

- [x] Schema fields complete: 15/15 required fields populated (per card body line 921).
- [x] No forbidden coupling field names (FORBIDDEN_FIELD_REGISTRY scan — clean at root + nested).
- [x] No forbidden value-position regex matches outside exempt paths (zero non-exempt matches against the four LIVE patterns).
- [x] No private organization-specific data.
- [x] No unsourced program-law claims (all program-law specifics carry primary-source citations; SOP edition qualifier at lines 34–39 defers per-revision detail to Program Rule Pack / Scout-VERIFY runtime).
- [x] No excessive quoted source text (`_research_metadata.primary_sources[*].verbatim_quote` entries are ≤2 sentences per Wave 1 OQ).
- [x] Lifecycle status consistent with architecture v7.0.11 §1.5: `draft_status: "signed"` + `runtime_load_status: "loaded"` + `runtime_loadable: true` + `signed_at` / `signed_by` / `content_hash` all present.
- [x] For multi-track CLCs: shared root metadata preserved on disk (single-track still); track restructure ceremony pending per OD-CLC-06-4. oneOf branch 2 (multi-track) compliance verification deferred until restructure fires.
- [x] Coupling-discipline self-audit: clean.
- [x] Phase 4 fold-in discipline self-check: clean (zero refusals tripped).
- [x] L-024 compliance: zero substantive Track B proposals; Track B audit limited to documenting minimal-stub posture + v0.2 Wave 3 routing.

---

## §7 — Regression Tests

### RT-1 — Track A vs Track B routing distinction (multi-track distinguishing test)

**Prompt:** "Tilth, the operator's MycoSymbiotics Cooperative is exploring 'capital-readiness funding for cooperative-development credit'. The opportunity arrived via a CDFI ecosystem newsletter. Surface CLC-06 Credit & Underwriting framing."

**Expected pre-edit behavior:** Scout returns CLC-06 candidate; Scribe enters credit-memo register; Judge applies 5C / SBA SOP / USDA RD / CDFI mission framework.

**Expected post-edit behavior (after multi-track restructure):** Scout returns CLC-06 candidate; Tilth surfaces `track_a` (debt) framing as primary. If the operator's narrative subsequently signals "grant-side capital readiness, not loan readiness," Tilth surfaces v0.2 Wave 3 routing prompt: "this opportunity looks like grant-side capital-readiness; route to v0.2 Wave 3 `grant_side_credit_readiness` CLC when it exists; fall back to minimal-stub Track B for v0.1."

### RT-2 — v0.2 Wave 3 routing surface for grant-side capital-readiness ideas

**Prompt:** "Tilth, the operator wants to write a grant proposal for 'capital-readiness coaching to help small farms become loan-ready'. What CLC applies?"

**Expected pre-edit behavior:** Scout might route to CLC-06 Credit & Underwriting (because of "loan-ready" keyword); Scribe might enter credit-memo register inappropriately.

**Expected post-edit behavior:** Scout surfaces CLC-06 Credit & Underwriting as **NOT the right home** per L-024 lesson; recommends operator-decision-at-draft: "this opportunity looks like grant-side capital-readiness (a grant program funding capital-readiness coaching), NOT credit underwriting (a loan to the farms). Route to v0.2 Wave 3 `grant_side_credit_readiness` CLC when it exists. For v0.1 fall back: route to closest existing CLC by funding-mechanism (likely Operating Capacity for the capital-readiness-coaching grant; flag for operator review)."

### RT-3 — Stacked-funding use case (L-024 verbatim example)

**Prompt:** "Tilth, plan funding for a farm value-added project: VAPG grant + low-interest farm loan + tourism grant + small business loan + small business advantage grant. Show which CLC applies to each."

**Expected pre-edit behavior:** Tilth might collapse to one CLC framing (likely Market Access for VAPG dominance) or single-track CLC-06 for all loan items without distinguishing FSA from SBA.

**Expected post-edit behavior:** Tilth surfaces five separate CLC + funding-mechanism activations:
- VAPG → Market Access (Track A SBIR Phase II analog; planning grant + working capital grant)
- low-interest farm loan → Credit & Underwriting Track A (debt; USDA FSA Direct/Guaranteed Farm Operating per OD-CLC-06-5)
- tourism grant → Catalytic Change or Operating Capacity (depending on framing)
- small business loan → Credit & Underwriting Track A (SBA 7(a) typical)
- small business advantage grant → grant-side capital readiness — pending v0.2 Wave 3 CLC; v0.1 fallback per OD-CLC-06-14

Each instrument has separate logic; per L-024 lesson "stacked funding stacks separate mechanisms — each instrument deserves its own CLC at runtime, not Track A / Track B of one CLC."

### RT-4 — Grant-language-on-debt-instrument detection

**Prompt:** Scribe receives an opportunity (CDFI-funded loan) with applicant-supplied narrative emphasizing "community impact, healthy food access, jobs for low-income workers" but no repayment-source narrative or DSCR math.

**Expected pre-edit behavior:** Scribe might draft mission-forward narrative; Judge might score against mission-impact rubric.

**Expected post-edit behavior:** Scribe refuses grant-narrative register (per CRITICAL FRAMING runtime expectation at card lines 14–22); Logician PRE-flight fires `common_red_flags[treating_debt_as_grant_in_application_framing]` (HIGH severity); Tilth surfaces missing-evidence prompts: repayment source narrative + DSCR math + cash flow projection + use-of-funds itemization + owner equity injection + collateral + management resume. Mission-impact narrative is INCLUDED as co-equal at CDFI but does NOT substitute for credit narrative.

### RT-5 — Investopedia source replacement regression test

**Prompt:** Pull `scoring_weight_patterns[0].source_citation` from card and verify URL.

**Expected pre-edit behavior:** Returns `https://www.investopedia.com/terms/f/five-c-credit.asp` (P0 per L-024 dispatch).

**Expected post-edit behavior:** Returns FDIC RMS Manual §3 Loans URL + OCC Comptroller's Handbook Commercial Lending URL (co-cited). Investopedia URL removed or downgraded to tertiary reference.

### RT-6 — HELOC equity injection edge case

**Prompt:** Applicant proposes 15% equity injection sourced from HELOC against personal residence.

**Expected pre-edit behavior:** Card flags `missing_owner_equity_injection` red flag generally (line 522) but the HELOC-specific edge case (excluded except when lender documents secured + non-dependent) is not surfaced as a dedicated probe.

**Expected post-edit behavior:** New `equity_injection_heloc_undisclosed` red flag fires (per TA-13); Logician surfaces SBA SOP 50 10 conditional language; operator-decision-at-draft prompt: "HELOC equity injection requires lender finding that HELOC is fully secured AND borrower repayment capacity does not depend on the SBA loan. Document both findings or substitute non-borrowed equity source."

---

## §8 — Patch Plan

**File:** `pipeline/cards/CLC/credit_underwriting.yaml`

(Operator dispatches edits as separate ceremony per OD-C / OD-E precedent: per-card lock_history supersession row + post-restructure SHA3-512 + publisher Ed25519 signature against `vault_shared/cards/publisher_pubkey.signed.yaml`. No edits applied from this research session.)

### Patch Plan §8.1 — Investopedia source replacement (P0 per L-024)

- `scoring_weight_patterns[0].source_citation`: replace `https://www.investopedia.com/terms/f/five-c-credit.asp` with FDIC RMS Manual §3 Loans URL co-cited with OCC Comptroller's Handbook Commercial Lending URL.
- `_research_metadata.primary_sources`: replace Investopedia entry with FDIC + OCC entries.
- Forward-binding: mark for `R-CARDS-ENUM-CANONICAL` (OD-B, pending) regression at v0.2 — Investopedia-style sources should fail closed when an official equivalent exists.

### Patch Plan §8.2 — Multi-track restructure (P1 per OD-CLC-06-4)

- Restructure card into multi-track shape per §18.6 v2 OD-E LOCK row 274.
- `track_a` = `debt` (everything currently in card body except `_research_metadata` + `lifecycle` + shared root metadata).
- `track_b` = `grant` (MINIMAL-STUB per L-024).
- `_partition_provenance.domain_clarification`: embed verbatim OD-E row 277 operator rationale (per OD-CLC-06-15).
- Shared root metadata preserved at root: `schema_version` / `card_axis` / `card_id` / `slug` / `display_name` / `funding_mechanism_summary` / `tilth_clc_id` / `lifecycle` / `_research_metadata`.
- Item-level not.anyOf defense-in-depth replicated inside each `track_container` per §18.6 v2 §1.6.

### Patch Plan §8.3 — USDA FSA farm-loan additions (P1 per OD-CLC-06-5)

- `common_application_forms[NEW]`: USDA FSA Direct / Guaranteed Farm Operating Loan application; USDA FSA Direct / Guaranteed Farm Ownership Loan application; USDA FSA Microloan application.
- `common_portals[NEW]`: USDA FSA Farm Loan Programs portal.
- `reviewer_profile_typical.reviewer_types[NEW]`: `usda_fsa_farm_loan_officer`; `farm_credit_system_lender`.
- `_research_metadata.primary_sources[NEW]`: fsa.usda.gov entries.

### Patch Plan §8.4 — Evidence weight additions (P1)

- `evidence_weights[NEW]: personal_financial_statement_sba_form_413` (per OD-CLC-06-6, TA-5).
- `evidence_weights[NEW]: ucc_search_result` (per OD-CLC-06-7, TA-6).
- Optional: split `evidence_weights.debt_schedule` into `business_debt_schedule` + `personal_debt_schedule` (per TA-4).

### Patch Plan §8.5 — Red-flag additions (P1)

- `common_red_flags[NEW]: equity_injection_heloc_undisclosed` (per TA-13, OD-CLC-06-8).
- `common_red_flags[NEW]: farm_loan_misroute_to_business_loan` (per TA-14, OD-CLC-06-8).
- `common_red_flags[NEW]: mission_lender_misrouted_as_commercial_bank` (per TA-15, OD-CLC-06-8).

### Patch Plan §8.6 — Body-surface MDI / credit-invisible / underbanked (P1)

- `reviewer_profile_typical.reviewer_types[NEW]`: `mdi_minority_depository_institution_lender`.
- `common_portals[NEW]`: FDIC MDI page; CFPB credit-invisible research page; FDIC unbanked / underbanked survey.
- `common_red_flags[NEW]` or `reviewer_priorities[NEW]`: surface CFPB credit-invisible status as a Scout-VERIFY signal for CDFI matching.

### Patch Plan §8.7 — Commitment-tracking additions (P1)

- `commitment_tracking_pattern.typical_commitments_extracted[NEW]: covid_era_residual_liability_status` (per TA-16, OD-CLC-06-9).
- `commitment_tracking_pattern.typical_commitments_extracted[NEW]: mdi_lender_classification` (per TA-17).

### Patch Plan §8.8 — Admin-risk register migration (P1; workspace file, not card YAML)

**File:** `pipeline/institutional_memory/admin_risk_register.yaml` (v2.4 follow-on).

- Confirm migration of 13 CLC-06-scoped flagged terms per OD-CLC-06-2.
- Apply per_clc_register cells per TA-10 (operator approves split-dialect cells per OD-CLC-06-3).

### Patch Plan §8.9 — Forward-binding contract notes

Per OD-D Phase 4 forward-binding contract: items in §8.2 (multi-track restructure), §8.6 (body-surface additions), and §8.8 (admin-risk register migration) touch refusal (a) / (b) territory only via legitimate canonical-schema expansion (no smuggling) and refusal (d) is unaffected (zero literal CLC slug strings introduced in non-exempt value positions). The patch plan is clean against the four Phase 4 refusals; mark for `F-CARDS-COUPLING-VIOLATION-EXTENSION` regression hardening at v0.2 first wave as defense-in-depth.

### Patch Plan §8.10 — v0.2 Wave 3 backlog item (Track B disposition — NOT a CLC-06 card edit)

Per OD-CLC-06-14: register v0.2 Wave 3 backlog item for a separate CLC handling grant-side credit-readiness or grant-side capital-matching logic. Provisional slug: `grant_side_credit_readiness` or `capital_readiness_grant`. Final naming pending Wave 3 dispatch. This is where substantive grant-side capital-readiness research lands — NOT here. **Per L-024 binding operator directive, this handback proposes zero substantive Track B content for CLC-06.**

---

## Summary

```
Card: CLC:credit_underwriting
Card file: pipeline/cards/CLC/credit_underwriting.yaml
Research hours actual: 2.9
Findings: 19 total — 1 P0, 11 P1, 7 P2
Decision queue: 15 operator approvals required (13 Track A + 2 Track B posture)
Conflicts with prior art: NONE
Coupling-discipline regression: NONE
Lifecycle gap surfaced: draft_status reads "signed" on disk; no normalization required per Run 1 P0-3
Track B posture: MINIMAL-STUB per L-024 — substantive expansion routed to v0.2 Wave 3 grant-side-credit-readiness CLC backlog
Multi-track on-disk shape: single-track legacy shape — §18.6 v2 cards-ceremony pending (CRITICAL FRAMING prose at lines 14–22 holds operative effect until restructure fires)
Review readiness: READY
```
