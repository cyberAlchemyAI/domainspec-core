"""Tests for pipeline.cards.models + JSON schema parse-ability + fixture-stub round trip.

Skeleton suite at v7.0.11 LOCK candidate. Bodies graduate alongside loader at v0.2
first wave.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml


REPO_ROOT = Path(__file__).resolve().parents[2]


# --- JSON schema parse-ability ----------------------------------------------

def test_cic_schema_is_valid_json():
    p = REPO_ROOT / "pipeline" / "cards" / "_schema" / "card_cic.schema.json"
    with p.open() as f:
        schema = json.load(f)
    assert schema["title"].startswith("Card — CIC")
    assert schema["properties"]["slug"]["enum"] == [
        "food_systems", "educator", "public_agency",
        "arts_culture", "cooperative", "ecosystem_intermediary",
    ]
    # The schema MUST forbid common_clc_patterns_observed at the structural level.
    forbidden_field_names = [
        c["required"][0] for c in schema["not"]["anyOf"]
    ]
    assert "common_clc_patterns_observed" in forbidden_field_names
    assert "eligible_clc_subset" in forbidden_field_names
    lifecycle = schema["properties"]["lifecycle"]
    assert lifecycle["properties"]["draft_status"]["enum"] == [
        "draft", "review_passed", "signed", "deprecated",
    ]
    assert "runtime_loadable" in lifecycle["required"]
    assert "signed_at" in lifecycle["properties"]
    assert "signed_by" in lifecycle["properties"]
    assert "content_hash" in lifecycle["properties"]


def test_clc_schema_is_valid_json():
    p = REPO_ROOT / "pipeline" / "cards" / "_schema" / "card_clc.schema.json"
    with p.open() as f:
        schema = json.load(f)
    assert schema["title"].startswith("Card — CLC")
    assert schema["properties"]["slug"]["enum"] == [
        "public_purpose_works", "catalytic_change", "operating_capacity",
        "research_evidence", "market_access", "credit_underwriting",
        "sponsorship_corporate", "shared_assets",
    ]
    forbidden_field_names = [
        c["required"][0] for c in schema["not"]["anyOf"]
    ]
    assert "eligible_cic_subset" in forbidden_field_names
    lifecycle = schema["properties"]["lifecycle"]
    assert lifecycle["properties"]["draft_status"]["enum"] == [
        "draft", "review_passed", "signed", "deprecated",
    ]
    assert "runtime_loadable" in lifecycle["required"]


def test_matrix_schema_is_valid_json():
    p = REPO_ROOT / "pipeline" / "cards" / "matrix" / "_schema" / "card_matrix.schema.json"
    with p.open() as f:
        schema = json.load(f)
    assert schema["title"].startswith("Card — CIC × CLC Matrix")
    # status MUST be FORWARD_COMPAT_ONLY at v7.0.11 LOCK.
    assert schema["properties"]["status"]["const"] == "FORWARD_COMPAT_ONLY"
    # binding_eligibility MUST be false (const).
    assert schema["properties"]["binding_eligibility"]["const"] is False


# --- Fixture-stub round trip -------------------------------------------------

def test_food_systems_cic_fixture_loads_and_has_required_fields():
    p = REPO_ROOT / "pipeline" / "cards" / "CIC" / "food_systems.yaml"
    with p.open() as f:
        doc = yaml.safe_load(f)
    assert doc["schema_version"] == "1.0-cic"
    assert doc["card_axis"] == "CIC"
    assert doc["slug"] == "food_systems"
    assert doc["card_id"] == "TILTH-CIC-01"
    assert "common_clc_patterns_observed" not in doc, (
        "F-CARDS-COUPLING-VIOLATION-EXTENSION precondition: the field must be absent"
    )


def test_operating_capacity_clc_fixture_loads_and_has_required_fields():
    p = REPO_ROOT / "pipeline" / "cards" / "CLC" / "operating_capacity.yaml"
    with p.open() as f:
        doc = yaml.safe_load(f)
    assert doc["schema_version"] == "1.0-clc"
    assert doc["card_axis"] == "CLC"
    assert doc["slug"] == "operating_capacity"
    assert doc["card_id"] == "TILTH-CLC-03"
    # F-CARDS-COUPLING-VIOLATION-EXTENSION preconditions:
    assert "eligible_cic_subset" not in doc
    assert "preferred_cics" not in doc


# --- Pydantic model surfaces -------------------------------------------------

def test_models_module_imports_cleanly():
    from pipeline.cards import models  # noqa: F401
    assert hasattr(models, "CICCard")
    assert hasattr(models, "CLCCard")
    assert hasattr(models, "MatrixCard")
    assert hasattr(models, "LoadedCard")
    assert hasattr(models, "Lifecycle")
    assert hasattr(models, "ResearchMetadata")


def test_canonical_slug_enumerations_match_schema():
    from pipeline.cards.models import CIC_SLUGS, CLC_SLUGS
    assert CIC_SLUGS == frozenset({
        "food_systems", "educator", "public_agency",
        "arts_culture", "cooperative", "ecosystem_intermediary",
    })
    assert CLC_SLUGS == frozenset({
        "public_purpose_works", "catalytic_change", "operating_capacity",
        "research_evidence", "market_access", "credit_underwriting",
        "sponsorship_corporate", "shared_assets",
    })


# --- Loader signatures (NotImplementedError at v0.1 Beta LOCK) ---------------

def test_loader_raises_notimplementederror_at_v01_beta():
    from pipeline.cards.loader import load_card
    with pytest.raises(NotImplementedError):
        load_card(
            path="pipeline/cards/CIC/food_systems.yaml",
            environment="development",
        )


def test_resolve_namespace_lands_live_at_lock():
    """resolve_card_namespace is LIVE at v7.0.11 LOCK (not deferred to v0.2)
    because it's a pure-string-function used by tests + tooling immediately."""
    from pipeline.cards.loader import resolve_card_namespace
    assert resolve_card_namespace(card_axis="CIC", slug="food_systems") == "cards:cic:food_systems"
    assert resolve_card_namespace(card_axis="CLC", slug="operating_capacity") == "cards:clc:operating_capacity"
    assert resolve_card_namespace(card_axis="MATRIX", intersection_id="food_systems__market_access") == "cards:matrix:food_systems__market_access"


# --- Display name resolution per arch v7.0.11 §7.2 ---------------------------

def test_display_name_short_resolution_for_cic_06():
    """CIC-06's slash-form display_name + short companion. Arch v7.0.11 §7.2."""
    # Build a minimal CIC card in-memory; test the resolver function shape.
    # Full integration test lands at v0.2 first wave when actual cards load.
    from pipeline.cards.loader import display_name_for_consumer  # noqa: F401
