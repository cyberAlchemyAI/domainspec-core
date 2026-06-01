"""Unit tests for pipeline.sovereignty.init_marker.

Section 1 Round I. Covers §2.7b + §3.11b + §4.9a + §6.5 F-ADM-11/12
+ §7.15 named tests.

Named tests per §7.15:

* ``test_first_boot_writes_init_marker_and_hmac``
* ``test_second_boot_verifies_init_marker_and_does_not_rewrite``
* ``test_tampered_init_marker_body_detected`` — F-ADM-12
* ``test_asymmetric_init_marker_rejected`` (marker XOR hmac) — F-ADM-11
* ``test_missing_init_marker_with_nonempty_ledger_rejected`` — F-ADM-12
* ``test_init_marker_schema_version_skew_rejected`` — F-ADM-12
* ``test_first_boot_write_twice_raises_already_exists`` — F-ADM-11
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from pipeline.sovereignty.init_marker import (
    INIT_MARKER_SCHEMA_VERSION,
    LedgerState,
    SovereigntyInitMarker,
    SovereigntyInitMarkerAlreadyExists,
    SovereigntyInitMarkerMismatch,
    SovereigntyInitMarkerMissing,
    verify_sovereignty_init_marker,
    write_sovereignty_init_marker_first_boot,
)
from pipeline.sovereignty.keys import KeyStore


_HMAC_KEY = b"\xab" * 32


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


@pytest.fixture
def paths(tmp_path: Path) -> dict[str, Path]:
    sov = tmp_path / "sovereignty"
    sov.mkdir(parents=True, exist_ok=True)
    return {
        "marker": sov / "init.marker",
        "hmac": sov / "init.marker.hmac",
        "lock": sov / "init.marker.lock",
        "sov": sov,
    }


def _empty_ledger_states() -> dict[str, LedgerState]:
    return {
        "admin_risk": LedgerState(
            ledger_name="admin_risk", last_seq_id=0, watermark_body_exists=False
        ),
        "degradation": LedgerState(
            ledger_name="degradation", last_seq_id=0, watermark_body_exists=False
        ),
    }


def _nonempty_ledger_states() -> dict[str, LedgerState]:
    return {
        "admin_risk": LedgerState(
            ledger_name="admin_risk", last_seq_id=5, watermark_body_exists=True
        ),
        "degradation": LedgerState(
            ledger_name="degradation", last_seq_id=0, watermark_body_exists=False
        ),
    }


# ---------------------------------------------------------------------------
# Verify outcomes
# ---------------------------------------------------------------------------


class TestFirstBootOutcome:
    def test_verify_returns_none_on_legitimate_first_boot(
        self, paths: dict[str, Path]
    ) -> None:
        result = verify_sovereignty_init_marker(
            marker_path=paths["marker"],
            hmac_path=paths["hmac"],
            keystore=_StubKeyStore(),
            ledger_states=_empty_ledger_states(),
        )
        assert result is None

    def test_first_boot_writes_init_marker_and_hmac(
        self, paths: dict[str, Path]
    ) -> None:
        body = write_sovereignty_init_marker_first_boot(
            marker_path=paths["marker"],
            hmac_path=paths["hmac"],
            lock_path=paths["lock"],
            keystore=_StubKeyStore(),
            boot_clock_history_seq=1,
            boot_epoch_ns=1_700_000_000_000_000_000,
            operator_slug="josh",
        )
        assert isinstance(body, SovereigntyInitMarker)
        assert body.init_version == INIT_MARKER_SCHEMA_VERSION
        assert body.operator_slug == "josh"
        assert body.boot_clock_history_seq_at_init == 1
        assert body.boot_epoch_ns_first == 1_700_000_000_000_000_000
        assert paths["marker"].is_file()
        assert paths["hmac"].is_file()

    def test_second_boot_verifies_init_marker_and_does_not_rewrite(
        self, paths: dict[str, Path]
    ) -> None:
        write_sovereignty_init_marker_first_boot(
            marker_path=paths["marker"],
            hmac_path=paths["hmac"],
            lock_path=paths["lock"],
            keystore=_StubKeyStore(),
            boot_clock_history_seq=1,
            boot_epoch_ns=1_700_000_000_000_000_000,
        )
        mtime_marker = paths["marker"].stat().st_mtime_ns
        mtime_hmac = paths["hmac"].stat().st_mtime_ns

        body = verify_sovereignty_init_marker(
            marker_path=paths["marker"],
            hmac_path=paths["hmac"],
            keystore=_StubKeyStore(),
            ledger_states=_nonempty_ledger_states(),  # ledgers now non-empty
        )
        assert body is not None
        assert body.boot_epoch_ns_first == 1_700_000_000_000_000_000
        assert paths["marker"].stat().st_mtime_ns == mtime_marker
        assert paths["hmac"].stat().st_mtime_ns == mtime_hmac


# ---------------------------------------------------------------------------
# Fail-closed outcomes
# ---------------------------------------------------------------------------


class TestFailClosed:
    def test_missing_init_marker_with_nonempty_ledger_rejected(
        self, paths: dict[str, Path]
    ) -> None:
        """F-ADM-12 — RT-v4 HIGH-1 first-boot-reset signature."""
        with pytest.raises(SovereigntyInitMarkerMismatch) as exc:
            verify_sovereignty_init_marker(
                marker_path=paths["marker"],
                hmac_path=paths["hmac"],
                keystore=_StubKeyStore(),
                ledger_states=_nonempty_ledger_states(),
            )
        assert exc.value.code == "F-ADM-12"

    def test_missing_init_marker_with_watermark_body_rejected(
        self, paths: dict[str, Path]
    ) -> None:
        states = {
            "admin_risk": LedgerState(
                ledger_name="admin_risk", last_seq_id=0, watermark_body_exists=True
            ),
        }
        with pytest.raises(SovereigntyInitMarkerMismatch):
            verify_sovereignty_init_marker(
                marker_path=paths["marker"],
                hmac_path=paths["hmac"],
                keystore=_StubKeyStore(),
                ledger_states=states,
            )

    def test_marker_without_hmac_rejected(self, paths: dict[str, Path]) -> None:
        paths["marker"].write_bytes(b'{"init_version": 1}')
        with pytest.raises(SovereigntyInitMarkerMissing) as exc:
            verify_sovereignty_init_marker(
                marker_path=paths["marker"],
                hmac_path=paths["hmac"],
                keystore=_StubKeyStore(),
                ledger_states=_empty_ledger_states(),
            )
        assert exc.value.code == "F-ADM-11"

    def test_hmac_without_marker_rejected(self, paths: dict[str, Path]) -> None:
        paths["hmac"].write_bytes(b'{"init_version": 1, "init_hmac": "deadbeef"}')
        with pytest.raises(SovereigntyInitMarkerMissing):
            verify_sovereignty_init_marker(
                marker_path=paths["marker"],
                hmac_path=paths["hmac"],
                keystore=_StubKeyStore(),
                ledger_states=_empty_ledger_states(),
            )

    def test_tampered_init_marker_body_detected(self, paths: dict[str, Path]) -> None:
        """F-ADM-12 — body-byte flip triggers HMAC mismatch."""
        write_sovereignty_init_marker_first_boot(
            marker_path=paths["marker"],
            hmac_path=paths["hmac"],
            lock_path=paths["lock"],
            keystore=_StubKeyStore(),
            boot_clock_history_seq=1,
            boot_epoch_ns=1_700_000_000_000_000_000,
        )
        tampered = json.loads(paths["marker"].read_bytes())
        tampered["operator_slug"] = "evil"
        paths["marker"].write_bytes(json.dumps(tampered).encode("utf-8"))
        with pytest.raises(SovereigntyInitMarkerMismatch) as exc:
            verify_sovereignty_init_marker(
                marker_path=paths["marker"],
                hmac_path=paths["hmac"],
                keystore=_StubKeyStore(),
                ledger_states=_empty_ledger_states(),
            )
        assert exc.value.code == "F-ADM-12"

    def test_different_key_fails_verify(self, paths: dict[str, Path]) -> None:
        write_sovereignty_init_marker_first_boot(
            marker_path=paths["marker"],
            hmac_path=paths["hmac"],
            lock_path=paths["lock"],
            keystore=_StubKeyStore(key_bytes=b"\x11" * 32),
            boot_clock_history_seq=1,
            boot_epoch_ns=1,
        )
        with pytest.raises(SovereigntyInitMarkerMismatch):
            verify_sovereignty_init_marker(
                marker_path=paths["marker"],
                hmac_path=paths["hmac"],
                keystore=_StubKeyStore(key_bytes=b"\x22" * 32),
                ledger_states=_empty_ledger_states(),
            )

    def test_init_marker_schema_version_skew_rejected(
        self, paths: dict[str, Path]
    ) -> None:
        """F-ADM-12 — init_version drift between body and trailer."""
        write_sovereignty_init_marker_first_boot(
            marker_path=paths["marker"],
            hmac_path=paths["hmac"],
            lock_path=paths["lock"],
            keystore=_StubKeyStore(),
            boot_clock_history_seq=1,
            boot_epoch_ns=1,
        )
        tr = json.loads(paths["hmac"].read_bytes())
        tr["init_version"] = 99
        paths["hmac"].write_bytes(json.dumps(tr).encode("utf-8"))
        with pytest.raises(SovereigntyInitMarkerMismatch):
            verify_sovereignty_init_marker(
                marker_path=paths["marker"],
                hmac_path=paths["hmac"],
                keystore=_StubKeyStore(),
                ledger_states=_empty_ledger_states(),
            )

    def test_first_boot_write_twice_raises_already_exists(
        self, paths: dict[str, Path]
    ) -> None:
        """F-ADM-11 — write-once invariant."""
        write_sovereignty_init_marker_first_boot(
            marker_path=paths["marker"],
            hmac_path=paths["hmac"],
            lock_path=paths["lock"],
            keystore=_StubKeyStore(),
            boot_clock_history_seq=1,
            boot_epoch_ns=1,
        )
        with pytest.raises(SovereigntyInitMarkerAlreadyExists) as exc:
            write_sovereignty_init_marker_first_boot(
                marker_path=paths["marker"],
                hmac_path=paths["hmac"],
                lock_path=paths["lock"],
                keystore=_StubKeyStore(),
                boot_clock_history_seq=2,
                boot_epoch_ns=2,
            )
        assert exc.value.code == "F-ADM-11"


class TestArgTypes:
    def test_verify_rejects_bad_paths(self, paths: dict[str, Path]) -> None:
        with pytest.raises(TypeError):
            verify_sovereignty_init_marker(
                marker_path="/tmp/x",  # type: ignore[arg-type]
                hmac_path=paths["hmac"],
                keystore=_StubKeyStore(),
                ledger_states=_empty_ledger_states(),
            )

    def test_verify_rejects_bad_keystore(self, paths: dict[str, Path]) -> None:
        with pytest.raises(TypeError):
            verify_sovereignty_init_marker(
                marker_path=paths["marker"],
                hmac_path=paths["hmac"],
                keystore="nope",  # type: ignore[arg-type]
                ledger_states=_empty_ledger_states(),
            )

    def test_write_rejects_bad_int(self, paths: dict[str, Path]) -> None:
        with pytest.raises(TypeError):
            write_sovereignty_init_marker_first_boot(
                marker_path=paths["marker"],
                hmac_path=paths["hmac"],
                lock_path=paths["lock"],
                keystore=_StubKeyStore(),
                boot_clock_history_seq="1",  # type: ignore[arg-type]
                boot_epoch_ns=1,
            )
