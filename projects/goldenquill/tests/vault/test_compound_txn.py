"""Unit tests for pipeline.vault.compound_txn (§2.10 + §4.10.5-7 + §7.11).

Round P — Option-B compound-transaction dispatcher.

Covers:
* begin mints token + increments session count + acquires lock.
* stage_write computes data_sha3_512 and produces a new frozen state.
* commit runs integrity check + calls persist hook + releases lock.
* abort releases lock and decrements session count.
* Session-cap enforcement (MAX_ACTIVE_COMPOUND_TXNS_PER_SESSION).
* Size-cap enforcement (MAX_COMPOUND_TXN_BYTES).
* Unknown txn_kind rejected.
* Unknown token rejected.
* Cross-session token rejected.
* Double-abort rejected.
* Frozen-record immutability (tuple staged_writes, StagedWrite.data bytes).
* Integrity check catches forged record.
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path

import pytest

from dataclasses import replace

from pipeline.vault import compound_txn as _compound_txn_mod
from pipeline.vault.compound_txn import (
    COMPOUND_TXN_KINDS,
    COMPOUND_TXN_TTL_SECONDS,
    MAX_ACTIVE_COMPOUND_TXNS_PER_SESSION,
    MAX_COMPOUND_TXN_BYTES,
    MAX_STAGED_BYTES_PER_TXN,
    MAX_STAGED_WRITES_PER_TXN,
    TXN_TOKEN_ENTROPY_BYTES,
    CompoundTxnDispatcher,
)
from pipeline.vault.error_codes import (
    VaultCompoundCapExceeded,
    VaultCompoundIntegrityError,
    VaultCompoundOversize,
    VaultCompoundProtocolViolation,
)
from pipeline.vault.schemas import CompoundTxnState, StagedWrite


@pytest.fixture
def dispatcher(tmp_path: Path) -> CompoundTxnDispatcher:
    return CompoundTxnDispatcher(
        compound_lock_path=tmp_path / ".compound.lock"
    )


def _noop_persist(state: CompoundTxnState) -> None:
    return None


# ---------------------------------------------------------------------------
# begin
# ---------------------------------------------------------------------------


class TestBegin:
    def test_begin_mints_token(self, dispatcher) -> None:
        token = dispatcher.begin(txn_kind="index-update", session_id="s1")
        assert isinstance(token, str)
        assert len(token) > 0
        dispatcher.abort(txn_token=token, session_id="s1", reason="test")

    def test_unknown_kind_rejected(self, dispatcher) -> None:
        with pytest.raises(VaultCompoundProtocolViolation):
            dispatcher.begin(txn_kind="bogus", session_id="s1")

    def test_session_cap_enforced(self, dispatcher) -> None:
        tokens = []
        for _ in range(MAX_ACTIVE_COMPOUND_TXNS_PER_SESSION):
            tokens.append(
                dispatcher.begin(txn_kind="index-update", session_id="s1")
            )
        with pytest.raises(VaultCompoundCapExceeded):
            dispatcher.begin(txn_kind="index-update", session_id="s1")
        for t in tokens:
            dispatcher.abort(txn_token=t, session_id="s1", reason="t")

    def test_distinct_sessions_isolated(self, dispatcher) -> None:
        t1 = dispatcher.begin(txn_kind="index-update", session_id="s1")
        t2 = dispatcher.begin(txn_kind="index-update", session_id="s2")
        assert t1 != t2
        dispatcher.abort(txn_token=t1, session_id="s1", reason="t")
        dispatcher.abort(txn_token=t2, session_id="s2", reason="t")

    def test_known_kinds_exact(self) -> None:
        assert COMPOUND_TXN_KINDS == frozenset(
            {"index-update", "index-amendment-audit-append"}
        )


# ---------------------------------------------------------------------------
# stage + commit
# ---------------------------------------------------------------------------


class TestStageCommit:
    def test_stage_pins_data_hash(self, dispatcher) -> None:
        token = dispatcher.begin(txn_kind="index-update", session_id="s1")
        dispatcher.stage_write(
            txn_token=token,
            session_id="s1",
            intent="index-update",
            path="orgs/myco/vault/index.json",
            data=b'{"k":1}',
        )
        committed = dispatcher.commit(
            txn_token=token, session_id="s1", persist=_noop_persist
        )
        assert len(committed) == 1
        sw = committed[0]
        assert sw.data_sha3_512 == hashlib.sha3_512(b'{"k":1}').hexdigest()

    def test_commit_calls_persist_once(self, dispatcher) -> None:
        token = dispatcher.begin(txn_kind="index-update", session_id="s1")
        dispatcher.stage_write(
            txn_token=token,
            session_id="s1",
            intent="index-update",
            path="p",
            data=b"x",
        )
        calls: list[CompoundTxnState] = []
        dispatcher.commit(
            txn_token=token,
            session_id="s1",
            persist=lambda s: calls.append(s),
        )
        assert len(calls) == 1
        assert calls[0].staged_writes[0].data == b"x"

    def test_persist_failure_aborts(self, dispatcher) -> None:
        token = dispatcher.begin(txn_kind="index-update", session_id="s1")
        dispatcher.stage_write(
            txn_token=token,
            session_id="s1",
            intent="index-update",
            path="p",
            data=b"x",
        )

        def boom(_state):
            raise RuntimeError("persist failed")

        with pytest.raises(RuntimeError):
            dispatcher.commit(
                txn_token=token, session_id="s1", persist=boom
            )
        # Txn should be torn down after the failure.
        with pytest.raises(VaultCompoundProtocolViolation):
            dispatcher.abort(txn_token=token, session_id="s1", reason="t")

    def test_staged_bytes_cap_enforced(
        self, dispatcher, monkeypatch
    ) -> None:
        # Monkey-patch the 128 MiB cap to 1024 to keep RAM bounded while
        # still exercising the stage-time VaultCompoundCapExceeded path.
        monkeypatch.setattr(_compound_txn_mod, "MAX_STAGED_BYTES_PER_TXN", 1024)
        token = dispatcher.begin(txn_kind="index-update", session_id="s1")
        big = b"x" * 1025
        with pytest.raises(VaultCompoundCapExceeded):
            dispatcher.stage_write(
                txn_token=token,
                session_id="s1",
                intent="index-update",
                path="p",
                data=big,
            )
        dispatcher.abort(txn_token=token, session_id="s1", reason="t")

    def test_staged_writes_count_cap_enforced(self, dispatcher) -> None:
        token = dispatcher.begin(txn_kind="index-update", session_id="s1")
        # §8 MAX_STAGED_WRITES_PER_TXN = 8: first 8 stages succeed, 9th denies.
        for i in range(MAX_STAGED_WRITES_PER_TXN):
            dispatcher.stage_write(
                txn_token=token,
                session_id="s1",
                intent="index-update",
                path=f"p{i}",
                data=b"x",
            )
        with pytest.raises(VaultCompoundCapExceeded):
            dispatcher.stage_write(
                txn_token=token,
                session_id="s1",
                intent="index-update",
                path="p_overflow",
                data=b"x",
            )
        dispatcher.abort(txn_token=token, session_id="s1", reason="t")

    def test_pre_commit_bytes_cap_enforced(
        self, dispatcher, monkeypatch
    ) -> None:
        # Monkey-patch the 64 MiB undo-snapshot cap to 1024 for RAM-safe test.
        monkeypatch.setattr(_compound_txn_mod, "MAX_COMPOUND_TXN_BYTES", 1024)
        token = dispatcher.begin(txn_kind="index-update", session_id="s1")
        dispatcher.stage_write(
            txn_token=token,
            session_id="s1",
            intent="index-update",
            path="p",
            data=b"x",
        )
        # Section 5's snapshot path populates pre_commit_bytes via
        # ``replace()`` prior to commit. Forge an over-cap snapshot.
        st = dispatcher._active[token]
        dispatcher._active[token] = replace(
            st, pre_commit_bytes=(("p", b"y" * 1025),)
        )
        with pytest.raises(VaultCompoundOversize):
            dispatcher.commit(
                txn_token=token, session_id="s1", persist=_noop_persist
            )

    def test_multiple_stage_accumulate(self, dispatcher) -> None:
        token = dispatcher.begin(txn_kind="index-update", session_id="s1")
        dispatcher.stage_write(
            txn_token=token,
            session_id="s1",
            intent="a",
            path="p1",
            data=b"a",
        )
        dispatcher.stage_write(
            txn_token=token,
            session_id="s1",
            intent="b",
            path="p2",
            data=b"bb",
        )
        committed = dispatcher.commit(
            txn_token=token, session_id="s1", persist=_noop_persist
        )
        assert len(committed) == 2


# ---------------------------------------------------------------------------
# abort / protocol
# ---------------------------------------------------------------------------


class TestAbort:
    def test_abort_releases_session_slot(self, dispatcher) -> None:
        token = dispatcher.begin(txn_kind="index-update", session_id="s1")
        dispatcher.abort(txn_token=token, session_id="s1", reason="t")
        # Should be able to open a new txn in the same session immediately.
        token2 = dispatcher.begin(txn_kind="index-update", session_id="s1")
        dispatcher.abort(txn_token=token2, session_id="s1", reason="t")

    def test_double_abort_rejected(self, dispatcher) -> None:
        token = dispatcher.begin(txn_kind="index-update", session_id="s1")
        dispatcher.abort(txn_token=token, session_id="s1", reason="t")
        with pytest.raises(VaultCompoundProtocolViolation):
            dispatcher.abort(txn_token=token, session_id="s1", reason="t")

    def test_unknown_token_rejected(self, dispatcher) -> None:
        with pytest.raises(VaultCompoundProtocolViolation):
            dispatcher.commit(
                txn_token="fake", session_id="s1", persist=_noop_persist
            )

    def test_wrong_session_rejected(self, dispatcher) -> None:
        token = dispatcher.begin(txn_kind="index-update", session_id="s1")
        with pytest.raises(VaultCompoundProtocolViolation):
            dispatcher.commit(
                txn_token=token, session_id="other", persist=_noop_persist
            )
        dispatcher.abort(txn_token=token, session_id="s1", reason="t")


# ---------------------------------------------------------------------------
# Frozen-record integrity
# ---------------------------------------------------------------------------


class TestIntegrity:
    def test_staged_writes_is_tuple(self, dispatcher) -> None:
        token = dispatcher.begin(txn_kind="index-update", session_id="s1")
        dispatcher.stage_write(
            txn_token=token,
            session_id="s1",
            intent="i",
            path="p",
            data=b"x",
        )
        committed = dispatcher.commit(
            txn_token=token, session_id="s1", persist=_noop_persist
        )
        assert isinstance(committed, tuple)

    def test_frozen_dataclass_rejects_mutation(self) -> None:
        sw = StagedWrite(
            intent="i",
            path="p",
            data=b"x",
            data_sha3_512="0" * 128,
            data_len=1,
            expected_current_file_hash=None,
            write_mode="overwrite",
            staged_at_monotonic_ns=0,
        )
        with pytest.raises(Exception):
            sw.data = b"y"  # type: ignore[misc]

    def test_integrity_catches_forged_record(self, dispatcher) -> None:
        # Fabricate an active txn whose staged-write has a mismatched hash.
        class Forged:
            __name__ = "StagedWrite"
            data = b"attacker"
            data_sha3_512 = "0" * 128
            data_len = 8

        token = dispatcher.begin(txn_kind="index-update", session_id="s1")
        real_state = dispatcher._active[token]
        forged_state = CompoundTxnState(
            txn_kind=real_state.txn_kind,
            txn_token=real_state.txn_token,
            session_id=real_state.session_id,
            created_at_monotonic_ns=real_state.created_at_monotonic_ns,
            staged_writes=(
                StagedWrite(
                    intent="i",
                    path="p",
                    data=b"real",
                    data_sha3_512="0" * 128,  # wrong hash
                    data_len=4,
                    expected_current_file_hash=None,
                    write_mode="overwrite",
                    staged_at_monotonic_ns=0,
                ),
            ),
            pre_commit_bytes=(),
        )
        dispatcher._active[token] = forged_state
        with pytest.raises(VaultCompoundIntegrityError):
            dispatcher.commit(
                txn_token=token, session_id="s1", persist=_noop_persist
            )


# ---------------------------------------------------------------------------
# Arg-type
# ---------------------------------------------------------------------------


class TestArgTypes:
    def test_compound_lock_path_must_be_path(self) -> None:
        with pytest.raises(TypeError):
            CompoundTxnDispatcher(compound_lock_path="/tmp/x")  # type: ignore[arg-type]

    def test_begin_rejects_non_str(self, dispatcher) -> None:
        with pytest.raises(TypeError):
            dispatcher.begin(txn_kind=None, session_id="s")  # type: ignore[arg-type]


class TestConstantPins:
    """§8 v7.1 pins — remediation-cycle-1 correcting pre-remediation drift.

    Pre-remediation values were `MAX_ACTIVE=8`, `MAX_COMPOUND_TXN_BYTES=8 MiB`,
    `TTL=60s`, and both `MAX_STAGED_*_PER_TXN` constants were absent entirely.
    This test pins the corrected values so any silent regression is loud.
    """

    def test_max_active_is_one(self) -> None:
        assert MAX_ACTIVE_COMPOUND_TXNS_PER_SESSION == 1

    def test_max_staged_bytes_is_128_mib(self) -> None:
        assert MAX_STAGED_BYTES_PER_TXN == 134_217_728

    def test_max_staged_writes_is_eight(self) -> None:
        assert MAX_STAGED_WRITES_PER_TXN == 8

    def test_max_compound_txn_bytes_is_64_mib(self) -> None:
        assert MAX_COMPOUND_TXN_BYTES == 67_108_864

    def test_ttl_is_ten_minutes(self) -> None:
        assert COMPOUND_TXN_TTL_SECONDS == 600

    def test_token_entropy_is_32_bytes(self) -> None:
        assert TXN_TOKEN_ENTROPY_BYTES == 32


class TestBlueprintDepsPin:
    def test_blueprint_deps_pin(self) -> None:
        from pipeline.vault import compound_txn as _mod

        deps = _mod.BLUEPRINT_DEPS
        assert "section_02_vault_topology.md" in deps
        section = deps["section_02_vault_topology.md"]
        assert section["version"] == "v7.1"
        assert section["hash_sha3_512_prefix16"] == "83a898275a4cf0a1"
