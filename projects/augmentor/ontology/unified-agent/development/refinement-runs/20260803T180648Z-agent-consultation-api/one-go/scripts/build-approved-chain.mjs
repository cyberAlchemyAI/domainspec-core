import { createHash } from "node:crypto";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const ONE_GO = path.resolve(fileURLToPath(new URL("../", import.meta.url)));
const REPO = path.resolve(ONE_GO, "../../../../../../../..");
const MANIFEST = path.join(ONE_GO, "audit/results-v2-execution-ready/objective-execution-manifest.json");
const APPROVAL_SCHEMA = path.join(ONE_GO, "contracts/decision-gate-approval-receipt.schema.json");
const CHAIN_SCHEMA = path.join(REPO, ".agents/skills/task-session-until-blocker/schemas/chain-config.schema.json");
const sha = (bytes) => createHash("sha256").update(bytes).digest("hex");
const arg = (name) => {
  const index = process.argv.indexOf(name);
  return index >= 0 ? process.argv[index + 1] : null;
};
const fail = (errors) => {
  console.log(JSON.stringify({ status: "BLOCK", terminal_code: "APPROVED_CHAIN_CONFIG_INVALID", errors, authority_effect: "none" }, null, 2));
  process.exit(2);
};
const relativeInsideRepo = (absolute) => {
  const relative = path.relative(REPO, absolute).replaceAll(path.sep, "/");
  if (!relative || relative.startsWith("../") || path.isAbsolute(relative)) throw new Error(`path escapes repository: ${absolute}`);
  return relative;
};
const exact = async (absolute) => {
  const bytes = await readFile(absolute);
  return { path: relativeInsideRepo(absolute), sha256: sha(bytes), size_bytes: bytes.length };
};
const validateSchema = (schemaPath, instancePath, label) => {
  const code = [
    "import json, sys",
    "from jsonschema import Draft202012Validator, FormatChecker",
    "schema = json.load(open(sys.argv[1], encoding='utf-8'))",
    "instance = json.load(open(sys.argv[2], encoding='utf-8'))",
    "errors = sorted(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(instance), key=lambda e: list(e.absolute_path))",
    "print('\\n'.join(f'{list(e.absolute_path)}: {e.message}' for e in errors))",
    "raise SystemExit(1 if errors else 0)"
  ].join("\n");
  const result = spawnSync("python3", ["-c", code, schemaPath, instancePath], { cwd: REPO, encoding: "utf8" });
  if (result.status !== 0) throw new Error(`${label} schema invalid: ${(result.stdout || result.stderr || "unknown error").trim()}`);
};

const approvalArg = arg("--approval-receipt");
const outputArg = arg("--output");
if (!approvalArg) fail(["--approval-receipt is required"]);
const approvalPath = path.resolve(REPO, approvalArg);
const outputPath = outputArg ? path.resolve(REPO, outputArg) : path.join(ONE_GO, "execution/chain-config.json");

try {
  relativeInsideRepo(approvalPath);
  relativeInsideRepo(outputPath);
  validateSchema(APPROVAL_SCHEMA, approvalPath, "Decision Gate approval receipt");
  const [approval, manifest] = await Promise.all([
    readFile(approvalPath, "utf8").then(JSON.parse),
    readFile(MANIFEST, "utf8").then(JSON.parse)
  ]);
  const epoch = manifest.epoch_binding;
  const approved = approval.epoch_binding;
  const comparisons = [
    ["epoch_id", approved.epoch_id, epoch.epoch_id],
    ["audit_projection_digest", approved.audit_projection_digest, epoch.audit_projection_digest],
    ["canonical_semantic_digest", approved.canonical_semantic_digest, epoch.canonical_semantic_digest],
    ["source_snapshot_digest", approved.source_snapshot_digest, epoch.source_snapshot_digest],
    ["finite_frontier", JSON.stringify(approved.finite_frontier), JSON.stringify(epoch.approved_frontier_ref)],
    ["run_budget", approved.run_budget, epoch.run_budget.max_task_session_requests]
  ];
  const mismatches = comparisons.filter(([, left, right]) => left !== right).map(([name]) => `${name} differs from audited epoch`);
  if (mismatches.length) fail(mismatches);
  if (manifest.authority_effect !== "none" || manifest.mutation_ready !== false || manifest.selected_unit !== null) fail(["manifest authority ceiling is invalid"]);

  const chain = {
    schema_version: "1.0.0",
    chain_id: `augmentor-consultation-l0-${epoch.epoch_id.slice(-8)}`,
    repository_root: ".",
    state_directory: relativeInsideRepo(path.join(ONE_GO, "execution/chain-state")),
    scope_id: relativeInsideRepo(path.resolve(ONE_GO, "..")),
    manifest_ref: await exact(MANIFEST),
    audit_verdict: "pass",
    audit_flags: [],
    approved_epoch: {
      epoch_id: epoch.epoch_id,
      audit_projection_digest: epoch.audit_projection_digest,
      canonical_semantic_digest: epoch.canonical_semantic_digest,
      source_snapshot_digest: epoch.source_snapshot_digest,
      decision_gate_approval_receipt_ref: await exact(approvalPath),
      approval_owner_ref: approval.approval_owner,
      approval_status: approval.approval_status
    },
    finite_frontier: epoch.approved_frontier_ref,
    run_budget: epoch.run_budget,
    risk_ceiling: approved.risk_ceiling,
    allowed_task_session_flags: [],
    persistence: { mode: "append-only-hash-chain", collision_policy: "exclusive-create" },
    compensation: { mode: "none", rationale: "Stop at the first blocker and preserve validated candidate-local bytes; do not roll back automatically." }
  };
  await mkdir(path.dirname(outputPath), { recursive: true });
  await writeFile(outputPath, `${JSON.stringify(chain, null, 2)}\n`, { flag: "wx", mode: 0o600 });
  try {
    validateSchema(CHAIN_SCHEMA, outputPath, "chain configuration");
  } catch (error) {
    await import("node:fs/promises").then(({ unlink }) => unlink(outputPath));
    throw error;
  }
  const outputRef = await exact(outputPath);
  console.log(JSON.stringify({ status: "PASS", terminal_code: "APPROVED_CHAIN_CONFIG_READY", chain_config_ref: outputRef, next_route: "task-session-until-blocker:preflight", authority_effect: "none" }, null, 2));
} catch (error) {
  fail([error.message]);
}
