"""pipeline.seats.judge.logician_wiring — R3 Judge PRE/POST gate assembly.

Spec card: ``pipeline/engineering/spec_cards/section_09_judge_round_3_seat_entry_and_sfr.md``
§4 (PRE/POST gate wiring) + §5 (test surface).

R3 authors pure *assemblers*. The predicates themselves live in:

- :mod:`pipeline.logician.cedar_eval` — cross-org isolation (Law 3 anchor).
- :mod:`pipeline.seats.judge.verdict_assembler` — coverage / score-bound /
  evidence-in-draft (Law 5 anchor).
- :mod:`pipeline.seats.judge.rubric_loader` — rubric SHA-256 continuity.

This module wires Judge-specific F-JUDGE-* codes over those predicates
via injected Protocol seams (E-017) and fires inline deterministic checks
for envelope-local invariants (cross-family family equality, rubric-hash
drift between envelope-pinned and on-disk rubric, evidence-quote
verbatim-substring discipline).

Disciplines:

- **F_PIPE_08 cross-family.** ``F-JUDGE-CROSS-FAMILY-COLLISION`` fires
  when ``envelope.scribe_provider_family == "google"`` (Judge's own
  family).
- **E-017 injected seams.** Every cross-module Logician call is a
  Protocol callable — production wires real modules, tests inject stubs.
- **Law 5 Judge-owned.** ``F-JUDGE-EVIDENCE-NOT-IN-DRAFT`` is checked
  locally over ``CriterionScore.evidence_quote`` ⊆
  ``SectionDraftLike.body_text``.
- **Fail-closed.** Every trip raises :class:`.seat.JudgeGateFailed` with
  ``failure_code`` + ``trigger`` + ``evidence``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Final, Mapping, Protocol

from pipeline.seats.judge.seat import (
    F_JUDGE_CROSS_FAMILY_COLLISION,
    F_JUDGE_ORG_CROSS_REF,
    JudgeEnvelope,
    JudgeGateFailed,
)
from pipeline.seats.judge.types import (
    F_JUDGE_CRITERION_MISSING,
    F_JUDGE_EVIDENCE_NOT_IN_DRAFT,
    F_JUDGE_RUBRIC_HASH_DRIFT,
    F_JUDGE_RUBRIC_MALFORMED,
    F_JUDGE_SCORE_OUT_OF_BOUND,
    JudgeVerdict,
    Rubric,
    SectionDraftLike,
)


# Judge's own family — V1 inline-literal-elsewhere; this constant is for
# human reading. The actual comparison inside the assembler uses the
# inline literal ``"google"`` per V1 rebind-resistance.
_JUDGE_OWN_FAMILY: Final[str] = "google"


# ---------------------------------------------------------------------------
# Protocol seams (E-017)
# ---------------------------------------------------------------------------


class CedarCrossOrgCheck(Protocol):
    """Cedar ``org_isolation`` policy evaluator.

    Returns the list of *foreign* org slugs detected in the envelope's
    project_context or section_drafts blob — empty list is PASS.
    Production typically delegates to
    ``pipeline.logician.cedar_eval.evaluate_cross_org_dossier``.
    """

    def __call__(
        self,
        *,
        envelope_org_slug: str,
        section_drafts_blob: tuple[Mapping[str, Any], ...],
        project_context: Mapping[str, Any],
    ) -> tuple[str, ...]: ...


class RubricHashRecompute(Protocol):
    """Recompute the rubric SHA-256 from the on-disk rubric path.

    Production wires ``pipeline.seats.judge.rubric_loader.compute_rubric_sha256``
    over a freshly-read JSON file. Returns the canonical 64-hex lowercase
    SHA-256 of the rubric's JSON-serialized form.
    """

    def __call__(self, *, rubric_path: str) -> str: ...


# ---------------------------------------------------------------------------
# Assembly result shapes
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class JudgePreGateAssembly:
    """Report of which F-codes the PRE-gate assembly checked and passed."""

    run_id: str
    org_slug: str
    codes_checked: tuple[str, ...]


@dataclass(frozen=True, kw_only=True, slots=True)
class JudgePostGateAssembly:
    """Report of which F-codes the POST-gate assembly checked and passed."""

    run_id: str
    org_slug: str
    codes_checked: tuple[str, ...]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _raise_judge(
    *, failure_code: str, trigger: str, evidence: Mapping[str, Any]
) -> None:
    """Construct + raise JudgeGateFailed with required kwargs."""
    raise JudgeGateFailed(
        failure_code=failure_code, trigger=trigger, evidence=evidence
    )


# ---------------------------------------------------------------------------
# PRE-gate assembler
# ---------------------------------------------------------------------------


def assemble_judge_pre_gate(
    *,
    envelope: JudgeEnvelope,
    cedar_cross_org_check: CedarCrossOrgCheck,
) -> JudgePreGateAssembly:
    """Judge PRE-gate: runs BEFORE the Google dispatch.

    Raises :class:`JudgeGateFailed` on any F-JUDGE-* trip; seat catches
    and emits structured stderr + exit 2.

    Checks (order is canonical):

    1. ``F-JUDGE-CROSS-FAMILY-COLLISION`` — Scribe-landed family equals
       Judge's own family ``"google"``.
    2. ``F-JUDGE-ORG-CROSS-REF`` via Cedar ``org_isolation`` over the
       envelope's project_context + section_drafts blob.
    """
    # Check 1 — cross-family discipline.
    if envelope.scribe_provider_family == "google":
        _raise_judge(
            failure_code=F_JUDGE_CROSS_FAMILY_COLLISION,
            trigger="scribe_landed_same_family_as_judge",
            evidence={
                "scribe_provider_family": envelope.scribe_provider_family,
                "judge_own_family": "google",
            },
        )

    # Check 2 — Cedar org-isolation.
    foreign_slugs = cedar_cross_org_check(
        envelope_org_slug=envelope.org_slug,
        section_drafts_blob=envelope.section_drafts_blob,
        project_context=envelope.project_context,
    )
    if foreign_slugs:
        _raise_judge(
            failure_code=F_JUDGE_ORG_CROSS_REF,
            trigger="cedar_org_isolation_tripped",
            evidence={
                "envelope_org_slug": envelope.org_slug,
                "foreign_slugs": list(foreign_slugs),
            },
        )

    return JudgePreGateAssembly(
        run_id=envelope.run_id,
        org_slug=envelope.org_slug,
        codes_checked=(
            F_JUDGE_CROSS_FAMILY_COLLISION,
            F_JUDGE_ORG_CROSS_REF,
        ),
    )


# ---------------------------------------------------------------------------
# POST-gate assembler
# ---------------------------------------------------------------------------


def _check_evidence_in_drafts(
    judge_verdict: JudgeVerdict,
    section_drafts: tuple[SectionDraftLike, ...],
) -> tuple[str, ...]:
    """Return tuple of criterion_ids whose evidence_quote is not a
    verbatim substring of any draft body. Empty tuple = PASS."""
    if not section_drafts:
        return tuple(sc.criterion_id for sc in judge_verdict.judge_output.criterion_scores)
    bad: list[str] = []
    for sc in judge_verdict.judge_output.criterion_scores:
        quote = sc.evidence_quote
        if not isinstance(quote, str) or not quote.strip():
            bad.append(sc.criterion_id)
            continue
        found = False
        for draft in section_drafts:
            if quote in draft.body_text:
                found = True
                break
        if not found:
            bad.append(sc.criterion_id)
    return tuple(bad)


def _check_score_bounds(
    judge_verdict: JudgeVerdict, rubric: Rubric
) -> tuple[str, ...]:
    """Return tuple of criterion_ids whose score is out of [0, max_points]
    against the rubric. Empty tuple = PASS.

    Walks rubric.criteria + subcriteria; if a score id does not match any
    criterion / subcriterion, that's a coverage failure (handled by
    :func:`_check_coverage`), not a bound failure — skip silently here.
    """
    by_id: dict[str, int] = {}
    for crit in rubric.criteria:
        by_id[crit.id] = crit.max_points
        for sub in crit.subcriteria:
            by_id[sub.id] = sub.max_points
    bad: list[str] = []
    for sc in judge_verdict.judge_output.criterion_scores:
        max_pts = by_id.get(sc.criterion_id)
        if max_pts is None:
            continue
        if sc.score < 0 or sc.score > max_pts:
            bad.append(sc.criterion_id)
    return tuple(bad)


def _check_coverage(
    judge_verdict: JudgeVerdict, rubric: Rubric
) -> tuple[str, ...]:
    """Return tuple of criterion_ids whose coverage is missing or partial.
    Empty tuple = PASS.

    Mirrors :func:`pipeline.seats.judge.verdict_assembler._coverage_max_for_criterion`
    — the assembler R2 already rejects malformed coverage, but a POST-gate
    re-check is defense-in-depth against test-stub orchestrators that
    bypass the R2 path.
    """
    score_ids = frozenset(
        sc.criterion_id for sc in judge_verdict.judge_output.criterion_scores
    )
    bad: list[str] = []
    for crit in rubric.criteria:
        parent_covered = crit.id in score_ids
        sub_ids = tuple(s.id for s in crit.subcriteria)
        sub_flags = tuple(sid in score_ids for sid in sub_ids)
        any_sub = any(sub_flags)
        all_sub = bool(sub_ids) and all(sub_flags)
        if parent_covered and any_sub:
            bad.append(crit.id)
            continue
        if parent_covered:
            continue
        if not crit.subcriteria:
            bad.append(crit.id)
            continue
        if all_sub:
            continue
        bad.append(crit.id)
    return tuple(bad)


def assemble_judge_post_gate(
    *,
    envelope: JudgeEnvelope,
    judge_verdict: JudgeVerdict,
    rubric: Rubric,
    section_drafts: tuple[SectionDraftLike, ...],
    rubric_hash_recompute: RubricHashRecompute,
) -> JudgePostGateAssembly:
    """Judge POST-gate: runs AFTER the orchestrator + SFR emission, before
    stdout.

    Raises :class:`JudgeGateFailed` on any F-JUDGE-* trip.

    Checks (order is canonical):

    1. ``F-JUDGE-RUBRIC-MALFORMED`` — rubric.criteria empty or
       rubric.max_score <= 0.
    2. ``F-JUDGE-RUBRIC-HASH-DRIFT`` — recompute on-disk rubric SHA-256
       and compare against ``judge_output.rubric_sha256`` (drift between
       score time and gate time).
    3. ``F-JUDGE-CRITERION-MISSING`` — coverage walker flags any criterion
       not covered by exactly-one path.
    4. ``F-JUDGE-SCORE-OUT-OF-BOUND`` — any score outside [0, max_points].
    5. ``F-JUDGE-EVIDENCE-NOT-IN-DRAFT`` (Law 5) — every evidence_quote
       must be a verbatim substring of at least one section_drafts[*].body_text.
    """
    # Check 1 — rubric malformed (defense-in-depth).
    if not rubric.criteria or rubric.max_score <= 0:
        _raise_judge(
            failure_code=F_JUDGE_RUBRIC_MALFORMED,
            trigger="rubric_empty_criteria_or_nonpositive_max_score",
            evidence={
                "criteria_count": len(rubric.criteria),
                "max_score": rubric.max_score,
            },
        )

    # Check 2 — rubric hash drift between score-time and gate-time.
    try:
        recomputed_sha = rubric_hash_recompute(rubric_path=envelope.rubric_path)
    except JudgeGateFailed:
        raise
    except Exception as exc:
        # Recompute path itself failed — surface as RUBRIC-HASH-DRIFT with
        # a class-only evidence field (defense-in-depth against on-disk
        # path / FS-state echoing through stderr).
        _raise_judge(
            failure_code=F_JUDGE_RUBRIC_HASH_DRIFT,
            trigger="rubric_hash_recompute_failed",
            evidence={"exception_class": type(exc).__name__},
        )
        return JudgePostGateAssembly(  # pragma: no cover  — _raise raises
            run_id=envelope.run_id,
            org_slug=envelope.org_slug,
            codes_checked=(),
        )
    if recomputed_sha != judge_verdict.judge_output.rubric_sha256:
        _raise_judge(
            failure_code=F_JUDGE_RUBRIC_HASH_DRIFT,
            trigger="rubric_sha256_drift_between_score_and_gate",
            evidence={
                "score_time_sha": judge_verdict.judge_output.rubric_sha256,
                "gate_time_sha": recomputed_sha,
            },
        )

    # Check 3 — coverage.
    missing = _check_coverage(judge_verdict, rubric)
    if missing:
        _raise_judge(
            failure_code=F_JUDGE_CRITERION_MISSING,
            trigger="rubric_criterion_coverage_failure",
            evidence={"missing_criteria": list(missing)},
        )

    # Check 4 — score bounds.
    out_of_bound = _check_score_bounds(judge_verdict, rubric)
    if out_of_bound:
        _raise_judge(
            failure_code=F_JUDGE_SCORE_OUT_OF_BOUND,
            trigger="score_outside_unit_max_points",
            evidence={"out_of_bound_criteria": list(out_of_bound)},
        )

    # Check 5 — evidence-in-draft (Law 5).
    unsourced = _check_evidence_in_drafts(judge_verdict, section_drafts)
    if unsourced:
        _raise_judge(
            failure_code=F_JUDGE_EVIDENCE_NOT_IN_DRAFT,
            trigger="evidence_quote_not_verbatim_substring_of_any_draft",
            evidence={"unsourced_criteria": list(unsourced)},
        )

    return JudgePostGateAssembly(
        run_id=envelope.run_id,
        org_slug=envelope.org_slug,
        codes_checked=(
            F_JUDGE_RUBRIC_MALFORMED,
            F_JUDGE_RUBRIC_HASH_DRIFT,
            F_JUDGE_CRITERION_MISSING,
            F_JUDGE_SCORE_OUT_OF_BOUND,
            F_JUDGE_EVIDENCE_NOT_IN_DRAFT,
        ),
    )


__all__ = [
    # Protocol seams
    "CedarCrossOrgCheck",
    "RubricHashRecompute",
    # Result shapes
    "JudgePreGateAssembly",
    "JudgePostGateAssembly",
    # Assemblers
    "assemble_judge_pre_gate",
    "assemble_judge_post_gate",
]
