"""pipeline.loop — §5 Pipeline Orchestrator foundations (Round 1).

Blueprint §5 v6 LOCKED 2026-04-19 (pipeline/blueprint/v0.1/section_05_pipeline.md)
           §5 v6 amendment LOCK-READY (pipeline/blueprint/v0.1/section_05_v6_amendment.md)

Round 1 ships shape-only foundations consumed by Rounds 2-12:
- config: §8 v6 constants + module-load integrity asserts + vault-relative path templates
- errors: 22 F-PIPE-* exception classes + sub-trigger taxonomies + F-EVAL-CROSS-ORG-READ sentinel
- types:  9 dataclasses (RunState, IterationState, SeatCharter, ProviderCascade,
          RateLimiterState, TabEnvelope, GoldenSetItem, CalibrationReportItem, CalibrationReport)
          plus 4 type aliases (RunMode, RunPhase, SeatKind, IntentKind)

Canonical home: `pipeline/loop/` (NOT `tilth/pipeline/`) — enforced by
`pipeline/linting/ast_lint.py` R2 LOOP_LOGICIAN_BAN target_glob.

Spec card: `pipeline/engineering/spec_cards/section_05_round_1_foundations.md`
"""

from __future__ import annotations

from pipeline.loop.config import (
    BLUEPRINT_DEPS,
    TAB_ORDERING,
    RUNSTATE_SCHEMA_VERSION,
    RUNSTATE_SCHEMA_VERSION_LEGACY_REJECTED,
    CALIBRATION_REPORT_SCHEMA_VERSION,
    CALIBRATION_SIGNING_ALGORITHM,
    MAX_CALIBRATION_AGE_DAYS,
    EVAL_MODE_ALLOWED_INTENTS,
    SUBMISSION_MODE_FORBIDDEN_INTENTS,
    CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS,
    CHECKPOINT_TOTAL_TIMEOUT_SEC,
    CRON_VAULT_RETRY_WINDOW_SEC,
    CRON_VAULT_RETRY_ATTEMPTS,
    RATE_LIMIT_JITTER_RANGE_MS,
    RATE_LIMIT_LEASE_TTL_SEC,
    CRON_STAMP_TTL_HOURS,
    SCRIBE_SUBPROCESS_TIMEOUT_MS,
    EDITOR_SUBPROCESS_TIMEOUT_MS,
    JUDGE_SUBPROCESS_TIMEOUT_MS,
    OPERATOR_INTERRUPT_POLL_INTERVAL_MS,
    MAX_REVISION_ITERATIONS,
    CALIBRATION_REPORT_PATH_TMPL,
    CALIBRATION_SIGNATURE_PATH_TMPL,
    BYPASS_PENDING_CHECKPOINT_PATH_TMPL,
    F_PIPE_21_TRIGGERS,
    F_PIPE_22_TRIGGERS,
)
from pipeline.loop.errors import (
    F_EVAL_CROSS_ORG_READ_CODE,
    F_PIPE_01,
    F_PIPE_02,
    F_PIPE_03,
    F_PIPE_04,
    F_PIPE_05,
    F_PIPE_06,
    F_PIPE_07,
    F_PIPE_08,
    F_PIPE_09,
    F_PIPE_10,
    F_PIPE_11,
    F_PIPE_12,
    F_PIPE_13,
    F_PIPE_14,
    F_PIPE_15,
    F_PIPE_16,
    F_PIPE_17,
    F_PIPE_18,
    F_PIPE_19,
    F_PIPE_20,
    F_PIPE_21,
    F_PIPE_22,
    F_PIPE_BY_CODE,
    PipelineFailure,
)
from pipeline.loop.run_lifecycle import (
    RunIdFactory,
    VaultReadCallable,
    resume_run,
    start_run,
)
from pipeline.loop.seat_runner import (
    MINIMAL_ENV_ALLOWED_KEYS,
    JudgeParseCallable,
    SeatInvocationContext,
    SeatInvocationResult,
    SubprocessLauncher,
    SubprocessResult,
    default_judge_parse,
    invoke_editor,
    invoke_judge,
    invoke_scribe,
    invoke_seat,
)
from pipeline.loop.revision_loop import (
    InnerLoopResult,
    InterruptProbe,
    SeatContextFactory,
    run_inner_loop,
)
from pipeline.loop.post_gate_runner import (
    GateRunnerProtocol,
    PostGateInputFactory,
    PostGateOrchestrationResult,
    PostGateRejected,
    run_post_gate_orchestration,
)
from pipeline.loop.rate_limiter import (
    InsufficientTokens,
    RandIntFn,
    Reserved,
    TokenBucket,
    can_reserve,
    release,
    reserve,
)
from pipeline.loop.cascade import (
    CascadeLevel,
    CascadeSelection,
    select_cascade_level,
)
from pipeline.loop.tab_delivery import (
    HashFileCallable,
    TabSigningResult,
    deliver_tab,
)
from pipeline.loop.cron_scheduler import (
    CronFireResult,
    FlockAcquire,
    OnFireCallable,
    VaultTransientError,
    build_cron_task_id,
    fire_once,
)
from pipeline.loop.run_pipeline import (
    PipelineRunResult,
    PreGateInputFactory,
    RunPipelineContext,
    run_pipeline,
)
from pipeline.loop.track_registry import (
    TILTH_VERSION_FAMILY,
    RegistrySchemaError,
    Track,
    TrackNotFound,
    TrackNotShippable,
    TrackRegistry,
    TrackRegistryError,
    TrackShapeUnimplemented,
    dispatch_track,
    get_track,
    load_track_registry,
)
# NOTE: `pipeline.loop.run_eval_pipeline` is NOT re-exported here because
# its import chain (→ pipeline.calibration.*) circles back through
# pipeline.loop.errors which callers import as `from pipeline.loop.errors
# import F_PIPE_21`. Callers needing the eval capstone import it directly:
# ``from pipeline.loop.run_eval_pipeline import run_eval_pipeline``.
from pipeline.loop.state_checkpoint import (
    CheckpointResult,
    ClockProtocol,
    SleepCallable,
    VaultWriteCallable,
    _assert_runstate_schema_current,
    checkpoint_atomic,
)
from pipeline.loop.types import (
    CalibrationReport,
    CalibrationReportItem,
    GoldenSetItem,
    IntentKind,
    IterationState,
    ProviderCascade,
    RateLimiterState,
    RunMode,
    RunPhase,
    RunState,
    SeatCharter,
    SeatKind,
    TabEnvelope,
    TokenBucketProtocol,
)

__all__ = [
    # config
    "BLUEPRINT_DEPS",
    "TAB_ORDERING",
    "RUNSTATE_SCHEMA_VERSION",
    "RUNSTATE_SCHEMA_VERSION_LEGACY_REJECTED",
    "CALIBRATION_REPORT_SCHEMA_VERSION",
    "CALIBRATION_SIGNING_ALGORITHM",
    "MAX_CALIBRATION_AGE_DAYS",
    "EVAL_MODE_ALLOWED_INTENTS",
    "SUBMISSION_MODE_FORBIDDEN_INTENTS",
    "CHECKPOINT_CAS_BACKOFF_SCHEDULE_MS",
    "CHECKPOINT_TOTAL_TIMEOUT_SEC",
    "CRON_VAULT_RETRY_WINDOW_SEC",
    "CRON_VAULT_RETRY_ATTEMPTS",
    "RATE_LIMIT_JITTER_RANGE_MS",
    "RATE_LIMIT_LEASE_TTL_SEC",
    "CRON_STAMP_TTL_HOURS",
    "SCRIBE_SUBPROCESS_TIMEOUT_MS",
    "EDITOR_SUBPROCESS_TIMEOUT_MS",
    "JUDGE_SUBPROCESS_TIMEOUT_MS",
    "OPERATOR_INTERRUPT_POLL_INTERVAL_MS",
    "MAX_REVISION_ITERATIONS",
    "CALIBRATION_REPORT_PATH_TMPL",
    "CALIBRATION_SIGNATURE_PATH_TMPL",
    "BYPASS_PENDING_CHECKPOINT_PATH_TMPL",
    "F_PIPE_21_TRIGGERS",
    "F_PIPE_22_TRIGGERS",
    # errors
    "PipelineFailure",
    "F_PIPE_01",
    "F_PIPE_02",
    "F_PIPE_03",
    "F_PIPE_04",
    "F_PIPE_05",
    "F_PIPE_06",
    "F_PIPE_07",
    "F_PIPE_08",
    "F_PIPE_09",
    "F_PIPE_10",
    "F_PIPE_11",
    "F_PIPE_12",
    "F_PIPE_13",
    "F_PIPE_14",
    "F_PIPE_15",
    "F_PIPE_16",
    "F_PIPE_17",
    "F_PIPE_18",
    "F_PIPE_19",
    "F_PIPE_20",
    "F_PIPE_21",
    "F_PIPE_22",
    "F_EVAL_CROSS_ORG_READ_CODE",
    "F_PIPE_BY_CODE",
    # state_checkpoint (Round 2)
    "CheckpointResult",
    "ClockProtocol",
    "SleepCallable",
    "VaultWriteCallable",
    "checkpoint_atomic",
    "_assert_runstate_schema_current",
    # run_lifecycle (Round 3)
    "RunIdFactory",
    "VaultReadCallable",
    "resume_run",
    "start_run",
    # seat_runner (Round 4)
    "MINIMAL_ENV_ALLOWED_KEYS",
    "JudgeParseCallable",
    "SeatInvocationContext",
    "SeatInvocationResult",
    "SubprocessLauncher",
    "SubprocessResult",
    "default_judge_parse",
    "invoke_editor",
    "invoke_judge",
    "invoke_scribe",
    "invoke_seat",
    # revision_loop (Round 5)
    "InnerLoopResult",
    "InterruptProbe",
    "SeatContextFactory",
    "run_inner_loop",
    # post_gate_runner (Round 6)
    "GateRunnerProtocol",
    "PostGateInputFactory",
    "PostGateOrchestrationResult",
    "PostGateRejected",
    "run_post_gate_orchestration",
    # rate_limiter (Round 7)
    "InsufficientTokens",
    "RandIntFn",
    "Reserved",
    "TokenBucket",
    "can_reserve",
    "release",
    "reserve",
    # cascade (Round 8)
    "CascadeLevel",
    "CascadeSelection",
    "select_cascade_level",
    # tab_delivery (Round 9)
    "HashFileCallable",
    "TabSigningResult",
    "deliver_tab",
    # cron_scheduler (Round 10)
    "CronFireResult",
    "FlockAcquire",
    "OnFireCallable",
    "VaultTransientError",
    "build_cron_task_id",
    "fire_once",
    # run_pipeline (Round 11 — submission-mode capstone)
    "PipelineRunResult",
    "RunPipelineContext",
    "run_pipeline",
    # run_eval_pipeline (R12.B) is NOT re-exported — see module comment above.
    # track_registry (§5 v8 amendment per R.PF1)
    "TILTH_VERSION_FAMILY",
    "RegistrySchemaError",
    "Track",
    "TrackNotFound",
    "TrackNotShippable",
    "TrackRegistry",
    "TrackRegistryError",
    "TrackShapeUnimplemented",
    "dispatch_track",
    "get_track",
    "load_track_registry",
    # types
    "RunState",
    "IterationState",
    "SeatCharter",
    "ProviderCascade",
    "RateLimiterState",
    "TokenBucketProtocol",
    "TabEnvelope",
    "GoldenSetItem",
    "CalibrationReportItem",
    "CalibrationReport",
    "RunMode",
    "RunPhase",
    "SeatKind",
    "IntentKind",
]
