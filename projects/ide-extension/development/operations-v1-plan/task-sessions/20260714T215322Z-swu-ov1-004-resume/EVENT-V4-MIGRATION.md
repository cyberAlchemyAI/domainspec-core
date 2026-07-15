# Operations V1 Event V4 Migration

- Migration: `OV1-EVENT-V4-M1`
- Date: 2026-07-14
- Source decision: human-selected Option 1 in
  `../20260714T214740Z-swu-ov1-004/DECISION-GATE.md`
- Compatibility: additive event-name correction before any V4 route emits

## Change

The SWU-OV1-001 event version 4 vocabulary migrates from five to six names by
adding:

```text
canvas.interaction_recorded
```

The name is intentionally shared with event version 3. `event_version` selects
the binding:

- V3 binds interactions to the displayed/current V0 Canvas surface/revision.
- V4 binds interactions to the durable displayed Operations V1
  surface/revision.

No emitted history requires rewriting because V4 event-producing routes do not
exist yet. V1/V2/V3 event names, shapes, and projections remain unchanged.

## Required Evidence

- Contract constants and tests assert the six-name vocabulary.
- V3 fixtures continue to replay byte-for-byte equivalently.
- V4 fixtures prove the Operations interaction shape and display-target binding.
- Unknown V4 names continue to fail closed.
