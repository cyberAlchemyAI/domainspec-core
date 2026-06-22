#!/usr/bin/env python3
"""
HRR-004 Builder 3 — observability.py
Structured error events, events.jsonl append-only log, T6 telemetry, real-time progress callbacks.
"""

from __future__ import annotations
import json
import uuid
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from enum import Enum
from typing import Optional, Dict, Any, Callable, List
from pathlib import Path


class EventType(Enum):
    SPEC_VIOLATION = "SPEC_VIOLATION"
    PROVIDER_ERROR = "PROVIDER_ERROR"
    ORCHESTRATOR_ERROR = "ORCHESTRATOR_ERROR"
    TIMEOUT = "TIMEOUT"
    WAVE_START = "WAVE_START"
    GATE_EVALUATION = "GATE_EVALUATION"
    WAVE_COMPLETE = "WAVE_COMPLETE"
    HUMAN_ESCALATION_SENT = "HUMAN_ESCALATION_SENT"
    ESCALATION_TIER_ADVANCED = "ESCALATION_TIER_ADVANCED"


@dataclass
class StructuredEvent:
    event_id: str
    event_type: str
    run_id: str
    wave_id: Optional[str]
    gate_id: Optional[str]
    severity: str  # INFO | WARN | ERROR | FATAL
    message: str
    context: Dict[str, Any]
    timestamp: str


class Observability:
    """T6 Telemetry + events.jsonl persistence + progress callbacks."""

    def __init__(self, run_id: str, events_path: Path = Path("events.jsonl")):
        self.run_id = run_id
        self.events_path = events_path
        self.progress_callback: Optional[Callable[[Dict], None]] = None
        self.events: List[StructuredEvent] = []

    def set_progress_callback(self, cb: Callable[[Dict], None]):
        """Real-time progress callback (Discord status updates, etc.)."""
        self.progress_callback = cb

    def emit(self, event_type: EventType, severity: str, message: str,
             wave_id: Optional[str] = None, gate_id: Optional[str] = None,
             context: Optional[Dict] = None) -> StructuredEvent:
        evt = StructuredEvent(
            event_id=str(uuid.uuid4()),
            event_type=event_type.value,
            run_id=self.run_id,
            wave_id=wave_id,
            gate_id=gate_id,
            severity=severity,
            message=message,
            context=context or {},
            timestamp=datetime.now(timezone.utc).replace(tzinfo=None).isoformat() + "Z",
        )
        self.events.append(evt)
        self._append_to_log(evt)

        if self.progress_callback:
            self.progress_callback(asdict(evt))

        return evt

    def _append_to_log(self, evt: StructuredEvent):
        """Append-only events.jsonl persistence."""
        with open(self.events_path, "a") as f:
            f.write(json.dumps(asdict(evt)) + "\n")

    # T6 Telemetry helpers
    def wave_start(self, wave_id: str, wave_name: str):
        self.emit(EventType.WAVE_START, "INFO", f"Wave {wave_id} started: {wave_name}", wave_id=wave_id)

    def gate_evaluation(self, wave_id: str, gate_id: str, result: str, score: float):
        self.emit(EventType.GATE_EVALUATION, "INFO", f"Gate {gate_id} evaluated: {result}",
                  wave_id=wave_id, gate_id=gate_id, context={"result": result, "score": score})

    def wave_complete(self, wave_id: str, status: str, duration_s: float):
        self.emit(EventType.WAVE_COMPLETE, "INFO", f"Wave {wave_id} complete ({status})",
                  wave_id=wave_id, context={"status": status, "duration_s": duration_s})

    def error(self, event_type: EventType, message: str, context: Dict):
        self.emit(event_type, "ERROR", message, context=context)
