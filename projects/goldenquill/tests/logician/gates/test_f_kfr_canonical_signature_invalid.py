"""F-KFR-CANONICAL-SIGNATURE-INVALID tests (M1 §2.4)."""

from __future__ import annotations

import hashlib
from typing import Optional

from pipeline.logician.canonicalization import canonicalize
from pipeline.logician.canonicalization.legacy_migration import (
    LEGACY_ACCEPT_DISABLED,
    LEGACY_ACCEPT_ENABLED,
)
from pipeline.logician.gates.f_kfr_canonical_signature_invalid import (
    F_KFR_CANONICAL_SIGNATURE_INVALID,
    check_kfr_canonical_signature_invalid,
)


def _make_verifier(*, accept_canonical: Optional[bytes] = None,
                   accept_raw: Optional[bytes] = None):
    """Returns a fake Ed25519 verifier closing over expected message bytes."""

    def _verify(message: bytes, signature: bytes, public_key: bytes) -> bool:
        del signature, public_key  # unused in fake
        if accept_canonical is not None and message == accept_canonical:
            return True
        if accept_raw is not None and message == accept_raw:
            return True
        return False

    return _verify


def test_failure_code_constant() -> None:
    assert F_KFR_CANONICAL_SIGNATURE_INVALID == "F-KFR-CANONICAL-SIGNATURE-INVALID"


def test_canonical_signature_passes() -> None:
    entry = {"fact_id": "F1", "value": 100, "unit": "usd"}
    canonical = canonicalize(entry)
    verifier = _make_verifier(accept_canonical=canonical)
    r = check_kfr_canonical_signature_invalid(
        fact_id="F1",
        entry_mapping=entry,
        raw_yaml_bytes=b"...",
        signature=b"sig",
        public_key=b"pk",
        signature_verify=verifier,
    )
    assert r.success is True
    assert r.used_legacy_path is False


def test_canonical_signature_fail_no_legacy_fallback() -> None:
    entry = {"fact_id": "F1", "value": 100}
    verifier = _make_verifier()
    r = check_kfr_canonical_signature_invalid(
        fact_id="F1",
        entry_mapping=entry,
        raw_yaml_bytes=b"raw_bytes",
        signature=b"sig",
        public_key=b"pk",
        signature_verify=verifier,
        legacy_accept_mode=LEGACY_ACCEPT_DISABLED,
    )
    assert r.success is False
    assert r.failure_code == F_KFR_CANONICAL_SIGNATURE_INVALID


def test_legacy_accept_path_passes() -> None:
    """When canonical fails AND legacy_accept_mode=enabled, raw fallback used."""
    entry = {"fact_id": "F1", "value": 100}
    raw = b"fact_id: F1\nvalue: 100\n"
    verifier = _make_verifier(accept_raw=raw)
    r = check_kfr_canonical_signature_invalid(
        fact_id="F1",
        entry_mapping=entry,
        raw_yaml_bytes=raw,
        signature=b"sig",
        public_key=b"pk",
        signature_verify=verifier,
        legacy_accept_mode=LEGACY_ACCEPT_ENABLED,
    )
    assert r.success is True
    assert r.used_legacy_path is True


def test_legacy_accept_path_canonical_preferred() -> None:
    """If canonical verifies, legacy path NOT used even when enabled."""
    entry = {"fact_id": "F1", "value": 100}
    canonical = canonicalize(entry)
    raw = b"fact_id: F1\nvalue: 100\n"
    verifier = _make_verifier(accept_canonical=canonical, accept_raw=raw)
    r = check_kfr_canonical_signature_invalid(
        fact_id="F1",
        entry_mapping=entry,
        raw_yaml_bytes=raw,
        signature=b"sig",
        public_key=b"pk",
        signature_verify=verifier,
        legacy_accept_mode=LEGACY_ACCEPT_ENABLED,
    )
    assert r.success is True
    assert r.used_legacy_path is False


def test_canonicalization_error_fails_closed() -> None:
    """Float in entry → canonicalization refuses → gate fails."""
    entry = {"fact_id": "F1", "value": 1.5}  # float forbidden
    verifier = _make_verifier()
    r = check_kfr_canonical_signature_invalid(
        fact_id="F1",
        entry_mapping=entry,
        raw_yaml_bytes=b"raw",
        signature=b"sig",
        public_key=b"pk",
        signature_verify=verifier,
    )
    assert r.success is False
    assert r.failure_code == F_KFR_CANONICAL_SIGNATURE_INVALID
    assert "canonicalization refused" in r.detail
