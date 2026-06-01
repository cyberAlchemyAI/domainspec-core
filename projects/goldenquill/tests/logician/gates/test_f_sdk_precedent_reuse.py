"""Unit tests for F-SDK-PRECEDENT-REUSE (F-AMDT-04)."""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from typing import Optional

import pytest

from pipeline.logician.gates.f_sdk_precedent_reuse import (
    EVENT_AMBIGUOUS,
    EVENT_READER_FAIL,
    EVENT_REUSE,
    F_AMDT_04,
    F_AMDT_04_AMBIGUOUS,
    F_AMDT_04_READER_FAIL,
    F_AMDT_04_REUSE,
    SdkPrecedentReuseDetail,
    SdkPrecedentReuseResult,
    check_sdk_precedent_reuse,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


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


def _sdk_row(
    *,
    seat: str,
    path: str,
    adopts: bool = True,
) -> dict:
    row: dict = {"seat": seat, "audit_evidence_path": path}
    if adopts:
        row["adopts_agent_sdk"] = True
    else:
        row["adopts_agent_sdk"] = False
    return row


def _fm(
    *,
    seat: str = "Scout",
    path: str = "pipeline/validation/scout_sdk_audit.md",
    adopts: bool = True,
    extra: Optional[dict] = None,
) -> dict:
    fm: dict = {"adopts_agent_sdk": adopts, "seat": seat, "audit_evidence_path": path}
    if extra:
        fm.update(extra)
    return fm


_SCRIBE_PATH = "pipeline/validation/scribe_phase0_spike_audit.md"
_SCOUT_PATH = "pipeline/validation/scout_sdk_audit.md"
_EDITOR_PATH = "pipeline/validation/editor_sdk_audit.md"


# ---------------------------------------------------------------------------
# Baseline / no-op paths
# ---------------------------------------------------------------------------


def test_adopts_agent_sdk_false_noop_pass():
    r = check_sdk_precedent_reuse(
        amendment_frontmatter=_fm(adopts=False),
        lock_history_reader=_LockHistory([]),
    )
    assert r.success is True
    assert r.failure_code is None
    assert r.detail.reason_tag == "adopts_agent_sdk_not_true_noop"


def test_adopts_agent_sdk_missing_noop_pass():
    r = check_sdk_precedent_reuse(
        amendment_frontmatter={"seat": "Scout", "audit_evidence_path": _SCOUT_PATH},
        lock_history_reader=_LockHistory([]),
    )
    assert r.success is True
    assert r.detail.reason_tag == "adopts_agent_sdk_not_true_noop"


def test_adopts_agent_sdk_truthy_not_True_noop():
    # Only the singleton `True` triggers the gate. "true" / 1 / [1] must
    # no-op. (The amendment is malformed; other gates catch it.)
    for val in ["true", "True", 1, [1], {"x": 1}]:
        r = check_sdk_precedent_reuse(
            amendment_frontmatter={
                "adopts_agent_sdk": val,
                "seat": "Scout",
                "audit_evidence_path": _SCOUT_PATH,
            },
            lock_history_reader=_LockHistory([]),
        )
        assert r.success is True, f"val={val!r} unexpectedly triggered gate"
        assert r.detail.reason_tag == "adopts_agent_sdk_not_true_noop"


def test_does_not_read_lock_history_when_no_op():
    lh = _LockHistory([])
    check_sdk_precedent_reuse(
        amendment_frontmatter=_fm(adopts=False),
        lock_history_reader=lh,
    )
    assert lh.calls == 0


# ---------------------------------------------------------------------------
# Happy paths (empty / non-matching history)
# ---------------------------------------------------------------------------


def test_first_adoption_empty_history_pass():
    r = check_sdk_precedent_reuse(
        amendment_frontmatter=_fm(seat="Scribe", path=_SCRIBE_PATH),
        lock_history_reader=_LockHistory([]),
    )
    assert r.success is True
    assert r.detail.reason_tag == "no_prior_sdk_row"
    assert r.detail.current_seat == "Scribe"
    assert r.detail.current_audit_evidence_path == _SCRIBE_PATH


def test_first_adoption_history_has_no_sdk_rows_pass():
    r = check_sdk_precedent_reuse(
        amendment_frontmatter=_fm(seat="Scribe", path=_SCRIBE_PATH),
        lock_history_reader=_LockHistory(
            [
                {"module": "pipeline.unrelated"},
                {"verdict": "LOCKED"},
            ]
        ),
    )
    assert r.success is True
    assert r.detail.reason_tag == "no_prior_sdk_row"


def test_same_seat_same_path_re_lock_passes():
    r = check_sdk_precedent_reuse(
        amendment_frontmatter=_fm(seat="Scribe", path=_SCRIBE_PATH),
        lock_history_reader=_LockHistory(
            [_sdk_row(seat="Scribe", path=_SCRIBE_PATH)]
        ),
    )
    assert r.success is True
    assert r.detail.reason_tag == "no_cross_seat_path_match"


def test_different_seat_different_path_passes():
    r = check_sdk_precedent_reuse(
        amendment_frontmatter=_fm(seat="Scout", path=_SCOUT_PATH),
        lock_history_reader=_LockHistory(
            [_sdk_row(seat="Scribe", path=_SCRIBE_PATH)]
        ),
    )
    assert r.success is True
    assert r.detail.reason_tag == "no_cross_seat_path_match"


def test_two_prior_adoptions_new_seat_unique_path_passes():
    r = check_sdk_precedent_reuse(
        amendment_frontmatter=_fm(seat="Judge", path="pipeline/validation/judge_sdk_audit.md"),
        lock_history_reader=_LockHistory(
            [
                _sdk_row(seat="Scribe", path=_SCRIBE_PATH),
                _sdk_row(seat="Scout", path=_SCOUT_PATH),
            ]
        ),
    )
    assert r.success is True


def test_adopts_false_prior_row_ignored():
    # A lock_history row with adopts_agent_sdk=False is NOT an SDK
    # adoption and must not trigger cross-seat reuse.
    r = check_sdk_precedent_reuse(
        amendment_frontmatter=_fm(seat="Scout", path=_SCRIBE_PATH),
        lock_history_reader=_LockHistory(
            [_sdk_row(seat="Scribe", path=_SCRIBE_PATH, adopts=False)]
        ),
    )
    assert r.success is True
    # saw_any_sdk_row stayed False => no_prior_sdk_row reason
    assert r.detail.reason_tag == "no_prior_sdk_row"


# ---------------------------------------------------------------------------
# DENY paths (cross-seat reuse)
# ---------------------------------------------------------------------------


def test_different_seat_same_path_denies():
    r = check_sdk_precedent_reuse(
        amendment_frontmatter=_fm(seat="Scout", path=_SCRIBE_PATH),
        lock_history_reader=_LockHistory(
            [_sdk_row(seat="Scribe", path=_SCRIBE_PATH)]
        ),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_04
    assert r.detail.emitted_event == EVENT_REUSE
    assert r.detail.reason_tag == "cross_seat_evidence_path_reuse"
    assert r.detail.prior_seat == "Scribe"
    assert r.detail.current_seat == "Scout"
    assert r.detail.current_audit_evidence_path == _SCRIBE_PATH


def test_two_prior_adoptions_new_seat_reuses_one_denies():
    r = check_sdk_precedent_reuse(
        amendment_frontmatter=_fm(seat="Judge", path=_SCOUT_PATH),
        lock_history_reader=_LockHistory(
            [
                _sdk_row(seat="Scribe", path=_SCRIBE_PATH),
                _sdk_row(seat="Scout", path=_SCOUT_PATH),
            ]
        ),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_04
    assert r.detail.prior_seat == "Scout"


def test_earliest_matching_prior_row_surfaced():
    # If multiple prior rows share the path, the first match encountered
    # in lock_history order surfaces in prior_seat.
    r = check_sdk_precedent_reuse(
        amendment_frontmatter=_fm(seat="Judge", path=_SCRIBE_PATH),
        lock_history_reader=_LockHistory(
            [
                _sdk_row(seat="Scribe", path=_SCRIBE_PATH),
                _sdk_row(seat="Editor", path=_SCRIBE_PATH),
            ]
        ),
    )
    assert r.success is False
    assert r.detail.prior_seat == "Scribe"


# ---------------------------------------------------------------------------
# DENY paths (ambiguous frontmatter)
# ---------------------------------------------------------------------------


def test_seat_missing_ambiguous():
    r = check_sdk_precedent_reuse(
        amendment_frontmatter={
            "adopts_agent_sdk": True,
            "audit_evidence_path": _SCRIBE_PATH,
        },
        lock_history_reader=_LockHistory([]),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_04_AMBIGUOUS
    assert r.detail.reason_tag == "seat_missing"


def test_seat_non_str_ambiguous():
    r = check_sdk_precedent_reuse(
        amendment_frontmatter={
            "adopts_agent_sdk": True,
            "seat": 42,
            "audit_evidence_path": _SCRIBE_PATH,
        },
        lock_history_reader=_LockHistory([]),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_04_AMBIGUOUS
    assert r.detail.reason_tag == "seat_not_str"


def test_seat_empty_ambiguous():
    r = check_sdk_precedent_reuse(
        amendment_frontmatter=_fm(seat=""),
        lock_history_reader=_LockHistory([]),
    )
    assert r.success is False
    assert r.detail.reason_tag == "seat_empty"


def test_audit_evidence_path_missing_ambiguous():
    r = check_sdk_precedent_reuse(
        amendment_frontmatter={"adopts_agent_sdk": True, "seat": "Scout"},
        lock_history_reader=_LockHistory([]),
    )
    assert r.success is False
    assert r.detail.reason_tag == "audit_evidence_path_missing"
    assert r.detail.current_seat == "Scout"


def test_audit_evidence_path_non_str_ambiguous():
    r = check_sdk_precedent_reuse(
        amendment_frontmatter={
            "adopts_agent_sdk": True,
            "seat": "Scout",
            "audit_evidence_path": 123,
        },
        lock_history_reader=_LockHistory([]),
    )
    assert r.success is False
    assert r.detail.reason_tag == "audit_evidence_path_not_str"


def test_audit_evidence_path_empty_ambiguous():
    r = check_sdk_precedent_reuse(
        amendment_frontmatter=_fm(path=""),
        lock_history_reader=_LockHistory([]),
    )
    assert r.success is False
    assert r.detail.reason_tag == "audit_evidence_path_empty"


def test_frontmatter_not_dict_ambiguous():
    r = check_sdk_precedent_reuse(
        amendment_frontmatter=["not", "a", "dict"],  # type: ignore[arg-type]
        lock_history_reader=_LockHistory([]),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_04_AMBIGUOUS
    assert r.detail.reason_tag == "frontmatter_not_dict"


def test_frontmatter_not_dict_skips_reader():
    lh = _LockHistory([])
    check_sdk_precedent_reuse(
        amendment_frontmatter=None,  # type: ignore[arg-type]
        lock_history_reader=lh,
    )
    assert lh.calls == 0


# ---------------------------------------------------------------------------
# DENY paths (reader failures)
# ---------------------------------------------------------------------------


def test_lock_history_not_list_reader_fail():
    r = check_sdk_precedent_reuse(
        amendment_frontmatter=_fm(),
        lock_history_reader=_LockHistory("not a list"),  # type: ignore[arg-type]
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_04_READER_FAIL
    assert r.detail.reason_tag == "lock_history_return_not_list"


def test_prior_row_non_dict_skipped():
    r = check_sdk_precedent_reuse(
        amendment_frontmatter=_fm(seat="Scout", path=_SCOUT_PATH),
        lock_history_reader=_LockHistory(
            [
                "not a dict",
                None,
                42,
                _sdk_row(seat="Scribe", path=_SCRIBE_PATH),
            ]
        ),
    )
    assert r.success is True
    # Still reports no_cross_seat_path_match (saw a SDK row for Scribe).
    assert r.detail.reason_tag == "no_cross_seat_path_match"


def test_prior_row_missing_seat_skipped():
    r = check_sdk_precedent_reuse(
        amendment_frontmatter=_fm(seat="Scout", path=_SCRIBE_PATH),
        lock_history_reader=_LockHistory(
            [
                # Prior SDK row with no seat field → skipped (can't
                # attribute cross-seat reuse without a seat).
                {"adopts_agent_sdk": True, "audit_evidence_path": _SCRIBE_PATH},
                _sdk_row(seat="Scribe", path=_SCRIBE_PATH),
            ]
        ),
    )
    assert r.success is False
    assert r.detail.prior_seat == "Scribe"


def test_prior_row_non_str_seat_skipped():
    r = check_sdk_precedent_reuse(
        amendment_frontmatter=_fm(seat="Scout", path=_SCRIBE_PATH),
        lock_history_reader=_LockHistory(
            [
                {"adopts_agent_sdk": True, "seat": 99, "audit_evidence_path": _SCRIBE_PATH},
            ]
        ),
    )
    assert r.success is True
    assert r.detail.reason_tag == "no_cross_seat_path_match"


def test_prior_row_empty_seat_skipped():
    r = check_sdk_precedent_reuse(
        amendment_frontmatter=_fm(seat="Scout", path=_SCRIBE_PATH),
        lock_history_reader=_LockHistory(
            [{"adopts_agent_sdk": True, "seat": "", "audit_evidence_path": _SCRIBE_PATH}]
        ),
    )
    assert r.success is True


def test_prior_row_missing_path_skipped():
    r = check_sdk_precedent_reuse(
        amendment_frontmatter=_fm(seat="Scout", path=_SCRIBE_PATH),
        lock_history_reader=_LockHistory(
            [{"adopts_agent_sdk": True, "seat": "Scribe"}]
        ),
    )
    assert r.success is True


def test_prior_row_non_str_path_skipped():
    r = check_sdk_precedent_reuse(
        amendment_frontmatter=_fm(seat="Scout", path=_SCRIBE_PATH),
        lock_history_reader=_LockHistory(
            [
                {
                    "adopts_agent_sdk": True,
                    "seat": "Scribe",
                    "audit_evidence_path": 7,
                }
            ]
        ),
    )
    assert r.success is True


def test_prior_row_empty_path_skipped():
    r = check_sdk_precedent_reuse(
        amendment_frontmatter=_fm(seat="Scout", path=_SCRIBE_PATH),
        lock_history_reader=_LockHistory(
            [
                {
                    "adopts_agent_sdk": True,
                    "seat": "Scribe",
                    "audit_evidence_path": "",
                }
            ]
        ),
    )
    assert r.success is True


# ---------------------------------------------------------------------------
# Parametrised across seat names
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("seat", ["Scout", "Editor", "Judge", "Scribe"])
def test_per_seat_first_adoption_passes(seat):
    path = f"pipeline/validation/{seat.lower()}_sdk_audit.md"
    r = check_sdk_precedent_reuse(
        amendment_frontmatter=_fm(seat=seat, path=path),
        lock_history_reader=_LockHistory([]),
    )
    assert r.success is True
    assert r.detail.current_seat == seat


@pytest.mark.parametrize(
    "current_seat,prior_seat",
    [
        ("Scout", "Scribe"),
        ("Editor", "Scribe"),
        ("Judge", "Scribe"),
        ("Scribe", "Scout"),
        ("Editor", "Judge"),
    ],
)
def test_cross_seat_reuse_denied_across_combinations(current_seat, prior_seat):
    shared_path = "pipeline/validation/shared_audit.md"
    r = check_sdk_precedent_reuse(
        amendment_frontmatter=_fm(seat=current_seat, path=shared_path),
        lock_history_reader=_LockHistory(
            [_sdk_row(seat=prior_seat, path=shared_path)]
        ),
    )
    assert r.success is False
    assert r.detail.prior_seat == prior_seat
    assert r.detail.current_seat == current_seat


# ---------------------------------------------------------------------------
# Constants + frozen dataclass
# ---------------------------------------------------------------------------


def test_constants_match_spec():
    assert F_AMDT_04 == "F-AMDT-04"
    assert F_AMDT_04_REUSE == "F-AMDT-04-REUSE"
    assert F_AMDT_04_AMBIGUOUS == "F-AMDT-04-AMBIGUOUS"
    assert F_AMDT_04_READER_FAIL == "F-AMDT-04-READER-FAIL"
    assert EVENT_REUSE == "F-AMDT-04-REUSE"
    assert EVENT_AMBIGUOUS == "F-AMDT-04-AMBIGUOUS"
    assert EVENT_READER_FAIL == "F-AMDT-04-READER-FAIL"


def test_detail_is_frozen():
    r = check_sdk_precedent_reuse(
        amendment_frontmatter=_fm(seat="Scout", path=_SCOUT_PATH),
        lock_history_reader=_LockHistory([]),
    )
    with pytest.raises(FrozenInstanceError):
        r.detail.reason_tag = "mutated"  # type: ignore[misc]


def test_result_is_frozen():
    r = check_sdk_precedent_reuse(
        amendment_frontmatter=_fm(seat="Scout", path=_SCOUT_PATH),
        lock_history_reader=_LockHistory([]),
    )
    with pytest.raises(FrozenInstanceError):
        r.success = False  # type: ignore[misc]
