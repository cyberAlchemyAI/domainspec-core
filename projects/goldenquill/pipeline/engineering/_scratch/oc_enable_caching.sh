#!/bin/bash
set -e
export PATH=/Users/goldenquill/.npm-global/bin:/opt/homebrew/opt/node/bin:$PATH

echo "=== SAFETY BACKUP ==="
TS=$(date -u +%Y%m%dT%H%M%SZ)
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.safety-bak-caching-$TS && echo "BAK: ~/.openclaw/openclaw.json.safety-bak-caching-$TS"

echo ""
echo "=== PYTHON PATCH: enable caching + add Opus 4.7 ==="
python3 <<'PYEOF'
import json, pathlib
p = pathlib.Path.home() / ".openclaw" / "openclaw.json"
data = json.loads(p.read_text())

allowlist = data["agents"]["defaults"]["models"]

# Add Opus 4.7 with long caching
if "anthropic/claude-opus-4-7" not in allowlist:
    allowlist["anthropic/claude-opus-4-7"] = {"params": {"cacheRetention": "long"}}
    print("Added: anthropic/claude-opus-4-7 (cacheRetention: long)")
else:
    allowlist["anthropic/claude-opus-4-7"].setdefault("params", {})["cacheRetention"] = "long"
    print("Updated: anthropic/claude-opus-4-7 cacheRetention: long")

# Enable long caching on Sonnet 4.6 (Scribe primary)
if "anthropic/claude-sonnet-4-6" in allowlist:
    entry = allowlist["anthropic/claude-sonnet-4-6"]
    if not isinstance(entry, dict):
        entry = {}
        allowlist["anthropic/claude-sonnet-4-6"] = entry
    entry.setdefault("params", {})["cacheRetention"] = "long"
    # Preserve alias if present
    if "alias" not in entry:
        entry["alias"] = "scribe"
    print("Updated: anthropic/claude-sonnet-4-6 cacheRetention: long (alias: scribe preserved)")

# Enable long caching on Opus 4.6 (Scribe escalation)
if "anthropic/claude-opus-4-6" in allowlist:
    entry = allowlist["anthropic/claude-opus-4-6"]
    if not isinstance(entry, dict):
        entry = {}
        allowlist["anthropic/claude-opus-4-6"] = entry
    entry.setdefault("params", {})["cacheRetention"] = "long"
    print("Updated: anthropic/claude-opus-4-6 cacheRetention: long")

print()
print("=== Final allowlist ===")
for k, v in allowlist.items():
    cache = (v.get("params", {}) if isinstance(v, dict) else {}).get("cacheRetention", "(default)")
    alias = v.get("alias") if isinstance(v, dict) else None
    print(f"  {k}  cache={cache}  alias={alias}")

p.write_text(json.dumps(data, indent=2))
print()
print("WROTE:", p)
PYEOF

echo ""
echo "=== VALIDATE ==="
openclaw config validate --json 2>&1 | head -3

echo ""
echo "=== GATEWAY RESTART (required for config reload) ==="
openclaw gateway restart 2>&1 | head -10

echo ""
echo "=== HEALTH CHECK ==="
sleep 3
openclaw health 2>&1 | head -5

echo ""
echo "=== TEST OPUS 4.7 (first call — should write cache) ==="
openclaw infer model run --gateway --model anthropic/claude-opus-4-7 --prompt 'HARD CONSTRAINT: Output only: OPUS47_OK' 2>&1 | head -15
