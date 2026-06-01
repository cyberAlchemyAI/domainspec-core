#!/bin/bash
set -e
export PATH=/Users/goldenquill/.npm-global/bin:/opt/homebrew/opt/node/bin:$PATH

echo "=== UPDATE judge ALIAS: qwen -> gemini-2.5-pro ==="
openclaw models aliases remove judge 2>&1 | tail -1 || echo "(alias remove silent)"
openclaw models aliases add judge google/gemini-2.5-pro 2>&1 | tail -1

echo ""
echo "=== VERIFY ==="
openclaw config validate --json 2>&1 | head -3
echo "--- Allowlist ---"
openclaw config get agents.defaults.models --json 2>&1 | python3 -c "import json,sys; d=json.load(sys.stdin); [print(k) for k in d.keys()]"
echo "--- Aliases ---"
openclaw models aliases list --plain 2>&1
echo "--- Plugins ---"
cat ~/.openclaw/openclaw.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(json.dumps(d.get('plugins', {}), indent=2))"

echo ""
echo "=== GEMINI JUDGE SMOKE TEST (with Judge prompt template header) ==="
openclaw infer model run --gateway --model google/gemini-2.5-pro --prompt 'You are Tilth Judge. HARD CONSTRAINT: Output only these three characters: JUD' 2>&1 | head -10
