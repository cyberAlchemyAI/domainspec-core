from __future__ import annotations

import argparse
import json
from pathlib import Path

from poker_agent_arena import __version__
from poker_agent_arena.constants import (
    DEFAULT_DECISION_TIMEOUT_MS,
    DEFAULT_PROCESS_KILL_AFTER_MS,
    FIXTURE_ID,
    PROJECT_ROOT,
    PROTOCOL_VERSION,
)
from poker_agent_arena.runner.match import replay_to_dir, run_eval


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="paa")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("doctor")

    run_parser = sub.add_parser("run")
    _add_match_args(run_parser)
    run_parser.add_argument("--seed-handle", default="kuhn-smoke-000")

    eval_parser = sub.add_parser("eval")
    _add_match_args(eval_parser)
    eval_parser.add_argument("--max-hands", type=int, default=None)

    replay_parser = sub.add_parser("replay")
    replay_parser.add_argument("transcript")
    replay_parser.add_argument("--out", required=True)

    args = parser.parse_args(argv)
    if args.command == "doctor":
        return _doctor()
    if args.command == "run":
        result = run_eval(
            args.agent_a,
            args.agent_b,
            Path(args.out),
            fixture_id=args.fixture,
            decision_timeout_ms=args.decision_timeout_ms,
            process_kill_after_ms=args.process_kill_after_ms,
            max_hands=1,
            single_seed_handle=args.seed_handle,
            seat_rotation=False,
        )
        print(json.dumps(result.summary, indent=2, sort_keys=True))
        return 0 if result.ok else 1
    if args.command == "eval":
        result = run_eval(
            args.agent_a,
            args.agent_b,
            Path(args.out),
            fixture_id=args.fixture,
            decision_timeout_ms=args.decision_timeout_ms,
            process_kill_after_ms=args.process_kill_after_ms,
            max_hands=args.max_hands,
            seat_rotation=True,
        )
        print(json.dumps(result.summary, indent=2, sort_keys=True))
        return 0 if result.ok else 1
    if args.command == "replay":
        report = replay_to_dir(Path(args.transcript), Path(args.out))
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0 if report["ok"] else 1
    return 2


def _add_match_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--fixture", default=FIXTURE_ID)
    parser.add_argument("--agent-a", required=True)
    parser.add_argument("--agent-b", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--decision-timeout-ms", type=int, default=DEFAULT_DECISION_TIMEOUT_MS)
    parser.add_argument("--process-kill-after-ms", type=int, default=DEFAULT_PROCESS_KILL_AFTER_MS)


def _doctor() -> int:
    required = [
        PROJECT_ROOT / "spec/l0/runtime/cli.md",
        PROJECT_ROOT / "spec/l0/protocol/decision-envelope.md",
        PROJECT_ROOT / "spec/l0/transcript/redaction-policy.md",
        PROJECT_ROOT / "fixtures/l0/kuhn_hidden_info/seeds.json",
        PROJECT_ROOT / "examples/agents/check_call.py",
        PROJECT_ROOT / "examples/agents/legal_random.py",
        PROJECT_ROOT / "examples/agents/timeout.py",
        PROJECT_ROOT / "examples/agents/invalid_json.py",
    ]
    checks = []
    missing = []
    for path in required:
        ok = path.exists()
        checks.append({"path": str(path.relative_to(PROJECT_ROOT)), "ok": ok})
        if not ok:
            missing.append(str(path.relative_to(PROJECT_ROOT)))
    result = {
        "ok": not missing,
        "version": __version__,
        "protocol_version": PROTOCOL_VERSION,
        "project_root": str(PROJECT_ROOT),
        "checks": checks,
        "missing": missing,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
