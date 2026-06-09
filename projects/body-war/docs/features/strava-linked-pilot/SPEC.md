# Strava-Linked Pilot Spec

## Summary

Strava-Linked Pilot is the first app-backed validation channel for TROQAR / Body War. It lets a runner connect Strava, fetch recent run activities, and submit one activity as evidence for a pilot track.

## Decision Context

| Decision                 | Selected                                                                 |
| ------------------------ | ------------------------------------------------------------------------ |
| Validation channel       | App/runtime-backed MVP with Strava API link and backend.                 |
| Public controller metric | Fastest verified time.                                                   |
| Parallel evidence        | Composite score and activity metadata recorded for later analysis.       |
| Monetization             | Unresolved; should remain out of this feature until explicitly selected. |

## Goals

- Prove the backend can link a runner account to Strava through OAuth.
- Fetch recent Strava activities for the connected athlete.
- Let a runner submit one recent run as track-control evidence.
- Store enough local evidence for pilot review without building the full mobile app.

## Non-Goals

- No payment, RunCoins, premium, or sponsor mechanics.
- No full GPS polygon/track-boundary validation.
- No anti-cheat automation beyond preserving activity metadata for later review.
- No mobile app implementation.

## Runtime Surface

| Surface    | Path                              | Purpose                                                                   |
| ---------- | --------------------------------- | ------------------------------------------------------------------------- |
| Backend    | `projects/body-war/app/server.py` | Serves UI, handles Strava OAuth, fetches activities, records submissions. |
| Frontend   | `projects/body-war/app/static/`   | Pilot operator/runner UI.                                                 |
| Local data | `projects/body-war/app/data/`     | Development token, track, and submission storage; ignored by git.         |

## Planning Artifacts

| Artifact                     | Purpose                                                                                                           |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| `IMPLEMENTATION-LAYERING.md` | L0-L3 test layer boundaries and promotion evidence.                                                               |
| `WORK-PACK.md`               | Executable test plan for local smoke, OAuth, activity import, submission, failure handling, and readiness review. |
| `test-runs/20260608-strava-test-001.md` | First local smoke and OAuth-start preflight report. |

## API Contract

| Route                       | Method | Purpose                                    |
| --------------------------- | ------ | ------------------------------------------ |
| `/api/status`               | GET    | Configuration and Strava connection state. |
| `/api/auth/strava/start`    | GET    | Start Strava OAuth.                        |
| `/api/auth/strava/callback` | GET    | Exchange OAuth code for tokens.            |
| `/api/activities`           | GET    | Fetch recent Strava activities.            |
| `/api/tracks`               | GET    | Return pilot track list.                   |
| `/api/submissions`          | GET    | Return local evidence submissions.         |
| `/api/submissions`          | POST   | Submit a Strava activity to a track.       |

## Acceptance Criteria

- App starts locally with `python3 server.py`.
- `/api/status` returns JSON even without Strava credentials.
- `/api/tracks` returns a Craft internal pilot track and a Body War placeholder physical track.
- Strava credentials are read from `.env` and are not committed.
- Token and submission JSON are ignored by git.
- Dispatch validation remains `pass` after the implementation decision is recorded.

## Source References

- `docs/decisions/mvp-readiness.md`
- `docs/features/park-track-pilot/implementation-layering.md`
- `app/README.md`
- `IMPLEMENTATION-LAYERING.md`
- `WORK-PACK.md`
