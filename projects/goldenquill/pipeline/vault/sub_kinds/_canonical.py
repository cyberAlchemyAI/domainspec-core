"""Canonical-bytes encode helpers shared by every operational sub-kind.

Matches the v7.1 ``serialize_manifest`` discipline (§2.4): UTF-8 JSON with
sorted keys and compact separators, so SHA-3-512 hashes are stable across
hosts and across re-encodes.
"""

from __future__ import annotations

import json
from dataclasses import asdict
from typing import Any


def to_canonical_json_bytes(record: Any) -> bytes:
    """Serialize a frozen-dataclass record to canonical JSON bytes.

    :param record: a frozen dataclass instance.
    :returns: UTF-8 JSON bytes with ``sort_keys=True`` and ``separators=(",", ":")``.
    """
    payload = asdict(record)
    return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode(
        "utf-8"
    )


def from_canonical_json_bytes(payload: bytes) -> dict[str, Any]:
    """Decode canonical JSON bytes to a plain dict.

    :param payload: bytes produced by :func:`to_canonical_json_bytes`.
    :raises ValueError: payload does not parse as a JSON object.
    """
    if not isinstance(payload, (bytes, bytearray)):
        raise TypeError(
            f"payload must be bytes|bytearray, got {type(payload).__name__}"
        )
    parsed = json.loads(payload.decode("utf-8"))
    if not isinstance(parsed, dict):
        raise ValueError(
            f"canonical sub-kind payload must decode to a JSON object, "
            f"got {type(parsed).__name__}"
        )
    return parsed


def _coerce_str_tuple(value: Any, *, field: str) -> tuple[str, ...]:
    """Coerce a JSON list-of-strings back into a tuple-of-strings.

    Re-validates the elements so a tampered file is rejected at decode.
    """
    if not isinstance(value, list):
        raise ValueError(
            f"{field} must be a list of strings, got {type(value).__name__}"
        )
    out: list[str] = []
    for i, elem in enumerate(value):
        if not isinstance(elem, str):
            raise ValueError(
                f"{field}[{i}] must be str, got {type(elem).__name__}"
            )
        out.append(elem)
    return tuple(out)


__all__ = [
    "_coerce_str_tuple",
    "from_canonical_json_bytes",
    "to_canonical_json_bytes",
]
