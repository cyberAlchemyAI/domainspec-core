#!/bin/bash
# Probe Groq API directly for available models + test candidates via OpenClaw
set -e
export PATH=/Users/goldenquill/.npm-global/bin:/opt/homebrew/opt/node/bin:$PATH

echo "=== GROQ API DIRECT: list actual accessible models ==="
source ~/.openclaw/.env
curl -s -H "Authorization: Bearer $GROQ_API_KEY" https://api.groq.com/openai/v1/models 2>&1 \
  | python3 -c "import json,sys; d=json.load(sys.stdin); [print(m.get('id','?'), '|', m.get('owned_by','?')) for m in sorted(d.get('data', []), key=lambda x: x.get('id',''))]" 2>&1 | head -50

echo ""
echo "=== ADD GEMMA + KEEP COMPOUND IN ALLOWLIST ==="
python3 <<'PYEOF'
import json, pathlib
p = pathlib.Path.home() / ".openclaw" / "openclaw.json"
data = json.loads(p.read_text())
allowlist = data["agents"]["defaults"]["models"]
for m in ["groq/gemma2-9b-it", "groq/compound-mini"]:
    if m not in allowlist:
        allowlist[m] = {}
        print("Added:", m)
p.write_text(json.dumps(data, indent=2))
PYEOF

echo ""
echo "=== TEST GEMMA ==="
openclaw infer model run --gateway --model groq/gemma2-9b-it --prompt 'You are a test endpoint. Output only: OK' 2>&1 | head -10

echo ""
echo "=== TEST COMPOUND ==="
openclaw infer model run --gateway --model groq/compound --prompt 'You are a test endpoint. Output only: OK' 2>&1 | head -10

echo ""
echo "=== TEST COMPOUND-MINI ==="
openclaw infer model run --gateway --model groq/compound-mini --prompt 'You are a test endpoint. Output only: OK' 2>&1 | head -10
