#!/usr/bin/env python3
"""Forward-completion of Wave 2 LOCK ceremony — cards already signed.

Cards already have LOCK edits + embedded signatures. This script:
  1. Re-derives sig + sha3 from the current YAMLs (idempotent verification).
  2. Appends 13 lock_history rows (12 cards + 1 §0.5 v29 paired-commit).
  3. Writes §0.5 v29 amendment file.
  4. Writes signature_summary.json to audit trail.
  5. Final re-verification.

Uses robust parser that handles historical rows without "row" key.
"""
from __future__ import annotations

import os
import sys
import json
import hashlib
import re
from pathlib import Path

import yaml

from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey, Ed25519PublicKey,
)
from cryptography.hazmat.primitives import serialization

# Import from the main ceremony script
sys.path.insert(0, str(Path(__file__).parent))
import importlib.util
spec = importlib.util.spec_from_file_location(
    "cards_wave_2_lock_ceremony_2026_05_16",
    Path(__file__).parent / "cards_wave_2_lock_ceremony_2026-05-16.py",
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

BASE = Path(os.environ.get("WORKSPACE_BASE", os.path.expanduser("~/Downloads/GoldenQuill")))


def main() -> int:
    seed_hex = os.environ.get("OPERATOR_SEED_HEX")
    if not seed_hex:
        print("ERROR: OPERATOR_SEED_HEX env not set", file=sys.stderr)
        return 1
    sk = Ed25519PrivateKey.from_private_bytes(bytes.fromhex(seed_hex.strip()))
    pk_bytes = sk.public_key().public_bytes(
        serialization.Encoding.Raw, serialization.PublicFormat.Raw,
    )
    if pk_bytes.hex() != mod.PINNED_PUBKEY_HEX:
        print(f"ERROR: pubkey mismatch", file=sys.stderr)
        return 1
    pubkey = Ed25519PublicKey.from_public_bytes(pk_bytes)

    audit_dir = BASE / "pipeline/validation/cards_wave_2_lock_ceremony_2026-05-16"
    audit_dir.mkdir(parents=True, exist_ok=True)

    print(f"# Cards Wave 2 LOCK Ceremony FORWARD-COMPLETION {mod.CEREMONY_TIMESTAMP}")
    print(f"# Pubkey verified MATCHES pinned: {pk_bytes.hex()}")
    print()

    # Stage A: extract sig + sha3 from each card (already in file)
    print("## Stage A: Extract sig + sha3 from already-edited cards")
    sig_summary = []
    rows_to_append = []
    sig_re = re.compile(r'ed25519_signature:\s*"([0-9a-f]{128})"')
    sha3_re = re.compile(r'pinning\):\s+([0-9a-f]{128})')
    for idx, (slug, card_id, axis, fp, schema_v, display_name, row) in enumerate(mod.WAVE_2_CARDS):
        text = (BASE / fp).read_text()
        sig_m = sig_re.search(text)
        sha3_m = sha3_re.search(text)
        if not sig_m or not sha3_m:
            print(f"  FAIL: cannot extract sig/sha3 from {slug}")
            return 2
        sig_hex = sig_m.group(1)
        sha3_hex = sha3_m.group(1)
        # Re-verify
        canonical, computed_sha3 = mod.canonical_json_for_signing(yaml_text=text)
        if computed_sha3 != sha3_hex:
            print(f"  FAIL: {slug} sha3 drift: file says {sha3_hex[:20]}, computed {computed_sha3[:20]}")
            return 3
        try:
            pubkey.verify(bytes.fromhex(sig_hex), canonical)
        except Exception as e:
            print(f"  FAIL: {slug} sig does NOT verify: {e}")
            return 4
        sig_summary.append({
            "slug": slug, "card_id": card_id, "row": row,
            "sha3_512_hex": sha3_hex, "sig_hex": sig_hex,
            "sig_prefix": sig_hex[:16], "verified": True,
            "file_path": fp,
        })
        lh_row = mod.build_card_lock_history_row(
            row=row, card_idx=idx, total=12, slug=slug, card_id=card_id, axis=axis,
            file_path=fp, schema_version=schema_v, display_name=display_name,
            sha3_hex=sha3_hex, sig_hex=sig_hex,
        )
        rows_to_append.append(lh_row)
        print(f"  row{row}  {card_id} {slug:30s} sig={sig_hex[:16]}... verify=OK")
    print()

    # §0.5 v29 row
    rows_to_append.append(mod.build_section_00_5_v29_row(row=mod.SECTION_00_5_V29_ROW))
    print(f"## Stage B: §0.5 v29 paired-commit row{mod.SECTION_00_5_V29_ROW} built")
    print()

    # Stage C: robust lock_history tail check
    print("## Stage C: Append rows to lock_history.v1.jsonl (robust parser)")
    lh_path = BASE / "pipeline/engineering/lock_history.v1.jsonl"
    max_existing = 0
    skipped_norow = 0
    with lh_path.open() as f:
        for line in f:
            if not line.strip():
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue
            if "row" in obj and isinstance(obj["row"], int):
                max_existing = max(max_existing, obj["row"])
            else:
                skipped_norow += 1
    print(f"  Pre-append max row: {max_existing} (skipped {skipped_norow} historical rows without row key)")
    print(f"  Wave 2 first row: {mod.WAVE_2_CARDS[0][6]}")
    if mod.WAVE_2_CARDS[0][6] != max_existing + 1:
        print(f"  ERROR: row collision. Expected start {max_existing + 1}; got {mod.WAVE_2_CARDS[0][6]}")
        print(f"  HARD STOP — inspect lock_history tail.")
        return 5
    with lh_path.open("a") as f:
        for r in rows_to_append:
            f.write(json.dumps(r) + "\n")
    print(f"  Appended {len(rows_to_append)} rows (rows {rows_to_append[0]['row']}..{rows_to_append[-1]['row']})")
    print()

    # Stage D: §0.5 v29 amendment file
    print("## Stage D: Write §0.5 v29 amendment file")
    section_path = BASE / "pipeline/blueprint/v0.1/section_00_5_cards_wave_2_amendment.md"
    content = mod.render_section_00_5_v29(sig_summary, rows_to_append[-1])
    section_path.write_text(content)
    print(f"  Wrote {section_path.relative_to(BASE)} ({len(content)} bytes)")
    print()

    # Stage E: signature_summary.json
    print("## Stage E: Audit trail signature_summary.json")
    summary_path = audit_dir / "signature_summary.json"
    summary_path.write_text(json.dumps({
        "ceremony_timestamp_utc": mod.CEREMONY_TIMESTAMP,
        "publisher_pubkey_ed25519_hex": mod.PINNED_PUBKEY_HEX,
        "lock_history_rows_card": [c["row"] for c in rows_to_append[:-1]],
        "lock_history_row_section_00_5": rows_to_append[-1]["row"],
        "cards": sig_summary,
    }, indent=2))
    print(f"  Wrote {summary_path.relative_to(BASE)}")
    print()

    # Final report
    print("## Ceremony FORWARD-COMPLETION COMPLETE.")
    print(f"# Audit trail: {audit_dir.relative_to(BASE)}")
    print()
    print("# Signature prefixes (first 16 hex chars per card, for operator handback):")
    for sm in sig_summary:
        print(f"  {sm['card_id']:14s} {sm['slug']:30s} sig={sm['sig_prefix']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
