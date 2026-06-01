"""§13.8.7 — State-rules card substrate.

Workspace-shared card YAMLs at `vault_shared/state_rules_card/<state>.yaml`
signed by SN-LLC's pinned public key. v0.2 first wave ships PA/CA/FL/TX/NY.

Per RT-21 closure + RT-C2-11 mirror — signature verification at every load is
MANDATORY (not optional). Card loader exposes `load_state_card` that
raises `StateCardSignatureError` on missing/invalid signature; the gate
predicate `F-DATACOLLECTOR-PII-LEAK-IN-OUTBOUND.state_card_signature_invalid`
converts the exception into a fail-closed gate verdict.

yaml.safe_load only per RT-27 closure / R-DATACOLLECTOR-CARD-SAFE-LOAD.
"""
from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Literal

import yaml
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

from pipeline.orchestrator.seats.data_collector import StateRulesCardEntry


# v0.2 first-wave registered states; expansion via SN-LLC card release.
SUPPORTED_STATES: tuple[str, ...] = ("PA", "CA", "FL", "TX", "NY")


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------

class StateCardError(Exception):
    """Base for state-rules card substrate errors."""


class StateCardNotFound(StateCardError):
    """Card file does not exist for the requested state code."""


class StateCardSignatureError(StateCardError):
    """Ed25519 signature missing or invalid against pinned SN-LLC public key."""


class StateCardSchemaError(StateCardError):
    """Card YAML parsed but failed schema validation."""


class StateCardStateUnsupported(StateCardError):
    """Requested state code is not in SUPPORTED_STATES (no card published)."""


class StateOptInNotGranted(StateCardError):
    """Operator has not opted in to the requested state's card."""


# ---------------------------------------------------------------------------
# Signature verification — Ed25519 over canonical-JSON of card content
# ---------------------------------------------------------------------------

def _canonical_payload(content: dict) -> bytes:
    """Canonical-JSON over card content fields EXCLUDING signature.

    The signature is computed over a deterministic JSON encoding of every
    field except `signature` itself.
    """
    payload = {k: v for k, v in content.items() if k != "signature"}
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def verify_card_signature(content: dict, *, sn_llc_pubkey: bytes) -> None:
    """Raises StateCardSignatureError on verify failure."""
    signature = content.get("signature")
    if not isinstance(signature, (bytes, bytearray)) or not signature:
        raise StateCardSignatureError("card signature missing or empty")
    try:
        pub = Ed25519PublicKey.from_public_bytes(sn_llc_pubkey)
        pub.verify(bytes(signature), _canonical_payload(content))
    except (InvalidSignature, ValueError) as exc:
        raise StateCardSignatureError(
            f"card signature invalid: {exc}"
        ) from exc


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------

def load_state_card(
    card_dir: Path,
    state_code: str,
    *,
    sn_llc_pubkey: bytes,
) -> StateRulesCardEntry:
    """Load a single state card with mandatory signature verification.

    Raises:
        StateCardStateUnsupported — state not in v0.2 first-wave set.
        StateCardNotFound — card file missing on disk.
        StateCardSignatureError — signature missing or verify failed.
        StateCardSchemaError — YAML parsed but schema invalid.
    """
    if state_code not in SUPPORTED_STATES:
        raise StateCardStateUnsupported(
            f"state {state_code!r} not in v0.2 first wave {SUPPORTED_STATES}"
        )
    path = Path(card_dir) / f"{state_code}.yaml"
    if not path.exists():
        raise StateCardNotFound(f"card missing on disk: {path}")
    if path.is_symlink():
        raise StateCardSchemaError(f"refusing symlink card path: {path}")
    with open(path, "rb") as fp:
        raw = yaml.safe_load(fp)
    if not isinstance(raw, dict):
        raise StateCardSchemaError(f"card YAML root must be dict, got {type(raw).__name__}")

    verify_card_signature(raw, sn_llc_pubkey=sn_llc_pubkey)
    try:
        return StateRulesCardEntry(
            state_code=raw["state_code"],
            email_disclaimers=list(raw.get("email_disclaimers", [])),
            sms_quiet_hours=tuple(raw.get("sms_quiet_hours", ("00:00", "00:00"))),  # type: ignore[arg-type]
            sms_required_opt_out_shortcodes=list(raw.get("sms_required_opt_out_shortcodes", [])),
            sms_minimum_consent_age_days=int(raw.get("sms_minimum_consent_age_days", 0)),
            voice_quiet_hours=tuple(raw.get("voice_quiet_hours", ("00:00", "00:00"))),  # type: ignore[arg-type]
            voice_automated_call_disclosure_script=str(raw.get("voice_automated_call_disclosure_script", "")),
            voice_state_dnc_check_required=bool(raw.get("voice_state_dnc_check_required", False)),
            whatsapp_disclaimers=list(raw.get("whatsapp_disclaimers", [])),
            card_version=str(raw["card_version"]),
            signed_by_sn_llc_at_utc=_parse_dt(raw["signed_by_sn_llc_at_utc"]),
            signed_by_sn_llc_pubkey_fingerprint=str(raw["signed_by_sn_llc_pubkey_fingerprint"]),
            signature=bytes(raw["signature"]),
        )
    except (TypeError, ValueError, KeyError) as exc:
        raise StateCardSchemaError(str(exc)) from exc


def _parse_dt(value) -> datetime:
    from datetime import timezone
    if isinstance(value, datetime):
        return value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    if isinstance(value, str):
        if value.endswith("Z"):
            value = value[:-1] + "+00:00"
        return datetime.fromisoformat(value)
    raise StateCardSchemaError(f"unparseable datetime: {value!r}")


# ---------------------------------------------------------------------------
# Operator opt-in resolver
# ---------------------------------------------------------------------------

def load_opted_in_states(opt_in_path: Path) -> frozenset[str]:
    """Read the operator-signed opt-in record; return the set of opted-in states.

    Schema expected: top-level dict with `opted_in_states: list[str]`. Returns
    an empty frozenset if the file does not exist (ships empty by default).
    """
    path = Path(opt_in_path)
    if not path.exists():
        return frozenset()
    if path.is_symlink():
        raise StateCardSchemaError(f"refusing symlink opt-in record: {path}")
    with open(path, "rb") as fp:
        raw = yaml.safe_load(fp)
    if raw is None:
        return frozenset()
    if not isinstance(raw, dict):
        raise StateCardSchemaError(f"opt-in record root must be dict, got {type(raw).__name__}")
    opted = raw.get("opted_in_states", [])
    if not isinstance(opted, list):
        raise StateCardSchemaError("opted_in_states must be a list")
    return frozenset(str(s).upper() for s in opted)


# ---------------------------------------------------------------------------
# Helper — author card YAML for fixtures / tests
# ---------------------------------------------------------------------------

def author_card_yaml(
    entry: StateRulesCardEntry,
    *,
    sn_llc_signing_key,
) -> dict:
    """Build a signed card YAML payload from an entry + signing key.

    Used by fixture builders and SN-LLC release tooling. Returns a dict suitable
    for yaml.safe_dump.
    """
    payload = {
        "state_code": entry.state_code,
        "email_disclaimers": list(entry.email_disclaimers),
        "sms_quiet_hours": list(entry.sms_quiet_hours),
        "sms_required_opt_out_shortcodes": list(entry.sms_required_opt_out_shortcodes),
        "sms_minimum_consent_age_days": entry.sms_minimum_consent_age_days,
        "voice_quiet_hours": list(entry.voice_quiet_hours),
        "voice_automated_call_disclosure_script": entry.voice_automated_call_disclosure_script,
        "voice_state_dnc_check_required": entry.voice_state_dnc_check_required,
        "whatsapp_disclaimers": list(entry.whatsapp_disclaimers),
        "card_version": entry.card_version,
        "signed_by_sn_llc_at_utc": entry.signed_by_sn_llc_at_utc.isoformat(),
        "signed_by_sn_llc_pubkey_fingerprint": entry.signed_by_sn_llc_pubkey_fingerprint,
    }
    msg = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    payload["signature"] = sn_llc_signing_key.sign(msg)
    return payload


__all__ = [
    "SUPPORTED_STATES",
    "StateCardError",
    "StateCardNotFound",
    "StateCardSchemaError",
    "StateCardSignatureError",
    "StateCardStateUnsupported",
    "StateOptInNotGranted",
    "author_card_yaml",
    "load_opted_in_states",
    "load_state_card",
    "verify_card_signature",
]
