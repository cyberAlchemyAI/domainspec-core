---
module: ide-extension-operations-v1
version: current
status: ready
updatedAt: 2026-07-12
docType: implementation-layering
---

# Implementation Layering: Operations V1

## Purpose

Deliver a kernel-owned HTML operations surface without changing the existing
V0 complete-file API, and promote scope only when the previous layer produces
durable evidence.

## Layer Boundary Rule

```text
After this layer, we know whether the stated decision is supported by retained
runtime evidence, not merely by completed code.
```

## Layer Decision Table

| Layer | Decision question | Minimum working unit | Included scope | Deferred scope | Exit evidence | Promotion decision |
| --- | --- | --- | --- | --- | --- | --- |
| L0 derive and replace | After this layer, do exact V0 derivation, immutable body authority, CAS replacement, and restart recovery work without changing V0? | `SWU-OV1-001` through `006`: contracts, parse5 adapter, blob store, replay state, derivation, replacement. | Separate operations-surface identity, 5/4/0.5/8 MiB budgets, blob-before-event ordering, immutable content route, idempotency, stale rejection. | Append, rebuild, navigation, retention enforcement, regions. | V0 suites remain green; derive and replacement bodies survive restart; duplicate and stale matrices pass. | Continue to L1 only if the complete L0 value loop passes. |
| L1 append and retry | After this layer, can a fragment append exactly once under timeout retries and concurrent writers? | `SWU-OV1-007`: parser-context append plus idempotency/concurrency matrix. | Body-context fragment parsing, deterministic serialization, duplicate return, conflict and stale rejection. | Automatic merge, collaboration, region mutation. | Appended nodes are interactive in committed complete bytes; retries do not duplicate; concurrent stale input rejects. | Continue to L2 only if append is repeatable and V0/L0 evidence remains green. |
| L2 rebuild, navigation, retention, and proof | After this layer, can the agent explicitly rebuild, show, refresh, and retain/prune surfaces predictably over restart? | `SWU-OV1-008` through `014`: exact rebuild, durable target, browser delivery, threshold-and-grace retention, CLI/value proof, integrated audit. | Separate display projection, transient refresh acknowledgement, manual and automatic pruning, 410 tombstones, browser and CLI witnesses. | Per-browser targets, durable refresh history, remote control, configurable production profiles. | Drift/restart/browser tests pass; pruning is tombstone-before-delete; real create/operate/show witness passes; integrated report closes traceability. | Mark Operations V1 whole-document package complete or remediate; do not enter L3 automatically. |
| L3 declared regions | After this layer, is region-scoped mutation valuable and unambiguous? | No unit in this work pack. A separate accepted design and plan are mandatory. | None. | Region identity, region replace semantics, scaffolding, merge behavior. | Future design must prove stable unique ids and preserve whole-document behavior. | Deferred. |

## Active Window

Execute L0 through L2 sequentially. L3 is explicitly outside this work pack.

## Fixed Plan Constants

| Constant | Value | Rule |
| --- | --- | --- |
| HTTP operation request | 5 MiB | Reject with `413 request_too_large` before JSON payload can commit. |
| Complete inline/workspace source | 4 MiB UTF-8 | Applies to derive, replace, and rebuild source admission. |
| Append fragment | 512 KiB UTF-8 | Applies before fragment parsing. |
| Committed complete result | 8 MiB | Applies after serialization and before blob/event commit. |
| Retention soft threshold | 1 GiB | Enter grace state and ask the user to prune. |
| Retention hard threshold | 2 GiB | Start automatic reclamation immediately. |
| Retention grace duration | 7 days | Start automatic reclamation on expiry while still above soft threshold. |
| Reclamation target | below 1 GiB | Provides hysteresis; do not stop at the triggering boundary. |

Tests may dependency-inject smaller thresholds and a fake clock. Runtime defaults
remain fixed in V1 and are not environment-configurable.

## Promotion Rules

- Every later layer preserves the original `/api/canvas/publish`, V0 surface
  identity, and mutable workspace-body behavior.
- Blobs become authoritative only for Operations V1 surfaces.
- A blob must be durable before an event references it.
- Same operation id plus same normalized request returns the original result;
  same id plus different input fails.
- Content commits never redirect unless the committed surface is already the
  display target.
- Current revisions are never pruned. Referenced bodies are deleted only after
  a durable tombstone, and shared bodies remain while any unpruned reference
  exists.
- Promotion evidence must include retained commands, counts, and evidence paths.

## Smallest Coherent Unit

```text
schema and parser contract
  -> immutable blob authority
  -> replayed operations surface
  -> exact V0 derivation
  -> CAS replacement
  -> immutable content after restart
```

This is `SWU-OV1-001` through `SWU-OV1-006`. No smaller runtime slice proves
the accepted separate identity, body authority, CAS, and restart claim together.
