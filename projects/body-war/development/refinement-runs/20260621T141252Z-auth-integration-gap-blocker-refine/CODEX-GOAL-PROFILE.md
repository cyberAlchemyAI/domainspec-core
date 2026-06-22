# Codex Goal Profile - BodyWar Whole Local Auth

Generated: 2026-06-21
Source work-pack: `projects/body-war/development/invoke-runs/20260621T131933Z-auth-user-management-integration/WORK-PACK.md`
Selected unit: `BWAUTH-LOCAL-AUTH-ONE-SHOT` (`SWU-BWAUTH-001` through `SWU-BWAUTH-007`)
Readiness: `pass`
One-shot mode: `yes`

## Readiness Basis

This one-shot stream is selected by operator intent: "do this whole auth for
BodyWar." It is bounded to local auth integration, not online VPS proof.

Readiness evidence:

- `WORK-PACK.md` has an ordered SWU manifest from `SWU-BWAUTH-001` through
  `SWU-BWAUTH-007`.
- Refine final synthesis says the first SWU is not blocked.
- Refine stage 01 provides strict context coverage.
- `evidence-index.json` classifies later blockers and excludes them from local
  execution.
- The known current app compile failure is the first repair target, not a
  pre-execution blocker.

## Native Goal

```text
/goal Complete the BodyWar local auth integration one-shot from projects/body-war/development/invoke-runs/20260621T131933Z-auth-user-management-integration/WORK-PACK.md, executing SWU-BWAUTH-001 through SWU-BWAUTH-007 in order. Use sidecar projects/body-war/development/refinement-runs/20260621T141252Z-auth-integration-gap-blocker-refine/CODEX-GOAL-PROFILE.md plus strict handoff pack projects/body-war/development/refinement-runs/20260621T141252Z-auth-integration-gap-blocker-refine/stages/01-context-builder.md and index projects/body-war/development/refinement-runs/20260621T141252Z-auth-integration-gap-blocker-refine/evidence-index.json. Outcome: BodyWar login/session/profile/fake-Strava local flow works with @domainspec/auth-user-management, Postgres, Drizzle Kit generated migrations, browser cookies, CSRF/origin guards, provider/profile tables, logout/activity redaction, Docker E2E, and docs sync. Verify with auth check+validate, BodyWar db:generate/check/validate, BodyWar e2e.sh all, runtime language policy, secret scan/probes, and git diff --check. Constraints: TypeScript runtime, shell only orchestration, Drizzle ORM plus Drizzle Kit generated migrations, no duplicate hand-written schema SQL, no package Strava/browser/product UI logic, no real deploy/DNS/Strava secrets/friend data. Boundaries: write only WORK-PACK scope; extra sources only for named gaps and report them. Iterate SWUs in order, validate after each repair, preserve receipts/docs. Stop and report if work requires VPS origin/access, real Strava callback/credentials, friend consent/private activity, Taquaral geometry/scoring, unbounded scope, or secret exposure.
```

## Verification Surface

Required before the goal can be marked complete:

```sh
npm --prefix projects/auth-user-management run check
npm --prefix projects/auth-user-management run validate
npm --prefix projects/body-war/app run db:generate
npm --prefix projects/body-war/app run check
npm --prefix projects/body-war/app run validate
bash projects/body-war/app/scripts/e2e.sh all
bash tools/check-runtime-language-policy.sh
git diff --check -- projects/auth-user-management projects/body-war
```

Additional required probes:

- Drizzle Kit generation is idempotent for auth and BodyWar migrations.
- Duplicate schema SQL probe over BodyWar E2E/helpers has no duplicate
  hand-written table definitions.
- Secret/token scan over touched auth, BodyWar app, docs, scripts, and infra
  artifacts shows no real tokens, OAuth codes, refresh tokens, client secrets,
  VPS secrets, or private activity payloads.
- Route/test evidence proves profile URL, token redaction, logout, activity
  no-geometry receipt, CSRF rejection, origin rejection, and simulated Strava
  callback.

## Boundaries

Allowed write scope is the source work-pack write scope:

- `projects/auth-user-management/src/application/auth-access-control/**`
- `projects/auth-user-management/src/domain/auth-access-control/**`
- `projects/auth-user-management/src/infrastructure/drizzle-postgres/**`
- `projects/auth-user-management/tests/**`
- `projects/auth-user-management/docs/ADOPTION.md`
- `projects/body-war/app/server.ts`
- `projects/body-war/app/src/**`
- `projects/body-war/app/tests/**`
- `projects/body-war/app/package.json`
- `projects/body-war/app/package-lock.json`
- `projects/body-war/app/tsconfig.json`
- `projects/body-war/app/tsconfig.test.json`
- `projects/body-war/app/drizzle.config.ts`
- `projects/body-war/app/drizzle/**`
- `projects/body-war/app/scripts/**`
- `projects/body-war/app/docker-compose.e2e.yml`
- `projects/body-war/app/.env.example`
- `projects/body-war/infra/**`
- `projects/body-war/docs/features/troqar-product-architecture/**`
- `projects/body-war/docs/INFRA-ARCHITECTURE.md`
- `projects/body-war/development/invoke-runs/20260621T131933Z-auth-user-management-integration/**`

Read-only source context:

- `projects/auth-user-management/drizzle/**`
- `projects/auth-user-management/README.md`
- `projects/auth-user-management/docs/auth-access-control/**`
- `projects/body-war/development/task-sessions/20260621T04*/**`
- `implementation/domainspec/architecture/pattern-library/SQL-PERSISTENCE.md`
- Refine run artifacts in
  `projects/body-war/development/refinement-runs/20260621T141252Z-auth-integration-gap-blocker-refine/**`

## Capability Policy

Allowed:

- Native Codex execution for the selected one-shot stream.
- Pack-first execution from the work-pack, handoff pack, and evidence index.
- Named-gap fallback exploration only for gaps listed in `evidence-index.json`.
- `decision-gate` only if a blocker-level choice appears inside the selected
  local-auth scope.
- `refine` only to repair or re-scope a named design/plan gap discovered during
  execution.
- `invoke` only if a missing define/design/plan/handoff artifact named by the
  pack is required before safe continuation.
- `craft` only if durable BodyWar blocker/gap/decision state must be synced and
  the write is scoped to the BodyWar ledger.

Not allowed without fresh operator approval:

- Subagents.
- Real VPS deploy.
- Real DNS/public-origin configuration.
- Real Strava callback or secret provisioning.
- Friend activity evidence handling.
- Taquaral geometry/scoring authority work.
- Package-level Strava/browser/product UI abstractions.

Receipt gates:

- Each SWU must report files touched, validation run, blockers, residue, and
  next route.
- The final report must name any extra sources used outside the handoff pack,
  the named gap that justified each source, and whether the source changed the
  result.
- The goal cannot be marked complete while required validation is failing unless
  the final report marks the goal blocked with the exact blocker.

## Iteration Policy

Execute SWUs in dependency order:

1. `SWU-BWAUTH-001`: auth package trusted-session use case.
2. `SWU-BWAUTH-002`: BodyWar Postgres schema and generated migration runner.
3. `SWU-BWAUTH-003`: BodyWar browser session adapter.
4. `SWU-BWAUTH-004`: BodyWar Strava OAuth/provider adapter with fake gateway
   tests.
5. `SWU-BWAUTH-005`: profile, activities, logout, and protected route wiring.
6. `SWU-BWAUTH-006`: Docker E2E and validation scripts.
7. `SWU-BWAUTH-007`: docs and deployment readiness sync without live deploy.

After each SWU:

- run the smallest relevant verification command;
- repair local failures before advancing unless the failure is explicitly routed
  to a later SWU;
- keep generated migrations from Drizzle Kit as the executable SQL source;
- avoid broad refactors not needed by the active SWU.

## Stop Condition

Stop and report `blocked` if execution requires any of these:

- VPS origin, DNS, SSH access, or live deployment;
- real Strava callback settings or real Strava secrets;
- friend consent or raw/private friend activity evidence;
- Taquaral geometry/scoring proof;
- unbounded cross-project scope;
- non-TypeScript runtime application code;
- duplicate hand-written SQL schema definitions instead of Drizzle Kit
  generated migrations;
- secret, token, OAuth code, or private payload exposure in tracked artifacts.

## Audit

- Decision profile: none.
- Handoff pack: `projects/body-war/development/refinement-runs/20260621T141252Z-auth-integration-gap-blocker-refine/stages/01-context-builder.md`.
- Context index: `projects/body-war/development/refinement-runs/20260621T141252Z-auth-integration-gap-blocker-refine/evidence-index.json`.
- Strict coverage: `pass`.
- Fallback exploration: named gaps only.
- Extra-source reporting: required.
