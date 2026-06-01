"""Shared runtime-checkable Protocols + frozen result schemas for §14
Report Generator gate family (F-REPORT-COMMITMENT-UNTRACED,
F-REPORT-COMMITMENT-MISSED, F-REPORT-OUT-OF-SCOPE-DRIFT,
F-REPORT-NUMERIC-DRIFT, F-REPORT-TEMPLATE-MISMATCH).

Substrate I/O (operational-data sub-kind reads, KFR canonical re-reads,
proposal_commitments PROMOTED filter, reporting_template hash compare,
workspace-shared published-template + first-wave marker reads, waiver +
SP0 signature verifies) is performed BY THE CALLER (the report_mode
track runner / pre-finalize consolidated check callable). The gate
modules consume already-parsed inputs and emit deterministic
sub-tag-routed verdicts.

This separation mirrors §4 v2.2 + §13 v1 + §11 v1 + WS-L Slice 3
(F-CLASS-*) Logician discipline:

* gates never call ``open()`` (AST-lint R3 LOGICIAN_OPEN_BAN)
* gates never import ``hashlib`` / ``cryptography`` / ``nacl``
  (AST-lint R1 LOGICIAN_IMPORT_BAN)
* gates take pre-parsed dicts / frozen dataclasses / injected Protocols
* the orchestrator + seat-module substrate is the only sanctioned route
  to bytes / hashes / signatures
"""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Final, Mapping, Optional, Protocol, Union, runtime_checkable


# ---------------------------------------------------------------------------
# Source-resolution input substrate (caller-supplied; pre-parsed)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class SourceResolutionAtFinalize:
    """Per-source re-read result computed by the seat / orchestrator before
    invoking the F-REPORT-COMMITMENT-UNTRACED gate.

    The gate compares this against the ``SourceRef`` snapshot recorded in
    the ``ClaimEvidenceMap`` at Scribe author time.

    * ``present`` — caller resolved + read the source successfully.
    * ``current_content_sha3_512`` — re-computed at finalize; the gate
      compares to the map-recorded value to detect substrate drift
      (RT-1b closure surfaces operational-data-modified-post-Scribe).
    * ``current_value`` — for numeric / financial claims, the re-read
      value. Decimal mandate per v7.0.4-M1: numeric values MUST be
      decimal.Decimal. int/str permitted for non-numeric source kinds
      (benchmarks may carry textual labels).
    * ``current_status`` — for proposal_commitments sources; the gate
      requires this to remain "PROMOTED" at finalize (RT-1a
      .commitment_id_not_promoted).
    * ``current_kfr_atomic_snapshot_id`` — for kfr sources (RT-1c
      atomic-snapshot discipline); the gate fails if the snapshot id at
      finalize differs from the one captured at author time.
    * ``current_consent_tier`` — for beneficiary_records sub-kind reads;
      used by F-REPORT-OUT-OF-SCOPE-DRIFT.beneficiary_consent_tier_violation.
    * ``current_consent_tier_history_signed_valid`` — for
      beneficiary_records (RT-6c closure); the gate fails if any
      post-collection tier downgrade is unsigned.
    * ``read_error`` — opaque error class name when ``present`` is False.
    """

    claim_id: str
    source_idx: int
    source_kind: str

    present: bool = True
    read_error: Optional[str] = None

    current_content_sha3_512: Optional[str] = None
    current_value: Optional[Union[Decimal, str, int]] = None
    current_status: Optional[str] = None
    current_kfr_atomic_snapshot_id: Optional[str] = None
    current_consent_tier: Optional[str] = None
    current_consent_tier_history_signed_valid: Optional[bool] = None


@dataclass(frozen=True, kw_only=True)
class CaptionResolutionAtFinalize:
    """Per-photo-reference-claim caption + bytes re-read result.

    Used by F-REPORT-COMMITMENT-UNTRACED.source_content_drift for
    photo_reference claims per RT-7b closure (caption hash AND bytes
    hash both re-checked at finalize).
    """

    claim_id: str
    caption_text_sha3_512_at_finalize: Optional[str]
    photo_bytes_sha3_512_at_finalize: Optional[str]


@dataclass(frozen=True, kw_only=True)
class DraftIntegrityAtFinalize:
    """Re-read draft markdown bytes hash at finalize.

    Used by F-REPORT-COMMITMENT-UNTRACED.draft_post_sign_mutation_attempt
    (RT-8b closure) — if the draft file was modified after operator
    signed the claim_evidence_map, the hash mismatch fail-closes.
    """

    draft_content_sha3_512_at_finalize: str
    post_sign_read: bool  # True iff caller is re-reading after operator sign event


# ---------------------------------------------------------------------------
# Proposal-commitments + template substrate (caller-supplied; pre-parsed)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class PromotedCommitmentRow:
    """A PROMOTED row from ``proposal_commitments.yaml``, pre-filtered by the caller.

    Fields read by the §14 gate family (subset of §11 v1 schema):

    * ``commitment_id`` — operator-supplied + sanitized via
      ``_commitment_id.sanitize_commitment_id`` BEFORE admission
      (RT-C2-02 closure).
    * ``status`` — MUST equal ``"PROMOTED"`` for any commitment fed to
      §14; otherwise the caller filters it out.
    * ``scope_tags`` — tuple of scope-tag strings.
    * ``required_sub_sections`` — tuple of sub-section names that MUST
      address this commitment (F-REPORT-COMMITMENT-MISSED).
    * ``evaluation_criteria`` — tuple of evaluation criteria; each is
      either ``("numeric", field, target, tolerance)`` or
      ``("narrative", field, required_min_length_chars)``.
    * ``period_n_window`` — optional tuple ``(start_period_n,
      end_period_n)`` indicating the periods this commitment applies to.
      Used by ``.commitment_period_n_not_due_yet`` sub-tag.
    """

    commitment_id: str
    status: str
    scope_tags: tuple[str, ...]
    required_sub_sections: tuple[str, ...]
    evaluation_criteria: tuple[Mapping[str, object], ...] = field(default_factory=tuple)
    period_n_window: Optional[tuple[int, int]] = None


@dataclass(frozen=True, kw_only=True)
class WaiverRecord:
    """Per-commitment operator-signed waiver per RT-2b closure.

    ``signature_valid`` is the verifier's verdict (caller invokes the
    Ed25519 verifier; gate consumes already-validated input).
    """

    commitment_id: str
    waiver_reason: str
    waiver_signed_at_utc: str
    signature_valid: bool


@dataclass(frozen=True, kw_only=True)
class ReportingTemplateSnapshot:
    """Operator-captured ``reporting_template.yaml`` pre-parsed view.

    Field set is the §14.4.2 ReportingTemplateContract subset the gates
    consume (the full YAML lives on disk; this dataclass carries just the
    fields the F-REPORT-TEMPLATE-MISMATCH predicate body inspects).
    """

    funder_id: str
    template_version: str
    template_captured_at_utc: str
    template_content_sha3_512: str
    required_sub_sections: tuple[str, ...]
    required_fields_per_sub_section: Mapping[str, tuple[Mapping[str, object], ...]]
    required_period_cadence: str
    report_due_n_days_after_period_end: int
    operator_key_version: Optional[str] = None
    template_signature_present: bool = False
    template_signature_valid: bool = False


@dataclass(frozen=True, kw_only=True)
class WorkspacePublishedTemplateSnapshot:
    """Workspace-shared published template snapshot.

    ``present`` is False when the funder's published template is not in
    ``vault_shared/funder_intelligence/<funder_id>/``. ``first_wave`` is
    True when the funder has a valid SN-LLC-signed
    ``sn_llc_first_wave.signed.yaml`` marker file (RT-5a + RT-C2-04
    closures); the gate's fail-closed-vs-advisory disposition pivots on
    this flag.
    """

    funder_id: str
    present: bool
    content_sha3_512: Optional[str] = None
    first_wave: bool = False
    first_wave_marker_signature_valid: Optional[bool] = None
    first_wave_marker_hash_bound_to_lock_history: Optional[bool] = None
    operator_key_versions_allowed: tuple[str, ...] = field(default_factory=tuple)


# ---------------------------------------------------------------------------
# Cross-period prior-period map integrity (RT-4a + RT-C2-09 closure inputs)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class PriorPeriodMapIntegrity:
    """Prior-period claim_evidence_map content integrity at consumption time.

    Used by F-REPORT-COMMITMENT-UNTRACED when SP0 flag
    ``accept_signed_prior_period_claim_evidence_map=true`` is active.
    """

    prior_period_n: int
    map_path: str
    sp0_signature_valid: bool  # RT-4a — SP0 flag activation signature
    map_content_sha3_512_matches_signature_record: bool  # RT-C2-09 — tamper detection
    sources_all_under_same_org_slug: bool  # RT-4b — cross-org leak detection


# ---------------------------------------------------------------------------
# Scope-tag extractor Protocol (RT-OOSD runtime detection)
# ---------------------------------------------------------------------------


@runtime_checkable
class ScopeTagExtractorCallable(Protocol):
    """Extracts scope-tags from a claim's text per §14.9.3 runtime check.

    Returns a (possibly empty) tuple of scope-tag strings. Empty return
    surfaces as ``.runtime_scope_tag_extraction_failed`` advisory.

    Implementation in WS-J Slice 2 / Slice 3 wiring uses a deterministic
    Python NER + scope-tag taxonomy (NOT LLM — Logician is zero-token
    by §4 v2.2 contract); for Slice 1 the gate accepts an injected
    callable so unit tests can pass a deterministic stub.
    """

    def __call__(self, claim_text: str) -> tuple[str, ...]: ...


@runtime_checkable
class BeneficiaryNameDictionaryCallable(Protocol):
    """Returns the per-grant beneficiary-name match dictionary.

    Per RT-C2-03 closure: F-REPORT-BENEFICIARY-PRIVACY-LEAK runs a
    deterministic name-match scan over narrative text using the
    operational-data beneficiary_records' ``beneficiary_name`` +
    ``beneficiary_aliases`` field union. Returns a mapping from
    beneficiary_id → (name_or_alias, consent_tier) tuples.
    """

    def __call__(
        self,
    ) -> Mapping[str, tuple[tuple[str, ...], str]]: ...


# ---------------------------------------------------------------------------
# Closed enum sets
# ---------------------------------------------------------------------------


PERMITTED_PERIOD_CADENCES: Final[frozenset[str]] = frozenset(
    {"monthly", "quarterly", "semi_annual", "annual"}
)


__all__ = [
    "BeneficiaryNameDictionaryCallable",
    "CaptionResolutionAtFinalize",
    "DraftIntegrityAtFinalize",
    "PERMITTED_PERIOD_CADENCES",
    "PriorPeriodMapIntegrity",
    "PromotedCommitmentRow",
    "ReportingTemplateSnapshot",
    "ScopeTagExtractorCallable",
    "SourceResolutionAtFinalize",
    "WaiverRecord",
    "WorkspacePublishedTemplateSnapshot",
]
