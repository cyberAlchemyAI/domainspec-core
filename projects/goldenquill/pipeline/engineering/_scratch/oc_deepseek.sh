#!/bin/bash
set -e
export PATH=/Users/goldenquill/.npm-global/bin:/opt/homebrew/opt/node/bin:$PATH

echo "=== ADD DEEPSEEK TO ALLOWLIST (python-patch, NOT config set) ==="
python3 <<'PYEOF'
import json, pathlib
p = pathlib.Path.home() / ".openclaw" / "openclaw.json"
data = json.loads(p.read_text())
allowlist = data["agents"]["defaults"]["models"]
if "groq/deepseek-r1-distill-llama-70b" not in allowlist:
    allowlist["groq/deepseek-r1-distill-llama-70b"] = {}
    print("Added: groq/deepseek-r1-distill-llama-70b")
# Also try groq/compound as backup
if "groq/compound" not in allowlist:
    allowlist["groq/compound"] = {}
    print("Added: groq/compound")
p.write_text(json.dumps(data, indent=2))
print("Keys:", list(allowlist.keys()))
PYEOF

echo ""
echo "=== UPDATE judge ALIAS: llama -> deepseek ==="
openclaw models aliases remove judge 2>&1 | tail -1 || echo "(remove silent)"
openclaw models aliases add judge groq/deepseek-r1-distill-llama-70b 2>&1 | tail -1

echo ""
echo "=== TEST DEEPSEEK ==="
openclaw infer model run --gateway --model groq/deepseek-r1-distill-llama-70b --prompt 'You are a test endpoint. Output only: OK' 2>&1 | head -15
