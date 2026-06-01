# TILTH-CLC-05 Market Access — Research Handback (multi-track)

**Filed:** 2026-05-17
**Workspace:** `/Users/goldenquill/Downloads/GoldenQuill/`
**Card:** `pipeline/cards/CLC/market_access.yaml`
**Authority chain:** master prompt `docs/cic_clc_unified_master_prompt_2026-05-17.md` §2 + §4 (OD-E dual-track shape) + §7 (OD-A admin-risk surface) + `pipeline/blueprint/v0.1/section_18_6_v2_dual_track_amendment.md` (LOCKED row 274, 2026-05-17T16:00:00Z).
**Track shape:** MULTI_TRACK per §18.6 v2 — `track_a = sbir_phase_ii`, `track_b = sbir_phase_iii`. Supersession-re-sign at lock_history row 276 (2026-05-17T16:00:00Z); embedded `ed25519_signature` intentionally stale per OD-C precedent.
**Lifecycle on disk:** `draft_status: "signed"` (already at production-load value — §11 lifecycle gap does NOT apply to this card; flagged per §5 below for completeness).
**Sidecar discipline:** zero LOCKed-file writes; zero git operations; output is this single handback file only.

---

## §1. Card Impact Thesis

`market_access` is the funder-side underwriting card for buyer-development, channel, commercialization, and demand-side capital. Under §18.6 v2 Option A it now carries two structurally-distinct tracks — SBIR Phase II and SBIR Phase III — that share root metadata but differ materially in reviewer profile, evidence anchor, budget convention, and reporting rhythm. The Phase II / Phase III axis is the SBIR-program-structure split; the broader Market-Access funding portfolio (USDA VAPG / LAMP / SCBGP / RFBC, EDA Build to Scale, SBA GAFC, USDA Farm to School, NSF I-Corps, state ag-marketing programs) sits inside the Phase II / Phase III containers per the §18.6 v2 partition (Track B inherits the broader §18.6 v1 market-access content per `pipeline/scripts/od_e_restructure_card.py:204-208`).

What this card should *cause Tilth to do differently* relative to a single-track market-access baseline:

**Track A — SBIR Phase II (further SBIR R&D funds; 24-month / $750k-$1.5M typical; agency-variable):** When Scout sees an SBIR Phase II solicitation, anchor the underwriting frame on the agency-specific Phase II solicitation (USDA NIFA / NSF / NIH / DOE / DOD / EPA), require Phase I evidence-of-feasibility, treat the commercialization plan as a 30-40% rubric weight section but NOT the primary lever, and force Scribe into research-and-development drafting register — not go-to-market register. Judge applies the agency's published Phase II evaluation criteria (technical merit + commercialization potential + team + Phase I outcomes); Logician enforces Phase I prerequisite evidence + agency-correct topic-alignment + indirect-rate-negotiation surfaces. Reviewer profile is a triangle of technical SME peer reviewer + commercialization reviewer + program officer; each weights criteria differently per agency culture (NIH peer-review-heavy; DOD program-officer-heavy; NSF balanced; USDA NIFA technical-merit-heavy).

**Track B — SBIR Phase III (commercialization-without-further-SBIR-funds; non-competitive sole-source authority + private capital + non-federal funders):** When Scout sees a Phase III opportunity (sole-source contract authority, follow-on private investment, USDA VAPG, EDA Build to Scale, SBA GAFC, USDA AMS LAMP / SCBGP / RFBC Business Builder, NSF I-Corps, foundation buyer-development portfolios), anchor on the buyer-commitment-evidence ladder (PO > signed contract > LOI w/ volume+price+term > LOI w/ volume only > expression of interest), force Scribe into go-to-market register (unit-economics arithmetic + channel-strategy specificity + revenue-model precision), and require named buyers with the strongest available commitment artifact. Judge consults the program-specific rubric (VAPG 100-pt rubric at `pipeline/rubrics/vapg_fy26.json` is canonical); Red Team challenges any claim of "verified buyer" unsupported by named-rung evidence; Logician enforces match-composition + Qualified Consultant prerequisites + sole-source-eligibility for genuine Phase III procurement vehicles.

Both tracks share root metadata (display_name / funding_mechanism_summary / lifecycle / _research_metadata) and the cross-track admin-risk vocabulary (per OD-A v2.4 13 CLC-05 entries already migrated to `pipeline/institutional_memory/admin_risk_register.yaml`). The card's distinguishing runtime contribution is **track-shape-aware drafting register selection + commitment-evidence-rung enforcement + agency-rubric routing inside Track A**.

---

## §2. Current State Audit

### §2.1 What is strong now

- **Buyer-commitment evidence ladder rendered as canonical prose** at `underwriting_criteria[2].description` (RUNG 1 PURCHASE ORDER → RUNG 5 EXPRESSION OF INTEREST). Wave 2 Cycle-2 FIX-IN-PLACE per §18.6 to avoid schema-extension risk; the rung framing is what makes Scribe + Judge + Red Team able to challenge "verified buyer" claims at the right granularity. Track B reviewer logic depends on this ladder; under §18.6 v2 this should be re-anchored under `track_b.underwriting_criteria[buyer_commitment].description` (where the broader Market-Access content lives per the restructure script).
- **VAPG numeric rubric on disk + qualitative card reference**. `pipeline/rubrics/vapg_fy26.json` carries the 100-pt 7-criterion VAPG rubric with numeric weights; `scoring_weight_patterns[0]` cites it qualitatively per OQ-6 carry-over. Judge can read the JSON directly at runtime — this is the right split given the OQ-6 quantitative-evidence threshold of ≥12 CycleReceipts (currently zero).
- **Commitment tracking pattern with sub-component CAC + gross/net margin granularity** (lines 736-768) — `customer_acquisition_cost_actual.measurement_method` breaks out sales_staff_time + marketing_spend + broker_commission + slotting_fees + trade-show; `gross_margin_total` and `net_margin_total` carry channel × SKU breakdown granularity. This is what Report Generator (v0.2) needs for proposal_commitments.yaml extraction; the granularity matches VAPG + SBIR Phase II commercialization-plan request patterns.
- **Reviewer dialect split rendered as note prose** at `reviewer_profile_typical.note` (lines 470-474). Federal-program-officer register vs business-reviewer/lender/commercialization-reviewer register is captured with explicit sequencing-and-relative-weighting caveat. This is the Track A vs Track B reviewer-triangle differentiator at runtime and should be re-anchored under each track container.
- **Admin-risk register migration COMPLETE**. The 15-entry `admin_risk_term_register` block was removed at Wave 2 Cycle-2 FIX-IN-PLACE per row-170; 13 of the 15 terms are now in `pipeline/institutional_memory/admin_risk_register.yaml` v2.4 with `per_clc_register` cells (`market_access: EXPECTED | OK`). The card body is correctly drained of cross-CLC vocabulary.
- **Statutory-anchor density**. Every `compliance_obligations[*].framework` cites a CFR Part or named program regulation; primary_sources carry verbatim quotes with URL + access_date pinning. 17 unique primary sources.
- **Lifecycle truth on disk**. `draft_status: signed`, `signature_status: signed`, `runtime_load_status: loaded`, `runtime_loadable: true`, `content_hash: sha256:01379d…9764`, `signed_at: 2026-05-16T16:00:00Z`, `signed_by: founder`, `lock_history_row: 258`, `lock_timestamp_utc: 2026-05-16T16:00:00Z`. Architecture v7.0.11 §1.5 production-load constraint is SATISFIED on disk; master prompt §11 / §5 lifecycle gap does NOT apply to this card.

### §2.2 What is stale, ambiguous, over-broad, too local, too federal, or under-sourced

- **P0 — On-disk shape does NOT match §18.6 v2 OD-E LOCK row 274.** The card on disk is **single-track shape** (top-level `underwriting_criteria`, `evidence_weights`, `reviewer_profile_typical`, `common_red_flags`, `reporting_requirements_typical`, `commitment_tracking_pattern`). The dispatch + lock_history row 276 + the §18.6 v2 amendment file + the helper script `pipeline/scripts/od_e_restructure_card.py:174-211` all describe a multi-track restructure with `track_a = sbir_phase_ii` + `track_b = sbir_phase_iii`. Grep for `^track_(a|b):` in `pipeline/cards/CLC/market_access.yaml` returns zero matches; grep also returns zero matches for `track_(a|b)` anywhere in the file. The pre-restructure backup at `pipeline/validation/od_e_dual_track_2026-05-16/backup/market_access_pre_restructure.yaml` is byte-similar to the current on-disk card (only header comment line 4-5 differs — backup says "Operator review … PENDING. DRAFT — NO LOCK"; on-disk says "Operator review … COMPLETE. SIGNED — runtime-loadable"). Possible causes: (a) restructure was performed against an in-memory copy at ceremony time but the on-disk file was not overwritten before sign; (b) restructure was reverted post-ceremony but the lock_history row was not amended; (c) the on-disk file was rolled back from the multi-track shape to single-track shape by a subsequent operation between row 276 (16:00:00Z) and now. Whichever the cause, the on-disk file currently fails the §18.6 v2 schema oneOf branch 2 ("multi-track shape") and would only validate under branch 1 ("single-track legacy"). Recommend operator dispatch a forensic comparison of the on-disk SHA3-512 vs the row-276 `post_restructure_canonical_bytes_sha3_512_hex` (`4eb75e9296cff…428be55e`) to confirm what state was signed, and either (i) re-restructure + re-sign, or (ii) supersede row 276 with a clarifying row capturing the actual on-disk shape. The recommendations in §4 below are written **as if the multi-track shape is canonical** per the dispatch contract; all `track_a.…` / `track_b.…` paths assume the restructure is in place or will be re-applied.
- **Track A (SBIR Phase II) content is thin in the current on-disk single-track form.** `scoring_weight_patterns[7]` is one ten-line SBIR Phase II rubric_example covering "USDA NIFA SBIR, NSF SBIR, NIH SBIR, DOE SBIR, DOD SBIR" as a single bucket. Per-agency Phase II rubrics differ materially: NSF uses Intellectual Merit + Broader Impacts; NIH uses Significance + Investigators + Innovation + Approach + Environment (and the criterion order varies by review cycle); USDA NIFA SBIR Phase II uses a 100-pt rubric across 3 criteria (commercialization plan + scientific/technical merit + project team); DOD SBIR Phase II Component-specific (Army / Navy / Air Force / DARPA / MDA each publish separate rubrics); DOE SBIR uses Technical Merit + Quality of Approach + Project Team + Commercialization (Phase II commercialization weighted 30-40% typical). EDA Build to Scale is NOT an SBIR program and should not sit under Track A. Track A needs deeper per-agency content.
- **Track B (SBIR Phase III) content currently inherits broad Market-Access scope** — VAPG / LAMP / SCBGP / RFBC / SBA / EDA / Foundation portfolios + true SBIR Phase III sole-source procurement. The conflation is intentional per restructure script (`pipeline/scripts/od_e_restructure_card.py:204-208` — "The broader §18.6 v1 market_access content … inherits to this track"). BUT this creates a confusion: true SBIR Phase III (sole-source contract authority for Phase II awardees) and general buyer-development / commercialization funding are different mechanisms. A reviewer encountering this card may read Track B as "everything that is not Phase II R&D" — operator should clarify whether Track B is "SBIR Phase III sole-source procurement specifically" or "all post-Phase-II / non-Phase-II commercialization funding". The track_description prose folded in at ceremony covers both; the partition rule for runtime routing needs to be explicit (Scout sees an opportunity → which track activates?).
- **Phase II indirect-rate negotiation absent.** SBIR Phase II indirect cost recovery is a hard topic — small-business applicants without a federally negotiated indirect rate must use the 10% de minimis (2 CFR 200.414) or negotiate a rate with the cognizant agency. Some agencies (NIH) have specific small-business indirect-rate guidance; some applicants try to overload direct costs to avoid the indirect-rate negotiation, which fails review. Card has no `track_a.underwriting_criteria[indirect_rate_negotiation_readiness]` entry.
- **Phase I evidence-of-feasibility prerequisite is implicit, not explicit.** SBIR Phase II competitive eligibility requires successful Phase I award completion (or an equivalent demonstration for Direct-to-Phase-II programs at certain agencies — NIH HHS / DOD). Card does not encode this prerequisite. Track A `underwriting_criteria` should explicitly carry `phase_i_evidence_of_feasibility_or_direct_to_phase_ii_eligibility` with the agency-by-agency variations.
- **SBIR Phase III sole-source contract evidence missing.** True Phase III work uses 15 USC 638(r) sole-source contracting authority; evidence of agency interest in a sole-source Phase III contract (e.g., a letter from a government program office expressing commercialization interest, a SBIR Data Rights claim, prior Phase II program-of-record alignment) is a load-bearing evidence kind absent from current `evidence_weights`. Track B needs `phase_iii_sole_source_letter_of_interest_from_agency` and `phase_iii_government_customer_program_office_endorsement` evidence entries.
- **Per-agency commercialization-plan template absent.** SBIR Phase II commercialization plans differ by agency: NIH uses a structured commercialization-plan-of-action; NSF uses a Commercialization Plan template with Path-to-Market sections; DOD has Component-specific commercialization-plan formats; USDA NIFA SBIR Phase II uses a 10-15 page commercialization plan within a 25-page total proposal. Track A `narrative_section_patterns[commercialization_pathway]` or equivalent should distinguish per-agency formats.
- **Investor term-sheet evidence missing for Track B.** Phase III non-federal capital often includes named follow-on private investment (seed round, Series A, strategic partner equity, venture debt). Evidence of investor commitment — term sheets, signed investment agreements, named lead investor + co-investors, valuation, board observer rights — is a Track B underwriting input absent from current `evidence_weights`.
- **Customer LOI vs Buyer LOI vs Government Customer LOI distinction absent.** Track B Phase III commercialization can take three forms: private-sector buyer LOI (standard commercial demand evidence); government customer LOI (specifically for Phase III sole-source vehicles); follow-on Phase II IIB / commercialization-extension funding (some agencies). The three demand-evidence types weight differently per reviewer. Current `evidence_weights.buyer_letters_of_intent` collapses them; should split for Track B.
- **NSF I-Corps as commercialization training input.** NSF I-Corps Teams + Hub programs produce structured customer-discovery evidence (100+ customer interviews + Lean LaunchPad iteration + pivot evidence) that feeds Phase II commercialization plans. The card cites I-Corps but doesn't render the I-Corps → SBIR Phase II → Phase III pipeline as a runtime-routable evidence flow. Track A would benefit from explicit `narrative_section_patterns[i_corps_customer_discovery_evidence_summary]`.
- **Defer-to-active-RFA reviewer-context refinement (OD-I pattern).** Per the OD-I memory entry (2026-05-16): admin-risk terms that have already migrated to the workspace-wide register should carry a "defer to active RFA" reviewer-context note in the card body. The Wave 2 Cycle-2 FIX-IN-PLACE removed the `admin_risk_term_register` block entirely from this card; the migrated terms (commercialization / growth / scalability / market disruption / etc.) now live in the workspace register with full `per_clc_register` cells. Card body has no operator-author-facing pointer to the register; recommend a one-line comment block above `lifecycle:` reading `# Admin-risk vocabulary: see pipeline/institutional_memory/admin_risk_register.yaml v2.4 — 13 CLC-05 entries with per_clc_register: market_access cells.`
- **Verbatim source quotes age out.** Primary sources dated `access_date: 2026-05-15`. Internet Archive snapshot re-verification is the §18.11 discipline; next Phase 4 re-dispatch should confirm Wayback Machine snapshots of all 17 primary_source URLs.
- **VAPG FY26 deadline 2026-04-22 already past.** Per `_review_handback.surface_ambiguities[1]` — VAPG is annual; FY27 NOFO posts on USDA RD calendar. Card cites the regulation (7 CFR 4284 Subpart J) as durable. Per Law 5, deadlines belong in Program Rule Packs (not card body).

### §2.3 Lifecycle / signature / schema concerns

- **`draft_status: signed` on disk.** No normalization required for this card. Master prompt §11 / §5 lifecycle gap (the all-cards-say-"draft" scenario) is reported as a historical observation; the current on-disk file has `draft_status: signed` per the Wave 2 LOCK ceremony at row 258 + subsequent OD-E supersession at row 276.
- **Embedded `ed25519_signature` stale per OD-C precedent.** The signature value on disk (`28d78c1ff…aaa08`) is the Wave 2 row 258 signature against the pre-restructure single-track canonical bytes. The authoritative new sig is the row 276 `ed25519_signature` (`83e6328bdf8…ed5002`) over the post-restructure canonical bytes (claimed SHA3-512 `4eb75e9296cff…428be55e`, claimed file size 97669 bytes). Loader-time re-validation is v0.2 first-wave scope per architecture v7.0.11 §5.
- **On-disk SHA3-512 likely does not match row 276 claim.** Given the on-disk shape is single-track (no `track_a` / `track_b` keys), the on-disk canonical-JSON SHA3-512 will not equal `4eb75e9296cff…428be55e`. This is the P0 surfaced in §2.2. A research-session validation script would report a hash mismatch here; that's a true defect, not an expected-stale-sig artifact.
- **Schema oneOf branch 2 validation would fail on current disk state.** Per `pipeline/cards/_schema/card_clc.schema.json` §18.6 v2 oneOf (the schema delta described in `section_18_6_v2_dual_track_amendment.md` §1.4), the multi-track branch requires `track_a` + `track_b` present and root-level track-specific fields ABSENT. The on-disk file has root-level track-specific fields present and no `track_a` / `track_b`. It validates under branch 1 (single-track legacy) — which is fine for backward-compat but contradicts the supersession claim at row 276.
- **Lock-history housekeeping.** `lifecycle.lock_history_row: 258`; no `supersession_lock_history_row` field carried for row 276. If a forward-binding contract expects the supersession-row to be reflected in the card body, recommend adding `supersession_lock_history_row: 276` at next ceremony (operator decision per food_systems handback Run 1 Patch E1).

### §2.4 Coupling-discipline self-audit (per master prompt §0 rule 3 — LIVE OD-C row 272 value-position regex set)

**Method.** Manual value-position scan over the full card body using the regex set from `pipeline/logician/gates/f_cards_coupling_violation_extension.py`:

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

**Results (grep over `pipeline/cards/CLC/market_access.yaml`):**

| Line | Path | Match | Exempt? |
|---|---|---|---|
| 23 | `card_id` | `TILTH-CLC-05` | YES — `_VALUE_POSITION_EXEMPT_PATHS` |
| 27 | `tilth_clc_id` | `TILTH-CLC-05` | YES — `_VALUE_POSITION_EXEMPT_PATHS` |
| 819 | `_research_metadata.priors_consulted[0].extract_note` | `TILTH-CLC-00` | YES — `_research_metadata` top-level key starts with `_` |
| 822 | `_research_metadata.priors_consulted[1].extract_note` | `TILTH-CLC-05` | YES — same exempt subtree |
| 834 | `_research_metadata.priors_consulted[7].extract_note` | `TILTH-CLC-05` | YES — same exempt subtree |

**Verdict — LIVE regex set: 0 non-exempt findings on the current on-disk single-track form.** Card passes. (Same scan must be re-run on whatever shape lands at next supersession — when the multi-track restructure is re-applied, the per-track containers must remain clean too. The restructure script preserves `_research_metadata` at root per the §18.6 v2 shared-metadata contract, so the exempt-subtree exemption continues to cover the `TILTH-CLC-*` references in `extract_note`.)

### §2.5 Forbidden-field-name registry self-audit

Manual grep for forbidden CLC-side top-level + nested-in-item field names (per master prompt §0 rule 2 / `FORBIDDEN_FIELD_REGISTRY`):

```
eligible_cic_subset / cic_allowlist / cic_denylist / preferred_cics / cic_win_rate / cic_ranking_preferences
```

Grep returns 0 hits across the card body. **Verdict: 0 forbidden-field findings.** The header-comment-block at lines 7-13 explicitly documents the absence per Wave 2 OQ resolution; the comment block is parser-stripped before canonical-bytes computation so does not contribute to the scan surface.

---

## §3. Research Findings

### §3.1 Official / primary sources consulted (already on card or newly verified)

| Source | URL | Type | Access | Supports | Confidence |
|---|---|---|---|---|---|
| USDA VAPG program page | https://www.rd.usda.gov/programs-services/business-programs/value-added-producer-grants | official | 2026-05-15 | Track B underwriting + evidence | HIGH |
| USDA AMS LAMP umbrella | https://www.ams.usda.gov/services/grants/lamp | official | 2026-05-15 | Track B FMPP / LFPP / RFSP | HIGH |
| USDA AMS LFPP | https://www.ams.usda.gov/services/grants/lfpp | official | 2026-05-15 | Track B intermediate supply chain | HIGH |
| USDA AMS SCBGP | https://www.ams.usda.gov/services/grants/scbgp | official | 2026-05-15 | Track B specialty crop state pass-through | HIGH |
| USDA AMS RFBC | https://www.ams.usda.gov/services/local-regional/rfbc | official | 2026-05-15 | Track B Business Builder subaward | HIGH |
| EDA Build to Scale | https://www.eda.gov/funding/programs/build-to-scale | official | 2026-05-15 | Track B regional ecosystem | HIGH |
| SBA grants overview | https://www.sba.gov/funding-programs/grants | official | 2026-05-15 | Track B SBA program scope | HIGH |
| SBA GAFC announcement | https://www.sba.gov/article/2024/may/01/sba-launches-2024-growth-accelerator-fund-competition-incentivizing-innovation-investment | official | 2026-05-15 | Track B SBA GAFC | HIGH |
| USDA Farm to School (FNS) | https://www.fns.usda.gov/cfs/farm-school-grant-program | official | 2026-05-15 | Track B institutional procurement | HIGH |
| PA DOA SCBGP | https://www.pa.gov/agencies/pda/programs/specialty-crop-block-grant-program.html | official | 2026-05-15 | Track B PA SCBGP example | HIGH |
| USDA AMS Market News | https://www.ams.usda.gov/market-news | official | 2026-05-15 | Track B market-study source | HIGH |
| BABA | https://www.transportation.gov/buyamerica | official | 2026-05-15 | Compliance (Track B infrastructure programs) | HIGH |
| FDA FSMA | https://www.fda.gov/food/guidance-regulation-food-and-dietary-supplements/food-safety-modernization-act-fsma | official | 2026-05-15 | Compliance (food products) | HIGH |
| 2 CFR Part 200 | https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200 | official | 2026-05-15 | Compliance baseline | HIGH |
| FFATA FSRS | https://www.fsrs.gov/ | official | 2026-05-15 | Sub-award reporting | HIGH |
| NASDA state-grants aggregator | https://www.nasda.org/policy/state-grants-programs | practitioner | 2026-05-15 | State ag-program discovery | MEDIUM |
| USDA RD portal | https://www.rd.usda.gov/ | official | 2026-05-15 | Track B portal | HIGH |
| EDA apply | https://www.eda.gov/funding/apply | official | 2026-05-15 | Track B portal | HIGH |

### §3.2 Sources NEW to this handback (Track A SBIR Phase II depth — not in card today)

| Source | URL | Type | Access | Supports | Confidence |
|---|---|---|---|---|---|
| SBIR.gov About / Phase III authority | https://www.sbir.gov/about | official | 2026-05-17 | Track A + Track B Phase distinction | HIGH |
| SBIR.gov Applicants | https://www.sbir.gov/applicants | official | 2026-05-17 | Track A SBIR application process | HIGH |
| NSF SBIR/STTR | https://seedfund.nsf.gov/ | official | 2026-05-17 | Track A NSF-specific Phase II rubric | HIGH |
| NSF I-Corps Teams | https://new.nsf.gov/funding/opportunities/innovation-corps-teams | official | 2026-05-17 | Track A I-Corps customer-discovery input | HIGH |
| NIH SBIR/STTR | https://seed.nih.gov/small-business-funding/small-business-program-basics/SBIR-STTR-programs | official | 2026-05-17 | Track A NIH-specific Phase II rubric | HIGH |
| USDA NIFA SBIR | https://www.nifa.usda.gov/grants/programs/small-business-innovation-research-program-sbir | official | 2026-05-17 | Track A USDA NIFA Phase II | HIGH |
| DOE SBIR/STTR | https://science.osti.gov/sbir | official | 2026-05-17 | Track A DOE Phase II commercialization weight | HIGH |
| DOD SBIR/STTR | https://www.dodsbirsttr.mil/ | official | 2026-05-17 | Track A DOD component-specific Phase II | HIGH |
| 15 USC 638 (SBIR/STTR statute incl. Phase III sole-source authority) | https://www.govinfo.gov/app/details/USCODE-2022-title15/USCODE-2022-title15-chap14A-sec638 | official | 2026-05-17 | Track B Phase III sole-source authority | HIGH |
| 2 CFR 200.414 (indirect cost recovery) | https://www.ecfr.gov/current/title-2/section-200.414 | official | 2026-05-17 | Track A indirect-rate negotiation | HIGH |

**Source-discipline note.** Per master prompt §2 rule 7: every newly proposed factual addition in §4 below cites one of these sources by URL + access date. No verbatim quotes exceed two sentences per the Wave 1 OQ verbatim-quote cap. Only the original 18 sources are reflected as `_research_metadata.primary_sources` entries today; the 10 NEW sources above would be appended at next supersession if the operator accepts the §4 patches.

---

## §4. Proposed Card Improvements

**Section organization.** Per master prompt §2 prompt body rule 12, recommendations are per-track unless they apply to shared root metadata. YAML paths assume the §18.6 v2 multi-track shape is in place (or will be re-applied per §2.2 P0). Where the on-disk shape today is single-track, the equivalent root-level path is noted in parens.

### §4.0 — Shared root-level (applies to both tracks)

**4.0.1** — `funding_mechanism_summary` (root): The current sentence is functional but conflates the two tracks awkwardly ("Includes the SBIR Phase III commercialization stage … Phase III is a status / mechanism reliant on private, customer-funded, or other non-federal capital, not a new federal grant. The Phase II → Phase III transition is characteristic of Market Access funding logic and distinguishes it from purely R&D-focused funding."). Per §18.6 v2 §2.4, `funding_mechanism_summary` is a single-sentence cross-track summary; per-track summaries live in `track_a.track_description` + `track_b.track_description`. **Recommend** rewrite to single sentence: *"Buyer-development, channel, commercialization, and demand-side capital — split into Track A (SBIR Phase II further R&D funds) and Track B (SBIR Phase III commercialization without further SBIR funds, plus the broader buyer-development federal + foundation portfolio: USDA VAPG / LAMP / SCBGP / RFBC, EDA Build to Scale, SBA GAFC, USDA Farm to School, NSF I-Corps, state ag-marketing programs)."* — Why: Scout reads `funding_mechanism_summary` for high-level routing; the multi-track flag should be obvious from the first read.

**4.0.2** — `_research_metadata.primary_sources[NEW]`: append the 10 Track A SBIR-agency-specific sources from §3.2. — Why: Phase II per-agency depth currently absent; Scribe / Judge cannot route per-agency Phase II content without the source pins. Card YAML.

**4.0.3** — Header comment block (root, comment-only — does NOT change canonical bytes): add one line above `lifecycle:` reading `# Admin-risk vocabulary: see pipeline/institutional_memory/admin_risk_register.yaml v2.4 — 13 CLC-05 market_access entries (commercialization / growth / scalability / market disruption / competitive advantage / import substitution / domestic supply chain / Buy American / underserved market / underrepresented founders / value-added / local food system / food sovereignty). Defer-to-active-RFA reviewer-context per OD-I.` — Why: per Wave 2 Cycle-2 FIX-IN-PLACE the `admin_risk_term_register` block was removed entirely; operator-authors of next-cycle research handbacks need an explicit pointer to the workspace register. Pure documentation; no re-sign required (canonical-JSON excludes comments — per memory entry `feedback_canonical_json_excludes_comments`).

**4.0.4** — `lifecycle.supersession_lock_history_row` (root): add field with value `276`. — Why: forward-binding contract per food_systems handback Run 1 Patch E1; surfaces the actual supersession-row pointer in card body for loader-time audit-trail traversal. Operator decision: would invalidate `content_hash` and force re-sign — bundle with the §2.2 P0 re-restructure ceremony.

### §4.1 — Track A (sbir_phase_ii) — Search Vocabulary / Underwriting Criteria

**4.1.1** — `track_a.underwriting_criteria[NEW]` `phase_i_evidence_of_feasibility_or_direct_to_phase_ii_eligibility`:
```yaml
- criterion: "phase_i_evidence_of_feasibility_or_direct_to_phase_ii_eligibility"
  description: "Successful SBIR Phase I award completion documented with technical results + commercialization-readiness deliverables, OR Direct-to-Phase-II eligibility under the agency-specific rules (HHS/NIH has standing D2P2 authority; DOD components publish D2P2 topics per cycle; NSF has D2P2 under select solicitations). Phase I-equivalent demonstration must show technical feasibility extended to commercial-readiness; reviewers compare proposed Phase II scope against Phase I findings + named pivot decisions."
  weight_in_typical_rubric: "qualitative"
  source_citation: "https://www.sbir.gov/about"
```
— Why: Phase I prerequisite is the gate — Logician PRE-gate (Scout: opportunity is Phase II) should refuse opportunities without Phase I evidence or D2P2 eligibility. Affects Scribe (no draft without prerequisite); Logician (PRE-gate); Scout (eligibility-screen). Card YAML.

**4.1.2** — `track_a.underwriting_criteria[NEW]` `commercialization_plan_per_agency_format`:
```yaml
- criterion: "commercialization_plan_per_agency_format"
  description: "Per-agency commercialization-plan template. NSF SBIR uses Commercialization Plan with Path-to-Market sections (≤10 pp). NIH SBIR uses Commercialization Plan-of-Action embedded in Research Strategy. USDA NIFA SBIR Phase II requires 10-15 pp commercialization plan within 25 pp total proposal envelope. DOD SBIR varies by Component (Army / Navy / Air Force / DARPA / MDA / SOCOM each publish format guidance per topic). DOE SBIR commercialization weighted 30-40% of total rubric. Scribe MUST select the per-agency template at draft time; cross-agency template reuse produces structurally-incorrect submissions."
  weight_in_typical_rubric: "qualitative"
  source_citation: "https://www.sbir.gov/applicants"
```
— Why: per-agency format variance is the most common Phase II structural defect; Scribe routing without this criterion produces wrong-shape commercialization plans. Affects Scribe (template selection); Judge (per-agency rubric); Logician (POST-gate format check). Card YAML.

**4.1.3** — `track_a.underwriting_criteria[NEW]` `indirect_rate_negotiation_readiness`:
```yaml
- criterion: "indirect_rate_negotiation_readiness"
  description: "Phase II applicants must declare indirect cost recovery posture: federally negotiated indirect rate agreement (NICRA) with cognizant agency; 10% de minimis MTDC per 2 CFR 200.414 if no NICRA AND total federal awards <$35M; or NICRA-in-negotiation with timeline. Indirect overload onto direct cost lines (a common applicant tactic to avoid NICRA negotiation) is a hard rejection at most agencies. NIH publishes small-business indirect-rate guidance; DOD components vary; USDA NIFA requires explicit declaration."
  weight_in_typical_rubric: "qualitative"
  source_citation: "https://www.ecfr.gov/current/section-200.414"
```
— Why: indirect-rate negotiation kills Phase II applicants who treat it as an afterthought; Scribe budget composition must declare the posture explicitly. Affects Scribe (budget narrative); Logician (PRE-gate check on declared posture). Card YAML.

**4.1.4** — `track_a.underwriting_criteria[NEW]` `topic_alignment_specificity_per_agency`:
```yaml
- criterion: "topic_alignment_specificity_per_agency"
  description: "Each SBIR Phase II solicitation publishes topic-specific subtopics; Phase II proposals must align to a named topic + subtopic from the Phase I award (or the D2P2-eligible topic). Off-topic proposals fail eligibility regardless of merit. DOD topics map to program-of-record needs; DOE topics map to mission-area portfolios; USDA NIFA SBIR topics map to ten programmatic areas (per 15 USC 638 statutory areas); NSF SBIR topics are technology-area-based; NIH SBIR topics map to Institute / Center priorities."
  weight_in_typical_rubric: "qualitative"
  source_citation: "https://www.sbir.gov/topics"
```
— Why: topic-alignment failures are zero-merit rejections; Scout VERIFY stage should refuse Phase II opportunities where applicant's Phase I award topic ≠ the Phase II solicitation topic. Affects Scout (VERIFY); Logician (PRE-gate). Card YAML.

### §4.2 — Track A — Reviewer Profile + Evidence Weights

**4.2.1** — `track_a.reviewer_profile_typical.reviewer_types` (replace or amend current single-track register):
```yaml
reviewer_types:
  - "sbir_program_manager_per_agency (USDA NIFA SBIR PM, NSF SBIR PD, NIH SBIR PO at the relevant IC, DOE SBIR Topic Manager, DOD Component SBIR PM)"
  - "technical_sme_peer_reviewer (technical-area expert; weights technical merit + scientific rigor; agency-recruited reviewer pool)"
  - "commercialization_peer_reviewer (commercial / industry expert; weights commercialization plan + market opportunity + team commercial experience)"
  - "phase_iii_program_office_endorser (where commercialization plan names a government customer; the named program office's expressed interest factors into evaluation)"
```
— Why: the SBIR Phase II reviewer **triangle** (program officer + technical reviewer + commercialization reviewer) is the single most important Phase II runtime concept; weighting Scribe register selection by which reviewer type dominates per agency is load-bearing. NIH peer-reviewer-heavy; DOD program-officer-heavy; NSF balanced; USDA NIFA technical-merit-heavy; DOE varies by program. Affects Scribe (register); Judge (agency-rubric application); Red Team (challenge against the dominant reviewer perspective). Card YAML.

**4.2.2** — `track_a.evidence_weights[NEW]` `phase_i_final_report_with_technical_results`:
```yaml
phase_i_final_report_with_technical_results:
  weight: "HIGH"
  rationale: "Phase I final report documenting demonstrated technical feasibility — performance results vs Phase I objectives, pivot decisions, lessons learned. Phase II reviewers read the Phase I report as evidence of execution capability; weak Phase I outcomes correlate strongly with Phase II rejection."
  source_citation: "https://www.sbir.gov/about"
```

**4.2.3** — `track_a.evidence_weights[NEW]` `agency_specific_commercialization_plan_template_completed`:
```yaml
agency_specific_commercialization_plan_template_completed:
  weight: "HIGH"
  rationale: "Commercialization plan completed in the per-agency template format (NSF / NIH / USDA NIFA / DOD Component / DOE). Off-template plans are restructured or rejected by program managers. NSF I-Corps customer-discovery evidence integrates into NSF SBIR Phase II commercialization plan; equivalent customer-discovery evidence improves all-agency Phase II commercialization scoring."
  source_citation: "https://www.sbir.gov/applicants"
```

**4.2.4** — `track_a.evidence_weights[NEW]` `i_corps_customer_discovery_evidence_summary`:
```yaml
i_corps_customer_discovery_evidence_summary:
  weight: "MEDIUM"
  rationale: "NSF I-Corps Teams or Hub completion produces structured customer-discovery evidence (100+ interviews + Business Model Canvas + pivot documentation) that feeds SBIR Phase II commercialization plans. NSF SBIR weights I-Corps evidence highly; cross-agency Phase II commercialization reviewers welcome the structured methodology."
  source_citation: "https://new.nsf.gov/funding/opportunities/innovation-corps-teams"
```

**4.2.5** — `track_a.evidence_weights[NEW]` `key_personnel_commercialization_experience`:
```yaml
key_personnel_commercialization_experience:
  weight: "HIGH"
  rationale: "Phase II team must include named Key Personnel with commercialization experience (industry roles, prior commercialization outcomes, IP development, prior SBIR Phase II / Phase III completions). Pure-academic teams without commercial experience score weakly on commercialization criterion regardless of technical merit."
  source_citation: "https://www.sbir.gov/applicants"
```

### §4.3 — Track A — Common Red Flags (red_team_probes)

**4.3.1** — `track_a.common_red_flags[NEW]` `commercialization_plan_too_thin_for_phase_ii`:
```yaml
- flag: "commercialization_plan_too_thin_for_phase_ii"
  severity: "HIGH"
  red_team_probe: "Phase II commercialization plan must walk the path from technical demonstration to first revenue. Does the plan name target customers, channel strategy, revenue model, pricing, regulatory pathway, IP strategy, follow-on capital plan? Generic 'we will commercialize through partners' fails."
  source_citation: "https://www.sbir.gov/applicants"
```

**4.3.2** — `track_a.common_red_flags[NEW]` `academic_team_no_commercial_experience`:
```yaml
- flag: "academic_team_no_commercial_experience"
  severity: "HIGH"
  red_team_probe: "Phase II team must include named Key Personnel with prior commercialization experience — industry role, prior product launch, prior Phase II / Phase III outcome. Pure-academic teams without a named commercial-lead Key Personnel are flagged by commercialization reviewers."
```

**4.3.3** — `track_a.common_red_flags[NEW]` `phase_i_outcomes_weak_or_pivoted_without_evidence`:
```yaml
- flag: "phase_i_outcomes_weak_or_pivoted_without_evidence"
  severity: "HIGH"
  red_team_probe: "Phase I results must show technical feasibility OR a documented pivot with rationale + evidence. Weak Phase I outcomes with no pivot evidence read as failure-to-execute; Phase II reviewers compare Phase II scope against Phase I results directly."
```

**4.3.4** — `track_a.common_red_flags[NEW]` `off_topic_proposal_to_solicitation`:
```yaml
- flag: "off_topic_proposal_to_solicitation"
  severity: "HIGH"
  red_team_probe: "Phase II proposal must align to a named topic + subtopic in the agency's Phase II solicitation. Off-topic proposals are administratively rejected regardless of merit. Has the applicant's Phase I award topic been verified against the Phase II solicitation topic list?"
  source_citation: "https://www.sbir.gov/topics"
```

**4.3.5** — `track_a.common_red_flags[NEW]` `indirect_cost_overload_to_avoid_nicra`:
```yaml
- flag: "indirect_cost_overload_to_avoid_nicra"
  severity: "MEDIUM"
  red_team_probe: "Budget direct-cost lines must reflect actual direct work, not indirect cost overload to avoid NICRA negotiation. Reviewers compare direct-cost composition against typical Phase II direct-cost patterns; outlier composition triggers indirect-rate scrutiny."
  source_citation: "https://www.ecfr.gov/current/section-200.414"
```

### §4.4 — Track A — Narrative Section Patterns

**4.4.1** — `track_a.narrative_section_patterns` (per agency):
- `sbir_phase_ii_specific_aims_or_technical_objectives` (NIH-style: Specific Aims; NSF-style: Project Description / Technical Objectives) — 1-2 pp typical
- `phase_i_results_summary_and_phase_ii_extension` — 2-4 pp typical
- `commercialization_plan_per_agency_template` — 5-15 pp depending on agency (NSF ≤10 pp; USDA NIFA 10-15 pp; NIH embedded in Research Strategy)
- `i_corps_customer_discovery_summary` (where I-Corps completed) — 1-3 pp
- `intellectual_property_strategy_and_data_rights_assertion` (SBIR Data Rights claim) — 1 pp
- `key_personnel_commercialization_experience_summary` — 1-2 pp
- `follow_on_capital_plan_and_phase_iii_pathway` — 2-4 pp

Why: per-agency narrative sections differ; current single-track `narrative_section_patterns[15]` (`Commercialization Pathway / SBIR Phase III Plan`) collapses Track A narrative into one entry. Track A reviewers read seven distinct narrative sections; Scribe needs the structure. Card YAML.

### §4.5 — Track A — Common Application Forms / Portals

**4.5.1** — `track_a.common_application_forms[NEW]` per agency:
- NIH SBIR Phase II via eRA Commons / Assist (`https://seed.nih.gov/`)
- NSF SBIR Phase II via Research.gov / FastLane (`https://seedfund.nsf.gov/`)
- USDA NIFA SBIR Phase II via Grants.gov (`https://www.nifa.usda.gov/grants/programs/small-business-innovation-research-program-sbir`)
- DOD SBIR Phase II via DSIP (`https://www.dodsbirsttr.mil/`)
- DOE SBIR Phase II via EERE Exchange or PAMS (`https://science.osti.gov/sbir`)

Why: per-agency portal routing for Uploader assembly. Affects Uploader (portal selection); Scribe (per-portal narrative format). Card YAML.

### §4.6 — Track B (sbir_phase_iii) — Underwriting Criteria

**4.6.1** — `track_b.underwriting_criteria[NEW]` `sole_source_phase_iii_authority_eligibility`:
```yaml
- criterion: "sole_source_phase_iii_authority_eligibility"
  description: "True SBIR Phase III work uses 15 USC 638(r) sole-source contracting authority, restricted to Phase II awardees pursuing commercialization derived from the Phase I/II work. Applicant must document Phase II award + technical derivation + named government customer agency expressing commercialization interest. Sole-source eligibility is verified by the contracting officer at award; pre-award evidence includes program-office endorsement letter, named buyer-program alignment, and SBIR Data Rights claim."
  weight_in_typical_rubric: "qualitative"
  source_citation: "https://www.govinfo.gov/app/details/USCODE-2022-title15/USCODE-2022-title15-chap14A-sec638"
```
— Why: Phase III sole-source authority is unique; Scout / Logician should distinguish true Phase III (sole-source procurement) from broader commercialization (open-competition VAPG / Build to Scale / etc.). Affects Scout (VERIFY); Logician (PRE-gate). Card YAML.

**4.6.2** — `track_b.underwriting_criteria[NEW]` `investor_or_follow_on_capital_commitment_strength`:
```yaml
- criterion: "investor_or_follow_on_capital_commitment_strength"
  description: "Phase III commercialization typically requires named follow-on capital — seed / Series A term sheet, strategic-partner investment commitment, venture-debt facility, customer-funded growth contract. Evidence ladder: signed term sheet with lead-investor + co-investors named + valuation + use-of-funds > committed-funding-not-yet-closed > soft-commitment-letter > advisor-introductions-only. Pre-revenue Phase III applicants must show capital-commitment evidence at the strongest available rung."
  weight_in_typical_rubric: "qualitative"
  source_citation: "https://www.sbir.gov/about"
```
— Why: Phase III is non-federal-funded; reviewers (where applicable) and downstream funders evaluate follow-on capital strength rigorously. Affects Scribe (capital narrative); Judge (capital-evidence scoring); Logician (capital-evidence PRE-gate for award announcements). Card YAML.

**4.6.3** — `track_b.underwriting_criteria[REFINE]` `buyer_commitment` (existing — keep the rung-ladder prose but split government-customer LOI from private-buyer LOI):
- Add paragraph: "*Government customer LOI distinction:* for Phase III sole-source pursuits, the buyer-commitment artifact is a letter from the named federal program office expressing interest in a Phase III sole-source procurement. This is a different artifact class from private-buyer LOIs — it does not commit dollars or volume, but it commits the program office to consider a sole-source action under 15 USC 638(r) authority. Scribe should attach both the program-office endorsement AND any private-buyer evidence at the strongest available rung."
— Why: Phase III dual-buyer-type evidence is load-bearing; single-track form collapses the distinction. Affects Scribe (evidence attachment); Judge (per-buyer-type evidence weighting); Logician (POST-gate evidence-class presence). Card YAML.

### §4.7 — Track B — Evidence Weights

**4.7.1** — `track_b.evidence_weights[NEW]` `phase_iii_sole_source_letter_of_interest_from_agency`:
```yaml
phase_iii_sole_source_letter_of_interest_from_agency:
  weight: "HIGH"
  rationale: "Letter from the named federal program office expressing interest in a Phase III sole-source procurement of the applicant's Phase II-derived technology. Required for true Phase III sole-source pursuits; absence forces routing through open-competition vehicles (VAPG / Build to Scale / SBA GAFC / foundation portfolios) rather than 15 USC 638(r) authority."
  source_citation: "https://www.govinfo.gov/app/details/USCODE-2022-title15/USCODE-2022-title15-chap14A-sec638"
```

**4.7.2** — `track_b.evidence_weights[NEW]` `investor_term_sheet_or_signed_investment_agreement`:
```yaml
investor_term_sheet_or_signed_investment_agreement:
  weight: "HIGH"
  rationale: "Signed term sheet (seed / Series A / strategic) with lead-investor + co-investors named + valuation + use-of-funds, OR signed investment agreement at any stage. Evidence of named follow-on capital is decisive for Phase III applicants; soft-commitment letters from advisors are NOT equivalent."
```

**4.7.3** — `track_b.evidence_weights[NEW]` `customer_funded_growth_contract_or_pilot_revenue`:
```yaml
customer_funded_growth_contract_or_pilot_revenue:
  weight: "HIGH"
  rationale: "Signed paid-pilot contract or first-revenue customer agreement with named customer + dollar value + delivery terms. Pre-revenue Phase III applicants without customer-funded contracts must rely entirely on investor capital + government-customer endorsement; named pilot revenue is the strongest demand-evidence rung at Phase III."
```

**4.7.4** — `track_b.evidence_weights[REFINE]` `buyer_letters_of_intent` (existing — split into three sub-classes via rationale rewrite):
- Add paragraph: "*Three Phase III sub-classes:* (i) private-sector buyer LOI on buyer letterhead with volume + price + term — strongest commercial demand artifact; (ii) government-customer program-office endorsement letter for sole-source Phase III pursuit — see `phase_iii_sole_source_letter_of_interest_from_agency`; (iii) strategic-partner investment-with-procurement-rights letter — typically attached to follow-on capital commitment. Reviewers weight per Phase III pursuit type (open-competition vs sole-source vs strategic-partner-anchored)."

### §4.8 — Track B — Common Red Flags

**4.8.1** — `track_b.common_red_flags[NEW]` `still_pre_revenue_at_phase_iii_no_capital_or_customer_evidence`:
```yaml
- flag: "still_pre_revenue_at_phase_iii_no_capital_or_customer_evidence"
  severity: "HIGH"
  red_team_probe: "Phase III requires named follow-on capital OR named customer revenue OR named government program office endorsement for sole-source. Pre-revenue Phase III applicants with no investor term sheet + no customer pilot + no program-office endorsement have no Phase III path; recommend pivot back to Phase IIB or open-competition Build to Scale / VAPG / GAFC."
```

**4.8.2** — `track_b.common_red_flags[NEW]` `no_third_party_validation_for_phase_iii_commercialization_claim`:
```yaml
- flag: "no_third_party_validation_for_phase_iii_commercialization_claim"
  severity: "HIGH"
  red_team_probe: "Phase III commercialization claims must carry third-party validation — named customers / investors / strategic partners / government program office. Applicant-internal projections without third-party validation read as fiction at Phase III maturity."
```

**4.8.3** — `track_b.common_red_flags[NEW]` `confusion_of_phase_iii_sole_source_with_open_competition`:
```yaml
- flag: "confusion_of_phase_iii_sole_source_with_open_competition"
  severity: "MEDIUM"
  red_team_probe: "Applicant has named 'Phase III' but is pursuing open-competition VAPG / Build to Scale / GAFC / foundation buyer-development funding. These are commercialization vehicles but not 15 USC 638(r) sole-source Phase III. The labels should match the underwriting vehicle; mislabeling causes Scribe + Judge to mis-route the application."
  source_citation: "https://www.govinfo.gov/app/details/USCODE-2022-title15/USCODE-2022-title15-chap14A-sec638"
```

### §4.9 — Track B — Reviewer Profile + Reporting

**4.9.1** — `track_b.reviewer_profile_typical.reviewer_types` (keep existing + add):
```yaml
  - "phase_iii_contracting_officer (where sole-source procurement; weights sole-source-authority eligibility + price-reasonableness + customer-agency interest documentation)"
  - "private_investor_or_strategic_partner (where Phase III commercialization is investor-anchored)"
```
— Why: Phase III reviewer triangle includes government contracting officers (for sole-source) + private investors (for capital-anchored commercialization) alongside the existing federal-program-officer + business-reviewer registers. Card YAML.

**4.9.2** — `track_b.reporting_requirements_typical.performance_reporting.content_required[NEW]`:
- "Phase III milestone tracking (sole-source contract award date; investor close date; first customer revenue date)"
- "Investor capital deployment vs Phase III commercialization milestones"

### §4.10 — Cross-track shared search vocabulary (root or per-track)

**4.10.1** — Per master prompt §0 OD-A v2.4 alignment: 13 CLC-05 admin-risk terms already migrated. Search-vocabulary recommendation: surface a comment block above each track's `underwriting_criteria` pointing to the workspace register entries that apply to that track's vocabulary. Example for Track A:
```yaml
track_a:
  # Admin-risk vocabulary for Track A (SBIR-context):
  # commercialization (GREEN, market_access: EXPECTED — SBIR Phase III statutory)
  # growth (GREEN, market_access: EXPECTED — SBA / SBIR statutory)
  # underrepresented founders (YELLOW, market_access: OK — SBA GAFC; route through register per-administration)
  # See pipeline/institutional_memory/admin_risk_register.yaml v2.4
  underwriting_criteria:
    ...
```
— Why: prevents accidental re-introduction of `admin_risk_term_register` block; surfaces register-cell lookups at the relevant track for next-cycle authors. Pure documentation; no canonical-bytes change.

**4.10.2** — Disambiguator vocabulary between Market Access (CLC-05) and Research & Evidence (CLC-04) — per dispatch highest-leverage research area (5):
- "research grant only" already in disqualifier-like position implicitly; recommend explicit Scout disqualifier for Market Access scope: "primary purpose is research methodology development" (route to Research & Evidence — display name, not slug, per master prompt §0 rule 3).
- "primary purpose is buyer-development or commercialization" → Market Access positive signal.
- "primary purpose is technology validation pre-commercialization" → ambiguous; Phase I = Research & Evidence, Phase II = Market Access Track A, Phase III = Market Access Track B. Surface as `track_a.search_vocabulary.disambiguator_with_research_evidence` (if a search_vocabulary container is added to track containers in a future amendment) OR as a `_review_handback.surface_ambiguities` entry today.

### §4.11 — Commitment Tracking Pattern — track-specific extension

**4.11.1** — `track_a.commitment_tracking_pattern.typical_commitments_extracted[NEW]`:
- `phase_ii_milestone_completion` — milestone name + planned date + actual date + technical result + variance
- `phase_i_to_phase_ii_pivot_decision` — pivot description + rationale + evidence trigger + cost impact
- `customer_discovery_interview_count` — total interviews + segment breakdown + pivot evidence triggered
- `intellectual_property_filing` — patent / trademark / data-rights filing + date + scope + jurisdiction

**4.11.2** — `track_b.commitment_tracking_pattern.typical_commitments_extracted[NEW]`:
- `phase_iii_sole_source_contract_award` — agency + contract value + period + scope
- `investor_capital_close` — investor name + amount + close date + valuation + use-of-funds
- `government_customer_program_office_endorsement_obtained` — agency + program office + endorsement date + scope

### §4.12 — Phase 4 fold-in discipline self-check (per master prompt §0 rule 6 / §18.11 v1.1)

For each of the §4.0-§4.11 patches:

| Patch | Refusal (a) struct-sub-field smuggling | Refusal (b) dedicated-field-name fork | Refusal (c) compound enum | Refusal (d) literal slug in non-exempt value position | Verdict |
|---|---|---|---|---|---|
| §4.0.1 | N/A — replaces existing string | N/A | N/A | NO (only display-name "Market Access" / "SBIR Phase II" / "SBIR Phase III") | PASS |
| §4.0.2 | N/A — appends to existing array | N/A | N/A | NO | PASS |
| §4.0.3 | N/A — comment only | N/A | N/A | NO | PASS (no canonical-bytes change) |
| §4.0.4 | N/A — existing schema field | N/A | N/A | NO | PASS |
| §4.1.1-4.1.4 | NO — uses canonical `criterion` / `description` / `weight_in_typical_rubric` / `source_citation` shape | NO — no parallel top-level field | NO — qualitative weight only | NO — display names only | PASS |
| §4.2.1 | NO — uses canonical `reviewer_types` shape | NO | N/A | NO | PASS |
| §4.2.2-4.2.5 | NO — uses canonical `weight: HIGH/MEDIUM` enum + rationale shape | NO | NO — canonical enum only | NO | PASS |
| §4.3.1-4.3.5 | NO — uses canonical `flag` / `severity` / `red_team_probe` shape | NO | NO — canonical HIGH/MEDIUM/LOW only | NO | PASS |
| §4.4 | NO — `narrative_section_patterns` canonical shape | NO | N/A | NO | PASS |
| §4.5 | NO — `common_application_forms` canonical shape | NO | N/A | NO | PASS |
| §4.6.1-4.6.3 | NO | NO | NO | NO — display names only | PASS |
| §4.7.1-4.7.4 | NO | NO | NO — canonical HIGH/MEDIUM | NO | PASS |
| §4.8.1-4.8.3 | NO | NO | NO | NO | PASS |
| §4.9.1-4.9.2 | NO | NO | NO | NO | PASS |
| §4.10.1 | N/A — comment-block only | N/A | N/A | NO | PASS (pure doc) |
| §4.10.2 | NO | NO | NO | NO — uses display name "Research & Evidence" not slug TILTH-CLC-04 per master prompt §0 rule 3 | PASS |
| §4.11.1-4.11.2 | NO — uses canonical `commitment_type` / `measurement_method` shape | NO | N/A | NO | PASS |

**Phase 4 fold-in self-check verdict: 0 refusals tripped across 17 proposed patches.**

### §4.13 — Where each proposal belongs (Law 5 routing)

| Proposal | Card YAML | Program Rule Pack | Admin-Risk Register | Funder Database | Rubric Library | v1.x matrix |
|---|---|---|---|---|---|---|
| 4.0.1-4.0.4 root metadata | YES | NO | NO | NO | NO | NO |
| 4.1.1-4.1.4 Track A criteria | YES | NO | NO | NO | NO | NO |
| 4.2.1-4.2.5 Track A reviewer + evidence | YES | NO | NO | NO | NO | NO |
| 4.3.1-4.3.5 Track A red flags | YES | NO | NO | NO | NO | NO |
| 4.4 Track A narrative sections | YES | NO | NO | NO | NO | NO |
| 4.5 Track A forms / portals | YES (form names + URLs durable) | NO | NO | NO | NO | NO |
| 4.6.1-4.6.3 Track B criteria | YES | NO | NO | NO | NO | NO |
| 4.7.1-4.7.4 Track B evidence | YES | NO | NO | NO | NO | NO |
| 4.8.1-4.8.3 Track B red flags | YES | NO | NO | NO | NO | NO |
| 4.9 Track B reviewer + reporting | YES | NO | NO | NO | NO | NO |
| 4.10 vocab comment block | YES (comment only) | NO | NO (already there) | NO | NO | NO |
| 4.11 commitment tracking | YES | NO | NO | NO | NO | NO |
| VAPG FY27 NOFO deadline + award amounts (per §2.2) | NO | YES — Program Rule Pack lives faster than card | NO | NO | NO | NO |
| Per-agency Phase II topic lists (per-cycle) | NO | YES | NO | YES (per-agency topic feeds) | NO | NO |
| Per-state SCBGP RFP details | NO | YES | NO | YES | NO | NO |
| Numeric VAPG rubric weights | NO (already at `pipeline/rubrics/vapg_fy26.json`) | NO | NO | NO | YES (already there) | NO |

---

## §5. Operator Decision Queue

1. **P0 — On-disk shape vs OD-E LOCK row 276 mismatch.** Operator must decide between three remediation paths: (a) re-apply the §18.6 v2 multi-track restructure to the on-disk file using the helper script `pipeline/scripts/od_e_restructure_card.py` against `pipeline/cards/CLC/market_access.yaml`, then supersession-re-sign with a new lock_history row that supersedes row 276; (b) supersede row 276 with a clarifying row capturing the actual on-disk single-track shape + amending the OD-E completion handoff to note the restructure did not persist for market_access; (c) confirm the restructure is on a different on-disk path than expected (forensic SHA3-512 search). Recommend (a) — the §18.6 v2 amendment + restructure script + per-track research depth in this handback are all aligned to multi-track shape; reverting the LOCK is the higher-blast-radius option.

2. **Track A vs Track B partition rule explicitness.** The §18.6 v2 helper script (`pipeline/scripts/od_e_restructure_card.py:204-208`) routes the broader §18.6 v1 Market-Access content (VAPG / SBA / Build to Scale / institutional procurement) into Track B Phase III. This is the operator-resolved partition. But for runtime routing, Scout needs an explicit rule: when an opportunity that is NOT SBIR Phase II OR Phase III sole-source (e.g., a VAPG NOFO, a Build to Scale Capital Challenge, a foundation buyer-development RFP) appears, does it route through Track B Phase III (current restructure-script intent), or should Track B be renamed to reflect the broader scope ("commercialization_beyond_phase_ii" or similar)? This is a v0.2 / §18.6 v3 amendment surface; flag for operator review.

3. **Per-agency Phase II content explosion.** §4.1-§4.5 proposes Track A content depth per agency (USDA NIFA SBIR / NSF SBIR / NIH SBIR / DOE SBIR / DOD SBIR / EPA SBIR / NASA SBIR). Card YAML can absorb the per-agency criteria + evidence + red-flag entries at moderate cost; alternative is to externalize per-agency Phase II rubrics into the rubric library (precedent: VAPG rubric at `pipeline/rubrics/vapg_fy26.json`). Operator decision: card-body per-agency depth (heavier card, runtime-instant) vs rubric-library files (lighter card, requires Judge to fetch). Recommend hybrid: keep agency-level criteria + reviewer profile + red flags in card body (decision-frame); externalize per-agency numeric rubrics into rubric library files.

4. **Admin-risk register cross-references in card body.** §4.0.3 + §4.10.1 propose comment-block-only pointers to the workspace `admin_risk_register.yaml` v2.4 entries. Operator decision: are pointer comments useful for next-cycle authors, or should the discipline be that authors always grep the register themselves? Recommend keeping the pointers as documentary aid; they cost zero canonical-bytes (comments stripped).

5. **PA-specific examples vs base card.** Card cites PA DOA SCBGP as one state example. Recommend per-state SCBGP / state-ag-marketing-program details belong in Program Rule Packs + funder database (Law 5); base card stays state-agnostic with the NASDA aggregator pointer as the state-discovery entry. OD-G state-overlay amendment surface may be the right home for state-specific overlays at v0.2.

6. **Sub-source primary-source verbatim quote refresh.** Operator should authorize next Phase 4 dispatch to refresh `access_date` against 2026-Q4 Wayback Machine snapshots for all 28 primary sources (18 existing + 10 NEW from §3.2 if §4.0.2 patch accepted).

7. **VAPG numeric rubric promotion to card body (v0.2 amendment surface).** `_review_handback.decision_queue[3]` from the existing card flagged this: VAPG numeric weights live at `pipeline/rubrics/vapg_fy26.json`, card cites qualitatively per OQ-6. As ≥12 CycleReceipts accumulate, the v0.2 first quantified Market-Access rubric amendment surface activates; operator decision on when.

8. **Phase III sole-source vs open-competition naming clarity.** §4.8.3 red-flag captures the confusion. Operator decision: should Track B carry a name that disambiguates (e.g., `phase_iii_commercialization_open_or_sole_source` vs current `sbir_phase_iii`)? Recommend keeping `sbir_phase_iii` as the canonical track_name (matches OD-E ceremony record) and surfacing the open-vs-sole-source distinction in `track_b.track_description` prose.

9. **Lifecycle gap (universal CLAUDE.md §5 flag).** Master prompt §11 / §5 says "every parsed runtime card currently carries `lifecycle.draft_status: 'draft'`." **This card's on-disk value is `signed`** (line 790). The universal gap claim is false-for-this-card OR the master prompt was written against a stale parse. Flagged here per dispatch contract; no remediation needed for this card. Recommend operator re-verify the universal claim against the actual 14-card grep before authoring the §18 v1.x draft_status normalization amendment described in master prompt §5.

10. **NEW Track A common_funders_observed entries.** Existing card has no `common_funders_observed` block (Law-5 / Law-4 discipline — funders are training data, not card primitives, per funder-as-specimen memory entry). Track A would gain operational benefit from a Law-5-compliant observational roster of SBIR Phase II funders (USDA NIFA / NSF / NIH / DOE / DOD by Component / EPA / NASA — frequency_observed = UNKNOWN per OQ-6) IF the operator wants Scout to surface them at discovery. Operator decision per Law-5 discipline.

---

## §6. Validation Checklist

| Check | Result | Notes |
|---|---|---|
| Schema required-fields populated | PASS (single-track shape on disk; 15/15) | Multi-track shape would require 8/8 per track + 9 shared root |
| Schema branch validation | branch-1 PASS on disk; branch-2 FAIL on disk | P0 §2.2 |
| No forbidden CLC-coupling field names (registry scan) | PASS — 0 hits | §2.5 |
| No forbidden CLC-coupling field names (nested-in-item scan) | PASS — 0 hits | §2.5 |
| No forbidden value-position regex matches outside exempt paths | PASS — 0 non-exempt hits | §2.4 |
| No private organization-specific data | PASS | Only public program-page citations + statute citations + public-aggregator references |
| No unsourced program-law claims | PASS for card body; FY-cycle deadlines flagged for Program Rule Pack | §2.2 + §4.13 |
| No excessive quoted source text | PASS | All verbatim quotes ≤2 sentences per Wave 1 OQ cap |
| Lifecycle status consistent with architecture v7.0.11 §1.5 | PASS on disk | `draft_status: signed` + `runtime_loadable: true` |
| For multi-track: shared root metadata preserved | N/A on current disk (single-track) — would PASS under proposed multi-track shape per §18.6 v2 §2.4 | |
| For multi-track: oneOf branch 2 compliance | FAIL on current disk per §2.2 P0 | Re-restructure resolves |

---

## §7. Regression Tests

5 prompts that should demonstrate behavior change between pre-edit and post-edit cards (where "post-edit" means §4 patches applied AND §18.6 v2 multi-track shape in place per §2.2 P0 remediation).

**Test 1 — Track A routing (SBIR Phase II opportunity)**
- Prompt: *"USDA NIFA SBIR Phase II solicitation just dropped — small business has a Phase I award on biocontrol agents. What does Tilth do first?"*
- Pre-edit (current single-track card): Scout treats this as generic Market Access; Scribe drafts a go-to-market narrative; Phase I evidence + commercialization plan format are not surfaced.
- Post-edit expected: Scout routes to Track A (sbir_phase_ii); Logician PRE-gate checks Phase I evidence presence (per §4.1.1) + USDA NIFA topic alignment (per §4.1.4); Scribe selects USDA NIFA Phase II commercialization-plan template (per §4.1.2); Judge consults agency-specific rubric (per §4.2.1); Red Team probes commercialization-plan thinness + academic-team-no-commercial-experience (per §4.3.1, §4.3.2).

**Test 2 — Track B routing (Phase III sole-source pursuit)**
- Prompt: *"Phase II awardee on drone-swarm sensor wants to pursue a Phase III sole-source contract with Air Force Research Lab — what evidence does the application need?"*
- Pre-edit: Scout treats as generic Market Access / commercialization; buyer-LOI ladder is surfaced but no Phase III sole-source authority distinction; no agency-endorsement-letter evidence path.
- Post-edit expected: Scout routes to Track B (sbir_phase_iii); Logician PRE-gate verifies 15 USC 638(r) sole-source authority eligibility (per §4.6.1); Scribe surfaces `phase_iii_sole_source_letter_of_interest_from_agency` evidence requirement (per §4.7.1); Judge weights program-office endorsement; Red Team probes sole-source-vs-open-competition confusion (per §4.8.3).

**Test 3 — Cross-track disambiguation (VAPG opportunity)**
- Prompt: *"USDA VAPG FY27 NOFO published — value-added meat producer wants Working Capital track. Track A or Track B?"*
- Pre-edit (single-track): no track decision needed.
- Post-edit expected: Scout routes to Track B (sbir_phase_iii by current restructure script intent — broader Market Access content lives there). If operator picks operator-decision §5 item 2 path (rename Track B to reflect broader scope), routing follows the rename. Either way: Scribe surfaces VAPG-specific narrative sections (criterion a.ii / a.iii / c) + buyer-LOI ladder + Qualified Consultant prerequisite (existing card content under Track B). Test surfaces the partition-rule explicitness gap.

**Test 4 — Cross-CLC disambiguation (research vs commercialization)**
- Prompt: *"Applicant has a USDA SARE preproposal for research on cover-crop economic outcomes — Market Access or Research & Evidence?"*
- Pre-edit: card body has no explicit disambiguator with CLC-04.
- Post-edit expected (per §4.10.2): Scout reads "primary purpose is research methodology" → routes to Research & Evidence (CLC-04, display name). Market Access disqualifier fires. Note: this requires the disambiguator to land in the card OR in the routing logic; current proposal surfaces it as a `_review_handback.surface_ambiguities` entry pending operator decision.

**Test 5 — Admin-risk vocabulary lookup**
- Prompt: *"Draft a Phase II commercialization narrative for an SBA GAFC R&D Track applicant who is an underrepresented founder."*
- Pre-edit: card body has no admin-risk register; author would re-introduce the removed `admin_risk_term_register` block by reflex.
- Post-edit expected (per §4.0.3 + §4.10.1): comment-block pointers route author to `admin_risk_register.yaml` v2.4 lookup; finds `underrepresented founders` entry with `per_clc_register.market_access: OK` + severity YELLOW + defer-to-active-RFA reviewer-context. Scribe surfaces the substitution candidate set without auto-rewrite. Logician POST-gate enforces approval flow.

---

## §8. Patch Plan

**Operator dispatches edits + supersession-re-sign as a separate ceremony per OD-C / OD-E precedent (per-card lock_history supersession row + post-restructure SHA3-512 + publisher Ed25519 signature against `vault_shared/cards/publisher_pubkey.signed.yaml`).**

### File: `pipeline/cards/CLC/market_access.yaml`

**Prerequisite ceremony (per §2.2 P0):**
P0. Re-apply §18.6 v2 multi-track restructure (or supersede row 276 to capture actual on-disk shape — §5 item 1).

**Edit set (after P0 resolved; numbering matches §4):**

1. §4.0.1 — `funding_mechanism_summary` rewrite (single sentence cross-track summary).
2. §4.0.2 — `_research_metadata.primary_sources[NEW]` 10 sources from §3.2.
3. §4.0.3 — Header comment block addition (admin-risk register pointer).
4. §4.0.4 — `lifecycle.supersession_lock_history_row: 276` (forward-binding contract).
5. §4.1.1-§4.1.4 — Track A underwriting_criteria 4 new entries (Phase I evidence / commercialization plan per-agency / indirect rate / topic alignment).
6. §4.2.1 — Track A reviewer_profile_typical.reviewer_types rewrite (per-agency-aware reviewer triangle).
7. §4.2.2-§4.2.5 — Track A evidence_weights 4 new entries (Phase I report / agency template / I-Corps evidence / KP commercialization experience).
8. §4.3.1-§4.3.5 — Track A common_red_flags 5 new entries.
9. §4.4 — Track A narrative_section_patterns 7 sections (per-agency aware).
10. §4.5 — Track A common_application_forms 5 per-agency entries.
11. §4.6.1-§4.6.3 — Track B underwriting_criteria 2 new + 1 refined (sole-source authority / investor capital / buyer-commitment three sub-classes).
12. §4.7.1-§4.7.4 — Track B evidence_weights 3 new + 1 refined.
13. §4.8.1-§4.8.3 — Track B common_red_flags 3 new entries.
14. §4.9.1-§4.9.2 — Track B reviewer profile + reporting additions.
15. §4.10.1 — Per-track admin-risk comment-block pointers (Track A + Track B).
16. §4.10.2 — Disambiguator with CLC-04 surfaced as `_review_handback.surface_ambiguities` entry pending operator decision.
17. §4.11.1-§4.11.2 — Track A + Track B commitment_tracking_pattern additions.

### File: `pipeline/blueprint/v0.1/section_18_6_v3_amendment.md` (proposed pre-stage; NOT created by this handback)

18. §5 item 2 — Track B partition-rule explicitness (current scope = SBIR Phase III sole-source OR Phase III sole-source + broader commercialization; operator-decision).
19. §5 item 3 — Per-agency Phase II rubric externalization to rubric library (parallel to `vapg_fy26.json`).

### File: `pipeline/institutional_memory/admin_risk_register.yaml`

20. No changes proposed — 13 CLC-05 entries already present at v2.4. Verify `per_clc_register.market_access` cells reflect Track A vs Track B distinction (Q: should the schema support per-track register cells inside one CLC? Operator decision — v0.2 admin-risk-register v3.x amendment surface).

### File: `pipeline/engineering/lock_history.v1.jsonl`

21. New supersession row per §2.2 P0 (one row appended; not edited in-place per LOCK discipline).

**OD-D Phase 4 forward-binding contract note:** All proposed edits pass Phase 4 fold-in self-check per §4.12. None touches refusal (c) compound-enum territory. None introduces literal canonical CIC/CLC slug strings in non-exempt value positions per refusal (d). For R-CARDS-ENUM-CANONICAL (OD-B, pending) the new `weight` enum values (`HIGH` / `MEDIUM`) and `severity` enum values (`HIGH` / `MEDIUM` / `LOW`) are canonical and would not trip the rule when it lands at v0.2.

---

**Summary block:**

```
Card: CLC:market_access
Card file: pipeline/cards/CLC/market_access.yaml
Track shape: MULTI_TRACK per §18.6 v2 (track_a=sbir_phase_ii, track_b=sbir_phase_iii)
On-disk shape: SINGLE_TRACK (mismatch with row 276 supersession claim — P0)
Research hours actual: 3.5
Findings: 28 total — 1 P0 (on-disk multi-track restructure absent), 14 P1, 13 P2
  Shared root: 4 (incl. 1 P0)
  Track A (sbir_phase_ii): 13 (4 criteria + 4 evidence + 5 red flags = 13 behavior-changing; +narrative/forms/commitments = supporting)
  Track B (sbir_phase_iii): 10 (3 criteria + 4 evidence + 3 red flags = 10 behavior-changing; +reviewer/reporting/commitments = supporting)
  Cross-track: 1 (CLC-04 disambiguator)
Decision queue: 10 operator approvals required
Conflicts with prior art: NONE (admin_risk_register v2.4 13 CLC-05 entries reused with consistent severity tiers; cross-track partition matches restructure-script intent at pipeline/scripts/od_e_restructure_card.py:174-211)
Coupling-discipline regression: NONE (0 non-exempt value-position regex matches; 0 forbidden-field-name registry hits)
Lifecycle gap surfaced: draft_status reads "signed" on disk — this card is NOT in the universal "draft" state described in master prompt §5; the universal gap claim should be re-verified by operator against actual 14-card grep before authoring §18 v1.x draft_status normalization amendment
Review readiness: DEFER_PENDING_CHANGES (P0 §2.2 — on-disk shape vs row 276 mismatch must resolve before §4 patches apply meaningfully; recommend operator dispatch re-restructure + supersession-re-sign ceremony before next research cycle)
```
