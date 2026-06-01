"""``financials`` sub-kind — line-item ledger records. [§2.11.2, §2.13]

Schema, canonical-bytes encode/decode, and intent constant for operational
financial line items (vendor invoices, reimbursements, internal transfers).

Severity YELLOW. Numeric integrity is preserved by storing amounts in
minor units (e.g. cents) as ``int`` rather than ``float`` — the architecture
treats currency drift as a P0 reporting risk per §R.3.

Blueprint authority:
    - section_02_v7_2_amendment.md §2.11.2 (schema)
    - section_02_v7_2_amendment.md §2.13 (POST_GATE_ALLOWLIST row)
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final

from pipeline.vault.sub_kinds._canonical import (
    from_canonical_json_bytes,
    to_canonical_json_bytes,
)

BLUEPRINT_DEPS: Final[dict[str, dict[str, object]]] = {
    "section_02_v7_2_amendment.md": {
        "version": "v7.2-DRAFT",
        "sections_implemented": [
            "§2.11.2 FinancialsRecord schema",
            "§2.13 operational-financials-write allowlist row",
        ],
    },
}

INTENT: Final[str] = "operational-financials-write"
SUB_KIND: Final[str] = "financials"
VAULT_SUBTREE: Final[str] = "operational/financials/"
ADMIN_RISK_SEVERITY: Final[str] = "YELLOW"


@dataclass(frozen=True, kw_only=True)
class FinancialsRecord:
    """One financial line item. Amount is in smallest currency units (e.g. cents)."""

    record_id: str
    amount_minor_units: int
    currency: str
    posted_at: str
    category: str
    description: str
    vendor: str

    def __post_init__(self) -> None:
        if not isinstance(self.record_id, str) or not self.record_id:
            raise ValueError("record_id must be a non-empty string")
        # Reject bool explicitly — Python ``bool`` is a subclass of ``int``
        # and would silently parse as 0 or 1 minor units.
        if not isinstance(self.amount_minor_units, int) or isinstance(
            self.amount_minor_units, bool
        ):
            raise ValueError(
                "amount_minor_units must be int (use minor units, e.g. cents)"
            )
        if not isinstance(self.currency, str) or len(self.currency) != 3 or not self.currency.isalpha() or self.currency != self.currency.upper():
            raise ValueError(
                "currency must be a 3-letter uppercase ISO-4217 code"
            )
        if not isinstance(self.posted_at, str) or not self.posted_at.endswith("Z"):
            raise ValueError("posted_at must be a UTC ISO-8601 string ending in 'Z'")
        if not isinstance(self.category, str):
            raise ValueError("category must be a string")
        if not isinstance(self.description, str):
            raise ValueError("description must be a string")
        if not isinstance(self.vendor, str):
            raise ValueError("vendor must be a string (may be empty)")


def to_canonical_bytes(record: FinancialsRecord) -> bytes:
    if not isinstance(record, FinancialsRecord):
        raise TypeError(
            f"record must be FinancialsRecord, got {type(record).__name__}"
        )
    return to_canonical_json_bytes(record)


def from_canonical_bytes(payload: bytes) -> FinancialsRecord:
    parsed = from_canonical_json_bytes(payload)
    return FinancialsRecord(
        record_id=str(parsed["record_id"]),
        amount_minor_units=int(parsed["amount_minor_units"]),
        currency=str(parsed["currency"]),
        posted_at=str(parsed["posted_at"]),
        category=str(parsed["category"]),
        description=str(parsed["description"]),
        vendor=str(parsed["vendor"]),
    )


def record_id_for(record: FinancialsRecord) -> str:
    return record.record_id


__all__ = [
    "ADMIN_RISK_SEVERITY",
    "BLUEPRINT_DEPS",
    "FinancialsRecord",
    "INTENT",
    "SUB_KIND",
    "VAULT_SUBTREE",
    "from_canonical_bytes",
    "record_id_for",
    "to_canonical_bytes",
]
