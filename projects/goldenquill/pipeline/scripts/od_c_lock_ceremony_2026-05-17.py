"""OD-C LOCK ceremony — §4 v2.x.7 + §0.5 v31 paired-commit (2026-05-17).

Reads the cards-publisher Ed25519 seed from env var ``OD_C_SEED`` (32-byte
hex). Verifies derived pubkey == pinned ``PINNED_PUBKEY_HEX``. Signs each
LOCK row's canonical-JSON payload (with sig + canonical_json_sha3_512
fields excluded). Appends two rows to ``pipeline/engineering/lock_history.v1.jsonl``.

Discipline:
  - One-shot script. Seed never echoed. Caller scrubs OD_C_SEED env var after.
  - Verify pubkey before signing.
  - Verify each signature round-trip post-sign.

Row shape mirrors OD-D rows 269-271 + OD-A rows 265-268:
  - signature_target_pubkey: vault_shared/cards/publisher_pubkey.signed.yaml
  - publisher_pubkey_ed25519_hex: pinned
  - canonical_json_sha3_512: SHA3-512 of canonical-JSON of row payload
    (sort_keys=True, separators=(",",":"), ensure_ascii=False; EXCLUDES the
    ``ed25519_signature`` + ``canonical_json_sha3_512`` fields themselves)
  - ed25519_signature: Ed25519 sign over the canonical-JSON bytes
  - sha3_512: SHA3-512 of on-disk file bytes at file_path

Note: For the sponsorship_corporate.yaml fix-in-place, per operator
directive the card's embedded ed25519_signature is NOT re-issued and NO
lock_history row is appended for the card. The card's bytes change; the
embedded sig goes stale until v0.2 first-wave loader graduation, when a
re-sign ceremony will fold the canonical-bytes update.
"""

from __future__ import annotations

import hashlib
import json
import os
import pathlib
import sys

from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from cryptography.hazmat.primitives import serialization

BASE = pathlib.Path(__file__).resolve().parent.parent.parent
LOCK_HISTORY = BASE / "pipeline" / "engineering" / "lock_history.v1.jsonl"

PINNED_PUBKEY_HEX = "0b1a0bbfa5ee9149af2c4e6153ed037dd03c0d562c94d3eaefeaf798e6f375bd"
CEREMONY_TIMESTAMP = "2026-05-17T05:30:00Z"

S4_AMENDMENT_PATH = "pipeline/blueprint/v0.1/section_04_v2_x_7_card_coupling_value_position_amendment.md"
S05_AMENDMENT_PATH = "pipeline/blueprint/v0.1/section_00_5_section_04_v2_x_7_amendment.md"
PREDICATE_PATH = "pipeline/logician/gates/f_cards_coupling_violation_extension.py"
SPONSORSHIP_PATH = "pipeline/cards/CLC/sponsorship_corporate.yaml"


def canonical_json_bytes(payload: dict) -> bytes:
    return json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def file_sha3_512_hex(rel_path: str) -> tuple[str, int]:
    p = BASE / rel_path
    data = p.read_bytes()
    return hashlib.sha3_512(data).hexdigest(), len(data)


def sign_row(*, sk: Ed25519PrivateKey, pubkey: Ed25519PublicKey, row_no_sig: dict) -> dict:
    """Return final row dict with canonical_json_sha3_512 + ed25519_signature populated.

    Sign convention: Ed25519 over canonical-JSON bytes of row payload with
    ed25519_signature + canonical_json_sha3_512 EXCLUDED.
    """
    payload = dict(row_no_sig)
    payload.pop("ed25519_signature", None)
    payload.pop("canonical_json_sha3_512", None)
    canon = canonical_json_bytes(payload)
    sha3_hex = hashlib.sha3_512(canon).hexdigest()
    sig = sk.sign(canon)
    sig_hex = sig.hex()
    # Round-trip verify
    pubkey.verify(sig, canon)
    final = dict(payload)
    final["canonical_json_sha3_512"] = sha3_hex
    final["ed25519_signature"] = sig_hex
    return final


def build_s4_v2_x_7_row(*, row_no: int) -> dict:
    sha3, fsize = file_sha3_512_hex(S4_AMENDMENT_PATH)
    pred_sha3, _ = file_sha3_512_hex(PREDICATE_PATH)
    return {
        "row": row_no,
        "lock_timestamp_utc": CEREMONY_TIMESTAMP,
        "lock_class": "blueprint",
        "lock_kind": "compound-paired-commit-double-member-1",
        "lock_cycle": "OD-C §4 v2.x.7 narrow-corrective amendment — F-CARDS-COUPLING-VIOLATION-EXTENSION predicate body graduated from NotImplementedError to LIVE three-layer scan (field-name registry + recursive value-position regex + matrix-card structural rule); sub-tag closure on row 562 extended in-place with 4 NEW value-position sub-tags + 3 GRADUATED matrix/field-name sub-tags (7 sub-tags total under existing failure-code owner per §4 v2.x.1 row-198 precedent)",
        "lock_mode": "COMPOUND-LOCK sibling-paired-commit-2 — paired with §0.5 v31 at the same lock_timestamp_utc per §6.17 Option-B. Self-LOCK per OD-C parent-handoff carve-out (predicate body + 36/36 PASS tests + 1965 PASS broader suite + 14-card backfill scan landed pre-ceremony; one operator-decision FIX-IN-PLACE surface — sponsorship_corporate.yaml display-name swap — resolved at ceremony time; post-fix backfill scan 14/14 PASS).",
        "module": "pipeline.blueprint.v0_1.section_04_v2_x_7_card_coupling_value_position_amendment",
        "file_path": S4_AMENDMENT_PATH,
        "file_size_bytes": fsize,
        "blueprint_section": S4_AMENDMENT_PATH,
        "blueprint_version": "§4 v2.x.7 LOCKED 2026-05-17",
        "amendment_class": "narrow-corrective sub-tag-extension + predicate-body graduation (no new top-level failure-code row; existing §0.5 v25 row 562 owner authoritative; mirrors §4 v2.x.1 row-198 precedent byte-for-byte)",
        "companion_lock_with": [S05_AMENDMENT_PATH],
        "compound_lock_with": [S05_AMENDMENT_PATH],
        "parent_lock_row": 228,
        "parent_handoff": "pipeline/handoffs/od_c_coupling_violation_extension_2026-05-16.md",
        "parent_completion": "pipeline/handoffs/od_c_completion_2026-05-16.md",
        "predecessor_amendments_chain": [
            "§4 v2.x card-hardening DRAFT (defines F-CARDS-COUPLING-VIOLATION-EXTENSION sig + FORBIDDEN_FIELD_REGISTRY constant at §4.X.1.7)",
            "§0.5 v25 row 562 LOCKED 2026-05-15T20:30:00Z (hosts the F-CARDS-COUPLING-VIOLATION-EXTENSION failure-code primitive)",
            "Cards Wave 2 LOCK ceremony rows 250-261 (12 cards LOCKED 2026-05-16T16:00:00Z) + §0.5 v29 paired-commit row 262",
            "§4 v2.x.6 router-dedup LOCK rows 263/264 at 2026-05-16T16:30:00Z (OD-5)",
            "OD-A admin_risk_register v2.4 compound LOCK rows 265-268 at 2026-05-16T20:28:58Z",
            "OD-D §18.11 v1.1 fold-in discipline + §18 main re-pin + §0.5 v30 triple paired-commit rows 269-271 at 2026-05-17T04:34:50Z",
        ],
        "companion_code_landed": {
            "predicate_body_module": PREDICATE_PATH,
            "predicate_body_sha3_512_hex": pred_sha3,
            "predicate_body_graduation": "NotImplementedError → LIVE three-layer scan (field-name registry + recursive value-position regex + matrix-card structural rule)",
            "tests_module": "tests/logician/gates/test_f_cards_coupling_violation_extension.py",
            "tests_count": "36/36 PASS focused; 1965 PASS + 7 environmental skips broader suite (tests/logician/gates/ + tests/cards/)",
        },
        "backfill_scan_outcome": {
            "scope": "14 LOCKed cards (Wave 1 + Wave 2)",
            "pre_ceremony": "13/14 PASS — 1 FAIL at pipeline/cards/CLC/sponsorship_corporate.yaml (track_b.underwriting_criteria[3].description + track_b.narrative_section_patterns[1].note carried literal TILTH-CLC-03)",
            "resolution": "Path-A FIX-IN-PLACE — display-name swap (Operating Capacity / Catalytic Change substituted for canonical TILTH-CLC-03 / TILTH-CLC-02 slugs; display names are NOT in the regex pattern set). Card embedded ed25519_signature NOT re-issued per operator carve-out (becomes stale; loader-time re-validation is v0.2 first-wave scope per architecture v7.0.11 §5).",
            "post_ceremony": "14/14 PASS clean",
            "post_fix_card_sha3_512_hex": file_sha3_512_hex(SPONSORSHIP_PATH)[0],
            "post_fix_card_size_bytes": file_sha3_512_hex(SPONSORSHIP_PATH)[1],
        },
        "amendment_status_transition": "DRAFT → LOCKED",
        "sub_tag_closure_under_row_562": [
            ".forbidden_field_name_for_axis (GRADUATED to LIVE)",
            ".value_literal_cic_slug (NEW)",
            ".value_literal_clc_slug (NEW)",
            ".value_literal_capital_logic_phrase (NEW)",
            ".value_literal_customer_identity_phrase (NEW)",
            ".matrix_binding_eligibility_true (GRADUATED to LIVE)",
            ".matrix_status_not_forward_compat_only (GRADUATED to LIVE)",
        ],
        "threat_severity_at_v0_1_v0_2": "LOW — bounded by v7 LOCKED A1+A4 (single-client + operator-trusted preflight); contributor-discipline drift class closure",
        "operator": "Josh Inklovich",
        "model_tier": "opus_4_7",
        "publisher_pubkey_ed25519_hex": PINNED_PUBKEY_HEX,
        "signature_target_pubkey": "vault_shared/cards/publisher_pubkey.signed.yaml",
        "sha3_512": sha3,
        "review_verdict": "Operator authorized self-LOCK per OD-C parent-handoff carve-out. Thesis-equivalent evidence layered: (a) 36/36 PASS tests, (b) 1965 PASS broader suite, (c) 14-card backfill scan PASS post-fix. Pre-flight cleared: file SHA3-512 fingerprints computed at ceremony time; pinned cards-publisher pubkey verified == 0b1a0bbf…6f375bd; lock_history tail clean (last logical row 271, OD-D §0.5 v30 paired-commit). Row shape mirrors OD-A / OD-D strong-trust posture field-for-field. Concurrent surfaces respected: §4 v2.x.6 runtime companion COMPLETED; OD-D LOCKED 271; OD-E pre-staged but fires AFTER this ceremony; OD-B (R-CARDS-ENUM-CANONICAL) parked for v0.2.",
        "verdict": "LOCKED — §4 v2.x.7 narrow-corrective amendment closing the design-time CIC × CLC coupling vector at the predicate-body layer; F-CARDS-COUPLING-VIOLATION-EXTENSION predicate body LIVE; sub-tag closure on row 562 extends in-place to 7 total; 14/14 backfill scan PASS post-FIX-IN-PLACE on sponsorship_corporate.yaml; sibling 1/2 of compound paired-commit at OD-C 2026-05-17 ceremony.",
    }


def build_s05_v31_row(*, row_no: int, s4_row_no: int) -> dict:
    sha3, fsize = file_sha3_512_hex(S05_AMENDMENT_PATH)
    return {
        "row": row_no,
        "lock_timestamp_utc": CEREMONY_TIMESTAMP,
        "lock_class": "blueprint-interface-index",
        "lock_kind": "compound-paired-commit-double-member-2",
        "lock_cycle": "OD-C §0.5 v31 paired-commit with §4 v2.x.7 — ONE marker row only (blueprint.amendment_anchor.s4_v2_x_7.v1; row 540 in §0.5 internal index)",
        "lock_mode": "COMPOUND-LOCK sibling-paired-commit-2 — paired with §4 v2.x.7 at the same lock_timestamp_utc per §6.17 Option-B. Marker-only sub-pattern (per §0.5 v31 §D): when a corrective amendment graduates an existing module's predicate body (rather than introducing a new dedicated module file), the §0.5 paired-commit lands ONE marker row only. f_cards_coupling_violation_extension.py already exists at row 562's defined_at per §0.5 v25 — no new enforcement-infrastructure row needed.",
        "module": "pipeline.blueprint.v0_1.section_00_5_section_04_v2_x_7_amendment",
        "file_path": S05_AMENDMENT_PATH,
        "file_size_bytes": fsize,
        "blueprint_section": S05_AMENDMENT_PATH,
        "blueprint_version": "§0.5 v31 LOCKED 2026-05-17",
        "amendment_class": "§0.5-paired-commit-narrow-corrective + marker-only sub-pattern (one marker row only; no schema rows; no enforcement-infrastructure rows; no failure-code rows; no AST-lint rows; sub-tag closure on row 562 extends in-place; precedent-extending §0.5 v16 + v26 + v30)",
        "companion_lock_with": [S4_AMENDMENT_PATH],
        "compound_lock_with": [S4_AMENDMENT_PATH],
        "parent_lock_row": 271,
        "blueprint_amendment_lock_row_parent": s4_row_no,
        "parent_handoff": "pipeline/handoffs/od_c_coupling_violation_extension_2026-05-16.md",
        "parent_completion": "pipeline/handoffs/od_c_completion_2026-05-16.md",
        "predecessor_amendments_chain": [
            "§0.5 v25 LOCKED 2026-05-15 row 228 (Wave 1 cards-cartridge primitive kind + row 562 F-CARDS-COUPLING-VIOLATION-EXTENSION failure-code primitive)",
            "§0.5 v26 LOCKED 2026-05-16 row 230 (§18 v1.1 paired-commit, marker-only)",
            "§0.5 v27 LOCKED 2026-05-16 row 233 (§4 v2.x.5 provider-boundary paired-commit)",
            "§0.5 v28 LOCKED 2026-05-16 row 237 (apolitical_dialect compound, runtime-live 552)",
            "§0.5 v29 paired-commit row 262 (Wave 2 signature_status unsigned→signed flip, runtime-live 538)",
            "§0.5 v30 LOCKED 2026-05-17 row 271 (OD-D §18.11 v1.1 documentation-only marker-only paired-commit, runtime-live 539)",
        ],
        "primitive_id_added": "blueprint.amendment_anchor.s4_v2_x_7.v1",
        "primitive_id_defined_at": S4_AMENDMENT_PATH,
        "primitive_id_kind": "marker",
        "primitive_id_seat_owner": "logician",
        "primitive_id_stability_tier": "STABLE",
        "primitive_id_parent_lock_version": "§4 v2.x.7",
        "row_delta": "+1 row (1 marker only; no enforcement-infrastructure; no schema; no failure-code; no ast-lint; no card-namespace)",
        "runtime_live_total_before": 539,
        "runtime_live_total_after": 540,
        "vocabulary_preservation": "the row's primitive_kind 'marker' resolves against the v5 + v6 + v17-v19 closed vocabulary",
        "seat_owner_attribute": "the row carries seat_owner: logician per §0.5 v20 RT-19/RT-C2-09 invariant (marker on a logician-family predicate-body graduation)",
        "sub_tag_closure_extension_on_row_562": "row 562 narrative sub-tag closure extends in-place with 4 NEW value-position sub-tags + 3 GRADUATED matrix/field-name sub-tags (7 total) per §4 v2.x.7 §3 + §0.5 v31 §B — annotation-only, NOT a row mutation per §4 v2.x.1 row-198 precedent",
        "cross_family_posture": "Self-LOCK per parent-handoff carve-out — Thesis-equivalent evidence (36/36 + 1965 + 14-card backfill PASS); F-INDEX-STALE PRE-gate clears at compound commit (the 1 new row must be present in the §0.5 index narrative).",
        "threat_severity_at_v0_1_v0_2": "LOW — bounded by v7 LOCKED A1+A4 (single-client + operator-trusted preflight); contributor-discipline drift class closure at the predicate-body layer",
        "operator": "Josh Inklovich",
        "model_tier": "opus_4_7",
        "publisher_pubkey_ed25519_hex": PINNED_PUBKEY_HEX,
        "signature_target_pubkey": "vault_shared/cards/publisher_pubkey.signed.yaml",
        "sha3_512": sha3,
        "review_verdict": "Operator authorized self-LOCK per documentation-only-equivalent carve-out (§4 v2.x.7 is narrow-corrective; this §0.5 paired-commit is marker-only). v31 header version verified pre-LOCK (sequencing: OD-D=v30 row 271, OD-C=v31 this row, next OD-E=v32). Pinned cards-publisher pubkey verified. Row shape mirrors OD-D row 271 / OD-A rows 265-268 field-for-field. Concurrent surfaces respected: OD-D LOCKED 271; OD-E pre-staged but fires AFTER this ceremony.",
        "verdict": "LOCKED — §0.5 v31 paired-commit; marker-only sub-pattern; +1 marker row (blueprint.amendment_anchor.s4_v2_x_7.v1, kind=marker, seat_owner=logician, stability_tier=STABLE); runtime-live total 539 → 540; sibling 2/2 of compound paired-commit at OD-C 2026-05-17 ceremony.",
    }


def main() -> int:
    seed_hex = os.environ.get("OD_C_SEED", "")
    if not seed_hex:
        print("ERROR: OD_C_SEED not set", file=sys.stderr)
        return 1
    try:
        seed = bytes.fromhex(seed_hex.strip())
    except ValueError:
        print("ERROR: OD_C_SEED is not valid hex", file=sys.stderr)
        return 1
    if len(seed) != 32:
        print(f"ERROR: seed must be 32 bytes; got {len(seed)}", file=sys.stderr)
        return 1
    sk = Ed25519PrivateKey.from_private_bytes(seed)
    pk = sk.public_key()
    pk_hex = pk.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    ).hex()
    if pk_hex != PINNED_PUBKEY_HEX:
        print(
            f"ERROR: derived pubkey {pk_hex[:16]}...{pk_hex[-16:]} != pinned {PINNED_PUBKEY_HEX[:16]}...{PINNED_PUBKEY_HEX[-16:]}",
            file=sys.stderr,
        )
        # Scrub
        del seed
        del sk
        return 2
    print(f"  pubkey verified == pinned 0b1a0bbf...6f375bd")

    # Determine next row number
    with LOCK_HISTORY.open() as f:
        max_row = 0
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            if isinstance(obj.get("row"), int):
                max_row = max(max_row, obj["row"])
    if max_row != 271:
        print(f"WARN: max existing row {max_row} != expected 271", file=sys.stderr)

    s4_row_no = max_row + 1
    s05_row_no = max_row + 2

    # Build + sign
    s4_unsigned = build_s4_v2_x_7_row(row_no=s4_row_no)
    s05_unsigned = build_s05_v31_row(row_no=s05_row_no, s4_row_no=s4_row_no)

    s4_final = sign_row(sk=sk, pubkey=pk, row_no_sig=s4_unsigned)
    s05_final = sign_row(sk=sk, pubkey=pk, row_no_sig=s05_unsigned)

    print(f"  row {s4_row_no}  §4 v2.x.7   sha3={s4_final['sha3_512'][:16]}...  canon_sha3={s4_final['canonical_json_sha3_512'][:16]}...  sig={s4_final['ed25519_signature'][:16]}...")
    print(f"  row {s05_row_no}  §0.5 v31    sha3={s05_final['sha3_512'][:16]}...  canon_sha3={s05_final['canonical_json_sha3_512'][:16]}...  sig={s05_final['ed25519_signature'][:16]}...")

    # Append (each row serialized as JSON one line)
    with LOCK_HISTORY.open("a") as f:
        f.write(json.dumps(s4_final) + "\n")
        f.write(json.dumps(s05_final) + "\n")
    print(f"  Appended 2 rows ({s4_row_no}, {s05_row_no}) to {LOCK_HISTORY.relative_to(BASE)}")

    # Scrub
    del seed
    del sk
    return 0


if __name__ == "__main__":
    sys.exit(main())
