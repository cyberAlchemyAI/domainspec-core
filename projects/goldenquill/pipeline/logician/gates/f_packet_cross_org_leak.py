"""F-PACKET-CROSS-ORG-LEAK — PRE-emission + PRE-load gate. [§4 v2.x.y.1 row 2, LIVE]

Two-axis defense mirroring ``check_f_wpfa_cross_org_leak`` byte-for-byte:
  (a) target_write_path slug matches packet.org_slug
  (b) every span_id's recorded org_slug matches packet.org_slug
      (sub-tag ``.span_org_slug_mismatch`` per Cycle 1 RT-09 fold-in)

M13: NOT bypassable (Law 3 structural gate).

Blueprint authority:
    - section_04_v2_x_y_1_packet_bodies_amendment.md §4.v2.x.y.1.1.2
    - section_16_reflection_packet.md §16.7 (sibling-not-nested verification)
    - section_16_reflection_packet.md §16.10.1 RT-09 fold-in
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Final, Iterable, Optional


F_PACKET_CROSS_ORG_LEAK: Final[str] = "F-PACKET-CROSS-ORG-LEAK"

_ORG_SUBTREE_RE: Final[re.Pattern[str]] = re.compile(
    r"(?:^|/)orgs/(?P<slug>[^/]+)/vault/operational/reflection_packets/"
)


@dataclass(frozen=True, kw_only=True)
class CrossOrgLeakResult:
    success: bool
    failure_code: Optional[str]
    detail: str
    sub_tag: Optional[str] = None
    path_slug: Optional[str] = None
    packet_slug: Optional[str] = None


def check_f_packet_cross_org_leak(
    *,
    target_write_path: str,
    packet_org_slug: str,
    span_provenance_org_slugs: Iterable[str] = (),
) -> CrossOrgLeakResult:
    """PRE-write: path slug AND every span_org_slug match packet.org_slug.

    Mirrors ``check_f_wpfa_cross_org_leak`` (§17) byte-for-byte at axis (a).
    Axis (b) per RT-09 fold-in extends with span-attribute cross-check.
    """
    if not isinstance(target_write_path, str) or not target_write_path:
        return CrossOrgLeakResult(
            success=False,
            failure_code=F_PACKET_CROSS_ORG_LEAK,
            detail="target_write_path empty",
        )
    if not isinstance(packet_org_slug, str) or not packet_org_slug:
        return CrossOrgLeakResult(
            success=False,
            failure_code=F_PACKET_CROSS_ORG_LEAK,
            detail="packet_org_slug empty",
        )
    # Axis (a) — path slug match
    normalised = PurePosixPath(target_write_path.replace("\\", "/")).as_posix()
    match = _ORG_SUBTREE_RE.search(normalised)
    if match is None:
        return CrossOrgLeakResult(
            success=False,
            failure_code=F_PACKET_CROSS_ORG_LEAK,
            sub_tag="path_outside_org",
            detail=(
                f"target_write_path {target_write_path!r} does not match "
                "orgs/<slug>/vault/operational/reflection_packets/ subtree"
            ),
            packet_slug=packet_org_slug,
        )
    path_slug = match.group("slug")
    if path_slug != packet_org_slug:
        return CrossOrgLeakResult(
            success=False,
            failure_code=F_PACKET_CROSS_ORG_LEAK,
            sub_tag="path_outside_org",
            detail=(
                f"path slug {path_slug!r} != packet.org_slug "
                f"{packet_org_slug!r} — Law 3 cross-org leak guard fires"
            ),
            path_slug=path_slug,
            packet_slug=packet_org_slug,
        )
    # Axis (b) — span_org_slug match per RT-09
    for sslug in span_provenance_org_slugs:
        if not isinstance(sslug, str) or not sslug:
            continue
        if sslug != packet_org_slug:
            return CrossOrgLeakResult(
                success=False,
                failure_code=F_PACKET_CROSS_ORG_LEAK,
                sub_tag="span_org_slug_mismatch",
                detail=(
                    f"span_provenance contains span with org_slug "
                    f"{sslug!r} != packet.org_slug {packet_org_slug!r}"
                ),
                path_slug=path_slug,
                packet_slug=packet_org_slug,
            )
    return CrossOrgLeakResult(
        success=True,
        failure_code=None,
        detail=(
            f"path slug + span_provenance org slugs match packet.org_slug "
            f"{packet_org_slug!r}"
        ),
        path_slug=path_slug,
        packet_slug=packet_org_slug,
    )


predicate_cross_org_leak = check_f_packet_cross_org_leak


__all__ = [
    "F_PACKET_CROSS_ORG_LEAK",
    "CrossOrgLeakResult",
    "check_f_packet_cross_org_leak",
    "predicate_cross_org_leak",
]
