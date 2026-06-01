"""Unit tests for pipeline.sovereignty.boot_clock.

Section 1 Round I. Covers §4.8 v4 + §9 step 2.5 + §6.5 F-ADM-09 + §7.14
named tests.

Named tests per §7.14:

* ``test_boot_clock_history_first_boot_empty``
* ``test_append_single_entry_chain_genesis``
* ``test_append_multiple_entries_chain_walk``
* ``test_idempotent_same_boot_epoch_ns``
* ``test_rollback_past_tolerance_rejected`` — F-ADM-09
* ``test_trailer_missing_on_nonempty_jsonl_rejected`` — F-ADM-09
* ``test_tampered_entry_detected`` — F-ADM-09
* ``test_tampered_trailer_detected`` — F-ADM-09
"""

from __future__ import annotations

import json
import platform
from pathlib import Path

import pytest

from pipeline.sovereignty.admin_risk import BootClockRecord
from pipeline.sovereignty.boot_clock import (
    BootClockHistoryCorrupt,
    BootClockHistoryEntry,
    BootClockHistoryRollback,
    BootClockHistoryTrailerMismatch,
    BootClockHistoryTrailerMissing,
    BootEpochUnavailable,
    append_boot_clock_record,
    read_boot_clock_history,
    read_boot_epoch_ns,
    verify_boot_clock_history_chain,
)
from pipeline.sovereignty.keys import KeyStore

_HMAC_KEY = b"\xcd" * 32


class _StubKeyStore(KeyStore):
    def __init__(self, *, key_bytes: bytes = _HMAC_KEY) -> None:
        self._key = key_bytes

    def _retrieve_raw(self, key_id: str) -> bytearray:
        return bytearray(self._key)

    def store(self, *, key_id: str, key_bytes, purpose: str) -> None:
        raise NotImplementedError

    def rotate(self, key_id: str) -> str:
        raise NotImplementedError

    def zero(self, key_id: str) -> None:
        raise NotImplementedError

    def exists(self, key_id: str) -> bool:
        return True

    def provider(self) -> str:
        return "stub"


def _rec(boot_epoch_ns: int, wall_at_boot_utc: str) -> BootClockRecord:
    return BootClockRecord(
        boot_epoch_ns=boot_epoch_ns, wall_at_boot_utc=wall_at_boot_utc
    )


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    return tmp_path


# ---------------------------------------------------------------------------
# Verify / read
# ---------------------------------------------------------------------------


class TestFirstBoot:
    def test_boot_clock_history_first_boot_empty(self, repo: Path) -> None:
        entries = verify_boot_clock_history_chain(
            repo_root=repo, keystore=_StubKeyStore()
        )
        assert entries == []

    def test_read_returns_empty_on_missing(self, repo: Path) -> None:
        assert read_boot_clock_history(repo) == []


class TestAppend:
    def test_append_single_entry_chain_genesis(self, repo: Path) -> None:
        entry = append_boot_clock_record(
            repo_root=repo,
            record=_rec(1_700_000_000_000_000_000, "2026-04-19T00:00:00Z"),
            keystore=_StubKeyStore(),
        )
        assert isinstance(entry, BootClockHistoryEntry)
        assert entry.prev_hash == "0" * 128
        assert entry.boot_epoch_ns == 1_700_000_000_000_000_000
        entries = verify_boot_clock_history_chain(
            repo_root=repo, keystore=_StubKeyStore()
        )
        assert len(entries) == 1
        assert entries[0].entry_hash == entry.entry_hash

    def test_append_multiple_entries_chain_walk(self, repo: Path) -> None:
        e1 = append_boot_clock_record(
            repo_root=repo,
            record=_rec(1, "2026-04-19T00:00:00Z"),
            keystore=_StubKeyStore(),
        )
        e2 = append_boot_clock_record(
            repo_root=repo,
            record=_rec(2, "2026-04-19T01:00:00Z"),
            keystore=_StubKeyStore(),
        )
        e3 = append_boot_clock_record(
            repo_root=repo,
            record=_rec(3, "2026-04-19T02:00:00Z"),
            keystore=_StubKeyStore(),
        )
        assert e1.prev_hash == "0" * 128
        assert e2.prev_hash == e1.entry_hash
        assert e3.prev_hash == e2.entry_hash
        entries = verify_boot_clock_history_chain(
            repo_root=repo, keystore=_StubKeyStore()
        )
        assert [e.boot_epoch_ns for e in entries] == [1, 2, 3]

    def test_idempotent_same_boot_epoch_ns(self, repo: Path) -> None:
        e1 = append_boot_clock_record(
            repo_root=repo,
            record=_rec(42, "2026-04-19T00:00:00Z"),
            keystore=_StubKeyStore(),
        )
        e2 = append_boot_clock_record(
            repo_root=repo,
            record=_rec(42, "2026-04-19T00:00:05Z"),  # wall differs; epoch same
            keystore=_StubKeyStore(),
        )
        assert e1 == e2
        entries = verify_boot_clock_history_chain(
            repo_root=repo, keystore=_StubKeyStore()
        )
        assert len(entries) == 1

    def test_rollback_past_tolerance_rejected(self, repo: Path) -> None:
        append_boot_clock_record(
            repo_root=repo,
            record=_rec(1, "2026-04-19T12:00:00Z"),
            keystore=_StubKeyStore(),
        )
        with pytest.raises(BootClockHistoryRollback) as exc:
            append_boot_clock_record(
                repo_root=repo,
                record=_rec(2, "2026-04-19T11:00:00Z"),  # -3600s, way past 300s
                keystore=_StubKeyStore(),
            )
        assert exc.value.code == "F-ADM-09"

    def test_rollback_within_tolerance_accepted(self, repo: Path) -> None:
        append_boot_clock_record(
            repo_root=repo,
            record=_rec(1, "2026-04-19T12:00:00Z"),
            keystore=_StubKeyStore(),
        )
        # 60s regression < 300s tolerance
        append_boot_clock_record(
            repo_root=repo,
            record=_rec(2, "2026-04-19T11:59:00Z"),
            keystore=_StubKeyStore(),
        )


# ---------------------------------------------------------------------------
# Fail-closed outcomes
# ---------------------------------------------------------------------------


class TestFailClosed:
    def test_trailer_missing_on_nonempty_jsonl_rejected(self, repo: Path) -> None:
        append_boot_clock_record(
            repo_root=repo,
            record=_rec(1, "2026-04-19T00:00:00Z"),
            keystore=_StubKeyStore(),
        )
        (repo / "sovereignty" / "clock" / "boot_clock_history.hmac").unlink()
        with pytest.raises(BootClockHistoryTrailerMissing) as exc:
            verify_boot_clock_history_chain(
                repo_root=repo, keystore=_StubKeyStore()
            )
        assert exc.value.code == "F-ADM-09"

    def test_trailer_without_jsonl_rejected(self, repo: Path) -> None:
        clock_dir = repo / "sovereignty" / "clock"
        clock_dir.mkdir(parents=True, exist_ok=True)
        (clock_dir / "boot_clock_history.hmac").write_bytes(b'{"x": 1}')
        with pytest.raises(BootClockHistoryTrailerMismatch):
            verify_boot_clock_history_chain(
                repo_root=repo, keystore=_StubKeyStore()
            )

    def test_tampered_entry_detected(self, repo: Path) -> None:
        append_boot_clock_record(
            repo_root=repo,
            record=_rec(1, "2026-04-19T00:00:00Z"),
            keystore=_StubKeyStore(),
        )
        jsonl = repo / "sovereignty" / "clock" / "boot_clock_history.jsonl"
        lines = jsonl.read_bytes().splitlines()
        obj = json.loads(lines[0])
        obj["boot_epoch_ns"] = 99  # body flip
        lines[0] = json.dumps(obj).encode("utf-8")
        jsonl.write_bytes(b"\n".join(lines) + b"\n")
        with pytest.raises(
            (BootClockHistoryCorrupt, BootClockHistoryTrailerMismatch)
        ) as exc:
            verify_boot_clock_history_chain(
                repo_root=repo, keystore=_StubKeyStore()
            )
        assert exc.value.code == "F-ADM-09"

    def test_tampered_trailer_detected(self, repo: Path) -> None:
        append_boot_clock_record(
            repo_root=repo,
            record=_rec(1, "2026-04-19T00:00:00Z"),
            keystore=_StubKeyStore(),
        )
        trailer = repo / "sovereignty" / "clock" / "boot_clock_history.hmac"
        obj = json.loads(trailer.read_bytes())
        obj["boot_clock_history_hmac"] = "0" * 128
        trailer.write_bytes(json.dumps(obj).encode("utf-8"))
        with pytest.raises(BootClockHistoryTrailerMismatch):
            verify_boot_clock_history_chain(
                repo_root=repo, keystore=_StubKeyStore()
            )

    def test_different_key_fails_verify(self, repo: Path) -> None:
        append_boot_clock_record(
            repo_root=repo,
            record=_rec(1, "2026-04-19T00:00:00Z"),
            keystore=_StubKeyStore(key_bytes=b"\x11" * 32),
        )
        with pytest.raises(BootClockHistoryTrailerMismatch):
            verify_boot_clock_history_chain(
                repo_root=repo, keystore=_StubKeyStore(key_bytes=b"\x22" * 32)
            )

    def test_trailer_last_seq_mismatch_detected(self, repo: Path) -> None:
        append_boot_clock_record(
            repo_root=repo,
            record=_rec(1, "2026-04-19T00:00:00Z"),
            keystore=_StubKeyStore(),
        )
        trailer = repo / "sovereignty" / "clock" / "boot_clock_history.hmac"
        obj = json.loads(trailer.read_bytes())
        obj["last_seq_id"] = 99
        trailer.write_bytes(json.dumps(obj).encode("utf-8"))
        with pytest.raises(BootClockHistoryTrailerMismatch):
            verify_boot_clock_history_chain(
                repo_root=repo, keystore=_StubKeyStore()
            )

    def test_corrupt_jsonl_line_detected(self, repo: Path) -> None:
        clock_dir = repo / "sovereignty" / "clock"
        clock_dir.mkdir(parents=True, exist_ok=True)
        (clock_dir / "boot_clock_history.jsonl").write_bytes(
            b"not-valid-json\n"
        )
        with pytest.raises(BootClockHistoryCorrupt):
            read_boot_clock_history(repo)


# ---------------------------------------------------------------------------
# Platform
# ---------------------------------------------------------------------------


class TestPlatform:
    def test_read_boot_epoch_ns_platform_dispatch(self) -> None:
        system = platform.system()
        if system in ("Darwin", "Linux"):
            ns = read_boot_epoch_ns()
            assert isinstance(ns, int)
            assert ns > 0
        else:
            with pytest.raises(BootEpochUnavailable):
                read_boot_epoch_ns()


# ---------------------------------------------------------------------------
# Arg-type gates (E-001)
# ---------------------------------------------------------------------------


class TestArgTypes:
    def test_verify_rejects_bad_path(self) -> None:
        with pytest.raises(TypeError):
            verify_boot_clock_history_chain(
                repo_root="/tmp/x",  # type: ignore[arg-type]
                keystore=_StubKeyStore(),
            )

    def test_verify_rejects_bad_keystore(self, repo: Path) -> None:
        with pytest.raises(TypeError):
            verify_boot_clock_history_chain(
                repo_root=repo, keystore="nope"  # type: ignore[arg-type]
            )

    def test_append_rejects_bad_record(self, repo: Path) -> None:
        with pytest.raises(TypeError):
            append_boot_clock_record(
                repo_root=repo,
                record={"boot_epoch_ns": 1},  # type: ignore[arg-type]
                keystore=_StubKeyStore(),
            )

    def test_read_rejects_str_path(self) -> None:
        with pytest.raises(TypeError):
            read_boot_clock_history("/tmp/x")  # type: ignore[arg-type]
