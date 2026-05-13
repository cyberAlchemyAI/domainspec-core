# Pilot Week 1

## Scope

Pilot adoption model and evidence gates for the first week.

## Finalized Decisions (Wave 2)

| Question | Decision                                                                      | Implication                                                            |
| -------- | ----------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| Q5       | `B` - Two repos (one stable, one noisy)                                       | Pilot must prove robustness, not only happy-path quality loops         |
| Q6       | `A` - Assisted-first default mode                                             | Human checkpoints are primary trust mechanism during week 1            |
| Q7       | `A` - Week-1 proof is gate progression + fallback evidence completeness       | Governance signal quality is the principal pilot success family        |
| Q8       | `A` - Convert to month-1 scale on repeatable weekly loop with low rescue rate | Pilot-to-scale gate is operational repeatability with low intervention |

## Pilot Qualification

The pilot entry gate includes:

- one stable repository for baseline repeatability
- one noisy repository for stress behavior
- assisted-first staffing for decision checkpoints

Reference: [AssistedDecisionWorkflow](../workflows.md#assisteddecisionworkflow)

## Week-1 Success Evidence

Primary evidence family:

1. quality gate progression consistency
2. runtime fallback evidence completeness when fallback occurs

Key references:

- [QualityGateProgressionPolicy](../rules.md#qualitygateprogressionpolicy)
- [ExecutionProviderFallbackPolicy](../rules.md#executionproviderfallbackpolicy)
- [CycleTelemetryEvent](../observability.md#cycletelemetryevent)

## Pilot-to-Scale Conversion Gate

A pilot is ready for month-1 scale motion when:

- weekly loop execution is repeatable across both repositories
- manual rescue frequency remains low
- checkpoint outcomes remain explicit and auditable

See also: [ProgressiveQualityLoopWorkflow](../workflows.md#progressivequalityloopworkflow)
