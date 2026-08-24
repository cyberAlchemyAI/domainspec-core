import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const stagingRoot = process.argv[2];
const outputPath = process.argv[3];
if (!stagingRoot || !outputPath) {
  throw new Error("usage: build-material-package.mjs <staging-root> <output>");
}

const targets = [
  "development/arcanum-addon/plan/DISPATCH.json",
  "development/arcanum-addon/design/VALIDATION-CONTRACTS.md",
  "development/arcanum-addon/plan/work-pack/tasks/TASK-4-LIFECYCLE-ACCEPTANCE.md",
  "development/arcanum-addon/plan/work-pack/shared/CLOSEOUT-SYNC.md",
  "development/arcanum-addon/plan/WORK-PACK.md",
  "development/arcanum-addon/design/DISTILL-VALIDATION.md",
  "development/arcanum-addon/plan/DISTILL-VALIDATION.md",
  "development/arcanum-addon/design/DESIGN-RESULT.json",
  "development/arcanum-addon/plan/PLAN-RESULT.json"
];

function exactRef(relativePath) {
  const bytes = fs.readFileSync(path.join(stagingRoot, relativePath));
  return {
    path: relativePath,
    sha256: crypto.createHash("sha256").update(bytes).digest("hex"),
    size_bytes: bytes.length
  };
}

const dependencies = targets.map((target, index) => ({
  dependency_id: `preimage-${String(index + 1).padStart(2, "0")}`,
  artifact_ref: exactRef(`inputs/${target}`)
}));

const dependencyByTarget = new Map(
  targets.map((target, index) => [
    target,
    `preimage-${String(index + 1).padStart(2, "0")}`
  ])
);

const document = {
  schema_version: "1.0.0",
  package_id: "arcanum-addon-invoke-repair-20260730-v1",
  mutation_mode: "apply-approved",
  mutation_state: "materialized",
  lifecycle_owner: "resonantos-planning-owner",
  authority_class: "public",
  publication_class: "internal",
  source_artifacts: [
    {
      ...exactRef("sources/revalidation-findings.md"),
      authority_class: "private"
    },
    {
      ...exactRef("sources/route-shape-admissibility-receipt.json"),
      authority_class: "private"
    }
  ],
  changes: targets.map((target) => ({
    target_path: target,
    operation: "update",
    output_ref: exactRef(`outputs/${target}`)
  })),
  target_inventory: targets.map((target) => ({
    target_path: target,
    lifecycle_owner: "resonantos-planning-owner",
    authority_class: "public",
    publication_class: "internal",
    dependency_ids: [dependencyByTarget.get(target)]
  })),
  dependencies,
  mirror_groups: [],
  approval: {
    class: "explicit-apply",
    owner: "resonantos-planning-owner",
    scope_paths: targets,
    authority_classes: ["public"],
    publication_classes: ["internal"]
  },
  validation_commands: [
    "jq empty on changed JSON outputs",
    "python3 arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py <staged DISPATCH.json>",
    "node material/validate-repair.mjs <staged output root>",
    "node material/validate-markdown-links.mjs <overlay root> <changed markdown paths>",
    "git diff --no-index --check <staged inputs> <staged outputs>",
    "npm run docs:check",
    "npm run test:docs",
    "sorted absolute-path define/design/plan aggregate sha256sum"
  ]
};

fs.writeFileSync(outputPath, `${JSON.stringify(document, null, 2)}\n`);
