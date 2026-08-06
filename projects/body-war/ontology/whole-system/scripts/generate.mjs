import { createHash } from "node:crypto"
import { execFileSync } from "node:child_process"
import { mkdir, readFile, rm, writeFile } from "node:fs/promises"
import { dirname, relative, resolve } from "node:path"
import { fileURLToPath } from "node:url"
import { bridgeRelations, systemLayers, systemNodes, systemRelations } from "../authoring/catalog.mjs"

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "../../../../../")
const PACKAGE = "projects/body-war/ontology/whole-system"
const PACKAGE_ROOT = resolve(ROOT, PACKAGE)
const BUSINESS_ROOT = "projects/body-war/ontology/business"
const OWNER = "body-war.product-ontology-owner"
const SERVER = "projects/body-war/app/server.ts"
const STATIC_UI = "projects/body-war/app/static/app.js"
const TYPES = "projects/body-war/app/src/auth/types.ts"
const MEMORY = "projects/body-war/app/src/auth/memory-repository.ts"
const DRIZZLE = "projects/body-war/app/src/auth/drizzle-repository.ts"
const SCHEMA = "projects/body-war/app/src/infrastructure/postgres/schema.ts"

const digest = (bytes) => createHash("sha256").update(bytes).digest("hex")
const json = (value) => `${JSON.stringify(value, null, 2)}\n`

async function sourceRef(input) {
  const absolute = resolve(ROOT, input.path)
  const bytes = await readFile(absolute)
  const text = bytes.toString("utf8")
  if (!text.includes(input.selector)) {
    throw new Error(`Selector not found: ${input.path} :: ${input.selector}`)
  }
  return { path: input.path, selector: input.selector, sha256: digest(bytes) }
}

async function bindRefs(entries, key) {
  return Promise.all(entries.map(async (entry) => ({
    ...entry,
    [key]: await Promise.all(entry[key].map(sourceRef)),
  })))
}

async function write(path, value) {
  const absolute = resolve(PACKAGE_ROOT, path)
  await mkdir(dirname(absolute), { recursive: true })
  await writeFile(absolute, typeof value === "string" ? value : json(value))
}

function trackedBodyWarFiles() {
  return execFileSync("git", ["ls-files", "-z", "projects/body-war"], { cwd: ROOT })
    .toString("utf8")
    .split("\0")
    .filter(Boolean)
    .filter((path) => !path.startsWith(`${PACKAGE}/`))
    .sort()
}

function classify(path) {
  if (path.startsWith("projects/body-war/app/") || path.startsWith("projects/body-war/infra/")) return "system"
  if (path.startsWith("projects/body-war/ontology/business/")) return "business"
  if (path.startsWith("projects/body-war/proofs/")) return "bridge-proof"
  if (path.startsWith("projects/body-war/domainspec/")) return "specification"
  if (path.startsWith("projects/body-war/docs/")) return "business-evidence"
  if (path.startsWith("projects/body-war/development/")) return "development-evidence"
  if (path.startsWith("projects/body-war/CRAFT/")) return "project-ledger"
  if (path.startsWith("projects/body-war/ontology/")) return "ontology-evidence"
  return "project-context"
}

function mediaType(path) {
  if (path.endsWith(".json")) return "application/json"
  if (path.endsWith(".html")) return "text/html"
  if (path.endsWith(".svg")) return "image/svg+xml"
  if (path.endsWith(".png")) return "image/png"
  if (path.endsWith(".md")) return "text/markdown"
  if (path.endsWith(".ts") || path.endsWith(".js") || path.endsWith(".mjs")) return "text/javascript"
  if (path.endsWith(".yml") || path.endsWith(".yaml")) return "application/yaml"
  return "application/octet-stream"
}

async function treeDigest(paths) {
  const lines = []
  for (const path of paths) {
    const bytes = await readFile(resolve(ROOT, path))
    lines.push(`${digest(bytes)}  ${path}\n`)
  }
  return digest(lines.join(""))
}

async function main() {
  await rm(resolve(PACKAGE_ROOT, "nodes/system"), { recursive: true, force: true })
  await mkdir(resolve(PACKAGE_ROOT, "nodes/system"), { recursive: true })

  const nodes = await Promise.all(systemNodes.map(async (entry) => ({
    schema_version: "body-war-system-node/v1",
    concept_id: entry.concept_id,
    label: entry.label,
    definition: entry.definition,
    concept_role: entry.concept_role,
    system_kind: entry.system_kind,
    branch_roles: ["system"],
    source_refs: await Promise.all(entry.source_refs.map(sourceRef)),
    owner_route: OWNER,
    observation_status: entry.observation_status,
    confidence: {
      evidence_confidence: entry.confidence,
      basis: "Directly bound to the named Body War implementation, test, or deployment selector; ontology inclusion adds no runtime or release authority.",
    },
    residue: entry.residue,
    forbidden_collapse: ["Do not treat this observed system concept as business authority, production proof, deployment, promotion, or release admission."],
  })))
  nodes.sort((a, b) => a.concept_id.localeCompare(b.concept_id))
  for (const entry of nodes) {
    await write(`nodes/system/${entry.concept_id.replace("body-war.system.", "")}.json`, entry)
  }

  const relations = (await bindRefs(systemRelations, "evidence_refs"))
    .map((entry) => ({
      schema_version: "body-war-system-relation/v1",
      ...entry,
      direction: "directed",
      owner_route: OWNER,
      authority_effect: "none",
      forbidden_collapse: ["Do not treat an observed system dependency as a business rule, authority transfer, deployment, promotion, or release admission."],
    }))
    .sort((a, b) => a.relation_id.localeCompare(b.relation_id))

  const bridges = (await Promise.all(bridgeRelations.map(async (entry) => ({
    schema_version: "body-war-business-system-bridge/v1",
    ...entry,
    business_evidence_refs: await Promise.all(entry.business_evidence_refs.map(sourceRef)),
    system_evidence_refs: await Promise.all(entry.system_evidence_refs.map(sourceRef)),
    direction: "directed",
    owner_route: OWNER,
    authority_effect: "none",
    forbidden_collapse: ["This bridge records candidate alignment only; it does not transfer authority, promote either branch, prove production behavior, or close a named gap."],
  })))).sort((a, b) => a.relation_id.localeCompare(b.relation_id))

  const tracked = trackedBodyWarFiles()
  const sourceUniverseEntries = []
  for (const path of tracked) {
    const bytes = await readFile(resolve(ROOT, path))
    sourceUniverseEntries.push({
      path,
      sha256: digest(bytes),
      bytes: bytes.byteLength,
      media_type: mediaType(path),
      evidence_class: classify(path),
    })
  }
  const coverageByClass = Object.fromEntries(
    [...new Set(sourceUniverseEntries.map((entry) => entry.evidence_class))]
      .sort()
      .map((kind) => [kind, sourceUniverseEntries.filter((entry) => entry.evidence_class === kind).length]),
  )

  const businessPaths = tracked.filter((path) => path.startsWith(`${BUSINESS_ROOT}/`))
  const businessManifest = JSON.parse(await readFile(resolve(ROOT, `${BUSINESS_ROOT}/nodes/manifest.json`), "utf8"))
  const businessRelations = JSON.parse(await readFile(resolve(ROOT, `${BUSINESS_ROOT}/relations/relations.json`), "utf8"))
  const businessArtifacts = await Promise.all([
    "profile.json",
    "nodes/manifest.json",
    "relations/relations.json",
    "sources.json",
    "residue.json",
  ].map(async (suffix) => {
    const path = `${BUSINESS_ROOT}/${suffix}`
    const bytes = await readFile(resolve(ROOT, path))
    return { path, sha256: digest(bytes) }
  }))
  const businessView = {
    schema_version: "body-war-branch-view/v1",
    branch_id: "body-war.branch.business",
    branch_role: "business",
    import_mode: "digest-bound-reference",
    imported_package: "body-war.business-ontology",
    imported_tree_sha256: await treeDigest(businessPaths),
    node_count: businessManifest.node_count,
    relation_count: businessRelations.relation_count,
    artifacts: businessArtifacts,
    authority_effect: "none",
  }
  const systemView = {
    schema_version: "body-war-branch-view/v1",
    branch_id: "body-war.branch.system",
    branch_role: "system",
    concepts: nodes.map((entry) => entry.concept_id),
    relations: relations.map((entry) => entry.relation_id),
    layers: systemLayers,
    authority_effect: "none",
  }
  const bridgeView = {
    schema_version: "body-war-branch-view/v1",
    branch_id: "body-war.branch.business-system-bridge",
    branch_role: "bridge",
    business_branch: businessView.branch_id,
    system_branch: systemView.branch_id,
    relations: bridges.map((entry) => entry.relation_id),
    authority_effect: "none",
  }

  const residue = {
    schema_version: "body-war-whole-system-residue/v1",
    entries: [
      { id: "BW-WS-GAP-001", status: "open", label: "Real Strava activity import absent", detail: "Both memory and Postgres repositories return deterministic synthetic activity summaries; OAuth connectivity does not prove activity ownership or live import.", source_refs: [await sourceRef({ path: MEMORY, selector: "fake-activity-" }), await sourceRef({ path: DRIZZLE, selector: "pg-activity-" })] },
      { id: "BW-WS-GAP-002", status: "open", label: "Visible evidence consent control absent", detail: "The browser submits a constant affirmative consent value; the user-visible unchecked consent contract remains unresolved.", source_refs: [await sourceRef({ path: STATIC_UI, selector: "consent_acknowledged: true" })] },
      { id: "BW-WS-GAP-003", status: "open", label: "Geometry and explained score absent", detail: "The runtime stops at redacted evidence and explicitly leaves route geometry unclaimed and composite scoring pending.", source_refs: [await sourceRef({ path: SERVER, selector: "route_geometry: \"deferred\"" }), await sourceRef({ path: SERVER, selector: "composite_score_pending" })] },
      { id: "BW-WS-GAP-004", status: "open", label: "Legacy and repository evidence paths coexist", detail: "The JSON-backed /api/submissions path and repository-backed SuggestedTrack evidence-candidate path have different validation and authority semantics.", source_refs: [await sourceRef({ path: SERVER, selector: "SUBMISSION_STORE" }), await sourceRef({ path: SERVER, selector: "handleSuggestedTrackEvidenceCreate" })] },
      { id: "BW-WS-GAP-005", status: "open", label: "Documented and implemented HTTP surfaces drift", detail: "Design documentation names future routes and /api/profile/me while the observed router exposes a smaller and different surface.", source_refs: [await sourceRef({ path: "projects/body-war/docs/features/troqar-product-architecture/interfaces.md", selector: "/api/profile/me" }), await sourceRef({ path: SERVER, selector: "url.pathname === \"/api/profile\"" })] },
      { id: "BW-WS-GAP-006", status: "open", label: "Database foreign-key constraints are not declared", detail: "Cross-record ownership and identity integrity is currently enforced by application behavior rather than declared database foreign keys.", source_refs: [await sourceRef({ path: SCHEMA, selector: "bodyWarActivityEvidenceCandidates" })] },
      { id: "BW-WS-GAP-007", status: "open", label: "Production compose variants diverge", detail: "The Caddy production compose omits the separate token-protection secret and names a runtime auth-store variable not consumed by the inspected server.", source_refs: [await sourceRef({ path: "projects/body-war/infra/docker-compose.prod.yml", selector: "BODY_WAR_AUTH_STORE" }), await sourceRef({ path: SERVER, selector: "BODY_WAR_TOKEN_PROTECTION_SECRET" })] },
      { id: "BW-WS-GAP-008", status: "open", label: "Structured observability absent", detail: "Named product signals are design intent; observed runtime surfaces are status, health checks, startup console output, deployment receipts, and smoke scripts.", source_refs: [await sourceRef({ path: "projects/body-war/docs/features/troqar-product-architecture/backend.md", selector: "auth.provider.connected" }), await sourceRef({ path: SERVER, selector: "console.log" })] },
      { id: "BW-WS-GAP-009", status: "open", label: "Operator promotion path absent", detail: "Review and source-backed states exist in business and storage models, but no observed operator endpoint implements promotion.", source_refs: [await sourceRef({ path: TYPES, selector: "operator_review" }), await sourceRef({ path: SERVER, selector: "if (url.pathname.startsWith(\"/api/\"))" })] },
      { id: "BW-WS-GAP-010", status: "open", label: "SuggestedTrack proof identifiers differ from business graph identifiers", detail: "The proof ontology and complete business ontology must remain explicitly bridged instead of being merged by similar labels.", source_refs: [await sourceRef({ path: "projects/body-war/proofs/suggested-track-ontology-domainspec/ontology/entries/SuggestedTrack.json", selector: "body-war.ontology.SuggestedTrack" }), await sourceRef({ path: `${BUSINESS_ROOT}/nodes/entity.suggested-track.json`, selector: "body-war.business.entity.suggested-track" })] },
    ],
  }

  const profile = {
    schema_version: "body-war-whole-system-ontology-profile/v1",
    package_id: "body-war.whole-system-ontology",
    label: "Body War whole-system ontology",
    ontology_type: "business-system-bridge",
    status: "candidate-local",
    authority_effect: "none",
    release_admission: "not-granted",
    owner_route: OWNER,
    claim_ceiling: "Digest-bound candidate view of the complete tracked Body War evidence universe, its existing business ontology, the directly observed prototype system, and evidence-backed branch alignments and gaps.",
    branches: [businessView.branch_id, systemView.branch_id, bridgeView.branch_id],
    source_universe_contract: {
      inclusion: "Every Git-tracked file under projects/body-war at generation time, excluding this generated whole-system package to avoid self-reference.",
      exclusions: ["untracked files", "ignored files", "runtime data", "dependencies", "secrets", `${PACKAGE}/**`],
      semantic_policy: "Complete evidence coverage does not mean one semantic node per file; nodes represent source-backed concepts and the source universe preserves the remaining evidence surface.",
    },
    imported_business_tree_sha256: businessView.imported_tree_sha256,
    forbidden_claims: ["canonical ontology promotion", "DomainSpec executable admission", "live Strava activity import", "source-backed geometry", "explained or verified scoring", "production readiness"],
  }

  await write("profile.json", profile)
  await write("nodes/manifest.json", { schema_version: "body-war-system-node-manifest/v1", node_count: nodes.length, concept_ids: nodes.map((entry) => entry.concept_id) })
  await write("relations/system-relations.json", { schema_version: "body-war-system-relations/v1", relation_count: relations.length, relations })
  await write("relations/bridge-relations.json", { schema_version: "body-war-business-system-bridges/v1", relation_count: bridges.length, relations: bridges })
  await write("views/business.json", businessView)
  await write("views/system.json", systemView)
  await write("views/bridge.json", bridgeView)
  await write("source-universe.json", { schema_version: "body-war-source-universe/v1", scope: "projects/body-war", generated_from: "git ls-files", exclusion_root: `${PACKAGE}/`, file_count: sourceUniverseEntries.length, coverage_by_class: coverageByClass, tree_sha256: await treeDigest(tracked), entries: sourceUniverseEntries })
  await write("residue.json", residue)
  await write("architecture-map.json", { schema_version: "body-war-system-architecture-map/v1", observation_status: "observed-with-explicit-gaps", layers: systemLayers, dependencies: relations.map(({ relation_id, predicate, source_concept, target_concept, observation_status }) => ({ relation_id, predicate, source_concept, target_concept, observation_status })), tests: nodes.filter((entry) => entry.system_kind === "test").map((entry) => entry.concept_id), deployment_units: nodes.filter((entry) => entry.system_kind === "deployment_unit").map((entry) => entry.concept_id), open_residue: residue.entries.map((entry) => entry.id) })

  const bridgeBytes = await readFile(resolve(PACKAGE_ROOT, "relations/bridge-relations.json"))
  const nodeDigest = async (id) => digest(await readFile(resolve(PACKAGE_ROOT, `nodes/system/${id.replace("body-war.system.", "")}.json`)))
  const contextPack = {
    schema_version: "body-war-context-pack/v1",
    task: "Implement and test the login-to-explained-score prototype without exceeding geometry, scoring, privacy, or authority evidence.",
    obligations: [
      { id: "BW-CTX-001", obligation: "Preserve authentication, browser-session, CSRF, origin, and server-only token boundaries.", sources: [{ path: `${BUSINESS_ROOT}/nodes/capability.auth-consent.json`, selector: "body-war.business.capability.auth-consent", sha256: digest(await readFile(resolve(ROOT, `${BUSINESS_ROOT}/nodes/capability.auth-consent.json`))) }, { path: `${PACKAGE}/nodes/system/module.browser-session-adapter.json`, selector: "body-war.system.module.browser-session-adapter", sha256: await nodeDigest("body-war.system.module.browser-session-adapter") }] },
      { id: "BW-CTX-002", obligation: "Reuse the observed SuggestedTrack and evidence-candidate path and keep consent explicit.", sources: [{ path: `${BUSINESS_ROOT}/nodes/workflow.suggested-track-expansion.json`, selector: "body-war.business.workflow.suggested-track-expansion", sha256: digest(await readFile(resolve(ROOT, `${BUSINESS_ROOT}/nodes/workflow.suggested-track-expansion.json`))) }, { path: `${PACKAGE}/nodes/system/endpoint.suggested-track-evidence.json`, selector: "body-war.system.endpoint.suggested-track-evidence", sha256: await nodeDigest("body-war.system.endpoint.suggested-track-evidence") }] },
      { id: "BW-CTX-003", obligation: "Acquire and derive source-bound activity geometry before any geometry or score claim.", sources: [{ path: `${BUSINESS_ROOT}/nodes/operation.fetch-selected-activity-geometry.json`, selector: "body-war.business.operation.fetch-selected-activity-geometry", sha256: digest(await readFile(resolve(ROOT, `${BUSINESS_ROOT}/nodes/operation.fetch-selected-activity-geometry.json`))) }, { path: `${PACKAGE}/nodes/system/gap.geometry-score-gap.json`, selector: "body-war.system.gap.geometry-score-gap", sha256: await nodeDigest("body-war.system.gap.geometry-score-gap") }] },
      { id: "BW-CTX-004", obligation: "Build a policy-bound score input snapshot and explained preview; do not present it as verified control or source-backed track authority.", sources: [{ path: `${BUSINESS_ROOT}/nodes/operation.calculate-score-preview.json`, selector: "body-war.business.operation.calculate-score-preview", sha256: digest(await readFile(resolve(ROOT, `${BUSINESS_ROOT}/nodes/operation.calculate-score-preview.json`))) }, { path: `${PACKAGE}/relations/bridge-relations.json`, selector: "body-war.bridge.score-preview-gap", sha256: digest(bridgeBytes) }] },
    ],
    unresolved_residue: ["BW-WS-GAP-001", "BW-WS-GAP-002", "BW-WS-GAP-003", "BW-WS-GAP-008", "BW-WS-GAP-009"],
    authority_effect: "none",
  }
  await write("context/context-pack.json", contextPack)
  await write("context/context-pack.md", renderContext(contextPack))
  await write("NODE-INDEX.md", renderIndex({ profile, businessView, nodes, relations, bridges, sourceUniverseEntries, coverageByClass, residue }))

  process.stdout.write(`Generated ${nodes.length} system nodes, ${relations.length} system relations, ${bridges.length} bridges, and ${sourceUniverseEntries.length} source records.\n`)
}

function renderContext(pack) {
  const lines = ["# Body War implementation context pack", "", `Task: ${pack.task}`, "", "## Obligations", ""]
  for (const item of pack.obligations) {
    lines.push(`### ${item.id}`, "", item.obligation, "")
    for (const source of item.sources) lines.push(`- \`${source.path}\` — \`${source.selector}\` — \`${source.sha256}\``)
    lines.push("")
  }
  lines.push("## Open residue", "", ...pack.unresolved_residue.map((id) => `- \`${id}\``), "", "Authority effect: none. This pack selects evidence; it does not authorize implementation or promotion.", "")
  return lines.join("\n")
}

function renderIndex({ profile, businessView, nodes, relations, bridges, sourceUniverseEntries, coverageByClass, residue }) {
  const lines = [
    "# Body War whole-system ontology", "",
    `Status: \`${profile.status}\` · Type: \`${profile.ontology_type}\` · Authority effect: \`${profile.authority_effect}\``, "",
    "This package keeps the existing business ontology intact, adds an observed system branch, and connects them with evidence-backed bridge relations. The source universe covers every tracked Body War file at generation time; semantic nodes remain selective so the graph represents concepts instead of becoming a file browser.", "",
    "## Coverage", "",
    `- Imported business branch: **${businessView.node_count} nodes**, **${businessView.relation_count} relations**`,
    `- Observed system branch: **${nodes.length} nodes**, **${relations.length} relations**`,
    `- Business-system bridge: **${bridges.length} relations**`,
    `- Tracked source universe: **${sourceUniverseEntries.length} files**`,
    `- Open residue: **${residue.entries.length} explicit gaps**`, "",
    "## Read the branches", "",
    "```mermaid", "flowchart LR", "  B[Business meaning\\nexisting 237-node graph] -->|realized_by / tested_by / drifts_from| S[Observed system\\nruntime, persistence, tests, deployment]", "  U[Complete tracked source universe] -->|supports| B", "  U -->|supports| S", "  G[Open residue] -. constrains .-> S", "```", "",
    "## System layers", "",
    "| Layer | Nodes |", "| --- | ---: |",
    ...systemLayers.map((layer) => `| ${layer.label} | ${layer.concepts.length} |`), "",
    "## System nodes", "", "| Kind | Node | Meaning | Status |", "| --- | --- | --- | --- |",
    ...nodes.map((entry) => `| ${entry.system_kind} | \`${entry.concept_id}\` | ${entry.definition} | ${entry.observation_status} |`), "",
    "## Relations as sentences", "",
    ...relations.map((entry) => `- **${entry.source_concept}** — \`${entry.predicate}\` → **${entry.target_concept}**.`), "",
    "## Business-system bridges", "",
    ...bridges.map((entry) => `- **${entry.business_concept}** — \`${entry.predicate}\` → **${entry.system_concept}** (${entry.alignment_status}). ${entry.note}`), "",
    "## Open gaps", "",
    ...residue.entries.map((entry) => `- **${entry.id} — ${entry.label}:** ${entry.detail}`), "",
    "## Source coverage", "", "| Evidence class | Files |", "| --- | ---: |",
    ...Object.entries(coverageByClass).map(([kind, count]) => `| ${kind} | ${count} |`), "",
    "See `source-universe.json` for every path, byte count, class, and SHA-256 digest. See `context/context-pack.md` for a strict login-to-score implementation selection.", "",
  ]
  return lines.join("\n")
}

await main()
