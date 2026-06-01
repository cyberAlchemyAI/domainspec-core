"""F-WPFA-REGISTRY-DRIFT — POST-load advisory gate. [§5.1.WPFA.10]

Trigger: local hardware measurement deviates >X% from SN-LLC registry
coefficient for the same SKU (advisory threshold operator-tunable;
default X=20%).

Surfaces measurement-vs-publication mismatch. Does NOT fail-close pipeline.

Sub-tags: ``.idle_watts_drift``, ``.peak_watts_drift``,
``.watt_hours_per_million_drift``, ``.registry_version_mismatch_no_ledger_entry``.
M13 not needed (advisory).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Final, Optional


F_WPFA_REGISTRY_DRIFT: Final[str] = "F-WPFA-REGISTRY-DRIFT"

# Default tolerance for drift advisory (20%; operator-tunable).
_DEFAULT_TOLERANCE_BASIS_POINTS: Final[int] = 2000  # 20% = 2000 bps


@dataclass(frozen=True, kw_only=True)
class RegistryDriftAdvisory:
    """One drift observation. Multiple may surface per check."""

    sub_tag: str
    detail: str
    metric_name: str
    registry_value_micro: int
    measured_value_micro: int
    deviation_basis_points: int  # signed; (measured - registry) / registry * 10000


@dataclass(frozen=True, kw_only=True)
class RegistryDriftResult:
    success: bool  # True iff no drift exceeded tolerance
    failure_code: Optional[str]
    detail: str
    advisories: tuple[RegistryDriftAdvisory, ...] = ()


def _basis_points(measured: int, registry: int) -> int:
    """Signed basis points = (measured - registry) / registry * 10000.

    A12 — int-only arithmetic. Zero registry value returns 0 deviation
    (avoid div-by-zero; downstream advisory should flag separately).
    """
    if registry == 0:
        return 0
    # Use integer math: (measured - registry) * 10000 // registry,
    # ROUND_HALF_EVEN approximated by floor for non-negative numerator.
    diff = measured - registry
    sign = 1 if diff >= 0 else -1
    return sign * (abs(diff) * 10000 // registry)


def check_f_wpfa_registry_drift(
    *,
    hardware_sku: str,
    measured_idle_watts_micro: Optional[int],
    measured_peak_watts_micro: Optional[int],
    measured_watt_hours_per_million_input_tokens_micro: Optional[int],
    measured_watt_hours_per_million_output_tokens_micro: Optional[int],
    registry_idle_watts_micro: Optional[int],
    registry_peak_watts_micro: Optional[int],
    registry_watt_hours_per_million_input_tokens_micro: Optional[int],
    registry_watt_hours_per_million_output_tokens_micro: Optional[int],
    tolerance_basis_points: int = _DEFAULT_TOLERANCE_BASIS_POINTS,
) -> RegistryDriftResult:
    """POST-load: surface advisories for >tolerance drift on local-SKU metrics.

    All measured values may be None — in which case no drift can be computed
    for that metric and no advisory surfaces. Cloud models (is_local=False)
    invoke with all None; this gate returns success.
    """
    if tolerance_basis_points < 0:
        return RegistryDriftResult(
            success=False,
            failure_code=F_WPFA_REGISTRY_DRIFT,
            detail=(
                f"tolerance_basis_points must be non-negative, got "
                f"{tolerance_basis_points}"
            ),
        )
    advisories: list[RegistryDriftAdvisory] = []
    for sub_tag, metric_name, measured, registry in (
        (
            "idle_watts_drift",
            "idle_watts_micro",
            measured_idle_watts_micro,
            registry_idle_watts_micro,
        ),
        (
            "peak_watts_drift",
            "peak_watts_micro",
            measured_peak_watts_micro,
            registry_peak_watts_micro,
        ),
        (
            "watt_hours_per_million_drift",
            "watt_hours_per_million_input_tokens_micro",
            measured_watt_hours_per_million_input_tokens_micro,
            registry_watt_hours_per_million_input_tokens_micro,
        ),
        (
            "watt_hours_per_million_drift",
            "watt_hours_per_million_output_tokens_micro",
            measured_watt_hours_per_million_output_tokens_micro,
            registry_watt_hours_per_million_output_tokens_micro,
        ),
    ):
        if measured is None or registry is None:
            continue
        if (
            isinstance(measured, bool)
            or isinstance(registry, bool)
            or not isinstance(measured, int)
            or not isinstance(registry, int)
        ):
            continue  # advisory gate — silently skip malformed inputs
        dev = _basis_points(measured, registry)
        if abs(dev) > tolerance_basis_points:
            advisories.append(
                RegistryDriftAdvisory(
                    sub_tag=sub_tag,
                    metric_name=metric_name,
                    detail=(
                        f"{hardware_sku} {metric_name}: measured {measured} "
                        f"vs registry {registry} "
                        f"(deviation {dev} bps, tolerance "
                        f"{tolerance_basis_points} bps)"
                    ),
                    registry_value_micro=registry,
                    measured_value_micro=measured,
                    deviation_basis_points=dev,
                )
            )
    if advisories:
        return RegistryDriftResult(
            success=False,  # advisory — caller does not fail pipeline
            failure_code=F_WPFA_REGISTRY_DRIFT,
            detail=(
                f"{len(advisories)} drift advisory/advisories for "
                f"hardware_sku {hardware_sku!r}"
            ),
            advisories=tuple(advisories),
        )
    return RegistryDriftResult(
        success=True,
        failure_code=None,
        detail=(
            f"no drift exceeded tolerance {tolerance_basis_points} bps "
            f"for hardware_sku {hardware_sku!r}"
        ),
    )


def check_registry_version_mismatch_no_ledger_entry(
    *,
    receipt_registry_version: str,
    active_registry_version: str,
    admin_risk_ledger_entries_for_cycle: tuple[str, ...],
) -> RegistryDriftResult:
    """POST-load: sub-tag for receipts pinning a non-active registry version
    without a justifying admin-risk-ledger entry.
    """
    if receipt_registry_version == active_registry_version:
        return RegistryDriftResult(
            success=True,
            failure_code=None,
            detail="receipt pins active registry version",
        )
    if not admin_risk_ledger_entries_for_cycle:
        return RegistryDriftResult(
            success=False,
            failure_code=F_WPFA_REGISTRY_DRIFT,
            detail=(
                f"receipt pins registry version {receipt_registry_version!r} "
                f"but active is {active_registry_version!r} and no admin-risk-"
                "ledger entry justifies the recomputation — "
                ".registry_version_mismatch_no_ledger_entry"
            ),
            advisories=(
                RegistryDriftAdvisory(
                    sub_tag="registry_version_mismatch_no_ledger_entry",
                    metric_name="coefficients_registry_version",
                    detail=(
                        f"{receipt_registry_version!r} != "
                        f"{active_registry_version!r}"
                    ),
                    registry_value_micro=0,
                    measured_value_micro=0,
                    deviation_basis_points=0,
                ),
            ),
        )
    return RegistryDriftResult(
        success=True,
        failure_code=None,
        detail=(
            "receipt pins non-active registry version but admin-risk-ledger "
            "entry justifies it"
        ),
    )


__all__ = [
    "F_WPFA_REGISTRY_DRIFT",
    "RegistryDriftAdvisory",
    "RegistryDriftResult",
    "check_f_wpfa_registry_drift",
    "check_registry_version_mismatch_no_ledger_entry",
]
