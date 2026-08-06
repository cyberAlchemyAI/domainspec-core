# Design Distill

- Mode: validate
- Verdict: pass
- Current smallest coherent unit: whole-wave capacity admission seam.
- Balancer objection: capacity evidence alone can race with another allocator.
- Reconciliation: preserve a `snapshot-only` ceiling and require reservation
  only for the later race-free claim; do not pull a scheduler into L0.
- Balancer objection: failure receipts are audit work, not prevention.
- Reconciliation: keep failure normalization as a separate second SWU because
  it repairs an observed invalid causal stream without pretending prevention.
- Split pressure: provider binding, route-option projection, generated parity,
  and host leases all pass independently and remain separate units.
- Recomposition: evidence -> decision -> compile/block; late failure -> null-ID
  receipt -> gate block.
- Navigation: Plan begins at `SWU-OCA-001`.

