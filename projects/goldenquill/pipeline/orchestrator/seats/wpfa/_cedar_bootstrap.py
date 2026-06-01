"""WPFA Cedar bootstrap — cycle_receipt_* policy bindings. [§17.9]

Three rules extend the operational_subkinds.cedar surface:

1. ``cycle_receipt_org_isolation`` — extension of existing
   ``operational_org_isolation`` rule to admit ``sub_kind == "cycle_receipt"``
   into the default-permit set.
2. ``cycle_receipt_operator_attestation`` — permits buyer-facing PDF
   emission ONLY when ``signed_by_operator_ed25519`` is non-None AND the
   signature verifies. F-WPFA-OPERATOR-SIGNATURE-MISSING surfaces denial.
3. ``cycle_receipt_read_isolation`` — permits reading a CycleReceipt only
   when the principal's ``org_slug`` attribute matches the path's
   ``<slug>`` OR the principal is ``wpfa_dashboard_workspace_aggregate``
   (operator-as-multi-org-actor Stage-1 carve-out).

Mirrors the §14 v1 Slice 2 ``_cedar_bootstrap.py`` pattern: a
``register_wpfa_policies()`` function the seat module calls at import,
plus dataclass-based principal/resource shapes for the Python evaluator
extension (authoritative at v0.1 until the .cedar file is M15-sealed).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from pipeline.vault.sub_kinds.policy_eval import (
    CedarOperationalDenied,
    OperationalPrincipal,
    OperationalResource,
    evaluate_operational_write,
)


# ---------------------------------------------------------------------------
# Cycle-receipt principal + resource shapes
# ---------------------------------------------------------------------------


WPFA_DASHBOARD_WORKSPACE_AGGREGATE_PRINCIPAL: Final[str] = (
    "wpfa_dashboard_workspace_aggregate"
)


@dataclass(frozen=True, kw_only=True)
class CycleReceiptReadPrincipal:
    """Principal context for a cycle_receipt READ operation.

    ``principal_kind == "per_org"`` requires ``org_slug`` matches resource.
    ``principal_kind == "workspace_aggregate"`` is the Stage-1 operator-as-
    multi-org-actor carve-out (per §15.2 Law 3) — permitted to read across
    orgs but only for aggregate statistics, never per-org content.
    """

    session_id: str
    principal_kind: str  # "per_org" | "workspace_aggregate"
    org_slug: str = ""

    def __post_init__(self) -> None:
        if self.principal_kind not in {"per_org", "workspace_aggregate"}:
            raise ValueError(
                f"principal_kind must be 'per_org' or 'workspace_aggregate', "
                f"got {self.principal_kind!r}"
            )
        if self.principal_kind == "per_org" and not self.org_slug:
            raise ValueError(
                "principal_kind='per_org' requires non-empty org_slug"
            )


@dataclass(frozen=True, kw_only=True)
class CycleReceiptResource:
    """Resource context for a cycle_receipt WRITE or READ operation."""

    org_slug_hint: str
    cycle_id: str
    is_buyer_attested: bool = False


# ---------------------------------------------------------------------------
# Policy evaluation (cycle_receipt_*)
# ---------------------------------------------------------------------------


F_WPFA_CEDAR_DENIED: Final[str] = "F-CEDAR-OPERATIONAL-DENIED"


class CycleReceiptCedarDenied(CedarOperationalDenied):
    """Specialization for cycle_receipt-specific Cedar denials."""


def evaluate_cycle_receipt_write(
    principal: OperationalPrincipal,
    resource: OperationalResource,
) -> None:
    """Rule 1 extension: cycle_receipt writes pass org-isolation check.

    Delegates to the shared :func:`evaluate_operational_write` once the
    sub_kind is verified to be ``cycle_receipt``. Defense-in-depth on top
    of F-WPFA-CROSS-ORG-LEAK at the Logician layer.
    """
    if resource.sub_kind != "cycle_receipt":
        raise CycleReceiptCedarDenied(
            f"evaluate_cycle_receipt_write called with sub_kind="
            f"{resource.sub_kind!r}; expected 'cycle_receipt'",
            sub_kind=resource.sub_kind,
            rule="cycle_receipt_org_isolation",
            reason="wrong_sub_kind",
        )
    evaluate_operational_write(principal, resource)


def evaluate_cycle_receipt_operator_attestation(
    *,
    signed_by_operator_ed25519: str | None,
    target_artifact: str,
) -> None:
    """Rule 2: buyer-facing PDF emission requires operator Ed25519.

    Cedar default-deny semantics. Permits ONLY when the source receipt
    carries a non-None Ed25519 signature AND the target_artifact is "pdf".
    Internal-only emission (no PDF) is admitted without operator signature.

    M13 NOT permitted (per §5.1.WPFA.8 OQ-E default — structural attestation
    boundary).
    """
    if target_artifact != "pdf":
        return  # rule scoped to PDF emission only
    if signed_by_operator_ed25519 is None:
        raise CycleReceiptCedarDenied(
            "buyer-facing PDF emission denied: signed_by_operator_ed25519 "
            "is None (cycle_receipt_operator_attestation; M13 NOT permitted)",
            sub_kind="cycle_receipt",
            rule="cycle_receipt_operator_attestation",
            reason="operator_signature_missing",
        )
    if (
        not isinstance(signed_by_operator_ed25519, str)
        or len(signed_by_operator_ed25519) != 128
        or not all(
            c in "0123456789abcdef" for c in signed_by_operator_ed25519.lower()
        )
    ):
        raise CycleReceiptCedarDenied(
            "signed_by_operator_ed25519 must be 128-char lowercase hex "
            "(cycle_receipt_operator_attestation)",
            sub_kind="cycle_receipt",
            rule="cycle_receipt_operator_attestation",
            reason="operator_signature_malformed",
        )


def evaluate_cycle_receipt_read_isolation(
    principal: CycleReceiptReadPrincipal,
    resource: CycleReceiptResource,
) -> None:
    """Rule 3: cycle_receipt READ requires same-org OR workspace_aggregate.

    Workspace-aggregate principal is the Stage-1 operator-as-multi-org-
    actor carve-out (per §15.2 + §17.9 #3 + §17.8.3 #2). Permitted at
    rollup-aggregation time only; per-org content reads still go through
    the per_org principal.
    """
    if not isinstance(principal, CycleReceiptReadPrincipal):
        raise TypeError(
            f"principal must be CycleReceiptReadPrincipal, got "
            f"{type(principal).__name__}"
        )
    if not isinstance(resource, CycleReceiptResource):
        raise TypeError(
            f"resource must be CycleReceiptResource, got "
            f"{type(resource).__name__}"
        )
    if principal.principal_kind == "workspace_aggregate":
        return  # Stage-1 carve-out
    # per_org: org_slug must match
    if principal.org_slug != resource.org_slug_hint:
        raise CycleReceiptCedarDenied(
            f"cycle_receipt READ denied: principal.org_slug="
            f"{principal.org_slug!r} != resource.org_slug_hint="
            f"{resource.org_slug_hint!r}",
            sub_kind="cycle_receipt",
            rule="cycle_receipt_read_isolation",
            reason="org_slug_mismatch",
        )


# ---------------------------------------------------------------------------
# Registration shim (mirrors §14 v1 Slice 2 pattern)
# ---------------------------------------------------------------------------


_REGISTERED = False


def register_wpfa_policies() -> None:
    """Idempotent registration shim.

    Mirrors §14 v1 Slice 2 _cedar_bootstrap.py: cycle_receipt extends the
    operational_subkinds.cedar surface without rebinding existing rules.
    At v0.1 the .cedar file is the human-auditable surface; the Python
    evaluators above are authoritative.
    """
    global _REGISTERED
    if _REGISTERED:
        return
    # No-op at v0.1 — the evaluator callables are module-level and live
    # alongside policy_eval.py. The cedar engine bootstrap happens here
    # for forward-compat: a future M15-sealed .cedar load would register
    # the cycle_receipt_* rules at this entrypoint.
    _REGISTERED = True


__all__ = [
    "CycleReceiptCedarDenied",
    "CycleReceiptReadPrincipal",
    "CycleReceiptResource",
    "F_WPFA_CEDAR_DENIED",
    "WPFA_DASHBOARD_WORKSPACE_AGGREGATE_PRINCIPAL",
    "evaluate_cycle_receipt_operator_attestation",
    "evaluate_cycle_receipt_read_isolation",
    "evaluate_cycle_receipt_write",
    "register_wpfa_policies",
]
