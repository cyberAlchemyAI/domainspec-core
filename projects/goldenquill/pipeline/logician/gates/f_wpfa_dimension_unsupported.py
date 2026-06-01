"""F-WPFA-DIMENSION-UNSUPPORTED — PRE-emission gate. [§5.1.WPFA.9]

Trigger: receipt asserts a dimension not in ``dimensions_active``, OR
``dimensions_active`` at v0.1 contains anything other than
``("dollars", "energy")``.

Defends against premature v0.2 dimension surfacing in v0.1 deployments.

Sub-tags: ``.water_at_v0_1``, ``.co2_at_v0_1``, ``.unknown_dimension``.
M13 audited.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Optional


F_WPFA_DIMENSION_UNSUPPORTED: Final[str] = "F-WPFA-DIMENSION-UNSUPPORTED"

_ALLOWED_AT_V0_1: Final[frozenset[str]] = frozenset({"dollars", "energy"})
_ALLOWED_AT_V0_2_PLUS: Final[frozenset[str]] = frozenset(
    {"dollars", "energy", "water", "co2"}
)


@dataclass(frozen=True, kw_only=True)
class DimensionUnsupportedResult:
    success: bool
    failure_code: Optional[str]
    detail: str
    sub_tag: Optional[str] = None
    offending: tuple[str, ...] = ()


def check_f_wpfa_dimension_unsupported(
    *,
    dimensions_active: tuple[str, ...],
    deployment_schema_version: str,  # e.g., "1.0.0" for v0.1 ship
) -> DimensionUnsupportedResult:
    """PRE-emission: dimensions_active must be the closed v0.1 set."""
    if not isinstance(dimensions_active, tuple):
        return DimensionUnsupportedResult(
            success=False,
            failure_code=F_WPFA_DIMENSION_UNSUPPORTED,
            sub_tag="unknown_dimension",
            detail="dimensions_active must be a tuple of str",
        )
    # Major-version parse
    try:
        major = int(deployment_schema_version.split(".")[0])
    except (ValueError, IndexError):
        return DimensionUnsupportedResult(
            success=False,
            failure_code=F_WPFA_DIMENSION_UNSUPPORTED,
            sub_tag="unknown_dimension",
            detail=(
                f"deployment_schema_version {deployment_schema_version!r} "
                "does not parse as semver"
            ),
        )
    # v0.1 = schema major version 1; v0.2 = major 1 still but feature flag
    # downstream; treat the function param as the source of truth for the
    # allowed set.
    allowed = _ALLOWED_AT_V0_1 if major <= 1 else _ALLOWED_AT_V0_2_PLUS
    # At v0.1 the active set MUST equal the v0.1 closed set
    if allowed == _ALLOWED_AT_V0_1:
        if set(dimensions_active) != _ALLOWED_AT_V0_1:
            extras = sorted(set(dimensions_active) - _ALLOWED_AT_V0_1)
            missing = sorted(_ALLOWED_AT_V0_1 - set(dimensions_active))
            if "water" in extras:
                sub_tag = "water_at_v0_1"
            elif "co2" in extras:
                sub_tag = "co2_at_v0_1"
            elif extras:
                sub_tag = "unknown_dimension"
            else:
                sub_tag = "unknown_dimension"
            return DimensionUnsupportedResult(
                success=False,
                failure_code=F_WPFA_DIMENSION_UNSUPPORTED,
                sub_tag=sub_tag,
                detail=(
                    f"dimensions_active {dimensions_active!r} != v0.1 closed "
                    f"set {sorted(_ALLOWED_AT_V0_1)} (extras: {extras}, "
                    f"missing: {missing})"
                ),
                offending=tuple(extras or missing),
            )
    else:
        unknown = sorted(set(dimensions_active) - allowed)
        if unknown:
            return DimensionUnsupportedResult(
                success=False,
                failure_code=F_WPFA_DIMENSION_UNSUPPORTED,
                sub_tag="unknown_dimension",
                detail=(
                    f"dimensions_active contains unknown dimension(s): "
                    f"{unknown}"
                ),
                offending=tuple(unknown),
            )
    return DimensionUnsupportedResult(
        success=True,
        failure_code=None,
        detail=(
            f"dimensions_active {dimensions_active!r} valid for "
            f"deployment schema {deployment_schema_version!r}"
        ),
    )


__all__ = [
    "F_WPFA_DIMENSION_UNSUPPORTED",
    "DimensionUnsupportedResult",
    "check_f_wpfa_dimension_unsupported",
]
