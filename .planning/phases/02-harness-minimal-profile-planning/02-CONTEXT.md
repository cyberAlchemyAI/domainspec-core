# Phase 2: Harness minimal profile planning - Context

**Gathered:** 2026-04-29
**Status:** Ready for planning
**Source:** User directive to plan minimal-first harness implementation with Temporal-ready boundaries

<domain>
## Phase Boundary

This phase produces executable plan artifacts for building the harness on a minimal runtime profile first, while preserving a clean adapter seam so durable orchestration can be added later without rewriting harness foundations.

This phase does not implement full durable orchestration and does not require Temporal rollout.

</domain>

<decisions>
## Implementation Decisions

### Minimal profile first

- **D-01:** Default implementation path is a minimal profile that is fast, deterministic, and cheaper to run.
- **D-02:** Phase plans must prioritize local-first deterministic validation before adding infrastructure-heavy dependencies.

### Adapter boundary and portability

- **D-03:** Runtime dispatch and durable orchestration are separated by explicit interfaces so durability engines remain plug-in adapters.
- **D-04:** Harness foundation modules cannot depend directly on Temporal SDK constructs.

### Durable promotion gate

- **D-05:** Promotion to full durable profile is allowed only when at least one trigger is present: resumable long-running flows, human-in-loop pause/resume requirements, or strict crash-recovery guarantees.
- **D-06:** Any durable promotion plan must preserve existing request/response envelope and telemetry contracts.

### the agent's Discretion

- Concrete implementation libraries for validation and resilience can be selected during execution planning, as long as they preserve minimal-profile determinism and adapter seam clarity.
- Exact file layout for harness runtime modules may follow existing repository conventions.

</decisions>

<specifics>
## Specific Ideas

- Keep the initial harness stack lean and contract-first.
- Use deterministic replayable test scenarios for routing, fallback, retry, timeout tiering, and typed output envelopes.
- Treat Temporal as a deferred adapter profile that activates only after trigger-gate approval.

</specifics>

<canonical_refs>

## Canonical References

Downstream agents MUST read these before planning or implementing.

### Runtime contracts and policies

- implementation/domainspec/plan/infra/INF-01-runtime-dispatch-gateway.md - Runtime gateway objective, deliverables, and done criteria.
- implementation/domainspec/plan/infra/INF-01-runtime-adapter-spec.md - Adapter interface and request envelope contract.
- implementation/domainspec/plan/infra/INF-01-dispatch-policy.md - Deterministic routing, retry, and timeout policy baseline.
- implementation/domainspec/plan/infra/INF-01-output-envelope-schema.md - Typed output envelope contract.
- implementation/domainspec/plan/infra/INF-01-health-fallback-policy.md - Health and fallback transition policy.
- implementation/domainspec/plan/infra/INF-02-agent-telemetry-saturn.md - Telemetry compatibility contract.

### Harness scope and role workflows

- implementation/domainspec/plan/harness/HARNESS-PRODUCT-OVERVIEW.md - Harness role in the system and rollout strategy.
- implementation/domainspec/plan/harness/HAR-01-domain-graph-chain-explorer.md - Harness graph capability target.
- implementation/domainspec/plan/harness/HAR-02-role-workspace-views.md - Role-aware workflow constraints.
- implementation/domainspec/plan/harness/HAR-03-owner-task-board.md - Owner-prioritized decision surface.
- implementation/domainspec/plan/harness/HAR-05-org-metrics-dashboard.md - Metrics coupling requirements.

### Planning and synchronization surfaces

- .planning/ROADMAP.md - Phase 2 scope, requirements, and plan slots.
- .planning/REQUIREMENTS.md - HARN requirement IDs and phase mapping.
- implementation/domainspec/plan/index.md - Program ordering and dependency context.
- implementation/domainspec/plan/TRACEABILITY.md - Task-to-gap and ADLC alignment mapping.
- implementation/domainspec/plan/COMPLETENESS-DASHBOARD.md - Plan completion tracking surface.

</canonical_refs>

<code_context>

## Existing Code Insights

### Reusable Assets

- INF-01 contract documents already define baseline runtime and envelope semantics that can anchor minimal harness design.
- INF-02 contract artifacts provide telemetry schema targets for harness assertions.

### Established Patterns

- Contract-first markdown specs are used to unblock implementation in dependent streams.
- Done criteria rely on explicit evidence and checkbox completion, not narrative claims.

### Integration Points

- Phase 2 execution plans should update infra and harness plan documents first, then synchronize traceability and dashboard surfaces.

</code_context>

<deferred>
## Deferred Ideas

- Full Temporal runtime rollout and worker infrastructure in the initial harness build.
- Broker/queue adoption beyond what is required for minimal deterministic harness behavior.

</deferred>

---

_Phase: 02-harness-minimal-profile-planning_
_Context gathered: 2026-04-29_
