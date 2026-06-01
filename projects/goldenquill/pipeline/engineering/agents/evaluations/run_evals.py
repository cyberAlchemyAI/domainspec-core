#!/usr/bin/env python3
"""Run each Tilth council seat's model against its own old-vs-new prompt upgrade."""
import subprocess, json, os, sys
from pathlib import Path
from datetime import date

BASE = Path.home() / "Downloads" / "GoldenQuill"
OLD_DIR = BASE / "skills"
NEW_DIR = BASE / "pipeline" / "engineering" / "agents"
OUT_DIR = NEW_DIR / "evaluations"
OUT_DIR.mkdir(parents=True, exist_ok=True)

EVAL_HEADER = """You are reviewing a proposed replacement for the {seat} council seat prompt in the Tilth grant-writing AI pipeline. The OLD prompt has been used to win 3 competitive grants in 2026. The NEW prompt is a proposed upgrade informed by an adversarial board review (5 cross-perspective reviewers).

Evaluate with brutal honesty. This is YOUR seat.

Report in this exact structure (no other sections):

## IMPROVEMENTS (what NEW does better for grant outcomes)
## REGRESSIONS (what OLD did better that NEW lost or weakened)
## MISSING (gaps in both versions)
## TENSIONS (tradeoffs where reasonable people would disagree)
## VERDICT: UPGRADE / DOWNGRADE / MIXED — one sentence
## TOP 3 CHANGES before deploying NEW as replacement

Under 500 words. Cite specific sections and content, not vibes."""

SEATS = [
    {
        "name": "scout",
        "model": "google/gemini-2.5-flash",
        "old": OLD_DIR / "scout-discovery" / "SKILL.md",
        "new": NEW_DIR / "scout_discovery_agent_v1.md",
    },
    {
        "name": "scribe",
        "model": "groq/qwen/qwen3-32b",  # fallback — Anthropic rate-limited by active Cowork session
        "old": OLD_DIR / "scribe-ghostwriter" / "SKILL.md",
        "new": NEW_DIR / "scribe_writer_agent_v1.md",
    },
    {
        "name": "editor",
        "model": "groq/llama-3.3-70b-versatile",
        "old": OLD_DIR / "editor" / "SKILL.md",
        "new": NEW_DIR / "editor_clarity_agent_v1.md",
    },
    {
        "name": "judge",
        "model": "google/gemini-2.5-pro",
        "old": OLD_DIR / "judge-rubric" / "SKILL.md",
        "new": NEW_DIR / "judge_scoring_agent_v1.md",
    },
    {
        "name": "logician",
        "model": "groq/openai/gpt-oss-120b",
        "old": OLD_DIR / "logician" / "SKILL.md",
        "new": NEW_DIR / "logician_enforcement_agent_v1.md",
    },
]

def run_one(seat_info):
    name = seat_info["name"]
    model = seat_info["model"]
    old_text = seat_info["old"].read_text()
    new_text = seat_info["new"].read_text()

    prompt = (
        EVAL_HEADER.format(seat=name.upper())
        + f"\n\n--- OLD {name.upper()} ---\n{old_text}"
        + f"\n\n--- NEW {name.upper()} ---\n{new_text}"
    )

    print(f"  [{name}] calling {model} ...", flush=True)
    try:
        result = subprocess.run(
            ["npx", "openclaw", "infer", "model", "run",
             "--gateway", "--model", model, "--prompt", prompt, "--json"],
            capture_output=True, text=True, timeout=180,
            env={**os.environ, "PATH": "/opt/homebrew/bin:/usr/local/bin:" + os.environ.get("PATH", "")}
        )
        raw = result.stdout.strip()
        try:
            data = json.loads(raw)
            if data.get("ok"):
                text = data["outputs"][0]["text"]
            else:
                text = f"ERROR: {json.dumps(data, indent=2)}"
        except json.JSONDecodeError:
            text = raw or result.stderr
    except subprocess.TimeoutExpired:
        text = "TIMEOUT: model did not respond within 180s"
    except Exception as e:
        text = f"EXCEPTION: {e}\nstdout: {getattr(e, 'stdout', '')}\nstderr: {getattr(e, 'stderr', '')}"

    out_file = OUT_DIR / f"{name}_eval.md"
    out_file.write_text(
        f"# {name.upper()} Self-Evaluation — {date.today()}\n\n"
        f"**Model:** {model}\n"
        f"**Old:** {seat_info['old']}\n"
        f"**New:** {seat_info['new']}\n\n---\n\n{text}\n"
    )
    print(f"  [{name}] done -> {out_file.name}", flush=True)
    return name, text


if __name__ == "__main__":
    # Run specific seat if passed as arg, otherwise all
    targets = SEATS
    if len(sys.argv) > 1:
        names = [a.lower() for a in sys.argv[1:]]
        targets = [s for s in SEATS if s["name"] in names]

    print(f"=== Tilth Seat Self-Evaluation ({date.today()}) ===\n")
    for seat in targets:
        run_one(seat)
    print(f"\n=== Done. Results in {OUT_DIR}/ ===")
