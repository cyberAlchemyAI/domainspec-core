---
feature: sonar-loop
version: current
status: draft
updatedAt: 2026-05-12
---

# Sonar Loop Stories

> Navigate by capability: [Quality Gate Targeting and Policy](#quality-gate-targeting-and-policy) · [Codebase Intelligence Mapping](#codebase-intelligence-mapping) · [Test Evidence and Sonar Evaluation](#test-evidence-and-sonar-evaluation) · [Task Orchestration, Solution Synthesis, and Learning](#task-orchestration-solution-synthesis-and-learning)

## User Journey Alignment

| Journey stage            | Approved decisions                                                                                             | Story anchors          |
| ------------------------ | -------------------------------------------------------------------------------------------------------------- | ---------------------- |
| Evaluator day 0-day 1    | Wave 1 (`Q1=A`, `Q2=C`, `Q3=B`, `Q4=C`)                                                                        | US-003, US-006, US-007 |
| Pilot week 1             | Wave 2 (`Q5=B`, `Q6=A`, `Q7=A`, `Q8=A`)                                                                        | US-002, US-005, US-006 |
| Scale month 1            | Wave 3 (`Q9=A`, `Q10=A`, `Q11=A`, `Q12=C`)                                                                     | US-002, US-003, US-007 |
| Packaging/pricing/growth | Wave 4 (`Q13=A` primary with `B` secondary intent, `Q14=A` one-time non-SaaS per-repository, `Q15=A`, `Q16=A`) | US-007, US-008         |

See detailed journey docs: [userjourney/README.md](userjourney/README.md).

## Quality Gate Targeting and Policy

### US-001 Select Progressive Quality Gate

As an **operator**, I want **the system to select a valid target quality gate for each cycle**, so that **quality progression is controlled and measurable**.

**Given** a new [ExecutionCycle](domain.md#executioncycle)
**When** [DetermineTargetQualityGate](operations.md#determinetargetqualitygate) runs
**Then** selected gate progression follows [QualityGateProgressionPolicy](rules.md#qualitygateprogressionpolicy).

**Acceptance checks**

- [ ] Gate jumps beyond one level are rejected unless rollback rationale is explicit.
- [ ] Gate downgrades persist mandatory `rollbackReason` in gate policy evidence.
- [ ] Selected gate is persisted in cycle state.
- [ ] Checkpoint policy is bound to selected mode.

**Domain coverage**

- Concepts: [ExecutionCycle](domain.md#executioncycle), [QualityGateProfile](domain.md#qualitygateprofile)
- Rules: [QualityGateProgressionPolicy](rules.md#qualitygateprogressionpolicy), [AutonomousCheckpointAndStopPolicy](rules.md#autonomouscheckpointandstoppolicy)
- Interfaces/Flows: [ModeControlInterface](interfaces.md#internal-modecontrolinterface), [ProgressiveQualityLoopWorkflow](workflows.md#progressivequalityloopworkflow)

**Covered concept IDs**

- `sonar-loop.ExecutionCycle`
- `sonar-loop.QualityGateProfile`
- `sonar-loop.DetermineTargetQualityGate`
- `sonar-loop.QualityGateProgressionPolicy`

**Capability links**

- [Quality Gate Targeting and Policy](SPEC.md#quality-gate-targeting-and-policy)

### US-002 Enforce Autonomous Checkpoint and Stop Control

As an **autonomous-mode operator**, I want **checkpoint and stop controls**, so that **long-running loop execution can be safely paused**.

**Given** mode is `autonomous`
**When** a checkpoint boundary is reached with stop requested
**Then** [ApplyModeControlCheckpoint](operations.md#applymodecontrolcheckpoint) transitions cycle to `halted`.

**Acceptance checks**

- [ ] [CheckpointControl](domain.md#checkpointcontrol) is the authoritative stop signal source.
- [ ] `pause` is an explicit first-class mode-control outcome.
- [ ] Stop requests are applied at next checkpoint.
- [ ] Halted cycles preserve existing artifacts and remain resumable checkpoint-holds.
- [ ] Stop compliance proof persists `stopRequestedAt`, `haltedAt`, and `haltedCheckpointIndex` with checkpoint correlation.
- [ ] Completion decisions are authoritative only via [ApplyModeControlCheckpoint](operations.md#applymodecontrolcheckpoint).
- [ ] Checkpoint outcome telemetry is emitted.

**Domain coverage**

- Concepts: [CheckpointControl](domain.md#checkpointcontrol), [ExecutionCycle](domain.md#executioncycle)
- Rules: [AutonomousCheckpointAndStopPolicy](rules.md#autonomouscheckpointandstoppolicy)
- Interfaces/Flows: [ModeControlInterface](interfaces.md#internal-modecontrolinterface), [AutonomousCheckpointWorkflow](workflows.md#autonomouscheckpointworkflow)

**Covered concept IDs**

- `sonar-loop.CheckpointControl`
- `sonar-loop.ApplyModeControlCheckpoint`
- `sonar-loop.AutonomousCheckpointAndStopPolicy`
- `sonar-loop.ModeControlOutcome`
- `sonar-loop.CompletionDecisionSource`

**Capability links**

- [Quality Gate Targeting and Policy](SPEC.md#quality-gate-targeting-and-policy)

## Codebase Intelligence Mapping

### US-003 Build Full TS Codebase Intelligence Map

As a **maintainer**, I want **the system to map dependencies, use-cases, rules, patterns, modules, APIs, architecture, and libraries**, so that **remediation planning uses real context**.

**Given** repository ingestion is complete
**When** [MapCodebaseIntelligence](operations.md#mapcodebaseintelligence) executes via selected [ExecutionRuntimeMode](domain.md#executionruntimemode)
**Then** [CodebaseKnowledgeMap](domain.md#codebaseknowledgemap) includes all required dimensions.

**Acceptance checks**

- [ ] Missing dimensions fail map validation.
- [ ] Map artifacts are linked to cycle context.
- [ ] Mapping runtime mode is explicit (`sandcastle`, `vscode-copilot`, or `claude-code`) and persisted in cycle state.
- [ ] Mapping fallback requires explicit `fallbackPolicyRef` when runtime mode is not `sandcastle`.
- [ ] Mapping fallback uses default deterministic order `sandcastle -> vscode-copilot -> claude-code`, unless an approved per-project order override policy artifact is supplied.
- [ ] Mapping fallback evidence minimum includes `fallbackPolicyRef`, `availabilityProbeRefs`, `fallbackDecisionId`, `fallbackApprovedAt`, and explicit `fallbackExpiresAt`/`fallbackNonExpiring`.
- [ ] Mapping fallback decision metadata includes `fallbackFrom`, `fallbackTo`, `fallbackReasonCode`, `fallbackResolverStage`, and `fallbackEvaluatedAt`.

**Domain coverage**

- Concepts: [CodebaseKnowledgeMap](domain.md#codebaseknowledgemap), [ExecutionCycle](domain.md#executioncycle), [ExecutionRuntimeMode](domain.md#executionruntimemode)
- Rules: [CycleStateMachine](rules.md#cyclestatemachine), [ExecutionProviderFallbackPolicy](rules.md#executionproviderfallbackpolicy)
- Interfaces/Flows: [SandcastleAgentExecutionInterface](interfaces.md#internal-sandcastleagentexecutioninterface), [ProgressiveQualityLoopWorkflow](workflows.md#progressivequalityloopworkflow)

**Covered concept IDs**

- `sonar-loop.CodebaseKnowledgeMap`
- `sonar-loop.MapCodebaseIntelligence`
- `sonar-loop.ExecutionRuntimeMode`
- `sonar-loop.SandcastleAgentExecutionInterface`
- `sonar-loop.ExecutionProviderFallbackPolicy`

**Capability links**

- [Codebase Intelligence Mapping](SPEC.md#codebase-intelligence-mapping)

### US-004 Publish Agnostic Skill Bundle

As a **coding agent runtime**, I want **an agnostic skill bundle for this loop**, so that **multiple agent implementations can execute the same capability contracts**.

**Given** a fresh codebase map exists
**When** [ComposeAgnosticSkillBundle](operations.md#composeagnosticskillbundle) evaluates recomposition triggers
**Then** [SkillBundleProfile](domain.md#skillbundleprofile) is recomposed only when triggers are present, otherwise the latest valid bundle is reused.

**Acceptance checks**

- [ ] Recomposition trigger set is deterministic (`previousBundleRef` missing, `capabilityChangeSet` non-empty, `runtimePolicyChangeMarkers` non-empty, `mapDriftIndicators` non-empty, or `forceRecompose=true`).
- [ ] When no trigger is present, reuse branch attaches the latest valid baseline bundle.
- [ ] Reused and recomposed bundles both satisfy agnosticity and full capability coverage.
- [ ] Branch decision evidence is persisted for telemetry/audit continuity.

**Domain coverage**

- Concepts: [SkillBundleProfile](domain.md#skillbundleprofile)
- Rules: [CycleStateMachine](rules.md#cyclestatemachine), [SkillBundleReusePolicy](rules.md#skillbundlereusepolicy)
- Interfaces/Flows: [SkillBundleInterface](interfaces.md#internal-skillbundleinterface)

**Covered concept IDs**

- `sonar-loop.SkillBundleProfile`
- `sonar-loop.ComposeAgnosticSkillBundle`
- `sonar-loop.SkillBundleReusePolicy`
- `sonar-loop.SkillBundleInterface`

**Capability links**

- [Codebase Intelligence Mapping](SPEC.md#codebase-intelligence-mapping)

## Test Evidence and Sonar Evaluation

### US-005 Upgrade Test Evidence Before Sonar Evaluation

As a **quality lead**, I want **integration/e2e/functional test evidence improved before gate evaluation**, so that **Sonar verdicts are based on credible quality signals**.

**Given** codebase map is ready
**When** [BuildAndImproveTestEvidence](operations.md#buildandimprovetestevidence) runs
**Then** required test scope is present and optional perf/load is included only when requested.

**Acceptance checks**

- [ ] Integration/e2e/functional coverage is mandatory.
- [ ] Sonar precondition blocks evaluation unless integration+e2e+functional evidence is present.
- [ ] Perf/load tests are opt-in and require explicit request artifact.
- [ ] Test-evidence execution uses explicit runtime mode selection (`sandcastle`, `vscode-copilot`, or `claude-code`).
- [ ] Test-evidence execution fallback uses the same explicit policy contract as mapping (`fallbackPolicyRef` required when runtime mode is not `sandcastle`).
- [ ] Test-evidence fallback uses default deterministic order `sandcastle -> vscode-copilot -> claude-code`, unless an approved per-project order override policy artifact is supplied.
- [ ] Test-evidence fallback evidence minimum includes `fallbackPolicyRef`, `availabilityProbeRefs`, `fallbackDecisionId`, `fallbackApprovedAt`, and explicit `fallbackExpiresAt`/`fallbackNonExpiring`.
- [ ] Test-evidence fallback decision metadata includes `fallbackFrom`, `fallbackTo`, `fallbackReasonCode`, `fallbackResolverStage`, and `fallbackEvaluatedAt`.
- [ ] Missing required scope blocks evaluation stage.

**Domain coverage**

- Concepts: [ExecutionCycle](domain.md#executioncycle), [ExecutionRuntimeMode](domain.md#executionruntimemode), [TestScopeLevel](domain.md#testscopelevel)
- Rules: [TestScopePolicy](rules.md#testscopepolicy), [ExecutionProviderFallbackPolicy](rules.md#executionproviderfallbackpolicy)
- Interfaces/Flows: [SandcastleAgentExecutionInterface](interfaces.md#internal-sandcastleagentexecutioninterface), [ProgressiveQualityLoopWorkflow](workflows.md#progressivequalityloopworkflow)

**Covered concept IDs**

- `sonar-loop.BuildAndImproveTestEvidence`
- `sonar-loop.ExecutionRuntimeMode`
- `sonar-loop.TestScopePolicy`
- `sonar-loop.ExecutionProviderFallbackPolicy`

**Capability links**

- [Test Evidence and Sonar Evaluation](SPEC.md#test-evidence-and-sonar-evaluation)

### US-006 Run Sonar Against Selected Gate and Bundle Findings

As a **quality operator**, I want **Sonar results grouped into context bundles**, so that **remediation tasks can be generated with high context quality**.

**Given** selected gate and test evidence are available
**When** [EvaluateWithSonarQualityGate](operations.md#evaluatewithsonarqualitygate) and [BundleFindingsByContext](operations.md#bundlefindingsbycontext) execute
**Then** findings are grouped by category and context tag.

**Acceptance checks**

- [ ] Sonar run uses selected gate profile.
- [ ] Sonar retry is bounded to one retry only.
- [ ] Retry attempt requires explicit remediation evidence.
- [ ] Retry failure ends in deterministic terminal `failed` outcome.
- [ ] Every finding is assigned to at least one context bundle.
- [ ] [FindingBundle](domain.md#findingbundle).contextTag uses controlled taxonomy with precedence.
- [ ] Bundle refs are linked to cycle.

**Domain coverage**

- Concepts: [QualityGateProfile](domain.md#qualitygateprofile), [FindingBundle](domain.md#findingbundle)
- Rules: [CycleStateMachine](rules.md#cyclestatemachine), [SonarRetryPolicy](rules.md#sonarretrypolicy)
- Interfaces/Flows: [SonarAnalysisInterface](interfaces.md#external-sonaranalysisinterface-restcli)

**Covered concept IDs**

- `sonar-loop.EvaluateWithSonarQualityGate`
- `sonar-loop.SonarRetryPolicy`
- `sonar-loop.BundleFindingsByContext`
- `sonar-loop.FindingBundle`
- `sonar-loop.FindingContextTagPolicy`

**Capability links**

- [Test Evidence and Sonar Evaluation](SPEC.md#test-evidence-and-sonar-evaluation)

## Task Orchestration, Solution Synthesis, and Learning

### US-007 Export Finding Tasks to GitHub and Jira via API-First Paths

As a **delivery manager**, I want **remediation tasks exported to GitHub and Jira epics/stories through APIs**, so that **execution can flow through existing planning systems**.

**Given** finding bundles are ready
**When** [CreateAndExportRemediationTasks](operations.md#createandexportremediationtasks) runs
**Then** repository tasks are created and exported via API-first integration.

**Acceptance checks**

- [ ] GitHub epic is modeled as issue plus metadata conventions.
- [ ] Repository task links are present in GitHub and Jira payloads.
- [ ] Export status model includes explicit retry transitions and `both-exported` terminal status.
- [ ] Completion is blocked while active retries exist or degradation threshold is breached unless explicit valid `riskAcceptedOverrideRef` is present.
- [ ] A completion override is valid only when [RiskAcceptanceOverride](domain.md#riskacceptanceoverride) uses enum-governed `approverRole`, enum-governed `overrideScopeType`, and required scope-binding fields for that scope type.
- [ ] Override lifecycle has no default expiry duration; validity requires explicit `expiresAt`/`nonExpiring` lifecycle choice and evidence/audit references.
- [ ] Revoked overrides are deterministically invalidated with `revokedAt`, `revokedByPrincipal`, and `revocationReasonCode`.
- [ ] MCP-only flow is not used as authoritative export path.

**Domain coverage**

- Concepts: [RemediationTask](domain.md#remediationtask), [TaskExportStatus](domain.md#taskexportstatus), [RiskAcceptanceOverride](domain.md#riskacceptanceoverride)
- Rules: [ApiFirstTaskIntegrationPolicy](rules.md#apifirsttaskintegrationpolicy), [CompletionGateUnderExportDegradationPolicy](rules.md#completiongateunderexportdegradationpolicy), [RiskAcceptanceOverrideValidityPolicy](rules.md#riskacceptanceoverridevaliditypolicy)
- Interfaces/Flows: [GitHubWorkApiInterface](interfaces.md#external-githubworkapiinterface-rest), [JiraWorkApiInterface](interfaces.md#external-jiraworkapiinterface-rest), [RiskAcceptanceOverrideRegistryInterface](interfaces.md#internal-riskacceptanceoverrideregistryinterface)

**Covered concept IDs**

- `sonar-loop.CreateAndExportRemediationTasks`
- `sonar-loop.ApiFirstTaskIntegrationPolicy`
- `sonar-loop.CompletionGateUnderExportDegradationPolicy`
- `sonar-loop.RiskAcceptanceOverride`
- `sonar-loop.RiskAcceptanceOverrideValidityPolicy`
- `sonar-loop.GitHubWorkApiInterface`
- `sonar-loop.JiraWorkApiInterface`
- `sonar-loop.TaskExportStatus`

**Capability links**

- [Task Orchestration, Solution Synthesis, and Learning](SPEC.md#task-orchestration-solution-synthesis-and-learning)

### US-008 Generate Three Solutions, Synthesize Abstractions, and Learn

As an **operator**, I want **three candidate solutions per task plus cross-smell abstractions and learning updates**, so that **future cycles improve without redundant fixes**.

**Given** remediation tasks are created
**When** [GenerateThreeCandidateSolutions](operations.md#generatethreecandidatesolutions), [SynthesizeCrossSmellAbstractions](operations.md#synthesizecrosssmellabstractions), and [ApplyOperatorSelectionLearning](operations.md#applyoperatorselectionlearning) run
**Then** each task has three candidates, abstractions reduce repeated smells, and operator choices update learning memory.

**Acceptance checks**

- [ ] Exactly three candidates exist per task.
- [ ] Abstractions use explicit scoring formula, threshold, and deterministic tie-break.
- [ ] Abstractions cover at least two smell bundles and avoid redundancy.
- [ ] Learning memory stores selected candidate, rationale, and observed outcome.

**Domain coverage**

- Concepts: [SolutionCandidate](domain.md#solutioncandidate), [LearningMemory](domain.md#learningmemory)
- Rules: [ThreeCandidateSolutionRule](rules.md#threecandidatesolutionrule), [NonRedundantAbstractionRule](rules.md#nonredundantabstractionrule), [LearningFeedbackRule](rules.md#learningfeedbackrule)
- Interfaces/Flows: [AssistedDecisionWorkflow](workflows.md#assisteddecisionworkflow), [ProgressiveQualityLoopWorkflow](workflows.md#progressivequalityloopworkflow)

**Covered concept IDs**

- `sonar-loop.GenerateThreeCandidateSolutions`
- `sonar-loop.SynthesizeCrossSmellAbstractions`
- `sonar-loop.ApplyOperatorSelectionLearning`
- `sonar-loop.LearningFeedbackRule`
- `sonar-loop.NonRedundantAbstractionRule`

**Capability links**

- [Task Orchestration, Solution Synthesis, and Learning](SPEC.md#task-orchestration-solution-synthesis-and-learning)

## Story Coverage Matrix

| Capability                                           | Story IDs      | Covered Concepts                                                                                                                                                                                                                                                                                                                                                                               | Notes                                                                                                                                                                                                                     |
| ---------------------------------------------------- | -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Quality Gate Targeting and Policy                    | US-001, US-002 | sonar-loop.ExecutionCycle, sonar-loop.QualityGateProfile, sonar-loop.DetermineTargetQualityGate, sonar-loop.AutonomousCheckpointAndStopPolicy, sonar-loop.ModeControlOutcome, sonar-loop.CompletionDecisionSource                                                                                                                                                                              | Covers gate progression, explicit pause outcome, resumable halted checkpoint-hold, stop-proof telemetry, and authoritative mode-control completion                                                                        |
| Codebase Intelligence Mapping                        | US-003, US-004 | sonar-loop.CodebaseKnowledgeMap, sonar-loop.MapCodebaseIntelligence, sonar-loop.ExecutionRuntimeMode, sonar-loop.SkillBundleProfile, sonar-loop.ComposeAgnosticSkillBundle, sonar-loop.SkillBundleReusePolicy, sonar-loop.ExecutionProviderFallbackPolicy                                                                                                                                      | Covers full TS mapping, explicit runtime-mode model, default deterministic fallback order with approved per-project override support, strong fallback evidence minimum, and reuse-first agnostic skill bundle composition |
| Test Evidence and Sonar Evaluation                   | US-005, US-006 | sonar-loop.BuildAndImproveTestEvidence, sonar-loop.ExecutionRuntimeMode, sonar-loop.EvaluateWithSonarQualityGate, sonar-loop.SonarRetryPolicy, sonar-loop.BundleFindingsByContext, sonar-loop.FindingBundle, sonar-loop.FindingContextTagPolicy                                                                                                                                                | Covers required evidence-first Sonar path, stage-parity fallback governance, detailed fallback evidence and telemetry metadata, bounded retry with remediation evidence, and context-tag precedence                       |
| Task Orchestration, Solution Synthesis, and Learning | US-007, US-008 | sonar-loop.CreateAndExportRemediationTasks, sonar-loop.CompletionGateUnderExportDegradationPolicy, sonar-loop.RiskAcceptanceOverride, sonar-loop.RiskAcceptanceOverrideValidityPolicy, sonar-loop.GenerateThreeCandidateSolutions, sonar-loop.SynthesizeCrossSmellAbstractions, sonar-loop.ApplyOperatorSelectionLearning, sonar-loop.TaskExportStatus, sonar-loop.NonRedundantAbstractionRule | Covers API-first export transitions, balanced completion gating with enum-governed override role/scope plus manual lifecycle semantics, candidate generation, scored abstractions, and learning loop                      |
