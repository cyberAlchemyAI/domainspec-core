"""Adversarial tests for F-ROLLBACK-SCRIPT-INTEGRITY (F-AMDT-05).

Attack vectors:
- Signature-verify that verifies different bytes than passed in.
- Ledger-hash prefix/suffix confusion (exact equality, not startswith).
- Homoglyph ledger-hash substitution.
- All readers raise simultaneously.
- Reader return type confusion (bool mimicking str).
- Strict `is True` identity under custom __bool__ objects.
- Exception-typed reader_error truncation.
- Script-path traversal / shell-escape patterns still pass type check.
- Metadata reader returns dict with ledger_hash_at_pin that is a bytes object
  pretending to be a string.
"""

from __future__ import annotations

import pytest

from pipeline.logician.gates.f_rollback_script_integrity import (
    F_AMDT_05,
    check_rollback_script_integrity,
)


_SCRIPT = b"#!/bin/bash\necho rollback\n"
_SIG = b"sig"
_PK = b"pk"
_LEDGER = "a" * 128  # 512-bit hex-like pin


def _ok_metadata():
    return lambda _p: {"ledger_hash_at_pin": _LEDGER}


def _ok_ledger():
    return lambda: _LEDGER


# ---------------------------------------------------------------------------
# Adversarial — verifier semantics
# ---------------------------------------------------------------------------


def test_adv_signature_valid_but_for_different_script() -> None:
    """Verifier returns True only for DIFFERENT bytes than the ones passed in;
    the gate must still DENY because ``signature_verify`` is called with the
    actual ``script_bytes``, not the bytes the adversary wants verified."""

    expected_other_bytes = b"OTHER_SCRIPT"

    def _selective(message: bytes, sig: bytes, pk: bytes) -> bool:
        # Verifier returns True only if caller passes `expected_other_bytes`.
        return (message, sig, pk) == (expected_other_bytes, _SIG, _PK)

    result = check_rollback_script_integrity(
        script_path="spike_rollback.sh",
        script_bytes=_SCRIPT,
        signature=_SIG,
        public_key=_PK,
        signature_verify=_selective,
        ledger_hash_reader=_ok_ledger(),
        script_metadata_reader=_ok_metadata(),
    )
    assert result.success is False
    assert result.failure_code == F_AMDT_05
    assert result.detail is not None
    assert result.detail.check_failed == "signature"


def test_adv_signature_verify_returns_custom_truthy_object() -> None:
    """A custom class whose __bool__ returns True must still DENY — strict
    `is True` identity, not truthy."""

    class _TruthyObject:
        def __bool__(self) -> bool:
            return True

    def _v(_a: bytes, _b: bytes, _c: bytes):  # type: ignore[no-untyped-def]
        return _TruthyObject()

    result = check_rollback_script_integrity(
        script_path="spike_rollback.sh",
        script_bytes=_SCRIPT,
        signature=_SIG,
        public_key=_PK,
        signature_verify=_v,
        ledger_hash_reader=_ok_ledger(),
        script_metadata_reader=_ok_metadata(),
    )
    assert result.success is False
    assert result.detail is not None
    assert result.detail.check_failed == "signature"


# ---------------------------------------------------------------------------
# Adversarial — ledger-hash semantics
# ---------------------------------------------------------------------------


def test_adv_ledger_hash_is_prefix_match_not_exact() -> None:
    """Live ledger hash is a proper prefix of the pinned hash → DENY.
    Verifies the gate uses exact equality, not ``startswith``."""

    def _verify(_a: bytes, _b: bytes, _c: bytes) -> bool:
        return True

    prefix = _LEDGER[:64]
    result = check_rollback_script_integrity(
        script_path="spike_rollback.sh",
        script_bytes=_SCRIPT,
        signature=_SIG,
        public_key=_PK,
        signature_verify=_verify,
        ledger_hash_reader=lambda: prefix,
        script_metadata_reader=_ok_metadata(),
    )
    assert result.success is False
    assert result.detail is not None
    assert result.detail.check_failed == "ledger_hash"


def test_adv_ledger_hash_trailing_whitespace_denies() -> None:
    """Whitespace-trimmed match attack: live hash has trailing whitespace."""

    def _verify(_a: bytes, _b: bytes, _c: bytes) -> bool:
        return True

    result = check_rollback_script_integrity(
        script_path="spike_rollback.sh",
        script_bytes=_SCRIPT,
        signature=_SIG,
        public_key=_PK,
        signature_verify=_verify,
        ledger_hash_reader=lambda: _LEDGER + "\n",
        script_metadata_reader=_ok_metadata(),
    )
    assert result.success is False
    assert result.detail is not None
    assert result.detail.check_failed == "ledger_hash"


def test_adv_ledger_hash_case_difference_denies() -> None:
    """Hex-case-folding attack: live hash is uppercase, pin is lowercase."""

    def _verify(_a: bytes, _b: bytes, _c: bytes) -> bool:
        return True

    upper = _LEDGER.upper()
    lower = _LEDGER.lower()
    assert upper != lower  # ensure the attack condition is meaningful
    result = check_rollback_script_integrity(
        script_path="spike_rollback.sh",
        script_bytes=_SCRIPT,
        signature=_SIG,
        public_key=_PK,
        signature_verify=_verify,
        ledger_hash_reader=lambda: upper,
        script_metadata_reader=lambda _p: {"ledger_hash_at_pin": lower},
    )
    # _LEDGER is all 'a's; upper and lower differ → mismatch expected.
    assert result.success is False
    assert result.detail is not None
    assert result.detail.check_failed == "ledger_hash"


def test_adv_ledger_hash_homoglyph_substitution_denies() -> None:
    """Pinned hash contains Latin 'a'; live hash substitutes Cyrillic 'а'
    (U+0430). Byte-identity comparison must reject."""

    def _verify(_a: bytes, _b: bytes, _c: bytes) -> bool:
        return True

    latin = "a" * 64
    cyrillic = "\u0430" * 64
    result = check_rollback_script_integrity(
        script_path="spike_rollback.sh",
        script_bytes=_SCRIPT,
        signature=_SIG,
        public_key=_PK,
        signature_verify=_verify,
        ledger_hash_reader=lambda: cyrillic,
        script_metadata_reader=lambda _p: {"ledger_hash_at_pin": latin},
    )
    assert result.success is False
    assert result.detail is not None
    assert result.detail.check_failed == "ledger_hash"


# ---------------------------------------------------------------------------
# Adversarial — reader raises
# ---------------------------------------------------------------------------


def test_adv_all_readers_raise_simultaneously_denies() -> None:
    def _verify_raises(_a: bytes, _b: bytes, _c: bytes) -> bool:
        raise RuntimeError("verifier nuked")

    def _ledger_raises() -> str:
        raise OSError("ledger nuked")

    def _metadata_raises(_p: str) -> dict:
        raise FileNotFoundError("metadata nuked")

    result = check_rollback_script_integrity(
        script_path="spike_rollback.sh",
        script_bytes=_SCRIPT,
        signature=_SIG,
        public_key=_PK,
        signature_verify=_verify_raises,
        ledger_hash_reader=_ledger_raises,
        script_metadata_reader=_metadata_raises,
    )
    assert result.success is False
    assert result.failure_code == F_AMDT_05
    assert result.detail is not None
    assert result.detail.check_failed == "both"
    assert result.detail.reader_error is not None
    # The combined reader_error must carry SOMETHING useful; spec says
    # signature_reader_error takes priority in the "both" case.
    assert "signature_verify" in result.detail.reader_error


def test_adv_ledger_reader_raises_after_metadata_ok_denies() -> None:
    """Metadata read succeeds, ledger read raises. Must FAIL fail-closed on
    ledger side."""

    def _verify(_a: bytes, _b: bytes, _c: bytes) -> bool:
        return True

    def _ledger_raises() -> str:
        raise PermissionError("no read")

    result = check_rollback_script_integrity(
        script_path="spike_rollback.sh",
        script_bytes=_SCRIPT,
        signature=_SIG,
        public_key=_PK,
        signature_verify=_verify,
        ledger_hash_reader=_ledger_raises,
        script_metadata_reader=_ok_metadata(),
    )
    assert result.success is False
    assert result.detail is not None
    assert result.detail.check_failed == "ledger_hash"
    assert result.detail.reason_tag == "ledger_hash_reader_raised"
    assert result.detail.reader_error is not None
    assert "PermissionError" in result.detail.reader_error


# ---------------------------------------------------------------------------
# Adversarial — reader return type confusion
# ---------------------------------------------------------------------------


def test_adv_ledger_reader_returns_subclass_of_str_accepted() -> None:
    """A subclass of str IS a str via isinstance — must accept iff content
    matches. This is actually a PASS case demonstrating the type check is
    isinstance-based, not strict identity."""

    class _MyStr(str):
        pass

    def _verify(_a: bytes, _b: bytes, _c: bytes) -> bool:
        return True

    result = check_rollback_script_integrity(
        script_path="spike_rollback.sh",
        script_bytes=_SCRIPT,
        signature=_SIG,
        public_key=_PK,
        signature_verify=_verify,
        ledger_hash_reader=lambda: _MyStr(_LEDGER),
        script_metadata_reader=_ok_metadata(),
    )
    assert result.success is True


def test_adv_metadata_ledger_hash_at_pin_is_bytes_denies() -> None:
    """bytes is not str — even if byte-decodes to the live hex, must DENY."""

    def _verify(_a: bytes, _b: bytes, _c: bytes) -> bool:
        return True

    result = check_rollback_script_integrity(
        script_path="spike_rollback.sh",
        script_bytes=_SCRIPT,
        signature=_SIG,
        public_key=_PK,
        signature_verify=_verify,
        ledger_hash_reader=_ok_ledger(),
        script_metadata_reader=lambda _p: {"ledger_hash_at_pin": _LEDGER.encode()},
    )
    assert result.success is False
    assert result.detail is not None
    assert result.detail.check_failed == "ledger_hash"
    assert result.detail.reason_tag == "ledger_hash_at_pin_missing_or_empty"


# ---------------------------------------------------------------------------
# Adversarial — script_path adversarial content
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "traversal_path",
    [
        "../../etc/passwd",
        "/etc/passwd",
        "spike_rollback.sh; rm -rf /",
        "spike_rollback.sh\x00hidden",
        "spike_rollback.sh\nscript-injection",
    ],
)
def test_adv_script_path_traversal_patterns_reach_gate_intact(
    traversal_path: str,
) -> None:
    """The gate does not sanitize script_path — it is a string token passed
    through to the metadata reader. The reader is responsible for refusing
    paths it cannot verify. For gate correctness we only verify the string
    is preserved and the metadata reader receives it verbatim."""

    received: list[str] = []

    def _meta(p: str) -> dict:
        received.append(p)
        return {"ledger_hash_at_pin": _LEDGER}

    def _verify(_a: bytes, _b: bytes, _c: bytes) -> bool:
        return True

    check_rollback_script_integrity(
        script_path=traversal_path,
        script_bytes=_SCRIPT,
        signature=_SIG,
        public_key=_PK,
        signature_verify=_verify,
        ledger_hash_reader=_ok_ledger(),
        script_metadata_reader=_meta,
    )
    assert received == [traversal_path]


# ---------------------------------------------------------------------------
# Adversarial — reader_error truncation
# ---------------------------------------------------------------------------


def test_adv_reader_error_truncated_at_500_chars() -> None:
    """An exception message longer than 500 chars must be truncated in
    ``reader_error`` to prevent log-flooding."""

    big_message = "X" * 10_000

    def _verify_raises(_a: bytes, _b: bytes, _c: bytes) -> bool:
        raise RuntimeError(big_message)

    result = check_rollback_script_integrity(
        script_path="spike_rollback.sh",
        script_bytes=_SCRIPT,
        signature=_SIG,
        public_key=_PK,
        signature_verify=_verify_raises,
        ledger_hash_reader=_ok_ledger(),
        script_metadata_reader=_ok_metadata(),
    )
    assert result.success is False
    assert result.detail is not None
    assert result.detail.reader_error is not None
    # "signature_verify: RuntimeError: X...X" — total must be ≤ 500 chars
    # including the "signature_verify: " prefix.
    assert len(result.detail.reader_error) <= 500 + len("signature_verify: ")


# ---------------------------------------------------------------------------
# Adversarial — isolation of checks
# ---------------------------------------------------------------------------


def test_adv_ledger_check_does_not_leak_signature_state() -> None:
    """A signature PASS must not affect ledger evaluation, and vice versa."""

    # Signature verifier passes.
    def _verify(_a: bytes, _b: bytes, _c: bytes) -> bool:
        return True

    # Ledger mismatch — must DENY with ledger_hash, never with signature.
    result = check_rollback_script_integrity(
        script_path="spike_rollback.sh",
        script_bytes=_SCRIPT,
        signature=_SIG,
        public_key=_PK,
        signature_verify=_verify,
        ledger_hash_reader=lambda: "x" * 128,
        script_metadata_reader=_ok_metadata(),
    )
    assert result.success is False
    assert result.detail is not None
    assert result.detail.check_failed == "ledger_hash"


def test_adv_metadata_with_extra_ledger_hash_at_pin_whitespace_denies() -> None:
    """A pin with trailing whitespace is NOT equal to the live hash → DENY."""

    def _verify(_a: bytes, _b: bytes, _c: bytes) -> bool:
        return True

    result = check_rollback_script_integrity(
        script_path="spike_rollback.sh",
        script_bytes=_SCRIPT,
        signature=_SIG,
        public_key=_PK,
        signature_verify=_verify,
        ledger_hash_reader=lambda: _LEDGER,
        script_metadata_reader=lambda _p: {"ledger_hash_at_pin": _LEDGER + " "},
    )
    assert result.success is False
    assert result.detail is not None
    assert result.detail.check_failed == "ledger_hash"
