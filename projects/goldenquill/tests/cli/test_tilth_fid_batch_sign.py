"""tilth fid batch-sign CLI tests."""

from __future__ import annotations

import pathlib
import textwrap

import pytest
import yaml

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization

# This test module depends on the sign_charter helper at
# pipeline/funder_intelligence/_methodology/sign_charter.py, which lands
# via PR #33. Until PR #33 merges, sign_charter is not importable on CI
# and the apply-flow tests would error at fixture setup. Skip the module
# cleanly with a clear reason rather than failing CI.
pytest.importorskip(
    "pipeline.funder_intelligence._methodology.sign_charter",
    reason=(
        "sign_charter helper is not on main yet (lands via PR #33 — "
        "fid-week-1-pillar-1-charters-2026-05-18). batch-sign tests run "
        "after PR #33 merges."
    ),
)

from pipeline.cli import tilth_fid_batch_sign as bs  # noqa: E402


CHARTER_FIXTURE_HEADER = textwrap.dedent(
    """\
    # Depth Charter — `{aid}`

    > **Pillar 1 of 4** per planning doc.
    > **Status: DRAFT v0** — pending operator review + Ed25519 sign-off.

    ---

    ## §1 — What "depth" means

    Body content for {aid}.

    ---

    ## §7 — Operator signature

    ```yaml
    charter_signed_at: <pending_operator_attestation>
    charter_signed_by_pubkey: <pending_operator_attestation>
    charter_signed_canonical_bytes_sha3_512: <pending_operator_attestation>
    charter_ed25519_signature: <pending_operator_attestation>
    ```
    """
)


MANIFEST_FIXTURE_TEMPLATE = textwrap.dedent(
    """\
    # MANIFEST

    | # | Artifact ID | Lifecycle | Sig status |
    |---|-------------|-----------|------------|
    {rows}
    """
)


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
    """Build a temporary FID tree, patch bs + sign_charter paths."""
    fid_root = tmp_path / "pipeline" / "funder_intelligence"
    charters_dir = fid_root / "pillar_1_charters"
    charters_dir.mkdir(parents=True)
    manifest = charters_dir / "MANIFEST.md"

    rows = "\n".join(
        f"| {i+1} | `{aid}` | DRAFT v0 | `<pending_operator_attestation>` |"
        for i, aid in enumerate(bs.PHASE_1_ROSTER)
    )
    manifest.write_text(MANIFEST_FIXTURE_TEMPLATE.format(rows=rows))

    # Patch our CLI paths
    monkeypatch.setattr(bs, "FID_ROOT", fid_root)
    monkeypatch.setattr(bs, "CHARTERS_DIR", charters_dir)
    monkeypatch.setattr(bs, "MANIFEST", manifest)
    monkeypatch.setattr(bs, "REPO_ROOT", tmp_path)

    # Patch sign_charter module paths so its writes hit the temp tree
    from pipeline.funder_intelligence._methodology import sign_charter
    monkeypatch.setattr(sign_charter, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(sign_charter, "CHARTERS_DIR", charters_dir)
    monkeypatch.setattr(sign_charter, "MANIFEST", manifest)
    return {
        "tmp_path": tmp_path,
        "fid_root": fid_root,
        "charters_dir": charters_dir,
        "manifest": manifest,
    }


def _write_charter(charters_dir: pathlib.Path, aid: str) -> pathlib.Path:
    p = charters_dir / f"{aid}_charter_v0_DRAFT.md"
    p.write_text(CHARTER_FIXTURE_HEADER.format(aid=aid))
    return p


# ─────────────────────────────────────────────────────────────────
# Roster sanity
# ─────────────────────────────────────────────────────────────────

class TestRoster:
    def test_roster_has_14(self):
        assert len(bs.PHASE_1_ROSTER) == 14

    def test_roster_no_dups(self):
        assert len(set(bs.PHASE_1_ROSTER)) == 14

    def test_resolve_default_returns_all(self):
        assert bs._resolve_artifact_set(None) == list(bs.PHASE_1_ROSTER)

    def test_resolve_subset_ok(self):
        assert bs._resolve_artifact_set(["USDA-RD", "USDA-NIFA"]) == ["USDA-RD", "USDA-NIFA"]

    def test_resolve_rejects_unknown(self):
        with pytest.raises(ValueError, match="not in Phase-1 roster"):
            bs._resolve_artifact_set(["NOPE"])


# ─────────────────────────────────────────────────────────────────
# stage
# ─────────────────────────────────────────────────────────────────

class TestStage:
    def test_stage_writes_canonical_bytes_and_sigs_yaml(self, fid_tree, tmp_path):
        # Drop one charter
        _write_charter(fid_tree["charters_dir"], "USDA-RD")
        stage_dir = tmp_path / "stage"
        rc = bs.main(["stage", "--stage-dir", str(stage_dir), "--artifact-id", "USDA-RD"])
        assert rc == 0
        assert (stage_dir / "USDA-RD.canonical_bytes").exists()
        assert (stage_dir / "signatures.yaml").exists()

        doc = yaml.safe_load((stage_dir / "signatures.yaml").read_text())
        ceremony = doc["fid_batch_sign_ceremony"]
        assert len(ceremony["charters"]) == 1
        entry = ceremony["charters"][0]
        assert entry["artifact_id"] == "USDA-RD"
        assert entry["signature_hex"].startswith("<fill")
        assert len(entry["content_hash_sha3_512"]) == 128  # SHA3-512 hex
        assert entry["canonical_bytes_size"] > 0

    def test_stage_skips_already_signed(self, fid_tree, tmp_path):
        # Pretend USDA-RD is already signed
        signed = fid_tree["charters_dir"] / "USDA-RD_charter_v1_SIGNED.md"
        signed.write_text("# signed placeholder")
        # And NIFA has a DRAFT to stage
        _write_charter(fid_tree["charters_dir"], "USDA-NIFA")

        stage_dir = tmp_path / "stage"
        rc = bs.main([
            "stage", "--stage-dir", str(stage_dir),
            "--artifact-id", "USDA-RD",
            "--artifact-id", "USDA-NIFA",
        ])
        assert rc == 0
        # Only NIFA was staged
        assert not (stage_dir / "USDA-RD.canonical_bytes").exists()
        assert (stage_dir / "USDA-NIFA.canonical_bytes").exists()
        doc = yaml.safe_load((stage_dir / "signatures.yaml").read_text())
        ceremony = doc["fid_batch_sign_ceremony"]
        assert [c["artifact_id"] for c in ceremony["charters"]] == ["USDA-NIFA"]

    def test_stage_skips_missing_drafts(self, fid_tree, tmp_path, capsys):
        # No charter on disk anywhere
        stage_dir = tmp_path / "stage"
        rc = bs.main(["stage", "--stage-dir", str(stage_dir), "--artifact-id", "USDA-RD"])
        assert rc == 0
        out = capsys.readouterr().out
        assert "missing draft" in out

    def test_stage_rejects_unknown_artifact(self, fid_tree, tmp_path, capsys):
        stage_dir = tmp_path / "stage"
        rc = bs.main(["stage", "--stage-dir", str(stage_dir), "--artifact-id", "NOT-A-FUNDER"])
        assert rc == 1
        assert "not in Phase-1 roster" in capsys.readouterr().err

    def test_stage_all_14_when_no_subset(self, fid_tree, tmp_path):
        for aid in bs.PHASE_1_ROSTER:
            _write_charter(fid_tree["charters_dir"], aid)
        stage_dir = tmp_path / "stage"
        rc = bs.main(["stage", "--stage-dir", str(stage_dir)])
        assert rc == 0
        # 14 canonical_bytes files
        files = list(stage_dir.glob("*.canonical_bytes"))
        assert len(files) == 14


# ─────────────────────────────────────────────────────────────────
# apply
# ─────────────────────────────────────────────────────────────────

class TestApply:
    def _stage_and_sign(self, fid_tree, tmp_path, keypair, aids):
        priv, pub_hex = keypair
        for aid in aids:
            _write_charter(fid_tree["charters_dir"], aid)
        stage_dir = tmp_path / "stage"
        argv = ["stage", "--stage-dir", str(stage_dir)] + sum(
            (["--artifact-id", a] for a in aids), [],
        )
        rc = bs.main(argv)
        assert rc == 0

        # Sign each canonical_bytes
        sigs_path = stage_dir / "signatures.yaml"
        doc = yaml.safe_load(sigs_path.read_text())
        ceremony = doc["fid_batch_sign_ceremony"]
        ceremony["signer_pubkey_fingerprint"] = pub_hex
        for entry in ceremony["charters"]:
            canonical = pathlib.Path(entry["canonical_bytes_path"]).read_bytes()
            entry["signature_hex"] = priv.sign(canonical).hex()
        sigs_path.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True))
        return stage_dir

    def test_apply_signs_all_charters(self, fid_tree, tmp_path, keypair):
        stage_dir = self._stage_and_sign(
            fid_tree, tmp_path, keypair, ["USDA-RD", "USDA-NIFA"],
        )
        rc = bs.main([
            "apply", "--stage-dir", str(stage_dir),
            "--allow-missing-pubkey-yaml",
        ])
        assert rc == 0
        # Both charters renamed to _v1_SIGNED.md
        assert (fid_tree["charters_dir"] / "USDA-RD_charter_v1_SIGNED.md").exists()
        assert (fid_tree["charters_dir"] / "USDA-NIFA_charter_v1_SIGNED.md").exists()
        # v0 DRAFTs gone
        assert not (fid_tree["charters_dir"] / "USDA-RD_charter_v0_DRAFT.md").exists()
        assert not (fid_tree["charters_dir"] / "USDA-NIFA_charter_v0_DRAFT.md").exists()

    def test_apply_skips_placeholder_signature(self, fid_tree, tmp_path, keypair, capsys):
        priv, pub_hex = keypair
        _write_charter(fid_tree["charters_dir"], "USDA-RD")
        stage_dir = tmp_path / "stage"
        bs.main(["stage", "--stage-dir", str(stage_dir), "--artifact-id", "USDA-RD"])

        # Fill the pubkey but leave signature_hex as placeholder
        sigs_path = stage_dir / "signatures.yaml"
        doc = yaml.safe_load(sigs_path.read_text())
        doc["fid_batch_sign_ceremony"]["signer_pubkey_fingerprint"] = pub_hex
        sigs_path.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True))

        rc = bs.main([
            "apply", "--stage-dir", str(stage_dir),
            "--allow-missing-pubkey-yaml",
        ])
        assert rc == 0
        out = capsys.readouterr().out
        assert "SKIP" in out
        assert "skipped: 1" in out
        # Charter NOT renamed
        assert not (fid_tree["charters_dir"] / "USDA-RD_charter_v1_SIGNED.md").exists()

    def test_apply_fails_on_bad_signature(self, fid_tree, tmp_path, keypair, capsys):
        priv, pub_hex = keypair
        _write_charter(fid_tree["charters_dir"], "USDA-RD")
        stage_dir = tmp_path / "stage"
        bs.main(["stage", "--stage-dir", str(stage_dir), "--artifact-id", "USDA-RD"])

        # Put pubkey but inject a wrong signature
        sigs_path = stage_dir / "signatures.yaml"
        doc = yaml.safe_load(sigs_path.read_text())
        ceremony = doc["fid_batch_sign_ceremony"]
        ceremony["signer_pubkey_fingerprint"] = pub_hex
        ceremony["charters"][0]["signature_hex"] = "aa" * 64
        sigs_path.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True))

        rc = bs.main([
            "apply", "--stage-dir", str(stage_dir),
            "--allow-missing-pubkey-yaml",
        ])
        # 1 failure, 0 signed → rc 3
        assert rc == 3
        out = capsys.readouterr().out
        assert "FAIL" in out
        assert "failed:  1" in out

    def test_apply_requires_signer_fingerprint(self, fid_tree, tmp_path, capsys):
        _write_charter(fid_tree["charters_dir"], "USDA-RD")
        stage_dir = tmp_path / "stage"
        bs.main(["stage", "--stage-dir", str(stage_dir), "--artifact-id", "USDA-RD"])
        # Leave signer_pubkey_fingerprint as placeholder
        rc = bs.main(["apply", "--stage-dir", str(stage_dir)])
        assert rc == 1
        assert "signer_pubkey_fingerprint not set" in capsys.readouterr().err

    def test_apply_missing_signatures_yaml(self, fid_tree, tmp_path, capsys):
        stage_dir = tmp_path / "stage"
        stage_dir.mkdir()
        rc = bs.main(["apply", "--stage-dir", str(stage_dir)])
        assert rc == 1
        assert "signatures.yaml not at" in capsys.readouterr().err


# ─────────────────────────────────────────────────────────────────
# status
# ─────────────────────────────────────────────────────────────────

class TestStatus:
    def test_status_reports_missing_when_empty(self, fid_tree, capsys):
        rc = bs.main(["status"])
        assert rc == 0
        out = capsys.readouterr().out
        assert "MISSING" in out
        assert "missing: 14 / 14" in out

    def test_status_reports_signed_when_signed_file_present(self, fid_tree, capsys):
        _write_charter(fid_tree["charters_dir"], "USDA-RD")
        (fid_tree["charters_dir"] / "USDA-NIFA_charter_v1_SIGNED.md").write_text("# signed")
        rc = bs.main(["status"])
        assert rc == 0
        out = capsys.readouterr().out
        assert "signed: 1 / 14" in out
        assert "draft: 1 / 14" in out

    def test_status_with_stage_dir_reports_sigs_fill(self, fid_tree, tmp_path, keypair, capsys):
        priv, pub_hex = keypair
        _write_charter(fid_tree["charters_dir"], "USDA-RD")
        _write_charter(fid_tree["charters_dir"], "USDA-NIFA")
        stage_dir = tmp_path / "stage"
        bs.main([
            "stage", "--stage-dir", str(stage_dir),
            "--artifact-id", "USDA-RD",
            "--artifact-id", "USDA-NIFA",
        ])
        # Fill one of the two signatures
        sigs_path = stage_dir / "signatures.yaml"
        doc = yaml.safe_load(sigs_path.read_text())
        ceremony = doc["fid_batch_sign_ceremony"]
        canonical0 = pathlib.Path(ceremony["charters"][0]["canonical_bytes_path"]).read_bytes()
        ceremony["charters"][0]["signature_hex"] = priv.sign(canonical0).hex()
        sigs_path.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True))

        rc = bs.main(["status", "--stage-dir", str(stage_dir)])
        assert rc == 0
        out = capsys.readouterr().out
        assert "signatures filled: 1 / 2" in out


# ─────────────────────────────────────────────────────────────────
# verify-only
# ─────────────────────────────────────────────────────────────────

class TestVerifyOnly:
    def _stage_two_with_one_sig(self, fid_tree, tmp_path, keypair, valid: bool):
        priv, pub_hex = keypair
        _write_charter(fid_tree["charters_dir"], "USDA-RD")
        _write_charter(fid_tree["charters_dir"], "USDA-NIFA")
        stage_dir = tmp_path / "stage"
        bs.main([
            "stage", "--stage-dir", str(stage_dir),
            "--artifact-id", "USDA-RD",
            "--artifact-id", "USDA-NIFA",
        ])
        sigs_path = stage_dir / "signatures.yaml"
        doc = yaml.safe_load(sigs_path.read_text())
        ceremony = doc["fid_batch_sign_ceremony"]
        ceremony["signer_pubkey_fingerprint"] = pub_hex
        canonical0 = pathlib.Path(ceremony["charters"][0]["canonical_bytes_path"]).read_bytes()
        if valid:
            ceremony["charters"][0]["signature_hex"] = priv.sign(canonical0).hex()
        else:
            ceremony["charters"][0]["signature_hex"] = "aa" * 64
        sigs_path.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True))
        return stage_dir

    def test_verify_passes_valid_sig(self, fid_tree, tmp_path, keypair, capsys):
        stage_dir = self._stage_two_with_one_sig(fid_tree, tmp_path, keypair, valid=True)
        rc = bs.main(["verify-only", "--stage-dir", str(stage_dir)])
        assert rc == 0
        out = capsys.readouterr().out
        assert "verified ok: 1" in out
        assert "skipped: 1" in out

    def test_verify_fails_bad_sig(self, fid_tree, tmp_path, keypair, capsys):
        stage_dir = self._stage_two_with_one_sig(fid_tree, tmp_path, keypair, valid=False)
        rc = bs.main(["verify-only", "--stage-dir", str(stage_dir)])
        assert rc == 2
        out = capsys.readouterr().out
        assert "failed: 1" in out


# ─────────────────────────────────────────────────────────────────
# Argparse surface
# ─────────────────────────────────────────────────────────────────

class TestArgparse:
    def test_no_subcommand_errors(self):
        with pytest.raises(SystemExit):
            bs.main([])

    def test_stage_requires_stage_dir(self):
        with pytest.raises(SystemExit):
            bs.main(["stage"])

    def test_apply_requires_stage_dir(self):
        with pytest.raises(SystemExit):
            bs.main(["apply"])

    def test_status_no_args_ok(self, fid_tree, capsys):
        rc = bs.main(["status"])
        assert rc == 0
