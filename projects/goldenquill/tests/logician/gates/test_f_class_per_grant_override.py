"""Unit tests for F-CLASS-PER-GRANT-OVERRIDE-UNSIGNED (PRE per-grant)."""

from __future__ import annotations

from pipeline.logician.gates.f_class_per_grant_override import (
    F_CLASS_PER_GRANT_OVERRIDE_UNSIGNED,
    PER_GRANT_SP0_SIGNATURE_KEY,
    check_class_per_grant_override_unsigned,
)


def _accept_for_pubkey(target: bytes):
    def _verify(message: bytes, signature: bytes, public_key: bytes) -> bool:
        return public_key == target
    return _verify


def test_failure_code_constant() -> None:
    assert F_CLASS_PER_GRANT_OVERRIDE_UNSIGNED == (
        "F-CLASS-PER-GRANT-OVERRIDE-UNSIGNED"
    )


def test_no_override_block_passes() -> None:
    r = check_class_per_grant_override_unsigned(
        grant_id="rfa_hash_001",
        grant_override_block=None,
        override_canonical_bytes=b"",
        signing_public_key=b"pinned",
        signature_verify=_accept_for_pubkey(b"pinned"),
    )
    assert r.success is True
    assert r.grant_id == "rfa_hash_001"


def test_signed_override_passes() -> None:
    block = {
        "fields_overridden": [
            {
                "field_path": "org.budget_detail",
                "class_for_this_grant": "confidential",
            }
        ],
        PER_GRANT_SP0_SIGNATURE_KEY: b"\x01\x02\x03",
    }
    r = check_class_per_grant_override_unsigned(
        grant_id="rfa_hash_002",
        grant_override_block=block,
        override_canonical_bytes=b"canonical",
        signing_public_key=b"pinned",
        signature_verify=_accept_for_pubkey(b"pinned"),
    )
    assert r.success is True


def test_missing_signature_fails() -> None:
    r = check_class_per_grant_override_unsigned(
        grant_id="rfa_hash_003",
        grant_override_block={"fields_overridden": []},
        override_canonical_bytes=b"x",
        signing_public_key=b"x",
        signature_verify=_accept_for_pubkey(b"x"),
    )
    assert r.success is False
    assert r.failure_code == F_CLASS_PER_GRANT_OVERRIDE_UNSIGNED
    assert PER_GRANT_SP0_SIGNATURE_KEY in r.detail


def test_empty_signature_fails() -> None:
    r = check_class_per_grant_override_unsigned(
        grant_id="rfa_hash_004",
        grant_override_block={PER_GRANT_SP0_SIGNATURE_KEY: b""},
        override_canonical_bytes=b"x",
        signing_public_key=b"x",
        signature_verify=_accept_for_pubkey(b"x"),
    )
    assert r.success is False


def test_non_bytes_signature_fails() -> None:
    r = check_class_per_grant_override_unsigned(
        grant_id="rfa_hash_005",
        grant_override_block={PER_GRANT_SP0_SIGNATURE_KEY: "string-sig"},
        override_canonical_bytes=b"x",
        signing_public_key=b"x",
        signature_verify=_accept_for_pubkey(b"x"),
    )
    assert r.success is False


def test_signature_verify_returns_false_fails() -> None:
    r = check_class_per_grant_override_unsigned(
        grant_id="rfa_hash_006",
        grant_override_block={PER_GRANT_SP0_SIGNATURE_KEY: b"sig"},
        override_canonical_bytes=b"canonical",
        signing_public_key=b"wrong-key",
        signature_verify=_accept_for_pubkey(b"right-key"),
    )
    assert r.success is False
    assert "verification" in r.detail


def test_signature_verify_raises_fails() -> None:
    def boom(*_a, **_kw) -> bool:
        raise ValueError("malformed sig")

    r = check_class_per_grant_override_unsigned(
        grant_id="rfa_hash_007",
        grant_override_block={PER_GRANT_SP0_SIGNATURE_KEY: b"sig"},
        override_canonical_bytes=b"x",
        signing_public_key=b"x",
        signature_verify=boom,
    )
    assert r.success is False
    assert "ValueError" in r.detail


def test_non_mapping_block_fails() -> None:
    r = check_class_per_grant_override_unsigned(
        grant_id="rfa_hash_008",
        grant_override_block="not a mapping",  # type: ignore[arg-type]
        override_canonical_bytes=b"x",
        signing_public_key=b"x",
        signature_verify=_accept_for_pubkey(b"x"),
    )
    assert r.success is False


def test_signature_returns_truthy_non_true_fails() -> None:
    def returns_one(*_a, **_kw):
        return 1  # truthy but not True

    r = check_class_per_grant_override_unsigned(
        grant_id="rfa_hash_009",
        grant_override_block={PER_GRANT_SP0_SIGNATURE_KEY: b"sig"},
        override_canonical_bytes=b"x",
        signing_public_key=b"x",
        signature_verify=returns_one,
    )
    assert r.success is False
