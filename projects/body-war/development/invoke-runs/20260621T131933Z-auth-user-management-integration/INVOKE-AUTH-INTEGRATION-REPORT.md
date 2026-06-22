# Invoke Report - BodyWar Auth Integration

Status: `pass`
Spell: `invoke`
Modes: `define`, `design`, `plan`
Target artifact owner: `projects/body-war`
Date: 2026-06-21

## Result

This run produced a governed spec, six-view design, implementation layering
model, validated dispatch route, and task-session-ready work-pack for
integrating BodyWar/TROQAR with `@domainspec/auth-user-management`.

## Key Finding

The current BodyWar app is not implementation-ready because it imports auth
package helpers that the current package does not export. Evidence:

```text
npm --prefix projects/body-war/app run check
```

Result: TypeScript compile failure for missing exports including
`createBrowserSessionGuard`, `createJsonAuthStore`,
`createStravaProviderAdapter`, `parseCookieHeader`, and related browser/OAuth
types.

The plan therefore starts by repairing the package/app contract boundary, not
by deploying to the VPS.

## Output Artifacts

- `CONTEXT-PACK.md`
- `AUTH-INTEGRATION-SPEC.md`
- `AUTH-INTEGRATION-DESIGN.md`
- `IMPLEMENTATION-LAYERING.md`
- `WORK-PACK.md`
- `DISPATCH.json`
- `PLAN-TRANSPORT.md`

## Selected Architecture

- `@domainspec/auth-user-management` owns core auth use cases, principals,
  sessions, access tokens, permission grants, token codec, Drizzle repositories,
  and generated auth migrations.
- BodyWar owns browser cookies, CSRF, Strava OAuth, provider token custody,
  profile projection, activity import, HTTP routes, and TROQAR UI behavior.
- A generic `createTrustedSessionUseCase` should be added to the auth package so
  OAuth consumers can create sessions after external identity proof without
  duplicating session/token lifecycle logic.
- BodyWar should add its own Drizzle schema and generated migrations for runner
  profile, OAuth state, provider account, and provider token custody.

## Distill Verdict

Verdict: `pass`.

Smallest coherent unit: `SWU-BWAUTH-001`, followed by BodyWar local adapter
SWUs. This is the smallest unit that repairs the broken compile boundary while
still recomposing into local E2E and later VPS proof.

## Dispatch Validation

Command:

```text
python3 .agents/skills/dispatch-spec/scripts/validate-dispatch.py projects/body-war/development/invoke-runs/20260621T131933Z-auth-user-management-integration/DISPATCH.json --json
```

Result:

```json
{"validation":"pass","blocks":[],"flags":[]}
```

## Validation Performed

- Read Invoke, context-builder, dispatch-spec, implementation-layering, and
  distill contracts.
- Built context from BodyWar product architecture, infra docs, app code, prior
  task-session receipts, auth package docs/source, and SQL persistence
  obligation.
- Ran `npm --prefix projects/body-war/app run check` as a current-state probe;
  failure recorded as the first implementation problem to repair.
- Validated `DISPATCH.json` with Dispatch Spec validator.
- Parsed `DISPATCH.json` with `python3 -m json.tool`.
- Ran `git diff --check` over this invoke run.

## Next Route

Run Task Session on the first SWU:

```text
[$task-session] projects/body-war/development/invoke-runs/20260621T131933Z-auth-user-management-integration/WORK-PACK.md --swu SWU-BWAUTH-001
```

Do not run real VPS deployment, configure real Strava callback settings, or use
friend activity evidence until the existing operator gates are resolved.
