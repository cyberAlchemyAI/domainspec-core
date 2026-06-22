# S07 Interrogation - Design Review

Status: `flag`
Mode: `refine-design-review`
Input: `stages/S06-INVOKE-DESIGN.md`

## Review Question

Can this design move into Task Session execution without hiding production
risks?

## Answer

Yes, if the first Task Session treats durable storage, production environment
configuration, and receipt generation as part of the core work rather than
later polish. The design is coherent, but the path remains flagged until those
items are implemented and validated.

## Findings

| Finding | Severity | Required Repair |
| --- | --- | --- |
| Production token custody cannot rely on the local JSON store. | high | Put a Postgres auth/profile/provider adapter before online Strava validation. |
| Domain/DNS and Strava redirect URI are not selected. | high | Add a decision gate or config task before deployment smoke. |
| Friend activity can tempt premature validation claims. | medium | Require consent and redacted import receipt before using it. |
| Prometheus/Grafana may delay the useful L0. | medium | Make health/logs mandatory and monitoring optional L1. |
| poker-team infra should be copied by pattern, not blindly. | medium | Rename services, env vars, paths, and secrets to Body War. |
| Route geometry remains unresolved. | medium | Add explicit UI/backend caveat that activity import does not certify a route. |

## Acceptance Conditions For Execution

- TypeScript remains the implementation language for app/auth/store code.
- Shell remains acceptable for deployment/check scripts.
- No Python service/runtime is reintroduced.
- Secrets stay outside git and outside generated artifacts.
- Strava tokens are never returned to the browser.
- Production cookies use HttpOnly, Secure, SameSite, and CSRF binding.
- Deployment smoke includes profile link and secret redaction checks.

## Verdict

The design is good enough to plan, with flags. It should not be marked
production-ready until the flagged repairs are included in the implementation
work-pack.

## Handoff

Proceed to Distill Repair to reshape the plan around these flags.
