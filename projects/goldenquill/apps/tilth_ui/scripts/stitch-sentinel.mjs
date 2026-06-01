import { watch } from "node:fs";
import { spawn } from "node:child_process";
import { mkdir, writeFile, cp } from "node:fs/promises";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const appRoot = fileURLToPath(new URL("..", import.meta.url));
const stitchDir = join(appRoot, "stitch_tilth_os_institutional_shell 3");
const reportsDir = join(appRoot, "reports", "stitch-sentinel");
const quarantineDir = join(appRoot, "quarantine", "stitch-failed-builds");

let debounceTimeout = null;
let isRunning = false;

async function runCommand(cmd, args) {
  return new Promise((resolve) => {
    const proc = spawn(cmd, args, { cwd: appRoot, shell: true });
    let stdout = "";
    let stderr = "";
    proc.stdout.on("data", (data) => (stdout += data.toString()));
    proc.stderr.on("data", (data) => (stderr += data.toString()));
    proc.on("close", (code) => {
      resolve({ code, stdout, stderr });
    });
  });
}

async function runTests() {
  if (isRunning) return;
  isRunning = true;
  
  console.log("\n[Sentinel] Change detected. Running firewall tests...");
  await mkdir(reportsDir, { recursive: true });
  await mkdir(quarantineDir, { recursive: true });

  const tests = [
    { name: "verify:static", cmd: "npm", args: ["run", "verify:static"] },
    { name: "stress:fail-closed", cmd: "npm", args: ["run", "stress:fail-closed"] },
    { name: "doctrine:lint", cmd: "npm", args: ["run", "doctrine:lint"] }
  ];

  let failed = false;
  let reportLog = "# Stitch Sentinel Firewall Report\n\nDate: " + new Date().toISOString() + "\n\n";

  for (const test of tests) {
    console.log(`[Sentinel] Running ${test.name}...`);
    const result = await runCommand(test.cmd, test.args);
    
    reportLog += `## ${test.name}\n`;
    reportLog += `Exit Code: ${result.code}\n\n\`\`\`\n${result.stdout}\n${result.stderr}\n\`\`\`\n\n`;

    if (result.code !== 0) {
      console.error(`[Sentinel] ❌ ${test.name} FAILED!`);
      failed = true;
    } else {
      console.log(`[Sentinel] ✅ ${test.name} PASSED.`);
    }
  }

  const latestMdPath = join(reportsDir, "latest.md");
  const latestJsonPath = join(reportsDir, "latest.json");
  
  await writeFile(latestMdPath, reportLog);
  await writeFile(latestJsonPath, JSON.stringify({ timestamp: Date.now(), failed }, null, 2));

  if (failed) {
    const timestamp = new Date().toISOString().replace(/[:.]/g, "-");
    const quarantineTarget = join(quarantineDir, timestamp);
    console.log(`[Sentinel] 🚨 Firewall breached! Quarantining build to ${quarantineTarget}`);
    await cp(stitchDir, quarantineTarget, { recursive: true });
  } else {
    console.log("[Sentinel] 🛡️ All checks passed. Build authorized.");
  }

  isRunning = false;
}

console.log(`[Sentinel] Watching ${stitchDir} for changes...`);
watch(stitchDir, { recursive: true }, (eventType, filename) => {
  if (filename && !filename.includes(".tmp") && !filename.includes(".git")) {
    if (debounceTimeout) clearTimeout(debounceTimeout);
    debounceTimeout = setTimeout(() => {
      runTests().catch(console.error);
    }, 1000);
  }
});
