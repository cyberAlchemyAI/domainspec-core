"""F-BENCHMARK-SEEDING-SOURCE-UNAUTHORIZED tests (M1 §5.4)."""

from __future__ import annotations

from pipeline.logician.benchmarks.seeding_allowlist_loader import SeedingAllowlist
from pipeline.logician.gates.f_benchmark_seeding_source_unauthorized import (
    F_BENCHMARK_SEEDING_SOURCE_UNAUTHORIZED,
    check_benchmark_seeding_source_unauthorized,
)


def _allowlist() -> SeedingAllowlist:
    return SeedingAllowlist(
        populated_by="op1",
        populated_at="2026-05-10T00:00:00Z",
        allowed_source_domains=("*.usda.gov", "*.nsf.gov"),
        allowed_source_path_prefixes=("vault_shared/funder_intelligence/docs/",),
        forbidden_source_path_prefixes=("orgs/",),
    )


def test_failure_code_constant() -> None:
    assert (
        F_BENCHMARK_SEEDING_SOURCE_UNAUTHORIZED
        == "F-BENCHMARK-SEEDING-SOURCE-UNAUTHORIZED"
    )


def test_allowed_domain_passes() -> None:
    r = check_benchmark_seeding_source_unauthorized(
        benchmark_id="B1",
        source_doc="https://www.usda.gov/data/2026.pdf",
        allowlist=_allowlist(),
    )
    assert r.success is True


def test_forbidden_path_prefix_fails() -> None:
    r = check_benchmark_seeding_source_unauthorized(
        benchmark_id="B1",
        source_doc="orgs/example/vault/financial.pdf",
        allowlist=_allowlist(),
    )
    assert r.success is False
    assert r.failure_code == F_BENCHMARK_SEEDING_SOURCE_UNAUTHORIZED


def test_allowed_path_prefix_passes() -> None:
    r = check_benchmark_seeding_source_unauthorized(
        benchmark_id="B1",
        source_doc="vault_shared/funder_intelligence/docs/usda_vapg_fy26.pdf",
        allowlist=_allowlist(),
    )
    assert r.success is True


def test_unknown_source_fails() -> None:
    r = check_benchmark_seeding_source_unauthorized(
        benchmark_id="B1",
        source_doc="https://random-blog.example.com/post",
        allowlist=_allowlist(),
    )
    assert r.success is False
