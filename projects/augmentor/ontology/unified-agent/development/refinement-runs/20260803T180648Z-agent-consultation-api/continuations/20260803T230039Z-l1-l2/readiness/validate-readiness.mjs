import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { readFile, stat, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const RUN_ROOT = path.resolve(HERE, "../../..");
const WORKSPACE_ROOT = process.cwd();
const CONSUMER_ROOT = path.resolve(WORKSPACE_ROOT, "../workspace-resonant/2.0.0-alpha");
const EXPECTED_ORDER = [
  "SWU-ACAPI-007",
  "SWU-ACAPI-008",
  "SWU-ACAPI-009",
  "SWU-ACAPI-010",
  "SWU-ACAPI-013",
  "SWU-ACAPI-011",
];

const sha256 = (bytes) => createHash("sha256").update(bytes).digest("hex");
const readJson = async (target) => JSON.parse(await readFile(target, "utf8"));
const git = (...args) => execFileSync("git", args, {
  cwd: CONSUMER_ROOT,
  encoding: "utf8",
}).trim();

async function isAbsent(target) {
  try {
    await stat(target);
    return false;
  } catch (error) {
    if (error?.code === "ENOENT") return true;
    throw error;
  }
}

const checks = [];
function check(id, passed, evidence) {
  checks.push({ id, status: passed ? "pass" : "fail", evidence });
}

const baseline = await readJson(path.join(HERE, "CONSUMER-BASELINE.json"));
const frontier = await readJson(path.join(HERE, "L1-L2-FRONTIER.json"));
const contextPack = await readJson(path.join(HERE, "SWU-ACAPI-007-CONTEXT-PACK.json"));
const hostReceipt = await readJson(path.join(HERE, "../decision/host-route-option-admissibility-receipt.json"));
const projectionReceipt = await readJson(path.join(HERE, "../decision/projection-policy-option-admissibility-receipt.json"));
const l0Approval = await readJson(path.join(RUN_ROOT, "one-go/decision/decision-gate-approval-receipt.json"));
const l0Completion = await readJson(path.join(RUN_ROOT, "one-go/execution/completion-receipt.json"));

check("consumer-head", git("rev-parse", "HEAD") === baseline.head, git("rev-parse", "HEAD"));
check("consumer-branch", git("branch", "--show-current") === baseline.branch, git("branch", "--show-current"));
check("consumer-clean", git("status", "--porcelain") === "", git("status", "--porcelain") || "clean");

for (const item of baseline.trackedBaselines) {
  const bytes = await readFile(path.join(CONSUMER_ROOT, item.path));
  check(`baseline:${item.path}`, sha256(bytes) === item.sha256, sha256(bytes));
}

for (const target of baseline.absentTargets) {
  check(`absent:${target}`, await isAbsent(path.join(CONSUMER_ROOT, target)), "expected absent");
}

check(
  "frontier-order",
  JSON.stringify(frontier.executionOrder) === JSON.stringify(EXPECTED_ORDER),
  frontier.executionOrder.join(" -> "),
);
check(
  "frontier-unexecutable",
  frontier.nextExecutableUnit === null && frontier.nextGate === "DG-L12-001",
  `next=${frontier.nextExecutableUnit}; gate=${frontier.nextGate}`,
);
check(
  "host-decision-gate",
  hostReceipt.routeOutcome === "gate" && hostReceipt.decisionGateRequired === true,
  `${hostReceipt.routeOutcome}:${hostReceipt.admissibleOptionIds.join(",")}`,
);
check(
  "projection-decision-gate",
  projectionReceipt.routeOutcome === "gate" && projectionReceipt.decisionGateRequired === true,
  `${projectionReceipt.routeOutcome}:${projectionReceipt.admissibleOptionIds.join(",")}`,
);
check(
  "context-blocks-runtime",
  contextPack.strictCoverage === "block" && contextPack.runtimeHandoffReady === false,
  `${contextPack.strictCoverage}:${contextPack.runtimeHandoffReady}`,
);
check(
  "old-epoch-excludes-l1",
  l0Approval.constraints?.l1_or_later === false &&
    l0Approval.epoch_binding?.finite_frontier?.at(-1) === "SWU-ACAPI-006",
  `${l0Approval.epoch_binding?.epoch_id}:${l0Approval.constraints?.l1_or_later}`,
);
check(
  "l0-complete",
  l0Completion.status === "COMPLETE" && l0Completion.epoch_id === l0Approval.epoch_binding.epoch_id,
  `${l0Completion.status}:${l0Completion.epoch_id}`,
);

const failed = checks.filter((item) => item.status === "fail");
const result = {
  schemaVersion: "augmentor.consultation.readiness-validation@0.1.0",
  validatedAt: new Date().toISOString(),
  validationStatus: failed.length === 0 ? "pass" : "fail",
  executionReady: false,
  executionReadyReason: failed.length
    ? "Readiness evidence drifted or failed validation."
    : "Evidence is current, but two protected owner decisions plus material, admission, and a new exact epoch remain open.",
  checkCount: checks.length,
  passCount: checks.length - failed.length,
  failCount: failed.length,
  checks,
  nextRoute: failed.length ? "invoke:refresh" : "decision-gate:DG-L12-001",
  mutationAuthority: false,
};

const rendered = `${JSON.stringify(result, null, 2)}\n`;
const outputIndex = process.argv.indexOf("--output");
if (outputIndex >= 0) {
  const outputPath = process.argv[outputIndex + 1];
  if (!outputPath) throw new Error("--output requires a path");
  await writeFile(path.resolve(outputPath), rendered, "utf8");
} else {
  process.stdout.write(rendered);
}

if (failed.length) process.exitCode = 1;
