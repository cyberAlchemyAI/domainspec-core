from enum import Enum
from typing import Optional, List, Dict, Any
from datetime import datetime
import re
from pydantic import BaseModel, Field, field_validator, model_validator

class RetrievalStatus(str, Enum):
    local_file = "local_file"
    html = "html"
    pdf = "pdf"
    api_json = "api_json"
    manual_source = "manual_source"
    disabled = "disabled"
    not_implemented = "not_implemented"
    fetch_failed = "fetch_failed"
    parse_failed = "parse_failed"
    stale = "stale"

class FetchLedgerEntry(BaseModel):
    entry_id: str = Field(..., min_length=1)
    source_id: str = Field(..., min_length=1)
    retrieval_status: RetrievalStatus
    source_url: Optional[str] = None
    retrieval_timestamp: datetime
    payload_sha256: Optional[str] = None
    local_artifact_path: Optional[str] = None
    http_status_code: Optional[int] = None
    error_class: Optional[str] = None

    @field_validator("entry_id", "source_id")
    @classmethod
    def validate_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("String cannot be empty")
        return v

    @field_validator("payload_sha256")
    @classmethod
    def validate_sha256(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if not re.match(r"^[a-fA-F0-9]{64}$", v):
                raise ValueError("payload_sha256 must be a valid 64-character hex string")
        return v

    @model_validator(mode='after')
    def validate_status_constraints(self) -> 'FetchLedgerEntry':
        no_payload_statuses = {
            RetrievalStatus.disabled,
            RetrievalStatus.not_implemented,
            RetrievalStatus.fetch_failed,
            RetrievalStatus.parse_failed
        }

        if self.retrieval_status in no_payload_statuses:
            if self.payload_sha256 is not None:
                raise ValueError(f"payload_sha256 must be None for status {self.retrieval_status.value}")
            if self.local_artifact_path is not None:
                raise ValueError(f"local_artifact_path must be None for status {self.retrieval_status.value}")

        return self

def validate_fetch_ledger_entry(data: Dict[str, Any]) -> FetchLedgerEntry:
    return FetchLedgerEntry(**data)

def make_fetch_ledger_entry(**kwargs) -> FetchLedgerEntry:
    return FetchLedgerEntry(**kwargs)

def sort_ledger_entries(entries: List[FetchLedgerEntry]) -> List[FetchLedgerEntry]:
    return sorted(entries, key=lambda x: (x.source_id, x.retrieval_timestamp))
