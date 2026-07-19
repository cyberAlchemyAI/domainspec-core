# TASK-BTE-INTEGRATED-CONSUMER-MANIFEST — BTE, IOLM, Body War, Craft

## Objective

Bind the backend engine receipt and both downstream read-only consumer receipts
into one exact, digest-bound, fail-closed evidence manifest.

## Required handoffs

1. BTE source/profile/schema/registry/graph/generated-root digests plus
   `O_spec`, `O_gen`, `T_gen`, `E_run`, tests, mutation, and receipt identities.
2. IOLM imported graph identity, semantic/projection hashes, parity result,
   deterministic rebuild, negative results, posture, and `G-DSV2-SG` state.
3. Body War fixture/adapter identity, private read-only posture, exact redacted
   field allowlist result, and negative results.
4. Craft continuation pointer and accountable role IDs.

## Fail-closed rules

Reject missing, extra, duplicate, stale, skipped, unrunnable, wrong-root,
wrong-scope, unknown-ID, redaction, semantic-mutating-overlay, or surviving-
mutant evidence. Any source, rule, profile, consumer posture, manifest, or
receipt-input change revokes the affected package until `O_spec` is regenerated,
the run is repeated, negatives are replayed, and a reviewed receipt is issued.

## Claim boundary

The manifest may support only the conservative FPR-02B exact-profile claim:
13/13 backend node kinds, 16/16 backend signatures, YAML formation, resolution,
deterministic compilation, bounded traversal, causal composition/removal,
provenance, fail-closed negatives, and integrated consumer-proof comparison.
It must exclude semantic satisfiability, business correctness, UI/full-language
completeness, production readiness, public release, hosted callbacks, and any
claim that a consumer proves upstream authority by itself.

## Done criteria

- Machine-readable manifest validates and lists all required inputs/outputs.
- `O_spec = O_gen = T_gen = E_run` is exact.
- BTE, IOLM, Body War, and Craft receipts compare deterministically.
- Production remains false and no UI/backend join is inferred.
