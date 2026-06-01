"""Tests for F-CARDS-COVERAGE-INCOMPLETE META gate.

The META gate is LIVE at v7.0.11 LOCK — its body is tested for real behavior,
not NotImplementedError smoke. Mirrors v7.0.7 §5.1 F-CLASS-COVERAGE-INCOMPLETE
test discipline + §16 v1 F-PACKET-COVERAGE-INCOMPLETE row-222 pattern.
"""

from __future__ import annotations

import pytest


def test_gate_imports_cleanly():
    from pipeline.logician.gates import f_cards_coverage_incomplete  # noqa: F401


def test_required_module_paths_listed():
    from pipeline.logician.gates.f_cards_coverage_incomplete import (
        REQUIRED_F_CARDS_MODULES,
        REQUIRED_F_CARDS_TEST_PATHS,
    )
    # Self-coverage check — the META gate's own module should NOT be in the list
    # (auditor not auditee, per F-CLASS-COVERAGE-INCOMPLETE precedent).
    # Wait — actually for our family roster we include the META gate itself.
    # The list should be exactly 10 entries: 7 F-CARDS-* + COVERAGE-INCOMPLETE + 2 extras = 10.
    assert len(REQUIRED_F_CARDS_MODULES) == 10
    assert len(REQUIRED_F_CARDS_TEST_PATHS) == 10


def test_module_coverage_check_with_all_modules_present():
    """When every required module exists on disk, the check returns empty."""
    from pipeline.logician.gates.f_cards_coverage_incomplete import (
        check_module_coverage,
        REQUIRED_F_CARDS_MODULES,
    )

    # Stub file_exists callable that says every required path exists.
    missing_modules, missing_tests = check_module_coverage(
        file_exists=lambda p: True,
    )
    assert missing_modules == ()
    assert missing_tests == ()


def test_module_coverage_check_with_missing_module():
    """When a required module is missing, the check reports it."""
    from pipeline.logician.gates.f_cards_coverage_incomplete import (
        check_module_coverage,
        REQUIRED_F_CARDS_MODULES,
    )

    missing_path = "pipeline/logician/gates/f_cards_schema_invalid.py"

    def fake_exists(p: str) -> bool:
        return p != missing_path

    missing_modules, missing_tests = check_module_coverage(file_exists=fake_exists)
    assert missing_path in missing_modules


def test_evaluate_returns_pass_when_complete():
    """Module-coverage-only evaluation when no card specified."""
    from pipeline.logician.gates.f_cards_coverage_incomplete import evaluate

    outcome = evaluate(
        environment="production",
        file_exists=lambda p: True,
    )
    assert outcome.passed is True
    assert outcome.mode == "WARN"
    assert outcome.missing_modules == ()


def test_evaluate_fails_when_module_missing():
    """Missing module → FAIL regardless of environment."""
    from pipeline.logician.gates.f_cards_coverage_incomplete import evaluate

    outcome = evaluate(
        environment="development",   # even dev mode FAILS on missing module
        file_exists=lambda p: False,
    )
    assert outcome.passed is False
    assert outcome.mode == "FAIL"
    assert len(outcome.missing_modules) > 0


def test_evaluate_pass_when_no_seat_depends_on_missing_field():
    """At v0.1 Beta LOCK seat_dependencies are empty → no field gap triggers FAIL."""
    from pipeline.logician.gates.f_cards_coverage_incomplete import evaluate

    outcome = evaluate(
        environment="production",
        file_exists=lambda p: True,
        loaded_card_axis="CIC",
        loaded_card_fields_present=frozenset({"slug", "card_id"}),  # minimal field set
    )
    # No seat depends on any field at v0.1 Beta → PASS even with sparse fields.
    assert outcome.passed is True
