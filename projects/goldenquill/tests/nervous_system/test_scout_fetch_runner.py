import pytest
import importlib
import ast
import os
from pathlib import Path

from pipeline.nervous_system.scout_fetch_runner import GovernedFetchRunner
from pipeline.nervous_system.scout_source_roster import SourceStatus
from pipeline.nervous_system.scout_fetch_ledger import FetchMethod

def test_unknown_source_id_fails_closed():
    record = GovernedFetchRunner.run_fetch_for_source("invalid_id_999", "fetch_1", "2026-05-27T00:00:00Z")
    assert record.result_status == SourceStatus.failed_validation
    assert record.content_hash is None
    assert "Unknown source ID" in record.error_message

def test_disabled_source_does_not_fetch(monkeypatch):
    from pipeline.nervous_system.scout_source_roster import SourceRecord, SourceType

    def mock_list_configured_sources():
        return [
            SourceRecord(
                source_id="test_disabled_1",
                name="Test Disabled",
                source_type=SourceType.manual_seed,
                source_status=SourceStatus.source_not_configured,
                enabled=False
            )
        ]

    monkeypatch.setattr("pipeline.nervous_system.scout_fetch_runner.list_configured_sources", mock_list_configured_sources)
    record = GovernedFetchRunner.run_fetch_for_source("test_disabled_1", "fetch_2", "2026-05-27T00:00:00Z")
    assert record.result_status == SourceStatus.blocked
    assert record.content_hash is None
    assert "explicitly disabled" in record.error_message

def test_unsupported_retrieval_method_fails_closed(monkeypatch):
    from pipeline.nervous_system.scout_source_roster import SourceRecord, SourceType

    def mock_list_configured_sources():
        return [
            SourceRecord(
                source_id="test_api_1",
                name="Test API",
                source_type=SourceType.api,
                source_status=SourceStatus.verified,
                enabled=True
            )
        ]

    monkeypatch.setattr("pipeline.nervous_system.scout_fetch_runner.list_configured_sources", mock_list_configured_sources)
    record = GovernedFetchRunner.run_fetch_for_source("test_api_1", "fetch_3", "2026-05-27T00:00:00Z")
    assert record.result_status == SourceStatus.not_implemented
    assert record.content_hash is None
    assert "Network retrieval methods are not implemented" in record.error_message

def test_successful_deterministic_retrieval_writes_hash(monkeypatch):
    from pipeline.nervous_system.scout_source_roster import SourceRecord, SourceType

    def mock_list_configured_sources():
        return [
            SourceRecord(
                source_id="test_manual_1",
                name="Test Manual",
                source_type=SourceType.manual_seed,
                source_status=SourceStatus.verified,
                enabled=True
            )
        ]

    monkeypatch.setattr("pipeline.nervous_system.scout_fetch_runner.list_configured_sources", mock_list_configured_sources)
    record = GovernedFetchRunner.run_fetch_for_source("test_manual_1", "fetch_4", "2026-05-27T00:00:00Z")

    assert record.result_status == SourceStatus.verified
    assert record.content_hash is not None
    assert record.snapshot_path is not None
    assert record.error_message is None

def test_failed_retrieval_writes_without_hash(monkeypatch, tmp_path):
    from pipeline.nervous_system.scout_source_roster import SourceRecord, SourceType

    def mock_list_configured_sources():
        return [
            SourceRecord(
                source_id="test_manual_fail",
                name="Test Manual Fail",
                source_type=SourceType.manual_seed,
                source_status=SourceStatus.verified,
                enabled=True
            )
        ]

    monkeypatch.setattr("pipeline.nervous_system.scout_fetch_runner.list_configured_sources", mock_list_configured_sources)
    # Monkeypatch os.path.join to return a non-existent file
    def mock_join(*args):
        return "/non/existent/path/for/sure/DEMO_DATA.json"

    monkeypatch.setattr("os.path.join", mock_join)

    record = GovernedFetchRunner.run_fetch_for_source("test_manual_fail", "fetch_5", "2026-05-27T00:00:00Z")

    assert record.result_status == SourceStatus.unavailable
    assert record.content_hash is None
    assert "No such file or directory" in record.error_message

def test_zero_forbidden_imports_in_fetch_runner():
    file_path = Path(__file__).parent.parent.parent / "pipeline" / "nervous_system" / "scout_fetch_runner.py"
    with open(file_path, "r") as f:
        tree = ast.parse(f.read())

    forbidden_imports = {
        "requests", "httpx", "urllib", "aiohttp", "playwright", "selenium",
        "bs4", "BeautifulSoup", "openai", "anthropic", "gemini",
        "google.generative", "ollama", "vllm"
    }

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name not in forbidden_imports, f"Forbidden import found: {alias.name}"
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                assert node.module not in forbidden_imports, f"Forbidden import found: {node.module}"

def test_zero_autonomous_url_discovery():
    file_path = Path(__file__).parent.parent.parent / "pipeline" / "nervous_system" / "scout_fetch_runner.py"
    with open(file_path, "r") as f:
        content = f.read().lower()

    forbidden_terms = ["crawl", "scrape", "search", "discover", "explore", "webdriver"]
    for term in forbidden_terms:
        assert term not in content, f"Forbidden autonomous discovery term found: {term}"
