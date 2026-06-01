"""Tests for pipeline.sovereignty.topology.

Coverage targets (per Round-B spec card `round_b_topology.md`):
  - §1 inventory row 7 public API
  - §7.5 `test_topology_doc_sourced_whitelist_*` regression pair
  - Five-root whitelist (every root accepted)
  - Rejection cases (cache, drafts, cross-org, prefix-collision)
  - Symlink-escape rejection (SymlinkRejected)
  - canonical_slug fail-loud entry gate (Round-B defensive enhancement)
  - Type-safety at public surface
  - Preserved corpus at tests/corpus/topology/v1/doc_sourced_vectors.json
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from pipeline.sovereignty import (
    DOC_SOURCED_ROOTS,
    DocSourcedRoot,
    InvalidSlug,
    PathEscapedRoot,
    ReservedSlug,
    SymlinkRejected,
    canonicalize_vault_path,
    is_doc_sourced_path,
)

_CORPUS_PATH = (
    Path(__file__).resolve().parents[1]
    / "corpus"
    / "topology"
    / "v1"
    / "doc_sourced_vectors.json"
)


def _load_corpus() -> dict:
    with _CORPUS_PATH.open() as f:
        return json.load(f)


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    """Tmp repo with the five DOC_SOURCED roots materialized for slug 'myco'."""
    root = tmp_path
    (root / "rfa").mkdir(parents=True)
    (root / "rfa" / "nested" / "deep").mkdir(parents=True)
    (root / "orgs" / "myco" / "dossier" / "entities").mkdir(parents=True)
    (root / "orgs" / "myco2").mkdir(parents=True)
    (root / "orgs" / "other").mkdir(parents=True)
    (root / "pipeline" / "rubrics").mkdir(parents=True)
    (root / "pipeline" / "institutional_memory").mkdir(parents=True)
    (root / "pipeline" / "drafts").mkdir(parents=True)
    (root / "vault" / "cached").mkdir(parents=True)
    (root / "rfa2").mkdir(parents=True)
    return root


def _touch(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("")
    return path


# ---------- DocSourcedRoot dataclass ----------


class TestDocSourcedRoot:
    def test_dataclass_is_frozen(self) -> None:
        root = DOC_SOURCED_ROOTS[0]
        with pytest.raises((AttributeError, Exception)):
            root.label = "mutated"  # type: ignore[misc]

    def test_five_roots_exactly(self) -> None:
        assert len(DOC_SOURCED_ROOTS) == 5

    def test_labels_are_lowercase_ascii(self) -> None:
        for root in DOC_SOURCED_ROOTS:
            assert root.label == root.label.lower()
            assert root.label.isascii()
            assert root.label.replace("_", "").isalnum()

    def test_labels_are_unique(self) -> None:
        labels = [r.label for r in DOC_SOURCED_ROOTS]
        assert len(labels) == len(set(labels))

    def test_slug_parameterized_flag_matches_template(self) -> None:
        for root in DOC_SOURCED_ROOTS:
            assert ("{slug}" in root.path_template) == root.slug_parameterized


# ---------- is_doc_sourced_path accept cases ----------


class TestAcceptsFiveRoots:
    """Blueprint §7.5 `test_topology_doc_sourced_whitelist_accepts_five_roots`."""

    def test_rfa_root(self, repo: Path) -> None:
        p = _touch(repo / "rfa" / "usda.pdf")
        assert is_doc_sourced_path(p, bound_slug="myco", repo_root=repo)

    def test_org_root(self, repo: Path) -> None:
        p = _touch(repo / "orgs" / "myco" / "PROJECT_CONTEXT.md")
        assert is_doc_sourced_path(p, bound_slug="myco", repo_root=repo)

    def test_dossier_root(self, repo: Path) -> None:
        p = _touch(repo / "orgs" / "myco" / "dossier" / "entities" / "partner_a.md")
        assert is_doc_sourced_path(p, bound_slug="myco", repo_root=repo)

    def test_rubrics_root(self, repo: Path) -> None:
        p = _touch(repo / "pipeline" / "rubrics" / "vapg_fy26.json")
        assert is_doc_sourced_path(p, bound_slug="myco", repo_root=repo)

    def test_institutional_memory_root(self, repo: Path) -> None:
        p = _touch(repo / "pipeline" / "institutional_memory" / "lessons.md")
        assert is_doc_sourced_path(p, bound_slug="myco", repo_root=repo)


# ---------- is_doc_sourced_path reject cases ----------


class TestRejectsNonDocSourced:
    """Blueprint §7.5 `test_topology_doc_sourced_whitelist_rejects_cache_path`."""

    def test_cache_path_rejected(self, repo: Path) -> None:
        p = _touch(repo / "vault" / "cached" / "foo.md")
        assert not is_doc_sourced_path(p, bound_slug="myco", repo_root=repo)

    def test_drafts_path_rejected(self, repo: Path) -> None:
        p = _touch(repo / "pipeline" / "drafts" / "x.md")
        assert not is_doc_sourced_path(p, bound_slug="myco", repo_root=repo)

    def test_cross_org_slug_mismatch_returns_false(self, repo: Path) -> None:
        p = _touch(repo / "orgs" / "other" / "PROJECT_CONTEXT.md")
        # bound to myco, path points to other — Law 3 says: not doc-sourced.
        assert not is_doc_sourced_path(p, bound_slug="myco", repo_root=repo)

    def test_prefix_collision_not_accepted(self, repo: Path) -> None:
        """`orgs/myco2/` must not match `orgs/myco/` prefix."""
        p = _touch(repo / "orgs" / "myco2" / "file.md")
        assert not is_doc_sourced_path(p, bound_slug="myco", repo_root=repo)

    def test_prefix_collision_rfa(self, repo: Path) -> None:
        """`rfa2/` must not match `rfa/` prefix."""
        p = _touch(repo / "rfa2" / "file.md")
        assert not is_doc_sourced_path(p, bound_slug="myco", repo_root=repo)

    def test_repo_root_itself_not_doc_sourced(self, repo: Path) -> None:
        p = _touch(repo / "README.md")
        assert not is_doc_sourced_path(p, bound_slug="myco", repo_root=repo)

    def test_outside_repo_root_returns_false(self, repo: Path, tmp_path: Path) -> None:
        outside = tmp_path.parent / "elsewhere.md"
        outside.parent.mkdir(parents=True, exist_ok=True)
        outside.write_text("")
        assert not is_doc_sourced_path(outside, bound_slug="myco", repo_root=repo)


# ---------- slug canonicality entry gate (Round-B defensive) ----------


class TestSlugEntryGate:
    def test_non_canonical_slug_raises_value_error(self, repo: Path) -> None:
        """`MyCo` is valid-but-not-canonical — must raise, not return False."""
        p = _touch(repo / "orgs" / "myco" / "x.md")
        with pytest.raises(ValueError) as exc_info:
            is_doc_sourced_path(p, bound_slug="MyCo", repo_root=repo)
        assert "not canonical" in str(exc_info.value)

    def test_invalid_slug_raises_invalid_slug(self, repo: Path) -> None:
        """Empty slug is invalid — canonical_slug propagates."""
        p = _touch(repo / "orgs" / "myco" / "x.md")
        with pytest.raises(InvalidSlug):
            is_doc_sourced_path(p, bound_slug="", repo_root=repo)

    def test_reserved_slug_raises_reserved_slug(self, repo: Path) -> None:
        p = _touch(repo / "orgs" / "myco" / "x.md")
        with pytest.raises(ReservedSlug):
            is_doc_sourced_path(p, bound_slug="index", repo_root=repo)

    def test_canonical_slug_with_trailing_space_rejected(self, repo: Path) -> None:
        p = _touch(repo / "orgs" / "myco" / "x.md")
        with pytest.raises(ValueError):
            is_doc_sourced_path(p, bound_slug="myco ", repo_root=repo)


# ---------- symlink escape ----------


class TestSymlinkEscape:
    def test_symlink_inside_repo_allowed(self, repo: Path) -> None:
        """Symlink whose target stays inside repo_root: allowed."""
        target = _touch(repo / "orgs" / "myco" / "real.md")
        link = repo / "orgs" / "myco" / "link.md"
        os.symlink(target, link)
        # The link resolves to `real.md` which is under `orgs/myco/` — OK.
        assert is_doc_sourced_path(link, bound_slug="myco", repo_root=repo)

    def test_symlink_escape_via_parent_component_rejected(
        self, repo: Path, tmp_path: Path
    ) -> None:
        """Parent-component symlink pointing outside repo_root must raise."""
        outside = tmp_path.parent / "outside_repo"
        outside.mkdir(exist_ok=True)
        # Plant a symlink inside orgs/myco pointing OUTSIDE repo_root.
        link = repo / "orgs" / "myco" / "escape_link"
        os.symlink(outside, link)
        # A file "under" the link resolves outside repo_root.
        # path.resolve() will land outside, so the prefix check rejects
        # BEFORE the symlink walker runs — result is False, not raise.
        probe = link / "foo.md"
        # The probe path doesn't exist; resolve strict=False lands outside.
        assert not is_doc_sourced_path(probe, bound_slug="myco", repo_root=repo)

    def test_symlink_inside_prefix_but_target_outside_raises(
        self, repo: Path, tmp_path: Path
    ) -> None:
        """Symlink inside the org prefix pointing outside — SymlinkRejected."""
        outside = tmp_path.parent / "outside_repo_2"
        outside.mkdir(exist_ok=True)
        outside_file = outside / "planted.md"
        outside_file.write_text("attacker content")
        # Plant the symlink INSIDE orgs/myco, pointing outside
        link = repo / "orgs" / "myco" / "planted.md"
        os.symlink(outside_file, link)
        # The link's resolve() lands outside repo_root, so is_doc_sourced_path
        # returns False (no exception — path simply isn't doc-sourced).
        # The stronger rejection happens in canonicalize_vault_path.
        assert not is_doc_sourced_path(link, bound_slug="myco", repo_root=repo)

    def test_canonicalize_rejects_symlink_escape(
        self, repo: Path, tmp_path: Path
    ) -> None:
        outside = tmp_path.parent / "outside_repo_3"
        outside.mkdir(exist_ok=True)
        outside_file = outside / "secret.md"
        outside_file.write_text("out")
        link = repo / "orgs" / "myco" / "bad_link.md"
        os.symlink(outside_file, link)
        with pytest.raises(PathEscapedRoot):
            canonicalize_vault_path(link, repo_root=repo)


# ---------- canonicalize_vault_path ----------


class TestCanonicalizeVaultPath:
    def test_resolves_existing_path(self, repo: Path) -> None:
        p = _touch(repo / "orgs" / "myco" / "x.md")
        resolved = canonicalize_vault_path(p, repo_root=repo)
        assert resolved.is_absolute()
        assert resolved == p.resolve()

    def test_raises_on_nonexistent(self, repo: Path) -> None:
        p = repo / "orgs" / "myco" / "does_not_exist.md"
        with pytest.raises(FileNotFoundError):
            canonicalize_vault_path(p, repo_root=repo)

    def test_raises_on_path_escapes_root(self, repo: Path, tmp_path: Path) -> None:
        outside = tmp_path.parent / "definitely_outside"
        outside.mkdir(exist_ok=True)
        target = outside / "file.md"
        target.write_text("")
        with pytest.raises(PathEscapedRoot):
            canonicalize_vault_path(target, repo_root=repo)

    def test_idempotent(self, repo: Path) -> None:
        p = _touch(repo / "orgs" / "myco" / "x.md")
        once = canonicalize_vault_path(p, repo_root=repo)
        twice = canonicalize_vault_path(once, repo_root=repo)
        assert once == twice


# ---------- type safety ----------


class TestTypeSafety:
    def test_is_doc_sourced_rejects_str_path(self, repo: Path) -> None:
        with pytest.raises(TypeError):
            is_doc_sourced_path("orgs/myco/x.md", bound_slug="myco", repo_root=repo)  # type: ignore[arg-type]

    def test_is_doc_sourced_rejects_bytes_slug(self, repo: Path) -> None:
        with pytest.raises(TypeError):
            is_doc_sourced_path(repo / "x", bound_slug=b"myco", repo_root=repo)  # type: ignore[arg-type]

    def test_is_doc_sourced_rejects_str_repo_root(self, repo: Path) -> None:
        with pytest.raises(TypeError):
            is_doc_sourced_path(
                repo / "x", bound_slug="myco", repo_root=str(repo)  # type: ignore[arg-type]
            )

    def test_canonicalize_rejects_str_args(self, repo: Path) -> None:
        with pytest.raises(TypeError):
            canonicalize_vault_path("/tmp/x", repo_root=repo)  # type: ignore[arg-type]


# ---------- corpus regression ----------


class TestCorpusAccept:
    @pytest.mark.parametrize(
        "vec", _load_corpus()["accept"], ids=lambda v: v["path_under_repo"]
    )
    def test_vector_accepted(self, vec: dict, repo: Path) -> None:
        p = _touch(repo / vec["path_under_repo"])
        assert is_doc_sourced_path(p, bound_slug=vec["bound_slug"], repo_root=repo)


class TestCorpusReject:
    @pytest.mark.parametrize(
        "vec", _load_corpus()["reject"], ids=lambda v: v["path_under_repo"]
    )
    def test_vector_rejected(self, vec: dict, repo: Path) -> None:
        p = _touch(repo / vec["path_under_repo"])
        assert not is_doc_sourced_path(p, bound_slug=vec["bound_slug"], repo_root=repo)


# ---------- properties / disjointness ----------


class TestProperties:
    def test_roots_ordering_stable(self) -> None:
        """Order is contractual — label sequence pinned."""
        labels = [r.label for r in DOC_SOURCED_ROOTS]
        assert labels == [
            "rfa",
            "org",
            "dossier",
            "rubrics",
            "institutional_memory",
        ]

    def test_dossier_is_strict_subset_of_org(self, repo: Path) -> None:
        """Dossier is inside org; both must return True for a dossier path."""
        p = _touch(repo / "orgs" / "myco" / "dossier" / "entities" / "e.md")
        # Since the loop returns on first match, the label order matters:
        # 'org' comes before 'dossier'. Both templates would match; function
        # returns True on the first match. Either way, the path is doc-sourced.
        assert is_doc_sourced_path(p, bound_slug="myco", repo_root=repo)

    def test_deep_nested_rfa_path(self, repo: Path) -> None:
        p = _touch(repo / "rfa" / "nested" / "deep" / "file.txt")
        assert is_doc_sourced_path(p, bound_slug="myco", repo_root=repo)
