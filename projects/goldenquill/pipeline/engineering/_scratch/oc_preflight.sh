#!/bin/bash
# OpenClaw cross-family remediation — pre-flight (read-only + backup)
export PATH=/Users/goldenquill/.npm-global/bin:/opt/homebrew/opt/node/bin:$PATH

TS=$(date -u +%Y%m%dT%H%M%SZ)
BAK="$HOME/.openclaw/openclaw.json.bak.pre-groq-allowlist-$TS"

echo "=== D.0 PRE-FLIGHT ==="

echo "--- Backup ---"
cp "$HOME/.openclaw/openclaw.json" "$BAK" && echo "BACKUP_OK: $BAK" || echo "BACKUP_FAIL"

echo "--- Health ---"
openclaw health 2>&1

echo "--- Current allowlist (keys only) ---"
openclaw config get agents.defaults.models --json 2>&1 | python3 -c "import json,sys; d=json.load(sys.stdin); print(list(d.keys()))" 2>&1

echo "--- Groq auth status ---"
OPENCLAW_AGENT_DIR="$HOME/.openclaw/agents/tilth/agent" openclaw infer model auth status 2>&1 | grep -A 4 '"provider": "groq"' || echo "(groq auth not shown in status)"
