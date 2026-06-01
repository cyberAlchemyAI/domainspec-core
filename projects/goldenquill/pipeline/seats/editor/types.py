"""pipeline.seats.editor.types — §8 Editor Round 1 typed shapes.

Adapter-pattern entry shapes for the Editor seat. Per parent spec card §4
decision 1, R1 wraps :file:`skills/editor/SKILL.md` rather than reimplementing
its prompt logic in Python; the typed shapes below pin the input/output
contract that the adapter and seat layers cooperate on.

Disciplines (see spec card §4 + §5):

- Frozen, kw-only, slots=True dataclasses (A-13 memory-layout discipline,
  8 GB dev node).
- Closed-set enumerations declared as inline-literal frozensets at module
  scope (V1 rebind-resistance — operator that hot-edits the literal in
  one place still cannot rebind it).
- ``__post_init__`` invariant enforcement on every shape EXCEPT the 2-3
  replacement invariant on :class:`FlaggedTerm`, which is enforced by
  :func:`pipeline.seats.editor.adapter.validate_editor_output_shape`
  (per §4 decision 5: parser must be able to construct a malformed shape
  so the validator can surface the violation via a clean F-code).

Schema mapping (skill JSON ↔ typed shape; see :file:`skills/editor/SKILL.md`):

- ``readability`` ↔ :class:`ReadabilityFeedback`
- ``readability.reviewer_fatigue_sections`` + skill prose ↔
  :class:`ToneFeedback`
- ``suggestions[]`` ↔ ``EditorOutput.flagged_terms`` (one
  :class:`FlaggedTerm` per ``suggestions[]`` entry)
- ``suggestions[].options[]`` ↔ ``FlaggedTerm.replacement_options`` (each a
  :class:`ReplacementOption`; 2-3 per term per skill prompt invariant)
- ``gaps[]`` ↔ :class:`EditorGap` (operator-visible needs-data flag)

Section taxonomy (goals / outputs / outcomes / objectives) lives in
:class:`TaxonomyCheck`, lifted from the legacy
:file:`pipeline/orchestrator/seats/editor.py:30-49` schema. Skill prompt
populates the four lists + miscategorizations; adapter maps verbatim.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Final, Literal, Mapping


# ---------------------------------------------------------------------------
# Closed-set enumerations (V1 rebind-resistance via inline-literal frozensets)
# ---------------------------------------------------------------------------

Dialect = Literal["conservative", "centrist", "progressive", "soul_fire"]

_DIALECT_VALID: Final[frozenset[str]] = frozenset(
    {"conservative", "centrist", "progressive", "soul_fire"}
)

# Issue-type vocabulary — lifted verbatim from
# ``pipeline/orchestrator/seats/editor.py:159-162`` plus the
# ``specificity_gap`` category surfaced in ``skills/editor/SKILL.md`` §3
# (lines 71-78).
IssueType = Literal[
    "jargon",
    "hedge_language",
    "buried_claim",
    "goal_output_confusion",
    "passive_voice",
    "dialect_mismatch",
    "redundancy",
    "ambiguity",
    "specificity_gap",
]

_ISSUE_TYPE_VALID: Final[frozenset[str]] = frozenset(
    {
        "jargon",
        "hedge_language",
        "buried_claim",
        "goal_output_confusion",
        "passive_voice",
        "dialect_mismatch",
        "redundancy",
        "ambiguity",
        "specificity_gap",
    }
)

Severity = Literal["high", "medium", "low"]

_SEVERITY_VALID: Final[frozenset[str]] = frozenset({"high", "medium", "low"})

ReplacementLabel = Literal["A", "B", "C"]

_REPLACEMENT_LABEL_VALID: Final[frozenset[str]] = frozenset({"A", "B", "C"})


# ---------------------------------------------------------------------------
# ReplacementOption (FlaggedTerm sub-shape)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class ReplacementOption:
    """One labeled replacement option from skill ``suggestions[].options[]``.

    Skill prompt invariant: 2-3 options per :class:`FlaggedTerm`, labeled
    A/B/C. ``note`` is optional rationale text (e.g., "Strongest — specific
    equipment, capacity, and throughput" from SKILL.md example).
    """

    label: ReplacementLabel
    text: str
    note: str

    def __post_init__(self) -> None:
        if self.label not in _REPLACEMENT_LABEL_VALID:
            raise ValueError(
                f"ReplacementOption.label must be one of "
                f"{sorted(_REPLACEMENT_LABEL_VALID)}; got {self.label!r}."
            )
        if not isinstance(self.text, str) or not self.text.strip():
            raise ValueError("ReplacementOption.text must be non-empty.")
        if not isinstance(self.note, str):
            raise ValueError("ReplacementOption.note must be a string (may be empty).")


# ---------------------------------------------------------------------------
# FlaggedTerm
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class FlaggedTerm:
    """One clarity issue surfaced by the Editor skill.

    Maps from ``suggestions[]`` entries in the skill JSON. The 2-3
    replacement invariant is **NOT** enforced here — see spec card §4
    decision 5. ``__post_init__`` admits ``replacement_options`` of any
    length so that a malformed skill response can be parsed; the
    validator (:func:`pipeline.seats.editor.adapter.validate_editor_output_shape`)
    catches the length violation and raises the
    ``F-EDITOR-SINGLE-REPLACEMENT`` POST-gate code.
    """

    section_ref: str
    issue_type: IssueType
    severity: Severity
    excerpt: str
    why_it_hurts: str
    replacement_options: tuple[ReplacementOption, ...]
    rubric_connection: str

    def __post_init__(self) -> None:
        if not isinstance(self.section_ref, str) or not self.section_ref.strip():
            raise ValueError("FlaggedTerm.section_ref must be non-empty.")
        if self.issue_type not in _ISSUE_TYPE_VALID:
            raise ValueError(
                f"FlaggedTerm.issue_type must be one of "
                f"{sorted(_ISSUE_TYPE_VALID)}; got {self.issue_type!r}."
            )
        if self.severity not in _SEVERITY_VALID:
            raise ValueError(
                f"FlaggedTerm.severity must be one of "
                f"{sorted(_SEVERITY_VALID)}; got {self.severity!r}."
            )
        if not isinstance(self.excerpt, str) or not self.excerpt.strip():
            raise ValueError("FlaggedTerm.excerpt must be non-empty.")
        if not isinstance(self.why_it_hurts, str) or not self.why_it_hurts.strip():
            raise ValueError("FlaggedTerm.why_it_hurts must be non-empty.")
        if not isinstance(self.replacement_options, tuple):
            raise ValueError(
                "FlaggedTerm.replacement_options must be a tuple (immutable)."
            )
        if not isinstance(self.rubric_connection, str):
            raise ValueError(
                "FlaggedTerm.rubric_connection must be a string (may be empty)."
            )


# ---------------------------------------------------------------------------
# Miscategorization (TaxonomyCheck sub-shape)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class Miscategorization:
    """One goal/output/outcome/objective miscategorization the skill flagged.

    From legacy schema ``taxonomy_check.miscategorizations[]``. Skill
    surfaces draft passages where the applicant called an output a goal or
    similar; adapter maps verbatim.
    """

    excerpt: str
    stated_as: str
    should_be: str
    why: str

    def __post_init__(self) -> None:
        if not isinstance(self.excerpt, str) or not self.excerpt.strip():
            raise ValueError("Miscategorization.excerpt must be non-empty.")
        if not isinstance(self.stated_as, str) or not self.stated_as.strip():
            raise ValueError("Miscategorization.stated_as must be non-empty.")
        if not isinstance(self.should_be, str) or not self.should_be.strip():
            raise ValueError("Miscategorization.should_be must be non-empty.")
        if not isinstance(self.why, str) or not self.why.strip():
            raise ValueError("Miscategorization.why must be non-empty.")


# ---------------------------------------------------------------------------
# TaxonomyCheck
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class TaxonomyCheck:
    """Goal / output / outcome / objective sort from skill output.

    Per ``skills/editor/SKILL.md`` §3 (lines 79-113), the skill checks
    drafts for tangled goal/output/outcome/objective distinctions — most
    applicants get this wrong. Empty lists are valid (the section may not
    contain any of the category).
    """

    goals_identified: tuple[str, ...]
    outputs_identified: tuple[str, ...]
    outcomes_identified: tuple[str, ...]
    objectives_identified: tuple[str, ...]
    miscategorizations: tuple[Miscategorization, ...]

    def __post_init__(self) -> None:
        for field_name in (
            "goals_identified",
            "outputs_identified",
            "outcomes_identified",
            "objectives_identified",
        ):
            value = getattr(self, field_name)
            if not isinstance(value, tuple):
                raise ValueError(
                    f"TaxonomyCheck.{field_name} must be a tuple; got "
                    f"{type(value).__name__}."
                )
            for i, entry in enumerate(value):
                if not isinstance(entry, str) or not entry.strip():
                    raise ValueError(
                        f"TaxonomyCheck.{field_name}[{i}] must be a non-empty "
                        f"string; got {entry!r}."
                    )
        if not isinstance(self.miscategorizations, tuple):
            raise ValueError(
                "TaxonomyCheck.miscategorizations must be a tuple."
            )


# ---------------------------------------------------------------------------
# ReadabilityFeedback (ToneFeedback sub-shape)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class ReadabilityFeedback:
    """Skill ``readability`` block — score/grade-level/verdict.

    Maps from skill JSON ``readability`` per SKILL.md lines 200-206.
    ``score_10`` is the legacy 0-10 readability score from the legacy
    schema (``orchestrator/seats/editor.py:30-32``); SKILL.md uses
    ``estimated_grade_level`` (an int grade level) — adapter maps both:
    skill emits ``score_10`` if available, else adapter computes from
    ``estimated_grade_level``.
    """

    score_10: int
    grade_level_estimate: str
    verdict: str

    def __post_init__(self) -> None:
        if not isinstance(self.score_10, int) or isinstance(self.score_10, bool):
            raise ValueError(
                f"ReadabilityFeedback.score_10 must be an int; got "
                f"{type(self.score_10).__name__}."
            )
        if not (0 <= self.score_10 <= 10):
            raise ValueError(
                f"ReadabilityFeedback.score_10 must be in 0..10; got "
                f"{self.score_10!r}."
            )
        if (
            not isinstance(self.grade_level_estimate, str)
            or not self.grade_level_estimate.strip()
        ):
            raise ValueError(
                "ReadabilityFeedback.grade_level_estimate must be non-empty."
            )
        if not isinstance(self.verdict, str) or not self.verdict.strip():
            raise ValueError("ReadabilityFeedback.verdict must be non-empty.")


# ---------------------------------------------------------------------------
# ToneFeedback
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class ToneFeedback:
    """Operator-visible prose-side feedback — readability + key message.

    Per spec card §4 decision 4: ``flagged_terms`` is the
    machine-consumable side; ``ToneFeedback`` is the read-only operator
    surface (free-form prose) and stays unstructured by design.
    """

    overall_readability: ReadabilityFeedback
    key_message: str
    reviewer_fatigue_sections: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.overall_readability, ReadabilityFeedback):
            raise ValueError(
                "ToneFeedback.overall_readability must be a "
                "ReadabilityFeedback instance."
            )
        if not isinstance(self.key_message, str) or not self.key_message.strip():
            raise ValueError("ToneFeedback.key_message must be non-empty.")
        if not isinstance(self.reviewer_fatigue_sections, tuple):
            raise ValueError(
                "ToneFeedback.reviewer_fatigue_sections must be a tuple."
            )
        for i, entry in enumerate(self.reviewer_fatigue_sections):
            if not isinstance(entry, str) or not entry.strip():
                raise ValueError(
                    f"ToneFeedback.reviewer_fatigue_sections[{i}] must be a "
                    f"non-empty string; got {entry!r}."
                )


# ---------------------------------------------------------------------------
# EditorGap (skill ``gaps[]`` entries)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class EditorGap:
    """One ``gaps[]`` entry — claim missing data the skill flagged for fill.

    Per SKILL.md §What-You-Do-Not-Do: "Add substance" is forbidden; instead,
    the skill flags gaps for the applicant to address. Adapter maps
    verbatim — Logician downstream may consume these for the
    overlooked-expenses cross-check, but R1 just preserves the structure.
    """

    section_ref: str
    issue: str
    action_needed: str

    def __post_init__(self) -> None:
        if not isinstance(self.section_ref, str) or not self.section_ref.strip():
            raise ValueError("EditorGap.section_ref must be non-empty.")
        if not isinstance(self.issue, str) or not self.issue.strip():
            raise ValueError("EditorGap.issue must be non-empty.")
        if not isinstance(self.action_needed, str) or not self.action_needed.strip():
            raise ValueError("EditorGap.action_needed must be non-empty.")


# ---------------------------------------------------------------------------
# EditorInput
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class EditorInput:
    """Adapter-layer input — what the seat hands to ``invoke_editor_adapter``.

    ``section_drafts`` is a tuple of dicts (skill consumes pre-rendered
    markdown; adapter renders the tuple to a single markdown string before
    dispatch). Decoupling from :class:`pipeline.seats.scribe.section_draft.SectionDraft`
    at this layer keeps the Editor adapter testable without a full
    Scribe-R3 import surface; production wiring renders SectionDraft to
    the dict shape at the call site.

    ``section_draft_dict`` shape (per-entry, mirrors the SectionDraft
    persistence schema):

    - ``section_name`` (str)
    - ``section_order`` (int >= 1)
    - ``body_text`` (str)
    - other fields tolerated but ignored by R1 markdown-render.
    """

    section_drafts: tuple[Mapping[str, object], ...]
    rfa_excerpt: str
    dialect: Dialect
    session_id: str
    org_slug: str

    def __post_init__(self) -> None:
        if not isinstance(self.section_drafts, tuple):
            raise ValueError(
                "EditorInput.section_drafts must be a tuple (immutable)."
            )
        if len(self.section_drafts) < 1:
            raise ValueError(
                "EditorInput.section_drafts must contain at least one section "
                "to edit."
            )
        for i, sd in enumerate(self.section_drafts):
            if not isinstance(sd, Mapping):
                raise ValueError(
                    f"EditorInput.section_drafts[{i}] must be a mapping; got "
                    f"{type(sd).__name__}."
                )
            for required in ("section_name", "section_order", "body_text"):
                if required not in sd:
                    raise ValueError(
                        f"EditorInput.section_drafts[{i}] missing required "
                        f"field {required!r}."
                    )
        if not isinstance(self.rfa_excerpt, str):
            raise ValueError("EditorInput.rfa_excerpt must be a string.")
        if self.dialect not in _DIALECT_VALID:
            raise ValueError(
                f"EditorInput.dialect must be one of "
                f"{sorted(_DIALECT_VALID)}; got {self.dialect!r}."
            )
        if not isinstance(self.session_id, str) or not self.session_id.strip():
            raise ValueError("EditorInput.session_id must be non-empty.")
        if not isinstance(self.org_slug, str) or not self.org_slug.strip():
            raise ValueError("EditorInput.org_slug must be non-empty.")


# ---------------------------------------------------------------------------
# EditorSkillInvocation (what the adapter sends to the skill subprocess)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class EditorSkillInvocation:
    """Adapter → skill subprocess stdin payload (typed form).

    ``invocation_at_utc`` is timezone-aware (E-017 clock-seam discipline).
    ``rfa_excerpt`` is truncated to the documented 4000-character ceiling
    BEFORE construction (the legacy adapter at
    :file:`pipeline/orchestrator/seats/editor.py:128` slices the same way).
    """

    draft_markdown: str
    rfa_excerpt: str
    dialect: Dialect
    session_id: str
    org_slug: str
    invocation_at_utc: datetime

    def __post_init__(self) -> None:
        if not isinstance(self.draft_markdown, str) or not self.draft_markdown.strip():
            raise ValueError("EditorSkillInvocation.draft_markdown must be non-empty.")
        if not isinstance(self.rfa_excerpt, str):
            raise ValueError("EditorSkillInvocation.rfa_excerpt must be a string.")
        if self.dialect not in _DIALECT_VALID:
            raise ValueError(
                f"EditorSkillInvocation.dialect must be one of "
                f"{sorted(_DIALECT_VALID)}; got {self.dialect!r}."
            )
        if not isinstance(self.session_id, str) or not self.session_id.strip():
            raise ValueError("EditorSkillInvocation.session_id must be non-empty.")
        if not isinstance(self.org_slug, str) or not self.org_slug.strip():
            raise ValueError("EditorSkillInvocation.org_slug must be non-empty.")
        if self.invocation_at_utc.tzinfo is None:
            raise ValueError(
                "EditorSkillInvocation.invocation_at_utc must be timezone-aware."
            )


# ---------------------------------------------------------------------------
# EditorOutput
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class EditorOutput:
    """Adapter-layer output — what ``invoke_editor_adapter`` returns.

    Mixed structured + prose per spec card §4 decision 4:

    - ``flagged_terms`` is machine-consumable (downstream Scribe-revision
      iteration walks the tuple).
    - ``tone_feedback`` is operator-visible prose (read-only surface).
    - ``quick_wins`` + ``terms_to_verify`` are operator-visible string
      tuples (Logician consumes ``terms_to_verify`` separately for
      admin-risk pre-cross-check).
    """

    flagged_terms: tuple[FlaggedTerm, ...]
    taxonomy_check: TaxonomyCheck
    tone_feedback: ToneFeedback
    quick_wins: tuple[str, ...]
    terms_to_verify: tuple[str, ...]
    gaps: tuple[EditorGap, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.flagged_terms, tuple):
            raise ValueError("EditorOutput.flagged_terms must be a tuple.")
        for i, ft in enumerate(self.flagged_terms):
            if not isinstance(ft, FlaggedTerm):
                raise ValueError(
                    f"EditorOutput.flagged_terms[{i}] must be a FlaggedTerm "
                    f"instance; got {type(ft).__name__}."
                )
        if not isinstance(self.taxonomy_check, TaxonomyCheck):
            raise ValueError(
                "EditorOutput.taxonomy_check must be a TaxonomyCheck instance."
            )
        if not isinstance(self.tone_feedback, ToneFeedback):
            raise ValueError(
                "EditorOutput.tone_feedback must be a ToneFeedback instance."
            )
        if not isinstance(self.quick_wins, tuple):
            raise ValueError("EditorOutput.quick_wins must be a tuple.")
        for i, qw in enumerate(self.quick_wins):
            if not isinstance(qw, str) or not qw.strip():
                raise ValueError(
                    f"EditorOutput.quick_wins[{i}] must be a non-empty string."
                )
        if not isinstance(self.terms_to_verify, tuple):
            raise ValueError("EditorOutput.terms_to_verify must be a tuple.")
        for i, tv in enumerate(self.terms_to_verify):
            if not isinstance(tv, str) or not tv.strip():
                raise ValueError(
                    f"EditorOutput.terms_to_verify[{i}] must be a non-empty string."
                )
        if not isinstance(self.gaps, tuple):
            raise ValueError("EditorOutput.gaps must be a tuple.")


__all__ = [
    # Closed-set Literals
    "Dialect",
    "IssueType",
    "Severity",
    "ReplacementLabel",
    # Shapes
    "ReplacementOption",
    "FlaggedTerm",
    "Miscategorization",
    "TaxonomyCheck",
    "ReadabilityFeedback",
    "ToneFeedback",
    "EditorGap",
    "EditorInput",
    "EditorSkillInvocation",
    "EditorOutput",
]
