"""Unit tests for F-KFR-SIGNATURE-INVALID + F-KFR-AUDIT-CHAIN-BROKEN (PRE-load).

Per architecture v7.0.4 §1.1 (RT-07 closure).
"""

from __future__ import annotations

from pipeline.logician.gates.f_kfr_signature_validation import (
    AUDIT_CHAIN_KIND_INITIAL,
    AUDIT_CHAIN_KIND_SP0_REVIEW,
    F_KFR_AUDIT_CHAIN_BROKEN,
    F_KFR_SIGNATURE_INVALID,
    KEY_ROTATION_MARKER_KIND,
    KeyringEntry,
    check_kfr_audit_chain_broken,
    check_kfr_signature_invalid,
)


def _accept_for_pubkey(target: bytes):
    def _verify(message: bytes, signature: bytes, public_key: bytes) -> bool:
        return public_key == target
    return _verify


# --------------------------------------------------------------------------
# F-KFR-SIGNATURE-INVALID
# --------------------------------------------------------------------------

def test_signature_invalid_failure_code_constant() -> None:
    assert F_KFR_SIGNATURE_INVALID == "F-KFR-SIGNATURE-INVALID"


def test_active_key_with_valid_signature_passes() -> None:
    keyring = [KeyringEntry(
        key_id="ed25519:active-1",
        public_key=b"active-pub",
        is_active=True,
    )]
    r = check_kfr_signature_invalid(
        fact_id="enrollment_fy25",
        confirmed_by_key_id="ed25519:active-1",
        confirmation_message_bytes=b"fact body bytes",
        confirmation_signature=b"sig",
        keyring=keyring,
        signature_verify=_accept_for_pubkey(b"active-pub"),
    )
    assert r.success is True
    assert r.fact_id == "enrollment_fy25"


def test_unknown_key_id_fails() -> None:
    r = check_kfr_signature_invalid(
        fact_id="x",
        confirmed_by_key_id="ed25519:ghost",
        confirmation_message_bytes=b"x",
        confirmation_signature=b"x",
        keyring=[],
        signature_verify=_accept_for_pubkey(b"any"),
    )
    assert r.success is False
    assert r.failure_code == F_KFR_SIGNATURE_INVALID
    assert "not present" in r.detail


def test_retired_key_fails() -> None:
    keyring = [KeyringEntry(
        key_id="ed25519:retired",
        public_key=b"old-pub",
        is_active=False,
        retired_at_utc="2026-01-01T00:00:00Z",
    )]
    r = check_kfr_signature_invalid(
        fact_id="x",
        confirmed_by_key_id="ed25519:retired",
        confirmation_message_bytes=b"x",
        confirmation_signature=b"x",
        keyring=keyring,
        signature_verify=_accept_for_pubkey(b"old-pub"),
    )
    assert r.success is False
    assert r.failure_code == F_KFR_SIGNATURE_INVALID
    assert "retired" in r.detail


def test_signature_verification_failure_fails() -> None:
    keyring = [KeyringEntry(
        key_id="ed25519:active",
        public_key=b"pub",
        is_active=True,
    )]
    r = check_kfr_signature_invalid(
        fact_id="x",
        confirmed_by_key_id="ed25519:active",
        confirmation_message_bytes=b"x",
        confirmation_signature=b"x",
        keyring=keyring,
        signature_verify=lambda *_a, **_kw: False,
    )
    assert r.success is False
    assert r.failure_code == F_KFR_SIGNATURE_INVALID


def test_empty_key_id_fails() -> None:
    r = check_kfr_signature_invalid(
        fact_id="x",
        confirmed_by_key_id="   ",
        confirmation_message_bytes=b"x",
        confirmation_signature=b"x",
        keyring=[],
        signature_verify=lambda *_a, **_kw: True,
    )
    assert r.success is False
    assert r.failure_code == F_KFR_SIGNATURE_INVALID
    assert "empty" in r.detail


def test_signature_verify_raising_fails_closed() -> None:
    keyring = [KeyringEntry(
        key_id="k",
        public_key=b"pub",
        is_active=True,
    )]
    def raising(*_a: object, **_kw: object) -> bool:
        raise ValueError("crypto subsystem down")

    r = check_kfr_signature_invalid(
        fact_id="x",
        confirmed_by_key_id="k",
        confirmation_message_bytes=b"x",
        confirmation_signature=b"x",
        keyring=keyring,
        signature_verify=raising,
    )
    assert r.success is False
    assert r.failure_code == F_KFR_SIGNATURE_INVALID
    assert "ValueError" in r.detail


def test_signature_verify_called_with_correct_public_key() -> None:
    captured: list[bytes] = []
    keyring = [KeyringEntry(
        key_id="k",
        public_key=b"the-real-pub",
        is_active=True,
    )]
    def capturing(message: bytes, signature: bytes, public_key: bytes) -> bool:
        captured.append(public_key)
        return True

    check_kfr_signature_invalid(
        fact_id="x",
        confirmed_by_key_id="k",
        confirmation_message_bytes=b"msg",
        confirmation_signature=b"sig",
        keyring=keyring,
        signature_verify=capturing,
    )
    assert captured == [b"the-real-pub"]


# --------------------------------------------------------------------------
# F-KFR-AUDIT-CHAIN-BROKEN
# --------------------------------------------------------------------------

def test_audit_chain_failure_code_constant() -> None:
    assert F_KFR_AUDIT_CHAIN_BROKEN == "F-KFR-AUDIT-CHAIN-BROKEN"


def test_well_formed_audit_chain_passes() -> None:
    keyring = [KeyringEntry(
        key_id="k1",
        public_key=b"pk",
        is_active=True,
    )]
    chain = [
        {
            "kind": AUDIT_CHAIN_KIND_INITIAL,
            "signed_at_utc": "2026-01-01T00:00:00Z",
            "signing_key_id": "k1",
        },
        {
            "kind": AUDIT_CHAIN_KIND_SP0_REVIEW,
            "signed_at_utc": "2026-03-15T12:00:00Z",
            "signing_key_id": "k1",
        },
        {
            "kind": AUDIT_CHAIN_KIND_SP0_REVIEW,
            "signed_at_utc": "2026-04-20T09:00:00Z",
            "signing_key_id": "k1",
        },
    ]
    r = check_kfr_audit_chain_broken(
        fact_id="enrollment",
        audit_chain=chain,
        keyring=keyring,
    )
    assert r.success is True


def test_empty_audit_chain_fails() -> None:
    r = check_kfr_audit_chain_broken(
        fact_id="x",
        audit_chain=[],
        keyring=[],
    )
    assert r.success is False
    assert r.failure_code == F_KFR_AUDIT_CHAIN_BROKEN
    assert "empty" in r.detail


def test_missing_initial_population_fails() -> None:
    chain = [
        {
            "kind": AUDIT_CHAIN_KIND_SP0_REVIEW,
            "signed_at_utc": "2026-03-01T00:00:00Z",
        },
    ]
    r = check_kfr_audit_chain_broken(
        fact_id="x",
        audit_chain=chain,
        keyring=[],
    )
    assert r.success is False
    assert r.failure_code == F_KFR_AUDIT_CHAIN_BROKEN
    assert "initial-population" in r.detail or "initial_population" in r.detail


def test_non_monotonic_sp0_timestamps_fail() -> None:
    keyring = [KeyringEntry(key_id="k", public_key=b"p", is_active=True)]
    chain = [
        {
            "kind": AUDIT_CHAIN_KIND_INITIAL,
            "signed_at_utc": "2026-01-01T00:00:00Z",
            "signing_key_id": "k",
        },
        {
            "kind": AUDIT_CHAIN_KIND_SP0_REVIEW,
            "signed_at_utc": "2026-04-01T00:00:00Z",
            "signing_key_id": "k",
        },
        {
            "kind": AUDIT_CHAIN_KIND_SP0_REVIEW,
            "signed_at_utc": "2026-02-15T00:00:00Z",  # earlier than prior
            "signing_key_id": "k",
        },
    ]
    r = check_kfr_audit_chain_broken(
        fact_id="x",
        audit_chain=chain,
        keyring=keyring,
    )
    assert r.success is False
    assert r.failure_code == F_KFR_AUDIT_CHAIN_BROKEN
    assert "non-monotonic" in r.detail


def test_retired_key_without_rotation_marker_fails() -> None:
    keyring = [
        KeyringEntry(
            key_id="k_retired",
            public_key=b"old",
            is_active=False,
            retired_at_utc="2026-02-01T00:00:00Z",
        ),
        KeyringEntry(key_id="k_active", public_key=b"new", is_active=True),
    ]
    chain = [
        {
            "kind": AUDIT_CHAIN_KIND_INITIAL,
            "signed_at_utc": "2026-01-01T00:00:00Z",
            "signing_key_id": "k_retired",
        },
    ]
    r = check_kfr_audit_chain_broken(
        fact_id="x",
        audit_chain=chain,
        keyring=keyring,
    )
    assert r.success is False
    assert r.failure_code == F_KFR_AUDIT_CHAIN_BROKEN
    assert "retired" in r.detail


def test_retired_key_with_rotation_marker_passes() -> None:
    keyring = [
        KeyringEntry(
            key_id="k_retired",
            public_key=b"old",
            is_active=False,
        ),
    ]
    chain = [
        {
            "kind": AUDIT_CHAIN_KIND_INITIAL,
            "signed_at_utc": "2026-01-01T00:00:00Z",
            "signing_key_id": "k_retired",
        },
        {
            "kind": KEY_ROTATION_MARKER_KIND,
            "retired_key_id": "k_retired",
            "operator_confirmed_at_utc": "2026-03-01T00:00:00Z",
        },
    ]
    r = check_kfr_audit_chain_broken(
        fact_id="x",
        audit_chain=chain,
        keyring=keyring,
    )
    assert r.success is True


def test_unknown_signing_key_in_chain_fails() -> None:
    chain = [
        {
            "kind": AUDIT_CHAIN_KIND_INITIAL,
            "signed_at_utc": "2026-01-01T00:00:00Z",
            "signing_key_id": "ed25519:never-issued",
        },
    ]
    r = check_kfr_audit_chain_broken(
        fact_id="x",
        audit_chain=chain,
        keyring=[],
    )
    assert r.success is False
    assert r.failure_code == F_KFR_AUDIT_CHAIN_BROKEN
    assert "unknown" in r.detail


def test_unrecognized_audit_chain_kind_fails() -> None:
    chain = [
        {
            "kind": AUDIT_CHAIN_KIND_INITIAL,
            "signed_at_utc": "2026-01-01T00:00:00Z",
        },
        {
            "kind": "operator_signature_at_invented_event",
            "signed_at_utc": "2026-02-01T00:00:00Z",
        },
    ]
    r = check_kfr_audit_chain_broken(
        fact_id="x",
        audit_chain=chain,
        keyring=[],
    )
    assert r.success is False
    assert r.failure_code == F_KFR_AUDIT_CHAIN_BROKEN
    assert "unrecognized" in r.detail


def test_sp0_row_with_empty_timestamp_fails() -> None:
    chain = [
        {
            "kind": AUDIT_CHAIN_KIND_INITIAL,
            "signed_at_utc": "2026-01-01T00:00:00Z",
        },
        {
            "kind": AUDIT_CHAIN_KIND_SP0_REVIEW,
            "signed_at_utc": "   ",
        },
    ]
    r = check_kfr_audit_chain_broken(
        fact_id="x",
        audit_chain=chain,
        keyring=[],
    )
    assert r.success is False
    assert r.failure_code == F_KFR_AUDIT_CHAIN_BROKEN
    assert "signed_at_utc" in r.detail
