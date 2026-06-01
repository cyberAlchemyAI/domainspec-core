"""Unit tests for F-MATCH-DB-CROSS-ORG (PRE-gate, Law 3, P0).

Per architecture v7.0.5 §5.1.
"""

from __future__ import annotations

from pipeline.logician.gates.f_match_db_cross_org import (
    F_MATCH_DB_CROSS_ORG,
    check_match_db_cross_org,
)


def test_failure_code_constant() -> None:
    assert F_MATCH_DB_CROSS_ORG == "F-MATCH-DB-CROSS-ORG"


def test_session_org_yaml_passes() -> None:
    r = check_match_db_cross_org(
        path="orgs/mycosymbiotics_cooperative/match_database/register.yaml",
        session_slug="mycosymbiotics_cooperative",
    )
    assert r.success is True
    assert r.failure_code is None


def test_session_org_yml_passes() -> None:
    r = check_match_db_cross_org(
        path="orgs/fit_farms/match_database/cycle_2026.yml",
        session_slug="fit_farms",
    )
    assert r.success is True


def test_session_org_json_passes() -> None:
    r = check_match_db_cross_org(
        path="orgs/run_a_muck/match_database/state.json",
        session_slug="run_a_muck",
    )
    assert r.success is True


def test_cross_org_path_fails() -> None:
    r = check_match_db_cross_org(
        path="orgs/other_org/match_database/leak.yaml",
        session_slug="mycosymbiotics_cooperative",
    )
    assert r.success is False
    assert r.failure_code == F_MATCH_DB_CROSS_ORG


def test_traversal_attempt_fails() -> None:
    r = check_match_db_cross_org(
        path="orgs/mycosymbiotics_cooperative/match_database/../../other/leak.yaml",
        session_slug="mycosymbiotics_cooperative",
    )
    assert r.success is False
    assert r.failure_code == F_MATCH_DB_CROSS_ORG
    assert "traversal" in r.detail


def test_wrong_extension_fails() -> None:
    r = check_match_db_cross_org(
        path="orgs/fit_farms/match_database/leak.txt",
        session_slug="fit_farms",
    )
    assert r.success is False
    assert r.failure_code == F_MATCH_DB_CROSS_ORG


def test_subdirectory_fails() -> None:
    # Match DB files must be flat under match_database/, no subdirectories
    r = check_match_db_cross_org(
        path="orgs/fit_farms/match_database/sub/sneaky.yaml",
        session_slug="fit_farms",
    )
    assert r.success is False
    assert r.failure_code == F_MATCH_DB_CROSS_ORG


def test_empty_session_slug_fails_closed() -> None:
    r = check_match_db_cross_org(
        path="orgs/fit_farms/match_database/register.yaml",
        session_slug="",
    )
    assert r.success is False
    assert r.failure_code == F_MATCH_DB_CROSS_ORG
    assert "empty session_slug" in r.detail


def test_path_outside_orgs_fails() -> None:
    r = check_match_db_cross_org(
        path="vault_shared/funder_intelligence/register.yaml",
        session_slug="fit_farms",
    )
    assert r.success is False
    assert r.failure_code == F_MATCH_DB_CROSS_ORG
