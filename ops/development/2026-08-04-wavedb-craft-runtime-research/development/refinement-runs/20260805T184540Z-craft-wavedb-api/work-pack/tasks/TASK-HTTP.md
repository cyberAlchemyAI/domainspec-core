# TASK-HTTP — Deliver the authorized L0 consultation slice

Layer/slice: L0 / S-HTTP. Source contracts: `API-CONTRACT.md`,
`SECURITY-BOUNDARY.md`, TASK-RUNTIME and TASK-CONTRACT outputs.

## SWU-CAPI-006 — Authentication/policy ports and concealment

- Primary behavior: explicit action/resource decisions implement the fixed
  route precedence with absent/denied indistinguishability.
- Independent boundary: fake-provider tests cover every competing-error pair
  without a network listener.
- Split analysis: authentication and authorization remain separate ports, but
  concealment ordering is one caller-observable behavior.
- Dependencies: SWU-CAPI-004 and owner approval of port shapes; real provider is
  deferred.
- Write scope: `implementation/domainspec/tools/craft-consultation-api/src/auth/`
  and `implementation/domainspec/tools/craft-consultation-api/test/auth/`.
- Done/evidence: action matrix for status, base/provenance/path/raw, row list/read;
  denial logs contain no rationale or protected data.
- Validation: policy matrix and golden problem-response tests.
- Owner/handoff: bounded implementation helper or local Task Session.

## SWU-CAPI-007 — Status, catalog, metadata, and raw HTTP routes

- Primary behavior: GET/HEAD L0 routes serve one captured verified snapshot
  under auth, metadata tiers, limits, cache rules, ETag, and snapshot pinning.
- Independent boundary: in-process HTTP contract suite exercises the whole raw
  consultation journey and read-only negatives.
- Split analysis: route modules may be files, but status/catalog/raw must share
  one response envelope and handle capture to prove no mixed snapshot.
- Dependencies: SWU-CAPI-002, 003, 005, 006.
- Write scope: `implementation/domainspec/tools/craft-consultation-api/src/http/`,
  `implementation/domainspec/tools/craft-consultation-api/test/http/`.
- Done/evidence: all L0 route, header, error, cache, precondition, concurrency,
  no-body, no-range, and unsupported-method cases pass; no writer is reachable.
- Validation: in-process contract tests, dependency/API surface scan, scoped
  whitespace and secret scan.
- Owner/handoff: bounded implementation helper or local Task Session.

Synchronization: no deployment, listener exposure, provider integration, or
snapshot publication is admitted by these SWUs.
