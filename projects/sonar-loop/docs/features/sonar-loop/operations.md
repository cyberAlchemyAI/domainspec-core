# Operations: Sonar Loop

## Capability Backlinks

- [Quality Gate Targeting and Policy](SPEC.md#quality-gate-targeting-and-policy)
- [Codebase Intelligence Mapping](SPEC.md#codebase-intelligence-mapping)
- [Test Evidence and Sonar Evaluation](SPEC.md#test-evidence-and-sonar-evaluation)
- [Task Orchestration, Solution Synthesis, and Learning](SPEC.md#task-orchestration-solution-synthesis-and-learning)

## User Journey Alignment

| Journey decision                                                  | Operational anchor                                                                                                                                                        |
| ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Wave 1 `Q3=B` day-1 value is actionable task output               | [BundleFindingsByContext](#bundlefindingsbycontext), [CreateAndExportRemediationTasks](#createandexportremediationtasks)                                                  |
| Wave 2 `Q6=A` assisted-first pilot mode                           | [ApplyModeControlCheckpoint](#applymodecontrolcheckpoint), [ApplyOperatorSelectionLearning](#applyoperatorselectionlearning)                                              |
| Wave 2 `Q7=A` and Wave 3 `Q10=A` governance proof package         | [MapCodebaseIntelligence](#mapcodebaseintelligence), [BuildAndImproveTestEvidence](#buildandimprovetestevidence), [RecordCycleTelemetryTrend](#recordcycletelemetrytrend) |
| Wave 3 `Q11=A` GitHub-first initial scale posture                 | [CreateAndExportRemediationTasks](#createandexportremediationtasks)                                                                                                       |
| Wave 4 `Q14=A` one-time per-repository non-SaaS packaging framing | Repository-scoped outputs and explicit export lifecycle in [CreateAndExportRemediationTasks](#createandexportremediationtasks)                                            |

Detailed narrative references: [userjourney/README.md](userjourney/README.md).

## DetermineTargetQualityGate

**Type:** Operation (mutation)
**Actor:** Operator or autonomous scheduler
**Triggers:** New [ExecutionCycle](domain.md#executioncycle) starts

Determines the [QualityGateProfile](domain.md#qualitygateprofile) for the current cycle using progression policy and mode-aware controls.

### Input

| Field             | Type                                                   | Required | Description                                                                                                                                                                               |
| ----------------- | ------------------------------------------------------ | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| cycleId           | string                                                 | yes      | Target [ExecutionCycle](domain.md#executioncycle).cycleId                                                                                                                                 |
| passId            | string                                                 | yes      | Active child pass identifier within the parent cycle                                                                                                                                      |
| requestedLevel    | [QualityGateLevel](domain.md#qualitygatelevel)         | no       | Operator-requested gate level                                                                                                                                                             |
| previousGateLevel | [QualityGateLevel](domain.md#qualitygatelevel)         | no       | Last successful cycle level                                                                                                                                                               |
| rollbackReason    | string                                                 | no       | Required when requested level is a downgrade                                                                                                                                              |
| mode              | [OperationMode](domain.md#operationmode)               | yes      | Current execution mode                                                                                                                                                                    |
| runtimeMode       | [ExecutionRuntimeMode](domain.md#executionruntimemode) | yes      | Selected runtime mode (`sandcastle` default order head, with approved per-project order override allowed via [ExecutionProviderFallbackPolicy](rules.md#executionproviderfallbackpolicy)) |

### Rules

| ID  | Rule                                            | Formal                                                                    |
| --- | ----------------------------------------------- | ------------------------------------------------------------------------- |
| R1  | Gate progression follows policy bounds          | See [QualityGateProgressionPolicy](rules.md#qualitygateprogressionpolicy) |
| R2  | Autonomous mode cannot bypass checkpoint gating | `mode=autonomous -> checkpointRequired=true`                              |
| R3  | Selected gate must be explicit                  | `targetGate.level != null`                                                |
| R4  | Gate downgrade must persist rollback reason     | `requestedLevel < previousGateLevel -> rollbackReason != null`            |
| R5  | Runtime mode must be explicitly supported       | `runtimeMode in enum(ExecutionRuntimeMode)`                               |

### State Transition

[ExecutionCycle](domain.md#executioncycle): `intake -> mapping`

### Postconditions

- [ExecutionCycle](domain.md#executioncycle).targetGate is set.
- [ExecutionCycle](domain.md#executioncycle).activePassId is set to `passId` and appended to [ExecutionCycle](domain.md#executioncycle).passIds when newly minted.
- [ExecutionCycle](domain.md#executioncycle).runtimeMode is set.
- [ExecutionCycle](domain.md#executioncycle).state becomes `mapping`.

### Error States

| Condition                            | Result                                 |
| ------------------------------------ | -------------------------------------- |
| Unsupported level jump               | `QUALITY_GATE_PROGRESS_VIOLATION`      |
| Missing requested and derived level  | `QUALITY_GATE_UNRESOLVED`              |
| Missing rollback reason on downgrade | `QUALITY_GATE_ROLLBACK_REASON_MISSING` |
| Unsupported runtime mode             | `RUNTIME_MODE_UNSUPPORTED`             |

---

## MapCodebaseIntelligence

**Type:** Operation (mutation)
**Actor:** Runtime execution engine
**Triggers:** Target gate is resolved

Builds a [CodebaseKnowledgeMap](domain.md#codebaseknowledgemap) that covers dependencies, use-cases, rules, patterns, modules, APIs, architecture, and libraries.

### Input

| Field                  | Type                                                             | Required | Description                                                                             |
| ---------------------- | ---------------------------------------------------------------- | -------- | --------------------------------------------------------------------------------------- |
| cycleId                | string                                                           | yes      | Parent [ExecutionCycle](domain.md#executioncycle).cycleId                               |
| passId                 | string                                                           | yes      | Active child pass identifier                                                            |
| repositoryRef          | string                                                           | yes      | Target repository                                                                       |
| scanScope              | string[]                                                         | yes      | Included directories/modules                                                            |
| runtimeMode            | [ExecutionRuntimeMode](domain.md#executionruntimemode)           | yes      | Selected runtime mode (`sandcastle`, `vscode-copilot`, `claude-code`)                   |
| fallbackPolicyRef      | string                                                           | no       | Required when runtime mode falls back from `sandcastle`                                 |
| fallbackOrderPolicyRef | string                                                           | no       | Optional approved per-project fallback-order policy artifact                            |
| availabilityProbeRefs  | string[]                                                         | no       | Required when runtime mode falls back from `sandcastle`                                 |
| fallbackDecisionId     | string                                                           | no       | Required when runtime mode falls back from `sandcastle`                                 |
| fallbackApprovedAt     | string (ISO-8601)                                                | no       | Required when runtime mode falls back from `sandcastle`                                 |
| fallbackExpiresAt      | string (ISO-8601)                                                | no       | Required when runtime mode falls back from `sandcastle` and `fallbackNonExpiring=false` |
| fallbackNonExpiring    | boolean                                                          | no       | Required when runtime mode falls back from `sandcastle`                                 |
| fallbackFrom           | [ExecutionRuntimeMode](domain.md#executionruntimemode)           | no       | Required when runtime mode falls back from `sandcastle`                                 |
| fallbackTo             | [ExecutionRuntimeMode](domain.md#executionruntimemode)           | no       | Required when runtime mode falls back from `sandcastle`; must equal `runtimeMode`       |
| fallbackReasonCode     | [RuntimeFallbackReasonCode](domain.md#runtimefallbackreasoncode) | no       | Required when runtime mode falls back from `sandcastle`                                 |
| fallbackResolverStage  | [RuntimeInvokingStage](domain.md#runtimeinvokingstage)           | no       | Required when runtime mode falls back from `sandcastle`; must be `mapping`              |
| fallbackEvaluatedAt    | string (ISO-8601)                                                | no       | Required when runtime mode falls back from `sandcastle`                                 |

### Rules

| ID  | Rule                                                                            | Formal                                                                                                                                                                                   |
| --- | ------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| R1  | Mapping must include all required dimensions                                    | `covers(dependencies,useCases,rules,patterns,modules,apis,architecture,libraries)=true`                                                                                                  |
| R2  | Mapping runtime mode defaults to Sandcastle with deterministic order resolution | `resolvedFallbackOrder = approvedOrder(fallbackOrderPolicyRef) or [sandcastle,vscode-copilot,claude-code]`                                                                               |
| R3  | Fallback runtime mode requires strong policy evidence                           | `runtimeMode!=sandcastle -> fallbackPolicyRef != null and count(availabilityProbeRefs)>=1 and fallbackDecisionId != null and fallbackApprovedAt != null and fallbackNonExpiring != null` |
| R4  | Fallback runtime mode selection is deterministic and auditable                  | `runtimeMode!=sandcastle -> fallbackTo=runtimeMode and runtimeMode = firstApprovedAvailable(resolvedFallbackOrder) and fallbackDecisionPersisted=true`                                   |
| R5  | Fallback runtime mode metadata is stage-bound                                   | `runtimeMode!=sandcastle -> fallbackFrom != null and fallbackReasonCode != null and fallbackResolverStage=mapping and fallbackEvaluatedAt != null`                                       |
| R6  | Expiring fallback approvals must be time-valid at evaluation                    | `runtimeMode!=sandcastle and fallbackNonExpiring=false -> fallbackExpiresAt > fallbackEvaluatedAt`                                                                                       |

### State Transition

[ExecutionCycle](domain.md#executioncycle): `mapping -> testing`

### Postconditions

- New [CodebaseKnowledgeMap](domain.md#codebaseknowledgemap) snapshot is stored.
- [ExecutionCycle](domain.md#executioncycle).codebaseMapRef is updated.
- [ExecutionCycle](domain.md#executioncycle).runtimeMode is persisted for downstream stages.

### Error States

| Condition                                          | Result                                             |
| -------------------------------------------------- | -------------------------------------------------- |
| Incomplete map dimensions                          | `CODEBASE_MAP_INCOMPLETE`                          |
| Selected runtime mode not available                | `RUNTIME_MODE_UNAVAILABLE`                         |
| Missing fallback policy evidence                   | `EXECUTION_PROVIDER_FALLBACK_POLICY_MISSING`       |
| Missing required fallback decision evidence fields | `EXECUTION_PROVIDER_FALLBACK_EVIDENCE_INCOMPLETE`  |
| Invalid fallback order override policy artifact    | `EXECUTION_PROVIDER_FALLBACK_ORDER_POLICY_INVALID` |
| Expired fallback approval artifact                 | `EXECUTION_PROVIDER_FALLBACK_APPROVAL_EXPIRED`     |
| Runtime mode outside governed enum                 | `RUNTIME_MODE_UNSUPPORTED`                         |

---

## ComposeAgnosticSkillBundle

**Type:** Operation (mutation)
**Actor:** Skill bundle composer
**Triggers:** Codebase map is refreshed and bundle trigger evaluation is requested

Evaluates deterministic recomposition triggers and either composes a capability-scoped [SkillBundleProfile](domain.md#skillbundleprofile) or reuses the latest valid bundle, while keeping skills agnostic across coding agents.

### Input

| Field                      | Type     | Required | Description                                                                                                    |
| -------------------------- | -------- | -------- | -------------------------------------------------------------------------------------------------------------- |
| mapId                      | string   | yes      | Source [CodebaseKnowledgeMap](domain.md#codebaseknowledgemap).mapId                                            |
| capabilityScope            | string[] | yes      | Covered capabilities                                                                                           |
| genericSkillRefs           | string[] | no       | Candidate agnostic skills; required when recomposition is selected                                             |
| previousBundleRef          | string   | no       | Latest valid [SkillBundleProfile](domain.md#skillbundleprofile) reference; required for reuse branch           |
| capabilityChangeSet        | string[] | no       | Capability-level deltas detected since the previous bundle snapshot                                            |
| runtimePolicyChangeMarkers | string[] | no       | Runtime/policy contract deltas that can invalidate prior bundle assumptions                                    |
| mapDriftIndicators         | string[] | no       | Drift indicators derived from current [CodebaseKnowledgeMap](domain.md#codebaseknowledgemap) vs prior baseline |
| forceRecompose             | boolean  | no       | Explicit override to force recomposition                                                                       |
| agnosticContractVersion    | string   | no       | Governing agnostic contract version used to validate reuse eligibility                                         |

### Rules

| ID  | Rule                                                              | Formal                                                                                                                                                                    |
| --- | ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| R1  | Recomposition branch must remain agent-agnostic                   | `recomposeRequired=true -> forall skill in genericSkillRefs, skill.agentSpecific=false`                                                                                   |
| R2  | Recomposition branch must cover all capability scopes             | `recomposeRequired=true -> coverage(capabilityScope,genericSkillRefs)=complete`                                                                                           |
| R3  | Recomposition trigger evaluation is deterministic                 | `recomposeRequired = forceRecompose=true or previousBundleRef=null or count(capabilityChangeSet)>0 or count(runtimePolicyChangeMarkers)>0 or count(mapDriftIndicators)>0` |
| R4  | Reuse branch requires valid prior bundle coverage and agnosticity | `recomposeRequired=false -> previousBundleRef != null and bundleAgnostic(previousBundleRef)=true and coverage(capabilityScope,skills(previousBundleRef))=complete`        |
| R5  | Exactly one branch is executed                                    | `xor(recomposeBranch,reuseBranch)=true`                                                                                                                                   |
| R6  | Reuse branch selects the latest valid baseline                    | `reuseBranch=true -> previousBundleRef=latestValidBundle(capabilityScope,agnosticContractVersion)`                                                                        |

### State Transition

[ExecutionCycle](domain.md#executioncycle): `testing -> testing`

### Postconditions

- When `recomposeRequired=true`, a new [SkillBundleProfile](domain.md#skillbundleprofile) version is created or updated and attached to cycle context.
- When `recomposeRequired=false`, the `previousBundleRef` is reused unchanged and attached to cycle context.
- Bundle decision evidence is persisted with evaluated trigger inputs for downstream telemetry.

### Error States

| Condition                                          | Result                                       |
| -------------------------------------------------- | -------------------------------------------- |
| Missing capability coverage                        | `SKILL_BUNDLE_COVERAGE_GAP`                  |
| Agent-specific lock-in detected                    | `SKILL_BUNDLE_NOT_AGNOSTIC`                  |
| Reuse branch selected without prior bundle         | `SKILL_BUNDLE_REUSE_BASELINE_MISSING`        |
| Reuse branch selected with invalid baseline bundle | `SKILL_BUNDLE_REUSE_INVALID`                 |
| Trigger evaluation input set is incomplete         | `SKILL_BUNDLE_TRIGGER_EVALUATION_INCOMPLETE` |

---

## BuildAndImproveTestEvidence

**Type:** Operation (mutation)
**Actor:** Runtime execution engine
**Triggers:** Codebase map and valid skill bundle context (recomposed or reused) are available

Creates or improves the test suite with required integration/e2e/functional coverage and optional perf/load scope on explicit request.

### Input

| Field                   | Type                                                             | Required | Description                                                                                            |
| ----------------------- | ---------------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------ |
| cycleId                 | string                                                           | yes      | Parent [ExecutionCycle](domain.md#executioncycle).cycleId                                              |
| passId                  | string                                                           | yes      | Active child pass identifier                                                                           |
| testScope               | [TestScopeLevel](domain.md#testscopelevel)[]                     | yes      | Requested test scope levels                                                                            |
| includePerf             | boolean                                                          | yes      | Performance tests requested                                                                            |
| includeLoad             | boolean                                                          | yes      | Load tests requested                                                                                   |
| optionalScopeRequestRef | string                                                           | no       | Explicit request artifact required for optional perf/load scopes                                       |
| mapRef                  | string                                                           | yes      | [CodebaseKnowledgeMap](domain.md#codebaseknowledgemap) reference                                       |
| runtimeMode             | [ExecutionRuntimeMode](domain.md#executionruntimemode)           | yes      | Selected runtime mode (`sandcastle` by default)                                                        |
| fallbackPolicyRef       | string                                                           | no       | Required when [BuildAndImproveTestEvidence](#buildandimprovetestevidence) falls back from `sandcastle` |
| fallbackOrderPolicyRef  | string                                                           | no       | Optional approved per-project fallback-order policy artifact                                           |
| availabilityProbeRefs   | string[]                                                         | no       | Required when runtime mode falls back from `sandcastle`                                                |
| fallbackDecisionId      | string                                                           | no       | Required when runtime mode falls back from `sandcastle`                                                |
| fallbackApprovedAt      | string (ISO-8601)                                                | no       | Required when runtime mode falls back from `sandcastle`                                                |
| fallbackExpiresAt       | string (ISO-8601)                                                | no       | Required when runtime mode falls back from `sandcastle` and `fallbackNonExpiring=false`                |
| fallbackNonExpiring     | boolean                                                          | no       | Required when runtime mode falls back from `sandcastle`                                                |
| fallbackFrom            | [ExecutionRuntimeMode](domain.md#executionruntimemode)           | no       | Required when runtime mode falls back from `sandcastle`                                                |
| fallbackTo              | [ExecutionRuntimeMode](domain.md#executionruntimemode)           | no       | Required when runtime mode falls back from `sandcastle`; must equal `runtimeMode`                      |
| fallbackReasonCode      | [RuntimeFallbackReasonCode](domain.md#runtimefallbackreasoncode) | no       | Required when runtime mode falls back from `sandcastle`                                                |
| fallbackResolverStage   | [RuntimeInvokingStage](domain.md#runtimeinvokingstage)           | no       | Required when runtime mode falls back from `sandcastle`; must be `testing`                             |
| fallbackEvaluatedAt     | string (ISO-8601)                                                | no       | Required when runtime mode falls back from `sandcastle`                                                |

### Rules

| ID  | Rule                                                           | Formal                                                                                                                                                                                                            |
| --- | -------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| R1  | Integration/e2e/functional slices are mandatory                | See [TestScopePolicy](rules.md#testscopepolicy)                                                                                                                                                                   |
| R2  | Perf/load are opt-in only with explicit request artifact       | `includePerf or includeLoad -> optionalScopeRequestRef != null`                                                                                                                                                   |
| R3  | Test-evidence runtime fallback requires strong policy evidence | `runtimeMode!=sandcastle -> fallbackPolicyRef != null and count(availabilityProbeRefs)>=1 and fallbackDecisionId != null and fallbackApprovedAt != null and fallbackNonExpiring != null`                          |
| R4  | Fallback runtime mode selection is deterministic and auditable | `runtimeMode!=sandcastle -> fallbackTo=runtimeMode and runtimeMode = firstApprovedAvailable(approvedOrder(fallbackOrderPolicyRef) or [sandcastle,vscode-copilot,claude-code]) and fallbackDecisionPersisted=true` |
| R5  | Fallback runtime mode metadata is stage-bound                  | `runtimeMode!=sandcastle -> fallbackFrom != null and fallbackReasonCode != null and fallbackResolverStage=testing and fallbackEvaluatedAt != null`                                                                |
| R6  | Expiring fallback approvals must be time-valid at evaluation   | `runtimeMode!=sandcastle and fallbackNonExpiring=false -> fallbackExpiresAt > fallbackEvaluatedAt`                                                                                                                |

### State Transition

[ExecutionCycle](domain.md#executioncycle): `testing -> evaluating`

### Postconditions

- Test evidence artifacts are produced for required `integration`, `e2e`, and `functional` scope.
- Optional perf/load evidence is present only when requested.
- [ExecutionCycle](domain.md#executioncycle).runtimeMode remains consistent with the selected runtime mode for this pass.

### Error States

| Condition                                          | Result                                         |
| -------------------------------------------------- | ---------------------------------------------- |
| Required test scope missing                        | `TEST_SCOPE_REQUIRED_MISSING`                  |
| Optional scope enabled without request             | `TEST_SCOPE_OPTIONAL_POLICY_VIOLATION`         |
| Optional scope request artifact missing            | `TEST_SCOPE_REQUEST_ARTIFACT_MISSING`          |
| Selected runtime mode unavailable                  | `RUNTIME_MODE_UNAVAILABLE`                     |
| Missing fallback policy evidence                   | `TEST_EXECUTION_FALLBACK_POLICY_MISSING`       |
| Missing required fallback decision evidence fields | `TEST_EXECUTION_FALLBACK_EVIDENCE_INCOMPLETE`  |
| Invalid fallback order override policy artifact    | `TEST_EXECUTION_FALLBACK_ORDER_POLICY_INVALID` |
| Expired fallback approval artifact                 | `TEST_EXECUTION_FALLBACK_APPROVAL_EXPIRED`     |
| Runtime mode outside governed enum                 | `RUNTIME_MODE_UNSUPPORTED`                     |

---

## EvaluateWithSonarQualityGate

**Type:** Operation (mutation)
**Actor:** Sonar evaluator
**Triggers:** Test evidence is available

Runs Sonar analysis against the selected [QualityGateProfile](domain.md#qualitygateprofile).

### Input

| Field                  | Type     | Required | Description                                                               |
| ---------------------- | -------- | -------- | ------------------------------------------------------------------------- |
| cycleId                | string   | yes      | Parent [ExecutionCycle](domain.md#executioncycle).cycleId                 |
| passId                 | string   | yes      | Active child pass identifier                                              |
| gateProfileId          | string   | yes      | Selected [QualityGateProfile](domain.md#qualitygateprofile).gateProfileId |
| sonarProjectKey        | string   | yes      | Sonar project identifier                                                  |
| testEvidenceRefs       | string[] | yes      | Evidence references from test stage                                       |
| retryAttempt           | integer  | yes      | Current retry attempt index (`0` initial run, `1` bounded retry)          |
| remediationEvidenceRef | string   | no       | Required when `retryAttempt=1`                                            |

### Rules

| ID  | Rule                                                            | Formal                                                                      |
| --- | --------------------------------------------------------------- | --------------------------------------------------------------------------- |
| R1  | Sonar run must use selected gate profile                        | `sonar.gateProfileId = gateProfileId`                                       |
| R2  | Sonar precondition requires integration/e2e/functional evidence | `hasEvidence(integration) and hasEvidence(e2e) and hasEvidence(functional)` |
| R3  | Sonar retry is bounded to one retry                             | `retryAttempt in {0,1}`                                                     |
| R4  | Retry attempt requires remediation evidence                     | `retryAttempt=1 -> remediationEvidenceRef != null`                          |
| R5  | Retry failure ends with deterministic terminal outcome          | `retryAttempt=1 and sonarFailed=true -> nextState=failed`                   |

### Calculations

| ID  | Calculation         | Formula                                      |
| --- | ------------------- | -------------------------------------------- |
| C1  | Gate pass ratio     | `passedConditions/totalConditions`           |
| C2  | Quality trend delta | `currentQualityScore - previousQualityScore` |

### State Transition

[ExecutionCycle](domain.md#executioncycle): `evaluating -> evaluating | bundling | failed`

### Postconditions

- On success, Sonar findings are persisted and linked to cycle.
- On success, gate verdict is recorded for trend reporting.
- On first failure (`retryAttempt=0`), one retry is scheduled and [ExecutionCycle](domain.md#executioncycle).sonarRetryAttemptCount is incremented.
- On retry failure (`retryAttempt=1`), [ExecutionCycle](domain.md#executioncycle) transitions to deterministic terminal `failed` state.

### Error States

| Condition                                    | Result                                     |
| -------------------------------------------- | ------------------------------------------ |
| Sonar analysis failed on initial attempt     | `SONAR_EVALUATION_FAILED_RETRY_SCHEDULED`  |
| Sonar analysis failed after bounded retry    | `SONAR_RETRY_TERMINAL_FAILED`              |
| Retry attempt exceeds bounded policy         | `SONAR_RETRY_LIMIT_EXCEEDED`               |
| Retry attempted without remediation evidence | `SONAR_RETRY_REMEDIATION_EVIDENCE_MISSING` |
| Missing gate profile                         | `SONAR_GATE_PROFILE_MISSING`               |
| Missing required evidence scope              | `SONAR_REQUIRED_EVIDENCE_MISSING`          |

---

## BundleFindingsByContext

**Type:** Operation (mutation)
**Actor:** Finding classifier
**Triggers:** Sonar findings are available

Categorizes and groups findings by type and context bundle for remediation planning.

### Input

| Field         | Type     | Required | Description                                                      |
| ------------- | -------- | -------- | ---------------------------------------------------------------- |
| cycleId       | string   | yes      | Parent [ExecutionCycle](domain.md#executioncycle).cycleId        |
| findingRefs   | string[] | yes      | Sonar finding references                                         |
| contextMapRef | string   | yes      | [CodebaseKnowledgeMap](domain.md#codebaseknowledgemap) reference |

### Rules

| ID  | Rule                                            | Formal                                                  |
| --- | ----------------------------------------------- | ------------------------------------------------------- |
| R1  | Every finding belongs to at least one bundle    | `forall finding in findingRefs, exists bundle(finding)` |
| R2  | Bundle context key must use controlled taxonomy | `bundle.contextTag in enum(FindingContextTag)`          |
| R3  | Context tag precedence is deterministic         | `contextTag=argmin(precedence(matchedContextTags))`     |

### State Transition

[ExecutionCycle](domain.md#executioncycle): `bundling -> tasking`

### Postconditions

- [FindingBundle](domain.md#findingbundle) artifacts are generated.
- Bundle references are attached to the cycle.
- [FindingBundle](domain.md#findingbundle).contextTag is resolved using [FindingContextTagPolicy](rules.md#findingcontexttagpolicy).

### Error States

| Condition                               | Result                        |
| --------------------------------------- | ----------------------------- |
| Unclassified finding remains            | `FINDING_BUNDLE_UNCLASSIFIED` |
| Context tag outside controlled taxonomy | `FINDING_CONTEXT_TAG_INVALID` |

---

## CreateAndExportRemediationTasks

**Type:** Operation (mutation)
**Actor:** Task orchestration runtime
**Triggers:** Finding bundles are finalized

Creates repository remediation tasks and exports them to GitHub and Jira as epics/projects/stories via API-first integrations.

### Input

| Field           | Type     | Required | Description                                               |
| --------------- | -------- | -------- | --------------------------------------------------------- |
| cycleId         | string   | yes      | Parent [ExecutionCycle](domain.md#executioncycle).cycleId |
| bundleIds       | string[] | yes      | Source [FindingBundle](domain.md#findingbundle) IDs       |
| githubConfigRef | string   | yes      | GitHub integration configuration reference                |
| jiraConfigRef   | string   | yes      | Jira integration configuration reference                  |

### Rules

| ID  | Rule                                                 | Formal                                                                      |
| --- | ---------------------------------------------------- | --------------------------------------------------------------------------- |
| R1  | Integration path is API-first                        | See [ApiFirstTaskIntegrationPolicy](rules.md#apifirsttaskintegrationpolicy) |
| R2  | Every created task links back to bundle context      | `forall task, length(task.bundleRefs)>=1`                                   |
| R3  | Export status transitions must be explicit and valid | `transition(task.exportStatus,event) in allowed(TaskExportStatus)`          |

### State Transition

[ExecutionCycle](domain.md#executioncycle): `tasking -> tasking`

### Postconditions

- Repository tasks are created.
- GitHub and Jira export references are recorded per task.
- Each [RemediationTask](domain.md#remediationtask) reaches explicit `both-exported`, `export-partial`, `retry-pending`, `retrying`, or `export-failed` state.

### Error States

| Condition                        | Result                                  |
| -------------------------------- | --------------------------------------- |
| GitHub export failed             | `TASK_EXPORT_GITHUB_FAILED`             |
| Jira export failed               | `TASK_EXPORT_JIRA_FAILED`               |
| Both exports failed              | `TASK_EXPORT_TOTAL_FAILED`              |
| Invalid export status transition | `TASK_EXPORT_STATUS_TRANSITION_INVALID` |
| Retry budget exhausted           | `TASK_EXPORT_RETRY_EXHAUSTED`           |

---

## GenerateThreeCandidateSolutions

**Type:** Operation (mutation)
**Actor:** Solution synthesis runtime
**Triggers:** Remediation task is created

Generates exactly three candidate solutions per task: established pattern, hybrid adaptation, and new pattern.

### Input

| Field                  | Type                                                             | Required | Description                                                                                                    |
| ---------------------- | ---------------------------------------------------------------- | -------- | -------------------------------------------------------------------------------------------------------------- |
| taskId                 | string                                                           | yes      | Target [RemediationTask](domain.md#remediationtask).taskId                                                     |
| bundleRefs             | string[]                                                         | yes      | Source finding context                                                                                         |
| patternCatalogRef      | string                                                           | yes      | Existing/new patterns catalog reference                                                                        |
| runtimeMode            | [ExecutionRuntimeMode](domain.md#executionruntimemode)           | yes      | Selected runtime mode (`sandcastle` by default)                                                                |
| fallbackPolicyRef      | string                                                           | no       | Required when [GenerateThreeCandidateSolutions](#generatethreecandidatesolutions) falls back from `sandcastle` |
| fallbackOrderPolicyRef | string                                                           | no       | Optional approved per-project fallback-order policy artifact                                                   |
| availabilityProbeRefs  | string[]                                                         | no       | Required when runtime mode falls back from `sandcastle`                                                        |
| fallbackDecisionId     | string                                                           | no       | Required when runtime mode falls back from `sandcastle`                                                        |
| fallbackApprovedAt     | string (ISO-8601)                                                | no       | Required when runtime mode falls back from `sandcastle`                                                        |
| fallbackExpiresAt      | string (ISO-8601)                                                | no       | Required when runtime mode falls back from `sandcastle` and `fallbackNonExpiring=false`                        |
| fallbackNonExpiring    | boolean                                                          | no       | Required when runtime mode falls back from `sandcastle`                                                        |
| fallbackFrom           | [ExecutionRuntimeMode](domain.md#executionruntimemode)           | no       | Required when runtime mode falls back from `sandcastle`                                                        |
| fallbackTo             | [ExecutionRuntimeMode](domain.md#executionruntimemode)           | no       | Required when runtime mode falls back from `sandcastle`; must equal `runtimeMode`                              |
| fallbackReasonCode     | [RuntimeFallbackReasonCode](domain.md#runtimefallbackreasoncode) | no       | Required when runtime mode falls back from `sandcastle`                                                        |
| fallbackResolverStage  | [RuntimeInvokingStage](domain.md#runtimeinvokingstage)           | no       | Required when runtime mode falls back from `sandcastle`; must be `solution-synthesis`                          |
| fallbackEvaluatedAt    | string (ISO-8601)                                                | no       | Required when runtime mode falls back from `sandcastle`                                                        |

### Rules

| ID  | Rule                                                                | Formal                                                                                                                                                                                                            |
| --- | ------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| R1  | Exactly three candidates are required                               | See [ThreeCandidateSolutionRule](rules.md#threecandidatesolutionrule)                                                                                                                                             |
| R2  | Candidate set must include established and new-pattern perspectives | `exists established and exists new-pattern`                                                                                                                                                                       |
| R3  | Solution synthesis runtime fallback requires strong policy evidence | `runtimeMode!=sandcastle -> fallbackPolicyRef != null and count(availabilityProbeRefs)>=1 and fallbackDecisionId != null and fallbackApprovedAt != null and fallbackNonExpiring != null`                          |
| R4  | Fallback runtime mode selection is deterministic and auditable      | `runtimeMode!=sandcastle -> fallbackTo=runtimeMode and runtimeMode = firstApprovedAvailable(approvedOrder(fallbackOrderPolicyRef) or [sandcastle,vscode-copilot,claude-code]) and fallbackDecisionPersisted=true` |
| R5  | Fallback runtime mode metadata is stage-bound                       | `runtimeMode!=sandcastle -> fallbackFrom != null and fallbackReasonCode != null and fallbackResolverStage=solution-synthesis and fallbackEvaluatedAt != null`                                                     |
| R6  | Expiring fallback approvals must be time-valid at evaluation        | `runtimeMode!=sandcastle and fallbackNonExpiring=false -> fallbackExpiresAt > fallbackEvaluatedAt`                                                                                                                |

### State Transition

[ExecutionCycle](domain.md#executioncycle): `tasking -> tasking`

### Postconditions

- [RemediationTask](domain.md#remediationtask).candidateSolutions has exactly three entries.
- [ExecutionCycle](domain.md#executioncycle).runtimeMode remains consistent with the selected runtime mode for this pass.

### Error States

| Condition                                          | Result                                             |
| -------------------------------------------------- | -------------------------------------------------- |
| Fewer or more than three candidates                | `SOLUTION_CANDIDATE_COUNT_INVALID`                 |
| Missing required perspective                       | `SOLUTION_CANDIDATE_PERSPECTIVE_GAP`               |
| Selected runtime mode unavailable                  | `RUNTIME_MODE_UNAVAILABLE`                         |
| Missing fallback policy evidence                   | `SOLUTION_SYNTHESIS_FALLBACK_POLICY_MISSING`       |
| Missing required fallback decision evidence fields | `SOLUTION_SYNTHESIS_FALLBACK_EVIDENCE_INCOMPLETE`  |
| Invalid fallback order override policy artifact    | `SOLUTION_SYNTHESIS_FALLBACK_ORDER_POLICY_INVALID` |
| Expired fallback approval artifact                 | `SOLUTION_SYNTHESIS_FALLBACK_APPROVAL_EXPIRED`     |
| Runtime mode outside governed enum                 | `RUNTIME_MODE_UNSUPPORTED`                         |

---

## SynthesizeCrossSmellAbstractions

**Type:** Operation (mutation)
**Actor:** Architecture synthesis runtime
**Triggers:** Candidate sets are available across multiple tasks

Finds abstractions that solve multiple smell clusters without redundant or conflicting patterns.

### Input

| Field         | Type     | Required | Description                                               |
| ------------- | -------- | -------- | --------------------------------------------------------- |
| cycleId       | string   | yes      | Parent [ExecutionCycle](domain.md#executioncycle).cycleId |
| taskIds       | string[] | yes      | Task set to inspect                                       |
| candidateRefs | string[] | yes      | Candidate solution references                             |

### Rules

| ID  | Rule                                                    | Formal                                                                             |
| --- | ------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| R1  | Abstraction must map to at least two smell bundles      | `coverage(abstraction,bundles) >= 2`                                               |
| R2  | Redundant abstraction proposals are rejected            | See [NonRedundantAbstractionRule](rules.md#nonredundantabstractionrule)            |
| R3  | Accepted abstraction must pass score threshold          | `abstractionScore >= 0.70`                                                         |
| R4  | Equal-score proposals use deterministic tie-break order | `tieBreakOrder(coverageScore,overlapPenalty,severityReductionScore,abstractionId)` |

### Calculations

| ID  | Calculation          | Formula                                                                                                               |
| --- | -------------------- | --------------------------------------------------------------------------------------------------------------------- |
| C1  | Abstraction score    | `0.45*coverageScore + 0.30*severityReductionScore + 0.15*feasibilityScore + 0.10*learningReuseScore - overlapPenalty` |
| C2  | Acceptance threshold | `abstractionScore >= 0.70`                                                                                            |

### State Transition

[ExecutionCycle](domain.md#executioncycle): `tasking -> learning`

### Postconditions

- Cross-smell abstraction proposals are attached to tasks.
- Redundant proposals are filtered out.

### Error States

| Condition                            | Result                                |
| ------------------------------------ | ------------------------------------- |
| No multi-smell abstraction candidate | `ABSTRACTION_MULTI_SMELL_NOT_FOUND`   |
| Redundancy threshold exceeded        | `ABSTRACTION_REDUNDANCY_VIOLATION`    |
| Score threshold not met              | `ABSTRACTION_SCORE_THRESHOLD_NOT_MET` |

---

## ApplyOperatorSelectionLearning

**Type:** Operation (mutation)
**Actor:** Operator + learning runtime
**Triggers:** Operator selects one candidate for a task

Persists operator selections and outcomes to [LearningMemory](domain.md#learningmemory) for future ranking and strategy adaptation.

### Input

| Field               | Type   | Required | Description                                                           |
| ------------------- | ------ | -------- | --------------------------------------------------------------------- |
| cycleId             | string | yes      | Parent [ExecutionCycle](domain.md#executioncycle).cycleId             |
| taskId              | string | yes      | Source [RemediationTask](domain.md#remediationtask).taskId            |
| selectedCandidateId | string | yes      | Selected [SolutionCandidate](domain.md#solutioncandidate).candidateId |
| selectionReason     | string | yes      | Operator rationale                                                    |
| observedOutcome     | string | yes      | Post-application outcome summary                                      |

### Rules

| ID  | Rule                                                    | Formal                                                    |
| --- | ------------------------------------------------------- | --------------------------------------------------------- |
| R1  | Selection must reference one of the task's candidates   | `selectedCandidateId in task.candidateSolutions`          |
| R2  | Learning record requires rationale and observed outcome | `selectionReason != null and observedOutcome != null`     |
| R3  | Learning updates influence subsequent ranking           | See [LearningFeedbackRule](rules.md#learningfeedbackrule) |

### State Transition

[ExecutionCycle](domain.md#executioncycle): `learning -> checkpoint`

### Postconditions

- [LearningMemory](domain.md#learningmemory) entry is persisted.
- Candidate ranking signals are updated for next cycle.

### Error States

| Condition                    | Result                         |
| ---------------------------- | ------------------------------ |
| Selected candidate not found | `LEARNING_SELECTION_INVALID`   |
| Missing rationale/outcome    | `LEARNING_EVIDENCE_INCOMPLETE` |

---

## RecordCycleTelemetryTrend

**Type:** Operation (mutation)
**Actor:** Telemetry runtime
**Triggers:** Pass stage boundary reached and completion candidacy evaluation requested

Captures interactions, task outcomes, and quality trend metrics for the cycle.

### Input

| Field                              | Type                                                             | Required | Description                                                                                                                                                  |
| ---------------------------------- | ---------------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| cycleId                            | string                                                           | yes      | Target [ExecutionCycle](domain.md#executioncycle).cycleId                                                                                                    |
| passId                             | string                                                           | yes      | Active child pass identifier                                                                                                                                 |
| runtimeMode                        | [ExecutionRuntimeMode](domain.md#executionruntimemode)           | yes      | Runtime mode used for this pass (`sandcastle` default or governed fallback)                                                                                  |
| fallbackPolicyRef                  | string                                                           | no       | Required when runtime fallback is used (`runtimeMode != sandcastle`)                                                                                         |
| fallbackOrderPolicyRef             | string                                                           | no       | Optional approved per-project fallback-order policy artifact used during fallback resolution                                                                 |
| availabilityProbeRefs              | string[]                                                         | no       | Required when runtime fallback is used; probe evidence refs for evaluated runtime modes                                                                      |
| fallbackFrom                       | [ExecutionRuntimeMode](domain.md#executionruntimemode)           | no       | Required when runtime fallback is used                                                                                                                       |
| fallbackTo                         | [ExecutionRuntimeMode](domain.md#executionruntimemode)           | no       | Required when runtime fallback is used; must equal `runtimeMode`                                                                                             |
| fallbackReasonCode                 | [RuntimeFallbackReasonCode](domain.md#runtimefallbackreasoncode) | no       | Required when runtime fallback is used                                                                                                                       |
| fallbackDecisionId                 | string                                                           | no       | Required when runtime fallback is used                                                                                                                       |
| fallbackApprovedAt                 | string (ISO-8601)                                                | no       | Required when runtime fallback is used                                                                                                                       |
| fallbackExpiresAt                  | string (ISO-8601)                                                | no       | Required when runtime fallback is used and `fallbackNonExpiring=false`                                                                                       |
| fallbackNonExpiring                | boolean                                                          | no       | Required when runtime fallback is used                                                                                                                       |
| fallbackResolverStage              | [RuntimeInvokingStage](domain.md#runtimeinvokingstage)           | no       | Required when runtime fallback is used                                                                                                                       |
| fallbackEvaluatedAt                | string (ISO-8601)                                                | no       | Required when runtime fallback is used                                                                                                                       |
| skillBundleDecision                | string                                                           | yes      | Skill bundle branch decision for this pass (`recomposed` or `reused`)                                                                                        |
| skillBundleDecisionRef             | string                                                           | yes      | Decision evidence reference emitted by [ComposeAgnosticSkillBundle](#composeagnosticskillbundle)                                                             |
| reusedBundleRef                    | string                                                           | no       | Required when `skillBundleDecision=reused`                                                                                                                   |
| recomposedBundleVersion            | string                                                           | no       | Required when `skillBundleDecision=recomposed`                                                                                                               |
| stageEventRefs                     | string[]                                                         | yes      | Stage-level telemetry event references emitted for this pass                                                                                                 |
| interactionCount                   | integer                                                          | yes      | Number of operator/agent interactions                                                                                                                        |
| taskOutcomeSummaryRef              | string                                                           | yes      | Task result summary reference                                                                                                                                |
| gatePassRate                       | number                                                           | yes      | Fraction of gate conditions passed                                                                                                                           |
| qualityTrendScore                  | number                                                           | yes      | Normalized trend score                                                                                                                                       |
| checkpointOutcome                  | [ModeControlOutcome](domain.md#modecontroloutcome)               | yes      | Explicit mode-control outcome (`continue`, `pause`, `halt`, `complete`)                                                                                      |
| checkpointIndex                    | integer                                                          | yes      | Checkpoint index correlated to current mode-control decision                                                                                                 |
| checkpointEvaluatedAt              | string (ISO-8601)                                                | yes      | Evaluation timestamp used for override validity checks                                                                                                       |
| stopRequestedAt                    | string (ISO-8601)                                                | no       | Required when `checkpointOutcome=halt`                                                                                                                       |
| haltedAt                           | string (ISO-8601)                                                | no       | Required when `checkpointOutcome=halt`                                                                                                                       |
| haltedCheckpointIndex              | integer                                                          | no       | Required when `checkpointOutcome=halt`; must equal `checkpointIndex`                                                                                         |
| activeExportRetryCount             | integer                                                          | yes      | Count of tasks in `retry-pending` or `retrying`                                                                                                              |
| exportDegradationThresholdBreached | boolean                                                          | yes      | Whether completion gate degradation threshold is breached                                                                                                    |
| riskAcceptedOverrideRef            | string                                                           | no       | Required when completion proceeds under blocked degradation conditions; must reference [RiskAcceptanceOverride](domain.md#riskacceptanceoverride).overrideId |
| riskAcceptedOverrideValidatedAt    | string (ISO-8601)                                                | no       | Required when `riskAcceptedOverrideRef != null`; persisted override validity evaluation timestamp                                                            |
| completionCandidate                | boolean                                                          | yes      | Whether this checkpoint could terminate the parent cycle                                                                                                     |
| terminalCycleSummaryRef            | string                                                           | no       | Required when completion candidate is accepted                                                                                                               |

### Rules

| ID  | Rule                                                                                  | Formal                                                                                                                                                                                                                                                                                                                                                                                  |
| --- | ------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| R1  | Telemetry envelope must be complete                                                   | See [TelemetryCompletenessRule](rules.md#telemetrycompletenessrule)                                                                                                                                                                                                                                                                                                                     |
| R2  | Trend score is bounded                                                                | `qualityTrendScore >= -1 and qualityTrendScore <= 1`                                                                                                                                                                                                                                                                                                                                    |
| R3  | Completion candidate requires terminal summary                                        | `completionCandidate=true -> terminalCycleSummaryRef != null`                                                                                                                                                                                                                                                                                                                           |
| R4  | Halt outcome requires stop compliance proof fields                                    | `checkpointOutcome=halt -> stopRequestedAt != null and haltedAt != null and haltedCheckpointIndex=checkpointIndex`                                                                                                                                                                                                                                                                      |
| R5  | Completion under degraded export conditions requires explicit valid override evidence | `completionCandidate=true and (activeExportRetryCount > 0 or exportDegradationThresholdBreached=true) -> riskAcceptedOverrideRef != null and riskAcceptedOverrideValidatedAt != null`                                                                                                                                                                                                   |
| R6  | Override validity requires active and non-expired (unless non-expiring) artifact      | `riskAcceptedOverrideRef != null -> validRiskAcceptanceOverride(riskAcceptedOverrideRef,checkpointEvaluatedAt)=true`                                                                                                                                                                                                                                                                    |
| R7  | Runtime fallback telemetry is mandatory when non-default runtime mode is used         | `runtimeMode!=sandcastle -> fallbackPolicyRef != null and count(availabilityProbeRefs)>=1 and fallbackFrom != null and fallbackTo=runtimeMode and fallbackReasonCode != null and fallbackDecisionId != null and fallbackApprovedAt != null and fallbackResolverStage != null and fallbackEvaluatedAt != null and (fallbackNonExpiring=true or fallbackExpiresAt > fallbackEvaluatedAt)` |
| R8  | Skill bundle decision branch metadata is mandatory and deterministic                  | `skillBundleDecision in {recomposed,reused} and skillBundleDecisionRef != null and (skillBundleDecision=reused -> reusedBundleRef != null) and (skillBundleDecision=recomposed -> recomposedBundleVersion != null)`                                                                                                                                                                     |

### State Transition

[ExecutionCycle](domain.md#executioncycle): `checkpoint -> checkpoint`

### Postconditions

- [TelemetryEnvelope](domain.md#telemetryenvelope).stageEventRefs is appended.
- [TelemetryEnvelope](domain.md#telemetryenvelope).terminalCycleSummaryRef is persisted when completion candidate is accepted.
- [TelemetryEnvelope](domain.md#telemetryenvelope).runtimeMode is persisted.
- Runtime fallback evidence (`fallbackPolicyRef`, `fallbackOrderPolicyRef`, `availabilityProbeRefs`, `fallbackFrom`, `fallbackTo`, `fallbackReasonCode`, `fallbackDecisionId`, `fallbackApprovedAt`, `fallbackExpiresAt`/`fallbackNonExpiring`, `fallbackResolverStage`, `fallbackEvaluatedAt`) is persisted when `runtimeMode!=sandcastle`.
- Skill bundle branch evidence (`skillBundleDecision`, `skillBundleDecisionRef`, `reusedBundleRef`/`recomposedBundleVersion`) is persisted.
- Stop compliance proof fields are persisted when `checkpointOutcome=halt`.
- Completion gate evidence (`activeExportRetryCount`, `exportDegradationThresholdBreached`, `riskAcceptedOverrideRef`, `riskAcceptedOverrideValidatedAt`) is persisted.
- Quality trend metrics are appended for cross-cycle analysis.

### Error States

| Condition                                                             | Result                                        |
| --------------------------------------------------------------------- | --------------------------------------------- |
| Missing required telemetry field                                      | `TELEMETRY_ENVELOPE_INCOMPLETE`               |
| Invalid trend score range                                             | `TELEMETRY_TREND_SCORE_INVALID`               |
| Completion candidate missing terminal summary                         | `TELEMETRY_TERMINAL_SUMMARY_MISSING`          |
| Halt outcome missing stop compliance proof                            | `TELEMETRY_STOP_PROOF_MISSING`                |
| Completion under degraded export conditions missing override evidence | `TELEMETRY_COMPLETION_OVERRIDE_MISSING`       |
| Completion override artifact invalid, revoked, or expired             | `TELEMETRY_COMPLETION_OVERRIDE_INVALID`       |
| Runtime fallback used without required fallback evidence              | `TELEMETRY_RUNTIME_FALLBACK_EVIDENCE_MISSING` |
| Skill bundle decision branch metadata missing or invalid              | `TELEMETRY_SKILL_BUNDLE_DECISION_MISSING`     |

---

## ApplyModeControlCheckpoint

**Type:** Operation (mutation)
**Actor:** Mode controller
**Triggers:** End of each stage boundary, explicit stop request, or explicit resume request

Applies autonomous checkpoint and stop behavior, assisted pause outcomes, and resumable halted checkpoint-holds before allowing next stage transition.

### Input

| Field                           | Type                                                   | Required | Description                                                                                                                     |
| ------------------------------- | ------------------------------------------------------ | -------- | ------------------------------------------------------------------------------------------------------------------------------- |
| cycleId                         | string                                                 | yes      | Target [ExecutionCycle](domain.md#executioncycle).cycleId                                                                       |
| mode                            | [OperationMode](domain.md#operationmode)               | yes      | Cycle operation mode                                                                                                            |
| runtimeMode                     | [ExecutionRuntimeMode](domain.md#executionruntimemode) | yes      | Runtime mode active for this checkpoint decision                                                                                |
| checkpointControl               | [CheckpointControl](domain.md#checkpointcontrol)       | yes      | Current checkpoint state                                                                                                        |
| telemetryEnvelopeRef            | string                                                 | yes      | Latest [TelemetryEnvelope](domain.md#telemetryenvelope) reference                                                               |
| resumeRequested                 | boolean                                                | yes      | Explicit request to resume from `halted` checkpoint-hold                                                                        |
| completionRequested             | boolean                                                | yes      | Request to close parent cycle after current pass                                                                                |
| checkpointEvaluatedAt           | string (ISO-8601)                                      | yes      | Decision timestamp used for override validity evaluation                                                                        |
| riskAcceptedOverrideRef         | string                                                 | no       | Explicit [RiskAcceptanceOverride](domain.md#riskacceptanceoverride).overrideId required for completion under export degradation |
| riskAcceptedOverrideValidatedAt | string (ISO-8601)                                      | no       | Required when `riskAcceptedOverrideRef != null`; records when override validity was confirmed                                   |

### Rules

| ID  | Rule                                                                                                                      | Formal                                                                                                                                                                                                            |
| --- | ------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| R1  | Autonomous mode must checkpoint at configured boundaries                                                                  | `mode=autonomous -> checkpointIndex increments on boundary`                                                                                                                                                       |
| R2  | Stop request from checkpoint control must halt at next checkpoint                                                         | `checkpointControl.stopRequested=true -> nextState=halted`                                                                                                                                                        |
| R3  | Assisted mode requires explicit pause for unresolved guarded transitions                                                  | `mode=assisted and guardedTransition=true and unresolved=true -> nextState=checkpoint and modeControlOutcome=pause`                                                                                               |
| R4  | Completion decisions are authoritative only from mode control                                                             | `nextState=completed -> completionDecisionSource=mode-control`                                                                                                                                                    |
| R5  | Continue decision mints next child pass identifier                                                                        | `nextState=mapping -> newPassId appended to passIds`                                                                                                                                                              |
| R6  | Completion is blocked while export retries are active or degradation threshold is breached unless a valid override exists | `completionRequested=true and (activeExportRetryCount > 0 or exportDegradationThresholdBreached=true) and not validRiskAcceptanceOverride(riskAcceptedOverrideRef,checkpointEvaluatedAt) -> nextState!=completed` |
| R7  | Halted state resumes only via explicit resume request with stop cleared                                                   | `state=halted and resumeRequested=true and checkpointControl.stopRequested=false -> nextState=checkpoint`                                                                                                         |
| R8  | Halt outcome requires stopRequestedAt, haltedAt, and checkpoint-index correlation                                         | `nextState=halted -> stopRequestedAt != null and haltedAt != null and haltedCheckpointIndex=checkpointIndex`                                                                                                      |
| R9  | Override validity evidence must be persisted when override is used                                                        | `riskAcceptedOverrideRef != null -> riskAcceptedOverrideValidatedAt != null`                                                                                                                                      |

### State Transition

[ExecutionCycle](domain.md#executioncycle): `checkpoint | halted -> mapping | checkpoint | halted | completed`

### Postconditions

- Checkpoint evidence is stored.
- Stop, pause, and approval outcomes are recorded for auditability.
- [ExecutionCycle](domain.md#executioncycle).completionDecisionSource is set to `mode-control` for terminal completion.
- [ExecutionCycle](domain.md#executioncycle).modeControlOutcome is set to explicit `continue`, `pause`, `halt`, or `complete`.
- On halt, [CheckpointControl](domain.md#checkpointcontrol).stopRequestedAt and [CheckpointControl](domain.md#checkpointcontrol).haltedAt are persisted with checkpoint index correlation.
- On continue, [ExecutionCycle](domain.md#executioncycle).activePassId advances to a new child pass identifier.
- On resume from `halted`, cycle returns to `checkpoint` for explicit follow-up decision.
- When used, [CheckpointControl](domain.md#checkpointcontrol).riskAcceptedOverrideValidatedAt is persisted with the evaluated override reference.

### Error States

| Condition                                                           | Result                                   |
| ------------------------------------------------------------------- | ---------------------------------------- |
| Missing checkpoint evidence in autonomous mode                      | `AUTONOMOUS_CHECKPOINT_MISSING`          |
| Stop request ignored                                                | `STOP_CONTROL_VIOLATION`                 |
| Completion decision attempted outside mode control                  | `COMPLETION_DECISION_UNAUTHORIZED`       |
| Completion requested without terminal summary                       | `COMPLETION_TERMINAL_SUMMARY_MISSING`    |
| Completion blocked by active export retries without override        | `COMPLETION_BLOCKED_EXPORT_RETRY_ACTIVE` |
| Completion blocked by export degradation threshold without override | `COMPLETION_BLOCKED_EXPORT_DEGRADATION`  |
| Completion override artifact invalid, revoked, or expired           | `COMPLETION_OVERRIDE_INVALID_OR_EXPIRED` |
| Halted transition missing stop compliance proof fields              | `HALT_STOP_PROOF_MISSING`                |
