import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";

const stagingRoot = process.argv[2];
const outputPath = process.argv[3];
if (!stagingRoot || !outputPath) {
  throw new Error("usage: build-material-package.mjs <staging-root> <output>");
}

const updateTargets = [
  "development/arcanum-addon/plan/DISPATCH.json",
  "development/arcanum-addon/plan/WORK-PACK.md",
  "development/arcanum-addon/plan/EXECUTION-PACK.md",
  "development/arcanum-addon/plan/work-pack/shared/CLOSEOUT-SYNC.md",
  "development/arcanum-addon/plan/DISPATCH-TECHNIQUE-TRACE.md",
  "development/arcanum-addon/plan/DISTILL-VALIDATION.md",
  "development/arcanum-addon/plan/PLAN-RESULT.json",
  "development/arcanum-addon/plan/PLAN-TRANSPORT.md"
];
const createTargets = [
  "development/arcanum-addon/plan/work-pack/shared/SWU-SELECTION-RECEIPT.schema.json",
  "development/arcanum-addon/plan/work-pack/shared/validate-swu-selection-reentry.mjs"
];
const targets = [...updateTargets, ...createTargets];

function exactRef(relativePath) {
  const bytes = fs.readFileSync(path.join(stagingRoot, relativePath));
  return {
    path: relativePath,
    sha256: crypto.createHash("sha256").update(bytes).digest("hex"),
    size_bytes: bytes.length
  };
}

const dependencies = updateTargets.map((target, index) => ({
  dependency_id: `preimage-${String(index + 1).padStart(2, "0")}`,
  artifact_ref: exactRef(`inputs/${target}`)
}));

const document = {
  schema_version: "1.0.0",
  package_id: "arcanum-addon-invoke-reentry-repair-20260730-v1",
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
  changes: targets.map((target) => ({
    target_path: target,
    operation: createTargets.includes(target) ? "create" : "update",
    output_ref: exactRef(`outputs/${target}`)
  })),
  target_inventory: targets.map((target) => ({
    target_path: target,
    lifecycle_owner: "resonantos-planning-owner",
    authority_class: "public",
    publication_class: "internal",
    dependency_ids: updateTargets.includes(target)
      ? [
          `preimage-${String(updateTargets.indexOf(target) + 1).padStart(
            2,
            "0"
          )}`
        ]
      : []
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
    "jq empty on all planning JSON",
    "python3 arcanum/formulae/dispatch-spec/scripts/validate-dispatch.py <staged DISPATCH.json>",
    "node development/arcanum-addon/plan/work-pack/shared/validate-swu-selection-reentry.mjs <staged plan root>",
    "node development/arcanum-addon/plan/work-pack/shared/validate-swu-selection-reentry.mjs --self-test",
    "node prior material/validate-markdown-links.mjs <overlay root> <changed markdown paths>",
    "git diff --no-index --check <staged inputs> <staged outputs>",
    "npm run docs:check",
    "npm run test:docs",
    "sorted absolute-path define/design/plan aggregate sha256sum"
  ]
};

fs.writeFileSync(outputPath, `${JSON.stringify(document, null, 2)}\n`);
