"""F-REPORT-COMMITMENT-MISSED — POST judge-equivalent + PRE pre-track-dispatch.

Per §14 Report Generator v1 LOCKED 2026-05-10 §14.9.2 (Cycle 1 RT-2a/2b/2c
+ Cycle 2 RT-C2-02 closures).

Trigger: a ``proposal_commitments.yaml`` row with ``status: PROMOTED`` has
NO corresponding draft section addressing it.

Sub-tags (canonical at §14 v1 LOCK):

* ``.empty_promoted_set`` — proposal_commitments has zero PROMOTED rows;
  PRE pre-track-dispatch fail-closed (nothing to report against).
* ``.commitment_required_subsection_missing`` — PROMOTED commitment's
  ``required_sub_sections`` includes a sub-section NOT in
  ``sub_sections_authored``. FAIL-CLOSED per RT-2b.
* ``.commitment_evaluation_criterion_unaddressed`` — PROMOTED commitment's
  ``evaluation_criteria`` includes a numeric field with no metrics_table
  cell OR a narrative field with no narrative paragraph. FAIL-CLOSED per RT-2b.
* ``.commitment_period_n_not_due_yet`` — PROMOTED commitment is for a
  future period; operator may suppress via signed waiver up to a cap.
* ``.commitment_waiver_unsigned`` — operator attempted not-due-yet
  suppression but the corresponding ``<commitment_id>.signed.yaml`` waiver
  file is missing OR Ed25519 signature does not verify. FAIL-CLOSED.
* ``.commitment_waiver_cap_exceeded`` — more waivers than the
  ``len(promoted_commitments) - 1`` cap permits (would result in zero
  commitments addressed; vacuous reports structurally forbidden).
* ``.commitment_id_invalid_format`` — RT-C2-02: commitment_id failed the
  ``^[A-Z0-9_-]+$`` safe-identifier regex. PRE pre-track-dispatch
  fail-closed BEFORE any filesystem operation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Final, Mapping, Optional, Sequence

from pipeline.logician.gates._report_protocols import (
    PromotedCommitmentRow,
    WaiverRecord,
)
from pipeline.orchestrator.seats.report_generator._commitment_id import (
    is_safe_commitment_id,
)

F_REPORT_COMMITMENT_MISSED: Final[str] = "F-REPORT-COMMITMENT-MISSED"

SUB_TAG_EMPTY_PROMOTED_SET: Final[str] = ".empty_promoted_set"
SUB_TAG_COMMITMENT_REQUIRED_SUBSECTION_MISSING: Final[str] = (
    ".commitment_required_subsection_missing"
)
SUB_TAG_COMMITMENT_EVALUATION_CRITERION_UNADDRESSED: Final[str] = (
    ".commitment_evaluation_criterion_unaddressed"
)
SUB_TAG_COMMITMENT_PERIOD_N_NOT_DUE_YET: Final[str] = (
    ".commitment_period_n_not_due_yet"
)
SUB_TAG_COMMITMENT_WAIVER_UNSIGNED: Final[str] = ".commitment_waiver_unsigned"
SUB_TAG_COMMITMENT_WAIVER_CAP_EXCEEDED: Final[str] = ".commitment_waiver_cap_exceeded"
SUB_TAG_COMMITMENT_ID_INVALID_FORMAT: Final[str] = ".commitment_id_invalid_format"


@dataclass(frozen=True, kw_only=True)
class CommitmentMissedFinding:
    """One sub-tag firing inside the commitment-missed verdict."""

    sub_tag: str
    commitment_id: Optional[str]
    detail: str


@dataclass(frozen=True, kw_only=True)
class CommitmentMissedResult:
    """Run-all-then-collect verdict per §14.9.0 Cycle 1 RT-10a closure."""

    success: bool
    failure_code: Optional[str]
    findings: tuple[CommitmentMissedFinding, ...] = field(default_factory=tuple)

    @property
    def fired_sub_tags(self) -> tuple[str, ...]:
        seen: list[str] = []
        for f in self.findings:
            if f.sub_tag not in seen:
                seen.append(f.sub_tag)
        return tuple(seen)


def _addressing_index(
    *,
    commitment_id: str,
    claim_commitment_links: Mapping[str, tuple[str, ...]],
) -> set[str]:
    """Returns the set of sub_section names where any claim links to this commitment_id.

    ``claim_commitment_links`` maps commitment_id → tuple of sub_section
    names where at least one claim_evidence_map entry's
    proposal_commitments source carries this commitment_id.
    """
    return set(claim_commitment_links.get(commitment_id, ()))


def _criteria_addressed(
    *,
    commitment_id: str,
    eval_criteria: Sequence[Mapping[str, object]],
    addressed_criteria: Mapping[str, frozenset[str]],
) -> tuple[Mapping[str, object], ...]:
    """Returns the evaluation_criteria entries with no addressing-element.

    ``addressed_criteria`` maps commitment_id → frozenset of evaluation-
    criterion ``field`` names that have a corresponding claim
    (metrics_table cell for numeric / narrative paragraph for narrative)
    in the draft.
    """
    addressed = addressed_criteria.get(commitment_id, frozenset())
    missing: list[Mapping[str, object]] = []
    for crit in eval_criteria:
        field_name = crit.get("field")
        if not isinstance(field_name, str):
            continue
        if field_name not in addressed:
            missing.append(crit)
    return tuple(missing)


def check_commitment_missed(
    *,
    promoted_commitments: Sequence[PromotedCommitmentRow],
    sub_sections_in_scope: tuple[str, ...],
    sub_sections_authored: tuple[str, ...],
    period_n: int,
    claim_commitment_links: Mapping[str, tuple[str, ...]],
    addressed_criteria: Mapping[str, frozenset[str]],
    waivers: Mapping[str, WaiverRecord],
) -> CommitmentMissedResult:
    """Walks PROMOTED commitments + checks coverage; collects all findings.

    Inputs:

    * ``promoted_commitments`` — caller pre-filtered list with status=PROMOTED.
    * ``sub_sections_in_scope`` — operator-tunable subset of v0.2 closed
      set (from ReportGeneratorRunInput).
    * ``sub_sections_authored`` — sub-sections actually drafted (from
      GrantReportBundle).
    * ``period_n`` — the current report period (used for
      ``period_n_not_due_yet`` detection against
      ``commitment.period_n_window``).
    * ``claim_commitment_links`` — caller assembles by walking the
      claim_evidence_map for proposal_commitments sources.
    * ``addressed_criteria`` — caller assembles by checking each
      evaluation_criterion against the draft (metrics_table cell match
      OR narrative paragraph match by field name).
    * ``waivers`` — per-commitment_id signed waiver records (caller
      verifies the Ed25519 signatures and packages into WaiverRecord).
    """
    findings: list[CommitmentMissedFinding] = []

    # PRE pre-track-dispatch — empty promoted set.
    if not promoted_commitments:
        findings.append(
            CommitmentMissedFinding(
                sub_tag=SUB_TAG_EMPTY_PROMOTED_SET,
                commitment_id=None,
                detail=(
                    "proposal_commitments.yaml has zero PROMOTED rows; nothing "
                    "to report against"
                ),
            )
        )
        return CommitmentMissedResult(
            success=False,
            failure_code=F_REPORT_COMMITMENT_MISSED,
            findings=tuple(findings),
        )

    # RT-C2-02 — commitment_id safe-identifier regex.
    safe_commitments: list[PromotedCommitmentRow] = []
    for row in promoted_commitments:
        if not is_safe_commitment_id(row.commitment_id):
            findings.append(
                CommitmentMissedFinding(
                    sub_tag=SUB_TAG_COMMITMENT_ID_INVALID_FORMAT,
                    commitment_id=row.commitment_id,
                    detail=(
                        f"commitment_id={row.commitment_id!r} fails safe-identifier "
                        f"regex (^[A-Z0-9_-]+$); RT-C2-02 fail-closed"
                    ),
                )
            )
        else:
            safe_commitments.append(row)

    # Cap on waivers: at least one commitment MUST be addressed (vacuous
    # reports forbidden per RT-2b).
    waiver_cap = max(0, len(safe_commitments) - 1)
    used_waivers: list[str] = []

    for row in safe_commitments:
        in_period = True
        if row.period_n_window is not None:
            start, end = row.period_n_window
            in_period = start <= period_n <= end

        if not in_period:
            # Future or past period — operator may suppress with a signed waiver
            waiver = waivers.get(row.commitment_id)
            if waiver is None:
                findings.append(
                    CommitmentMissedFinding(
                        sub_tag=SUB_TAG_COMMITMENT_PERIOD_N_NOT_DUE_YET,
                        commitment_id=row.commitment_id,
                        detail=(
                            f"commitment is for period window "
                            f"{row.period_n_window}; current period_n={period_n}; "
                            f"no waiver supplied"
                        ),
                    )
                )
                continue
            if not waiver.signature_valid:
                findings.append(
                    CommitmentMissedFinding(
                        sub_tag=SUB_TAG_COMMITMENT_WAIVER_UNSIGNED,
                        commitment_id=row.commitment_id,
                        detail=(
                            f"waiver signature invalid for commitment "
                            f"{row.commitment_id!r}"
                        ),
                    )
                )
                continue
            used_waivers.append(row.commitment_id)
            continue

        # In-period — check required_sub_sections coverage
        addressing_sub_sections = _addressing_index(
            commitment_id=row.commitment_id,
            claim_commitment_links=claim_commitment_links,
        )
        for required_subsec in row.required_sub_sections:
            if required_subsec not in sub_sections_authored:
                findings.append(
                    CommitmentMissedFinding(
                        sub_tag=SUB_TAG_COMMITMENT_REQUIRED_SUBSECTION_MISSING,
                        commitment_id=row.commitment_id,
                        detail=(
                            f"required sub_section={required_subsec!r} not in "
                            f"sub_sections_authored={list(sub_sections_authored)!r}"
                        ),
                    )
                )

        # Per-criterion addressing
        missing_crit = _criteria_addressed(
            commitment_id=row.commitment_id,
            eval_criteria=row.evaluation_criteria,
            addressed_criteria=addressed_criteria,
        )
        for crit in missing_crit:
            findings.append(
                CommitmentMissedFinding(
                    sub_tag=SUB_TAG_COMMITMENT_EVALUATION_CRITERION_UNADDRESSED,
                    commitment_id=row.commitment_id,
                    detail=(
                        f"evaluation_criterion field={crit.get('field')!r} "
                        f"(kind={crit.get('kind')!r}) not addressed in draft"
                    ),
                )
            )

    if len(used_waivers) > waiver_cap:
        findings.append(
            CommitmentMissedFinding(
                sub_tag=SUB_TAG_COMMITMENT_WAIVER_CAP_EXCEEDED,
                commitment_id=None,
                detail=(
                    f"used_waivers={len(used_waivers)} > cap={waiver_cap} "
                    f"(promoted={len(safe_commitments)}); vacuous reports forbidden"
                ),
            )
        )

    if findings:
        return CommitmentMissedResult(
            success=False,
            failure_code=F_REPORT_COMMITMENT_MISSED,
            findings=tuple(findings),
        )
    return CommitmentMissedResult(
        success=True,
        failure_code=None,
        findings=(),
    )


__all__ = [
    "CommitmentMissedFinding",
    "CommitmentMissedResult",
    "F_REPORT_COMMITMENT_MISSED",
    "SUB_TAG_COMMITMENT_EVALUATION_CRITERION_UNADDRESSED",
    "SUB_TAG_COMMITMENT_ID_INVALID_FORMAT",
    "SUB_TAG_COMMITMENT_PERIOD_N_NOT_DUE_YET",
    "SUB_TAG_COMMITMENT_REQUIRED_SUBSECTION_MISSING",
    "SUB_TAG_COMMITMENT_WAIVER_CAP_EXCEEDED",
    "SUB_TAG_COMMITMENT_WAIVER_UNSIGNED",
    "SUB_TAG_EMPTY_PROMOTED_SET",
    "check_commitment_missed",
]
