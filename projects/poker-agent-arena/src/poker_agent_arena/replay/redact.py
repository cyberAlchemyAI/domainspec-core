from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any

from poker_agent_arena.constants import FORBIDDEN_PUBLIC_FIELDS
from poker_agent_arena.games.kuhn import KuhnGame
from poker_agent_arena.protocol.validation import find_forbidden_fields
from poker_agent_arena.transcript.io import read_jsonl


def replay_private_transcript(path: Path) -> tuple[bool, list[str]]:
    events = read_jsonl(path)
    by_hand: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for event in events:
        hand_id = event.get("hand_id")
        if hand_id:
            by_hand[hand_id].append(event)
    errors: list[str] = []
    for hand_id, hand_events in by_hand.items():
        start = next((event for event in hand_events if event["type"] == "hand_start"), None)
        result = next((event for event in hand_events if event["type"] == "hand_result"), None)
        if not start or not result:
            errors.append(f"{hand_id}: missing start/result")
            continue
        game = KuhnGame(
            match_id=start["match_id"],
            hand_id=hand_id,
            seed_handle=start["seed_handle"],
            raw_seed=start["raw_seed"],
            cards=start["private_cards"],
        )
        for event in hand_events:
            if event["type"] in {"action", "fallback"}:
                game.apply(event["action"])
        if not game.terminal:
            errors.append(f"{hand_id}: replay did not reach terminal state")
            continue
        replayed = game.result()
        if replayed["payouts"] != result["payouts"]:
            errors.append(f"{hand_id}: payout mismatch")
    return not errors, errors


def build_public_replay(events: list[dict[str, Any]]) -> dict[str, Any]:
    match_start = next(event for event in events if event["type"] == "match_start")
    hands: list[dict[str, Any]] = []
    hand_events: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for event in events:
        if "hand_id" in event:
            hand_events[event["hand_id"]].append(event)
    for hand_id, grouped in hand_events.items():
        start = next(event for event in grouped if event["type"] == "hand_start")
        result = next(event for event in grouped if event["type"] == "hand_result")
        actions = [
            {
                "type": event["type"],
                "seat_id": event["seat_id"],
                "agent_id": event["agent_id"],
                "action": event["action"],
                "event_code": event.get("event_code"),
            }
            for event in grouped
            if event["type"] in {"action", "fallback"}
        ]
        hands.append(
            {
                "hand_id": hand_id,
                "seed_handle": start["seed_handle"],
                "actions": actions,
                "final_history": result["final_history"],
                "revealed_cards": result["revealed_cards"],
                "payouts": result["payouts"],
            }
        )
    summary = next((event["summary"] for event in events if event["type"] == "match_summary"), {})
    return {
        "protocol_version": match_start["protocol_version"],
        "match_id": match_start["match_id"],
        "fixture_id": match_start["fixture_id"],
        "seed_handles": match_start["seed_handles"],
        "hands": hands,
        "diagnostics_summary": summary,
    }


def public_replay_redaction_pass(public_replay: dict[str, Any]) -> tuple[bool, list[str]]:
    hits = find_forbidden_fields(public_replay)
    for forbidden in FORBIDDEN_PUBLIC_FIELDS:
        if forbidden in str(public_replay):
            hits.append(f"string:{forbidden}")
    return not hits, hits
