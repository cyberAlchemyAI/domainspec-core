---
project: body-war
product-name: TROQAR
status: operator-manual
updatedAt: 2026-06-22
---

# TROQAR Online Deploy Manual

This manual is for the first Hostinger VPS deployment using the Docker and
Traefik instance that already exist on the server.

The repository provides deployable artifacts, but the real secrets stay on the
VPS. Agents should not receive, print, copy, or commit production secrets.

## What You Need

- A domain or subdomain, for example `troqar.example.com`.
- DNS `A` record pointing that host to the Hostinger VPS public IP.
- The Traefik external Docker network name on the VPS.
- The Traefik certificate resolver name on the VPS.
- A Strava API application.
- A Docker image for the app, published or available to the VPS.

## 1. Build And Push The Image

Run from the repository root:

```sh
projects/body-war/infra/scripts/build-image.sh 20260622T000000Z ghcr.io/domainspec/body-war-app
docker push ghcr.io/domainspec/body-war-app:20260622T000000Z
```

Use any image repository the VPS can pull. If it is private, log in to the
registry on the VPS as a trusted human/operator. Do not give registry secrets to
the deploy agent.

## 2. Copy Public Deploy Files To The VPS

On the VPS, use `/srv/troqar`:

```sh
sudo mkdir -p /srv/troqar/receipts
sudo cp docker-compose.traefik.yml /srv/troqar/docker-compose.traefik.yml
sudo cp .env.traefik.example /srv/troqar/.env
```

The files to copy from this repo are:

- `projects/body-war/infra/docker-compose.traefik.yml`
- `projects/body-war/infra/.env.traefik.example`

## 3. Configure `/srv/troqar/.env`

Edit `/srv/troqar/.env` on the VPS. Replace every placeholder.

Required public values:

```sh
BODY_WAR_DOMAIN=troqar.example.com
BODY_WAR_APP_IMAGE=ghcr.io/domainspec/body-war-app
IMAGE_TAG=20260622T000000Z
BODY_WAR_PUBLIC_BASE_URL=https://troqar.example.com
BODY_WAR_ALLOWED_ORIGINS=https://troqar.example.com
STRAVA_REDIRECT_URI=https://troqar.example.com/api/auth/strava/callback
TRAEFIK_NETWORK=traefik
TRAEFIK_ENTRYPOINT=websecure
TRAEFIK_CERT_RESOLVER=letsencrypt
```

Required private values:

```sh
BODY_WAR_SESSION_SECRET=<generate privately>
BODY_WAR_TOKEN_PROTECTION_SECRET=<generate privately>
STRAVA_CLIENT_ID=<from Strava>
STRAVA_CLIENT_SECRET=<from Strava>
POSTGRES_PASSWORD=<generate privately>
```

Generate secrets on the VPS:

```sh
openssl rand -hex 32
```

Lock the env file:

```sh
sudo chown root:root /srv/troqar/.env
sudo chmod 600 /srv/troqar/.env
```

If you later install the restricted deploy command for a non-root deploy user,
either run the wrapper through a controlled `sudo` rule or change ownership to a
trusted deploy group with mode `640`. The command must be able to read `.env`,
but the agent must not get a general shell that can print it.

## 4. Configure Strava

In the Strava API app settings, set the callback URL to:

```text
https://troqar.example.com/api/auth/strava/callback
```

Use the same host as `BODY_WAR_DOMAIN`.

## 5. Run The First Manual Deploy

From `/srv/troqar` on the VPS:

```sh
IMAGE_TAG=20260622T000000Z docker compose --env-file .env -f docker-compose.traefik.yml pull app
IMAGE_TAG=20260622T000000Z docker compose --env-file .env -f docker-compose.traefik.yml up -d postgres
IMAGE_TAG=20260622T000000Z docker compose --env-file .env -f docker-compose.traefik.yml run --rm app node dist/src/infrastructure/postgres/migrate-cli.js
IMAGE_TAG=20260622T000000Z docker compose --env-file .env -f docker-compose.traefik.yml up -d app
```

Do not run `docker compose config` with the real `.env` in a shared transcript;
it can print secrets.

## 6. Smoke Test

From your machine or the VPS:

```sh
projects/body-war/infra/scripts/smoke-online.sh https://troqar.example.com
```

Expected:

- `/api/status` returns 200.
- `/` contains `Bora correr`.
- the first page does not render token-like secret terms.

## 7. Test Strava Login

Open:

```text
https://troqar.example.com
```

Click `Entrar com Strava`, approve access, and confirm:

- callback returns to TROQAR,
- the profile renders,
- the Strava public profile link opens,
- no token values appear on the page.

## 8. Optional Restricted Agent Deploy

Only after the manual deploy works, install:

```sh
sudo cp deploy-agent.sh /usr/local/bin/troqar-deploy-agent
sudo chmod 755 /usr/local/bin/troqar-deploy-agent
```

The agent command should accept only an image tag:

```sh
troqar-deploy-agent 20260622T000000Z
```

For true secret-blind deploys, the SSH key used by agents should be restricted
to this command. Do not give that key a normal shell with Docker access.

## Current Blocker

Online testing is blocked until you configure:

- DNS for the selected host,
- `/srv/troqar/.env`,
- Strava callback URL,
- Traefik network and resolver names,
- app image availability on the VPS.
