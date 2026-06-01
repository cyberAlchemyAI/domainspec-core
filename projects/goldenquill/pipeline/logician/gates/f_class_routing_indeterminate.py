"""F-CLASS-ROUTING-INDETERMINATE — PRE per-call routing-decision gate.

Per architecture v7.0.7 §1 (single architectural pattern) + §5
(fail-closed defaults).

Per-call routing must resolve to one of two posture states:

  * cloud-frontier route: ALL inputs are classified ``public`` OR
    ``shareable``,
  * local-only route: ANY input is classified ``confidential`` or
    ``operator_flagged``.

If any input's classification is unset / unknown / ``pending_operator_review``,
the routing decision is INDETERMINATE. Per §5 the default is ROUTE
LOCAL — but the gate also fires F-CLASS-ROUTING-INDETERMINATE so the
operator review queue learns about the affected inputs.

This gate ALWAYS produces a fail-closed signal when indeterminate. The
caller is responsible for honoring the safe-default-local routing
behavior; this gate only flags the indeterminate condition.

Bypass: M13 (audited; admin-risk MEDIUM — operator must classify the
inputs before the call can route to cloud).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Final, Optional, Sequence


F_CLASS_ROUTING_INDETERMINATE: Final[str] = "F-CLASS-ROUTING-INDETERMINATE"

CLASS_PUBLIC: Final[str] = "public"
CLASS_SHAREABLE: Final[str] = "shareable"
CLASS_CONFIDENTIAL: Final[str] = "confidential"
CLASS_OPERATOR_FLAGGED: Final[str] = "operator_flagged"

PERMITTED_CLASSES: Final[frozenset[str]] = frozenset({
    CLASS_PUBLIC,
    CLASS_SHAREABLE,
    CLASS_CONFIDENTIAL,
    CLASS_OPERATOR_FLAGGED,
})


@dataclass(frozen=True, kw_only=True)
class CallInput:
    """One classification-tagged input to a per-agent-call routing decision.

    `class_name` may be any of PERMITTED_CLASSES, OR a sentinel value
    indicating an unset / pending-review state. The gate treats anything
    outside PERMITTED_CLASSES as INDETERMINATE.
    """

    field_path: str
    class_name: str
    locked_by: str = ""


@dataclass(frozen=True, kw_only=True)
class RoutingIndeterminateResult:
    """Result of F-CLASS-ROUTING-INDETERMINATE check."""

    success: bool
    failure_code: Optional[str]
    detail: str
    indeterminate_paths: tuple[str, ...] = field(default_factory=tuple)
    safe_default_route: str = "local"


def check_class_routing_indeterminate(
    *,
    inputs: Sequence[CallInput],
) -> RoutingIndeterminateResult:
    """PRE per-call: every input must have a recognized classification.

    Identifies inputs whose ``class_name`` is unset, blank, or outside
    PERMITTED_CLASSES, OR whose ``locked_by`` is
    ``pending_operator_review`` (indicating the routing layer should
    not yet make a determination on this input).

    Returns
    -------
    RoutingIndeterminateResult. PASS only when every input has a
    recognized class AND no input carries the
    ``pending_operator_review`` lock flag. On failure, the
    ``safe_default_route`` field documents the fail-closed-local
    posture per §5.
    """
    if not inputs:
        return RoutingIndeterminateResult(
            success=False,
            failure_code=F_CLASS_ROUTING_INDETERMINATE,
            detail=(
                "no inputs supplied to routing decision — fail-closed; the "
                "router cannot determine posture from empty input"
            ),
            safe_default_route="local",
        )

    indeterminate: list[str] = []
    for entry in inputs:
        class_name = entry.class_name
        if not isinstance(class_name, str):
            indeterminate.append(
                f"{entry.field_path or '<unknown>'}:non-string-class"
            )
            continue
        if not class_name.strip() or class_name not in PERMITTED_CLASSES:
            indeterminate.append(
                f"{entry.field_path or '<unknown>'}:class={class_name!r}"
            )
            continue
        if entry.locked_by == "pending_operator_review":
            indeterminate.append(
                f"{entry.field_path or '<unknown>'}:locked_by="
                "pending_operator_review"
            )

    if indeterminate:
        return RoutingIndeterminateResult(
            success=False,
            failure_code=F_CLASS_ROUTING_INDETERMINATE,
            detail=(
                "routing decision indeterminate — input(s) lack a recognized "
                f"classification: {', '.join(indeterminate[:5])}"
                + (
                    f" (+{len(indeterminate) - 5} more)"
                    if len(indeterminate) > 5
                    else ""
                )
                + " — fail-closed default ROUTE LOCAL applies; operator must "
                "classify before cloud route is permitted"
            ),
            indeterminate_paths=tuple(indeterminate[:5]),
            safe_default_route="local",
        )

    return RoutingIndeterminateResult(
        success=True,
        failure_code=None,
        detail=(
            f"all {len(inputs)} inputs carry a recognized classification; "
            "router can resolve posture deterministically"
        ),
        safe_default_route="cloud_or_local_per_class",
    )


__all__ = [
    "CLASS_CONFIDENTIAL",
    "CLASS_OPERATOR_FLAGGED",
    "CLASS_PUBLIC",
    "CLASS_SHAREABLE",
    "CallInput",
    "F_CLASS_ROUTING_INDETERMINATE",
    "PERMITTED_CLASSES",
    "RoutingIndeterminateResult",
    "check_class_routing_indeterminate",
]
