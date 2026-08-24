#!/usr/bin/env python3
"""Build the first deterministic OAVA-003 outer-loop decision request."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
initialized = json.loads((ROOT / "initialize-result.json").read_text(encoding="utf-8"))
request = {
    "operation": "decide",
    "policy": initialized["policy"],
    "state": initialized["state"],
    "available_inputs": [],
    "installed_owner_routes": ["task-session:execute", "invoke:refresh"],
}
(ROOT / "decide-selection-request.json").write_text(
    json.dumps(request, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
print(json.dumps({"status": "pass", "phase": initialized["state"]["phase"]}, indent=2))
