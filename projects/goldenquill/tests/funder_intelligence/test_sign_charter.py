"""Tests for the FID Pillar-1 Depth-Charter signing helper.

Per the P1 audit acceptance criteria at
`pipeline/funder_intelligence/pillar_1_charters/README.md` §"[P1: signing helper]".
"""

from __future__ import annotations

import hashlib
import pathlib
import subprocess
import sys
import textwrap

import pytest

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives import serialization

from pipeline.funder_intelligence._methodology import sign_charter


CHARTER_FIXTURE_HEADER = textwrap.dedent(
    """\
    # Depth Charter — `TEST-FUNDER`

    > **Pillar 1 of 4** per planning doc.
    > **Status: DRAFT v0** — pending operator review + Ed25519 sign-off.

    ---

    ## §1 — What "depth" means for THIS artifact

    Test charter body. Some content that is signature-relevant.

    ---

    ## §7 — Operator signature

    ```yaml
    charter_signed_at: <pending_operator_attestation>
    charter_signed_by_pubkey: <pending_operator_attestation>
    charter_signed_canonical_bytes_sha3_512: <pending_operator_attestation>
    charter_ed25519_signature: <pending_operator_attestation>
    ```

    Some trailing notes.
    """
)


@pytest.fixture
def test_keypair():
    """Generate a fresh Ed25519 keypair for the test."""
    privkey = Ed25519PrivateKey.generate()
    pubkey = privkey.public_key()
    pubkey_hex = pubkey.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    ).hex()
    return privkey, pubkey, pubkey_hex


@pytest.fixture
def charter_file(tmp_path):
    """Write a fixture charter at tmp_path/<id>_charter_v0_DRAFT.md."""
    p = tmp_path / "TEST-FUNDER_charter_v0_DRAFT.md"
    p.write_text(CHARTER_FIXTURE_HEADER)
    return p


@pytest.fixture
def manifest_file(tmp_path, monkeypatch):
    """Stub a MANIFEST.md alongside the charter; patch the helper to point at it."""
    manifest = tmp_path / "MANIFEST.md"
    manifest.write_text(
        textwrap.dedent(
            """\
            # MANIFEST

            | # | Artifact ID | Family | Batch | Charter file | Lifecycle | Sig status |
            |---|-------------|--------|:-----:|--------------|-----------|:----------:|
            | 1 | `TEST-FUNDER` | funder | A | `TEST-FUNDER_charter_v0_DRAFT.md` | DRAFT v0 | `<pending_operator_attestation>` |
            """
        )
    )
    monkeypatch.setattr(sign_charter, "MANIFEST", manifest)
    monkeypatch.setattr(sign_charter, "CHARTERS_DIR", tmp_path)
    return manifest


# ─────────────────────────────────────────────────────────────────
# Canonicalization correctness
# ─────────────────────────────────────────────────────────────────

def test_canonicalize_replaces_signature_block(charter_file):
    raw = charter_file.read_bytes()
    canonical = sign_charter.canonicalize_charter(raw)
    text = canonical.decode("utf-8")
    # Signature field placeholders all present
    assert text.count("<pending_operator_attestation>") == 4
    # Document structure preserved otherwise
    assert "TEST-FUNDER" in text
    assert "§1" in text or "§7" in text


def test_canonicalize_deterministic(charter_file):
    raw = charter_file.read_bytes()
    a = sign_charter.canonicalize_charter(raw)
    b = sign_charter.canonicalize_charter(raw)
    assert a == b
    assert sign_charter.content_hash(a) == sign_charter.content_hash(b)


def test_canonicalize_signature_field_independent(charter_file):
    """Canonicalization should produce the same bytes whether DRAFT placeholders or partly-filled."""
    raw = charter_file.read_bytes()
    canonical_clean = sign_charter.canonicalize_charter(raw)
    # Mutate the charter: stuff a fake signature in
    mutated = raw.replace(
        b"charter_ed25519_signature: <pending_operator_attestation>",
        b"charter_ed25519_signature: deadbeef" * 4,
    ).replace(
        b"charter_signed_at: <pending_operator_attestation>",
        b"charter_signed_at: 2026-05-18T20:00:00Z",
    )
    canonical_mutated = sign_charter.canonicalize_charter(mutated)
    # Canonicalized bytes match: the signature block is normalized away
    assert canonical_clean == canonical_mutated


def test_canonicalize_rejects_missing_block(tmp_path):
    p = tmp_path / "no_sig_block.md"
    p.write_text("# Some charter\n\nNo signature block here.\n")
    with pytest.raises(ValueError, match="no parseable §7 signature block"):
        sign_charter.canonicalize_charter(p.read_bytes())


# ─────────────────────────────────────────────────────────────────
# Sign + verify round-trip
# ─────────────────────────────────────────────────────────────────

def test_sign_verify_round_trip(charter_file, test_keypair):
    privkey, pubkey, pubkey_hex = test_keypair
    raw = charter_file.read_bytes()
    canonical = sign_charter.canonicalize_charter(raw)
    sig = privkey.sign(canonical)
    assert sign_charter.verify_signature(canonical, sig.hex(), pubkey)


def test_sign_verify_fails_on_wrong_key(charter_file, test_keypair):
    privkey, pubkey, _ = test_keypair
    other_priv = Ed25519PrivateKey.generate()
    raw = charter_file.read_bytes()
    canonical = sign_charter.canonicalize_charter(raw)
    sig = other_priv.sign(canonical)
    assert not sign_charter.verify_signature(canonical, sig.hex(), pubkey)


def test_sign_verify_fails_on_mutated_bytes(charter_file, test_keypair):
    privkey, pubkey, _ = test_keypair
    raw = charter_file.read_bytes()
    canonical = sign_charter.canonicalize_charter(raw)
    sig = privkey.sign(canonical)
    # Mutate canonical bytes after signing
    mutated_canonical = canonical.replace(b"TEST-FUNDER", b"OTHER-FUNDER")
    assert not sign_charter.verify_signature(mutated_canonical, sig.hex(), pubkey)


# ─────────────────────────────────────────────────────────────────
# CLI behavior — dry-run + apply
# ─────────────────────────────────────────────────────────────────

def test_cli_dry_run_prints_hash(charter_file, capsys, monkeypatch):
    rc = sign_charter.main([str(charter_file), "--dry-run"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "content_hash_sha3_512:" in out
    assert "Canonical bytes" in out
    # File is unchanged
    assert charter_file.exists()
    assert charter_file.name.endswith("_charter_v0_DRAFT.md")


def test_cli_apply_signature_writes_signed_file(charter_file, manifest_file, test_keypair):
    privkey, pubkey, pubkey_hex = test_keypair
    raw = charter_file.read_bytes()
    canonical = sign_charter.canonicalize_charter(raw)
    sig = privkey.sign(canonical).hex()

    rc = sign_charter.main(
        [
            str(charter_file),
            "--signer-pubkey-fingerprint", pubkey_hex,
            "--signature-hex", sig,
            "--signed-at", "2026-05-18T20:00:00Z",
            "--allow-missing-pubkey-yaml",  # test mode: trust the given fingerprint
        ]
    )
    assert rc == 0

    # v0 DRAFT removed
    assert not charter_file.exists()

    # v1 SIGNED present
    signed_path = charter_file.parent / "TEST-FUNDER_charter_v1_SIGNED.md"
    assert signed_path.exists()
    signed_text = signed_path.read_text()
    assert "charter_signed_at: 2026-05-18T20:00:00Z" in signed_text
    assert f"charter_signed_by_pubkey: {pubkey_hex}" in signed_text
    assert f"charter_ed25519_signature: {sig}" in signed_text
    assert "<pending_operator_attestation>" not in signed_text

    # MANIFEST regenerated
    manifest_text = manifest_file.read_text()
    assert "SIGNED v1" in manifest_text
    assert "DRAFT v0" not in manifest_text


def test_cli_rejects_bad_signature(charter_file, manifest_file, test_keypair):
    privkey, pubkey, pubkey_hex = test_keypair
    raw = charter_file.read_bytes()
    canonical = sign_charter.canonicalize_charter(raw)
    # Sign DIFFERENT bytes (wrong signature)
    sig = privkey.sign(b"wrong bytes").hex()

    rc = sign_charter.main(
        [
            str(charter_file),
            "--signer-pubkey-fingerprint", pubkey_hex,
            "--signature-hex", sig,
            "--allow-missing-pubkey-yaml",
        ]
    )
    assert rc == 2
    # File NOT modified
    assert charter_file.exists()
    assert not (charter_file.parent / "TEST-FUNDER_charter_v1_SIGNED.md").exists()


def test_cli_rejects_pubkey_mismatch(charter_file, manifest_file, tmp_path, test_keypair, monkeypatch):
    privkey, pubkey, pubkey_hex = test_keypair
    raw = charter_file.read_bytes()
    canonical = sign_charter.canonicalize_charter(raw)
    sig = privkey.sign(canonical).hex()

    # Pin a DIFFERENT pubkey
    other_priv = Ed25519PrivateKey.generate()
    other_pub = other_priv.public_key()
    other_hex = other_pub.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    ).hex()
    pinned = tmp_path / "publisher_pubkey.signed.yaml"
    pinned.write_text(f"publisher_pubkey_ed25519_hex: {other_hex}\n")
    monkeypatch.setattr(sign_charter, "PUBKEY_YAML", pinned)

    rc = sign_charter.main(
        [
            str(charter_file),
            "--signer-pubkey-fingerprint", pubkey_hex,  # mismatch with pinned
            "--signature-hex", sig,
        ]
    )
    assert rc == 2
    assert charter_file.exists()  # not modified


def test_cli_idempotent_guard_on_signed_file(charter_file):
    signed_path = charter_file.parent / "TEST-FUNDER_charter_v1_SIGNED.md"
    signed_path.write_text("already signed")
    rc = sign_charter.main([str(signed_path), "--dry-run"])
    assert rc == 4


def test_cli_missing_charter_returns_1(tmp_path):
    rc = sign_charter.main([str(tmp_path / "does_not_exist.md"), "--dry-run"])
    assert rc == 1


def test_cli_apply_requires_pubkey_fingerprint(charter_file):
    """--signature-hex without --signer-pubkey-fingerprint should error."""
    rc = sign_charter.main(
        [
            str(charter_file),
            "--signature-hex", "deadbeef" * 16,
        ]
    )
    assert rc == 1
