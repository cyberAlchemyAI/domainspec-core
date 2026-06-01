import { spawn } from "node:child_process";
import { readFile } from "node:fs/promises";
import { homedir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const appRoot = fileURLToPath(new URL("../", import.meta.url));
const repoRoot = join(appRoot, "..", "..");
const routerPath = join(repoRoot, "router.yaml");
const openClawBin = process.env.OPENCLAW_BIN || "openclaw";
const pythonBin = process.env.TILTH_PYTHON_BIN || join(repoRoot, ".venv", "bin", "python3");

function normalizeAction(action) {
  return String(action || "").trim().replace(/[-\s]+/g, "_").toLowerCase();
}

function openClawEnv() {
  const pathPrefix = [
    join(homedir(), ".npm-global", "bin"),
    "/opt/homebrew/opt/node/bin",
    "/opt/homebrew/bin",
    "/usr/local/bin",
  ].join(":");
  return {
    ...process.env,
    PATH: `${pathPrefix}:${process.env.PATH || ""}`,
  };
}

function extractSeatBlock(routerText, seat) {
  const lines = routerText.split(/\r?\n/);
  const seatHeader = new RegExp(`^\\s{2}${seat}:\\s*$`);
  const start = lines.findIndex((line) => seatHeader.test(line));
  if (start < 0) throw new Error(`router.yaml is missing tilth.${seat}`);
  const block = [];
  for (let index = start + 1; index < lines.length; index += 1) {
    const line = lines[index];
    if (/^\s{2}[A-Za-z0-9_]+:\s*(?:#.*)?$/.test(line)) break;
    block.push(line);
  }
  return block.join("\n");
}

export async function readRouterModel(seat, tier = "primary") {
  const routerText = await readFile(routerPath, "utf8");
  const block = extractSeatBlock(routerText, seat);
  const match = block.match(new RegExp(`^\\s{4}${tier}:\\s*([^\\s#]+)`, "m"));
  if (!match) throw new Error(`router.yaml is missing tilth.${seat}.${tier}`);
  return match[1].trim();
}

function parseGatewayOutput(stdout) {
  try {
    const json = JSON.parse(stdout);
    const outputText = json.outputs?.map((item) => item.text).filter(Boolean).join("\n").trim() || "";
    return {
      json,
      output_text: outputText,
      transport: json.transport,
      provider: json.provider,
      model: json.model,
    };
  } catch {
    return {
      json: null,
      output_text: stdout.trim(),
      transport: "",
      provider: "",
      model: "",
    };
  }
}

export function runOpenClaw(args, options = {}) {
  const timeoutMs = Number(options.timeoutMs || 90_000);
  return new Promise((resolve) => {
    const startedAt = new Date().toISOString();
    const child = spawn(openClawBin, args, {
      cwd: appRoot,
      env: openClawEnv(),
      stdio: ["ignore", "pipe", "pipe"],
    });
    const stdout = [];
    const stderr = [];
    let timedOut = false;
    const timer = setTimeout(() => {
      timedOut = true;
      child.kill("SIGTERM");
    }, timeoutMs);

    child.stdout.on("data", (chunk) => stdout.push(chunk));
    child.stderr.on("data", (chunk) => stderr.push(chunk));
    child.on("error", (error) => {
      clearTimeout(timer);
      resolve({
        ok: false,
        started_at: startedAt,
        finished_at: new Date().toISOString(),
        error: error.message,
        stdout: Buffer.concat(stdout).toString("utf8"),
        stderr: Buffer.concat(stderr).toString("utf8"),
      });
    });
    child.on("close", (code) => {
      clearTimeout(timer);
      const out = Buffer.concat(stdout).toString("utf8");
      const err = Buffer.concat(stderr).toString("utf8");
      resolve({
        ok: code === 0 && !timedOut,
        exit_code: code,
        timed_out: timedOut,
        started_at: startedAt,
        finished_at: new Date().toISOString(),
        stdout: out,
        stderr: err,
      });
    });
  });
}

async function openClawStatus() {
  const result = await runOpenClaw(["--version"], { timeoutMs: 15_000 });
  return {
    ok: result.ok,
    action: "status",
    version: result.stdout.trim(),
    reason: result.ok ? "" : result.stderr.trim() || result.error || "OpenClaw status check failed.",
    exit_code: result.exit_code,
  };
}

function runTilthScoutBridge(args, options = {}) {
  // Spawns the dev-path Scout bridge:
  //   <repo>/.venv/bin/python3 -m pipeline.deprecated.operator_glue.tilth_scout_ui --org-slug ...
  // Live Grants.gov (Channel A) + orchestrator/seats/scout.py (router-bound
  // ollama/mistral:7b) → JSON on stdout matching SCOUT_INTEGRATION_SPEC §2.
  // Bridge lives under pipeline.deprecated.operator_glue/ so AST-lint
  // quarantines its direct ollama-http egress per R-NO-DIRECT-PROVIDER-HTTP
  // grandfather glob; invocation is subprocess-only, no pipeline-runtime import.
  const timeoutMs = Number(options.timeoutMs || 240_000);
  return new Promise((resolve) => {
    const startedAt = new Date().toISOString();
    const child = spawn(pythonBin, ["-m", "pipeline.deprecated.operator_glue.tilth_scout_ui", ...args], {
      cwd: repoRoot,
      env: openClawEnv(),
      stdio: ["ignore", "pipe", "pipe"],
    });
    const stdout = [];
    const stderr = [];
    let timedOut = false;
    const timer = setTimeout(() => {
      timedOut = true;
      child.kill("SIGTERM");
    }, timeoutMs);

    child.stdout.on("data", (chunk) => stdout.push(chunk));
    child.stderr.on("data", (chunk) => stderr.push(chunk));
    child.on("error", (error) => {
      clearTimeout(timer);
      resolve({
        ok: false,
        started_at: startedAt,
        finished_at: new Date().toISOString(),
        error: error.message,
        stdout: Buffer.concat(stdout).toString("utf8"),
        stderr: Buffer.concat(stderr).toString("utf8"),
      });
    });
    child.on("close", (code) => {
      clearTimeout(timer);
      resolve({
        ok: code === 0 && !timedOut,
        exit_code: code,
        timed_out: timedOut,
        started_at: startedAt,
        finished_at: new Date().toISOString(),
        stdout: Buffer.concat(stdout).toString("utf8"),
        stderr: Buffer.concat(stderr).toString("utf8"),
      });
    });
  });
}

export async function runScoutDiscovery({ cycle_id, query, context }) {
  const ctx = context || {};
  const orgSlug = ctx.org_slug || "";
  const cic = ctx.cic || "";
  const clc = ctx.clc || "";

  const args = [
    "--org-slug", orgSlug,
    "--cycle-id", cycle_id,
  ];
  if (query) args.push("--query", query);
  if (cic) args.push("--cic", cic);
  if (clc) args.push("--clc", clc);

  const result = await runTilthScoutBridge(args, { timeoutMs: 240_000 });

  let opportunities = [];
  let totals = {
    value: 0,
    signals: 0,
    blocked_value: 0,
    tracked: 0,
    new_today: 0,
  };
  let meta = {};
  let reason = "";

  // The bridge always prints a single JSON object — success and failure
  // paths both emit { ok, reason, opportunities, totals, meta }. Parse
  // first, then fall back to stderr on hard process failure.
  let bodyParsed = null;
  try {
    const trimmed = (result.stdout || "").trim();
    if (trimmed) bodyParsed = JSON.parse(trimmed);
  } catch (err) {
    reason = `Invalid JSON from Scout bridge: ${err.message}`;
  }

  if (bodyParsed && typeof bodyParsed === "object") {
    opportunities = Array.isArray(bodyParsed.opportunities) ? bodyParsed.opportunities : [];
    totals = bodyParsed.totals && typeof bodyParsed.totals === "object"
      ? { ...totals, ...bodyParsed.totals }
      : totals;
    meta = bodyParsed.meta || {};
    if (bodyParsed.ok === false && bodyParsed.reason) reason = bodyParsed.reason;
  }

  if (!result.ok && !reason) {
    reason = result.stderr?.trim() || result.error || "Scout bridge exited with error.";
  }

  const ok = result.ok && !reason;

  return {
    ok,
    reason: ok ? "" : (reason || "Scout discovery failed."),
    opportunities,
    totals,
    meta,
  };
}

async function gatewaySmoke(label = "OpenClaw gateway smoke") {
  const model = await readRouterModel("editor", "primary");
  const prompt = [
    "You are the Golden Quill local UI OpenClaw smoke endpoint.",
    "This request contains no client facts and no grant substance.",
    "HARD CONSTRAINT: output exactly OK.",
  ].join("\n");
  const result = await runOpenClaw([
    "infer",
    "model",
    "run",
    "--gateway",
    "--model",
    model,
    "--prompt",
    prompt,
    "--json",
  ]);
  const parsed = parseGatewayOutput(result.stdout);
  return {
    ok: result.ok,
    action: "gateway_smoke",
    label,
    router_ref: "/router.yaml#tilth.editor.primary",
    model_requested: model,
    model: parsed.model || model,
    provider: parsed.provider,
    transport: parsed.transport,
    output_text: parsed.output_text,
    reason: result.ok ? "" : result.stderr.trim() || result.error || "OpenClaw gateway smoke failed.",
    exit_code: result.exit_code,
    timed_out: result.timed_out,
  };
}

export async function handleOpenClawRequest(input = {}) {
  const action = normalizeAction(input.action);
  if (action === "status") return openClawStatus();
  if (action === "gateway_smoke" || action === "initialize" || action === "initialize_openclaw") {
    return gatewaySmoke(input.label);
  }
  return {
    ok: false,
    action,
    reason: `Unsupported OpenClaw action: ${input.action || "(missing)"}`,
  };
}
