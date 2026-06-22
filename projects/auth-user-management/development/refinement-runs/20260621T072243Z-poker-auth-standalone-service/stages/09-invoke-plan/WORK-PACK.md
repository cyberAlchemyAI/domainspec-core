# Work Pack: Poker Auth Standalone Service

## Objective

Replace the current `projects/auth-user-management` implementation direction
with a standalone TypeScript service copied from Poker Team auth-access-control,
normalized for reuse, including extracted docs, and validated with tests.

## Complexity

Medium.

Reasons:

- more than five files,
- durable-state adapter,
- domain and application logic,
- test migration from Poker Team source,
- source documentation extraction,
- reusable import surface.

## Write Scope

Allowed:

- `projects/auth-user-management/src/**`
- `projects/auth-user-management/tests/**`
- `projects/auth-user-management/docs/**`
- `projects/auth-user-management/package.json`
- `projects/auth-user-management/package-lock.json`
- this refinement run folder

Read-only:

- `validation/poker-team/**`
- `arcanum/**`

## Source Anchors

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

## Task Board

| Task | Layer | Status | SWUs |
| --- | --- | --- | --- |
| TASK-AUM-001 Copy domain and ports | L0 | ready | SWU-AUM-001 |
| TASK-AUM-002 Copy application use cases with port normalization | L0 | ready | SWU-AUM-002 |
| TASK-AUM-003 Extract Drizzle/Postgres persistence | L1 | ready | SWU-AUM-003 |
| TASK-AUM-004 Port tests and validation | L1 | ready | SWU-AUM-004 |
| TASK-AUM-005 Public API and adoption docs | L2 | ready | SWU-AUM-005 |
| TASK-AUM-006 Extract and normalize source docs | L2 | ready | SWU-AUM-006 |
| TASK-AUM-007 Readiness audit | L3 | ready | SWU-AUM-007 |

## Smallest Working Units

### SWU-AUM-001: Copy Domain And Define Ports

Parent task: TASK-AUM-001

Goal:

Copy Poker Team auth-access-control domain into the standalone package and add
portable ports for concrete dependencies.

Dependencies:

- none

Write scope:

- `projects/auth-user-management/src/domain/**`
- `projects/auth-user-management/src/ports/**`
- `projects/auth-user-management/src/index.ts`

Done criteria:

- Domain files compile under package TypeScript settings.
- Domain has no Poker Team imports.
- Ports exist for token codec, password service, clock, id generation,
  telemetry, and repository set.

Verification:

```bash
npm --prefix projects/auth-user-management run build
```

### SWU-AUM-002: Copy Application Use Cases

Parent task: TASK-AUM-002

Goal:

Copy Poker Team auth use cases and normalize all concrete dependencies into
ports/configuration.

Dependencies:

- SWU-AUM-001

Write scope:

- `projects/auth-user-management/src/application/**`
- `projects/auth-user-management/src/ports/**`
- `projects/auth-user-management/src/index.ts`

Implementation detail:

- Replace direct `jsonwebtoken` use with `TokenCodec`.
- Replace direct bcrypt use with `PasswordService`.
- Replace direct `randomUUID` with `IdGenerator`.
- Replace direct `new Date()` with `Clock`.
- Replace telemetry imports with optional `AuthTelemetry` or no-op observer.
- Replace `process.env` access with explicit config input.
- Make admin logout permission configurable.
- Make bootstrap return a report instead of writing console output as package
  authority.

Verification:

```bash
npm --prefix projects/auth-user-management run build
```

### SWU-AUM-003: Extract Drizzle/Postgres Persistence

Parent task: TASK-AUM-003

Goal:

Copy Poker Team auth schema/repository into the package as the default SQL
persistence surface.

Dependencies:

- SWU-AUM-001

Write scope:

- `projects/auth-user-management/src/infrastructure/drizzle-postgres/**`
- `projects/auth-user-management/package.json`
- `projects/auth-user-management/package-lock.json`

Implementation detail:

- Export auth enums and tables only.
- Export `authAccessControlSchema`.
- Repository factories accept injected Drizzle database.
- Keep memory repositories separate from production SQL defaults.
- Do not export raw SQL schema strings as the canonical production API.

Verification:

```bash
npm --prefix projects/auth-user-management run build
```

### SWU-AUM-004: Port Behavior Tests

Parent task: TASK-AUM-004

Goal:

Port the Poker Team auth-access-control behavior tests to the standalone
package, trimming HTTP-route assertions and preserving domain/application
coverage.

Dependencies:

- SWU-AUM-001
- SWU-AUM-002
- SWU-AUM-003

Write scope:

- `projects/auth-user-management/tests/**`
- `projects/auth-user-management/package.json`
- `projects/auth-user-management/package-lock.json`

Implementation detail:

- Cover login R1/R2/R3 behavior.
- Cover token issue TTL bounds.
- Cover authenticate bearer token missing/invalid/expired/revoked/session
  inactive cases.
- Cover authorization deny override.
- Cover logout token/session revocation.
- Cover token introspection inactive reason precedence.
- Cover permission catalog deduplication.
- Cover lifecycle transitions and validation helpers.
- Cover bootstrap without plaintext secret leakage.
- Cover Drizzle repository table names and mapping with fakes or query fixtures.

Verification:

```bash
npm --prefix projects/auth-user-management run test
```

### SWU-AUM-005: Public API And Adoption Docs

Parent task: TASK-AUM-005

Goal:

Expose the reusable package surface and document consumer wiring for Body
War/TROQAR and later services.

Dependencies:

- SWU-AUM-001
- SWU-AUM-002
- SWU-AUM-003

Write scope:

- `projects/auth-user-management/src/index.ts`
- `projects/auth-user-management/README.md`
- `projects/auth-user-management/docs/**`

Done criteria:

- Entry point exports domain, application, ports, memory adapters, and
  Drizzle/Postgres adapters.
- Docs state that SQL/Postgres uses Drizzle by default.
- Docs state roles/permissions are consumer-provided.
- Docs state HTTP cookies, CSRF, Strava, and UI are consumer adapters, not core.

Verification:

```bash
npm --prefix projects/auth-user-management run build
```

### SWU-AUM-006: Extract And Normalize Source Docs

Parent task: TASK-AUM-006

Goal:

Extract the Poker Team auth-access-control docs into the standalone package and
normalize them so they describe reusable package authority rather than Poker
Team product routes.

Dependencies:

- SWU-AUM-001
- SWU-AUM-002
- SWU-AUM-003
- SWU-AUM-004
- SWU-AUM-005

Write scope:

- `projects/auth-user-management/docs/**`
- `projects/auth-user-management/README.md`

Implementation detail:

- Copy or transcribe the source docs under
  `projects/auth-user-management/docs/auth-access-control/`.
- Preserve the feature spec, DomainSpec aspect docs, capability docs,
  `TEST-SPEC.md`, `STORIES.md`, `tasks.en.md`, `decisions.en.md`, and
  `CHANGELOG.md`.
- Use `docs/slos.md` and `infra/alerts/auth-access-control.rules.yml` as
  operational documentation input.
- Rewrite local links and remove stale `validation/poker-team`, `backend/src`,
  and `apps/web` references from package-authority docs.
- Mark Poker Team roles, UI routes, player/coach examples, and product feature
  map entries as examples or deferred consumer-interface material.
- Keep browser cookie, CSRF, Strava, and Body War/TROQAR profile docs outside
  this core service slice unless they are explicitly framed as consumer wiring.

Done criteria:

- Extracted docs include `SPEC.md`, aspect docs, capability docs, test spec,
  stories, decisions, and tasks.
- Documentation states Drizzle/Postgres is the default SQL persistence surface.
- Documentation states roles and permissions are consumer-provided.
- Documentation distinguishes reusable auth authority from Poker Team examples.

Verification:

```bash
test -f projects/auth-user-management/docs/auth-access-control/SPEC.md
test -f projects/auth-user-management/docs/auth-access-control/capabilities/login.md
! rg -n "validation/poker-team|backend/src|apps/web" projects/auth-user-management/docs/auth-access-control
```

### SWU-AUM-007: Readiness Audit

Parent task: TASK-AUM-007

Goal:

Validate package readiness and sync evidence.

Dependencies:

- SWU-AUM-004
- SWU-AUM-005
- SWU-AUM-006

Write scope:

- `projects/auth-user-management/development/refinement-runs/20260621T072243Z-poker-auth-standalone-service/**`

Verification:

```bash
npm --prefix projects/auth-user-management run check
bash tools/check-runtime-language-policy.sh
test -f projects/auth-user-management/docs/auth-access-control/SPEC.md
! rg -n "validation/poker-team|backend/src|apps/web" projects/auth-user-management/docs/auth-access-control
git diff --check -- projects/auth-user-management
```

## Validation Strategy

Required before marking implementation complete:

```bash
npm --prefix projects/auth-user-management run check
bash tools/check-runtime-language-policy.sh
test -f projects/auth-user-management/docs/auth-access-control/SPEC.md
! rg -n "validation/poker-team|backend/src|apps/web" projects/auth-user-management/docs/auth-access-control
git diff --check -- projects/auth-user-management
```

## Blockers

None. Test runner choice is an implementation decision, not a blocker.

## Next Route

`task-session` on `SWU-AUM-001` through `SWU-AUM-007`, preferably in one
bounded session because the source and target are local and the copy boundary is
clear.
