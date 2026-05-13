# Observability: Sonar Loop

## Capability Backlinks

- [Test Evidence and Sonar Evaluation](SPEC.md#test-evidence-and-sonar-evaluation)
- [Task Orchestration, Solution Synthesis, and Learning](SPEC.md#task-orchestration-solution-synthesis-and-learning)
- [Quality Gate Targeting and Policy](SPEC.md#quality-gate-targeting-and-policy)

## User Journey Alignment

Telemetry evidence in this document supports the approved pilot and scale proof package:

- Wave 2 `Q7=A`: gate progression and fallback evidence completeness are primary week-1 proof signals.
- Wave 3 `Q10=A`: governance proof package requires fallback, override validity, and completion-gate traces.
- Wave 3 `Q12=C`: operator-throughput with governed controls is the flagship month-1 outcome.

Journey detail references: [pilot-week1.md](userjourney/pilot-week1.md), [scale-month1.md](userjourney/scale-month1.md).

## QualityTrendMapping

**Type:** Mapping
**Concept ID:** `sonar-loop.QualityTrendMapping`

Maps stage outputs to cycle-level telemetry fields used to evaluate progressive gate improvements over repeated loops.

### Mapping Table

| Source                                                                                           | Target Telemetry Field                                                                                                                                        | Required         | Notes                                                                                    |
| ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------- | ---------------------------------------------------------------------------------------- |
| [DetermineTargetQualityGate](operations.md#determinetargetqualitygate) selected gate             | `targetGateLevel`                                                                                                                                             | yes              | Used for progression trend analysis                                                      |
| [DetermineTargetQualityGate](operations.md#determinetargetqualitygate) active pass               | `passId`                                                                                                                                                      | yes              | Binds stage events to child pass lineage                                                 |
| [DetermineTargetQualityGate](operations.md#determinetargetqualitygate) runtime mode              | `runtimeMode`                                                                                                                                                 | yes              | Captures explicit runtime-mode selection (`sandcastle`, `vscode-copilot`, `claude-code`) |
| Runtime fallback policy resolution for runtime-invoking stages                                   | `fallbackPolicyRef`, `fallbackOrderPolicyRef`, `availabilityProbeRefs`, `fallbackDecisionId`, `fallbackApprovedAt`, `fallbackExpiresAt`/`fallbackNonExpiring` | conditional      | Required when fallback is used (`runtimeMode != sandcastle`)                             |
| Runtime fallback decision metadata                                                               | `fallbackFrom`, `fallbackTo`, `fallbackReasonCode`, `fallbackResolverStage`, `fallbackEvaluatedAt`                                                            | conditional      | Required when fallback is used (`runtimeMode != sandcastle`)                             |
| [BuildAndImproveTestEvidence](operations.md#buildandimprovetestevidence) evidence summary        | `testEvidenceCoverage`                                                                                                                                        | yes              | Required to contextualize Sonar verdict                                                  |
| [EvaluateWithSonarQualityGate](operations.md#evaluatewithsonarqualitygate) gate result           | `gatePassRate`                                                                                                                                                | yes              | Primary quality gate trend signal                                                        |
| [BundleFindingsByContext](operations.md#bundlefindingsbycontext) grouped findings                | `findingDistribution`                                                                                                                                         | yes              | Supports category trend drift checks                                                     |
| [CreateAndExportRemediationTasks](operations.md#createandexportremediationtasks) export outcomes | `taskExportSuccessRate`                                                                                                                                       | yes              | Measures GitHub/Jira workflow health                                                     |
| [ApplyOperatorSelectionLearning](operations.md#applyoperatorselectionlearning) learning delta    | `learningImpactScore`                                                                                                                                         | yes              | Captures feedback-loop effectiveness                                                     |
| [ApplyModeControlCheckpoint](operations.md#applymodecontrolcheckpoint) checkpoint outcomes       | `checkpointOutcome`                                                                                                                                           | yes              | Tracks autonomous/assisted control behavior                                              |
| [ApplyModeControlCheckpoint](operations.md#applymodecontrolcheckpoint) stop compliance proof     | `stopRequestedAt`, `haltedAt`, `haltedCheckpointIndex`                                                                                                        | conditional      | Required when `checkpointOutcome=halt`                                                   |
| [ApplyModeControlCheckpoint](operations.md#applymodecontrolcheckpoint) completion gate evidence  | `activeExportRetryCount`, `exportDegradationThresholdBreached`, `riskAcceptedOverrideRef`, `riskAcceptedOverrideValidatedAt`                                  | yes/conditional  | Blocks completion unless explicit valid override is present under degradation            |
| [RecordCycleTelemetryTrend](operations.md#recordcycletelemetrytrend) stage event stream          | `stageEventRefs`                                                                                                                                              | yes              | Required stream for each pass stage                                                      |
| [RecordCycleTelemetryTrend](operations.md#recordcycletelemetrytrend) terminal summary            | `terminalCycleSummaryRef`                                                                                                                                     | yes for terminal | Required for completed parent cycle                                                      |

## CycleTelemetryEvent

**Type:** Event
**Concept ID:** `sonar-loop.CycleTelemetryEvent`

Represents one emitted stage-level telemetry row for pass execution, interaction, and stage outcome movement.

### Event Payload

| Field                              | Type                                                             | Required | Description                                                                                                                                              |
| ---------------------------------- | ---------------------------------------------------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| cycleId                            | string                                                           | yes      | Source [ExecutionCycle](domain.md#executioncycle).cycleId                                                                                                |
| passId                             | string                                                           | yes      | Source child pass identifier                                                                                                                             |
| stageName                          | string                                                           | yes      | Stage label in progressive loop (`gate`, `mapping`, `testing`, `evaluating`, `bundling`, `tasking`, `learning`, `checkpoint`)                            |
| mode                               | [OperationMode](domain.md#operationmode)                         | yes      | `autonomous` or `assisted`                                                                                                                               |
| runtimeMode                        | [ExecutionRuntimeMode](domain.md#executionruntimemode)           | yes      | `sandcastle`, `vscode-copilot`, or `claude-code`                                                                                                         |
| fallbackPolicyRef                  | string                                                           | no       | Required when runtime fallback is used (`runtimeMode != sandcastle`)                                                                                     |
| fallbackOrderPolicyRef             | string                                                           | no       | Optional approved per-project fallback-order policy artifact used during fallback resolution                                                             |
| availabilityProbeRefs              | string[]                                                         | no       | Required when runtime fallback is used                                                                                                                   |
| fallbackFrom                       | [ExecutionRuntimeMode](domain.md#executionruntimemode)           | no       | Required when runtime fallback is used                                                                                                                   |
| fallbackTo                         | [ExecutionRuntimeMode](domain.md#executionruntimemode)           | no       | Required when runtime fallback is used; must equal `runtimeMode`                                                                                         |
| fallbackReasonCode                 | [RuntimeFallbackReasonCode](domain.md#runtimefallbackreasoncode) | no       | Required when runtime fallback is used                                                                                                                   |
| fallbackDecisionId                 | string                                                           | no       | Required when runtime fallback is used                                                                                                                   |
| fallbackApprovedAt                 | string (ISO-8601)                                                | no       | Required when runtime fallback is used                                                                                                                   |
| fallbackExpiresAt                  | string (ISO-8601)                                                | no       | Required when runtime fallback is used and `fallbackNonExpiring=false`                                                                                   |
| fallbackNonExpiring                | boolean                                                          | no       | Required when runtime fallback is used                                                                                                                   |
| fallbackResolverStage              | [RuntimeInvokingStage](domain.md#runtimeinvokingstage)           | no       | Required when runtime fallback is used                                                                                                                   |
| fallbackEvaluatedAt                | string (ISO-8601)                                                | no       | Required when runtime fallback is used                                                                                                                   |
| targetGateLevel                    | [QualityGateLevel](domain.md#qualitygatelevel)                   | yes      | Gate level evaluated this cycle                                                                                                                          |
| gatePassRate                       | number                                                           | yes      | Passed gate conditions ratio                                                                                                                             |
| qualityTrendScore                  | number                                                           | yes      | Normalized trend delta                                                                                                                                   |
| interactionCount                   | integer                                                          | yes      | Operator-agent interaction count                                                                                                                         |
| taskOutcomeSummaryRef              | string                                                           | yes      | Task outcomes summary artifact                                                                                                                           |
| checkpointOutcome                  | [ModeControlOutcome](domain.md#modecontroloutcome)               | yes      | Continue/pause/halt/complete control result                                                                                                              |
| checkpointIndex                    | integer                                                          | yes      | Checkpoint index for correlation and audit                                                                                                               |
| checkpointEvaluatedAt              | string (ISO-8601)                                                | yes      | Decision timestamp used for override validity checks                                                                                                     |
| stopRequestedAt                    | string (ISO-8601)                                                | no       | Required when `checkpointOutcome=halt`                                                                                                                   |
| haltedAt                           | string (ISO-8601)                                                | no       | Required when `checkpointOutcome=halt`                                                                                                                   |
| haltedCheckpointIndex              | integer                                                          | no       | Required when `checkpointOutcome=halt`; must equal `checkpointIndex`                                                                                     |
| activeExportRetryCount             | integer                                                          | yes      | Number of active export retries at decision time                                                                                                         |
| exportDegradationThresholdBreached | boolean                                                          | yes      | Completion gate degradation signal                                                                                                                       |
| riskAcceptedOverrideRef            | string                                                           | no       | Required when completion proceeds under degraded export conditions; must reference [RiskAcceptanceOverride](domain.md#riskacceptanceoverride).overrideId |
| riskAcceptedOverrideValidatedAt    | string (ISO-8601)                                                | no       | Required when `riskAcceptedOverrideRef != null`; override validity-check timestamp                                                                       |
| emittedAt                          | string (ISO-8601)                                                | yes      | Event emission timestamp                                                                                                                                 |

## TerminalCycleSummary

**Type:** Event
**Concept ID:** `sonar-loop.TerminalCycleSummary`

Represents the terminal summary for a parent cycle after mode control authorizes completion.

### Summary Payload

| Field                    | Type                                                           | Required | Description                                               |
| ------------------------ | -------------------------------------------------------------- | -------- | --------------------------------------------------------- |
| cycleId                  | string                                                         | yes      | Parent [ExecutionCycle](domain.md#executioncycle).cycleId |
| terminalPassId           | string                                                         | yes      | Final child pass identifier                               |
| totalPassCount           | integer                                                        | yes      | Total number of child passes in the cycle                 |
| completionDecisionSource | [CompletionDecisionSource](domain.md#completiondecisionsource) | yes      | Must be `mode-control`                                    |
| gatePassRate             | number                                                         | yes      | Final gate pass ratio                                     |
| qualityTrendScore        | number                                                         | yes      | Final normalized trend score                              |
| emittedAt                | string (ISO-8601)                                              | yes      | Summary emission timestamp                                |

## Stage Telemetry Coverage Matrix

| Stage                   | Core telemetry requirement          | Mandatory fields                                                                                                                                                                                                    |
| ----------------------- | ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 gate targeting        | Gate selection stage event          | `cycleId`, `passId`, `targetGateLevel`, `mode`, `emittedAt`                                                                                                                                                         |
| 2 mapping               | Map coverage stage event            | `cycleId`, `passId`, `runtimeMode`, `mappingCoveragePct`, `emittedAt` (+ fallback fields when `runtimeMode!=sandcastle`)                                                                                            |
| 3 test evidence         | Test scope stage event              | `cycleId`, `passId`, `runtimeMode`, `testEvidenceCoverage`, `emittedAt` (+ fallback fields when `runtimeMode!=sandcastle`)                                                                                          |
| 4 sonar evaluation      | Gate verdict stage event            | `cycleId`, `passId`, `gatePassRate`, `findingCount`, `emittedAt`                                                                                                                                                    |
| 5 finding bundling      | Bundle distribution stage event     | `cycleId`, `passId`, `findingDistribution`, `emittedAt`                                                                                                                                                             |
| 6 task export           | Export status stage event           | `cycleId`, `passId`, `taskExportSuccessRate`, `emittedAt`                                                                                                                                                           |
| 7 solutions             | Candidate quality stage event       | `cycleId`, `passId`, `runtimeMode`, `candidateCoverage`, `emittedAt` (+ fallback fields when `runtimeMode!=sandcastle`)                                                                                             |
| 8 abstraction synthesis | Abstraction impact stage event      | `cycleId`, `passId`, `abstractionCoverage`, `emittedAt`                                                                                                                                                             |
| 9 learning update       | Learning feedback stage event       | `cycleId`, `passId`, `learningImpactScore`, `emittedAt`                                                                                                                                                             |
| 10 trend recording      | Stage telemetry consolidation event | `cycleId`, `passId`, `qualityTrendScore`, `gatePassRate`, `emittedAt`                                                                                                                                               |
| 11 mode control         | Checkpoint/completion stage event   | `cycleId`, `passId`, `runtimeMode`, `checkpointOutcome`, `checkpointIndex`, `checkpointEvaluatedAt`, `activeExportRetryCount`, `exportDegradationThresholdBreached`, `riskAcceptedOverrideValidatedAt`, `emittedAt` |
| terminal summary        | Parent-cycle terminal summary       | `cycleId`, `terminalPassId`, `totalPassCount`, `completionDecisionSource`, `emittedAt`                                                                                                                              |

## Metrics Derived From Telemetry

| Metric                                        | Definition                                                                                | Formula                                                                          | Target Direction |
| --------------------------------------------- | ----------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | ---------------- |
| `quality_gate_progress_rate`                  | Fraction of cycles that progress gate level without violation                             | `count(cycles with allowed upward progress)/count(cycles)`                       | increase         |
| `gate_pass_rate`                              | Fraction of gate conditions passed per cycle                                              | `passedConditions/totalConditions`                                               | increase         |
| `finding_density_per_kloc`                    | Normalized findings by code size                                                          | `totalFindings/(kloc)`                                                           | decrease         |
| `task_export_success_rate`                    | Fraction of tasks in explicit both-exported terminal state                                | `count(tasks where exportStatus=both-exported)/count(tasks)`                     | increase         |
| `runtime_mode_fallback_rate`                  | Fraction of passes that used non-default runtime mode                                     | `count(passes where runtimeMode!=sandcastle)/count(passes)`                      | stabilize/low    |
| `runtime_fallback_evidence_completeness_rate` | Fraction of fallback pass events that include all required fallback evidence fields       | `count(fallback events with complete evidence)/count(fallback events)`           | increase to 1.0  |
| `three_candidate_compliance_rate`             | Fraction of tasks with exactly three candidates                                           | `count(tasks with 3 candidates)/count(tasks)`                                    | increase to 1.0  |
| `abstraction_reuse_impact`                    | Average number of bundles solved per accepted abstraction                                 | `sum(bundleCoverage)/count(acceptedAbstractions)`                                | increase         |
| `learning_gain_rate`                          | Fraction of operator selections yielding positive quality delta                           | `count(qualityDelta>0)/count(selections)`                                        | increase         |
| `autonomous_checkpoint_halt_rate`             | Fraction of autonomous checkpoints ending in halt                                         | `count(autonomous checkpointOutcome=halt)/count(autonomous checkpoints)`         | stabilize/low    |
| `assisted_decision_wait_time`                 | Median wait time for assisted decision gates                                              | `median(decisionResolvedAt - decisionPromptAt)`                                  | decrease         |
| `stop_control_latency`                        | Time from stop request to halted transition                                               | `haltedAt - stopRequestedAt`                                                     | decrease         |
| `completion_gate_block_rate`                  | Fraction of completion requests blocked by active retries or degradation threshold        | `count(completionBlocked)/count(completionRequested)`                            | stabilize/low    |
| `completion_override_invalid_block_rate`      | Fraction of completion requests blocked due to invalid/revoked/expired override artifacts | `count(completionBlocked where overrideInvalid=true)/count(completionRequested)` | decrease         |

## Alert Conditions

| Alert                                       | Severity | Condition                                                                                                                                     | Primary Action                                                             |
| ------------------------------------------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| `quality_trend_regression`                  | P1       | `qualityTrendScore < 0` for 3 consecutive cycles                                                                                              | Hold gate progression and review bundles                                   |
| `telemetry_incomplete`                      | P0       | Missing mandatory telemetry fields at cycle completion                                                                                        | Block cycle completion                                                     |
| `task_export_degradation`                   | P1       | `task_export_success_rate < 0.8` in rolling 5 cycles                                                                                          | Trigger integration remediation                                            |
| `runtime_mode_fallback_policy_missing`      | P0       | `runtimeMode!=sandcastle` and missing fallback policy evidence                                                                                | Block stage execution and require policy artifact                          |
| `runtime_mode_fallback_evidence_incomplete` | P0       | `runtimeMode!=sandcastle` and one or more required fallback evidence fields are missing                                                       | Block stage execution and require complete deterministic fallback evidence |
| `checkpoint_policy_violation`               | P0       | stop requested but cycle not halted at next checkpoint                                                                                        | Force halt and flag policy incident                                        |
| `completion_gate_degradation_blocked`       | P1       | completion requested while (`activeExportRetryCount > 0` or `exportDegradationThresholdBreached=true`) and no valid `riskAcceptedOverrideRef` | Keep cycle in checkpoint hold and require explicit risk decision           |
| `completion_override_invalid`               | P1       | completion requested with `riskAcceptedOverrideRef` that is revoked or expired at `checkpointEvaluatedAt`                                     | Keep cycle in checkpoint hold and require valid override artifact          |

## Standard Evidence Checklist

- [ ] Cycle telemetry includes interactions, task outcomes, gate pass rate, and trend score.
- [ ] Every executed pass stage emits one [CycleTelemetryEvent](#cycletelemetryevent).
- [ ] Every completed parent cycle has one [TerminalCycleSummary](#terminalcyclesummary).
- [ ] Every pass event records explicit [ExecutionRuntimeMode](domain.md#executionruntimemode) with Sandcastle-default/fallback evidence.
- [ ] Every fallback pass event includes `fallbackPolicyRef`, `availabilityProbeRefs`, `fallbackDecisionId`, `fallbackApprovedAt`, and explicit `fallbackExpiresAt`/`fallbackNonExpiring`.
- [ ] Every fallback pass event includes `fallbackFrom`, `fallbackTo`, `fallbackReasonCode`, `fallbackResolverStage`, and `fallbackEvaluatedAt`.
- [ ] Autonomous/assisted checkpoints include explicit [ModeControlOutcome](domain.md#modecontroloutcome) values (`continue`, `pause`, `halt`, `complete`).
- [ ] Halt outcomes include `stopRequestedAt`, `haltedAt`, and `haltedCheckpointIndex` correlated to `checkpointIndex`.
- [ ] Assisted mode decision pauses include decision wait metrics.
- [ ] Task export telemetry includes GitHub and Jira status traces.
- [ ] Completion requests under export degradation include a valid `riskAcceptedOverrideRef` plus `riskAcceptedOverrideValidatedAt`, or remain blocked.
