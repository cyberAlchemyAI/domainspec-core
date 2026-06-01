#!/usr/bin/env node
// tilth-batch.mjs — Anthropic Message Batches wrapper for Tilth.
//
// Subcommands:
//   submit --requests <jsonl> --org <slug> [--workflow <name>]
//   status --batch-id <id>   --org <slug>
//   fetch  --batch-id <id>   --org <slug> [--out <jsonl>]
//
// Auth: ANTHROPIC_API_KEY from env.
// SDK:  imports vendored @anthropic-ai/sdk from OpenClaw's node_modules.
// Per handoff `pipeline/handoffs/caching_batch_build_handoff_2026-04-19.md` §D1.

import { createRequire } from "node:module";
import { randomUUID } from "node:crypto";
import { createReadStream, promises as fs } from "node:fs";
import path from "node:path";
import readline from "node:readline";

const OPENCLAW_MODULES =
  "/Users/goldenquill/.npm-global/lib/node_modules/openclaw/node_modules";
const SDK_PKG_PATH = path.join(OPENCLAW_MODULES, "@anthropic-ai/sdk/package.json");

const require_ = createRequire(SDK_PKG_PATH);
const Anthropic = require_("@anthropic-ai/sdk").default;

const REPO_ROOT = path.resolve(new URL(".", import.meta.url).pathname, "../..");
const LOGS_ROOT = path.join(REPO_ROOT, "tilth/logs");

function die(msg, code = 2) {
  process.stderr.write(`tilth-batch: ${msg}\n`);
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

function requireEnvKey() {
  const key = process.env.ANTHROPIC_API_KEY;
  if (!key) die("ANTHROPIC_API_KEY not set in env");
  return key;
}

function client() {
  return new Anthropic({ apiKey: requireEnvKey() });
}

function customId(orgSlug, workflow) {
  // Anthropic requires custom_id to match /^[a-zA-Z0-9_-]{1,64}$/, so we use
  // underscores (not colons) and strip UUID dashes to fit the 64-char ceiling.
  const wf = (workflow || "default").replace(/[^a-zA-Z0-9_-]/g, "-");
  const slug = orgSlug.replace(/[^a-zA-Z0-9_-]/g, "-");
  const uuid = randomUUID().replace(/-/g, "");
  let id = `${slug}_${wf}_${uuid}`;
  if (id.length > 64) {
    // keep slug intact, truncate workflow then shorten uuid as a last resort
    const keep = 64 - slug.length - 2;
    const half = Math.max(8, Math.floor(keep / 2));
    const wfCut = wf.slice(0, keep - half);
    const idCut = uuid.slice(0, keep - wfCut.length);
    id = `${slug}_${wfCut}_${idCut}`;
  }
  return id.slice(0, 64);
}

async function readJsonl(filePath) {
  const rl = readline.createInterface({
    input: createReadStream(filePath, "utf8"),
    crlfDelay: Infinity,
  });
  const rows = [];
  let lineNum = 0;
  for await (const line of rl) {
    lineNum++;
    const trimmed = line.trim();
    if (!trimmed) continue;
    try {
      rows.push(JSON.parse(trimmed));
    } catch (err) {
      die(`invalid JSON at ${filePath}:${lineNum} — ${err.message}`);
    }
  }
  return rows;
}

async function ensureDir(p) {
  await fs.mkdir(p, { recursive: true });
}

// ---- submit -----------------------------------------------------------------
async function cmdSubmit(args) {
  const requestsPath = args.requests;
  const orgSlug = args.org;
  const workflow = args.workflow || "default";
  if (!requestsPath) die("submit: --requests <jsonl> is required");
  if (!orgSlug) die("submit: --org <slug> is required");

  const rows = await readJsonl(requestsPath);
  if (rows.length === 0) die(`submit: ${requestsPath} has no rows`);

  const requests = rows.map((row) => {
    const { custom_id, params, ...rest } = row;
    const merged = params ? { ...rest, ...params } : rest;
    return {
      custom_id: custom_id || customId(orgSlug, row.workflow || workflow),
      params: merged,
    };
  });

  const seen = new Set();
  for (const r of requests) {
    if (seen.has(r.custom_id)) die(`submit: duplicate custom_id ${r.custom_id}`);
    seen.add(r.custom_id);
  }

  const anthropic = client();
  const batch = await anthropic.messages.batches.create({ requests });

  const orgLogDir = path.join(LOGS_ROOT, orgSlug, "batches", batch.id);
  await ensureDir(orgLogDir);
  await fs.writeFile(
    path.join(orgLogDir, "submit.json"),
    JSON.stringify({ submitted_at: new Date().toISOString(), batch, requests }, null, 2),
  );

  process.stdout.write(JSON.stringify({
    batch_id: batch.id,
    processing_status: batch.processing_status,
    request_counts: batch.request_counts,
    request_count: requests.length,
    log_dir: orgLogDir,
  }) + "\n");
}

// ---- status -----------------------------------------------------------------
async function cmdStatus(args) {
  const batchId = args["batch-id"];
  const orgSlug = args.org;
  if (!batchId) die("status: --batch-id <id> is required");
  if (!orgSlug) die("status: --org <slug> is required");

  const anthropic = client();
  const batch = await anthropic.messages.batches.retrieve(batchId);

  const orgLogDir = path.join(LOGS_ROOT, orgSlug, "batches", batch.id);
  await ensureDir(orgLogDir);
  await fs.writeFile(
    path.join(orgLogDir, "status.json"),
    JSON.stringify({ checked_at: new Date().toISOString(), batch }, null, 2),
  );

  process.stdout.write(JSON.stringify({
    batch_id: batch.id,
    processing_status: batch.processing_status,
    request_counts: batch.request_counts,
    ended_at: batch.ended_at,
    results_url: batch.results_url,
  }) + "\n");
}

// ---- fetch ------------------------------------------------------------------
async function cmdFetch(args) {
  const batchId = args["batch-id"];
  const orgSlug = args.org;
  if (!batchId) die("fetch: --batch-id <id> is required");
  if (!orgSlug) die("fetch: --org <slug> is required");

  const orgLogDir = path.join(LOGS_ROOT, orgSlug, "batches", batchId);
  await ensureDir(orgLogDir);
  const outPath = args.out || path.join(orgLogDir, "results.jsonl");

  const anthropic = client();
  const batch = await anthropic.messages.batches.retrieve(batchId);
  if (batch.processing_status !== "ended") {
    die(
      `fetch: batch ${batchId} not ended (status=${batch.processing_status}); ` +
        `retry after completion`,
      3,
    );
  }

  const stream = await anthropic.messages.batches.results(batchId);
  const lines = [];
  let count = 0;
  for await (const row of stream) {
    lines.push(JSON.stringify(row));
    count++;
  }
  await fs.writeFile(outPath, lines.join("\n") + (lines.length ? "\n" : ""));

  process.stdout.write(JSON.stringify({
    batch_id: batchId,
    written: outPath,
    row_count: count,
    request_counts: batch.request_counts,
  }) + "\n");
}

// ---- dispatch ---------------------------------------------------------------
async function main() {
  const [, , sub, ...rest] = process.argv;
  const args = parseArgs(rest);
  switch (sub) {
    case "submit":
      await cmdSubmit(args);
      break;
    case "status":
      await cmdStatus(args);
      break;
    case "fetch":
      await cmdFetch(args);
      break;
    case "-h":
    case "--help":
    case undefined:
      process.stdout.write(
        `usage:
  tilth-batch submit --requests <jsonl> --org <slug> [--workflow <name>]
  tilth-batch status --batch-id <id>   --org <slug>
  tilth-batch fetch  --batch-id <id>   --org <slug> [--out <jsonl>]
`,
      );
      process.exit(sub ? 0 : 2);
      break;
    default:
      die(`unknown subcommand: ${sub}`);
  }
}

main().catch((err) => {
  process.stderr.write(`tilth-batch: ${err.stack || err.message || err}\n`);
  process.exit(1);
});
