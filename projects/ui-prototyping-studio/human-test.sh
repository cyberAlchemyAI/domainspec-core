#!/usr/bin/env bash
set -Eeuo pipefail

PROJECT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$PROJECT_DIR/backend"
TSX="$BACKEND_DIR/node_modules/.bin/tsx"
CLI="$BACKEND_DIR/src/cli/studio.ts"
FIXTURES="$PROJECT_DIR/human-test/fixtures"
MODE="interactive"
NO_OPEN=0
PREVIEW_PID=""

usage() {
  cat <<'EOF'
Usage:
  ./human-test.sh
  ./human-test.sh --no-open
  ./human-test.sh --self-check

Interactive mode prepares an isolated Studio session and guides a human
through annotation, approval, staged review, Accept, Revert, and handoff.

--no-open     Print the preview URL without trying to open a browser.
--self-check  Exercise the script and CLI seams non-interactively. This is
              harness validation, not human-study evidence.
EOF
}

for arg in "$@"; do
  case "$arg" in
    --no-open) NO_OPEN=1 ;;
    --self-check) MODE="self-check"; NO_OPEN=1 ;;
    -h|--help) usage; exit 0 ;;
    *)
      printf 'Unknown option: %s\n\n' "$arg" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [[ ! -x "$TSX" ]]; then
  printf 'Missing local tsx runtime: %s\n' "$TSX" >&2
  printf 'Install dependencies first: cd %s && pnpm install\n' "$BACKEND_DIR" >&2
  exit 1
fi

for fixture in a.html b.html c.html candidate.html; do
  if [[ ! -f "$FIXTURES/$fixture" ]]; then
    printf 'Missing human-test fixture: %s\n' "$FIXTURES/$fixture" >&2
    exit 1
  fi
done

if [[ "$MODE" == "interactive" && ! -t 0 ]]; then
  printf 'Interactive human testing requires a terminal. Use --self-check in automation.\n' >&2
  exit 1
fi

RUN_DIR="$(mktemp -d "${TMPDIR:-/tmp}/ups-human-test.XXXXXX")"
VARIANT_DIR="$RUN_DIR/variants"
mkdir -p "$VARIANT_DIR"
cp "$FIXTURES/a.html" "$VARIANT_DIR/a.html"
cp "$FIXTURES/b.html" "$VARIANT_DIR/b.html"
cp "$FIXTURES/c.html" "$VARIANT_DIR/c.html"

export STUDIO_DATA="$RUN_DIR/studio.json"
export STUDIO_DOCS_ROOT="$PROJECT_DIR"
export STUDIO_ACTOR="human-test-user"

cleanup() {
  if [[ -n "$PREVIEW_PID" ]] && kill -0 "$PREVIEW_PID" 2>/dev/null; then
    kill "$PREVIEW_PID" 2>/dev/null || true
    wait "$PREVIEW_PID" 2>/dev/null || true
  fi
}
trap cleanup EXIT INT TERM

studio() {
  (
    cd "$BACKEND_DIR"
    "$TSX" "$CLI" "$@"
  )
}

json_field() {
  local file="$1"
  local path="$2"
  node -e '
    const fs = require("node:fs");
    let value = JSON.parse(fs.readFileSync(process.argv[1], "utf8"));
    for (const key of process.argv[2].split(".")) value = value[key];
    if (value === undefined || value === null) process.exit(3);
    process.stdout.write(String(value));
  ' "$file" "$path"
}

json_length() {
  node -e '
    const fs = require("node:fs");
    const value = JSON.parse(fs.readFileSync(process.argv[1], "utf8"));
    if (!Array.isArray(value)) process.exit(3);
    process.stdout.write(String(value.length));
  ' "$1"
}

capture() {
  local file="$1"
  shift
  studio "$@" >"$file"
}

pause() {
  printf '\n%s\n' "$1"
  read -r -p "Press Enter when done... " _
}

confirm_yes() {
  local answer
  read -r -p "$1 [y/N] " answer
  [[ "$answer" == "y" || "$answer" == "Y" ]]
}

open_preview() {
  if [[ "$NO_OPEN" -eq 1 ]]; then
    return
  fi
  if command -v xdg-open >/dev/null 2>&1; then
    xdg-open "$PREVIEW_URL" >/dev/null 2>&1 &
  elif command -v open >/dev/null 2>&1; then
    open "$PREVIEW_URL" >/dev/null 2>&1 &
  fi
}

assert_state() {
  local expected="$1"
  local file="$RUN_DIR/state-check.json"
  studio state "$SID" >"$file"
  local actual
  actual="$(json_field "$file" "session.state")"
  if [[ "$actual" != "$expected" ]]; then
    printf 'Expected state %s, got %s. Full state:\n' "$expected" "$actual" >&2
    cat "$file" >&2
    return 1
  fi
  printf 'Verified state: %s\n' "$actual"
}

printf '\nUI Prototyping Studio — guided human test\n'
printf 'Mode: %s\n' "$MODE"
printf 'Isolated run directory: %s\n' "$RUN_DIR"
printf 'Nothing in this run authorizes publication or release.\n\n'

capture "$RUN_DIR/01-session.json" session open --variants 3
SID="$(json_field "$RUN_DIR/01-session.json" "sessionId")"
capture "$RUN_DIR/02-prompt.json" prompt submit "$SID" \
  "A calm, trustworthy signup card with an obvious primary action"
capture "$RUN_DIR/03-variants.json" variants register "$SID" --from "$VARIANT_DIR"
capture "$RUN_DIR/04-baseline-select.json" baseline select "$SID" A
capture "$RUN_DIR/05-baseline-commit.json" baseline commit "$SID"
printf 'Prepared session %s with variants A/B/C and committed baseline A.\n' "$SID"

PREVIEW_LOG="$RUN_DIR/preview.log"
studio preview "$SID" >"$PREVIEW_LOG" 2>&1 &
PREVIEW_PID=$!

for _ in $(seq 1 200); do
  if ! kill -0 "$PREVIEW_PID" 2>/dev/null; then
    printf 'Preview exited before readiness:\n' >&2
    cat "$PREVIEW_LOG" >&2
    exit 1
  fi
  if grep -q '"preview"' "$PREVIEW_LOG"; then
    break
  fi
  sleep 0.1
done

if ! grep -q '"preview"' "$PREVIEW_LOG"; then
  printf 'Preview did not become ready. Log:\n' >&2
  cat "$PREVIEW_LOG" >&2
  exit 1
fi

PREVIEW_URL="$(json_field "$PREVIEW_LOG" "preview")"
printf '\nPreview: %s\n' "$PREVIEW_URL"
open_preview

node -e '
  fetch(process.argv[1]).then((response) => {
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    console.log("Preview readiness: pass");
  }).catch((error) => {
    console.error(error);
    process.exit(1);
  });
' "$PREVIEW_URL"

if [[ "$MODE" == "self-check" ]]; then
  studio comment add "$SID" \
    --selector "[data-od-id=cta.primary]" \
    --label "Start free trial button" \
    --od-id "cta.primary" \
    --severity medium \
    --intent reword \
    --note "Change the label to Continue securely and use green emphasis" \
    >"$RUN_DIR/06-comment.json"
else
  printf '\nSTEP 1 — Orient and annotate\n'
  printf '1. Open the preview URL if it did not open automatically.\n'
  printf '2. Confirm variant A is the current head and B/C are labeled history.\n'
  printf '3. In Annotate, click the “Start free trial” button.\n'
  printf '4. Confirm the selected target is cta.primary.\n'
  printf '5. Use severity “medium”, intent “reword”, and note:\n'
  printf '   Change the label to Continue securely and use green emphasis\n'
  printf '6. Add the comment and look for “captured ✓”.\n'

  comment_count=0
  for attempt in 1 2 3; do
    pause "Complete the browser annotation (attempt $attempt of 3)."
    studio pending "$SID" >"$RUN_DIR/06-pending.json"
    comment_count="$(json_length "$RUN_DIR/06-pending.json")"
    if [[ "$comment_count" -ge 1 ]]; then
      printf 'Verified pending comments: %s\n' "$comment_count"
      break
    fi
    printf 'No pending comment is visible yet. The page may still need submission.\n'
  done
  if [[ "$comment_count" -lt 1 ]]; then
    printf 'Human-test checkpoint failed: no browser comment was captured.\n' >&2
    exit 1
  fi
fi

capture "$RUN_DIR/07-synthesis.json" synthesize "$SID"
BATCH_ID="$(json_field "$RUN_DIR/07-synthesis.json" "batch.batchId")"
node -e '
  const fs = require("node:fs");
  const { batch } = JSON.parse(fs.readFileSync(process.argv[1], "utf8"));
  console.log(`Draft batch: ${batch.batchId}`);
  console.log(`Checksum: ${batch.checksum}`);
  for (const task of batch.tasks) {
    console.log(`- ${task.taskId} · ${task.odId ?? task.target} · ${task.acceptanceText}`);
  }
' "$RUN_DIR/07-synthesis.json"

if [[ "$MODE" == "interactive" ]]; then
  printf '\nSTEP 2 — Review approval intent\n'
  printf 'The synthesized batch is printed above. Its target should be cta.primary.\n'
  if ! confirm_yes "Approve this exact batch?"; then
    printf 'Stopped before approval. Run artifacts remain at %s\n' "$RUN_DIR"
    exit 0
  fi
fi

capture "$RUN_DIR/08-approval.json" batch approve "$SID" "$BATCH_ID"
capture "$RUN_DIR/09-apply.json" apply "$SID" "$BATCH_ID" \
  --candidate-from "$FIXTURES/candidate.html"

VERDICT="$(json_field "$RUN_DIR/09-apply.json" "verdict")"
if [[ "$VERDICT" != "NOT_REJECT" ]]; then
  printf 'Candidate was not admitted. Verdict: %s\n' "$VERDICT" >&2
  exit 1
fi
node -e '
  const fs = require("node:fs");
  const result = JSON.parse(fs.readFileSync(process.argv[1], "utf8"));
  const diff = result.diff;
  console.log(`Candidate admitted: ${result.candidateHtmlHash}`);
  console.log(`Diff: +${diff.added} ~${diff.changed} -${diff.removed}; style ${diff.style.changed ? "changed" : "unchanged"}; visible ${diff.visibleChangeCount}`);
' "$RUN_DIR/09-apply.json"
assert_state "RevisionApplied"

if [[ "$MODE" == "self-check" ]]; then
  studio accept "$SID" >"$RUN_DIR/10-accept.json"
else
  printf '\nSTEP 3 — Inspect and Accept in the browser\n'
  printf 'The preview should reload to a staged before/after comparison.\n'
  printf '1. Confirm the candidate is not yet the current head.\n'
  printf '2. Confirm the button text/color changed and the diff reports style evidence.\n'
  printf '3. Narrow the browser or panel to about 390px and check that cards stack\n'
  printf '   without horizontal page overflow.\n'
  printf '4. Confirm Accept is disabled before acknowledgment.\n'
  printf '5. Read the candidate identity, target state, and diff recap.\n'
  printf '6. Check the acknowledgment, then click “Accept this change”.\n'
  pause "Accept the staged change in the browser."
fi

assert_state "RevisionRecorded"
studio revisions "$SID" >"$RUN_DIR/11-revisions-before-revert.json"
BEFORE_REVERT="$(json_length "$RUN_DIR/11-revisions-before-revert.json")"

if [[ "$MODE" == "self-check" ]]; then
  studio revert "$SID" >"$RUN_DIR/12-revert.json"
else
  printf '\nSTEP 4 — Exercise reversible history\n'
  printf 'The preview should now show “Revert current head”.\n'
  printf '1. Confirm Revert is disabled before acknowledgment.\n'
  printf '2. Read the revision identity, target state, and diff recap.\n'
  printf '3. Check the acknowledgment, then click “Revert last change”.\n'
  pause "Revert the accepted change in the browser."
fi

assert_state "RevisionRecorded"
capture "$RUN_DIR/13-revisions-after-revert.json" revisions "$SID"
AFTER_REVERT="$(json_length "$RUN_DIR/13-revisions-after-revert.json")"
if [[ "$AFTER_REVERT" -ne $((BEFORE_REVERT + 1)) ]]; then
  printf 'Expected Revert to append one revision (%s -> %s).\n' \
    "$BEFORE_REVERT" "$AFTER_REVERT" >&2
  exit 1
fi
printf 'Verified append-only Revert: revisions %s -> %s\n' \
  "$BEFORE_REVERT" "$AFTER_REVERT"

set +e
studio handoff export "$SID" >"$RUN_DIR/14-unconfirmed-export.json"
UNCONFIRMED_CODE=$?
set -e
cat "$RUN_DIR/14-unconfirmed-export.json"
if [[ "$UNCONFIRMED_CODE" -ne 3 ]]; then
  printf 'Expected unconfirmed export to exit 3, got %s.\n' \
    "$UNCONFIRMED_CODE" >&2
  exit 1
fi
printf 'Verified: unconfirmed export was refused.\n'

EXPORT_RESULT="not-run"
if [[ "$MODE" == "self-check" ]]; then
  studio handoff export "$SID" --confirm >"$RUN_DIR/15-confirmed-export.json"
  EXPORT_RESULT="confirmed"
else
  printf '\nSTEP 5 — Confirm the terminal handoff edge\n'
  printf 'The refusal above is expected. Export confirmation is separate from\n'
  printf 'evidenceComplete, integrationReady, implementationReady, and release.\n'
  read -r -p "Type EXPORT to run the confirmed local handoff (anything else skips): " answer
  if [[ "$answer" == "EXPORT" ]]; then
    capture "$RUN_DIR/15-confirmed-export.json" handoff export "$SID" --confirm
    EXPORT_RESULT="confirmed"
  else
    printf 'Confirmed export skipped by tester.\n'
    EXPORT_RESULT="skipped"
  fi
fi

if [[ "$EXPORT_RESULT" == "confirmed" ]]; then
  node -e '
    const fs = require("node:fs");
    const result = JSON.parse(fs.readFileSync(process.argv[1], "utf8"));
    const bundle = result.bundle ?? result;
    console.log("Confirmed handoff predicates:");
    console.log(`- missingRefs: ${JSON.stringify(bundle.missingRefs)}`);
    console.log(`- exportConfirmed: ${bundle.exportConfirmed}`);
    console.log(`- evidenceComplete: ${bundle.evidenceComplete}`);
    console.log(`- integrationReady: ${bundle.integrationReady}`);
    console.log(`- implementationReady: ${bundle.implementationReady}`);
    console.log("- releaseAuthorized: not a Studio handoff field");
  ' "$RUN_DIR/15-confirmed-export.json"
fi

if [[ "$MODE" == "interactive" ]]; then
  printf '\nSTEP 6 — Record your observations\n'
  read -r -p "Did current head versus history stay clear? " q1
  read -r -p "Was staged versus recorded clear? " q2
  read -r -p "Did the acknowledgment match the action? " q3
  read -r -p "Did any unintended revision appear? " q4
  read -r -p "Was the 390px comparison inspectable without overflow? " q5
  read -r -p "Biggest point of confusion: " q6
  read -r -p "One improvement you would make: " q7
  {
    printf '# UI Prototyping Studio — Human Test Observation\n\n'
    printf -- '- Session: `%s`\n' "$SID"
    printf -- '- Run directory: `%s`\n' "$RUN_DIR"
    printf -- '- Export: `%s`\n' "$EXPORT_RESULT"
    printf -- '- Current head versus history: %s\n' "$q1"
    printf -- '- Staged versus recorded: %s\n' "$q2"
    printf -- '- Acknowledgment matched action: %s\n' "$q3"
    printf -- '- Unintended revision: %s\n' "$q4"
    printf -- '- 390px comparison: %s\n' "$q5"
    printf -- '- Biggest confusion: %s\n' "$q6"
    printf -- '- Suggested improvement: %s\n' "$q7"
    printf '\nThis is one tester observation, not a human-study or release verdict.\n'
  } >"$RUN_DIR/feedback.md"
else
  printf '# Self-check only; not human evidence.\n' >"$RUN_DIR/feedback.md"
fi

printf '\nHuman-test harness result: PASS\n'
printf 'Session: %s\n' "$SID"
printf 'Preview: %s\n' "$PREVIEW_URL"
printf 'Run artifacts: %s\n' "$RUN_DIR"
printf 'Feedback: %s\n' "$RUN_DIR/feedback.md"

if [[ "$MODE" == "interactive" ]]; then
  pause "Review anything else in the preview. The local server stops after this."
fi
