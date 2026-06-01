"""pipeline.observability — per-invocation record emission, STR derivation, and rolling-window accumulation.

Blueprint reference: pipeline/blueprint/v0.1/section_05_pipeline.md §5 v6 §5.7-§5.8 LOCKED 2026-04-19.
"""

from pipeline.observability._record import InvocationRecord, INVOCATION_RECORD_SCHEMA_VERSION
from pipeline.observability._str_window import (
    STRWindow,
    compute_str,
    STRWindowResult,
    STR_WINDOW_MIN_SESSIONS,
    STR_WINDOW_MAX_AGE_DAYS,
)

__all__ = [
    "InvocationRecord",
    "INVOCATION_RECORD_SCHEMA_VERSION",
    "STRWindow",
    "STRWindowResult",
    "compute_str",
    "STR_WINDOW_MIN_SESSIONS",
    "STR_WINDOW_MAX_AGE_DAYS",
]
