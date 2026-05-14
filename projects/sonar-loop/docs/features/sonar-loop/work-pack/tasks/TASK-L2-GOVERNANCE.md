# TASK-L2-GOVERNANCE: Runtime, Export, and Override Governance

## Goal

Harden degraded paths through deterministic runtime fallback, API-first GitHub/Jira export lifecycle, completion gate enforcement, risk override validation, and stop/halt proof.

## DomainSpec Coverage

`sonar-loop.ExecutionRuntimeMode`, `sonar-loop.RuntimeInvokingStage`, `sonar-loop.RuntimeFallbackReasonCode`, `sonar-loop.TaskExportStatus`, `sonar-loop.RiskAcceptanceOverride`, `sonar-loop.ExecutionProviderFallbackPolicy`, `sonar-loop.ApiFirstTaskIntegrationPolicy`, `sonar-loop.CompletionGateUnderExportDegradationPolicy`, `sonar-loop.RiskAcceptanceOverrideValidityPolicy`, `sonar-loop.AutonomousCheckpointAndStopPolicy`, `sonar-loop.SandcastleAgentExecutionInterface`, `sonar-loop.GitHubWorkApiInterface`, `sonar-loop.JiraWorkApiInterface`, `sonar-loop.RiskAcceptanceOverrideRegistryInterface`, `sonar-loop.ModeControlInterface`.

## Architecture References

- Domain layer owns fallback, export-state, completion-gate, override-validity, and stop/halt policies.
- Application layer enforces policy decisions before state transitions.
- Infrastructure layer owns Sandcastle, Sonar, GitHub REST, Jira REST, and override registry adapters.
- Interface layer exposes commands/APIs without embedding business policy.

## Implementation Directives

- Enforce default runtime order `sandcastle -> vscode-copilot -> claude-code` unless an approved fallback order policy exists.
- Require fallback policy/probe/decision/metadata fields whenever runtime mode is not `sandcastle`.
- Model GitHub/Jira export through API-first adapters and explicit `TaskExportStatus` transitions.
- Block completion while export retries or degradation breach exist unless a valid override is resolved.
- Persist stop compliance proof on halt.

## Gaps and Questions

- GitHub/Jira config refs must be provided by runtime configuration.
- Override registry storage and audit ledger are adapter choices.

## Decision Lock

- D-002: do not merge W3 governance hardening with W4 scale-fit validation.
