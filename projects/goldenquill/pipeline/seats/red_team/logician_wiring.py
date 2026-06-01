"""pipeline.seats.red_team.logician_wiring — PRE/POST gate orchestration.

R3 wires §10's failure-code surface into Logician PRE/POST gate dispatch:

PRE-gates (before Red Team subprocess invocation):
- F-RT-FAMILY-OVERLAP — 3-way distinct check (Red Team ≠ Scribe AND ≠ Judge).
- F-RT-INPUT-MISSING / F-RT-INPUT-INCONSISTENT — input-bundle invariants.
- F-RT-RUBRIC-DRIFT — rubric content-hash matches session manifest pin.
- F-RT-DIALECT-UNCLASSIFIED — funder dialect classification present.
- F-RT-CONTEXT-PLACEMENT — anti-anchoring instructions at start AND end.

POST-gates (after Red Team verdict emission):
- F-RT-EVIDENCE-NOT-IN-DRAFT — Law 5 verbatim-substring (delegates to
  :func:`pipeline.seats.red_team.attack_memo.assert_evidence_in_drafts`).
- F-RT-CRITERION-MISSING — identity-invariant against Judge's scored ID set
  (delegates to :func:`pipeline.seats.red_team.cross_rubric_dispatch.assert_red_team_id_set_matches_judge`).
- F-RT-VERDICT-CERT-MALFORMED — SFR three-block parser (R3 stub here;
  full parser lives in §6 Operating Envelope).
- F-COUNCIL-SPLIT — disagreement-threshold detection (delegates to
  :func:`pipeline.seats.red_team.attack_memo.detect_council_split`).
- F-RT-JUDGE-ANCHOR-SUSPECTED — non-blocking advisory (delegates).

E-017 injected-seam pattern: PRE/POST gate orchestration consumes
deterministic Protocols at the test boundary; production wires concrete
Cedar / admin-risk / vault primitives. Production HTTP is on the provider
side; this module is pure stdlib + Protocol-injected callables.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Protocol, runtime_checkable

from pipeline.seats.red_team.attack_memo import (
    assert_evidence_in_drafts,
    detect_council_split,
    detect_judge_anchor_suspected,
)
from pipeline.seats.red_team.cross_rubric_dispatch import (
    assert_red_team_id_set_matches_judge,
)
from pipeline.seats.red_team.types import (
    F_COUNCIL_SPLIT,
    F_RT_CONTEXT_PLACEMENT,
    F_RT_DIALECT_UNCLASSIFIED,
    F_RT_EVIDENCE_NOT_IN_DRAFT,
    F_RT_FAMILY_OVERLAP,
    F_RT_INPUT_INCONSISTENT,
    F_RT_INPUT_MISSING,
    F_RT_JUDGE_ANCHOR_SUSPECTED,
    F_RT_NO_COMPLIANT_FAMILY,
    F_RT_RUBRIC_DRIFT,
    F_RT_SCOPE_MISSING,
    F_RT_VERDICT_CERT_MALFORMED,
    RedTeamInput,
    RedTeamVerdict,
    SectionDraftLike,
)


# ---------------------------------------------------------------------------
# Result shapes
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True, slots=True)
class PreGateResult:
    """Outcome of the Red Team PRE-gate batch."""

    success: bool
    failure_codes: tuple[str, ...]
    failure_details: tuple[str, ...]


@dataclass(frozen=True, kw_only=True, slots=True)
class PostGateResult:
    """Outcome of the Red Team POST-gate batch.

    `council_split_detected` and `judge_anchor_suspected` are non-blocking
    advisory signals — they're set on success-PASS too, for downstream
    routing.
    """

    success: bool
    failure_codes: tuple[str, ...]
    failure_details: tuple[str, ...]
    council_split_detected: bool
    judge_anchor_suspected: bool


# ---------------------------------------------------------------------------
# E-017 seams: family resolver + scope-statement checker + prompt-template lint
# ---------------------------------------------------------------------------


@runtime_checkable
class FamilyResolver(Protocol):
    """Resolve a seat's currently-bound provider family (after cascade-fallback).

    Production wires this to read ``RunState.run_iteration_families_so_far``
    per §5 v6 §3.2.1; tests inject deterministic stubs.
    """

    def resolve(self, *, seat: str) -> str:
        ...


@runtime_checkable
class PromptCompiledTextProvider(Protocol):
    """Provide the *compiled* prompt text (after operating-envelope template
    substitution) for context-placement linting."""

    def get_compiled_prompt(self, *, run_id: str) -> str:
        ...


# ---------------------------------------------------------------------------
# PRE-gate batch
# ---------------------------------------------------------------------------


def run_pre_gate(
    *,
    input_bundle: RedTeamInput,
    family_resolver: FamilyResolver,
    session_rubric_hash: str,
    compiled_prompt: str,
    anti_anchoring_phrase: str = "Judge's scoring is context, not authority",
) -> PreGateResult:
    """Execute the Red Team PRE-gate batch.

    Returns ``PreGateResult`` with all firing codes; success iff
    ``failure_codes`` is empty.

    The 3-way cross-family distinct check is the load-bearing PRE-gate:
    Red Team's resolved family MUST differ from BOTH Scribe's AND Judge's.
    """
    codes: list[str] = []
    details: list[str] = []

    # F-RT-INPUT-MISSING: Should have been raised at construction time, but
    # defense-in-depth — re-check the structural invariants.
    if not input_bundle.section_drafts:
        codes.append(F_RT_INPUT_MISSING)
        details.append("section_drafts empty")
    if input_bundle.judge_verdict is None:
        # M13 review-seat-bypass scenario; flag as informational. Not a
        # PRE-gate failure (run can proceed under M13 bypass).
        pass

    # F-RT-INPUT-INCONSISTENT: judge_verdict run_id + rubric_hash bind.
    if input_bundle.judge_verdict is not None:
        if input_bundle.judge_verdict.run_id != input_bundle.run_id:
            codes.append(F_RT_INPUT_INCONSISTENT)
            details.append(
                f"judge_verdict.run_id {input_bundle.judge_verdict.run_id!r} "
                f"≠ input run_id {input_bundle.run_id!r}"
            )

    # F-RT-RUBRIC-DRIFT: rubric.content_hash matches session manifest pin.
    if input_bundle.rubric.content_hash != session_rubric_hash:
        codes.append(F_RT_RUBRIC_DRIFT)
        details.append(
            f"rubric.content_hash != session_rubric_hash "
            f"({input_bundle.rubric.content_hash!r} vs {session_rubric_hash!r})"
        )

    # F-RT-DIALECT-UNCLASSIFIED: funder_dialect is a required Literal at
    # construction; defense-in-depth here — re-verify it's present.
    if not input_bundle.funder_dialect:
        codes.append(F_RT_DIALECT_UNCLASSIFIED)
        details.append("funder_dialect empty")

    # F-RT-FAMILY-OVERLAP: 3-way distinct (Red Team ≠ Scribe AND ≠ Judge).
    try:
        scribe_family = family_resolver.resolve(seat="scribe")
        judge_family = family_resolver.resolve(seat="judge")
        red_team_family = family_resolver.resolve(seat="red_team")
        if red_team_family == scribe_family:
            codes.append(F_RT_FAMILY_OVERLAP)
            details.append(
                f"resolved Red Team family {red_team_family!r} matches "
                f"Scribe family (.with_scribe sub-tag)"
            )
        if red_team_family == judge_family:
            codes.append(F_RT_FAMILY_OVERLAP)
            details.append(
                f"resolved Red Team family {red_team_family!r} matches "
                f"Judge family (.with_judge sub-tag)"
            )
    except KeyError as e:
        # Family resolver doesn't know about a required seat → no compliant
        # family possible until cascade resolves.
        codes.append(F_RT_NO_COMPLIANT_FAMILY)
        details.append(f"family resolver KeyError: {e}")

    # F-RT-CONTEXT-PLACEMENT: anti-anchoring phrase at start AND end.
    if anti_anchoring_phrase:
        if anti_anchoring_phrase not in compiled_prompt:
            codes.append(F_RT_CONTEXT_PLACEMENT)
            details.append(
                f"anti-anchoring phrase {anti_anchoring_phrase!r} absent "
                f"from compiled prompt"
            )
        else:
            # Stronger check: phrase appears in BOTH first 1/3 AND last 1/3 of prompt.
            n = len(compiled_prompt)
            head_third = compiled_prompt[: n // 3]
            tail_third = compiled_prompt[2 * n // 3:]
            if anti_anchoring_phrase not in head_third or anti_anchoring_phrase not in tail_third:
                codes.append(F_RT_CONTEXT_PLACEMENT)
                details.append(
                    "anti-anchoring phrase not present in BOTH start AND end thirds of prompt"
                )

    return PreGateResult(
        success=len(codes) == 0,
        failure_codes=tuple(codes),
        failure_details=tuple(details),
    )


# ---------------------------------------------------------------------------
# POST-gate batch
# ---------------------------------------------------------------------------


def run_post_gate(
    *,
    verdict: RedTeamVerdict,
    drafts: tuple[SectionDraftLike, ...],
    judge_total_score: int | None,
    judge_scored_ids: frozenset[str] | None,
    rubric_criteria_count: int,
    total_words: int,
) -> PostGateResult:
    """Execute the Red Team POST-gate batch.

    Returns ``PostGateResult`` with all firing codes + advisory flags.
    Council-split + judge-anchor-suspected are non-blocking; they SET
    the advisory flags but don't add to ``failure_codes`` (the latter is
    success-blocking).

    F-COUNCIL-SPLIT IS added to failure_codes because per §10.6 it
    routes to a sub-phase rather than failing the run, but the gate is
    still "the run cannot auto-advance" — operator decision required.
    """
    blocking_codes: list[str] = []
    blocking_details: list[str] = []

    # F-RT-EVIDENCE-NOT-IN-DRAFT (Law 5 mirror).
    evidence_violations = assert_evidence_in_drafts(verdict=verdict, drafts=drafts)
    if evidence_violations:
        blocking_codes.append(F_RT_EVIDENCE_NOT_IN_DRAFT)
        blocking_details.extend(evidence_violations)

    # F-RT-CRITERION-MISSING (identity-invariant against Judge).
    if judge_scored_ids is not None:
        red_team_ids = frozenset(c.criterion_id for c in verdict.criteria)
        id_violations = assert_red_team_id_set_matches_judge(
            red_team_scored_ids=red_team_ids,
            judge_scored_ids=judge_scored_ids,
        )
        if id_violations:
            blocking_codes.extend(["F-RT-CRITERION-MISSING"] * len(id_violations))
            blocking_details.extend(id_violations)

    # F-COUNCIL-SPLIT (operator-routing; non-blocking on run-validity but
    # blocking on auto-advancement to report_signed per §10.6).
    council_split = False
    if judge_total_score is not None:
        council_split = detect_council_split(
            judge_total_score=judge_total_score,
            red_team_total_score=verdict.total_score,
        )
        if council_split:
            blocking_codes.append(F_COUNCIL_SPLIT)
            blocking_details.append(
                f"|judge {judge_total_score} - red_team {verdict.total_score}| "
                f">= RT_DISAGREEMENT_THRESHOLD"
            )

    # F-RT-JUDGE-ANCHOR-SUSPECTED (non-blocking advisory).
    judge_anchor = False
    if judge_total_score is not None:
        judge_anchor = detect_judge_anchor_suspected(
            judge_total_score=judge_total_score,
            red_team_total_score=verdict.total_score,
            rubric_criteria_count=rubric_criteria_count,
            total_words=total_words,
        )
        # Advisory does NOT add to blocking_codes — surfaces in PostGateResult.

    # Note: F-RT-VERDICT-CERT-MALFORMED is enforced by §6 SFR parser at
    # subprocess output time; the gate runner consumes the parse result.
    # If verdict construction succeeded (typed dataclass), structural validity
    # is implied. The structural-vs-semantic boundary per §10.4 is the §6
    # parser's job, not this orchestrator.

    return PostGateResult(
        success=len(blocking_codes) == 0,
        failure_codes=tuple(blocking_codes),
        failure_details=tuple(blocking_details),
        council_split_detected=council_split,
        judge_anchor_suspected=judge_anchor,
    )


# ---------------------------------------------------------------------------
# SFR-malformed gate stub (R3 minimal — §6 owns the full parser)
# ---------------------------------------------------------------------------


def assert_sfr_three_block_present(sfr_markdown: str) -> tuple[str, ...]:
    """Lightweight SFR three-block presence check.

    Returns violation strings; empty tuple ⇒ pass. R3 minimal — §6 Operating
    Envelope owns the full SFR parser per architecture §F.1.
    """
    violations: list[str] = []
    required_headings = ("## Premises", "## Execution trace", "## Conclusion")
    for heading in required_headings:
        if heading not in sfr_markdown:
            violations.append(
                f"{F_RT_VERDICT_CERT_MALFORMED}.missing_block: {heading}"
            )
    if not violations:
        # Order check — Premises before Trace before Conclusion.
        idx_p = sfr_markdown.find("## Premises")
        idx_t = sfr_markdown.find("## Execution trace")
        idx_c = sfr_markdown.find("## Conclusion")
        if not (idx_p < idx_t < idx_c):
            violations.append(
                f"{F_RT_VERDICT_CERT_MALFORMED}.block_order_wrong"
            )
    return tuple(violations)


__all__ = [
    "PreGateResult",
    "PostGateResult",
    "FamilyResolver",
    "PromptCompiledTextProvider",
    "run_pre_gate",
    "run_post_gate",
    "assert_sfr_three_block_present",
]
