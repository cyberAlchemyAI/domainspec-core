import ast
import json
import subprocess
import sys
from pathlib import Path
from unittest import mock
import pytest

CLI_MODULE = "pipeline.nervous_system.scout_cli.intake"

def run_cli(*args):
    cmd = [sys.executable, "-m", CLI_MODULE, *args]
    return subprocess.run(cmd, capture_output=True, text=True)

@pytest.fixture
def synthetic_csv(tmp_path):
    csv_content = (
        "Opportunity Title,Agency,Opportunity Number,Close Date\n"
        "Test Opp,Test Agency,OPP-123,2026-12-31\n"
    )
    p = tmp_path / "test.csv"
    p.write_text(csv_content, encoding="utf-8-sig")
    return p

@pytest.fixture
def synthetic_csv_no_opp(tmp_path):
    csv_content = (
        "Opportunity Title,Agency,Close Date\n"
        "Test Opp,Test Agency,2026-12-31\n"
    )
    p = tmp_path / "test_no_opp.csv"
    p.write_text(csv_content, encoding="utf-8-sig")
    return p

def test_cli_accepts_public_corpus_without_applied_as_entity_id(tmp_path, synthetic_csv):
    out = tmp_path / "out"
    res = run_cli(
        "--source", "grants_gov",
        "--identity-scope", "public_corpus",
        "--input", str(synthetic_csv),
        "--output-root", str(out),
        "--run-id", "test-1"
    )
    assert res.returncode == 0
    assert "Intake complete" in res.stdout

def test_cli_rejects_public_corpus_with_applied_as_entity_id(tmp_path, synthetic_csv):
    out = tmp_path / "out"
    res = run_cli(
        "--source", "grants_gov",
        "--identity-scope", "public_corpus",
        "--input", str(synthetic_csv),
        "--output-root", str(out),
        "--run-id", "test-1",
        "--applied-as-entity-id", "test_entity"
    )
    assert res.returncode != 0
    assert "forbidden when identity_scope=public_corpus" in res.stderr

def test_cli_rejects_applied_as_entity_without_applied_as_entity_id(tmp_path, synthetic_csv):
    out = tmp_path / "out"
    res = run_cli(
        "--source", "grants_gov",
        "--identity-scope", "applied_as_entity",
        "--input", str(synthetic_csv),
        "--output-root", str(out),
        "--run-id", "test-1"
    )
    assert res.returncode != 0
    assert "required when identity_scope=applied_as_entity" in res.stderr

def test_cli_accepts_applied_as_entity_with_applied_as_entity_id(tmp_path, synthetic_csv):
    out = tmp_path / "out"
    res = run_cli(
        "--source", "grants_gov",
        "--identity-scope", "applied_as_entity",
        "--input", str(synthetic_csv),
        "--output-root", str(out),
        "--run-id", "test-1",
        "--applied-as-entity-id", "test_entity"
    )
    assert res.returncode == 0
    assert "Intake complete" in res.stdout

def test_cli_rejects_generated_at_utc_with_fractional_seconds(tmp_path, synthetic_csv):
    out = tmp_path / "out"
    res = run_cli(
        "--source", "grants_gov",
        "--identity-scope", "public_corpus",
        "--input", str(synthetic_csv),
        "--output-root", str(out),
        "--run-id", "test-1",
        "--generated-at-utc", "2026-05-27T21:00:00.123456Z"
    )
    assert res.returncode != 0
    assert "Invalid generated_at_utc format" in res.stderr

def test_cli_accepts_generated_at_utc_with_exact_seconds(tmp_path, synthetic_csv):
    out = tmp_path / "out"
    res = run_cli(
        "--source", "grants_gov",
        "--identity-scope", "public_corpus",
        "--input", str(synthetic_csv),
        "--output-root", str(out),
        "--run-id", "test-1",
        "--generated-at-utc", "2026-05-27T21:00:00Z"
    )
    assert res.returncode == 0
    assert "Intake complete" in res.stdout

def test_cli_generated_timestamp_has_no_fractional_seconds(tmp_path, synthetic_csv):
    out = tmp_path / "out"
    res = run_cli(
        "--source", "grants_gov",
        "--identity-scope", "public_corpus",
        "--input", str(synthetic_csv),
        "--output-root", str(out),
        "--run-id", "test-timestamp"
    )
    assert res.returncode == 0
    manifest = out / "snapshots" / "test-timestamp" / "manifest.json"
    data = json.loads(manifest.read_text())
    assert "." not in data["generated_at_utc"]
    assert data["generated_at_utc"].endswith("Z")

def test_cli_output_uses_d6_atomic_export_locations(tmp_path, synthetic_csv):
    out = tmp_path / "out"
    res = run_cli(
        "--source", "grants_gov",
        "--identity-scope", "public_corpus",
        "--input", str(synthetic_csv),
        "--output-root", str(out),
        "--run-id", "test-1"
    )
    assert res.returncode == 0
    assert (out / "snapshots" / "test-1" / "manifest.json").exists()
    assert (out / "latest" / "manifest.json").exists()
    assert not (out / "latest.tmp").exists()
    assert not (out / "snapshots" / "test-1.tmp").exists()

def test_public_corpus_requires_opportunity_number(tmp_path, synthetic_csv_no_opp):
    out = tmp_path / "out"
    res = run_cli(
        "--source", "grants_gov",
        "--identity-scope", "public_corpus",
        "--input", str(synthetic_csv_no_opp),
        "--output-root", str(out),
        "--run-id", "test-1"
    )
    assert res.returncode != 0
    assert "Missing opportunity number" in res.stderr

def test_public_corpus_identity_hash_excludes_applied_as_entity_id_and_no_sentinel_identity(tmp_path, synthetic_csv):
    out = tmp_path / "out"
    res = run_cli(
        "--source", "grants_gov",
        "--identity-scope", "public_corpus",
        "--input", str(synthetic_csv),
        "--output-root", str(out),
        "--run-id", "test-hash"
    )
    assert res.returncode == 0
    full_jsonl = out / "snapshots" / "test-hash" / "enriched_opportunities_full.jsonl"
    lines = full_jsonl.read_text().strip().split("\n")
    assert len(lines) == 1
    record = json.loads(lines[0])

    # Must not contain PUBLIC_SCOUT_INTAKE or similar sentinels
    assert "PUBLIC_SCOUT_INTAKE" not in str(record)

    # The applied_as_entity_id should be None
    grants_gov = record.get("grants_gov", {})
    assert grants_gov.get("applied_as_entity_id") is None

    # Identity hash should match D7.1 behavior for public_corpus
    # "OPP-", "public_corpus", "opp-123", "test opp", "test agency"
    import hashlib
    hasher = hashlib.sha3_256()
    hasher.update("public_corpus|opp-123|test opp|test agency".encode("utf-8"))
    expected_id = "OPP-" + hasher.hexdigest()[:16]

    assert record["opportunity_id"] == expected_id

def _get_module_source():
    p = Path(__file__).parent.parent.parent / "pipeline" / "nervous_system" / "scout_cli" / "intake.py"
    with open(p, "r", encoding="utf-8") as f:
        return f.read(), str(p)

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
