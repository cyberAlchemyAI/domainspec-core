#!/usr/bin/env bash
# test_cache_org_isolation.sh — Law-3 acceptance test for cache-key namespacing.
#
# Per handoff `pipeline/handoffs/caching_batch_build_handoff_2026-04-19.md` §D3:
# Two orgs issuing identical preamble bodies MUST NOT share cache tokens.
# Each cached system prompt is prefixed `ORG:<orgSlug>\nTRACE:<sessionId>\n`
# so the cache keys diverge at the first byte of the system block.
#
# Procedure:
#   1. Org A, preamble body X, long cache → expect cache_creation > 0 (write)
#   2. Org A, preamble body X, long cache → expect cache_read > 0 (hit)
#   3. Org B, preamble body X, long cache → expect cache_read == 0 (miss)
#
# Exit 0 on all three assertions pass; exit 1 otherwise.
#
# Requires: ANTHROPIC_API_KEY in env, jq, node, network access to Anthropic.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
BIN="$REPO_ROOT/tilth/bin/tilth-infer-cached.mjs"

if [[ ! -x "$BIN" ]]; then
  echo "FAIL: $BIN not executable" >&2
  exit 1
fi
if [[ -z "${ANTHROPIC_API_KEY:-}" ]]; then
  echo "SKIP: ANTHROPIC_API_KEY not set — live API test cannot run" >&2
  exit 2
fi

ORG_A="acme-test-a"
ORG_B="acme-test-b"
TRACE_ID="$(uuidgen 2>/dev/null || date +%s%N)"

# Preamble body (≥1024 tokens to be cache-eligible on Sonnet). Identical for
# both orgs — the ORG: prefix is what must force a cache-key divergence.
BODY="$(python3 -c 'print(("The applicant narrative describes a regenerative agriculture cooperative applying under the Specialty Crop Block Grant Program (SCBGP). Eligible commodities include mushrooms, leafy greens, herbs, and tree fruit. The cooperative structure aligns with USDA AMS priority criteria for increasing the competitiveness of specialty crops. " * 40).strip())')"

build_system() {
  local org_slug="$1"
  printf 'ORG:%s\nTRACE:%s\n%s' "$org_slug" "$TRACE_ID" "$BODY"
}

call() {
  local org_slug="$1"
  local label="$2"
  local sys
  sys="$(build_system "$org_slug")"
  local out
  out="$(node "$BIN" \
    --model anthropic/claude-sonnet-4-6 \
    --system "$sys" \
    --prompt "Acknowledge with the single word: OK." \
    --org "$org_slug" \
    --workflow cache-isolation-test \
    --max-tokens 16 \
    --cache-retention long)"
  echo "$out" | jq -c --arg l "$label" '{label:$l, cr:.ledger.cache_read_input_tokens, cw:.ledger.cache_creation_input_tokens, in:.ledger.input_tokens}'
  echo "$out"
}

assert_gt() {
  local name="$1" actual="$2" threshold="$3"
  if (( actual > threshold )); then
    echo "PASS: $name ($actual > $threshold)"
  else
    echo "FAIL: $name ($actual not > $threshold)" >&2
    return 1
  fi
}

assert_eq() {
  local name="$1" actual="$2" expected="$3"
  if [[ "$actual" == "$expected" ]]; then
    echo "PASS: $name ($actual == $expected)"
  else
    echo "FAIL: $name ($actual != $expected)" >&2
    return 1
  fi
}

extract() { echo "$1" | jq -r ".ledger.$2"; }

echo "=== Step 1: Org A first call (expect cache write) ==="
OUT_A1="$(call "$ORG_A" a1 | tail -n +2)"
CW_A1=$(extract "$OUT_A1" cache_creation_input_tokens)
CR_A1=$(extract "$OUT_A1" cache_read_input_tokens)
echo "A1: cacheWrite=$CW_A1 cacheRead=$CR_A1"

echo "=== Step 2: Org A second call (expect cache hit) ==="
OUT_A2="$(call "$ORG_A" a2 | tail -n +2)"
CW_A2=$(extract "$OUT_A2" cache_creation_input_tokens)
CR_A2=$(extract "$OUT_A2" cache_read_input_tokens)
echo "A2: cacheWrite=$CW_A2 cacheRead=$CR_A2"

echo "=== Step 3: Org B first call, same body (expect no cross-org read) ==="
OUT_B1="$(call "$ORG_B" b1 | tail -n +2)"
CW_B1=$(extract "$OUT_B1" cache_creation_input_tokens)
CR_B1=$(extract "$OUT_B1" cache_read_input_tokens)
echo "B1: cacheWrite=$CW_B1 cacheRead=$CR_B1"

echo
echo "=== Assertions ==="
fails=0
assert_gt "A1 wrote to cache" "$CW_A1" 0 || fails=$((fails+1))
assert_gt "A2 read from cache" "$CR_A2" 0 || fails=$((fails+1))
assert_eq "B1 did NOT read Org A's cache" "$CR_B1" 0 || fails=$((fails+1))

if (( fails == 0 )); then
  echo
  echo "ALL PASS — Law 3 cache isolation holds."
  exit 0
else
  echo
  echo "FAILED ($fails assertion(s))" >&2
  exit 1
fi
