"""§14.6.5 beneficiary_section sub-section composer.

Reads: operational-data ``beneficiary_records`` sub-kind WITH Cedar PII
enforcement at the read path + ``reporting_template``
``beneficiary_section`` field requirements.

Per Cycle 1 RT-6a / RT-6b / RT-6c closures:

* RT-6a — aggregate-of-≤2 advisory: aggregate counts ≤
  :data:`AGGREGATE_IDENTIFYING_THRESHOLD` surface to operator via
  ``F-REPORT-OUT-OF-SCOPE-DRIFT.beneficiary_aggregate_identifying``.
* RT-6b — Cedar engine readiness check per-read (not module-init only);
  failure → :class:`CedarOperationalDenied`-like propagation.
* RT-6c — ``consent_tier_history_at_read_utc`` timestamp captured on
  every beneficiary_reference claim; pre-finalize re-checks for unsigned
  post-collection downgrade.

Per-beneficiary ``consent_tier`` gates inclusion:

* ``narrative-text-only`` floor for text inclusion.
* ``metrics-only`` allows aggregate count but no per-beneficiary text.
* ``no-narrative`` excludes the beneficiary entirely.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Optional, Sequence

from .._schemas import ClaimEntry, SourceRef
from ._base import (
    ClockCallable,
    ComposerError,
    HashBytesCallable,
    ScribeFieldSpec,
    ScribeProtocol,
    VaultReadIntentCallable,
    compute_claim_id,
)


_SUB_SECTION: str = "beneficiary_section"

# Per RT-6a closure — aggregate counts at or below this threshold surface
# operator-confirmation requirement.
AGGREGATE_IDENTIFYING_THRESHOLD: int = 2

# Per RT-C2-10 / §13 v1 enumeration — consent_tier enum at the §14 read path.
_TIER_NARRATIVE_TEXT_ONLY: str = "narrative-text-only"
_TIER_METRICS_ONLY: str = "metrics-only"
_TIER_NO_NARRATIVE: str = "no-narrative"
_TIER_OPERATOR_AUTHORIZED_IDENTIFIED: str = "operator-authorized-identified"
_TIER_ANONYMIZED: str = "anonymized"

# Tiers permitting per-beneficiary text inclusion.
_TIERS_PERMIT_TEXT: frozenset[str] = frozenset(
    {_TIER_NARRATIVE_TEXT_ONLY, _TIER_OPERATOR_AUTHORIZED_IDENTIFIED}
)


@dataclass(frozen=True, kw_only=True)
class BeneficiaryRecordRow:
    """Pre-parsed view of one operational-data ``beneficiary_records`` row.

    ``consent_tier`` is the §13 v1 RT-C2-10 enumeration (NOT the simpler
    §2 v7.2 BeneficiaryRecord 2-tier enum — the §13 layer extends to
    the 5-tier model the Report Generator reads).
    """

    record_id: str
    source_path: str
    beneficiary_opaque_id: str
    outcome_summary: str
    consent_tier: str
    content_sha3_512: str
    consent_tier_history_signed_valid: bool = True
    related_commitment_id: Optional[str] = None


@dataclass(frozen=True, kw_only=True)
class BeneficiarySectionDeps:
    read_beneficiary_records: VaultReadIntentCallable
    read_template_field_specs: VaultReadIntentCallable
    scribe: ScribeProtocol
    clock: ClockCallable
    hash_bytes: HashBytesCallable
    # Per RT-6b — Cedar engine readiness check at every read.
    cedar_engine_assert_ready: object = None  # callable () -> None, raises on fail


@dataclass(frozen=True, kw_only=True)
class BeneficiarySectionResult:
    markdown_fragment: str
    claims: tuple[ClaimEntry, ...]
    aggregate_count: int
    aggregate_identifying_advisory: bool


def compose_beneficiary_section(
    *,
    deps: BeneficiarySectionDeps,
    org_slug: str,
    grant_id: str,
    period_n: int,
    operational_data_root: str,
    reporting_template_path: str,
) -> BeneficiarySectionResult:
    """Compose ``beneficiary_section`` per §14.6.5.

    Composer-level invariants:

    1. Cedar engine readiness asserted BEFORE the read (RT-6b).
    2. Per-beneficiary ``consent_tier`` gates inclusion (RT-6a / RT-6c).
    3. Aggregate counts ≤ :data:`AGGREGATE_IDENTIFYING_THRESHOLD` flag
       the result's ``aggregate_identifying_advisory`` field.
    4. Every claim ``sub_section == "beneficiary_section"`` and
       ``claim_kind == "beneficiary_reference"``.
    5. Every claim has at least one operational_data source with
       ``sub_kind == "beneficiary_records"``.
    6. Per RT-6c — every claim carries ``consent_tier_history_at_read_utc``.
    """
    if period_n < 1:
        raise ComposerError(f"period_n must be >= 1; got {period_n!r}")

    # RT-6b — Cedar engine readiness check at every read.
    _assert_cedar_ready(deps.cedar_engine_assert_ready)

    _field_specs_raw = deps.read_template_field_specs(
        kind="reporting_template",
        path=reporting_template_path,
        sub_section=_SUB_SECTION,
    )

    records = _coerce_beneficiary_records(
        deps.read_beneficiary_records(
            kind="operational_data",
            sub_kind="beneficiary_records",
            path=f"{operational_data_root.rstrip('/')}/beneficiary_records",
            period_n=period_n,
        )
    )

    read_at_utc = deps.clock()
    if not isinstance(read_at_utc, str):
        raise ComposerError(
            f"clock() returned non-string: {type(read_at_utc).__name__}"
        )

    md_parts: list[str] = []
    claims: list[ClaimEntry] = []
    aggregate_count = 0
    excluded_no_narrative = 0

    for idx, record in enumerate(records):
        if record.consent_tier == _TIER_NO_NARRATIVE:
            excluded_no_narrative += 1
            continue
        if record.consent_tier == _TIER_ANONYMIZED:
            # Anonymized beneficiaries count in aggregate but do NOT
            # surface in per-beneficiary narrative text.
            aggregate_count += 1
            continue

        # RT-6c — consent_tier_history must be signed-valid; fail-closed
        # at compose time if the read indicates an unsigned downgrade.
        if not record.consent_tier_history_signed_valid:
            raise ComposerError(
                f"beneficiary_section composer: record {record.record_id!r} has "
                f"unsigned consent_tier_history downgrade (RT-6c)"
            )

        aggregate_count += 1
        if record.consent_tier == _TIER_METRICS_ONLY:
            # Counted but no per-beneficiary text.
            continue

        if record.consent_tier not in _TIERS_PERMIT_TEXT:
            # Defensive — unknown tier shouldn't reach text inclusion.
            raise ComposerError(
                f"beneficiary_section composer: record {record.record_id!r} "
                f"consent_tier={record.consent_tier!r} not in permitted-text "
                f"set {sorted(_TIERS_PERMIT_TEXT)!r}"
            )

        # Scribe drafts the per-beneficiary outcome paragraph.
        outcome_spec = ScribeFieldSpec(
            sub_section=_SUB_SECTION,
            field_name="beneficiary_outcome",
            kind="beneficiary_block",
        )
        drafted = deps.scribe(
            spec=outcome_spec,
            sources=(
                {
                    "kind": "operational_data",
                    "sub_kind": "beneficiary_records",
                    "record_id": record.record_id,
                    "beneficiary_opaque_id": record.beneficiary_opaque_id,
                    "outcome_summary": record.outcome_summary,
                    "consent_tier": record.consent_tier,
                },
            ),
        )
        if not isinstance(drafted, str):
            raise ComposerError(
                f"Scribe returned non-string for beneficiary_section: "
                f"{type(drafted).__name__}"
            )

        md_parts.append(f"- {drafted}")

        claim_id = compute_claim_id(
            sub_section=_SUB_SECTION,
            paragraph_index=idx,
            sentence_index=0,
            claim_text=drafted,
        )
        ref = SourceRef(
            kind="operational_data",
            sub_kind="beneficiary_records",
            source_path=record.source_path,
            source_row_id=record.record_id,
            source_content_sha3_512=record.content_sha3_512,
        )
        claims.append(
            ClaimEntry(
                claim_id=claim_id,
                sub_section=_SUB_SECTION,
                claim_text=drafted,
                claim_kind="beneficiary_reference",
                sources=(ref,),
                consent_tier_history_at_read_utc=read_at_utc,
            )
        )

    # Append aggregate-count footer (always present).
    md_parts.append(f"\n**Aggregate beneficiaries served:** {aggregate_count}")

    advisory = 0 < aggregate_count <= AGGREGATE_IDENTIFYING_THRESHOLD

    _validate_composer_invariants(claims=tuple(claims))

    return BeneficiarySectionResult(
        markdown_fragment="\n".join(md_parts) if md_parts else "_no beneficiaries to report_",
        claims=tuple(claims),
        aggregate_count=aggregate_count,
        aggregate_identifying_advisory=advisory,
    )


# ---------------------------------------------------------------------------
# Cedar readiness check (RT-6b)
# ---------------------------------------------------------------------------


def _assert_cedar_ready(assert_ready: object) -> None:
    """RT-6b — Cedar engine readiness check at every read.

    The injected ``cedar_engine_assert_ready`` callable performs the
    readiness verification. If absent, the composer falls back to the
    seat-module Cedar bootstrap engine. Failure raises
    :class:`pipeline.orchestrator.seats.report_generator._cedar_bootstrap.CriticalPolicyError`.
    """
    if assert_ready is not None:
        if not callable(assert_ready):
            raise ComposerError(
                "cedar_engine_assert_ready must be callable (RT-6b)"
            )
        assert_ready()
        return
    # Fallback — use the seat's bootstrap engine.
    from .._cedar_bootstrap import CriticalPolicyError, get_cedar_engine

    engine = get_cedar_engine()
    if engine.is_ready() is not True:
        raise CriticalPolicyError(
            "Cedar engine not ready at beneficiary_section read (RT-6b)"
        )


# ---------------------------------------------------------------------------
# Coercion helpers
# ---------------------------------------------------------------------------


def _coerce_beneficiary_records(raw: object) -> tuple[BeneficiaryRecordRow, ...]:
    if raw is None:
        return ()
    if not isinstance(raw, (list, tuple)):
        raise ComposerError(
            f"beneficiary_records must be list/tuple; got {type(raw).__name__}"
        )
    rows: list[BeneficiaryRecordRow] = []
    for idx, r in enumerate(raw):
        if isinstance(r, BeneficiaryRecordRow):
            rows.append(r)
            continue
        if not isinstance(r, Mapping):
            raise ComposerError(f"beneficiary_records[{idx}] not Mapping")
        try:
            rows.append(
                BeneficiaryRecordRow(
                    record_id=str(r["record_id"]),
                    source_path=str(r["source_path"]),
                    beneficiary_opaque_id=str(r["beneficiary_opaque_id"]),
                    outcome_summary=str(r["outcome_summary"]),
                    consent_tier=str(r["consent_tier"]),
                    content_sha3_512=str(r["content_sha3_512"]),
                    consent_tier_history_signed_valid=bool(
                        r.get("consent_tier_history_signed_valid", True)
                    ),
                    related_commitment_id=(
                        str(r["related_commitment_id"])
                        if r.get("related_commitment_id") is not None
                        else None
                    ),
                )
            )
        except KeyError as exc:
            raise ComposerError(
                f"beneficiary_records[{idx}] missing key {exc!s}"
            ) from exc
    return tuple(rows)


def _validate_composer_invariants(*, claims: tuple[ClaimEntry, ...]) -> None:
    for c in claims:
        if c.sub_section != _SUB_SECTION:
            raise ComposerError(
                f"beneficiary_section claim {c.claim_id!r} sub_section="
                f"{c.sub_section!r}"
            )
        if c.claim_kind != "beneficiary_reference":
            raise ComposerError(
                f"beneficiary_section claim {c.claim_id!r} claim_kind="
                f"{c.claim_kind!r}; expected 'beneficiary_reference'"
            )
        if c.consent_tier_history_at_read_utc is None:
            raise ComposerError(
                f"beneficiary_section claim {c.claim_id!r} missing "
                f"consent_tier_history_at_read_utc (RT-6c)"
            )
        if not c.sources:
            raise ComposerError(
                f"beneficiary_section claim {c.claim_id!r} has no sources"
            )


__all__ = [
    "AGGREGATE_IDENTIFYING_THRESHOLD",
    "BeneficiaryRecordRow",
    "BeneficiarySectionDeps",
    "BeneficiarySectionResult",
    "compose_beneficiary_section",
]
