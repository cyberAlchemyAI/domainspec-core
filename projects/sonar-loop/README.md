# Sonar Loop

Sonar Loop is a docs-first quality orchestration specification for TypeScript codebases. It defines how teams run a progressive quality loop, govern runtime fallback decisions, and control completion under risk.

The source of truth is the feature docs in [docs/features/sonar-loop](docs/features/sonar-loop/SPEC.md).

## What Sonar Loop solves

Sonar Loop addresses a common delivery gap: teams can run static analysis, tests, and task export, but often without one governed loop that is repeatable, evidence-based, and auditable.

The Sonar Loop specification defines one end-to-end model for:

- progressive quality gate targeting across repeated passes
- codebase intelligence mapping before remediation
- evidence-first Sonar evaluation with bounded retry behavior
- API-first remediation task export with explicit lifecycle states
- operator-informed learning and checkpoint-based control

## Who it is for

Sonar Loop is for adopters who want a governed quality loop, especially:

- engineering leaders evaluating quality governance approaches
- maintainers running iterative remediation across repositories
- quality operators who need explicit stop, pause, and completion controls
- teams that must justify fallback and risk decisions with telemetry evidence

## Core outcomes and value

What a consumer can expect from the documented solution model:

- predictable loop progression from gate selection through remediation orchestration, with reuse-first skill-bundle handling for faster repeat passes
- stronger confidence in Sonar outcomes through required integration, e2e, and functional evidence
- clearer operational traceability through stage telemetry and terminal cycle summaries
- controlled delivery handoff through GitHub and Jira API-first export contracts
- explicit decision accountability for fallback, pause, halt, and completion

## How it works at a high level

Sonar Loop runs as a progressive cycle with ordered passes:

1. Select the target quality gate for the active pass.
2. Map codebase intelligence, then either recompose the reusable agnostic skill bundle when deterministic triggers (drift or policy changes) exist or reuse the latest valid baseline bundle.
3. Build required test evidence, then evaluate against the selected Sonar gate.
4. Bundle findings, create remediation tasks, and generate three candidate solutions per task.
5. Apply operator learning, record telemetry, and use mode control to continue, pause, halt, or complete.

Canonical workflow: [workflows.md](docs/features/sonar-loop/workflows.md)

## Architecture

Sonar Loop architecture is designed as a governed progressive loop with clear responsibility boundaries:

- gate and mode control own checkpoint and completion authority
- runtime-invoking stages (mapping, testing, synthesis) follow deterministic fallback governance
- Sonar evaluation, task export, and telemetry each produce auditable evidence artifacts

Architecture docs:

- Overview and in-depth design: [architecture.md](docs/features/sonar-loop/architecture.md)

## User Journey

The buyer and operator journey decisions are maintained as a first-class section under [userjourney](docs/features/sonar-loop/userjourney/README.md).

Journey docs:

- Evaluator day 0-day 1: [evaluator-day0-day1.md](docs/features/sonar-loop/userjourney/evaluator-day0-day1.md)
- Pilot week 1: [pilot-week1.md](docs/features/sonar-loop/userjourney/pilot-week1.md)
- Scale month 1: [scale-month1.md](docs/features/sonar-loop/userjourney/scale-month1.md)
- Packaging, pricing, and growth: [packaging-pricing-and-growth.md](docs/features/sonar-loop/userjourney/packaging-pricing-and-growth.md)

Approved commercialization narrative anchors:

- one-time non-SaaS purchase framing with per-repository packaging anchor
- docs/spec product as primary package, with guided implementation support as secondary intent
- assisted-first pilot posture for week-1 trust building
- governance proof package (fallback, override validity, completion-gate traceability) as month-1 risk answer
- GitHub-first integration posture for initial scale motion

## Why this is safe and governed

Sonar Loop treats governance as a product trust feature, not an add-on.

- Runtime modes are explicitly bounded to sandcastle, vscode-copilot, and claude-code.
- The default fallback order is deterministic: sandcastle -> vscode-copilot -> claude-code.
- Fallback to a non-default runtime requires policy and telemetry evidence fields.
- Sonar retry is bounded to one retry and requires remediation evidence before retry.
- Reuse-first bundle handling is gated: only a latest valid baseline may be reused, and deterministic drift/policy triggers force recomposition while coverage checks remain mandatory.
- Completion is mode-control authoritative and can be blocked when export degradation is active.
- Degraded completion is only allowed with a valid governed risk-acceptance override.
- Halted state is resumable and requires explicit stop compliance proof.

Governance references: [rules.md](docs/features/sonar-loop/rules.md), [operations.md](docs/features/sonar-loop/operations.md), [interfaces.md](docs/features/sonar-loop/interfaces.md), [observability.md](docs/features/sonar-loop/observability.md)

## What you can evaluate now

Current status:

- Feature status: [SPEC.md](docs/features/sonar-loop/SPEC.md) is draft (updated 2026-05-12).
- Project phase: docs-first specification and governance refinement.
- Scope statement: no implementation-completeness claim is made in this README.

Documentation map for evaluation:

- Product contract and capability index: [SPEC.md](docs/features/sonar-loop/SPEC.md)
- User journeys and coverage: [STORIES.md](docs/features/sonar-loop/STORIES.md)
- Domain model: [domain.md](docs/features/sonar-loop/domain.md)
- Operations and flow control: [operations.md](docs/features/sonar-loop/operations.md)
- End-to-end workflow: [workflows.md](docs/features/sonar-loop/workflows.md)
- Governance and invariants: [rules.md](docs/features/sonar-loop/rules.md)
- Runtime and integration boundaries: [interfaces.md](docs/features/sonar-loop/interfaces.md)
- Telemetry model: [observability.md](docs/features/sonar-loop/observability.md)
- Architecture overview and in-depth design: [architecture.md](docs/features/sonar-loop/architecture.md)
- Feature change history: [CHANGELOG.md](docs/features/sonar-loop/CHANGELOG.md)

Capability detail docs:

- [quality-gate-targeting-and-policy.md](docs/features/sonar-loop/capabilities/quality-gate-targeting-and-policy.md)
- [codebase-intelligence-mapping.md](docs/features/sonar-loop/capabilities/codebase-intelligence-mapping.md)
- [test-evidence-and-sonar-evaluation.md](docs/features/sonar-loop/capabilities/test-evidence-and-sonar-evaluation.md)
- [task-orchestration-solution-synthesis-and-learning.md](docs/features/sonar-loop/capabilities/task-orchestration-solution-synthesis-and-learning.md)
