# BodyWar Auth Integration Spec

Status: `invoke-spec-pass`
Target: `projects/body-war/app` plus `@domainspec/auth-user-management`
Date: 2026-06-21

## Purpose

Make BodyWar/TROQAR login, browser session, minimal runner profile, Strava
connection status, and Strava profile link work against the reusable
`@domainspec/auth-user-management` package without importing non-existent
browser/OAuth helpers from that package.

## Capability Boundary

| Capability | Owner | Included |
| --- | --- | --- |
| Core auth domain | `@domainspec/auth-user-management` | principals, sessions, access tokens, permission grants, permission resolution, logout, token authentication, Drizzle repositories, generated auth migrations. |
| Browser session adapter | BodyWar app | cookie parsing, HttpOnly session cookie, CSRF cookie/header binding, origin checks, route guards, error-to-HTTP mapping. |
| Strava OAuth adapter | BodyWar app | OAuth state, callback, code exchange, provider token custody, provider account linkage, activity summary gateway. |
| Runner profile projection | BodyWar app | display name, Strava profile URL, privacy status, validation caveats, profile read model. |
| Activity import | BodyWar app | redacted Strava activity summaries and no-geometry/no-scoring authority receipt. |
| Deployment | BodyWar infra | Caddy, Postgres, app service, secret inventory, deployment receipts. |

## Required Package Contract

BodyWar may import these stable package surfaces:

- `createDrizzleAuthRepositories`
- `authAccessControlSchema`
- `authenticateRequestUseCase`
- `authorizeRequestUseCase`
- `logoutUseCase`
- `seedSystemBootstrap`
- `createHmacTokenCodec`
- `createPbkdf2PasswordService`
- principal/session/token/grant repository and domain types

BodyWar needs one new shared auth package use case before clean OAuth
integration:

`createTrustedSessionUseCase`

Inputs:

- `principalId`
- `ttlSeconds` optional
- `metadata` optional
- repositories, token codec, clock, id generator, config, telemetry

Behavior:

1. Load the active principal by id.
2. Resolve effective permissions from role grants, direct permissions, and
   principal grants.
3. Create an active auth session.
4. Issue an access token through the same token lifecycle as login.
5. Return session id, token id, access token, expiry, principal id, and
   permissions.

Non-goals:

- It does not exchange OAuth codes.
- It does not create browser cookies.
- It does not store provider tokens.
- It does not create UI profile read models.

## BodyWar Data Model

BodyWar owns these PostgreSQL tables through its own Drizzle schema and
generated migrations:

| Table | Purpose |
| --- | --- |
| `body_war_runner_profiles` | BodyWar display name and profile preferences keyed by auth principal id. |
| `body_war_oauth_states` | Single-use Strava OAuth state, nonce, expiry, redirect target, and consumed timestamp. |
| `body_war_provider_accounts` | Principal-to-provider identity link, public provider user id, display name, scope, status, linked timestamps. |
| `body_war_provider_tokens` | Server-side encrypted provider access/refresh token custody and expiry metadata. |

`auth_principals`, `auth_sessions`, `auth_access_tokens`, and
`auth_permission_grants` stay owned by the auth package schema and migrations.

## Browser Session Contract

BodyWar wraps the package bearer token flow into server-owned cookies:

- `bw_session`: HttpOnly session cookie containing or referencing the package
  access token.
- `bw_csrf`: non-HttpOnly CSRF value bound to the session.
- Unsafe methods require matching `x-csrf-token` and allowed `Origin`.
- Production cookies are `Secure`, `HttpOnly` where applicable, and
  `SameSite=Lax`.
- Logout calls the auth package logout use case and clears cookies.

The adapter must never expose access tokens to JavaScript, response JSON, logs,
or tracked validation receipts.

## Strava OAuth Contract

1. `GET /api/auth/strava/start` creates an OAuth state row, sets a state cookie,
   and redirects to Strava with required scopes.
2. `GET /api/auth/strava/callback` validates state, exchanges code
   server-side, stores provider tokens encrypted, upserts provider account and
   runner profile, then creates a trusted auth session through the package.
3. `GET /api/status` returns configuration and connection state only.
4. `GET /api/profile` returns profile projection and safe Strava profile URL.
5. `GET /api/activities` returns redacted activity summaries only after session
   and provider account checks.

## Permission Model

Initial BodyWar permission keys:

- `body-war.profile.read`
- `body-war.activity.read`
- `body-war.submission.create`
- `body-war.auth.disconnect`
- `body-war.operator.read`
- `body-war.operator.review`

Initial roles:

- `runner`: profile, activity, submission, disconnect.
- `operator`: runner permissions plus operator read/review.

## Security Invariants

- OAuth state is single-use and expires.
- Provider tokens are encrypted or otherwise protected server-side.
- Provider tokens and OAuth codes never appear in browser payloads.
- Strava profile link derives only from public provider user id.
- Activity summaries omit maps, notes, raw private payloads, and tokens.
- Friend activity evidence requires explicit consent before tracked receipts.
- Imported activity does not imply verified Taquaral geometry or scoring.
- SQL schema setup uses generated migrations, not hand-written duplicate schema
  SQL.

## Acceptance Criteria

Local integration is acceptable when:

1. `npm --prefix projects/body-war/app run check` passes.
2. BodyWar imports only exported auth package APIs.
3. BodyWar has Drizzle Kit config, generated migrations, and a migration
   application path for auth plus BodyWar-owned tables.
4. Tests prove session cookie creation, CSRF rejection, logout, profile read,
   safe Strava profile link, and no token leakage.
5. A local E2E test can simulate Strava callback without real Strava secrets.
6. Production deploy remains blocked unless operator decisions and private
   credentials are supplied.

## Upstream Patch Requests

Existing BodyWar docs should be updated in a later documentation SWU:

- `interfaces.md` should not say the auth package owns Strava provider logic.
- `ARCHITECTURE.md` should say the auth package owns core auth and BodyWar owns
  browser/OAuth/provider adapters.
- `app/README.md` should replace the claim that auth-user-management owns
  session guards, CSRF checks, provider links, and Strava token custody.
