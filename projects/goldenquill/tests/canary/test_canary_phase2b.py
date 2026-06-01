"""Phase 2b Canary tests — §4.15 contract verification (v0.1 stub).

Blueprint §4 v2.4 §4.15 LOCKED 2026-04-19.
"""

from __future__ import annotations

import pytest

from pipeline.canary import (
    CanaryVerdict,
    CanaryResult,
    run_canary_gate,
    F_CANARY_STR_REGRESSION,
    F_CANARY_SCORE_REGRESSION,
    F_CANARY_TEST_VECTORS_MISSING,
)


class TestCanaryStub:
    """v0.1 stub: always STUB_BLOCKED with F-CANARY-TEST-VECTORS-MISSING."""

    def test_stub_returns_stub_blocked(self):
        result = run_canary_gate("hash-a", "hash-b")
        assert result.verdict == CanaryVerdict.STUB_BLOCKED

    def test_stub_failure_code_test_vectors_missing(self):
        result = run_canary_gate("hash-a", "hash-b")
        assert result.failure_code == F_CANARY_TEST_VECTORS_MISSING

    def test_stub_blocks_regardless_of_corpus_path(self):
        result = run_canary_gate("hash-a", "hash-b", test_vector_corpus_path="/some/path")
        assert result.verdict == CanaryVerdict.STUB_BLOCKED

    def test_stub_blocks_with_none_corpus_path(self):
        result = run_canary_gate("hash-a", "hash-b", test_vector_corpus_path=None)
        assert result.verdict == CanaryVerdict.STUB_BLOCKED

    def test_stub_detail_contains_reason(self):
        result = run_canary_gate("hash-a", "hash-b")
        assert result.detail is not None
        assert result.detail["reason"] == "v0.1_stub_no_corpus_interface"

    def test_stub_same_hash_still_blocked(self):
        result = run_canary_gate("same-hash", "same-hash")
        assert result.verdict == CanaryVerdict.STUB_BLOCKED

    def test_result_is_frozen(self):
        result = run_canary_gate("hash-a", "hash-b")
        with pytest.raises((AttributeError, TypeError)):
            result.verdict = CanaryVerdict.PROMOTED  # type: ignore[misc]

    def test_canary_verdict_values(self):
        assert CanaryVerdict.STUB_BLOCKED == "STUB_BLOCKED"
        assert CanaryVerdict.PROMOTED == "PROMOTED"

    def test_failure_code_constants(self):
        assert F_CANARY_STR_REGRESSION == "F-CANARY-STR-REGRESSION"
        assert F_CANARY_SCORE_REGRESSION == "F-CANARY-SCORE-REGRESSION"
        assert F_CANARY_TEST_VECTORS_MISSING == "F-CANARY-TEST-VECTORS-MISSING"
