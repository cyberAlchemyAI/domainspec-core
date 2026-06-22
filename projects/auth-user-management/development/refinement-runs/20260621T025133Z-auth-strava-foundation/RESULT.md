# Refine Result - Auth User Management Strava Foundation

- Target: `projects/auth-user-management`
- Status: `pass`
- Preset: `standard`
- Research: `research-if-gap-appears`
- Dispatch route: `REFINE-DISPATCH.json`
- Dispatch validation: `pass`
- Runtime handoff: `RUNTIME-HANDOFF.md`
- Run manifest: `RUN-MANIFEST.md`
- Evidence index: `evidence-index.json`

## Final Synthesis

The right first product slice is a reusable auth/user-management foundation,
with Body War as the first consumer for login plus Strava connection. Track
geometry and game mechanics remain deferred.

The selected foundation shape is hybrid:

- browser flows use an HttpOnly cookie session plus CSRF binding and same-origin
  enforcement,
- service/API flows may use bearer JWTs whose authoritative identity is the
  server-backed `sid`,
- all protected routes load server-side session and token state before trusting
  request bodies,
- permissions are canonical, deny-by-default, and deny-overrides,
- provider links and provider tokens are server-owned,
- Strava is the first provider adapter.

## Decisions

- `DEC-AUTH-TRANSPORT-001`: selected
  `hybrid-cookie-for-browser-bearer-for-service-api`.
- `DEC-AUTH-STRAVA-SCOPE-001`: selected
  `link-identity-and-import-recent-activity-summaries`.
- Default Strava scope: `read,activity:read`.
- Explicit escalation: `activity:read_all` only when a consenting athlete needs
  private or Only Me activity import.

## What Transfers

From poker-team:

- `sid` as server-backed session authority,
- Principal, Session, AccessToken, PermissionGrant, AuthContext,
- login, logout, authenticate, authorize, introspect,
- token revocation, inactive reasons, deny-overrides, and P0 auth tests.

From Savvy:

- cookie session id,
- server session store lookup,
- session expiry/revocation checks,
- CSRF cookie/header binding,
- resource scope,
- audit context,
- forged-auth/CSRF/permission/session denial tests.

From Body War:

- Strava connection as first consumer,
- recent activity summary import,
- redacted run-submission handoff.

## What Does Not Transfer

- poker-specific roles and permission namespaces,
- fixed TTLs as universal policy,
- bootstrap password logging,
- bearer-only assumption,
- Savvy mock 2FA,
- client-supplied `authStatus`,
- localStorage as session authority,
- real Strava tokens or athlete data in repo artifacts.

## Stage Evidence

- Context Builder evidence baseline: `pass`
- Invoke Define: `pass`
- Interrogation refine-review: `pass`
- Research decision: `pass`
- Distill: `pass`
- Invoke Redefine / Design: `pass`
- Interrogation refine-design-review: `pass`
- Distill Repair: `pass`
- Invoke Plan: `pass`
- Final Interrogation and Synthesis: `pass`

## Recommended Next Routes

1. `task-session` for `SWU-AUTH-001`: reusable auth core domain and ports.
2. `task-session` for `SWU-AUTH-002`: browser session guard and tests.
3. `task-session` for `SWU-AUTH-005`: Strava provider adapter.
4. `task-session` for `SWU-BW-AUTH-001`: Body War first consumer adapter.

## Residue

Implementation remains pending. Body War's real Strava activity evidence
blocker remains active until a consenting activity imports and submits without
token leakage.
