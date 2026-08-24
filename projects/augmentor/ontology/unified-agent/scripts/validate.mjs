import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const PACKAGE_ROOT = path.resolve(fileURLToPath(new URL("../", import.meta.url)));
const REPOSITORY_ROOT = path.resolve(PACKAGE_ROOT, "../../../..");

const FILES = {
  profile: "profile.json",
  sources: "sources.json",
  nodes: "nodes/nodes.json",
  relations: "relations/relations.json",
  residue: "residue.json",
  receipt: "receipts/validation-receipt.json",
  nodeSchema: "schemas/node.schema.json",
  relationSchema: "schemas/relation.schema.json",
  viewSchema: "schemas/view.schema.json"
};

const sha256 = (bytes) => createHash("sha256").update(bytes).digest("hex");

const readBytes = (relativePath) => readFile(path.join(PACKAGE_ROOT, relativePath));

const readJson = async (relativePath) => JSON.parse(await readFile(path.join(PACKAGE_ROOT, relativePath), "utf8"));

const unique = (values) => values.length === new Set(values).size;

const push = (errors, at, message) => errors.push(`${at}: ${message}`);

const validateClosedSchema = (value, schema, at, errors) => {
  if (schema.const !== undefined && value !== schema.const) {
    push(errors, at, `must equal ${JSON.stringify(schema.const)}`);
    return;
  }
  if (schema.enum && !schema.enum.includes(value)) {
    push(errors, at, `must be one of ${schema.enum.join(", ")}`);
    return;
  }

  if (schema.type === "object") {
    if (!value || typeof value !== "object" || Array.isArray(value)) {
      push(errors, at, "must be an object");
      return;
    }
    for (const key of schema.required ?? []) {
      if (!(key in value)) push(errors, `${at}.${key}`, "is required");
    }
    if (schema.additionalProperties === false) {
      const allowed = new Set(Object.keys(schema.properties ?? {}));
      for (const key of Object.keys(value)) {
        if (!allowed.has(key)) push(errors, `${at}.${key}`, "is not allowed");
      }
    }
    for (const [key, propertySchema] of Object.entries(schema.properties ?? {})) {
      if (key in value) validateClosedSchema(value[key], propertySchema, `${at}.${key}`, errors);
    }
    return;
  }

  if (schema.type === "array") {
    if (!Array.isArray(value)) {
      push(errors, at, "must be an array");
      return;
    }
    if (schema.minItems !== undefined && value.length < schema.minItems) {
      push(errors, at, `must contain at least ${schema.minItems} item(s)`);
    }
    if (schema.uniqueItems && !unique(value.map((item) => JSON.stringify(item)))) {
      push(errors, at, "must contain unique items");
    }
    if (schema.items) {
      value.forEach((item, index) => validateClosedSchema(item, schema.items, `${at}[${index}]`, errors));
    }
    return;
  }

  if (schema.type === "string") {
    if (typeof value !== "string") {
      push(errors, at, "must be a string");
      return;
    }
    if (schema.minLength !== undefined && value.length < schema.minLength) {
      push(errors, at, `must have length >= ${schema.minLength}`);
    }
    if (schema.pattern && !new RegExp(schema.pattern).test(value)) {
      push(errors, at, `must match ${schema.pattern}`);
    }
  }
};

export const validateRelationBoundary = (relation) => {
  const errors = [];
  if (relation.authority_effect !== "none") {
    errors.push("project relations must retain authority_effect none");
  }
  if (relation.value_effect === "value-constraining" && relation.cycle_policy === "cycle-permitted") {
    errors.push("value-constraining cycle-permitted relation requires a separately governed exception");
  }
  if (!Array.isArray(relation.forbidden_collapse) || relation.forbidden_collapse.length === 0) {
    errors.push("relation must declare at least one forbidden collapse");
  }
  return errors;
};

export const validateSourceRecord = async (source, repositoryRoots) => {
  const errors = [];
  const repository = repositoryRoots[source.repository];
  if (!repository) return [`unknown repository root ${source.repository}`];
  if (path.isAbsolute(source.path) || source.path.split(path.sep).includes("..")) {
    return ["source path must be repository-relative and cannot traverse upward"];
  }
  const root = path.resolve(REPOSITORY_ROOT, repository.path);
  const target = path.resolve(root, source.path);
  if (target !== root && !target.startsWith(`${root}${path.sep}`)) {
    return ["resolved source escapes its declared repository root"];
  }
  let bytes;
  try {
    bytes = await readFile(target);
  } catch (error) {
    return [`cannot read ${target}: ${error.message}`];
  }
  const actual = sha256(bytes);
  if (actual !== source.sha256) errors.push(`digest mismatch: expected ${source.sha256}, got ${actual}`);
  return errors;
};

export const validatePackage = async () => {
  const errors = [];
  const [
    profile,
    sourcesDocument,
    nodesDocument,
    relationsDocument,
    residueDocument,
    nodeSchema,
    relationSchema,
    viewSchema,
    storedReceipt
  ] = await Promise.all([
    readJson(FILES.profile),
    readJson(FILES.sources),
    readJson(FILES.nodes),
    readJson(FILES.relations),
    readJson(FILES.residue),
    readJson(FILES.nodeSchema),
    readJson(FILES.relationSchema),
    readJson(FILES.viewSchema),
    readJson(FILES.receipt)
  ]);

  if (profile.status !== "candidate-local") push(errors, "profile.status", "must remain candidate-local");
  if (profile.authority_effect !== "none") push(errors, "profile.authority_effect", "must remain none");
  if (profile.release_admission !== "not-granted") {
    push(errors, "profile.release_admission", "must remain not-granted");
  }
  for (const blocked of [
    "authority-decision",
    "promotion-verdict",
    "canonical-write",
    "resonantos-projection",
    "release-admission"
  ]) {
    if (!profile.blocked_outputs?.includes(blocked)) {
      push(errors, "profile.blocked_outputs", `must include ${blocked}`);
    }
  }

  const sourceIds = sourcesDocument.sources.map((source) => source.source_id);
  if (!unique(sourceIds)) push(errors, "sources", "source_id values must be unique");
  const sourceIdSet = new Set(sourceIds);
  await Promise.all(sourcesDocument.sources.map(async (source, index) => {
    for (const error of await validateSourceRecord(source, sourcesDocument.repository_roots)) {
      push(errors, `sources[${index}]`, error);
    }
  }));

  const nodeIds = nodesDocument.nodes.map((node) => node.concept_id);
  if (!unique(nodeIds)) push(errors, "nodes", "concept_id values must be unique");
  const nodeIdSet = new Set(nodeIds);
  nodesDocument.nodes.forEach((node, index) => {
    validateClosedSchema(node, nodeSchema, `nodes[${index}]`, errors);
    for (const sourceRef of node.source_refs ?? []) {
      if (!sourceIdSet.has(sourceRef)) push(errors, `nodes[${index}].source_refs`, `unknown ${sourceRef}`);
    }
  });

  const relationIds = relationsDocument.relations.map((relation) => relation.relation_id);
  if (!unique(relationIds)) push(errors, "relations", "relation_id values must be unique");
  const relationIdSet = new Set(relationIds);
  relationsDocument.relations.forEach((relation, index) => {
    validateClosedSchema(relation, relationSchema, `relations[${index}]`, errors);
    if (!nodeIdSet.has(relation.source_concept)) {
      push(errors, `relations[${index}].source_concept`, `unknown ${relation.source_concept}`);
    }
    if (!nodeIdSet.has(relation.target_concept)) {
      push(errors, `relations[${index}].target_concept`, `unknown ${relation.target_concept}`);
    }
    for (const sourceRef of relation.evidence_refs ?? []) {
      if (!sourceIdSet.has(sourceRef)) push(errors, `relations[${index}].evidence_refs`, `unknown ${sourceRef}`);
    }
    for (const error of validateRelationBoundary(relation)) {
      push(errors, `relations[${index}]`, error);
    }
  });
  nodesDocument.nodes.forEach((node, index) => {
    for (const edge of [
      ...(node.challenge_contract?.contradiction_edges ?? []),
      ...(node.challenge_contract?.validation_edges ?? [])
    ]) {
      if (!relationIdSet.has(edge)) {
        push(errors, `nodes[${index}].challenge_contract`, `unknown relation ${edge}`);
      }
    }
  });

  const residueIds = residueDocument.items.map((item) => item.residue_id);
  if (!unique(residueIds)) push(errors, "residue", "residue_id values must be unique");
  const residueIdSet = new Set(residueIds);
  for (const [index, item] of residueDocument.items.entries()) {
    for (const sourceRef of item.evidence_refs ?? []) {
      if (!sourceIdSet.has(sourceRef)) push(errors, `residue[${index}].evidence_refs`, `unknown ${sourceRef}`);
    }
  }
  for (const [index, node] of nodesDocument.nodes.entries()) {
    const route = node.challenge_contract?.challenge_residue_route;
    if (route && !residueIdSet.has(route)) {
      push(errors, `nodes[${index}].challenge_contract.challenge_residue_route`, `unknown ${route}`);
    }
  }

  const viewDocuments = await Promise.all(profile.views.map((view) => readJson(view.path)));
  const viewRoles = new Set();
  let viewDigests;
  profile.views.forEach((profileView, index) => {
    const view = viewDocuments[index];
    validateClosedSchema(view, viewSchema, `views[${index}]`, errors);
    if (profileView.id !== view.view_id.replace("aug.view.", "augmentor-").replace("_", "-")) {
      push(errors, `views[${index}].view_id`, `does not map to profile id ${profileView.id}`);
    }
    if (profileView.view_role !== view.view_role) {
      push(errors, `views[${index}].view_role`, `does not match profile role ${profileView.view_role}`);
    }
    viewRoles.add(view.view_role);
    for (const sourceRef of view.source_refs ?? []) {
      if (!sourceIdSet.has(sourceRef)) push(errors, `views[${index}].source_refs`, `unknown ${sourceRef}`);
    }
    for (const nodeRef of view.node_refs ?? []) {
      if (!nodeIdSet.has(nodeRef)) push(errors, `views[${index}].node_refs`, `unknown ${nodeRef}`);
    }
    for (const relationRef of view.relation_refs ?? []) {
      if (!relationIdSet.has(relationRef)) push(errors, `views[${index}].relation_refs`, `unknown ${relationRef}`);
    }
    for (const [sequenceIndex, sequence] of (view.sequences ?? []).entries()) {
      for (const step of sequence.steps ?? []) {
        if (!nodeIdSet.has(step)) {
          push(errors, `views[${index}].sequences[${sequenceIndex}].steps`, `unknown ${step}`);
        }
      }
    }
    for (const residueRef of view.residue ?? []) {
      if (!residueIdSet.has(residueRef)) push(errors, `views[${index}].residue`, `unknown ${residueRef}`);
    }
  });
  for (const role of ["meaning", "system", "evidence", "bridge"]) {
    if (!viewRoles.has(role)) push(errors, "views", `missing ${role} view`);
  }

  const viewDigestEntries = await Promise.all(profile.views.map(async (view) => [
    view.id,
    sha256(await readBytes(view.path))
  ]));
  viewDigests = Object.fromEntries(viewDigestEntries);

  const counts = {
    sources: sourcesDocument.sources.length,
    nodes: nodesDocument.nodes.length,
    relations: relationsDocument.relations.length,
    views: viewDocuments.length,
    residue: residueDocument.items.length
  };
  const digests = {
    profile: sha256(await readBytes(FILES.profile)),
    sources: sha256(await readBytes(FILES.sources)),
    nodes: sha256(await readBytes(FILES.nodes)),
    relations: sha256(await readBytes(FILES.relations)),
    residue: sha256(await readBytes(FILES.residue)),
    views: viewDigests
  };
  if (JSON.stringify(storedReceipt.counts) !== JSON.stringify(counts)) {
    push(errors, "receipts/validation-receipt.json", "stored counts are stale");
  }
  if (JSON.stringify(storedReceipt.digests) !== JSON.stringify(digests)) {
    push(errors, "receipts/validation-receipt.json", "stored digests are stale");
  }
  if (storedReceipt.status !== "pass") {
    push(errors, "receipts/validation-receipt.json", "stored status must be pass");
  }

  const receipt = {
    schema: "augmentor.unified-agent.validation-receipt@0.1.0",
    package_id: profile.package_id,
    status: errors.length === 0 ? "pass" : "fail",
    counts,
    digests,
    checks: {
      source_digests: "checked",
      closed_schemas: "checked",
      relation_endpoints: "checked",
      view_references: "checked",
      stored_receipt: "checked",
      value_cycle_guard: "checked",
      authority_effect_ceiling: "checked",
      claim_ceiling: profile.claim_ceiling
    },
    violations: errors
  };

  return receipt;
};

const isMain = process.argv[1] && pathToFileURL(path.resolve(process.argv[1])).href === import.meta.url;

if (isMain) {
  const receipt = await validatePackage();
  process.stdout.write(`${JSON.stringify(receipt, null, 2)}\n`);
  if (receipt.status !== "pass") process.exitCode = 1;
}
