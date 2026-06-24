---
project: body-war
product-name: TROQAR
status: operator-manual
updatedAt: 2026-06-23
---

# TROQAR Online Deploy Manual

This manual is for the first Hostinger VPS deployment using the Docker and
Traefik instance that already exist on the server.

The repository provides deployable artifacts, but the real secrets stay on the
VPS. Agents should not receive, print, copy, or commit production secrets.

## What You Need

- A domain or subdomain, for example `troqar.example.com`.
- DNS `A` record pointing that host to the Hostinger VPS public IP.
- The Traefik certificate resolver name on the VPS.
- A Strava API application.

## 1. Easy Direct VPS Deploy

The simplest path copies a small source bundle to the VPS, creates
`/srv/troqar/.env` if it does not exist, builds the Docker image on the VPS, runs
Drizzle-generated migrations, and starts the app plus Postgres.

Edit the connection lines at the top of:

```sh
projects/body-war/infra/scripts/simple-vps-deploy.sh
```

Typical edits:

```sh
SSH_CMD="ssh root@your-vps-ip"
SCP_CMD="scp"
REMOTE_COPY_TARGET="root@your-vps-ip:/srv/troqar"
BODY_WAR_DOMAIN="troqar.example.com"
BODY_WAR_EDGE_NETWORK="troqar_edge"
TRAEFIK_CERT_RESOLVER="letsencrypt"
```

Run from the repository root:

```sh
projects/body-war/infra/scripts/simple-vps-deploy.sh
```

On the first run, the script uploads the deploy files and creates
`/srv/troqar/.env`, then stops if placeholders remain.

Edit the env file on the VPS:

```sh
ssh root@your-vps-ip "nano /srv/troqar/.env"
```

Generate private values on the VPS:

```sh
openssl rand -hex 32
```

Then rerun:

```sh
projects/body-war/infra/scripts/simple-vps-deploy.sh
```

The second run builds and starts the stack directly on the VPS.

## 2. Configure `/srv/troqar/.env`

Replace every `CHANGE_ME` value in `/srv/troqar/.env`.

Required public values:

```sh
BODY_WAR_DOMAIN=troqar.example.com
BODY_WAR_APP_IMAGE=troqar-body-war-app
BODY_WAR_PUBLIC_BASE_URL=https://troqar.example.com
BODY_WAR_ALLOWED_ORIGINS=https://troqar.example.com
STRAVA_REDIRECT_URI=https://troqar.example.com/api/auth/strava/callback
BODY_WAR_EDGE_NETWORK=troqar_edge
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

Lock the env file:

```sh
chmod 600 /srv/troqar/.env
```

Do not run `docker compose config` with the real `.env` in a shared transcript;
it can print secrets.

## 3. Configure Strava

In the Strava API app settings, set the Authorization Callback Domain to the
domain only:

```text
troqar.example.com
```

Do not include `https://` and do not include `/api/auth/strava/callback` in the
Strava dashboard field. The app still sends the full redirect URI during OAuth:

```text
https://troqar.example.com/api/auth/strava/callback
```

Use the same host as `BODY_WAR_DOMAIN`. For example, if the app env uses
`BODY_WAR_DOMAIN=troqarapp.com`, the Strava dashboard callback domain must be
`troqarapp.com`, not `www.troqarapp.com`.

## 4. Smoke Test

From your machine after deploy:

```sh
projects/body-war/infra/scripts/smoke-online.sh https://troqar.example.com
```

Expected:

- `/api/status` returns 200.
- `/` contains `Bora correr`.
- the first page does not render token-like secret terms.

## 5. Test Strava Login

Open:

```text
https://troqar.example.com
```

Click `Entrar com Strava`, approve access, and confirm:

- callback returns to TROQAR,
- the profile renders,
- the Strava public profile link opens,
- no token values appear on the page.

## Optional Registry Deploy

Use this path later if you want CI to publish an image and the VPS to pull it.

### 1. Build And Push The Image

Run from the repository root:

```sh
projects/body-war/infra/scripts/build-image.sh 20260622T000000Z ghcr.io/domainspec/body-war-app
docker push ghcr.io/domainspec/body-war-app:20260622T000000Z
```

Use any image repository the VPS can pull. If it is private, log in to the
registry on the VPS as a trusted human/operator. Do not give registry secrets to
the deploy agent.

### 2. Copy Public Deploy Files To The VPS

On the VPS, use `/srv/troqar`:

```sh
sudo mkdir -p /srv/troqar/receipts
sudo cp docker-compose.traefik.yml /srv/troqar/docker-compose.traefik.yml
sudo cp .env.traefik.example /srv/troqar/.env
```

The files to copy from this repo are:

- `projects/body-war/infra/docker-compose.traefik.yml`
- `projects/body-war/infra/.env.traefik.example`

### 3. Configure `/srv/troqar/.env`

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

### 4. Run The First Manual Deploy

From `/srv/troqar` on the VPS:

```sh
IMAGE_TAG=20260622T000000Z docker compose --env-file .env -f docker-compose.traefik.yml pull app
IMAGE_TAG=20260622T000000Z docker compose --env-file .env -f docker-compose.traefik.yml up -d postgres
IMAGE_TAG=20260622T000000Z docker compose --env-file .env -f docker-compose.traefik.yml run --rm app node dist/src/infrastructure/postgres/migrate-cli.js
IMAGE_TAG=20260622T000000Z docker compose --env-file .env -f docker-compose.traefik.yml up -d app
```

Do not run `docker compose config` with the real `.env` in a shared transcript;
it can print secrets.

### 5. Optional Restricted Agent Deploy

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
- Traefik entrypoint and certificate resolver names.

The app image only needs external registry availability if you choose the
optional registry deploy path.
