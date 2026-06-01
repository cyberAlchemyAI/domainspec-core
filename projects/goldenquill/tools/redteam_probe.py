#!/usr/bin/env python3
"""Cross-family Red Team probe of the final migration plan.

Routes to Groq GPT-OSS-120B (non-Anthropic, reasoning enabled) via openclaw.
Thesis-defense style: probing questions, not grades.
"""
import subprocess
import sys
from pathlib import Path

PLAN_PATH = Path("/Users/goldenquill/Downloads/GoldenQuill/MIGRATION_PLAN_FINAL_2026-04-14.md")
OPENCLAW = Path.home() / ".npm-global" / "bin" / "openclaw"
OUT_PATH = Path("/Users/goldenquill/Downloads/GoldenQuill/REDTEAM_REVIEW_2026-04-14.md")

plan = PLAN_PATH.read_text()

framing = """You are the Red Team seat on the Tilth council. Your job is adversarial probing — not grading.

An Anthropic model (Claude Opus 4.6) just authored the migration + Tilth upgrade plan below. Probe it like a thesis-defense board member. Find weak points a skeptical reviewer would hit. Identify rationalizations disguised as decisions. Name risks the plan waves at but does not actually close. Find order-of-operations errors where a later gate depends on something an earlier gate did not actually produce. Challenge unstated assumptions.

Be specific. Every finding in remediation-shape: WHICH gate/section, WHAT is wrong or weak, WHY it matters, HOW to fix or strengthen.

Categorize each finding as one of:
- BRITTLE (works in the happy path, fails under realistic stress)
- RATIONALIZATION (the plan defends a choice that should be reconsidered)
- GAP (a risk or step is missing entirely)
- ORDERING (dependency between steps is wrong)

Do not be polite. Do not grade. Do not congratulate. Probe.

===== PLAN BEGINS =====

"""

closing = """

===== PLAN ENDS =====

Return 8–15 probing findings, numbered, categorized. End with a single paragraph: if you were Josh, what would make you pause before starting Gate 1?"""

prompt = framing + plan + closing

print(f"[probe] prompt length: {len(prompt):,} chars")
print(f"[probe] routing to groq openai/gpt-oss-120b via openclaw infer model run")
print(f"[probe] Anthropic is NOT in the loop for this review.")

result = subprocess.run(
    [
        str(OPENCLAW),
        "infer", "model", "run",
        "--model", "openai/gpt-oss-120b",
        "--prompt", prompt,
    ],
    capture_output=True,
    text=True,
    timeout=300,
)

stdout = result.stdout
stderr = result.stderr

print(f"[probe] exit code: {result.returncode}")
print(f"[probe] stdout bytes: {len(stdout)}")
print(f"[probe] stderr bytes: {len(stderr)}")

OUT_PATH.write_text(
    f"---\ntitle: Red Team probe of MIGRATION_PLAN_FINAL_2026-04-14.md\n"
    f"date: 2026-04-14\nreviewer: Groq / GPT-OSS-120B (non-Anthropic)\n"
    f"author_of_plan: Anthropic / Claude Opus 4.6\n"
    f"pattern: cross-family adversarial review (L-003)\n---\n\n"
    f"# Red Team Probe\n\n"
    f"## Output\n\n{stdout}\n\n"
    f"## Stderr (if any)\n\n```\n{stderr}\n```\n"
)

print(f"[probe] written to {OUT_PATH}")
sys.exit(result.returncode)
