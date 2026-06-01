"""Python evaluator for ``operational_subkinds.cedar``. [§6, §7]

Authoritative at v0.1 — mirrors the §2 v7.1 §3.4 lifecycle for
``org_isolation.cedar`` (fallback evaluator at
``pipeline/logician/cedar_eval.py::evaluate_org_isolation`` is authoritative
until the .cedar file is M15-sealed).

Three rules from ``operational_subkinds.cedar``:

1. ``operational_org_isolation`` — permits operational writes when
   ``principal.org_slug == resource.org_slug_hint``.
2. ``beneficiary_pii_anonymized`` — permits beneficiary writes when
   ``resource.consent_tier == "anonymized"`` AND ``resource.pii_present == False``.
3. ``beneficiary_pii_with_consent`` — permits beneficiary writes when
   ``resource.consent_tier == "operator-authorized-identified"`` AND
   ``resource.pii_present == True`` AND
   ``principal.operator_authorized_pii == True``.

Anything else → deny → :class:`CedarOperationalDenied`.

Schema-side enforcement:
    The :class:`pipeline.vault.sub_kinds.beneficiary_records.BeneficiaryRecord`
    ``__post_init__`` rejects any record that violates the consent-tier ↔
    PII consistency invariant before bytes touch disk. The Cedar evaluator
    here is the second layer (belt-and-suspenders) — a tampered-on-disk
    record that bypasses the schema validator (e.g. operator manually
    crafted the file) still hits the policy gate when re-read at write
    time. The two layers cover schema-bypass and Cedar-bypass attacks
    independently.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Final

from pipeline.vault.error_codes import VaultError
from pipeline.vault.sub_kinds import beneficiary_records as _beneficiary

BLUEPRINT_DEPS: Final[dict[str, dict[str, object]]] = {
    "section_02_v7_2_amendment.md": {
        "version": "v7.2-DRAFT",
        "sections_implemented": [
            "§6 operational_subkinds.cedar Python evaluator",
            "§7 F-CEDAR-OPERATIONAL-DENIED + F-OPERATIONAL-PII-CONSENT-MISSING + F-OPERATIONAL-SCHEMA-INVALID",
        ],
    },
}


# ---------------------------------------------------------------------------
# Failure codes (v7.2 §7 additions)
# ---------------------------------------------------------------------------

F_CEDAR_OPERATIONAL_DENIED: Final[str] = "F-CEDAR-OPERATIONAL-DENIED"
F_OPERATIONAL_PII_CONSENT_MISSING: Final[str] = "F-OPERATIONAL-PII-CONSENT-MISSING"
F_OPERATIONAL_SCHEMA_INVALID: Final[str] = "F-OPERATIONAL-SCHEMA-INVALID"


class CedarOperationalDenied(VaultError):
    code = F_CEDAR_OPERATIONAL_DENIED

    def __init__(
        self,
        message: str = "",
        *,
        sub_kind: str = "",
        rule: str = "",
        reason: str = "",
    ) -> None:
        super().__init__(message)
        self.sub_kind = sub_kind
        self.rule = rule
        self.reason = reason


class OperationalPIIConsentMissing(VaultError):
    code = F_OPERATIONAL_PII_CONSENT_MISSING


class OperationalSchemaInvalid(VaultError):
    code = F_OPERATIONAL_SCHEMA_INVALID


# ---------------------------------------------------------------------------
# Principal + resource shapes (Cedar-equivalent, plain-Python at v0.1)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class OperationalPrincipal:
    """Principal context for an operational write decision."""

    session_id: str
    org_slug: str
    operator_authorized_pii: bool = False


@dataclass(frozen=True, kw_only=True)
class OperationalResource:
    """Resource context for an operational write decision.

    Mirrors the fields a Cedar resource carries: ``org_slug_hint`` for
    isolation, ``sub_kind`` for sub-kind dispatch, and
    ``(consent_tier, pii_present)`` for the beneficiary-only rules. The
    last two are ``None`` for non-beneficiary sub-kinds.
    """

    sub_kind: str
    org_slug_hint: str
    consent_tier: str | None = None
    pii_present: bool | None = None


# ---------------------------------------------------------------------------
# Policy evaluation
# ---------------------------------------------------------------------------


def _evaluate_org_isolation(
    principal: OperationalPrincipal, resource: OperationalResource
) -> bool:
    """Rule 1: same-org match."""
    return (
        isinstance(principal.org_slug, str)
        and isinstance(resource.org_slug_hint, str)
        and principal.org_slug == resource.org_slug_hint
        and principal.org_slug != ""
    )


def _evaluate_beneficiary_anonymized(resource: OperationalResource) -> bool:
    """Rule 2: anonymized beneficiary write."""
    return (
        resource.sub_kind == _beneficiary.SUB_KIND
        and resource.consent_tier == _beneficiary.CONSENT_TIER_ANONYMIZED
        and resource.pii_present is False
    )


def _evaluate_beneficiary_with_consent(
    principal: OperationalPrincipal, resource: OperationalResource
) -> bool:
    """Rule 3: identified beneficiary write with operator PII authorization."""
    return (
        resource.sub_kind == _beneficiary.SUB_KIND
        and resource.consent_tier
        == _beneficiary.CONSENT_TIER_OPERATOR_AUTHORIZED_IDENTIFIED
        and resource.pii_present is True
        and principal.operator_authorized_pii is True
    )


def evaluate_operational_write(
    principal: OperationalPrincipal,
    resource: OperationalResource,
) -> None:
    """Evaluate a proposed operational write.

    :raises CedarOperationalDenied: no rule permits the write.
    :raises OperationalPIIConsentMissing: beneficiary record claims PII but
        the principal lacks ``operator_authorized_pii``.
    """
    if not isinstance(principal, OperationalPrincipal):
        raise TypeError(
            f"principal must be OperationalPrincipal, got {type(principal).__name__}"
        )
    if not isinstance(resource, OperationalResource):
        raise TypeError(
            f"resource must be OperationalResource, got {type(resource).__name__}"
        )
    # Rule 1 must always hold (org isolation is universal).
    if not _evaluate_org_isolation(principal, resource):
        raise CedarOperationalDenied(
            f"operational_org_isolation: principal.org_slug={principal.org_slug!r} "
            f"!= resource.org_slug_hint={resource.org_slug_hint!r}",
            sub_kind=resource.sub_kind,
            rule="operational_org_isolation",
            reason="org_slug_mismatch",
        )
    # Beneficiary-specific layered enforcement.
    if resource.sub_kind == _beneficiary.SUB_KIND:
        if _evaluate_beneficiary_anonymized(resource):
            return
        if _evaluate_beneficiary_with_consent(principal, resource):
            return
        # Anything else for beneficiary records is a PII discipline failure.
        if resource.pii_present is True and not principal.operator_authorized_pii:
            raise OperationalPIIConsentMissing(
                "beneficiary record has pii_present=True but principal lacks "
                "operator_authorized_pii",
            )
        raise CedarOperationalDenied(
            f"beneficiary write denied: consent_tier={resource.consent_tier!r}, "
            f"pii_present={resource.pii_present!r}, "
            f"operator_authorized_pii={principal.operator_authorized_pii!r}",
            sub_kind=resource.sub_kind,
            rule="beneficiary_pii_consent",
            reason="consent_tier_mismatch_or_pii_unauthorized",
        )
    # §17 WPFA: cycle_receipt extends the default-permit set explicitly.
    # The wpfa _cedar_bootstrap layer adds buyer-PDF-specific gates on top.
    # Non-beneficiary operational writes (including cycle_receipt) pass
    # once org isolation holds.
    return


__all__ = [
    "BLUEPRINT_DEPS",
    "CedarOperationalDenied",
    "F_CEDAR_OPERATIONAL_DENIED",
    "F_OPERATIONAL_PII_CONSENT_MISSING",
    "F_OPERATIONAL_SCHEMA_INVALID",
    "OperationalPIIConsentMissing",
    "OperationalPrincipal",
    "OperationalResource",
    "OperationalSchemaInvalid",
    "evaluate_operational_write",
]
