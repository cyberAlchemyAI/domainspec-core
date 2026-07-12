# Execution Pack: Operations V1

## Choreography

```text
W0 contracts and transformer
  -> W1 immutable blob and replay substrate
  -> W2 exact derivation and replacement
  -> W3 append and retry
  -> W4 rebuild and navigation
  -> W5 retention lifecycle
  -> W6 value proof and integrated closeout
```

## Wave Map

| Wave | Layer | Tasks | SWUs | Entry gate | Exit evidence |
| --- | --- | --- | --- | --- | --- |
| [W0](work-pack/waves/W0.md) | L0 | Contract/transform | 001-002 | Closed planning gate. | Schemas, budgets, and golden parse5 output pass. |
| [W1](work-pack/waves/W1.md) | L0 | Blob/replay | 003-004 | W0 pass. | Atomic blobs and mixed V1-V4 replay survive restart. |
| [W2](work-pack/waves/W2.md) | L0 | Derive/replace | 005-006 | W1 pass. | Smallest coherent unit and V0 compatibility pass. |
| [W3](work-pack/waves/W3.md) | L1 | Append | 007 | W2 pass. | Exactly-once fragment append/concurrency matrix passes. |
| [W4](work-pack/waves/W4.md) | L2 | Rebuild/navigation | 008-010 | W3 pass. | Exact rebuild and durable workbench target pass browser restart. |
| [W5](work-pack/waves/W5.md) | L2 | Retention | 011-012 | W4 pass. | Manual grace and automatic reclaim preserve tombstone invariants. |
| [W6](work-pack/waves/W6.md) | L2 | Value/verify | 013-014 | W5 pass. | Real agent-to-browser witness and integrated audit pass. |

## Parallelism

Execution is sequential. Projector, server, schema registry, CLI, browser, and
shared tests overlap across tasks. Conceptual independence is not sufficient to
justify concurrent writes. A later coordinator may parallelize read-only
validation, but mutation still follows SWU order.

## Execution Receipt Handoff

Every SWU returns:

- exact files touched and whether pre-existing changes intersected them;
- commands, counts, and results;
- created event/schema/route names when applicable;
- blocker and residue classification;
- retained Task Session result path;
- next ready SWU or explicit stop reason.

## Promotion Gates

- W0 -> W1: exact parser and size contracts are frozen.
- W1 -> W2: event replay cannot reference an absent committed body.
- W2 -> W3: derive-plus-replace survives restart and V0 remains unchanged.
- W3 -> W4: append is exactly-once under retry/concurrency.
- W4 -> W5: workbench target and rebuild semantics survive restart.
- W5 -> W6: retention never silently deletes current/shared/un-tombstoned data.
- Close: value witness and integrated audit support only the accepted honest
  claim, not regions, collaboration, hostile HTML safety, or remote control.

## Stop Conditions

- Stop on any need to change the accepted V0 request/response behavior.
- Stop if an event can commit before its body is durable.
- Stop if operation normalization or serialization is nondeterministic.
- Stop if exact retry can create a second revision.
- Stop if automatic reclaim can run after malformed or partial replay.
- Stop if browser navigation requires durable per-browser identity.
- Stop before any declared-region implementation.
