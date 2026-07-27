#!/usr/bin/env python3
"""Build an exact Task Session admission request from validated material."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[6]
PRODUCER_SCHEMA = (
    ".agents/skills/invoke/schemas/material-package-receipt.schema.json"
)


def exact_ref(path: str) -> dict[str, object]:
    content = (REPO_ROOT / path).read_bytes()
    return {
        "path": path,
        "sha256": hashlib.sha256(content).hexdigest(),
        "sizeBytes": len(content),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", required=True)
    parser.add_argument("--swu", required=True)
    parser.add_argument("--task-contract", required=True)
    parser.add_argument("--work-pack", required=True)
    parser.add_argument("--context-pack", required=True)
    parser.add_argument("--source", action="append", default=[])
    parser.add_argument("--dependency", action="append", default=[])
    parser.add_argument("--material-package", required=True)
    parser.add_argument("--material-receipt", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    package = json.loads(
        (REPO_ROOT / args.material_package).read_text(encoding="utf-8")
    )
    controls = [
        {
            **exact_ref(args.task_contract),
            "role": "task-contract",
            "authorityClass": "private",
        },
        {
            **exact_ref(args.work_pack),
            "role": "work-pack",
            "authorityClass": "private",
        },
        {
            **exact_ref(args.context_pack),
            "role": "context-pack",
            "authorityClass": "private",
        },
        *[
            {
                **exact_ref(path),
                "role": "source",
                "authorityClass": "private",
            }
            for path in args.source
        ],
    ]
    dependencies = []
    for raw in args.dependency:
        dependency_id, separator, path = raw.partition("=")
        if not separator or not dependency_id or not path:
            raise ValueError(f"dependency must be id=path: {raw}")
        dependencies.append(
            {
                "dependencyId": dependency_id,
                "artifactRef": exact_ref(path),
            }
        )
    request = {
        "schemaVersion": "1.0.0",
        "executionMode": "routed-mutation",
        "taskId": args.task,
        "swuId": args.swu,
        "controlArtifacts": controls,
        "dependencyFrontier": dependencies,
        "materialPackage": exact_ref(args.material_package),
        "materialReceipt": exact_ref(args.material_receipt),
        "producerReceiptSchema": exact_ref(PRODUCER_SCHEMA),
        "allowedWrites": sorted(
            change["target_path"] for change in package["changes"]
        ),
        "validationCommands": package["validation_commands"],
        "lifecycleOwner": package["lifecycle_owner"],
        "authorityClass": package["authority_class"],
        "publicationClass": package["publication_class"],
    }
    Path(args.output).write_text(
        json.dumps(request, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
