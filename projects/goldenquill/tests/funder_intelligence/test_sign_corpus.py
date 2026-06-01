"""Tests for the FID Pillar-2 corpus signing helper.

Mirrors the shape of `tests/funder_intelligence/test_sign_charter.py`.
"""

from __future__ import annotations

import hashlib
import pathlib
import textwrap

import pytest
import yaml

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey
from cryptography.hazmat.primitives import serialization

from pipeline.funder_intelligence._methodology import sign_corpus


# ─────────────────────────────────────────────────────────────────
# Fixtures
# ─────────────────────────────────────────────────────────────────

@pytest.fixture
def test_keypair():
    priv = Ed25519PrivateKey.generate()
    pub = priv.public_key()
    pub_hex = pub.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    ).hex()
    return priv, pub, pub_hex


@pytest.fixture
def corpus_root(tmp_path):
    """Scaffold a minimal pillar_2_corpus/<id>/ tree."""
    artifact_id = "TEST-ARTIFACT"
    root = tmp_path / "pillar_2_corpus" / artifact_id
    (root / "raw").mkdir(parents=True)
    (root / "extracted").mkdir(parents=True)

    # Add a fake source file
    src = root / "raw" / "nofo.pdf"
    src.write_bytes(b"%PDF fake bytes")
    src_sha = hashlib.sha256(b"%PDF fake bytes").hexdigest()

    # Write sources.yaml
    (root / "sources.yaml").write_text(yaml.safe_dump({
        "artifact_id": artifact_id,
        "charter_path": "charter.signed.yaml",
        "populated_at": "2026-05-18T20:00:00Z",
        "files": [{
            "file_path": "raw/nofo.pdf",
            "source_url": "https://example.gov/nofo.pdf",
            "access_date": "2026-05-18",
            "content_type": "application/pdf",
            "sha256": src_sha,
            "bytes_size": len(b"%PDF fake bytes"),
            "classification_tier": 1,
            "classification_rationale": "Public NOFO",
            "status": "registered",
        }],
    }))

    # Write one extracted cluster
    (root / "extracted" / "gates.yaml").write_text(yaml.safe_dump({
        "cluster_name": "gates",
        "facts": [{
            "fact_id": "F1",
            "corpus_ref": "TEST-ARTIFACT:raw/nofo.pdf:p1",
            "verbatim_quote": "One sentence.",
            "analysis": "Test.",
        }],
    }))
    return root


@pytest.fixture
def manifest_file(tmp_path, monkeypatch):
    """Stub MANIFEST.md alongside corpus tree; patch helper to use it."""
    manifest = tmp_path / "pillar_2_corpus" / "MANIFEST.md"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(textwrap.dedent("""\
        # Pillar-2 Corpus — MANIFEST

        | # | Artifact ID | Family | Batch | Pillar-1 charter file | Pillar-2 status | Sig prefix |
        |---|-------------|--------|:-----:|------------------------|-----------------|------------|
        | 1 | `TEST-ARTIFACT` | funder | A | `pillar_1_charters/TEST-ARTIFACT_charter_v0_DRAFT.md` | EXTRACTING | `<pending_operator_attestation>` |
    """))
    monkeypatch.setattr(sign_corpus, "MANIFEST", manifest)
    return manifest


# ─────────────────────────────────────────────────────────────────
# Canonicalization correctness
# ─────────────────────────────────────────────────────────────────

class TestCanonicalize:
    def test_build_manifest_includes_sources_and_extracted(self, corpus_root):
        m = sign_corpus.build_canonical_manifest(corpus_root)
        assert m["artifact_id"] == "TEST-ARTIFACT"
        assert m["sources_summary"]["total_files"] == 1
        assert m["sources_summary"]["tier_counts"][1] == 1
        assert m["extracted_summary"]["cluster_count"] == 1
        assert m["extracted_summary"]["clusters"][0]["cluster_name"] == "gates"
        # Signature fields placeholdered
        assert m["signed_at"] == sign_corpus.PLACEHOLDER
        assert m["corpus_ed25519_signature"] == sign_corpus.PLACEHOLDER

    def test_canonicalize_deterministic(self, corpus_root):
        m1 = sign_corpus.build_canonical_manifest(corpus_root)
        m2 = sign_corpus.build_canonical_manifest(corpus_root)
        b1 = sign_corpus.canonicalize_manifest(m1)
        b2 = sign_corpus.canonicalize_manifest(m2)
        assert b1 == b2
        assert sign_corpus.content_hash(b1) == sign_corpus.content_hash(b2)

    def test_canonicalize_signature_field_independent(self, corpus_root):
        m_clean = sign_corpus.build_canonical_manifest(corpus_root)
        b_clean = sign_corpus.canonicalize_manifest(m_clean)
        # Mutate the dict's signature fields; canonical bytes must match
        m_mut = dict(m_clean)
        m_mut["signed_at"] = "2026-05-18T20:00:00Z"
        m_mut["corpus_ed25519_signature"] = "deadbeef" * 8
        b_mut = sign_corpus.canonicalize_manifest(m_mut)
        assert b_clean == b_mut

    def test_build_manifest_rejects_missing_root(self, tmp_path):
        with pytest.raises(FileNotFoundError):
            sign_corpus.build_canonical_manifest(tmp_path / "nope")

    def test_build_manifest_rejects_missing_sources_yaml(self, tmp_path):
        d = tmp_path / "art"
        d.mkdir()
        with pytest.raises(FileNotFoundError):
            sign_corpus.build_canonical_manifest(d)


# ─────────────────────────────────────────────────────────────────
# Sign + verify round-trip
# ─────────────────────────────────────────────────────────────────

class TestSignVerify:
    def test_sign_verify_round_trip(self, corpus_root, test_keypair):
        priv, pub, _ = test_keypair
        m = sign_corpus.build_canonical_manifest(corpus_root)
        canon = sign_corpus.canonicalize_manifest(m)
        sig = priv.sign(canon)
        assert sign_corpus.verify_signature(canon, sig.hex(), pub)

    def test_sign_verify_fails_on_wrong_key(self, corpus_root, test_keypair):
        _, pub, _ = test_keypair
        other_priv = Ed25519PrivateKey.generate()
        m = sign_corpus.build_canonical_manifest(corpus_root)
        canon = sign_corpus.canonicalize_manifest(m)
        sig = other_priv.sign(canon)
        assert not sign_corpus.verify_signature(canon, sig.hex(), pub)

    def test_sign_verify_fails_on_mutated_bytes(self, corpus_root, test_keypair):
        priv, pub, _ = test_keypair
        m = sign_corpus.build_canonical_manifest(corpus_root)
        canon = sign_corpus.canonicalize_manifest(m)
        sig = priv.sign(canon)
        mutated = canon.replace(b"TEST-ARTIFACT", b"OTHER-ARTIFACT")
        assert not sign_corpus.verify_signature(mutated, sig.hex(), pub)


# ─────────────────────────────────────────────────────────────────
# CLI dry-run + apply
# ─────────────────────────────────────────────────────────────────

class TestCLI:
    def test_dry_run_prints_hash(self, corpus_root, capsys):
        rc = sign_corpus.main([str(corpus_root), "--dry-run"])
        out = capsys.readouterr().out
        assert rc == 0
        assert "corpus_canonical_bytes_sha3_512:" in out
        assert "Canonical bytes" in out
        assert not (corpus_root / "_signed.yaml").exists()

    def test_apply_signature_writes_signed_yaml(self, corpus_root, manifest_file, test_keypair):
        priv, pub, pub_hex = test_keypair
        m = sign_corpus.build_canonical_manifest(corpus_root)
        canon = sign_corpus.canonicalize_manifest(m)
        sig = priv.sign(canon).hex()

        rc = sign_corpus.main([
            str(corpus_root),
            "--signer-pubkey-fingerprint", pub_hex,
            "--signature-hex", sig,
            "--signed-at", "2026-05-18T20:00:00Z",
            "--allow-missing-pubkey-yaml",
        ])
        assert rc == 0
        signed = corpus_root / "_signed.yaml"
        assert signed.exists()
        data = yaml.safe_load(signed.read_text())
        assert data["signed_by_pubkey"] == pub_hex
        assert data["corpus_ed25519_signature"] == sig
        assert data["signed_at"] == "2026-05-18T20:00:00Z"
        assert data["corpus_canonical_bytes_sha3_512"] == sign_corpus.content_hash(canon)
        # MANIFEST updated
        manifest_text = manifest_file.read_text()
        assert "SIGNED" in manifest_text
        assert "<pending_operator_attestation>" not in manifest_text

    def test_apply_rejects_bad_signature(self, corpus_root, manifest_file, test_keypair, capsys):
        priv, pub, pub_hex = test_keypair
        wrong = priv.sign(b"wrong bytes").hex()
        rc = sign_corpus.main([
            str(corpus_root),
            "--signer-pubkey-fingerprint", pub_hex,
            "--signature-hex", wrong,
            "--allow-missing-pubkey-yaml",
        ])
        assert rc == 2
        assert not (corpus_root / "_signed.yaml").exists()

    def test_apply_rejects_pubkey_mismatch(self, corpus_root, manifest_file, test_keypair, tmp_path, monkeypatch, capsys):
        priv, pub, pub_hex = test_keypair
        m = sign_corpus.build_canonical_manifest(corpus_root)
        canon = sign_corpus.canonicalize_manifest(m)
        sig = priv.sign(canon).hex()
        # Pin a DIFFERENT pubkey
        other_priv = Ed25519PrivateKey.generate()
        other_hex = other_priv.public_key().public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        ).hex()
        pinned = tmp_path / "publisher_pubkey.signed.yaml"
        pinned.write_text(f"publisher_pubkey_ed25519_hex: {other_hex}\n")
        monkeypatch.setattr(sign_corpus, "PUBKEY_YAML", pinned)

        rc = sign_corpus.main([
            str(corpus_root),
            "--signer-pubkey-fingerprint", pub_hex,
            "--signature-hex", sig,
        ])
        assert rc == 2
        assert not (corpus_root / "_signed.yaml").exists()

    def test_idempotent_guard_on_signed_corpus(self, corpus_root):
        (corpus_root / "_signed.yaml").write_text("already: signed\n")
        rc = sign_corpus.main([str(corpus_root), "--dry-run"])
        assert rc == 4

    def test_missing_corpus_root_returns_1(self, tmp_path):
        rc = sign_corpus.main([str(tmp_path / "ghost"), "--dry-run"])
        assert rc == 1

    def test_apply_requires_pubkey_fingerprint(self, corpus_root):
        rc = sign_corpus.main([
            str(corpus_root),
            "--signature-hex", "deadbeef" * 16,
        ])
        assert rc == 1


# ─────────────────────────────────────────────────────────────────
# MANIFEST regen
# ─────────────────────────────────────────────────────────────────

class TestManifestRegen:
    def test_regen_replaces_pending_row(self, corpus_root, manifest_file):
        sign_corpus.regenerate_manifest_entry(corpus_root, "a" * 128)
        text = manifest_file.read_text()
        assert "SIGNED" in text
        assert "<pending_operator_attestation>" not in text
        assert "aaaaaaaaaaaaaaaa" in text  # first 16 of hash

    def test_regen_fails_when_no_matching_row(self, corpus_root, manifest_file):
        manifest_file.write_text("# Empty manifest\n")
        with pytest.raises(RuntimeError, match="No Pillar-2 MANIFEST row matched"):
            sign_corpus.regenerate_manifest_entry(corpus_root, "a" * 128)
