#!/usr/bin/env python3
"""Tests for escalation.py — Human Escalation Protocol."""

import pytest
from pathlib import Path
from zrig.escalation import (
    HumanEscalationProtocol, EscalationTrigger, HumanResponse,
    create_default_escalation_config, PipelineState, EscalationTier
)


def test_trigger_escalation_enters_paused_state():
    config = create_default_escalation_config()
    proto = HumanEscalationProtocol(config)
    trigger = EscalationTrigger(
        escalation_id="esc-001", run_id="HRR-004", trigger_wave="W5",
        trigger_gate="G5.2", reason_code="CRITICAL_FINDING",
        triggering_artifact_ids=[], triggering_finding_ids=[],
        summary="Test escalation", requested_action="REVIEW_AND_DECIDE",
        created_at="2026-06-16T12:00:00Z"
    )
    state = proto.trigger_escalation(trigger)
    assert state == PipelineState.PIPELINE_PAUSED
    assert proto.current_escalation is not None


def test_record_approve_resumes_with_override():
    config = create_default_escalation_config()
    proto = HumanEscalationProtocol(config)
    trigger = EscalationTrigger("esc-002", "HRR-004", "W7", "G7.1", "OPERATOR_OVERRIDE", [], [], "Test", "REVIEW", "2026-06-16T12:00:00Z")
    proto.trigger_escalation(trigger)

    resp = HumanResponse("esc-002", "dr.tom", "APPROVE", [], "Looks good", "2026-06-16T12:05:00Z")
    state = proto.record_human_response(resp)
    assert state == PipelineState.RESUMED
    manifest = proto.get_resume_manifest()
    assert manifest["human_override"] is True


def test_timeout_cascade_advances_tiers():
    config = create_default_escalation_config()
    proto = HumanEscalationProtocol(config)
    trigger = EscalationTrigger("esc-003", "HRR-004", "W9", "G9.3", "TIMEOUT_VERIFICATION", [], [], "Test", "REVIEW", "2026-06-16T12:00:00Z")
    proto.trigger_escalation(trigger)
    # Force immediate cascade advance for test
    proto.cascade_start = proto.cascade_start - 20000  # simulate >4h elapsed
    state = proto.advance_timeout_cascade()
    assert state in (PipelineState.PIPELINE_PAUSED, PipelineState.PIPELINE_PAUSED_CRITICAL)
