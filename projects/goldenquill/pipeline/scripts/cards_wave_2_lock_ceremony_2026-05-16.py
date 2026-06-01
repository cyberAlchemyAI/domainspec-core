#!/usr/bin/env python3
"""Cards Wave 2 LOCK Ceremony — 12 thesis_passed cards.

Per operator directive 2026-05-16 (Wave 2 close synthesis at
pipeline/validation/cards_wave_2_thesis_2026-05-15/WAVE_2_CLOSE_SYNTHESIS.md).
Mirrors Wave 1 LOCK ceremony (rows 226/227) at 12-card scale.

Protocol (from Wave 1 in-file documentation, food_systems.yaml line 788-793):
  - Canonical-JSON form: sort_keys=True, separators=(",",":"), UTF-8, ensure_ascii=False
  - `_research_metadata.ed25519_signature` set to null in the canonical form
  - SHA3-512 of canonical-JSON bytes recorded as integrity hash
  - Ed25519 signature over canonical-JSON bytes (NOT the hash)
  - Signature target pubkey: vault_shared/cards/publisher_pubkey.signed.yaml
    (publisher_pubkey_ed25519_hex 0b1a0bbfa5ee9149af2c4e6153ed037dd03c0d562c94d3eaefeaf798e6f375bd)

For each card:
  1. Apply LOCK lifecycle edits (review_status passed, signature_status signed,
     runtime_load_status loaded, lock_history_row, lock_timestamp_utc, LOCK comment).
  2. Parse YAML; set ed25519_signature to None.
  3. Canonical-JSON serialize → SHA3-512 hex → Ed25519 sign canonical-JSON bytes.
  4. Verify with pinned publisher pubkey.
  5. Insert/replace ed25519_signature line + preceding integrity comment in YAML file.
  6. Record per-card audit row.

Then:
  7. Append 12 card rows + 1 §0.5 v29 paired-commit row (rows 250-262) to lock_history.v1.jsonl.
  8. Write §0.5 v29 amendment file.
  9. Print signature prefixes for operator handback.

Vocabulary note: post-scrub workspace uses "card" not "cartridge". lock_history.v1.jsonl
is PRESERVE_FILES — historical rows 226/227 retain "card_cartridge" lock_class and
"cartridge_*" key names. New Wave 2 rows use lock_class "card_cartridge" for
historical-query continuity but use post-scrub "card_*" field names for content.
"""
from __future__ import annotations

import os
import sys
import json
import hashlib
import datetime
from pathlib import Path

import yaml

from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey, Ed25519PublicKey,
)
from cryptography.hazmat.primitives import serialization

BASE = Path(os.environ.get("WORKSPACE_BASE", os.path.expanduser("~/Downloads/GoldenQuill")))
CEREMONY_TIMESTAMP = "2026-05-16T16:00:00Z"
PINNED_PUBKEY_HEX = "0b1a0bbfa5ee9149af2c4e6153ed037dd03c0d562c94d3eaefeaf798e6f375bd"

# Per Wave 1 row 226 + close-synthesis directive.
WAVE_2_CARDS = [
    # (slug, card_id, axis, file_path, schema_version, display_name, lock_history_row)
    ("educator",               "TILTH-CIC-02", "CIC", "pipeline/cards/CIC/educator.yaml",             "1.0-cic", "Educator",               250),
    ("public_agency",          "TILTH-CIC-03", "CIC", "pipeline/cards/CIC/public_agency.yaml",        "1.0-cic", "Public Agency",          251),
    ("arts_culture",           "TILTH-CIC-04", "CIC", "pipeline/cards/CIC/arts_culture.yaml",         "1.0-cic", "Arts & Culture",         252),
    ("cooperative",            "TILTH-CIC-05", "CIC", "pipeline/cards/CIC/cooperative.yaml",          "1.0-cic", "Cooperative",            253),
    ("ecosystem_intermediary", "TILTH-CIC-06", "CIC", "pipeline/cards/CIC/ecosystem_intermediary.yaml","1.0-cic", "Ecosystem Intermediary", 254),
    ("public_purpose_works",   "TILTH-CLC-01", "CLC", "pipeline/cards/CLC/public_purpose_works.yaml", "1.0-clc", "Public Purpose & Works", 255),
    ("catalytic_change",       "TILTH-CLC-02", "CLC", "pipeline/cards/CLC/catalytic_change.yaml",     "1.0-clc", "Catalytic Change",       256),
    ("research_evidence",      "TILTH-CLC-04", "CLC", "pipeline/cards/CLC/research_evidence.yaml",    "1.0-clc", "Research & Evidence",    257),
    ("market_access",          "TILTH-CLC-05", "CLC", "pipeline/cards/CLC/market_access.yaml",        "1.0-clc", "Market Access",          258),
    ("credit_underwriting",    "TILTH-CLC-06", "CLC", "pipeline/cards/CLC/credit_underwriting.yaml",  "1.0-clc", "Credit & Underwriting",  259),
    ("sponsorship_corporate",  "TILTH-CLC-07", "CLC", "pipeline/cards/CLC/sponsorship_corporate.yaml","1.0-clc", "Sponsorship & Corporate Support", 260),
    ("shared_assets",          "TILTH-CLC-08", "CLC", "pipeline/cards/CLC/shared_assets.yaml",        "1.0-clc", "Shared Assets",          261),
]
SECTION_00_5_V29_ROW = 262

LOCK_COMMENT_TEMPLATE = """\
  # LOCK ceremony 2026-05-16 PM after L-005 two-cycle audit closed at
  # pipeline/validation/cards_wave_2_thesis_2026-05-15/{axis_dir}/{slug}/FINAL_VERDICT.md
  # (THESIS_PASSED). review_status flipped pending→passed; signature_status
  # unsigned→signed; runtime_load_status not_loaded→loaded. Operator publisher
  # pubkey pinned at vault_shared/cards/publisher_pubkey.signed.yaml. The
  # ed25519_signature in _research_metadata is the operator Ed25519 signature
  # over canonical-JSON of this YAML with ed25519_signature: null. OD-F + OD-H
  # operator-decisions resolved pre-ceremony (cards LOCKed as-on-disk per
  # operator directive 2026-05-16)."""


def derive_pubkey(seed_hex: str) -> bytes:
    seed = bytes.fromhex(seed_hex.strip())
    if len(seed) != 32:
        raise ValueError(f"Seed must be 32 bytes, got {len(seed)}")
    sk = Ed25519PrivateKey.from_private_bytes(seed)
    pk_bytes = sk.public_key().public_bytes(
        serialization.Encoding.Raw, serialization.PublicFormat.Raw,
    )
    return pk_bytes


def apply_lifecycle_edits(*, text: str, row: int, axis_dir: str, slug: str) -> str:
    """Apply LOCK lifecycle flips and insert lock_history_row + lock_timestamp_utc + LOCK comment.

    Surgical text edits preserve all comments and formatting. The current lifecycle block
    pattern for all 12 cards (verified pre-ceremony) is:

        lifecycle:
          draft_status: "draft"
          review_status: "pending"
          cross_family_thesis_status: "passed"
          signature_status: "unsigned"
          runtime_load_status: "not_loaded"

    Some cards have trailing comments after runtime_load_status — these are preserved
    by inserting new fields BEFORE any existing trailing comments.
    """
    # Flip three status fields.
    replacements = [
        ('  review_status: "pending"', '  review_status: "passed"'),
        ('  signature_status: "unsigned"', '  signature_status: "signed"'),
    ]
    for old, new in replacements:
        if old not in text:
            raise RuntimeError(f"Cannot find lifecycle field: {old!r} in {slug}")
        text = text.replace(old, new, 1)

    # Replace runtime_load_status + insert lock_history_row + lock_timestamp_utc + LOCK comment.
    lock_comment = LOCK_COMMENT_TEMPLATE.format(axis_dir=axis_dir, slug=slug)
    old = '  runtime_load_status: "not_loaded"'
    new = (
        '  runtime_load_status: "loaded"\n'
        f'  lock_history_row: {row}\n'
        f'  lock_timestamp_utc: "{CEREMONY_TIMESTAMP}"\n'
        f'{lock_comment}'
    )
    if old not in text:
        raise RuntimeError(f"Cannot find runtime_load_status line in {slug}")
    text = text.replace(old, new, 1)
    return text


def canonical_json_for_signing(*, yaml_text: str) -> tuple[bytes, str]:
    """Parse YAML, set _research_metadata.ed25519_signature to None, canonical-JSON serialize.

    Returns (canonical_bytes, sha3_512_hex).

    Per Wave 1 in-file protocol: sort_keys=True, separators=(",", ":"),
    UTF-8, ensure_ascii=False.
    """
    parsed = yaml.safe_load(yaml_text)
    if "_research_metadata" not in parsed:
        raise RuntimeError("_research_metadata block missing from card YAML")
    parsed["_research_metadata"]["ed25519_signature"] = None
    canonical = json.dumps(
        parsed, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    sha3_512_hex = hashlib.sha3_512(canonical).hexdigest()
    return canonical, sha3_512_hex


def embed_signature(*, text: str, sig_hex: str, sha3_hex: str, axis: str) -> str:
    """Embed the signature + integrity comment block into the YAML file.

    Two cases:
      - CLC cards (7): replace existing `  ed25519_signature: null` line with sig + comment.
      - CIC cards (5): insert sig + comment before the `  # common_clc_patterns_observed`
                        comment block that ends _research_metadata.
    """
    comment_block = (
        f"\n"
        f"  # Ed25519 signature over canonical-JSON of this YAML with this field set to\n"
        f"  # null. Canonical-JSON form: sorted keys, compact separators (\",\",\":\"), UTF-8,\n"
        f"  # ensure_ascii=False. Canonical-JSON SHA3-512 (for white-glove integrity\n"
        f"  # pinning): {sha3_hex}\n"
        f"  # Signature target pubkey: vault_shared/cards/publisher_pubkey.signed.yaml\n"
        f"  # (publisher_pubkey_ed25519_hex {PINNED_PUBKEY_HEX})\n"
        f"  ed25519_signature: \"{sig_hex}\"\n"
    )
    if axis == "CLC":
        # CLC cards have `  ed25519_signature: null` placeholder already.
        old = "\n  ed25519_signature: null\n"
        if old not in text:
            raise RuntimeError("Expected CLC placeholder not found")
        return text.replace(old, comment_block, 1)
    else:
        # CIC cards: insert before "  # common_clc_patterns_observed — INTENTIONALLY ABSENT."
        anchor = "  # common_clc_patterns_observed — INTENTIONALLY ABSENT."
        if anchor not in text:
            raise RuntimeError("Expected CIC anchor comment not found")
        # Insert comment_block + newline before anchor
        return text.replace(anchor, comment_block.lstrip("\n") + "\n" + anchor, 1)


def build_card_lock_history_row(
    *, row: int, card_idx: int, total: int, slug: str, card_id: str, axis: str,
    file_path: str, schema_version: str, display_name: str,
    sha3_hex: str, sig_hex: str,
) -> dict:
    """Build per-card lock_history row mirroring row 226 structure.

    Post-scrub vocab: card_* field names. lock_class "card_cartridge" preserved
    for historical-query continuity with row 226/227.
    """
    return {
        "row": row,
        "lock_timestamp_utc": CEREMONY_TIMESTAMP,
        "lock_class": "card_cartridge",
        "lock_kind": f"compound-paired-commit-thirteen-member-{card_idx + 1}",
        "lock_cycle": f"Cards Wave 2 card LOCK ceremony — {card_id} {display_name}",
        "lock_mode": (
            f"COMPOUND-LOCK sibling {card_idx + 1}/13 — paired with 11 other Wave 2 cards "
            f"+ §0.5 v29 paired-commit at the same lock_timestamp_utc per §6.17 Option-B. "
            f"Wave 2 LOCK ceremony at 12-card scale follows Wave 1 (rows 226/227) precedent. "
            f"OD-F (CIC-05 named-org cleanup) resolved pre-ceremony via Phase D A.1 full anonymization "
            f"(2026-05-16T14:00:00Z); OD-H (CIC-03/CIC-04 racial-justice severity) confirmed both HIGH per "
            f"close-synthesis Phase A.2 refresh — both decisions land cards as-on-disk."
        ),
        "module": f"pipeline.cards.{axis}.{slug}",
        "card_file": file_path,
        "card_id": card_id,
        "card_slug": slug,
        "card_axis": axis,
        "card_schema_version": schema_version,
        "parent_lock_row": None,
        "parent_thesis_round": f"pipeline/validation/cards_wave_2_thesis_2026-05-15/{axis}/{slug}/FINAL_VERDICT.md",
        "thesis_verdict": "THESIS_PASSED",
        "predecessor_amendments_chain": [
            "Cards Wave 1 LOCK rows 226/227 (TILTH-CIC-01 food_systems + TILTH-CLC-03 operating_capacity)",
            "§18 v1.1 narrow-corrective row 229 (Wave 1 schema refinement)",
            "§18 v1.2 narrow-corrective row 235 (dialect_routing_table item-shape extension under v7.0.12)",
            "Cards Wave 2 Thesis dispatch 2026-05-15 (12 cards × 2 cycles × 3 seats = 72 reviewer dispatches)",
            "Vocab scrub supersession ceremony 2026-05-16T14:30:00Z rows 238-249 (cartridge → card workspace-wide)",
        ],
        "amendment_class": "wave-2-card-class-LOCK + post-vocab-scrub-precedent",
        "compound_lock_with": [c[3] for c in WAVE_2_CARDS if c[6] != row] + [
            "pipeline/blueprint/v0.1/section_00_5_cards_wave_2_amendment.md",
        ],
        "lifecycle_transition": "draft → reviewed → thesis_passed → signed → loaded",
        "signature_target_pubkey": "vault_shared/cards/publisher_pubkey.signed.yaml",
        "publisher_pubkey_ed25519_hex": PINNED_PUBKEY_HEX,
        "canonical_json_sha3_512": sha3_hex,
        "ed25519_signature": sig_hex,
        "model_tier": "operator + cross-family-thesis-passed",
        "operator": "Josh Inklovich",
        "review_verdict": (
            f"LOCKED — {card_id} {display_name} Wave 2 card; lifecycle.signature_status: signed + "
            f"runtime_load_status: loaded. L-005 strict two-cycle CROSS-FAMILY Thesis CLOSED "
            f"(Editor groq/llama-3.3-70b-versatile + Judge google/gemini-2.5-pro + Red Team "
            f"groq/openai/gpt-oss-120b); per-card disposition counts in FINAL_VERDICT.md "
            f"(see close-synthesis Wave 2 totals: 88 Cycle-1 folds + 34 Cycle-2 fix-in-place + 12 "
            f"lifecycle flips = 134 cross-Wave card edits). Wave-wide ODs disposition: OD-F resolved "
            f"pre-ceremony via Phase D A.1 full anonymization (Cooperation Jackson / USFWC / DAWI / "
            f"Industrial Commons / Highlander removed entirely per Law 5 substance discipline, not "
            f"relocated); OD-H racial-justice severity confirmed both HIGH per Phase A.2 refresh; "
            f"OD-A/B/C/D/E/G/I deferred to post-LOCK follow-on dispatches."
        ),
        "audit_trail": f"pipeline/validation/cards_wave_2_thesis_2026-05-15/{axis}/{slug}/",
        "ceremony_audit_trail": "pipeline/validation/cards_wave_2_lock_ceremony_2026-05-16/",
        "cross_family_posture": (
            "LIVE FULL CROSS-FAMILY (no Section E carve-out). Three distinct provider families: "
            "Meta (Llama-3.3-70B / Editor) + Google (Gemini-2.5-Pro / Judge) + OpenAI-OSS "
            "(gpt-oss-120b / Red Team); no family-overlap with Anthropic author."
        ),
        "od_dispositions": {
            "OD-F-named-org-relocation": "resolved-pre-ceremony-via-full-anonymization-2026-05-16T14:00:00Z (operator directive)",
            "OD-H-racial-justice-severity": "confirmed-defensible-both-HIGH-per-Phase-A.2-refresh",
            "OD-A-admin-risk-register-v2.3": "deferred-to-post-LOCK-follow-on-dispatch",
            "OD-B-R-CARDS-ENUM-CANONICAL": "deferred-to-§4-v2.x.y-follow-on-amendment",
            "OD-C-coupling-violation-extension": "deferred-to-post-LOCK-follow-on-dispatch",
            "OD-D-fold-in-discipline-checklist": "deferred-to-§18.11-Phase-4-documentation",
            "OD-E-dual-track-structural-separation": "deferred-to-§18.6-schema-amendment",
            "OD-G-state-overlay-amendment": "deferred-to-v1.x",
            "OD-I-defer-to-active-RFA-cross-CIC": "deferred-to-cross-card-documentation-only-refinement",
        },
        "verdict": (
            f"WAVE-2-LOCK — {card_id} {display_name} promoted to signed + loaded; "
            f"row {row} of 12-card Wave 2 LOCK ceremony + §0.5 v29 paired-commit at row {SECTION_00_5_V29_ROW}."
        ),
    }


def build_section_00_5_v29_row(*, row: int) -> dict:
    return {
        "row": row,
        "lock_timestamp_utc": CEREMONY_TIMESTAMP,
        "lock_class": "blueprint-interface-index",
        "lock_kind": "compound-paired-commit-thirteen-member-13",
        "lock_cycle": (
            "§0.5 v29 paired-commit with Cards Wave 2 LOCK ceremony "
            "(12 per-card primitive_id signature_status: signed flips)"
        ),
        "lock_mode": (
            "COMPOUND-LOCK sibling 13/13 — paired with 12 Wave 2 card LOCKs at the same "
            "lock_timestamp_utc per §6.17 Option-B. Mirrors §0.5 v25 (Wave 1) precedent at "
            "row 228. Pinned-mode-narrow-corrective: flips signature_status from unsigned to "
            "signed for 12 already-registered primitive_ids (no new namespace registration; "
            "all 14 card namespaces registered in §0.5 v25 rows 537-550). No new vocabulary kind."
        ),
        "module": "pipeline.blueprint.v0_1.section_00_5_cards_wave_2_amendment",
        "amendment_file": "pipeline/blueprint/v0.1/section_00_5_cards_wave_2_amendment.md",
        "amendment_class": "§0.5-paired-commit-narrow-corrective (signature_status flip-only, no new rows)",
        "parent_amendment_chain": [
            "§0.5 v25 LOCKED 2026-05-15 row 228 (Wave 1 paired-commit)",
            "§0.5 v26 LOCKED 2026-05-16 row 230 (§18 v1.1)",
            "§0.5 v27 LOCKED 2026-05-16 row 233 (CC-007 §4 v2.x.5)",
            "§0.5 v28 LOCKED 2026-05-16 row 237 (v7.0.12 apolitical-dialect)",
        ],
        "primitive_id_updates": [
            {
                "primitive_id": f"cards.{c[2].lower()}.{c[0]}.v1",
                "field": "signature_status",
                "before": "unsigned",
                "after": "signed",
                "card_lock_row": c[6],
            }
            for c in WAVE_2_CARDS
        ],
        "runtime_live_pre_lock": 538,
        "runtime_live_post_lock": 538,
        "publisher_pubkey_ed25519_hex": PINNED_PUBKEY_HEX,
        "operator": "Josh Inklovich",
        "model_tier": "operator",
        "ceremony_audit_trail": "pipeline/validation/cards_wave_2_lock_ceremony_2026-05-16/",
        "verdict": (
            f"§0.5 v29 LOCKED — 12 per-card primitive_id signature_status flipped unsigned→signed "
            f"at compound Wave 2 LOCK ceremony (rows 250-261). §0.5 itself remains at runtime-live 538 "
            f"(no new rows; only existing-row attribute updates)."
        ),
    }


def main() -> int:
    seed_hex = os.environ.get("OPERATOR_SEED_HEX")
    if not seed_hex:
        print("ERROR: OPERATOR_SEED_HEX env not set", file=sys.stderr)
        return 1
    seed = bytes.fromhex(seed_hex.strip())
    if len(seed) != 32:
        print(f"ERROR: seed wrong length: {len(seed)}", file=sys.stderr)
        return 1
    sk = Ed25519PrivateKey.from_private_bytes(seed)
    pk_bytes = sk.public_key().public_bytes(
        serialization.Encoding.Raw, serialization.PublicFormat.Raw,
    )
    if pk_bytes.hex() != PINNED_PUBKEY_HEX:
        print(f"ERROR: derived pubkey {pk_bytes.hex()} != pinned {PINNED_PUBKEY_HEX}", file=sys.stderr)
        return 1
    pubkey = Ed25519PublicKey.from_public_bytes(pk_bytes)
    print(f"# Cards Wave 2 LOCK Ceremony {CEREMONY_TIMESTAMP}")
    print(f"# Pubkey verified MATCHES pinned cards-publisher: {pk_bytes.hex()}")
    print()

    # Audit trail directory
    audit_dir = BASE / "pipeline/validation/cards_wave_2_lock_ceremony_2026-05-16"
    audit_dir.mkdir(parents=True, exist_ok=True)
    (audit_dir / "backup").mkdir(exist_ok=True)
    audit_log = audit_dir / "ceremony_log.txt"

    log_lines = []
    def log(msg):
        print(msg)
        log_lines.append(msg)

    log("## Stage 1: Backup current card YAMLs")
    for slug, _, _, fp, *_ in WAVE_2_CARDS:
        src = BASE / fp
        dst = audit_dir / "backup" / f"{slug}_pre_lock.yaml"
        dst.write_bytes(src.read_bytes())
    log(f"  Backed up 12 cards to {audit_dir / 'backup'}")
    log("")

    log("## Stage 2: Apply LOCK edits + sign each card")
    rows_to_append = []
    sig_summary = []
    for idx, (slug, card_id, axis, fp, schema_v, display_name, row) in enumerate(WAVE_2_CARDS):
        full = BASE / fp
        original = full.read_text()
        axis_dir = axis
        # Step 1: apply lifecycle edits
        post_edit = apply_lifecycle_edits(text=original, row=row, axis_dir=axis_dir, slug=slug)
        # Step 2: parse + canonicalize (with ed25519_signature: null)
        canonical, sha3_hex = canonical_json_for_signing(yaml_text=post_edit)
        # Step 3: sign canonical bytes
        sig_bytes = sk.sign(canonical)
        sig_hex = sig_bytes.hex()
        # Step 4: verify
        try:
            pubkey.verify(sig_bytes, canonical)
            verified = True
        except Exception as e:
            verified = False
            log(f"  ERROR: signature verification FAILED for {slug}: {e}")
            return 2
        # Step 5: embed signature + comment in YAML
        final_text = embed_signature(text=post_edit, sig_hex=sig_hex, sha3_hex=sha3_hex, axis=axis)
        full.write_text(final_text)
        # Step 6: re-parse final file + re-canonicalize + verify sig still validates
        reparse_canonical, reparse_sha3 = canonical_json_for_signing(yaml_text=final_text)
        if reparse_sha3 != sha3_hex:
            log(f"  ERROR: round-trip sha3 mismatch for {slug}: {reparse_sha3} != {sha3_hex}")
            return 3
        # Build lock_history row
        lh_row = build_card_lock_history_row(
            row=row, card_idx=idx, total=12, slug=slug, card_id=card_id, axis=axis,
            file_path=fp, schema_version=schema_v, display_name=display_name,
            sha3_hex=sha3_hex, sig_hex=sig_hex,
        )
        rows_to_append.append(lh_row)
        sig_summary.append({
            "slug": slug, "card_id": card_id, "row": row,
            "sha3_512_hex": sha3_hex, "sig_hex": sig_hex,
            "sig_prefix": sig_hex[:16], "verified": verified,
            "file_path": fp,
        })
        log(f"  row{row}  {card_id} {slug:30s} sha3={sha3_hex[:16]}... sig={sig_hex[:16]}... verified={verified}")
    log("")

    log("## Stage 3: Append §0.5 v29 paired-commit row")
    section_00_5_row = build_section_00_5_v29_row(row=SECTION_00_5_V29_ROW)
    rows_to_append.append(section_00_5_row)
    log(f"  row{SECTION_00_5_V29_ROW}  §0.5 v29 paired-commit (blueprint-interface-index)")
    log("")

    log("## Stage 4: Append 13 rows to lock_history.v1.jsonl")
    lh_path = BASE / "pipeline/engineering/lock_history.v1.jsonl"
    # Check current tail row
    with lh_path.open() as f:
        existing_rows = [int(json.loads(l)["row"]) for l in f if l.strip()]
    max_existing = max(existing_rows) if existing_rows else 0
    log(f"  Pre-append max row: {max_existing}; Wave 2 first row: {WAVE_2_CARDS[0][6]}")
    if WAVE_2_CARDS[0][6] != max_existing + 1:
        log(f"  ERROR: row collision — expected start row {max_existing + 1}, got {WAVE_2_CARDS[0][6]}")
        log(f"  HARD STOP: aborting append. Inspect lock_history.v1.jsonl tail and rebase row numbers.")
        return 4
    with lh_path.open("a") as f:
        for r in rows_to_append:
            f.write(json.dumps(r) + "\n")
    log(f"  Appended {len(rows_to_append)} rows")
    log("")

    log("## Stage 5: Write §0.5 v29 amendment file")
    section_00_5_v29_file = BASE / "pipeline/blueprint/v0.1/section_00_5_cards_wave_2_amendment.md"
    section_00_5_v29_content = render_section_00_5_v29(sig_summary, section_00_5_row)
    section_00_5_v29_file.write_text(section_00_5_v29_content)
    log(f"  Wrote {section_00_5_v29_file.relative_to(BASE)} ({len(section_00_5_v29_content)} bytes)")
    log("")

    log("## Stage 6: Write per-card signature summary to audit trail")
    sig_summary_path = audit_dir / "signature_summary.json"
    sig_summary_path.write_text(json.dumps({
        "ceremony_timestamp_utc": CEREMONY_TIMESTAMP,
        "publisher_pubkey_ed25519_hex": PINNED_PUBKEY_HEX,
        "lock_history_rows": [c["row"] for c in rows_to_append],
        "section_00_5_v29_row": SECTION_00_5_V29_ROW,
        "cards": sig_summary,
    }, indent=2))
    log(f"  Wrote {sig_summary_path.relative_to(BASE)}")
    log("")

    log("## Stage 7: Final verification — re-read each YAML, verify embedded sig")
    all_verified = True
    for sm in sig_summary:
        text = (BASE / sm["file_path"]).read_text()
        canonical, sha3 = canonical_json_for_signing(yaml_text=text)
        if sha3 != sm["sha3_512_hex"]:
            log(f"  FAIL {sm['slug']}: SHA3 drift {sha3[:20]} != {sm['sha3_512_hex'][:20]}")
            all_verified = False
            continue
        try:
            pubkey.verify(bytes.fromhex(sm["sig_hex"]), canonical)
            log(f"  OK   {sm['slug']:30s} sig verifies against pinned pubkey")
        except Exception as e:
            log(f"  FAIL {sm['slug']}: {e}")
            all_verified = False
    if not all_verified:
        log("  HARD STOP: at least one card failed final verification")
        return 5
    log("  All 12 cards verified.")

    audit_log.write_text("\n".join(log_lines) + "\n")
    print()
    print("# Ceremony COMPLETE.")
    print(f"# Audit trail: {audit_dir.relative_to(BASE)}")
    return 0


def render_section_00_5_v29(sig_summary, section_00_5_row):
    """Render the §0.5 v29 amendment file content."""
    lines = [
        "---",
        f"title: §0.5 v29 — Interface Index paired-commit for Cards Wave 2 LOCK ceremony (12-card signature_status flip)",
        f"filed: 2026-05-16",
        f"operator: Josh Inklovich",
        f"status: LOCKED 2026-05-16T16:00:00Z at lock_history row {SECTION_00_5_V29_ROW}",
        f"parent_locks:",
        f"  - pipeline/blueprint/v0.1/section_00_5_apolitical_dialect_amendment.md       # §0.5 v28 LOCKED 2026-05-16 row 237 (predecessor)",
        f"  - pipeline/blueprint/v0.1/section_00_5_section_18_cards_wave_1_paired_commit_amendment.md  # §0.5 v25 LOCKED 2026-05-15 row 228 (Wave 1 precedent)",
        f"compound_lock_with: 12 Wave 2 card LOCKs (rows 250-261) at the same lock_timestamp_utc per §6.17 Option-B",
        f"amendment_class: §0.5-paired-commit-narrow-corrective (signature_status flip-only, no new rows)",
        f"target_lock_row: {SECTION_00_5_V29_ROW}",
        f"runtime_live_pre_lock: 538",
        f"runtime_live_post_lock: 538",
        f"session_metrics: pipeline/metrics/session_log.jsonl",
        f"---",
        f"",
        f"# §0.5 v29 — Interface Index amendment for Cards Wave 2 LOCK ceremony",
        f"",
        f"## §0.5.v29.0 Amendment intent",
        f"",
        f"This amendment is a paired-commit with the Cards Wave 2 LOCK ceremony (12 cards "
        f"LOCKed at rows 250-261 of lock_history.v1.jsonl at compound timestamp `{CEREMONY_TIMESTAMP}`).",
        f"",
        f"**No new primitive_id rows are appended to §0.5.** All 14 card namespaces (6 CIC + 8 CLC) "
        f"were already registered in §0.5 v25 at LOCK rows 537-550. This amendment is a narrow-corrective "
        f"`signature_status` flip on the 12 Wave 2 card primitives — Wave 1 (food_systems + operating_capacity) "
        f"already flipped at §0.5 v25 LOCK.",
        f"",
        f"**Vocabulary check.** No new `kind` values introduced. All updates land within the existing "
        f"`card-namespace` kind registered at §0.5 v25.",
        f"",
        f"## §0.5.v29.1 — Per-primitive signature_status flips (12 entries)",
        f"",
        f"| primitive_id | field | before | after | card_lock_row |",
        f"|---|---|---|---|---|",
    ]
    for c in WAVE_2_CARDS:
        slug, card_id, axis, fp, schema_v, display_name, row = c
        pid = f"cards.{axis.lower()}.{slug}.v1"
        lines.append(f"| `{pid}` | `signature_status` | `unsigned` | `signed` | {row} |")
    lines += [
        f"",
        f"## §0.5.v29.2 — Per-card audit pointer",
        f"",
        f"Each of the 12 Wave 2 cards is signed with operator publisher Ed25519 key (pinned at "
        f"`vault_shared/cards/publisher_pubkey.signed.yaml`, pubkey hex `{PINNED_PUBKEY_HEX}`). "
        f"Per-card signature + canonical-JSON SHA3-512 recorded in lock_history rows 250-261. "
        f"Audit trail at `pipeline/validation/cards_wave_2_lock_ceremony_2026-05-16/`.",
        f"",
        f"| card_id | slug | lock_history_row | sig prefix (16 hex) | sha3 prefix (16 hex) |",
        f"|---|---|---|---|---|",
    ]
    for sm in sig_summary:
        lines.append(f"| {sm['card_id']} | {sm['slug']} | {sm['row']} | `{sm['sig_prefix']}` | `{sm['sha3_512_hex'][:16]}` |")
    lines += [
        f"",
        f"## §0.5.v29.3 — Operator-decision dispositions (Wave 2 close synthesis)",
        f"",
        f"- **OD-F** (CIC-05 named-org cleanup): resolved pre-ceremony via Phase D A.1 full anonymization "
        f"(named soul_fire orgs Cooperation Jackson / USFWC / DAWI / Industrial Commons / Highlander removed "
        f"entirely per operator directive 2026-05-16T14:00:00Z, not relocated). Per Law 5 substance discipline.",
        f"- **OD-H** (CIC-03/CIC-04 racial-justice severity): confirmed defensible per Phase A.2 refresh — "
        f"both CIC-03 public_agency and CIC-04 arts_culture carry `racial justice = HIGH` (original CC-8 "
        f"finding stale; refreshed flag is `DEI / equity / inclusion` HIGH on CIC-02 + CIC-04 vs MED on "
        f"CIC-03 + CIC-05, applied as-authored).",
        f"- **OD-A/B/C/D/E/G/I**: deferred to post-LOCK follow-on dispatches (see Wave 2 close synthesis).",
        f"",
        f"## §0.5.v29.4 — LOCK metadata",
        f"",
        f"- LOCK timestamp: `{CEREMONY_TIMESTAMP}`",
        f"- LOCK row: {SECTION_00_5_V29_ROW}",
        f"- Publisher pubkey: `{PINNED_PUBKEY_HEX}`",
        f"- Compound-LOCK with: 12 Wave 2 card rows (250-261)",
        f"- Ceremony audit trail: `pipeline/validation/cards_wave_2_lock_ceremony_2026-05-16/`",
    ]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    sys.exit(main())
