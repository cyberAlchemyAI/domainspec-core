# Infra Definition Extraction

Status: `draft-pass`
Run: `20260621T043947Z-online-auth-profile-vps-refine`

## Input Sources

| Source | Extracted Use |
| --- | --- |
| `implementation/domainspec/templates/infra-architecture.md` | Presets, stack layers, environment table, secrets model, infra layout, networking, monitoring, CI/CD, scaling roadmap, and deployment conventions. |
| `implementation/domainspec/copilot/skills/domainspec-infra-deploy/SKILL.md` | Infra sync process, source contracts, generated targets, validation commands, Prometheus naming, and mutation constraints. |
| `ops/development/infra-spec-research-strategy.md` | Infra-spec candidate axes: runtime instance, state namespace, operational proof status, evidence substrate, residue, boundary object, validation gate, promotion status. |
| `validation/poker-team/docs/INFRA-ARCHITECTURE.md` | Concrete single-VPS implementation of the DomainSpec infra template. |
| `validation/poker-team/infra/docker-compose.prod.yml` | Production compose services, health checks, internal DB, Caddy, Prometheus, Grafana, and volumes. |
| `validation/poker-team/infra/Caddyfile` | HTTPS reverse-proxy pattern and Prometheus basic-auth pattern. |
| `validation/poker-team/infra/cloud-init.yaml` | VPS bootstrap: deploy user, Docker, firewall, disabled password auth, app directory. |
| `validation/poker-team/infra/index.ts` | Pulumi TypeScript model for VPS, firewall, DNS, and outputs. |
| `validation/poker-team/docs/features/auth-access-control/` | Principal, Session, AccessToken, PermissionGrant, AuthContext, login/logout/authenticate/authorize contracts. |
| `projects/auth-user-management/README.md` and `docs/ADOPTION.md` | Reusable browser session, CSRF, Strava provider, environment variables, token custody, and Body War consumer notes. |
| `projects/body-war/docs/features/troqar-product-architecture/` | TROQAR capabilities, UI routes, backend boundary, active gaps, and security requirements. |

## Definitions To Carry Into Body War

| Definition | Body War Meaning |
| --- | --- |
| `environment` | Local and production runtime boundaries with different URLs, secret handling, cookie flags, and validation gates. |
| `runtime_instance` | The deployed VPS process/container set corresponding to the Body War app spec. |
| `deployment_unit` | A deployable Docker Compose service such as `app`, `postgres`, or `caddy`. |
| `service_boundary` | The API/static app, database, reverse proxy, monitoring, and future worker boundaries. |
| `state_namespace` | Explicit split between source, runtime, generated, local, private, and evidence state. |
| `secret_boundary` | Values that must never enter git, logs, UI payloads, or public artifacts. |
| `provider_account` | Server-side link from Body War principal to Strava athlete identity. |
| `provider_token_custody` | Storage and refresh of Strava tokens only on the server. |
| `runner_profile` | Minimal authenticated read model combining app identity, provider connection, Strava profile link, and validation readiness. |
| `health_check` | A deploy proof that the app answers through the public HTTPS path and internal service checks. |
| `observability_signal` | Runtime metric/log/receipt that proves behavior without exposing private activity or secrets. |
| `deployment_receipt` | Evidence that build, deploy, health check, login, connect, and import smoke tests ran. |
| `infra_residue` | Anything that fails to cross cleanly from spec to deployed runtime, such as missing DNS, missing Postgres adapter, or unverified TLS/cookie flags. |
| `promotion_status` | Separate labels for specified, implemented, deployed, observed, validated, reflected, and promoted. |

## L0 Infra Candidate

The smallest useful online topology is:

```text
VPS
  caddy      public HTTPS, auto-TLS
  app        TypeScript Body War server, static UI, /api/*
  postgres   sessions, provider accounts, provider tokens, runner profiles
```

Prometheus/Grafana can be added from the poker-team pattern after Body War has
feature observability and SLO documents. For this L0, a health endpoint, server
logs, token-redaction checks, and smoke-test receipts are sufficient.

## Production-Readiness Gaps

| Gap | Why It Matters |
| --- | --- |
| `GAP-BODY-WAR-DOMAIN-001` | A stable public domain is required for Strava callback and Caddy TLS. |
| `GAP-BODY-WAR-POSTGRES-AUTH-STORE-001` | The current JSON auth store is local-pilot only; online sessions/provider tokens need a server-side DB adapter. |
| `GAP-BODY-WAR-VPS-DEPLOYMENT-RECEIPT-001` | A VPS exists, but deployment is not validated until health/login/connect/import receipts exist. |
| `GAP-BODY-WAR-FRIEND-CONSENT-RECEIPT-001` | The friend's activity can validate the flow only after consent is recorded privately and token-safely. |
| `GAP-BODY-WAR-OBSERVABILITY-SCOPE-001` | Health/logs may be enough for L0, but SLO/Prometheus scope is not yet selected. |
