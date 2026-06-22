# S06 Invoke Design - Online Identity Loop

Status: `pass`
Capability: `invoke design`
Input: `stages/S05-DISTILL.md`

## Context View

Actors and systems:

- Runner uses browser UI.
- Body War app serves static UI and `/api/*` routes from TypeScript Node.
- `auth-user-management` owns browser sessions, CSRF checks, Strava OAuth, and
  provider-token custody contracts.
- PostgreSQL stores users, sessions, provider accounts, provider tokens, profile
  read models, and import receipts.
- Caddy terminates TLS and routes the canonical HTTPS origin to the app.
- Strava provides OAuth and activity summary data.
- Operator controls VPS deployment and receives deployment receipts.
- Friend activity is protected validation evidence only after consent.

## High-Level View

```text
Browser
  -> Caddy HTTPS
    -> Body War TypeScript app
      -> auth-user-management
      -> PostgreSQL
      -> Strava API

Operator
  -> deploy receipt
  -> health/login/connect/profile/activity validation
```

The default route shape is same-origin:

- `/` static app shell
- `/api/status`
- `/api/auth/strava/start`
- `/api/auth/strava/callback`
- `/api/auth/logout`
- `/api/profile`
- `/api/activities`

## Low-Level Component View

| Component | Responsibility |
| --- | --- |
| `BrowserSessionGuard` | Read and verify HttpOnly signed session cookie, enforce CSRF on unsafe requests, reject invalid origins. |
| `StravaOAuthAdapter` | Generate single-use OAuth state, exchange callback code, persist provider account and tokens server-side. |
| `RunnerProfileService` | Build minimal profile read model from principal, provider account, privacy settings, and Strava link. |
| `ActivitySummaryService` | Fetch and store redacted Strava activity summaries without exposing provider tokens. |
| `AuthStorePostgresAdapter` | Production store for sessions, users, provider accounts, provider tokens, OAuth states, and audit/import receipts. |
| `DeploymentHealth` | Expose `/api/status` and smoke-testable readiness for app plus database. |
| `InfraPack` | Compose services for app, postgres, and caddy; optional monitoring after L0 health is proven. |

## Workflow View

Login/session:

1. Runner opens app over HTTPS.
2. App sets or verifies a signed HttpOnly session cookie.
3. Unsafe requests require readable CSRF cookie plus matching header.
4. Logout revokes the server-side session and clears cookies.

Strava connect:

1. Runner starts Strava OAuth.
2. Server creates single-use OAuth state bound to session.
3. Strava callback exchanges code server-side.
4. Server stores provider account metadata and tokens in PostgreSQL.
5. Browser receives no tokens.

Profile:

1. Runner visits `/profile`.
2. UI calls `/api/profile`.
3. Server returns public-safe profile state and Strava connection/link.
4. UI shows privacy state and connection status.

Activity summaries:

1. Runner requests activities.
2. Server refreshes token when needed.
3. Server imports redacted summaries.
4. UI shows summaries without private raw payloads.

Deployment receipt:

1. Deploy app, postgres, and caddy to VPS.
2. Confirm HTTPS and status endpoint.
3. Perform login/session smoke.
4. Perform Strava connect/callback smoke.
5. Confirm profile and Strava link.
6. Confirm activity summary import.
7. Run secret/log redaction check.

## Decision Flow

| Question | Default |
| --- | --- |
| Single origin or split API host? | Single origin until domain/DNS requires otherwise. |
| Existing VPS or provisioned droplet? | Existing VPS first. |
| JSON store or Postgres? | JSON only for local pilot; Postgres for online. |
| Prometheus/Grafana in L0? | Defer unless setup is already available. |
| Friend activity in test data? | No, not until consent and redacted receipt. |
| Route geometry claim? | No, explicitly deferred. |

## Dependency Interface

Inputs required from implementation:

- `BODY_WAR_PUBLIC_BASE_URL`
- `BODY_WAR_SESSION_SECRET`
- `STRAVA_CLIENT_ID`
- `STRAVA_CLIENT_SECRET`
- `STRAVA_REDIRECT_URI`
- database URL or equivalent Postgres connection settings
- production cookie/security flags

Outputs required for governance:

- deployment receipt,
- auth/profile smoke result,
- Strava connect smoke result,
- redacted activity import receipt,
- secret scan result,
- gap status update for route/game deferrals.

## Handoff

Proceed to refine-design-review with emphasis on production store, domain/DNS,
friend consent, and deployment proof.
