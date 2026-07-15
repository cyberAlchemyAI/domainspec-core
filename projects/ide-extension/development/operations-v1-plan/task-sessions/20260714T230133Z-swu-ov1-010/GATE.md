# Task Gate: SWU-OV1-010

```yaml
swu_id: SWU-OV1-010
verdict: pass
blocking_decisions: []
dependency: SWU-OV1-009 pass
runtime: local plus real Chromium
```

## Basis

- SWU-009 proves durable display, transient command status/ack, typed notices,
  target admission, and selected-only display advancement.
- The current workbench already preflights content, loads a hidden frame, waits
  for load, atomically swaps, forwards trusted frame messages, and retains a
  manual fallback.
- Migration OV1-EVENT-V4-M1 fixes Operations interaction event semantics while
  preserving the V3 event name and legacy V0 route.
- Desktop and mobile Chromium projects and existing Canvas journeys are already
  installed and runnable.

## Stop Conditions

- The existing visible frame is removed before replacement content loads.
- Browser code reads Operations display from `/api/canvas/current`.
- Refresh is treated as a content revision or durable event.
- Operations interaction payloads enter the V3 V0 route or weaken its schema.
- Non-selected commits reload or redirect the workbench.
- Failure acknowledgement claims loaded, or successful load claims failed.
- Approval desk behavior or existing V0 Canvas journeys regress.
