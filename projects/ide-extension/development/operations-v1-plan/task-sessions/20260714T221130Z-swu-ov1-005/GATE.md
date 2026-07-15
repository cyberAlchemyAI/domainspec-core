# Task Gate: SWU-OV1-005

```yaml
swu_id: SWU-OV1-005
verdict: pass
blocking_decisions: []
dependency: SWU-OV1-004 pass
runtime: local
```

## Basis

- The accepted task contract fixes interfaces, ordering, normalization,
  idempotency, exact-source admission, stable failures, and no-redirect
  postconditions.
- The existing Canvas reader is the canonical workspace admission boundary.
- SWU-OV1-003 and SWU-OV1-004 prove blob-before-event durability and strict V4
  replay/reference recovery.
- The existing server mutation queue is the declared serialization boundary.
- No product, authority, destructive, remote-control, or schema-version choice
  remains for this bounded unit.

## Stop Conditions

- V0 mutation, republish, redirect, or implicit synchronization.
- Blob/event creation after source drift or unavailability.
- Reuse of one derivation key for different normalized input.
- Event append before exact bytes are durable.
- New operation, browser, navigation, or retention behavior.
