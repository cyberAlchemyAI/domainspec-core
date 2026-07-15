# Operations V1 Event V4 Migration

- Migration: `OV1-EVENT-V4-M2`
- Date: 2026-07-15
- Source decision: human-selected Option 1 in
  `../20260714T234403Z-swu-ov1-012/DECISION-GATE.md`
- Compatibility: additive event name and reducer before automatic cleanup emits

## Change

The Operations V1 event version 4 vocabulary migrates from six to seven names
by adding:

```text
canvas.pruning_completed
```

The event records cleanup-only convergence when replay-proven orphan and/or
temporary deletion brings storage below soft without requiring a revision
tombstone. Its exact completion payload binds:

- the active pruning request,
- the automatic trigger (`hard_threshold`, `grace_expired`, or `recovery`),
- reclaimed orphan bytes,
- reclaimed temporary bytes,
- final physical Canvas storage bytes,
- completion timestamp.

The projector accepts the event only while the referenced request is active
and only when `final_total_bytes` is below that request's `soft_limit_bytes`.
It then records the completion, returns retention to `normal`, and clears
`active_request`.

Existing V4 histories replay unchanged. `canvas.revision_pruned` remains an
exact revision tombstone and is never fabricated for cleanup-only convergence.
Automatic revision tombstones remain `reclaiming`; the completion event closes
the request only after physical storage is verified below soft.
V1/V2/V3 names, shapes, and projections remain unchanged.

## Required Evidence

- Contract tests assert the seven-name vocabulary.
- Replay tests prove valid completion, exact shape, active-request binding, and
  below-soft validation.
- Existing V4 fixtures replay without rewriting.
- Automatic orphan-only recovery emits the new completion after deletion.
- Unknown V4 names continue to fail closed.
