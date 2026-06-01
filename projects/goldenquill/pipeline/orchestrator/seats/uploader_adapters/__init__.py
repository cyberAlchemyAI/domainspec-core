"""
Portal adapters for Uploader (§12).

Each adapter implements PortalAdapterProtocol and registers itself
in the ADAPTER_REGISTRY. Seven adapters at v0.1:

  grants_gov        — Grants.gov Workspace (federal mandatory)
  sam_gov           — SAM.gov (registration/certification validation)
  common_grant_app  — Common Grant Application (foundation standard)
  foundant          — Foundant portal platform
  submittable       — Submittable portal platform
  fluxx             — Fluxx portal platform
  copy_paste        — Fallback for unsupported portals

Per ADR-001: frozen at Golden Image build. Adding a new adapter is a
code change (new module + §12 amendment + §0.5 row), not a runtime config.
"""

from pipeline.orchestrator.seats.uploader_adapters.grants_gov import GrantsGovAdapter
from pipeline.orchestrator.seats.uploader_adapters.sam_gov import SamGovAdapter
from pipeline.orchestrator.seats.uploader_adapters.common_grant_app import CommonGrantAppAdapter
from pipeline.orchestrator.seats.uploader_adapters.foundant import FoundantAdapter
from pipeline.orchestrator.seats.uploader_adapters.submittable import SubmittableAdapter
from pipeline.orchestrator.seats.uploader_adapters.fluxx import FluxxAdapter
from pipeline.orchestrator.seats.uploader_adapters.copy_paste import CopyPasteAdapter

from pipeline.orchestrator.seats.uploader import ADAPTER_REGISTRY

ADAPTER_REGISTRY["grants_gov"] = GrantsGovAdapter
ADAPTER_REGISTRY["sam_gov"] = SamGovAdapter
ADAPTER_REGISTRY["common_grant_app"] = CommonGrantAppAdapter
ADAPTER_REGISTRY["foundant"] = FoundantAdapter
ADAPTER_REGISTRY["submittable"] = SubmittableAdapter
ADAPTER_REGISTRY["fluxx"] = FluxxAdapter
ADAPTER_REGISTRY["copy_paste"] = CopyPasteAdapter

__all__ = [
    "GrantsGovAdapter",
    "SamGovAdapter",
    "CommonGrantAppAdapter",
    "FoundantAdapter",
    "SubmittableAdapter",
    "FluxxAdapter",
    "CopyPasteAdapter",
]
