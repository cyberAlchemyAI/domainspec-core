# Deployment Result — Co-Op Project Showcase

Status: pass

Public URL: `https://cyberalchemize.com/`

## Outcome

The accepted Co-Op project showcase is deployed as an isolated static Nginx
service on the VPS and Traefik edge pattern first established by Body War.
The apex previously returned 404; the deployment did not replace a live apex
application.

The deployment has its own:

- `/srv/co-op-engine` remote directory;
- `coop-engine-site` container;
- `coop-engine` Traefik router and service;
- public-only routing environment.

It shares only the existing `troqar_edge` network. It does not share or mutate
TROQAR or Time Capsule application directories, containers, routers,
databases, or environment files.

## Validation

- Source and downloaded HTML SHA-256 match.
- HTTP redirects to HTTPS and TLS verification passes.
- HTTPS returns 200 and the expected page title.
- All security headers are present after one recorded header-inheritance
  repair.
- Live Chromium checks pass for filters, Whisper disclosure, all twenty
  presentation stages, desktop/mobile overflow, console, and network.
- `time-capsule.cyberalchemize.com` remains HTTP 200 with its expected title.
- TROQAR root and `/api/status` remain HTTP 200; its app and database remain
  healthy without restart.

Detailed receipt:
`projects/co-op-engine/infra/deployment-receipts/2026-07-26T201929Z-live.md`.

Browser evidence:
`output/playwright/ux-validator/co-op-showcase-20260726/deployment/`.

## Claim boundary

Deployment establishes public reachability and the tested browser behavior
only. The page remains a public review prototype; human understanding,
recruitment outcome, current owner welcome, and production readiness remain
unproved.
