# Phase 2: Harness minimal profile planning - Research

**Researched:** 2026-04-29
**Domain:** Runtime gateway and harness architecture (minimal-first with durable promotion gates)
**Confidence:** HIGH

<user_constraints>

## User Constraints (from CONTEXT.md)

### Locked Decisions

- D-01: Default implementation path is a minimal profile that is fast, deterministic, and cheaper to run.
- D-02: Phase plans must prioritize local-first deterministic validation before adding infrastructure-heavy dependencies.
- D-03: Runtime dispatch and durable orchestration are separated by explicit interfaces so durability engines remain plug-in adapters.
- D-04: Harness foundation modules cannot depend directly on Temporal SDK constructs.
- D-05: Promotion to full durable profile is allowed only when at least one trigger is present: resumable long-running flows, human-in-loop pause/resume requirements, or strict crash-recovery guarantees.
- D-06: Any durable promotion plan must preserve existing request/response envelope and telemetry contracts.

### the agent's Discretion

- Concrete implementation libraries for validation and resilience can be selected during execution planning, as long as they preserve minimal-profile determinism and adapter seam clarity.
- Exact file layout for harness runtime modules may follow existing repository conventions.

### Deferred Ideas (OUT OF SCOPE)

- Full Temporal runtime rollout and worker infrastructure in the initial harness build.
- Broker/queue adoption beyond what is required for minimal deterministic harness behavior.

</user_constraints>

<research_summary>

## Summary

This research pass revalidated the Phase 2 direction against current ecosystem guidance and package maturity for gateway routing, resilience policies, schema validation, and telemetry pipelines. The main objective was to challenge the current plan, not to confirm it by default. The evidence still favors a minimal-first harness profile with strict contract boundaries and deterministic local replay before any durable orchestration investment.

For the minimal profile, the most stable pattern remains: typed request/response envelope contracts, deterministic routing policy, explicit retry/timeout/circuit semantics, and telemetry assertions that can run locally without distributed workflow infrastructure. This keeps delivery speed high while reducing migration risk, because the durable seam is treated as an optional adapter contract rather than a core dependency.

Durable orchestration remains a promotion target, not a baseline requirement. Temporal is still the strongest candidate when resumability, human-in-loop pause/resume, or strict crash-recovery guarantees become real operational requirements. Until one of those gates is satisfied with evidence, adopting full durable orchestration would add disproportionate complexity and operational burden.

**Primary recommendation:** Execute Phase 2 exactly as planned: codify minimal profile contracts and deterministic verification first, then formalize durable promotion gates with explicit evidence and no-rewrite migration constraints.
</research_summary>

<standard_stack>

## Standard Stack

The established libraries/tools for this domain:

### Core

| Library                       | Version                                | Purpose                                                      | Why Standard                                                              |
| ----------------------------- | -------------------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------------------- |
| LiteLLM (proxy or SDK)        | 1.x                                    | Unified model gateway and provider abstraction               | Reduces provider lock-in and normalizes request/response handling quickly |
| Zod                           | 4.x                                    | Runtime validation for typed envelopes in TS codepaths       | Strong TS ergonomics for contract-first local validation loops            |
| Cockatiel                     | 3.x                                    | Retry, timeout, circuit breaker, fallback policy composition | Deterministic resilience policies without hand-rolled control flow        |
| OpenTelemetry SDK + Collector | SDK current + Collector 0.151.x/1.57.x | Unified telemetry emission and transport pipeline            | Standard observability foundation with batching/retry/filtering support   |

### Supporting

| Library        | Version         | Purpose                                              | When to Use                                                           |
| -------------- | --------------- | ---------------------------------------------------- | --------------------------------------------------------------------- |
| Ajv            | 8.x             | JSON Schema validation for schema-governed envelopes | Use when schema artifacts must be validated independent of TS runtime |
| Vitest         | 2.x             | Deterministic local harness verification             | Use for matrix-driven fast CI and local replay                        |
| Temporal       | 1.x server line | Durable workflow engine                              | Use only after durable promotion gates are met                        |
| BullMQ or NATS | current stable  | Queue/event plumbing                                 | Use only if specific queue semantics are required before Temporal     |

### Alternatives Considered

| Instead of | Could Use                    | Tradeoff                                                                                   |
| ---------- | ---------------------------- | ------------------------------------------------------------------------------------------ |
| Zod        | Ajv-only                     | Better standards portability, weaker TS-native ergonomics for day-to-day app contracts     |
| Cockatiel  | Opossum + custom retry layer | More modular but easier to create policy drift and duplicated logic                        |
| LiteLLM    | Direct provider SDK fan-out  | Fewer dependencies but much higher adapter and ops maintenance overhead                    |
| Temporal   | BullMQ/NATS orchestration    | Lower barrier initially, but weaker durable workflow semantics for pause/resume and replay |

**Installation:**

```bash
npm install zod ajv cockatiel @opentelemetry/api @opentelemetry/sdk-node vitest
# optional durable profile add-ons (deferred until gate pass)
npm install @temporalio/client @temporalio/worker
```

</standard_stack>

<architecture_patterns>

## Architecture Patterns

### Recommended Project Structure

```
apps/
  harness/
    src/
      contracts/           # request/output envelope schemas + type guards
      runtime/             # dispatch core, policy executor, adapter registry
      adapters/
        model/             # model gateway adapter(s), default minimal profile
        durability/        # noop durability adapter + optional temporal adapter
      telemetry/           # instrumentation emitters and evidence mapping
      verification/        # deterministic matrix scenarios and fixtures
```

### Pattern 1: Policy-Composed Dispatch Pipeline

**What:** Use explicit resilience policies (retry/timeout/breaker/fallback) wrapped around dispatch execution.
**When to use:** Always for runtime dispatch in minimal profile.
**Example:**

```typescript
import {
  retry,
  timeout,
  circuitBreaker,
  wrap,
  handleWhen,
  ExponentialBackoff,
  ConsecutiveBreaker,
  TimeoutStrategy,
} from "cockatiel";

const isTransient = (err: unknown) => err instanceof Error;

const retryPolicy = retry(handleWhen(isTransient), {
  maxAttempts: 3,
  backoff: new ExponentialBackoff({ initialDelay: 25, maxDelay: 250 }),
});

const breakerPolicy = circuitBreaker(handleWhen(isTransient), {
  halfOpenAfter: 10_000,
  breaker: new ConsecutiveBreaker(5),
});

const timeoutPolicy = timeout(2_000, TimeoutStrategy.Aggressive);

export const dispatchPolicy = wrap(retryPolicy, breakerPolicy, timeoutPolicy);
```

### Pattern 2: Optional Durability Adapter (Noop by Default)

**What:** Define a durability interface with noop implementation for minimal profile.
**When to use:** Always in Phase 2; temporal adapter only behind promotion gate.
**Example:**

```typescript
export interface DurabilityAdapter {
  schedule(input: DispatchEnvelope): Promise<DurableHandle>;
  resume(handleId: string): Promise<DispatchResult>;
  enabled(): boolean;
}

export class NoopDurabilityAdapter implements DurabilityAdapter {
  async schedule(): Promise<DurableHandle> {
    throw new Error("Durability profile not enabled");
  }
  async resume(): Promise<DispatchResult> {
    throw new Error("Durability profile not enabled");
  }
  enabled(): boolean {
    return false;
  }
}
```

### Anti-Patterns to Avoid

- **Temporal-in-core imports:** Pulling Temporal SDK types into harness-core breaks the adapter seam and raises migration risk.
- **Implicit retries in multiple layers:** Hidden retries in SDK + app + proxy create non-deterministic behavior and cost spikes.
- **Schema drift by ad hoc objects:** Bypassing typed envelope validation introduces non-replayable failures.
  </architecture_patterns>

<dont_hand_roll>

## Don't Hand-Roll

Problems that look simple but have existing solutions:

| Problem                     | Don't Build                               | Use Instead                          | Why                                                                        |
| --------------------------- | ----------------------------------------- | ------------------------------------ | -------------------------------------------------------------------------- |
| Retry and backoff           | Custom recursive retry helper             | Cockatiel retry + backoff primitives | Avoids edge-case bugs, adds observability hooks, keeps behavior consistent |
| Runtime contract validation | Manual if/else object checks              | Zod and/or Ajv schemas               | Prevents schema drift and improves deterministic failure reporting         |
| Telemetry fan-out transport | Custom exporter forwarding service        | OTel SDK + Collector pipeline        | Handles batching/retry/filtering with standard tooling                     |
| Provider abstraction        | Multiple direct SDK wrappers in core path | LiteLLM gateway boundary             | Reduces integration churn and keeps model routing portable                 |

**Key insight:** In this domain, hand-rolled control paths fail at boundary conditions (timeouts, partial failures, schema evolution). Standard libraries reduce latent defects and preserve determinism under load and failure.
</dont_hand_roll>

<common_pitfalls>

## Common Pitfalls

### Pitfall 1: Boundary Violation Between Harness-Core and Durability Engine

**What goes wrong:** Core modules depend on durable orchestration types.
**Why it happens:** Convenience imports during early implementation.
**How to avoid:** Enforce adapter interfaces and lint/path boundaries.
**Warning signs:** Temporal symbols appearing in core dispatch/contract files.

### Pitfall 2: Non-Deterministic Retry Behavior

**What goes wrong:** Different retry policies fire in proxy, client, and adapter layers.
**Why it happens:** Policy defaults are enabled in multiple places.
**How to avoid:** Declare one authoritative retry policy and disable duplicates.
**Warning signs:** Same request showing variable attempt counts across runs.

### Pitfall 3: Weak Evidence Surface for Promotion Decisions

**What goes wrong:** Teams promote to durable profile based on anecdotal incidents.
**Why it happens:** Missing traceable metrics for resumability and crash recovery needs.
**How to avoid:** Gate promotion on documented trigger evidence and approval flow.
**Warning signs:** Durable migration proposals without reproducible failure datasets.
</common_pitfalls>

<code_examples>

## Code Examples

Verified patterns from official sources:

### Envelope Validation in Dispatch Entry

```typescript
// Source: https://zod.dev/api and https://ajv.js.org/guide/getting-started.html
import * as z from "zod";

const DispatchEnvelopeSchema = z.object({
  requestId: z.string(),
  taskType: z.string(),
  payload: z.record(z.unknown()),
  timeoutMs: z.number().int().positive().max(30_000),
});

export type DispatchEnvelope = z.infer<typeof DispatchEnvelopeSchema>;

export function parseEnvelope(input: unknown): DispatchEnvelope {
  return DispatchEnvelopeSchema.parse(input);
}
```

### Composed Resilience Execution

```typescript
// Source: https://github.com/connor4312/cockatiel (retry/circuit-breaker/timeout patterns)
export async function executeWithPolicy<T>(fn: () => Promise<T>): Promise<T> {
  return dispatchPolicy.execute(async () => fn());
}
```

### Promotion-Ready Durability Adapter Selection

```typescript
// Source: adapter-boundary pattern derived from Temporal and minimal-profile contract constraints
export function createDurabilityAdapter(
  mode: "minimal" | "durable",
): DurabilityAdapter {
  if (mode === "durable") {
    // Temporal adapter is intentionally loaded only in durable profile.
    return new TemporalDurabilityAdapter();
  }
  return new NoopDurabilityAdapter();
}
```

</code_examples>

<sota_updates>

## State of the Art (2024-2025)

What's changed recently:

| Old Approach                            | Current Approach                                   | When Changed                                   | Impact                                                     |
| --------------------------------------- | -------------------------------------------------- | ---------------------------------------------- | ---------------------------------------------------------- |
| Direct provider SDK fan-out in app code | Unified gateway abstraction (LiteLLM-style)        | 2024-2025 mainstreaming                        | Faster provider portability and centralized policy control |
| Ad hoc retry helpers                    | Policy composition libraries with structured hooks | Matured by 2024+                               | Better determinism and observability for failure handling  |
| Service-only telemetry export           | OTel Collector pipeline as standard ops primitive  | Ongoing 2024-2026 adoption                     | Easier batching/retry/filtering/security hardening         |
| Early durable orchestration by default  | Trigger-gated durable adoption                     | Emerging best practice in cost-sensitive teams | Lower early complexity and clearer migration economics     |

**New tools/patterns to consider:**

- Collector resiliency and scaling playbooks in OTel docs for production hardening after minimal profile is stable.
- LiteLLM gateway + callback patterns for cost, latency, and fallback telemetry unification.

**Deprecated/outdated:**

- One-off hand-rolled retry/timeout wrappers without structured policy events.
- Hard-coupled workflow-engine references in foundational runtime modules.
  </sota_updates>

<open_questions>

## Open Questions

1. **Primary runtime contract validator for shared artifacts: Zod-first or Ajv-first?**
   - What we know: Zod is ergonomically better for TS runtime flows; Ajv is stronger for standalone JSON Schema governance.
   - What's unclear: Which artifact is authoritative in execution paths vs governance checks.
   - Recommendation: Use Zod for runtime entrypoints and Ajv for schema-governance checks in CI until one authority is formally declared.

2. **When to prefer BullMQ/NATS before Temporal promotion?**
   - What we know: Queue/event tools can handle some async load distribution.
   - What's unclear: Whether any Phase 2 scenarios require queue semantics before durable gates are met.
   - Recommendation: Keep queue adoption deferred unless a concrete scenario fails minimal profile constraints.
     </open_questions>

<sources>
## Sources

### Primary (HIGH confidence)

- https://docs.litellm.ai/ - provider abstraction, proxy model, routing/fallback context
- https://github.com/BerriAI/litellm - project maturity, release cadence, OSS footprint
- https://docs.temporal.io/ - durable execution guarantees and workflow model
- https://github.com/temporalio/temporal - server maturity and release line
- https://github.com/connor4312/cockatiel - resilience policy APIs and composition patterns
- https://zod.dev/api and https://github.com/colinhacks/zod - typed runtime validation patterns
- https://ajv.js.org/ and https://github.com/ajv-validator/ajv - JSON Schema validation model and standards coverage
- https://opentelemetry.io/docs/collector/ and https://github.com/open-telemetry/opentelemetry-collector - collector architecture and resiliency model

### Secondary (MEDIUM confidence)

- Prior Phase 2 planning artifacts and INF/HAR contract docs in this repository (cross-validated with current web sources)

### Tertiary (LOW confidence - needs validation)

- Specific package minor-version pin recommendations should be confirmed at implementation time before lockfile updates
  </sources>

<metadata>
## Metadata

**Research scope:**

- Core technology: harness runtime profile architecture with optional durable seam
- Ecosystem: LiteLLM, Zod, Ajv, Cockatiel, Temporal, OpenTelemetry Collector
- Patterns: adapter boundary, deterministic policy composition, evidence-gated migration
- Pitfalls: boundary coupling, policy duplication, evidence gaps

**Confidence breakdown:**

- Standard stack: HIGH - mature OSS projects with active docs and releases
- Architecture: HIGH - directly aligned with locked Phase 2 decisions and existing INF contracts
- Pitfalls: HIGH - repeatedly observed failure modes in orchestration and gateway systems
- Code examples: MEDIUM - adapted from official APIs to repository-specific contracts

**Research date:** 2026-04-29
**Valid until:** 2026-05-29
</metadata>

---

_Phase: 02-harness-minimal-profile-planning_
_Research completed: 2026-04-29_
_Ready for planning: yes_
