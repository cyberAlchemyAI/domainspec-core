#!/bin/bash
set -e
export PATH=/Users/goldenquill/.npm-global/bin:/opt/homebrew/opt/node/bin:$PATH

echo "=== TEST: kimi-k2-instruct (no -0905 suffix) ==="
openclaw infer model run --gateway --model groq/moonshotai/kimi-k2-instruct --prompt 'You are a test endpoint. Output only: OK' 2>&1 | head -10

echo ""
echo "=== PYTHON CLEANUP + ADD KIMI CLEAN ==="
python3 <<'PYEOF'
import json, pathlib
p = pathlib.Path.home() / ".openclaw" / "openclaw.json"
data = json.loads(p.read_text())

allowlist = data["agents"]["defaults"]["models"]
# Remove polluted quote-wrapped keys
polluted = [k for k in list(allowlist.keys()) if k.startswith('"') and k.endswith('"')]
for k in polluted:
    del allowlist[k]
    print("Removed polluted:", k)

# Remove the -0905 version if present (404s from Groq)
if "groq/moonshotai/kimi-k2-instruct-0905" in allowlist:
    del allowlist["groq/moonshotai/kimi-k2-instruct-0905"]
    print("Removed 404 model: groq/moonshotai/kimi-k2-instruct-0905")

# Add base kimi-k2-instruct cleanly
if "groq/moonshotai/kimi-k2-instruct" not in allowlist:
    allowlist["groq/moonshotai/kimi-k2-instruct"] = {}
    print("Added: groq/moonshotai/kimi-k2-instruct")

print("Final keys:", list(allowlist.keys()))
p.write_text(json.dumps(data, indent=2))
PYEOF

echo ""
echo "=== UPDATE judge ALIAS TO BASE KIMI ==="
openclaw models aliases remove judge 2>&1 | tail -1 || echo "(removal silent)"
openclaw models aliases add judge groq/moonshotai/kimi-k2-instruct 2>&1 | tail -1

echo ""
echo "=== VERIFY ==="
openclaw config validate --json 2>&1 | head -3
echo "--- Aliases ---"
openclaw models aliases list --plain 2>&1

echo ""
echo "=== TEST KIMI via ALIAS + via FULL ID ==="
echo "--- Full id ---"
openclaw infer model run --gateway --model groq/moonshotai/kimi-k2-instruct --prompt 'Output only: OK' 2>&1 | head -10
echo ""
echo "--- Alias form ---"
openclaw infer model run --gateway --model judge --prompt 'Output only: OK' 2>&1 | head -10
