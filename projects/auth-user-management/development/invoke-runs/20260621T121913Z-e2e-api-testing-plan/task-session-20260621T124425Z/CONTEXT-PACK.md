# Task Session Context Pack

## Identity

- Task: `projects/auth-user-management/development/invoke-runs/20260621T121913Z-e2e-api-testing-plan/WORK-PACK.md`
- Session: `task-session-20260621T124425Z`
- Mode: standard
- Runtime: local Codex execution
- Handoff pack: none
- Strict coverage: pass

## Obligations

| ID | Obligation | Evidence | Status |
| --- | --- | --- | --- |
| O1 | Add Docker Compose PostgreSQL and shell orchestration | `WORK-PACK.md` SWU-AUME2E-001; `EXECUTION-PACK.md` implementation order | covered |
| O2 | Add Drizzle/PostgreSQL E2E harness | `WORK-PACK.md` SWU-AUME2E-002; exported `createDrizzleAuthRepositories` and `authAccessControlSchema` | covered |
| O3 | Add full TypeScript public API scenario program | `API-E2E-SCENARIO-MATRIX.md`; `src/index.ts`; `src/application/auth-access-control/index.ts` | covered |
| O4 | Wire package scripts, docs, and dependency | `package.json`; `docs/ADOPTION.md`; `scripts/validate.sh` | covered |
| O5 | Validate with Docker E2E, package checks, language policy, and diff check | `WORK-PACK.md` SWU-AUME2E-005; Docker preflight; baseline `npm run check` | covered |

## Controlling Constraints

- Use shell for orchestration and TypeScript for program logic.
- Use Drizzle with PostgreSQL for SQL persistence.
- Do not introduce an HTTP server.
- Do not commit generated JavaScript E2E source.
- Do not log secrets, bearer tokens, password hashes, or full database URLs.
- Docker state must be cleaned on success and failure.
- Runtime package API should be imported through `src/index.ts`.

## Selected Evidence

- `WORK-PACK.md`: write scope, SWU list, acceptance criteria, validation commands.
- `API-E2E-SCENARIO-MATRIX.md`: required scenario coverage across bootstrap, login, issue token, authenticate, authorize, logout, introspect, catalog, and export smoke.
- `EXECUTION-PACK.md`: Docker preflight, implementation order, default environment variables, failure handling.
- `package.json`: existing build/test/check/validate scripts and dependency split.
- `tsconfig.json` and `tsconfig.test.json`: NodeNext TypeScript shape and ignored build outputs.
- `src/index.ts`: public package export boundary.
- `src/infrastructure/drizzle-postgres/index.ts`: public Drizzle repository/schema exports.
- `docs/ADOPTION.md`: consumer-facing package boundary and Drizzle/PostgreSQL default.
- `scripts/validate.sh`: current validation does not run Docker E2E by default.

## Decisions

- Decision 1: Use `postgres` as a dev dependency because the package exposes Drizzle repository factories but only the E2E harness needs the postgres-js driver directly.
- Decision 2: Compile E2E output into `.runtime/e2e-dist`, which is already ignored, instead of adding a new tracked ignore rule for `dist-e2e`.
- Decision 3: Treat the API under test as the public TypeScript package API, not HTTP transport.

## Gate Verdict

Pass. Docker is available and the baseline `npm --prefix projects/auth-user-management run check` passed before implementation mutation.
