"""
Copy-paste fallback adapter (§12.10.4).

Universal fallback for portals without a dedicated adapter. Produces a
clean, organized package the operator can manually upload to any portal.
Every other adapter extends this base behavior.

v0.1 first ship: stages each SectionDraft as a DOCX (canonical from
Scribe per §7.5) plus a PDF rendering via LibreOffice headless. Filename
convention: ``<section_order>_<section_name>.<ext>`` — simple, readable.
Portal-field export covers RFA + PROJECT_CONTEXT-derivable fields with
generic labels. No portal-specific field IDs.

Per ADR-001 substrate: python-docx for DOCX writes, pypdf for PDF
validation, ``subprocess.run(["soffice", ...], check=True)`` for the
PDF conversion. AST-lint R-UPLOADER-NO-SUBMIT enforces the allow-list.
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from pipeline.orchestrator.seats.uploader import (
    DocxToPdfConverter,
    ManifestEntry,
    PortalField,
    SubmissionManifest,
    _safe_filename,
    build_manifest_entry,
    render_section_to_docx,
)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class CopyPasteAdapter:
    """Copy-paste fallback adapter — base implementation for v0.1.

    Subclasses (Common Grant App, Grants.gov) override ``required_format``,
    ``filename_convention`` and ``map_fields`` to add portal-specific
    optimizations on top of this base.
    """

    converter: DocxToPdfConverter = field(default_factory=DocxToPdfConverter)
    portal_id_value: str = "copy_paste"
    stage_pdf: bool = True
    stage_docx_source: bool = True

    @property
    def portal_id(self) -> str:
        return self.portal_id_value

    def required_format(self, portal_section: str | None) -> str | None:
        # PDF for universal portability per §12.10.4.
        return "pdf"

    def page_limit(self, portal_section: str | None) -> int | None:
        return None

    def file_size_limit(self, portal_section: str | None) -> int | None:
        return None

    def filename_convention(
        self, portal_section: str | None, original_name: str
    ) -> str:
        return _safe_filename(original_name)

    def map_fields(
        self,
        rfa: object,
        section_drafts: tuple,
        project_context: object,
    ) -> tuple[PortalField, ...]:
        """Generic field export — RFA + PROJECT_CONTEXT-derivable values.

        v0.1: deterministic field-extraction pass (zero LLM calls in the
        fallback). Sub-adapters that need disambiguation hit the
        F-UPLOADER-FIELD-MAP-CLOUD-ROUTED gate before invoking the
        always-local Mistral 7B endpoint.
        """
        fields: list[PortalField] = []
        if rfa is not None:
            program_name = getattr(rfa, "program_name", "")
            if program_name:
                fields.append(
                    PortalField(
                        field_id="program_name",
                        field_label="Program Name",
                        value=str(program_name),
                        source="RFA:program_name",
                        instructions=(
                            "Paste into the portal's funding-program / "
                            "opportunity field."
                        ),
                    )
                )
            cfda = getattr(rfa, "cfda_or_aln", None)
            if cfda:
                fields.append(
                    PortalField(
                        field_id="cfda_or_aln",
                        field_label="CFDA / Assistance Listing Number",
                        value=str(cfda),
                        source="RFA:cfda_or_aln",
                        instructions=(
                            "Paste into the portal's CFDA / ALN field."
                        ),
                    )
                )
        if project_context is not None:
            org_name = getattr(project_context, "organization_legal_name", None)
            if org_name:
                fields.append(
                    PortalField(
                        field_id="organization_legal_name",
                        field_label="Organization Legal Name",
                        value=str(org_name),
                        source="PROJECT_CONTEXT:organization.legal_name",
                        instructions=(
                            "Paste into the portal's applicant-name field."
                        ),
                    )
                )
        return tuple(fields)

    def assemble_package(
        self,
        section_drafts: tuple,
        attachments: tuple,
        rfa: object,
        output_dir: str,
    ) -> SubmissionManifest:
        """Assemble narrative package: DOCX (canonical) + PDF per section.

        Attachments are accepted in the signature for v1.1 forward-compat
        but ignored at v0.1 first ship per §12.6 deferral.
        """
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)
        entries: list[ManifestEntry] = []

        sorted_sections = sorted(
            section_drafts,
            key=lambda s: getattr(s, "section_order", 0),
        )

        for section in sorted_sections:
            section_name = getattr(section, "section_name", "section")
            section_order = getattr(section, "section_order", 0)
            body_text = getattr(section, "body_text", "")
            base_name = _safe_filename(f"{section_order:02d}_{section_name}")

            docx_path = out_path / f"{base_name}.docx"
            render_section_to_docx(
                section_name=section_name,
                body_text=body_text,
                output_path=docx_path,
            )
            docx_portal_name = self.filename_convention(
                section_name, f"{base_name}.docx"
            )
            if self.stage_docx_source:
                entries.append(
                    build_manifest_entry(
                        file_path=docx_path,
                        portal_file_name=docx_portal_name,
                        fmt="docx",
                        source="council_draft",
                        source_ref=f"SectionDraft:{section_name}",
                        portal_section=section_name,
                    )
                )

            if self.stage_pdf and self.required_format(section_name) == "pdf":
                pdf_portal_name = self.filename_convention(
                    section_name, f"{base_name}.pdf"
                )
                try:
                    pdf_path = self.converter.convert(
                        docx_path=docx_path, output_dir=out_path
                    )
                    entries.append(
                        build_manifest_entry(
                            file_path=pdf_path,
                            portal_file_name=pdf_portal_name,
                            fmt="pdf",
                            source="council_draft",
                            source_ref=f"SectionDraft:{section_name}",
                            portal_section=section_name,
                        )
                    )
                except (FileNotFoundError, subprocess.CalledProcessError):
                    # LibreOffice unavailable or conversion failed → DOCX
                    # remains as the staged artifact and
                    # F-UPLOADER-FORMAT-MISMATCH surfaces in readiness.
                    if not self.stage_docx_source:
                        # Ensure DOCX is staged so the operator has at
                        # least the canonical artifact.
                        entries.append(
                            build_manifest_entry(
                                file_path=docx_path,
                                portal_file_name=docx_portal_name,
                                fmt="docx",
                                source="council_draft",
                                source_ref=f"SectionDraft:{section_name}",
                                portal_section=section_name,
                            )
                        )

        run_id = ""
        for section in sorted_sections:
            run_id = getattr(section, "run_id", "") or run_id
        manifest = SubmissionManifest(
            entries=tuple(entries),
            assembled_at_utc=_utc_now(),
            adapter_id=self.portal_id,
            run_id=run_id,
        )
        return manifest
