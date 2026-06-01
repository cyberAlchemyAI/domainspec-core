"""Shared fixtures for v7.2 operational sub-kind round-trip tests."""

from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture
def operational_org(tmp_path: Path) -> dict[str, Path]:
    """Construct an org vault root suitable for operational-write tests.

    Layout: ``<tmp>/orgs/<slug>/vault/`` with the seven operational
    subtree directories pre-created on first write (vault_write does the
    parent ``mkdir(parents=True)``). Returns a dict the per-sub-kind tests
    use as their canonical fixture handle.
    """
    slug = "myco"
    vault_root = tmp_path / "orgs" / slug / "vault"
    vault_root.mkdir(parents=True, exist_ok=True)
    return {
        "slug": slug,
        "root": vault_root,
        "lock": vault_root / ".write.lock",
        "operational": vault_root / "operational",
    }
