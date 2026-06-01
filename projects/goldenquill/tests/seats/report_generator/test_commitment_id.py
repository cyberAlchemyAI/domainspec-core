"""Tests for ``pipeline.orchestrator.seats.report_generator._commitment_id``.

Per RT-C2-02 closure: safe-identifier regex ``^[A-Z0-9_-]+$`` with
length bound ``COMMITMENT_ID_MAX_LEN``. Path-traversal mitigation +
filesystem-escape vectors.
"""
from __future__ import annotations

import pytest

from pipeline.orchestrator.seats.report_generator._commitment_id import (
    COMMITMENT_ID_MAX_LEN,
    CommitmentIdInvalid,
    is_safe_commitment_id,
    sanitize_commitment_id,
)


class TestIsSafeCommitmentId:
    @pytest.mark.parametrize(
        "value",
        [
            "COMMIT-001",
            "A",
            "WORKFORCE_TRAINING-FY26",
            "A0_-",
            "ABC123",
        ],
    )
    def test_safe_returns_true(self, value):
        assert is_safe_commitment_id(value)

    @pytest.mark.parametrize(
        "value",
        [
            "",  # empty
            "lowercase",  # lowercase rejected
            "Commit-001",  # mixed case
            "A B",  # whitespace
            "A.B",  # dot
            "A/B",  # path separator
            "A\\B",  # backslash
            "A'B",  # quote
            "A\"B",  # quote
            "../etc/passwd",
            "A" * (COMMITMENT_ID_MAX_LEN + 1),  # too long
            "café-1",  # non-ASCII
        ],
    )
    def test_unsafe_returns_false(self, value):
        assert not is_safe_commitment_id(value)

    def test_non_str_returns_false(self):
        assert not is_safe_commitment_id(None)
        assert not is_safe_commitment_id(123)
        assert not is_safe_commitment_id(b"COMMIT-001")


class TestSanitizeCommitmentId:
    def test_safe_passthrough(self):
        assert sanitize_commitment_id("COMMIT-001") == "COMMIT-001"

    def test_non_str_raises_must_be_str_rule(self):
        with pytest.raises(CommitmentIdInvalid) as ei:
            sanitize_commitment_id(123)
        assert ei.value.rule == "commitment_id_must_be_str"

    def test_empty_raises(self):
        with pytest.raises(CommitmentIdInvalid) as ei:
            sanitize_commitment_id("")
        assert ei.value.rule == "commitment_id_empty_or_too_long"

    def test_too_long_raises(self):
        with pytest.raises(CommitmentIdInvalid) as ei:
            sanitize_commitment_id("A" * (COMMITMENT_ID_MAX_LEN + 1))
        assert ei.value.rule == "commitment_id_empty_or_too_long"

    def test_regex_mismatch_raises(self):
        with pytest.raises(CommitmentIdInvalid) as ei:
            sanitize_commitment_id("lowercase")
        assert ei.value.rule == "commitment_id_regex_mismatch"

    def test_path_traversal_raises(self):
        with pytest.raises(CommitmentIdInvalid) as ei:
            sanitize_commitment_id("../etc")
        assert ei.value.rule == "commitment_id_regex_mismatch"

    def test_exception_str_includes_value_and_rule(self):
        try:
            sanitize_commitment_id("bad value!")
        except CommitmentIdInvalid as exc:
            msg = str(exc)
            assert "bad value!" in msg
            assert "commitment_id_regex_mismatch" in msg
