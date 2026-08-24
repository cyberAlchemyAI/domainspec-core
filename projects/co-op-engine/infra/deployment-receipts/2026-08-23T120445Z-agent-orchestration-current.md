---
deployment_id: agent-orchestration-current-20260823T120445Z
deployed_at: 2026-08-23T12:04:45Z
scope: agent-orchestration-guide
result: pass
authority_effect: bounded-public-route-update
---

# Agent Orchestration Current-Version Deployment Receipt

## Outcome

The exact current learner-facing guide is deployed at:

- `https://cyberalchemize.com/agent-orchestration`
- `https://cyberalchemize.com/agent-orchestration-guide`

Both routes returned HTTP 200 and the exact source bytes:

- Source: `ops/development/2026-08-13-agent-orchestration-beginner-guide/guided-class.html`
- SHA-256: `5cd904111381062b4793b7ec416605fa5eb3d994188a237f08e91323a0ca2217`
- Size: 107216 bytes

## Source Validation

The exact local file passed a Playwright 1.59.1 browser run with the shared Chromium revision 1217 at 390 by 844 and 1280 by 900:

- title: `Agent orchestration with Lantern and Priya: from prompt to proof`;
- two arrow route controls;
- seven lessons and eleven questions;
- forward and backward traversal reached the exact `Lesson 1 of 7` through `Lesson 7 of 7` states;
- exactly one lesson was visible at every route transition;
- document width equaled viewport width at both viewports;
- console errors: zero;
- page errors: zero; and
- HTTP requests from the local file: zero.

Chromium executable SHA-256: `696170a79640ec5b50c7518140ace06c69a49cfb295bf527d4a85e26a12b89a7`.

## Bounded Deployment Route

The repository's current uncommitted deployment controls still include a newer protected-review route that is absent from the active server. They were not deployed:

- local deployment script: `24f37c6b61b525cea27f07b253f9535cba78a12081acc2e4470261a62ae3839f`;
- local Nginx config: `7c2b419b6f75b4719173661e99fcdd990a83963cf283cdd1a8f8fc426d635594`; and
- local Compose config: `894d2e8d2b75251ab6dd5e54d4f9ec6192b1324f391c6f6ac2d831d25815627f`.

A temporary compatibility transaction was derived outside the repository and pinned to the active remote controls:

- temporary script SHA-256: `d67b2e23e37855802538c9a53ad307894f4ad7b6117cb45a731bd4c06e317da6`;
- temporary script size: 52239 bytes;
- active remote Nginx SHA-256: `62d842bf0052ad4020ea95ffa7cbce2a4da6ae8ebf7068969a673cc5360c6639`;
- active remote Compose SHA-256: `c3022b1cb3eddae1879d21b8b5e78143dbe7b6b5c1d8fe1e66056d1dbf6f1e07`;
- shell syntax: pass;
- scoped whitespace: pass;
- ShellCheck: unavailable in the local environment and therefore not claimed; and
- `DEPLOY_SCOPE=agent-orchestration-guide DRY_RUN=1`: pass.

The compatibility transaction uploaded only a one-file guide overlay. It neither uploaded nor changed Nginx, Compose, environment, password-verifier, image, Traefik, TLS, or protected-route controls.

## Deployment Validation

- Candidate contained one regular guide file with mode 0644 under a mode 0755 directory.
- Candidate digest matched the declared source digest.
- The active Nginx and Compose hashes were rechecked before candidate validation, rollback snapshot creation, switch, and post-switch container checks.
- Every non-guide site file compared byte-identical between the active generation and the candidate.
- Existing remote Nginx syntax passed in an isolated networkless container.
- An exact whole-site rollback snapshot was created as `/srv/co-op-engine/site.previous`.
- The rollback guide retains the prior SHA-256 `904956c5e014f9e75f487a2d5bef95647b6388568ef42239dac5c770cd8745da`.
- The existing static container was recreated without changing its image, Compose file, Nginx file, or Traefik labels.
- Container health and both in-container guide routes passed.
- Independent post-deploy comparison confirmed every non-guide byte remained unchanged.
- Both public guide routes returned 107216 bytes with the exact source digest.
- Existing `/`, `/craft`, and `/bella` public digest checks passed.
- Anonymous `/domainspec/` access remained HTTP 401.
- Public guide response checks retained HTML content type, restrictive content security policy, `nosniff`, frame denial, restrictive permissions policy, and no-cache behavior.

## Public Browser Evidence

The exact public alias route passed Playwright 1.59.1 at 390 by 844 and 1280 by 900:

- HTTP 200;
- exact title and Lantern/Priya introduction;
- two route arrows, seven lessons, and eleven questions;
- all seven route transitions with one active lesson at a time;
- no page-wide horizontal overflow;
- console errors: zero;
- page errors: zero; and
- request inventory: only `https://cyberalchemize.com/agent-orchestration`.

## Claim Ceiling

This receipt establishes exact-byte deployment, bounded preservation, rollback availability, and the browser observations above. It does not establish human comprehension, teaching effectiveness, semantic truth, authorization for agent execution, canonical Arcanum documentation status, or production readiness.

No commit or push was performed. The pending Refine strategy was not executed, and the guide source was not modified during deployment.
