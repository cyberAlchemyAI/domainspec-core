---
id: ide-extension-operations-v1-layering-seed
project: ide-extension
title: "Operations V1 Implementation Layering Seed"
status: design-seed
node_type: implementation-layering-seed
updatedAt: 2026-07-12
---

# Implementation Layering Seed: Operations V1

| Layer | Decision question | Minimum proof | Promotion evidence |
| --- | --- | --- | --- |
| L0 derive and replace | Can an exact V0 revision become an immutable separate surface and accept one CAS-guarded replacement? | Derive route, blob store, replacement operation, immutable content route. | V0 unchanged; derived replacement survives restart. |
| L1 append and retry | Can fragments append once under retries and concurrency? | Parser-based append, operation digest, idempotent replay, stale rejection. | Duplicate, conflict, parser, and concurrent operation matrix passes. |
| L2 rebuild and navigation | Can a surface explicitly rebuild from workspace and display predictably? | Exact-hash rebuild, lineage, redirect/refresh command and acknowledgement. | Drift, restart, notification, and browser evidence pass. |
| L3 declared regions | Is region-scoped mutation valuable and unambiguous? | Separate approved design plus fixtures for stable unique region ids. | Whole-document behavior remains unchanged; region value witness passes. |

## Active Window

Operations V1 planning may activate L0 through L2. L3 remains deferred until
whole-document operations produce value evidence.

## Smallest Coherent Unit

```text
derive exact V0 revision
  -> commit immutable operations surface
  -> replace against expected revision
  -> serve and display committed result after restart
```

This unit proves the separate identity, body authority, CAS, and display path.
Append without this substrate would only create another mutable-file shortcut.

## Distill Verdict

- Coherent unit: derive plus one replacement revision.
- Split pressure: parser append and navigation can follow after storage/CAS.
- Deferred complexity: regions, merge, collaboration, hostile HTML.
- Verdict: `pass` for design handoff to a dedicated Operations V1 plan.
