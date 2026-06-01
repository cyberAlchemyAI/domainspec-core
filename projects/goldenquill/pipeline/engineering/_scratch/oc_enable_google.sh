#!/bin/bash
set -e
export PATH=/Users/goldenquill/.npm-global/bin:/opt/homebrew/opt/node/bin:$PATH

echo "=== SAFETY BACKUP ==="
TS=$(date -u +%Y%m%dT%H%M%SZ)
BAK="$HOME/.openclaw/openclaw.json.safety-bak-google-$TS"
cp ~/.openclaw/openclaw.json "$BAK" && echo "SAFETY_BAK: $BAK"

echo ""
echo "=== ENABLE GOOGLE PLUGIN ==="
openclaw plugins enable google 2>&1 | tail -5

echo ""
echo "=== ALSO ENABLE OPENAI (Josh has key + is paying) ==="
openclaw plugins enable openai 2>&1 | tail -5

echo ""
echo "=== VALIDATE + STATUS ==="
openclaw config validate --json 2>&1 | head -3
echo "--- Plugin entries now ---"
cat ~/.openclaw/openclaw.json | python3 -c "import json,sys; d=json.load(sys.stdin); print(json.dumps(d.get('plugins', {}), indent=2))"

echo ""
echo "=== GOOGLE/OPENAI CATALOG MODELS (post-enable) ==="
openclaw infer model list --json 2>&1 | python3 -c "
import json, sys
data = json.load(sys.stdin) if sys.stdin.readable() else []
" 2>&1 | head -3 || echo "(list parse inline below)"

echo "--- Google models ---"
openclaw infer model list --json 2>&1 | grep -E '\"provider\": \"google' -B 2 | head -30 || echo "(no google matches)"
echo ""
echo "--- OpenAI models (non-oss, direct) ---"
openclaw infer model list --json 2>&1 | grep -E '\"provider\": \"openai\"' -B 2 | head -30 || echo "(no direct openai)"
