# Spec card — vault_shared/canonical_enum_hashes.yaml signing ceremony

**Architecture anchor:** `pipeline/architecture/v0.1/architecture_v7_0_8_amendment.md` §1 + §4.0 (LOCKED 2026-05-08).
**Spec-card version:** v1
**Round:** post-v7.0.8-LOCK (companion module 3 of 3 — operator-only ceremony, not a code module).
**Priority:** v0.1 medium — F-CIC-CLC-ENUM-DRIFT requires the signed reference hash to exist; without it, the gate fails-closed every Tilth startup.

---

## Purpose

Establish the operator-signed reference-hash file that F-CIC-CLC-ENUM-DRIFT (PRE-gate order 6.45) compares against at every Tilth startup. This is a **one-time operator ceremony** at amendment LOCK plus subsequent re-signs whenever a future amendment legitimately modifies `pipeline/types/identity_capital.py`.

## File location

`vault_shared/canonical_enum_hashes.yaml`

## Schema

```yaml
schema_version: canonical_enum_hashes.v1
signed_at_iso8601: <utc-timestamp>
signed_by_operator_key_id: <ed25519_public_key_fingerprint>

identity_capital_module_path: pipeline/types/identity_capital.py
identity_capital_module_sha3_512: <128-char hex>

canonical_cic_count: 6
canonical_clc_count: 8

amendment_authority:
  amendment_id: v7.0.8
  amendment_path: pipeline/architecture/v0.1/architecture_v7_0_8_amendment.md
  amendment_lock_timestamp_iso8601: 2026-05-08T<lock-time>Z

# Hybrid Ed25519 + ML-DSA-65 signature per A12 crypto-agility envelope.
# Both signatures cover signed_payload_bytes (canonicalized JSON of the
# above fields). Both must verify for F-CIC-CLC-ENUM-DRIFT to pass.

signed_payload_bytes: <base64 of canonicalized JSON>

signature_ed25519: <base64>
signature_ml_dsa_65: <base64>

operator_public_key_ed25519: <base64>
operator_public_key_ml_dsa_65: <base64>
```

## Signing ceremony

```bash
# 1. Compute the hash of the canonical-enum module
openssl dgst -sha3-512 pipeline/types/identity_capital.py
# → record the hex digest as identity_capital_module_sha3_512

# 2. Construct the canonical-payload JSON (Python script — TBD)
python3 scripts/sign_canonical_enums.py \
    --module pipeline/types/identity_capital.py \
    --amendment-id v7.0.8 \
    --amendment-path pipeline/architecture/v0.1/architecture_v7_0_8_amendment.md \
    --operator-key-id <key_fingerprint> \
    --output vault_shared/canonical_enum_hashes.yaml

# 3. Sign with operator's keys (the script prompts; uses operator's
#    Ed25519 + ML-DSA-65 private keys via the same hardware path used
#    for daily-log lock blocks per BT9 audit-chain discipline)
```

## Re-signing trigger

A new architecture amendment that legitimately modifies `pipeline/types/identity_capital.py` (e.g., adding a 7th CIC after the four "additional pathways" research lands per `memory/project_six_launch_markets_2026-05-08.md`) requires:

1. The amendment LOCKs.
2. Operator runs the signing ceremony again, citing the new amendment as `amendment_authority.amendment_id`.
3. Cycle-2 verification of the new amendment confirms the hash chain.
4. F-CIC-CLC-ENUM-DRIFT now passes against the new module + new reference hash.

Until all four complete, F-CIC-CLC-ENUM-DRIFT fail-closes Tilth startup.

## Acceptance tests

- The signing script produces a YAML file matching the schema.
- F-CIC-CLC-ENUM-DRIFT passes against the produced file (real integration test, not unit-test mock).
- Tampering with `identity_capital_module_sha3_512` field by a single hex character makes F-CIC-CLC-ENUM-DRIFT.signature_invalid fire (signed_payload_bytes won't match).
- Tampering with `pipeline/types/identity_capital.py` (e.g., adding a 9th CLC entry) makes F-CIC-CLC-ENUM-DRIFT.hash_mismatch fire.
- Tampering with `canonical_cic_count: 6 → 7` field without re-signing fires `F-CIC-CLC-ENUM-DRIFT.signature_invalid`.

## Coordination

- Composes against the existing operator-signature path used for `lock_history.v1.jsonl` and daily-log lock blocks (BT9 audit chain).
- Same Ed25519 + ML-DSA-65 hybrid envelope per A12 crypto-agility (`memory/project_tilth_architecture_v7_locked.md`).
- Build the `scripts/sign_canonical_enums.py` script first; the YAML file is its output.

## Open questions for build session

1. Where does the operator's ML-DSA-65 signing key live? (Per A12: persistent operator key issuance is gated on real-engineer onboarding per Da Vinci §13 / DV-F-10. Until then, dev-mode `--generate-keys` ephemeral keypair acceptable per the v7.0.1 GPP LOCK precedent.)
2. Should the signing script live in `scripts/` (workspace-wide) or `pipeline/scripts/` (pipeline-scoped)? (Suggest: `scripts/`. It's an operator ceremony, not pipeline runtime code.)
3. What's the test approach for the signing ceremony? (Suggest: integration test that runs the script against a mock module file, verifies output schema, then runs F-CIC-CLC-ENUM-DRIFT against the output and asserts pass.)
