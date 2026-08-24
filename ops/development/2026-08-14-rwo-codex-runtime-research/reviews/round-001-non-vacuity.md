# Round 1 — Non-Vacuity

Verdict: `REJECT_NON_VACUITY`.

The synthesis correctly denies readiness but does not yet prove a closed planning artifact. It has scenario labels rather than finite witnesses, an illustrative rather than closed active-Eve denominator, no inherited durability-cut denominator, and a desired exact-duplicate rule contradicted by F-01.

Rejected claims:

- `NV-C01`: active Eve surface is not a closed selector/digest-bound denominator.
- `NV-C02`: acceptance scenarios omit identities, preconditions, persisted records, ordered provider events, gate/result, first stop, forbidden effects, proof status, and validator.
- `NV-C03`: inherited Go durability has no closed cut denominator, and current byte drift prevents reusing the earlier PASS.
- `NV-C04`: F-01 rejects same-ID/same-payload replay while the target invariant requires an inert exact duplicate.
- `NV-C05`: compatibility/readiness is correctly not claimed and that ceiling must remain.

Required finite witnesses:

| ID | Scenario | Exact future validator |
|---|---|---|
| `RWO-CODEX-NV-01` | successful command through Codex to Rust no-successor | `TestCodexTraceSuccessNoSuccessor` |
| `RWO-CODEX-NV-02` | permission pause and scope-expansion denial | `TestCodexTracePermissionPauseAndScopeExpansion` |
| `RWO-CODEX-NV-03` | stale input stops before provider launch | `TestCodexTraceStaleInputStopsBeforeLaunch` |
| `RWO-CODEX-NV-04` | interrupt and recovery-only resume | `TestCodexTraceInterruptRecoveryOnlyResume` |
| `RWO-CODEX-NV-05A` | ambiguous create with unique reconciliation | `TestCodexTraceAmbiguousCreateUniqueReconciliation` |
| `RWO-CODEX-NV-05B` | ambiguous create without unique reconciliation freezes | `TestCodexTraceAmbiguousCreateFreezes` |
| `RWO-CODEX-NV-06` | exact duplicate no-op | `TestCodexTraceExactDuplicateIsInert` |
| `RWO-CODEX-NV-07` | identity/hash mismatch blocks | `TestCodexTraceIdentityHashMismatchBlocks` |
| `RWO-CODEX-NV-08` | invalid/reordered/incomplete/post-terminal events | `TestCodexTraceInvalidAndPostTerminalEvents` |
| `RWO-CODEX-NV-09` | Task Session closeout failure | `TestCodexTraceTaskSessionCloseoutFailure` |
| `RWO-CODEX-NV-10` | every inherited Go durability cut | `TestCodexDurabilityCutMatrixComplete` |

Each fixture must include identities, preconditions, persisted records, ordered raw events, gate/result, first stop, forbidden effects, current proof status, and exact validator. The durability manifest must prove fixture-to-manifest cardinality and selector equality. No files were changed by the reviewer.
