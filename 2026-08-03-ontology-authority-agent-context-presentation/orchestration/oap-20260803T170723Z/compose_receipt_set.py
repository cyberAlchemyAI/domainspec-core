#!/usr/bin/env python3
"""Materialize exactly the agent receipts admitted by a cumulative run plan."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-plan", required=True, type=Path)
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    plan = json.loads(args.run_plan.read_text(encoding="utf-8"))
    expected = {item["action_id"] for item in plan["actions"]}
    found = {}
    for path in sorted(args.source.glob("*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        action_id = payload.get("action_id")
        if action_id in expected:
            if action_id in found:
                raise SystemExit(f"duplicate receipt for {action_id}")
            found[action_id] = (path, payload)
    missing = sorted(expected - set(found))
    if missing:
        raise SystemExit(f"missing receipts: {missing}")
    args.output.mkdir(parents=True, exist_ok=False)
    for action_id in sorted(found, key=lambda value: int(value.split("-")[-1])):
        source_path, payload = found[action_id]
        target = args.output / source_path.name
        target.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"{args.output}: {len(found)} receipts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
