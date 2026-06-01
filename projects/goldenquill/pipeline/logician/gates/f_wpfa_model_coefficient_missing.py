"""F-WPFA-MODEL-COEFFICIENT-MISSING — PRE-emission gate. [§5.1.WPFA.4]

Trigger: span tree references a ``model_id`` that has no entry in the
loaded Coefficient Registry. Common cause is operator added a new
local model SKU without updating the registry.

Sub-tags: ``.unknown_model_id``, ``.deprecated_model_referenced``.
M13 audited.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Iterable, Optional


F_WPFA_MODEL_COEFFICIENT_MISSING: Final[str] = "F-WPFA-MODEL-COEFFICIENT-MISSING"


@dataclass(frozen=True, kw_only=True)
class ModelCoefficientMissingResult:
    success: bool
    failure_code: Optional[str]
    detail: str
    missing_model_ids: tuple[str, ...] = ()
    sub_tag: Optional[str] = None


def check_f_wpfa_model_coefficient_missing(
    *,
    span_model_ids: Iterable[str],
    registry_model_ids: Iterable[str],
    deprecated_model_ids: Iterable[str] = (),
) -> ModelCoefficientMissingResult:
    """PRE-emission: every span model_id resolves to a registry entry.

    Deprecated models in the registry are still resolvable — they fail-close
    with the ``.deprecated_model_referenced`` sub-tag so the operator can
    re-route or escalate.
    """
    if not isinstance(span_model_ids, (list, tuple, set, frozenset)):
        span_model_ids = list(span_model_ids)
    if not isinstance(registry_model_ids, (list, tuple, set, frozenset)):
        registry_model_ids = list(registry_model_ids)
    reg_set = set(registry_model_ids)
    dep_set = set(deprecated_model_ids)
    missing: list[str] = []
    deprecated: list[str] = []
    for mid in span_model_ids:
        if not isinstance(mid, str) or not mid:
            return ModelCoefficientMissingResult(
                success=False,
                failure_code=F_WPFA_MODEL_COEFFICIENT_MISSING,
                detail=(
                    f"span model_id entry is not a non-empty string: {mid!r}"
                ),
                sub_tag="unknown_model_id",
            )
        if mid not in reg_set:
            missing.append(mid)
        elif mid in dep_set:
            deprecated.append(mid)
    if missing:
        return ModelCoefficientMissingResult(
            success=False,
            failure_code=F_WPFA_MODEL_COEFFICIENT_MISSING,
            sub_tag="unknown_model_id",
            detail=(
                f"span tree references model_ids absent from registry: "
                f"{sorted(missing)!r}"
            ),
            missing_model_ids=tuple(sorted(missing)),
        )
    if deprecated:
        return ModelCoefficientMissingResult(
            success=False,
            failure_code=F_WPFA_MODEL_COEFFICIENT_MISSING,
            sub_tag="deprecated_model_referenced",
            detail=(
                f"span tree references deprecated model_ids: "
                f"{sorted(deprecated)!r}"
            ),
            missing_model_ids=tuple(sorted(deprecated)),
        )
    return ModelCoefficientMissingResult(
        success=True,
        failure_code=None,
        detail="all span model_ids resolve to non-deprecated registry entries",
    )


__all__ = [
    "F_WPFA_MODEL_COEFFICIENT_MISSING",
    "ModelCoefficientMissingResult",
    "check_f_wpfa_model_coefficient_missing",
]
