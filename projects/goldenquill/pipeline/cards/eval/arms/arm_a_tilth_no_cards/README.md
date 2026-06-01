# Arm A — Tilth WITHOUT cards active (baseline)

## Purpose

Controls for everything Tilth-specific except the card layer. Answers the question: *did the cards add value, or did Tilth already do this without them?*

## System configuration

- Full Tilth pipeline (Scout, Scribe, Editor, Judge, Logician, Red Team, Archivist) at the same version + same router.yaml as Arm B.
- **Card loader disabled.** `pipeline.cards.loader.load_card` returns early without registering any seat-default; consuming seats fall back to their pre-card default behavior (the v0.1 Beta posture before Phase B runtime context injection landed).
- Same model bindings, same prompts, same fixtures EXCEPT no card-driven Scout vocabulary, register defaults, dialect routing, evidence weights, etc.

## Execution recipe

For each test scenario at `pipeline/cards/eval/scenarios/<slug>.yaml`:

1. Spin up Tilth runtime with `CARDS_ENABLED=false` (env flag; lands at v0.2 first wave alongside CardRuntimeContext wiring).
2. Submit scenario applicant + opportunity through the standard Tilth grant cycle.
3. Capture final draft + full audit log + Logician gate trace.
4. Save artifact at `pipeline/cards/eval/results/<scenario_slug>/arm_a/`.
5. Strip applicant identity + system identity from draft before reviewer distribution (blinding).

## What gets measured

Reviewer scores per the rubric dimensions declared in the scenario's `review_dimensions` block. Per-dimension scores + rank-order preference + free-text comments + likelihood-of-funding judgment.

## What does NOT happen

- Card content does not influence Scout search vocabulary.
- Scribe register defaults fall back to v0.1 Beta pre-card defaults.
- Judge evaluates against generic rubric library only, not card-derived underwriting criteria.
- Report Generator uses generic commitment templates.
- Archivist does not tag the cycle with active CIC/CLC.
