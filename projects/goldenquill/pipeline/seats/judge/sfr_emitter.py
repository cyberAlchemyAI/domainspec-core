"""pipeline.seats.judge.sfr_emitter — §9 R3 SFR (Score-to-Funder Ratio) emission.

Architecture v7 §F.1 mandates SFR emission for every council seat that
ships a verdict. **Judge is NOT exempt** — the spec card §4 lists "SFR
emission" as a Round-3 deliverable. This module composes a frozen
:class:`SfrReport` from a :class:`pipeline.seats.judge.types.JudgeVerdict`
plus rubric metadata + scored drafts. The three blocks are:

- **Premises** — rubric citation (program code + funder + nofo number +
  rubric SHA-256) + RFA scope summary supplied by the caller.
- **Execution** — per-criterion score table (criterion id + score +
  max_points + confidence) plus the verbatim ``evidence_quote`` for each
  CriterionScore.
- **Conclusion** — total score / max_total + percent score + pass-or-fail
  flag against the funder's published threshold + mean confidence.

Pure-deterministic: stdlib + intra-package imports only; zero LLM, zero
network, zero subprocess, no I/O. Mirrors the Scribe-side compress
helpers' shape (frozen dataclass with explicit invariants checked at
__post_init__).

Threat model:

- **In scope.** Empty drafts → ``ValueError``; criterion id missing from
  rubric → ``ValueError`` (the verdict_assembler R2 already enforces; this
  module re-raises for defense-in-depth); negative pass_threshold → reject
  (a funder threshold of zero is technically valid; the report sets the
  default to the rubric ``min_score`` and surfaces a pass when total ≥
  threshold).
- **Out of scope, deferred.** Funder-specific tier classifications (e.g.
  VAPG's "competitive vs. non-competitive" ranges) — Judge ships the
  numeric score + boolean pass; downstream Editor or human-review surface
  decides the tier label.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Mapping, Union

from pipeline.seats.judge.types import (
    CriterionScore,
    JudgeVerdict,
    Rubric,
    RubricCriterion,
    RubricSubCriterion,
    SectionDraftLike,
)


# ---------------------------------------------------------------------------
# Block-name closed set (Premises / Execution / Conclusion)
# ---------------------------------------------------------------------------


SFR_BLOCK_NAMES: Final[tuple[str, ...]] = ("Premises", "Execution", "Conclusion")


# ---------------------------------------------------------------------------
# Frozen result shape
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class SfrLineItem:
    """One row of the per-criterion Execution table.

    ``criterion_id`` matches a :class:`CriterionScore.criterion_id`;
    ``max_points`` is the resolved unit's max_points (criterion.max_points
    when scored at criterion level; subcriterion.max_points when scored at
    subcriterion level).
    """

    criterion_id: str
    score: int
    max_points: int
    confidence: float
    evidence_quote: str
    rationale: str

    def __post_init__(self) -> None:
        if not self.criterion_id.strip():
            raise ValueError("SfrLineItem.criterion_id is empty.")
        if self.score < 0:
            raise ValueError(
                f"SfrLineItem({self.criterion_id!r}).score must be >= 0; "
                f"got {self.score!r}."
            )
        if self.max_points < 0:
            raise ValueError(
                f"SfrLineItem({self.criterion_id!r}).max_points must be >= 0; "
                f"got {self.max_points!r}."
            )
        if self.score > self.max_points:
            raise ValueError(
                f"SfrLineItem({self.criterion_id!r}).score "
                f"({self.score}) > max_points ({self.max_points})."
            )
        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError(
                f"SfrLineItem({self.criterion_id!r}).confidence must be "
                f"in [0.0, 1.0]; got {self.confidence!r}."
            )


@dataclass(frozen=True, kw_only=True, slots=True)
class SfrReport:
    """Three-block SFR report emitted alongside a :class:`JudgeVerdict`.

    Construction-time invariants:

    - ``program_code`` and ``funder`` non-empty; ``rubric_sha256`` 64-hex
      lowercase (matches :class:`Rubric.rubric_sha256`).
    - ``rfa_scope_summary`` non-empty (Premises block must cite scope).
    - ``line_items`` non-empty (every verdict has at least one criterion).
    - ``total_score`` matches ``sum(line_items[*].score)`` and ``max_total``
      matches ``sum(line_items[*].max_points)`` — caller supplies both for
      defense-in-depth (mismatch surfaces a programmer error rather than a
      silent SFR drift).
    - ``percent_score`` is ``total_score / max_total`` (when ``max_total``
      is 0 the rubric is degenerate; ``percent_score`` is forced to 0.0).
    - ``pass_threshold`` non-negative; ``passed`` ⇔ ``total_score >= pass_threshold``.
    - ``mean_confidence`` matches the arithmetic mean of
      ``line_items[*].confidence``.
    """

    program_code: str
    funder: str
    nofo_number: str
    rubric_sha256: str
    rfa_scope_summary: str
    line_items: tuple[SfrLineItem, ...]
    total_score: int
    max_total: int
    percent_score: float
    pass_threshold: int
    passed: bool
    mean_confidence: float

    def __post_init__(self) -> None:
        if not self.program_code.strip():
            raise ValueError("SfrReport.program_code is empty.")
        if not self.funder.strip():
            raise ValueError("SfrReport.funder is empty.")
        if not self.nofo_number.strip():
            raise ValueError("SfrReport.nofo_number is empty.")
        if len(self.rubric_sha256) != 64:
            raise ValueError(
                f"SfrReport.rubric_sha256 must be 64-hex chars; got "
                f"{len(self.rubric_sha256)}."
            )
        if self.rubric_sha256 != self.rubric_sha256.lower():
            raise ValueError("SfrReport.rubric_sha256 must be lowercase hex.")
        if not self.rfa_scope_summary.strip():
            raise ValueError("SfrReport.rfa_scope_summary is empty.")
        if not self.line_items:
            raise ValueError("SfrReport.line_items must be non-empty.")
        sum_score = sum(li.score for li in self.line_items)
        sum_max = sum(li.max_points for li in self.line_items)
        if sum_score != self.total_score:
            raise ValueError(
                f"SfrReport.total_score ({self.total_score}) does not match "
                f"sum(line_items[*].score)={sum_score}."
            )
        if sum_max != self.max_total:
            raise ValueError(
                f"SfrReport.max_total ({self.max_total}) does not match "
                f"sum(line_items[*].max_points)={sum_max}."
            )
        if self.pass_threshold < 0:
            raise ValueError(
                f"SfrReport.pass_threshold must be >= 0; got "
                f"{self.pass_threshold!r}."
            )
        # Verify percent_score consistency.
        if self.max_total == 0:
            expected_pct = 0.0
        else:
            expected_pct = self.total_score / self.max_total
        # Floating-point tolerance — 1e-9 is well below any rubric
        # discretization (worst case rubric: 0.5-pt granularity over 100
        # points = 0.005 percent).
        if abs(self.percent_score - expected_pct) > 1e-9:
            raise ValueError(
                f"SfrReport.percent_score ({self.percent_score}) does not "
                f"match total_score/max_total ({expected_pct})."
            )
        # passed flag invariant.
        expected_passed = self.total_score >= self.pass_threshold
        if self.passed != expected_passed:
            raise ValueError(
                f"SfrReport.passed ({self.passed}) does not match "
                f"total_score>=pass_threshold ({expected_passed})."
            )
        expected_mean_conf = sum(li.confidence for li in self.line_items) / len(
            self.line_items
        )
        if abs(self.mean_confidence - expected_mean_conf) > 1e-9:
            raise ValueError(
                f"SfrReport.mean_confidence ({self.mean_confidence}) does "
                f"not match arithmetic mean of line_items confidence "
                f"({expected_mean_conf})."
            )


# ---------------------------------------------------------------------------
# Resolution helpers (rubric criterion / subcriterion lookup)
# ---------------------------------------------------------------------------


def _resolve_unit_max_points(
    rubric: Rubric, criterion_id: str
) -> int:
    """Return the resolved unit's ``max_points`` for ``criterion_id``.

    Walks rubric.criteria + subcriteria; raises ``ValueError`` when the id
    is not a criterion or subcriterion of the rubric (programmer error —
    the verdict_assembler R2 should have caught this).
    """
    for crit in rubric.criteria:
        if crit.id == criterion_id:
            return crit.max_points
        for sub in crit.subcriteria:
            if sub.id == criterion_id:
                return sub.max_points
    raise ValueError(
        f"_resolve_unit_max_points: criterion_id={criterion_id!r} not found "
        f"in rubric {rubric.program_code!r}."
    )


# ---------------------------------------------------------------------------
# Public emitter
# ---------------------------------------------------------------------------


def emit_sfr(
    *,
    judge_verdict: JudgeVerdict,
    rubric: Rubric,
    section_drafts: tuple[SectionDraftLike, ...],
    rfa_scope_summary: str,
    pass_threshold: int | None = None,
) -> SfrReport:
    """Emit a frozen :class:`SfrReport` for a Judge run.

    Args:
        judge_verdict: the verdict produced by R2's
            :func:`pipeline.seats.judge.verdict_assembler.assemble_verdict`.
        rubric: the rubric the scores were computed against. Must match
            ``judge_verdict.rubric_program_code`` and
            ``judge_verdict.judge_output.rubric_sha256``.
        section_drafts: the drafts the scorer read. Must be non-empty —
            the SFR's Execution block cites at least one body. The
            ``evidence_quote`` substring discipline was already enforced at
            assembly; this emitter trusts those invariants.
        rfa_scope_summary: caller-supplied prose summarizing the RFA scope
            for the Premises block. Must be non-empty.
        pass_threshold: funder-published score threshold for "pass"; default
            is :attr:`Rubric.min_score`. Must be >= 0.

    Returns:
        A frozen :class:`SfrReport` ready for inclusion in the seat's
        stdout JudgeOutput payload.

    Raises:
        ValueError: rubric/verdict program-code drift; empty drafts / empty
            scope summary; criterion id not present in rubric.
    """
    if rubric.program_code != judge_verdict.rubric_program_code:
        raise ValueError(
            f"emit_sfr: rubric.program_code={rubric.program_code!r} != "
            f"judge_verdict.rubric_program_code="
            f"{judge_verdict.rubric_program_code!r}."
        )
    if rubric.rubric_sha256 != judge_verdict.judge_output.rubric_sha256:
        raise ValueError(
            f"emit_sfr: rubric.rubric_sha256={rubric.rubric_sha256!r} != "
            f"judge_verdict.judge_output.rubric_sha256="
            f"{judge_verdict.judge_output.rubric_sha256!r}."
        )
    if not section_drafts:
        raise ValueError("emit_sfr: section_drafts must be non-empty.")
    if not rfa_scope_summary or not rfa_scope_summary.strip():
        raise ValueError("emit_sfr: rfa_scope_summary must be non-empty.")

    threshold = (
        pass_threshold if pass_threshold is not None else rubric.min_score
    )
    if threshold < 0:
        raise ValueError(
            f"emit_sfr: pass_threshold must be >= 0; got {threshold!r}."
        )

    line_items: list[SfrLineItem] = []
    for sc in judge_verdict.judge_output.criterion_scores:
        max_points = _resolve_unit_max_points(rubric, sc.criterion_id)
        line_items.append(
            SfrLineItem(
                criterion_id=sc.criterion_id,
                score=sc.score,
                max_points=max_points,
                confidence=sc.confidence,
                evidence_quote=sc.evidence_quote,
                rationale=sc.rationale,
            )
        )
    line_items_tuple = tuple(line_items)
    total_score = judge_verdict.judge_output.total_score
    max_total = judge_verdict.judge_output.max_total
    percent_score = (total_score / max_total) if max_total > 0 else 0.0
    passed = total_score >= threshold
    mean_confidence = sum(li.confidence for li in line_items_tuple) / len(
        line_items_tuple
    )

    return SfrReport(
        program_code=rubric.program_code,
        funder=rubric.funder,
        nofo_number=rubric.nofo_number,
        rubric_sha256=rubric.rubric_sha256,
        rfa_scope_summary=rfa_scope_summary.strip(),
        line_items=line_items_tuple,
        total_score=total_score,
        max_total=max_total,
        percent_score=percent_score,
        pass_threshold=threshold,
        passed=passed,
        mean_confidence=mean_confidence,
    )


# ---------------------------------------------------------------------------
# Render helpers — produce the canonical three-block string for stdout
# ---------------------------------------------------------------------------


def render_sfr_text(report: SfrReport) -> str:
    """Render a human-readable three-block SFR string.

    Format is deterministic — line-oriented, no markdown fences. Block
    headers use the canonical names in :data:`SFR_BLOCK_NAMES`. The
    caller is responsible for embedding this string in the JudgeOutput
    JSON (or for emitting it as a sibling artifact).
    """
    lines: list[str] = []
    # ----- Premises -----
    lines.append(f"# {SFR_BLOCK_NAMES[0]}")
    lines.append("")
    lines.append(f"Rubric: {report.program_code} ({report.funder})")
    lines.append(f"NOFO: {report.nofo_number}")
    lines.append(f"Rubric SHA-256: {report.rubric_sha256}")
    lines.append("")
    lines.append("RFA Scope Summary:")
    lines.append(report.rfa_scope_summary)
    lines.append("")
    # ----- Execution -----
    lines.append(f"# {SFR_BLOCK_NAMES[1]}")
    lines.append("")
    lines.append("| Criterion | Score | Max | Confidence |")
    lines.append("|-----------|-------|-----|------------|")
    for li in report.line_items:
        lines.append(
            f"| {li.criterion_id} | {li.score} | {li.max_points} | "
            f"{li.confidence:.2f} |"
        )
    lines.append("")
    lines.append("## Evidence Quotes")
    lines.append("")
    for li in report.line_items:
        lines.append(f"### {li.criterion_id}")
        lines.append(f"> {li.evidence_quote}")
        lines.append("")
        lines.append(f"Rationale: {li.rationale}")
        lines.append("")
    # ----- Conclusion -----
    lines.append(f"# {SFR_BLOCK_NAMES[2]}")
    lines.append("")
    lines.append(
        f"Total: {report.total_score} / {report.max_total} "
        f"({report.percent_score * 100:.1f}%)"
    )
    lines.append(f"Pass threshold: {report.pass_threshold}")
    lines.append(f"Passed: {report.passed}")
    lines.append(f"Mean confidence: {report.mean_confidence:.2f}")
    return "\n".join(lines)


__all__ = [
    # Block-name closed set
    "SFR_BLOCK_NAMES",
    # Shapes
    "SfrLineItem",
    "SfrReport",
    # Public emitter
    "emit_sfr",
    "render_sfr_text",
]
