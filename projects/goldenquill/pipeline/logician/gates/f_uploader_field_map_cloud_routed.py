"""F-UPLOADER-FIELD-MAP-CLOUD-ROUTED gate (PRE).

Backs §0.5 v9 row 229 (`uploader.pre_gate.field_map_routing.v1`).
Spec: pipeline/blueprint/v0.1/section_12_uploader.md §12.9.6.
Registered: pipeline/blueprint/v0.1/section_04_v2_x_uploader_gates_amendment.md §6 F-UPLOADER-FIELD-MAP-CLOUD-ROUTED.

Sequence position: PRE — fires at every portal-field-disambiguation LLM call
site (Pydantic AI ``before_model_request`` hook). Hard-block / fail-closed.
M13-bypass eligible (HIGH-severity admin-risk row at bypass time).

This file lands as a §12 v1 LOCK-companion edit per Audit-#1 RT-5c closure
(predicate file existed only as placeholder before the round; authored to
EXISTS-tier per L-006).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Protocol, runtime_checkable

from pipeline.orchestrator.seats.uploader import GateResult


# ---------------------------------------------------------------------------
# Input shape (Spec §12.9.6 — covered by §0.5 row 229 per consolidation
# pattern; no separate `field_map_call_context` schema row).
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class FieldMapCallContext:
    """Context object passed to F-UPLOADER-FIELD-MAP-CLOUD-ROUTED at every
    portal-field-disambiguation LLM call site."""

    portal_field_id: str
    portal_field_label: str
    caller_module: str
    routed_to: Literal["local", "cloud"]
    model_id: str
    classification_at_call: Literal["public", "shareable", "confidential"]


# ---------------------------------------------------------------------------
# Predicate (Protocol-DI per existing §4 v2.7 pattern).
# ---------------------------------------------------------------------------


@runtime_checkable
class _FieldMapCallContextLike(Protocol):
    routed_to: str


def check_uploader_field_map_cloud_routed(
    field_map_call: _FieldMapCallContextLike,
) -> GateResult:
    """Hard-block any portal-field-disambiguation LLM call routed to cloud.

    Per §12.11 routing posture: Uploader operates on post-fill drafts with
    Confidential values embedded (v7.0.7 split-context discipline). Every
    field-map LLM call must hit the always-local Mistral 7B-class endpoint;
    cloud routing is architecturally prohibited.

    Production binds the seat-side `FieldMapCallContext` shape; tests inject
    mock contexts via the Protocol-DI surface above.
    """

    if getattr(field_map_call, "routed_to", None) != "local":
        return GateResult.FAIL(
            code="F-UPLOADER-FIELD-MAP-CLOUD-ROUTED",
            detail=(
                "Portal-field disambiguation call routed to "
                f"{getattr(field_map_call, 'routed_to', '<unknown>')!r}; "
                "Uploader requires local routing per §12.11."
            ),
        )
    return GateResult.PASS()
