---
date: 2026-04-20
mode: dialogue exploration (Cowork session)
operator: Josh
status: DEFERRED — future software development queue; not engineered; not in v0.1 scope
directive: "this was an exploration between you and I to include in future software development"
---

# Exploration — Variant Fan-out, Temperature Tuning, Team Building

## Origin

Dialogue between operator (Josh) and the Cowork agent following completion of the 7-card Logician v2.2 spec-card split (F-AMDT-01 through F-AMDT-07 per-gate cards). The conversation opened with operator's question: *"can we change temperatures on models to get different responses and ideas based on the organization, people, resources, needs, and the funder?"* It expanded from temperature to variant fan-out, then to team building, then to coop-scale matching, quality-floor invariants, and a structural observation about the imbalance between program-backlog and business-backlog capture disciplines.

Operator directive near session end: *"this is all deferred to a later date but mandatory to log for the future."* All items below are logged as future-software-development input — not spec'd for v0.1, not in the engineering queue.

---

## Items generated

### #1 Per-seat temperature tuning, funder- and context-conditioned

**The idea.** Each council seat (Scout, Scribe, Editor, Judge, Logician) has different functional needs around response diversity. Temperature should not be a single global knob. Propose a `router.yaml` extension: `temperature` field per seat-mode (e.g., `scribe.draft`, `scribe.polish`, `scout.discover`, `scout.verify`, `judge.score=0` locked, `editor.clarity` low, `logician` N/A since deterministic Python). Funder-conditioned layer: a `funder_temperature_profile` map in the rubric library applies deltas on top of seat defaults — a USDA-SCBGP reviewer wants crisp SMART outcomes (lower temp); a Surdna Foundation reviewer wants theory-of-change narrative (higher temp). Parallel axis to the existing dialect codebook (conservative / centrist / progressive / soul-fire), not folded into it.

**What it is NOT.** Not a replacement for structured prompt variation. Most of what varies between drafts is explicit framing instructions, not stochastic sampling. Temperature is fine-tuning inside a framing; prompt variation is the macro knob; cross-family (different model houses) is a third lever. Items #2 and #3 below use these other levers.

**Mandatory prerequisites before any non-zero temperature ships on Scribe.**
- A Scribe analog of F-VERDICT-CITATION-MISSING (F-AMDT-03). Every Scribe claim must cite RFA or PROJECT_CONTEXT verbatim, gated by Logician. Without this, temp-raising Scribe is just raising fabrication risk against Law 1 (RFA is truth) and Law 5 (applicant brings substance).
- A seed-availability preflight gate. If `temperature > 0`, the provider must expose a seed parameter; otherwise the session is unreplayable. Anthropic and OpenAI do; Groq partially; some don't. Gate fires at session init.

**Invariant.** Judge temperature stays at or near zero. Scoring reproducibility is the whole point of the 90+ Rubric; if Judge's temp varies, the same draft scores differently on replay and the two-audit cycle (L-005) loses its teeth. Logician is moot (deterministic Python).

**Open questions captured:**
1. Stage 1 (v0.1) or deferred? Additive to architecture but real surface area.
2. Do the three operational gears (Sparring Partner / Co-Pilot / Synthesizer) *become* the temperature lever (one knob) or stay orthogonal? — see item #3.
3. Within a cross-family Judge committee, is temperature diversity (one reviewer at 0.0, one at 0.3) useful for catching edge cases, or does strict determinism across all Judge seats remain the invariant? — see item #4.

**Addendum (#1a): expert-calibration requirement.** You cannot ship a (seat × funder × context × gear) temperature matrix without calibration data or domain expertise. First ship needs a *calibration discipline* — how Tilth LEARNS the right temperature for new funders, not just applies preset ones. Frame as a first-class problem, not a config oversight.

---

### #2 Variant fan-out workflow

**The idea.** Instead of one run per application, Tilth supports a *fan-out run* that produces N variant drafts for the same concept and surfaces them in a scoreboard for operator comparison. Grant equivalent of A/B testing framings before committing to one.

**Three flavors.**

- **Category fan-out.** Same concept, N category-framings. Operator example: *Pittsburgh Foundation has 5 categories but an org can only apply under 1. Org has 3 ideas; Tilth drafts them for different categories to see which looks strongest.* Scout scores category-fit for each of the funder's categories; Scribe drafts the top 2-3; Judge scores each against that category's rubric; operator picks winner.

- **Scope fan-out.** Same category, N scope-budget-outcome variants. Operator example: *SARE farmer research grant — parse out different ideas that meet the budget and goals.* Minimal / core / ambitious, each with its own budget line, timeline, SMART outcomes. Judge scores all N against the same rubric; scoreboard shows rubric score, budget fit, outcome density.

- **Angle fan-out.** Same substance, different narrative postures. Research-forward vs. applicant-history-forward vs. community-impact-forward. Same rubric, different voicing.

**Mechanisms that drive variation — in order of signal strength.**

1. Structured prompt variation — explicit framing instructions per variant. Deterministic, replayable, highest signal. Same model, same temperature, different angle. Most of the variation operator described is this.
2. Cross-family — run two variants through Anthropic Scribe and Groq Scribe. Different houses of voice.
3. Temperature — stochastic micro-variation inside a framing. Useful as fine-tuning, not as the macro knob.

**Architectural fit.**

- Each variant is its own RunState with a shared `run_group_id`. Law 3 (org isolation) untouched — same org, same PROJECT_CONTEXT.
- Law 2 (boundary drift) is the new watch. Generating category variants tempts stretching the concept to fit each. Scout's category-fit score becomes a threshold gate — below `fit_floor`, Scribe doesn't draft the variant. Prevents inflating "options" with bad-fit drafts.
- Law 5 holds — same applicant substance across variants. No invented data per-variant.
- Judge scores each variant independently, fresh invocation, no cross-variant anchoring.
- New artifact: a *scoreboard* per `run_group_id` — rubric score, category-fit score, budget fit, word-count fit, SMART-outcome density. Headless markdown table, consistent with no-UI-for-v0.1.
- Rejected variants don't vanish — they go to `pipeline/variants/<run_group_id>/rejected/` so institutional memory learns which framings the operator rejects and why.

**Gotchas.**
- Token cost scales with N. BYOK makes it transparent; Scout's fit-floor gate is the cost control.
- Seed-per-variant mandatory if any seat runs at `temp > 0` (from #1's seed-availability gate).
- Judge blindness — Judge must not see variants 1-2's scores when scoring variant 3.

**Open questions captured:**
1. Stage 1 (v0.1) or defer? Real surface area — RunState grouping, scoreboard format, rejected-variants storage.
2. Promote Scout to emit a 0-100 numerical fit score alongside its VERIFIED_FIT / UNVERIFIED / VERIFIED_NOT_FIT label, or add a separate "category-fit estimator" that runs only when fan-out is invoked? — see item #5.

---

### #3 Gear-to-temperature collapse decision

**The question.** The three operational gears already imply temperature:
- Sparring Partner — high (you want options)
- Co-Pilot — moderate (you want execution)
- Synthesizer — low (you want decision-quality)

Do gears *become* the temperature lever (one knob, not two), or stay orthogonal so combinations like "Co-Pilot mode, high-temp Scribe" are expressible?

**Trade.** One knob is simpler and keeps the gears semantically meaningful. Orthogonal gives more expressive power but creates more surface area for operator confusion.

**Not decided.** Logged as an item to decide before or during the first ship of temperature tuning.

---

### #4 Judge cross-family temperature diversity

**The question.** When Judge is cross-family-reviewed (the standard committee mode, per L-003), should the reviewers run at diverse temperatures — one at 0.0, one at 0.3 — to catch edge cases that a fully deterministic reviewer would miss? Or is strict determinism across all Judge seats the invariant?

**Tension.** Diversity might surface edge cases. Determinism preserves the replay-on-demand property that makes Judge scoring auditable.

**Not decided.** Logged as item to decide jointly with #1 before Judge temperature policy locks.

---

### #5 Scout numerical fit-score emission

**The idea.** Scout currently emits categorical labels: VERIFIED_FIT / UNVERIFIED / VERIFIED_NOT_FIT / VERIFICATION_FAILED. Variant fan-out (#2) needs a numerical fit score (0-100) to threshold on (the `fit_floor` gate). Two paths:

- Promote Scout's VERIFY stage to emit a continuous score alongside the existing label. Affects more pipeline consumers, wider test surface.
- Add a separate "category-fit estimator" that runs only when fan-out is invoked. Narrower blast radius, slight redundancy.

**Dependency.** Blocker for #2 (fan-out). No fan-out ship without this.

---

### #6 In-house team building from network data

**The idea.** RFAs mandate structural roles (SARE Partnership = producer + researcher + educator; SARE Farmer = farmer + technical advisor; USDA SCBGP often wants an evaluation partner). Tilth could:

1. Parse slot requirements from the RFA (new Scout capability).
2. Surface candidates from the applicant's network — PROJECT_CONTEXT partners, past-grant collaborators, prior-work contacts — matched against slot requirements.
3. Flag gaps early — "SARE requires a technical advisor with research credentials; your current network has zero matches" with weeks of lead time to recruit, not days.
4. Role-fit memory — Joe filled tech advisor on VAPG 2025, app was funded → boost his weight for similar slots going forward. Lives in institutional memory.

**Biggest gotcha: Law 3.** Drawing from OTHER clients' networks is a silent cross-contamination vector. Joe advises MycoSymbiotics — can Tilth propose Joe for Mystic Mamas's SARE team? Only if Joe is tagged "composable" under the consent tiers already in the Golden Quill architecture (my-eyes-only / matchable-to-opportunities / composable-with-others). This is a natural fit for that infrastructure — team-building becomes one of the concrete mechanisms that makes those consent tiers matter. Without team-building as a use case, the consent tiers are architecturally elegant but thinly justified.

**Intersects with fan-out (#2).** Scope variants need different team sizes — minimal-scope SARE might need 2 people, ambitious-scope needs 5. Fan-out + team building = "for each scope variant, assemble the team, score rubric fit including team completeness." Combined system attacks the three hardest parts of a submission in one move: right frame, right team, right scope.

**Dependencies that must land first:**
- Structured contact data model per org. PROJECT_CONTEXT today has freeform partner lists, not schema. Team building needs real schema (name, role credentials, affiliations, consent tier, past-role history).
- RFA role-slot parser in Scout (new Scout capability, not in current spec).
- Cross-org consent-tier enforcement implemented in the data layer, not just described in architecture.

**Stage fit.** Earliest is Stage 2 — requires both the structured contact model and cross-org consent tier enforcement, neither of which is in v0.1.

---

### #7 85%+ rubric-floor invariant

**The idea.** Tilth never presents a draft below 85% rubric score. Revision loop iterates until it hits; scoreboard surfaces variants in descending score order. Makes it a hard quality promise, not a nice-to-have.

**Connection to existing architecture.** Logician's revision-loop counter today enforces a ceiling on iteration count. The floor (minimum acceptable score before surfacing to operator) is a separate lever. Needs to be added as a new gate — something like F-REVISION-FLOOR-UNMET.

**"Only up from there."** Operator's phrasing implies a feedback loop: every funded grant raises the floor for the next round, because institutional memory learns what 85% actually looked like when it won. Over time, the floor drifts upward as a function of win-rate — not a fixed constant. This is a lessons-accumulation pattern, consistent with the existing `lessons.md` / `pipeline/institutional_memory/lessons.json` discipline.

---

### #8 Cross-Golden-Quill coop matching

**The idea.** Team building (#6) scaled across multiple Golden Quill owners who opt into a coop structure. Same consent-tier gating as within-workspace team building (my-eyes-only / matchable / composable), but the data-sharing surface is now MaatAI territory.

**Stage fit.** Stage 5 only. MaatAI on the Sovereign Node is the substrate.

**Why log it now.** So MaatAI design accommodates it when Stage 5 stands up, rather than discovering the use case after coop-level data-sharing primitives are already built for other purposes.

---

## Cross-cut: combinatorial pruning discipline

Items #1, #2, and #6 combine combinatorially. The in-house exploration operator described — *"different teams with different skills and draft different grant ideas that are graded and the rough drafts are presented in order of strength"* — looks like N framings × M teams × K scopes × T temperature profiles. Exhaustive fan-out (3 × 3 × 3 × 2 = 54 drafts per application) is prohibitive even at BYOK.

**Design constraint.** Fit-floor gating + iterative refinement, not exhaustive search. You don't generate all 54 — Scout's fit-floor prunes framings, past-performance prunes team candidates, budget-fit prunes scopes, and only then does temperature variation get applied to the top survivors. This pruning discipline is itself a feature to design before any of the combinators ship.

---

## Structural observation: business-backlog vs. program-backlog imbalance

Operator surfaced this as a concern near session end: *"I feel like we have a business plan which is the future of the Golden Quill and its business. but we have been capturing lots of ideas that are more structural or add on components that require more building more talent and is in the program the code the structure vs the business."*

**Diagnosis.**
- `pipeline/engineering/spec_cards/` — engineering queue. Well-disciplined. Midas dispatch territory. Grows fast because engineering gates have forcing functions (tests must pass, LOCKs must commit).
- `Sovereign_Node_Handoff/project_docs/Sovereign_Node_Master_Plan_v2.odt` — business plan and product vision. Relatively static.
- **Gap 1** (filled by this roadmap folder): deferred product features between "engineering task" and "business vision." These go under `pipeline/roadmap/`.
- **Gap 2** (still open): nowhere for *live* business questions — pricing model, partner-by-application contract template, CDFI / foundation infrastructure pitch, Stage 4 partner roster, Stage 5 coop governance board, how Golden Quill gets sold vs. leased vs. coop-owned.

The code/program backlog outpaces the business backlog because engineering has forcing functions and business questions don't. Nothing fails if you don't answer "what's the Stage 1 contract template?" today — so it stays in your head and the asymmetry grows.

**Proposal pending operator decision.** Parallel `business_backlog/` folder (workspace root or under `Sovereign_Node_Handoff/`) — one file per live business question, same log-and-surface discipline as this roadmap. No commitment to decide, just capture so it doesn't evaporate. Complement to the master plan doc, not a replacement.

---

## What to do with this doc

- **Next time operator expands scope at a Stage transition:** read this doc. Each item has enough context to make a feature-level decision (yes/no/defer further).
- **If operator green-lights any item for engineering:** split the relevant section into a per-item file under `pipeline/roadmap/deferred/`, then spawn a spec card in `pipeline/engineering/spec_cards/` when ready to dispatch.
- **If new exploration dialogue extends this thread:** append a new exploration doc with the date in filename; cross-link from this one's "Related explorations" section (to be added when the second exploration lands).
- **For the business-backlog gap:** if operator decides to stand up `business_backlog/`, move the Structural Observation section above into that folder's README as the rationale.

---

## Quick reference: deferred items by Stage fit

| # | Item | Earliest Stage | Hard prerequisite |
|---|------|----------------|-------------------|
| #1 | Per-seat temperature tuning | Stage 1 possible, likely deferred | Scribe citation gate + seed-availability gate + calibration discipline |
| #1a | Expert-calibration for temperature | Pairs with #1 | — |
| #2 | Variant fan-out workflow | Stage 1 possible, likely deferred | Scout numerical fit score (#5) |
| #3 | Gear-to-temperature collapse | Decide before shipping #1 | — |
| #4 | Judge cross-family temp diversity | Decide before shipping #1 | — |
| #5 | Scout numerical fit-score | Prerequisite for #2 | Scout VERIFY stage extension |
| #6 | In-house team building | Stage 2 | Structured contact model + cross-org consent tier enforcement |
| #7 | 85%+ rubric-floor invariant | Stage 1 candidate | New Logician gate (F-REVISION-FLOOR-UNMET) |
| #8 | Cross-Golden-Quill coop matching | Stage 5 | MaatAI substrate |

---

*Exploration v1 — 2026-04-20 — logged per operator directive; status DEFERRED; no engineering work authorized.*
