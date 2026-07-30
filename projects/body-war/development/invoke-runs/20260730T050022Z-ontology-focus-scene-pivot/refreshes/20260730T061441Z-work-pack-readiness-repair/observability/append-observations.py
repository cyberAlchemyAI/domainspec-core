#!/usr/bin/env python3
"""Append exactly one validated central signal per local envelope."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[7]
LEDGER = ROOT / ".arcanum/observability/signals/sigil-invocations.jsonl"
ENVELOPES = [
    HERE / "SPELLCRAFT-ENVELOPE.json",
    HERE / "INVOKE-REFRESH-ENVELOPE.json",
]
REQUIRED = {
    "timestamp",
    "run_id",
    "session_id",
    "sigil",
    "tier",
    "mode",
    "evidence",
    "request",
    "execution",
    "observer",
    "target_artifact",
}


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"JSON object required: {path}")
    missing = REQUIRED - set(value)
    if missing:
        raise ValueError(f"{path}: missing {sorted(missing)}")
    return value


def main() -> int:
    existing = LEDGER.read_text(encoding="utf-8").splitlines()
    parsed = [json.loads(line) for line in existing if line.strip()]
    dedupe = {item.get("dedupe_key") for item in parsed}
    rows = []
    for path in ENVELOPES:
        row = load(path)
        row["dedupe_key"] = (
            f"{row['run_id']}:signal-observer:0.1.0"
        )
        row["observer_version"] = "0.1.0"
        if row["dedupe_key"] in dedupe:
            raise SystemExit(f"duplicate observation: {row['dedupe_key']}")
        dedupe.add(row["dedupe_key"])
        rows.append(
            json.dumps(
                row,
                sort_keys=True,
                separators=(",", ":"),
                ensure_ascii=False,
            )
        )
    descriptor = os.open(LEDGER, os.O_WRONLY | os.O_APPEND)
    with os.fdopen(descriptor, "a", encoding="utf-8") as handle:
        for row in rows:
            handle.write(row + "\n")
        handle.flush()
        os.fsync(handle.fileno())
    final = LEDGER.read_text(encoding="utf-8").splitlines()
    appended = [json.loads(line) for line in final[-len(rows) :]]
    if [item["dedupe_key"] for item in appended] != [
        json.loads(row)["dedupe_key"] for row in rows
    ]:
        raise SystemExit("appended observation validation failed")
    receipt = {
        "schema_version": "signal-observer.append-receipt.v1",
        "ledger": str(LEDGER.relative_to(ROOT)),
        "appended": len(rows),
        "dedupe_keys": [item["dedupe_key"] for item in appended],
        "validation": "pass",
    }
    (HERE / "OBSERVATION-RECEIPT.json").write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(receipt, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
