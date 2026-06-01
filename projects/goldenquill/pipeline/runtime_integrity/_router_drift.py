"""Drift-from-Locked-Router detection — §4.2.1 Row 23.

Blueprint §4 v2.5 LOCKED 2026-04-19.
Computes canonical-bytes SHA-3-512 of router.yaml and compares to the hash
pinned in the most recent LOCK manifest. YAML serialized via canonical JSON
for hash parity (sort_keys=True, separators=(",",":"), ensure_ascii=False).
"""

from __future__ import annotations

import hashlib
import json
import unicodedata
from dataclasses import dataclass
from typing import Any, Final

BLUEPRINT_DEPS: Final[dict] = {
    "section_04_v2_4_v2_5_amendment.md": {
        "sections_implemented": ["§4.2.1 Row 23 drift-from-locked-router detection"],
        "hash_source_version": "v2.5",
    },
}

F_RUNTIME_DRIFT_FROM_LOCKED_ROUTER: Final[str] = "F-RUNTIME-DRIFT-FROM-LOCKED-ROUTER"
F_ROUTER_CANONICAL_BYTES_NONSTR_KEY: Final[str] = "F-ROUTER-CANONICAL-BYTES-NONSTR-KEY"


@dataclass(frozen=True)
class RouterDriftResult:
    """Result of the drift-from-locked-router detection (§4.2.1 Row 23)."""

    drift_detected: bool
    computed_hash: str
    expected_hash: str | None
    failure_code: str | None
    detail: dict[str, Any] | None


def _nfc_normalize(obj: Any) -> Any:
    """Walk the structure and NFC-normalize every str leaf (and every str key).

    YAML → Python → canonical-JSON can preserve Unicode NFD sequences that visually
    match an NFC form but hash differently. Strict NFC discipline (E-003) applied
    at the canonical-bytes boundary closes the normalization-evasion attack surface
    (adversarial review Finding F2, phase0_through_2b_2026-04-19).
    """
    if isinstance(obj, str):
        return unicodedata.normalize("NFC", obj)
    if isinstance(obj, dict):
        return {_nfc_normalize(k): _nfc_normalize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_nfc_normalize(x) for x in obj]
    if isinstance(obj, tuple):
        return tuple(_nfc_normalize(x) for x in obj)
    return obj


def _assert_str_keys(obj: Any, path: str = "$") -> None:
    """Reject any dict that contains a non-str key anywhere in the tree.

    YAML permits integer / bool / null / date keys. `json.dumps` silently coerces
    them to their str repr, enabling two visually-distinct router.yaml files to
    hash identically (adversarial review Finding F3, phase0_through_2b_2026-04-19).
    Enforce str keys explicitly at the canonical-bytes boundary.
    """
    if isinstance(obj, dict):
        for k, v in obj.items():
            if not isinstance(k, str):
                raise TypeError(
                    f"{F_ROUTER_CANONICAL_BYTES_NONSTR_KEY}: non-str key "
                    f"{type(k).__name__}={k!r} at {path}"
                )
            _assert_str_keys(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, x in enumerate(obj):
            _assert_str_keys(x, f"{path}[{i}]")


def canonical_bytes_sha3_512(data: dict) -> str:
    """Compute canonical-bytes SHA-3-512 of a Python dict. [§4.2.1 Row 23]

    Follows the §0.5 canonical-bytes recipe:
    json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
    allow_nan=False) encoded to UTF-8, then hashed with SHA-3-512.

    Hardenings applied at this layer per adversarial review 2026-04-19:
      - ``allow_nan=False`` rejects NaN/Infinity that json.dumps would otherwise
        serialize as non-RFC-8259 literals (Finding F8).
      - Non-str dict keys raise TypeError with F-ROUTER-CANONICAL-BYTES-NONSTR-KEY
        (Finding F3; YAML→dict can carry int/bool/None keys that json.dumps
        silently coerces, enabling hash-collision across visually-distinct YAML).
      - All str leaves and keys are NFC-normalized (Finding F2; E-003 discipline).

    Returns the lowercase hex digest.
    """
    _assert_str_keys(data)
    normalized = _nfc_normalize(data)
    canonical = json.dumps(
        normalized,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha3_512(canonical).hexdigest()


def check_router_drift(
    router_data: dict,
    expected_hash: str | None,
    operator_attested: bool = False,
) -> RouterDriftResult:
    """Drift-from-Locked-Router detection (§4.2.1 Row 23). [LOCKED §4 v2.5]

    Parameters
    ----------
    router_data : dict
        Parsed contents of router.yaml (from yaml.safe_load or equivalent).
        Caller is responsible for loading the YAML file.
    expected_hash : str | None
        SHA-3-512 hex digest pinned in the most recent LOCK manifest
        `router_yaml_hash` field. If None, pass by construction (first run
        before hash is pinned per §4 v2.5 spec).
    operator_attested : bool
        True when a signed operator-attested edit marker is present.
        If True and hash differs, pass (legitimate operator edit).

    Returns
    -------
    RouterDriftResult
        drift_detected=True when hash mismatch without operator attestation.
    """
    computed = canonical_bytes_sha3_512(router_data)

    if expected_hash is None:
        return RouterDriftResult(
            drift_detected=False,
            computed_hash=computed,
            expected_hash=None,
            failure_code=None,
            detail={"reason": "no_lock_manifest_hash_first_run"},
        )

    if computed == expected_hash:
        return RouterDriftResult(
            drift_detected=False,
            computed_hash=computed,
            expected_hash=expected_hash,
            failure_code=None,
            detail=None,
        )

    if operator_attested:
        return RouterDriftResult(
            drift_detected=False,
            computed_hash=computed,
            expected_hash=expected_hash,
            failure_code=None,
            detail={"reason": "operator_attested_edit", "hash_changed": True},
        )

    return RouterDriftResult(
        drift_detected=True,
        computed_hash=computed,
        expected_hash=expected_hash,
        failure_code=F_RUNTIME_DRIFT_FROM_LOCKED_ROUTER,
        detail={
            "computed_hash": computed,
            "expected_hash": expected_hash,
            "operator_attested": False,
        },
    )
