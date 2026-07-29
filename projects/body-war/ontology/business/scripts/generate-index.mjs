import { readFile, readdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const packageRoot = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "..",
);
const nodeRoot = path.join(packageRoot, "nodes");

async function readJson(absolutePath) {
  return JSON.parse(await readFile(absolutePath, "utf8"));
}

const nodeNames = (await readdir(nodeRoot))
  .filter((name) => name.endsWith(".json") && name !== "manifest.json")
  .sort();
const nodes = await Promise.all(
  nodeNames.map((name) => readJson(path.join(nodeRoot, name))),
);
const receipt = await readJson(
  path.join(packageRoot, "receipts/validation-receipt.json"),
);

const byKind = new Map();
const byStatus = new Map();
for (const node of nodes) {
  byKind.set(node.business_kind, (byKind.get(node.business_kind) ?? 0) + 1);
  byStatus.set(
    node.candidate_status,
    (byStatus.get(node.candidate_status) ?? 0) + 1,
  );
}

const flowIds = [
  "body-war.business.actor.anonymous-visitor",
  "body-war.business.operation.authenticate-via-strava",
  "body-war.business.actor.connected-runner",
  "body-war.business.operation.select-suggested-track",
  "body-war.business.entity.suggested-track",
  "body-war.business.operation.confirm-track-with-activity",
  "body-war.business.entity.runner-confirmation",
  "body-war.business.entity.activity-evidence-candidate",
  "body-war.business.operation.fetch-selected-activity-geometry",
  "body-war.business.value.activity-geometry-sample",
  "body-war.business.operation.derive-geometry-candidate",
  "body-war.business.entity.geometry-candidate",
  "body-war.business.operation.build-score-input-snapshot",
  "body-war.business.value.score-input-snapshot",
  "body-war.business.operation.calculate-score-preview",
  "body-war.business.outcome.score-preview",
  "body-war.business.operation.project-score-preview",
];
const nodeById = new Map(nodes.map((node) => [node.concept_id, node]));

const lines = [
  "# Body War Business Ontology Node Index",
  "",
  "Status: `generated-projection`",
  "",
  "This is a human review projection. The individual JSON records in `nodes/`",
  "are the validated candidate node surface. This index has no authority effect.",
  "",
  "Start with [Business Ontology Views](BUSINESS-VIEWS.md) for arrow-based",
  "capability, journey, evidence, territory, progression, and lifecycle maps.",
  "Return here when you need the exhaustive node catalog.",
  "",
  "## Validation summary",
  "",
  `- Nodes: ${receipt.counts.nodes}`,
  `- Relations: ${receipt.counts.relations}`,
  `- Lifecycle policies: ${receipt.counts.lifecycle_policies}`,
  `- Residue items: ${receipt.counts.residue_items}`,
  `- Receipt status: \`${receipt.status}\``,
  `- Authority effect: \`${receipt.authority_effect}\``,
  "",
  "### Nodes by business kind",
  "",
  "| Business kind | Count |",
  "| --- | ---: |",
  ...[...byKind.entries()]
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([kind, count]) => `| \`${kind}\` | ${count} |`),
  "",
  "### Nodes by candidate status",
  "",
  "| Candidate status | Count |",
  "| --- | ---: |",
  ...[...byStatus.entries()]
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([status, count]) => `| \`${status}\` | ${count} |`),
  "",
  "## Login to ScorePreview chain",
  "",
  "| Step | Concept | Kind | Status | Resolution gate |",
  "| ---: | --- | --- | --- | --- |",
  ...flowIds.map((id, index) => {
    const node = nodeById.get(id);
    if (!node) throw new Error(`Missing flow node: ${id}`);
    const filename = `${id.replace("body-war.business.", "")}.json`;
    return `| ${index + 1} | [${node.label}](nodes/${filename}) | \`${node.business_kind}\` | \`${node.candidate_status}\` | \`${node.challenge_contract.resolution_gate}\` |`;
  }),
  "",
  "The blocked steps are intentionally present. A deterministic fixture can later",
  "exercise them only after its exact policy inputs are selected; real-provider",
  "geometry remains separately gated by privacy, scope, retention, and supervised",
  "evidence.",
  "",
  "## All nodes",
  "",
  "| Concept | Label | Kind | Role | Status | Evidence | Commitment |",
  "| --- | --- | --- | --- | --- | --- | --- |",
  ...nodes
    .sort(
      (a, b) =>
        a.business_kind.localeCompare(b.business_kind) ||
        a.concept_id.localeCompare(b.concept_id),
    )
    .map((node) => {
      const filename = `${node.concept_id.replace("body-war.business.", "")}.json`;
      return `| [\`${node.concept_id}\`](nodes/${filename}) | ${node.label} | \`${node.business_kind}\` | ${node.concept_role} | \`${node.candidate_status}\` | \`${node.confidence.evidence_confidence}\` | \`${node.confidence.commitment_confidence}\` |`;
    }),
  "",
];

await writeFile(
  path.join(packageRoot, "NODE-INDEX.md"),
  lines.join("\n"),
);
process.stdout.write(`generated node index for ${nodes.length} concepts\n`);
