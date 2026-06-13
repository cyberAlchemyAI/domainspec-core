import uuid
import threading
from app.event_store import EventStore
from app.schemas import EventEnvelope, EventType, Actor, ActorKind
import pytest

def test_first_event_is_seq_1():
    store = EventStore("mycel_audit.db")
    session_id = uuid.uuid4()
    
    env = EventEnvelope(
        session_id=session_id,
        seq=1,
        event_type=EventType.HUMAN_SEED,
        actor=Actor(kind=ActorKind.HUMAN, actor_id="operator"),
        payload={"content": "test"}
    )
    
    saved = store.append(env)
    assert saved.seq == 1
    
    env2 = EventEnvelope(
        session_id=session_id,
        seq=1,
        event_type=EventType.HUMAN_SEED,
        actor=Actor(kind=ActorKind.HUMAN, actor_id="operator"),
        payload={"content": "test"}
    )
    saved2 = store.append(env2)
    assert saved2.seq == 2

def test_idempotency_key_returns_original():
    store = EventStore("mycel_audit.db")
    session_id = uuid.uuid4()
    idem_key = "test-key-1"
    
    env = EventEnvelope(
        session_id=session_id,
        seq=1,
        event_type=EventType.HUMAN_SEED,
        actor=Actor(kind=ActorKind.HUMAN, actor_id="operator"),
        idempotency_key=idem_key,
        payload={"content": "test"}
    )
    
    saved = store.append(env)
    assert saved.seq == 1
    
    env2 = EventEnvelope(
        session_id=session_id,
        seq=1,
        event_type=EventType.HUMAN_SEED,
        actor=Actor(kind=ActorKind.HUMAN, actor_id="operator"),
        idempotency_key=idem_key,
        payload={"content": "test2"}
    )
    saved2 = store.append(env2)
    
    assert saved2.seq == 1
    assert saved2.event_id == saved.event_id

def test_concurrent_appends():
    store = EventStore("mycel_audit.db")
    session_id = uuid.uuid4()
    
    def worker():
        for _ in range(20):
            env = EventEnvelope(
                session_id=session_id,
                seq=1,
                event_type=EventType.HUMAN_SEED,
                actor=Actor(kind=ActorKind.HUMAN, actor_id="operator"),
                payload={"content": "test"}
            )
            store.append(env)
            
    threads = [threading.Thread(target=worker) for _ in range(5)]
    for t in threads: t.start()
    for t in threads: t.join()
    
    latest = store.latest_seq(session_id)
    assert latest == 100
    
    events = store.get_events(session_id)
    seqs = [e.seq for e in events]
    assert seqs == list(range(1, 101))
