"""Unit tests for pipeline.vault.layout (§2.9 + §7.1).

Round K. Covers VaultLayout path resolution, reserved-slug guard, and
seed-vs-cache partition classifier.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from pipeline.vault.error_codes import VaultSlugUnknown
from pipeline.vault.layout import (
    RESERVED_SLUGS,
    ReservedSlugError,
    VaultLayout,
    ensure_slug_not_reserved,
    is_cache_partition,
    is_seed_partition,
)


@pytest.fixture
def layout(tmp_path: Path) -> VaultLayout:
    home = tmp_path / "home"
    home.mkdir()
    return VaultLayout.from_repo_root(tmp_path, home_root=home)


class TestOrgPaths:
    def test_org_path(self, layout: VaultLayout) -> None:
        p = layout.org_path("mycosymbiotics")
        assert p == layout.repo_root / "orgs" / "mycosymbiotics"

    def test_org_vault_root(self, layout: VaultLayout) -> None:
        assert layout.org_vault_root("mystic") == (
            layout.repo_root / "orgs" / "mystic" / "vault"
        )

    def test_org_vault_children(self, layout: VaultLayout) -> None:
        slug = "mycosymbiotics"
        root = layout.org_vault_root(slug)
        assert layout.org_vault_init_marker(slug) == root / "init.marker"
        assert layout.org_vault_init_marker_hmac(slug) == root / "init.marker.hmac"
        assert layout.org_vault_write_lock(slug) == root / ".write.lock"
        assert layout.org_vault_compound_txn_lock(slug) == root / ".compound_txn.lock"
        assert layout.org_vault_broker_socket(slug) == root / ".broker.sock"
        assert layout.org_vault_subscribed_feeds(slug) == root / "subscribed_feeds"
        assert layout.org_vault_project_context(slug) == root / "project_context"
        assert layout.org_vault_drafts(slug) == root / "drafts"
        assert layout.org_vault_contracts(slug) == root / "contracts"
        assert layout.org_vault_audit(slug) == root / "audit"
        assert layout.org_vault_state(slug) == root / "state"
        assert layout.org_vault_claim_evidence(slug) == root / "claim_evidence"
        assert layout.org_vault_admin_risk(slug) == root / "admin_risk"
        assert layout.org_vault_conversation_log(slug) == root / "conversation_log"
        assert layout.org_vault_rails_reports(slug) == root / "rails_reports"
        assert layout.org_vault_lessons_delta(slug) == root / "lessons_delta"


class TestSharedPaths:
    def test_vault_shared_children(self, layout: VaultLayout) -> None:
        vs = layout.vault_shared_root
        assert layout.shared_init_marker == vs / "init.marker"
        assert layout.shared_init_marker_hmac == vs / "init.marker.hmac"
        assert layout.seed_manifest_json == vs / "seed_manifest.json"
        assert layout.seed_manifest_sig == vs / "seed_manifest.sig"
        assert layout.cedar_root == vs / "cedar"
        assert layout.cedar_policy("org_isolation") == vs / "cedar" / "org_isolation.cedar"
        assert layout.cedar_policy_head == vs / "cedar" / "policy_head.json"
        assert layout.process_wrappers_root == vs / "process_wrappers"
        assert layout.sandbox_profiles_root == vs / "sandbox_profiles"
        assert layout.seccomp_filters_root == vs / "seccomp_filters"
        assert layout.cached_opportunities_root == vs / "cached_opportunities"
        assert layout.research_db_root == vs / "research_db"
        assert layout.research_db_seed_root == vs / "research_db" / "seed"
        assert layout.sources_root == vs / "sources"
        assert layout.section_02_lock_marker == vs / "section_02.lock.json"

    def test_trust_root_mirror_paths(self, layout: VaultLayout) -> None:
        tr = layout.trust_root_mirror_root
        assert tr == layout.home_root / ".tilth" / "logician_trust_root"
        assert layout.trust_root_mirror_router_yaml == tr / "router.yaml"
        assert layout.trust_root_mirror_manifest == tr / "manifest.json"
        assert layout.trust_root_mirror_manifest_sig == tr / "manifest.sig"


class TestReservedSlugs:
    @pytest.mark.parametrize(
        "reserved",
        ["_shared", "_template", "_TEMPLATE", "init", "audit", "logician", "tilth", ".tilth"],
    )
    def test_rejects_reserved(self, reserved: str) -> None:
        with pytest.raises(ReservedSlugError):
            ensure_slug_not_reserved(reserved)

    def test_accepts_real_slug(self) -> None:
        ensure_slug_not_reserved("mycosymbiotics")
        ensure_slug_not_reserved("fit_farms_llc")
        ensure_slug_not_reserved("mystic_mamas")

    def test_reserved_slug_error_is_vault_slug_unknown(self) -> None:
        assert issubclass(ReservedSlugError, VaultSlugUnknown)

    def test_org_path_rejects_reserved(self, layout: VaultLayout) -> None:
        with pytest.raises(ReservedSlugError):
            layout.org_path("init")

    def test_rejects_non_string(self) -> None:
        with pytest.raises(TypeError):
            ensure_slug_not_reserved(42)  # type: ignore[arg-type]

    def test_reserved_set_is_frozen(self) -> None:
        assert isinstance(RESERVED_SLUGS, frozenset)


class TestPartitionClassifier:
    @pytest.mark.parametrize(
        "path,is_cache",
        [
            ("cached_opportunities/ollama.json", True),
            ("cached_opportunities/", True),
            ("research_db/index.json", True),
            ("research_db/stamps/2026-04.json", True),
            ("research_db/seed/corpus.json", False),
            ("research_db/seed/", False),
            ("cedar/org_isolation.cedar", False),
            ("seed_manifest.json", False),
            ("sandbox_profiles/scout.sb", False),
            ("process_wrappers/linux-systemd/tilth-seat@.service", False),
            ("sources/m15_sources.md", False),
            ("custom_dir/_cache/blob", True),
            ("some/deep/tree/_cache/item.json", True),
            ("leading_slash_allowed", False),
            ("/cached_opportunities/foo", True),
        ],
    )
    def test_classifies(self, path: str, is_cache: bool) -> None:
        assert is_cache_partition(path) is is_cache
        assert is_seed_partition(path) is not is_cache

    def test_rejects_non_string(self) -> None:
        with pytest.raises(TypeError):
            is_cache_partition(Path("cached_opportunities/x"))  # type: ignore[arg-type]


class TestVaultLayoutArgTypes:
    def test_from_repo_root_rejects_str(self) -> None:
        with pytest.raises(TypeError):
            VaultLayout.from_repo_root("/tmp/x")  # type: ignore[arg-type]

    def test_from_repo_root_rejects_str_home(self, tmp_path: Path) -> None:
        with pytest.raises(TypeError):
            VaultLayout.from_repo_root(tmp_path, home_root="/home/j")  # type: ignore[arg-type]

    def test_cedar_policy_rejects_non_string(self, layout: VaultLayout) -> None:
        with pytest.raises(TypeError):
            layout.cedar_policy(123)  # type: ignore[arg-type]

# ---------------------------------------------------------------------------
# BLUEPRINT_DEPS pin — drift-detection guard (§4.6 engineering_process_v0.1.md)
# ---------------------------------------------------------------------------


class TestBlueprintDepsPin:
    def test_blueprint_deps_pin(self) -> None:
        from pipeline.vault import layout as _mod

        deps = _mod.BLUEPRINT_DEPS
        assert "section_02_vault_topology.md" in deps
        section = deps["section_02_vault_topology.md"]
        assert section["version"] == "v7.1"
        assert section["hash_sha3_512_prefix16"] == "83a898275a4cf0a1"
