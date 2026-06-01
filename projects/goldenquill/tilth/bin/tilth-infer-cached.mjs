#!/usr/bin/env node
// tilth-infer-cached.mjs — cache telemetry wrapper around Anthropic inference.
//
// Usage:
//   tilth-infer-cached \
//     --model anthropic/claude-sonnet-4-6 \
//     --system "<system preamble>" \
//     --prompt "<user text>" \
//     --org <orgSlug> \
//     [--workflow <name>] [--max-tokens 1024] [--cache-retention long|short] \
//     [--cycle-id <id>] [--seat <scribe|scout|judge|editor|red_team|logician>] \
//     [--card-id <id>]
//
// `--cycle-id`, `--seat`, and `--card-id` are optional and backward-compatible.
// When supplied, they are stamped into the per-call ledger row so downstream
// tooling (e.g. `tilth metrics cycle-cost`) can join + break down spend by
// cycle / seat / card invocation. Rows from before this change have these
// fields absent — the reader treats absent as "unattributed".
//
// Why SDK not openclaw CLI: `openclaw infer model run --json` does NOT surface
// `usage.cacheRead`/`usage.cacheWrite` as of 2026.4.14 — the normalized fields
// exist inside pi-ai but are not emitted through the CLI envelope (only
// `outputs[].text`). Log-tailing the gateway JSON stream is brittle. The
// handoff spec's "fall back" clause (plan §B.2) applies here: call the
// vendored @anthropic-ai/sdk directly with the same ANTHROPIC_API_KEY the
// gateway uses, which gives us deterministic access to
// `cache_read_input_tokens` and `cache_creation_input_tokens`. Documented as a
// deviation in `daily_logs/2026-04-20.md`.
//
// Writes:
//   tilth/logs/<org>/cache-ledger.jsonl  (append per call)
//   tilth/logs/<org>/cache-tally.json    (overwrite running tally)

import { createRequire } from "node:module";
import { promises as fs, existsSync } from "node:fs";
import path from "node:path";

const OPENCLAW_MODULES =
  "/Users/goldenquill/.npm-global/lib/node_modules/openclaw/node_modules";
const SDK_PKG_PATH = path.join(OPENCLAW_MODULES, "@anthropic-ai/sdk/package.json");
const require_ = createRequire(SDK_PKG_PATH);
const Anthropic = require_("@anthropic-ai/sdk").default;

const REPO_ROOT = path.resolve(new URL(".", import.meta.url).pathname, "../..");
const LOGS_ROOT = path.join(REPO_ROOT, "tilth/logs");

// Anthropic prices — USD per million tokens. Cache multipliers per
// https://platform.claude.com/docs/en/build-with-claude/prompt-caching
// Cache read = 0.1× base input. Cache write long (1h) = 2×. Cache write
// short (5min) = 1.25×.
const MODEL_RATES = {
  "claude-sonnet-4-6": { inputPerMTok: 3.0, outputPerMTok: 15.0 },
  "claude-opus-4-6":   { inputPerMTok: 15.0, outputPerMTok: 75.0 },
  "claude-opus-4-7":   { inputPerMTok: 15.0, outputPerMTok: 75.0 },
  "claude-haiku-4-5":  { inputPerMTok: 0.8,  outputPerMTok: 4.0 },
};

function die(msg, code = 2) {
  process.stderr.write(`tilth-infer-cached: ${msg}\n`);
  process.exit(code);
}

function parseArgs(argv) {
  const out = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith("--")) {
      const k = a.slice(2);
      const v = argv[i + 1];
      if (v === undefined || v.startsWith("--")) {
        out[k] = true;
      } else {
        out[k] = v;
        i++;
      }
    } else {
      out._.push(a);
    }
  }
  return out;
}

function normalizeModel(m) {
  // strip "anthropic/" prefix if present
  return m.includes("/") ? m.split("/").pop() : m;
}

function ratesFor(model) {
  const key = normalizeModel(model);
  const r = MODEL_RATES[key];
  if (!r) {
    return { inputPerMTok: 3.0, outputPerMTok: 15.0, fallback: true };
  }
  return { ...r, fallback: false };
}

function computeCostsUSD({ usage, rates, cacheRetention }) {
  // Tokens reported by Anthropic.
  const u = usage || {};
  const inputTokens = u.input_tokens ?? 0;
  const outputTokens = u.output_tokens ?? 0;
  const cacheRead = u.cache_read_input_tokens ?? 0;
  const cacheWrite = u.cache_creation_input_tokens ?? 0;

  const cacheReadRate = rates.inputPerMTok * 0.1;
  const cacheWriteRate =
    cacheRetention === "long"
      ? rates.inputPerMTok * 2.0
      : rates.inputPerMTok * 1.25;

  // Note: Anthropic returns `input_tokens` as uncached-only (tokens that were
  // neither read from cache nor written to cache). Billed totals combine all
  // three buckets.
  const paidUSD =
    (inputTokens / 1e6) * rates.inputPerMTok +
    (outputTokens / 1e6) * rates.outputPerMTok +
    (cacheRead / 1e6) * cacheReadRate +
    (cacheWrite / 1e6) * cacheWriteRate;

  // Savings = (what we'd have paid without cache read) minus (what we paid for
  // cache read). Cache-write is a premium we accept to enable future reads;
  // not counted as savings here.
  const cachedSavingsUSD = (cacheRead / 1e6) * (rates.inputPerMTok - cacheReadRate);

  return {
    input_tokens: inputTokens,
    output_tokens: outputTokens,
    cache_read_input_tokens: cacheRead,
    cache_creation_input_tokens: cacheWrite,
    paid_usd: round6(paidUSD),
    cached_savings_usd: round6(cachedSavingsUSD),
  };
}

function round6(n) {
  return Math.round(n * 1e6) / 1e6;
}

async function ensureDir(p) {
  await fs.mkdir(p, { recursive: true });
}

async function appendJsonl(filePath, obj) {
  await ensureDir(path.dirname(filePath));
  await fs.appendFile(filePath, JSON.stringify(obj) + "\n");
}

async function updateTally(tallyPath, entry) {
  await ensureDir(path.dirname(tallyPath));
  let tally = {
    totals: {
      calls: 0,
      input_tokens: 0,
      output_tokens: 0,
      cache_read_input_tokens: 0,
      cache_creation_input_tokens: 0,
      paid_usd: 0,
      cached_savings_usd: 0,
    },
    per_workflow: {},
    updated_at: null,
  };
  if (existsSync(tallyPath)) {
    try {
      tally = JSON.parse(await fs.readFile(tallyPath, "utf8"));
    } catch {
      // corrupt — reset; previous ledger jsonl is the source of truth.
    }
  }
  const wf = entry.workflow || "default";
  if (!tally.per_workflow[wf]) {
    tally.per_workflow[wf] = {
      calls: 0,
      input_tokens: 0,
      output_tokens: 0,
      cache_read_input_tokens: 0,
      cache_creation_input_tokens: 0,
      paid_usd: 0,
      cached_savings_usd: 0,
    };
  }
  const buckets = [tally.totals, tally.per_workflow[wf]];
  for (const b of buckets) {
    b.calls += 1;
    b.input_tokens += entry.input_tokens;
    b.output_tokens += entry.output_tokens;
    b.cache_read_input_tokens += entry.cache_read_input_tokens;
    b.cache_creation_input_tokens += entry.cache_creation_input_tokens;
    b.paid_usd = round6(b.paid_usd + entry.paid_usd);
    b.cached_savings_usd = round6(b.cached_savings_usd + entry.cached_savings_usd);
  }
  tally.updated_at = new Date().toISOString();
  await fs.writeFile(tallyPath, JSON.stringify(tally, null, 2));
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help || args.h) {
    process.stdout.write(
      `usage: tilth-infer-cached \\
  --model anthropic/claude-sonnet-4-6 --system "<preamble>" \\
  --prompt "<user>" --org <slug> [--workflow <name>] \\
  [--max-tokens 1024] [--cache-retention long|short]
`,
    );
    process.exit(0);
  }

  const model = args.model || "anthropic/claude-sonnet-4-6";
  const systemText = args.system || "";
  const userText = args.prompt || "";
  const orgSlug = args.org;
  const workflow = args.workflow || "default";
  const maxTokens = Number(args["max-tokens"] || 1024);
  const cacheRetention = args["cache-retention"] || "long";
  const cycleId = args["cycle-id"] === true ? null : args["cycle-id"] || null;
  const seat = args.seat === true ? null : args.seat || null;
  const cardId = args["card-id"] === true ? null : args["card-id"] || null;
  if (!orgSlug) die("--org <slug> is required");
  if (!userText) die("--prompt <text> is required");
  if (!systemText) die("--system <text> is required to exercise caching");

  const apiKey = process.env.ANTHROPIC_API_KEY;
  if (!apiKey) die("ANTHROPIC_API_KEY not set in env");

  const anthropic = new Anthropic({ apiKey });

  const systemBlock = [
    {
      type: "text",
      text: systemText,
      cache_control:
        cacheRetention === "long"
          ? { type: "ephemeral", ttl: "1h" }
          : { type: "ephemeral" },
    },
  ];

  const modelName = normalizeModel(model);
  const started = Date.now();
  const response = await anthropic.messages.create({
    model: modelName,
    max_tokens: maxTokens,
    system: systemBlock,
    messages: [{ role: "user", content: userText }],
  });
  const elapsedMs = Date.now() - started;

  const rates = ratesFor(model);
  const costs = computeCostsUSD({
    usage: response.usage,
    rates,
    cacheRetention,
  });

  const entry = {
    ts: new Date().toISOString(),
    org: orgSlug,
    workflow,
    model: modelName,
    cache_retention: cacheRetention,
    elapsed_ms: elapsedMs,
    ...costs,
    response_id: response.id,
    stop_reason: response.stop_reason,
    rates_fallback: rates.fallback,
    cycle_id: cycleId,
    seat,
    card_id: cardId,
  };

  const orgLogDir = path.join(LOGS_ROOT, orgSlug);
  const ledgerPath = path.join(orgLogDir, "cache-ledger.jsonl");
  const tallyPath = path.join(orgLogDir, "cache-tally.json");
  await appendJsonl(ledgerPath, entry);
  await updateTally(tallyPath, entry);

  const text = (response.content || [])
    .filter((b) => b.type === "text")
    .map((b) => b.text)
    .join("");

  process.stdout.write(
    JSON.stringify(
      {
        ok: true,
        text,
        ledger: entry,
        log_paths: { ledger: ledgerPath, tally: tallyPath },
      },
      null,
      2,
    ) + "\n",
  );
}

main().catch((err) => {
  process.stderr.write(`tilth-infer-cached: ${err.stack || err.message || err}\n`);
  process.exit(1);
});
