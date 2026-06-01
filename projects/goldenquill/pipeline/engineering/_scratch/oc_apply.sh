#!/bin/bash
set -e
export PATH=/Users/goldenquill/.npm-global/bin:/opt/homebrew/opt/node/bin:$PATH

BATCH=/Users/goldenquill/Downloads/GoldenQuill/pipeline/engineering/_scratch/openclaw_cross_family_allowlist_batch.json

echo "=== D.2 APPLY BATCH ==="
openclaw config set --batch-file "$BATCH" --strict-json 2>&1
echo "--- Validate post-change ---"
openclaw config validate --json 2>&1 | head -10

echo ""
echo "=== D.3 REGISTER ROLE ALIASES ==="
openclaw models aliases add editor   groq/llama-3.3-70b-versatile 2>&1
openclaw models aliases add judge    groq/qwen/qwen3-32b 2>&1
openclaw models aliases add red_team groq/openai/gpt-oss-120b 2>&1
echo "--- Current aliases ---"
openclaw models aliases list --plain 2>&1 | head -20

echo ""
echo "=== D.4 RE-VERIFY ==="
echo "--- Health ---"
openclaw health 2>&1 | head -3
echo "--- Updated allowlist (keys only) ---"
openclaw config get agents.defaults.models --json 2>&1 | python3 -c "import json,sys; d=json.load(sys.stdin); print(list(d.keys()))" 2>&1
echo "--- Auth allowed list ---"
OPENCLAW_AGENT_DIR="$HOME/.openclaw/agents/tilth/agent" openclaw infer model auth status 2>&1 | grep -E '"allowed"' -A 6 || echo "(allowed list not shown)"
