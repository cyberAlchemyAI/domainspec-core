# Stage 05 — Distill (coherent unit)

- Capability: `distill` · Mode: `standard` · Status: **pass**

## Selected coherent unit (SCU)

**`UIIdentityIndex` — a derived read-model registry over the append-only event log.**

The keystone that closes Q4 and makes everything else (components page, cross-session recognition) a projection rather than new construction.

## Pareto (value ÷ cost)

| Capability | Value | Cost | Keep? |
| --- | --- | --- | --- |
| `UIIdentityIndex` derived projection (AF1) | High — closes Q4, no new entity name (A1), regenerable | Low (projection over existing events) | **Yes** |
| Components page = projection of the index (AF3) | High — the page is *free* once the index exists | ~0 once index exists | **Yes** |
| `data-od-id` equality matching, phase 1 (AF4) | High — exact, deterministic | Low | **Yes** |
| Owned 24-enum DNA as canonical genome (AF2) | High — holds A2/A3, DiffSummary stays meaningful | (already designed) | **Yes** |
| Resonant namespace-**names** fill R-7 dims (AF2) | Med — fills Motion/Interaction/State/Feedback/Numeric as `external_context`, names-only | Low (reuse s1 mapping, no vendoring) | **Yes** |
| DNA-similarity matching, phase 2 (AF4) | Med — detects reuse when od-id misses | Med | Defer |
| Durable canonical registry file | (negative) — second source of truth | — | **No** |
| Vendor resonant / import token values | (negative) — A2 raw-values trap + license gate | High | **No** |

## Rejected alternatives (recorded)

- **Durable canonical registry entity** — rejected: a second source of truth violates "regenerable projection"; the event log is already canonical.
- **Adopt resonant as the DNA source / vendor it** — rejected: A3 (no promotion) + A2 (raw values) + unverified license. Names-only `external_context` captures the value at zero cost.
- **New entity name for the registry** — rejected: A1 forbids it; `UIIdentityIndex` is a *read-model*, not a new durable entity.

## Recomposition target

`UIIdentityIndex` recomposes the full vision: components page (projection) → per-element composition (compose from recognized identities) → cross-session recognition (index aggregates repo event logs) → conformance (DiffSummary over indexed signatures).

## distill-frame → s06
