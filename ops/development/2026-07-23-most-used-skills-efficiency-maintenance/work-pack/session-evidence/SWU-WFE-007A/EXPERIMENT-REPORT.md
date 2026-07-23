# Experiment Report: Dispatch Sheet Evidence Binding

- Run: `dispatch-sheet-binding-20260723T040423Z`
- Result: `PASS`
- Lifecycle owner: private tooling plus `sigil-development`

The complete appender battery passed 102/102. New schema 0.7.0 rows require a
repo-contained live sheet whose bytes match two unique PASS handles and one
explicit-confirmation handle. Missing, failing, partial, substituted, mutated,
duplicate, and full-return evidence failed without changing the ledger.
Historical rows and duplicate-close behavior remained compatible. The real
telemetry ledger was not touched.
