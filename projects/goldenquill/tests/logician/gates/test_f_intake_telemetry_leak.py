"""F-INTAKE-TELEMETRY-LEAK tests (M1 §8.4)."""

from __future__ import annotations

import os

from pipeline.cli.tilth_intake import (
    LOGFIRE_DISABLED_ENV,
    LOGFIRE_DISABLED_VALUE,
)
from pipeline.logician.gates.f_intake_telemetry_leak import (
    F_INTAKE_TELEMETRY_LEAK,
    check_intake_telemetry_leak,
)


def test_failure_code_constant() -> None:
    assert F_INTAKE_TELEMETRY_LEAK == "F-INTAKE-TELEMETRY-LEAK"


def test_clean_cli_entry_passes(monkeypatch) -> None:
    monkeypatch.setenv(LOGFIRE_DISABLED_ENV, LOGFIRE_DISABLED_VALUE)
    r = check_intake_telemetry_leak(cli_entry=True)
    assert r.success is True


def test_cli_entry_with_logfire_enabled_fails(monkeypatch) -> None:
    monkeypatch.setenv(LOGFIRE_DISABLED_ENV, "1")
    r = check_intake_telemetry_leak(cli_entry=True)
    assert r.success is False
    assert r.failure_code == F_INTAKE_TELEMETRY_LEAK


def test_event_with_source_quote_fails() -> None:
    events = [{
        "tool": "intake",
        "source_quote": "the operator's confidential value",
        "endpoint": "https://logfire.pydantic.dev",
    }]
    r = check_intake_telemetry_leak(intake_tool_call_events=events)
    assert r.success is False
    assert r.severity == "HIGH"  # non-local endpoint


def test_event_with_source_quote_local_endpoint_fails_low() -> None:
    events = [{
        "tool": "intake",
        "source_quote": "value",
        "endpoint": "file:///tmp/local-logfire.jsonl",
    }]
    r = check_intake_telemetry_leak(intake_tool_call_events=events)
    assert r.success is False
    assert r.severity == "LOW"


def test_event_with_classification_confidential_fails() -> None:
    events = [{
        "tool": "intake",
        "fields": [{"name": "ein", "classification": "confidential"}],
        "endpoint": "https://logfire.pydantic.dev",
    }]
    r = check_intake_telemetry_leak(intake_tool_call_events=events)
    assert r.success is False


def test_clean_event_passes() -> None:
    events = [{
        "tool": "intake",
        "operation": "bulk_ingest",
        "endpoint": "file:///tmp/ok.jsonl",
    }]
    r = check_intake_telemetry_leak(intake_tool_call_events=events)
    assert r.success is True


def test_classification_map_confidential_fails() -> None:
    events = [{
        "tool": "intake",
        "classifications": {"value": "confidential"},
        "endpoint": "https://logfire.pydantic.dev",
    }]
    r = check_intake_telemetry_leak(intake_tool_call_events=events)
    assert r.success is False
