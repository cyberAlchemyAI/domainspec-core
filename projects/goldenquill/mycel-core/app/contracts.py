from app.schemas import EventType

GEM_ALLOWED_EVENTS = {
    "scribe": [EventType.THOUGHT, EventType.SEMANTIC_DIFF],
    "auditor": [EventType.SCORE],
    "logician": [EventType.GATE],
    "scout": [EventType.THOUGHT],
    "archivist": ["EvidenceItem", "ProvenanceLink"], # placeholders
    "wildcard": [EventType.THOUGHT, EventType.SEMANTIC_DIFF],
    "conductor": ["RouteProposal"]
}

def validate_gem_emission(gem_name: str, event_type: EventType, payload: dict):
    gem_name_lower = gem_name.lower()
    if gem_name_lower not in GEM_ALLOWED_EVENTS:
        raise ValueError(f"Unknown gem: {gem_name}")
        
    allowed_types = GEM_ALLOWED_EVENTS[gem_name_lower]
    if event_type not in allowed_types and getattr(event_type, 'value', event_type) not in allowed_types:
        raise ValueError(f"Event type {event_type} not allowed for gem {gem_name}")

    if gem_name_lower == "auditor":
        if event_type == EventType.THOUGHT:
            raise ValueError("Auditor cannot emit ThoughtObject")
        forbidden_fields = {"content", "summary", "rewritten_text", "draft", "edited_text"}
        if any(f in payload for f in forbidden_fields):
            raise ValueError("Auditor cannot carry prose fields")
            
    if gem_name_lower == "logician":
        if event_type == EventType.THOUGHT:
            raise ValueError("Logician cannot emit ThoughtObject")
        forbidden_fields = {"content", "summary", "rewritten_text", "draft", "edited_text"}
        if any(f in payload for f in forbidden_fields):
            raise ValueError("Logician cannot carry prose fields")
