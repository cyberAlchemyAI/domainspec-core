#!/usr/bin/env python3
"""Build a Task Session 1.2 admission probe from the Invoke material receipt."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


REPOSITORY = Path(__file__).resolve().parents[7]
REFRESH = Path(__file__).resolve().parent

TASK = (
    "projects/body-war/development/invoke-runs/"
    "20260730T062453Z-business-ontology-atlas-arrows/"
    "work-pack/tasks/TASK-BWAA-001.md"
)
WORK_PACK = (
    "projects/body-war/development/invoke-runs/"
    "20260730T062453Z-business-ontology-atlas-arrows/WORK-PACK.md"
)
CONTEXT = (
    "projects/body-war/development/invoke-runs/"
    "20260730T062453Z-business-ontology-atlas-arrows/refreshes/"
    "20260730T090724Z-swu-bwaa-001-material-admission/CONTEXT-PACK.json"
)
PACKAGE = (
    "projects/body-war/development/invoke-runs/"
    "20260730T062453Z-business-ontology-atlas-arrows/refreshes/"
    "20260730T090724Z-swu-bwaa-001-material-admission/material/"
    "MATERIAL-PACKAGE.json"
)
RECEIPT = (
    "projects/body-war/development/invoke-runs/"
    "20260730T062453Z-business-ontology-atlas-arrows/refreshes/"
    "20260730T090724Z-swu-bwaa-001-material-admission/material/"
    "MATERIAL-RECEIPT.json"
)
PRODUCER_SCHEMA = (
    ".agents/skills/invoke/schemas/material-package-receipt.schema.json"
)

MATERIAL_WRITES = [
    "projects/body-war/ontology/business/scripts/view-atlas-projection.mjs",
    "projects/body-war/ontology/business/scripts/validate-view-atlas.mjs",
    "projects/body-war/ontology/business/tests/business-view-atlas-projection.test.mjs",
]
EXECUTION_OUTPUTS = [
    "projects/body-war/ontology/business/receipts/view-atlas-coverage-receipt.json",
    "projects/body-war/development/invoke-runs/20260730T062453Z-business-ontology-atlas-arrows/work-pack/closeout/SWU-BWAA-001.receipt.json",
]
VALIDATION_COMMANDS = [
    "node --test projects/body-war/ontology/business/tests/business-view-atlas-projection.test.mjs",
    "node projects/body-war/ontology/business/scripts/validate-view-atlas.mjs",
    "git diff --check -- projects/body-war/ontology/business/scripts/view-atlas-projection.mjs projects/body-war/ontology/business/scripts/validate-view-atlas.mjs projects/body-war/ontology/business/tests/business-view-atlas-projection.test.mjs",
]


def exact_ref(relative: str, *, camel: bool = True) -> dict[str, object]:
    data = (REPOSITORY / relative).read_bytes()
    size_key = "sizeBytes" if camel else "size_bytes"
    return {
        "path": relative,
        "sha256": hashlib.sha256(data).hexdigest(),
        size_key: len(data),
    }


def main() -> None:
    request = {
        "schemaVersion": "1.2.0",
        "executionMode": "routed-mutation",
        "taskId": "TASK-BWAA-001",
        "swuId": "SWU-BWAA-001",
        "controlArtifacts": [
            {
                **exact_ref(TASK),
                "role": "task-contract",
                "authorityClass": "private",
            },
            {
                **exact_ref(WORK_PACK),
                "role": "work-pack",
                "authorityClass": "private",
            },
            {
                **exact_ref(CONTEXT),
                "role": "context-pack",
                "authorityClass": "private",
            },
        ],
        "dependencyFrontier": [],
        "materialPackage": exact_ref(PACKAGE),
        "materialReceipt": exact_ref(RECEIPT),
        "producerReceiptSchema": exact_ref(PRODUCER_SCHEMA),
        "materialWrites": MATERIAL_WRITES,
        "executionOutputs": EXECUTION_OUTPUTS,
        "allowedWrites": MATERIAL_WRITES + EXECUTION_OUTPUTS,
        "validationCommands": VALIDATION_COMMANDS,
        "lifecycleOwner": "body-war.product-ontology-owner",
        "authorityClass": "private",
        "publicationClass": "internal",
    }
    (REFRESH / "TASK-SESSION-ADMISSION-PROBE-REQUEST.json").write_text(
        json.dumps(request, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
