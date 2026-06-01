# Arm B — Tilth WITH cards active (treatment)

## Purpose

The treatment arm. Tests whether card-driven runtime behavior produces better grant drafts than the Arm A baseline.

## System configuration

- Full Tilth pipeline at the same version + same router.yaml as Arm A.
- **Card loader enabled.** `pipeline.cards.loader.load_card` registers the relevant CIC + CLC card defaults with all consuming seats per the scenario's `cic_assignment` + `clc_assignment`.
- All card-derived behaviors active: Scout uses CIC search_vocabulary + funder_program_keywords + disqualifier_terms; Scribe uses CIC register_defaults + dialect_routing_table + admin_risk_term_register + CLC narrative_section_patterns; Judge uses CLC underwriting_criteria + scoring_weight_patterns + evidence_weights; Logician uses CIC compliance_burdens + CLC compliance_obligations; Report Generator uses CIC reporting_cadence_typical + CLC commitment_tracking_pattern.

## Execution recipe

For each test scenario at `pipeline/cards/eval/scenarios/<slug>.yaml`:

1. Spin up Tilth runtime with `CARDS_ENABLED=true` (env flag; v0.2 first wave default).
2. Loader reads + validates + signature-verifies + registers the relevant CIC + CLC cards per scenario assignment.
3. Submit scenario applicant + opportunity through the standard Tilth grant cycle.
4. Capture final draft + full audit log + Logician gate trace + card-load receipt.
5. Save artifact at `pipeline/cards/eval/results/<scenario_slug>/arm_b/`.
6. Strip applicant identity + system identity from draft before reviewer distribution (blinding).

## What gets measured

Same rubric as Arm A — identical dimensions, identical scoring scale, identical reviewer assignments. Per-dimension delta (Arm B − Arm A) is the primary outcome measure per the scenario's pre-registration.

## Card version pinning

Each Arm B execution records the SHA-256 canonical-bytes fingerprint of every loaded card. Results are reproducible against an exact card content version. If card content drifts between executions (Phase D research updates), the study results note the card version delta.
