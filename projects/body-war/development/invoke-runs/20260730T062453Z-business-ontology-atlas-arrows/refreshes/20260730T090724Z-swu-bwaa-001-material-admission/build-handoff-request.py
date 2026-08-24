#!/usr/bin/env python3
"""Bind the current material receipt into an Invoke Refresh handoff request."""

from __future__ import annotations

import json
from pathlib import Path


REFRESH = Path(__file__).resolve().parent
MATERIAL = REFRESH / "material"


def main() -> None:
    receipt = json.loads((MATERIAL / "MATERIAL-RECEIPT.json").read_text())
    request = {
        "activationSource": "direct-user",
        "authoredPhaseStatus": "pass",
        "requestedHandoff": "ready",
        "expectedPackageId": receipt["packageId"],
        "expectedPackageDigest": receipt["packageDigest"],
        "materialReceipt": receipt,
    }
    (MATERIAL / "REFRESH-HANDOFF-REQUEST.json").write_text(
        json.dumps(request, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
