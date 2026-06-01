"""Card lifecycle truth tests.

These tests lock the trust-boundary rule: active runtime cards must be signed,
content-hashed, and registry-declared; draft cards are research artifacts and
must not pass the loader preflight.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from pipeline.cards.loader import (
    CardCouplingError,
    CardLifecycleError,
    canonical_bytes_sha256,
    enforce_lifecycle_truth,
    load_card,
    validate_card_schema_shape,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
CARD_PATHS = tuple(sorted(
    list((REPO_ROOT / "pipeline" / "cards" / "CIC").glob("*.yaml"))
    + list((REPO_ROOT / "pipeline" / "cards" / "CLC").glob("*.yaml"))
))


def _load(path: Path) -> dict:
    with path.open() as f:
        return yaml.safe_load(f)


def test_all_14_runtime_cards_have_signed_lifecycle_truth():
    assert len(CARD_PATHS) == 14
    for path in CARD_PATHS:
        doc = _load(path)
        validate_card_schema_shape(card_path=str(path), card_body=doc)
        enforce_lifecycle_truth(card_path=str(path), card_body=doc)
        lifecycle = doc["lifecycle"]
        assert lifecycle["draft_status"] == "signed"
        assert lifecycle["runtime_loadable"] is True
        assert lifecycle["signature_status"] == "signed"
        assert lifecycle["runtime_load_status"] == "loaded"
        assert lifecycle["signed_at"]
        assert lifecycle["signed_by"] == "founder"
        assert lifecycle["content_hash"] == f"sha256:{canonical_bytes_sha256(card_body=doc)}"


def test_no_runtime_card_has_forbidden_cic_clc_coupling_keys():
    forbidden_by_axis = {
        "CIC": {
            "common_clc_patterns_observed",
            "eligible_clc_subset",
            "clc_allowlist",
            "clc_denylist",
            "preferred_clcs",
            "clc_win_rate",
            "clc_ranking_preferences",
        },
        "CLC": {
            "eligible_cic_subset",
            "cic_allowlist",
            "cic_denylist",
            "preferred_cics",
            "cic_win_rate",
            "cic_ranking_preferences",
        },
    }
    for path in CARD_PATHS:
        doc = _load(path)
        assert not (set(doc) & forbidden_by_axis[doc["card_axis"]]), path


def test_active_card_registry_declares_only_signed_runtime_loadable_cards():
    registry_path = REPO_ROOT / "pipeline" / "cards" / "registry.yaml"
    registry = _load(registry_path)
    entries = registry["active_cards"]
    assert registry["registry_kind"] == "active_card_registry"
    assert len(entries) == 14
    assert {REPO_ROOT / e["card_path"] for e in entries} == set(CARD_PATHS)

    for entry in entries:
        assert entry["active"] is True
        assert entry["required_draft_status"] == "signed"
        assert entry["required_runtime_loadable"] is True
        doc = _load(REPO_ROOT / entry["card_path"])
        assert doc["card_axis"] == entry["card_axis"]
        assert doc["card_id"] == entry["card_id"]
        assert doc["slug"] == entry["slug"]
        assert doc["lifecycle"]["draft_status"] == "signed"
        assert doc["lifecycle"]["runtime_loadable"] is True


def test_loader_refuses_draft_card_even_when_other_statuses_claim_signed(tmp_path: Path):
    doc = _load(REPO_ROOT / "pipeline" / "cards" / "CIC" / "food_systems.yaml")
    doc["lifecycle"]["draft_status"] = "draft"
    draft_path = tmp_path / "draft_card.yaml"
    draft_path.write_text(yaml.safe_dump(doc, sort_keys=False))

    with pytest.raises(CardLifecycleError, match="Loader refuses draft cards"):
        load_card(path=str(draft_path), environment="production")


def test_loader_refuses_runtime_loadable_non_signed_card(tmp_path: Path):
    doc = _load(REPO_ROOT / "pipeline" / "cards" / "CIC" / "food_systems.yaml")
    doc["lifecycle"]["draft_status"] = "review_passed"
    doc["lifecycle"]["runtime_loadable"] = True
    bad_path = tmp_path / "review_passed_runtime_card.yaml"
    bad_path.write_text(yaml.safe_dump(doc, sort_keys=False))

    with pytest.raises(CardLifecycleError, match="runtime_loadable must be false"):
        load_card(path=str(bad_path), environment="production")


def test_loader_refuses_forbidden_cic_to_clc_coupling_key(tmp_path: Path):
    doc = _load(REPO_ROOT / "pipeline" / "cards" / "CIC" / "food_systems.yaml")
    # Recompute content hash after adding a forbidden key so the failure proves
    # coupling enforcement, not lifecycle-hash enforcement.
    doc["common_clc_patterns_observed"] = []
    doc["lifecycle"]["content_hash"] = f"sha256:{canonical_bytes_sha256(card_body=doc)}"
    bad_path = tmp_path / "coupled_cic.yaml"
    bad_path.write_text(yaml.safe_dump(doc, sort_keys=False))

    with pytest.raises(CardCouplingError, match="common_clc_patterns_observed"):
        load_card(path=str(bad_path), environment="production")


def test_valid_runtime_card_passes_preflight_then_stops_at_v02_boundary():
    with pytest.raises(NotImplementedError, match="runtime registration graduates"):
        load_card(
            path=str(REPO_ROOT / "pipeline" / "cards" / "CIC" / "food_systems.yaml"),
            environment="production",
        )
