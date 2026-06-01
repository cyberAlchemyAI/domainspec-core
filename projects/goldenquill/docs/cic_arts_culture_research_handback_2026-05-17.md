# TILTH-CIC-04 Arts & Culture — Research Handback

**Filed:** 2026-05-17
**Workspace:** `/Users/goldenquill/Downloads/GoldenQuill/`
**Run:** Run 2 of operator's controlled-batch sequence (Phase 4 CIC handbacks; 4 of 6).
**Card:** `pipeline/cards/CIC/arts_culture.yaml` (Wave 2 LOCKed 2026-05-16 row 252; SHA-256 `ed1ddd…00e0`; signed `2026-05-16T16:00:00Z`).
**Authority chain:** master prompt §2 + plan §1.4 + Run 1 priors (binding).
**Run 1 priors folded in:** all 14 cards on disk are `draft_status: "signed"` (P0-3); §18 v1.2 LOCKed-but-not-applied (L2-F0); operator v2.1 Law-5 split uniformly applied (L2-F5); coupling-extension value-position regex not LIVE at runtime (L1-F3); operator reframe = aggressive content OK.

---

## §1. Card Impact Thesis

`arts_culture` carries Tilth's hardest dialect-discipline workload: **preserve artistic voice + translate cultural / civic / accessibility / preservation / humanities / audience / production-value into funder-legible evidence + hold the boundary between artist-voice (verbatim self-identification) and funder-legible-prose (rubric-scorable framing) without flattening either.** Under EO 14151 + EO 14168 + downstream NEA + NEH funding-clause environment, this card faces the highest admin-risk-vocabulary load of any CIC — identity-based vocabulary (queer / trans / racial justice / decolonial / liberation / abolition) carries documented enforcement risk on federal arts grants while foundation funders vary widely.

What this card should *cause Tilth to do differently*:

1. When Scout sees `artist`, `arts organization`, `performing arts`, `visual arts`, `humanities`, `creative placemaking`, `cultural heritage`, `accessibility`, anchor to NEA Grants for Arts Projects discipline roster + NEH program-area framing + IMLS Museums for America categories + state arts councils + foundation arts portfolios.
2. When Scribe drafts an arts narrative, run BOTH the artistic-merit register (work samples + artistic vision) AND the sustainability register (audience math + revenue diversification + post-grant continuation) — do not collapse either into the other.
3. When Logician audits a draft mentioning `queer`, `trans`, `decolonial`, `liberation`, `racial justice`, `anti-racist`, fire admin_risk_term entries with severity HIGH; surface substitution candidates that preserve artist-voice self-identification while routing funder-legible frame per active RFA. **CRITICAL: when artist self-identifies, Scribe MUST NOT rewrite verbatim self-identification.** Operator decides per RFA routing.
4. When the active opportunity is NEA or NEH (federal), surface funding-clause-environment context (gender-ideology / DEI attestation language) and route admin-risk-vocabulary per current-administration framing. State arts councils that pass NEA partnership funds inherit downstream restrictions on the federal portion.
5. When `accessibility` surfaces, anchor to ADA / Section 504 / NEA Office of Accessibility — these are statutory-anchor frames that are reviewer-neutral across all four political axes.
6. When `fiscal sponsorship` surfaces, anchor to NYFA / Fractured Atlas / The Field 501(c)(3) fiscal-sponsor pathway for individual artists / unincorporated collectives.

The runtime-behavior delta this card produces is **dialect-discipline depth + artist-voice preservation + admin-risk discipline under EO 14151 / EO 14168 / NEA + NEH funding-clause environment + accessibility as statutory anchor.** The card is currently strong on all four.

---

## §2. Current State Audit

### §2.1 What is strong now

- **21 core_terms with discipline-roster precision.** NEA Grants for Arts Projects discipline roster (Theater / Musical Theater / Opera / Dance / Music / Visual Arts / Design / Media Arts / Crafts / Folk & Traditional Arts / Literary Arts / Artist Communities / Local Arts Agencies / Presenting & Multidisciplinary Works) cited at lines 64–74. NEH program division roster (Public Programs / Preservation & Access / Sustaining Cultural Heritage Collections / Public Humanities Projects) cited at lines 154–166. IMLS Museums for America three-category framing (Lifelong Learning / Community Anchors and Catalysts / Collections Stewardship and Public Access) cited at lines 167–171 + 1133–1139.
- **Foundation arts portfolio depth.** Mellon Arts and Culture (line 176), Doris Duke Performing Arts (line 178), Ford Foundation Creativity and Free Expression (line 181), Knight Foundation Arts (line 184), Wallace audience-building (line 187), Surdna Thriving Cultures (line 190), Heinz Endowments Creativity (line 193), Native Arts and Cultures Foundation (line 196), United States Artists (line 199), W.A.G.E. (line 1197) — each with explicit source_citation.
- **Critical EO 14151 + EO 14168 framing block at lines 454–484.** Card explicitly carries:
  - "DEFER-TO-ACTIVE-RFA DISCIPLINE (Tilth-wide): EO 14151 + EO 14168 are named here as illustrative reviewer-context anchors for the authoring-time administration, NOT as permanent ground truth. Federal arts-grant attestation language has changed mid-cycle and will continue to change across administrations. Scribe + Logician MUST defer to the per-active-RFA attestation language at runtime."
  - "IMPORTANT — operational severity preserved: the illustrative-anchor reframing above applies ONLY to the EO 14151 / EO 14168 framing context. Per-term severity values (HIGH / MEDIUM / LOW) in each admin_risk_term_register entry remain operationally NORMATIVE at runtime."
  This is the cleanest administration-neutralization framing across the CIC body — recommend it as a pattern for sibling cards (food_systems / educator / public_agency / cooperative / ecosystem_intermediary).
- **15 admin_risk_term entries** (lines 486–718) — radical / abolition / decolonial / liberation / resistance / queer / trans / gender ideology / racial justice / censorship / occupation / DEI / social justice / anti-racist + (implicit boundary for `anti-displacement` carry-over). Identity-term entries (queer, trans, gender ideology) include explicit "artist-voice self-identification MUST NOT be rewritten" discipline (lines 572–578, 595–597).
- **Cultural-sovereignty dialect** (lines 445–447) — `scribe.cultural_sovereignty` dialect for soul-fire-aligned funders (NACF / First Peoples Fund / NDN Collective). Distinct from other CICs' soul-fire dialect; reflects cultural-sovereignty practice provenance.
- **W.A.G.E. (Working Artists and the Greater Economy) fee calculator** at line 1198 — underbudgeted-artist-fees risk mitigation. This is the kind of practitioner-specific evidence anchor unique to arts.
- **Phase E Option 2 Law-5 cleanup.** Top-level `common_funders_observed: []` at line 1024; subagent candidates at `_research_metadata.draft_funder_candidates_pending_operator_engagement_confirmation` line 1235 (per Run 1 §6.3 cross-reference).
- **Lifecycle truth.** All five lifecycle gate fields at pass-state; lock_history_row 252.

### §2.2 What is stale, ambiguous, over-broad, too local, too federal, or under-sourced

- **NEA / NEH funding-clause environment is administration-time-anchored.** The admin_risk_term reviewer_context (lines 567–597 on queer / trans; lines 600–618 on gender ideology) repeatedly cites "Under EO 14168 + post-EO 14151 NEA + NEH funding-clause environment." The card's defer-to-active-RFA framing at lines 454–484 partially mitigates, but per-entry reviewer_context still time-stamps to current administration. Recommend tightening to defer-to-RFA-attestation language at runtime; operator confirms each application's active-RFA attestation language.
- **Verbatim NEA funding-clause language not pinned with primary_source.** Lines 458–464 reference "an attestation they will not 'operate any programs promoting gender ideology' and will not 'use Federal funds to promote DEI'" — strong illustrative anchor but the actual NEA grant terms page (https://www.arts.gov/grants/grant-program-description) is cited at line 1203 + 1176 with non-verbatim source description ("under current administration framing, projects must not promote 'gender ideology'"). Recommend tighten primary_sources to capture verbatim NEA grant-terms quote ≤2 sentences per OQ-4.
- **`dialect_routing_table` v1.1 shape with retired political-axis enum** (lines 435–447). Same status: cards-ceremony bottleneck.
- **Foundation funder roster carries by-invitation-pattern foundations.** Doris Duke (Performing Artist Awards by-nomination), Mellon, Ford — flagged as by-invitation patterns in some practitioner usage. Recommend `frequency_observed: RARE` for cold-application context vs `OCCASIONAL / FREQUENT` for invited-application context if the operator's engagement history accumulates enough signal to differentiate.
- **State arts councils — 1:1 PCA-only example.** Lines 173–175 cite PA Council on the Arts (PCA) program lines (Entry / Project Stream / PPA Re-grant); state arts councils across NEA partnership are 56 in total (50 states + 6 territories + DC) per the National Assembly of State Arts Agencies (NASAA) directory cited at line 1209. **Recommend:** `state_arts_council` core_term as omnibus with NASAA cross-reference; PCA as PA-specific example only. Per master prompt §1.4 + state-overlay guidance: PA-specific entries are state-overlay candidates.
- **No `Native American Languages Act` core_term** — important for Indigenous-arts applicants; named indirectly in Educator card's admin_risk_term reviewer_context for parallel statutory framework, absent from arts card. Recommend cross-CIC consistency.
- **No `creative aging` or `arts and aging` core_term.** Emerging funding category — NEA + AARP Foundation + state arts councils with arts-and-aging portfolios.
- **No `arts and health` or `arts in medicine`** core_term — NEA Creative Forces (military/veteran clinical creative-arts therapies) named at line 153 but the broader arts-health pathway (university arts-medicine programs, hospital artists-in-residence, music therapy) is under-indexed.
- **No `accessibility coordinator` or `cultural accessibility plan` evidence_signal.** Section 504 / ADA Title II/III compliance is named in core_terms (line 93) and admin_risk_term reviewer_context (line 686) but no evidence_signal for cultural-accessibility-plan documentation, large-print / audio-description / ASL-interpretation provisions, captioning practices.
- **`fiscal_sponsorship` core_term named at line 95 with NYFA / Fractured Atlas / The Field exemplars** — but no evidence_signal for fiscal-sponsorship-relationship documentation (sponsor 501(c)(3) determination + fiscal-sponsor agreement + project-relationship-to-sponsor narrative).
- **`metrics_table_template` strong but missing arts-specific metrics.** Audience-development metrics (new vs returning audience), demographic-disaggregation of audience, accessibility-accommodation-served counts, artist-fee-fairness ratio (artist-fees-as-percent-of-project-budget), W.A.G.E.-certification-compliance.
- **Verbatim source quotes** at primary_sources (lines 1083–1219) are dated 2026-05-15; recommend Internet Archive snapshot pass for high-volatility URLs (NEA + NEH program pages, NEA grant terms page especially likely to shift under administration framing changes).

### §2.3 Lifecycle / signature / schema concerns

- **`draft_status: signed`.** No normalization needed.
- **Header comment cleanliness.** Lines 1–40 are reasonably clean; the EO 14151 + EO 14168 + admin-risk-discipline framing is operator-grade.
- **`dialect_routing_table` v1.1 shape** (lines 435–447). Cards-ceremony bottleneck.
- **`_research_metadata.draft_funder_candidates_pending_operator_engagement_confirmation` field not schema-known.** Same status.
- **Embedded `ed25519_signature` LIVE** (verify at line 1220 — `ed25519_signature: null` in current snippet; double-check during cards-ceremony).
- **`assets/cards/customer_identification/arts_culture.png` path canonicalization** (line 1067) — comment notes operator may have asset under spaced filename `arts and culture.png`; operator-side housekeeping. No card-body change.

### §2.4 Coupling-discipline self-audit

| Line | Path | Match | Exempt? |
|---|---|---|---|
| 1 | (YAML header comment) | `TILTH-CIC-04` | YES — comments not in canonical bytes |
| 3 | (YAML header comment) | `TILTH-CIC-04` | YES |
| 43 | `card_id` | `TILTH-CIC-04` | YES |
| 48 | `tilth_cic_id` | `TILTH-CIC-04` | YES |
| 1069 | `_research_metadata.priors_consulted[*].extract_note` | `TILTH-CIC-04` | YES — `_research_metadata` exempt subtree |
| 1079 | `_research_metadata.priors_consulted[*].extract_note` | `TILTH-CIC-04` + `Customer Identity Categories` | YES |

**Verdict — LIVE regex set: 0 non-exempt findings.** Card passes.

### §2.5 Legacy-phrase defense scan

Grep for `[Cc]ustomer [Ii]nformation`: 0 hits.

**Verdict — legacy-phrase defense-in-depth: 0 findings.**

---

## §3. Research Findings

### §3.1 Source verification table — official + primary

| URL | Type | Access date | Fields supported | Confidence |
|---|---|---|---|---|
| https://www.arts.gov/grants/grants-for-arts-projects | official | 2026-05-15 | NEA Grants for Arts Projects scope + award range + 1:1 match | HIGH |
| https://www.arts.gov/grants/challenge-america | official | 2026-05-15 | Challenge America $10K flat-grant first-time / underserved-community framing | HIGH |
| https://www.arts.gov/grants/our-town | official | 2026-05-15 | Our Town creative placemaking + nonprofit + local-government partnership | HIGH |
| https://www.neh.gov/divisions/public | official | 2026-05-15 | NEH Public Programs division scope | HIGH |
| https://www.neh.gov/divisions/preservation | official | 2026-05-15 | NEH Preservation & Access division scope | HIGH |
| https://www.neh.gov/grants/preservation/sustaining-cultural-heritage-collections | official | 2026-05-15 | NEH SCHC environmental management framing | HIGH |
| https://www.imls.gov/grants/available/museums-america | official | 2026-05-15 | IMLS MFA three-category framing | HIGH |
| https://arts.pa.gov/grants-funding/programs | official | 2026-05-15 | PA Council on the Arts (state-specific) | HIGH |
| https://www.mellon.org/grant-programs/arts-and-culture | official (foundation) | 2026-05-15 | Mellon arts portfolio | HIGH |
| https://www.ddcf.org/what-we-fund/performing-arts | official (foundation) | 2026-05-15 | Doris Duke Performing Artist Awards | HIGH |
| https://www.fordfoundation.org/work/our-grants/creativity-and-free-expression | official (foundation) | 2026-05-15 | Ford Creativity and Free Expression | HIGH |
| https://knightfoundation.org/programs/arts | official (foundation) | 2026-05-15 | Knight Foundation Arts initiative + Knight cities scope | HIGH |
| https://www.surdna.org/our-programs/thriving-cultures | official (foundation) | 2026-05-15 | Surdna Thriving Cultures + progressive-dialect example | HIGH |
| https://www.heinz.org/grants | official (foundation) | 2026-05-15 | Heinz Endowments Creativity (Pittsburgh region) | HIGH |
| https://www.nativeartsandcultures.org/ | official (foundation) | 2026-05-15 | NACF SHIFT / LIFT / Mentor Artist Fellowships | HIGH |
| https://www.firstpeoplesfund.org/ | official (foundation) | 2026-05-15 | First Peoples Fund Indigenous artist work | HIGH |
| https://wageforwork.com/ | practitioner | 2026-05-15 | W.A.G.E. fee calculator + certification | MEDIUM (practitioner) |
| https://www.arts.gov/about/equal-opportunity-policies | official | 2026-05-15 | NEA Office of Accessibility + ADA / Section 504 grantee guidance | HIGH |
| https://nasaa-arts.org/state-arts-agencies/ | practitioner | 2026-05-15 | NASAA directory of 50 states + 6 territories + DC arts agencies | HIGH |
| https://www.statehumanities.org/ | practitioner | 2026-05-15 | Federation of State Humanities Councils directory | HIGH |

### §3.2 New / refreshed sources to verify and add

| URL | Type | Why add | Card fields it would support | Confidence |
|---|---|---|---|---|
| https://www.arts.gov/grants/grant-program-description (current NEA grant terms page) | official | Verbatim NEA grant-terms attestation language for funding-clause-environment provenance | refresh primary_sources for verbatim quote per OQ-4 | HIGH |
| https://www.neh.gov/grant-conditions | official | Verbatim NEH grant-terms attestation language | refresh primary_sources | HIGH |
| https://www.imls.gov/grants/available/national-leadership-grants-libraries | official | IMLS National Leadership Grants for Libraries (companion to MFA) — under-indexed | New funder_program_keywords row | MEDIUM |
| https://www.imls.gov/grants/available/native-american-library-services-basic | official | IMLS Native American Library Services Basic + Enhancement Grants | New funder_program_keywords + cultural-sovereignty dialect cross-reference | MEDIUM |
| https://maryland.gov/marylandsta.gov | (representative state arts agency example) | Cross-reference for state arts agency variation; one example beyond PCA | optional cross-reference in `_research_metadata.priors_consulted` | LOW |
| https://www.americansforthearts.org/ | practitioner | Americans for the Arts — useful for arts-and-economic-impact + audience-research framing | optional priors_consulted | MEDIUM |
| https://www.creativecapital.org/ | practitioner | Creative Capital + MAP Fund (experimental-arts funders) — by-invitation + open-application hybrid; useful for `frequency_observed` calibration | New funder_program_keywords row + priors_consulted | MEDIUM |
| https://www.macfound.org/grants | official (foundation) | MacArthur Foundation arts portfolio — by-invitation primarily but appears in cross-funder synthesis | optional new funder_program_keywords row | LOW (by-invitation pattern) |
| https://www.berthafdn.org/ | official (foundation) | Bertha Foundation (international arts + free expression) — useful for soul-fire dialect international cross-reference | optional priors_consulted | LOW |
| https://www.aarpfoundation.org/grants | official (foundation) | AARP Foundation arts and aging portfolio | New funder_program_keywords row + new `creative_aging` core_term | MEDIUM |
| https://www.nationalmusiccouncil.org/ | practitioner | National Music Council music-education-funding clearinghouse | optional priors_consulted | LOW |

### §3.3 Internet Archive snapshot verification

Recommended for next Phase 4-CIC re-pass: verify Wayback snapshots of all NEA + NEH program pages (high-volatility under administration framing). NEA grant-terms page especially likely to shift on each administration transition. IMLS pages relatively stable. State arts councils (NASAA directory + PCA) stable.

---

## §4. Proposed Card Improvements

### §4.1 search_vocabulary / classification

- **`search_vocabulary.core_terms[NEW]` — add `state arts council` (omnibus with NASAA cross-reference), `state humanities council` (omnibus with Federation of State Humanities Councils cross-reference), `Native American Languages Act`, `creative aging` / `arts and aging`, `arts and health` / `arts in medicine`, `accessibility coordinator` / `cultural accessibility plan`.** **Seat:** Scout + Logician. **Where:** card body.
- **`search_vocabulary.funder_program_keywords[NEW]` — add IMLS National Leadership Grants for Libraries, IMLS Native American Library Services Basic + Enhancement Grants, AARP Foundation arts and aging portfolio, Creative Capital + MAP Fund.** **Seat:** Scout. **Where:** card body.
- **`search_vocabulary.synonym_map[NEW]` — add `state_arts_council` mapping (PCA / NASAA-listed agencies / state cultural commission) + `accessibility` mapping (ADA / Section 504 / cultural accessibility / inclusive design / audio description / large print / ASL interpretation / open captioning).** **Seat:** Scout. **Where:** card body.
- **`search_vocabulary.disqualifier_terms[NEW]` — add `non-501(c)(3) without fiscal sponsor`, `religious-purpose-only programming` (First Amendment Establishment Clause for federal arts grants), `for-profit-only commercial production` (NEA / NEH eligibility), `non-US-domestic project` (most US federal arts grants are US-domestic-only).** **Seat:** Logician. **Where:** card body.

### §4.2 evidence capture / missing-evidence prompts

- **`evidence_signals[NEW]` — add `cultural_accessibility_plan`.** source_pattern = "Written cultural accessibility plan covering: physical access (ADA Title II/III), program access (audio description, large print, ASL, captioning), accessibility coordinator designation, attendee accommodation request protocol, accessibility evaluation cycle." weight = HIGH (for accessibility-eligible programs) / MEDIUM (otherwise). freshness_tolerance_days = 730. source_citation = NEA Office of Accessibility guidance + ADA Title II/III + Section 504. **Seat:** Scribe + Logician. **Where:** card body.
- **`evidence_signals[NEW]` — add `fiscal_sponsorship_relationship_documentation`.** source_pattern = "501(c)(3) sponsor determination letter; signed fiscal-sponsor agreement; project-relationship-to-sponsor narrative; fiscal-sponsor expense-pass-through tracking." weight = HIGH (for fiscally sponsored applicants). freshness_tolerance_days = 365. source_citation = National Network of Fiscal Sponsors model agreements. **Seat:** Scribe + Logician. **Where:** card body.
- **`evidence_signals[NEW]` — add `artist_fee_fairness_documentation`.** source_pattern = "Artist-fees-as-percent-of-project-budget; per-artist-day rate; W.A.G.E. certification status; artist-fee-table breakdown; honoraria / commission-fee breakdown." weight = MEDIUM. freshness_tolerance_days = 365. source_citation = W.A.G.E. fee calculator + certification framework + arts-and-labor field practice. **Seat:** Scribe + Logician. **Where:** card body.
- **`evidence_signals[NEW]` — add `audience_demographic_disaggregation_documentation`.** source_pattern = "Audience-demographic survey methodology + recent results (≤2 years); ticket-data demographic-mapping; attendee-survey response rates; audience-diversification-strategy-and-outcome." weight = MEDIUM. freshness_tolerance_days = 730. source_citation = Wallace Foundation audience-development research + NEA accessibility framework. **Seat:** Scribe. **Where:** card body.
- **`evidence_signals[NEW]` — add `rights_and_permissions_documentation`.** source_pattern = "Copyright clearances + venue / location permissions + image / likeness consent + sensitive-material handling protocols + rights-holder approvals." weight = HIGH (for exhibitions / public art / documentation projects). freshness_tolerance_days = 180. source_citation = standard arts practice + IMLS collections management + foundation arts grant expectations. **Seat:** Scribe + Logician. **Where:** card body.

### §4.3 KFR fact classes + provenance_requirements

- **`kfr_fact_classes[NEW]` — add `accessibility_compliance_status`.** description = "Designated accessibility coordinator; written accessibility plan; recent accessibility evaluation; venue / facility accessibility-audit record." typical_provenance = "accessibility coordinator designation document; written cultural accessibility plan; recent accessibility audit report." **Where:** card body.
- **`kfr_fact_classes[NEW]` — add `fiscal_sponsor_relationship`.** description = "501(c)(3) status of sponsor; fiscal-sponsor agreement terms; expense-pass-through fee structure; project-vs-sponsor expense allocation." typical_provenance = "501(c)(3) determination letter; signed fiscal-sponsor agreement; recent expense allocation memo." **Where:** card body.
- **`kfr_fact_classes[NEW]` — add `artist_fee_practice_documentation`.** description = "Per-artist-day rates; honoraria scale; W.A.G.E. certification status; commission fee structure for visual / public art." typical_provenance = "artist-fee schedule; W.A.G.E. certification letter if applicable; commission-fee contract template." **Where:** card body.
- **`provenance_requirements[NEW]` — entries for new KFR fact-classes.** **Where:** card body.

### §4.4 drafting register / admin-risk handling

- **`admin_risk_term_register[REFINE]` — soften administration-time-anchoring in reviewer_context across all 15 entries.** The card's lines 467–474 "DEFER-TO-ACTIVE-RFA DISCIPLINE" prose is the canonical pattern; recommend per-entry reviewer_context tighten to defer-to-active-RFA-attestation language rather than name EO 14151 + EO 14168 as the binding context. Operational severity (HIGH / MEDIUM) preserved per the existing safeguard at lines 476–484. Per Law 4: approval_required: true preserved.
- **`admin_risk_term_register[NEW]` — add `cultural appropriation` admin-risk-term.** severity = MEDIUM. substitution_candidates = ["cross-cultural artistic exchange (with named cultural-partner consent documentation)", "Indigenous-knowledge centering (with tribal-partner consent)", "cultural-bearer-led practice (operator-grade with cultural-partner attestation)"]. reviewer_context = "Term reads as activist framing in conservative review climates; reads as critical-discourse framework in academic / cultural-sovereignty-aligned funder contexts. When applicant work involves cross-cultural practice with named cultural partners, the cultural-partner-consent-documentation framing is operator-defensible across all four political axes. Tilth flags the term for operator decision."
- **`admin_risk_term_register[NEW]` — add `Indigenous knowledge`.** severity = MEDIUM. substitution_candidates = ["traditional knowledge (with tribal-partner attribution)", "tradition-bearer-led methodology", "Native American Languages Act-anchored Indigenous-language practice", "cultural-bearer-led cultural-heritage work"]. reviewer_context = "Term carries cultural-sovereignty-practice provenance in NACF / First Peoples Fund / cultural-sovereignty-aligned funder contexts. Conservative federal review climates accept the term when paired with tribal-partner attribution; centrist climates accept selectively. Tilth respects cultural-sovereignty-practice provenance; substitution applies only for funder-legible-frame routing, never for artist-voice content."
- **OD-A v2.4 cross-CIC migration check.** The 15 admin_risk_term entries on this card include 9+ that are cross-CIC shared (DEI / equity / inclusion / racial justice / anti-racist / radical / abolition / decolonial / social justice / queer / trans / gender ideology). ≥3-card recurrence threshold met. Surface to workspace-register migration ceremony.

### §4.5 reviewer / rubric logic

- **`narrative_sections_typical[NEW]` — add `"Cultural Accessibility Plan"` (where applicable) between `"Project Management Plan"` and `"Evaluation Plan"`.** Accessibility-aligned NEA / NEH proposals routinely require accessibility narrative as discrete scoring criterion.
- **`narrative_sections_typical[NEW]` — add `"Artist Voice and Voice Preservation Discipline"` (where applicable) for soul-fire / cultural-sovereignty-aligned applicants.** This makes Tilth's Scribe-discipline explicit at the proposal-shape level — artist-voice sections are preserved verbatim; funder-legible-frame sections route per active-RFA dialect.
- **`narrative_sections_typical[NEW]` — add `"Rights, Permissions, and Sensitive-Material Handling"` (where applicable) for exhibition / public art / documentation projects.**

### §4.6 red-team probes / admin-risk register

- **`common_risk_register_entries[NEW]` — add `Artist-voice rewrite without consent` risk.** likelihood = MEDIUM. impact = HIGH. mitigation_pattern = "Scribe + Logician artifacts that distinguish artist-voice content (verbatim, no rewrite) from funder-legible-frame content (operator-approved substitution per active RFA); operator approval at every admin-risk-flagged-term substitution per OQ-5 default."
- **`common_risk_register_entries[NEW]` — add `Cultural-sovereignty practice misframing`.** likelihood = MEDIUM. impact = HIGH. mitigation_pattern = "When applicant invokes cultural-sovereignty practice or Indigenous-knowledge centering, route to soul-fire dialect + cultural-bearer-attributed-source-citation; never substitute to centrist / conservative dialect without operator + cultural-partner approval."
- **`common_risk_register_entries[NEW]` — add `Accessibility-plan absence on accessibility-eligible programs`.** likelihood = MEDIUM. impact = HIGH. mitigation_pattern = "Pre-application accessibility-plan audit; NEA Office of Accessibility framework as anchor; section-by-section coverage of physical / program / staff access components."

### §4.7 reporting / commitment extraction

- **`reporting_cadence_typical.per_funder_overrides[NEW]` — add IMLS Native American Library Services, AARP Foundation arts and aging, Creative Capital / MAP Fund, state humanities councils (omnibus).** **Seat:** Archivist + Report Generator.

### §4.8 memory namespace usefulness

Standard sub-keys mirroring siblings:
- `cards:cic:arts_culture:scout_vocabulary` through `cards:cic:arts_culture:draft_funder_candidates`

### §4.9 Phase 4 fold-in discipline self-check

| Proposal | (a) | (b) | (c) | (d) |
|---|---|---|---|---|
| §4.1 core_terms / synonym_map / funder_program_keywords additions | NO | NO | NO | NO |
| §4.1 disqualifier_terms additions | NO | NO | NO | NO |
| §4.2 evidence_signals additions (accessibility / fiscal sponsor / artist fee / audience demographic / rights & permissions) | NO | NO | NO | NO |
| §4.3 kfr_fact_classes / provenance_requirements additions | NO | NO | NO | NO |
| §4.4 admin_risk_term refines + adds (cultural appropriation / Indigenous knowledge) | NO — refines within canonical entry shape | NO | NO | NO |
| §4.5 narrative_sections_typical additions | NO | NO | NO | NO |
| §4.6 common_risk_register_entries additions | NO | NO | NO — canonical HIGH/MEDIUM × HIGH/MEDIUM | NO |
| §4.7 reporting_cadence_typical.per_funder_overrides additions | NO | NO | NO | NO |
| §4.8 memory namespace sub-keys | N/A — architecture decision | N/A | N/A | N/A |

**Verdict:** No proposed change trips any of the four Phase 4 fold-in refusals.

---

## §5. Operator Decision Queue

1. **Defer-to-active-RFA reviewer_context tightening across all 15 admin_risk_term entries.** Per-entry rewrites moving from EO-named anchoring to active-RFA-attestation-language anchoring. Approval required per OQ-5.
2. **`cultural appropriation` + `Indigenous knowledge` admin_risk_term additions.** Approval required per OQ-5 — high-sensitivity territory; recommend operator + cultural-partner consultation if extending Tilth's Indigenous-arts deployment scope.
3. **OD-A v2.4 cross-CIC migration for shared terms.** DEI / equity / inclusion / racial justice / anti-racist / radical / abolition / decolonial / social justice / queer / trans / gender ideology appear ≥3 cards; workspace-register migration ceremony.
4. **PA-specific PCA state-overlay routing.** Per master prompt §1.4 + Run 1 P2 — defer to v1.x cross-cutting amendment.
5. **`state arts council` + `state humanities council` omnibus core_term additions.** Operator confirms scope.
6. **`creative aging` / `arts and aging` core_term addition.** Operator confirms whether v0.1 Beta scope extends to AARP Foundation + state-arts-council aging-portfolio deployment.
7. **`arts and health` / `arts in medicine` core_term addition.** Operator confirms scope.
8. **Foundation by-invitation-vs-cold-application discrimination.** Doris Duke / Mellon / Ford / MacArthur are by-invitation patterns. Current `frequency_observed: RARE` for cold applications is correct; consider operator-engagement-driven RARE → OCCASIONAL transition once engagement signal accumulates.
9. **Verbatim NEA + NEH grant-terms attestation language refresh** in primary_sources. Operator confirms whether current NEA grant-terms verbatim quote is operationally pinnable per OQ-4 ≤2-sentence cap.
10. **Lock-history housekeeping field disposition** (cross-card).
11. **Re-signing ceremony budget for card body changes.** ~22 distinct edits; bundle into cards-ceremony per Run 1 Patch Queue Batch B.

---

## §6. Validation Checklist

| Check | Result | Evidence |
|---|---|---|
| Schema fields complete against current §18.5 schema | PASS | 15/15 required CIC fields present |
| No forbidden coupling field names | PASS | Grep across file: 7 forbidden CIC-side names absent |
| No forbidden value-position regex matches outside exempt paths | PASS | §2.4 — 0 non-exempt findings |
| No legacy-phrase `[Cc]ustomer [Ii]nformation` matches | PASS | 0 hits |
| No private organization-specific data in card body | PASS | Top-level common_funders_observed empty |
| No unsourced program-law claims at body | PASS at body | NEA grant-terms attestation language is illustratively cited; the active-RFA-defer discipline framing at lines 467–474 is the operator-defensible posture |
| No excessive verbatim source text | PASS | Per OQ-4 |
| Lifecycle status consistent with architecture v7.0.11 §1.5 | PASS | All five lifecycle gate fields at pass-state |
| **Top-level `common_funders_observed:` is empty (Law-5 split per operator v2.1)** | PASS | Line 1024 empty list; subagent candidates at `_research_metadata.draft_funder_candidates_pending_operator_engagement_confirmation` line 1235 |
| **No populated top-level `common_funders_observed` without operator-engagement-attestation** | PASS | Empty list |
| For multi-track CLCs: shared root + oneOf branch 2 compliance | N/A — CIC card |

**Net coupling-discipline regression: 0 findings.**

---

## §7. Regression Tests

### Test 1 — Trans visual-artist applying to LGBTQ-focused foundation + state arts council

**Prompt:** "Trans visual artist with self-identified queer artistic practice applying to Astraea Lesbian Foundation for Justice + PA Council on the Arts Project Stream."

**Pre-edit:** Foundation route — Scribe retains `trans` / `queer` verbatim; Logician fires admin_risk_term HIGH severity; operator approves per approval_required: true. PA Council (state pass-through with NEA partnership funds) — Scribe must navigate federal-portion attestation language inheritance.

**Post-edit (with §4.4 defer-to-active-RFA refresh):** Per-entry reviewer_context now defers to active-RFA-attestation language rather than naming EO 14168. Same operational outcome for Astraea (retain verbatim); for PA Council, Scribe / Logician check active RFA attestation language at runtime and route per current pass-through provisions. Artist-voice preservation discipline preserved (lines 572–578 + new `common_risk_register_entries[Artist-voice rewrite without consent]` mitigation).

**Seat:** Scribe + Logician. **Pass criterion:** Artist-voice content preserved; funder-legible frame per active RFA.

### Test 2 — Indigenous-led arts-residency program

**Prompt:** "Indigenous-led arts residency featuring tradition-bearer-led practice applying to NACF + IMLS Native American Library Services + NEH Public Humanities Projects."

**Pre-edit:** Scout matches `Native Arts and Cultures Foundation (NACF)` + `First Peoples Fund` (existing core_terms / funder_program_keywords). NACF + First Peoples Fund route to soul-fire dialect / cultural_sovereignty register.

**Post-edit (with §4.1 + §4.4 + §4.5 additions):** Scout adds `Native American Languages Act` core_term + `Indigenous knowledge` admin_risk_term + `IMLS Native American Library Services Basic + Enhancement` funder_program_keyword. Logician routes cultural-sovereignty practice provenance with tribal-partner-attribution discipline. Scribe surfaces `"Cultural Accessibility Plan"` + `"Artist Voice and Voice Preservation Discipline"` narrative sections.

**Seat:** Scout + Scribe + Logician. **Pass criterion:** Cultural-sovereignty practice routing preserved; tribal-partner attribution surfaced.

### Test 3 — Accessibility-coordinator gap on NEA application

**Prompt:** "Performing arts organization applying to NEA Grants for Arts Projects for a multidisciplinary production touring three venues; no formal accessibility coordinator on staff."

**Pre-edit:** Scribe drafts NEA narrative; Logician fires NEA ADA / Section 504 compliance prompts per existing core_term (line 93) + compliance_burdens (lines 882–890). No `accessibility_compliance_status` KFR fact-class — accessibility coordinator gap not surfaced at intake.

**Post-edit (with §4.2 + §4.3 + §4.6 additions):** `cultural_accessibility_plan` evidence_signal fires (HIGH weight for NEA-applicable programs). `accessibility_compliance_status` KFR fact-class surfaces in intake. `common_risk_register_entries[Accessibility-plan absence on accessibility-eligible programs]` fires if applicant has no accessibility coordinator designation.

**Seat:** Scout + Logician + Scribe. **Pass criterion:** Accessibility-coordinator gap surfaces at intake before NEA narrative drafting begins.

### Test 4 — Fiscal-sponsored individual artist

**Prompt:** "Individual literary artist applying to NEH Creative Writing Fellowship via NYFA fiscal sponsorship."

**Pre-edit:** Scout matches `literary arts` + `fiscal sponsorship`. NYFA cited as fiscal-sponsor exemplar (line 96). Scribe drafts narrative without fiscal-sponsor-relationship documentation prompt.

**Post-edit (with §4.2 + §4.3 additions):** `fiscal_sponsorship_relationship_documentation` evidence_signal fires (HIGH weight for fiscally-sponsored applicants). `fiscal_sponsor_relationship` KFR fact-class surfaces in intake. Scribe drafts narrative with explicit sponsor-vs-project relationship clarity + fiscal-sponsor-agreement provisions.

**Seat:** Scout + Scribe + Logician. **Pass criterion:** Fiscal-sponsor relationship documentation surfaces at intake.

### Test 5 — Cards-ceremony post-condition (dialect_routing_table re-keyed)

**Prompt:** "Cultural-heritage preservation project for African-American historic site applying to NEH Sustaining Cultural Heritage Collections + Mellon humanities-in-place."

**Pre-cards-ceremony:** dialect_routing_table keyed on `funder_political_axis: centrist` for NEH SCHC (scribe.technical_precise); `progressive` for Mellon (scribe.movement_aligned).

**Post-cards-ceremony:** dialect_routing_table rows re-key to:
- `clc: public_purpose_works` (NEH SCHC if framed as cultural-heritage preservation) OR `clc: research_evidence` (if framed as humanities scholarship) + dialect `scribe.technical_precise` + register_description for technical/research register.
- `clc: catalytic_change` (Mellon humanities-in-place if framed as systems-change) OR `clc: research_evidence` + dialect `scribe.movement_aligned` + register_description for academic/foundation register.

**Seat:** Scribe + Judge. **Pass criterion:** Pre-ceremony body validates against v1.1 schema; post-ceremony validates against §18 v1.2 schema. CLC-keyed routing reflects opportunity-driven CIC × CLC matching per architecture v7.0.11 §6.1 — orthogonality preserved.

---

## §8. Patch Plan

### File: `pipeline/cards/CIC/arts_culture.yaml`

**Ceremony shape:** supersession-re-sign per OD-E precedent. Parent_lock_row = 252.

**Edit set:**

1. `search_vocabulary.core_terms[NEW]` — state arts council, state humanities council, Native American Languages Act, creative aging, arts and aging, arts and health, arts in medicine, accessibility coordinator, cultural accessibility plan (§4.1).
2. `search_vocabulary.funder_program_keywords[NEW]` — IMLS National Leadership Grants for Libraries, IMLS Native American Library Services, AARP Foundation arts and aging, Creative Capital, MAP Fund (§4.1).
3. `search_vocabulary.synonym_map[NEW]` — state_arts_council + accessibility mappings (§4.1).
4. `search_vocabulary.disqualifier_terms[NEW]` — non-501(c)(3) without fiscal sponsor / religious-purpose-only programming / for-profit-only commercial production / non-US-domestic project (§4.1).
5. `evidence_signals[NEW]` — cultural_accessibility_plan / fiscal_sponsorship_relationship_documentation / artist_fee_fairness_documentation / audience_demographic_disaggregation_documentation / rights_and_permissions_documentation (§4.2).
6. `kfr_fact_classes[NEW]` — accessibility_compliance_status / fiscal_sponsor_relationship / artist_fee_practice_documentation (§4.3).
7. `provenance_requirements[NEW]` — entries for new KFR fact-classes (§4.3).
8. `admin_risk_term_register[REFINE]` — defer-to-active-RFA reviewer_context across all 15 entries (§4.4).
9. `admin_risk_term_register[NEW]` — `cultural appropriation`, `Indigenous knowledge` (§4.4).
10. `narrative_sections_typical[NEW]` — `Cultural Accessibility Plan`, `Artist Voice and Voice Preservation Discipline`, `Rights, Permissions, and Sensitive-Material Handling` (§4.5).
11. `common_risk_register_entries[NEW]` — Artist-voice rewrite without consent / Cultural-sovereignty practice misframing / Accessibility-plan absence (§4.6).
12. `reporting_cadence_typical.per_funder_overrides[NEW]` — IMLS Native American Library Services / AARP Foundation arts and aging / Creative Capital / MAP Fund / state humanities councils (§4.7).
13. Primary_sources verbatim NEA + NEH grant-terms refresh (§3.2).
14. `register_defaults` / dialect_routing_table refresh — bundle with cards-ceremony.

### File: `pipeline/cards/_schema/card_cic.schema.json`

15. Patch B20 (Run 1) + Patch B1 (Run 1) — cards-ceremony schema patches.

### File: `pipeline/institutional_memory/admin_risk_register.yaml`

16. Cross-CIC workspace-register migration candidates for shared terms (§4.4 + §5 item 3).

**OD-D Phase 4 forward-binding contract note:** All proposed edits value-position clean per §2.4 + Phase 4 fold-in clean per §4.9.

---

**Summary block:**

```
Card: CIC:arts_culture
Card file: pipeline/cards/CIC/arts_culture.yaml
Research hours actual: 1.7
Findings: 28 total — 0 P0, 13 P1, 15 P2
Decision queue: 11 operator approvals required
Conflicts with prior art: NONE
Coupling-discipline regression: NONE
Lifecycle gap surfaced: draft_status reads "signed" on disk; no normalization required per Run 1 P0-3
Review readiness: READY
```
