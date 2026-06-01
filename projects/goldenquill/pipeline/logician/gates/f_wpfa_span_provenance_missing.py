"""F-WPFA-SPAN-PROVENANCE-MISSING — PRE-emission gate. [§5.1.WPFA.6]

Trigger: any quantitative claim in the receipt (``actual.dollars_total``,
per-model row, ``counterfactual.*``, ``delta.*``, PDF rendered claim)
does not carry an originating ``trace_id`` / ``span_id`` in
``span_provenance.per_claim_span_ids``.

Sibling pattern (per Path B naming reconciliation,
``pipeline/planning/f_reflection_f_wpfa_naming_reconciliation_2026-05-10.md``):
forthcoming ``F-PACKET-SPAN-PROVENANCE-MISSING`` covers the Reflection
Packet artifact's analogous discipline. F-REFLECTION-* family (Archivist
sub-mode) does NOT contain a SPAN-PROVENANCE-MISSING code.

Sub-tags: ``.no_trace_id``, ``.trace_id_unresolvable_in_logfire``,
``.claim_key_unmapped``, ``.pdf_claim_unlinked`` (per §17.7.5
auditability mandate; folded F-WPFA-PDF-AUDITABILITY-BROKEN per OQ-7).

M13 audited.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Iterable, Mapping, Optional


F_WPFA_SPAN_PROVENANCE_MISSING: Final[str] = "F-WPFA-SPAN-PROVENANCE-MISSING"

# Minimum claim keys every CycleReceipt MUST map. Extended by the v0.2
# water/CO2 emission path.
_REQUIRED_CLAIM_KEYS_V0_1: Final[frozenset[str]] = frozenset(
    {
        "actual.dollars_total",
        "actual.watt_hours_total",
        "counterfactual.dollars_total",
        "counterfactual.watt_hours_total",
        "delta.dollars_saved",
        "delta.watt_hours_saved",
    }
)


@dataclass(frozen=True, kw_only=True)
class SpanProvenanceMissingResult:
    success: bool
    failure_code: Optional[str]
    detail: str
    sub_tag: Optional[str] = None
    missing_claim_keys: tuple[str, ...] = ()


def check_f_wpfa_span_provenance_missing(
    *,
    per_claim_span_ids: Mapping[str, tuple[str, ...]],
    resolvable_span_ids: Iterable[str],
    required_claim_keys: frozenset[str] = _REQUIRED_CLAIM_KEYS_V0_1,
) -> SpanProvenanceMissingResult:
    """PRE-emission: every required claim key maps to >=1 resolvable span_id.

    ``resolvable_span_ids`` is the set of span_ids actually present in the
    Logfire export for the cycle. Span_ids referenced in
    ``per_claim_span_ids`` that are NOT in this set fail with
    ``.trace_id_unresolvable_in_logfire``.
    """
    if not isinstance(per_claim_span_ids, Mapping):
        return SpanProvenanceMissingResult(
            success=False,
            failure_code=F_WPFA_SPAN_PROVENANCE_MISSING,
            sub_tag="claim_key_unmapped",
            detail="per_claim_span_ids must be a Mapping",
        )
    resolvable_set = set(resolvable_span_ids)
    missing_required = sorted(
        k for k in required_claim_keys if k not in per_claim_span_ids
    )
    if missing_required:
        return SpanProvenanceMissingResult(
            success=False,
            failure_code=F_WPFA_SPAN_PROVENANCE_MISSING,
            sub_tag="claim_key_unmapped",
            detail=(
                f"required claim keys absent from per_claim_span_ids: "
                f"{missing_required!r}"
            ),
            missing_claim_keys=tuple(missing_required),
        )
    for ckey, sids in per_claim_span_ids.items():
        if not isinstance(sids, tuple) or not sids:
            return SpanProvenanceMissingResult(
                success=False,
                failure_code=F_WPFA_SPAN_PROVENANCE_MISSING,
                sub_tag="no_trace_id",
                detail=f"claim {ckey!r} maps to empty span_ids tuple",
                missing_claim_keys=(ckey,),
            )
        for s in sids:
            if not isinstance(s, str) or not s:
                return SpanProvenanceMissingResult(
                    success=False,
                    failure_code=F_WPFA_SPAN_PROVENANCE_MISSING,
                    sub_tag="no_trace_id",
                    detail=(
                        f"claim {ckey!r} contains empty/non-str span_id"
                    ),
                    missing_claim_keys=(ckey,),
                )
            if s not in resolvable_set:
                return SpanProvenanceMissingResult(
                    success=False,
                    failure_code=F_WPFA_SPAN_PROVENANCE_MISSING,
                    sub_tag="trace_id_unresolvable_in_logfire",
                    detail=(
                        f"claim {ckey!r} span_id {s!r} not present in "
                        "Logfire export"
                    ),
                    missing_claim_keys=(ckey,),
                )
    return SpanProvenanceMissingResult(
        success=True,
        failure_code=None,
        detail="all required claim keys map to resolvable Logfire span_ids",
    )


def check_pdf_claim_unlinked(
    *,
    pdf_rendered_claims: Iterable[str],
    per_claim_span_ids: Mapping[str, tuple[str, ...]],
) -> SpanProvenanceMissingResult:
    """PRE-PDF-emit: every claim rendered in the PDF must map per §17.7.5."""
    if not isinstance(per_claim_span_ids, Mapping):
        return SpanProvenanceMissingResult(
            success=False,
            failure_code=F_WPFA_SPAN_PROVENANCE_MISSING,
            sub_tag="pdf_claim_unlinked",
            detail="per_claim_span_ids must be a Mapping",
        )
    unlinked: list[str] = []
    for claim in pdf_rendered_claims:
        if not isinstance(claim, str) or not claim:
            continue
        if claim not in per_claim_span_ids:
            unlinked.append(claim)
    if unlinked:
        return SpanProvenanceMissingResult(
            success=False,
            failure_code=F_WPFA_SPAN_PROVENANCE_MISSING,
            sub_tag="pdf_claim_unlinked",
            detail=(
                f"PDF rendered claims missing span_provenance mapping: "
                f"{sorted(unlinked)!r}"
            ),
            missing_claim_keys=tuple(sorted(unlinked)),
        )
    return SpanProvenanceMissingResult(
        success=True,
        failure_code=None,
        detail="every PDF claim links to span_provenance",
    )


__all__ = [
    "F_WPFA_SPAN_PROVENANCE_MISSING",
    "SpanProvenanceMissingResult",
    "check_f_wpfa_span_provenance_missing",
    "check_pdf_claim_unlinked",
]
