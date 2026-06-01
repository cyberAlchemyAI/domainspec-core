"""Unit tests for F-VERDICT-BLOCKING-MISSING (F-AMDT-02).

≥30 unit tests per spec card. Adversarial tests live in
``test_adv_f_verdict_blocking_missing.py``.
"""

from __future__ import annotations

import pytest

from pipeline.logician.gates import (
    F_AMDT_02,
    BlockingMissingResult,
    check_verdict_blocking,
)


# ---------------------------------------------------------------------------
# Happy path — bool value accepted
# ---------------------------------------------------------------------------


def test_blocking_true_minimal_pass() -> None:
    r = check_verdict_blocking({"blocking": True})
    assert r.success is True
    assert r.failure_code is None
    assert r.detail is None


def test_blocking_false_minimal_pass() -> None:
    r = check_verdict_blocking({"blocking": False})
    assert r.success is True
    assert r.failure_code is None
    assert r.detail is None


def test_blocking_true_with_extra_fields_pass() -> None:
    r = check_verdict_blocking(
        {
            "blocking": True,
            "rationale": "major structural failure",
            "seat": "Editor",
            "timestamp": "2026-04-20T00:00:00Z",
        }
    )
    assert r.success is True


def test_blocking_false_with_extra_fields_pass() -> None:
    r = check_verdict_blocking(
        {
            "blocking": False,
            "dimensions": [{"name": "clarity", "score": 90}],
            "rubric_version": "vapg_fy26",
        }
    )
    assert r.success is True


def test_blocking_true_with_nested_fields_pass() -> None:
    r = check_verdict_blocking(
        {"blocking": True, "dimensions": {"clarity": {"score": 10}}}
    )
    assert r.success is True


# ---------------------------------------------------------------------------
# Key-absent failures
# ---------------------------------------------------------------------------


def test_empty_dict_denied() -> None:
    r = check_verdict_blocking({})
    assert r.success is False
    assert r.failure_code == F_AMDT_02
    assert r.detail is not None
    assert r.detail.reason_tag == "blocking_key_absent"


def test_dict_without_blocking_key_denied() -> None:
    r = check_verdict_blocking({"rationale": "text", "seat": "Judge"})
    assert r.success is False
    assert r.failure_code == F_AMDT_02
    assert r.detail.reason_tag == "blocking_key_absent"


def test_dict_with_many_fields_but_no_blocking_denied() -> None:
    r = check_verdict_blocking(
        {
            "a": 1,
            "b": "two",
            "c": [3, 4, 5],
            "d": {"nested": "value"},
            "e": None,
            "f": True,
        }
    )
    assert r.success is False
    assert r.detail.reason_tag == "blocking_key_absent"


def test_case_variant_blocking_key_denied_capital() -> None:
    r = check_verdict_blocking({"Blocking": True})
    assert r.success is False
    assert r.detail.reason_tag == "blocking_key_absent"


def test_case_variant_blocking_key_denied_upper() -> None:
    r = check_verdict_blocking({"BLOCKING": True})
    assert r.success is False
    assert r.detail.reason_tag == "blocking_key_absent"


def test_whitespace_blocking_key_denied() -> None:
    r = check_verdict_blocking({"blocking ": True, " blocking": True})
    assert r.success is False
    assert r.detail.reason_tag == "blocking_key_absent"


# ---------------------------------------------------------------------------
# Wrong-type failures
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "bad_value",
    [
        "true",
        "false",
        "True",
        "False",
        "",
        "0",
        "1",
    ],
)
def test_blocking_value_string_denied(bad_value: str) -> None:
    r = check_verdict_blocking({"blocking": bad_value})
    assert r.success is False
    assert r.failure_code == F_AMDT_02
    assert r.detail.reason_tag == "blocking_value_not_bool"
    assert r.detail.observed_type == "str"


@pytest.mark.parametrize("bad_value", [1, 0, -1, 42, 2**63])
def test_blocking_value_int_denied(bad_value: int) -> None:
    r = check_verdict_blocking({"blocking": bad_value})
    assert r.success is False
    assert r.detail.reason_tag == "blocking_value_not_bool"
    assert r.detail.observed_type == "int"


def test_blocking_value_float_denied() -> None:
    r = check_verdict_blocking({"blocking": 1.0})
    assert r.success is False
    assert r.detail.reason_tag == "blocking_value_not_bool"
    assert r.detail.observed_type == "float"


def test_blocking_value_none_denied() -> None:
    r = check_verdict_blocking({"blocking": None})
    assert r.success is False
    assert r.detail.reason_tag == "blocking_value_not_bool"
    assert r.detail.observed_type == "NoneType"


def test_blocking_value_empty_list_denied() -> None:
    r = check_verdict_blocking({"blocking": []})
    assert r.success is False
    assert r.detail.observed_type == "list"


def test_blocking_value_nonempty_list_denied() -> None:
    r = check_verdict_blocking({"blocking": [True]})
    assert r.success is False
    assert r.detail.observed_type == "list"


def test_blocking_value_empty_dict_denied() -> None:
    r = check_verdict_blocking({"blocking": {}})
    assert r.success is False
    assert r.detail.observed_type == "dict"


def test_blocking_value_tuple_denied() -> None:
    r = check_verdict_blocking({"blocking": (True,)})
    assert r.success is False
    assert r.detail.observed_type == "tuple"


def test_blocking_value_set_denied() -> None:
    r = check_verdict_blocking({"blocking": {True}})
    assert r.success is False
    assert r.detail.observed_type == "set"


def test_blocking_value_bytes_denied() -> None:
    r = check_verdict_blocking({"blocking": b"true"})
    assert r.success is False
    assert r.detail.observed_type == "bytes"


# ---------------------------------------------------------------------------
# Nested / misplaced key
# ---------------------------------------------------------------------------


def test_blocking_at_wrong_depth_denied() -> None:
    r = check_verdict_blocking({"metadata": {"blocking": True}})
    assert r.success is False
    assert r.detail.reason_tag == "blocking_key_absent"


def test_blocking_in_list_entry_denied() -> None:
    r = check_verdict_blocking({"verdicts": [{"blocking": True}]})
    assert r.success is False
    assert r.detail.reason_tag == "blocking_key_absent"


# ---------------------------------------------------------------------------
# Seat-type parametrization (Editor, Judge, Red Team)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("seat", ["Editor", "Judge", "RedTeam"])
def test_seat_parametrized_valid_pass(seat: str) -> None:
    r = check_verdict_blocking({"blocking": True, "seat": seat})
    assert r.success is True


@pytest.mark.parametrize("seat", ["Editor", "Judge", "RedTeam"])
def test_seat_parametrized_missing_key_denied(seat: str) -> None:
    r = check_verdict_blocking({"seat": seat, "rationale": "text"})
    assert r.success is False
    assert r.detail.reason_tag == "blocking_key_absent"


@pytest.mark.parametrize("seat", ["Editor", "Judge", "RedTeam"])
def test_seat_parametrized_string_true_denied(seat: str) -> None:
    r = check_verdict_blocking({"seat": seat, "blocking": "true"})
    assert r.success is False
    assert r.detail.reason_tag == "blocking_value_not_bool"


# ---------------------------------------------------------------------------
# Result-shape invariants
# ---------------------------------------------------------------------------


def test_pass_result_is_frozen_dataclass() -> None:
    r = check_verdict_blocking({"blocking": True})
    with pytest.raises((AttributeError, Exception)):
        r.success = False  # type: ignore[misc]


def test_pass_result_detail_is_none_not_empty_dataclass() -> None:
    r = check_verdict_blocking({"blocking": False})
    assert r.detail is None


def test_fail_result_detail_observed_repr_truncated() -> None:
    long_string = "x" * 5000
    r = check_verdict_blocking({"blocking": long_string})
    assert r.success is False
    assert len(r.detail.observed_repr) <= 210  # 200 + quotes


def test_failure_code_constant_matches_spec_card() -> None:
    assert F_AMDT_02 == "F-AMDT-02"


def test_pass_result_failure_code_is_none() -> None:
    r = check_verdict_blocking({"blocking": True})
    assert r.failure_code is None


def test_blocking_missing_result_shape() -> None:
    r = check_verdict_blocking({"blocking": False})
    assert isinstance(r, BlockingMissingResult)


# ---------------------------------------------------------------------------
# Regression: extra keys do not interfere
# ---------------------------------------------------------------------------


def test_blocking_with_reserved_python_keywords_as_siblings_pass() -> None:
    r = check_verdict_blocking(
        {"blocking": True, "class": "x", "type": "y", "def": "z"}
    )
    assert r.success is True


def test_blocking_key_present_but_value_is_zero_int_denied() -> None:
    r = check_verdict_blocking({"blocking": 0})
    assert r.success is False
    assert r.detail.observed_type == "int"


def test_blocking_key_present_but_value_is_one_int_denied() -> None:
    r = check_verdict_blocking({"blocking": 1})
    assert r.success is False
    assert r.detail.observed_type == "int"
