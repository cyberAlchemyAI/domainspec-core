"""Operational-data sub-kinds for §2 Vault topology (v7.2, R.PF2 backfill).

Per architecture §R.PF2 (v7 LOCKED 2026-04-19): §2 Vault topology accommodates
operational data alongside funder/grant artifacts. The seven SIMPLE sub-kinds
land here (metrics / financials / photos / narrative_entries /
timeline_of_activities / beneficiary_records / attachments). Each module owns
its schema, canonical-bytes encoder/decoder, and registry binding. Cedar
policy enforcement is centralized in :mod:`pipeline.vault.sub_kinds.policy_eval`
(authoritative Python evaluator at v0.1, mirroring §2 v7.1 §3.4).

Blueprint amendment: ``pipeline/blueprint/v0.1/section_02_v7_2_amendment.md``
(DRAFT, Code phase 2026-05-10; awaiting Cowork Thesis round LOCK).
"""

from __future__ import annotations

from pipeline.vault.sub_kinds.attachments import (
    AttachmentRecord,
    INTENT as ATTACHMENT_INTENT,
)
from pipeline.vault.sub_kinds.beneficiary_records import (
    BeneficiaryRecord,
    INTENT as BENEFICIARY_INTENT,
)
from pipeline.vault.sub_kinds.financials import (
    FinancialsRecord,
    INTENT as FINANCIALS_INTENT,
)
from pipeline.vault.sub_kinds.metrics import (
    INTENT as METRICS_INTENT,
    MetricsRecord,
)
from pipeline.vault.sub_kinds.narrative_entries import (
    INTENT as NARRATIVE_INTENT,
    NarrativeEntry,
)
from pipeline.vault.sub_kinds.photos import (
    INTENT as PHOTO_INTENT,
    PhotoRecord,
)
from pipeline.vault.sub_kinds.policy_eval import (
    F_CEDAR_OPERATIONAL_DENIED,
    F_OPERATIONAL_PII_CONSENT_MISSING,
    F_OPERATIONAL_SCHEMA_INVALID,
    CedarOperationalDenied,
    OperationalPIIConsentMissing,
    OperationalSchemaInvalid,
    evaluate_operational_write,
)
from pipeline.vault.sub_kinds.registry import (
    OPERATIONAL_INTENTS,
    OPERATIONAL_SUBTREE_PREFIX,
    SUB_KIND_REGISTRY,
    SEVERITY_GREEN,
    SEVERITY_RED,
    SEVERITY_YELLOW,
    SubKindDescriptor,
    descriptor_for_intent,
    descriptor_for_sub_kind,
    operational_subtree_for,
)
from pipeline.vault.sub_kinds.timeline_of_activities import (
    INTENT as TIMELINE_INTENT,
    TimelineActivity,
)

__all__ = [
    # registry
    "OPERATIONAL_INTENTS",
    "OPERATIONAL_SUBTREE_PREFIX",
    "SUB_KIND_REGISTRY",
    "SEVERITY_GREEN",
    "SEVERITY_RED",
    "SEVERITY_YELLOW",
    "SubKindDescriptor",
    "descriptor_for_intent",
    "descriptor_for_sub_kind",
    "operational_subtree_for",
    # records
    "AttachmentRecord",
    "BeneficiaryRecord",
    "FinancialsRecord",
    "MetricsRecord",
    "NarrativeEntry",
    "PhotoRecord",
    "TimelineActivity",
    # intents (re-exported from each sub-kind module)
    "ATTACHMENT_INTENT",
    "BENEFICIARY_INTENT",
    "FINANCIALS_INTENT",
    "METRICS_INTENT",
    "NARRATIVE_INTENT",
    "PHOTO_INTENT",
    "TIMELINE_INTENT",
    # policy + failure surface
    "CedarOperationalDenied",
    "F_CEDAR_OPERATIONAL_DENIED",
    "F_OPERATIONAL_PII_CONSENT_MISSING",
    "F_OPERATIONAL_SCHEMA_INVALID",
    "OperationalPIIConsentMissing",
    "OperationalSchemaInvalid",
    "evaluate_operational_write",
]
