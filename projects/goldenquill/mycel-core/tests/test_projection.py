import uuid
from app.projection import build_frame
from app.event_store import EventStore
from app.schemas import EventEnvelope, EventType, Actor, ActorKind, SystemStatus

def test_projection_fold():
    store = EventStore("mycel_audit.db")
    session_id = uuid.uuid4()
    
    frame = build_frame(session_id, store)
    assert frame.derived_from_seq == 0
    
    env1 = EventEnvelope(
        session_id=session_id,
        seq=1,
        event_type=EventType.CONTROLLER_STATE_CHANGED,
        actor=Actor(kind=ActorKind.HUMAN, actor_id="operator"),
        payload={
            "controller_state_id": str(uuid.uuid4()),
            "selected_topology": "chain",
            "system_status": "active",
            "resolved_agent_weights": {}
        }
    )
    store.append(env1)
    
    env2 = EventEnvelope(
        session_id=session_id,
        seq=1,
        event_type=EventType.SYSTEM_CONTROL,
        actor=Actor(kind=ActorKind.HUMAN, actor_id="operator"),
        payload={"action": "halt_routing"}
    )
    store.append(env2)
    
    frame1 = build_frame(session_id, store)
    frame2 = build_frame(session_id, store)
    
    assert frame1.derived_from_seq == 2
    assert frame2.derived_from_seq == 2
    
    d1 = frame1.model_dump(exclude={"last_updated_at"})
    d2 = frame2.model_dump(exclude={"last_updated_at"})
    assert d1 == d2
    
    assert frame1.system_status == SystemStatus.HALTED
    assert len(frame1.score_badges) == 0
    assert len(frame1.gate_badges) == 0
    assert len(frame1.tension_badges) == 0
