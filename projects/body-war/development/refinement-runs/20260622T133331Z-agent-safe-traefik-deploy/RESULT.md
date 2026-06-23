---
id: refine-result-agent-safe-traefik-deploy
status: pass
target: projects/body-war
---

# Refine Result - Agent-Safe Traefik Deploy

## Final Synthesis

The simplest safe deployment route is not Caddy-in-Compose. It is a
Traefik-attached app Compose stack plus a restricted deploy command on the VPS.
Postgres should also be provided by Docker Compose in that same app stack, not
as an external managed database.

Agents should deploy by image tag only. The VPS should own `.env`, registry
auth, Traefik, Postgres volumes, migrations, and deploy receipts. The agent
should only be able to trigger a validated server-side script and read redacted
health output.

## Recommended Architecture

```text
Hostinger VPS
  Traefik already running
  /srv/troqar/
    compose.yml              # non-secret app + postgres stack
    .env                     # root/deploy owned, mode 600, never printed
    postgres_data            # Docker volume, not exposed publicly
    receipts/                # redacted deploy receipts only
  /usr/local/bin/troqar-deploy-agent
    validates image tag
    checks .env exists without reading it to stdout
    docker compose pull
    docker compose up -d postgres
    docker compose run --rm app node dist/src/infrastructure/postgres/migrate-cli.js
    docker compose up -d app
    curls /api/status
```

## Traefik Compose Shape

The next Task Session should replace or fork `infra/docker-compose.prod.yml`
into a Traefik shape:

```yaml
services:
  app:
    image: ${BODY_WAR_APP_IMAGE}:${IMAGE_TAG}
    environment:
      NODE_ENV: production
      BODY_WAR_AUTH_BACKEND: postgres
      BODY_WAR_HOST: 0.0.0.0
      BODY_WAR_PORT: "5174"
      BODY_WAR_PUBLIC_BASE_URL: ${BODY_WAR_PUBLIC_BASE_URL}
      BODY_WAR_ALLOWED_ORIGINS: ${BODY_WAR_ALLOWED_ORIGINS}
      BODY_WAR_SECURE_COOKIES: "1"
      BODY_WAR_SESSION_SECRET: ${BODY_WAR_SESSION_SECRET}
      BODY_WAR_TOKEN_PROTECTION_SECRET: ${BODY_WAR_TOKEN_PROTECTION_SECRET}
      STRAVA_CLIENT_ID: ${STRAVA_CLIENT_ID}
      STRAVA_CLIENT_SECRET: ${STRAVA_CLIENT_SECRET}
      STRAVA_REDIRECT_URI: ${STRAVA_REDIRECT_URI}
      DATABASE_URL: postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}
    labels:
      - traefik.enable=true
      - traefik.http.routers.troqar.rule=Host(`${BODY_WAR_DOMAIN}`)
      - traefik.http.routers.troqar.entrypoints=websecure
      - traefik.http.routers.troqar.tls=true
      - traefik.http.routers.troqar.tls.certresolver=${TRAEFIK_CERT_RESOLVER}
      - traefik.http.services.troqar.loadbalancer.server.port=5174
    networks:
      - troqar_internal
      - traefik

  postgres:
    image: postgres:15-alpine
    restart: unless-stopped
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - troqar_internal

volumes:
  postgres_data:

networks:
  troqar_internal:
    internal: true
  traefik:
    external: true
    name: ${TRAEFIK_NETWORK}
```

## Secret-Blind Deploy Contract

1. Human/trusted setup creates `/srv/troqar/.env`.
2. `.env` is owned by root or a trusted deploy owner and mode `600`.
3. The agent deploy key does not get a general shell.
4. The agent deploy key is forced to run only `troqar-deploy-agent`.
5. The deploy command accepts only an image tag matching a strict regex.
6. The wrapper never runs `set -x`, never prints env, and never runs
   `docker compose config` with the real `.env`.
7. Receipts redact domains if needed and always redact tokens/secrets/codes.

## Minimal Next Work Pack

| SWU | Purpose | Output |
| --- | --- | --- |
| `SWU-BW-DEPLOY-TRAEFIK-001` | Replace Caddy deploy path with Traefik Compose and placeholder env. | `infra/docker-compose.traefik.yml`, `.env.example`, docs |
| `SWU-BW-DEPLOY-AGENT-002` | Add restricted deploy scripts. | `infra/scripts/deploy-agent.sh`, `infra/scripts/deploy-local.sh` |
| `SWU-BW-DEPLOY-RECEIPT-003` | Add redacted deploy receipt template and checks. | `infra/deployment-receipts/TEMPLATE.md`, smoke script |
| `SWU-BW-DEPLOY-DOCS-004` | Update VPS decision gate and infra architecture. | docs synchronized |

## Remaining Human Decisions

- Public domain/subdomain.
- Traefik network name and cert resolver on the VPS.
- Whether app image is public or private registry with server-side `docker login`.
- Real Strava callback configured to `https://<domain>/api/auth/strava/callback`.
- Whether first activity validation uses the operator account or friend consent.

## Recommended Next Route

Run `task-session` on `SWU-BW-DEPLOY-TRAEFIK-001` through
`SWU-BW-DEPLOY-DOCS-004`. Do not deploy yet; first implement the harness, then
run a second task session for the actual VPS deployment receipt.
