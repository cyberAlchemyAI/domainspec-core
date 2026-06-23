---
project: body-war
product-name: TROQAR
status: task-session-pass
preset: single-vps-existing-host
vps-provider: existing-vps
dns-provider: tbd
iac-tool: docker-compose-first
container-registry: configurable
ci-cd: manual-first
created: 2026-06-21
updated: 2026-06-21
source-run: 20260621T045622Z-task-bwo-001-infra-shape
---

# Infrastructure Architecture Constitution

> Governing document for the first online Body War/TROQAR runtime.
> This document defines the infrastructure shape. It is not a deployment
> receipt and does not claim production readiness by itself.

## Preset

Current: `single-vps-existing-host`

The immediate path uses an already available VPS and a small Docker Compose
stack. This adapts the DomainSpec `single-vps` preset without requiring cloud
provisioning or Pulumi before the first online identity loop is useful.

| Preset | Runtime | IaC | Monitoring | Deploy |
| --- | --- | --- | --- | --- |
| Dev | local Node/TypeScript app | none | app status only | `npm start` |
| Single VPS existing host | Docker Compose on available VPS | shell/manual first | app, Traefik, and Postgres health | copy config and `docker compose up -d` |
| Single VPS managed | Docker Compose on provisioned VPS | Pulumi TypeScript | Prometheus/Grafana optional | GitHub Actions or scripted deploy |
| Split/HA | later | later | later | later |

## Stack

| Layer | Choice | Notes |
| --- | --- | --- |
| VPS provider | existing VPS | Operator has an available VPS; provider details are not required for the first infra definition. |
| DNS provider | tbd | Required before production Strava callback and TLS smoke. |
| IaC | Docker Compose first; Pulumi TypeScript later | Keep the first deploy small, then promote to managed infra once the online loop works. |
| Reverse proxy | Existing Traefik | Public HTTPS entrypoint and same-origin routing to the TypeScript app on the Hostinger VPS. |
| App runtime | TypeScript Node server | Current app starts with `npm --prefix projects/body-war/app start` after build. |
| App image | configurable container image | `BODY_WAR_APP_IMAGE` and `IMAGE_TAG` select the deployed image. |
| Database | PostgreSQL 15 | Included for auth package sessions/principals plus Body War profile/provider state. Migrations are Drizzle Kit generated. |
| Monitoring | health/logs first | Prometheus/Grafana are L1 after SLOs and deploy receipt exist. |
| CI/CD | manual first | GitHub Actions can be added after the first deployment receipt. |

## Environments

| Environment | Purpose | URL | Deploy Trigger |
| --- | --- | --- | --- |
| local | development and smoke | `http://127.0.0.1:5174` | `npm --prefix projects/body-war/app start` |
| production | first online identity loop | `https://<BODY_WAR_DOMAIN>` | manual VPS compose deploy |

## Runtime Services

| Service | Internal Port | Exposed | Role |
| --- | --- | --- | --- |
| `app` | `5174` | via Traefik only | TypeScript static UI and `/api/*` server. |
| `postgres` | `5432` | no | Auth package sessions/principals plus Body War provider accounts, provider tokens, OAuth state, and runner profiles. |
| `traefik` | existing VPS service | yes | TLS and reverse proxy; not owned by this app Compose stack. |

For L0, the app Compose stack owns `app + postgres`; the existing VPS Traefik
service owns ingress. Monitoring services are deferred until the app has a
deployment receipt and feature SLOs.

## Networking

Public ingress:

- TCP `80` for HTTP to HTTPS redirect and ACME.
- TCP `443` for HTTPS.
- SSH only through the VPS operator's accepted key path.

Private-only:

- PostgreSQL stays on the Docker network.
- App port `5174` is not published directly.
- Future metrics ports stay private unless protected through Traefik auth.

Default route model:

- `https://<BODY_WAR_DOMAIN>/` -> app static UI
- `https://<BODY_WAR_DOMAIN>/api/*` -> app API
- `https://<BODY_WAR_DOMAIN>/api/status` -> health/status smoke
- `https://<BODY_WAR_DOMAIN>/api/auth/strava/callback` -> Strava redirect URI

## Secrets

Tracked files may contain only names, descriptions, and placeholders. Real
values belong in the VPS environment, a private deploy secret store, or a later
CI secret store.

| Secret | Purpose | Tracked Status |
| --- | --- | --- |
| `BODY_WAR_DOMAIN` | Canonical public host. | placeholder only |
| `BODY_WAR_SESSION_SECRET` | HMAC signing for session and CSRF cookies. | secret value never committed |
| `STRAVA_CLIENT_ID` | Strava OAuth app id. | placeholder only |
| `STRAVA_CLIENT_SECRET` | Strava OAuth app secret. | secret value never committed |
| `STRAVA_REDIRECT_URI` | Production callback URL. | derived from public domain |
| `POSTGRES_USER` | Database user. | non-secret default allowed |
| `POSTGRES_PASSWORD` | Database password. | secret value never committed |
| `POSTGRES_DB` | Database name. | non-secret default allowed |
| `DATABASE_URL` | App database connection string. | generated inside compose from DB values |
| `BODY_WAR_APP_IMAGE` | Container image repository. | non-secret |
| `IMAGE_TAG` | App image tag. | non-secret |
| `BODY_WAR_AUTH_BACKEND` | Selects memory or Postgres auth backend. | non-secret |
| `BODY_WAR_TOKEN_PROTECTION_SECRET` | Encrypts provider token ciphertext at rest. | secret value never committed |
| `TRAEFIK_NETWORK` | Existing external Traefik Docker network. | non-secret |
| `TRAEFIK_CERT_RESOLVER` | Existing Traefik TLS resolver. | non-secret |

The current app supports `BODY_WAR_AUTH_BACKEND=memory` for local fake-Strava
development and `BODY_WAR_AUTH_BACKEND=postgres` for the local production-shape
path. Public online readiness still requires a VPS/DNS/real-Strava deployment
receipt, but the app no longer depends on a JSON auth store for the hosted
auth/profile/provider shape.

## Infrastructure Layout

```text
projects/body-war/
  docs/
    INFRA-ARCHITECTURE.md
  infra/
    Caddyfile              # legacy/non-Hostinger Caddy path
    docker-compose.prod.yml # legacy/non-Hostinger Caddy path
    docker-compose.traefik.yml
    .env.traefik.example
    scripts/
    .env.example
    .gitignore
    SECRET-INVENTORY.md
  app/
    server.ts
    static/
```

Future managed Single VPS artifacts can add:

```text
projects/body-war/infra/
  Pulumi.yaml
  Pulumi.production.yaml
  index.ts
  cloud-init.yaml
  prometheus.yml
  grafana/
  alerts/
```

## Deployment Flow

L0 manual compose on existing Hostinger Traefik:

1. Build and publish a Body War app image.
2. Copy `infra/docker-compose.traefik.yml` and a private `.env` file to the VPS.
3. Set DNS for `BODY_WAR_DOMAIN` to the VPS public IP.
4. Set the Strava app callback to
   `https://<BODY_WAR_DOMAIN>/api/auth/strava/callback`.
5. Run migrations and `docker compose --env-file .env -f docker-compose.traefik.yml up -d`.
6. Record a deployment receipt with health, login, connect, profile, activity,
   CSRF, and secret-redaction checks.

## Validation Gates

| Gate | Required Evidence |
| --- | --- |
| Compose shape | `docker compose --env-file projects/body-war/infra/.env.traefik.example -f projects/body-war/infra/docker-compose.traefik.yml config` passes. |
| Language invariant | `bash tools/check-runtime-language-policy.sh` passes. |
| Health | `https://<BODY_WAR_DOMAIN>/api/status` returns 200 through Traefik/TLS. |
| Session | Login creates server-owned cookies with HttpOnly, Secure, SameSite, and CSRF binding. |
| Strava connect | OAuth callback succeeds with the configured production redirect URI. |
| Profile link | `/profile` shows a safe Strava athlete link and no tokens. |
| Activity import | Summaries are redacted and do not include raw private activity payloads. |
| Secret redaction | Logs, receipts, and tracked artifacts contain no real tokens, secrets, codes, or private athlete payloads. |
| Geometry caveat | Imported Strava activity does not claim verified Taquaral route geometry or score. |

## Open Flags

| Flag | Why It Remains |
| --- | --- |
| `GAP-BODY-WAR-DOMAIN-001` | The canonical public domain is not selected. |
| `GAP-BODY-WAR-DEPLOYED-AUTH-RECEIPT-001` | Local Postgres auth/profile/provider flow exists, but no VPS/DNS/real-Strava hosted receipt exists yet. |
| `GAP-BODY-WAR-VPS-DEPLOYMENT-RECEIPT-001` | The VPS exists but no deploy/health/login/connect receipt exists yet. |
| `GAP-BODY-WAR-FRIEND-CONSENT-RECEIPT-001` | The friend's activity needs explicit consent before validation use. |
| `GAP-BODY-WAR-OBSERVABILITY-SCOPE-001` | Prometheus/Grafana are not part of L0 until SLOs exist. |

## Conventions

- Use TypeScript for app, auth, database adapter, and Pulumi code.
- Use shell scripts for deployment and validation commands when scripts are
  needed.
- Keep app/API same-origin unless a later decision explicitly splits hosts.
- Never expose PostgreSQL directly to the internet.
- Never commit `.env`, real secrets, Strava tokens, OAuth codes, or raw private
  activity payloads.
- Treat poker-team as infrastructure evidence, not a source of Body War product
  names, domains, roles, or secrets.
- Do not claim production readiness until deployment receipts exist.
