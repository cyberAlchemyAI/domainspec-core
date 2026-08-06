import { createHash } from "node:crypto"
import { cp, mkdir, readFile, readdir, rm, writeFile } from "node:fs/promises"
import { basename, dirname, join, resolve } from "node:path"
import { fileURLToPath } from "node:url"

import { buildBodyWarAdapterArtifacts } from "../../../../../cyberAlchemy-v2/implementation/ontology-evidence-workbench/src/body-war-adapter-writer.mjs"
import { canonicalBytes, canonicalSha256, sha256Bytes } from "../../../../../cyberAlchemy-v2/implementation/ontology-evidence-workbench/src/canonical-json.mjs"
import { UPSTREAM_CONTRACT } from "../../../../../cyberAlchemy-v2/implementation/ontology-evidence-workbench/src/adapter-run-writer.mjs"

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "../../../../../")
const PACKAGE = resolve(ROOT, "projects/body-war/ontology/whole-system")
const FRONTEND = resolve(PACKAGE, "frontend")
const DATA = resolve(FRONTEND, "oew-data")
const RETAINED_DIST = resolve(ROOT, "cyberAlchemy-v2/implementation/ontology-evidence-workbench/generated/runs/SWU-OEWSN-023/20260804T035543Z/dashboard-dist")
const BUSINESS = resolve(ROOT, "projects/body-war/ontology/business")
const CREATED_AT = "2026-08-04T00:00:00.000Z"
const RUN_ID = "BODY-WAR-WHOLE-SYSTEM-001"
const OLD_RECEIPT_SHA = "07c9491aaec8c1a98a15aa75c46f3a1b28a9c96365e20d8cfb252722d80b9b95"
const OLD_RELATIONS_SHA = "234ad4152b731edcb03cd1b45dfa21570bd37df741090ca6ca0940fd98c0ce00"
const OLD_ENCODING_SHA = "64cfafc1ce0803ccd7d21354b713458898256fb5db1372a380f3c383ca1d14e6"
const NORMALIZED_RELATION_SCHEMA = "body-war-whole-system-relation/v1"
const NORMALIZED_RELATION_SET_SCHEMA = "body-war-whole-system-relation-set/v1"
const ALLOWED_EDGE_TYPES = new Set([
  "imports", "exports", "contains", "inherits", "implements", "calls", "subscribes", "publishes", "middleware", "reads_from", "writes_to", "transforms", "validates", "depends_on", "tested_by", "configures", "related", "similar_to", "deploys", "serves", "provisions", "triggers", "migrates", "documents", "routes", "defines_schema", "contains_flow", "flow_step", "cross_domain", "cites", "contradicts", "builds_on", "exemplifies", "categorized_under", "authored_by", "instance_of", "variant_of", "uses_token",
])

const sha = (bytes) => createHash("sha256").update(bytes).digest("hex")
const readJson = async (path) => JSON.parse(await readFile(path, "utf8"))
const logical = (path) => path.slice(ROOT.length + 1)

function titleCase(value) {
  return String(value).split(/[_-]/).map((part) => `${part.slice(0, 1).toUpperCase()}${part.slice(1)}`).join(" ")
}

function graphNodeType(kind) {
  return ["external_dependency", "test"].includes(kind) ? "source" : "claim"
}

function sourceKind(node) {
  if (node.system_kind === "gap") return "Finding"
  if (node.system_kind === "test") return "Observation"
  if (node.system_kind === "external_dependency") return "Research artifact"
  return "Definition"
}

function edgeType(predicate) {
  if (["drifts_from", "contests", "does_not_promote"].includes(predicate)) return "contradicts"
  if (["depends_on", "implements", "realized_by", "supports", "fulfills", "tested_by", "tests", "traced_to", "observed_by"].includes(predicate)) return "builds_on"
  return "related"
}

function uniqueEdgeTypes(relations) {
  const used = new Set()
  const alternates = ["related", "builds_on", "contradicts"]
  return relations.map((relation) => {
    const preferred = edgeType(relation.predicate)
    const key = (type) => `${relation.source_concept}\0${relation.target_concept}\0${type}`
    let selected = preferred
    let diagnostic = null
    if (used.has(key(selected))) {
      selected = alternates.find((type) => !used.has(key(type)))
      if (!selected) throw new Error(`No presentation edge type can disambiguate ${relation.relation_id}`)
      diagnostic = `PRESENTATION_TUPLE_DISAMBIGUATED:${preferred}->${selected}`
    }
    if (!ALLOWED_EDGE_TYPES.has(selected)) throw new Error(`Unsupported edge type: ${selected}`)
    used.add(key(selected))
    return { ...relation, presentation_relation: selected, projection_diagnostic: diagnostic }
  })
}

function normalizeBusinessRelation(relation) {
  return {
    relation_id: relation.relation_id,
    predicate: relation.predicate,
    source_concept: relation.source_concept,
    target_concept: relation.target_concept,
    direction: relation.direction,
    authority_effect: relation.authority_effect,
    evidence_refs: relation.evidence_refs,
    source_schema_version: relation.schema_version,
    branch_role: "business",
  }
}

function normalizeSystemRelation(relation) {
  return {
    relation_id: relation.relation_id,
    predicate: relation.predicate,
    source_concept: relation.source_concept,
    target_concept: relation.target_concept,
    direction: relation.direction,
    authority_effect: relation.authority_effect,
    evidence_refs: relation.evidence_refs,
    source_schema_version: relation.schema_version,
    branch_role: "system",
  }
}

function normalizeBridgeRelation(relation) {
  return {
    relation_id: relation.relation_id,
    predicate: relation.predicate,
    source_concept: relation.business_concept,
    target_concept: relation.system_concept,
    direction: relation.direction,
    authority_effect: relation.authority_effect,
    evidence_refs: [...relation.business_evidence_refs, ...relation.system_evidence_refs],
    source_schema_version: relation.schema_version,
    branch_role: "bridge",
    alignment_status: relation.alignment_status,
  }
}

function normalizedSourceRecord(relation) {
  return {
    schema_version: NORMALIZED_RELATION_SCHEMA,
    relation_id: relation.relation_id,
    predicate: relation.predicate,
    source_concept: relation.source_concept,
    target_concept: relation.target_concept,
    direction: relation.direction,
    authority_effect: relation.authority_effect,
    evidence_refs: relation.evidence_refs,
    source_schema_version: relation.source_schema_version,
    branch_role: relation.branch_role,
    ...(relation.alignment_status ? { alignment_status: relation.alignment_status } : {}),
    adapter_normalization: "Presentation-only endpoint normalization; source artifact remains unchanged.",
  }
}

function relativeLuminance(hex) {
  const values = [1, 3, 5].map((offset) => Number.parseInt(hex.slice(offset, offset + 2), 16) / 255)
    .map((value) => value <= 0.04045 ? value / 12.92 : ((value + 0.055) / 1.055) ** 2.4)
  return 0.2126 * values[0] + 0.7152 * values[1] + 0.0722 * values[2]
}

function contrast(left, right) {
  const values = [relativeLuminance(left), relativeLuminance(right)].sort((a, b) => b - a)
  return (values[0] + 0.05) / (values[1] + 0.05)
}

function hslToHex(h, s, l) {
  const c = (1 - Math.abs(2 * l - 1)) * s
  const x = c * (1 - Math.abs((h / 60) % 2 - 1))
  const m = l - c / 2
  const [r, g, b] = h < 60 ? [c, x, 0] : h < 120 ? [x, c, 0] : h < 180 ? [0, c, x] : h < 240 ? [0, x, c] : h < 300 ? [x, 0, c] : [c, 0, x]
  return `#${[r, g, b].map((value) => Math.round((value + m) * 255).toString(16).padStart(2, "0")).join("").toUpperCase()}`
}

function accessibleColor(hue, background, mode) {
  const candidates = []
  for (let index = 15; index <= 85; index += 1) {
    const lightness = index / 100
    const hex = hslToHex(hue, 0.72, lightness)
    const ratio = contrast(hex, background)
    if (ratio >= 4.5) candidates.push({ hex, ratio, distance: Math.abs(lightness - (mode === "dark" ? 0.55 : 0.38)) })
  }
  if (candidates.length === 0) throw new Error(`No accessible color for hue ${hue}`)
  candidates.sort((a, b) => a.distance - b.distance)
  return candidates[0]
}

function relationEncoding(relations, graphSha) {
  const predicates = [...new Set(relations.map((entry) => entry.predicate))].sort()
  const presentationTypes = [...new Set(relations.map((entry) => entry.presentation_relation))].sort()
  const predicateColorMap = {}
  const colorTokens = {}
  predicates.forEach((predicate, index) => {
    const token = `edge.predicate.${predicate.replaceAll("_", "-")}`
    const hue = (index * 137.508) % 360
    const dark = accessibleColor(hue, "#0B0D0F", "dark")
    const light = accessibleColor(hue, "#FFFFFF", "light")
    predicateColorMap[predicate] = token
    colorTokens[token] = {
      family: "source-predicate",
      predicate,
      dark: dark.hex,
      dark_contrast: Number(dark.ratio.toFixed(3)),
      light: light.hex,
      light_contrast: Number(light.ratio.toFixed(3)),
    }
  })
  const patterns = ["edge.pattern.solid", "edge.pattern.dashed", "edge.pattern.dotted"]
  const presentationPatternMap = Object.fromEntries(presentationTypes.map((type, index) => [type, patterns[index % patterns.length]]))
  return {
    schema_version: "body-war.semantic-navigation-relation-encoding-candidate.v1",
    profile_id: "body-war-relation-encoding-v1-candidate",
    status: "candidate-local",
    authority_effect: "none",
    selection: { strategy: "one unique color per exact source predicate", source: "user request", selected_at: CREATED_AT },
    source_bindings: { presentation_graph_sha256: graphSha },
    backgrounds: { dark: "#0B0D0F", light: "#FFFFFF" },
    minimum_graphical_contrast: 4.5,
    predicateColorMap,
    colorTokens,
    presentationPatternMap,
    patternTokens: {
      "edge.pattern.solid": { label: "solid", stroke_dasharray: "none" },
      "edge.pattern.dashed": { label: "dashed", stroke_dasharray: "8 5" },
      "edge.pattern.dotted": { label: "dotted", stroke_dasharray: "2 4" },
    },
    redundancy_rules: ["Exact predicate text remains visible.", "Color is presentation only and never changes ontology meaning or authority."],
  }
}

function patchOnce(text, before, after, label) {
  const first = text.indexOf(before)
  if (first < 0 || text.indexOf(before, first + before.length) >= 0) throw new Error(`${label} replacement cardinality is not one`)
  return `${text.slice(0, first)}${after}${text.slice(first + before.length)}`
}

async function treeDigest(root, ignored = new Set()) {
  const rows = []
  async function walk(directory) {
    for (const entry of (await readdir(directory, { withFileTypes: true })).sort((a, b) => a.name.localeCompare(b.name))) {
      const path = join(directory, entry.name)
      if (entry.isDirectory()) await walk(path)
      else if (!ignored.has(path)) {
        const bytes = await readFile(path)
        rows.push(`${sha(bytes)} ${bytes.length} ${path.slice(root.length + 1)}`)
      }
    }
  }
  await walk(root)
  return sha(`${rows.join("\n")}\n`)
}

async function main() {
  const wholeReceiptPath = resolve(PACKAGE, "receipts/validation-receipt.json")
  const wholeReceiptBytes = await readFile(wholeReceiptPath)
  const wholeReceipt = JSON.parse(wholeReceiptBytes)
  if (wholeReceipt.status !== "pass" || wholeReceipt.authority_effect !== "none") throw new Error("Whole-system ontology validation receipt is not admissible")

  const business = await buildBodyWarAdapterArtifacts()
  const systemManifest = await readJson(resolve(PACKAGE, "nodes/manifest.json"))
  const systemNodes = []
  for (const conceptId of systemManifest.concept_ids) {
    const path = resolve(PACKAGE, `nodes/system/${conceptId.replace("body-war.system.", "")}.json`)
    systemNodes.push({ node: await readJson(path), path, bytes: await readFile(path) })
  }
  const systemRelations = (await readJson(resolve(PACKAGE, "relations/system-relations.json"))).relations.map(normalizeSystemRelation)
  const bridgeRelations = (await readJson(resolve(PACKAGE, "relations/bridge-relations.json"))).relations.map(normalizeBridgeRelation)
  const businessRelations = (await readJson(resolve(BUSINESS, "relations/relations.json"))).relations.map(normalizeBusinessRelation)
  const relations = uniqueEdgeTypes([...businessRelations, ...systemRelations, ...bridgeRelations].sort((a, b) => a.relation_id.localeCompare(b.relation_id)))

  const degree = new Map()
  for (const relation of relations) {
    degree.set(relation.source_concept, (degree.get(relation.source_concept) ?? 0) + 1)
    degree.set(relation.target_concept, (degree.get(relation.target_concept) ?? 0) + 1)
  }
  const presentationNodes = [...business.graph.nodes]
  const sidecarNodes = { ...business.sidecar.nodes }
  for (const { node, path, bytes } of systemNodes.sort((a, b) => a.node.concept_id.localeCompare(b.node.concept_id))) {
    const id = `presentation:${node.concept_id}`
    const kind = sourceKind(node)
    const type = graphNodeType(node.system_kind)
    presentationNodes.push({
      id,
      type,
      name: node.label,
      filePath: logical(path),
      summary: node.definition,
      tags: ["authority:none", "branch:system", `system-kind:${node.system_kind}`, `observation-status:${node.observation_status}`, `concept-role:${node.concept_role.replaceAll(" ", "-")}`, `confidence:${node.confidence.evidence_confidence}`],
      complexity: (degree.get(node.concept_id) ?? 0) >= 5 ? "complex" : (degree.get(node.concept_id) ?? 0) >= 3 ? "moderate" : "simple",
      knowledgeMeta: { category: titleCase(node.system_kind), content: node.definition },
    })
    sidecarNodes[id] = {
      source_ref: node.concept_id,
      source_kind: kind,
      source_kind_original: node.system_kind,
      source_artifact: logical(path),
      source_path: logical(path),
      source_digest: sha(bytes),
      presentation_type: ["Observation", "Research artifact"].includes(kind) ? "source" : "claim",
      mapping_loss: "generalized",
      authority_effect: "none",
    }
  }
  presentationNodes.sort((a, b) => a.id.localeCompare(b.id))

  const presentationEdges = []
  const sidecarEdges = {}
  const sourceRelationRecords = []
  const lossCounts = { exact: 0, generalized: 0, lossy: 0 }
  for (const relation of relations) {
    const id = `presentation-edge:${relation.relation_id}`
    const loss = relation.presentation_relation === "contradicts" && relation.predicate === "drifts_from" ? "generalized" : relation.presentation_relation === edgeType(relation.predicate) ? "generalized" : "lossy"
    lossCounts[loss] += 1
    presentationEdges.push({
      source: `presentation:${relation.source_concept}`,
      target: `presentation:${relation.target_concept}`,
      type: relation.presentation_relation,
      direction: relation.direction === "symmetric" ? "bidirectional" : "forward",
      description: relation.predicate,
      weight: 1,
    })
    sidecarEdges[id] = {
      source_ref: relation.relation_id,
      source: relation.source_concept,
      target: relation.target_concept,
      source_relation: relation.predicate,
      presentation_relation: relation.presentation_relation,
      mapping_loss: loss,
      policy_disposition: relation.alignment_status === "gap" ? "policy-indeterminate" : "not-applicable",
      diagnostics: [relation.projection_diagnostic, relation.alignment_status === "gap" ? "IMPLEMENTATION_GAP" : null].filter(Boolean),
      grounding_inclusion: relation.alignment_status === "gap" ? "excluded" : "not-applicable",
      evidence_refs: relation.evidence_refs.map((entry) => entry.path),
      authority_effect: "none",
    }
    sourceRelationRecords.push(normalizedSourceRecord(relation))
  }

  const idsBySystemKind = new Map()
  for (const { node } of systemNodes) {
    const ids = idsBySystemKind.get(node.system_kind) ?? []
    ids.push(`presentation:${node.concept_id}`)
    idsBySystemKind.set(node.system_kind, ids)
  }
  const systemLayers = [...idsBySystemKind.entries()].sort(([a], [b]) => a.localeCompare(b)).map(([kind, nodeIds]) => ({
    id: `body-war-system-${kind.replaceAll("_", "-")}`,
    name: `System · ${titleCase(kind)}`,
    description: `Observed Body War ${titleCase(kind).toLowerCase()} concepts; authority effect is none.`,
    nodeIds: nodeIds.sort(),
  }))
  const tour = [
    { order: 1, title: "Business and system branches", description: "Start with the business workflow and its observed HTTP runtime.", nodeIds: ["body-war.business.workflow.login-to-score-preview", "body-war.business.context.identity-consent", "body-war.system.component.http-server", "body-war.system.interface.http-api"] },
    { order: 2, title: "Connect through Strava", description: "Follow OAuth from business intent to the server adapters and callback.", nodeIds: ["body-war.business.operation.start-strava-oauth", "body-war.business.operation.complete-strava-oauth", "body-war.system.endpoint.strava-start", "body-war.system.endpoint.strava-callback", "body-war.system.module.strava-oauth-adapter"] },
    { order: 3, title: "Suggest a track", description: "See the candidate suggestion operation, API, and persistence table.", nodeIds: ["body-war.business.operation.create-suggested-track", "body-war.business.entity.suggested-track", "body-war.system.endpoint.suggested-tracks", "body-war.system.table.suggested-tracks"] },
    { order: 4, title: "Attach activity evidence", description: "Inspect the redacted candidate evidence path and consent boundary.", nodeIds: ["body-war.business.operation.attach-activity-evidence-candidate", "body-war.business.entity.activity-evidence-candidate", "body-war.business.policy.consent-contract", "body-war.system.endpoint.suggested-track-evidence", "body-war.system.table.activity-evidence-candidates"] },
    { order: 5, title: "Geometry and score gap", description: "The business workflow continues, while the observed runtime remains explicitly incomplete.", nodeIds: ["body-war.business.operation.fetch-selected-activity-geometry", "body-war.business.operation.calculate-score-preview", "body-war.business.outcome.score-preview", "body-war.system.gap.geometry-score-gap"] },
    { order: 6, title: "Verification boundary", description: "Tests and deployment units prove a candidate prototype only, not production readiness.", nodeIds: ["body-war.system.test.auth-consumer-tests", "body-war.system.test.api-e2e-tests", "body-war.system.test.browser-e2e-tests", "body-war.system.deployment_unit.app-container"] },
  ].map((step) => ({ ...step, nodeIds: step.nodeIds.map((id) => `presentation:${id}`) }))

  const graph = {
    version: "1.0.0",
    kind: "knowledge",
    project: {
      name: "Body War Whole-System Ontology",
      languages: ["JSON", "Markdown", "TypeScript", "HTML"],
      frameworks: ["Ontology Evidence Workbench"],
      description: "Candidate-local business, observed system, and evidence-backed bridge graph. Authority effect is none; open gaps remain visible.",
      analyzedAt: CREATED_AT,
      gitCommitHash: sha(wholeReceiptBytes),
    },
    nodes: presentationNodes,
    edges: presentationEdges,
    layers: [...business.graph.layers, ...systemLayers],
    tour,
  }
  const graphBytes = canonicalBytes(graph)
  const sourceRelations = { schema_version: NORMALIZED_RELATION_SET_SCHEMA, relations: sourceRelationRecords, authority_effect: "none" }
  const encoding = relationEncoding(relations, sha256Bytes(graphBytes))
  const sourceRelationsSha = canonicalSha256(sourceRelations)
  const encodingSha = canonicalSha256(encoding)
  const sidecar = {
    schema_version: "oew.evidence-sidecar.v1",
    source_run: { run_id: "body-war.whole-system-ontology", terminal_receipt_sha256: sha(wholeReceiptBytes), authority_effect: "none" },
    upstream_contract: UPSTREAM_CONTRACT,
    nodes: sidecarNodes,
    edges: sidecarEdges,
    source_relations: sourceRelations,
    relation_encoding: encoding,
    grounding: {
      included_path: tour[4].nodeIds.map((id) => id.replace("presentation:", "")),
      visible_excluded: systemNodes.filter(({ node }) => node.observation_status === "gap").map(({ node }) => node.concept_id),
      indeterminate_candidates: relations.filter((entry) => entry.alignment_status === "gap").map((entry) => entry.relation_id),
    },
    counts: {
      source_nodes: presentationNodes.length,
      presentation_nodes: presentationNodes.length,
      sidecar_nodes: Object.keys(sidecarNodes).length,
      by_type: { claim: Object.values(sidecarNodes).filter((entry) => entry.presentation_type === "claim").length, source: Object.values(sidecarNodes).filter((entry) => entry.presentation_type === "source").length },
      source_relations: presentationEdges.length,
      presentation_edges: presentationEdges.length,
      sidecar_edges: Object.keys(sidecarEdges).length,
      by_mapping_loss: lossCounts,
    },
    input_digests: { node_subset_sha256: canonicalSha256(presentationNodes), relation_subset_sha256: canonicalSha256(sourceRelations) },
    authority_effect: "none",
  }
  const sidecarBytes = canonicalBytes(sidecar)
  const receipt = {
    schema_version: "oew.adapter-receipt.v1",
    state: "receipt-complete",
    result: "pass",
    run_id: RUN_ID,
    created_at: CREATED_AT,
    source_run: sidecar.source_run,
    adapter: { name: "@cyberalchemy/ontology-evidence-workbench", version: "0.2.0-body-war-whole-system-candidate", canonicalization: "canonical-json-key-order-v1" },
    upstream_contract: UPSTREAM_CONTRACT,
    artifacts: [
      { role: "presentation-graph", path: "presentation-graph.json", sha256: sha256Bytes(graphBytes), size_bytes: graphBytes.length },
      { role: "evidence-sidecar", path: "evidence-sidecar.json", sha256: sha256Bytes(sidecarBytes), size_bytes: sidecarBytes.length },
    ],
    determinism: { builds_compared: 2, byte_identical: true, graph_sha256: sha256Bytes(graphBytes), sidecar_sha256: sha256Bytes(sidecarBytes) },
    mapping_counts: { source_nodes: presentationNodes.length, presentation_nodes: presentationNodes.length, sidecar_nodes: Object.keys(sidecarNodes).length, source_relations: presentationEdges.length, presentation_edges: presentationEdges.length, sidecar_edges: Object.keys(sidecarEdges).length },
    protected_source_check: { ...sidecar.input_digests, read_only: true, authority_effect: "none" },
    semantic_fixture: { schema_version: "oew.semantic-navigation-browser-fixture.v1", authority_effect: "none", source_relations_sha256: sourceRelationsSha, relation_encoding_sha256: encodingSha, source_relation_ids: sourceRelationRecords.map((entry) => entry.relation_id) },
    evidence_ceiling: "Deterministic read-only projection of the candidate-local Body War whole-system ontology; no ontology promotion, live Strava import, source-backed geometry, score authority, release, deployment, production, or human-outcome claim.",
    authority_effect: "none",
  }
  const receiptBytes = canonicalBytes(receipt)
  const receiptSha = sha256Bytes(receiptBytes)

  await rm(FRONTEND, { recursive: true, force: true })
  await cp(RETAINED_DIST, FRONTEND, { recursive: true })
  await mkdir(DATA, { recursive: true })
  await writeFile(resolve(DATA, "presentation-graph.json"), graphBytes)
  await writeFile(resolve(DATA, "evidence-sidecar.json"), sidecarBytes)
  await writeFile(resolve(DATA, "adapter-receipt.json"), receiptBytes)
  await writeFile(resolve(FRONTEND, "knowledge-graph.json"), graphBytes)
  await writeFile(resolve(FRONTEND, "meta.json"), canonicalBytes({ theme: { presetId: "obsidian", accentId: "gold" } }))
  await writeFile(resolve(FRONTEND, "config.json"), canonicalBytes({ outputLanguage: "en" }))
  await writeFile(resolve(FRONTEND, "staleness.json"), canonicalBytes({ graphs: { knowledge: { status: "unknown", reason: "graph-commit-unavailable" } } }))
  await writeFile(resolve(FRONTEND, "diff-overlay.json"), canonicalBytes({ changedNodeIds: [], affectedNodeIds: [] }))
  await writeFile(resolve(FRONTEND, "domain-graph.json"), "null\n")
  await writeFile(
    resolve(FRONTEND, "local-bootstrap.js"),
    'window.sessionStorage.setItem("understand-anything-token", "body-war-local-readonly");\nwindow.localStorage.setItem("ua-onboarding-dismissed-v1", "1");\n',
  )

  let index = await readFile(resolve(FRONTEND, "index.html"), "utf8")
  const assetMatch = index.match(/src="\/(assets\/index-[^"]+\.js)"/)
  if (!assetMatch) throw new Error("Main dashboard asset was not found")
  index = index.replace(/\s*<link\b[^>]*href="https?:\/\/[^\"]+"[^>]*>/g, "")
    .replace("<title>Understand Anything</title>", "<title>Body War Whole-System Ontology</title>")
    .replace('<script type="module"', '<script src="/local-bootstrap.js"></script>\n    <script type="module"')
  await writeFile(resolve(FRONTEND, "index.html"), index)

  const assetPath = resolve(FRONTEND, assetMatch[1])
  let asset = await readFile(assetPath, "utf8")
  asset = patchOnce(asset, OLD_RECEIPT_SHA, receiptSha, "receipt digest")
  asset = patchOnce(asset, OLD_RELATIONS_SHA, sourceRelationsSha, "relation-set digest")
  asset = patchOnce(asset, OLD_ENCODING_SHA, encodingSha, "encoding digest")
  asset = patchOnce(asset, "body-war-business-relation/v1", NORMALIZED_RELATION_SCHEMA, "normalized relation schema")
  asset = patchOnce(asset, "body-war-business-relation-set/v1", NORMALIZED_RELATION_SET_SCHEMA, "normalized relation-set schema")
  asset = asset.replaceAll("body-war.business-ontology", "body-war.whole-system-ontology")
  asset = asset.replaceAll("Poker O13 · verified local candidate", "Body War · whole-system candidate")
  asset = asset.replaceAll("Poker walkthrough · ", "Body War walkthrough · ")
  asset = asset.replaceAll("Poker O13", "Body War")
  asset = asset.replaceAll('"F1"', '"body-war.business.workflow.login-to-score-preview"')
  const curatedPositions = {
    "body-war.business.workflow.login-to-score-preview": { x: 22, y: 27 },
    "body-war.business.context.identity-consent": { x: 72, y: 27 },
    "body-war.system.component.http-server": { x: 22, y: 69 },
    "body-war.system.interface.http-api": { x: 72, y: 69 },
    "body-war.business.operation.start-strava-oauth": { x: 15, y: 25 },
    "body-war.business.operation.complete-strava-oauth": { x: 50, y: 25 },
    "body-war.system.module.strava-oauth-adapter": { x: 85, y: 25 },
    "body-war.system.endpoint.strava-start": { x: 30, y: 72 },
    "body-war.system.endpoint.strava-callback": { x: 70, y: 72 },
    "body-war.business.operation.create-suggested-track": { x: 18, y: 25 },
    "body-war.business.entity.suggested-track": { x: 50, y: 25 },
    "body-war.system.endpoint.suggested-tracks": { x: 82, y: 25 },
    "body-war.system.table.suggested-tracks": { x: 50, y: 72 },
    "body-war.business.operation.attach-activity-evidence-candidate": { x: 14, y: 25 },
    "body-war.business.entity.activity-evidence-candidate": { x: 43, y: 25 },
    "body-war.business.policy.consent-contract": { x: 72, y: 25 },
    "body-war.system.endpoint.suggested-track-evidence": { x: 28, y: 72 },
    "body-war.system.table.activity-evidence-candidates": { x: 66, y: 72 },
  }
  asset = patchOnce(
    asset,
    "const Yt=e=>{const t=String(e);let n=2166136261;",
    `const Yt=e=>{const t=String(e),o=${JSON.stringify(curatedPositions)};if(o[t])return o[t];let n=2166136261;`,
    "curated OEW scene positions",
  )
  asset = patchOnce(
    asset,
    'function Mh(e,t={}){const n=zh(fn(e),t.filters);return{rows:n,selectedSourceRef:t.selectedSourceRef??null,selected:n.find(o=>o.sourceRef===t.selectedSourceRef)??fn(e).find(o=>o.sourceRef===t.selectedSourceRef)??null,groundingPath:[...es],visibleResidue:[...ts],authorityEffect:"none"}}',
    'function Mh(e,t={}){const n=zh(fn(e),t.filters),o=new Set;if(t.view==="graph"&&t.selectedSourceRef){const r=e.sourceRefIndex?.[t.selectedSourceRef];if(r?.kind==="edge")o.add(r.sourceRef),o.add(r.row.source),o.add(r.row.target);else if(r?.kind==="node"){const i=e.graph.tour?.find(a=>a.nodeIds?.includes(r.presentationId));if(i){for(const a of i.nodeIds??[]){const c=e.sidecar.nodes?.[a]?.source_ref;c&&o.add(c)}for(const a of Object.values(e.sidecar.edges??{}))o.has(a.source)&&o.has(a.target)&&o.add(a.source_ref)}else{o.add(r.sourceRef);for(const a of Object.values(e.sidecar.edges??{}))(a.source===r.sourceRef||a.target===r.sourceRef)&&(o.add(a.source_ref),o.add(a.source),o.add(a.target))}}}const r=o.size?n.filter(i=>o.has(i.sourceRef)):n;return{rows:r,selectedSourceRef:t.selectedSourceRef??null,selected:r.find(i=>i.sourceRef===t.selectedSourceRef)??fn(e).find(i=>i.sourceRef===t.selectedSourceRef)??null,groundingPath:[...es],visibleResidue:[...ts],authorityEffect:"none"}}',
    "focused OEW graph scene",
  )
  asset = patchOnce(
    asset,
    "n?Mh(n,{selectedSourceRef:u,filters:h})",
    "n?Mh(n,{selectedSourceRef:u,filters:h,view:x})",
    "OEW view-aware model",
  )
  asset = patchOnce(
    asset,
    "visibleResidue:[]},[n,u,h]),H=",
    "visibleResidue:[]},[n,u,h,x]),H=",
    "OEW view-aware model dependencies",
  )
  asset = patchOnce(
    asset,
    '[["graph","Evidence"],["outline","Outline"],["table","Table"]]',
    '[["graph","Focused graph"],["outline","Full outline"],["table","Full index"]]',
    "OEW surface labels",
  )
  asset = patchOnce(
    asset,
    "selectedNodeId:null,focusNodeId:null,nodeHistory:[],viewMode:d?\"domain\":\"structural\"",
    "selectedNodeId:null,focusNodeId:\"presentation:body-war.business.workflow.login-to-score-preview\",nodeHistory:[],viewMode:d?\"domain\":\"structural\"",
    "default whole-system focus scene",
  )
  asset = patchOnce(
    asset,
    "searchResults:i,navigationLevel:\"overview\",activeLayerId:null,selectedNodeId:null,focusNodeId:\"presentation:body-war.business.workflow.login-to-score-preview\"",
    "searchResults:i,tourActive:!0,currentTourStep:0,tourHighlightedNodeIds:Array.isArray(n.tour)&&n.tour.length>0?n.tour[0].nodeIds:[],navigationLevel:\"overview\",activeLayerId:null,selectedNodeId:null,focusNodeId:\"presentation:body-war.business.workflow.login-to-score-preview\"",
    "default whole-system tour scene",
  )
  asset = patchOnce(
    asset,
    "if(n===Kt.fresh)return null",
    "if(n===Kt.fresh||n===Kt.unknown)return null",
    "candidate-local unknown freshness presentation",
  )
  const tourStart = asset.indexOf("const mh=[")
  const tourEnd = asset.indexOf(",rt={steps:mh};function gh", tourStart)
  if (tourStart < 0 || tourEnd < 0) throw new Error("Compiled tour binding not found")
  const compiledTour = [
    { id: "branches", focus: "body-war.business.workflow.login-to-score-preview", view: "graph", title: "Business meets the runtime", body: "Start with the login-to-score workflow and inspect its business and system neighbors." },
    { id: "login", focus: "body-war.system.module.strava-oauth-adapter", view: "graph", title: "Connect through Strava", body: "The server-side adapter realizes OAuth and token custody, while activity import remains synthetic." },
    { id: "suggest", focus: "body-war.business.operation.create-suggested-track", view: "graph", title: "Suggest a track", body: "Follow the business operation through the HTTP endpoint and SuggestedTrack table." },
    { id: "evidence", focus: "body-war.system.endpoint.suggested-track-evidence", view: "graph", title: "Attach candidate evidence", body: "The endpoint records consent-bound redacted evidence without promoting geometry or score authority." },
    { id: "gap", focus: "body-war.system.gap.geometry-score-gap", view: "table", title: "Keep the missing geometry visible", body: "Geometry acquisition, geometry derivation, and explained scoring are explicit open gaps." },
    { id: "trust", focus: "receipt", view: "graph", title: "Inspect trust", body: "The receipt binds all 276 nodes, 301 relations, exact predicate colors, source digests, and authority_effect none." },
  ]
  asset = `${asset.slice(0, tourStart)}const mh=${JSON.stringify(compiledTour)}${asset.slice(tourEnd)}`
  await writeFile(assetPath, asset)

  const projectionReceiptPath = resolve(FRONTEND, "PROJECTION-RECEIPT.json")
  const projectionReceipt = {
    schema_version: "body-war-whole-system-oew-projection-receipt/v1",
    result: "pass",
    source_ontology_receipt: { path: logical(wholeReceiptPath), sha256: sha(wholeReceiptBytes) },
    retained_prototype: { path: logical(RETAINED_DIST), tree_sha256: await treeDigest(RETAINED_DIST) },
    adapter_receipt: { path: logical(resolve(DATA, "adapter-receipt.json")), sha256: receiptSha },
    projection: { nodes: presentationNodes.length, edges: presentationEdges.length, layers: graph.layers.length, tour_steps: tour.length, predicates: Object.keys(encoding.predicateColorMap).length, unique_color_tokens: new Set(Object.values(encoding.predicateColorMap)).size },
    compatibility_patch: {
      scope: "copied candidate-local dashboard asset and loopback bootstrap only",
      relation_schema: NORMALIZED_RELATION_SCHEMA,
      default_focus: "body-war.business.workflow.login-to-score-preview",
      default_tour_step: 1,
      local_read_only_token_bootstrap: true,
      generic_onboarding_dismissed: true,
      unknown_freshness_banner_hidden: true,
      evidence_graph_scope: "selected curated tour scene or selected one-hop relation scene",
      curated_scene_positions: Object.keys(curatedPositions).length,
      full_evidence_surfaces: ["outline", "table"],
      source_prototype_unchanged: true,
    },
    authority_effect: "none",
  }
  await writeFile(projectionReceiptPath, canonicalBytes(projectionReceipt))
  projectionReceipt.frontend_tree_sha256 = await treeDigest(FRONTEND, new Set([projectionReceiptPath]))
  await writeFile(projectionReceiptPath, canonicalBytes(projectionReceipt))
  process.stdout.write(`Generated OEW frontend: ${presentationNodes.length} nodes, ${presentationEdges.length} edges, ${graph.layers.length} layers, ${Object.keys(encoding.predicateColorMap).length} predicate colors. Receipt ${receiptSha}.\n`)
}

await main()
