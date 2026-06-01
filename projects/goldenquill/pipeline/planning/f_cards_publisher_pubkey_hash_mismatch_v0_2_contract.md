---
status: DRAFT contract — forward-binding to v0.2 first wave loader-realization
filed: 2026-05-15
parent_lock_rows: [226, 227, 228]  # Cards Wave 1 LOCK ceremony (CIC + CLC + §0.5 v25)
parent_locks:
  - pipeline/cards/CIC/food_systems.yaml                                                 # TILTH-CIC-01 LOCKED 2026-05-15 PM
  - pipeline/cards/CLC/operating_capacity.yaml                                            # TILTH-CLC-03 LOCKED 2026-05-15 PM
  - pipeline/blueprint/v0.1/section_00_5_section_18_cards_wave_1_paired_commit_amendment.md  # §0.5 v25
  - vault_shared/cards/publisher_pubkey.signed.yaml                                       # operator publisher signed-asset pinned at Wave 1 LOCK
  - pipeline/blueprint/v0.1/section_17_watts_per_funding_action.md                        # §17 v1 §6.1 router-template publisher-pubkey trust mechanism precedent (mirror byte-for-byte)
  - pipeline/blueprint/v0.1/section_16_reflection_packet.md                               # §16 v1.1 producer-pubkey signed-asset pattern precedent
companion_amendments_pending:
  - "§4 v2.x card-hardening amendment (DRAFT cluster pending L-005 round per project_card_system_v7_0_11_DRAFT.md) — adds F-CARDS-PUBLISHER-PUBKEY-HASH-MISMATCH as sub-tag of F-CARDS-SIGNATURE-INVALID; predicate body lands at v0.2 first wave loader-realization."
operator: Josh
---

# F-CARDS-PUBLISHER-PUBKEY-HASH-MISMATCH — v0.2 loader-realization contract

## Purpose

At v0.2 first wave loader-realization, the card loader (`pipeline/cards/loader.py`) verifies the integrity of the operator publisher pubkey signed-asset (`vault_shared/cards/publisher_pubkey.signed.yaml`) **before** consuming it as the verification target for `F-CARDS-SIGNATURE-INVALID`. The verification compares the on-disk asset's canonical-bytes SHA3-512 against a white-glove-pinned hash. Mismatch → fail-closed.

This sub-tag is the card-system analog of:

- `F-WPFA-COEFFICIENT-SIGNATURE-INVALID` (§17 v1 §6.1 — Coefficient Registry publisher-pubkey hash discipline)
- `F-PACKET-PRODUCER-PUBKEY-HASH-MISMATCH` (§16 v1.1 §16.v1.1.3 — Reflection Packet producer-pubkey hash discipline; forward-binding parallel)

Per Path B naming reconciliation, `F-CARDS-*` is its own orthogonal failure-code family. This sub-tag belongs to the cards family.

## Failure code primitive

```
F-CARDS-SIGNATURE-INVALID
  └── .publisher_pubkey_hash_mismatch   # this contract
```

Sub-tag of `F-CARDS-SIGNATURE-INVALID` rather than a new top-level primitive. Rationale: the failure-mode is one specific *cause* of "signature verification cannot proceed in good faith" rather than a distinct failure class. Mirrors §4 v2.x.1 row-198 sub-tag-extension pattern.

## Predicate body — v0.2 first wave loader-realization

Pseudocode (lands at `pipeline/logician/gates/f_cards_signature_invalid.py` via the F-CARDS-* family registration that ships with §4 v2.x card-hardening amendment):

```python
import hashlib
import re
from pathlib import Path

CANONICAL_BYTES_SIG_FIELD_PATTERN = re.compile(r'(publisher_signature_ed25519_hex: ")[^"]*(")')
CANONICAL_BYTES_HASH_FIELD_PATTERN = re.compile(r'(canonical_bytes_sha3_512_hex: ")[^"]*(")')


def verify_publisher_pubkey_hash(
    signed_asset_path: Path,
    white_glove_pinned_sha3_512_hex: str,
) -> tuple[bool, str | None]:
    """PRE-loader gate.

    Verify on-disk publisher_pubkey.signed.yaml has not drifted from the hash
    white-glove-pinned at deployment-manifest time.

    Returns (ok, reason_or_none). On (False, reason), the caller fails closed
    with F-CARDS-SIGNATURE-INVALID.publisher_pubkey_hash_mismatch.

    Mirrors the §17 v1 §6.1 Coefficient Registry verify-signature pattern
    byte-for-byte: read file → blank out signature + hash fields → recompute
    SHA3-512 → compare against pinned hash.
    """
    raw = signed_asset_path.read_text(encoding='utf-8')
    canonical_text = CANONICAL_BYTES_SIG_FIELD_PATTERN.sub(r'\1\2', raw)
    canonical_text = CANONICAL_BYTES_HASH_FIELD_PATTERN.sub(r'\1\2', canonical_text)
    canonical_bytes = canonical_text.encode('utf-8')
    computed_sha3 = hashlib.sha3_512(canonical_bytes).hexdigest()
    if computed_sha3 != white_glove_pinned_sha3_512_hex:
        return False, (
            f'F-CARDS-SIGNATURE-INVALID.publisher_pubkey_hash_mismatch — '
            f'computed SHA3-512 {computed_sha3[:32]}... does not match '
            f'white-glove-pinned hash {white_glove_pinned_sha3_512_hex[:32]}...'
        )
    return True, None
```

The function lives next to the existing F-CARDS-SIGNATURE-INVALID predicate body and is invoked **before** the predicate's signature-verification call against `publisher_pubkey_ed25519_hex` reads the asset. Order:

1. `verify_publisher_pubkey_hash(asset_path, pinned_hash)` → fail-closed if mismatch.
2. Parse asset → extract `publisher_pubkey_ed25519_hex`.
3. Verify card `_research_metadata.ed25519_signature` against canonical-JSON of card with `ed25519_signature: None` using that pubkey.

Without the hash-pre-check, an attacker who swaps the on-disk asset with a substitute pubkey would silently re-route signature verification through their key. The pre-check forces the deployment-manifest-pinned hash to be the source of truth.

## White-glove deployment manifest binding

At white-glove onboarding, the deployment manifest records (in operator-Ed25519-signed form, mirroring the v7.0.7 §6.1 router-template-update verification pattern):

```yaml
cards_publisher_signed_asset:
  path: "vault_shared/cards/publisher_pubkey.signed.yaml"
  canonical_bytes_sha3_512_hex: "<the pinned hash; copied from the asset's canonical_bytes_sha3_512_hex field at first-install time>"
  publisher_pubkey_ed25519_hex: "<32-byte raw hex>"
```

At Wave 1 LOCK ceremony (2026-05-15 PM, first install), the pinned hash IS:

```
112d105ba98727f773ac11f1312037f4342881c7003a3291ec54d18bc01557873e9d4bcd301f7a41953b5a2ef10f2782c193759115352390302d3ae38be0a872
```

The publisher pubkey IS:

```
0b1a0bbfa5ee9149af2c4e6153ed037dd03c0d562c94d3eaefeaf798e6f375bd
```

Loader behavior given these values:

- Asset SHA3-512 matches deployment-manifest pin → asset trusted → pubkey extracted → card signature verified.
- Asset SHA3-512 ≠ deployment-manifest pin → fail-closed with sub-tag `.publisher_pubkey_hash_mismatch`.

## Rotation path

Per §16 v1.1 + §17 v1 precedent, publisher pubkey rotation:

1. Operator generates new keypair offline.
2. New pubkey YAML is co-signed by **prior pubkey** (Trust-On-First-Use chain) via `prior_pubkey_signature_ed25519_hex` field.
3. Operator updates the white-glove deployment manifest with the new pinned hash.
4. Loader-realization at v0.2: when both old + new hashes can verify the asset's canonical bytes, the loader accepts the new pubkey AND verifies the `prior_pubkey_signature_ed25519_hex` against the old pubkey. Without that chain, rotation rejection is required to prevent pubkey-swap attacks.
5. HIGH-severity admin-risk ledger entry filed at rotation time per §16 v1.1 / §17 v1 / v7.0.7 §6.1 byte-for-byte.

The `verify_publisher_pubkey_hash` predicate body extends at v1.x rotation to accept (old_hash, new_hash) tuple when a rotation YAML carries `prior_pubkey_signature_ed25519_hex` non-null.

## Tests landing at v0.2 first wave loader-realization

Test file: `tests/cards/test_f_cards_signature_invalid_pubkey_hash_mismatch.py`

Binding test contract:

1. `test_signed_asset_unmodified_passes` — pinned hash matches on-disk asset hash → predicate returns (True, None).
2. `test_signed_asset_tampered_pubkey_fails_closed` — flip one hex char in `publisher_pubkey_ed25519_hex` → recompute hash → ≠ pinned hash → predicate returns (False, reason containing "publisher_pubkey_hash_mismatch").
3. `test_signed_asset_tampered_signature_does_not_fool_pre_check` — `publisher_signature_ed25519_hex` field is BLANKED in canonical form, so flipping it post-LOCK does NOT change the computed hash. Predicate returns (True, None) for hash check (signature-verify will catch this separately at the next step).
4. `test_signed_asset_tampered_hash_self_referential_fails` — operator tries to "fix" a tampered asset by recomputing canonical_bytes_sha3_512_hex in place. That field is BLANKED in canonical form, so the recomputed hash IS the true hash, but the pinned deployment-manifest hash is the old one → predicate returns (False, mismatch). Confirms the deployment-manifest pin is the source of truth.
5. `test_swapped_signed_asset_fails` — replace entire asset with a different pubkey asset (legitimately signed but by a different operator key). Hash will differ from pinned → fail-closed.
6. `test_rotation_chain_v1_x_horizon` — v1.x test surface: asset carries `prior_pubkey_signature_ed25519_hex` non-null AND new hash matches new white-glove-pinned hash; predicate accepts. (Marked `xfail` at v0.2; lands at v1.x rotation-amendment realization.)

## Integration with §18 §18.14 loader pseudocode

§18.14 currently shows:

```python
def load_card(path: str, environment: str) -> LoadedCard:
    card = read_yaml(path)
    validate_schema(card)
    require_lifecycle_block(card)
    reject_private_org_data(card)
    reject_cic_clc_coupling_violation(card)
    if environment == "production":
        require_operator_review_pass(card)
        require_cross_family_thesis_pass(card)
        require_signature(card)
        verify_signature(card)
    ...
```

At v0.2 first wave, `verify_signature(card)` decomposes to:

```python
def verify_signature(card):
    asset_path = Path('vault_shared/cards/publisher_pubkey.signed.yaml')
    pinned = load_white_glove_manifest()['cards_publisher_signed_asset']

    # Step 1 — F-CARDS-SIGNATURE-INVALID.publisher_pubkey_hash_mismatch
    ok, reason = verify_publisher_pubkey_hash(asset_path, pinned['canonical_bytes_sha3_512_hex'])
    if not ok:
        fail_closed(F_CARDS_SIGNATURE_INVALID, sub_tag='publisher_pubkey_hash_mismatch', reason=reason)

    # Step 2 — extract pubkey
    asset = read_yaml(asset_path)
    pubkey_hex = asset['publisher_pubkey_ed25519_hex']
    assert pubkey_hex == pinned['publisher_pubkey_ed25519_hex'], 'pubkey field disagrees with manifest pin'

    # Step 3 — F-CARDS-SIGNATURE-INVALID (top-level — card signature does not verify)
    sig_hex = card['_research_metadata']['ed25519_signature']
    card_copy = deepcopy(card)
    card_copy['_research_metadata']['ed25519_signature'] = None
    canonical_json = json.dumps(card_copy, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')
    try:
        Ed25519PublicKey.from_public_bytes(bytes.fromhex(pubkey_hex)).verify(bytes.fromhex(sig_hex), canonical_json)
    except InvalidSignature:
        fail_closed(F_CARDS_SIGNATURE_INVALID, reason='card signature does not verify against publisher pubkey')
```

## Verdict at landing

When the §4 v2.x card-hardening amendment LOCKs (currently DRAFT pending L-005 round per `project_card_system_v7_0_11_DRAFT.md`), this contract should be embedded as `F-CARDS-PUBLISHER-PUBKEY-HASH-MISMATCH` sub-tag spec for the F-CARDS-SIGNATURE-INVALID gate module. The predicate body MAY be authored at NotImplementedError stub at LOCK (mirrors §16 v1 18 BINDING NotImplementedError pattern) and graduate LIVE at v0.2 first wave loader-realization.

## Sibling-not-nested verification

- F-CARDS-* family does NOT cross to F-WPFA-* / F-PACKET-* / F-REPORT-* / F-FG-* / F-DATACOLLECTOR-* / F-ARCHIVIST-* / F-REFLECTION-* / F-CEDAR-* / F-CLASS-* (Path B naming reconciliation orthogonality preserved).
- The hash-discipline pattern is shared substrate; the gate code itself is per-family.
- AST-lint at v0.2 enforces cross-family-import ban on `f_cards_*.py`.
