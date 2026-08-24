#!/usr/bin/env python3
"""Compose a cumulative per-wave run plan from coordinator-emitted actions."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dispatch", required=True, type=Path)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--wave", required=True)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("actions", nargs="+", type=Path)
    args = parser.parse_args()

    dispatch = load(args.dispatch)
    strategy = dispatch["subagent_strategy"]
    wave = next(item for item in strategy["execution_waves"] if item["wave_id"] == args.wave)

    actions = []
    seen = set()
    for path in args.actions:
        payload = load(path)
        candidates = payload.get("actions") if isinstance(payload.get("actions"), list) else [payload]
        for action in candidates:
            action_id = action["action_id"]
            if action_id in seen:
                raise SystemExit(f"duplicate action id: {action_id}")
            if action["run_id"] != args.run_id:
                raise SystemExit(f"run id mismatch: {path}")
            seen.add(action_id)
            actions.append(action)

    actions.sort(key=lambda item: int(item["action_id"].split("-")[-1]))
    selected_ids = {item["role"] for item in actions if item["wave_id"] == args.wave}
    if selected_ids != set(wave["role_ids"]):
        raise SystemExit(f"selected role mismatch: {sorted(selected_ids)}")

    plan = {
        "action_artifacts": [str(path) for path in args.actions],
        "actions": actions,
        "dispatch_id": dispatch["dispatch_id"],
        "run_id": args.run_id,
        "schema_version": "arcanum.native-dispatch-runner.run-plan.v0.1",
        "selected_wave": {
            "depends_on_waves": wave.get("depends_on_waves", []),
            "gate_after": wave.get("gate_after"),
            "join_policy": wave.get("join_policy", "all"),
            "on_incomplete": wave.get("on_incomplete", "block"),
            "parallel": bool(wave.get("parallel", False)),
            "role_ids": wave["role_ids"],
            "wave_id": wave["wave_id"],
        },
        "state": "wave_ready",
        "validation_status": "pass",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
