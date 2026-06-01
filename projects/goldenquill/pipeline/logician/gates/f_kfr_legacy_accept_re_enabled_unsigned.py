"""F-KFR-LEGACY-ACCEPT-RE-ENABLED-UNSIGNED — KFR PRE-write gate (M1 §2.6.3).

After legacy-accept migration completes for an org, re-enabling
``legacy_accept_mode`` from ``disabled`` / ``completed`` back to
``enabled`` is a tamper event.  The transition requires an
operator-signed admin-risk-ledger entry with rationale; the gate
fails-closed when the ledger entry is absent or the operator has not
signed.

Bypass: M13 (audited operator override; HIGH severity admin-risk entry).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Final, Mapping, Optional, Sequence

from pipeline.logician.canonicalization.legacy_migration import (
    LEGACY_ACCEPT_COMPLETED,
    LEGACY_ACCEPT_DISABLED,
    LEGACY_ACCEPT_ENABLED,
)


F_KFR_LEGACY_ACCEPT_RE_ENABLED_UNSIGNED: Final[str] = (
    "F-KFR-LEGACY-ACCEPT-RE-ENABLED-UNSIGNED"
)

LEDGER_KIND_LEGACY_RE_ENABLE: Final[str] = "kfr_legacy_accept_re_enable"


@dataclass(frozen=True, kw_only=True)
class LegacyAcceptReEnabledResult:
    success: bool
    failure_code: Optional[str]
    detail: str
    org_slug: Optional[str] = None


def _has_signed_re_enable_ledger_entry(
    ledger_entries: Sequence[Mapping[str, Any]],
    *,
    org_slug: str,
) -> bool:
    for row in ledger_entries:
        if not isinstance(row, Mapping):
            continue
        if row.get("ledger_kind") != LEDGER_KIND_LEGACY_RE_ENABLE:
            continue
        if row.get("org_slug") != org_slug:
            continue
        signed = row.get("signed_at_utc")
        operator_key = row.get("operator_key_id")
        rationale = row.get("rationale")
        if not isinstance(signed, str) or not signed.strip():
            continue
        if not isinstance(operator_key, str) or not operator_key.strip():
            continue
        if not isinstance(rationale, str) or not rationale.strip():
            continue
        return True
    return False


def check_kfr_legacy_accept_re_enabled_unsigned(
    *,
    org_slug: str,
    previous_mode: str,
    new_mode: str,
    ledger_entries: Sequence[Mapping[str, Any]],
) -> LegacyAcceptReEnabledResult:
    """PRE-write gate: refuse re-enable without operator-signed ledger row.

    Parameters
    ----------
    previous_mode
        The on-disk legacy_accept_mode BEFORE this write.
    new_mode
        The on-disk legacy_accept_mode AFTER this write.
    """
    if previous_mode == new_mode:
        return LegacyAcceptReEnabledResult(
            success=True,
            failure_code=None,
            detail=(
                f"legacy_accept_mode unchanged ({previous_mode!r}); "
                "no transition to re-confirm"
            ),
            org_slug=org_slug,
        )
    if new_mode != LEGACY_ACCEPT_ENABLED:
        return LegacyAcceptReEnabledResult(
            success=True,
            failure_code=None,
            detail=(
                f"legacy_accept_mode transition "
                f"{previous_mode!r}→{new_mode!r} not a re-enable "
                "(targeted only at enabled)"
            ),
            org_slug=org_slug,
        )
    # Transition INTO enabled — only legitimate from a fresh state
    # (where previous_mode is the pre-migration phase, i.e., when
    # migration was first kicked off).  After the org has reached
    # disabled or completed, re-enable requires a signed ledger row.
    if previous_mode in {LEGACY_ACCEPT_DISABLED, LEGACY_ACCEPT_COMPLETED}:
        if not _has_signed_re_enable_ledger_entry(
            ledger_entries, org_slug=org_slug
        ):
            return LegacyAcceptReEnabledResult(
                success=False,
                failure_code=F_KFR_LEGACY_ACCEPT_RE_ENABLED_UNSIGNED,
                detail=(
                    f"legacy_accept_mode transition "
                    f"{previous_mode!r}→{LEGACY_ACCEPT_ENABLED!r} for "
                    f"org {org_slug!r} requires a signed admin-risk-"
                    f"ledger row of kind "
                    f"{LEDGER_KIND_LEGACY_RE_ENABLE!r} with operator "
                    "signature + rationale; none found"
                ),
                org_slug=org_slug,
            )
    return LegacyAcceptReEnabledResult(
        success=True,
        failure_code=None,
        detail=(
            f"legacy_accept_mode re-enable from {previous_mode!r} "
            "authorized via signed admin-risk-ledger row"
        ),
        org_slug=org_slug,
    )


__all__ = [
    "F_KFR_LEGACY_ACCEPT_RE_ENABLED_UNSIGNED",
    "LEDGER_KIND_LEGACY_RE_ENABLE",
    "LegacyAcceptReEnabledResult",
    "check_kfr_legacy_accept_re_enabled_unsigned",
]
