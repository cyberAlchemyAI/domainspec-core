"""Unit tests for pipeline.vault.fd_broker (§2.7 + §2.9 + §3.4).

Round Q — Vault-owned-skill FD issuance broker (v0.1 scope).

v0.1 scope covered:
* Hard-coded two-skill allowlist (vault-query, research-db-query).
* Per-request nonce registry (in-process) with TTL pruning.
* Default-allow Cedar stub that mints a synthetic decision_id.
* Logician post-gate hook registration + veto.
* open via gate_and_open; identity_tuple capture; FD returned to caller.

v0.1 deferred (explicitly out-of-scope for this round):
* SCM_RIGHTS FD passing over Unix domain sockets.
* Cedar policy loader + signed-manifest enforcement.
* Seccomp filter install + sandbox-profile binding.
* Wrapper-hash re-verify at exec-time.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Iterator

import pytest

from pipeline.vault.error_codes import F_FD_01, F_FD_02, F_FD_03
from pipeline.vault.fd_broker import (
    FD_BROKER_ALLOWED_INTENTS,
    FD_BROKER_ALLOWED_SKILLS,
    NONCE_TTL_SECONDS,
    FDBroker,
    FdBrokerCedarVeto,
    FdBrokerNonceReplayed,
    FdBrokerPostGateVeto,
    FdBrokerUnknownSkill,
)
from pipeline.vault.gate_and_open import open_vault_root
from pipeline.vault.schemas import FDBrokerRequest


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def vault_tree(tmp_path: Path) -> Path:
    """A minimal vault-rooted tree with one readable file."""
    vault_root = tmp_path / "vault_root"
    vault_root.mkdir()
    orgs = vault_root / "orgs" / "demo" / "vault"
    orgs.mkdir(parents=True)
    (orgs / "sample.txt").write_bytes(b"hello vault")
    return vault_root


@pytest.fixture
def broker(vault_tree: Path) -> Iterator[FDBroker]:
    root_fd = open_vault_root(vault_tree)
    try:
        yield FDBroker(vault_root_fd=root_fd, vault_root_path=vault_tree)
    finally:
        os.close(root_fd)


def _request(
    *,
    requester_skill: str = "vault-query",
    requester_pid: int = os.getpid(),
    requester_session_id: str = "sess-1",
    requester_org_slug: str = "demo",
    requested_path: str = "orgs/demo/vault/sample.txt",
    intent: str = "read",
    nonce_hex: str = "a" * 64,
) -> FDBrokerRequest:
    return FDBrokerRequest(
        requester_skill=requester_skill,
        requester_pid=requester_pid,
        requester_session_id=requester_session_id,
        requester_org_slug=requester_org_slug,
        requested_path=requested_path,
        intent=intent,
        nonce_hex=nonce_hex,
    )


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------


class TestConstants:
    def test_allowlist_is_exactly_two_skills(self) -> None:
        assert FD_BROKER_ALLOWED_SKILLS == frozenset(
            {"vault-query", "research-db-query"}
        )

    def test_intents_cover_v0_1_surface(self) -> None:
        assert FD_BROKER_ALLOWED_INTENTS == frozenset(
            {"read", "write", "execute", "read-wrapper"}
        )

    def test_nonce_ttl_positive(self) -> None:
        assert NONCE_TTL_SECONDS > 0


# ---------------------------------------------------------------------------
# Construction + arg-type gates (E-001)
# ---------------------------------------------------------------------------


class TestConstruction:
    def test_accepts_valid_args(self, vault_tree: Path) -> None:
        root_fd = open_vault_root(vault_tree)
        try:
            broker = FDBroker(vault_root_fd=root_fd, vault_root_path=vault_tree)
            assert isinstance(broker, FDBroker)
        finally:
            os.close(root_fd)

    def test_rejects_non_int_root_fd(self, vault_tree: Path) -> None:
        with pytest.raises(TypeError):
            FDBroker(vault_root_fd="0", vault_root_path=vault_tree)  # type: ignore[arg-type]

    def test_rejects_non_path_root(self, vault_tree: Path) -> None:
        root_fd = open_vault_root(vault_tree)
        try:
            with pytest.raises(TypeError):
                FDBroker(vault_root_fd=root_fd, vault_root_path=str(vault_tree))  # type: ignore[arg-type]
        finally:
            os.close(root_fd)

    def test_rejects_non_callable_hook(self, vault_tree: Path) -> None:
        root_fd = open_vault_root(vault_tree)
        try:
            with pytest.raises(TypeError):
                FDBroker(
                    vault_root_fd=root_fd,
                    vault_root_path=vault_tree,
                    post_gate_hook="not callable",  # type: ignore[arg-type]
                )
        finally:
            os.close(root_fd)


# ---------------------------------------------------------------------------
# Allowlist
# ---------------------------------------------------------------------------


class TestAllowlist:
    def test_vault_query_accepted(self, broker: FDBroker) -> None:
        resp, fd = broker.request_fd(_request(requester_skill="vault-query"))
        assert resp.granted is True
        assert fd is not None
        broker.release_fd(fd)

    def test_research_db_query_accepted(self, broker: FDBroker) -> None:
        resp, fd = broker.request_fd(
            _request(
                requester_skill="research-db-query", nonce_hex="b" * 64
            )
        )
        assert resp.granted is True
        assert fd is not None
        broker.release_fd(fd)

    def test_vault_write_rejected(self, broker: FDBroker) -> None:
        resp, fd = broker.request_fd(
            _request(requester_skill="vault-write", nonce_hex="c" * 64)
        )
        assert resp.granted is False
        assert resp.fd_count == 0
        assert fd is None
        assert "unknown-skill" in resp.denial_reason

    def test_unknown_skill_rejected(self, broker: FDBroker) -> None:
        resp, fd = broker.request_fd(
            _request(requester_skill="scout", nonce_hex="d" * 64)
        )
        assert resp.granted is False
        assert fd is None
        assert "unknown-skill" in resp.denial_reason


# ---------------------------------------------------------------------------
# Intent validation
# ---------------------------------------------------------------------------


class TestIntent:
    def test_read_accepted(self, broker: FDBroker) -> None:
        resp, fd = broker.request_fd(_request(intent="read"))
        assert resp.granted is True
        broker.release_fd(fd)  # type: ignore[arg-type]

    def test_write_accepted_for_allowed_skill(self, broker: FDBroker) -> None:
        resp, fd = broker.request_fd(
            _request(intent="write", nonce_hex="e" * 64)
        )
        assert resp.granted is True
        broker.release_fd(fd)  # type: ignore[arg-type]

    def test_invalid_intent_rejected(self, broker: FDBroker) -> None:
        resp, fd = broker.request_fd(
            _request(intent="delete", nonce_hex="f" * 64)
        )
        assert resp.granted is False
        assert "invalid-intent" in resp.denial_reason


# ---------------------------------------------------------------------------
# Nonce replay
# ---------------------------------------------------------------------------


class TestNonceReplay:
    def test_same_nonce_twice_second_rejected(
        self, broker: FDBroker
    ) -> None:
        req = _request(nonce_hex="1" * 64)
        resp1, fd1 = broker.request_fd(req)
        assert resp1.granted is True
        broker.release_fd(fd1)  # type: ignore[arg-type]

        req2 = _request(nonce_hex="1" * 64)  # same nonce
        resp2, fd2 = broker.request_fd(req2)
        assert resp2.granted is False
        assert fd2 is None
        assert "nonce-replay" in resp2.denial_reason

    def test_different_nonces_both_accepted(self, broker: FDBroker) -> None:
        resp1, fd1 = broker.request_fd(_request(nonce_hex="2" * 64))
        resp2, fd2 = broker.request_fd(_request(nonce_hex="3" * 64))
        assert resp1.granted is True
        assert resp2.granted is True
        broker.release_fd(fd1)  # type: ignore[arg-type]
        broker.release_fd(fd2)  # type: ignore[arg-type]

    def test_nonce_prune_after_ttl(self, vault_tree: Path) -> None:
        clock = {"t": 1000.0}
        root_fd = open_vault_root(vault_tree)
        try:
            broker = FDBroker(
                vault_root_fd=root_fd,
                vault_root_path=vault_tree,
                clock=lambda: clock["t"],
            )
            resp1, fd1 = broker.request_fd(_request(nonce_hex="4" * 64))
            assert resp1.granted is True
            broker.release_fd(fd1)  # type: ignore[arg-type]

            # advance clock past TTL
            clock["t"] += NONCE_TTL_SECONDS + 1.0

            # same nonce is reusable after TTL — the old record was pruned
            resp2, fd2 = broker.request_fd(_request(nonce_hex="4" * 64))
            assert resp2.granted is True, resp2.denial_reason
            broker.release_fd(fd2)  # type: ignore[arg-type]
        finally:
            os.close(root_fd)


# ---------------------------------------------------------------------------
# Post-gate hook
# ---------------------------------------------------------------------------


class TestPostGate:
    def test_no_hook_is_allow(self, broker: FDBroker) -> None:
        resp, fd = broker.request_fd(_request(nonce_hex="5" * 64))
        assert resp.granted is True
        broker.release_fd(fd)  # type: ignore[arg-type]

    def test_hook_returns_true_allows(self, broker: FDBroker) -> None:
        broker.register_post_gate(lambda req: True)
        resp, fd = broker.request_fd(_request(nonce_hex="6" * 64))
        assert resp.granted is True
        broker.release_fd(fd)  # type: ignore[arg-type]

    def test_hook_returns_false_vetoes(self, broker: FDBroker) -> None:
        broker.register_post_gate(lambda req: False)
        resp, fd = broker.request_fd(_request(nonce_hex="7" * 64))
        assert resp.granted is False
        assert fd is None
        assert "post-gate-veto" in resp.denial_reason

    def test_hook_sees_request_payload(self, broker: FDBroker) -> None:
        seen: list[FDBrokerRequest] = []

        def _spy(req: FDBrokerRequest) -> bool:
            seen.append(req)
            return True

        broker.register_post_gate(_spy)
        broker.request_fd(_request(nonce_hex="8" * 64))
        assert len(seen) == 1
        assert seen[0].requester_skill == "vault-query"

    def test_hook_replaced_by_second_register(
        self, broker: FDBroker
    ) -> None:
        broker.register_post_gate(lambda req: False)
        broker.register_post_gate(lambda req: True)
        resp, fd = broker.request_fd(_request(nonce_hex="9" * 64))
        assert resp.granted is True
        broker.release_fd(fd)  # type: ignore[arg-type]

    def test_register_rejects_non_callable(self, broker: FDBroker) -> None:
        with pytest.raises(TypeError):
            broker.register_post_gate("not callable")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Path safety (delegated to gate_and_open, broker surfaces the denial)
# ---------------------------------------------------------------------------


class TestPathSafety:
    def test_path_escape_rejected(self, broker: FDBroker) -> None:
        resp, fd = broker.request_fd(
            _request(requested_path="../../etc/passwd", nonce_hex="a1" * 32)
        )
        assert resp.granted is False
        assert fd is None

    def test_absolute_path_rejected(self, broker: FDBroker) -> None:
        resp, fd = broker.request_fd(
            _request(requested_path="/etc/passwd", nonce_hex="a2" * 32)
        )
        assert resp.granted is False
        assert fd is None

    def test_nonexistent_path_rejected(self, broker: FDBroker) -> None:
        resp, fd = broker.request_fd(
            _request(
                requested_path="orgs/demo/vault/missing.txt",
                nonce_hex="a3" * 32,
            )
        )
        assert resp.granted is False
        assert fd is None


# ---------------------------------------------------------------------------
# Happy path + release
# ---------------------------------------------------------------------------


class TestHappyPath:
    def test_fd_is_readable(self, broker: FDBroker) -> None:
        resp, fd = broker.request_fd(_request(nonce_hex="b1" * 32))
        assert resp.granted is True
        assert fd is not None
        assert resp.fd_count == 1
        data = os.read(fd, 4096)
        assert data == b"hello vault"
        broker.release_fd(fd)

    def test_response_carries_identity_tuple(self, broker: FDBroker) -> None:
        resp, fd = broker.request_fd(_request(nonce_hex="b2" * 32))
        assert resp.granted is True
        assert resp.identity_tuple is not None
        assert resp.identity_tuple.volume_uuid
        broker.release_fd(fd)  # type: ignore[arg-type]

    def test_response_carries_cedar_decision_id(
        self, broker: FDBroker
    ) -> None:
        resp, fd = broker.request_fd(_request(nonce_hex="b3" * 32))
        assert resp.granted is True
        assert resp.cedar_decision_id
        assert len(resp.cedar_decision_id) >= 16
        broker.release_fd(fd)  # type: ignore[arg-type]

    def test_release_fd_closes(self, broker: FDBroker) -> None:
        resp, fd = broker.request_fd(_request(nonce_hex="b4" * 32))
        assert fd is not None
        broker.release_fd(fd)
        # Second close should fail with EBADF
        with pytest.raises(OSError):
            os.fstat(fd)

    def test_release_fd_on_already_closed_is_safe(
        self, broker: FDBroker
    ) -> None:
        resp, fd = broker.request_fd(_request(nonce_hex="b5" * 32))
        assert fd is not None
        os.close(fd)
        # broker.release_fd should not propagate on already-closed
        broker.release_fd(fd)

    def test_release_fd_rejects_non_int(self, broker: FDBroker) -> None:
        with pytest.raises(TypeError):
            broker.release_fd("3")  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# request_fd arg-type gate
# ---------------------------------------------------------------------------


class TestRequestArgTypes:
    def test_request_fd_rejects_non_request_type(
        self, broker: FDBroker
    ) -> None:
        with pytest.raises(TypeError):
            broker.request_fd({"requester_skill": "vault-query"})  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# BLUEPRINT_DEPS pin (F-2..F-5: vault_batch_1_redispatch_2026-04-22)
# ---------------------------------------------------------------------------


class TestBlueprintDepsPin:
    def test_blueprint_deps_pin(self) -> None:
        import importlib
        _mod = importlib.import_module('pipeline.vault.fd_broker')
        deps = _mod.BLUEPRINT_DEPS
        assert "section_02_vault_topology.md" in deps
        section = deps["section_02_vault_topology.md"]
        assert section["version"] == "v7.1"
        assert section["hash_sha3_512_prefix16"] == "83a898275a4cf0a1"
