"""Adversarial tests for F-VERDICT-CITATION-MISSING (F-AMDT-03).

Threat model (spec card v1, 2026-04-20):
  * Draft-reader failure (file missing, permission denied, OSError) must
    fail-closed with a typed ``reader_raised`` reason, not propagate the
    raw exception upward.
  * Whitespace-only evidence — ``"   "`` splits to ``[]``; tokens-list
    empty; gate must DENY (treat as no citation, not vacuous PASS).
  * Evidence that resolves against ONE draft but not the draft indicated
    by ``draft_path`` — gate must consult the path-bound reader result,
    not some stashed global text.
  * Unicode-only tokens with decomposed vs. composed forms — substring
    match is byte/grapheme-exact; composed ≠ decomposed by design.
  * ``dimensions`` field is a dict or string — structural DENY.
  * Reader returning huge string — gate must not time out or skip tokens.
"""

from __future__ import annotations

import pytest

from pipeline.logician.gates import (
    F_AMDT_03,
    DraftReaderCallable,
    check_verdict_citations,
)


def test_adv_draft_reader_raises() -> None:
    """Reader raises FileNotFoundError — gate fail-closed, does not propagate."""

    def _bad_reader(_: str) -> str:
        raise FileNotFoundError("no such file: d.md")

    r = check_verdict_citations(
        verdict_json={"dimensions": [{"name": "x", "evidence": "tok"}]},
        draft_path="d.md",
        draft_reader=_bad_reader,
    )
    assert r.success is False
    assert r.failure_code == F_AMDT_03
    assert r.detail.reason_tag == "draft_reader_raised"
    assert "FileNotFoundError" in (r.detail.reader_error or "")


def test_adv_draft_reader_raises_oserror() -> None:
    def _bad_reader(_: str) -> str:
        raise OSError("permission denied")

    r = check_verdict_citations(
        verdict_json={"dimensions": [{"name": "x", "evidence": "tok"}]},
        draft_path="d.md",
        draft_reader=_bad_reader,
    )
    assert r.success is False
    assert r.detail.reason_tag == "draft_reader_raised"
    assert "OSError" in (r.detail.reader_error or "")


def test_adv_draft_reader_raises_custom_exception() -> None:
    class VaultUnavailable(RuntimeError):
        pass

    def _bad_reader(_: str) -> str:
        raise VaultUnavailable("vault node offline")

    r = check_verdict_citations(
        verdict_json={"dimensions": [{"name": "x", "evidence": "tok"}]},
        draft_path="d.md",
        draft_reader=_bad_reader,
    )
    assert r.success is False
    assert r.detail.reason_tag == "draft_reader_raised"
    assert "VaultUnavailable" in (r.detail.reader_error or "")


def test_adv_evidence_is_whitespace_only() -> None:
    """``"   "`` → ``split()`` returns ``[]`` — DENY (no citation)."""
    def _reader(_: str) -> str:
        return "draft with content"

    for ws in ("   ", "\t\t", "\n\n", " \t\n ", "\u00a0\u00a0"):
        r = check_verdict_citations(
            verdict_json={"dimensions": [{"name": "x", "evidence": ws}]},
            draft_path="d.md",
            draft_reader=_reader,
        )
        assert r.success is False, f"whitespace-only {ws!r} wrongly passed"
        # "\u00a0" is a non-breaking space — str.split() DOES split on it;
        # the result is ``[]`` if the entire string is NBSPs.
        assert r.detail.failed_dimensions[0].reason_tag == "evidence_whitespace_only"


def test_adv_evidence_matches_different_draft() -> None:
    """Evidence resolves against draft B text but gate is given draft A via
    ``draft_path``. The injected reader is the single source of truth; the
    gate cannot be fooled by evidence that happens to match some other
    draft's text."""
    draft_a = "alpha beta gamma"
    # draft_b = "zzz_unique_token"  # used only conceptually — gate never sees it

    def _reader_a(_: str) -> str:
        return draft_a

    r = check_verdict_citations(
        verdict_json={
            "dimensions": [{"name": "x", "evidence": "zzz_unique_token"}]
        },
        draft_path="d_a.md",
        draft_reader=_reader_a,
    )
    assert r.success is False
    assert r.detail.failed_dimensions[0].missing_tokens == ("zzz_unique_token",)


def test_adv_unicode_token_resolution() -> None:
    """Evidence with Unicode characters that appear in draft → PASS."""
    draft_unicode = "Yaxché tree spans agroforestry plots. 栽培 is cultivation."

    def _reader(_: str) -> str:
        return draft_unicode

    r = check_verdict_citations(
        verdict_json={"dimensions": [{"name": "x", "evidence": "Yaxché 栽培"}]},
        draft_path="d.md",
        draft_reader=_reader,
    )
    assert r.success is True


def test_adv_unicode_composed_vs_decomposed_not_normalized() -> None:
    """Composed é (\u00e9) vs decomposed e + combining acute (e\u0301) are
    DIFFERENT byte sequences. The gate does not normalise; exact substring
    match required. Documents strict-bytes behaviour."""
    draft_composed = "caf\u00e9"  # "café" with single composed codepoint
    evidence_decomposed = "cafe\u0301"  # "cafe" + combining acute

    def _reader(_: str) -> str:
        return draft_composed

    r = check_verdict_citations(
        verdict_json={"dimensions": [{"name": "x", "evidence": evidence_decomposed}]},
        draft_path="d.md",
        draft_reader=_reader,
    )
    assert r.success is False
    assert r.detail.failed_dimensions[0].reason_tag == "evidence_tokens_unresolved"


def test_adv_dimensions_is_tuple() -> None:
    """A tuple is not a list — gate must DENY structurally."""
    r = check_verdict_citations(
        verdict_json={"dimensions": ({"name": "x", "evidence": "tok"},)},
        draft_path="d.md",
        draft_reader=lambda _: "tok in draft",
    )
    assert r.success is False
    assert r.detail.reason_tag == "dimensions_not_list"


def test_adv_dimensions_is_none() -> None:
    r = check_verdict_citations(
        verdict_json={"dimensions": None},
        draft_path="d.md",
        draft_reader=lambda _: "draft",
    )
    assert r.success is False
    assert r.detail.reason_tag == "dimensions_not_list"


def test_adv_reader_returns_empty_string_all_evidence_fails() -> None:
    """Empty draft — every non-empty evidence token fails to resolve."""
    r = check_verdict_citations(
        verdict_json={
            "dimensions": [
                {"name": "a", "evidence": "x"},
                {"name": "b", "evidence": "y z"},
            ]
        },
        draft_path="d.md",
        draft_reader=lambda _: "",
    )
    assert r.success is False
    assert len(r.detail.failed_dimensions) == 2


def test_adv_evidence_contains_embedded_null_byte() -> None:
    """A token containing a NUL byte — substring match still works in Python
    strings; if NUL is in draft, it matches; else DENY."""
    draft = "clean ascii with\x00embedded null"

    def _reader(_: str) -> str:
        return draft

    r_pass = check_verdict_citations(
        verdict_json={"dimensions": [{"name": "x", "evidence": "with\x00embedded"}]},
        draft_path="d.md",
        draft_reader=_reader,
    )
    assert r_pass.success is True

    r_fail = check_verdict_citations(
        verdict_json={"dimensions": [{"name": "x", "evidence": "absent\x00token"}]},
        draft_path="d.md",
        draft_reader=_reader,
    )
    assert r_fail.success is False


def test_adv_dimension_entry_is_none() -> None:
    r = check_verdict_citations(
        verdict_json={"dimensions": [None, {"name": "x", "evidence": "tok"}]},
        draft_path="d.md",
        draft_reader=lambda _: "tok in draft",
    )
    assert r.success is False
    assert r.detail.failed_dimensions[0].reason_tag == "dimension_entry_not_dict"
    assert r.detail.failed_dimensions[0].dimension_index == 0
