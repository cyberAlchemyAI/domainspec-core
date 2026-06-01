"""Tests for pipeline.calibration.signing (R12.A).

Covers:
- sign_report happy path + re-sign refusal + bad-signature-length rejection.
- sign_report TypeError on non-str signed_at_iso; ValueError on empty.
- sign_report TypeError on non-bytes signer return.
- reconcile_operator_pubkey first-write / match / rotation-rejection paths.
- reconcile_operator_pubkey rejects wrong pubkey length / non-bytes.
- reconcile_operator_pubkey rejects empty operator/run_id/first_write_iso.
- verify_calibration_report happy path (sign then verify).
- verify_calibration_report unsigned-report rejection.
- verify_calibration_report stale-signature F_PIPE_21.calibration_signature_stale.
- verify_calibration_report canonical_sha256 tamper rejection.
- verify_calibration_report Ed25519 InvalidSignature on byte tamper.
- verify_calibration_report naive clock rejection + naive signed_at rejection.
- verify_calibration_report pubkey length / type guards.
- _parse_signed_at Z-suffix normalization.
- _build_provenance_bytes deterministic inline-literal "Ed25519".
- _pubkey_key_path / _pubkey_provenance_path inline-literal builders.
- Ed25519ReferenceSigner wraps Ed25519PrivateKey cleanly.
- Module-load asserts for CALIBRATION_KEY_PATH_TMPL +
  CALIBRATION_PUBKEY_PROVENANCE_PATH_TMPL (runtime snapshot).
- Freshness window is exactly 90 days (inline-literal RHS: 90 days - 1 sec ok,
  90 days exact = stale).
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timedelta, timezone
from typing import Any

import pytest
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from pipeline.calibration.report import (
    CalibrationReport,
    CalibrationReportItem,
    canonical_bytes,
    compute_canonical_sha256,
)
from pipeline.calibration.signing import (
    CALIBRATION_KEY_PATH_TMPL,
    CALIBRATION_PUBKEY_PROVENANCE_PATH_TMPL,
    CalibrationSignerProtocol,
    Ed25519ReferenceSigner,
    _build_provenance_bytes,
    _parse_signed_at,
    _pubkey_key_path,
    _pubkey_provenance_path,
    reconcile_operator_pubkey,
    sign_report,
    verify_calibration_report,
)
from pipeline.loop.errors import F_PIPE_21


# ---------------------------------------------------------------------------
# Fixtures + helpers
# ---------------------------------------------------------------------------


def _item_kwargs(**o: Any) -> dict[str, Any]:
    base = dict(
        item_id="gs-001",
        judge_total_score=85,
        judge_per_dimension={"clarity": 9, "fit": 8, "alignment": 9},
        editor_critique_summary="strong draft; tightened section 3",
        iterations_used=2,
        revision_loop_outcome="pass_iter2",
        item_run_id="run-001",
    )
    base.update(o)
    return base


def _build_unsigned_report(**o: Any) -> CalibrationReport:
    items = (CalibrationReportItem(**_item_kwargs()),)
    base = dict(
        schema_version=1,
        run_id="run-eval-001",
        operator_org_slug="fit_farms_llc",
        golden_set_manifest_path="vault/fit_farms_llc/golden_set/manifest.json",
        golden_set_manifest_hash="a" * 64,
        items=items,
        summary_judge_mean=85.0,
        summary_judge_stddev=0.0,
        summary_per_dimension_mean={"clarity": 9.0, "fit": 8.0, "alignment": 9.0},
        council_charter_snapshot_hash="c" * 64,
        router_yaml_snapshot_hash="d" * 64,
        assembled_at_iso="2026-04-21T12:00:00+00:00",
        signature=None,
        signed_at_iso=None,
    )
    base.update(o)
    # canonical_sha256 must match actual canonical bytes for verify tests.
    skeleton = CalibrationReport(canonical_sha256="", **base)
    digest = compute_canonical_sha256(skeleton)
    return CalibrationReport(canonical_sha256=digest, **base)


class _FakeBadLenSigner:
    """Returns a 63-byte signature — violates Ed25519 64-byte invariant."""

    def __init__(self, pubkey: bytes = b"\x00" * 32) -> None:
        self._pubkey = pubkey

    def sign(self, canonical_bytes_: bytes) -> bytes:
        return b"\x00" * 63

    def public_key_bytes(self) -> bytes:
        return self._pubkey


class _FakeNonBytesSigner:
    def sign(self, canonical_bytes_: bytes) -> Any:
        return "not-bytes"

    def public_key_bytes(self) -> bytes:
        return b"\x00" * 32


class _FakeWrongPubkeyLenSigner:
    """public_key_bytes returns 31 bytes — rejected by reconcile."""

    def sign(self, canonical_bytes_: bytes) -> bytes:
        return b"\x00" * 64

    def public_key_bytes(self) -> bytes:
        return b"\x00" * 31


class _FakeNonBytesPubkeySigner:
    def sign(self, canonical_bytes_: bytes) -> bytes:
        return b"\x00" * 64

    def public_key_bytes(self) -> Any:
        return "not-bytes"


class _PubkeyVault:
    """In-memory fake PubkeyVaultReader + PubkeyVaultWriter pair."""

    def __init__(self) -> None:
        self.store: dict[str, bytes] = {}
        self.provenance: dict[str, bytes] = {}
        self.writes: int = 0

    def read(self, *, operator_org_slug: str) -> bytes | None:
        return self.store.get(operator_org_slug)

    def write(
        self,
        *,
        operator_org_slug: str,
        pubkey_bytes: bytes,
        provenance_bytes: bytes,
    ) -> tuple[str, str]:
        self.store[operator_org_slug] = pubkey_bytes
        self.provenance[operator_org_slug] = provenance_bytes
        self.writes += 1
        return (
            f"pubkey-ref-{operator_org_slug}",
            f"prov-ref-{operator_org_slug}",
        )


# ---------------------------------------------------------------------------
# Module-load / constant snapshots
# ---------------------------------------------------------------------------


def test_calibration_key_path_tmpl_inline_literal() -> None:
    assert CALIBRATION_KEY_PATH_TMPL == (
        "vault/{operator_org_slug}/calibration/keys/operator_pubkey.ed25519"
    )


def test_calibration_pubkey_provenance_path_tmpl_inline_literal() -> None:
    assert CALIBRATION_PUBKEY_PROVENANCE_PATH_TMPL == (
        "vault/{operator_org_slug}/calibration/keys/"
        "pubkey_first_write_provenance.json"
    )


# ---------------------------------------------------------------------------
# _pubkey_key_path / _pubkey_provenance_path
# ---------------------------------------------------------------------------


def test_pubkey_key_path_happy() -> None:
    assert _pubkey_key_path("fit_farms_llc") == (
        "vault/fit_farms_llc/calibration/keys/operator_pubkey.ed25519"
    )


def test_pubkey_key_path_rejects_empty() -> None:
    with pytest.raises(ValueError, match="operator_org_slug must be non-empty"):
        _pubkey_key_path("")


def test_pubkey_provenance_path_happy() -> None:
    assert _pubkey_provenance_path("acme") == (
        "vault/acme/calibration/keys/pubkey_first_write_provenance.json"
    )


def test_pubkey_provenance_path_rejects_empty() -> None:
    with pytest.raises(ValueError, match="operator_org_slug must be non-empty"):
        _pubkey_provenance_path("")


# ---------------------------------------------------------------------------
# _build_provenance_bytes
# ---------------------------------------------------------------------------


def test_build_provenance_bytes_deterministic() -> None:
    a = _build_provenance_bytes(
        operator_org_slug="fit_farms_llc",
        run_id="run-001",
        first_write_iso="2026-04-21T12:00:00+00:00",
    )
    b = _build_provenance_bytes(
        operator_org_slug="fit_farms_llc",
        run_id="run-001",
        first_write_iso="2026-04-21T12:00:00+00:00",
    )
    assert a == b


def test_build_provenance_bytes_contains_inline_literal_algorithm() -> None:
    provenance = _build_provenance_bytes(
        operator_org_slug="acme",
        run_id="run-001",
        first_write_iso="2026-04-21T12:00:00+00:00",
    )
    payload = json.loads(provenance.decode("utf-8"))
    assert payload["algorithm"] == "Ed25519"
    assert payload["schema_version"] == "1"
    assert payload["operator_org_slug"] == "acme"
    assert payload["first_write_run_id"] == "run-001"
    assert payload["first_write_iso"] == "2026-04-21T12:00:00+00:00"


def test_build_provenance_bytes_sort_keys_stable() -> None:
    provenance = _build_provenance_bytes(
        operator_org_slug="a",
        run_id="r",
        first_write_iso="2026-04-21T12:00:00+00:00",
    )
    # Sorted alphabetical order of keys in the JSON output.
    text = provenance.decode("utf-8")
    keys_in_order = [
        text.index('"algorithm"'),
        text.index('"first_write_iso"'),
        text.index('"first_write_run_id"'),
        text.index('"operator_org_slug"'),
        text.index('"schema_version"'),
    ]
    assert keys_in_order == sorted(keys_in_order)


# ---------------------------------------------------------------------------
# sign_report
# ---------------------------------------------------------------------------


def test_sign_report_happy_path() -> None:
    priv = Ed25519PrivateKey.generate()
    signer = Ed25519ReferenceSigner(priv)
    report = _build_unsigned_report()
    signed = sign_report(
        report, signer=signer, signed_at_iso="2026-04-21T12:00:00+00:00"
    )
    assert signed.signature is not None
    assert len(signed.signature) == 64
    assert signed.signed_at_iso == "2026-04-21T12:00:00+00:00"
    # canonical_sha256 is the hash of the signed-variant bytes (signed_at_iso
    # is canonical-included, so it differs from the unsigned hash).
    assert signed.canonical_sha256 != report.canonical_sha256
    assert len(signed.canonical_sha256) == 64
    # All other fields preserved.
    assert signed.run_id == report.run_id
    assert signed.operator_org_slug == report.operator_org_slug


def test_sign_report_refuses_re_sign() -> None:
    priv = Ed25519PrivateKey.generate()
    signer = Ed25519ReferenceSigner(priv)
    report = _build_unsigned_report()
    signed = sign_report(
        report, signer=signer, signed_at_iso="2026-04-21T12:00:00+00:00"
    )
    with pytest.raises(ValueError, match="already signed"):
        sign_report(
            signed, signer=signer, signed_at_iso="2026-04-22T12:00:00+00:00"
        )


def test_sign_report_rejects_empty_signed_at() -> None:
    priv = Ed25519PrivateKey.generate()
    signer = Ed25519ReferenceSigner(priv)
    report = _build_unsigned_report()
    with pytest.raises(ValueError, match="signed_at_iso must be non-empty"):
        sign_report(report, signer=signer, signed_at_iso="")


def test_sign_report_rejects_non_str_signed_at() -> None:
    priv = Ed25519PrivateKey.generate()
    signer = Ed25519ReferenceSigner(priv)
    report = _build_unsigned_report()
    with pytest.raises(TypeError, match="signed_at_iso must be str"):
        sign_report(report, signer=signer, signed_at_iso=12345)  # type: ignore[arg-type]


def test_sign_report_rejects_bad_signature_length() -> None:
    signer = _FakeBadLenSigner()
    report = _build_unsigned_report()
    with pytest.raises(ValueError, match="expected 64"):
        sign_report(
            report, signer=signer, signed_at_iso="2026-04-21T12:00:00+00:00"
        )


def test_sign_report_rejects_non_bytes_signer_return() -> None:
    signer = _FakeNonBytesSigner()
    report = _build_unsigned_report()
    with pytest.raises(TypeError, match="must return bytes"):
        sign_report(
            report, signer=signer, signed_at_iso="2026-04-21T12:00:00+00:00"
        )


# ---------------------------------------------------------------------------
# reconcile_operator_pubkey
# ---------------------------------------------------------------------------


def test_reconcile_first_write() -> None:
    priv = Ed25519PrivateKey.generate()
    signer = Ed25519ReferenceSigner(priv)
    vault = _PubkeyVault()
    pubkey, first = reconcile_operator_pubkey(
        operator_org_slug="fit_farms_llc",
        run_id="run-001",
        first_write_iso="2026-04-21T12:00:00+00:00",
        signer=signer,
        pubkey_read=vault.read,
        pubkey_write=vault.write,
    )
    assert first is True
    assert len(pubkey) == 32
    assert vault.writes == 1
    assert vault.store["fit_farms_llc"] == pubkey
    # Provenance sidecar carries inline-literal Ed25519.
    payload = json.loads(vault.provenance["fit_farms_llc"].decode("utf-8"))
    assert payload["algorithm"] == "Ed25519"


def test_reconcile_match_no_write() -> None:
    priv = Ed25519PrivateKey.generate()
    signer = Ed25519ReferenceSigner(priv)
    vault = _PubkeyVault()
    # Seed vault with signer's pubkey.
    vault.store["fit_farms_llc"] = signer.public_key_bytes()
    pubkey, first = reconcile_operator_pubkey(
        operator_org_slug="fit_farms_llc",
        run_id="run-002",
        first_write_iso="2026-04-22T12:00:00+00:00",
        signer=signer,
        pubkey_read=vault.read,
        pubkey_write=vault.write,
    )
    assert first is False
    assert pubkey == signer.public_key_bytes()
    assert vault.writes == 0  # no write on match


def test_reconcile_rotation_rejected() -> None:
    priv_a = Ed25519PrivateKey.generate()
    priv_b = Ed25519PrivateKey.generate()
    signer = Ed25519ReferenceSigner(priv_b)
    vault = _PubkeyVault()
    # Seed vault with DIFFERENT key.
    vault.store["fit_farms_llc"] = Ed25519ReferenceSigner(
        priv_a
    ).public_key_bytes()
    with pytest.raises(ValueError, match="rotation detected"):
        reconcile_operator_pubkey(
            operator_org_slug="fit_farms_llc",
            run_id="run-003",
            first_write_iso="2026-04-23T12:00:00+00:00",
            signer=signer,
            pubkey_read=vault.read,
            pubkey_write=vault.write,
        )
    assert vault.writes == 0


def test_reconcile_rejects_empty_operator() -> None:
    priv = Ed25519PrivateKey.generate()
    signer = Ed25519ReferenceSigner(priv)
    vault = _PubkeyVault()
    with pytest.raises(ValueError, match="operator_org_slug must be non-empty"):
        reconcile_operator_pubkey(
            operator_org_slug="",
            run_id="run-001",
            first_write_iso="2026-04-21T12:00:00+00:00",
            signer=signer,
            pubkey_read=vault.read,
            pubkey_write=vault.write,
        )


def test_reconcile_rejects_empty_run_id() -> None:
    priv = Ed25519PrivateKey.generate()
    signer = Ed25519ReferenceSigner(priv)
    vault = _PubkeyVault()
    with pytest.raises(ValueError, match="run_id must be non-empty"):
        reconcile_operator_pubkey(
            operator_org_slug="fit_farms_llc",
            run_id="",
            first_write_iso="2026-04-21T12:00:00+00:00",
            signer=signer,
            pubkey_read=vault.read,
            pubkey_write=vault.write,
        )


def test_reconcile_rejects_empty_first_write_iso() -> None:
    priv = Ed25519PrivateKey.generate()
    signer = Ed25519ReferenceSigner(priv)
    vault = _PubkeyVault()
    with pytest.raises(ValueError, match="first_write_iso must be non-empty"):
        reconcile_operator_pubkey(
            operator_org_slug="fit_farms_llc",
            run_id="run-001",
            first_write_iso="",
            signer=signer,
            pubkey_read=vault.read,
            pubkey_write=vault.write,
        )


def test_reconcile_rejects_wrong_pubkey_length() -> None:
    signer = _FakeWrongPubkeyLenSigner()
    vault = _PubkeyVault()
    with pytest.raises(ValueError, match="expected 32"):
        reconcile_operator_pubkey(
            operator_org_slug="fit_farms_llc",
            run_id="run-001",
            first_write_iso="2026-04-21T12:00:00+00:00",
            signer=signer,
            pubkey_read=vault.read,
            pubkey_write=vault.write,
        )


def test_reconcile_rejects_non_bytes_pubkey() -> None:
    signer = _FakeNonBytesPubkeySigner()
    vault = _PubkeyVault()
    with pytest.raises(TypeError, match="public_key_bytes must return bytes"):
        reconcile_operator_pubkey(
            operator_org_slug="fit_farms_llc",
            run_id="run-001",
            first_write_iso="2026-04-21T12:00:00+00:00",
            signer=signer,
            pubkey_read=vault.read,
            pubkey_write=vault.write,
        )


# ---------------------------------------------------------------------------
# _parse_signed_at
# ---------------------------------------------------------------------------


def test_parse_signed_at_z_suffix() -> None:
    dt = _parse_signed_at("2026-04-21T12:00:00Z")
    assert dt.tzinfo is not None
    assert dt == datetime(2026, 4, 21, 12, 0, 0, tzinfo=timezone.utc)


def test_parse_signed_at_offset() -> None:
    dt = _parse_signed_at("2026-04-21T12:00:00+00:00")
    assert dt.tzinfo is not None
    assert dt == datetime(2026, 4, 21, 12, 0, 0, tzinfo=timezone.utc)


def test_parse_signed_at_naive_rejected() -> None:
    with pytest.raises(ValueError, match="must be timezone-aware"):
        _parse_signed_at("2026-04-21T12:00:00")


# ---------------------------------------------------------------------------
# verify_calibration_report
# ---------------------------------------------------------------------------


def test_verify_happy_path() -> None:
    priv = Ed25519PrivateKey.generate()
    signer = Ed25519ReferenceSigner(priv)
    report = _build_unsigned_report()
    signed = sign_report(
        report, signer=signer, signed_at_iso="2026-04-21T12:00:00+00:00"
    )
    # Pin "now" just inside the 90-day window.
    now = datetime(2026, 4, 21, 12, 0, 30, tzinfo=timezone.utc)
    verify_calibration_report(
        signed,
        pubkey_bytes=signer.public_key_bytes(),
        now_utc=lambda: now,
    )


def test_verify_rejects_unsigned() -> None:
    report = _build_unsigned_report()
    with pytest.raises(ValueError, match="unsigned"):
        verify_calibration_report(
            report,
            pubkey_bytes=b"\x00" * 32,
            now_utc=lambda: datetime(2026, 4, 21, tzinfo=timezone.utc),
        )


def test_verify_stale_signature_fires_f_pipe_21() -> None:
    priv = Ed25519PrivateKey.generate()
    signer = Ed25519ReferenceSigner(priv)
    report = _build_unsigned_report()
    signed = sign_report(
        report, signer=signer, signed_at_iso="2026-01-01T00:00:00+00:00"
    )
    # 91 days later.
    now = datetime(2026, 4, 2, 0, 0, 1, tzinfo=timezone.utc)
    with pytest.raises(F_PIPE_21) as exc_info:
        verify_calibration_report(
            signed,
            pubkey_bytes=signer.public_key_bytes(),
            now_utc=lambda: now,
        )
    assert exc_info.value.trigger == "calibration_signature_stale"
    assert exc_info.value.details["max_days"] == 90
    assert exc_info.value.details["run_id"] == signed.run_id


def test_verify_exactly_90_days_is_stale() -> None:
    priv = Ed25519PrivateKey.generate()
    signer = Ed25519ReferenceSigner(priv)
    report = _build_unsigned_report()
    signed = sign_report(
        report, signer=signer, signed_at_iso="2026-01-01T00:00:00+00:00"
    )
    # Exactly 90 days later — age >= window => stale.
    now = datetime(2026, 4, 1, 0, 0, 0, tzinfo=timezone.utc)
    with pytest.raises(F_PIPE_21):
        verify_calibration_report(
            signed,
            pubkey_bytes=signer.public_key_bytes(),
            now_utc=lambda: now,
        )


def test_verify_one_second_under_90_days_passes() -> None:
    priv = Ed25519PrivateKey.generate()
    signer = Ed25519ReferenceSigner(priv)
    report = _build_unsigned_report()
    signed = sign_report(
        report, signer=signer, signed_at_iso="2026-01-01T00:00:00+00:00"
    )
    # 89 days, 23:59:59 later.
    now = datetime(2026, 3, 31, 23, 59, 59, tzinfo=timezone.utc)
    verify_calibration_report(
        signed,
        pubkey_bytes=signer.public_key_bytes(),
        now_utc=lambda: now,
    )


def test_verify_canonical_sha256_tampered() -> None:
    priv = Ed25519PrivateKey.generate()
    signer = Ed25519ReferenceSigner(priv)
    report = _build_unsigned_report()
    signed = sign_report(
        report, signer=signer, signed_at_iso="2026-04-21T12:00:00+00:00"
    )
    # Rebuild report with corrupted canonical_sha256 but preserve signature/iso.
    tampered = CalibrationReport(
        schema_version=1,
        run_id=signed.run_id,
        operator_org_slug=signed.operator_org_slug,
        golden_set_manifest_path=signed.golden_set_manifest_path,
        golden_set_manifest_hash=signed.golden_set_manifest_hash,
        items=signed.items,
        summary_judge_mean=signed.summary_judge_mean,
        summary_judge_stddev=signed.summary_judge_stddev,
        summary_per_dimension_mean=signed.summary_per_dimension_mean,
        council_charter_snapshot_hash=signed.council_charter_snapshot_hash,
        router_yaml_snapshot_hash=signed.router_yaml_snapshot_hash,
        assembled_at_iso=signed.assembled_at_iso,
        canonical_sha256="f" * 64,  # TAMPERED
        signature=signed.signature,
        signed_at_iso=signed.signed_at_iso,
    )
    now = datetime(2026, 4, 21, 12, 0, 30, tzinfo=timezone.utc)
    with pytest.raises(ValueError, match="canonical_sha256 mismatch"):
        verify_calibration_report(
            tampered,
            pubkey_bytes=signer.public_key_bytes(),
            now_utc=lambda: now,
        )


def test_verify_ed25519_signature_tampered() -> None:
    priv = Ed25519PrivateKey.generate()
    signer = Ed25519ReferenceSigner(priv)
    report = _build_unsigned_report()
    signed = sign_report(
        report, signer=signer, signed_at_iso="2026-04-21T12:00:00+00:00"
    )
    # Flip one byte of the signature.
    assert signed.signature is not None
    tampered_sig = bytearray(signed.signature)
    tampered_sig[0] ^= 0xFF
    tampered = CalibrationReport(
        schema_version=1,
        run_id=signed.run_id,
        operator_org_slug=signed.operator_org_slug,
        golden_set_manifest_path=signed.golden_set_manifest_path,
        golden_set_manifest_hash=signed.golden_set_manifest_hash,
        items=signed.items,
        summary_judge_mean=signed.summary_judge_mean,
        summary_judge_stddev=signed.summary_judge_stddev,
        summary_per_dimension_mean=signed.summary_per_dimension_mean,
        council_charter_snapshot_hash=signed.council_charter_snapshot_hash,
        router_yaml_snapshot_hash=signed.router_yaml_snapshot_hash,
        assembled_at_iso=signed.assembled_at_iso,
        canonical_sha256=signed.canonical_sha256,
        signature=bytes(tampered_sig),
        signed_at_iso=signed.signed_at_iso,
    )
    now = datetime(2026, 4, 21, 12, 0, 30, tzinfo=timezone.utc)
    with pytest.raises(InvalidSignature):
        verify_calibration_report(
            tampered,
            pubkey_bytes=signer.public_key_bytes(),
            now_utc=lambda: now,
        )


def test_verify_rejects_wrong_pubkey() -> None:
    priv_a = Ed25519PrivateKey.generate()
    priv_b = Ed25519PrivateKey.generate()
    signer_a = Ed25519ReferenceSigner(priv_a)
    signer_b = Ed25519ReferenceSigner(priv_b)
    report = _build_unsigned_report()
    signed = sign_report(
        report, signer=signer_a, signed_at_iso="2026-04-21T12:00:00+00:00"
    )
    now = datetime(2026, 4, 21, 12, 0, 30, tzinfo=timezone.utc)
    with pytest.raises(InvalidSignature):
        verify_calibration_report(
            signed,
            pubkey_bytes=signer_b.public_key_bytes(),
            now_utc=lambda: now,
        )


def test_verify_rejects_wrong_pubkey_length() -> None:
    priv = Ed25519PrivateKey.generate()
    signer = Ed25519ReferenceSigner(priv)
    report = _build_unsigned_report()
    signed = sign_report(
        report, signer=signer, signed_at_iso="2026-04-21T12:00:00+00:00"
    )
    now = datetime(2026, 4, 21, 12, 0, 30, tzinfo=timezone.utc)
    with pytest.raises(ValueError, match="must be 32 bytes"):
        verify_calibration_report(
            signed, pubkey_bytes=b"\x00" * 31, now_utc=lambda: now
        )


def test_verify_rejects_non_bytes_pubkey() -> None:
    priv = Ed25519PrivateKey.generate()
    signer = Ed25519ReferenceSigner(priv)
    report = _build_unsigned_report()
    signed = sign_report(
        report, signer=signer, signed_at_iso="2026-04-21T12:00:00+00:00"
    )
    now = datetime(2026, 4, 21, 12, 0, 30, tzinfo=timezone.utc)
    with pytest.raises(TypeError, match="pubkey_bytes must be bytes"):
        verify_calibration_report(
            signed, pubkey_bytes="not-bytes", now_utc=lambda: now  # type: ignore[arg-type]
        )


def test_verify_rejects_naive_clock() -> None:
    priv = Ed25519PrivateKey.generate()
    signer = Ed25519ReferenceSigner(priv)
    report = _build_unsigned_report()
    signed = sign_report(
        report, signer=signer, signed_at_iso="2026-04-21T12:00:00+00:00"
    )
    with pytest.raises(ValueError, match="naive datetime"):
        verify_calibration_report(
            signed,
            pubkey_bytes=signer.public_key_bytes(),
            now_utc=lambda: datetime(2026, 4, 21, 12, 0, 30),
        )


def test_verify_default_clock_uses_utc_now() -> None:
    # Use a fresh signed report; real now is far newer than Jan 2026 but within
    # 90 days of 2026-04-21 if current time is April 2026. This relies on the
    # test suite's wall clock being near the blueprint's current date. To be
    # deterministic: just check the default clock path is wired (no explicit
    # now_utc) by signing with a recent ISO (today at module-load moment).
    priv = Ed25519PrivateKey.generate()
    signer = Ed25519ReferenceSigner(priv)
    report = _build_unsigned_report()
    now_iso = datetime.now(timezone.utc).isoformat()
    signed = sign_report(report, signer=signer, signed_at_iso=now_iso)
    verify_calibration_report(signed, pubkey_bytes=signer.public_key_bytes())


# ---------------------------------------------------------------------------
# Ed25519ReferenceSigner
# ---------------------------------------------------------------------------


def test_ed25519_reference_signer_rejects_non_private_key() -> None:
    with pytest.raises(TypeError, match="Ed25519PrivateKey"):
        Ed25519ReferenceSigner("not-a-key")  # type: ignore[arg-type]


def test_ed25519_reference_signer_sign_rejects_non_bytes() -> None:
    priv = Ed25519PrivateKey.generate()
    signer = Ed25519ReferenceSigner(priv)
    with pytest.raises(TypeError, match="canonical_bytes_ must be bytes"):
        signer.sign("not-bytes")  # type: ignore[arg-type]


def test_ed25519_reference_signer_public_key_is_32_bytes() -> None:
    priv = Ed25519PrivateKey.generate()
    signer = Ed25519ReferenceSigner(priv)
    pubkey = signer.public_key_bytes()
    assert isinstance(pubkey, bytes)
    assert len(pubkey) == 32


def test_ed25519_reference_signer_sign_produces_64_bytes() -> None:
    priv = Ed25519PrivateKey.generate()
    signer = Ed25519ReferenceSigner(priv)
    sig = signer.sign(b"payload")
    assert isinstance(sig, bytes)
    assert len(sig) == 64


def test_ed25519_reference_signer_implements_protocol() -> None:
    priv = Ed25519PrivateKey.generate()
    signer = Ed25519ReferenceSigner(priv)
    assert isinstance(signer, CalibrationSignerProtocol)


# ---------------------------------------------------------------------------
# End-to-end round trip: sign → canonical bytes match verify recompute
# ---------------------------------------------------------------------------


def test_signed_report_canonical_sha256_matches_bytes() -> None:
    priv = Ed25519PrivateKey.generate()
    signer = Ed25519ReferenceSigner(priv)
    report = _build_unsigned_report()
    signed = sign_report(
        report, signer=signer, signed_at_iso="2026-04-21T12:00:00+00:00"
    )
    cbytes = canonical_bytes(signed)
    recomputed = hashlib.sha256(cbytes).hexdigest()
    assert recomputed == signed.canonical_sha256


def test_signed_at_iso_included_in_canonical_bytes() -> None:
    # signed_at_iso IS canonical-included; two signs with different iso produce
    # different canonical bytes (but same canonical_sha256 only if the pre-sign
    # iso was null; here both are signed variants).
    priv = Ed25519PrivateKey.generate()
    signer = Ed25519ReferenceSigner(priv)
    report = _build_unsigned_report()
    signed_a = sign_report(
        report, signer=signer, signed_at_iso="2026-04-21T12:00:00+00:00"
    )
    signed_b = sign_report(
        report, signer=signer, signed_at_iso="2026-04-22T12:00:00+00:00"
    )
    assert canonical_bytes(signed_a) != canonical_bytes(signed_b)
