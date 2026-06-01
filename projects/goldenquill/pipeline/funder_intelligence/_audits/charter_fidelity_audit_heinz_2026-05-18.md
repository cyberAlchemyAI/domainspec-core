# Charter Fidelity Cross-Check Audit — `HEINZ-FOUNDATION`

> **Methodology:** `pipeline/funder_intelligence/_audits/charter_fidelity_audit_template.md` v1.0
> **Charter:** `pipeline/funder_intelligence/pillar_1_charters/HEINZ-FOUNDATION_charter_v0_DRAFT.md`
> **Branch / PR:** `fid-week-1-pillar-1-charters-2026-05-18` (PR #33)
> **Audit date:** 2026-05-18
> **Auditor:** Cowork session (operator-commissioned after Heinz GPR memo upload)
> **Trigger:** operator caught the Pittsburgh-metro / Allegheny-County HARD-GATE framing as a P0 fidelity break against Heinz's own public scope statement.
>
> **Amendment history:**
> - **Commit 1 (`6ac8d69`) — [FIDELITY-FIX-HEINZ] Geo scope SWPA-10 + 7-area taxonomy + GPR-backed eligibility/funding/portfolio.** Geo-scope corrected from Allegheny-only to SWPA-10-county + PA-Commonwealth-serving-SWPA. Taxonomy refreshed from legacy 4-area to current 7-area. Eligibility broadened. Funding range / DEI / application-process / staff-load material added. F-HEINZ-NOT-PITTSBURGH-METRO → F-HEINZ-NOT-SWPA-OR-PA.
> - **Commit 2 (`<pending>`) — [FIDELITY-FIX-HEINZ] Three-mechanism behavior parse + demote universal geo gate + correct downgrade claims.** Operator + ChatGPT collaborative parse of the GPR identified three distinct behavior_mechanisms (regional_legitimacy_capital + transition_sensitive_relationship_clarity + capacity_partnership_beyond_grant). Charter §B restructured around these mechanisms. Universal-Pittsburgh-fail-close gate (which had become F-HEINZ-NOT-SWPA-OR-PA P0 after commit 1) DEMOTED to F-HEINZ-OUTSIDE-PA-WARNING (MED) at the funder layer — GPR respondent geography includes outside-PA respondents, so a universal funder-layer geo P0 over-restricts against corpus evidence. "Outcomes-vs-outputs conflation is Heinz's #1 downgrade vector" claim DEMOTED to general foundation-program-officer heuristic (GPR does not support the Heinz-specific framing). "Innovative is suspicious" REPLACED with "unsupported_innovation is suspicious" (GPR p.2 explicitly praises Heinz's innovative approaches when backed). Cold-outreach gate revised to operator-action shape, not hard-fail.

---

## §1 — Header

| Field | Value |
|------:|:------|
| `artifact_id` | `HEINZ-FOUNDATION` |
| `charter_path` | `pipeline/funder_intelligence/pillar_1_charters/HEINZ-FOUNDATION_charter_v0_DRAFT.md` |
| `branch` | `fid-week-1-pillar-1-charters-2026-05-18` |
| `PR` | #33 |
| `pre-fix charter SHA-256` | `db3801eb98ec5ff1f76d3ae24e6eb3f5f6925609fe05f47029d68744ad506c11` (HEAD = `5b9590a`) |
| `post-fix charter SHA-256` | `28429d7fdf80cc321d70c9dfd02b0e883f143ce0143fffe817b7b615d44c0558` |
| `commit tag` | `[FIDELITY-FIX-HEINZ]` |
| `sign_charter --dry-run` | content_hash_sha3_512 = `d1ed99aac11509ac5984657cb70481f8b419a797caf2383620fd55068560761c6d0ca3f71b95e439281ceb925804b19ad89b8c384d6ce1357b5a27eed81cd533` (canonicalization GREEN) |
| `tests/funder_intelligence/test_sign_charter.py` | 14/14 PASS post-fix (0.12s) |

---

## §2 — Sources consulted

| # | Source | Authority tier | URL / path | Retrieved | Backed which claim families |
|---|--------|:--------------:|------------|-----------|------------------------------|
| 1 | **Heinz GPR 2024 Key Findings Memo** (prepared by Center for Effective Philanthropy, dated 2025-03-21) | 2 (operator-supplied authoritative from funder itself) | Operator-uploaded PDF (400.7 KB). Canonical URL: `https://www.heinz.org/UserFiles/File/THE%20Grantee%20Perception%20Report.pdf` | 2026-05-18 | FUNDING_RANGE (median $100K 2024, 1.7yr avg length); PORTFOLIO_PATTERN (>2/3 grantees serve historically disadvantaged groups, particularly Black communities); PROGRAM_STAFF_LOAD (53 active grants + 50 apps per staffer; up from 36/36 in 2019); APPLICATION_PROCESS (23 hours process time at median grantee; down from 30 in 2019); RELATIONSHIP_HEALTH (61% receive consistent Heinz funding; ratings declining since 2019 on communication / transparency); MEDIAN_GRANTEE_BUDGET (~$1.5M stable in real terms) |
| 2 | **Heinz Endowments — Grants page** (Process & How to Apply) | 1 (funder's own public website) | `https://www.heinz.org/grants` | 2026-05-18 | GEO_SCOPE (canonical scope quote); ELIG_ENTITY (501(c)(3) + 509(a) + federally-tax-exempt government entity; individuals + for-profits not eligible); APPLICATION_PROCESS (rolling LOI ~10 min, 45-day acknowledgement target, 60-90 day decision, Blackbaud Applicant & Grantee Portal) |
| 3 | **Heinz Endowments — Strategies page** (canonical seven-area taxonomy) | 1 (funder's own public website) | `https://www.heinz.org/strategic-areas` | 2026-05-18 | PROGRAM_AREA (canonical 7-strategy taxonomy: Arts & Culture; Civic Participation; Climate, Environment & Health; Community & Economic Development; Food Systems; Veterans; Workforce — **supersedes legacy 4-area taxonomy**) |
| 4 | **Heinz Endowments — Home page** (incl. 2026 Workforce announcement + grantmaking-volume framing) | 1 (funder's own public website) | `https://www.heinz.org/` | 2026-05-18 | GEO_SCOPE (10-county SWPA span — "These Workforce grants span 10 counties"); ANNUAL_VOLUME (~$90M average annual grantmaking); MISSION_FRAMING (SWPA orientation) |

---

## §3 — Findings table

| # | Claim type | Charter line(s) (pre-fix) | Source contradicting / refining | Classification | Severity | Fix applied |
|---|------------|---------------------------|--------------------------------|----------------|:--------:|:-----------:|
| 1 | HARD_GATE / GEO_SCOPE | `runtime_consumer.scout.decision_changed`: "Scout DISCOVER restricts radar to Pittsburgh-metro / Allegheny-County-focused applicants. Out-of-region applicants downgrade to OUT_OF_SCOPE regardless of project quality (geographic-fit is hard gate at Heinz)." + `runtime_consumer.logician.decision_changed`: "F-HEINZ-NOT-PITTSBURGH-METRO (P0; primary service area not Pittsburgh-metro / Allegheny / adjacent counties)" + multiple prose mentions in §A / §B / §1 | Heinz public grants page (source 2): *"We concentrate our efforts and resources in southwestern Pennsylvania (SWPA). Given our primarily regional focus, the foundation is generally unable to consider applications for funding outside the Commonwealth of Pennsylvania, unless the proposal is expressly for the benefit of residents of the SWPA region or state."* + Heinz home page (source 4): *"These Workforce grants span 10 counties"* | **CONTRADICTED** | **P0** | YES |
| 2 | PROGRAM_AREA | `mission_framing.one_paragraph_summary`: "thematic areas (Sustainability, Creativity, Learning, Community & Economic Development)" + `source_backing.corpus_refs`: "thematic-area position papers (Sustainability / Creativity / Learning / Community & Economic Development)" | Heinz strategies page (source 3): canonical 7 strategies — Arts & Culture; Civic Participation; Climate, Environment & Health; Community & Economic Development; Food Systems; Veterans; Workforce | **STALE** | **P1** | YES |
| 3 | LANGUAGE_FLAG | `language_register.suspicious_terms`: includes `rural` with rationale "Heinz is metro-focused" | Heinz public grants page + Heinz home page Workforce span: SWPA includes Greene, Fayette, Indiana, Lawrence, Armstrong, Butler — all with substantial rural / small-town communities Heinz funds. The "metro-focused" rationale was assertion-without-source. | **UNSUPPORTED** | **P1** | YES (removed from suspicious_terms with inline comment) |
| 4 | ELIG_ENTITY / HARD_GATE | `logician_gate_candidates.F-HEINZ-501C3-MISSING`: failure_condition `kfr.applicant.tax_status != '501c3' AND not kfr.applicant.has_fiscal_sponsor()` | Heinz public grants page (source 2): *"The foundation funds organizations classified as tax-exempt under Section 501(c)(3) of the U.S. Internal Revenue Code and as public charities under Section 509(a) of that code. Organizations and government entities that are federally tax-exempt may also apply. Individuals and for-profit organizations are not eligible for funding."* — charter was missing 509(a) public-charity language and government-entity eligibility; was also missing the explicit individual / for-profit hard-ban as a distinct gate. | **PARTIAL** / **UNSUPPORTED** | **P1** | YES (renamed to `F-HEINZ-ELIGIBLE-ENTITY-MISSING` + added `F-HEINZ-INDIVIDUAL-OR-FORPROFIT` P0) |
| 5 | FUNDING_RANGE | Charter prose carried no median grant size, no average grant length, no annual grantmaking volume | GPR 2024 (source 1): median $100K in 2024, avg grant length 1.7 years (down from 2.5yr in 2019, vs 2.2yr median funder); Heinz home page (source 4): ~$90M average annual grantmaking | **PARTIAL** (material omission) | **P2** | YES (added to `mission_framing.one_paragraph_summary` + Scribe `must_do` cost-calibration line) |
| 6 | PORTFOLIO_PATTERN | Charter prose did not surface Heinz's grantee demographic-impact composition | GPR 2024 (source 1): *"over two thirds of Heinz grantees report their funded work was meant primarily to benefit at least one historically disadvantaged group, particularly African American or Black individuals and communities"* | **PARTIAL** (material omission) | **P2** | YES (added to `stage_behavior.consensus.portfolio_considerations` + new preferred_term `historically_disadvantaged`) |
| 7 | APPLICATION_PROCESS | `stage_behavior.screen.time_budget` was `<NEEDED Pillar 2>`; no portal name; no LOI vs full-application detail; no response-time targets | Heinz public grants page (source 2): rolling LOI ~10 min; 45-day acknowledgement target; 60-90 day decision; Blackbaud Applicant & Grantee Portal | **PARTIAL** (material omission) | **P2** | YES (added to `screen.time_budget` + an `application_process` thread woven through pass_fail_triggers) |
| 8 | RELATIONSHIP_PATTERN | Charter `red_team` decision_changed mentioned "prior-relationship absence" without quantifying program-officer load | GPR 2024 (source 1): program staff carry 53 active grants + 50 applications per staffer in 2024 (up from 36/36 in 2019) | **PARTIAL** (material omission) | **P2** | YES (added to `runtime_consumer.red_team.decision_changed` + `red_team_probe_seeds` rationale) |
| 9 | PROGRAM_AREA / LANGUAGE_FLAG | Charter had no Logician gate detecting accidental use of the legacy 4-area taxonomy | Heinz strategies page (source 3): 7-area taxonomy is canonical; legacy taxonomy in a draft signals stale source material | **STALE** | **P1** (rolled into finding #2 fix) | YES (added `F-HEINZ-LEGACY-TAXONOMY-LEAK` LOW gate) |

---

## §4 — P0 finding (detailed narrative)

### P0.1 — GEO_SCOPE: "Pittsburgh-metro / Allegheny-County HARD GATE" was a fidelity break

**Where the break lived (charter pre-fix, line numbers from the v0 DRAFT at branch HEAD `5b9590a`):**

- Line 30 — `runtime_consumer.scout.decision_changed`
- Line 42 — `runtime_consumer.red_team.decision_changed`
- Line 46 — `runtime_consumer.logician.decision_changed`
- Line 70 — §A `Proposal rejected` answer
- Line 90 — `runtime_consumers.scout` paragraph in §B
- Lines 106-107 — `mission_framing.one_paragraph_summary`
- Line 119 — `stage_behavior.screen.pass_fail_triggers`
- Line 124 — `stage_behavior.screen.common_rejections`
- Line 152 — `stage_behavior.consensus.portfolio_considerations`
- Line 169 — `evidence_ladder.weak`
- Line 172 — `evidence_ladder.unacceptable`
- Line 185 — `language_register.preferred_terms` (`place_based # Pittsburgh-region resonance`)
- Line 193 — `language_register.sentence_shapes_that_work`
- Lines 204, 210 — `drafting_implications.scribe_must_do` + `must_not_do`
- Line 232 — `red_team_probe_seeds`
- Line 238 — `logician_gate_candidates.F-HEINZ-NOT-PITTSBURGH-METRO`
- Line 273 — §1 "Pittsburgh-metro geographic discipline"
- Line 277 — §1 Codex test
- Line 289 — §2 "Pittsburgh-metro focus framing"

**Authoritative source contradicting:**

- Heinz public grants page (`https://www.heinz.org/grants`), Step 2 — Determine your eligibility: *"We concentrate our efforts and resources in southwestern Pennsylvania (SWPA). Given our primarily regional focus, the foundation is generally unable to consider applications for funding outside the Commonwealth of Pennsylvania, unless the proposal is expressly for the benefit of residents of the SWPA region or state."*
- Heinz home page (`https://www.heinz.org/`), 2026 Workforce announcement: *"These Workforce grants span 10 counties and support everything from pre-apprenticeship programs to long-term research."*
- Heinz home page mission line: *"In an era of massive change — technological, economic, ecological — southwestern Pennsylvania has the drive and wisdom to shape our nation's future."*

**Why this is P0:** The previous framing would have caused Scout DISCOVER to deprioritize or reject closed on applicants whose primary service area is Beaver County, Westmoreland County, Fayette County, Butler County, Armstrong County, Lawrence County, Greene County, Indiana County, or Washington County — 9 of the 10 SWPA counties Heinz publicly funds. It would also have caused Logician PRE-gate `F-HEINZ-NOT-PITTSBURGH-METRO` to fail closed against applicants in those 9 counties. **Live operational behavior under the previous charter: Heinz applications from 9 of 10 in-scope counties would have been rejected before drafting began.**

**Downstream consumers affected:**

- Scout DISCOVER — would have falsely narrowed radar to Allegheny only
- Scribe scaffold — would have written generic "Pittsburgh-metro" framing, missing the broader regional scope
- Judge — would have downgraded valid non-Pittsburgh-proper SWPA applicants
- Red Team — would have probed wrong-shape geographic-fit failures
- Logician — would have fired the wrong PRE-gate name and shape

**Fix applied:**

- Renamed Logician gate `F-HEINZ-NOT-PITTSBURGH-METRO` → `F-HEINZ-NOT-SWPA-OR-PA`, with `note:` field documenting the rename + why the previous gate was a fidelity break
- Rewrote `runtime_consumer.scout.decision_changed`, `runtime_consumer.scribe.decision_changed`, `runtime_consumer.judge.decision_changed`, `runtime_consumer.red_team.decision_changed`, `runtime_consumer.logician.decision_changed`
- Replaced §A `Proposal rejected` answer with the corrected scope language
- Rewrote `mission_framing.one_paragraph_summary` to name SWPA + the 10 counties + the PA-Commonwealth eligibility envelope
- Rewrote `stage_behavior.screen.pass_fail_triggers` + `common_rejections`
- Rewrote `stage_behavior.consensus.portfolio_considerations` to include both Pittsburgh neighborhoods AND non-Pittsburgh SWPA counties + DEI portfolio pattern
- Rewrote `evidence_ladder.weak` + `unacceptable`
- Updated `language_register.preferred_terms` (added `southwestern_pennsylvania`, `SWPA`)
- Rewrote `language_register.sentence_shapes_that_work` to model precise county / neighborhood naming + PA-statewide-serving-SWPA phrasing
- Rewrote `drafting_implications.scribe_must_do` + `must_not_do` to enforce precise SWPA sub-geography and prohibit Allegheny-default
- Rewrote `red_team_probe_seeds` geographic-fit probe to match the PA-Commonwealth boundary + SWPA-10-county preference shape
- Rewrote §1 "what depth means" and Codex test
- Rewrote §2 "primary sources in scope" to mark GPR memo + public grants page + strategies page + home page as LANDED

**Discrepancy surfaced:**

- The original operator dispatch directed "name the 9 counties." Primary sources (Heinz home page 2026 Workforce announcement, plus Heinz's published regional definition) confirm **10 counties**: Allegheny, Armstrong, Beaver, Butler, Fayette, Greene, Indiana, Lawrence, Washington, Westmoreland. The audit uses 10 — surfaced here as an explicit operator-supplied-framing vs primary-source discrepancy for operator awareness, since the fix relies on the primary-source count.

---

## §5 — P1 findings (detailed narrative)

### P1.1 — STALE: Legacy 4-area thematic taxonomy

Charter referred to "thematic areas (Sustainability, Creativity, Learning, Community & Economic Development)" — Heinz's older 4-area framing. Heinz refreshed to a 7-strategy taxonomy: Arts & Culture; Civic Participation; Climate, Environment & Health; Community & Economic Development; Food Systems; Veterans; Workforce.

**Why P1 not P0:** the legacy taxonomy doesn't directly reject valid applicants — but it leaks stale language into Scribe-generated drafts (signaling to Heinz program officers that the applicant is reading old material) and misroutes the Scout strategic-area mapping. Fix: replaced taxonomy throughout the charter + added new `F-HEINZ-LEGACY-TAXONOMY-LEAK` LOW Logician gate that warns when a draft uses any of {Sustainability, Creativity, Learning} as a Heinz strategic-area label.

### P1.2 — UNSUPPORTED: "rural" flagged as suspicious_term

Charter language_register tagged `rural` suspicious with the rationale "Heinz is metro-focused." This was assertion-without-source and contradicts the SWPA 10-county span (which includes Greene, Fayette, Indiana, Lawrence, Armstrong, Butler — all with substantial rural / small-town communities Heinz actively funds). The 2026 Workforce announcement explicitly spans rural counties.

**Why P1 not P0:** flagging `rural` doesn't rescind eligibility — it just causes Editor to flag a valid term as suspicious and steers Scribe away from accurate sub-geography framing. Fix: removed `rural` from suspicious_terms; left an inline comment in the YAML documenting the removal for audit trail.

### P1.3 — PARTIAL / UNSUPPORTED: `F-HEINZ-501C3-MISSING` gate was incomplete

The previous gate captured only 501(c)(3) tax status + fiscal-sponsor escape hatch. Heinz public grants page is broader: 501(c)(3) **AND** 509(a) public charity status, **PLUS** federally-tax-exempt government entities. The previous gate would have caused Logician to fail closed on legitimate government-entity applicants (school districts, public agencies, county / municipal departments).

**Why P1 not P0:** government-entity applicants for the kinds of work in scope at this stage of Tilth's deployment are a smaller slice than the geo-scope error. But the gate is wrong as written. Fix: renamed `F-HEINZ-501C3-MISSING` → `F-HEINZ-ELIGIBLE-ENTITY-MISSING` with a corrected failure_condition that admits 501(c)(3)+509(a) AND federally-tax-exempt government entities; added a separate P0 gate `F-HEINZ-INDIVIDUAL-OR-FORPROFIT` that fails closed on individuals + for-profits (which Heinz public grants page explicitly excludes — also previously missing as a distinct gate).

---

## §6 — P2 findings (detailed narrative, aggregated)

### P2.1 — Funding-range context (material omission)

Charter had no Heinz median grant size, average grant length, or annual grantmaking volume. Fix: added all three to `mission_framing.one_paragraph_summary` (~$100K median 2024, 1.7 yr average length, ~$90M annual volume) plus a Scribe `must_do` cost-calibration line ("Calibrate request size against Heinz's median grant of ~$100K (2024 GPR). Ambitious larger asks are not blocked but need stronger sustained-change framing").

### P2.2 — DEI portfolio pattern (material omission)

GPR 2024 captures that >2/3 of Heinz grantees report their funded work primarily benefits at least one historically disadvantaged group, particularly African American or Black individuals and communities. This is a material portfolio-composition signal Scribe should match against. Fix: added to `stage_behavior.consensus.portfolio_considerations`; added `historically_disadvantaged` to `language_register.preferred_terms`.

### P2.3 — Application-process logistics (material omission)

Charter `screen.time_budget` was `<NEEDED Pillar 2>`. Heinz public grants page details: rolling LOI ~10 min, 45-day acknowledgement target, 60-90 day decision, Blackbaud Applicant & Grantee Portal. Fix: replaced `<NEEDED>` with the corpus-backed values + woven application-process triggers through `pass_fail_triggers`.

### P2.4 — Program staff load context (material omission)

GPR 2024 captures program-staffer load (53 active grants + 50 applications per staffer in 2024, up from 36/36 in 2019). This contextualizes the cold-outreach risk: cold-outreach proposals are competing for thin attention against an already-stretched program-staff pool. Fix: added to `runtime_consumer.red_team.decision_changed` + the prior-relationship probe in `red_team_probe_seeds`.

---

## §7 — Discrepancies surfaced

| # | Discrepancy | Source-of-truth used |
|---|-------------|----------------------|
| 1 | Operator dispatch said "name the 9 counties." Primary sources confirm 10. | Used 10 (Heinz home-page 2026 Workforce announcement: "span 10 counties"; published SWPA scope). Surfaced explicitly in §4 P0.1 for operator awareness. |

---

## §8 — Fix summary

**Files changed:**

- `pipeline/funder_intelligence/pillar_1_charters/HEINZ-FOUNDATION_charter_v0_DRAFT.md` (charter amended in place; v0 DRAFT preserved per pre-sign discipline)

**Gates renamed / added:**

- `F-HEINZ-NOT-PITTSBURGH-METRO` → `F-HEINZ-NOT-SWPA-OR-PA` (renamed; severity P0 unchanged; rationale captured in `note:` field on the gate)
- `F-HEINZ-501C3-MISSING` → `F-HEINZ-ELIGIBLE-ENTITY-MISSING` (renamed; failure_condition broadened to admit 509(a) + federally-tax-exempt government entities; severity P0 unchanged; rationale in `note:`)
- `F-HEINZ-INDIVIDUAL-OR-FORPROFIT` (new; severity P0; rationale in `note:`)
- `F-HEINZ-LEGACY-TAXONOMY-LEAK` (new; severity LOW; warn on legacy 4-area taxonomy language)

**source_backing.corpus_refs additions:**

- Heinz GPR 2024 Key Findings Memo (URL: `https://www.heinz.org/UserFiles/File/THE%20Grantee%20Perception%20Report.pdf`; date published 2025-03-21; retrieved 2026-05-18; relied-on-for inventory itemized)
- Heinz Endowments Grants page (URL: `https://www.heinz.org/grants`; retrieved 2026-05-18; relied-on-for inventory itemized)
- Heinz Endowments Strategies page (URL: `https://www.heinz.org/strategic-areas`; retrieved 2026-05-18; relied-on-for inventory itemized)
- Heinz Endowments Home page (URL: `https://www.heinz.org/`; retrieved 2026-05-18; relied-on-for inventory itemized)
- Confidence promoted from `LOW pre-corpus` to `MEDIUM` (geographic / eligibility / taxonomy / application-process facts now corpus-backed; portfolio composition + per-strategy priorities still owed to Pillar-2)
- `unresolved_questions` updated to reflect newly answered + still-open questions

---

## §9 — Verification

| Check | Result |
|-------|:------:|
| `sign_charter --dry-run` against amended Heinz charter — canonicalization succeeds | GREEN (content_hash_sha3_512 = `d1ed99aac11509...d533`) |
| `pytest tests/funder_intelligence/test_sign_charter.py` post-amendment | GREEN (14/14 PASS in 0.12s) |
| §7 signature block preserved with placeholders | GREEN (all four fields = `<pending_operator_attestation>`) |
| Post-fix grep for remaining instances of broken framing | GREEN (only intentional historical notes in renamed-gate `note:` fields + Codex §1 with/without-test contrast text) |
| Roundtrip CI dependency | sign_charter helper landed on this branch; signature-roundtrip discipline unbroken |

---

## §10 — Sign-off readiness

**GREEN — fix is ready for operator review and Ed25519 sign-off on the corrected charter.**

The Pillar-1 README v0-batch sign-off path (manual ceremony per `pillar_1_charters/README.md`) is unblocked for the Heinz charter once operator has reviewed both [FIDELITY-FIX-HEINZ] amendments (commit 1 + commit 2).

**Aggregate counts for Heinz (cumulative across both commits):**

| Severity | Count | Status |
|----------|:-----:|--------|
| P0 | 1 | Fixed (commit 1: geo-scope corrected; commit 2: gate further demoted to MED warning-shape after corpus-evidence-driven re-assessment) |
| P1 | 6 | Fixed (commit 1: 3 — taxonomy stale, rural unsupported, eligibility partial. commit 2: 3 — universal-geo-fail over-restrictive, outcomes-vs-outputs over-claimed as Heinz-specific, innovative-as-suspicious over-broad) |
| P2 | 5 | Fixed (commit 1: 4 — funding-range, DEI, app-process, staff-load. commit 2: 1 — capacity-mismatch gate added per M3) |
| TOTAL | 12 | Fixed |

---

## §10A — Commit 2 amendment narrative (three-mechanism behavior parse + gate demotion + downgrade-claim corrections)

After commit 1 landed, the operator and a collaborator (ChatGPT) re-parsed the GPR memo and identified three distinct funder-behavior mechanisms — not one generic "Heinz likes relationships" idea, but three specific cause-of-decision shapes. They also surfaced that the geo-scope fix in commit 1, while correct in direction, was still too aggressive in shape (it had become F-HEINZ-NOT-SWPA-OR-PA P0 at the funder layer). The GPR's respondent geography evidence and the actual funder-layer-vs-program-layer separation make a weighted preference more accurate than a universal hard-fail. Three structural corrections also fell out of this re-parse.

### §10A.1 — Three-mechanism restructure

Added a `behavior_mechanisms:` block to §B carrying three named mechanisms, each with id + summary + source citation (with GPR page numbers) + runtime_effect for Scout / Scribe / Judge / Red Team:

- **M1 regional_legitimacy_capital** — sources: GPR p.2 §"The Endowments as a Community Leader" (grantee quote on Heinz as the foundation that makes-or-breaks projects in Pittsburgh; top-quarter ratings on local-community impact).
- **M2 transition_sensitive_relationship_clarity** — sources: GPR p.1 §"Context and Overview" (active staff / communications / strategy transition) + GPR p.4-5 §"Decreases in Clarity of Communication and Depth in Grantee Relationships" (significantly lower 2024-vs-2019 ratings on clarity / openness / candor; program-staff load jumped from 36/36 to 53/50).
- **M3 capacity_partnership_beyond_grant** — sources: GPR p.3 §"Monetary Support" (avg grant length 1.7yr, shortest since 2005; declining real-dollar value) + GPR p.4 §"Future Opportunity – Increase Grant Length" (3rd-most-common improvement theme) + GPR p.3 §"Assistance Beyond Grant Dollars" (only ~50% receive beyond-grant assistance; those who do rate Heinz higher across understanding / interaction / clarity / openness / transparency; Sustainability program 70%+).

All four AI seats (Scout, Scribe, Judge, Red Team) now wire decision_changed strings directly to the three mechanisms. `runtime_consumers` in §B updated to match. `judge_implications.scoring_dimensions_to_weight_harder` re-weighted to put M1/M2/M3 at ≥20% each, with Theory of Change ≥15%, Sustained Change ≥10%, and Outcomes Articulation downweighted to ~5-10% (was ≥20%).

### §10A.2 — Demoting the universal Pittsburgh hard gate

Commit 1 had renamed `F-HEINZ-NOT-PITTSBURGH-METRO` (P0) to `F-HEINZ-NOT-SWPA-OR-PA` (P0). Commit 2 **deletes both predecessor gates** and replaces them with `F-HEINZ-OUTSIDE-PA-WARNING` (MED, WARN_OPERATOR) at the funder layer. Rationale (cited in the gate's `note:` field): GPR 2024 respondent geography includes outside-Allegheny and outside-Pennsylvania respondents — a universal funder-layer geo P0 over-restricts against the corpus evidence. The Heinz public grants page favors PA-Commonwealth-serving-SWPA proposals, but the funder-layer enforcement is a weighted preference + advisory warning, not a universal hard-fail. **Per-program Heinz initiatives may upgrade this to P0 in the per-program charter** (e.g., a Workforce or Food Systems RFP that explicitly geo-limits to the SWPA 10-county region) — but those gates layer ON TOP of the funder-layer warning, not replacing it.

A `recommended_operator_action:` block was added to the gate listing what the operator should do when the warning fires.

### §10A.3 — Demoting the outcomes-vs-outputs claim

The prior charter framed outcomes-vs-outputs conflation as "most-common foundation downgrade" with a Heinz-specific weighting (≥20% of Judge score). **GPR 2024 does not support that Heinz-specific framing.** The GPR surfaces declining communication / understanding ratings and shortened grant length as the salient grantee-experience signals — it does not isolate outcomes-conflation as Heinz's #1 downgrade vector. Commit 2 reclassifies outcomes-vs-outputs as a **general foundation-program-officer heuristic** (still relevant, still flagged by Editor, but no longer Heinz-specific load-bearing) and downweights Judge from ≥20% to ~5-10%. F-HEINZ-OUTCOMES-CONFLATED-WITH-OUTPUTS severity lowers from MED to LOW.

### §10A.4 — Replacing "innovative is suspicious" with "unsupported_innovation is suspicious"

The prior `language_register.suspicious_terms` flagged `innovative` and `cutting_edge` flat with rationale "foundations have heard it a lot." **GPR 2024 p.2 explicitly praises Heinz's long-term "innovative" approaches** as a portfolio signature. The failure mode is *empty / unsupported* innovation language, not innovation itself. Commit 2 replaces the flat flags with `unsupported_innovation` + `unsupported_cutting_edge` and adds a new low-severity Logician gate `F-HEINZ-UNSUPPORTED-INNOVATION` (LOW) that fires when innovation framing appears without a backing track record, named mechanism, or evidence.

### §10A.5 — Cold-outreach gate revised to operator-action shape

Commit 1's `F-HEINZ-COLD-OUTREACH-WARNING` (MED) was an unstructured warning. Commit 2 adds `recommended_operator_action:` listing the three structured actions the operator should consider: (1) seek program-officer conversation before submission, (2) find peer grantee / civic partner introduction, (3) submit LOI only after strategy-fit language is tightened. Explicitly named NOT a universal hard-fail.

### §10A.6 — New gate: F-HEINZ-CAPACITY-SHORT-TERM-MISMATCH

Added per behavior_mechanism M3. Fires when a draft asks for a single-year horizon to do multi-year capacity-building / systems-change / sustained-program-continuity work. WARN_OPERATOR severity MED. Source: GPR 2024 §"Monetary Support" p.3 + §"Future Opportunity – Increase Grant Length" p.4.

### §10A.7 — Severity-table effects

Commit 2 cumulative changes to the post-commit-1 severity baseline:
- 1 gate demoted P0 → MED (geo)
- 1 gate severity lowered MED → LOW (outcomes-vs-outputs)
- 1 new MED gate added (capacity-short-term-mismatch)
- 1 new LOW gate added (unsupported-innovation)
- 1 gate restructured to operator-action-shape (cold-outreach)
- 1 set of suspicious_terms replaced (innovative → unsupported_innovation)
- 0 P0 gates added

The new P0 surface is: F-HEINZ-ELIGIBLE-ENTITY-MISSING + F-HEINZ-INDIVIDUAL-OR-FORPROFIT. Both are entity-eligibility gates derived directly from the Heinz public grants page; both are conservatively load-bearing.

---

## §11 — What the GPR memo revealed beyond the geo-scope fix

The operator-supplied GPR memo (2024 Key Findings, dated 2025-03-21) added far more than the geo-scope correction. It is the load-bearing source for **5 of the 8 findings above** (Findings #5 funding-range, #6 DEI portfolio, #7 application-process partial, #8 staff load, plus partial-backing for the Common Rejections language). It also revealed material that did NOT contradict the charter but supports future Pillar-2 elaboration:

- Heinz is in a period of strategic change as of 2024 — staff turnover including communications + program staff + leadership; strategy refresh underway. Grantee ratings declined since 2019 on clarity of communication, openness to grantee ideas, candor, and staff responsiveness.
- 61% of grantees report receiving consistent Heinz funding — and those grantees rate significantly higher on impact. The prior-relationship signal is strongly evidence-backed, not folklore. (Strengthens the existing charter framing.)
- Average grant length has shortened from 2.5yr (2019) → 1.7yr (2024); grant dollars per month have risen slightly nominally but eroded after inflation. Grantees are explicitly asking for multi-year framing. Material context for Scribe's "sustained-change" framing emphasis.
- ~50% of grantees receive assistance beyond the grant (lower than typical); Sustainability program grantees lead at >70%. Asymmetric across strategic areas.
- Heinz grantmaking process is streamlined for grantees: median 23 hours of grantee process time in 2024, fewer than at peers. The 12-hour selection-process median is favorable framing for the Scribe "approachable application" voice match.
- DEI emphasis is operationally strong but communication of what DEI means has eroded since 2019. Per-applicant framing should treat Heinz as DEI-committed but cautious about over-claiming.

These additional GPR-revealed details are queued for Pillar-2 corpus elaboration — they aren't fidelity breaks that needed fix-amendment, but they do strengthen Scribe / Judge / Red Team behavior once promoted from CONJECTURE to FACT in the per-claim source_backing.

---

## §12 — Recommended next dispatch for the other 13 charters

See `pipeline/funder_intelligence/_audits/charter_fidelity_audit_template.md` §6. Parallel dispatch of 13 audits, one `[FIDELITY-FIX-<ARTIFACT>]` commit per charter to the same PR #33 branch. Aggregate roll-up authored once all 13 land. The Heinz audit is the template-instantiation reference.

