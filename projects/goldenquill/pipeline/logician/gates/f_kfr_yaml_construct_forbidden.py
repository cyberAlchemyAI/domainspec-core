"""F-KFR-YAML-CONSTRUCT-FORBIDDEN — KFR PRE-load gate (M1 §2.4).

Fires fail-closed when a KFR file load encounters anchor / alias /
merge-key / custom tag / forbidden-numeric construct.  Wraps
:func:`pipeline.logician.canonicalization.kfr_safe_loader.load_kfr_safe_bytes`.

Bypass: M13 (audited operator override; HIGH severity admin-risk entry).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Final, Optional

from pipeline.logician.canonicalization.kfr_safe_loader import (
    KfrConstructError,
    load_kfr_safe_bytes,
)


F_KFR_YAML_CONSTRUCT_FORBIDDEN: Final[str] = "F-KFR-YAML-CONSTRUCT-FORBIDDEN"


@dataclass(frozen=True, kw_only=True)
class YamlConstructForbiddenResult:
    success: bool
    failure_code: Optional[str]
    detail: str
    offending_construct: Optional[str] = None
    parsed: Any = None


def check_kfr_yaml_construct_forbidden(
    *,
    raw_bytes: bytes,
) -> YamlConstructForbiddenResult:
    """PRE-load gate: refuse anchor / alias / merge-key / custom-tag KFR files."""
    try:
        parsed = load_kfr_safe_bytes(raw_bytes)
    except KfrConstructError as exc:
        return YamlConstructForbiddenResult(
            success=False,
            failure_code=F_KFR_YAML_CONSTRUCT_FORBIDDEN,
            detail=str(exc),
            offending_construct=getattr(exc, "offending_construct", None),
        )
    return YamlConstructForbiddenResult(
        success=True,
        failure_code=None,
        detail=(
            "KFR YAML loaded under SafeLoader discipline (no anchor / "
            "alias / merge-key / custom-tag construct present)"
        ),
        parsed=parsed,
    )


__all__ = [
    "F_KFR_YAML_CONSTRUCT_FORBIDDEN",
    "YamlConstructForbiddenResult",
    "check_kfr_yaml_construct_forbidden",
]
