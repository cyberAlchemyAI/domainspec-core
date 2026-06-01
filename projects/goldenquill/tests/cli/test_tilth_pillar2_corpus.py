"""tilth pillar2 corpus CLI tests."""

from __future__ import annotations

import hashlib
import pathlib
import textwrap

import pytest
import yaml

from pipeline.cli import tilth_pillar2_corpus as cli


SIGNED_CHARTER_FIXTURE = textwrap.dedent(
    """\
    # Depth Charter — `TEST-FUNDER`

    > **Pillar 1 of 4** — SIGNED v1 (test fixture).

    ## §7 — Operator signature

    ```yaml
    charter_signed_at: 2026-05-18T20:00:00Z
    charter_signed_by_pubkey: aabbccdd
    charter_signed_canonical_bytes_sha3_512: deadbeef
    charter_ed25519_signature: cafebabe
    ```
    """
)


# ─────────────────────────────────────────────────────────────────
# Fixtures: monkeypatch FID_ROOT into a temp tree
# ─────────────────────────────────────────────────────────────────

@pytest.fixture
def fid_tree(tmp_path, monkeypatch):
    """Build a temporary FID tree mirroring on-disk shape; patch CLI paths."""
    fid_root = tmp_path / "pipeline" / "funder_intelligence"
    charters_dir = fid_root / "pillar_1_charters"
    p2_root = fid_root / "pillar_2_corpus"
    charters_dir.mkdir(parents=True)
    p2_root.mkdir(parents=True)
    # Inject a roster artifact ID for tests; cli.PHASE_1_ROSTER is the truth roster.
    monkeypatch.setattr(cli, "FID_ROOT", fid_root)
    monkeypatch.setattr(cli, "CHARTERS_DIR", charters_dir)
    monkeypatch.setattr(cli, "P2_ROOT", p2_root)
    monkeypatch.setattr(cli, "P2_MANIFEST", p2_root / "MANIFEST.md")
    return {"fid_root": fid_root, "charters_dir": charters_dir, "p2_root": p2_root}


@pytest.fixture
def real_roster_id():
    """Pick the methodology anchor as the universal test artifact_id."""
    return "USDA-RD-RBDG-FY26"


@pytest.fixture
def signed_charter(fid_tree, real_roster_id):
    p = fid_tree["charters_dir"] / f"{real_roster_id}_charter_v1_SIGNED.md"
    p.write_text(SIGNED_CHARTER_FIXTURE)
    return p


# ─────────────────────────────────────────────────────────────────
# Roster + path helpers
# ─────────────────────────────────────────────────────────────────

class TestRoster:
    def test_roster_has_14_artifacts(self) -> None:
        assert len(cli.PHASE_1_ROSTER) == 14

    def test_roster_no_duplicates(self) -> None:
        assert len(set(cli.PHASE_1_ROSTER)) == 14

    def test_assert_in_roster_rejects_unknown(self) -> None:
        with pytest.raises(ValueError, match="not in the Phase-1"):
            cli.assert_in_roster("UNKNOWN-FUNDER")

    def test_assert_in_roster_accepts_known(self) -> None:
        cli.assert_in_roster("USDA-RD-RBDG-FY26")  # no raise

    def test_signed_charter_path_shape(self) -> None:
        p = cli.signed_charter_path("USDA-RD")
        assert p.name == "USDA-RD_charter_v1_SIGNED.md"


# ─────────────────────────────────────────────────────────────────
# init
# ─────────────────────────────────────────────────────────────────

class TestInit:
    def test_init_requires_signed_charter(self, fid_tree, real_roster_id, capsys):
        rc = cli.main(["init", "--artifact-id", real_roster_id])
        assert rc == 1
        err = capsys.readouterr().err
        assert "F-FID-CORPUS-UNSIGNED-CHARTER" in err

    def test_init_rejects_unknown_artifact_id(self, fid_tree, capsys):
        rc = cli.main(["init", "--artifact-id", "NOT-A-REAL-FUNDER"])
        assert rc == 1
        err = capsys.readouterr().err
        assert "not in the Phase-1" in err

    def test_init_succeeds_with_signed_charter(self, fid_tree, signed_charter, real_roster_id):
        rc = cli.main(["init", "--artifact-id", real_roster_id])
        assert rc == 0
        root = cli.artifact_root(real_roster_id)
        assert (root / "raw" / ".gitkeep").exists()
        assert (root / "extracted" / ".gitkeep").exists()
        assert (root / "sources.yaml").exists()
        assert (root / "charter.signed.yaml").exists()

    def test_init_idempotent(self, fid_tree, signed_charter, real_roster_id):
        cli.main(["init", "--artifact-id", real_roster_id])
        # Modify sources.yaml to verify init doesn't clobber on second run.
        sp = cli.sources_yaml_path(real_roster_id)
        data = cli.load_sources(real_roster_id)
        data["files"].append({"file_path": "marker"})
        cli.write_sources(real_roster_id, data)
        rc = cli.main(["init", "--artifact-id", real_roster_id])
        assert rc == 0
        data2 = cli.load_sources(real_roster_id)
        assert any(f.get("file_path") == "marker" for f in data2["files"])


# ─────────────────────────────────────────────────────────────────
# fetch --register
# ─────────────────────────────────────────────────────────────────

class TestFetch:
    def _init(self, real_roster_id):
        cli.main(["init", "--artifact-id", real_roster_id])

    def test_fetch_registers_file(self, fid_tree, signed_charter, real_roster_id):
        self._init(real_roster_id)
        root = cli.artifact_root(real_roster_id)
        f = root / "raw" / "nofo.pdf"
        f.write_bytes(b"%PDF fake NOFO bytes")
        rc = cli.main([
            "fetch",
            "--artifact-id", real_roster_id,
            "--register", "raw/nofo.pdf",
            "--source-url", "https://example.gov/nofo.pdf",
            "--classification-tier", "1",
            "--classification-rationale", "Public NOFO",
        ])
        assert rc == 0
        data = cli.load_sources(real_roster_id)
        assert len(data["files"]) == 1
        entry = data["files"][0]
        assert entry["file_path"] == "raw/nofo.pdf"
        assert entry["sha256"] == hashlib.sha256(b"%PDF fake NOFO bytes").hexdigest()
        assert entry["classification_tier"] == 1
        assert entry["content_type"] == "application/pdf"

    def test_fetch_missing_file_returns_1(self, fid_tree, signed_charter, real_roster_id, capsys):
        self._init(real_roster_id)
        rc = cli.main([
            "fetch",
            "--artifact-id", real_roster_id,
            "--register", "raw/missing.pdf",
            "--source-url", "https://example.gov/",
            "--classification-tier", "1",
        ])
        assert rc == 1
        assert "file not on disk" in capsys.readouterr().err

    def test_fetch_noop_on_same_hash(self, fid_tree, signed_charter, real_roster_id, capsys):
        self._init(real_roster_id)
        root = cli.artifact_root(real_roster_id)
        f = root / "raw" / "nofo.pdf"
        f.write_bytes(b"bytes")
        argv = [
            "fetch",
            "--artifact-id", real_roster_id,
            "--register", "raw/nofo.pdf",
            "--source-url", "https://example.gov/",
            "--classification-tier", "1",
        ]
        assert cli.main(argv) == 0
        rc2 = cli.main(argv)
        assert rc2 == 0
        out = capsys.readouterr().out
        assert "NOOP" in out
        # Still only one entry
        data = cli.load_sources(real_roster_id)
        assert len(data["files"]) == 1

    def test_fetch_hash_mismatch_returns_2(self, fid_tree, signed_charter, real_roster_id, capsys):
        self._init(real_roster_id)
        root = cli.artifact_root(real_roster_id)
        f = root / "raw" / "nofo.pdf"
        f.write_bytes(b"first")
        cli.main([
            "fetch",
            "--artifact-id", real_roster_id,
            "--register", "raw/nofo.pdf",
            "--source-url", "https://example.gov/",
            "--classification-tier", "1",
        ])
        # Mutate file → register again → mismatch
        f.write_bytes(b"second")
        rc = cli.main([
            "fetch",
            "--artifact-id", real_roster_id,
            "--register", "raw/nofo.pdf",
            "--source-url", "https://example.gov/",
            "--classification-tier", "1",
        ])
        assert rc == 2
        assert "F-FID-CORPUS-HASH-MISMATCH" in capsys.readouterr().err

    def test_fetch_refuses_unsigned_charter(self, fid_tree, real_roster_id, capsys):
        # No signed charter, no init either
        rc = cli.main([
            "fetch",
            "--artifact-id", real_roster_id,
            "--register", "raw/nofo.pdf",
            "--source-url", "https://example.gov/",
            "--classification-tier", "1",
        ])
        assert rc == 1
        assert "F-FID-CORPUS-UNSIGNED-CHARTER" in capsys.readouterr().err


# ─────────────────────────────────────────────────────────────────
# extract validation
# ─────────────────────────────────────────────────────────────────

class TestExtract:
    def _init_with_source(self, fid_tree, real_roster_id):
        cli.main(["init", "--artifact-id", real_roster_id])
        root = cli.artifact_root(real_roster_id)
        f = root / "raw" / "nofo.pdf"
        f.write_bytes(b"%PDF fake")
        cli.main([
            "fetch",
            "--artifact-id", real_roster_id,
            "--register", "raw/nofo.pdf",
            "--source-url", "https://example.gov/",
            "--classification-tier", "1",
        ])
        return root

    def _write_cluster(self, root: pathlib.Path, cluster: str, facts: list[dict]) -> None:
        (root / "extracted" / f"{cluster}.yaml").write_text(
            yaml.safe_dump({"cluster_name": cluster, "facts": facts}, sort_keys=False)
        )

    def test_extract_passes_well_formed(self, fid_tree, signed_charter, real_roster_id):
        root = self._init_with_source(fid_tree, real_roster_id)
        self._write_cluster(root, "gates", [
            {
                "fact_id": "F1",
                "corpus_ref": f"{real_roster_id}:raw/nofo.pdf:p1",
                "verbatim_quote": "Eligible entities must serve rural areas with populations of 50,000 or fewer.",
                "analysis": "Rural-pop gate.",
                "classification_tier": 1,
            }
        ])
        rc = cli.main(["extract", "--artifact-id", real_roster_id, "--cluster", "gates"])
        assert rc == 0

    def test_extract_fails_on_orphan_fact(self, fid_tree, signed_charter, real_roster_id, capsys):
        root = self._init_with_source(fid_tree, real_roster_id)
        self._write_cluster(root, "gates", [
            {
                "fact_id": "F1",
                # corpus_ref pointing at unregistered file
                "corpus_ref": f"{real_roster_id}:raw/ghost.pdf:p1",
                "verbatim_quote": "Some fact.",
            }
        ])
        rc = cli.main(["extract", "--artifact-id", real_roster_id, "--cluster", "gates"])
        assert rc == 1
        assert "F-FID-CORPUS-FACT-ORPHAN" in capsys.readouterr().err

    def test_extract_fails_on_missing_corpus_ref(self, fid_tree, signed_charter, real_roster_id, capsys):
        root = self._init_with_source(fid_tree, real_roster_id)
        self._write_cluster(root, "gates", [
            {"fact_id": "F1", "verbatim_quote": "no ref"}
        ])
        rc = cli.main(["extract", "--artifact-id", real_roster_id, "--cluster", "gates"])
        assert rc == 1
        assert "F-FID-CORPUS-FACT-ORPHAN" in capsys.readouterr().err

    def test_extract_fails_on_verbatim_too_long(self, fid_tree, signed_charter, real_roster_id, capsys):
        root = self._init_with_source(fid_tree, real_roster_id)
        self._write_cluster(root, "gates", [
            {
                "fact_id": "F1",
                "corpus_ref": f"{real_roster_id}:raw/nofo.pdf:p1",
                "verbatim_quote": "Sentence one. Sentence two. Sentence three.",
            }
        ])
        rc = cli.main(["extract", "--artifact-id", real_roster_id, "--cluster", "gates"])
        assert rc == 1
        assert "F-FID-CORPUS-VERBATIM-TOO-LONG" in capsys.readouterr().err

    def test_extract_passes_exactly_two_sentences(self, fid_tree, signed_charter, real_roster_id):
        root = self._init_with_source(fid_tree, real_roster_id)
        self._write_cluster(root, "gates", [
            {
                "fact_id": "F1",
                "corpus_ref": f"{real_roster_id}:raw/nofo.pdf:p1",
                "verbatim_quote": "Sentence one. Sentence two.",
            }
        ])
        rc = cli.main(["extract", "--artifact-id", real_roster_id, "--cluster", "gates"])
        assert rc == 0

    def test_extract_missing_cluster_returns_1(self, fid_tree, signed_charter, real_roster_id, capsys):
        cli.main(["init", "--artifact-id", real_roster_id])
        rc = cli.main(["extract", "--artifact-id", real_roster_id, "--cluster", "ghost"])
        assert rc == 1
        assert "extracted cluster not at" in capsys.readouterr().err


# ─────────────────────────────────────────────────────────────────
# status
# ─────────────────────────────────────────────────────────────────

class TestStatus:
    def test_status_not_initialized_when_no_charter(self, fid_tree, real_roster_id, capsys):
        rc = cli.main(["status", "--artifact-id", real_roster_id])
        assert rc == 0
        out = capsys.readouterr().out
        assert "NOT_INITIALIZED" in out
        assert "MISSING" in out

    def test_status_fetching_after_init(self, fid_tree, signed_charter, real_roster_id, capsys):
        cli.main(["init", "--artifact-id", real_roster_id])
        rc = cli.main(["status", "--artifact-id", real_roster_id])
        assert rc == 0
        out = capsys.readouterr().out
        assert "FETCHING" in out
        assert "SIGNED v1" in out

    def test_status_extracting_after_source_and_cluster(self, fid_tree, signed_charter, real_roster_id, capsys):
        cli.main(["init", "--artifact-id", real_roster_id])
        root = cli.artifact_root(real_roster_id)
        (root / "raw" / "nofo.pdf").write_bytes(b"bytes")
        cli.main([
            "fetch", "--artifact-id", real_roster_id,
            "--register", "raw/nofo.pdf",
            "--source-url", "https://example.gov/",
            "--classification-tier", "1",
        ])
        # Add an extracted cluster
        (root / "extracted" / "c.yaml").write_text("facts: []\n")
        rc = cli.main(["status", "--artifact-id", real_roster_id])
        assert rc == 0
        out = capsys.readouterr().out
        assert "READY_FOR_SIGN" in out or "EXTRACTING" in out

    def test_status_detects_hash_mismatch(self, fid_tree, signed_charter, real_roster_id, capsys):
        cli.main(["init", "--artifact-id", real_roster_id])
        root = cli.artifact_root(real_roster_id)
        (root / "raw" / "nofo.pdf").write_bytes(b"first")
        cli.main([
            "fetch", "--artifact-id", real_roster_id,
            "--register", "raw/nofo.pdf",
            "--source-url", "https://example.gov/",
            "--classification-tier", "1",
        ])
        # Mutate after registration
        (root / "raw" / "nofo.pdf").write_bytes(b"second")
        rc = cli.main(["status", "--artifact-id", real_roster_id])
        assert rc == 2
        assert "F-FID-CORPUS-HASH-MISMATCH" in capsys.readouterr().out


# ─────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────

class TestHelpers:
    @pytest.mark.parametrize("text,expected", [
        ("", 0),
        ("One sentence.", 1),
        ("Sentence one. Sentence two.", 2),
        ("First. Second. Third.", 3),
        ("No terminator", 1),
        ("Q one? A two!", 2),
    ])
    def test_count_sentences(self, text, expected):
        assert cli.count_sentences(text) == expected

    def test_guess_content_type(self):
        assert cli._guess_content_type(pathlib.Path("x.pdf")) == "application/pdf"
        assert cli._guess_content_type(pathlib.Path("x.html")) == "text/html"
        assert cli._guess_content_type(pathlib.Path("x.unknown")) == "application/octet-stream"


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

    def test_fetch_requires_required_args(self):
        with pytest.raises(SystemExit):
            cli.main(["fetch", "--artifact-id", "USDA-RD"])
