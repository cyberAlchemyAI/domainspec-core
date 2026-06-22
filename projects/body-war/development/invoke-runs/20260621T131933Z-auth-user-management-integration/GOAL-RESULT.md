# Goal Result - BodyWar Auth Integration

Status: `complete-local`
Completed: `20260621T150516Z`
Source work-pack: `WORK-PACK.md`
Executed stream: `SWU-BWAUTH-001` through `SWU-BWAUTH-007`

## Outcome

The BodyWar local auth integration is implemented and verified for the
production-shaped local path:

- `@domainspec/auth-user-management` now exposes generic trusted-session
  creation for consumers that already proved an external identity.
- BodyWar owns browser cookies, CSRF/origin checks, Strava OAuth/provider
  behavior, provider token custody, runner profiles, profile responses,
  logout, activity redaction, and fake-Strava local testing.
- PostgreSQL uses Drizzle ORM plus Drizzle Kit generated migrations. BodyWar
  migrations contain only BodyWar profile/provider tables; auth package
  migrations are applied from the package.
- Docker E2E starts Postgres, applies auth and BodyWar migrations, runs the
  fake-Strava login/profile/activity/submission/logout flow, and tears down the
  container.
- Docs now state the package/BodyWar ownership split and do not claim live VPS
  deployment, real Strava callback readiness, Taquaral geometry proof, or
  friend activity consent.

## SWU Receipt

| SWU | Result | Receipt |
| --- | --- | --- |
| `SWU-BWAUTH-001` | complete | Added `createTrustedSessionUseCase`, exports, tests, and package validation. |
| `SWU-BWAUTH-002` | complete | Added BodyWar Drizzle schema, generated migrations, and TypeScript migration runner applying package then app SQL. |
| `SWU-BWAUTH-003` | complete | Replaced broken package imports with BodyWar-owned browser session adapter, cookies, CSRF, origin checks, and auth error mapping. |
| `SWU-BWAUTH-004` | complete | Added BodyWar-owned Strava OAuth adapter with fake gateway, OAuth state, protected token storage, provider account/profile upserts, and trusted-session bridge. |
| `SWU-BWAUTH-005` | complete | Wired status, profile, activities, logout, and submissions through the new adapters with token redaction and geometry caveat behavior. |
| `SWU-BWAUTH-006` | complete | Added Docker Compose Postgres E2E, TypeScript E2E program, `scripts/e2e.sh`, and `scripts/validate.sh`. |
| `SWU-BWAUTH-007` | complete | Synced app README, infra architecture, and TROQAR architecture docs with the corrected ownership and readiness boundary. |

## Verification

Passed:

- `npm --prefix projects/auth-user-management run check`
- `npm --prefix projects/auth-user-management run validate`
- `npm --prefix projects/body-war/app run db:generate`
- `npm --prefix projects/body-war/app run check`
- `npm --prefix projects/body-war/app run validate`
- `bash projects/body-war/app/scripts/e2e.sh all`
- `npm --prefix projects/body-war/app run e2e:all`
- `bash tools/check-runtime-language-policy.sh`
- `git diff --check -- projects/auth-user-management projects/body-war`
- duplicate auth schema probe over BodyWar app migrations/source/tests/E2E
- high-confidence secret pattern probe over touched auth, BodyWar app, and
  BodyWar docs artifacts
- stale ownership wording probe over app README, infra docs, and TROQAR product
  architecture docs

## Remaining Non-Local Blockers

These are intentionally outside this work-pack:

- VPS/DNS/public origin setup and live deployment receipt.
- Real Strava callback configuration and real Strava credentials.
- Friend consent/private activity evidence handling.
- Taquaral geometry/scoring authority.
- Production observability hardening beyond health/logs and local validation.
