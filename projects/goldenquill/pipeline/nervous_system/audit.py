from datetime import datetime, timezone
import uuid
from typing import Optional, List, Any
from pydantic import BaseModel, Field

class AuditEvent(BaseModel):
    event_type: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    request_id: str
    session_id: Optional[str] = None
    active_user_id: Optional[str] = None
    licensed_node_id: Optional[str] = None
    licensed_customer_entity_id: Optional[str] = None
    applied_as_entity_id: Optional[str] = None
    route_mode: Optional[str] = None
    operation_intent: Optional[str] = None
    boundary: Optional[str] = None
    outcome: Optional[str] = None

class InMemoryAuditSink:
    def __init__(self):
        self.events: List[AuditEvent] = []

    def record(self, event: AuditEvent):
        self.events.append(event)

    def clear(self):
        self.events.clear()

    def get_events(self) -> List[AuditEvent]:
        return list(self.events)

class AuditRecorder:
    def __init__(self, sink=None):
        self.sink = sink or InMemoryAuditSink()

    def record_event(self, event: AuditEvent):
        self.sink.record(event)

# Global test-visible recorder
global_audit_sink = InMemoryAuditSink()
audit_recorder = AuditRecorder(sink=global_audit_sink)
