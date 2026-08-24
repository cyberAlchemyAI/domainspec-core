"""Deterministic canonical bytes and SHA-256 identity for ChapterRun."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

from .model import ChapterRun, validate_chapter_run


@dataclass(frozen=True, slots=True)
class CanonicalIdentity:
    canonical_bytes: bytes
    sha256: str


def canonical_bytes(value: object) -> bytes:
    """Return compact sorted UTF-8 JSON for one structurally valid envelope."""

    run: ChapterRun = validate_chapter_run(value).require()
    return json.dumps(
        run.to_document(),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def canonical_sha256(value: object) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def canonical_identity(value: object) -> CanonicalIdentity:
    payload = canonical_bytes(value)
    return CanonicalIdentity(payload, hashlib.sha256(payload).hexdigest())


__all__ = [
    "CanonicalIdentity",
    "canonical_bytes",
    "canonical_identity",
    "canonical_sha256",
]
