"""Tests for the FID Pillar-3 artifact signing helper."""

from __future__ import annotations

import pathlib
import textwrap

import pytest
import yaml

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization

from pipeline.funder_intelligence._methodology import sign_artifact


@pytest.fixture
def keypair():
    priv = Ed25519PrivateKey.generate()
    pub_hex = priv.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    ).hex()
    return priv, pub_hex


@pytest.fixture
def fid_tree(tmp_path, monkeypatch):
    fid_root = tmp_path / "pipeline" / "funder_intelligence"
    funders_dir = fid_root / "funders"
    programs_dir = fid_root / "programs"
    compliance_dir = fid_root / "compliance_cascades"
    reviewers_dir = fid_root / "reviewer_heuristics"
    for d in (funders_dir, programs_dir, compliance_dir, reviewers_dir):
        d.mkdir(parents=True)

    monkeypatch.setattr(sign_artifact, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(sign_artifact, "FID_ROOT", fid_root)
    monkeypatch.setattr(sign_artifact, "ARTIFACT_FAMILY_TO_DIR", {
        "funder": funders_dir,
        "program": programs_dir,
        "compliance_cascade": compliance_dir,
        "reviewer_type": reviewers_dir,
    })
    return {"tmp_path": tmp_path, "fid_root": fid_root,
            "funders_dir": funders_dir, "programs_dir": programs_dir}


def _make_funder_stub(funders_dir: pathlib.Path, aid: str) -> pathlib.Path:
    data = {
        "artifact_id": aid,
        "artifact_family": "funder",
        "lifecycle_status": "draft",
        "publisher_pubkey_fingerprint": "<pending_operator_attestation>",
        "ed25519_signature": "<pending_operator_attestation>",
        "canonical_bytes_sha3_512": "<pending_operator_attestation>",
        "mission_framing": {"one_paragraph_summary": "body"},
    }
    p = funders_dir / f"{aid}.yaml"
    p.write_text(yaml.safe_dump(data, sort_keys=True))
    return p


def _make_manifest(funders_dir: pathlib.Path, aid: str) -> pathlib.Path:
    m = funders_dir / "MANIFEST.md"
    m.write_text(
        "# Funders MANIFEST\n\n"
        "| # | Artifact ID | Lifecycle | Sig prefix |\n"
        "|---|-------------|-----------|------------|\n"
        f"| 1 | `{aid}` | draft | `<pending_operator_attestation>` |\n"
    )
    return m


class TestCanonicalize:
    def test_canonical_strips_signature_fields(self, fid_tree):
        artifact = _make_funder_stub(fid_tree["funders_dir"], "USDA-RD")
        data = sign_artifact.load_artifact(artifact)
        canon = sign_artifact.canonicalize_artifact(data)
        text = canon.decode("utf-8")
        # All three signature fields should canonicalize to placeholder
        assert "ed25519_signature: <pending_operator_attestation>" in text
        assert "canonical_bytes_sha3_512: <pending_operator_attestation>" in text
        assert "publisher_pubkey_fingerprint: <pending_operator_attestation>" in text

    def test_canonical_is_deterministic(self, fid_tree):
        artifact = _make_funder_stub(fid_tree["funders_dir"], "USDA-RD")
        data1 = sign_artifact.load_artifact(artifact)
        data2 = sign_artifact.load_artifact(artifact)
        canon1 = sign_artifact.canonicalize_artifact(data1)
        canon2 = sign_artifact.canonicalize_artifact(data2)
        assert canon1 == canon2

    def test_content_hash_is_sha3_512(self, fid_tree):
        artifact = _make_funder_stub(fid_tree["funders_dir"], "USDA-RD")
        data = sign_artifact.load_artifact(artifact)
        canon = sign_artifact.canonicalize_artifact(data)
        h = sign_artifact.content_hash(canon)
        assert len(h) == 128  # SHA3-512 hex = 128 chars


class TestLoad:
    def test_load_missing_artifact_raises(self, fid_tree):
        with pytest.raises(FileNotFoundError):
            sign_artifact.load_artifact(fid_tree["funders_dir"] / "ghost.yaml")

    def test_load_unknown_family_raises(self, fid_tree):
        bad = fid_tree["funders_dir"] / "weird.yaml"
        bad.write_text(yaml.safe_dump({
            "artifact_id": "weird",
            "artifact_family": "alien",
        }))
        with pytest.raises(ValueError, match="not in"):
            sign_artifact.load_artifact(bad)

    def test_load_missing_required_field_raises(self, fid_tree):
        bad = fid_tree["funders_dir"] / "incomplete.yaml"
        bad.write_text(yaml.safe_dump({"artifact_id": "x"}))
        with pytest.raises(ValueError, match="missing required field"):
            sign_artifact.load_artifact(bad)


class TestSignFlow:
    def test_dry_run_emits_canonical_bytes(self, fid_tree, capsys):
        artifact = _make_funder_stub(fid_tree["funders_dir"], "USDA-RD")
        rc = sign_artifact.main([str(artifact), "--dry-run"])
        assert rc == 0
        out = capsys.readouterr().out
        assert "canonical_bytes_sha3_512" in out

    def test_apply_signs_artifact(self, fid_tree, keypair):
        priv, pub_hex = keypair
        artifact = _make_funder_stub(fid_tree["funders_dir"], "USDA-RD")
        _make_manifest(fid_tree["funders_dir"], "USDA-RD")

        # Compute canonical bytes + sign
        data = sign_artifact.load_artifact(artifact)
        canon = sign_artifact.canonicalize_artifact(data)
        sig_hex = priv.sign(canon).hex()

        rc = sign_artifact.main([
            str(artifact),
            "--signer-pubkey-fingerprint", pub_hex,
            "--signature-hex", sig_hex,
            "--allow-missing-pubkey-yaml",
        ])
        assert rc == 0
        signed_data = yaml.safe_load(artifact.read_text())
        assert signed_data["lifecycle_status"] == "audited"
        assert signed_data["ed25519_signature"] == sig_hex
        assert signed_data["publisher_pubkey_fingerprint"] == pub_hex
        assert len(signed_data["canonical_bytes_sha3_512"]) == 128

        # MANIFEST row updated
        manifest = (fid_tree["funders_dir"] / "MANIFEST.md").read_text()
        assert "audited" in manifest

    def test_apply_bad_signature_returns_2(self, fid_tree, keypair):
        _priv, pub_hex = keypair
        artifact = _make_funder_stub(fid_tree["funders_dir"], "USDA-RD")
        _make_manifest(fid_tree["funders_dir"], "USDA-RD")
        rc = sign_artifact.main([
            str(artifact),
            "--signer-pubkey-fingerprint", pub_hex,
            "--signature-hex", "aa" * 64,
            "--allow-missing-pubkey-yaml",
        ])
        assert rc == 2

    def test_idempotent_guard_already_audited(self, fid_tree, keypair, capsys):
        priv, pub_hex = keypair
        artifact = _make_funder_stub(fid_tree["funders_dir"], "USDA-RD")
        _make_manifest(fid_tree["funders_dir"], "USDA-RD")
        data = sign_artifact.load_artifact(artifact)
        canon = sign_artifact.canonicalize_artifact(data)
        sig_hex = priv.sign(canon).hex()
        # First sign — ok
        rc1 = sign_artifact.main([
            str(artifact),
            "--signer-pubkey-fingerprint", pub_hex,
            "--signature-hex", sig_hex,
            "--allow-missing-pubkey-yaml",
        ])
        assert rc1 == 0
        # Second sign — refused
        rc2 = sign_artifact.main([
            str(artifact),
            "--signer-pubkey-fingerprint", pub_hex,
            "--signature-hex", sig_hex,
            "--allow-missing-pubkey-yaml",
        ])
        assert rc2 == 4
        assert "idempotent guard" in capsys.readouterr().err

    def test_manifest_regen_fails_when_no_row_matches(self, fid_tree, keypair):
        priv, pub_hex = keypair
        artifact = _make_funder_stub(fid_tree["funders_dir"], "NO-MANIFEST-ROW")
        # Manifest exists but doesn't have NO-MANIFEST-ROW row
        m = fid_tree["funders_dir"] / "MANIFEST.md"
        m.write_text(
            "# Funders MANIFEST\n\n"
            "| # | Artifact ID | Lifecycle | Sig prefix |\n"
            "|---|-------------|-----------|------------|\n"
            "| 1 | `OTHER` | draft | `<pending_operator_attestation>` |\n"
        )
        data = sign_artifact.load_artifact(artifact)
        canon = sign_artifact.canonicalize_artifact(data)
        sig_hex = priv.sign(canon).hex()
        rc = sign_artifact.main([
            str(artifact),
            "--signer-pubkey-fingerprint", pub_hex,
            "--signature-hex", sig_hex,
            "--allow-missing-pubkey-yaml",
        ])
        # Artifact is signed on disk, but MANIFEST regen fails → exit 3
        assert rc == 3


class TestVerify:
    def test_verify_signature_valid(self, fid_tree, keypair):
        priv, _ = keypair
        artifact = _make_funder_stub(fid_tree["funders_dir"], "USDA-RD")
        data = sign_artifact.load_artifact(artifact)
        canon = sign_artifact.canonicalize_artifact(data)
        sig_hex = priv.sign(canon).hex()
        assert sign_artifact.verify_signature(canon, sig_hex, priv.public_key())

    def test_verify_signature_invalid(self, fid_tree, keypair):
        priv, _ = keypair
        artifact = _make_funder_stub(fid_tree["funders_dir"], "USDA-RD")
        data = sign_artifact.load_artifact(artifact)
        canon = sign_artifact.canonicalize_artifact(data)
        bad = "aa" * 64
        assert not sign_artifact.verify_signature(canon, bad, priv.public_key())
