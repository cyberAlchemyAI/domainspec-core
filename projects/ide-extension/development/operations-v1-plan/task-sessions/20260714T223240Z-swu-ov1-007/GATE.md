# Task Gate: SWU-OV1-007

```yaml
swu_id: SWU-OV1-007
verdict: pass
blocking_decisions: []
dependency: SWU-OV1-006 and L0 promotion pass
runtime: local
```

## Basis

- SWU-OV1-002 froze body-context parse5 append bytes.
- SWU-OV1-006 proved normalization, operation lookup, CAS, limits, blob/event
  ordering, immutable content, CLI, and crash recovery.
- The accepted task contract fixes the fragment corpus and browser witness.
- No new API, event, authority, destructive, or navigation choice remains.

## Stop Conditions

- Raw string insertion or partial content.
- Duplicate event/revision on retry.
- Stale auto-rebase, merge, or overwrite.
- Workspace reread for current Operations content.
- Parser serializer drift from SWU-OV1-002.
- Notification or redirect for a non-selected surface.
