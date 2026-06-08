# Strava-Linked Pilot Test Implementation Layering

## Invoke Result

- Mode: plan
- Spell: invoke
- Scope: Body War / TROQAR Strava-linked pilot testing
- Phase status: pass
- Companion work-pack: `WORK-PACK.md`
- Target app: `projects/body-war/app/`
- Next route: task-session

## Purpose

Define the layer boundaries for testing the first app-backed Strava validation channel without expanding into production architecture, mobile implementation, full anti-cheat, payment, or map/track geometry automation.

## Layer Boundary

| Layer                    | Decision Question                                            | Test Scope                                                                          | Promotion Evidence                                                                                                      |
| ------------------------ | ------------------------------------------------------------ | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| L0 - Local Smoke         | Does the backend and UI boot without Strava credentials?     | Compile backend, start server, hit `/`, `/api/status`, `/api/tracks`.               | Local endpoints return expected unauthenticated responses.                                                              |
| L1 - OAuth Link          | Can a real athlete connect through Strava OAuth?             | Configure `.env`, register callback, connect Strava, verify athlete status.         | `/api/status` reports `connected=true` and athlete identity without exposing tokens.                                    |
| L2 - Activity Evidence   | Can a recent Strava run become pilot evidence?               | Fetch activities, select a run, submit to a pilot track.                            | `/api/submissions` contains an evidence row with track, activity, athlete, time, distance, and hybrid authority fields. |
| L3 - Failure And Refresh | Does the pilot behave safely when auth or API state changes? | Invalid config, denied auth, expired token refresh, no runs, Strava error response. | Failures are visible, non-destructive, and do not leak credentials or corrupt submissions.                              |

## Source Constraints

- Strava web OAuth starts at `GET https://www.strava.com/oauth/authorize`.
- Strava redirects with an authorization `code` and accepted `scope`; the code is exchanged at `POST https://www.strava.com/oauth/token`.
- Access tokens are short-lived and must be refreshed with the most recent refresh token.
- `localhost` and `127.0.0.1` are permitted callback domains for local testing.
- Listing athlete activities uses `GET /api/v3/athlete/activities` and requires `activity:read`; private "Only Me" activities require `activity:read_all`.

## Non-Goals

- Do not store real credentials in git.
- Do not test payment, RunCoins, sponsors, or premium hooks.
- Do not implement GPS polygon validation.
- Do not claim production security readiness.
- Do not promote Craft or Body War artifacts from this test alone.

## Layer Exit Rules

- L0 can pass without Strava credentials.
- L1 requires real Strava app credentials and a consenting test athlete.
- L2 requires at least one visible Strava run or a documented no-run blocker.
- L3 can pass through controlled local simulation for token expiry and visible error handling.

## Blockers

| Blocker                                  | Owner        | Effect                                                                                           |
| ---------------------------------------- | ------------ | ------------------------------------------------------------------------------------------------ |
| Missing Strava app credentials           | Operator     | Blocks L1 and later.                                                                             |
| Callback mismatch in Strava app settings | Operator     | Blocks OAuth callback.                                                                           |
| No recent visible run activity           | Test athlete | Blocks activity submission unless test switches to `activity:read_all` or creates a visible run. |
| Network/API unavailability               | External     | Blocks live API verification but not local smoke tests.                                          |
