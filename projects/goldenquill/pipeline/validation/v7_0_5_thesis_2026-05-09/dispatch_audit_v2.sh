#!/bin/bash
# Dispatch v7.0.5 Audit #2 — cross-family L-005 verification cycle
# Usage: bash pipeline/validation/v7_0_5_thesis_2026-05-09/dispatch_audit_v2.sh [editor|judge|red_team|all]
set -e
export PATH="$HOME/.npm-global/bin:/opt/homebrew/opt/node/bin:/opt/homebrew/bin:/usr/local/bin:$PATH"

BASE="$HOME/Downloads/GoldenQuill"
DIR="$BASE/pipeline/validation/v7_0_5_thesis_2026-05-09"
AMENDMENT="$BASE/pipeline/architecture/v0.1/architecture_v7_0_5_amendment.md"
HEADER="$DIR/audit_prompt_v1_common_header.md"

build_prompt() {
  local seat="$1"
  cat "$HEADER"
  echo
  echo '=== v7.0.5 amendment text — Cycle 1 fixes APPLIED (BEGIN) ==='
  cat "$AMENDMENT"
  echo '=== v7.0.5 amendment text (END) ==='
  echo
  cat "$DIR/audit_prompt_v2_${seat}_task.md"
}

dispatch() {
  local seat="$1"
  local family="$2"
  local model="$3"
  local out="$DIR/audit_v2_${seat}.md"
  local raw="$DIR/audit_v2_${seat}.raw.json"

  echo "▶ Dispatching ${seat} via ${model} (family: ${family})..."
  local prompt
  prompt=$(build_prompt "$seat")

  openclaw infer model run --gateway --model "$model" --prompt "$prompt" --json > "$raw" 2>&1

  local ts="$(date -u +%FT%TZ)"
  RAW_PATH="$raw" SEAT="$seat" FAMILY="$family" MODEL="$model" TS="$ts" python3 - <<'PY' > "$out"
import json, os
raw_path = os.environ["RAW_PATH"]
seat = os.environ["SEAT"]; family = os.environ["FAMILY"]; model = os.environ["MODEL"]; ts = os.environ["TS"]
with open(raw_path) as f:
    raw = f.read()
try:
    data = json.loads(raw)
    if isinstance(data, dict):
        outs = data.get("outputs") or []
        text = (outs[0].get("text") if outs and isinstance(outs[0], dict) else "") or data.get("text") or data.get("content") or ""
        if not text:
            text = "[NO TEXT EXTRACTED]\n\n```\n" + json.dumps(data, indent=2) + "\n```"
    else:
        text = "[NON-DICT RESPONSE]\n\n```\n" + json.dumps(data, indent=2) + "\n```"
except Exception as e:
    text = f"[JSON parse failed: {e}]\n\n```\n{raw}\n```"
print(f"<!-- seat={seat} family={family} model={model} cycle=2 dispatched_at={ts} -->")
print()
print(text)
PY
  echo "✓ ${seat} → $out"
  wc -l "$out"
}

CMD="${1:-all}"
[ "$CMD" = "editor" ] || [ "$CMD" = "all" ] && dispatch editor meta groq/llama-3.3-70b-versatile
[ "$CMD" = "judge" ] || [ "$CMD" = "all" ] && dispatch judge google google/gemini-2.5-pro
[ "$CMD" = "red_team" ] || [ "$CMD" = "all" ] && dispatch red_team openai-oss groq/openai/gpt-oss-120b
echo "=== DISPATCH COMPLETE ==="
