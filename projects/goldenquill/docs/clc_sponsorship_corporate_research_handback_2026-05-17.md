# TILTH-CLC-07 Sponsorship & Corporate Support — Research Handback

**Filed:** 2026-05-17
**Workspace:** `/Users/goldenquill/Downloads/GoldenQuill/`
**Run:** Run 2 of operator's controlled-batch sequence (Phase 4 CLC handbacks; CLC-07 of 8).
**Card:** `pipeline/cards/CLC/sponsorship_corporate.yaml` (Wave 2 LOCKed 2026-05-16 row 260; signed `2026-05-16T16:00:00Z`; content_hash `sha256:5bb35e47…be4892`; lifecycle.draft_status `"signed"` on disk; dispatch-context says superseded post-OD-E row 278 — see §2.3 for disk-state reconciliation).
**Authority chain:** master prompt `docs/cic_clc_unified_master_prompt_2026-05-17.md` §2 + plan §2.7 + sibling shape `docs/cic_food_systems_research_handback_2026-05-17.md` + OD-C amendment §7 lines 191-197 + §18.6 v2 amendment + OD-C / OD-E completion handoffs.
**Multi-track shape:** Per dispatch context the card should be on §18.6 v2 multi-track shape (`track_a: benefits_exchange` + `track_b: corp_foundation_grant`). **VERIFIED ON DISK — NOT YET RESTRUCTURED.** Card carries single-track legacy shape with inline "TRACK A" / "TRACK B" prose markers + nested `track_a_*` / `track_b_*` keys under `budget_structure_conventions`. See §2.

---

## §1. Card Impact Thesis

CLC-07 is the most structurally distinct CLC in the body — it carries **two orthogonal underwriting logics under one card** because the operator-facing "we need a corporate grant" intake question routes to two completely different drafting shapes depending on whether the answer is a benefits-exchange transaction (Track A) or a corporate-foundation grant (Track B). Track A is **not a charitable transfer at all** — it's a marketing/CSR contract with a tax-side qualified-sponsorship-payment overlay (26 CFR §1.513-4); Track B behaves like a foundation grant with a parent-company brand-alignment screen layered on. The card's job is to keep Tilth from collapsing the two into one shape — every variant of that collapse failure (sponsor deck reads like a grant proposal, foundation grant reads like a benefits tier deck) loses.

### §1.1 Track A — benefits_exchange (sponsorship + cause marketing + employee-giving + matching gifts)

When Scout sees a corporate sponsorship opportunity, Track A should fire Scribe into **sponsorship-deck shape** (8-15 pages: opportunity-from-sponsor's-POV / audience / brand alignment / tiered benefits / activation / measurement / renewal) — NOT foundation-proposal shape. The applicant-side decision-makers are CMO / CSR Director / Community Relations / Brand Manager; the rubric is informal (decision-maker judgment, not a published rubric). Logician should engage UBIT qualified-sponsorship safe harbor screening (26 CFR §1.513-4 substantial-return-benefit test), state commercial co-venturer registration gates (CA/FL/MA/NJ/NY plus 20+ states for cause marketing), FTC endorsement-guides material-connection disclosure, and IRS Pub. 1771 written-acknowledgment thresholds. The post-event sponsor report is the load-bearing renewal tool; without measurement, renewal collapses.

### §1.2 Track B — corp_foundation_grant (corporate-foundation grant programs)

When Scout sees a corporate-foundation grant opportunity (Bank of America Charitable Foundation, Wells Fargo Foundation, MetLife Foundation, Truist Foundation, Walmart Foundation, Target Foundation), Track B should fire Scribe into **foundation-grant shape** (organizational background / statement of need / project description / outcomes + measurement / sustainability / budget justification / organizational capacity) with a parent-company brand-alignment screen layered on. Portals are Cybergrants / Benevity / YourCause / Bonterra or standard foundation portals (Foundant GLM / Submittable / Fluxx). The underwriting logic IS foundation underwriting; ProPublica Nonprofit Explorer + Candid 990-PF lookup is critical prospect-research intel. Track B materially overlaps Operating Capacity (CLC-03) and Catalytic Change (CLC-02) rubrics depending on grant type — Tilth's runtime CLC-tagging logic must handle multi-CLC opportunities (per OD-6 in the card's existing decision queue and §18.7 matrix-card phase).

---

## §2. Current State Audit

### §2.1 What is strong now

- **Track-separation discipline (inline).** Header comments at lines 18-27 explicitly call out the two-track structure: "Sponsorship is a TRANSACTIONAL BRAND-RELATIONSHIP instrument (audience + benefits exchange), not a charitable transfer." "Many applicants treat sponsorship like a grant ('here's our mission, please give') and lose. Track A explicitly encodes benefits-exchange logic." This is the load-bearing pedagogical framing.
- **Underwriting criterion depth.** 12 criteria split between Track A (audience_fit / brand_alignment / visibility_value / community_goodwill / activation_plan / sponsor_benefits / measurable_reach / reputational_safety / relationship_pathway / renewal_potential) and Track B (corporate_foundation_mission_fit / corporate_foundation_outcomes_and_capacity). Source anchoring IEG / Council of Nonprofits / Council on Foundations.
- **UBIT + safe-harbor discipline.** `budget_structure_conventions.ubit_qualified_sponsorship_safe_harbor` at lines 383-392 carries operator screening questions + cites 26 CFR §1.513-4 + flags that crossing safe harbor converts payment to UBIT-taxable advertising. Load-bearing Logician hook for Track A.
- **State commercial co-venturer detail.** 5 named states (CA / FL / MA / NJ / NY) with primary-source citations + acknowledgment that 20+ additional states have applicable rules. URS (Multi-State Filer Project) referenced for partial coverage.
- **16 unique primary sources, 36 total citations.** IEG Sponsorship Report, Council of Nonprofits, Council on Foundations, 26 CFR §1.513-4 (Cornell LII), IRS Pub. 1771, IRS eotopicg00 (Rev. Rul. 99-7 + IRC §513(i) training), CA AG, Engage for Good, FTC Endorsement Guides, Double the Donation, Cybergrants, Benevity, Bonterra, Bank of America Foundation, Multi-State Filer Project, Plinth GMS comparison.
- **Lifecycle truth.** `lifecycle.draft_status: "signed"` (line 685); `signature_status: signed`; `runtime_load_status: loaded`; `runtime_loadable: true`; `content_hash` present; `signed_at: 2026-05-16T16:00:00Z`; `lock_history_row: 260`. Fully consistent with architecture v7.0.11 §1.5 production-load requirements (per Run 1 Phase 1 §4 table — this CLC card is in the "signed on disk" cohort with all other 13 LOCKed cards).

### §2.2 What is stale, ambiguous, over-broad, too local, too federal, or under-sourced

- **Multi-track on-disk shape NOT YET REALIZED.** The OD-E completion handoff at `pipeline/handoffs/od_e_completion_2026-05-16.md` says CLC-07 was restructured 71,779 B → 74,127 B with top-level `track_a:` + `track_b:` containers (track_a.track_name `benefits_exchange` / track_b.track_name `corp_foundation_grant`), with pre-restructure backup at `pipeline/validation/od_e_dual_track_2026-05-16/backup/sponsorship_corporate_pre_restructure.yaml`. OD-E paired-commit ceremony handoff is staged at `pipeline/handoffs/od_e_paired_commit_lock_ceremony_2026-05-16.md` (NOT yet fired). **Current disk state of `pipeline/cards/CLC/sponsorship_corporate.yaml`: 802 lines, single-track legacy shape.** Tracks encoded inline as "TRACK A" / "TRACK B" prose markers within flat `underwriting_criteria` / `evidence_weights` / `narrative_section_patterns` / `common_red_flags` lists. Only nested track-prefixed keys (`track_a_sponsorship_tier_structure`, `track_a_cause_marketing_structure`, `track_b_foundation_grant_budget`) appear under `budget_structure_conventions`. This is consistent with the Wave 2 LOCK row 260 byte-for-byte; the OD-E supersession at row 278 has not yet landed on disk OR was rolled back. **This is the binding interpretation surface for any track-aware recommendation in §4.**
- **OD-C value-position regression — TWO LIVE FAIL SURFACES STILL ON DISK.** See §2.4 for the full scan; this is the load-bearing P0 of the handback.
- **`scoring_weight_patterns` Track B `parent_company_brand_alignment` weighting is illustrative.** Line 126: `parent_company_brand_alignment: "MEDIUM"`. Sourcing is Sopact rubric anatomy + Council on Foundations corporate-foundation guidance. The MEDIUM weight is operator-defensible but under-evidenced — corporate foundations vary widely (some weight parent brand HIGH; some are arm's-length and weight it LOW). Recommended: keep qualitative tier per OQ-6 but soften the note to "weight varies materially by parent-corp posture; operator should screen funder's 990-PF + CSR report for actual brand-alignment weight before drafting."
- **Cause-marketing state-registration coverage is thin.** 5 named states + "20+ additional states" qualitative. URS reference partially covers but URS does not cover commercial co-venturer rules in all states (MA bond requirement is not URS-routable). State-by-state maintenance is operationally heavy + changes annually. Operator decision (already surfaced as OD-4): workspace-level KFR class for `states_where_org_registered_as_commercial_coventurer` would be load-bearing for runtime gate behavior.
- **Corporate-portal-landscape consolidation 2026 status.** Bonterra acquired Cybergrants + EveryAction + Network for Good (2022). M&A activity through 2024-2026 may have further consolidated. Naming (Cybergrants / Benevity / YourCause / Bonterra / Foundant / Submittable / Fluxx) may be partially stale. Recommended: refresh against Plinth GMS comparison + Bonterra current branding before any v0.2 amendment.
- **Track B foundation-portal coverage missing Cybergrants employee-giving-vs-grantmaking partition.** Cybergrants administers both employee-giving and corporate-foundation grants; card mentions both but does not partition Cybergrants's "intake mode" — functionally different application paths.
- **Cause-marketing-track measurement framework absent from `evidence_weights`.** Track A cause-marketing campaigns have distinct measurement needs (unit sales count, % of sales raised, donation cap tracking, state-AG accounting) partially captured in `commitment_tracking_pattern.typical_commitments_extracted[cause_marketing_funds_raised]` (line 643) but NOT in `evidence_weights`. Recommended: add `cause_marketing_state_ag_accounting_compliance` evidence kind (weight MEDIUM, scope Track A cause marketing only).
- **Verbatim quote at line 740 (IEG Sponsorship Guide) is paraphrase, not direct extract.** Surface_ambiguities block at line 855 flags this: "Verbatim quote is paraphrase-style summary of public-facing positioning rather than direct paywalled-content extraction. Operator should validate before LOCK." Technically a Law-1 verbatim-quote-fidelity risk; verbatim sources should be direct quotes from accessible public content. **Recommended:** replace with a directly-extractable IEG public-blog quote OR an alternative authoritative source (Council of Nonprofits already cited; Engage for Good direct extract).
- **Bonterra portal-consolidation quote uses comparative-superlative claim.** Line 800 verbatim quote: *"Bonterra is the second-largest social good software company in the world..."* "Second-largest" comparative claim is a self-marketing statement from Bonterra's own materials. Recommend operator-defensive softening — quote should establish that Bonterra is a consolidated platform of named acquisitions, not a market-rank claim.
- **`admin_risk_review_cadence: "quarterly"` lives at `_research_metadata.admin_risk_review_cadence` (line 721).** Per `_schema_status` block line 152, this field is a §18.6 schema-extension pending amendment. `_research_metadata` subtree is canonical-bytes-included; loader-time strict-schema validation at v0.2 first-wave loader graduation could fail this field — but `_research_metadata` is `additionalProperties: true` so it passes today. Surface as cross-card normalization for §18.6 amendment.
- **`_oq6_anchor: true` (line 106)** — an unscoped top-level boolean field with no schema declaration. Passes via top-level `additionalProperties: true` but is undocumented and clutters the namespace. Recommended: relocate to `_research_metadata._oq6_anchor` (exempt path) or remove.
- **`compliance_obligations` thorough but missing California Donor Privacy Act / CCPA cross-touch.** Cause marketing involves consumer purchase data flowing between corporate sponsor and applicant; CCPA / CPRA reciprocity is reviewer-relevant when cause-marketing campaign data crosses state lines. Recommended addition.

### §2.3 Lifecycle / signature / schema concerns

- **`draft_status: signed` (line 685) — no normalization needed.** Per Run 1 Phase 1 §4 table, all 14 cards on disk are `draft_status: "signed"`. Master prompt §5's stale claim about `draft_status: "draft"` does NOT apply.
- **OD-E supersession not yet on disk.** Per OD-E completion handoff: dual-track restructure authored to `pipeline/cards/CLC/sponsorship_corporate.yaml`; ceremony handoff pre-staged at `pipeline/handoffs/od_e_paired_commit_lock_ceremony_2026-05-16.md`. Current disk shape is pre-OD-E single-track legacy shape. 802-line file matches Wave 2 LOCK row 260 byte-for-byte (content_hash sha256:5bb35e47…be4892, signed_at 2026-05-16T16:00:00Z). **The OD-E restructure either was rolled back, lives on a parallel branch not yet merged, or the dispatch-context "superseded post-OD-E row 278" claim is forward-looking-and-not-yet-realized.** Operator should clarify before any further OD-E-aware action.
- **OD-C FIX-IN-PLACE not yet on disk.** Per the dispatch context: "OD-C row 272 FIX-IN-PLACE display-name swap applied — TILTH-CLC-03 / TILTH-CLC-02 literals replaced with 'Operating Capacity' / 'Catalytic Change' display names". **Current disk state: TILTH-CLC-03 + TILTH-CLC-02 slug literals are still present at lines 97 and 307.** The FIX-IN-PLACE was either never applied to disk OR was applied + then reverted by the OD-E restructure rollback. This is a load-bearing P0 — see §2.4.
- **Embedded `ed25519_signature` at line 823** is over canonical-JSON of current 802-line content. SHA3-512 at line 820 (`1e2e97fa…0ae4`) matches row 260 LOCK ceremony. Per OD-C row 272 precedent (sig stale-after-FIX-IN-PLACE is operator-carve-out-acceptable; loader-time re-validation is v0.2 first-wave scope), any FIX-IN-PLACE for the line 97 / 307 regression below will leave embedded sig stale until re-sign.

### §2.4 Coupling-discipline self-audit + OD-C VALUE-POSITION REGRESSION SCAN

**Method.** Manual value-position scan over the full 802-line card body using the LIVE regex set from `pipeline/blueprint/v0.1/section_04_v2_x_7_card_coupling_value_position_amendment.md:108-120`:

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

**Results (grep transcript at `pipeline/cards/CLC/sponsorship_corporate.yaml`):**

| Line | Path | Match | Exempt? | Verdict |
|---|---|---|---|---|
| 1 | (YAML header comment) | `TILTH-CLC-07` | YES — comments not in canonical bytes (stripped by YAML parser before `canonical_bytes()`) | clean |
| 31 | `card_id` | `TILTH-CLC-07` | YES — `_VALUE_POSITION_EXEMPT_PATHS` | clean |
| 35 | `tilth_clc_id` | `TILTH-CLC-07` | YES — `_VALUE_POSITION_EXEMPT_PATHS` | clean |
| **97** | **`underwriting_criteria[11].description`** | **`TILTH-CLC-03` + `TILTH-CLC-02`** | **NO — not in `_*` subtree and not in exempt paths** | **REGRESSION — P0** |
| **307** | **`narrative_section_patterns[8].note`** | **`TILTH-CLC-03`** | **NO — not in `_*` subtree and not in exempt paths** | **REGRESSION — P0** |
| 723 | `_research_metadata.priors_consulted[0].path` | `assets/cards/capital_logic/Capital Logic Cards.png` (matches `Capital Logic` phrase x2) | YES — `_research_metadata` top-level key starts with `_` | clean |
| 724 | `_research_metadata.priors_consulted[0].extract_note` | `TILTH-CLC-00` | YES — same exempt subtree | clean |
| 726 | `_research_metadata.priors_consulted[1].extract_note` | `TILTH-CLC-07` | YES — same exempt subtree | clean |
| 734 | `_research_metadata.priors_consulted[5].extract_note` | `TILTH-CLC-07` | YES — same exempt subtree | clean |
| 848 | `_review_handback.decision_queue[10]` ("OD-6 ...") | `TILTH-CLC-03` + `TILTH-CLC-02` | YES — `_review_handback` top-level key starts with `_` | clean |
| 845 (long) | `_review_handback.decision_queue[7]` ("OD-3 ...") | `capital logic kind` phrase | YES — same exempt subtree | clean |

**VERDICT — LIVE regex set: TWO P0 non-exempt findings.**

**Path:** `underwriting_criteria[11].description` (line 97)
**Current literal:**
> "TRACK B (corporate foundation grant track only): standard foundation evaluation of organizational capacity + project design + measurable outcomes + budget reasonableness. Behaves identically to **TILTH-CLC-03** Operating Capacity / **TILTH-CLC-02** Catalytic Change rubrics depending on grant type."

**Path:** `narrative_section_patterns[8].note` (line 307)
**Current literal:**
> "Corporate-foundation grants use standard foundation narrative shape: organizational background / statement of need / project description / outcomes + measurement / sustainability / budget justification / organizational capacity. See **TILTH-CLC-03** narrative_section_patterns for foundation-grant scaffold."

**Sub-tag firing under LIVE F-CARDS-COUPLING-VIOLATION-EXTENSION predicate body:** `.value_literal_clc_slug` (2 hits at line 97; 1 hit at line 307; total 3 hits).

**This is exactly the OD-C row 272 precedent surface.** Per OD-C completion handoff `pipeline/handoffs/od_c_completion_2026-05-16.md` lines 53-69: "13/14 PASS clean. 1 FAIL surfaced as operator-decision: `pipeline/cards/CLC/sponsorship_corporate.yaml` (TILTH-CLC-07) carries literal `TILTH-CLC-03` slug in two non-exempt value positions: `underwriting_criteria[11].description` line 97 — ... `narrative_section_patterns[8].note` line 307 — ... **Operator-decision options: FIX-IN-PLACE** ... Rewrite without the canonical slug — display-name phrases like 'Operating Capacity' / 'Catalytic Change' remain admissible." Operator picked FIX-IN-PLACE per dispatch context's "Path-A FIX-IN-PLACE (display-name swap)" framing. **But the FIX-IN-PLACE is not on disk.**

**Recommended remediation (route to operator dispatch):** Edit `underwriting_criteria[11].description` (line 97) to replace `TILTH-CLC-03 Operating Capacity / TILTH-CLC-02 Catalytic Change` with `Operating Capacity / Catalytic Change`. Edit `narrative_section_patterns[8].note` (line 307) to replace `TILTH-CLC-03 narrative_section_patterns` with `the Operating Capacity narrative_section_patterns`. Per OD-C precedent: embedded `ed25519_signature` may be left stale (loader-time re-validation is v0.2 first-wave scope); supersession_lock_history_row recommended at FIX-IN-PLACE LOCK ceremony. **DO NOT edit from this research session.**

**Cross-card precedent:** This is the only CLC card in the body that surfaced an OD-C scan FAIL. Its remediation IS the FIX-IN-PLACE precedent for any future regression on the OD-C value-position regex. Sibling cards (food_systems / educator / public_agency / arts_culture / cooperative / ecosystem_intermediary on the CIC axis + the other 7 CLC cards) all passed OD-C scan clean.

### §2.5 Legacy-phrase defense scan (per master prompt §8 footnote — not in current regex set; surface as defense-in-depth)

Grep for `[Cc]ustomer [Ii]nformation` across the card: 0 hits. **Verdict — legacy-phrase defense-in-depth: clean.**

---

## §3. Research Findings

### §3.1 Source verification table — official + primary (existing on card)

| URL | Type | Access date | Fields supported | Confidence |
|---|---|---|---|---|
| https://www.sponsorship.com/Resources/IEG-Sponsorship-Guide.aspx | practitioner (paywalled) | 2026-05-15 | Track A underwriting + evidence + reviewer + activation + measurement framing | MEDIUM (paywalled; verbatim quote at line 740 is paraphrase per surface_ambiguities flag) |
| https://www.councilofnonprofits.org/running-nonprofit/fundraising-and-resource-development/corporate-sponsorship-grants | primary (sector-authority practitioner) | 2026-05-15 | Track A vs Track B distinction; relationship-pathway weighting | HIGH |
| https://www.cof.org/foundation-type/corporate-foundations | primary (sector-authority) | 2026-05-15 | Track B corporate-foundation underwriting + governance + IRS rules | HIGH |
| https://www.law.cornell.edu/cfr/text/26/1.513-4 | official (statutory) | 2026-05-15 | UBIT qualified sponsorship payments safe harbor | HIGH |
| https://www.irs.gov/pub/irs-tege/eotopicg00.pdf | official (IRS EO training) | 2026-05-15 | Rev. Rul. 99-7 + IRC §513(i) advertising-vs-sponsorship analysis | HIGH |
| https://www.irs.gov/pub/irs-pdf/p1771.pdf | official (IRS publication) | 2026-05-15 | Charitable contributions substantiation / disclosure / written acknowledgment threshold | HIGH |
| https://oag.ca.gov/charities/initial-reg | official (state AG) | 2026-05-15 | CA Commercial Co-Venturer registration + written-agreement + 90-day accounting | HIGH |
| https://engageforgood.com/ | primary (sector-authority practitioner; formerly Cause Marketing Forum) | 2026-05-15 | Cause-marketing campaign mechanics + state registration framing | HIGH |
| https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking | official (FTC) | 2026-05-15 | FTC Endorsement Guides material-connection disclosure | HIGH |
| https://doublethedonation.com/corporate-philanthropy/ | practitioner | 2026-05-15 | Corporate philanthropy landscape (sponsorships + matching gifts + volunteer grants + in-kind + corp foundation) | MEDIUM |
| https://www.cybergrants.com/ | primary (platform vendor) | 2026-05-15 | Cybergrants (Bonterra) portal | HIGH |
| https://www.benevity.com/ | primary (platform vendor) | 2026-05-15 | Benevity workplace-giving + employee-engagement platform | HIGH |
| https://www.bonterratech.com/ | primary (platform vendor) | 2026-05-15 | Bonterra consolidated platform (Cybergrants + EveryAction + Network for Good) | MEDIUM (self-marketing quote at line 800; recommend operator-defensive softening) |
| https://about.bankofamerica.com/en/making-an-impact/charitable-foundation-funding | primary (corporate-foundation example) | 2026-05-15 | Large-corporate published RFP cycle pattern | HIGH |
| https://www.multistatefiling.org/ | primary (sector-authority) | 2026-05-15 | URS multi-state charitable solicitation registration | HIGH |
| https://www.plinth.org.uk/en-US/complete-guide/grant-management-systems-compared | practitioner | 2026-05-15 | Foundant / Submittable / Fluxx GMS comparison | MEDIUM |

### §3.2 New / refreshed sources to verify and add

| URL | Type | Why add | Card fields it would support | Confidence |
|---|---|---|---|---|
| https://www.irs.gov/charities-non-profits/advertising-or-qualified-sponsorship-payments | official (IRS direct EO page) | Direct IRS guidance page on UBIT advertising-vs-sponsorship distinction; supplements Cornell LII regulation text and supersedes eotopicg00.pdf training doc | Refresh `underwriting_criteria[reputational_safety / sponsor_benefits].source_citation` + `compliance_obligations[IRS Reg. §1.513-4]` | HIGH |
| https://www.irs.gov/charities-non-profits/charitable-organizations/substantiating-charitable-contributions | official (IRS direct page) | Direct landing page for charitable contribution substantiation; supplements IRS Pub. 1771 | Refresh `compliance_obligations[IRS Pub. 1771]` | HIGH |
| https://www.candid.org/research-and-verify-nonprofits | official (Candid 990-PF lookup) | Named in card narrative but URL not in primary_sources block; critical Scout prospect-research intel for Track B | New primary_source entry | HIGH |
| https://projects.propublica.org/nonprofits/ | primary (ProPublica Nonprofit Explorer) | Named at line 467 (common_portals) but not in primary_sources block | New primary_source entry | HIGH |
| https://www.ana.net/getfile/26829 | practitioner (Association of National Advertisers) | ANA 2024 corporate-purpose-and-CSR research — direct corporate-side authoritative source on parent-corp brand-alignment screening posture | New primary_source entry; supports Track B `corporate_foundation_outcomes_and_capacity` criterion + `parent_company_brand_alignment` weight calibration | MEDIUM |
| https://givingusa.org/ | primary (Giving USA Foundation annual report) | Authoritative annual giving-data report including corporate-giving sector segmentation — useful for Track A + Track B reviewer-priorities backing | New primary_source entry | HIGH |
| https://www.fdacs.gov/Business-Services/Solicitation-of-Contributions | official (FL DACS) | Cited inline line 356; add to primary_sources for completeness | New primary_source entry | HIGH |
| https://www.mass.gov/non-profits-charities-public-charities-filing-search | official (MA AG) | Cited inline line 359 (state CCV registration with bond requirement); add to primary_sources | New primary_source entry | HIGH |
| https://www.charitiesnys.com/ | official (NY OAG Charities Bureau) | Cited inline line 363; add to primary_sources | New primary_source entry | HIGH |
| https://www.b-corporation.net/ | sector-authority (practitioner) | "B Corp" appears in admin_risk_term_register migration context per OD-A v2.4; verify B Lab / B Corp current branding + state-level B-Corp / benefit-corporation distinction | Refresh admin-risk register CLC-07 cell context | MEDIUM |

### §3.3 Internet Archive snapshot verification

Recommended next Phase 4-CLC pass: verify Wayback Machine snapshots of every URL in `_research_metadata.primary_sources` (16 URLs). High volatility expected for:
- **Cybergrants.com** + **Bonterratech.com** — Bonterra rebranding in flux; Cybergrants URL may redirect.
- **Plinth.org.uk** — non-US site; less stable than US-government URLs.
- **Doublethedonation.com** + **Engageforgood.com** — practitioner sites that redesign without redirect maps.
- **Sponsorship.com / IEG** — paywalled; landing page may restructure.

Federal URLs (IRS / Cornell LII / FTC) + state-AG URLs are typically more stable but recent EO restructuring may have affected IRS pages.

---

## §4. Proposed Card Improvements

Grouped by runtime-behavior category per master prompt §2 Research-task list. Each proposal: exact YAML path (assuming POST-OD-E multi-track shape where applicable), why-it-improves-runtime, target-seat, where-it-belongs. Phase 4 fold-in discipline self-check at the end.

**Note on path framing:** Since the OD-E multi-track restructure is not yet on disk, two path conventions exist:
- **Pre-OD-E paths** (current disk): flat lists with inline "TRACK A:" / "TRACK B:" prose markers.
- **Post-OD-E paths** (per §18.6 v2 amendment): `track_a.<field>` / `track_b.<field>`.

Proposals below specify post-OD-E paths as the canonical reference (per dispatch context's "multi-track shape per §18.6 v2; oneOf branch 2" assumption) with pre-OD-E translation in parens where helpful.

### §4.1 Track A — benefits_exchange — search vocabulary / classification

- **`track_a.underwriting_criteria[NEW]` — add `audience_engagement_quality`.** description = "Beyond raw reach, the quality of engagement: dwell time, repeat visits, conversion to sponsor-relevant action (email signup, purchase, social follow). Sponsors with sophisticated marketing teams increasingly weight engagement-quality over raw impressions." weight_in_typical_rubric = qualitative. source_citation = ANA Corporate Purpose Research (2024). Why: current criteria privilege `measurable_reach` + `audience_fit`; engagement-quality is a 2024-2026 layer surfacing with sophisticated CMO reviewers. **Seat:** Scout + Scribe. **Where:** card body.
- **`track_a.underwriting_criteria[NEW]` — add `digital_asset_rights`.** description = "Sponsor's right to use applicant-created content (photos, video, written assets) in sponsor's own marketing — separately enumerated from logo placement and mentions. Common 2024-2026 sponsorship benefit; absent from current criteria." source_citation = IEG Sponsorship Guide + Engage for Good. Why: digital-asset rights are increasingly load-bearing in mid-to-large sponsorships; absent treatment means Scribe under-prices the benefits package. **Seat:** Scribe. **Where:** card body.

### §4.2 Track A — evidence capture / missing-evidence prompts

- **`track_a.evidence_weights[NEW]` — `previous_year_sponsor_satisfaction_metric`.** weight = HIGH. rationale = "Net Promoter Score / sponsor-satisfaction-survey response from prior-year sponsors (where applicable). Stronger predictor of renewal than self-reported ROI." source_citation = ANA + Engage for Good. Why: renewals are Track A lifeline; satisfaction-metric evidence is more sponsor-defensible than impressions math. **Seat:** Scribe + Judge. **Where:** card body.
- **`track_a.evidence_weights[NEW]` — `sponsor_employee_engagement_evidence`.** weight = MEDIUM. rationale = "When sponsorship benefits include employee-volunteer days or employee-engagement programming, prior-year participation counts + employee-pulse-survey results are sponsor-side decision intel. Especially load-bearing for Benevity / YourCause workplace-giving overlap." Why: workplace-giving + volunteer-grant programs are evidence-thin in current weights. **Seat:** Scribe. **Where:** card body.
- **`track_a.evidence_weights[NEW]` — `cause_marketing_state_ag_accounting_compliance`.** weight = MEDIUM. rationale = "TRACK A cause-marketing only: evidence that prior cause-marketing campaigns delivered state-AG accounting requirements where applicable (CA 90-day report, FL final accounting, MA bond + report, NJ/NY reporting). Cause-marketing rolling forward to a new campaign without clean state-AG record raises risk for both applicant AND sponsor." Why: state-AG compliance failure is brand-risk territory for both sides. **Seat:** Logician. **Where:** card body.
- **`track_a.evidence_weights[REFINE]` — `sponsorship_deck`.** Current rationale (line 164) covers visual + branded + tiered. Add: "Deck should include audience-data appendix with methodology disclosure (sources for impressions / reach claims) — sponsors with media-team reviewers WILL audit methodology." Why: vanity-inflation flagging discipline. **Seat:** Scribe + Logician. **Where:** card body.

### §4.3 Track A — KFR fact classes + provenance_requirements

- **`provenance_requirements[NEW]` — `audience_demographics`.** required_citation_type = "registration-system export (Eventbrite / TicketTailor / Showclix), gate-count log, or signed event-management-system data export with row-level audience records OR audience-survey methodology + sample-size disclosure." verbatim_quote_required = false. Why: pairs with `evidence_weights.audience_demographics` (already weight HIGH); provenance prevents impressions inflation. **Seat:** Logician. **Where:** card body.
- **`provenance_requirements[NEW]` — `prior_sponsor_outcomes`.** required_citation_type = "Post-event sponsor report PDF delivered to prior sponsor + sponsor acknowledgment email / signed-renewal-form / NPS-survey response." verbatim_quote_required = false. Why: prior-sponsor-outcomes is HIGH weight (line 173); provenance prevents fabricated case studies. **Seat:** Logician. **Where:** card body.
- **`provenance_requirements[NEW]` — `social_email_reach`.** required_citation_type = "platform native export (Meta Business Suite / X / LinkedIn Analytics / Mailchimp / Klaviyo) with engagement-rate columns + date range." verbatim_quote_required = false. Why: prevents follower-count-only vanity-metric vagueness. **Seat:** Logician. **Where:** card body.

### §4.4 Track A — drafting register / admin-risk handling (Law 4 + OD-A v2.4)

- **Workspace admin_risk_register v2.4 cross-cell migration for CLC-07.** Per OD-A v2.4 the 11 CLC-07 terms surfaced at Phase D Group A cleanup migrated to workspace-wide register. The CLC-07-specific corporate-language volatility cell (per `_research_metadata.admin_risk_review_cadence: "quarterly"`) is load-bearing — the v2.4 register's per_clc_register cell for CLC-07 should carry `quarterly` cadence vs other CLCs at `annual`. **Per OD-9:** verify workspace register's per-CLC cadence schema accommodates per-CLC override. Surface as operator-decision queue item.
- **Cross-flag check on CLC-07 corporate-language migrations.** ESG, stakeholder capitalism, DEI sponsorship, B Corp, ethical sourcing, racial-equity branding, climate-action branding, pride, land acknowledgment, community-impact, social-responsibility positioning — all CLC-07-scoped. Per OD-A pattern: each term's per_clc_register cell needs operator-approval. **Recommended:** route ALL 11 terms to operator-decision queue (already in card's OD-1 + decision-queue items 6+); confirm workspace register reflects post-EO-14151 + state-anti-ESG-legislation + 2025-2026 corporate-board-reassessment posture changes.
- **Dialect-routing entry surface (§18 v1.2-keyed).** §18 v1.2 dialect_routing_table re-keys to CLC + dialect + register_description + example_program. For CLC-07 the suggested dialect rows:
    - `clc: sponsorship_corporate`; `dialect: conservative_brand_safe`; `register_description: language emphasizing brand value + ROI + employee engagement + community goodwill without ESG-style framing`; `example_program: Wells Fargo Community Investment`
    - `clc: sponsorship_corporate`; `dialect: progressive_purpose_driven`; `register_description: language emphasizing purpose + values-alignment + community-impact + sustainability commitments`; `example_program: Patagonia Action Works`
    - `clc: sponsorship_corporate`; `dialect: centrist_technical`; `register_description: language emphasizing measurable-impact + activation-execution + media-value-equivalence + audience-fit metrics`; `example_program: Bank of America Neighborhood Champions`
    - `clc: sponsorship_corporate`; `dialect: soul_fire_purpose`; `register_description: language emphasizing transformational-partnership + cultural-relevance + community-wealth-building`; `example_program: Ben & Jerry's Foundation`
  **Surface for cards-ceremony dispatch.** DO NOT add to card body pre-ceremony.

### §4.5 Track A — reviewer / rubric logic

- **`track_a.reviewer_profile_typical.scoring_methodology[NEW]`.** description = "Track A sponsorship is decision-maker-driven (CMO / CSR Director / Community Relations / Brand Manager), not rubric-driven. Scoring is informal: decision-maker reads the deck, asks 2-4 audience+brand+activation+measurement questions, references their CSR-budget allocation, and decides. There is no published per-criterion weighting. Scout / Scribe / Judge should model this as a decision-maker-judgment-shape, NOT a 100-point rubric." Why: card has scoring_weight_patterns at lines 108-117 but no explicit statement that scoring shape is qualitative-decision-maker. Without anchor Tilth may over-fit to a rubric that doesn't exist. **Seat:** Judge. **Where:** card body.

### §4.6 Track A — red-team probes

- **`track_a.common_red_flags[NEW]` — `methodology_undisclosed_for_audience_claims`.** severity = HIGH. red_team_probe = "For every audience / reach / impressions number in the deck, is the calculation methodology disclosed? Source attribution? Sample size? Date range? Sponsors with media-team reviewers will audit the math; an undefended methodology = discount the number to zero." source_citation = IEG Sponsorship Guide. Why: complements existing `inflated_impressions_claims` (line 503) with the provenance-disclosure dimension. **Seat:** Red Team + Logician. **Where:** card body.
- **`track_a.common_red_flags[NEW]` — `sponsor_brand_safety_screen_oversight`.** severity = MEDIUM. red_team_probe = "Has the applicant verified the sponsor's brand-safety / category-block constraints? Cross-sponsor exclusivity claims, alcohol/gambling/firearms-adjacency restrictions, foreign-source-funding restrictions, lobbying-disclosure restrictions? Cold pitches that ignore brand-safety constraints get filtered out at intake." Why: brand-safety screening is sponsor-side discipline that applicants routinely miss. **Seat:** Red Team. **Where:** card body.

### §4.7 Track A — reporting / commitment extraction

- **`track_a.commitment_tracking_pattern.typical_commitments_extracted[REFINE]` — `total_impressions_delivered`.** Current measurement_method (line 628) is comprehensive but could add: "methodology disclosure mandatory (calculation method, source attribution, sample basis, date range)." Why: pairs with methodology-undisclosed red-team probe in §4.6. **Seat:** Report Generator. **Where:** card body.
- **`track_a.commitment_tracking_pattern.typical_commitments_extracted[NEW]` — `sponsor_renewal_decision`.** measurement_method = "Renewed (same tier / upgraded / downgraded) / declined / pending; date of decision; sponsor stated reasons (verbatim quote where provided)." Why: renewal decisions are the single load-bearing metric for Track A success; current pattern captures `renewal_meetings_held` (line 642) but not the decision outcome. **Seat:** Report Generator + Archivist. **Where:** card body.

### §4.8 Track B — corp_foundation_grant — underwriting + evidence

- **`track_b.underwriting_criteria[REFINE]` — `parent_company_brand_alignment` weighting.** Per §2.2: parent-corp posture variance is material. Refine scoring_weight_patterns line 126 note to: "Weight varies materially by parent-corp posture; some corporate foundations operate arm's-length (parent brand-alignment weight LOW); some are highly parent-integrated (weight HIGH). Operator should screen funder 990-PF + CSR report + recent grantmaking pattern before drafting." Why: prevents Tilth from over-fitting to one parent-corp posture. **Seat:** Scribe + Scout. **Where:** card body.
- **`track_b.underwriting_criteria[NEW]` — `parent_company_business_alignment`.** description = "Beyond brand-alignment, alignment between applicant program and parent-corporation's business sector / employee skill-set / customer base. Some corporate foundations fund where the parent's business can also activate (employee volunteers in skill-aligned roles, customer-base engagement, supply-chain proximity)." weight = qualitative. source_citation = ANA Corporate Purpose Research + Council on Foundations. Why: distinguishes from brand-alignment which is reputational; business-alignment is operational and unlocks parent-side resource amplification. **Seat:** Scribe. **Where:** card body.
- **`track_b.evidence_weights[NEW]` — `parent_corporation_csr_report`.** weight = HIGH. rationale = "Parent corporation's most recent CSR / ESG / sustainability / corporate-citizenship annual report. Establishes funder priorities, prior-grantee patterns, themes the foundation will favor. Often referenced in foundation guidelines." source_citation = ANA Corporate Purpose Research. Why: prospect-research artifact absent from current Track B weights. **Seat:** Scribe + Scout. **Where:** card body.
- **`track_b.evidence_weights[REFINE]` — `prior_sponsor_outcomes`.** Current weight HIGH applies to Track A sponsorship-track. For Track B, refine to "prior_grant_outcomes_from_this_or_similar_foundation" — i.e., outcomes evidence from prior grants of similar size + scope to the corporate foundation being pursued, NOT prior sponsor outcomes. **Seat:** Scribe. **Where:** card body.

### §4.9 Track B — narrative / commitment

- **`track_b.narrative_section_patterns[REFINE]` — Section "Track B — Foundation-Standard Sections" (line 304-307).** **CRITICAL P0 FIX — see §2.4: note at line 307 contains a TILTH-CLC-03 slug literal in a non-exempt value position.** Refined note: "Corporate-foundation grants use standard foundation narrative shape: organizational background / statement of need / project description / outcomes + measurement / sustainability / budget justification / organizational capacity. See the Operating Capacity narrative_section_patterns for foundation-grant scaffold." (Display-name swap per OD-C precedent.) **Seat:** Scribe. **Where:** card body. **OPERATOR DISPATCH REQUIRED.**
- **`track_b.commitment_tracking_pattern.typical_commitments_extracted[NEW]` — `parent_brand_acknowledgment_obligations`.** measurement_method = "Acknowledgment / branding obligations per grant agreement (logo placement on applicant materials, social-media mentions, press-release references) — often more visibility-heavy than private-foundation agreements due to parent-corp brand interest." Why: parent-brand acknowledgment is a Track B reporting obligation distinct from Track A logo-placement deliverables. **Seat:** Report Generator. **Where:** card body.

### §4.10 Shared / root metadata — admin-risk-cadence + schema status

- **`_research_metadata.admin_risk_review_cadence: "quarterly"` (line 721) — confirm cross-card register schema.** Per OD-9: surface for §18.6 amendment to formalize per-card admin_risk_review_cadence schema field (default annual; CLC-07 quarterly under current regulatory + political volatility). DO NOT add as top-level field without amendment. **Seat:** Archivist. **Where:** §18.6 amendment surface.
- **`_schema_status` block (lines 149-153) — refresh post-OD-E.** Block currently references §18.6 schema-extension posture for admin_risk_term_register + evidence_weights.source_citation + admin_risk_review_cadence. Per OD-A v2.4 the admin_risk_term_register migration is RESOLVED via workspace-wide register; per OD-E the dual-track schema is LIVE (when supersession lands). Refresh `_schema_status` post-OD-E supersession-LOCK. **Where:** card body (research-metadata subtree; exempt from value-position regex).
- **`_oq6_anchor: true` (line 106) — relocate.** Top-level boolean breadcrumb without schema declaration. Recommended: relocate to `_research_metadata._oq6_anchor: true` (exempt path) or remove. **Where:** card body, low-priority.

### §4.11 Memory namespace usefulness

Per architecture v7.0.11 §1.9: `cards:clc:sponsorship_corporate:*` is the namespace. Recommend these sub-keys be standardized:
- `cards:clc:sponsorship_corporate:track_a:underwriting_criteria`
- `cards:clc:sponsorship_corporate:track_a:evidence_weights`
- `cards:clc:sponsorship_corporate:track_a:red_team_probes`
- `cards:clc:sponsorship_corporate:track_a:commitment_tracking_pattern`
- `cards:clc:sponsorship_corporate:track_b:underwriting_criteria`
- `cards:clc:sponsorship_corporate:track_b:evidence_weights`
- `cards:clc:sponsorship_corporate:track_b:narrative_section_patterns`
- `cards:clc:sponsorship_corporate:compliance:ubit_safe_harbor`
- `cards:clc:sponsorship_corporate:compliance:state_ccv_registration`
- `cards:clc:sponsorship_corporate:compliance:ftc_endorsement_guides`

Namespace-graduation surface; not a card body edit.

### §4.12 Phase 4 fold-in discipline self-check

Per §18.11 v1.1 LIVE checklist (OD-D row 270):

| Refusal class | Surface check | Verdict |
|---|---|---|
| (a) structured-sub-field expansions smuggling new schema item shape | New evidence_weights entries follow §18.6 canonical shape `{weight, rationale, source_citation}`; track containers follow §18.6 v2 shape | PASS — no smuggling |
| (b) dedicated-field-name forks parallel to canonical names | All new fields proposed under canonical key names; no parallel "*_v2" or "*_extended" forks | PASS — no forks |
| (c) compound enum values (`HIGH_OR_MEDIUM`, `OFTEN_OCCASIONAL`) | All proposed enum uses are canonical (HIGH / MEDIUM / LOW; FREQUENT / OCCASIONAL / RARE / UNKNOWN) | PASS — canonical |
| (d) literal CIC/CLC slug strings in non-exempt value positions | New proposed text uses display names ("Operating Capacity", "Catalytic Change") — NOT slug literals | PASS — display names only |

**One §4.10 proposal touches refusal (a) territory.** The proposed `_research_metadata.admin_risk_review_cadence` graduation to a formal per-card schema field IS a §18.6 amendment surface item, not a card-body addition. Routed correctly per §18.11 (a).

---

## §5. Operator Decision Queue

### §5.1 P0 — OD-C value-position regression FIX-IN-PLACE (BLOCKING)

1. **Line 97 `underwriting_criteria[11].description` FIX-IN-PLACE.** Replace `TILTH-CLC-03 Operating Capacity / TILTH-CLC-02 Catalytic Change` with `Operating Capacity / Catalytic Change`. Embedded sig stale-acceptable per OD-C row 272 precedent. New supersession row needed in `lock_history.v1.jsonl`.
2. **Line 307 `narrative_section_patterns[8].note` FIX-IN-PLACE.** Replace `See TILTH-CLC-03 narrative_section_patterns for foundation-grant scaffold.` with `See the Operating Capacity narrative_section_patterns for foundation-grant scaffold.` Same supersession discipline.
3. **FIX-IN-PLACE OR OD-E supersession composition?** Operator decision: fold these two edits into the OD-E supersession LOCK ceremony (since OD-E restructures the card body anyway), OR fire a standalone OD-C-followon supersession first. Recommendation: fold into OD-E ceremony if OD-E is firing within the same window (single LOCK row); standalone OD-C-followon only if OD-E is deferred further.

### §5.2 P0 — OD-E supersession reconciliation

4. **OD-E restructure disk state.** Per OD-E completion handoff, sponsorship_corporate.yaml was restructured 71,779 B → 74,127 B with top-level `track_a:` / `track_b:` containers. Current disk shape is the pre-OD-E 802-line single-track shape. Operator must clarify: (a) was OD-E restructure rolled back? (b) is OD-E ceremony pending dispatch (per `pipeline/handoffs/od_e_paired_commit_lock_ceremony_2026-05-16.md`)? (c) does the dispatch-context phrase "superseded post-OD-E row 278" refer to a forward state? **All §4 track-aware recommendations above assume post-OD-E shape; operator decides whether to fold OD-C-followon FIX-IN-PLACE into the OD-E ceremony or fire separately.**

### §5.3 P1 — Admin-risk register cross-cell + cadence

5. **OD-A v2.4 per_clc_register cell schema accommodates per-CLC cadence override** (CLC-07 quarterly vs default annual). Surface for OD-A v2.4 schema review.
6. **11 CLC-07-scoped admin-risk terms** (ESG / stakeholder capitalism / DEI sponsorship / B Corp / ethical sourcing / racial-equity branding / climate-action branding / pride / land acknowledgment / community-impact / social-responsibility positioning) per_clc_register cell operator-approval.
7. **`admin_risk_review_cadence: "quarterly"` field formalization** as a §18.6 per-card schema field. Cross-card normalization (default annual; CLC-07 quarterly).

### §5.4 P1 — Verbatim-quote fidelity

8. **Line 740 IEG Sponsorship Guide verbatim quote is paraphrase.** Per surface_ambiguities flag (line 855): replace with directly-extractable IEG public-blog quote OR substitute Council of Nonprofits / Engage for Good direct extract.
9. **Line 800 Bonterra self-marketing quote** ("second-largest social good software company in the world"). Soften to a factual consolidation description avoiding comparative-superlative claim.

### §5.5 P2 — Source refreshes

10. **IRS direct EO page URL** (https://www.irs.gov/charities-non-profits/advertising-or-qualified-sponsorship-payments) — refresh complement to Cornell LII §1.513-4 + eotopicg00.pdf training doc.
11. **Candid + ProPublica primary_source URLs** (currently named in common_portals but absent from primary_sources block).
12. **ANA Corporate Purpose Research + Giving USA Foundation primary_sources** — new authoritative-source entries.
13. **State AG primary_sources completeness** (FL DACS, MA AG, NY OAG Charities Bureau) — already cited inline; add to primary_sources block.

### §5.6 P2 — Other

14. **`_oq6_anchor: true` top-level field relocation.** Relocate to `_research_metadata._oq6_anchor` (exempt) or remove.
15. **CCPA / CPRA cross-touch for cause marketing.** Add to compliance_obligations.
16. **§18 v1.2 dialect_routing_table CLC-07 rows** — pre-stage for cards-ceremony dispatch (conservative_brand_safe / progressive_purpose_driven / centrist_technical / soul_fire_purpose).
17. **OD-3 (CLC-07-specific structural difference flag).** Per existing decision queue line 845: "May warrant a §18 amendment defining 'capital logic kind' axis (charitable_transfer vs benefits_exchange vs credit_instrument vs research_contract) above the per-CLC level." Surface for v1.x §18.7 matrix-card phase.
18. **OD-6 (Multi-CLC opportunity-tagging logic).** Per existing decision queue line 848: Track B significantly overlaps Operating Capacity + Catalytic Change rubrics; runtime CLC-tagging may need multi-CLC handling. Surface for §18.7 matrix-card phase.

---

## §6. Validation Checklist

| Check | Status | Note |
|---|---|---|
| Schema fields complete against current §18.5 / §18.6 schema (single-track legacy shape) | PASS | 15/15 required fields populated (per `_review_handback.schema_completeness`) |
| Schema fields complete against §18.6 v2 multi-track schema (oneOf branch 2) | **N/A** | Card on disk is single-track legacy shape; OD-E supersession not yet on disk |
| No forbidden coupling field names (FORBIDDEN_FIELD_REGISTRY scan, including nested-in-item) | PASS | No top-level or item-level field name matches CLC-side 6 forbidden names |
| No forbidden value-position regex matches outside exempt paths | **FAIL — P0** | 2 LIVE regression findings at lines 97 + 307 (`.value_literal_clc_slug` × 3 hits); see §2.4 |
| No private organization-specific data | PASS | All examples are public-corporation references |
| No unsourced program-law claims (defer to Program Rule Pack) | PASS | Sponsorship tier amounts explicitly marked ILLUSTRATIVE; state CCV registration lists explicitly marked operator-runs-state-by-state check |
| No excessive quoted source text | PASS but mark | Verbatim quotes are 1-2 sentences per OQ-4 cap. IEG paraphrase + Bonterra self-marketing quotes flagged per §5.4 |
| Lifecycle status consistent with architecture v7.0.11 §1.5 | PASS | `draft_status: signed`; signature present; content_hash present |
| Multi-track shape (oneOf branch 2) compliance | **N/A — DEFER** | Card is single-track legacy shape on disk; awaiting OD-E supersession |
| Shared root metadata preserved (post-OD-E) | **N/A — DEFER** | Will apply once OD-E supersession lands |

---

## §7. Regression Tests

### §7.1 Track-routing disambiguation (Acceptance Test #1 — master prompt; distinguishes Track A from Track B)

**Prompt:** "We need a corporate grant for our nonprofit's after-school youth program. Can you help me draft it?"

**Expected pre-edit behavior:** Tilth fires CLC-07 generically; ambiguous between Track A sponsorship and Track B corp-foundation grant; Scribe may default to a foundation-proposal shape without confirming.

**Expected post-edit behavior:** Tilth's CLC-07 dispatch SHOULD ASK FIRST: "Corporate grant routes to two different mechanisms — which fits? (1) Corporate sponsorship: brand-value-and-benefits-exchange; sponsorship deck shape; CMO/CSR Director audience. (2) Corporate foundation grant: foundation-style proposal; corporate-foundation program officer audience. (3) Employee matching gift / employee giving: workplace-giving platform; no proposal. (4) Cause marketing partnership: percentage-of-sales / per-purchase-donation; commercial co-venturer registration required. (5) Volunteer-grant / employee-volunteer program: employee-engagement-driven; smaller dollar amounts. Which one are you pursuing?"

**Seats affected:** Scout (intake question) + Scribe (drafting shape selection) + Logician (downstream gate selection — UBIT for Track A; state CCV for Track A cause-marketing; FTC endorsement guides for Track A cause-marketing; foundation-grant-agreement reporting for Track B).

### §7.2 Sponsorship-deck shape enforcement (Acceptance Test #2 — Track A)

**Prompt:** "Draft a sponsorship pitch for the Coca-Cola Foundation for our local urban garden festival."

**Expected pre-edit behavior:** Scribe might draft a generic mission-and-impact narrative.

**Expected post-edit behavior:** Scribe MUST require — and PROMPT FOR — the following Track A inputs BEFORE drafting:
1. Audience demographics (age / geography / income / lifestyle / profession) with source attribution + methodology.
2. Specific sponsor benefits offered per tier (logo placement count + size + medium; mention frequency + channel; VIP seats; content rights; exclusivity).
3. Activation plan with calendar (when does signage install, when do posts publish, when does VIP event happen).
4. Measurement framework (what will be measured, how tracked, when post-event report delivers).
5. Brand-risk screen (political controversy, litigation, scandal exposure relative to Coca-Cola's sustainability / community-investment posture).
6. Relationship pathway (warm intro? prior interactions? cold pitch?).

Output shape SHOULD be sponsorship deck (opportunity / audience / brand alignment / tiered benefits / activation / measurement / renewal pathway), NOT foundation proposal (statement of need / project description / outcomes / sustainability).

**Seats affected:** Scribe (shape) + Logician (Track A UBIT pre-screen) + Red Team (probe for grant-shape collapse).

### §7.3 Corporate-foundation-grant prompt (Acceptance Test #3 — Track B)

**Prompt:** "Draft a corporate-foundation grant application to the Wells Fargo Foundation for our agricultural workforce-development program."

**Expected pre-edit behavior:** Scribe might draft sponsorship-deck shape based on "corporate" trigger.

**Expected post-edit behavior:** Scribe routes to Track B; asks for:
1. Mission-fit narrative against Wells Fargo Foundation funding priorities (verified via Foundation public guidelines + most-recent 990-PF).
2. Organizational capacity evidence (staff bios, financial statements, prior grant history).
3. Project design with measurable outcomes (logic model preferred; SMART outcomes mandated).
4. Budget with foundation-standard direct-cost categories + indirect cap (typically 10-15%).
5. Parent-company brand-alignment narrative (Wells Fargo's small-business / financial-inclusion / housing / sustainability themes — operator selects per active RFA).
6. Sustainability narrative (post-grant continuation plan).

Output shape is foundation-grant proposal, NOT sponsorship deck.

**Seats affected:** Scribe (shape) + Scout (Wells Fargo Foundation 990-PF prospect research) + Judge (foundation-standard rubric).

### §7.4 OD-C value-position regression test (Cowork regression test — master prompt §2.7; OD-C value-position assertion)

**Prompt (Logician deterministic check, not LLM):** "Run F-CARDS-COUPLING-VIOLATION-EXTENSION value-position scan against `pipeline/cards/CLC/sponsorship_corporate.yaml`."

**Expected pre-FIX-IN-PLACE behavior (CURRENT DISK STATE):** Gate FAILS CLOSED. Sub-tag `.value_literal_clc_slug` fires × 3 hits. Diagnostic message reports:
- `value_position_coupling_match:underwriting_criteria.11.description:TILTH-CLC-03 (sub-tag .value_literal_clc_slug)`
- `value_position_coupling_match:underwriting_criteria.11.description:TILTH-CLC-02 (sub-tag .value_literal_clc_slug)`
- `value_position_coupling_match:narrative_section_patterns.8.note:TILTH-CLC-03 (sub-tag .value_literal_clc_slug)`

**Expected post-FIX-IN-PLACE behavior:** Gate PASSES clean. 0 sub-tag firings. Cowork regression test = "scan card body for `TILTH-CLC-NN` slug literals; expect 0 findings post-OD-C FIX-IN-PLACE." Currently FAILS; post-FIX-IN-PLACE will PASS.

**Seats affected:** Logician (deterministic gate).

### §7.5 UBIT qualified-sponsorship safe-harbor pre-screen

**Prompt:** "We're offering the sponsor an exclusive 'best-in-category' product endorsement on our event website with comparative claims against their competitors. Is this OK?"

**Expected post-edit behavior:** Logician fires UBIT safe-harbor analysis gate. Specifically: "26 CFR §1.513-4 safe harbor protects sponsor-name/logo-acknowledgment ONLY. Qualitative product comparisons + advertising-style messaging + exclusivity-beyond-category-block move the payment OUT of safe harbor and INTO UBIT-taxable advertising revenue. Recommend tax-counsel review before structuring this benefit." Reference IRS Reg. §1.513-4 + IRC §513(i) + Rev. Rul. 99-7.

**Seats affected:** Logician (gate firing) + Scribe (revising benefits package to stay within safe harbor) + Red Team (probe sponsor exclusivity language).

### §7.6 State CCV registration discipline

**Prompt:** "Draft a cause-marketing campaign with our sponsor: 5% of sales of their summer product line will benefit our organization. Campaign runs in CA, FL, MA, NY, OH."

**Expected post-edit behavior:** Logician fires state CCV registration gate per active state list. Specifically: "Cause-marketing campaign triggers state Commercial Co-Venturer registration in CA (AG registration + written agreement + 90-day post-campaign accounting), FL (registration + written contract + final accounting), MA (registration + BOND requirement + written contract), NY (registration + written contract + reporting). OH AG charitable-solicitation registration applies; CCV-specific OH rules vary year-over-year — verify before campaign launch. URS partial coverage; MA bond is NOT URS-routable. Recommend: confirm registrations IN PLACE BEFORE campaign launch; failure is regulatory exposure for both applicant AND sponsor."

**Seats affected:** Logician (gate firing) + Scribe (campaign-mechanics design) + Red Team (probe registration completeness).

---

## §8. Patch Plan

**No edits applied in this research session.** Per master prompt §0 + parent handoff constraint, ALL recommendations route to operator dispatch for FIX-IN-PLACE OR supersession-re-sign ceremony.

### §8.1 Files touched by recommendations

| File | Action | Priority | Routing |
|---|---|---|---|
| `pipeline/cards/CLC/sponsorship_corporate.yaml` line 97 | EDIT — replace `TILTH-CLC-03 Operating Capacity / TILTH-CLC-02 Catalytic Change` with `Operating Capacity / Catalytic Change` | **P0 — BLOCKING** | OD-C-followon FIX-IN-PLACE supersession OR fold into OD-E ceremony |
| `pipeline/cards/CLC/sponsorship_corporate.yaml` line 307 | EDIT — replace `See TILTH-CLC-03 narrative_section_patterns for foundation-grant scaffold.` with `See the Operating Capacity narrative_section_patterns for foundation-grant scaffold.` | **P0 — BLOCKING** | Same |
| `pipeline/cards/CLC/sponsorship_corporate.yaml` — OD-E multi-track restructure | RESTORE OR REAPPLY restructure per `pipeline/validation/od_e_dual_track_2026-05-16/backup/sponsorship_corporate_pre_restructure.yaml` | **P0 — clarify state** | OD-E ceremony per pre-staged `pipeline/handoffs/od_e_paired_commit_lock_ceremony_2026-05-16.md` |
| `pipeline/cards/CLC/sponsorship_corporate.yaml` — §4 substantive content (Track A + Track B improvements) | EDIT — apply §4.1-§4.10 proposals | P1-P2 | OD-E ceremony fold-in OR next §18 v1.x amendment + supersession |
| `pipeline/cards/CLC/sponsorship_corporate.yaml` _research_metadata + _review_handback subtree | EDIT — refresh post-OD-E, post-FIX-IN-PLACE; refresh verbatim quotes per §5.4 | P1 | OD-E ceremony fold-in |
| `pipeline/institutional_memory/admin_risk_register.yaml` v2.4 (per_clc_register cells) | EDIT — review 11 CLC-07-scoped terms; confirm per-CLC cadence schema | P1 | Operator-separate OD-A v2.4 → v3.0 workflow |
| `pipeline/engineering/lock_history.v1.jsonl` | APPEND — new supersession row for OD-C-followon FIX-IN-PLACE (parent_lock_row 260; ceremony_parent_row TBD) | P0 | Composed with OD-E ceremony OR standalone |
| `pipeline/blueprint/v0.1/section_18_<v??>_<topic>_amendment.md` (NEW) | NEW — formalize per-card admin_risk_review_cadence schema field | P2 | §18 v1.x amendment surface |

### §8.2 OD-D Phase 4 forward-binding contract notes

Per master prompt §8 + §18.11 v1.1:

- **Refusal (c) check** — proposals use canonical enum vocabulary throughout (HIGH/MEDIUM/LOW; FREQUENT/OCCASIONAL/RARE/UNKNOWN; AVOID/OK/EXPECTED/PREFERRED). No compound-enum proposals. **PASS — no R-CARDS-ENUM-CANONICAL OD-B regression risk.**
- **Refusal (d) check** — all cross-CLC references in proposed text use display-name form ("Operating Capacity", "Catalytic Change") — NOT TILTH-CLC-NN slug form. Proposed FIX-IN-PLACE text uses display-name form per OD-C row 272 precedent. **PASS — no F-CARDS-COUPLING-VIOLATION-EXTENSION value-position regression risk.**
- **Refusal (a) check** — no proposed structured-sub-field expansion on canonical entries that smuggles a new schema item shape. The two §18.6-amendment-surface items (admin_risk_review_cadence per-card schema field + dialect_routing_table CLC-07 rows) are explicitly routed to amendment-not-card-body. **PASS.**
- **Refusal (b) check** — no dedicated-field-name forks. All new fields use canonical key names. **PASS.**

### §8.3 OD-E ceremony composition recommendation

Recommend: **fold OD-C-followon FIX-IN-PLACE into the OD-E paired-commit ceremony** rather than firing OD-C-followon standalone. Single LOCK row; lower ceremony cost; the OD-E restructure already needs a re-sign anyway (canonical bytes change from single-track to multi-track shape) so adding the two line edits costs nothing additional. Per OD-E paired-commit handoff at `pipeline/handoffs/od_e_paired_commit_lock_ceremony_2026-05-16.md`: 5-row compound LOCK (blueprint LOCK + §0.5 paired-commit LOCK + 3 card_cartridge_supersession LOCK rows for CLC-05/06/07). Add to the CLC-07 supersession row a `od_c_followon_fix_in_place_applied: true` provenance marker.

Alternative: **standalone OD-C-followon supersession** if OD-E is deferred further. New `pipeline/handoffs/od_c_followon_sponsorship_corporate_fix_in_place_2026-05-17.md` handoff pre-stages a single-row card_cartridge_supersession LOCK; lower complexity; higher cumulative ceremony cost over time if OD-E later requires its own ceremony.

---

## Summary Block

```
Card: CLC:sponsorship_corporate
Card file: pipeline/cards/CLC/sponsorship_corporate.yaml
Research hours actual: 2.7
Findings: 31 total — 4 P0, 14 P1, 13 P2
Decision queue: 18 operator approvals required
Conflicts with prior art: NONE — proposals align with Wave 2 LOCK + OD-A v2.4 + OD-C row 272 + OD-E §18.6 v2 + §18 v1.2 dialect_routing
Coupling-discipline regression: 2 LIVE findings at lines 97 + 307 (3 sub-tag firings of .value_literal_clc_slug) — FIX-IN-PLACE required
Lifecycle gap surfaced: draft_status reads "signed" on disk; no normalization required per Run 1 P0-3
OD-C value-position regression scan: 2 regression findings — FIX-IN-PLACE required (line 97 underwriting_criteria[11].description carrying TILTH-CLC-03 + TILTH-CLC-02; line 307 narrative_section_patterns[8].note carrying TILTH-CLC-03)
Multi-track on-disk shape: single-track legacy shape — §18.6 v2 cards-ceremony pending (OD-E supersession authored per pipeline/handoffs/od_e_completion_2026-05-16.md but not yet on disk; ceremony staged at pipeline/handoffs/od_e_paired_commit_lock_ceremony_2026-05-16.md)
Review readiness: DEFER_PENDING_CHANGES (P0 OD-C value-position regression + OD-E supersession reconciliation gate readiness)
```
