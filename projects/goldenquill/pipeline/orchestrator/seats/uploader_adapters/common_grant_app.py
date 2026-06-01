"""
Common Grant Application adapter (§12.10.3).

Foundation standard format. Covers a large share of US foundation
portals. PDF for narrative, XLSX or PDF for budget. Filename convention:
``OrgName_SectionName.pdf``.

Inherits CopyPasteAdapter assembly behavior (DOCX + PDF rendering,
deterministic readiness checklist) and overrides ``map_fields`` to
emit the standard Common Grant Application field set.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from pipeline.orchestrator.seats.uploader import (
    DocxToPdfConverter,
    PortalField,
    _safe_filename,
)
from pipeline.orchestrator.seats.uploader_adapters.copy_paste import (
    CopyPasteAdapter,
)


@dataclass
class CommonGrantAppAdapter(CopyPasteAdapter):
    """Common Grant Application adapter — foundation standard format."""

    converter: DocxToPdfConverter = field(default_factory=DocxToPdfConverter)
    portal_id_value: str = "common_grant_app"

    def required_format(self, portal_section: str | None) -> str | None:
        # CGA: PDF for narrative, XLSX for budget.
        if portal_section is not None:
            lowered = portal_section.lower()
            if "budget" in lowered:
                return "xlsx"
        return "pdf"

    def filename_convention(
        self, portal_section: str | None, original_name: str
    ) -> str:
        """``OrgName_SectionName.pdf`` per §12.10.3 — minus the OrgName
        prefix at this layer (the run-time render injects org name once
        ``project_context`` reaches the adapter — see ``map_fields``).
        """
        return _safe_filename(original_name)

    def map_fields(
        self,
        rfa: object,
        section_drafts: tuple,
        project_context: object,
    ) -> tuple[PortalField, ...]:
        """Standard CGA field set — organization, project, budget,
        evaluation. Sources: PROJECT_CONTEXT + RFA + SectionDraft.
        """
        base = list(
            super().map_fields(rfa, section_drafts, project_context)
        )

        # Mission statement.
        if project_context is not None:
            mission = getattr(project_context, "mission_statement", None)
            if mission:
                base.append(
                    PortalField(
                        field_id="mission_statement",
                        field_label="Mission Statement",
                        value=str(mission),
                        source="PROJECT_CONTEXT:mission_statement",
                        instructions=(
                            "Paste into the CGA 'Organizational Mission' "
                            "section."
                        ),
                    )
                )

        # Project title — first SectionDraft section_name conventionally
        # carries the project title at v0.1; sub-adapters can override
        # via the SectionDraft section_name == "Project Title" pattern.
        for section in section_drafts:
            section_name = getattr(section, "section_name", "")
            if section_name.lower() in {"project title", "title"}:
                body_text = getattr(section, "body_text", "")
                if body_text:
                    base.append(
                        PortalField(
                            field_id="project_title",
                            field_label="Project Title",
                            value=body_text.strip().splitlines()[0]
                            if body_text.strip()
                            else "",
                            source=f"SectionDraft:{section_name}",
                            instructions="Paste into the CGA 'Project Title' field.",
                        )
                    )
                break

        # Requested amount + match.
        if rfa is not None:
            ceiling = getattr(rfa, "award_ceiling", None)
            if ceiling is not None:
                base.append(
                    PortalField(
                        field_id="award_ceiling",
                        field_label="Award Ceiling",
                        value=str(ceiling),
                        source="RFA:award_ceiling",
                        instructions=(
                            "Use as the upper bound when entering the "
                            "'Amount Requested' field."
                        ),
                    )
                )

        return tuple(base)
