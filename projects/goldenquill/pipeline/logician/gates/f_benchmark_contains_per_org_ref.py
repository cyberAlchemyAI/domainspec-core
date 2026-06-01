"""F-BENCHMARK-CONTAINS-PER-ORG-REF — workspace-shared write+read PRE-gate (RT-05).

Per architecture v7.0.4 §7.2.

Workspace-shared registers are Law-3-sensitive. Sovereign Node LLC
seeding is workspace-shared write; the prior text didn't prevent an
accidental seed where the source data is per-org. The gate closes the
gap with two sub-codes:

* ``F-BENCHMARK-CONTAINS-PER-ORG-REF.path`` — fires when a benchmark
  entry's ``source_doc`` path matches ``orgs/<any-slug>/...``.
  External sources only; benchmarks may not derive from any per-org
  vault subtree.

* ``F-BENCHMARK-CONTAINS-PER-ORG-REF.value`` — fires when a benchmark
  entry's ``value`` tolerance-matches a ``value`` in any per-org KFR
  (within the type-default tolerance). The match check uses
  workspace-shared canonical-value hashing — no per-org KFR content
  is exposed cross-org by the gate; only value-hash pairs.

HIGH severity. HARD_BLOCK at write (refuses to add the benchmark) and
HARD_BLOCK at read (refuses to surface the benchmark to drafting
seats — defense-in-depth catch even if a benchmark slipped through
write-time validation).

Bypass: M13 (audited operator override; HIGH severity admin-risk entry).
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from typing import Any, Final, Mapping, Optional, Sequence, Union


F_BENCHMARK_CONTAINS_PER_ORG_REF: Final[str] = "F-BENCHMARK-CONTAINS-PER-ORG-REF"
F_BENCHMARK_CONTAINS_PER_ORG_REF_PATH: Final[str] = (
    "F-BENCHMARK-CONTAINS-PER-ORG-REF.path"
)
F_BENCHMARK_CONTAINS_PER_ORG_REF_VALUE: Final[str] = (
    "F-BENCHMARK-CONTAINS-PER-ORG-REF.value"
)

# Per-org vault root prefix. ``orgs/<slug>/...`` is the per-org subtree;
# benchmarks must not source from anywhere within.
_PER_ORG_PATH_PREFIX: Final[str] = "orgs/"

# Default per-type tolerance for the value-hash collision check.
# Mirrors §4 type defaults — keeps this gate symmetrical with
# F-LOGICIAN-FACT-DRIFT's tolerance discipline.
DEFAULT_VALUE_TOLERANCE_PCT: Final[float] = 2.0


@dataclass(frozen=True, kw_only=True)
class PerOrgValueProbe:
    """Workspace-shared canonical-value probe.

    Each probe carries one per-org KFR fact's value plus a per-fact
    tolerance for the collision check. The probe shape is the I/O-
    wrapper's contract: it materializes one probe per per-org KFR
    numeric fact, stripped of fact_id / who / what / org_slug — only
    the value + tolerance + unit reach the gate, so cross-org content
    isn't exposed by the read.
    """

    value: Decimal
    unit: str
    tolerance_pct: float = DEFAULT_VALUE_TOLERANCE_PCT


@dataclass(frozen=True, kw_only=True)
class BenchmarkPerOrgRefResult:
    """Result of F-BENCHMARK-CONTAINS-PER-ORG-REF check."""

    success: bool
    failure_code: Optional[str]
    detail: str
    benchmark_id: Optional[str] = None


def _coerce_decimal(value: Any) -> Optional[Decimal]:
    if isinstance(value, Decimal):
        return value
    if isinstance(value, (int, float)):
        return Decimal(str(value))
    if isinstance(value, str):
        try:
            return Decimal(value.replace(",", "").replace("_", ""))
        except InvalidOperation:
            return None
    return None


def _path_under_per_org(path: str) -> bool:
    """True iff path begins with ``orgs/`` (after leading-./ strip)."""
    if not isinstance(path, str):
        return False
    cleaned = path.strip()
    if cleaned.startswith("./"):
        cleaned = cleaned[2:]
    return cleaned.startswith(_PER_ORG_PATH_PREFIX)


def _value_tolerance_match(
    benchmark_value: Decimal,
    probe: PerOrgValueProbe,
) -> bool:
    """True iff |benchmark - probe| / probe <= tolerance_pct (with
    zero-handling)."""
    if probe.value == 0:
        return benchmark_value == 0
    delta = abs(benchmark_value - probe.value) / probe.value * Decimal("100")
    return float(delta) <= probe.tolerance_pct


def check_benchmark_contains_per_org_ref(
    *,
    benchmark_entry: Mapping[str, Any],
    per_org_value_probes: Sequence[PerOrgValueProbe],
) -> BenchmarkPerOrgRefResult:
    """PRE-write + PRE-read gate: benchmark must not derive from per-org data.

    Sub-code dispatch
    -----------------
    * If ``source_doc`` resolves under ``orgs/<slug>/...`` → fail with
      ``.path`` sub-code.
    * Else, if benchmark ``value`` tolerance-matches any
      :class:`PerOrgValueProbe` (value + unit match within
      ``tolerance_pct``) → fail with ``.value`` sub-code.
    * Else → PASS.

    Parameters
    ----------
    benchmark_entry
        Parsed benchmark mapping (one row from
        ``vault_shared/benchmarks/register.yaml``). The gate reads
        ``benchmark_id``, ``source_doc``, ``value``, ``unit``.
    per_org_value_probes
        Workspace-shared probe sequence — one entry per numeric fact
        across all per-org KFRs at gate-fire time. The wrapper that
        materializes the probes is responsible for not exposing any
        per-org identifier; only ``value``, ``unit``, ``tolerance_pct``
        reach the gate.

    Returns
    -------
    BenchmarkPerOrgRefResult.
    """
    benchmark_id_raw = benchmark_entry.get("benchmark_id")
    benchmark_id = (
        benchmark_id_raw.strip() if isinstance(benchmark_id_raw, str) else None
    )

    source_doc = benchmark_entry.get("source_doc")
    if _path_under_per_org(source_doc if isinstance(source_doc, str) else ""):
        return BenchmarkPerOrgRefResult(
            success=False,
            failure_code=F_BENCHMARK_CONTAINS_PER_ORG_REF_PATH,
            detail=(
                f"benchmark source_doc {source_doc!r} resolves under "
                f"per-org vault prefix {_PER_ORG_PATH_PREFIX!r} — "
                "benchmarks must derive from external sources only "
                "(Law 3 cross-contamination guard)"
            ),
            benchmark_id=benchmark_id,
        )

    benchmark_value = _coerce_decimal(benchmark_entry.get("value"))
    if benchmark_value is None:
        # Non-numeric benchmark — value-hash leg trivially passes; the
        # path leg already cleared above.
        return BenchmarkPerOrgRefResult(
            success=True,
            failure_code=None,
            detail=(
                f"benchmark source_doc external; value non-numeric "
                "(value-hash leg trivially passes)"
            ),
            benchmark_id=benchmark_id,
        )

    benchmark_unit_raw = benchmark_entry.get("unit")
    benchmark_unit = (
        benchmark_unit_raw.strip().lower()
        if isinstance(benchmark_unit_raw, str)
        else ""
    )

    for probe in per_org_value_probes:
        # Unit must match for the value-collision check to be meaningful;
        # different units (USD vs acres) won't collide semantically.
        if probe.unit.strip().lower() != benchmark_unit:
            continue
        if _value_tolerance_match(benchmark_value, probe):
            return BenchmarkPerOrgRefResult(
                success=False,
                failure_code=F_BENCHMARK_CONTAINS_PER_ORG_REF_VALUE,
                detail=(
                    f"benchmark value={benchmark_value} unit={benchmark_unit!r} "
                    f"tolerance-matches a per-org KFR probe "
                    f"(probe value={probe.value}, tolerance="
                    f"{probe.tolerance_pct}%) — Law 3 cross-contamination "
                    "guard fires"
                ),
                benchmark_id=benchmark_id,
            )

    return BenchmarkPerOrgRefResult(
        success=True,
        failure_code=None,
        detail=(
            f"benchmark source_doc external and value does not "
            f"tolerance-match any of the {len(per_org_value_probes)} "
            f"per-org value probe(s)"
        ),
        benchmark_id=benchmark_id,
    )


__all__ = [
    "DEFAULT_VALUE_TOLERANCE_PCT",
    "F_BENCHMARK_CONTAINS_PER_ORG_REF",
    "F_BENCHMARK_CONTAINS_PER_ORG_REF_PATH",
    "F_BENCHMARK_CONTAINS_PER_ORG_REF_VALUE",
    "BenchmarkPerOrgRefResult",
    "PerOrgValueProbe",
    "check_benchmark_contains_per_org_ref",
]
