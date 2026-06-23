---
id: runtime-handoff-agent-safe-traefik-deploy
status: blocked-awaiting-confirmation
target: projects/body-war
---

# Runtime Handoff

## Runtime Objective

After confirmation, execute a Task Session that implements a deploy harness for
the existing Hostinger VPS with Docker and Traefik.

## Permission State

No runtime deploy permission is implied by this refine packet.

## Required Operator-Private Inputs

These must be installed on the VPS by the operator or a trusted human path, not
given to the agent:

- `/srv/troqar/.env` with production secrets.
- Strava app client id and client secret.
- Postgres password.
- `BODY_WAR_SESSION_SECRET`.
- `BODY_WAR_TOKEN_PROTECTION_SECRET`.
- Any private registry login if the image is not public.

## Agent-Visible Inputs

- SSH target alias, if already configured and safe to use.
- Image tag to deploy.
- Domain name after DNS is selected.
- Traefik Docker network name, if not the default chosen in the repo.

## Blocked Runtime Actions

- Do not cat, copy, print, or validate real `.env` contents.
- Do not run `docker compose config` against a real `.env`, because it can
  render secrets into output.
- Do not grant agents general Docker socket access if the goal is actual
  secret non-disclosure.
