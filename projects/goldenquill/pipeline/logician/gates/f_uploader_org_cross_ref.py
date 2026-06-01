"""F-UPLOADER-ORG-CROSS-REF — PRE-gate.

Per Blueprint §12.9.5 + §4 v2.7 amendment. Law 3 enforcement. The input
bundle must reference paths under exactly one ``orgs/<slug>/`` subtree.
Multi-org reference (in any of: declared ``org_slug``, attachment paths,
``submission_bundle_ref``) blocks Uploader assembly.

This is the **Logician-side surface** for the predicate. Per the §4 v2.2
``_protocols.py`` pattern (E-017 injected-callable), the cross-ref check
is a Protocol-typed dependency injected into ``check_uploader_org_cross_
ref``. Production binds to the seat-side ``f_uploader_org_cross_ref``
adapter via the ``_uploader_defaults`` registry; tests inject mocks.

This module imports only ``_uploader_protocols`` and ``_uploader_defaults``
— **zero direct imports from ``pipeline.orchestrator.seats.uploader``**.

Bypass: M13.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from pipeline.logician.gates._uploader_defaults import (
    get_default_org_cross_ref_check,
)
from pipeline.logician.gates._uploader_protocols import OrgCrossRefCheck


F_UPLOADER_ORG_CROSS_REF: str = "F-UPLOADER-ORG-CROSS-REF"


@dataclass(frozen=True, kw_only=True)
class OrgCrossRefResult:
    """Result of F-UPLOADER-ORG-CROSS-REF check."""

    success: bool
    failure_code: Optional[str]
    detail: str


def check_uploader_org_cross_ref(
    *,
    uploader_input: object,
    check: Optional[OrgCrossRefCheck] = None,
) -> OrgCrossRefResult:
    """PRE-gate (PRE-36): input references exactly one orgs/<slug>/ subtree.

    Parameters
    ----------
    uploader_input
        The Uploader input bundle (duck-typed).
    check
        Injected ``OrgCrossRefCheck`` callable. When ``None``, the
        seat-side ``f_uploader_org_cross_ref`` predicate (which sweeps
        ``org_slug`` + every ``AttachmentRef.file_path`` + the
        ``submission_bundle_ref``) is bound via the ``_uploader_defaults``
        registry.
    """
    cross_ref_check = check or get_default_org_cross_ref_check()
    if cross_ref_check(uploader_input):
        return OrgCrossRefResult(
            success=True,
            failure_code=None,
            detail="single org slug in input (org_slug + attachments + bundle_ref)",
        )
    return OrgCrossRefResult(
        success=False,
        failure_code=F_UPLOADER_ORG_CROSS_REF,
        detail=(
            "multiple org slugs detected across org_slug, attachment paths, "
            "or submission_bundle_ref — Law-3 violation"
        ),
    )
