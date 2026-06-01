"""§13.9.6 + §13.16.6.2 RT-C2-11 — Inbound classification register substrate.

Operator-curated map `(recipient_id, field_class) → classification_status`.
Stored at `orgs/<slug>/data_collector/classification_register.signed.yaml`.
Operator-signed (Ed25519). Per RT-C2-11, signature is RE-verified on every
inbound write — mirrors §15 v1 §15.9.5 NF-01 runtime-immutability self-check.

Entries:

    {
      "entries": {
        "<recipient_id>::<field_class>": {
          "classification_status": "OPERATOR_CLASSIFIED" | "DEFAULT_CONFIDENTIAL_PENDING_REVIEW",
          "classification_value": "Public" | "Shareable" | "Confidential" | null,
          "operator_at_utc": "<ISO8601>"
        },
        ...
      },
      "signed_at_utc": "<ISO8601>",
      "signature": <bytes>
    }

yaml.safe_load only per RT-27 / R-DATACOLLECTOR-CARD-SAFE-LOAD.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

import yaml
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey


CLASSIFICATION_STATUS_OPERATOR_CLASSIFIED: str = "OPERATOR_CLASSIFIED"
CLASSIFICATION_STATUS_DEFAULT_CONFIDENTIAL_PENDING_REVIEW: str = "DEFAULT_CONFIDENTIAL_PENDING_REVIEW"
CLASSIFICATION_STATUS_UNSET: str = "UNSET"
PERMITTED_CLASSIFICATION_VALUES: frozenset[str] = frozenset({"Public", "Shareable", "Confidential"})


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------

class ClassificationRegisterError(Exception):
    """Base error."""


class ClassificationRegisterNotFound(ClassificationRegisterError):
    pass


class ClassificationRegisterSignatureError(ClassificationRegisterError):
    """Ed25519 signature missing or verify failed (RT-C2-11)."""


class ClassificationRegisterSchemaError(ClassificationRegisterError):
    pass


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

@dataclass(frozen=True, kw_only=True)
class ClassificationEntry:
    recipient_id: str
    field_class: str
    classification_status: Literal["OPERATOR_CLASSIFIED", "DEFAULT_CONFIDENTIAL_PENDING_REVIEW", "UNSET"]
    classification_value: str | None  # Public / Shareable / Confidential
    operator_at_utc: datetime | None


@dataclass(frozen=True, kw_only=True)
class ClassificationRegister:
    entries: dict[tuple[str, str], ClassificationEntry]
    signed_at_utc: datetime
    signature: bytes


# ---------------------------------------------------------------------------
# Canonical-JSON for signing
# ---------------------------------------------------------------------------

def _canonical_payload(entries_serialized: dict, signed_at_utc: str) -> bytes:
    payload = {
        "entries": entries_serialized,
        "signed_at_utc": signed_at_utc,
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _serialize_entries(entries: dict[tuple[str, str], ClassificationEntry]) -> dict:
    out: dict = {}
    for (recipient_id, field_class), entry in sorted(entries.items()):
        key = f"{recipient_id}::{field_class}"
        out[key] = {
            "classification_status": entry.classification_status,
            "classification_value": entry.classification_value,
            "operator_at_utc": entry.operator_at_utc.isoformat() if entry.operator_at_utc else None,
        }
    return out


def _deserialize_entries(raw: dict) -> dict[tuple[str, str], ClassificationEntry]:
    out: dict[tuple[str, str], ClassificationEntry] = {}
    for key, val in raw.items():
        if "::" not in key:
            raise ClassificationRegisterSchemaError(f"malformed entry key: {key!r}")
        recipient_id, field_class = key.split("::", 1)
        if not isinstance(val, dict):
            raise ClassificationRegisterSchemaError(f"entry {key!r} not a dict")
        status = val.get("classification_status")
        if status not in {
            CLASSIFICATION_STATUS_OPERATOR_CLASSIFIED,
            CLASSIFICATION_STATUS_DEFAULT_CONFIDENTIAL_PENDING_REVIEW,
            CLASSIFICATION_STATUS_UNSET,
        }:
            raise ClassificationRegisterSchemaError(f"entry {key!r} bad status: {status!r}")
        value = val.get("classification_value")
        if value is not None and value not in PERMITTED_CLASSIFICATION_VALUES:
            raise ClassificationRegisterSchemaError(f"entry {key!r} bad value: {value!r}")
        op_at_str = val.get("operator_at_utc")
        op_at = _parse_dt(op_at_str) if op_at_str else None
        out[(recipient_id, field_class)] = ClassificationEntry(
            recipient_id=recipient_id,
            field_class=field_class,
            classification_status=status,
            classification_value=value,
            operator_at_utc=op_at,
        )
    return out


def _parse_dt(value) -> datetime:
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    if isinstance(value, str):
        if value.endswith("Z"):
            value = value[:-1] + "+00:00"
        return datetime.fromisoformat(value)
    raise ClassificationRegisterSchemaError(f"unparseable datetime: {value!r}")


# ---------------------------------------------------------------------------
# Load + verify
# ---------------------------------------------------------------------------

def load_classification_register(
    path: Path,
    *,
    operator_pubkey: bytes,
) -> ClassificationRegister:
    """Atomic read of operator-signed register with mandatory signature verify.

    Per RT-C2-11 — this function MUST be invoked at every inbound write to
    operational-data sub-kind. The signature is re-checked on each call so
    that any tampering between writes fail-closes.
    """
    path = Path(path)
    if not path.exists():
        raise ClassificationRegisterNotFound(f"register missing: {path}")
    if path.is_symlink():
        raise ClassificationRegisterSchemaError(f"refusing symlink register path: {path}")
    with open(path, "rb") as fp:
        raw = yaml.safe_load(fp)
    if not isinstance(raw, dict):
        raise ClassificationRegisterSchemaError("register root must be dict")
    entries_raw = raw.get("entries", {})
    if not isinstance(entries_raw, dict):
        raise ClassificationRegisterSchemaError("entries must be dict")
    signed_at_str = raw.get("signed_at_utc")
    if not isinstance(signed_at_str, str):
        raise ClassificationRegisterSchemaError("signed_at_utc missing or non-string")
    import base64
    signature_b64 = raw.get("signature_b64")
    if not isinstance(signature_b64, str):
        raise ClassificationRegisterSignatureError("signature_b64 missing or non-string")
    signature = base64.b64decode(signature_b64)

    payload = _canonical_payload(entries_raw, signed_at_str)
    try:
        Ed25519PublicKey.from_public_bytes(operator_pubkey).verify(signature, payload)
    except (InvalidSignature, ValueError) as exc:
        raise ClassificationRegisterSignatureError(
            f"register signature invalid: {exc}"
        ) from exc
    return ClassificationRegister(
        entries=_deserialize_entries(entries_raw),
        signed_at_utc=_parse_dt(signed_at_str),
        signature=signature,
    )


def write_classification_register(
    path: Path,
    *,
    entries: dict[tuple[str, str], ClassificationEntry],
    signed_at_utc: datetime,
    operator_signing_key,
) -> ClassificationRegister:
    """Author + write a signed classification register."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    serialized = _serialize_entries(entries)
    signed_at_str = signed_at_utc.isoformat()
    payload = _canonical_payload(serialized, signed_at_str)
    signature = operator_signing_key.sign(payload)
    import base64
    with open(path, "w") as fp:
        yaml.safe_dump(
            {
                "entries": serialized,
                "signed_at_utc": signed_at_str,
                "signature_b64": base64.b64encode(signature).decode("ascii"),
            },
            fp,
            sort_keys=True,
            default_flow_style=False,
        )
    return ClassificationRegister(
        entries=dict(entries),
        signed_at_utc=signed_at_utc,
        signature=signature,
    )


def lookup_classification(
    register: ClassificationRegister,
    recipient_id: str,
    field_class: str,
) -> ClassificationEntry | None:
    return register.entries.get((recipient_id, field_class))


__all__ = [
    "CLASSIFICATION_STATUS_DEFAULT_CONFIDENTIAL_PENDING_REVIEW",
    "CLASSIFICATION_STATUS_OPERATOR_CLASSIFIED",
    "CLASSIFICATION_STATUS_UNSET",
    "PERMITTED_CLASSIFICATION_VALUES",
    "ClassificationEntry",
    "ClassificationRegister",
    "ClassificationRegisterError",
    "ClassificationRegisterNotFound",
    "ClassificationRegisterSchemaError",
    "ClassificationRegisterSignatureError",
    "load_classification_register",
    "lookup_classification",
    "write_classification_register",
]
