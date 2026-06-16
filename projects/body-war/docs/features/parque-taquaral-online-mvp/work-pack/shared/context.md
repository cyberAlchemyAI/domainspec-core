# Shared Context

## Target

Parque Taquaral online MVP for Body War / TROQAR.

## Source Of Truth

| Artifact | Use |
| --- | --- |
| `projects/body-war/docs/decisions/parque-taquaral-online-mvp-oneshot.md` | Product and success decisions. |
| `projects/body-war/docs/features/parque-taquaral-online-mvp/DESIGN.md` | Architecture/design source for this plan. |
| `projects/body-war/docs/features/parque-taquaral-online-mvp/IMPLEMENTATION-LAYERING.md` | L0-L3 promotion boundary. |
| `projects/body-war/docs/features/parque-taquaral-online-mvp/PILOT-DOMAINSPEC-COVERAGE.md` | Missing coverage synthesis. |
| `projects/body-war/docs/features/parque-taquaral-online-mvp/PILOT-DOMAINSPEC-BACKLOG.md` | P0 artifact order and blockers. |
| `projects/body-war/docs/features/parque-taquaral-online-mvp/ARCHITECTURE-AUDIT.md` | TypeScript app and DomainSpec path/source boundary. |

## Guardrails

- Hosted friend preview is success; do not claim pilot-ready.
- Visible runner data is real consenting Strava data.
- Fixtures are allowed for tests only.
- `preview-accepted` is not `verified`.
- No repo artifact may include tokens, secrets, raw private activity payloads, or
  unredacted friend data.
- Do not replace Python app files until W0 is complete.
