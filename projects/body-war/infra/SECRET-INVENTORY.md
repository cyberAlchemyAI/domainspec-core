# Secret Inventory

Status: `draft-task-session`
Scope: Body War/TROQAR Single VPS existing-host runtime

This inventory lists required runtime values. It does not contain real secret
values.

## Public Or Non-Secret Configuration

| Name | Purpose | Example |
| --- | --- | --- |
| `BODY_WAR_DOMAIN` | Canonical public host for the app. | `troqar.example.com` |
| `BODY_WAR_TLS_EMAIL` | ACME contact for Caddy. | `ops@example.com` |
| `BODY_WAR_APP_IMAGE` | App image repository. | `ghcr.io/domainspec/body-war-app` |
| `IMAGE_TAG` | App image tag. | `latest` |
| `BODY_WAR_PUBLIC_BASE_URL` | Public origin for same-origin and OAuth alignment. | `https://troqar.example.com` |
| `BODY_WAR_ALLOWED_ORIGINS` | Comma-separated origins accepted for unsafe browser requests. | `https://troqar.example.com` |
| `BODY_WAR_SECURE_COOKIES` | Enables Secure cookie flag in deployed mode. | `1` |
| `STRAVA_REDIRECT_URI` | Strava callback URL. | `https://troqar.example.com/api/auth/strava/callback` |
| `POSTGRES_USER` | Database user. | `body_war` |
| `POSTGRES_DB` | Database name. | `body_war` |

## Secret Values

| Name | Purpose | Storage Rule |
| --- | --- | --- |
| `BODY_WAR_SESSION_SECRET` | HMAC signing secret for session and CSRF cookies. | Generate privately; never commit. |
| `STRAVA_CLIENT_ID` | Strava OAuth client id. | Keep in private VPS/CI env. |
| `STRAVA_CLIENT_SECRET` | Strava OAuth client secret. | Keep in private VPS/CI env; never log. |
| `POSTGRES_PASSWORD` | Database password. | Generate privately; never commit. |

## Server-Owned Private Runtime State

These are not environment secrets, but they must not be tracked or exposed:

- Strava access tokens.
- Strava refresh tokens.
- OAuth authorization codes.
- OAuth state records.
- Session records.
- Raw private athlete payloads.
- Friend activity evidence before consent and redaction.

## Tracking Rules

- `projects/body-war/infra/.env` is ignored.
- `projects/body-war/app/.env` is ignored.
- `projects/body-war/app/data/*.json` is ignored except `.gitkeep`.
- Deployment receipts must redact tokens, secrets, OAuth codes, and raw private
  athlete payloads before they enter tracked artifacts.

## Current Flag

The current app has a JSON local-pilot auth store. Production token custody is
not complete until the Postgres auth/profile/provider adapter work-pack lands.
