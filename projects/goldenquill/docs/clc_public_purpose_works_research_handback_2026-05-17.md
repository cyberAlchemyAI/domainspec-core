# TILTH-CLC-01 Public Purpose & Works — Research Handback

**Filed:** 2026-05-17
**Workspace:** `/Users/goldenquill/Downloads/GoldenQuill/`
**Dispatch:** Per-card research-improvement pass per `docs/cic_clc_unified_master_prompt_2026-05-17.md` §2.
**Card:** `pipeline/cards/CLC/public_purpose_works.yaml` (Wave 2 LOCKed 2026-05-16T16:00:00Z row 255; content_hash `sha256:18ac074d533f027bf542246a1c111bd1a5f342025eaa42d36f9e14deb16924a9`; signed by `founder`).
**Track shape:** single_track.
**Authority chain:** master prompt §2 + §3 (LIVE F-CARDS-COUPLING-VIOLATION-EXTENSION) + §5 (lifecycle gap) + §7 (OD-A v2.4 register).
**Companion artifacts read:** card body (sections lines 1-905), schema `card_clc.schema.json`, `pipeline/program_rule_packs/_manifest/active_prps.yaml` (6-entry draft roster, loader at v0.1 NotImplementedError), `pipeline/institutional_memory/admin_risk_register.yaml` v2.4 (CLC-01 entries at lines 900/911/921 — `disadvantaged community` GREEN/EXPECTED, `equitable access` GREEN/OK, `resilience` GREEN/EXPECTED), and sibling handbacks (`food_systems`, `public_agency`).

---

## §1. Card Impact Thesis

`public_purpose_works` is the funder-side underwriting logic for government-mandate, civic-benefit, public-works program funding — the eight statutory-anchor channels named at lines 27–411: CDBG (HUD), Community Facilities (USDA RD), BRIC (FEMA), CWSRF/DWSRF (EPA), BUILD/RAISE (DOT), Public Works (EDA), CDBG-DR (HUD), and state-administered SRF/SCBGP pass-throughs (PennVEST as the operator's PA exemplar). Its job is to make Tilth read **any** applicant pursuing this funding through statutory authority + public benefit + procurement compliance + secured non-federal match + project readiness + audit posture + NEPA pathway + maintenance commitment — and to do so without coupling the funder-side logic to any applicant archetype (Law-2 / orthogonality), without smuggling live program-law (active match percentages, current single-audit threshold cycle math, page limits) into the card body that belongs in Program Rule Packs, and without silently rewriting administration-flagged vocabulary (Justice40, environmental justice, climate resilience, equitable access).

What this card should cause Tilth to do differently:

1. When Scout sees `CDBG`, `Community Facilities`, `BRIC`, `CWSRF`, `DWSRF`, `BUILD`, `RAISE`, `Public Works`, `PennVEST`, `IIJA`, anchor underwriting logic in the cited statute (24 CFR 570 / 7 CFR 3570 / Public Law 117-58 §70914 BABA / 40 USC §3141 Davis-Bacon / 2 CFR 200 Subparts D–F / 44 CFR Part 201 / 33 U.S.C. §1383) — not in the NOFO restatement alone.
2. When Scribe drafts a public-works narrative, force `eligibility_citation` + `board_resolution` + `engineering_estimate` + `capital_plan_reference` + `match_commitment_letter` + `site_control` + `procurement_policy` + `environmental_review_pathway` + `audit_documentation` + `benefit_cost_analysis` evidence prompts at the appropriate weights, with explicit Davis-Bacon + BABA acknowledgement on every federally-assisted construction draft.
3. When Logician audits a draft, fire the 16 common_red_flags (vague eligibility / weak public benefit / uncommitted match / procurement silence / unresolved site control / unrealistic timeline / no NEPA pathway / Davis-Bacon nonresponsive / BABA waiver no rationale / engineering estimate quality / unfunded maintenance / missing planning citation / single-audit findings unaddressed) with the published `red_team_probe` for each.
4. When Report Generator builds commitment-tracking, extract the 16 commitment types (construction-milestone NTP / substantial completion / final acceptance / procurement-executed / match-expenditure / beneficiary count / facility units delivered / jobs / Davis-Bacon payrolls / BABA filing / single-audit / FFATA sub-award / closeout / final SF-425 / final performance report / property inventory) into `proposal_commitments.yaml` under `public_purpose_works_commitments`.
5. When the active opportunity is federal under current administration framing, route administration-flagged vocabulary (`disadvantaged community`, `equitable access`, `resilience`, `climate resilience`, `environmental justice`, `Justice40`, `equity`) through the workspace-wide `admin_risk_register.yaml` v2.4 with the CLC-01-specific `per_clc_register` cell — never silently rewrite, always surface for operator approval.
6. When the underwriting logic intersects the now-staged PRP roster (TILTH-PRP-2CFR200 / TILTH-PRP-DAVIS-BACON / TILTH-PRP-NEPA-24CFR58), the card should carry the *grammar* (what reviewers expect to see; weight-of-evidence) while the PRPs carry the *law* (current thresholds, current procurement-tier dollar amounts, current weekly-payroll mechanics, current Choice-Limiting Action blocker, current Eight-Step floodplain process). Per master prompt rule 5: live program law that updates faster than card LOCK ceremonies belongs in PRPs, not the card.

The runtime-behavior delta this card should produce versus a sector-naive baseline is **statutory-anchor density + reviewer-aware evidence prompting + PRP delegation discipline on live program law + administration-aware admin-risk handling + commitment-tracking precision on the public-works lifecycle from NTP through closeout**. The card is currently strong on (1)–(4); (5) is partially aligned with OD-A v2.4 (the three CLC-01-specific terms migrated, see §3.1); (6) needs explicit hand-off discipline added now that the active PRP manifest exists.

---

## §2. Current State Audit

### §2.1 What is strong now

- **Statutory-anchor density.** 12 `underwriting_criteria` entries each carry a CFR / agency-page `source_citation` (24 CFR 570 / 2 CFR 200 Subpart D + E + F / 7 CFR 3570 / 44 CFR Part 201 / 40 USC §3141 / Public Law 117-58 §70914 / 23 CFR 771 referenced via DOT pages). The threshold-vs-weighted distinction (`qualitative_threshold` vs `qualitative`) is consistently applied per OQ-6.
- **Audit-threshold accuracy at threshold-selector resolution.** `evidence_weights.audit_documentation.rationale` (lines 243-246) and `compliance_obligations[0].typical_filings` (line 584) both carry the legacy-vs-current threshold selector: "$750K legacy threshold for FY beginning pre-Oct-2024 with 90-day closeout per legacy §200.344; $1M current threshold for FY beginning Oct 2024+ with 120-day closeout per 2024 Uniform Guidance update." This is exactly the 2024-OMB-Final-Rule discipline a sector-naive Scribe gets wrong.
- **Sixteen common_red_flags + sixteen commitment_tracking_pattern types.** Per-flag `red_team_probe` published at lines 493-550; per-commitment `measurement_method` published at lines 666-698. Both blocks are reviewer-actionable, not framing prose.
- **Davis-Bacon + BABA severity-lift fold-in (OD-2).** Both `davis_bacon_nonresponsive` (line 529-532) and `baba_waiver_no_rationale` (lines 534-537) are HIGH severity with explicit compliance-breach reviewer-context language. Cycle-1 Thesis F7 fold closed at LOCK per `_review_handback.decision_queue[2]`.
- **Anti-coupling discipline in eligibility-criterion phrasing (OD-3).** `underwriting_criteria[0]` description (lines 43-46) — "Any entity satisfying the statutory eligibility criteria qualifies. Eligibility citation must reference the authorizing statute or program regulation, not just the NOFO. Entity types named in current federal program statutes vary by program (illustrative-only, not constraining)." — explicitly disavows archetype-driven eligibility per Cycle-1 Red Team RT-1 closure. The "illustrative-only" enumeration of entity types preserves Scout vocabulary surface without forcing CIC × CLC coupling.
- **Eleven compliance_obligations frameworks** (lines 578-660): 2 CFR 200 (Uniform Guidance) / 2 CFR 200.306 (federal-funds-as-match prohibition) / Davis-Bacon / BABA / NEPA / Section 106 NHPA / ADA / Title VI / Section 504 / FFATA / Uniform Guidance §200.344 Closeout. Each carries `applicability` + `typical_filings` + `source_citation`. Coverage is wider than any other CLC card.
- **Phase D Group A.4 cleanup precedent applied.** `underwriting_criteria[0]` comment block (lines 34-42) documents the deliberate scrub of literal "Customer Identity Card" + "CIC × CLC coupling" prose that would have failed the OD-C value-position regex. Anti-coupling intent is captured in operator-readable comments; the field description is regex-clean.
- **OD-1 path (a) workspace-register handoff closed at card.** `admin_risk_term_register` field intentionally absent at card body (lines 703-726 comment block); five CLC-01-specific terms (`disadvantaged community`, `climate resilience`, `equitable access`, `underserved`, `resilience`) routed to workspace `admin_risk_register.yaml` v2.3+. Three of those five (`disadvantaged community`, `equitable access`, `resilience`) verified present in v2.4 lines 900/911/921 with `per_clc_register.public_purpose_works` cells populated (EXPECTED / OK / EXPECTED respectively).
- **Lifecycle signed at row 255.** `draft_status: signed` / `review_status: passed` / `cross_family_thesis_status: passed` / `signature_status: signed` / `runtime_load_status: loaded` / `runtime_loadable: true` / `content_hash` present / `signed_at: 2026-05-16T16:00:00Z` / `signed_by: founder` / `lock_history_row: 255` / valid Ed25519 signature at line 866 against publisher pubkey `0b1a0bbfa5ee9149af2c4e6153ed037dd03c0d562c94d3eaefeaf798e6f375bd`.

### §2.2 What is stale, ambiguous, over-broad, too local, too federal, or under-sourced

- **Match percentages and BCA threshold encoded as card prose belong in PRPs.** `underwriting_criteria[match_committed].description` (line 74) carries FY24 baseline match percentages (CDBG entitlement 0% / USDA CF MHI-scaled / FEMA BRIC 25% non-federal / 10% tribes-disadvantaged / DOT BUILD/RAISE 20% non-federal / EDA Public Works 50% non-federal). `budget_structure_conventions.match_requirements_typical` (line 410) restates the same FY24 baselines. `evidence_weights.benefit_cost_analysis.rationale` (line 239-241) carries the FEMA BRIC BCA ≥1.0 threshold. These are program-law-cycle facts. Per master prompt rule 5 + the now-staged TILTH-PRP-2CFR200 + PRP-FEMA-BRIC-cycle (future) approach: card should carry the *grammar* ("match committed in writing from an allowable non-federal source") and *delegate threshold values to PRPs*. Current card mitigates by tagging FY24 as illustrative + adding "runtime Scout layers current-NOFO match rules" (line 74 final clause) and the `EVIDENCE WEIGHTS BASELINE NOTE` (lines 175-181) — but the per-program percentages still flow through card text. **Recommendation:** keep the qualitative criterion ("match committed; non-federal where 2 CFR 200.306 requires; allowability per active program rules") in card; soften the per-program FY24 percentages into a single sentence ("Match percentages vary 0%–50% by program and cycle; verify per active NOFO / PRP."); move the FY24 detail into either (a) the `_research_metadata.primary_sources` verbatim quotes (already done for FEMA BRIC at line 787-788; extend to CDBG / CF / DOT / EDA) and/or (b) the v0.2 PRP body for each program.
- **`scoring_weight_patterns` is editorial summary of agency rubrics, not enforced grammar.** Six rubric examples (CDBG / USDA CF / FEMA BRIC / EPA SRF / DOT BUILD-RAISE / EDA Public Works) at lines 109-170 with `threshold` vs `weighted` tags. This is genuinely useful as Scribe / Judge prior — but the rubric weights themselves are program-law that shifts NOFO-to-NOFO (the FEMA BRIC FY24 100-point structure cited at line 137 is explicitly FY24 and will be revised; FY26 BRIC NOFO unpublished as of LOCK per `surface_ambiguities[1]`). **Recommendation:** keep the card-level grammar (the six rubrics named + qualitative `threshold`/`weighted` tags) as Scout/Scribe priors; route per-cycle rubric numerics to PRP-FEMA-BRIC-FYxx / PRP-EDA-PW-FYxx as they're authored.
- **Davis-Bacon thresholds and certified-payroll mechanics belong in TILTH-PRP-DAVIS-BACON now that it exists in the active manifest.** Lines 596-602 (`compliance_obligations.Davis-Bacon`) carry "typically $2,000 for direct federal contracts; varies for federal-assistance programs" + "Posted wage decisions / certified weekly payrolls / compliance monitoring + worker interviews." Per `pipeline/program_rule_packs/_manifest/active_prps.yaml` Entry 3 (TILTH-PRP-DAVIS-BACON): the PRP will encode "the $2,000 covered-contract threshold, weekly prevailing-wage payment, the four weekly-pay compliance pathways (system modification, third-party API, weekly cash advance, weekly draw check), WH-347 weekly certified payroll, signed Statement of Compliance, three-year retention, and the $10M prime contractor certification trigger." **Recommendation:** simplify card `compliance_obligations[Davis-Bacon]` to one-sentence applicability + delegate-to-PRP pointer + cross-reference `TILTH-PRP-DAVIS-BACON`. Same pattern for `compliance_obligations[BABA]` → `TILTH-PRP-BABA-IIJA` (not yet in manifest; surface as candidate); `compliance_obligations[2 CFR 200]` → already covered by `TILTH-PRP-2CFR200`; `compliance_obligations[NEPA]` + `[Section 106]` → covered by `TILTH-PRP-NEPA-24CFR58` (HUD Part 58 piece). PRPs are draft-status today (loader raises NotImplementedError per manifest §v0.1 DRAFT NOTE), so the card cannot rely on them at runtime yet — but **the card can prepare the delegation pointer now** as a `cross_references_prp:` annotation that v0.2 first-wave loader honors.
- **`common_application_forms` carries portal-and-form-version detail that ages out.** Lines 261-321 enumerate 12 forms/portals. SF-424 family + Workspace + FEMA-GO + RD-Apply + HUD IDIS are durable platform/form references. The version field is "OMB Approved" (which is a state, not a version number) — that's fine. But OMB control numbers + revision dates would be useful for Scout if the form catalog is what Scout matches against. **Lower priority — accept.**
- **`common_portals` is duplicative with `common_application_forms`.** Lines 452-487 list 9 portals; lines 292-321 list 12 forms/portals. There's overlap (Grants.gov, FEMA-GO, HUD IDIS, RD-Apply, PA DCED, PENNVEST). The split is plausible (forms = submission artifacts; portals = where you log in) but a reviewer would expect consolidation. **Recommendation:** keep both, but cross-reference each portal entry to the forms it accepts in `common_portals[*].forms_accepted`.
- **No `Section 3 of the Housing and Urban Development Act` framework named in `compliance_obligations`.** Section 3 (24 CFR 75) is HUD-specific employment + contracting for low-income persons; applies to CDBG, HOME, Public Housing, lead-hazard projects ≥$200K. Several of the 16 common_red_flags + 16 commitment-tracking types implicitly reference Section 3 outputs (workforce hiring, sub-recipient contracting) but the framework itself isn't named. Reviewers on HUD applications will expect Section 3 acknowledgement.
- **No `Disadvantaged Business Enterprise (DBE)` / `Minority Business Enterprise (MBE)` / `Women Business Enterprise (WBE)` compliance framework.** DOT-funded construction triggers DBE program (49 CFR Part 26) explicitly; HUD CDBG-DR has its own MBE/WBE goals (24 CFR 135). The card mentions "M/W/DBE outreach approach where required" inline in `narrative_section_patterns[Procurement Approach].note` (line 376), but does not surface DBE/MBE/WBE as a discrete `compliance_obligations` framework with `applicability` + `typical_filings`.
- **No `Section 504 / 8 CFR Part 8 ADA Technical Standards` distinction.** Card cites ADA + Section 504 separately in `compliance_obligations` (lines 626-644). Useful refinement: ADA Title II (state/local government program access) vs. Title III (public accommodations) vs. ADA Standards for Accessible Design 2010 (architectural standards triggered by new construction). For BABA / IIJA programs the relevant cross-reference is 24 CFR 8 (HUD's Section 504 reg) for HUD-assisted facilities and 49 CFR 27 (DOT) for DOT-assisted. **Lower priority — accept; expand at v1.x.**
- **`scoring_weight_patterns` missing two major federal programs that intersect this CLC.** No row for **HUD Section 108 Loan Guarantee** (a federal credit instrument backed by CDBG — sometimes operates as CLC-01 + CLC-06 hybrid per L-024). No row for **FEMA Hazard Mitigation Grant Program (HMGP)** (post-disaster mitigation — distinct from BRIC pre-disaster). No row for **EPA Brownfields Assessment / Cleanup / RLF**. No row for **DOT Safe Streets and Roads for All (SS4A)** + **Reconnecting Communities (RCP)** + **Active Transportation Infrastructure Investment Program (ATIIP)** + **INFRA** + **MEGA** + **BUILD America Bureau** + **Bridge Investment Program (BIP)** + **CRP Carbon Reduction**. These are the most-active federal-funded discretionary capital programs and they're absent from the rubric-prior list. (Surfaced in `_review_handback.decision_queue[6]` at LOCK as "confirm coverage" question — this handback closes that question with the recommended additions.)
- **No `Justice40 Covered Program` framing surfaced.** Justice40 status under current administration is in flux per `surface_ambiguities[0]` at LOCK; the card already names the issue. The associated tooling (CEJST / EJScreen / SVI) does not appear in card vocabulary, only in admin-risk reviewer-context on workspace-register entries (admin_risk_register.yaml line 138-146 environmental_justice cross-reference). **Recommendation:** add CEJST + EJScreen + SVI as `underwriting_criteria[service_area_need].description` reference tools alongside census ACS (already cited at line 89).
- **No `American Rescue Plan Act (ARPA) State and Local Fiscal Recovery Funds (SLFRF)` cross-reference.** SLFRF was the largest federal-to-public-agency funding stream 2021–2024 (~$130B); many municipalities still report on remaining SLFRF balances. Public-agency CIC handback flagged the same gap for `funder_program_keywords`. On the CLC-01 funder-side: SLFRF reporting is per Treasury Final Rule 31 CFR Part 35 + SLFRF Compliance and Reporting Guidance; SLFRF intersects this CLC because municipalities use SLFRF as match on other federal programs (subject to 2 CFR 200.306 federal-funds-as-match prohibition + per-program statutory carve-outs). **Recommendation:** add `compliance_obligations[ARPA SLFRF cross-reference]` framework entry + `common_red_flags[slfrf_as_federal_match_without_carve_out]` probe.
- **Verbatim sources are PA-leaning.** `_research_metadata.primary_sources` includes PA DCED Single Application (line 850) + PENNVEST (line 855). These are operator-deployment-relevant (PA-anchored) but not universal. Per master prompt §1.3 / sibling-handback OD-G state-overlay pattern: defer to v1.x state-overlay amendment for multi-state deployment.
- **Verbatim quotes age out.** All 17 primary_sources are dated `access_date: 2026-05-15`. Wayback Machine re-verification recommended per §18.11 discipline. EPA / CEQ / DOT pages under current administration are at higher risk of restructuring.

### §2.3 Lifecycle / signature / schema concerns

- **`draft_status: signed` — no normalization needed.** Per master prompt §5: the universal lifecycle gap (draft_status reading "draft" across the on-disk roster) does NOT apply here. Direct read of `lifecycle.draft_status` (line 732) shows `"signed"`. Architecture v7.0.11 §1.5 production-load requirement is satisfied at this card. (Cross-handback note: the master prompt's claim that "every parsed runtime card currently carries `lifecycle.draft_status: draft` on disk" is stale for this card and for the other Wave 1 / Wave 2 LOCKed cards per Run 1 priors documented in sibling handbacks. Surface as `Lifecycle gap surfaced: NO` in §5 + summary block.)
- **Header comment drift.** Line 4: `# Operator review + cross-family thesis + Ed25519 signature COMPLETE.` Line 5: `# SIGNED — runtime-loadable; lifecycle truth enforced by loader preflight.` These are current at this card (post-LOCK 2026-05-16). No drift. Lines 14-20 carry "operator OQ resolutions applied" with `# Lifecycle: draft / pending / pending / unsigned / not_loaded. ed25519_signature: null.` — that line is STALE; it describes the pre-LOCK state, not the post-LOCK state. **Recommendation:** documentation-only refresh of lines 14-20 (header-comment edit; comments not in canonical bytes; no re-sign required). Bundle with content edits to avoid two ceremonies.
- **`schema_version: "1.0-clc"`.** Matches current `card_clc.schema.json` per master prompt §2 read-first item 2. No mismatch.
- **`dialect_routing_table` not present at this card.** §18.5 declares it; §18.6 does not. Card is CLC-side so the field absence is correct. (§18 v1.2 amendment re-keys the field on CIC-side; no CLC-side action needed.)
- **Embedded `ed25519_signature` LIVE at line 866** against publisher pubkey hex `0b1a0bbfa5ee9149af2c4e6153ed037dd03c0d562c94d3eaefeaf798e6f375bd` per `vault_shared/cards/publisher_pubkey.signed.yaml`. SHA3-512 canonical-bytes pin at line 863. Sig should re-validate at loader; per master prompt §8 item 4 the three OD-E-restructured CLC cards carry intentionally-stale embedded sigs — this card is NOT one of the three (no OD-E restructure; single-track shape), so the embedded sig should be live and authoritative.
- **`_review_handback.decision_queue` carries 10 entries.** Most are CLOSED at LOCK (OD-1 / OD-2 / OD-3) or v1.x backlog routed. Two are still open at this dispatch: item 6 "scoring_weight_patterns: confirm representative coverage" (addressed in §4.5 below) and item 7 "Closeout timing 120-day vs 90-day persistence on legacy awards" (addressed in §4.4 below).

### §2.4 Coupling-discipline self-audit (LIVE F-CARDS-COUPLING-VIOLATION-EXTENSION value-position regex set)

**Method.** Manual value-position scan over the full card body using the regex set from `f_cards_coupling_violation_extension.py`:

| Pattern | Description |
|---|---|
| `TILTH-CIC-\d{2}` | canonical CIC slug literal |
| `TILTH-CLC-\d{2}` | canonical CLC slug literal |
| `[Cc]apital [Ll]ogic` | capital-logic phrase |
| `[Cc]ustomer [Ii]dentity` | customer-identity phrase |

**Exempt paths:** any top-level key beginning with `_` (e.g., `_research_metadata`) + `card_id` / `tilth_cic_id` / `tilth_clc_id`.

**Results (grep transcript at `pipeline/cards/CLC/public_purpose_works.yaml`):**

| Line | Path | Match | Exempt? |
|---|---|---|---|
| 1 | (YAML header comment) | `TILTH-CLC-01` | YES — comments stripped from canonical bytes |
| 8 | (YAML header comment) | (none of 4 patterns; mentions forbidden field names in comment-prose explanation) | YES — comments stripped |
| 24 | `card_id` | `TILTH-CLC-01` | YES — exempt path |
| 28 | `tilth_clc_id` | `TILTH-CLC-01` | YES — exempt path |
| 35 | `underwriting_criteria[0]` Phase-D-cleanup comment | `"Customer Identity Card"` + `"CIC × CLC coupling"` | YES — YAML comment, stripped from canonical bytes (this is the explicit anti-coupling rationale prose preserved as comment per Cycle-1 Cycle-2 fold) |
| 761 | `_research_metadata.priors_consulted[0].path` + `extract_note` | `Capital Logic` + `TILTH-CLC-00` | YES — `_research_metadata` exempt subtree |
| 762 | `_research_metadata.priors_consulted[0].extract_note` | (Public Purpose & Works name only — no regex match) | N/A |
| 764 | `_research_metadata.priors_consulted[1].extract_note` | `TILTH-CLC-01` | YES — exempt subtree |
| 770 | `_research_metadata.priors_consulted[4].extract_note` | `TILTH-CLC-00` | YES — exempt subtree |

**Verdict — LIVE value-position regex set: 0 non-exempt findings.** Card passes.

### §2.5 Forbidden CLC-side coupling field-name scan

Grep across the file for the 6 forbidden CLC-side top-level field names (`eligible_cic_subset`, `cic_allowlist`, `cic_denylist`, `preferred_cics`, `cic_win_rate`, `cic_ranking_preferences`): all matches are in the header-comment anti-coupling-rationale block (lines 8-12), explicitly stating "this card contains NO" — i.e., in narrative-explanation prose, not as field-name positions. 0 forbidden-field-name regressions.

### §2.6 Legacy-phrase defense-in-depth scan

Grep for `[Cc]ustomer [Ii]nformation` (the operator-side working-name slip per master prompt §1): 0 hits. 0 regressions.

---

## §3. Research Findings

### §3.1 Source verification — official + primary (current card)

| URL | Type | Access date | Fields supported | Confidence |
|---|---|---|---|---|
| https://www.hud.gov/program_offices/comm_planning/cdbg | official | 2026-05-15 | CDBG national-objective + LMI benefit framing | HIGH |
| https://www.rd.usda.gov/programs-services/community-facilities/community-facilities-direct-loan-grant-program | official | 2026-05-15 | USDA RD CF essential-community-facility framing + MHI-scaled grant share | HIGH |
| https://www.fema.gov/grants/mitigation/building-resilient-infrastructure-communities | official | 2026-05-15 | FEMA BRIC pre-disaster mitigation + 25% non-federal cost share + BCA ≥1.0 | HIGH |
| https://www.fema.gov/grants/mitigation/benefit-cost-analysis | official | 2026-05-15 | FEMA BCA methodology + threshold | HIGH |
| https://www.epa.gov/cwsrf/clean-water-state-revolving-fund-cwsrf | official | 2026-05-15 | EPA CWSRF state-administered framing | HIGH |
| https://www.transportation.gov/RAISEgrants | official | 2026-05-15 | DOT BUILD/RAISE merit criteria + project readiness | HIGH |
| https://www.eda.gov/funding/programs/public-works | official | 2026-05-15 | EDA Public Works distress eligibility + CEDS alignment | HIGH |
| https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200 | official | 2026-05-15 | 2 CFR 200 Uniform Guidance | HIGH |
| https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200/subpart-D/.../section-200.317 | official | 2026-05-15 | Procurement standards 200.317-327 | HIGH |
| https://www.dol.gov/agencies/whd/government-contracts/construction | official | 2026-05-15 | Davis-Bacon Act + Related Acts | HIGH |
| https://www.whitehouse.gov/wp-content/uploads/2023/08/M-24-02-Buy-America-Implementation-Guidance-Update.pdf | official | 2026-05-15 | BABA implementation guidance | HIGH |
| https://ceq.doe.gov/laws-regulations/regulations.html | official | 2026-05-15 | NEPA regulations | HIGH |
| https://www.achp.gov/protecting-historic-properties/section-106-process | official | 2026-05-15 | Section 106 NHPA | HIGH |
| https://www.ecfr.gov/.../section-200.344 | official | 2026-05-15 | 2 CFR 200.344 Closeout (120-day window) | HIGH |
| https://www.ecfr.gov/.../subpart-F | official | 2026-05-15 | Single Audit ($1M threshold post-FY2024-10) | HIGH |
| https://dced.pa.gov/programs-funding/single-application/ | official | 2026-05-15 | PA DCED Single Application | HIGH |
| https://www.pennvest.pa.gov/ | official | 2026-05-15 | PENNVEST PA water/wastewater SRF | HIGH |

17 primary sources; all official .gov + .pa.gov; all access_date 2026-05-15; all ≤2-sentence verbatim quotes per OQ-4.

### §3.2 New / refreshed sources to verify and add

| URL | Type | Why add | Card fields it would support | Confidence |
|---|---|---|---|---|
| https://www.hud.gov/section3 (or 24 CFR Part 75) | official | Section 3 framework (low-income hiring/contracting on HUD-funded projects ≥$200K) not currently named | New `compliance_obligations[Section 3 of HUD Act]` entry | HIGH |
| https://www.transportation.gov/civil-rights/disadvantaged-business-enterprise | official | DBE program 49 CFR Part 26 — DOT-funded construction requires DBE; absent from compliance_obligations | New `compliance_obligations[DBE/MBE/WBE]` entry | HIGH |
| https://www.hud.gov/program_offices/comm_planning/section_108 | official | HUD Section 108 Loan Guarantee — credit instrument backed by CDBG; absent from `scoring_weight_patterns` | New `scoring_weight_patterns[HUD Section 108]` entry | HIGH |
| https://www.fema.gov/grants/mitigation/hazard-mitigation | official | FEMA HMGP (post-disaster mitigation) — distinct from BRIC; absent from rubric-prior list | New `scoring_weight_patterns[FEMA HMGP]` entry | HIGH |
| https://www.transportation.gov/grants/ss4a | official | DOT SS4A (Safe Streets and Roads for All) — major IIJA-era discretionary program; absent | New `scoring_weight_patterns[DOT SS4A]` entry | HIGH |
| https://www.transportation.gov/grants/reconnecting-communities | official | DOT Reconnecting Communities Pilot (RCP) — major IIJA program; absent | New `scoring_weight_patterns[DOT RCP]` entry | HIGH |
| https://www.transportation.gov/buildamerica/financing/infra-grants | official | DOT INFRA (Multimodal Project Discretionary Grant) — major IIJA capital program; absent | New `scoring_weight_patterns[DOT INFRA]` entry | MEDIUM |
| https://www.epa.gov/brownfields | official | EPA Brownfields Assessment + Cleanup + RLF — major EPA public-works program; absent | New `scoring_weight_patterns[EPA Brownfields]` entry | HIGH |
| https://www.fema.gov/grants/mitigation/swift-current | official | FEMA Swift Current (BRIC subprogram for already-flooded NFIP properties) — newer; absent | Cross-reference under FEMA BRIC rubric note | MEDIUM |
| https://home.treasury.gov/policy-issues/coronavirus/.../state-and-local-fiscal-recovery-funds | official | ARPA SLFRF as federal-funds-as-match cross-reference | New compliance_obligations entry + new common_red_flag | MEDIUM (program closing out; relevance through reporting tail) |
| https://www.epa.gov/ejscreen | official | EJScreen — Justice40 covered-program disadvantaged-community tool; not in card | `underwriting_criteria[service_area_need]` reference + cross-ref to workspace admin_risk_register entries | HIGH |
| https://screeningtool.geoplatform.gov/en/ | official | CEJST (Climate and Economic Justice Screening Tool) — same | Same | HIGH |
| https://www.atsdr.cdc.gov/placeandhealth/svi/index.html | official | CDC SVI — same | Same | HIGH |
| https://www.hud.gov/program_offices/cpd/environment/laws-and-regulations/laws/nepa | official | HUD 24 CFR Part 58 (HUD-Responsible-Entity NEPA) — distinct from CEQ NEPA; central to CDBG | New `compliance_obligations` cross-reference (or PRP delegation) | HIGH |
| https://www.govinfo.gov/content/pkg/FR-2024-04-22/pdf/2024-07496.pdf | official | 2024 Uniform Guidance Final Rule full text — supports the audit threshold + closeout window discipline already in card | Strengthens `evidence_weights.audit_documentation.source_citation` | HIGH |
| https://www.naco.org/ | practitioner | NACo (counties) — cross-reference for county-applicant practice | Optional `_research_metadata.priors_consulted` | LOW |
| https://www.nlc.org/ | practitioner | NLC (cities) — same | Optional priors_consulted | LOW |

### §3.3 PRP-cross-reference integrity (master prompt rule 5)

Per `pipeline/program_rule_packs/_manifest/active_prps.yaml` (loader at v0.1 raises NotImplementedError; entries draft-status; v0.2 first-wave graduation paired with cards-loader graduation):

| PRP ID | Card content currently overlapping the PRP scope | Recommendation |
|---|---|---|
| TILTH-PRP-2CFR200 | `compliance_obligations[2 CFR Part 200]` (line 579-586); `underwriting_criteria[allowable_use]` (line 58-61); `underwriting_criteria[procurement_compliance]` (line 68-71); `budget_structure_conventions.indirect_cost_treatment` (line 409) | Annotate card entries with `cross_references_prp: TILTH-PRP-2CFR200` (v0.2 first-wave loader will honor); keep card grammar; soften per-tier-dollar-amounts |
| TILTH-PRP-DAVIS-BACON | `compliance_obligations[Davis-Bacon Act]` (line 596-602); `underwriting_criteria[procurement_compliance]` Davis-Bacon clause; `common_red_flags[davis_bacon_nonresponsive]` (line 529-532); `evidence_weights[davis_bacon_compliance_certification]` (line 248-251); `commitment_tracking_pattern[davis_bacon_payrolls_filed]` (line 683-684) | Annotate with `cross_references_prp: TILTH-PRP-DAVIS-BACON`; keep card grammar; soften weekly-payroll mechanics into PRP scope |
| TILTH-PRP-NEPA-24CFR58 | `compliance_obligations[NEPA]` (line 611-616); `compliance_obligations[Section 106 NHPA]` (line 618-624); `underwriting_criteria[environmental_review_pathway]` (line 98-101); `evidence_weights[environmental_review_pathway]` (line 229-232); `common_red_flags[no_nepa_pathway]` (line 524-527); `narrative_section_patterns[Environmental Review / NEPA]` (line 358-361) | Annotate with `cross_references_prp: TILTH-PRP-NEPA-24CFR58`; surface the Choice-Limiting Action Blocker pattern as a new common_red_flag entry pending PRP-go-live |
| TILTH-PRP-FERPA-COPPA-HIPAA | (not applicable to public_purpose_works) | N/A — CIC-02 educator concern |
| TILTH-PRP-SUBCHAPTER-T | (not applicable to public_purpose_works directly; applicable when applicant entity is a cooperative pursuing public-works funding — but underwriting logic stays per this CLC) | N/A — CLC-05/06/07 cooperative cross-reference |
| TILTH-PRP-USDA-VAPG-FY26 | (program-specific exemplar — not in this CLC scope) | N/A — CIC-01 food_systems / CLC-05 market_access concern |

**PRP candidate not yet in manifest:** TILTH-PRP-BABA-IIJA (Build America Buy America Act implementation: PL 117-58 §70914 + 2 CFR 184 + OMB M-22-11 / M-24-02 — covers iron/steel/manufactured-products/construction-materials sourcing + waiver pathways + agency-specific implementation memos). Surfaces at scale on every federal-assistance infrastructure project; high enough cross-cycle volatility (agency memos update annually) to belong in a PRP not card body. Surface to operator as PRP roster expansion candidate.

### §3.4 Internet Archive snapshot verification

Recommended for next Phase 4-CLC re-pass: verify Wayback Machine snapshots of all 17 primary_sources URLs. EPA / CEQ / DOT URLs are at elevated risk of restructuring under current administration. HUD CDBG + USDA RD Community Facilities pages are relatively stable. Treasury SLFRF page is in close-out phase.

---

## §4. Proposed Card Improvements

Grouped by master prompt §2 "Research task" runtime-behavior categories. Each proposal: exact YAML path, why-it-improves-runtime, target-seat, and where-it-belongs (card body vs PRP vs admin-risk-register vs funder DB vs matrix-layer-v1.x). Phase 4 fold-in discipline self-check at the end of §4.

### §4.1 search vocabulary / classification (CLC = underwriting_criteria + reviewer_profile_typical + common_red_flags vocabulary)

- **`underwriting_criteria[service_area_need].description[REFINE]`** (line 89). Add CEJST + EJScreen + CDC SVI alongside existing "census ACS / hazard maps / water quality reports / transportation crash data / broadband-availability data" enumeration. New phrasing: "Documented need in the defined service area using objective data — census ACS, EPA EJScreen indicators, CEJST disadvantaged-community designation (where Justice40-covered programs apply per active RFA), CDC Social Vulnerability Index, hazard maps, water quality reports, transportation crash data, broadband-availability data. Disadvantaged-community designation (Justice40 covered programs) where applicable; LMI-area benefit math for CDBG; rural/distressed designation for USDA RD." **Seat:** Scout + Scribe. **Where:** card body. **Source:** see §3.2 (EJScreen / CEJST / CDC SVI URLs).
- **`reviewer_profile_typical.reviewer_priorities[NEW]`** (line 427-434). Add: "Is the project aligned with disadvantaged-community-investment scoring (per Justice40 covered-program status as of active RFA), where applicable?" — explicit named reviewer-priority for Justice40-era weighted scoring. **Seat:** Scribe. **Where:** card body.
- **`reviewer_profile_typical.common_red_flags_from_reviewer_pov[NEW]`** (line 436-446). Add: "Cost-share certification fraud — claimed match source that is itself federal without statutory carve-out, OR claimed cash match that proves to be in-kind valuation, OR claimed third-party contribution without signed commitment letter." Reviewer-POV mirror of the cost-share-fraud category named in the operator's CLC-specific focus area for this dispatch. **Seat:** Scribe + Logician. **Where:** card body.
- **`reviewer_profile_typical.common_red_flags_from_reviewer_pov[NEW]`** (line 436-446). Add: "Federal-funds-as-match disclosure absent — applicant invokes another federal source as match without naming the statutory carve-out (which 2 CFR 200.306 requires)." Pairs with new `common_red_flag[federal_funds_as_match_undisclosed]` below. **Seat:** Logician. **Where:** card body.

### §4.2 evidence capture / missing-evidence prompts

- **`evidence_weights[NEW]` — add `slfrf_match_disclosure`.** weight = MEDIUM. rationale = "When applicant invokes ARPA SLFRF balance as match on another federal program, 2 CFR 200.306 federal-funds-as-match prohibition applies unless a statutory carve-out is named. SLFRF Final Rule (31 CFR Part 35) permits SLFRF-as-match on specific eligible categories (Treasury guidance updated periodically); applicant must cite the carve-out, not assume. Reviewer expects either (a) explicit statutory carve-out citation OR (b) non-federal match source." source_citation = "https://home.treasury.gov/policy-issues/coronavirus/assistance-for-state-local-and-tribal-governments/state-and-local-fiscal-recovery-funds". **Seat:** Scribe + Logician. **Where:** card body.
- **`evidence_weights[NEW]` — add `section_3_compliance_plan`.** weight = MEDIUM. rationale = "HUD-funded construction projects ≥$200,000 trigger Section 3 (24 CFR Part 75) low-income hiring + contracting requirements. Reviewer expects Section 3 plan + numerical hiring/contracting goals + sub-recipient flow-down language." source_citation = "https://www.hud.gov/section3". **Seat:** Scribe + Logician. **Where:** card body. **Applicability gate:** fire only when funder is HUD or HUD-pass-through AND project_category includes construction.
- **`evidence_weights[NEW]` — add `dbe_mbe_wbe_outreach_plan`.** weight = MEDIUM. rationale = "DOT-funded construction triggers DBE compliance (49 CFR Part 26): annual DBE goal-setting, race-conscious / race-neutral methods, sub-contractor outreach documentation, DBE Directory consultation. CDBG-DR triggers parallel MBE/WBE goals (24 CFR 135). Reviewer expects DBE plan + outreach evidence." source_citation = "https://www.transportation.gov/civil-rights/disadvantaged-business-enterprise". **Seat:** Scribe + Logician. **Where:** card body. **Applicability gate:** funder = DOT (DBE) or HUD CDBG-DR (MBE/WBE) AND project_category = construction.
- **`evidence_weights[REFINE]` — `davis_bacon_compliance_certification`** (line 248-251). Add cross-reference: "PRP TILTH-PRP-DAVIS-BACON encodes covered-contract threshold mechanics (currently $2,000 for direct contracts), four weekly-pay compliance pathways, WH-347 weekly certified payroll, signed Statement of Compliance, three-year retention, and $10M prime contractor certification trigger; card-level weight stays MEDIUM as evidence-prompt anchor." **Seat:** Logician. **Where:** card body (annotation to existing entry).
- **`evidence_weights[REFINE]` — `baba_compliance_plan`** (line 253-256). Same pattern: annotate to declare PRP cross-reference once TILTH-PRP-BABA-IIJA is in the manifest (currently not). Until then, card carries the evidence prompt at MEDIUM weight per current published content.
- **`evidence_weights[REFINE]` — `environmental_review_pathway`** (line 229-232). Annotate: "PRP TILTH-PRP-NEPA-24CFR58 (HUD Responsible-Entity NEPA layer) encodes the Choice-Limiting Action Blocker, the five review classifications (Exempt, CENST, CEST, EA, EIS), CEST 7-day comment + 15-day objection, EA 15-day comment + 15-day objection, Certifying Officer personal liability, and the Eight-Step floodplain Decision-Making Process; card-level weight stays HIGH as evidence-prompt anchor."

### §4.3 KFR fact classes + provenance (CLC-side: scoring weight patterns + evidence weights serve this role; per master prompt §2)

- **`scoring_weight_patterns[NEW]` — add 5 federal-program rubric entries:** HUD Section 108 Loan Guarantee / FEMA HMGP / DOT SS4A / DOT Reconnecting Communities Pilot / EPA Brownfields. Each follows the existing 6-entry pattern: `rubric_example`, `weights` map (threshold/weighted tags only — no numeric per-cycle weights per OQ-6), `source_citation`, `note`. URLs per §3.2. **Seat:** Scribe + Judge. **Where:** card body. **Closes `_review_handback.decision_queue[6]` "scoring_weight_patterns: confirm representative coverage" item.**
- **`scoring_weight_patterns[REFINE]` — `FEMA BRIC FY24`** (lines 129-138). Soften to "FEMA BRIC (current-cycle structure varies; FY24 baseline 100-point qualitative-and-technical structure cited as reference)" + add `note` line: "FY26 NOFO unpublished as of 2026-05-16 LOCK; PRP-FEMA-BRIC-FYxx (when authored) carries cycle-specific weights + cost-share + disadvantaged-community designation." **Seat:** Scribe. **Where:** card body.

### §4.4 drafting register / admin-risk handling (Law 4 + OD-A v2.4)

- **OD-A v2.4 register cross-check (CLC-01-side).** Three CLC-01-specific terms verified present in workspace register at lines 900-927: `disadvantaged community` (GREEN; EXPECTED for public_purpose_works), `equitable access` (GREEN; OK for public_purpose_works), `resilience` (GREEN; EXPECTED for public_purpose_works). Two of the original five CLC-01-specific terms named in card comment block (lines 717-721) are NOT yet visible at v2.4: `climate resilience` is at line 576 (v2.1-era YELLOW entry; per_clc_register cell for public_purpose_works not yet added) and `underserved` is at line 363 (v2.1-era entry; same gap). **Recommendation:** route the two missing `per_clc_register` cell additions to the OD-A v2.x → v3.0 scrub workflow per master prompt §7. This is a workspace-register update (not a card-body update); the card-body comment block at lines 715-722 is correct documentation; no card-body action needed beyond confirming the gap was surfaced.
- **`common_red_flags[NEW]` — add `flag: "federal_funds_as_match_undisclosed"`.** severity: HIGH. red_team_probe: "If match source is itself a federal program (e.g., ARPA SLFRF balance, CDBG-DR, prior FEMA award, USDA RD loan), where is the statutory carve-out citation that permits federal-funds-as-match? 2 CFR 200.306 prohibits federal-as-match by default; carve-outs are per-program-statute and must be cited explicitly." source_citation: "https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200/subpart-D/subject-group-ECFRf78b8bb6dffa70d/section-200.306". **Seat:** Logician + Red Team. **Where:** card body.
- **`common_red_flags[NEW]` — add `flag: "cost_share_certification_fraud"`.** severity: HIGH. red_team_probe: "Does the match certification reflect actual committed source — signed commitment letter (cash) OR board-resolution-backed valuation (in-kind) — OR does it overstate planned-but-unsecured contributions? Cost-share misrepresentation is a False Claims Act exposure (31 USC §3729) and a HIGH compliance breach in federal-construction audit cycles." source_citation: "https://www.justice.gov/civil/false-claims-act". **Seat:** Logician + Red Team. **Where:** card body.
- **`common_red_flags[NEW]` — add `flag: "nepa_skip_or_premature_action"`.** severity: HIGH. red_team_probe: "Has the applicant committed to a 'Choice-Limiting Action' (24 CFR 58.22) before NEPA finding is issued — site purchase, demolition, construction start, contract execution? Choice-Limiting Action Blocker is fail-closed: HUD will deny clearance and reclaim funds if applicant skips. For non-HUD programs (USDA 7 CFR 1970, DOT 23 CFR 771), parallel agency-specific NEPA-skip blockers apply." source_citation: "https://www.ecfr.gov/current/title-24/subtitle-A/part-58/subpart-A/section-58.22". **Seat:** Logician + Red Team. **Where:** card body. **PRP cross-reference:** TILTH-PRP-NEPA-24CFR58.
- **`common_red_flags[NEW]` — add `flag: "davis_bacon_weekly_payroll_gap"`.** severity: HIGH. red_team_probe: "Are certified weekly payrolls (WH-347) filed by every covered contractor + subcontractor on every weekly cycle from project start through final acceptance — including weeks with zero hours worked? Weekly-payroll-gap risk is HIGH on small-jurisdiction applicants whose accounting systems do weekly-payroll-batch-process not weekly-payroll-by-contract; one missed week is a Davis-Bacon violation with prevailing-wage backpay + civil penalty exposure." source_citation: "https://www.dol.gov/agencies/whd/government-contracts/construction". **Seat:** Logician + Red Team. **Where:** card body. **PRP cross-reference:** TILTH-PRP-DAVIS-BACON.
- **`common_red_flags[NEW]` — add `flag: "section_3_silence_on_hud_construction"`.** severity: MEDIUM. red_team_probe: "On HUD-funded construction ≥$200K, has applicant published Section 3 hiring + contracting goals + outreach plan + sub-recipient flow-down language? Section 3 silence on HUD construction is a routine reviewer find that delays award but rarely disqualifies (corrective action available)." source_citation: "https://www.hud.gov/section3". **Seat:** Logician. **Where:** card body. **Applicability gate:** funder = HUD or HUD-pass-through AND project_category = construction.

### §4.5 reviewer / rubric logic

- **`scoring_weight_patterns[NEW]` rubric additions** per §4.3 above. Closes `_review_handback.decision_queue[6]`.
- **`reviewer_profile_typical.reviewer_types[NEW]`** (line 418-426). Add: `"buy_america_compliance_reviewer"`, `"davis_bacon_wage_determination_reviewer"`, `"section_3_compliance_reviewer"`. These are discrete federal-reviewer roles that show up on agency review panels for federally-assisted construction. **Seat:** Scribe. **Where:** card body.

### §4.6 red-team probes / common_red_flags (already covered in §4.4)

Five new red_team_probes added (federal-funds-as-match undisclosed / cost-share certification fraud / NEPA-skip / Davis-Bacon weekly-payroll gap / Section 3 silence on HUD construction). All carry the operator-CLC-focus areas surfaced in the dispatch prompt.

### §4.7 reporting / commitment_tracking_pattern

- **`commitment_tracking_pattern.typical_commitments_extracted[NEW]` — add `commitment_type: "civic_benefit_reporting"`.** measurement_method = "Per-program civic-benefit metric reporting (CDBG: LMI beneficiaries served + national-objective compliance; FEMA BRIC: lifeline beneficiaries + risk-reduction quantification; DOT BUILD/RAISE: per-mode mobility + safety performance; EDA Public Works: jobs created/retained + private-investment leveraged; EPA SRF: water-quality compliance + service connections); report frequency per program (typically annual; quarterly for some)." **Seat:** Report Generator + Archivist. **Where:** card body.
- **`commitment_tracking_pattern.typical_commitments_extracted[NEW]` — add `commitment_type: "built_asset_commissioning"`.** measurement_method = "Beneficial-use certificate or equivalent: commissioning report for facility/system (water plant commissioning, transit-asset acceptance, bridge load-test, broadband network acceptance, building TCO occupancy). Pairs with `construction_milestone_final_acceptance` (existing line 671-672)." **Seat:** Report Generator. **Where:** card body.
- **`commitment_tracking_pattern.typical_commitments_extracted[NEW]` — add `commitment_type: "section_3_workforce_outcomes"`.** measurement_method = "HUD Section 3 hiring + contracting outcomes (low-income hires placed by sub-recipient; Section-3-eligible contracts awarded + sub-contracted; goal-attainment percentage)." **Seat:** Report Generator. **Where:** card body. **Applicability gate:** HUD-funded only.
- **`commitment_tracking_pattern.typical_commitments_extracted[NEW]` — add `commitment_type: "dbe_mbe_wbe_outcomes"`.** measurement_method = "DOT DBE goal-attainment / HUD MBE/WBE goal-attainment (race-conscious + race-neutral methods broken out per DOT 49 CFR 26 reporting cycle)." **Seat:** Report Generator. **Where:** card body.

### §4.8 memory namespace usefulness (per architecture v7.0.11 §1.9)

Standard sub-key map mirroring food_systems / public_agency pattern (re-stated for completeness; v0.2 first-wave loader concern):

- `cards:clc:public_purpose_works:underwriting_criteria`
- `cards:clc:public_purpose_works:scoring_weight_patterns`
- `cards:clc:public_purpose_works:evidence_weights`
- `cards:clc:public_purpose_works:common_application_forms`
- `cards:clc:public_purpose_works:narrative_section_patterns`
- `cards:clc:public_purpose_works:budget_structure_conventions`
- `cards:clc:public_purpose_works:reviewer_profile_typical`
- `cards:clc:public_purpose_works:common_portals`
- `cards:clc:public_purpose_works:common_red_flags`
- `cards:clc:public_purpose_works:reporting_requirements_typical`
- `cards:clc:public_purpose_works:compliance_obligations`
- `cards:clc:public_purpose_works:commitment_tracking_pattern`
- `cards:clc:public_purpose_works:prp_cross_references` *(new sub-key for the PRP-delegation annotations proposed in §4.2 + §4.4)*

**Seat:** all consuming seats. **Where:** architecture v7.0.11 §1.9 sets the namespace pattern; per-card sub-key map is v0.2 loader-graduation concern.

### §4.9 PRP-delegation annotations (master prompt rule 5 — new card-side discipline)

- **NEW card-side field-pattern recommendation — `cross_references_prp:` annotation on five existing entries:**
  - `compliance_obligations[2 CFR Part 200]` → `cross_references_prp: TILTH-PRP-2CFR200`
  - `compliance_obligations[Davis-Bacon Act]` → `cross_references_prp: TILTH-PRP-DAVIS-BACON`
  - `compliance_obligations[NEPA]` + `compliance_obligations[Section 106 NHPA]` → `cross_references_prp: TILTH-PRP-NEPA-24CFR58`
  - `evidence_weights[davis_bacon_compliance_certification]` → `cross_references_prp: TILTH-PRP-DAVIS-BACON`
  - `evidence_weights[environmental_review_pathway]` → `cross_references_prp: TILTH-PRP-NEPA-24CFR58`
  - `common_red_flags[no_nepa_pathway]` + `[nepa_skip_or_premature_action]` (new) → `cross_references_prp: TILTH-PRP-NEPA-24CFR58`
  - `common_red_flags[davis_bacon_nonresponsive]` + `[davis_bacon_weekly_payroll_gap]` (new) → `cross_references_prp: TILTH-PRP-DAVIS-BACON`

  **Phase 4 fold-in discipline self-check on `cross_references_prp:` as a NEW field-name:** This is a new structured-sub-field on canonical entries (refusal `(a)` territory per §18.11 v1.1) AND it is a dedicated field-name (refusal `(b)` territory). **It MUST be routed as a §18 v1.x amendment candidate per master prompt rule 6 fallback** — surface as YAML comment on the card during the next supersession ceremony, AND route the structural gap to `_review_handback.decision_queue` for a §18 v1.x amendment that adds `cross_references_prp: list[str]` to the `card_clc.schema.json` item shapes. Do NOT bake the new field into card body silently. Document the proposal in the comment-block-only fallback per master prompt rule 6 (precedent: CLC-06 + CLC-08 Wave 2 use of this pattern). **Seat:** Logician + Report Generator (when PRP-graduation lands at v0.2 first wave). **Where:** comment block now; card body + schema after §18 v1.x amendment.

### §4.10 Phase 4 fold-in discipline self-check (per master prompt rule 6 / §18.11 v1.1)

| Proposal | (a) structured-sub-field expansion? | (b) dedicated-field-name fork? | (c) compound enum value? | (d) literal canonical CIC/CLC slug in non-exempt value position? |
|---|---|---|---|---|
| §4.1 `underwriting_criteria[service_area_need]` refine (EJScreen / CEJST / SVI) | NO — refines description prose | NO | NO | NO |
| §4.1 `reviewer_profile_typical.reviewer_priorities` + `common_red_flags_from_reviewer_pov` additions | NO | NO | NO | NO |
| §4.2 `evidence_weights[NEW]` slfrf / section_3 / dbe_mbe_wbe entries | NO — adds new items at canonical item shape | NO | NO | NO |
| §4.2 `evidence_weights[REFINE]` PRP cross-reference annotations (prose only, no new field-name) | NO — refines rationale prose only | NO | NO | NO |
| §4.3 `scoring_weight_patterns[NEW]` 5 rubric entries | NO | NO | NO | NO |
| §4.3 `scoring_weight_patterns[REFINE]` FEMA BRIC FY24 softening | NO | NO | NO | NO |
| §4.4 `common_red_flags[NEW]` 5 new probes | NO | NO | NO — uses canonical HIGH/MEDIUM | NO |
| §4.5 `reviewer_profile_typical.reviewer_types[NEW]` three additions | NO | NO | NO | NO |
| §4.7 `commitment_tracking_pattern.typical_commitments_extracted[NEW]` 4 additions | NO | NO | NO | NO |
| §4.8 memory namespace sub-keys | N/A — architecture decision, not card body | N/A | N/A | N/A |
| **§4.9 `cross_references_prp:` new field-name** | **YES — refusal (b) territory** | **YES — refusal (b) territory** | NO | NO |

**Verdict:** All proposals except §4.9 PRP cross-reference field pass cleanly. §4.9 trips refusals (a) + (b) and is routed per master prompt rule 6 fallback: comment-block-only on card now; structural gap surfaces to `_review_handback.decision_queue` for §18 v1.x amendment (precedent: CLC-06 + CLC-08 Wave 2 use of comment-block-only fallback). **Per master prompt §0:** no LOCKed-file edits; the proposal stays in this handback as recommendation only.

---

## §5. Operator Decision Queue

1. **PRP-delegation annotation field (`cross_references_prp:`) — §18 v1.x amendment candidate.** Per §4.9 self-check, this is a refusal-(a)+(b)-territory proposal that must be routed as an amendment, not a silent card-body edit. **Decision:** approve §18 v1.x amendment dispatch to add `cross_references_prp: list[str]` to `card_clc.schema.json` item shapes for `compliance_obligations[*]`, `evidence_weights[*]`, `common_red_flags[*]`? OR keep PRP-card linkage as comment-only narrative until v0.2 first-wave PRP loader-graduation lands and the integration shape is concrete?
2. **TILTH-PRP-BABA-IIJA roster addition.** Currently absent from `pipeline/program_rule_packs/_manifest/active_prps.yaml`. BABA is a major federal-assistance infrastructure law (Public Law 117-58 §70914) with annually-shifting OMB implementation guidance (M-22-11, M-24-02, future memos) and agency-specific implementation memos. **Decision:** add TILTH-PRP-BABA-IIJA to the v0.2 first-wave manifest? (Handoff drafted at next dispatch — not initiated here per §0 no-LOCK-ceremony rule.)
3. **Match percentage softening per master prompt rule 5.** Current card carries FY24 per-program match percentages in `underwriting_criteria[match_committed].description` (line 74) + `budget_structure_conventions.match_requirements_typical` (line 410). Recommendation: soften to one qualitative sentence per location + delegate per-program numerics to PRP-FEMA-BRIC-FYxx / PRP-EDA-PW-FYxx / PRP-CDBG-FYxx (none in current manifest). **Decision:** approve softening now (per §4.2 PRP-cross-reference annotation precedent) OR defer until per-program PRPs are authored?
4. **`scoring_weight_patterns` rubric coverage (closes `_review_handback.decision_queue[6]`).** Five recommended additions per §4.3: HUD Section 108 Loan Guarantee / FEMA HMGP / DOT SS4A / DOT Reconnecting Communities Pilot / EPA Brownfields. **Decision:** approve all five additions? Surface other gaps (FHWA STBG / Army Corps Section 14/22 named in `_review_handback.decision_queue[6]`)?
5. **Closeout-timing legacy persistence (closes `_review_handback.decision_queue[7]`).** Card carries the explicit threshold selector ($750K legacy / $1M current; 90-day legacy / 120-day current closeout window) per evidence_weights line 245 + compliance_obligations lines 584 / 657-659. **Decision:** is the current text adequate, OR should compliance_obligations[Uniform Guidance §200.344 Closeout] (lines 653-660) carry the explicit per-FY-applicability statement ("90-day closeout applies to awards issued under pre-2024 UG version; 120-day closeout applies to awards issued under 2024-update UG version; legacy awards retain their original closeout terms")?
6. **OD-A v2.4 per_clc_register gap for `climate resilience` + `underserved`.** Two of the five CLC-01-specific terms named in card lines 717-721 are not yet visible in v2.4 workspace register with `per_clc_register.public_purpose_works` cell. **Decision:** route to v2.x → v3.0 scrub workflow per master prompt §7? (Separate operator-approval-token flow per Wave 2 OD-A precedent.)
7. **Five new common_red_flags additions (§4.4 + §4.6).** federal-funds-as-match undisclosed / cost-share certification fraud / NEPA-skip / Davis-Bacon weekly-payroll gap / Section 3 silence on HUD construction. **Decision:** approve all five? Each adds Logician + Red Team probe coverage; each is sourceable to a primary URL per §3.2.
8. **Four new commitment_tracking_pattern types (§4.7).** civic_benefit_reporting / built_asset_commissioning / section_3_workforce_outcomes / dbe_mbe_wbe_outcomes. **Decision:** approve all four? Each feeds Report Generator (v0.2 horizon).
9. **CEJST + EJScreen + SVI in `underwriting_criteria[service_area_need]`** per §4.1. **Decision:** approve administration-status-dependency-aware addition (text accommodates Justice40-covered-program status varying RFA-to-RFA)?
10. **State-overlay for PA-specific entries** (PA DCED Single Application at line 850; PENNVEST at line 855; `common_portals[PA DCED]` at line 481; `common_portals[eCivis]` at line 485; `common_application_forms[PA DCED Single Application]` at line 307; `common_application_forms[PA DEP eFACTS / PENNVEST]` at line 312). Per master prompt §1.3 + OD-G state-overlay pattern. **Decision:** keep in base card per current Wave 2 precedent OR extract to PA-state overlay at v1.x?
11. **Re-signing ceremony budget for card body changes.** Per §5 items 4 + 7 + 8 + 9: ~18 distinct content edits. Bundle into single supersession-re-sign ceremony per OD-E precedent (parent_lock_row = 255). **Decision:** approve bundled ceremony OR sequence as separate dispatches?

---

## §6. Validation Checklist

| Check | Result | Evidence |
|---|---|---|
| Schema fields complete against current §18.6 schema | PASS | 13/13 required CLC fields present per `card_clc.schema.json` |
| No forbidden coupling field names (top-level + nested-in-item not.anyOf) | PASS | Grep across file: none of 6 forbidden CLC-side names (`eligible_cic_subset`, `cic_allowlist`, `cic_denylist`, `preferred_cics`, `cic_win_rate`, `cic_ranking_preferences`) appear as field positions; the two header-comment matches at lines 8-9 are inside the explicit anti-coupling rationale prose ("this card contains NO …") |
| No forbidden value-position regex matches outside exempt paths | PASS | §2.4 — 0 non-exempt findings; all hits in `card_id` / `tilth_clc_id` / header comments / `_research_metadata` exempt subtree |
| No legacy-phrase `[Cc]ustomer [Ii]nformation` matches | PASS | 0 hits |
| No private organization-specific data in card body | PASS | No org-specific PII; PA-anchored portals are public state-portal references |
| No unsourced program-law claims at body | PARTIAL — see §2.2 + §5 item 3 | FY24 per-program match percentages and FEMA BRIC FY24 100-point structure are program-law cited in card prose; current card mitigates with "verify per active NOFO" disclaimers + the EVIDENCE WEIGHTS BASELINE NOTE block; full delegation to PRPs is the recommended improvement |
| No excessive verbatim source text | PASS | Per OQ-4: 17 primary_sources with ≤2-sentence verbatim quotes |
| Lifecycle status consistent with architecture v7.0.11 §1.5 | PASS | `draft_status: signed` + `signature_status: signed` + `runtime_load_status: loaded` + `runtime_loadable: true` + `content_hash` + `signed_at` + `signed_by` + `lock_history_row` all present and valid |
| Track-shape compliance (single_track) | PASS | No `track_a` / `track_b` containers; oneOf branch 1 (single-track legacy) compliance verified |

**Net coupling-discipline regression: 0 findings.**

---

## §7. Regression Tests

### Test 1 — Borough water/wastewater + CDBG-State + PennVEST stacking

**Prompt:** "PA borough, population 6,500, applying for combined CDBG-State (water-system upgrade component) + PennVEST loan (wastewater treatment plant capacity upgrade). Project includes federal-assistance construction triggering Davis-Bacon, BABA, NEPA, and CDBG Section 3."

**Pre-edit behavior:** Scribe drafts CDBG narrative + PennVEST narrative; Logician fires existing Davis-Bacon + BABA + NEPA + procurement red_team_probes. Logician does NOT fire `nepa_skip_or_premature_action` Choice-Limiting Action probe (not present); does NOT fire `davis_bacon_weekly_payroll_gap` probe (not present); does NOT surface Section 3 evidence prompt (no `section_3_compliance_plan` evidence weight).

**Post-edit (with §4.2 + §4.4 additions):** Logician fires `section_3_compliance_plan` evidence prompt on the CDBG-State portion (HUD-pass-through trigger). Logician fires `nepa_skip_or_premature_action` probe (Choice-Limiting Action discipline). Logician fires `davis_bacon_weekly_payroll_gap` probe (small-borough accounting-system risk). Scribe drafts with Section 3 plan + Davis-Bacon-weekly-discipline acknowledgement + Choice-Limiting-Action commitment.

**Seat:** Scribe + Logician + Red Team. **Pass criterion:** Section 3 + Choice-Limiting-Action + Davis-Bacon-weekly probes all fire; Scribe surfaces each in narrative.

### Test 2 — County BRIC application with ARPA SLFRF match

**Prompt:** "Rural Pennsylvania county applying to FEMA BRIC for stormwater + hazard-mitigation infrastructure (population 28K; previously experienced 2 federally-declared floods 2020-2024). County intends to use $750K remaining ARPA SLFRF balance as the 25% non-federal cost share."

**Pre-edit behavior:** Scribe drafts FEMA BRIC narrative with BCA. Existing `evidence_weights[match_commitment_letter]` (HIGH) prompts for cash-match commitment. Logician does NOT fire SLFRF-as-match disclosure probe (not present); does NOT fire `federal_funds_as_match_undisclosed` red_team probe (not present).

**Post-edit (with §4.2 + §4.4 additions):** Logician fires `slfrf_match_disclosure` evidence prompt: "ARPA SLFRF as match requires 2 CFR 200.306 carve-out citation; SLFRF Final Rule (31 CFR Part 35) permits SLFRF-as-match in specific categories — cite the carve-out." Logician fires `federal_funds_as_match_undisclosed` red_team probe. Scribe surfaces the Treasury SLFRF Final Rule carve-out citation OR escalates to operator that SLFRF-as-FEMA-match needs explicit Treasury permission.

**Seat:** Scribe + Logician + Red Team. **Pass criterion:** SLFRF-as-match disclosure probe fires; statutory carve-out citation surfaced in narrative OR operator escalation triggered.

### Test 3 — DOT BUILD/RAISE application with DBE compliance gap

**Prompt:** "Regional planning commission applying for DOT BUILD/RAISE multimodal capital project (~$15M total, $12M federal request). RPC has prior DBE goal-attainment record but recent FHWA review found gaps in race-conscious method documentation."

**Pre-edit behavior:** Scribe drafts BUILD/RAISE narrative against existing 8-criterion DOT rubric. Logician does NOT fire DBE-specific evidence prompt (not present); existing `procurement_compliance` underwriting_criterion mentions M/W/DBE outreach in `narrative_section_patterns[Procurement Approach]` line 376 but no discrete evidence weight.

**Post-edit (with §4.2 additions):** Logician fires `dbe_mbe_wbe_outreach_plan` evidence prompt (MEDIUM weight, DOT funder gate). Scribe drafts with explicit DBE annual goal + race-conscious vs race-neutral method documentation + sub-contractor outreach evidence + DBE Directory consultation. Report Generator (v0.2) extracts `dbe_mbe_wbe_outcomes` commitment type for ongoing reporting.

**Seat:** Scribe + Logician + Report Generator (v0.2). **Pass criterion:** DBE evidence prompt fires when funder=DOT; race-conscious method documentation surfaced in narrative.

### Test 4 — HUD Section 108 Loan Guarantee rubric application

**Prompt:** "Distressed CDBG entitlement city applying for HUD Section 108 Loan Guarantee to redevelop a downtown commercial corridor (loan-backed by future CDBG allocations)."

**Pre-edit behavior:** Scout matches `CDBG`; routes toward CDBG Entitlement rubric (existing `scoring_weight_patterns` entry). Scribe drafts as straight CDBG with CDBG-program-rubric framing. Section 108 specific underwriting + credit-instrument framing absent — Section 108 is not in `scoring_weight_patterns` so Judge does not surface Section-108-specific evaluation criteria.

**Post-edit (with §4.3 new rubric):** Scout + Judge recognize HUD Section 108 Loan Guarantee as a discrete rubric. Scribe drafts narrative with credit-instrument framing + future-CDBG-allocation pledge documentation + Section 108 statutory authority citation (24 CFR 570 Subpart M). Judge evaluates against Section 108 weights specifically (not CDBG-entitlement weights). Per L-024 lesson candidate: Section 108 is structurally a CLC-01 + CLC-06 hybrid (federal credit instrument), but underwriting logic for the public-purpose-grant component stays in this CLC; loan-credit component routes to CLC-06 Track A debt — orthogonality preserved at runtime, opportunity-driven.

**Seat:** Scout + Scribe + Judge. **Pass criterion:** Section 108 rubric row surfaces; Section 108 statutory authority (24 CFR 570 Subpart M) cited in narrative; Judge evaluates against Section 108 weights specifically.

### Test 5 — Justice40 covered-program admin-risk discipline

**Prompt:** "Township applying to EPA CWSRF for combined sewer overflow remediation in low-income service area. Active EPA NOFO references 'disadvantaged community' designation under CEJST as a weighted scoring component."

**Pre-edit behavior:** Scribe drafts SRF narrative; service-area-need framing references census ACS only (per existing `underwriting_criteria[service_area_need]`). Disadvantaged-community designation under CEJST is admin-risk-flagged per workspace register (`disadvantaged community` GREEN/EXPECTED for public_purpose_works at line 900-907) — Logician surfaces the term as substitute-or-retain decision. Existing prose does not surface CEJST as a Scout-vocabulary tool.

**Post-edit (with §4.1 underwriting_criteria refinement):** Scout + Scribe match CEJST + EJScreen + SVI as discrete tooling references. Scribe surfaces CEJST-designation evidence at intake (active EPA NOFO Justice40-covered status verified per RFA, not assumed). Logician fires `disadvantaged community` admin-risk register entry; given `per_clc_register.public_purpose_works: EXPECTED`, Logician confirms retain-verbatim posture; operator approves via approval_required: true.

**Seat:** Scout + Scribe + Logician. **Pass criterion:** CEJST/EJScreen/SVI surface as Scout vocabulary; disadvantaged-community designation cited per workspace-register guidance; substitution-vs-retain decision routed cleanly through admin-risk register.

---

## §8. Patch Plan

Edits proposed in this handback grouped by file path. **No edits applied from this dispatch (sidecar-only per master prompt §0).** Operator dispatches each ceremony separately.

### File: `pipeline/cards/CLC/public_purpose_works.yaml`

**Ceremony shape:** supersession-re-sign per OD-E precedent. Parent_lock_row = 255. Ceremony_parent_row = `<NEXT-AVAILABLE-COMPOUND-PARENT>` if bundled with §18 v1.x PRP-cross-reference amendment, OR `<NEXT-AVAILABLE>` standalone.

**Edit set:**

1. Header comment refresh — lines 14-20 update to reflect post-LOCK lifecycle ("Lifecycle: signed (Wave 2 LOCK row 255, 2026-05-16T16:00:00Z). Ed25519 signature present at _research_metadata.ed25519_signature; content_hash present at lifecycle.content_hash.") — documentation-only; comments stripped from canonical bytes; bundle to avoid two ceremonies (§2.3).
2. `underwriting_criteria[service_area_need].description` refine — add EJScreen + CEJST + CDC SVI (§4.1).
3. `underwriting_criteria[match_committed].description` soften FY24 per-program percentages per §5 item 3 (defer pending operator decision).
4. `scoring_weight_patterns[NEW]` — 5 rubric additions (HUD Section 108 / FEMA HMGP / DOT SS4A / DOT RCP / EPA Brownfields) per §4.3 + §5 item 4.
5. `scoring_weight_patterns[REFINE]` — FEMA BRIC FY24 softening per §4.3.
6. `evidence_weights[NEW]` — `slfrf_match_disclosure` + `section_3_compliance_plan` + `dbe_mbe_wbe_outreach_plan` per §4.2.
7. `evidence_weights[REFINE]` — PRP cross-reference annotations on davis_bacon / baba / environmental_review (prose-only in rationale field; no new field-name) per §4.2.
8. `reviewer_profile_typical.reviewer_types[NEW]` — buy_america_compliance_reviewer / davis_bacon_wage_determination_reviewer / section_3_compliance_reviewer per §4.5.
9. `reviewer_profile_typical.reviewer_priorities[NEW]` — Justice40 disadvantaged-community scoring priority per §4.1.
10. `reviewer_profile_typical.common_red_flags_from_reviewer_pov[NEW]` — cost-share certification fraud + federal-funds-as-match disclosure absent per §4.1.
11. `common_red_flags[NEW]` — 5 new probes (federal_funds_as_match_undisclosed / cost_share_certification_fraud / nepa_skip_or_premature_action / davis_bacon_weekly_payroll_gap / section_3_silence_on_hud_construction) per §4.4 + §5 item 7.
12. `commitment_tracking_pattern.typical_commitments_extracted[NEW]` — 4 new commitment types (civic_benefit_reporting / built_asset_commissioning / section_3_workforce_outcomes / dbe_mbe_wbe_outcomes) per §4.7 + §5 item 8.
13. Comment-block-only fallback — add commentary near `compliance_obligations[2 CFR Part 200]` / `[Davis-Bacon]` / `[NEPA]` describing intent to delegate live program-law to TILTH-PRP-2CFR200 / TILTH-PRP-DAVIS-BACON / TILTH-PRP-NEPA-24CFR58 once PRP loader graduates at v0.2 first wave + once the §18 v1.x `cross_references_prp:` amendment lands (per §4.9 + §5 item 1). Routes the structural gap to `_review_handback.decision_queue`.

### File: `pipeline/blueprint/v0.1/section_18_v1_x_prp_cross_reference_amendment.md` (proposed; not authored)

**Ceremony shape:** §18 v1.x amendment per master prompt rule 6 + §18.11 v1.1 fallback.

14. Author §18 v1.x amendment introducing `cross_references_prp: list[str]` to `card_clc.schema.json` (and `card_cic.schema.json` if applicable) item shapes for `compliance_obligations[*]`, `evidence_weights[*]`, `common_red_flags[*]`. Defines item-level `not.anyOf` defense-in-depth (forbidden coupling field names remain forbidden inside `cross_references_prp` list items per inheritance). Defines runtime semantics: when a card item carries `cross_references_prp: ["TILTH-PRP-XXX"]`, loader resolves the PRP at item-evaluation time IF PRP is active per `active_prps.yaml` manifest; otherwise falls back to card-only content. **No edits to LOCKed files** — this surfaces the amendment as proposal only.

### File: `pipeline/program_rule_packs/_manifest/active_prps.yaml` (proposed manifest expansion)

15. Add TILTH-PRP-BABA-IIJA entry per §5 item 2 (Build America Buy America Act + IIJA §70914 + 2 CFR 184 + OMB M-22-11 / M-24-02; iron/steel/manufactured-products/construction-materials sourcing + waiver pathways + agency-specific implementation memos). Status: draft. Content_hash: TBD. Per master prompt §0 + manifest §v0.1 DRAFT NOTE: no LOCK ceremony initiated here; surface as proposal-pending-operator-dispatch.

### File: `pipeline/institutional_memory/admin_risk_register.yaml`

16. Add `per_clc_register.public_purpose_works` cells to existing `climate resilience` entry (line 576) + `underserved` entry (line 363) per §4.4 + §5 item 6. **Out of scope for this card-only dispatch** (workspace-register update); surface to v2.x → v3.0 scrub workflow.

**OD-D Phase 4 forward-binding contract note (per master prompt rule 6 + §18.11 v1.1):**

- Edits 1-13 are value-position clean per §2.4 + Phase 4 fold-in clean per §4.10. No proposal trips refusal (c) (compound enum) or refusal (d) (literal slug in non-exempt value position).
- Edit 13 is the comment-block-only fallback for the refusal-(a)+(b) `cross_references_prp:` proposal (§4.9). Routes structurally per master prompt rule 6.
- Edit 14 is the §18 v1.x amendment proposal that, once LOCKed, removes the refusal-(b) blocker for the `cross_references_prp:` field-name addition; THEN a subsequent supersession-re-sign on the card can add the field-name to the canonical body.
- Edit 16 is workspace-register update (OD-A v2.x → v3.0 scrub workflow per master prompt §7); out of scope for card-only dispatch.

---

**Summary block:**

```
Card: CLC:public_purpose_works
Card file: pipeline/cards/CLC/public_purpose_works.yaml
Research hours actual: 1.8
Findings: 27 total — 0 P0, 14 P1, 13 P2
Decision queue: 11 operator approvals required
Conflicts with prior art: NONE (admin-risk terms align with v2.4 workspace register; 2 per_clc_register cells still pending per §5 item 6; PRP cross-references align with active manifest)
Coupling-discipline regression: NONE (0 forbidden-field-name positions; 0 non-exempt value-position regex matches; 0 legacy-phrase matches)
Lifecycle gap surfaced: draft_status reads "signed" on disk (master prompt §5 universal-gap claim does NOT apply to this Wave-2-LOCKed card; no normalization required)
Review readiness: READY (content improvements bundleable to supersession-re-sign ceremony per OD-E precedent; PRP-cross-reference field requires §18 v1.x amendment first; workspace-register cells deferred to v2.x → v3.0 scrub)
```
