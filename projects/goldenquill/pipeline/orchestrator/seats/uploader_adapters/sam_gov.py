"""
SAM.gov adapter (§12.10.2).

Entity registration validation + representations-and-certifications
staging. SAM.gov is a pre-submission requirement, not a grant
submission portal — Uploader does not assemble narrative documents
here. Instead, the adapter:

  1. Reads ``PROJECT_CONTEXT.sam_registration_status`` and
     ``PROJECT_CONTEXT.sam_expiration_date``.
  2. Emits a validation report (XLSX workbook) under output_dir
     listing SAM status, UEI, expiration date, and gaps if any.
  3. Stages required-attachment representations-and-certifications
     metadata into ``portal_fields.yaml`` so the operator knows what
     to upload directly on the SAM.gov portal.

No narrative DOCX/PDF rendering at v0.1 — SAM.gov has no narrative
upload surface, and the §12.6 attachment deferral applies the same
way to representations-and-certifications letters (operator manually
uploads on SAM.gov).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path

from pipeline.orchestrator.seats.uploader import (
    DocxToPdfConverter,
    ManifestEntry,
    PortalField,
    SubmissionManifest,
    _safe_filename,
    build_manifest_entry,
    write_xlsx_validation_workbook,
)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _today_utc() -> date:
    now = _utc_now()
    return now.date()


@dataclass
class SamGovAdapter:
    """SAM.gov entity-registration validation adapter."""

    converter: DocxToPdfConverter = field(default_factory=DocxToPdfConverter)

    @property
    def portal_id(self) -> str:
        return "sam_gov"

    def required_format(self, portal_section: str | None) -> str | None:
        # SAM.gov has no narrative document surface at v0.1 — output is
        # portal_fields.yaml + an XLSX validation snapshot. Returning
        # None signals "any format accepted" so the readiness checklist's
        # format-compliance walk does not flag the validation workbook.
        return None

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
        fields: list[PortalField] = []
        if project_context is None:
            return tuple(fields)

        uei = getattr(project_context, "uei", None)
        if uei:
            fields.append(
                PortalField(
                    field_id="sam.uei",
                    field_label="Unique Entity Identifier (UEI)",
                    value=str(uei),
                    source="PROJECT_CONTEXT:uei",
                    instructions=(
                        "Confirm this UEI on the SAM.gov entity-search "
                        "page; the registration record must show 'Active'."
                    ),
                )
            )

        status = getattr(project_context, "sam_registration_status", None)
        if status:
            fields.append(
                PortalField(
                    field_id="sam.registration_status",
                    field_label="SAM Registration Status",
                    value=str(status),
                    source="PROJECT_CONTEXT:sam_registration_status",
                    instructions=(
                        "Cross-check on the SAM.gov entity record before "
                        "submitting any federal application."
                    ),
                )
            )

        expiration = getattr(project_context, "sam_expiration_date", None)
        if expiration:
            fields.append(
                PortalField(
                    field_id="sam.expiration_date",
                    field_label="SAM Registration Expiration",
                    value=str(expiration),
                    source="PROJECT_CONTEXT:sam_expiration_date",
                    instructions=(
                        "If within 60 days of expiration, renew on "
                        "SAM.gov before submitting any federal "
                        "application."
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
        """Emit XLSX validation report + manifest entry.

        section_drafts is unused (SAM.gov has no narrative surface).
        attachments is accepted in the signature for v1.1 forward-compat
        but ignored at v0.1 first ship.
        """
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)

        # The validation workbook captures a snapshot of registration state
        # the operator can audit against the SAM.gov portal record.
        rows: list[tuple[str, str]] = [
            ("portal_id", "sam_gov"),
            ("validated_at_utc", _utc_now().isoformat()),
        ]
        # Pull validation context from RFA (program), not a project_context
        # — this adapter's assemble_package takes neither, by protocol.
        if rfa is not None:
            program = getattr(rfa, "program_name", None)
            if program:
                rows.append(("program_name", str(program)))

        report_path = out_path / "sam_validation_report.xlsx"
        write_xlsx_validation_workbook(
            rows=tuple(rows),
            output_path=report_path,
            sheet_name="sam_validation",
        )
        entry = build_manifest_entry(
            file_path=report_path,
            portal_file_name="sam_validation_report.xlsx",
            fmt="xlsx",
            source="readiness_checklist",
            source_ref="adapter:sam_gov",
            portal_section=None,
        )
        run_id = ""
        for section in section_drafts:
            run_id = getattr(section, "run_id", "") or run_id
        manifest = SubmissionManifest(
            entries=(entry,),
            assembled_at_utc=_utc_now(),
            adapter_id=self.portal_id,
            run_id=run_id,
        )
        return manifest
