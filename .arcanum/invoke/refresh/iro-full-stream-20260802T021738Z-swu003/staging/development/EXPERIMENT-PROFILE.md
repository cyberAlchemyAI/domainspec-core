# Experiment profile: intent-route-resolver candidate

- PROFILE_ID: `intent-route-resolver-candidate-v1`
- LIFECYCLE_OWNER: `candidate-lifecycle-owner`
- ARTIFACT_TYPE: `sigil`
- CONTRACT_PATH: `SKILL.md`
- PROMPT_SET: `development/example-prompts/core-four-dispositions.md`
- REGIME_SET: `development/regimes/core-portability.json`
- PROFILE_VALIDATION: `pending executable stage`

## Quality bar

The executable stage must prove exact canonical bytes for all four dispositions,
complete route traces, catalog-order invariance, uncertainty monotonicity,
zero-authority behavior, Node portability, and one real-browser witness.

## Anti-pattern controls

The harness fails on semantic fallback, inferred unresolved values, omitted
routes, product-specific imports, network or filesystem effects, noncanonical
bytes, empty evidence, save-summary evidence, or claims beyond candidate-local
portability.

## Evidence layout

Deterministic fixtures remain controls. Executable outputs belong under
`development/example-outputs/`; raw attempt evidence and timestamped reports
belong under `development/runs/`. Existing evidence is never overwritten unless
an explicit rerun policy says so.
