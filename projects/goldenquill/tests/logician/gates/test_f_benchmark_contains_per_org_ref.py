"""Unit tests for F-BENCHMARK-CONTAINS-PER-ORG-REF (PRE-write+read, RT-05).

Per architecture v7.0.4 §7.2.
"""

from __future__ import annotations

from decimal import Decimal

from pipeline.logician.gates.f_benchmark_contains_per_org_ref import (
    DEFAULT_VALUE_TOLERANCE_PCT,
    F_BENCHMARK_CONTAINS_PER_ORG_REF,
    F_BENCHMARK_CONTAINS_PER_ORG_REF_PATH,
    F_BENCHMARK_CONTAINS_PER_ORG_REF_VALUE,
    PerOrgValueProbe,
    check_benchmark_contains_per_org_ref,
)


def _external_benchmark(
    bid: str = "pa_avg_2025",
    source_doc: str = "PA Department of Education Annual Report 2025",
    value: object = 0.84,
    unit: str = "percentage",
) -> dict:
    return {
        "benchmark_id": bid,
        "source_doc": source_doc,
        "value": value,
        "unit": unit,
    }


def test_failure_code_constants() -> None:
    assert F_BENCHMARK_CONTAINS_PER_ORG_REF == "F-BENCHMARK-CONTAINS-PER-ORG-REF"
    assert F_BENCHMARK_CONTAINS_PER_ORG_REF_PATH == (
        "F-BENCHMARK-CONTAINS-PER-ORG-REF.path"
    )
    assert F_BENCHMARK_CONTAINS_PER_ORG_REF_VALUE == (
        "F-BENCHMARK-CONTAINS-PER-ORG-REF.value"
    )


def test_external_source_unique_value_passes() -> None:
    probes = [
        PerOrgValueProbe(value=Decimal("197"), unit="count"),
    ]
    r = check_benchmark_contains_per_org_ref(
        benchmark_entry=_external_benchmark(),
        per_org_value_probes=probes,
    )
    assert r.success is True


def test_per_org_path_fails_with_path_subcode() -> None:
    benchmark = _external_benchmark(
        source_doc="orgs/mycosymbiotics_cooperative/vault/financials.pdf",
    )
    r = check_benchmark_contains_per_org_ref(
        benchmark_entry=benchmark,
        per_org_value_probes=[],
    )
    assert r.success is False
    assert r.failure_code == F_BENCHMARK_CONTAINS_PER_ORG_REF_PATH
    assert "Law 3" in r.detail


def test_dot_slash_orgs_path_also_fails() -> None:
    benchmark = _external_benchmark(
        source_doc="./orgs/run_a_muck_farm/source.pdf",
    )
    r = check_benchmark_contains_per_org_ref(
        benchmark_entry=benchmark,
        per_org_value_probes=[],
    )
    assert r.success is False
    assert r.failure_code == F_BENCHMARK_CONTAINS_PER_ORG_REF_PATH


def test_value_collision_within_tolerance_fails_with_value_subcode() -> None:
    benchmark = _external_benchmark(value=200, unit="count")
    probes = [
        PerOrgValueProbe(
            value=Decimal("197"), unit="count", tolerance_pct=2.0
        ),  # 197 ±2% = ~193..201, 200 is in
    ]
    r = check_benchmark_contains_per_org_ref(
        benchmark_entry=benchmark,
        per_org_value_probes=probes,
    )
    assert r.success is False
    assert r.failure_code == F_BENCHMARK_CONTAINS_PER_ORG_REF_VALUE
    assert "Law 3" in r.detail


def test_value_collision_outside_tolerance_passes() -> None:
    benchmark = _external_benchmark(value=300, unit="count")
    probes = [
        PerOrgValueProbe(
            value=Decimal("197"), unit="count", tolerance_pct=2.0
        ),
    ]
    r = check_benchmark_contains_per_org_ref(
        benchmark_entry=benchmark,
        per_org_value_probes=probes,
    )
    assert r.success is True


def test_unit_mismatch_skips_value_collision() -> None:
    # 197 USD vs 197 acres should not collide.
    benchmark = _external_benchmark(value=197, unit="acres")
    probes = [
        PerOrgValueProbe(value=Decimal("197"), unit="USD", tolerance_pct=2.0),
    ]
    r = check_benchmark_contains_per_org_ref(
        benchmark_entry=benchmark,
        per_org_value_probes=probes,
    )
    assert r.success is True


def test_unit_match_case_insensitive() -> None:
    benchmark = _external_benchmark(value=197, unit="USD")
    probes = [
        PerOrgValueProbe(value=Decimal("197"), unit="usd", tolerance_pct=2.0),
    ]
    r = check_benchmark_contains_per_org_ref(
        benchmark_entry=benchmark,
        per_org_value_probes=probes,
    )
    assert r.success is False
    assert r.failure_code == F_BENCHMARK_CONTAINS_PER_ORG_REF_VALUE


def test_path_check_fires_before_value_check() -> None:
    # Both legs would fail; path leg fires first per dispatch order.
    benchmark = _external_benchmark(
        source_doc="orgs/mycosymbiotics/data.pdf",
        value=197,
        unit="count",
    )
    probes = [
        PerOrgValueProbe(value=Decimal("197"), unit="count"),
    ]
    r = check_benchmark_contains_per_org_ref(
        benchmark_entry=benchmark,
        per_org_value_probes=probes,
    )
    assert r.failure_code == F_BENCHMARK_CONTAINS_PER_ORG_REF_PATH


def test_zero_value_probe_only_collides_with_zero_benchmark() -> None:
    probes = [PerOrgValueProbe(value=Decimal(0), unit="count")]
    r_collide = check_benchmark_contains_per_org_ref(
        benchmark_entry=_external_benchmark(value=0, unit="count"),
        per_org_value_probes=probes,
    )
    assert r_collide.success is False

    r_distinct = check_benchmark_contains_per_org_ref(
        benchmark_entry=_external_benchmark(value=10, unit="count"),
        per_org_value_probes=probes,
    )
    assert r_distinct.success is True


def test_non_numeric_benchmark_value_passes_value_leg() -> None:
    benchmark = _external_benchmark(value="not-a-number", unit="count")
    probes = [PerOrgValueProbe(value=Decimal("197"), unit="count")]
    r = check_benchmark_contains_per_org_ref(
        benchmark_entry=benchmark,
        per_org_value_probes=probes,
    )
    assert r.success is True
    assert "non-numeric" in r.detail


def test_no_probes_passes_value_leg() -> None:
    r = check_benchmark_contains_per_org_ref(
        benchmark_entry=_external_benchmark(),
        per_org_value_probes=[],
    )
    assert r.success is True


def test_default_tolerance_constant() -> None:
    assert DEFAULT_VALUE_TOLERANCE_PCT == 2.0


def test_string_value_parsed_to_decimal() -> None:
    benchmark = _external_benchmark(value="1,250", unit="count")
    probes = [
        PerOrgValueProbe(value=Decimal("1250"), unit="count", tolerance_pct=0.5),
    ]
    r = check_benchmark_contains_per_org_ref(
        benchmark_entry=benchmark,
        per_org_value_probes=probes,
    )
    assert r.success is False
    assert r.failure_code == F_BENCHMARK_CONTAINS_PER_ORG_REF_VALUE


def test_external_path_passes_when_value_distinct() -> None:
    benchmark = _external_benchmark(
        source_doc="vault_shared/funder_intelligence/USDA/synopsis.pdf",
        value=42,
        unit="count",
    )
    probes = [PerOrgValueProbe(value=Decimal("197"), unit="count")]
    r = check_benchmark_contains_per_org_ref(
        benchmark_entry=benchmark,
        per_org_value_probes=probes,
    )
    assert r.success is True
