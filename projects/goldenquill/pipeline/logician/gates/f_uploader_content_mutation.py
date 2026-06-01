"""F-UPLOADER-CONTENT-MUTATION — POST-gate.

Per Blueprint §12.9.5 + §4 v2.7 amendment. Uploader is a renderer, not an
editor. Format conversion (e.g. docx-to-pdf) must preserve text content
byte-for-byte at the prose layer.

The gate compares the input ``SectionDraft.body_text`` against the text
extracted from the rendered output document (per-section). Whitespace is
collapsed and format-artifact lines (page numbers, headers/footers) are
filtered by the caller's text extractor before being passed in. Any
remaining non-whitespace delta is a content mutation → hard-block.

Per §12.8 caveat: table-cell content and image alt-text are excluded from
the prose-layer diff and validated via structural hash by the caller. This
gate operates on `body_text` only.

Fail-closed. Bypass: M13.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional


F_UPLOADER_CONTENT_MUTATION: str = "F-UPLOADER-CONTENT-MUTATION"


_WHITESPACE_RUN = re.compile(r"\s+")


def _normalize(text: str) -> str:
    """Collapse all runs of whitespace into single spaces; strip ends."""
    return _WHITESPACE_RUN.sub(" ", text).strip()


@dataclass(frozen=True, kw_only=True)
class ContentMutationResult:
    """Result of F-UPLOADER-CONTENT-MUTATION check for one section."""

    success: bool
    failure_code: Optional[str]
    section_name: str
    input_length: int
    output_length: int
    detail: str


def check_uploader_content_mutation(
    *,
    section_name: str,
    input_body_text: str,
    output_extracted_text: str,
) -> ContentMutationResult:
    """POST-gate: text-layer diff between input draft and rendered output."""
    norm_in = _normalize(input_body_text)
    norm_out = _normalize(output_extracted_text)
    if norm_in != norm_out:
        # Compute a small slice for the detail message (truncated to keep
        # session_log entries bounded)
        return ContentMutationResult(
            success=False,
            failure_code=F_UPLOADER_CONTENT_MUTATION,
            section_name=section_name,
            input_length=len(norm_in),
            output_length=len(norm_out),
            detail=(
                f"section {section_name!r}: text-layer mutation detected "
                f"(in={len(norm_in)} chars, out={len(norm_out)} chars)"
            ),
        )
    return ContentMutationResult(
        success=True,
        failure_code=None,
        section_name=section_name,
        input_length=len(norm_in),
        output_length=len(norm_out),
        detail=f"section {section_name!r}: text content preserved",
    )
