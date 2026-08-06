# TASK-AUGPUB-01 — Candidate Proof

- Units: `SWU-AUGPUB-002` and `SWU-AUGPUB-003`
- Owners: Augmentor producer/page owner, ResonantOS consumer owner, validation
  owner
- Goal: rebuild, validate, and package one exact candidate with no external
  transport.
- Write scope: deterministic generated outputs only if current source requires
  them; candidate-local manifest, fixtures, and receipts.
- Forbidden: production, credentials, unrelated repository dirt, Git.
- Acceptance: all commands in the implementation plan pass under Node
  `22.13.0`; dry-run inventory and rollback rehearsal pass.
- Closeout: candidate admission receipt routes to the explicit external-effect
  gate for `TASK-AUGPUB-02`.

