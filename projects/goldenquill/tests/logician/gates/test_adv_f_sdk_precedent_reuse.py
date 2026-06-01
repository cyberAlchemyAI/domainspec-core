"""Adversarial tests for F-SDK-PRECEDENT-REUSE (F-AMDT-04).

Covers the five adversarial cases named by the spec card plus defence-
in-depth cases for reader_error clipping, precedence ordering (malformed
frontmatter must short-circuit before any reader fires), and exhaustive
prior-row malformation skipping.
"""

from __future__ import annotations

from typing import Optional

import pytest

from pipeline.logician.gates.f_sdk_precedent_reuse import (
    EVENT_AMBIGUOUS,
    EVENT_READER_FAIL,
    EVENT_REUSE,
    F_AMDT_04,
    F_AMDT_04_AMBIGUOUS,
    F_AMDT_04_READER_FAIL,
    check_sdk_precedent_reuse,
)


class _LockHistory:
    def __init__(self, rows, *, raises: Optional[BaseException] = None):
        self._rows = rows
        self._raises = raises
        self.calls = 0

    def __call__(self):
        self.calls += 1
        if self._raises is not None:
            raise self._raises
        return self._rows


def _sdk_row(seat: str, path: str) -> dict:
    return {"adopts_agent_sdk": True, "seat": seat, "audit_evidence_path": path}


def _fm(*, seat: str, path: str) -> dict:
    return {"adopts_agent_sdk": True, "seat": seat, "audit_evidence_path": path}


_SCRIBE = "pipeline/validation/scribe_phase0_spike_audit.md"


# ---------------------------------------------------------------------------
# 1. Spec-card adversarial cases
# ---------------------------------------------------------------------------


def test_adv_lock_history_reader_raises():
    r = check_sdk_precedent_reuse(
        amendment_frontmatter=_fm(seat="Scout", path="pipeline/validation/scout.md"),
        lock_history_reader=_LockHistory(
            [], raises=PermissionError("lock_history unreadable")
        ),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_04_READER_FAIL
    assert r.detail.emitted_event == EVENT_READER_FAIL
    assert r.detail.reason_tag == "lock_history_reader_raised"
    assert r.detail.reader_error is not None
    assert "lock_history_reader" in r.detail.reader_error
    assert "PermissionError" in r.detail.reader_error


def test_adv_evidence_path_differs_by_trailing_slash():
    # Exact string match: "path/to/evidence" vs "path/to/evidence/" are
    # distinct paths → PASS.
    r = check_sdk_precedent_reuse(
        amendment_frontmatter=_fm(
            seat="Scout",
            path="pipeline/validation/scribe_phase0_spike_audit.md/",
        ),
        lock_history_reader=_LockHistory(
            [_sdk_row(seat="Scribe", path=_SCRIBE)]
        ),
    )
    assert r.success is True
    assert r.detail.reason_tag == "no_cross_seat_path_match"


def test_adv_same_seat_different_evidence_overwrites():
    # Same seat submits a NEW evidence path → PASS. Not cross-seat reuse
    # (the gate only protects against CROSS-seat reuse).
    r = check_sdk_precedent_reuse(
        amendment_frontmatter=_fm(
            seat="Scribe",
            path="pipeline/validation/scribe_phase1_audit.md",
        ),
        lock_history_reader=_LockHistory(
            [_sdk_row(seat="Scribe", path=_SCRIBE)]
        ),
    )
    assert r.success is True
    assert r.detail.reason_tag == "no_cross_seat_path_match"


def test_adv_adopts_sdk_is_string_true():
    # `adopts_agent_sdk: "true"` (string) is NOT the singleton True.
    # Strict `is True` check short-circuits to no-op — the amendment is
    # malformed but caught by a different gate.
    r = check_sdk_precedent_reuse(
        amendment_frontmatter={
            "adopts_agent_sdk": "true",
            "seat": "Scout",
            "audit_evidence_path": "pipeline/validation/scout.md",
        },
        lock_history_reader=_LockHistory([]),
    )
    assert r.success is True
    assert r.detail.reason_tag == "adopts_agent_sdk_not_true_noop"


def test_adv_circular_reuse_three_seats():
    # Seats A, B, C each try to re-use seat A's evidence. B and C DENY.
    lh = [_sdk_row(seat="Scribe", path=_SCRIBE)]

    # B (Scout) submits Scribe's evidence → DENY.
    r_b = check_sdk_precedent_reuse(
        amendment_frontmatter=_fm(seat="Scout", path=_SCRIBE),
        lock_history_reader=_LockHistory(list(lh)),
    )
    assert r_b.success is False
    assert r_b.failure_code == F_AMDT_04
    assert r_b.detail.prior_seat == "Scribe"

    # C (Editor) submits Scribe's evidence → DENY.
    r_c = check_sdk_precedent_reuse(
        amendment_frontmatter=_fm(seat="Editor", path=_SCRIBE),
        lock_history_reader=_LockHistory(list(lh)),
    )
    assert r_c.success is False
    assert r_c.failure_code == F_AMDT_04
    assert r_c.detail.prior_seat == "Scribe"


# ---------------------------------------------------------------------------
# 2. Defence-in-depth
# ---------------------------------------------------------------------------


def test_adv_reader_error_clipped_at_500_chars():
    huge = "X" * 2000
    r = check_sdk_precedent_reuse(
        amendment_frontmatter=_fm(seat="Scout", path="pipeline/validation/scout.md"),
        lock_history_reader=_LockHistory([], raises=RuntimeError(huge)),
    )
    assert r.success is False
    assert r.detail.reader_error is not None
    # Prefix "lock_history_reader: " (21 chars) + ≤500 clipped payload.
    assert len(r.detail.reader_error) <= len("lock_history_reader: ") + 500


def test_adv_precedence_frontmatter_not_dict_skips_reader():
    # Non-dict frontmatter must short-circuit BEFORE the reader fires.
    lh = _LockHistory([], raises=AssertionError("reader must not be called"))
    r = check_sdk_precedent_reuse(
        amendment_frontmatter="this is not a dict",  # type: ignore[arg-type]
        lock_history_reader=lh,
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_04_AMBIGUOUS
    assert r.detail.reason_tag == "frontmatter_not_dict"
    assert lh.calls == 0


def test_adv_precedence_no_op_short_circuits_reader():
    # `adopts_agent_sdk` not True must short-circuit BEFORE any reader
    # call. Leaked reader invocation would be a correctness bug.
    lh = _LockHistory([], raises=AssertionError("reader must not be called"))
    r = check_sdk_precedent_reuse(
        amendment_frontmatter={
            "adopts_agent_sdk": False,
            "seat": "Scout",
            "audit_evidence_path": "pipeline/validation/scout.md",
        },
        lock_history_reader=lh,
    )
    assert r.success is True
    assert lh.calls == 0


def test_adv_precedence_missing_seat_skips_reader():
    # Missing seat must short-circuit BEFORE any reader call.
    lh = _LockHistory([], raises=AssertionError("reader must not be called"))
    r = check_sdk_precedent_reuse(
        amendment_frontmatter={
            "adopts_agent_sdk": True,
            "audit_evidence_path": "pipeline/validation/scout.md",
        },
        lock_history_reader=lh,
    )
    assert r.success is False
    assert r.detail.reason_tag == "seat_missing"
    assert lh.calls == 0


def test_adv_walks_entire_history_to_find_match():
    # Put non-matching noise first, then the cross-seat reuse at the
    # tail. Walker must still find it.
    rows = [
        {"adopts_agent_sdk": False, "seat": "Scribe", "audit_evidence_path": _SCRIBE},
        "junk",
        None,
        {"module": "pipeline.other"},
        _sdk_row(seat="Scribe", path=_SCRIBE),
    ]
    r = check_sdk_precedent_reuse(
        amendment_frontmatter=_fm(seat="Scout", path=_SCRIBE),
        lock_history_reader=_LockHistory(rows),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_04
    assert r.detail.prior_seat == "Scribe"
