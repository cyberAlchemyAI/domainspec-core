import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

const ONE_GO = path.resolve(fileURLToPath(new URL("../", import.meta.url)));
const REPO = path.resolve(ONE_GO, "../../../../../../../..");
const TERMINAL_SCHEMA = path.join(ONE_GO, "contracts/terminal-receipt.schema.json");
const TERMINAL_VALIDATOR = path.join(ONE_GO, "scripts/validate-terminal-receipt.mjs");
const TRANSITION_SCHEMA = path.join(REPO, ".agents/skills/task-session-until-blocker/schemas/chain-transition.schema.json");
const CHAIN_RUNNER = path.join(REPO, ".agents/skills/task-session-until-blocker/scripts/run_chain.py");
const WORK_PACK = path.resolve(ONE_GO, "../WORK-PACK.md");

const sha = (bytes) => createHash("sha256").update(bytes).digest("hex");
const arg = (name) => {
  const index = process.argv.indexOf(name);
  return index >= 0 ? process.argv[index + 1] : null;
};
const has = (name) => process.argv.includes(name);
const fail = (errors) => {
  console.log(JSON.stringify({
    status: "BLOCK",
    terminal_code: "TRANSITION_RECEIPT_JOIN_INVALID",
    claim: "transition receipts were not joined to their exact bytes",
    errors,
    authority_effect: "none"
  }, null, 2));
  process.exit(2);
};
const resolveInsideRepo = (rawPath) => {
  if (typeof rawPath !== "string" || rawPath.length === 0 || path.isAbsolute(rawPath)) {
    throw new Error(`unsafe artifact path: ${String(rawPath)}`);
  }
  const absolute = path.resolve(REPO, rawPath);
  const relative = path.relative(REPO, absolute);
  if (relative.startsWith("..") || path.isAbsolute(relative)) throw new Error(`artifact escapes repository: ${rawPath}`);
  return absolute;
};
const exactBytes = async (reference, label) => {
  if (!reference || typeof reference !== "object") throw new Error(`${label} reference missing`);
  const absolute = resolveInsideRepo(reference.path);
  const bytes = await readFile(absolute);
  if (sha(bytes) !== reference.sha256) throw new Error(`${label} digest mismatch`);
  if (Object.hasOwn(reference, "size_bytes") && bytes.length !== reference.size_bytes) throw new Error(`${label} size mismatch`);
  return { absolute, bytes };
};
const sameRef = (left, right) => Boolean(
  left && right && left.path === right.path && left.sha256 === right.sha256
);
const canonical = (value) => {
  if (Array.isArray(value)) return `[${value.map(canonical).join(",")}]`;
  if (value && typeof value === "object") {
    return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${canonical(value[key])}`).join(",")}}`;
  }
  return JSON.stringify(value);
};
const validateSchema = (schemaPath, instancePath, label) => {
  const code = [
    "import json, sys",
    "from jsonschema import Draft202012Validator",
    "schema = json.load(open(sys.argv[1], encoding='utf-8'))",
    "instance = json.load(open(sys.argv[2], encoding='utf-8'))",
    "errors = sorted(Draft202012Validator(schema).iter_errors(instance), key=lambda e: list(e.absolute_path))",
    "print('\\n'.join(f'{list(e.absolute_path)}: {e.message}' for e in errors))",
    "raise SystemExit(1 if errors else 0)"
  ].join("\n");
  const result = spawnSync("python3", ["-c", code, schemaPath, instancePath], { cwd: REPO, encoding: "utf8" });
  if (result.status !== 0) throw new Error(`${label} schema invalid: ${(result.stdout || result.stderr || "unknown error").trim()}`);
};

const configArg = arg("--config");
const transitionArg = arg("--transition");
if (!configArg || !transitionArg) fail(["--config and --transition are required"]);

const configPath = path.resolve(REPO, configArg);
const transitionPath = path.resolve(REPO, transitionArg);
const errors = [];
let transition;
let receipt;
let receiptPath;

try {
  validateSchema(TRANSITION_SCHEMA, transitionPath, "transition");
  transition = JSON.parse(await readFile(transitionPath, "utf8"));
  const terminal = await exactBytes(transition.terminal_receipt_ref, "normalized terminal receipt");
  receiptPath = terminal.absolute;
  receipt = JSON.parse(terminal.bytes.toString("utf8"));
  validateSchema(TERMINAL_SCHEMA, receiptPath, "normalized terminal receipt");
} catch (error) {
  errors.push(error.message);
}

if (transition && receipt) {
  const expectedStatus = transition.task_session_result.toLowerCase();
  if (receipt.unit_id !== transition.selector) errors.push("normalized terminal unit differs from transition selector");
  if (receipt.status !== expectedStatus) errors.push("normalized terminal status differs from transition result");
  if (receipt.continuity_cursor !== transition.cursor) errors.push("normalized terminal cursor differs from transition cursor");
  if (receipt.successor !== transition.successor.unit_id) errors.push("normalized terminal successor differs from transition successor");

  try {
    await exactBytes(receipt.task_session_terminal_ref, "Task Session terminal receipt");
    await exactBytes(receipt.closeout_owner_ref, "closeout owner receipt");
    await exactBytes(receipt.router_verification_ref, "Continuation Router verification receipt");
  } catch (error) {
    errors.push(error.message);
  }

  if (transition.closeout.result === "PASS") {
    if (!sameRef(receipt.closeout_owner_ref, transition.closeout.owner_receipt_ref)) errors.push("PASS closeout owner receipt differs from normalized terminal join");
    if (!sameRef(receipt.router_verification_ref, transition.closeout.continuation_router_verification_receipt_ref)) errors.push("PASS Router verification differs from normalized terminal join");
  } else if (transition.closeout.result === "NO_OP") {
    if (transition.closeout.owner_receipt_ref !== null) errors.push("NO_OP transition must not carry an owner receipt reference");
    if (!sameRef(receipt.router_verification_ref, transition.closeout.continuation_router_verification_receipt_ref)) errors.push("NO_OP Router verification differs from normalized terminal join");
    try {
      const proofBytes = await exactBytes(receipt.closeout_owner_ref, "NO_OP proof receipt");
      const proof = JSON.parse(proofBytes.bytes.toString("utf8"));
      if (canonical(proof) !== canonical(transition.closeout.no_op_proof)) errors.push("inline NO_OP proof differs from its normalized receipt bytes");
    } catch (error) {
      errors.push(error.message);
    }
  }

  const expectedSuccessor = receipt.successor === null ? "__complete__" : receipt.successor;
  const semantic = spawnSync("node", [
    TERMINAL_VALIDATOR,
    "--receipt", receiptPath,
    "--unit", transition.selector,
    "--successor", expectedSuccessor,
    "--work-pack", WORK_PACK
  ], { cwd: REPO, encoding: "utf8" });
  if (semantic.status !== 0) errors.push(`terminal receipt semantics failed: ${(semantic.stdout || semantic.stderr || "unknown error").trim()}`);
}

if (errors.length) fail(errors);

if (has("--validate-only")) {
  console.log(JSON.stringify({
    status: "PASS",
    terminal_code: "TRANSITION_RECEIPTS_JOINED",
    selector: transition.selector,
    claim: "transition and normalized Task Session, closeout, and Router receipts resolve to exact joined bytes",
    canonical_runner_invoked: false,
    authority_effect: "none"
  }, null, 2));
  process.exit(0);
}

const chain = spawnSync("python3", [CHAIN_RUNNER, "--config", configPath, "--transition", transitionPath], {
  cwd: REPO,
  stdio: "inherit"
});
if (chain.error) throw chain.error;
process.exit(chain.status ?? 2);
