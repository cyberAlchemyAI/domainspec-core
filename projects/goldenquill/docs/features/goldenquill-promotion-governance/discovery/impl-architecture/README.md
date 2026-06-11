# Implementation architecture — discovery pack (victor pattern)

Team-facing explanation of the **current implementation architecture and model** of the
`goldenquill-promotion-governance` feature, derived READ-ONLY from its spec and rendered in
the four-view victor discovery pattern.

Produced by dispatch `gq-impl-arch-discovery-2026-06-10`
(route: [ops/development/goldenquill-impl-architecture-discovery.dispatch.json](../../../../../../../ops/development/goldenquill-impl-architecture-discovery.dispatch.json)).
Spec-derived 2026-06-10; drift-checked and count-corrected.

## Read in this order
1. **[discovery.md](discovery.md)** — start here. Plain-language story + **the heart** (why owner decision alone can approve reuse) + honest build status + open questions for the team.
2. **[engineer-view.md](engineer-view.md)** — component inventory (C1–C16, build status), decision verdicts (D-A…D-F, D-001…D-007), blockers, work-pack reality. Owns the verdicts.
3. **[ontology-view.md](ontology-view.md)** — entities, enums, the five state machines, invariants. Owns the formal types.
4. **[system-view.md](system-view.md)** — shape at altitude, the three runtime planes, authority boundaries, and the canonical cross-reference map. Owns anti-drift.

## Provenance / evidence
- **[_derivation-substrate.md](_derivation-substrate.md)** — the shared spec-derived substrate all four views were authored from (the `handle.impl-architecture-and-model`).
- **[drift-check-ledger.md](drift-check-ledger.md)** — s5 validation: every load-bearing claim traced to a spec selector; flags found and corrected.

## One-line model
An event-sourced governance spine that turns bounded-adapter observations into a replayable
journal, projects it into a grant-run DAG + lifecycle/KPI/analytics read models, derives only
*proposed* learning candidates, and lets **owner decision alone** convert a candidate into
approved, scope-bounded reusable knowledge that future grant work may consume.

## Honest status
**Designed, not built.** L0 is fixture-only and audit-only (`mutation_allowed=false`); only
components C2/C3/C8 are in the L0 cut. This pack explains the *seam shape*, not a running loop.
