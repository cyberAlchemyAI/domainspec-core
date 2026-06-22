# Codex Goal Profile: Auth Work-Pack One Shot

## Identity

- Source work-pack: `projects/auth-user-management/development/refinement-runs/20260621T072243Z-poker-auth-standalone-service/stages/09-invoke-plan/WORK-PACK.md`
- Selected unit: `ONE-SHOT-AUM-WORK-PACK`
- Stream: `SWU-AUM-001` through `SWU-AUM-007`
- Handoff pack: `projects/auth-user-management/development/refinement-runs/20260621T072243Z-poker-auth-standalone-service/stages/01-context-builder/CONTEXT-PACK.md`
- Handoff index: `projects/auth-user-management/development/refinement-runs/20260621T072243Z-poker-auth-standalone-service/stages/01-context-builder/context-index.json`
- Strict coverage: pass
- Decision profile: none
- One-shot mode: yes

## Native Goal

```text
/goal Execute the full auth-user-management work-pack as one ordered stream: projects/auth-user-management/development/refinement-runs/20260621T072243Z-poker-auth-standalone-service/stages/09-invoke-plan/WORK-PACK.md, using sidecar projects/auth-user-management/development/refinement-runs/20260621T072243Z-poker-auth-standalone-service/goal-profiles/20260621T080000Z-auth-work-pack-one-shot/GOAL-PROFILE.md. Outcome: replace the current package direction with a standalone TypeScript auth/user-management service copied from Poker Team auth-access-control, including domain, application use cases, Drizzle/Postgres persistence, tests, public API/adoption docs, extracted normalized docs, and readiness evidence. Verification: npm --prefix projects/auth-user-management run check; bash tools/check-runtime-language-policy.sh; test -f projects/auth-user-management/docs/auth-access-control/SPEC.md; test -f projects/auth-user-management/docs/auth-access-control/capabilities/login.md; ! rg -n "validation/poker-team|backend/src|apps/web" projects/auth-user-management/docs/auth-access-control; git diff --check -- projects/auth-user-management. Boundaries: write only projects/auth-user-management/src/**, tests/**, docs/**, package.json, package-lock.json, and this run folder; read validation/poker-team/** and arcanum/** only. Iterate SWU-AUM-001 through SWU-AUM-007 in order, running the narrowest useful check after each slice and final full validation. Stop blocked if completion requires mutating read-only sources, widening beyond auth-user-management core, adding Strava/browser-cookie/UI implementation, leaking secrets, or making an unresolved product/architecture decision; report blocker, extra sources used, and current validation state.
```

## Capability Policy

- Native Codex code/doc execution is allowed inside the write scope.
- Subagents are not authorized.
- `refine` and `invoke` are not needed unless the work-pack itself proves a named design or plan gap.
- `decision-gate` is allowed only for a blocker-level decision that cannot be safely inferred from the work-pack, context pack, or local source.
- `craft` is not required unless a later operator instruction asks to sync ledger state.

## Execution Order

1. `SWU-AUM-001`: copy domain and define ports.
2. `SWU-AUM-002`: copy application use cases and normalize concrete dependencies into ports/config.
3. `SWU-AUM-003`: extract Drizzle/Postgres schema and repository factories.
4. `SWU-AUM-004`: port behavior tests.
5. `SWU-AUM-005`: expose public API and adoption docs.
6. `SWU-AUM-006`: extract and normalize source docs.
7. `SWU-AUM-007`: run readiness audit and sync evidence.

## Source Anchors

Read-only source anchors:

- `validation/poker-team/backend/src/domain/auth-access-control/`
- `validation/poker-team/backend/src/use-cases/auth-access-control/`
- `validation/poker-team/backend/src/infrastructure/repositories/drizzle-auth.repository.ts`
- `validation/poker-team/backend/src/infrastructure/database/schema.ts`
- `validation/poker-team/backend/src/infrastructure/http/auth/auth-access-control.test.ts`
- `validation/poker-team/backend/src/use-cases/auth-access-control/seed-system-bootstrap.test.ts`
- `validation/poker-team/docs/features/auth-access-control/`
- `validation/poker-team/docs/index/feature-map.md`
- `validation/poker-team/docs/slos.md`
- `validation/poker-team/infra/alerts/auth-access-control.rules.yml`

## Write Scope

Allowed:

- `projects/auth-user-management/src/**`
- `projects/auth-user-management/tests/**`
- `projects/auth-user-management/docs/**`
- `projects/auth-user-management/package.json`
- `projects/auth-user-management/package-lock.json`
- `projects/auth-user-management/development/refinement-runs/20260621T072243Z-poker-auth-standalone-service/**`

Read-only:

- `validation/poker-team/**`
- `arcanum/**`
- unrelated workspace files and submodule gitlinks

## Invariants

- Runtime code is TypeScript.
- Shell is acceptable for scripts.
- SQL/PostgreSQL persistence uses Drizzle by default.
- Domain/application layers do not import Drizzle, HTTP frameworks, process environment, or concrete telemetry.
- Use cases receive token, password, clock, id, telemetry, config, and repository dependencies through ports/configuration.
- Role definitions and permissions are consumer-provided or examples, not reusable package authority.
- HTTP cookies, CSRF, Strava, UI pages, and Body War/TROQAR profile behavior stay outside this core service slice.
- Do not write provider secrets, access tokens, refresh tokens, generated credentials, or private runtime profile contents to tracked files.

## Verification Surface

Run the full surface before completion:

```bash
npm --prefix projects/auth-user-management run check
bash tools/check-runtime-language-policy.sh
test -f projects/auth-user-management/docs/auth-access-control/SPEC.md
test -f projects/auth-user-management/docs/auth-access-control/capabilities/login.md
! rg -n "validation/poker-team|backend/src|apps/web" projects/auth-user-management/docs/auth-access-control
git diff --check -- projects/auth-user-management
```

Useful slice checks:

```bash
npm --prefix projects/auth-user-management run build
npm --prefix projects/auth-user-management run test
```

## Fallback Exploration

Fallback exploration is limited to named gaps:

- test runner choice: port source tests to `node:test` or add Vitest only if justified by lower risk,
- optional concrete helpers: decide during execution whether `jsonwebtoken`/`bcrypt` helpers belong in package infrastructure or remain consumer-supplied ports,
- source docs normalization: follow linked docs needed to make copied package docs coherent.

Any extra source used outside the work-pack, context pack, context index, and listed source anchors must be named in the final report with the gap that justified it and whether it changed the result.

## Stop Condition

Stop and report blocked instead of widening scope when:

- a task requires mutating `validation/poker-team/**`, `arcanum/**`, or unrelated workspace files,
- implementation needs a product decision about Strava, browser cookies, UI, Body War/TROQAR profile pages, or public package publishing,
- validation cannot run because package setup is missing and the repair would exceed write scope,
- a secret or credential would need to be committed,
- the same blocker repeats across three meaningful repair attempts.
