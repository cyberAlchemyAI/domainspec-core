import hashlib
import json
from datetime import datetime, timezone
import uuid
from typing import Optional, List, Any, Dict
from pydantic import BaseModel, Field

class AuditProofEvent(BaseModel):
    schema_version: str = "1.0"
    event_type: str
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    request_id: str
    sequence_number: int
    previous_event_hash: Optional[str] = None
    event_hash: Optional[str] = None

    actor_snapshot: Optional[Dict[str, Any]] = None
    identity_context_snapshot: Optional[Dict[str, Any]] = None

    route_mode: Optional[str] = None
    operation_intent: Optional[str] = None
    applied_as_entity_id: Optional[str] = None
    boundary: Optional[str] = None
    outcome: Optional[str] = None
    metadata_redacted: Optional[Dict[str, Any]] = None

    def compute_hash(self) -> str:
        # Create a dictionary of the event without the event_hash itself
        data = self.model_dump(exclude={"event_hash"})
        # Canonical JSON serialization
        canonical_str = json.dumps(data, sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(canonical_str.encode('utf-8')).hexdigest()

class AuditProofChain:
    def __init__(self, chain_id: str = None):
        self.chain_id = chain_id or str(uuid.uuid4())
        self.events: List[AuditProofEvent] = []
        self.last_hash: Optional[str] = None

    def append_event(self, event: AuditProofEvent):
        event.previous_event_hash = self.last_hash
        event.sequence_number = len(self.events) + 1
        event.event_hash = event.compute_hash()

        self.events.append(event)
        self.last_hash = event.event_hash

class InMemoryAuditProofSink:
    def __init__(self):
        self.chains: Dict[str, AuditProofChain] = {}

    def get_chain(self, chain_id: str) -> AuditProofChain:
        if chain_id not in self.chains:
            self.chains[chain_id] = AuditProofChain(chain_id=chain_id)
        return self.chains[chain_id]

    def clear(self):
        self.chains.clear()

def redact_sensitive_data(data: Any) -> Any:
    """Recursively redacts sensitive keys from dictionaries."""
    if isinstance(data, dict):
        redacted = {}
        for k, v in data.items():
            k_lower = k.lower()
            # Redaction guard rules
            if any(forbidden in k_lower for forbidden in ["api_key", "authorization", "bearer", "secret", "token"]):
                redacted[k] = "[REDACTED]"
            elif k_lower in ["raw_response", "synthetic_response", "prompt_body", "scout_pipeline", "scout_totals"]:
                # Strip raw provider responses, payloads, etc.
                redacted[k] = "[STRIPPED]"
            else:
                redacted[k] = redact_sensitive_data(v)
        return redacted
    elif isinstance(data, list):
        return [redact_sensitive_data(item) for item in data]
    return data

class AuditProofRecorder:
    def __init__(self, sink: InMemoryAuditProofSink):
        self.sink = sink

    def record(self, chain_id: str, event_type: str, request_id: str, **kwargs):
        chain = self.sink.get_chain(chain_id)

        # Redact any metadata
        raw_meta = kwargs.pop("metadata", {})
        redacted_meta = redact_sensitive_data(raw_meta)

        event = AuditProofEvent(
            event_type=event_type,
            request_id=request_id,
            sequence_number=0, # Computed by chain
            metadata_redacted=redacted_meta,
            **kwargs
        )
        chain.append_event(event)
        return event

# Global test-local sink
global_proof_sink = InMemoryAuditProofSink()
proof_recorder = AuditProofRecorder(sink=global_proof_sink)
