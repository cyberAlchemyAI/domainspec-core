import { createHash } from "node:crypto";
import { mkdir, readFile, stat, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ONE_GO = path.resolve(fileURLToPath(new URL("../", import.meta.url)));
const REPO = path.resolve(ONE_GO, "../../../../../../../..");
const RUN = path.dirname(ONE_GO);
const MAP_PATH = path.join(ONE_GO, "material-map.json");
const SOURCE = path.join(ONE_GO, "material-source");
const GENERATED = path.join(ONE_GO, "generated");
const sha = (bytes) => createHash("sha256").update(bytes).digest("hex");
const canonicalize = (value) => Array.isArray(value) ? value.map(canonicalize) : value && typeof value === "object" ? Object.fromEntries(Object.keys(value).sort().map((key) => [key, canonicalize(value[key])])) : value;
const canonicalDigest = (value) => sha(JSON.stringify(canonicalize(value)));
const rel = (absolute) => path.relative(REPO, absolute).replaceAll(path.sep, "/");

const exact = async (relative, camel = false) => {
  const bytes = await readFile(path.join(REPO, relative));
  return camel ? { path: relative, sha256: sha(bytes), sizeBytes: bytes.length } : { path: relative, sha256: sha(bytes), size_bytes: bytes.length };
};
const sourceRef = async (relative) => ({ ...(await exact(relative)), authority_class: "private" });
const binding = async (id, owner, relative, selector = "") => ({ binding_id: id, owner_ref: owner, artifact_ref: await exact(relative), selector });
const writeJson = async (target, value) => { await mkdir(path.dirname(target), { recursive: true }); await writeFile(target, `${JSON.stringify(value, null, 2)}\n`); };

const targetState = async (relative) => {
  try {
    const bytes = await readFile(path.join(REPO, relative));
    return { state: "present", sha256: sha(bytes), size_bytes: bytes.length };
  } catch (error) {
    if (error.code === "ENOENT") return { state: "absent" };
    throw error;
  }
};

const applyReplacements = (text, replacements, target) => {
  let result = text;
  for (const replacement of replacements) {
    const count = result.split(replacement.find).length - 1;
    if (count !== 1) throw new Error(`${target}: replacement match count ${count}`);
    result = result.replace(replacement.find, replacement.replace);
  }
  return result;
};

const materialChange = async (unit, entry) => {
  if (entry.operation === "replace_text") {
    const beforeBytes = await readFile(path.join(REPO, entry.target_path));
    const after = applyReplacements(beforeBytes.toString("utf8"), entry.replacements, entry.target_path);
    return { target_path: entry.target_path, operation: "replace_text", before_sha256: sha(beforeBytes), after_sha256: sha(after), replacements: entry.replacements };
  }
  throw new Error(`${unit.unit_id}: unsupported explicit change ${entry.operation}`);
};

const build = async () => {
  const map = JSON.parse(await readFile(MAP_PATH, "utf8"));
  let priorPackagePath = null;
  const summary = [];
  for (const unit of map.units) {
    const unitDir = path.join(GENERATED, unit.unit_id);
    const receiptPath = rel(path.join(ONE_GO, "execution/receipts", `${unit.unit_id}.json`));
    const validationCommands = unit.validation_commands.map((argv) => JSON.stringify(argv));
    const changes = [];
    for (const sourceFile of unit.source_files ?? []) {
      const content = await readFile(path.join(SOURCE, sourceFile), "utf8");
      const targetPath = `${map.target_root}/${sourceFile}`;
      const before = await targetState(targetPath);
      if (before.state !== "absent") throw new Error(`${unit.unit_id}: create target already exists ${targetPath}`);
      changes.push({ target_path: targetPath, operation: "create_text", before_state: "absent", after_sha256: sha(content), content });
    }
    for (const entry of unit.changes ?? []) changes.push(await materialChange(unit, entry));
    const materialWrites = changes.map((change) => change.target_path).sort();
    const executionOutputs = [...unit.execution_outputs, receiptPath].sort();
    const allowedWrites = [...materialWrites, ...executionOutputs].sort();
    const context = {
      schema_version: "augmentor.consultation.task-context@0.1.0",
      task_id: unit.task_id,
      swu_id: unit.unit_id,
      strict_coverage: true,
      execution_contract: {
        writeProfile: "material-bound",
        materialWrites,
        executionOutputs,
        allowedWrites,
        validationCommands,
        lifecycleOwner: "augmentor-consultation-candidate-owner",
        authorityClass: "private",
        publicationClass: "private"
      },
      successor: unit.successor,
      stop_policy: "first-blocker-or-frontier-complete"
    };
    const contextPath = path.join(unitDir, "context-pack.json");
    await writeJson(contextPath, context);
    const controls = [
      { ...(await exact(unit.task_contract, true)), role: "task-contract", authorityClass: "private" },
      { ...(await exact(rel(path.join(RUN, "WORK-PACK.md")), true)), role: "work-pack", authorityClass: "private" },
      { ...(await exact(rel(contextPath), true)), role: "context-pack", authorityClass: "private" },
      { ...(await exact(rel(MAP_PATH), true)), role: "source", authorityClass: "private" }
    ];
    const packageSources = await Promise.all(controls.map(async (item) => ({ path: item.path, sha256: item.sha256, size_bytes: item.sizeBytes, authority_class: item.authorityClass })));
    const dependencies = priorPackagePath ? [{ dependency_id: unit.dependencies[0], artifact_ref: await exact(priorPackagePath) }] : [];
    const targetInventory = await Promise.all(changes.map(async (change) => ({ target_path: change.target_path, before: await targetState(change.target_path), after_sha256: change.after_sha256 })));
    const packageDoc = {
      schema_version: "augmentor.consultation.material-package@0.1.0",
      package_id: `material-${unit.unit_id.toLowerCase()}`,
      task_id: unit.task_id,
      swu_id: unit.unit_id,
      source_artifacts: packageSources,
      dependencies,
      changes,
      target_inventory: targetInventory,
      validation_commands: validationCommands,
      lifecycle_owner: "augmentor-consultation-candidate-owner",
      authority_class: "private",
      publication_class: "private"
    };
    const packagePath = path.join(unitDir, "material-package.json");
    await writeJson(packagePath, packageDoc);
    const producerReceipt = {
      schemaVersion: "augmentor.consultation.material-receipt@0.1.0",
      packageId: packageDoc.package_id,
      packageDigest: canonicalDigest(packageDoc),
      patchVerdict: "pass",
      mutationHandoff: "ready",
      dependencyResult: "pass",
      ownerBoundaryResult: "pass",
      publicationBoundaryResult: "pass",
      validatedPaths: materialWrites,
      validationCommands,
      lifecycleOwner: "augmentor-consultation-candidate-owner",
      authorityClass: "private",
      publicationClass: "private",
      reasons: []
    };
    const producerReceiptPath = path.join(unitDir, "producer-receipt.json");
    await writeJson(producerReceiptPath, producerReceipt);
    const targetInventoryPath = path.join(unitDir, "target-inventory.json");
    await writeJson(targetInventoryPath, { schema_version: "augmentor.consultation.target-inventory@0.1.0", unit_id: unit.unit_id, targets: targetInventory });
    const request = {
      schemaVersion: "1.2.0",
      executionMode: "reusable-mutation",
      taskId: unit.task_id,
      swuId: unit.unit_id,
      controlArtifacts: controls,
      dependencyFrontier: dependencies.map((dependency) => ({ dependencyId: dependency.dependency_id, artifactRef: { path: dependency.artifact_ref.path, sha256: dependency.artifact_ref.sha256, sizeBytes: dependency.artifact_ref.size_bytes } })),
      materialPackage: await exact(rel(packagePath), true),
      materialReceipt: await exact(rel(producerReceiptPath), true),
      producerReceiptSchema: await exact(rel(path.join(ONE_GO, "contracts/material-receipt.schema.json")), true),
      materialWrites,
      executionOutputs,
      allowedWrites,
      validationCommands,
      lifecycleOwner: "augmentor-consultation-candidate-owner",
      authorityClass: "private",
      publicationClass: "private"
    };
    const requestPath = path.join(unitDir, "mutation-admission-request.json");
    await writeJson(requestPath, request);
    const baselinePath = path.join(unitDir, "byte-baseline.json");
    await writeJson(baselinePath, { schema_version: "augmentor.consultation.absence-aware-baseline@0.1.0", unit_id: unit.unit_id, targets: targetInventory });
    summary.push({ unit_id: unit.unit_id, package_path: rel(packagePath), package_digest: producerReceipt.packageDigest, request_path: rel(requestPath), baseline_path: rel(baselinePath), material_writes: materialWrites, execution_outputs: executionOutputs, successor: unit.successor });
    priorPackagePath = rel(packagePath);
  }
  await writeJson(path.join(GENERATED, "material-summary.json"), { schema_version: "augmentor.consultation.material-summary@0.1.0", frontier: map.frontier, units: summary });
  console.log(`MATERIALS=prepared units=${summary.length}`);
};

await build();
