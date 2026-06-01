"""pipeline.loop.errors — 22 F-PIPE-* exception classes + forward-dep sentinel.

Blueprint §5 v6 §6 LOCKED 2026-04-19 — 22 F-PIPE-* failure codes (F-PIPE-01
through F-PIPE-22). Each code ships a subclass of :class:`PipelineFailure`
that pins ``CODE``, ``SEVERITY``, and ``SAVE_STATE_CONTRACT`` as
``Final[str]`` class attributes so that downstream rounds (state_checkpoint,
run_lifecycle, seat_runner, revision_loop, three_tab_delivery, eval_mode)
can uniformly dispatch on ``type(exc)`` without string parsing.

F-EVAL-CROSS-ORG-READ is owned by §4 v2.1 (PRE-gate predicate). §5 cites the
code string via :data:`F_EVAL_CROSS_ORG_READ_CODE` for branching; §5 never
raises its class.

Spec card: `pipeline/engineering/spec_cards/section_05_round_1_foundations.md`
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, Final

from pipeline.loop.config import F_PIPE_21_TRIGGERS, F_PIPE_22_TRIGGERS

BLUEPRINT_DEPS: Final[dict[str, dict[str, object]]] = {
    "section_05_pipeline.md": {
        "version": "v6",
        "hash_sha3_512_prefix16": "feb5928491e4dc40",
        "sections_implemented": [
            "§6 failure-code table (22 codes + F-EVAL-CROSS-ORG-READ forward-dep)",
            "§7.13-§7.16 invariant naming (referenced by F_PIPE_16, F_PIPE_21)",
        ],
    },
}

# Forward-dep sentinel: §4 v2.1 PRE-gate returns this code string. §5 does not
# raise F_EVAL_CROSS_ORG_READ; it dispatches on the returned code.
F_EVAL_CROSS_ORG_READ_CODE: Final[str] = "F-EVAL-CROSS-ORG-READ"
assert F_EVAL_CROSS_ORG_READ_CODE == "F-EVAL-CROSS-ORG-READ", (
    "F_EVAL_CROSS_ORG_READ_CODE has been rebound at module load; "
    "refusing to load pipeline.loop.errors"
)


class PipelineFailure(Exception):
    """Base class for every §5 F-PIPE-* raise.

    Subclasses pin three ``Final[str]`` class attributes (``CODE``,
    ``SEVERITY``, ``SAVE_STATE_CONTRACT``) and accept a free-form
    ``trigger`` + structured ``details`` dict. Instances are never mutated
    after construction (no ``__setattr__`` override; the convention is
    enforced by callers, not the class).

    Consumers pattern-match via ``isinstance(exc, F_PIPE_XX)`` OR via
    ``F_PIPE_BY_CODE[code_str]`` lookup. The class attribute contract makes
    these two paths interchangeable.
    """

    CODE: Final[str] = ""
    SEVERITY: Final[str] = ""
    SAVE_STATE_CONTRACT: Final[str] = ""

    def __init__(
        self,
        code_or_trigger: str = "",
        *,
        trigger: str | None = None,
        details: Mapping[str, Any] | None = None,
    ) -> None:
        # Allow both legacy `PipelineFailure("F-PIPE-01", trigger=...)` calls
        # (blueprint-prose style; used by some §5 callers in the blueprint
        # pseudo-code) and direct-subclass calls where the CODE is implicit.
        # For the base class, the first positional is the code; for
        # subclasses, it's treated as a trigger shortcut if `trigger` is not
        # supplied separately.
        if type(self) is PipelineFailure:
            inferred_code = code_or_trigger
            inferred_trigger = trigger or ""
        else:
            inferred_code = type(self).CODE
            inferred_trigger = trigger if trigger is not None else code_or_trigger
        self.code: str = inferred_code
        self.trigger: str = inferred_trigger
        self.details: dict[str, Any] = dict(details or {})
        super().__init__(
            f"{self.code}: {self.trigger}"
            + (f" {self.details!r}" if self.details else "")
        )


# ---------------------------------------------------------------------------
# Concrete F-PIPE-* classes (22 total, one per §6 v6 row)
# ---------------------------------------------------------------------------


class F_PIPE_01(PipelineFailure):
    """run_state_corrupt — CAS exhausted / schema mismatch / quarantine path."""

    CODE: Final[str] = "F-PIPE-01"
    SEVERITY: Final[str] = "CRIT"
    SAVE_STATE_CONTRACT: Final[str] = "state-failure + quarantine marker"


class F_PIPE_02(PipelineFailure):
    """pre_gate_timeout — PRE gate exceeded timeout."""

    CODE: Final[str] = "F-PIPE-02"
    SEVERITY: Final[str] = "HIGH"
    SAVE_STATE_CONTRACT: Final[str] = "state-failure"


class F_PIPE_03(PipelineFailure):
    """post_gate_timeout — POST gate exceeded timeout."""

    CODE: Final[str] = "F-PIPE-03"
    SEVERITY: Final[str] = "HIGH"
    SAVE_STATE_CONTRACT: Final[str] = "state-failure"


class F_PIPE_04(PipelineFailure):
    """judge_convergence_false_positive — delta-plateau below min-score threshold."""

    CODE: Final[str] = "F-PIPE-04"
    SEVERITY: Final[str] = "MED"
    SAVE_STATE_CONTRACT: Final[str] = "state-failure"


class F_PIPE_05(PipelineFailure):
    """iteration_cap_exceeded — three iterations, no PASS, no plateau."""

    CODE: Final[str] = "F-PIPE-05"
    SEVERITY: Final[str] = "MED"
    SAVE_STATE_CONTRACT: Final[str] = "state-failure"


class F_PIPE_06(PipelineFailure):
    """rate_limit_exhausted — cascade exhausts + retries."""

    CODE: Final[str] = "F-PIPE-06"
    SEVERITY: Final[str] = "HIGH"
    SAVE_STATE_CONTRACT: Final[str] = "state-failure"


class F_PIPE_07(PipelineFailure):
    """seat_subprocess_timeout — seat subprocess timeout."""

    CODE: Final[str] = "F-PIPE-07"
    SEVERITY: Final[str] = "HIGH"
    SAVE_STATE_CONTRACT: Final[str] = "state-failure"


class F_PIPE_08(PipelineFailure):
    """cross_family_violation — cascade can't find cross-family-compatible level."""

    CODE: Final[str] = "F-PIPE-08"
    SEVERITY: Final[str] = "CRIT"
    SAVE_STATE_CONTRACT: Final[str] = "state-failure + admin-risk CRIT"


class F_PIPE_09(PipelineFailure):
    """judge_output_malformed — Judge JSON unparsable after retry."""

    CODE: Final[str] = "F-PIPE-09"
    SEVERITY: Final[str] = "HIGH"
    SAVE_STATE_CONTRACT: Final[str] = "state-failure (never success)"


class F_PIPE_10(PipelineFailure):
    """signoff_cancelled — operator declined."""

    CODE: Final[str] = "F-PIPE-10"
    SEVERITY: Final[str] = "LOW"
    SAVE_STATE_CONTRACT: Final[str] = "state-failure"


class F_PIPE_11(PipelineFailure):
    """operator_interrupt — Ctrl-C or interrupt flag."""

    CODE: Final[str] = "F-PIPE-11"
    SEVERITY: Final[str] = "LOW"
    SAVE_STATE_CONTRACT: Final[str] = "state-failure (post-checkpoint)"


class F_PIPE_12(PipelineFailure):
    """hardware_degraded_mode_failed — Ollama fallback failed."""

    CODE: Final[str] = "F-PIPE-12"
    SEVERITY: Final[str] = "HIGH"
    SAVE_STATE_CONTRACT: Final[str] = "state-failure"


class F_PIPE_13(PipelineFailure):
    """review_seat_outage_pending_bypass — review cascade exhausted, escape-valve awaiting."""

    CODE: Final[str] = "F-PIPE-13"
    SEVERITY: Final[str] = "CRIT"
    SAVE_STATE_CONTRACT: Final[str] = "state-failure + bypass-pending"


class F_PIPE_14(PipelineFailure):
    """review_seat_bypass_expired — bypass not signed in 24h."""

    CODE: Final[str] = "F-PIPE-14"
    SEVERITY: Final[str] = "HIGH"
    SAVE_STATE_CONTRACT: Final[str] = "state-failure"


class F_PIPE_15(PipelineFailure):
    """cron_dedupe_failure — vault retry window exhausted."""

    CODE: Final[str] = "F-PIPE-15"
    SEVERITY: Final[str] = "HIGH"
    SAVE_STATE_CONTRACT: Final[str] = "state-failure"


class F_PIPE_16(PipelineFailure):
    """tab_envelope_ordering_violation — inline-literal runtime check."""

    CODE: Final[str] = "F-PIPE-16"
    SEVERITY: Final[str] = "CRIT"
    SAVE_STATE_CONTRACT: Final[str] = "state-failure + admin-risk CRIT"


class F_PIPE_17(PipelineFailure):
    """bypass_authorization_ledger_write_failed — admin-risk append failed."""

    CODE: Final[str] = "F-PIPE-17"
    SEVERITY: Final[str] = "CRIT"
    SAVE_STATE_CONTRACT: Final[str] = "state-failure"


class F_PIPE_18(PipelineFailure):
    """resume_phase_mismatch — resume stored phase not in allowed set."""

    CODE: Final[str] = "F-PIPE-18"
    SEVERITY: Final[str] = "CRIT"
    SAVE_STATE_CONTRACT: Final[str] = "state-failure + quarantine"


class F_PIPE_19(PipelineFailure):
    """soft_restart_forbidden — transition to inner_loop_iter_M when iter_n >= M."""

    CODE: Final[str] = "F-PIPE-19"
    SEVERITY: Final[str] = "CRIT"
    SAVE_STATE_CONTRACT: Final[str] = "state-failure + admin-risk CRIT"


class F_PIPE_20(PipelineFailure):
    """cedar_decision_missing — PreGateResult.cedar_decision_ref is None on PASS."""

    CODE: Final[str] = "F-PIPE-20"
    SEVERITY: Final[str] = "CRIT"
    SAVE_STATE_CONTRACT: Final[str] = "state-failure"


class F_PIPE_21(PipelineFailure):
    """calibration_report_in_submission_bundle — mode-isolation shield.

    Trigger strings are validated against :data:`F_PIPE_21_TRIGGERS` (15
    exhaustive values per blueprint §6 v6 line 1052). A free-form trigger
    string is rejected at construction time — every raise-site must cite a
    taxonomy row.
    """

    CODE: Final[str] = "F-PIPE-21"
    SEVERITY: Final[str] = "CRIT"
    SAVE_STATE_CONTRACT: Final[str] = "state-failure + admin-risk CRIT"

    def __init__(
        self,
        code_or_trigger: str = "",
        *,
        trigger: str | None = None,
        details: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(code_or_trigger, trigger=trigger, details=details)
        if self.trigger not in F_PIPE_21_TRIGGERS:
            raise ValueError(
                f"F_PIPE_21 trigger {self.trigger!r} is not in F_PIPE_21_TRIGGERS; "
                "every raise-site must cite an enumerated §6 v6 sub-trigger"
            )


class F_PIPE_22(PipelineFailure):
    """runstate_schema_downgrade — schema-version check precedes phase check.

    Trigger strings validated against :data:`F_PIPE_22_TRIGGERS` (2 exhaustive
    values per blueprint §6 v6 line 1053).
    """

    CODE: Final[str] = "F-PIPE-22"
    SEVERITY: Final[str] = "CRIT"
    SAVE_STATE_CONTRACT: Final[str] = "state-failure + quarantine"

    def __init__(
        self,
        code_or_trigger: str = "",
        *,
        trigger: str | None = None,
        details: Mapping[str, Any] | None = None,
    ) -> None:
        super().__init__(code_or_trigger, trigger=trigger, details=details)
        if self.trigger not in F_PIPE_22_TRIGGERS:
            raise ValueError(
                f"F_PIPE_22 trigger {self.trigger!r} is not in F_PIPE_22_TRIGGERS; "
                "every raise-site must cite an enumerated §6 v6 sub-trigger"
            )


# ---------------------------------------------------------------------------
# Code -> class dispatch table
# ---------------------------------------------------------------------------

F_PIPE_BY_CODE: Final[Mapping[str, type[PipelineFailure]]] = {
    "F-PIPE-01": F_PIPE_01,
    "F-PIPE-02": F_PIPE_02,
    "F-PIPE-03": F_PIPE_03,
    "F-PIPE-04": F_PIPE_04,
    "F-PIPE-05": F_PIPE_05,
    "F-PIPE-06": F_PIPE_06,
    "F-PIPE-07": F_PIPE_07,
    "F-PIPE-08": F_PIPE_08,
    "F-PIPE-09": F_PIPE_09,
    "F-PIPE-10": F_PIPE_10,
    "F-PIPE-11": F_PIPE_11,
    "F-PIPE-12": F_PIPE_12,
    "F-PIPE-13": F_PIPE_13,
    "F-PIPE-14": F_PIPE_14,
    "F-PIPE-15": F_PIPE_15,
    "F-PIPE-16": F_PIPE_16,
    "F-PIPE-17": F_PIPE_17,
    "F-PIPE-18": F_PIPE_18,
    "F-PIPE-19": F_PIPE_19,
    "F-PIPE-20": F_PIPE_20,
    "F-PIPE-21": F_PIPE_21,
    "F-PIPE-22": F_PIPE_22,
}
assert len(F_PIPE_BY_CODE) == 22, (
    "F_PIPE_BY_CODE has been rebound at module load; "
    "refusing to load pipeline.loop.errors"
)

__all__ = [
    "BLUEPRINT_DEPS",
    "F_EVAL_CROSS_ORG_READ_CODE",
    "F_PIPE_BY_CODE",
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
]
