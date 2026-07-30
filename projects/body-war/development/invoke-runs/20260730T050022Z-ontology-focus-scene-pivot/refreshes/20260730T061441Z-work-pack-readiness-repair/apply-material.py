#!/usr/bin/env python3
"""Atomically apply the exact admitted Invoke Refresh material package."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any


REFRESH = Path(__file__).resolve().parent
ROOT = REFRESH.parents[6]


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    return value


def digest(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def main() -> int:
    package = load(REFRESH / "MATERIAL-PACKAGE.json")
    receipt = load(REFRESH / "MATERIAL-RECEIPT.json")
    handoff = load(REFRESH / "REFRESH-HANDOFF-RESULT.json")
    if not (
        receipt["patchVerdict"] == "pass"
        and receipt["mutationHandoff"] == "ready"
        and handoff["mutationReady"] is True
        and handoff["handoffStatus"] == "ready"
    ):
        raise SystemExit("material package is not admitted for apply")
    validated = set(receipt["validatedPaths"])
    approved = set(package["approval"]["scope_paths"])
    changes = {item["target_path"]: item for item in package["changes"]}
    inventory = {item["target_path"] for item in package["target_inventory"]}
    if not validated == approved == set(changes) == inventory:
        raise SystemExit("validated, approved, change, and inventory scopes differ")
    sources = {item["path"]: item for item in package["source_artifacts"]}

    prepared: list[tuple[Path, Path, bytes]] = []
    for target_path in sorted(changes):
        change = changes[target_path]
        target = ROOT / target_path
        operation = change["operation"]
        if operation == "update":
            source = sources.get(target_path)
            if source is None or not target.is_file():
                raise SystemExit(f"missing update preimage: {target_path}")
            current = target.read_bytes()
            if digest(current) != source["sha256"] or len(current) != source["size_bytes"]:
                raise SystemExit(f"stale update preimage: {target_path}")
        elif target.exists():
            raise SystemExit(f"create target already exists: {target_path}")

        output_ref = change["output_ref"]
        output_path = ROOT / output_ref["path"]
        output = output_path.read_bytes()
        if digest(output) != output_ref["sha256"] or len(output) != output_ref["size_bytes"]:
            raise SystemExit(f"staged output mismatch: {target_path}")
        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = target.with_name(target.name + ".invoke-refresh-tmp")
        if temporary.exists():
            raise SystemExit(f"temporary apply path already exists: {temporary}")
        prepared.append((target, temporary, output))

    for _, temporary, output in prepared:
        descriptor = os.open(
            temporary,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL,
            0o644,
        )
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(output)
            handle.flush()
            os.fsync(handle.fileno())

    for target, temporary, _ in prepared:
        os.replace(temporary, target)

    for target, _, output in prepared:
        current = target.read_bytes()
        if current != output:
            raise SystemExit(f"post-apply mismatch: {target}")

    print(
        json.dumps(
            {
                "applied": len(prepared),
                "paths": sorted(changes),
                "package_id": package["package_id"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
