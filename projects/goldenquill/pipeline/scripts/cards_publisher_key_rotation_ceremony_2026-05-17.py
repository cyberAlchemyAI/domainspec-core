"""Cards-publisher key rotation LOCK ceremony — compromise-class TOFU re-pin (2026-05-18).

Mirrors ``pipeline/scripts/od_e_fix_forward_ceremony_2026-05-17.py`` for shape,
seed-handling discipline, and atomic-append behavior. Fires the 2-row compound
paired-commit that retires the COMPROMISED cards-publisher pubkey
``0b1a0bbfa5ee9149af2c4e6153ed037dd03c0d562c94d3eaefeaf798e6f375bd`` and pins
the NEW pubkey ``c93f1881cbb7ff315b29f416c2f8bc16dc9e1d1576e743f63e577de992e41107``
per the Trust-On-First-Use re-pin path (``key_rotation_policy.md`` §4.1 step 5
second clause — old key under attacker control after exposure in Dispatch chat
2026-05-17).

Reads the NEW cards-publisher Ed25519 seed from env var
``CARDS_PUBLISHER_ROTATION_SEED`` (32-byte hex). Verifies derived pubkey ==
``PINNED_PUBKEY_HEX_NEW``. Fails closed on any mismatch.

Appends 2 rows to ``pipeline/engineering/lock_history.v1.jsonl`` at single
``CEREMONY_TIMESTAMP``:

  Row 280  key_rotation                cards.operator_publisher — TOFU re-pin (compromise-response)
  Row 281  blueprint-interface-index   §0.5 v33 paired-commit marker (runtime-live 541→542)

Discipline:
  - One-shot script. Seed never echoed. Caller scrubs env var after.
  - Verify derived pubkey == pinned NEW pubkey before ANY signing.
  - max_row guard (expects 279 — the OD-E post-ceremony housekeeping row).
  - Signs the YAML self-signature first (updates publisher_signature_ed25519_hex
    in vault_shared/cards/publisher_pubkey.signed.yaml so the trust anchor is
    internally consistent post-rotation), then signs the 2 lock_history rows.
  - Round-trip verifies each signature post-sign.
  - Atomic write via tmp + os.replace for both YAML and lock_history.
  - Exit codes:
      0  success — rows 280-281 appended; YAML self-sig filled; round-trip PASS
      1  bad seed (missing env var / not hex / wrong length)
      2  derived pubkey != pinned NEW pubkey (operator pasted wrong seed)
      3  max_row guard failed (lock_history not at expected 279)
      4  YAML/canonical/signature consistency check failed post-update

Row shapes mirror artifact 03 §3.1 (key_rotation) + §3.2 (§0.5 v33 paired-commit).
"""

from __future__ import annotations

import hashlib
import json
import os
import pathlib
import sys
import tempfile

import yaml

from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from cryptography.hazmat.primitives import serialization

BASE = pathlib.Path(__file__).resolve().parent.parent.parent
LOCK_HISTORY = BASE / "pipeline" / "engineering" / "lock_history.v1.jsonl"
PUBKEY_YAML = BASE / "vault_shared" / "cards" / "publisher_pubkey.signed.yaml"
S05_V33_AMENDMENT = BASE / "pipeline" / "blueprint" / "v0.1" / "section_00_5_cards_publisher_rotation_amendment.md"

# ─────────────────────────────────────────────────────────────────
# Rotation constants
# ─────────────────────────────────────────────────────────────────
PINNED_PUBKEY_HEX_OLD = "0b1a0bbfa5ee9149af2c4e6153ed037dd03c0d562c94d3eaefeaf798e6f375bd"
PINNED_PUBKEY_HEX_NEW = "c93f1881cbb7ff315b29f416c2f8bc16dc9e1d1576e743f63e577de992e41107"
CEREMONY_TIMESTAMP = "2026-05-18T00:00:00Z"
EXPECTED_MAX_ROW = 279

ROTATION_HANDOFF = "pipeline/handoffs/cards_publisher_key_rotation_2026-05-17/03_key_rotation_paired_commit.md"
COMPROMISE_RECORD = "pipeline/handoffs/cards_publisher_key_rotation_2026-05-17/05_old_key_compromise_record.md"
RUNBOOK_REF = "vault_shared/key_rotation_policy.md §4 (compromise-response runbook)"

PREDECESSOR_CHAIN = [
    "Wave 1 cards LOCK ceremony 2026-05-15T20:00:00Z (pinned compromised pubkey 0b1a0bbf...6f375bd via TOFU self-signed asset)",
    "Wave 2 LOCK ceremony rows 250-261 (12 cards LOCKED 2026-05-16T16:00:00Z) + §0.5 v29 paired-commit row 262",
    "§4 v2.x.6 router dedup LOCK rows 263/264 at 2026-05-16T16:30:00Z (OD-5)",
    "OD-A admin_risk_register v2.4 compound LOCK rows 265-268 at 2026-05-16T20:28:58Z",
    "OD-D §18.11 v1.1 fold-in discipline + §18 main re-pin + §0.5 v30 triple paired-commit rows 269-271 at 2026-05-17T04:34:50Z",
    "OD-C §4 v2.x.7 + §0.5 v31 narrow-corrective compound LOCK rows 272-273 at 2026-05-17T05:30:00Z",
    "OD-E §18.6 v2 dual-track restructure compound LOCK rows 274-278 at 2026-05-17T16:00:00Z (signed with prior-now-compromised pubkey; rows remain audit-valid per retroactive_validity_preservation)",
    "OD-E post-ceremony status-flip housekeeping supersession row 279 at 2026-05-17T16:01:00Z",
    "Dispatch chat seed exposure 2026-05-17 PM (incident discovery)",
    f"Cards-publisher rotation ceremony (this row) at {CEREMONY_TIMESTAMP}",
]


# ─── canonical-bytes recipes ───
def yaml_canonical_bytes(data: dict) -> bytes:
    """YAML canonical-bytes recipe (mirrors loader / artifact 02 §Verification).

    data MUST already have publisher_signature_ed25519_hex AND
    canonical_bytes_sha3_512_hex removed.
    """
    return yaml.safe_dump(data, sort_keys=True, default_flow_style=False).encode("utf-8")


def row_canonical_bytes(row: dict) -> bytes:
    """lock_history-row canonical-bytes recipe (mirrors OD-E ceremony script)."""
    payload = dict(row)
    payload.pop("ed25519_signature", None)
    payload.pop("canonical_json_sha3_512", None)
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


# ─── atomic write ───
def atomic_write_text(path: pathlib.Path, text: str) -> None:
    """Write text to path atomically via tmp + os.replace."""
    fd, tmp = tempfile.mkstemp(
        dir=str(path.parent),
        prefix=path.name + ".tmp.",
    )
    try:
        with os.fdopen(fd, "w") as f:
            f.write(text)
        os.replace(tmp, str(path))
    except Exception:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def atomic_append_lines(path: pathlib.Path, lines: list[str]) -> None:
    """Append lines (each must end with \\n) to path atomically.

    Reads existing contents, concatenates, writes via tmp + os.replace.
    """
    existing = path.read_bytes() if path.exists() else b""
    suffix = ("".join(lines)).encode("utf-8")
    fd, tmp = tempfile.mkstemp(
        dir=str(path.parent),
        prefix=path.name + ".tmp.",
    )
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(existing)
            f.write(suffix)
        os.replace(tmp, str(path))
    except Exception:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


# ─── signing ───
def sign_row(*, sk: Ed25519PrivateKey, pubkey: Ed25519PublicKey, row_no_sig: dict) -> dict:
    canon = row_canonical_bytes(row_no_sig)
    sha3_hex = hashlib.sha3_512(canon).hexdigest()
    sig = sk.sign(canon)
    pubkey.verify(sig, canon)  # round-trip
    final = dict(row_no_sig)
    final.pop("ed25519_signature", None)
    final.pop("canonical_json_sha3_512", None)
    final["canonical_json_sha3_512"] = sha3_hex
    final["ed25519_signature"] = sig.hex()
    return final


# ─── YAML self-signature update ───
def update_pubkey_yaml_self_signature(*, sk: Ed25519PrivateKey, pubkey: Ed25519PublicKey) -> int:
    """Read PUBKEY_YAML, compute canonical bytes, sign with sk, write back.

    Returns 0 on success, 4 on consistency-check failure.
    """
    raw = PUBKEY_YAML.read_text()
    data = yaml.safe_load(raw)

    # Verify pinned pubkey matches NEW
    pinned_yaml_pubkey = data.get("publisher_pubkey_ed25519_hex", "")
    if pinned_yaml_pubkey != PINNED_PUBKEY_HEX_NEW:
        print(
            f"ERROR: YAML publisher_pubkey_ed25519_hex = {pinned_yaml_pubkey[:16]}...{pinned_yaml_pubkey[-16:]} "
            f"!= expected NEW pubkey {PINNED_PUBKEY_HEX_NEW[:16]}...{PINNED_PUBKEY_HEX_NEW[-16:]}",
            file=sys.stderr,
        )
        return 4

    # Compute canonical bytes (with sig + hash fields stripped)
    clone = dict(data)
    clone.pop("publisher_signature_ed25519_hex", None)
    clone.pop("canonical_bytes_sha3_512_hex", None)
    canon = yaml_canonical_bytes(clone)
    canon_sha3 = hashlib.sha3_512(canon).hexdigest()

    # Verify the pinned canonical_bytes_sha3_512_hex (if it's a real hex value) matches
    pinned_hash = data.get("canonical_bytes_sha3_512_hex", "")
    if len(pinned_hash) == 128 and all(c in "0123456789abcdef" for c in pinned_hash):
        if pinned_hash != canon_sha3:
            print(
                f"ERROR: YAML canonical_bytes_sha3_512_hex = {pinned_hash[:32]}... "
                f"!= recomputed {canon_sha3[:32]}... — YAML body changed since pre-stage; "
                f"re-pin canonical_bytes_sha3_512_hex before re-running.",
                file=sys.stderr,
            )
            return 4
        print(f"  YAML canonical_bytes_sha3_512_hex verified: {canon_sha3[:32]}...")
    else:
        # Pinned hash was a placeholder; fill it now
        print(f"  YAML canonical_bytes_sha3_512_hex pinned: {canon_sha3[:32]}...")

    # Sign canonical bytes
    sig = sk.sign(canon)
    pubkey.verify(sig, canon)  # round-trip
    sig_hex = sig.hex()

    # Patch the raw file text: replace the placeholder + pinned_hash lines.
    # We use a text-level replacement so we preserve the file's comments.
    new_sig_line = f'publisher_signature_ed25519_hex: "{sig_hex}"'
    new_hash_line = f'canonical_bytes_sha3_512_hex: "{canon_sha3}"'

    updated = raw
    # Replace any existing publisher_signature_ed25519_hex line
    lines_out = []
    sig_patched = False
    hash_patched = False
    for line in updated.splitlines(keepends=True):
        stripped = line.lstrip()
        if stripped.startswith("publisher_signature_ed25519_hex:"):
            indent = line[: len(line) - len(stripped)]
            lines_out.append(f"{indent}{new_sig_line}\n")
            sig_patched = True
        elif stripped.startswith("canonical_bytes_sha3_512_hex:"):
            indent = line[: len(line) - len(stripped)]
            lines_out.append(f"{indent}{new_hash_line}\n")
            hash_patched = True
        else:
            lines_out.append(line)
    if not (sig_patched and hash_patched):
        print(
            f"ERROR: YAML self-sig patch did not find both publisher_signature_ed25519_hex "
            f"and canonical_bytes_sha3_512_hex lines (sig_patched={sig_patched}, "
            f"hash_patched={hash_patched})",
            file=sys.stderr,
        )
        return 4

    atomic_write_text(PUBKEY_YAML, "".join(lines_out))

    # Post-write round-trip verify
    rdata = yaml.safe_load(PUBKEY_YAML.read_text())
    rclone = dict(rdata)
    rclone.pop("publisher_signature_ed25519_hex", None)
    rclone.pop("canonical_bytes_sha3_512_hex", None)
    rcanon = yaml_canonical_bytes(rclone)
    rcanon_sha3 = hashlib.sha3_512(rcanon).hexdigest()
    if rcanon_sha3 != rdata["canonical_bytes_sha3_512_hex"]:
        print(
            f"ERROR: post-write canonical hash mismatch ({rcanon_sha3[:32]}... vs {rdata['canonical_bytes_sha3_512_hex'][:32]}...)",
            file=sys.stderr,
        )
        return 4
    try:
        pubkey.verify(bytes.fromhex(rdata["publisher_signature_ed25519_hex"]), rcanon)
    except Exception as exc:  # noqa: BLE001
        print(f"ERROR: post-write self-signature verify FAILED — {exc}", file=sys.stderr)
        return 4
    print("  YAML self-signature post-write round-trip: PASS")
    return 0


# ─── row builders ───
def build_row_280_key_rotation() -> dict:
    """Row 280 — key_rotation lock_class for the cards-publisher TOFU re-pin."""
    yaml_sha3, yaml_size = file_sha3_512_hex(str(PUBKEY_YAML.relative_to(BASE)))
    return {
        "row": 280,
        "lock_timestamp_utc": CEREMONY_TIMESTAMP,
        "lock_class": "key_rotation",
        "lock_kind": "compound-paired-commit-two-member-1",
        "lock_cycle": (
            f"Cards-publisher compromise-class rotation — TOFU re-pin per "
            f"key_rotation_policy.md §4.1 step 5 second clause (old key under attacker "
            f"control). Old pubkey {PINNED_PUBKEY_HEX_OLD[:8]}...{PINNED_PUBKEY_HEX_OLD[-7:]} "
            f"marked COMPROMISED-RETIRED per {COMPROMISE_RECORD}. New pubkey "
            f"{PINNED_PUBKEY_HEX_NEW[:8]}...{PINNED_PUBKEY_HEX_NEW[-7:]} takes effect at "
            f"this row's lock_timestamp_utc."
        ),
        "lock_mode": (
            "COMPOUND-LOCK sibling-paired-commit-2 — paired with §0.5 v33 paired-commit "
            f"marker row 281 at the same lock_timestamp_utc per §6.17 Option-B. "
            f"Compromise-response runbook executed per key_rotation_policy.md §4 "
            f"(HIGH-severity admin-risk ledger anchor + revoke + generate-new + re-sign + "
            f"lock_history append + notify-consumers + close-ledger). This row is the "
            f"lock_history-layer audit anchor for the rotation event."
        ),
        "module": "cards.operator_publisher",
        "file_path": str(PUBKEY_YAML.relative_to(BASE)),
        "rotation_class": "compromise_response",
        "rotation_trigger": "Cards-publisher Ed25519 seed exposed in Dispatch chat 2026-05-17",
        "rotation_trigger_runbook_ref": RUNBOOK_REF,
        "old_pubkey_ed25519_hex": PINNED_PUBKEY_HEX_OLD,
        "old_pubkey_status": f"COMPROMISED-RETIRED 2026-05-17 — see {COMPROMISE_RECORD}",
        "new_pubkey_ed25519_hex": PINNED_PUBKEY_HEX_NEW,
        "new_pubkey_pinned_at_utc": CEREMONY_TIMESTAMP,
        "tofu_repin_path": (
            "key_rotation_policy.md §4.1 step 5 second clause — prior key under attacker "
            "control; SKIP co-sign; operator re-pins new pubkey directly"
        ),
        "prior_pubkey_cosign_signature_ed25519_hex": None,
        "prior_pubkey_cosign_skip_reason": (
            "Compromise-class rotation — old key in attacker hands; co-sign by old key "
            "would be attacker-controlled signature and would not establish trust"
        ),
        "parent_lock_row": 0,
        "parent_lock_row_note": (
            "Foundational rotation — no prior key_rotation row in lock_history; this is "
            "the first rotation event for cards.operator_publisher since Wave 1 LOCK "
            "ceremony 2026-05-15 PM"
        ),
        "parent_handoff": ROTATION_HANDOFF,
        "retroactive_validity_preservation": (
            "All lock_history rows 226-279 signed with the prior key "
            f"{PINNED_PUBKEY_HEX_OLD[:8]}...{PINNED_PUBKEY_HEX_OLD[-7:]} remain audit-valid: "
            "at the time of signing, the prior key was not yet exposed and signature "
            "verification against the prior pubkey continues to succeed for any party who "
            "recorded the prior pubkey before its retirement. This rotation prevents "
            "FUTURE use of the compromised seed but does not retroactively invalidate "
            "prior signatures. The retired pubkey is preserved in the compromise record "
            "and on this row's old_pubkey_ed25519_hex field for ongoing verification of "
            "historical rows."
        ),
        "consumer_notification": (
            "Cowork session (this), Dispatch session (sibling AI), operator's own audit "
            "trail. No external buyer-facing artifacts signed by cards-publisher exist as "
            "of rotation — buyer-facing PDF emission is operator-attestation-signed per "
            "§17 WPFA and §4 v2.x.y.1 Reflection Packet, not cards-publisher."
        ),
        "admin_risk_ledger_anchor": (
            "pipeline/engineering/admin_risk_ledger.v1.jsonl — HIGH-severity entry filed "
            "at exposure discovery + the rotation-completion update on this row"
        ),
        "predecessor_amendments_chain": PREDECESSOR_CHAIN,
        "threat_severity_at_v0_1_v0_2": (
            "P0 audit-integrity (the compromised key could be used by any party with "
            "Dispatch chat access to forge cards-publisher signatures on lock_history "
            "rows, card supersession claims, and future card LOCKs; rotation closes the "
            "exposure window structurally)"
        ),
        "operator": "Josh Inklovich",
        "model_tier": "opus_4_7",
        "publisher_pubkey_ed25519_hex": PINNED_PUBKEY_HEX_NEW,
        "signature_target_pubkey": "vault_shared/cards/publisher_pubkey.signed.yaml (post-rotation update)",
        "sha3_512": yaml_sha3,
        "file_size_bytes": yaml_size,
        "review_verdict": (
            "Operator authorized compromise-class rotation per key_rotation_policy.md §4 "
            "runbook at exposure discovery 2026-05-17. TOFU re-pin path per §4.1 step 5 "
            "second clause (old key under attacker control). NEW pubkey verified against "
            "operator's stashed seed via derived-pubkey check at ceremony fire time. "
            "max_row guard cleared (=279). YAML self-signature filled + round-trip "
            "verified pre-row-sign. Pre-OD-E sequencing per rotate-first discipline."
        ),
        "verdict": (
            f"LOCKED — Cards-publisher key rotated from COMPROMISED-RETIRED "
            f"{PINNED_PUBKEY_HEX_OLD[:8]}...{PINNED_PUBKEY_HEX_OLD[-7:]} to "
            f"{PINNED_PUBKEY_HEX_NEW[:8]}...{PINNED_PUBKEY_HEX_NEW[-7:]}; TOFU re-pin per "
            f"§4.1 step 5 second clause; row 1/2 of compound paired-commit at "
            f"{CEREMONY_TIMESTAMP}."
        ),
    }


def build_row_281_s05_v33() -> dict:
    """Row 281 — §0.5 v33 paired-commit marker."""
    amendment_rel = str(S05_V33_AMENDMENT.relative_to(BASE))
    amendment_sha3, amendment_size = file_sha3_512_hex(amendment_rel)
    return {
        "row": 281,
        "lock_timestamp_utc": CEREMONY_TIMESTAMP,
        "lock_class": "blueprint-interface-index",
        "lock_kind": "compound-paired-commit-two-member-2",
        "lock_cycle": (
            "Cards-publisher rotation §0.5 v33 paired-commit with key_rotation row 280 — "
            "ONE marker row only (blueprint.amendment_anchor.cards_publisher_rotation.v1; "
            "row 542 in §0.5 internal index). Mirrors prior §0.5-paired-commit pattern "
            "from OD-D (v30 row 271) / OD-C (v31 row 273) / OD-E (v32 row 275)."
        ),
        "lock_mode": (
            "COMPOUND-LOCK sibling-paired-commit-2 — paired with key_rotation row 280 at "
            "the same lock_timestamp_utc per §6.17 Option-B. Marker-only sub-pattern per "
            "§0.5 v31 §D + §0.5 v32 (extended to compromise-response-class scope at this "
            "row): when a rotation ceremony introduces no new failure-code/schema/AST-lint "
            "surface, the §0.5 paired-commit lands ONE marker row only."
        ),
        "module": "pipeline.blueprint.v0_1.section_00_5_cards_publisher_rotation_amendment",
        "file_path": amendment_rel,
        "file_size_bytes": amendment_size,
        "blueprint_section": amendment_rel,
        "blueprint_version": f"§0.5 v33 LOCKED {CEREMONY_TIMESTAMP}",
        "amendment_class": (
            "§0.5-paired-commit-compromise-response + marker-only sub-pattern (one marker "
            "row only; no schema rows; no enforcement-infrastructure rows; no failure-code "
            "rows; no AST-lint rows; no vocabulary kind extension; precedent-extending "
            "§0.5 v16 + v26 + v30 + v31 + v32; compromise-response-class scope at "
            "companion key_rotation row 280)"
        ),
        "companion_lock_with": [f"key_rotation row 280 at lock_timestamp_utc {CEREMONY_TIMESTAMP}"],
        "compound_lock_with": [str(PUBKEY_YAML.relative_to(BASE))],
        "parent_lock_row": 275,
        "blueprint_amendment_parent_chain": [271, 273, 275],
        "parent_handoff": ROTATION_HANDOFF,
        "predecessor_amendments_chain": [
            "OD-D §0.5 v30 paired-commit row 271 at 2026-05-17T04:34:50Z",
            "OD-C §0.5 v31 paired-commit row 273 at 2026-05-17T05:30:00Z",
            "OD-E §0.5 v32 paired-commit row 275 at 2026-05-17T16:00:00Z",
            f"Cards-publisher rotation §0.5 v33 paired-commit (this row) at {CEREMONY_TIMESTAMP}",
        ],
        "primitive_id_added": "blueprint.amendment_anchor.cards_publisher_rotation.v1",
        "primitive_id_defined_at": amendment_rel,
        "primitive_id_kind": "marker",
        "primitive_id_seat_owner": "cards",
        "primitive_id_stability_tier": "STABLE",
        "primitive_id_parent_lock_version": "cards-publisher TOFU re-pin (key_rotation_policy.md §4.1 step 5 second clause)",
        "row_delta": "+1 row (1 marker only; no enforcement-infrastructure; no schema; no failure-code; no ast-lint; no card-namespace)",
        "runtime_live_total_before": 541,
        "runtime_live_total_after": 542,
        "vocabulary_preservation": "the row's primitive_kind 'marker' resolves against the v5 + v6 + v17-v19 closed vocabulary",
        "seat_owner_attribute": "the row carries seat_owner: cards per §0.5 v20 RT-19/RT-C2-09 invariant",
        "cross_family_posture": (
            "Self-LOCK per compromise-response carve-out — operator-authorized rotation "
            "per key_rotation_policy.md §4 runbook. L-005 Thesis dispatch waived under "
            "compromise-response-class scope (no new enforcement teeth; audit-trail anchor "
            "only for the rotation event). The cross-family rigor for cards changes lives "
            "in normal cards-LOCK ceremonies; this is a key-management event riding the "
            "§6.17 Option-B paired-commit primitive."
        ),
        "threat_severity_at_v0_1_v0_2": (
            "LOW — §0.5 marker row at the rotation-event audit-anchor layer; no v0.1 "
            "runtime impact (the runtime impact lives in row 280's pubkey re-pin + the "
            "publisher_pubkey.signed.yaml update)"
        ),
        "operator": "Josh Inklovich",
        "model_tier": "opus_4_7",
        "publisher_pubkey_ed25519_hex": PINNED_PUBKEY_HEX_NEW,
        "signature_target_pubkey": "vault_shared/cards/publisher_pubkey.signed.yaml (post-rotation update)",
        "sha3_512": amendment_sha3,
        "review_verdict": (
            "Operator authorized §0.5 v33 paired-commit self-LOCK per compromise-response "
            "carve-out. Sequencing verified: OD-E = §0.5 v32 row 275 → cards-publisher "
            f"rotation = §0.5 v33 (this row). The next §0.5 version (v34) will be paired "
            f"with the OD-E fix-forward ceremony. NEW pubkey verified == "
            f"{PINNED_PUBKEY_HEX_NEW[:8]}...{PINNED_PUBKEY_HEX_NEW[-7:]} via derived-"
            f"pubkey check at ceremony fire time."
        ),
        "verdict": (
            "LOCKED — §0.5 v33 cards-publisher-rotation paired-commit; marker-only "
            "sub-pattern; +1 marker row (blueprint.amendment_anchor.cards_publisher_rotation.v1, "
            "kind=marker, seat_owner=cards, stability_tier=STABLE); runtime-live total "
            f"541 → 542; sibling 2/2 of cards-publisher rotation compound LOCK "
            f"{CEREMONY_TIMESTAMP}."
        ),
    }


# ─── main ───
def main() -> int:
    print(f"Cards-publisher rotation ceremony — {CEREMONY_TIMESTAMP}")
    print(f"  base: {BASE}")
    print(f"  lock_history: {LOCK_HISTORY.relative_to(BASE)}")
    print(f"  pubkey YAML:  {PUBKEY_YAML.relative_to(BASE)}")
    print(f"  §0.5 v33 amendment: {S05_V33_AMENDMENT.relative_to(BASE)}")
    print()

    # 0. Pre-flight: required files exist
    for required in (PUBKEY_YAML, LOCK_HISTORY, S05_V33_AMENDMENT):
        if not required.exists():
            print(f"ERROR: required file missing: {required.relative_to(BASE)}", file=sys.stderr)
            return 4

    # 1. Read seed from env
    seed_hex = os.environ.get("CARDS_PUBLISHER_ROTATION_SEED", "")
    if not seed_hex:
        print("ERROR: CARDS_PUBLISHER_ROTATION_SEED env var not set", file=sys.stderr)
        return 1
    try:
        seed = bytes.fromhex(seed_hex.strip())
    except ValueError:
        print("ERROR: CARDS_PUBLISHER_ROTATION_SEED is not valid hex", file=sys.stderr)
        return 1
    if len(seed) != 32:
        print(f"ERROR: seed must be 32 bytes; got {len(seed)}", file=sys.stderr)
        return 1

    # 2. Derive pubkey + check against pinned NEW
    sk = Ed25519PrivateKey.from_private_bytes(seed)
    pk = sk.public_key()
    pk_hex = pk.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    ).hex()
    if pk_hex != PINNED_PUBKEY_HEX_NEW:
        print(
            f"ERROR: derived pubkey {pk_hex[:16]}...{pk_hex[-16:]} != pinned NEW "
            f"{PINNED_PUBKEY_HEX_NEW[:16]}...{PINNED_PUBKEY_HEX_NEW[-16:]}. "
            f"Re-check that _private/cards_publisher_privkey_2026-05-17.txt holds the "
            f"NEW cards-publisher seed (matching pubkey "
            f"{PINNED_PUBKEY_HEX_NEW[:8]}...{PINNED_PUBKEY_HEX_NEW[-7:]}).",
            file=sys.stderr,
        )
        del seed
        del sk
        return 2
    print(f"  pubkey verified == pinned NEW {PINNED_PUBKEY_HEX_NEW[:8]}...{PINNED_PUBKEY_HEX_NEW[-7:]}")
    print()

    # 3. max_row guard
    with LOCK_HISTORY.open() as f:
        max_row = 0
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            if isinstance(obj.get("row"), int):
                max_row = max(max_row, obj["row"])
    if max_row != EXPECTED_MAX_ROW:
        print(
            f"ERROR: max existing row {max_row} != expected {EXPECTED_MAX_ROW} — abort to "
            f"avoid race with concurrent ceremony",
            file=sys.stderr,
        )
        del seed
        del sk
        return 3
    print(f"  max_row guard PASS (max_row={max_row})")
    print()

    # 4. YAML self-signature update (so the trust anchor is internally consistent
    #    BEFORE we sign the rows that reference its post-update sha3_512)
    print("Updating publisher_pubkey.signed.yaml self-signature...")
    rc = update_pubkey_yaml_self_signature(sk=sk, pubkey=pk)
    if rc != 0:
        del seed
        del sk
        return rc
    print()

    # 5. Build + sign 2 rows
    print("Building and signing rows...")
    rows_unsigned = [build_row_280_key_rotation(), build_row_281_s05_v33()]
    rows_signed: list[dict] = []
    for r in rows_unsigned:
        signed = sign_row(sk=sk, pubkey=pk, row_no_sig=r)
        rows_signed.append(signed)
        rno = signed["row"]
        klass = signed["lock_class"]
        slug = signed.get("module", "-")
        canon_sha3 = signed["canonical_json_sha3_512"]
        sig = signed["ed25519_signature"]
        print(
            f"  row {rno}  {klass:28s}  module={slug:64s}  "
            f"canon_sha3={canon_sha3[:16]}...  sig={sig[:16]}..."
        )
    print()

    # 6. Atomic append
    lines = [json.dumps(r) + "\n" for r in rows_signed]
    atomic_append_lines(LOCK_HISTORY, lines)
    print(f"  Appended 2 rows (280, 281) to {LOCK_HISTORY.relative_to(BASE)}")

    # 7. Post-write round-trip verify
    print()
    print("Post-write round-trip verification...")
    written_rows = [
        json.loads(l)
        for l in LOCK_HISTORY.read_text().splitlines()
        if l.strip()
    ]
    last_two = [r for r in written_rows if r.get("row") in (280, 281)]
    if len(last_two) != 2:
        print(
            f"ERROR: post-write read did not find rows 280 + 281 (found {[r.get('row') for r in last_two]})",
            file=sys.stderr,
        )
        del seed
        del sk
        return 4
    for r in last_two:
        sig_hex = r["ed25519_signature"]
        canon = row_canonical_bytes(r)
        canon_sha3 = hashlib.sha3_512(canon).hexdigest()
        canon_ok = canon_sha3 == r["canonical_json_sha3_512"]
        try:
            pk.verify(bytes.fromhex(sig_hex), canon)
            sig_ok = True
        except Exception as exc:  # noqa: BLE001
            print(f"ERROR: row {r['row']} signature verify FAILED — {exc}", file=sys.stderr)
            sig_ok = False
        if not (canon_ok and sig_ok):
            print(
                f"ERROR: row {r['row']} consistency check FAILED "
                f"(canon_ok={canon_ok}, sig_ok={sig_ok})",
                file=sys.stderr,
            )
            del seed
            del sk
            return 4
        print(f"  row {r['row']}  canon-sha3 match: True  sig verify: PASS")

    # 8. Scrub
    del seed
    del sk
    print()
    print("Rotation ceremony complete. Next: fire OD-E fix-forward ceremony "
          "(Command B) which appends rows 282-288 under the NEW cards-publisher key.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
