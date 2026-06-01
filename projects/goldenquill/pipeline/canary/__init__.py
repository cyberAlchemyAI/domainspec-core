"""pipeline.canary — Canary edit-time lock-validation replay gate (§4.15).

Blueprint reference: pipeline/blueprint/v0.1/section_04_v2_4_v2_5_amendment.md §4.15 LOCKED 2026-04-19.
v0.1: stub. v0.2: real harness.
"""

from pipeline.canary._harness import (
    CanaryVerdict,
    CanaryResult,
    run_canary_gate,
    F_CANARY_STR_REGRESSION,
    F_CANARY_SCORE_REGRESSION,
    F_CANARY_TEST_VECTORS_MISSING,
)

__all__ = [
    "CanaryVerdict",
    "CanaryResult",
    "run_canary_gate",
    "F_CANARY_STR_REGRESSION",
    "F_CANARY_SCORE_REGRESSION",
    "F_CANARY_TEST_VECTORS_MISSING",
]
