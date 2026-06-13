import uuid
from typing import Optional
from app.schemas import (
    VisualProjectionFrame, EventType,
    ScoreEvent, GateEvent, TensionEvent,
    SystemStatus, TopologyType
)
from app.event_store import EventStore

def build_frame(session_id: uuid.UUID, event_store: EventStore, up_to_seq: Optional[int] = None) -> VisualProjectionFrame:
    events = event_store.get_events(session_id, after_seq=0)
    if up_to_seq is not None:
        events = [e for e in events if e.seq <= up_to_seq]
        
    derived_seq = events[-1].seq if events else 0
    
    frame = VisualProjectionFrame(
        session_id=session_id,
        derived_from_seq=derived_seq,
    )
    
    for envelope in events:
        payload = envelope.payload
        if envelope.event_type == EventType.CONTROLLER_STATE_CHANGED:
            frame.latest_controller_state_id = uuid.UUID(payload["controller_state_id"])
            frame.active_topology = TopologyType(payload["selected_topology"])
            frame.system_status = SystemStatus(payload["system_status"])
            frame.resolved_agent_weights = payload["resolved_agent_weights"]
        elif envelope.event_type == EventType.THOUGHT:
            t_id = uuid.UUID(payload["thought_id"])
            if t_id not in frame.visible_thought_ids:
                frame.visible_thought_ids.append(t_id)
        elif envelope.event_type == EventType.SCORE:
            thought_id = uuid.UUID(payload["thought_id"])
            frame.score_badges[thought_id] = ScoreEvent(**payload)
        elif envelope.event_type == EventType.GATE:
            thought_id = uuid.UUID(payload["thought_id"])
            frame.gate_badges[thought_id] = GateEvent(**payload)
        elif envelope.event_type == EventType.TENSION:
            frame.tension_badges.append(TensionEvent(**payload))
        elif envelope.event_type == EventType.SYSTEM_CONTROL:
            if payload.get("action") == "halt_routing":
                frame.system_status = SystemStatus.HALTED
                
    return frame
