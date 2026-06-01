"""Coefficient Registry — workspace-shared SN-LLC-signed asset class. [§2.14, §17.4]

The Coefficient Registry carries per-model dollars/watt-hours coefficients
for every model Tilth can route to, plus per-hardware-SKU baseline metrics
for local nodes. SN-LLC publishes; Tilth deployments verify the Ed25519
signature against the white-glove-pinned SN-LLC public key BEFORE loading.

Trust mechanism mirrors v7.0.7 §6.1 router-template signing byte-for-byte:
canonical-JSON over all fields except ``sn_llc_signature_ed25519``, sorted
keys, no insignificant whitespace, UTF-8.

Blueprint authority:
    - section_02_v7_4_coefficient_registry_amendment.md §2.14.* (schema, trust mechanism)
    - section_17_watts_per_funding_action.md §17.4 (Cycle Accountant read interface)
    - section_04_v2_x_z_wpfa_amendment.md §5.1.WPFA.{1,2,3} (failure codes)
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Final, Iterable, Protocol, runtime_checkable

from pipeline.vault.sub_kinds._canonical import to_canonical_json_bytes


BLUEPRINT_DEPS: Final[dict[str, dict[str, object]]] = {
    "section_02_v7_4_coefficient_registry_amendment.md": {
        "version": "v7.4-LOCKED-2026-05-11",
        "sections_implemented": [
            "§2.14.2 CoefficientRegistry + CoefficientEntry shapes",
            "§2.14.3 invariants",
            "§2.14.4 trust mechanism (mirrors v7.0.7 §6.1)",
            "§2.14.11 loader interface",
        ],
    },
}

_SEMVER_RE: Final[re.Pattern[str]] = re.compile(r"^\d+\.\d+\.\d+$")
_QUARTER_RE: Final[re.Pattern[str]] = re.compile(r"^Q[1-4]-\d{4}$")
_UTC_ISO_RE: Final[re.Pattern[str]] = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?Z$"
)
_DATE_ONLY_RE: Final[re.Pattern[str]] = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_SHA3_512_HEX_RE: Final[re.Pattern[str]] = re.compile(r"^[0-9a-f]{128}$")
_URL_RE: Final[re.Pattern[str]] = re.compile(r"^https?://[^\s]+$")
_ED25519_HEX_LEN: Final[int] = 128


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class CoefficientRegistryError(Exception):
    """Base error for Coefficient Registry load/verify failures."""


class CoefficientRegistryUnreadableError(CoefficientRegistryError):
    """The registry file does not exist or is not readable."""


class CoefficientRegistryUnsignedError(CoefficientRegistryError):
    """The registry file has no signature, empty signature, or wrong shape."""


class CoefficientSignatureInvalidError(CoefficientRegistryError):
    """The signature does not verify against the pinned pubkey."""

    def __init__(self, message: str, *, sub_tag: str) -> None:
        super().__init__(message)
        self.sub_tag = sub_tag


class CoefficientSchemaInvalidError(CoefficientRegistryError):
    """Schema invariants violated."""


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------


@dataclass(frozen=True, kw_only=True)
class CoefficientEntry:
    """Per-model coefficients."""

    model_id: str
    is_local: bool
    hardware_sku: str | None
    dollars_per_million_input_tokens_minor_units: int
    dollars_per_million_output_tokens_minor_units: int
    watt_hours_per_million_input_tokens_micro: int
    watt_hours_per_million_output_tokens_micro: int
    idle_watts_baseline_micro: int | None
    peak_watts_under_load_micro: int | None
    citation_url: str
    measurement_date: str
    measurement_methodology_url: str

    def __post_init__(self) -> None:
        if not isinstance(self.model_id, str) or not self.model_id:
            raise ValueError("model_id must be non-empty string")
        if not isinstance(self.is_local, bool):
            raise ValueError("is_local must be bool")
        for fname in (
            "dollars_per_million_input_tokens_minor_units",
            "dollars_per_million_output_tokens_minor_units",
            "watt_hours_per_million_input_tokens_micro",
            "watt_hours_per_million_output_tokens_micro",
        ):
            v = getattr(self, fname)
            if isinstance(v, bool) or not isinstance(v, int) or v < 0:
                raise ValueError(
                    f"{fname} must be non-negative int (A12 mandate; "
                    f"bool excluded)"
                )
        if self.is_local:
            if not isinstance(self.hardware_sku, str) or not self.hardware_sku:
                raise ValueError("is_local=True requires non-empty hardware_sku")
            for fname in (
                "idle_watts_baseline_micro",
                "peak_watts_under_load_micro",
            ):
                v = getattr(self, fname)
                if isinstance(v, bool) or not isinstance(v, int) or v < 0:
                    raise ValueError(
                        f"is_local=True requires non-negative int {fname}"
                    )
        else:
            if self.hardware_sku is not None:
                raise ValueError("is_local=False requires hardware_sku=None")
            if self.idle_watts_baseline_micro is not None:
                raise ValueError(
                    "is_local=False requires idle_watts_baseline_micro=None"
                )
            if self.peak_watts_under_load_micro is not None:
                raise ValueError(
                    "is_local=False requires peak_watts_under_load_micro=None"
                )
        if not _URL_RE.match(self.citation_url):
            raise ValueError("citation_url must match ^https?://")
        if not _DATE_ONLY_RE.match(self.measurement_date):
            raise ValueError("measurement_date must match ^\\d{4}-\\d{2}-\\d{2}$")
        if not _URL_RE.match(self.measurement_methodology_url):
            raise ValueError(
                "measurement_methodology_url must match ^https?://"
            )


@dataclass(frozen=True, kw_only=True)
class CoefficientRegistry:
    """Workspace-shared, SN-LLC-signed coefficient table."""

    schema_version: str
    quarter: str
    published_at: str
    sn_llc_signature_ed25519: str
    sn_llc_signing_key_id: str
    baseline_model_id: str
    entries: tuple[CoefficientEntry, ...]
    methodology_url: str
    rollback_pointer: str | None = None

    def __post_init__(self) -> None:
        if not _SEMVER_RE.match(self.schema_version):
            raise ValueError("schema_version must match semver")
        if not _QUARTER_RE.match(self.quarter):
            raise ValueError("quarter must match ^Q[1-4]-\\d{4}$")
        if not _UTC_ISO_RE.match(self.published_at):
            raise ValueError("published_at must be UTC ISO-8601 'Z'")
        if (
            not isinstance(self.sn_llc_signature_ed25519, str)
            or len(self.sn_llc_signature_ed25519) != _ED25519_HEX_LEN
            or not all(
                c in "0123456789abcdef"
                for c in self.sn_llc_signature_ed25519.lower()
            )
        ):
            raise ValueError(
                "sn_llc_signature_ed25519 must be 128-char lowercase hex"
            )
        if (
            not isinstance(self.sn_llc_signing_key_id, str)
            or not self.sn_llc_signing_key_id
        ):
            raise ValueError("sn_llc_signing_key_id must be non-empty string")
        if not isinstance(self.baseline_model_id, str) or not self.baseline_model_id:
            raise ValueError("baseline_model_id must be non-empty string")
        if not isinstance(self.entries, tuple) or not self.entries:
            raise ValueError("entries must be non-empty tuple of CoefficientEntry")
        # Unique model_ids
        seen: set[str] = set()
        baseline_in_entries = False
        for e in self.entries:
            if e.model_id in seen:
                raise ValueError(
                    f"duplicate model_id {e.model_id!r} in entries"
                )
            seen.add(e.model_id)
            if e.model_id == self.baseline_model_id:
                baseline_in_entries = True
        if not baseline_in_entries:
            raise ValueError(
                f"baseline_model_id {self.baseline_model_id!r} must resolve to "
                "an entry in entries"
            )
        if not _URL_RE.match(self.methodology_url):
            raise ValueError("methodology_url must match ^https?://")
        if self.rollback_pointer is not None and not _SHA3_512_HEX_RE.match(
            self.rollback_pointer
        ):
            raise ValueError(
                "rollback_pointer must be None or 128-hex-char SHA3-512"
            )

    def lookup(self, model_id: str) -> CoefficientEntry | None:
        """O(N) per-model lookup. Returns None if model_id absent."""
        for e in self.entries:
            if e.model_id == model_id:
                return e
        return None


# ---------------------------------------------------------------------------
# Canonical signing payload — mirrors v7.0.7 §6.1 router-template byte-for-byte
# ---------------------------------------------------------------------------


def to_signing_payload(registry: CoefficientRegistry) -> bytes:
    """Canonical-JSON bytes over all fields EXCEPT sn_llc_signature_ed25519.

    Mirrors v7.0.7 §6.1 router-template signing scope byte-for-byte.
    Sorted keys; compact separators; UTF-8.
    """
    if not isinstance(registry, CoefficientRegistry):
        raise TypeError(
            f"registry must be CoefficientRegistry, got {type(registry).__name__}"
        )
    # Use the canonical helper but strip the signature field
    from dataclasses import asdict

    payload = asdict(registry)
    payload.pop("sn_llc_signature_ed25519", None)
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode(
        "utf-8"
    )


def to_canonical_bytes(registry: CoefficientRegistry) -> bytes:
    """Full canonical-JSON bytes including signature (for on-disk hashing)."""
    return to_canonical_json_bytes(registry)


# ---------------------------------------------------------------------------
# Loader interface (Protocol-DI seam for signature verifier)
# ---------------------------------------------------------------------------


@runtime_checkable
class SignatureVerifyCallable(Protocol):
    """Ed25519 verifier — same shape as logician/gates/_protocols.py.

    Returns True iff `signature` is a valid Ed25519 signature over
    `message_bytes` under `public_key`. Raises on internal error
    (caller treats as fail-closed).
    """

    def __call__(
        self,
        message_bytes: bytes,
        signature: bytes,
        public_key: bytes,
    ) -> bool: ...


def load_active(
    *,
    registry_path: str | Path,
    pinned_pubkey_hex: str,
    signature_verify: SignatureVerifyCallable,
) -> CoefficientRegistry:
    """Load + verify the active Coefficient Registry.

    Fails closed on:
      - File missing/unreadable → CoefficientRegistryUnreadableError.
      - Signature absent/empty/malformed → CoefficientRegistryUnsignedError
        (F-WPFA-COEFFICIENT-REGISTRY-UNSIGNED).
      - Signature invalid → CoefficientSignatureInvalidError
        (F-WPFA-COEFFICIENT-SIGNATURE-INVALID).
      - Schema invariants violated → CoefficientSchemaInvalidError.

    No network access. No retries.
    """
    path = Path(registry_path)
    try:
        raw = path.read_bytes()
    except (OSError, FileNotFoundError) as exc:
        raise CoefficientRegistryUnreadableError(
            f"registry path {path!r} unreadable: {exc}"
        ) from exc

    try:
        parsed = json.loads(raw.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise CoefficientSchemaInvalidError(
            f"registry at {path!r} is not valid UTF-8 JSON: {exc}"
        ) from exc

    if not isinstance(parsed, dict):
        raise CoefficientSchemaInvalidError(
            "registry top-level must be a JSON object"
        )

    sig_hex = parsed.get("sn_llc_signature_ed25519")
    if not isinstance(sig_hex, str) or not sig_hex:
        raise CoefficientRegistryUnsignedError(
            "registry missing or empty sn_llc_signature_ed25519 — "
            "F-WPFA-COEFFICIENT-REGISTRY-UNSIGNED"
        )
    if len(sig_hex) != _ED25519_HEX_LEN or not all(
        c in "0123456789abcdef" for c in sig_hex.lower()
    ):
        raise CoefficientSignatureInvalidError(
            "sn_llc_signature_ed25519 wrong length/charset",
            sub_tag="signature_bytes_invalid",
        )

    # Build the schema first (so schema-invariant failures surface before sig
    # verify; signature is verified over the canonical signing payload).
    try:
        entries = tuple(
            CoefficientEntry(
                model_id=str(e["model_id"]),
                is_local=bool(e["is_local"]),
                hardware_sku=(
                    None if e.get("hardware_sku") is None else str(e["hardware_sku"])
                ),
                dollars_per_million_input_tokens_minor_units=_dec_int(
                    e["dollars_per_million_input_tokens_minor_units"],
                    "dollars_per_million_input_tokens_minor_units",
                ),
                dollars_per_million_output_tokens_minor_units=_dec_int(
                    e["dollars_per_million_output_tokens_minor_units"],
                    "dollars_per_million_output_tokens_minor_units",
                ),
                watt_hours_per_million_input_tokens_micro=_dec_int(
                    e["watt_hours_per_million_input_tokens_micro"],
                    "watt_hours_per_million_input_tokens_micro",
                ),
                watt_hours_per_million_output_tokens_micro=_dec_int(
                    e["watt_hours_per_million_output_tokens_micro"],
                    "watt_hours_per_million_output_tokens_micro",
                ),
                idle_watts_baseline_micro=_dec_opt_int(
                    e.get("idle_watts_baseline_micro"),
                    "idle_watts_baseline_micro",
                ),
                peak_watts_under_load_micro=_dec_opt_int(
                    e.get("peak_watts_under_load_micro"),
                    "peak_watts_under_load_micro",
                ),
                citation_url=str(e["citation_url"]),
                measurement_date=str(e["measurement_date"]),
                measurement_methodology_url=str(e["measurement_methodology_url"]),
            )
            for e in parsed["entries"]
        )
        registry = CoefficientRegistry(
            schema_version=str(parsed["schema_version"]),
            quarter=str(parsed["quarter"]),
            published_at=str(parsed["published_at"]),
            sn_llc_signature_ed25519=sig_hex,
            sn_llc_signing_key_id=str(parsed["sn_llc_signing_key_id"]),
            baseline_model_id=str(parsed["baseline_model_id"]),
            entries=entries,
            methodology_url=str(parsed["methodology_url"]),
            rollback_pointer=(
                None
                if parsed.get("rollback_pointer") is None
                else str(parsed["rollback_pointer"])
            ),
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise CoefficientSchemaInvalidError(
            f"registry schema invalid: {exc}"
        ) from exc

    # Pinned pubkey
    if (
        not isinstance(pinned_pubkey_hex, str)
        or len(pinned_pubkey_hex) != 64  # 32 bytes Ed25519 raw pubkey hex
        or not all(c in "0123456789abcdef" for c in pinned_pubkey_hex.lower())
    ):
        raise CoefficientSignatureInvalidError(
            "pinned_pubkey_hex must be 64-char lowercase hex (Ed25519 pubkey)",
            sub_tag="pubkey_mismatch",
        )

    # Verify signature over canonical signing payload
    payload = to_signing_payload(registry)
    try:
        sig_bytes = bytes.fromhex(sig_hex)
        pubkey_bytes = bytes.fromhex(pinned_pubkey_hex)
    except ValueError as exc:
        raise CoefficientSignatureInvalidError(
            f"signature/pubkey hex decode failed: {exc}",
            sub_tag="signature_bytes_invalid",
        ) from exc

    try:
        verified = signature_verify(payload, sig_bytes, pubkey_bytes)
    except Exception as exc:  # fail-closed
        raise CoefficientSignatureInvalidError(
            f"signature_verify raised: {type(exc).__name__}: {exc}",
            sub_tag="canonical_json_mismatch",
        ) from exc

    if verified is not True:  # strict identity
        raise CoefficientSignatureInvalidError(
            "signature verification returned False — deployment stays on "
            "previous pinned version",
            sub_tag="canonical_json_mismatch",
        )

    return registry


def _dec_int(value: object, field_name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(
            f"{field_name} must decode as int (A12 mandate), got "
            f"{type(value).__name__}"
        )
    return value


def _dec_opt_int(value: object, field_name: str) -> int | None:
    if value is None:
        return None
    return _dec_int(value, field_name)


__all__ = [
    "CoefficientRegistry",
    "CoefficientEntry",
    "CoefficientRegistryError",
    "CoefficientRegistryUnreadableError",
    "CoefficientRegistryUnsignedError",
    "CoefficientSignatureInvalidError",
    "CoefficientSchemaInvalidError",
    "SignatureVerifyCallable",
    "to_signing_payload",
    "to_canonical_bytes",
    "load_active",
]
