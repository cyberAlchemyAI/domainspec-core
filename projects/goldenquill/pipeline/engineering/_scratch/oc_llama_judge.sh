#!/bin/bash
set -e
export PATH=/Users/goldenquill/.npm-global/bin:/opt/homebrew/opt/node/bin:$PATH

echo "=== PYTHON CLEANUP: remove kimi 404 entries from allowlist ==="
python3 <<'PYEOF'
import json, pathlib
p = pathlib.Path.home() / ".openclaw" / "openclaw.json"
data = json.loads(p.read_text())
allowlist = data["agents"]["defaults"]["models"]
for key in ["groq/moonshotai/kimi-k2-instruct", "groq/moonshotai/kimi-k2-instruct-0905"]:
    if key in allowlist:
        del allowlist[key]
        print("Removed:", key)
print("Final keys:", list(allowlist.keys()))
p.write_text(json.dumps(data, indent=2))
PYEOF

echo ""
echo "=== UPDATE judge ALIAS: kimi -> llama ==="
openclaw models aliases remove judge 2>&1 | tail -1 || echo "(alias remove silent)"
openclaw models aliases add judge groq/llama-3.3-70b-versatile 2>&1 | tail -1

echo ""
echo "=== VERIFY ==="
openclaw config validate --json 2>&1 | head -3
echo "--- Aliases ---"
openclaw models aliases list --plain 2>&1

echo ""
echo "=== TEST JUDGE ON LLAMA with literal-instruction prompt ==="
openclaw infer model run --gateway --model groq/llama-3.3-70b-versatile --prompt 'You are a test endpoint. Output only: OK' 2>&1 | head -10

echo ""
echo "=== FULL 3-SEAT SMOKE TEST ==="
echo "--- EDITOR (Llama) ---"
openclaw infer model run --gateway --model groq/llama-3.3-70b-versatile --prompt 'You are a test endpoint. Output only: READY_EDITOR' 2>&1 | head -8
echo ""
echo "--- JUDGE (now Llama) ---"
openclaw infer model run --gateway --model groq/llama-3.3-70b-versatile --prompt 'You are a test endpoint. Output only: READY_JUDGE' 2>&1 | head -8
echo ""
echo "--- RED TEAM (GPT-OSS) ---"
openclaw infer model run --gateway --model groq/openai/gpt-oss-120b --prompt 'You are a test endpoint. Output only: READY_RED_TEAM' 2>&1 | head -8
