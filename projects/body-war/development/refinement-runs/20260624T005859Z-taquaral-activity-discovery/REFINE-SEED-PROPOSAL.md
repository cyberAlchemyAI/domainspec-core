---
node_type: refine-seed-proposal
status: strategy-proposed
run_id: 20260624T005859Z-taquaral-activity-discovery
target: projects/body-war/app
preset: standard
research_mode: research-if-gap-appears
---

# Refine Seed Proposal: Taquaral Circuit Discovery

## Operator Intent

The hosted TROQAR app is online with Strava login. A connected runner may have
the Parque Taquaral circuit activity in their Strava history. Before building
track/game mechanics, define the architecture and plan for asking the runner for
the minimum data needed to identify and import that activity safely.

## Refined Target

Add a connected-home discovery box that helps a consenting runner identify the
activity that contains the Taquaral circuit, then submit it as protected preview
evidence. The first slice must not claim verified geometry or game scoring.

## Source Context

- `projects/body-war/app/server.ts` already exposes Strava auth, status,
  profile, activity summaries, tracks, and submissions.
- `projects/body-war/app/static/index.html` and `app.js` already render a
  connected home with profile, activities, tracks, and evidence submissions.
- `projects/body-war/app/src/auth/strava-oauth.ts` stores Strava tokens
  server-side and currently lists repository activity summaries rather than
  live Strava activity summaries.
- Existing Body War planning says friend/Taquaral activity evidence requires
  consent, token safety, redaction, and no geometry claim before source-backed
  evidence exists.

## Write Scope For Future Implementation

- `projects/body-war/app/server.ts`
- `projects/body-war/app/src/auth/*`
- `projects/body-war/app/src/infrastructure/postgres/*`
- `projects/body-war/app/static/*`
- `projects/body-war/app/tests/*`
- `projects/body-war/app/e2e/*`
- feature docs under `projects/body-war/docs/features/parque-taquaral-online-mvp/`

## Non-Goals

- No city-wide map, territory control, scoring, leaderboard, or anti-cheat.
- No raw Strava token or raw private activity payload in the browser or repo
  docs.
- No final Parque Taquaral route geometry claim from a single activity until an
  explicit geometry artifact is approved.

## Done Criteria For The Future Task Session

1. Connected home shows a Taquaral discovery box.
2. The box states the data needed: approximate date, activity selection,
   distance/time check, and explicit consent to use the selected activity as
   preview evidence.
3. Backend can list real Strava run summaries from the connected account.
4. Backend can persist a protected Taquaral activity candidate.
5. UI shows whether the candidate is `needs_selection`, `candidate_submitted`,
   `operator_review`, or `source_backed`.
6. Tests prove no token, refresh token, or raw private payload reaches the page.

## Research Decision

`research-if-gap-appears`. Local evidence is enough for the architecture and
plan. External Strava docs are only needed during implementation for exact API
field contracts.
