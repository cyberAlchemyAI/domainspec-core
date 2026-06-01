"""pipeline.seats.judge.cross_rubric_dispatch — §9 R2 dispatcher.

Routes the criteria of a :class:`pipeline.seats.judge.types.Rubric` to
the correct scorer-role handler bucket and surfaces the actual scoring
units (subcriteria when present, else parent criterion) so the R3
orchestrator iterates a flat tuple of "things to score."

Pure-deterministic at R2: stdlib + intra-package imports only; zero LLM,
zero network, zero subprocess, no I/O. Both functions are total — no
side effects, no globals mutation.

Threat model (R2):

- **In scope.** Empty ``rubric.criteria`` is impossible by construction
  (Rubric ``__post_init__`` rejects); :func:`dispatch_criteria_to_scorers`
  preserves criterion order within a role bucket; missing role key in
  the returned mapping ⇒ no criteria with that scorer (empty tuple).
  :func:`dispatch_score_units` always produces at least one unit per
  criterion (the criterion itself when no subcriteria, or every
  subcriterion otherwise) and therefore always returns a non-empty tuple.
- **Out of scope, deferred.** Multi-rubric merging into a
  ``JudgeVerdictBundle`` (per spec card §5: single-rubric-per-invocation
  unless §9 blueprint mandates merging — §9 blueprint is deferred);
  scorer-role-specific prompt variation (R3 seat decides whether
  administrator-discretionary criteria use a different LLM-call shape);
  rubric-library cross-checks (a separate cross-rubric verification
  pass over the JudgeVerdict).

§9 design decision pin: the dispatcher returns the canonical scoring
units rather than always-criterion-level. Subcriteria-bearing criteria
(e.g., VAPG ``a`` with ``a.i``/``a.ii``/``a.iii``) score per-subcriterion
because the LLM's max_points context is more accurate at the
subcriterion level (10 pts) than at the rolled-up parent (30 pts);
no-subcriterion criteria (e.g., VAPG ``b`` flat 20 pts) score at the
criterion level. Mixing modes within a single criterion (some subs
scored, some skipped) is rejected by
:func:`pipeline.seats.judge.verdict_assembler.assemble_verdict`.
"""

from __future__ import annotations

from typing import Mapping, Union

from pipeline.seats.judge.types import (
    Rubric,
    RubricCriterion,
    RubricScorerRole,
    RubricSubCriterion,
)


# ---------------------------------------------------------------------------
# Closed-set Literal mirror — V1 inline-literal rebind-resistance
# ---------------------------------------------------------------------------

# Same closed set as types._RUBRIC_SCORER_ROLES; copied here as an
# inline literal so the dispatcher does not import a private symbol
# across module boundaries (V1 discipline + import-graph cleanliness).
_SCORER_ROLES: tuple[RubricScorerRole, ...] = (
    "review_panel",
    "state_office",
    "administrator",
)


# ---------------------------------------------------------------------------
# Public dispatcher API
# ---------------------------------------------------------------------------


def dispatch_criteria_to_scorers(
    rubric: Rubric,
) -> Mapping[RubricScorerRole, tuple[RubricCriterion, ...]]:
    """Partition the rubric's criteria into per-scorer-role buckets.

    Returns a mapping with every scorer-role key present (empty tuple
    when no criteria carry that role). Order within a bucket follows the
    rubric's ``criteria`` order. The returned mapping is a fresh
    ``dict`` — caller may mutate without affecting the rubric.

    For VAPG FY26: ``review_panel`` → ``(a, b, c)``; ``state_office`` →
    ``(d, e, f)``; ``administrator`` → ``(g,)``.
    """
    buckets: dict[RubricScorerRole, list[RubricCriterion]] = {
        role: [] for role in _SCORER_ROLES
    }
    for crit in rubric.criteria:
        # Rubric.__post_init__ already validates scorer is a member of
        # _RUBRIC_SCORER_ROLES; this lookup is therefore total.
        buckets[crit.scorer].append(crit)
    return {role: tuple(buckets[role]) for role in _SCORER_ROLES}


def dispatch_score_units(
    rubric: Rubric,
) -> tuple[Union[RubricCriterion, RubricSubCriterion], ...]:
    """Flatten the rubric's criteria into the canonical iteration of
    "things to score."

    Rule:

    - If a :class:`RubricCriterion` has non-empty ``subcriteria``, every
      subcriterion is emitted (in declared order) and the parent itself
      is NOT emitted.
    - If a criterion has empty ``subcriteria``, the criterion itself is
      emitted.

    Order is the rubric's declared criterion order; within a criterion,
    subcriteria preserve their declared order. This matches the
    flattening expected by R3's per-unit ``score_dimension`` calls.

    Examples (VAPG FY26): ``a``-with-subs → ``(a.i, a.ii, a.iii)``;
    ``b``-flat → ``(b,)``; full rubric → ``(a.i, a.ii, a.iii, b, c, d,
    e, f.i, f.ii, g)`` for a length of 10.
    """
    units: list[Union[RubricCriterion, RubricSubCriterion]] = []
    for crit in rubric.criteria:
        if crit.subcriteria:
            for sub in crit.subcriteria:
                units.append(sub)
        else:
            units.append(crit)
    return tuple(units)


def parent_criterion_for_unit(
    unit: Union[RubricCriterion, RubricSubCriterion],
    rubric: Rubric,
) -> RubricCriterion:
    """Resolve the parent :class:`RubricCriterion` for a scoring unit.

    A unit that is itself a :class:`RubricCriterion` is its own parent.
    A unit that is a :class:`RubricSubCriterion` is matched against the
    rubric's criteria by walking each criterion's ``subcriteria`` and
    returning the criterion whose subcriterion has the same ``id``.

    Raises:
        ValueError: the unit is a :class:`RubricSubCriterion` whose id
            does not appear under any criterion of the rubric — this is
            a programmer error (the unit was not produced by
            :func:`dispatch_score_units` over the given rubric).
    """
    if isinstance(unit, RubricCriterion):
        return unit
    for crit in rubric.criteria:
        for sub in crit.subcriteria:
            if sub.id == unit.id:
                return crit
    raise ValueError(
        f"parent_criterion_for_unit: subcriterion id {unit.id!r} not found "
        f"under any criterion of rubric {rubric.program_code!r}."
    )


__all__ = [
    "dispatch_criteria_to_scorers",
    "dispatch_score_units",
    "parent_criterion_for_unit",
]
