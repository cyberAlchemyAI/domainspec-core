#!/usr/bin/env python3
"""Validate the Studio work-pack chain and its Craft projections."""

from __future__ import annotations

import json
import re
from pathlib import Path

import yaml


PROJECT_ROOT = Path(__file__).resolve().parents[4]
WORK_PACK_ROOT = (
    PROJECT_ROOT
    / "development/invoke-runs/20260727T042935Z-architecture-review-refresh"
)
CHAIN_ROOT = Path(__file__).resolve().parents[1]

FRONTIER = [f"SWU-GSP-{index:03d}" for index in range(1, 8)]
DEPENDENCIES = {
    "SWU-GSP-001": "none",
    **{
        f"SWU-GSP-{index:03d}": f"SWU-GSP-{index - 1:03d}"
        for index in range(2, 8)
    },
}
TASK_FILES = {
    swu: next((WORK_PACK_ROOT / "work-pack/tasks").glob(f"TASK-GSP-{swu[-3:]}-*.md"))
    for swu in FRONTIER
}


def validate_indexes(ledger: dict[str, object]) -> None:
    indexes = ledger["indexes"]["by_id"]
    for identifier, locator in indexes.items():
        match = re.fullmatch(r"([a-z_]+)\[(\d+)\]", locator)
        if match is None:
            raise AssertionError(f"invalid locator for {identifier}: {locator}")
        collection, raw_index = match.groups()
        row = ledger[collection][int(raw_index)]
        row_id = next(
            value for key, value in row.items() if key.endswith("_id")
        )
        if row_id != identifier:
            raise AssertionError(
                f"index mismatch for {identifier}: found {row_id}"
            )


def main() -> None:
    work_pack = (WORK_PACK_ROOT / "WORK-PACK.md").read_text(encoding="utf-8")
    for swu, dependency in DEPENDENCIES.items():
        task = TASK_FILES[swu]
        if not task.exists():
            raise AssertionError(f"missing task for {swu}")
        text = task.read_text(encoding="utf-8")
        if f"This task binds `{swu}`" not in text:
            raise AssertionError(f"missing closeout binding for {swu}")
        if dependency != "none" and f"`{dependency}`" not in text:
            raise AssertionError(f"missing dependency {dependency} for {swu}")
    ordered = " → ".join(FRONTIER)
    normalized_work_pack = " ".join(
        work_pack.replace("`", "").splitlines()
    )
    if ordered not in normalized_work_pack:
        raise AssertionError("captured frontier is absent or out of order")
    for schema_name in (
        "task-session-result.schema.json",
        "closeout-owner-receipt.schema.json",
        "chain-state.schema.json",
    ):
        json.loads(
            (CHAIN_ROOT / "schemas" / schema_name).read_text(encoding="utf-8")
        )
    ledger = yaml.safe_load(
        (PROJECT_ROOT / ".craft/ledger.yml").read_text(encoding="utf-8")
    )
    validate_indexes(ledger)
    if (
        ledger["indexes"]["by_id"]["DEC-GSP-CHAIN-ORDER-031"]
        != "decisions[33]"
    ):
        raise AssertionError("chain decision index missing")
    print("chain-contract: pass")


if __name__ == "__main__":
    main()
