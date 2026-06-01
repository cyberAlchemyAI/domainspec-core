"""F-REPORT-COMMITMENT-UNTRACED — POST scribe-equivalent + PRE pre-finalize.

Per §14 Report Generator v1 LOCKED 2026-05-10 §14.9.1 (Cycle 1 RT-1a/1b/1c
+ RT-6c + RT-7b + RT-8b closures; Cycle 2 RT-C2-08/09/10 closures).

Refuses report finalization when any claim in ``draft_<v>.md`` lacks an
entry in ``claim_evidence_map.yaml`` OR when any per-claim source has
drifted between author time and pre-finalize check time. Operator
cannot sign a draft with untraced claims; the gate fail-closes BEFORE
the operator-approval surface displays the draft for sign-off (RT-1b
closure).

Sub-tags (canonical at §14 v1 LOCK):

* ``.claim_text_no_map_entry``
* ``.numeric_claim_no_numeric_source``
* ``.narrative_claim_no_narrative_source``
* ``.photo_reference_no_photo_source``
* ``.beneficiary_reference_no_beneficiary_source``
* ``.beneficiary_reference_consent_tier_unverified``
* ``.source_value_drift`` — semantic-entailment failure per RT-1a
* ``.source_content_drift`` — content-hash mismatch
* ``.commitment_id_not_promoted``
* ``.kfr_source_canonical_drift`` — RT-1c atomic-snapshot mismatch
* ``.cross_period_signature_invalid`` — RT-4a SP0 flag signature failure
* ``.draft_post_sign_mutation_attempt`` — RT-8b post-sign mutation
* ``.prior_period_map_integrity_failure`` — RT-C2-09 prior-period tamper
* ``.narrative_paraphrase_unflagged`` — RT-C2-10 verbatim-or-paraphrase contract

The predicate body composes ``_entailment.check_numeric_entailment`` +
``_entailment.check_narrative_entailment`` for the semantic-entailment
check; substrate I/O (operational-data re-read, KFR atomic snapshot)
is performed by the caller and supplied via ``SourceResolutionAtFinalize``
pre-parsed inputs.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Final, Mapping, Optional, Sequence

from pipeline.logician.gates._report_protocols import (
    CaptionResolutionAtFinalize,
    DraftIntegrityAtFinalize,
    PriorPeriodMapIntegrity,
    SourceResolutionAtFinalize,
)
from pipeline.orchestrator.seats.report_generator._entailment import (
    check_narrative_entailment,
    check_numeric_entailment,
)
from pipeline.orchestrator.seats.report_generator._schemas import (
    PROPOSAL_COMMITMENT_STATUS_PROMOTED,
    ClaimEntry,
    ClaimEvidenceMap,
    SourceRef,
)

F_REPORT_COMMITMENT_UNTRACED: Final[str] = "F-REPORT-COMMITMENT-UNTRACED"

SUB_TAG_CLAIM_TEXT_NO_MAP_ENTRY: Final[str] = ".claim_text_no_map_entry"
SUB_TAG_NUMERIC_CLAIM_NO_NUMERIC_SOURCE: Final[str] = ".numeric_claim_no_numeric_source"
SUB_TAG_NARRATIVE_CLAIM_NO_NARRATIVE_SOURCE: Final[str] = (
    ".narrative_claim_no_narrative_source"
)
SUB_TAG_PHOTO_REFERENCE_NO_PHOTO_SOURCE: Final[str] = ".photo_reference_no_photo_source"
SUB_TAG_BENEFICIARY_REFERENCE_NO_BENEFICIARY_SOURCE: Final[str] = (
    ".beneficiary_reference_no_beneficiary_source"
)
SUB_TAG_BENEFICIARY_REFERENCE_CONSENT_TIER_UNVERIFIED: Final[str] = (
    ".beneficiary_reference_consent_tier_unverified"
)
SUB_TAG_SOURCE_VALUE_DRIFT: Final[str] = ".source_value_drift"
SUB_TAG_SOURCE_CONTENT_DRIFT: Final[str] = ".source_content_drift"
SUB_TAG_COMMITMENT_ID_NOT_PROMOTED: Final[str] = ".commitment_id_not_promoted"
SUB_TAG_KFR_SOURCE_CANONICAL_DRIFT: Final[str] = ".kfr_source_canonical_drift"
SUB_TAG_CROSS_PERIOD_SIGNATURE_INVALID: Final[str] = ".cross_period_signature_invalid"
SUB_TAG_DRAFT_POST_SIGN_MUTATION_ATTEMPT: Final[str] = (
    ".draft_post_sign_mutation_attempt"
)
SUB_TAG_PRIOR_PERIOD_MAP_INTEGRITY_FAILURE: Final[str] = (
    ".prior_period_map_integrity_failure"
)
SUB_TAG_NARRATIVE_PARAPHRASE_UNFLAGGED: Final[str] = ".narrative_paraphrase_unflagged"


# Per-claim-kind source-kind admissibility set (per §14.5.1 invariants).
_ADMISSIBLE_SOURCES_FOR_CLAIM_KIND: Final[Mapping[str, frozenset[str]]] = {
    "numeric": frozenset({"operational_data", "kfr"}),
    "financial": frozenset({"operational_data", "kfr"}),
    "narrative": frozenset({"operational_data", "proposal_commitments"}),
    "photo_reference": frozenset({"operational_data"}),
    "beneficiary_reference": frozenset({"operational_data"}),
    "timeline_reference": frozenset({"operational_data"}),
}


@dataclass(frozen=True, kw_only=True)
class CommitmentUntracedFinding:
    """One sub-tag firing inside the consolidated commitment-untraced result."""

    sub_tag: str
    claim_id: Optional[str]
    source_idx: Optional[int]
    detail: str


@dataclass(frozen=True, kw_only=True)
class CommitmentUntracedResult:
    """Run-all-then-collect verdict per §14.9.0 Cycle 1 RT-10a closure.

    ``success=True`` iff zero findings fired across every claim + every
    source + draft integrity + prior-period integrity (when applicable).
    Caller routes the comprehensive findings list to the operator UI
    ranked by severity.
    """

    success: bool
    failure_code: Optional[str]
    findings: tuple[CommitmentUntracedFinding, ...] = field(default_factory=tuple)

    @property
    def fired_sub_tags(self) -> tuple[str, ...]:
        """Deterministic-ordered tuple of unique sub-tags that fired."""
        seen: list[str] = []
        for f in self.findings:
            if f.sub_tag not in seen:
                seen.append(f.sub_tag)
        return tuple(seen)


def _resolutions_for_claim(
    claim: ClaimEntry,
    resolutions: Mapping[tuple[str, int], SourceResolutionAtFinalize],
) -> tuple[Optional[SourceResolutionAtFinalize], ...]:
    """Look up the resolution for each source_idx of a claim."""
    return tuple(
        resolutions.get((claim.claim_id, idx)) for idx in range(len(claim.sources))
    )


def _check_per_claim_kind_source_admissibility(
    claim: ClaimEntry,
) -> Optional[CommitmentUntracedFinding]:
    """Verify at least one source matches the per-kind admissibility set."""
    admissible = _ADMISSIBLE_SOURCES_FOR_CLAIM_KIND.get(claim.claim_kind, frozenset())
    has_admissible = any(s.kind in admissible for s in claim.sources)
    if has_admissible:
        return None
    if claim.claim_kind in ("numeric", "financial"):
        return CommitmentUntracedFinding(
            sub_tag=SUB_TAG_NUMERIC_CLAIM_NO_NUMERIC_SOURCE,
            claim_id=claim.claim_id,
            source_idx=None,
            detail=(
                f"claim_kind={claim.claim_kind!r} has no source in "
                f"{sorted(admissible)}"
            ),
        )
    if claim.claim_kind == "narrative":
        return CommitmentUntracedFinding(
            sub_tag=SUB_TAG_NARRATIVE_CLAIM_NO_NARRATIVE_SOURCE,
            claim_id=claim.claim_id,
            source_idx=None,
            detail=(
                f"narrative claim has no source in {sorted(admissible)}"
            ),
        )
    if claim.claim_kind == "photo_reference":
        return CommitmentUntracedFinding(
            sub_tag=SUB_TAG_PHOTO_REFERENCE_NO_PHOTO_SOURCE,
            claim_id=claim.claim_id,
            source_idx=None,
            detail="photo_reference claim has no operational_data photos source",
        )
    if claim.claim_kind == "beneficiary_reference":
        return CommitmentUntracedFinding(
            sub_tag=SUB_TAG_BENEFICIARY_REFERENCE_NO_BENEFICIARY_SOURCE,
            claim_id=claim.claim_id,
            source_idx=None,
            detail="beneficiary_reference claim has no operational_data source",
        )
    return None  # timeline_reference: no specific sub-tag at v0.2 first ship


def _check_source_content_drift(
    claim: ClaimEntry,
    src_idx: int,
    src: SourceRef,
    resolution: SourceResolutionAtFinalize,
) -> Optional[CommitmentUntracedFinding]:
    """Verify source_content_sha3_512 in map matches resolution.current_content_sha3_512."""
    if src.kind not in ("operational_data", "kfr", "benchmarks"):
        return None  # proposal_commitments has no content_sha; covered elsewhere
    if not resolution.present:
        return CommitmentUntracedFinding(
            sub_tag=SUB_TAG_SOURCE_CONTENT_DRIFT,
            claim_id=claim.claim_id,
            source_idx=src_idx,
            detail=(
                f"source kind={src.kind} not readable at finalize "
                f"(read_error={resolution.read_error!r})"
            ),
        )
    if resolution.current_content_sha3_512 != src.source_content_sha3_512:
        return CommitmentUntracedFinding(
            sub_tag=SUB_TAG_SOURCE_CONTENT_DRIFT,
            claim_id=claim.claim_id,
            source_idx=src_idx,
            detail=(
                f"content drift: author={src.source_content_sha3_512[:16] if src.source_content_sha3_512 else None}…"
                f" vs finalize={(resolution.current_content_sha3_512 or '')[:16]}…"
            ),
        )
    return None


def _check_kfr_atomic_snapshot(
    claim: ClaimEntry,
    src_idx: int,
    src: SourceRef,
    resolution: SourceResolutionAtFinalize,
) -> Optional[CommitmentUntracedFinding]:
    """RT-1c closure — KFR atomic-snapshot id MUST match between author + finalize."""
    if src.kind != "kfr":
        return None
    if not resolution.present:
        return None  # content-drift check fires earlier
    if (
        src.kfr_atomic_snapshot_id is None
        or resolution.current_kfr_atomic_snapshot_id is None
        or src.kfr_atomic_snapshot_id != resolution.current_kfr_atomic_snapshot_id
    ):
        return CommitmentUntracedFinding(
            sub_tag=SUB_TAG_KFR_SOURCE_CANONICAL_DRIFT,
            claim_id=claim.claim_id,
            source_idx=src_idx,
            detail=(
                f"kfr atomic snapshot drift: author={src.kfr_atomic_snapshot_id!r} "
                f"finalize={resolution.current_kfr_atomic_snapshot_id!r}"
            ),
        )
    return None


def _check_commitment_status_still_promoted(
    claim: ClaimEntry,
    src_idx: int,
    src: SourceRef,
    resolution: SourceResolutionAtFinalize,
) -> Optional[CommitmentUntracedFinding]:
    """RT-1a — proposal_commitments source MUST still be PROMOTED at finalize."""
    if src.kind != "proposal_commitments":
        return None
    if resolution.current_status != PROPOSAL_COMMITMENT_STATUS_PROMOTED:
        return CommitmentUntracedFinding(
            sub_tag=SUB_TAG_COMMITMENT_ID_NOT_PROMOTED,
            claim_id=claim.claim_id,
            source_idx=src_idx,
            detail=(
                f"commitment_id={src.commitment_id!r} status at finalize="
                f"{resolution.current_status!r}; required=PROMOTED"
            ),
        )
    return None


def _check_numeric_source_value(
    claim: ClaimEntry,
    src_idx: int,
    src: SourceRef,
    resolution: SourceResolutionAtFinalize,
) -> Optional[CommitmentUntracedFinding]:
    """RT-1a closure — semantic-entailment for numeric claim_kind: source_value MUST
    match in Decimal."""
    if claim.claim_kind not in ("numeric", "financial"):
        return None
    if src.kind not in ("operational_data", "kfr"):
        return None
    if not resolution.present:
        return None  # content-drift fires earlier
    author_value = src.source_value
    finalize_value = resolution.current_value
    if author_value is None or finalize_value is None:
        return None  # nothing to compare
    if not isinstance(author_value, Decimal) or not isinstance(finalize_value, Decimal):
        # Defense-in-depth — Decimal mandate per v7.0.4-M1.
        return CommitmentUntracedFinding(
            sub_tag=SUB_TAG_SOURCE_VALUE_DRIFT,
            claim_id=claim.claim_id,
            source_idx=src_idx,
            detail=(
                f"numeric source_value not Decimal: author_type="
                f"{type(author_value).__name__}, finalize_type="
                f"{type(finalize_value).__name__} (R-REPORT-DECIMAL-MANDATE)"
            ),
        )
    verdict = check_numeric_entailment(
        claim_value=author_value, source_value=finalize_value
    )
    if verdict.success:
        return None
    return CommitmentUntracedFinding(
        sub_tag=SUB_TAG_SOURCE_VALUE_DRIFT,
        claim_id=claim.claim_id,
        source_idx=src_idx,
        detail=verdict.detail,
    )


def _check_narrative_entailment(
    claim: ClaimEntry,
    narrative_source_texts: Mapping[str, tuple[str, ...]],
) -> Optional[CommitmentUntracedFinding]:
    """RT-1a + RT-C2-10 — narrative claims MUST be verbatim OR paraphrase-flagged.

    ``narrative_source_texts`` maps claim_id → tuple of source texts for the
    narrative_entries / proposal_commitments sources of that claim. Caller
    assembles by reading the operational-data narrative_entries +
    proposal_commitments rows referenced in ``claim.sources``.
    """
    if claim.claim_kind != "narrative":
        return None
    source_texts = narrative_source_texts.get(claim.claim_id, ())
    verdict = check_narrative_entailment(
        claim_text=claim.claim_text,
        source_texts=source_texts,
        editor_approved_paraphrase=claim.editor_approved_paraphrase,
    )
    if verdict.success and verdict.path != "ngram_advisory_only":
        return None
    if verdict.success:
        # ngram advisory PASS — caller decides whether to surface to operator
        return None
    return CommitmentUntracedFinding(
        sub_tag=SUB_TAG_NARRATIVE_PARAPHRASE_UNFLAGGED,
        claim_id=claim.claim_id,
        source_idx=None,
        detail=verdict.detail,
    )


def _check_photo_caption_and_bytes(
    claim: ClaimEntry,
    caption_resolution: Optional[CaptionResolutionAtFinalize],
) -> tuple[CommitmentUntracedFinding, ...]:
    """RT-7b closure — caption hash AND photo bytes hash re-checked at finalize."""
    if claim.claim_kind != "photo_reference":
        return ()
    findings: list[CommitmentUntracedFinding] = []
    if caption_resolution is None:
        findings.append(
            CommitmentUntracedFinding(
                sub_tag=SUB_TAG_SOURCE_CONTENT_DRIFT,
                claim_id=claim.claim_id,
                source_idx=None,
                detail="caption_resolution missing at finalize",
            )
        )
        return tuple(findings)
    if claim.caption_text_sha3_512 != caption_resolution.caption_text_sha3_512_at_finalize:
        findings.append(
            CommitmentUntracedFinding(
                sub_tag=SUB_TAG_SOURCE_CONTENT_DRIFT,
                claim_id=claim.claim_id,
                source_idx=None,
                detail=(
                    f"caption hash drift: author="
                    f"{(claim.caption_text_sha3_512 or '')[:16]}… vs finalize="
                    f"{(caption_resolution.caption_text_sha3_512_at_finalize or '')[:16]}…"
                ),
            )
        )
    return tuple(findings)


def _check_beneficiary_consent_tier_verified(
    claim: ClaimEntry,
    resolutions: tuple[Optional[SourceResolutionAtFinalize], ...],
) -> Optional[CommitmentUntracedFinding]:
    """RT-6c — beneficiary_reference claims require consent_tier_history_at_read_utc
    on the ClaimEntry AND signed-valid tier history at the resolution layer."""
    if claim.claim_kind != "beneficiary_reference":
        return None
    if not claim.consent_tier_history_at_read_utc:
        return CommitmentUntracedFinding(
            sub_tag=SUB_TAG_BENEFICIARY_REFERENCE_CONSENT_TIER_UNVERIFIED,
            claim_id=claim.claim_id,
            source_idx=None,
            detail="beneficiary_reference claim missing consent_tier_history_at_read_utc",
        )
    for src_idx, (src, res) in enumerate(zip(claim.sources, resolutions)):
        if src.kind != "operational_data" or src.sub_kind != "beneficiary_records":
            continue
        if res is None or res.current_consent_tier_history_signed_valid is not True:
            return CommitmentUntracedFinding(
                sub_tag=SUB_TAG_BENEFICIARY_REFERENCE_CONSENT_TIER_UNVERIFIED,
                claim_id=claim.claim_id,
                source_idx=src_idx,
                detail=(
                    "beneficiary_records consent_tier_history signed-valid check "
                    "missing or False"
                ),
            )
    return None


def check_commitment_untraced(
    *,
    claim_evidence_map: ClaimEvidenceMap,
    source_resolutions: Mapping[tuple[str, int], SourceResolutionAtFinalize],
    narrative_source_texts: Mapping[str, tuple[str, ...]],
    caption_resolutions: Mapping[str, CaptionResolutionAtFinalize],
    draft_integrity: DraftIntegrityAtFinalize,
    prior_period_integrity: Optional[PriorPeriodMapIntegrity] = None,
) -> CommitmentUntracedResult:
    """Run all F-REPORT-COMMITMENT-UNTRACED sub-checks; collect every fired sub-tag.

    The run-all-then-collect semantics is the RT-10a closure pattern —
    operator receives the comprehensive failure-code list ranked by
    severity for actionable prioritization.

    The caller (``report_generator.pre_gate.pre_finalize_consolidated.v1``)
    is responsible for:

    1. Re-reading each source listed in claim_evidence_map.claims to
       produce ``source_resolutions`` (key = (claim_id, source_idx)).
    2. Assembling ``narrative_source_texts`` for narrative claims by
       reading the operational_data narrative_entries text fields +
       proposal_commitments commitment_text fields.
    3. Hashing the photo bytes + caption text for each
       photo_reference claim into ``caption_resolutions``.
    4. Re-reading the draft markdown file to produce ``draft_integrity``.
    5. When SP0 ``accept_signed_prior_period_claim_evidence_map=True``,
       computing ``prior_period_integrity``.
    """
    findings: list[CommitmentUntracedFinding] = []

    # Draft post-sign mutation (RT-8b)
    if (
        draft_integrity.post_sign_read
        and draft_integrity.draft_content_sha3_512_at_finalize
        != claim_evidence_map.draft_content_sha3_512
    ):
        findings.append(
            CommitmentUntracedFinding(
                sub_tag=SUB_TAG_DRAFT_POST_SIGN_MUTATION_ATTEMPT,
                claim_id=None,
                source_idx=None,
                detail=(
                    f"draft_content_sha3_512 drift: map="
                    f"{claim_evidence_map.draft_content_sha3_512[:16]}… vs finalize="
                    f"{draft_integrity.draft_content_sha3_512_at_finalize[:16]}…"
                ),
            )
        )

    # Prior-period integrity (RT-4a + RT-4b + RT-C2-09)
    if prior_period_integrity is not None:
        if not prior_period_integrity.sp0_signature_valid:
            findings.append(
                CommitmentUntracedFinding(
                    sub_tag=SUB_TAG_CROSS_PERIOD_SIGNATURE_INVALID,
                    claim_id=None,
                    source_idx=None,
                    detail=(
                        f"SP0 flag signature invalid at prior period "
                        f"{prior_period_integrity.prior_period_n}"
                    ),
                )
            )
        if not prior_period_integrity.map_content_sha3_512_matches_signature_record:
            findings.append(
                CommitmentUntracedFinding(
                    sub_tag=SUB_TAG_PRIOR_PERIOD_MAP_INTEGRITY_FAILURE,
                    claim_id=None,
                    source_idx=None,
                    detail=(
                        f"prior-period map content drift detected at period "
                        f"{prior_period_integrity.prior_period_n}"
                    ),
                )
            )

    # Per-claim sub-checks
    for claim in claim_evidence_map.claims:
        # Per-kind source admissibility
        admiss = _check_per_claim_kind_source_admissibility(claim)
        if admiss is not None:
            findings.append(admiss)

        resolutions = _resolutions_for_claim(claim, source_resolutions)

        for src_idx, (src, res) in enumerate(zip(claim.sources, resolutions)):
            if res is None:
                findings.append(
                    CommitmentUntracedFinding(
                        sub_tag=SUB_TAG_CLAIM_TEXT_NO_MAP_ENTRY,
                        claim_id=claim.claim_id,
                        source_idx=src_idx,
                        detail=(
                            f"no resolution supplied for "
                            f"({claim.claim_id!r}, {src_idx})"
                        ),
                    )
                )
                continue
            for finding in (
                _check_source_content_drift(claim, src_idx, src, res),
                _check_kfr_atomic_snapshot(claim, src_idx, src, res),
                _check_commitment_status_still_promoted(claim, src_idx, src, res),
                _check_numeric_source_value(claim, src_idx, src, res),
            ):
                if finding is not None:
                    findings.append(finding)

        # Narrative entailment (cross-source)
        narr = _check_narrative_entailment(claim, narrative_source_texts)
        if narr is not None:
            findings.append(narr)

        # Photo caption + bytes (RT-7b)
        findings.extend(
            _check_photo_caption_and_bytes(claim, caption_resolutions.get(claim.claim_id))
        )

        # Beneficiary consent_tier_history (RT-6c)
        ben = _check_beneficiary_consent_tier_verified(claim, resolutions)
        if ben is not None:
            findings.append(ben)

    if findings:
        return CommitmentUntracedResult(
            success=False,
            failure_code=F_REPORT_COMMITMENT_UNTRACED,
            findings=tuple(findings),
        )
    return CommitmentUntracedResult(
        success=True,
        failure_code=None,
        findings=(),
    )


__all__ = [
    "CommitmentUntracedFinding",
    "CommitmentUntracedResult",
    "F_REPORT_COMMITMENT_UNTRACED",
    "SUB_TAG_BENEFICIARY_REFERENCE_CONSENT_TIER_UNVERIFIED",
    "SUB_TAG_BENEFICIARY_REFERENCE_NO_BENEFICIARY_SOURCE",
    "SUB_TAG_CLAIM_TEXT_NO_MAP_ENTRY",
    "SUB_TAG_COMMITMENT_ID_NOT_PROMOTED",
    "SUB_TAG_CROSS_PERIOD_SIGNATURE_INVALID",
    "SUB_TAG_DRAFT_POST_SIGN_MUTATION_ATTEMPT",
    "SUB_TAG_KFR_SOURCE_CANONICAL_DRIFT",
    "SUB_TAG_NARRATIVE_CLAIM_NO_NARRATIVE_SOURCE",
    "SUB_TAG_NARRATIVE_PARAPHRASE_UNFLAGGED",
    "SUB_TAG_NUMERIC_CLAIM_NO_NUMERIC_SOURCE",
    "SUB_TAG_PHOTO_REFERENCE_NO_PHOTO_SOURCE",
    "SUB_TAG_PRIOR_PERIOD_MAP_INTEGRITY_FAILURE",
    "SUB_TAG_SOURCE_CONTENT_DRIFT",
    "SUB_TAG_SOURCE_VALUE_DRIFT",
    "check_commitment_untraced",
]
