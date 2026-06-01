"""pipeline.loop.types — §5 v6 data structures (shape-only, zero algorithm).

Blueprint §5 v6 LOCKED 2026-04-19:
- §3.2.1 RunState (v4 mode-discriminated union + eval-mode phases)
- §3.2.2 IterationState
- §3.2.3 SeatCharter
- §3.2.4 ProviderCascade
- §3.2.5 RateLimiterState (v2 lease fields)
- §3.2.6 TabEnvelope (v2 Final tab_ordering)
- §5.6.1 GoldenSetItem
- §5.6.2 CalibrationReportItem
- §5.6.3 CalibrationReport

Round 1 ships only *shape* — ``__post_init__`` enforces construction-time
invariants (mode-discriminated union, tab-ordering literal check, schema
version equality, numeric-range bounds). Algorithmic behaviour (checkpoint,
resume, revision loop) lives in Rounds 2-12.

Every frozen dataclass below is ``kw_only=True`` so that field additions in
v0.2 cannot silently reorder positional calls.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Final, Literal, Protocol, TypeAlias, runtime_checkable

from pipeline.loop.config import (
    CALIBRATION_REPORT_SCHEMA_VERSION,
    MAX_REVISION_ITERATIONS,
    RUNSTATE_SCHEMA_VERSION,
)
from pipeline.loop.errors import F_PIPE_16, F_PIPE_21, F_PIPE_22

BLUEPRINT_DEPS: Final[dict[str, dict[str, object]]] = {
    "section_05_pipeline.md": {
        "version": "v6",
        "hash_sha3_512_prefix16": "feb5928491e4dc40",
        "sections_implemented": [
            "§3.2.1 RunState (v4 mode + v2 schema_version)",
            "§3.2.2 IterationState",
            "§3.2.3 SeatCharter",
            "§3.2.4 ProviderCascade",
            "§3.2.5 RateLimiterState (v2 lease)",
            "§3.2.6 TabEnvelope (v2 Final tab_ordering)",
            "§5.6.1 GoldenSetItem",
            "§5.6.2 CalibrationReportItem",
            "§5.6.3 CalibrationReport",
        ],
    },
}

# ---------------------------------------------------------------------------
# Type aliases
# ---------------------------------------------------------------------------

RunMode: TypeAlias = Literal["submission", "eval"]

RunPhase: TypeAlias = Literal[
    "initialized",
    "pre_gate_pending",
    "pre_gate_passed",
    "inner_loop_iter_1",
    "inner_loop_iter_2",
    "inner_loop_iter_3",
    "post_gate_pending",
    "post_gate_passed",
    "signoff_pending",
    "signoff_pending_council_split",  # v7 NEW: F-COUNCIL-SPLIT routes here from POST-gate
    "report_signed",
    "tabs_delivered",
    "finalized",
    "degraded_paused",
    "aborted_trusted_fail",
    "aborted_operator",
    "quarantined",
    "eval_iter_pending",
    "calibration_assembled",
    "calibration_signed",
    "eval_finalized",
]

SeatKind: TypeAlias = Literal["scribe", "editor", "judge", "red_team"]

IntentKind: TypeAlias = Literal[
    "state-success",
    "state-failure",
    "state-quarantine",
    "golden-set-read",
    "golden-set-write",
    "three-tab-deliver",
    "bypass-pending",
    "bypass-authorization",
    "admin-risk-append",
    "cron-stamp",
]


# Inline-literal RHS sets used at runtime to catch module-attribute rebinds
# (V1 discipline — the RHS is a fresh literal at every comparison site).
_RUNPHASE_VALID_SET: Final[frozenset[str]] = frozenset(
    {
        "initialized",
        "pre_gate_pending",
        "pre_gate_passed",
        "inner_loop_iter_1",
        "inner_loop_iter_2",
        "inner_loop_iter_3",
        "post_gate_pending",
        "post_gate_passed",
        "signoff_pending",
        "signoff_pending_council_split",  # v7 NEW
        "report_signed",
        "tabs_delivered",
        "finalized",
        "degraded_paused",
        "aborted_trusted_fail",
        "aborted_operator",
        "quarantined",
        "eval_iter_pending",
        "calibration_assembled",
        "calibration_signed",
        "eval_finalized",
    }
)
assert len(_RUNPHASE_VALID_SET) == 21, (
    "_RUNPHASE_VALID_SET has been rebound at module load; "
    "refusing to load pipeline.loop.types"
)

_SEATKIND_VALID_SET: Final[frozenset[str]] = frozenset(
    {"scribe", "editor", "judge", "red_team"}
)
assert len(_SEATKIND_VALID_SET) == 4, (
    "_SEATKIND_VALID_SET has been rebound at module load; "
    "refusing to load pipeline.loop.types"
)


# ---------------------------------------------------------------------------
# Round-7-forward-dep: TokenBucket shape (declared here so RateLimiterState
# typechecks today; Round 7 rate_limiter.py supplies the concrete class)
# ---------------------------------------------------------------------------


@runtime_checkable
class TokenBucketProtocol(Protocol):
    """Round-7-owned shape; declared here so RateLimiterState typechecks in Round 1.

    Round 7 (rate_limiter.py) provides the concrete implementation. Round 1
    consumers (if any) treat the protocol as opaque — they do not call
    methods on it; they only pass it through RateLimiterState.
    """

    capacity: int
    tokens: float
    refill_rate_per_sec: float


# ---------------------------------------------------------------------------
# §3.2.2 IterationState (v1 unchanged)
# ---------------------------------------------------------------------------


@dataclass(slots=True, kw_only=True)
class IterationState:
    """§3.2.2 — one revision-loop iteration.

    iter_number is 1-indexed; ``1 <= iter_number <= MAX_REVISION_ITERATIONS``.
    seat_draft_hashes accumulates the per-seat draft hash as the iteration
    progresses through Scribe → Editor → Judge.
    """

    iter_number: int
    seat_draft_hashes: dict[str, str] = field(default_factory=dict)
    judge_verdict: dict[str, Any] | None = None
    red_team_verdict: dict[str, Any] | None = None  # v7 NEW (§5 v7 amendment §4.5a)
    failure_code: str | None = None
    started_at_iso: str = ""
    completed_at_iso: str | None = None
    exit_reason: Literal["converged", "max_iterations", "council_split", ""] = ""  # v7 NEW

    def __post_init__(self) -> None:
        if not (1 <= self.iter_number <= MAX_REVISION_ITERATIONS):
            raise ValueError(
                f"IterationState.iter_number must be in [1, {MAX_REVISION_ITERATIONS}]; "
                f"got {self.iter_number}"
            )


# ---------------------------------------------------------------------------
# §3.2.3 SeatCharter (v1 unchanged)
# ---------------------------------------------------------------------------


@dataclass(slots=True, kw_only=True)
class SeatCharter:
    """§3.2.3 — a seat's charter: allowed families + primary model + timeout.

    allowed_families is a frozenset of provider-family names (from router.yaml
    taxonomy — e.g. {"anthropic", "google", "meta", "openai", "alibaba",
    "moonshot", "openai-oss"}). cascade_level is the current level index
    into the ProviderCascade (0-indexed).
    """

    seat_kind: str
    allowed_families: frozenset[str]
    primary_model: str
    cascade_level: int
    subprocess_timeout_ms: int

    def __post_init__(self) -> None:
        if self.seat_kind not in frozenset({"scribe", "editor", "judge", "red_team"}):
            raise ValueError(
                f"SeatCharter.seat_kind must be one of scribe/editor/judge/red_team; "
                f"got {self.seat_kind!r}"
            )
        if self.cascade_level < 0:
            raise ValueError(
                f"SeatCharter.cascade_level must be >= 0; got {self.cascade_level}"
            )
        if self.subprocess_timeout_ms <= 0:
            raise ValueError(
                f"SeatCharter.subprocess_timeout_ms must be > 0; "
                f"got {self.subprocess_timeout_ms}"
            )
        if not self.allowed_families:
            raise ValueError("SeatCharter.allowed_families must be non-empty")
        if not self.primary_model:
            raise ValueError("SeatCharter.primary_model must be non-empty")


# ---------------------------------------------------------------------------
# §3.2.4 ProviderCascade (v1 unchanged)
# ---------------------------------------------------------------------------


@dataclass(slots=True, kw_only=True)
class ProviderCascade:
    """§3.2.4 — ordered cascade levels per seat.

    Each level is a (family, model_id) pair. current_level indexes into
    levels; equal to len(levels) means 'exhausted' and is the trigger for
    F_PIPE_06 / F_PIPE_08.
    """

    seat_kind: str
    levels: tuple[tuple[str, str], ...]
    current_level: int

    def __post_init__(self) -> None:
        if self.seat_kind not in frozenset({"scribe", "editor", "judge", "red_team"}):
            raise ValueError(
                f"ProviderCascade.seat_kind must be one of scribe/editor/judge/red_team; "
                f"got {self.seat_kind!r}"
            )
        if not self.levels:
            raise ValueError("ProviderCascade.levels must be non-empty")
        if not (0 <= self.current_level <= len(self.levels)):
            raise ValueError(
                f"ProviderCascade.current_level out of range "
                f"[0, {len(self.levels)}]; got {self.current_level}"
            )
        for idx, level in enumerate(self.levels):
            if (
                not isinstance(level, tuple)
                or len(level) != 2
                or not all(isinstance(s, str) and s for s in level)
            ):
                raise ValueError(
                    f"ProviderCascade.levels[{idx}] must be a (family, model_id) "
                    f"tuple of non-empty strings; got {level!r}"
                )


# ---------------------------------------------------------------------------
# §3.2.5 RateLimiterState (v2 lease fields)
# ---------------------------------------------------------------------------


@dataclass(slots=True, kw_only=True)
class RateLimiterState:
    """§3.2.5 — rate-limiter snapshot with v2 lease fields.

    lease_holder_id and lease_expires_at_iso are both None when no lease is
    held; both non-None when a lease is active. The blueprint's lease TTL
    (30s) is enforced by Round 7's rate_limiter.py.
    """

    buckets: dict[str, TokenBucketProtocol] = field(default_factory=dict)
    last_refill_iso: str = ""
    lease_holder_id: str | None = None
    lease_expires_at_iso: str | None = None

    def __post_init__(self) -> None:
        # Lease half-present is a bug (partial construction). Round 7 asserts
        # both-present-or-both-absent; Round 1 re-asserts defensively.
        if (self.lease_holder_id is None) != (
            self.lease_expires_at_iso is None
        ):
            raise ValueError(
                "RateLimiterState lease fields must be both None or both non-None; "
                f"got holder={self.lease_holder_id!r} "
                f"expires={self.lease_expires_at_iso!r}"
            )


# ---------------------------------------------------------------------------
# §3.2.6 TabEnvelope (v2 Final tab_ordering + dataclass-level inline-literal check)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True, kw_only=True)
class TabEnvelope:
    """§3.2.6 — three-tab delivery envelope.

    ``tab_ordering`` is pinned to ``("live_radar", "deep_brief",
    "council_draft")``. The ``__post_init__`` check uses an inline tuple
    literal as RHS — a rebind of ``pipeline.loop.config.TAB_ORDERING`` cannot
    fool this check (V1 discipline). F_PIPE_16 is raised on violation.
    """

    run_id: str
    tab_ordering: tuple[str, str, str]
    live_radar_payload_hash: str
    deep_brief_payload_hash: str
    council_draft_payload_hash: str
    assembled_at_iso: str
    envelope_sha256: str

    def __post_init__(self) -> None:
        if self.tab_ordering != ("live_radar", "deep_brief", "council_draft"):
            raise F_PIPE_16(
                trigger="tab_envelope_ordering_violation",
                details={"observed": self.tab_ordering},
            )


# ---------------------------------------------------------------------------
# §5.6.1 GoldenSetItem
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True, kw_only=True)
class GoldenSetItem:
    """§5.6.1 — one item in the operator's signed golden set."""

    item_id: str
    rfa_hash: str
    project_context_hash: str
    expected_judge_min_score: float
    expected_topline_claims: tuple[str, ...]
    schema_version: int

    def __post_init__(self) -> None:
        if self.schema_version != 1:
            raise F_PIPE_22(
                trigger="calibration_report_schema_mismatch",
                details={
                    "shape": "GoldenSetItem",
                    "observed": self.schema_version,
                    "expected": 1,
                },
            )
        if not (0.0 <= self.expected_judge_min_score <= 100.0):
            raise ValueError(
                f"GoldenSetItem.expected_judge_min_score must be in [0, 100]; "
                f"got {self.expected_judge_min_score}"
            )


# ---------------------------------------------------------------------------
# §5.6.2 CalibrationReportItem
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True, kw_only=True)
class CalibrationReportItem:
    """§5.6.2 — one golden-set item's per-run calibration outcome."""

    item_id: str
    run_id: str
    actual_judge_score: float
    iterations_taken: int
    failure_code: str | None
    claim_overlap_ratio: float
    str_observation: float | None

    def __post_init__(self) -> None:
        if not (0 <= self.iterations_taken <= 3):
            raise ValueError(
                f"CalibrationReportItem.iterations_taken must be in "
                f"[0, {MAX_REVISION_ITERATIONS}]; got {self.iterations_taken}"
            )
        if not (0.0 <= self.claim_overlap_ratio <= 1.0):
            raise ValueError(
                f"CalibrationReportItem.claim_overlap_ratio must be in [0, 1]; "
                f"got {self.claim_overlap_ratio}"
            )


# ---------------------------------------------------------------------------
# §5.6.3 CalibrationReport
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True, kw_only=True)
class CalibrationReport:
    """§5.6.3 — signed aggregate report for one eval_mode run.

    ``signature`` is None before §4.15 step 9 (calibration.signing.sign); it
    is populated with the Ed25519 detached signature after. Verification
    (§4.15 step 10) requires ``signature is not None``.
    """

    schema_version: int
    run_id: str
    org_slug: str
    golden_set_manifest_hash: str
    items: tuple[CalibrationReportItem, ...]
    signed_at_iso: str
    signature: str | None = None

    def __post_init__(self) -> None:
        if self.schema_version != 1:
            raise F_PIPE_22(
                trigger="calibration_report_schema_mismatch",
                details={
                    "shape": "CalibrationReport",
                    "observed": self.schema_version,
                    "expected": 1,
                },
            )
        if not self.org_slug:
            raise ValueError("CalibrationReport.org_slug must be non-empty")
        if not self.run_id:
            raise ValueError("CalibrationReport.run_id must be non-empty")


# ---------------------------------------------------------------------------
# §3.2.1 RunState — v4 mode-discriminated-union invariants at construction
# ---------------------------------------------------------------------------


@dataclass(slots=True, kw_only=True)
class RunState:
    """§3.2.1 — top-level run state. Not frozen (checkpoint layer copy-on-write).

    ``__post_init__`` enforces three v4 invariants (blueprint §3.2.1 lines
    329-332) and the v5 schema-version invariant (§4.1 MA-07/MB-05):

    1. ``schema_version`` MUST equal ``RUNSTATE_SCHEMA_VERSION`` (inline
       literal ``== 2`` RHS). Legacy version 1 raises F_PIPE_22 as well.
    2. ``mode == "submission"`` ⟹ rfa_hash + project_context_hash non-None;
       golden_set_ref, calibration_*_ref all None.
    3. ``mode == "eval"`` ⟹ golden_set_ref non-None; rfa_hash,
       project_context_hash, three_tab_envelope_hash all None.
    4. ``phase`` MUST be a declared RunPhase (inline-literal frozenset).
    """

    schema_version: int
    run_id: str
    mode: str
    rfa_hash: str | None
    project_context_hash: str | None
    golden_set_ref: str | None
    org_slug: str
    session_id: str
    phase: str
    iterations: list[IterationState] = field(default_factory=list)
    active_cascade: ProviderCascade | None = None
    rate_limiter_snapshot: RateLimiterState | None = None
    run_iteration_families_so_far: dict[str, tuple[str, str]] = field(
        default_factory=dict
    )
    started_at_iso: str = ""
    last_checkpoint_iso: str = ""
    pre_gate_result_hash: str | None = None
    post_gate_result_hash: str | None = None
    signed_claim_evidence_map_hash: str | None = None
    three_tab_envelope_hash: str | None = None
    bypass_authorization_ref: str | None = None
    bypass_pending_checkpoint_ref: str | None = None
    quarantine_marker_ref: str | None = None
    calibration_report_ref: str | None = None
    calibration_signature_ref: str | None = None
    # v7 NEW (§5 v7 amendment §3.2.1) — optional, default None for v6 backward compat.
    red_team_verdict_ref: str | None = None
    council_split_decision: dict[str, Any] | None = None
    red_team_bypass_authorization_ref: str | None = None  # M13 escape valve

    def __post_init__(self) -> None:
        # (1) schema-version enforcement. Inline-literal RHS — rebind-resistant.
        # v5 §4.1 step 1: schema check precedes phase check.
        if self.schema_version != 2:
            raise F_PIPE_22(
                trigger="runstate_schema_downgrade",
                details={
                    "observed": self.schema_version,
                    "expected": 2,
                },
            )
        # Defence-in-depth: the top-level constant has not been rebound.
        if RUNSTATE_SCHEMA_VERSION != 2:
            raise F_PIPE_22(
                trigger="runstate_schema_downgrade",
                details={
                    "observed": RUNSTATE_SCHEMA_VERSION,
                    "reason": "pipeline.loop.config.RUNSTATE_SCHEMA_VERSION rebound",
                },
            )

        # (2) mode validity
        if self.mode not in frozenset({"submission", "eval"}):
            raise ValueError(
                f"RunState.mode must be 'submission' or 'eval'; got {self.mode!r}"
            )

        # (3) phase validity — inline-literal RHS
        if self.phase not in frozenset(
            {
                "initialized",
                "pre_gate_pending",
                "pre_gate_passed",
                "inner_loop_iter_1",
                "inner_loop_iter_2",
                "inner_loop_iter_3",
                "post_gate_pending",
                "post_gate_passed",
                "signoff_pending",
                "signoff_pending_council_split",  # v7 NEW
                "report_signed",
                "tabs_delivered",
                "finalized",
                "degraded_paused",
                "aborted_trusted_fail",
                "aborted_operator",
                "quarantined",
                "eval_iter_pending",
                "calibration_assembled",
                "calibration_signed",
                "eval_finalized",
            }
        ):
            raise ValueError(
                f"RunState.phase must be a declared RunPhase; got {self.phase!r}"
            )

        # (4) mode-discriminated union — blueprint §3.2.1 lines 329-332
        if self.mode == "submission":
            if self.rfa_hash is None:
                raise F_PIPE_21(
                    trigger="submission_mode_missing_rfa_hash",
                    details={"run_id": self.run_id},
                )
            if self.project_context_hash is None:
                raise F_PIPE_21(
                    trigger="submission_mode_missing_project_context_hash",
                    details={"run_id": self.run_id},
                )
            if self.golden_set_ref is not None:
                raise F_PIPE_21(
                    trigger="submission_mode_calibration_intent",
                    details={"run_id": self.run_id, "field": "golden_set_ref"},
                )
            if self.calibration_report_ref is not None:
                raise F_PIPE_21(
                    trigger="submission_mode_has_calibration_ref",
                    details={
                        "run_id": self.run_id,
                        "field": "calibration_report_ref",
                    },
                )
            if self.calibration_signature_ref is not None:
                raise F_PIPE_21(
                    trigger="submission_mode_has_calibration_ref",
                    details={
                        "run_id": self.run_id,
                        "field": "calibration_signature_ref",
                    },
                )
        elif self.mode == "eval":
            if self.golden_set_ref is None:
                raise F_PIPE_21(
                    trigger="eval_mode_missing_golden_set_ref",
                    details={"run_id": self.run_id},
                )
            if self.rfa_hash is not None:
                raise F_PIPE_21(
                    trigger="eval_mode_has_rfa_hash",
                    details={"run_id": self.run_id},
                )
            if self.project_context_hash is not None:
                raise F_PIPE_21(
                    trigger="eval_mode_has_project_context_hash",
                    details={"run_id": self.run_id},
                )
            if self.three_tab_envelope_hash is not None:
                raise F_PIPE_21(
                    trigger="eval_mode_has_tab_envelope_hash",
                    details={"run_id": self.run_id},
                )

        # org_slug + run_id non-empty
        if not self.org_slug:
            raise ValueError("RunState.org_slug must be non-empty")
        if not self.run_id:
            raise ValueError("RunState.run_id must be non-empty")


# Reference CALIBRATION_REPORT_SCHEMA_VERSION to keep it importable and verify
# the round's assumption that the constant value is 1. A module-load check
# here mirrors the config-module assertion so a rebind of the config constant
# is caught before any dataclass is constructed.
assert CALIBRATION_REPORT_SCHEMA_VERSION == 1, (
    "pipeline.loop.config.CALIBRATION_REPORT_SCHEMA_VERSION has been rebound "
    "before pipeline.loop.types import; refusing to load"
)


__all__ = [
    "BLUEPRINT_DEPS",
    "RunMode",
    "RunPhase",
    "SeatKind",
    "IntentKind",
    "TokenBucketProtocol",
    "IterationState",
    "SeatCharter",
    "ProviderCascade",
    "RateLimiterState",
    "TabEnvelope",
    "GoldenSetItem",
    "CalibrationReportItem",
    "CalibrationReport",
    "RunState",
]
