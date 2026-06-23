---
id: refine-seed-agent-safe-traefik-deploy
status: pass
target: projects/body-war
preset: compact
research: no-research
---

# Refine Seed Proposal

## Target

TROQAR/Body War deployment path for the first online auth/profile/Strava
preview.

## Operator Constraint

The VPS is already available on Hostinger, SSH is already configured, Docker is
already installed, and Traefik is already running. Agents should be able to
deploy the app without knowing production secrets.

## Refined Problem

The current infra shape assumes a self-contained Compose stack with Caddy. That
is no longer the shortest path. The shortest path is:

1. Reuse the existing Traefik ingress.
2. Keep production secrets server-owned on the VPS.
3. Give agents a restricted deployment interface that accepts only a safe image
   tag and runs a server-side deploy script.
4. Run Postgres from Docker Compose on the VPS, private on the app Compose
   network, with a persistent Docker volume.
5. Produce redacted deployment receipts after health/login/profile checks.

## Done Criteria

- Agents can trigger deploy by image tag or git-derived release id.
- Agents never receive, copy, cat, print, or commit `.env` values.
- Agent SSH cannot become a general shell with Docker inspect access.
- Traefik owns TLS and public routing.
- App uses Docker-provided Postgres-backed auth in production.
- Deploy receipt proves `/api/status`, login redirect, profile safety, CSRF
  behavior, and no secret leakage in tracked outputs.

## Write Scope For Next Task Session

- Add Traefik-specific Compose file or replace current Caddy production shape.
- Add shell deploy scripts with a restricted-command mode.
- Add `.env.example` updates for Traefik and Postgres auth.
- Add a deploy receipt template with redaction rules.
- Update infra docs and decision gate status from "blocked for unknown VPS" to
  "implementation-ready after domain/Strava values are installed privately".

## Non-Goals

- Do not handle real secret values.
- Do not deploy in the refinement run.
- Do not expose Postgres.
- Do not require Caddy.
- Do not add CI before the first manual/restricted deploy works.
