#!/bin/bash
set -e
export PATH=/Users/goldenquill/.npm-global/bin:/opt/homebrew/opt/node/bin:$PATH

echo "=== CLEAN ALLOWLIST: remove experimental test models ==="
python3 <<'PYEOF'
import json, pathlib
p = pathlib.Path.home() / ".openclaw" / "openclaw.json"
data = json.loads(p.read_text())
allowlist = data["agents"]["defaults"]["models"]

# Keep only the 4 canonical seat models
canonical = {
    "anthropic/claude-sonnet-4-6",
    "groq/llama-3.3-70b-versatile",
    "groq/qwen/qwen3-32b",
    "groq/openai/gpt-oss-120b",
}
for k in list(allowlist.keys()):
    if k not in canonical:
        del allowlist[k]
        print("Removed:", k)

# Make sure all 4 canonical are present
for k in canonical:
    if k not in allowlist:
        allowlist[k] = {}
        print("Added (canonical):", k)

print("Final keys:", list(allowlist.keys()))
p.write_text(json.dumps(data, indent=2))
PYEOF

echo ""
echo "=== RESET judge ALIAS: llama/deepseek -> qwen ==="
openclaw models aliases remove judge 2>&1 | tail -1 || echo "(remove silent)"
openclaw models aliases add judge groq/qwen/qwen3-32b 2>&1 | tail -1

echo ""
echo "=== VERIFY ==="
openclaw config validate --json 2>&1 | head -3
echo "--- Allowlist ---"
openclaw config get agents.defaults.models --json 2>&1 | python3 -c "import json,sys; d=json.load(sys.stdin); [print(k) for k in d.keys()]"
echo "--- Aliases ---"
openclaw models aliases list --plain 2>&1

echo ""
echo "=== TEST QWEN JUDGE WITH HARDENED FRAMING ==="
openclaw infer model run --gateway --model groq/qwen/qwen3-32b --prompt 'You are a test endpoint. HARD CONSTRAINT: Output only these two characters with no elaboration, commentary, or context: OK' 2>&1 | head -10
