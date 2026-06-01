"""F-WPFA-PDF-CONFIDENTIAL-LEAK — PRE-PDF-emit gate. [§5.1.WPFA.13]

Trigger: buyer-facing PDF emission attempts to render any field value
whose classification register entry is ``confidential``.

PRE-gate scans rendered PDF content (the field-value strings about to be
embedded in the template) against the operator-signed classification
register; fail-closes if Confidential content detected.

Sub-tags: ``.confidential_field_in_pdf``,
``.classification_register_unread_at_emit``.

M13: NOT bypassable for buyer-attested artifacts (structural Law 3 + v7.0.7
gate).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Iterable, Mapping, Optional


F_WPFA_PDF_CONFIDENTIAL_LEAK: Final[str] = "F-WPFA-PDF-CONFIDENTIAL-LEAK"


@dataclass(frozen=True, kw_only=True)
class PdfConfidentialLeakResult:
    success: bool
    failure_code: Optional[str]
    detail: str
    sub_tag: Optional[str] = None
    offending_field_paths: tuple[str, ...] = ()


def check_f_wpfa_pdf_confidential_leak(
    *,
    rendered_field_paths: Iterable[str],
    classification_register: Optional[Mapping[str, str]],
) -> PdfConfidentialLeakResult:
    """PRE-PDF-emit: every rendered field MUST be `shareable` or `public`.

    ``classification_register`` maps field_path (e.g.,
    ``orgs/foo/financials/annual_revenue``) → classification class
    (``confidential`` | ``shareable`` | ``public``). If the register is
    ``None`` the gate fails closed (classification_register_unread_at_emit
    — the emit code path MUST load the register first).
    """
    if classification_register is None:
        return PdfConfidentialLeakResult(
            success=False,
            failure_code=F_WPFA_PDF_CONFIDENTIAL_LEAK,
            sub_tag="classification_register_unread_at_emit",
            detail=(
                "classification_register is None — PDF emit MUST load the "
                "operator-signed register before scanning rendered fields"
            ),
        )
    if not isinstance(classification_register, Mapping):
        return PdfConfidentialLeakResult(
            success=False,
            failure_code=F_WPFA_PDF_CONFIDENTIAL_LEAK,
            sub_tag="classification_register_unread_at_emit",
            detail="classification_register must be a Mapping",
        )
    offending: list[str] = []
    for field_path in rendered_field_paths:
        if not isinstance(field_path, str) or not field_path:
            continue
        cls = classification_register.get(field_path)
        if cls is None:
            # Unset = treat as confidential at v0.1 (fail-closed default
            # mirrors §11.7 INCREMENTAL_INGEST new-fact default).
            offending.append(field_path)
            continue
        if cls == "confidential" or cls == "operator_flagged":
            offending.append(field_path)
    if offending:
        return PdfConfidentialLeakResult(
            success=False,
            failure_code=F_WPFA_PDF_CONFIDENTIAL_LEAK,
            sub_tag="confidential_field_in_pdf",
            detail=(
                f"PDF would render {len(offending)} confidential/unset "
                f"field(s): {sorted(offending)[:5]!r}"
                + ("…" if len(offending) > 5 else "")
            ),
            offending_field_paths=tuple(sorted(offending)),
        )
    return PdfConfidentialLeakResult(
        success=True,
        failure_code=None,
        detail=(
            f"all {len(list(rendered_field_paths)) if not hasattr(rendered_field_paths, '__len__') else len(rendered_field_paths)} "
            "rendered fields are shareable/public"
        ),
    )


__all__ = [
    "F_WPFA_PDF_CONFIDENTIAL_LEAK",
    "PdfConfidentialLeakResult",
    "check_f_wpfa_pdf_confidential_leak",
]
