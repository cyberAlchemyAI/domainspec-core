from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict, model_validator

class SourceType(str, Enum):
    api = "api"
    html_page = "html_page"
    pdf_index = "pdf_index"
    rss = "rss"
    email_newsletter = "email_newsletter"
    manual_seed = "manual_seed"
    state_portal = "state_portal"
    foundation_page = "foundation_page"
    other = "other"

class SourceStatus(str, Enum):
    verified = "verified"
    stale = "stale"
    blocked = "blocked"
    not_implemented = "not_implemented"
    fixture_only = "fixture_only"
    source_not_configured = "source_not_configured"
    unavailable = "unavailable"
    failed_validation = "failed_validation"

class SourceRecord(BaseModel):
    source_id: str
    name: str
    source_type: SourceType
    source_status: SourceStatus
    url: Optional[str] = None
    sectors: List[str] = Field(default_factory=list)
    geography: Optional[str] = None
    owner_entity: Optional[str] = None
    enabled: bool = False
    last_checked_at: Optional[str] = None
    notes: Optional[str] = None

    model_config = ConfigDict(extra="allow")

    @model_validator(mode="after")
    def validate_other_type(self):
        if self.source_type == SourceType.other:
            if not self.notes or not self.notes.strip():
                raise ValueError("source_type 'other' requires non-empty notes")
        return self

def list_configured_sources() -> List[SourceRecord]:
    from .scout_adapters.registry import default_registry
    static_sources = [
        SourceRecord(
            source_id="seed_vapg",
            name="USDA VAPG FY26 Seed",
            source_type=SourceType.manual_seed,
            source_status=SourceStatus.source_not_configured,
            enabled=False,
            notes="Deterministically seeded from demo RFA JSON."
        )
    ]
    return static_sources + default_registry.list_metadata()

def list_enabled_sources() -> List[SourceRecord]:
    return [s for s in list_configured_sources() if s.enabled]

def summarize_source_coverage() -> Dict[str, Any]:
    sources = list_enabled_sources()
    fixture_mode = len(sources) == 0
    if fixture_mode:
        channels = [
            SourceRecord(
                source_id="fallback_not_configured",
                name="Fallback No Sources",
                source_type=SourceType.other,
                source_status=SourceStatus.source_not_configured,
                enabled=False,
                notes="No real source channels are configured in this build."
            ).model_dump(mode="json")
        ]
    else:
        channels = [s.model_dump(mode="json") for s in sources]
    return {
        "fixture_mode": fixture_mode,
        "channels": channels
    }
