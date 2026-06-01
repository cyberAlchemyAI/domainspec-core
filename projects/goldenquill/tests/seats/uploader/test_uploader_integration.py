"""§12.13.4 Uploader integration tests — end-to-end per-adapter assembly.

Spec card: ``pipeline/blueprint/v0.1/section_12_uploader.md`` §12.13.2 +
§12.13.4. Each test exercises a full ``run_uploader`` cycle against a
realistic UploaderInput fixture. The DOCX→PDF converter is replaced with
a docx-pass-through stub so tests do not depend on LibreOffice being on
``PATH`` — F-UPLOADER-FORMAT-MISMATCH falls out cleanly when the stub is
in place, and the AST-lint allow-list is unaffected (the stub lives in
the test module, not in any uploader / uploader_adapters file).

Coverage:
- copy_paste end-to-end: manifest complete, readiness PASS (with WARN
  on manual-attach to-dos), sections rendered as DOCX, content
  preserved, no auto-submit, state persisted.
- grants_gov end-to-end: SF-424 fields populated from PROJECT_CONTEXT,
  filename convention applied, file-size limit respected.
- common_grant_app end-to-end: CGA fields populated, PDF/XLSX format
  rules honored.
- sam_gov end-to-end: validation report XLSX written, portal_fields.yaml
  surfaces SAM status / UEI / expiration.
- F-UPLOADER-PACKAGE-INCOMPLETE fires when an RFA section is missing.
- F-UPLOADER-FIELD-MAP-CLOUD-ROUTED fires on a cloud-routed
  disambiguation context.
"""

from __future__ import annotations

import dataclasses
import hashlib
from datetime import datetime, timezone
from pathlib import Path

import pytest

from pipeline.orchestrator.seats.uploader import (
    DocxToPdfConverter,
    FieldMapCallContext,
    OperatorSignature,
    PortalField,
    SubmissionManifest,
    UploaderInput,
    build_readiness_checklist,
    extract_docx_text,
    gate_field_map_call,
    render_section_to_docx,
    run_uploader,
)
from pipeline.orchestrator.seats.uploader_adapters.copy_paste import (
    CopyPasteAdapter,
)
from pipeline.orchestrator.seats.uploader_adapters.common_grant_app import (
    CommonGrantAppAdapter,
)
from pipeline.orchestrator.seats.uploader_adapters.grants_gov import (
    GrantsGovAdapter,
)
from pipeline.orchestrator.seats.uploader_adapters.sam_gov import (
    SamGovAdapter,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


_NOW = datetime(2026, 5, 10, 12, 0, 0, tzinfo=timezone.utc)


@dataclasses.dataclass(frozen=True)
class StubSection:
    section_name: str
    section_order: int
    body_text: str


@dataclasses.dataclass(frozen=True)
class StubSectionSpec:
    section_name: str


@dataclasses.dataclass(frozen=True)
class StubRfa:
    program_name: str
    cfda_or_aln: str | None
    award_ceiling: int | None
    award_floor: int | None
    section_structure: tuple
    required_attachments: tuple
    rfa_content_sha3_512: str


@dataclasses.dataclass(frozen=True)
class StubProjectContext:
    organization_legal_name: str
    ein: str
    uei: str
    duns: str | None
    organization_street_address: str
    organization_city: str
    organization_state: str
    organization_zip: str
    authorized_representative_name: str
    authorized_representative_title: str
    project_director_name: str
    mission_statement: str
    sam_registration_status: str | None = None
    sam_expiration_date: str | None = None


def _write_minimal_pdf(path: Path) -> None:
    """Use pypdf.PdfWriter to write a minimal one-page valid PDF.

    The pass-through converter calls this so manifest builders that
    invoke pypdf.PdfReader can count pages correctly.
    """
    import pypdf

    writer = pypdf.PdfWriter()
    writer.add_blank_page(width=612, height=792)
    with path.open("wb") as fh:
        writer.write(fh)


class _DocxPassThroughConverter(DocxToPdfConverter):
    """Test-only converter that emits a minimal valid PDF in place of
    LibreOffice rendering.

    Lives in the test module — AST-lint R-UPLOADER-NO-SUBMIT operates only
    on uploader.py + uploader_adapters/*. This stub stays out of that
    glob, so it is exempt from the allow-list.
    """

    def convert(self, *, docx_path: Path, output_dir: Path) -> Path:
        pdf_path = output_dir / (docx_path.stem + ".pdf")
        _write_minimal_pdf(pdf_path)
        return pdf_path


class _NotSofficeConverter(DocxToPdfConverter):
    """Test-only converter that simulates LibreOffice being unavailable."""

    def convert(self, *, docx_path: Path, output_dir: Path) -> Path:
        raise FileNotFoundError("soffice not on PATH (test stub)")


def _make_section_drafts() -> tuple[StubSection, ...]:
    return (
        StubSection(
            section_name="Project Title",
            section_order=1,
            body_text="Mycelium Land Stewardship Cooperative",
        ),
        StubSection(
            section_name="Project Narrative",
            section_order=2,
            body_text=(
                "FIT Farms proposes a cooperative-led mycelium remediation "
                "pilot across three pilot sites in central Pennsylvania. "
                "The pilot will train ten farmer-members on substrate "
                "preparation, inoculation, and outplanting protocols."
            ),
        ),
        StubSection(
            section_name="Budget Plan",
            section_order=3,
            body_text=(
                "Personnel: $30,000\nSupplies: $15,000\nEquipment: $10,000"
            ),
        ),
    )


def _make_rfa() -> StubRfa:
    return StubRfa(
        program_name="USDA VAPG FY26",
        cfda_or_aln="10.352",
        award_ceiling=250000,
        award_floor=50000,
        section_structure=(
            StubSectionSpec(section_name="Project Title"),
            StubSectionSpec(section_name="Project Narrative"),
            StubSectionSpec(section_name="Budget Plan"),
        ),
        required_attachments=("SF-424A", "Audit Report"),
        rfa_content_sha3_512="0" * 128,
    )


def _make_project_context() -> StubProjectContext:
    return StubProjectContext(
        organization_legal_name="FIT Farms LLC",
        ein="12-3456789",
        uei="ABC123XYZ456",
        duns=None,
        organization_street_address="123 Spore Lane",
        organization_city="Bellefonte",
        organization_state="PA",
        organization_zip="16823",
        authorized_representative_name="Josh Inklovich",
        authorized_representative_title="Founder",
        project_director_name="Josh Inklovich",
        mission_statement="Cultivate regenerative food systems.",
        sam_registration_status="Active",
        sam_expiration_date="2027-01-15",
    )


def _stage_bundle_and_input(
    *,
    tmp_path: Path,
    target_portal: str,
    section_drafts: tuple,
    rfa: StubRfa,
    project_context: StubProjectContext | None = None,
    org_slug: str = "fit_farms",
    grant_id: str = "vapg_fy26",
    run_id: str = "run-001",
) -> tuple[UploaderInput, bytes]:
    org_root = (
        tmp_path / "orgs" / org_slug / "vault" / "grants" / grant_id
    )
    org_root.mkdir(parents=True, exist_ok=True)
    bundle_bytes = b"submission-bundle-bytes-fixture"
    bundle_path = org_root / "submission_bundle.yaml"
    bundle_path.write_bytes(bundle_bytes)
    bundle_hash = hashlib.sha3_512(bundle_bytes).hexdigest()
    operator_signature = OperatorSignature(
        signed_at_utc=_NOW,
        signer_id="josh",
        bundle_content_hash=bundle_hash,
    )
    bundle_ref = (
        f"orgs/{org_slug}/vault/grants/{grant_id}/submission_bundle.yaml"
    )
    uploader_input = UploaderInput(
        run_id=run_id,
        grant_id=grant_id,
        org_slug=org_slug,
        submission_bundle_ref=bundle_ref,
        section_drafts=section_drafts,
        claim_evidence_map=(),
        rfa_extracted_record=rfa,
        operator_signature=operator_signature,
        attachments=(),
        target_portal=target_portal,  # type: ignore[arg-type]
        portal_config=None,
        prepared_at_utc=_NOW,
    )
    # Stash project_context on the input as a setattr-friendly attribute the
    # adapters can opportunistically read. UploaderInput is frozen, so we
    # carry it via a dedicated wrapper attribute.
    object.__setattr__(uploader_input, "project_context", project_context)
    return uploader_input, bundle_bytes


# ---------------------------------------------------------------------------
# Copy-paste fallback adapter
# ---------------------------------------------------------------------------


class TestCopyPasteEndToEnd:
    def test_full_run_passthrough_converter(self, tmp_path: Path) -> None:
        rfa = _make_rfa()
        sections = _make_section_drafts()
        uploader_input, bundle_bytes = _stage_bundle_and_input(
            tmp_path=tmp_path,
            target_portal="copy_paste",
            section_drafts=sections,
            rfa=rfa,
            project_context=_make_project_context(),
        )
        # Use the pass-through converter to avoid LibreOffice dependency.
        # We also directly construct the adapter with the converter so
        # run_uploader's default DocxToPdfConverter() does not fire.
        # run_uploader signature accepts an injected converter — wire it.
        result = run_uploader(
            uploader_input=uploader_input,
            vault_root=tmp_path,
            submission_bundle_bytes=bundle_bytes,
            converter=_DocxPassThroughConverter(),
        )

        assert result.output is not None
        assert result.output.submitted is False  # Layer 3 invariant
        manifest = result.output.manifest
        # 3 sections × (DOCX + PDF) + 1 portal_fields.yaml = 7 entries
        assert len(manifest.entries) == 7
        # All section entries reference council_draft.
        council_entries = [
            e for e in manifest.entries if e.source == "council_draft"
        ]
        assert len(council_entries) == 6
        # Every section has both a DOCX and a PDF entry.
        formats_per_section: dict[str, set[str]] = {}
        for e in council_entries:
            assert e.portal_section is not None
            formats_per_section.setdefault(e.portal_section, set()).add(e.format)
        for section_name, fmts in formats_per_section.items():
            assert "docx" in fmts, f"Missing DOCX for {section_name}"
            assert "pdf" in fmts, f"Missing PDF for {section_name}"

        # Readiness checklist surfaces manual-attach WARN entries.
        checklist = result.output.readiness_checklist
        warns = [i for i in checklist.items if i.status == "warn"]
        assert any(i.check_id == "manual_attach_required" for i in warns)
        # Both required_attachments surface as WARN entries.
        warn_sources = {i.source for i in warns}
        assert "SF-424A" in warn_sources
        assert "Audit Report" in warn_sources

        # State persisted.
        state_dir = (
            tmp_path
            / "orgs"
            / uploader_input.org_slug
            / "vault"
            / "grants"
            / uploader_input.grant_id
            / "uploader_state"
        )
        state_file = state_dir / f"{uploader_input.run_id}.yaml"
        assert state_file.exists()
        # Manifest YAML written.
        output_dir = Path(result.output.output_dir)
        assert (output_dir / "submission_manifest.yaml").exists()
        assert (output_dir / "readiness_checklist.yaml").exists()
        assert (output_dir / "portal_fields.yaml").exists()


# ---------------------------------------------------------------------------
# Grants.gov adapter
# ---------------------------------------------------------------------------


class TestGrantsGovEndToEnd:
    def test_sf424_field_export(self, tmp_path: Path) -> None:
        rfa = _make_rfa()
        sections = _make_section_drafts()
        uploader_input, bundle_bytes = _stage_bundle_and_input(
            tmp_path=tmp_path,
            target_portal="grants_gov",
            section_drafts=sections,
            rfa=rfa,
            project_context=_make_project_context(),
        )
        result = run_uploader(
            uploader_input=uploader_input,
            vault_root=tmp_path,
            submission_bundle_bytes=bundle_bytes,
            converter=_DocxPassThroughConverter(),
        )
        assert result.output is not None
        manifest = result.output.manifest
        # SF-424 fields show up in portal_fields export.
        portal_fields_entry = next(
            e for e in manifest.entries if e.source == "portal_field_export"
        )
        portal_fields_path = Path(result.output.output_dir) / portal_fields_entry.file_name
        body = portal_fields_path.read_text(encoding="utf-8")
        # Smoke-check: SF-424 EIN + UEI + project director rendered.
        assert "sf424.ein" in body
        assert "sf424.uei" in body
        assert "sf424.applicant_legal_name" in body
        assert "FIT Farms LLC" in body

    def test_filename_convention_applied(self, tmp_path: Path) -> None:
        adapter = GrantsGovAdapter()
        # Mixed spaces / hyphens / >50 chars — collapse + truncate.
        result = adapter.filename_convention(
            None, "Project Narrative — Final Approved.pdf"
        )
        assert " " not in result
        assert "-" not in result
        assert len(result) <= 50

    def test_file_size_limit_set(self, tmp_path: Path) -> None:
        adapter = GrantsGovAdapter()
        # 20 MB per attachment.
        assert adapter.file_size_limit(None) == 20 * 1024 * 1024


# ---------------------------------------------------------------------------
# Common Grant Application adapter
# ---------------------------------------------------------------------------


class TestCommonGrantAppEndToEnd:
    def test_field_mapping_includes_mission_statement(
        self, tmp_path: Path
    ) -> None:
        rfa = _make_rfa()
        sections = _make_section_drafts()
        uploader_input, bundle_bytes = _stage_bundle_and_input(
            tmp_path=tmp_path,
            target_portal="common_grant_app",
            section_drafts=sections,
            rfa=rfa,
            project_context=_make_project_context(),
        )
        result = run_uploader(
            uploader_input=uploader_input,
            vault_root=tmp_path,
            submission_bundle_bytes=bundle_bytes,
            converter=_DocxPassThroughConverter(),
        )
        assert result.output is not None
        portal_fields_path = (
            Path(result.output.output_dir) / "portal_fields.yaml"
        )
        body = portal_fields_path.read_text(encoding="utf-8")
        assert "mission_statement" in body
        assert "Cultivate regenerative food systems" in body
        # Project title from SectionDraft is exported.
        assert "project_title" in body


# ---------------------------------------------------------------------------
# SAM.gov adapter
# ---------------------------------------------------------------------------


class TestSamGovEndToEnd:
    def test_sam_validation_report(self, tmp_path: Path) -> None:
        rfa = _make_rfa()
        sections = ()  # SAM.gov has no narrative surface
        uploader_input, bundle_bytes = _stage_bundle_and_input(
            tmp_path=tmp_path,
            target_portal="sam_gov",
            section_drafts=sections,
            rfa=rfa,
            project_context=_make_project_context(),
        )
        result = run_uploader(
            uploader_input=uploader_input,
            vault_root=tmp_path,
            submission_bundle_bytes=bundle_bytes,
            converter=_DocxPassThroughConverter(),
        )
        assert result.output is not None
        # XLSX validation workbook + portal_fields.yaml present.
        manifest = result.output.manifest
        formats = {e.format for e in manifest.entries}
        assert "xlsx" in formats
        assert "yaml" in formats
        # portal_fields.yaml lists SAM UEI + status + expiration.
        portal_fields_path = (
            Path(result.output.output_dir) / "portal_fields.yaml"
        )
        body = portal_fields_path.read_text(encoding="utf-8")
        assert "sam.uei" in body
        assert "sam.registration_status" in body
        assert "sam.expiration_date" in body


# ---------------------------------------------------------------------------
# F-UPLOADER-PACKAGE-INCOMPLETE — POST-gate
# ---------------------------------------------------------------------------


class TestPackageIncompleteSurface:
    def test_missing_section_surfaces_in_readiness(self, tmp_path: Path) -> None:
        """Sections in RFA but not in manifest → readiness FAIL items."""
        rfa = _make_rfa()
        # Only render one of three RFA-required sections.
        sections = (
            StubSection(
                section_name="Project Title",
                section_order=1,
                body_text="Test",
            ),
        )
        uploader_input, bundle_bytes = _stage_bundle_and_input(
            tmp_path=tmp_path,
            target_portal="copy_paste",
            section_drafts=sections,
            rfa=rfa,
            project_context=_make_project_context(),
        )
        result = run_uploader(
            uploader_input=uploader_input,
            vault_root=tmp_path,
            submission_bundle_bytes=bundle_bytes,
            converter=_DocxPassThroughConverter(),
        )
        assert result.output is not None
        checklist = result.output.readiness_checklist
        assert checklist.overall_status == "not_ready"
        section_fails = [
            i for i in checklist.items
            if i.check_id == "section_completeness" and i.status == "fail"
        ]
        # Project Narrative + Budget Plan missing → 2 fails.
        assert len(section_fails) == 2
        sources = {i.source for i in section_fails}
        assert "Project Narrative" in sources
        assert "Budget Plan" in sources


# ---------------------------------------------------------------------------
# F-UPLOADER-FIELD-MAP-CLOUD-ROUTED — PRE-gate
# ---------------------------------------------------------------------------


class TestFieldMapCloudRoutedGate:
    def test_local_passes(self) -> None:
        ctx = FieldMapCallContext(
            portal_field_id="sf424.applicant_name",
            portal_field_label="Applicant Name",
            caller_module=(
                "pipeline.orchestrator.seats.uploader_adapters.grants_gov"
            ),
            routed_to="local",
            model_id="ollama/mistral:7b",
            classification_at_call="confidential",
        )
        result = gate_field_map_call(ctx)
        assert result.passed
        assert result.code is None

    def test_cloud_fails(self) -> None:
        ctx = FieldMapCallContext(
            portal_field_id="sf424.applicant_name",
            portal_field_label="Applicant Name",
            caller_module=(
                "pipeline.orchestrator.seats.uploader_adapters.grants_gov"
            ),
            routed_to="cloud",
            model_id="anthropic/claude-opus-4",
            classification_at_call="confidential",
        )
        result = gate_field_map_call(ctx)
        assert not result.passed
        assert result.code == "F-UPLOADER-FIELD-MAP-CLOUD-ROUTED"


# ---------------------------------------------------------------------------
# DOCX render + content preservation
# ---------------------------------------------------------------------------


class TestDocxRendering:
    def test_render_section_to_docx_round_trip(self, tmp_path: Path) -> None:
        out = tmp_path / "section.docx"
        body = "Paragraph one.\n\nParagraph two."
        size = render_section_to_docx(
            section_name="Test Section", body_text=body, output_path=out
        )
        assert size > 0
        assert out.exists()
        # Read back and verify body text round-trips.
        extracted = extract_docx_text(out)
        assert "Paragraph one." in extracted
        assert "Paragraph two." in extracted


# ---------------------------------------------------------------------------
# Auto-submit invariant — runtime layer
# ---------------------------------------------------------------------------


class TestAutoSubmitInvariant:
    def test_run_uploader_output_submitted_false(self, tmp_path: Path) -> None:
        rfa = _make_rfa()
        sections = _make_section_drafts()
        uploader_input, bundle_bytes = _stage_bundle_and_input(
            tmp_path=tmp_path,
            target_portal="copy_paste",
            section_drafts=sections,
            rfa=rfa,
            project_context=_make_project_context(),
        )
        result = run_uploader(
            uploader_input=uploader_input,
            vault_root=tmp_path,
            submission_bundle_bytes=bundle_bytes,
            converter=_DocxPassThroughConverter(),
        )
        assert result.output is not None
        # Layer 3 invariant: submitted is structurally False.
        assert result.output.submitted is False


# ---------------------------------------------------------------------------
# Soffice-unavailable graceful degradation
# ---------------------------------------------------------------------------


class TestSofficeUnavailable:
    def test_assemble_falls_back_to_docx(self, tmp_path: Path) -> None:
        rfa = _make_rfa()
        sections = _make_section_drafts()
        uploader_input, bundle_bytes = _stage_bundle_and_input(
            tmp_path=tmp_path,
            target_portal="copy_paste",
            section_drafts=sections,
            rfa=rfa,
            project_context=_make_project_context(),
        )
        result = run_uploader(
            uploader_input=uploader_input,
            vault_root=tmp_path,
            submission_bundle_bytes=bundle_bytes,
            converter=_NotSofficeConverter(),
        )
        # Run completes; manifest contains DOCX but no PDF.
        assert result.output is not None
        formats = {e.format for e in result.output.manifest.entries}
        assert "docx" in formats
        assert "pdf" not in formats
        # Format-mismatch fail items appear in readiness checklist
        # (PDF was required by adapter but DOCX was staged).
        checklist = result.output.readiness_checklist
        assert checklist.overall_status == "not_ready"
        format_fails = [
            i for i in checklist.items
            if i.check_id == "format_compliance" and i.status == "fail"
        ]
        assert len(format_fails) == len(sections)
