"""Unit tests for pipeline.vault.research_db_query_skill (§3.3 + §2.9).

Round Q' — thin wrapper over :func:`pipeline.vault.vault_query_skill.vault_read`
scoped to ``vault_shared/research_db/``. Enforces cross-org key rejection.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Iterator

import pytest

from pipeline.vault.error_codes import VaultAccessDenied, VaultCrossOrgAccess
from pipeline.vault.fd_broker import FDBroker
from pipeline.vault.gate_and_open import open_vault_root
from pipeline.vault.research_db_query_skill import research_db_read


@pytest.fixture
def vault_tree(tmp_path: Path) -> Path:
    vault_root = tmp_path / "vault_root"
    vault_root.mkdir()
    rdb = vault_root / "vault_shared" / "research_db"
    rdb.mkdir(parents=True)
    (rdb / "entry_01.json").write_bytes(b'{"fit": "rfa-123"}')
    (rdb / "seed").mkdir()
    (rdb / "seed" / "seed_01.json").write_bytes(b'{"seeded": true}')
    return vault_root


@pytest.fixture
def broker(vault_tree: Path) -> Iterator[FDBroker]:
    root_fd = open_vault_root(vault_tree)
    try:
        yield FDBroker(vault_root_fd=root_fd, vault_root_path=vault_tree)
    finally:
        os.close(root_fd)


# ---------------------------------------------------------------------------
# Happy path
# ---------------------------------------------------------------------------


class TestHappyPath:
    def test_reads_entry(self, broker: FDBroker) -> None:
        data, identity = research_db_read(
            key="entry_01.json",
            session_id="s",
            slug="demo",
            broker=broker,
        )
        assert data == b'{"fit": "rfa-123"}'
        assert identity.fs_type != "denied"

    def test_reads_seeded_entry(self, broker: FDBroker) -> None:
        data, _ = research_db_read(
            key="seed/seed_01.json",
            session_id="s",
            slug="demo",
            broker=broker,
        )
        assert data == b'{"seeded": true}'


# ---------------------------------------------------------------------------
# Cross-org key rejection
# ---------------------------------------------------------------------------


class TestCrossOrgRejection:
    def test_orgs_prefix_rejected(self, broker: FDBroker) -> None:
        with pytest.raises(VaultCrossOrgAccess):
            research_db_read(
                key="orgs/other/vault/secret.json",
                session_id="s",
                slug="demo",
                broker=broker,
            )

    def test_parent_path_rejected(self, broker: FDBroker) -> None:
        with pytest.raises(VaultCrossOrgAccess):
            research_db_read(
                key="../../etc/passwd",
                session_id="s",
                slug="demo",
                broker=broker,
            )

    def test_absolute_path_rejected(self, broker: FDBroker) -> None:
        with pytest.raises(VaultCrossOrgAccess):
            research_db_read(
                key="/etc/passwd",
                session_id="s",
                slug="demo",
                broker=broker,
            )

    def test_vault_shared_prefix_rejected(self, broker: FDBroker) -> None:
        # The key must not include the research_db/ prefix itself — the skill
        # prepends it. A key like "vault_shared/..." or "research_db/..." is
        # a layering violation and is rejected.
        with pytest.raises(VaultCrossOrgAccess):
            research_db_read(
                key="vault_shared/research_db/entry_01.json",
                session_id="s",
                slug="demo",
                broker=broker,
            )

    def test_research_db_prefix_rejected(self, broker: FDBroker) -> None:
        with pytest.raises(VaultCrossOrgAccess):
            research_db_read(
                key="research_db/entry_01.json",
                session_id="s",
                slug="demo",
                broker=broker,
            )


# ---------------------------------------------------------------------------
# Missing entry surfaces as VaultAccessDenied (same as vault_read)
# ---------------------------------------------------------------------------


class TestDenials:
    def test_missing_entry_raises(self, broker: FDBroker) -> None:
        with pytest.raises(VaultAccessDenied):
            research_db_read(
                key="no_such_entry.json",
                session_id="s",
                slug="demo",
                broker=broker,
            )


# ---------------------------------------------------------------------------
# E-001 arg-type gates
# ---------------------------------------------------------------------------


class TestArgTypes:
    def test_key_must_be_str(self, broker: FDBroker) -> None:
        with pytest.raises(TypeError):
            research_db_read(
                key=123,  # type: ignore[arg-type]
                session_id="s",
                slug="demo",
                broker=broker,
            )

    def test_empty_key_rejected(self, broker: FDBroker) -> None:
        with pytest.raises(ValueError):
            research_db_read(
                key="",
                session_id="s",
                slug="demo",
                broker=broker,
            )

    def test_session_id_must_be_str(self, broker: FDBroker) -> None:
        with pytest.raises(TypeError):
            research_db_read(
                key="entry_01.json",
                session_id=123,  # type: ignore[arg-type]
                slug="demo",
                broker=broker,
            )

    def test_broker_must_be_fdbroker(self) -> None:
        with pytest.raises(TypeError):
            research_db_read(
                key="entry_01.json",
                session_id="s",
                slug="demo",
                broker="not a broker",  # type: ignore[arg-type]
            )


class TestBlueprintDepsPin:
    def test_blueprint_deps_pin(self) -> None:
        from pipeline.vault import research_db_query_skill as _mod

        deps = _mod.BLUEPRINT_DEPS
        assert "section_02_vault_topology.md" in deps
        section = deps["section_02_vault_topology.md"]
        assert section["version"] == "v7.1"
        assert section["hash_sha3_512_prefix16"] == "83a898275a4cf0a1"
