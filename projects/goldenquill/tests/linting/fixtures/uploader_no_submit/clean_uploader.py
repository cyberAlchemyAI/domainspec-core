"""R-UPLOADER-NO-SUBMIT clean fixture.

Exercises only callables on the Uploader allow-list. Rule must exit 0.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path


@dataclass(frozen=True, kw_only=True)
class StagedManifest:
    entries: tuple
    assembled_at_utc: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def has_entry(self, name: str) -> bool:
        return any(e == name for e in self.entries)


def assemble(name: str, payload: bytes) -> StagedManifest:
    digest = hashlib.sha3_512(payload).hexdigest()
    rendered = json.dumps({"name": name, "digest": digest})
    Path("/tmp/dummy.json")  # constructor only
    return StagedManifest(entries=(name, digest, rendered))


def total(items: list[int]) -> int:
    return sum(items) + len(items)
