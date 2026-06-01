"""SN-LLC seeding allowlist loader (architecture v7.0.4-M1 §5.2.3).

Allowlist file structure per §5.2.3 (verbatim YAML shape):

```yaml
schema_version: benchmark_seeding_allowlist.v1
canonicalization: kfr_canonical.v1
populated_by: <operator_key_id>
populated_at: <iso8601>
allowed_source_domains: [...]
allowed_source_path_prefixes: [...]
forbidden_source_path_prefixes: [...]
audit_chain: [...]
signature_ed25519: <base64-encoded sig over canonical-JSON bytes>
signature_key_id: <operator key_id>
```

Loader discipline (RT-09 closure):

1. Read bytes from disk via :func:`load_kfr_safe` (refuses anchors /
   aliases / merge-keys).
2. Compute canonical-JSON bytes per §2.2.1, EXCLUDING the
   ``signature_ed25519`` and ``signature_key_id`` fields.
3. Verify Ed25519 signature against operator-keyring active-key
   catalog (per v7.0.4 §1.1 keyring discipline).
4. On verification failure → raise :class:`AllowlistError` with
   ``failure_code=F-BENCHMARK-SEEDING-ALLOWLIST-SIGNATURE-INVALID``.
5. On verification success → return :class:`SeedingAllowlist`.

Source-doc authorization (loader returns the predicate; the gate
:mod:`pipeline.logician.gates.f_benchmark_seeding_source_unauthorized`
calls it).
"""

from __future__ import annotations

import base64
import fnmatch
from dataclasses import dataclass, field
from typing import Callable, Final, Optional

from pipeline.logician.canonicalization.kfr_canonical import (
    CANONICALIZATION_SCHEMA_VERSION,
    canonical_dump,
)
from pipeline.logician.canonicalization.kfr_safe_loader import (
    KfrConstructError,
    load_kfr_safe_bytes,
)


ALLOWLIST_SCHEMA_VERSION: Final[str] = "benchmark_seeding_allowlist.v1"

F_BENCHMARK_SEEDING_ALLOWLIST_SIGNATURE_INVALID: Final[str] = (
    "F-BENCHMARK-SEEDING-ALLOWLIST-SIGNATURE-INVALID"
)

# RT-10 closure (Cycle 1, 2026-05-10): strict-key whitelist on the
# allowlist YAML schema. Any key outside this set is refused at load —
# closes the per-org-leakage-via-extra-keys defense-in-depth concern.
# `signature_ed25519` and `signature_key_id` are stripped before
# canonicalization but MUST be present at load time.
_ALLOWED_ALLOWLIST_KEYS: Final[frozenset[str]] = frozenset({
    "schema_version",
    "canonicalization",
    "populated_by",
    "populated_at",
    "allowed_source_domains",
    "allowed_source_path_prefixes",
    "forbidden_source_path_prefixes",
    "audit_chain",
    "signature_ed25519",
    "signature_key_id",
})


class AllowlistError(ValueError):
    """Raised when allowlist load / signature verification fails."""

    def __init__(
        self,
        message: str,
        *,
        failure_code: str = F_BENCHMARK_SEEDING_ALLOWLIST_SIGNATURE_INVALID,
    ) -> None:
        super().__init__(message)
        self.failure_code = failure_code


@dataclass(frozen=True, kw_only=True)
class SeedingAllowlist:
    """Verified SN-LLC seeding allowlist."""

    populated_by: str
    populated_at: str
    allowed_source_domains: tuple[str, ...]
    allowed_source_path_prefixes: tuple[str, ...]
    forbidden_source_path_prefixes: tuple[str, ...]
    audit_chain: tuple[str, ...] = field(default_factory=tuple)


SignatureVerifyCallable = Callable[[bytes, bytes, bytes], bool]


def canonical_allowlist_payload(parsed: dict) -> bytes:
    """Render the allowlist-without-signature view to canonical-JSON.

    The signature surface signs all fields EXCEPT
    ``signature_ed25519`` and ``signature_key_id`` (which are
    themselves the signature output).  The caller (operator tooling)
    uses the same renderer to produce the bytes that get signed.
    """
    if not isinstance(parsed, dict):
        raise AllowlistError(
            f"allowlist must be a mapping, got {type(parsed).__name__}",
            failure_code=F_BENCHMARK_SEEDING_ALLOWLIST_SIGNATURE_INVALID,
        )
    payload = {
        k: v for k, v in parsed.items()
        if k not in {"signature_ed25519", "signature_key_id"}
    }
    return canonical_dump(payload)


def load_seeding_allowlist(
    *,
    raw_bytes: bytes,
    operator_public_key: bytes,
    expected_key_id: str,
    signature_verify: SignatureVerifyCallable,
) -> SeedingAllowlist:
    """Load + signature-verify a seeding allowlist file (§5.2.3).

    Parameters
    ----------
    raw_bytes
        File bytes (UTF-8 YAML).
    operator_public_key
        Ed25519 public key from the operator keyring.
    expected_key_id
        Key ID the loader expects on the allowlist's ``signature_key_id``
        field.  Mismatch fails-closed.
    signature_verify
        Injected verifier — same shape as the rest of §4 verifier
        signatures (``(message, signature, public_key) → bool``).
    """
    try:
        parsed = load_kfr_safe_bytes(raw_bytes)
    except KfrConstructError as exc:
        raise AllowlistError(
            f"allowlist YAML refused: {exc}",
            failure_code=F_BENCHMARK_SEEDING_ALLOWLIST_SIGNATURE_INVALID,
        ) from exc

    if not isinstance(parsed, dict):
        raise AllowlistError(
            f"allowlist must be a mapping, got {type(parsed).__name__}",
        )
    # RT-10 closure (Cycle 1): strict-key whitelist. Any key outside
    # _ALLOWED_ALLOWLIST_KEYS fails-closed — defense-in-depth against
    # per-org content leakage through extra fields the loader would
    # otherwise silently ignore.
    extra_keys = set(parsed.keys()) - _ALLOWED_ALLOWLIST_KEYS
    if extra_keys:
        raise AllowlistError(
            f"allowlist contains forbidden keys "
            f"{sorted(extra_keys)!r} — only "
            f"{sorted(_ALLOWED_ALLOWLIST_KEYS)} are admitted "
            "(RT-10 closure leg 1; defense-in-depth against per-org "
            "content leakage via extra fields)",
        )
    if parsed.get("schema_version") != ALLOWLIST_SCHEMA_VERSION:
        raise AllowlistError(
            f"allowlist schema_version mismatch: expected "
            f"{ALLOWLIST_SCHEMA_VERSION!r}, got "
            f"{parsed.get('schema_version')!r}",
        )
    if parsed.get("canonicalization") != CANONICALIZATION_SCHEMA_VERSION:
        raise AllowlistError(
            f"allowlist canonicalization mismatch: expected "
            f"{CANONICALIZATION_SCHEMA_VERSION!r}, got "
            f"{parsed.get('canonicalization')!r}",
        )

    sig_b64 = parsed.get("signature_ed25519")
    sig_key_id = parsed.get("signature_key_id")
    if not isinstance(sig_b64, str) or not sig_b64.strip():
        raise AllowlistError(
            "allowlist signature_ed25519 missing or empty",
        )
    if not isinstance(sig_key_id, str) or not sig_key_id.strip():
        raise AllowlistError(
            "allowlist signature_key_id missing or empty",
        )
    if sig_key_id != expected_key_id:
        raise AllowlistError(
            f"allowlist signature_key_id={sig_key_id!r} does not match "
            f"expected={expected_key_id!r}",
        )

    try:
        signature_bytes = base64.b64decode(sig_b64, validate=True)
    except (ValueError, base64.binascii.Error) as exc:  # type: ignore[attr-defined]
        raise AllowlistError(
            f"allowlist signature_ed25519 not valid base64: {exc}",
        ) from exc

    payload_bytes = canonical_allowlist_payload(parsed)
    try:
        verified = signature_verify(
            payload_bytes, signature_bytes, operator_public_key
        )
    except Exception as exc:  # noqa: BLE001 — fail-closed
        raise AllowlistError(
            f"allowlist signature_verify raised "
            f"{type(exc).__name__}: {exc}",
        ) from exc

    if verified is not True:
        raise AllowlistError(
            "allowlist Ed25519 signature failed verification against "
            f"operator key {expected_key_id!r}",
        )

    return SeedingAllowlist(
        populated_by=str(parsed.get("populated_by", "")).strip(),
        populated_at=str(parsed.get("populated_at", "")).strip(),
        allowed_source_domains=tuple(
            str(d) for d in (parsed.get("allowed_source_domains") or [])
        ),
        allowed_source_path_prefixes=tuple(
            str(p) for p in (parsed.get("allowed_source_path_prefixes") or [])
        ),
        forbidden_source_path_prefixes=tuple(
            str(p) for p in (parsed.get("forbidden_source_path_prefixes") or [])
        ),
        audit_chain=tuple(
            str(row) for row in (parsed.get("audit_chain") or [])
        ),
    )


def source_doc_authorized(
    *,
    source_doc: str,
    allowlist: SeedingAllowlist,
) -> tuple[bool, str]:
    """Returns ``(authorized, reason)``.

    Forbidden-path-prefix wins over allowed-path-prefix.  A source
    matching ``orgs/`` (per default forbidden list) fails-closed even
    if a more permissive prefix would otherwise admit it.
    """
    if not isinstance(source_doc, str):
        return False, (
            f"source_doc must be str, got {type(source_doc).__name__}"
        )
    cleaned = source_doc.strip()
    if cleaned.startswith("./"):
        cleaned = cleaned[2:]

    for forbidden in allowlist.forbidden_source_path_prefixes:
        if cleaned.startswith(forbidden):
            return False, (
                f"source_doc {source_doc!r} matches forbidden_source_"
                f"path_prefix {forbidden!r}"
            )

    # Domain-style allowance — used when the source_doc is a URL or
    # FQDN reference.  The match is glob-based (e.g., ``*.usda.gov``).
    for domain in allowlist.allowed_source_domains:
        if fnmatch.fnmatch(cleaned, domain):
            return True, (
                f"source_doc matches allowed_source_domain {domain!r}"
            )
        # Also try a host-only match (strip scheme).
        host = cleaned.split("://", 1)[-1].split("/", 1)[0]
        if fnmatch.fnmatch(host, domain):
            return True, (
                f"source_doc host {host!r} matches allowed_source_"
                f"domain {domain!r}"
            )

    for prefix in allowlist.allowed_source_path_prefixes:
        if cleaned.startswith(prefix):
            return True, (
                f"source_doc matches allowed_source_path_prefix "
                f"{prefix!r}"
            )

    return False, (
        f"source_doc {source_doc!r} matches neither allowed_source_"
        "domains nor allowed_source_path_prefixes"
    )


__all__ = [
    "ALLOWLIST_SCHEMA_VERSION",
    "AllowlistError",
    "F_BENCHMARK_SEEDING_ALLOWLIST_SIGNATURE_INVALID",
    "SeedingAllowlist",
    "_ALLOWED_ALLOWLIST_KEYS",
    "canonical_allowlist_payload",
    "load_seeding_allowlist",
    "source_doc_authorized",
]
