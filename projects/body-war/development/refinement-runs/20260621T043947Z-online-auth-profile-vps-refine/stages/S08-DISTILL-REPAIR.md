# S08 Distill Repair

Status: `pass`
Input: `stages/S07-INTERROGATION-DESIGN-REVIEW.md`

## Repair Principle

Do not solve every TROQAR surface. Repair only what would make the Online
Identity Loop falsely appear production-ready.

## Repairs Applied

| Flag | Repair |
| --- | --- |
| JSON/local store is not production token custody. | Make Postgres store implementation a first-class SWU before VPS smoke. |
| Domain/DNS missing. | Keep deployment as config-ready until canonical origin and redirect URI are supplied. |
| Friend activity consent missing. | Treat friend activity as a validation precondition, not a seed data source. |
| Monitoring could bloat L0. | Require health/logs and defer Prometheus/Grafana to L1 unless already cheap. |
| poker-team copy risk. | Copy topology and discipline only; all code/config names become Body War specific. |
| Track geometry unresolved. | Add explicit no-geometry/no-score caveat to profile/activity validation. |

## Repaired Execution Shape

L0A: Production-shape local implementation.

- Auth/profile APIs use production security flags in config.
- Postgres adapter exists and is testable locally.
- Profile page and Strava link are implemented.
- Activity summaries are redacted.
- Secret scan and TypeScript checks pass.

L0B: VPS deployment after domain/env decisions.

- Compose/Caddy config uses canonical origin.
- Secrets are provisioned out of git.
- Strava production redirect URI matches the deployed callback.
- Deployment receipt proves health, session, connect, profile, activity, and
  redaction.

L1: Operational hardening.

- GitHub Actions deploy, backup/restore, Prometheus/Grafana, alert rules, and
  longer-form runbooks.

## Residue After Repair

The run remains `flag`, not `block`. The remaining items are executable work or
operator decisions:

- canonical domain,
- VPS access details,
- Strava app redirect update,
- Postgres adapter implementation,
- friend consent receipt.

## Handoff

Proceed to Invoke Plan. The plan should start with documentation/infra authority
and durable auth storage, then profile UI, then deployment receipt.
