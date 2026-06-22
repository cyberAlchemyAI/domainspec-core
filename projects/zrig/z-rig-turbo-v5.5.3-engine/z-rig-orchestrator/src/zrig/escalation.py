#!/usr/bin/env python3
"""
HRR-004 Builder 3 — escalation.py
Human Escalation Protocol (A.8 + A.8.5)
PIPELINE_PAUSED state machine, notification dispatch, timeout cascade, response parsing, resume.
"""

from __future__ import annotations
import json
import uuid
import time
from dataclasses import dataclass, asdict
from datetime import datetime, timezone, timedelta
from enum import Enum
from typing import Optional, Dict, Any, List, Callable
import hashlib
import hmac


class PipelineState(Enum):
    RUNNING = "RUNNING"
    PIPELINE_PAUSED = "PIPELINE_PAUSED"
    PIPELINE_PAUSED_CRITICAL = "PIPELINE_PAUSED_CRITICAL"
    PIPELINE_HALTED = "PIPELINE_HALTED"
    RESUMED = "RESUMED"


class EscalationResponse(Enum):
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    OVERRIDE = "OVERRIDE"
    ABORT = "ABORT"


class EscalationTier(Enum):
    PRIMARY = "PRIMARY"
    SECONDARY = "SECONDARY"
    EMERGENCY = "EMERGENCY"


@dataclass
class EscalationTrigger:
    escalation_id: str
    run_id: str
    trigger_wave: str
    trigger_gate: str
    reason_code: str
    triggering_artifact_ids: List[str]
    triggering_finding_ids: List[str]
    summary: str
    requested_action: str
    created_at: str


@dataclass
class HumanResponse:
    escalation_id: str
    responder: str
    response: str  # APPROVE | REJECT | OVERRIDE | ABORT
    conditions: List[str]
    rationale: str
    responded_at: str


@dataclass
class EscalationContact:
    id: str
    display_name: str
    channels: List[Dict[str, str]]
    availability_window: Optional[Dict] = None


@dataclass
class EscalationConfig:
    primary: EscalationContact
    secondary: Optional[EscalationContact] = None
    emergency_abort: Optional[EscalationContact] = None
    timeouts: Dict[str, int] = None  # ms


class HumanEscalationProtocol:
    """Implements A.8 Human Escalation Protocol + A.8.5 Escalation Chain."""

    def __init__(self, config: EscalationConfig, discord_webhook: Optional[str] = None):
        self.config = config
        self.discord_webhook = discord_webhook
        self.state = PipelineState.RUNNING
        self.current_escalation: Optional[EscalationTrigger] = None
        self.responses: Dict[str, HumanResponse] = {}
        self.notification_log: List[Dict] = []
        self.resume_manifest: Optional[Dict] = None

    def trigger_escalation(self, trigger: EscalationTrigger) -> PipelineState:
        """Enter PIPELINE_PAUSED. Send notifications. Start timers."""
        self.current_escalation = trigger
        self.state = PipelineState.PIPELINE_PAUSED

        self._dispatch_notification(EscalationTier.PRIMARY)
        self._emit_event("HUMAN_ESCALATION_SENT", {"tier": "PRIMARY"})

        # In real impl: schedule timers (primary 4h, secondary 2h, emergency 2h)
        # For this module we record the cascade start time.
        self.cascade_start = time.time()
        return self.state

    def _dispatch_notification(self, tier: EscalationTier):
        """Send structured JSON notification via Discord webhook (or configured channels)."""
        payload = {
            "notification_id": str(uuid.uuid4()),
            "run_id": self.current_escalation.run_id,
            "escalation_id": self.current_escalation.escalation_id,
            "tier": tier.value,
            "wave_blocked": self.current_escalation.trigger_wave,
            "gate_blocked": self.current_escalation.trigger_gate,
            "reason_code": self.current_escalation.reason_code,
            "summary": self.current_escalation.summary,
            "timestamp": datetime.now(timezone.utc).replace(tzinfo=None).isoformat() + "Z",
        }
        self.notification_log.append(payload)

        if self.discord_webhook:
            # Real impl would POST; here we just log the intent
            print(f"[ESCALATION] Would POST to Discord: {json.dumps(payload, indent=2)}")

    def record_human_response(self, response: HumanResponse) -> PipelineState:
        """Parse APPROVED/REJECTED/DEFERRED (mapped to OVERRIDE/ABORT)."""
        self.responses[response.escalation_id] = response

        if response.response == "APPROVE":
            self.state = PipelineState.RESUMED
            self.resume_manifest = {
                "resume_from": self.current_escalation.trigger_gate,
                "human_override": True,
                "response": asdict(response),
            }
        elif response.response == "REJECT":
            self.state = PipelineState.PIPELINE_HALTED
        elif response.response == "ABORT":
            self.state = PipelineState.PIPELINE_HALTED
        elif response.response == "OVERRIDE":
            self.state = PipelineState.RESUMED
            self.resume_manifest = {
                "resume_from": self.current_escalation.trigger_gate,
                "override": True,
                "response": asdict(response),
            }
        return self.state

    def advance_timeout_cascade(self) -> PipelineState:
        """Simulate timeout progression (primary → secondary → emergency → auto-abort)."""
        if self.state not in (PipelineState.PIPELINE_PAUSED, PipelineState.PIPELINE_PAUSED_CRITICAL):
            return self.state

        elapsed = time.time() - self.cascade_start
        primary_ms = self.config.timeouts.get("primary_ms", 14400000) / 1000
        secondary_ms = self.config.timeouts.get("secondary_ms", 7200000) / 1000

        if elapsed > primary_ms + secondary_ms + 7200:  # emergency exhausted
            self._emit_event("ESCALATION_EXHAUSTED", {})
            self.state = PipelineState.PIPELINE_HALTED
            self.resume_manifest = {"halt_reason": "ESCALATION_EXHAUSTED"}
        elif elapsed > primary_ms + secondary_ms:
            self.state = PipelineState.PIPELINE_PAUSED_CRITICAL
            self._dispatch_notification(EscalationTier.EMERGENCY)
        elif elapsed > primary_ms:
            self._dispatch_notification(EscalationTier.SECONDARY)
            self._emit_event("ESCALATION_TIER_ADVANCED", {"from": "PRIMARY", "to": "SECONDARY"})

        return self.state

    def _emit_event(self, event_type: str, data: Dict):
        self.notification_log.append({"event": event_type, "data": data, "ts": datetime.now(timezone.utc).replace(tzinfo=None).isoformat()})

    def get_resume_manifest(self) -> Optional[Dict]:
        return self.resume_manifest


# Convenience factory for tests
def create_default_escalation_config() -> EscalationConfig:
    primary = EscalationContact(
        id="op-primary",
        display_name="Primary Operator",
        channels=[{"type": "discord", "endpoint": "https://discord.webhook.example"}],
    )
    secondary = EscalationContact(
        id="op-secondary",
        display_name="Secondary Operator",
        channels=[{"type": "discord", "endpoint": "https://discord.webhook.secondary"}],
    )
    return EscalationConfig(
        primary=primary,
        secondary=secondary,
        timeouts={"primary_ms": 14400000, "secondary_ms": 7200000, "emergency_ms": 7200000},
    )
