# Queries

## queryGeneration

- Input: authorized workspace root, expected ledger digest, and one allowlisted
  query shape.
- Admission: fresh-read and validate YAML, require exact digest match, then run
  complete generation verification.
- Output: canonical JSON bytes for the declared entity/index query.
- Failure oracle: zero rows plus one stable code such as
  `PACKAGE_PROVENANCE_MISMATCH`, `LEDGER_DIGEST_MISMATCH`,
  `WORKSPACE_MISMATCH`, `GENERATION_INCOMPLETE`, or
  `PROJECTION_VERIFICATION_FAILED`.
- Forbidden: stale-generation fallback, prefix-only trust, Graph/GraphQL
  authority, or partial output.

## renderProjectionComparison

Returns exact byte/hash comparisons between YAML-derived candidate views and
the frozen fixture. It never renders from database bytes for admission.
