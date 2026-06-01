# Tilth CIC/CLC Unified Per-Card Research Plan (6 CIC + 8 CLC)

Prepared: 2026-05-17
Workspace: `/Users/goldenquill/Downloads/GoldenQuill/`
Authority: Synthesis of operator working artifact §Research Plans By Card + Cowork canonical card content + today's OD-A / OD-C / OD-D / OD-E ceremony LOCKs (lock_history rows 250–279).

## §0 — How to use this document

This document is dispatched alongside the unified master prompt (`docs/cic_clc_unified_master_prompt_2026-05-17.md`). For each card, the master prompt is the spine; the per-card plan below is the **research-angle annotation** that situates the master prompt against (a) the operator's per-card priority targets and (b) the Cowork canonical state from today's ceremonies.

Each per-card section carries:
- **Operator impact target** — the operator's one-sentence framing of what the card should cause Tilth to do differently.
- **Cowork canonical annotations** — pointers into §18 main + amendments + lock_history + OD-* completions that the per-card researcher must read before research.
- **Priority research vectors** — the operator's list, refined where the canonical state changes the framing.
- **Acceptance tests** — the operator's tests, plus Cowork-side additions where the LIVE F-CARDS-* gates or OD-E multi-track shape add a new acceptance requirement.

The 14 cards are addressed in the canonical order (CIC-01..CIC-06; CLC-01..CLC-08). Card slugs and IDs match the LIVE §18.2 / §18.3 rosters.

## §1 — Customer Identity Cards (CIC) — 6 cards

### §1.1 TILTH-CIC-01 `food_systems`

**Operator impact target.** Make Tilth understand farms, producers, food hubs, value-added processors, local food systems, conservation practice, and farm-to-school work as operating realities with seasonality, production proof, buyer proof, and safety/compliance constraints.

**Cowork canonical annotations.**
- Card file: `pipeline/cards/CIC/food_systems.yaml` (Wave 1 LOCKED 2026-05-15 row 226; §18 v1.1 schema-refinement-conformed; v1.2 dialect_routing_table re-keyed at v7.0.12 LOCK).
- §18.9 (per-CIC starter content requirements) — the `food_systems` paragraph enumerates: search terms, program keywords, evidence signals, KFR classes, register defaults, admin-risk terms, risk entries. Treat as the canonical content roster; recommend additions and refinements against it, not from scratch.
- §18 v1.1 narrow-corrective precedent — `food_systems.yaml` is the Wave 1 reference card; the schema item-shape extensions (`frequency_observed`, `dialect_routing_table.items.required`, `provenance_requirements.additionalProperties`) all originated from this card.
- §18 v1.2 — `dialect_routing_table` items now key on `clc` + `dialect` + `register_description` + optional `example_program`. Confirm the card carries the v1.2 shape post-LOCK.
- OD-A admin_risk_register v2.4 — `food_systems` is a CIC, so its admin-risk terms (`food sovereignty`, `land back`, `climate justice`, `decolonize`, `anti-capitalist`) stay CIC-side (workspace register is currently CLC-axis-keyed). If a Wave 2-style cross-CIC consolidation is dispatched later, route here.

**Priority research vectors (refined).**
- Verify current USDA VAPG, AMS LAMP, SCBGP, RFSP, LFPP, FMPP, NRCS EQIP/CSP, SARE, AFRI, BFRDP, RCDG, REAP, PA Ag Innovation source details. Confirm 2026 cycle dates moved to Program Rule Packs (not the card body).
- Review recent awarded abstracts/descriptions from USDA, state agriculture departments, and regional foundations. Separate producer-side evidence from intermediary/education evidence.
- Strengthen missing-evidence prompts for sales ledgers, buyer LOIs, production records, crop plans, food safety certifications, equipment quotes, match, and conservation practice documentation.
- Cowork addition: per OD-C row 272 value-position regex coverage, scan the card body for any literal `TILTH-CLC-NN` slug references introduced post-Wave-1 (none expected, but defense-in-depth scan); use display names if cross-CLC reference is needed.
- Cowork addition: confirm `dialect_routing_table` entries reference valid CLC slugs from the canonical 8-slug set, not the retired political axis.

**Acceptance tests.**
- Freeze dryer / equipment request triggers production capacity + buyer demand + value-added workflow + quote evidence.
- Regenerative agriculture claim triggers source-backed practice evidence rather than vague impact prose.
- Farm-to-school project routes education/food-system evidence without forcing a CLC pairing (orthogonality).
- Cowork addition: a Scout dispatch on an SBIR Phase II ag opportunity routes to CLC-05 `track_a` (sbir_phase_ii), not the legacy single-track shape — verifies the §18.6 v2 multi-track awareness propagates through to a CIC card's funder-program-keyword routing.

### §1.2 TILTH-CIC-02 `educator`

**Operator impact target.** Make Tilth treat education applicants as compliance-dense learning institutions where dosage, authorization, student privacy, evidence of learning, and safeguarding matter as much as mission language.

**Cowork canonical annotations.**
- Card file: `pipeline/cards/CIC/educator.yaml` (Wave 2 LOCKED 2026-05-16 row 252 or 253 — confirm against lock_history rows 252–261).
- A companion `pipeline/cards/CIC/educator_amendment_proposal_2026-05-16.md` exists on disk; read it for Wave 2 close-synthesis decisions deferred to amendment.
- §18.9 `educator` paragraph: search terms (schools, afterschool, youth development, tutoring, mentoring, workforce readiness, CTE, college readiness, STEM/STEAM, social-emotional learning, family engagement, evidence-based intervention).
- §18 v1.1 RT-02 fold-in: provenance_requirements item-level not.anyOf defense-in-depth applies — confirm.

**Priority research vectors (refined).**
- Verify Department of Education Title I, 21st CCLC, EIR, GEAR UP, TRIO, CSP, FERPA, PPRA, COPPA, IDEA, ESSA, IES/WWC, NSF STEM, YouthBuild, Farm to School references.
- Add or refine source distinctions for K-12, higher education, afterschool, workforce, tutoring, mentoring, STEM/STEAM, SEL, family engagement.
- Refresh federal admin-risk context for DEI, gender identity, trauma-informed, restorative justice, culturally responsive, equity language. Surface for operator approval; do not auto-rewrite.
- Confirm whether CIPA, Section 504, McKinney-Vento, Title IX, state school-code entries belong in base card or state overlays (OD-G coordination if active).
- Cowork addition: review `educator_amendment_proposal_2026-05-16.md` for any Wave-2-deferred schema refinements; align research recommendations with the proposed amendment direction.

**Acceptance tests.**
- Tutoring proposal asks for grade band, dosage, baseline, assessment measure, staff credentials, partner authorization, privacy protocol.
- Youth workforce program distinguishes training outcomes from educational achievement claims.
- Student testimonial/photo request triggers consent/privacy warnings.
- Cowork addition: a draft mentioning "evidence-based intervention" routes Logician to enforce IES What Works Clearinghouse + ESSA evidence tier provenance — surfaces as missing-evidence prompt if the draft lacks the citation.

### §1.3 TILTH-CIC-03 `public_agency`

**Operator impact target.** Make Tilth read public-sector applicants through authority, public benefit, procurement, site control, match, engineering readiness, environmental review, public accountability, audit exposure.

**Cowork canonical annotations.**
- Card file: `pipeline/cards/CIC/public_agency.yaml` (Wave 2 LOCKED 2026-05-16 — confirm row).
- §18.9 `public_agency` paragraph: enumerates the seven evidence categories (board resolutions, capital plans, engineering estimates, etc.).
- The card carries `environmental_review_status` evidence + KFR fact-class + provenance_requirements (verified via grep at lines 316, 378, 425, 1145).

**Priority research vectors (refined).**
- Verify HUD CDBG, USDA Community Facilities, USDA WEP, EPA CWSRF/DWSRF, Brownfields, FEMA BRIC/Public Assistance, DOT RAISE/SS4A, EDA Public Works, BEAD, 2 CFR 200, NEPA, Davis-Bacon, BABA, state programs.
- Strengthen distinctions: municipality / borough / authority / school district (LEA) / county / tribal government / special district.
- Verify public-meeting, board-resolution, capital-plan, procurement-policy, environmental-review evidence patterns.
- Decide which PA examples stay in base card vs OD-G state overlay.
- Cowork addition: `environmental_review_status` is a KFR fact-class with `verbatim_quote_required: true` per provenance discipline; confirm the source citation (HUD CDBG Responsible Entity Environmental Review, 24 CFR Part 58) is still current.

**Acceptance tests.**
- Municipal stormwater project asks for service area, authorizing resolution, engineering estimate, match, site control, environmental review.
- Public safety request doesn't drift into political language; asks for public benefit + statutory authority.
- Construction proposal surfaces procurement, Davis-Bacon, BABA, NEPA conditions where applicable.

### §1.4 TILTH-CIC-04 `arts_culture`

**Operator impact target.** Preserve artistic voice while translating cultural, civic, accessibility, preservation, humanities, audience, production value into funder-legible evidence.

**Cowork canonical annotations.**
- Card file: `pipeline/cards/CIC/arts_culture.yaml` (Wave 2 LOCKED 2026-05-16 — confirm row).
- §18.9 `arts_culture` paragraph: enumerates the evidence + admin-risk terms (radical, decolonial, liberation, queer, trans, racial justice, censorship, occupation).
- §18 v1.2 LOCK retired the four-axis political enum; arts_culture historically had the deepest dialect-routing-table dependency on the political axis — confirm the v1.2 re-keying handled the cultural-register routing without flattening voice.

**Priority research vectors (refined).**
- Verify NEA, NEH, IMLS, state arts councils, humanities councils, Mellon, Doris Duke, Ford, Knight, Surdna, Heinz, Native Arts and Cultures, First Peoples Fund, W.A.G.E., accessibility/equal-opportunity sources.
- Separate performing arts, visual arts, public art, humanities, preservation, festivals, cultural heritage, creative placemaking/placekeeping, community arts.
- Strengthen evidence prompts for work samples, venue agreements, rights/permissions, production budget, artist fees, accessibility plan, audience data, documentation, press.
- Tighten admin-risk handling: terms like radical, decolonial, liberation, queer, trans, racial justice, censorship, occupation are NOT flattened or silently rewritten — surface flagged terms with severity + reviewer context + substitution candidates + approval required.
- Cowork addition: per §18 v1.2 retirement of `funder_political_axis`, confirm dialect routing now keys on CLC slug + register_description. The "soul_fire" axis value retired; map prior soul_fire-routed entries to appropriate CLC slugs (`catalytic_change` for systems-change framing; `public_purpose_works` for civic-formal framing; `sponsorship_corporate` for brand/audience framing).

**Acceptance tests.**
- Festival request asks for venue, date confirmation, audience history, artist fee budget, permits, accessibility, documentation.
- Public art project distinguishes public benefit from artist statement.
- Cultural heritage proposal preserves specificity while checking rights, permissions, community authority.
- Cowork addition: a draft using "decolonial" + "queer" within the same paragraph triggers Scribe to surface BOTH admin-risk flags + their per-funder substitution candidates; operator approval queue surfaces before Scribe finalizes.

### §1.5 TILTH-CIC-05 `cooperative`

**Operator impact target.** Make Tilth understand member-governed ownership as a governance, capitalization, patronage, democratic-control, shared-benefit, and financial-controls problem — not just a values statement.

**Cowork canonical annotations.**
- Card file: `pipeline/cards/CIC/cooperative.yaml` (Wave 2 LOCKED 2026-05-16 — confirm row).
- §18.9 `cooperative` paragraph: enumerates the seven evidence categories (bylaws, articles, member roster, governance minutes, patronage model, capitalization plan, shared asset plan).
- This is one of the 6-of-8 Wave 2 cards that surfaced the Cycle 2 NEW-defect-from-Cycle-1-fold pattern that drove OD-D §18.11 v1.1. The Cycle 2 fix-in-place precedent for this card is the on-disk reference for fold-in discipline.
- L-024 lesson connection: cooperative + shared_assets often co-fund (e.g., a worker cooperative's shared-use kitchen requires both CIC-05 + CIC-06 framing + CLC-08 shared_assets underwriting). Orthogonality holds; the runtime composition is the operator's runtime decision, not a card-body coupling.

**Priority research vectors (refined).**
- Verify USDA RCDG, SDGG, VAPG cooperative categories, DOL Employee Ownership Initiative, Subchapter T, ESOP/ERISA boundaries, Main Street Employee Ownership Act, ICA cooperative principles, USFWC, DAWI, cooperative CDFIs, state cooperative statutes.
- Decide whether ESOPs, platform co-ops, LLC-with-cooperative-bylaws, and true statutory cooperatives belong in one CIC or need subtypes later. Do NOT propose subtypes from a research session; route as a v0.2 Wave 3 schema-shape question.
- Strengthen evidence prompts for bylaws, member roster, voting rights, board minutes, patronage model, capitalization plan, member commitments, shared assets, controls.
- Keep common funders operator-confirmed only; candidate funders stay metadata/pending confirmation (frequency_observed: UNKNOWN until confirmed).
- Cowork addition: admin-risk terms `anti-capitalist`, `solidarity economy`, `mutual aid`, `commons`, `worker control`, `collectivize`, `abolition`, `wealth redistribution` — confirm the substitution candidates (shared ownership, democratic enterprise, pooled infrastructure, community wealth-building) are still operator-approved post-Wave-2.

**Acceptance tests.**
- Worker-owner conversion request asks for legal pathway, ownership transition, valuation, financing, governance, member training, controls.
- Producer cooperative equipment request asks for member commitments and shared-asset access rules.
- Mutual aid language translated only with operator approval and funder context.

### §1.6 TILTH-CIC-06 `ecosystem_intermediary`

**Operator impact target.** Make Tilth treat intermediaries, technical assistance providers, backbone organizations, implementation partners, regenerative systems suppliers as proof-of-adoption and end-user-benefit organizations — not vendors pitching themselves.

**Cowork canonical annotations.**
- Card file: `pipeline/cards/CIC/ecosystem_intermediary.yaml` (Wave 2 LOCKED 2026-05-16 — confirm row).
- §18.2 `display_name` carries the slash form "Ecosystem Intermediary / Regenerative Systems Supplier"; `display_name_short` = "Ecosystem Intermediary" per §18 main §18.2 / architecture v7.0.11 §7.2 LOCKED.
- §18.9 `ecosystem_intermediary` paragraph: deepest TRL-aware content set; the operator flagged "Decide how deep TRL should go in base card versus tech-subtype overlay."

**Priority research vectors (refined).**
- Verify USDA RBDG, RCDG, Regional Food Business Centers, EDA Build to Scale, EDA Tech Hubs, SBIR FAST, NSF Convergence Accelerator, NSF I-Corps, NIST MEP, DOL apprenticeship grants, IES Comprehensive Centers, SBA Microloan intermediaries, collective impact, fiscal sponsorship, TRL sources.
- Decide how deep TRL should go in base card vs tech-subtype overlay. Recommend a v0.2 Wave 3 schema-shape question for tech-subtype if depth exceeds base-card scope.
- Strengthen proof for customer letters, partner commitments, deployment history, case studies, training curriculum, support model, pricing model, implementation plan, downstream outcomes.
- Check language around AI, automation, platform, surveillance, vendor subsidy, proprietary lock-in, workforce replacement. Surface admin-risk terms for operator approval.
- Cowork addition: confirm `display_name_short` field is populated correctly and `display_name` carries the slash form unchanged.

**Acceptance tests.**
- Supplier grant request asks for customer demand, deployment proof, user benefit, support burden, data governance, maintenance plan.
- TA provider request asks for service model, curriculum, credentials, partner network, adoption outcomes.
- AI-enabled project avoids hype and surfaces data/control boundaries.

## §2 — Capital Logic Cards (CLC) — 8 cards

### §2.1 TILTH-CLC-01 `public_purpose_works`

**Operator impact target.** Make Judge / Logician evaluate public-purpose money through eligibility, statutory authority, public benefit, readiness, procurement, site control, match, maintenance, environmental review, audit readiness.

**Cowork canonical annotations.**
- Card file: `pipeline/cards/CLC/public_purpose_works.yaml` (Wave 2 LOCKED 2026-05-16 row 252 — confirm).
- §18.10 `public_purpose_works` paragraph: underwriting criteria + program terms + evidence weights + narrative sections + reviewer profile + red flags + post-award commitments.
- Single-track (oneOf branch 1 of §18.6 v2 schema). No track restructuring.
- OD-A admin_risk_register v2.4: public_purpose_works contributed 4 entries to the workspace migration — minimal admin-risk surface compared to catalytic_change (13) / credit_underwriting (15).

**Priority research vectors (refined).**
- Verify HUD CDBG, USDA Community Facilities, FEMA BRIC/BCA, EPA SRFs, DOT RAISE/SS4A, EDA Public Works, 2 CFR 200 procurement/closeout/single audit, Davis-Bacon, BABA, NEPA, Section 106, PA DCED, PENNVEST.
- Move program-specific amounts/deadlines/rules to Program Rule Packs where needed.
- Strengthen narrative section patterns for public benefit, readiness, procurement, environmental review, operations, maintenance, timeline.
- Add red-team probes for public controversy, preliminary engineering, match weakness, maintenance ambiguity.

**Acceptance tests.**
- Water infrastructure proposal asks for engineering stage, service area, environmental review, SRF/USDA path, match, ratepayer/beneficiary logic.
- Park/facility proposal asks for site control, public access, maintenance, procurement, ADA.

### §2.2 TILTH-CLC-02 `catalytic_change`

**Operator impact target.** Distinguish real catalytic funding from buzzword-heavy transformation language by requiring a leverage point, theory of change, learning agenda, partnership roles, replication path, timing, follow-on capital logic.

**Cowork canonical annotations.**
- Card file: `pipeline/cards/CLC/catalytic_change.yaml` (Wave 2 LOCKED 2026-05-16 — confirm row).
- §18.10 `catalytic_change` paragraph: underwriting criteria + program terms + evidence weights + narrative sections + reviewer profile + red flags + post-award commitments.
- Single-track.
- OD-A v2.4: catalytic_change contributed 13 entries to the workspace admin_risk_register migration — joint-highest with credit_underwriting; the cross-CLC vocabulary overlap with operating_capacity is the operator-flagged normalization target.

**Priority research vectors (refined).**
- Verify MacArthur 100&Change, Ford BUILD, NSF Convergence Accelerator, ARPA-E, IES evidence tiers, USDA AFRI, EDA Build to Scale, Rockefeller catalytic capital, Skoll, Kresge LIFT, FSG systems-change framework, Hewlett, 2 CFR 200, FCOI sources.
- Separate foundation systems-change logic from federal innovation-stage-gate logic.
- Add stronger tests for role-less partnerships, vague innovation, absent leverage point, no learning agenda, no replication path.
- Normalize shared admin-risk terms with CLC-03 and workspace admin-risk register (per OD-A v2.4 migration pattern).
- Cowork addition: catalytic_change is a high-volume intersection target per §18.19.2 (food_systems × catalytic_change is one of the three highest-volume intersection cells); regression-test coverage proposals should prioritize this intersection.

**Acceptance tests.**
- "Transform food systems" prompt demands a system map, leverage point, pilot design, partner roles, learning outputs.
- Innovation ask is rejected or downgraded if novelty is unsupported or evidence path is missing.

### §2.3 TILTH-CLC-03 `operating_capacity`

**Operator impact target.** Evaluate capacity funding as bottleneck removal with durable operational gains — not generic operating support language.

**Cowork canonical annotations.**
- Card file: `pipeline/cards/CLC/operating_capacity.yaml` (Wave 1 LOCKED 2026-05-15 row 227; the v1.1 directory-case + lifecycle-field-name reconciliations originated here).
- §18.10 `operating_capacity` paragraph + §18 v1.1 §1.1–1.5 lineage.
- Single-track.
- OD-A v2.4: operating_capacity contributed 1 entry (cross-flag on `community wealth-building` from CLC-06 + CLC-08) — minimal admin-risk surface.

**Priority research vectors (refined).**
- Verify Ford BUILD, MacArthur field support, Kresge LIFT, Hewlett, Bush Foundation, community foundation capacity-building programs, capacity rubrics, Foundant/Submittable/Fluxx/GLM portal patterns, 2 CFR 200 where applicable.
- Strengthen distinctions among staffing, governance, data systems, strategic planning, TA, board development, administrative capacity.
- Add measurable capacity-gain templates: turnaround time, backlog, service volume, data quality, training completion, policies adopted, staff retained.
- Check whether foundation-specific common forms remain useful or should become funder database entries.
- Cowork addition: operating_capacity is the Wave 1 reference CLC card; new schema item-shape proposals should compare against this card's on-disk shape before recommending changes (lest they re-trigger the v1.1 narrow-corrective pattern).

**Acceptance tests.**
- "Need more staff" triggers bottleneck, job description, supervision, timeline, budget-to-task, sustainability prompts.
- Software/system request asks for adoption plan, data migration, training, ownership, measurable operating gains.

### §2.4 TILTH-CLC-04 `research_evidence`

**Operator impact target.** Enforce research logic: question, significance, method fit, data plan, human subjects, team qualifications, evaluation rigor, dissemination, broader impacts.

**Cowork canonical annotations.**
- Card file: `pipeline/cards/CLC/research_evidence.yaml` (Wave 2 LOCKED 2026-05-16 — confirm row).
- §18.10 `research_evidence` paragraph: full research-rigor enumeration.
- Single-track.
- OD-A v2.4: research_evidence contributed 9 entries to workspace admin_risk_register migration.
- Per §18.19.4 funding pathway: research_evidence is the probable CLC match for the §18.19 three-arm reviewer study's funding pitch (with catalytic_change + market_access as alternates).

**Priority research vectors (refined).**
- Verify NIH review criteria, NSF PAPPG + broader impacts, NIH DMS policy, 45 CFR 46, NIH/NSF biosketch rules, USDA AFRI, SARE, IES goals, SF-424 R&R forms, NIH Public Access, RPPR, Research.gov, DMPTool, 2 CFR 200.
- Separate basic research, applied research, evaluation, demonstration, SBIR/STTR, participatory research, field trials, education research.
- Strengthen data-management + IRB triggers.
- Clarify SBIR/STTR commercialization overlap with CLC-05 so the card doesn't blur research proof with market access. Cowork addition: the §18.6 v2 multi-track shape on CLC-05 (track_a sbir_phase_ii / track_b sbir_phase_iii) clarifies the SBIR boundary — research_evidence stays research-rigor-side; market_access track_a covers SBIR Phase II further-SBIR-funds review; market_access track_b covers Phase III commercialization-without-SBIR-funds.

**Acceptance tests.**
- Evaluation proposal asks for research question, design, sample, measures, data management, IRB, dissemination.
- SBIR prompt distinguishes Phase I feasibility, Phase II R&D, Phase III commercialization path.

### §2.5 TILTH-CLC-05 `market_access` — MULTI-TRACK (OD-E)

**Operator impact target.** Evaluate market-access funding through verified demand, buyer/channel commitments, revenue model, pricing, production capacity, unit economics, commercialization path, customer acquisition.

**Cowork canonical annotations.**
- Card file: `pipeline/cards/CLC/market_access.yaml` (Wave 2 LOCKED 2026-05-16 row 258; superseded post-OD-E restructure at row 276, 2026-05-17T16:00:00Z; post-restructure SHA3-512 = `4eb75e9296cffdf658f313614e6cd7730acafc1f471b69c59b48304506f2ec23cf8455a28cbe6c49583ca292f2983bfc10bf4b9ac2d11b12c3078022428be55e`).
- §18.6 v2 LOCKED row 274: top-level `track_a` (sbir_phase_ii) + `track_b` (sbir_phase_iii). Shared root metadata stays at root.
- §18.10 `market_access` paragraph: enumerates the v1 single-track content; the OD-E restructure partitions this content into the two tracks per the SBIR Phase II / Phase III distinction.
- OD-A v2.4: market_access contributed 13 entries to workspace admin_risk_register migration.
- §18.19.2 high-volume intersection: food_systems × market_access is one of the three highest-volume intersection cells.

**Priority research vectors (refined per multi-track shape).**

*Track A (sbir_phase_ii):*
- Verify SBIR Phase II program structure across NIH, NSF, USDA, DOE, DOD variants — further SBIR R&D funds; technical feasibility from Phase I extends to commercialization-readiness; team capability; intellectual merit + broader impacts.
- Reviewer profile: SBIR program managers + peer reviewers (technical SMEs).
- Evidence weights: Phase I demonstration results + Phase II technical work plan + commercialization plan + team biosketches.

*Track B (sbir_phase_iii):*
- Confirm Phase III wording: NO further SBIR funding; customer / private / non-SBIR capital; sole-source contract authority available to Phase II awardees.
- Verify USDA VAPG/LAMP/SCBGP/RFSP, Regional Food Business Centers, EDA Build to Scale, SBA growth programs, NSF I-Corps, state agricultural marketing, export/trade promotion, commercialization-plan templates.
- Strengthen evidence for buyer letters, purchase orders, sales history, customer pipeline, distributor agreements, market study, price sheet, customer interviews, channel partners.
- Reviewer profile: commercial procurement officers / private investors / strategic partners.

*Shared root:*
- `funding_mechanism_summary` reads as a single sentence spanning both tracks.
- Separate market-access logic from credit underwriting and research evidence (orthogonality).

**Acceptance tests.**
- Track A: An SBIR Phase II proposal routes to track_a; Scribe drafts a Phase II R&D narrative; reviewer-profile defaults pull from track_a.reviewer_profile_typical.
- Track B: An SBIR Phase III commercialization sole-source pursuit routes to track_b; Scribe drafts a commercialization narrative; "We have a huge market" challenge triggers buyer/customer evidence prompts.
- Operator-decision-at-draft: an opportunity tagged as "SBIR Phase II/III dual track" surfaces an SP0 operator-decision prompt asking which track applies to this opportunity — Scribe does NOT auto-aggregate.

### §2.6 TILTH-CLC-06 `credit_underwriting` — MULTI-TRACK (OD-E), TRACK B MINIMAL-STUB

**Operator impact target.** Evaluate loans, guarantees, CDFI lending, SBA lending, USDA credit, revolving funds, credit readiness through repayment capacity, cash flow, collateral, equity, controls, debt schedule, covenants, lender fit.

**Cowork canonical annotations.**
- Card file: `pipeline/cards/CLC/credit_underwriting.yaml` (Wave 2 LOCKED 2026-05-16 row 259; superseded post-OD-E restructure at row 277, 2026-05-17T16:00:00Z; post-restructure SHA3-512 = `bc050602bc6869addfba8988986717060f124e153b3068a08dc792e7e659c88a15adaeb98b3107552089aa8bce1b113a2067ce1d02d6a2389b59a35a8fca6ce9`).
- §18.6 v2 LOCKED row 274: top-level `track_a` (debt) + `track_b` (grant).
- **OPERATOR DIRECTIVE (binding for any researcher dispatched to this card):** Track B is a minimal-stub per operator decision 2026-05-17 at OD-E ceremony. Per the verbatim operator rationale recorded in `_partition_provenance.domain_clarification` on the card + §G of `section_00_5_section_18_6_v2_amendment.md`: "Grant logic and credit underwriting logic are objectively different mechanisms even though both are financial-access tools. The stacked-funding use case (e.g., VAPG + low-interest farm loan + tourism grant + small business loan + small business advantage grant) requires separate logic per funding type. Track B is therefore not the right home for grant-side capital — a separate CLC for grant-side credit-readiness or grant-side capital matching belongs in v0.2 Wave 3, not as Track B of credit_underwriting."
- The L-024 lesson candidate: **don't conflate grant logic with credit underwriting logic; stacked funding stacks separate mechanisms — each instrument deserves its own CLC at runtime, not Track A / Track B of one CLC.**
- v0.2 Wave 3 backlog: provisional new CLC slug `grant_side_credit_readiness` or `capital_readiness_grant` (final naming pending Wave 3 dispatch).
- OD-A v2.4: credit_underwriting contributed 15 entries to workspace admin_risk_register migration — joint-highest with catalytic_change.

**Priority research vectors.**

*Track A (debt) — IN SCOPE FOR RESEARCH:*
- Verify SBA SOP 50 10, SBA 7(a)/504/Microloan, USDA B&I, USDA Community Facilities loans, USDA IRP, CDFI Fund certification/awards, OFN CDFI Locator, SBA Lender Match, SSBCI, CDFA, SBDC, SCORE, ECOA/Reg B, FDIC underbanked, CFPB credit invisible, MDI references.
- Keep generic credit concepts sourced; avoid treating Investopedia-style materials as authority where official lender guidance exists.
- Strengthen evidence prompts: tax returns, P&L, balance sheet, cash flow forecast, debt schedule, collateral, owner equity, insurance, management resume, use-of-funds.
- Clarify where Program Rule Packs own lender-specific eligibility.

*Track B (grant) — DO NOT EXPAND PER OPERATOR DIRECTIVE:*
- Substantive Track B research routes to a v0.2 Wave 3 backlog item for a separate grant-side credit-readiness CLC. Do not propose substantive Track B content from a card research session.
- Acceptable: confirm the existing minimal-stub Track B content + `_partition_provenance.domain_clarification` block remain intact post-Wave-3-CLC-spawn.

**Acceptance tests.**
- Track A: Loan request asks for repayment source, DSCR / cash flow, collateral, equity injection, existing debt, controls.
- Track A: Grant-style community impact claim does not replace repayment logic.
- Track B: Operator-decision-at-draft surfaces a question — "this opportunity looks like grant-side capital-readiness; route to the v0.2 Wave 3 grant-side-credit-readiness CLC when it exists" — and falls back to the minimal-stub Track B for the v0.1 timeframe.

### §2.7 TILTH-CLC-07 `sponsorship_corporate` — MULTI-TRACK (OD-E), OD-C FIX-IN-PLACE LINEAGE

**Operator impact target.** Distinguish sponsorship, cause marketing, corporate foundation grants, employee engagement, in-kind support, corporate giving — while keeping tax/UBIT/advertising and brand-safety boundaries visible.

**Cowork canonical annotations.**
- Card file: `pipeline/cards/CLC/sponsorship_corporate.yaml` (Wave 2 LOCKED 2026-05-16 row 260; OD-C row 272 FIX-IN-PLACE display-name swap applied — `TILTH-CLC-03` / `TILTH-CLC-02` literals replaced with `Operating Capacity` / `Catalytic Change` display names; superseded post-OD-E restructure at row 278, 2026-05-17T16:00:00Z; post-restructure SHA3-512 = `58b61e0382e83afced78769e8d643b7b0ccd6af8956451e5f0b36f6e87b29709d88755fcb4a5f32189daad1d7b1addec607c726aab99915832b13446dbe79e3b`; post-fix file size 74115 bytes).
- §18.6 v2 LOCKED row 274: top-level `track_a` (benefits_exchange) + `track_b` (corp_foundation_grant).
- §18.10 `sponsorship_corporate` paragraph mentions "Add two-track logic" — the OD-E amendment realizes that, in canonical schema shape.
- OD-A v2.4: sponsorship_corporate contributed 9 entries to workspace admin_risk_register migration.
- The OD-C FIX-IN-PLACE lineage: this card was the single FAIL in the OD-C row 272 backfill scan; future research sessions MUST scan for and avoid reintroducing `TILTH-CLC-NN` slug literals in value positions (use display names like "Operating Capacity").

**Priority research vectors (refined per multi-track shape).**

*Track A (benefits_exchange):*
- Verify IEG/sponsorship industry guidance, FTC endorsement guides, state commercial co-venturer rules, Engage for Good, IRS 26 CFR 1.513-4 qualified sponsorship payments + IRS Publication 1771 (the UBIT boundary), Benevity, Bonterra/CyberGrants.
- Strengthen activation schedule, audience proof, sponsor benefits, brand alignment, disclosure, measurement, post-event reporting, renewal logic.
- Reviewer profile: CMO / CSR Director / Community Relations / Brand Manager — decision-maker-driven, rarely scored against a published rubric. Sponsorship deck is the primary application artifact.

*Track B (corp_foundation_grant):*
- Verify National Council of Nonprofits, Council on Foundations corporate foundations, corporate foundation examples, multi-state solicitation registration.
- Behaves like foundation grants with CSR overlay (mission-fit + capacity + outcomes + budget + parent-company brand-alignment screen).
- Reviewer profile: corporate foundation program officer + parent-company brand review.
- Portals: Foundant + Cybergrants typical. Rubric: foundation-style structured scoring with parent-company brand review layered on.

**Acceptance tests.**
- Track A: "We need a corporate grant" first asks whether this is sponsorship, foundation grant, matching gift, employee volunteer program, or cause marketing — then routes accordingly.
- Track A: Sponsorship deck prompt requires audience, benefits, activation, measurement, brand risk.
- Track B: Corporate foundation grant prompt asks for mission-fit + outcomes + budget + parent-company brand alignment.
- Cowork addition (regression test): scan the card body for `TILTH-CLC-NN` slug literals; expect 0 findings post-OD-C FIX-IN-PLACE. Any finding is a regression and surfaces for FIX-IN-PLACE dispatch.

### §2.8 TILTH-CLC-08 `shared_assets`

**Operator impact target.** Evaluate shared assets through shared need, users, governance, access policy, site/asset control, utilization, maintenance, insurance, cost recovery, replacement reserve, anti-capture safeguards.

**Cowork canonical annotations.**
- Card file: `pipeline/cards/CLC/shared_assets.yaml` (Wave 2 LOCKED 2026-05-16 — confirm row).
- §18.10 `shared_assets` paragraph: enumerates the eight evidence categories (user/member commitments, governance agreement, access policy, etc.).
- Single-track.
- §CC-4 (Wave 2 close synthesis) streak-breaker pattern: shared_assets used the comment-block-only fold-in discipline (along with credit_underwriting) — it is one of the on-disk references for §18.11 v1.1 Phase 4 fold-in checklist.
- OD-A v2.4: shared_assets contributed 7 entries to workspace admin_risk_register migration (including cross-flag on `community wealth-building` from CLC-06 + CLC-08).
- L-024 connection: shared_assets co-funds with cooperative (CIC-05) or food_systems (CIC-01) more than other CICs; the runtime composition is orthogonal — co-funding is the operator's runtime decision, not a card-body coupling.

**Priority research vectors (refined).**
- Verify USDA Community Facilities, RCDG, RFSP/LAMP, HFFI, Community Food Projects, CDFI shared food infrastructure, replacement reserve guidance, Kresge/community development, 7 CFR 3570, 2 CFR 200, FSMA, ADA, Davis-Bacon, PA DCED Keystone Communities.
- Add stronger evidence prompts for user commitments, scheduling/access rules, conflict resolution, fee waivers, non-discrimination, onboarding/training, maintenance logs, insurance, reserve contributions.
- Clarify boundary with Public Purpose & Works and Credit & Underwriting without making eligibility claims (orthogonality).
- Check whether food-system shared-use kitchen assumptions overfit the card; recommend broadening or routing kitchen-specific content to a state-overlay (OD-G coordination).

**Acceptance tests.**
- Shared-use kitchen request asks for users, access rules, health/FSMA licensing, site control, maintenance, scheduling, insurance, utilization, reserve.
- Equipment library request flags one-party capture risk if governance is weak.
- Cowork addition: a research session proposing a new field structure for the shared-use kitchen vs equipment library distinction uses comment-block-only fold-in discipline per §18.11 v1.1 — does not introduce a `kitchen_specific_fields` parallel field structure.

## §3 — Cross-card synthesis prep (for the batch supervisor)

This per-card plan supports the batch supervisor's cross-card synthesis at `docs/cic_clc_unified_batch_supervisor_prompt_2026-05-17.md`. After the 14 per-card handbacks return, the supervisor will roll up:

- **Lifecycle gap (the `draft_status: "draft"` issue):** all 14 cards expected to surface this; consolidate to a single §CC-N item + a single §18 v1.x amendment + a single 14-row supersession-re-sign ceremony per OD-E precedent.
- **Admin-risk register consolidation:** continue the OD-A pattern; route recurrent terms (≥3-card recurrence or higher per operator-chosen threshold) to `admin_risk_register.yaml` v2.x → v3.0 scrub workflow.
- **Program Rule Pack extraction:** live deadlines / amounts / forms route out of card bodies into `pipeline/program_rule_packs/<funder>/<program>.yaml` (forward-compat at v0.1 Beta).
- **State overlay separation:** PA-specific examples surface for OD-G coordination if active.
- **Coupling-discipline backfill:** scan all 14 cards against LIVE F-CARDS-COUPLING-VIOLATION-EXTENSION; expect 14/14 PASS post OD-C row 272 + OD-E rows 274/276/277/278.
- **Multi-track regression:** confirm CLC-05/06/07 schema validation under §18.6 v2 oneOf branch 2 (multi-track); confirm single-track CLCs (CLC-01/02/03/04/08) still validate under branch 1.
- **Regression-test coverage:** prioritize the §18.19.2 high-volume intersections (food_systems × operating_capacity, food_systems × market_access, food_systems × catalytic_change).

The supervisor's output (the batch synthesis file + per-OD handoff briefs + completion handoff) feeds the operator's next round of LOCK ceremony decisions.
