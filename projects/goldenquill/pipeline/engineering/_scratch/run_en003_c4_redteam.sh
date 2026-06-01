#!/bin/bash
set -e
export PATH=/Users/goldenquill/.npm-global/bin:/opt/homebrew/opt/node/bin:/usr/local/bin:/opt/homebrew/bin:$PATH

SCRATCH=/Users/goldenquill/Downloads/GoldenQuill/pipeline/engineering/_scratch
OUT_DIR=/Users/goldenquill/Downloads/GoldenQuill/pipeline/engineering/amendments/agent_sdk_thesis_2026-04-19/en003_cross_family_audit_cycle4
mkdir -p "$OUT_DIR"

PROMPT="$(cat "$SCRATCH/en003_c4_redteam_prompt.txt")"

# Write header so verdict file is human-readable even if dispatch fails.
{
  echo "model.run via gateway"
  echo "provider: groq"
  echo "model: openai/gpt-oss-120b"
  echo "dispatched_at: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  echo "prompt_sha256: $(shasum -a 256 "$SCRATCH/en003_c4_redteam_prompt.txt" | awk '{print $1}')"
  echo ""
} > "$OUT_DIR/red_team_verdict.md"

# Dispatch. --json emits {"outputs":[{"text":"..."}]} but legacy path writes plain text; append whichever arrives.
openclaw infer model run --gateway --model groq/openai/gpt-oss-120b --prompt "$PROMPT" --json \
  >> "$OUT_DIR/red_team_verdict.md" 2>&1

echo ""
echo "=== DISPATCH COMPLETE ==="
echo "verdict file: $OUT_DIR/red_team_verdict.md"
wc -l "$OUT_DIR/red_team_verdict.md"
