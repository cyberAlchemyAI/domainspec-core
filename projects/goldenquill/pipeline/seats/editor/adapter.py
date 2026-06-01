"""pipeline.seats.editor.adapter — §8 Editor Round 1 adapter entry.

Wraps :file:`skills/editor/SKILL.md` per parent spec card §4 Option A
(adapter pattern, v0.1.0). The adapter does NOT reimplement the skill's
clarity-pass prompt — production wires
:func:`invoke_editor_adapter` to a clawdis-subprocess
:class:`SkillLauncher` that runs SKILL.md verbatim. Tests inject deterministic
fakes per E-017 pattern.

Threat-model boundaries (per spec card §11 hardenings):

- **Trusted-operator envelope (§3.11 v5).** Caller controls
  ``EditorInput`` construction; the adapter does not validate the
  envelope's source — that is the seat layer's PRE-gate responsibility.
- **Skill-subprocess trust boundary.** The skill itself runs out-of-process
  (clawdis) and is the LLM-call layer; the adapter only orchestrates the
  envelope transform + dispatch + parse + validate cycle. Anything the
  skill emits is treated as untrusted JSON until validated.
- **E-027 non-applicability.** Editor's production binding per
  ``router.yaml`` is Meta (``groq/llama-3.3-70b-versatile``) primary +
  OpenAI (``openai/gpt-4o-mini``) fallback — neither is Qwen3-32B, so the
  ``<think>``-block degenerate-repetition shape that triggered E-027 in
  the Vault Batch 3 dispatch does not apply here. The adapter still raises
  ``F_EDITOR_SKILL_OUTPUT_MALFORMED_JSON`` on any non-JSON response;
  explicit retry-with-clarification (parent spec §9 mitigation) is R2
  scope.
- **E-028 non-applicability.** The adapter dispatches to the skill, NOT
  to a code-review committee. Payload-size ceiling is between skill and
  provider, not adapter and reviewer; transient 503 retries are a
  ``SkillLauncher`` implementation concern, not the adapter's.
- **Retry-with-clarification (R2 §3.1).** On malformed skill output —
  JSON parse failure, structural shape violation, or 2-3 replacement
  invariant violation — :func:`invoke_editor_adapter` re-invokes the
  skill once with a ``clarification_suffix`` appended to the stdin
  payload describing the parse failure and asking the skill to re-emit
  clean JSON. Bounded to **1 retry** (N=2 total attempts) per
  E-028 transport-discipline precedent. Hard launcher failures
  (:class:`EditorSkillTimeout`, :class:`EditorSkillSubprocessFail`)
  are NOT retried — those are launcher-layer concerns surfaced to the
  cascade by the seat. The retry behavior is opt-out via the
  ``enable_retry_with_clarification`` keyword (defaults ``True``); R1
  callers wanting strict single-attempt behavior pass ``False``.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Final, Literal, Mapping, Protocol, runtime_checkable

from pipeline.seats.editor.types import (
    EditorGap,
    EditorInput,
    EditorOutput,
    EditorSkillInvocation,
    FlaggedTerm,
    Miscategorization,
    ReadabilityFeedback,
    ReplacementOption,
    TaxonomyCheck,
    ToneFeedback,
    _DIALECT_VALID,
    _ISSUE_TYPE_VALID,
    _REPLACEMENT_LABEL_VALID,
    _SEVERITY_VALID,
)


# ---------------------------------------------------------------------------
# Failure-code string constants (§4.2.1 POST-gate slot allocation per spec
# card §4 decision 10 + OQ-3 recommendation b)
# ---------------------------------------------------------------------------

F_EDITOR_OUTPUT_SHAPE: Final[str] = "F-EDITOR-OUTPUT-SHAPE"
F_EDITOR_REWROTE_INSTEAD_OF_FLAGGED: Final[str] = "F-EDITOR-REWROTE-INSTEAD-OF-FLAGGED"
F_EDITOR_SINGLE_REPLACEMENT: Final[str] = "F-EDITOR-SINGLE-REPLACEMENT"
F_EDITOR_SKILL_SUBPROCESS_FAIL: Final[str] = "F-EDITOR-SKILL-SUBPROCESS-FAIL"
F_EDITOR_SKILL_OUTPUT_MALFORMED_JSON: Final[str] = (
    "F-EDITOR-SKILL-OUTPUT-MALFORMED-JSON"
)
F_EDITOR_SKILL_TIMEOUT: Final[str] = "F-EDITOR-SKILL-TIMEOUT"


# ---------------------------------------------------------------------------
# Exceptions — adapter raises one of these per F-EDITOR-* code; seat.py
# catches and emits structured stderr + exit 2 (matching Scribe R3 pattern).
# ---------------------------------------------------------------------------


class EditorOutputShapeError(ValueError):
    """``F-EDITOR-OUTPUT-SHAPE`` — structural violation of EditorOutput."""

    failure_code: str = F_EDITOR_OUTPUT_SHAPE


class EditorRewroteInsteadOfFlaggedError(ValueError):
    """``F-EDITOR-REWROTE-INSTEAD-OF-FLAGGED`` — Law 4 enforcement.

    Skill attempted whole-draft rewrite rather than point-fix; threshold
    is 40% body-coverage (inline-literal per V1 rebind-resistance).
    """

    failure_code: str = F_EDITOR_REWROTE_INSTEAD_OF_FLAGGED


class EditorSingleReplacementError(ValueError):
    """``F-EDITOR-SINGLE-REPLACEMENT`` — 2-3 invariant violation."""

    failure_code: str = F_EDITOR_SINGLE_REPLACEMENT


class EditorSkillSubprocessFail(RuntimeError):
    """``F-EDITOR-SKILL-SUBPROCESS-FAIL`` — launcher raised non-timeout error."""

    failure_code: str = F_EDITOR_SKILL_SUBPROCESS_FAIL


class EditorSkillOutputMalformedJson(ValueError):
    """``F-EDITOR-SKILL-OUTPUT-MALFORMED-JSON`` — parse failure."""

    failure_code: str = F_EDITOR_SKILL_OUTPUT_MALFORMED_JSON


class EditorSkillTimeout(TimeoutError):
    """``F-EDITOR-SKILL-TIMEOUT`` — launcher exceeded 180_000 ms ceiling."""

    failure_code: str = F_EDITOR_SKILL_TIMEOUT


# ---------------------------------------------------------------------------
# Skill-subprocess result shape + SkillLauncher Protocol (E-017 seam)
# ---------------------------------------------------------------------------


class SkillSubprocessResult:
    """Lightweight result wrapper from a SkillLauncher invocation.

    Not a frozen dataclass — production launcher implementations may
    populate this from a dynamic clawdis stdout buffer, and we keep the
    shape Open for forward compatibility (e.g., adding stderr / latency
    fields at R2). Equality is identity-based (default).
    """

    __slots__ = ("stdout", "exit_code")

    def __init__(self, *, stdout: str, exit_code: int) -> None:
        if not isinstance(stdout, str):
            raise TypeError("SkillSubprocessResult.stdout must be str")
        if not isinstance(exit_code, int) or isinstance(exit_code, bool):
            raise TypeError("SkillSubprocessResult.exit_code must be int")
        self.stdout = stdout
        self.exit_code = exit_code


@runtime_checkable
class SkillLauncher(Protocol):
    """E-017 injected callable seam — 12th firing.

    Production wires a clawdis-subprocess invoker; tests inject
    deterministic fakes. ``timeout_ms`` is enforced by the launcher
    implementation (the adapter passes the inline-literal 180_000 ms).
    Launcher MUST raise :class:`TimeoutError` (or subclass) on timeout
    so the adapter can translate it into ``F_EDITOR_SKILL_TIMEOUT``.
    """

    def __call__(
        self,
        *,
        skill_slug: Literal["editor"],
        stdin_payload: bytes,
        timeout_ms: int,
    ) -> SkillSubprocessResult: ...


# ---------------------------------------------------------------------------
# Module-private helpers — strip_fences + extract_json lifted verbatim from
# pipeline/orchestrator/seats/editor.py:139-156 (Josh's 3-grant-proven
# parse discipline; spec card §4 decision 7).
# ---------------------------------------------------------------------------


def _strip_fences(s: str) -> str:
    """Strip a leading/trailing ``\\u0060\\u0060\\u0060`` markdown code fence."""
    s = s.strip()
    if s.startswith("```"):
        first_nl = s.find("\n")
        s = s[first_nl + 1:] if first_nl > 0 else s[3:]
        if s.endswith("```"):
            s = s[:-3]
    return s.strip()


def _extract_json_object(text: str) -> Mapping[str, Any]:
    """Return the first JSON object embedded in ``text``.

    Strips fences first, then locates the first ``{`` and uses
    :class:`json.JSONDecoder.raw_decode` to consume one object. Raises
    :class:`EditorSkillOutputMalformedJson` on any failure.
    """
    t = _strip_fences(text)
    if not t:
        raise EditorSkillOutputMalformedJson(
            f"{F_EDITOR_SKILL_OUTPUT_MALFORMED_JSON}: empty stdout"
        )
    start = t.find("{")
    if start < 0:
        raise EditorSkillOutputMalformedJson(
            f"{F_EDITOR_SKILL_OUTPUT_MALFORMED_JSON}: no JSON object found "
            f"in skill output"
        )
    decoder = json.JSONDecoder()
    try:
        obj, _ = decoder.raw_decode(t[start:])
    except json.JSONDecodeError as exc:
        raise EditorSkillOutputMalformedJson(
            f"{F_EDITOR_SKILL_OUTPUT_MALFORMED_JSON}: JSON decode failed: {exc}"
        ) from exc
    if not isinstance(obj, dict):
        raise EditorSkillOutputMalformedJson(
            f"{F_EDITOR_SKILL_OUTPUT_MALFORMED_JSON}: top-level JSON must be "
            f"object; got {type(obj).__name__}"
        )
    return obj


def parse_skill_output(stdout: str) -> Mapping[str, Any]:
    """Public alias for :func:`_extract_json_object` — pure, testable alone.

    Per spec card §3 ``__all__``: this is a public surface symbol so
    fixtures can exercise the parse path without booting the full adapter.
    Returns an opaque mapping; ``_map_skill_json_to_editor_output`` is the
    layer that walks the structure into typed shapes.
    """
    return _extract_json_object(stdout)


# ---------------------------------------------------------------------------
# Module-private helpers — markdown render + skill JSON → EditorOutput
# ---------------------------------------------------------------------------


def _render_section_drafts_to_markdown(
    section_drafts: tuple[Mapping[str, object], ...],
) -> str:
    """Render section-draft dicts to a single markdown string.

    Sections are emitted in :attr:`section_order` order (lowest first).
    Format: ``## <section_name>\\n\\n<body_text>\\n``. Stable so the skill
    receives the same input under the same draft regardless of dict
    insertion order.
    """
    ordered = sorted(
        section_drafts,
        key=lambda sd: int(sd["section_order"]),  # type: ignore[arg-type]
    )
    parts: list[str] = []
    for sd in ordered:
        name = str(sd["section_name"])
        body = str(sd["body_text"])
        parts.append(f"## {name}\n\n{body}")
    return "\n\n".join(parts) + "\n"


def _default_utc_now() -> datetime:
    """Wall-clock seam for production; tests inject deterministic clocks."""
    return datetime.now(tz=timezone.utc)


def _require_str_field(
    obj: Mapping[str, Any], path: str, *, allow_empty: bool = False
) -> str:
    """Pull a required string field from ``obj`` at dotted ``path``.

    Raises :class:`EditorOutputShapeError` if missing or wrong type.
    """
    keys = path.split(".")
    cur: Any = obj
    for k in keys:
        if not isinstance(cur, Mapping) or k not in cur:
            raise EditorOutputShapeError(
                f"{F_EDITOR_OUTPUT_SHAPE}: missing required field {path!r}"
            )
        cur = cur[k]
    if not isinstance(cur, str):
        raise EditorOutputShapeError(
            f"{F_EDITOR_OUTPUT_SHAPE}: field {path!r} must be string; got "
            f"{type(cur).__name__}"
        )
    if not allow_empty and not cur.strip():
        raise EditorOutputShapeError(
            f"{F_EDITOR_OUTPUT_SHAPE}: field {path!r} must be non-empty"
        )
    return cur


def _require_int_field(obj: Mapping[str, Any], path: str) -> int:
    keys = path.split(".")
    cur: Any = obj
    for k in keys:
        if not isinstance(cur, Mapping) or k not in cur:
            raise EditorOutputShapeError(
                f"{F_EDITOR_OUTPUT_SHAPE}: missing required field {path!r}"
            )
        cur = cur[k]
    if isinstance(cur, bool) or not isinstance(cur, int):
        raise EditorOutputShapeError(
            f"{F_EDITOR_OUTPUT_SHAPE}: field {path!r} must be int; got "
            f"{type(cur).__name__}"
        )
    return cur


def _require_list_field(obj: Mapping[str, Any], key: str) -> list[Any]:
    if key not in obj:
        raise EditorOutputShapeError(
            f"{F_EDITOR_OUTPUT_SHAPE}: missing required list field {key!r}"
        )
    value = obj[key]
    if not isinstance(value, list):
        raise EditorOutputShapeError(
            f"{F_EDITOR_OUTPUT_SHAPE}: field {key!r} must be list; got "
            f"{type(value).__name__}"
        )
    return value


def _map_replacement_options(
    raw_options: list[Any],
) -> tuple[ReplacementOption, ...]:
    """Map raw skill ``options[]`` array into a tuple of ReplacementOption.

    Permissive on count — the validator (``validate_editor_output_shape``)
    enforces the 2-3 invariant via ``F_EDITOR_SINGLE_REPLACEMENT``.
    """
    out: list[ReplacementOption] = []
    for i, raw in enumerate(raw_options):
        if not isinstance(raw, Mapping):
            raise EditorOutputShapeError(
                f"{F_EDITOR_OUTPUT_SHAPE}: options[{i}] must be object; got "
                f"{type(raw).__name__}"
            )
        label = raw.get("label")
        text = raw.get("text")
        note = raw.get("note", "")
        if label not in _REPLACEMENT_LABEL_VALID:
            raise EditorOutputShapeError(
                f"{F_EDITOR_OUTPUT_SHAPE}: options[{i}].label must be one of "
                f"{sorted(_REPLACEMENT_LABEL_VALID)}; got {label!r}"
            )
        if not isinstance(text, str) or not text.strip():
            raise EditorOutputShapeError(
                f"{F_EDITOR_OUTPUT_SHAPE}: options[{i}].text must be "
                f"non-empty string"
            )
        if not isinstance(note, str):
            raise EditorOutputShapeError(
                f"{F_EDITOR_OUTPUT_SHAPE}: options[{i}].note must be string"
            )
        out.append(ReplacementOption(label=label, text=text, note=note))
    return tuple(out)


def _map_flagged_term(raw: Mapping[str, Any], index: int) -> FlaggedTerm:
    """Map one ``suggestions[]`` skill entry into a :class:`FlaggedTerm`."""
    issue_type = raw.get("issue_type")
    if issue_type not in _ISSUE_TYPE_VALID:
        raise EditorOutputShapeError(
            f"{F_EDITOR_OUTPUT_SHAPE}: suggestions[{index}].issue_type must "
            f"be one of {sorted(_ISSUE_TYPE_VALID)}; got {issue_type!r}"
        )
    severity = raw.get("severity")
    if severity not in _SEVERITY_VALID:
        raise EditorOutputShapeError(
            f"{F_EDITOR_OUTPUT_SHAPE}: suggestions[{index}].severity must "
            f"be one of {sorted(_SEVERITY_VALID)}; got {severity!r}"
        )
    section_ref = raw.get("section")
    if not isinstance(section_ref, str) or not section_ref.strip():
        raise EditorOutputShapeError(
            f"{F_EDITOR_OUTPUT_SHAPE}: suggestions[{index}].section must "
            f"be non-empty string"
        )
    excerpt = raw.get("original")
    if not isinstance(excerpt, str) or not excerpt.strip():
        raise EditorOutputShapeError(
            f"{F_EDITOR_OUTPUT_SHAPE}: suggestions[{index}].original must "
            f"be non-empty string"
        )
    why = raw.get("issue")
    if not isinstance(why, str) or not why.strip():
        raise EditorOutputShapeError(
            f"{F_EDITOR_OUTPUT_SHAPE}: suggestions[{index}].issue must be "
            f"non-empty string"
        )
    options_raw = raw.get("options")
    if not isinstance(options_raw, list):
        raise EditorOutputShapeError(
            f"{F_EDITOR_OUTPUT_SHAPE}: suggestions[{index}].options must be list"
        )
    options = _map_replacement_options(options_raw)
    rubric_connection = raw.get("rubric_connection", "")
    if not isinstance(rubric_connection, str):
        raise EditorOutputShapeError(
            f"{F_EDITOR_OUTPUT_SHAPE}: suggestions[{index}].rubric_connection "
            f"must be string"
        )
    return FlaggedTerm(
        section_ref=section_ref,
        issue_type=issue_type,
        severity=severity,
        excerpt=excerpt,
        why_it_hurts=why,
        replacement_options=options,
        rubric_connection=rubric_connection,
    )


def _map_taxonomy_check(raw: Mapping[str, Any]) -> TaxonomyCheck:
    """Map ``taxonomy_check`` block into typed shape.

    Empty/missing block → empty TaxonomyCheck (skill may legitimately
    return no goal/output/outcome/objective sort if the section doesn't
    contain any of the categories).
    """
    if not isinstance(raw, Mapping):
        raise EditorOutputShapeError(
            f"{F_EDITOR_OUTPUT_SHAPE}: taxonomy_check must be object"
        )

    def _strs(key: str) -> tuple[str, ...]:
        value = raw.get(key, [])
        if not isinstance(value, list):
            raise EditorOutputShapeError(
                f"{F_EDITOR_OUTPUT_SHAPE}: taxonomy_check.{key} must be list"
            )
        result: list[str] = []
        for i, entry in enumerate(value):
            if not isinstance(entry, str) or not entry.strip():
                raise EditorOutputShapeError(
                    f"{F_EDITOR_OUTPUT_SHAPE}: taxonomy_check.{key}[{i}] must "
                    f"be non-empty string"
                )
            result.append(entry)
        return tuple(result)

    misc_raw = raw.get("miscategorizations", [])
    if not isinstance(misc_raw, list):
        raise EditorOutputShapeError(
            f"{F_EDITOR_OUTPUT_SHAPE}: taxonomy_check.miscategorizations "
            f"must be list"
        )
    miscategorizations: list[Miscategorization] = []
    for i, entry in enumerate(misc_raw):
        if not isinstance(entry, Mapping):
            raise EditorOutputShapeError(
                f"{F_EDITOR_OUTPUT_SHAPE}: "
                f"taxonomy_check.miscategorizations[{i}] must be object"
            )
        miscategorizations.append(
            Miscategorization(
                excerpt=_require_str_field(entry, "excerpt"),
                stated_as=_require_str_field(entry, "stated_as"),
                should_be=_require_str_field(entry, "should_be"),
                why=_require_str_field(entry, "why"),
            )
        )

    return TaxonomyCheck(
        goals_identified=_strs("goals_identified"),
        outputs_identified=_strs("outputs_identified"),
        outcomes_identified=_strs("outcomes_identified"),
        objectives_identified=_strs("objectives_identified"),
        miscategorizations=tuple(miscategorizations),
    )


def _map_readability(raw: Mapping[str, Any]) -> ReadabilityFeedback:
    """Map ``readability`` block into ReadabilityFeedback.

    SKILL.md uses ``estimated_grade_level`` (int); legacy schema uses
    ``score_10`` (int 0..10). Adapter prefers explicit ``score_10`` if
    supplied, else derives from grade level: 10..12 → 8 (good), <10 → 6
    (rough), >12 → 5 (too dense).
    """
    if not isinstance(raw, Mapping):
        raise EditorOutputShapeError(
            f"{F_EDITOR_OUTPUT_SHAPE}: readability must be object"
        )
    if "score_10" in raw:
        score_10 = _require_int_field(raw, "score_10")
    elif "estimated_grade_level" in raw:
        grade = _require_int_field(raw, "estimated_grade_level")
        if 10 <= grade <= 12:
            score_10 = 8
        elif grade < 10:
            score_10 = 6
        else:
            score_10 = 5
    else:
        raise EditorOutputShapeError(
            f"{F_EDITOR_OUTPUT_SHAPE}: readability missing both score_10 and "
            f"estimated_grade_level"
        )
    grade_level = raw.get("grade_level_estimate")
    if grade_level is None:
        # Synthesize a stringified grade-level estimate when only the
        # numeric ``estimated_grade_level`` is present.
        if "estimated_grade_level" in raw:
            grade_level = f"grade {raw['estimated_grade_level']}"
        else:
            raise EditorOutputShapeError(
                f"{F_EDITOR_OUTPUT_SHAPE}: readability.grade_level_estimate "
                f"required when estimated_grade_level absent"
            )
    if not isinstance(grade_level, str) or not grade_level.strip():
        raise EditorOutputShapeError(
            f"{F_EDITOR_OUTPUT_SHAPE}: readability.grade_level_estimate must "
            f"be non-empty string"
        )
    verdict = raw.get("verdict") or raw.get("overall")
    if not isinstance(verdict, str) or not verdict.strip():
        raise EditorOutputShapeError(
            f"{F_EDITOR_OUTPUT_SHAPE}: readability.verdict (or .overall) must "
            f"be non-empty string"
        )
    return ReadabilityFeedback(
        score_10=score_10,
        grade_level_estimate=grade_level,
        verdict=verdict,
    )


def _map_tone_feedback(raw: Mapping[str, Any]) -> ToneFeedback:
    readability = _map_readability(raw.get("readability", {}))
    key_message = raw.get("readability", {}).get("key_message", "")
    if not isinstance(key_message, str) or not key_message.strip():
        raise EditorOutputShapeError(
            f"{F_EDITOR_OUTPUT_SHAPE}: readability.key_message must be "
            f"non-empty string"
        )
    fatigue = raw.get("readability", {}).get("reviewer_fatigue_sections", [])
    if not isinstance(fatigue, list):
        raise EditorOutputShapeError(
            f"{F_EDITOR_OUTPUT_SHAPE}: readability.reviewer_fatigue_sections "
            f"must be list"
        )
    fatigue_tup: list[str] = []
    for i, entry in enumerate(fatigue):
        if not isinstance(entry, str) or not entry.strip():
            raise EditorOutputShapeError(
                f"{F_EDITOR_OUTPUT_SHAPE}: "
                f"readability.reviewer_fatigue_sections[{i}] must be "
                f"non-empty string"
            )
        fatigue_tup.append(entry)
    return ToneFeedback(
        overall_readability=readability,
        key_message=key_message,
        reviewer_fatigue_sections=tuple(fatigue_tup),
    )


def _map_gaps(raw_gaps: list[Any]) -> tuple[EditorGap, ...]:
    out: list[EditorGap] = []
    for i, entry in enumerate(raw_gaps):
        if not isinstance(entry, Mapping):
            raise EditorOutputShapeError(
                f"{F_EDITOR_OUTPUT_SHAPE}: gaps[{i}] must be object"
            )
        section_ref = entry.get("section")
        if not isinstance(section_ref, str) or not section_ref.strip():
            raise EditorOutputShapeError(
                f"{F_EDITOR_OUTPUT_SHAPE}: gaps[{i}].section must be non-empty"
            )
        issue = entry.get("issue")
        if not isinstance(issue, str) or not issue.strip():
            raise EditorOutputShapeError(
                f"{F_EDITOR_OUTPUT_SHAPE}: gaps[{i}].issue must be non-empty"
            )
        action_needed = entry.get("action_needed")
        if not isinstance(action_needed, str) or not action_needed.strip():
            raise EditorOutputShapeError(
                f"{F_EDITOR_OUTPUT_SHAPE}: gaps[{i}].action_needed must be "
                f"non-empty"
            )
        out.append(
            EditorGap(
                section_ref=section_ref,
                issue=issue,
                action_needed=action_needed,
            )
        )
    return tuple(out)


def _map_skill_json_to_editor_output(skill_json: Mapping[str, Any]) -> EditorOutput:
    """Map raw skill JSON into a typed :class:`EditorOutput`."""
    suggestions_raw = _require_list_field(skill_json, "suggestions")
    flagged_terms = tuple(
        _map_flagged_term(entry, i) if isinstance(entry, Mapping) else _bad_suggestion(i, entry)
        for i, entry in enumerate(suggestions_raw)
    )
    taxonomy_raw = skill_json.get("taxonomy_check", {})
    taxonomy = _map_taxonomy_check(taxonomy_raw)
    tone = _map_tone_feedback(skill_json)
    quick_wins_raw = _require_list_field(skill_json, "quick_wins")
    quick_wins: list[str] = []
    for i, qw in enumerate(quick_wins_raw):
        if not isinstance(qw, str) or not qw.strip():
            raise EditorOutputShapeError(
                f"{F_EDITOR_OUTPUT_SHAPE}: quick_wins[{i}] must be non-empty string"
            )
        quick_wins.append(qw)
    terms_raw = _require_list_field(skill_json, "terms_to_verify")
    terms: list[str] = []
    for i, t in enumerate(terms_raw):
        if not isinstance(t, str) or not t.strip():
            raise EditorOutputShapeError(
                f"{F_EDITOR_OUTPUT_SHAPE}: terms_to_verify[{i}] must be "
                f"non-empty string"
            )
        terms.append(t)
    gaps_raw = skill_json.get("gaps", [])
    if not isinstance(gaps_raw, list):
        raise EditorOutputShapeError(
            f"{F_EDITOR_OUTPUT_SHAPE}: gaps must be list"
        )
    gaps = _map_gaps(gaps_raw)
    return EditorOutput(
        flagged_terms=flagged_terms,
        taxonomy_check=taxonomy,
        tone_feedback=tone,
        quick_wins=tuple(quick_wins),
        terms_to_verify=tuple(terms),
        gaps=gaps,
    )


def _bad_suggestion(index: int, entry: object) -> FlaggedTerm:
    raise EditorOutputShapeError(
        f"{F_EDITOR_OUTPUT_SHAPE}: suggestions[{index}] must be object; got "
        f"{type(entry).__name__}"
    )


# ---------------------------------------------------------------------------
# Validator — POST-gate surface for §4.2.1 F-EDITOR-* slots
# ---------------------------------------------------------------------------


_REWRITE_BODY_COVERAGE_THRESHOLD: Final[float] = 0.40


# ---------------------------------------------------------------------------
# R2 retry-with-clarification (§3.1) — bounded N=1 retry on malformed output
# ---------------------------------------------------------------------------

# Inline-literal retry ceiling — V1 rebind-resistance (matches E-028
# transport-budget discipline of one retry per call site). The skill
# subprocess is given exactly one chance to recover before the adapter
# escalates the failure to its caller (seat.py → cascade).
_RETRY_WITH_CLARIFICATION_MAX_ATTEMPTS: Final[int] = 2

# Clarification suffix appended to the second-attempt stdin payload as a
# top-level key. Keeps the original envelope intact so the skill prompt's
# parse path sees the same draft / RFA / dialect surface; the suffix is
# additive feedback the skill's system prompt is invited (not required)
# to honor.
_RETRYABLE_FAILURE_CODES: Final[frozenset[str]] = frozenset(
    {
        F_EDITOR_SKILL_OUTPUT_MALFORMED_JSON,
        F_EDITOR_OUTPUT_SHAPE,
        F_EDITOR_SINGLE_REPLACEMENT,
    }
)


def _build_clarification_suffix(
    *, first_failure_code: str, first_failure_message: str
) -> str:
    """Compose the human-readable clarification block for the retry payload.

    Sanitized output: includes the F-code and a one-line failure summary
    truncated to 256 characters. No stack traces, no exception class
    fingerprints — same fingerprint-leak discipline as Scribe R3 seat.
    """
    summary = first_failure_message.splitlines()[0] if first_failure_message else ""
    if len(summary) > 256:
        summary = summary[:253] + "..."
    return (
        f"Your previous response failed validation: {first_failure_code}. "
        f"Reason: {summary} "
        f"Please re-emit a single JSON object that matches the schema in "
        f"skills/editor/SKILL.md lines 194-241. Every suggestion must carry "
        f"2-3 labeled replacement options. Emit JSON only — no fences, no "
        f"prose, no commentary."
    )


def validate_editor_output_shape(
    output: EditorOutput,
    *,
    source_section_drafts: tuple[Mapping[str, object], ...],
) -> None:
    """Raise on any §4.2.1 POST-gate F-EDITOR-* code violation.

    Invariants enforced (per spec card §4 decisions 5-6 + §10):

    1. ``F_EDITOR_SINGLE_REPLACEMENT`` — every FlaggedTerm has 2-3
       replacement options.
    2. ``F_EDITOR_REWROTE_INSTEAD_OF_FLAGGED`` — collective replacement
       text length across all FlaggedTerms must not exceed 40% of the
       source body length (skill should point-fix, not rewrite).
    3. ``F_EDITOR_OUTPUT_SHAPE`` — readability score in 0..10 (already
       enforced at ReadabilityFeedback.__post_init__ but re-checked here
       for defense-in-depth).

    Source-body length is summed across all section drafts; threshold is
    inline-literal at 40% per V1 rebind-resistance.
    """
    if not isinstance(output, EditorOutput):
        raise EditorOutputShapeError(
            f"{F_EDITOR_OUTPUT_SHAPE}: output must be EditorOutput instance; "
            f"got {type(output).__name__}"
        )

    # Invariant 1: 2-3 replacement options per FlaggedTerm
    for i, term in enumerate(output.flagged_terms):
        n = len(term.replacement_options)
        if not (2 <= n <= 3):
            raise EditorSingleReplacementError(
                f"{F_EDITOR_SINGLE_REPLACEMENT}: flagged_terms[{i}] has "
                f"{n} replacement options; expected 2-3 (section_ref="
                f"{term.section_ref!r})"
            )

    # Invariant 2: rewrite-detection — sum text across all replacement
    # options and compare to source body length.
    source_body_len = sum(
        len(str(sd.get("body_text", "")))
        for sd in source_section_drafts
    )
    if source_body_len > 0:
        replacement_total = 0
        for term in output.flagged_terms:
            for opt in term.replacement_options:
                replacement_total += len(opt.text)
        if replacement_total > int(_REWRITE_BODY_COVERAGE_THRESHOLD * source_body_len):
            raise EditorRewroteInsteadOfFlaggedError(
                f"{F_EDITOR_REWROTE_INSTEAD_OF_FLAGGED}: replacement text "
                f"length {replacement_total} exceeds 40% of source body "
                f"length {source_body_len} — skill attempted whole-draft "
                f"rewrite"
            )

    # Invariant 3: defense-in-depth on readability score
    score = output.tone_feedback.overall_readability.score_10
    if not (0 <= score <= 10):
        raise EditorOutputShapeError(
            f"{F_EDITOR_OUTPUT_SHAPE}: tone_feedback.overall_readability."
            f"score_10 must be in 0..10; got {score!r}"
        )


# ---------------------------------------------------------------------------
# Public adapter entry — invoke_editor_adapter
# ---------------------------------------------------------------------------


# Inline-literal timeout — V1 rebind-resistance (§7.15 §6.13 precedent;
# matches seat_runner.py §4.4 Editor 180_000 ms).
def _build_base_payload(input_: EditorInput, *, clock) -> bytes:
    """Render the input to canonical UTF-8 JSON bytes for the skill stdin.

    Pure (no I/O); the caller-supplied ``clock`` is the only seam.
    Output is sort-keyed + comma/colon-tight (no whitespace) for
    deterministic byte-level equivalence in tests.
    """
    draft_md = _render_section_drafts_to_markdown(input_.section_drafts)
    invocation = EditorSkillInvocation(
        draft_markdown=draft_md,
        rfa_excerpt=input_.rfa_excerpt[:4000],
        dialect=input_.dialect,
        session_id=input_.session_id,
        org_slug=input_.org_slug,
        invocation_at_utc=clock(),
    )
    payload_dict = {
        "draft_markdown": invocation.draft_markdown,
        "rfa_excerpt": invocation.rfa_excerpt,
        "dialect": invocation.dialect,
        "session_id": invocation.session_id,
        "org_slug": invocation.org_slug,
        "invocation_at_utc": invocation.invocation_at_utc.isoformat(),
    }
    return json.dumps(
        payload_dict, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def _build_clarification_payload(
    base_payload: bytes,
    *,
    first_failure_code: str,
    first_failure_message: str,
) -> bytes:
    """Re-emit the stdin payload with a top-level ``clarification`` key.

    Pure transform: decodes the base payload, inserts the clarification
    block, re-emits as canonical UTF-8 JSON. Preserves all original
    fields verbatim — the skill's system prompt parses the same envelope
    keys and the additional ``clarification`` field is additive feedback.
    """
    decoded = json.loads(base_payload.decode("utf-8"))
    if not isinstance(decoded, dict):
        # Defense-in-depth — _build_base_payload always emits an object,
        # but if a caller hands us non-object bytes, surface as malformed.
        raise EditorSkillOutputMalformedJson(
            f"{F_EDITOR_SKILL_OUTPUT_MALFORMED_JSON}: base_payload is not "
            f"a JSON object"
        )
    decoded["clarification"] = _build_clarification_suffix(
        first_failure_code=first_failure_code,
        first_failure_message=first_failure_message,
    )
    decoded["retry_attempt"] = 2
    return json.dumps(
        decoded, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def _dispatch_skill_once(
    *,
    skill_launcher: SkillLauncher,
    stdin_payload: bytes,
) -> SkillSubprocessResult:
    """Single launcher dispatch with inline-literal timeout + error mapping.

    Maps :class:`TimeoutError` → :class:`EditorSkillTimeout`; any other
    launcher exception → :class:`EditorSkillSubprocessFail`. Hard
    launcher failures are NOT retried — both classes propagate up to
    :func:`invoke_editor_adapter` (and onward to seat.py / cascade).
    """
    try:
        skill_result = skill_launcher(
            skill_slug="editor",
            stdin_payload=stdin_payload,
            timeout_ms=180_000,
        )
    except TimeoutError as exc:
        raise EditorSkillTimeout(
            f"{F_EDITOR_SKILL_TIMEOUT}: skill launcher exceeded 180_000 ms"
        ) from exc
    except Exception as exc:
        raise EditorSkillSubprocessFail(
            f"{F_EDITOR_SKILL_SUBPROCESS_FAIL}: launcher raised "
            f"{type(exc).__name__}"
        ) from exc
    if not isinstance(skill_result, SkillSubprocessResult):
        raise EditorSkillSubprocessFail(
            f"{F_EDITOR_SKILL_SUBPROCESS_FAIL}: launcher returned "
            f"{type(skill_result).__name__}; expected SkillSubprocessResult"
        )
    return skill_result


def _parse_map_validate(
    skill_result: SkillSubprocessResult,
    *,
    source_section_drafts: tuple[Mapping[str, object], ...],
) -> EditorOutput:
    """Parse skill stdout → map → validate POST-gate invariants.

    Any of the three steps may raise an F-EDITOR-* exception. The caller
    decides whether to retry-with-clarification or escalate.
    """
    skill_json = parse_skill_output(skill_result.stdout)
    output = _map_skill_json_to_editor_output(skill_json)
    validate_editor_output_shape(
        output, source_section_drafts=source_section_drafts
    )
    return output


def invoke_editor_adapter(
    input_: EditorInput,
    *,
    skill_launcher: SkillLauncher,
    clock=_default_utc_now,  # type: ignore[assignment]
    enable_retry_with_clarification: bool = True,
) -> EditorOutput:
    """Adapter entry — transform → dispatch → parse → validate (+ R2 retry).

    Flow (R1 baseline):

    1. Render ``EditorInput.section_drafts`` to a single markdown string.
    2. Construct :class:`EditorSkillInvocation` envelope.
    3. Dispatch via injected :class:`SkillLauncher` (180_000 ms timeout
       inline literal).
    4. Parse skill stdout — strip fences + extract JSON object.
    5. Map skill JSON → :class:`EditorOutput` (typed shapes).
    6. Validate POST-gate invariants (raises F-EDITOR-* on violation).

    R2 retry-with-clarification (§3.1, default-on):

    - On a *retryable* parse / shape failure on the first attempt
      (``F_EDITOR_SKILL_OUTPUT_MALFORMED_JSON`` / ``F_EDITOR_OUTPUT_SHAPE``
      / ``F_EDITOR_SINGLE_REPLACEMENT``), re-invoke the launcher once
      with a clarification suffix appended to the stdin payload.
    - The retry uses the same source-of-truth section drafts and clock
      tick (the second invocation_at_utc would diverge but the launcher
      payload is keyed against the original envelope so cache lookups
      are stable).
    - On the second attempt's failure, the original F-code propagates.
    - Pass ``enable_retry_with_clarification=False`` to disable (callers
      that want R1's strict single-attempt semantics).

    Hard launcher failures (timeout / subprocess crash) are NOT retried;
    they propagate to the cascade per §4.4 / §4.5 contracts.

    Failure-code mapping:

    - Launcher raises :class:`TimeoutError` → :class:`EditorSkillTimeout`
      (``F-EDITOR-SKILL-TIMEOUT``).
    - Launcher raises any other exception →
      :class:`EditorSkillSubprocessFail`
      (``F-EDITOR-SKILL-SUBPROCESS-FAIL``).
    - Parse failure → :class:`EditorSkillOutputMalformedJson`
      (``F-EDITOR-SKILL-OUTPUT-MALFORMED-JSON``).
    - Shape / 2-3 / rewrite violations → corresponding F-EDITOR-* exception.
    """
    if not isinstance(input_, EditorInput):
        raise TypeError(
            f"invoke_editor_adapter requires EditorInput; got "
            f"{type(input_).__name__}"
        )

    base_payload = _build_base_payload(input_, clock=clock)

    # First attempt — hard launcher failures bubble up untouched.
    skill_result = _dispatch_skill_once(
        skill_launcher=skill_launcher,
        stdin_payload=base_payload,
    )

    first_failure_code: str | None = None
    first_failure_message: str = ""
    try:
        return _parse_map_validate(
            skill_result, source_section_drafts=input_.section_drafts
        )
    except (
        EditorSkillOutputMalformedJson,
        EditorOutputShapeError,
        EditorSingleReplacementError,
    ) as first_exc:
        # Python 3 clears the `as` binding when the except block exits;
        # capture into module-stable locals before we leave the handler.
        first_failure_code = first_exc.failure_code  # type: ignore[union-attr]
        first_failure_message = str(first_exc)
        if (
            not enable_retry_with_clarification
            or first_failure_code not in _RETRYABLE_FAILURE_CODES
        ):
            raise

    # R2: retry once with clarification suffix (N=2 cap inline literal).
    assert first_failure_code is not None  # set by the except handler above
    clarification_payload = _build_clarification_payload(
        base_payload,
        first_failure_code=first_failure_code,
        first_failure_message=first_failure_message,
    )
    retry_result = _dispatch_skill_once(
        skill_launcher=skill_launcher,
        stdin_payload=clarification_payload,
    )
    return _parse_map_validate(
        retry_result, source_section_drafts=input_.section_drafts
    )


__all__ = [
    # Public adapter surface
    "SkillLauncher",
    "SkillSubprocessResult",
    "invoke_editor_adapter",
    "parse_skill_output",
    "validate_editor_output_shape",
    # Failure codes (string constants)
    "F_EDITOR_OUTPUT_SHAPE",
    "F_EDITOR_REWROTE_INSTEAD_OF_FLAGGED",
    "F_EDITOR_SINGLE_REPLACEMENT",
    "F_EDITOR_SKILL_SUBPROCESS_FAIL",
    "F_EDITOR_SKILL_OUTPUT_MALFORMED_JSON",
    "F_EDITOR_SKILL_TIMEOUT",
    # Exception classes
    "EditorOutputShapeError",
    "EditorRewroteInsteadOfFlaggedError",
    "EditorSingleReplacementError",
    "EditorSkillSubprocessFail",
    "EditorSkillOutputMalformedJson",
    "EditorSkillTimeout",
]
