# Ed25519 Seal Ceremony — v1 DRAFT

**Filed:** 2026-04-21
**Status:** DRAFT protocol — operator review + keypair generation required before execution.
**Purpose:** Promote the four amendment authorization-ledger rows from `PRE-CRYPTO-SEAL` to full Ed25519 cryptographic seal.
**Precondition:** v2.2 Wave 3 gates #5 (F-ROLLBACK-SCRIPT-INTEGRITY) + #10 (F-ROUTER-INTEGRITY-MULTI-SOURCE) LOCKED (both done as of 2026-04-21). The `SignatureVerifyCallable` Protocol in `pipeline/logician/gates/_protocols.py` is the verifier contract.
**Targets:**
1. `pipeline/engineering/amendments/agent_sdk_thesis_2026-04-19/EN-001_sdk_scribe_spike_2026-04-19.md`
2. `pipeline/engineering/amendments/agent_sdk_thesis_2026-04-19/EN-002_sdk_lifecycle_vocabulary_2026-04-19.md`
3. `pipeline/engineering/amendments/agent_sdk_thesis_2026-04-19/EN-003_code_thesis_committee_kimi_replacement_2026-04-19.md`
4. `pipeline/engineering/protocols/tilth_self_improvement_protocol_v0.1.md` (TSIP v0.1)

Ledger at `pipeline/engineering/operator_authorization_ledger.v1.jsonl` — four rows currently `seal_status: "PRE-CRYPTO-SEAL"`, `ed25519_signature: null`, `ed25519_public_key_fingerprint: null`.

---

## Ceremony principles

1. **Operator-only keypair.** The Ed25519 private key is generated and held by Josh alone. No Cowork session, no Midas session, no other agent generates or touches the private key material.
2. **Out-of-repo storage.** Private key lives at `~/.tilth/sovereignty/operator_ed25519_v1.key` (operator-chosen path). Private key NEVER enters the repo, NEVER enters any Claude conversation context.
3. **Public key pinned in-repo.** Public key is written to `pipeline/engineering/sovereignty/operator_ed25519_v1.pub` (fingerprint also recorded in the ledger rows). This is the pinned artifact the Logician verifier gates consume.
4. **Canonical bytes.** Signatures are computed over the exact SHA-3-512 hashes already recorded in each ledger row (`canonical_sha3_512` field). Operator signs the hash, not the file — avoids file-handling ambiguity.
5. **Hybrid post-quantum option (deferred).** v1 uses Ed25519 alone. v1.x may add ML-DSA-65 co-signatures per Da Vinci §7 hybrid signature plan. Canonical manifest reserves the field.

---

## Step 1 — Keypair generation (operator)

Operator runs (Josh's terminal, not Claude's sandbox):

```bash
# Generate Ed25519 keypair via OpenSSL (macOS default, post-3.0)
mkdir -p ~/.tilth/sovereignty
openssl genpkey -algorithm Ed25519 -out ~/.tilth/sovereignty/operator_ed25519_v1.key
chmod 600 ~/.tilth/sovereignty/operator_ed25519_v1.key

# Extract + save public key
openssl pkey -in ~/.tilth/sovereignty/operator_ed25519_v1.key -pubout -out ~/.tilth/sovereignty/operator_ed25519_v1.pub

# Compute public-key fingerprint (SHA-256 of the DER-encoded public key)
openssl pkey -in ~/.tilth/sovereignty/operator_ed25519_v1.pub -pubin -outform DER | openssl dgst -sha256
```

Record the fingerprint — it's referenced in every ledger row post-ceremony.

## Step 2 — Pin public key in repo (operator + Cowork coordinate)

```bash
# Operator copies public key + fingerprint file into repo
cp ~/.tilth/sovereignty/operator_ed25519_v1.pub pipeline/engineering/sovereignty/operator_ed25519_v1.pub
```

Cowork (me) writes the fingerprint manifest at `pipeline/engineering/sovereignty/operator_ed25519_v1.fingerprint.json`:

```json
{
  "algorithm": "Ed25519",
  "key_version": "v1",
  "public_key_path": "pipeline/engineering/sovereignty/operator_ed25519_v1.pub",
  "fingerprint_sha256": "<output from Step 1 line 3>",
  "generated_at_iso8601": "<operator fills in>",
  "generated_by": "Josh Inklovich (operator-ceremony)",
  "hybrid_ml_dsa_65_pending": true
}
```

## Step 3 — Sign each amendment hash (operator)

For each of the four amendments, operator signs the canonical SHA-3-512 hash already recorded in the ledger:

```bash
# EN-001 — hash 532f8cc5...fdea62
echo -n "532f8cc518a8afbd792b12d096d611670659b44734cba423936f2efe0e9bdb53e1d0463244f11ddce0ff7226acd2904e9ad8959c88e0f2d715dbe26586fdea62" | openssl pkeyutl -sign -inkey ~/.tilth/sovereignty/operator_ed25519_v1.key -rawin -out /tmp/en001.sig

# Base64-encode for ledger storage
base64 /tmp/en001.sig

# Repeat for EN-002 (1d5cab47...52ca81), EN-003 (570699c6...dcdf8827cf), TSIP (367c4756...78fc52e1)
```

Alternative: Python script does all four in one shot. Draft at `scripts/ed25519_seal_ceremony_v1.py` (to be written by Cowork):

```python
# scripts/ed25519_seal_ceremony_v1.py — operator runs this ONCE after keypair gen
# Signs the four amendment hashes + writes .sig sidecars + updates ledger rows
# Requires: private key at ~/.tilth/sovereignty/operator_ed25519_v1.key
# Reads: operator_authorization_ledger.v1.jsonl current state
# Writes: .sig sidecar files + updated ledger.v2.jsonl (v2 = post-Ed25519-seal schema)
```

## Step 4 — Write .sig sidecars

For each amendment, a companion `.sig` file records the base64-encoded signature + metadata:

```
pipeline/engineering/amendments/agent_sdk_thesis_2026-04-19/EN-001_sdk_scribe_spike_2026-04-19.md.sig
pipeline/engineering/amendments/agent_sdk_thesis_2026-04-19/EN-002_sdk_lifecycle_vocabulary_2026-04-19.md.sig
pipeline/engineering/amendments/agent_sdk_thesis_2026-04-19/EN-003_code_thesis_committee_kimi_replacement_2026-04-19.md.sig
pipeline/engineering/protocols/tilth_self_improvement_protocol_v0.1.md.sig
```

Each `.sig` file is a JSON object:

```json
{
  "algorithm": "Ed25519",
  "key_version": "v1",
  "signed_over": "canonical_sha3_512_of_amendment_bytes",
  "canonical_sha3_512": "<hash from ledger>",
  "signature_base64": "<operator-produced signature>",
  "public_key_fingerprint_sha256": "<from step 2 manifest>",
  "signed_at_iso8601": "<operator fills>",
  "hybrid_ml_dsa_65_signature_base64": null
}
```

## Step 5 — Promote ledger rows

Update `pipeline/engineering/operator_authorization_ledger.v1.jsonl` → write `v2.jsonl` with the four rows bumped:

```json
{
  "row_id": "auth-001",
  ...existing fields...,
  "seal_status": "ED25519_SEALED",
  "ed25519_signature_base64": "<from step 3>",
  "ed25519_public_key_fingerprint_sha256": "<from step 2>",
  "ed25519_sealed_at_iso8601": "<ceremony time>",
  "sig_sidecar_path": "pipeline/engineering/amendments/.../EN-001_...md.sig"
}
```

v1 ledger preserved on disk as audit trail; v2 supersedes.

## Step 6 — Verify ceremony via F-ROLLBACK-SCRIPT-INTEGRITY path

The F-AMDT-05 gate's `SignatureVerifyCallable` Protocol is the verifier contract. Run the verifier against each of the four signatures using the pinned public key. Every verify must return `True`. Any `False` → ceremony failed; operator re-investigates. Zero retries on failed verification — that's a cryptographic fault.

Test harness (Cowork writes, operator runs):
```
scripts/verify_ed25519_seal_ceremony.py — reads v2 ledger, loads pinned public key,
for each row: verify signature; report PASS/FAIL. Expected: 4 PASS, 0 FAIL.
```

## Step 7 — Lock the ceremony

On 4/4 verification PASS:
- Commit v2 ledger + .sig sidecars + fingerprint manifest as one operator-signed change.
- Daily log entry: "Ed25519 seal ceremony v1 complete; EN-001/002/003/TSIP promoted from PRE-CRYPTO-SEAL to ED25519_SEALED."
- lock_history row (lock_class: "architectural_thesis" per F-AMDT-11 carve-out, since the ceremony affects the sovereignty envelope).
- MEMORY.md entry.
- Pre-stage v1.x (hybrid ML-DSA-65 co-signature) as a next-iteration spec card.

---

## Failure-mode matrix

| Failure | Response |
|---|---|
| Keypair generation fails (OpenSSL error) | Operator investigates OpenSSL version; retry on same ceremony |
| Private key accidentally committed to repo | Revoke keypair; start over with a fresh key; old key considered compromised |
| Any signature fails verification (step 6) | Abort ceremony; do NOT write v2 ledger; operator investigates (corrupted hash? wrong key? signing-payload mismatch?) |
| Public key fingerprint mismatch between sidecars and manifest | Ceremony aborted; likely multiple keypairs used mid-ceremony; revoke + restart |
| Operator loses private key post-ceremony | Every sealed artifact remains valid (verification is public-key-only); new signings require fresh keypair ceremony; LOCKED-backfilled discipline for any post-loss amendments |

## Deferred to v1.x

- **ML-DSA-65 hybrid signatures** — post-quantum defense-in-depth per Da Vinci §7 hybrid plan. Sidecar format already reserves `hybrid_ml_dsa_65_signature_base64` field.
- **HSM-backed key storage** — BT4 HSM-capable key storage already exists in §1; operator may opt to move the Ed25519 private key to a YubiKey or similar. No ceremony change beyond key-gen step.
- **Multi-operator signatures** — Stage 3 (cooperative governance) will require m-of-n operator signatures. v1 is single-operator only.

---

## What Cowork can prepare now (without operator key material)

- `scripts/ed25519_seal_ceremony_v1.py` — signing script skeleton (takes a private-key path as input; never reads key material into any Claude session)
- `scripts/verify_ed25519_seal_ceremony.py` — verifier script
- `pipeline/engineering/sovereignty/operator_ed25519_v1.fingerprint.json` — empty template
- `pipeline/engineering/operator_authorization_ledger.v2_schema.md` — schema doc for the v2 ledger post-ceremony
- `.sig` sidecar template

All of the above are operator-runnable scripts that take the private key as an argument at runtime — Claude sessions never hold the key material.

## What Cowork CANNOT do

- Generate the keypair (operator only)
- Sign any hash (operator only, with private key)
- Hold the private key in context (never, under any circumstance)
- Execute Step 1 via bash in Claude's sandbox (sandbox is separate filesystem; keypair must exist on operator's real machine at operator-chosen path)

---

*DRAFT v0 — 2026-04-21 — ceremony protocol + Cowork prep surface. Operator review → keypair generation → Cowork writes scripts → ceremony executes → verifier PASSES → v2 ledger locks.*
