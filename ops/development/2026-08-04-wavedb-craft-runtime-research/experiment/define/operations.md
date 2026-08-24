# Operations

## buildGeneration

- Input: authorized workspace root and expected fresh ledger digest.
- Preconditions: WP-0 provenance pass, valid canonical YAML, no existing served
  generation at the target digest.
- Effect: writes a complete payload to a new isolated generation, reads it back,
  and writes the manifest last.
- Failure: stable error, zero output, no YAML mutation, suspect generation
  remains unserved.

## verifyGeneration

- Input: authorized workspace root and expected ledger digest.
- Behavior: fresh-read YAML; enumerate the complete generation; reject missing,
  extra, malformed, or wrong key/value bytes; recompute every declared digest.
- Effect: none beyond an external observation receipt.

## quarantineGeneration

- Input: exact isolated generation identity and reason.
- Effect: records an external quarantine receipt and prevents further service by
  the candidate adapter.
- Non-effect: no receipt or quarantine marker is inserted into WaveDB.

## rebuildGeneration

- Input: fresh canonical YAML and a quarantined/missing generation identity.
- Effect: creates a fresh sibling from YAML.
- Forbidden: in-place repair or recovery from database bytes.

## renderFromYaml

- Input: fresh canonical YAML.
- Output: deterministic candidate `CRAFT.md` bytes.
- Invariant: edited derived bytes are never ingested.
