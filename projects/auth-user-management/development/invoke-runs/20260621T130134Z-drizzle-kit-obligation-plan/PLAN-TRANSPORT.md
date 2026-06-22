# Plan Transport - Drizzle Kit Obligation

## Distill Verdict

- Verdict: pass
- Smallest coherent unit: Drizzle Kit migration generation plus E2E migration consumption.
- Hidden gap exposed: the prior E2E harness used hand-written duplicate schema SQL.
- Recomposition proof: architecture obligation -> auth package generator config -> generated migration -> E2E migration applier -> existing API behavior proof.

## Obligation Surface

Reusable obligation:

- `implementation/domainspec/architecture/pattern-library/SQL-PERSISTENCE.md`

Package obligation:

- `projects/auth-user-management/WORK-PACK` route requires Drizzle Kit generated migrations before the E2E harness is considered production-ready.

## Validation Strategy

Run during task-session:

```sh
npm --prefix projects/auth-user-management run db:generate
rg -n "auth_principals|auth_sessions|auth_access_tokens|auth_permission_grants" projects/auth-user-management/drizzle
rg -n "create table auth_|create type principal_|create type session_|create type permission_|create type grantee_" projects/auth-user-management/e2e/postgres-schema.ts
bash projects/auth-user-management/scripts/e2e.sh all
npm --prefix projects/auth-user-management run check
npm --prefix projects/auth-user-management run validate
bash tools/check-runtime-language-policy.sh
git diff --check -- implementation/domainspec/architecture projects/auth-user-management
```

Expected note: the `rg` check against `e2e/postgres-schema.ts` should return no matches after repair.

## Next Route

`task-session` on `WORK-PACK.md`, starting with `SWU-AUMDK-001`.
