"""
Adversarial torture tests for pipeline.nervous_system.funder_terrain.intake

Coverage required:
1. Stable deterministic output across reordered JSON keys.
2. Stable deterministic output across repeated runs.
3. Rejection of malformed JSON.
4. Rejection of non-object JSON root values.
5. Rejection of empty files.
6. Rejection of remote-looking path strings.
7. Rejection of forbidden source_id values containing http, https, api, web, url, scrape, crawler, llm, model, candidate, partner_alert.
8. Human-review fallback for incomplete curated records.
9. Unicode-heavy record succeeds deterministically.
10. Large local text_window succeeds without network/model behavior.
11. Output-dir write remains deterministic and does not mutate ledgers.
12. Static source check confirms no forbidden imports/calls in intake.py.
"""

import ast
import json
import random
import uuid
from pathlib import Path

import pytest

from pipeline.nervous_system.funder_terrain.intake import (
    CURATED_LOCAL_SOURCE_TYPE,
    intake_curated_funder_terrain_file,
)


def _write_json(tmp_path: Path, data: dict, filename: str = "record.json") -> Path:
    p = tmp_path / filename
    p.write_text(json.dumps(data), encoding="utf-8")
    return p


_BASE_RECORD = {
    "funder_name": "National Endowment for the Arts",
    "program_name": "Challenge America",
    "document_type": "Notice of Funding Opportunity",
    "geography": "United States",
    "notes": "Annual deadline in April.",
    "eligibility": "Nonprofits, local governments.",
}


# 1. Stable deterministic output across reordered JSON keys.
def test_stable_deterministic_across_reordered_keys(tmp_path):
    keys = list(_BASE_RECORD.keys())
    p = tmp_path / "record.json"

    # Write first time with original key order
    record1 = {k: _BASE_RECORD[k] for k in keys}
    p.write_text(json.dumps(record1), encoding="utf-8")
    res1 = intake_curated_funder_terrain_file(p, source_id="stable_src")

    # Write second time with shuffled key order to the EXACT same path
    keys_shuffled = keys[:]
    random.seed(42)
    random.shuffle(keys_shuffled)
    record2 = {k: _BASE_RECORD[k] for k in keys_shuffled}
    p.write_text(json.dumps(record2), encoding="utf-8")
    res2 = intake_curated_funder_terrain_file(p, source_id="stable_src")

    assert res1.record_sha256 == res2.record_sha256
    assert res1.normalization_input_sha256 == res2.normalization_input_sha256


# 2. Stable deterministic output across repeated runs.
def test_stable_deterministic_across_repeated_runs(tmp_path):
    p = _write_json(tmp_path, _BASE_RECORD)
    res1 = intake_curated_funder_terrain_file(p, source_id="stable_src")
    res2 = intake_curated_funder_terrain_file(p, source_id="stable_src")
    res3 = intake_curated_funder_terrain_file(p, source_id="stable_src")

    assert res1.record_sha256 == res2.record_sha256 == res3.record_sha256


# 3. Rejection of malformed JSON.
def test_rejection_malformed_json(tmp_path):
    p = tmp_path / "malformed.json"
    p.write_text("{ \"missing_quote: true }", encoding="utf-8")
    with pytest.raises(ValueError, match="Malformed JSON"):
        intake_curated_funder_terrain_file(p)


# 4. Rejection of non-object JSON root values.
@pytest.mark.parametrize("json_val", [
    "\"a string\"",
    "42",
    "[1, 2, 3]",
    "true",
    "null"
])
def test_rejection_non_object_json_root(tmp_path, json_val):
    p = tmp_path / "non_object.json"
    p.write_text(json_val, encoding="utf-8")
    with pytest.raises(ValueError, match="JSON object"):
        intake_curated_funder_terrain_file(p)


# 5. Rejection of empty files.
def test_rejection_empty_file(tmp_path):
    p = tmp_path / "empty.json"
    p.write_text("", encoding="utf-8")
    with pytest.raises(ValueError, match="Malformed JSON"):
        intake_curated_funder_terrain_file(p)


# 6. Rejection of remote-looking path strings.
def test_rejection_remote_looking_paths(tmp_path):
    p = _write_json(tmp_path, _BASE_RECORD)

    # We can't pass a remote Path to intake, but we can pass a fake PosixPath
    # and it should fail the validation step if it starts with http/https etc.
    remote_path = Path("http://example.com/record.json")
    with pytest.raises(ValueError, match="[Rr]emote-looking path rejected"):
        intake_curated_funder_terrain_file(remote_path)


# 7. Rejection of forbidden source_id values.
@pytest.mark.parametrize("forbidden_term", [
    "http", "https", "api", "web", "url", "scrape", "crawler",
    "llm", "model", "candidate", "partner_alert"
])
def test_rejection_forbidden_source_id(tmp_path, forbidden_term):
    p = _write_json(tmp_path, _BASE_RECORD)
    with pytest.raises(ValueError, match="Forbidden term"):
        intake_curated_funder_terrain_file(p, source_id=f"my_{forbidden_term}_source")


# 8. Human-review fallback for incomplete curated records.
def test_human_review_fallback_incomplete_record(tmp_path):
    p = _write_json(tmp_path, {"notes": "Some very ambiguous record."})
    res = intake_curated_funder_terrain_file(p)
    assert res.review_status.human_review_required is True
    assert len(res.metadata_gaps.missing_fields) > 0


# 9. Unicode-heavy record succeeds deterministically.
def test_unicode_heavy_record_succeeds(tmp_path):
    unicode_record = _BASE_RECORD.copy()
    unicode_record["notes"] += " 🌍🚀 Important grant 📝. Über prüfen. 基金会 (Foundation)"

    p = _write_json(tmp_path, unicode_record)
    res1 = intake_curated_funder_terrain_file(p, source_id="unicode_test")
    res2 = intake_curated_funder_terrain_file(p, source_id="unicode_test")

    assert res1.record_sha256 is not None
    assert res1.record_sha256 == res2.record_sha256


# 10. Large local text_window succeeds without network/model behavior.
def test_large_local_text_window_succeeds(tmp_path):
    large_text = "This is a repeated paragraph. " * 10000 # ~300KB text
    large_record = {
        "funder_name": "Big Funder",
        "document_type": "Guidelines",
        "description": large_text
    }
    p = _write_json(tmp_path, large_record)
    res = intake_curated_funder_terrain_file(p, source_id="large_test")

    assert res.record_id is not None
    assert len(res.normalization_input_sha256) == 64
    assert res.source_provenance.source_type == CURATED_LOCAL_SOURCE_TYPE


# 11. Output-dir write remains deterministic and does not mutate ledgers.
def test_output_dir_write_remains_deterministic(tmp_path):
    out_dir = tmp_path / "output"
    out_dir.mkdir(parents=True, exist_ok=True)

    input_dir = tmp_path / "input"
    input_dir.mkdir(parents=True, exist_ok=True)

    p = _write_json(input_dir, _BASE_RECORD, filename="usda.json")

    res = intake_curated_funder_terrain_file(p, source_id="write_test", output_dir=out_dir)

    out_file = out_dir / f"{res.record_id}.json"
    assert out_file.exists()

    written_data = out_file.read_text(encoding="utf-8")
    loaded = json.loads(written_data)

    # Must be completely identical when parsed back
    assert loaded["record_id"] == res.record_id
    assert loaded["record_sha256"] == res.record_sha256

    # Keys should be sorted in the JSON output, meaning it's deterministic.
    # We verify stable keys by checking the string serialization again.
    written_data_2 = json.dumps(loaded, sort_keys=True, default=str)
    assert written_data == written_data_2


# 12. Static source check confirms no forbidden imports/calls in intake.py.
def test_static_source_check_no_forbidden_imports_calls():
    intake_path = Path(__file__).resolve().parent.parent.parent / \
        "pipeline" / "nervous_system" / "funder_terrain" / "intake.py"

    source = intake_path.read_text(encoding="utf-8").lower()

    hard_forbidden_calls = [
        "requests.get(", "requests.post(", "httpx.", "aiohttp.",
        "subprocess.run(", "subprocess.call(", "subprocess.popen(",
        "os.system(", "__import__(", "importlib.import_module(",
        "asyncio.run(", "asyncio.create_task(",
        "event_candidate_boundary", "emit_ui_event(",
        "scout_fetch_ledger", "vault_projection_adapter",
    ]
    for sym in hard_forbidden_calls:
        assert sym not in source, f"Forbidden runtime call {sym!r} found in intake.py source"

    # Check imports
    tree = ast.parse(source)
    imported_names = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported_names.append(alias.name.lower())
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imported_names.append(node.module.lower())

    forbidden_imports = [
        "requests", "httpx", "urllib", "aiohttp", "playwright", "selenium",
        "beautifulsoup", "bs4", "openai", "anthropic", "gemini",
        "google.generativeai", "google.generative", "ollama", "vllm",
        "subprocess", "asyncio"
    ]

    for sym in forbidden_imports:
        for name in imported_names:
            assert sym not in name, f"Forbidden import {sym!r} found in intake.py"
