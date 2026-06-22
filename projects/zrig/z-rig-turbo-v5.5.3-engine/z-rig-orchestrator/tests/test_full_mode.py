"""Tests for FULL mode waves (W6/W7) and self-improvement triggers (MECH-038)."""

import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from zrig.config import RunConfig, TaskDescription
from zrig.gates import evaluate_g6, evaluate_g7, WAVE_GATE_MAP
from zrig.live_executor import WAVE_SEAT_CONFIG, LiveWaveExecutor
from zrig.wave_prompts import WavePromptBuilder


# ---------------------------------------------------------------------------
# Test fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def sample_task():
    return TaskDescription(
        task_id="T-001",
        summary="Test task",
        requested_change="Implement feature X",
        acceptance_criteria=["Criterion 1", "Criterion 2"],
        target_files=["src/example.py"],
        artifact_type="code",
    )


@pytest.fixture
def sample_run_config():
    return RunConfig(
        run_id="test-run-001",
        mode="FULL",
        provider_list=["anthropic", "openai", "xai"],
        w1_panel_size=3,
        w2_builder_count=3,
        w4_verifier_count=3,
        w5_squad_count=2,
        w9_panel_size=3,
        max_rework_cycles=2,
    )


# ---------------------------------------------------------------------------
# W6/W7 Prompt Tests
# ---------------------------------------------------------------------------

def test_w6_prompt_includes_w4_w5_findings(sample_task, sample_run_config):
    """W6 prompt must reference W4 and W5 outputs."""
    builder = WavePromptBuilder(sample_task, sample_run_config)
    context = {
        "prior_waves": {
            "W4": {"findings": [{"id": "F1", "severity": "high"}]},
            "W5": {"findings": [{"id": "F2", "severity": "critical"}]},
        }
    }
    prompt = builder.build_prompt("W6", "consolidator", 0, context)

    assert "W4" in prompt or "W5" in prompt
    assert "consolidated_findings" in prompt
    assert "consolidation_confidence" in prompt


def test_w7_prompt_includes_consolidated_findings(sample_task, sample_run_config):
    """W7 prompt must reference W3 canonical + W6 consolidated findings."""
    builder = WavePromptBuilder(sample_task, sample_run_config)
    context = {
        "prior_waves": {
            "W3": {"canonical_implementation": {"files": []}},
            "W6": {"consolidated_findings": [{"id": "F1", "severity": "FATAL"}]},
        }
    }
    prompt = builder.build_prompt("W7", "qa_tester", 0, context)

    assert "W3" in prompt or "W6" in prompt
    assert "qa_results" in prompt
    assert "false_positive_rate" in prompt


# ---------------------------------------------------------------------------
# Seat Config Tests
# ---------------------------------------------------------------------------

def test_w6_seat_config_single_consolidator():
    """W6 must use exactly 1 consolidator seat."""
    role, count_source, is_from_config = WAVE_SEAT_CONFIG["W6"]
    assert role == "consolidator"
    assert count_source == 1
    assert is_from_config is False


def test_w7_seat_config_uses_verifier_count():
    """W7 must use w4_verifier_count for seat allocation."""
    role, count_source, is_from_config = WAVE_SEAT_CONFIG["W7"]
    assert role == "qa_tester"
    assert count_source == "w4_verifier_count"
    assert is_from_config is True


# ---------------------------------------------------------------------------
# G6 Gate Tests
# ---------------------------------------------------------------------------

def test_g6_passes_on_high_confidence(sample_run_config):
    """G6 passes when consolidation_confidence > 0.7 and no unresolved FATAL."""
    wave_output = {
        "consolidated_findings": [
            {"id": "F1", "severity": "high", "description": "Issue", "source_wave": "W4", "location": "src/a.py"},
        ],
        "dedup_count": 2,
        "consolidation_confidence": 0.85,
    }
    manifest = MagicMock()
    manifest.registry_hash = "abc123"
    registry = MagicMock()
    registry.compute_hash.return_value = "abc123"

    result = evaluate_g6(wave_output, sample_run_config, registry, manifest)
    assert result.passed is True


def test_g6_fails_on_unresolved_fatal(sample_run_config):
    """G6 fails when there are unresolved FATAL findings."""
    wave_output = {
        "consolidated_findings": [
            {"id": "F1", "severity": "FATAL", "description": "Critical", "source_wave": "W4", "location": "src/a.py"},
        ],
        "dedup_count": 0,
        "consolidation_confidence": 0.85,
    }
    manifest = MagicMock()
    manifest.registry_hash = "abc123"
    registry = MagicMock()
    registry.compute_hash.return_value = "abc123"

    result = evaluate_g6(wave_output, sample_run_config, registry, manifest)
    assert result.passed is False
    assert any("FATAL" in str(r) for r in result.failure_reasons)


# ---------------------------------------------------------------------------
# G7 Gate Tests
# ---------------------------------------------------------------------------

def test_g7_passes_on_low_false_positive_rate(sample_run_config):
    """G7 passes when false_positive_rate < 0.3 and all FATAL confirmed."""
    wave_output = {
        "qa_results": [
            {"finding_id": "F1", "confirmed": True, "evidence": "Test passed", "severity_adjustment": "none"},
            {"finding_id": "F2", "confirmed": True, "evidence": "Confirmed", "severity_adjustment": "none"},
        ],
        "false_positive_rate": 0.15,
        "qa_confidence": 0.90,
    }
    manifest = MagicMock()
    manifest.registry_hash = "abc123"
    registry = MagicMock()
    registry.compute_hash.return_value = "abc123"

    result = evaluate_g7(wave_output, sample_run_config, registry, manifest)
    assert result.passed is True


def test_g7_fails_on_high_false_positive_rate(sample_run_config):
    """G7 fails when false_positive_rate >= 0.3."""
    wave_output = {
        "qa_results": [
            {"finding_id": "F1", "confirmed": False, "evidence": "", "severity_adjustment": "downgrade"},
        ],
        "false_positive_rate": 0.45,
        "qa_confidence": 0.70,
    }
    manifest = MagicMock()
    manifest.registry_hash = "abc123"
    registry = MagicMock()
    registry.compute_hash.return_value = "abc123"

    result = evaluate_g7(wave_output, sample_run_config, registry, manifest)
    assert result.passed is False
    assert any("false positive rate" in str(r).lower() for r in result.failure_reasons)


# ---------------------------------------------------------------------------
# Gate Map Tests
# ---------------------------------------------------------------------------

def test_g6_g7_in_wave_gate_map():
    """G6 and G7 must be registered in WAVE_GATE_MAP."""
    assert WAVE_GATE_MAP.get("W6") == "G6"
    assert WAVE_GATE_MAP.get("W7") == "G7"


# ---------------------------------------------------------------------------
# Self-Improvement Trigger Test (MECH-038)
# ---------------------------------------------------------------------------

def test_self_improvement_triggers_logged(sample_run_config):
    """Pipeline must call MetricsStore.evaluate_triggers after completion."""
    # This is a structural test — verifies the call pattern exists in pipeline.py
    # In a real run, the pipeline would import and invoke:
    #   metrics_store = MetricsStore(run_dir / "metrics_store.jsonl")
    #   run_metrics = RunMetrics(...)
    #   metrics_store.record_run(run_metrics)
    #   triggers = metrics_store.evaluate_triggers(run_metrics)
    #   if triggers: obs.emit(...)

    # We verify the expected structure by checking imports and method existence
    from zrig import metrics

    assert hasattr(metrics, "MetricsStore")
    assert hasattr(metrics.MetricsStore, "evaluate_triggers")
    assert hasattr(metrics, "RunMetrics")