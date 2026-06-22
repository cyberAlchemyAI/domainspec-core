# TASK-BODY-WAR-AUTH-CONSUMER

## Objective

Move Body War's auth and Strava login boundary off the Python auth package and onto the TypeScript auth package or a TypeScript service/API boundary.

## Source Contracts

- `projects/body-war/app/server.py`
- `projects/body-war/app/static/app.js`
- `projects/body-war/app/test_auth_adapter.py`
- `projects/auth-user-management` TypeScript package outputs from W1

## Smallest Working Units

### SWU-BW-001 - Body War Auth Consumer Boundary

- Dependencies: `SWU-AUTH-004`, `SWU-AUTH-005`.
- Write scope: `projects/body-war/`.
- Done criteria: Body War no longer imports `auth_user_management`; auth/status/logout/Strava start/callback/activity requests consume a TypeScript-owned auth boundary; game/track mechanics unchanged.
- Acceptance evidence: Body War auth smoke/contract test passes; grep shows no Python auth package import.
- Validation surface: Body War auth test command selected during execution, plus `git diff --check -- projects/body-war`.
- Execution owner: local-fallback.
- Handoff note: if full Body War TS server migration is too large, use a small TS auth service boundary first, but final auth authority must remain TypeScript.

## Synchronization

Do not update track/game docs or mechanics in this task.
