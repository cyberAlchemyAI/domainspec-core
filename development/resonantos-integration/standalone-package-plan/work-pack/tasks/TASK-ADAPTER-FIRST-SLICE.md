# TASK-ADAPTER-FIRST-SLICE

## Objective

Specify the first safe runtime behavior: a read-only observer/meter and an owner-gated
no-promotion policy.

## Layer And Slice

- Layers: L1 and L2.
- Slice: S-003.
- Waves: W1 and W2.

## Source Contracts

- `development/resonantos-integration/RESONANTOS-INTEGRATION-GUIDE.md`
- `development/resonantos-integration/owned-base/BASE-FOR-VICTOR.md`
- `work-pack/shared/context.md`

## Dependencies

- `SWU-RCI-003`.

## Blocker State

None.

## Completion State

Completed in `task-session-20260629T164831Z-standalone-package`.

## Smallest Working Units

### SWU-RCI-004

- Goal: specify a read-only observer/meter first slice.
- Dependencies: `SWU-RCI-003`.
- Source anchors: integration guide "Install / dogfood path + first slice".
- Related context: read operations `living_archive_search` and `living_archive_read`.
- Write scope:
  - `standalone-package/docs/read-only-observer.md`
  - `standalone-package/examples/observer/`
- Done criteria:
  - Observer contract names read/search hooks only.
  - Meter receipt shape is defined.
  - No write, request-ingest, decide, or promote operation appears in first slice.
- Acceptance evidence:
  - Scoped scan for write/promote tool names in observer example.
  - Review receipt shape.
- Validation surface:
  - Text scan and markdown review.
- Execution owner: local-fallback.
- Handoff note: keep this slice risk-free; do not add writes for convenience.

### SWU-RCI-005

- Goal: specify no-promotion guardrail and decide-step policy.
- Dependencies: `SWU-RCI-003`.
- Source anchors: `owned-base/BASE-FOR-VICTOR.md` first-slice recommendation.
- Related context: necronomicon no-promotion guardrail as public-safe design.
- Write scope:
  - `standalone-package/docs/no-promotion-policy.md`
  - `standalone-package/fixtures/no-promotion/`
- Done criteria:
  - Policy states default-deny.
  - Candidate cannot promote itself.
  - Decide step remains owner-gated.
  - Reject and escalate states are represented.
- Acceptance evidence:
  - No-promotion fixture review.
  - Decision enum mapping review.
- Validation surface:
  - Fixture parse plus checklist.
- Execution owner: local-fallback.
- Handoff note: this policy is a guardrail, not a new Review Queue.

## Synchronization Rules

W2 cannot close until both no-write observer and no-promotion policy are present.

## Completion Receipt

- Read-only observer contract exists at `standalone-package/docs/read-only-observer.md`.
- No-promotion policy exists at `standalone-package/docs/no-promotion-policy.md`.
- No-promotion fixture parses and represents default-deny owner gating.
