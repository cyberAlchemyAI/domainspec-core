# Sonar Loop — Changelog

All notable changes to the **sonar-loop** feature are documented in this file.

## 2026-05-12 (userjourney section and cross-artifact propagation)

### Added

- **User journey documentation section** — added [userjourney/README.md](userjourney/README.md) plus stage docs for evaluator day 0-1, pilot week 1, scale month 1, and packaging/pricing/growth.

### Changed

- **Spec and aspect linkage** — updated [SPEC.md](SPEC.md), [STORIES.md](STORIES.md), [domain.md](domain.md), [operations.md](operations.md), [workflows.md](workflows.md), [rules.md](rules.md), [interfaces.md](interfaces.md), [observability.md](observability.md), and [architecture.md](architecture.md) with additive user-journey alignment sections and cross-links.
- **Commercialization framing synchronization** — aligned doc narrative to approved decisions: assisted-first pilot, governance proof package, GitHub-first initial scale, and one-time non-SaaS per-repository packaging anchor.

## 2026-05-12 (conditional skill-bundle compose/reuse contract)

### Changed

- **ComposeAgnosticSkillBundle contract** — made skill-bundle composition reuse-first: recomposition runs only when deterministic trigger conditions are present; otherwise the latest valid agnostic baseline bundle is reused.
- **Workflow step 2b semantics** — changed progressive workflow to explicit branch semantics (conditional `2b` recomposition vs reuse path) while preserving deterministic stage order.
- **Reuse policy governance** — added formal reuse-vs-recompose decision policy with deterministic trigger formula, baseline validity requirements, and branch exclusivity guarantees.
- **Telemetry completeness for bundle branching** — required branch decision evidence (`recomposed`/`reused` and decision references) so audits can prove why a pass recomposed or reused.

## 2026-05-12 (interview decision alignment Q1-Q6)

### Changed

- **Runtime fallback precedence** — kept default order `sandcastle -> vscode-copilot -> claude-code` and added approved per-project fallback-order policy artifact support with deterministic/auditable resolution.
- **Fallback boundary expansion** — applied fallback governance to every runtime-invoking stage (mapping, test evidence, solution synthesis, and approved future runtime stages), not only mapping/testing.
- **Fallback evidence minimum hardening** — required fallback evidence now includes `fallbackPolicyRef`, `availabilityProbeRefs`, `fallbackDecisionId`, `fallbackApprovedAt`, and explicit `fallbackExpiresAt`/`fallbackNonExpiring` lifecycle fields.
- **Fallback telemetry granularity** — added detailed fallback telemetry fields across contracts: `fallbackFrom`, `fallbackTo`, `fallbackReasonCode`, `fallbackDecisionId`, `fallbackResolverStage`, `fallbackEvaluatedAt`.
- **Override role/scope strictness** — replaced free-text override role/scope with fixed enums and required scope-binding fields by scope type.
- **Override lifecycle defaults** — removed implicit expiry defaults; override expiry/non-expiring and revocation are explicit manual lifecycle actions with deterministic revocation invalidation semantics.

## 2026-05-12 (runtime mode and override governance hardening)

### Added

- **Runtime mode domain model** — added explicit [ExecutionRuntimeMode](domain.md#executionruntimemode) support for `sandcastle`, `vscode-copilot`, and `claude-code` with Sandcastle default semantics.
- **Risk override governed artifact** — added [RiskAcceptanceOverride](domain.md#riskacceptanceoverride) and [RiskAcceptanceOverrideStatus](domain.md#riskacceptanceoverridestatus) to replace implicit string-only override treatment.
- **Override validity policy** — added [RiskAcceptanceOverrideValidityPolicy](rules.md#riskacceptanceoverridevaliditypolicy) and registry contract in [interfaces.md](interfaces.md#internal-riskacceptanceoverrideregistryinterface).

### Changed

- **Fallback governance determinism** — updated [ExecutionProviderFallbackPolicy](rules.md#executionproviderfallbackpolicy) and runtime interfaces/operations to enforce deterministic fallback order (`sandcastle -> vscode-copilot -> claude-code`) with explicit policy evidence.
- **Completion gate hardening** — updated completion gate rules and mode-control/telemetry operations to require valid override checks (active and non-expired unless explicitly non-expiring) before degraded completion is allowed.
- **Telemetry and story coverage alignment** — updated [observability.md](observability.md), [STORIES.md](STORIES.md), capability docs, and [SPEC.md](SPEC.md) to capture runtime-mode evidence and override-validation evidence across feature contracts.

## 2026-05-12

### Added

- **Initial capability-driven baseline** — added [SPEC.md](SPEC.md) with four core capabilities, concept registry, feature graph, and aspect index.
- **Domain model** — added [domain.md](domain.md) with cycle, quality gate, mapping, finding, task, learning, and skill-bundle concepts under `sonar-loop.*` IDs.
- **Behavior contracts** — added [operations.md](operations.md), [workflows.md](workflows.md), and [rules.md](rules.md) to define the 11-stage progressive loop, autonomous/assisted mode controls, and policy invariants.
- **Integration boundaries** — added [interfaces.md](interfaces.md) with Sandcastle runtime integration and API-first GitHub/Jira export contracts.
- **Telemetry baseline** — added [observability.md](observability.md) with cycle telemetry event schema, quality trend mapping, and checkpoint metrics.
- **Story coverage baseline** — added [STORIES.md](STORIES.md) with capability-scoped user stories and concept-ID coverage matrix.
- **Capability detail packs** — added four capability docs in [capabilities](capabilities) for gate policy, mapping, evidence/evaluation, and task/learning orchestration.

### Changed

- **Hybrid cycle semantics** — modeled parent cycle plus child pass identifiers and clarified cycle cardinality.
- **Completion authority** — made mode control authoritative for completion decisions and [CheckpointControl](domain.md#checkpointcontrol) authoritative for stop signals.
- **Halted state semantics** — reclassified `halted` as resumable checkpoint-hold (non-terminal) with explicit resume transition back to checkpoint control.
- **Pause outcome contract** — formalized `pause` as a first-class mode-control workflow outcome across operations, rules, and telemetry.
- **Stop compliance proof** — required explicit `stopRequestedAt` and `haltedAt` with checkpoint-index correlation for every halt transition.
- **Telemetry contract** — aligned telemetry model to require stage events plus terminal cycle summary at completion.
- **Evidence policy hardening** — made Sonar precondition explicitly require integration, e2e, and functional evidence; optional perf/load now requires explicit request artifact.
- **Provider policy** — set Sandcastle as default execution provider with explicit fallback policy requirements.
- **Fallback parity** — enforced identical fallback contract inputs for both mapping and test-evidence stages.
- **Sonar retry governance** — formalized one bounded retry with required remediation evidence and deterministic terminal failure on retry exhaustion.
- **Completion under export degradation** — completion now blocks while active export retries exist or degradation threshold is breached unless explicit risk-accepted override evidence is present.
- **Gate rollback governance** — required persisted `rollbackReason` for gate downgrades.
- **Task export model** — added explicit retry transitions and `both-exported` terminal status in [TaskExportStatus](domain.md#taskexportstatus).
- **GitHub epic modeling** — defined epic representation as issue plus metadata conventions.
- **Abstraction governance** — added explicit cross-smell scoring formula, threshold, and deterministic tie-breaks.
- **Finding context taxonomy** — constrained [FindingBundle](domain.md#findingbundle).contextTag to controlled taxonomy with precedence.
