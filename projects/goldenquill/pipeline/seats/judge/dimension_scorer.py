"""pipeline.seats.judge.dimension_scorer — §9 R1 single-dimension predicate.

Pure-over-injected-seam predicate: given a tuple of section drafts, a
criterion (or subcriterion), and an :class:`LLMCallFn` callable,
:func:`score_dimension` builds a deterministic prompt, invokes the
callable, parses the JSON response, and returns a frozen
:class:`pipeline.seats.judge.types.CriterionScore`.

E-017 12th+ formal firing of the injected-callable seam: the LLM
provider binding lives in ``router.yaml`` ``tilth.judge`` (Google Gemini
2.5 Pro) and is wired to a real HTTPS provider at R3. R1 unit tests
inject deterministic fakes returning canned strings.

Threat model (R1):

- **In scope.** Empty drafts → ``ValueError``; LLM raises → propagates
  (NOT swallowed); JSON-fenced output → fences stripped before parse;
  unparseable LLM output → ``ValueError`` tagged
  ``F-JUDGE-SCORE-UNPARSEABLE``; out-of-bound score (>``max_points`` or
  <0) → ``ValueError`` tagged ``F-JUDGE-SCORE-OUT-OF-BOUND``;
  out-of-bound confidence (outside ``[0.0, 1.0]``) → ``ValueError``;
  extra fields in LLM JSON → ignored (no field-leakage attack surface).
- **Out of scope, deferred to R3.** Evidence-in-draft verification
  (``F-JUDGE-EVIDENCE-NOT-IN-DRAFT`` is a Logician POST-gate over
  ``CriterionScore.evidence_quote`` ∈ ``SectionDraftLike.body_text``);
  LLM provider binding; cross-family routing; rubric-library dispatch;
  SFR format emission; subprocess entry. The function is pure-over-
  injected-seam — no file I/O, no globals mutation, no import of any
  ``pipeline.providers.*`` module.

Score-bound discipline: a criterion's ``max_points`` is the upper
bound; subcriteria carry their own ``max_points`` (e.g. VAPG ``a.i`` has
max=10, parent ``a`` has max=30 across three subcriteria). Caller
chooses which level to score and passes the corresponding object;
:func:`score_dimension` polymorphic-dispatches over
``Union[RubricCriterion, RubricSubCriterion]`` via duck-typing on the
shared ``id`` / ``name`` / ``max_points`` / ``must_address`` /
``tiers`` fields.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Callable, Mapping, Union

from pipeline.seats.judge.types import (
    CriterionScore,
    F_JUDGE_SCORE_OUT_OF_BOUND,
    F_JUDGE_SCORE_UNPARSEABLE,
    LLMCallFn,
    RubricCriterion,
    RubricSubCriterion,
    SectionDraftLike,
)


ClockFn = Callable[[], datetime]


def _default_utc_now() -> datetime:
    return datetime.now(tz=timezone.utc)


# ---------------------------------------------------------------------------
# Prompt-token budget — Judge LLM call uses a moderate completion budget
# (the response is a small JSON object). Inline literal per V1 discipline.
# ---------------------------------------------------------------------------

_DEFAULT_MAX_TOKENS: int = 1024


# ---------------------------------------------------------------------------
# Prompt composition
# ---------------------------------------------------------------------------


def _format_must_address(items: tuple[str, ...]) -> str:
    if not items:
        return "(none)"
    return "\n".join(f"  - {item}" for item in items)


def _format_tiers(tiers: tuple[Mapping[str, Any], ...]) -> str:
    if not tiers:
        return "(none — score guidance via parent criterion)"
    lines: list[str] = []
    for tier in tiers:
        points = tier.get("points", "?")
        description = tier.get("description", "")
        lines.append(f"  - points={points}: {description}")
    return "\n".join(lines)


def _format_drafts(drafts: tuple[SectionDraftLike, ...]) -> str:
    blocks: list[str] = []
    for draft in drafts:
        blocks.append(
            f"### Section {draft.section_order}: {draft.section_name}\n\n"
            f"{draft.body_text}"
        )
    return "\n\n".join(blocks)


def _build_scoring_prompt(
    drafts: tuple[SectionDraftLike, ...],
    criterion: Union[RubricCriterion, RubricSubCriterion],
) -> str:
    """Compose the deterministic Judge scoring prompt.

    The prompt embeds (a) the criterion id+name+max_points, (b) the
    must_address checklist, (c) the scoring tiers, and (d) the section
    drafts under review. Output contract: a single JSON object with
    ``score`` (int), ``evidence_quote`` (str — verbatim substring of one
    section body), ``confidence`` (float in [0,1]), ``rationale`` (str).
    """
    return (
        "You are scoring a grant proposal section against a published "
        "rubric criterion. Respond with a single JSON object — no prose, "
        "no markdown fences.\n\n"
        f"## Criterion\n"
        f"- id: {criterion.id}\n"
        f"- name: {criterion.name}\n"
        f"- max_points: {criterion.max_points}\n\n"
        f"## Must-address checklist\n{_format_must_address(criterion.must_address)}\n\n"
        f"## Scoring tiers\n{_format_tiers(criterion.tiers)}\n\n"
        f"## Section drafts under review\n\n{_format_drafts(drafts)}\n\n"
        "## Required output JSON shape\n"
        '{"score": <int 0..max_points>, '
        '"evidence_quote": "<verbatim substring of one section body>", '
        '"confidence": <float 0.0..1.0>, '
        '"rationale": "<short prose, 1-2 sentences>"}\n'
    )


# ---------------------------------------------------------------------------
# Response parsing — JSON-fence-tolerant per Rule 4 Clean Output discipline
# ---------------------------------------------------------------------------


def _strip_json_fences(text: str) -> str:
    """Strip leading/trailing ```json fences if present.

    Matches Scribe / Editor pattern: LLMs frequently wrap JSON in
    Markdown fences despite explicit prompt instruction. The Four
    Autonomy Rules (Rule 4) require seats to clean output before
    handing to the next stage.
    """
    s = text.strip()
    if s.startswith("```"):
        # Drop the opening fence line — could be ```json or just ```.
        first_newline = s.find("\n")
        if first_newline != -1:
            s = s[first_newline + 1 :]
        else:
            # Single-line ```json{...}``` form — strip leading fence.
            s = s[3:]
            if s.startswith("json"):
                s = s[4:]
        # Drop the trailing fence.
        if s.rstrip().endswith("```"):
            s = s.rstrip()[:-3]
    return s.strip()


def _parse_llm_response(raw: str) -> Mapping[str, Any]:
    """Parse the Judge LLM's JSON response.

    Raises ``ValueError`` tagged ``F-JUDGE-SCORE-UNPARSEABLE`` on:
    non-JSON output, JSON whose top level is not an object, missing
    required fields (``score``/``evidence_quote``/``confidence``/
    ``rationale``), wrong-typed fields. Extra fields are silently
    ignored — defends against a malicious-prompt injection that adds
    e.g. ``"override_max": 999`` (no field elevation).
    """
    cleaned = _strip_json_fences(raw)
    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"{F_JUDGE_SCORE_UNPARSEABLE}: LLM response is not valid JSON: "
            f"{exc}"
        ) from exc
    if not isinstance(parsed, Mapping):
        raise ValueError(
            f"{F_JUDGE_SCORE_UNPARSEABLE}: LLM response top level must be "
            f"a JSON object; got {type(parsed).__name__}."
        )
    return parsed


def _require_response_int(parsed: Mapping[str, Any], key: str) -> int:
    value = parsed.get(key)
    # Reject bool: True/False are int subclasses but not a valid score.
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(
            f"{F_JUDGE_SCORE_UNPARSEABLE}: LLM response field {key!r} must "
            f"be an int; got {type(value).__name__} ({value!r})."
        )
    return value


def _require_response_str(parsed: Mapping[str, Any], key: str) -> str:
    value = parsed.get(key)
    if not isinstance(value, str):
        raise ValueError(
            f"{F_JUDGE_SCORE_UNPARSEABLE}: LLM response field {key!r} must "
            f"be a string; got {type(value).__name__}."
        )
    return value


def _require_response_float(parsed: Mapping[str, Any], key: str) -> float:
    value = parsed.get(key)
    if isinstance(value, bool):
        raise ValueError(
            f"{F_JUDGE_SCORE_UNPARSEABLE}: LLM response field {key!r} must "
            f"be a number; got bool ({value!r})."
        )
    if isinstance(value, (int, float)):
        return float(value)
    raise ValueError(
        f"{F_JUDGE_SCORE_UNPARSEABLE}: LLM response field {key!r} must be "
        f"a number; got {type(value).__name__} ({value!r})."
    )


# ---------------------------------------------------------------------------
# Public predicate
# ---------------------------------------------------------------------------


def score_dimension(
    section_drafts: tuple[SectionDraftLike, ...],
    criterion: Union[RubricCriterion, RubricSubCriterion],
    *,
    llm_call: LLMCallFn,
    clock: ClockFn = _default_utc_now,
    max_tokens: int = _DEFAULT_MAX_TOKENS,
) -> CriterionScore:
    """Score one dimension (criterion or subcriterion) of a rubric.

    Pure-over-injected-seam: builds a deterministic prompt, invokes
    ``llm_call``, parses the response, validates score / confidence
    bounds against the criterion ``max_points``, and returns a frozen
    :class:`CriterionScore`. Does NOT verify ``evidence_quote`` is
    actually a substring of any draft — that is R3's POST-gate scope.

    Raises:
        ValueError: empty section_drafts; unparseable response (tagged
            ``F-JUDGE-SCORE-UNPARSEABLE``); out-of-bound score (tagged
            ``F-JUDGE-SCORE-OUT-OF-BOUND``); out-of-bound confidence.
        Exception: any exception raised by ``llm_call`` propagates
            unchanged (timeouts, transport errors, provider rejections —
            not swallowed).

    The ``clock`` callable is currently unused inside this function but
    is accepted to match the seat-wide injection convention; R3
    orchestration adds a ``scored_at_utc`` timestamp on
    :class:`pipeline.seats.judge.types.JudgeOutput` via the same clock
    seam.
    """
    if not section_drafts:
        raise ValueError(
            "score_dimension: section_drafts must be non-empty; cannot "
            "score against zero drafts."
        )

    prompt = _build_scoring_prompt(section_drafts, criterion)
    raw = llm_call(prompt=prompt, max_tokens=max_tokens)
    parsed = _parse_llm_response(raw)

    score = _require_response_int(parsed, "score")
    evidence_quote = _require_response_str(parsed, "evidence_quote")
    confidence = _require_response_float(parsed, "confidence")
    rationale = _require_response_str(parsed, "rationale")

    if score < 0 or score > criterion.max_points:
        raise ValueError(
            f"{F_JUDGE_SCORE_OUT_OF_BOUND}: criterion {criterion.id!r} "
            f"max_points={criterion.max_points}; LLM returned "
            f"score={score!r}."
        )
    # Confidence bound: catch the 1.5 / -0.1 case before CriterionScore
    # __post_init__ does (the failure code is more specific than the
    # generic dataclass message).
    if not (0.0 <= confidence <= 1.0):
        raise ValueError(
            f"{F_JUDGE_SCORE_UNPARSEABLE}: LLM confidence "
            f"{confidence!r} out of range [0.0, 1.0]."
        )

    # Touch the clock for symmetry with the rest of the seat (and so
    # tests that inject a tracking clock can verify it was invoked).
    clock()

    return CriterionScore(
        criterion_id=criterion.id,
        score=score,
        evidence_quote=evidence_quote,
        confidence=confidence,
        rationale=rationale,
    )


__all__ = [
    "ClockFn",
    "score_dimension",
]
