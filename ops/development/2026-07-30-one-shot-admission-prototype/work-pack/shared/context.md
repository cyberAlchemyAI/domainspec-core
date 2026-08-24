# Shared execution context

## Accepted architecture

WPRA phases 1–4 derive a digest-bound admission projection with
`authorityEffect: none`. Exact producers retain material ownership. Decision
Gate/human approval binds a finite epoch. Task Session Until Blocker may request
one fresh one-SWU Task Session only while epoch, cursor, successor, budget, and
closeout evidence remain valid.

## Prototype defaults

- Add parallel v2 contracts; do not silently change v1 semantics.
- Receipt-producing owners own their schemas and validators.
- WPRA may flag only `observability-residue`; all admission semantics block.
- Chain transitions are immutable and hash-linked.
- NO_OP binds terminal receipt, closeout contract, before/after inventories,
  validator identity, and continuation verification.
- Compensation is `none` with rationale or `owner-routed`; never automatic.

## Source selectors

- Research: `findings.md#current-and-target-architecture`,
  `#normalized-objective-execution-manifest`, `#plan-epoch-and-invalidation`,
  `#exact-body-war-replay-and-fixtures`.
- WPRA: `README.md#phase-contract`.
- Chain: `README.md#preconditions`, `#shared-chain-state`, `#phases`.
