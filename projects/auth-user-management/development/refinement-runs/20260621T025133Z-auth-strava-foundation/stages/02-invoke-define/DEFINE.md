# Define - Reusable Auth User Management Foundation

## Definition

Auth User Management is a reusable private foundation for projects that need:

1. user identity,
2. login and logout,
3. server-owned session continuity,
4. access token and session lifecycle,
5. permission and resource authorization,
6. browser session protection,
7. provider account links,
8. provider token custody,
9. audit events,
10. adoption tests and copy guide.

Body War is the first consumer: it should use the foundation for login, a
server-owned user/session, and Strava connection before any track geometry or
game mechanics resume.

## Ownership Split

| Layer | Owner | Responsibility |
|---|---|---|
| Core domain | `projects/auth-user-management` | Principal, session, token, permission, provider account, audit types. |
| Browser adapter | `projects/auth-user-management` | HttpOnly session cookie, CSRF binding, same-origin guard, no body-trust auth. |
| API adapter | `projects/auth-user-management` | Bearer JWT with authoritative `sid` and server session/token lookup. |
| Storage adapter | Future implementation route | Session store, token store, provider token store, migrations. |
| Strava adapter | First provider package | OAuth start/callback, scope checks, token refresh/revoke, activity summary import. |
| Body War consumer | `projects/body-war` | Login UI and Strava connection usage; no token custody. |

## Transfer Rules

From poker-team:

- Keep: Principal, Session, AccessToken, PermissionGrant, AuthContext,
  AuthenticateRequest, AuthorizeRequest, Logout, IntrospectToken, server-side
  revocation and deny-overrides.
- Exclude: poker roles, poker namespaces, player visibility rules, fixed TTLs,
  admin bootstrap password logging, `JWT_SECRET` fallback.

From Savvy:

- Keep: cookie session id, session store lookup, session expiry/revocation,
  CSRF cookie/header binding, resource scope check, audit context, denial tests.
- Exclude: mock 2FA, client-supplied `authStatus`, localStorage authority,
  JSON fixture session store as production backing.

From Body War:

- Keep: first-consumer provider need, Strava OAuth/activity summary import,
  redacted activity-submission evidence.
- Exclude: track geometry, anti-cheat automation, scoring, monetization, and
  game mechanics for this first slice.

## Done Shape

A later task-session should be able to implement the foundation as a copyable
package boundary with tests before Body War consumes it.
