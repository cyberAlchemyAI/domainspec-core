#!/usr/bin/env python3
"""
Uploader support agent — submission package assembly.

Per Blueprint §12: assembles operator-approved final proposal into
funder-portal-required formats. Stages the package for operator review.
Surfaces a readiness checklist. DOES NOT auto-submit.

The operator clicks final submit on the funder portal — this constraint
is non-negotiable (federal-portal ToS + operator-accountability).

Substrate: deterministic Python over python-docx + pypdf + openpyxl
+ per-portal adapters. Zero LLM calls. Always-local routing.

Logician gates owned:
  F-UPLOADER-PACKAGE-INCOMPLETE    (POST — missing RFA-required sections/attachments)
  F-UPLOADER-FORMAT-MISMATCH       (POST — wrong format / page-limit / file-size)
  F-UPLOADER-AUTOSUBMIT-ATTEMPTED  (PRE — fail-closed, no M13 bypass)
  F-UPLOADER-SIGNATURE-MISSING     (PRE — no operator sign-off)
  F-UPLOADER-CONTENT-MUTATION      (POST — text changed during format conversion)
  F-UPLOADER-ATTACHMENT-TAMPERED   (PRE — attachment hash mismatch)
  F-UPLOADER-ATTACHMENT-MISSING    (PRE — attachment file not on disk)
  F-UPLOADER-INPUT-INCONSISTENT    (PRE — claim_evidence_map vs section_drafts mismatch)
  F-UPLOADER-RFA-MISSING           (PRE — RFA record absent or hash mismatch)
  F-UPLOADER-SIGNATURE-MISMATCH    (PRE — bundle modified after signature)
  F-UPLOADER-ORG-CROSS-REF         (PRE — multi-org paths in input)

Module scaffold authored at §12 v1 LOCK. Full implementation is downstream.
"""

from __future__ import annotations

import hashlib
import json
import os
import os.path
import re
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Final, Literal, Protocol, final, runtime_checkable

import yaml

import docx
import openpyxl
import pypdf


# Timezone-aware UTC factory. ``datetime.UTC`` is 3.11+, ``timezone.utc`` is
# the 3.10-compatible equivalent — pyproject pins >=3.11 so either works,
# but ``timezone.utc`` keeps a single import path across Python versions.
def _utc_now() -> datetime:
    """Return a timezone-aware UTC datetime (replaces ``datetime.utcnow()``)."""
    return datetime.now(timezone.utc)


# ---------------------------------------------------------------------------
# Core data models (frozen, kw_only per Tilth convention)
# ---------------------------------------------------------------------------

@dataclass(frozen=True, kw_only=True)
class OperatorSignature:
    """Operator's sign-off on the final SubmissionBundle."""
    signed_at_utc: datetime
    signer_id: str
    bundle_content_hash: str  # SHA3-512 of SubmissionBundle bytes


@dataclass(frozen=True, kw_only=True)
class AttachmentRef:
    """Reference to an operator-uploaded attachment file."""
    file_path: str  # vault path under orgs/<slug>/vault/grants/<grant_id>/attachments/
    original_file_name: str
    content_sha3_512: str
    uploaded_at_utc: datetime
    uploaded_by: str
    rfa_attachment_match: str | None  # which required_attachment entry this satisfies


@dataclass(frozen=True, kw_only=True)
class AttachmentProvenance:
    """Provenance record for an attachment at assembly time."""
    attachment_ref: AttachmentRef
    hash_verified_at_assembly: bool
    format_at_assembly: str


@dataclass(frozen=True, kw_only=True)
class PortalConfig:
    """Per-portal configuration overrides."""
    foundant_portal_id: str | None = None
    submittable_form_id: str | None = None
    fluxx_portal_id: str | None = None
    character_limits: dict[str, int] | None = None  # field_id -> max chars


@dataclass(frozen=True, kw_only=True)
class UploaderInput:
    """Input bundle for Uploader. Consumed after §5 submission_mode terminus."""
    run_id: str
    grant_id: str
    org_slug: str
    submission_bundle_ref: str  # vault path to signed SubmissionBundle
    section_drafts: tuple  # tuple[SectionDraft, ...] — from §7.5
    claim_evidence_map: tuple  # tuple[ClaimEvidence, ...]
    rfa_extracted_record: object  # RfaExtractedRecord from §7.3
    operator_signature: OperatorSignature | None
    attachments: tuple[AttachmentRef, ...] = ()
    target_portal: Literal[
        "grants_gov", "sam_gov", "common_grant_app",
        "foundant", "submittable", "fluxx", "copy_paste",
    ] = "copy_paste"
    portal_config: PortalConfig | None = None
    prepared_at_utc: datetime = field(default_factory=_utc_now)


@dataclass(frozen=True, kw_only=True)
class ManifestEntry:
    """Single entry in the submission manifest."""
    file_name: str
    portal_file_name: str
    format: Literal["pdf", "docx", "xlsx", "yaml", "txt", "other"]
    source: Literal["council_draft", "attachment", "portal_field_export", "readiness_checklist"]
    source_ref: str
    content_sha3_512: str
    page_count: int | None = None
    file_size_bytes: int = 0
    portal_section: str | None = None


@dataclass(frozen=True, kw_only=True)
class SubmissionManifest:
    """Complete manifest of the staged submission package."""
    entries: tuple[ManifestEntry, ...]
    assembled_at_utc: datetime
    adapter_id: str
    run_id: str

    def has_section(self, section_name: str) -> bool:
        return any(
            e.portal_section == section_name
            for e in self.entries
            if e.source == "council_draft"
        )


@dataclass(frozen=True, kw_only=True)
class PortalField:
    """A single portal form field with its value and provenance."""
    field_id: str
    field_label: str
    value: str
    source: str
    instructions: str = ""


@dataclass(frozen=True, kw_only=True)
class ChecklistItem:
    """Single readiness checklist item."""
    check_id: str
    status: Literal["pass", "fail", "warn"]
    detail: str
    source: str | None = None


@dataclass(frozen=True, kw_only=True)
class ReadinessChecklist:
    """Self-validation result for the submission package (Rule 2)."""
    overall_status: Literal["ready", "not_ready"]
    items: tuple[ChecklistItem, ...]
    fail_count: int
    warn_count: int
    pass_count: int
    checked_at_utc: datetime


@final
@dataclass(frozen=True, kw_only=True)
class UploaderOutput:
    """Uploader's output — the staged submission package metadata.

    Decorated ``@typing.final`` and overrides ``__init_subclass__`` to raise
    so that subclassing UploaderOutput cannot bypass the
    F-UPLOADER-AUTOSUBMIT-ATTEMPTED runtime invariant by overriding
    ``__post_init__``. Closes the RT-1f / RT-1h subclass-bypass paths
    surfaced in §12 v1 Audit #1 (2026-05-10).
    """
    run_id: str
    manifest: SubmissionManifest
    readiness_checklist: ReadinessChecklist
    output_dir: str
    submitted: bool = False  # ALWAYS False — structural invariant
    prepared_at_utc: datetime = field(default_factory=_utc_now)

    def __init_subclass__(cls, **kwargs: object) -> None:
        # Block subclassing entirely. ``@typing.final`` is a static-analysis
        # hint; this runtime guard fails at class-creation time.
        raise TypeError(
            "F-UPLOADER-AUTOSUBMIT-ATTEMPTED: UploaderOutput is final. "
            "Subclassing is prohibited because a subclass could override "
            "__post_init__ to bypass the runtime auto-submit invariant. "
            f"(attempted subclass: {cls.__name__!r})"
        )

    def __post_init__(self) -> None:
        # F-UPLOADER-AUTOSUBMIT-ATTEMPTED runtime layer (Layer 3 of three).
        # Explicit raise (NOT assert) so `python -O` cannot strip the check.
        # `dataclasses.replace(out, submitted=True)` calls __init__ on the
        # new instance, which calls __post_init__ here, which raises — so the
        # replace bypass is foreclosed by Layer 3 alone.
        if self.submitted is True:
            raise RuntimeError(
                "F-UPLOADER-AUTOSUBMIT-ATTEMPTED: Uploader output must never "
                "have submitted=True. Auto-submit is architecturally "
                "prohibited. No bypass via python -O, no bypass via "
                "dataclasses.replace, no M13 escape valve."
            )


@dataclass(frozen=True, kw_only=True)
class UploaderState:
    """Persistent state per Rule 1 — saved on success AND failure."""
    run_id: str
    grant_id: str
    org_slug: str
    adapter_id: str
    assembly_attempted_at_utc: datetime
    assembly_succeeded: bool
    sections_assembled: tuple[str, ...]
    sections_failed: tuple[str, ...]
    attachments_staged: int
    readiness_status: str | None  # "ready" | "not_ready" | None if not reached
    failure_reason: str | None = None


# ---------------------------------------------------------------------------
# Gate results
# ---------------------------------------------------------------------------

@dataclass(frozen=True, kw_only=True)
class GateResult:
    """Result of a Logician gate check."""
    passed: bool
    code: str | None = None
    detail: str | None = None

    @classmethod
    def PASS(cls) -> GateResult:
        return cls(passed=True)

    @classmethod
    def FAIL(cls, *, code: str, detail: str) -> GateResult:
        return cls(passed=False, code=code, detail=detail)


# ---------------------------------------------------------------------------
# Logician gates (deterministic Python predicates, zero token cost)
# ---------------------------------------------------------------------------

def _check_signature_presence(uploader_input: UploaderInput) -> bool:
    """Return True iff operator signature is present on the input bundle.

    Single-purpose predicate per §12.9.5 audit-trail clarity. Used by the
    PRE-31 (F-UPLOADER-SIGNATURE-MISSING) wrapper to decide PASS/FAIL.
    """
    return uploader_input.operator_signature is not None


def _check_signature_hash(
    uploader_input: UploaderInput,
    bundle_bytes: bytes,
) -> bool:
    """Return True iff the operator signature hash matches the bundle bytes.

    Single-purpose predicate per §12.9.5. Caller is responsible for first
    confirming presence via :func:`_check_signature_presence` — this
    function returns False when the signature is absent (no signature → no
    matching hash possible), but the discrimination between MISSING and
    MISMATCH belongs to the §4 wrappers, not here.
    """
    if uploader_input.operator_signature is None:
        return False
    computed_hash = hashlib.sha3_512(bundle_bytes).hexdigest()
    return uploader_input.operator_signature.bundle_content_hash == computed_hash


def f_uploader_signature_missing(
    uploader_input: UploaderInput,
    submission_bundle_bytes: bytes,
) -> GateResult:
    """PRE-gate composition: operator signature present and hash matches.

    Backwards-compat wrapper kept for callers that want both checks in one
    surface. The §4 wrappers (`f_uploader_signature_missing` /
    `f_uploader_signature_mismatch` modules in `pipeline/logician/gates/`)
    call the single-purpose predicates above instead so each Logician
    surface owns exactly one failure code.
    """
    if not _check_signature_presence(uploader_input):
        return GateResult.FAIL(
            code="F-UPLOADER-SIGNATURE-MISSING",
            detail="No operator signature on submission bundle.",
        )
    if not _check_signature_hash(uploader_input, submission_bundle_bytes):
        # Signature is present but hash differs — MISMATCH discrimination.
        # We re-compute here purely for the diagnostic detail string.
        computed_hash = hashlib.sha3_512(submission_bundle_bytes).hexdigest()
        assert uploader_input.operator_signature is not None  # type-narrow
        return GateResult.FAIL(
            code="F-UPLOADER-SIGNATURE-MISMATCH",
            detail=(
                f"Signature hash mismatch: expected {computed_hash[:32]}..., "
                f"got {uploader_input.operator_signature.bundle_content_hash[:32]}..."
            ),
        )
    return GateResult.PASS()


def _extract_org_slug(path: str) -> str | None:
    """Return the org slug from any path under ``orgs/<slug>/...``, else None."""
    if not path:
        return None
    parts = path.split("/")
    if len(parts) >= 2 and parts[0] == "orgs":
        return parts[1]
    return None


def f_uploader_org_cross_ref(uploader_input: UploaderInput) -> GateResult:
    """PRE-gate: input references only one org slug.

    Sweeps:
      - the declared ``org_slug`` field;
      - every ``AttachmentRef.file_path``;
      - the ``submission_bundle_ref`` itself (a bundle ref pointing into
        another org's vault is the same Law-3 violation as a stray
        attachment, and would otherwise sneak past §4 PRE-36).
    """
    slugs: set[str] = {uploader_input.org_slug}
    for att in uploader_input.attachments:
        slug = _extract_org_slug(att.file_path)
        if slug is not None:
            slugs.add(slug)
    bundle_slug = _extract_org_slug(uploader_input.submission_bundle_ref)
    if bundle_slug is not None:
        slugs.add(bundle_slug)
    if len(slugs) > 1:
        return GateResult.FAIL(
            code="F-UPLOADER-ORG-CROSS-REF",
            detail=f"Multiple org slugs in input: {sorted(slugs)}",
        )
    return GateResult.PASS()


def f_uploader_autosubmit_check() -> None:
    """
    Structural assertion — this function exists as documentation that
    auto-submit is architecturally prohibited. The actual enforcement is:
    1. AST-lint rule R-UPLOADER-NO-SUBMIT (static analysis)
    2. Cedar policy uploader_no_submit.cedar
    3. UploaderOutput.__post_init__ assertion (runtime)
    No M13 bypass.
    """
    pass  # Enforcement is structural, not runtime-callable


# ---------------------------------------------------------------------------
# Portal adapter protocol
# ---------------------------------------------------------------------------

@runtime_checkable
class PortalAdapterProtocol(Protocol):
    """Contract every portal adapter satisfies. Per §12.10."""

    @property
    def portal_id(self) -> str: ...

    def required_format(self, portal_section: str | None) -> str | None: ...

    def page_limit(self, portal_section: str | None) -> int | None: ...

    def file_size_limit(self, portal_section: str | None) -> int | None: ...

    def filename_convention(self, portal_section: str | None, original_name: str) -> str: ...

    def map_fields(
        self,
        rfa: object,
        section_drafts: tuple,
        project_context: object,
    ) -> tuple[PortalField, ...]: ...

    def assemble_package(
        self,
        section_drafts: tuple,
        attachments: tuple[AttachmentRef, ...],
        rfa: object,
        output_dir: str,
    ) -> SubmissionManifest: ...


# ---------------------------------------------------------------------------
# Adapter registry
# ---------------------------------------------------------------------------

ADAPTER_REGISTRY: dict[str, type] = {}
# Populated by adapter module imports — each adapter registers itself.
# e.g., from uploader_adapters.grants_gov import GrantsGovAdapter
#        ADAPTER_REGISTRY["grants_gov"] = GrantsGovAdapter


def get_adapter(portal: str) -> type:
    """Look up the adapter class for a portal identifier."""
    if portal not in ADAPTER_REGISTRY:
        raise ValueError(
            f"Unknown portal '{portal}'. Available: {sorted(ADAPTER_REGISTRY)}"
        )
    return ADAPTER_REGISTRY[portal]


# ---------------------------------------------------------------------------
# Local-LLM call routing (per §12.9.6 / §12.11)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class FieldMapCallContext:
    """Context object passed to F-UPLOADER-FIELD-MAP-CLOUD-ROUTED at every
    portal-field-disambiguation LLM call site (§12.9.6 RT-5a).

    Mirrors `pipeline.logician.gates.f_uploader_field_map_cloud_routed.
    FieldMapCallContext` — duplicated here so adapter code can construct
    the context without importing from the gate module (the gate module
    is the §4 Logician registration; this is the seat-side surface).
    """

    portal_field_id: str
    portal_field_label: str
    caller_module: str
    routed_to: Literal["local", "cloud"]
    model_id: str
    classification_at_call: Literal["public", "shareable", "confidential"]


def gate_field_map_call(ctx: FieldMapCallContext) -> GateResult:
    """PRE-gate wrapper invoked at every portal-field-disambiguation site.

    Delegates to the §4 Logician predicate; surfaces the GateResult in
    the same shape Uploader uses for the rest of its gate fan-out. Per
    §12.9.6 wiring discipline: every adapter's ``map_fields`` that issues
    an LLM disambiguation call MUST construct a ``FieldMapCallContext``
    and call this wrapper BEFORE invoking the model.
    """
    from pipeline.logician.gates.f_uploader_field_map_cloud_routed import (
        check_uploader_field_map_cloud_routed,
    )
    return check_uploader_field_map_cloud_routed(ctx)


# ---------------------------------------------------------------------------
# Field-map LLM endpoint contract (always-local per §12.11)
# ---------------------------------------------------------------------------


@runtime_checkable
class LocalLLMEndpoint(Protocol):
    """Always-local Mistral-7B-class endpoint for field disambiguation.

    Concrete binding lives in production at the Pydantic AI tool layer;
    tests inject a stub. The endpoint MUST be loopback-bound (127.0.0.1
    or ::1) — F-UPLOADER-FIELD-MAP-CLOUD-ROUTED catches any non-local
    routing decision the caller might make.
    """

    @property
    def model_id(self) -> str: ...

    @property
    def host(self) -> str: ...

    def disambiguate(
        self,
        *,
        portal_field_id: str,
        portal_field_label: str,
        candidates: tuple[str, ...],
    ) -> str: ...


# ---------------------------------------------------------------------------
# Substrate helpers — DOCX / PDF / XLSX I/O
# ---------------------------------------------------------------------------


_FILENAME_SAFE = re.compile(r"[^A-Za-z0-9._-]+")
_WHITESPACE_RUN = re.compile(r"\s+")


def _safe_filename(name: str) -> str:
    """Strip filesystem-unsafe characters; collapse whitespace to underscore."""
    cleaned = _FILENAME_SAFE.sub("_", name).strip("_")
    if not cleaned:
        cleaned = "untitled"
    return cleaned


def _normalize_text(text: str) -> str:
    """Whitespace-collapse for content-mutation comparisons (§12.8.1)."""
    return _WHITESPACE_RUN.sub(" ", text).strip()


def _hash_file(path: Path) -> str:
    """SHA3-512 hex digest of a file's bytes."""
    data = path.read_bytes()
    return hashlib.sha3_512(data).hexdigest()


def render_section_to_docx(
    *,
    section_name: str,
    body_text: str,
    output_path: Path,
) -> int:
    """Write a SectionDraft.body_text to a DOCX file. Return file size in bytes.

    Uses python-docx (substrate per ADR-001). Heading is the section name;
    each paragraph in body_text becomes a python-docx paragraph. No
    formatting beyond paragraph breaks — Uploader is a renderer, not an
    editor (§12.2 Law 2).
    """
    document = docx.Document()
    document.add_heading(section_name, level=1)
    paragraphs = body_text.split("\n\n") if body_text else [""]
    for para in paragraphs:
        document.add_paragraph(para)
    document.save(str(output_path))
    return output_path.stat().st_size


def extract_docx_text(path: Path) -> str:
    """Extract concatenated paragraph text from a DOCX file (no styling)."""
    document = docx.Document(str(path))
    parts: list[str] = []
    for paragraph in document.paragraphs:
        parts.append(paragraph.text)
    return "\n".join(parts)


def count_pdf_pages(path: Path) -> int:
    """Return the page count of a PDF file via pypdf."""
    reader = pypdf.PdfReader(str(path))
    return len(reader.pages)


def extract_pdf_text(path: Path) -> str:
    """Extract concatenated text from a PDF file via pypdf."""
    reader = pypdf.PdfReader(str(path))
    parts: list[str] = []
    for page in reader.pages:
        parts.append(page.extract_text() or "")
    return "\n".join(parts)


def write_xlsx_validation_workbook(
    *,
    rows: tuple[tuple[str, str], ...],
    output_path: Path,
    sheet_name: str = "validation",
) -> int:
    """Write a 2-column workbook (label, value) for SAM validation reports
    or budget-form scaffolds. Return file size in bytes.
    """
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = sheet_name
    worksheet.append(("label", "value"))
    for label, value in rows:
        worksheet.append((label, value))
    workbook.save(str(output_path))
    return output_path.stat().st_size


# ---------------------------------------------------------------------------
# DOCX → PDF conversion via LibreOffice headless subprocess
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class DocxToPdfConverter:
    """Subprocess-launching DOCX→PDF converter.

    Uses LibreOffice headless mode per §12.8 — the only subprocess target
    permitted by AST-lint allow-list (`subprocess.run` with `check=True`
    and `argv[0] == "soffice"`).

    Tests can construct this with a custom ``soffice_path`` (e.g. the
    macOS bundle path) or replace the converter wholesale via dependency
    injection.
    """

    soffice_path: str = "soffice"
    timeout_seconds: int = 120

    def convert(self, *, docx_path: Path, output_dir: Path) -> Path:
        """Convert one DOCX into a PDF in output_dir; return the PDF path.

        Raises FileNotFoundError if soffice is not on PATH (caller may
        handle by leaving the entry as DOCX and surfacing
        F-UPLOADER-FORMAT-MISMATCH at the readiness checklist).
        Raises subprocess.CalledProcessError if soffice exits non-zero.
        """
        argv = [
            self.soffice_path,
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            str(output_dir),
            str(docx_path),
        ]
        subprocess.run(  # noqa: S603 — soffice-only path; AST-lint allow-list
            argv,
            check=True,
            timeout=self.timeout_seconds,
            capture_output=True,
        )
        pdf_path = output_dir / (docx_path.stem + ".pdf")
        if not pdf_path.exists():
            raise FileNotFoundError(
                f"LibreOffice produced no output at {pdf_path}"
            )
        return pdf_path


# ---------------------------------------------------------------------------
# Manifest builders + readiness checklist
# ---------------------------------------------------------------------------


def build_manifest_entry(
    *,
    file_path: Path,
    portal_file_name: str,
    fmt: Literal["pdf", "docx", "xlsx", "yaml", "txt", "other"],
    source: Literal["council_draft", "attachment", "portal_field_export", "readiness_checklist"],
    source_ref: str,
    portal_section: str | None = None,
) -> ManifestEntry:
    """Build a ManifestEntry from a staged file's on-disk state."""
    page_count: int | None = None
    if fmt == "pdf":
        page_count = count_pdf_pages(file_path)
    return ManifestEntry(
        file_name=file_path.name,
        portal_file_name=portal_file_name,
        format=fmt,
        source=source,
        source_ref=source_ref,
        content_sha3_512=_hash_file(file_path),
        page_count=page_count,
        file_size_bytes=file_path.stat().st_size,
        portal_section=portal_section,
    )


def write_portal_fields_yaml(
    *,
    fields: tuple[PortalField, ...],
    output_path: Path,
) -> int:
    """Serialize portal fields to YAML; return file size."""
    payload = [
        {
            "field_id": f.field_id,
            "field_label": f.field_label,
            "value": f.value,
            "source": f.source,
            "instructions": f.instructions,
        }
        for f in fields
    ]
    output_path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
    return output_path.stat().st_size


def write_submission_manifest_yaml(
    *,
    manifest: SubmissionManifest,
    output_path: Path,
) -> int:
    """Serialize the SubmissionManifest to YAML; return file size."""
    assembled_at_utc = manifest.assembled_at_utc
    payload = {
        "run_id": manifest.run_id,
        "adapter_id": manifest.adapter_id,
        "assembled_at_utc": assembled_at_utc.isoformat(),
        "entries": [
            {
                "file_name": e.file_name,
                "portal_file_name": e.portal_file_name,
                "format": e.format,
                "source": e.source,
                "source_ref": e.source_ref,
                "content_sha3_512": e.content_sha3_512,
                "page_count": e.page_count,
                "file_size_bytes": e.file_size_bytes,
                "portal_section": e.portal_section,
            }
            for e in manifest.entries
        ],
    }
    output_path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
    return output_path.stat().st_size


def write_readiness_checklist_yaml(
    *,
    checklist: ReadinessChecklist,
    output_path: Path,
) -> int:
    checked_at_utc = checklist.checked_at_utc
    payload = {
        "overall_status": checklist.overall_status,
        "checked_at_utc": checked_at_utc.isoformat(),
        "fail_count": checklist.fail_count,
        "warn_count": checklist.warn_count,
        "pass_count": checklist.pass_count,
        "items": [
            {
                "check_id": i.check_id,
                "status": i.status,
                "detail": i.detail,
                "source": i.source,
            }
            for i in checklist.items
        ],
    }
    output_path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
    return output_path.stat().st_size


def build_readiness_checklist(
    *,
    rfa: object,
    manifest: SubmissionManifest,
    adapter: PortalAdapterProtocol,
    section_drafts: tuple,
    portal_fields: tuple[PortalField, ...],
    operator_signature_present: bool,
    output_dir: Path,
    content_mutation_failures: tuple[tuple[str, str], ...] = (),
) -> ReadinessChecklist:
    """Run the §12.7 readiness checklist deterministically."""
    items: list[ChecklistItem] = []

    # 1. Section completeness — every RFA section_structure entry has a manifest doc.
    section_structure = getattr(rfa, "section_structure", ()) if rfa is not None else ()
    rfa_section_names = tuple(getattr(s, "section_name", "") for s in section_structure)
    for name in rfa_section_names:
        if manifest.has_section(name):
            items.append(
                ChecklistItem(
                    check_id="section_completeness",
                    status="pass",
                    detail=f"Section {name!r} present.",
                    source=name,
                )
            )
        else:
            items.append(
                ChecklistItem(
                    check_id="section_completeness",
                    status="fail",
                    detail=f"RFA-required section {name!r} missing from manifest.",
                    source=name,
                )
            )

    # 2. Manual-attach checklist — operator-facing WARN per §12.6 (v1 deferral).
    required_attachments = (
        getattr(rfa, "required_attachments", ()) if rfa is not None else ()
    )
    for att in required_attachments:
        items.append(
            ChecklistItem(
                check_id="manual_attach_required",
                status="warn",
                detail=(
                    f"Operator must manually attach {att!r} at portal upload "
                    "time (v1 deferral per §12.6)."
                ),
                source=att,
            )
        )

    # 3. Format compliance.
    for entry in manifest.entries:
        if entry.source != "council_draft":
            continue
        expected = adapter.required_format(entry.portal_section)
        if expected is None or entry.format == expected:
            items.append(
                ChecklistItem(
                    check_id="format_compliance",
                    status="pass",
                    detail=f"{entry.file_name}: format {entry.format!r}.",
                    source=entry.file_name,
                )
            )
        else:
            items.append(
                ChecklistItem(
                    check_id="format_compliance",
                    status="fail",
                    detail=(
                        f"{entry.file_name}: expected {expected!r}, "
                        f"got {entry.format!r}."
                    ),
                    source=entry.file_name,
                )
            )

    # 4 + 5. Page-count and file-size compliance.
    for entry in manifest.entries:
        if entry.source != "council_draft":
            continue
        page_limit = adapter.page_limit(entry.portal_section)
        if (
            page_limit is not None
            and entry.page_count is not None
            and entry.page_count > page_limit
        ):
            items.append(
                ChecklistItem(
                    check_id="page_count_compliance",
                    status="fail",
                    detail=(
                        f"{entry.file_name}: {entry.page_count} pages > "
                        f"limit {page_limit}."
                    ),
                    source=entry.file_name,
                )
            )
        size_limit = adapter.file_size_limit(entry.portal_section)
        if size_limit is not None and entry.file_size_bytes > size_limit:
            items.append(
                ChecklistItem(
                    check_id="file_size_compliance",
                    status="fail",
                    detail=(
                        f"{entry.file_name}: {entry.file_size_bytes} bytes > "
                        f"limit {size_limit}."
                    ),
                    source=entry.file_name,
                )
            )

    # 6. Filename convention compliance.
    for entry in manifest.entries:
        if entry.source != "council_draft":
            continue
        suggested = adapter.filename_convention(
            entry.portal_section, entry.portal_file_name
        )
        if suggested == entry.portal_file_name:
            continue
        items.append(
            ChecklistItem(
                check_id="filename_convention",
                status="fail",
                detail=(
                    f"{entry.file_name}: portal_file_name "
                    f"{entry.portal_file_name!r} does not match adapter "
                    f"convention; suggested {suggested!r}."
                ),
                source=entry.file_name,
            )
        )

    # 7. Manifest integrity.
    extra_files: list[str] = []
    if output_dir.exists():
        manifest_files = {e.file_name for e in manifest.entries}
        for child in output_dir.iterdir():
            if not child.is_file():
                continue
            if child.name == "submission_manifest.yaml":
                continue
            if child.name == "readiness_checklist.yaml":
                continue
            if child.name not in manifest_files:
                extra_files.append(child.name)
    for entry in manifest.entries:
        on_disk = output_dir / entry.file_name
        if not on_disk.exists():
            items.append(
                ChecklistItem(
                    check_id="manifest_integrity",
                    status="fail",
                    detail=f"Manifest entry {entry.file_name!r} not on disk.",
                    source=entry.file_name,
                )
            )
            continue
        actual_hash = _hash_file(on_disk)
        if actual_hash != entry.content_sha3_512:
            items.append(
                ChecklistItem(
                    check_id="manifest_integrity",
                    status="fail",
                    detail=(
                        f"Manifest hash mismatch for {entry.file_name!r}."
                    ),
                    source=entry.file_name,
                )
            )
    for extra in extra_files:
        items.append(
            ChecklistItem(
                check_id="manifest_integrity",
                status="fail",
                detail=f"File {extra!r} on disk not in manifest.",
                source=extra,
            )
        )

    # 8. Operator signature presence (verified at PRE-gate; reported here).
    items.append(
        ChecklistItem(
            check_id="operator_signature",
            status="pass" if operator_signature_present else "fail",
            detail=(
                "Operator signature present and bundle hash matches."
                if operator_signature_present
                else "Operator signature missing or bundle hash mismatch."
            ),
            source=None,
        )
    )

    # 9. Portal field completeness.
    for fld in portal_fields:
        value = fld.value
        if not value or not value.strip():
            items.append(
                ChecklistItem(
                    check_id="portal_field_completeness",
                    status="fail",
                    detail=(
                        f"Portal field {fld.field_id!r} ({fld.field_label!r}) "
                        "has empty value."
                    ),
                    source=fld.field_id,
                )
            )

    # 10. Content integrity (reported by caller after content-mutation diff).
    for section_name, detail in content_mutation_failures:
        items.append(
            ChecklistItem(
                check_id="content_integrity",
                status="fail",
                detail=detail,
                source=section_name,
            )
        )

    fail_count = sum(1 for i in items if i.status == "fail")
    warn_count = sum(1 for i in items if i.status == "warn")
    pass_count = sum(1 for i in items if i.status == "pass")
    overall = "ready" if fail_count == 0 else "not_ready"

    return ReadinessChecklist(
        overall_status=overall,
        items=tuple(items),
        fail_count=fail_count,
        warn_count=warn_count,
        pass_count=pass_count,
        checked_at_utc=_utc_now(),
    )


# ---------------------------------------------------------------------------
# Uploader state persistence (Rule 1)
# ---------------------------------------------------------------------------


def write_uploader_state(
    *,
    state: UploaderState,
    state_dir: Path,
) -> Path:
    """Persist UploaderState to ``<state_dir>/<run_id>.yaml``. Return path.

    Per §12.5 state directory: separate from submission_package — Tilth-
    internal artifact that must not leak into the operator's portal
    upload.
    """
    state_dir.mkdir(parents=True, exist_ok=True)
    out_path = state_dir / f"{state.run_id}.yaml"
    assembly_attempted_at_utc = state.assembly_attempted_at_utc
    payload = {
        "run_id": state.run_id,
        "grant_id": state.grant_id,
        "org_slug": state.org_slug,
        "adapter_id": state.adapter_id,
        "assembly_attempted_at_utc": assembly_attempted_at_utc.isoformat(),
        "assembly_succeeded": state.assembly_succeeded,
        "sections_assembled": list(state.sections_assembled),
        "sections_failed": list(state.sections_failed),
        "attachments_staged": state.attachments_staged,
        "readiness_status": state.readiness_status,
        "failure_reason": state.failure_reason,
    }
    out_path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")
    return out_path


# ---------------------------------------------------------------------------
# Top-level orchestration: run_uploader
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class UploaderRunResult:
    """Wraps either a successful UploaderOutput OR a PRE-gate failure state.

    On success: ``output`` is populated, ``state.assembly_succeeded`` is True.
    On PRE-gate failure: ``output`` is None, ``state.assembly_succeeded``
    is False with ``failure_reason`` set to the failing gate code.
    """

    state: UploaderState
    output: UploaderOutput | None
    pre_gate_failure: GateResult | None = None


def _vault_root_for(uploader_input: UploaderInput, vault_root: Path) -> Path:
    """Resolve the org-grant root path for an UploaderInput under vault_root."""
    return vault_root / "orgs" / uploader_input.org_slug / "vault" / "grants" / uploader_input.grant_id


def _read_submission_bundle_bytes(
    uploader_input: UploaderInput,
    vault_root: Path,
) -> bytes:
    """Read SubmissionBundle bytes via the spec'd 'submission-bundle-read' intent.

    At v0.1 the read is direct file I/O (Vault read-intent dispatch is
    a v0.2 horizon item; the §2-owned read intent is a contract surface
    that the test seam injects via a stubbed callable when the vault
    primitive lands). The path is normalized via Path.resolve() and
    enforced to sit under the declared org-grant subtree — symlink
    escape trips F-UPLOADER-ORG-CROSS-REF.
    """
    raw_path = vault_root / uploader_input.submission_bundle_ref
    bundle_path = raw_path.resolve()
    expected_raw = _vault_root_for(uploader_input, vault_root)
    expected_root = expected_raw.resolve()
    bundle_str = str(bundle_path)
    expected_str = str(expected_root)
    if not (bundle_str == expected_str or bundle_str.startswith(expected_str + os.sep)):
        raise ValueError(
            "F-UPLOADER-ORG-CROSS-REF.symlink_escape: submission_bundle_ref "
            f"resolves to {bundle_path!r}, outside org-grant subtree "
            f"{expected_root!r}."
        )
    return bundle_path.read_bytes()


def run_uploader(
    *,
    uploader_input: UploaderInput,
    vault_root: Path,
    submission_bundle_bytes: bytes | None = None,
    converter: DocxToPdfConverter | None = None,
) -> UploaderRunResult:
    """End-to-end Uploader run — PRE-gates, assembly, POST-gates, state.

    Pipeline:
      1. PRE: F-UPLOADER-ORG-CROSS-REF
      2. PRE: F-UPLOADER-SIGNATURE-MISSING / -MISMATCH
      3. Adapter dispatch + assembly.
      4. POST: F-UPLOADER-PACKAGE-INCOMPLETE / -FORMAT-MISMATCH
         (surfaced via readiness checklist).
      5. Manifest + readiness checklist persisted.
      6. UploaderState persisted on success AND failure (Rule 1).

    No subprocess, no auto-submit. F-UPLOADER-AUTOSUBMIT-ATTEMPTED is
    structurally enforced by UploaderOutput.__post_init__ (Layer 3).
    """
    org_grant_root = _vault_root_for(uploader_input, vault_root)
    state_dir = org_grant_root / "uploader_state"
    output_dir = org_grant_root / "submission_package" / uploader_input.run_id
    started = _utc_now()

    def _persist_pre_failure(code: str, detail: str) -> UploaderRunResult:
        state = UploaderState(
            run_id=uploader_input.run_id,
            grant_id=uploader_input.grant_id,
            org_slug=uploader_input.org_slug,
            adapter_id=uploader_input.target_portal,
            assembly_attempted_at_utc=started,
            assembly_succeeded=False,
            sections_assembled=(),
            sections_failed=(),
            attachments_staged=0,
            readiness_status="not_ready",
            failure_reason=f"{code}: {detail}",
        )
        write_uploader_state(state=state, state_dir=state_dir)
        return UploaderRunResult(
            state=state,
            output=None,
            pre_gate_failure=GateResult.FAIL(code=code, detail=detail),
        )

    # PRE-gate 1 — F-UPLOADER-ORG-CROSS-REF (path-level only at v1 per §12.2 Law 3).
    cross_ref = f_uploader_org_cross_ref(uploader_input)
    if not cross_ref.passed:
        return _persist_pre_failure(
            cross_ref.code or "F-UPLOADER-ORG-CROSS-REF",
            cross_ref.detail or "",
        )

    # PRE-gate 2 — F-UPLOADER-SIGNATURE-MISSING / -MISMATCH.
    if submission_bundle_bytes is None:
        try:
            submission_bundle_bytes = _read_submission_bundle_bytes(
                uploader_input, vault_root
            )
        except (FileNotFoundError, ValueError, OSError) as exc:
            return _persist_pre_failure(
                "F-UPLOADER-SIGNATURE-MISSING",
                f"submission-bundle-read failed: {exc!r}",
            )
    sig_result = f_uploader_signature_missing(uploader_input, submission_bundle_bytes)
    if not sig_result.passed:
        return _persist_pre_failure(
            sig_result.code or "F-UPLOADER-SIGNATURE-MISSING",
            sig_result.detail or "",
        )

    # Dispatch + assembly.
    adapter_cls = get_adapter(uploader_input.target_portal)
    if converter is None:
        converter_obj: DocxToPdfConverter = DocxToPdfConverter()
    else:
        converter_obj = converter
    adapter = adapter_cls(converter=converter_obj)  # type: ignore[call-arg]
    output_dir.mkdir(parents=True, exist_ok=True)

    sections_assembled: list[str] = []
    sections_failed: list[str] = []
    content_mutation_failures: list[tuple[str, str]] = []

    try:
        manifest = adapter.assemble_package(
            uploader_input.section_drafts,
            uploader_input.attachments,
            uploader_input.rfa_extracted_record,
            str(output_dir),
        )
    except (FileNotFoundError, OSError, ValueError, RuntimeError) as exc:
        # Assembly failure → state-only, no manifest, no output.
        state = UploaderState(
            run_id=uploader_input.run_id,
            grant_id=uploader_input.grant_id,
            org_slug=uploader_input.org_slug,
            adapter_id=uploader_input.target_portal,
            assembly_attempted_at_utc=started,
            assembly_succeeded=False,
            sections_assembled=tuple(sections_assembled),
            sections_failed=tuple(
                getattr(s, "section_name", "?")
                for s in uploader_input.section_drafts
            ),
            attachments_staged=0,
            readiness_status="not_ready",
            failure_reason=f"assembly_error: {exc!r}",
        )
        write_uploader_state(state=state, state_dir=state_dir)
        return UploaderRunResult(state=state, output=None)

    # Content-mutation check per section.
    for section in uploader_input.section_drafts:
        section_name = getattr(section, "section_name", "?")
        sections_assembled.append(section_name)
        body_text = getattr(section, "body_text", "")
        for entry in manifest.entries:
            if entry.portal_section != section_name:
                continue
            if entry.format == "docx":
                staged_path = output_dir / entry.file_name
                extracted = extract_docx_text(staged_path)
                if _normalize_text(body_text) not in _normalize_text(extracted):
                    content_mutation_failures.append(
                        (
                            section_name,
                            (
                                f"Content mutation in {entry.file_name!r}: "
                                "rendered DOCX text does not contain the "
                                "original SectionDraft.body_text."
                            ),
                        )
                    )
            elif entry.format == "pdf":
                staged_path = output_dir / entry.file_name
                extracted = extract_pdf_text(staged_path)
                if (
                    _normalize_text(body_text)
                    and _normalize_text(body_text) not in _normalize_text(extracted)
                ):
                    content_mutation_failures.append(
                        (
                            section_name,
                            (
                                f"Content mutation in {entry.file_name!r}: "
                                "extracted PDF text does not contain the "
                                "original SectionDraft.body_text."
                            ),
                        )
                    )

    # Portal-field export.
    project_context = getattr(uploader_input, "project_context", None)
    portal_fields = adapter.map_fields(
        uploader_input.rfa_extracted_record,
        uploader_input.section_drafts,
        project_context,
    )

    extra_entries: list[ManifestEntry] = list(manifest.entries)
    if portal_fields:
        portal_fields_path = output_dir / "portal_fields.yaml"
        write_portal_fields_yaml(fields=portal_fields, output_path=portal_fields_path)
        extra_entries.append(
            build_manifest_entry(
                file_path=portal_fields_path,
                portal_file_name="portal_fields.yaml",
                fmt="yaml",
                source="portal_field_export",
                source_ref=str(portal_fields_path),
            )
        )

    full_manifest = SubmissionManifest(
        entries=tuple(extra_entries),
        assembled_at_utc=manifest.assembled_at_utc,
        adapter_id=manifest.adapter_id,
        run_id=manifest.run_id,
    )

    # Readiness checklist.
    checklist = build_readiness_checklist(
        rfa=uploader_input.rfa_extracted_record,
        manifest=full_manifest,
        adapter=adapter,
        section_drafts=uploader_input.section_drafts,
        portal_fields=portal_fields,
        operator_signature_present=True,
        output_dir=output_dir,
        content_mutation_failures=tuple(content_mutation_failures),
    )

    # Persist manifest + checklist.
    write_submission_manifest_yaml(
        manifest=full_manifest,
        output_path=output_dir / "submission_manifest.yaml",
    )
    write_readiness_checklist_yaml(
        checklist=checklist,
        output_path=output_dir / "readiness_checklist.yaml",
    )

    # Build output (submitted is structurally False — Layer 3 invariant).
    output = UploaderOutput(
        run_id=uploader_input.run_id,
        manifest=full_manifest,
        readiness_checklist=checklist,
        output_dir=str(output_dir),
        submitted=False,
    )

    state = UploaderState(
        run_id=uploader_input.run_id,
        grant_id=uploader_input.grant_id,
        org_slug=uploader_input.org_slug,
        adapter_id=uploader_input.target_portal,
        assembly_attempted_at_utc=started,
        assembly_succeeded=True,
        sections_assembled=tuple(sections_assembled),
        sections_failed=tuple(sections_failed),
        attachments_staged=0,
        readiness_status=checklist.overall_status,
    )
    write_uploader_state(state=state, state_dir=state_dir)
    return UploaderRunResult(state=state, output=output)
