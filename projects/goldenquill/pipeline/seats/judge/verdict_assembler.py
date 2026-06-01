"""pipeline.seats.judge.verdict_assembler — §9 R2 :class:`JudgeVerdict` builder.

Composes a tuple of :class:`pipeline.seats.judge.types.CriterionScore`
instances + a :class:`Rubric` + the section drafts that were scored
into a frozen :class:`pipeline.seats.judge.types.JudgeVerdict`.

Validation discipline (R2 enforcement; R3 wires a Logician POST-gate
for each):

- **Rubric-hash continuity** — the rubric's ``rubric_sha256`` is
  carried verbatim into the assembled :class:`JudgeOutput`. Drift
  between the rubric the scorer used and the rubric the assembler
  binds → :data:`pipeline.seats.judge.types.F_JUDGE_RUBRIC_HASH_DRIFT`.
- **Criterion coverage** — every rubric criterion must be covered
  exactly once: either by a single :class:`CriterionScore` whose
  ``criterion_id`` matches the criterion id, OR by exactly one
  :class:`CriterionScore` per subcriterion of that criterion. Mixed
  coverage (some subs scored, some skipped, parent absent) →
  :data:`F_JUDGE_CRITERION_MISSING`.
- **Score-band sanity** — every score is non-negative and ≤ the unit's
  ``max_points``; sum-of-scores ≤ rubric ``max_score``. Violations →
  :data:`F_JUDGE_SCORE_OUT_OF_BOUND`.
- **Evidence-in-draft (Law 5)** — every ``evidence_quote`` must be a
  verbatim substring of at least one scored
  :class:`SectionDraftLike.body_text`. Pre-gate for R3's Logician
  POST-gate :data:`F_JUDGE_EVIDENCE_NOT_IN_DRAFT`. R2 raises a
  ``ValueError`` tagged with the same code so the assembler refuses
  to construct an unsourced verdict before persistence.

Pure-deterministic: stdlib + intra-package imports only; zero LLM,
zero network, zero subprocess, no I/O. The clock is the only injected
seam (matches the seat-wide convention).

Threat model (R2):

- **In scope.** Empty ``criterion_scores`` → ``ValueError``. Duplicate
  ``criterion_id`` in scores → ``ValueError`` tagged
  ``F-JUDGE-CRITERION-MISSING`` (silent re-scoring is a coverage
  violation). Score id not present in rubric (neither as criterion nor
  as subcriterion) → ``ValueError`` tagged
  ``F-JUDGE-CRITERION-MISSING``. Empty ``section_drafts`` → ``ValueError``.
- **Out of scope, deferred to R3.** Logician PRE/POST gate wiring;
  cross-rubric library cross-check (Judge library spec); SFR format
  emission; multi-rubric ``JudgeVerdictBundle``.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Callable, Mapping, Union

from pipeline.seats.judge.types import (
    CriterionScore,
    F_JUDGE_CRITERION_MISSING,
    F_JUDGE_EVIDENCE_NOT_IN_DRAFT,
    F_JUDGE_RUBRIC_HASH_DRIFT,
    F_JUDGE_SCORE_OUT_OF_BOUND,
    JudgeOutput,
    JudgeVerdict,
    ResponsivenessMap,
    Rubric,
    RubricCriterion,
    RubricSubCriterion,
    SectionDraftLike,
)


ClockFn = Callable[[], datetime]


def _default_utc_now() -> datetime:
    return datetime.now(tz=timezone.utc)


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _build_score_index(
    rubric: Rubric,
) -> tuple[
    Mapping[str, RubricCriterion],
    Mapping[str, tuple[RubricCriterion, RubricSubCriterion]],
]:
    """Return ``(criterion_by_id, subcriterion_by_id)`` lookup maps.

    ``subcriterion_by_id`` maps a subcriterion id to a
    ``(parent_criterion, subcriterion)`` tuple so the assembler can
    resolve the parent's max_points + coverage in a single dict lookup.
    """
    crit_by_id: dict[str, RubricCriterion] = {}
    sub_by_id: dict[str, tuple[RubricCriterion, RubricSubCriterion]] = {}
    for crit in rubric.criteria:
        crit_by_id[crit.id] = crit
        for sub in crit.subcriteria:
            sub_by_id[sub.id] = (crit, sub)
    return crit_by_id, sub_by_id


def _check_evidence_in_drafts(
    score: CriterionScore, drafts: tuple[SectionDraftLike, ...]
) -> None:
    """Raise if ``score.evidence_quote`` is not a verbatim substring of
    any ``drafts[*].body_text``.

    Empty quote is rejected (cannot be a substring of nothing-meaningful;
    R3's Logician gate would also reject; R2 fails earlier for a clearer
    error message). Whitespace-only quote also rejected.
    """
    quote = score.evidence_quote
    if not isinstance(quote, str) or not quote.strip():
        raise ValueError(
            f"{F_JUDGE_EVIDENCE_NOT_IN_DRAFT}: criterion "
            f"{score.criterion_id!r} evidence_quote is empty or "
            f"whitespace-only."
        )
    for draft in drafts:
        if quote in draft.body_text:
            return
    raise ValueError(
        f"{F_JUDGE_EVIDENCE_NOT_IN_DRAFT}: criterion {score.criterion_id!r} "
        f"evidence_quote is not a verbatim substring of any scored "
        f"section_drafts.body_text."
    )


def _check_score_bound(
    score: CriterionScore,
    unit: Union[RubricCriterion, RubricSubCriterion],
) -> None:
    if score.score < 0 or score.score > unit.max_points:
        raise ValueError(
            f"{F_JUDGE_SCORE_OUT_OF_BOUND}: criterion {score.criterion_id!r} "
            f"score={score.score!r} outside [0, {unit.max_points}]."
        )


def _coverage_max_for_criterion(
    crit: RubricCriterion,
    score_ids: frozenset[str],
) -> tuple[bool, int]:
    """Check that ``crit`` is covered exactly once by ``score_ids`` and
    return ``(covered, max_for_crit)`` — ``max_for_crit`` is the sum of
    max_points contributed to the rubric total by this coverage path
    (parent.max_points if parent-covered; sum of sub.max_points for
    every sub-covered subcriterion).

    Raises:
        ValueError: tagged ``F-JUDGE-CRITERION-MISSING`` when coverage
            is partial / mixed / missing.
    """
    parent_covered = crit.id in score_ids
    sub_ids = tuple(sub.id for sub in crit.subcriteria)
    sub_covered_flags = tuple(sid in score_ids for sid in sub_ids)
    any_sub_covered = any(sub_covered_flags)
    all_sub_covered = bool(sub_ids) and all(sub_covered_flags)

    if parent_covered and any_sub_covered:
        raise ValueError(
            f"{F_JUDGE_CRITERION_MISSING}: criterion {crit.id!r} is covered "
            f"both at parent level AND at subcriterion level — pick one "
            f"coverage path per criterion."
        )
    if parent_covered:
        return True, crit.max_points
    if not crit.subcriteria:
        # No subcriteria → must be parent-covered.
        raise ValueError(
            f"{F_JUDGE_CRITERION_MISSING}: criterion {crit.id!r} has no "
            f"subcriteria and no CriterionScore for the criterion id."
        )
    if all_sub_covered:
        return True, sum(sub.max_points for sub in crit.subcriteria)
    if any_sub_covered:
        # Partial sub-coverage — name the missing subs explicitly.
        missing = tuple(
            sub_ids[i] for i, covered in enumerate(sub_covered_flags) if not covered
        )
        raise ValueError(
            f"{F_JUDGE_CRITERION_MISSING}: criterion {crit.id!r} has "
            f"partial subcriterion coverage; missing: {missing!r}."
        )
    raise ValueError(
        f"{F_JUDGE_CRITERION_MISSING}: criterion {crit.id!r} is uncovered "
        f"(neither the criterion id nor any subcriterion id appears in "
        f"criterion_scores)."
    )


# ---------------------------------------------------------------------------
# Public assembler
# ---------------------------------------------------------------------------


def assemble_verdict(
    criterion_scores: tuple[CriterionScore, ...],
    *,
    rubric: Rubric,
    section_drafts: tuple[SectionDraftLike, ...],
    rfa_content_sha3_512: str,
    responsiveness_map: ResponsivenessMap,
    rubric_sha256_at_score_time: str,
    scored_at_utc: datetime,
    clock: ClockFn = _default_utc_now,
) -> JudgeVerdict:
    """Assemble a :class:`JudgeVerdict` from per-unit scores + rubric +
    drafts.

    Validation order (fail-loudest-first):

    1. ``criterion_scores`` non-empty; ``section_drafts`` non-empty;
       ``rubric_sha256_at_score_time`` matches ``rubric.rubric_sha256``
       (drift check before any other inspection).
    2. Every score's ``criterion_id`` resolves to a rubric criterion or
       subcriterion (else ``F-JUDGE-CRITERION-MISSING``); duplicate ids
       → same code.
    3. Every score satisfies ``[0, max_points]`` against its resolved
       unit (else ``F-JUDGE-SCORE-OUT-OF-BOUND``).
    4. Every ``evidence_quote`` is a verbatim substring of at least one
       ``section_drafts[*].body_text`` (else
       ``F-JUDGE-EVIDENCE-NOT-IN-DRAFT``).
    5. Every rubric criterion has exactly-one coverage path (parent
       OR all-subcriteria); mixed / partial / missing coverage →
       ``F-JUDGE-CRITERION-MISSING``.
    6. ``total_score = sum(scores[*].score)``;
       ``max_total = sum(coverage-contributing max_points)``;
       ``total_score <= max_total`` (sanity); ``max_total ≤ rubric.max_score``.

    Args:
        criterion_scores: one entry per scored unit. Order is preserved
            in the assembled :class:`JudgeOutput`.
        rubric: the rubric the scores were computed against.
        section_drafts: the drafts the scorer read.
        rfa_content_sha3_512: 128-hex SHA-3-512 of the RFA content
            (mirrors the value Scribe carried — Judge does not re-hash
            the RFA at R2; that ships at R3 with the seat subprocess).
        responsiveness_map: pre-built map from
            :func:`pipeline.seats.judge.responsiveness_mapper.build_responsiveness_map`.
            Pass an empty :class:`ResponsivenessMap` for a technical-only
            rubric.
        rubric_sha256_at_score_time: the rubric_sha256 the scorer
            captured before invoking the LLM. Compared against
            ``rubric.rubric_sha256`` to detect drift between load and
            assembly.
        scored_at_utc: timestamp the scorer attached to the run.
        clock: injected clock — produces ``assembled_at_utc``. Default
            wires ``datetime.now(tz=UTC)``.

    Returns:
        A frozen :class:`JudgeVerdict`.

    Raises:
        ValueError: any validation failure; the message carries the
            originating ``F-JUDGE-*`` code as a prefix.
    """
    if not criterion_scores:
        raise ValueError(
            "assemble_verdict: criterion_scores must be non-empty."
        )
    if not section_drafts:
        raise ValueError(
            "assemble_verdict: section_drafts must be non-empty."
        )
    if rubric_sha256_at_score_time != rubric.rubric_sha256:
        raise ValueError(
            f"{F_JUDGE_RUBRIC_HASH_DRIFT}: rubric_sha256_at_score_time="
            f"{rubric_sha256_at_score_time!r} does not match "
            f"rubric.rubric_sha256={rubric.rubric_sha256!r}."
        )

    crit_by_id, sub_by_id = _build_score_index(rubric)

    # Step 2 + 3 + 4: per-score validation.
    seen_ids: set[str] = set()
    score_id_to_unit: dict[
        str, Union[RubricCriterion, RubricSubCriterion]
    ] = {}
    for sc in criterion_scores:
        if sc.criterion_id in seen_ids:
            raise ValueError(
                f"{F_JUDGE_CRITERION_MISSING}: duplicate "
                f"CriterionScore.criterion_id={sc.criterion_id!r}."
            )
        seen_ids.add(sc.criterion_id)
        if sc.criterion_id in crit_by_id:
            unit: Union[RubricCriterion, RubricSubCriterion] = crit_by_id[
                sc.criterion_id
            ]
        elif sc.criterion_id in sub_by_id:
            unit = sub_by_id[sc.criterion_id][1]
        else:
            raise ValueError(
                f"{F_JUDGE_CRITERION_MISSING}: CriterionScore.criterion_id="
                f"{sc.criterion_id!r} is not a criterion or subcriterion "
                f"id in rubric {rubric.program_code!r}."
            )
        score_id_to_unit[sc.criterion_id] = unit
        _check_score_bound(sc, unit)
        _check_evidence_in_drafts(sc, section_drafts)

    # Step 5: rubric-criterion coverage.
    score_id_set = frozenset(seen_ids)
    max_total = 0
    for crit in rubric.criteria:
        _, max_for_crit = _coverage_max_for_criterion(crit, score_id_set)
        max_total += max_for_crit

    # Step 6: total_score sanity. Both branches are downstream of the
    # per-score bound check (Step 3) and Rubric.__post_init__'s
    # max_score >= sum-of-criterion-max-points invariant — they cannot
    # trip on a well-formed rubric + bound-checked scores. R3 keeps
    # them as defense-in-depth against future Rubric invariant changes.
    total_score = sum(sc.score for sc in criterion_scores)
    if total_score > max_total:  # pragma: no cover — sanity guard, score-bound check upstream prevents this
        raise ValueError(
            f"{F_JUDGE_SCORE_OUT_OF_BOUND}: total_score ({total_score}) > "
            f"max_total ({max_total})."
        )
    if max_total > rubric.max_score:  # pragma: no cover — sanity guard, Rubric.__post_init__ enforces upstream
        raise ValueError(
            f"{F_JUDGE_SCORE_OUT_OF_BOUND}: coverage max_total ({max_total}) "
            f"> rubric.max_score ({rubric.max_score})."
        )

    judge_output = JudgeOutput(
        criterion_scores=criterion_scores,
        total_score=total_score,
        max_total=max_total,
        rubric_sha256=rubric.rubric_sha256,
        rfa_content_sha3_512=rfa_content_sha3_512,
        scored_at_utc=scored_at_utc,
    )
    assembled_at_utc = clock()
    return JudgeVerdict(
        judge_output=judge_output,
        rubric_program_code=rubric.program_code,
        responsiveness_map=responsiveness_map,
        assembled_at_utc=assembled_at_utc,
    )


__all__ = [
    "ClockFn",
    "assemble_verdict",
]
