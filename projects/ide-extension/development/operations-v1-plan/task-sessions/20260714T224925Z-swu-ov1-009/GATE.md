# Task Gate: SWU-OV1-009

```yaml
swu_id: SWU-OV1-009
verdict: pass
blocking_decisions: []
dependency: SWU-OV1-008 pass
runtime: local
```

## Basis

- OVG-004 selected one durable global display target plus ephemeral refresh and
  acknowledgement state.
- V4 already freezes `canvas.display_target_selected`, redirect command shape,
  display lineage validation, and replay state.
- Navigation request and acknowledgement schemas already pass the SWU-001
  contract boundary.
- The existing mutation queue, persistence store, V0 projection, Operations
  service, blob store, and SSE hub provide all required implementation seams.

## Stop Conditions

- `/api/canvas/current` begins returning Operations state or changes its V0
  contract.
- Refresh or acknowledgement enters the durable event log.
- Operations commits select a new display target.
- Unknown, mismatched, unavailable, or pruned revisions are admitted.
- Redirect idempotency depends on current display rather than committed command
  identity.
- Browser identities, tab-specific targets, durable delivery replay, or queues
  enter scope.
