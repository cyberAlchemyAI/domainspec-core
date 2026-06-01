"""Unit tests for F-CLASS-ROUTER-TEMPLATE-SIGNATURE-INVALID (PRE update)."""

from __future__ import annotations

from pipeline.logician.gates.f_class_router_template_signature import (
    F_CLASS_ROUTER_TEMPLATE_SIGNATURE_INVALID,
    check_class_router_template_signature_invalid,
)


def _accept_for_pubkey(target: bytes):
    def _verify(message: bytes, signature: bytes, public_key: bytes) -> bool:
        return public_key == target
    return _verify


def test_failure_code_constant() -> None:
    assert F_CLASS_ROUTER_TEMPLATE_SIGNATURE_INVALID == (
        "F-CLASS-ROUTER-TEMPLATE-SIGNATURE-INVALID"
    )


def test_valid_signature_passes() -> None:
    r = check_class_router_template_signature_invalid(
        template_version="2026-Q2-r1",
        template_canonical_bytes=b"router-template-bytes",
        template_signature=b"sig",
        pinned_signing_public_key=b"pinned-pub",
        signature_verify=_accept_for_pubkey(b"pinned-pub"),
    )
    assert r.success is True
    assert r.template_version == "2026-Q2-r1"


def test_wrong_pubkey_fails() -> None:
    r = check_class_router_template_signature_invalid(
        template_version="2026-Q3-r1",
        template_canonical_bytes=b"x",
        template_signature=b"sig",
        pinned_signing_public_key=b"wrong",
        signature_verify=_accept_for_pubkey(b"pinned"),
    )
    assert r.success is False
    assert r.failure_code == F_CLASS_ROUTER_TEMPLATE_SIGNATURE_INVALID
    assert "REJECTED" in r.detail


def test_empty_template_version_fails() -> None:
    r = check_class_router_template_signature_invalid(
        template_version="",
        template_canonical_bytes=b"x",
        template_signature=b"sig",
        pinned_signing_public_key=b"x",
        signature_verify=_accept_for_pubkey(b"x"),
    )
    assert r.success is False
    assert "unidentified" in r.detail


def test_empty_template_bytes_fails() -> None:
    r = check_class_router_template_signature_invalid(
        template_version="v1",
        template_canonical_bytes=b"",
        template_signature=b"sig",
        pinned_signing_public_key=b"x",
        signature_verify=_accept_for_pubkey(b"x"),
    )
    assert r.success is False


def test_empty_signature_fails() -> None:
    r = check_class_router_template_signature_invalid(
        template_version="v1",
        template_canonical_bytes=b"bytes",
        template_signature=b"",
        pinned_signing_public_key=b"x",
        signature_verify=_accept_for_pubkey(b"x"),
    )
    assert r.success is False
    assert "missing" in r.detail


def test_empty_pinned_pubkey_fails() -> None:
    r = check_class_router_template_signature_invalid(
        template_version="v1",
        template_canonical_bytes=b"bytes",
        template_signature=b"sig",
        pinned_signing_public_key=b"",
        signature_verify=_accept_for_pubkey(b""),
    )
    assert r.success is False
    assert "white-glove" in r.detail


def test_signature_verify_raises_fails() -> None:
    def boom(*_a, **_kw) -> bool:
        raise RuntimeError("transport error")

    r = check_class_router_template_signature_invalid(
        template_version="v1",
        template_canonical_bytes=b"bytes",
        template_signature=b"sig",
        pinned_signing_public_key=b"key",
        signature_verify=boom,
    )
    assert r.success is False
    assert "RuntimeError" in r.detail


def test_signature_verify_returns_truthy_non_true_fails() -> None:
    def returns_str(*_a, **_kw):
        return "yes"

    r = check_class_router_template_signature_invalid(
        template_version="v1",
        template_canonical_bytes=b"bytes",
        template_signature=b"sig",
        pinned_signing_public_key=b"key",
        signature_verify=returns_str,
    )
    assert r.success is False


def test_template_version_whitespace_only_fails() -> None:
    r = check_class_router_template_signature_invalid(
        template_version="   ",
        template_canonical_bytes=b"bytes",
        template_signature=b"sig",
        pinned_signing_public_key=b"key",
        signature_verify=_accept_for_pubkey(b"key"),
    )
    assert r.success is False
