# Methodology Profile: [Experiment ID and Title]

Status: draft
Version: 0.1.0

## Identity

- experiment_id: [E# or experiment-key]
- bundle_path: `experiments/<experiment-key>/`
- tier: foundation | full
- owner: [agent or operator]

## Framework Selection

- primary_framework: [for example Wohlin et al.]
- measurement_model: [for example GQM]
- triangulation_policy: [required/optional and how]

## Analysis Commitments

- required_steps:
  - [step]
  - [step]
- optional_steps:
  - [step]
  - [step]
- confidence_and_effect_policy: [CI type, effect size expectation]

## Validity Threat Plan

- internal_validity: [plan]
- external_validity: [plan]
- construct_validity: [plan]
- conclusion_validity: [plan]

## Claim Adjudication Policy

- evidence_strength_levels: strong | moderate | weak | insufficient | contradicted
- status_levels: supported | partially supported | insufficient evidence | contradicted
- upgrade_rule: [conditions]
- downgrade_rule: [conditions]

## Reproducibility Requirements

Mandatory metadata fields:
- experiment_id
- run_id
- timestamp
- model
- model_temperature
- system_prompt_hash
- operator

## Deviations

List any approved deviations from baseline methodology.

| Deviation | Rationale | Impact | Approval |
|---|---|---|---|
|  |  |  |  |

## Related Artifacts

- `experiments/<experiment-key>/protocol.md`
- `experiments/<experiment-key>/sources.md`
- `experiments/<experiment-key>/results/*.md`
- `definitions/METHODOLOGY-PROFILE-CONTRACT.md`
