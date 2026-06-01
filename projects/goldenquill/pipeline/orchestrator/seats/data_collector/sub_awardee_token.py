"""§13.6.0 + §13.8.8 — Sub-awardee token register substrate.

Per-recipient × per-channel × per-grant shared-secret tokens. Hardened across
Cycle 1 + Cycle 2 closures:

- RT-10: channel-binding (token bound to exactly one channel at issuance).
- RT-11: AEAD authentication (AES-GCM) — tag verified BEFORE token value
  accepted.
- RT-12: explicit revocation field (`revoked: bool`) — revoked tokens
  rejected regardless of `rotates_at_utc`.
- RT-C2-06: uuid4 token_id + runtime uniqueness scan at issue.
- RT-C2-07: per-token 12-byte random nonce; nonce uniqueness validator.

Per-recipient × per-channel storage path:
    `orgs/<slug>/data_collector/per_recipient_tokens/<grant_id>__<recipient_id>__<channel>.signed.yaml`
"""
from __future__ import annotations

import json
import os
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

import yaml
from cryptography.exceptions import InvalidSignature, InvalidTag
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from pipeline.orchestrator.seats.data_collector import SubAwardeeToken


AEAD_NONCE_BYTES: int = 12  # 96-bit per AES-GCM recommended; RT-C2-07
AEAD_KEY_BYTES: int = 32  # 256-bit AES-GCM key
TOKEN_SECRET_BYTES: int = 32  # 256-bit secret per §13.6.0


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------

class TokenError(Exception):
    """Base for sub-awardee token substrate errors."""


class TokenNotFound(TokenError):
    """No token file matches the requested (grant, recipient, channel) triple."""


class TokenCollisionError(TokenError):
    """token_id collision detected at issue (RT-C2-06)."""


class TokenSignatureError(TokenError):
    """Operator Ed25519 signature missing or invalid on token record."""


class TokenSchemaError(TokenError):
    """Token YAML parsed but failed schema validation."""


class TokenAEADInvalid(TokenError):
    """AES-GCM authentication tag invalid (RT-11 closure)."""


# ---------------------------------------------------------------------------
# Storage path
# ---------------------------------------------------------------------------

def token_path(root: Path, grant_id: str, recipient_id: str, channel: str) -> Path:
    return Path(root) / f"{grant_id}__{recipient_id}__{channel}.signed.yaml"


# ---------------------------------------------------------------------------
# Issue — RT-10 + RT-11 + RT-C2-06 + RT-C2-07
# ---------------------------------------------------------------------------

def issue_token(
    *,
    grant_id: str,
    recipient_id: str,
    channel: Literal["email", "sms", "voice", "telegram", "whatsapp"],
    aead_key: bytes,
    operator_signing_key,
    issued_at_utc: datetime,
    rotates_at_utc: datetime,
    existing_token_ids: frozenset[str] = frozenset(),
) -> tuple[SubAwardeeToken, bytes]:
    """Issue a new token bound to (grant, recipient, channel).

    Returns (SubAwardeeToken record, plaintext_secret). The caller is
    responsible for transmitting `plaintext_secret` to the recipient OOB and
    persisting the SubAwardeeToken record to disk.

    `aead_key` is the KFR-classified-confidential 256-bit AES-GCM key
    per §13.6.0 + v7.0.4 §1.1 KFR-signature discipline.
    """
    if len(aead_key) != AEAD_KEY_BYTES:
        raise TokenSchemaError(f"aead_key must be {AEAD_KEY_BYTES} bytes; got {len(aead_key)}")
    token_id = str(uuid.uuid4())
    if token_id in existing_token_ids:
        # RT-C2-06: probability is ~5e-37, but the check is mandatory.
        raise TokenCollisionError(f"token_id {token_id!r} collision against existing register")
    plaintext = os.urandom(TOKEN_SECRET_BYTES)
    nonce = os.urandom(AEAD_NONCE_BYTES)
    aead = AESGCM(aead_key)
    aad = _aad_for_token(grant_id=grant_id, recipient_id=recipient_id, channel=channel, token_id=token_id)
    ciphertext = aead.encrypt(nonce, plaintext, aad)
    record_unsigned = {
        "token_id": token_id,
        "grant_id": grant_id,
        "recipient_id": recipient_id,
        "channel_binding": channel,
        "secret_value_ciphertext": ciphertext,
        "aead_nonce": nonce,
        "issued_at_utc": issued_at_utc.isoformat(),
        "rotates_at_utc": rotates_at_utc.isoformat(),
        "revoked": False,
        "revoked_at_utc": None,
    }
    signature = operator_signing_key.sign(_canonical_record_payload(record_unsigned))
    token = SubAwardeeToken(
        token_id=token_id,
        grant_id=grant_id,
        recipient_id=recipient_id,
        channel_binding=channel,
        secret_value_ciphertext=ciphertext,
        aead_nonce=nonce,
        issued_at_utc=_ensure_utc(issued_at_utc),
        rotates_at_utc=_ensure_utc(rotates_at_utc),
        revoked=False,
        revoked_at_utc=None,
        operator_signature=signature,
    )
    return token, plaintext


def _aad_for_token(*, grant_id: str, recipient_id: str, channel: str, token_id: str) -> bytes:
    """AEAD additional-authenticated-data binds ciphertext to the token's identity."""
    return json.dumps(
        {"g": grant_id, "r": recipient_id, "c": channel, "t": token_id},
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _canonical_record_payload(record: dict) -> bytes:
    """Canonical-JSON of token record EXCLUDING operator_signature.

    Bytes fields are b64-encoded for stable JSON. The canonical encoding
    binds: grant_id, recipient_id, channel_binding, token_id,
    rotates_at_utc, revoked, revoked_at_utc, plus the ciphertext+nonce
    (so that tampering with either is signature-detected).
    """
    import base64
    payload = {
        "token_id": record["token_id"],
        "grant_id": record["grant_id"],
        "recipient_id": record["recipient_id"],
        "channel_binding": record["channel_binding"],
        "secret_value_ciphertext_b64": base64.b64encode(record["secret_value_ciphertext"]).decode("ascii"),
        "aead_nonce_b64": base64.b64encode(record["aead_nonce"]).decode("ascii"),
        "issued_at_utc": record["issued_at_utc"],
        "rotates_at_utc": record["rotates_at_utc"],
        "revoked": record["revoked"],
        "revoked_at_utc": record["revoked_at_utc"],
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _ensure_utc(dt: datetime) -> datetime:
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


# ---------------------------------------------------------------------------
# Persist / read
# ---------------------------------------------------------------------------

def write_token(root: Path, token: SubAwardeeToken) -> None:
    root = Path(root)
    root.mkdir(parents=True, exist_ok=True)
    path = token_path(root, token.grant_id, token.recipient_id, token.channel_binding)
    if path.is_symlink():
        raise TokenSchemaError(f"refusing symlink token path: {path}")
    with open(path, "w") as fp:
        yaml.safe_dump(_token_to_dict(token), fp, sort_keys=True, default_flow_style=False)


def read_token(root: Path, grant_id: str, recipient_id: str, channel: str) -> SubAwardeeToken:
    path = token_path(root, grant_id, recipient_id, channel)
    if not path.exists():
        raise TokenNotFound(f"no token file for {grant_id}/{recipient_id}/{channel}: {path}")
    if path.is_symlink():
        raise TokenSchemaError(f"refusing symlink token path: {path}")
    with open(path, "rb") as fp:
        raw = yaml.safe_load(fp)
    return _dict_to_token(raw)


def _token_to_dict(token: SubAwardeeToken) -> dict:
    import base64
    return {
        "token_id": token.token_id,
        "grant_id": token.grant_id,
        "recipient_id": token.recipient_id,
        "channel_binding": token.channel_binding,
        "secret_value_ciphertext_b64": base64.b64encode(token.secret_value_ciphertext).decode("ascii"),
        "aead_nonce_b64": base64.b64encode(token.aead_nonce).decode("ascii"),
        "issued_at_utc": token.issued_at_utc.isoformat(),
        "rotates_at_utc": token.rotates_at_utc.isoformat(),
        "revoked": token.revoked,
        "revoked_at_utc": token.revoked_at_utc.isoformat() if token.revoked_at_utc else None,
        "operator_signature_b64": base64.b64encode(token.operator_signature).decode("ascii"),
    }


def _dict_to_token(data: dict) -> SubAwardeeToken:
    import base64
    try:
        ct = base64.b64decode(data["secret_value_ciphertext_b64"])
        nonce = base64.b64decode(data["aead_nonce_b64"])
        sig = base64.b64decode(data["operator_signature_b64"])
        return SubAwardeeToken(
            token_id=str(data["token_id"]),
            grant_id=str(data["grant_id"]),
            recipient_id=str(data["recipient_id"]),
            channel_binding=str(data["channel_binding"]),  # type: ignore[arg-type]
            secret_value_ciphertext=ct,
            aead_nonce=nonce,
            issued_at_utc=_parse_dt(data["issued_at_utc"]),
            rotates_at_utc=_parse_dt(data["rotates_at_utc"]),
            revoked=bool(data["revoked"]),
            revoked_at_utc=_parse_dt(data["revoked_at_utc"]) if data["revoked_at_utc"] else None,
            operator_signature=sig,
        )
    except (KeyError, ValueError, TypeError) as exc:
        raise TokenSchemaError(str(exc)) from exc


def _parse_dt(value) -> datetime:
    if isinstance(value, datetime):
        return _ensure_utc(value)
    if isinstance(value, str):
        if value.endswith("Z"):
            value = value[:-1] + "+00:00"
        return datetime.fromisoformat(value)
    raise TokenSchemaError(f"unparseable datetime: {value!r}")


# ---------------------------------------------------------------------------
# Validate — RT-10 + RT-11 + RT-12
# ---------------------------------------------------------------------------

@dataclass(frozen=True, kw_only=True)
class TokenValidationResult:
    valid: bool
    reason: str | None
    token_id: str | None = None


def validate_token_record(
    token: SubAwardeeToken,
    *,
    operator_pubkey: bytes,
    expected_channel: str,
    inbound_at_utc: datetime,
    aead_key: bytes,
    presented_plaintext: bytes,
) -> TokenValidationResult:
    """Validate a token record under per-channel binding + AEAD + revocation.

    Failure reasons (sub-tag mapping per §13.16.4 + §13.16.6.2):
    - `channel_binding_mismatch` (RT-10)
    - `revoked_token_replay` (RT-12)
    - `stale` (token past rotates_at_utc)
    - `aead_tag_invalid` (RT-11)
    - `operator_signature_invalid`
    - `mismatch` (plaintext mismatch — forged token)
    """
    if token.channel_binding != expected_channel:
        return TokenValidationResult(
            valid=False, reason="channel_binding_mismatch", token_id=token.token_id,
        )
    if token.revoked:
        return TokenValidationResult(
            valid=False, reason="revoked_token_replay", token_id=token.token_id,
        )
    if _ensure_utc(inbound_at_utc) >= _ensure_utc(token.rotates_at_utc):
        return TokenValidationResult(
            valid=False, reason="stale", token_id=token.token_id,
        )
    # Verify operator Ed25519 signature.
    record_payload = _canonical_record_payload({
        "token_id": token.token_id,
        "grant_id": token.grant_id,
        "recipient_id": token.recipient_id,
        "channel_binding": token.channel_binding,
        "secret_value_ciphertext": token.secret_value_ciphertext,
        "aead_nonce": token.aead_nonce,
        "issued_at_utc": token.issued_at_utc.isoformat(),
        "rotates_at_utc": token.rotates_at_utc.isoformat(),
        "revoked": token.revoked,
        "revoked_at_utc": token.revoked_at_utc.isoformat() if token.revoked_at_utc else None,
    })
    try:
        Ed25519PublicKey.from_public_bytes(operator_pubkey).verify(token.operator_signature, record_payload)
    except (InvalidSignature, ValueError):
        return TokenValidationResult(
            valid=False, reason="operator_signature_invalid", token_id=token.token_id,
        )
    # Decrypt + verify AEAD tag.
    aad = _aad_for_token(
        grant_id=token.grant_id,
        recipient_id=token.recipient_id,
        channel=token.channel_binding,
        token_id=token.token_id,
    )
    try:
        plaintext = AESGCM(aead_key).decrypt(token.aead_nonce, token.secret_value_ciphertext, aad)
    except InvalidTag:
        return TokenValidationResult(
            valid=False, reason="aead_tag_invalid", token_id=token.token_id,
        )
    if plaintext != presented_plaintext:
        return TokenValidationResult(
            valid=False, reason="mismatch", token_id=token.token_id,
        )
    return TokenValidationResult(valid=True, reason=None, token_id=token.token_id)


def revoke_token(token: SubAwardeeToken, *, revoked_at_utc: datetime, operator_signing_key) -> SubAwardeeToken:
    """Mark a token revoked; re-sign the record with the operator key."""
    record = {
        "token_id": token.token_id,
        "grant_id": token.grant_id,
        "recipient_id": token.recipient_id,
        "channel_binding": token.channel_binding,
        "secret_value_ciphertext": token.secret_value_ciphertext,
        "aead_nonce": token.aead_nonce,
        "issued_at_utc": token.issued_at_utc.isoformat(),
        "rotates_at_utc": token.rotates_at_utc.isoformat(),
        "revoked": True,
        "revoked_at_utc": revoked_at_utc.isoformat(),
    }
    new_sig = operator_signing_key.sign(_canonical_record_payload(record))
    import dataclasses as _dc
    return _dc.replace(
        token,
        revoked=True,
        revoked_at_utc=_ensure_utc(revoked_at_utc),
        operator_signature=new_sig,
    )


def collect_existing_token_ids(root: Path, grant_id: str) -> frozenset[str]:
    """Scan token register for an existing (grant_id, *) to check uuid uniqueness."""
    root = Path(root)
    if not root.exists():
        return frozenset()
    seen: set[str] = set()
    for path in root.glob(f"{grant_id}__*.signed.yaml"):
        try:
            with open(path, "rb") as fp:
                raw = yaml.safe_load(fp)
            if isinstance(raw, dict) and "token_id" in raw:
                seen.add(str(raw["token_id"]))
        except (OSError, yaml.YAMLError):
            continue
    return frozenset(seen)


__all__ = [
    "AEAD_KEY_BYTES",
    "AEAD_NONCE_BYTES",
    "TOKEN_SECRET_BYTES",
    "TokenAEADInvalid",
    "TokenCollisionError",
    "TokenError",
    "TokenNotFound",
    "TokenSchemaError",
    "TokenSignatureError",
    "TokenValidationResult",
    "collect_existing_token_ids",
    "issue_token",
    "read_token",
    "revoke_token",
    "token_path",
    "validate_token_record",
    "write_token",
]
