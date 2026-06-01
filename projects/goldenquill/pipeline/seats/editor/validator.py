"""pipeline.seats.editor.validator — §8 Editor Round 2 enhanced validation.

R2 polish-round predicates layered after the R1 adapter parse + map cycle.
Spec card: ``pipeline/engineering/spec_cards/section_08_editor_round_2_polish.md``
§3.2 enhanced validation:

- **Taxonomy sort audit:** flag items appearing in >1 goal/output/outcome/
  objective category. Returns informational NOTE-tier strings; does NOT
  raise (skill may legitimately list the same passage in multiple
  buckets when describing miscategorizations).
- **Tone consistency check:** defense-in-depth on
  ``readability.score_10 ∈ 0..10``. Already enforced by
  ``ReadabilityFeedback.__post_init__`` and the R1 validator; re-run as
  POST-gate so any future drift in the skill output schema surfaces
  before downstream consumers see the (frozen but invalid-by-contract)
  EditorOutput.
- **Quick-wins deduplication:** strip duplicate entries while preserving
  first-seen order. Returns a (potentially) new EditorOutput; identity
  unchanged when no duplicates were present.
- **Terms-to-verify cross-reference:** flag terms that do not appear in
  any ``flagged_terms[].excerpt``. Returns NOTE-tier orphans; does NOT
  raise (the skill may legitimately surface admin-risk terms that aren't
  literal substrings of any flagged excerpt — e.g., the term is paraphrased
  in the issue description, or the skill found it in the source body but
  flagged a different region of the same paragraph).

Design discipline (per spec card §11 hardenings):

- All predicates are pure (input-in / output-out, no I/O, no clock, no
  global state).
- :func:`apply_r2_validation` is the single orchestrator entry — it
  composes the four predicates and returns the deduped EditorOutput
  alongside a :class:`ValidationReport` carrying the NOTE-tier
  diagnostics.
- The validator does NOT mutate the input EditorOutput (frozen by
  contract); deduplication produces a new instance only when the
  ``quick_wins`` tuple actually changes.
- Threat model: input may be hostile (skill returned arbitrary strings).
  All predicates handle empty / unicode / very-long inputs without panic.

R2 retry-with-clarification (adapter.py §3.1) is a *separate* enhancement
landing on the same round LOCK; this module is feedback-only and never
talks to the skill subprocess.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from pipeline.seats.editor.adapter import (
    EditorOutputShapeError,
    F_EDITOR_OUTPUT_SHAPE,
)
from pipeline.seats.editor.types import EditorOutput


# ---------------------------------------------------------------------------
# Public taxonomy-category names (used by audit_taxonomy_sort + tests)
# ---------------------------------------------------------------------------

TAXONOMY_CATEGORIES: Final[tuple[str, ...]] = (
    "goals",
    "outputs",
    "outcomes",
    "objectives",
)


# ---------------------------------------------------------------------------
# ValidationReport — NOTE-tier diagnostics from the R2 pass
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class ValidationReport:
    """NOTE-tier diagnostics surfaced by :func:`apply_r2_validation`.

    Both fields are tuples of strings (immutable, deterministic order).
    Empty tuples mean the corresponding audit found no issues.

    - :attr:`taxonomy_duplicates`: items appearing in >1 of the four
      taxonomy categories. Sorted alphabetically.
    - :attr:`term_orphans`: terms in ``terms_to_verify`` that do NOT
      appear in any flagged_term excerpt. Order preserves the original
      ``terms_to_verify`` ordering.
    - :attr:`quick_wins_deduplicated`: count of duplicate ``quick_wins``
      entries that were stripped. ``0`` means no change.
    """

    taxonomy_duplicates: tuple[str, ...]
    term_orphans: tuple[str, ...]
    quick_wins_deduplicated: int

    def __post_init__(self) -> None:
        if not isinstance(self.taxonomy_duplicates, tuple):
            raise ValueError("taxonomy_duplicates must be a tuple.")
        for i, entry in enumerate(self.taxonomy_duplicates):
            if not isinstance(entry, str):
                raise ValueError(
                    f"taxonomy_duplicates[{i}] must be string; "
                    f"got {type(entry).__name__}"
                )
        if not isinstance(self.term_orphans, tuple):
            raise ValueError("term_orphans must be a tuple.")
        for i, entry in enumerate(self.term_orphans):
            if not isinstance(entry, str):
                raise ValueError(
                    f"term_orphans[{i}] must be string; got {type(entry).__name__}"
                )
        if not isinstance(self.quick_wins_deduplicated, int) or isinstance(
            self.quick_wins_deduplicated, bool
        ):
            raise ValueError(
                "quick_wins_deduplicated must be int (not bool); got "
                f"{type(self.quick_wins_deduplicated).__name__}"
            )
        if self.quick_wins_deduplicated < 0:
            raise ValueError(
                f"quick_wins_deduplicated must be >= 0; got "
                f"{self.quick_wins_deduplicated!r}"
            )


# ---------------------------------------------------------------------------
# audit_taxonomy_sort — flag items in >1 category
# ---------------------------------------------------------------------------


def audit_taxonomy_sort(output: EditorOutput) -> tuple[str, ...]:
    """Return items appearing in >1 of goals/outputs/outcomes/objectives.

    Sorted alphabetically for deterministic output. Empty tuple if every
    item appears in exactly one category (or the categories are empty).

    Comparison is exact-match (case-sensitive, no normalization). Skill
    output is operator-vetted text — false positives from whitespace /
    punctuation drift are R3 scope (heuristic similarity).
    """
    if not isinstance(output, EditorOutput):
        raise EditorOutputShapeError(
            f"{F_EDITOR_OUTPUT_SHAPE}: audit_taxonomy_sort requires "
            f"EditorOutput; got {type(output).__name__}"
        )
    seen: dict[str, set[str]] = {}
    pairs = (
        ("goals", output.taxonomy_check.goals_identified),
        ("outputs", output.taxonomy_check.outputs_identified),
        ("outcomes", output.taxonomy_check.outcomes_identified),
        ("objectives", output.taxonomy_check.objectives_identified),
    )
    for category, items in pairs:
        for item in items:
            seen.setdefault(item, set()).add(category)
    duplicates = sorted(item for item, cats in seen.items() if len(cats) > 1)
    return tuple(duplicates)


# ---------------------------------------------------------------------------
# assert_tone_consistency — defense-in-depth on score_10 in 0..10
# ---------------------------------------------------------------------------


def assert_tone_consistency(output: EditorOutput) -> None:
    """Raise :class:`EditorOutputShapeError` on score_10 outside 0..10.

    The :class:`pipeline.seats.editor.types.ReadabilityFeedback`
    ``__post_init__`` already enforces this invariant at construction
    time, AND :func:`pipeline.seats.editor.adapter.validate_editor_output_shape`
    re-checks it as the third invariant. This validator runs as a third
    defensive layer for the R2 pass — if the skill schema ever changes
    to a 0..100 range (the spec card §3.2 floats this possibility), this
    is the exact failure site that surfaces the drift.
    """
    if not isinstance(output, EditorOutput):
        raise EditorOutputShapeError(
            f"{F_EDITOR_OUTPUT_SHAPE}: assert_tone_consistency requires "
            f"EditorOutput; got {type(output).__name__}"
        )
    score = output.tone_feedback.overall_readability.score_10
    if not (0 <= score <= 10):
        raise EditorOutputShapeError(
            f"{F_EDITOR_OUTPUT_SHAPE}: tone_feedback.overall_readability."
            f"score_10 must be in 0..10; got {score!r}"
        )


# ---------------------------------------------------------------------------
# dedupe_quick_wins — strip duplicate entries; preserve first-seen order
# ---------------------------------------------------------------------------


def dedupe_quick_wins(output: EditorOutput) -> tuple[EditorOutput, int]:
    """Return ``(deduped_output, duplicates_removed_count)``.

    Preserves the first-seen order of ``quick_wins``. When no duplicates
    exist, returns the original ``output`` instance (identity preserved)
    and ``0``; otherwise constructs a new :class:`EditorOutput` with the
    deduped tuple and reports the count of removed entries.

    Comparison is exact-match: ``"Drop hedge"`` and ``"drop hedge"`` are
    distinct entries (case-sensitive). The skill output is operator-vetted
    text and the dedup pass is conservative by design — case-folding /
    whitespace-normalization is R3 scope.
    """
    if not isinstance(output, EditorOutput):
        raise EditorOutputShapeError(
            f"{F_EDITOR_OUTPUT_SHAPE}: dedupe_quick_wins requires "
            f"EditorOutput; got {type(output).__name__}"
        )
    seen: set[str] = set()
    deduped: list[str] = []
    for entry in output.quick_wins:
        if entry not in seen:
            seen.add(entry)
            deduped.append(entry)
    removed = len(output.quick_wins) - len(deduped)
    if removed == 0:
        return output, 0
    new_output = EditorOutput(
        flagged_terms=output.flagged_terms,
        taxonomy_check=output.taxonomy_check,
        tone_feedback=output.tone_feedback,
        quick_wins=tuple(deduped),
        terms_to_verify=output.terms_to_verify,
        gaps=output.gaps,
    )
    return new_output, removed


# ---------------------------------------------------------------------------
# audit_terms_to_verify_cross_reference — flag orphan terms
# ---------------------------------------------------------------------------


def audit_terms_to_verify_cross_reference(output: EditorOutput) -> tuple[str, ...]:
    """Return ``terms_to_verify`` entries with no excerpt cross-reference.

    A term is *orphaned* when it does not appear as a substring of any
    ``flagged_terms[].excerpt``. Order preserves the original
    ``terms_to_verify`` ordering (stable so report diffs are minimal).

    NOTE-tier (informational): the skill may legitimately surface
    admin-risk candidate terms it spotted in the source body without
    flagging the surrounding sentence as a clarity issue, or it may
    paraphrase the term in the issue description rather than the excerpt.
    This audit is a hint to the operator to double-check, not a blocker.

    Match is case-sensitive substring (``in`` operator). Empty term
    string is skipped (would match all excerpts trivially).
    """
    if not isinstance(output, EditorOutput):
        raise EditorOutputShapeError(
            f"{F_EDITOR_OUTPUT_SHAPE}: audit_terms_to_verify_cross_reference "
            f"requires EditorOutput; got {type(output).__name__}"
        )
    excerpts = tuple(t.excerpt for t in output.flagged_terms)
    orphans: list[str] = []
    for term in output.terms_to_verify:
        if not term:
            continue
        if not any(term in excerpt for excerpt in excerpts):
            orphans.append(term)
    return tuple(orphans)


# ---------------------------------------------------------------------------
# apply_r2_validation — orchestrator
# ---------------------------------------------------------------------------


def apply_r2_validation(
    output: EditorOutput,
) -> tuple[EditorOutput, ValidationReport]:
    """Run the R2 enhanced-validation pass.

    Order of operations:

    1. :func:`assert_tone_consistency` — raises :class:`EditorOutputShapeError`
       on score-range drift before any further work.
    2. :func:`audit_taxonomy_sort` — collect taxonomy-category duplicates.
    3. :func:`dedupe_quick_wins` — produce deduped EditorOutput +
       removed-count.
    4. :func:`audit_terms_to_verify_cross_reference` — collect orphans
       on the **deduped** output (unchanged in practice — dedupe only
       affects ``quick_wins``, not ``flagged_terms`` or ``terms_to_verify``,
       but the orchestration order is documented for clarity).

    Returns ``(deduped_output, report)``. If no duplicates / orphans /
    quick-win dupes were found, the returned output is identity-equal to
    the input.
    """
    assert_tone_consistency(output)
    duplicates = audit_taxonomy_sort(output)
    deduped, removed = dedupe_quick_wins(output)
    orphans = audit_terms_to_verify_cross_reference(deduped)
    report = ValidationReport(
        taxonomy_duplicates=duplicates,
        term_orphans=orphans,
        quick_wins_deduplicated=removed,
    )
    return deduped, report


__all__ = [
    "TAXONOMY_CATEGORIES",
    "ValidationReport",
    "audit_taxonomy_sort",
    "assert_tone_consistency",
    "dedupe_quick_wins",
    "audit_terms_to_verify_cross_reference",
    "apply_r2_validation",
]
