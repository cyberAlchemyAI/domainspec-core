# Design Distill Validation

## Status

- Mode: Validate
- Runtime path: independent Proposer and Balancer roles
- Dispatch: `arcanum-addon-invoke-distill-validation-v1`
- Run: `run-20260730-f3ada9f1`
- Proposer: spawned once, joined, closed, validation `block`
- Balancer: spawned once, joined, closed, validation `block`
- Native gate: `gate_block`
- Current verdict: block after first independent review and parent reconciliation
- Design selection validator: pass
- Architecture authoring: complete

## Why This Is Separate

The deterministic Design selector proves total concern coverage and a stable
output set. It does not independently challenge whether the architecture is the
smallest coherent unit, whether a hidden owner transfer remains, or whether the
significant scenario recomposes without hidden glue.

## Joined Read-only Roles

| Role | Review target | Required receipt |
| --- | --- | --- |
| Proposer | smallest coherent integration, six-view closure, recomposition into the expected end state | [`../plan/distill/PROPOSER.md`](../plan/distill/PROPOSER.md) |
| Balancer | owner collapse, hidden runtime, state/replay/secret/rollback gaps, planned-witness inflation | [`../plan/distill/BALANCER.md`](../plan/distill/BALANCER.md) |

Join policy `all` completed. Both agents were read-only. Invoke remains the
synthesis owner.

## Reconciliation

- Accepted: add a durable L0 continuation receipt.
- Accepted: treat uninstall and rollback as isolated branches from copies of
  one accepted disabled snapshot.
- Accepted: add explicit degradation, uninstall-preservation, and rollback
  success/failure witnesses.
- Accepted: require complete SWU atomicity coverage and a BOOT-002 partial-apply
  contract.
- Accepted: make the governance packet fail closed on partial synchronization.

The Design witness contracts were revised, but the original independent
receipts correctly remain blocking evidence over the bytes they reviewed. A
second independently authorized validation is required to move this verdict to
pass. Design may inform blocked planning; it does not authorize mutation.
