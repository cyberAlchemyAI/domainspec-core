---
id: 20260622T133331Z-agent-safe-traefik-deploy
sigil: refine
status: strategy-proposal
target: projects/body-war
createdAt: 2026-06-22T13:33:31Z
---

# Run Manifest

## Objective

Refine the simplest safe deployment route for TROQAR on an existing Hostinger
VPS where SSH, Docker, and Traefik already exist, while allowing agents to
deploy without receiving or inspecting production secrets.

## Inputs

- Operator update: Hostinger VPS already has SSH, Docker, and Traefik.
- Existing app: `projects/body-war/app`.
- Existing infra: `projects/body-war/infra/docker-compose.prod.yml`,
  `projects/body-war/infra/SECRET-INVENTORY.md`,
  `projects/body-war/docs/INFRA-ARCHITECTURE.md`.
- Prior blocker: `projects/body-war/docs/decisions/vps-deployment-readiness.md`.

## Artifacts

| Artifact | Status |
| --- | --- |
| `REFINE-SEED-PROPOSAL.md` | pass |
| `REFINE-DISPATCH.json` | pass-json |
| `RUNTIME-HANDOFF.md` | strategy-only |
| `RESULT.md` | pass |
| `evidence-index.json` | pass-json |
| `stages/00-strategy.md` | pass |

## Research Decision

`no-research`: local repository evidence and operator-supplied VPS/Traefik
context are sufficient for the next non-executed plan. External provider docs
are not needed until implementation.

## Execution Boundary

No deployment was executed. No secrets were requested, read, printed, copied, or
validated.
