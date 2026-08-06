import assert from "node:assert/strict"
import { createHash } from "node:crypto"
import { execFileSync } from "node:child_process"
import { readdir, readFile, writeFile } from "node:fs/promises"
import { dirname, resolve } from "node:path"
import { fileURLToPath } from "node:url"

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "../../../../../")
const PACKAGE = "projects/body-war/ontology/whole-system"
const PACKAGE_ROOT = resolve(ROOT, PACKAGE)
const BUSINESS = "projects/body-war/ontology/business"
const digest = (bytes) => createHash("sha256").update(bytes).digest("hex")
const parse = async (path) => JSON.parse(await readFile(resolve(ROOT, path), "utf8"))

const NODE_KEYS = ["schema_version", "concept_id", "label", "definition", "concept_role", "system_kind", "branch_roles", "source_refs", "owner_route", "observation_status", "confidence", "residue", "forbidden_collapse"]
const SYSTEM_RELATION_KEYS = ["schema_version", "relation_id", "predicate", "source_concept", "target_concept", "evidence_refs", "observation_status", "direction", "owner_route", "authority_effect", "forbidden_collapse"]
const BRIDGE_KEYS = ["schema_version", "relation_id", "predicate", "business_concept", "system_concept", "business_evidence_refs", "system_evidence_refs", "alignment_status", "note", "direction", "owner_route", "authority_effect", "forbidden_collapse"]
const SYSTEM_KINDS = new Set(["component", "interface", "module", "service", "endpoint", "schema", "table", "job", "configuration", "test", "deployment_unit", "data_store", "external_dependency", "gap"])
const SYSTEM_PREDICATES = new Set(["contains", "exposes", "serves", "calls", "uses", "implements", "depends_on", "reads", "writes", "persists_to", "protects_with", "configured_by", "migrates", "runs", "routes_to", "tests", "constrains"])
const BRIDGE_PREDICATES = new Set(["realized_by", "depends_on", "constrained_by", "observed_by", "tested_by", "drifts_from", "traced_to"])

function closed(value, keys, label) {
  assert.deepEqual(Object.keys(value).sort(), [...keys].sort(), `${label} must be closed-shape`)
}

async function verifyRef(source, label) {
  assert.deepEqual(Object.keys(source).sort(), ["path", "selector", "sha256"], `${label} source ref must be closed-shape`)
  assert.match(source.sha256, /^[a-f0-9]{64}$/, `${label} source digest`)
  const bytes = await readFile(resolve(ROOT, source.path))
  assert.equal(digest(bytes), source.sha256, `${label} stale digest: ${source.path}`)
  assert.ok(bytes.toString("utf8").includes(source.selector), `${label} missing selector: ${source.path} :: ${source.selector}`)
}

async function verifyRefs(refs, label) {
  assert.ok(Array.isArray(refs) && refs.length > 0, `${label} requires evidence`)
  for (const source of refs) await verifyRef(source, label)
}

async function trackedFiles() {
  return execFileSync("git", ["ls-files", "-z", "projects/body-war"], { cwd: ROOT })
    .toString("utf8").split("\0").filter(Boolean)
    .filter((path) => !path.startsWith(`${PACKAGE}/`)).sort()
}

async function treeDigest(paths) {
  let lines = ""
  for (const path of paths) lines += `${digest(await readFile(resolve(ROOT, path)))}  ${path}\n`
  return digest(lines)
}

async function main() {
  const profile = await parse(`${PACKAGE}/profile.json`)
  const manifest = await parse(`${PACKAGE}/nodes/manifest.json`)
  const systemBundle = await parse(`${PACKAGE}/relations/system-relations.json`)
  const bridgeBundle = await parse(`${PACKAGE}/relations/bridge-relations.json`)
  const businessView = await parse(`${PACKAGE}/views/business.json`)
  const systemView = await parse(`${PACKAGE}/views/system.json`)
  const bridgeView = await parse(`${PACKAGE}/views/bridge.json`)
  const sourceUniverse = await parse(`${PACKAGE}/source-universe.json`)
  const residue = await parse(`${PACKAGE}/residue.json`)
  const context = await parse(`${PACKAGE}/context/context-pack.json`)
  const businessManifest = await parse(`${BUSINESS}/nodes/manifest.json`)
  const businessRelations = await parse(`${BUSINESS}/relations/relations.json`)

  assert.equal(profile.ontology_type, "business-system-bridge")
  assert.equal(profile.status, "candidate-local")
  assert.equal(profile.authority_effect, "none")
  assert.equal(profile.release_admission, "not-granted")
  assert.deepEqual(profile.branches, ["body-war.branch.business", "body-war.branch.system", "body-war.branch.business-system-bridge"])

  const nodeFiles = (await readdir(resolve(PACKAGE_ROOT, "nodes/system"))).filter((path) => path.endsWith(".json")).sort()
  assert.equal(nodeFiles.length, manifest.node_count, "node manifest count")
  const nodes = await Promise.all(nodeFiles.map((path) => parse(`${PACKAGE}/nodes/system/${path}`)))
  const nodeIds = new Set()
  for (const node of nodes) {
    closed(node, NODE_KEYS, node.concept_id)
    assert.equal(node.schema_version, "body-war-system-node/v1")
    assert.match(node.concept_id, /^body-war\.system\.[a-z0-9_.-]+$/)
    assert.ok(!nodeIds.has(node.concept_id), `duplicate node: ${node.concept_id}`)
    nodeIds.add(node.concept_id)
    assert.ok(SYSTEM_KINDS.has(node.system_kind), `invalid system kind: ${node.system_kind}`)
    assert.deepEqual(node.branch_roles, ["system"])
    assert.ok(["observed", "partial", "planned", "gap"].includes(node.observation_status))
    assert.equal(node.owner_route, "body-war.product-ontology-owner")
    assert.ok(node.forbidden_collapse.length > 0)
    await verifyRefs(node.source_refs, node.concept_id)
    for (const forbidden of ["implementation_body", "executable_logic", "transition_guard", "effect_code"]) assert.ok(!(forbidden in node), `${node.concept_id} contains executable logic`)
  }
  assert.deepEqual([...nodeIds].sort(), [...manifest.concept_ids].sort(), "node manifest closure")
  for (const required of ["component", "interface", "module", "endpoint", "table", "test", "deployment_unit", "data_store", "external_dependency", "gap"]) {
    assert.ok(nodes.some((node) => node.system_kind === required), `missing system kind: ${required}`)
  }

  assert.equal(systemBundle.relation_count, systemBundle.relations.length)
  const relationIds = new Set()
  const connectedSystemIds = new Set()
  for (const relation of systemBundle.relations) {
    closed(relation, SYSTEM_RELATION_KEYS, relation.relation_id)
    assert.equal(relation.schema_version, "body-war-system-relation/v1")
    assert.ok(!relationIds.has(relation.relation_id), `duplicate relation: ${relation.relation_id}`)
    relationIds.add(relation.relation_id)
    assert.ok(SYSTEM_PREDICATES.has(relation.predicate), `invalid system predicate: ${relation.predicate}`)
    assert.ok(nodeIds.has(relation.source_concept), `missing relation source: ${relation.source_concept}`)
    assert.ok(nodeIds.has(relation.target_concept), `missing relation target: ${relation.target_concept}`)
    assert.notEqual(relation.source_concept, relation.target_concept, `self relation: ${relation.relation_id}`)
    assert.equal(relation.authority_effect, "none")
    connectedSystemIds.add(relation.source_concept)
    connectedSystemIds.add(relation.target_concept)
    await verifyRefs(relation.evidence_refs, relation.relation_id)
  }

  const businessIds = new Set(businessManifest.concept_ids)
  assert.equal(bridgeBundle.relation_count, bridgeBundle.relations.length)
  const bridgeIds = new Set()
  const bridgeTuples = new Set()
  for (const relation of bridgeBundle.relations) {
    closed(relation, BRIDGE_KEYS, relation.relation_id)
    assert.equal(relation.schema_version, "body-war-business-system-bridge/v1")
    assert.ok(!bridgeIds.has(relation.relation_id), `duplicate bridge: ${relation.relation_id}`)
    bridgeIds.add(relation.relation_id)
    assert.ok(BRIDGE_PREDICATES.has(relation.predicate), `invalid bridge predicate: ${relation.predicate}`)
    assert.ok(businessIds.has(relation.business_concept), `missing business bridge endpoint: ${relation.business_concept}`)
    assert.ok(nodeIds.has(relation.system_concept), `missing system bridge endpoint: ${relation.system_concept}`)
    assert.ok(["supported", "partial", "gap", "drift"].includes(relation.alignment_status))
    assert.equal(relation.authority_effect, "none")
    const tuple = `${relation.business_concept}\0${relation.predicate}\0${relation.system_concept}`
    assert.ok(!bridgeTuples.has(tuple), `duplicate bridge tuple: ${relation.relation_id}`)
    bridgeTuples.add(tuple)
    connectedSystemIds.add(relation.system_concept)
    assert.ok(relation.business_evidence_refs.every((entry) => entry.path.startsWith(`${BUSINESS}/`)), `${relation.relation_id} business evidence must come from business branch`)
    assert.ok(relation.system_evidence_refs.every((entry) => entry.path.startsWith("projects/body-war/app/") || entry.path.startsWith("projects/body-war/infra/")), `${relation.relation_id} system evidence must come from app or infra`)
    await verifyRefs(relation.business_evidence_refs, `${relation.relation_id}:business`)
    await verifyRefs(relation.system_evidence_refs, `${relation.relation_id}:system`)
  }
  assert.deepEqual([...nodeIds].filter((id) => !connectedSystemIds.has(id)), [], "standalone system nodes are forbidden; use residue or connect the concept")

  assert.equal(businessView.node_count, businessManifest.node_count)
  assert.equal(businessView.relation_count, businessRelations.relation_count)
  const businessPaths = (await trackedFiles()).filter((path) => path.startsWith(`${BUSINESS}/`))
  assert.equal(businessView.imported_tree_sha256, await treeDigest(businessPaths), "business import tree drift")
  assert.equal(profile.imported_business_tree_sha256, businessView.imported_tree_sha256)
  for (const artifact of businessView.artifacts) {
    const bytes = await readFile(resolve(ROOT, artifact.path))
    assert.equal(digest(bytes), artifact.sha256, `business artifact drift: ${artifact.path}`)
  }
  assert.deepEqual([...systemView.concepts].sort(), [...nodeIds].sort(), "system view node closure")
  assert.deepEqual([...systemView.relations].sort(), [...relationIds].sort(), "system view relation closure")
  assert.deepEqual([...bridgeView.relations].sort(), [...bridgeIds].sort(), "bridge view relation closure")

  const tracked = await trackedFiles()
  assert.equal(sourceUniverse.file_count, tracked.length, "source-universe count")
  assert.deepEqual(sourceUniverse.entries.map((entry) => entry.path), tracked, "source-universe path closure")
  assert.equal(sourceUniverse.tree_sha256, await treeDigest(tracked), "source-universe tree drift")
  const sourcePaths = new Set()
  for (const entry of sourceUniverse.entries) {
    assert.ok(!sourcePaths.has(entry.path), `duplicate source path: ${entry.path}`)
    sourcePaths.add(entry.path)
    assert.ok(!entry.path.startsWith(`${PACKAGE}/`), "source universe must exclude its own output root")
    const bytes = await readFile(resolve(ROOT, entry.path))
    assert.equal(bytes.byteLength, entry.bytes, `source byte count drift: ${entry.path}`)
    assert.equal(digest(bytes), entry.sha256, `source digest drift: ${entry.path}`)
  }
  const coverageTotal = Object.values(sourceUniverse.coverage_by_class).reduce((sum, count) => sum + count, 0)
  assert.equal(coverageTotal, sourceUniverse.file_count, "source class coverage")

  assert.ok(residue.entries.length >= 10, "explicit whole-system residue coverage")
  assert.equal(new Set(residue.entries.map((entry) => entry.id)).size, residue.entries.length, "unique residue IDs")
  for (const entry of residue.entries) {
    assert.equal(entry.status, "open")
    await verifyRefs(entry.source_refs, entry.id)
  }

  assert.ok(context.obligations.length >= 4, "context builder dry-run obligations")
  const obligationIds = new Set()
  for (const obligation of context.obligations) {
    assert.ok(!obligationIds.has(obligation.id), `duplicate obligation: ${obligation.id}`)
    obligationIds.add(obligation.id)
    assert.ok(obligation.obligation.length > 20)
    await verifyRefs(obligation.sources, obligation.id)
  }
  assert.ok(context.unresolved_residue.every((id) => residue.entries.some((entry) => entry.id === id)), "context residue closure")
  assert.equal(context.authority_effect, "none")

  for (const schema of ["system-node.schema.json", "system-relation.schema.json", "bridge-relation.schema.json", "branch-view.schema.json"]) {
    const value = await parse(`${PACKAGE}/schemas/${schema}`)
    assert.equal(value.$schema, "https://json-schema.org/draft/2020-12/schema")
    assert.equal(value.type, "object")
  }

  const receiptPath = resolve(PACKAGE_ROOT, "receipts/validation-receipt.json")
  const receiptBody = {
    schema_version: "body-war-whole-system-validation-receipt/v1",
    status: "pass",
    package_id: profile.package_id,
    business_import: { nodes: businessView.node_count, relations: businessView.relation_count, tree_sha256: businessView.imported_tree_sha256 },
    system_branch: { nodes: nodes.length, relations: systemBundle.relation_count },
    bridge_branch: { relations: bridgeBundle.relation_count },
    source_universe: { files: sourceUniverse.file_count, tree_sha256: sourceUniverse.tree_sha256 },
    residue_count: residue.entries.length,
    context_obligations: context.obligations.length,
    authority_effect: "none",
    release_admission: "not-granted",
  }
  let generatedAt = new Date().toISOString()
  try {
    const existing = await parse(`${PACKAGE}/receipts/validation-receipt.json`)
    const { generated_at: existingGeneratedAt, ...existingBody } = existing
    if (typeof existingGeneratedAt === "string" && JSON.stringify(existingBody) === JSON.stringify(receiptBody)) {
      generatedAt = existingGeneratedAt
    }
  } catch (error) {
    if (error?.code !== "ENOENT") throw error
  }
  const { schema_version, status, ...receiptDetails } = receiptBody
  const receipt = {
    schema_version,
    status,
    generated_at: generatedAt,
    ...receiptDetails,
  }
  await writeFile(receiptPath, `${JSON.stringify(receipt, null, 2)}\n`)
  process.stdout.write(`PASS: ${nodes.length} system nodes, ${systemBundle.relation_count} system relations, ${bridgeBundle.relation_count} bridges, ${sourceUniverse.file_count} tracked sources, ${residue.entries.length} gaps.\n`)
}

await main()
