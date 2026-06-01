"""Frozen schemas for §14 Report Generator (claim_evidence_map subtree).

Per §14.5.1 + §14 v1 LOCK 2026-05-10. Field set mirrors the §0.5 v17
amendment rows 382 + 384 + 386-390 (schema + failure-code primitives).

Three closed enum sets are pinned at module level:

* ``CLAIM_KINDS`` — claim categorization per §14.5.1 (numeric / narrative
  / photo_reference / beneficiary_reference / timeline_reference /
  financial). Drives F-REPORT-COMMITMENT-UNTRACED per-kind source
  requirements.
* ``SOURCE_KINDS`` — claim-source categorization per §14.5.1
  (operational_data / proposal_commitments / kfr / benchmarks).
* ``OPERATIONAL_SUB_KINDS`` — §2 v7.2 operational-data sub-kinds the
  Report Generator reads (metrics / financials / photos /
  narrative_entries / timeline_of_activities / beneficiary_records /
  attachments).

The schemas are stored as YAML on disk (canonical-JSON-encoded YAML
per §14.5.1) and signed via the Ed25519 envelope at finalize time.
Construction-time validation enforces per-kind invariants — the source
dict carries kind-conditional fields.

Bundle invariants enforced PRE-gate by ``report_generator.pre_gate.
input_validation.v1`` per §0.5 v17 row 391.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Final, Optional, Union

# ---------------------------------------------------------------------------
# Pinned enum sets (per §14.5.1)
# ---------------------------------------------------------------------------


CLAIM_KINDS: Final[frozenset[str]] = frozenset(
    {
        "numeric",
        "narrative",
        "photo_reference",
        "beneficiary_reference",
        "timeline_reference",
        "financial",
    }
)

SOURCE_KINDS: Final[frozenset[str]] = frozenset(
    {
        "operational_data",
        "proposal_commitments",
        "kfr",
        "benchmarks",
    }
)

OPERATIONAL_SUB_KINDS: Final[frozenset[str]] = frozenset(
    {
        "metrics",
        "financials",
        "photos",
        "narrative_entries",
        "timeline_of_activities",
        "beneficiary_records",
        "attachments",
    }
)

# Per §14.6 — five sub-section names at v0.2 first ship.
SUB_SECTIONS_V0_2: Final[frozenset[str]] = frozenset(
    {
        "narrative",
        "metrics_table",
        "financial_summary",
        "photo_gallery",
        "beneficiary_section",
    }
)

# Per §11 v1 RT-05 closure / §14.4.1 — proposal_commitments rows are
# consumed by Report Generator ONLY when status == PROMOTED.
PROPOSAL_COMMITMENT_STATUS_PROMOTED: Final[str] = "PROMOTED"

# Per §14.5.1 RT-8c closure — claim_evidence_map_version is immutable
# per-map; v0.2 first ship uses single-map signing; v1.x candidate per
# OQ-REPORT-CLAIM-SIGNING-GRAIN bumps to per-claim signing.
CLAIM_EVIDENCE_MAP_VERSION_V0_2: Final[str] = "v0.2_first_ship_single_map_signing"

# Per §14.5.0 — bundle_state enum + operator_signature_status enum.
BUNDLE_STATE_DRAFT_PENDING: Final[str] = "DRAFT_PENDING_OPERATOR_SIGN"
BUNDLE_STATE_FINALIZED: Final[str] = "FINALIZED"
BUNDLE_STATES: Final[frozenset[str]] = frozenset(
    {BUNDLE_STATE_DRAFT_PENDING, BUNDLE_STATE_FINALIZED}
)

OPERATOR_SIG_STATUS_PENDING: Final[str] = "PENDING_OPERATOR_REVIEW"
OPERATOR_SIG_STATUS_SIGNED: Final[str] = "SIGNED"
OPERATOR_SIG_STATUSES: Final[frozenset[str]] = frozenset(
    {OPERATOR_SIG_STATUS_PENDING, OPERATOR_SIG_STATUS_SIGNED}
)

# Per §14.4.1 — proposal_commitments evaluation_criterion kind enum.
EVAL_CRITERION_KINDS: Final[frozenset[str]] = frozenset({"numeric", "narrative"})


# ---------------------------------------------------------------------------
# Frozen dataclasses
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True, kw_only=True)
class SourceRef:
    """Per §14.5.1 — one source-row entry inside a ``ClaimEntry.sources`` list.

    Field set is kind-conditional. Validation lives in
    ``__post_init__`` so any construction path catches the violation.

    Common fields (every kind):

    * ``kind`` — one of ``SOURCE_KINDS``

    operational_data fields:

    * ``sub_kind`` (required when kind == operational_data) — one of
      ``OPERATIONAL_SUB_KINDS``
    * ``source_path`` (required) — under
      ``orgs/<slug>/vault/operational/grants/<grant_id>/period_<n>/<sub_kind>/``
    * ``source_row_id`` (required) — stable per-row id within the file
    * ``source_content_sha3_512`` (required) — 128-hex SHA3-512 of the
      operational-data row at author time
    * ``source_value`` (required for numeric / financial claim_kind;
      typed as Decimal | str | int) — re-read at finalize to detect drift

    proposal_commitments fields:

    * ``commitment_id`` (required) — sanitized per
      ``_commitment_id.sanitize_commitment_id`` BEFORE construction
    * ``commitment_status`` (required, MUST be "PROMOTED")
    * ``scope_tags_at_commitment`` (required tuple) — scope_tags captured
      at author time

    kfr fields:

    * ``source_path`` (required) — KFR canonical register path
    * ``source_row_id`` (required) — KFR row id
    * ``source_content_sha3_512`` (required) — KFR canonical-signed hash
    * ``source_value`` (required for numeric claims)
    * ``kfr_atomic_snapshot_id`` (required per RT-1c closure) — atomic
      snapshot id captured at author-time KFR read

    benchmarks fields:

    * ``source_path`` (required) — benchmark register path
    * ``source_row_id`` (required) — benchmark row id
    * ``source_content_sha3_512`` (required)
    * ``source_value`` (optional)
    """

    kind: str

    # Common to operational_data / kfr / benchmarks
    source_path: Optional[str] = None
    source_row_id: Optional[str] = None
    source_content_sha3_512: Optional[str] = None
    source_value: Optional[Union[Decimal, str, int]] = None

    # operational_data-specific
    sub_kind: Optional[str] = None

    # proposal_commitments-specific
    commitment_id: Optional[str] = None
    commitment_status: Optional[str] = None
    scope_tags_at_commitment: tuple[str, ...] = field(default_factory=tuple)

    # kfr-specific (RT-1c closure)
    kfr_atomic_snapshot_id: Optional[str] = None

    def __post_init__(self) -> None:
        if self.kind not in SOURCE_KINDS:
            raise ValueError(
                f"SourceRef.kind {self.kind!r} not in {sorted(SOURCE_KINDS)}"
            )
        if self.kind == "operational_data":
            if self.sub_kind not in OPERATIONAL_SUB_KINDS:
                raise ValueError(
                    f"operational_data SourceRef requires sub_kind in "
                    f"{sorted(OPERATIONAL_SUB_KINDS)}; got {self.sub_kind!r}"
                )
            for required in ("source_path", "source_row_id", "source_content_sha3_512"):
                if getattr(self, required) is None:
                    raise ValueError(
                        f"operational_data SourceRef requires {required}"
                    )
        elif self.kind == "proposal_commitments":
            if self.commitment_id is None:
                raise ValueError("proposal_commitments SourceRef requires commitment_id")
            if self.commitment_status != PROPOSAL_COMMITMENT_STATUS_PROMOTED:
                raise ValueError(
                    f"proposal_commitments SourceRef requires commitment_status="
                    f"{PROPOSAL_COMMITMENT_STATUS_PROMOTED!r}; got "
                    f"{self.commitment_status!r}"
                )
        elif self.kind == "kfr":
            for required in (
                "source_path",
                "source_row_id",
                "source_content_sha3_512",
                "kfr_atomic_snapshot_id",
            ):
                if getattr(self, required) is None:
                    raise ValueError(f"kfr SourceRef requires {required} (RT-1c closure)")
        elif self.kind == "benchmarks":
            for required in ("source_path", "source_row_id", "source_content_sha3_512"):
                if getattr(self, required) is None:
                    raise ValueError(f"benchmarks SourceRef requires {required}")


@dataclass(frozen=True, slots=True, kw_only=True)
class ClaimEntry:
    """Per §14.5.1 — one claim row in ``ClaimEvidenceMap.claims``.

    Per-claim-kind optional fields:

    * ``caption_text_sha3_512`` (only for ``claim_kind == photo_reference``;
      RT-7b closure) — hash of just the caption text in the draft, separate
      from photo-bytes hash.
    * ``consent_tier_history_at_read_utc`` (only for ``claim_kind ==
      beneficiary_reference``; RT-6c closure) — timestamp at which the
      beneficiary record's consent_tier_history was read.
    * ``editor_approved_paraphrase`` (only for ``claim_kind == narrative``;
      RT-C2-10 closure) — operator paraphrase flag bypassing verbatim
      requirement.
    """

    claim_id: str
    sub_section: str
    claim_text: str
    claim_kind: str
    sources: tuple[SourceRef, ...]

    # Per-kind optional extensions
    caption_text_sha3_512: Optional[str] = None
    consent_tier_history_at_read_utc: Optional[str] = None
    editor_approved_paraphrase: bool = False

    def __post_init__(self) -> None:
        if self.claim_kind not in CLAIM_KINDS:
            raise ValueError(
                f"ClaimEntry.claim_kind {self.claim_kind!r} not in {sorted(CLAIM_KINDS)}"
            )
        if self.sub_section not in SUB_SECTIONS_V0_2:
            raise ValueError(
                f"ClaimEntry.sub_section {self.sub_section!r} not in "
                f"{sorted(SUB_SECTIONS_V0_2)}"
            )
        if not isinstance(self.sources, tuple):
            raise TypeError(
                f"ClaimEntry.sources must be tuple, got {type(self.sources).__name__}"
            )
        if not self.sources:
            raise ValueError("ClaimEntry requires at least one source")
        for src in self.sources:
            if not isinstance(src, SourceRef):
                raise TypeError(
                    f"ClaimEntry.sources entries must be SourceRef, got "
                    f"{type(src).__name__}"
                )
        # Per-kind extension-field invariants
        if self.caption_text_sha3_512 is not None and self.claim_kind != "photo_reference":
            raise ValueError(
                "caption_text_sha3_512 is only valid on photo_reference claims"
            )
        if (
            self.consent_tier_history_at_read_utc is not None
            and self.claim_kind != "beneficiary_reference"
        ):
            raise ValueError(
                "consent_tier_history_at_read_utc is only valid on "
                "beneficiary_reference claims"
            )
        if self.editor_approved_paraphrase and self.claim_kind != "narrative":
            raise ValueError(
                "editor_approved_paraphrase is only valid on narrative claims"
            )


@dataclass(frozen=True, slots=True, kw_only=True)
class ClaimEvidenceMap:
    """Per §14.5.1 — top-level write-substrate.

    Mirrors the YAML on-disk schema. Canonical-JSON serialization via
    ``pipeline.orchestrator.seats.report_generator.claim_evidence_map.
    canonical_map_bytes``. Ed25519 operator signature covers canonical-JSON
    of all fields EXCEPT ``operator_signature`` and ``operator_signed_at_utc``.
    """

    schema_version: str  # "claim_evidence_map.v1"
    claim_evidence_map_version: str  # RT-8c closure pinned constant
    run_id: str
    org_slug: str
    grant_id: str
    period_n: int
    draft_path: str
    draft_version: int
    draft_content_sha3_512: str
    authored_at_utc: str
    authored_by_seat: str
    claims: tuple[ClaimEntry, ...]
    operator_signature_status: str
    operator_signature: str
    operator_signed_at_utc: str

    def __post_init__(self) -> None:
        if self.schema_version != "claim_evidence_map.v1":
            raise ValueError(
                f"schema_version must be 'claim_evidence_map.v1'; got "
                f"{self.schema_version!r}"
            )
        if self.claim_evidence_map_version != CLAIM_EVIDENCE_MAP_VERSION_V0_2:
            raise ValueError(
                f"claim_evidence_map_version must be "
                f"{CLAIM_EVIDENCE_MAP_VERSION_V0_2!r} at v0.2 first ship; got "
                f"{self.claim_evidence_map_version!r}"
            )
        if self.operator_signature_status not in OPERATOR_SIG_STATUSES:
            raise ValueError(
                f"operator_signature_status must be in "
                f"{sorted(OPERATOR_SIG_STATUSES)}; got "
                f"{self.operator_signature_status!r}"
            )
        if not isinstance(self.period_n, int) or self.period_n < 1:
            raise ValueError(f"period_n must be int >= 1; got {self.period_n!r}")
        if not isinstance(self.claims, tuple):
            raise TypeError(
                f"claims must be tuple, got {type(self.claims).__name__}"
            )
        for c in self.claims:
            if not isinstance(c, ClaimEntry):
                raise TypeError(
                    f"claims entries must be ClaimEntry, got {type(c).__name__}"
                )


@dataclass(frozen=True, slots=True, kw_only=True)
class ReportGeneratorRunInput:
    """Per §14.4.0 — input bundle invariants enforced PRE-gate by
    ``report_generator.pre_gate.input_validation.v1`` (per §0.5 v17 row 391)."""

    run_id: str
    org_slug: str
    grant_id: str
    period_n: int
    proposal_commitments_path: str
    reporting_template_path: str
    operational_data_root: str
    kfr_register_path: str
    funder_intelligence_root: str
    benchmarks_root: str
    sub_sections_in_scope: tuple[str, ...]
    trend_narrative_authorized: bool
    invoked_at_utc: str

    def __post_init__(self) -> None:
        if not isinstance(self.period_n, int) or self.period_n < 1:
            raise ValueError(f"period_n must be int >= 1; got {self.period_n!r}")
        if not isinstance(self.sub_sections_in_scope, tuple):
            raise TypeError(
                f"sub_sections_in_scope must be tuple, got "
                f"{type(self.sub_sections_in_scope).__name__}"
            )
        if not self.sub_sections_in_scope:
            raise ValueError("sub_sections_in_scope must be non-empty")
        for s in self.sub_sections_in_scope:
            if s not in SUB_SECTIONS_V0_2:
                raise ValueError(
                    f"sub_sections_in_scope entry {s!r} not in "
                    f"{sorted(SUB_SECTIONS_V0_2)}"
                )


@dataclass(frozen=True, slots=True, kw_only=True)
class GrantReportBundle:
    """Per §14.5.0 — output substrate. bundle_state transitions
    DRAFT_PENDING_OPERATOR_SIGN → FINALIZED only when operator signs."""

    run_id: str
    org_slug: str
    grant_id: str
    period_n: int
    draft_path: str
    draft_version: int
    claim_evidence_map_path: str
    scoring_dir: str
    proposal_commitments_consumed: tuple[str, ...]
    reporting_template_content_sha3_512: str
    sub_sections_authored: tuple[str, ...]
    operator_signature_status: str
    operator_signature: str
    operator_signed_at_utc: str
    finalized_at_utc: str
    bundle_state: str

    def __post_init__(self) -> None:
        if self.bundle_state not in BUNDLE_STATES:
            raise ValueError(
                f"bundle_state must be in {sorted(BUNDLE_STATES)}; got "
                f"{self.bundle_state!r}"
            )
        if self.operator_signature_status not in OPERATOR_SIG_STATUSES:
            raise ValueError(
                f"operator_signature_status must be in "
                f"{sorted(OPERATOR_SIG_STATUSES)}; got "
                f"{self.operator_signature_status!r}"
            )
        # bundle_state == FINALIZED requires SIGNED + non-empty signature/timestamp
        if self.bundle_state == BUNDLE_STATE_FINALIZED:
            if self.operator_signature_status != OPERATOR_SIG_STATUS_SIGNED:
                raise ValueError(
                    "bundle_state=FINALIZED requires operator_signature_status=SIGNED"
                )
            if not self.operator_signature:
                raise ValueError(
                    "bundle_state=FINALIZED requires non-empty operator_signature"
                )
            if not self.operator_signed_at_utc:
                raise ValueError(
                    "bundle_state=FINALIZED requires non-empty operator_signed_at_utc"
                )
            if not self.finalized_at_utc:
                raise ValueError(
                    "bundle_state=FINALIZED requires non-empty finalized_at_utc"
                )


__all__ = [
    "BUNDLE_STATES",
    "BUNDLE_STATE_DRAFT_PENDING",
    "BUNDLE_STATE_FINALIZED",
    "CLAIM_EVIDENCE_MAP_VERSION_V0_2",
    "CLAIM_KINDS",
    "ClaimEntry",
    "ClaimEvidenceMap",
    "EVAL_CRITERION_KINDS",
    "GrantReportBundle",
    "OPERATIONAL_SUB_KINDS",
    "OPERATOR_SIG_STATUSES",
    "OPERATOR_SIG_STATUS_PENDING",
    "OPERATOR_SIG_STATUS_SIGNED",
    "PROPOSAL_COMMITMENT_STATUS_PROMOTED",
    "ReportGeneratorRunInput",
    "SOURCE_KINDS",
    "SUB_SECTIONS_V0_2",
    "SourceRef",
]
