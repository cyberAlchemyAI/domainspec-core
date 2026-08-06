#!/usr/bin/env python3
"""Bind the direct resume confirmation to the first audited Anime.js SWU."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


HERE = Path(__file__).resolve().parent


def repository_root() -> Path:
    for candidate in [HERE, *HERE.parents]:
        if (candidate / ".git").exists():
            return candidate
    raise RuntimeError("repository root not found")


ROOT = repository_root()


def exact(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "sha256": hashlib.sha256(data).hexdigest(),
        "size_bytes": len(data),
    }


request = {
    "schemaVersion": "1.0.0",
    "manifestRef": exact(HERE / "audit-output-pass/plan-semantic-manifest.json"),
    "auditConfigPath": (HERE / "audit-config.json").relative_to(ROOT).as_posix(),
    "taskId": "TASK-AKV-CONTRACTS",
    "swuId": "SWU-AKV-NV-001",
    "explicitConfirmation": {
        "confirmed": True,
        "confirmedBy": "direct-user",
        "confirmationId": "2026-08-03-finish-animejs-ontology",
    },
    "dependencyReceipts": [],
    "lifecycleEligibility": {
        "eligible": True,
        "state": "selected-for-first-task-session",
        "evidenceRefs": [exact(HERE / "evidence.json")],
    },
}

(HERE / "selection-request.json").write_text(
    json.dumps(request, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
print((HERE / "selection-request.json").relative_to(ROOT).as_posix())
