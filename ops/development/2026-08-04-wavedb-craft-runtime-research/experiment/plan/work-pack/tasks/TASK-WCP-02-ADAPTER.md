# TASK-WCP-02: Projection adapter

## Objective

Construct the smallest bounded adapter that builds, verifies, queries,
quarantines, and rebuilds only digest-addressed candidate generations. Layer
L0, slice S-WCP-02, wave W1. Depends on SWU-WCP-002 pass.

## SWU-WCP-003

- Primary behavior: implement the six-operation adapter and closed codec.
- Inputs: exact package lock, frozen fixture manifest, Design interface and
  dependency rules.
- Outputs: candidate-local runtime source, tests, package lock, and isolated
  smoke evidence.
- Algorithm: resolve workspace; fresh-read/validate/hash YAML; build a new
  unserved payload; independent complete readback; write manifest last; fresh
  verify on every allowlisted query; external quarantine; sibling rebuild.
- Required errors: package/provenance, workspace, YAML digest, invalid fixture,
  incomplete generation, extra key, value/hash mismatch, query refusal.
- Edge cases: path traversal, percent encoding, empty IDs, duplicate decoded
  IDs, missing/extra keys, malformed manifest, stale digest, unverified prefix.
- Write scope: `experiment/runtime/package*.json`, `runtime/src/**`,
  `runtime/test/**`, exact isolated test stores, and session evidence.
- Forbidden: active pointer, raw exported database authority, derived ingestion,
  Graph/GraphQL/vector authority, database-to-YAML writes, receipt storage,
  live Craft paths.
- Done: unit tests and one native smoke test pass with unchanged fixture YAML.
- Validation: package lock integrity; key/codec unit tests; exact manifest test;
  YAML guard; allowlist scan; API export scan; native smoke test.
- Execution owner: Task Session local.

## Split analysis

Codec, builder, verifier, and query facade are kept as one SWU because the
adapter is not safely reviewable or useful if any part can bypass manifest-last
construction and fresh complete verification. Normal-path empirical execution
is separate SWU-WCP-004.
