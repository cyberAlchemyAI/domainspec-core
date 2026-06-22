# Implementation Layering: Auth Access Control Core

## Mode Result

- Owner: invoke plan
- Complexity: medium
- Layer coverage: L0-L3
- Next owner: task-session

## L0: Copy And Compile Core

Question answered: can the Poker Team auth-access-control behavior live in a
standalone package without Poker Team imports?

Scope:

- copy domain files,
- copy application use cases,
- add ports,
- adjust imports,
- add memory repositories,
- compile package.

Promotion evidence:

- `npm --prefix projects/auth-user-management run build` passes.

## L1: Persistence And Tests

Question answered: can the standalone service execute copied behavior with
repository implementations and focused tests?

Scope:

- extract Drizzle/Postgres schema,
- copy and normalize repository factories,
- port behavior tests,
- validate memory and Drizzle mapping.

Promotion evidence:

- `npm --prefix projects/auth-user-management run test` passes.

## L2: Consumer Readiness

Question answered: can Body War/TROQAR and later services import the package
without hidden Poker Team assumptions?

Scope:

- public entrypoint exports,
- adoption docs,
- extracted source DomainSpec docs normalized to package-local paths,
- explicit consumer role/permission bootstrap instructions,
- no HTTP/Strava coupling in core.

Promotion evidence:

- README/adoption guide lists import surface and consumer wiring.
- Extracted docs include feature spec, aspect docs, capability docs, test spec,
  decisions, and stories.
- `rg` confirms no forbidden Poker Team product permission defaults in package
  authority files.

## L3: Release Hygiene

Question answered: is the package safe to treat as a reusable workspace service?

Scope:

- runtime language policy,
- diff checks,
- final result/evidence sync,
- optional generated dist cleanup policy.

Promotion evidence:

- `bash tools/check-runtime-language-policy.sh` passes.
- `git diff --check -- projects/auth-user-management` passes.

## Layer Decision

Run L0-L2 in one Task Session if possible. Stop before consumer integration if
package checks fail.
