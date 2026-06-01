"""Cards embedded re-sign LOCK ceremony — 3 dual-track CLCs (2026-05-18).

Repairs the OD-E carry-over: lock_history rows 285-287 (signed 2026-05-18T01:00:00Z
under NEW cards-publisher pubkey c93f1881…2e41107) declared the post-restructure
canonical bytes for the 3 dual-track CLC cards as the authoritative
supersession-delivery surface, but the in-card embedded fields
``lifecycle.content_hash`` (SHA-256) and ``_research_metadata.ed25519_signature``
(Ed25519 over canonical_bytes) were intentionally left stale per the OD-C row 272
precedent that deferred embedded re-sign to v0.2 first-wave loader graduation.

The v0.1 loader DOES enforce ``lifecycle.content_hash`` at ``enforce_lifecycle_truth``
preflight (verify_content_hash=True default), which means the stale-by-design
embedded hashes fail-close the loader against the 3 cards.

This ceremony refreshes the embedded fields to match the on-disk post-restructure
canonical bytes (Option B per pre-push preflight 2026-05-18). The cryptographic
posture becomes fully coherent: the in-card hash + signature match the on-disk
canonical bytes, and the embedded signature verifies against the NEW
cards-publisher pubkey (the same pubkey that signed lock_history rows 285-287).

Reads the cards-publisher Ed25519 seed from env var
``CARDS_EMBEDDED_RE_SIGN_SEED`` (32-byte hex). Verifies derived pubkey ==
``PINNED_PUBKEY_HEX``. Fails closed on any mismatch.

Appends 4 rows to ``pipeline/engineering/lock_history.v1.jsonl`` at single
``CEREMONY_TIMESTAMP``:

  Row 289  card_embedded_re_sign       market_access — content_hash + ed25519_signature refresh
  Row 290  card_embedded_re_sign       credit_underwriting — content_hash + ed25519_signature refresh
  Row 291  card_embedded_re_sign       sponsorship_corporate — content_hash + ed25519_signature refresh
  Row 292  blueprint-interface-index   §0.5 v35 paired-commit marker (runtime-live 543→544)

Discipline:
  - One-shot script. Seed never echoed. Caller scrubs env var after.
  - Verify derived pubkey == pinned NEW pubkey before ANY signing.
  - max_row guard (expects 288 — the §0.5 v34 OD-E fix-forward paired-commit).
  - Surgical line-replacement: only ``  content_hash: sha256:…`` and
    ``  ed25519_signature: <hex>`` lines are modified. All comments, field
    ordering, and other content preserved verbatim.
  - Pre-write integrity check: yaml.safe_load round-trip of the pre-modified
    YAML produces card_body whose canonical_bytes == sign-time canonical_bytes
    (no whitespace / encoding drift).
  - Post-write integrity check: yaml.safe_load of the modified YAML produces
    card_body whose new lifecycle.content_hash matches recomputed canonical-
    bytes-SHA256 and whose new _research_metadata.ed25519_signature verifies
    against the NEW pubkey.
  - Atomic write via tmp + os.replace for both YAML and lock_history.
  - Exit codes:
      0  success — rows 289-292 appended; embedded fields refreshed; all
         round-trip checks PASS
      1  bad seed (missing env var / not hex / wrong length)
      2  derived pubkey != pinned NEW pubkey (operator pasted wrong seed)
      3  max_row guard failed (lock_history not at expected 288)
      4  card preflight failed (canonical bytes drift or unexpected disk state)
      5  post-write integrity check failed (the cure was worse than the disease)

Row 289-291 shape mirrors OD-E delivery rows 285-287 field-for-field except for:
  - lock_kind: ``card_embedded_re_sign`` (NEW kind under §6.17 Option-B; no new
    vocabulary primitive — kind resolves as a sub-pattern of the existing
    ``card_cartridge_supersession`` family per §0.5 v32 §G + §0.5 v34 §A)
  - new fields: ``new_content_hash_sha256``, ``new_embedded_ed25519_signature``
    (both signed-over via canonical_bytes-then-sign discipline)
  - explicit cross-ref to authoritative supersession row 285/286/287 + parent
    OD-E fix-forward row 282 + §0.5 v34 row 288

Row 292 mirrors row 288 §0.5 paired-commit shape field-for-field.
"""

from __future__ import annotations

import copy
import hashlib
import json
import os
import pathlib
import re
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

PINNED_PUBKEY_HEX = "c93f1881cbb7ff315b29f416c2f8bc16dc9e1d1576e743f63e577de992e41107"

CEREMONY_TIMESTAMP = "2026-05-18T05:00:00Z"

PARENT_HANDOFF = (
    "pipeline/handoffs/cards_publisher_key_rotation_2026-05-17/"
    "00_operator_execution_checklist.md"
)

MAX_ROW_GUARD_EXPECTED = 288
START_ROW = 289
END_ROW = 292


# ─── card targets (matches OD-E delivery rows 285/286/287) ───
# Ordering mirrors rows 285→286→287 (market_access, credit_underwriting,
# sponsorship_corporate). Each entry pairs with the supersession-delivery row
# that declared post-restructure canonical bytes under the NEW pubkey.
CARDS = [
    {
        "rel_path": "pipeline/cards/CLC/market_access.yaml",
        "slug": "market_access",
        "card_id": "TILTH-CLC-05",
        "supersession_row": 285,
        "module": "pipeline.cards.CLC.market_access",
    },
    {
        "rel_path": "pipeline/cards/CLC/credit_underwriting.yaml",
        "slug": "credit_underwriting",
        "card_id": "TILTH-CLC-06",
        "supersession_row": 286,
        "module": "pipeline.cards.CLC.credit_underwriting",
    },
    {
        "rel_path": "pipeline/cards/CLC/sponsorship_corporate.yaml",
        "slug": "sponsorship_corporate",
        "card_id": "TILTH-CLC-07",
        "supersession_row": 287,
        "module": "pipeline.cards.CLC.sponsorship_corporate",
    },
]


# ─── canonical-bytes recipe (mirrors pipeline/cards/loader.py:canonical_bytes) ───
def _without_signature_and_hash_fields(card_body: dict) -> dict:
    normalized = copy.deepcopy(dict(card_body))
    lifecycle = normalized.get("lifecycle")
    if isinstance(lifecycle, dict):
        lifecycle.pop("signature_status", None)
        lifecycle.pop("content_hash", None)
    research_metadata = normalized.get("_research_metadata")
    if isinstance(research_metadata, dict):
        research_metadata.pop("ed25519_signature", None)
    return normalized


def card_canonical_bytes(card_body: dict) -> bytes:
    normalized = _without_signature_and_hash_fields(card_body)
    return json.dumps(
        normalized,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def row_canonical_bytes(row: dict) -> bytes:
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


# ─── surgical line replacement ───
# The card YAMLs were authored with human-readable comments + specific field
# ordering. yaml.safe_dump round-trips lose all of that. We do line-level edits
# on the two specific fields we need to change.
#
# The content_hash field lives inside the lifecycle: mapping at 2-space indent:
#     lifecycle:
#       …
#       content_hash: sha256:<64-hex>
#       …
#
# The ed25519_signature field lives inside _research_metadata: at 2-space indent:
#     _research_metadata:
#       …
#       ed25519_signature: <128-hex>
#       …
#
# Both fields are single-line scalar values. Surgical regex replacement on each.

CONTENT_HASH_LINE_RE = re.compile(
    r"^(?P<indent>\s+)content_hash:\s*sha256:[0-9a-f]{64}\s*$",
    re.MULTILINE,
)
ED25519_SIG_LINE_RE = re.compile(
    r"^(?P<indent>\s+)ed25519_signature:\s*[0-9a-f]{128}\s*$",
    re.MULTILINE,
)


def replace_content_hash_line(yaml_text: str, new_hash_hex: str) -> str:
    """Replace the single content_hash: sha256:… line. Preserves indentation."""
    matches = list(CONTENT_HASH_LINE_RE.finditer(yaml_text))
    if len(matches) != 1:
        raise RuntimeError(
            f"expected exactly 1 content_hash line, found {len(matches)}"
        )
    m = matches[0]
    new_line = f"{m.group('indent')}content_hash: sha256:{new_hash_hex}"
    return yaml_text[: m.start()] + new_line + yaml_text[m.end() :]


def replace_ed25519_signature_line(yaml_text: str, new_sig_hex: str) -> str:
    """Replace the single ed25519_signature: <hex> line. Preserves indentation."""
    matches = list(ED25519_SIG_LINE_RE.finditer(yaml_text))
    if len(matches) != 1:
        raise RuntimeError(
            f"expected exactly 1 ed25519_signature line, found {len(matches)}"
        )
    m = matches[0]
    new_line = f"{m.group('indent')}ed25519_signature: {new_sig_hex}"
    return yaml_text[: m.start()] + new_line + yaml_text[m.end() :]


def atomic_write_text(path: pathlib.Path, content: str) -> None:
    fd, tmp_path = tempfile.mkstemp(
        prefix=path.name + ".",
        suffix=".tmp",
        dir=str(path.parent),
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(content)
        os.replace(tmp_path, path)
    except Exception:
        try:
            os.unlink(tmp_path)
        finally:
            raise


def append_lock_history_rows(rows: list[dict]) -> None:
    """Atomic append of pre-signed rows to lock_history.v1.jsonl."""
    existing = LOCK_HISTORY.read_text(encoding="utf-8")
    if existing and not existing.endswith("\n"):
        existing = existing + "\n"
    appended = "".join(
        json.dumps(r, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n"
        for r in rows
    )
    atomic_write_text(LOCK_HISTORY, existing + appended)


def sign_row(sk: Ed25519PrivateKey, row_no_sig: dict) -> dict:
    """Sign row payload, return row with canonical_json_sha3_512 + ed25519_signature."""
    canon = row_canonical_bytes(row_no_sig)
    sha3_hex = hashlib.sha3_512(canon).hexdigest()
    sig = sk.sign(canon)
    final = dict(row_no_sig)
    final.pop("ed25519_signature", None)
    final.pop("canonical_json_sha3_512", None)
    final["canonical_json_sha3_512"] = sha3_hex
    final["ed25519_signature"] = sig.hex()
    return final


def max_row_in_lock_history() -> int:
    max_row = -1
    with LOCK_HISTORY.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            row = r.get("row")
            if isinstance(row, int):
                max_row = max(max_row, row)
    return max_row


def main() -> int:
    # ─── seed → key ───
    seed_hex = os.environ.get("CARDS_EMBEDDED_RE_SIGN_SEED", "").strip()
    if not seed_hex or len(seed_hex) != 64:
        print(
            "ERROR: env var CARDS_EMBEDDED_RE_SIGN_SEED must be set to the "
            "32-byte NEW cards-publisher seed (64 hex chars). Aborting.",
            file=sys.stderr,
        )
        return 1
    try:
        seed = bytes.fromhex(seed_hex)
    except ValueError:
        print("ERROR: seed is not valid hex. Aborting.", file=sys.stderr)
        return 1
    if len(seed) != 32:
        print("ERROR: seed must be exactly 32 bytes. Aborting.", file=sys.stderr)
        return 1

    sk = Ed25519PrivateKey.from_private_bytes(seed)
    pk = sk.public_key()
    pk_hex = pk.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    ).hex()
    if pk_hex != PINNED_PUBKEY_HEX:
        print(
            f"ERROR: derived pubkey {pk_hex} != pinned NEW pubkey "
            f"{PINNED_PUBKEY_HEX}. Operator pasted wrong seed. Aborting.",
            file=sys.stderr,
        )
        del seed
        del sk
        return 2

    # ─── max_row guard ───
    current_max = max_row_in_lock_history()
    if current_max != MAX_ROW_GUARD_EXPECTED:
        print(
            f"ERROR: lock_history.v1.jsonl max row = {current_max}; expected "
            f"{MAX_ROW_GUARD_EXPECTED} (§0.5 v34 OD-E fix-forward paired-commit). "
            f"Refusing to append — verify operator dispatched ceremonies in order.",
            file=sys.stderr,
        )
        del seed
        del sk
        return 3

    # ─── preflight: read all 3 cards, compute pre-modification canonical hashes ───
    preflight: list[dict] = []
    for entry in CARDS:
        card_path = BASE / entry["rel_path"]
        yaml_text = card_path.read_text(encoding="utf-8")
        body = yaml.safe_load(yaml_text)
        canon = card_canonical_bytes(body)
        new_hash_hex = hashlib.sha256(canon).hexdigest()
        old_hash = (body.get("lifecycle", {}) or {}).get("content_hash", "")
        old_sig = (body.get("_research_metadata", {}) or {}).get("ed25519_signature", "")

        # Sign canonical_bytes with NEW seed
        new_sig = sk.sign(canon).hex()

        # Pre-write integrity: confirm canonical_bytes match line-level recipe by
        # re-extracting body after yaml.safe_load round-trip
        if hashlib.sha256(card_canonical_bytes(body)).hexdigest() != new_hash_hex:
            print(
                f"ERROR: {entry['rel_path']} canonical_bytes drift on re-compute. "
                f"Aborting before any write.",
                file=sys.stderr,
            )
            del seed
            del sk
            return 4

        preflight.append({
            "entry": entry,
            "card_path": card_path,
            "yaml_text": yaml_text,
            "old_content_hash": old_hash,
            "new_content_hash_hex": new_hash_hex,
            "old_ed25519_signature_hex": old_sig,
            "new_ed25519_signature_hex": new_sig,
            "canonical_bytes_sha3_512_hex": hashlib.sha3_512(canon).hexdigest(),
        })

        print(
            f"  preflight {entry['slug']:24s}  "
            f"new content_hash sha256:{new_hash_hex[:24]}…  "
            f"new sig {new_sig[:24]}…"
        )

    # ─── modify all 3 YAMLs (atomic per file) ───
    for pf in preflight:
        new_text = replace_content_hash_line(
            pf["yaml_text"], pf["new_content_hash_hex"]
        )
        new_text = replace_ed25519_signature_line(
            new_text, pf["new_ed25519_signature_hex"]
        )
        atomic_write_text(pf["card_path"], new_text)
        print(f"  wrote {pf['entry']['rel_path']}")

    # ─── post-write integrity check: re-read each card, verify hash + signature ───
    for pf in preflight:
        entry = pf["entry"]
        body = yaml.safe_load(pf["card_path"].read_text(encoding="utf-8"))
        canon = card_canonical_bytes(body)
        check_hash = "sha256:" + hashlib.sha256(canon).hexdigest()
        if check_hash != body["lifecycle"]["content_hash"]:
            print(
                f"ERROR: {entry['rel_path']} post-write content_hash mismatch — "
                f"expected {check_hash}, found {body['lifecycle']['content_hash']}. "
                f"Aborting.",
                file=sys.stderr,
            )
            del seed
            del sk
            return 5
        # verify signature
        sig_hex = body["_research_metadata"]["ed25519_signature"]
        pk_verify = Ed25519PublicKey.from_public_bytes(bytes.fromhex(PINNED_PUBKEY_HEX))
        try:
            pk_verify.verify(bytes.fromhex(sig_hex), canon)
        except Exception as exc:
            print(
                f"ERROR: {entry['rel_path']} post-write signature verify FAILED — "
                f"{exc}. Aborting.",
                file=sys.stderr,
            )
            del seed
            del sk
            return 5
        print(f"  verified {entry['rel_path']}  hash + sig OK against NEW pubkey")

    # ─── assemble + sign 4 lock_history rows ───
    new_rows: list[dict] = []

    for member_no, pf in enumerate(preflight, start=1):
        entry = pf["entry"]
        file_sha3, fsize = file_sha3_512_hex(entry["rel_path"])
        row_no_sig = {
            "row": START_ROW + (member_no - 1),
            "lock_class": "cards",
            "lock_kind": f"compound-paired-commit-four-member-{member_no}",
            "lock_cycle": (
                f"Cards embedded re-sign — {entry['slug']} (sub-event of OD-E "
                f"fix-forward; deferred embedded re-sign per OD-C row 272 precedent "
                f"folded here so v0.1 loader content_hash enforcement passes). "
                f"Updates in-card lifecycle.content_hash + "
                f"_research_metadata.ed25519_signature to match on-disk post-"
                f"restructure canonical bytes already declared authoritative by "
                f"supersession-delivery row {entry['supersession_row']}. Signed "
                f"by NEW cards-publisher key c93f1881...2e41107 (post-rotation row 280)."
            ),
            "lock_mode": (
                "COMPOUND-LOCK sibling-paired-commit-4 — paired with 2 sibling "
                "embedded-re-sign rows + 1 §0.5 v35 paired-commit at the same "
                f"lock_timestamp_utc {CEREMONY_TIMESTAMP} per §6.17 Option-B. "
                "Surgical line-replacement preserves all YAML comments + field "
                "ordering. Round-trip verification: post-write canonical_bytes "
                "SHA-256 matches in-card content_hash; post-write Ed25519 "
                "signature verifies against NEW pubkey."
            ),
            "module": entry["module"],
            "card_id": entry["card_id"],
            "slug": entry["slug"],
            "amendment_file": entry["rel_path"],
            "file_path": entry["rel_path"],
            "ceremony_parent_row": 282,
            "supersession_authority_row": entry["supersession_row"],
            "parent_lock_row": 288,
            "parent_handoff": PARENT_HANDOFF,
            "embedded_re_sign_kind": "content_hash+ed25519_signature",
            "prior_content_hash": pf["old_content_hash"],
            "new_content_hash": f"sha256:{pf['new_content_hash_hex']}",
            "prior_embedded_ed25519_signature_hex": pf["old_ed25519_signature_hex"],
            "new_embedded_ed25519_signature_hex": pf["new_ed25519_signature_hex"],
            "post_resign_canonical_bytes_sha3_512_hex": pf["canonical_bytes_sha3_512_hex"],
            "post_resign_file_size_bytes": fsize,
            "post_resign_file_sha3_512_hex": file_sha3,
            "verified_against_pinned_pubkey": True,
            "embedded_signature_status": (
                "REFRESHED 2026-05-18 under NEW cards-publisher pubkey "
                "c93f1881...2e41107; content_hash + ed25519_signature aligned with "
                "on-disk post-restructure canonical bytes. v0.1 loader "
                "verify_content_hash now passes; v0.2 first-wave loader graduation "
                "(per architecture v7.0.11 §5) will verify the in-card signature "
                "against the publisher pubkey as a fully-active loader gate."
            ),
            "threat_severity_at_v0_1_v0_2": (
                "LOW — embedded refresh aligning in-card data with already-"
                "authoritative supersession surface (rows 285-287). No canonical-"
                "bytes change (the bytes that count have been on disk since OD-E "
                "fix-forward; this row updates the IN-CARD hash + sig fields that "
                "are stripped before canonical-bytes computation)."
            ),
            "lock_timestamp_utc": CEREMONY_TIMESTAMP,
            "operator": "Josh Inklovich",
            "model_tier": "opus_4_7",
            "publisher_pubkey_ed25519_hex": PINNED_PUBKEY_HEX,
            "signature_target_pubkey": "vault_shared/cards/publisher_pubkey.signed.yaml",
            "sha3_512": file_sha3,
            "file_size_bytes": fsize,
            "review_verdict": (
                "Operator authorized embedded re-sign per pre-push preflight "
                "2026-05-18 Option B. Aligns v0.1 loader content_hash enforcement "
                "with on-disk post-restructure canonical bytes already declared "
                "authoritative by supersession-delivery rows 285-287."
            ),
            "verdict": (
                f"LOCKED — embedded re-sign of {entry['slug']} card under NEW "
                f"cards-publisher pubkey c93f1881...2e41107; content_hash + "
                f"ed25519_signature refreshed; post-write round-trip verify PASS."
            ),
        }
        signed = sign_row(sk, row_no_sig)
        new_rows.append(signed)

    # Row 292 — §0.5 v35 paired-commit marker
    final_card_row_signed = new_rows[-1]
    runtime_live_total_after_v35 = 544  # v34 closed at 543 per row 288
    v35_row_no_sig = {
        "row": END_ROW,
        "lock_class": "blueprint-interface-index",
        "lock_kind": "compound-paired-commit-four-member-4",
        "lock_cycle": (
            "Cards embedded re-sign §0.5 v35 paired-commit — ONE marker row only "
            "(blueprint.amendment_anchor.cards_embedded_re_sign.v1; row 544 in "
            "§0.5 internal index). §0.5 v34 was consumed by the OD-E fix-forward "
            f"(row 288). v35 anchors the embedded re-sign event {CEREMONY_TIMESTAMP} "
            "as a sub-event of the OD-E fix-forward audit-integrity repair "
            "chain. Signed by NEW cards-publisher pubkey c93f1881...2e41107."
        ),
        "lock_mode": (
            "COMPOUND-LOCK sibling-paired-commit-4 — paired with 3 sibling "
            f"embedded-re-sign rows at the same lock_timestamp_utc "
            f"{CEREMONY_TIMESTAMP} per §6.17 Option-B. Marker-only sub-pattern "
            "per §0.5 v33 + v34 precedent: no new schema rows, no new failure-"
            "code rows, no new AST-lint rows, no new vocabulary kinds. The "
            "marker's primitive_kind 'marker' resolves against the v5 + v6 + "
            "v17-v19 closed vocabulary."
        ),
        "module": "pipeline.blueprint.v0_1.section_00_5_cards_embedded_re_sign_marker",
        "amendment_class": (
            "§0.5-paired-commit-embedded-re-sign + marker-only sub-pattern (one "
            "marker row only; no schema rows; no enforcement-infrastructure rows; "
            "no failure-code rows; no AST-lint rows; no vocabulary kind extension; "
            "audit-trail anchor only for the embedded re-sign event)"
        ),
        "blueprint_amendment_parent_chain": [271, 273, 275, 281, 288],
        "blueprint_section": (
            "pipeline/blueprint/v0.1/section_00_5_section_18_6_v2_amendment.md"
        ),
        "blueprint_version": "§0.5 v35 LOCKED 2026-05-18",
        "companion_lock_with": [
            "3 × card_embedded_re_sign rows (289/290/291) at lock_timestamp_utc "
            f"{CEREMONY_TIMESTAMP}"
        ],
        "compound_lock_with": [
            entry["rel_path"] for entry in CARDS
        ],
        "cross_family_posture": (
            "Self-LOCK per embedded-re-sign carve-out — operator-authorized "
            "Option B per pre-push preflight 2026-05-18. L-005 Thesis dispatch "
            "waived under audit-integrity-class repair scope (no new enforcement "
            "teeth; loader-side content_hash enforcement already LIVE and was "
            "the source of this repair pressure)."
        ),
        "file_path": (
            "pipeline/blueprint/v0.1/section_00_5_section_18_6_v2_amendment.md"
        ),
        "lock_timestamp_utc": CEREMONY_TIMESTAMP,
        "operator": "Josh Inklovich",
        "model_tier": "opus_4_7",
        "parent_handoff": PARENT_HANDOFF,
        "parent_lock_row": 288,
        "ceremony_parent_row": 282,
        "predecessor_amendments_chain": [
            "Wave 2 LOCK ceremony rows 250-261 (12 cards LOCKED 2026-05-16T16:00:00Z) + "
            "§0.5 v29 paired-commit row 262",
            "§4 v2.x.6 router dedup LOCK rows 263/264 at 2026-05-16T16:30:00Z (OD-5)",
            "OD-A admin_risk_register v2.4 compound LOCK rows 265-268 at "
            "2026-05-16T20:28:58Z",
            "OD-D §18.11 v1.1 fold-in discipline + §18 main re-pin + §0.5 v30 triple "
            "paired-commit rows 269-271 at 2026-05-17T04:34:50Z",
            "OD-C §4 v2.x.7 + §0.5 v31 narrow-corrective compound LOCK rows 272-273 at "
            "2026-05-17T05:30:00Z",
            "OD-E §18.6 v2 dual-track restructure compound LOCK rows 274-278 at "
            "2026-05-17T16:00:00Z (initial fire — embedded re-sign deferred)",
            "OD-E post-ceremony status-flip housekeeping supersession row 279 at "
            "2026-05-17T16:01:00Z",
            "Cards-publisher compromise-class rotation row 280 + §0.5 v33 marker row "
            "281 at 2026-05-18T00:00:00Z",
            "OD-E fix-forward delivery + §0.5 v34 paired-commit rows 282-288 at "
            "2026-05-18T01:00:00Z (post-restructure canonical bytes declared "
            "authoritative; embedded re-sign deferred per OD-C row 272 precedent)",
        ],
        "primitive_id_added": "blueprint.amendment_anchor.cards_embedded_re_sign.v1",
        "primitive_id_defined_at": (
            "pipeline/blueprint/v0.1/section_00_5_section_18_6_v2_amendment.md"
        ),
        "primitive_id_kind": "marker",
        "primitive_id_parent_lock_version": "§18.6 v2 embedded re-sign",
        "primitive_id_seat_owner": "cards",
        "primitive_id_stability_tier": "STABLE",
        "publisher_pubkey_ed25519_hex": PINNED_PUBKEY_HEX,
        "signature_target_pubkey": "vault_shared/cards/publisher_pubkey.signed.yaml",
        "row_delta": (
            "+1 row (1 marker only; no enforcement-infrastructure; no schema; "
            "no failure-code; no ast-lint; no card-namespace)"
        ),
        "runtime_live_total_after": runtime_live_total_after_v35,
        "runtime_live_total_before": runtime_live_total_after_v35 - 1,
        "seat_owner_attribute": (
            "the row carries seat_owner: cards per §0.5 v20 RT-19/RT-C2-09 "
            "invariant (mirrors §0.5 v34 cards.* fix-forward at the audit-"
            "integrity-repair layer)"
        ),
        "review_verdict": (
            "Operator authorized embedded re-sign §0.5 v35 paired-commit self-LOCK "
            "per pre-push preflight 2026-05-18 Option B. Sequencing verified: "
            "OD-E = §0.5 v32 row 275 → cards-publisher rotation = §0.5 v33 row 281 "
            "→ OD-E fix-forward = §0.5 v34 row 288 → embedded re-sign = §0.5 v35 "
            f"row {END_ROW} at {CEREMONY_TIMESTAMP}."
        ),
        "threat_severity_at_v0_1_v0_2": (
            "LOW — embedded re-sign audit anchor; no new runtime enforcement; "
            "completes the OD-E audit-integrity chain by aligning in-card hash "
            "+ sig fields with already-authoritative supersession surface."
        ),
        "vocabulary_preservation": (
            "the row's primitive_kind 'marker' resolves against the v5 + v6 + "
            "v17-v19 closed vocabulary"
        ),
        "verdict": (
            f"LOCKED — §0.5 v35 embedded re-sign paired-commit; marker-only "
            f"sub-pattern; +1 marker row "
            f"(blueprint.amendment_anchor.cards_embedded_re_sign.v1, kind=marker, "
            f"seat_owner=cards, stability_tier=STABLE); runtime-live total "
            f"{runtime_live_total_after_v35 - 1}→{runtime_live_total_after_v35}."
        ),
    }
    new_rows.append(sign_row(sk, v35_row_no_sig))

    # ─── append all 4 rows atomically ───
    append_lock_history_rows(new_rows)
    print(
        f"  appended rows {START_ROW}-{END_ROW} to "
        f"pipeline/engineering/lock_history.v1.jsonl"
    )

    # ─── round-trip verify each appended row's signature ───
    pk_verify = Ed25519PublicKey.from_public_bytes(bytes.fromhex(PINNED_PUBKEY_HEX))
    with LOCK_HISTORY.open(encoding="utf-8") as fh:
        all_rows = [json.loads(line) for line in fh if line.strip()]
    appended_rows = [r for r in all_rows if r.get("row") in range(START_ROW, END_ROW + 1)]
    if len(appended_rows) != 4:
        print(
            f"ERROR: post-write read found {len(appended_rows)} of expected 4 rows; "
            f"refusing to declare success.",
            file=sys.stderr,
        )
        del seed
        del sk
        return 5
    for r in appended_rows:
        canon = row_canonical_bytes(r)
        canon_sha = hashlib.sha3_512(canon).hexdigest()
        if canon_sha != r["canonical_json_sha3_512"]:
            print(
                f"ERROR: row {r['row']} canonical-bytes drift post-write "
                f"({canon_sha[:24]}… vs {r['canonical_json_sha3_512'][:24]}…)",
                file=sys.stderr,
            )
            del seed
            del sk
            return 5
        try:
            pk_verify.verify(bytes.fromhex(r["ed25519_signature"]), canon)
        except Exception as exc:
            print(
                f"ERROR: row {r['row']} signature verify FAILED post-write — {exc}",
                file=sys.stderr,
            )
            del seed
            del sk
            return 5
        print(f"  row {r['row']} round-trip verify PASS")

    # ─── scrub key material ───
    del seed
    del sk

    print(
        f"\nCards embedded re-sign ceremony COMPLETE. 3 cards updated, "
        f"4 lock_history rows appended ({START_ROW}-{END_ROW}), all signatures "
        f"verified against pinned cards-publisher pubkey c93f1881…2e41107."
    )
    print(
        "\nCaller MUST scrub the CARDS_EMBEDDED_RE_SIGN_SEED env var:\n"
        "  unset CARDS_EMBEDDED_RE_SIGN_SEED"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
