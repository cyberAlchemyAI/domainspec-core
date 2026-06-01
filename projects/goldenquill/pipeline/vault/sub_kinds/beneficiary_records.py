"""``beneficiary_records`` sub-kind — per-beneficiary outcome records. [§2.11.6, §2.13]

Schema, canonical-bytes encode/decode, and intent constant for beneficiary
records (per-individual program/service outcomes).

Severity:
    * RED when ``pii_present == True`` — operator must be flagged
      ``operator_authorized_pii`` for the session; per-write admin-risk
      ledger entry required (RED severity rate-limit applies per Section 1
      ``SEVERITY_LIMITS``).
    * YELLOW when ``pii_present == False`` (anonymized records).

PII discipline (R.PF2 architectural commitment):
    The schema validator (``__post_init__``) enforces consent-tier ↔ PII
    consistency before bytes touch disk:
        * ``pii_present=True`` requires ``consent_tier="operator-authorized-identified"``
          AND non-empty ``pii_fields``.
        * ``pii_present=False`` requires empty ``pii_fields`` AND
          ``consent_tier="anonymized"``.
    Cedar policy ``operational_subkinds.cedar`` re-asserts the same
    invariant at the policy layer (see ``policy_eval.py``); the two layers
    are belt-and-suspenders. A schema-bypass attack still hits the Cedar
    rule, and a Cedar-bypass attack still hits the schema validator.

Blueprint authority:
    - section_02_v7_2_amendment.md §2.11.6 (schema)
    - section_02_v7_2_amendment.md §2.13 (POST_GATE_ALLOWLIST row)
    - section_02_v7_2_amendment.md §6 (Cedar policy)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from pipeline.vault.sub_kinds._canonical import (
    _coerce_str_tuple,
    from_canonical_json_bytes,
    to_canonical_json_bytes,
)

BLUEPRINT_DEPS: Final[dict[str, dict[str, object]]] = {
    "section_02_v7_2_amendment.md": {
        "version": "v7.2-DRAFT",
        "sections_implemented": [
            "§2.11.6 BeneficiaryRecord schema",
            "§2.13 operational-beneficiary-write allowlist row",
            "§6 operational_subkinds.cedar PII discipline",
        ],
    },
}

INTENT: Final[str] = "operational-beneficiary-write"
SUB_KIND: Final[str] = "beneficiary_records"
VAULT_SUBTREE: Final[str] = "operational/beneficiaries/"

CONSENT_TIER_ANONYMIZED: Final[str] = "anonymized"
CONSENT_TIER_OPERATOR_AUTHORIZED_IDENTIFIED: Final[str] = "operator-authorized-identified"
ALLOWED_CONSENT_TIERS: Final[frozenset[str]] = frozenset(
    {CONSENT_TIER_ANONYMIZED, CONSENT_TIER_OPERATOR_AUTHORIZED_IDENTIFIED}
)

# Severity is RED when PII is present, YELLOW otherwise. Default exposed for
# the registry; per-record severity is computed via :func:`severity_for`.
ADMIN_RISK_SEVERITY: Final[str] = "RED"
ADMIN_RISK_SEVERITY_ANONYMIZED: Final[str] = "YELLOW"


@dataclass(frozen=True, kw_only=True)
class BeneficiaryRecord:
    """One beneficiary record. PII discipline enforced at schema construction."""

    record_id: str
    beneficiary_opaque_id: str
    service: str
    outcome: str
    consent_tier: str
    pii_present: bool
    pii_fields: tuple[str, ...]
    captured_at: str

    def __post_init__(self) -> None:
        if not isinstance(self.record_id, str) or not self.record_id:
            raise ValueError("record_id must be a non-empty string")
        if not isinstance(self.beneficiary_opaque_id, str) or not self.beneficiary_opaque_id:
            raise ValueError("beneficiary_opaque_id must be a non-empty opaque id")
        if not isinstance(self.service, str) or not self.service:
            raise ValueError("service must be a non-empty string")
        if not isinstance(self.outcome, str):
            raise ValueError("outcome must be a string")
        if not isinstance(self.consent_tier, str):
            raise ValueError("consent_tier must be a string")
        if self.consent_tier not in ALLOWED_CONSENT_TIERS:
            raise ValueError(
                f"consent_tier must be in {sorted(ALLOWED_CONSENT_TIERS)}; "
                f"got {self.consent_tier!r}"
            )
        if not isinstance(self.pii_present, bool):
            raise ValueError("pii_present must be bool")
        if not isinstance(self.pii_fields, tuple):
            raise ValueError("pii_fields must be a tuple of strings")
        for i, f in enumerate(self.pii_fields):
            if not isinstance(f, str):
                raise ValueError(f"pii_fields[{i}] must be str")
        if not isinstance(self.captured_at, str) or not self.captured_at.endswith("Z"):
            raise ValueError("captured_at must be a UTC ISO-8601 string ending in 'Z'")
        # PII consent consistency — fail-closed at schema construction.
        if self.pii_present:
            if self.consent_tier != CONSENT_TIER_OPERATOR_AUTHORIZED_IDENTIFIED:
                raise ValueError(
                    "pii_present=True requires consent_tier='operator-authorized-identified'"
                )
            if not self.pii_fields:
                raise ValueError(
                    "pii_present=True requires non-empty pii_fields"
                )
        else:
            if self.consent_tier != CONSENT_TIER_ANONYMIZED:
                raise ValueError(
                    "pii_present=False requires consent_tier='anonymized'"
                )
            if self.pii_fields:
                raise ValueError(
                    "pii_present=False requires empty pii_fields"
                )


def severity_for(record: BeneficiaryRecord) -> str:
    """Return ``"RED"`` if the record carries PII, else ``"YELLOW"``."""
    if not isinstance(record, BeneficiaryRecord):
        raise TypeError(
            f"record must be BeneficiaryRecord, got {type(record).__name__}"
        )
    return ADMIN_RISK_SEVERITY if record.pii_present else ADMIN_RISK_SEVERITY_ANONYMIZED


def to_canonical_bytes(record: BeneficiaryRecord) -> bytes:
    if not isinstance(record, BeneficiaryRecord):
        raise TypeError(
            f"record must be BeneficiaryRecord, got {type(record).__name__}"
        )
    return to_canonical_json_bytes(record)


def from_canonical_bytes(payload: bytes) -> BeneficiaryRecord:
    parsed = from_canonical_json_bytes(payload)
    return BeneficiaryRecord(
        record_id=str(parsed["record_id"]),
        beneficiary_opaque_id=str(parsed["beneficiary_opaque_id"]),
        service=str(parsed["service"]),
        outcome=str(parsed["outcome"]),
        consent_tier=str(parsed["consent_tier"]),
        pii_present=bool(parsed["pii_present"]),
        pii_fields=_coerce_str_tuple(
            parsed.get("pii_fields", []), field="pii_fields"
        ),
        captured_at=str(parsed["captured_at"]),
    )


def record_id_for(record: BeneficiaryRecord) -> str:
    return record.record_id


__all__ = [
    "ADMIN_RISK_SEVERITY",
    "ADMIN_RISK_SEVERITY_ANONYMIZED",
    "ALLOWED_CONSENT_TIERS",
    "BLUEPRINT_DEPS",
    "BeneficiaryRecord",
    "CONSENT_TIER_ANONYMIZED",
    "CONSENT_TIER_OPERATOR_AUTHORIZED_IDENTIFIED",
    "INTENT",
    "SUB_KIND",
    "VAULT_SUBTREE",
    "from_canonical_bytes",
    "record_id_for",
    "severity_for",
    "to_canonical_bytes",
]
