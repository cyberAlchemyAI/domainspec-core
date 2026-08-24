---
deployment_id: agent-orchestration-copy-20260822T183440Z
deployed_at: 2026-08-22T18:34:40Z
scope: agent-orchestration-guide
result: pass
authority_effect: bounded-public-route-update
---

# Agent Orchestration Copy Deployment Receipt

## Outcome

The revised learner-facing guide is deployed at:

- `https://cyberalchemize.com/agent-orchestration`
- `https://cyberalchemize.com/agent-orchestration-guide`

Both routes returned HTTP 200 and the exact local HTML bytes:

- Source: `ops/development/2026-08-13-agent-orchestration-beginner-guide/guided-class.html`
- SHA-256: `a8bd3398aa6a8e6f72717ac019895287ddc1dde6285f27d140df58925d6fd3cf`
- Size: 115829 bytes

## Deployment Validation

Deployment controls:

- Script: `projects/co-op-engine/infra/deploy-static-vps.sh`, SHA-256 `64c924dfe8f76d48a47aa1ebfd34f04384514a185d134d9adc2623432232cb2b`.
- Nginx config: `projects/co-op-engine/infra/nginx.conf`, SHA-256 `62d842bf0052ad4020ea95ffa7cbce2a4da6ae8ebf7068969a673cc5360c6639`.
- Compose config: `projects/co-op-engine/infra/docker-compose.yml`, SHA-256 `c3022b1cb3eddae1879d21b8b5e78143dbe7b6b5c1d8fe1e66056d1dbf6f1e07`.
- Shell syntax, scoped whitespace, and local digest preflight: pass.
- `DEPLOY_SCOPE=agent-orchestration-guide DRY_RUN=1 .../deploy-static-vps.sh`: pass.
- `DEPLOY_SCOPE=agent-orchestration-guide .../deploy-static-vps.sh`: pass.
- Candidate Nginx syntax and worker readability: pass.
- Exact public digest and 115829-byte size on both routes: pass.
- Existing `/`, `/craft`, and `/bella` public bytes: preserved.
- Anonymous `/domainspec` access: HTTP 401.

The independent response-header check observed HTTP/2 200, `text/html`, a
deny-by-default content security policy, `X-Content-Type-Options: nosniff`,
`X-Frame-Options: DENY`, a restrictive permissions policy, and the configured
referrer policy on both guide routes.

The deploy script created exact rollback snapshots before switching:
`site.previous`, `docker-compose.yml.previous`, `nginx.conf.previous`,
`.env.previous`, and `.domainspec.htpasswd.previous` under the isolated
`/srv/co-op-engine` deployment directory.

## Public Browser Evidence

- Runtime: Playwright 1.59.1 with Chrome for Testing 147.0.7727.15, installed revision 1217.
- Chromium executable SHA-256: `696170a79640ec5b50c7518140ace06c69a49cfb295bf527d4a85e26a12b89a7`.
- Viewports: 390 by 844 and 1280 by 900.
- Public response: HTTP 200 at the clean `/agent-orchestration` URL.
- Page title: `Agent orchestration: from prompt to proof`.
- Revised Route 1 context heading: `Two messy requests, one deciding difference`.
- Seven of seven lesson transitions exposed exactly one active lesson.
- Eleven learner questions were present.
- Every lesson had document width equal to viewport width at both viewports; no page-wide horizontal overflow was observed.
- Console errors: none. Page errors: none.
- Reload request inventory: only `https://cyberalchemize.com/agent-orchestration`; no third-party request was observed.

The CLI's first browser attempts did not run product assertions because the
default system Chrome path was absent and a Windows-mounted temporary directory
could not host the Unix control socket. The terminal run used the already
approved shared Chromium executable and `/tmp`; it completed all checks above.

## Claim Ceiling

This receipt establishes exact-byte deployment, bounded route preservation,
and the browser observations above. It does not establish human comprehension,
intended-reader success, semantic truth, authorization for agent execution,
canonical Arcanum documentation status, or production readiness.

No commit or push was performed. The scoped release did not include unrelated
dirty-worktree bytes. The separate local Whisper skill changes were not part of
this static-site deployment.
