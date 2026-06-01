# TILTH-CIC-01 Food Systems — Research Handback

**Filed:** 2026-05-17
**Workspace:** `/Users/goldenquill/Downloads/GoldenQuill/`
**Run:** Run 2 of operator's controlled-batch sequence (Phase 4 CIC handbacks; 1 of 6).
**Card:** `pipeline/cards/CIC/food_systems.yaml` (Wave 1 LOCKed 2026-05-15 row 226; SHA-256 `7aafd0…cc1a`; signed `2026-05-15T20:30:00Z`).
**Authority chain:** master prompt `docs/cic_clc_unified_master_prompt_2026-05-17.md` §2 (per-card output shape) + plan `docs/cic_clc_unified_research_plan_2026-05-17.md` §1.1 (priority vectors) + Run 1 priors at `docs/card_system_deep_research_2026-05-17/` (binding).
**Run 1 priors folded in:**
- All 14 cards on disk are `draft_status: "signed"` (P0-3 / L1-F0 — no normalization needed).
- §18 v1.2 dialect_routing_table re-keying is LOCKed-but-not-applied (L2-F0 / P0-1).
- Operator v2.1 Law-5 split on `common_funders_observed` is uniformly applied across all 6 CIC cards (L2-F5 / Phase 2 §6.3).
- F-CARDS-COUPLING-VIOLATION-EXTENSION predicate body raises `NotImplementedError` at runtime (L1-F3 / P1-1) — value-position regex is spec-only today.
- Operator reframe: this card is "first unit / unlocked"; aggressive content improvements OK to recommend; re-signing ceremony cost acceptable.

---

## §1. Card Impact Thesis

`food_systems` is the Wave 1 reference card and the deepest precedent in the CIC body for shape, comment density, and Law-5 / Law-4 discipline. Its job is to make Tilth read agricultural-producer, food-hub, value-added-processor, conservation, and farm-to-school applicants as **operating realities with seasonal cash-flow, production proof, buyer proof, and safety/compliance constraints** — and to make Scout / Scribe / Judge / Logician honor those realities at runtime without sliding into either greenwashing prose or activist signaling that disqualifies a federal application.

What this card should *cause Tilth to do differently* relative to a sector-naive baseline:

1. When Scout sees "value-added agriculture" in an opportunity, anchor on the USDA VAPG 7 CFR 4284 Subpart J statutory definition, NOT generic foundation-prose readings.
2. When Scribe drafts a producer narrative, force buyer-LOI + production-record + match-documentation evidence prompts rather than soft impact prose.
3. When Logician audits a draft using "regenerative agriculture" or "food sovereignty," surface admin-risk-register tier + reviewer-context + substitution candidates — NEVER silently rewrite.
4. When Judge evaluates the dialect routing, the funder-political-axis dimension that currently keys routing (LOCKed-but-pending re-key to CLC-keyed per §18 v1.2) drives sub-register selection (business_commercial / ecological_conservation / community_benefit) per the active opportunity.
5. When Archivist captures lessons, the FY26 NRCS Regenerative Pilot $700M scope, the SCBGP state-pass-through path, and the PA Ag Innovation Grant 50% non-state match rule belong in Program Rule Packs (live program law), NOT in card body — the card carries the *grammar*, the Pack carries the *law*.

The runtime-behavior delta this card should produce versus a sector-naive baseline is **specificity of evidence demanded + precision of register selected + restraint at admin-risk-flagged vocabulary**. The card is currently strong on (1)–(3); (4) is bottlenecked on the §18 v1.2 cards-ceremony; (5) is partially achieved (some 2026 cycle dates already moved out; some, like NRCS Regenerative Pilot FY26 dollar amounts, still live in admin-risk reviewer-context prose).

---

## §2. Current State Audit

### §2.1 What is strong now

- **Statutory-anchor density.** Every `search_vocabulary.core_terms[*].source_citation` cites a CFR Subpart, statute, or named USDA program page. 17/17 core_terms carry source_citation; FY26 Regenerative Pilot, SARE regional structure, AFRI six-priority structure, and VAPG/LAMP/SCBGP component breakdowns are precisely cited.
- **Sub-register triad.** The `register_defaults.sub_registers` block at lines 298–322 is the Cycle-1 F-01 fold output — three explicitly named sub-registers (business_commercial / ecological_conservation / community_benefit) with `sub_register_selection_rule` prose at lines 315–322 making Scribe's runtime selection rule explicit. The C2-01 fix-in-place removed the `typical_clc_contexts` field that constituted a design-time CIC × CLC coupling violation.
- **Evidence-signal weighting.** Ten evidence kinds with HIGH/MEDIUM weights, freshness_tolerance_days per kind (180 / 365 / 730), and per-kind source_citation. The buyer-LOI freshness window at 180d and conservation-plan window at 730d reflect actual USDA program expectations.
- **Provenance discipline.** Five fact-classes (annual_revenue / certifications_held / buyer_relationships / conservation_practices_in_place / operator_priority_category) carry explicit `required_citation_type` + `verbatim_quote_required` flags. buyer_relationships requires verbatim — this matches USDA VAPG reviewer expectation that letter-of-intent terms be quotable.
- **Phase E Option 2 Law-5 cleanup.** Top-level `common_funders_observed: []` at line 626 + `_research_metadata.draft_funder_candidates_pending_operator_engagement_confirmation:` at line 808 carries the 12 candidates correctly. The pattern is the canonical CIC reference for the Law-5 split.
- **Lifecycle truth.** `draft_status: signed`, `signature_status: signed`, `runtime_load_status: loaded`, `runtime_loadable: true`, `content_hash: sha256:7aafd0…cc1a`, `signed_at: 2026-05-15T20:30:00Z`, `signed_by: founder`, `lock_history_row: 226`, `lock_timestamp_utc: 2026-05-15T20:30:00Z` — fully consistent with architecture v7.0.11 §1.5 production-load requirements (per Run 1 Phase 1 §4 table).

### §2.2 What is stale, ambiguous, over-broad, too local, too federal, or under-sourced

- **`dialect_routing_table` keys on retired axis.** Lines 326–345 use `funder_political_axis: conservative | centrist | progressive | soul_fire` per the v1.1 schema. The §18 v1.2 amendment (LOCKed 2026-05-16T14:00:00Z) retired this enum and prescribes `clc + dialect + register_description + example_program` per-row. **Not a card body defect** — the amendment LOCKed without the companion card-ceremony firing. Bottlenecked on the cards-ceremony per Run 1 Patch Queue Batch B. See §5 / §8.
- **NRCS Regenerative Pilot FY26 dollar amounts in reviewer_context.** Line 391–397 carries program-law detail ("Term peaked under prior administration"). Also at lines 731–737 the `_research_metadata.primary_sources` block quotes the NRCS Regenerative Pilot $700M total verbatim. The verbatim quote in primary_sources is correct (it's a research-trail citation), but the *summary* prose at line 391–397 risks staleness when the next administration shifts framing. Recommended: keep the verbatim quote in primary_sources, soften the "term peaked under prior administration" gloss in reviewer_context to "term framing varies by administration; verify per active RFA."
- **EPA EE / NEETP `frequency_observed: RARE` entry.** Line 866–875 carries a 6-line operator-defensive rationale. The Cycle-1 F-03 fold preserved this entry deliberately ("eligible-edge-case applicant whose work otherwise falls outside USDA"); the rationale is operator-defensible. No change. **But** the entry is fragile to EPA program-realignment under current administration framing — flag for re-confirmation when the operator's next engagement cycle touches food-systems education.
- **`disqualifier_terms` length is thin (3 entries).** "personal use," "research grant only," "indirect non-agricultural use" are correct but under-cover the disqualifier landscape. Missing: "non-rural applicant" (kills RCDG / SDGG eligibility), "FSA-ineligible commodity" (kills CSP/EQIP eligibility for some practices), "ESOP-only" (kills VAPG / cooperative-priority routing — separate cooperative discipline).
- **`evidence_signals` missing climate-adaptation evidence pattern.** No `kind` for risk-disclosure / climate-vulnerability assessment. USDA SARE + AFRI increasingly weight climate-adaptation framing; some 2024-2025 RFAs added climate-resilience evidence weight. Cross-cuts with admin-risk discipline on "climate-smart agriculture" — when the term IS retained verbatim per the active RFA, evidence pattern should also be present.
- **`metrics_table_template` 6 entries — under-covers institutional procurement.** "annual sales revenue / number of buyers / units produced / acres under conservation practice / producers reached or trained / jobs created or retained" is the right starter set, but misses: pounds-of-produce-to-institution (USDA Farm to School), gallons-of-milk-or-other-perishable-distributed (LFPP / RFSP), volunteer-hours-coordinated (BFRDP partnerships), CSA-share-equivalents (community-food framing). Recommended additions.
- **`common_risk_register_entries` "overclaiming regenerative / sustainable / organic impact" risk.** Lines 608–614 — mitigation_pattern correctly routes to NRCS practice codes + Logician admin-risk register. Strong. **But** the `likelihood: MEDIUM` understates the actual operator-defensible likelihood — every regenerative-framed proposal Tilth touches will hit this risk. Recommended: tighten to HIGH × HIGH; the mitigation is already adequate.
- **No `farm_to_school` and no `urban_agriculture` core_term.** USDA FNS Patrick Leahy Farm to School Grant is named in funder_program_keywords on the educator card and in food_systems' priors_consulted, but `farm-to-school` doesn't appear as a search_vocabulary core_term on food_systems. Same for urban agriculture — a frame USDA has explicitly programmatized via the Urban Agriculture and Innovative Production Grant (UAIPG). These should be on food_systems Scout vocabulary.
- **`narrative_sections_typical` is 13 items — typical structure.** Strong. One missing item: "Project Partnership and Letters of Support" — separately broken out from "Eligibility Narrative" because USDA VAPG/BFRDP/LFPP all weight LOIs / partnerships as a discrete scoring criterion; the current "Match / Cost Share Documentation" section captures the dollar-side but not the relationship-side.
- **`compliance_burdens` does not name H-2A or seasonal labor compliance.** Producers above a certain employee count routinely encounter H-2A; H-2A compliance is reviewer-relevant on any VAPG / RCDG cooperative-producer application with hired-labor scope. Recommended addition.
- **Verbatim source quotes age out.** Primary sources (lines 685–790) are dated `access_date: 2026-05-15`. Annual re-verification against Internet Archive snapshot is the §18.11 discipline; recommend the next Phase 4-CIC re-dispatch confirm Wayback Machine snapshots of every primary_source URL.

### §2.3 Lifecycle / signature / schema concerns

- **`draft_status: signed`.** No normalization needed (per Run 1 Phase 1 §3.2 / Patch A1 retirement of master prompt §5's stale claim).
- **Header comment drift (P1-4).** Line 28: `# Lifecycle: draft. NO Ed25519 signature. Operator review pending before Wave 1 LOCK ceremony as separate dispatch.` This is stale — file has been signed since 2026-05-15T20:30:00Z. Recommend update to `# Lifecycle: signed (Wave 1 LOCK row 226, 2026-05-15T20:30:00Z). Ed25519 signature present at _research_metadata.ed25519_signature; content_hash present at lifecycle.content_hash.` Header comments are not in canonical bytes (stripped by YAML parser before `canonical_bytes()` hash) — pure documentation-only edit; no re-sign required.
- **`dialect_routing_table` v1.1 shape still active.** Schema mismatch with the LOCKed §18 v1.2 amendment is intentional per Run 1 — the cards-ceremony fires the patch. Card body is conformant with the *current on-disk* schema (`pipeline/cards/_schema/card_cic.schema.json:208-274` still v1.1 shape per Run 1 Phase 2 §3.1).
- **`_research_metadata.draft_funder_candidates_pending_operator_engagement_confirmation` field not schema-known.** Per Run 1 Patch B20 — the field passes via `_research_metadata.additionalProperties: true` but the schema doesn't declare it. Cross-card normalization opportunity; route to cards-ceremony per Run 1 Patch Queue Batch B.
- **Lock-history housekeeping.** `lifecycle.lock_history_row: 226` + `lifecycle.lock_timestamp_utc: 2026-05-15T20:30:00Z` + `lifecycle.supersession_lock_history_row` absent (no supersession yet). These three optional fields are not in `models.py.Lifecycle` (per Run 1 L1-F8); the canonical-bytes-exclusion set does NOT exclude `lock_history_row`/`lock_timestamp_utc`/`supersession_lock_history_row` (per Run 1 L1-F7). Any future cards-ceremony supersession that updates `lock_history_row` will invalidate `content_hash` and force re-sign — meaning the cards-ceremony for §18 v1.2 dialect_routing_table re-keying ALSO needs to budget for re-sign-on-lock-history-row-update. Operator decision: graduate these fields into `models.py.Lifecycle` + canonical-bytes-exclusion set, OR remove them from schema (Run 1 Patch E1).

### §2.4 Coupling-discipline self-audit (per master prompt §2 item 2 + Run 1 enforcement-context guidance L1-F3)

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

**Results (grep transcript at `pipeline/cards/CIC/food_systems.yaml`):**

| Line | Path | Match | Exempt? |
|---|---|---|---|
| 1 | (YAML header comment) | `TILTH-CIC-01` | YES — comments are not in canonical bytes (stripped by YAML parser before `canonical_bytes()`); not in scanner surface |
| 33 | `card_id` | `TILTH-CIC-01` | YES — `_VALUE_POSITION_EXEMPT_PATHS` |
| 38 | `tilth_cic_id` | `TILTH-CIC-01` | YES — `_VALUE_POSITION_EXEMPT_PATHS` |
| 672 | `_research_metadata.priors_consulted[1].extract_note` | `TILTH-CIC-01` | YES — `_research_metadata` top-level key starts with `_` |
| 674 | `_research_metadata.priors_consulted[2].extract_note` | `TILTH-CIC-01` | YES — same exempt subtree |
| 680 | `_research_metadata.priors_consulted[6].extract_note` | `TILTH-CIC-01` + "Customer Identity Categories" | YES — same exempt subtree |

**Verdict — LIVE regex set: 0 non-exempt findings.** Card passes.

### §2.5 Legacy-phrase defense scan (per Run 1 Phase 2 L2-F3 — not in current regex set; surface as defense-in-depth)

Grep for `[Cc]ustomer [Ii]nformation` across the card: 0 hits.

**Verdict — legacy-phrase defense-in-depth: 0 findings.** No regression risk.

---

## §3. Research Findings

### §3.1 Source verification table — official + primary

| URL | Type | Access date | Fields supported | Confidence |
|---|---|---|---|---|
| https://www.rd.usda.gov/programs-services/business-programs/value-added-producer-grants | official | 2026-05-15 (card primary_sources line 686) | VAPG eligible-applicant types (Agricultural Producer / Producer Group / Farmer or Rancher Cooperative / Majority-Controlled Producer-Based Business Venture); criterion-a.i / a.iii / b / d scoring framing; planning grant ≤$50K + working capital grant ≤$200K | HIGH |
| https://www.ecfr.gov/current/title-7/subtitle-B/chapter-XLII/part-4284/subpart-J | official | 2026-05-15 (card primary_sources line 694) | VAPG statutory regulation; eligibility / project content / review procedures | HIGH |
| https://www.sare.org/ | official | 2026-05-15 (card primary_sources line 697) | "USDA's only farmer-driven federal research program"; four-regional structure (Northeast, North Central, South, West) | HIGH |
| https://www.nifa.usda.gov/grants/programs/agriculture-food-research-initiative | official | 2026-05-15 (card primary_sources line 705) | AFRI six priority areas + three program structure (FAS / SAS / EWD) | HIGH |
| https://www.ams.usda.gov/services/grants/scbgp | official | 2026-05-15 (card primary_sources line 714) | SCBGP statutory framing; state-pass-through ("Only state departments of agriculture may apply") | HIGH |
| https://www.ams.usda.gov/services/grants/lamp | official | 2026-05-15 (card primary_sources line 721) | LAMP umbrella (FMPP + LFPP + RFSP) | HIGH |
| https://www.nrcs.usda.gov/programs-initiatives/regenerative-pilot-program | official | 2026-05-15 (card primary_sources line 729) | NRCS Regenerative Pilot FY26 scope ($400M EQIP + $300M CSP); admin-risk register basis for "regenerative agriculture" entry | HIGH |
| https://www.nrcs.usda.gov/programs-initiatives/conservation-stewardship-program | official | 2026-05-15 (card primary_sources line 738) | CSP five-year contract structure | HIGH |
| https://www.pa.gov/services/pda/apply-for-the-agricultural-innovation-grant | official | 2026-05-15 (card primary_sources line 741) | PA Ag Innovation Grant award range ($5K–$200K individual) + 50% non-state match requirement | HIGH |
| https://www.nifa.usda.gov/grants/programs/beginning-farmer-rancher-development-program-bfrdp | official | 2026-05-15 (card primary_sources line 748) | BFRDP partnership requirement (collaborative network applicant only) | HIGH |
| https://www.rd.usda.gov/programs-services/business-programs/rural-cooperative-development-grant-program | official | 2026-05-15 (card primary_sources line 755) | RCDG nonprofit-only eligibility + cooperative-development scope | HIGH |
| https://www.epa.gov/education/grants | official | 2026-05-15 (card primary_sources line 764) | EPA EE program scope ($200K–$250K, 16 grants nationwide) | MEDIUM (program under current-administration realignment review) |
| https://www.heinz.org/grants | official (foundation) | 2026-05-15 (card primary_sources line 771) | Heinz Endowments Food Systems portfolio framing | HIGH |
| https://www.iatp.org/new-regenerative-agriculture-initiative-greenwashing | practitioner | 2026-05-15 (card primary_sources line 780) | IATP commentary on "regenerative agriculture" definitional landscape — labeled as practitioner input to operator-defensive substitution candidates | MEDIUM (explicitly framed as non-adjudicative in card body) |
| https://nffc.net/what-we-do/food-sovereignty/ | practitioner | 2026-05-15 (card primary_sources line 788) | NFFC food-sovereignty framing — basis for admin_risk_term_register "food sovereignty" entry | MEDIUM (movement-aligned framing; operator decides per RFA) |

### §3.2 New / refreshed sources to verify and add

| URL | Type | Why add | Card fields it would support | Confidence |
|---|---|---|---|---|
| https://www.fns.usda.gov/cfs/farm-school-grant-program | official | `farm_to_school` is a documented Scout vocabulary gap on this card; currently only on educator card | New `search_vocabulary.core_terms` entry + `funder_program_keywords` entry + likely new `kfr_fact_classes.farm_to_school_partnership` | HIGH (USDA FNS authoritative) |
| https://www.nifa.usda.gov/grants/programs/urban-agriculture-innovative-production-grant | official | UAIPG is a 2022-introduced statutory program absent from current card; urban agriculture is an under-represented vocabulary | New `funder_program_keywords` entry + `core_terms.urban_agriculture` + `disqualifier_terms` refinement (rural-only programs do NOT serve urban applicants — already partly captured in CIC-03 disqualifier_terms but specifically missing here) | HIGH |
| https://www.ams.usda.gov/services/local-regional/lamp/farmers-market-promotion | official | LAMP component (FMPP) is named but the cost-share / award-range specifics need refresh against FY26 NOFO if available | refresh `funder_program_keywords[FMPP]` source_citation | HIGH |
| https://www.dol.gov/agencies/whd/agriculture/h2a | official | H-2A seasonal-labor compliance is reviewer-relevant on producer applications with hired-labor scope; currently absent from `compliance_burdens` | New `compliance_burdens` entry | HIGH |
| https://www.fsa.usda.gov/programs-and-services/farm-loan-programs/farm-operating-loans/index | official | FSA Operating / Microloans are working-capital pathway separate from VAPG / NRCS — many food-systems producers stack these | refresh `_research_metadata.draft_funder_candidates_pending_operator_engagement_confirmation` — likely add FSA Direct Operating + Microloan | HIGH |
| https://www.usda.gov/topics/farming/climate-smart-commodities | official | Partnerships for Climate-Smart Commodities (PCSC) sunset under current administration; verify status — admin-risk-term context | refresh reviewer_context on "climate-smart agriculture" admin_risk_term entry | MEDIUM (program status in flux) |
| https://www.usda.gov/initiatives/local-and-regional-food-systems | official | Cross-program USDA local/regional food synthesis page — useful for the Scout-to-CLC routing thinking the cards-ceremony will need | sets up `_research_metadata.priors_consulted` row 7 for the next Phase 4 dispatch | MEDIUM |
| https://www.rd.usda.gov/programs-services/farm-labor-housing-direct-loans-grants | official | Farm Labor Housing program — adjacent to producer applicants employing seasonal labor; cross-program | new `funder_program_keywords` row only if operator scope extends to housing-side capital readiness; otherwise route to v0.2 Wave 3 grant-side-credit-readiness CLC backlog item per L-024 | MEDIUM |
| https://www.iatp.org/ (homepage; check for updated 2026 publications) | practitioner | IATP regenerative-greenwashing publication is dated; check for refreshed 2026 piece for reviewer_context anchoring | refresh `admin_risk_term_register["regenerative agriculture"]` reviewer_context | LOW (movement-side; not authoritative) |
| https://attra.ncat.org/ | practitioner | ATTRA / NCAT — USDA-funded but operationally independent — useful for "regenerative practices" + farmer technical-assistance references; useful for `evidence_signals` cross-reference | optional `_research_metadata.priors_consulted` addition | MEDIUM |
| https://www.sustainableagriculture.net/ | practitioner | NSAC policy commentary — useful for tracking program status changes across administrations | optional `_research_metadata.priors_consulted` addition | MEDIUM |

### §3.3 Internet Archive snapshot verification (per master prompt §2 read-first item 7)

Recommended next Phase 4-CIC pass: verify Wayback Machine snapshots of every URL in `_research_metadata.primary_sources` (15 URLs). Specifically the EPA EE / NEETP URL — high risk of program-page restructuring under current administration. The IATP and NFFC practitioner URLs should also be Wayback-verified because they're cited as movement-side framing anchors and movement-side org websites tend to redesign without redirect maps.

---

## §4. Proposed Card Improvements

Grouped by the eight runtime-behavior categories per master prompt §2 "Research task." Each proposal: exact YAML path, why-it-improves-runtime, target-seat, and where-it-belongs (card body vs Program Rule Pack vs admin-risk-register vs funder-DB vs matrix-layer-v1.x). Phase 4 fold-in discipline self-check at the end of §4.

### §4.1 search_vocabulary / classification

- **`search_vocabulary.core_terms[NEW]` — add `farm-to-school`.** Source_citation = USDA FNS Patrick Leahy Farm to School Grant Program. Why: Scout currently won't fire on `farm-to-school` text in an opportunity unless the educator card is also LIVE in the seat-context — which is opportunity-driven at runtime per architecture v7.0.11 §6.1, not always the case for a food-systems-leading opportunity. **Seat affected:** Scout. **Where:** card body.
- **`search_vocabulary.core_terms[NEW]` — add `urban agriculture` + `controlled environment agriculture (CEA)`.** Source_citation = USDA NIFA UAIPG + UA-Innovation-Production statutory category. Why: urban-ag producers are routinely mis-routed to USDA RD rural-only programs by sector-naive Scouts. **Seat affected:** Scout + Logician (rural-only-disqualifier discipline). **Where:** card body.
- **`search_vocabulary.disqualifier_terms[NEW]` — add `urban applicant for rural-only program` + `ESOP-only applicant for cooperative-priority program`.** Why: current disqualifier_terms (3 entries) under-cover the disqualifier landscape. **Seat affected:** Logician. **Where:** card body.
- **`search_vocabulary.synonym_map[NEW]` — add `urban_agriculture` mapping.** Synonyms: `community garden`, `rooftop farm`, `vertical farm`, `controlled environment`, `hydroponic`, `aquaponic`. **Seat affected:** Scout. **Where:** card body.
- **`search_vocabulary.synonym_map[NEW]` — add `farm_to_school` mapping.** Synonyms: `school food procurement`, `K-12 procurement`, `local food in schools`, `producer-to-school`, `school garden producer`. **Seat affected:** Scout. **Where:** card body.
- **`search_vocabulary.funder_program_keywords[NEW]` — add `Urban Agriculture and Innovative Production Grant (UAIPG)`.** Funder = USDA NIFA / Office of Urban Agriculture and Innovative Production. **Seat affected:** Scout + Logician. **Where:** card body.
- **`search_vocabulary.funder_program_keywords[NEW]` — add `Patrick Leahy Farm to School Grant`.** Funder = USDA FNS. **Seat affected:** Scout. **Where:** card body. (Cross-references educator card — orthogonality holds; the same federal program serves both producer-side and school-side applicants and a CIC × CLC at runtime is opportunity-driven per architecture v7.0.11 §6.1.)
- **`search_vocabulary.funder_program_keywords[NEW]` — add `FSA Direct Operating Loan` + `FSA Microloan`.** Funder = USDA Farm Service Agency. **Seat affected:** Scout. **Where:** Belongs in card body for Scout vocabulary, but per L-024 the *underwriting logic* for these is CLC-06 credit_underwriting territory (Track A debt; FSA is non-CDFI farm credit but underwriting-logic-equivalent). Card body addition is Scout-side only — no CLC coupling implied.

### §4.2 evidence capture / missing-evidence prompts

- **`evidence_signals[NEW]` — add `climate_resilience_assessment`.** source_pattern = "documented climate-risk assessment for operation: precipitation trend, heat-stress days, frost-date shifts, drought-decadal projection; or NRCS Soil Survey vulnerability assessment; or Cooperative Extension regional-climate risk-management worksheet." weight = MEDIUM. freshness_tolerance_days = 1095. source_citation = USDA SARE climate-adaptation priorities + NRCS Climate Hub + USDA AFRI Climate Resilience priority area. Why: SARE / AFRI / SCBGP 2024–2025 RFAs increasingly weight climate-adaptation framing; without an evidence_signal anchor Scribe must extemporize. **Seat affected:** Scribe + Logician. **Where:** card body.
- **`evidence_signals[NEW]` — add `institutional_procurement_buyer_history`.** source_pattern = "signed institutional procurement agreement(s) from named buyer with volume + price + cadence + term; cumulative annual institutional revenue ledger." weight = HIGH. freshness_tolerance_days = 365. source_citation = USDA RFSP + LFPP institutional-procurement framing + Farm to School Grant Program expectations. Why: institutional-procurement-buyer evidence is a HIGH-weight signal that distinguishes producer-side aggregator/hub work from direct-to-consumer farming and currently is folded into the generic `buyer_letters_or_letters_of_intent` signal; institutional buyers behave differently (multi-year contracts, K-12 procurement rules, FSMA-tier compliance). **Seat affected:** Scribe + Logician. **Where:** card body.
- **`evidence_signals[REFINE]` — refine `food_safety_certification`.** Currently lists GAP / GHP / FSMA Produce Safety Rule / USDA Organic / third-party. Add per evidence-pattern bullet: "Hazard Analysis and Risk-Based Preventive Controls (HARPC) certification for value-added processors" + "AIB International / SQF for institutional buyer compliance." Why: VAPG value-added projects at scale routinely require HARPC, not just GAP/GHP. **Seat affected:** Scribe + Logician. **Where:** card body.

### §4.3 KFR fact classes + provenance_requirements

- **`kfr_fact_classes[NEW]` — add `production_seasonality`.** description = "monthly / quarterly production calendar with peak harvest windows, off-season operations, post-harvest handling capacity." typical_provenance = "crop plan; harvest log; livestock production schedule." Why: cash-flow / match-timing / reporting cadence all depend on seasonality which is currently implicit. **Seat affected:** Scribe + Judge + Logician. **Where:** card body.
- **`kfr_fact_classes[NEW]` — add `food_safety_certification_chain`.** description = "applicant-side cert + named third-party verifier + cert renewal cycle + scope of certification (commodity + facility + handler)." typical_provenance = "certifying body letter; audit report; cert renewal calendar." Why: more granular than the current `certifications_held` fact-class which mixes certs across types. **Seat affected:** Logician + Judge. **Where:** card body.
- **`provenance_requirements[NEW]` — add `production_seasonality` entry.** required_citation_type = "crop plan or harvest log signed by operator or production manager with year + month columns." verbatim_quote_required = false. Why: pairs with the new kfr_fact_class. **Seat affected:** Logician. **Where:** card body.
- **`provenance_requirements[REFINE]` — refine `buyer_relationships`.** Already requires verbatim. Add path-pattern detail: "verbatim buyer name + commitment terms (volume, price, term, cadence) preserved in source document; if buyer requires anonymity, signed Letter of Commitment from intermediary with anonymized buyer reference + Cooperative Extension or producer-association attestation of buyer identity." Why: institutional buyers (school districts, hospitals) routinely require confidentiality in producer applications — current provenance_requirements language doesn't accommodate. **Seat affected:** Scribe + Logician. **Where:** card body.

### §4.4 drafting register / admin-risk handling (Law 4 + OD-A v2.4)

- **`admin_risk_term_register[REFINE]` — soften `regenerative agriculture` reviewer_context.** Current line 391–397 says "Term peaked under prior administration; current USDA framing pivoted to 'regenerative' + 'Farmer First' language." This conflates two administrations (pre-2021 and 2025-) into a single timeline. Recommended rewrite: "Term framing varies by administration and by funder type. USDA NRCS uses 'regenerative' officially in the Regenerative Pilot Program (FY26). Most foundations and many state agencies use 'regenerative' broadly; conservative federal review climates may treat it as politically loaded. When applying to centrist / technical reviewers, substituting to NRCS-named practice codes (cover crop, no-till, rotational grazing) reads as more precise. Keep verbatim when the active RFA uses the term or when funder's own materials use it as primary frame. Operator decides per application; Tilth does not adjudicate definitional dispute." **Seat affected:** Scribe + Logician. **Where:** card body. **Per Law 4 + OQ-5:** approval_required: true preserved.
- **`admin_risk_term_register[REFINE]` — refine `climate-smart agriculture` reviewer_context.** Current line 391–397 says "Term peaked under prior administration." Add: "Partnerships for Climate-Smart Commodities (PCSC) program was the largest federal climate-smart funding mechanism through 2024–2025; program status under current administration is in flux (verify against active RFA before assuming program is operational). FAO and foundation funders continue using climate-smart vocabulary." Why: program-status fact, not term-politics fact, is what changes year-over-year. **Seat affected:** Scribe + Logician. **Where:** card body.
- **`admin_risk_term_register[NEW]` — add `frontline community`.** severity = MEDIUM. substitution_candidates = ["distressed-community service area", "Census ACS LMI service area", "high-vulnerability community per CEJST tier-2 or higher"]. reviewer_context = "Term carries movement-side framing tied to Justice40 era. Substitute to functional descriptors anchored to statutory or recognized indices (LMI, CDC SVI, EPA EJScreen, CEJST). For soul-fire-aligned funders, retain verbatim per active RFA." approval_required = true. Why: term appears in some food-system / food-equity applications; currently no substitution discipline. **Seat affected:** Scribe + Logician. **Where:** card body.
- **OD-A admin_risk_register v2.4 cross-flag check.** The 8 admin_risk_term_register entries on this card (food sovereignty / regenerative agriculture / climate-smart agriculture / land back / climate justice / decolonize / anti-capitalist / DEI / equity / inclusion) span both CIC-side (food sovereignty, land back, regenerative agriculture, climate-smart agriculture) and CIC-shared (DEI, climate justice, decolonize, anti-capitalist) terms. Per OD-A v2.4 the cross-shared terms (DEI, climate justice, decolonize, anti-capitalist) are candidates for workspace-register migration once a cross-CIC consolidation dispatches. Route to operator decision queue as cross-CIC normalization candidate; **do NOT auto-migrate from this dispatch.**

### §4.5 reviewer / rubric logic

- **`register_defaults.sub_register_selection_rule[REFINE]`.** Current text (lines 315–322) says "Scribe selects the sub-register matching the active CLC (identified at runtime per opportunity) plus the funder dialect from `dialect_routing_table`." After §18 v1.2 cards-ceremony fires, `dialect_routing_table` re-keys to CLC + dialect + register_description; the selection rule then becomes implicit (the row carries the dialect already). Pre-ceremony, the rule is correct. Post-ceremony, the rule should be refined to clarify that the sub-register IS the matching `dialect_routing_table[*].dialect` row's runtime register. Defer to cards-ceremony dispatch.
- **`narrative_sections_typical[NEW]` — add `"Project Partnership and Letters of Support"` between `"Key Personnel and Qualifications"` and `"Budget and Budget Justification"`.** Why: USDA VAPG/BFRDP/LFPP separately weight partnership; current `narrative_sections_typical` 13 items conflates this into `"Eligibility Narrative"`. **Seat affected:** Scribe. **Where:** card body.

### §4.6 red-team probes (admin-risk register)

- **`common_risk_register_entries[REFINE]` — `overclaiming regenerative / sustainable / organic impact`.** Currently `likelihood: MEDIUM` / `impact: HIGH`. Tighten to HIGH × HIGH. Why: every regenerative-framed proposal Tilth touches will hit this risk; calibrating MEDIUM understates the practical hit rate.
- **`common_risk_register_entries[NEW]` — add `seasonal labor compliance gap`.** likelihood = MEDIUM. impact = HIGH. mitigation_pattern = "H-2A documentation completeness if applicable; state seasonal-employment labor certification; for cooperative-producer applicants, member-vs-employee classification clarity per state law." Why: VAPG / RCDG applicants employing seasonal labor at any scale encounter H-2A or state-equivalent compliance routinely; absent risk-register coverage means Scribe doesn't surface the question early. **Seat affected:** Logician + Scribe. **Where:** card body.
- **`common_risk_register_entries[NEW]` — add `FSMA Produce Safety Rule exemption-loss risk`.** likelihood = MEDIUM. impact = HIGH. mitigation_pattern = "Track Produce Safety Rule small-farm exemption threshold (~$25K-$500K sliding scale per 21 CFR Part 112 — verify per FDA reissuance); any project that crosses applicant past the threshold or that brings new produce onto the operation triggers full FSMA covered-farm compliance." Why: PCSR small-farm-exemption loss is a routine reviewer challenge for value-added projects at moderate scale. **Seat affected:** Logician. **Where:** card body.

### §4.7 reporting / commitment extraction (CLC-side; partial CIC-side applies)

This category is primarily CLC-side. CIC-side relevance: the `reporting_cadence_typical` block at lines 463–476 captures per-funder reporting cadence with 10 funder entries. **Refine:** add USDA Patrick Leahy Farm to School Grant + USDA UAIPG (Urban Agriculture) + USDA RFSP regional food system reporting cadence entries (currently absent). **Seat affected:** Archivist + Report Generator. **Where:** card body.

### §4.8 memory namespace usefulness

Per architecture v7.0.11 §1.9: `cards:cic:food_systems:*` is the namespace. Recommend the following sub-keys be standardized (for future Scout / Scribe consumption when seat-registration graduates per v0.2 first-wave loader):

- `cards:cic:food_systems:scout_vocabulary` → search_vocabulary
- `cards:cic:food_systems:evidence_signals` → evidence_signals
- `cards:cic:food_systems:kfr_fact_classes` → kfr_fact_classes
- `cards:cic:food_systems:provenance_requirements` → provenance_requirements
- `cards:cic:food_systems:register_defaults` → register_defaults
- `cards:cic:food_systems:dialect_routing_table` → dialect_routing_table (post-cards-ceremony, re-keyed to CLC-keyed shape)
- `cards:cic:food_systems:admin_risk_terms` → admin_risk_term_register
- `cards:cic:food_systems:reporting_cadence` → reporting_cadence_typical
- `cards:cic:food_systems:metrics_template` → metrics_table_template
- `cards:cic:food_systems:narrative_sections` → narrative_sections_typical
- `cards:cic:food_systems:capacity_signals` → capacity_signals_required
- `cards:cic:food_systems:compliance_burdens` → compliance_burdens
- `cards:cic:food_systems:common_risks` → common_risk_register_entries
- `cards:cic:food_systems:common_funders_observed` → common_funders_observed (live; operator-confirmed-engagement-only)
- `cards:cic:food_systems:draft_funder_candidates` → `_research_metadata.draft_funder_candidates_pending_operator_engagement_confirmation` (pre-engagement; not for runtime authority)

**Seat affected:** all consuming seats. **Where:** architecture v7.0.11 §1.9 sets the namespace pattern; the per-card sub-key map is a v0.2 first-wave loader concern; the seat-registry depends-on-field mapping per Run 1 Patch D5 is the right home. Surface to operator as a v0.2 loader-graduation enumeration question.

### §4.9 Phase 4 fold-in discipline self-check (per master prompt rule 6 / §18.11 v1.1)

Each proposed change above scanned against the four refusals:

| Proposal | (a) structured-sub-field expansion on canonical entries? | (b) dedicated-field-name fork? | (c) compound enum value? | (d) literal canonical CIC/CLC slug in non-exempt value position? |
|---|---|---|---|---|
| §4.1 core_terms add `farm-to-school` + `urban agriculture` + `CEA` | NO — adds new items, canonical item shape preserved | NO | NO | NO |
| §4.1 disqualifier_terms add `urban applicant for rural-only program` + `ESOP-only applicant` | NO | NO | NO | NO |
| §4.1 synonym_map add `urban_agriculture` + `farm_to_school` | NO — additions to canonical object | NO | NO | NO |
| §4.1 funder_program_keywords add UAIPG / Farm-to-School / FSA Direct Operating + Microloan | NO | NO | NO | NO |
| §4.2 evidence_signals add `climate_resilience_assessment` + `institutional_procurement_buyer_history` | NO | NO | NO | NO |
| §4.2 evidence_signals refine `food_safety_certification` | NO — refines source_pattern within canonical item shape | NO | NO | NO |
| §4.3 kfr_fact_classes add `production_seasonality` + `food_safety_certification_chain` | NO | NO | NO | NO |
| §4.3 provenance_requirements add `production_seasonality` + refine `buyer_relationships` | NO | NO | NO | NO |
| §4.4 admin_risk_term_register refine `regenerative agriculture` + refine `climate-smart agriculture` | NO — refines reviewer_context prose | NO | NO | NO |
| §4.4 admin_risk_term_register add `frontline community` | NO | NO | NO | NO |
| §4.5 register_defaults.sub_register_selection_rule refine (post-cards-ceremony) | NO | NO | NO | NO |
| §4.5 narrative_sections_typical add `"Project Partnership and Letters of Support"` | NO | NO | NO | NO |
| §4.6 common_risk_register_entries tighten `overclaiming regenerative impact` + add `seasonal labor compliance gap` + `FSMA exemption-loss risk` | NO | NO | NO — uses canonical HIGH × HIGH / MEDIUM × HIGH | NO |
| §4.7 reporting_cadence_typical add USDA Farm-to-School / UAIPG / RFSP | NO | NO | NO | NO |
| §4.8 memory namespace sub-keys | N/A — architecture decision, not card body | N/A | N/A | N/A |

**Verdict:** No proposed change trips any of the four Phase 4 fold-in refusals.

---

## §5. Operator Decision Queue

Decisions that require Josh / operator approval before any patch dispatches:

1. **Admin-risk-register cross-CIC normalization for shared terms.** DEI / equity / inclusion appears on this card AND on educator AND on public_agency AND on cooperative AND on arts_culture AND on ecosystem_intermediary. Per OD-A v2.4 pattern, ≥3-card recurrence is the migration-to-workspace-register threshold. The five additional shared terms (climate justice / decolonize / anti-capitalist / DEI / equity / inclusion) are migration candidates. **Surface as P0 for operator decision: should these five terms migrate to `admin_risk_register.yaml` v3.0 with `per_clc_register` cells (and `per_cic_register` cells once the schema permits)?** This is a workspace-register schema-extension decision, not a card-body decision. Route to v2.x → v3.0 scrub workflow per master prompt §7.
2. **`regenerative agriculture` reviewer_context refresh.** Current prose conflates pre-2021 and 2025-administration framings. Proposed §4.4 rewrite is operator-grade — needs operator sign-off before re-sign. **Approval required:** YES per OQ-5 default.
3. **`climate-smart agriculture` reviewer_context program-status refresh.** Partnerships for Climate-Smart Commodities (PCSC) status under current administration is in flux; the card should be updated to reflect program status. Needs operator confirmation of PCSC operational status as of dispatch date. **Approval required:** YES.
4. **`frontline community` admin_risk_term_register addition.** Proposed §4.4 NEW entry — needs operator approval per OQ-5 default.
5. **Urban Agriculture and Innovative Production Grant (UAIPG) Scout vocabulary addition.** Operator may have a preference about whether UAIPG belongs primarily on `food_systems` or on `ecosystem_intermediary` (UA-intermediary is a thing); current proposal lands UAIPG on `food_systems` per producer-side framing. Operator decides.
6. **Farm-to-School cross-CIC orthogonality posture.** Patrick Leahy Farm to School Grant is named on `educator` already. Adding it to `food_systems` is producer-side framing; the program serves both. Per architecture v7.0.11 §6.1 CIC × CLC orthogonality and per cards-ceremony Law-5 discipline, listing the same program on two CICs is fine (it's funder grammar, not CIC × CLC binding). But operator may want to lead-CIC the program for the cross-CIC Scout vocabulary registry. **Recommended posture: dual-list; operator-side runtime decides lead-CIC per opportunity (per architecture v7.0.11 §6.1, opportunity-driven CLC matching applies to CIC orientation too).** Operator decides.
7. **FSA Direct Operating Loan + FSA Microloan addition.** These are debt-side instruments. Adding to `food_systems` Scout vocabulary is fine (it's a federal program in the producer-applicant funding landscape). The underwriting logic is CLC-06 Track A debt — not a CIC × CLC coupling because the CIC vocabulary entry doesn't encode CLC preference. Operator decides.
8. **State-overlay PA-specific entries.** `PA Ag Innovation Grant` and `Pennsylvania Department of Agriculture` are PA-anchored entries in `funder_program_keywords` and `_research_metadata.draft_funder_candidates_pending_operator_engagement_confirmation`. Per master prompt §1.5 + OD-G state-overlay design: do these belong in base card OR in PA-state overlay? **Recommended posture: keep in base card per current Wave 1 precedent; v0.2 Wave 3 OD-G state-overlay dispatch can extract per the operator's then-active multi-state deployment scope.** Operator decides.
9. **OD-A v2.4 cross-flag check.** Per master prompt §7: "Card-body `admin_risk_term_register` entries that are repeated across CLCs are the migration candidates per the OD-A pattern. Card-body entries that are CIC-side and applicant-specific stay on the CIC card." `food sovereignty` / `regenerative agriculture` / `climate-smart agriculture` / `land back` are CIC-side, applicant-specific — they stay. The shared terms (DEI / climate justice / decolonize / anti-capitalist) are workspace-register candidates. Operator decides per cross-CIC consolidation timing.
10. **Lock-history housekeeping field disposition.** Per Run 1 Patch E1: `lifecycle.lock_history_row` / `lock_timestamp_utc` / `supersession_lock_history_row` are schema-only with no `models.py` mirror. Operator decides: graduate them into `models.py.Lifecycle` + canonical-bytes-exclusion set, OR remove from schema. This is a cross-card decision; not specific to `food_systems`. Surface to cards-ceremony.
11. **Re-signing ceremony budget for card body changes.** Per operator reframe ("first units / unlocked"): aggressive content improvements OK to recommend; re-signing ceremony cost acceptable. The §4 proposals above touch ~25 distinct card-body edits. Bundle them into the cards-ceremony per Run 1 Patch Queue Batch B as `food_systems` supersession-re-sign? Or run them as a separate Phase 4-CIC-derived content refresh ceremony? **Recommendation:** bundle into the cards-ceremony if §4.5 register_defaults.sub_register_selection_rule refinement is in-scope post-§18 v1.2 (since both touch the same file). Otherwise sequence as separate content-refresh dispatch after cards-ceremony lands the §18 v1.2 / §18.6 v2 reconciliation.

---

## §6. Validation Checklist

| Check | Result | Evidence |
|---|---|---|
| Schema fields complete against current §18.5 / §18.6 schema | PASS | 15/15 required CIC fields present per `card_cic.schema.json:7-23`; lifecycle block satisfies allOf conditional at lines 468–520 (runtime_loadable=true → draft_status=signed AND signature_status=signed AND runtime_load_status=loaded; signed_at/signed_by/content_hash present) |
| No forbidden coupling field names (top-level + nested per item-level not.anyOf) | PASS | Grep across the file: none of 7 forbidden CIC-side names (`common_clc_patterns_observed`, `eligible_clc_subset`, `clc_allowlist`, `clc_denylist`, `preferred_clcs`, `clc_win_rate`, `clc_ranking_preferences`) appear anywhere |
| No forbidden value-position regex matches outside exempt paths | PASS | Per §2.4 above — 0 non-exempt findings; all hits are in `card_id` / `tilth_cic_id` / `_research_metadata.priors_consulted[*].extract_note` |
| No legacy-phrase `[Cc]ustomer [Ii]nformation` matches (defense-in-depth) | PASS | 0 hits — verified by grep |
| No private organization-specific data in card body | PASS | Top-level common_funders_observed is empty list; subagent-populated candidates in `_research_metadata.draft_funder_candidates_pending_operator_engagement_confirmation` carry only program/funder names, no client-specific data |
| No unsourced program-law claims | PASS at body | Verbatim quotes ≤2 sentences per OQ-4 throughout; program statutory anchors are CFR / USC / official agency page cited per OQ-3. **Minor exception:** the FY26 NRCS Regenerative Pilot $700M and FY26 PA Ag Innovation Grant $10M dollar amounts are program-law (active appropriation cycle); per master prompt §1.5 these belong in Program Rule Packs not card body — current card carries them only in `_research_metadata.primary_sources` verbatim quotes (correct), not in operational fields. PASS. |
| No excessive verbatim source text | PASS | Verbatim quotes capped at ≤2 sentences per primary_source row per OQ-4 |
| Lifecycle status consistent with architecture v7.0.11 §1.5 production-load requirements | PASS | All five lifecycle gate fields at pass-state; runtime_loadable=true; content_hash present; signed_at + signed_by present |
| **Top-level `common_funders_observed:` is empty (Law-5 split per operator v2.1 reconciliation)** | PASS | Line 626 `common_funders_observed: []`; `_research_metadata.draft_funder_candidates_pending_operator_engagement_confirmation` at line 808 carries 12 subagent-populated candidates as expected |
| **No populated top-level `common_funders_observed` without operator-engagement-attestation** | PASS | Empty list; no Law-5 violation surface present |
| For multi-track CLCs: shared root metadata + oneOf branch 2 compliance | N/A — this is a CIC card |

**Net coupling-discipline regression: 0 findings.**

---

## §7. Regression Tests

3–5 prompts that should demonstrate behavior change between pre-edit and post-edit cards. Each prompt + expected pre-edit behavior + expected post-edit behavior + which seat changes.

### Test 1 — Urban agricultural producer prompt

**Prompt:** "We're an urban farm in Pittsburgh running a 1-acre rooftop hydroponic specialty-crop operation. We want to apply for USDA grant funding to expand to a second rooftop site."

**Pre-edit behavior (current Scout vocabulary):**
- Scout matches `specialty crop`, `agricultural producer` — routes toward USDA AMS SCBGP, USDA VAPG; suggests value-added analysis.
- Scout does NOT surface USDA NIFA UAIPG or any urban-ag-specific pathway because `urban agriculture` is not in core_terms.
- Logician does NOT pre-disqualify USDA RD CF / RBDG rural-only programs because the `urban applicant for rural-only program` disqualifier is absent — applicant is routed inefficiently.

**Post-edit behavior (with §4.1 additions):**
- Scout matches `urban agriculture` + `specialty crop` — routes toward USDA NIFA UAIPG (primary) and USDA AMS SCBGP / FMPP (secondary for direct-marketing-to-consumer extension).
- Scout matches `controlled environment agriculture (CEA)` synonym — surfaces same UAIPG + AMS SCBGP routing.
- Logician pre-disqualifies USDA RD CF / RBDG rural-only programs because `urban applicant for rural-only program` disqualifier_term fires.
- Result: applicant routed to UAIPG and AMS programs in first response; USDA RD rural-only programs not surfaced as candidates.

**Seat affected:** Scout + Logician. **Pass criterion:** Scout candidate-program list includes UAIPG; USDA RD CF / RBDG NOT included with a disqualifier note.

### Test 2 — K-12 school district food-procurement partnership prompt

**Prompt:** "A regional aggregator wants to apply for USDA funding to grow institutional procurement with three K-12 school districts. The aggregator pools produce from 15 small producer-cooperative members; districts have committed to a 5-year procurement schedule."

**Pre-edit behavior:**
- Scout matches `food hub`, `institutional procurement`, `farmer or rancher cooperative` — routes toward LFPP, RFSP, VAPG.
- Scout does NOT surface USDA FNS Patrick Leahy Farm to School Grant because `farm-to-school` is absent from `food_systems` core_terms (only on `educator` card).
- Scribe drafts narrative without explicit Farm-to-School framing — misses a primary federal-program match.
- `institutional_procurement_buyer_history` is not a discrete evidence_signal — Scribe folds institutional buyer evidence into `buyer_letters_or_letters_of_intent`.

**Post-edit behavior (with §4.1 + §4.2 additions):**
- Scout matches `farm-to-school` core_term (new) + `food hub` (existing); routes to LFPP + RFSP + Patrick Leahy Farm to School Grant + VAPG.
- Scribe surfaces Farm-to-School framing as a candidate dialect — runs the dialect_routing_table sub-register matching against active opportunity.
- `institutional_procurement_buyer_history` evidence_signal fires (HIGH weight) — Scribe surfaces multi-year district procurement-commitment evidence with 365-day freshness and explicit institutional-procurement provenance discipline.
- Result: applicant prompted for institutional-procurement-specific evidence early; Patrick Leahy Farm to School added to funder shortlist; cross-CIC orthogonality preserved (food_systems lead; educator card available if Scout / Logician identify educator-side scope at runtime).

**Seat affected:** Scout + Scribe + Logician. **Pass criterion:** Patrick Leahy Farm to School Grant appears in Scout output; `institutional_procurement_buyer_history` evidence_signal fires when applicant invokes institutional-buyer language.

### Test 3 — Regenerative-language admin-risk discipline

**Prompt:** "We're a regenerative cattle operation in central Pennsylvania looking to apply for USDA NRCS funding for soil-health practices and a USDA SARE producer grant."

**Pre-edit behavior:**
- Scribe drafts with "regenerative agriculture" verbatim throughout (NRCS Regenerative Pilot accepts; the card's admin_risk_term_register reviewer_context says "Keep 'regenerative' verbatim when the active RFA uses the term").
- Logician fires admin_risk_term_register["regenerative agriculture"] at MEDIUM severity, surfaces substitution candidates, requires operator approval per approval_required: true.
- Cycle 1 reviewer_context says "Term peaked under prior administration" — operator approves once, may be confused by the prior-administration framing.

**Post-edit behavior (with §4.4 refined reviewer_context):**
- Scribe drafts with "regenerative agriculture" verbatim where active RFA (NRCS Regenerative Pilot) uses the term; for SARE producer-grant narrative, defaults to NRCS-named practice codes (cover crop, no-till, rotational grazing) per refined reviewer_context.
- Logician fires admin_risk_term_register["regenerative agriculture"] at MEDIUM severity; reviewer_context is admin-neutral (does not conflate pre-2021 + 2025-administration framings); operator approves once with clearer context.
- Result: same operational outcome; tighter operator-decision time spent on regenerative-substitution per application.

**Seat affected:** Scribe + Logician. **Pass criterion:** Scribe routes "regenerative" verbatim when NRCS Regenerative Pilot is the active RFA; substitutes to practice codes when active RFA is SARE technical-precise; Logician's admin-risk reviewer_context reads admin-neutral.

### Test 4 — Climate-resilience evidence surfacing

**Prompt:** "We're a Mid-Atlantic mixed-crop farm in extreme-heat-vulnerable region applying to USDA AFRI Climate-Resilience priority and to NRCS EQIP for cover-crop expansion."

**Pre-edit behavior:**
- Scribe draws on evidence_signals (sales_ledger, buyer_letters, production_records, soil_test_or_conservation_plan) — no climate-resilience-specific evidence signal.
- Scribe extemporizes climate-vulnerability claims without prompted evidence pattern; reviewer reads as vague impact prose.
- `common_risk_register_entries` includes "weather variance / crop failure" with MEDIUM × HIGH but no specific climate-adaptation evidence anchor.

**Post-edit behavior (with §4.2 new evidence_signal):**
- `climate_resilience_assessment` evidence_signal fires (MEDIUM weight, 1095-day freshness window) — Scribe prompts for NRCS Climate Hub regional-risk worksheet OR Cooperative Extension regional climate-adaptation assessment OR documented precipitation/heat-stress/frost-date local trend.
- Provenance discipline applies — `provenance_requirements` extends to climate_resilience_assessment with citation type clarity.
- Result: applicant prompted for AFRI-relevant climate-resilience evidence at intake; not pushed to drafting without evidence-pattern anchor.

**Seat affected:** Scribe + Logician. **Pass criterion:** `climate_resilience_assessment` evidence_signal surfaces in intake when AFRI Climate-Resilience priority is the active RFA.

### Test 5 — Cards-ceremony post-condition (dialect_routing_table re-keyed to CLC)

**Prompt:** "We're a beginning farmer cooperative aiming at USDA AFRI's Sustainable Agricultural Systems priority area for a research-and-development grant on regenerative livestock genetics."

**Pre-cards-ceremony behavior:**
- Scribe reads `dialect_routing_table` keyed on `funder_political_axis: centrist`, dialect `scribe.technical_precise`. The `funder_political_axis` value carries no per-CLC reasoning — Scribe selects sub_register heuristically based on AFRI being a research program.
- Logician routes underwriting logic to CLC-04 research_evidence per opportunity-driven matching at runtime (not encoded in card body — orthogonality preserved).
- Pre-ceremony, the dialect_routing_table row carries the retired political axis.

**Post-cards-ceremony behavior (per Run 1 Patch B2–B7 + operator §18 v1.2 content-judgment re-key):**
- `dialect_routing_table` row re-keys to `clc: research_evidence` + `dialect: scribe.technical_precise` + `register_description: "research-rigor technical-precise register for federal NIFA research panels; PIs + program managers expect biosketch-grade methodology disclosure"` + (optional) `example_program: "USDA AFRI Sustainable Agricultural Systems"`.
- Scribe selects sub_register from CLC + dialect explicitly — no funder-political-axis intermediary.
- Same operational outcome for this opportunity (research-precise register) but no political-axis primary key.
- Result: post-ceremony, dialect_routing rows are CLC-keyed; political-axis enum is fully retired from runtime.

**Seat affected:** Scribe + Judge. **Pass criterion:** Pre-ceremony card body validates against current schema v1.1; post-ceremony validates against §18 v1.2 schema. Same proposal routing for this opportunity; political-axis enum absent from re-signed card.

---

## §8. Patch Plan

Edits proposed in this handback grouped by file path. **No edits applied from this dispatch.** Operator dispatches each ceremony separately per the OD-C / OD-E precedent.

### File: `pipeline/cards/CIC/food_systems.yaml`

**Ceremony shape:** supersession-re-sign per OD-E precedent (row 276 / 277 / 278 model). Parent_lock_row = 226 (Wave 1 LOCK). Ceremony_parent_row = `<NEXT-AVAILABLE-COMPOUND-PARENT>` if bundled with cards-ceremony, OR `<NEXT-AVAILABLE>` standalone.

**Edit set:**

1. Header comment normalization (line 28). Per Run 1 Patch A4 — documentation-only, comments not in canonical bytes, NO re-sign needed if isolated. Recommend bundling with content edits to avoid two separate ceremonies.
2. `search_vocabulary.core_terms[NEW]` — add `farm-to-school`, `urban agriculture`, `controlled environment agriculture (CEA)` (§4.1).
3. `search_vocabulary.synonym_map[NEW]` — add `urban_agriculture` and `farm_to_school` mappings (§4.1).
4. `search_vocabulary.funder_program_keywords[NEW]` — add UAIPG, Patrick Leahy Farm to School Grant, FSA Direct Operating Loan, FSA Microloan (§4.1).
5. `search_vocabulary.disqualifier_terms[NEW]` — add "urban applicant for rural-only program," "ESOP-only applicant for cooperative-priority program" (§4.1).
6. `evidence_signals[NEW]` — add `climate_resilience_assessment` and `institutional_procurement_buyer_history` (§4.2).
7. `evidence_signals[REFINE]` — refine `food_safety_certification` source_pattern (§4.2).
8. `kfr_fact_classes[NEW]` — add `production_seasonality`, `food_safety_certification_chain` (§4.3).
9. `provenance_requirements[NEW]` — add `production_seasonality` (§4.3).
10. `provenance_requirements[REFINE]` — refine `buyer_relationships` (§4.3).
11. `admin_risk_term_register[REFINE]` — refine `regenerative agriculture` reviewer_context (§4.4).
12. `admin_risk_term_register[REFINE]` — refine `climate-smart agriculture` reviewer_context (§4.4).
13. `admin_risk_term_register[NEW]` — add `frontline community` (§4.4).
14. `narrative_sections_typical[NEW]` — add `"Project Partnership and Letters of Support"` (§4.5).
15. `common_risk_register_entries[REFINE]` — tighten `overclaiming regenerative impact` to HIGH × HIGH (§4.6).
16. `common_risk_register_entries[NEW]` — add `seasonal labor compliance gap`, `FSMA Produce Safety Rule exemption-loss risk` (§4.6).
17. `reporting_cadence_typical.per_funder_overrides[NEW]` — add USDA Farm-to-School / UAIPG / RFSP entries (§4.7).
18. `register_defaults.sub_register_selection_rule[REFINE]` — clarify post-cards-ceremony selection rule (§4.5). **Bundle with cards-ceremony per Run 1 Batch B (depends on §18 v1.2 + dialect_routing_table re-keyed shape).**

**OD-D Phase 4 forward-binding contract note (per master prompt rule 6 + §18.11 v1.1):**

- No proposal in this patch plan touches refusal (c) (compound enum values) — all admin_risk_term entries use canonical HIGH/MEDIUM/LOW + canonical FREQUENT/OCCASIONAL/RARE/UNKNOWN.
- No proposal touches refusal (d) (literal canonical CIC/CLC slug in non-exempt value position) — value-position-scan verified clean per §2.4.
- No proposal touches refusal (a) (structured-sub-field expansion on canonical entries) — additions are at canonical item-shape boundaries.
- No proposal touches refusal (b) (dedicated field-name fork) — no new top-level field names proposed.

Per Run 1 P1-1 / L1-F3 — the F-CARDS-COUPLING-VIOLATION-EXTENSION gate body is currently `NotImplementedError`. The value-position-scan that should catch refusal (d) regressions is not LIVE at runtime today. The compensating control is loader.py's enforce_no_forbidden_coupling (field-name layer only). This patch plan is value-position clean as verified by manual scan; recommend the gate-body graduation per Run 1 Patch C1 happen in parallel with or before the cards-ceremony to harden runtime defense.

### File: `pipeline/cards/_schema/card_cic.schema.json`

**Ceremony shape:** part of cards-ceremony compound LOCK per Run 1 Patch Queue Batch B (Patches B1 + B20).

**Edit set:**

19. Patch B20 — add `_research_metadata.draft_funder_candidates_pending_operator_engagement_confirmation` schema-known field (Run 1).
20. Patch B1 — apply §18 v1.2 dialect_routing_table re-key schema delta (Run 1).

### File: `pipeline/institutional_memory/admin_risk_register.yaml`

**Ceremony shape:** workspace-register update (OD-A v2.4 → v3.0 scrub workflow per master prompt §7).

**Edit set:**

21. Surface DEI / climate justice / decolonize / anti-capitalist as workspace-register migration candidates per OD-A v2.4 cross-CIC threshold (§4.4 + §5 item 1). **No card-body change from this card alone**; the migration is a workspace-register schema-extension decision.

### File: `pipeline/cards/CLC/operating_capacity.yaml` (cross-card; out of scope for this dispatch)

Per the proposal in §4.4 cross-CIC normalization for shared admin-risk terms: any migration affects the per-CLC register cells on CLC-side cards too. **Out of scope for `food_systems` handback. Surface to cards-ceremony / Phase 4-CLC for parallel dispatch.**

---

**Summary block:**

```
Card: CIC:food_systems
Card file: pipeline/cards/CIC/food_systems.yaml
Research hours actual: 1.4
Findings: 24 total — 0 P0, 11 P1, 13 P2
Decision queue: 11 operator approvals required
Conflicts with prior art: NONE (all admin_risk_term entries align with admin_risk_register v2.4 severity tiers; cross-CIC term-set is normalization-candidate, not conflict)
Coupling-discipline regression: NONE
Lifecycle gap surfaced: draft_status reads "signed" on disk (per Run 1 P0-3 — master prompt §5 stale claim retired; no normalization required)
Review readiness: READY (content improvements bundled to cards-ceremony per Run 1 Patch Queue Batch B; documentation-only header-comment patch bundle-able with the same ceremony to minimize ceremony count)
```
