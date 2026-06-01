"""F-ROUTER-FAMILY-COLLISION invocation-time PRE-gate.

Blueprint §4 v2.5 §4.16 LOCKED 2026-04-19.
Canonical definition site for F-ROUTER-FAMILY-COLLISION (shared with §4.15 Canary).
Fires at model-dispatch time for council seats; checks that no two resolved
model families are the same after fallback resolution.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from typing import Any, Final

BLUEPRINT_DEPS: Final[dict] = {
    "section_04_v2_4_v2_5_amendment.md": {
        "sections_implemented": ["§4.16 family collision PRE-gate"],
        "hash_source_version": "v2.5",
    },
}

F_ROUTER_FAMILY_COLLISION: Final[str] = "F-ROUTER-FAMILY-COLLISION"


@dataclass(frozen=True)
class FamilyCollisionResult:
    """Result of the family-collision PRE-gate (§4.16)."""

    collision_detected: bool
    failure_code: str | None
    colliding_families: tuple[str, ...] | None
    detail: dict[str, Any] | None


def check_family_collision(
    resolved_families: list[str],
    require_all_distinct: bool = True,
) -> FamilyCollisionResult:
    """Invocation-time family-collision PRE-gate (§4.16). [§4.2.1 Row implicit]

    Parameters
    ----------
    resolved_families : list[str]
        Provider-family names after fallback resolution (e.g., ["anthropic",
        "openai", "meta", "alibaba", "moonshot"]).
    require_all_distinct : bool
        If True (default), every family must appear at most once.
        Set False to skip the distinct check (testing / non-council paths).

    Returns
    -------
    FamilyCollisionResult
        collision_detected=True + failure_code when families collide.
        Always returns; never raises.
    """
    if not require_all_distinct:
        return FamilyCollisionResult(
            collision_detected=False,
            failure_code=None,
            colliding_families=None,
            detail=None,
        )

    counts = Counter(resolved_families)
    colliding = [fam for fam, count in counts.items() if count > 1]

    if colliding:
        return FamilyCollisionResult(
            collision_detected=True,
            failure_code=F_ROUTER_FAMILY_COLLISION,
            colliding_families=tuple(sorted(colliding)),
            detail={
                "sub_tag": "runtime_invocation_time",
                "resolved_families": resolved_families,
                "family_counts": dict(counts),
            },
        )

    return FamilyCollisionResult(
        collision_detected=False,
        failure_code=None,
        colliding_families=None,
        detail=None,
    )
