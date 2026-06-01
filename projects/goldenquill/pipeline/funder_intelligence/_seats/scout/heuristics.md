# Scout — Cross-Charter Heuristic Library

**Authored:** 2026-05-19, Pass 2 (Scout) dry-run
**Scope:** Cross-funder pre-filter patterns that emerge across the 14 Pillar-1 charters. This document is the source-of-truth for what Scout does DIFFERENTLY funder-to-funder, and what it does the SAME across all funders. It companions the per-charter `runtime_consumers.scout` blocks.

**Status:** v0 dry-run. Acceptance criteria: each heuristic must trace to (a) the corpus of 14 Pillar-1 charters' Scout blocks OR (b) the canonical reference doc. Conjecture (heuristics not yet backed by charter or canonical reference) is marked `[CONJECTURE — Pillar-2 corpus pending]`.

---

## §1 — Funder-class heuristics (the "first-axis" Scout decision)

Scout's FIRST action on encountering an opportunity is to classify the funder. The class determines which pre-filter family runs.

### §1.1 — Federal program (USDA, EPA, EDA, HUD, USDA-NIFA program-instance, USDA-RD program-instance, USDA-AMS program-instance)

**Universal pre-filter (inherited from federal-baseline):**

- SAM-active at submission (not just at-application) — registration must be live + non-expiring within the submission window
- UEI present in SAM record
- Federal debt resolved (31 USC 3720B)
- No active suspension / debarment (2 CFR 180)

**Source:** USDA-RD funder-level charter encodes these 4 PRE-gates explicitly (F-USDA-RD-SAM-INACTIVE / UEI-MISSING / FEDERAL-DEBT-UNRESOLVED / SUSPENSION-ACTIVE; 2 CFR 200 §200.205 + 2 CFR 180 + 31 USC 3720B).

**Inheritance pattern:** All federal program-instance charters (USDA-RD-CFP, USDA-RD-RBDG, USDA-RD-RCDG, USDA-AMS-VAPG, USDA-NIFA-SARE-NE) inherit this baseline implicitly. **At Pass 2, the baseline is now also encoded in their structured Scout blocks via `eligibility_dimensions.sam_uei_baseline`.**

**Scout pre-filter sequence:**
1. Federal-baseline check (above).
2. Funder-level program-portfolio check (does the opportunity fit the funder's program portfolio?).
3. Program-instance-specific gates (rural-pop threshold, producer-eligibility test, etc.).

---

### §1.2 — Federal funder-level (USDA-AMS, USDA-NIFA, USDA-RD)

**Pre-filter responsibilities:**

- The federal-baseline check (§1.1).
- Funder-level register / sector classification (Is this a USDA-AMS opportunity? USDA-NIFA? USDA-RD?).
- Routing DOWN to program-instance charters when fit is identified.
- Routing LATERALLY to sister federal funders when fit is borderline.

**Note:** Funder-level federal charters typically carry 0-1 hard_eligibility_gate at the funder layer; the load-bearing predicates live in program-instances. USDA-NIFA carries 0; USDA-AMS carries 1 (independent-producer); USDA-RD carries 4 (the baseline itself).

---

### §1.3 — State-program (PA-DEPT-AG, PA-DCED, PA-DEPT-AG-AGINNOV)

**Universal pre-filter:**

- **PA-locality.** Project located in PA / principal operations in PA / explicit PA-resident-benefit. This is a P0 hard gate on all PA state-program charters.
- **State-budget-cycle awareness.** Operator-attention trigger when state appropriation has not yet been enacted at planned submission window. NOT a hard gate — but a Scout-layer signal that escalates to operator BEFORE Scribe is invoked.
- **PA-Preferred signal** (when applicable). Competitive scoring dimension, not hard gate.
- **Legislator-district sensitivity.** Operator-attention trigger when applicant identity is sensitive in a named-district frame. Operator judgment, not algorithmic.

**Source:** PA-DEPT-AG / PA-DCED / PA-DEPT-AG-AGINNOV-FY26 charter Scout blocks.

**Scout-layer absence:** PA state-program charters do **NOT** carry SAM/UEI baseline. PA state programs use their own state-vendor-registration system; federal SAM is irrelevant. Documented here so Scout doesn't falsely add SAM-check to state-program pre-filter.

---

### §1.4 — Foundation (Heinz, RK Mellon, [future: Hillman, Pittsburgh Foundation, McCune])

**Universal pre-filter:**

- **Eligible-entity-type.** 501(c)(3)+509(a) public charity is the baseline; some foundations widen to public-agency + mission-driven-for-profit (e.g., RK Mellon social-impact-investments branch).
- **Geographic concentration.** Foundation-grants are typically geo-concentrated. SWPA-10-county is the baseline for the Pittsburgh foundation cohort. Out-of-region is typically wrong-funder-match BUT may be weighted-fit-not-hard-fail (Heinz pattern) or hard-fail (RK Mellon pattern) depending on foundation.
- **Relationship signal.** Foundations weight prior funding / peer-grantee introduction / documented contact heavily. Cold-outreach is an operator-attention trigger, NOT a hard gate. Heinz GPR 2024 documents this explicitly.
- **Program-area alignment.** Each foundation has a named program-area roster; project must align. Roster shape varies by foundation.

**Scout-layer absence:** Foundation charters do **NOT** carry SAM/UEI baseline. Foundations do not require federal registration. Documented here for clarity per §S2-5 of Pass-2 improvements log.

**Source:** HEINZ-FOUNDATION + RICHARD-KING-MELLON-FOUNDATION charter Scout blocks.

---

### §1.5 — Cooperative-intermediary (NCBA-CLUSA, [future: Cooperative Development Foundation, Capital Impact Partners])

**Universal pre-filter:**

- **Cooperative form authenticity.** Applicant must be incorporated as a cooperative under state cooperative law. Nonprofit-with-cooperative-language is a wrong-funder-match flag.
- **Rochdale-principle operationalization.** Bylaws, governance, patronage distribution must enact (not aspire to) the 7 Rochdale Pioneers principles.
- **Member-equity / democratic-governance substance.** Documented in bylaws + minutes, not just claimed.

**Source:** NCBA-CLUSA charter Scout block (currently `[CONJECTURE — Pillar-2 corpus pending]`; Pillar-2 priority ingest target).

---

## §2 — Cross-funder routing heuristics (the "second-axis" Scout decision)

When Scout has classified the funder but encounters borderline fit, it routes laterally. The routing patterns observed across the 14 charters:

### §2.1 — Pittsburgh-foundation cohort

Heinz ↔ RK Mellon ↔ Hillman ↔ McCune ↔ Pittsburgh Foundation. Scout routes between these when:
- Applicant is SWPA-located.
- Project sits at the intersection of conservation / education / community-vitality / arts-culture.
- Foundation A's program-area roster doesn't include the project but Foundation B's does.

**Encoded in:** HEINZ-FOUNDATION + RICHARD-KING-MELLON-FOUNDATION Scout blocks.

### §2.2 — USDA portfolio routing

USDA-AMS ↔ USDA-NIFA ↔ USDA-RD lateral routing rules:

- **Producer-applicant + market-access focus** → USDA-AMS (and program-instances VAPG, FSMIP, SCBG, FMLFPP).
- **Researcher-applicant + scientific-merit focus** → USDA-NIFA (and program-instances AFRI, SARE).
- **Rural-area + community-facility / business-development focus** → USDA-RD (and program-instances CFP, RBDG, RCDG, B&I).
- **Non-producer, non-research, non-rural** → routed AWAY from USDA entirely (toward EDA, HUD CDBG, SBA, etc.).

**Encoded in:** USDA-AMS + USDA-NIFA + USDA-RD funder-level Scout blocks.

### §2.3 — State ↔ federal lateral routing

When applicant has BOTH state and federal track-record:

- **Scale ≤ $200K + state-match-allowed:** prefer state-program path (PA-DEPT-AG-AGINNOV, PA-DCED) — administrative burden lower.
- **Scale > $200K OR federal-match-required:** prefer federal path (USDA-AMS / USDA-RD / USDA-NIFA).
- **PA-Preferred eligibility positive:** prefer state-program path (additional competitive lift).
- **State-budget-cycle uncertain:** routing to federal path may reduce timing risk (federal NOFAs publish on fiscal-year cadence; PA state budget on biennial reconciliation).

**Encoded in:** PA-DEPT-AG / PA-DEPT-AG-AGINNOV-FY26 / PA-DCED Scout blocks.

### §2.4 — Cooperative ↔ Non-cooperative lateral routing

NCBA-CLUSA routes laterally to:

- **USDA-RD-RCDG** when applicant is a Cooperative Development Center (not the cooperative itself).
- **USDA-AMS** when cooperative is producer-cooperative seeking market access.
- **State coop programs** (when applicant has state-coop registration).

**Encoded in:** NCBA-CLUSA + USDA-RD-RCDG-FY26 Scout blocks.

---

## §3 — Timing-axis heuristics (the "third-axis" Scout decision)

Scout pre-filters not only WHO fits but also WHEN they should pursue.

### §3.1 — Federal-cycle timing

- Federal NOFAs publish per-program on roughly-annual cadence. Scout monitors NOFO drop dates (VERIFY phase fetches live NOFO URL + literal-FY-string + non-past closing_date).
- Cycle-CLOSED is a META warning (e.g., F-VAPG-CYCLE-CLOSED) — operator-attention trigger NOT applicant-eligibility hard gate. Applicant should defer to next cycle.

### §3.2 — State-cycle timing (PA-state-programs)

- PA state programs are gated by **state-budget reconciliation**. Appropriations must be enacted before the program can open. State-budget timing risk is a Scout-layer escalation trigger to operator.
- PA budget is biennial-with-annual-adjustments. Submission windows shift year-to-year based on budget timing.

### §3.3 — Foundation-cycle timing

- Foundations use LOI + invited-proposal cadence, with **rolling deadlines or quarterly board cycles**. Scout monitors the foundation's board-meeting calendar.
- Heinz transition timing (per GPR 2024) introduced operator-attention triggers: strategy refresh, staff-load increase, communication clarity decline. These are Scout-layer signals for whether to pursue NOW vs DEFER to post-refresh window.

---

## §4 — Operator-escalation heuristics (when Scout hands to operator BEFORE Scribe)

Scout's `operator_assist_required:` block fires on these conditions across charters:

1. **Hard-gate borderline.** Predicate is at threshold (e.g., applicant population is exactly 50,000 for RBDG; producer-authenticity is at fiscal-sponsor boundary).
2. **Source citation pending Pillar-2.** Scout cannot verify a claim against source authority; operator must attest.
3. **Cycle status uncertain.** Funding window is unclear (state-budget uncertainty, foundation-board cycle ambiguity, federal CR uncertainty).
4. **Relationship signal weak.** Foundation-specific: documented contact / prior funding absent (Heinz F-HEINZ-COLD-OUTREACH-WARNING pattern).
5. **Cross-funder routing decision required.** Borderline fit between sister-funders; operator picks lane.

---

## §5 — Anti-patterns (what Scout MUST NOT do)

These are the negative-space heuristics — practices that have shown up as failure modes in the canonical reference + improvements logs.

1. **Do not silently rewrite Scout claims that lack source citation.** If `source_authority` is `[CONJECTURE — Pillar-2 corpus pending]`, the claim must remain marked until Pillar-2 ingest, NOT silently promoted to source-backed.
2. **Do not invent cross-funder routing rules without corpus backing.** §2 routes are derived from the 14 charters' Scout blocks; routes not encoded are not invented.
3. **Do not pre-filter on Scribe-shape concerns.** Scout's job is eligibility + routing. Voice/register/funder-dialect concerns are Scribe's (Pass 3) job. Scout flags applicants who would NOT pass eligibility; it does NOT flag applicants who would draft poorly.
4. **Do not apply SAM/UEI check to non-federal funders.** Foundation and state-program charters do not carry the federal-baseline. Adding SAM-check to those Scout flows is a wrong-pattern application of §1.1.
5. **Do not silently merge CIC↔CLC binding.** CICs (customer identity) and CLCs (capital logic) are orthogonal per CLAUDE.md. Scout does NOT pre-bind a CIC to a CLC subset. The opportunity drives CLC engagement at runtime, not archetype.

---

## §6 — Open questions for operator

1. **CIC routing field.** Should `runtime_consumers.scout` carry an explicit `applicant_cic_routing:` field naming the CIC archetype Scout is operating in? Pass 2 left this out (the CIC binding lives at PROJECT_CONTEXT layer per-applicant), but operator may want explicit Scout-layer surface.
2. **CLC affinity field.** Should `runtime_consumers.scout` carry an explicit `funder_clc_affinity:` field naming the CLC types this funder typically engages? Pass 2 left this out (per CLAUDE.md no-pre-mapping rule), but the inventory at `per_charter_scout_inventory.md` does carry an "operator-inferred" CLC affinity per charter for discovery purposes — operator decides whether to formalize.
3. **Verify_required gate inclusion.** Per P1-7, several gates classified `competitive_scoring_signal` at Pass 1 are candidates for `verify_required_gate` migration. Should Scout's `hard_gate_refs` field also include `verify_required_refs` for those?
4. **Funder-class enum.** Should we encode the §1 funder-class as a structured field (`funder_class: federal_program | federal_funder_level | state_program | foundation | cooperative_intermediary`)? Currently implicit in the Scout block prose.

---

## Cross-references

* Canonical methodology: `docs/FID_REFINEMENT_METHODOLOGY_2026-05-18.md`
* Canonical content reference: `docs/FID_CANONICAL_REFERENCE_2026-05-18.md`
* Mistakes log: `docs/FID_MISTAKES_LOG_2026-05-18.md` (Pass-0 + Pass-1; Pass-2 append pending operator approval)
* Pass-1 Logician improvements log: `pipeline/validation/pass-1-logician-dry-run-2026-05-18/improvements_log_pass_1.md`
* Per-charter Scout inventory: `pipeline/validation/pass-2-scout-dry-run-2026-05-18/per_charter_scout_inventory.md`
* CIC + CLC card files: `assets/cards/customer_identification/` + `assets/cards/capital_logic/`
