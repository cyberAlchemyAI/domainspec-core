#!/usr/bin/env python3
"""3-seat cross-family code review probe — board-health-managed.

Uses logician.board_health to classify seat responses, apply the remedy
ladder (retry with more tokens, switch model, escalate), and surface a
DEGRADED board to the operator rather than silently emitting thin output.

Board (all reasoning-capable, three distinct provider families):
  - Judge    → qwen/qwen3-32b → moonshotai/kimi-k2-instruct (fallback)
  - Editor   → moonshotai/kimi-k2-instruct → llama-3.3-70b-versatile
  - Red Team → openai/gpt-oss-120b → qwen/qwen3-32b (fallback)

Anthropic authored the code → excluded (cross-family rigor, L-003).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

# Make pipeline.* importable without install.
# Portable: derive workspace root from this file's location.
# tools/code_review_probe.py → workspace root is one parent up.
# Override via QUILL_WORKSPACE env var if needed.
import os as _os
_REPO = Path(_os.environ.get("QUILL_WORKSPACE") or Path(__file__).resolve().parent.parent)
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from pipeline.logician.board_health import (  # noqa: E402
    ResponseInfo, Validator, run_seat_with_remedy, summarize_board_health,
)

FILES = [
    _REPO / "pipeline/logician/gates/topology_gate.py",
    _REPO / "pipeline/logician/gates/citation_verify.py",
    _REPO / "tools/dedup_skills.py",
]
ENV_PATH = Path.home() / ".openclaw" / ".env"
OUT_PATH = _REPO / "CODE_REVIEW_2026-04-14.md"
HEALTH_PATH = _REPO / "CODE_REVIEW_BOARD_HEALTH_2026-04-14.json"

env = {}
if ENV_PATH.exists():
    for line in ENV_PATH.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        env[k.strip()] = v.strip().strip('"').strip("'")

GROQ_KEY = env.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
if not GROQ_KEY:
    print("[probe] FATAL: GROQ_API_KEY not found", file=sys.stderr)
    sys.exit(2)

# Build one bundle of all three files; each seat gets the full bundle.
bundle_parts = []
for p in FILES:
    bundle_parts.append(f"===== FILE: {p.name} =====\n")
    bundle_parts.append(p.read_text(encoding="utf-8"))
    bundle_parts.append(f"\n===== END: {p.name} =====\n\n")
CODE_BUNDLE = "".join(bundle_parts)

SEATS = [
    {
        "name": "Judge",
        "models": ["qwen/qwen3-32b", "moonshotai/kimi-k2-instruct"],
        "framing": (
            "You are the Judge seat. Review three load-bearing Python files "
            "against rigorous spec criteria: correctness of classification "
            "logic, completeness of edge-case handling, unambiguous success/"
            "failure criteria, traceability of every docstring claim to "
            "actual code behavior, and whether fail-closed semantics actually "
            "fail closed. Probe for spec-contract gaps."
        ),
    },
    {
        "name": "Editor",
        "models": ["moonshotai/kimi-k2-instruct", "llama-3.3-70b-versatile"],
        "framing": (
            "You are the Editor seat. Review these three files for clarity, "
            "maintainability, and whether a non-coding operator could read "
            "the CLI output and act on it. Are error messages actionable? "
            "Do function names describe what they do? Are docstrings accurate "
            "vs. aspirational? Is any logic obscure enough it will bite in "
            "six months?"
        ),
    },
    {
        "name": "Red Team",
        "models": ["openai/gpt-oss-120b", "qwen/qwen3-32b"],
        "framing": (
            "You are the Red Team seat. Find bugs, security issues, race "
            "conditions, ordering errors where one function depends on state "
            "another doesn't produce, resource leaks (file handles, "
            "subprocess), input-validation gaps, and ways malformed or "
            "malicious input breaks fail-closed guarantees. Name the "
            "specific line/function for each issue."
        ),
    },
]

FRAME = (
    "\n\nAn Anthropic model authored these three files for the Golden Quill "
    "migration. They are load-bearing: topology_gate enforces filesystem "
    "zone boundaries (fail-closed); citation_verify blocks hallucinated "
    "citations (fail-closed on HALLUCINATION only); dedup_skills merges "
    "two skill trees with per-skill operator approval.\n\n"
    "OUTPUT CONTRACT (mandatory — if you do not follow this, your review "
    "is discarded and you fail the board):\n"
    "- Organize output by file. Use literal headers:\n"
    "    `## File: topology_gate.py`\n"
    "    `## File: citation_verify.py`\n"
    "    `## File: dedup_skills.py`\n"
    "- Under each file, 5 to 10 numbered findings.\n"
    "- Each finding MUST have this shape:\n"
    "    N. CATEGORY: <one of BRITTLE | RATIONALIZATION | GAP | ORDERING "
    "| AMBIGUOUS | BUG | SECURITY | RACE>\n"
    "       Location: <line number or function name>\n"
    "       What: <what is wrong>\n"
    "       Why: <why it matters in this migration's context>\n"
    "       Fix: <concrete remediation — not 'improve' or 'consider'>\n"
    "- End with a single paragraph headed "
    "`### If I were running these tonight:` — what from your seat's angle "
    "would make you pause before a production migration.\n\n"
    "Be direct. No congratulations. No grading. Probe.\n\n"
    "===== CODE BUNDLE BEGINS =====\n\n"
    f"{CODE_BUNDLE}\n"
    "===== CODE BUNDLE ENDS =====\n"
)

VALIDATOR = Validator(
    min_content_chars=1200,
    required_tags=["BRITTLE", "RATIONALIZATION", "GAP", "ORDERING",
                   "AMBIGUOUS", "BUG", "SECURITY", "RACE"],
    min_distinct_tags=3,
    required_sections=[
        "## File: topology_gate.py",
        "## File: citation_verify.py",
        "## File: dedup_skills.py",
    ],
    min_required_sections=3,
)


def _groq_call(model: str, system: str, user: str, max_tokens: int):
    """Returns (ResponseInfo, finish_reason, elapsed_seconds)."""
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        "temperature": 0.3,
        "max_tokens": max_tokens,
    }
    # Only models that support Groq's reasoning_format parameter.
    # kimi-k2-instruct explicitly rejects it with
    #   "`reasoning_format` is not supported with this model".
    if any(hint in model for hint in ("qwen", "gpt-oss")):
        payload["reasoning_format"] = "parsed"
    body = json.dumps(payload)
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        f.write(body)
        body_path = f.name
    t0 = time.time()
    try:
        proc = subprocess.run(
            [
                "curl", "-sS", "-X", "POST",
                "https://api.groq.com/openai/v1/chat/completions",
                "-H", f"Authorization: Bearer {GROQ_KEY}",
                "-H", "Content-Type: application/json",
                "-H", "User-Agent: openclaw-code-review/3.0",
                "--data-binary", f"@{body_path}",
                "--max-time", "420",
                "-w", "\n__HTTPCODE__%{http_code}",
            ],
            capture_output=True, text=True, timeout=450,
        )
    except subprocess.TimeoutExpired:
        return (
            ResponseInfo(http_code=-1, content="",
                        exception_type="TimeoutExpired",
                        exception_msg="curl wall-clock timeout"),
            "", time.time() - t0,
        )
    finally:
        try:
            os.unlink(body_path)
        except OSError:
            pass

    elapsed = time.time() - t0
    out = proc.stdout or ""
    if "__HTTPCODE__" in out:
        body_out, _, code_s = out.rpartition("__HTTPCODE__")
        try:
            http_code = int(code_s.strip())
        except ValueError:
            http_code = -1
    else:
        body_out = out
        http_code = -1

    if proc.returncode != 0 and http_code == -1:
        return (
            ResponseInfo(http_code=-1, content="",
                        exception_type="CurlError",
                        exception_msg=proc.stderr[:200],
                        body_snippet=body_out[:400]),
            "", elapsed,
        )

    if http_code != 200:
        return (
            ResponseInfo(http_code=http_code, content="",
                        body_snippet=body_out[:500]),
            "", elapsed,
        )

    try:
        data = json.loads(body_out)
        choice = data["choices"][0]
        msg = choice.get("message", {})
        content = msg.get("content") or ""
        reasoning = msg.get("reasoning") or ""
        finish_reason = choice.get("finish_reason", "") or ""
        return (
            ResponseInfo(
                http_code=200,
                content=content,
                reasoning=reasoning,
                body_snippet=body_out[:400],
            ),
            finish_reason,
            elapsed,
        )
    except Exception as e:
        return (
            ResponseInfo(http_code=200, content="",
                        exception_type=type(e).__name__,
                        exception_msg=str(e)[:200],
                        body_snippet=body_out[:400]),
            "", elapsed,
        )


def main() -> int:
    seat_results = []
    for seat in SEATS:
        print(f"[probe] === {seat['name']} ===", flush=True)

        def _call(model: str, max_tokens: int, _seat=seat):
            print(f"[probe]   calling {model} (max_tokens={max_tokens}) ...",
                  flush=True)
            resp, finish, elapsed = _groq_call(
                model, _seat["framing"], FRAME, max_tokens
            )
            print(
                f"[probe]     http={resp.http_code} content={len(resp.content)} "
                f"reasoning={len(resp.reasoning)} finish={finish!r} "
                f"elapsed={elapsed:.1f}s",
                flush=True,
            )
            return resp, finish, elapsed

        sr = run_seat_with_remedy(
            seat_name=seat["name"],
            candidate_models=seat["models"],
            call_fn=_call,
            validator=VALIDATOR,
            initial_max_tokens=16384,
            max_attempts_per_model=2,
        )
        seat_results.append(sr)
        print(
            f"[probe]   terminal: {sr.terminal_status} via {sr.final_model} "
            f"({len(sr.attempts)} attempts) — {'HEALTHY' if sr.healthy else sr.escalation_reason}",
            flush=True,
        )

    summary = summarize_board_health(seat_results)

    # --- Write board-health audit JSON -----------------------------------
    audit = {
        "summary": summary,
        "seats": [
            {
                "seat": r.seat_name,
                "final_model": r.final_model,
                "healthy": r.healthy,
                "terminal_status": r.terminal_status,
                "escalation_reason": r.escalation_reason,
                "attempts": [
                    {
                        "attempt": a.attempt,
                        "model": a.model,
                        "status": a.status,
                        "action": a.action,
                        "reason": a.reason,
                        "http_code": a.http_code,
                        "content_chars": a.content_chars,
                        "reasoning_chars": a.reasoning_chars,
                        "elapsed": a.elapsed,
                    }
                    for a in r.attempts
                ],
            }
            for r in seat_results
        ],
    }
    HEALTH_PATH.write_text(json.dumps(audit, indent=2), encoding="utf-8")

    # --- Write human review document -------------------------------------
    lines = [
        "---",
        "title: Cross-Family Code Review — topology_gate / citation_verify / dedup_skills (rev 3)",
        "date: 2026-04-14",
        "pattern: 3-seat cross-family code review (L-003) + board_health remedy ladder",
        "code_author: Anthropic / Claude Opus 4.6",
        f"board_status: {summary['board_status']}",
        f"seats_healthy: {summary['seats_healthy']}/{summary['seats_total']}",
        "---",
        "",
        f"# Cross-Family Code Review (rev 3) — board {summary['board_status']}",
        "",
    ]
    if summary["board_status"] != "HEALTHY":
        lines.append("> **WARNING: Board is DEGRADED.** One or more seats did "
                     "not return healthy output even after the remedy ladder. "
                     "Findings below are partial. See "
                     "`CODE_REVIEW_BOARD_HEALTH_2026-04-14.json` for diagnostics.")
        lines.append("")
        for u in summary["unhealthy_seats"]:
            lines.append(
                f"- **{u['seat']}** (final model: `{u['final_model']}`) — "
                f"terminal `{u['terminal_status']}` after {u['attempts']} attempt(s): "
                f"{u['escalation_reason']}"
            )
        lines.append("")

    for r in seat_results:
        badge = "HEALTHY" if r.healthy else f"DEGRADED — {r.terminal_status}"
        lines.append(f"## {r.seat_name} — `{r.final_model}` ({badge})")
        lines.append("")
        # Attempt trail
        lines.append("**Attempt trail:**")
        lines.append("")
        for a in r.attempts:
            lines.append(
                f"- attempt {a.attempt}: `{a.model}` → status `{a.status}`, "
                f"action `{a.action}`, http={a.http_code}, "
                f"content={a.content_chars}, reasoning={a.reasoning_chars}, "
                f"{a.elapsed}s — {a.reason}"
            )
        lines.append("")
        if r.content:
            lines.append(r.content)
        else:
            lines.append("_(no content returned)_")
        lines.append("")
        lines.append("---")
        lines.append("")

    OUT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"[probe] review written to {OUT_PATH}")
    print(f"[probe] board-health written to {HEALTH_PATH}")
    print(f"[probe] board_status: {summary['board_status']}")
    return 0 if summary["board_status"] == "HEALTHY" else 1


if __name__ == "__main__":
    sys.exit(main())
