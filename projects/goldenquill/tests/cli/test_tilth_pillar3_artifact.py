"""tilth pillar3 artifact CLI tests."""

from __future__ import annotations

import pathlib
import textwrap

import pytest
import yaml

from pipeline.cli import tilth_pillar3_artifact as cli


SIGNED_CHARTER_FIXTURE = textwrap.dedent(
    """\
    # Depth Charter — `TEST` (test fixture)

    ## §7 — Operator signature
    ```yaml
    charter_signed_at: 2026-05-18T20:00:00Z
    charter_signed_by_pubkey: aabbccdd
    charter_signed_canonical_bytes_sha3_512: deadbeef
    charter_ed25519_signature: cafebabe
    ```
    """
)


@pytest.fixture
def fid_tree(tmp_path, monkeypatch):
    """Build a tmp FID tree mirroring on-disk shape; patch cli paths."""
    fid_root = tmp_path / "pipeline" / "funder_intelligence"
    charters_dir = fid_root / "pillar_1_charters"
    p2_root = fid_root / "pillar_2_corpus"
    funders_dir = fid_root / "funders"
    programs_dir = fid_root / "programs"
    compliance_dir = fid_root / "compliance_cascades"
    for d in (charters_dir, p2_root, funders_dir, programs_dir, compliance_dir):
        d.mkdir(parents=True)

    # Seed family MANIFESTs with the roster rows the regen step expects.
    rows_funders = "\n".join(
        f"| {i+1} | `{aid}` | stub | `<pending_operator_attestation>` |"
        for i, aid in enumerate(cli.PHASE_1_FUNDERS)
    )
    (funders_dir / "MANIFEST.md").write_text(
        "# Funders MANIFEST\n\n| # | Artifact ID | Lifecycle | Sig prefix |\n"
        "|---|-------------|-----------|------------|\n" + rows_funders + "\n"
    )
    rows_programs = "\n".join(
        f"| {i+1} | `{aid}` | stub | `<pending_operator_attestation>` |"
        for i, aid in enumerate(cli.PHASE_1_PROGRAMS)
    )
    (programs_dir / "MANIFEST.md").write_text(
        "# Programs MANIFEST\n\n| # | Artifact ID | Lifecycle | Sig prefix |\n"
        "|---|-------------|-----------|------------|\n" + rows_programs + "\n"
    )

    monkeypatch.setattr(cli, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(cli, "FID_ROOT", fid_root)
    monkeypatch.setattr(cli, "CHARTERS_DIR", charters_dir)
    monkeypatch.setattr(cli, "P2_ROOT", p2_root)
    monkeypatch.setattr(cli, "FUNDERS_DIR", funders_dir)
    monkeypatch.setattr(cli, "PROGRAMS_DIR", programs_dir)
    monkeypatch.setattr(cli, "COMPLIANCE_DIR", compliance_dir)

    # Patch sign_artifact module so MANIFEST regen hits this tree
    from pipeline.funder_intelligence._methodology import sign_artifact
    monkeypatch.setattr(sign_artifact, "REPO_ROOT", tmp_path)
    monkeypatch.setattr(sign_artifact, "FID_ROOT", fid_root)
    monkeypatch.setattr(sign_artifact, "ARTIFACT_FAMILY_TO_DIR", {
        "funder": funders_dir,
        "program": programs_dir,
        "compliance_cascade": compliance_dir,
        "reviewer_type": fid_root / "reviewer_heuristics",
    })

    return {
        "tmp_path": tmp_path,
        "fid_root": fid_root,
        "charters_dir": charters_dir,
        "p2_root": p2_root,
        "funders_dir": funders_dir,
        "programs_dir": programs_dir,
    }


def _seed_signed_deps(fid_tree, aid):
    """Drop a signed charter + signed corpus yaml so init can succeed."""
    (fid_tree["charters_dir"] / f"{aid}_charter_v1_SIGNED.md").write_text(SIGNED_CHARTER_FIXTURE)
    corpus_dir = fid_tree["p2_root"] / aid
    corpus_dir.mkdir(parents=True, exist_ok=True)
    (corpus_dir / "_signed.yaml").write_text("artifact_id: " + aid + "\n")


# ─────────────────────────────────────────────────────────────────
# roster
# ─────────────────────────────────────────────────────────────────

class TestRoster:
    def test_funders_count(self):
        assert len(cli.PHASE_1_FUNDERS) == 8

    def test_programs_count(self):
        assert len(cli.PHASE_1_PROGRAMS) == 6

    def test_all_count(self):
        assert len(cli.PHASE_1_ALL) == 14

    def test_no_dup_across_families(self):
        assert len(set(cli.PHASE_1_ALL)) == 14

    def test_family_for_funder(self):
        assert cli.family_for("USDA-RD") == "funder"

    def test_family_for_program(self):
        assert cli.family_for("USDA-RD-RBDG-FY26") == "program"

    def test_family_for_unknown_raises(self):
        with pytest.raises(ValueError, match="not in Phase-1 roster"):
            cli.family_for("UNKNOWN")


# ─────────────────────────────────────────────────────────────────
# init
# ─────────────────────────────────────────────────────────────────

class TestInit:
    def test_init_requires_signed_charter(self, fid_tree, capsys):
        rc = cli.main(["init", "--artifact-id", "USDA-RD"])
        assert rc == 1
        assert "F-FID-ARTIFACT-UNSIGNED-CHARTER" in capsys.readouterr().err

    def test_init_requires_signed_corpus(self, fid_tree, capsys):
        # Charter signed, corpus not
        (fid_tree["charters_dir"] / "USDA-RD_charter_v1_SIGNED.md").write_text(SIGNED_CHARTER_FIXTURE)
        rc = cli.main(["init", "--artifact-id", "USDA-RD"])
        assert rc == 1
        assert "F-FID-ARTIFACT-UNSIGNED-CORPUS" in capsys.readouterr().err

    def test_init_succeeds_with_deps(self, fid_tree):
        _seed_signed_deps(fid_tree, "USDA-RD")
        rc = cli.main(["init", "--artifact-id", "USDA-RD"])
        assert rc == 0
        yaml_path = fid_tree["funders_dir"] / "USDA-RD.yaml"
        assert yaml_path.exists()
        data = yaml.safe_load(yaml_path.read_text())
        assert data["artifact_id"] == "USDA-RD"
        assert data["artifact_family"] == "funder"
        assert data["lifecycle_status"] == "stub"
        # All 5 §A.1 seats present
        for seat in ("scout", "scribe", "judge", "red_team", "logician"):
            assert seat in data["runtime_consumer"]
        # §A.2 canonical defaults present
        assert "facts belonging to another artifact" in data["artifact_must_not_contain"]
        # §A.3 strength_test present
        assert len(data["strength_test"]) == 3

    def test_init_program_stub_has_program_body(self, fid_tree):
        _seed_signed_deps(fid_tree, "USDA-RD-RBDG-FY26")
        rc = cli.main(["init", "--artifact-id", "USDA-RD-RBDG-FY26"])
        assert rc == 0
        data = yaml.safe_load(
            (fid_tree["programs_dir"] / "USDA-RD-RBDG-FY26.yaml").read_text()
        )
        assert data["artifact_family"] == "program"
        # Program-specific body keys present
        for k in ("scoring_rubric", "eligibility_gates", "match_requirements",
                  "scout_verify", "judge_scoring_map", "red_team_probes"):
            assert k in data

    def test_init_refuses_overwrite_without_force(self, fid_tree, capsys):
        _seed_signed_deps(fid_tree, "USDA-RD")
        cli.main(["init", "--artifact-id", "USDA-RD"])
        rc = cli.main(["init", "--artifact-id", "USDA-RD"])
        assert rc == 1
        assert "already exists" in capsys.readouterr().err

    def test_init_force_overwrites(self, fid_tree):
        _seed_signed_deps(fid_tree, "USDA-RD")
        cli.main(["init", "--artifact-id", "USDA-RD"])
        rc = cli.main(["init", "--artifact-id", "USDA-RD", "--force"])
        assert rc == 0

    def test_init_skip_deps_for_debug(self, fid_tree):
        rc = cli.main([
            "init", "--artifact-id", "USDA-RD",
            "--skip-dependency-check",
        ])
        assert rc == 0
        assert (fid_tree["funders_dir"] / "USDA-RD.yaml").exists()

    def test_init_unknown_artifact_rejected(self, fid_tree, capsys):
        rc = cli.main(["init", "--artifact-id", "FAKE-FUNDER"])
        assert rc == 1
        assert "not in Phase-1 roster" in capsys.readouterr().err


# ─────────────────────────────────────────────────────────────────
# status
# ─────────────────────────────────────────────────────────────────

class TestStatus:
    def test_status_full_roster_works(self, fid_tree, capsys):
        rc = cli.main(["status"])
        assert rc == 0
        out = capsys.readouterr().out
        for aid in cli.PHASE_1_ALL:
            assert aid in out

    def test_status_single_artifact(self, fid_tree, capsys):
        rc = cli.main(["status", "--artifact-id", "USDA-RD"])
        assert rc == 0
        out = capsys.readouterr().out
        assert "USDA-RD" in out
        assert "USDA-NIFA" not in out  # only one artifact reported

    def test_status_reports_deps(self, fid_tree, capsys):
        _seed_signed_deps(fid_tree, "USDA-RD")
        rc = cli.main(["status", "--artifact-id", "USDA-RD"])
        assert rc == 0
        out = capsys.readouterr().out
        assert "charter:C" in out
        assert "corpus:K" in out

    def test_status_reports_not_initialized(self, fid_tree, capsys):
        rc = cli.main(["status", "--artifact-id", "USDA-RD"])
        out = capsys.readouterr().out
        assert "not_initialized" in out

    def test_status_unknown_artifact_rejected(self, fid_tree, capsys):
        rc = cli.main(["status", "--artifact-id", "FAKE"])
        assert rc == 1
        assert "not in Phase-1 roster" in capsys.readouterr().err


# ─────────────────────────────────────────────────────────────────
# sign (integration via sign_artifact)
# ─────────────────────────────────────────────────────────────────

class TestSign:
    def test_sign_dry_run_after_init(self, fid_tree, capsys):
        _seed_signed_deps(fid_tree, "USDA-RD")
        cli.main(["init", "--artifact-id", "USDA-RD"])
        rc = cli.main(["sign", "--artifact-id", "USDA-RD", "--dry-run"])
        assert rc == 0
        out = capsys.readouterr().out
        assert "canonical_bytes_sha3_512" in out

    def test_sign_fails_without_init(self, fid_tree, capsys):
        rc = cli.main(["sign", "--artifact-id", "USDA-RD", "--dry-run"])
        assert rc == 1
        assert "Run `init`" in capsys.readouterr().err


# ─────────────────────────────────────────────────────────────────
# argparse surface
# ─────────────────────────────────────────────────────────────────

class TestArgparse:
    def test_no_subcommand_errors(self):
        with pytest.raises(SystemExit):
            cli.main([])

    def test_init_requires_artifact_id(self):
        with pytest.raises(SystemExit):
            cli.main(["init"])

    def test_sign_requires_artifact_id(self):
        with pytest.raises(SystemExit):
            cli.main(["sign"])
