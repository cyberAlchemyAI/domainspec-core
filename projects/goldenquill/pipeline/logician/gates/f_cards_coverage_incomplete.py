"""F-CARDS-COVERAGE-INCOMPLETE — META PRE-cycle gate (LIVE at v7.0.11 LOCK).

Per architecture v7.0.11 §1.6 #1 + blueprint §4 v2.x card-hardening §4.X.1.1.

Mode-sensitive behavior:
  - Development mode: WARN on any missing required card field; never FAIL.
  - Production mode + missing field's seat dependency declared in seat_dependencies:
    FAIL CLOSED.
  - Production mode + missing field is nonessential or forward-compat: WARN.

This is the dormant-binding lever for the F-CARDS-* family. Mirrors
F-CLASS-COVERAGE-INCOMPLETE (v7.0.7 §5.1) + F-PACKET-COVERAGE-INCOMPLETE
(§16 v1 row-222) + F-REPORT-COVERAGE-INCOMPLETE (§4 v2.x.3) for the
coverage-completeness aspect; adds WARN/FAIL bifurcation unique to the
card case.

LIVE at v7.0.11 LOCK — the META gate is the load-bearing primitive that
makes the rest of the F-CARDS-* family enforceable.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Literal, Mapping, Sequence

from pipeline.cards.seat_dependencies import (
    SEAT_CARD_FIELD_DEPENDENCIES,
    seats_depending_on,
)


GATE_ID: Final[str] = "F-CARDS-COVERAGE-INCOMPLETE"
PRE_GATE_ORDER: Final[float] = 7.2  # after F-CLASS-COVERAGE-INCOMPLETE (7.1)


# Required module + test paths the META gate verifies exist on-disk.
REQUIRED_F_CARDS_MODULES: Final[tuple[str, ...]] = (
    "pipeline/logician/gates/f_cards_coverage_incomplete.py",
    "pipeline/logician/gates/f_cards_schema_invalid.py",
    "pipeline/logician/gates/f_cards_unsigned_production_load.py",
    "pipeline/logician/gates/f_cards_signature_invalid.py",
    "pipeline/logician/gates/f_cards_private_data_in_card.py",
    "pipeline/logician/gates/f_cards_cross_org_namespace_leak.py",
    "pipeline/logician/gates/f_cards_coupling_violation_extension.py",
    "pipeline/logician/gates/f_cards_malformed_lifecycle.py",
    "pipeline/logician/gates/f_cards_load_in_wrong_namespace.py",
    "pipeline/logician/gates/f_cic_clc_pattern_read_during_eligibility.py",
)

REQUIRED_F_CARDS_TEST_PATHS: Final[tuple[str, ...]] = (
    "tests/logician/gates/test_f_cards_coverage_incomplete.py",
    "tests/logician/gates/test_f_cards_schema_invalid.py",
    "tests/logician/gates/test_f_cards_unsigned_production_load.py",
    "tests/logician/gates/test_f_cards_signature_invalid.py",
    "tests/logician/gates/test_f_cards_private_data_in_card.py",
    "tests/logician/gates/test_f_cards_cross_org_namespace_leak.py",
    "tests/logician/gates/test_f_cards_coupling_violation_extension.py",
    "tests/logician/gates/test_f_cards_malformed_lifecycle.py",
    "tests/logician/gates/test_f_cards_load_in_wrong_namespace.py",
    "tests/logician/gates/test_f_cic_clc_pattern_read_during_eligibility.py",
)


@dataclass(frozen=True, kw_only=True)
class CoverageGateOutcome:
    """META gate outcome — separates module-coverage check from card-field-coverage check."""
    passed: bool
    mode: Literal["WARN", "FAIL"]
    missing_modules: tuple[str, ...]
    missing_tests: tuple[str, ...]
    card_field_gaps: tuple[str, ...]   # field_paths missing from a card that a registered seat depends on
    message: str


def check_module_coverage(
    *,
    file_exists: callable,
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """Verify every required F-CARDS-* module + test file exists on-disk.
    Returns (missing_modules, missing_tests).
    """
    missing_modules = tuple(p for p in REQUIRED_F_CARDS_MODULES if not file_exists(p))
    missing_tests = tuple(p for p in REQUIRED_F_CARDS_TEST_PATHS if not file_exists(p))
    return (missing_modules, missing_tests)


def check_card_field_coverage(
    *,
    loaded_card_axis: Literal["CIC", "CLC", "MATRIX"],
    loaded_card_fields_present: frozenset[str],
) -> tuple[str, ...]:
    """For a loaded card, check that every field path any registered
    consumer seat depends on is present in the card body.
    Returns the tuple of missing field paths (gaps).

    At v0.1 Beta LOCK every seat declares an empty dependency set, so this
    function returns () unconditionally. At v0.2 first wave when seats begin
    declaring their card reads, this function starts returning real gaps.
    """

    required_paths = set()
    for seat_deps in SEAT_CARD_FIELD_DEPENDENCIES.values():
        required_paths.update(seat_deps.get(loaded_card_axis, frozenset()))

    return tuple(sorted(required_paths - loaded_card_fields_present))


def evaluate(
    *,
    environment: Literal["development", "production"],
    file_exists: callable,
    loaded_card_axis: Literal["CIC", "CLC", "MATRIX"] | None = None,
    loaded_card_fields_present: frozenset[str] | None = None,
) -> CoverageGateOutcome:
    """Run the META gate.

    Mode-sensitive resolution per architecture v7.0.11 §1.6 #1 + §7.3:
      - Missing modules / missing tests → always FAIL (regardless of environment).
      - Missing card-field-dependency in production + seat depends on it → FAIL.
      - Missing card-field-dependency in development → WARN.
      - Missing card-field that no seat depends on → WARN (forward-compat).
    """

    missing_modules, missing_tests = check_module_coverage(file_exists=file_exists)

    if missing_modules or missing_tests:
        return CoverageGateOutcome(
            passed=False,
            mode="FAIL",
            missing_modules=missing_modules,
            missing_tests=missing_tests,
            card_field_gaps=(),
            message=(
                f"F-CARDS-COVERAGE-INCOMPLETE: missing modules={missing_modules!r}, "
                f"missing tests={missing_tests!r}. Beta deployment blocked until "
                f"every required F-CARDS-* module + test exists on-disk."
            ),
        )

    if loaded_card_axis is None or loaded_card_fields_present is None:
        # Module-coverage check only — card-field check skipped.
        return CoverageGateOutcome(
            passed=True,
            mode="WARN",
            missing_modules=(),
            missing_tests=(),
            card_field_gaps=(),
            message="F-CARDS-COVERAGE-INCOMPLETE: module coverage check passed.",
        )

    field_gaps = check_card_field_coverage(
        loaded_card_axis=loaded_card_axis,
        loaded_card_fields_present=loaded_card_fields_present,
    )

    if not field_gaps:
        return CoverageGateOutcome(
            passed=True,
            mode="WARN",
            missing_modules=(),
            missing_tests=(),
            card_field_gaps=(),
            message="F-CARDS-COVERAGE-INCOMPLETE: all coverage checks passed.",
        )

    # Determine if ANY field gap has a seat-dependency in production.
    if environment == "production":
        gaps_with_seat_deps = [
            p for p in field_gaps
            if seats_depending_on(axis=loaded_card_axis, field_path=p)
        ]
        if gaps_with_seat_deps:
            return CoverageGateOutcome(
                passed=False,
                mode="FAIL",
                missing_modules=(),
                missing_tests=(),
                card_field_gaps=field_gaps,
                message=(
                    f"F-CARDS-COVERAGE-INCOMPLETE: card field gaps with seat "
                    f"dependencies in production={gaps_with_seat_deps!r}. Production "
                    f"deployment blocked until card content lands or seat-deps "
                    f"registry is updated."
                ),
            )

    # Development environment OR production with no seat-dep-impacting gaps → WARN.
    return CoverageGateOutcome(
        passed=True,
        mode="WARN",
        missing_modules=(),
        missing_tests=(),
        card_field_gaps=field_gaps,
        message=(
            f"F-CARDS-COVERAGE-INCOMPLETE: card field gaps "
            f"(WARN, not blocking)={field_gaps!r}."
        ),
    )
