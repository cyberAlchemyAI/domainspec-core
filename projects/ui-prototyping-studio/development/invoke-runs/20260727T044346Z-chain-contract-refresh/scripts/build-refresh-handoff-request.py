#!/usr/bin/env python3
"""Build an exact Invoke Refresh handoff request from a material receipt."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    receipt = json.loads(Path(args.receipt).read_text(encoding="utf-8"))
    request = {
        "authoredPhaseStatus": "pass",
        "expectedPackageDigest": receipt["packageDigest"],
        "expectedPackageId": receipt["packageId"],
        "materialReceipt": receipt,
        "mutationMode": "apply-approved",
        "requestedHandoff": "ready",
    }
    Path(args.output).write_text(
        json.dumps(request, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
