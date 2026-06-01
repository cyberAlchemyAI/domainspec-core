"""FID Pillar-3 structured-artifact signing helper.

Mirrors ``sign_corpus.py`` byte-for-byte in canonicalization shape, adapted
for typed funder / program / compliance-cascade YAML artifacts.

Per the FID quality spec at
``docs/FID_ARTIFACT_OPTIMIZATION_PRINCIPLES_2026-05-18.md`` §3.1, every
Pillar-3 artifact carries:

  - artifact_id / artifact_family / artifact_path / schema_version
  - lifecycle_status / classification_default_tier
  - charter_pointer / corpus_dir
  - publisher_pubkey_fingerprint / publisher_pubkey_path
  - runtime_consumer / artifact_must_not_contain / strength_test (§2)
  - ed25519_signature / canonical_bytes_sha3_512

This helper:

  1. Loads the artifact YAML.
  2. Canonicalizes the YAML body (sort_keys=True; UTF-8; allow_unicode=True;
     signature fields → placeholders so canonical bytes are stable
     regardless of when the operator signs).
  3. SHA3-512 hashes the canonical bytes.
  4. Verifies the operator's Ed25519 signature against the pinned FID
     publisher pubkey.
  5. Writes signature back into the YAML's ed25519_signature field +
     canonical_bytes_sha3_512.
  6. Flips lifecycle_status from "draft" to "audited" (next stage per spec).
  7. Regenerates the family-level MANIFEST row.

CC-007 / Law-5 boundary
------------------------
Zero HTTP. Reads/writes on-disk YAML only. Cryptography limited to
``cryptography.hazmat.primitives.asymmetric.ed25519``. No provider calls.

Discipline parity with ``sign_charter.py`` / ``sign_corpus.py``
---------------------------------------------------------------
* Same dual-mode CLI (``--dry-run`` surfaces canonical bytes; signed-mode
  applies the operator's offline-produced signature).
* Same pinned-pubkey verification flow against
  ``vault_shared/funder_intelligence/publisher_pubkey.signed.yaml``.
* Same ``--allow-missing-pubkey-yaml`` testing escape hatch.
* Same exit-code shape:

  | code | meaning                                                                |
  |------|------------------------------------------------------------------------|
  | 0    | success — artifact YAML signature applied + MANIFEST updated          |
  | 1    | bad CLI args / artifact shape invalid / dependent files missing       |
  | 2    | signature failed Ed25519 verify against pinned FID publisher pubkey   |
  | 3    | MANIFEST regen failed (signature is on disk; surface failure)         |
  | 4    | artifact already at lifecycle_status >= "audited" (idempotent guard)  |
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
FID_ROOT = REPO_ROOT / "pipeline" / "funder_intelligence"
PUBKEY_YAML = REPO_ROOT / "vault_shared" / "funder_intelligence" / "publisher_pubkey.signed.yaml"

PLACEHOLDER = "<pending_operator_attestation>"
SIG_FIELDS = ("ed25519_signature", "canonical_bytes_sha3_512", "publisher_pubkey_fingerprint")
LIFECYCLE_DRAFT = "draft"
LIFECYCLE_AUDITED = "audited"

ARTIFACT_FAMILY_TO_DIR = {
    "funder": FID_ROOT / "funders",
    "program": FID_ROOT / "programs",
    "compliance_cascade": FID_ROOT / "compliance_cascades",
    "reviewer_type": FID_ROOT / "reviewer_heuristics",
}


def load_artifact(path: pathlib.Path) -> dict:
    """Load + minimally-validate an artifact YAML."""
    if not path.exists():
        raise FileNotFoundError(f"artifact not at {path}")
    data = yaml.safe_load(path.read_text())
    if not isinstance(data, dict):
        raise ValueError(f"{path}: not a YAML mapping")
    for required in ("artifact_id", "artifact_family"):
        if required not in data:
            raise ValueError(f"{path}: missing required field `{required}`")
    if data["artifact_family"] not in ARTIFACT_FAMILY_TO_DIR:
        raise ValueError(
            f"{path}: artifact_family `{data['artifact_family']}` not in "
            f"{list(ARTIFACT_FAMILY_TO_DIR)}"
        )
    return data


def canonicalize_artifact(data: dict) -> bytes:
    """Strip signature fields to placeholder + emit deterministic YAML bytes."""
    d = dict(data)  # shallow
    for f in SIG_FIELDS:
        d[f] = PLACEHOLDER
    # lifecycle_status excluded from canonicalization-strip — it's
    # signature-relevant (operator signs over the lifecycle at sign time).
    text = yaml.safe_dump(d, sort_keys=True, allow_unicode=True, default_flow_style=False)
    return text.encode("utf-8")


def content_hash(canonical_bytes: bytes) -> str:
    return hashlib.sha3_512(canonical_bytes).hexdigest()


def load_pinned_pubkey() -> Tuple[str, Ed25519PublicKey]:
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


def write_signed_artifact(
    path: pathlib.Path,
    data: dict,
    content_hash_hex: str,
    signer_pubkey_fingerprint: str,
    signature_hex: str,
    signed_at: str,
) -> pathlib.Path:
    """Update lifecycle_status + signature fields in the artifact YAML in place."""
    signed = dict(data)
    signed["publisher_pubkey_fingerprint"] = signer_pubkey_fingerprint
    signed["canonical_bytes_sha3_512"] = content_hash_hex
    signed["ed25519_signature"] = signature_hex
    signed["lifecycle_status"] = LIFECYCLE_AUDITED
    signed["last_signed_at"] = signed_at
    path.write_text(
        yaml.safe_dump(signed, sort_keys=True, allow_unicode=True, default_flow_style=False)
    )
    return path


def regenerate_manifest_entry(
    family: str, artifact_id: str, content_hash_hex: str
) -> pathlib.Path:
    """Update the family-level MANIFEST.md row for this artifact's signature state."""
    family_dir = ARTIFACT_FAMILY_TO_DIR[family]
    manifest = family_dir / "MANIFEST.md"
    if not manifest.exists():
        raise FileNotFoundError(f"Family MANIFEST not at {manifest}")
    sig_prefix = content_hash_hex[:16]
    text = manifest.read_text()
    # Match row shape: `| # | `<id>` | <lifecycle> | `<sig>` |`
    # Lifecycle column is `draft` / `stub` / `pending`; sig column starts
    # with the canonical placeholder string.
    row_pattern = re.compile(
        rf"(\|\s*\d+\s*\|\s*`{re.escape(artifact_id)}`\s*\|)\s*"
        rf"(draft|stub|pending)\s*\|\s*`<pending_operator_attestation>`\s*\|",
    )
    new_text, count = row_pattern.subn(
        rf"\1 audited | `{sig_prefix}…` |",
        text,
    )
    if count == 0:
        raise RuntimeError(f"No MANIFEST row matched for {artifact_id} in {manifest}")
    manifest.write_text(new_text)
    return manifest


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description=(
            "FID Pillar-3 artifact signing helper "
            "(canonicalize YAML + hash + apply operator Ed25519 signature + "
            "flip lifecycle draft→audited + MANIFEST regen)."
        ),
    )
    p.add_argument("artifact_path", type=pathlib.Path,
                   help="Path to the artifact YAML (funders/<id>.yaml or programs/<id>.yaml).")
    p.add_argument("--signer-pubkey-fingerprint",
                   help="Hex fingerprint of the FID publisher pubkey the operator signed with.")
    p.add_argument("--signature-hex",
                   help="Operator-provided Ed25519 signature in hex over the canonical bytes.")
    p.add_argument("--signed-at", default=None,
                   help="UTC ISO-8601 timestamp. Defaults to now() in UTC.")
    p.add_argument("--dry-run", action="store_true",
                   help="Print canonical bytes hash + the bytes themselves; no file changes.")
    p.add_argument("--allow-missing-pubkey-yaml", action="store_true",
                   help="(Testing.) Skip pinned-pubkey verification.")
    args = p.parse_args(argv)

    artifact_path: pathlib.Path = args.artifact_path.resolve()
    try:
        data = load_artifact(artifact_path)
    except (FileNotFoundError, ValueError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    if data.get("lifecycle_status") not in (None, LIFECYCLE_DRAFT, "stub", "pending"):
        if not args.dry_run:
            print(
                f"ERROR: artifact already at lifecycle_status="
                f"`{data.get('lifecycle_status')}`; refusing to re-sign "
                f"(idempotent guard).",
                file=sys.stderr,
            )
            return 4

    canonical = canonicalize_artifact(data)
    hash_hex = content_hash(canonical)

    if args.dry_run or not args.signature_hex:
        print("=== FID Pillar-3 Artifact Canonical Bytes ===")
        print(f"path: {artifact_path}")
        print(f"canonical_bytes_sha3_512: {hash_hex}")
        print()
        print("=== Canonical bytes (sign these with the FID publisher Ed25519 key) ===")
        sys.stdout.buffer.write(canonical)
        print()
        print()
        print("Next step: produce the Ed25519 signature over the canonical bytes, then re-run:")
        print(
            f"  python -m pipeline.funder_intelligence._methodology.sign_artifact \\\n"
            f"      {artifact_path} \\\n"
            f"      --signer-pubkey-fingerprint <fingerprint> \\\n"
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
        print("ERROR: Ed25519 signature does NOT verify against pinned FID publisher pubkey.", file=sys.stderr)
        return 2

    signed_at = args.signed_at or dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    try:
        write_signed_artifact(
            path=artifact_path,
            data=data,
            content_hash_hex=hash_hex,
            signer_pubkey_fingerprint=args.signer_pubkey_fingerprint,
            signature_hex=args.signature_hex,
            signed_at=signed_at,
        )
    except (RuntimeError, FileNotFoundError, OSError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    try:
        regenerate_manifest_entry(data["artifact_family"], data["artifact_id"], hash_hex)
    except (RuntimeError, FileNotFoundError) as e:
        print(f"ERROR: MANIFEST regen failed: {e}", file=sys.stderr)
        return 3

    print(f"SIGNED OK: {artifact_path}")
    print(f"  canonical_bytes_sha3_512: {hash_hex}")
    print(f"  signer_pubkey_fingerprint: {args.signer_pubkey_fingerprint}")
    print(f"  signed_at: {signed_at}")
    print(f"  lifecycle_status: {LIFECYCLE_DRAFT} → {LIFECYCLE_AUDITED}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
