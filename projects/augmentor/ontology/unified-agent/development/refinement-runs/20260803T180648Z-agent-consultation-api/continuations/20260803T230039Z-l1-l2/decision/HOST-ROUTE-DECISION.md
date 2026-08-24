# Decision Gate: L1 Alpha Host Route

## Decision

Which runtime owner should expose the read-only Augmentor consultation boundary
in the current ResonantOS Alpha?

This blocks the refreshed work-pack because the choice changes the exact paths,
route capability, readable source boundary, tests, documentation, owners, and
material-package digest for SWU-007 through SWU-011.

## Admissible options

### `NEW_NAMED_BRIDGE_SERVICE` — recommended

- Benefit: one narrow owner for consultation, one scoped read capability, and a
  clean separation from memory mutation and provider invocation.
- Cost/risk: adds a service, route declaration, capability, composition wiring,
  focused tests, and ownership documentation.
- Choose when: consultation should remain an evidence-only service with no
  memory-write or provider-call authority.
- Downstream effect: the refreshed task targets a dedicated host service plus
  pure shared contracts; the next gate can approve its exact projection fields.
- Owner gate: ResonantOS product and host owner approval of the route,
  capability, readable projection location, and issue acceptance.

### `EXTEND_MEMORY_HOST_SERVICE`

- Benefit: reuses existing approved-source and local-data plumbing.
- Cost/risk: expands the memory owner's responsibility and can blur the
  boundary between read-only ontology consultation and governed memory
  intake/promotion.
- Choose when: the product intentionally treats the approved neutral
  projection as a memory source and the memory owner accepts the added policy.
- Downstream effect: every L1-L2 package and failure test must also preserve the
  memory service's existing review, promotion, and source-root boundaries.
- Owner gate: ResonantOS product, host, and memory owner approval.

### `DEFER_L1_L2`

- Benefit: retains the completed L0 result without new consumer risk.
- Cost/risk: the API remains candidate-local and no agent can consult it through
  the current Alpha runtime.
- Downstream effect: keep the goal open or explicitly defer it; generate no new
  epoch.

### `STOP_L1_L2`

- Benefit: closes this continuation with no consumer or authority changes.
- Cost/risk: the requested L1-L2 integration is not delivered.
- Downstream effect: stop the active goal without claiming L2.

## Rejected option

`CORE_ONLY_NO_ALPHA_ROUTE` is structurally inadmissible. `src/core` may own pure
shared contracts, but it is not a privileged Alpha process and cannot produce
the required host witness.

## Standing context option

`EXPLAIN_HOST_ROUTE` asks for deeper context and does not resolve the gate.

## Current result

- Result: `PASS`.
- Selected option: `NEW_NAMED_BRIDGE_SERVICE`.
- Decision source: direct user instruction on `2026-08-04` to implement the
  complete API so owner-selected clients can consult it.
- Interpretation: the API remains authenticated; "anyone I want" means
  individually grantable and revocable access keys, not anonymous access.
- Owner binding: the dedicated consultation host service owns consultation
  behavior; the bridge retains transport authentication and capability checks.
- This decision does not authorize deployment or non-loopback exposure.
- Next decision: `DG-L12-002`, resolved in favor of the strict opaque consumer
  projection by the same direct instruction and stated implementation boundary.
