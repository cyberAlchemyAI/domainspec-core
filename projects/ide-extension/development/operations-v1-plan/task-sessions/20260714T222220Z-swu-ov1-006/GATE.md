# Task Gate: SWU-OV1-006

```yaml
swu_id: SWU-OV1-006
verdict: pass
blocking_decisions: []
dependency: SWU-OV1-005 pass
runtime: local
```

## Basis

- The accepted task contract fixes schema, normalization, lookup-before-CAS,
  retry, parse5, limits, storage ordering, content, and notification semantics.
- The V4 content event and projection bindings passed SWU-OV1-004.
- Exact derivation and server/blob-store integration passed SWU-OV1-005.
- No product, destructive, authority, remote-control, or new schema-version
  choice remains in this bounded unit.

## Stop Conditions

- Duplicate revision on exact retry.
- Stale writer merge or overwrite.
- Workspace reread for Operations content.
- Result event before durable blob.
- Implicit redirect or V0 current mutation.
- Append, rebuild, browser navigation, retention deletion, or region behavior.
