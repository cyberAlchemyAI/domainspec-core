#!/usr/bin/env python3
import json
import random
import sys

PROTOCOL_VERSION = "paa.l0.v1"


def choose(decision):
    rng = random.Random(decision["decision_id"])
    legal = rng.choice(decision["legal_actions"])
    action = {"type": legal["type"]}
    if "min_amount" in legal:
        action["amount"] = legal["min_amount"]
    return action


for line in sys.stdin:
    if not line.strip():
        continue
    decision = json.loads(line)
    response = {
        "protocol_version": PROTOCOL_VERSION,
        "decision_id": decision["decision_id"],
        "action": choose(decision),
    }
    print(json.dumps(response, separators=(",", ":")), flush=True)
