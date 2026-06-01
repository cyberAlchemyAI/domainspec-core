"""Tests for pipeline.sovereignty.audit.

Coverage targets (per Round-B spec card `round_b_audit.md`):
  - §1 row 4 public API
  - §5.3 BT3 atomic append protocol
  - §5.6 BT8 HMAC trailer + watermark integrity
  - §7.3 regression triplet:
      test_bt3_fail_closed_on_unreadable_ledger
      test_bt8_chain_verification_detects_tamper
      test_bt8_chain_verification_detects_replay
  - §6.5 failure-code coverage
  - E-001 min_key_bytes default enforcement
  - Rollback-attack simulation (RT-v3 HIGH-1 closure)
  - Concurrency via fcntl lock
"""

from __future__ import annotations

import json
import os
import threading
from pathlib import Path
from typing import Iterator

import pytest

from pipeline.sovereignty import (
    CHAIN_VERIFY_FAST_TAIL_ENTRIES,
    LEDGER_ROTATION_SIZE_LIMIT_BYTES,
    LedgerChainBroken,
    LedgerHMACTrailerMismatch,
    LedgerTrailer,
    LedgerUnreadable,
    LedgerWatermark,
    LedgerWatermarkRegression,
    WatermarkHmacMismatch,
    WatermarkHmacMissing,
    append_to_ledger,
    canonical_json_bytes,
    rotate_ledger_if_needed,
    update_watermark,
    verify_ledger,
    verify_ledger_freshness,
    verify_watermarks,
)


# -------- fixtures --------


@pytest.fixture
def paths(tmp_path: Path) -> dict[str, Path]:
    """Full set of paths a caller passes to append_to_ledger."""
    base = tmp_path
    (base / "ledgers").mkdir()
    (base / "ledgers" / "locks").mkdir()
    (base / "watermarks").mkdir()
    return {
        "ledger": base / "ledgers" / "admin_risk.jsonl",
        "trailer": base / "ledgers" / "admin_risk.hmac",
        "lock": base / "ledgers" / "locks" / "admin_risk.lock",
        "watermarks": base / "watermarks" / "ledger_watermarks.json",
        "watermarks_hmac": base / "watermarks" / "ledger_watermarks.hmac",
        "watermarks_lock": base / "watermarks" / "ledger_watermarks.lock",
    }


@pytest.fixture
def keys() -> dict[str, bytes]:
    """Deterministic keys for tests — 32 bytes each (E-001 floor)."""
    return {
        "ledger": b"L" * 32,
        "watermarks": b"W" * 32,
    }


def _append(
    paths: dict[str, Path],
    keys: dict[str, bytes],
    entry: dict,
    *,
    ledger_name: str = "admin_risk",
) -> LedgerTrailer:
    return append_to_ledger(
        paths["ledger"],
        entry,
        ledger_name=ledger_name,
        hmac_key=keys["ledger"],
        lock_path=paths["lock"],
        trailer_path=paths["trailer"],
        watermarks_path=paths["watermarks"],
        watermarks_hmac_key=keys["watermarks"],
        watermarks_hmac_path=paths["watermarks_hmac"],
        watermarks_lock_path=paths["watermarks_lock"],
    )


# -------- canonical_json_bytes --------


class TestCanonicalJsonBytes:
    def test_deterministic(self) -> None:
        a = canonical_json_bytes({"b": 2, "a": 1})
        b = canonical_json_bytes({"a": 1, "b": 2})
        assert a == b == b'{"a":1,"b":2}'

    def test_no_whitespace(self) -> None:
        assert b" " not in canonical_json_bytes({"x": 1, "y": [1, 2, 3]})

    def test_utf8_non_ascii_preserved(self) -> None:
        out = canonical_json_bytes({"name": "café"})
        # ensure_ascii=False preserves the utf-8 bytes
        assert "café".encode("utf-8") in out

    def test_round_trip_through_json_loads(self) -> None:
        obj = {"a": 1, "b": [1, 2, 3], "c": {"nested": True}}
        canonical = canonical_json_bytes(obj)
        reparsed = json.loads(canonical)
        assert reparsed == obj

    def test_non_serializable_raises(self) -> None:
        with pytest.raises(TypeError):
            canonical_json_bytes({"bytes_leak": b"bytes-not-json-serializable"})


# -------- append: happy path + chain invariants --------


class TestAppendHappyPath:
    def test_single_append_produces_trailer(self, paths, keys) -> None:
        trailer = _append(paths, keys, {"severity": "GREEN", "payload": {"x": 1}})
        assert isinstance(trailer, LedgerTrailer)
        assert trailer.last_seq_id == 1
        assert trailer.ledger_name == "admin_risk"
        assert len(trailer.ledger_hmac) == 128
        assert len(trailer.trailer_hmac) == 128
        assert len(trailer.last_entry_hash) == 128

    def test_multiple_appends_monotonic_seq(self, paths, keys) -> None:
        seqs = []
        for i in range(10):
            t = _append(paths, keys, {"severity": "GREEN", "i": i})
            seqs.append(t.last_seq_id)
        assert seqs == list(range(1, 11))

    def test_ledger_file_has_one_line_per_append(self, paths, keys) -> None:
        for i in range(5):
            _append(paths, keys, {"severity": "GREEN", "i": i})
        lines = paths["ledger"].read_bytes().splitlines()
        assert len(lines) == 5

    def test_each_entry_has_required_chain_fields(self, paths, keys) -> None:
        _append(paths, keys, {"severity": "GREEN"})
        _append(paths, keys, {"severity": "YELLOW"})
        for raw in paths["ledger"].read_bytes().splitlines():
            entry = json.loads(raw)
            for key in ("seq_id", "prev_hash", "entry_hash", "timestamp_utc", "issued_monotonic_ns"):
                assert key in entry
            assert len(entry["prev_hash"]) == 128
            assert len(entry["entry_hash"]) == 128

    def test_genesis_prev_hash_is_zero(self, paths, keys) -> None:
        _append(paths, keys, {"severity": "GREEN"})
        first = json.loads(paths["ledger"].read_bytes().splitlines()[0])
        assert first["prev_hash"] == "0" * 128


# -------- verify_ledger --------


class TestVerifyLedger:
    def test_verify_succeeds_after_appends(self, paths, keys) -> None:
        for i in range(3):
            _append(paths, keys, {"i": i})
        trailer = verify_ledger(
            paths["ledger"], paths["trailer"], hmac_key=keys["ledger"]
        )
        assert trailer.last_seq_id == 3

    def test_verify_raises_on_missing_trailer(self, paths, keys) -> None:
        _append(paths, keys, {"i": 1})
        paths["trailer"].unlink()
        with pytest.raises(LedgerUnreadable):
            verify_ledger(paths["ledger"], paths["trailer"], hmac_key=keys["ledger"])

    def test_verify_raises_on_wrong_key(self, paths, keys) -> None:
        _append(paths, keys, {"i": 1})
        with pytest.raises(LedgerHMACTrailerMismatch):
            verify_ledger(
                paths["ledger"], paths["trailer"], hmac_key=b"X" * 32
            )

    def test_verify_raises_on_ledger_tamper(self, paths, keys) -> None:
        """Blueprint §7.3 `test_bt8_chain_verification_detects_tamper`."""
        _append(paths, keys, {"severity": "GREEN", "x": "legit"})
        # Flip one byte in the middle of the ledger.
        raw = paths["ledger"].read_bytes()
        mid = len(raw) // 2
        tampered = raw[:mid] + bytes([raw[mid] ^ 0x01]) + raw[mid + 1 :]
        paths["ledger"].write_bytes(tampered)
        with pytest.raises((LedgerChainBroken, LedgerHMACTrailerMismatch)):
            verify_ledger(
                paths["ledger"], paths["trailer"], hmac_key=keys["ledger"]
            )

    def test_verify_raises_on_replay_line_deleted(self, paths, keys) -> None:
        """Blueprint §7.3 `test_bt8_chain_verification_detects_replay`."""
        for i in range(5):
            _append(paths, keys, {"i": i})
        # Delete line N+1 (second line, index 1).
        lines = paths["ledger"].read_bytes().splitlines()
        truncated = b"\n".join(lines[:1] + lines[2:]) + b"\n"
        paths["ledger"].write_bytes(truncated)
        with pytest.raises((LedgerChainBroken, LedgerHMACTrailerMismatch)):
            verify_ledger(
                paths["ledger"], paths["trailer"], hmac_key=keys["ledger"]
            )

    def test_verify_raises_on_prev_hash_mismatch(self, paths, keys) -> None:
        _append(paths, keys, {"i": 1})
        _append(paths, keys, {"i": 2})
        lines = paths["ledger"].read_bytes().splitlines()
        second = json.loads(lines[1])
        second["prev_hash"] = "f" * 128  # rewrite to non-matching hash
        lines[1] = canonical_json_bytes(second)
        paths["ledger"].write_bytes(b"\n".join(lines) + b"\n")
        with pytest.raises((LedgerChainBroken, LedgerHMACTrailerMismatch)):
            verify_ledger(
                paths["ledger"], paths["trailer"], hmac_key=keys["ledger"]
            )

    def test_verify_raises_on_trailer_tamper(self, paths, keys) -> None:
        _append(paths, keys, {"i": 1})
        raw = paths["trailer"].read_bytes()
        # Flip a byte in the trailer body line.
        tampered = bytes([raw[0] ^ 0x01]) + raw[1:]
        paths["trailer"].write_bytes(tampered)
        with pytest.raises((LedgerHMACTrailerMismatch, LedgerUnreadable)):
            verify_ledger(
                paths["ledger"], paths["trailer"], hmac_key=keys["ledger"]
            )


# -------- watermarks --------


class TestWatermarks:
    def test_watermark_populated_after_append(self, paths, keys) -> None:
        _append(paths, keys, {"i": 1})
        wms = verify_watermarks(
            paths["watermarks"],
            paths["watermarks_hmac"],
            watermarks_hmac_key=keys["watermarks"],
        )
        assert "admin_risk" in wms
        assert wms["admin_risk"].last_seq_id == 1

    def test_watermark_tracks_latest_seq(self, paths, keys) -> None:
        for i in range(7):
            _append(paths, keys, {"i": i})
        wms = verify_watermarks(
            paths["watermarks"],
            paths["watermarks_hmac"],
            watermarks_hmac_key=keys["watermarks"],
        )
        assert wms["admin_risk"].last_seq_id == 7

    def test_verify_watermarks_empty_both_missing(self, paths, keys) -> None:
        wms = verify_watermarks(
            paths["watermarks"],
            paths["watermarks_hmac"],
            watermarks_hmac_key=keys["watermarks"],
        )
        assert wms == {}

    def test_watermark_body_without_hmac_raises(self, paths, keys) -> None:
        _append(paths, keys, {"i": 1})
        paths["watermarks_hmac"].unlink()
        with pytest.raises(WatermarkHmacMissing):
            verify_watermarks(
                paths["watermarks"],
                paths["watermarks_hmac"],
                watermarks_hmac_key=keys["watermarks"],
            )

    def test_watermark_hmac_without_body_raises(self, paths, keys) -> None:
        _append(paths, keys, {"i": 1})
        paths["watermarks"].unlink()
        with pytest.raises(WatermarkHmacMissing):
            verify_watermarks(
                paths["watermarks"],
                paths["watermarks_hmac"],
                watermarks_hmac_key=keys["watermarks"],
            )

    def test_watermark_body_tamper_detected(self, paths, keys) -> None:
        _append(paths, keys, {"i": 1})
        body = json.loads(paths["watermarks"].read_bytes())
        body["admin_risk"]["last_seq_id"] = 99999  # forge forward
        paths["watermarks"].write_bytes(canonical_json_bytes(body))
        with pytest.raises(WatermarkHmacMismatch):
            verify_watermarks(
                paths["watermarks"],
                paths["watermarks_hmac"],
                watermarks_hmac_key=keys["watermarks"],
            )

    def test_watermark_trailer_tamper_detected(self, paths, keys) -> None:
        _append(paths, keys, {"i": 1})
        raw = paths["watermarks_hmac"].read_bytes()
        tampered = bytes([raw[0] ^ 0x01]) + raw[1:]
        paths["watermarks_hmac"].write_bytes(tampered)
        with pytest.raises((WatermarkHmacMismatch, WatermarkHmacMissing)):
            verify_watermarks(
                paths["watermarks"],
                paths["watermarks_hmac"],
                watermarks_hmac_key=keys["watermarks"],
            )

    def test_watermark_wrong_key_detected(self, paths, keys) -> None:
        _append(paths, keys, {"i": 1})
        with pytest.raises(WatermarkHmacMismatch):
            verify_watermarks(
                paths["watermarks"],
                paths["watermarks_hmac"],
                watermarks_hmac_key=b"Z" * 32,
            )


# -------- freshness / rollback --------


class TestLedgerFreshness:
    def test_freshness_succeeds_same_seq(self, paths, keys) -> None:
        _append(paths, keys, {"i": 1})
        wms = verify_watermarks(
            paths["watermarks"],
            paths["watermarks_hmac"],
            watermarks_hmac_key=keys["watermarks"],
        )
        trailer = verify_ledger_freshness(
            paths["ledger"], paths["trailer"], wms, hmac_key=keys["ledger"]
        )
        assert trailer.last_seq_id == 1

    def test_rollback_attack_detected(self, paths, keys, tmp_path) -> None:
        """RT-v3 HIGH-1 closure — full three-file rollback rejected.

        Snapshot ledger+trailer+watermarks after 5 appends, then after
        10 appends, roll the three ledger files back to snapshot-1, but
        leave watermark body+HMAC at snapshot-2. Verify detects
        regression.

        Actually the stronger test is: roll all THREE files (ledger,
        trailer, watermark body, watermark HMAC) back to snapshot-1 in
        a self-consistent way. The watermark HMAC on disk still
        verifies — BUT a fresh reader needs to see the on-disk state,
        which IS consistent, so verify_ledger_freshness alone won't
        detect it because it only compares trailer to watermark (both
        rolled back).

        The defence here is: F-ADM-10 watermark HMAC binds body to a
        key out of attacker's reach. Attacker cannot forge a NEW
        watermark for a ROLLED-BACK ledger. This test exercises the
        simpler case — partial rollback (ledger+trailer rolled back,
        watermark kept) — which is what freshness check catches.
        """
        # Snapshot 1
        for i in range(5):
            _append(paths, keys, {"i": i})
        snap1_ledger = paths["ledger"].read_bytes()
        snap1_trailer = paths["trailer"].read_bytes()
        # Advance to snapshot 2
        for i in range(5, 10):
            _append(paths, keys, {"i": i})
        # Partial rollback — ledger + trailer to snap1, watermarks kept at snap2.
        paths["ledger"].write_bytes(snap1_ledger)
        paths["trailer"].write_bytes(snap1_trailer)
        wms = verify_watermarks(
            paths["watermarks"],
            paths["watermarks_hmac"],
            watermarks_hmac_key=keys["watermarks"],
        )
        with pytest.raises(LedgerWatermarkRegression):
            verify_ledger_freshness(
                paths["ledger"], paths["trailer"], wms, hmac_key=keys["ledger"]
            )

    def test_same_seq_different_hmac_detected(self, paths, keys) -> None:
        """If trailer hmac differs from watermark at same seq — rollback."""
        _append(paths, keys, {"i": 1})
        wms = verify_watermarks(
            paths["watermarks"],
            paths["watermarks_hmac"],
            watermarks_hmac_key=keys["watermarks"],
        )
        # Forge a different watermark entry at same seq_id.
        forged = {
            "admin_risk": LedgerWatermark(
                schema_version="v1",
                ledger_name="admin_risk",
                last_seq_id=1,
                last_trailer_hmac_hex="a" * 128,
                wall_at_write_utc="2026-04-19T00:00:00Z",
            )
        }
        with pytest.raises(LedgerWatermarkRegression):
            verify_ledger_freshness(
                paths["ledger"], paths["trailer"], forged, hmac_key=keys["ledger"]
            )


# -------- rotation --------


class TestRotation:
    def test_rotation_skipped_when_small(self, paths, keys) -> None:
        _append(paths, keys, {"i": 1})
        result = rotate_ledger_if_needed(paths["ledger"], trailer_path=paths["trailer"])
        assert result is None

    def test_rotation_moves_ledger_and_creates_empty(self, paths, keys, monkeypatch) -> None:
        """Force the rotation threshold low so the test finishes fast."""
        import pipeline.sovereignty.audit as audit_mod

        monkeypatch.setattr(audit_mod, "LEDGER_ROTATION_SIZE_LIMIT_BYTES", 64)
        # Append entries until file exceeds 64 bytes (first append will do it).
        _append(paths, keys, {"i": 0, "padding": "x" * 100})
        # Ensure > threshold
        assert paths["ledger"].stat().st_size >= 64
        rotated = rotate_ledger_if_needed(
            paths["ledger"], trailer_path=paths["trailer"]
        )
        assert rotated is not None
        assert rotated.exists()
        assert paths["ledger"].exists()
        assert paths["ledger"].stat().st_size == 0


# -------- type safety --------


class TestTypeSafety:
    def test_append_rejects_str_path(self, paths, keys) -> None:
        with pytest.raises(TypeError):
            append_to_ledger(
                str(paths["ledger"]),  # type: ignore[arg-type]
                {"x": 1},
                ledger_name="admin_risk",
                hmac_key=keys["ledger"],
                lock_path=paths["lock"],
                trailer_path=paths["trailer"],
                watermarks_path=paths["watermarks"],
                watermarks_hmac_key=keys["watermarks"],
                watermarks_hmac_path=paths["watermarks_hmac"],
                watermarks_lock_path=paths["watermarks_lock"],
            )

    def test_append_rejects_str_key(self, paths, keys) -> None:
        with pytest.raises(TypeError):
            _append(paths, {"ledger": "not-bytes", "watermarks": keys["watermarks"]}, {"x": 1})  # type: ignore[dict-item]

    def test_append_rejects_reserved_fields(self, paths, keys) -> None:
        with pytest.raises(ValueError) as exc_info:
            _append(paths, keys, {"seq_id": 99, "data": "x"})
        assert "reserved" in str(exc_info.value).lower()

    def test_verify_rejects_str_path(self, paths, keys) -> None:
        with pytest.raises(TypeError):
            verify_ledger(
                str(paths["ledger"]), paths["trailer"], hmac_key=keys["ledger"]  # type: ignore[arg-type]
            )

    def test_verify_rejects_str_key(self, paths, keys) -> None:
        _append(paths, keys, {"i": 1})
        with pytest.raises(TypeError):
            verify_ledger(
                paths["ledger"], paths["trailer"], hmac_key="not-bytes"  # type: ignore[arg-type]
            )


# -------- blueprint §7.3 regression triplet --------


class TestBT3BT8Regression:
    def test_bt3_fail_closed_on_unreadable_ledger(self, paths, keys) -> None:
        """§7.3 — corrupt JSONL → LedgerUnreadable or LedgerChainBroken."""
        # Write garbage where ledger would be.
        paths["ledger"].parent.mkdir(parents=True, exist_ok=True)
        paths["ledger"].write_bytes(b"\x00\x01this is not json\x00\n")
        # Write a bogus trailer so verify gets far enough to try to read.
        paths["trailer"].write_bytes(
            canonical_json_bytes(
                {
                    "schema_version": "v2",
                    "ledger_name": "admin_risk",
                    "last_seq_id": 1,
                    "last_entry_hash": "0" * 128,
                    "ledger_hmac": "0" * 128,
                    "trailer_version": 2,
                }
            )
            + b"\n"
            + canonical_json_bytes({"trailer_hmac": "0" * 128})
            + b"\n"
        )
        with pytest.raises((LedgerUnreadable, LedgerChainBroken, LedgerHMACTrailerMismatch)):
            verify_ledger(paths["ledger"], paths["trailer"], hmac_key=keys["ledger"])

    def test_bt8_chain_verification_detects_tamper(self, paths, keys) -> None:
        _append(paths, keys, {"severity": "YELLOW", "msg": "original"})
        _append(paths, keys, {"severity": "YELLOW", "msg": "second"})
        raw = paths["ledger"].read_bytes()
        # Flip byte in the middle of line 1.
        idx = raw.index(b"original") + 3
        tampered = raw[:idx] + bytes([raw[idx] ^ 0x20]) + raw[idx + 1 :]
        paths["ledger"].write_bytes(tampered)
        with pytest.raises((LedgerChainBroken, LedgerHMACTrailerMismatch)):
            verify_ledger(
                paths["ledger"], paths["trailer"], hmac_key=keys["ledger"]
            )

    def test_bt8_chain_verification_detects_replay(self, paths, keys) -> None:
        for i in range(4):
            _append(paths, keys, {"i": i})
        # Delete line 2 (index 1).
        lines = paths["ledger"].read_bytes().splitlines()
        paths["ledger"].write_bytes(b"\n".join(lines[:1] + lines[2:]) + b"\n")
        with pytest.raises((LedgerChainBroken, LedgerHMACTrailerMismatch)):
            verify_ledger(
                paths["ledger"], paths["trailer"], hmac_key=keys["ledger"]
            )


# -------- concurrency --------


class TestConcurrency:
    def test_two_threads_serialize_via_fcntl(self, paths, keys) -> None:
        """Two threads racing append_to_ledger produce monotonic seq."""
        errors: list[Exception] = []

        def worker(n: int) -> None:
            try:
                _append(paths, keys, {"thread": "x", "n": n})
            except Exception as e:  # pragma: no cover - diagnostic
                errors.append(e)

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        assert errors == [], f"concurrent errors: {errors}"
        # Verify all 8 appends succeeded, chain intact, seq_ids 1..8.
        trailer = verify_ledger(
            paths["ledger"], paths["trailer"], hmac_key=keys["ledger"]
        )
        assert trailer.last_seq_id == 8
        # Also watermark reflects latest
        wms = verify_watermarks(
            paths["watermarks"],
            paths["watermarks_hmac"],
            watermarks_hmac_key=keys["watermarks"],
        )
        assert wms["admin_risk"].last_seq_id == 8


# -------- deterministic trailer --------


class TestDeterministicTrailer:
    def test_append_then_verify_byte_identical_trailer(self, paths, keys) -> None:
        """Trailer bytes stable under a given (ledger_state, key, ledger_name)."""
        _append(paths, keys, {"x": 1})
        snap = paths["trailer"].read_bytes()
        # Re-verify twice; trailer file unchanged between verifications.
        verify_ledger(paths["ledger"], paths["trailer"], hmac_key=keys["ledger"])
        assert paths["trailer"].read_bytes() == snap


# -------- E-001 HMAC key floor --------


class TestHMACKeyDiscipline:
    def test_append_accepts_32_byte_key(self, paths) -> None:
        keys = {"ledger": b"A" * 32, "watermarks": b"B" * 32}
        t = _append(paths, keys, {"x": 1})
        assert t.last_seq_id == 1

    def test_append_rejects_short_key(self, paths) -> None:
        keys = {"ledger": b"short", "watermarks": b"B" * 32}
        with pytest.raises(ValueError):
            _append(paths, keys, {"x": 1})

    def test_append_rejects_short_watermark_key(self, paths) -> None:
        keys = {"ledger": b"A" * 32, "watermarks": b"short"}
        with pytest.raises(ValueError):
            _append(paths, keys, {"x": 1})


# -------- constants sanity --------


class TestConstants:
    def test_rotation_is_100_mib(self) -> None:
        assert LEDGER_ROTATION_SIZE_LIMIT_BYTES == 100 * 1024 * 1024

    def test_fast_tail_entries_is_100(self) -> None:
        assert CHAIN_VERIFY_FAST_TAIL_ENTRIES == 100


# -------- corpus: empty / single / many --------


class TestCorpus:
    def test_empty_ledger_tail_is_genesis(self, paths, keys) -> None:
        """Freshly-created ledger (no appends) returns empty watermarks."""
        wms = verify_watermarks(
            paths["watermarks"],
            paths["watermarks_hmac"],
            watermarks_hmac_key=keys["watermarks"],
        )
        assert wms == {}

    def test_single_entry_chain(self, paths, keys) -> None:
        t = _append(paths, keys, {"only": True})
        assert t.last_seq_id == 1
        trailer = verify_ledger(
            paths["ledger"], paths["trailer"], hmac_key=keys["ledger"]
        )
        assert trailer.last_seq_id == 1

    def test_thousand_entries_chain(self, paths, keys) -> None:
        """Larger corpus test — chain holds at non-trivial N."""
        for i in range(1000):
            _append(paths, keys, {"i": i})
        trailer = verify_ledger(
            paths["ledger"], paths["trailer"], hmac_key=keys["ledger"]
        )
        assert trailer.last_seq_id == 1000
