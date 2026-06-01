"""Canary edit-time lock-validation replay gate stub (v0.1).

Blueprint §4 v2.4 §4.15 LOCKED 2026-04-19.
v0.1: stub always returns STUB_BLOCKED (fail-closed — no test-vector corpus
interface pinned in v0.1). Real harness wired at v0.2.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Final

BLUEPRINT_DEPS: Final[dict] = {
    "section_04_v2_4_v2_5_amendment.md": {
        "sections_implemented": ["§4.15 Canary edit-time gate (v0.1 stub)"],
        "hash_source_version": "v2.4",
    },
}

F_CANARY_STR_REGRESSION: Final[str] = "F-CANARY-STR-REGRESSION"
F_CANARY_SCORE_REGRESSION: Final[str] = "F-CANARY-SCORE-REGRESSION"
F_CANARY_TEST_VECTORS_MISSING: Final[str] = "F-CANARY-TEST-VECTORS-MISSING"


class CanaryVerdict(str, Enum):
    """Canary gate verdict [§4.15]."""

    PROMOTED = "PROMOTED"
    BLOCKED_STR_REGRESSION = "BLOCKED_STR_REGRESSION"
    BLOCKED_SCORE_REGRESSION = "BLOCKED_SCORE_REGRESSION"
    BLOCKED_TEST_VECTORS_MISSING = "BLOCKED_TEST_VECTORS_MISSING"
    BLOCKED_FAMILY_COLLISION = "BLOCKED_FAMILY_COLLISION"
    STUB_BLOCKED = "STUB_BLOCKED"


@dataclass(frozen=True)
class CanaryResult:
    """Result of the Canary gate (§4.15)."""

    verdict: CanaryVerdict
    failure_code: str | None
    detail: dict[str, Any] | None


def run_canary_gate(
    candidate_router_hash: str,
    baseline_router_hash: str,
    test_vector_corpus_path: str | None = None,
) -> CanaryResult:
    """Canary edit-time lock-validation replay gate (§4.15). [v0.1 stub]

    Always returns STUB_BLOCKED in v0.1 — no locked-test-vector corpus interface
    pinned yet. v0.2 replaces with real STR + score regression replay harness.
    """
    _ = candidate_router_hash, baseline_router_hash, test_vector_corpus_path
    return CanaryResult(
        verdict=CanaryVerdict.STUB_BLOCKED,
        failure_code=F_CANARY_TEST_VECTORS_MISSING,
        detail={"reason": "v0.1_stub_no_corpus_interface"},
    )
