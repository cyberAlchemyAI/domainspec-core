"""Canonical paths and partition rules for the Vault on-disk layout.

Blueprint §2.9 on-disk layout + §2.9 seed-vs-cache partition + reserved-slug
guard.

Section 1's ``pipeline.sovereignty.org_slug`` performs primary canonicalisation
and reserved-slug enforcement. ``VaultLayout`` re-verifies to prevent drift —
one of the two checkpoints for reserved slugs so a single module bug cannot
smuggle a reserved slug into Vault-owned paths.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Final

from pipeline.vault.error_codes import VaultSlugUnknown


BLUEPRINT_DEPS: Final[dict[str, dict[str, object]]] = {
    "section_02_vault_topology.md": {
        "version": "v7.1",
        "hash_sha3_512_prefix16": "83a898275a4cf0a1",
        "sections_implemented": [
            "§2.9 on-disk layout — orgs/<slug>/ partition",
            "§2.9 seed-vs-cache partition rules",
            "§2.9 reserved-slug guard (defence-in-depth second checkpoint against §1 org_slug canonicalisation)",
        ],
    },
    "section_02_v7_2_amendment.md": {
        "version": "v7.2-DRAFT",
        "sections_implemented": [
            "§5 VaultLayout extensions — orgs/<slug>/vault/operational/<sub_kind>/",
        ],
    },
}


# ---------------------------------------------------------------------------
# Reserved-slug guard (§2.9 Reserved slugs)
# ---------------------------------------------------------------------------

RESERVED_SLUGS: frozenset[str] = frozenset(
    {
        "_shared",
        "_template",
        "_TEMPLATE",
        "init",
        "audit",
        "logician",
        "tilth",
        ".tilth",
    }
)


class ReservedSlugError(VaultSlugUnknown):
    """Raised when a caller passes a reserved slug to a layout helper."""


def ensure_slug_not_reserved(slug: str) -> None:
    if not isinstance(slug, str):
        raise TypeError(f"slug must be str, got {type(slug).__name__}")
    if slug in RESERVED_SLUGS:
        raise ReservedSlugError(f"slug {slug!r} is reserved by Vault")


# ---------------------------------------------------------------------------
# Seed-vs-cache partition (§2.9 M15.1 path-keyed partition)
# ---------------------------------------------------------------------------

_CACHE_PREFIXES: tuple[str, ...] = (
    "cached_opportunities/",
    "research_db/",
)
_CACHE_SUFFIX_MARKER = "/_cache/"
_RESEARCH_DB_SEED_PREFIX = "research_db/seed/"


def is_cache_partition(vault_shared_relative_path: str) -> bool:
    """Return True if the path is mutable (cache) partition under vault_shared/.

    Path-keyed: no content inspection needed. Rule:

    * starts with ``cached_opportunities/`` → cache
    * starts with ``research_db/`` and NOT with ``research_db/seed/`` → cache
    * contains ``/_cache/`` anywhere → cache
    * everything else → seed
    """
    if not isinstance(vault_shared_relative_path, str):
        raise TypeError(
            "vault_shared_relative_path must be str, got "
            f"{type(vault_shared_relative_path).__name__}"
        )
    rel = vault_shared_relative_path.lstrip("/")
    if rel.startswith(_RESEARCH_DB_SEED_PREFIX):
        return False
    for prefix in _CACHE_PREFIXES:
        if rel.startswith(prefix):
            return True
    if _CACHE_SUFFIX_MARKER in ("/" + rel):
        return True
    return False


def is_seed_partition(vault_shared_relative_path: str) -> bool:
    """Inverse of :func:`is_cache_partition`."""
    return not is_cache_partition(vault_shared_relative_path)


# ---------------------------------------------------------------------------
# VaultLayout — canonical path resolver
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class VaultLayout:
    """Canonical filesystem layout anchor for Section 2.

    Construct with ``repo_root`` and an optional ``home_root`` (defaults to
    ``Path.home()``). Every helper returns a resolved :class:`pathlib.Path`
    that callers can ``Path.is_file()`` / ``open()`` without further
    joining.
    """

    repo_root: Path
    home_root: Path

    @classmethod
    def from_repo_root(cls, repo_root: Path, *, home_root: Path | None = None) -> "VaultLayout":
        if not isinstance(repo_root, Path):
            raise TypeError(
                f"repo_root must be pathlib.Path, got {type(repo_root).__name__}"
            )
        if home_root is None:
            home_root = Path.home()
        if not isinstance(home_root, Path):
            raise TypeError(
                f"home_root must be pathlib.Path, got {type(home_root).__name__}"
            )
        return cls(repo_root=repo_root, home_root=home_root)

    # ------- org-scoped paths -------

    def org_path(self, slug: str) -> Path:
        ensure_slug_not_reserved(slug)
        return self.repo_root / "orgs" / slug

    def org_vault_root(self, slug: str) -> Path:
        return self.org_path(slug) / "vault"

    def org_vault_init_marker(self, slug: str) -> Path:
        return self.org_vault_root(slug) / "init.marker"

    def org_vault_init_marker_hmac(self, slug: str) -> Path:
        return self.org_vault_root(slug) / "init.marker.hmac"

    def org_vault_write_lock(self, slug: str) -> Path:
        return self.org_vault_root(slug) / ".write.lock"

    def org_vault_compound_txn_lock(self, slug: str) -> Path:
        return self.org_vault_root(slug) / ".compound_txn.lock"

    def org_vault_broker_socket(self, slug: str) -> Path:
        return self.org_vault_root(slug) / ".broker.sock"

    def org_vault_subscribed_feeds(self, slug: str) -> Path:
        return self.org_vault_root(slug) / "subscribed_feeds"

    def org_vault_project_context(self, slug: str) -> Path:
        return self.org_vault_root(slug) / "project_context"

    def org_vault_drafts(self, slug: str) -> Path:
        return self.org_vault_root(slug) / "drafts"

    def org_vault_contracts(self, slug: str) -> Path:
        return self.org_vault_root(slug) / "contracts"

    def org_vault_audit(self, slug: str) -> Path:
        return self.org_vault_root(slug) / "audit"

    def org_vault_state(self, slug: str) -> Path:
        return self.org_vault_root(slug) / "state"

    def org_vault_claim_evidence(self, slug: str) -> Path:
        return self.org_vault_root(slug) / "claim_evidence"

    def org_vault_admin_risk(self, slug: str) -> Path:
        return self.org_vault_root(slug) / "admin_risk"

    def org_vault_conversation_log(self, slug: str) -> Path:
        return self.org_vault_root(slug) / "conversation_log"

    def org_vault_rails_reports(self, slug: str) -> Path:
        return self.org_vault_root(slug) / "rails_reports"

    def org_vault_lessons_delta(self, slug: str) -> Path:
        return self.org_vault_root(slug) / "lessons_delta"

    # ------- v7.2 §5 (DRAFT) — operational-data sub-kind subtrees -------
    # Each sub-kind lives under orgs/<slug>/vault/operational/<sub_kind>/.
    # Adding a new sub-kind = one new helper here + one allowlist row in
    # vault_write.POST_GATE_ALLOWLIST + one new sub-kinds/ module +
    # one row in sub_kinds/registry.py.

    def org_vault_operational_root(self, slug: str) -> Path:
        return self.org_vault_root(slug) / "operational"

    def org_vault_operational_metrics(self, slug: str) -> Path:
        return self.org_vault_operational_root(slug) / "metrics"

    def org_vault_operational_financials(self, slug: str) -> Path:
        return self.org_vault_operational_root(slug) / "financials"

    def org_vault_operational_photos(self, slug: str) -> Path:
        return self.org_vault_operational_root(slug) / "photos"

    def org_vault_operational_narratives(self, slug: str) -> Path:
        return self.org_vault_operational_root(slug) / "narratives"

    def org_vault_operational_timeline(self, slug: str) -> Path:
        return self.org_vault_operational_root(slug) / "timeline"

    def org_vault_operational_beneficiaries(self, slug: str) -> Path:
        return self.org_vault_operational_root(slug) / "beneficiaries"

    def org_vault_operational_attachments(self, slug: str) -> Path:
        return self.org_vault_operational_root(slug) / "attachments"

    # ------- shared Vault paths (§2.9 vault_shared/) -------

    @property
    def vault_shared_root(self) -> Path:
        return self.repo_root / "vault_shared"

    @property
    def shared_init_marker(self) -> Path:
        return self.vault_shared_root / "init.marker"

    @property
    def shared_init_marker_hmac(self) -> Path:
        return self.vault_shared_root / "init.marker.hmac"

    @property
    def seed_manifest_json(self) -> Path:
        return self.vault_shared_root / "seed_manifest.json"

    @property
    def seed_manifest_sig(self) -> Path:
        return self.vault_shared_root / "seed_manifest.sig"

    @property
    def cedar_root(self) -> Path:
        return self.vault_shared_root / "cedar"

    @property
    def cedar_policy_head(self) -> Path:
        return self.cedar_root / "policy_head.json"

    def cedar_policy(self, name: str) -> Path:
        if not isinstance(name, str):
            raise TypeError(f"name must be str, got {type(name).__name__}")
        return self.cedar_root / f"{name}.cedar"

    @property
    def process_wrappers_root(self) -> Path:
        return self.vault_shared_root / "process_wrappers"

    @property
    def sandbox_profiles_root(self) -> Path:
        return self.vault_shared_root / "sandbox_profiles"

    @property
    def seccomp_filters_root(self) -> Path:
        return self.vault_shared_root / "seccomp_filters"

    @property
    def cached_opportunities_root(self) -> Path:
        return self.vault_shared_root / "cached_opportunities"

    @property
    def research_db_root(self) -> Path:
        return self.vault_shared_root / "research_db"

    @property
    def research_db_seed_root(self) -> Path:
        return self.research_db_root / "seed"

    @property
    def sources_root(self) -> Path:
        return self.vault_shared_root / "sources"

    @property
    def section_02_lock_marker(self) -> Path:
        return self.vault_shared_root / "section_02.lock.json"

    # ------- trust-root mirror (§2.9 ~/.tilth/logician_trust_root/) -------

    @property
    def trust_root_mirror_root(self) -> Path:
        return self.home_root / ".tilth" / "logician_trust_root"

    @property
    def trust_root_mirror_router_yaml(self) -> Path:
        return self.trust_root_mirror_root / "router.yaml"

    @property
    def trust_root_mirror_manifest(self) -> Path:
        return self.trust_root_mirror_root / "manifest.json"

    @property
    def trust_root_mirror_manifest_sig(self) -> Path:
        return self.trust_root_mirror_root / "manifest.sig"


__all__ = [
    "RESERVED_SLUGS",
    "ReservedSlugError",
    "VaultLayout",
    "ensure_slug_not_reserved",
    "is_cache_partition",
    "is_seed_partition",
]
