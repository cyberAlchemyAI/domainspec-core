#!/bin/bash
# Usage: eval_one_seat.sh <seat_name> <model> <old_file> <new_file> <out_file>
set -euo pipefail
export PATH=/opt/homebrew/bin:/usr/local/bin:$PATH

SEAT="$1"
MODEL="$2"
OLD_FILE="$3"
NEW_FILE="$4"
OUT_FILE="$5"

TMPFILE=$(mktemp /tmp/tilth_eval_XXXXXX.txt)
trap 'rm -f "$TMPFILE"' EXIT

# Build prompt in temp file to avoid shell escaping issues with file contents
cat > "$TMPFILE" << 'HEADER'
You are reviewing a proposed replacement for a council seat prompt in the Tilth grant-writing AI pipeline. The OLD prompt has been used to win 3 competitive grants in 2026. The NEW prompt is a proposed upgrade informed by an adversarial board review (5 cross-perspective reviewers).

Evaluate with brutal honesty. This is YOUR seat — you know the work.

Report in this exact structure (no other sections):

## IMPROVEMENTS (what NEW does better for grant outcomes)
## REGRESSIONS (what OLD did better that NEW lost or weakened)
## MISSING (gaps in both versions)
## TENSIONS (tradeoffs where reasonable people would disagree)
## VERDICT: UPGRADE / DOWNGRADE / MIXED — one sentence
## TOP 3 CHANGES before deploying NEW as replacement

Under 500 words. Cite specific sections and content, not vibes.
HEADER

printf '\n--- OLD %s ---\n' "$SEAT" >> "$TMPFILE"
cat "$OLD_FILE" >> "$TMPFILE"
printf '\n--- NEW %s ---\n' "$SEAT" >> "$TMPFILE"
cat "$NEW_FILE" >> "$TMPFILE"

# Read prompt from file — avoids all shell escaping issues
PROMPT_TEXT=$(cat "$TMPFILE")

RESULT=$(npx openclaw infer model run --gateway --model "$MODEL" --prompt "$PROMPT_TEXT" --json 2>&1)

# Extract text from JSON
TEXT=$(printf '%s' "$RESULT" | python3 -c "
import sys, json
try:
    d = json.load(sys.stdin)
    if d.get('ok'):
        print(d['outputs'][0]['text'])
    else:
        print('ERROR: ' + json.dumps(d))
except Exception as e:
    print('PARSE_ERROR: ' + str(e))
" 2>/dev/null || printf '%s' "$RESULT")

printf '# %s Self-Evaluation — %s\n\n**Model:** %s\n**Old:** %s\n**New:** %s\n\n---\n\n%s\n' \
  "$SEAT" "$(date +%Y-%m-%d)" "$MODEL" "$OLD_FILE" "$NEW_FILE" "$TEXT" > "$OUT_FILE"

echo "done:${SEAT}"
