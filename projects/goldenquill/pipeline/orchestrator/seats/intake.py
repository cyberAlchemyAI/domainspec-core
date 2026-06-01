#!/usr/bin/env python3
"""
Intake support agent — KFR ingestion + AWARD_INGEST extraction.

Per Blueprint §11 (LOCKED 2026-05-10 row 185): bulk-ingest org documents at
white-glove onboarding (BULK_INGEST), process new docs incrementally during
operations (INCREMENTAL_INGEST), and extract proposal commitments from won
proposals at award acceptance (AWARD_INGEST).

The operator confirms every promotion to canonical KFR — Intake never writes
canonical KFR entries directly. F-EXTRACTOR-FABRICATION ensures no fabricated
candidate ever reaches the operator-review queue.

Substrate (frozen at Golden Image per ADR-001):
  FAISS or Chroma + bge-large-en-v1.5 + Pydantic AI tool composition
  + small local Mistral 7B class LLM. Always-local routing per §11.10.

The substrate is dependency-injected via Protocol so the seat module is
exercisable without the heavy runtime (pypdf / python-docx / Pydantic AI /
FAISS / Mistral). Production-wiring adapters live alongside the seat in
pipeline/orchestrator/seats/intake_adapters/ (out of scope for v0.1 first
ship; Code-phase follow-up). Tests substitute deterministic fakes.

Logician gates owned (per §11.9):
  F-EXTRACTOR-FABRICATION              (PRE pre-queue — verbatim source_quote validation per substrate)
  F-EXTRACTOR-AWARD-SIGNATURE-INVALID  (PRE — submission_artifact + award_doc signature, .proposal + .award)
  F-INTAKE-ORG-CROSS-REF               (PRE — path-isolation discipline)
  F-INTAKE-INPUT-MISSING               (PRE — required input file/directory existence)
  F-INTAKE-UNSUPPORTED-FORMAT          (PRE — file extension allowlist; advisory at INCREMENTAL with quarantine)
  F-INTAKE-QUEUE-INTEGRITY             (POST + PRE-run-start — queue file integrity + state-file sanity)
  F-INTAKE-EMBEDDING-NS-MISMATCH       (PRE-tool-call — org_slug/grant_id arg validation; compound-key collision)
  F-INTAKE-CONFIG-SIGNATURE-INVALID    (PRE — operator-config Ed25519 signature)
  F-INTAKE-EMBEDDING-ENDPOINT-INVALID  (PRE-tool-call — sealed Golden-Image-baked endpoint; localhost-only)
  F-INTAKE-WATCHER-TOCTOU              (PRE-file-open — O_NOFOLLOW + post-open re-resolve)

Skeleton authored at §11 v1 LOCK 2026-05-10 (row 185).
Full implementation landed at WS-E Code phase 2026-05-10.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import unicodedata
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Final, Literal, Mapping, Protocol, Sequence
from urllib.parse import urlparse

# Substrate-dispatched fabrication check lives in the Logician slice 3 module.
from pipeline.logician.gates.f_extractor_fabrication import (
    CandidateFact as _LogicianCandidateFact,
    SUBSTRATE_DOCX as _SUBSTRATE_DOCX,
    SUBSTRATE_MARKDOWN as _SUBSTRATE_MARKDOWN,
    SUBSTRATE_PDF as _SUBSTRATE_PDF,
    check_extractor_fabrication as _check_extractor_fabrication,
)
from pipeline.logician.gates.f_extractor_award_signature_invalid import (
    AwardSignatureLeg as _AwardSignatureLeg,
    check_extractor_award_signature_invalid as _check_award_signature,
)

# commitment_id safe-identifier contract per §11 v1.1 amendment (LOCKED
# 2026-05-11). AWARD_INGEST extraction validates every commitment_id
# against ``^[A-Z0-9_-]+$`` BEFORE proposal_commitments.yaml row admission
# (RT-C2-02 producer-side closure). The canonical home lives in the
# shared producer/consumer sibling module; §14 Report Generator imports
# the same names via a backward-compat shim.
from pipeline.orchestrator.seats._commitment_id import (
    CommitmentIdInvalid as _CommitmentIdInvalid,
    SAFE_COMMITMENT_ID_PATTERN as _SAFE_COMMITMENT_ID_PATTERN,
    sanitize_commitment_id as _sanitize_commitment_id,
)


# ---------------------------------------------------------------------------
# UTC factory + helpers
# ---------------------------------------------------------------------------


def _utc_now() -> datetime:
    """Return a timezone-aware UTC datetime."""
    return datetime.now(timezone.utc)


def _utc_iso(dt: datetime) -> str:
    """ISO-8601 with explicit ``+00:00`` zone for state files."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# Mode literal — three modes per §11.6
# ---------------------------------------------------------------------------

IntakeMode = Literal["BULK_INGEST", "INCREMENTAL_INGEST", "AWARD_INGEST"]

SOURCE_FORMAT_PDF: Final[str] = "pdf"
SOURCE_FORMAT_DOCX: Final[str] = "docx"
SOURCE_FORMAT_TXT: Final[str] = "txt"
SOURCE_FORMAT_MD: Final[str] = "md"
SUPPORTED_FORMATS: Final[frozenset[str]] = frozenset({
    SOURCE_FORMAT_PDF,
    SOURCE_FORMAT_DOCX,
    SOURCE_FORMAT_TXT,
    SOURCE_FORMAT_MD,
})
AWARD_DOC_FORMATS: Final[frozenset[str]] = frozenset({
    SOURCE_FORMAT_PDF,
    SOURCE_FORMAT_DOCX,
})

LOCALHOST_HOSTS: Final[frozenset[str]] = frozenset({
    "localhost",
    "127.0.0.1",
    "::1",
})

_SCHEMA_VERSION_PENDING: Final[str] = "pending_facts.v1"
_SCHEMA_VERSION_COMMITMENTS: Final[str] = "proposal_commitments.v1"
_STATUS_PENDING_REVIEW: Final[str] = "PENDING_OPERATOR_REVIEW"


# ---------------------------------------------------------------------------
# Input contracts (per §11.4) — frozen kw_only
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class IntakeBulkInput:
    """BULK_INGEST input bundle. Per §11.4.1."""
    run_id: str
    org_slug: str
    inbox_dir: str  # Path.resolve() under orgs/<org_slug>/
    confidence_autopromote_threshold: float = 0.85
    invoked_at_utc: datetime = field(default_factory=_utc_now)
    mode: IntakeMode = "BULK_INGEST"
    # Optional override pointing MIGRATION_BULK_INGEST at a single
    # PROJECT_CONTEXT.md (per §11.11). When set, sweep is bypassed and the
    # named path becomes the sole source doc; mode flag stays BULK_INGEST.
    migration_target_path: str | None = None


@dataclass(frozen=True, kw_only=True)
class IntakeIncrementalInput:
    """INCREMENTAL_INGEST input bundle. Per §11.4.2."""
    run_id: str
    org_slug: str
    doc_path: str  # Path.resolve() under orgs/<org_slug>/intake/inbox/
    trigger: Literal["watcher", "operator_explicit"]
    confidence_autopromote_threshold: float = 0.85
    invoked_at_utc: datetime = field(default_factory=_utc_now)
    mode: IntakeMode = "INCREMENTAL_INGEST"


@dataclass(frozen=True, kw_only=True)
class IntakeAwardInput:
    """AWARD_INGEST input bundle. Per §11.4.3."""
    run_id: str
    org_slug: str
    grant_id: str
    submission_artifact_ref: str  # auto-resolved from --grant
    award_doc_path: str            # operator-supplied
    award_doc_unsigned_attestation: bool = False
    invoked_at_utc: datetime = field(default_factory=_utc_now)
    mode: IntakeMode = "AWARD_INGEST"


IntakeInput = IntakeBulkInput | IntakeIncrementalInput | IntakeAwardInput


# ---------------------------------------------------------------------------
# Pending fact + proposal commitment schemas (per §11.5)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class PendingFact:
    """Single candidate fact in the operator-review queue. Per §11.5.1."""
    candidate_id: str
    intake_run_id: str
    extracted_at_utc: datetime
    source_doc: str
    source_format: Literal["pdf", "docx", "txt", "md"]
    source_page: int | None
    source_paragraph_id: int | None
    source_line_id: int | None
    source_quote: str
    confidence_score: float
    autopromote_batch: bool
    multiple_page_match: bool = False
    fact_payload: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, kw_only=True)
class ProposalCommitment:
    """Single commitment row extracted from a won proposal. Per §11.5.2."""
    commitment_id: str
    intake_run_id: str
    extracted_at_utc: datetime
    source_section: str
    commitment_text: str
    commitment_proposal_offset: int
    measurable_metric: str
    target_value: float | None
    target_unit: str | None
    due_period: str | None
    page_tolerance_applied: bool = False
    kfr_fact_ref: str | None = None


# ---------------------------------------------------------------------------
# State (per Rule 1 Save State Always)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class IntakeState:
    """Persistent state per Intake run. Saved on success AND failure per Rule 1."""
    run_id: str
    org_slug: str
    grant_id: str | None
    mode: IntakeMode
    invoked_at_utc: datetime
    mode_completed: bool
    candidates_emitted_to_LLM: int
    candidates_in_queue: int
    candidates_rejected: int
    failure_reason: str | None = None
    failure_detail: str | None = None
    trigger: Literal["watcher", "operator_explicit", "operator_explicit_award"] | None = None
    docs_processed: tuple[str, ...] = ()
    skipped_unsupported: tuple[str, ...] = ()


# ---------------------------------------------------------------------------
# Gate result envelope
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class GateResult:
    """Result of a Logician gate check. Per §12 Uploader convention."""
    passed: bool
    code: str | None = None
    sub_tag: str | None = None
    detail: str | None = None

    @classmethod
    def PASS(cls) -> GateResult:
        return cls(passed=True)

    @classmethod
    def FAIL(cls, *, code: str, sub_tag: str | None = None, detail: str | None = None) -> GateResult:
        return cls(passed=False, code=code, sub_tag=sub_tag, detail=detail)


# ---------------------------------------------------------------------------
# Substrate dependency Protocols — injected at handler call sites
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class ParsedDocument:
    """Output of a DocumentParser — the substrate-relevant slice of source bytes.

    Exactly one of ``pages`` / ``paragraphs`` / ``lines`` is populated per the
    declared ``source_format``.  The slice is the input to F-EXTRACTOR-FABRICATION.
    """
    source_doc: str
    source_format: Literal["pdf", "docx", "txt", "md"]
    pages: Mapping[int, str] | None = None
    paragraphs: Sequence[str] | None = None
    lines: Sequence[str] | None = None
    raw_bytes: bytes | None = None


class DocumentParserProtocol(Protocol):
    """Contract for substrate-specific document parsing.

    The production adapter wraps pypdf / python-docx / native text read; the
    test adapter supplies deterministic in-memory parses.
    """

    def parse(self, file_path: str, source_format: str) -> ParsedDocument: ...


@dataclass(frozen=True, kw_only=True)
class ExtractedCandidate:
    """LLM-emitted candidate prior to gate validation.

    The LLM proposes ``source_*`` anchors; F-EXTRACTOR-FABRICATION verifies
    the quote against the parsed source bytes at those anchors.
    """
    source_doc: str
    source_format: Literal["pdf", "docx", "txt", "md"]
    source_page: int | None
    source_paragraph_id: int | None
    source_line_id: int | None
    source_quote: str
    confidence_score: float
    fact_payload: Mapping[str, Any] = field(default_factory=dict)
    multiple_page_match: bool = False


@dataclass(frozen=True, kw_only=True)
class ExtractedCommitment:
    """LLM-emitted commitment prior to gate validation."""
    source_section: str
    commitment_text: str
    commitment_proposal_offset: int
    measurable_metric: str
    target_value: float | None = None
    target_unit: str | None = None
    due_period: str | None = None
    source_page: int | None = None
    source_paragraph_id: int | None = None
    source_line_id: int | None = None
    page_tolerance_applied: bool = False
    kfr_fact_ref: str | None = None


class FactExtractorProtocol(Protocol):
    """Contract for the extraction LLM (BULK + INCREMENTAL)."""

    def extract_facts(
        self,
        *,
        org_slug: str,
        parsed: ParsedDocument,
    ) -> Sequence[ExtractedCandidate]: ...


class CommitmentExtractorProtocol(Protocol):
    """Contract for the extraction LLM (AWARD_INGEST)."""

    def extract_commitments(
        self,
        *,
        org_slug: str,
        grant_id: str,
        parsed: ParsedDocument,
    ) -> Sequence[ExtractedCommitment]: ...


SignatureVerifyCallable = Callable[[bytes, bytes, bytes], bool]
KeyActiveLookupCallable = Callable[[str, datetime], bool]


@dataclass(frozen=True, kw_only=True)
class SignedConfigBlock:
    """Operator-signed wrapper around a per-org intake_config payload."""
    payload_canonical_bytes: bytes
    signature: bytes
    signed_by: str
    signed_at_utc: datetime
    signer_public_key: bytes


@dataclass(frozen=True, kw_only=True)
class SignedClaimEvidenceMap:
    """Section 4 v2.1 SignedClaimEvidenceMap subset used by AWARD_INGEST.

    Only the fields F-EXTRACTOR-AWARD-SIGNATURE-INVALID.proposal needs are
    modeled here; the full schema lives in §4.
    """
    payload_canonical_bytes: bytes
    signature: bytes
    signed_by: str
    signed_at_utc: datetime
    signer_public_key: bytes
    submission_artifact_content_sha3_512: str | None  # absent → .legacy_unhashed


@dataclass(frozen=True, kw_only=True)
class FunderSignatureMaterial:
    """Funder-side signature material extracted from an award document.

    ``signature``/``message_bytes``/``public_key`` are populated when the
    funder publishes signing keys; otherwise ``unsigned`` is True and the
    operator must supply ``award_doc_unsigned_attestation=True`` at CLI to
    bypass per §11.9.3 (with ledger entry).
    """
    signature: bytes
    message_bytes: bytes
    public_key: bytes
    unsigned: bool = False


# ---------------------------------------------------------------------------
# Mode dispatcher — §11.6 entry point
# ---------------------------------------------------------------------------


_MODE_DISPATCHER: dict[IntakeMode, str] = {
    "BULK_INGEST": "bulk_ingest",
    "INCREMENTAL_INGEST": "incremental_ingest",
    "AWARD_INGEST": "award_ingest",
}


def get_mode_handler_name(mode: IntakeMode) -> str:
    """Return the name of the handler for a given mode.

    Per §11.6.0 three-mode summary table — exactly three modes register at v1
    (BULK_INGEST / INCREMENTAL_INGEST / AWARD_INGEST). MIGRATION_BULK_INGEST is
    a special invocation of BULK_INGEST scoped to PROJECT_CONTEXT.md per §11.11
    — NOT a fourth registered mode.
    """
    if mode not in _MODE_DISPATCHER:
        raise ValueError(
            f"Unknown Intake mode '{mode}'. Available: {sorted(_MODE_DISPATCHER)}"
        )
    return _MODE_DISPATCHER[mode]


def list_registered_modes() -> tuple[IntakeMode, ...]:
    """Return the tuple of registered mode literals."""
    return tuple(_MODE_DISPATCHER.keys())  # type: ignore[return-value]


# ---------------------------------------------------------------------------
# Path utilities (org-isolation, file existence, format check)
# ---------------------------------------------------------------------------


def _resolve(path: str | os.PathLike[str]) -> Path:
    """Path.resolve() with strict=False; resolves symlinks but tolerates absent files."""
    return Path(path).expanduser().resolve()


def _is_under(child: Path, parent: Path) -> bool:
    """True iff ``child`` is the same as or under ``parent`` after resolution."""
    try:
        child.relative_to(parent)
    except ValueError:
        return False
    return True


def _format_from_extension(file_path: str) -> str | None:
    suffix = Path(file_path).suffix.lower().lstrip(".")
    return suffix or None


# ---------------------------------------------------------------------------
# §11.9.4 F-INTAKE-ORG-CROSS-REF (PRE)
# ---------------------------------------------------------------------------


def f_intake_org_cross_ref(intake_input: IntakeInput) -> GateResult:
    """Path-isolation discipline. Per §11.9.4."""
    org_slug = intake_input.org_slug
    org_root = _resolve(f"orgs/{org_slug}")
    if isinstance(intake_input, IntakeBulkInput):
        target = intake_input.inbox_dir
        resolved = _resolve(target)
        if not _is_under(resolved, org_root):
            sub = ".symlink_escape" if Path(target).is_symlink() else ".path_outside_inbox"
            return GateResult.FAIL(
                code="F-INTAKE-ORG-CROSS-REF",
                sub_tag=sub,
                detail=f"inbox_dir resolved to {resolved}, outside {org_root}",
            )
        return GateResult.PASS()

    if isinstance(intake_input, IntakeIncrementalInput):
        inbox_root = _resolve(f"orgs/{org_slug}/intake/inbox")
        target = intake_input.doc_path
        resolved = _resolve(target)
        if not _is_under(resolved, inbox_root):
            sub = ".symlink_escape" if Path(target).is_symlink() else ".path_outside_inbox"
            return GateResult.FAIL(
                code="F-INTAKE-ORG-CROSS-REF",
                sub_tag=sub,
                detail=f"doc_path resolved to {resolved}, outside {inbox_root}",
            )
        return GateResult.PASS()

    # AWARD_INGEST
    grant_root = _resolve(f"orgs/{org_slug}/vault/grants/{intake_input.grant_id}")
    award_root = grant_root / "award"
    submission = _resolve(intake_input.submission_artifact_ref)
    if not _is_under(submission, grant_root):
        return GateResult.FAIL(
            code="F-INTAKE-ORG-CROSS-REF",
            sub_tag=".cross_grant",
            detail=f"submission_artifact_ref resolved to {submission}, outside {grant_root}",
        )
    award = _resolve(intake_input.award_doc_path)
    if not _is_under(award, award_root):
        return GateResult.FAIL(
            code="F-INTAKE-ORG-CROSS-REF",
            sub_tag=".award_doc_outside_vault",
            detail=f"award_doc_path resolved to {award}, outside {award_root}",
        )
    return GateResult.PASS()


# ---------------------------------------------------------------------------
# §11.9.5 F-INTAKE-INPUT-MISSING (PRE)
# ---------------------------------------------------------------------------


def f_intake_input_missing(intake_input: IntakeInput) -> GateResult:
    """Required input file/directory existence check. Per §11.9.5."""
    if isinstance(intake_input, IntakeBulkInput):
        target = intake_input.migration_target_path or intake_input.inbox_dir
        resolved = _resolve(target)
        if intake_input.migration_target_path is not None:
            if not resolved.is_file():
                return GateResult.FAIL(
                    code="F-INTAKE-INPUT-MISSING",
                    sub_tag=".doc_absent",
                    detail=f"migration_target_path {resolved} not a regular file",
                )
            return GateResult.PASS()
        if not resolved.is_dir():
            return GateResult.FAIL(
                code="F-INTAKE-INPUT-MISSING",
                sub_tag=".inbox_dir_absent",
                detail=f"inbox_dir {resolved} does not exist or is not a directory",
            )
        return GateResult.PASS()

    if isinstance(intake_input, IntakeIncrementalInput):
        resolved = _resolve(intake_input.doc_path)
        if not resolved.is_file():
            return GateResult.FAIL(
                code="F-INTAKE-INPUT-MISSING",
                sub_tag=".doc_absent",
                detail=f"doc_path {resolved} does not exist or is not a regular file",
            )
        return GateResult.PASS()

    # AWARD_INGEST
    submission = _resolve(intake_input.submission_artifact_ref)
    if not submission.is_file():
        return GateResult.FAIL(
            code="F-INTAKE-INPUT-MISSING",
            sub_tag=".submission_artifact_absent",
            detail=f"submission_artifact_ref {submission} does not exist",
        )
    award = _resolve(intake_input.award_doc_path)
    if not award.is_file():
        return GateResult.FAIL(
            code="F-INTAKE-INPUT-MISSING",
            sub_tag=".award_doc_absent",
            detail=f"award_doc_path {award} does not exist",
        )
    return GateResult.PASS()


# ---------------------------------------------------------------------------
# §11.9.6 F-INTAKE-UNSUPPORTED-FORMAT (PRE / advisory at INCREMENTAL)
# ---------------------------------------------------------------------------


def f_intake_unsupported_format(file_path: str, *, mode: IntakeMode) -> GateResult:
    """File extension allowlist check. Per §11.9.6."""
    fmt = _format_from_extension(file_path)
    allowed = AWARD_DOC_FORMATS if mode == "AWARD_INGEST" else SUPPORTED_FORMATS
    if fmt is None or fmt not in allowed:
        sub = ".award_doc" if mode == "AWARD_INGEST" else None
        return GateResult.FAIL(
            code="F-INTAKE-UNSUPPORTED-FORMAT",
            sub_tag=sub,
            detail=f"format {fmt!r} not in supported set {sorted(allowed)} for mode {mode}",
        )
    return GateResult.PASS()


# ---------------------------------------------------------------------------
# §11.9.8 F-INTAKE-EMBEDDING-NS-MISMATCH (PRE-tool-call)
# ---------------------------------------------------------------------------


def f_intake_embedding_ns_mismatch(
    *,
    expected_org_slug: str,
    expected_grant_id: str | None,
    tool_arg_org_slug: str,
    tool_arg_grant_id: str | None,
    embedding_storage_path: str | None = None,
    existing_storage_owners: Mapping[str, str] | None = None,
) -> GateResult:
    """Pre-tool guard against cross-org/cross-grant vector store calls.

    Compound-key collision check (RT-10): if ``embedding_storage_path`` is
    supplied AND ``existing_storage_owners`` maps it to a different org_slug,
    fire ``.compound_key_collision``.
    """
    if tool_arg_org_slug != expected_org_slug:
        return GateResult.FAIL(
            code="F-INTAKE-EMBEDDING-NS-MISMATCH",
            sub_tag=".org_slug_mismatch",
            detail=(
                f"tool arg org_slug {tool_arg_org_slug!r} != input bundle "
                f"org_slug {expected_org_slug!r}"
            ),
        )
    if expected_grant_id is not None and tool_arg_grant_id != expected_grant_id:
        return GateResult.FAIL(
            code="F-INTAKE-EMBEDDING-NS-MISMATCH",
            sub_tag=".grant_id_mismatch",
            detail=(
                f"tool arg grant_id {tool_arg_grant_id!r} != input bundle "
                f"grant_id {expected_grant_id!r}"
            ),
        )
    if (
        embedding_storage_path is not None
        and existing_storage_owners is not None
        and embedding_storage_path in existing_storage_owners
        and existing_storage_owners[embedding_storage_path] != expected_org_slug
    ):
        return GateResult.FAIL(
            code="F-INTAKE-EMBEDDING-NS-MISMATCH",
            sub_tag=".compound_key_collision",
            detail=(
                f"embedding storage path {embedding_storage_path!r} already "
                f"owned by org_slug "
                f"{existing_storage_owners[embedding_storage_path]!r}"
            ),
        )
    return GateResult.PASS()


# ---------------------------------------------------------------------------
# §11.9.9 F-INTAKE-CONFIG-SIGNATURE-INVALID (PRE)
# ---------------------------------------------------------------------------


def f_intake_config_signature_invalid(
    config_yaml_path: str,
    *,
    signed_block_loader: Callable[[str], SignedConfigBlock | None] | None = None,
    signature_verify: SignatureVerifyCallable | None = None,
    key_active_lookup: KeyActiveLookupCallable | None = None,
) -> GateResult:
    """Validates intake_config.yaml Ed25519 signature. Per §11.9.9 + RT-07.

    Absence of the file is PASS (hardcoded 0.85 default applies; no attack
    surface). Presence requires a SignedConfig block from a key currently
    active in the Section 1 key catalog at signed_at_utc time.
    """
    resolved = _resolve(config_yaml_path)
    if not resolved.is_file():
        return GateResult.PASS()

    if signed_block_loader is None or signature_verify is None or key_active_lookup is None:
        return GateResult.FAIL(
            code="F-INTAKE-CONFIG-SIGNATURE-INVALID",
            sub_tag=".signature_absent",
            detail=(
                "intake_config.yaml present but signed_block_loader / "
                "signature_verify / key_active_lookup not wired — fail-closed"
            ),
        )

    block = signed_block_loader(str(resolved))
    if block is None:
        return GateResult.FAIL(
            code="F-INTAKE-CONFIG-SIGNATURE-INVALID",
            sub_tag=".signature_absent",
            detail="intake_config.yaml has no SignedConfig block",
        )

    try:
        ok = signature_verify(block.payload_canonical_bytes, block.signature, block.signer_public_key)
    except Exception as exc:  # noqa: BLE001 — fail-closed
        return GateResult.FAIL(
            code="F-INTAKE-CONFIG-SIGNATURE-INVALID",
            sub_tag=".signature_invalid",
            detail=f"signature verifier raised {type(exc).__name__}: {exc}",
        )
    if ok is not True:
        return GateResult.FAIL(
            code="F-INTAKE-CONFIG-SIGNATURE-INVALID",
            sub_tag=".signature_invalid",
            detail="signature verification returned non-True",
        )

    if not key_active_lookup(block.signed_by, block.signed_at_utc):
        return GateResult.FAIL(
            code="F-INTAKE-CONFIG-SIGNATURE-INVALID",
            sub_tag=".retired_key",
            detail=(
                f"signing key {block.signed_by!r} not active at signed_at_utc "
                f"{_utc_iso(block.signed_at_utc)}"
            ),
        )
    return GateResult.PASS()


# ---------------------------------------------------------------------------
# §11.9.10 F-INTAKE-EMBEDDING-ENDPOINT-INVALID (PRE-tool-call)
# ---------------------------------------------------------------------------


_UNIX_SOCKET_RE: Final[re.Pattern[str]] = re.compile(r"^unix://(/[^?#]+)$")


def f_intake_embedding_endpoint_invalid(endpoint: str) -> GateResult:
    """Validates embedding endpoint against localhost-or-unix-socket allowlist."""
    if _UNIX_SOCKET_RE.match(endpoint):
        return GateResult.PASS()
    parsed = urlparse(endpoint)
    if parsed.scheme not in {"http", "https"}:
        return GateResult.FAIL(
            code="F-INTAKE-EMBEDDING-ENDPOINT-INVALID",
            detail=f"unsupported scheme {parsed.scheme!r} in endpoint {endpoint!r}",
        )
    host = (parsed.hostname or "").lower()
    if host not in LOCALHOST_HOSTS:
        return GateResult.FAIL(
            code="F-INTAKE-EMBEDDING-ENDPOINT-INVALID",
            detail=(
                f"host {host!r} not in localhost allowlist "
                f"{sorted(LOCALHOST_HOSTS)}"
            ),
        )
    return GateResult.PASS()


# ---------------------------------------------------------------------------
# §11.9.11 F-INTAKE-WATCHER-TOCTOU (PRE-file-open)
# ---------------------------------------------------------------------------


def f_intake_watcher_toctou(
    file_path: str,
    *,
    expected_org_subtree: str,
) -> GateResult:
    """TOCTOU-safe file open. Per §11.9.11 + RT-11.

    Performs Path.resolve() + is_file() + not is_symlink() + os.O_NOFOLLOW
    open + post-open re-resolve. Returns PASS only if all four checks succeed
    AND the post-open resolved path equals the pre-open resolve.
    """
    pre_resolved = _resolve(file_path)
    expected_root = _resolve(expected_org_subtree)
    if not _is_under(pre_resolved, expected_root):
        return GateResult.FAIL(
            code="F-INTAKE-WATCHER-TOCTOU",
            sub_tag=".pre_resolve_outside_subtree",
            detail=f"pre-open resolve {pre_resolved} outside {expected_root}",
        )
    p = Path(file_path)
    if not p.is_file():
        return GateResult.FAIL(
            code="F-INTAKE-WATCHER-TOCTOU",
            sub_tag=".not_regular_file",
            detail=f"path {file_path!r} is not a regular file at gate time",
        )
    if p.is_symlink():
        return GateResult.FAIL(
            code="F-INTAKE-WATCHER-TOCTOU",
            sub_tag=".symlink_at_gate",
            detail=f"path {file_path!r} is a symlink at gate time",
        )
    try:
        fd = os.open(str(p), os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    except OSError as exc:
        return GateResult.FAIL(
            code="F-INTAKE-WATCHER-TOCTOU",
            sub_tag=".o_nofollow_eloop",
            detail=f"os.open(O_NOFOLLOW) raised {type(exc).__name__}: {exc}",
        )
    try:
        post_resolved = _resolve(file_path)
        if post_resolved != pre_resolved:
            return GateResult.FAIL(
                code="F-INTAKE-WATCHER-TOCTOU",
                sub_tag=".post_open_resolve_mismatch",
                detail=(
                    f"post-open resolve {post_resolved} != pre-open resolve "
                    f"{pre_resolved}"
                ),
            )
    finally:
        os.close(fd)
    return GateResult.PASS()


# ---------------------------------------------------------------------------
# §11.9.7 F-INTAKE-QUEUE-INTEGRITY (POST + PRE-run-start)
# ---------------------------------------------------------------------------


def f_intake_queue_integrity_pre_run(
    *,
    state_file_path: str,
    queue_file_path: str | None = None,
    reject_count_for_run: int | None = None,
    state_loader: Callable[[str], dict[str, Any] | None] | None = None,
    queue_loader: Callable[[str], list[dict[str, Any]]] | None = None,
) -> GateResult:
    """PRE-run-start sanity check on the most-recent state file. Per RT-12."""
    state_path = Path(state_file_path)
    if not state_path.is_file():
        # Legitimate first-invocation case.
        return GateResult.PASS()
    if state_loader is None:
        return GateResult.PASS()
    try:
        state = state_loader(state_file_path)
    except Exception as exc:  # noqa: BLE001 — fail-closed on parse error
        return GateResult.FAIL(
            code="F-INTAKE-QUEUE-INTEGRITY",
            sub_tag=".state_corrupted",
            detail=f"state_loader raised {type(exc).__name__}: {exc}",
        )
    if state is None or not isinstance(state, dict):
        return GateResult.FAIL(
            code="F-INTAKE-QUEUE-INTEGRITY",
            sub_tag=".state_corrupted",
            detail="state file did not parse to a dict",
        )
    required_fields = (
        "run_id",
        "mode",
        "candidates_emitted_to_LLM",
        "candidates_in_queue",
        "candidates_rejected",
    )
    for fld in required_fields:
        if fld not in state:
            return GateResult.FAIL(
                code="F-INTAKE-QUEUE-INTEGRITY",
                sub_tag=".state_corrupted",
                detail=f"state file missing required field {fld!r}",
            )
    if (
        queue_file_path is not None
        and queue_loader is not None
        and reject_count_for_run is not None
    ):
        try:
            queue = queue_loader(queue_file_path)
        except Exception as exc:  # noqa: BLE001
            return GateResult.FAIL(
                code="F-INTAKE-QUEUE-INTEGRITY",
                sub_tag=".cross_run_drift",
                detail=f"queue_loader raised {type(exc).__name__}: {exc}",
            )
        run_id = state["run_id"]
        run_in_queue = sum(1 for r in queue if r.get("intake_run_id") == run_id)
        emitted = int(state["candidates_emitted_to_LLM"])
        rejected = int(state["candidates_rejected"])
        if emitted != run_in_queue + rejected:
            return GateResult.FAIL(
                code="F-INTAKE-QUEUE-INTEGRITY",
                sub_tag=".cross_run_drift",
                detail=(
                    f"emitted {emitted} != in_queue {run_in_queue} + rejected "
                    f"{rejected} for run {run_id}"
                ),
            )
    return GateResult.PASS()


def f_intake_queue_integrity_post_write(
    *,
    state: IntakeState,
    queue_file_path: str,
    queue_loader: Callable[[str], list[dict[str, Any]]],
    reject_count_for_run: int,
) -> GateResult:
    """POST-write integrity check on the queue file. Per §11.9.7."""
    try:
        queue = queue_loader(queue_file_path)
    except Exception as exc:  # noqa: BLE001
        return GateResult.FAIL(
            code="F-INTAKE-QUEUE-INTEGRITY",
            sub_tag=".post_write_pydantic_fail",
            detail=f"queue_loader raised {type(exc).__name__}: {exc}",
        )
    in_queue = sum(1 for r in queue if r.get("intake_run_id") == state.run_id)
    if in_queue != state.candidates_in_queue:
        return GateResult.FAIL(
            code="F-INTAKE-QUEUE-INTEGRITY",
            sub_tag=".post_write_count_mismatch",
            detail=(
                f"queue contains {in_queue} entries for run {state.run_id} "
                f"but state.candidates_in_queue == {state.candidates_in_queue}"
            ),
        )
    if state.candidates_emitted_to_LLM != in_queue + reject_count_for_run:
        return GateResult.FAIL(
            code="F-INTAKE-QUEUE-INTEGRITY",
            sub_tag=".post_write_count_mismatch",
            detail=(
                f"emitted {state.candidates_emitted_to_LLM} != in_queue "
                f"{in_queue} + rejected {reject_count_for_run}"
            ),
        )
    return GateResult.PASS()


# ---------------------------------------------------------------------------
# §11.9.1 F-EXTRACTOR-FABRICATION (PRE pre-queue)
# ---------------------------------------------------------------------------


def _format_to_substrate(source_format: str) -> str:
    if source_format == SOURCE_FORMAT_PDF:
        return _SUBSTRATE_PDF
    if source_format == SOURCE_FORMAT_DOCX:
        return _SUBSTRATE_DOCX
    if source_format in (SOURCE_FORMAT_TXT, SOURCE_FORMAT_MD):
        return _SUBSTRATE_MARKDOWN
    raise ValueError(f"unsupported source_format {source_format!r}")


def f_extractor_fabrication(
    candidate: ExtractedCandidate | ExtractedCommitment,
    *,
    mode: IntakeMode,
    parsed: ParsedDocument,
    operator_award_page_offset_flag: bool = False,
) -> GateResult:
    """PRE-pre-queue verbatim-quote validation. Per §11.9.1.

    Substrate-dispatched via the Logician slice 3 implementation
    (``pipeline.logician.gates.f_extractor_fabrication``). Mode-tolerance
    is read from the ``mode`` argument only (which is plumbed from the
    Intake input dataclass at the handler call site, never from runtime
    config) per RT-04 immutability.

    Markdown extra defense (RT-02): single-line constraint at gate time —
    multi-line ``source_quote`` rejected with ``.markdown_multiline``.
    """
    if isinstance(candidate, ExtractedCandidate):
        quote = candidate.source_quote
        source_format = candidate.source_format
        source_doc = candidate.source_doc
        source_page = candidate.source_page
        source_paragraph_id = candidate.source_paragraph_id
        source_line_id = candidate.source_line_id
        multi = candidate.multiple_page_match
    else:
        quote = candidate.commitment_text
        source_format = parsed.source_format
        source_doc = parsed.source_doc
        source_page = candidate.source_page
        source_paragraph_id = candidate.source_paragraph_id
        source_line_id = candidate.source_line_id
        multi = False

    if source_format == SOURCE_FORMAT_MD and ("\n" in quote or "\r" in quote):
        return GateResult.FAIL(
            code="F-EXTRACTOR-FABRICATION",
            sub_tag=".markdown_multiline",
            detail="markdown source_quote contains newline — single-line constraint",
        )

    substrate = _format_to_substrate(source_format)

    award_offset_flag = bool(
        mode == "AWARD_INGEST"
        and substrate == _SUBSTRATE_PDF
        and operator_award_page_offset_flag
    )

    locator_kwargs: dict[str, Any] = {}
    if substrate == _SUBSTRATE_PDF:
        locator_kwargs["source_page"] = source_page
    elif substrate == _SUBSTRATE_DOCX:
        locator_kwargs["source_paragraph_index"] = source_paragraph_id
    else:  # MARKDOWN (.md or .txt)
        if source_line_id is None:
            return GateResult.FAIL(
                code="F-EXTRACTOR-FABRICATION",
                sub_tag=".line_mismatch",
                detail=f"{source_format} substrate requires source_line_id",
            )
        locator_kwargs["source_line"] = source_line_id + 1  # logician gate is 1-based

    logician_candidate = _LogicianCandidateFact(
        candidate_quote=quote,
        source_doc_id=source_doc,
        mode=mode,
        substrate=substrate,
        operator_award_page_offset_flag=award_offset_flag,
        **locator_kwargs,
    )

    pdf_pages = parsed.pages if substrate == _SUBSTRATE_PDF else None
    docx_paragraphs = parsed.paragraphs if substrate == _SUBSTRATE_DOCX else None
    md_lines = parsed.lines if substrate == _SUBSTRATE_MARKDOWN else None

    # PDF unique-page-match (RT-01): the logician gate accepts substring on the
    # declared page; §11.9.1.A also requires that the FIRST occurrence of the
    # quote in the doc is at the declared page (or that the candidate carries
    # multiple_page_match=True for boilerplate). Enforce here on top of the
    # logician gate.
    if substrate == _SUBSTRATE_PDF and pdf_pages is not None and source_page is not None:
        normalized_quote = _normalize(quote)
        if normalized_quote:
            first_page: int | None = None
            occurrence_count = 0
            for p in sorted(pdf_pages.keys()):
                if normalized_quote in _normalize(pdf_pages[p]):
                    occurrence_count += 1
                    if first_page is None:
                        first_page = p
            if first_page is not None and not award_offset_flag:
                if first_page != source_page and not multi:
                    return GateResult.FAIL(
                        code="F-EXTRACTOR-FABRICATION",
                        sub_tag=".page_mismatch",
                        detail=(
                            f"first occurrence at page {first_page}, declared "
                            f"page {source_page}"
                        ),
                    )
                if occurrence_count > 1 and not multi:
                    return GateResult.FAIL(
                        code="F-EXTRACTOR-FABRICATION",
                        sub_tag=".multiple_page_match",
                        detail=(
                            f"quote occurs on {occurrence_count} pages — "
                            "set multiple_page_match=True to override"
                        ),
                    )

    result = _check_extractor_fabrication(
        candidate=logician_candidate,
        source_pages=pdf_pages,
        source_paragraphs=docx_paragraphs,
        source_lines=md_lines,
    )
    if result.success:
        return GateResult.PASS()
    sub_tag = ".docx_paragraph_mismatch" if substrate == _SUBSTRATE_DOCX else (
        ".line_mismatch" if substrate == _SUBSTRATE_MARKDOWN else ".page_mismatch"
    )
    if "ellipsis" in (result.detail or "").lower():
        sub_tag = ".ellipsis_substring"
    return GateResult.FAIL(
        code="F-EXTRACTOR-FABRICATION",
        sub_tag=sub_tag,
        detail=result.detail,
    )


_WS_RE: Final[re.Pattern[str]] = re.compile(r"[\t\n\r\f\v ]+")


def _normalize(text: str) -> str:
    return _WS_RE.sub(" ", unicodedata.normalize("NFC", text)).strip()


# ---------------------------------------------------------------------------
# §11.9.2 + §11.9.3 F-EXTRACTOR-AWARD-SIGNATURE-INVALID
# ---------------------------------------------------------------------------


def f_extractor_award_signature_invalid_proposal(
    award_input: IntakeAwardInput,
    *,
    submission_artifact_bytes: bytes,
    signed_claim_evidence_map: SignedClaimEvidenceMap,
    signature_verify: SignatureVerifyCallable,
    key_active_lookup: KeyActiveLookupCallable,
) -> GateResult:
    """SignedClaimEvidenceMap signature + content-hash binding. Per §11.9.2 + RT-05."""
    leg = _AwardSignatureLeg(
        signature=signed_claim_evidence_map.signature,
        message_bytes=signed_claim_evidence_map.payload_canonical_bytes,
        public_key=signed_claim_evidence_map.signer_public_key,
    )
    # Reuse logician proposal-only path: pass dummy attested-unsigned award leg.
    award_leg_dummy = _AwardSignatureLeg(
        signature=b"",
        message_bytes=b"",
        public_key=b"",
        unsigned_with_attestation=True,
    )
    res = _check_award_signature(
        proposal_leg=leg,
        award_leg=award_leg_dummy,
        signature_verify=signature_verify,
    )
    if not res.success:
        return GateResult.FAIL(
            code="F-EXTRACTOR-AWARD-SIGNATURE-INVALID",
            sub_tag=".signature_invalid",
            detail=res.detail,
        )
    if not key_active_lookup(
        signed_claim_evidence_map.signed_by,
        signed_claim_evidence_map.signed_at_utc,
    ):
        return GateResult.FAIL(
            code="F-EXTRACTOR-AWARD-SIGNATURE-INVALID",
            sub_tag=".retired_key",
            detail=(
                f"signing key {signed_claim_evidence_map.signed_by!r} not "
                f"active at signed_at_utc"
            ),
        )
    expected = signed_claim_evidence_map.submission_artifact_content_sha3_512
    if expected is None:
        return GateResult.FAIL(
            code="F-EXTRACTOR-AWARD-SIGNATURE-INVALID",
            sub_tag=".legacy_unhashed",
            detail="SignedClaimEvidenceMap predates §11 v1 LOCK content-hash binding",
        )
    actual = hashlib.sha3_512(submission_artifact_bytes).hexdigest()
    if actual != expected:
        return GateResult.FAIL(
            code="F-EXTRACTOR-AWARD-SIGNATURE-INVALID",
            sub_tag=".hash_mismatch",
            detail=f"submission artifact SHA3-512 mismatch (expected {expected[:16]}…)",
        )
    return GateResult.PASS()


def f_extractor_award_signature_invalid_award(
    award_input: IntakeAwardInput,
    *,
    funder_signature_material: FunderSignatureMaterial | None,
    signature_verify: SignatureVerifyCallable,
) -> GateResult:
    """Award-document funder signature OR operator attestation. Per §11.9.3 + RT-06."""
    attestation = award_input.award_doc_unsigned_attestation
    if funder_signature_material is None or funder_signature_material.unsigned:
        if attestation:
            return GateResult.PASS()
        return GateResult.FAIL(
            code="F-EXTRACTOR-AWARD-SIGNATURE-INVALID",
            sub_tag=".award_unsigned_no_attestation",
            detail=(
                "funder publishes no signing key AND "
                "award_doc_unsigned_attestation=False"
            ),
        )
    proposal_leg_dummy = _AwardSignatureLeg(
        signature=b"\x00" * 64,
        message_bytes=b"sentinel",
        public_key=b"\x00" * 32,
    )
    award_leg = _AwardSignatureLeg(
        signature=funder_signature_material.signature,
        message_bytes=funder_signature_material.message_bytes,
        public_key=funder_signature_material.public_key,
    )

    def _two_track_verify(message: bytes, sig: bytes, key: bytes) -> bool:
        if message == b"sentinel":
            return True  # short-circuit dummy proposal leg
        return signature_verify(message, sig, key)

    res = _check_award_signature(
        proposal_leg=proposal_leg_dummy,
        award_leg=award_leg,
        signature_verify=_two_track_verify,
    )
    if res.success:
        return GateResult.PASS()
    return GateResult.FAIL(
        code="F-EXTRACTOR-AWARD-SIGNATURE-INVALID",
        sub_tag=".award_signature_invalid",
        detail=res.detail,
    )


# ---------------------------------------------------------------------------
# State + queue I/O helpers (Rule 1 + Rule 4)
# ---------------------------------------------------------------------------


def _state_file_path(intake_input: IntakeInput) -> Path:
    return Path(
        f"orgs/{intake_input.org_slug}/vault/kfr/intake_state/"
        f"{intake_input.run_id}.yaml"
    )


def _pending_facts_path(org_slug: str) -> Path:
    return Path(f"orgs/{org_slug}/vault/kfr/pending_facts.yaml")


def _proposal_commitments_path(org_slug: str, grant_id: str) -> Path:
    return Path(
        f"orgs/{org_slug}/vault/grants/{grant_id}/proposal_commitments.yaml"
    )


def _reject_dir(org_slug: str, run_id: str) -> Path:
    return Path(f"pipeline/validation/extractor_rejects/{org_slug}/{run_id}")


def _signature_trail_path(org_slug: str, grant_id: str, run_id: str) -> Path:
    return Path(
        f"pipeline/validation/extractor_signature_verification/"
        f"{org_slug}/{grant_id}/{run_id}.yaml"
    )


def _serialize(obj: Any) -> Any:
    if isinstance(obj, datetime):
        return _utc_iso(obj)
    if isinstance(obj, Path):
        return str(obj)
    if isinstance(obj, Mapping):
        return {k: _serialize(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_serialize(x) for x in obj]
    return obj


def _dump_state(state: IntakeState, vault_root: Path) -> Path:
    path = vault_root / _state_file_path_for(state)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {k: _serialize(v) for k, v in asdict(state).items()}
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return path


def _state_file_path_for(state: IntakeState) -> Path:
    return Path(
        f"orgs/{state.org_slug}/vault/kfr/intake_state/{state.run_id}.yaml"
    )


def _append_pending_facts(
    *,
    facts: Sequence[PendingFact],
    org_slug: str,
    run_id: str,
    vault_root: Path,
) -> Path:
    path = vault_root / _pending_facts_path(org_slug)
    path.parent.mkdir(parents=True, exist_ok=True)
    existing: dict[str, Any] = {
        "schema_version": _SCHEMA_VERSION_PENDING,
        "org_slug": org_slug,
        "queue_populated_at": _utc_iso(_utc_now()),
        "queue_populated_by": f"intake@{run_id}",
        "pending_facts": [],
    }
    if path.is_file():
        try:
            existing = json.loads(path.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001 — fall back to fresh queue if corrupt
            existing = {
                "schema_version": _SCHEMA_VERSION_PENDING,
                "org_slug": org_slug,
                "queue_populated_at": _utc_iso(_utc_now()),
                "queue_populated_by": f"intake@{run_id}",
                "pending_facts": [],
            }
    rows = list(existing.get("pending_facts", []))
    for fact in facts:
        rows.append({k: _serialize(v) for k, v in asdict(fact).items()})
    existing["pending_facts"] = rows
    existing["queue_populated_at"] = _utc_iso(_utc_now())
    path.write_text(
        json.dumps(existing, indent=2, sort_keys=True), encoding="utf-8"
    )
    return path


def _write_proposal_commitments(
    *,
    commitments: Sequence[ProposalCommitment],
    org_slug: str,
    grant_id: str,
    run_id: str,
    vault_root: Path,
) -> Path:
    path = vault_root / _proposal_commitments_path(org_slug, grant_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": _SCHEMA_VERSION_COMMITMENTS,
        "org_slug": org_slug,
        "grant_id": grant_id,
        "intake_run_id": run_id,
        "queue_populated_at": _utc_iso(_utc_now()),
        "queue_populated_by": f"intake@{run_id}",
        "status": _STATUS_PENDING_REVIEW,
        "proposal_commitments": [
            {k: _serialize(v) for k, v in asdict(c).items()} for c in commitments
        ],
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return path


def _write_reject(
    *,
    org_slug: str,
    run_id: str,
    candidate: ExtractedCandidate | ExtractedCommitment,
    parsed: ParsedDocument,
    gate_result: GateResult,
    vault_root: Path,
) -> Path:
    reject_root = vault_root / _reject_dir(org_slug, run_id)
    reject_root.mkdir(parents=True, exist_ok=True)
    reject_id = uuid.uuid4().hex
    path = reject_root / f"{reject_id}.yaml"
    payload = {
        "reject_id": reject_id,
        "org_slug": org_slug,
        "run_id": run_id,
        "rejected_at_utc": _utc_iso(_utc_now()),
        "reject_reason_code": gate_result.code,
        "reject_sub_tag": gate_result.sub_tag,
        "reject_detail": gate_result.detail,
        "candidate": _serialize(asdict(candidate)),
        "source_doc": parsed.source_doc,
        "source_format": parsed.source_format,
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return path


def _write_signature_trail(
    *,
    award_input: IntakeAwardInput,
    proposal_result: GateResult,
    award_result: GateResult,
    vault_root: Path,
) -> Path:
    path = vault_root / _signature_trail_path(
        award_input.org_slug, award_input.grant_id, award_input.run_id,
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "run_id": award_input.run_id,
        "submission_artifact_path": award_input.submission_artifact_ref,
        "submission_signature_verified_at": (
            _utc_iso(_utc_now()) if proposal_result.passed else None
        ),
        "submission_signature_outcome": (
            "PASS" if proposal_result.passed else f"FAIL{proposal_result.sub_tag or ''}"
        ),
        "award_doc_path": award_input.award_doc_path,
        "award_doc_signature_verified_at": (
            _utc_iso(_utc_now()) if award_result.passed else None
        ),
        "award_doc_unsigned_attestation_logged": (
            award_input.award_doc_unsigned_attestation
        ),
        "award_signature_outcome": (
            "PASS" if award_result.passed else f"FAIL{award_result.sub_tag or ''}"
        ),
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# Mode handlers
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class IntakeRunResult:
    """Aggregate result returned by every mode handler."""
    state: IntakeState
    state_file_path: Path
    pending_facts_path: Path | None = None
    proposal_commitments_path: Path | None = None
    rejects_dir: Path | None = None
    signature_trail_path: Path | None = None


def _make_pre_gate_failure_state(
    *,
    intake_input: IntakeInput,
    failure: GateResult,
    vault_root: Path,
) -> IntakeRunResult:
    state = IntakeState(
        run_id=intake_input.run_id,
        org_slug=intake_input.org_slug,
        grant_id=getattr(intake_input, "grant_id", None),
        mode=intake_input.mode,
        invoked_at_utc=intake_input.invoked_at_utc,
        mode_completed=False,
        candidates_emitted_to_LLM=0,
        candidates_in_queue=0,
        candidates_rejected=0,
        failure_reason=f"{failure.code}{failure.sub_tag or ''}",
        failure_detail=failure.detail,
        trigger=getattr(intake_input, "trigger", None),
    )
    return IntakeRunResult(state=state, state_file_path=_dump_state(state, vault_root))


def _validate_and_collect_facts(
    *,
    candidates: Sequence[ExtractedCandidate],
    parsed_lookup: Mapping[str, ParsedDocument],
    mode: IntakeMode,
    threshold: float,
    run_id: str,
    org_slug: str,
    vault_root: Path,
) -> tuple[list[PendingFact], int]:
    facts: list[PendingFact] = []
    rejects = 0
    for cand in candidates:
        parsed = parsed_lookup.get(cand.source_doc)
        if parsed is None:
            rejects += 1
            _write_reject(
                org_slug=org_slug,
                run_id=run_id,
                candidate=cand,
                parsed=ParsedDocument(
                    source_doc=cand.source_doc, source_format=cand.source_format
                ),
                gate_result=GateResult.FAIL(
                    code="F-EXTRACTOR-FABRICATION",
                    sub_tag=".source_doc_unparsed",
                    detail="extractor produced candidate for a doc not in the parse map",
                ),
                vault_root=vault_root,
            )
            continue
        gate = f_extractor_fabrication(cand, mode=mode, parsed=parsed)
        if not gate.passed:
            rejects += 1
            _write_reject(
                org_slug=org_slug,
                run_id=run_id,
                candidate=cand,
                parsed=parsed,
                gate_result=gate,
                vault_root=vault_root,
            )
            continue
        autopromote = (
            cand.confidence_score >= threshold and not cand.multiple_page_match
        )
        facts.append(
            PendingFact(
                candidate_id=uuid.uuid4().hex,
                intake_run_id=run_id,
                extracted_at_utc=_utc_now(),
                source_doc=cand.source_doc,
                source_format=cand.source_format,
                source_page=cand.source_page,
                source_paragraph_id=cand.source_paragraph_id,
                source_line_id=cand.source_line_id,
                source_quote=cand.source_quote,
                confidence_score=cand.confidence_score,
                autopromote_batch=autopromote,
                multiple_page_match=cand.multiple_page_match,
                fact_payload=dict(cand.fact_payload),
            )
        )
    return facts, rejects


def _validate_and_collect_commitments(
    *,
    commitments: Sequence[ExtractedCommitment],
    parsed: ParsedDocument,
    run_id: str,
    org_slug: str,
    vault_root: Path,
) -> tuple[list[ProposalCommitment], int]:
    rows: list[ProposalCommitment] = []
    rejects = 0
    for cmt in commitments:
        gate = f_extractor_fabrication(
            cmt,
            mode="AWARD_INGEST",
            parsed=parsed,
            operator_award_page_offset_flag=cmt.page_tolerance_applied,
        )
        if not gate.passed:
            rejects += 1
            _write_reject(
                org_slug=org_slug,
                run_id=run_id,
                candidate=cmt,
                parsed=parsed,
                gate_result=gate,
                vault_root=vault_root,
            )
            continue
        # commitment_id must satisfy the safe-identifier contract
        # (^[A-Z0-9_-]+$) per §11 v1.1 amendment + §14 v1 LOCK Cycle 2
        # RT-C2-02 closure. ``uuid.uuid4().hex`` is lowercase hex; the
        # ``.upper()`` projection yields uppercase hex (32 chars of
        # [A-F0-9]) which is a strict subset of the safe regex. The
        # ``sanitize_commitment_id`` wrapper is defense-in-depth: any
        # future change to the ID generation strategy that drifts
        # outside the safe set fails closed here at extraction time
        # rather than silently writing a path-traversal-eligible
        # commitment_id into ``proposal_commitments.yaml``.
        commitment_id = _sanitize_commitment_id(uuid.uuid4().hex.upper())
        rows.append(
            ProposalCommitment(
                commitment_id=commitment_id,
                intake_run_id=run_id,
                extracted_at_utc=_utc_now(),
                source_section=cmt.source_section,
                commitment_text=cmt.commitment_text,
                commitment_proposal_offset=cmt.commitment_proposal_offset,
                measurable_metric=cmt.measurable_metric,
                target_value=cmt.target_value,
                target_unit=cmt.target_unit,
                due_period=cmt.due_period,
                page_tolerance_applied=cmt.page_tolerance_applied,
                kfr_fact_ref=cmt.kfr_fact_ref,
            )
        )
    return rows, rejects


def _sweep_inbox(
    inbox_dir: Path,
    *,
    mode: IntakeMode,
) -> tuple[list[Path], list[str]]:
    """Yield (supported, skipped) paths from a directory sweep."""
    supported: list[Path] = []
    skipped: list[str] = []
    for entry in sorted(inbox_dir.rglob("*")):
        if not entry.is_file():
            continue
        name = entry.name
        if name.startswith(".") or name in {".gitkeep"}:
            continue
        result = f_intake_unsupported_format(str(entry), mode=mode)
        if not result.passed:
            skipped.append(str(entry))
            continue
        supported.append(entry)
    return supported, skipped


def bulk_ingest(
    intake_input: IntakeBulkInput,
    *,
    parser: DocumentParserProtocol,
    extractor: FactExtractorProtocol,
    vault_root: Path = Path("."),
) -> IntakeRunResult:
    """BULK_INGEST handler. Per §11.6.1.

    Sweeps ``inbox_dir`` (or runs MIGRATION_BULK_INGEST against a single
    PROJECT_CONTEXT.md if ``migration_target_path`` is set), parses each
    supported file, calls ``extractor.extract_facts``, validates each
    candidate via F-EXTRACTOR-FABRICATION, and writes the queue + state +
    audit-trail files.
    """
    for predicate in (f_intake_org_cross_ref, f_intake_input_missing):
        gate = predicate(intake_input)
        if not gate.passed:
            return _make_pre_gate_failure_state(
                intake_input=intake_input, failure=gate, vault_root=vault_root,
            )

    if intake_input.migration_target_path is not None:
        target = _resolve(intake_input.migration_target_path)
        sources: list[Path] = [target]
        skipped_unsupported: list[str] = []
    else:
        inbox_root = _resolve(intake_input.inbox_dir)
        sources, skipped_unsupported = _sweep_inbox(inbox_root, mode="BULK_INGEST")

    parsed_lookup: dict[str, ParsedDocument] = {}
    all_candidates: list[ExtractedCandidate] = []
    docs_processed: list[str] = []
    for src in sources:
        fmt = _format_from_extension(str(src))
        if fmt is None or fmt not in SUPPORTED_FORMATS:
            skipped_unsupported.append(str(src))
            continue
        parsed = parser.parse(str(src), fmt)
        parsed_lookup[str(src)] = parsed
        all_candidates.extend(extractor.extract_facts(
            org_slug=intake_input.org_slug, parsed=parsed,
        ))
        docs_processed.append(str(src))

    facts, rejects = _validate_and_collect_facts(
        candidates=all_candidates,
        parsed_lookup=parsed_lookup,
        mode="BULK_INGEST",
        threshold=intake_input.confidence_autopromote_threshold,
        run_id=intake_input.run_id,
        org_slug=intake_input.org_slug,
        vault_root=vault_root,
    )

    queue_path: Path | None = None
    if facts:
        queue_path = _append_pending_facts(
            facts=facts,
            org_slug=intake_input.org_slug,
            run_id=intake_input.run_id,
            vault_root=vault_root,
        )

    state = IntakeState(
        run_id=intake_input.run_id,
        org_slug=intake_input.org_slug,
        grant_id=None,
        mode="BULK_INGEST",
        invoked_at_utc=intake_input.invoked_at_utc,
        mode_completed=True,
        candidates_emitted_to_LLM=len(all_candidates),
        candidates_in_queue=len(facts),
        candidates_rejected=rejects,
        docs_processed=tuple(docs_processed),
        skipped_unsupported=tuple(skipped_unsupported),
    )
    state_path = _dump_state(state, vault_root)
    return IntakeRunResult(
        state=state,
        state_file_path=state_path,
        pending_facts_path=queue_path,
        rejects_dir=(
            vault_root / _reject_dir(intake_input.org_slug, intake_input.run_id)
            if rejects else None
        ),
    )


def incremental_ingest(
    intake_input: IntakeIncrementalInput,
    *,
    parser: DocumentParserProtocol,
    extractor: FactExtractorProtocol,
    vault_root: Path = Path("."),
) -> IntakeRunResult:
    """INCREMENTAL_INGEST handler. Per §11.6.2."""
    for predicate in (f_intake_org_cross_ref, f_intake_input_missing):
        gate = predicate(intake_input)
        if not gate.passed:
            return _make_pre_gate_failure_state(
                intake_input=intake_input, failure=gate, vault_root=vault_root,
            )

    fmt_gate = f_intake_unsupported_format(
        intake_input.doc_path, mode="INCREMENTAL_INGEST",
    )
    if not fmt_gate.passed:
        return _make_pre_gate_failure_state(
            intake_input=intake_input, failure=fmt_gate, vault_root=vault_root,
        )

    toctou = f_intake_watcher_toctou(
        intake_input.doc_path,
        expected_org_subtree=f"orgs/{intake_input.org_slug}/intake/inbox",
    )
    if not toctou.passed:
        return _make_pre_gate_failure_state(
            intake_input=intake_input, failure=toctou, vault_root=vault_root,
        )

    fmt = _format_from_extension(intake_input.doc_path)
    assert fmt is not None  # gate above guaranteed
    parsed = parser.parse(intake_input.doc_path, fmt)
    candidates = list(extractor.extract_facts(
        org_slug=intake_input.org_slug, parsed=parsed,
    ))
    facts, rejects = _validate_and_collect_facts(
        candidates=candidates,
        parsed_lookup={parsed.source_doc: parsed, intake_input.doc_path: parsed},
        mode="INCREMENTAL_INGEST",
        threshold=intake_input.confidence_autopromote_threshold,
        run_id=intake_input.run_id,
        org_slug=intake_input.org_slug,
        vault_root=vault_root,
    )
    queue_path: Path | None = None
    if facts:
        queue_path = _append_pending_facts(
            facts=facts,
            org_slug=intake_input.org_slug,
            run_id=intake_input.run_id,
            vault_root=vault_root,
        )
    state = IntakeState(
        run_id=intake_input.run_id,
        org_slug=intake_input.org_slug,
        grant_id=None,
        mode="INCREMENTAL_INGEST",
        invoked_at_utc=intake_input.invoked_at_utc,
        mode_completed=True,
        candidates_emitted_to_LLM=len(candidates),
        candidates_in_queue=len(facts),
        candidates_rejected=rejects,
        trigger=intake_input.trigger,
        docs_processed=(intake_input.doc_path,),
    )
    state_path = _dump_state(state, vault_root)
    return IntakeRunResult(
        state=state,
        state_file_path=state_path,
        pending_facts_path=queue_path,
        rejects_dir=(
            vault_root / _reject_dir(intake_input.org_slug, intake_input.run_id)
            if rejects else None
        ),
    )


def award_ingest(
    intake_input: IntakeAwardInput,
    *,
    parser: DocumentParserProtocol,
    extractor: CommitmentExtractorProtocol,
    signed_claim_evidence_map: SignedClaimEvidenceMap,
    funder_signature_material: FunderSignatureMaterial | None,
    signature_verify: SignatureVerifyCallable,
    key_active_lookup: KeyActiveLookupCallable,
    vault_root: Path = Path("."),
) -> IntakeRunResult:
    """AWARD_INGEST handler. Per §11.6.3."""
    for predicate in (f_intake_org_cross_ref, f_intake_input_missing):
        gate = predicate(intake_input)
        if not gate.passed:
            return _make_pre_gate_failure_state(
                intake_input=intake_input, failure=gate, vault_root=vault_root,
            )

    award_fmt_gate = f_intake_unsupported_format(
        intake_input.award_doc_path, mode="AWARD_INGEST",
    )
    if not award_fmt_gate.passed:
        return _make_pre_gate_failure_state(
            intake_input=intake_input, failure=award_fmt_gate, vault_root=vault_root,
        )

    submission_path = _resolve(intake_input.submission_artifact_ref)
    submission_bytes = submission_path.read_bytes()

    proposal_gate = f_extractor_award_signature_invalid_proposal(
        intake_input,
        submission_artifact_bytes=submission_bytes,
        signed_claim_evidence_map=signed_claim_evidence_map,
        signature_verify=signature_verify,
        key_active_lookup=key_active_lookup,
    )
    award_gate = (
        f_extractor_award_signature_invalid_award(
            intake_input,
            funder_signature_material=funder_signature_material,
            signature_verify=signature_verify,
        )
        if proposal_gate.passed
        else GateResult.FAIL(
            code="F-EXTRACTOR-AWARD-SIGNATURE-INVALID",
            sub_tag=".skipped_after_proposal_failure",
            detail="award leg not evaluated due to proposal-leg failure",
        )
    )

    trail_path = _write_signature_trail(
        award_input=intake_input,
        proposal_result=proposal_gate,
        award_result=award_gate,
        vault_root=vault_root,
    )

    if not proposal_gate.passed:
        result = _make_pre_gate_failure_state(
            intake_input=intake_input, failure=proposal_gate, vault_root=vault_root,
        )
        return IntakeRunResult(
            state=result.state,
            state_file_path=result.state_file_path,
            signature_trail_path=trail_path,
        )
    if not award_gate.passed:
        result = _make_pre_gate_failure_state(
            intake_input=intake_input, failure=award_gate, vault_root=vault_root,
        )
        return IntakeRunResult(
            state=result.state,
            state_file_path=result.state_file_path,
            signature_trail_path=trail_path,
        )

    parsed = parser.parse(intake_input.submission_artifact_ref, SOURCE_FORMAT_MD)
    commitments_raw = list(extractor.extract_commitments(
        org_slug=intake_input.org_slug,
        grant_id=intake_input.grant_id,
        parsed=parsed,
    ))
    rows, rejects = _validate_and_collect_commitments(
        commitments=commitments_raw,
        parsed=parsed,
        run_id=intake_input.run_id,
        org_slug=intake_input.org_slug,
        vault_root=vault_root,
    )
    commitments_path = _write_proposal_commitments(
        commitments=rows,
        org_slug=intake_input.org_slug,
        grant_id=intake_input.grant_id,
        run_id=intake_input.run_id,
        vault_root=vault_root,
    )

    state = IntakeState(
        run_id=intake_input.run_id,
        org_slug=intake_input.org_slug,
        grant_id=intake_input.grant_id,
        mode="AWARD_INGEST",
        invoked_at_utc=intake_input.invoked_at_utc,
        mode_completed=True,
        candidates_emitted_to_LLM=len(commitments_raw),
        candidates_in_queue=len(rows),
        candidates_rejected=rejects,
        trigger="operator_explicit_award",
        docs_processed=(
            intake_input.submission_artifact_ref,
            intake_input.award_doc_path,
        ),
    )
    state_path = _dump_state(state, vault_root)
    return IntakeRunResult(
        state=state,
        state_file_path=state_path,
        proposal_commitments_path=commitments_path,
        signature_trail_path=trail_path,
        rejects_dir=(
            vault_root / _reject_dir(intake_input.org_slug, intake_input.run_id)
            if rejects else None
        ),
    )


__all__ = [
    "IntakeMode",
    "IntakeBulkInput",
    "IntakeIncrementalInput",
    "IntakeAwardInput",
    "IntakeInput",
    "IntakeState",
    "IntakeRunResult",
    "PendingFact",
    "ProposalCommitment",
    "GateResult",
    "ParsedDocument",
    "DocumentParserProtocol",
    "ExtractedCandidate",
    "ExtractedCommitment",
    "FactExtractorProtocol",
    "CommitmentExtractorProtocol",
    "SignedConfigBlock",
    "SignedClaimEvidenceMap",
    "FunderSignatureMaterial",
    "SignatureVerifyCallable",
    "KeyActiveLookupCallable",
    "SOURCE_FORMAT_PDF",
    "SOURCE_FORMAT_DOCX",
    "SOURCE_FORMAT_TXT",
    "SOURCE_FORMAT_MD",
    "SUPPORTED_FORMATS",
    "AWARD_DOC_FORMATS",
    "LOCALHOST_HOSTS",
    "get_mode_handler_name",
    "list_registered_modes",
    "f_intake_org_cross_ref",
    "f_intake_input_missing",
    "f_intake_unsupported_format",
    "f_intake_embedding_ns_mismatch",
    "f_intake_config_signature_invalid",
    "f_intake_embedding_endpoint_invalid",
    "f_intake_watcher_toctou",
    "f_intake_queue_integrity_pre_run",
    "f_intake_queue_integrity_post_write",
    "f_extractor_fabrication",
    "f_extractor_award_signature_invalid_proposal",
    "f_extractor_award_signature_invalid_award",
    "bulk_ingest",
    "incremental_ingest",
    "award_ingest",
]
