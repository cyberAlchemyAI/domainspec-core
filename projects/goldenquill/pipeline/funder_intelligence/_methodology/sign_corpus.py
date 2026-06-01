"""FID Pillar-2 corpus signing helper.

Mirrors ``sign_charter.py`` byte-for-byte in canonicalization shape:

  1. Build a deterministic corpus manifest YAML from ``sources.yaml`` + the
     extracted-cluster files under ``extracted/``. Sort keys; UTF-8;
     ensure_ascii=False; signature fields placeholdered.
  2. SHA3-512 the canonical bytes → ``corpus_canonical_bytes_sha3_512``.
  3. Operator's Ed25519 signature targets the canonical bytes (the hex
     signature passed in via ``--signature-hex`` must verify against the FID
     publisher pubkey when applied to these bytes).
  4. Write ``_signed.yaml`` at the corpus root with the operator signature
     fields filled in.
  5. Update the top-level Pillar-2 MANIFEST row to ``SIGNED`` with the hash
     prefix.

Discipline parity with ``sign_charter.py``
------------------------------------------
* Same dual-mode CLI: ``--dry-run`` prints canonical bytes + hash; the
  signed-mode invocation (``--signature-hex`` + ``--signer-pubkey-fingerprint``)
  applies the operator's offline-produced signature.
* Same pinned-pubkey verification flow against
  ``vault_shared/funder_intelligence/publisher_pubkey.signed.yaml``.
* Same ``--allow-missing-pubkey-yaml`` testing-only escape hatch.
* Same exit-code shape:

  | code | meaning                                                                |
  |------|------------------------------------------------------------------------|
  | 0    | success — _signed.yaml written + MANIFEST updated                      |
  | 1    | bad CLI args / corpus shape invalid / dependent files missing          |
  | 2    | signature failed Ed25519 verify against pinned FID publisher pubkey    |
  | 3    | MANIFEST regen failed (signature is on disk; surface failure)          |
  | 4    | corpus already at _signed.yaml state (idempotent guard)                |

CC-007 / Law-5 boundary
------------------------
This helper performs zero HTTP. It reads on-disk files only. The cryptography
work uses ``cryptography.hazmat.primitives.asymmetric.ed25519`` (the same
import shape as ``sign_charter.py``) — no provider calls.

Output shape (``_signed.yaml``)
-------------------------------
.. code-block:: yaml

    artifact_id: USDA-RD-RBDG-FY26
    corpus_root: pipeline/funder_intelligence/pillar_2_corpus/USDA-RD-RBDG-FY26/
    signed_at: 2026-05-XXTXX:XX:XXZ
    signed_by_pubkey: <hex>
    corpus_canonical_bytes_sha3_512: <128-hex>
    corpus_ed25519_signature: <hex>
    sources_summary:
      total_files: <int>
      tier_counts: {1: <int>, 2: <int>, 3: <int>}
      file_hashes:
        - file_path: raw/nofos/...
          sha256: <64-hex>
    extracted_summary:
      cluster_count: <int>
      clusters: [<list of cluster filenames>]
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
P2_ROOT = REPO_ROOT / "pipeline" / "funder_intelligence" / "pillar_2_corpus"
MANIFEST = P2_ROOT / "MANIFEST.md"
PUBKEY_YAML = REPO_ROOT / "vault_shared" / "funder_intelligence" / "publisher_pubkey.signed.yaml"

PLACEHOLDER = "<pending_operator_attestation>"


def _walk_extracted_clusters(corpus_root: pathlib.Path) -> list[pathlib.Path]:
    ex_dir = corpus_root / "extracted"
    if not ex_dir.exists():
        return []
    return sorted(p for p in ex_dir.glob("*.yaml") if p.is_file())


def build_canonical_manifest(corpus_root: pathlib.Path) -> dict:
    """Produce the deterministic corpus manifest dict (pre-canonicalization)."""
    if not corpus_root.exists() or not corpus_root.is_dir():
        raise FileNotFoundError(f"corpus_root does not exist: {corpus_root}")

    sources_path = corpus_root / "sources.yaml"
    if not sources_path.exists():
        raise FileNotFoundError(f"sources.yaml not at {sources_path}")
    sources = yaml.safe_load(sources_path.read_text()) or {}
    if not isinstance(sources, dict):
        raise ValueError(f"sources.yaml at {sources_path} is not a YAML mapping")

    artifact_id = sources.get("artifact_id") or corpus_root.name
    files = sources.get("files") or []

    # File-hashes summary — sort by file_path for determinism.
    file_summaries = sorted(
        (
            {
                "file_path": str(f.get("file_path", "")),
                "sha256": str(f.get("sha256", "")),
                "classification_tier": int(f.get("classification_tier", 0) or 0),
                "source_url": str(f.get("source_url", "")),
                "content_type": str(f.get("content_type", "")),
            }
            for f in files
        ),
        key=lambda x: x["file_path"],
    )
    tier_counts = {1: 0, 2: 0, 3: 0}
    for s in file_summaries:
        t = s["classification_tier"]
        if t in tier_counts:
            tier_counts[t] += 1

    # Extracted-cluster hashes (over the cluster file bytes).
    clusters = _walk_extracted_clusters(corpus_root)
    cluster_summaries = sorted(
        (
            {
                "cluster_name": p.stem,
                "file_path": f"extracted/{p.name}",
                "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
            }
            for p in clusters
        ),
        key=lambda x: x["cluster_name"],
    )

    manifest = {
        "artifact_id": artifact_id,
        "corpus_root": f"pipeline/funder_intelligence/pillar_2_corpus/{corpus_root.name}/",
        "signed_at": PLACEHOLDER,
        "signed_by_pubkey": PLACEHOLDER,
        "corpus_canonical_bytes_sha3_512": PLACEHOLDER,
        "corpus_ed25519_signature": PLACEHOLDER,
        "sources_summary": {
            "total_files": len(file_summaries),
            "tier_counts": tier_counts,
            "file_hashes": file_summaries,
        },
        "extracted_summary": {
            "cluster_count": len(cluster_summaries),
            "clusters": cluster_summaries,
        },
    }
    return manifest


def canonicalize_manifest(manifest: dict) -> bytes:
    """Deterministic YAML bytes for hash + signature.

    Strips the four signature fields to placeholder values regardless of
    what's in ``manifest`` so the canonical bytes are stable.
    """
    m = dict(manifest)  # shallow copy
    m["signed_at"] = PLACEHOLDER
    m["signed_by_pubkey"] = PLACEHOLDER
    m["corpus_canonical_bytes_sha3_512"] = PLACEHOLDER
    m["corpus_ed25519_signature"] = PLACEHOLDER
    # sort_keys=True for determinism; allow_unicode=True to match Cards/WPFA.
    text = yaml.safe_dump(m, sort_keys=True, allow_unicode=True, default_flow_style=False)
    return text.encode("utf-8")


def content_hash(canonical_bytes: bytes) -> str:
    return hashlib.sha3_512(canonical_bytes).hexdigest()


def load_pinned_pubkey() -> Tuple[str, Ed25519PublicKey]:
    """Load + parse the pinned FID publisher pubkey.

    Returns (fingerprint_hex, parsed_pubkey).
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


def write_signed_corpus(
    corpus_root: pathlib.Path,
    manifest: dict,
    content_hash_hex: str,
    signer_pubkey_fingerprint: str,
    signature_hex: str,
    signed_at: str,
) -> pathlib.Path:
    """Write ``_signed.yaml`` at corpus root; return the path."""
    signed = dict(manifest)
    signed["signed_at"] = signed_at
    signed["signed_by_pubkey"] = signer_pubkey_fingerprint
    signed["corpus_canonical_bytes_sha3_512"] = content_hash_hex
    signed["corpus_ed25519_signature"] = signature_hex

    out_path = corpus_root / "_signed.yaml"
    if out_path.exists():
        raise RuntimeError(f"Refusing to overwrite existing signed corpus at {out_path}")
    out_path.write_text(
        yaml.safe_dump(signed, sort_keys=True, allow_unicode=True, default_flow_style=False)
    )
    return out_path


def regenerate_manifest_entry(corpus_root: pathlib.Path, content_hash_hex: str) -> None:
    """Update the top-level Pillar-2 MANIFEST.md row for this artifact."""
    if not MANIFEST.exists():
        raise FileNotFoundError(f"Pillar-2 MANIFEST not at {MANIFEST}")
    artifact_id = corpus_root.name
    sig_prefix = content_hash_hex[:16]

    manifest_text = MANIFEST.read_text()
    # Match the artifact's row by ID; replace the status column + sig column
    # at the row's tail. Status column is bracketed by `|`; sig column is the
    # last column before the trailing `|`.
    row_pattern = re.compile(
        rf"(\|\s*\d+\s*\|\s*`{re.escape(artifact_id)}`\s*\|[^\n]*?\|)\s*"
        rf"(NOT_INITIALIZED|FETCHING|EXTRACTING|READY_FOR_SIGN)"
        rf"\s*\|\s*`<pending_operator_attestation>`\s*\|",
    )
    new_text, count = row_pattern.subn(
        rf"\1 SIGNED | `{sig_prefix}…` |",
        manifest_text,
    )
    if count == 0:
        raise RuntimeError(f"No Pillar-2 MANIFEST row matched for {artifact_id}")
    MANIFEST.write_text(new_text)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description=(
            "FID Pillar-2 corpus signing helper (canonicalize manifest + hash + "
            "apply operator Ed25519 signature + write _signed.yaml + MANIFEST regen)."
        ),
    )
    p.add_argument("corpus_root", type=pathlib.Path,
                   help="Path to the pillar_2_corpus/<artifact_id>/ directory.")
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

    corpus_root: pathlib.Path = args.corpus_root.resolve()

    if not corpus_root.exists():
        print(f"ERROR: corpus_root not found at {corpus_root}", file=sys.stderr)
        return 1
    if (corpus_root / "_signed.yaml").exists():
        print(
            f"ERROR: corpus already signed (idempotent guard): {corpus_root / '_signed.yaml'}",
            file=sys.stderr,
        )
        return 4

    try:
        manifest = build_canonical_manifest(corpus_root)
    except (FileNotFoundError, ValueError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    canonical = canonicalize_manifest(manifest)
    hash_hex = content_hash(canonical)

    if args.dry_run or not args.signature_hex:
        print("=== FID Pillar-2 Corpus Canonical Bytes ===")
        print(f"corpus_root: {corpus_root}")
        print(f"corpus_canonical_bytes_sha3_512: {hash_hex}")
        print()
        print("=== Canonical bytes (sign these with the FID publisher Ed25519 key) ===")
        sys.stdout.buffer.write(canonical)
        print()
        print()
        print("Next step: produce the Ed25519 signature over the canonical bytes above, then re-run:")
        print(
            f"  python -m pipeline.funder_intelligence._methodology.sign_corpus \\\n"
            f"      {corpus_root} \\\n"
            f"      --signer-pubkey-fingerprint <FID-publisher-fingerprint-hex> \\\n"
            f"      --signature-hex <signature-hex>"
        )
        return 0

    if not args.signer_pubkey_fingerprint:
        print("ERROR: --signer-pubkey-fingerprint required when --signature-hex is given.", file=sys.stderr)
        return 1

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
        print(
            "ERROR: Ed25519 signature does NOT verify against pinned FID publisher pubkey.",
            file=sys.stderr,
        )
        return 2

    signed_at = args.signed_at or dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    try:
        out_path = write_signed_corpus(
            corpus_root=corpus_root,
            manifest=manifest,
            content_hash_hex=hash_hex,
            signer_pubkey_fingerprint=args.signer_pubkey_fingerprint,
            signature_hex=args.signature_hex,
            signed_at=signed_at,
        )
    except (RuntimeError, FileNotFoundError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    try:
        regenerate_manifest_entry(corpus_root, hash_hex)
    except (RuntimeError, FileNotFoundError) as e:
        print(f"ERROR: MANIFEST regen failed: {e}", file=sys.stderr)
        return 3

    print(f"SIGNED OK: {out_path}")
    print(f"  corpus_canonical_bytes_sha3_512: {hash_hex}")
    print(f"  signer_pubkey_fingerprint: {args.signer_pubkey_fingerprint}")
    print(f"  signed_at: {signed_at}")
    print(f"  MANIFEST regenerated: {MANIFEST}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
