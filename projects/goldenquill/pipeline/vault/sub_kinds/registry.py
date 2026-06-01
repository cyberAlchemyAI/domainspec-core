"""Operational sub-kind registry. [§2.12]

Single canonical mapping from sub-kind name → :class:`SubKindDescriptor`.
The descriptor exposes everything downstream callers (Data Collector v0.2,
Report Generator v0.2, Uploader v0.1.1, Archivist v1.x) need to round-trip
operational records without hardcoding the per-sub-kind module:

* ``intent`` — the ``vault_write`` intent string for this sub-kind.
* ``vault_subtree`` — the ``operational/<sub_kind>/`` prefix.
* ``record_class`` — the frozen-dataclass record type.
* ``to_canonical_bytes`` / ``from_canonical_bytes`` — encoders.
* ``record_id_for`` — filename-stem derivation.
* ``severity_default`` — admin-risk severity for routing decisions.
* ``severity_for(record)`` — record-level severity (RED for PII-bearing
  beneficiary records, ``severity_default`` otherwise).

Future sub-kinds register via one new module + one row here + one
allowlist row in ``vault_write.POST_GATE_ALLOWLIST``. R.PF2 calls this
out as the extensibility surface; F-VAULT-ARTIFACT-ONLY audits enforce
that adding a sub-kind is row-additive, not architectural.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Final, Optional

from pipeline.vault.sub_kinds import (
    attachments as _attachments,
    beneficiary_records as _beneficiary,
    cycle_receipts as _cycle_receipts,
    financials as _financials,
    metrics as _metrics,
    narrative_entries as _narrative,
    photos as _photos,
    timeline_of_activities as _timeline,
)

BLUEPRINT_DEPS: Final[dict[str, dict[str, object]]] = {
    "section_02_v7_2_amendment.md": {
        "version": "v7.2-DRAFT",
        "sections_implemented": [
            "§2.12 SUB_KIND_REGISTRY single canonical mapping",
            "§1 scope sub-kind table — admin-risk severity defaults",
        ],
    },
}

# Severity tiers — must remain in sync with Section 1
# ``pipeline.sovereignty.admin_risk.SEVERITY_LIMITS`` (GREEN / YELLOW / RED).
SEVERITY_GREEN: Final[str] = "GREEN"
SEVERITY_YELLOW: Final[str] = "YELLOW"
SEVERITY_RED: Final[str] = "RED"

OPERATIONAL_SUBTREE_PREFIX: Final[str] = "operational/"


@dataclass(frozen=True, kw_only=True)
class SubKindDescriptor:
    """Registry entry for one operational sub-kind."""

    sub_kind: str
    intent: str
    vault_subtree: str
    record_class: type
    to_canonical_bytes: Callable[[Any], bytes]
    from_canonical_bytes: Callable[[bytes], Any]
    record_id_for: Callable[[Any], str]
    severity_default: str
    severity_for: Callable[[Any], str]


def _default_severity_callable(severity_default: str) -> Callable[[Any], str]:
    """Build a record→severity callable that always returns ``severity_default``."""

    def _severity(_record: Any) -> str:
        return severity_default

    return _severity


SUB_KIND_REGISTRY: Final[dict[str, SubKindDescriptor]] = {
    _metrics.SUB_KIND: SubKindDescriptor(
        sub_kind=_metrics.SUB_KIND,
        intent=_metrics.INTENT,
        vault_subtree=_metrics.VAULT_SUBTREE,
        record_class=_metrics.MetricsRecord,
        to_canonical_bytes=_metrics.to_canonical_bytes,
        from_canonical_bytes=_metrics.from_canonical_bytes,
        record_id_for=_metrics.record_id_for,
        severity_default=_metrics.ADMIN_RISK_SEVERITY,
        severity_for=_default_severity_callable(_metrics.ADMIN_RISK_SEVERITY),
    ),
    _financials.SUB_KIND: SubKindDescriptor(
        sub_kind=_financials.SUB_KIND,
        intent=_financials.INTENT,
        vault_subtree=_financials.VAULT_SUBTREE,
        record_class=_financials.FinancialsRecord,
        to_canonical_bytes=_financials.to_canonical_bytes,
        from_canonical_bytes=_financials.from_canonical_bytes,
        record_id_for=_financials.record_id_for,
        severity_default=_financials.ADMIN_RISK_SEVERITY,
        severity_for=_default_severity_callable(_financials.ADMIN_RISK_SEVERITY),
    ),
    _photos.SUB_KIND: SubKindDescriptor(
        sub_kind=_photos.SUB_KIND,
        intent=_photos.INTENT,
        vault_subtree=_photos.VAULT_SUBTREE,
        record_class=_photos.PhotoRecord,
        to_canonical_bytes=_photos.to_canonical_bytes,
        from_canonical_bytes=_photos.from_canonical_bytes,
        record_id_for=_photos.record_id_for,
        severity_default=_photos.ADMIN_RISK_SEVERITY,
        severity_for=_default_severity_callable(_photos.ADMIN_RISK_SEVERITY),
    ),
    _narrative.SUB_KIND: SubKindDescriptor(
        sub_kind=_narrative.SUB_KIND,
        intent=_narrative.INTENT,
        vault_subtree=_narrative.VAULT_SUBTREE,
        record_class=_narrative.NarrativeEntry,
        to_canonical_bytes=_narrative.to_canonical_bytes,
        from_canonical_bytes=_narrative.from_canonical_bytes,
        record_id_for=_narrative.record_id_for,
        severity_default=_narrative.ADMIN_RISK_SEVERITY,
        severity_for=_default_severity_callable(_narrative.ADMIN_RISK_SEVERITY),
    ),
    _timeline.SUB_KIND: SubKindDescriptor(
        sub_kind=_timeline.SUB_KIND,
        intent=_timeline.INTENT,
        vault_subtree=_timeline.VAULT_SUBTREE,
        record_class=_timeline.TimelineActivity,
        to_canonical_bytes=_timeline.to_canonical_bytes,
        from_canonical_bytes=_timeline.from_canonical_bytes,
        record_id_for=_timeline.record_id_for,
        severity_default=_timeline.ADMIN_RISK_SEVERITY,
        severity_for=_default_severity_callable(_timeline.ADMIN_RISK_SEVERITY),
    ),
    _beneficiary.SUB_KIND: SubKindDescriptor(
        sub_kind=_beneficiary.SUB_KIND,
        intent=_beneficiary.INTENT,
        vault_subtree=_beneficiary.VAULT_SUBTREE,
        record_class=_beneficiary.BeneficiaryRecord,
        to_canonical_bytes=_beneficiary.to_canonical_bytes,
        from_canonical_bytes=_beneficiary.from_canonical_bytes,
        record_id_for=_beneficiary.record_id_for,
        severity_default=_beneficiary.ADMIN_RISK_SEVERITY,
        severity_for=_beneficiary.severity_for,
    ),
    _attachments.SUB_KIND: SubKindDescriptor(
        sub_kind=_attachments.SUB_KIND,
        intent=_attachments.INTENT,
        vault_subtree=_attachments.VAULT_SUBTREE,
        record_class=_attachments.AttachmentRecord,
        to_canonical_bytes=_attachments.to_canonical_bytes,
        from_canonical_bytes=_attachments.from_canonical_bytes,
        record_id_for=_attachments.record_id_for,
        severity_default=_attachments.ADMIN_RISK_SEVERITY,
        severity_for=_default_severity_callable(_attachments.ADMIN_RISK_SEVERITY),
    ),
    # §17 WPFA cycle_receipt sub-kind — LOCKED 2026-05-11 row 205.
    # severity_for() elevates to RED iff the receipt carries an operator
    # Ed25519 attestation (per §17.3.3) — buyer-attested receipts need
    # admin-risk attention before they ship externally.
    _cycle_receipts.SUB_KIND: SubKindDescriptor(
        sub_kind=_cycle_receipts.SUB_KIND,
        intent=_cycle_receipts.INTENT,
        vault_subtree=_cycle_receipts.VAULT_SUBTREE,
        record_class=_cycle_receipts.CycleReceipt,
        to_canonical_bytes=_cycle_receipts.to_canonical_bytes,
        from_canonical_bytes=_cycle_receipts.from_canonical_bytes,
        record_id_for=_cycle_receipts.record_id_for,
        severity_default=_cycle_receipts.ADMIN_RISK_SEVERITY_DEFAULT,
        severity_for=lambda record: (
            SEVERITY_RED
            if getattr(record, "signed_by_operator_ed25519", None) is not None
            else _cycle_receipts.ADMIN_RISK_SEVERITY_DEFAULT
        ),
    ),
    # §16 reflection_packet sub-kind — DEFERRED to v0.2 first wave LOCK per
    # §16 v1 LOCK row 216 (2026-05-15) "v0.1 Beta hook DORMANT per OQ-2 (a)".
    # Schema module is authored at pipeline.vault.sub_kinds.reflection_packets
    # but intentionally NOT imported / NOT registered here. Vault read/write
    # dispatch will not find a "reflection_packet" sub-kind at v0.1 hook —
    # by design. Registration lands at the v0.2 first wave compound LOCK
    # (§16 v1.1 + §2 v7.x + §4 v2.x.y.1 + §15 v2.x + §0.5 paired-commit).
}


# Reverse index: intent → descriptor (built once at import).
_INTENT_TO_DESCRIPTOR: Final[dict[str, SubKindDescriptor]] = {
    d.intent: d for d in SUB_KIND_REGISTRY.values()
}

OPERATIONAL_INTENTS: Final[frozenset[str]] = frozenset(_INTENT_TO_DESCRIPTOR)


def descriptor_for_sub_kind(sub_kind: str) -> SubKindDescriptor:
    """Return the descriptor for ``sub_kind``.

    :raises KeyError: ``sub_kind`` is not registered.
    """
    if not isinstance(sub_kind, str):
        raise TypeError(f"sub_kind must be str, got {type(sub_kind).__name__}")
    return SUB_KIND_REGISTRY[sub_kind]


def descriptor_for_intent(intent: str) -> Optional[SubKindDescriptor]:
    """Return the descriptor for ``intent`` or ``None`` if not operational."""
    if not isinstance(intent, str):
        raise TypeError(f"intent must be str, got {type(intent).__name__}")
    return _INTENT_TO_DESCRIPTOR.get(intent)


def operational_subtree_for(sub_kind: str) -> str:
    """Return the ``operational/<sub_kind>/`` vault subtree prefix."""
    return descriptor_for_sub_kind(sub_kind).vault_subtree


__all__ = [
    "BLUEPRINT_DEPS",
    "OPERATIONAL_INTENTS",
    "OPERATIONAL_SUBTREE_PREFIX",
    "SEVERITY_GREEN",
    "SEVERITY_RED",
    "SEVERITY_YELLOW",
    "SUB_KIND_REGISTRY",
    "SubKindDescriptor",
    "descriptor_for_intent",
    "descriptor_for_sub_kind",
    "operational_subtree_for",
]
