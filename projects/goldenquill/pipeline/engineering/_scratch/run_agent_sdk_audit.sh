#!/bin/bash
set -e
export PATH=/Users/goldenquill/.npm-global/bin:/opt/homebrew/opt/node/bin:$PATH

SCRATCH=/Users/goldenquill/Downloads/GoldenQuill/pipeline/engineering/_scratch
OUT_DIR=/Users/goldenquill/Downloads/GoldenQuill/pipeline/engineering/amendments/agent_sdk_thesis_2026-04-19/cross_family_audit
mkdir -p "$OUT_DIR"

echo "=== EDITOR (Llama 3.3 70B, Meta) ==="
EDITOR_PROMPT=$(cat "$SCRATCH/audit_editor_prompt.txt")
openclaw infer model run --gateway --model groq/llama-3.3-70b-versatile --prompt "$EDITOR_PROMPT" 2>&1 > "$OUT_DIR/editor_verdict_cycle1.md" && echo "Editor done → $OUT_DIR/editor_verdict_cycle1.md"
echo "--- First 20 lines ---"
head -20 "$OUT_DIR/editor_verdict_cycle1.md"

echo ""
echo "=== JUDGE (Gemini 2.5 Pro, Google) ==="
JUDGE_PROMPT=$(cat "$SCRATCH/audit_judge_prompt.txt")
openclaw infer model run --gateway --model google/gemini-2.5-pro --prompt "$JUDGE_PROMPT" 2>&1 > "$OUT_DIR/judge_verdict_cycle1.md" && echo "Judge done → $OUT_DIR/judge_verdict_cycle1.md"
echo "--- First 20 lines ---"
head -20 "$OUT_DIR/judge_verdict_cycle1.md"

echo ""
echo "=== RED TEAM (GPT-OSS 120B, OpenAI-OSS) ==="
REDTEAM_PROMPT=$(cat "$SCRATCH/audit_redteam_prompt.txt")
openclaw infer model run --gateway --model groq/openai/gpt-oss-120b --prompt "$REDTEAM_PROMPT" 2>&1 > "$OUT_DIR/red_team_verdict_cycle1.md" && echo "Red Team done → $OUT_DIR/red_team_verdict_cycle1.md"
echo "--- First 20 lines ---"
head -20 "$OUT_DIR/red_team_verdict_cycle1.md"

echo ""
echo "=== ALL THREE COMPLETE ==="
wc -l "$OUT_DIR"/*.md
