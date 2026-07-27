import { spawn, spawnSync, type ChildProcess } from "node:child_process";
import { mkdtempSync } from "node:fs";
import net from "node:net";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const BACKEND_DIR = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const TSX_PATH = join(
  BACKEND_DIR,
  "node_modules",
  ".bin",
  process.platform === "win32" ? "tsx.cmd" : "tsx",
);
const STUDIO_CLI_PATH = join(BACKEND_DIR, "src", "cli", "studio.ts");

/** A fresh, isolated STUDIO_DATA path per test (own dir ⇒ own artifacts root). */
export function newDataDir(): string {
  return join(mkdtempSync(join(tmpdir(), "ups-e2e-")), "studio.json");
}

export interface CliResult {
  command: string;
  args: string[];
  /** Compatibility view: failed commands include stderr, as before this repair. */
  stdout: string;
  /** Exact process stdout without the compatibility merge. */
  rawStdout: string;
  stderr: string;
  json: any;
  code: number;
  signal: NodeJS.Signals | null;
}

/** Run one studio CLI verb to completion via tsx; capture stdout JSON + exit code. */
export function cli(args: string[], dataDir: string): CliResult {
  const env = { ...process.env, STUDIO_DATA: dataDir, STUDIO_ACTOR: "agent:cycle" };
  const commandArgs = [STUDIO_CLI_PATH, ...args];
  const result = spawnSync(TSX_PATH, commandArgs, {
    cwd: BACKEND_DIR,
    env,
    encoding: "utf8",
  });
  const rawStdout = result.stdout ?? "";
  const stderr = [
    result.stderr ?? "",
    result.error ? `${result.error.name}: ${result.error.message}` : "",
  ].filter(Boolean).join("\n");
  const stdout = result.status === 0
    ? rawStdout
    : [rawStdout, stderr].filter(Boolean).join("");
  return {
    command: TSX_PATH,
    args: commandArgs,
    stdout,
    rawStdout,
    stderr,
    json: tryParse(rawStdout),
    code: result.status ?? 1,
    signal: result.signal,
  };
}

function tryParse(s: string): any {
  try { return JSON.parse(s.trim()); } catch { return null; }
}

/** Seed a baseline-ready session (variantCount 1, baseline A) from the given fixture. */
export function seedBaseline(dataDir: string, fixture = "e2e/fixtures/base.html"): string {
  const open = cli(["session", "open", "--variants", "1"], dataDir);
  const sid = open.json.sessionId as string;
  cli(["prompt", "submit", sid, "p"], dataDir);
  cli(["variants", "register", sid, "--label", "A", "--file", fixture], dataDir);
  cli(["baseline", "select", sid, "A"], dataDir);
  return sid;
}

/** Scaffolding: reach the RevisionApplied (staged) screen — a candidate is staged, head NOT advanced. */
export function seedStaged(dataDir: string): string {
  const sid = seedBaseline(dataDir);
  cli(["comment", "add", sid, "--od-id", "cta.primary", "--selector", "[data-od-id=cta.primary]", "--label", "Primary button", "--intent", "reword", "--note", "say Continue"], dataDir);
  const syn = cli(["synthesize", sid], dataDir);
  const batchId = syn.json.batch.batchId as string;
  cli(["batch", "approve", sid, batchId], dataDir);
  cli(["apply", sid, batchId, "--candidate-from", "e2e/fixtures/continue.html"], dataDir);
  return sid;
}

export async function freePort(): Promise<number> {
  return new Promise((resolve) => {
    const s = net.createServer();
    s.listen(0, "127.0.0.1", () => {
      const port = (s.address() as net.AddressInfo).port;
      s.close(() => resolve(port));
    });
  });
}

export interface PreviewHandle {
  url: string;
  port: number;
  stop(): void;
}

export interface PreviewStartOptions {
  cliPath?: string;
  startupTimeoutMs?: number;
}

function executionDiagnostic(
  reason: string,
  command: string,
  args: string[],
  code: number | null,
  signal: NodeJS.Signals | null,
  stdout: string,
  stderr: string,
): Error {
  return new Error([
    reason,
    `command: ${JSON.stringify([command, ...args])}`,
    `exit code: ${code === null ? "none" : code}`,
    `signal: ${signal ?? "none"}`,
    `stdout:\n${stdout || "(empty)"}`,
    `stderr:\n${stderr || "(empty)"}`,
  ].join("\n"));
}

/** Launch `studio preview` locally; resolve only after its session state route responds. */
export async function startPreview(
  sid: string,
  dataDir: string,
  options: PreviewStartOptions = {},
): Promise<PreviewHandle> {
  const port = await freePort();
  const commandArgs = [
    options.cliPath ?? STUDIO_CLI_PATH,
    "preview",
    sid,
    "--port",
    String(port),
  ];
  const proc: ChildProcess = spawn(TSX_PATH, commandArgs, {
    cwd: BACKEND_DIR,
    env: { ...process.env, STUDIO_DATA: dataDir },
  });
  await new Promise<void>((resolve, reject) => {
    let stdout = "";
    let stderr = "";
    let settled = false;
    const finish = (error?: Error) => {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      proc.off("error", onError);
      proc.off("exit", onExit);
      if (error) reject(error);
      else resolve();
    };
    const fail = (
      reason: string,
      code: number | null = proc.exitCode,
      signal: NodeJS.Signals | null = proc.signalCode,
    ) => finish(executionDiagnostic(
      reason,
      TSX_PATH,
      commandArgs,
      code,
      signal,
      stdout,
      stderr,
    ));
    const onError = (error: Error) => {
      stderr += `${stderr ? "\n" : ""}${error.name}: ${error.message}`;
      fail("preview process failed before readiness");
    };
    const onExit = (code: number | null, signal: NodeJS.Signals | null) => {
      fail("preview exited before readiness", code, signal);
    };
    const timer = setTimeout(() => {
      fail(`preview did not become ready within ${options.startupTimeoutMs ?? 30_000}ms`);
      if (proc.exitCode === null) proc.kill("SIGTERM");
    }, options.startupTimeoutMs ?? 30_000);
    proc.stdout?.on("data", (data) => { stdout += data.toString(); });
    proc.stderr?.on("data", (data) => { stderr += data.toString(); });
    proc.once("error", onError);
    proc.once("exit", onExit);
    void (async () => {
      const stateUrl = `http://127.0.0.1:${port}/state`;
      while (!settled) {
        try {
          const response = await fetch(stateUrl);
          if (response.ok) {
            finish();
            return;
          }
        } catch {
          // The listener may not be ready yet; the bounded timer owns failure.
        }
        await new Promise((next) => setTimeout(next, 50));
      }
    })();
  });
  return {
    url: `http://127.0.0.1:${port}/preview/${sid}`,
    port,
    stop: () => {
      if (proc.exitCode !== null) return;
      proc.kill("SIGTERM");
      const forceTimer = setTimeout(() => {
        if (proc.exitCode === null) proc.kill("SIGKILL");
      }, 2_000);
      forceTimer.unref();
      proc.once("exit", () => clearTimeout(forceTimer));
    },
  };
}
