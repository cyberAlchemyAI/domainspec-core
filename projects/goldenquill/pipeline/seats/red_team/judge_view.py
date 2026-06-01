"""pipeline.seats.red_team.judge_view — Red Team's view of Judge's output.

Red Team consumes a *truncated* view of Judge's verdict per §10.3 + §10.8:
``total_score``, ``max_score``, ``recommendation``, and ``overall_notes``
(truncated to 400 chars per orchestrator-CLI anti-anchoring discipline).

Red Team does NOT see Judge's per-criterion breakdown (would maximize
anchoring). The :class:`JudgeContextView` is the structural narrowing that
the input bundle's ``judge_verdict`` field carries.

This module ships the view + the adapter that builds it from Judge's
concrete :class:`pipeline.seats.judge.types.JudgeVerdict`. The adapter
is the canonical R2 binding — :func:`view_from_judge_verdict` reads
Judge's nested ``judge_output.total_score`` + ``judge_output.max_total``
+ ``judge_output.rubric_sha256`` and produces a flat view shape Red Team
consumes structurally.

E-026 lineage discipline: tests in :mod:`tests.seats.red_team.test_e026_judge_view_bind`
assert ``pipeline.seats.judge.types.JudgeVerdict.__module__`` resolves
exactly to ``pipeline.seats.judge.types`` — guards against import-path
drift between Judge R3 + Red Team R2 LOCK rounds.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Protocol, runtime_checkable


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

OVERALL_NOTES_TRUNCATION_CHARS: Final[int] = 400
"""Anti-anchoring discipline: Red Team sees Judge's overall_notes truncated
to 400 chars (orchestrator-CLI line 144 source-grounding). Per §10.8."""


assert OVERALL_NOTES_TRUNCATION_CHARS == 400, (
    "OVERALL_NOTES_TRUNCATION_CHARS rebound at module load; "
    "refusing to load pipeline.seats.red_team.judge_view"
)


# ---------------------------------------------------------------------------
# View shape — what Red Team's input bundle carries
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class JudgeContextView:
    """Anti-anchoring narrow view of Judge's verdict (§10.3 + §10.8).

    Carries headline numbers + recommendation + truncated notes. Does NOT
    carry per-criterion breakdown — Red Team forms its own per-criterion
    view fresh.

    Construction-time invariants:

    - ``run_id`` is non-empty (run-scoped binding to RedTeamInput).
    - ``rubric_hash`` is non-empty hex string (matched against
      ``RedTeamInput.rubric.content_hash`` at PRE-gate time).
    - ``total_score`` and ``max_score`` are non-negative ints with
      ``total_score <= max_score``.
    - ``recommendation`` is a free-form string (R1 typed Literal; here
      kept str to accommodate Judge's recommendation vocabulary which may
      differ from Red Team's closed set).
    - ``overall_notes`` is at most :data:`OVERALL_NOTES_TRUNCATION_CHARS`
      chars (400). The adapter truncates with no ellipsis — Red Team only
      ever sees a prefix of Judge's full notes, never the full body.
    """

    run_id: str
    rubric_hash: str
    total_score: int
    max_score: int
    recommendation: str
    overall_notes: str

    def __post_init__(self) -> None:
        if not isinstance(self.run_id, str) or not self.run_id.strip():
            raise ValueError("run_id must be non-empty str")
        if not isinstance(self.rubric_hash, str) or not self.rubric_hash.strip():
            raise ValueError("rubric_hash must be non-empty str")
        if not isinstance(self.total_score, int) or self.total_score < 0:
            raise ValueError(
                f"total_score must be non-negative int; got {self.total_score!r}"
            )
        if not isinstance(self.max_score, int) or self.max_score <= 0:
            raise ValueError(
                f"max_score must be positive int; got {self.max_score!r}"
            )
        if self.total_score > self.max_score:
            raise ValueError(
                f"total_score {self.total_score} > max_score {self.max_score}"
            )
        if not isinstance(self.recommendation, str):
            raise TypeError("recommendation must be str")
        if not isinstance(self.overall_notes, str):
            raise TypeError("overall_notes must be str")
        if len(self.overall_notes) > OVERALL_NOTES_TRUNCATION_CHARS:
            raise ValueError(
                f"overall_notes exceeds {OVERALL_NOTES_TRUNCATION_CHARS} chars "
                f"({len(self.overall_notes)}) — adapter must truncate before construction"
            )


# ---------------------------------------------------------------------------
# Adapter: Judge's concrete shape → Red Team's view
# ---------------------------------------------------------------------------


@runtime_checkable
class _JudgeOutputLike(Protocol):
    """Forward-Protocol for Judge's :class:`JudgeOutput` shape."""

    total_score: int
    max_total: int
    rubric_sha256: str


@runtime_checkable
class _ResponsivenessMapLike(Protocol):
    """Forward-Protocol for Judge's :class:`ResponsivenessMap` shape."""

    entries: tuple


@runtime_checkable
class _JudgeVerdictLike(Protocol):
    """Forward-Protocol for Judge's :class:`JudgeVerdict` shape.

    The adapter binds via this Protocol; production callers pass the
    concrete ``pipeline.seats.judge.types.JudgeVerdict`` instance. The
    E-026 lineage test asserts the import path hasn't drifted.
    """

    judge_output: _JudgeOutputLike
    rubric_program_code: str
    responsiveness_map: _ResponsivenessMapLike


def view_from_judge_verdict(
    judge_verdict: _JudgeVerdictLike,
    *,
    run_id: str,
    recommendation: str,
    overall_notes: str,
) -> JudgeContextView:
    """Adapter: Judge's :class:`JudgeVerdict` → Red Team's :class:`JudgeContextView`.

    Args:
        judge_verdict: concrete Judge verdict (or any structural match per
            the runtime-checkable Protocol).
        run_id: the run-scoped UUID — Judge's verdict shape doesn't carry
            this directly (it's pinned in the assembling caller's run-state),
            so the caller threads it through.
        recommendation: Judge's recommendation string. Judge's verdict
            doesn't yet carry a Literal recommendation field at R3 LOCK time;
            the caller derives it from JudgeOutput.total_score / max_total
            ratio against the rubric's recommendation thresholds.
        overall_notes: Judge's full notes; truncated by this adapter to
            :data:`OVERALL_NOTES_TRUNCATION_CHARS` (400 chars).

    Returns:
        :class:`JudgeContextView` — the structurally-narrowed view Red
        Team consumes.

    Raises:
        ValueError: any field-shape invariant violation.
    """
    truncated_notes = overall_notes[:OVERALL_NOTES_TRUNCATION_CHARS]
    return JudgeContextView(
        run_id=run_id,
        rubric_hash=judge_verdict.judge_output.rubric_sha256,
        total_score=judge_verdict.judge_output.total_score,
        max_score=judge_verdict.judge_output.max_total,
        recommendation=recommendation,
        overall_notes=truncated_notes,
    )


__all__ = [
    "OVERALL_NOTES_TRUNCATION_CHARS",
    "JudgeContextView",
    "view_from_judge_verdict",
]
