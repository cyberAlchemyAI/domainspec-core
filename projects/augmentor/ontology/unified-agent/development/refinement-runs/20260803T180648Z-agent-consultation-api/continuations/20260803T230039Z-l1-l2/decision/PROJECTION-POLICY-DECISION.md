# Decision Gate: Neutral Consumer Projection

This is the second independent blocker. It is prepared now but must be asked
only after `DG-L12-001` resolves the host ownership route.

## Decision

Which exact projection policy may cross from the private ontology owner into
the ResonantOS consumer?

## `STRICT_OPAQUE_CONSUMER_V1` — recommended

Allow only:

- projection: `schemaVersion`, `records`, `structuredConflicts`;
- record: opaque `id`, controlled `kind`, reviewed `label`, reviewed `summary`,
  controlled `viewIds`, reviewed `responsibility`, reviewed `boundary`;
- provenance: opaque `fieldProvenance` and `sourceHandles` only;
- confidence: controlled `level`, opaque `ownerRef`, controlled `basis`, ISO
  `assessedAt`, opaque `sourceHandle`;
- conflicts: opaque subject/statement IDs plus controlled predicate;
- manifest: schema and compiler versions, compiler digest, allowlist digest,
  opaque-ID policy version, opaque input handles plus digests, record counts,
  generation time, output digest, and typed owner approval reference.

Reject undeclared fields and any value containing private paths, private IDs,
credentials, bearer material, secrets, executable instructions, or
write/run/route/approve effects. Apply length and vocabulary bounds before
consumer emission.

- Benefit: preserves useful evidence and conflict semantics while eliminating
  raw ownership metadata and free-form confidence rationale.
- Cost/risk: requires a consumer schema/compiler version and migration from the
  fixture-only manifest.
- Downstream effect: gives SWU-007 an exact, testable read boundary and lets L2
  cache keys bind the projection and compiler digests.

## `REVIEWED_L0_SHAPE_V1`

Retain the current L0 fields, including free-form `ownerRef` and confidence
`basis`, while replacing fixture-only approval with an exact consumer approval.

- Benefit: less schema and compiler change.
- Cost/risk: every free-form value needs content review; leakage and prompt
  injection risk are higher.
- Downstream effect: faster materialization but a wider review and failure-test
  surface.

## `DEFER_CONSUMER_PROJECTION`

Keep the private-to-consumer boundary closed. L1 and L2 remain unexecuted.

## `STOP_CONSUMER_PROJECTION`

End the continuation while preserving L0 candidate-local evidence.

## Standing context option

`EXPLAIN_PROJECTION_POLICY` asks for deeper context and does not resolve the
gate.

## Current result

- Result: `PASS`.
- Selected option: `STRICT_OPAQUE_CONSUMER_V1`.
- Decision source: direct user instruction on `2026-08-04` to finish the API,
  combined with the explicitly stated strict-projection implementation scope.
- Owner binding: private ontology projection owner plus the dedicated
  consultation consumer-data boundary.
- Raw private paths, private IDs, credentials, executable instructions, and
  write/run/route/approve effects remain forbidden.
- This decision authorizes the strict data contract for implementation; it does
  not authorize publication or deployment of private ontology content.
