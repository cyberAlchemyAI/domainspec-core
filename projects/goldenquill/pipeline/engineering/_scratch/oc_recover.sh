#!/bin/bash
set -e
export PATH=/Users/goldenquill/.npm-global/bin:/opt/homebrew/opt/node/bin:$PATH

BAK="$HOME/.openclaw/openclaw.json.bak.pre-groq-allowlist-20260419T233111Z"

echo "=== RESTORE FROM BACKUP ==="
echo "--- Backup exists? ---"
ls -la "$BAK" 2>&1

echo "--- Restoring ---"
cp "$BAK" "$HOME/.openclaw/openclaw.json" && echo "RESTORE_OK"

echo "--- Validate restored ---"
openclaw config validate --json 2>&1 | head -3

echo "--- Post-restore allowlist ---"
openclaw config get agents.defaults.models --json 2>&1 | python3 -c "import json,sys; d=json.load(sys.stdin); print(list(d.keys()))"

echo ""
echo "=== RE-APPLY VIA INDIVIDUAL CONFIG SET CALLS ==="
openclaw config set 'agents.defaults.models["groq/llama-3.3-70b-versatile"]' '{}' --strict-json 2>&1 | tail -3
openclaw config set 'agents.defaults.models["groq/qwen/qwen3-32b"]' '{}' --strict-json 2>&1 | tail -3
openclaw config set 'agents.defaults.models["groq/openai/gpt-oss-120b"]' '{}' --strict-json 2>&1 | tail -3

echo ""
echo "--- Validate ---"
openclaw config validate --json 2>&1 | head -3

echo "--- Allowlist keys after re-apply ---"
openclaw config get agents.defaults.models --json 2>&1 | python3 -c "import json,sys; d=json.load(sys.stdin); print(list(d.keys()))"

echo ""
echo "=== RE-REGISTER ALIASES ==="
openclaw models aliases add editor   groq/llama-3.3-70b-versatile 2>&1 | tail -1
openclaw models aliases add judge    groq/qwen/qwen3-32b 2>&1 | tail -1
openclaw models aliases add red_team groq/openai/gpt-oss-120b 2>&1 | tail -1

echo "--- Aliases list ---"
openclaw models aliases list --plain 2>&1
