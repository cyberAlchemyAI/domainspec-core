#!/bin/bash
set -e
export PATH=/Users/goldenquill/.npm-global/bin:/opt/homebrew/opt/node/bin:$PATH

echo "=== ADD KIMI K2 TO ALLOWLIST ==="
openclaw config set 'agents.defaults.models["groq/moonshotai/kimi-k2-instruct-0905"]' '{}' --strict-json 2>&1 | tail -3

echo ""
echo "=== UPDATE judge ALIAS: qwen -> kimi ==="
openclaw models aliases remove judge 2>&1 | tail -1
openclaw models aliases add judge groq/moonshotai/kimi-k2-instruct-0905 2>&1 | tail -1

echo ""
echo "=== VERIFY ==="
echo "--- Allowlist keys ---"
openclaw config get agents.defaults.models --json 2>&1 | python3 -c "import json,sys; d=json.load(sys.stdin); [print(k) for k in d.keys()]"
echo "--- Aliases ---"
openclaw models aliases list --plain 2>&1
echo "--- Validate ---"
openclaw config validate --json 2>&1 | head -3

echo ""
echo "=== SMOKE TEST: KIMI JUDGE ==="
openclaw infer model run --gateway --model groq/moonshotai/kimi-k2-instruct-0905 --prompt 'You are a test endpoint. Output only these two characters: OK' 2>&1 | head -10
