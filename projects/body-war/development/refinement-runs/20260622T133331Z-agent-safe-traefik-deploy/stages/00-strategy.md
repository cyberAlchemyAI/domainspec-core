---
id: stage-00-strategy
status: pass
---

# Stage 00 - Strategy Synthesis

## Selected Deployment Model

Use a restricted-command, server-owned-secret deployment model.

Agents should not SSH into the VPS as a normal Docker-capable user. A normal
Docker-capable shell can inspect container environment and recover secrets. The
deploy interface should instead be:

```text
agent -> ssh deploy alias "deploy <image-tag>"
server forced-command wrapper -> validates tag -> reads root-owned .env -> runs compose/migrate/up -> prints redacted status
```

## Why This Wins

- Reuses the existing Hostinger VPS, Docker, and Traefik.
- Removes Caddy from the first deploy path.
- Keeps secrets in one private server location.
- Keeps Postgres Docker-provided, private, and volume-backed on the same VPS.
- Lets agents perform routine deploys with only an image tag.
- Avoids CI setup before the first online receipt.
- Preserves a future path to GitHub Actions by reusing the same remote deploy
  wrapper.

## Core Rule

Secret-blind is not just "do not paste secrets into chat." If an agent has a
normal shell with Docker access, it can inspect secrets. The real invariant is
to give agents a restricted deploy command, not general server authority.
