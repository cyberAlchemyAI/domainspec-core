---
node_type: refine-result
status: pass
run_id: 20260629T050046Z-suggested-track-decision-build-route
authorization: approved
---

# Refine Result: SuggestedTrack Decision And One-Go Build Route

The confirmed Refine route is complete and ready for a Task Session handoff.

## Selected Path

```text
open decision slate -> confirm defaults -> reviewed Refine loop -> one-go Task Session handoff
```

## Proposed Defaults

1. Connected runners can see suggested tracks in L0.
2. Login is required before submitting a suggestion.
3. "Volta do Taquaral" is versioned seed data applied idempotently after Drizzle
   migration.
4. Operator-only promotion controls `source_backed` status in L0.
5. The build reuses the existing Body War Postgres/Drizzle stack.
6. Taquaral stays `needs_evidence` until source-backed evidence exists.
7. The one-go build includes docs, schema, migration, seed, API, UI, and tests,
   but excludes pilot-ready/source-backed geometry claims.

## Status

`pass`: no blocker remains for the next `task-session` route.

The future Task Session still has a hard preflight: update the feature
docs/work-pack gate before mutating app code.

## Review Outcome

- `product-decision-synthesist`: `flag`, repaired by Craft alignment and copy
  polish in the handoff.
- `data-security-schema-reviewer`: `pass`.
- `one-go-build-slice-planner`: `flag`, repaired by explicit preflight gate and
  validation commands.

## Next Route

`task-session` on `HND-SUGGESTED-TRACK-ONE-GO-BUILD-001`.

The task-session should build docs, schema, migration, seed, API, UI, and tests
in one pass, while preserving no raw Strava persistence and no source-backed or
pilot-ready overclaim.
