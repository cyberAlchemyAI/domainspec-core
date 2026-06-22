# Online Auth/Profile Infra Slice

Status: `draft-refine-seed`
Owner scope: `projects/body-war`
Source packet: `troqar-product-architecture`

## Operator Update

The next priority is to make TROQAR available online with login, a minimal user
profile, Strava connection, and a safe link to the connected athlete's Strava
profile page. A friend has a Parque Taquaral run in Strava and a VPS is
available for hosting.

This changes the immediate implementation priority from broad game mechanics to
an online identity and provider-link slice:

1. Deploy a production-like app to the VPS.
2. Support server-owned browser login/session.
3. Show a minimal authenticated profile.
4. Connect Strava and display provider connection status.
5. Link to the connected athlete's Strava profile page when a provider user id
   is available.
6. Import redacted activity summaries for validation.
7. Use the friend's Taquaral activity as consented validation evidence.

Track geometry, territory scoring, clans, economy, and public leaderboard claims
remain downstream.

## L0 Capability Boundary

| Capability | Included In L0 | Deferred |
| --- | --- | --- |
| `CAP-AUTH` | Browser session, logout, Strava OAuth, consent/privacy copy, CSRF. | Multi-provider account settings. |
| `CAP-ACTIVITY` | Recent Strava activity summaries, redacted fields only. | Private map/polyline import, deep analytics. |
| `CAP-SCORE` | Minimal profile shell with placeholders for XP/league. | Real XP, season, badges, streak computation. |
| `CAP-EVIDENCE` | Use one friend's Taquaral activity as token-safe validation evidence. | Public verified submissions and operator adjudication. |
| `CAP-TRACK` | Keep Taquaral as pilot context and label geometry status. | Source-backed route geometry and map claims. |

## Page Boundary

| Route | Status | L0 Job |
| --- | --- | --- |
| `/` | included | Public online home/status shell with connect/profile entrypoints. |
| `/connect` | included | Start Strava OAuth and show consent/provider status. |
| `/profile` | included | Show runner identity, session state, connected Strava account, Strava profile link, and recent activity summary entrypoint. |
| `/profile/privacy` | included | Show consent, scope, retention, and disconnect/logout actions. |
| `/activities` | included if time permits | Show redacted recent activity summaries after Strava connection. |
| `/operator` | deferred | Review and verification after the online identity slice is stable. |
| `/map`, `/routes`, `/challenges`, `/community`, `/rankings`, `/store`, `/sponsor` | deferred | Keep design-defined, not L0 implementation blockers. |

## Domain Definitions

| Term | Definition | Source |
| --- | --- | --- |
| Online preview instance | The deployed VPS-hosted runtime reachable through HTTPS and backed by server-side session/token custody. | DomainSpec infra template; poker-team single-VPS stack. |
| Runner principal | A Body War application identity that owns sessions and permissions. It is distinct from Strava athlete identity. | poker-team `Principal`; auth-user-management `Principal`. |
| Runner profile | Minimal read model for authenticated user state: principal id, display name, provider connection, Strava profile URL, and validation readiness. | TROQAR UI `/profile`; Body War profile table. |
| Provider account | Server-side link between a runner principal and a Strava athlete id, scope, display name, and public metadata. | Body War Strava adapter backed by Drizzle. |
| Provider token custody | Server-side storage of Strava access/refresh tokens; tokens never return to browser clients or tracked artifacts. | Body War token table with encrypted ciphertext. |
| Strava profile link | A UI-safe link derived from `providerUserId`, such as `https://www.strava.com/athletes/{providerUserId}`. It is display data, not an auth credential. | L0 product requirement. |
| Friend activity validation fixture | A consented Strava activity from a friend that can prove the online connect/import path. It does not by itself close geometry or public verification claims. | Operator update; existing blocker closure conditions. |

## Infrastructure Definitions

| Definition | L0 Choice | Notes |
| --- | --- | --- |
| Preset | `single-vps-existing-host` | Adapt DomainSpec `single-vps`; use the available VPS instead of requiring new provisioning first. |
| Runtime | Docker Compose on VPS | Mirrors poker-team single-VPS runtime. |
| Reverse proxy | Caddy | Auto-TLS and one public HTTPS entrypoint. |
| Public origin | One canonical HTTPS app origin | Prefer same-origin `/api/*` for L0 to reduce CORS/CSRF complexity. |
| App service | TypeScript Node server | Existing Body War `server.ts` serves static UI and API. |
| Database | PostgreSQL for online runtime | Auth package migrations own core auth tables; Body War migrations own provider/profile tables. |
| Secrets | Server or deployment-secret store | `BODY_WAR_SESSION_SECRET`, `STRAVA_CLIENT_ID`, `STRAVA_CLIENT_SECRET`, `STRAVA_REDIRECT_URI`, `DATABASE_URL`, and public base URL. |
| Firewall | Expose 80/443 and SSH only | Database, metrics, and internal service ports stay private. |
| Observability | Health endpoint first; Prometheus/Grafana optional L0+ | Poker-team stack supplies the later pattern. |
| Deployment receipt | Health check plus login/connect smoke result | Runtime evidence cannot become promotion authority without recorded validation. |

## Suggested Compose Shape

```text
services:
  app       TypeScript Body War server, static UI, /api/*
  postgres  server-side sessions, provider accounts, provider tokens, profiles
  caddy     HTTPS reverse proxy
  prometheus optional after health/observability specs exist
  grafana    optional after Prometheus is useful
```

For L0, `app + postgres + caddy` is enough if health checks and logs are
present. Prometheus/Grafana can be added from poker-team once SLOs and
observability specs exist.

## Security Invariants

- Session cookie is HttpOnly, signed, `SameSite=Lax`, and `Secure` in
  production.
- Unsafe browser methods require CSRF cookie/header binding and allowed-origin
  checks.
- Strava OAuth state is single-use and expires.
- Strava access and refresh tokens are server-side only.
- Strava activity summaries are redacted and omit maps, notes, and raw private
  metadata.
- The profile may display a Strava profile URL but must not expose provider
  tokens, OAuth codes, or private athlete payloads.
- The friend's activity requires explicit consent before it is used as
  validation evidence.
- A Taquaral activity import does not imply sourced route geometry.

## Validation Surface

| Validation | Required Before Online Claim |
| --- | --- |
| VPS health | `https://<domain>/api/health` returns 200 through Caddy/TLS. |
| Session | Login creates server-owned session and cookies with production flags. |
| CSRF | Unsafe API requests fail without matching CSRF binding. |
| Strava connect | OAuth start/callback succeeds with configured production callback URL. |
| Profile | `/profile` shows application identity plus Strava connection status. |
| Strava link | Profile link points to Strava athlete page and contains no tokens. |
| Activity import | Friend's consenting Taquaral run appears as a redacted summary. |
| Secret scan | Logs and tracked artifacts contain no tokens, secrets, codes, or raw private activity payloads. |
| Geometry caveat | UI does not claim verified route geometry from one imported activity. |

## Open Decisions

| Decision | Why It Matters | Suggested Default |
| --- | --- | --- |
| Domain name | Required for Strava production callback and Caddy TLS. | Use the eventual TROQAR domain or a stable subdomain. |
| Deployment method | Existing VPS can be manual compose now or IaC-managed later. | Manual compose for first L0, then Pulumi/GitHub Actions hardening. |
| Deployed auth receipt | Local Postgres/fake-Strava flow is production-shaped, but not a hosted receipt. | Deploy to VPS with DNS and real Strava callback, then record health/login/connect evidence. |
| Monitoring scope | Full Grafana stack may be overkill for L0. | Health endpoint plus logs first; Prometheus after SLO docs. |
| Friend consent artifact | Needed to turn the friend's activity into validation evidence. | Record a private local consent receipt outside tracked public docs if sensitive. |
