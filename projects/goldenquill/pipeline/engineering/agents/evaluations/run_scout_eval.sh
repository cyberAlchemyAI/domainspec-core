#!/bin/bash
set -euo pipefail
BASE="$HOME/Downloads/GoldenQuill"
OUT="$BASE/pipeline/engineering/agents/evaluations/scout_eval.md"

EVAL_PROMPT="You are reviewing a proposed replacement for the SCOUT council seat prompt in the Tilth grant-writing AI pipeline. The OLD prompt has been used to win 3 competitive grants in 2026. The NEW prompt is a proposed upgrade based on adversarial board review.

Evaluate with brutal honesty. This is YOUR seat.

Report exactly:
## IMPROVEMENTS (NEW does better)
## REGRESSIONS (OLD did better or NEW lost something)
## MISSING (gaps in both)
## TENSIONS (tradeoffs)
## VERDICT: UPGRADE / DOWNGRADE / MIXED — one sentence
## TOP 3 CHANGES before deploying

Under 500 words. Cite specifics.

--- OLD SCOUT ---
$(cat "$BASE/skills/scout-discovery/SKILL.md")

--- NEW SCOUT ---
$(cat "$BASE/pipeline/engineering/agents/scout_discovery_agent_v1.md")"

RESULT=$(npx openclaw infer model run --gateway --model google/gemini-2.5-flash --prompt "$EVAL_PROMPT" --json 2>&1)

echo "# Scout Self-Evaluation — $(date +%Y-%m-%d)" > "$OUT"
echo "" >> "$OUT"
echo "**Model:** google/gemini-2.5-flash (Scout escalation)" >> "$OUT"
echo "" >> "$OUT"
echo "$RESULT" >> "$OUT"
echo "✓ Scout eval → $OUT"
