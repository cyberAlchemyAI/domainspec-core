---
node_type: refine-result
status: strategy-proposed
run_id: 20260624T010822Z-suggested-track-expansion-route
---

# Refine Result: Strategy Proposed

The refined route is `SuggestedTrack` first:

```text
SuggestedTrack -> EvidenceRequest -> ActivityEvidenceCandidate -> SourceBackedTrack
```

Taquaral becomes the first seeded suggestion, not a special-case activity
workflow.

## Status

`flag`: architecture and plan are ready for confirmation. Runtime-backed
execution and implementation are blocked until the operator confirms.

## Recommended Next Route

Task Session on Slice 1:

1. Update feature specs with `SuggestedTrack`, `TrackEvidenceCandidate`, and
   status lifecycle.
2. Add Drizzle schema and generated migrations for Postgres.
3. Seed "Volta do Taquaral" as `needs_evidence`.
4. Keep Strava activity consult ephemeral until the runner consents to attach
   one activity.
