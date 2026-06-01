from enum import Enum
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, field_validator, model_validator

class ChannelType(str, Enum):
    local_file = "local_file"
    html = "html"
    pdf = "pdf"
    api_json = "api_json"
    manual_source = "manual_source"

class RetrievalMethod(str, Enum):
    manual = "manual"
    managed_fetch = "managed_fetch"
    disabled = "disabled"
    not_implemented = "not_implemented"

class SourceChannelDefinition(BaseModel):
    source_id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    channel_type: ChannelType
    retrieval_method: RetrievalMethod
    jurisdiction: str
    category: str
    freshness_threshold_seconds: int
    enabled: bool = False
    base_url: Optional[str] = None
    notes: Optional[str] = None

    @field_validator("freshness_threshold_seconds")
    @classmethod
    def validate_freshness(cls, v: int) -> int:
        if v <= 0:
            raise ValueError("freshness_threshold_seconds must be > 0")
        return v

    @field_validator("source_id", "name")
    @classmethod
    def validate_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("String cannot be empty")
        return v

def validate_source_channel(data: Dict[str, Any]) -> SourceChannelDefinition:
    return SourceChannelDefinition(**data)

def normalize_source_channel(data: Dict[str, Any]) -> Dict[str, Any]:
    record = SourceChannelDefinition(**data)
    return record.model_dump(exclude_none=True)

def load_source_manifest_from_records(records: List[Dict[str, Any]]) -> List[SourceChannelDefinition]:
    channels = [SourceChannelDefinition(**r) for r in records]
    # Sort deterministically by source_id
    channels.sort(key=lambda x: x.source_id)
    return channels
