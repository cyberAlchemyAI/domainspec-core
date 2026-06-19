#!/usr/bin/env bash
# TW1 — live-capture adapter for the operating-SKILL harness.
# Runs ONE studio CLI verb under a given actor, appends a transcript JSONL line, prints stdout.
#
# Usage:
#   capture-session.sh <transcript.jsonl> <actor> <verb...> [-- argjson '<json>']
#     <actor>      e.g. agent:claude-code | human:operator   (sets STUDIO_ACTOR)
#     <verb...>    the studio verb + args, e.g. "synthesize" "$SID"
#     argjson      optional JSON object recorded as the line's "args" (for M2/M3 fields);
#                  if omitted, "args" is {}.
#
# Records {actor, verb, args, narration:"", ok:<bool>}. ok reflects the CLI exit code
# (closes the first-test gap: a shape-compliant transcript must not mask a failed call).
# Requires STUDIO_DATA + the backend on PATH context (run from backend/ or set BACKEND_DIR).
set -uo pipefail

TR="${1:?usage: capture-session.sh <transcript> <actor> <verb...> [argjson <json>]}"; shift
ACTOR="${1:?actor required}"; shift
BACKEND_DIR="${BACKEND_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../../backend" && pwd)}"
TSX="$BACKEND_DIR/node_modules/.bin/tsx"

# split trailing "argjson <json>"
ARGS_JSON="{}"
VERB_ARGS=()
while [[ $# -gt 0 ]]; do
  if [[ "$1" == "argjson" ]]; then ARGS_JSON="${2:-{}}"; shift 2; continue; fi
  VERB_ARGS+=("$1"); shift
done

STUDIO_ACTOR="$ACTOR" "$TSX" "$BACKEND_DIR/src/cli/studio.ts" "${VERB_ARGS[@]}" >/tmp/cs.out 2>/tmp/cs.err
RC=$?
OK=$([[ $RC -eq 0 ]] && echo true || echo false)
VERB="${VERB_ARGS[0]:-}"; [[ "${VERB_ARGS[1]:-}" =~ ^(open|submit|generate|register|select|commit|add|approve|apply|export)$ ]] && VERB="${VERB_ARGS[0]} ${VERB_ARGS[1]}"

python3 -c "
import json,sys
print(json.dumps({'actor':sys.argv[1],'verb':sys.argv[2],'args':json.loads(sys.argv[3]),'narration':'','ok':sys.argv[4]=='true'}))
" "$ACTOR" "$VERB" "$ARGS_JSON" "$OK" >> "$TR"

cat /tmp/cs.out
[[ $RC -ne 0 ]] && cat /tmp/cs.err >&2
exit $RC
