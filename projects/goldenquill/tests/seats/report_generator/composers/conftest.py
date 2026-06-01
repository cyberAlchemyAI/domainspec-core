"""Shared composer test fixtures.

Provides:

* :func:`fixed_clock` — deterministic UTC ISO-8601 clock callable.
* :func:`hash_bytes` — SHA3-512 lowercase-hex.
* :func:`make_read_intent` — builds a deterministic
  :class:`VaultReadIntentCallable` from a per-kind/path dict registry.
* :func:`make_scribe` — builds a deterministic
  :class:`ScribeProtocol` that joins source ``text`` / ``commitment_text``
  fields per spec.field_name (so tests can assert content traces).
"""

from __future__ import annotations

import hashlib
from typing import Mapping

import pytest


_FIXED_UTC: str = "2026-05-11T12:00:00Z"


@pytest.fixture
def fixed_clock():
    """Return a deterministic clock callable -> ``_FIXED_UTC``."""

    def _clock() -> str:
        return _FIXED_UTC

    return _clock


@pytest.fixture
def fixed_clock_value() -> str:
    """The value the fixed_clock returns; for asserts in tests."""
    return _FIXED_UTC


@pytest.fixture
def hash_bytes():
    """Return a SHA3-512 lowercase-hex hash callable."""

    def _hash(data: bytes) -> str:
        return hashlib.sha3_512(data).hexdigest()

    return _hash


@pytest.fixture
def make_read_intent():
    """Factory: build a deterministic read intent from a registry dict.

    Usage::

        read = make_read_intent({
            ("operational_data", "metrics"): [
                {"metric_id": "M1", "actual": "50", ...},
                ...
            ],
            ("reporting_template", None): [
                {"field_name": "...", ...},
            ],
            ("proposal_commitments", None): [...],
            ("kfr", None): [...],
        })
    """

    def _factory(registry: Mapping[tuple, object]):
        def _read(*, kind: str, path: str = "", **kwargs):
            sub_kind = kwargs.get("sub_kind")
            key = (kind, sub_kind)
            if key in registry:
                return registry[key]
            # Fallback to kind-only key.
            if (kind, None) in registry:
                return registry[(kind, None)]
            return ()

        return _read

    return _factory


@pytest.fixture
def make_scribe():
    """Factory: deterministic Scribe stub.

    The default behaviour produces a one-paragraph summary of the
    supplied sources keyed off ``spec.field_name``. Tests can pass a
    callable override to customize.
    """

    def _factory(override=None):
        if override is not None:
            return override

        def _scribe(*, spec, sources):
            parts = []
            for s in sources:
                if "text" in s and isinstance(s["text"], str):
                    parts.append(s["text"])
                elif "commitment_text" in s and isinstance(s["commitment_text"], str):
                    parts.append(s["commitment_text"])
                elif "actual" in s:
                    parts.append(f"{s.get('metric_name', '?')} actual={s['actual']}")
                elif "caption_at_capture" in s:
                    parts.append(s["caption_at_capture"])
                elif "outcome_summary" in s:
                    parts.append(s["outcome_summary"])
            joined = " ".join(parts) if parts else f"[{spec.field_name}]"
            return f"{joined}."

        return _scribe

    return _factory
