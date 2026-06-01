import ast
import json
import subprocess
import sys
from pathlib import Path
from unittest import mock

import pytest

from pipeline.nervous_system.scout_adapters.grants_gov_download import GrantsGovOpportunityRecord
from pipeline.nervous_system.scout_adapters.sam_gov_assistance_listings import SamGovAssistanceListingRecord
from pipeline.nervous_system.scout_cli.read_model_smoke import create_synthetic_listing, create_synthetic_opportunity

CLI_MODULE = "pipeline.nervous_system.scout_cli.read_model_smoke"

def run_cli(*args):
    cmd = [sys.executable, "-m", CLI_MODULE, *args]
    return subprocess.run(cmd, capture_output=True, text=True)


def test_cli_requires_output_root(tmp_path):
    result = run_cli("--run-id", "test1")
    assert result.returncode != 0
    assert "the following arguments are required: --output-root" in result.stderr


def test_cli_writes_snapshot_and_latest_to_tmp_path(tmp_path):
    output_root = tmp_path / "output"
    run_id = "test-run-1"
    result = run_cli("--output-root", str(output_root), "--run-id", run_id)
    assert result.returncode == 0

    snapshot_dir = output_root / "snapshots" / run_id
    latest_dir = output_root / "latest"

    assert (snapshot_dir / "enriched_opportunities_full.jsonl").exists()
    assert (snapshot_dir / "enriched_opportunities_index.jsonl").exists()
    assert (snapshot_dir / "manifest.json").exists()

    assert (latest_dir / "enriched_opportunities_full.jsonl").exists()
    assert (latest_dir / "enriched_opportunities_index.jsonl").exists()
    assert (latest_dir / "manifest.json").exists()


def test_cli_prints_manifest_counts(tmp_path):
    result = run_cli("--output-root", str(tmp_path), "--run-id", "test2")
    assert result.returncode == 0
    assert "full_record_count: 5" in result.stdout
    assert "index_record_count: 5" in result.stdout
    assert "matched_count: 1" in result.stdout
    assert "missing_aln_count: 1" in result.stdout
    assert "malformed_aln_count: 1" in result.stdout
    assert "unmatched_count: 1" in result.stdout
    assert "ambiguous_count: 1" in result.stdout


def test_cli_exits_zero_on_success(tmp_path):
    result = run_cli("--output-root", str(tmp_path), "--run-id", "test3")
    assert result.returncode == 0


def test_cli_exits_nonzero_when_snapshot_exists_without_overwrite(tmp_path):
    run_id = "test4"
    res1 = run_cli("--output-root", str(tmp_path), "--run-id", run_id)
    assert res1.returncode == 0
    res2 = run_cli("--output-root", str(tmp_path), "--run-id", run_id)
    assert res2.returncode != 0
    assert "Error during export" in res2.stderr


def test_cli_overwrite_snapshot_flag_allows_repeat_run(tmp_path):
    run_id = "test5"
    res1 = run_cli("--output-root", str(tmp_path), "--run-id", run_id)
    assert res1.returncode == 0
    res2 = run_cli("--output-root", str(tmp_path), "--run-id", run_id, "--overwrite-snapshot")
    assert res2.returncode == 0


def test_cli_does_not_write_generated_artifacts_to_repo(tmp_path):
    run_id = "test6"
    output_root = tmp_path / "test6_out"

    repo_root = Path(__file__).parent.parent.parent
    before_manifests = set(repo_root.rglob("manifest.json"))
    before_jsonls = set(repo_root.rglob("enriched_opportunities_*.jsonl"))

    res = run_cli("--output-root", str(output_root), "--run-id", run_id)
    assert res.returncode == 0

    after_manifests = set(repo_root.rglob("manifest.json"))
    after_jsonls = set(repo_root.rglob("enriched_opportunities_*.jsonl"))

    new_manifests = after_manifests - before_manifests
    new_jsonls = after_jsonls - before_jsonls

    for p in new_manifests:
        if output_root not in p.parents:
            pytest.fail(f"Artifact leaked into repo at {p}")
    for p in new_jsonls:
        if output_root not in p.parents:
            pytest.fail(f"Artifact leaked into repo at {p}")


def test_cli_output_manifest_has_expected_status_mix(tmp_path):
    run_id = "test7"
    run_cli("--output-root", str(tmp_path), "--run-id", run_id)
    manifest_path = tmp_path / "snapshots" / run_id / "manifest.json"
    data = json.loads(manifest_path.read_text())

    assert data["matched_count"] == 1
    assert data["missing_aln_count"] == 1
    assert data["malformed_aln_count"] == 1
    assert data["unmatched_count"] == 1
    assert data["ambiguous_count"] == 1
    assert data["full_record_count"] == 5


def test_cli_uses_d6_read_model_export(tmp_path):
    # Behavioral proof: output schema matches D6 expectations
    run_id = "test8"
    run_cli("--output-root", str(tmp_path), "--run-id", run_id)
    manifest_path = tmp_path / "snapshots" / run_id / "manifest.json"
    data = json.loads(manifest_path.read_text())

    assert data["schema_version"] == "1.0"
    assert data["read_model_version"] == "scout_enriched_opportunities_v1"
    assert "source_grants_gov_file" in data


def test_cli_synthetic_records_use_d3_d4_dataclasses():
    opp = create_synthetic_opportunity("x", "test", "10.000")
    assert isinstance(opp, GrantsGovOpportunityRecord)
    assert getattr(opp, "cfda_number", None) == "10.000"

    lst = create_synthetic_listing("y", "test", "10.000")
    assert isinstance(lst, SamGovAssistanceListingRecord)
    assert lst.assistance_listing_number == "10.000"


def _get_module_source():
    p = Path(__file__).parent.parent.parent / "pipeline" / "nervous_system" / "scout_cli" / "read_model_smoke.py"
    with open(p, "r", encoding="utf-8") as f:
        return f.read(), str(p)


def test_cli_uses_standard_library_argparse_only():
    src, path = _get_module_source()
    tree = ast.parse(src, filename=path)
    banned = {"click", "typer", "rich", "fire", "docopt"}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split('.')[0] not in banned
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                assert node.module.split('.')[0] not in banned


def test_no_network_or_model_imports():
    src, path = _get_module_source()
    tree = ast.parse(src, filename=path)
    banned = {
        "requests", "httpx", "aiohttp", "urllib", "socket",
        "playwright", "selenium", "openai", "anthropic", "google.generativeai"
    }
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


def test_no_ui_final_packet_application_guide_references():
    src, _ = _get_module_source()
    banned = ["apps/", "final_packet", "application_guide"]
    for b in banned:
        assert b not in src
