# Experiment Report: Typed One-Use Overrides

- Run: `decision-gate-override-20260723T035758Z`
- Result: `PASS`
- Lifecycle owner: `sigil-development`

The override matrix passed 11/11 cases and the option prefilter regression
passed 10/10. Exact reversible evidence consumed once; replay preserved the
first consumer. Ambient, malformed, stale, target/scope/hazard mismatch, and
pre-consumed evidence blocked without rewriting the artifact. Protected
hazards blocked both without an owner receipt and with an untyped path, proving
that generic override cannot bypass an owning gate.
