# Distill: Copy Unit

## Mode Result

- Mode: standard
- Proposal tracks: 1
- Recursive rounds: 2
- Verdict: pass
- Next route: invoke design

## Broad Layer

Auth/user-management as a workspace reusable capability.

## Candidate Units

| Unit | Fit | Decision |
| --- | --- | --- |
| Domain-only auth-access-control copy | Too small; misses application readiness. | rejected |
| Current `projects/auth-user-management` package continuation | Conflicts with corrected source-of-truth route. | rejected |
| Poker Team auth-access-control vertical slice with ports and docs | Small enough to execute and large enough to preserve behavior and specification authority. | selected |
| Full auth plus Strava/browser sessions/Body War profile | Too broad for a reusable core copy. | deferred |

## Selected Smallest Coherent Unit

`auth-access-control-core`

Responsibility:

- copy Poker Team auth-access-control domain,
- copy application use cases,
- copy/own Drizzle/Postgres auth schema and repositories,
- normalize concrete dependencies into ports,
- copy focused behavior tests,
- extract and normalize the source DomainSpec docs,
- expose a standalone package API.

## Closure Proof

The selected unit closes because it has:

- named inputs: credentials, bearer header/token, required permission, session
  id, token id, grant namespace, bootstrap config;
- named outputs: login result, issued token, auth context, authorization result,
  logout result, introspection result, permission catalog, bootstrap report;
- persistence ports: principal, session, token, permission grants;
- documentation authority: normalized spec, aspect docs, capability docs, test
  spec, decisions, stories, and adoption notes;
- validation: copied test scaffold plus package checks.

## Recomposition Proof

The unit recomposes upward into:

- Body War/TROQAR login by importing login/authenticate/authorize/logout and
  wiring HTTP cookies or bearer transport outside the package;
- Strava connection by storing provider principals/sessions separately in a
  consumer-specific provider module;
- future services by supplying their own roles, permissions, HTTP adapters,
  token codec config, and Drizzle database.

## Deferred Complexity

- Browser cookie sessions and CSRF guards remain a consumer/interface package
  concern unless later promoted into a separate transport adapter.
- Strava OAuth remains outside this core slice.
- User profile pages and Body War UI remain outside this core slice.

## Premortem

Likely failure: copying too literally and leaving Poker Team telemetry, route,
role, doc links, and env coupling in the package. Guardrail: every application
dependency must be a port or explicit configuration input, and docs must rewrite
Poker Team paths into package-local references.

## Verdict

pass
