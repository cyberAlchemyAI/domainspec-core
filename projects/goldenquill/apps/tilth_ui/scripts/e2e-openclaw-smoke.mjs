import { spawn } from "node:child_process";
import { setTimeout as delay } from "node:timers/promises";
import { fileURLToPath } from "node:url";

const port = Number(process.env.PORT || 4197);
const baseUrl = `http://127.0.0.1:${port}`;
const appRoot = fileURLToPath(new URL("..", import.meta.url));

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

async function waitForServer() {
  const deadline = Date.now() + 20_000;
  while (Date.now() < deadline) {
    try {
      const response = await fetch(`${baseUrl}/api/projections/current`);
      if (response.ok) return;
    } catch {
      // Server is still starting.
    }
    await delay(250);
  }
  throw new Error(`Server did not become ready at ${baseUrl}`);
}

async function postJson(path, body) {
  const response = await fetch(`${baseUrl}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  const json = await response.json();
  return { response, json };
}

const server = spawn(process.execPath, ["server.mjs"], {
  cwd: appRoot,
  env: { ...process.env, PORT: String(port) },
  stdio: ["ignore", "pipe", "pipe"],
});

const serverOutput = [];
server.stdout.on("data", (chunk) => serverOutput.push(chunk.toString("utf8")));
server.stderr.on("data", (chunk) => serverOutput.push(chunk.toString("utf8")));

try {
  await waitForServer();

  const statusResponse = await fetch(`${baseUrl}/api/openclaw/status`);
  const status = await statusResponse.json();
  assert(statusResponse.ok && status.ok, `OpenClaw status failed: ${status.reason || JSON.stringify(status)}`);
  assert(String(status.version || "").includes("OpenClaw"), "OpenClaw version response did not include OpenClaw");

  const smoke = await postJson("/api/openclaw/run", { action: "gateway_smoke", label: "e2e live gateway smoke" });
  assert(smoke.response.ok && smoke.json.ok, `OpenClaw gateway smoke failed: ${smoke.json.reason || JSON.stringify(smoke.json)}`);
  assert(smoke.json.transport === "gateway", `OpenClaw smoke did not use gateway transport: ${JSON.stringify(smoke.json)}`);
  assert(smoke.json.output_text === "OK", `OpenClaw smoke output was not OK: ${JSON.stringify(smoke.json)}`);

  console.log(`Live OpenClaw gateway smoke OK.`);
} finally {
  server.kill("SIGTERM");
  await delay(250);
}
