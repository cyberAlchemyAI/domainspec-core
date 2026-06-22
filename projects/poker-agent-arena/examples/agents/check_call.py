#!/usr/bin/env python3
import json
import sys

PROTOCOL_VERSION = "paa.l0.v1"


def choose(legal_actions):
    names = [action["type"] for action in legal_actions]
    for preferred in ("check", "call", "fold", "bet"):
        if preferred in names:
            action = {"type": preferred}
            legal = legal_actions[names.index(preferred)]
            if "min_amount" in legal:
                action["amount"] = legal["min_amount"]
            return action
    return {"type": names[0]}


for line in sys.stdin:
    if not line.strip():
        continue
    decision = json.loads(line)
    response = {
        "protocol_version": PROTOCOL_VERSION,
        "decision_id": decision["decision_id"],
        "action": choose(decision["legal_actions"]),
    }
    print(json.dumps(response, separators=(",", ":")), flush=True)
