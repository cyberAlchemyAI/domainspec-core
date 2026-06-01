"""InvocationRecord — per-invocation telemetry record schema.

Blueprint §5 v6 §5.7 LOCKED 2026-04-19.
Eight required fields, immutable after construction, append-only to session log.

Schema evolution (documented 2026-04-19 after adversarial review C1):
The v0.2 Canary harness will correlate STR regressions back to rail-level
attribution. The *attribution* channel is the POST-gate Rails Report (§4.17),
not this record — rails fired are per-RUN, not per-INVOCATION. If a future
expansion genuinely needs per-invocation rail metadata (e.g. mid-run router
mutation audit), that triggers INVOCATION_RECORD_SCHEMA_VERSION=2 with an
explicit migration path. The v1 schema is deliberately minimal to make bumps
cheap and visible. Do not add fields here without bumping the version
constant, updating the module-load assertion, and adding a v1→v2 reader
shim in session_log consumers.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

INVOCATION_RECORD_SCHEMA_VERSION: Final[int] = 1

assert INVOCATION_RECORD_SCHEMA_VERSION == 1, (
    "INVOCATION_RECORD_SCHEMA_VERSION has been rebound at module load; "
    "refusing to load pipeline.observability._record"
)


@dataclass(frozen=True)
class InvocationRecord:
    """Immutable per-invocation telemetry record (§5.7.1).

    All eight fields are required. Validated at construction time.
    Never include in SubmissionBundle or CalibrationReport (§5.7.2 invariant).

    Fields
    ------
    run_id : str
        Pipeline run identifier (UUID-4); bound at start_run / start_eval_run.
    seat : str
        Seat name from router.yaml (e.g. "scribe", "judge", "code_reviewer_1").
    timestamp : str
        ISO 8601 UTC wall-clock time at invocation dispatch (before model round-trip).
    model_family_resolved : str
        Provider-family after fallback resolution (canonical name from router.yaml taxonomy).
    token_count_input : int
        Input-token count from provider response metadata. Minimum 0.
    token_count_output : int
        Output-token count from provider response metadata. Minimum 0.
    success_flag : int
        1 = well-formed accepted response; 0 = error or rejected response. Must be 0 or 1.
    latency_ms : int
        Round-trip latency in milliseconds (dispatch to response-complete).
    """

    run_id: str
    seat: str
    timestamp: str
    model_family_resolved: str
    token_count_input: int
    token_count_output: int
    success_flag: int
    latency_ms: int

    def __post_init__(self) -> None:
        if self.success_flag not in (0, 1):
            raise ValueError(
                f"success_flag must be 0 or 1, got {self.success_flag!r}"
            )
        if self.token_count_input < 0:
            raise ValueError(
                f"token_count_input must be >= 0, got {self.token_count_input}"
            )
        if self.token_count_output < 0:
            raise ValueError(
                f"token_count_output must be >= 0, got {self.token_count_output}"
            )
        if self.latency_ms < 0:
            raise ValueError(
                f"latency_ms must be >= 0, got {self.latency_ms}"
            )
        if not self.run_id:
            raise ValueError("run_id must be non-empty")
        if not self.seat:
            raise ValueError("seat must be non-empty")
        if not self.timestamp:
            raise ValueError("timestamp must be non-empty")
        if not self.model_family_resolved:
            raise ValueError("model_family_resolved must be non-empty")
