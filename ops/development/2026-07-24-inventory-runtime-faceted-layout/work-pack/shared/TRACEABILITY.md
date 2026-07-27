# Requirement Traceability

| Acceptance | Architecture | SWU | Evidence |
|---|---|---|---|
| AC-01 unrelated CWD | root resolver | 002, 007 | package-relative receipt |
| AC-02 clean warning delta | warning delta | 002, 007 | zero-introduced fixture |
| AC-03 one new warning | warning delta | 002, 007 | one-introduced fixture |
| AC-04 repeated dry-run | receipt emitter | 001, 002, 007 | byte identity and filesystem digests |
| AC-05 no-op/conflict | normalizer/candidate builder | 002 | state fixtures |
| AC-06 partial mutation | write observer | 003 | injected failure receipts |
| AC-07 faceted path/maps | facet policy/projections | 004, 005 | schema and projection fixtures |
| AC-08 legacy preserved | facet policy | 004, 005 | legacy fixture |
| AC-09 sync safety | manifest/sync | 006, 007 | managed-set receipt |
| AC-10 public/private boundary | every public component | 006, 007, VERIFY | boundary scan |

