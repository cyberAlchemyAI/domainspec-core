"""Tests for pipeline.cards.seat_dependencies — per-seat card-field dependency registry.

Per architecture v7.0.11 §7.3 (resolved 2026-05-15 PM). Static declarations at
loader step 8 drive F-CARDS-COVERAGE-INCOMPLETE introspection.
"""

from __future__ import annotations

import pytest
from types import MappingProxyType


def test_registry_imports_and_is_immutable():
    from pipeline.cards.seat_dependencies import (
        SEAT_CARD_FIELD_DEPENDENCIES,
        SEAT_NAMES,
    )
    # Top-level must be MappingProxyType per §4 v2.x.1 row-198 RT-14 fold-in.
    assert isinstance(SEAT_CARD_FIELD_DEPENDENCIES, MappingProxyType)


def test_every_declared_seat_appears_in_seat_names():
    from pipeline.cards.seat_dependencies import (
        SEAT_CARD_FIELD_DEPENDENCIES,
        SEAT_NAMES,
    )
    declared = set(SEAT_CARD_FIELD_DEPENDENCIES.keys())
    assert declared <= SEAT_NAMES, f"Undeclared seats: {declared - SEAT_NAMES}"
    assert declared == SEAT_NAMES, f"Missing seats: {SEAT_NAMES - declared}"


def test_each_seat_declares_cic_and_clc_axes():
    from pipeline.cards.seat_dependencies import SEAT_CARD_FIELD_DEPENDENCIES
    for seat, axes in SEAT_CARD_FIELD_DEPENDENCIES.items():
        assert "CIC" in axes, f"{seat} missing CIC axis"
        assert "CLC" in axes, f"{seat} missing CLC axis"


def test_v01_beta_lock_empty_dependencies():
    """At v0.1 Beta LOCK every seat declares empty dependency set —
    documents that no seat consumes card content at v0.1 Beta.
    Populates at v0.2 first wave alongside Phase B runtime context injection.
    """
    from pipeline.cards.seat_dependencies import SEAT_CARD_FIELD_DEPENDENCIES
    for seat, axes in SEAT_CARD_FIELD_DEPENDENCIES.items():
        for axis, deps in axes.items():
            assert deps == frozenset(), (
                f"{seat}.{axis} expected empty at v0.1 Beta LOCK, got {deps!r}. "
                f"Populating this at v0.1 Beta would imply a seat consumes "
                f"card content before Phase B runtime context injection lands."
            )


def test_all_declared_field_paths_helper():
    from pipeline.cards.seat_dependencies import all_declared_field_paths
    assert all_declared_field_paths(axis="CIC") == frozenset()
    assert all_declared_field_paths(axis="CLC") == frozenset()


def test_seats_depending_on_helper_with_empty_registry():
    from pipeline.cards.seat_dependencies import seats_depending_on
    # No seat declares any field at v0.1 Beta — every lookup returns empty.
    assert seats_depending_on(axis="CIC", field_path="search_vocabulary.core_terms") == frozenset()
    assert seats_depending_on(axis="CLC", field_path="underwriting_criteria") == frozenset()
