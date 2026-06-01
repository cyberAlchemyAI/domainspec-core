"""Unit tests for F-CIC-CLC-ENUM-DRIFT.

Per architecture v7.0.8 §4.0 (LOCKED 2026-05-08, Cycle-1 RT-01 fix).
"""

from __future__ import annotations

from pipeline.logician.gates.f_cic_clc_enum_drift import GATE_ID, PRE_GATE_ORDER, run


# ---------------------------------------------------------------------------
# Reader fixtures
# ---------------------------------------------------------------------------


_FIXED_HASH = "a" * 128  # SHA3-512 hex is 128 chars


def _module_reader(content: bytes):
    def _r() -> bytes:
        return content
    return _r


def _hash_callable(out: str):
    def _r(data: bytes) -> str:
        return out
    return _r


def _canonical_hash_reader_ok():
    def _r() -> dict:
        return {
            "identity_capital_module_sha3_512": _FIXED_HASH,
            "signature_ed25519": b"sig_ed",
            "signature_ml_dsa_65": b"sig_ml",
            "signed_payload_bytes": b"payload",
            "operator_public_key_ed25519": b"pk_ed",
            "operator_public_key_ml_dsa_65": b"pk_ml",
        }
    return _r


def _canonical_hash_reader_with(expected: str):
    def _r() -> dict:
        return {
            "identity_capital_module_sha3_512": expected,
            "signature_ed25519": b"sig_ed",
            "signature_ml_dsa_65": b"sig_ml",
            "signed_payload_bytes": b"payload",
            "operator_public_key_ed25519": b"pk_ed",
            "operator_public_key_ml_dsa_65": b"pk_ml",
        }
    return _r


def _verify_signature(returns: bool):
    def _r(*args, **kwargs) -> bool:
        return returns
    return _r


def _amendment_count_reader(cic: int, clc: int):
    def _r() -> tuple[int, int]:
        return (cic, clc)
    return _r


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------


def test_gate_id() -> None:
    assert GATE_ID == "F-CIC-CLC-ENUM-DRIFT"


def test_pre_gate_order_earliest_among_cic_clc_gates() -> None:
    """Per v7.0.8 §4.4 — must fire before coupling violation (6.5)."""
    assert PRE_GATE_ORDER == 6.45
    assert PRE_GATE_ORDER < 6.5


# ---------------------------------------------------------------------------
# Happy path — everything aligned
# ---------------------------------------------------------------------------


def test_happy_path_passes() -> None:
    r = run(
        enum_module_reader=_module_reader(b"any-content"),
        canonical_hash_reader=_canonical_hash_reader_ok(),
        hash_bytes=_hash_callable(_FIXED_HASH),
        verify_hybrid_signature=_verify_signature(True),
        amendment_count_reader=_amendment_count_reader(6, 8),
    )
    assert r.passed is True
    assert r.subcodes == ()


# ---------------------------------------------------------------------------
# Hash mismatch (RT-01 primary scenario)
# ---------------------------------------------------------------------------


def test_hash_mismatch_fails() -> None:
    """Adversary edits identity_capital.py without operator re-sign."""
    r = run(
        enum_module_reader=_module_reader(b"adversary-edited"),
        canonical_hash_reader=_canonical_hash_reader_ok(),
        hash_bytes=_hash_callable("b" * 128),  # mismatched hash
        verify_hybrid_signature=_verify_signature(True),
        amendment_count_reader=_amendment_count_reader(6, 8),
    )
    assert r.passed is False
    assert f"{GATE_ID}.hash_mismatch" in r.subcodes


# ---------------------------------------------------------------------------
# Signature failure
# ---------------------------------------------------------------------------


def test_signature_invalid_fails() -> None:
    r = run(
        enum_module_reader=_module_reader(b"any-content"),
        canonical_hash_reader=_canonical_hash_reader_ok(),
        hash_bytes=_hash_callable(_FIXED_HASH),
        verify_hybrid_signature=_verify_signature(False),
        amendment_count_reader=_amendment_count_reader(6, 8),
    )
    assert r.passed is False
    assert f"{GATE_ID}.signature_invalid" in r.subcodes


def test_non_boolean_signature_treated_as_failure() -> None:
    """Per Logician design: strict ``is True`` on verifier return."""

    def _bogus_verify(*args, **kwargs):
        return 1  # truthy but not True

    r = run(
        enum_module_reader=_module_reader(b"any"),
        canonical_hash_reader=_canonical_hash_reader_ok(),
        hash_bytes=_hash_callable(_FIXED_HASH),
        verify_hybrid_signature=_bogus_verify,
        amendment_count_reader=_amendment_count_reader(6, 8),
    )
    assert r.passed is False
    assert f"{GATE_ID}.signature_invalid" in r.subcodes


# ---------------------------------------------------------------------------
# Amendment-text count drift (defends against in-code constant drift)
# ---------------------------------------------------------------------------


def test_amendment_count_cic_drift_fails() -> None:
    r = run(
        enum_module_reader=_module_reader(b"any"),
        canonical_hash_reader=_canonical_hash_reader_ok(),
        hash_bytes=_hash_callable(_FIXED_HASH),
        verify_hybrid_signature=_verify_signature(True),
        amendment_count_reader=_amendment_count_reader(7, 8),  # CIC drift
    )
    assert r.passed is False
    assert f"{GATE_ID}.amendment_count_drift" in r.subcodes


def test_amendment_count_clc_drift_fails() -> None:
    r = run(
        enum_module_reader=_module_reader(b"any"),
        canonical_hash_reader=_canonical_hash_reader_ok(),
        hash_bytes=_hash_callable(_FIXED_HASH),
        verify_hybrid_signature=_verify_signature(True),
        amendment_count_reader=_amendment_count_reader(6, 9),  # CLC drift
    )
    assert r.passed is False
    assert f"{GATE_ID}.amendment_count_drift" in r.subcodes


# ---------------------------------------------------------------------------
# Multiple subcodes aggregate
# ---------------------------------------------------------------------------


def test_multiple_failures_aggregate_subcodes() -> None:
    r = run(
        enum_module_reader=_module_reader(b"any"),
        canonical_hash_reader=_canonical_hash_reader_ok(),
        hash_bytes=_hash_callable("c" * 128),  # hash mismatch
        verify_hybrid_signature=_verify_signature(False),  # sig bad
        amendment_count_reader=_amendment_count_reader(7, 9),  # both drift
    )
    assert r.passed is False
    assert f"{GATE_ID}.hash_mismatch" in r.subcodes
    assert f"{GATE_ID}.signature_invalid" in r.subcodes
    assert f"{GATE_ID}.amendment_count_drift" in r.subcodes
