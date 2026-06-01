"""pipeline.seats.red_team.attack_memo — composer + Law 5 verbatim pre-check.

Round 1 ships:

- :func:`compose_red_team_verdict` — assembles a :class:`RedTeamVerdict` from
  the model's parsed JSON + the input bundle, applying the §10.8
  computed-from-criteria authoritative invariant (auto-correction logged in
  ``total_score_correction`` if the model's reported total disagreed).
- :func:`assert_evidence_in_drafts` — Law 5 verbatim-substring pre-check
  walked over every cited evidence in the verdict against the input
  bundle's section drafts. Returns the list of violations; empty list ⇒
  pre-check PASS. R3 wires this into a Logician POST-gate (F-RT-EVIDENCE-
  NOT-IN-DRAFT).

R1 is pure-deterministic: zero LLM, zero network, zero subprocess. The
caller is responsible for the model call + JSON parse; this module
consumes parsed dicts and emits typed shapes.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Final, Sequence

from pipeline.seats.red_team.types import (
    AttackMemo,
    F_RT_EVIDENCE_NOT_IN_DRAFT,
    F_RT_RECOMMENDATION_INVALID,
    F_RT_WEAKNESS_FIELD_MISSING,
    F_RT_WEAKNESSES_EMPTY,
    RedTeamCriterionScore,
    RedTeamDialect,
    RedTeamInput,
    RedTeamVerdict,
    SectionDraftLike,
    TotalScoreCorrection,
    Weakness,
    _RT_RECOMMENDATIONS,
)


# ---------------------------------------------------------------------------
# Composer
# ---------------------------------------------------------------------------


def _coerce_weaknesses(raw: Sequence[dict]) -> tuple[Weakness, ...]:
    """Coerce raw model JSON list-of-dicts into typed Weakness tuple.

    Raises :class:`ValueError` with F-RT-WEAKNESS-FIELD-MISSING-style detail
    when any required field is absent.
    """
    if not raw:
        raise ValueError(
            f"{F_RT_WEAKNESSES_EMPTY}: top_weaknesses empty (Red Team must "
            f"produce at least one weakness)"
        )
    out: list[Weakness] = []
    for i, w in enumerate(raw):
        if not isinstance(w, dict):
            raise TypeError(f"top_weaknesses[{i}] must be dict; got {type(w).__name__}")
        for required in ("severity", "claim", "why_it_fails", "what_a_reviewer_would_say", "fix_hint"):
            if required not in w or not isinstance(w[required], str) or not w[required].strip():
                raise ValueError(
                    f"{F_RT_WEAKNESS_FIELD_MISSING}: top_weaknesses[{i}].{required} "
                    f"missing or empty"
                )
        out.append(
            Weakness(
                severity=w["severity"],  # type: ignore[arg-type]
                claim=w["claim"],
                why_it_fails=w["why_it_fails"],
                what_a_reviewer_would_say=w["what_a_reviewer_would_say"],
                fix_hint=w["fix_hint"],
            )
        )
    return tuple(out)


def _coerce_criteria(
    raw: Sequence[dict], rubric_max_points_by_id: dict[str, int]
) -> tuple[RedTeamCriterionScore, ...]:
    """Coerce raw model JSON list-of-dicts into typed RedTeamCriterionScore tuple."""
    out: list[RedTeamCriterionScore] = []
    for i, c in enumerate(raw):
        if not isinstance(c, dict):
            raise TypeError(
                f"criteria[{i}] must be dict; got {type(c).__name__}"
            )
        # Defaults for missing optional fields:
        notes = c.get("notes", "")
        missing = tuple(c.get("missing", ())) if isinstance(c.get("missing", ()), (list, tuple)) else ()
        cid = c.get("id") or c.get("criterion_id")
        cname = c.get("name") or c.get("criterion_name") or cid
        if not cid:
            raise ValueError(f"criteria[{i}]: id/criterion_id missing")
        max_points = c.get("max_points") or rubric_max_points_by_id.get(cid)
        if max_points is None:
            raise ValueError(
                f"criteria[{i}] ({cid}): max_points missing in both model output "
                f"and rubric"
            )
        out.append(
            RedTeamCriterionScore(
                criterion_id=str(cid),
                criterion_name=str(cname),
                max_points=int(max_points),
                score=int(c["score"]),
                tier_matched=str(c.get("tier_matched", "")),
                evidence=str(c.get("evidence", "")),
                missing=tuple(str(x) for x in missing),
                notes=str(notes),
            )
        )
    return tuple(out)


def compose_red_team_verdict(
    *,
    parsed_model_output: dict,
    input_bundle: RedTeamInput,
    rubric_max_points_by_id: dict[str, int],
    rubric_max_score: int,
    red_team_dialect: RedTeamDialect = "conservative",
    verdict_at_utc: datetime | None = None,
) -> RedTeamVerdict:
    """Assemble a :class:`RedTeamVerdict` from a parsed model JSON dict.

    The §10.8 computed-from-criteria authoritative invariant is enforced:
    ``total_score`` is always the sum of ``criteria[*].score``. If the
    model's reported ``total_score`` disagreed, the disagreement is captured
    in ``total_score_correction`` (audit trail) but the verdict's authoritative
    total is the computed sum.

    Raises :class:`ValueError` with structured F-code prefix when invariants
    are violated at the model layer (recommendation invalid, weaknesses
    empty, etc.).
    """
    raw_criteria = parsed_model_output.get("criteria", [])
    criteria = _coerce_criteria(raw_criteria, rubric_max_points_by_id)

    raw_memo = parsed_model_output.get("attack_memo", {})
    weaknesses = _coerce_weaknesses(raw_memo.get("top_weaknesses", []))
    memo = AttackMemo(
        top_weaknesses=weaknesses,
        unsupported_assertions=tuple(
            str(s) for s in raw_memo.get("unsupported_assertions", ())
        ),
        dialect_mismatches=tuple(
            str(s) for s in raw_memo.get("dialect_mismatches", ())
        ),
        boundary_drift=tuple(str(s) for s in raw_memo.get("boundary_drift", ())),
        overall_verdict=str(raw_memo.get("overall_verdict", "")),
    )

    recommendation = parsed_model_output.get("recommendation")
    if recommendation not in _RT_RECOMMENDATIONS:
        raise ValueError(
            f"{F_RT_RECOMMENDATION_INVALID}: recommendation must be one of "
            f"{sorted(_RT_RECOMMENDATIONS)}; got {recommendation!r}"
        )

    # §10.8 computed-from-criteria authoritative invariant.
    computed_sum = sum(c.score for c in criteria)
    model_reported_raw = parsed_model_output.get("total_score")
    correction: TotalScoreCorrection | None = None
    if isinstance(model_reported_raw, int) and model_reported_raw != computed_sum:
        correction = TotalScoreCorrection(
            model_reported=model_reported_raw,
            computed_from_criteria=computed_sum,
            delta=computed_sum - model_reported_raw,
        )

    return RedTeamVerdict(
        run_id=input_bundle.run_id,
        rubric_id=input_bundle.rubric.rubric_id,
        rubric_hash=input_bundle.rubric.content_hash,
        total_score=computed_sum,
        max_score=rubric_max_score,
        recommendation=recommendation,  # type: ignore[arg-type]
        criteria=criteria,
        attack_memo=memo,
        total_score_correction=correction,
        verdict_at_utc=verdict_at_utc or datetime.now(tz=timezone.utc),
        red_team_dialect=red_team_dialect,
    )


# ---------------------------------------------------------------------------
# Law 5 verbatim-substring pre-check (R3 wires Logician POST-gate)
# ---------------------------------------------------------------------------


def _draft_body_concatenated(drafts: Sequence[SectionDraftLike]) -> str:
    """Concatenate all section bodies for substring search.

    R1 uses a simple flatten; R3's POST-gate may scope the substring search
    to the section the criterion targets (more precise; less expensive on
    large drafts). The flatten is correct-by-construction for R1: a verbatim
    quote MUST appear somewhere in the draft set.
    """
    return "\n\n".join(d.body_text for d in drafts)


def assert_evidence_in_drafts(
    *,
    verdict: RedTeamVerdict,
    drafts: Sequence[SectionDraftLike],
) -> tuple[str, ...]:
    """Walk every cited evidence string and verify byte-identical substring.

    Per §10.9 ``F-RT-EVIDENCE-NOT-IN-DRAFT`` (Law 5 mirror). Returns a tuple
    of human-readable violation strings; empty tuple ⇒ pre-check PASS.

    R3 wires this into the Logician POST-gate; R1 uses it for unit tests
    + the composer's optional pre-check.
    """
    body = _draft_body_concatenated(drafts)
    violations: list[str] = []

    # Per-criterion evidence quotes
    for crit in verdict.criteria:
        if crit.evidence and crit.evidence not in body:
            violations.append(
                f"{F_RT_EVIDENCE_NOT_IN_DRAFT}: criteria[{crit.criterion_id}].evidence "
                f"not a verbatim substring of any draft body_text "
                f"(first 80 chars of evidence: {crit.evidence[:80]!r})"
            )

    # Per-weakness claim quotes
    for i, weakness in enumerate(verdict.attack_memo.top_weaknesses):
        if weakness.claim not in body:
            violations.append(
                f"{F_RT_EVIDENCE_NOT_IN_DRAFT}: top_weaknesses[{i}].claim not "
                f"verbatim substring (first 80 chars: {weakness.claim[:80]!r})"
            )

    # attack_memo string lists
    for field_name in ("unsupported_assertions", "dialect_mismatches", "boundary_drift"):
        items: tuple[str, ...] = getattr(verdict.attack_memo, field_name)
        for i, item in enumerate(items):
            if item not in body:
                violations.append(
                    f"{F_RT_EVIDENCE_NOT_IN_DRAFT}: attack_memo.{field_name}[{i}] not "
                    f"verbatim substring (first 80 chars: {item[:80]!r})"
                )

    return tuple(violations)


# ---------------------------------------------------------------------------
# Council-split detection helper (R3 wires POST-gate; R1 ships pure logic)
# ---------------------------------------------------------------------------

RT_DISAGREEMENT_THRESHOLD: Final[int] = 10
RT_ANCHOR_SUSPECTED_THRESHOLD: Final[int] = 2


# Mirror §5 v7 §8 module-load asserts in this module too — V1 inline-literal
# rebind-resistance against any same-uid peer mutating the constant.
assert RT_DISAGREEMENT_THRESHOLD == 10, (
    "RT_DISAGREEMENT_THRESHOLD rebound at module load; refusing to load "
    "pipeline.seats.red_team.attack_memo"
)
assert RT_ANCHOR_SUSPECTED_THRESHOLD == 2, (
    "RT_ANCHOR_SUSPECTED_THRESHOLD rebound at module load; refusing to load "
    "pipeline.seats.red_team.attack_memo"
)


def detect_council_split(
    *,
    judge_total_score: int,
    red_team_total_score: int,
    threshold: int = RT_DISAGREEMENT_THRESHOLD,
) -> bool:
    """Return ``True`` iff |judge - red_team| >= threshold.

    Per §10.6: boundary INCLUSIVE at threshold. Default threshold is the
    canonical RT_DISAGREEMENT_THRESHOLD = 10. Operator-override carries
    a different threshold per `PROJECT_CONTEXT.rt_disagreement_threshold_override`
    — caller responsibility to substitute.
    """
    if not isinstance(judge_total_score, int) or judge_total_score < 0:
        raise ValueError(f"judge_total_score must be non-negative int; got {judge_total_score!r}")
    if not isinstance(red_team_total_score, int) or red_team_total_score < 0:
        raise ValueError(
            f"red_team_total_score must be non-negative int; got {red_team_total_score!r}"
        )
    if not isinstance(threshold, int) or threshold < 0:
        raise ValueError(f"threshold must be non-negative int; got {threshold!r}")
    return abs(judge_total_score - red_team_total_score) >= threshold


def detect_judge_anchor_suspected(
    *,
    judge_total_score: int,
    red_team_total_score: int,
    rubric_criteria_count: int,
    total_words: int,
    advisory_threshold: int = RT_ANCHOR_SUSPECTED_THRESHOLD,
) -> bool:
    """Return ``True`` iff the suspect-anchoring smoke check fires.

    Per §10.6: ``|judge - red_team| < advisory_threshold`` AND
    ``rubric_criteria_count >= 5`` AND ``total_words >= 1000``. Non-blocking
    advisory only; surfaces as admin-risk LOW-severity at sign-off.
    """
    if rubric_criteria_count < 5:
        return False
    if total_words < 1000:
        return False
    return abs(judge_total_score - red_team_total_score) < advisory_threshold


__all__ = [
    "RT_DISAGREEMENT_THRESHOLD",
    "RT_ANCHOR_SUSPECTED_THRESHOLD",
    "compose_red_team_verdict",
    "assert_evidence_in_drafts",
    "detect_council_split",
    "detect_judge_anchor_suspected",
]
