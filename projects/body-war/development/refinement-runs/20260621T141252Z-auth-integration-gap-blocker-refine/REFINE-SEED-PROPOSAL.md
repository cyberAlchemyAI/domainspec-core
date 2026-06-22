# Refine Seed Proposal - Auth Integration Gap/Blocker Review

Status: `strategy-proposed`
Created: 2026-06-21
Target: `projects/body-war/development/invoke-runs/20260621T131933Z-auth-user-management-integration/`
Preset: `standard`
Research: `no-research`

## Operator Intent

Refine whether the BodyWar auth integration packet has any gaps or blockers
before the next `task-session` execution.

## Desired Outcome

A local, evidence-backed gap/blocker review that answers:

- what blocks `SWU-BWAUTH-001`;
- what blocks the full BodyWar auth integration work-pack;
- what blocks online proof on the VPS;
- whether the invoke packet needs repair before execution.

## Evidence Boundary

Primary target:

- `projects/body-war/development/invoke-runs/20260621T131933Z-auth-user-management-integration/`

Supporting local evidence:

- `projects/body-war/.craft/ledger.yml`
- `projects/body-war/docs/decisions/vps-deployment-readiness.md`
- `projects/body-war/docs/features/troqar-product-architecture/`
- `projects/body-war/app/server.ts`
- `projects/body-war/app/tests/auth-consumer.test.ts`
- `projects/auth-user-management/README.md`
- `projects/auth-user-management/docs/ADOPTION.md`
- `projects/auth-user-management/src/index.ts`
- `implementation/domainspec/architecture/pattern-library/SQL-PERSISTENCE.md`

## Preliminary Gap/Blocker Forecast

Known blockers already visible before running the full Refine loop:

1. `SWU-BWAUTH-001` is not blocked by product decisions; it is the correct first
   execution unit.
2. The current BodyWar app is blocked for implementation readiness because it
   imports auth package members that are not exported by the current package.
3. Full local integration is blocked until BodyWar owns browser/session, CSRF,
   Strava OAuth, provider token custody, profile projection, and its own Drizzle
   migrations.
4. Online proof is blocked by existing operator decisions: public origin, VPS
   access, real Strava callback/credentials, and friend activity consent.
5. BodyWar Craft still tracks active project gaps: real Strava activity evidence
   and Taquaral geometry evidence.
6. Existing BodyWar docs contain stale ownership statements from earlier auth
   work and need a later documentation SWU.

## Planned Refine Route

Use the canonical ten-stage Refine loop:

1. Context Builder evidence baseline.
2. Invoke Define review.
3. Interrogation refine-review.
4. Research decision.
5. Distill.
6. Invoke Redefine / Design.
7. Interrogation refine-design-review.
8. Distill Repair.
9. Invoke Plan repair or confirmation.
10. Final Interrogation and Refine synthesis.

## Permission State

This run stops after strategy proposal and dispatch validation. It does not run
runtime-backed stages until the operator confirms the strategy.

## Recommended Confirmation

Confirm the local Refine loop if you want the packet repaired or affirmed before
starting `task-session`.
