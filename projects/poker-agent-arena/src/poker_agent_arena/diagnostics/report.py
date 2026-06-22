from __future__ import annotations

from typing import Any

from poker_agent_arena.constants import FIXTURE_ID, PROTOCOL_VERSION


def initial_agent_stats() -> dict[str, Any]:
    return {
        "clean_ev": 0,
        "fallback_inclusive_ev": 0,
        "decisions": 0,
        "invalid_decisions": 0,
        "timeouts": 0,
        "fallback_count": 0,
    }


def finalize_report(
    stats: dict[str, dict[str, Any]],
    hands: int,
    replay_determinism: bool,
    hidden_info_canary_pass: bool,
    public_replay_redaction_pass: bool,
    fallback_abuse_pass: bool,
) -> dict[str, Any]:
    agents: dict[str, Any] = {}
    for agent_id, data in stats.items():
        decisions = data["decisions"] or 1
        agents[agent_id] = {
            "clean_ev": data["clean_ev"],
            "fallback_inclusive_ev": data["fallback_inclusive_ev"],
            "invalid_rate": data["invalid_decisions"] / decisions,
            "timeout_rate": data["timeouts"] / decisions,
            "fallback_count": data["fallback_count"],
            "decisions": data["decisions"],
        }
    return {
        "protocol_version": PROTOCOL_VERSION,
        "fixture_id": FIXTURE_ID,
        "hands": hands,
        "agents": agents,
        "replay_determinism": replay_determinism,
        "hidden_info_canary_pass": hidden_info_canary_pass,
        "public_replay_redaction_pass": public_replay_redaction_pass,
        "fallback_abuse_pass": fallback_abuse_pass,
    }
