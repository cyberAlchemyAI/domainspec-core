# Interfaces: Sonar Loop

## Capability Backlinks

- [Codebase Intelligence Mapping](SPEC.md#codebase-intelligence-mapping)
- [Test Evidence and Sonar Evaluation](SPEC.md#test-evidence-and-sonar-evaluation)
- [Task Orchestration, Solution Synthesis, and Learning](SPEC.md#task-orchestration-solution-synthesis-and-learning)
- [Quality Gate Targeting and Policy](SPEC.md#quality-gate-targeting-and-policy)

## User Journey Alignment

- Wave 2 assisted-first pilot (`Q6=A`) depends on explicit checkpoint interaction paths in [Internal: ModeControlInterface](#internal-modecontrolinterface).
- Wave 3 initial scale integration posture (`Q11=A`) keeps [External: GitHubWorkApiInterface (REST)](#external-githubworkapiinterface-rest) as the primary scale anchor while preserving Jira contract continuity.
- Wave 4 one-time per-repository packaging framing (`Q14=A`) aligns with repository-scoped task export payloads in both external work interfaces.

Journey detail references: [userjourney/README.md](userjourney/README.md), [scale-month1.md](userjourney/scale-month1.md), [packaging-pricing-and-growth.md](userjourney/packaging-pricing-and-growth.md).

## Internal: SandcastleAgentExecutionInterface

**Purpose:** Execute runtime-invoking stages (mapping, testing, and synthesis) using the governed runtime-mode model with Sandcastle as the default.

### Exposes

- [MapCodebaseIntelligence](operations.md#mapcodebaseintelligence)
- [BuildAndImproveTestEvidence](operations.md#buildandimprovetestevidence)
- [GenerateThreeCandidateSolutions](operations.md#generatethreecandidatesolutions)

### Methods

| Method                     | Input                                                                                                                                                                                                                                                                                                                         | Output                                                                                                         | Maps To                                                                                                                                                                                                                      |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `runMappingTask`           | `repositoryRef`, `scanScope`, `cycleId`, `runtimeMode`, `fallbackPolicyRef`, `fallbackOrderPolicyRef`, `availabilityProbeRefs`, `fallbackDecisionId`, `fallbackApprovedAt`, `fallbackExpiresAt`/`fallbackNonExpiring`, `fallbackFrom`, `fallbackTo`, `fallbackReasonCode`, `fallbackResolverStage`, `fallbackEvaluatedAt`     | map artifact references                                                                                        | [MapCodebaseIntelligence](operations.md#mapcodebaseintelligence)                                                                                                                                                             |
| `runTestUpgradeTask`       | `repositoryRef`, `testScope`, `cycleId`, `runtimeMode`, `fallbackPolicyRef`, `fallbackOrderPolicyRef`, `availabilityProbeRefs`, `fallbackDecisionId`, `fallbackApprovedAt`, `fallbackExpiresAt`/`fallbackNonExpiring`, `fallbackFrom`, `fallbackTo`, `fallbackReasonCode`, `fallbackResolverStage`, `fallbackEvaluatedAt`     | test evidence references                                                                                       | [BuildAndImproveTestEvidence](operations.md#buildandimprovetestevidence)                                                                                                                                                     |
| `runSolutionSynthesisTask` | `taskId`, `bundleRefs`, `patternCatalogRef`, `runtimeMode`, `fallbackPolicyRef`, `fallbackOrderPolicyRef`, `availabilityProbeRefs`, `fallbackDecisionId`, `fallbackApprovedAt`, `fallbackExpiresAt`/`fallbackNonExpiring`, `fallbackFrom`, `fallbackTo`, `fallbackReasonCode`, `fallbackResolverStage`, `fallbackEvaluatedAt` | candidate solution set                                                                                         | [GenerateThreeCandidateSolutions](operations.md#generatethreecandidatesolutions)                                                                                                                                             |
| `resolveRuntimeMode`       | `cycleId`, `passId`, `stage`, `fallbackPolicyRef`, `fallbackOrderPolicyRef`, `availabilityProbeRefs`                                                                                                                                                                                                                          | one of `sandcastle`, `vscode-copilot`, `claude-code` plus fallback decision evidence when non-default selected | [MapCodebaseIntelligence](operations.md#mapcodebaseintelligence), [BuildAndImproveTestEvidence](operations.md#buildandimprovetestevidence), [GenerateThreeCandidateSolutions](operations.md#generatethreecandidatesolutions) |

### Contract Notes

- Source baseline: [Sandcastle](https://github.com/mattpocock/sandcastle).
- Runtime payloads must preserve `cycleId` and task-level traceability fields.
- Supported runtime modes are [ExecutionRuntimeMode](domain.md#executionruntimemode) values: `sandcastle`, `vscode-copilot`, `claude-code`.
- Sandcastle is the default runtime mode.
- Any fallback runtime mode requires explicit strong policy evidence as defined by [ExecutionProviderFallbackPolicy](rules.md#executionproviderfallbackpolicy).
- Fallback governance applies to every runtime-invoking stage, including mapping, test evidence, solution synthesis, and approved future runtime stages.
- Fallback runtime mode resolution is deterministic with default order `sandcastle -> vscode-copilot -> claude-code`.
- Per-project override order is permitted only when `fallbackOrderPolicyRef` points to an approved deterministic and auditable policy artifact.

---

## External: SonarAnalysisInterface (REST+CLI)

**Purpose:** Run quality-gate evaluation and retrieve findings for bundling.

### Exposes

- [EvaluateWithSonarQualityGate](operations.md#evaluatewithsonarqualitygate)

### Methods

| Method                 | Input                                                   | Output                             | Maps To                                                                    |
| ---------------------- | ------------------------------------------------------- | ---------------------------------- | -------------------------------------------------------------------------- |
| `startAnalysis`        | `projectKey`, `branch`, `gateProfileId`, `evidenceRefs` | analysis task id                   | [EvaluateWithSonarQualityGate](operations.md#evaluatewithsonarqualitygate) |
| `getQualityGateStatus` | analysis task id                                        | gate status and condition verdicts | [EvaluateWithSonarQualityGate](operations.md#evaluatewithsonarqualitygate) |
| `listFindings`         | `projectKey`, `analysisId`                              | raw finding set                    | [BundleFindingsByContext](operations.md#bundlefindingsbycontext)           |

### Contract Notes

- Supports Sonar REST API queries and scanner CLI invocation.
- Gate status and finding payloads must be linked to [ExecutionCycle](domain.md#executioncycle).cycleId.

---

## External: GitHubWorkApiInterface (REST)

**Purpose:** Export remediation artifacts to GitHub issues/projects with API-first integration.

### Exposes

- [CreateAndExportRemediationTasks](operations.md#createandexportremediationtasks)

### Methods

| Method                        | Input                                | Output                | Maps To                                                                          |
| ----------------------------- | ------------------------------------ | --------------------- | -------------------------------------------------------------------------------- |
| `createEpicIssue`             | task summary bundle                  | issue id/url          | [CreateAndExportRemediationTasks](operations.md#createandexportremediationtasks) |
| `createStoryIssue`            | task item payload                    | issue id/url          | [CreateAndExportRemediationTasks](operations.md#createandexportremediationtasks) |
| `addIssueToProject`           | issue id, project id, field mappings | project item id       | [CreateAndExportRemediationTasks](operations.md#createandexportremediationtasks) |
| `applyEpicMetadataConvention` | issue id, convention payload         | metadata confirmation | [CreateAndExportRemediationTasks](operations.md#createandexportremediationtasks) |

### Contract Notes

- Uses GitHub REST API as authoritative path.
- GitHub epic model is represented as issue plus metadata conventions.
- Export payload must include `repositoryTaskRef`, `cycleId`, and source [FindingBundle](domain.md#findingbundle) references.
- MCP-only route is not sufficient for authoritative export.

---

## External: JiraWorkApiInterface (REST)

**Purpose:** Export remediation tasks as Jira epics/stories in API-first mode.

### Exposes

- [CreateAndExportRemediationTasks](operations.md#createandexportremediationtasks)

### Methods

| Method            | Input                                           | Output            | Maps To                                                                          |
| ----------------- | ----------------------------------------------- | ----------------- | -------------------------------------------------------------------------------- |
| `createEpic`      | epic payload with cycle metadata                | issue key         | [CreateAndExportRemediationTasks](operations.md#createandexportremediationtasks) |
| `createStory`     | story payload with parent epic and task context | issue key         | [CreateAndExportRemediationTasks](operations.md#createandexportremediationtasks) |
| `linkStoryToEpic` | story key, epic key                             | link confirmation | [CreateAndExportRemediationTasks](operations.md#createandexportremediationtasks) |

### Contract Notes

- Uses Jira Cloud REST API v3 as authoritative path.
- Payload must include source bundle refs and repository task refs.
- Export failures and retries must map to [TaskExportStatus](domain.md#taskexportstatus) transitions, including `retry-pending`, `retrying`, `export-partial`, and `both-exported`.

---

## Internal: SkillBundleInterface

**Purpose:** Evaluate, publish, reuse, and validate agnostic skill bundles used by coding agents.

### Exposes

- [ComposeAgnosticSkillBundle](operations.md#composeagnosticskillbundle)

### Methods

| Method                          | Input                                                                                                                                                                   | Output                                                                                 | Maps To                                                                |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| `evaluateRecompositionTriggers` | `mapId`, `capabilityScope`, `previousBundleRef`, `capabilityChangeSet`, `runtimePolicyChangeMarkers`, `mapDriftIndicators`, `forceRecompose`, `agnosticContractVersion` | deterministic branch decision (`recomposed` or `reused`) with `skillBundleDecisionRef` | [ComposeAgnosticSkillBundle](operations.md#composeagnosticskillbundle) |
| `publishBundle`                 | `mapId`, `capabilityScope`, `genericSkillRefs`, `version`, `skillBundleDecisionRef`                                                                                     | [SkillBundleProfile](domain.md#skillbundleprofile) reference                           | [ComposeAgnosticSkillBundle](operations.md#composeagnosticskillbundle) |
| `reuseLatestValidBundle`        | `capabilityScope`, `previousBundleRef`, `agnosticContractVersion`, `skillBundleDecisionRef`                                                                             | reused [SkillBundleProfile](domain.md#skillbundleprofile) reference                    | [ComposeAgnosticSkillBundle](operations.md#composeagnosticskillbundle) |
| `validateAgnosticity`           | skill bundle draft                                                                                                                                                      | pass/fail with reason                                                                  | [ComposeAgnosticSkillBundle](operations.md#composeagnosticskillbundle) |
| `resolveBundleForCycle`         | `cycleId`, `bundleId`                                                                                                                                                   | runtime bundle snapshot                                                                | [MapCodebaseIntelligence](operations.md#mapcodebaseintelligence)       |

### Contract Notes

- Recomposition is conditional: if no trigger is present and baseline validity checks pass, the interface must return `reused` instead of recomposing.
- Reuse path must validate latest-baseline agnosticity and capability coverage before attachment.
- Branch decision evidence (`skillBundleDecisionRef`) is required for telemetry and audit continuity.

---

## Internal: ModeControlInterface

**Purpose:** Enforce autonomous checkpoints, assisted decision gates, and stop control.

### Exposes

- [ApplyModeControlCheckpoint](operations.md#applymodecontrolcheckpoint)

### Methods

| Method                        | Input                                                                                                                                                                                                                                | Output                                                      | Maps To                                                                |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------- | ---------------------------------------------------------------------- |
| `evaluateCheckpoint`          | `cycleId`, `mode`, `runtimeMode`, `checkpointControl`, `telemetryEnvelopeRef`, `checkpointEvaluatedAt`, `activeExportRetryCount`, `exportDegradationThresholdBreached`, `riskAcceptedOverrideRef`, `riskAcceptedOverrideValidatedAt` | [ModeControlOutcome](domain.md#modecontroloutcome) decision | [ApplyModeControlCheckpoint](operations.md#applymodecontrolcheckpoint) |
| `requestStop`                 | `cycleId`, `stopReason`, `requestedAt`                                                                                                                                                                                               | stop request confirmation with persisted `stopRequestedAt`  | [ApplyModeControlCheckpoint](operations.md#applymodecontrolcheckpoint) |
| `resumeFromHaltedCheckpoint`  | `cycleId`, `resumeRequestedAt`                                                                                                                                                                                                       | resume acknowledgement                                      | [ApplyModeControlCheckpoint](operations.md#applymodecontrolcheckpoint) |
| `acknowledgeAssistedDecision` | `cycleId`, `decisionRef`                                                                                                                                                                                                             | approval token                                              | [ApplyModeControlCheckpoint](operations.md#applymodecontrolcheckpoint) |
| `decideCompletion`            | `cycleId`, `completionRequested`, `terminalCycleSummaryRef`, `checkpointEvaluatedAt`, `activeExportRetryCount`, `exportDegradationThresholdBreached`, `riskAcceptedOverrideRef`, `riskAcceptedOverrideValidatedAt`                   | authoritative completion decision or block reason           | [ApplyModeControlCheckpoint](operations.md#applymodecontrolcheckpoint) |

### Contract Notes

- Autonomous mode requires deterministic checkpoint logging.
- [CheckpointControl](domain.md#checkpointcontrol) is the authoritative stop signal source.
- Stop compliance proof requires explicit `stopRequestedAt`, `haltedAt`, and checkpoint-index correlation.
- Completion decisions are authoritative only when issued by mode control.
- Completion is blocked while active export retries exist or degradation threshold is breached unless explicit `riskAcceptedOverrideRef` is valid under [RiskAcceptanceOverrideValidityPolicy](rules.md#riskacceptanceoverridevaliditypolicy).
- Override validation requires active/non-expired (or explicit non-expiring) artifact state with persisted `riskAcceptedOverrideValidatedAt`.

---

## Internal: RiskAcceptanceOverrideRegistryInterface

**Purpose:** Resolve and validate governed [RiskAcceptanceOverride](domain.md#riskacceptanceoverride) artifacts referenced by completion-gate decisions.

### Exposes

- [ApplyModeControlCheckpoint](operations.md#applymodecontrolcheckpoint)
- [RecordCycleTelemetryTrend](operations.md#recordcycletelemetrytrend)

### Methods

| Method                          | Input                                                                                                 | Output                                                                                                                     | Maps To                                                                                                                                      |
| ------------------------------- | ----------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| `getOverrideById`               | `overrideId`                                                                                          | [RiskAcceptanceOverride](domain.md#riskacceptanceoverride) artifact                                                        | [ApplyModeControlCheckpoint](operations.md#applymodecontrolcheckpoint)                                                                       |
| `validateOverrideForCompletion` | `overrideId`, `checkpointEvaluatedAt`, `activeExportRetryCount`, `exportDegradationThresholdBreached` | `valid` or invalid reason (`expired`, `revoked`, `incomplete`, `scope-binding-missing`, `role-invalid`) plus `validatedAt` | [ApplyModeControlCheckpoint](operations.md#applymodecontrolcheckpoint), [RecordCycleTelemetryTrend](operations.md#recordcycletelemetrytrend) |
| `recordOverrideUsage`           | `overrideId`, `cycleId`, `passId`, `validatedAt`, `decisionRef`                                       | audit usage reference                                                                                                      | [RecordCycleTelemetryTrend](operations.md#recordcycletelemetrytrend)                                                                         |

### Contract Notes

- Override artifacts must include enum-governed approver role, approver principal, rationale, enum-governed scope type with required scope-binding fields, approval timestamp, explicit expiry/non-expiring lifecycle fields, and evidence/audit references.
- Validation semantics are governed by [RiskAcceptanceOverrideValidityPolicy](rules.md#riskacceptanceoverridevaliditypolicy).
- No default expiry duration is applied; expiry and revocation are explicit manual lifecycle actions.
- Revocation invalidation is deterministic and requires `revokedAt`, `revokedByPrincipal`, and `revocationReasonCode`.
- `riskAcceptedOverrideRef` is treated as a governed artifact identifier, not an unstructured free-form string.

---

## Internal: TelemetryLedgerInterface

**Purpose:** Persist cycle interactions, outcomes, and trend metrics for cross-cycle analysis.

### Exposes

- [RecordCycleTelemetryTrend](operations.md#recordcycletelemetrytrend)

### Methods

| Method                         | Input                                                                                                                                                                                                                                                                                                                                                                                                              | Output                         | Maps To                                                              |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------ | -------------------------------------------------------------------- |
| `appendStageTelemetryEvent`    | `cycleId`, `passId`, `runtimeMode`, `fallbackPolicyRef`, `fallbackOrderPolicyRef`, `availabilityProbeRefs`, `fallbackFrom`, `fallbackTo`, `fallbackReasonCode`, `fallbackDecisionId`, `fallbackApprovedAt`, `fallbackExpiresAt`/`fallbackNonExpiring`, `fallbackResolverStage`, `fallbackEvaluatedAt`, `skillBundleDecision`, `skillBundleDecisionRef`, `reusedBundleRef`/`recomposedBundleVersion`, stage payload | stage event row reference      | [RecordCycleTelemetryTrend](operations.md#recordcycletelemetrytrend) |
| `appendTerminalCycleSummary`   | `cycleId`, terminal summary payload                                                                                                                                                                                                                                                                                                                                                                                | terminal summary row reference | [RecordCycleTelemetryTrend](operations.md#recordcycletelemetrytrend) |
| `appendCycleTelemetryEnvelope` | [TelemetryEnvelope](domain.md#telemetryenvelope) payload including `runtimeMode`, fallback decision evidence fields, `skillBundleDecision`, `skillBundleDecisionRef`, `reusedBundleRef`/`recomposedBundleVersion`, `riskAcceptedOverrideRef`, and `riskAcceptedOverrideValidatedAt`                                                                                                                                | envelope row reference         | [RecordCycleTelemetryTrend](operations.md#recordcycletelemetrytrend) |
| `queryQualityTrend`            | `repositoryRef`, window                                                                                                                                                                                                                                                                                                                                                                                            | trend series                   | [RecordCycleTelemetryTrend](operations.md#recordcycletelemetrytrend) |
