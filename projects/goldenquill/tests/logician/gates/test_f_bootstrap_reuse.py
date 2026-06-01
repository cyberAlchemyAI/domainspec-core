"""Unit tests for F-BOOTSTRAP-REUSE (F-AMDT-01)."""

from __future__ import annotations

import pytest

from pipeline.logician.gates import (
    F_AMDT_01,
    BootstrapReuseDetail,
    BootstrapReuseResult,
    check_bootstrap_reuse,
)


def _make_reader(rows):
    def _r() -> list[dict]:
        return rows
    return _r


# ---------------------------------------------------------------------------
# Happy paths
# ---------------------------------------------------------------------------


def test_empty_history_passes() -> None:
    r = check_bootstrap_reuse(lock_history_reader=_make_reader([]))
    assert r.success is True
    assert r.failure_code is None
    assert r.detail is None


def test_single_bootstrap_row_passes() -> None:
    r = check_bootstrap_reuse(
        lock_history_reader=_make_reader([{"bootstrap_exception": True}])
    )
    assert r.success is True


def test_zero_bootstrap_rows_passes() -> None:
    r = check_bootstrap_reuse(
        lock_history_reader=_make_reader(
            [{"module": "a"}, {"module": "b"}, {"module": "c"}]
        )
    )
    assert r.success is True


def test_non_bootstrap_rows_with_false_flag_passes() -> None:
    r = check_bootstrap_reuse(
        lock_history_reader=_make_reader(
            [{"bootstrap_exception": False}, {"bootstrap_exception": False}]
        )
    )
    assert r.success is True


def test_single_bootstrap_among_many_rows_passes() -> None:
    rows: list[dict] = [{"module": f"m{i}"} for i in range(50)]
    rows[17]["bootstrap_exception"] = True
    r = check_bootstrap_reuse(lock_history_reader=_make_reader(rows))
    assert r.success is True


# ---------------------------------------------------------------------------
# Reuse detection
# ---------------------------------------------------------------------------


def test_two_bootstrap_rows_denied() -> None:
    r = check_bootstrap_reuse(
        lock_history_reader=_make_reader(
            [{"bootstrap_exception": True}, {"bootstrap_exception": True}]
        )
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_01
    assert r.detail is not None
    assert r.detail.reason_tag == "bootstrap_reuse_detected"
    assert r.detail.bootstrap_count == 2
    assert r.detail.offending_indices == (0, 1)


def test_three_bootstrap_rows_denied() -> None:
    r = check_bootstrap_reuse(
        lock_history_reader=_make_reader(
            [{"bootstrap_exception": True}] * 3
        )
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_01
    assert r.detail.bootstrap_count == 3
    assert r.detail.offending_indices == (0, 1, 2)


def test_ten_bootstrap_rows_denied() -> None:
    rows = [{"bootstrap_exception": True} for _ in range(10)]
    r = check_bootstrap_reuse(lock_history_reader=_make_reader(rows))
    assert r.success is False
    assert r.detail.bootstrap_count == 10
    assert r.detail.offending_indices == tuple(range(10))


def test_two_bootstrap_rows_non_consecutive() -> None:
    rows = [{"module": f"m{i}"} for i in range(20)]
    rows[3]["bootstrap_exception"] = True
    rows[17]["bootstrap_exception"] = True
    r = check_bootstrap_reuse(lock_history_reader=_make_reader(rows))
    assert r.success is False
    assert r.detail.offending_indices == (3, 17)


# ---------------------------------------------------------------------------
# Strict-bool identity — truthy values do NOT count
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "bogus",
    [
        1, 0, 2, -1,
        "true", "True", "TRUE", "false", "yes", "no", "1", "",
        [True], (True,), {"inner": True},
        None,
        1.0, 0.0,
    ],
)
def test_truthy_but_not_strict_bool_not_counted(bogus: object) -> None:
    # Even many such rows should pass — none is strictly `True`.
    rows = [{"bootstrap_exception": bogus} for _ in range(20)]
    r = check_bootstrap_reuse(lock_history_reader=_make_reader(rows))
    assert r.success is True


def test_mixed_string_true_and_real_true_counts_only_real() -> None:
    r = check_bootstrap_reuse(
        lock_history_reader=_make_reader(
            [
                {"bootstrap_exception": "true"},
                {"bootstrap_exception": True},
                {"bootstrap_exception": "True"},
                {"bootstrap_exception": None},
            ]
        )
    )
    assert r.success is True


def test_key_absent_not_counted() -> None:
    rows = [{"module": "a"}, {"module": "b"}, {"bootstrap_exception": True}]
    r = check_bootstrap_reuse(lock_history_reader=_make_reader(rows))
    assert r.success is True


def test_bootstrap_false_explicitly_not_counted() -> None:
    rows = [{"bootstrap_exception": False}] * 50
    r = check_bootstrap_reuse(lock_history_reader=_make_reader(rows))
    assert r.success is True


# ---------------------------------------------------------------------------
# Reader contract violations
# ---------------------------------------------------------------------------


def test_reader_raises_exception_denied() -> None:
    def _bad() -> list[dict]:
        raise RuntimeError("boom")
    r = check_bootstrap_reuse(lock_history_reader=_bad)
    assert r.success is False
    assert r.failure_code == F_AMDT_01
    assert r.detail.reason_tag == "reader_raised"
    assert "RuntimeError" in (r.detail.reader_error or "")


def test_reader_returns_non_list_denied() -> None:
    def _bad() -> list[dict]:
        return "not a list"  # type: ignore[return-value]
    r = check_bootstrap_reuse(lock_history_reader=_bad)
    assert r.success is False
    assert r.detail.reason_tag == "reader_contract_violation"


def test_reader_returns_none_denied() -> None:
    def _bad() -> list[dict]:
        return None  # type: ignore[return-value]
    r = check_bootstrap_reuse(lock_history_reader=_bad)
    assert r.success is False
    assert r.detail.reason_tag == "reader_contract_violation"


def test_reader_returns_dict_denied() -> None:
    def _bad() -> list[dict]:
        return {"oops": True}  # type: ignore[return-value]
    r = check_bootstrap_reuse(lock_history_reader=_bad)
    assert r.success is False
    assert r.detail.reason_tag == "reader_contract_violation"


def test_non_dict_row_denied() -> None:
    r = check_bootstrap_reuse(
        lock_history_reader=_make_reader([{"a": 1}, "not a dict"])  # type: ignore[list-item]
    )
    assert r.success is False
    assert r.detail.reason_tag == "reader_contract_violation"
    assert "str" in (r.detail.reader_error or "")


def test_non_dict_row_at_index_zero_denied() -> None:
    r = check_bootstrap_reuse(
        lock_history_reader=_make_reader([42])  # type: ignore[list-item]
    )
    assert r.success is False
    assert r.detail.reason_tag == "reader_contract_violation"


# ---------------------------------------------------------------------------
# Scale parametrization
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("n_rows", [0, 1, 10, 100, 1000])
def test_scale_zero_bootstrap(n_rows: int) -> None:
    r = check_bootstrap_reuse(
        lock_history_reader=_make_reader([{"module": f"m{i}"} for i in range(n_rows)])
    )
    assert r.success is True


@pytest.mark.parametrize("n_rows", [1, 10, 100])
def test_scale_exactly_one_bootstrap(n_rows: int) -> None:
    rows = [{"module": f"m{i}"} for i in range(n_rows)]
    rows[0]["bootstrap_exception"] = True
    r = check_bootstrap_reuse(lock_history_reader=_make_reader(rows))
    assert r.success is True


@pytest.mark.parametrize("n_rows", [2, 3, 10, 100])
def test_scale_all_bootstrap(n_rows: int) -> None:
    r = check_bootstrap_reuse(
        lock_history_reader=_make_reader(
            [{"bootstrap_exception": True} for _ in range(n_rows)]
        )
    )
    assert r.success is False
    assert r.detail.bootstrap_count == n_rows


# ---------------------------------------------------------------------------
# Result shape invariants
# ---------------------------------------------------------------------------


def test_pass_result_shape() -> None:
    r = check_bootstrap_reuse(lock_history_reader=_make_reader([]))
    assert isinstance(r, BootstrapReuseResult)
    assert r.success is True
    assert r.failure_code is None
    assert r.detail is None


def test_fail_result_shape() -> None:
    r = check_bootstrap_reuse(
        lock_history_reader=_make_reader(
            [{"bootstrap_exception": True}, {"bootstrap_exception": True}]
        )
    )
    assert isinstance(r, BootstrapReuseResult)
    assert isinstance(r.detail, BootstrapReuseDetail)
    assert r.success is False
    assert r.failure_code == F_AMDT_01


def test_result_is_frozen() -> None:
    r = check_bootstrap_reuse(lock_history_reader=_make_reader([]))
    with pytest.raises(Exception):
        r.success = False  # type: ignore[misc]


def test_detail_is_frozen_when_present() -> None:
    r = check_bootstrap_reuse(
        lock_history_reader=_make_reader(
            [{"bootstrap_exception": True}, {"bootstrap_exception": True}]
        )
    )
    with pytest.raises(Exception):
        r.detail.bootstrap_count = 99  # type: ignore[misc,union-attr]


def test_detail_offending_indices_is_tuple() -> None:
    r = check_bootstrap_reuse(
        lock_history_reader=_make_reader(
            [{"bootstrap_exception": True}, {"bootstrap_exception": True}]
        )
    )
    assert isinstance(r.detail.offending_indices, tuple)


def test_failure_code_constant_value() -> None:
    assert F_AMDT_01 == "F-AMDT-01"


# ---------------------------------------------------------------------------
# Field-name sensitivity
# ---------------------------------------------------------------------------


def test_wrong_field_name_not_counted() -> None:
    r = check_bootstrap_reuse(
        lock_history_reader=_make_reader(
            [
                {"bootstrap": True},
                {"BootstrapException": True},
                {"BOOTSTRAP_EXCEPTION": True},
                {"bootstrap_exception ": True},
            ]
        )
    )
    assert r.success is True


# ---------------------------------------------------------------------------
# Other row fields do not interfere
# ---------------------------------------------------------------------------


def test_rich_rows_pass_when_one_bootstrap() -> None:
    rows = [
        {
            "module": "pipeline.sovereignty._types",
            "lock_timestamp_utc": "2026-04-19T00:00:00Z",
            "bootstrap_exception": True,
        },
        {
            "module": "pipeline.vault._constants",
            "lock_timestamp_utc": "2026-04-19T01:00:00Z",
            "code_sha3_512_prefix": "abcdef0123456789",
        },
    ]
    r = check_bootstrap_reuse(lock_history_reader=_make_reader(rows))
    assert r.success is True


def test_extra_fields_do_not_affect_counting() -> None:
    rows = [
        {
            "bootstrap_exception": True,
            "extra_1": "value",
            "extra_2": [1, 2, 3],
            "extra_3": {"nested": True},
        },
        {
            "bootstrap_exception": True,
            "extra_1": "other",
        },
    ]
    r = check_bootstrap_reuse(lock_history_reader=_make_reader(rows))
    assert r.success is False
    assert r.detail.bootstrap_count == 2


# ---------------------------------------------------------------------------
# Reader called exactly once
# ---------------------------------------------------------------------------


def test_reader_called_exactly_once() -> None:
    calls = {"n": 0}
    def _reader() -> list[dict]:
        calls["n"] += 1
        return [{"bootstrap_exception": True}]
    check_bootstrap_reuse(lock_history_reader=_reader)
    assert calls["n"] == 1


def test_reader_called_exactly_once_on_fail() -> None:
    calls = {"n": 0}
    def _reader() -> list[dict]:
        calls["n"] += 1
        return [{"bootstrap_exception": True}, {"bootstrap_exception": True}]
    r = check_bootstrap_reuse(lock_history_reader=_reader)
    assert calls["n"] == 1
    assert r.success is False


# ---------------------------------------------------------------------------
# Offending indices ordering
# ---------------------------------------------------------------------------


def test_offending_indices_are_sorted_ascending() -> None:
    rows = [{"module": f"m{i}"} for i in range(100)]
    for i in (7, 23, 58, 91):
        rows[i]["bootstrap_exception"] = True
    r = check_bootstrap_reuse(lock_history_reader=_make_reader(rows))
    assert r.success is False
    assert r.detail.offending_indices == (7, 23, 58, 91)


def test_offending_count_matches_indices_length() -> None:
    r = check_bootstrap_reuse(
        lock_history_reader=_make_reader(
            [{"bootstrap_exception": True}] * 5
        )
    )
    assert r.detail.bootstrap_count == len(r.detail.offending_indices) == 5
