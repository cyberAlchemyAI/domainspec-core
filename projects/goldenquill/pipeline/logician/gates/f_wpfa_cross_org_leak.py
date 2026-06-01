"""F-WPFA-CROSS-ORG-LEAK — PRE-write gate. [§5.1.WPFA.12]

Trigger: any CycleReceipt write whose path resolves to
``orgs/<other_slug>/vault/operational/cycle_receipts/...`` where
``<other_slug>`` differs from the receipt's ``org_slug`` field.

Defense-in-depth on top of ``operational_org_isolation.cedar`` Rule 1.

M13: NOT bypassable (Law 3 structural gate).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Final, Optional


F_WPFA_CROSS_ORG_LEAK: Final[str] = "F-WPFA-CROSS-ORG-LEAK"

_ORG_SUBTREE_RE: Final[re.Pattern[str]] = re.compile(
    r"(?:^|/)orgs/(?P<slug>[^/]+)/vault/operational/cycle_receipts/"
)


@dataclass(frozen=True, kw_only=True)
class CrossOrgLeakResult:
    success: bool
    failure_code: Optional[str]
    detail: str
    path_slug: Optional[str] = None
    receipt_slug: Optional[str] = None


def check_f_wpfa_cross_org_leak(
    *,
    target_write_path: str,
    receipt_org_slug: str,
) -> CrossOrgLeakResult:
    """PRE-write: the path slug MUST equal the receipt's org_slug field.

    Path is normalised via PurePosixPath and matched against the
    canonical orgs/<slug>/vault/operational/cycle_receipts/ subtree.
    Paths outside that subtree fail-close (defense-in-depth: writes go
    only through the §2 v7.2 vault write intent).
    """
    if not isinstance(target_write_path, str) or not target_write_path:
        return CrossOrgLeakResult(
            success=False,
            failure_code=F_WPFA_CROSS_ORG_LEAK,
            detail="target_write_path empty",
        )
    if not isinstance(receipt_org_slug, str) or not receipt_org_slug:
        return CrossOrgLeakResult(
            success=False,
            failure_code=F_WPFA_CROSS_ORG_LEAK,
            detail="receipt_org_slug empty",
        )
    # Normalise to POSIX
    normalised = PurePosixPath(target_write_path.replace("\\", "/")).as_posix()
    match = _ORG_SUBTREE_RE.search(normalised)
    if match is None:
        return CrossOrgLeakResult(
            success=False,
            failure_code=F_WPFA_CROSS_ORG_LEAK,
            detail=(
                f"target_write_path {target_write_path!r} does not match the "
                "canonical orgs/<slug>/vault/operational/cycle_receipts/ "
                "subtree"
            ),
            receipt_slug=receipt_org_slug,
        )
    path_slug = match.group("slug")
    if path_slug != receipt_org_slug:
        return CrossOrgLeakResult(
            success=False,
            failure_code=F_WPFA_CROSS_ORG_LEAK,
            detail=(
                f"path slug {path_slug!r} != receipt.org_slug "
                f"{receipt_org_slug!r} — Law 3 cross-org leak guard fires"
            ),
            path_slug=path_slug,
            receipt_slug=receipt_org_slug,
        )
    return CrossOrgLeakResult(
        success=True,
        failure_code=None,
        detail=f"path slug matches receipt.org_slug {receipt_org_slug!r}",
        path_slug=path_slug,
        receipt_slug=receipt_org_slug,
    )


__all__ = [
    "F_WPFA_CROSS_ORG_LEAK",
    "CrossOrgLeakResult",
    "check_f_wpfa_cross_org_leak",
]
