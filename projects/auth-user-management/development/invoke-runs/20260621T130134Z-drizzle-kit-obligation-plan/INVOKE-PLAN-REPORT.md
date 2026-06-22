# Drizzle Kit Obligation Invoke Plan

## Invocation

- Run id: `20260621T130134Z-drizzle-kit-obligation-plan`
- Mode: `/invoke plan`
- Target: `projects/auth-user-management`
- Architecture obligation target: `implementation/domainspec/architecture/pattern-library/SQL-PERSISTENCE.md`
- Status: ready for `task-session`

## Intent

Repair the E2E schema shortcut introduced during the auth API harness work:
`e2e/postgres-schema.ts` currently recreates auth tables and enums with
hand-written SQL. That proves the API against PostgreSQL, but it duplicates the
Drizzle schema and can drift.

The production-ready shape is Drizzle ORM schema as the TypeScript source of
truth plus Drizzle Kit generated migrations as the executable SQL source.

## Evidence

- Poker Team reference uses `validation/poker-team/backend/drizzle.config.ts`.
- Poker Team scripts include `db:generate`, `db:migrate`, and `db:push`.
- Poker Team commits generated migrations under `validation/poker-team/backend/drizzle/`.
- Poker Team runtime image copies `backend/drizzle/` into the container.
- Auth package currently has `drizzle-orm`, `postgres`, and a Drizzle schema, but no `drizzle-kit`, `drizzle.config.ts`, or committed `drizzle/` migrations.
- Auth package E2E currently keeps duplicate table and enum creation SQL in `e2e/postgres-schema.ts`.

## Obligation Installed

The architecture pattern library now has a SQL persistence obligation:

- `implementation/domainspec/architecture/pattern-library/SQL-PERSISTENCE.md`

It says PostgreSQL persistence must use Drizzle schema plus Drizzle Kit generated
migrations, and that hand-written duplicate schema SQL is not an acceptable
production or E2E schema source when a Drizzle schema exists.

## Dispatch Technique Trace

| Technique | Applied To | Effect |
| --- | --- | --- |
| `sequence` | obligation first, package repair second | Makes the reusable rule explicit before package-local remediation. |
| `authority_split_gate` | architecture vs auth package | Architecture pattern owns the invariant; auth package owns implementation. |
| `scu_swu_reduction` | work-pack decomposition | Smallest executable unit starts with adding Drizzle Kit config and generated migrations. |
| `recomposition_proof` | E2E repair | Generated migrations must recompose with the current Drizzle schema and existing E2E scenario matrix. |
| `validation_loop` | acceptance commands | Every SWU has a runnable command or reviewable check. |
| `execution_receipt_handoff` | next route | Task Session receives exact file scope and expected receipts. |

Full dispatch JSON is not required because this is a straightforward plan-to-task-session route with one package owner and one architecture obligation update.

## Distill Validation

- Verdict: pass
- Smallest coherent repair: introduce Drizzle Kit migration generation and make E2E consume generated migrations.
- Not smaller because adding only `drizzle.config.ts` still leaves duplicate raw SQL in E2E.
- Not larger because HTTP, deployment, Troqar, and Strava remain out of scope.
- Recomposition proof: Drizzle schema -> Drizzle Kit generated migration -> E2E migration runner -> existing 8 auth API scenarios.

## Next Route

Run `task-session` on `WORK-PACK.md`, starting at `SWU-AUMDK-001`.
