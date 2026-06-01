---
title: WPFA Sovereign Node LLC signing ceremony runbook (for SN-LLC governance)
filed: 2026-05-18
status: AUTHORED 2026-05-18 — pre-publication runbook for Sovereign Node LLC governance; not a Tilth operator runbook (operator side is `docs/wpfa_white_glove_pubkey_pin_runbook_2026-05-18.md`)
applies_to: Sovereign Node LLC governance + technical team executing inaugural Q3-2026 Coefficient Registry signing (and every subsequent quarterly publish)
parent_locks:
  - pipeline/blueprint/v0.1/section_17_watts_per_funding_action.md                                 # §17 v1 LOCKED 2026-05-11
  - pipeline/blueprint/v0.1/section_02_v7_4_coefficient_registry_amendment.md                     # §2 v7.4 LOCKED 2026-05-11
  - pipeline/architecture/v0.1/architecture_v7_0_7_amendment.md                                   # v7.0.7 LOCKED 2026-05-10 — §6.1 router-template Ed25519 signing precedent (byte-for-byte trust mechanism)
authority: Cowork pre-stage 2026-05-18; canonical ceremony procedure is SN-LLC governance territory; this document is a baseline that SN-LLC governance ratifies, amends, or replaces before inaugural publication
cross_links:
  - docs/wpfa_methodology_v1_draft_2026-05-18.md
  - docs/wpfa_white_glove_pubkey_pin_runbook_2026-05-18.md
  - vault_shared/wpfa/coefficient_registry/draft_Q3_2026_unsigned.yaml
  - pipeline/vault/sub_kinds/coefficient_registry.py
---

# 1. Audience and scope

This runbook is for the **Sovereign Node LLC** governance + technical team. It documents how SN-LLC signs and publishes a Coefficient Registry version that Tilth deployments will trust through the operator-pinned-pubkey chain at white-glove onboarding.

Out of scope for this runbook:
- Operator-side pubkey pinning (separate runbook: `docs/wpfa_white_glove_pubkey_pin_runbook_2026-05-18.md`)
- Methodology document authoring (see `docs/wpfa_methodology_v1_draft_2026-05-18.md`)
- Tilth runtime emission of CycleReceipts (§17 v1 blueprint)
- Operator-only dress-rehearsal procedure (`docs/wpfa_dress_rehearsal_runbook_2026-05-18.md` — that procedure uses a synthetic operator-only key; it is NOT this ceremony)

# 2. Pre-ceremony prerequisites

Before SN-LLC executes signing:

1. **Methodology canonical version published.** The methodology document at `methodology_url` (per §17.4 + the draft skeleton at `docs/wpfa_methodology_v1_draft_2026-05-18.md`) is final, governance-ratified, and live at a stable URL.
2. **Coefficient measurements landed.** All `<TBD>` placeholders in the draft registry (`vault_shared/wpfa/coefficient_registry/draft_Q3_2026_unsigned.yaml`) are replaced with measured + ratified values.
3. **SN-LLC keypair held.** SN-LLC holds an Ed25519 signing keypair. The private key is in SN-LLC custody (HSM, hardware token, or operator-team-private key vault per SN-LLC governance posture). The public key is the value that white-glove operators will pin.
4. **Signing-key-id chosen.** SN-LLC picks a stable identifier for this signing key, conventionally `sn-llc-2026-q3` (matching the registry's `sn_llc_signing_key_id` field). Identifier scheme: `sn-llc-<year>-<quarter>` for quarterly publishes; `sn-llc-emergency-<date>` for out-of-cycle emergency publishes per §3.1 of methodology.
5. **Publication URL stood up.** SN-LLC's publication channel (e.g., GitHub release, signed S3 object, or other stable HTTPS URL) is configured to host the signed YAML and a parallel `.sig`-or-equivalent verification artifact.
6. **First-cycle target deployment identified.** At least one paid Beta operator-deployment is ready to run the pubkey-pin ceremony (`docs/wpfa_white_glove_pubkey_pin_runbook_2026-05-18.md`) once the inaugural registry publishes.

# 3. Canonical-JSON encoding (byte-for-byte critical)

The signature scheme mirrors v7.0.7 §6.1 router-template signing **byte-for-byte**:

- The registry is a JSON object with all fields **except** `sn_llc_signature_ed25519`.
- All keys are sorted alphabetically at every level.
- Separators: `(",", ":")` — no insignificant whitespace.
- UTF-8 encoding.
- Newline only after the closing brace (depending on tool; the verify side handles either).

In Python this is:

```python
import json
from pathlib import Path

def canonical_bytes(registry_dict: dict) -> bytes:
    # Strip the signature field
    payload = {k: v for k, v in registry_dict.items() if k != "sn_llc_signature_ed25519"}
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
```

**The YAML extension is a naming convention; the verifier loads via `json.loads` only** (per §2.14.4 + Cycle 2 RT-01/02/C2-04 fold-ins). YAML-only features (anchors, tags, comments, etc.) are rejected at load by the loader's JSON-strict parse. SN-LLC MUST publish JSON-loadable YAML — practically this means: scalars only, no anchors, no tags, no merge keys, no comments interleaved with data.

If SN-LLC's authoring tooling produces YAML with comments or anchors, run the file through `python -c 'import yaml, json, sys; print(json.dumps(yaml.safe_load(sys.stdin.read())))' < src.yaml > canonical.json` to normalize, then sign the canonical-JSON output and publish that.

# 4. Ceremony procedure

## 4.1 Stage the unsigned registry

Start from the draft template at `vault_shared/wpfa/coefficient_registry/draft_Q3_2026_unsigned.yaml`. Replace every `<TBD>` placeholder with the measured + ratified value. Replace:

- `schema_version` → `"1.0.0"` (semver per §2.14.3 invariant)
- `quarter` → e.g., `"Q3-2026"` (matches publication quarter)
- `published_at` → exact UTC ISO-8601 'Z' timestamp of publication
- `sn_llc_signature_ed25519` → leave empty string `""` for now
- `sn_llc_signing_key_id` → e.g., `"sn-llc-2026-q3"`
- `baseline_model_id` → ratified per methodology §3
- `methodology_url` → the canonical published URL
- `rollback_pointer` → `null` for inaugural; SHA3-512 hex of the prior registry version for subsequent publishes
- Every `entries[i].dollars_per_million_*` → measured value (smallest currency unit; A12)
- Every `entries[i].watt_hours_per_million_*` → measured value (micro-Wh; A12 extension)
- Every `entries[i].citation_url` → live URL captured at measurement
- Every `entries[i].measurement_date` → ISO date `YYYY-MM-DD` of measurement
- Every `entries[i].measurement_methodology_url` → live anchor within the canonical methodology document

Save as e.g., `inaugural_Q3_2026.unsigned.yaml`.

## 4.2 Compute canonical bytes

```bash
python3 -c '
import json, yaml, sys
d = yaml.safe_load(open("inaugural_Q3_2026.unsigned.yaml"))
payload = {k: v for k, v in d.items() if k != "sn_llc_signature_ed25519"}
out = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
sys.stdout.write(out)
' > inaugural_Q3_2026.canonical.json
```

Verify the canonical-JSON output is well-formed:

```bash
python3 -c 'import json; json.loads(open("inaugural_Q3_2026.canonical.json").read())'
```

(Clean exit = well-formed.)

## 4.3 Sign with SN-LLC private key

Using SN-LLC's Ed25519 signing tooling (HSM CLI, hardware-token CLI, or equivalent), sign the canonical-JSON bytes and capture the signature as 128-character lowercase hex.

Reference Python (illustrative — production signing uses SN-LLC's custody tooling):

```python
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

priv = Ed25519PrivateKey.from_private_bytes(<32-byte-private-key>)
canonical = open("inaugural_Q3_2026.canonical.json", "rb").read()
sig = priv.sign(canonical)
print(sig.hex())  # 128-char lowercase hex
```

## 4.4 Assemble the signed registry

Insert the 128-hex signature into the registry's `sn_llc_signature_ed25519` field:

```bash
python3 -c '
import yaml
d = yaml.safe_load(open("inaugural_Q3_2026.unsigned.yaml"))
d["sn_llc_signature_ed25519"] = "<128-hex-signature-from-step-4.3>"
print(yaml.safe_dump(d, sort_keys=True, allow_unicode=True))
' > inaugural_Q3_2026.signed.yaml
```

Verify the signed file is JSON-loadable (per §3):

```bash
python3 -c '
import json, yaml
d = yaml.safe_load(open("inaugural_Q3_2026.signed.yaml"))
print(json.dumps(d, sort_keys=True, separators=(",", ":"), ensure_ascii=False))
' > /dev/null
```

(Clean exit = JSON-loadable.)

## 4.5 Self-verify the signature

Re-canonicalize the signed file (stripping the signature field), then verify the signature against SN-LLC's public key:

```python
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.exceptions import InvalidSignature
import json, yaml

d = yaml.safe_load(open("inaugural_Q3_2026.signed.yaml"))
sig_hex = d["sn_llc_signature_ed25519"]
payload = {k: v for k, v in d.items() if k != "sn_llc_signature_ed25519"}
canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

pub = Ed25519PublicKey.from_public_bytes(<32-byte-public-key>)
try:
    pub.verify(bytes.fromhex(sig_hex), canonical)
    print("OK")
except InvalidSignature:
    print("FAILED — do not publish; recompute canonical and re-sign")
```

If verification fails, the canonicalization in §4.2 and the signing in §4.3 are out of sync. Recompute and re-sign. Do not publish a registry whose self-verify fails.

## 4.6 Compute SHA3-512 of the signed payload

For audit-trail purposes and for the rollback pointer that any future registry version will hold, compute:

```bash
python3 -c '
import hashlib
print(hashlib.sha3_512(open("inaugural_Q3_2026.signed.yaml", "rb").read()).hexdigest())
'
```

Record this 128-hex SHA3-512 digest in SN-LLC's publication ledger. Future emergency publishes that supersede this registry will carry this hash in their `rollback_pointer` field.

## 4.7 Publish

Publish `inaugural_Q3_2026.signed.yaml` at SN-LLC's stable publication URL. Convention: a content-addressable name including the quarter + SHA3 prefix:

```
https://sovereignnode.example/wpfa/coefficient_registry/Q3-2026.<sha3-12-prefix>.signed.yaml
```

Alongside, publish a publication ledger entry capturing:

- File name + URL
- SHA3-512 hash
- `sn_llc_signing_key_id`
- Published-at timestamp (matches the registry's `published_at` field)
- Methodology URL active at publication time

## 4.8 Publish the SN-LLC pubkey bundle

For first-time deployments, SN-LLC publishes the public key separately so operators can pin it via `tilth wpfa registry pin-pubkey` (see `docs/wpfa_white_glove_pubkey_pin_runbook_2026-05-18.md` §3.1). Bundle format:

```yaml
pubkey_hex: "<64-lowercase-hex>"
```

For rotations (subsequent quarters where the signing key changes), the bundle additionally carries a co-signature of the new pubkey bytes by the prior signing key, per the rotation procedure in the operator pubkey-pin runbook §4. SN-LLC computes this co-signature using the prior quarter's signing key over the raw new-pubkey bytes (32 bytes; not hex).

# 5. Verification chain summary

This ceremony establishes the verification chain Tilth deployments rely on:

1. SN-LLC private key signs the canonical-JSON-encoded registry → `sn_llc_signature_ed25519` field in the published YAML.
2. SN-LLC public key is published out-of-band to the operator.
3. Operator pins the SN-LLC public key at white-glove via `tilth wpfa registry pin-pubkey` (per the operator pubkey-pin runbook).
4. Tilth's Cycle Accountant calls `coefficient_registry.load_active()` which:
   - reads `vault_shared/wpfa/coefficient_registry/active.yaml`
   - reads `vault_shared/wpfa/sn_llc_pubkey.signed.yaml`
   - canonicalizes the registry (strip signature field, sorted keys, no whitespace)
   - verifies the signature against the pinned public key
   - fail-closes via `F-WPFA-COEFFICIENT-SIGNATURE-INVALID` on mismatch
5. Every CycleReceipt emission embeds the registry's SHA3-512 hash, so buyer-facing PDFs trace every claim back to this exact signed bytes.

If any link in the chain breaks, the gate fail-closes and no buyer-facing claim is emitted. This is the structural guarantee that "every dollar and watt-hour in this report links to a published coefficient + cycle_id + Logfire trace_id" (per §17.7.2 of the blueprint).

# 6. Emergency publishing (mid-quarter)

Per DPC-1 and §17 v7.0.7 §6.1, SN-LLC may publish an out-of-cycle registry within 7 days of a major vendor pricing or availability shock. Procedure:

1. Repeat §4 with `published_at` = the emergency-publication timestamp and `rollback_pointer` = the SHA3-512 hash of the registry being superseded.
2. Notify all known deployments via SN-LLC's notification channel (operator email list, status page, etc.) of the emergency-update event including the new SHA3 hash so operators can verify.
3. Operators run `tilth wpfa registry update --path <emergency-registry.signed.yaml>` against the new file.

There is no signing-key rotation in an emergency publish — same SN-LLC private key signs. If the emergency is itself a signing-key compromise, the procedure is a key-rotation publish (§7) not an emergency content publish.

# 7. Signing-key rotation

When SN-LLC rotates the signing keypair (planned cycle: new keypair per year minimum, more frequent at SN-LLC governance discretion; unplanned: compromise event):

1. SN-LLC generates a new Ed25519 keypair.
2. SN-LLC signs the **raw new-public-key bytes (32 bytes)** with the **prior signing key**. This is the rotation co-signature.
3. SN-LLC publishes a rotation bundle:

```yaml
pubkey_hex: "<new-64-hex-pubkey>"
co_signed_by_prior_signature_hex: "<128-hex-cosig>"
prior_signing_key_id: "<prior-sn-llc-key-id>"
new_signing_key_id: "<new-sn-llc-key-id>"
rotated_at_utc: "<UTC-iso-Z>"
```

4. The next published Coefficient Registry uses the new private key for signing and the new `sn_llc_signing_key_id`.
5. Operators run `tilth wpfa registry pin-pubkey --path <rotation-bundle.yaml> --co-signed-by-prior-signature-hex "<128-hex>" ...` per the rotation path in the operator pubkey-pin runbook §4.

Compromise rotations follow the same procedure but should be accompanied by SN-LLC's standard incident-disclosure communication. v0.1 single-client A1+A4 threat model allows hand-serialized rotation; v1.x adds the atomic `registry_rotation.lock` + 48h rotation lock-out gate per §17.15.1 forward-binding.

# 8. Audit trail

Every signing ceremony produces:

- One signed registry file at SN-LLC's publication URL.
- One ledger entry in SN-LLC's publication ledger (per §4.7).
- One SHA3-512 hash recorded for future rollback-pointer use.
- Operator-side: one `tilth wpfa registry update` ledger entry per deployment importing the signed registry.
- Operator-side: one CycleReceipt per cycle thereafter, each embedding the registry's SHA3-512 hash + the `sn_llc_signing_key_id` of the active signing key at emission time.

# 9. Failure modes specific to SN-LLC side

| Symptom | Cause | Recovery |
|---|---|---|
| Self-verify in §4.5 fails | Canonicalization in §4.2 used inconsistent encoding (whitespace, key ordering, charset) | Recompute canonical with the exact recipe in §3. Common gotchas: trailing newline, non-UTF-8 input, BOM, anchors-in-source-YAML producing inconsistent JSON output. |
| Operator deployment reports `F-WPFA-COEFFICIENT-SIGNATURE-INVALID` despite signed publication | Operator pinned a different pubkey than the one used to sign | Verify SN-LLC's published pubkey bundle matches the keypair used in §4.3. Verify operator obtained the bundle from SN-LLC's official channel. |
| Operator deployment reports `F-WPFA-COEFFICIENT-REGISTRY-UNSIGNED` | The published file's signature field is empty or wrong-length | Republish with the signature inserted (§4.4). |
| Operator deployment reports schema invariant failure | One of the §2.14.3 invariants is violated in the published file (e.g., `baseline_model_id` not present in `entries`, duplicate `model_id`, malformed URL) | Republish after fixing the schema. Schema invariants are non-negotiable. |
| Operator deployment reports `F-WPFA-MODEL-COEFFICIENT-MISSING` at runtime | A model Tilth routes to has no coefficient entry in the published registry | Add the missing entry in the next quarterly publish, OR publish an emergency mid-quarter update per §6. Until then, that model cannot be routed to. |

# 10. Cross-references

- Schema authority: `pipeline/blueprint/v0.1/section_02_v7_4_coefficient_registry_amendment.md`
- Loader implementation: `pipeline/vault/sub_kinds/coefficient_registry.py`
- Operator pubkey-pin runbook: `docs/wpfa_white_glove_pubkey_pin_runbook_2026-05-18.md`
- Methodology skeleton: `docs/wpfa_methodology_v1_draft_2026-05-18.md`
- Dress-rehearsal runbook (operator-only synthetic-key flow): `docs/wpfa_dress_rehearsal_runbook_2026-05-18.md`
- Trust mechanism precedent: `pipeline/architecture/v0.1/architecture_v7_0_7_amendment.md` §6.1 (router-template signing; byte-for-byte mirror)
