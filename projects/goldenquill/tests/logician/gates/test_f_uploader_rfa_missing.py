"""Unit tests for F-UPLOADER-RFA-MISSING (PRE-30).

Per Blueprint §12.9.5 + §4 v2.7 amendment.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from pipeline.logician.gates.f_uploader_rfa_missing import (
    F_UPLOADER_RFA_MISSING,
    check_uploader_rfa_missing,
)


@dataclass(frozen=True)
class _Rfa:
    rfa_content_sha3_512: str


def _pin_reader(per_run: dict[str, Optional[str]]):
    def _r(run_id: str) -> Optional[str]:
        return per_run.get(run_id)
    return _r


def test_failure_code_constant() -> None:
    assert F_UPLOADER_RFA_MISSING == "F-UPLOADER-RFA-MISSING"


def test_rfa_present_and_hash_matches_passes() -> None:
    r = check_uploader_rfa_missing(
        run_id="r1",
        rfa=_Rfa(rfa_content_sha3_512="abc123"),
        manifest_pin_reader=_pin_reader({"r1": "abc123"}),
    )
    assert r.success is True
    assert r.failure_code is None


def test_rfa_absent_fails() -> None:
    r = check_uploader_rfa_missing(
        run_id="r1",
        rfa=None,
        manifest_pin_reader=_pin_reader({"r1": "abc123"}),
    )
    assert r.success is False
    assert r.failure_code == F_UPLOADER_RFA_MISSING
    assert r.reason_tag == "rfa_record_absent"


def test_pin_absent_fails() -> None:
    r = check_uploader_rfa_missing(
        run_id="r_unknown",
        rfa=_Rfa(rfa_content_sha3_512="abc123"),
        manifest_pin_reader=_pin_reader({}),
    )
    assert r.success is False
    assert r.reason_tag == "rfa_pin_absent"


def test_hash_mismatch_fails() -> None:
    r = check_uploader_rfa_missing(
        run_id="r1",
        rfa=_Rfa(rfa_content_sha3_512="abc123"),
        manifest_pin_reader=_pin_reader({"r1": "different_hash"}),
    )
    assert r.success is False
    assert r.reason_tag == "rfa_hash_mismatch"


def test_pin_reader_raises_fails_closed() -> None:
    def _bad(run_id: str) -> Optional[str]:
        raise RuntimeError("manifest unreadable")

    r = check_uploader_rfa_missing(
        run_id="r1",
        rfa=_Rfa(rfa_content_sha3_512="abc123"),
        manifest_pin_reader=_bad,
    )
    assert r.success is False
    assert r.reason_tag == "rfa_pin_absent"
