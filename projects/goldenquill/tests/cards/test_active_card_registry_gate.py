"""F-CARDS-NOT-IN-ACTIVE-MANIFEST gate tests + registry-contract locks.

These tests cover the manifest-membership half of the trust boundary. They split
into two clusters:

1. Registry-contract locks (LIVE). Assert that `pipeline/cards/registry.yaml`
   is well-formed, structurally exhaustive over the on-disk CIC/CLC card
   inventory, and free of orphan entries in either direction. These tests pass
   today and lock the registry artifact PR #15 landed.

2. Loader-gate enforcement tests (XFAIL until Phase 1 P1-2 lands). Assert the
   loader fails closed with F-CARDS-NOT-IN-ACTIVE-MANIFEST when a production
   load is attempted on a card whose card_id is not declared in registry.yaml.
   These tests are marked `xfail(strict=True)` because the loader gate is not
   yet wired — the loader has no manifest-membership check. When P1-2 lands
   the gate, the XFails flip to passes automatically and signal the gate is
   live. If the gate ever regresses, the strict-XFail flip back to xpass
   triggers a CI failure.

Path-policy note 2026-05-17: The Embedding Plan §A.2 P1-1 specifies the
manifest at `pipeline/cards/_manifest/active_cards.yaml`. The artifact PR #15
landed lives at `pipeline/cards/registry.yaml` (different path, same
semantics — `registry_kind: active_card_registry`, 14-entry coverage,
content_hash + draft_status + runtime_loadable per entry's required_* fields).
These tests treat `registry.yaml` as the canonical artifact. If the operator
canonicalizes the spec-path instead, change REGISTRY_PATH below and any P1-2
loader gate.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from pipeline.cards.loader import (
    CardLoaderError,
    CardManifestMembershipError,
    canonical_bytes_sha256,
    load_card,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = REPO_ROOT / "pipeline" / "cards" / "registry.yaml"
CIC_DIR = REPO_ROOT / "pipeline" / "cards" / "CIC"
CLC_DIR = REPO_ROOT / "pipeline" / "cards" / "CLC"

CARD_PATHS = tuple(sorted(
    list(CIC_DIR.glob("*.yaml")) + list(CLC_DIR.glob("*.yaml"))
))


def _load(path: Path) -> dict:
    with path.open() as f:
        return yaml.safe_load(f)


def _registry() -> dict:
    return _load(REGISTRY_PATH)


# ─────────────────────────────────────────────────────────────────────────────
# Cluster 1 — Registry-contract locks (LIVE)
# ─────────────────────────────────────────────────────────────────────────────


def test_registry_file_exists_and_loads():
    """The active-card registry MUST exist and parse as a YAML mapping."""

    assert REGISTRY_PATH.exists(), (
        f"Registry artifact missing at {REGISTRY_PATH}. PR #15 was expected to "
        "land this file; if it didn't, Phase 1 P1-1 is still open."
    )
    doc = _registry()
    assert isinstance(doc, dict), "registry.yaml root must be a mapping"
    assert doc.get("registry_kind") == "active_card_registry"
    assert doc.get("schema_version") == "1.0-card-registry"


def test_registry_declares_truth_invariant_field():
    """Registry MUST self-document its truth invariant for downstream consumers."""

    doc = _registry()
    invariant = doc.get("truth_invariant")
    assert isinstance(invariant, str) and invariant.strip(), (
        "registry.yaml must carry a non-empty truth_invariant string explaining "
        "the active-cards-only semantics."
    )


def test_registry_entry_set_is_exhaustive_over_card_directories():
    """Every on-disk signed card MUST appear in the registry and vice versa.

    Catches both directions of drift: (a) a new card YAML added without
    registry update; (b) a stale registry entry referencing a removed card.
    """

    doc = _registry()
    entries = doc["active_cards"]
    assert isinstance(entries, list)
    assert len(entries) == 14, "Expected 14 active cards (6 CIC + 8 CLC)"

    registry_paths = {(REPO_ROOT / e["card_path"]).resolve() for e in entries}
    disk_paths = {p.resolve() for p in CARD_PATHS}
    assert registry_paths == disk_paths, (
        f"Registry vs. disk drift detected.\n"
        f"Only in registry: {registry_paths - disk_paths}\n"
        f"Only on disk: {disk_paths - registry_paths}"
    )


def test_registry_card_ids_are_unique():
    """No registry entry may share a card_id with another."""

    doc = _registry()
    ids = [e["card_id"] for e in doc["active_cards"]]
    assert len(ids) == len(set(ids)), f"Duplicate card_id in registry: {ids}"


def test_registry_slugs_are_unique():
    """No registry entry may share a slug with another."""

    doc = _registry()
    slugs = [e["slug"] for e in doc["active_cards"]]
    assert len(slugs) == len(set(slugs)), f"Duplicate slug in registry: {slugs}"


def test_registry_entry_metadata_matches_card_body():
    """Every registry entry's card_axis/card_id/slug MUST match the YAML it points at."""

    doc = _registry()
    for entry in doc["active_cards"]:
        card_path = REPO_ROOT / entry["card_path"]
        card_body = _load(card_path)
        assert card_body["card_axis"] == entry["card_axis"], entry["card_path"]
        assert card_body["card_id"] == entry["card_id"], entry["card_path"]
        assert card_body["slug"] == entry["slug"], entry["card_path"]


def test_registry_requires_signed_runtime_loadable_for_every_entry():
    """Every active-card entry MUST require draft_status=signed + runtime_loadable=true."""

    doc = _registry()
    for entry in doc["active_cards"]:
        assert entry["active"] is True, entry
        assert entry["required_draft_status"] == "signed", entry
        assert entry["required_runtime_loadable"] is True, entry


def test_registry_namespace_matches_axis_slug_convention():
    """namespace MUST follow `cards:<axis>:<slug>` per loader.resolve_card_namespace()."""

    doc = _registry()
    for entry in doc["active_cards"]:
        axis_lower = entry["card_axis"].lower()
        expected = f"cards:{axis_lower}:{entry['slug']}"
        assert entry["namespace"] == expected, entry


# ─────────────────────────────────────────────────────────────────────────────
# Cluster 2 — Loader F-CARDS-NOT-IN-ACTIVE-MANIFEST gate (LIVE per P1-2)
# ─────────────────────────────────────────────────────────────────────────────


def test_loader_rejects_card_with_card_id_not_in_registry(tmp_path: Path):
    """Production load of a card whose card_id is not in registry MUST fail closed."""

    doc = _load(CIC_DIR / "food_systems.yaml")
    # Mutate card_id to a value the registry does not declare. Keep everything
    # else valid (slug stays in CIC_SLUGS, lifecycle stays signed) and
    # re-derive content_hash so lifecycle truth still verifies — the only
    # remaining failure surface is the manifest-membership gate.
    doc["card_id"] = "TILTH-CIC-99"
    doc["tilth_cic_id"] = "TILTH-CIC-99"
    doc["lifecycle"]["content_hash"] = f"sha256:{canonical_bytes_sha256(card_body=doc)}"
    rogue_path = tmp_path / "rogue_card.yaml"
    rogue_path.write_text(yaml.safe_dump(doc, sort_keys=False))

    with pytest.raises(CardManifestMembershipError, match="F-CARDS-NOT-IN-ACTIVE-MANIFEST"):
        load_card(path=str(rogue_path), environment="production")


def test_loader_rejects_card_at_path_not_in_registry(tmp_path: Path):
    """Production load of a card by path not declared in registry MUST fail closed.

    Even if card_id happens to match a registered entry, loading from an
    unregistered path is a manifest-membership violation per the spec semantics.
    """

    src = CIC_DIR / "food_systems.yaml"
    rogue_path = tmp_path / "food_systems_relocated.yaml"
    rogue_path.write_bytes(src.read_bytes())

    with pytest.raises(CardManifestMembershipError, match="F-CARDS-NOT-IN-ACTIVE-MANIFEST"):
        load_card(path=str(rogue_path), environment="production")


def test_development_environment_skips_manifest_gate(tmp_path: Path):
    """Development-environment load MUST permit cards-not-in-manifest.

    The manifest gate is production-only. Dev loads should bypass the gate
    and reach the v0.2 NotImplementedError boundary even when the card_id is
    unknown to the manifest.
    """

    doc = _load(CIC_DIR / "food_systems.yaml")
    doc["card_id"] = "TILTH-CIC-99"
    doc["tilth_cic_id"] = "TILTH-CIC-99"
    doc["lifecycle"]["content_hash"] = f"sha256:{canonical_bytes_sha256(card_body=doc)}"
    rogue_path = tmp_path / "rogue_dev_card.yaml"
    rogue_path.write_text(yaml.safe_dump(doc, sort_keys=False))

    with pytest.raises(NotImplementedError, match="runtime registration graduates"):
        load_card(path=str(rogue_path), environment="development")


def test_production_load_of_registered_card_passes_gate_and_reaches_v02_boundary():
    """Positive path: a real registered card under production loads cleanly
    through the manifest gate and stops at the v0.2 NotImplementedError boundary."""

    with pytest.raises(NotImplementedError, match="runtime registration graduates"):
        load_card(
            path=str(CIC_DIR / "food_systems.yaml"),
            environment="production",
        )


def test_loader_accepts_explicit_manifest_path_override(tmp_path: Path):
    """The manifest_path override MUST be respected so tests and future
    deployments can supply a non-default manifest without patching internals.

    Construct a one-entry manifest that includes only the test card; pass it
    via manifest_path and confirm the load reaches the v0.2 boundary.
    """

    src = CIC_DIR / "food_systems.yaml"
    overlay_manifest_path = tmp_path / "registry_override.yaml"
    overlay_manifest_path.write_text(yaml.safe_dump({
        "registry_kind": "active_card_registry",
        "schema_version": "1.0-card-registry",
        "truth_invariant": "test-override",
        "active_cards": [{
            "namespace": "cards:cic:food_systems",
            "card_path": str(src.resolve()),
            "card_axis": "CIC",
            "card_id": "TILTH-CIC-01",
            "slug": "food_systems",
            "active": True,
            "required_draft_status": "signed",
            "required_runtime_loadable": True,
        }],
    }, sort_keys=False))

    with pytest.raises(NotImplementedError, match="runtime registration graduates"):
        load_card(
            path=str(src),
            environment="production",
            manifest_path=str(overlay_manifest_path),
        )


def test_loader_rejects_when_explicit_manifest_omits_card(tmp_path: Path):
    """Override-manifest scenario, negative path: a manifest that omits the
    loaded card MUST fail closed even if the card is fine in every other way."""

    src = CIC_DIR / "food_systems.yaml"
    overlay_manifest_path = tmp_path / "registry_empty.yaml"
    overlay_manifest_path.write_text(yaml.safe_dump({
        "registry_kind": "active_card_registry",
        "schema_version": "1.0-card-registry",
        "truth_invariant": "test-empty",
        "active_cards": [{
            "namespace": "cards:cic:educator",
            "card_path": "pipeline/cards/CIC/educator.yaml",
            "card_axis": "CIC",
            "card_id": "TILTH-CIC-02",
            "slug": "educator",
            "active": True,
            "required_draft_status": "signed",
            "required_runtime_loadable": True,
        }],
    }, sort_keys=False))

    with pytest.raises(CardManifestMembershipError, match="F-CARDS-NOT-IN-ACTIVE-MANIFEST"):
        load_card(
            path=str(src),
            environment="production",
            manifest_path=str(overlay_manifest_path),
        )


def test_loader_rejects_when_manifest_entry_marked_inactive(tmp_path: Path):
    """A manifest entry whose ``active`` field is anything other than True
    MUST fail closed at production-load time. Models a 'card deprecated but
    file still present' scenario."""

    src = CIC_DIR / "food_systems.yaml"
    overlay_manifest_path = tmp_path / "registry_inactive.yaml"
    overlay_manifest_path.write_text(yaml.safe_dump({
        "registry_kind": "active_card_registry",
        "schema_version": "1.0-card-registry",
        "truth_invariant": "test-inactive",
        "active_cards": [{
            "namespace": "cards:cic:food_systems",
            "card_path": str(src.resolve()),
            "card_axis": "CIC",
            "card_id": "TILTH-CIC-01",
            "slug": "food_systems",
            "active": False,  # deactivated
            "required_draft_status": "signed",
            "required_runtime_loadable": True,
        }],
    }, sort_keys=False))

    with pytest.raises(CardManifestMembershipError, match="F-CARDS-NOT-IN-ACTIVE-MANIFEST"):
        load_card(
            path=str(src),
            environment="production",
            manifest_path=str(overlay_manifest_path),
        )


def test_loader_rejects_when_manifest_file_missing(tmp_path: Path):
    """If the explicit manifest_path does not exist, production load MUST fail
    closed with F-CARDS-NOT-IN-ACTIVE-MANIFEST (not a bare FileNotFoundError)."""

    src = CIC_DIR / "food_systems.yaml"
    missing_manifest_path = tmp_path / "does_not_exist.yaml"

    with pytest.raises(CardManifestMembershipError, match="F-CARDS-NOT-IN-ACTIVE-MANIFEST"):
        load_card(
            path=str(src),
            environment="production",
            manifest_path=str(missing_manifest_path),
        )
