import pytest
from app.schemas import (
    DataPosture, MacroControls, CommitEvent, Actor, ActorKind,
    ScoreEvent
)
from pydantic import ValidationError
import uuid

def test_data_posture_values():
    assert DataPosture.LOCAL_ONLY.value == "LOCAL_ONLY"
    assert DataPosture.HYBRID.value == "HYBRID"
    assert DataPosture.FULL_ACCESS.value == "FULL_ACCESS"
    
    with pytest.raises(ValueError):
        DataPosture("SANITIZED")
        
    with pytest.raises(ValueError):
        DataPosture("STERILIZED")

def test_macro_controls_only_allowed_fields():
    controls = MacroControls(maturity=0.5, divergence=0.5, grounding=0.5, pressure=0.5)
    assert hasattr(controls, "maturity")

def test_commit_event_actor():
    with pytest.raises(ValidationError):
        CommitEvent(
            actor=Actor(kind=ActorKind.GEM, actor_id="gem"),
            selected_thought_id=uuid.uuid4(),
            controller_state_id=uuid.uuid4()
        )
        
    commit = CommitEvent(
        actor=Actor(kind=ActorKind.HUMAN, actor_id="user"),
        selected_thought_id=uuid.uuid4(),
        controller_state_id=uuid.uuid4()
    )
    assert commit.actor.kind == ActorKind.HUMAN

def test_score_event():
    with pytest.raises(ValidationError):
        ScoreEvent(
            thought_id=uuid.uuid4(),
            rubric_type="test",
            novelty=0.5,
            feasibility=0.5,
            coherence=0.5,
            development_potential=0.5,
            resource_fit=0.5,
            # missing evidence_readiness and risk
        )
