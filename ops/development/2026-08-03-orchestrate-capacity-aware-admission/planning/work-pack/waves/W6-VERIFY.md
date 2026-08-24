# W6 — Integrated read-only verification

- Task: [TASK-OCA-VERIFY](../tasks/TASK-OCA-VERIFY.md)
- Dependency: OCA-001 through OCA-005 terminal receipts
- Mutation: forbidden

Run the exact regression, recomposition, parity, public-boundary, whitespace,
and scoped-diff checks. On failure, identify the owning SWU and block; do not
patch during this wave.

The terminal receipt may claim candidate implementation validation only. Live
host reservation/release, consumer adoption, deployment, and production
readiness remain deferred.
