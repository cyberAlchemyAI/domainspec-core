import assert from "node:assert/strict"
import { createHash } from "node:crypto"
import { readFile, readdir } from "node:fs/promises"
import { dirname, join, resolve } from "node:path"
import { fileURLToPath } from "node:url"

import { canonicalSha256 } from "../../../../../cyberAlchemy-v2/implementation/ontology-evidence-workbench/src/canonical-json.mjs"
import { verifyAdapterReceipt } from "../../../../../cyberAlchemy-v2/implementation/ontology-evidence-workbench/scripts/verify-adapter-receipt.mjs"

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "../../../../../")
const PACKAGE = resolve(ROOT, "projects/body-war/ontology/whole-system")
const FRONTEND = resolve(PACKAGE, "frontend")
const DATA = resolve(FRONTEND, "oew-data")
const RETAINED_DIST = resolve(ROOT, "cyberAlchemy-v2/implementation/ontology-evidence-workbench/generated/runs/SWU-OEWSN-023/20260804T035543Z/dashboard-dist")
const RETAINED_TREE_SHA256 = "38ed5045b9972b1e3dec26074027d04b9ed917adf18804ea39661b315aa6bc93"
const sha = (bytes) => createHash("sha256").update(bytes).digest("hex")
const readJson = async (path) => JSON.parse(await readFile(path, "utf8"))

async function treeDigest(root, ignored = new Set()) {
  const rows = []
  async function walk(directory) {
    for (const entry of (await readdir(directory, { withFileTypes: true })).sort((left, right) => left.name.localeCompare(right.name))) {
      const path = join(directory, entry.name)
      if (entry.isSymbolicLink()) throw new Error(`TREE_SYMLINK:${path}`)
      if (entry.isDirectory()) await walk(path)
      else if (entry.isFile() && !ignored.has(path)) {
        const bytes = await readFile(path)
        rows.push(`${sha(bytes)} ${bytes.length} ${path.slice(root.length + 1)}`)
      }
    }
  }
  await walk(root)
  return sha(`${rows.join("\n")}\n`)
}

async function main() {
  const graphBytes = await readFile(resolve(DATA, "presentation-graph.json"))
  const sidecarBytes = await readFile(resolve(DATA, "evidence-sidecar.json"))
  const receiptBytes = await readFile(resolve(DATA, "adapter-receipt.json"))
  const graph = JSON.parse(graphBytes)
  const sidecar = JSON.parse(sidecarBytes)
  const receipt = JSON.parse(receiptBytes)
  const projection = await readJson(resolve(FRONTEND, "PROJECTION-RECEIPT.json"))
  const sourceReceipt = await readJson(resolve(PACKAGE, "receipts/validation-receipt.json"))

  const adapterVerification = await verifyAdapterReceipt(
    "projects/body-war/ontology/whole-system/frontend/oew-data/adapter-receipt.json",
    { repositoryRoot: ROOT },
  )
  assert.deepEqual(adapterVerification.issues, [])
  assert.equal(adapterVerification.verified, true)
  assert.equal(adapterVerification.receipt_sha256, sha(receiptBytes))

  assert.equal(graph.version, "1.0.0")
  assert.equal(graph.kind, "knowledge")
  assert.equal(graph.nodes.length, 276)
  assert.equal(graph.edges.length, 301)
  assert.equal(graph.layers.length, 29)
  assert.equal(graph.tour.length, 6)
  assert.equal(Object.keys(sidecar.nodes).length, graph.nodes.length)
  assert.equal(Object.keys(sidecar.edges).length, graph.edges.length)
  assert.equal(receipt.authority_effect, "none")
  assert.equal(sourceReceipt.authority_effect, "none")

  const nodeIds = new Set(graph.nodes.map((node) => node.id))
  assert.equal(nodeIds.size, 276)
  assert.deepEqual([...nodeIds].sort(), Object.keys(sidecar.nodes).sort())
  assert.equal(graph.nodes.filter((node) => node.tags.includes("branch:system")).length, 39)
  assert.equal(graph.nodes.filter((node) => !node.tags.includes("branch:system")).length, 237)

  const relationRecords = sidecar.source_relations.relations
  assert.equal(sidecar.source_relations.schema_version, "body-war-whole-system-relation-set/v1")
  assert.equal(relationRecords.length, 301)
  assert.equal(new Set(relationRecords.map((relation) => relation.relation_id)).size, 301)
  const relationCounts = Object.fromEntries([...new Set(relationRecords.map((relation) => relation.source_schema_version))].sort().map((schema) => [schema, relationRecords.filter((relation) => relation.source_schema_version === schema).length]))
  assert.deepEqual(relationCounts, {
    "body-war-business-relation/v1": 231,
    "body-war-business-system-bridge/v1": 25,
    "body-war-system-relation/v1": 45,
  })
  const graphTuples = graph.edges.map((edge) => `${edge.source}\0${edge.type}\0${edge.target}`)
  assert.equal(new Set(graphTuples).size, 301)
  for (const [presentationId, row] of Object.entries(sidecar.edges)) {
    const matches = graph.edges.filter((edge) => edge.source === `presentation:${row.source}` && edge.target === `presentation:${row.target}` && edge.type === row.presentation_relation)
    assert.equal(matches.length, 1, `edge mapping ${presentationId}`)
    assert.equal(matches[0].description, row.source_relation)
  }

  const encoding = sidecar.relation_encoding
  const predicates = [...new Set(relationRecords.map((relation) => relation.predicate))].sort()
  assert.equal(predicates.length, 39)
  assert.deepEqual(Object.keys(encoding.predicateColorMap).sort(), predicates)
  assert.equal(new Set(Object.values(encoding.predicateColorMap)).size, predicates.length)
  assert.equal(new Set(Object.values(encoding.colorTokens).map((token) => token.dark)).size, predicates.length)
  assert.equal(new Set(Object.values(encoding.colorTokens).map((token) => token.light)).size, predicates.length)
  for (const token of Object.values(encoding.colorTokens)) {
    assert.ok(token.dark_contrast >= 4.5)
    assert.ok(token.light_contrast >= 4.5)
  }
  assert.equal(canonicalSha256(sidecar.source_relations), receipt.semantic_fixture.source_relations_sha256)
  assert.equal(canonicalSha256(encoding), receipt.semantic_fixture.relation_encoding_sha256)

  const layered = graph.layers.flatMap((layer) => layer.nodeIds)
  assert.equal(layered.length, 276)
  assert.equal(new Set(layered).size, 276)
  assert.ok(layered.every((id) => nodeIds.has(id)))
  for (const step of graph.tour) assert.ok(step.nodeIds.every((id) => nodeIds.has(id)))
  assert.deepEqual(sidecar.grounding.visible_excluded, ["body-war.system.gap.geometry-score-gap"])
  assert.equal(sidecar.grounding.indeterminate_candidates.length, 3)

  assert.equal(await treeDigest(RETAINED_DIST), RETAINED_TREE_SHA256)
  assert.equal(projection.retained_prototype.tree_sha256, RETAINED_TREE_SHA256)
  assert.equal(projection.frontend_tree_sha256, await treeDigest(FRONTEND, new Set([resolve(FRONTEND, "PROJECTION-RECEIPT.json")])))
  assert.equal(projection.source_ontology_receipt.sha256, sha(await readFile(resolve(PACKAGE, "receipts/validation-receipt.json"))))
  assert.equal(projection.adapter_receipt.sha256, sha(receiptBytes))
  assert.deepEqual(projection.projection, { edges: 301, layers: 29, nodes: 276, predicates: 39, tour_steps: 6, unique_color_tokens: 39 })

  const index = await readFile(resolve(FRONTEND, "index.html"), "utf8")
  const bootstrap = await readFile(resolve(FRONTEND, "local-bootstrap.js"), "utf8")
  const assetPath = resolve(FRONTEND, index.match(/src="\/(assets\/index-[^"]+\.js)"/)[1])
  const asset = await readFile(assetPath, "utf8")
  assert.match(index, /<title>Body War Whole-System Ontology<\/title>/)
  assert.doesNotMatch(index, /https?:\/\//)
  assert.match(index, /<script src="\/local-bootstrap\.js"><\/script>/)
  assert.equal(bootstrap, 'window.sessionStorage.setItem("understand-anything-token", "body-war-local-readonly");\nwindow.localStorage.setItem("ua-onboarding-dismissed-v1", "1");\n')
  assert.match(asset, new RegExp(sha(receiptBytes)))
  assert.match(asset, /body-war-whole-system-relation\/v1/)
  assert.match(asset, /body-war-whole-system-relation-set\/v1/)
  assert.match(asset, /Body War · whole-system candidate/)
  assert.match(asset, /focusNodeId:"presentation:body-war\.business\.workflow\.login-to-score-preview"/)
  assert.match(asset, /tourHighlightedNodeIds:Array\.isArray\(n\.tour\)&&n\.tour\.length>0\?n\.tour\[0\]\.nodeIds:\[\]/)
  assert.match(asset, /if\(n===Kt\.fresh\|\|n===Kt\.unknown\)return null/)
  assert.match(asset, /t\.view==="graph"&&t\.selectedSourceRef/)
  assert.match(asset, /body-war\.business\.workflow\.login-to-score-preview":\{"x":22,"y":27\}/)
  assert.match(asset, /n\?Mh\(n,\{selectedSourceRef:u,filters:h,view:x\}\)/)
  assert.match(asset, /visibleResidue:\[\]\},\[n,u,h,x\]\),H=/)
  assert.match(asset, /Focused graph/)
  assert.match(asset, /Full outline/)
  assert.match(asset, /Full index/)
  assert.doesNotMatch(asset, /Poker O13|Poker walkthrough/)

  process.stdout.write("PASS: Body War whole-system OEW frontend binds 276 nodes, 301 relations, 29 clusters, 39 unique predicate colors, six tour steps, and the visible geometry-score gap.\n")
}

await main()
