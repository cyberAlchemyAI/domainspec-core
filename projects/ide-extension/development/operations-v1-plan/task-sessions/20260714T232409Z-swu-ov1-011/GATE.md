# Task Gate: SWU-OV1-011

```yaml
swu_id: SWU-OV1-011
verdict: pass
blocking_decisions: []
dependency: SWU-OV1-010 pass
runtime: local plus real Chromium
```

## Basis

- OVG-003 and cross-task decisions OV1-PD8 through OV1-PD10 freeze the policy,
  reclaim order, and tombstone-before-delete invariant.
- SWU-001 already freezes request schemas, constants, and the two V4 pruning
  event names.
- SWU-003 and SWU-004 prove content-addressed storage, deterministic
  diagnostics, replay-first reference validation, and fail-closed reconciliation.
- SWU-010 proves the browser can consume typed notices and retain a good frame
  while a pruned historical route degrades explicitly.
- The current projector already rejects current, displayed, mismatched,
  duplicate, or request-unbound prune tombstones.

## Stop Conditions

- Any body is deleted before its tombstone commits.
- Current, displayed, shared-still-referenced, or unselected content is deleted.
- Preview candidates derive from a stale projection or filesystem age.
- A stale digest commits a different candidate set.
- Grace requests duplicate while one is active.
- Exact operation retry reruns after body pruning.
- Orphan deletion, timers, startup hooks, or hard-threshold automation enter
  this SWU.
- Existing V0 or navigation behavior changes.
