# TILTH-CLC-04 Research & Evidence — Research Handback

**Filed:** 2026-05-17
**Workspace:** `/Users/goldenquill/Downloads/GoldenQuill/`
**Run:** Run 2 Phase 4-CLC (1 of 8 CLC handbacks dispatched in parallel).
**Card:** `pipeline/cards/CLC/research_evidence.yaml` (Wave 2 LOCKed 2026-05-16 row 257; `content_hash sha256:d1304309…a68ec`; `signed_at 2026-05-16T16:00:00Z`; `signed_by founder`).
**Shape:** single-track (oneOf branch 1 of §18.6 v2 schema).
**Authority chain:** master prompt `docs/cic_clc_unified_master_prompt_2026-05-17.md` §2 + plan `docs/cic_clc_unified_research_plan_2026-05-17.md` §2.4 + Run 1 priors at `docs/card_system_deep_research_2026-05-17/` (binding).

**Run 1 priors folded in (do not re-surface):**
- All 14 cards on disk are `draft_status: "signed"` (P0-3 / L1-F0 — no normalization needed).
- §18 v1.2 dialect_routing_table re-keying is LOCKed-but-not-applied (this card has no `dialect_routing_table` — CIC-only field — so L2-F0 is structurally inapplicable here; surface only).
- Operator v2.1 Law-5 split state for CLC cards is UNCONFIRMED (master prompt is silent; on-disk inspection of this card's `common_funders_observed` shape needs operator ruling — surface in §2.3 / §5).
- F-CARDS-COUPLING-VIOLATION-EXTENSION predicate body raises `NotImplementedError` at runtime; value-position regex scan is manual today.
- Operator reframe: aggressive content improvements OK to recommend; re-signing ceremony cost acceptable.

---

## §1. Card Impact Thesis

`research_evidence` is the CLC-04 underwriting card for **inquiry, evaluation, pilots, and proof-building funding** where research design rigor, methods fit, IRB / data management, and dissemination drive underwriting decisions. The card encodes the funder-side grammar that NIH study sections, NSF panels, USDA NIFA AFRI peer-reviewers, USDA SARE regional reviewers, IES standing panels, and foundation evaluation officers actually use.

What this card should *cause Tilth to do differently* relative to a research-naive baseline:

1. **Force the question-method-data-IRB-dissemination chain at intake.** When Scout/Scribe see "evaluation," "pilot," "study," "demonstration," "evidence base," the card forces five reviewer demands in order — specific testable question, design-fit, sample/measures, IRB plan if humans, data-management plan with named repository — before drafting moves forward.
2. **Distinguish mechanism class at the start of drafting.** Basic / applied / evaluation / demonstration / participatory / field-trial / SBIR-STTR / education-research are different mechanism classes with different evidence weights, different forms, different reviewer profiles. Wrong-mechanism choice is the #1 program-officer-side rejection.
3. **Hold the SBIR research-vs-market boundary clean.** Per §18.6 v2 OD-E (row 274): SBIR Phase II commercial-readiness-with-further-SBIR-funds and Phase III commercialization-without-SBIR-funds live on Market Access (CLC-05). Research & Evidence stays research-rigor-side — Phase I feasibility, Phase II R&D-substance, and the Commercialization Plan *as a research-rigor artifact* (TRL staging + IP position + scientific feasibility tier) belong here.
4. **Force named repository + persistent identifier + sharing timeline at proposal time.** NIH 2023 DMS Policy + NSF DMP (since 2011) + most federal research now require this; Logician fails closed on "data will be available upon request" prose.
5. **Honor mechanism-coded preliminary-data expectations.** R01 / AFRI standard → HIGH; R21 / R03 / EAGER / SBIR Phase I → MEDIUM by design. The card-encoded mechanism dependency steers Judge and Red Team away from boilerplate "preliminary data missing" critiques on early-stage mechanisms.
6. **Surface the §18.19.4 funding-pathway probability.** Per research plan §2.4: `research_evidence` is the probable CLC match for the §18.19 three-arm reviewer study's own funding pitch (alternates: Catalytic Change, Market Access). The card's evidence-rigor grammar should map cleanly to that pitch when Scout surfaces it.

The runtime-behavior delta this card should produce versus a research-naive baseline is **mechanism-precise routing + provenance-strict evidence demand + IRB/DMP/dissemination as gate-not-decoration**. Strong on (1)/(2)/(4)/(5). (3) is bottlenecked on opportunity-driven CLC matching at runtime per architecture v7.0.11 §6.1, not a card-body coupling. (6) requires Scout-to-CLC routing test for the §18.19 study and is operator scope.

---

## §2. Current State Audit

### §2.1 What is strong now

- **Twelve well-anchored underwriting criteria.** `underwriting_criteria` (lines 30–89) covers research_question, significance, method_fit, data_collection_plan, evaluation_rigor, team_qualifications, human_subjects_irb, data_management_plan, dissemination_plan, broader_impacts, feasibility, preliminary_data — each with a CFR / NIH / NSF / IES anchor. The mechanism-coded preliminary-data expectation (line 87–89) explicitly says HIGH for R01 / AFRI standard, MEDIUM for R21 / R03 / EAGER / SBIR Phase I — exactly the Judge / Red Team discipline needed.
- **Five-rubric scoring_weight_patterns (lines 96–134).** NIH (5+1 criteria, 1–9 scoring, simplified review framework noted for 2025), NSF (Intellectual Merit + Broader Impacts; statutory since 1997), USDA NIFA AFRI (per-RFA disclaimer), USDA SARE (four regional + per-program), IES (4 criteria across NCER/NCSER). Each row preserves the qualitative-only posture per OQ-6.
- **HIGH-weighted IRB and DMP evidence_weights (lines 169–172, 164–167).** IRB rationale enumerates sIRB / Subpart B / C / D / cognitively impaired adults / consent workflows / identifiable-data protection. DMSP rationale enumerates the NIH 2023 six required elements. Reviewer-realistic, not boilerplate.
- **Commercialization Plan as research-side evidence (lines 197–200, 323–331).** Commercialization Plan + Intellectual Property & TRL are named as narrative sections; weighted HIGH on `evidence_weights.commercialization_plan` with explicit "SBIR / STTR mechanisms only" scoping. This is the clean research-side framing — TRL staging + IP position + scientific feasibility tier — that holds the Phase II / Phase III boundary with Market Access.
- **Dissemination upward-shift documented (line 184–186).** MEDIUM baseline for fundamental research; reviewer-weighting shifts upward for translational, applied, education, community-engaged work. Encoded as rationale prose rather than a compound enum value per §18 v1.1 schema closed set — correct fold-in discipline.
- **Twenty named portals + forms (lines 205–262, 398–437).** SF-424 R&R, PHS 398, ASSIST, Research.gov, Grants.gov Workspace, NIFA, SARE regional, IES eApplication, SciENcv-generated biosketch, DMPTool — operationally complete.
- **Adversarial red-team probes (lines 442–498).** 14 flags covering vague_research_question / method_mismatch / underbudgeted_evaluation / human_subjects_glossed / weak_DMP / sample-size / overclaimed_causality / vague_dissemination / team_gaps / no_preliminary_data / scope_creep / broader_impacts_boilerplate / wrong_mechanism_choice. Each has a Red Team probe phrasing usable verbatim.
- **Compliance obligations span 14 frameworks (lines 530–639).** 2 CFR 200, 45 CFR 46, HIPAA, FDA IND/IDE, IACUC, NIH DMSP, NSF Public Access, NIH Public Access, RCR, FCOI, FFATA, FERPA, NIH Inclusion of Women & Minorities, Bayh-Dole — the full federal research compliance grid.
- **Commitment tracking pattern (lines 645–674).** 13 commitment types with measurement_method for each, including SBIR/STTR commercialization milestones tied to Commercialization Plan — feeds Report Generator (v0.2 horizon) cleanly.
- **Lifecycle truth.** `draft_status: signed`, `signature_status: signed`, `runtime_load_status: loaded`, `runtime_loadable: true`, `content_hash sha256:d1304309…a68ec`, `signed_at 2026-05-16T16:00:00Z`, `signed_by: founder`, `lock_history_row: 257`. Architecture v7.0.11 §1.5 production-load satisfied.
- **OD-A migration already executed cleanly.** Comment block at lines 677–691 documents the Phase D Group A admin_risk_term_register removal (10 CLC-04 terms migrated to workspace register). Schema-conformance violation closed.

### §2.2 What is stale, ambiguous, over-broad, too local, too federal, or under-sourced

- **NIH simplified review framework — anchored but light.** Line 106 mentions "Effective 2025, NIH uses a simplified review framework grouping criteria into Factor 1 (Importance of the Research), Factor 2 (Rigor and Feasibility), Factor 3 (Expertise and Resources)." Strong anchor, but the card's NIH rubric_example still enumerates the legacy 5-criteria shape (significance / investigators / innovation / approach / environment). Operator-decision: does the card encode legacy, simplified, or both as named rubric_example rows? **Recommend:** add a second NIH rubric_example keyed on the simplified 3-factor framework so Scribe / Judge route per active FOA; some NIH FOAs already use the simplified framework, others still use legacy.
- **AFRI "per-RFA scoring" anchor is correct but operationally thin.** Lines 115–119 say "operator must read the active-cycle RFA." Correct per OQ-6 qualitative posture — but Scout has no card-encoded scoring anchor for AFRI and must dispatch a runtime fetch from `https://www.nifa.usda.gov/grants/funding-opportunities/agriculture-food-research-initiative-foundational-applied-science`. **Recommend:** add a `scout_runtime_fetch_required: true` field-level signal on the AFRI rubric_example so Scout knows to dispatch live fetch (forward-compat field shape; canonical schema allows `additionalProperties: true` per §18.5).
- **SBIR/STTR research-rigor scoping is precise but Phase-III boundary leans on prose.** The card correctly says Commercialization Plan is HIGH for SBIR/STTR (line 197–200). The §18.6 v2 OD-E partition lives on Market Access — but a researcher reading CLC-04 alone could miss that boundary. **Recommend:** add an explicit cross-CLC reference using the display name (NOT slug) — "When opportunity is SBIR Phase II further-SBIR-funds review or Phase III commercialization-without-SBIR-funds, Market Access track_a (sbir_phase_ii) and track_b (sbir_phase_iii) carry the commercial-readiness scoring; this card holds research-rigor scoring for both Phases."
- **NIH 2023 DMSP six-element coverage is rationale-only.** Line 166–167 enumerates the six required elements inline in `evidence_weights.data_management_plan.rationale`. Reviewer-realistic, but Scribe currently has no structured field-level prompt per element. Per §18.11 v1.1 fold-in discipline, this proposal would be a structured-sub-field expansion (refusal (a)) — surface to operator as a §18 v1.x amendment candidate; do NOT bake into the card body silently.
- **Participatory / CBPR / community-engaged research is partially anchored but thin.** `research_partner_letter` evidence_weight (lines 174–177) names CBPR as a HIGH-weight context and IES Development/Impact as a HIGH-weight context. **Missing:** a dedicated `underwriting_criterion` for participatory partnership rigor (community advisory board, co-PI structure, equitable budget distribution to community partners, partner authorship in dissemination, training-and-capacity-building commitments). Per research plan §2.4: "Separate basic research, applied research, evaluation, demonstration, SBIR/STTR, participatory research, field trials, education research." Participatory research is named but doesn't get its own criterion — folded into research_partner_letter MEDIUM/HIGH. **Recommend:** add `underwriting_criterion: community_engagement_rigor` keyed to CBPR / participatory research standards.
- **Field-trial research mechanism not separately anchored.** USDA AFRI / SARE / NRCS field trials carry different rigor requirements (statistical experimental design with field-block randomization, ANOVA design, treatment replication, growing-season cycles, weather variance handling). `method_fit` rationale (line 41–44) names "RCT, quasi-experimental, mixed methods, qualitative, observational, computational" but doesn't enumerate field-trial design. **Recommend:** extend `method_fit` rationale to include "field-experimental designs (randomized block, split-plot, latin-square) with replication-and-control discipline for USDA SARE / AFRI / NRCS / land-grant research."
- **Education research / IES Development & Impact mechanism boundary is anchored but thin.** Line 130–134 IES rubric_example carries 4 criteria across NCER and NCSER. The IES goal-coded mechanism distinction (Exploration / Development / Impact / Measurement) — where preliminary-data + research-design rigor + analytic-rigor differ across the 4 goals — is in the note but not structured. **Recommend:** add a per-goal note OR surface as a §18 v1.x amendment per refusal (a).
- **Evaluation funding (foundation + federal) not separately anchored.** The card treats evaluation as a mechanism class but doesn't separately enumerate foundation evaluation funds (Hewlett Strategy & Learning, RWJF evaluation, MacArthur strategy & insights). Federal evaluation (IES, NIJ, USDA ERS eval) is covered; private-foundation evaluation rigor is under-anchored. **Recommend:** add foundation-evaluation entries.
- **Verbatim source quotes age out.** Primary sources (lines 743–817) dated `access_date: 2026-05-15`. Annual re-verification against Internet Archive snapshot is the §18.11 discipline. High-priority re-verify: NSF PAPPG (annual policy refresh), NIH DMSP overview (administration-policy posture), NIH Public Access (executive-action volatility per card line 349 note), USDA AFRI funding-opportunities page (cycle-specific RFAs republish), IES funding page, USDA SARE grants page.
- **NIH sIRB policy + reliance-agreement framing — could benefit from updated sources.** Line 62 cites only `https://www.hhs.gov/ohrp/regulations-and-policy/regulations/45-cfr-46/index.html`. The SMART IRB and IAA reliance frameworks have their own canonical pages (https://smartirb.org/, https://grants.nih.gov/grants/guide/notice-files/NOT-OD-16-094.html). Add as supplementary primary_sources.
- **2 CFR 200 — recent updates.** Line 351 cites 2 CFR 200; the 2024 update changed the single-audit threshold to $1M (card's own line 535 says this). Recommend confirming the active threshold text against current eCFR.

### §2.3 Lifecycle / signature / schema concerns

- **`draft_status: "signed"` on disk.** No normalization needed per Run 1 P0-3. The master prompt §5 stale-claim that all 14 cards carry `draft_status: "draft"` is retired (per Run 1 Patch A1). The on-disk card is fully signed.
- **Operator Law-5 split state for CLC cards is UNCONFIRMED.** Per master prompt and research plan, the §18 v1.1 Law-5 reconciliation (`common_funders_observed: []` empty at top-level + candidate funders under `_research_metadata.draft_funder_candidates_pending_operator_engagement_confirmation`) is canonical for CIC cards. **For CLC cards the master prompt is silent.** Inspecting the card structure: `common_funders_observed` is schema-optional on CLC and may carry funder-grammar references (NIH, NSF, USDA NIFA, IES, USDA SARE, foundations). The same `not.anyOf` item-level defense-in-depth applies — but the operator-engagement-attestation question is CIC-side. **Surface to operator decision queue (P0):** Does the operator's v2.1 Law-5 split apply to CLC cards, or is CLC-side `common_funders_observed` exempt because funder identity on the CLC axis is a funder-grammar reference (e.g., "NIH peer review" as a rubric pattern), not an applicant-org-engagement reference?
- **Cross-family Thesis dispatch (Editor + Judge + Red Team)** completed per `_review_handback` (line 838+). No regression.
- **Ed25519 signature present** at `_research_metadata.ed25519_signature` (line 825); content_hash present at lifecycle.content_hash. Architecture v7.0.11 §1.5 production-load satisfied.
- **Header comment alignment.** Line 4 says "Operator review + cross-family thesis + Ed25519 signature COMPLETE. SIGNED — runtime-loadable; lifecycle truth enforced by loader preflight." Header is current.
- **`_research_metadata.research_budget_hours_actual: 3.0` (line 724).** Wave 2 research budget was 3.0h; this Run 2 Phase 4-CLC handback is shorter (see summary).

### §2.4 Coupling-discipline self-audit (per master prompt rule 3 + Run 1 enforcement-context guidance L1-F3)

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

**Results (grep transcript at `pipeline/cards/CLC/research_evidence.yaml`):**

| Line | Path | Match | Exempt? |
|---|---|---|---|
| 1 | (YAML header comment) | `TILTH-CLC-04` | YES — comments stripped from canonical bytes before hash; not in scanner surface |
| 21 | `card_id` | `TILTH-CLC-04` | YES — `_VALUE_POSITION_EXEMPT_PATHS` |
| 25 | `tilth_clc_id` | `TILTH-CLC-04` | YES — `_VALUE_POSITION_EXEMPT_PATHS` |
| 726 | `_research_metadata.priors_consulted[0].path` | `capital_logic` (file-path segment of PNG) | YES — `_research_metadata` top-level key starts with `_` |
| 727 | `_research_metadata.priors_consulted[0].extract_note` | `TILTH-CLC-00` + `TILTH-CLC-04` + "Capital Logic Cards" | YES — same exempt subtree |
| 729 | `_research_metadata.priors_consulted[1].extract_note` | `TILTH-CLC-04` | YES — same exempt subtree |
| 741 | `_research_metadata.priors_consulted[7].extract_note` | `TILTH-CLC-04` | YES — same exempt subtree |

**Verdict — LIVE regex set: 0 non-exempt findings.** Card passes.

### §2.5 Legacy-phrase defense scan (per Run 1 Phase 2 L2-F3 — not in current regex set; surface as defense-in-depth)

Grep for `[Cc]ustomer [Ii]nformation` across the card: 0 hits.

**Verdict — legacy-phrase defense-in-depth: 0 findings.** No regression risk.

---

## §3. Research Findings

### §3.1 Source verification table — official + primary (15 currently on card)

| URL | Type | Access date | Fields supported | Confidence |
|---|---|---|---|---|
| https://grants.nih.gov/grants/peer/critiques/rpg.htm | official | 2026-05-15 (card line 744) | NIH peer-review 5-criteria + Overall Impact scoring | HIGH |
| https://www.nsf.gov/pubs/policydocs/pappg/index.jsp | official | 2026-05-15 (card line 749) | NSF Intellectual Merit + Broader Impacts statutory framework | HIGH |
| https://www.nsf.gov/funding/preparing/broaderimpacts.jsp | official | 2026-05-15 (card line 754) | NSF Broader Impacts criterion definition | HIGH |
| https://sharing.nih.gov/data-management-and-sharing-policy/about-data-management-and-sharing-policies/data-management-and-sharing-policy-overview | official | 2026-05-15 (card line 759) | NIH 2023 DMSP | HIGH |
| https://www.hhs.gov/ohrp/regulations-and-policy/regulations/45-cfr-46/index.html | official | 2026-05-15 (card line 764) | 45 CFR 46 / Common Rule | HIGH |
| https://grants.nih.gov/grants/forms/biosketch.htm | official | 2026-05-15 (card line 769) | NIH Biosketch 5-page max + SciENcv | HIGH |
| https://www.nifa.usda.gov/grants/funding-opportunities/agriculture-food-research-initiative-foundational-applied-science | official | 2026-05-15 (card line 774) | USDA AFRI six priority areas | HIGH |
| https://www.sare.org/grants/ | official | 2026-05-15 (card line 779) | USDA SARE four-region structure | HIGH |
| https://ies.ed.gov/funding/grants.asp | official | 2026-05-15 (card line 784) | IES NCER/NCSER programs + 4 goals | HIGH |
| https://www.grants.gov/forms/r-r-family.html | official | 2026-05-15 (card line 789) | SF-424 R&R federal-wide forms | HIGH |
| https://publicaccess.nih.gov/ | official | 2026-05-15 (card line 794) | NIH Public Access — PMC deposit within 12 months | HIGH |
| https://www.ecfr.gov/current/title-2/subtitle-A/chapter-II/part-200 | official | 2026-05-15 (card line 799) | 2 CFR 200 Uniform Guidance | HIGH |
| https://grants.nih.gov/grants/rppr/rppr_instruction_guide.pdf | official | 2026-05-15 (card line 804) | NIH RPPR | HIGH |
| https://www.research.gov/research-web/ | official | 2026-05-15 (card line 809) | NSF Research.gov (FastLane decommissioned) | HIGH |
| https://dmptool.org/ | official (CDL) | 2026-05-15 (card line 814) | DMPTool agency templates | HIGH |

15 primary_sources — meets OQ primary-source floor (8–15) at the ceiling.

### §3.2 New / refreshed sources to verify and add

| URL | Type | Why add | Card fields it would support | Confidence |
|---|---|---|---|---|
| https://grants.nih.gov/policy-and-compliance/policy-topics/peer-review/simplified-review-framework | official | NIH simplified review framework (2025-effective) | New `scoring_weight_patterns[*]` row | HIGH |
| https://nexus.od.nih.gov/all/2023/05/03/new-simplified-review-framework-for-most-research-project-grant-applications/ | official | NIH simplified-framework rollout details | Supporting anchor | HIGH |
| https://smartirb.org/ | official | SMART IRB reliance master agreement | Supplementary IRB anchor | HIGH |
| https://grants.nih.gov/grants/guide/notice-files/NOT-OD-16-094.html | official | NIH single-IRB policy notice | Same | HIGH |
| https://www.nsf.gov/awardsearch/ | official | NSF awarded-project search; Broader Impacts precedent | Optional priors entry | MEDIUM |
| https://reporter.nih.gov/ | official | NIH RePORTER funded-project database | Optional priors entry | MEDIUM |
| https://www.nifa.usda.gov/about-nifa/how-we-work/grant-management/grant-application-review-process | official | USDA NIFA grant application review process | Refresh AFRI rubric_example anchor | HIGH |
| https://www.sbir.gov/funding | official | SBIR program-by-agency overview | Supplementary SBIR anchor; pairs with Market Access | HIGH |
| https://www.sbir.gov/sbirsearch/award/all | official | SBIR awards database; Phase II/III precedent search | Optional priors entry | MEDIUM |
| https://ies.ed.gov/ncer/projects/program.asp | official (already on card line 177) | IES NCER project database | Promote to primary_sources | HIGH |
| https://www2.ed.gov/policy/elsec/leg/essa/index.html | official | ESSA evidence tiers; cross-card CIC-02 educator dependency | Cross-reference (operator decides) | MEDIUM |
| https://ies.ed.gov/ncee/wwc/ | official | What Works Clearinghouse — ESSA evidence-tier authority | Cross-reference | MEDIUM |
| https://www.ahrq.gov/funding/grant-mgmt/index.html | official | AHRQ health-services research mechanism not anchored | New rubric_example | MEDIUM |
| https://www.nih.gov/research-training/funding-research-training-grants | official | NIH T-/F-/K- training-grant mechanism overview | Optional narrative_section_patterns addition for training-mechanism distinct from RPG | MEDIUM |
| https://orcid.org/ | community | ORCID — supports SciENcv biosketch population | Optional anchor | MEDIUM |
| https://datadryad.org/ + https://zenodo.org/ + https://osf.io/ + https://dataverse.org/ + https://www.icpsr.umich.edu/ | community | Named generalist + domain repositories per NIH 2023 DMSP | Optional anchors for evidence_weights.data_sharing_repository_named | HIGH |

### §3.3 Internet Archive snapshot verification

Recommended next Phase 4-CLC pass: verify Wayback Machine snapshots of every URL in `_research_metadata.primary_sources` (15 URLs). High priority: NSF PAPPG (annual update cycle), NIH DMSP overview (administration policy posture), NIH Public Access (executive-action volatility), USDA AFRI funding-opportunities page, USDA SARE grants page, IES funding page.

---

## §4. Proposed Card Improvements

Grouped by the eight runtime-behavior categories per master prompt §2. Each proposal: exact YAML path, why-it-improves-runtime, target-seat, where-it-belongs.

### §4.1 search_vocabulary / classification (CLC-side: underwriting_criteria + reviewer_profile_typical + common_red_flags)

- **`underwriting_criteria[NEW]` — add `community_engagement_rigor`.** description: "Where the proposal is participatory, community-engaged research (CBPR), or co-design / co-research with community partners — reviewers look for: community advisory board structure with named members and meeting cadence; co-PI / co-investigator structure where appropriate; equitable budget distribution to community partners (typical floor 15–25% to community partner sub-awards); partner co-authorship commitment in dissemination; training-and-capacity-building commitments to community partners; bidirectional benefit articulation. Empty 'we engaged the community' prose is a reviewer red flag." weight_in_typical_rubric: qualitative. **Seat affected:** Scribe + Judge + Logician. **Where:** card body.
- **`underwriting_criteria[REFINE]` — refine `method_fit`.** Extend rationale to enumerate field-experimental designs (randomized block, split-plot, latin-square) with replication-and-control discipline for USDA SARE / AFRI / NRCS / land-grant research. **Seat affected:** Scribe + Judge. **Where:** card body.
- **`scoring_weight_patterns[NEW]` — add NIH simplified review framework (3-factor)** as a parallel rubric_example. weights: factor_1_importance_of_research / factor_2_rigor_and_feasibility / factor_3_expertise_and_resources, each scored 1–9. note: "Active for most NIH FOAs effective Jan 2025; legacy 5-criteria framework still applies to some institute-specific FOAs — operator must read the active FOA." **Seat affected:** Scribe + Judge + Red Team. **Where:** card body.
- **`reviewer_profile_typical.reviewer_types[REFINE]` — add `nih_simplified_framework_reviewer`.** **Seat affected:** Scribe + Red Team. **Where:** card body.
- **`common_red_flags[NEW]` — add `participatory_research_partnership_without_substance`.** severity: HIGH. red_team_probe: "Where is the community advisory board roster? When does it meet? What is its decision-making authority over the research design? How is the budget allocated between academic team and community partner — and does the academic team retain >85% of direct costs? Is there a community-partner co-authorship commitment for dissemination? Or is the community partner relegated to 'recruitment / outreach' with no research-design authority?" **Seat affected:** Red Team + Logician. **Where:** card body.
- **`common_red_flags[NEW]` — add `field_trial_design_underspecified`.** severity: MEDIUM. red_team_probe: "Is the field trial design randomized-block, split-plot, latin-square, or none-stated? How many replications per treatment? How is location-by-treatment variance handled? Are control treatments included? How are weather-cycle confounders managed across growing seasons?" **Seat affected:** Red Team + Logician. **Where:** card body.
- **`common_red_flags[REFINE]` — refine `wrong_mechanism_choice` red_team_probe.** Add explicit IES goal-coded mechanism distinction (Exploration / Development / Impact / Measurement) and NIH F-/K-/T-/R- mechanism distinction. **Seat affected:** Red Team. **Where:** card body.

### §4.2 evidence capture / missing-evidence prompts (CLC-side: evidence_weights)

- **`evidence_weights[NEW]` — add `community_advisory_board_documentation`.** weight: MEDIUM, rises to HIGH for CBPR / IES Development & Impact / participatory grants. rationale: "Names + affiliations + meeting cadence + decision-making authority + IRB-approved consent if board is a research subject vs research partner. Reviewer red flag if board is named but not described, or described but has no decision authority." **Seat affected:** Scribe + Logician. **Where:** card body.
- **`evidence_weights[NEW]` — add `irb_pre_approval_or_pre_submission_consult`.** weight: MEDIUM. rationale: "For institutions with formal IRB processes, evidence that the team has consulted IRB pre-submission shortens post-award startup time. Names + institutional IRB contact + pre-consultation date." **Seat affected:** Scribe + Logician. **Where:** card body.
- **`evidence_weights[REFINE]` — refine `data_sharing_repository_named` rationale (line 192–195).** Enumerate Dataverse / Zenodo / Figshare / ICPSR / OSF / Data Dryad / domain-specific (GEO, dbGaP, ChEMBL) explicitly; require persistent-identifier commitment in narrative. **Seat affected:** Scribe + Logician. **Where:** card body.

### §4.3 KFR fact classes + scoring weight patterns + evidence_weights (CLC-side: provenance_requirements is the load-bearing field; absent on this card)

- **`provenance_requirements[NEW SECTION]` — add the field, currently absent.** Schema-optional under CLC schema; canonical item shape applies; item-level `not.anyOf` defense-in-depth enforced per §18 v1.1 RT-02 fold-in.
  - `irb_documentation`: required_citation_type: "IRB approval letter or pre-submission consultation note with institutional IRB contact + protocol number + approval date if approved." verbatim_quote_required: false.
  - `dms_plan_repository_named`: required_citation_type: "Named repository with persistent-identifier commitment; for non-generalist repositories, statement of why that repository is the right fit for the data type." verbatim_quote_required: false.
  - `data_management_plan_six_elements_addressed`: required_citation_type: "DMSP that addresses NIH 2023 six elements (data type / related tools / standards / preservation+access / reuse considerations / oversight). For NSF, the 2-page DMP addresses agency-specific elements per directorate." verbatim_quote_required: false.
  - `human_subjects_protections_documented`: required_citation_type: "PHS Human Subjects and Clinical Trials Information form completed; Subpart B / C / D protections where applicable; consent procedure with comprehension verification where literacy / language / capacity warrants; FERPA pathway for student educational records (IES / NSF education work)." verbatim_quote_required: false.
  - `commercialization_plan_for_sbir_sttr`: required_citation_type: "Commercialization Plan section per agency-specific SBIR/STTR template; addresses market opportunity + end-user + IP + financing + competition + Phase III pathway." verbatim_quote_required: false. **Note:** stays research-rigor-side per §1 thesis; Market Access track_a / track_b carries commercial-readiness scoring.
- **Seat affected:** Logician across all 5. **Where:** card body.

### §4.4 drafting register / admin-risk handling (Law 4 + OD-A v2.4)

- **OD-A v2.4 cross-flag check.** Per comment block at lines 677–691, 10 CLC-04 admin-risk terms were migrated to workspace `admin_risk_register.yaml` v2.4 (DEI in research / diverse perspectives / underrepresented populations / health equity / equity in research / decolonize methodology / community-based participatory research / two-spirit / Indigenous methodologies / intersectionality). Verified on disk via grep at `pipeline/institutional_memory/admin_risk_register.yaml:1069-1143` — 7 of 10 migrated under "CLC-04 research_evidence (7 new entries)." **Operator decision (§5 item 5):** the 3-term delta — were those 3 absorbed into existing pre-Wave-2 register entries (e.g., DEI / health equity already in v2.2)?
- **Workspace-register memory-namespace anchor in card header comment.** Card header comment block (lines 677–691) names CLC-04 sources but doesn't tell Scribe where to look at runtime. Per architecture v7.0.11 §1.9, the namespace pattern is `admin_risk:research_evidence:*`. **Recommend:** add a brief comment in card header pointing Scribe at the workspace register memory namespace for runtime substitution. Documentation-only — comments not in canonical bytes; no re-sign needed for header-comment edit (bundle with content edits to minimize ceremonies). **Seat affected:** Scribe. **Where:** card header comment.
- **NEW admin-risk vocabulary surface (research-side specifics).** Candidate terms not yet on workspace register:
  - `community-engaged research` — reviewer-context: GREEN at most reviewer audiences; preserve verbatim.
  - `marginalized communities` — reviewer-context: YELLOW at conservative federal review climates; substitutions: "low-income communities," "rural underserved communities," "historically underrepresented communities."
  - `social justice research` — reviewer-context: YELLOW for federal research panels; consider substitution to "research on social policy outcomes," "research on access to public services."
  - `broader impacts misframing` — NSF Broader Impacts can drift to activism-prose vs concrete-pathway prose; advisory, not substitution.
  - `Indigenous data sovereignty` — CARE Principles + OCAP — substantive research-rigor consideration tied to research with Indigenous communities; preserve verbatim if RFA invokes; flag for explicit IRB + data-sovereignty pathway documentation.
- **Route the 5 candidate terms to v2.x → v3.0 workspace-register scrub workflow per master prompt §7. No card-body change from this card alone.**

### §4.5 reviewer / rubric logic

- **`scoring_weight_patterns[REFINE]` — refine USDA SARE rubric_example.** Add per-region anchor URLs (Northeast SARE, North Central SARE, Southern SARE, Western SARE — each has a published grants page) and note per-program scoring per-call. **Seat affected:** Scout (forwarding to per-region fetch) + Scribe. **Where:** card body.
- **`scoring_weight_patterns[REFINE]` — refine USDA NIFA AFRI rubric_example.** Add `scout_runtime_fetch_required: true` field-level signal so Scout dispatches live fetch of the active-cycle RFA. **Seat affected:** Scout. **Where:** card body. **Note:** `additionalProperties: true` permissiveness on `scoring_weight_patterns[*]` per §18.5 allows this field shape without §18 v1.x amendment (operator may choose to graduate to schema-known optional; see §5 item 9).
- **`scoring_weight_patterns[NEW]` — add foundation-evaluation rubric_example.** weights: significance / theory_of_change / measurement_strategy / capacity_to_execute / dissemination. note: "Foundation evaluation grants emphasize theory-of-change clarity + measurement strategy + utility-of-findings-for-practice over inferential statistical rigor; mixed-methods and qualitative are typically welcomed where well-designed; the rubric is less standardized than federal — operator must read each foundation's published guidance." **Seat affected:** Scribe + Judge. **Where:** card body.
- **`scoring_weight_patterns[NEW]` — add AHRQ health-services research rubric_example.** AHRQ rubrics are NIH-derivative but health-services-specific (implementation science, dissemination science, patient-safety, comparative effectiveness). source_citation: `https://www.ahrq.gov/funding/grant-mgmt/index.html`. **Seat affected:** Scribe + Judge. **Where:** card body.

### §4.6 red-team probes (partially covered in §4.1)

- **`common_red_flags[NEW]` — add `repository_named_only_aspirationally`.** severity: MEDIUM. red_team_probe: "Does the DMSP / DMP name a specific repository with a persistent-identifier strategy and a timeline? Or does it say 'data will be deposited in an appropriate repository upon publication' without naming the repository? NIH 2023 DMSP and NSF DMP both expect named-repository commitment at proposal time." **Seat affected:** Red Team. **Where:** card body.
- **`common_red_flags[NEW]` — add `sbir_phase_iii_funding_pathway_unspecified`.** severity: MEDIUM (operator may rule MEDIUM_TO_HIGH; see §5 item 2). red_team_probe: "What is the named Phase III financing pathway? Private investment + LOI? Strategic partnership + MOU? Federal sole-source contract? Customer LOI + revenue projection? 'We will commercialize the technology' without a named pathway is a reviewer red flag." **Note:** commercial-readiness scoring lives on Market Access track_b (sbir_phase_iii); the research-rigor side of this question (technical-feasibility-supports-Phase-III-commercialization) belongs here. **Seat affected:** Red Team. **Where:** card body.

### §4.7 reporting / commitment extraction

- **`commitment_tracking_pattern.typical_commitments_extracted[NEW]` — add `community_engagement_milestones`.** measurement_method: "community advisory board meeting cadence + decision authority + community partner sub-award disbursement schedule + community-partner co-authorship status on dissemination products." **Seat affected:** Archivist + Report Generator (v0.2 horizon). **Where:** card body.
- **`commitment_tracking_pattern.typical_commitments_extracted[NEW]` — add `irb_continuing_review_schedule`.** measurement_method: "IRB approval date + continuing review schedule (annual default; less frequent for minimal-risk; institution-specific) + adverse event reporting trail." **Seat affected:** Archivist + Report Generator. **Where:** card body.
- **`reporting_requirements_typical.performance_reporting.content_required[NEW]` — add `dms_plan_compliance_status_per_element`.** Currently dms_plan_compliance is captured in commitment_tracking_pattern; reporting_requirements_typical also enumerates six-element NIH 2023 DMSP compliance reporting because RPPR is where it gets reviewed annually. **Seat affected:** Archivist + Report Generator. **Where:** card body.

### §4.8 memory namespace usefulness

Per architecture v7.0.11 §1.9: `cards:clc:research_evidence:*` is the namespace. Recommend standardized sub-keys (for v0.2 first-wave loader graduation):

- `cards:clc:research_evidence:underwriting_criteria` → underwriting_criteria
- `cards:clc:research_evidence:scoring_weight_patterns` → scoring_weight_patterns
- `cards:clc:research_evidence:evidence_weights` → evidence_weights
- `cards:clc:research_evidence:provenance_requirements` → provenance_requirements (proposed addition per §4.3)
- `cards:clc:research_evidence:common_application_forms` → common_application_forms
- `cards:clc:research_evidence:narrative_section_patterns` → narrative_section_patterns
- `cards:clc:research_evidence:reviewer_profile` → reviewer_profile_typical
- `cards:clc:research_evidence:common_portals` → common_portals
- `cards:clc:research_evidence:common_red_flags` → common_red_flags
- `cards:clc:research_evidence:reporting_requirements` → reporting_requirements_typical
- `cards:clc:research_evidence:compliance_obligations` → compliance_obligations
- `cards:clc:research_evidence:commitment_tracking_pattern` → commitment_tracking_pattern
- `cards:clc:research_evidence:budget_structure_conventions` → budget_structure_conventions
- `cards:clc:research_evidence:common_funders_observed` → common_funders_observed (subject to §5 item 1 Law-5 split decision)

**Seat affected:** all consuming seats. **Where:** architecture v7.0.11 §1.9 sets the namespace pattern; per-card sub-key map is a v0.2 first-wave loader concern. Surface as v0.2 loader-graduation enumeration.

### §4.9 Phase 4 fold-in discipline self-check (per master prompt rule 6 / §18.11 v1.1)

Each proposed change above scanned against the four refusals:

| Proposal | (a) structured-sub-field expansion on canonical entries? | (b) dedicated field-name fork? | (c) compound enum value? | (d) literal canonical CIC/CLC slug in non-exempt value position? |
|---|---|---|---|---|
| §4.1 underwriting_criteria add `community_engagement_rigor` | NO — adds new item at canonical shape | NO | NO | NO |
| §4.1 underwriting_criteria refine `method_fit` rationale | NO | NO | NO | NO |
| §4.1 scoring_weight_patterns add NIH simplified framework row | NO — new item, canonical shape | NO | NO | NO |
| §4.1 reviewer_profile_typical add `nih_simplified_framework_reviewer` | NO | NO | NO | NO |
| §4.1 common_red_flags add `participatory_research_partnership_without_substance` + `field_trial_design_underspecified` | NO | NO | NO | NO |
| §4.1 common_red_flags refine `wrong_mechanism_choice` probe | NO | NO | NO | NO |
| §4.2 evidence_weights add `community_advisory_board_documentation` + `irb_pre_approval_or_pre_submission_consult` | NO | NO | NO | NO |
| §4.2 evidence_weights refine `data_sharing_repository_named` rationale | NO — refines rationale within canonical item shape | NO | NO | NO |
| §4.3 provenance_requirements add 5 entries (field newly populated) | NO — provenance_requirements is schema-known optional; canonical item shape preserved per §18 v1.1 RT-02 fold-in not.anyOf defense | NO — filling-the-optional-field, not forking | NO | NO |
| §4.5 scoring_weight_patterns refine SARE + AFRI rubric_example with anchor URLs + `scout_runtime_fetch_required` field | NO — `additionalProperties: true` on rubric_example item permits the shape | NO | NO | NO |
| §4.5 scoring_weight_patterns add foundation_evaluation + AHRQ rubric_example | NO | NO | NO | NO |
| §4.6 common_red_flags add `repository_named_only_aspirationally` + `sbir_phase_iii_funding_pathway_unspecified` | NO | NO | NO — defaults to canonical MEDIUM per §5 item 2 disposition | NO |
| §4.7 commitment_tracking_pattern.typical_commitments_extracted add `community_engagement_milestones` + `irb_continuing_review_schedule` | NO | NO | NO | NO |
| §4.7 reporting_requirements_typical.performance_reporting.content_required add `dms_plan_compliance_status_per_element` | NO | NO | NO | NO |
| §4.8 memory namespace sub-keys | N/A — architecture decision, not card body | N/A | N/A | N/A |
| §4.4 OD-A workspace-register additions of 5 new admin-risk terms | NO — workspace-register-side, not card-body | NO | NO | NO |

**Verdict:** No proposed change trips any of the four Phase 4 fold-in refusals.

**Caveat on `MEDIUM_TO_HIGH` severity tier (pre-existing).** The card already uses this compound value at lines 483 (`no_preliminary_data_when_required`) and 492 (`broader_impacts_boilerplate_nsf`). Strictly speaking, refusal (c) targets compound enum values. The card's existing `MEDIUM_TO_HIGH` predates this dispatch (Wave 2 LOCKed); it's an inherited shape. **Surface to operator decision queue (§5 item 2):** admit `MEDIUM_TO_HIGH` to closed-set vocabulary, OR normalize both existing entries to MEDIUM with "rises to HIGH where X" rationale (mirroring the `evidence_weights.dissemination_plan` MEDIUM-baseline / functional-HIGH rationale pattern at lines 184–186). New entries in this patch plan default to canonical MEDIUM with rationale prose pending operator ruling.

---

## §5. Operator Decision Queue

Decisions that require Josh / operator approval before any patch dispatches:

1. **Law-5 split state for CLC cards (P0; cross-card; applies to all 8 CLC cards).** Per §2.3: the operator's v2.1 Law-5 reconciliation for `common_funders_observed` (engagement-attestation discipline + empty-at-top-level + `draft_funder_candidates_pending_operator_engagement_confirmation` under `_research_metadata`) is canonical for CIC cards. For CLC cards the master prompt is silent. CLC-side `common_funders_observed` reads as funder-grammar reference (NIH peer review as a rubric pattern), not as applicant-org-engagement reference. **Decision:** does Law-5 engagement-attestation discipline apply to CLC-side `common_funders_observed`? **Recommendation:** rule `NO` — CLC funders are pattern-reference, not org-relationship-reference; rule explicitly to lock the precedent for all 8 CLC cards.

2. **`MEDIUM_TO_HIGH` severity tier disposition (P1; cross-card).** The card already uses this compound value at lines 483 and 492. Per master prompt rule 6 (refusal (c)), compound enum values are forbidden. The card LOCKed at Wave 2 with the value present — operator may have implicitly approved or it slipped through. **Decision:** admit `MEDIUM_TO_HIGH` to closed-set severity vocabulary, OR normalize both existing entries (and prohibit future use). If the latter, both lines re-shape to canonical MEDIUM with rationale clause.

3. **NIH simplified review framework rubric_example (P1).** §4.1 proposes adding the 2025-effective 3-factor framework as a parallel rubric_example. **Decision:** add as new row, OR refine the existing NIH row to fold in simplified framework, OR table for v0.2 Wave 3 (when more NIH FOAs have migrated). Recommendation: add as new row — operator-decision-at-draft surfaces which framework applies per active FOA.

4. **Community engagement rigor as a new underwriting_criterion (P1).** §4.1 proposes adding as the 13th underwriting_criterion. **Decision:** add now, or surface as §18 v1.x amendment if considered a structured-sub-field expansion of `research_partner_letter`? Recommendation: add now — `underwriting_criteria` is an array-of-canonical-shape items per §18.5; adding a new item is the canonical add-pathway, not a sub-field expansion.

5. **OD-A v2.4 migration completeness for CLC-04 (P1).** The card's removal comment names 10 CLC-04 terms; workspace register's CLC-04 section names 7. **Decision:** are the 3 missing terms absorbed into pre-Wave-2 register entries? Operator confirmation routes either to no-action or backfill of the missing 3 to the workspace register.

6. **New admin-risk vocabulary candidates (P2; per §4.4).** Five new terms for the workspace register scrub workflow: `community-engaged research`, `marginalized communities`, `social justice research`, `broader impacts misframing` (advisory), `Indigenous data sovereignty`. Operator decides which graduate to v3.0 workspace register and which stay informal.

7. **Foundation-evaluation rubric_example (P2).** §4.5 proposes adding foundation-evaluation scoring as a separate rubric_example. **Decision:** add to card body, OR route to a separate foundation-evaluation Program Rule Pack? Recommendation: add to card body — the card carries funding grammar; specific foundation guidelines are Program Rule Pack territory but the *grammar* of foundation evaluation rubrics is card-body.

8. **AHRQ rubric_example (P2).** §4.5 proposes adding AHRQ as a research funder. **Decision:** add to card body — AHRQ is research_evidence-territory federal funder not currently anchored.

9. **`scoring_weight_patterns[*].scout_runtime_fetch_required` field shape (P2; cross-card).** §4.5 proposes adding a Scout-signaling field. **Decision:** encode in `pipeline/cards/_schema/card_clc.schema.json` as known optional (since useful across all 8 CLC cards), OR stay as `additionalProperties: true` per-card permissiveness?

10. **Workspace admin-risk-register runtime-lookup pointer in card header (P2; documentation-only).** §4.4 proposes naming the workspace register memory namespace (`admin_risk:research_evidence:*`) in card header so Scribe knows where to look at runtime. Comments not in canonical bytes; NO re-sign needed if isolated. Bundle with content edits.

11. **Re-signing ceremony budget for card body changes (P2).** Per operator reframe: aggressive content improvements OK; re-signing ceremony cost acceptable. The §4 proposals touch ~25 distinct card-body edits. **Decision:** bundle into single Phase 4-CLC-derived content refresh ceremony (CLC-04 supersession-re-sign modeled on OD-E row 277 / 278 precedent)?

---

## §6. Validation Checklist

| Check | Result | Evidence |
|---|---|---|
| Schema fields complete against current §18.5 / §18.6 schema | PASS | 15/15 required CLC fields present per `card_clc.schema.json:7-23`; lifecycle block satisfies allOf conditional (runtime_loadable=true → draft_status=signed AND signature_status=signed AND runtime_load_status=loaded; signed_at/signed_by/content_hash present) |
| No forbidden coupling field names (top-level + nested per item-level not.anyOf) | PASS | Grep across the file: none of 6 forbidden CLC-side names (`eligible_cic_subset`, `cic_allowlist`, `cic_denylist`, `preferred_cics`, `cic_win_rate`, `cic_ranking_preferences`) appear anywhere |
| No forbidden value-position regex matches outside exempt paths | PASS | Per §2.4 above — 0 non-exempt findings; all hits in `card_id` / `tilth_clc_id` / `_research_metadata` exempt subtree |
| No legacy-phrase `[Cc]ustomer [Ii]nformation` matches (defense-in-depth) | PASS | 0 hits |
| No private organization-specific data in card body | PASS | Funder references are funder-grammar reference; no client-specific data |
| No unsourced program-law claims | PASS at body | Verbatim quotes ≤2 sentences per OQ-4; statutory anchors are CFR / NIH / NSF / USDA NIFA / IES per OQ-3. Program-law (live deadlines, award amounts) is absent from operational fields; FY26 federal F&A rate volatility note at line 349 flags rate volatility without committing to a specific rate. |
| No excessive verbatim source text | PASS | Verbatim quotes ≤2 sentences per primary_source row per OQ-4 |
| Lifecycle status consistent with architecture v7.0.11 §1.5 production-load requirements | PASS | All five lifecycle gate fields at pass-state; runtime_loadable=true; content_hash present; signed_at + signed_by present |
| Single-track (oneOf branch 1 of §18.6 v2 schema) compliance | PASS | Card has no `track_a` / `track_b` containers — correctly single-track |
| For multi-track CLCs: shared root metadata + branch 2 compliance | N/A — single-track CLC |
| OD-A v2.4 admin_risk_term_register migration discipline | PASS-WITH-VERIFICATION | Comment block at lines 677–691 documents removal; workspace register has 7 CLC-04 entries; operator verification of migration completeness (10-vs-7 delta) routes to §5 item 5 |
| Coupling-discipline regression (LIVE regex + legacy-phrase defense-in-depth) | NONE | 0 non-exempt findings on either scan |

**Net coupling-discipline regression: 0 findings.**

---

## §7. Regression Tests

5 prompts that should demonstrate behavior change between pre-edit and post-edit cards.

### Test 1 — SBIR Phase II proposal (research-rigor vs commercial-readiness boundary)

**Prompt:** "We're a small ag-tech startup applying to USDA NIFA SBIR Phase II for a Phase I-demonstrated soil-microbiome diagnostic. We need help drafting the technical narrative and the commercialization plan."

**Pre-edit behavior:**
- Scout matches `SBIR Phase II` — routes to Research & Evidence AND Market Access track_a at runtime.
- Scribe draws on `narrative_section_patterns[Commercialization Plan]` (line 323) + `evidence_weights.commercialization_plan` (line 197) — currently mixes research-rigor scoring (TRL staging, IP, scientific feasibility) and commercial-readiness scoring (market opportunity, end-user, financing) in the same field-level prompts.
- Logician fires `human_subjects_irb` (if humans involved) + `data_management_plan` per standard SBIR research-side discipline.
- Reviewer-rubric routing is ambiguous — peer reviewers (technical SMEs) vs commercial reviewers (program officers) get the same draft.

**Post-edit behavior (with §4.1 + §4.3 + §4.6 additions):**
- Scout routes to Research & Evidence (research-rigor side) AND Market Access track_a (commercial-readiness side); explicit cross-CLC partition per new card-body cross-reference comment.
- Scribe drafts research-rigor narrative anchored here: scientific-feasibility tier, TRL staging, IP position, methods-fit, evaluation rigor, IRB plan, DMS plan. Commercial-readiness narrative (Market opportunity, end-user, financing, Phase III pathway) anchors to Market Access track_a; this card surfaces it as explicit handoff.
- `provenance_requirements.commercialization_plan_for_sbir_sttr` (NEW) fires — Scribe prompts for agency-specific Commercialization Plan template before drafting.
- `common_red_flags.sbir_phase_iii_funding_pathway_unspecified` (NEW) — Red Team probes whether Phase III financing pathway is named.

**Seat affected:** Scout + Scribe + Red Team + Logician. **Pass criterion:** Cross-CLC reference present; Phase III funding pathway probed; agency-specific Commercialization Plan template surfaced.

### Test 2 — Participatory CBPR research proposal

**Prompt:** "We're an academic-community research partnership applying to NIH R01 for community-based participatory research on food-access intervention in West Philadelphia. The community partner is a 25-year-old neighborhood health council."

**Pre-edit behavior:**
- Scout matches `community-based participatory research` (CBPR) + `R01` — routes to Research & Evidence.
- Scribe draws on `evidence_weights.research_partner_letter` (line 174–177) — names CBPR as HIGH-weight context but doesn't surface concrete community-partnership-rigor evidence prompts (budget distribution, decision authority, co-authorship).
- Logician fires standard human-subjects-IRB discipline but no community-engagement-specific provenance.
- Red Team doesn't have a `participatory_research_partnership_without_substance` probe.

**Post-edit behavior (with §4.1 + §4.2 + §4.3 additions):**
- `underwriting_criteria.community_engagement_rigor` (NEW) fires — Scribe drafts community advisory board structure + budget distribution + co-authorship commitments as structured section.
- `evidence_weights.community_advisory_board_documentation` (NEW) fires — Scribe prompts for: roster of board members + affiliations + meeting cadence + decision authority over research design + IRB-approved consent if board members are research subjects.
- `provenance_requirements.community_advisory_board_documentation` would fire if added.
- Red Team probes `participatory_research_partnership_without_substance`: budget allocation between academic and community; co-authorship commitment; decision authority.

**Seat affected:** Scribe + Logician + Red Team. **Pass criterion:** Community-engagement-rigor section drafted with named board structure + budget distribution + co-authorship; Red Team probe fires.

### Test 3 — Evaluation proposal (foundation, not federal)

**Prompt:** "We're applying to RWJF for a 3-year evaluation grant on a state-level Medicaid food-as-medicine pilot. We need help framing the theory of change, measurement strategy, and dissemination."

**Pre-edit behavior:**
- Scout matches `evaluation grant` + `foundation funder` + `theory of change` — routes to Research & Evidence.
- Scribe falls through `scoring_weight_patterns` to NIH / NSF / AFRI / SARE / IES rubric_examples; no foundation-evaluation rubric_example.
- Scribe defaults to federal-evaluation-research drafting register; misses foundation-evaluation emphasis on theory-of-change + measurement strategy + utility-of-findings.
- Logician fires `evaluation_rigor` underwriting_criterion + `dissemination_plan` — fine, but no foundation-specific anchor.

**Post-edit behavior (with §4.5 NEW foundation-evaluation rubric_example):**
- Scribe routes to new `foundation_evaluation` rubric_example — drafts with theory_of_change clarity + measurement_strategy + capacity_to_execute + dissemination.
- Mixed-methods and qualitative designs framed as RWJF-accepted.
- Foundation-aware draft, not federal-research-method default.

**Seat affected:** Scribe + Judge. **Pass criterion:** Foundation-evaluation rubric drives draft; mixed-methods framed appropriately.

### Test 4 — NIH 2023 DMSP repository-named discipline

**Prompt:** "We're applying to NIH for a 5-year R01 on diabetes-prevention behavioral intervention. The data will include survey responses, biomarkers, and de-identified EHR data."

**Pre-edit behavior:**
- Scout matches `R01` + NIH — routes to Research & Evidence.
- Scribe drafts DMS Plan addressing six elements per evidence_weights.data_management_plan rationale (line 166–167).
- Logician fires evidence_weights.data_management_plan but no specific provenance check.
- Red Team probes `missing_or_weak_data_management_plan` (line 462–464) — but generic.

**Post-edit behavior (with §4.3 NEW provenance_requirements + §4.6 NEW red_team_probe):**
- `provenance_requirements.dms_plan_repository_named` (NEW) fires — Logician requires named repository (Dataverse, Zenodo, Figshare, ICPSR, OSF) with persistent-identifier strategy.
- `provenance_requirements.data_management_plan_six_elements_addressed` (NEW) fires — Logician requires DMSP addresses all six NIH 2023 elements.
- `common_red_flags.repository_named_only_aspirationally` (NEW) — Red Team probes whether repository is named with persistent-identifier + timeline.
- DMSP-prep enforced at structural level; no "data available upon request" boilerplate slips through.

**Seat affected:** Scribe + Logician + Red Team. **Pass criterion:** DMSP names specific repository; six elements addressed.

### Test 5 — USDA AFRI per-RFA scout-runtime-fetch

**Prompt:** "We're applying to USDA AFRI Foundational and Applied Science FY26 for plant-health-and-production. We need to know the scoring criteria for the active cycle."

**Pre-edit behavior:**
- Scout matches `AFRI` + `Foundational and Applied Science` — routes to Research & Evidence.
- Scribe draws on `scoring_weight_patterns[USDA NIFA AFRI peer review]` (line 115–119) — text says "per_rfa_scoring_dimensions: qualitative_per_program_area" + "Operator must read the active-cycle RFA."
- Scribe drafts generically against AFRI six priority areas without active-cycle anchoring.

**Post-edit behavior (with §4.5 NEW `scout_runtime_fetch_required` field):**
- Scout sees `scout_runtime_fetch_required: true` on AFRI rubric_example row.
- Scout dispatches live fetch of active FY26 AFRI plant-health-and-production RFA from `https://www.nifa.usda.gov/grants/funding-opportunities/agriculture-food-research-initiative-foundational-applied-science`.
- Scout surfaces active-cycle scoring dimensions as runtime data; Scribe drafts against them.

**Seat affected:** Scout + Scribe. **Pass criterion:** Scout dispatches live fetch; Scribe drafts against fetched active-cycle scoring criteria.

---

## §8. Patch Plan

Edits proposed in this handback grouped by file path. **No edits applied from this dispatch.** Operator dispatches each ceremony separately per the OD-C / OD-E precedent.

### File: `pipeline/cards/CLC/research_evidence.yaml`

**Ceremony shape:** supersession-re-sign per OD-E precedent (row 277 / 278 model). Parent_lock_row = 257 (Wave 2 LOCK). Ceremony_parent_row = `<NEXT-AVAILABLE-COMPOUND-PARENT>` if bundled with Phase 4-CLC content ceremonies; `<NEXT-AVAILABLE>` standalone.

**Edit set:**

1. `underwriting_criteria[NEW]` — add `community_engagement_rigor` (§4.1).
2. `underwriting_criteria[REFINE]` — refine `method_fit` rationale to include field-experimental designs (§4.1).
3. `scoring_weight_patterns[NEW]` — add NIH simplified review framework 3-factor rubric_example (§4.1).
4. `scoring_weight_patterns[REFINE]` — refine USDA SARE rubric_example with per-region anchor URLs (§4.5).
5. `scoring_weight_patterns[REFINE]` — refine USDA NIFA AFRI rubric_example with `scout_runtime_fetch_required: true` (§4.5).
6. `scoring_weight_patterns[NEW]` — add foundation-evaluation rubric_example (§4.5).
7. `scoring_weight_patterns[NEW]` — add AHRQ health-services research rubric_example (§4.5).
8. `reviewer_profile_typical.reviewer_types[REFINE]` — add `nih_simplified_framework_reviewer` (§4.1).
9. `evidence_weights[NEW]` — add `community_advisory_board_documentation` (§4.2).
10. `evidence_weights[NEW]` — add `irb_pre_approval_or_pre_submission_consult` (§4.2).
11. `evidence_weights[REFINE]` — refine `data_sharing_repository_named` rationale to enumerate named repositories (§4.2).
12. `provenance_requirements[NEW SECTION]` — add the entire `provenance_requirements` field (currently absent per schema-optional). 5 entries: `irb_documentation`, `dms_plan_repository_named`, `data_management_plan_six_elements_addressed`, `human_subjects_protections_documented`, `commercialization_plan_for_sbir_sttr` (§4.3).
13. `common_red_flags[NEW]` — add `participatory_research_partnership_without_substance` (§4.1).
14. `common_red_flags[NEW]` — add `field_trial_design_underspecified` (§4.1).
15. `common_red_flags[NEW]` — add `repository_named_only_aspirationally` (§4.6).
16. `common_red_flags[NEW]` — add `sbir_phase_iii_funding_pathway_unspecified` (§4.6).
17. `common_red_flags[REFINE]` — refine `wrong_mechanism_choice` red_team_probe to enumerate IES goal-coded + NIH mechanism distinction (§4.1).
18. `commitment_tracking_pattern.typical_commitments_extracted[NEW]` — add `community_engagement_milestones` (§4.7).
19. `commitment_tracking_pattern.typical_commitments_extracted[NEW]` — add `irb_continuing_review_schedule` (§4.7).
20. `reporting_requirements_typical.performance_reporting.content_required[NEW]` — add `dms_plan_compliance_status_per_element` (§4.7).
21. Cross-CLC reference comment block — add brief comment in card body (e.g., near `narrative_section_patterns[Commercialization Plan]`) referring Scribe to Market Access track_a (sbir_phase_ii) and track_b (sbir_phase_iii) for commercial-readiness scoring partition. **Use display name "Market Access" — NOT slug** per master prompt rule 3.
22. Card header comment normalization — add reference to workspace admin_risk_register memory namespace (`admin_risk:research_evidence:*`) for Scribe runtime substitution lookup (§4.4). Documentation-only — comments not in canonical bytes; bundling with re-sign ceremony recommended.

**Edits NOT applied from this dispatch (deferred to other ceremonies):**

- OD-A workspace-register additions of 5 new admin-risk terms (§4.4). Route to v2.x → v3.0 workspace-register scrub workflow per master prompt §7.
- Operator-confirmed migration completeness check for 10-vs-7 CLC-04 admin-risk delta (§5 item 5).
- `MEDIUM_TO_HIGH` severity vocabulary disposition (§5 item 2; cross-card).
- Law-5 split state for CLC cards (§5 item 1; cross-card; applies to all 8 CLC cards' `common_funders_observed`).

### File: `pipeline/cards/_schema/card_clc.schema.json`

**Ceremony shape:** part of cards-ceremony compound LOCK if `scout_runtime_fetch_required` is graduated to schema-known optional field (§5 item 9).

**Edit set:**

23. (Optional per §5 item 9) Add `scout_runtime_fetch_required: boolean` to `scoring_weight_patterns[*]` item schema if operator graduates from `additionalProperties: true` permissiveness.

### File: `pipeline/institutional_memory/admin_risk_register.yaml`

**Ceremony shape:** workspace-register update (OD-A v2.4 → v3.0 scrub workflow per master prompt §7).

**Edit set:**

24. Surface 5 new admin-risk terms (per §4.4) as v3.0-schema candidates: `community-engaged research`, `marginalized communities`, `social justice research`, `broader impacts misframing`, `Indigenous data sovereignty`. **No card-body change from this card alone.**
25. Operator-confirm migration completeness for 10-vs-7 CLC-04 admin-risk delta. Backfill if needed.

### File: `pipeline/cards/CLC/market_access.yaml` (cross-card; out of scope for this dispatch)

Per the §1 thesis and §4.7 commercialization-partition: when CLC-04 adds the cross-CLC reference comment, the symmetric reference on Market Access pointing back to Research & Evidence is a parallel edit. **Out of scope for this handback; surface to Phase 4-CLC supervisor for the Market Access cross-reference symmetry.**

---

**OD-D Phase 4 forward-binding contract note (per master prompt rule 6 + §18.11 v1.1):**

- No proposal touches refusal (c) compound enum values — all new severity tags use canonical HIGH / MEDIUM / LOW. The card's pre-existing `MEDIUM_TO_HIGH` shape on lines 483 and 492 is inherited from Wave 2 LOCK; new entries default to MEDIUM with rationale prose until operator rules on §5 item 2.
- No proposal touches refusal (d) literal canonical CIC/CLC slug in non-exempt value position. Edit 21 (cross-CLC reference) uses display name "Market Access" per master prompt rule 3.
- No proposal touches refusal (a) structured-sub-field expansion on canonical entries — additions are at canonical item-shape boundaries.
- No proposal touches refusal (b) dedicated field-name fork — `provenance_requirements` is schema-known optional; its absence at LOCK was a permissive choice; adding it is filling-the-optional-field, not forking.

Per Run 1 P1-1 / L1-F3 — the F-CARDS-COUPLING-VIOLATION-EXTENSION gate body is currently `NotImplementedError` at runtime. The value-position-scan that should catch refusal (d) regressions is not LIVE today. The compensating control is `loader.py.enforce_no_forbidden_coupling` (field-name layer only). This patch plan is value-position clean as verified by manual scan; recommend the gate-body graduation per Run 1 Patch C1 happen in parallel with or before the cards-ceremony to harden runtime defense.

---

**Summary block:**

```
Card: CLC:research_evidence
Card file: pipeline/cards/CLC/research_evidence.yaml
Research hours actual: 1.6
Findings: 23 total — 1 P0, 9 P1, 13 P2
Decision queue: 11 operator approvals required
Conflicts with prior art: NONE (OD-A workspace-register migration intact pending operator verification of 10-vs-7 CLC-04 delta; all new admin-risk-term candidates align with v2.4 severity-tier scheme)
Coupling-discipline regression: NONE
Lifecycle gap surfaced: draft_status reads "signed" on disk; no normalization required per Run 1 P0-3
Review readiness: READY (content improvements bundle to Phase 4-CLC-derived re-sign ceremony; Law-5 split decision for CLC cards is the only P0 and applies cross-card to all 8 CLC cards, not blocking on this card alone)
```
