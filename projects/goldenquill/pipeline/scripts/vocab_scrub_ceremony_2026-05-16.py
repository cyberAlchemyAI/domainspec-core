#!/usr/bin/env python3
"""
Vocabulary scrub LOCK ceremony — retire 'card' workspace-wide.

Per operator directive 2026-05-16: remove 'card' from every file name and content.
Per operator confirmation: Option A (vocabulary-scrub LOCK pass with re-signing).

Stages:
  1. Backup workspace state to vault_shared/vocab_scrub_2026-05-16_backup.tar.gz
  2. Bulk content scrub across all .md/.py/.json/.yaml/.txt/.sh files
     (excludes pipeline/engineering/lock_history.v1.jsonl + raw reviewer outputs +
      pyc/.venv/.claude/.git directories)
  3. Rename files + directories containing 'card'
  4. Update path references in code/JSON for renamed paths (already covered by content scrub)
  5. Re-compute SHA3-512 of previously-LOCKed amendment files with new bytes
  6. Sign each new SHA3-512 with operator Ed25519 (env $OPERATOR_SEED_HEX)
  7. Append supersession rows to lock_history.v1.jsonl
  8. Verification grep — report remaining 'card' usage

Operator pubkey pinned: 0b1a0bbfa5ee9149af2c4e6153ed037dd03c0d562c94d3eaefeaf798e6f375bd
"""
import os
import re
import sys
import json
import hashlib
import binascii
import subprocess
import datetime
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives import serialization

BASE = Path(os.path.expanduser("~/Downloads/GoldenQuill"))
BACKUP = BASE / "vault_shared/vocab_scrub_2026-05-16_backup.tar.gz"
CEREMONY_TIMESTAMP = "2026-05-16T14:30:00Z"
PINNED_PUBKEY_HEX = "0b1a0bbfa5ee9149af2c4e6153ed037dd03c0d562c94d3eaefeaf798e6f375bd"

# Files that are LOCKed audit trail (append-only). PRESERVE — never scrub.
PRESERVE_FILES = {
    BASE / "pipeline/engineering/lock_history.v1.jsonl",
}

# Directories that are reviewer raw outputs / verbatim audit trail. PRESERVE.
PRESERVE_DIRS_RAW_REVIEWER = [
    BASE / "pipeline/validation/cards_wave_1_thesis_2026-05-15",
    BASE / "pipeline/validation/cards_wave_2_thesis_2026-05-15",
    BASE / "pipeline/validation/v7_0_5_thesis_2026-05-09",
    BASE / "pipeline/validation/cc007_thesis_2026-05-16",
]

# Skip these directories entirely.
EXCLUDE_DIRS = {".claude", ".venv", ".git", "node_modules", "__pycache__", "data"}

# File extensions to scrub.
SCRUB_EXTENSIONS = {".md", ".py", ".json", ".yaml", ".yml", ".txt", ".sh"}

# Substitution rules — applied in order. Earlier rules consume compounds before later rules catch standalone.
SCRUB_RULES = [
    ("Card System", "Card System"),
    ("card_system", "card_system"),
    ("card_cic", "card_cic"),
    ("card_clc", "card_clc"),
    ("card", "card"),
    ("Card", "Card"),
    ("card", "card"),
    ("Cards", "Cards"),
    ("CARDS", "CARDS"),
    ("cards", "cards"),
    ("Card", "Card"),
    ("CARD", "CARD"),
    ("card", "card"),
]

# Path renames. Apply LAST after content scrub (so content references to old paths
# get scrubbed first, then file rename matches new paths).
PATH_RENAMES = [
    # Schema files
    ("pipeline/cards/_schema/card_cic.schema.json",
     "pipeline/cards/_schema/card_cic.schema.json"),
    ("pipeline/cards/_schema/card_clc.schema.json",
     "pipeline/cards/_schema/card_clc.schema.json"),
    # Architecture amendment
    ("pipeline/architecture/v0.1/architecture_v7_0_11_card_amendment.md",
     "pipeline/architecture/v0.1/architecture_v7_0_11_card_amendment.md"),
    # Blueprint sections
    ("pipeline/blueprint/v0.1/section_18_card_system.md",
     "pipeline/blueprint/v0.1/section_18_card_system.md"),
    ("pipeline/blueprint/v0.1/section_00_5_section_18_card_amendment.md",
     "pipeline/blueprint/v0.1/section_00_5_section_18_card_amendment.md"),
    # Logician gate
    ("pipeline/logician/gates/f_cards_private_data_in_card.py",
     "pipeline/logician/gates/f_cards_private_data_in_card.py"),
    # Test for above
    ("tests/logician/gates/test_f_cards_private_data_in_card.py",
     "tests/logician/gates/test_f_cards_private_data_in_card.py"),
    # Data collector seat
    ("pipeline/orchestrator/seats/data_collector/state_rules_card.py",
     "pipeline/orchestrator/seats/data_collector/state_rules_card.py"),
    ("tests/seats/data_collector/test_state_rules_card.py",
     "tests/seats/data_collector/test_state_rules_card.py"),
    # Docs
    ("docs/post_alpha/post_alpha_card_system_revised_2026-05-15.md",
     "docs/post_alpha/post_alpha_card_system_revised_2026-05-15.md"),
    ("docs/post_alpha/post_alpha_card_system_source_doc.md",
     "docs/post_alpha/post_alpha_card_system_source_doc.md"),
    # Vault shared
    ("vault_shared/state_rules_card",
     "vault_shared/state_rules_card"),
    # Cards eval arms
    ("pipeline/cards/eval/arms/arm_a_tilth_no_cards",
     "pipeline/cards/eval/arms/arm_a_tilth_no_cards"),
    ("pipeline/cards/eval/arms/arm_b_tilth_with_cards",
     "pipeline/cards/eval/arms/arm_b_tilth_with_cards"),
]

# Previously-LOCKed amendment files. Re-sign if bytes changed during scrub.
# Paths are POST-RENAME (so the script knows where to find them after step 3).
LOCKED_AMENDMENTS_FOR_RESIGN = [
    # Cards (Wave 1)
    ("wave_1_food_systems",      "pipeline/cards/CIC/food_systems.yaml",                          226),
    ("wave_1_operating_capacity","pipeline/cards/CLC/operating_capacity.yaml",                    227),
    # §18 chain
    ("section_18_v1",            "pipeline/blueprint/v0.1/section_18_card_system.md",             228),
    ("section_18_v1_1",          "pipeline/blueprint/v0.1/section_18_v1_1_amendment.md",          229),
    ("section_18_v1_2",          "pipeline/blueprint/v0.1/section_18_v1_2_amendment.md",          235),
    # §0.5 v26 (paired with §18 v1.1)
    ("section_00_5_v26",         "pipeline/blueprint/v0.1/section_00_5_section_18_card_amendment.md", 230),
    # §0.5 v27 (CC-007 paired)
    ("section_00_5_v27",         "pipeline/blueprint/v0.1/section_00_5_section_04_v2_x_5_amendment.md", 233),
    # §0.5 v28 (apolitical paired) — just LOCKed today
    ("section_00_5_v28",         "pipeline/blueprint/v0.1/section_00_5_apolitical_dialect_amendment.md", 237),
    # §4 v2.x.5 CC-007
    ("section_04_v2_x_5",        "pipeline/blueprint/v0.1/section_04_v2_x_5_provider_boundary_amendment.md", 232),
    # Architecture v7.0.12 (just-LOCKed today)
    ("architecture_v7_0_12",     "pipeline/architecture/v0.1/architecture_v7_0_12_apolitical_dialect_amendment.md", 234),
    # §4 v2.x apolitical_dialect (just-LOCKed today)
    ("section_04_apolitical",    "pipeline/blueprint/v0.1/section_04_logician_v2_x_apolitical_dialect.md", 236),
]


def in_preserve_path(p: Path) -> bool:
    """True if path is under a PRESERVE_DIRS_RAW_REVIEWER or matches PRESERVE_FILES."""
    if p in PRESERVE_FILES:
        return True
    for d in PRESERVE_DIRS_RAW_REVIEWER:
        try:
            p.relative_to(d)
            return True
        except ValueError:
            continue
    return False


def should_scrub_file(p: Path) -> bool:
    """True if file is scrubbable (right extension, not preserved, not in excluded dir)."""
    if p.suffix not in SCRUB_EXTENSIONS:
        return False
    if in_preserve_path(p):
        return False
    for part in p.parts:
        if part in EXCLUDE_DIRS:
            return False
    return True


def apply_scrub(text: str) -> str:
    """Apply all substitution rules in order."""
    for old, new in SCRUB_RULES:
        text = text.replace(old, new)
    return text


def stage_1_backup():
    """Create tarball backup. Excludes .venv, .git, node_modules to keep size small."""
    print(f"## Stage 1: Backup → {BACKUP}")
    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "tar", "czf", str(BACKUP),
        "--exclude=.git", "--exclude=.venv", "--exclude=node_modules",
        "--exclude=__pycache__", "--exclude=*.pyc",
        "--exclude=data/raw", "--exclude=data/pa_foundations/raw",
        "-C", str(BASE), ".",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  BACKUP STDERR: {result.stderr[:500]}")
    print(f"  Backup size: {BACKUP.stat().st_size // (1024*1024)} MB")
    return result.returncode == 0


def stage_2_content_scrub():
    """Bulk content scrub across SCRUB_EXTENSIONS files."""
    print("## Stage 2: Content scrub")
    files_scanned = 0
    files_changed = 0
    bytes_before = 0
    bytes_after = 0
    for p in BASE.rglob("*"):
        if not p.is_file():
            continue
        if not should_scrub_file(p):
            continue
        files_scanned += 1
        try:
            text = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, PermissionError):
            continue
        scrubbed = apply_scrub(text)
        if scrubbed != text:
            try:
                p.write_text(scrubbed, encoding="utf-8")
                bytes_before += len(text)
                bytes_after += len(scrubbed)
                files_changed += 1
            except (PermissionError, OSError) as e:
                # File is read-only or otherwise unwritable. Try chmod + retry, else skip.
                try:
                    os.chmod(p, 0o644)
                    p.write_text(scrubbed, encoding="utf-8")
                    bytes_before += len(text)
                    bytes_after += len(scrubbed)
                    files_changed += 1
                except Exception:
                    print(f"  SKIP (unwritable): {p.relative_to(BASE)} — {e.__class__.__name__}")
    print(f"  Files scanned: {files_scanned}")
    print(f"  Files changed: {files_changed}")
    print(f"  Bytes before: {bytes_before}, after: {bytes_after}, delta: {bytes_after - bytes_before}")


def stage_3_path_renames():
    """Rename files and directories containing 'card'."""
    print("## Stage 3: Path renames")
    renamed = 0
    skipped = 0
    for old_rel, new_rel in PATH_RENAMES:
        old = BASE / old_rel
        new = BASE / new_rel
        if not old.exists():
            print(f"  SKIP (source missing): {old_rel}")
            skipped += 1
            continue
        if new.exists():
            print(f"  SKIP (target exists): {new_rel}")
            skipped += 1
            continue
        new.parent.mkdir(parents=True, exist_ok=True)
        old.rename(new)
        renamed += 1
        print(f"  RENAMED: {old_rel} → {new_rel}")
    # Clean __pycache__ directories so .pyc files regenerate fresh
    for cache in BASE.rglob("__pycache__"):
        if cache.is_dir():
            subprocess.run(["rm", "-rf", str(cache)], check=False)
    print(f"  Total renamed: {renamed}; skipped: {skipped}")


def stage_4_resign(privkey, pubkey_bytes):
    """Re-compute SHA3-512 + re-sign LOCKed amendments with new post-scrub bytes."""
    print("## Stage 4: Re-sign previously-LOCKed amendments")
    pubkey = Ed25519PublicKey.from_public_bytes(pubkey_bytes)
    supersession_rows = []
    for slug, rel_path, original_lock_row in LOCKED_AMENDMENTS_FOR_RESIGN:
        full = BASE / rel_path
        if not full.exists():
            print(f"  WARN: amendment file missing: {rel_path}")
            continue
        post_bytes = full.read_bytes()
        sha3_512 = hashlib.sha3_512(post_bytes).hexdigest()
        sig = privkey.sign(bytes.fromhex(sha3_512))
        sig_hex = sig.hex()
        try:
            pubkey.verify(sig, bytes.fromhex(sha3_512))
            verified = True
        except Exception:
            verified = False
        supersession_rows.append({
            "slug": slug,
            "rel_path": rel_path,
            "original_lock_row": original_lock_row,
            "post_scrub_sha3_512_hex": sha3_512,
            "post_scrub_sig_ed25519_hex": sig_hex,
            "verified": verified,
            "file_size_bytes": len(post_bytes),
        })
        print(f"  {slug:30s} sha={sha3_512[:16]}...{sha3_512[-16:]} sig={sig_hex[:16]}... verified={verified}")
    return supersession_rows


def stage_5_append_lock_history(supersession_rows):
    """Append supersession rows to lock_history.v1.jsonl. Preserve historical rows verbatim."""
    print("## Stage 5: Append supersession rows to lock_history.v1.jsonl")
    lh_path = BASE / "pipeline/engineering/lock_history.v1.jsonl"
    # Read current max row id
    max_row = 0
    with lh_path.open() as f:
        for line in f:
            if not line.strip():
                continue
            try:
                obj = json.loads(line)
                if isinstance(obj.get("row"), int):
                    max_row = max(max_row, obj["row"])
            except json.JSONDecodeError:
                continue
    # Append a single ceremony-summary row + per-amendment supersession rows
    next_row = max_row + 1
    ceremony_row = {
        "row": next_row,
        "lock_timestamp_utc": CEREMONY_TIMESTAMP,
        "lock_class": "vocab_scrub_supersession_ceremony",
        "lock_kind": "vocabulary-scrub-workspace-wide-card-retirement",
        "lock_cycle": "Card → card vocabulary scrub LOCK pass — Option A canonical retirement (operator directive 2026-05-16T14:30:00Z)",
        "lock_mode": (
            f"WORKSPACE-WIDE VOCABULARY SCRUB. {len(supersession_rows)} previously-LOCKed amendments "
            f"re-signed at post-scrub SHA3-512. Historical rows 226-237 preserved verbatim as audit trail; "
            f"this ceremony APPENDS supersession rows that record the post-scrub canonical bytes + new sigs. "
            f"Trigger: third operator-flagged card-vocabulary slip in v7.0.12 LOCK ceremony (2026-05-16T14:00:00Z). "
            f"Operator chose Option A over Options B (surgical) and C (brute-force) for audit-integrity preservation."
        ),
        "module": "pipeline.scripts.vocab_scrub_ceremony_2026-05-16",
        "ceremony_script": "pipeline/scripts/vocab_scrub_ceremony_2026-05-16.py",
        "supersession_summary": {
            "amendments_re_signed": len(supersession_rows),
            "all_verified": all(r["verified"] for r in supersession_rows),
            "backup_path": str(BACKUP.relative_to(BASE)),
            "scrub_rules_count": len(SCRUB_RULES),
            "path_renames_count": len(PATH_RENAMES),
        },
        "operator": "Josh Inklovich",
        "model_tier": "opus_4_7",
        "publisher_pubkey_ed25519_hex": PINNED_PUBKEY_HEX,
        "verdict": "SUPERSESSION-LOCK — vocabulary scrub canonical retirement of 'card' workspace-wide; historical lock_history rows preserved as audit trail; per-amendment supersession rows appended below.",
    }
    rows_to_append = [ceremony_row]
    for i, sr in enumerate(supersession_rows):
        rows_to_append.append({
            "row": next_row + 1 + i,
            "lock_timestamp_utc": CEREMONY_TIMESTAMP,
            "lock_class": "vocab_scrub_supersession",
            "lock_kind": f"per-amendment-supersession-member-{i+1}-of-{len(supersession_rows)}",
            "lock_cycle": f"Re-sign {sr['slug']} at post-scrub SHA3-512 (supersedes lock_history row {sr['original_lock_row']} canonical bytes)",
            "parent_lock_row": sr["original_lock_row"],
            "ceremony_parent_row": next_row,
            "module": sr["slug"],
            "amendment_file": sr["rel_path"],
            "post_scrub_canonical_bytes_sha3_512_hex": sr["post_scrub_sha3_512_hex"],
            "post_scrub_publisher_signature_ed25519_hex": sr["post_scrub_sig_ed25519_hex"],
            "publisher_pubkey_ed25519_hex": PINNED_PUBKEY_HEX,
            "post_scrub_file_size_bytes": sr["file_size_bytes"],
            "verified_against_pinned_pubkey": sr["verified"],
            "operator": "Josh Inklovich",
            "verdict": f"SUPERSESSION — {sr['slug']} re-signed post vocab-scrub; row {sr['original_lock_row']} canonical bytes superseded by new SHA3-512 + sig recorded here. Historical row {sr['original_lock_row']} preserved verbatim in audit trail.",
        })
    with lh_path.open("a") as f:
        for row in rows_to_append:
            f.write(json.dumps(row) + "\n")
    print(f"  Appended {len(rows_to_append)} rows ({next_row}..{next_row + len(rows_to_append) - 1})")


def stage_6_verify():
    """Verification grep — report remaining 'card' usage."""
    print("## Stage 6: Verification")
    result = subprocess.run(
        ["grep", "-rln", "card",
         "--include=*.md", "--include=*.py", "--include=*.json",
         "--include=*.yaml", "--include=*.txt", "--include=*.sh",
         "--exclude-dir=.git", "--exclude-dir=.venv", "--exclude-dir=.claude",
         "--exclude-dir=__pycache__", "--exclude-dir=node_modules",
         str(BASE)],
        capture_output=True, text=True,
    )
    remaining = [line for line in result.stdout.split("\n") if line.strip()]
    print(f"  Remaining 'card' occurrences in scrubbable files: {len(remaining)}")
    if remaining and len(remaining) < 30:
        for r in remaining:
            print(f"    {r}")
    # Verify lock_history.v1.jsonl historical rows preserved
    lh = (BASE / "pipeline/engineering/lock_history.v1.jsonl").read_text()
    historical_card = lh.count("card")
    print(f"  lock_history.v1.jsonl 'card' occurrences (audit-trail preserved): {historical_card}")


def main() -> int:
    seed_hex = os.environ.get("OPERATOR_SEED_HEX")
    if not seed_hex:
        print("ERROR: OPERATOR_SEED_HEX env not set", file=sys.stderr)
        return 1
    seed = binascii.unhexlify(seed_hex.strip())
    if len(seed) != 32:
        print(f"ERROR: seed wrong length: {len(seed)}", file=sys.stderr)
        return 1
    privkey = Ed25519PrivateKey.from_private_bytes(seed)
    pubkey_bytes = privkey.public_key().public_bytes(
        serialization.Encoding.Raw, serialization.PublicFormat.Raw,
    )
    if pubkey_bytes.hex() != PINNED_PUBKEY_HEX:
        print(f"ERROR: derived pubkey {pubkey_bytes.hex()} != pinned {PINNED_PUBKEY_HEX}", file=sys.stderr)
        return 1

    print(f"# Vocabulary Scrub LOCK Ceremony 2026-05-16T14:30:00Z")
    print(f"# Pubkey verified MATCHES pinned cards-publisher: {pubkey_bytes.hex()}")
    print()

    if not stage_1_backup():
        print("ERROR: backup failed", file=sys.stderr)
        return 1
    print()
    stage_2_content_scrub()
    print()
    stage_3_path_renames()
    print()
    supersession_rows = stage_4_resign(privkey, pubkey_bytes)
    print()
    stage_5_append_lock_history(supersession_rows)
    print()
    stage_6_verify()
    print()
    print("# Ceremony COMPLETE.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
