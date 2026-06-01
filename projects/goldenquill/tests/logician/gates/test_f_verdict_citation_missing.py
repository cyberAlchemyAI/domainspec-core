"""Unit tests for F-VERDICT-CITATION-MISSING (F-AMDT-03).

≥30 unit tests per spec card. Adversarial tests live in
``test_adv_f_verdict_citation_missing.py``.
"""

from __future__ import annotations

import pytest

from pipeline.logician.gates import (
    F_AMDT_03,
    CitationMissingResult,
    DraftReaderCallable,
    check_verdict_citations,
)


# ---------------------------------------------------------------------------
# Fixtures / helpers
# ---------------------------------------------------------------------------


def _stub_reader(text: str) -> DraftReaderCallable:
    def _reader(draft_path: str) -> str:
        return text

    return _reader


_DRAFT_A = (
    "The project will plant 5,000 oyster mushroom bags across 3 counties.\n"
    "Budget requests $48,000 for mycelium substrate and labor.\n"
    "Partner organizations include MycoSymbiotics Cooperative and FIT Farms.\n"
)


# ---------------------------------------------------------------------------
# Happy path — evidence resolves
# ---------------------------------------------------------------------------


def test_single_dimension_single_token_pass() -> None:
    r = check_verdict_citations(
        verdict_json={"dimensions": [{"name": "budget", "evidence": "$48,000"}]},
        draft_path="d.md",
        draft_reader=_stub_reader(_DRAFT_A),
    )
    assert r.success is True
    assert r.failure_code is None
    assert r.detail is None


def test_single_dimension_multi_token_all_resolve_pass() -> None:
    r = check_verdict_citations(
        verdict_json={
            "dimensions": [{"name": "scope", "evidence": "5,000 oyster mushroom bags"}]
        },
        draft_path="d.md",
        draft_reader=_stub_reader(_DRAFT_A),
    )
    assert r.success is True


def test_multiple_dimensions_all_resolve_pass() -> None:
    r = check_verdict_citations(
        verdict_json={
            "dimensions": [
                {"name": "scope", "evidence": "5,000"},
                {"name": "budget", "evidence": "$48,000"},
                {"name": "partners", "evidence": "MycoSymbiotics"},
            ]
        },
        draft_path="d.md",
        draft_reader=_stub_reader(_DRAFT_A),
    )
    assert r.success is True


def test_substring_match_within_word_pass() -> None:
    r = check_verdict_citations(
        verdict_json={"dimensions": [{"name": "partners", "evidence": "Symbiotics"}]},
        draft_path="d.md",
        draft_reader=_stub_reader(_DRAFT_A),
    )
    assert r.success is True


def test_empty_dimensions_list_vacuous_pass() -> None:
    r = check_verdict_citations(
        verdict_json={"dimensions": []},
        draft_path="d.md",
        draft_reader=_stub_reader(_DRAFT_A),
    )
    assert r.success is True


# ---------------------------------------------------------------------------
# Evidence structural failures
# ---------------------------------------------------------------------------


def test_evidence_key_absent_denied() -> None:
    r = check_verdict_citations(
        verdict_json={"dimensions": [{"name": "scope", "score": 10}]},
        draft_path="d.md",
        draft_reader=_stub_reader(_DRAFT_A),
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_03
    assert len(r.detail.failed_dimensions) == 1
    assert r.detail.failed_dimensions[0].reason_tag == "evidence_key_absent"
    assert r.detail.failed_dimensions[0].dimension_index == 0
    assert r.detail.failed_dimensions[0].dimension_name == "scope"


def test_evidence_empty_string_denied() -> None:
    r = check_verdict_citations(
        verdict_json={"dimensions": [{"name": "scope", "evidence": ""}]},
        draft_path="d.md",
        draft_reader=_stub_reader(_DRAFT_A),
    )
    assert r.success is False
    assert r.detail.failed_dimensions[0].reason_tag == "evidence_empty"


def test_evidence_integer_denied() -> None:
    r = check_verdict_citations(
        verdict_json={"dimensions": [{"name": "scope", "evidence": 48000}]},
        draft_path="d.md",
        draft_reader=_stub_reader(_DRAFT_A),
    )
    assert r.success is False
    assert r.detail.failed_dimensions[0].reason_tag == "evidence_not_string"


def test_evidence_list_denied() -> None:
    r = check_verdict_citations(
        verdict_json={
            "dimensions": [{"name": "scope", "evidence": ["5,000", "bags"]}]
        },
        draft_path="d.md",
        draft_reader=_stub_reader(_DRAFT_A),
    )
    assert r.success is False
    assert r.detail.failed_dimensions[0].reason_tag == "evidence_not_string"


def test_evidence_none_denied() -> None:
    r = check_verdict_citations(
        verdict_json={"dimensions": [{"name": "scope", "evidence": None}]},
        draft_path="d.md",
        draft_reader=_stub_reader(_DRAFT_A),
    )
    assert r.success is False
    assert r.detail.failed_dimensions[0].reason_tag == "evidence_not_string"


# ---------------------------------------------------------------------------
# Token resolution failures
# ---------------------------------------------------------------------------


def test_single_token_not_in_draft_denied() -> None:
    r = check_verdict_citations(
        verdict_json={"dimensions": [{"name": "scope", "evidence": "hyperloop"}]},
        draft_path="d.md",
        draft_reader=_stub_reader(_DRAFT_A),
    )
    assert r.success is False
    f = r.detail.failed_dimensions[0]
    assert f.reason_tag == "evidence_tokens_unresolved"
    assert f.missing_tokens == ("hyperloop",)


def test_multi_token_last_missing_denied() -> None:
    r = check_verdict_citations(
        verdict_json={
            "dimensions": [{"name": "scope", "evidence": "5,000 bags hyperloop"}]
        },
        draft_path="d.md",
        draft_reader=_stub_reader(_DRAFT_A),
    )
    assert r.success is False
    f = r.detail.failed_dimensions[0]
    assert f.missing_tokens == ("hyperloop",)


def test_multi_token_multiple_missing_denied() -> None:
    r = check_verdict_citations(
        verdict_json={
            "dimensions": [{"name": "scope", "evidence": "alpha beta 5,000 gamma"}]
        },
        draft_path="d.md",
        draft_reader=_stub_reader(_DRAFT_A),
    )
    assert r.success is False
    f = r.detail.failed_dimensions[0]
    assert f.missing_tokens == ("alpha", "beta", "gamma")


def test_empty_draft_denies_nonempty_evidence() -> None:
    r = check_verdict_citations(
        verdict_json={"dimensions": [{"name": "scope", "evidence": "anything"}]},
        draft_path="d.md",
        draft_reader=_stub_reader(""),
    )
    assert r.success is False
    assert r.detail.failed_dimensions[0].reason_tag == "evidence_tokens_unresolved"


def test_case_sensitive_match_budget_vs_Budget() -> None:
    # Draft contains "Budget" (capital B). Evidence "budget" (lowercase) must FAIL.
    r = check_verdict_citations(
        verdict_json={"dimensions": [{"name": "budget", "evidence": "budget"}]},
        draft_path="d.md",
        draft_reader=_stub_reader(_DRAFT_A),
    )
    assert r.success is False
    assert r.detail.failed_dimensions[0].missing_tokens == ("budget",)


def test_case_sensitive_match_Budget_pass() -> None:
    r = check_verdict_citations(
        verdict_json={"dimensions": [{"name": "budget", "evidence": "Budget"}]},
        draft_path="d.md",
        draft_reader=_stub_reader(_DRAFT_A),
    )
    assert r.success is True


# ---------------------------------------------------------------------------
# Partial-failure surfaces — some pass, some fail
# ---------------------------------------------------------------------------


def test_multiple_dimensions_one_fails_lists_failing_dim() -> None:
    r = check_verdict_citations(
        verdict_json={
            "dimensions": [
                {"name": "scope", "evidence": "5,000"},
                {"name": "bogus", "evidence": "zzz_not_in_draft"},
                {"name": "budget", "evidence": "$48,000"},
            ]
        },
        draft_path="d.md",
        draft_reader=_stub_reader(_DRAFT_A),
    )
    assert r.success is False
    assert len(r.detail.failed_dimensions) == 1
    assert r.detail.failed_dimensions[0].dimension_index == 1
    assert r.detail.failed_dimensions[0].dimension_name == "bogus"


def test_multiple_dimensions_all_fail() -> None:
    r = check_verdict_citations(
        verdict_json={
            "dimensions": [
                {"name": "a", "evidence": "nope1"},
                {"name": "b", "evidence": "nope2"},
                {"name": "c", "evidence": "nope3"},
            ]
        },
        draft_path="d.md",
        draft_reader=_stub_reader(_DRAFT_A),
    )
    assert r.success is False
    assert len(r.detail.failed_dimensions) == 3


# ---------------------------------------------------------------------------
# Structural verdict failures
# ---------------------------------------------------------------------------


def test_verdict_not_dict_denied() -> None:
    r = check_verdict_citations(
        verdict_json=["dimensions", []],
        draft_path="d.md",
        draft_reader=_stub_reader(_DRAFT_A),
    )
    assert r.success is False
    assert r.detail.reason_tag == "verdict_not_dict"


def test_dimensions_key_absent_denied() -> None:
    r = check_verdict_citations(
        verdict_json={"blocking": False, "rationale": "text"},
        draft_path="d.md",
        draft_reader=_stub_reader(_DRAFT_A),
    )
    assert r.success is False
    assert r.detail.reason_tag == "dimensions_key_absent"


def test_dimensions_is_dict_denied() -> None:
    r = check_verdict_citations(
        verdict_json={"dimensions": {"scope": {"evidence": "x"}}},
        draft_path="d.md",
        draft_reader=_stub_reader(_DRAFT_A),
    )
    assert r.success is False
    assert r.detail.reason_tag == "dimensions_not_list"


def test_dimensions_is_string_denied() -> None:
    r = check_verdict_citations(
        verdict_json={"dimensions": "all good"},
        draft_path="d.md",
        draft_reader=_stub_reader(_DRAFT_A),
    )
    assert r.success is False
    assert r.detail.reason_tag == "dimensions_not_list"


def test_dimensions_entry_not_dict_denied() -> None:
    r = check_verdict_citations(
        verdict_json={"dimensions": ["not a dict"]},
        draft_path="d.md",
        draft_reader=_stub_reader(_DRAFT_A),
    )
    assert r.success is False
    assert r.detail.failed_dimensions[0].reason_tag == "dimension_entry_not_dict"


# ---------------------------------------------------------------------------
# Dimension-name fallback — name field missing or non-string
# ---------------------------------------------------------------------------


def test_dimension_without_name_field_reports_none() -> None:
    r = check_verdict_citations(
        verdict_json={"dimensions": [{"evidence": "missing_tok"}]},
        draft_path="d.md",
        draft_reader=_stub_reader(_DRAFT_A),
    )
    assert r.success is False
    assert r.detail.failed_dimensions[0].dimension_name is None


def test_dimension_name_non_string_reports_none() -> None:
    r = check_verdict_citations(
        verdict_json={"dimensions": [{"name": 42, "evidence": "missing_tok"}]},
        draft_path="d.md",
        draft_reader=_stub_reader(_DRAFT_A),
    )
    assert r.success is False
    assert r.detail.failed_dimensions[0].dimension_name is None


# ---------------------------------------------------------------------------
# Parametrized dimension counts
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("n", [1, 3, 7, 12])
def test_parametrized_n_dimensions_all_valid_pass(n: int) -> None:
    dims = [{"name": f"d{i}", "evidence": "5,000"} for i in range(n)]
    r = check_verdict_citations(
        verdict_json={"dimensions": dims},
        draft_path="d.md",
        draft_reader=_stub_reader(_DRAFT_A),
    )
    assert r.success is True


@pytest.mark.parametrize("n", [1, 3, 7, 12])
def test_parametrized_n_dimensions_all_invalid_denied(n: int) -> None:
    dims = [{"name": f"d{i}", "evidence": f"zzz_{i}"} for i in range(n)]
    r = check_verdict_citations(
        verdict_json={"dimensions": dims},
        draft_path="d.md",
        draft_reader=_stub_reader(_DRAFT_A),
    )
    assert r.success is False
    assert len(r.detail.failed_dimensions) == n


# ---------------------------------------------------------------------------
# Reader contract
# ---------------------------------------------------------------------------


def test_reader_receives_exact_draft_path() -> None:
    captured: list[str] = []

    def _reader(draft_path: str) -> str:
        captured.append(draft_path)
        return _DRAFT_A

    r = check_verdict_citations(
        verdict_json={"dimensions": [{"name": "x", "evidence": "5,000"}]},
        draft_path="orgs/fit_farms/drafts/v1.md",
        draft_reader=_reader,
    )
    assert r.success is True
    assert captured == ["orgs/fit_farms/drafts/v1.md"]


def test_reader_returns_non_string_denied() -> None:
    def _reader(_: str) -> str:
        return b"bytes not str"  # type: ignore[return-value]

    r = check_verdict_citations(
        verdict_json={"dimensions": [{"name": "x", "evidence": "5,000"}]},
        draft_path="d.md",
        draft_reader=_reader,
    )
    assert r.success is False
    assert r.detail.reason_tag == "draft_reader_raised"
    assert "expected str" in (r.detail.reader_error or "")


def test_reader_is_not_called_if_structural_fail_first() -> None:
    calls = {"n": 0}

    def _reader(_: str) -> str:
        calls["n"] += 1
        return _DRAFT_A

    r = check_verdict_citations(
        verdict_json={},
        draft_path="d.md",
        draft_reader=_reader,
    )
    assert r.success is False
    assert calls["n"] == 0


# ---------------------------------------------------------------------------
# Result invariants
# ---------------------------------------------------------------------------


def test_pass_result_shape_is_citation_missing_result() -> None:
    r = check_verdict_citations(
        verdict_json={"dimensions": []},
        draft_path="d.md",
        draft_reader=_stub_reader(_DRAFT_A),
    )
    assert isinstance(r, CitationMissingResult)
    assert r.failure_code is None
    assert r.detail is None


def test_failure_code_constant_matches_spec_card() -> None:
    assert F_AMDT_03 == "F-AMDT-03"


def test_result_is_immutable() -> None:
    r = check_verdict_citations(
        verdict_json={"dimensions": []},
        draft_path="d.md",
        draft_reader=_stub_reader(_DRAFT_A),
    )
    with pytest.raises((AttributeError, Exception)):
        r.success = False  # type: ignore[misc]


# ---------------------------------------------------------------------------
# Token / whitespace edge cases
# ---------------------------------------------------------------------------


def test_evidence_with_tabs_and_newlines_tokenized() -> None:
    r = check_verdict_citations(
        verdict_json={
            "dimensions": [{"name": "x", "evidence": "5,000\toyster\nmushroom"}]
        },
        draft_path="d.md",
        draft_reader=_stub_reader(_DRAFT_A),
    )
    assert r.success is True


def test_evidence_with_repeated_token_pass() -> None:
    r = check_verdict_citations(
        verdict_json={"dimensions": [{"name": "x", "evidence": "5,000 5,000 5,000"}]},
        draft_path="d.md",
        draft_reader=_stub_reader(_DRAFT_A),
    )
    assert r.success is True


def test_evidence_multi_token_substring_matches_within_words() -> None:
    # "counties" is in draft — "count" is a substring of "counties".
    r = check_verdict_citations(
        verdict_json={"dimensions": [{"name": "x", "evidence": "count"}]},
        draft_path="d.md",
        draft_reader=_stub_reader(_DRAFT_A),
    )
    assert r.success is True
