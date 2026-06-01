# `pipeline/cards/eval/` — Card Effectiveness Test Harness

**Status at v7.0.11 LOCK candidate:** Directory scaffold landed. Content populates as study design + funding land (Milestone 7, v1.x scope per blueprint §18.19.6).

**Authoritative spec:** `pipeline/blueprint/v0.1/section_18_card_system.md` §18.19 (Card Effectiveness Test Harness — three-arm blind expert-reviewer study).

## What this directory exists to test

Per operator directive 2026-05-15 PM: **"the idea of the crads and whether they work has to be tested. ... part of needing funding is to pay experts to survey different answers."**

The core empirical question: **do Cards measurably improve grant-writing outcomes vs. Tilth-without-cards vs. an external industry-baseline LLM?**

## Three-arm design

| Arm | System | Directory |
|-----|--------|-----------|
| **A** | Tilth WITHOUT cards active (baseline) | `arms/arm_a_tilth_no_cards/` |
| **B** | Tilth WITH cards active (treatment) | `arms/arm_b_tilth_with_cards/` |
| **C** | Highest-rated frontier LLM, rudimentary prompting (industry reference) | `arms/arm_c_external_llm_rudimentary_prompt/` |

Same test scenarios → three drafts → blinded paid expert reviewer panel → per-dimension scoring + rank-order preference + likelihood-of-funding judgment.

## What is NOT in this directory

- **Operator historical wins are not used as test scenarios.** Per operator directive 2026-05-15: wrong target (survivor bias, single-applicant sample, private data leakage, measures card-mimicry-of-existing-skill rather than card-contribution-to-outcomes). Synthetic scenarios only at v0.1/v0.2; permission-based real-applicant scenarios are a v1.x extension contingent on explicit consent + IRB-equivalent review.
- **Judge-evaluates-Judge cross-check.** Circular — the cards' Judge underwriting criteria would evaluate drafts produced by a system using those same criteria. Reviewers are humans, not Tilth's Judge seat.

## Phase ordering

1. **v0.1 Beta LOCK (this LOCK):** directory scaffold lands; in-house pre-checks (schema validation, AST-lint, gate coverage) are live; expert study is unfunded.
2. **v0.2:** funding application(s) draft + submit (using Tilth's own grant-finder + grant-writer skills — meta-dogfooding); scenario authoring begins; reviewer-panel recruitment criteria drafted.
3. **v0.2-late / v1.x:** funding secured → reviewer panel recruited → blinded eval runs → results published regardless of finding direction.
4. **v1.x post-results:** if Arm B > Arm A → card investment continues + customer-facing materials gain empirical backing. If Arm B ≈ Arm A → card investment pauses or pivots. If Arm B < Arm A → card layer rolls back.

## Pre-registration discipline

Hypothesis + primary outcome measure + statistical-power calculation + analysis plan all pre-registered BEFORE reviewers see any drafts. No HARKing (hypothesizing after results known). Public results regardless of finding direction.

## In-house pre-checks (build-time, not the cards-work test)

Before the expensive paid-reviewer study runs on a candidate card set, these must pass:

- Schema validation against `pipeline/cards/_schema/`.
- AST-lint clean (R-CARDS-NO-COUPLING-FIELD scan returns zero findings).
- F-CARDS-COVERAGE-INCOMPLETE META gate PASS at production-environment evaluation.
- Fixture-stub round-trip load.
- Per-seat dependency coverage complete.

Pre-checks are necessary but **structurally insufficient** to answer the cards-work question. They confirm the cards are well-formed, not that they help.
