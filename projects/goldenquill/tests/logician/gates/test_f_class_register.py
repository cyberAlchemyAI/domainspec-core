"""Unit tests for F-CLASS-REGISTER-* sub-codes (PRE-onboarding + PRE-cycle).

Per architecture v7.0.7 §5.1.
"""

from __future__ import annotations

from pipeline.logician.gates.f_class_register import (
    F_CLASS_REGISTER_HASH_MISMATCH,
    F_CLASS_REGISTER_MISSING,
    F_CLASS_REGISTER_SIGNATURE_INVALID,
    F_CLASS_REGISTER_UNSIGNED,
    SIGN_OFF_HASH_CLASS_KEY,
    SIGN_OFF_HASH_FIELDS_KEY,
    SIGN_OFF_KEY,
    check_class_register_hash_mismatch,
    check_class_register_missing,
    check_class_register_signature_invalid,
    check_class_register_unsigned,
)


# ---------------------------------------------------------------------------
# F-CLASS-REGISTER-MISSING
# ---------------------------------------------------------------------------


def test_register_missing_failure_code_constant() -> None:
    assert F_CLASS_REGISTER_MISSING == "F-CLASS-REGISTER-MISSING"


def test_register_present_passes() -> None:
    r = check_class_register_missing(
        register_path="vault_shared/classification/register.yaml",
        file_exists=lambda _p: True,
    )
    assert r.success is True
    assert r.failure_code is None
    assert r.register_path == "vault_shared/classification/register.yaml"


def test_register_absent_fails() -> None:
    r = check_class_register_missing(
        register_path="orgs/missing/vault/classification/register.yaml",
        file_exists=lambda _p: False,
    )
    assert r.success is False
    assert r.failure_code == F_CLASS_REGISTER_MISSING
    assert "not found" in r.detail


def test_register_path_empty_fails() -> None:
    r = check_class_register_missing(
        register_path="",
        file_exists=lambda _p: True,
    )
    assert r.success is False
    assert r.failure_code == F_CLASS_REGISTER_MISSING
    assert "empty" in r.detail


def test_register_path_whitespace_only_fails() -> None:
    r = check_class_register_missing(
        register_path="   ",
        file_exists=lambda _p: True,
    )
    assert r.success is False
    assert r.failure_code == F_CLASS_REGISTER_MISSING


def test_register_file_exists_raises_fails() -> None:
    def boom(_p: str) -> bool:
        raise PermissionError("denied")

    r = check_class_register_missing(
        register_path="vault_shared/classification/register.yaml",
        file_exists=boom,
    )
    assert r.success is False
    assert r.failure_code == F_CLASS_REGISTER_MISSING
    assert "PermissionError" in r.detail


# ---------------------------------------------------------------------------
# F-CLASS-REGISTER-UNSIGNED
# ---------------------------------------------------------------------------


def _signed_block() -> dict:
    return {
        "signed_at_iso8601": "2026-05-10T12:00:00Z",
        "signing_key_id": "ed25519:operator-1",
        "signature": b"\x01\x02\x03\x04",
        SIGN_OFF_HASH_FIELDS_KEY: "0123456789abcdef",
        SIGN_OFF_HASH_CLASS_KEY: "fedcba9876543210",
    }


def test_register_unsigned_failure_code_constant() -> None:
    assert F_CLASS_REGISTER_UNSIGNED == "F-CLASS-REGISTER-UNSIGNED"


def test_signed_register_passes() -> None:
    r = check_class_register_unsigned(
        register={SIGN_OFF_KEY: _signed_block()},
        register_path="path/to/register.yaml",
    )
    assert r.success is True
    assert r.failure_code is None


def test_register_missing_signoff_block_fails() -> None:
    r = check_class_register_unsigned(register={"some_other_key": "value"})
    assert r.success is False
    assert r.failure_code == F_CLASS_REGISTER_UNSIGNED
    assert SIGN_OFF_KEY in r.detail


def test_register_signoff_non_mapping_fails() -> None:
    r = check_class_register_unsigned(register={SIGN_OFF_KEY: "string instead"})
    assert r.success is False
    assert r.failure_code == F_CLASS_REGISTER_UNSIGNED


def test_register_empty_signature_bytes_fails() -> None:
    block = _signed_block()
    block["signature"] = b""
    r = check_class_register_unsigned(register={SIGN_OFF_KEY: block})
    assert r.success is False
    assert r.failure_code == F_CLASS_REGISTER_UNSIGNED


def test_register_non_bytes_signature_fails() -> None:
    block = _signed_block()
    block["signature"] = "looks-like-hex-but-is-string"
    r = check_class_register_unsigned(register={SIGN_OFF_KEY: block})
    assert r.success is False
    assert r.failure_code == F_CLASS_REGISTER_UNSIGNED


def test_register_missing_signed_at_fails() -> None:
    block = _signed_block()
    del block["signed_at_iso8601"]
    r = check_class_register_unsigned(register={SIGN_OFF_KEY: block})
    assert r.success is False
    assert r.failure_code == F_CLASS_REGISTER_UNSIGNED


def test_register_blank_signed_at_fails() -> None:
    block = _signed_block()
    block["signed_at_iso8601"] = "   "
    r = check_class_register_unsigned(register={SIGN_OFF_KEY: block})
    assert r.success is False


# ---------------------------------------------------------------------------
# F-CLASS-REGISTER-SIGNATURE-INVALID
# ---------------------------------------------------------------------------


def _accept_for_pubkey(target: bytes):
    def _verify(message: bytes, signature: bytes, public_key: bytes) -> bool:
        return public_key == target
    return _verify


def test_register_signature_invalid_constant() -> None:
    assert F_CLASS_REGISTER_SIGNATURE_INVALID == (
        "F-CLASS-REGISTER-SIGNATURE-INVALID"
    )


def test_register_signature_verifies_passes() -> None:
    r = check_class_register_signature_invalid(
        register={SIGN_OFF_KEY: _signed_block()},
        signed_message_bytes=b"canonical message",
        signing_public_key=b"pinned-pub",
        signature_verify=_accept_for_pubkey(b"pinned-pub"),
    )
    assert r.success is True


def test_register_signature_wrong_key_fails() -> None:
    r = check_class_register_signature_invalid(
        register={SIGN_OFF_KEY: _signed_block()},
        signed_message_bytes=b"canonical message",
        signing_public_key=b"wrong-pub",
        signature_verify=_accept_for_pubkey(b"pinned-pub"),
    )
    assert r.success is False
    assert r.failure_code == F_CLASS_REGISTER_SIGNATURE_INVALID
    assert "verification" in r.detail


def test_register_signature_verify_raises_fails() -> None:
    def boom(*_args, **_kw) -> bool:
        raise ValueError("bad signature shape")

    r = check_class_register_signature_invalid(
        register={SIGN_OFF_KEY: _signed_block()},
        signed_message_bytes=b"x",
        signing_public_key=b"x",
        signature_verify=boom,
    )
    assert r.success is False
    assert "ValueError" in r.detail


def test_register_signature_signoff_missing_fails() -> None:
    r = check_class_register_signature_invalid(
        register={"foo": "bar"},
        signed_message_bytes=b"x",
        signing_public_key=b"x",
        signature_verify=_accept_for_pubkey(b"x"),
    )
    assert r.success is False
    assert r.failure_code == F_CLASS_REGISTER_SIGNATURE_INVALID


def test_register_signature_returns_non_true_fails() -> None:
    # Verifier returns 1 (truthy but not True) — should fail by identity check.
    def returns_int(*_a, **_kw):
        return 1

    r = check_class_register_signature_invalid(
        register={SIGN_OFF_KEY: _signed_block()},
        signed_message_bytes=b"x",
        signing_public_key=b"x",
        signature_verify=returns_int,
    )
    assert r.success is False


# ---------------------------------------------------------------------------
# F-CLASS-REGISTER-HASH-MISMATCH
# ---------------------------------------------------------------------------


def test_register_hash_mismatch_constant() -> None:
    assert F_CLASS_REGISTER_HASH_MISMATCH == "F-CLASS-REGISTER-HASH-MISMATCH"


def test_register_hash_matches_passes() -> None:
    fields_full_hash = "0123456789abcdef" + "0" * 112
    class_full_hash = "fedcba9876543210" + "0" * 112

    def hash_bytes(b: bytes) -> str:
        if b == b"fields-bytes":
            return fields_full_hash
        if b == b"class-bytes":
            return class_full_hash
        return "0" * 128

    block = _signed_block()
    block[SIGN_OFF_HASH_FIELDS_KEY] = "0123456789abcdef"
    block[SIGN_OFF_HASH_CLASS_KEY] = "fedcba9876543210"

    r = check_class_register_hash_mismatch(
        register={SIGN_OFF_KEY: block},
        field_classifications_canonical_bytes=b"fields-bytes",
        class_definitions_canonical_bytes=b"class-bytes",
        hash_bytes=hash_bytes,
    )
    assert r.success is True


def test_register_hash_field_drift_fails() -> None:
    def hash_bytes(_b: bytes) -> str:
        return "deadbeefdeadbeef" + "0" * 112

    r = check_class_register_hash_mismatch(
        register={SIGN_OFF_KEY: _signed_block()},
        field_classifications_canonical_bytes=b"x",
        class_definitions_canonical_bytes=b"y",
        hash_bytes=hash_bytes,
    )
    assert r.success is False
    assert r.failure_code == F_CLASS_REGISTER_HASH_MISMATCH
    assert "field_classifications" in r.detail


def test_register_hash_class_drift_fails() -> None:
    fields_full_hash = "0123456789abcdef" + "0" * 112

    def hash_bytes(b: bytes) -> str:
        if b == b"fields-bytes":
            return fields_full_hash
        return "deadbeefdeadbeef" + "0" * 112

    block = _signed_block()
    block[SIGN_OFF_HASH_FIELDS_KEY] = "0123456789abcdef"
    block[SIGN_OFF_HASH_CLASS_KEY] = "fedcba9876543210"

    r = check_class_register_hash_mismatch(
        register={SIGN_OFF_KEY: block},
        field_classifications_canonical_bytes=b"fields-bytes",
        class_definitions_canonical_bytes=b"class-bytes",
        hash_bytes=hash_bytes,
    )
    assert r.success is False
    assert r.failure_code == F_CLASS_REGISTER_HASH_MISMATCH
    assert "class_definitions" in r.detail


def test_register_hash_signed_field_missing_fails() -> None:
    block = _signed_block()
    del block[SIGN_OFF_HASH_FIELDS_KEY]
    r = check_class_register_hash_mismatch(
        register={SIGN_OFF_KEY: block},
        field_classifications_canonical_bytes=b"x",
        class_definitions_canonical_bytes=b"y",
        hash_bytes=lambda _b: "0" * 128,
    )
    assert r.success is False
    assert r.failure_code == F_CLASS_REGISTER_HASH_MISMATCH


def test_register_hash_compares_case_insensitive() -> None:
    fields_full_hash_upper = "0123456789ABCDEF" + "0" * 112
    class_full_hash_upper = "FEDCBA9876543210" + "0" * 112

    def hash_bytes(b: bytes) -> str:
        if b == b"fields-bytes":
            return fields_full_hash_upper
        return class_full_hash_upper

    block = _signed_block()
    block[SIGN_OFF_HASH_FIELDS_KEY] = "0123456789abcdef"
    block[SIGN_OFF_HASH_CLASS_KEY] = "fedcba9876543210"

    r = check_class_register_hash_mismatch(
        register={SIGN_OFF_KEY: block},
        field_classifications_canonical_bytes=b"fields-bytes",
        class_definitions_canonical_bytes=b"class-bytes",
        hash_bytes=hash_bytes,
    )
    assert r.success is True


def test_register_hash_callable_raises_fails() -> None:
    def boom(_b: bytes) -> str:
        raise RuntimeError("hash failure")

    r = check_class_register_hash_mismatch(
        register={SIGN_OFF_KEY: _signed_block()},
        field_classifications_canonical_bytes=b"x",
        class_definitions_canonical_bytes=b"y",
        hash_bytes=boom,
    )
    assert r.success is False
    assert "RuntimeError" in r.detail
