# Domain: Sonar Loop

## Capability Backlinks

- [Quality Gate Targeting and Policy](SPEC.md#quality-gate-targeting-and-policy)
- [Codebase Intelligence Mapping](SPEC.md#codebase-intelligence-mapping)
- [Test Evidence and Sonar Evaluation](SPEC.md#test-evidence-and-sonar-evaluation)
- [Task Orchestration, Solution Synthesis, and Learning](SPEC.md#task-orchestration-solution-synthesis-and-learning)

## User Journey Context

Commercialization decisions that shape how this domain model is explained to evaluators/operators are captured in [userjourney/README.md](userjourney/README.md). Domain contracts remain authoritative in this document.

- Evaluator day 0-day 1 assumptions: [evaluator-day0-day1.md](userjourney/evaluator-day0-day1.md)
- Pilot and scale positioning: [pilot-week1.md](userjourney/pilot-week1.md), [scale-month1.md](userjourney/scale-month1.md)
- Packaging and growth framing: [packaging-pricing-and-growth.md](userjourney/packaging-pricing-and-growth.md)

## Entities

### ExecutionCycle

Represents a hybrid progressive loop with one parent cycle identifier and one or more child pass identifiers.

| Field                    | Type                                                  | Required | Description                                                                                                                                                 |
| ------------------------ | ----------------------------------------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| cycleId                  | string                                                | yes      | Stable parent identifier for [ExecutionCycle](#executioncycle)                                                                                              |
| activePassId             | string                                                | yes      | Active child pass identifier within the parent cycle                                                                                                        |
| passIds                  | string[]                                              | yes      | Ordered list of all child pass identifiers executed under this cycle                                                                                        |
| passSequence             | integer                                               | yes      | Monotonic count of executed child passes                                                                                                                    |
| repositoryRef            | string                                                | yes      | Ingested TypeScript repository reference                                                                                                                    |
| mode                     | [OperationMode](#operationmode)                       | yes      | Execution mode (`autonomous` or `assisted`)                                                                                                                 |
| runtimeMode              | [ExecutionRuntimeMode](#executionruntimemode)         | yes      | Runtime mode used for mapping/testing/synthesis (`sandcastle` default order head; per-project override order allowed only through approved policy artifact) |
| state                    | [CycleState](#cyclestate)                             | yes      | Current cycle lifecycle state                                                                                                                               |
| targetGate               | [QualityGateProfile](#qualitygateprofile)             | yes      | Gate profile selected for this cycle                                                                                                                        |
| codebaseMapRef           | string                                                | yes      | Pointer to current [CodebaseKnowledgeMap](#codebaseknowledgemap) snapshot                                                                                   |
| findingBundleRefs        | string[]                                              | yes      | Ordered references to [FindingBundle](#findingbundle) outputs                                                                                               |
| taskRefs                 | string[]                                              | yes      | Ordered references to [RemediationTask](#remediationtask) outputs                                                                                           |
| checkpointControl        | [CheckpointControl](#checkpointcontrol)               | yes      | Checkpoint/stop policy status for the cycle                                                                                                                 |
| modeControlOutcome       | [ModeControlOutcome](#modecontroloutcome)             | yes      | Last explicit mode-control outcome (`continue`, `pause`, `halt`, `complete`)                                                                                |
| sonarRetryAttemptCount   | integer                                               | yes      | Number of [EvaluateWithSonarQualityGate](operations.md#evaluatewithsonarqualitygate) retries consumed (`0` or `1`)                                          |
| sonarRetryRemediationRef | string                                                | no       | Required when [ExecutionCycle](#executioncycle).sonarRetryAttemptCount is `1`                                                                               |
| telemetryEnvelope        | [TelemetryEnvelope](#telemetryenvelope)               | yes      | Interaction, outcome, and trend telemetry summary                                                                                                           |
| completionDecisionSource | [CompletionDecisionSource](#completiondecisionsource) | yes      | Authoritative source for terminal completion decisions                                                                                                      |
| startedAt                | string (ISO-8601)                                     | yes      | Cycle start timestamp                                                                                                                                       |
| terminalAt               | string (ISO-8601)                                     | no       | Required when [ExecutionCycle](#executioncycle).state is `completed` or `failed`                                                                            |

**Lifecycle:** See [CycleStateMachine](rules.md#cyclestatemachine)
**Operations:** [DetermineTargetQualityGate](operations.md#determinetargetqualitygate), [RecordCycleTelemetryTrend](operations.md#recordcycletelemetrytrend), [ApplyModeControlCheckpoint](operations.md#applymodecontrolcheckpoint)

**Cardinality:** One parent [ExecutionCycle](#executioncycle) owns one or more child pass identifiers (`count(passIds) >= 1`), and `activePassId` must always be a member of `passIds`. State `halted` is a resumable checkpoint-hold state, not a terminal state.

---

### QualityGateProfile

Defines the selected gate level and threshold vectors that Sonar must satisfy for cycle completion.

| Field                    | Type                                  | Required | Description                                                                                                                |
| ------------------------ | ------------------------------------- | -------- | -------------------------------------------------------------------------------------------------------------------------- |
| gateProfileId            | string                                | yes      | Stable identifier for [QualityGateProfile](#qualitygateprofile)                                                            |
| level                    | [QualityGateLevel](#qualitygatelevel) | yes      | Named target level (`baseline`, `moderate`, `strict`, `hardened`)                                                          |
| reliabilityThreshold     | string                                | yes      | Required reliability rating threshold                                                                                      |
| securityThreshold        | string                                | yes      | Required security rating threshold                                                                                         |
| maintainabilityThreshold | string                                | yes      | Required maintainability rating threshold                                                                                  |
| coverageThresholdPct     | number                                | yes      | Minimum code coverage percentage                                                                                           |
| duplicationThresholdPct  | number                                | yes      | Maximum code duplication percentage                                                                                        |
| progressionFromLevel     | [QualityGateLevel](#qualitygatelevel) | no       | Prior level used for progression validation                                                                                |
| rollbackReason           | string                                | no       | Mandatory persisted rationale when level is downgraded from [QualityGateProfile](#qualitygateprofile).progressionFromLevel |

**Operations:** [DetermineTargetQualityGate](operations.md#determinetargetqualitygate), [EvaluateWithSonarQualityGate](operations.md#evaluatewithsonarqualitygate)

---

### CodebaseKnowledgeMap

Captures structured analysis of the TypeScript codebase used to drive testing, finding context, and candidate solutions.

| Field               | Type              | Required | Description                                                         |
| ------------------- | ----------------- | -------- | ------------------------------------------------------------------- |
| mapId               | string            | yes      | Stable identifier for [CodebaseKnowledgeMap](#codebaseknowledgemap) |
| repositoryRef       | string            | yes      | Source repository reference                                         |
| dependencyGraphRef  | string            | yes      | Dependency graph artifact reference                                 |
| useCaseCatalogRef   | string            | yes      | Use-case extraction artifact reference                              |
| ruleCatalogRef      | string            | yes      | Existing rules and policy artifact reference                        |
| patternCatalogRef   | string            | yes      | Existing/new patterns artifact reference                            |
| moduleMapRef        | string            | yes      | Module boundary map artifact reference                              |
| apiSurfaceRef       | string            | yes      | Internal/external API inventory artifact reference                  |
| architectureMapRef  | string            | yes      | Architecture topology artifact reference                            |
| libraryInventoryRef | string            | yes      | Third-party libraries and risk profile reference                    |
| generatedAt         | string (ISO-8601) | yes      | Map generation timestamp                                            |

**Operations:** [MapCodebaseIntelligence](operations.md#mapcodebaseintelligence), [ComposeAgnosticSkillBundle](operations.md#composeagnosticskillbundle)

---

### FindingBundle

Groups Sonar findings into actionable context bundles by category, location, and shared cause.

| Field               | Type                                    | Required | Description                                             |
| ------------------- | --------------------------------------- | -------- | ------------------------------------------------------- |
| bundleId            | string                                  | yes      | Stable identifier for [FindingBundle](#findingbundle)   |
| cycleId             | string                                  | yes      | Parent [ExecutionCycle](#executioncycle).cycleId        |
| category            | [FindingCategory](#findingcategory)     | yes      | Dominant finding category                               |
| contextTag          | [FindingContextTag](#findingcontexttag) | yes      | Controlled taxonomy key resolved with precedence policy |
| findingRefs         | string[]                                | yes      | Sonar finding references grouped in this bundle         |
| severitySummary     | string                                  | yes      | Aggregated severity summary                             |
| rootCauseHypothesis | string                                  | yes      | Candidate shared root cause                             |

**Operations:** [EvaluateWithSonarQualityGate](operations.md#evaluatewithsonarqualitygate), [BundleFindingsByContext](operations.md#bundlefindingsbycontext)

---

### RemediationTask

Represents one remediation task generated from finding bundles and prepared for repository, GitHub, and Jira workflows.

| Field              | Type                                      | Required | Description                                                    |
| ------------------ | ----------------------------------------- | -------- | -------------------------------------------------------------- |
| taskId             | string                                    | yes      | Stable identifier for [RemediationTask](#remediationtask)      |
| cycleId            | string                                    | yes      | Parent [ExecutionCycle](#executioncycle).cycleId               |
| title              | string                                    | yes      | Task title                                                     |
| bundleRefs         | string[]                                  | yes      | Source [FindingBundle](#findingbundle) references              |
| candidateSolutions | [SolutionCandidate](#solutioncandidate)[] | yes      | Exactly three candidate solution options                       |
| abstractionRefs    | string[]                                  | no       | Cross-task abstraction proposal references                     |
| githubExportRef    | string                                    | no       | External GitHub export identifier                              |
| jiraExportRef      | string                                    | no       | External Jira export identifier                                |
| exportStatus       | [TaskExportStatus](#taskexportstatus)     | yes      | Current export status                                          |
| exportAttemptCount | integer                                   | yes      | Number of export attempts across initial and retry transitions |

**Operations:** [CreateAndExportRemediationTasks](operations.md#createandexportremediationtasks), [GenerateThreeCandidateSolutions](operations.md#generatethreecandidatesolutions), [SynthesizeCrossSmellAbstractions](operations.md#synthesizecrosssmellabstractions)

---

### LearningMemory

Stores operator-selected solutions and measured outcomes to improve future candidate ranking and abstraction choices.

| Field               | Type              | Required | Description                                                  |
| ------------------- | ----------------- | -------- | ------------------------------------------------------------ |
| learningId          | string            | yes      | Stable identifier for [LearningMemory](#learningmemory)      |
| cycleId             | string            | yes      | Source [ExecutionCycle](#executioncycle).cycleId             |
| taskId              | string            | yes      | Source [RemediationTask](#remediationtask).taskId            |
| selectedCandidateId | string            | yes      | Identifier of chosen [SolutionCandidate](#solutioncandidate) |
| selectionReason     | string            | yes      | Operator-provided rationale                                  |
| observedOutcome     | string            | yes      | Outcome after implementation/verification                    |
| qualityDelta        | number            | yes      | Normalized quality delta attributed to selection             |
| capturedAt          | string (ISO-8601) | yes      | Capture timestamp                                            |

**Operations:** [ApplyOperatorSelectionLearning](operations.md#applyoperatorselectionlearning), [GenerateThreeCandidateSolutions](operations.md#generatethreecandidatesolutions)

---

### SkillBundleProfile

Defines the agnostic skill bundle provided to coding agents for this feature loop.

| Field            | Type     | Required | Description                                                     |
| ---------------- | -------- | -------- | --------------------------------------------------------------- |
| bundleId         | string   | yes      | Stable identifier for [SkillBundleProfile](#skillbundleprofile) |
| capabilityScope  | string[] | yes      | Capability-level responsibilities covered by the bundle         |
| genericSkillRefs | string[] | yes      | Agent-agnostic skill references                                 |
| requiredInputs   | string[] | yes      | Required input artifact categories                              |
| outputContracts  | string[] | yes      | Expected output artifact categories                             |
| version          | string   | yes      | Skill bundle semantic version                                   |

**Operations:** [ComposeAgnosticSkillBundle](operations.md#composeagnosticskillbundle)

---

### RiskAcceptanceOverride

Represents a governed risk-acceptance artifact that can authorize completion under export degradation when explicit validity checks pass.

| Field                    | Type                                                                      | Required | Description                                                                                             |
| ------------------------ | ------------------------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------- |
| overrideId               | string                                                                    | yes      | Stable identifier for [RiskAcceptanceOverride](#riskacceptanceoverride)                                 |
| approverRole             | [RiskAcceptanceApproverRole](#riskacceptanceapproverrole)                 | yes      | Governance role enum of approver                                                                        |
| approverPrincipal        | string                                                                    | yes      | Approver identity principal                                                                             |
| rationale                | string                                                                    | yes      | Explicit reason for accepting completion risk                                                           |
| overrideScopeType        | [RiskAcceptanceOverrideScopeType](#riskacceptanceoverridescopetype)       | yes      | Scope type enum for deterministic override binding                                                      |
| scopeCycleId             | string                                                                    | no       | Required when `overrideScopeType in {cycle,pass}`; must match [ExecutionCycle](#executioncycle).cycleId |
| scopePassId              | string                                                                    | no       | Required when `overrideScopeType=pass`; must match one [ExecutionCycle](#executioncycle).passIds member |
| scopeGateConditionFamily | [QualityGateConditionFamily](#qualitygateconditionfamily)                 | no       | Required when `overrideScopeType=gate-condition-family`                                                 |
| approvedAt               | string (ISO-8601)                                                         | yes      | Approval timestamp                                                                                      |
| expiresAt                | string (ISO-8601)                                                         | no       | Required when `nonExpiring=false`; no implicit default duration is applied                              |
| nonExpiring              | boolean                                                                   | yes      | Explicit lifecycle choice; must be set manually at approval time                                        |
| evidenceRef              | string                                                                    | yes      | Evidence artifact reference proving approval rationale and context                                      |
| auditRef                 | string                                                                    | yes      | Audit ledger/reference id for governance traceability                                                   |
| status                   | [RiskAcceptanceOverrideStatus](#riskacceptanceoverridestatus)             | yes      | Lifecycle status for validity checks                                                                    |
| revokedAt                | string (ISO-8601)                                                         | no       | Required when `status=revoked`                                                                          |
| revokedByPrincipal       | string                                                                    | no       | Required when `status=revoked`; identity principal that performed revocation                            |
| revocationReasonCode     | [RiskAcceptanceRevocationReasonCode](#riskacceptancerevocationreasoncode) | no       | Required when `status=revoked`                                                                          |

**Operations:** [ApplyModeControlCheckpoint](operations.md#applymodecontrolcheckpoint), [RecordCycleTelemetryTrend](operations.md#recordcycletelemetrytrend)

**Lifecycle policy:** No default expiry duration is applied. Override expiry and revocation are manual governance actions with deterministic validation semantics.

**Validity:** `status=active and (nonExpiring=true or expiresAt > checkpointEvaluatedAt)`

## Value Objects

### SolutionCandidate

| Field          | Type     | Constraint                                                   |
| -------------- | -------- | ------------------------------------------------------------ |
| candidateId    | string   | Non-empty and unique per [RemediationTask](#remediationtask) |
| strategyType   | string   | Must classify as `established`, `hybrid`, or `new-pattern`   |
| summary        | string   | Non-empty                                                    |
| patternRefs    | string[] | Must reference existing or proposed pattern artifacts        |
| expectedImpact | string   | Must include quality gate impact statement                   |
| riskNotes      | string   | Non-empty risk statement                                     |

**Equality:** Two [SolutionCandidate](#solutioncandidate) values are equal when `candidateId`, `strategyType`, and `summary` match.

---

### CheckpointControl

| Field                              | Type                      | Constraint                                                                                                                                                                                                                                   |
| ---------------------------------- | ------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| checkpointPolicy                   | string                    | Must reference [AutonomousCheckpointAndStopPolicy](rules.md#autonomouscheckpointandstoppolicy)                                                                                                                                               |
| checkpointIndex                    | integer                   | Non-negative and monotonic                                                                                                                                                                                                                   |
| stopRequested                      | boolean                   | Authoritative stop signal; `true` forces transition to `halted` at next checkpoint                                                                                                                                                           |
| stopRequestedAt                    | string (ISO-8601)         | Required when `stopRequested=true`                                                                                                                                                                                                           |
| lastCheckpointAt                   | string (ISO-8601)         | Required when `checkpointIndex > 0`                                                                                                                                                                                                          |
| haltedAt                           | string (ISO-8601)         | Required when [ModeControlOutcome](#modecontroloutcome) is `halt`                                                                                                                                                                            |
| haltedCheckpointIndex              | integer                   | Required when `haltedAt != null`; must equal `checkpointIndex` at halt transition                                                                                                                                                            |
| activeExportRetryCount             | integer                   | Non-negative active retry count used by completion gating                                                                                                                                                                                    |
| exportDegradationThresholdBreached | boolean                   | `true` when export degradation threshold is breached                                                                                                                                                                                         |
| riskAcceptedOverrideRef            | string                    | Required when completion proceeds while `activeExportRetryCount > 0` or `exportDegradationThresholdBreached=true`; must reference an active [RiskAcceptanceOverride](#riskacceptanceoverride) that is non-expired or explicitly non-expiring |
| riskAcceptedOverrideValidatedAt    | string (ISO-8601)         | Required when `riskAcceptedOverrideRef != null`; timestamp of the active/non-expired validity check                                                                                                                                          |
| stopReason                         | [StopReason](#stopreason) | Required when `stopRequested=true`                                                                                                                                                                                                           |

**Equality:** Two [CheckpointControl](#checkpointcontrol) values are equal when `checkpointPolicy`, `checkpointIndex`, `stopRequested`, `stopRequestedAt`, and `haltedAt` match.

---

### TelemetryEnvelope

| Field                           | Type                                                    | Constraint                                                                                                                 |
| ------------------------------- | ------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| cycleId                         | string                                                  | Must match [ExecutionCycle](#executioncycle).cycleId                                                                       |
| activePassId                    | string                                                  | Must match [ExecutionCycle](#executioncycle).activePassId when state is non-terminal                                       |
| runtimeMode                     | [ExecutionRuntimeMode](#executionruntimemode)           | Must match [ExecutionCycle](#executioncycle).runtimeMode                                                                   |
| fallbackPolicyRef               | string                                                  | Required when runtime fallback is used (`runtimeMode != sandcastle`)                                                       |
| fallbackOrderPolicyRef          | string                                                  | Optional approved per-project order-override policy artifact used during fallback resolution                               |
| availabilityProbeRefs           | string[]                                                | Required when runtime fallback is used; probe evidence refs for evaluated runtime modes                                    |
| fallbackFrom                    | [ExecutionRuntimeMode](#executionruntimemode)           | Required when runtime fallback is used; runtime candidate that failed availability/policy checks                           |
| fallbackTo                      | [ExecutionRuntimeMode](#executionruntimemode)           | Required when runtime fallback is used; runtime candidate selected for execution                                           |
| fallbackReasonCode              | [RuntimeFallbackReasonCode](#runtimefallbackreasoncode) | Required when runtime fallback is used                                                                                     |
| fallbackDecisionId              | string                                                  | Required when runtime fallback is used; deterministic fallback decision artifact id                                        |
| fallbackApprovedAt              | string (ISO-8601)                                       | Required when runtime fallback is used                                                                                     |
| fallbackExpiresAt               | string (ISO-8601)                                       | Required when runtime fallback is used and `fallbackNonExpiring=false`                                                     |
| fallbackNonExpiring             | boolean                                                 | Required when runtime fallback is used                                                                                     |
| fallbackResolverStage           | [RuntimeInvokingStage](#runtimeinvokingstage)           | Required when runtime fallback is used                                                                                     |
| fallbackEvaluatedAt             | string (ISO-8601)                                       | Required when runtime fallback is used                                                                                     |
| stageEventRefs                  | string[]                                                | Must include one or more stage telemetry event references per executed pass stage                                          |
| terminalCycleSummaryRef         | string                                                  | Required when [ExecutionCycle](#executioncycle).state is `completed`                                                       |
| interactionCount                | integer                                                 | Non-negative                                                                                                               |
| taskOutcomeSummaryRef           | string                                                  | Non-empty reference                                                                                                        |
| qualityTrendScore               | number                                                  | Normalized score in range `[-1, 1]`                                                                                        |
| gatePassRate                    | number                                                  | Ratio in range `[0, 1]`                                                                                                    |
| riskAcceptedOverrideRef         | string                                                  | Optional [RiskAcceptanceOverride](#riskacceptanceoverride).overrideId used for completion under degraded export conditions |
| riskAcceptedOverrideValidatedAt | string (ISO-8601)                                       | Required when `riskAcceptedOverrideRef != null`                                                                            |
| emittedAt                       | string (ISO-8601)                                       | Required                                                                                                                   |

**Equality:** Two [TelemetryEnvelope](#telemetryenvelope) values are equal when `cycleId`, `emittedAt`, and `qualityTrendScore` match.

## Enums

### OperationMode

| Value      | Description                                                             |
| ---------- | ----------------------------------------------------------------------- |
| autonomous | Loop proceeds automatically with mandatory checkpoints and stop control |
| assisted   | Loop pauses at decision gates for operator confirmation                 |

### ExecutionRuntimeMode

| Value          | Description                                                                                                      |
| -------------- | ---------------------------------------------------------------------------------------------------------------- |
| sandcastle     | Default runtime mode for mapping/testing/synthesis execution                                                     |
| vscode-copilot | Approved fallback runtime mode when Sandcastle is unavailable and fallback governance allows                     |
| claude-code    | Approved fallback runtime mode when higher-priority runtime modes are unavailable and fallback governance allows |

### RuntimeInvokingStage

| Value                | Description                                                          |
| -------------------- | -------------------------------------------------------------------- |
| mapping              | Runtime-invoking mapping stage                                       |
| testing              | Runtime-invoking test-evidence stage                                 |
| solution-synthesis   | Runtime-invoking candidate-synthesis stage                           |
| custom-runtime-stage | Reserved value for approved future runtime-invoking stage extensions |

### RuntimeFallbackReasonCode

| Value                      | Description                                            |
| -------------------------- | ------------------------------------------------------ |
| provider-unreachable       | Runtime endpoint could not be reached                  |
| availability-probe-failed  | Runtime availability probe failed deterministic checks |
| credentials-missing        | Required runtime credentials were missing or invalid   |
| quota-exhausted            | Runtime usage quota prevented execution                |
| policy-disallowed          | Runtime candidate was disallowed by approved policy    |
| explicit-operator-fallback | Explicit governed operator fallback selection          |

### ModeControlOutcome

| Value    | Description                                                                 |
| -------- | --------------------------------------------------------------------------- |
| continue | Mode control authorizes next pass execution                                 |
| pause    | Mode control keeps cycle in checkpoint-hold for explicit operator follow-up |
| halt     | Mode control transitions cycle to `halted` checkpoint-hold                  |
| complete | Mode control authorizes terminal completion                                 |

### CycleState

| Value      | Description                                                   |
| ---------- | ------------------------------------------------------------- |
| intake     | Cycle accepted and awaiting gate determination                |
| mapping    | Codebase intelligence mapping in progress                     |
| testing    | Test evidence generation/improvement in progress              |
| evaluating | Sonar evaluation in progress                                  |
| bundling   | Findings grouped into context bundles                         |
| tasking    | Task generation/export and candidate synthesis in progress    |
| learning   | Learning memory update in progress                            |
| checkpoint | Awaiting explicit mode-control outcome                        |
| halted     | Resumable checkpoint-hold entered after stop compliance proof |
| completed  | Cycle finished with terminal telemetry                        |
| failed     | Cycle terminated due to non-recoverable failure               |

### QualityGateLevel

| Value    | Description                                                            |
| -------- | ---------------------------------------------------------------------- |
| baseline | Minimal enforceable gate for initial adoption                          |
| moderate | Stronger gate with tighter reliability/coverage constraints            |
| strict   | High assurance gate for mature quality posture                         |
| hardened | Maximum gate with aggressive enforcement and drift tolerance near zero |

### FindingCategory

| Value                 | Description                                            |
| --------------------- | ------------------------------------------------------ |
| bug-risk              | Potential defects and correctness issues               |
| security-risk         | Security vulnerabilities or insecure coding patterns   |
| maintainability-smell | Code smells and maintainability debt                   |
| test-gap              | Missing or weak evidence in critical test paths        |
| architecture-drift    | Violations of intended module or dependency boundaries |

### TaskExportStatus

| Value              | Description                                                             |
| ------------------ | ----------------------------------------------------------------------- |
| draft              | Task generated but not exported                                         |
| repository-created | Repository-local task created                                           |
| github-exported    | Task exported to GitHub epic/issue/project item                         |
| jira-exported      | Task exported to Jira epic/story                                        |
| export-partial     | Export completed for only one external system                           |
| retry-pending      | Export failed in prior attempt and is queued for retry                  |
| retrying           | Export retry attempt is in progress                                     |
| both-exported      | Terminal success state after GitHub and Jira exports are both confirmed |
| export-failed      | Export failed for one or more destinations                              |

### TestScopeLevel

| Value         | Description                                               |
| ------------- | --------------------------------------------------------- |
| integration   | Integration tests required by default                     |
| e2e           | End-to-end tests required by default                      |
| functional    | Functional tests required by default                      |
| perf-optional | Performance tests included only when explicitly requested |
| load-optional | Load tests included only when explicitly requested        |

### FindingContextTag

| Value              | Description                                                            |
| ------------------ | ---------------------------------------------------------------------- |
| architecture-layer | Findings tied to architecture layer boundaries (precedence 1)          |
| module-boundary    | Findings tied to module ownership boundaries (precedence 2)            |
| api-contract       | Findings tied to API contracts and schema compatibility (precedence 3) |
| rule-family        | Findings tied to shared policy/rule families (precedence 4)            |
| dependency-risk    | Findings tied to dependency or library risk vectors (precedence 5)     |
| test-scope         | Findings tied to coverage or test-slice evidence scope (precedence 6)  |
| miscellaneous      | Findings that only fit fallback taxonomy (precedence 7)                |

### StopReason

| Value         | Description                      |
| ------------- | -------------------------------- |
| operator-stop | Operator manually requested stop |
| policy-stop   | Policy checkpoint forced stop    |
| risk-stop     | Risk threshold exceeded          |

### RiskAcceptanceOverrideStatus

| Value   | Description                                                                |
| ------- | -------------------------------------------------------------------------- |
| active  | Override can be used if manual lifecycle fields satisfy validity semantics |
| revoked | Override is invalid and cannot be used for completion authorization        |

### RiskAcceptanceApproverRole

| Value          | Description                       |
| -------------- | --------------------------------- |
| quality-owner  | Quality governance approver role  |
| delivery-owner | Delivery governance approver role |
| risk-approver  | Risk governance approver role     |

### RiskAcceptanceOverrideScopeType

| Value                 | Description                                                                      |
| --------------------- | -------------------------------------------------------------------------------- |
| cycle                 | Override binds to one cycle (`scopeCycleId`)                                     |
| pass                  | Override binds to one pass within one cycle (`scopeCycleId` + `scopePassId`)     |
| gate-condition-family | Override binds to one quality-gate condition family (`scopeGateConditionFamily`) |

### QualityGateConditionFamily

| Value           | Description                      |
| --------------- | -------------------------------- |
| reliability     | Reliability condition family     |
| security        | Security condition family        |
| maintainability | Maintainability condition family |
| coverage        | Coverage condition family        |
| duplication     | Duplication condition family     |

### RiskAcceptanceRevocationReasonCode

| Value                | Description                                    |
| -------------------- | ---------------------------------------------- |
| manual-withdrawal    | Manual revocation by authorized principal      |
| policy-violation     | Override revoked due to policy violation       |
| evidence-invalidated | Supporting evidence became invalid             |
| superseded           | Override replaced by a newer approved artifact |

### CompletionDecisionSource

| Value        | Description                                                                                         |
| ------------ | --------------------------------------------------------------------------------------------------- |
| mode-control | Completion was authorized by [ApplyModeControlCheckpoint](operations.md#applymodecontrolcheckpoint) |
