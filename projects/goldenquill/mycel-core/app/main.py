import uuid
import asyncio
from typing import Optional
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from pydantic import BaseModel

from app.schemas import (
    MacroControls, DataPosture, TopologyType, EventEnvelope, EventType,
    Actor, ActorKind, ControllerState
)
from app.event_store import EventStore
from app.macro_resolver import resolve_macro_controls
from app.projection import build_frame
from app.database import init_db

init_db("mycel_audit.db")

app = FastAPI(title="MyCel V1")
event_store = EventStore("mycel_audit.db")

class MacroControlsRequest(BaseModel):
    macro_controls: MacroControls
    data_posture: Optional[DataPosture] = DataPosture.LOCAL_ONLY
    topology: Optional[TopologyType] = TopologyType.CHAIN
    correlation_id: Optional[uuid.UUID] = None
    input_gesture_id: Optional[uuid.UUID] = None
    source_surface: str = "browser"
    idempotency_key: Optional[str] = None

@app.post("/api/v1/sessions/{session_id}/macro-controls")
async def apply_macro_controls(session_id: uuid.UUID, req: MacroControlsRequest):
    controller_state, tensions = resolve_macro_controls(
        session_id=session_id,
        macro_controls=req.macro_controls,
        data_posture=req.data_posture,
        topology_intent=req.topology,
        correlation_id=req.correlation_id,
        input_gesture_id=req.input_gesture_id,
        source_surface=req.source_surface
    )
    
    actor = Actor(kind=ActorKind.HUMAN, actor_id="operator")
    
    env = EventEnvelope(
        session_id=session_id,
        seq=1, # EventStore overrides this
        event_type=EventType.CONTROLLER_STATE_CHANGED,
        actor=actor,
        controller_state_id=controller_state.controller_state_id,
        correlation_id=req.correlation_id,
        idempotency_key=req.idempotency_key,
        payload=controller_state.model_dump(mode="json")
    )
    
    saved_env = event_store.append(env)
    
    for t in tensions:
        t_env = EventEnvelope(
            session_id=session_id,
            seq=1, # EventStore overrides
            event_type=EventType.TENSION,
            actor=actor,
            controller_state_id=controller_state.controller_state_id,
            correlation_id=req.correlation_id,
            payload=t.model_dump(mode="json")
        )
        event_store.append(t_env)
        
    return {
        "status": "success",
        "controller_state_id": controller_state.controller_state_id,
        "seq": saved_env.seq,
        "tension_count": len(tensions)
    }

@app.get("/api/v1/sessions/{session_id}/projection")
async def get_projection(session_id: uuid.UUID):
    frame = build_frame(session_id, event_store)
    return {
        "audit_cursor": frame.derived_from_seq,
        "latest_visual_projection_frame": frame.model_dump(mode="json")
    }

@app.websocket("/ws/v1/sessions/{session_id}/events")
async def websocket_endpoint(websocket: WebSocket, session_id: uuid.UUID, cursor: int = 0):
    await websocket.accept()
    
    # replay events > cursor
    events = event_store.get_events(session_id, after_seq=cursor)
    for env in events:
        await websocket.send_json(env.model_dump(mode="json"))
        cursor = env.seq
        
    try:
        while True:
            # heartbeat handling: wait for a heartbeat or timeout
            try:
                # We do a simplistic poll
                message = await asyncio.wait_for(websocket.receive_text(), timeout=0.1)
                # Ignore heartbeat message - just transport, no persist
            except asyncio.TimeoutError:
                pass
                
            new_events = event_store.get_events(session_id, after_seq=cursor)
            for env in new_events:
                await websocket.send_json(env.model_dump(mode="json"))
                cursor = env.seq
    except WebSocketDisconnect:
        pass
