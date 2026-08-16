# Agent orchestration guided class deployment receipt

- Date: `2026-08-16T13:43:13Z`
- Operator: Codex, under direct user deployment instruction
- Route: `https://cyberalchemize.com/agent-orchestration-guide`
- Access: public HTTPS
- Source: `ops/development/2026-08-13-agent-orchestration-beginner-guide/guided-class.html`
- Remote target: `/srv/co-op-engine/site/agent-orchestration-guide/index.html`
- Remote directory: `/srv/co-op-engine`
- Container: `coop-engine-site`
- Image: `nginx:1.27-alpine`
- Image ID: `sha256:65645c7bb6a0661892a8b03b89d0743208a18dd2f3f17a54ef4b76fb8e2f2a10`
- Deployment scope: `agent-orchestration-guide`
- Result: `pass`

## Deployed bytes

| Artifact | SHA-256 |
| --- | --- |
| Local source, remote file, and live HTTPS response | `59d38eff75024ea95028ed8b455e19a1cec9859e9735a035b58ea3f82db75446` |
| Applied deployment script | `6cb61996b14b18051d63060f1fea3170f79d1181447648d9b07a496c285bed29` |
| Post-deployment hardened deployment script | `088db275174c50abb77dfbd93b903336aacd4fbadb22761dd69051313aaf9dcc` |
| Deployed and local Nginx configuration | `075ad3a424c383e4d245702a0da4da0ff053b6aad4613d40cd5363d478954f34` |
| Final deployment README | `3d50159b19871220eb53646395dcad8e3b5f550dd405fbbc43ef8fb8703e3446` |

The source was untracked at deployment time. This receipt therefore binds the
deployed bytes directly; it does not claim a source commit or publication.

## Routing shape

The existing Traefik router already owns the complete
`Host("cyberalchemize.com")` surface. Creating another host router would have
introduced overlapping route selection, so this release reused the current
router and added three exact Nginx locations:

- `/agent-orchestration-guide` serves the class index;
- `/agent-orchestration-guide/` redirects `308` to the canonical route;
- `/agent-orchestration-guide/index.html` redirects `308` to the canonical
  route.

The active container remained attached only to `troqar_edge`; its router rule,
entrypoint `websecure`, and TLS resolver `letsencrypt` remained unchanged.

## Deployment checks

| Check | Result | Evidence |
| --- | --- | --- |
| Public baseline | pass | Before the switch, `/`, `/craft`, and `/bella` returned `200`; the target and slash variant returned `404`; `/domainspec/` returned `401` |
| Read-only safety review | pass | One bounded helper independently found that no second Traefik router was needed, mapped the exact source and target, required remote-site preservation, and changed no files |
| Public-content boundary | pass | The self-contained page cites public Arcanum implementation paths, contains no remote assets or network bridge, and does not describe DomainSpec or Saturn as shipped |
| Dry run | pass | `DEPLOY_SCOPE=agent-orchestration-guide DRY_RUN=1 projects/co-op-engine/infra/deploy-static-vps.sh` completed before the live invocation |
| Staged payload | pass | The overlay contained exactly one regular file with mode `0644` beneath a `0755` directory and matched the source digest |
| Existing-site preservation | pass | The remote candidate began as `cp -a site site.next`; every file outside the selected route matched the active generation byte for byte before switching |
| Candidate configuration | pass | Existing Compose configuration passed; candidate Nginx syntax passed in `nginx:1.27-alpine`; UID/GID `101:101` could read the guide and the existing verifier |
| Rollback preparation | pass | A complete site copy and exact Compose, Nginx, environment, and verifier snapshots were verified before the active paths changed |
| Container health | pass | The same `coop-engine-site` service was recreated without an image pull; `/healthz` returned `ok`; running-container Nginx syntax passed |
| Canonical route | pass | `/agent-orchestration-guide` returns `200` and the exact source digest |
| Redirects and missing path | pass | The slash and `index.html` variants return `308` with the canonical relative location; an unknown child returns `404` |
| Response headers | pass | HTML content type, CSP with `connect-src 'none'`, nosniff, frame denial, restrictive permissions, referrer policy, and `no-cache` are present |
| Portfolio continuity | pass | `/` remained byte-identical at `477f2ca9a1c1787054e5e0d75b15417e59d7af113a5fdd403a69702e24cc6196` |
| Craft continuity | pass | `/craft` remained byte-identical at `a2fc1c35490fb1da00145602b427298fb8e17f25bb5d348be97a233dcecac3bc` |
| Bella continuity | pass | `/bella` remained byte-identical at `e0dc32910abe18c63194dbdbce672d34c0ff95de7d7543dd5b5268141f2dfb48` |
| DomainSpec protection | pass | Anonymous and intentionally wrong credentials still return `401` for the protected index, named guide, and absent deep path; the Basic Auth challenge remains present |
| Adjacent host continuity | pass | `https://time-capsule.cyberalchemize.com/` and `https://troqarapp.com/` both returned `200` after the release |
| Staging cleanup | pass | No `.next`, `site.failed`, or `site.rollback-next` path remained after success |
| Future release preservation | pass | Final local `full`, `domainspec`, and `agent-orchestration-guide` dry runs all pass; `full` packages the reviewed source and `domainspec` captures the current live guide so later releases cannot silently erase the route |

The `domainspec` and `full` regression dry runs used `.git/HEAD` only as a
non-secret, one-line local input that satisfies password-file shape checks.
`DRY_RUN=1` prevented upload or remote mutation; no credential was read or
recorded.

## Browser acceptance

The live HTTPS page was exercised in Chromium, not only opened. The run selected
the correct answers, recorded a relay state, inspected a code field, copied a
fixture command, completed all seven lessons, submitted the exit ticket, copied
and parsed the learning receipt, reloaded the page, and verified restoration.

| Check | Result |
| --- | --- |
| Navigation and document | `200`; expected title and `h1`; seven lessons |
| Progress | advanced `0/7` through `7/7` in order |
| Receipt boundary | `self_recorded_unverified`; all seven lesson IDs present |
| Clipboard | copied receipt parsed successfully with seven completed lessons |
| Persistence | reload restored `7/7`, the `Gate decided` relay trace, and the exit ticket |
| Desktop layout | `1440` viewport and document width; no horizontal overflow |
| Mobile layout | `390` viewport and document width; no horizontal overflow |
| Reduced motion | media query matched; lesson transition reduced to `1e-06s` |
| Network boundary | three document requests, all from `https://cyberalchemize.com`; no failed request |
| Runtime errors | zero console errors, page errors, or warnings |

Browser evidence:

| File | SHA-256 |
| --- | --- |
| `output/playwright/agent-orchestration-guide-live.JOwSeK/desktop.png` | `8641dc051bb9f7c779a9f99dac7bced995d333ed879617e91330cf9040647d30` |
| `output/playwright/agent-orchestration-guide-live.JOwSeK/mobile.png` | `54910e507a3505d93c14fcfa888e8760e42cbe69a143f6ec827f9a034da2860d` |

## Browser runtime

- Playwright: `1.59.1`
- Chromium revision: `1217`
- Executable: `/home/vrondelli/.cache/ms-playwright/chromium-1217/chrome-linux64/chrome`
- Executable SHA-256: `696170a79640ec5b50c7518140ace06c69a49cfb295bf527d4a85e26a12b89a7`

The active shell used Node `22.13.0`, where Playwright was absent. No package or
browser was installed. Acceptance used the repository-approved shared Node
`22.12.0` Playwright runtime directly.

## Preserved infrastructure and rollback

The following remote bytes were unchanged across the release:

| Artifact | SHA-256 |
| --- | --- |
| `docker-compose.yml` | `c3022b1cb3eddae1879d21b8b5e78143dbe7b6b5c1d8fe1e66056d1dbf6f1e07` |
| `.env` | `a3283a429867352f1a9dab9ba97a6cfc37055040b884c88d2bcf42b71ee8a2fa` |
| `.domainspec.htpasswd` | `aa6d1cd8f5814127b95cb4a248c251a2c1d4c4f3a4f583b26cf5f68247af8d7a` |

The immediately previous complete site generation remains at
`/srv/co-op-engine/site.previous`. `nginx.conf.previous` retains the pre-route
digest `cd88d8b8db0be01d7752323c44246b7c4917fda2912a1a5e76f4a3ca2d93bf5f`;
the `.previous` Compose, environment, and verifier hashes match the active
preserved bytes. The scoped script restores that generation and recreates the
same service if switching, startup, direct health, worker readability, or live
HTTPS validation fails.

## Boundaries

- This is a deployed public learning prototype, not canonical documentation,
  a product release, or evidence that the taught runtime is production-ready.
- Scripted browser completion proves the encoded interaction path works. It
  does not prove human comprehension or the semantic quality of a learner's
  free-text answer.
- The learning receipt deliberately identifies itself as self-recorded and
  unverified; it is not authorization, publication, deployment, production, or
  semantic truth.
- No commit or push was requested or performed. The guide source, deployment
  changes, this receipt, and ignored browser evidence remain local workspace
  artifacts.
