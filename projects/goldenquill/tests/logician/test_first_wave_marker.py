"""Tests for pipeline.logician.first_wave_marker (WS-J Slice 3 / RT-C2-04).

Per §14 v1 LOCKED 2026-05-10 §14.9.5 + WS-J Slice 3 handoff (2026-05-11).

The marker verifier is a pure deterministic function — it takes injected
reader + verifier callables and emits a :class:`FirstWaveMarkerVerdict`.
Tests construct stub readers + a stub verifier to exercise every branch.
"""

from __future__ import annotations

from typing import Mapping, Optional

import pytest

from pipeline.logician.first_wave_marker import (
    FIRST_WAVE_FUNDER_IDS,
    FirstWaveMarkerVerdict,
    is_first_wave_funder,
    verify_first_wave_marker,
)


# Helpers --------------------------------------------------------------------


_VALID_HASH = "0" * 128
_OTHER_HASH = "1" * 128
_VALID_SIG = b"\x01" * 64
_VALID_BODY = b"the marker body bytes"
_PUB_KEY = b"\x02" * 32


def _good_marker(funder_id: str) -> dict[str, object]:
    return {
        "funder_id": funder_id,
        "marker_content_sha3_512": _VALID_HASH,
        "signature": _VALID_SIG,
        "signed_bytes": _VALID_BODY,
    }


def _good_ledger(funder_id: str, *, marker_hash: str = _VALID_HASH) -> dict[str, object]:
    return {
        "schema_version": "first_wave_markers.v1",
        "signed_at_utc": "2026-05-11T00:00:00Z",
        "signature": _VALID_SIG,
        "signed_bytes": b"ledger body",
        "entries": {
            funder_id: {
                "marker_content_sha3_512": marker_hash,
                "released_at_utc": "2026-05-11T00:00:00Z",
            }
        },
    }


def _verifier_always_true(message_bytes: bytes, signature: bytes, public_key: bytes) -> bool:
    return True


def _verifier_always_false(message_bytes: bytes, signature: bytes, public_key: bytes) -> bool:
    return False


def _verifier_truthy_not_true(message_bytes: bytes, signature: bytes, public_key: bytes):
    return 1  # truthy but not is-True


# Tests ----------------------------------------------------------------------


class TestFirstWaveFunderSet:
    def test_canonical_five_funders(self) -> None:
        assert FIRST_WAVE_FUNDER_IDS == frozenset(
            {"VAPG", "NIFA", "SARE", "EPA_NEETP", "SBIR"}
        )

    @pytest.mark.parametrize("funder_id", ["VAPG", "NIFA", "SARE", "EPA_NEETP", "SBIR"])
    def test_is_first_wave_funder_true(self, funder_id: str) -> None:
        assert is_first_wave_funder(funder_id) is True

    @pytest.mark.parametrize("funder_id", ["USDA", "NSF", "NEA", "unknown"])
    def test_is_first_wave_funder_false(self, funder_id: str) -> None:
        assert is_first_wave_funder(funder_id) is False


class TestVerifyFirstWaveMarker:
    def test_happy_path_first_wave_funder(self) -> None:
        marker = _good_marker("VAPG")
        ledger = _good_ledger("VAPG")
        verdict = verify_first_wave_marker(
            "VAPG",
            marker_reader=lambda funder_id: marker,
            lock_history_reader=lambda: ledger,
            signature_verifier=_verifier_always_true,
            sn_llc_public_key=_PUB_KEY,
        )
        assert verdict.is_first_wave is True
        assert verdict.present is True
        assert verdict.signature_valid is True
        assert verdict.hash_bound_to_lock_history is True

    def test_marker_missing(self) -> None:
        verdict = verify_first_wave_marker(
            "VAPG",
            marker_reader=lambda funder_id: None,
            lock_history_reader=lambda: _good_ledger("VAPG"),
            signature_verifier=_verifier_always_true,
            sn_llc_public_key=_PUB_KEY,
        )
        assert verdict.present is False
        assert verdict.signature_valid is False
        assert verdict.hash_bound_to_lock_history is False

    def test_marker_funder_id_mismatch(self) -> None:
        bad = _good_marker("NIFA")
        verdict = verify_first_wave_marker(
            "VAPG",
            marker_reader=lambda funder_id: bad,
            lock_history_reader=lambda: _good_ledger("VAPG"),
            signature_verifier=_verifier_always_true,
            sn_llc_public_key=_PUB_KEY,
        )
        assert verdict.present is False
        assert "tampered or mis-published" in verdict.detail

    def test_marker_hash_malformed(self) -> None:
        bad = _good_marker("VAPG") | {"marker_content_sha3_512": "short"}
        verdict = verify_first_wave_marker(
            "VAPG",
            marker_reader=lambda funder_id: bad,
            lock_history_reader=lambda: _good_ledger("VAPG"),
            signature_verifier=_verifier_always_true,
            sn_llc_public_key=_PUB_KEY,
        )
        assert verdict.signature_valid is False
        assert "marker_content_sha3_512 malformed" in verdict.detail

    def test_marker_signature_invalid(self) -> None:
        verdict = verify_first_wave_marker(
            "VAPG",
            marker_reader=lambda funder_id: _good_marker("VAPG"),
            lock_history_reader=lambda: _good_ledger("VAPG"),
            signature_verifier=_verifier_always_false,
            sn_llc_public_key=_PUB_KEY,
        )
        assert verdict.present is True
        assert verdict.signature_valid is False
        assert "did not verify" in verdict.detail

    def test_marker_signature_truthy_not_true_rejected(self) -> None:
        """Strict is-True identity per §4 F-AMDT precedent."""
        verdict = verify_first_wave_marker(
            "VAPG",
            marker_reader=lambda funder_id: _good_marker("VAPG"),
            lock_history_reader=lambda: _good_ledger("VAPG"),
            signature_verifier=_verifier_truthy_not_true,
            sn_llc_public_key=_PUB_KEY,
        )
        assert verdict.signature_valid is False
        assert "strict is-True required" in verdict.detail

    def test_lock_history_empty(self) -> None:
        verdict = verify_first_wave_marker(
            "VAPG",
            marker_reader=lambda funder_id: _good_marker("VAPG"),
            lock_history_reader=lambda: None,
            signature_verifier=_verifier_always_true,
            sn_llc_public_key=_PUB_KEY,
        )
        assert verdict.signature_valid is True
        assert verdict.hash_bound_to_lock_history is False
        assert "operator-deployment-empty" in verdict.detail

    def test_lock_history_entry_missing(self) -> None:
        ledger = _good_ledger("NIFA")  # different funder
        verdict = verify_first_wave_marker(
            "VAPG",
            marker_reader=lambda funder_id: _good_marker("VAPG"),
            lock_history_reader=lambda: ledger,
            signature_verifier=_verifier_always_true,
            sn_llc_public_key=_PUB_KEY,
        )
        assert verdict.hash_bound_to_lock_history is False
        assert "no lock_history entry" in verdict.detail

    def test_lock_history_hash_mismatch(self) -> None:
        ledger = _good_ledger("VAPG", marker_hash=_OTHER_HASH)
        verdict = verify_first_wave_marker(
            "VAPG",
            marker_reader=lambda funder_id: _good_marker("VAPG"),
            lock_history_reader=lambda: ledger,
            signature_verifier=_verifier_always_true,
            sn_llc_public_key=_PUB_KEY,
        )
        assert verdict.hash_bound_to_lock_history is False
        assert "tamper detected" in verdict.detail

    def test_non_first_wave_funder(self) -> None:
        marker = _good_marker("USDA")
        ledger = _good_ledger("USDA")
        verdict = verify_first_wave_marker(
            "USDA",
            marker_reader=lambda funder_id: marker,
            lock_history_reader=lambda: ledger,
            signature_verifier=_verifier_always_true,
            sn_llc_public_key=_PUB_KEY,
        )
        assert verdict.is_first_wave is False
        # All three booleans can still be True for a non-first-wave funder;
        # the gate caller's §14.9.5 logic decides whether absence is
        # fail-closed or advisory.
        assert verdict.present is True
        assert verdict.signature_valid is True
        assert verdict.hash_bound_to_lock_history is True

    def test_funder_id_empty(self) -> None:
        verdict = verify_first_wave_marker(
            "",
            marker_reader=lambda funder_id: _good_marker("VAPG"),
            lock_history_reader=lambda: _good_ledger("VAPG"),
            signature_verifier=_verifier_always_true,
            sn_llc_public_key=_PUB_KEY,
        )
        assert verdict.present is False
        assert "must be a non-empty string" in verdict.detail
