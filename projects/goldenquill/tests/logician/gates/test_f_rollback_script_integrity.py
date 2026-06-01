"""Unit tests for F-ROLLBACK-SCRIPT-INTEGRITY (F-AMDT-05).

Spec card: pipeline/engineering/spec_cards/logician_v2_2_f_rollback_script_integrity.md
Gate module: pipeline/logician/gates/f_rollback_script_integrity.py
"""

from __future__ import annotations

import pytest

from pipeline.logician.gates.f_rollback_script_integrity import (
    F_AMDT_05,
    RollbackScriptIntegrityDetail,
    RollbackScriptIntegrityResult,
    check_rollback_script_integrity,
)


# ---------------------------------------------------------------------------
# Fakes
# ---------------------------------------------------------------------------


class _StaticVerifier:
    """Signature verifier that maps a fixed ``(bytes, signature, key)`` triple
    to True and returns False for everything else."""

    def __init__(
        self,
        valid_bytes: bytes,
        valid_signature: bytes,
        valid_public_key: bytes,
    ) -> None:
        self._valid = (valid_bytes, valid_signature, valid_public_key)
        self.calls: list[tuple[bytes, bytes, bytes]] = []

    def __call__(self, message_bytes: bytes, signature: bytes, public_key: bytes) -> bool:
        self.calls.append((message_bytes, signature, public_key))
        return (message_bytes, signature, public_key) == self._valid


def _const_ledger(value: str):
    def _reader() -> str:
        return value
    return _reader


def _const_metadata(value: dict):
    def _reader(script_path: str) -> dict:
        return value
    return _reader


_SCRIPT = b"#!/bin/bash\necho rollback\n"
_SIG = b"sig-bytes"
_PK = b"pk-bytes"
_LEDGER = "abc123def456"


@pytest.fixture
def ok_verifier() -> _StaticVerifier:
    return _StaticVerifier(_SCRIPT, _SIG, _PK)


def _ok_inputs() -> dict:
    return dict(
        script_path="spike_rollback.sh",
        script_bytes=_SCRIPT,
        signature=_SIG,
        public_key=_PK,
    )


# ---------------------------------------------------------------------------
# Happy paths
# ---------------------------------------------------------------------------


def test_valid_signature_matching_ledger_passes(ok_verifier: _StaticVerifier) -> None:
    result = check_rollback_script_integrity(
        **_ok_inputs(),
        signature_verify=ok_verifier,
        ledger_hash_reader=_const_ledger(_LEDGER),
        script_metadata_reader=_const_metadata({"ledger_hash_at_pin": _LEDGER}),
    )
    assert result.success is True
    assert result.failure_code is None
    assert isinstance(result.detail, RollbackScriptIntegrityDetail)
    assert result.detail.reason_tag == "ok"
    assert result.detail.check_failed == ""
    assert result.detail.reader_error is None
    assert result.detail.script_path == "spike_rollback.sh"


def test_valid_signature_with_extra_metadata_keys_passes(ok_verifier: _StaticVerifier) -> None:
    metadata = {
        "ledger_hash_at_pin": _LEDGER,
        "author_timestamp_utc": "2026-04-20T00:00:00Z",
        "amendment_id": "EN-001",
    }
    result = check_rollback_script_integrity(
        **_ok_inputs(),
        signature_verify=ok_verifier,
        ledger_hash_reader=_const_ledger(_LEDGER),
        script_metadata_reader=_const_metadata(metadata),
    )
    assert result.success is True


def test_empty_script_bytes_with_matching_signature_passes() -> None:
    verifier = _StaticVerifier(b"", _SIG, _PK)
    result = check_rollback_script_integrity(
        script_path="empty.sh",
        script_bytes=b"",
        signature=_SIG,
        public_key=_PK,
        signature_verify=verifier,
        ledger_hash_reader=_const_ledger(_LEDGER),
        script_metadata_reader=_const_metadata({"ledger_hash_at_pin": _LEDGER}),
    )
    assert result.success is True


def test_empty_ledger_head_pin_matches_passes() -> None:
    """Degenerate case: ledger is empty (genesis); script pinned to empty."""
    verifier = _StaticVerifier(_SCRIPT, _SIG, _PK)
    result = check_rollback_script_integrity(
        **_ok_inputs(),
        signature_verify=verifier,
        ledger_hash_reader=_const_ledger(""),
        script_metadata_reader=_const_metadata({"ledger_hash_at_pin": ""}),
    )
    # Pinned hash empty → treated as missing, DENY.
    assert result.success is False
    assert result.detail is not None
    assert result.detail.check_failed == "ledger_hash"


# ---------------------------------------------------------------------------
# Signature failures
# ---------------------------------------------------------------------------


def test_signature_verify_returns_false_denies() -> None:
    def _bad_verify(_a: bytes, _b: bytes, _c: bytes) -> bool:
        return False

    result = check_rollback_script_integrity(
        **_ok_inputs(),
        signature_verify=_bad_verify,
        ledger_hash_reader=_const_ledger(_LEDGER),
        script_metadata_reader=_const_metadata({"ledger_hash_at_pin": _LEDGER}),
    )
    assert result.success is False
    assert result.failure_code == F_AMDT_05
    assert result.detail is not None
    assert result.detail.check_failed == "signature"
    assert result.detail.reason_tag == "signature_verify_returned_false"


def test_script_modified_single_byte_denies() -> None:
    verifier = _StaticVerifier(_SCRIPT, _SIG, _PK)
    mutated = _SCRIPT[:-1] + b"X"
    result = check_rollback_script_integrity(
        script_path="spike_rollback.sh",
        script_bytes=mutated,
        signature=_SIG,
        public_key=_PK,
        signature_verify=verifier,
        ledger_hash_reader=_const_ledger(_LEDGER),
        script_metadata_reader=_const_metadata({"ledger_hash_at_pin": _LEDGER}),
    )
    assert result.success is False
    assert result.detail is not None
    assert result.detail.check_failed == "signature"


def test_empty_signature_bytes_denies() -> None:
    verifier = _StaticVerifier(_SCRIPT, b"sig", _PK)
    result = check_rollback_script_integrity(
        script_path="spike_rollback.sh",
        script_bytes=_SCRIPT,
        signature=b"",
        public_key=_PK,
        signature_verify=verifier,
        ledger_hash_reader=_const_ledger(_LEDGER),
        script_metadata_reader=_const_metadata({"ledger_hash_at_pin": _LEDGER}),
    )
    assert result.success is False
    assert result.detail is not None
    assert result.detail.check_failed == "signature"


def test_wrong_public_key_denies() -> None:
    verifier = _StaticVerifier(_SCRIPT, _SIG, _PK)
    result = check_rollback_script_integrity(
        script_path="spike_rollback.sh",
        script_bytes=_SCRIPT,
        signature=_SIG,
        public_key=b"wrong-pk",
        signature_verify=verifier,
        ledger_hash_reader=_const_ledger(_LEDGER),
        script_metadata_reader=_const_metadata({"ledger_hash_at_pin": _LEDGER}),
    )
    assert result.success is False
    assert result.detail is not None
    assert result.detail.check_failed == "signature"


def test_signature_verify_returns_truthy_not_True_denies() -> None:
    """Strict `is True` identity: non-bool truthy values are NOT accepted."""

    def _truthy(_a: bytes, _b: bytes, _c: bytes):  # type: ignore[no-untyped-def]
        return 1  # truthy but not True

    result = check_rollback_script_integrity(
        **_ok_inputs(),
        signature_verify=_truthy,
        ledger_hash_reader=_const_ledger(_LEDGER),
        script_metadata_reader=_const_metadata({"ledger_hash_at_pin": _LEDGER}),
    )
    assert result.success is False
    assert result.detail is not None
    assert result.detail.check_failed == "signature"


@pytest.mark.parametrize("truthy", ["yes", 1, 2.5, [1], {"a": 1}, object()])
def test_signature_verify_truthy_not_True_denies_parametrized(truthy: object) -> None:
    def _v(_a: bytes, _b: bytes, _c: bytes):  # type: ignore[no-untyped-def]
        return truthy

    result = check_rollback_script_integrity(
        **_ok_inputs(),
        signature_verify=_v,
        ledger_hash_reader=_const_ledger(_LEDGER),
        script_metadata_reader=_const_metadata({"ledger_hash_at_pin": _LEDGER}),
    )
    assert result.success is False
    assert result.detail is not None
    assert result.detail.check_failed == "signature"


# ---------------------------------------------------------------------------
# Ledger-hash failures
# ---------------------------------------------------------------------------


def test_ledger_hash_mismatch_denies(ok_verifier: _StaticVerifier) -> None:
    result = check_rollback_script_integrity(
        **_ok_inputs(),
        signature_verify=ok_verifier,
        ledger_hash_reader=_const_ledger("DIFFERENT_HASH"),
        script_metadata_reader=_const_metadata({"ledger_hash_at_pin": _LEDGER}),
    )
    assert result.success is False
    assert result.detail is not None
    assert result.detail.check_failed == "ledger_hash"
    assert result.detail.reason_tag == "ledger_hash_live_mismatches_pin"


def test_ledger_hash_differs_by_one_character_denies(ok_verifier: _StaticVerifier) -> None:
    live = _LEDGER[:-1] + "Z"
    result = check_rollback_script_integrity(
        **_ok_inputs(),
        signature_verify=ok_verifier,
        ledger_hash_reader=_const_ledger(live),
        script_metadata_reader=_const_metadata({"ledger_hash_at_pin": _LEDGER}),
    )
    assert result.success is False
    assert result.detail is not None
    assert result.detail.check_failed == "ledger_hash"


def test_metadata_missing_ledger_hash_at_pin_denies(ok_verifier: _StaticVerifier) -> None:
    result = check_rollback_script_integrity(
        **_ok_inputs(),
        signature_verify=ok_verifier,
        ledger_hash_reader=_const_ledger(_LEDGER),
        script_metadata_reader=_const_metadata({"other_field": "x"}),
    )
    assert result.success is False
    assert result.detail is not None
    assert result.detail.check_failed == "ledger_hash"
    assert result.detail.reason_tag == "ledger_hash_at_pin_missing_or_empty"


def test_metadata_ledger_hash_empty_string_denies(ok_verifier: _StaticVerifier) -> None:
    result = check_rollback_script_integrity(
        **_ok_inputs(),
        signature_verify=ok_verifier,
        ledger_hash_reader=_const_ledger(_LEDGER),
        script_metadata_reader=_const_metadata({"ledger_hash_at_pin": ""}),
    )
    assert result.success is False
    assert result.detail is not None
    assert result.detail.check_failed == "ledger_hash"
    assert result.detail.reason_tag == "ledger_hash_at_pin_missing_or_empty"


@pytest.mark.parametrize("bad_pin", [None, 123, ["a"], {"x": "y"}, b"bytes"])
def test_metadata_ledger_hash_wrong_type_denies_parametrized(
    ok_verifier: _StaticVerifier, bad_pin: object
) -> None:
    result = check_rollback_script_integrity(
        **_ok_inputs(),
        signature_verify=ok_verifier,
        ledger_hash_reader=_const_ledger(_LEDGER),
        script_metadata_reader=_const_metadata({"ledger_hash_at_pin": bad_pin}),
    )
    assert result.success is False
    assert result.detail is not None
    assert result.detail.check_failed == "ledger_hash"


def test_metadata_not_dict_denies(ok_verifier: _StaticVerifier) -> None:
    def _reader(_path: str):  # type: ignore[no-untyped-def]
        return "not-a-dict"

    result = check_rollback_script_integrity(
        **_ok_inputs(),
        signature_verify=ok_verifier,
        ledger_hash_reader=_const_ledger(_LEDGER),
        script_metadata_reader=_reader,  # type: ignore[arg-type]
    )
    assert result.success is False
    assert result.detail is not None
    assert result.detail.check_failed == "ledger_hash"
    assert result.detail.reason_tag == "script_metadata_not_dict"


def test_live_ledger_hash_not_str_denies(ok_verifier: _StaticVerifier) -> None:
    def _reader():  # type: ignore[no-untyped-def]
        return 42

    result = check_rollback_script_integrity(
        **_ok_inputs(),
        signature_verify=ok_verifier,
        ledger_hash_reader=_reader,  # type: ignore[arg-type]
        script_metadata_reader=_const_metadata({"ledger_hash_at_pin": _LEDGER}),
    )
    assert result.success is False
    assert result.detail is not None
    assert result.detail.check_failed == "ledger_hash"
    assert result.detail.reason_tag == "ledger_hash_live_not_str"


# ---------------------------------------------------------------------------
# Both-failed composition
# ---------------------------------------------------------------------------


def test_both_signature_and_ledger_fail_reports_both() -> None:
    def _bad(_a: bytes, _b: bytes, _c: bytes) -> bool:
        return False

    result = check_rollback_script_integrity(
        **_ok_inputs(),
        signature_verify=_bad,
        ledger_hash_reader=_const_ledger("different"),
        script_metadata_reader=_const_metadata({"ledger_hash_at_pin": _LEDGER}),
    )
    assert result.success is False
    assert result.detail is not None
    assert result.detail.check_failed == "both"
    assert result.detail.reason_tag == "signature_and_ledger_hash_both_failed"


def test_both_failed_carries_reader_error_when_verifier_raised() -> None:
    def _raises(_a: bytes, _b: bytes, _c: bytes) -> bool:
        raise RuntimeError("verifier boom")

    result = check_rollback_script_integrity(
        **_ok_inputs(),
        signature_verify=_raises,
        ledger_hash_reader=_const_ledger("different"),
        script_metadata_reader=_const_metadata({"ledger_hash_at_pin": _LEDGER}),
    )
    assert result.success is False
    assert result.detail is not None
    assert result.detail.check_failed == "both"
    assert result.detail.reader_error is not None
    assert "signature_verify" in result.detail.reader_error
    assert "RuntimeError" in result.detail.reader_error


# ---------------------------------------------------------------------------
# Reader failures (fail-closed)
# ---------------------------------------------------------------------------


def test_signature_verify_raises_fail_closed() -> None:
    def _raises(_a: bytes, _b: bytes, _c: bytes) -> bool:
        raise ValueError("bad key")

    result = check_rollback_script_integrity(
        **_ok_inputs(),
        signature_verify=_raises,
        ledger_hash_reader=_const_ledger(_LEDGER),
        script_metadata_reader=_const_metadata({"ledger_hash_at_pin": _LEDGER}),
    )
    assert result.success is False
    assert result.detail is not None
    assert result.detail.check_failed == "signature"
    assert result.detail.reason_tag == "signature_verify_raised"
    assert result.detail.reader_error is not None
    assert "ValueError" in result.detail.reader_error


def test_ledger_hash_reader_raises_fail_closed(ok_verifier: _StaticVerifier) -> None:
    def _raises() -> str:
        raise OSError("ledger read failed")

    result = check_rollback_script_integrity(
        **_ok_inputs(),
        signature_verify=ok_verifier,
        ledger_hash_reader=_raises,
        script_metadata_reader=_const_metadata({"ledger_hash_at_pin": _LEDGER}),
    )
    assert result.success is False
    assert result.detail is not None
    assert result.detail.check_failed == "ledger_hash"
    assert result.detail.reason_tag == "ledger_hash_reader_raised"
    assert result.detail.reader_error is not None
    assert "OSError" in result.detail.reader_error


def test_script_metadata_reader_raises_fail_closed(ok_verifier: _StaticVerifier) -> None:
    def _raises(_path: str) -> dict:
        raise FileNotFoundError("metadata sidecar missing")

    result = check_rollback_script_integrity(
        **_ok_inputs(),
        signature_verify=ok_verifier,
        ledger_hash_reader=_const_ledger(_LEDGER),
        script_metadata_reader=_raises,
    )
    assert result.success is False
    assert result.detail is not None
    assert result.detail.check_failed == "ledger_hash"
    assert result.detail.reason_tag == "script_metadata_reader_raised"
    assert result.detail.reader_error is not None
    assert "FileNotFoundError" in result.detail.reader_error


@pytest.mark.parametrize(
    "exc_type",
    [ValueError, RuntimeError, TypeError, KeyError, IndexError, OSError],
)
def test_ledger_reader_raises_various_exceptions_parametrized(
    ok_verifier: _StaticVerifier, exc_type: type
) -> None:
    def _raises() -> str:
        raise exc_type("boom")

    result = check_rollback_script_integrity(
        **_ok_inputs(),
        signature_verify=ok_verifier,
        ledger_hash_reader=_raises,
        script_metadata_reader=_const_metadata({"ledger_hash_at_pin": _LEDGER}),
    )
    assert result.success is False
    assert result.detail is not None
    assert result.detail.check_failed == "ledger_hash"
    assert result.detail.reader_error is not None
    assert exc_type.__name__ in result.detail.reader_error


# ---------------------------------------------------------------------------
# Structural input validation (pre-check failures)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "bad_path", ["", None, 123, b"bytes-path", ["list"], {"dict": 1}]
)
def test_script_path_invalid_types_denies(
    ok_verifier: _StaticVerifier, bad_path: object
) -> None:
    result = check_rollback_script_integrity(
        script_path=bad_path,  # type: ignore[arg-type]
        script_bytes=_SCRIPT,
        signature=_SIG,
        public_key=_PK,
        signature_verify=ok_verifier,
        ledger_hash_reader=_const_ledger(_LEDGER),
        script_metadata_reader=_const_metadata({"ledger_hash_at_pin": _LEDGER}),
    )
    assert result.success is False
    assert result.detail is not None
    assert result.detail.reason_tag == "script_path_invalid"
    assert result.detail.check_failed == ""


@pytest.mark.parametrize("bad_bytes", ["str-not-bytes", None, 0, ["b"], bytearray(b"x")])
def test_script_bytes_not_bytes_denies(
    ok_verifier: _StaticVerifier, bad_bytes: object
) -> None:
    result = check_rollback_script_integrity(
        script_path="spike_rollback.sh",
        script_bytes=bad_bytes,  # type: ignore[arg-type]
        signature=_SIG,
        public_key=_PK,
        signature_verify=ok_verifier,
        ledger_hash_reader=_const_ledger(_LEDGER),
        script_metadata_reader=_const_metadata({"ledger_hash_at_pin": _LEDGER}),
    )
    assert result.success is False
    assert result.detail is not None
    assert result.detail.reason_tag == "script_bytes_not_bytes"


def test_signature_not_bytes_denies(ok_verifier: _StaticVerifier) -> None:
    result = check_rollback_script_integrity(
        script_path="spike_rollback.sh",
        script_bytes=_SCRIPT,
        signature="str-not-bytes",  # type: ignore[arg-type]
        public_key=_PK,
        signature_verify=ok_verifier,
        ledger_hash_reader=_const_ledger(_LEDGER),
        script_metadata_reader=_const_metadata({"ledger_hash_at_pin": _LEDGER}),
    )
    assert result.success is False
    assert result.detail is not None
    assert result.detail.reason_tag == "signature_not_bytes"


def test_public_key_not_bytes_denies(ok_verifier: _StaticVerifier) -> None:
    result = check_rollback_script_integrity(
        script_path="spike_rollback.sh",
        script_bytes=_SCRIPT,
        signature=_SIG,
        public_key="str-not-bytes",  # type: ignore[arg-type]
        signature_verify=ok_verifier,
        ledger_hash_reader=_const_ledger(_LEDGER),
        script_metadata_reader=_const_metadata({"ledger_hash_at_pin": _LEDGER}),
    )
    assert result.success is False
    assert result.detail is not None
    assert result.detail.reason_tag == "public_key_not_bytes"


# ---------------------------------------------------------------------------
# Multiple scripts parametrization
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "script_path",
    [
        "spike_rollback.sh",
        "scripts/rollbacks/en001_spike_rollback.sh",
        "scripts/rollbacks/en003_kimi_k2_rollback.sh",
        "relative/deep/nested/path/rollback.sh",
    ],
)
def test_multiple_script_paths_pass(
    ok_verifier: _StaticVerifier, script_path: str
) -> None:
    result = check_rollback_script_integrity(
        script_path=script_path,
        script_bytes=_SCRIPT,
        signature=_SIG,
        public_key=_PK,
        signature_verify=ok_verifier,
        ledger_hash_reader=_const_ledger(_LEDGER),
        script_metadata_reader=_const_metadata({"ledger_hash_at_pin": _LEDGER}),
    )
    assert result.success is True
    assert result.detail is not None
    assert result.detail.script_path == script_path


# ---------------------------------------------------------------------------
# Result shape / invariants
# ---------------------------------------------------------------------------


def test_result_is_frozen_dataclass(ok_verifier: _StaticVerifier) -> None:
    result = check_rollback_script_integrity(
        **_ok_inputs(),
        signature_verify=ok_verifier,
        ledger_hash_reader=_const_ledger(_LEDGER),
        script_metadata_reader=_const_metadata({"ledger_hash_at_pin": _LEDGER}),
    )
    with pytest.raises(Exception):
        result.success = False  # type: ignore[misc]


def test_detail_is_frozen_dataclass(ok_verifier: _StaticVerifier) -> None:
    result = check_rollback_script_integrity(
        **_ok_inputs(),
        signature_verify=ok_verifier,
        ledger_hash_reader=_const_ledger(_LEDGER),
        script_metadata_reader=_const_metadata({"ledger_hash_at_pin": _LEDGER}),
    )
    assert result.detail is not None
    with pytest.raises(Exception):
        result.detail.reason_tag = "tamper"  # type: ignore[misc]


def test_failure_code_constant_is_exported() -> None:
    assert F_AMDT_05 == "F-AMDT-05"


def test_pass_record_script_path_populated(ok_verifier: _StaticVerifier) -> None:
    result = check_rollback_script_integrity(
        **_ok_inputs(),
        signature_verify=ok_verifier,
        ledger_hash_reader=_const_ledger(_LEDGER),
        script_metadata_reader=_const_metadata({"ledger_hash_at_pin": _LEDGER}),
    )
    assert result.detail is not None
    assert result.detail.script_path == "spike_rollback.sh"


def test_signature_check_runs_even_when_ledger_would_pass() -> None:
    """Non-short-circuit guarantee: signature always checked."""
    verifier = _StaticVerifier(_SCRIPT, _SIG, _PK)
    # Make signature bytes mismatch so verifier returns False.
    wrong_sig = b"WRONG"
    result = check_rollback_script_integrity(
        script_path="spike_rollback.sh",
        script_bytes=_SCRIPT,
        signature=wrong_sig,
        public_key=_PK,
        signature_verify=verifier,
        ledger_hash_reader=_const_ledger(_LEDGER),
        script_metadata_reader=_const_metadata({"ledger_hash_at_pin": _LEDGER}),
    )
    assert result.success is False
    assert verifier.calls  # verifier was invoked


def test_ledger_check_runs_even_when_signature_failed() -> None:
    """Both checks always run — ensures the 'both' path is reachable."""
    metadata_calls: list[str] = []

    def _metadata(path: str) -> dict:
        metadata_calls.append(path)
        return {"ledger_hash_at_pin": "different"}

    def _bad_verify(_a: bytes, _b: bytes, _c: bytes) -> bool:
        return False

    result = check_rollback_script_integrity(
        **_ok_inputs(),
        signature_verify=_bad_verify,
        ledger_hash_reader=_const_ledger(_LEDGER),
        script_metadata_reader=_metadata,
    )
    assert result.success is False
    assert metadata_calls == ["spike_rollback.sh"]
    assert result.detail is not None
    assert result.detail.check_failed == "both"


def test_signature_verify_receives_exact_inputs() -> None:
    verifier = _StaticVerifier(_SCRIPT, _SIG, _PK)
    check_rollback_script_integrity(
        **_ok_inputs(),
        signature_verify=verifier,
        ledger_hash_reader=_const_ledger(_LEDGER),
        script_metadata_reader=_const_metadata({"ledger_hash_at_pin": _LEDGER}),
    )
    assert verifier.calls == [(_SCRIPT, _SIG, _PK)]
