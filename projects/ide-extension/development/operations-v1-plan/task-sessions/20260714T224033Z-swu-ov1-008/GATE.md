# Task Gate: SWU-OV1-008

```yaml
swu_id: SWU-OV1-008
verdict: pass
blocking_decisions: []
dependency: SWU-OV1-007 and L1 promotion pass
runtime: local
```

## Basis

- The task contract fixes exact-hash source admission, parser, limits, lineage,
  identity, retry, and no-implicit-sync behavior.
- Canonical workspace path admission and generic operation/CAS/blob/event/CLI
  infrastructure already pass.
- No new route, event, authority, destructive, or navigation choice remains.

## Stop Conditions

- Workspace bytes accepted after expected-hash drift.
- External-link, directory, or missing source admitted.
- Operations surface identity replaced rather than advanced.
- V0 publish implicitly triggers rebuild.
- Workspace content used for ordinary Operations revision content reads.
- Navigation, refresh, browser, retention, or region behavior enters scope.
