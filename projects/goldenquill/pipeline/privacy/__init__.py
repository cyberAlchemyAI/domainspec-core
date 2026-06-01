"""pipeline.privacy — Privacy Router PRE-gate (§4.14).

Blueprint reference: pipeline/blueprint/v0.1/section_04_v2_3_amendment.md §4.14 LOCKED 2026-04-19.
"""

from pipeline.privacy._classifier import PrivacyTag
from pipeline.privacy._router import (
    PrivacyRouteResult,
    run_privacy_pregate,
    PRIVACY_FAILURE_CODE_CLASSIFIER_ERROR,
    PRIVACY_FAILURE_CODE_BYPASS_ATTEMPT,
)

__all__ = [
    "PrivacyTag",
    "PrivacyRouteResult",
    "run_privacy_pregate",
    "PRIVACY_FAILURE_CODE_CLASSIFIER_ERROR",
    "PRIVACY_FAILURE_CODE_BYPASS_ATTEMPT",
]
