# tilth/bin — cache + batch wrappers

Two Node scripts that make Anthropic prompt caching and the Message Batches API usable from Tilth workflows. Both import the vendored `@anthropic-ai/sdk` that ships with OpenClaw; no separate `npm install`. Both require `ANTHROPIC_API_KEY` in env (same key the OpenClaw gateway uses).

Per `AGENTS.md` → "Caching Discipline", every cached system block must start with:

    ORG:<orgSlug>
    TRACE:<sessionId>
    <preamble…>

The scripts do not rewrite your system text — you prepend the two lines yourself before passing `--system`.

---

## Pattern 1 — Sync cached inference (`tilth-infer-cached.mjs`)

One-shot Anthropic call with cache telemetry appended to `tilth/logs/<org>/cache-ledger.jsonl`.

    node tilth/bin/tilth-infer-cached.mjs \
      --model anthropic/claude-sonnet-4-6 \
      --system "$(printf 'ORG:%s\nTRACE:%s\n%s' "$ORG" "$TRACE" "$PREAMBLE")" \
      --prompt "$USER_TEXT" \
      --org "$ORG" \
      --workflow scribe-draft \
      --max-tokens 2048 \
      --cache-retention long

Writes:

- `tilth/logs/<org>/cache-ledger.jsonl` — one line per call (ts, model, token counts, `cached_savings_usd`)
- `tilth/logs/<org>/cache-tally.json` — rolling totals by workflow

First call with a given preamble should log non-zero `cache_creation_input_tokens`. Second call with the identical preamble (within the 1h window for `--cache-retention long`, 5min for `short`) should log non-zero `cache_read_input_tokens` and a non-zero `cached_savings_usd`.

---

## Pattern 2 — Batch submit (`tilth-batch.mjs submit`)

Submit a JSONL of `{custom_id?, params}` rows to `/v1/messages/batches`. If `custom_id` is omitted, one is generated as `<orgSlug>:<workflow>:<uuid>`. Caching compounds inside the batch — each request can carry its own `cache_control` on its own system block.

    node tilth/bin/tilth-batch.mjs submit \
      --requests path/to/requests.jsonl \
      --org acme \
      --workflow scout-daily-radar

Returns JSON on stdout including `batch_id`. Full submit record saved at `tilth/logs/<org>/batches/<batchId>/submit.json`.

Each JSONL row looks like:

    {"params":{"model":"claude-sonnet-4-6","max_tokens":256,"system":[{"type":"text","text":"ORG:acme\nTRACE:xyz\n…","cache_control":{"type":"ephemeral","ttl":"1h"}}],"messages":[{"role":"user","content":"…"}]}}

---

## Pattern 3 — Batch status + fetch

Poll status (Anthropic may take up to 24h; usually minutes):

    node tilth/bin/tilth-batch.mjs status --batch-id msgbatch_… --org acme

When `processing_status` is `ended`, stream the results:

    node tilth/bin/tilth-batch.mjs fetch --batch-id msgbatch_… --org acme

Results land at `tilth/logs/<org>/batches/<batchId>/results.jsonl`. Match rows back to requests by `custom_id`.

---

## Acceptance test — org isolation

    ANTHROPIC_API_KEY=… bash tilth/tests/test_cache_org_isolation.sh

Three assertions: (1) Org A first call writes cache; (2) Org A second call reads cache; (3) Org B with same preamble body but different `ORG:` prefix does NOT read Org A's cache. Exit 0 = Law 3 holds.

---

## When not to use these

- Any flow routed through `claude-cli/*` model refs — OAuth auth strips `cache_control`; cache won't fire. Use `anthropic/*` api-key refs instead (see `router.yaml`).
- Scout two-stage discovery's VERIFY step — live synopsis fetching is a different API surface, not Anthropic inference.
- Anything under Cedar M13 bypass — caching is orthogonal to bypass, but telemetry will log the call and inflate ledger; be deliberate.
