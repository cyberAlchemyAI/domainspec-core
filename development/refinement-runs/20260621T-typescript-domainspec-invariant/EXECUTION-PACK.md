# Execution Pack

Run ID: `20260621T-typescript-domainspec-invariant`

## Wave Order

1. [W0](work-pack/waves/W0.md) - TypeScript package baseline.
2. [W1](work-pack/waves/W1.md) - Auth and Strava behavior.
3. [W2](work-pack/waves/W2.md) - Repo invariant and Body War consumer.
4. [W3](work-pack/waves/W3.md) - Production readiness.

## Execution Rule

Execute one SWU at a time. The first selected SWU is `SWU-AUTH-001`.

## Receipt Shape

```yaml
swu_id: SWU-AUTH-001
result: pass | flag | block | interrupted
capability_ref: task-session
receipt_kind: native-stage | local-fallback | blocked
receipt_artifact: <path or none>
files_touched:
  - <path>
validation:
  - <command and result>
blockers:
  - <blocker or none>
residue:
  - <unresolved evidence or none>
reroute: <next owner or none>
handoff_note: <what the parent coordinator needs next>
```

## Parallelization

No parallel execution until `SWU-AUTH-001` passes. After W0, `SWU-AUTH-002` and `SWU-INV-001` may be prepared in parallel only if write scopes stay disjoint.
