import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const targetRoot = process.argv[2];
const templatePath = process.argv[3];
const stagingRoot = process.argv[4];
const findingsPath = process.argv[5];
const packagePath = process.argv[6];
if (
  !targetRoot ||
  !templatePath ||
  !stagingRoot ||
  !findingsPath ||
  !packagePath
) {
  throw new Error(
    "usage: build-validator-path-repair.mjs <target-root> <template> <staging-root> <findings> <package>"
  );
}

const target =
  "development/arcanum-addon/plan/work-pack/shared/validate-swu-selection-reentry.mjs";
const ensureParent = (filePath) =>
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
const copy = (source, destination) => {
  ensureParent(destination);
  fs.copyFileSync(source, destination);
};
copy(
  path.join(targetRoot, target),
  path.join(stagingRoot, "inputs", target)
);
copy(templatePath, path.join(stagingRoot, "outputs", target));
copy(
  findingsPath,
  path.join(stagingRoot, "sources", "repair-revalidation-findings.md")
);

const exactRef = (relativePath) => {
  const bytes = fs.readFileSync(path.join(stagingRoot, relativePath));
  return {
    path: relativePath,
    sha256: crypto.createHash("sha256").update(bytes).digest("hex"),
    size_bytes: bytes.length
  };
};

const document = {
  schema_version: "1.0.0",
  package_id: "arcanum-addon-selection-path-repair-20260730-v2",
  mutation_mode: "apply-approved",
  mutation_state: "materialized",
  lifecycle_owner: "resonantos-planning-owner",
  authority_class: "public",
  publication_class: "internal",
  source_artifacts: [
    {
      ...exactRef("sources/repair-revalidation-findings.md"),
      authority_class: "private"
    }
  ],
  changes: [
    {
      target_path: target,
      operation: "update",
      output_ref: exactRef(`outputs/${target}`)
    }
  ],
  target_inventory: [
    {
      target_path: target,
      lifecycle_owner: "resonantos-planning-owner",
      authority_class: "public",
      publication_class: "internal",
      dependency_ids: ["preimage-01"]
    }
  ],
  dependencies: [
    {
      dependency_id: "preimage-01",
      artifact_ref: exactRef(`inputs/${target}`)
    }
  ],
  mirror_groups: [],
  approval: {
    class: "explicit-apply",
    owner: "resonantos-planning-owner",
    scope_paths: [target],
    authority_classes: ["public"],
    publication_classes: ["internal"]
  },
  validation_commands: [
    "node validate-swu-selection-reentry.mjs <plan-root>",
    "node validate-swu-selection-reentry.mjs --self-test",
    "runtime selection path/content mismatch rejection",
    "atomic single-use claim and replay rejection"
  ]
};
ensureParent(packagePath);
fs.writeFileSync(packagePath, `${JSON.stringify(document, null, 2)}\n`);
process.stdout.write("staged one-file selection-path validator repair\n");
