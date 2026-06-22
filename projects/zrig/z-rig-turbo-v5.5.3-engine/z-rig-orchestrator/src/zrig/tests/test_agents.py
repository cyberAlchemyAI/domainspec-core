#!/usr/bin/env python3
"""
HRR-005 Builder 3 — tests/test_agents.py

Mock tests for both execution modes:
  - Embedded mode via openclaw_bridge (file protocol)
  - Standalone mode via gateway_client (HTTP)
"""

from __future__ import annotations

import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from zrig.agents import SeatAssignment, StubAgentRunner, wrap_in_envelope
from zrig.openclaw_bridge import (
    WaveDispatchRequest,
    write_dispatch_request,
    wait_for_wave_output,
    get_output_dir,
)
from zrig.gateway_client import OpenClawGatewayClient, GatewayConfig


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def sample_seat():
    return SeatAssignment(
        seat_id="W2_builder_1_abc123",
        wave="W2",
        role="builder_1",
        model_requested="grok-4",
        model_actual="grok-4",
        family_actual="xai",
        agent_isolation_id="agent_1234-5678",
    )


@pytest.fixture
def sample_bundle():
    return {"bundle_id": "B-001", "payload": {"task": "build something"}}


# ---------------------------------------------------------------------------
# Stub / embedded mode tests
# ---------------------------------------------------------------------------

def test_stub_runner_returns_envelope(sample_seat, sample_bundle):
    runner = StubAgentRunner(synthetic_payloads={"W2": {"status": "ok"}})
    import asyncio
    result = asyncio.run(runner(sample_seat, sample_bundle, "grok-4"))

    assert result["payload"]["status"] == "ok"
    assert result["agent_isolation_id"] == sample_seat.agent_isolation_id
    assert result["envelope_version"] == "5.5.2"


def test_stub_runner_fail_on_model(sample_seat, sample_bundle):
    runner = StubAgentRunner(fail_on_models=["gpt-4"])
    import asyncio
    with pytest.raises(Exception):
        asyncio.run(runner(sample_seat, sample_bundle, "gpt-4"))


# ---------------------------------------------------------------------------
# openclaw_bridge protocol tests
# ---------------------------------------------------------------------------

def test_write_dispatch_request_creates_file(sample_seat):
    with tempfile.TemporaryDirectory() as tmp:
        wave_dir = Path(tmp) / "wave2"
        req = WaveDispatchRequest(
            request_id="req-001",
            run_id="HRR-005",
            wave="W2",
            seats=[sample_seat.__dict__],
            bundles=[{"payload": "test"}],
            timeout_ms=3_600_000,
            created_at="2026-06-16T00:00:00Z",
        )
        path = write_dispatch_request(wave_dir, req)
        assert path.exists()
        data = json.loads(path.read_text())
        assert data["wave"] == "W2"
        assert data["protocol_version"] == "1.0"


def test_wait_for_wave_output_falls_back_to_individual_files(sample_seat):
    with tempfile.TemporaryDirectory() as tmp:
        wave_dir = Path(tmp) / "wave2"
        output_dir = get_output_dir(wave_dir)
        output_dir.mkdir(parents=True)

        # Write one agent output
        out_path = output_dir / f"{sample_seat.agent_isolation_id}.json"
        envelope = wrap_in_envelope({"result": "success"}, sample_seat)
        out_path.write_text(json.dumps(envelope))

        manifest = wait_for_wave_output(
            wave_dir,
            expected_agent_ids=[sample_seat.agent_isolation_id],
            poll_interval_s=0.1,
            max_wait_s=2.0,
        )
        assert manifest.successful_count == 1
        assert manifest.outputs[0]["payload"]["result"] == "success"


# ---------------------------------------------------------------------------
# gateway_client mock tests (standalone mode)
# ---------------------------------------------------------------------------

def test_gateway_client_spawn_and_wait():
    cfg = GatewayConfig(base_url="http://localhost:18789", token="test-token")
    client = OpenClawGatewayClient(cfg)

    with patch.object(client._client, "post") as mock_post, \
         patch.object(client._client, "get") as mock_get:

        mock_post.return_value.json.return_value = {"session_id": "sess_123"}
        mock_post.return_value.raise_for_status = lambda: None

        mock_get.side_effect = [
            MagicMock(json=lambda: {"status": "RUNNING"}, raise_for_status=lambda: None),
            MagicMock(json=lambda: {"status": "COMPLETED"}, raise_for_status=lambda: None),
            MagicMock(json=lambda: {"payload": {"ok": True}}, raise_for_status=lambda: None),
        ]

        result = client.spawn_and_wait(model="grok-4", task="do work")

        assert result["payload"]["ok"] is True
        mock_post.assert_called_once()
        assert mock_get.call_count == 3
