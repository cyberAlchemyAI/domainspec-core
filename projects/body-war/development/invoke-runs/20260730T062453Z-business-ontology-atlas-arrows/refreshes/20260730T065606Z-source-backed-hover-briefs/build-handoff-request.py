#!/usr/bin/env python3
"""Bind the validated material receipt into an Invoke Refresh handoff request."""

from __future__ import annotations

import json
from pathlib import Path


REFRESH_ROOT = Path(__file__).resolve().parent
receipt = json.loads(
    (REFRESH_ROOT / "material" / "MATERIAL-RECEIPT.json").read_text()
)
request = {
    "schemaVersion": "1.0.0",
    "activationSource": "direct-user",
    "mutationMode": "apply-approved",
    "authoredPhaseStatus": "pass",
    "requestedHandoff": "ready",
    "expectedPackageId": receipt["packageId"],
    "expectedPackageDigest": receipt["packageDigest"],
    "materialReceipt": receipt,
}
(REFRESH_ROOT / "material" / "REFRESH-HANDOFF-REQUEST.json").write_text(
    json.dumps(request, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
