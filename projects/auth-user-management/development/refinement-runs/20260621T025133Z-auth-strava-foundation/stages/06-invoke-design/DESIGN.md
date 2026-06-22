# Design - Auth User Management Foundation

## Parent Synthesis

The foundation should use a hybrid transport profile:

- Browser clients use an HttpOnly session cookie plus CSRF binding and
  same-origin enforcement.
- Service/API clients may use bearer JWTs whose authoritative identity is the
  `sid` claim and whose validity is checked against server-side session and
  token records.
- Permissions are resolved server-side, with deny-by-default and deny-overrides.

This reconciles the poker-team and Savvy evidence: poker-team proves the bearer
`sid` domain spine, while Savvy proves the browser-session guard shape.

## Components

| Component | Purpose | Source evidence |
|---|---|---|
| `Principal` | Authenticated user or service actor. | poker-team domain |
| `Session` | Server-owned continuity record with status, expiry, permissions, and auth context. | poker-team session, Savvy session record |
| `AccessToken` | Bearer token record with `sid`, `jti`, expiry, and revocation. | poker-team token use cases |
| `PermissionGrant` | Canonical permission assignment with allow/deny behavior. | poker-team permission resolution |
| `AuthContext` | Normalized request context for downstream authorization. | poker-team and Savvy auth contexts |
| `BrowserSessionBinding` | Cookie session id plus CSRF cookie/header binding. | Savvy guard |
| `ProviderAccount` | External account link owned by a principal. | Strava first-consumer requirement |
| `ProviderToken` | Server-side external token custody record. | Strava token custody requirement |
| `AuditEvent` | Redacted trace for auth, provider, and protected-resource decisions. | poker telemetry, Savvy audit fields |

## Interfaces

| Interface | Requirement |
|---|---|
| `login` | Creates server session proof and CSRF binding; never trusts client auth state. |
| `logout` | Terminates session and revokes active bearer/provider tokens where applicable. |
| `authenticateRequest` | Validates cookie or bearer transport and loads server session. |
| `authorizeRequest` | Requires canonical permission and resource scope. |
| `introspectToken` | Reports active/inactive reason for bearer tokens. |
| `connectProvider` | Starts provider OAuth with state and scope intent. |
| `providerCallback` | Validates state, exchanges code, stores tokens server-side, records granted scope. |
| `disconnectProvider` | Revokes or marks provider link disconnected and clears usable tokens. |
| `listProviderActivities` | Returns redacted activity summaries only after auth and scope checks. |

## Body War First Consumer

Body War receives:

- login/logout,
- current user/session,
- Strava connection status,
- activity summary import,
- activity submission handoff to existing Body War evidence logic.

Body War does not receive:

- refresh tokens,
- access tokens,
- client secrets,
- raw private athlete data,
- track geometry logic,
- scoring or game mechanics.

## Strava Scope

Default requested scope: `read,activity:read`.

Escalation: request `activity:read_all` only if a consenting athlete needs
private or Only Me activity import. The UI and audit should make the escalation
explicit.

## Acceptance Gates

1. Forged client auth state cannot access protected routes.
2. Expired, revoked, inactive, malformed, unknown, or orphaned sessions fail.
3. Unsafe browser methods require valid same-origin and CSRF binding.
4. Missing permission or resource mismatch returns deterministic forbidden.
5. Bearer token expiry, revocation, missing `sid`, and inactive session fail.
6. Strava callback validates state and stores tokens only server-side.
7. Strava activity import redacts tokens and avoids broad scope by default.
8. Body War consumer can connect Strava and import activity summaries without
   owning token custody.

## Verdict

Pass for design. The implementation route is separate.
