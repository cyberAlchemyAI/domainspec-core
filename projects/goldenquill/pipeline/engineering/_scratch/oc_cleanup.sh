#!/bin/bash
set -e
export PATH=/Users/goldenquill/.npm-global/bin:/opt/homebrew/opt/node/bin:$PATH

CONFIG="$HOME/.openclaw/openclaw.json"
TS=$(date -u +%Y%m%dT%H%M%SZ)
SAFETY_BAK="$HOME/.openclaw/openclaw.json.safety-bak-$TS"

echo "=== SAFETY BACKUP (pre-cleanup) ==="
cp "$CONFIG" "$SAFETY_BAK" && echo "SAFETY_BAK: $SAFETY_BAK"
ls -la "$SAFETY_BAK"

echo ""
echo "=== PYTHON PATCH: remove polluted keys ==="
python3 <<'PYEOF'
import json, pathlib
p = pathlib.Path.home() / ".openclaw" / "openclaw.json"
data = json.loads(p.read_text())

allowlist = data["agents"]["defaults"]["models"]
polluted = [k for k in list(allowlist.keys()) if k.startswith('"') and k.endswith('"')]
print("Polluted keys found:", polluted)
for k in polluted:
    del allowlist[k]

print("Keys after cleanup:", list(allowlist.keys()))
p.write_text(json.dumps(data, indent=2))
print("WROTE:", p)
PYEOF

echo ""
echo "=== VALIDATE ==="
openclaw config validate --json 2>&1 | head -3

echo ""
echo "=== FINAL ALLOWLIST ==="
openclaw config get agents.defaults.models --json 2>&1

echo ""
echo "=== ALIASES (should be preserved) ==="
openclaw models aliases list --plain 2>&1
