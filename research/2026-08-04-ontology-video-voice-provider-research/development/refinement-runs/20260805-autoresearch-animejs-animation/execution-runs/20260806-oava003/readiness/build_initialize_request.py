#!/usr/bin/env python3
"""Bind the passing OAVA-003 audit to one bounded Goal execution intent."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
request = {
    "operation": "initialize-readiness",
    "audit_config": json.loads((ROOT / "audit-config.json").read_text(encoding="utf-8")),
    "audit_report": json.loads(
        (ROOT / "audit-output" / "work-pack-readiness-report-v2.json").read_text(
            encoding="utf-8"
        )
    ),
    "source_invocation_id": "goal-oava-prototype-20260806-round001",
    "created_at": "2026-08-06T16:38:12Z",
    "execution_mode": "one-unit",
    "step_budget": 1,
}
(ROOT / "initialize-request.json").write_text(
    json.dumps(request, indent=2, sort_keys=True) + "\n", encoding="utf-8"
)
print(
    json.dumps(
        {
            "status": "pass",
            "source_invocation_id": request["source_invocation_id"],
            "execution_mode": request["execution_mode"],
            "step_budget": request["step_budget"],
        },
        indent=2,
    )
)
