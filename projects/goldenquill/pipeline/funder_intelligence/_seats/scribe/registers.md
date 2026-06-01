# Scribe — Cross-Charter Register Library

**Authored:** 2026-05-19, Pass 3 (Scribe) dry-run
**Scope:** Cross-funder Scribe register patterns that emerge across the 14 Pillar-1 charters. This document is the source-of-truth for what Scribe does DIFFERENTLY funder-to-funder at the voice / register / mandatory-framing layer. It companions the per-charter `runtime_consumers.scribe` blocks (now structured to a 7-field mapping at Pass-3 LOCK) and the per-charter `language_register` / `drafting_implications` blocks (funder-level) plus the `language_register_inheritance:` pointers (program-instance level).

**Status:** v0 dry-run. Acceptance criteria: each register section must trace to (a) the corpus of 14 Pillar-1 charters' language_register + drafting_implications blocks OR (b) the canonical reference doc. Conjecture is marked `[CONJECTURE — Pillar-2 corpus pending]`.

**Pattern shape:** mirrors Pass-2 Scout heuristics.md §1 funder-class structure. Each section gives: voice signature; preferred terms; suspicious terms; sentence shapes that work; sentence shapes that fail; source_authority.

---

## §1 — USDA-RD register (federal-rural-prosperity / leveraging / public-purpose)

**Voice signature.** USDA-RD-fluent federal-program-officer register; rural-prosperity framing leads §I; "leveraging" (noun-form only) when describing match; FTE-quantified economic-impact in §II; public-purpose justification for nonprofit/tribal applicants; OMB-adjusted decennial census cited for rural-area service-area.

**Preferred terms.** `rural_prosperity`, `leveraging` (noun), `economic_impact`, `jobs_created`, `jobs_retained`, `small_and_emerging_businesses` (RBDG-canonical but cross-program-typical), `rural_community`, `public_purpose`, `essential_community_facility` (CFP-canonical), `cooperative` (RCDG-canonical).

**Suspicious terms.** `innovative` (underweighted vs leveraging + impact), `cutting_edge`, `revolutionary`, `significant_impact` without effect size, `sustainable` (not punished but not particularly rewarded at USDA-RD; that's SARE territory).

**Sentence shapes that work.**
- "We will leverage $[X] in cash match (unconditional, commitment letters attached) to deliver [N] FTE jobs created + [M] FTE jobs retained over [T] years in [named rural county/region]."
- "This project advances USDA-RD's rural prosperity mission by [specific economic-impact mechanism]."

**Sentence shapes that fail.**
- *"Our innovative approach will create rural opportunity..."* (suspicious terms + vague).
- *"Significant economic impact will result..."* (no effect size; no methodology).
- *"We will partner with local farmers to..."* (applicant-vs-beneficiary clarity absent for RBDG/RCDG).

**Source authority.** Canonical reference §USDA Rural Development (USDA‑RD) Funder Profile + cross-program 7 CFR Part 4280 / 4284 / 3570 framing patterns. Specific "leveraging > innovation" weighting heuristic is operator-derived; Pillar-2 corpus pending.

**Program-instances composing this register.** USDA-RD-RBDG-FY26 (small-and-emerging overlay), USDA-RD-RCDG-FY26 (CDC + NCBA-CLUSA overlay), USDA-RD-CFP-FY26 (essential-community-facility + MHI + Davis-Bacon + NEPA overlays).

---

## §2 — USDA-NIFA register (peer-review-academic / hypothesis / methodology)

**Voice signature.** Peer-review-academic register; methodology-first §I ordering; falsifiable hypothesis + statistical power analysis + prior-evidence cites; co-investigator role + time commitment documented; broader-impacts / extension plan as a distinct section, not afterthought; IRB/IACUC/DMP cross-references when subjects-research or data-generation signals present.

**Preferred terms.** `hypothesis`, `methodology`, `statistical_power`, `control`, `treatment`, `falsifiable`, `peer_reviewed`, `broader_impacts`, `extension` (NIFA-canonical), `intellectual_merit`.

**Suspicious terms.** `innovative` (without methodology specifics), `groundbreaking`, `paradigm_shift`, `significant_results` (without effect size), `we_will_explore` (implies no hypothesis).

**Sentence shapes that work.**
- "We hypothesize that [X mechanism] produces [Y measurable outcome] in [Z agroecosystem], testable via [methodology] with statistical power of [N] to detect effect size [E]."
- "Prior work (Smith et al. 2023; Jones et al. 2024) demonstrates [phenomenon] in adjacent systems; this proposal extends to [novel context] via [specific methodology]."

**Sentence shapes that fail.**
- *"We will explore the relationship between..."* (no hypothesis).
- *"This innovative approach will yield significant insights..."* (suspicious terms).
- *"We expect to see effects..."* (no methodology, no effect size).

**Source authority.** USDA-NIFA Grants Application Guide + canonical reference §USDA – National Institute of Food and Agriculture (USDA‑NIFA) Funder Profile. Specific weighting heuristics ("methodology rigor ≥30%") operator-derived; pinpoint NIFA AFRI / OREI / BFRDP rubric ingest pending Pillar-2.

**Program-instances composing this register.** USDA-NIFA-SARE-NE-FY26 (with SARE-specific overlay — see §4).

---

## §3 — USDA-AMS register (market-access / producer-revenue causal chain)

**Voice signature.** Market-access register; producer-revenue causal chain explicit in §II; USDA-AMS canonical value-added definition cited verbatim in §I (program-instance specific); buyer commitments (signed PO ideal, LOI minimum) attached as Exhibits and referenced by ID; 'producer' (not 'farmer alone'); cash before in-kind in matching-funds narrative; contingent commitments flagged explicitly.

**Preferred terms.** `value_added`, `producer` (not 'farmer' alone), `market_access`, `revenue_increase`, `producer_marketing_chain`, `aggregation_for_producer_ownership`, `planning_grant` (VAPG track), `working_capital` (VAPG track), `matching_funds`.

**Suspicious terms.** `innovative`, `cutting_edge`, `we_will_explore_market`, `significant_market_opportunity` (without sized dollar), `farmer` (use 'producer').

**Sentence shapes that work.**
- "Producer [name] produces [commodity X] at [N units/year]; this project transforms X into [value-added product Y]; Y captures premium of $[Z]/unit; revenue increases from $[A]/year to $[B]/year."
- "Buyer commitment from [named buyer] documents [N units] at $[price] over [T years] (signed PO Exhibit [X])."

**Sentence shapes that fail.**
- *"We will market our product to farmers..."* (passive; no causal chain).
- *"Significant market opportunity exists..."* (suspicious terms; no sizing).

**Source authority.** Canonical reference §USDA – Agricultural Marketing Service (USDA‑AMS) Funder Profile + §USDA-AMS Evaluation Themes. VAPG rubric source-backed at `pipeline/rubrics/vapg_fy26.json` (100 pts, 7 criteria — extracted). Cross-program weighting heuristics operator-derived; pinpoint Pillar-2 LAMP / FMPP / LFPP / SCBGP corroboration pending.

**Program-instances composing this register.** USDA-AMS-VAPG-FY26 (Planning vs Working Capital track-selection + value-added definition verbatim overlays).

---

## §4 — SARE register (producer-as-co-investigator / three-pillar sustainability)

**Voice signature.** Sustainable-agriculture-research register — overlays the USDA-NIFA peer-review-academic base register with SARE-specific moves: SARE's three-pillar sustainability definition (economically viable + environmentally sound + socially responsible) cited verbatim in §I; producer named as **co-investigator** (NOT collaborator / subject / data source); outreach plan as a distinct section with ≥3 dissemination channels + reach target per channel + timeline; producer-engagement letter on PRODUCER letterhead (not researcher-institution letterhead).

**Preferred terms.** `sustainable_agriculture` (SARE-canonical; verbatim from SARE definition), `economically_viable`, `environmentally_sound`, `socially_responsible`, `producer` (not 'farmer' alone; SARE includes ranchers, producers, growers), `co_investigator` (for the producer partner; signals partnership integrity), `outreach`, `dissemination`, `measurable_outcome`, `on_farm_research` (SARE-canonical), `producer_to_producer` (SARE-canonical for farmer-network outreach).

**Suspicious terms.** `innovative` (SARE reviewers averse without specific operational difference), `cutting_edge` (generic-sounding; SARE prefers concrete + measurable), `subject` (for the producer — implies extraction, not partnership), `collaborator` (for the producer — should be co-investigator; collaborator is weaker), `will_share_results` (placeholder for outreach plan; trigger for Red Team probe), `significant_impact` (without effect size + counterfactual).

**Sentence shapes that work.**
- "We will [specific action] with [named producer] as co-investigator, measuring [specific outcome] over [timeframe], with reach to [N] producers via [named channels]."
- "SARE defines sustainable agriculture as [verbatim three-pillar definition]. This proposal advances all three pillars through [pillar 1 mechanism], [pillar 2 mechanism], [pillar 3 mechanism]."

**Sentence shapes that fail.**
- *"We will conduct research and share findings."* (generic; no outreach channels; no co-investigator language).
- *"Our innovative approach will revolutionize..."* (suspicious terms; no concrete operational difference).
- *"Farmers will benefit from..."* (passive; producer-as-recipient, not co-investigator).

**Source authority.** USDA-NIFA-SARE-NE FY26 Partnership Grant RFA + canonical reference §USDA‑NIFA – SARE Northeast (FY 2026). SARE national framework three-pillar definition source-backed. Producer-as-co-investigator weighting heuristic operator-derived from SARE Partnership track guidance; pinpoint Pillar-2 FY26 RFA ingest pending.

**Charter:** USDA-NIFA-SARE-NE-FY26 (Northeast-region applicability — out-of-region applicants route to sister-SARE programs Southern / North-Central / Western).

---

## §5 — PA state register (Commonwealth-localized / county-district / PA-Preferred conditional)

**Voice signature.** State-program-officer register; PA-Commonwealth-localized; named county + Senate-district + House-district economic-impact framing; PA-Preferred branding conditional (verify eligibility BEFORE claiming); PA-source data backing (PA-Census, PA Center for Workforce Information) over national-only data; state-budget-cycle awareness; "Commonwealth of Pennsylvania" or "Pennsylvania" (not generic "PA" alone in formal narrative).

**Preferred terms.** `PA_Preferred`, `Pennsylvania`, `PA_Farm_Bill`, `rural_PA`, `PA_specialty_crop`, `state_match`, `Pennsylvania_agriculture`, `Commonwealth_of_Pennsylvania`. PA-DCED-specific overlay: `economic_impact`, `FTE`, `private_investment_leverage`, `Keystone_Communities`, `industrial_sites_reuse`, `PIDA`, `main_street`.

**Suspicious terms.** `innovative` (state-officers neutral on novelty framing), `cutting_edge`, `we_will_serve_the_region` (too vague), `significant_PA_impact` (without sizing). PA-DCED-specific: `we_will_attract` (without committed investor), `significant_economic_growth` (without sizing).

**Sentence shapes that work.**
- "This project creates [N] FTE jobs in [named PA county] (PA Senate District [X], PA House District [Y]) at $[Z] average wage, with PA-source match of $[W] from [named PA funder/program]."
- "Product is PA-Preferred eligible (PA-grown / PA-produced / PA-processed per category [C]) per PA-Preferred standards."
- "Private-investment leverage of $[X] from [named investor] is committed (Exhibit [E]: signed commitment letter)." *(DCED overlay)*

**Sentence shapes that fail.**
- *"We will serve rural Pennsylvania..."* (no district / county specifics).
- *"This innovative PA-Preferred opportunity..."* (suspicious terms; PA-Preferred without eligibility).
- *"We will create significant economic growth..."* (DCED — suspicious + no sizing).

**Source authority.** Canonical reference §Pennsylvania Department of Agriculture + §PA Dept of Ag – Agricultural Innovation Grant Program (FY 2025–26) + operator-attested PA-Preferred standards + PA-DCED program portfolio. Specific weighting heuristics operator-derived; pinpoint PIDA / Keystone Communities / FY26 AGINNOV NOFA ingest pending Pillar-2.

**Program-instances composing this register.** PA-DEPT-AG-AGINNOV-FY26 (grant-type-cascade + non-State-match overlay — Pass-0 D-AGINNOV polarity flip). PA-DCED is a sister state-agency funder-level charter with its own ECONOMIC-DEVELOPMENT-METRICS overlay that composes PA-state register but weights private-investment leverage heavier than PA-DEPT-AG.

---

## §6 — Heinz register (theory-of-change / sustained impact / SWPA-anchored / M1/M2/M3 mechanism alignment)

**Voice signature.** Foundation-program-officer register; theory-of-change framing dominates §I; all three GPR-derived behavior_mechanisms wired explicitly into section content:

- **M1 regional_legitimacy_capital** — frame the request as a regional alignment opportunity, not merely an organizational need. Name the larger Pittsburgh civic / SWPA-ecosystem movement the project sits inside.
- **M2 transition_sensitive_relationship_clarity** — make strategic-fit logic explicit. Map the project to one (or more) of the seven canonical strategic areas. Surface any context that Heinz program officers might NOT already have (active strategy refresh + 53 active grants + 50 apps per staffer per GPR 2024).
- **M3 capacity_partnership_beyond_grant** — include a partnership-use paragraph in §V (or sidebar): name how Heinz can help beyond dollars — thought partnership, convening, introductions, multi-year continuity.

Foundation-program-officer register; named SWPA sub-geography (Allegheny / Armstrong / Beaver / Butler / Fayette / Greene / Indiana / Lawrence / Washington / Westmoreland) — NOT generic "greater Pittsburgh area"; sustained-change / transition-plan in §III; calibrate request size against Heinz's median ~$100K (2024 GPR).

**Preferred terms.** `theory_of_change`, `outcomes` (NOT outputs), `mechanism`, `sustained_change`, `operational_picture`, `program_officer` (foundation-canonical), `strategic_area` (Heinz canonical per 2026 site refresh; supersedes "thematic_area"), `southwestern_pennsylvania`, `SWPA`, `emerging_practice`, `place_based`, `historically_disadvantaged` (GPR 2024 portfolio-pattern alignment).

**Suspicious terms.** `unsupported_innovation` (innovative claim without track record / mechanism / evidence — backed innovation IS rewarded per GPR p.2), `unsupported_cutting_edge`, `we_will_deliver` (activity framing not outcomes), `significant_outputs` (outputs ≠ outcomes). NOTE: "rural" was previously flagged here and was REMOVED in the [FIDELITY-FIX-HEINZ] amendment 2026-05-18 — SWPA includes Greene, Fayette, Indiana, Lawrence, Armstrong, Butler — all of which have rural and small-town communities Heinz actively funds.

**Sentence shapes that work.**
- "If we [intervention] in [named SWPA county or Pittsburgh neighborhood], we expect [outcome] over [3 years], because [mechanism]. By year 3, success looks like [specific operational picture]." *([M1] regional alignment + [M2] strategy fit)*
- "Sustained change at year 5 requires [retention mechanism] beyond grant period; we will [transition plan]."
- "Our work expressly benefits residents of [named SWPA county] within the southwestern Pennsylvania region." *(PA-statewide-serving-SWPA framing)*

**Sentence shapes that fail.**
- *"We will deliver workshops to X participants..."* (outputs as outcomes).
- *"Our innovative approach will create..."* (suspicious — unsupported innovation).
- *"Our program serves the greater Pittsburgh area..."* (generic; name the actual county or neighborhood).

**Source authority.** Heinz GPR 2024 Key Findings Memo + Heinz public Grants page + Heinz strategies page (anchored in [FIDELITY-FIX-HEINZ] commit). The three-mechanism wiring (M1/M2/M3) is source-backed. Foundation-program-officer register is operator-derived heuristic.

**Charter:** HEINZ-FOUNDATION.

---

## §7 — RK Mellon register (scale / permanence / strategic capital / governance)

**Voice signature.** Strategic-capital register; 10-20 year scale-and-permanence framing leads §I; conservation outcomes quantified in protected acres + habitat metrics; economic-development outcomes quantified in FTE jobs + private-investment leverage; permanence mechanism named (endowment / earned revenue / cross-funder pipeline); senior-leadership / board engagement readiness documented.

**Preferred terms.** `strategic_capital`, `scale_and_permanence`, `multi_year_commitment`, `conservation` (canonical for RK Mellon Conservation track), `protected_acres`, `habitat_metrics`, `large_landscape_stewardship`, `regional_economic_development`, `senior_leadership`, `endowment`.

**Suspicious terms.** `innovative` (rewarded less than scale-and-permanence), `cutting_edge`, `we_hope_to` (aspirational permanence flag), `significant_impact` (without scale + permanence + measurement).

**Sentence shapes that work.**
- "Over 10-20 years, this project [outcome] in [southwestern PA / specific landscape], deployed at $[X] strategic capital with permanence mechanism [Y]."
- "Conservation outcomes: [N] protected acres of [habitat type], measured by [methodology], over [T] year horizon."

**Sentence shapes that fail.**
- *"We will protect natural resources..."* (no acres / habitat).
- *"We hope to sustain this beyond the grant..."* (aspirational; no mechanism).

**Source authority.** Canonical reference §Richard King Mellon Foundation (six program areas + emphasis: scale, permanence, leadership, measurable outcomes). Strategic-capital weighting heuristics operator-derived; pinpoint Pillar-2 RK Mellon position-paper / program-officer interview ingest pending. P1-9 reconciliation pending: charter currently encodes 5-program-area subset; canonical reference enumerates 6.

**Charter:** RICHARD-KING-MELLON-FOUNDATION.

**Cross-foundation note.** Within the Pittsburgh-foundation cohort (Heinz / RK Mellon / Hillman / McCune / Pittsburgh Foundation), RK Mellon weights scale-and-permanence heavier than Heinz; Heinz weights M1/M2/M3 relationship signals heavier than RK Mellon. Same SWPA applicant pitching both code-switches per foundation.

---

## §8 — NCBA-CLUSA register (cooperative authenticity overlay)

**Voice signature.** Cooperative-board-peer-review register — NOT a standalone-funder register but a CROSS-FUNDER COMPOSABLE OVERLAY. Any USDA program favoring cooperatives (RCDG / VAPG / RBDG) or foundation funder favoring cooperative governance composes the Rochdale-principles operationalization layer over its own register.

State-cooperative-corporation-act registration documented in §I; all 7 Rochdale principles operationalized explicitly in §II; bylaws Articles cited for patronage-distribution + surplus-to-members + democratic-governance; member-education program (curriculum + facilitator + cadence) documented; sister-coop partnerships + NCBA-network engagement named.

**Preferred terms.** `cooperative`, `member_ownership`, `one_member_one_vote`, `patronage_dividend`, `surplus_allocation`, `Rochdale_principles`, `democratic_governance`, `member_education`, `cooperation_among_cooperatives`, `Subchapter_T` (IRS cooperative tax pass-through).

**Suspicious terms.** `innovative`, `cutting_edge`, `we_are_cooperative` (without operational substance), `member_driven` (without one-member-one-vote operationalization), `community_oriented_nonprofit` (signals NOT cooperative form).

**Sentence shapes that work.**
- "Cooperative registered under [state cooperative corporation act §X], with [N] members each holding one vote at annual meeting (Bylaws Art. [Y]). Surplus allocated to members per patronage formula in Bylaws Art. [Z]."
- "All 7 Rochdale principles operationalized: [voluntary membership: open enrollment]; [democratic governance: annual meeting + member vote]; [member economic participation: patronage distribution]; [autonomy: independence from non-member control]; [education: curriculum + facilitator]; [cooperation: sister-coop partnerships]; [community concern: outreach program]."

**Sentence shapes that fail.**
- *"We are a member-driven organization..."* (without operational substance).
- *"Our cooperative approach to community work..."* (cooperative as adjective; not cooperative as form).

**Source authority.** Canonical reference §NCBA CLUSA – Cooperative Authenticity Layer + the Rochdale Pioneers principles + IRS Subchapter T cooperative tax pass-through. The two principles routinely tested by scoring are one-member-one-vote (Rochdale 2) and patronage (Rochdale 3). NCBA-CLUSA-specific corpus is conjecture pending Pillar-2 — marked `[CONJECTURE — Pillar-2 corpus pending]` per Pass-2 P2-7.

**Charter:** NCBA-CLUSA (overlay anchor); composed into USDA-RD-RCDG-FY26 (CDC describing sub-cooperative beneficiaries) and into USDA-AMS-VAPG-FY26 (when applicant is a producer cooperative).

---

## §9 — Cross-funder composition patterns

**Pattern 1 — Same applicant, multiple agencies, code-switching per agency.**
A producer cooperative might pitch USDA-AMS VAPG (market-access + producer-revenue), USDA-RD RCDG (CDC + cooperative-authenticity overlay), USDA-NIFA AFRI (peer-review-academic + hypothesis-first), and PA-DEPT-AG AGINNOV (state-program-officer + non-state match). Each is a different register; same substance code-switched.

**Pattern 2 — Composable overlays.**
NCBA-CLUSA's cooperative-authenticity overlay composes onto USDA-RD-RCDG (sub-cooperative beneficiaries), USDA-AMS-VAPG (cooperative applicants), and any foundation funder favoring cooperative governance. The overlay does NOT replace the base register — it adds Rochdale-principles operationalization within whichever register-of-record applies.

**Pattern 3 — Program-instance inheritance.**
Federal program-instances (RBDG, RCDG, CFP, VAPG, SARE-NE) inherit funder-level register (USDA-RD, USDA-AMS, USDA-NIFA) and add program-specific overlays. Inheritance is documented via the `language_register_inheritance:` block in each program-instance charter rather than duplicating funder-level register entries — keeps the source-of-truth at the funder level and avoids drift.

**Pattern 4 — Funder-class register families.**
Three broad families emerge:

| Family | Funders | Register signature |
|---|---|---|
| Federal | USDA-RD, USDA-NIFA, USDA-AMS | Federal-program-officer register; OMB-canonical compliance baseline; FTE / hypothesis / value-added registers per sub-agency. |
| State | PA-DEPT-AG, PA-DCED | State-program-officer register; PA-Commonwealth-localized; named county + Senate / House districts; state-budget-cycle awareness. |
| Foundation | Heinz, RK Mellon | Foundation-program-officer register; theory-of-change / scale-and-permanence dominant; rolling LOI vs board-meeting cadence; relationship-sensitive. |

NCBA-CLUSA is cross-family (overlay).

---

## §10 — Anti-patterns (what Scribe MUST NOT do)

These are the negative-space register heuristics — practices that have shown up as failure modes in the canonical reference + improvements logs.

1. **Do not silently rewrite operator-flagged terms.** If a term appears in `language_register.suspicious_terms`, Scribe presents the operator with substitution options (per CLAUDE.md Law 4 funder-dialect code-switching). Scribe does NOT silently rewrite.
2. **Do not invent register entries.** Each preferred / suspicious term traces to a charter's language_register block or to the canonical reference. New terms surfaced at draft time route through operator review at Pass 3 or later, not as silent additions.
3. **Do not collapse register across funder classes.** USDA-RD's "leveraging" framing is not Heinz's framing. USDA-NIFA's hypothesis-first ordering is not USDA-AMS's value-added ordering. Code-switch per funder, do not template.
4. **Do not skip the inheritance pointer.** Program-instance charters MUST declare `language_register_inheritance:` rather than re-declaring funder-level register entries inline; otherwise inheritance drift is impossible to detect.
5. **Do not encode CIC→CLC binding in register guidance.** Per CLAUDE.md, CICs and CLCs are orthogonal. Scribe's register guidance is keyed to the FUNDER (CLC-axis-of-funder-side) not to the applicant CIC archetype. Same applicant CIC, different funder = different register.
6. **Do not promote conjecture register entries to source-backed without operator attestation.** [CONJECTURE — Pillar-2 corpus pending] markers stay until Pillar-2 ingest + operator sign-off.

---

## §11 — Open questions for operator

1. **NCBA-CLUSA overlay composition contract.** Should `language_register_inheritance:` carry a `composed_overlay:` field naming the cooperative-authenticity overlay explicitly? Currently RCDG declares it; VAPG declares it as conditional ("when applicant is a cooperative"). Pass 3 left both shapes as authored; operator may want a single canonical shape.
2. **Funder-class enum field.** Should each charter carry a structured `funder_class: federal | state | foundation | cooperative_overlay` field? Currently implicit in inheritance pointers. (Parallel to Pass-2 Scout §6.4 open question.)
3. **Register-versioning.** When Heinz refreshes its 7-strategy taxonomy or PA-Dept-Ag updates its specialty-crop list, how does Scribe register version-track? Pass 3 left versioning implicit; operator may want explicit `register_version:` field with refresh-trigger semantics.
4. **Drafting-warning gate-class migration.** Per Pass-1 P1-7, several gates classified `competitive_scoring_signal` at Pass 1 are candidates for `drafting_warning` migration (HEINZ outcomes/taxonomy/innovation; SARE-NE producer-as-collaborator; PA-DEPT-AG named-district; RK Mellon permanence). Pass 3 leaves the migration to Pass 4 / operator decision; preferred Pass-3 posture is to keep them as competitive_scoring_signal with explicit drafting-warning narrative in the per-charter scribe block.

---

## Cross-references

* Canonical methodology: `docs/FID_REFINEMENT_METHODOLOGY_2026-05-18.md`
* Canonical content reference: `docs/FID_CANONICAL_REFERENCE_2026-05-18.md`
* Mistakes log: `docs/FID_MISTAKES_LOG_2026-05-18.md` (Pass-3 append pending operator approval)
* Pass-2 Scout heuristics: `pipeline/funder_intelligence/_seats/scout/heuristics.md`
* Per-charter Scribe inventory: `pipeline/validation/pass-3-scribe-dry-run-2026-05-18/per_charter_scribe_inventory.md`
* Pillar-1 charter set: `pipeline/funder_intelligence/pillar_1_charters/`
