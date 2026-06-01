"""
Tests for pipeline.nervous_system.funder_terrain.intake

Coverage:
1. Successful local JSON intake.
2. Deterministic output / stable hashes across repeated runs.
3. Missing file rejection.
4. Non-Path input rejection.
5. Remote-looking source/path rejection.
6. Forbidden source_type / source_id term rejection.
7. Malformed JSON rejection.
8. Provenance propagation: source_id, source_type, input hash, record hash.
9. Human-review fallback for incomplete/ambiguous metadata.
10. Static import poison pill: intake.py must not import network, LLM, subprocess,
    async, candidate, partner-alert, Scout projection, UI, export, or submission symbols.
"""

import ast
import inspect
import json
import textwrap
from pathlib import Path

import pytest

from pipeline.nervous_system.funder_terrain.intake import (
    CURATED_LOCAL_SOURCE_TYPE,
    intake_curated_funder_terrain_file,
)
from pipeline.nervous_system.funder_terrain.models import FunderTerrainNormalizedRecord


# ---------------------------------------------------------------------------
# Helpers / fixtures
# ---------------------------------------------------------------------------

def _write_json(tmp_path: Path, data: dict, filename: str = "record.json") -> Path:
    p = tmp_path / filename
    p.write_text(json.dumps(data), encoding="utf-8")
    return p


def _write_yaml(tmp_path: Path, data: str, filename: str = "record.yaml") -> Path:
    p = tmp_path / filename
    p.write_text(data, encoding="utf-8")
    return p


_MINIMAL_USDA_RECORD = {
    "funder_name": "USDA",
    "program_name": "Organic Transition Initiative",
    "document_type": "Guidelines",
    "geography": "Vermont",
    "notes": "Annual cycle, letters of inquiry due in spring.",
}

_MINIMAL_AMBIGUOUS_RECORD = {
    "notes": "Some funder we heard about but have no details for.",
}


# ---------------------------------------------------------------------------
# 1. Successful local JSON intake
# ---------------------------------------------------------------------------

def test_successful_json_intake(tmp_path):
    p = _write_json(tmp_path, _MINIMAL_USDA_RECORD)
    result = intake_curated_funder_terrain_file(p)
    assert isinstance(result, FunderTerrainNormalizedRecord)
    assert result.record_id is not None
    assert result.source_provenance is not None
    assert result.source_provenance.source_type == CURATED_LOCAL_SOURCE_TYPE


# ---------------------------------------------------------------------------
# 2. Successful local YAML intake
# ---------------------------------------------------------------------------

def test_successful_yaml_intake(tmp_path):
    yaml_content = textwrap.dedent("""\
        funder_name: USDA
        program_name: Organic Transition Initiative
        document_type: Guidelines
        geography: Vermont
    """)
    p = _write_yaml(tmp_path, yaml_content)
    result = intake_curated_funder_terrain_file(p)
    assert isinstance(result, FunderTerrainNormalizedRecord)
    assert result.source_provenance.source_type == CURATED_LOCAL_SOURCE_TYPE


# ---------------------------------------------------------------------------
# 3. Deterministic output / stable hashes across repeated runs
# ---------------------------------------------------------------------------

def test_deterministic_output(tmp_path):
    p = _write_json(tmp_path, _MINIMAL_USDA_RECORD, filename="usda.json")
    r1 = intake_curated_funder_terrain_file(p, source_id="test_stable_src")
    r2 = intake_curated_funder_terrain_file(p, source_id="test_stable_src")
    assert r1.record_id == r2.record_id
    assert r1.normalization_input_sha256 == r2.normalization_input_sha256
    assert r1.ruleset_sha256 == r2.ruleset_sha256
    assert r1.record_sha256 == r2.record_sha256


# ---------------------------------------------------------------------------
# 4. Missing file rejection
# ---------------------------------------------------------------------------

def test_missing_file_rejection(tmp_path):
    nonexistent = tmp_path / "does_not_exist.json"
    with pytest.raises(FileNotFoundError):
        intake_curated_funder_terrain_file(nonexistent)


# ---------------------------------------------------------------------------
# 5. Non-Path input rejection
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("bad_input", [
    "/some/path/record.json",
    b"/some/path/record.json",
    None,
    42,
    {"path": "/some/path"},
])
def test_non_path_input_rejection(bad_input):
    with pytest.raises(TypeError):
        intake_curated_funder_terrain_file(bad_input)


# ---------------------------------------------------------------------------
# 6. Remote-looking path rejection
# ---------------------------------------------------------------------------

def test_remote_http_path_rejection(tmp_path):
    # We can't construct a Path that starts with http://, but we verify the guard
    # via source_id and by confirming the validator catches URI-scheme-looking strings.
    # The path guard fires on str-prefixed remote URIs; for absolute local paths we confirm
    # normal local paths pass validation.
    local = _write_json(tmp_path, _MINIMAL_USDA_RECORD)
    # source_id containing "http" must be rejected
    with pytest.raises(ValueError, match="Forbidden term"):
        intake_curated_funder_terrain_file(local, source_id="http_source_id")


# ---------------------------------------------------------------------------
# 7. Forbidden source_id term rejection (all forbidden terms)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("forbidden_term", [
    "http", "https", "api", "web", "url", "scrape", "crawler",
    "llm", "model", "candidate", "partner_alert",
])
def test_forbidden_source_id_term_rejection(tmp_path, forbidden_term):
    p = _write_json(tmp_path, _MINIMAL_USDA_RECORD)
    with pytest.raises(ValueError, match="Forbidden term"):
        intake_curated_funder_terrain_file(p, source_id=f"my_{forbidden_term}_source")


# ---------------------------------------------------------------------------
# 8. Empty source_id rejection
# ---------------------------------------------------------------------------

def test_empty_source_id_rejection(tmp_path):
    p = _write_json(tmp_path, _MINIMAL_USDA_RECORD)
    with pytest.raises(ValueError):
        intake_curated_funder_terrain_file(p, source_id="")
    with pytest.raises(ValueError):
        intake_curated_funder_terrain_file(p, source_id="   ")


# ---------------------------------------------------------------------------
# 9. Malformed JSON rejection
# ---------------------------------------------------------------------------

def test_malformed_json_rejection(tmp_path):
    p = tmp_path / "bad.json"
    p.write_text("{this is not json", encoding="utf-8")
    with pytest.raises(ValueError, match="Malformed JSON"):
        intake_curated_funder_terrain_file(p)


# ---------------------------------------------------------------------------
# 10. Malformed YAML rejection
# ---------------------------------------------------------------------------

def test_malformed_yaml_rejection(tmp_path):
    p = tmp_path / "bad.yaml"
    p.write_text("key: [\nunclosed", encoding="utf-8")
    with pytest.raises(ValueError, match="Malformed YAML"):
        intake_curated_funder_terrain_file(p)


# ---------------------------------------------------------------------------
# 11. Non-dict top-level JSON rejected
# ---------------------------------------------------------------------------

def test_non_dict_json_rejection(tmp_path):
    p = tmp_path / "list.json"
    p.write_text(json.dumps(["item1", "item2"]), encoding="utf-8")
    with pytest.raises(ValueError, match="JSON object"):
        intake_curated_funder_terrain_file(p)


# ---------------------------------------------------------------------------
# 12. Unsupported file extension rejection
# ---------------------------------------------------------------------------

def test_unsupported_extension_rejection(tmp_path):
    p = tmp_path / "record.txt"
    p.write_text("some text", encoding="utf-8")
    with pytest.raises(ValueError, match="Unsupported file extension"):
        intake_curated_funder_terrain_file(p)


# ---------------------------------------------------------------------------
# 13. Provenance propagation: source_id, source_type, input hash, record hash
# ---------------------------------------------------------------------------

def test_provenance_propagation(tmp_path):
    p = _write_json(tmp_path, _MINIMAL_USDA_RECORD)
    my_source_id = "org_usda_curated_2026"
    result = intake_curated_funder_terrain_file(p, source_id=my_source_id)

    # source_id must be reflected in provenance
    assert result.source_provenance.source_id == my_source_id

    # source_type must always be the offline literal
    assert result.source_provenance.source_type == CURATED_LOCAL_SOURCE_TYPE

    # url_or_local_path must be the resolved local path (not a URL)
    local_path_str = result.source_provenance.url_or_local_path
    assert local_path_str is not None
    assert "http" not in local_path_str.lower()
    assert str(p.resolve()) == local_path_str

    # input hash must be a non-empty hex string
    assert len(result.normalization_input_sha256) == 64
    assert all(c in "0123456789abcdef" for c in result.normalization_input_sha256)

    # record hash must be a non-empty hex string
    assert result.record_sha256 is not None
    assert len(result.record_sha256) == 64


# ---------------------------------------------------------------------------
# 14. Human-review fallback for incomplete/ambiguous metadata
# ---------------------------------------------------------------------------

def test_human_review_fallback_ambiguous_record(tmp_path):
    p = _write_json(tmp_path, _MINIMAL_AMBIGUOUS_RECORD)
    result = intake_curated_funder_terrain_file(p)
    assert result.review_status.human_review_required is True
    assert len(result.metadata_gaps.missing_fields) > 0


# ---------------------------------------------------------------------------
# 15. Output dir write produces deterministic JSON
# ---------------------------------------------------------------------------

def test_output_dir_write(tmp_path):
    input_dir = tmp_path / "input"
    input_dir.mkdir(parents=True, exist_ok=True)
    out_dir = tmp_path / "output"
    out_dir.mkdir(parents=True, exist_ok=True)

    p = _write_json(input_dir, _MINIMAL_USDA_RECORD, filename="usda.json")

    result = intake_curated_funder_terrain_file(p, source_id="write_test_src", output_dir=out_dir)
    out_file = out_dir / f"{result.record_id}.json"
    assert out_file.exists()
    loaded = json.loads(out_file.read_text(encoding="utf-8"))
    assert loaded["record_id"] == result.record_id


# ---------------------------------------------------------------------------
# 16. output_dir non-Path rejection
# ---------------------------------------------------------------------------

def test_output_dir_non_path_rejection(tmp_path):
    p = _write_json(tmp_path, _MINIMAL_USDA_RECORD)
    with pytest.raises(TypeError):
        intake_curated_funder_terrain_file(p, output_dir="/tmp/some/dir")


# ---------------------------------------------------------------------------
# 17. output_dir missing directory rejection
# ---------------------------------------------------------------------------

def test_output_dir_missing_rejection(tmp_path):
    p = _write_json(tmp_path, _MINIMAL_USDA_RECORD)
    with pytest.raises(FileNotFoundError):
        intake_curated_funder_terrain_file(p, output_dir=tmp_path / "nonexistent_dir")


# ---------------------------------------------------------------------------
# 18. Static import poison pill — intake.py must not contain forbidden symbols
# ---------------------------------------------------------------------------

FORBIDDEN_INTAKE_SYMBOLS = [
    # Network
    "requests", "httpx", "urllib", "aiohttp", "playwright", "selenium",
    "BeautifulSoup", "bs4",
    # LLM / model providers
    "openai", "anthropic", "gemini", "google.generativeai", "google.generative",
    "ollama", "vllm",
    # System / shell
    "subprocess", "os.system",
    # Eval / exec
    # NOTE: These appear below as strings-in-strings only; we scan the AST import nodes.
    # Async
    "asyncio",
    # Boundary-crossing
    "event_candidate_boundary",
    "partner_alert",
    "emit_ui_event",
    # Scout live projections / candidate pipeline
    "scout_fetch_ledger", "vault_projection_adapter", "stub_projection_adapter",
    # Drafting / export / submission
    "draft", "export", "submit", "submission",
    # Scraping
    "scrape", "crawler",
]


def test_intake_module_static_import_poison_pill():
    """
    Parse intake.py as an AST and assert none of the forbidden symbols
    appear in import statements.
    """
    intake_path = Path(__file__).resolve().parent.parent.parent / \
        "pipeline" / "nervous_system" / "funder_terrain" / "intake.py"
    assert intake_path.exists(), f"intake.py not found at {intake_path}"
    source = intake_path.read_text(encoding="utf-8")
    tree = ast.parse(source)

    imported_names = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported_names.append(alias.name.lower())
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imported_names.append(node.module.lower())

    for symbol in FORBIDDEN_INTAKE_SYMBOLS:
        sym_lower = symbol.lower()
        for name in imported_names:
            assert sym_lower not in name, (
                f"Forbidden symbol {symbol!r} found in import {name!r} in intake.py"
            )


def test_intake_module_no_forbidden_top_level_strings():
    """
    Scan the raw source of intake.py for forbidden *runtime call* symbols that
    cannot be caught purely by AST import analysis (e.g., dynamic __import__ calls).

    NOTE: intake.py legitimately declares a frozenset of rejection-term strings
    (e.g., "partner_alert", "candidate") as data constants used to validate caller
    input.  The scan below targets *runtime call patterns*, not bare string literals.
    """
    intake_path = Path(__file__).resolve().parent.parent.parent / \
        "pipeline" / "nervous_system" / "funder_terrain" / "intake.py"
    source = intake_path.read_text(encoding="utf-8").lower()

    # These are *call-site* patterns — they indicate active invocation of a
    # forbidden capability, not mere mention of a term in a data constant.
    hard_forbidden_calls = [
        "requests.get(", "requests.post(", "httpx.", "aiohttp.",
        "subprocess.run(", "subprocess.call(", "subprocess.popen(",
        "os.system(", "__import__(", "importlib.import_module(",
        "asyncio.run(", "asyncio.create_task(",
        "event_candidate_boundary", "emit_ui_event(",
        "scout_fetch_ledger", "vault_projection_adapter",
    ]
    for sym in hard_forbidden_calls:
        assert sym not in source, (
            f"Forbidden runtime call {sym!r} found in intake.py source"
        )
