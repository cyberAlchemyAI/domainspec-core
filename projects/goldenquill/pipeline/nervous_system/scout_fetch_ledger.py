from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from pipeline.nervous_system.scout_source_roster import SourceStatus

class FetchMethod(str, Enum):
    api = "api"
    html = "html"
    pdf = "pdf"
    rss = "rss"
    email = "email"
    manual = "manual"
    browser_pending = "browser_pending"

class FetchLedgerRecord(BaseModel):
    fetch_id: str
    source_id: str
    checked_at: str
    method: FetchMethod
    result_status: SourceStatus
    http_status: Optional[int] = None
    content_hash: Optional[str] = None
    snapshot_path: Optional[str] = None
    error_message: Optional[str] = None
    extracted_opportunity_count: Optional[int] = None
    notes: Optional[str] = None

    model_config = ConfigDict(extra="allow")

def build_empty_fetch_ledger() -> list:
    return []
