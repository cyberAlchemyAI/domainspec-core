# Context Pack - Auth User Management Strava Foundation

## Runtime Frame

- Run id: `20260621T025133Z-auth-strava-foundation`
- Dispatch id: `refine-20260621-auth-strava-foundation`
- Target: `projects/auth-user-management`
- Confirmed action: run the validated refine strategy with three read-only
  delegated lanes.
- Write scope: `projects/auth-user-management/` and Body War planning links.
- Read-only references: `validation/poker-team/`,
  `projects/savvy_legal-studio-ai/`, and `projects/body-war/`.

## Operator Intent

Leave track geometry and game mechanics for later. First make login, auth,
user/session management, and Strava connection possible. Shape this as a
reusable auth/user-management project that can be copied into later projects.

## Local Evidence

| Evidence | Role |
|---|---|
| `validation/poker-team/docs/features/auth-access-control/SPEC.md` | Implemented auth-access-control DomainSpec. |
| `validation/poker-team/docs/features/auth-access-control/TEST-SPEC.md` | Deterministic auth test obligations. |
| `validation/poker-team/backend/src/use-cases/auth-access-control/` | Login, logout, authenticate, authorize, introspect behavior. |
| `projects/savvy_legal-studio-ai/frontend/savvy-legal-studio/lib/auth/savvy-auth.ts` | Browser cookie/session/CSRF guard proof. |
| `projects/savvy_legal-studio-ai/frontend/savvy-legal-studio/tests/auth/savvy-auth.test.ts` | Guard tests for forged auth, CSRF, permission, and session failures. |
| `projects/body-war/docs/features/strava-linked-pilot/WORK-PACK.md` | Strava OAuth and activity submission test plan. |
| `projects/body-war/.craft/ledger.yml` | Body War auth-first pivot and active Strava blocker. |

## External Check

Official Strava developer documentation was checked only for the named provider
scope gap. The check confirmed that applications should request only needed
scopes, `activity:read` reads activities visible to Everyone and Followers, and
`activity:read_all` extends access to Only You activities and privacy-zone data.
The Strava changelog also records a 2026-04-23 authentication response change:
the returned `scope` field is space-delimited.

## Boundaries

- No runtime code is edited in this refine run.
- No private validation content is copied into public `arcanum` surfaces.
- No Strava client secret, access token, refresh token, authorization code, or
  raw athlete data is written to repository artifacts.
- Track geometry and game mechanics remain deferred.

## Coverage Verdict

Pass for context baseline. The evidence is sufficient for a non-executed
production-ready plan.
