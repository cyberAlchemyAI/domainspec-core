#!/usr/bin/env python3
"""Bind the OAVA-003 selection request to the Goal outer-loop intent."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


REPO = Path(__file__).resolve().parents[8]
ROOT = Path(__file__).resolve().parent
manifest_path = ROOT / "audit-output" / "plan-semantic-manifest.json"
evidence_path = ROOT / "evidence.json"
initialized = json.loads((ROOT / "initialize-result.json").read_text(encoding="utf-8"))
binding = initialized["state"]["current_binding"]


def file_ref(path: Path) -> dict[str, object]:
    payload = path.read_bytes()
    return {
        "path": path.relative_to(REPO).as_posix(),
        "sha256": hashlib.sha256(payload).hexdigest(),
        "size_bytes": len(payload),
    }


request = {
    "schemaVersion": "1.0.0",
    "manifestRef": file_ref(manifest_path),
    "auditConfigPath": (ROOT / "audit-config.json").relative_to(REPO).as_posix(),
    "taskId": "TASK-OAVA-RUNTIME-ADMISSION",
    "swuId": "SWU-OAVA-003",
    "executionIntentBinding": {
        "bindingId": binding["binding_id"],
        "sourceInvocationId": binding["source_invocation_id"],
        "workPackId": binding["work_pack_id"],
        "bindingDigest": binding["binding_digest"],
        "authorityEffect": "bounded-execution-only",
    },
    "dependencyReceipts": [],
    "lifecycleEligibility": {
        "eligible": True,
        "state": "selected",
        "evidenceRefs": [file_ref(evidence_path)],
    },
}
(ROOT / "selection-request.json").write_text(
    json.dumps(request, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
print(
    json.dumps(
        {
            "status": "pass",
            "binding_id": binding["binding_id"],
            "source_invocation_id": binding["source_invocation_id"],
            "swu_id": request["swuId"],
        },
        indent=2,
    )
)
