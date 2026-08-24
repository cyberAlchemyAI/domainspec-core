# W1: State, Journal, and Projection

- Layer question: can exact episode history be accepted, replayed, and exposed
  without ambiguity or canonical graph mutation?
- Ordered units: SWU-AKVE-003 → 004 → 005 → 006.
- Tasks: [transition oracle](../tasks/TASK-AKVE-02-TRANSITIONS.md),
  [journal](../tasks/TASK-AKVE-03-JOURNAL.md), and
  [reducer/projection](../tasks/TASK-AKVE-04-PROJECTION.md).
- Entry: W0 terminal receipts.
- Exit: transition totality, atomic retry/recovery, deterministic replay,
  quarantine, overlay isolation, and zero-canonical-write evidence pass.
- Parallelization: none for mutation; each unit binds its predecessor's exact
  contract digest. After closeout, read-only regression checks may run together.

