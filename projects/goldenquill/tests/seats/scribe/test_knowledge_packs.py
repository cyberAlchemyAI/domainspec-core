"""Tests for ``pipeline.seats.scribe.knowledge_packs``.

Exercises:
- Loader resolves directory layout (``<sector>/*.json`` auto-merge).
- Loader resolves single-file layout (``<sector>.json``).
- Missing sector → empty pack with ``is_loaded=False`` (not an error).
- Schema violations → :class:`KnowledgePackSchemaError`.
- Duplicate ids across merged files → :class:`KnowledgePackDuplicateIdError`.
- Invalid sector name → :class:`KnowledgePackInvalidSectorError`.
- Frozen dataclass invariants (empty id, empty statement, bad confidence).

Real-pack smoke test: loads ``regenerative_ag/usda_terminology.json`` from
the actual repo to verify the example pack parses and looks plausible.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from pipeline.seats.scribe.knowledge_packs import (
    DEFAULT_BASE_DIR,
    KnowledgePack,
    KnowledgePackDuplicateIdError,
    KnowledgePackInvalidSectorError,
    KnowledgePackSchemaError,
    PackFact,
    PROJECT_CONTEXT_PACK_KEY,
    SECTOR_VALID,
    load_sector_pack,
    merge_pack_into_project_context,
    render_sector_context_block,
)


# --------------------------------------------------------------------------
# Fixtures — synthetic packs in a tmp dir
# --------------------------------------------------------------------------

def _write_pack(path: Path, *, facts: list[dict], domains: list[dict] | None = None,
                relationships: list[dict] | None = None,
                schema_version: str = "1.0") -> None:
    payload = {
        "schemaVersion": schema_version,
        "description": "synthetic test pack",
        "domains": domains if domains is not None else [
            {"id": "dom-1", "name": "Domain One", "description": "test domain"}
        ],
        "facts": facts,
        "relationships": relationships or [],
    }
    path.write_text(json.dumps(payload), encoding="utf-8")


def _basic_fact(fact_id: str = "fct-1", domain_id: str = "dom-1") -> dict:
    return {
        "id": fact_id,
        "domainId": domain_id,
        "statement": "synthetic test fact",
        "tags": ["test"],
        "confidence": "high",
        "scope": "general",
    }


# --------------------------------------------------------------------------
# Sector enum + missing-pack semantics
# --------------------------------------------------------------------------

class TestSectorEnum:

    def test_six_sectors_exact(self) -> None:
        assert SECTOR_VALID == frozenset({
            "workforce_future",
            "education_future",
            "regenerative_ag",
            "urban_ag",
            "land_community",
            "eco_art",
        })

    def test_invalid_sector_raises(self, tmp_path: Path) -> None:
        with pytest.raises(KnowledgePackInvalidSectorError):
            load_sector_pack("not_a_real_sector", base_dir=tmp_path)


class TestMissingPack:

    def test_missing_sector_returns_empty_pack(self, tmp_path: Path) -> None:
        pack = load_sector_pack("urban_ag", base_dir=tmp_path)
        assert isinstance(pack, KnowledgePack)
        assert pack.sector == "urban_ag"
        assert pack.is_loaded is False
        assert pack.facts == ()
        assert pack.domains == ()
        assert pack.source_files == ()


# --------------------------------------------------------------------------
# Layout: single file
# --------------------------------------------------------------------------

class TestSingleFileLayout:

    def test_loads_single_file(self, tmp_path: Path) -> None:
        _write_pack(
            tmp_path / "urban_ag.json",
            facts=[_basic_fact("fct-a")],
        )
        pack = load_sector_pack("urban_ag", base_dir=tmp_path)
        assert pack.is_loaded is True
        assert len(pack.facts) == 1
        assert pack.facts[0].id == "fct-a"
        assert len(pack.source_files) == 1


# --------------------------------------------------------------------------
# Layout: directory auto-merge
# --------------------------------------------------------------------------

class TestDirectoryAutoMerge:

    def test_merges_multiple_files_sorted(self, tmp_path: Path) -> None:
        sector_dir = tmp_path / "regenerative_ag"
        sector_dir.mkdir()
        _write_pack(
            sector_dir / "b_second.json",
            facts=[_basic_fact("fct-b", "dom-2")],
            domains=[{"id": "dom-2", "name": "Two"}],
            schema_version="1.0",
        )
        _write_pack(
            sector_dir / "a_first.json",
            facts=[_basic_fact("fct-a", "dom-1")],
            domains=[{"id": "dom-1", "name": "One"}],
            schema_version="1.0",
        )

        pack = load_sector_pack("regenerative_ag", base_dir=tmp_path)
        assert pack.is_loaded is True
        assert len(pack.facts) == 2
        # Sorted glob → 'a_first.json' before 'b_second.json'
        assert pack.facts[0].id == "fct-a"
        assert pack.facts[1].id == "fct-b"
        assert len(pack.domains) == 2
        assert pack.source_files[0].name == "a_first.json"

    def test_duplicate_fact_id_across_files_raises(self, tmp_path: Path) -> None:
        sector_dir = tmp_path / "regenerative_ag"
        sector_dir.mkdir()
        _write_pack(
            sector_dir / "first.json",
            facts=[_basic_fact("dup-id")],
        )
        _write_pack(
            sector_dir / "second.json",
            facts=[_basic_fact("dup-id")],
        )

        with pytest.raises(KnowledgePackDuplicateIdError):
            load_sector_pack("regenerative_ag", base_dir=tmp_path)

    def test_duplicate_domain_id_across_files_raises(self, tmp_path: Path) -> None:
        sector_dir = tmp_path / "regenerative_ag"
        sector_dir.mkdir()
        _write_pack(
            sector_dir / "first.json",
            facts=[_basic_fact("fct-x")],
            domains=[{"id": "shared-dom", "name": "First name"}],
        )
        _write_pack(
            sector_dir / "second.json",
            facts=[_basic_fact("fct-y")],
            domains=[{"id": "shared-dom", "name": "Second name"}],
        )

        with pytest.raises(KnowledgePackDuplicateIdError):
            load_sector_pack("regenerative_ag", base_dir=tmp_path)


# --------------------------------------------------------------------------
# Schema violations
# --------------------------------------------------------------------------

class TestSchemaErrors:

    def test_missing_schema_version(self, tmp_path: Path) -> None:
        path = tmp_path / "urban_ag.json"
        path.write_text(json.dumps({
            "domains": [],
            "facts": [],
            "relationships": [],
        }), encoding="utf-8")
        with pytest.raises(KnowledgePackSchemaError, match="schemaVersion"):
            load_sector_pack("urban_ag", base_dir=tmp_path)

    def test_facts_must_be_list(self, tmp_path: Path) -> None:
        path = tmp_path / "urban_ag.json"
        path.write_text(json.dumps({
            "schemaVersion": "1.0",
            "domains": [],
            "facts": "not a list",
            "relationships": [],
        }), encoding="utf-8")
        with pytest.raises(KnowledgePackSchemaError, match="facts"):
            load_sector_pack("urban_ag", base_dir=tmp_path)

    def test_invalid_json_raises(self, tmp_path: Path) -> None:
        path = tmp_path / "urban_ag.json"
        path.write_text("{not valid json", encoding="utf-8")
        with pytest.raises(KnowledgePackSchemaError, match="JSON parse"):
            load_sector_pack("urban_ag", base_dir=tmp_path)

    def test_top_level_must_be_object(self, tmp_path: Path) -> None:
        path = tmp_path / "urban_ag.json"
        path.write_text(json.dumps(["not", "an", "object"]), encoding="utf-8")
        with pytest.raises(KnowledgePackSchemaError, match="top-level"):
            load_sector_pack("urban_ag", base_dir=tmp_path)

    def test_fact_with_empty_id_raises(self, tmp_path: Path) -> None:
        path = tmp_path / "urban_ag.json"
        bad_fact = _basic_fact("")  # empty id
        path.write_text(json.dumps({
            "schemaVersion": "1.0",
            "domains": [{"id": "dom-1", "name": "One"}],
            "facts": [bad_fact],
            "relationships": [],
        }), encoding="utf-8")
        with pytest.raises(KnowledgePackSchemaError, match="id"):
            load_sector_pack("urban_ag", base_dir=tmp_path)

    def test_fact_with_bad_confidence_raises(self, tmp_path: Path) -> None:
        path = tmp_path / "urban_ag.json"
        bad_fact = _basic_fact("fct-1")
        bad_fact["confidence"] = "very-high"  # not in {high, medium, low}
        path.write_text(json.dumps({
            "schemaVersion": "1.0",
            "domains": [{"id": "dom-1", "name": "One"}],
            "facts": [bad_fact],
            "relationships": [],
        }), encoding="utf-8")
        with pytest.raises(KnowledgePackSchemaError, match="confidence"):
            load_sector_pack("urban_ag", base_dir=tmp_path)


# --------------------------------------------------------------------------
# Pack accessors
# --------------------------------------------------------------------------

class TestPackAccessors:

    def test_fact_by_id_hits(self, tmp_path: Path) -> None:
        _write_pack(
            tmp_path / "urban_ag.json",
            facts=[_basic_fact("fct-target")],
        )
        pack = load_sector_pack("urban_ag", base_dir=tmp_path)
        hit = pack.fact_by_id("fct-target")
        assert hit is not None
        assert hit.id == "fct-target"

    def test_fact_by_id_misses(self, tmp_path: Path) -> None:
        _write_pack(
            tmp_path / "urban_ag.json",
            facts=[_basic_fact("fct-target")],
        )
        pack = load_sector_pack("urban_ag", base_dir=tmp_path)
        assert pack.fact_by_id("not-there") is None

    def test_facts_in_domain(self, tmp_path: Path) -> None:
        _write_pack(
            tmp_path / "urban_ag.json",
            facts=[
                _basic_fact("a", "dom-X"),
                _basic_fact("b", "dom-X"),
                _basic_fact("c", "dom-Y"),
            ],
            domains=[
                {"id": "dom-X", "name": "X"},
                {"id": "dom-Y", "name": "Y"},
            ],
        )
        pack = load_sector_pack("urban_ag", base_dir=tmp_path)
        x_facts = pack.facts_in_domain("dom-X")
        assert len(x_facts) == 2
        assert {f.id for f in x_facts} == {"a", "b"}


# --------------------------------------------------------------------------
# Real-pack smoke test — load the example regenerative_ag pack from disk
# --------------------------------------------------------------------------

class TestExampleRegenerativeAgPack:
    """Verify the seed pack at pipeline/knowledge_packs/regenerative_ag/
    parses cleanly under the loader contract.
    """

    def test_default_base_dir_resolves(self) -> None:
        # DEFAULT_BASE_DIR points to <repo>/pipeline/knowledge_packs/
        assert DEFAULT_BASE_DIR.name == "knowledge_packs"

    def test_loads_seed_pack(self) -> None:
        pack = load_sector_pack("regenerative_ag")
        assert pack.is_loaded is True, (
            "Expected pipeline/knowledge_packs/regenerative_ag/ to contain "
            "at least one pack file (e.g., usda_terminology.json)."
        )
        assert pack.sector == "regenerative_ag"
        assert len(pack.facts) >= 5, (
            "Seed pack should ship with at least 5 facts to be useful."
        )
        # Spot-check structural invariants
        for fact in pack.facts:
            assert isinstance(fact, PackFact)
            assert fact.confidence in {"high", "medium", "low"}
            assert fact.statement.strip()


# --------------------------------------------------------------------------
# Integration helpers — render + merge
# --------------------------------------------------------------------------

class TestRenderSectorContextBlock:
    """`render_sector_context_block` produces prompt-ready Markdown."""

    def test_empty_pack_renders_empty_string(self, tmp_path: Path) -> None:
        # No pack files on disk → unloaded pack → empty rendered block
        pack = load_sector_pack("urban_ag", base_dir=tmp_path)
        assert pack.is_loaded is False
        assert render_sector_context_block(pack) == ""

    def test_loaded_pack_includes_sector_header(self, tmp_path: Path) -> None:
        _write_pack(
            tmp_path / "urban_ag.json",
            facts=[_basic_fact("fct-1")],
        )
        pack = load_sector_pack("urban_ag", base_dir=tmp_path)
        block = render_sector_context_block(pack)
        assert "## Sector context: urban_ag" in block
        assert "Domain One" in block  # default domain name
        assert "[high]" in block      # confidence tier surfaced
        assert "synthetic test fact" in block

    def test_max_facts_caps_output(self, tmp_path: Path) -> None:
        _write_pack(
            tmp_path / "urban_ag.json",
            facts=[
                _basic_fact("fct-1"),
                _basic_fact("fct-2"),
                _basic_fact("fct-3"),
                _basic_fact("fct-4"),
            ],
        )
        pack = load_sector_pack("urban_ag", base_dir=tmp_path)
        block_capped = render_sector_context_block(pack, max_facts=2)
        # Two of the four facts surface
        bullet_count = block_capped.count("- [high]")
        assert bullet_count == 2

    def test_max_facts_zero_renders_headers_only(self, tmp_path: Path) -> None:
        _write_pack(
            tmp_path / "urban_ag.json",
            facts=[_basic_fact("fct-1")],
        )
        pack = load_sector_pack("urban_ag", base_dir=tmp_path)
        block = render_sector_context_block(pack, max_facts=0)
        # No bullet points emitted
        assert "- [" not in block

    def test_orphan_fact_surfaces_under_other_context(self, tmp_path: Path) -> None:
        # Fact references a domain_id that isn't in the pack's domains list
        path = tmp_path / "urban_ag.json"
        path.write_text(json.dumps({
            "schemaVersion": "1.0",
            "description": "test",
            "domains": [{"id": "dom-A", "name": "A"}],
            "facts": [
                {
                    "id": "fct-orphan",
                    "domainId": "dom-NONEXISTENT",
                    "statement": "orphan fact",
                    "tags": [],
                    "confidence": "medium",
                    "scope": "general",
                }
            ],
            "relationships": [],
        }), encoding="utf-8")
        pack = load_sector_pack("urban_ag", base_dir=tmp_path)
        block = render_sector_context_block(pack)
        assert "### Other context" in block
        assert "orphan fact" in block

    def test_real_pack_renders_cleanly(self) -> None:
        """Real regenerative_ag seed pack should produce a well-formed block."""
        pack = load_sector_pack("regenerative_ag")
        block = render_sector_context_block(pack)
        assert block.startswith("## Sector context: regenerative_ag")
        assert "### " in block  # at least one domain header
        assert block.endswith("\n")
        # Token-budget sanity: rendered block should fit comfortably under
        # any reasonable Anthropic prompt slot. ~24 facts * ~300 chars = 7200,
        # generous ceiling 16k.
        assert len(block) < 16384, (
            f"Rendered block is {len(block)} chars — exceeds 16k ceiling, "
            f"may bust prompt budget. Reduce DEFAULT_PROMPT_FACT_CAP or "
            f"trim pack facts."
        )


class TestMergePackIntoProjectContext:
    """`merge_pack_into_project_context` injects sector_knowledge key."""

    def test_unloaded_pack_still_surfaces_loaded_false(
        self, tmp_path: Path
    ) -> None:
        pack = load_sector_pack("urban_ag", base_dir=tmp_path)
        ctx = merge_pack_into_project_context({"applicant": "Test Org"}, pack)
        assert PROJECT_CONTEXT_PACK_KEY in ctx
        assert ctx[PROJECT_CONTEXT_PACK_KEY]["loaded"] is False
        assert ctx[PROJECT_CONTEXT_PACK_KEY]["sector"] == "urban_ag"
        assert ctx[PROJECT_CONTEXT_PACK_KEY]["fact_count"] == 0

    def test_loaded_pack_populates_fields(self, tmp_path: Path) -> None:
        _write_pack(
            tmp_path / "urban_ag.json",
            facts=[_basic_fact("fct-1"), _basic_fact("fct-2")],
        )
        pack = load_sector_pack("urban_ag", base_dir=tmp_path)
        ctx = merge_pack_into_project_context({"applicant": "Test Org"}, pack)
        entry = ctx[PROJECT_CONTEXT_PACK_KEY]
        assert entry["loaded"] is True
        assert entry["sector"] == "urban_ag"
        assert entry["fact_count"] == 2
        assert entry["domain_count"] == 1
        assert len(entry["source_files"]) == 1
        assert "## Sector context: urban_ag" in entry["rendered_block"]

    def test_does_not_mutate_input(self, tmp_path: Path) -> None:
        pack = load_sector_pack("urban_ag", base_dir=tmp_path)
        original = {"applicant": "Test Org", "year": 2026}
        merged = merge_pack_into_project_context(original, pack)
        # original mapping is unchanged
        assert PROJECT_CONTEXT_PACK_KEY not in original
        assert original == {"applicant": "Test Org", "year": 2026}
        # merged is a new dict
        assert merged is not original
        # Existing keys preserved
        assert merged["applicant"] == "Test Org"
        assert merged["year"] == 2026

    def test_preserves_existing_keys(self, tmp_path: Path) -> None:
        _write_pack(
            tmp_path / "urban_ag.json",
            facts=[_basic_fact("fct-1")],
        )
        pack = load_sector_pack("urban_ag", base_dir=tmp_path)
        existing = {
            "applicant": "FIT Farms LLC",
            "evidence_facts": [{"id": "ev-1", "text": "..."}],
            "narrative_spine": "soil-health led",
        }
        merged = merge_pack_into_project_context(existing, pack)
        assert merged["applicant"] == "FIT Farms LLC"
        assert merged["narrative_spine"] == "soil-health led"
        assert merged["evidence_facts"] == [{"id": "ev-1", "text": "..."}]
        assert PROJECT_CONTEXT_PACK_KEY in merged


# --------------------------------------------------------------------------
# Wire-in integration scenario: load → merge → block-render → simulate
# orchestrator passing the augmented context down to the seat envelope.
# --------------------------------------------------------------------------

class TestEndToEndWireIn:
    """Simulates the orchestrator's envelope-build sequence using real
    regenerative_ag seed pack. Proves the helpers compose."""

    def test_full_pipeline_load_merge_render(self) -> None:
        # 1. Orchestrator determines sector from PROJECT_CONTEXT.md
        sector = "regenerative_ag"

        # 2. Orchestrator loads the sector pack
        pack = load_sector_pack(sector)
        assert pack.is_loaded is True

        # 3. Orchestrator merges pack into project_context map
        base_project_context = {
            "applicant_name": "FIT Farms LLC",
            "narrative_spine": "five soil-health principles",
            "evidence_facts": [{"id": "ev-1", "text": "200-acre cover-cropped"}],
        }
        augmented_ctx = merge_pack_into_project_context(
            base_project_context, pack
        )

        # 4. The augmented context now carries sector_knowledge
        sk = augmented_ctx[PROJECT_CONTEXT_PACK_KEY]
        assert sk["loaded"] is True
        assert sk["sector"] == "regenerative_ag"
        assert sk["fact_count"] >= 5
        assert sk["rendered_block"].startswith("## Sector context: regenerative_ag")

        # 5. Original keys preserved — Scribe seat sees both base context
        # and sector pack via the same project_context mapping.
        assert augmented_ctx["applicant_name"] == "FIT Farms LLC"
        assert augmented_ctx["narrative_spine"] == "five soil-health principles"

        # 6. Block is a non-empty string ready for splicing into compiled_prompt
        block = sk["rendered_block"]
        assert isinstance(block, str)
        assert block.strip()  # not just whitespace

    def test_orchestrator_can_skip_unset_sector(self, tmp_path: Path) -> None:
        # Sector that hasn't been seeded yet → merge still works,
        # `loaded=False` flag tells downstream code to skip pack-aware logic.
        pack = load_sector_pack("eco_art", base_dir=tmp_path)
        ctx = merge_pack_into_project_context({"applicant": "X"}, pack)
        assert ctx[PROJECT_CONTEXT_PACK_KEY]["loaded"] is False
        # No spurious header injection — empty block, not garbage
        assert ctx[PROJECT_CONTEXT_PACK_KEY]["rendered_block"] == ""
