from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from poker_agent_arena.constants import (
    DEFAULT_DECISION_TIMEOUT_MS,
    DEFAULT_PROCESS_KILL_AFTER_MS,
    FIXTURE_ID,
    PROJECT_ROOT,
    PROTOCOL_VERSION,
)
from poker_agent_arena.diagnostics.report import finalize_report, initial_agent_stats
from poker_agent_arena.games.kuhn import KuhnGame
from poker_agent_arena.protocol.validation import fallback_action, find_forbidden_fields, validate_action
from poker_agent_arena.replay.redact import build_public_replay, public_replay_redaction_pass, replay_private_transcript
from poker_agent_arena.runner.agent_process import AgentProcess
from poker_agent_arena.transcript.io import read_jsonl, write_jsonl


@dataclass
class AgentSpec:
    agent_id: str
    command: str


@dataclass
class RunResult:
    ok: bool
    out_dir: Path
    diagnostics: dict[str, Any]
    summary: dict[str, Any]


def load_seed_corpus() -> list[dict[str, str]]:
    path = PROJECT_ROOT / "fixtures/l0/kuhn_hidden_info/seeds.json"
    return json.loads(path.read_text(encoding="utf-8"))["seeds"]


def run_eval(
    agent_a: str,
    agent_b: str,
    out_dir: Path,
    fixture_id: str = FIXTURE_ID,
    decision_timeout_ms: int = DEFAULT_DECISION_TIMEOUT_MS,
    process_kill_after_ms: int = DEFAULT_PROCESS_KILL_AFTER_MS,
    max_hands: int | None = None,
    single_seed_handle: str | None = None,
    seat_rotation: bool = True,
) -> RunResult:
    if fixture_id != FIXTURE_ID:
        raise ValueError("Local Arena CLI v0 supports only kuhn_hidden_info")
    out_dir.mkdir(parents=True, exist_ok=True)
    seeds = load_seed_corpus()
    if single_seed_handle:
        seeds = [seed for seed in seeds if seed["seed_handle"] == single_seed_handle]
        if not seeds:
            raise ValueError(f"unknown seed handle: {single_seed_handle}")
    agent_specs = {"agent_a": AgentSpec("agent_a", agent_a), "agent_b": AgentSpec("agent_b", agent_b)}
    stats = {agent_id: initial_agent_stats() for agent_id in agent_specs}
    events: list[dict[str, Any]] = []
    match_id = "paa-local-eval-0001"
    seed_handles = [seed["seed_handle"] for seed in seeds]
    events.append(
        {
            "type": "match_start",
            "protocol_version": PROTOCOL_VERSION,
            "match_id": match_id,
            "fixture_id": fixture_id,
            "seed_handles": seed_handles,
            "decision_timeout_ms": decision_timeout_ms,
            "process_kill_after_ms": process_kill_after_ms,
        }
    )
    hidden_info_hits: list[str] = []
    hand_count = 0
    assignments = [("agent_a", "agent_b"), ("agent_b", "agent_a")] if seat_rotation else [("agent_a", "agent_b")]
    stop = False
    for seed in seeds:
        for seat_agents in assignments:
            if max_hands is not None and hand_count >= max_hands:
                stop = True
                break
            hand_count += 1
            hand_id = f"hand-{hand_count:04d}"
            seat_to_agent = {"seat_0": seat_agents[0], "seat_1": seat_agents[1]}
            game = KuhnGame(match_id, hand_id, seed["seed_handle"], seed["raw_seed"])
            events.append(
                {
                    "type": "hand_start",
                    "match_id": match_id,
                    "hand_id": hand_id,
                    "seed_handle": seed["seed_handle"],
                    "raw_seed": seed["raw_seed"],
                    "private_cards": dict(game.cards),
                    "seat_to_agent": dict(seat_to_agent),
                }
            )
            processes = {
                seat: AgentProcess(agent_specs[agent_id].command, agent_id)
                for seat, agent_id in seat_to_agent.items()
            }
            hand_fallback_agents: set[str] = set()
            decision_index = 0
            try:
                while not game.terminal:
                    seat = game.to_act()
                    assert seat is not None
                    agent_id = seat_to_agent[seat]
                    decision = game.decision_envelope(decision_index, decision_timeout_ms)
                    hidden_info_hits.extend(f"{hand_id}:{hit}" for hit in find_forbidden_fields(decision))
                    events.append(
                        {
                            "type": "decision",
                            "match_id": match_id,
                            "hand_id": hand_id,
                            "decision_id": decision["decision_id"],
                            "seat_id": seat,
                            "agent_id": agent_id,
                            "decision_envelope": decision,
                        }
                    )
                    stats[agent_id]["decisions"] += 1
                    response = processes[seat].request(decision, decision_timeout_ms)
                    accepted = False
                    event_code = response.event_code
                    action: dict[str, Any] | None = None
                    if response.status == "ok" and response.envelope is not None:
                        accepted, event_code, action = validate_action(response.envelope, decision)
                    if not accepted or action is None:
                        if event_code == "timeout":
                            stats[agent_id]["timeouts"] += 1
                        else:
                            stats[agent_id]["invalid_decisions"] += 1
                        stats[agent_id]["fallback_count"] += 1
                        hand_fallback_agents.add(agent_id)
                        action = fallback_action(decision["legal_actions"])
                        events.append(
                            {
                                "type": "fallback",
                                "match_id": match_id,
                                "hand_id": hand_id,
                                "decision_id": decision["decision_id"],
                                "seat_id": seat,
                                "agent_id": agent_id,
                                "event_code": event_code or "invalid",
                                "action": action,
                                "elapsed_ms": response.elapsed_ms,
                                "raw_stdout": response.raw_stdout,
                            }
                        )
                    else:
                        events.append(
                            {
                                "type": "action",
                                "match_id": match_id,
                                "hand_id": hand_id,
                                "decision_id": decision["decision_id"],
                                "seat_id": seat,
                                "agent_id": agent_id,
                                "action": action,
                                "elapsed_ms": response.elapsed_ms,
                            }
                        )
                    game.apply(action)
                    decision_index += 1
                result = game.result()
                agent_payouts = {seat_to_agent[seat]: payout for seat, payout in result["payouts"].items()}
                for agent_id, payout in agent_payouts.items():
                    stats[agent_id]["fallback_inclusive_ev"] += payout
                    if agent_id not in hand_fallback_agents:
                        stats[agent_id]["clean_ev"] += payout
                events.append(
                    {
                        "type": "hand_result",
                        "match_id": match_id,
                        "hand_id": hand_id,
                        "seat_to_agent": dict(seat_to_agent),
                        "winner": result["winner"],
                        "payouts": result["payouts"],
                        "agent_payouts": agent_payouts,
                        "showdown": result["showdown"],
                        "revealed_cards": result["revealed_cards"],
                        "final_history": result["final_history"],
                        "pot": result["pot"],
                    }
                )
            finally:
                for process in processes.values():
                    process.stop()
        if stop:
            break
    events.append({"type": "match_summary", "match_id": match_id, "summary": {"hands": hand_count, "stats": stats}})
    transcript_path = out_dir / "private-transcript.jsonl"
    write_jsonl(transcript_path, events)
    replay_ok, replay_errors = replay_private_transcript(transcript_path)
    public = build_public_replay(events)
    redaction_ok, redaction_hits = public_replay_redaction_pass(public)
    fallback_abuse_pass = _fallback_abuse_pass(stats)
    diagnostics = finalize_report(
        stats,
        hand_count,
        replay_ok,
        not hidden_info_hits,
        redaction_ok,
        fallback_abuse_pass,
    )
    diagnostics["replay_errors"] = replay_errors
    diagnostics["hidden_info_canary_hits"] = hidden_info_hits
    diagnostics["public_replay_redaction_hits"] = redaction_hits
    summary = {
        "ok": replay_ok and not hidden_info_hits and redaction_ok,
        "match_id": match_id,
        "transcript": str(transcript_path),
        "diagnostics": str(out_dir / "diagnostics-report.json"),
        "hands": hand_count,
    }
    (out_dir / "diagnostics-report.json").write_text(json.dumps(diagnostics, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return RunResult(bool(summary["ok"]), out_dir, diagnostics, summary)


def replay_to_dir(transcript_path: Path, out_dir: Path) -> dict[str, Any]:
    out_dir.mkdir(parents=True, exist_ok=True)
    events = read_jsonl(transcript_path)
    replay_ok, replay_errors = replay_private_transcript(transcript_path)
    public = build_public_replay(events)
    redaction_ok, redaction_hits = public_replay_redaction_pass(public)
    summary = next((event.get("summary", {}) for event in events if event["type"] == "match_summary"), {})
    diagnostics = {
        "protocol_version": PROTOCOL_VERSION,
        "fixture_id": FIXTURE_ID,
        "replay_determinism": replay_ok,
        "public_replay_redaction_pass": redaction_ok,
        "replay_errors": replay_errors,
        "public_replay_redaction_hits": redaction_hits,
        "source_summary": summary,
    }
    report = {
        "ok": replay_ok and redaction_ok,
        "source_transcript": str(transcript_path),
        "public_replay": str(out_dir / "public-replay.json"),
        "diagnostics_report": str(out_dir / "diagnostics-report.json"),
        "replay_errors": replay_errors,
    }
    (out_dir / "public-replay.json").write_text(json.dumps(public, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out_dir / "diagnostics-report.json").write_text(json.dumps(diagnostics, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out_dir / "replay-report.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def _fallback_abuse_pass(stats: dict[str, dict[str, Any]]) -> bool:
    clean_agents = [data for data in stats.values() if data["fallback_count"] == 0]
    failing_agents = [data for data in stats.values() if data["fallback_count"] > 0]
    if not clean_agents or not failing_agents:
        return True
    best_clean = max(data["fallback_inclusive_ev"] for data in clean_agents)
    best_failing = max(data["fallback_inclusive_ev"] for data in failing_agents)
    return best_failing <= best_clean
