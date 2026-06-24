---
node_type: refine-seed-proposal
status: strategy-proposed
run_id: 20260624T010822Z-suggested-track-expansion-route
target: projects/body-war/app
preset: standard
research_mode: research-if-gap-appears
---

# Refine Seed Proposal: Suggested Track Expansion Route

## Operator Intent

Refine the newer route: instead of centering the feature on one person's
Taquaral activity, model track expansion as a natural user action. A runner can
suggest a track, other runners can help provide Strava evidence, and a suggested
track can later become source-backed and pilot-ready.

## Refined Unit

`SuggestedTrack` is the product anchor.

```text
SuggestedTrack -> EvidenceRequest -> ActivityEvidenceCandidate -> SourceBackedTrack
```

Taquaral becomes the first suggested track:

```text
Volta do Taquaral
status: needs_evidence
```

Strava activity consultation remains live and private until the runner chooses
to attach one activity as evidence with consent.

## Source Context

- The app already has Strava login, profile, activity list, track cards, and
  preview evidence submission.
- Existing docs warn that real friend activity requires consent and that
  Parque Taquaral geometry must not be claimed before source-backed evidence.
- The current `tracks.json` has placeholder track metadata; this route gives
  that concept a natural expansion lifecycle.

## Write Scope For Future Implementation

- `projects/body-war/app/src/infrastructure/postgres/schema.ts`
- generated Drizzle migrations under `projects/body-war/app/drizzle/`
- `projects/body-war/app/server.ts`
- `projects/body-war/app/src/auth/*`
- `projects/body-war/app/static/*`
- `projects/body-war/app/tests/*`
- `projects/body-war/app/e2e/*`
- feature docs under `projects/body-war/docs/features/parque-taquaral-online-mvp/`

## Done Criteria For The Future Task Session

1. `SuggestedTrack` and `TrackEvidenceCandidate` are specified.
2. Taquaral is represented as a seed suggested track, not hardcoded as a single
   special-case activity request.
3. The UI lets a connected runner ask for a new track or help an existing
   suggestion.
4. Strava activities are consulted live and redacted.
5. Activity evidence is saved only after explicit consent.
6. The app never claims verified geometry until source-backed promotion.

## Research Decision

`research-if-gap-appears`. Local repository evidence is enough for route
architecture. External Strava docs may be needed during implementation for exact
activity fields and stream/polyline APIs.
