"""F-REPORT-OUT-OF-SCOPE-DRIFT — POST judge-equivalent + Cedar at write path.

Per §14 Report Generator v1 LOCKED 2026-05-10 §14.9.3 (Cycle 1 RT-6a/6b/6c
+ RT-7a + Cycle 2 RT-C2-03 closures).

Trigger: a claim in ``draft_<v>.md`` exceeds the original proposal's
defined scope (Boundary Drift per Law 2 + Law 5).

Three-layer detection (AST-lint on prompt templates + runtime check
here + Cedar policy at write path).

Sub-tags (canonical at §14 v1 LOCK):

* ``.scope_tag_not_in_promoted_set`` — claim's scope-tag not in any
  PROMOTED commitment's scope-tag set.
* ``.cross_grant`` — claim references a different grant_id (Law 3
  composes with F-REPORT-CROSS-ORG-LEAK).
* ``.cross_org`` — claim references a different org_slug (Law 3
  structural enforcement; RT-4b prior-period cross-org closure).
* ``.cross_period`` — claim references different period_n without SP0
  approval.
* ``.beneficiary_consent_tier_violation`` — claim includes beneficiary
  detail at tier above the beneficiary's consent_tier (composes with
  F-CEDAR-PII-CONSENT-MISSING).
* ``.photo_consent_tier_violation`` — claim includes a photo whose
  consent_tier is ``internal_only``.
* ``.photo_consent_tier_violation.cross_section_reference`` — RT-7a
  closure: text in a non-photo_gallery section references an
  internal_only / funder_only photo_id.
* ``.beneficiary_aggregate_identifying`` — RT-6a closure: aggregate
  count ≤ 2 without per-beneficiary-aggregate operator Ed25519 signature.
* ``.beneficiary_privacy_leak`` — RT-C2-03 closure: narrative mentions
  beneficiary by name where consent_tier disallows narrative inclusion.
* ``.runtime_scope_tag_extraction_failed`` — advisory: NER could not
  extract scope-tags from claim text.
"""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass, field
from typing import Final, Mapping, Optional, Sequence

from pipeline.logician.gates._report_protocols import (
    BeneficiaryNameDictionaryCallable,
    PromotedCommitmentRow,
    ScopeTagExtractorCallable,
)
from pipeline.orchestrator.seats.report_generator._schemas import (
    ClaimEntry,
    ClaimEvidenceMap,
    SourceRef,
)

F_REPORT_OUT_OF_SCOPE_DRIFT: Final[str] = "F-REPORT-OUT-OF-SCOPE-DRIFT"

SUB_TAG_SCOPE_TAG_NOT_IN_PROMOTED_SET: Final[str] = ".scope_tag_not_in_promoted_set"
SUB_TAG_CROSS_GRANT: Final[str] = ".cross_grant"
SUB_TAG_CROSS_ORG: Final[str] = ".cross_org"
SUB_TAG_CROSS_PERIOD: Final[str] = ".cross_period"
SUB_TAG_BENEFICIARY_CONSENT_TIER_VIOLATION: Final[str] = (
    ".beneficiary_consent_tier_violation"
)
SUB_TAG_PHOTO_CONSENT_TIER_VIOLATION: Final[str] = ".photo_consent_tier_violation"
SUB_TAG_PHOTO_CONSENT_TIER_VIOLATION_CROSS_SECTION: Final[str] = (
    ".photo_consent_tier_violation.cross_section_reference"
)
SUB_TAG_BENEFICIARY_AGGREGATE_IDENTIFYING: Final[str] = (
    ".beneficiary_aggregate_identifying"
)
SUB_TAG_BENEFICIARY_PRIVACY_LEAK: Final[str] = ".beneficiary_privacy_leak"
SUB_TAG_RUNTIME_SCOPE_TAG_EXTRACTION_FAILED: Final[str] = (
    ".runtime_scope_tag_extraction_failed"
)

# Per RT-6a closure: aggregate counts of <= this many beneficiaries
# trigger HIGH-advisory + require per-aggregate operator signature.
AGGREGATE_IDENTIFYING_THRESHOLD: Final[int] = 2

# Per §14.6.5: consent_tier text-inclusion floor.
_BENEFICIARY_NARRATIVE_ALLOWED_TIERS: Final[frozenset[str]] = frozenset(
    {"narrative-text-only"}
)
_BENEFICIARY_METRICS_ONLY_TIER: Final[str] = "metrics-only"
_BENEFICIARY_NO_NARRATIVE_TIER: Final[str] = "no-narrative"

# Per §14.6.4: photo consent_tier values that exclude from gallery.
_PHOTO_GALLERY_EXCLUDED_TIERS: Final[frozenset[str]] = frozenset(
    {"internal_only"}
)
# Tiers permitted in photo_gallery but NOT in other sub-sections (RT-7a).
_PHOTO_NON_GALLERY_RESTRICTED_TIERS: Final[frozenset[str]] = frozenset(
    {"internal_only", "funder_only"}
)


@dataclass(frozen=True, kw_only=True)
class OutOfScopeFinding:
    sub_tag: str
    claim_id: Optional[str]
    detail: str


@dataclass(frozen=True, kw_only=True)
class OutOfScopeResult:
    success: bool
    failure_code: Optional[str]
    findings: tuple[OutOfScopeFinding, ...] = field(default_factory=tuple)

    @property
    def fired_sub_tags(self) -> tuple[str, ...]:
        seen: list[str] = []
        for f in self.findings:
            if f.sub_tag not in seen:
                seen.append(f.sub_tag)
        return tuple(seen)


@dataclass(frozen=True, kw_only=True)
class AggregateBeneficiaryCountReference:
    """Per-aggregate-count reference + operator signature record.

    Caller assembles by walking metrics_table + beneficiary_section for
    aggregate-count claims; ``operator_aggregate_signature_valid`` is
    True when the per-aggregate Ed25519 signature verifies AND the
    aggregate count ≤ AGGREGATE_IDENTIFYING_THRESHOLD AND operator
    explicitly approved.
    """

    claim_id: str
    aggregate_count: int
    operator_aggregate_signature_valid: bool


@dataclass(frozen=True, kw_only=True)
class PhotoConsentInfo:
    """Per-photo_id consent_tier + which sub-section the claim resides in."""

    photo_id: str
    consent_tier: str
    referenced_in_sub_section: str


@dataclass(frozen=True, kw_only=True)
class BeneficiaryConsentInfo:
    """Per-beneficiary_id consent_tier referenced by a claim's source."""

    beneficiary_id: str
    claim_id: str
    consent_tier: str
    claim_sub_section: str


def _claim_is_aggregate_count(claim: ClaimEntry) -> bool:
    """Heuristic for aggregate-count claims (metrics_table or beneficiary_section
    numeric claim whose claim_text mentions a count phrasing)."""
    if claim.sub_section not in ("metrics_table", "beneficiary_section"):
        return False
    if claim.claim_kind not in ("numeric", "beneficiary_reference"):
        return False
    return True


def check_out_of_scope_drift(
    *,
    claim_evidence_map: ClaimEvidenceMap,
    promoted_commitments: Sequence[PromotedCommitmentRow],
    report_grant_id: str,
    report_org_slug: str,
    report_period_n: int,
    sp0_cross_period_authorized: bool,
    scope_tag_extractor: ScopeTagExtractorCallable,
    beneficiary_consent_infos: Sequence[BeneficiaryConsentInfo] = (),
    photo_consent_infos: Sequence[PhotoConsentInfo] = (),
    aggregate_references: Sequence[AggregateBeneficiaryCountReference] = (),
    beneficiary_name_dictionary: Optional[BeneficiaryNameDictionaryCallable] = None,
) -> OutOfScopeResult:
    """Walks every claim + every consent input; collects all findings.

    Caller assembles ``beneficiary_consent_infos`` /
    ``photo_consent_infos`` / ``aggregate_references`` by walking the
    operational-data sub-kinds (beneficiary_records + photos) referenced
    by claims; ``scope_tag_extractor`` is the deterministic NER callable.
    """
    findings: list[OutOfScopeFinding] = []

    # Promoted-set scope-tag union.
    promoted_scope_union: set[str] = set()
    for row in promoted_commitments:
        for tag in row.scope_tags:
            promoted_scope_union.add(tag)

    # Per-claim — scope-tag drift + cross-grant/org/period via source refs
    for claim in claim_evidence_map.claims:
        # Cross-grant / cross-org / cross-period detection via source paths.
        for src in claim.sources:
            _check_cross_grant_org_period(
                claim=claim,
                src=src,
                report_grant_id=report_grant_id,
                report_org_slug=report_org_slug,
                report_period_n=report_period_n,
                sp0_cross_period_authorized=sp0_cross_period_authorized,
                findings=findings,
            )

        # Scope-tag extraction
        try:
            extracted = scope_tag_extractor(claim.claim_text)
        except Exception as exc:
            findings.append(
                OutOfScopeFinding(
                    sub_tag=SUB_TAG_RUNTIME_SCOPE_TAG_EXTRACTION_FAILED,
                    claim_id=claim.claim_id,
                    detail=(
                        f"scope_tag_extractor raised {type(exc).__name__}: {exc!s}"
                    ),
                )
            )
            continue
        if not extracted:
            findings.append(
                OutOfScopeFinding(
                    sub_tag=SUB_TAG_RUNTIME_SCOPE_TAG_EXTRACTION_FAILED,
                    claim_id=claim.claim_id,
                    detail="scope_tag_extractor returned empty tuple",
                )
            )
            continue
        for tag in extracted:
            if tag not in promoted_scope_union:
                findings.append(
                    OutOfScopeFinding(
                        sub_tag=SUB_TAG_SCOPE_TAG_NOT_IN_PROMOTED_SET,
                        claim_id=claim.claim_id,
                        detail=(
                            f"scope_tag={tag!r} not in promoted union "
                            f"{sorted(promoted_scope_union)!r}"
                        ),
                    )
                )

    # Beneficiary consent_tier violation (claim text references beneficiary
    # at tier above their consent_tier).
    for info in beneficiary_consent_infos:
        if info.consent_tier in _BENEFICIARY_NARRATIVE_ALLOWED_TIERS:
            continue  # any narrative inclusion ok
        if info.consent_tier == _BENEFICIARY_METRICS_ONLY_TIER:
            # Allowed in aggregate-count claims; forbidden in beneficiary_section
            # text claims.
            if info.claim_sub_section in ("narrative", "beneficiary_section"):
                # Caller should have stripped before sending; if it didn't,
                # surface.
                findings.append(
                    OutOfScopeFinding(
                        sub_tag=SUB_TAG_BENEFICIARY_CONSENT_TIER_VIOLATION,
                        claim_id=info.claim_id,
                        detail=(
                            f"beneficiary_id={info.beneficiary_id!r} consent_tier="
                            f"metrics-only included in narrative-style sub_section="
                            f"{info.claim_sub_section!r}"
                        ),
                    )
                )
        elif info.consent_tier == _BENEFICIARY_NO_NARRATIVE_TIER:
            findings.append(
                OutOfScopeFinding(
                    sub_tag=SUB_TAG_BENEFICIARY_CONSENT_TIER_VIOLATION,
                    claim_id=info.claim_id,
                    detail=(
                        f"beneficiary_id={info.beneficiary_id!r} consent_tier="
                        f"no-narrative referenced in sub_section="
                        f"{info.claim_sub_section!r}"
                    ),
                )
            )
        else:
            findings.append(
                OutOfScopeFinding(
                    sub_tag=SUB_TAG_BENEFICIARY_CONSENT_TIER_VIOLATION,
                    claim_id=info.claim_id,
                    detail=(
                        f"beneficiary_id={info.beneficiary_id!r} consent_tier="
                        f"{info.consent_tier!r} (unknown tier; fail-closed)"
                    ),
                )
            )

    # Photo consent_tier violations
    for info in photo_consent_infos:
        if info.referenced_in_sub_section == "photo_gallery":
            if info.consent_tier in _PHOTO_GALLERY_EXCLUDED_TIERS:
                findings.append(
                    OutOfScopeFinding(
                        sub_tag=SUB_TAG_PHOTO_CONSENT_TIER_VIOLATION,
                        claim_id=None,
                        detail=(
                            f"photo_id={info.photo_id!r} consent_tier="
                            f"{info.consent_tier!r} excluded from photo_gallery"
                        ),
                    )
                )
        else:
            # RT-7a: cross-section reference
            if info.consent_tier in _PHOTO_NON_GALLERY_RESTRICTED_TIERS:
                findings.append(
                    OutOfScopeFinding(
                        sub_tag=SUB_TAG_PHOTO_CONSENT_TIER_VIOLATION_CROSS_SECTION,
                        claim_id=None,
                        detail=(
                            f"photo_id={info.photo_id!r} consent_tier="
                            f"{info.consent_tier!r} referenced in non-photo_gallery "
                            f"sub_section={info.referenced_in_sub_section!r}"
                        ),
                    )
                )

    # Aggregate-of-1 indirect identification (RT-6a)
    for agg in aggregate_references:
        if agg.aggregate_count <= AGGREGATE_IDENTIFYING_THRESHOLD:
            if not agg.operator_aggregate_signature_valid:
                findings.append(
                    OutOfScopeFinding(
                        sub_tag=SUB_TAG_BENEFICIARY_AGGREGATE_IDENTIFYING,
                        claim_id=agg.claim_id,
                        detail=(
                            f"aggregate_count={agg.aggregate_count} "
                            f"<= threshold={AGGREGATE_IDENTIFYING_THRESHOLD}; "
                            f"per-aggregate operator Ed25519 signature missing/invalid"
                        ),
                    )
                )

    # Beneficiary privacy leak via name match (RT-C2-03)
    if beneficiary_name_dictionary is not None:
        try:
            name_dict = beneficiary_name_dictionary()
        except Exception as exc:
            name_dict = None
            findings.append(
                OutOfScopeFinding(
                    sub_tag=SUB_TAG_RUNTIME_SCOPE_TAG_EXTRACTION_FAILED,
                    claim_id=None,
                    detail=(
                        f"beneficiary_name_dictionary raised {type(exc).__name__}: "
                        f"{exc!s}"
                    ),
                )
            )
        if name_dict is not None:
            for claim in claim_evidence_map.claims:
                if claim.sub_section not in ("narrative", "beneficiary_section"):
                    continue
                normalized_claim = unicodedata.normalize("NFC", claim.claim_text).lower()
                for beneficiary_id, (names, tier) in name_dict.items():
                    if tier in _BENEFICIARY_NARRATIVE_ALLOWED_TIERS:
                        continue
                    for name in names:
                        if not name:
                            continue
                        if name.lower() in normalized_claim:
                            findings.append(
                                OutOfScopeFinding(
                                    sub_tag=SUB_TAG_BENEFICIARY_PRIVACY_LEAK,
                                    claim_id=claim.claim_id,
                                    detail=(
                                        f"beneficiary_id={beneficiary_id!r} name "
                                        f"{name!r} appears in narrative claim "
                                        f"(consent_tier={tier!r} disallows)"
                                    ),
                                )
                            )

    if findings:
        return OutOfScopeResult(
            success=False,
            failure_code=F_REPORT_OUT_OF_SCOPE_DRIFT,
            findings=tuple(findings),
        )
    return OutOfScopeResult(
        success=True,
        failure_code=None,
        findings=(),
    )


def _check_cross_grant_org_period(
    *,
    claim: ClaimEntry,
    src: SourceRef,
    report_grant_id: str,
    report_org_slug: str,
    report_period_n: int,
    sp0_cross_period_authorized: bool,
    findings: list[OutOfScopeFinding],
) -> None:
    """Walk a source's path tokens to detect cross-grant / cross-org / cross-period."""
    if src.source_path is None:
        return
    parts = src.source_path.split("/")
    # Expected shape: orgs/<slug>/vault/.../grants/<grant_id>/period_<n>/...
    if "orgs" in parts:
        idx_orgs = parts.index("orgs")
        if idx_orgs + 1 < len(parts):
            org_in_path = parts[idx_orgs + 1]
            if org_in_path != report_org_slug:
                findings.append(
                    OutOfScopeFinding(
                        sub_tag=SUB_TAG_CROSS_ORG,
                        claim_id=claim.claim_id,
                        detail=(
                            f"source_path orgs/{org_in_path!r} != report org="
                            f"{report_org_slug!r}"
                        ),
                    )
                )
    if "grants" in parts:
        idx_g = parts.index("grants")
        if idx_g + 1 < len(parts):
            grant_in_path = parts[idx_g + 1]
            if grant_in_path != report_grant_id:
                findings.append(
                    OutOfScopeFinding(
                        sub_tag=SUB_TAG_CROSS_GRANT,
                        claim_id=claim.claim_id,
                        detail=(
                            f"source_path grants/{grant_in_path!r} != report "
                            f"grant={report_grant_id!r}"
                        ),
                    )
                )
    for part in parts:
        if part.startswith("period_"):
            tail = part[len("period_"):]
            if tail.isdigit():
                p_in_path = int(tail)
                if p_in_path != report_period_n and not sp0_cross_period_authorized:
                    findings.append(
                        OutOfScopeFinding(
                            sub_tag=SUB_TAG_CROSS_PERIOD,
                            claim_id=claim.claim_id,
                            detail=(
                                f"source_path period_{p_in_path} != report "
                                f"period_n={report_period_n} (SP0 not authorized)"
                            ),
                        )
                    )


__all__ = [
    "AGGREGATE_IDENTIFYING_THRESHOLD",
    "AggregateBeneficiaryCountReference",
    "BeneficiaryConsentInfo",
    "F_REPORT_OUT_OF_SCOPE_DRIFT",
    "OutOfScopeFinding",
    "OutOfScopeResult",
    "PhotoConsentInfo",
    "SUB_TAG_BENEFICIARY_AGGREGATE_IDENTIFYING",
    "SUB_TAG_BENEFICIARY_CONSENT_TIER_VIOLATION",
    "SUB_TAG_BENEFICIARY_PRIVACY_LEAK",
    "SUB_TAG_CROSS_GRANT",
    "SUB_TAG_CROSS_ORG",
    "SUB_TAG_CROSS_PERIOD",
    "SUB_TAG_PHOTO_CONSENT_TIER_VIOLATION",
    "SUB_TAG_PHOTO_CONSENT_TIER_VIOLATION_CROSS_SECTION",
    "SUB_TAG_RUNTIME_SCOPE_TAG_EXTRACTION_FAILED",
    "SUB_TAG_SCOPE_TAG_NOT_IN_PROMOTED_SET",
    "check_out_of_scope_drift",
]
