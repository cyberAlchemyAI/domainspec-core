# Rules: Sonar Loop

## Capability Backlinks

- [Quality Gate Targeting and Policy](SPEC.md#quality-gate-targeting-and-policy)
- [Codebase Intelligence Mapping](SPEC.md#codebase-intelligence-mapping)
- [Test Evidence and Sonar Evaluation](SPEC.md#test-evidence-and-sonar-evaluation)
- [Task Orchestration, Solution Synthesis, and Learning](SPEC.md#task-orchestration-solution-synthesis-and-learning)

## User Journey Alignment

This ruleset carries the governance proof package selected in Wave 2 and Wave 3 (`Q7=A`, `Q10=A`) and addresses the evaluator objection from Wave 1 (`Q4=C`) with explicit outcome-bound policy evidence.

- Day-1 overhead objection control: [QualityGateProgressionPolicy](#qualitygateprogressionpolicy), [ApiFirstTaskIntegrationPolicy](#apifirsttaskintegrationpolicy)
- Pilot/scale governance proof anchors: [ExecutionProviderFallbackPolicy](#executionproviderfallbackpolicy), [CompletionGateUnderExportDegradationPolicy](#completiongateunderexportdegradationpolicy), [RiskAcceptanceOverrideValidityPolicy](#riskacceptanceoverridevaliditypolicy)
- Weekly governed loop cadence support: [CycleStateMachine](#cyclestatemachine), [AutonomousCheckpointAndStopPolicy](#autonomouscheckpointandstoppolicy)

Journey detail references: [userjourney/README.md](userjourney/README.md).

## CycleStateMachine

**Type:** State Machine
**Applies To:** [ExecutionCycle](domain.md#executioncycle)

### Transition Table

| From       | Event                 | To         | Guard                                                                                                                        | Effect                                                                                                              |
| ---------- | --------------------- | ---------- | ---------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| intake     | gate-selected         | mapping    | Target gate is valid                                                                                                         | Persist [QualityGateProfile](domain.md#qualitygateprofile) and initialize first child pass ID                       |
| mapping    | map-complete          | testing    | Map dimensions complete                                                                                                      | Persist [CodebaseKnowledgeMap](domain.md#codebaseknowledgemap)                                                      |
| testing    | skill-bundle-ready    | testing    | [ComposeAgnosticSkillBundle](operations.md#composeagnosticskillbundle) branch resolved deterministically                     | Persist [SkillBundleProfile](domain.md#skillbundleprofile) reference and branch decision evidence                   |
| testing    | evidence-ready        | evaluating | Required scope complete                                                                                                      | Store test evidence refs                                                                                            |
| evaluating | sonar-retry-scheduled | evaluating | First Sonar failure and [ExecutionCycle](domain.md#executioncycle).sonarRetryAttemptCount=`0` with remediation evidence      | Increment [ExecutionCycle](domain.md#executioncycle).sonarRetryAttemptCount and persist remediation evidence        |
| evaluating | sonar-finished        | bundling   | Sonar analysis returned findings/verdict                                                                                     | Persist findings                                                                                                    |
| evaluating | sonar-failed-terminal | failed     | Sonar retry failed or retry not permitted                                                                                    | Emit deterministic terminal failure telemetry                                                                       |
| bundling   | bundles-ready         | tasking    | Every finding classified                                                                                                     | Persist [FindingBundle](domain.md#findingbundle) refs                                                               |
| tasking    | tasks-ready           | learning   | Tasks and candidates valid                                                                                                   | Persist [RemediationTask](domain.md#remediationtask) refs                                                           |
| learning   | learning-updated      | checkpoint | Selection learning complete                                                                                                  | Persist [LearningMemory](domain.md#learningmemory)                                                                  |
| checkpoint | telemetry-recorded    | checkpoint | Stage events recorded                                                                                                        | Append [TelemetryEnvelope](domain.md#telemetryenvelope).stageEventRefs                                              |
| checkpoint | continue              | mapping    | Mode control selected [ModeControlOutcome](domain.md#modecontroloutcome)=`continue` and stop not requested                   | Mint next child pass ID and increment checkpoint index                                                              |
| checkpoint | pause                 | checkpoint | Mode control selected [ModeControlOutcome](domain.md#modecontroloutcome)=`pause`                                             | Preserve checkpoint-hold and await explicit resume/decision                                                         |
| checkpoint | complete              | completed  | Mode control selected complete, terminal summary exists, and completion gate allows (including valid override when degraded) | Finalize [TelemetryEnvelope](domain.md#telemetryenvelope) and persist completion gate evidence                      |
| checkpoint | stop                  | halted     | [CheckpointControl](domain.md#checkpointcontrol).stopRequested=true                                                          | Persist stop compliance proof (`stopRequestedAt`, `haltedAt`, `haltedCheckpointIndex`) and preserve cycle artifacts |
| halted     | resume                | checkpoint | Resume requested and [CheckpointControl](domain.md#checkpointcontrol).stopRequested=false                                    | Preserve artifacts and return to explicit checkpoint decision                                                       |
| \*         | fatal-error           | failed     | Non-recoverable failure                                                                                                      | Emit failure telemetry                                                                                              |

### Invariants

| ID     | Invariant                                                                                  | Formal                                                                                                                                                                          |
| ------ | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| I-SM-1 | State progression follows lifecycle order                                                  | `order(intake,mapping,testing,evaluating,bundling,tasking,learning,checkpoint)`                                                                                                 |
| I-SM-2 | Terminal states are explicit                                                               | `state in {completed,failed}` for terminal                                                                                                                                      |
| I-SM-3 | Completed cycle requires telemetry completeness                                            | `state=completed -> telemetryComplete=true`                                                                                                                                     |
| I-SM-4 | Completion authority is mode control                                                       | `state=completed -> completionDecisionSource=mode-control`                                                                                                                      |
| I-SM-5 | Hybrid parent cycle always tracks active child pass                                        | `activePassId in passIds and count(passIds)>=1`                                                                                                                                 |
| I-SM-6 | Halted is resumable checkpoint-hold                                                        | `state=halted -> terminal=false`                                                                                                                                                |
| I-SM-7 | Stop compliance proof includes timestamp and checkpoint correlation                        | `state=halted -> stopRequestedAt != null and haltedAt != null and haltedCheckpointIndex=checkpointIndex`                                                                        |
| I-SM-8 | Completion gate blocks degraded export completion unless valid override exists             | `state=completed -> (activeExportRetryCount=0 and exportDegradationThresholdBreached=false) or validRiskAcceptanceOverride(riskAcceptedOverrideRef,checkpointEvaluatedAt)=true` |
| I-SM-9 | Testing cannot progress to evaluation without deterministic skill-bundle branch resolution | `transition(testing,evidence-ready,evaluating) -> skillBundleDecision in {recomposed,reused}`                                                                                   |

---

## QualityGateProgressionPolicy

**Type:** Policy
**Applies To:** [DetermineTargetQualityGate](operations.md#determinetargetqualitygate)

### Decision Table

| Previous Level | Requested Level    | Result                              | Notes                        |
| -------------- | ------------------ | ----------------------------------- | ---------------------------- |
| none           | baseline           | allow                               | First cycle bootstrap        |
| baseline       | moderate           | allow                               | Normal progression           |
| moderate       | strict             | allow                               | Normal progression           |
| strict         | hardened           | allow                               | Normal progression           |
| baseline       | strict or hardened | block                               | Skip progression not allowed |
| moderate       | hardened           | block                               | Skip progression not allowed |
| any            | lower level        | allow with explicit rollback reason | Requires rationale           |

### Rules

| ID     | Rule                                                           | Formal                                                                                  |
| ------ | -------------------------------------------------------------- | --------------------------------------------------------------------------------------- |
| P-QG-1 | Upward progression can increase by at most one level per cycle | `levelDelta <= 1`                                                                       |
| P-QG-2 | Rollback requires explicit persisted reason                    | `requestedLevel < previousLevel -> rollbackReason != null and rollbackReason persisted` |
| P-QG-3 | Gate thresholds must be fully populated                        | `thresholdsComplete=true`                                                               |

---

## ExecutionProviderFallbackPolicy

**Type:** Policy
**Applies To:** [MapCodebaseIntelligence](operations.md#mapcodebaseintelligence), [BuildAndImproveTestEvidence](operations.md#buildandimprovetestevidence), [GenerateThreeCandidateSolutions](operations.md#generatethreecandidatesolutions), and any approved future runtime-invoking stage

### Decision Table

| Stage                  | Condition                                                                           | Selected Runtime Mode                              | Required Evidence                                                                                                                                                                                                                       |
| ---------------------- | ----------------------------------------------------------------------------------- | -------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| runtime-invoking stage | Sandcastle available                                                                | `sandcastle`                                       | Standard run context                                                                                                                                                                                                                    |
| runtime-invoking stage | Sandcastle unavailable and next approved/available runtime exists in resolved order | first approved available runtime in resolved order | `fallbackPolicyRef`, `availabilityProbeRefs`, `fallbackDecisionId`, `fallbackApprovedAt`, `fallbackExpiresAt`/`fallbackNonExpiring`, `fallbackFrom`, `fallbackTo`, `fallbackReasonCode`, `fallbackResolverStage`, `fallbackEvaluatedAt` |
| runtime-invoking stage | Approved per-project fallback-order policy artifact provided                        | runtime resolved from approved deterministic order | `fallbackOrderPolicyRef` plus all fallback evidence fields                                                                                                                                                                              |
| runtime-invoking stage | No approved/available runtime mode in resolved deterministic order                  | none                                               | Fail operation                                                                                                                                                                                                                          |

### Rules

| ID     | Rule                                                                         | Formal                                                                                                                                                                                                                                                                                                                                                                                    |
| ------ | ---------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| P-EP-1 | Sandcastle is the default runtime mode and default order head                | `runtimeModeDefault=sandcastle and defaultFallbackOrder=[sandcastle,vscode-copilot,claude-code]`                                                                                                                                                                                                                                                                                          |
| P-EP-2 | Runtime mode must be from governed enum                                      | `runtimeMode in {sandcastle,vscode-copilot,claude-code}`                                                                                                                                                                                                                                                                                                                                  |
| P-EP-3 | Per-project override order is allowed only through approved policy artifact  | `resolvedFallbackOrder = approvedOrder(fallbackOrderPolicyRef) or [sandcastle,vscode-copilot,claude-code]`                                                                                                                                                                                                                                                                                |
| P-EP-4 | Fallback requires explicit policy artifact                                   | `runtimeMode!=sandcastle -> fallbackPolicyRef != null`                                                                                                                                                                                                                                                                                                                                    |
| P-EP-5 | Fallback decision evidence minimum is deterministic and mandatory            | `runtimeMode!=sandcastle -> count(availabilityProbeRefs)>=1 and fallbackDecisionId != null and fallbackApprovedAt != null and fallbackFrom != null and fallbackTo=runtimeMode and fallbackReasonCode != null and fallbackResolverStage != null and fallbackEvaluatedAt != null and fallbackNonExpiring != null and (fallbackNonExpiring=true or fallbackExpiresAt > fallbackEvaluatedAt)` |
| P-EP-6 | Fallback decision is auditable                                               | `runtimeMode!=sandcastle -> fallbackDecisionPersisted=true`                                                                                                                                                                                                                                                                                                                               |
| P-EP-7 | Fallback order evaluation is deterministic                                   | `runtimeMode = firstApprovedAvailable(resolvedFallbackOrder)`                                                                                                                                                                                                                                                                                                                             |
| P-EP-8 | Fallback contract applies to every runtime-invoking stage present and future | `stage in enum(RuntimeInvokingStage) -> (runtimeMode!=sandcastle -> fallbackContractSatisfied=true)`                                                                                                                                                                                                                                                                                      |

---

## SkillBundleReusePolicy

**Type:** Policy
**Applies To:** [ComposeAgnosticSkillBundle](operations.md#composeagnosticskillbundle), [ProgressiveQualityLoopWorkflow](workflows.md#progressivequalityloopworkflow)

### Decision Table

| Condition                                      | Decision  | Required Evidence                                                 |
| ---------------------------------------------- | --------- | ----------------------------------------------------------------- |
| `previousBundleRef` missing                    | recompose | Current `mapId`, `capabilityScope`                                |
| `count(capabilityChangeSet)>0`                 | recompose | `capabilityChangeSet`                                             |
| `count(runtimePolicyChangeMarkers)>0`          | recompose | `runtimePolicyChangeMarkers`                                      |
| `count(mapDriftIndicators)>0`                  | recompose | `mapDriftIndicators`                                              |
| No trigger and latest baseline bundle is valid | reuse     | `previousBundleRef`, agnosticity and coverage validation evidence |
| No trigger and baseline bundle missing/invalid | fail      | Deterministic policy error                                        |

### Rules

| ID     | Rule                                                                                       | Formal                                                                                                                                                                                                                |
| ------ | ------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| P-SB-1 | Recompose-vs-reuse trigger evaluation is deterministic                                     | `recomposeRequired = forceRecompose=true or previousBundleRef=null or count(capabilityChangeSet)>0 or count(runtimePolicyChangeMarkers)>0 or count(mapDriftIndicators)>0`                                             |
| P-SB-2 | Reuse is allowed only with latest valid agnostic baseline and complete capability coverage | `recomposeRequired=false -> previousBundleRef=latestValidBundle(capabilityScope,agnosticContractVersion) and bundleAgnostic(previousBundleRef)=true and coverage(capabilityScope,skills(previousBundleRef))=complete` |
| P-SB-3 | Recomposition enforces agnosticity and complete capability coverage                        | `recomposeRequired=true -> forall skill in genericSkillRefs, skill.agentSpecific=false and coverage(capabilityScope,genericSkillRefs)=complete`                                                                       |
| P-SB-4 | Exactly one branch executes per pass                                                       | `xor(recomposeBranch,reuseBranch)=true`                                                                                                                                                                               |
| P-SB-5 | Branch decision evidence is mandatory for telemetry                                        | `skillBundleDecision in {recomposed,reused} and skillBundleDecisionRef != null`                                                                                                                                       |

---

## TestScopePolicy

**Type:** Policy
**Applies To:** [BuildAndImproveTestEvidence](operations.md#buildandimprovetestevidence)

### Rules

| ID     | Rule                                                            | Formal                                                         |
| ------ | --------------------------------------------------------------- | -------------------------------------------------------------- |
| P-TS-1 | Integration tests are mandatory                                 | `integration in requiredScopes`                                |
| P-TS-2 | E2E tests are mandatory                                         | `e2e in requiredScopes`                                        |
| P-TS-3 | Functional tests are mandatory                                  | `functional in requiredScopes`                                 |
| P-TS-4 | Sonar precondition requires integration/e2e/functional evidence | `sonarPrecondition -> hasEvidence(integration,e2e,functional)` |
| P-TS-5 | Perf tests are optional and request-bound                       | `perf-optional -> optionalScopeRequestRef != null`             |
| P-TS-6 | Load tests are optional and request-bound                       | `load-optional -> optionalScopeRequestRef != null`             |

---

## SonarRetryPolicy

**Type:** Policy
**Applies To:** [EvaluateWithSonarQualityGate](operations.md#evaluatewithsonarqualitygate)

### Decision Table

| Attempt | Condition                                     | Result                         | Required Evidence                                  |
| ------- | --------------------------------------------- | ------------------------------ | -------------------------------------------------- |
| 0       | Sonar run fails and retry budget is available | schedule exactly one retry     | remediation evidence must be produced before retry |
| 1       | Sonar run succeeds                            | continue to bundling           | verdict + findings persisted                       |
| 1       | Sonar run fails                               | deterministic terminal failure | failure telemetry emitted                          |

### Rules

| ID     | Rule                                            | Formal                                                                  |
| ------ | ----------------------------------------------- | ----------------------------------------------------------------------- |
| P-SR-1 | Sonar retry is bounded to one retry             | `sonarRetryAttemptCount in {0,1}`                                       |
| P-SR-2 | Retry requires remediation evidence             | `sonarRetryAttemptCount=1 -> sonarRetryRemediationRef != null`          |
| P-SR-3 | Retry failure is deterministic terminal outcome | `sonarRetryAttemptCount=1 and sonarFailed=true -> nextState=failed`     |
| P-SR-4 | No implicit additional retries are allowed      | `sonarRetryAttemptCount=1 and sonarFailed=true -> retryScheduled=false` |

---

## ApiFirstTaskIntegrationPolicy

**Type:** Policy
**Applies To:** [CreateAndExportRemediationTasks](operations.md#createandexportremediationtasks)

### Rule

Task export uses first-party HTTP APIs for GitHub and Jira; MCP-only routing is not authoritative for this feature.

Formal: `exportPath = githubREST and jiraREST`

### Constraints

| ID      | Constraint                                               | Formal                                                                                |
| ------- | -------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| P-API-1 | GitHub export must carry repository task linkage         | `githubPayload contains repositoryTaskRef`                                            |
| P-API-2 | Jira export must carry repository task linkage           | `jiraPayload contains repositoryTaskRef`                                              |
| P-API-3 | Partial export status must be explicit                   | `oneExportFailed -> exportStatus=export-partial`                                      |
| P-API-4 | GitHub epic model uses issue plus metadata conventions   | `githubEpic = issue and metadataConventionsApplied=true`                              |
| P-API-5 | Both-system export terminal state is explicit            | `githubExported and jiraExported -> exportStatus=both-exported`                       |
| P-API-6 | Active export retries are surfaced for completion gating | `activeExportRetryCount = count(task where exportStatus in {retry-pending,retrying})` |

### Task Export Transition Model

| From Status        | Event                   | To Status          | Guard                           |
| ------------------ | ----------------------- | ------------------ | ------------------------------- |
| draft              | repository-task-created | repository-created | repository task persisted       |
| repository-created | github-export-success   | github-exported    | GitHub issue + metadata created |
| repository-created | jira-export-success     | jira-exported      | Jira issue created              |
| github-exported    | jira-export-success     | both-exported      | Jira success received           |
| jira-exported      | github-export-success   | both-exported      | GitHub success received         |
| repository-created | export-error            | retry-pending      | retry budget remaining          |
| github-exported    | export-error            | retry-pending      | retry budget remaining          |
| jira-exported      | export-error            | retry-pending      | retry budget remaining          |
| export-partial     | retry-scheduled         | retry-pending      | retry budget remaining          |
| retry-pending      | retry-started           | retrying           | retry worker acquired task      |
| retrying           | retry-success-both      | both-exported      | both exports now confirmed      |
| retrying           | retry-partial-success   | export-partial     | one export still pending        |
| retrying           | retry-exhausted         | export-failed      | retry budget exhausted          |

---

## CompletionGateUnderExportDegradationPolicy

**Type:** Policy
**Applies To:** [ApplyModeControlCheckpoint](operations.md#applymodecontrolcheckpoint)

### Decision Table

| Condition                                                                                                                    | Completion Decision | Required Evidence                                                         |
| ---------------------------------------------------------------------------------------------------------------------------- | ------------------- | ------------------------------------------------------------------------- |
| `activeExportRetryCount > 0` and no override                                                                                 | block               | None; completion remains blocked                                          |
| `exportDegradationThresholdBreached=true` and no override                                                                    | block               | None; completion remains blocked                                          |
| (`activeExportRetryCount > 0` or `exportDegradationThresholdBreached=true`) and override present but invalid/revoked/expired | block               | Persist invalidation reason                                               |
| (`activeExportRetryCount > 0` or `exportDegradationThresholdBreached=true`) and override present and valid                   | allow-with-override | `riskAcceptedOverrideRef` and `riskAcceptedOverrideValidatedAt` persisted |
| `activeExportRetryCount=0` and `exportDegradationThresholdBreached=false`                                                    | allow               | None                                                                      |

### Rules

| ID     | Rule                                                                                              | Formal                                                                                                                                                                                                                      |
| ------ | ------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| P-CG-1 | Active retries block completion without override                                                  | `activeExportRetryCount > 0 and riskAcceptedOverrideRef = null -> completionAllowed=false`                                                                                                                                  |
| P-CG-2 | Degradation threshold breach blocks completion without override                                   | `exportDegradationThresholdBreached=true and riskAcceptedOverrideRef = null -> completionAllowed=false`                                                                                                                     |
| P-CG-3 | Override must be explicit, persisted, and valid                                                   | `completionAllowed=true and (activeExportRetryCount > 0 or exportDegradationThresholdBreached=true) -> riskAcceptedOverrideRef != null and validRiskAcceptanceOverride(riskAcceptedOverrideRef,checkpointEvaluatedAt)=true` |
| P-CG-4 | Override validity requires active status and non-expired window (or explicit non-expiring policy) | `validRiskAcceptanceOverride(ref,t) -> status(ref)=active and (nonExpiring(ref)=true or expiresAt(ref) > t) and lifecycleManagedManually(ref)=true`                                                                         |
| P-CG-5 | Completion decision evidence includes export gate inputs and override validation evidence         | `completionDecision -> activeExportRetryCount recorded and exportDegradationThresholdBreached recorded and (riskAcceptedOverrideRef != null -> riskAcceptedOverrideValidatedAt recorded)`                                   |

---

## RiskAcceptanceOverrideValidityPolicy

**Type:** Policy
**Applies To:** [ApplyModeControlCheckpoint](operations.md#applymodecontrolcheckpoint), [RecordCycleTelemetryTrend](operations.md#recordcycletelemetrytrend)

### Decision Table

| Condition                                                                             | Validity Result    | Required Evidence                        |
| ------------------------------------------------------------------------------------- | ------------------ | ---------------------------------------- |
| `status=active` and `nonExpiring=true`                                                | valid              | `evidenceRef`, `auditRef`                |
| `status=active` and `nonExpiring=false` and `expiresAt > checkpointEvaluatedAt`       | valid              | `evidenceRef`, `auditRef`, `expiresAt`   |
| `status=active` and required scope binding fields are missing for `overrideScopeType` | invalid-incomplete | Persist scope-binding validation failure |
| `status=active` and `approverRole` is outside governed enum                           | invalid-incomplete | Persist role validation failure          |
| `status=active` and `nonExpiring=false` and `expiresAt <= checkpointEvaluatedAt`      | invalid-expired    | Persist expiry reason                    |
| `status=revoked`                                                                      | invalid-revoked    | Persist revocation reason                |
| Missing required evidence/audit fields                                                | invalid-incomplete | Persist validation failure               |

### Rules

| ID     | Rule                                                                     | Formal                                                                                                                                                                                                                                    |
| ------ | ------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| P-RO-1 | Override id must resolve to existing governed artifact                   | `riskAcceptedOverrideRef != null -> exists(RiskAcceptanceOverride.overrideId=riskAcceptedOverrideRef)`                                                                                                                                    |
| P-RO-2 | Approver role and principal are mandatory and role must be enum-governed | `validRiskAcceptanceOverride(ref,t)=true -> approverRole(ref) in enum(RiskAcceptanceApproverRole) and approverPrincipal(ref) != null`                                                                                                     |
| P-RO-3 | Rationale and typed scope bindings are mandatory                         | `validRiskAcceptanceOverride(ref,t)=true -> rationale(ref) != null and overrideScopeType(ref) in enum(RiskAcceptanceOverrideScopeType)`                                                                                                   |
| P-RO-4 | Evidence and audit references are mandatory                              | `validRiskAcceptanceOverride(ref,t)=true -> evidenceRef(ref) != null and auditRef(ref) != null`                                                                                                                                           |
| P-RO-5 | Time validity is mandatory unless explicitly non-expiring                | `validRiskAcceptanceOverride(ref,t)=true -> status(ref)=active and (nonExpiring(ref)=true or expiresAt(ref) > t)`                                                                                                                         |
| P-RO-6 | Validation timestamp must be persisted when override is evaluated        | `riskAcceptedOverrideRef != null -> riskAcceptedOverrideValidatedAt != null`                                                                                                                                                              |
| P-RO-7 | Override lifecycle is manual and has no implicit expiry duration         | `nonExpiring(ref)=false -> expiresAt(ref) explicitly set by approval; defaultExpiry(ref)=null`                                                                                                                                            |
| P-RO-8 | Scope binding fields must match scope type                               | `overrideScopeType(ref)=cycle -> scopeCycleId(ref) != null; overrideScopeType(ref)=pass -> scopeCycleId(ref) != null and scopePassId(ref) != null; overrideScopeType(ref)=gate-condition-family -> scopeGateConditionFamily(ref) != null` |
| P-RO-9 | Revocation invalidation semantics are deterministic                      | `status(ref)=revoked -> validRiskAcceptanceOverride(ref,t)=false and revokedAt(ref) != null and revokedByPrincipal(ref) != null and revocationReasonCode(ref) in enum(RiskAcceptanceRevocationReasonCode)`                                |

---

## ThreeCandidateSolutionRule

**Type:** Rule
**Applies To:** [GenerateThreeCandidateSolutions](operations.md#generatethreecandidatesolutions)

### Rule

Every [RemediationTask](domain.md#remediationtask) must provide exactly three [SolutionCandidate](domain.md#solutioncandidate) options.

Formal: `count(candidateSolutions)=3`

### Candidate Mix Constraint

| ID     | Constraint                             | Formal                                      |
| ------ | -------------------------------------- | ------------------------------------------- |
| R-3C-1 | Include one established-pattern option | `exists candidate.strategyType=established` |
| R-3C-2 | Include one hybrid or variant option   | `exists candidate.strategyType=hybrid`      |
| R-3C-3 | Include one new-pattern option         | `exists candidate.strategyType=new-pattern` |

---

## NonRedundantAbstractionRule

**Type:** Rule
**Applies To:** [SynthesizeCrossSmellAbstractions](operations.md#synthesizecrosssmellabstractions)

### Rule

Cross-smell abstraction proposals must reduce duplication and avoid overlapping redundant abstractions.

Formal: `forall abstractionA, abstractionB where A!=B, overlap(smellsA,smellsB) < redundancyThreshold and abstractionScore >= 0.70`

### Scoring Formula

`abstractionScore = 0.45*coverageScore + 0.30*severityReductionScore + 0.15*feasibilityScore + 0.10*learningReuseScore - overlapPenalty`

Acceptance threshold: `abstractionScore >= 0.70`

### Constraints

| ID     | Constraint                                             | Formal                                                                          |
| ------ | ------------------------------------------------------ | ------------------------------------------------------------------------------- |
| R-NR-1 | Each abstraction must solve at least two smell bundles | `coverageCount >= 2`                                                            |
| R-NR-2 | Abstraction score must exceed threshold                | `abstractionScore >= 0.70`                                                      |
| R-NR-3 | Tie-breaks are deterministic                           | `sortBy(-coverageScore,+overlapPenalty,-severityReductionScore,+abstractionId)` |

---

## FindingContextTagPolicy

**Type:** Policy
**Applies To:** [BundleFindingsByContext](operations.md#bundlefindingsbycontext)

### Controlled Taxonomy With Precedence

| Tag                | Precedence | Meaning                                                     |
| ------------------ | ---------- | ----------------------------------------------------------- |
| architecture-layer | 1          | Architecture layer boundary and layering drift context      |
| module-boundary    | 2          | Module ownership and boundary context                       |
| api-contract       | 3          | API contract, schema, and compatibility context             |
| rule-family        | 4          | Shared policy/rule family context                           |
| dependency-risk    | 5          | Third-party dependency and supply-chain context             |
| test-scope         | 6          | Test evidence and scope context                             |
| miscellaneous      | 7          | Fallback context when no higher-precedence taxonomy matches |

### Rules

| ID     | Rule                                             | Formal                                         |
| ------ | ------------------------------------------------ | ---------------------------------------------- |
| P-FC-1 | Context tags use only controlled taxonomy values | `contextTag in enum(FindingContextTag)`        |
| P-FC-2 | Precedence chooses the authoritative context tag | `contextTag = argmin(precedence(matchedTags))` |
| P-FC-3 | Same-precedence ties are deterministic           | `tie -> sortBy(-severity,+tagName)`            |

---

## LearningFeedbackRule

**Type:** Rule
**Applies To:** [ApplyOperatorSelectionLearning](operations.md#applyoperatorselectionlearning)

### Rule

Operator-selected candidates and outcomes must update ranking signals used by subsequent cycles.

Formal: `selection + outcome -> update(candidateRankingSignals)`

### Constraints

| ID     | Constraint                                          | Formal                                           |
| ------ | --------------------------------------------------- | ------------------------------------------------ |
| R-LF-1 | Selection rationale is mandatory                    | `selectionReason != null`                        |
| R-LF-2 | Outcome capture is mandatory                        | `observedOutcome != null`                        |
| R-LF-3 | Learning update ties to one existing task candidate | `selectedCandidateId in task.candidateSolutions` |

---

## AutonomousCheckpointAndStopPolicy

**Type:** Policy
**Applies To:** [ApplyModeControlCheckpoint](operations.md#applymodecontrolcheckpoint)

### Decision Table

| Mode                   | Condition                                                                                          | Selected Behavior | Notes                                                                 |
| ---------------------- | -------------------------------------------------------------------------------------------------- | ----------------- | --------------------------------------------------------------------- |
| autonomous             | checkpoint boundary reached and no stop requested                                                  | continue          | Checkpoint evidence still required                                    |
| autonomous             | checkpoint boundary reached and stop requested                                                     | halt              | Must transition to `halted` with stop compliance proof                |
| autonomous or assisted | checkpoint boundary with completion requested, terminal summary ready, and completion gate allowed | complete          | Completion only via mode-control decision                             |
| assisted               | decision gate reached and unresolved                                                               | pause             | First-class mode-control outcome; remain at checkpoint                |
| autonomous or assisted | state is `halted`, stop cleared, and resume requested                                              | pause             | Return to checkpoint-hold and await explicit `continue` or `complete` |

### Rules

| ID     | Rule                                                                              | Formal                                                                                                         |
| ------ | --------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| P-AC-1 | Autonomous mode must honor stop at next checkpoint                                | `mode=autonomous and stopRequested=true -> nextState=halted`                                                   |
| P-AC-2 | Assisted mode must pause at decision gates                                        | `mode=assisted and decisionGate=true and unresolved=true -> modeControlOutcome=pause and nextState=checkpoint` |
| P-AC-3 | Checkpoint evidence must be persisted for all mode transitions                    | `modeTransition -> checkpointEvidenceRef != null`                                                              |
| P-AC-4 | Checkpoint control is authoritative stop source                                   | `nextState=halted -> checkpointControl.stopRequested=true`                                                     |
| P-AC-5 | Mode control is authoritative completion source                                   | `nextState=completed -> completionDecisionSource=mode-control`                                                 |
| P-AC-6 | Halt transition requires stop compliance proof fields                             | `nextState=halted -> stopRequestedAt != null and haltedAt != null and haltedCheckpointIndex=checkpointIndex`   |
| P-AC-7 | Halted state is resumable via explicit resume request                             | `state=halted and resumeRequested=true and stopRequested=false -> nextState=checkpoint`                        |
| P-AC-8 | Completion gate enforces export degradation blocking unless valid override exists | `nextState=completed -> completionAllowedBy(CompletionGateUnderExportDegradationPolicy)=true`                  |

---

## TelemetryCompletenessRule

**Type:** Rule
**Applies To:** [RecordCycleTelemetryTrend](operations.md#recordcycletelemetrytrend)

### Rule

Cycle telemetry must include stage event stream, runtime mode, skill-bundle branch evidence, fallback evidence (when fallback occurs), and terminal cycle summary for completion decisions.

Formal: `required(stageEventRefs,interactionCount,taskOutcomeSummaryRef,qualityTrendScore,gatePassRate,runtimeMode,skillBundleDecision,skillBundleDecisionRef,emittedAt)`

### Constraints

| ID     | Constraint                                                                    | Formal                                                                                                                                                                                                                                                                                                                                                                                                        |
| ------ | ----------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| R-TC-1 | Gate pass rate is bounded                                                     | `0 <= gatePassRate <= 1`                                                                                                                                                                                                                                                                                                                                                                                      |
| R-TC-2 | Quality trend score is bounded                                                | `-1 <= qualityTrendScore <= 1`                                                                                                                                                                                                                                                                                                                                                                                |
| R-TC-3 | Completed cycles require telemetry envelope                                   | `state=completed -> telemetryEnvelope != null`                                                                                                                                                                                                                                                                                                                                                                |
| R-TC-4 | Completed cycles require terminal cycle summary                               | `state=completed -> terminalCycleSummaryRef != null`                                                                                                                                                                                                                                                                                                                                                          |
| R-TC-5 | Halt events require stop compliance timestamps with checkpoint correlation    | `checkpointOutcome=halt -> stopRequestedAt != null and haltedAt != null and haltedCheckpointIndex=checkpointIndex`                                                                                                                                                                                                                                                                                            |
| R-TC-6 | Completion under export degradation requires explicit valid override evidence | `(activeExportRetryCount > 0 or exportDegradationThresholdBreached=true) and checkpointOutcome=complete -> riskAcceptedOverrideRef != null and riskAcceptedOverrideValidatedAt != null and validRiskAcceptanceOverride(riskAcceptedOverrideRef,checkpointEvaluatedAt)=true`                                                                                                                                   |
| R-TC-7 | Runtime mode must use governed enum values                                    | `runtimeMode in enum(ExecutionRuntimeMode)`                                                                                                                                                                                                                                                                                                                                                                   |
| R-TC-8 | Runtime fallback evidence minimum is required when fallback occurs            | `runtimeMode!=sandcastle -> fallbackPolicyRef != null and count(availabilityProbeRefs)>=1 and fallbackFrom != null and fallbackTo=runtimeMode and fallbackReasonCode != null and fallbackDecisionId != null and fallbackApprovedAt != null and fallbackResolverStage in enum(RuntimeInvokingStage) and fallbackEvaluatedAt != null and (fallbackNonExpiring=true or fallbackExpiresAt > fallbackEvaluatedAt)` |
| R-TC-9 | Skill-bundle branch telemetry is required and must match the selected branch  | `skillBundleDecision in {recomposed,reused} and skillBundleDecisionRef != null and (skillBundleDecision=reused -> reusedBundleRef != null) and (skillBundleDecision=recomposed -> recomposedBundleVersion != null)`                                                                                                                                                                                           |
