"""
Grants.gov Workspace adapter (§12.10.1).

Federal mandatory portal. SF-424 family field mapping per Grants.gov
submission rules.

Required format: PDF for narrative, XLSX for budget forms (SF-424A/B/C).
Filename conventions: no spaces, max 50 chars, prefix with attachment
type code per the Grants.gov Workspace naming guide. Per-attachment file
size limit: 20 MB at v0.1 (limit is portal-configurable for future
updates).

At v0.1 attachments are NOT staged by Uploader (§12.6 deferral) — the
operator manually attaches SF-424A/B/C and other required forms after
reviewing the narrative + portal_fields export. The narrative + SF-424
field map are the canonical Tilth-emitted artifacts at v1.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from pipeline.orchestrator.seats.uploader import (
    DocxToPdfConverter,
    PortalField,
)
from pipeline.orchestrator.seats.uploader_adapters.copy_paste import (
    CopyPasteAdapter,
)


_GRANTS_GOV_MAX_FILENAME_CHARS = 50
_GRANTS_GOV_PER_ATTACHMENT_SIZE_BYTES = 20 * 1024 * 1024


@dataclass
class GrantsGovAdapter(CopyPasteAdapter):
    """Grants.gov Workspace federal portal adapter."""

    converter: DocxToPdfConverter = field(default_factory=DocxToPdfConverter)
    portal_id_value: str = "grants_gov"

    def required_format(self, portal_section: str | None) -> str | None:
        if portal_section is not None:
            lowered = portal_section.lower()
            if "budget" in lowered:
                return "xlsx"
        return "pdf"

    def page_limit(self, portal_section: str | None) -> int | None:
        # Page limits are RFA-driven, not portal-driven for Grants.gov.
        return None

    def file_size_limit(self, portal_section: str | None) -> int | None:
        return _GRANTS_GOV_PER_ATTACHMENT_SIZE_BYTES

    def filename_convention(
        self, portal_section: str | None, original_name: str
    ) -> str:
        """No spaces; underscores only; max 50 chars."""
        # Replace whitespace and dashes with underscores; strip everything else.
        cleaned = original_name.replace(" ", "_").replace("-", "_")
        # Drop characters that violate the convention.
        allowed = []
        for ch in cleaned:
            if ch.isalnum() or ch in {"_", "."}:
                allowed.append(ch)
            else:
                allowed.append("_")
        cleaned = "".join(allowed)
        # Truncate to 50 chars, preserving extension.
        if "." in cleaned:
            stem, dot, ext = cleaned.rpartition(".")
            max_stem = _GRANTS_GOV_MAX_FILENAME_CHARS - 1 - len(ext)
            if max_stem < 1:
                max_stem = 1
            stem = stem[:max_stem]
            cleaned = f"{stem}{dot}{ext}"
        else:
            cleaned = cleaned[:_GRANTS_GOV_MAX_FILENAME_CHARS]
        if len(cleaned) > _GRANTS_GOV_MAX_FILENAME_CHARS:
            cleaned = cleaned[:_GRANTS_GOV_MAX_FILENAME_CHARS]
        return cleaned

    def map_fields(
        self,
        rfa: object,
        section_drafts: tuple,
        project_context: object,
    ) -> tuple[PortalField, ...]:
        """SF-424 family field mapping. Federal-portal canonical fields.

        Sources: PROJECT_CONTEXT (organization legal name, EIN, UEI,
        DUNS, address, authorized representative, project director) +
        RFA (program name, CFDA/ALN, award ceiling/floor, budget /
        project periods) + SectionDraft (project title, abstract).

        Disambiguation pass (§12.11) is NOT invoked at v0.1 first ship —
        SF-424 fields are deterministically derivable from the inputs.
        Sub-adapters that need disambiguation MUST gate via
        F-UPLOADER-FIELD-MAP-CLOUD-ROUTED before the local-LLM call.
        """
        fields: list[PortalField] = list(
            super().map_fields(rfa, section_drafts, project_context)
        )

        # SF-424 organizational identifiers from PROJECT_CONTEXT.
        if project_context is not None:
            for attr_name, field_id, label, instructions in (
                (
                    "organization_legal_name",
                    "sf424.applicant_legal_name",
                    "Applicant — Legal Name",
                    "SF-424 Box 8.a (Applicant Legal Name).",
                ),
                (
                    "ein",
                    "sf424.ein",
                    "Employer Identification Number (EIN)",
                    "SF-424 Box 5.a (Federal Tax Identification Number).",
                ),
                (
                    "uei",
                    "sf424.uei",
                    "Unique Entity Identifier (UEI)",
                    "SF-424 Box 8.c (UEI).",
                ),
                (
                    "duns",
                    "sf424.duns",
                    "DUNS Number (legacy)",
                    "SF-424 Box 8.b — retired federal-wide; included for "
                    "non-Grants.gov portals that still request it.",
                ),
                (
                    "organization_street_address",
                    "sf424.applicant_street",
                    "Applicant — Street Address",
                    "SF-424 Box 8.d.",
                ),
                (
                    "organization_city",
                    "sf424.applicant_city",
                    "Applicant — City",
                    "SF-424 Box 8.e.",
                ),
                (
                    "organization_state",
                    "sf424.applicant_state",
                    "Applicant — State",
                    "SF-424 Box 8.f.",
                ),
                (
                    "organization_zip",
                    "sf424.applicant_zip",
                    "Applicant — ZIP / Postal Code",
                    "SF-424 Box 8.h.",
                ),
                (
                    "authorized_representative_name",
                    "sf424.authorized_rep_name",
                    "Authorized Representative — Name",
                    "SF-424 Box 21 (Authorized Representative).",
                ),
                (
                    "authorized_representative_title",
                    "sf424.authorized_rep_title",
                    "Authorized Representative — Title",
                    "SF-424 Box 21 (Title).",
                ),
                (
                    "project_director_name",
                    "sf424.project_director_name",
                    "Project Director — Name",
                    "SF-424 Box 14 (Project Director / PI).",
                ),
            ):
                value = getattr(project_context, attr_name, None)
                if value:
                    fields.append(
                        PortalField(
                            field_id=field_id,
                            field_label=label,
                            value=str(value),
                            source=f"PROJECT_CONTEXT:{attr_name}",
                            instructions=instructions,
                        )
                    )

        # SF-424 budget + project period fields from RFA.
        if rfa is not None:
            for attr_name, field_id, label, instructions in (
                (
                    "award_ceiling",
                    "sf424.award_ceiling",
                    "Award Ceiling",
                    "SF-424 Box 18.a — use as the upper bound when "
                    "entering the requested federal share.",
                ),
                (
                    "award_floor",
                    "sf424.award_floor",
                    "Award Floor",
                    "SF-424 Box 18.a — use as the lower bound.",
                ),
            ):
                value = getattr(rfa, attr_name, None)
                if value is not None:
                    fields.append(
                        PortalField(
                            field_id=field_id,
                            field_label=label,
                            value=str(value),
                            source=f"RFA:{attr_name}",
                            instructions=instructions,
                        )
                    )

        # Project title from a SectionDraft if present.
        for section in section_drafts:
            section_name = getattr(section, "section_name", "")
            if section_name.lower() in {"project title", "title"}:
                body_text = getattr(section, "body_text", "")
                stripped = body_text.strip()
                if stripped:
                    first_line = stripped.splitlines()[0]
                    fields.append(
                        PortalField(
                            field_id="sf424.project_title",
                            field_label="Project Title",
                            value=first_line,
                            source=f"SectionDraft:{section_name}",
                            instructions="SF-424 Box 15 (Descriptive Title of Applicant's Project).",
                        )
                    )
                break

        return tuple(fields)
