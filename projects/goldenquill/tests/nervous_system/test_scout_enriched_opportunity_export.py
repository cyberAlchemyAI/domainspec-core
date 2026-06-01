import ast
import json
import pytest
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from pipeline.nervous_system.scout_read_models.enriched_opportunity_export import (
    SnapshotAlreadyExistsError,
    export_enriched_opportunities_read_model,
)

@dataclass
class MockOpp:
    id: str
    title: str
    agency: str
    posted_date: str
    close_date: str

@dataclass
class MockListing:
    id: str
    objectives: str

@dataclass
class MockEnrichedRecord:
    opportunity: MockOpp
    assistance_listing: Optional[MockListing]
    assistance_listing_number_normalized: Optional[str]
    enrichment_status: str
    enrichment_reason: str
    enrichment_version: str
    joined_at_utc: str

def make_dummy_records():
    return [
        MockEnrichedRecord(
            opportunity=MockOpp(id="OPP1", title="Test 1", agency="A1", posted_date="2026-01-01", close_date="2026-02-01"),
            assistance_listing=MockListing(id="L1", objectives="Obj 1"),
            assistance_listing_number_normalized="10.001",
            enrichment_status="matched",
            enrichment_reason="Success",
            enrichment_version="v1",
            joined_at_utc="2026-01-02T00:00:00Z"
        ),
        MockEnrichedRecord(
            opportunity=MockOpp(id="OPP2", title="Test 2", agency="A2", posted_date="2026-01-02", close_date="2026-02-02"),
            assistance_listing=None,
            assistance_listing_number_normalized=None,
            enrichment_status="missing_aln",
            enrichment_reason="Missing",
            enrichment_version="v1",
            joined_at_utc="2026-01-02T00:00:00Z"
        )
    ]

def test_exports_snapshot_and_latest_files(tmp_path):
    recs = make_dummy_records()
    res = export_enriched_opportunities_read_model(
        enriched_records=recs,
        output_root=tmp_path,
        run_id="run_123",
        generated_at_utc="2026-01-02T01:00:00Z",
        source_grants_gov_file="gg.csv",
        source_sam_gov_file="sam.csv",
        source_grants_gov_hash="gghash",
        source_sam_gov_hash="samhash"
    )

    assert Path(res.full_jsonl_path).exists()
    assert Path(res.index_jsonl_path).exists()
    assert Path(res.manifest_path).exists()

    assert Path(res.latest_full_jsonl_path).exists()
    assert Path(res.latest_index_jsonl_path).exists()
    assert Path(res.latest_manifest_path).exists()

def test_snapshot_is_immutable_by_default(tmp_path):
    recs = make_dummy_records()
    export_enriched_opportunities_read_model(
        enriched_records=recs,
        output_root=tmp_path,
        run_id="run_123",
        generated_at_utc="2026-01-02T01:00:00Z",
        source_grants_gov_file="gg.csv",
        source_sam_gov_file="sam.csv",
        source_grants_gov_hash="gghash",
        source_sam_gov_hash="samhash"
    )

    with pytest.raises(SnapshotAlreadyExistsError):
        export_enriched_opportunities_read_model(
            enriched_records=recs,
            output_root=tmp_path,
            run_id="run_123",
            generated_at_utc="2026-01-02T01:00:00Z",
            source_grants_gov_file="gg.csv",
            source_sam_gov_file="sam.csv",
            source_grants_gov_hash="gghash",
            source_sam_gov_hash="samhash"
        )

def test_overwrite_snapshot_requires_explicit_flag(tmp_path):
    recs = make_dummy_records()
    export_enriched_opportunities_read_model(
        enriched_records=recs,
        output_root=tmp_path,
        run_id="run_123",
        generated_at_utc="2026-01-02T01:00:00Z",
        source_grants_gov_file="gg.csv",
        source_sam_gov_file="sam.csv",
        source_grants_gov_hash="gghash",
        source_sam_gov_hash="samhash"
    )

    # Should not raise
    export_enriched_opportunities_read_model(
        enriched_records=recs,
        output_root=tmp_path,
        run_id="run_123",
        generated_at_utc="2026-01-02T01:00:00Z",
        source_grants_gov_file="gg.csv",
        source_sam_gov_file="sam.csv",
        source_grants_gov_hash="gghash",
        source_sam_gov_hash="samhash",
        overwrite_snapshot=True
    )

def test_full_jsonl_contains_schema_version_record_type_and_lineage(tmp_path):
    recs = make_dummy_records()
    res = export_enriched_opportunities_read_model(
        enriched_records=recs,
        output_root=tmp_path,
        run_id="run_123",
        generated_at_utc="2026-01-02T01:00:00Z",
        source_grants_gov_file="gg.csv",
        source_sam_gov_file="sam.csv",
        source_grants_gov_hash="gghash",
        source_sam_gov_hash="samhash"
    )

    with open(res.full_jsonl_path, "r", encoding="utf-8") as f:
        first_line = json.loads(f.readline())

    assert first_line["schema_version"] == "1.0"
    assert first_line["record_type"] == "enriched_opportunity_full"
    assert first_line["read_model_version"] == "scout_enriched_opportunities_v1"

    lin = first_line["lineage"]
    assert lin["source_grants_gov_file"] == "gg.csv"
    assert lin["source_grants_gov_hash"] == "gghash"
    assert lin["source_sam_gov_file"] == "sam.csv"
    assert lin["source_sam_gov_hash"] == "samhash"
    assert lin["run_id"] == "run_123"

def test_index_jsonl_is_thin(tmp_path):
    recs = make_dummy_records()
    res = export_enriched_opportunities_read_model(
        enriched_records=recs,
        output_root=tmp_path,
        run_id="run_123",
        generated_at_utc="2026-01-02T01:00:00Z",
        source_grants_gov_file="gg.csv",
        source_sam_gov_file="sam.csv",
        source_grants_gov_hash="gghash",
        source_sam_gov_hash="samhash"
    )

    with open(res.index_jsonl_path, "r", encoding="utf-8") as f:
        first_line = json.loads(f.readline())

    assert first_line["schema_version"] == "1.0"
    assert first_line["record_type"] == "enriched_opportunity_index"
    assert first_line["opportunity_id"] == "OPP1"
    assert "objectives" not in first_line
    assert "grants_gov" not in first_line
    assert "sam_gov" not in first_line

def test_manifest_contains_counts_hashes_and_lineage(tmp_path):
    recs = make_dummy_records()
    res = export_enriched_opportunities_read_model(
        enriched_records=recs,
        output_root=tmp_path,
        run_id="run_123",
        generated_at_utc="2026-01-02T01:00:00Z",
        source_grants_gov_file="gg.csv",
        source_sam_gov_file="sam.csv",
        source_grants_gov_hash="gghash",
        source_sam_gov_hash="samhash"
    )

    with open(res.manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    assert manifest["full_record_count"] == 2
    assert manifest["index_record_count"] == 2
    assert manifest["matched_count"] == 1
    assert manifest["missing_aln_count"] == 1
    assert manifest["full_jsonl_sha256"]
    assert manifest["index_jsonl_sha256"]
    assert manifest["source_grants_gov_file"] == "gg.csv"

def test_record_counts_match_between_full_and_index(tmp_path):
    recs = make_dummy_records()
    res = export_enriched_opportunities_read_model(
        enriched_records=recs,
        output_root=tmp_path,
        run_id="run_123",
        generated_at_utc="2026-01-02T01:00:00Z",
        source_grants_gov_file="gg.csv",
        source_sam_gov_file="sam.csv",
        source_grants_gov_hash="gghash",
        source_sam_gov_hash="samhash"
    )

    assert res.full_record_count == res.index_record_count

def test_stable_record_order_by_opportunity_id(tmp_path):
    recs = make_dummy_records()
    # pass them out of order
    recs = [recs[1], recs[0]]
    res = export_enriched_opportunities_read_model(
        enriched_records=recs,
        output_root=tmp_path,
        run_id="run_123",
        generated_at_utc="2026-01-02T01:00:00Z",
        source_grants_gov_file="gg.csv",
        source_sam_gov_file="sam.csv",
        source_grants_gov_hash="gghash",
        source_sam_gov_hash="samhash"
    )

    with open(res.full_jsonl_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    l1 = json.loads(lines[0])
    l2 = json.loads(lines[1])
    assert l1["opportunity_id"] == "OPP1"
    assert l2["opportunity_id"] == "OPP2"

def test_hashes_are_over_exact_written_bytes(tmp_path):
    import hashlib
    recs = make_dummy_records()
    res = export_enriched_opportunities_read_model(
        enriched_records=recs,
        output_root=tmp_path,
        run_id="run_123",
        generated_at_utc="2026-01-02T01:00:00Z",
        source_grants_gov_file="gg.csv",
        source_sam_gov_file="sam.csv",
        source_grants_gov_hash="gghash",
        source_sam_gov_hash="samhash"
    )

    b_full = Path(res.full_jsonl_path).read_bytes()
    b_index = Path(res.index_jsonl_path).read_bytes()
    b_manifest = Path(res.manifest_path).read_bytes()

    assert hashlib.sha256(b_full).hexdigest() == res.full_jsonl_sha256
    assert hashlib.sha256(b_index).hexdigest() == res.index_jsonl_sha256
    assert hashlib.sha256(b_manifest).hexdigest() == res.manifest_sha256

def test_latest_is_updated_as_convenience_view(tmp_path):
    recs = make_dummy_records()
    export_enriched_opportunities_read_model(
        enriched_records=recs,
        output_root=tmp_path,
        run_id="run_A",
        generated_at_utc="2026-01-02T01:00:00Z",
        source_grants_gov_file="gg.csv",
        source_sam_gov_file="sam.csv",
        source_grants_gov_hash="gghash",
        source_sam_gov_hash="samhash"
    )
    res_b = export_enriched_opportunities_read_model(
        enriched_records=recs,
        output_root=tmp_path,
        run_id="run_B",
        generated_at_utc="2026-01-02T01:00:00Z",
        source_grants_gov_file="gg.csv",
        source_sam_gov_file="sam.csv",
        source_grants_gov_hash="gghash",
        source_sam_gov_hash="samhash"
    )

    with open(res_b.latest_manifest_path, "r", encoding="utf-8") as f:
        m = json.load(f)
    assert m["run_id"] == "run_B"

def test_does_not_mutate_input_records(tmp_path):
    recs = make_dummy_records()
    orig_opp_id = recs[0].opportunity.id

    export_enriched_opportunities_read_model(
        enriched_records=recs,
        output_root=tmp_path,
        run_id="run_A",
        generated_at_utc="2026-01-02T01:00:00Z",
        source_grants_gov_file="gg.csv",
        source_sam_gov_file="sam.csv",
        source_grants_gov_hash="gghash",
        source_sam_gov_hash="samhash"
    )

    assert recs[0].opportunity.id == orig_opp_id

def test_handles_null_sam_gov_block_for_unmatched_records(tmp_path):
    recs = [
        MockEnrichedRecord(
            opportunity=MockOpp(id="OPP1", title="Test 1", agency="A1", posted_date="2026-01-01", close_date="2026-02-01"),
            assistance_listing=None,
            assistance_listing_number_normalized="10.001",
            enrichment_status="unmatched",
            enrichment_reason="Success",
            enrichment_version="v1",
            joined_at_utc="2026-01-02T00:00:00Z"
        )
    ]
    res = export_enriched_opportunities_read_model(
        enriched_records=recs,
        output_root=tmp_path,
        run_id="run_A",
        generated_at_utc="2026-01-02T01:00:00Z",
        source_grants_gov_file="gg.csv",
        source_sam_gov_file="sam.csv",
        source_grants_gov_hash="gghash",
        source_sam_gov_hash="samhash"
    )

    with open(res.full_jsonl_path, "r", encoding="utf-8") as f:
        l = json.loads(f.readline())

    assert l["sam_gov"] is None

def test_status_counts_include_matched_missing_malformed_unmatched_ambiguous(tmp_path):
    recs = [
        MockEnrichedRecord(opportunity=MockOpp(id="1", title="1", agency="1", posted_date="", close_date=""), assistance_listing=None, assistance_listing_number_normalized=None, enrichment_status="matched", enrichment_reason="", enrichment_version="", joined_at_utc=""),
        MockEnrichedRecord(opportunity=MockOpp(id="2", title="2", agency="2", posted_date="", close_date=""), assistance_listing=None, assistance_listing_number_normalized=None, enrichment_status="missing_aln", enrichment_reason="", enrichment_version="", joined_at_utc=""),
        MockEnrichedRecord(opportunity=MockOpp(id="3", title="3", agency="3", posted_date="", close_date=""), assistance_listing=None, assistance_listing_number_normalized=None, enrichment_status="malformed_aln", enrichment_reason="", enrichment_version="", joined_at_utc=""),
        MockEnrichedRecord(opportunity=MockOpp(id="4", title="4", agency="4", posted_date="", close_date=""), assistance_listing=None, assistance_listing_number_normalized=None, enrichment_status="unmatched", enrichment_reason="", enrichment_version="", joined_at_utc=""),
        MockEnrichedRecord(opportunity=MockOpp(id="5", title="5", agency="5", posted_date="", close_date=""), assistance_listing=None, assistance_listing_number_normalized=None, enrichment_status="ambiguous", enrichment_reason="", enrichment_version="", joined_at_utc=""),
    ]
    res = export_enriched_opportunities_read_model(
        enriched_records=recs,
        output_root=tmp_path,
        run_id="run_A",
        generated_at_utc="2026-01-02T01:00:00Z",
        source_grants_gov_file="gg.csv",
        source_sam_gov_file="sam.csv",
        source_grants_gov_hash="gghash",
        source_sam_gov_hash="samhash"
    )

    assert res.matched_count == 1
    assert res.missing_aln_count == 1
    assert res.malformed_aln_count == 1
    assert res.unmatched_count == 1
    assert res.ambiguous_count == 1

def test_serializes_dataclasses_and_simple_objects(tmp_path):
    class SimpleObj:
        def __init__(self):
            self.foo = "bar"

    recs = [
        MockEnrichedRecord(
            opportunity=SimpleObj(),
            assistance_listing=None,
            assistance_listing_number_normalized="10.001",
            enrichment_status="unmatched",
            enrichment_reason="Success",
            enrichment_version="v1",
            joined_at_utc="2026-01-02T00:00:00Z"
        )
    ]
    res = export_enriched_opportunities_read_model(
        enriched_records=recs,
        output_root=tmp_path,
        run_id="run_A",
        generated_at_utc="2026-01-02T01:00:00Z",
        source_grants_gov_file="gg.csv",
        source_sam_gov_file="sam.csv",
        source_grants_gov_hash="gghash",
        source_sam_gov_hash="samhash"
    )
    with open(res.full_jsonl_path, "r", encoding="utf-8") as f:
        l = json.loads(f.readline())
        assert l["grants_gov"]["foo"] == "bar"

def test_no_generated_read_models_are_written_to_repo_paths_by_default():
    import inspect
    from pipeline.nervous_system.scout_read_models import enriched_opportunity_export
    sig = inspect.signature(enriched_opportunity_export.export_enriched_opportunities_read_model)
    # output_root should not have a default pointing to the repo
    assert sig.parameters['output_root'].default == inspect.Parameter.empty


def _get_module_source():
    p = Path(__file__).parent.parent.parent / "pipeline" / "nervous_system" / "scout_read_models" / "enriched_opportunity_export.py"
    with open(p, "r", encoding="utf-8") as f:
        return f.read(), str(p)


def test_no_network_or_model_imports():
    src, path = _get_module_source()
    tree = ast.parse(src, filename=path)
    banned = {"requests", "httpx", "aiohttp", "urllib", "socket", "playwright", "selenium",
              "openai", "anthropic", "google.generativeai", "llm", "vllm", "ollama"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split('.')[0] not in banned
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                assert node.module.split('.')[0] not in banned


def test_no_dynamic_import_or_eval_escape_hatches():
    src, _ = _get_module_source()
    banned = ["importlib", "__import__", "eval(", "exec("]
    for b in banned:
        assert b not in src


def test_no_authority_expansion_language():
    src, _ = _get_module_source()
    src_lower = src.lower()
    banned = [
        "crawl", "scrape", "discover urls", "discover_url", "autonomous",
        "submit", "portal upload", "partner_alert", "outreach",
        "candidate_generation", "drafting", "all_model_access", "frontier_eligible"
    ]
    for b in banned:
        assert b not in src_lower


def test_no_funder_terrain_import_or_path_reference():
    src, _ = _get_module_source()
    assert "funder_terrain" not in src


def test_no_ui_export_application_guide_references():
    src, _ = _get_module_source()
    banned = ["apps/", "final_packet", "application_guide"]
    for b in banned:
        assert b not in src
