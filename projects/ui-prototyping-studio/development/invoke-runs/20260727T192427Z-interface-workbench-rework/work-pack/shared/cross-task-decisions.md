# Cross-Task Decisions

- D-01: `StudioSessionStorePort.getProjectionReadToken()` is the authoritative
  coherence token producer: `file:absent` or exact raw-file-byte SHA-256 for
  file storage, and `memory:<counter>` for memory storage.
- D-02: token admission uses exact string equality, one initial attempt plus
  retry limit 2, then `ProjectionSnapshotUnstableError`; no new version on
  exhaustion.
- D-03: SWU-003 uses only current internal route constructors. New route-family
  admission is SWU-018, so no forward dependency is hidden.
- D-04: SWU-006 is a pure typed context-plan computation. SWU-007 alone owns
  live journal/commit/rollback.
- D-05: scoped status stays with SWU-016 interaction/focus/live behavior because
  it shares the event and feedback boundary; visual/targets are SWU-017.
- D-06: server route admission (018) and browser sandbox/safe rendering (019)
  are separate acceptance boundaries.
- D-07: semantic dependencies and serialization-only ordering are explicit and
  machine-readable.
- D-08: all omitted implementation paths are unauthorized; preflight binds
  exact existing bytes or `ABSENT`.
- D-09: one primary owner exists per assertion; shared witnesses remain lawful
  regression/recomposition checks.
- D-10: no SWU is selected by Plan authoring or closeout synchronization.
