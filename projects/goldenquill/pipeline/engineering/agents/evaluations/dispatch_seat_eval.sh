#!/bin/bash
# Seat Self-Evaluation Dispatch — runs each seat's model against its own old-vs-new prompt
# Usage: bash dispatch_seat_eval.sh
# Requires: OpenClaw 2026.4.14+, active API keys for all seat models
#
# Each seat's PRIMARY model reads its old SKILL.md and new agent prompt,
# then evaluates: what improved, what regressed, what's missing.

set -euo pipefail

BASE="$HOME/Downloads/GoldenQuill"
OLD_DIR="$BASE/skills"
NEW_DIR="$BASE/pipeline/engineering/agents"
OUT_DIR="$NEW_DIR/evaluations"
mkdir -p "$OUT_DIR"

TIMESTAMP=$(date +%Y%m%dT%H%M%S)

# ── Shared evaluation frame ──────────────────────────────────────────
read -r -d '' EVAL_FRAME <<'FRAME' || true
You are reviewing a proposed replacement for your own council seat prompt in the Tilth grant-writing pipeline. You have two documents:

OLD: The current SKILL.md that has been used to win 3 competitive grants in 2026.
NEW: The proposed v1 upgrade based on adversarial board review and research.

Evaluate with brutal honesty. This is your seat — you know the work better than anyone.

Report in this exact structure:

## IMPROVEMENTS (things NEW does better)
- [item]: [why it matters for grant outcomes]

## REGRESSIONS (things OLD did better that NEW lost or weakened)
- [item]: [what's at risk]

## MISSING (things neither version handles that should exist)
- [item]: [impact]

## TENSIONS (tradeoffs where reasonable people disagree)
- [item]: [both sides]

## VERDICT
[UPGRADE / DOWNGRADE / MIXED] — one sentence why.

## TOP 3 CHANGES before deploying NEW
1. [most critical]
2. [second]
3. [third]

Keep under 600 words. Be specific — cite section numbers and line content, not vibes.
FRAME

# ── Function: run one seat evaluation ────────────────────────────────
run_eval() {
  local seat="$1"
  local model="$2"
  local old_file="$3"
  local new_file="$4"
  local out_file="$OUT_DIR/${seat}_eval_${TIMESTAMP}.md"

  echo "▶ Evaluating $seat via $model ..."

  local old_content
  old_content=$(cat "$old_file")
  local new_content
  new_content=$(cat "$new_file")

  local prompt
  prompt=$(printf '%s\n\n--- OLD %s SKILL.md ---\n%s\n\n--- NEW %s agent v1 ---\n%s' \
    "$EVAL_FRAME" "$seat" "$old_content" "$seat" "$new_content")

  local result
  result=$(npx openclaw infer model run \
    --gateway \
    --model "$model" \
    --prompt "$prompt" \
    --json 2>&1) || true

  # Extract the text content from JSON response
  local text
  text=$(echo "$result" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    # Handle various response shapes
    if isinstance(data, dict):
        print(data.get('text', data.get('content', data.get('message', json.dumps(data)))))
    else:
        print(data)
except:
    print(sys.stdin.read())
" 2>/dev/null || echo "$result")

  cat > "$out_file" <<EOF
# ${seat^} Self-Evaluation — $(date +%Y-%m-%d)

**Model:** $model
**Old:** $old_file
**New:** $new_file

---

$text
EOF

  echo "✓ $seat → $out_file"
}

# ── Dispatch all five seats ──────────────────────────────────────────
# Models per router.yaml (primary for each seat)

echo "═══ Tilth Council Seat Self-Evaluation ═══"
echo "Timestamp: $TIMESTAMP"
echo ""

# Scout — ollama/mistral:7b is local; use escalation google/gemini-2.5-flash for eval
# (mistral:7b may not have enough reasoning depth for comparative analysis)
run_eval "scout" "google/gemini-2.5-flash" \
  "$OLD_DIR/scout-discovery/SKILL.md" \
  "$NEW_DIR/scout_discovery_agent_v1.md"

# Scribe — anthropic/claude-sonnet-4-6
run_eval "scribe" "anthropic/claude-sonnet-4-6" \
  "$OLD_DIR/scribe-ghostwriter/SKILL.md" \
  "$NEW_DIR/scribe_writer_agent_v1.md"

# Editor — groq/llama-3.3-70b-versatile
run_eval "editor" "groq/llama-3.3-70b-versatile" \
  "$OLD_DIR/editor/SKILL.md" \
  "$NEW_DIR/editor_clarity_agent_v1.md"

# Judge — google/gemini-2.5-pro
run_eval "judge" "google/gemini-2.5-pro" \
  "$OLD_DIR/judge-rubric/SKILL.md" \
  "$NEW_DIR/judge_scoring_agent_v1.md"

# Logician is deterministic (no LLM) — use Red Team model for adversarial eval
run_eval "logician" "groq/openai/gpt-oss-120b" \
  "$OLD_DIR/logician/SKILL.md" \
  "$NEW_DIR/logician_enforcement_agent_v1.md"

echo ""
echo "═══ All evaluations complete ═══"
echo "Results in: $OUT_DIR/"
echo ""
echo "Next: read all 5 eval files and synthesize a deployment decision."
