# S05 - Distill Correction Unit

Owner: `distill`
Mode: `standard`
Verdict: `pass`

## Objective And Output Artifact

Distill the broad correction into the smallest coherent executable unit that still recomposes into the reusable auth/user-management foundation and Body War Strava login goal.

Output artifact shape: implementation-layering plus work-pack.

## Proposal Trace

### Proposer Claim

The smallest coherent unit is not "rewrite everything in Body War" and not "write a policy doc." It is:

`SWU-AUTH-001`: retire the Python auth foundation and create the TypeScript package skeleton, shell validation entrypoint, and domain/application boundary contracts.

### Balancer Objection

If only the package skeleton is created, Strava login might still be unproven and Body War might still import Python.

### Reconciliation

Keep `SWU-AUTH-001` as the first executable unit, but make the work-pack include dependent SWUs for domain rules, browser guard, Strava provider, Body War consumer boundary, and invariant enforcement. The first SWU must remove the bad foundation and establish the TypeScript package shape so all later auth work lands in the right language.

## Current Smallest Coherent Unit

`SWU-AUTH-001 - TypeScript Auth Package Baseline`

Responsibility:

- stop treating Python files as the auth package,
- create TypeScript package metadata and compiler/test setup,
- create DomainSpec layer folders,
- create shell validation script,
- add placeholder exports/contracts that compile,
- leave implementation details for subsequent SWUs.

## Concept Layer Map

| Layer | Scope |
| --- | --- |
| Broad system | Repo-wide language invariant for all private projects. |
| Feature family | Reusable auth/user-management and provider-link foundation. |
| Package | `projects/auth-user-management` TypeScript package. |
| First executable unit | TypeScript baseline plus shell validation and Python retirement. |

## Closure And Recomposition Proof

Closure:

- `SWU-AUTH-001` has a bounded write scope.
- It can be verified by shell, package metadata, TypeScript compile/check, and absence of Python auth runtime files.
- It does not require production Strava credentials.

Recomposition:

- Later SWUs add domain rules, application use-cases, infrastructure adapters, interface guards, Strava integration, and Body War consumption into the package skeleton.
- Repo invariant enforcement composes around the same package validation surface.

## Deferred Complexity

- Production IdP choice.
- Durable database schema migration.
- Real Strava credential smoke test.
- Body War full app migration away from Python.

## Distill Result

- Target context: reusable auth foundation plus first Body War consumer.
- Mode and budget: standard, two role passes simulated locally.
- Verdict: pass.
- Current smallest coherent unit: `SWU-AUTH-001`.
- Next route: invoke design, then invoke plan.
