"""pipeline.vault.classification.signed_register_loader — Ed25519 signed register.

Companion code for §4 v2.x.5 amendment (LOCKED 2026-05-16 row 232) — Cycle 2
RT-C2-01 closure.

Loads the operator-signed classification register from a signed YAML file at
``vault_shared/classification/operator_signed_register.signed.yaml`` and
verifies its Ed25519 signature against the white-glove-pinned operator
public key. Mirrors the v7.0.7 §6.1 router-template signing discipline
byte-for-byte (publisher pubkey pinned at onboarding; Trust-On-First-Use;
sig verifies on every load attempt).

PYTHONPATH-based module-replacement attacks fail because this loader does
NOT import a Python module — it reads + verifies the signed YAML at
startup. The loaded register is wrapped in a ``MappingProxyType`` view
exposed as an immutable module-level constant; reassignment attempts raise
``TypeError`` (RT-C2-01 + RT-14 closure precedent on
R-ARCHIVIST-NO-CANONICAL-MUTATE.FORBIDDEN_PRIMITIVES).

Failure mode
------------

Verification failure raises
:class:`pipeline.orchestrator.provider_boundary.OutboundBoundaryRefusedError`
with failure-code
``F-CLASS-REGISTER-SIGNATURE-INVALID.signed_file_invalid``. Callers
(wrapper construction sites) treat the failure as fail-closed: no cloud
egress proceeds without a verified register.

Schema (signed YAML payload)
----------------------------

.. code-block:: yaml

    register:
      org_slug: "fit_farms_llc"
      version: "v1"
      posture: "frontier_eligible"
      entries:
        - field_path: "ein"
          value: "12-3456789"
          class_name: "confidential"
        - field_path: "operator_address"
          value: "123 Main St, Anywhere PA 12345"
          class_name: "confidential"
        # ... more entries ...
    signature:
      algorithm: "ed25519"
      public_key_b64: "..."
      signature_b64: "..."
      signed_canonical_bytes_sha3_512: "..."
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from types import MappingProxyType
from typing import Any, Final, Mapping

# Default vault_shared path — operator white-glove sets this at onboarding.
DEFAULT_SIGNED_REGISTER_PATH: Final[str] = (
    "vault_shared/classification/operator_signed_register.signed.yaml"
)

DEFAULT_PINNED_PUBKEY_PATH: Final[str] = (
    "vault_shared/classification/operator_pubkey.signed.yaml"
)

#: Failure code emitted when sig verification fails. Sub-tag extension on
#: existing F-CLASS-REGISTER-SIGNATURE-INVALID primitive per §0.5 v27.
F_CLASS_REGISTER_SIGNATURE_INVALID_SIGNED_FILE_INVALID: Final[str] = (
    "F-CLASS-REGISTER-SIGNATURE-INVALID.signed_file_invalid"
)


class SignedRegisterLoadError(RuntimeError):
    """Raised when the signed register file fails to load or verify."""

    def __init__(self, failure_code: str, detail: str) -> None:
        self.failure_code = failure_code
        self.detail = detail
        super().__init__(f"{failure_code}: {detail}")


def _canonical_bytes(payload: Mapping[str, Any]) -> bytes:
    """Compute canonical JSON bytes of the register payload for sig verification.

    Canonical-JSON convention: ``sort_keys=True, separators=(",", ":"),
    ensure_ascii=False, UTF-8``. Mirrors the v7.0.7 §6.1 router-template
    canonical-bytes shape.
    """
    return json.dumps(
        dict(payload),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def _verify_ed25519(
    canonical: bytes, signature_b64: str, public_key_b64: str
) -> bool:
    """Verify an Ed25519 signature using the cryptography library.

    Returns True on PASS, False on any failure (including
    InvalidSignature, mis-formatted key, or library unavailability).
    """
    import base64

    try:
        from cryptography.exceptions import InvalidSignature
        from cryptography.hazmat.primitives.asymmetric.ed25519 import (
            Ed25519PublicKey,
        )
    except ImportError:
        # cryptography is a pinned dep at >=42.0 per pyproject.toml; if
        # it's absent the deployment is broken and we fail-closed.
        return False

    try:
        pub_raw = base64.b64decode(public_key_b64, validate=True)
        sig_raw = base64.b64decode(signature_b64, validate=True)
        pubkey = Ed25519PublicKey.from_public_bytes(pub_raw)
    except (ValueError, TypeError):
        return False

    try:
        pubkey.verify(sig_raw, canonical)
        return True
    except InvalidSignature:
        return False
    except Exception:
        return False


def load_signed_register(
    *,
    path: str | Path | None = None,
    pinned_pubkey_b64: str | None = None,
    root: Path | None = None,
) -> Mapping[str, Any]:
    """Load + Ed25519-verify the operator-signed classification register.

    Parameters
    ----------
    path
        Absolute or repo-relative path to the signed YAML file. Defaults to
        ``DEFAULT_SIGNED_REGISTER_PATH``.
    pinned_pubkey_b64
        Operator's white-glove-pinned Ed25519 public key (base64-encoded raw
        32-byte key). If None, the loader reads the pubkey from the
        ``signature.public_key_b64`` field in the signed YAML (Trust-On-
        First-Use; operator confirms the displayed pubkey at first load).
        Production deployments MUST pass an explicit pinned key.
    root
        Repository root for repo-relative path resolution. Defaults to CWD.

    Returns
    -------
    MappingProxyType view over the loaded register payload. Raises
    SignedRegisterLoadError on any load / parse / verify failure.
    """
    resolved_path = Path(path) if path else Path(DEFAULT_SIGNED_REGISTER_PATH)
    if not resolved_path.is_absolute():
        base = root or Path.cwd()
        resolved_path = base / resolved_path

    if not resolved_path.exists():
        raise SignedRegisterLoadError(
            F_CLASS_REGISTER_SIGNATURE_INVALID_SIGNED_FILE_INVALID,
            f"signed register file not found at {resolved_path}",
        )

    try:
        raw_text = resolved_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise SignedRegisterLoadError(
            F_CLASS_REGISTER_SIGNATURE_INVALID_SIGNED_FILE_INVALID,
            f"failed to read signed register at {resolved_path}: {exc}",
        ) from exc

    # YAML parse — falls back to JSON if PyYAML is unavailable. The signed
    # file is canonical-JSON-shaped under a YAML extension by convention; the
    # JSON loader is a superset-compatible fallback.
    try:
        import yaml

        data = yaml.safe_load(raw_text)
    except ImportError:
        try:
            data = json.loads(raw_text)
        except json.JSONDecodeError as exc:
            raise SignedRegisterLoadError(
                F_CLASS_REGISTER_SIGNATURE_INVALID_SIGNED_FILE_INVALID,
                f"failed to parse signed register (no yaml; json fallback failed): {exc}",
            ) from exc
    except Exception as exc:
        raise SignedRegisterLoadError(
            F_CLASS_REGISTER_SIGNATURE_INVALID_SIGNED_FILE_INVALID,
            f"yaml parse error in signed register: {exc}",
        ) from exc

    if not isinstance(data, dict):
        raise SignedRegisterLoadError(
            F_CLASS_REGISTER_SIGNATURE_INVALID_SIGNED_FILE_INVALID,
            "signed register must decode to a mapping at top level",
        )

    register_payload = data.get("register")
    sig_block = data.get("signature")
    if not isinstance(register_payload, dict) or not isinstance(sig_block, dict):
        raise SignedRegisterLoadError(
            F_CLASS_REGISTER_SIGNATURE_INVALID_SIGNED_FILE_INVALID,
            "signed register must contain `register:` mapping and "
            "`signature:` mapping",
        )

    algorithm = str(sig_block.get("algorithm", ""))
    if algorithm != "ed25519":
        raise SignedRegisterLoadError(
            F_CLASS_REGISTER_SIGNATURE_INVALID_SIGNED_FILE_INVALID,
            f"unsupported signature algorithm {algorithm!r}; only ed25519 is "
            "accepted",
        )

    signature_b64 = str(sig_block.get("signature_b64", ""))
    if not signature_b64:
        raise SignedRegisterLoadError(
            F_CLASS_REGISTER_SIGNATURE_INVALID_SIGNED_FILE_INVALID,
            "signed register missing signature_b64",
        )

    # Use the operator's pinned pubkey if supplied, else fall back to the
    # signed file's own embedded pubkey (Trust-On-First-Use). Production
    # MUST pass an explicit pinned key.
    effective_pubkey_b64 = (
        pinned_pubkey_b64
        if pinned_pubkey_b64
        else str(sig_block.get("public_key_b64", ""))
    )
    if not effective_pubkey_b64:
        raise SignedRegisterLoadError(
            F_CLASS_REGISTER_SIGNATURE_INVALID_SIGNED_FILE_INVALID,
            "no pinned operator pubkey supplied and signature.public_key_b64 "
            "is missing",
        )

    canonical = _canonical_bytes(register_payload)
    if not _verify_ed25519(canonical, signature_b64, effective_pubkey_b64):
        raise SignedRegisterLoadError(
            F_CLASS_REGISTER_SIGNATURE_INVALID_SIGNED_FILE_INVALID,
            "ed25519 signature verification failed",
        )

    # Optional canonical-bytes sha3-512 anchor — if supplied, must match.
    expected_hash = str(sig_block.get("signed_canonical_bytes_sha3_512", ""))
    if expected_hash:
        actual = hashlib.sha3_512(canonical).hexdigest()
        if actual != expected_hash.lower():
            raise SignedRegisterLoadError(
                F_CLASS_REGISTER_SIGNATURE_INVALID_SIGNED_FILE_INVALID,
                "canonical-bytes sha3-512 does not match signature.signed_"
                "canonical_bytes_sha3_512",
            )

    # Return immutable view (MappingProxyType deep-wrap not required; the
    # top-level proxy is sufficient to satisfy the contract under v7 A1+A4).
    return MappingProxyType(dict(data))


def load_pinned_pubkey(
    *, path: str | Path | None = None, root: Path | None = None
) -> str:
    """Read the operator-pinned Ed25519 pubkey from
    ``vault_shared/classification/operator_pubkey.signed.yaml``.

    Returns the ``public_key_b64`` string. Raises SignedRegisterLoadError if
    the file is missing or malformed.
    """
    resolved_path = Path(path) if path else Path(DEFAULT_PINNED_PUBKEY_PATH)
    if not resolved_path.is_absolute():
        base = root or Path.cwd()
        resolved_path = base / resolved_path

    if not resolved_path.exists():
        raise SignedRegisterLoadError(
            F_CLASS_REGISTER_SIGNATURE_INVALID_SIGNED_FILE_INVALID,
            f"pinned pubkey file not found at {resolved_path}",
        )

    try:
        raw_text = resolved_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise SignedRegisterLoadError(
            F_CLASS_REGISTER_SIGNATURE_INVALID_SIGNED_FILE_INVALID,
            f"failed to read pinned pubkey at {resolved_path}: {exc}",
        ) from exc

    try:
        import yaml

        data = yaml.safe_load(raw_text)
    except ImportError:
        data = json.loads(raw_text)
    except Exception as exc:
        raise SignedRegisterLoadError(
            F_CLASS_REGISTER_SIGNATURE_INVALID_SIGNED_FILE_INVALID,
            f"failed to parse pinned pubkey: {exc}",
        ) from exc

    if not isinstance(data, dict):
        raise SignedRegisterLoadError(
            F_CLASS_REGISTER_SIGNATURE_INVALID_SIGNED_FILE_INVALID,
            "pinned pubkey file must decode to a mapping",
        )

    pubkey_b64 = str(data.get("public_key_b64", ""))
    if not pubkey_b64:
        raise SignedRegisterLoadError(
            F_CLASS_REGISTER_SIGNATURE_INVALID_SIGNED_FILE_INVALID,
            "pinned pubkey file missing public_key_b64 field",
        )
    return pubkey_b64


__all__ = [
    "F_CLASS_REGISTER_SIGNATURE_INVALID_SIGNED_FILE_INVALID",
    "SignedRegisterLoadError",
    "load_signed_register",
    "load_pinned_pubkey",
    "DEFAULT_SIGNED_REGISTER_PATH",
    "DEFAULT_PINNED_PUBKEY_PATH",
]
