"""Unit tests for pipeline.vault.vault_query_skill (§3.3 + §2.9).

Round Q' — Vault-owned first-class read skill. Thin consumer of
:class:`pipeline.vault.fd_broker.FDBroker`.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Iterator

import pytest

from pipeline.vault.error_codes import VaultAccessDenied
from pipeline.vault.fd_broker import FDBroker
from pipeline.vault.gate_and_open import open_vault_root
from pipeline.vault.vault_query_skill import vault_read


@pytest.fixture
def vault_tree(tmp_path: Path) -> Path:
    vault_root = tmp_path / "vault_root"
    vault_root.mkdir()
    (vault_root / "orgs" / "demo" / "vault").mkdir(parents=True)
    (vault_root / "orgs" / "demo" / "vault" / "sample.txt").write_bytes(
        b"hello research"
    )
    # Larger file to cover multi-chunk reads.
    (vault_root / "orgs" / "demo" / "vault" / "big.bin").write_bytes(
        b"X" * (65_536 * 3 + 123)
    )
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
    def test_returns_bytes_and_identity(self, broker: FDBroker) -> None:
        data, identity = vault_read(
            path="orgs/demo/vault/sample.txt",
            session_id="sess-1",
            slug="demo",
            broker=broker,
        )
        assert data == b"hello research"
        assert identity.volume_uuid
        assert identity.fs_type != "denied"

    def test_reads_full_content_beyond_one_buffer(
        self, broker: FDBroker
    ) -> None:
        data, _ = vault_read(
            path="orgs/demo/vault/big.bin",
            session_id="sess-2",
            slug="demo",
            broker=broker,
        )
        assert len(data) == 65_536 * 3 + 123
        assert data == b"X" * len(data)

    def test_two_calls_use_distinct_nonces(self, broker: FDBroker) -> None:
        vault_read(
            path="orgs/demo/vault/sample.txt",
            session_id="sess-3",
            slug="demo",
            broker=broker,
        )
        # Second call must succeed (fresh nonce each call).
        vault_read(
            path="orgs/demo/vault/sample.txt",
            session_id="sess-3",
            slug="demo",
            broker=broker,
        )


# ---------------------------------------------------------------------------
# Denials surface as exceptions
# ---------------------------------------------------------------------------


class TestDenials:
    def test_missing_file_raises(self, broker: FDBroker) -> None:
        with pytest.raises(VaultAccessDenied):
            vault_read(
                path="orgs/demo/vault/missing.txt",
                session_id="sess-4",
                slug="demo",
                broker=broker,
            )

    def test_post_gate_veto_raises(self, broker: FDBroker) -> None:
        broker.register_post_gate(lambda req: False)
        with pytest.raises(VaultAccessDenied):
            vault_read(
                path="orgs/demo/vault/sample.txt",
                session_id="sess-5",
                slug="demo",
                broker=broker,
            )

    def test_path_escape_raises(self, broker: FDBroker) -> None:
        with pytest.raises(VaultAccessDenied):
            vault_read(
                path="../../etc/passwd",
                session_id="sess-6",
                slug="demo",
                broker=broker,
            )


# ---------------------------------------------------------------------------
# E-001 arg-type gates
# ---------------------------------------------------------------------------


class TestArgTypes:
    def test_path_must_be_str(self, broker: FDBroker) -> None:
        with pytest.raises(TypeError):
            vault_read(
                path=123,  # type: ignore[arg-type]
                session_id="s",
                slug="demo",
                broker=broker,
            )

    def test_session_id_must_be_str(self, broker: FDBroker) -> None:
        with pytest.raises(TypeError):
            vault_read(
                path="orgs/demo/vault/sample.txt",
                session_id=None,  # type: ignore[arg-type]
                slug="demo",
                broker=broker,
            )

    def test_slug_must_be_str(self, broker: FDBroker) -> None:
        with pytest.raises(TypeError):
            vault_read(
                path="orgs/demo/vault/sample.txt",
                session_id="s",
                slug=None,  # type: ignore[arg-type]
                broker=broker,
            )

    def test_broker_must_be_fdbroker(self) -> None:
        with pytest.raises(TypeError):
            vault_read(
                path="orgs/demo/vault/sample.txt",
                session_id="s",
                slug="demo",
                broker="not a broker",  # type: ignore[arg-type]
            )

    def test_empty_path_raises(self, broker: FDBroker) -> None:
        with pytest.raises(ValueError):
            vault_read(
                path="",
                session_id="s",
                slug="demo",
                broker=broker,
            )


class TestBlueprintDepsPin:
    def test_blueprint_deps_pin(self) -> None:
        from pipeline.vault import vault_query_skill as _mod

        deps = _mod.BLUEPRINT_DEPS
        assert "section_02_vault_topology.md" in deps
        section = deps["section_02_vault_topology.md"]
        assert section["version"] == "v7.1"
        assert section["hash_sha3_512_prefix16"] == "83a898275a4cf0a1"
