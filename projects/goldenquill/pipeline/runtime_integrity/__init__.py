"""pipeline.runtime_integrity — Runtime Integrity family (§4.16-§4.17 + §4.2.1 Rows 22-23).

Blueprint reference: pipeline/blueprint/v0.1/section_04_v2_4_v2_5_amendment.md §4.16-§4.17 LOCKED 2026-04-19.
"""

from pipeline.runtime_integrity._family_collision import (
    FamilyCollisionResult,
    check_family_collision,
    F_ROUTER_FAMILY_COLLISION,
)
from pipeline.runtime_integrity._key_presence import (
    KeyPresenceResult,
    check_key_presence,
    F_KEY_PRESENCE_PREFLIGHT_FAIL,
)
from pipeline.runtime_integrity._router_drift import (
    RouterDriftResult,
    check_router_drift,
    canonical_bytes_sha3_512,
    F_RUNTIME_DRIFT_FROM_LOCKED_ROUTER,
)
from pipeline.runtime_integrity._rails_report import (
    RailsReportResult,
    emit_rails_report,
    F_RAILS_REPORT_EMISSION_FAIL,
)

__all__ = [
    "FamilyCollisionResult",
    "check_family_collision",
    "F_ROUTER_FAMILY_COLLISION",
    "KeyPresenceResult",
    "check_key_presence",
    "F_KEY_PRESENCE_PREFLIGHT_FAIL",
    "RouterDriftResult",
    "check_router_drift",
    "canonical_bytes_sha3_512",
    "F_RUNTIME_DRIFT_FROM_LOCKED_ROUTER",
    "RailsReportResult",
    "emit_rails_report",
    "F_RAILS_REPORT_EMISSION_FAIL",
]
