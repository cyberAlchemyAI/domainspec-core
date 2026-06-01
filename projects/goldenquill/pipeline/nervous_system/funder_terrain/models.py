from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

SCHEMA_VERSION = "funder_terrain.v0.1"

class FunderTerrainProgramStatus(str, Enum):
    known_active = "known_active"
    recurring = "recurring"
    historical = "historical"
    unknown = "unknown"
    closed = "closed"

class FunderTerrainSourceRecord(BaseModel):
    source_id: str
    source_type: str
    url_or_local_path: Optional[str] = None

class FunderTerrainReviewStatus(BaseModel):
    human_review_required: bool = False
    reason: Optional[str] = None

class FunderTerrainMetadataGap(BaseModel):
    missing_fields: List[str]

class FunderTerrainNormalizedRecord(BaseModel):
    record_id: str
    schema_version: str = SCHEMA_VERSION
    funder_family: Optional[str] = None
    document_type: Optional[str] = None
    related_project: Optional[str] = None
    geography_scope: Optional[str] = None
    program_status: FunderTerrainProgramStatus = FunderTerrainProgramStatus.unknown
    source_provenance: Optional[FunderTerrainSourceRecord] = None
    metadata_gaps: FunderTerrainMetadataGap
    review_status: FunderTerrainReviewStatus
    normalization_input_sha256: str
    ruleset_sha256: str
    record_sha256: Optional[str] = None
