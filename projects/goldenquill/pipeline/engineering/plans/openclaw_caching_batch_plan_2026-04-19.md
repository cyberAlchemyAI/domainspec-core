# OpenClaw Prompt Caching + Batch API + Opus 4.7 Integration Plan

**Date:** 2026-04-19
**Author:** Plan/Opus subagent via Cowork delegation
**Status:** Executed — config-only changes applied this session; batch wrapper + telemetry are engineering follow-ups
**Context:** Tilth sovereign grant-writing system, BYOK API costs paid by operator. 90% savings on cached prompts + 50% savings on batched non-time-sensitive work = mission-aligned cost reduction.

---

## Key findings from plugin probe (saves rediscovery)

1. **OpenClaw 2026.4.14's Anthropic plugin ALREADY SUPPORTS prompt caching.** Hidden in rollup-chunk files (`anthropic-payload-policy-DoMPeV9T.js`, `extra-params-BtfRJ0hh.js`, `usage-n3a2gQ8W.js`), not the top-level human-readable plugin files my initial grep missed. Implementation:
   - Underlying SDK: `@mariozechner/pi-ai@0.66.1` which wraps `@anthropic-ai/sdk`. Both vendored in `~/.npm-global/lib/node_modules/openclaw/node_modules/`.
   - Applies `cache_control: { type: "ephemeral" }` (with optional `ttl: "1h"` for `cacheRetention: "long"`) to system prompt, tools, last user block.
   - Accepts `options.cacheRetention: "short" | "long" | "none"`.
   - Defaults to `"short"` (5min TTL) for api-key auth. `PI_CACHE_RETENTION=long` env flips to 1h.
   - `cache_creation_input_tokens` / `cache_read_input_tokens` normalize to `usage.cacheWrite` / `usage.cacheRead`.

2. **Batch API IS missing.** Anthropic SDK has `resources/messages/batches.js` ready to use; OpenClaw never calls it. Needs external wrapper script.

3. **Opus 4.7 shipped 2026-04-16** as `claude-opus-4-7`, drop-in for 4-6. OpenClaw's forward-compat resolver only pattern-matches 4-5/4-6; doesn't auto-discover 4-7. Needs explicit allowlist entry.

4. **Law 3 cache isolation risk.** Cache keys = exact prompt prefix. Two orgs with identical preambles would share cached tokens (cross-org leak). Mitigation: namespace every cached system block with `ORG:<orgId>` prefix. Enforcement at prompt-construction layer, not plugin.

5. **OAuth/Claude-CLI auth path strips cache_control.** Caching config only takes effect on `anthropic/*` (api-key auth) model refs, NOT on `claude-cli/*`. Route cost-sensitive reusable flows through api-key models.

---

## Architecture — Option 3 hybrid (executed)

**Config-only caching enablement + external Batch wrapper.** No OpenClaw patches.

Why this path: npm update safety, maintenance-free, leverages existing SDK support, batch bypass of gateway is fine because batching is async by nature.

---

## What got executed this session

### 1. Caching enabled via config

```
openclaw config set 'agents.defaults.models.anthropic/claude-sonnet-4-6.params.cacheRetention' long
openclaw config set 'agents.defaults.models.anthropic/claude-opus-4-6.params.cacheRetention' long
openclaw config set 'agents.defaults.models.anthropic/claude-opus-4-7.params.cacheRetention' long
```

1h cache retention for Anthropic models used by Scribe (routine + escalation) and the future Opus 4.7.

### 2. Opus 4.7 added to allowlist

Via Python-patch (L-008 workaround for the bracket-quote bug), `agents.defaults.models` now includes `anthropic/claude-opus-4-7` + associated `params.cacheRetention: long`.

### 3. Daemon restart

`openclaw gateway restart` applied for config to take effect.

### 4. Smoke test

- First Opus 4.7 call: should log `cache_creation_input_tokens` > 0
- Second Opus 4.7 call (same system prompt): should log `cache_read_input_tokens` > 0 and `cache_creation_input_tokens` = 0

---

## Engineering follow-ups (not done this session — surfaces for operator decision)

### Follow-up A — `tilth-batch.mjs` external wrapper

External Node script, ~150 lines, imports the vendored `@anthropic-ai/sdk` directly from OpenClaw's node_modules. Three subcommands: `submit`, `status`, `fetch`.

- Submit: POST `/v1/messages/batches` with N requests, each tagged `custom_id: <orgId>:<workflow>:<uuid>` for Law 3 isolation + traceability.
- Status: poll `/v1/messages/batches/{id}`.
- Fetch: stream results into `tilth/logs/<org>/batches/<batchId>/results.jsonl`.

Each request within a batch can carry its own `system` block with `cache_control` — caching compounds with batching for double savings.

Auth: reads `ANTHROPIC_API_KEY` from env (same as gateway). Bypasses OpenClaw gateway entirely for batch endpoints.

**Estimated build: 2-3 hours. Test suite: 1-2 hours. Total: half-day.**

### Follow-up B — Cache telemetry ledger

`tilth-infer-cached.mjs` wrapper that shells out to `openclaw infer model run`, parses response usage, writes `tilth/logs/<org>/cache-ledger.jsonl` with per-call savings.

Needed because OpenClaw CLI doesn't surface `cacheRead`/`cacheWrite` by default — the normalized fields are in the response envelope but Tilth scripts need to extract them for accounting.

**Estimated build: 1 hour. Useful for proving caching is actually firing under live Tilth workloads.**

### Follow-up C — Org-isolation preamble prefixing

Tilth script convention: every cached system prompt starts with `ORG:<orgSlug>\nTRACE:<sessionId>\n`. This ensures two orgs with otherwise-identical preambles produce different cache keys.

**Implementation: convention + one acceptance test** (call for Org A, then Org B with same preamble body, verify `cache_read_input_tokens = 0` for Org B's first call).

### Follow-up D — router.yaml amendment for Opus 4.7

Once Opus 4.7 is smoke-tested, consider elevating:
- Scribe escalation: `claude-opus-4-6` → `claude-opus-4-7` (stronger reasoning for complex sections)
- Da Vinci backing model: already references 4.7 in architecture v7 A2 Block 1; router.yaml now aligned

---

## Tilth workflow savings map

| # | Workflow | Pattern | Savings mechanism | Est. savings |
|---|----------|---------|-------------------|--------------|
| 1 | Cross-family audit (today's pattern: 3 seats × ~5K preamble) | Cache 4K preamble across 3 calls | 1h cache (long) | Call 1 +25%, Calls 2-3 −70%. Net ~50% for 3-call audit. |
| 2 | Cycle 2 re-audit (amendments + prior debate trail) | Cache 6-8K context | 5min cache | ~65% on repeated tokens |
| 3 | Scout daily radar (20-50 candidates, same format) | Preamble + per-candidate 500-1500 tokens | **Batch API** (3am cron) + cache inside batch | ~60-70% total |
| 4 | Judge rubric scoring across 8 sections | Same 3K rubric, different 2K section | 5min cache | ~55% on repeated rubric tokens |
| 5 | Scribe draft expansion from outline | 5K org + funder anchor, 200-token paragraph prompts | 5min cache | ~70% per paragraph |
| 6 | Monthly lessons.md cross-org lint | 10K preamble, 50+ entries | **Batch API** overnight + 1h cache | ~65% total |

**Estimated weekly API-spend reduction: 35-45% typical, >50% under heavy re-audit workloads.**

---

## Verification steps (post-daemon-restart)

1. Run Scribe call twice with same system prompt. Check gateway log for `cache_creation_input_tokens > 0` on call 1, `cache_read_input_tokens > 0` on call 2.
2. If usage fields not surfaced in CLI output, check gateway log path (`openclaw daemon status` for log location) or the future telemetry ledger (Follow-up B).
3. If cache never fires: verify `cacheRetention: long` is in config (`openclaw config get agents.defaults.models.anthropic/claude-sonnet-4-6.params`), check auth mode is api-key not OAuth, inspect outbound payload for `cache_control` marker.

---

## Law 3 isolation note (MANDATORY for multi-org use)

As Tilth scales beyond Josh's single-operator use to multiple client orgs, the preamble-prefixing convention (Follow-up C) becomes non-optional. Without it, caching creates a cross-org side channel: an identical preamble body between two orgs produces identical cache keys, meaning Org B's first call may read Org A's cached tokens (and pay nothing for tokens Anthropic attributes to Org A's workspace). Anthropic's Feb 2026 workspace-isolation change partially mitigates this at the workspace level; Tilth's defense-in-depth is per-org API key OR per-org preamble prefix (or both).

Current single-operator use: acceptable without prefix convention. Future multi-org use: required before first multi-org audit run.

---

## Opus 4.7 activation summary

- Shipped 2026-04-16 as `claude-opus-4-7` (drop-in for 4-6).
- Adds high-resolution image support (GA), adaptive thinking by default.
- OpenClaw resolver does not auto-discover; explicit allowlist entry executed this session.
- `shouldUseAnthropicAdaptiveThinkingDefault` only matches 4-5/4-6 — for 4-7, set `params.thinking: {type:"adaptive"}` manually if adaptive reasoning desired.
- Beta header `task-budgets-2026-03-13` available via `params.anthropicBeta` if task-budget features are needed.

---

## Risk register (active)

| Risk | Mitigation |
|------|------------|
| npm upgrade wipes config | Config is in `~/.config/openclaw/`, not node_modules. Verify after each upgrade with `openclaw config get`. |
| Cache not firing silently | Telemetry ledger (Follow-up B) provides visibility. Add to quarterly Operating audit (TSIP Phase 7). |
| Law 3 cross-org leak | Follow-up C preamble prefix before any multi-org use. |
| SDK version mismatch (pi-ai upgrades break API) | Add to TSIP surveillance watchlist: weekly check `npm ls @mariozechner/pi-ai` vs pinned version. |
| OAuth path strips cache_control | Use api-key auth models for cost-sensitive reusable flows. Document in AGENTS.md. |
| Opus 4.7 adaptive thinking not auto-enabled | Manual `params.thinking: {type:"adaptive"}` in config until OpenClaw 2026.5.x updates resolver. |
| Batch request quota interaction with sync quota | Space batch submissions during low-use hours (cron 3am); monitor combined quota hit. |
| 1h cache eviction mid-workflow | Refresh on hit extends TTL; long workflows stay warm. If idle >1h, recompute once. |

---

## Watchlist items added to TSIP surveillance

1. **Anthropic model release** — any new `claude-*-4-N` where N > current default → patch allowlist + model config within 24h.
2. **OpenClaw release** — any version bump → run post-upgrade verification of caching config.
3. **pi-ai release** — any breaking change to `options.cacheRetention` API → immediate Thesis round.
4. **Anthropic API billing changes** — cache cost multipliers or batch discounts adjust → refresh workflow savings map.

---

## Sources

- Prompt caching docs: https://platform.claude.com/docs/en/build-with-claude/prompt-caching
- Batch processing docs: https://platform.claude.com/docs/en/build-with-claude/batch-processing
- Opus 4.7 release: https://github.blog/changelog/2026-04-16-claude-opus-4-7-is-generally-available/
- OpenClaw plugin source (read-only reference): `~/.npm-global/lib/node_modules/openclaw/dist/extensions/anthropic/`
- SDK bundled: `@mariozechner/pi-ai@0.66.1`, `@anthropic-ai/sdk` (both vendored under openclaw's node_modules)
