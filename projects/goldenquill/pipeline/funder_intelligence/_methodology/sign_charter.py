"""FID Pillar-1 Depth-Charter signing helper.

Per `pipeline/funder_intelligence/pillar_1_charters/README.md` §"[P1: signing
helper]" + Codex external-validity audit
`pipeline/validation/review_qa_validity_audit_2026-05-18/findings.md` §P1.

The helper canonicalizes a Pillar-1 Depth Charter markdown file, computes its
SHA3-512 content hash, accepts an operator-provided Ed25519 signature via
``--signature-hex``, and writes the signed file at
``<charter_id>_charter_v1_SIGNED.md`` (renaming the v0 DRAFT). It NEVER touches
private key material — the operator runs the Ed25519 signature step offline
against the FID publisher private key and pastes the hex signature in.

Canonicalization (mirrors Cards / WPFA / Reflection Packet convention via
``pipeline/scripts/cards_publisher_key_rotation_ceremony_2026-05-17.py``):

  1. Read the charter markdown bytes verbatim.
  2. Replace the signature block in §7 with the placeholder shape (all four
     signature fields set to ``<pending_operator_attestation>``) so the
     canonical bytes are stable regardless of when the operator signs.
  3. UTF-8 encode the result. These are the canonical bytes.
  4. SHA3-512 the canonical bytes → ``content_hash_sha3_512_hex``.
  5. Operator's Ed25519 signature targets the canonical bytes (the hex
     signature passed in via ``--signature-hex`` must verify against the FID
     publisher pubkey when applied to these bytes).

Output workflow:

  python -m pipeline.funder_intelligence._methodology.sign_charter \\
      <path/to/<id>_charter_v0_DRAFT.md> \\
      --dry-run

    Prints content_hash_sha3_512_hex + the canonical bytes (no file changes).
    Operator runs Ed25519 sign on those bytes against their private key.

  python -m pipeline.funder_intelligence._methodology.sign_charter \\
      <path/to/<id>_charter_v0_DRAFT.md> \\
      --signer-pubkey-fingerprint <hex> \\
      --signature-hex <hex> \\
      --signed-at 2026-05-18T20:00:00Z

    Verifies signature against the pinned FID publisher pubkey at
    ``vault_shared/funder_intelligence/publisher_pubkey.signed.yaml``,
    fills §7 block, renames file to ``<id>_charter_v1_SIGNED.md``,
    updates the MANIFEST entry's sig status.

Exit codes:

  0  success — file signed + renamed + MANIFEST updated
  1  bad CLI args / file not found / charter shape invalid
  2  signature failed Ed25519 verify against pinned FID publisher pubkey
  3  MANIFEST regen failed
  4  file already at SIGNED state (idempotent guard)
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import pathlib
import re
import sys
from typing import Tuple

try:
    import yaml
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
except ImportError as e:  # pragma: no cover - imported by tests under venv
    print(f"ERROR: missing dep ({e}); install via `pip install pyyaml cryptography`.", file=sys.stderr)
    sys.exit(1)


REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
CHARTERS_DIR = REPO_ROOT / "pipeline" / "funder_intelligence" / "pillar_1_charters"
MANIFEST = CHARTERS_DIR / "MANIFEST.md"
PUBKEY_YAML = REPO_ROOT / "vault_shared" / "funder_intelligence" / "publisher_pubkey.signed.yaml"

PLACEHOLDER = "<pending_operator_attestation>"
SIGNATURE_BLOCK_PATTERN = re.compile(
    r"```yaml\s*\n"
    r"charter_signed_at:\s*[^\n]*\n"
    r"charter_signed_by_pubkey:\s*[^\n]*\n"
    r"charter_signed_canonical_bytes_sha3_512:\s*[^\n]*\n"
    r"charter_ed25519_signature:\s*[^\n]*\n"
    r"```",
    re.MULTILINE,
)


def canonicalize_charter(raw_bytes: bytes) -> bytes:
    """Replace signature block fields with placeholder shape → return canonical bytes."""
    text = raw_bytes.decode("utf-8")
    placeholder_block = (
        "```yaml\n"
        f"charter_signed_at: {PLACEHOLDER}\n"
        f"charter_signed_by_pubkey: {PLACEHOLDER}\n"
        f"charter_signed_canonical_bytes_sha3_512: {PLACEHOLDER}\n"
        f"charter_ed25519_signature: {PLACEHOLDER}\n"
        "```"
    )
    replaced, count = SIGNATURE_BLOCK_PATTERN.subn(placeholder_block, text)
    if count == 0:
        raise ValueError(
            "Charter has no parseable §7 signature block. Expected a fenced ```yaml block "
            "with charter_signed_at / charter_signed_by_pubkey / "
            "charter_signed_canonical_bytes_sha3_512 / charter_ed25519_signature fields."
        )
    if count > 1:
        raise ValueError(f"Charter has {count} signature blocks; expected exactly 1.")
    return replaced.encode("utf-8")


def content_hash(canonical_bytes: bytes) -> str:
    return hashlib.sha3_512(canonical_bytes).hexdigest()


def load_pinned_pubkey() -> Tuple[str, Ed25519PublicKey]:
    """Load + parse the pinned FID publisher pubkey.

    Returns (fingerprint_hex, parsed_pubkey).
    Falls back to a stub when the pinned YAML doesn't exist yet (early-bootstrap;
    tests pass an explicit pubkey to bypass).
    """
    if not PUBKEY_YAML.exists():
        raise FileNotFoundError(f"FID publisher pubkey not pinned at {PUBKEY_YAML}")
    data = yaml.safe_load(PUBKEY_YAML.read_text())
    pubkey_hex = data.get("publisher_pubkey_ed25519_hex") or data.get("pubkey_hex")
    if not pubkey_hex:
        raise ValueError(
            f"{PUBKEY_YAML} does not contain publisher_pubkey_ed25519_hex; "
            f"keys present: {list(data.keys()) if isinstance(data, dict) else 'not a dict'}"
        )
    return pubkey_hex, Ed25519PublicKey.from_public_bytes(bytes.fromhex(pubkey_hex))


def verify_signature(canonical_bytes: bytes, signature_hex: str, pubkey: Ed25519PublicKey) -> bool:
    try:
        pubkey.verify(bytes.fromhex(signature_hex), canonical_bytes)
        return True
    except Exception:
        return False


def write_signed_charter(
    charter_path: pathlib.Path,
    canonical_bytes: bytes,
    content_hash_hex: str,
    signer_pubkey_fingerprint: str,
    signature_hex: str,
    signed_at: str,
) -> pathlib.Path:
    """Write signed charter at the _v1_SIGNED path; return the new path."""
    text = canonical_bytes.decode("utf-8")
    signed_block = (
        "```yaml\n"
        f"charter_signed_at: {signed_at}\n"
        f"charter_signed_by_pubkey: {signer_pubkey_fingerprint}\n"
        f"charter_signed_canonical_bytes_sha3_512: {content_hash_hex}\n"
        f"charter_ed25519_signature: {signature_hex}\n"
        "```"
    )
    final_text, count = SIGNATURE_BLOCK_PATTERN.subn(signed_block, text)
    if count != 1:
        raise RuntimeError(f"Unexpected signature-block substitution count: {count}")

    new_name = charter_path.name.replace("_charter_v0_DRAFT.md", "_charter_v1_SIGNED.md")
    new_path = charter_path.parent / new_name
    if new_path.exists():
        raise RuntimeError(f"Refusing to overwrite existing signed file at {new_path}")
    new_path.write_text(final_text)
    charter_path.unlink()  # remove v0 DRAFT (preserved in git history)
    return new_path


def regenerate_manifest_entry(charter_path: pathlib.Path, content_hash_hex: str) -> None:
    """Update the MANIFEST.md row for this charter's lifecycle + sig hash prefix."""
    if not MANIFEST.exists():
        raise FileNotFoundError(f"MANIFEST not at {MANIFEST}")
    artifact_id_match = re.match(r"^(.+)_charter_v1_SIGNED\.md$", charter_path.name)
    if not artifact_id_match:
        raise RuntimeError(f"Path does not match _charter_v1_SIGNED.md convention: {charter_path.name}")
    artifact_id = artifact_id_match.group(1)
    sig_prefix = content_hash_hex[:16]

    manifest_text = MANIFEST.read_text()
    # Pattern: row containing the artifact_id + DRAFT v0 + placeholder sig status
    # Replace lifecycle column "DRAFT v0" → "SIGNED v1" and sig-status column
    # with sig hash prefix.
    row_pattern = re.compile(
        rf"(\|\s*\d+\s*\|\s*`{re.escape(artifact_id)}`.*?\|)\s*DRAFT v0\s*\|\s*`<pending_operator_attestation>`\s*\|",
    )
    new_text, count = row_pattern.subn(
        rf"\1 SIGNED v1 | `{sig_prefix}…` |",
        manifest_text,
    )
    if count == 0:
        raise RuntimeError(f"No MANIFEST row matched for {artifact_id}")
    MANIFEST.write_text(new_text)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="FID Pillar-1 Depth-Charter signing helper "
        "(canonicalize + hash + apply operator Ed25519 signature + rename + MANIFEST regen).",
    )
    p.add_argument("charter_path", type=pathlib.Path, help="Path to the *_charter_v0_DRAFT.md file.")
    p.add_argument(
        "--signer-pubkey-fingerprint",
        help="Hex fingerprint of the FID publisher pubkey the operator signed with. "
        "Must match the pinned pubkey at vault_shared/funder_intelligence/publisher_pubkey.signed.yaml.",
    )
    p.add_argument(
        "--signature-hex",
        help="Operator-provided Ed25519 signature in hex over the canonical bytes "
        "(see --dry-run to surface the bytes).",
    )
    p.add_argument(
        "--signed-at",
        default=None,
        help="UTC ISO-8601 timestamp for the signature. Defaults to now() in UTC.",
    )
    p.add_argument(
        "--dry-run",
        action="store_true",
        help="Print canonical bytes hash + the bytes themselves, do not modify any files. "
        "Use this to get the bytes for offline Ed25519 signing.",
    )
    p.add_argument(
        "--allow-missing-pubkey-yaml",
        action="store_true",
        help="(Testing.) Skip pinned-pubkey verification; trust --signer-pubkey-fingerprint verbatim. "
        "DO NOT use in production signing ceremony.",
    )
    args = p.parse_args(argv)

    if not args.charter_path.exists():
        print(f"ERROR: charter not found at {args.charter_path}", file=sys.stderr)
        return 1
    if args.charter_path.name.endswith("_charter_v1_SIGNED.md"):
        print(f"ERROR: charter already signed (idempotent guard): {args.charter_path}", file=sys.stderr)
        return 4

    raw = args.charter_path.read_bytes()
    try:
        canonical = canonicalize_charter(raw)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    hash_hex = content_hash(canonical)

    if args.dry_run or not args.signature_hex:
        print("=== FID Charter Canonical Bytes ===")
        print(f"path: {args.charter_path}")
        print(f"content_hash_sha3_512: {hash_hex}")
        print()
        print("=== Canonical bytes (sign these with the FID publisher Ed25519 key) ===")
        sys.stdout.buffer.write(canonical)
        print()
        print()
        print("Next step: produce the Ed25519 signature over the canonical bytes above, then re-run:")
        print(
            f"  python -m pipeline.funder_intelligence._methodology.sign_charter \\\n"
            f"      {args.charter_path} \\\n"
            f"      --signer-pubkey-fingerprint <FID-publisher-fingerprint-hex> \\\n"
            f"      --signature-hex <signature-hex>"
        )
        return 0

    if not args.signer_pubkey_fingerprint:
        print("ERROR: --signer-pubkey-fingerprint required when --signature-hex is given.", file=sys.stderr)
        return 1

    # Verify signature against pinned pubkey (unless explicitly skipped for tests)
    if args.allow_missing_pubkey_yaml:
        pubkey = Ed25519PublicKey.from_public_bytes(bytes.fromhex(args.signer_pubkey_fingerprint))
        pinned_fingerprint = args.signer_pubkey_fingerprint
    else:
        try:
            pinned_fingerprint, pubkey = load_pinned_pubkey()
        except (FileNotFoundError, ValueError) as e:
            print(f"ERROR: cannot load pinned FID publisher pubkey: {e}", file=sys.stderr)
            return 2

    if args.signer_pubkey_fingerprint.lower() != pinned_fingerprint.lower():
        print(
            f"ERROR: signer pubkey fingerprint {args.signer_pubkey_fingerprint} "
            f"does not match pinned FID publisher pubkey {pinned_fingerprint}.",
            file=sys.stderr,
        )
        return 2

    if not verify_signature(canonical, args.signature_hex, pubkey):
        print("ERROR: Ed25519 signature does NOT verify against pinned FID publisher pubkey.", file=sys.stderr)
        return 2

    signed_at = args.signed_at or dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    try:
        new_path = write_signed_charter(
            charter_path=args.charter_path,
            canonical_bytes=canonical,
            content_hash_hex=hash_hex,
            signer_pubkey_fingerprint=args.signer_pubkey_fingerprint,
            signature_hex=args.signature_hex,
            signed_at=signed_at,
        )
    except (RuntimeError, FileNotFoundError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    try:
        regenerate_manifest_entry(new_path, hash_hex)
    except (RuntimeError, FileNotFoundError) as e:
        print(f"ERROR: MANIFEST regen failed: {e}", file=sys.stderr)
        # Charter is already signed on disk; surface the failure but don't roll back.
        return 3

    print(f"SIGNED OK: {new_path}")
    print(f"  content_hash_sha3_512: {hash_hex}")
    print(f"  signer_pubkey_fingerprint: {args.signer_pubkey_fingerprint}")
    print(f"  signed_at: {signed_at}")
    print(f"  MANIFEST regenerated: {MANIFEST}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
