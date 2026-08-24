# Invoke Refresh: SWU-CAPI-000 `-02` Block Closeout

- Mode: `refresh`
- Mutation mode: `apply-approved`
- Result: owner closeout `pass`; source Task Session remains `block`
- Activation source: terminal continuation
- Scope: exactly `WORK-PACK.md` and
  `work-pack/execution-receipts/SWU-CAPI-000.refresh.json`

The refresh preserved the owner-selected 28-ledger/57-record contract and
recorded immutable attempt `wcli-20260805-node26-0.15.9-02` as blocked. The
importer treated a generated ledger under a literal `staged/` directory as
authority input because that component was missing from its exclusion filter.
The attempt stopped before database creation.

The consumed automatic route is now removed. No retry, successor, API work,
Craft-source mutation, publication, or deployment is admitted. A fresh
immutable attempt requires explicit owner authorization after binding the
literal `staged/` exclusion.

Validation passed for the closeout material package, handoff, live baseline,
owner receipt schema and digest, exact-byte target application, JSON parsing,
and scoped whitespace checks.
