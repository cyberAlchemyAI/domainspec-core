import uuid
from app.macro_resolver import resolve_macro_controls
from app.schemas import MacroControls, DataPosture, SystemStatus

def test_nominal_controls():
    session_id = uuid.uuid4()
    mc = MacroControls(maturity=0.5, divergence=0.5, grounding=0.5, pressure=0.5)
    
    cs, tensions = resolve_macro_controls(session_id, mc, DataPosture.LOCAL_ONLY)
    assert len(tensions) == 0
    assert cs.system_status == SystemStatus.ACTIVE
    assert cs.data_posture == DataPosture.LOCAL_ONLY
    assert cs.resolved_routing_params["data_posture"] == "LOCAL_ONLY"

def test_divergence_vs_grounding():
    session_id = uuid.uuid4()
    mc = MacroControls(maturity=0.5, divergence=0.8, grounding=0.8, pressure=0.5)
    
    cs, tensions = resolve_macro_controls(session_id, mc, DataPosture.LOCAL_ONLY)
    assert len(tensions) == 1
    assert tensions[0].tension_type == "divergence_vs_grounding"
    assert tensions[0].resolved_vectors["divergence"] == 0.75
    assert cs.resolved_generation_params["model_temperature"] == 0.7 + (0.75 * 0.3)

def test_rigor_without_scrutiny():
    session_id = uuid.uuid4()
    mc = MacroControls(maturity=0.9, divergence=0.5, grounding=0.5, pressure=0.1)
    
    cs, tensions = resolve_macro_controls(session_id, mc, DataPosture.LOCAL_ONLY)
    assert len(tensions) == 1
    assert tensions[0].tension_type == "rigor_without_scrutiny"
    assert tensions[0].resolved_vectors["rubric_strictness"] == 0.60
    assert cs.resolved_review_params["rubric_strictness"] == 0.60

def test_pressure_without_grounding():
    session_id = uuid.uuid4()
    mc = MacroControls(maturity=0.5, divergence=0.5, grounding=0.1, pressure=0.95)
    
    cs, tensions = resolve_macro_controls(session_id, mc, DataPosture.LOCAL_ONLY)
    assert len(tensions) == 1
    assert tensions[0].tension_type == "pressure_without_grounding"
    assert cs.system_status == SystemStatus.UNRESOLVED_TENSIONS
