"""
Fluxx adapter (§12.10.6).

Foundation portal platform. Per-portal field mapping.
Requires PortalConfig.fluxx_portal_id.
"""

from __future__ import annotations
from dataclasses import dataclass


@dataclass
class FluxxAdapter:
    """Fluxx portal adapter. Scaffold — full implementation downstream."""

    @property
    def portal_id(self) -> str:
        return "fluxx"

    def required_format(self, portal_section: str | None) -> str | None:
        return "pdf"

    def page_limit(self, portal_section: str | None) -> int | None:
        return None

    def file_size_limit(self, portal_section: str | None) -> int | None:
        return None

    def filename_convention(self, portal_section: str | None, original_name: str) -> str:
        return original_name.replace(" ", "_")

    def map_fields(self, rfa: object, section_drafts: tuple, project_context: object) -> tuple:
        return ()

    def assemble_package(self, section_drafts: tuple, attachments: tuple, rfa: object, output_dir: str) -> object:
        raise NotImplementedError("FluxxAdapter.assemble_package: scaffold — implementation downstream")
