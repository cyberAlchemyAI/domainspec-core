import uuid
from typing import Tuple, List, Optional
from app.schemas import (
    MacroControls, DataPosture, TopologyType, ControllerState, TensionEvent,
    SystemStatus, ResolutionStatus
)

def resolve_macro_controls(
    session_id: uuid.UUID,
    macro_controls: MacroControls,
    data_posture: DataPosture,
    topology_intent: TopologyType = TopologyType.CHAIN,
    correlation_id: Optional[uuid.UUID] = None,
    input_gesture_id: Optional[uuid.UUID] = None,
    source_surface: str = "browser",
    supersedes_state_id: Optional[uuid.UUID] = None,
    state_sequence_nonce: int = 1
) -> Tuple[ControllerState, List[TensionEvent]]:
    
    tensions: List[TensionEvent] = []
    
    # 1. divergence_vs_grounding
    effective_divergence = macro_controls.divergence
    if macro_controls.divergence >= 0.70 and macro_controls.grounding >= 0.70:
        effective_divergence = min(macro_controls.divergence, 0.75)
        tensions.append(TensionEvent(
            tension_type="divergence_vs_grounding",
            requested_vectors={"divergence": macro_controls.divergence, "grounding": macro_controls.grounding},
            resolved_vectors={"divergence": effective_divergence, "grounding": macro_controls.grounding}
        ))
        
    # 2. rigor_without_scrutiny
    effective_rubric_strictness = 0.5
    if macro_controls.maturity > 0.80 and macro_controls.pressure < 0.20:
        effective_rubric_strictness = max(effective_rubric_strictness, 0.60)
        tensions.append(TensionEvent(
            tension_type="rigor_without_scrutiny",
            requested_vectors={"maturity": macro_controls.maturity, "pressure": macro_controls.pressure},
            resolved_vectors={"rubric_strictness": effective_rubric_strictness}
        ))
        
    # 3. pressure_without_grounding
    system_status = SystemStatus.ACTIVE
    if macro_controls.pressure > 0.90 and macro_controls.grounding < 0.20:
        system_status = SystemStatus.UNRESOLVED_TENSIONS
        tensions.append(TensionEvent(
            tension_type="pressure_without_grounding",
            requested_vectors={"pressure": macro_controls.pressure, "grounding": macro_controls.grounding},
            resolved_vectors={"system_status": system_status.value}
        ))
    
    if tensions and system_status == SystemStatus.ACTIVE:
        system_status = SystemStatus.RESOLVED_WITH_TENSION

    resolution_status = ResolutionStatus.CLEAN
    if tensions:
        resolution_status = ResolutionStatus.RESOLVED_WITH_TENSION

    resolved_routing_params = {
        "routing_strategy": "default",
        "selected_topology": topology_intent.value,
        "data_posture": data_posture.value,
        "allowed_model_boundary": data_posture.value
    }
    
    resolved_generation_params = {
        "model_temperature": 0.7 + (effective_divergence * 0.3),
        "candidate_count": int(3 + (effective_divergence * 2)),
        "search_depth": int(1 + (macro_controls.maturity * 3))
    }
    
    resolved_agent_weights = {
        "conductor": 1.0,
        "scribe": 1.0,
        "scout": 1.0,
        "auditor": macro_controls.pressure,
        "logician": macro_controls.pressure,
        "archivist": macro_controls.grounding,
        "wildcard": effective_divergence
    }
    
    resolved_review_params = {
        "rubric_strictness": effective_rubric_strictness,
        "consensus_threshold": 0.5 + (macro_controls.pressure * 0.4),
        "retrieval_depth": int(macro_controls.grounding * 5)
    }
    
    controller_state = ControllerState(
        controller_state_id=uuid.uuid4(),
        session_id=session_id,
        supersedes_state_id=supersedes_state_id,
        state_sequence_nonce=state_sequence_nonce,
        correlation_id=correlation_id,
        input_gesture_id=input_gesture_id,
        source_surface=source_surface,
        macro_controls=macro_controls,
        data_posture=data_posture,
        selected_topology=topology_intent,
        active_gem=None,
        system_status=system_status,
        resolution_status=resolution_status,
        resolved_generation_params=resolved_generation_params,
        resolved_routing_params=resolved_routing_params,
        resolved_agent_weights=resolved_agent_weights,
        resolved_review_params=resolved_review_params,
        is_tension_active=len(tensions) > 0,
        tension_event_ids=[t.tension_id for t in tensions]
    )
    
    return controller_state, tensions
