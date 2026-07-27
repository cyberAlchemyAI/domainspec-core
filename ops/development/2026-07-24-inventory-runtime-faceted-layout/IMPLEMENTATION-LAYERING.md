---
module: inventory-runtime-faceted-layout
version: candidate
status: authored
updatedAt: 2026-07-24
docType: implementation-layering
---

# Implementation Layering: Inventory Runtime And Faceted Layout

## Target And Scope

- Target: public Inventory sigil and installed consumer runtime.
- Current state: updater and validator substrate exist; Candidate B and facets
  are unimplemented.
- Boundary: new faceted entries only; legacy migration and atomic transactions
  are excluded.

## Layer Boundary Rule

Each layer ends when its decision can be answered with independent evidence.

| Layer | Decision question | Minimum working unit | Included | Deferred | Exit evidence | Promotion |
|---|---|---|---|---|---|---|
| L0 | After this layer, we know whether one Inventory operation receipt can be canonical, digest-bound, and byte-reproducible. | Receipt schema, canonical serializer, fingerprint/digest rules, deterministic fixtures. | Pure computation only. | CLI, validators, writes, facets, packaging. | Repeated serializer tests and schema validation. | Continue only if byte identity closes. |
| L1 | After this layer, we know whether a package-local dry-run can attribute baseline, candidate, warning delta, and no-mutation outcomes. | Unrelated-CWD dry-run over the complete validator pair. | Dry-run, conflict/no-op, baseline/candidate gates, warning delta. | Apply, facets, sync. | Four named dry-run receipt classes and unchanged filesystem digests. | Continue only if no-mutation and warning attribution pass. |
| L2 | After this layer, we know whether fail-closed sequential apply and faceted new-entry admission preserve conformance. | Apply observation plus new-entry facet/path/projection validation. | Apply/failure states, namespace/class/concept admission, derived maps. | Lock/journal/recovery, legacy moves, packaging. | Failure-injection receipts, legacy compatibility, map conformance. | Continue only if partial mutation is visible and legacy remains valid. |
| L3 | After this layer, we know whether the complete runtime can be installed and reproduced without touching consumer-owned state. | Manifest sync plus isolated installed-consumer proof. | Runtime payload, drift check/apply, boundary scan, acceptance receipts. | Live repository migration, release, publication, currentness verifier. | Isolated consumer proof and managed-path negative fixture. | Hand off release/pilot decisions separately. |

## Value/Cost Boundary

- L0 isolates the highest-value uncertainty—canonical causal evidence—without
  mutation or packaging cost.
- L1 adds the complete no-write path before any sequential-write risk.
- L2 groups mutation correctness and new-record organization because both
  depend on the admitted candidate model, but keeps them as separate SWUs.
- L3 delays distribution until behavior and schema are stable.

## Non-Regression Guardrails

- L1-L3 preserve L0 byte determinism.
- L2-L3 preserve L1 zero-mutation states and full validator ownership.
- L3 preserves L2 legacy compatibility and consumer-state ownership.
- No layer introduces currentness, atomicity, migration, or promotion claims.
- Public fixtures remain generic.

## Recommended Next Layer

- Next layer: L0.
- First mutation-capable unit after lifecycle acceptance:
  `SWU-IFR-001`.
- Major deferral: all legacy file moves and Candidate C transaction machinery.

