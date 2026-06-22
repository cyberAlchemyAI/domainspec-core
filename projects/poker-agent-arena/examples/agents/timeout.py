#!/usr/bin/env python3
import json
import sys
import time

PROTOCOL_VERSION = "paa.l0.v1"


for line in sys.stdin:
    if not line.strip():
        continue
    decision = json.loads(line)
    time.sleep(decision.get("deadline_ms", 5000) / 1000 + 0.25)
    response = {
        "protocol_version": PROTOCOL_VERSION,
        "decision_id": decision["decision_id"],
        "action": {"type": "check"},
    }
    print(json.dumps(response, separators=(",", ":")), flush=True)
