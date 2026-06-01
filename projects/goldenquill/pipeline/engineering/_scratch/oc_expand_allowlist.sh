#!/bin/bash
set -e
export PATH=/Users/goldenquill/.npm-global/bin:/opt/homebrew/opt/node/bin:$PATH

echo "=== SAFETY BACKUP ==="
TS=$(date -u +%Y%m%dT%H%M%SZ)
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.safety-bak-expand-$TS && echo "BAK: ~/.openclaw/openclaw.json.safety-bak-expand-$TS"

echo ""
echo "=== PYTHON PATCH: add 3 escalation/variant models ==="
python3 <<'PYEOF'
import json, pathlib
p = pathlib.Path.home() / ".openclaw" / "openclaw.json"
data = json.loads(p.read_text())
allowlist = data["agents"]["defaults"]["models"]
for m in [
    "anthropic/claude-opus-4-6",      # Scribe escalation
    "openai/gpt-5.1",                  # Red Team escalation candidate
    "google/gemini-2.5-flash",         # Scout escalation candidate
]:
    if m not in allowlist:
        allowlist[m] = {}
        print("Added:", m)
print("Final keys:", list(allowlist.keys()))
p.write_text(json.dumps(data, indent=2))
PYEOF

echo ""
echo "=== VALIDATE ==="
openclaw config validate --json 2>&1 | head -3

echo ""
echo "=== SMOKE TEST 1: OPUS 4.6 ==="
openclaw infer model run --gateway --model anthropic/claude-opus-4-6 --prompt 'HARD CONSTRAINT: Output only: OPUS_OK' 2>&1 | head -10

echo ""
echo "=== SMOKE TEST 2: GPT-5.1 ==="
openclaw infer model run --gateway --model openai/gpt-5.1 --prompt 'HARD CONSTRAINT: Output only: GPT51_OK' 2>&1 | head -10

echo ""
echo "=== SMOKE TEST 3: GEMINI 2.5 FLASH ==="
openclaw infer model run --gateway --model google/gemini-2.5-flash --prompt 'HARD CONSTRAINT: Output only: FLASH_OK' 2>&1 | head -10
