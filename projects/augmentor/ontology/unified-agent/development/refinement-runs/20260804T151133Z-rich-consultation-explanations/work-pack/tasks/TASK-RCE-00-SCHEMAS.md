# TASK-RCE-00: Contract Baseline

## SWU-RCE-000

Reconcile the current repository JSON schema versions with compiler and consumer runtime constants without adding rich fields or changing returned behavior.

- Inspect and declare the authoritative producer/consumer version matrix.
- Add drift tests that fail on unmatched query, result, projection, manifest, and evidence-statement identities.
- Preserve current generated projection bytes unless the accepted compatibility policy requires a deterministic version-only change.
- Run both current producer and targeted consumer suites.
- Stop if the owner cannot select one canonical family.

## SWU-RCE-001

Define closed `explanation-support` and `glossary` schemas and extend query, result, projection, and manifest contracts.

- Positive fixtures: brief, guided, deep; illustrative and source-derived examples; complete analogy; 2-5 glossary refs.
- Negative fixtures: unknown fields/refs, missing limit, mixed versions, unscoped state, unbounded arrays, unused glossary entries, final prose field.
- No source data or compiler behavior changes in this unit.
- Acceptance: deterministic validator passes all positives and rejects every negative with stable codes.
