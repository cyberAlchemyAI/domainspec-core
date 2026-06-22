from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from poker_agent_arena.constants import FALLBACK_ORDER, FORBIDDEN_PUBLIC_FIELDS, PROTOCOL_VERSION
from poker_agent_arena.games.kuhn import normalize_action


@dataclass
class ParsedOutput:
    status: str
    envelope: dict[str, Any] | None = None
    event_code: str | None = None
    raw_stdout: str = ""


def parse_agent_output(line: str) -> ParsedOutput:
    raw = line.rstrip("\n")
    stripped = raw.strip()
    if not stripped:
        return ParsedOutput("invalid", event_code="malformed_json", raw_stdout=raw)
    if not stripped.startswith("{"):
        return ParsedOutput("invalid", event_code="prose_before_json", raw_stdout=raw)
    decoder = json.JSONDecoder()
    try:
        obj, idx = decoder.raw_decode(stripped)
    except json.JSONDecodeError:
        return ParsedOutput("invalid", event_code="malformed_json", raw_stdout=raw)
    if stripped[idx:].strip():
        return ParsedOutput("invalid", event_code="extra_json_object", raw_stdout=raw)
    if not isinstance(obj, dict):
        return ParsedOutput("invalid", event_code="malformed_json", raw_stdout=raw)
    return ParsedOutput("ok", envelope=obj, raw_stdout=raw)


def validate_action(
    action_envelope: dict[str, Any],
    decision_envelope: dict[str, Any],
) -> tuple[bool, str | None, dict[str, Any] | None]:
    if action_envelope.get("protocol_version") != PROTOCOL_VERSION:
        return False, "malformed_json", None
    if action_envelope.get("decision_id") != decision_envelope["decision_id"]:
        return False, "mismatched_decision_id", None
    if "action" not in action_envelope:
        return False, "missing_action", None
    action = normalize_action(action_envelope["action"])
    action_type = action.get("type")
    legal = decision_envelope["legal_actions"]
    legal_match = next((item for item in legal if item["type"] == action_type), None)
    if legal_match is None:
        return False, "illegal_action", None
    if "min_amount" in legal_match or "max_amount" in legal_match:
        amount = action.get("amount")
        if not isinstance(amount, int):
            return False, "illegal_amount", None
        if amount < legal_match.get("min_amount", amount) or amount > legal_match.get("max_amount", amount):
            return False, "illegal_amount", None
    return True, None, action


def fallback_action(legal_actions: list[dict[str, Any]]) -> dict[str, Any]:
    for preferred in FALLBACK_ORDER:
        for candidate in legal_actions:
            if candidate["type"] == preferred:
                action = {"type": preferred}
                if "min_amount" in candidate:
                    action["amount"] = candidate["min_amount"]
                return action
    if not legal_actions:
        raise RuntimeError("cannot fallback without legal actions")
    candidate = legal_actions[0]
    action = {"type": candidate["type"]}
    if "min_amount" in candidate:
        action["amount"] = candidate["min_amount"]
    return action


def find_forbidden_fields(value: Any, path: str = "$") -> list[str]:
    hits: list[str] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            child_path = f"{path}.{key}"
            if key in FORBIDDEN_PUBLIC_FIELDS:
                hits.append(child_path)
            hits.extend(find_forbidden_fields(nested, child_path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            hits.extend(find_forbidden_fields(item, f"{path}[{index}]"))
    return hits
