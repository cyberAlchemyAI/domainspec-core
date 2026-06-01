"""F-WPFA-BASELINE-MISSING — PRE-emission gate. [§5.1.WPFA.5]

Trigger: counterfactual baseline not set for the cycle's quarter.
Either registry ``baseline_model_id`` is empty / falsy, OR it does not
resolve to an entry in the registry's ``entries`` tuple.

M13 audited.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Iterable, Optional


F_WPFA_BASELINE_MISSING: Final[str] = "F-WPFA-BASELINE-MISSING"


@dataclass(frozen=True, kw_only=True)
class BaselineMissingResult:
    success: bool
    failure_code: Optional[str]
    detail: str


def check_f_wpfa_baseline_missing(
    *,
    baseline_model_id: Optional[str],
    registry_model_ids: Iterable[str],
) -> BaselineMissingResult:
    """PRE-emission: baseline_model_id must be non-empty and resolve."""
    if not isinstance(baseline_model_id, str) or not baseline_model_id:
        return BaselineMissingResult(
            success=False,
            failure_code=F_WPFA_BASELINE_MISSING,
            detail=(
                "registry baseline_model_id is empty or falsy — counterfactual "
                "cannot be computed"
            ),
        )
    if not isinstance(registry_model_ids, (list, tuple, set, frozenset)):
        registry_model_ids = list(registry_model_ids)
    if baseline_model_id not in set(registry_model_ids):
        return BaselineMissingResult(
            success=False,
            failure_code=F_WPFA_BASELINE_MISSING,
            detail=(
                f"baseline_model_id {baseline_model_id!r} not present in "
                "registry entries — counterfactual coefficient unresolvable"
            ),
        )
    return BaselineMissingResult(
        success=True,
        failure_code=None,
        detail=f"baseline_model_id {baseline_model_id!r} resolves",
    )


__all__ = [
    "F_WPFA_BASELINE_MISSING",
    "BaselineMissingResult",
    "check_f_wpfa_baseline_missing",
]
