import pytest
from app.contracts import validate_gem_emission
from app.schemas import EventType

def test_auditor_prose_rejected():
    with pytest.raises(ValueError):
        validate_gem_emission("auditor", EventType.THOUGHT, {})
        
    with pytest.raises(ValueError):
        validate_gem_emission("auditor", EventType.SCORE, {"content": "some text"})

def test_logician_prose_rejected():
    with pytest.raises(ValueError):
        validate_gem_emission("logician", EventType.THOUGHT, {})
        
    with pytest.raises(ValueError):
        validate_gem_emission("logician", EventType.GATE, {"summary": "some text"})

def test_unknown_gem_rejected():
    with pytest.raises(ValueError):
        validate_gem_emission("fakegem", EventType.THOUGHT, {})
        
def test_scribe_thought_accepted():
    validate_gem_emission("scribe", EventType.THOUGHT, {})
