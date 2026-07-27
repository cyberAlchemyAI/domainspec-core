# CyberAlchemy collaboration portfolio deployment receipt

- Date: `2026-07-26T21:56:37Z`
- Operator: Codex, under direct user deployment instruction
- Source SHA-256:
  `477f2ca9a1c1787054e5e0d75b15417e59d7af113a5fdd403a69702e24cc6196`
- Domain: `https://cyberalchemize.com/`
- Remote directory: `/srv/co-op-engine`
- Container: `coop-engine-site`
- Image: `nginx:1.27-alpine`
- Image ID:
  `sha256:65645c7bb6a0661892a8b03b89d0743208a18dd2f3f17a54ef4b76fb8e2f2a10`
- Compose file: `projects/co-op-engine/infra/docker-compose.yml`
- Environment: public routing values only
- Result: `pass`

## Checks

| Check | Result | Evidence |
| --- | --- | --- |
| CyberAlchemy HTTPS | pass | HTTP redirects to HTTPS; HTTPS returns 200 and `CyberAlchemy — Collaboration Portfolio` |
| Byte identity | pass | downloaded HTML and `/srv/co-op-engine/site/index.html` hashes equal the local source hash |
| Container health | pass | direct `/healthz` returned `ok`; `coop-engine-site` is running |
| Security headers | pass | CSP, frame, referrer, content-type, permissions, and no-cache headers present |
| Identity and copy | pass | no Co-Op or meta-narration denylist hits in visible or accessibility-facing browser text |
| Contact contract | pass | exact base email and LinkedIn routes plus 14 subject-only project email routes |
| JavaScript-disabled contact | pass | opening Whisper and following its static contact link reaches `#contact-whisper` |
| Presentation | pass | 20 stages; PageDown preserves stage and scrolls; focused controls retain arrow behavior; Escape restores focus |
| Filter consistency | pass | visible cards, count, heading, status, and project jumps remain synchronized |
| Responsive behavior | pass | 390×844 has no horizontal overflow and exposes identity plus Explore/Contact actions in the first viewport |
| Browser runtime | pass | Playwright Firefox found zero console errors/warnings and zero external requests |
| Time Capsule isolation | pass | expected title and HTTP 200; existing container continuity remains `Up 2 weeks` |
| TROQAR isolation | pass | root and `/api/status` return 200; app/database remain healthy with `Up 4 weeks` continuity |
| Traefik isolation | pass | existing `coop-engine` router/service and `/srv/co-op-engine` deployment root were reused |

## Browser scope

Google Chrome was unavailable at `/opt/google/chrome/chrome`. The browser
acceptance surface was exercised in Playwright Firefox and backed by exact-byte
HTTP verification.

## Boundaries

- The page exposes working inquiry paths; it does not prove that a person will
  respond, that collaboration is a fit, or that recruitment will convert.
- Reachability does not promote any project claim or artifact summary.
- No secrets, credentials, participant data, analytics, tracking, or private
  source paths were deployed.
