"""Unit tests for F-VECTOR-NS-MISMATCH (PRE-gate, Law 3, P0).

Per architecture v7.0.5 §5.2.
"""

from __future__ import annotations

from pipeline.logician.gates.f_vector_ns_mismatch import (
    F_VECTOR_NS_MISMATCH,
    PER_ORG_NAMESPACE_PREFIXES,
    WORKSPACE_SCOPED_NAMESPACES,
    check_vector_ns_mismatch,
)


def test_failure_code_constant() -> None:
    assert F_VECTOR_NS_MISMATCH == "F-VECTOR-NS-MISMATCH"


def test_workspace_namespace_funder_intel_skips_slug_check() -> None:
    # Workspace-scoped — slug irrelevant
    r = check_vector_ns_mismatch(
        namespace="funder_intel/",
        requested_org_slug=None,
        session_slug="fit_farms",
    )
    assert r.success is True


def test_workspace_namespace_benchmarks_skips_slug_check() -> None:
    r = check_vector_ns_mismatch(
        namespace="benchmarks/",
        requested_org_slug="anyone",
        session_slug="fit_farms",
    )
    assert r.success is True


def test_per_org_kfr_facts_matching_slug_passes() -> None:
    r = check_vector_ns_mismatch(
        namespace="kfr_facts/fit_farms/",
        requested_org_slug="fit_farms",
        session_slug="fit_farms",
    )
    assert r.success is True


def test_per_org_kfr_facts_mismatched_slug_fails() -> None:
    r = check_vector_ns_mismatch(
        namespace="kfr_facts/fit_farms/",
        requested_org_slug="other_org",
        session_slug="fit_farms",
    )
    assert r.success is False
    assert r.failure_code == F_VECTOR_NS_MISMATCH
    assert "does not match" in r.detail


def test_per_org_kfr_facts_missing_slug_fails_closed() -> None:
    r = check_vector_ns_mismatch(
        namespace="kfr_facts/fit_farms/",
        requested_org_slug=None,
        session_slug="fit_farms",
    )
    assert r.success is False
    assert r.failure_code == F_VECTOR_NS_MISMATCH


def test_per_org_namespace_path_slug_segment_must_match() -> None:
    # tool slug arg matches session, but namespace path encodes a different slug
    r = check_vector_ns_mismatch(
        namespace="kfr_facts/other_org/",
        requested_org_slug="fit_farms",
        session_slug="fit_farms",
    )
    assert r.success is False
    assert r.failure_code == F_VECTOR_NS_MISMATCH


def test_match_db_namespace_forward_design_protection() -> None:
    # match_db/ namespace is forward-design — same enforcement should apply
    r = check_vector_ns_mismatch(
        namespace="match_db/fit_farms/",
        requested_org_slug="fit_farms",
        session_slug="fit_farms",
    )
    assert r.success is True


def test_unrecognized_namespace_fails_closed() -> None:
    r = check_vector_ns_mismatch(
        namespace="random_unknown_ns/",
        requested_org_slug="fit_farms",
        session_slug="fit_farms",
    )
    assert r.success is False
    assert r.failure_code == F_VECTOR_NS_MISMATCH


def test_empty_session_slug_fails_closed() -> None:
    r = check_vector_ns_mismatch(
        namespace="kfr_facts/fit_farms/",
        requested_org_slug="fit_farms",
        session_slug="",
    )
    assert r.success is False
    assert r.failure_code == F_VECTOR_NS_MISMATCH


def test_namespace_constants_exported() -> None:
    assert "funder_intel/" in WORKSPACE_SCOPED_NAMESPACES
    assert "kfr_facts/" in PER_ORG_NAMESPACE_PREFIXES
    assert "match_db/" in PER_ORG_NAMESPACE_PREFIXES
