"""
Submittable adapter (§12.10.5).

Foundation/arts/civic portal platform. Distinguishes between
file-upload and inline-text form fields.
Requires PortalConfig.submittable_form_id.
"""

from __future__ import annotations
from dataclasses import dataclass


@dataclass
class SubmittableAdapter:
    """Submittable portal adapter. Scaffold — full implementation downstream."""

    @property
    def portal_id(self) -> str:
        return "submittable"

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
        raise NotImplementedError("SubmittableAdapter.assemble_package: scaffold — implementation downstream")
