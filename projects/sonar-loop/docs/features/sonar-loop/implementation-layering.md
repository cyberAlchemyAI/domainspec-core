---
feature: sonar-loop
version: current
status: draft
updatedAt: 2026-05-13
docType: implementation-layering
owners:
  - sonar-loop
---

# Sonar Loop Implementation Layering

This document defines a POC-first implementation layering model for Sonar Loop.

Scope note: Layer 0 is the minimum working unit that proves the feature concept. Every later layer must preserve Layer 0 guarantees while adding capability or governance depth.

## Layering Method

- Layer 0 proves concept viability with the smallest end-to-end governed loop slice.
- Each subsequent layer explicitly improves the previous one (no parallel disconnected rewrites).
- Promotion to the next layer is allowed only when exit criteria and evidence for the current layer are complete.

## Layer Boundary Heuristic

A layer ends at the smallest slice that changes what the team can responsibly decide next.

```text
Layer value = decision unlocked + user-visible outcome + risk reduced
Layer cost = implementation time + verification time + coordination burden

Stop the layer when the next unit of work has lower value-per-cost for the current decision than starting the next decision layer.
```

For Sonar Loop, this keeps L0 focused on the governed loop spine instead of pulling fallback, export degradation, and multi-repo scale into the first proof.

## Layer Decision Framing

| Layer    | Decision Question                                                                           | Minimum Working Unit                                                                                   | Deferred Scope                                                                           | Promotion Decision                                                                                  |
| -------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| L0 (POC) | After this, we know whether a governed quality loop can turn evidence into actionable work. | One pass from gate selection to checkpoint with one remediation task and telemetry event.              | Runtime fallback depth, export degradation gates, override lifecycle, scale replication. | Continue to L1 if one pass is coherent and inspectable; pivot if the task output is not actionable. |
| L1       | After this, we know whether the loop can run repeatedly and deterministically in one repo.  | Retry, bundle reuse, three-candidate solutions, and learning writeback over the same single-repo loop. | Adverse provider/export conditions and multi-repo packaging.                             | Continue to L2 if repeatability holds without hidden manual fixes.                                  |
| L2       | After this, we know whether governance remains trustworthy under degraded conditions.       | Fallback evidence, export state governance, degraded-completion gate, and override validation.         | Replication proof and commercialization packaging.                                       | Continue to L3 if degraded-path decisions remain auditable and bounded.                             |
| L3       | After this, we know whether pilot and multi-repo scale claims are credible.                 | Replication proof across repos plus a governance proof package aligned to user-journey waves.          | Later productization beyond repo-scoped non-SaaS packaging.                              | Move to pilot/package only if repeatability and proof artifacts survive a second repo.              |

## Capability Progression Matrix

| Capability                                                                                                                 | Layer 0 (POC proof)                                       | Layer 1 (first hardening)                           | Layer 2 (governance hardening)                                         | Layer 3 (scale fit)                                      |
| -------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------- | --------------------------------------------------- | ---------------------------------------------------------------------- | -------------------------------------------------------- |
| [Quality Gate Targeting and Policy](capabilities/quality-gate-targeting-and-policy.md)                                     | Fixed gate selection plus one checkpoint decision path    | Full progression bounds and explicit pause handling | Stop/halt compliance and degraded-completion gate behavior             | Multi-repo repeatable checkpoint policy envelope         |
| [Codebase Intelligence Mapping](capabilities/codebase-intelligence-mapping.md)                                             | Minimal map for one repository slice                      | Reuse-vs-recompose skill-bundle branch logic        | Runtime fallback evidence and deterministic fallback order enforcement | Repo-agnostic replication baseline for additional repos  |
| [Test Evidence and Sonar Evaluation](capabilities/test-evidence-and-sonar-evaluation.md)                                   | Baseline evidence + one Sonar attempt + finding bundling  | One bounded remediation-evidenced retry             | Fallback parity across runtime-invoking stages                         | Stable quality trend signal cadence for scale operations |
| [Task Orchestration, Solution Synthesis, and Learning](capabilities/task-orchestration-solution-synthesis-and-learning.md) | One remediation task and one selected candidate rationale | Three-candidate generation + learning writeback     | API-first export retries, degradation controls, override validation    | Governance proof package for pilot and scale posture     |

## Layer Definitions

| Layer    | Objective                                                         | Builds On | Primary Scope                                                                                   | Exit Evidence                                                | Value/Cost Notes                                                                                                     |
| -------- | ----------------------------------------------------------------- | --------- | ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------- |
| L0 (POC) | Prove the progressive quality loop concept end-to-end in one pass | none      | Gate selection -> mapping -> evidence -> Sonar -> bundling -> one task -> checkpoint            | Core operation outputs plus one cycle telemetry event        | Highest value-per-cost because it validates the central promise before governance depth is built.                    |
| L1       | Complete deterministic capability behavior for single-repo usage  | L0        | Retry policy, bundle reuse branching, solution candidate set, learning update, richer telemetry | Policy-conformant pass with terminal summary evidence        | Worth doing before degraded-path hardening because repeatability defects would invalidate later governance evidence. |
| L2       | Harden governance controls under degraded or fallback conditions  | L1        | Runtime fallback evidence, export degradation gating, override validity, stop/halt controls     | Full policy field coverage and completion-gate evidence      | Higher verification cost is justified only after the repeatable single-repo loop is credible.                        |
| L3       | Validate replication and packaging posture for scale claims       | L2        | Multi-repo reproducibility, pilot robustness, GitHub-first growth handoff                       | Repeatability evidence package aligned to user-journey waves | Scale work starts only after degraded-path governance can be trusted.                                                |

## Layer 0 - Minimum Working Unit POC

### Goal

Prove that Sonar Loop can run one governed pass from gate selection to checkpoint decision while producing actionable remediation output.

### Included Scope

- [DetermineTargetQualityGate](operations.md#determinetargetqualitygate)
- [MapCodebaseIntelligence](operations.md#mapcodebaseintelligence)
- [BuildAndImproveTestEvidence](operations.md#buildandimprovetestevidence)
- [EvaluateWithSonarQualityGate](operations.md#evaluatewithsonarqualitygate) (attempt 0)
- [BundleFindingsByContext](operations.md#bundlefindingsbycontext)
- [CreateAndExportRemediationTasks](operations.md#createandexportremediationtasks) (minimum viable task output)
- [RecordCycleTelemetryTrend](operations.md#recordcycletelemetrytrend)
- [ApplyModeControlCheckpoint](operations.md#applymodecontrolcheckpoint)

### Explicitly Deferred Beyond L0

- Fallback-runtime governance depth from [ExecutionProviderFallbackPolicy](rules.md#executionproviderfallbackpolicy)
- Degraded export completion path from [CompletionGateUnderExportDegradationPolicy](rules.md#completiongateunderexportdegradationpolicy)
- Override lifecycle validation from [RiskAcceptanceOverrideValidityPolicy](rules.md#riskacceptanceoverridevaliditypolicy)
- Cross-smell abstraction scoring from [SynthesizeCrossSmellAbstractions](operations.md#synthesizecrosssmellabstractions)

### Exit Criteria

- One parent cycle and one child pass are recorded with deterministic stage ordering.
- At least one finding bundle and one remediation task are produced.
- A checkpoint decision (`continue`, `pause`, `halt`, or `complete`) is recorded with evidence.
- Cycle telemetry event exists and links to the pass-level outputs.

### Promotion Decision

- Continue to L1 when the remediation task is actionable, the telemetry envelope is inspectable, and the checkpoint decision can be replayed from evidence.
- Pivot within L0 when the loop runs but the task output is too vague for an operator or agent to act on.
- Stop when the pass cannot produce a finding bundle, remediation task, or checkpoint decision without manual hidden state.

## Layer-by-Layer Improvement Model

### L1 Improvements Over L0

- Adds bounded retry governance via [SonarRetryPolicy](rules.md#sonarretrypolicy).
- Adds skill-bundle branch behavior via [ComposeAgnosticSkillBundle](operations.md#composeagnosticskillbundle) and [SkillBundleReusePolicy](rules.md#skillbundlereusepolicy).
- Adds structured solution decision set via [GenerateThreeCandidateSolutions](operations.md#generatethreecandidatesolutions) and [ThreeCandidateSolutionRule](rules.md#threecandidatesolutionrule).
- Adds learning capture via [ApplyOperatorSelectionLearning](operations.md#applyoperatorselectionlearning).

### L2 Improvements Over L1

- Adds runtime fallback evidence depth for runtime-invoking stages via [ExecutionProviderFallbackPolicy](rules.md#executionproviderfallbackpolicy).
- Adds explicit API-first export state governance via [ApiFirstTaskIntegrationPolicy](rules.md#apifirsttaskintegrationpolicy).
- Adds degraded completion safety gate via [CompletionGateUnderExportDegradationPolicy](rules.md#completiongateunderexportdegradationpolicy).
- Adds override lifecycle validation via [RiskAcceptanceOverrideValidityPolicy](rules.md#riskacceptanceoverridevaliditypolicy).

### L3 Improvements Over L2

- Adds scale replication readiness tied to [pilot-week1](userjourney/pilot-week1.md) and [scale-month1](userjourney/scale-month1.md).
- Adds packaging-fit readiness tied to [packaging-pricing-and-growth](userjourney/packaging-pricing-and-growth.md).
- Adds operator-facing trend and alert posture via [QualityTrendMapping](observability.md#qualitytrendmapping) and [Alert Conditions](observability.md#alert-conditions).

## Implementation Wave Backbone

| Wave | Target Layer       | Goal                                                    | Key Artifacts                                                                                                    | Verification Focus                  |
| ---- | ------------------ | ------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- | ----------------------------------- |
| W0   | L0 definition lock | Freeze POC scope and non-goals before mutation          | [SPEC.md](SPEC.md), [architecture.md](architecture.md), [implementation-layering.md](implementation-layering.md) | Scope freeze plus link completeness |
| W1   | L0 build           | Deliver minimum end-to-end governed pass                | operation outputs, remediation task output, telemetry event                                                      | POC exit criteria                   |
| W2   | L1 hardening       | Enable deterministic retry/bundle/learning behavior     | retry evidence, branch evidence, candidate and learning artifacts                                                | L1 policy compliance                |
| W3   | L2 hardening       | Enforce fallback/export/degradation/override governance | fallback fields, export-state evidence, completion-gate evidence                                                 | L2 governance coverage              |
| W4   | L3 fit             | Validate replication and commercialization posture      | governance proof package, trend metrics, journey alignment evidence                                              | L3 scale-fit criteria               |

## Non-Regression Guardrails Across Layers

- [CycleStateMachine](rules.md#cyclestatemachine) order must stay valid in every layer.
- [TelemetryCompletenessRule](rules.md#telemetrycompletenessrule) fields required by current layer must be present before promotion.
- [AutonomousCheckpointAndStopPolicy](rules.md#autonomouscheckpointandstoppolicy) remains the authority for stop/halt/continue/complete outcomes.

## Open Decisions For Next Iteration

- Should L0 task export stay local-only or include GitHub export in the minimum unit?
- Should L2 and L3 remain separate waves for pilot use, or merged for speed in single-team rollouts?
