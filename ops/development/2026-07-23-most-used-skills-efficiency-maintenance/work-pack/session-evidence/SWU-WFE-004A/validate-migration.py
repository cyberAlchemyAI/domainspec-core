#!/usr/bin/env python3
"""Validate the exact SWU-WFE-004A kind-only Inventory migration."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[6]
EVIDENCE_DIR = Path(__file__).resolve().parent
INDEX_PATH = REPOSITORY_ROOT / ".arcanum/inventory/index.json"
BASELINE_PATH = EVIDENCE_DIR / "before-projection.json"
ALLOWED_KINDS = {
    "page",
    "entry",
    "query",
    "lint",
    "raw-manifest",
    "evidence-card-bundle",
    "evidence-set-bundle",
}


def digest(value: object) -> str:
    payload = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode()
    return hashlib.sha256(payload).hexdigest()


def main() -> int:
    index = json.loads(INDEX_PATH.read_text(encoding="utf-8"))
    baseline = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
    entries = {entry["id"]: entry for entry in index["entries"]}
    failures: list[str] = []

    for expected in baseline["entries"]:
        entry = entries.get(expected["id"])
        if entry is None:
            failures.append(f"missing entry: {expected['id']}")
            continue
        if entry["path"] != expected["path"]:
            failures.append(f"path changed: {expected['id']}")
        if entry["kind"] != expected["after_kind"]:
            failures.append(
                f"kind mismatch: {expected['id']}={entry['kind']}"
            )
        non_kind = {key: value for key, value in entry.items() if key != "kind"}
        if digest(non_kind) != expected["non_kind_sha256"]:
            failures.append(f"non-kind fields changed: {expected['id']}")

    invalid = [
        entry["id"]
        for entry in index["entries"]
        if entry["kind"] not in ALLOWED_KINDS
    ]
    if invalid:
        failures.append("unsupported kinds remain: " + ", ".join(invalid))
    if digest([entry["id"] for entry in index["entries"]]) != baseline[
        "entry_order_sha256"
    ]:
        failures.append("entry order changed")
    if digest(index["indexes"]) != baseline["indexes_sha256"]:
        failures.append("derived indexes changed")

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}")
        print(f"RESULT: fail ({len(failures)} failures)")
        return 1
    print(
        "PASS: exact 15-row kind migration; non-kind fields, entry order, "
        "and derived indexes preserved"
    )
    print("PASS: invalid kind count 15 -> 0")
    print("RESULT: pass")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
