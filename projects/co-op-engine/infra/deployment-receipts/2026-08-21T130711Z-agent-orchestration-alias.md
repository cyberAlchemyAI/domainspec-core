# Agent orchestration short-route deployment receipt

- Date: `2026-08-21T13:07:11Z`
- Operator: Codex, under direct user deployment instruction
- Requested route: `https://cyberalchemize.com/agent-orchestration`
- Retained route: `https://cyberalchemize.com/agent-orchestration-guide`
- Access: public HTTPS
- Source: `ops/development/2026-08-13-agent-orchestration-beginner-guide/guided-class.html`
- Remote source file: `/srv/co-op-engine/site/agent-orchestration-guide/index.html`
- Remote directory: `/srv/co-op-engine`
- Container: `coop-engine-site`
- Image ID: `sha256:65645c7bb6a0661892a8b03b89d0743208a18dd2f3f17a54ef4b76fb8e2f2a10`
- Deployment scope: `agent-orchestration-guide`
- Result: `pass`

## Applied route shape

The shorter route serves the existing reviewed guide file through an exact
Nginx location. It does not create a second content copy or replace the
original route.

- `/agent-orchestration` returns the guide with `200`.
- `/agent-orchestration/` redirects `308` to `/agent-orchestration`.
- `/agent-orchestration/index.html` redirects `308` to
  `/agent-orchestration`.
- An unknown child beneath the alias returns `404`.
- `/agent-orchestration-guide` remains available and byte-identical.

## Exact bytes

| Artifact | SHA-256 | Bytes |
| --- | --- | ---: |
| Local source, remote source file, and both live HTTPS responses | `59d38eff75024ea95028ed8b455e19a1cec9859e9735a035b58ea3f82db75446` | 101880 |
| Applied local and remote Nginx configuration | `62d842bf0052ad4020ea95ffa7cbce2a4da6ae8ebf7068969a673cc5360c6639` | 3936 |
| Hardened deployment script | `64c924dfe8f76d48a47aa1ebfd34f04384514a185d134d9adc2623432232cb2b` | 33490 |
| Deployment README | `41b18b5bfd45c04ba6823de760cbf0a5c905cffedb9126c1f6daf93aab4784e6` | 5075 |

## Deployment checks

| Check | Result | Evidence |
| --- | --- | --- |
| Pre-deployment baseline | pass | Requested alias returned `404`; retained route returned `200` with source digest `59d38e...5446` |
| Shell and whitespace validation | pass | `sh -n` and scoped `git diff --check` returned zero |
| Fail-closed dry run | pass | Scoped dry run completed before remote mutation |
| Preserved-site candidate | pass | Candidate cloned the active `site`; only the selected guide subtree could be overlaid; every other file was compared byte-for-byte |
| Candidate Nginx | pass | `nginx:1.27-alpine -t` passed before the switch |
| Rollback preparation | pass | Complete site, Compose, Nginx, environment, and verifier snapshots were prepared before switching |
| Container health | pass | Existing container recreated without image or Traefik changes; `/healthz` and both in-container guide routes passed |
| Requested route | pass | `200`, `text/html`, exact source digest |
| Retained route | pass | `200`, exact source digest |
| Alias variants | pass | Slash and `index.html` variants return `308` to the clean alias; unknown child returns `404` |
| Existing public routes | pass | Deployment validator rehashed `/`, `/craft`, and `/bella` against their pre-switch responses |
| DomainSpec boundary | pass | Anonymous and wrong-credential checks remained `401`; challenge and security headers remained present |
| Remote infrastructure | pass | Compose `c3022b...1e07`, environment `a3283a...a2fa`, verifier `aa6d1c...8d7a`, and image ID remained unchanged |

## Mobile browser acceptance

The requested route was opened in Chromium through the repository-approved
shared Playwright `1.59.1` runtime using the `iPhone 13` device profile.

| Check | Result |
| --- | --- |
| Navigation | `200`; final URL remained the requested clean alias |
| Document | Expected title and `h1`; viewport meta present; main content and 47 buttons rendered |
| Viewport | `390px` inner, client, document, and body width; no horizontal overflow |
| Network | One request, same origin; no external requests |
| Runtime | Zero console warnings/errors and zero page errors |
| Visual inspection | Mobile layout rendered legibly with controls contained inside the viewport |

Screenshot:
`output/playwright/agent-orchestration-mobile.FTudPx/mobile.png`
(`038387c90ce1bd80a4ce5c621867a1bfa10006b037a12ca4fea5a4589d31a733`,
2323485 bytes).

## Boundaries

- This release exposes the previously reviewed guided-class HTML under the
  requested shorter route. It does not apply the blocked authoring candidate
  or resolve `WP-AOG-THREE-MOMENT-V1` / `SWU-AOG-005`.
- It is a public learning prototype, not canonical documentation, production
  readiness evidence, or proof of human comprehension.
- No commit or push was requested or performed.
