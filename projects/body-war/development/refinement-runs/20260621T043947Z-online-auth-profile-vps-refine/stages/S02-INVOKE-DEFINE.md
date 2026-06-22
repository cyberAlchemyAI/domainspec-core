# S02 Invoke Define - Online Identity Loop

Status: `pass`
Capability: `invoke define`
Input: `stages/S01-CONTEXT-BUILDER.md`

## Definition

The refined feature is the Body War/TROQAR Online Identity Loop:

> A VPS-hosted TypeScript web app where a runner can open the app over HTTPS,
> establish a browser session, connect Strava, view a minimal runner profile,
> open the connected Strava profile link, and review token-safe activity
> summaries.

This loop intentionally excludes track geometry, game scoring, rankings,
economy, operator control surfaces, and public social mechanics.

## Domain Terms

| Term | Definition |
| --- | --- |
| `OnlinePreviewInstance` | The first deployed Body War/TROQAR runtime on the available VPS, reachable through one canonical HTTPS origin. |
| `RunnerPrincipal` | The authenticated user represented by a server-side session and user record. |
| `RunnerProfile` | Minimal user-facing profile read model containing display identity, Strava connection status, Strava profile link when available, and privacy state. |
| `BrowserSession` | HttpOnly signed cookie session with SameSite and Secure production flags plus CSRF binding for unsafe requests. |
| `ProviderAccount` | Server-side record linking a runner principal to Strava athlete identity and public account metadata. |
| `ProviderTokenCustody` | Server-only storage and refresh of Strava access and refresh tokens; tokens never enter browser payloads, logs, or artifacts. |
| `StravaProfileLink` | Safe outbound link to the connected Strava athlete page, derived from public provider account identity where available. |
| `FriendActivityValidationFixture` | A consented, redacted Taquaral Strava activity import used only to prove import mechanics and not to claim route authority. |
| `DeploymentReceipt` | Evidence that the online instance passed health, auth, Strava connect, profile, activity, and secret-redaction checks. |

## Runtime Boundary

Included for L0:

- HTTPS web app on VPS.
- Browser session login/logout.
- Strava OAuth start/callback.
- Minimal profile endpoint and profile page.
- Strava connection status and profile link.
- Redacted activity summary import/list.
- Health endpoint and deployment smoke receipt.

Deferred:

- Track geometry and map claim authority.
- Route submissions and route validation.
- Scoring, proof-of-run, challenges, leaderboards, and economy.
- Operator/admin pages beyond basic deployment visibility.
- Prometheus/Grafana unless the VPS setup cost is low enough to include after health checks pass.

## Adopted Infra Definitions

| Definition | Refined Use |
| --- | --- |
| DomainSpec Single VPS preset | Primary deployment shape for L0. |
| Existing VPS variant | Use the user's available VPS before adding cloud provider provisioning. |
| Caddy reverse proxy | TLS and same-origin routing for app/API. |
| PostgreSQL | Durable online auth/profile/provider state. |
| Docker Compose | Service packaging for app, postgres, and caddy. |
| Health-first observability | `/api/status`, logs, and deploy smoke before heavier monitoring. |
| Runtime evidence substrate | Deployment receipts, smoke results, secret scans, and consent receipts are first-class artifacts. |

## Decisions Made By Refine

- Same-origin `/api/*` is the default unless a domain decision requires split hosts.
- `projects/auth-user-management/` is the reusable auth package to adopt rather
  than copying poker-team implementation files wholesale.
- poker-team infra is a structural reference for compose/Caddy/Pulumi/security,
  not a source of product-specific code.
- Production token custody requires PostgreSQL or an equivalent server-side
  durable store before public online validation.
- The first deployment plan should not wait for track/game surfaces.

## Open Decisions

| Decision | Required Before |
| --- | --- |
| Public domain and canonical app origin. | Strava production redirect URI and Caddy config. |
| Existing VPS access model and deploy user. | Deployment automation. |
| Store implementation path for `auth-user-management`. | Production Strava token custody. |
| Friend consent and redaction receipt. | Real Taquaral activity validation. |
| Monitoring depth for L0. | Prometheus/Grafana inclusion. |

## Handoff

Proceed to refine-review interrogation with special attention to consent,
production token custody, and no premature route authority claims.
