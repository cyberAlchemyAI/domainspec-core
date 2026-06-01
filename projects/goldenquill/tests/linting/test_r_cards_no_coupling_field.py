"""Tests for R-CARDS-NO-COUPLING-FIELD AST-lint rule.

LIVE at v7.0.11 LOCK — independent of runtime gate body NotImplementedError state.
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path

import pytest
import yaml


REPO_ROOT = Path(__file__).resolve().parents[2]


def test_rule_imports_cleanly():
    from pipeline.linting import r_cards_no_coupling_field  # noqa: F401


def test_rule_id():
    from pipeline.linting.r_cards_no_coupling_field import RULE_ID
    assert RULE_ID == "R-CARDS-NO-COUPLING-FIELD"


def test_scan_clean_fixture_returns_no_findings(tmp_path):
    """Authoring a clean CIC YAML in a tmp tree should produce zero findings."""
    from pipeline.linting.r_cards_no_coupling_field import scan_card_file

    clean_cic = {
        "schema_version": "1.0-cic",
        "card_axis": "CIC",
        "card_id": "TILTH-CIC-01",
        "slug": "food_systems",
        "display_name": "Food Systems",
        "coverage_axis": "Production",
        "tilth_cic_id": "TILTH-CIC-01",
        "search_vocabulary": {"core_terms": [{"term": "farms"}]},
        "register_defaults": {},
        "reporting_cadence_typical": {},
        "admin_risk_term_register": [],
        "evidence_signals": [],
        "kfr_fact_classes": [],
        "lifecycle": {
            "draft_status": "draft",
            "review_status": "pending",
            "cross_family_thesis_status": "pending",
            "signature_status": "unsigned",
            "runtime_load_status": "not_loaded",
        },
        "_research_metadata": {
            "authored_at": "2026-05-15T00:00:00Z",
            "authored_by_role": "platform_team",
        },
    }
    test_file = tmp_path / "clean_cic.yaml"
    with test_file.open("w") as f:
        yaml.safe_dump(clean_cic, f)

    findings = scan_card_file(file_path=str(test_file), card_axis="CIC")
    assert findings == ()


def test_scan_dirty_cic_detects_forbidden_field(tmp_path):
    """Authoring a CIC with common_clc_patterns_observed should produce a finding."""
    from pipeline.linting.r_cards_no_coupling_field import scan_card_file

    dirty_cic = {
        "schema_version": "1.0-cic",
        "card_axis": "CIC",
        "slug": "food_systems",
        "common_clc_patterns_observed": [   # forbidden!
            {"clc_slug": "operating_capacity", "frequency": "FREQUENT"},
        ],
    }
    test_file = tmp_path / "dirty_cic.yaml"
    with test_file.open("w") as f:
        yaml.safe_dump(dirty_cic, f)

    findings = scan_card_file(file_path=str(test_file), card_axis="CIC")
    assert len(findings) == 1
    assert findings[0].forbidden_field == "common_clc_patterns_observed"
    assert findings[0].severity == "FAIL"


def test_scan_dirty_clc_detects_eligible_cic_subset(tmp_path):
    """Authoring a CLC with eligible_cic_subset should produce a finding."""
    from pipeline.linting.r_cards_no_coupling_field import scan_card_file

    dirty_clc = {
        "schema_version": "1.0-clc",
        "card_axis": "CLC",
        "slug": "operating_capacity",
        "eligible_cic_subset": ["cooperative", "ecosystem_intermediary"],  # forbidden!
    }
    test_file = tmp_path / "dirty_clc.yaml"
    with test_file.open("w") as f:
        yaml.safe_dump(dirty_clc, f)

    findings = scan_card_file(file_path=str(test_file), card_axis="CLC")
    assert len(findings) == 1
    assert findings[0].forbidden_field == "eligible_cic_subset"


def test_scan_actual_fixture_stubs_are_clean():
    """The fixture stubs at pipeline/cards/CIC/food_systems.yaml and
    pipeline/cards/CLC/operating_capacity.yaml MUST be clean."""
    from pipeline.linting.r_cards_no_coupling_field import scan_card_file

    f1 = REPO_ROOT / "pipeline" / "cards" / "CIC" / "food_systems.yaml"
    findings = scan_card_file(file_path=str(f1), card_axis="CIC")
    assert findings == (), f"food_systems.yaml has forbidden fields: {findings}"

    f2 = REPO_ROOT / "pipeline" / "cards" / "CLC" / "operating_capacity.yaml"
    findings = scan_card_file(file_path=str(f2), card_axis="CLC")
    assert findings == (), f"operating_capacity.yaml has forbidden fields: {findings}"
