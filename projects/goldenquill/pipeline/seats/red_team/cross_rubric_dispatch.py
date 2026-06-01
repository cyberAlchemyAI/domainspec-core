"""pipeline.seats.red_team.cross_rubric_dispatch — parent-vs-subcriteria scoring selector.

Per §10.8 + OQ-10.8 (closed at R2 SCOPING DRAFT — match Judge's structure):
Red Team scores at the SAME structural level Judge scored at.

- If Judge scored a criterion at parent-level (no subcriteria), Red Team
  scores that criterion at parent-level.
- If Judge scored a criterion at subcriteria-level (one entry per
  subcriterion), Red Team scores at subcriteria-level for that criterion.

This module is the deterministic dispatcher: given a rubric and Judge's
per-criterion score map, it returns the set of (criterion_id_or_subcriteria_id,
max_points) entries Red Team must score against.

R2 ships pure-deterministic stdlib only; R3 wires this into the seat
runtime so the prompt-template carries the correct structural directive.
"""

from __future__ import annotations

from typing import Mapping, Protocol, runtime_checkable


# ---------------------------------------------------------------------------
# Forward-Protocols (match Judge's R1 RubricCriterion / RubricSubCriterion)
# ---------------------------------------------------------------------------


@runtime_checkable
class _SubCriterionLike(Protocol):
    """Forward-Protocol for Judge's :class:`RubricSubCriterion`."""

    id: str
    name: str
    max_points: int


@runtime_checkable
class _CriterionLike(Protocol):
    """Forward-Protocol for Judge's :class:`RubricCriterion`."""

    id: str
    name: str
    max_points: int
    subcriteria: tuple


@runtime_checkable
class _RubricLike(Protocol):
    """Forward-Protocol for Judge's :class:`Rubric`."""

    rubric_id: str
    criteria: tuple


# ---------------------------------------------------------------------------
# Dispatcher
# ---------------------------------------------------------------------------


def select_scoring_targets(
    *,
    rubric: _RubricLike,
    judge_scored_ids: frozenset[str],
) -> tuple[tuple[str, str, int], ...]:
    """Select the (id, name, max_points) tuples Red Team must score against.

    Args:
        rubric: Judge's rubric (or any structural match).
        judge_scored_ids: the set of criterion / subcriterion IDs that
            Judge actually scored. Determined by walking Judge's
            ``JudgeOutput.criterion_scores[*].criterion_id``.

    Returns:
        Tuple of ``(target_id, target_name, max_points)`` triples — exactly
        the IDs Red Team must score, in rubric-order. Each target is
        either a top-level criterion (when Judge scored at parent-level)
        or a subcriterion (when Judge scored at subcriteria-level).

    Per §10.8: identity-invariant means Red Team scores the SAME set of
    IDs Judge scored — not a superset, not a subset. F-RT-CRITERION-MISSING
    fires at POST-gate if Red Team's verdict carries a different ID set.

    Raises:
        ValueError: if any of ``judge_scored_ids`` doesn't appear in the
            rubric (Judge's IDs must be a subset of rubric IDs).
    """
    if not isinstance(judge_scored_ids, frozenset):
        # Defensive — frozen for hashability + immutability.
        judge_scored_ids = frozenset(judge_scored_ids)

    targets: list[tuple[str, str, int]] = []
    rubric_ids: set[str] = set()

    for criterion in rubric.criteria:
        rubric_ids.add(criterion.id)
        if criterion.subcriteria:
            # Hierarchical: enumerate subcriteria.
            for sub in criterion.subcriteria:
                rubric_ids.add(sub.id)
                if sub.id in judge_scored_ids:
                    targets.append((sub.id, sub.name, sub.max_points))
            # If Judge scored the parent (mixed mode), include parent too —
            # but coverage rule from §9 R2 (parent OR all-subs) means this
            # rarely happens. Include for completeness.
            if criterion.id in judge_scored_ids:
                targets.append((criterion.id, criterion.name, criterion.max_points))
        else:
            # Flat: parent only.
            if criterion.id in judge_scored_ids:
                targets.append((criterion.id, criterion.name, criterion.max_points))

    # Verify all judge-scored IDs are accounted for.
    unknown = judge_scored_ids - rubric_ids
    if unknown:
        raise ValueError(
            f"judge_scored_ids contains IDs not in rubric: {sorted(unknown)}"
        )

    return tuple(targets)


def assert_red_team_id_set_matches_judge(
    *,
    red_team_scored_ids: frozenset[str],
    judge_scored_ids: frozenset[str],
) -> tuple[str, ...]:
    """Identity-invariant pre-check: Red Team's IDs must equal Judge's IDs.

    Returns a tuple of human-readable violation strings; empty tuple ⇒
    PASS. Per §10.8: F-RT-CRITERION-MISSING fires if Red Team's set differs
    from Judge's set.
    """
    if not isinstance(red_team_scored_ids, frozenset):
        red_team_scored_ids = frozenset(red_team_scored_ids)
    if not isinstance(judge_scored_ids, frozenset):
        judge_scored_ids = frozenset(judge_scored_ids)
    violations: list[str] = []
    missing_in_red_team = judge_scored_ids - red_team_scored_ids
    extra_in_red_team = red_team_scored_ids - judge_scored_ids
    if missing_in_red_team:
        violations.append(
            f"F-RT-CRITERION-MISSING: Red Team did not score "
            f"{sorted(missing_in_red_team)}"
        )
    if extra_in_red_team:
        violations.append(
            f"F-RT-CRITERION-MISSING: Red Team scored unexpected IDs "
            f"{sorted(extra_in_red_team)} (not in Judge's scored set)"
        )
    return tuple(violations)


__all__ = [
    "select_scoring_targets",
    "assert_red_team_id_set_matches_judge",
]
