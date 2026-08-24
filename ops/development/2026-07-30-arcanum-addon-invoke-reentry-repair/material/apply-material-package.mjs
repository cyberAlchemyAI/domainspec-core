import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const packagePath = process.argv[2];
const packageRoot = process.argv[3];
const targetRoot = process.argv[4];
const receiptPath = process.argv[5];
const handoffPath = process.argv[6];
const outputReceiptPath = process.argv[7];
if (
  !packagePath ||
  !packageRoot ||
  !targetRoot ||
  !receiptPath ||
  !handoffPath ||
  !outputReceiptPath
) {
  throw new Error(
    "usage: apply-material-package.mjs <package> <package-root> <target-root> <receipt> <handoff> <output-receipt>"
  );
}

const document = JSON.parse(fs.readFileSync(packagePath, "utf8"));
const receipt = JSON.parse(fs.readFileSync(receiptPath, "utf8"));
const handoff = JSON.parse(fs.readFileSync(handoffPath, "utf8"));
const digest = (bytes) =>
  crypto.createHash("sha256").update(bytes).digest("hex");

if (
  receipt.patchVerdict !== "pass" ||
  receipt.mutationHandoff !== "ready" ||
  handoff.mutationReady !== true ||
  handoff.handoffStatus !== "ready" ||
  receipt.packageId !== document.package_id ||
  handoff.materialPackage.packageDigest !== receipt.packageDigest
) {
  throw new Error("material receipt or refresh handoff is not ready");
}

const dependencyById = new Map(
  document.dependencies.map((item) => [item.dependency_id, item])
);
const inventoryByTarget = new Map(
  document.target_inventory.map((item) => [item.target_path, item])
);
const preflight = [];
for (const change of document.changes) {
  const target = path.join(targetRoot, change.target_path);
  const output = path.join(packageRoot, change.output_ref.path);
  const outputBytes = fs.readFileSync(output);
  if (
    digest(outputBytes) !== change.output_ref.sha256 ||
    outputBytes.length !== change.output_ref.size_bytes
  ) {
    throw new Error(`staged output drift: ${change.target_path}`);
  }
  const inventory = inventoryByTarget.get(change.target_path);
  if (!inventory) throw new Error(`missing inventory: ${change.target_path}`);
  if (change.operation === "create") {
    if (fs.existsSync(target)) {
      const existing = fs.readFileSync(target);
      if (!existing.equals(outputBytes)) {
        throw new Error(`create target already exists with other bytes: ${change.target_path}`);
      }
      preflight.push({ target_path: change.target_path, state: "already-applied" });
    } else {
      preflight.push({ target_path: change.target_path, state: "absent-ready" });
    }
    continue;
  }
  if (inventory.dependency_ids.length !== 1) {
    throw new Error(`update target needs exactly one preimage: ${change.target_path}`);
  }
  const dependency = dependencyById.get(inventory.dependency_ids[0]);
  const targetBytes = fs.readFileSync(target);
  if (
    digest(targetBytes) !== dependency.artifact_ref.sha256 ||
    targetBytes.length !== dependency.artifact_ref.size_bytes
  ) {
    throw new Error(`target preimage drift: ${change.target_path}`);
  }
  preflight.push({ target_path: change.target_path, state: "preimage-match" });
}

const applied = [];
for (const change of document.changes) {
  const target = path.join(targetRoot, change.target_path);
  const output = path.join(packageRoot, change.output_ref.path);
  const outputBytes = fs.readFileSync(output);
  fs.mkdirSync(path.dirname(target), { recursive: true });
  if (!fs.existsSync(target) || !fs.readFileSync(target).equals(outputBytes)) {
    const temporary = `${target}.arcanum-material-${process.pid}.tmp`;
    fs.writeFileSync(temporary, outputBytes, { mode: 0o644, flag: "wx" });
    fs.renameSync(temporary, target);
  }
  const appliedBytes = fs.readFileSync(target);
  if (
    digest(appliedBytes) !== change.output_ref.sha256 ||
    appliedBytes.length !== change.output_ref.size_bytes
  ) {
    throw new Error(`post-apply mismatch: ${change.target_path}`);
  }
  applied.push({
    target_path: change.target_path,
    operation: change.operation,
    sha256: change.output_ref.sha256,
    size_bytes: change.output_ref.size_bytes
  });
}

const applyReceipt = {
  schema_version: "invoke.refresh.material-apply.v1",
  package_id: document.package_id,
  package_digest: receipt.packageDigest,
  target_root: targetRoot,
  preflight,
  applied,
  status: "pass"
};
fs.writeFileSync(outputReceiptPath, `${JSON.stringify(applyReceipt, null, 2)}\n`);
process.stdout.write(
  `applied and byte-verified ${applied.length} exact material targets\n`
);
