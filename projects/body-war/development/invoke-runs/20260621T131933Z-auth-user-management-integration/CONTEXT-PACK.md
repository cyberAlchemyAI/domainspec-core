# Context Pack - BodyWar Auth Integration

Session evidence for an Invoke define/design/plan pass targeting BodyWar/TROQAR
integration with `@domainspec/auth-user-management`.

## Objective

Specify and design the implementation path for BodyWar to consume the reusable
auth package while keeping TROQAR-owned browser session, Strava OAuth, profile,
and activity routes inside the BodyWar app boundary.

## Selected Sources

| Source | Why Included |
| --- | --- |
| `projects/body-war/docs/features/troqar-product-architecture/SPEC.md` | App-wide capability map and cross-feature dependency on auth. |
| `projects/body-war/docs/features/troqar-product-architecture/ARCHITECTURE.md` | Existing six-view TROQAR design and auth dependency decision. |
| `projects/body-war/docs/features/troqar-product-architecture/ONLINE-AUTH-PROFILE-INFRA.md` | Immediate online priority: login, profile, Strava link, VPS, privacy, validation. |
| `projects/body-war/docs/INFRA-ARCHITECTURE.md` | Single-VPS, TypeScript app, PostgreSQL, Caddy, secret, and validation gates. |
| `projects/body-war/docs/decisions/vps-deployment-readiness.md` | Operator-level blockers for public origin, VPS access, Strava credentials, and friend activity. |
| `projects/body-war/app/server.ts` | Current TypeScript app integration attempt and route/API surface. |
| `projects/body-war/app/tests/auth-consumer.test.ts` | Existing expected auth/session/profile behaviors. |
| `projects/auth-user-management/README.md` | Reusable package boundary: core auth behavior, not HTTP/cookies/OAuth/UI. |
| `projects/auth-user-management/docs/ADOPTION.md` | Consumer responsibilities and Drizzle migration ownership. |
| `projects/auth-user-management/src/index.ts` | Current public package exports. |
| `projects/auth-user-management/src/application/auth-access-control/` | Stable use cases for login, token issue, authenticate, authorize, logout, introspection, catalog, bootstrap. |
| `projects/auth-user-management/src/infrastructure/drizzle-postgres/` | PostgreSQL Drizzle repositories and generated migration schema. |
| `implementation/domainspec/architecture/pattern-library/SQL-PERSISTENCE.md` | SQL persistence obligation: Drizzle ORM plus Drizzle Kit generated migrations. |

## Current Evidence

`npm --prefix projects/body-war/app run check` currently fails because
`server.ts` and tests import auth package members that are not exported by the
current package:

- `DEFAULT_STRAVA_SCOPE`
- `allow`
- `createBrowserSessionGuard`
- `createJsonAuthStore`
- `createPrincipal`
- `createStravaProviderAdapter`
- `parseCookieHeader`
- several HTTP/browser/OAuth types

This means the integration cannot proceed by preserving the current BodyWar
imports. The implementation plan must first repair the contract boundary.

## Governing Constraints

- Runtime code must be TypeScript.
- Shell is orchestration only.
- PostgreSQL persistence must use Drizzle ORM and Drizzle Kit generated
  migrations.
- `@domainspec/auth-user-management` remains reusable and must not absorb
  BodyWar product pages, HTTP routing, browser copy, or Strava-specific UI.
- BodyWar owns Strava OAuth, browser cookies, CSRF, provider token custody,
  profile projection, activity import, and TROQAR UI routes.
- Token, OAuth code, provider payload, and friend activity evidence must never
  enter tracked artifacts unredacted.
- Deployment to the real VPS remains blocked until operator decisions in
  `vps-deployment-readiness.md` are resolved.

## Authority Correction

Some existing BodyWar docs and previous task-session receipts say the auth
package owns session guards, CSRF checks, provider links, and Strava token
custody. The current reusable package boundary says otherwise. This Invoke run
treats live package source plus `docs/ADOPTION.md` as the authority and records
an upstream BodyWar doc patch request rather than silently mutating existing
product architecture documents.

## Assumptions

- BodyWar can add local adapter modules around the auth package instead of
  requiring all browser/OAuth helpers to live in the shared package.
- A small reusable auth package extension for "trusted session from existing
  principal" is acceptable because OAuth consumers need to create sessions after
  provider identity proof without password login.
- BodyWar can add its own Drizzle schema and migrations for runner profile,
  OAuth state, provider account, and provider token custody.
- The first executable unit should be local compile and E2E validation, not VPS
  deployment.

## Blockers Preserved

- `GAP-BODY-WAR-DOMAIN-001`: canonical public domain not selected.
- `GAP-BODY-WAR-VPS-DEPLOYMENT-RECEIPT-001`: no deploy/health/login/connect
  receipt.
- `GAP-BODY-WAR-FRIEND-CONSENT-RECEIPT-001`: friend activity requires consent.
- Real Strava production credentials and callback changes remain private
  operator actions.
