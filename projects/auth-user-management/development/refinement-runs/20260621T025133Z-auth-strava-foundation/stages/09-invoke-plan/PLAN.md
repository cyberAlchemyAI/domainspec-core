# Plan - Auth User Management Implementation Route

## Work-Pack Shape

This is a non-executed implementation plan. Route each SWU through
`task-session`; do not implement all slices in one uncontrolled change.

## SWUs

| SWU | Goal | Write Scope | Depends On | Done Criteria |
|---|---|---|---|---|
| SWU-AUTH-001 | Define reusable core domain and ports. | `projects/auth-user-management/src/core/`, tests | none | Principal, Session, AccessToken, PermissionGrant, AuthContext, ProviderAccount, ProviderToken, AuditEvent types and ports exist. |
| SWU-AUTH-002 | Implement browser cookie session guard. | `projects/auth-user-management/src/browser/`, tests | SWU-AUTH-001 | HttpOnly cookie contract, CSRF binding, same-origin guard, permission/resource denial tests. |
| SWU-AUTH-003 | Implement bearer `sid` guard. | `projects/auth-user-management/src/bearer/`, tests | SWU-AUTH-001 | Missing/invalid/expired/revoked token and inactive session tests pass. |
| SWU-AUTH-004 | Implement storage adapter contract. | `projects/auth-user-management/src/storage/`, docs | SWU-AUTH-001 | Session/token/provider-token persistence interface and migration notes exist. |
| SWU-AUTH-005 | Implement Strava provider adapter. | `projects/auth-user-management/src/providers/strava/`, tests | SWU-AUTH-001, SWU-AUTH-004 | OAuth state, callback, scope validation, token custody, refresh/revoke, redacted activity summaries. |
| SWU-AUTH-006 | Write copy/adoption guide. | `projects/auth-user-management/docs/` | SWU-AUTH-001..005 | Project adoption checklist covers env, storage, permissions, routes, tests, and boundaries. |
| SWU-BW-AUTH-001 | Body War first consumer. | `projects/body-war/` app/spec files | SWU-AUTH-002, SWU-AUTH-005 | Body War can login, connect Strava, import activity summaries, and submit one run without owning token custody. |

## First Implementation Recommendation

Start with `SWU-AUTH-001` and `SWU-AUTH-002` together only if the write scopes
stay cleanly separated. Otherwise run `SWU-AUTH-001` first.

## Validation Gates

- Typecheck and unit tests for each package slice.
- Guard tests reject forged body auth, bad cookies, unknown/expired/revoked
  sessions, missing/invalid CSRF, missing permission, and resource mismatch.
- Bearer tests reject invalid signature, expired token, revoked token, missing
  `sid`, and inactive/missing session.
- Strava tests use fixtures only: no real token, secret, or athlete data in repo.
- Markdown/JSON/YAML parse checks for planning surfaces.
- `git diff --check`.

## Explicit Non-Goals

- Track geometry.
- Scoring and game rules.
- Anti-cheat automation.
- Payments, RunCoins, premium, or sponsor mechanics.
- Full hosted deployment proof.

## Next Route

Run `task-session` for `SWU-AUTH-001`.
